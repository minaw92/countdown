"""Daily "a new light is lit" email for Ellen's countdown.

Runs once a day from an EventBridge schedule. Works out which day of the
countdown today is, and emails her a nudge with a link to the map. Sends
nothing before the countdown starts or after it ends, so the schedule can
be left switched on and forgotten.

Environment variables (set these on the Lambda):
    START_DATE   first day of the countdown, e.g. 2026-09-17
    SITE_URL     link to the site
    TO_EMAIL     her address
    FROM_EMAIL   a verified SES sender
    HER_NAME     defaults to Ellen
"""

import os
import datetime
import zoneinfo

import boto3
from botocore.exceptions import ClientError

TIMEZONE = zoneinfo.ZoneInfo("America/Chicago")
TOTAL_DAYS = 10

# A different line each morning so the ten emails do not read identically.
TEASERS = {
    1: "The first light is lit.",
    2: "Someone else just showed up on the map.",
    3: "A third light, from somewhere far away.",
    4: "Another one. The map is filling in.",
    5: "Halfway. Five people so far.",
    6: "Another light, another person who thought of you.",
    7: "Seven. Three left.",
    8: "The map is nearly full.",
    9: "One more after this one.",
    10: "Happy birthday. The last light is yours.",
}


def current_day(start_date: datetime.date, today: datetime.date) -> int:
    """Return which countdown day today is, or 0 before it starts.

    Day 1 falls on the start date, so a difference of zero days is day 1.
    Anything past the final day returns 0 as well, so nothing is sent.
    """
    difference = (today - start_date).days
    if difference < 0:
        return 0
    day = difference + 1
    if day > TOTAL_DAYS:
        return 0
    return day


def build_html(name: str, day: int, teaser: str, site_url: str) -> str:
    """Build the HTML body, styled to match the site."""
    is_final = day == TOTAL_DAYS
    heading = "Happy birthday" if is_final else f"Day {day}"
    button = "Open your gift" if is_final else "See who it is"

    return f"""<!doctype html>
<html>
  <body style="margin:0;padding:0;background:#12162a;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
           style="background:#12162a;padding:40px 20px;">
      <tr>
        <td align="center">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
                 style="max-width:480px;background:#1a2044;border:1px solid rgba(217,168,87,.25);
                        border-radius:14px;padding:36px 30px;">
            <tr>
              <td style="font-family:Georgia,serif;color:#d9a857;font-size:12px;
                         letter-spacing:.2em;text-transform:uppercase;padding-bottom:14px;">
                {heading}
              </td>
            </tr>
            <tr>
              <td style="font-family:Georgia,serif;color:#f3ecdd;font-size:26px;
                         padding-bottom:16px;">
                {name}, a new light is lit.
              </td>
            </tr>
            <tr>
              <td style="font-family:Helvetica,Arial,sans-serif;color:#cfc6ae;
                         font-size:15px;line-height:1.7;padding-bottom:28px;">
                {teaser}
              </td>
            </tr>
            <tr>
              <td>
                <a href="{site_url}"
                   style="display:inline-block;background:#d9a857;color:#12162a;
                          font-family:Helvetica,Arial,sans-serif;font-size:15px;
                          text-decoration:none;padding:13px 26px;border-radius:8px;">
                  {button}
                </a>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>"""


def lambda_handler(event, context):
    """Send today's email, if today is part of the countdown."""
    start_date = datetime.date.fromisoformat(os.environ["START_DATE"])
    site_url = os.environ["SITE_URL"]
    to_email = os.environ["TO_EMAIL"]
    from_email = os.environ["FROM_EMAIL"]
    name = os.environ.get("HER_NAME", "Ellen")

    # Use her local date, not the Lambda's UTC date, or the mail arrives
    # on the wrong day for anything scheduled near midnight.
    today = datetime.datetime.now(TIMEZONE).date()
    day = current_day(start_date, today)

    if day == 0:
        print(f"{today}: outside the countdown, nothing sent")
        return {"sent": False, "day": 0}

    teaser = TEASERS.get(day, "A new light is lit.")
    subject = (
        f"Happy birthday, {name}"
        if day == TOTAL_DAYS
        else f"Day {day} of {TOTAL_DAYS} is open"
    )

    client = boto3.client("ses")
    try:
        response = client.send_email(
            Source=from_email,
            Destination={"ToAddresses": [to_email]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {
                    "Html": {
                        "Data": build_html(name, day, teaser, site_url),
                        "Charset": "UTF-8",
                    },
                    "Text": {
                        "Data": f"{teaser}\n\n{site_url}",
                        "Charset": "UTF-8",
                    },
                },
            },
        )
    except ClientError as error:
        print(f"SES refused to send day {day}: {error}")
        raise

    print(f"{today}: sent day {day}, message {response['MessageId']}")
    return {"sent": True, "day": day, "messageId": response["MessageId"]}
