"""Daily "a new light is lit" email for Ellen's countdown.

Runs once a day from an EventBridge schedule. Works out which day of the
countdown today is, and emails her a nudge with a link to the map. Sends
nothing before the countdown starts or after it ends, so the schedule can
be left switched on and forgotten.

Sends through Gmail's SMTP server rather than SES. Gmail publishes a DMARC
policy, so mail claiming to come from a gmail.com address but sent by
Amazon fails authentication and is discarded silently — no bounce, nothing
in the spam folder. Sending through Gmail itself means the message really
does come from that account, so it authenticates and arrives.

Environment variables (set these on the Lambda):
    START_DATE    first day of the countdown, e.g. 2026-09-17
    SITE_URL      link to the site
    TO_EMAIL      her address
    FROM_EMAIL    the Gmail address the app password belongs to
    GMAIL_APP_PASSWORD  16-character app password, no spaces
    HER_NAME      defaults to Ellen
    FROM_NAME     name she sees in her inbox, defaults to Mina
    TEST_DAY      optional, forces a day for testing
"""

import os
import datetime
import smtplib
import zoneinfo
from email.message import EmailMessage

TIMEZONE = zoneinfo.ZoneInfo("America/Chicago")
TOTAL_DAYS = 10
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

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


def resolve_day(event, start_date, today):
    """Decide which day to send, honouring the test overrides.

    Order of precedence, so a console test can always win:
      1. "day" in the test event payload
      2. TEST_DAY environment variable
      3. today's real position in the countdown

    Returns the day number, or 0 meaning send nothing.
    """
    override = None
    source = None

    if isinstance(event, dict) and event.get("day") is not None:
        override = event["day"]
        source = "event payload"
    elif os.environ.get("TEST_DAY", "").strip():
        override = os.environ["TEST_DAY"].strip()
        source = "TEST_DAY variable"

    if override is None:
        return current_day(start_date, today)

    try:
        day = int(override)
    except (TypeError, ValueError):
        print(f"ignoring bad day override {override!r} from {source}")
        return current_day(start_date, today)

    if not 1 <= day <= TOTAL_DAYS:
        print(f"ignoring out-of-range day {day} from {source}")
        return current_day(start_date, today)

    print(f"TEST: forcing day {day} from {source}")
    return day


def lambda_handler(event, context):
    """Send today's email, if today is part of the countdown.

    For testing, force a specific day either by setting the TEST_DAY
    environment variable, or by running a test with {"day": 3} as the
    event. Remove TEST_DAY before the real run or every scheduled email
    will announce the same day.
    """
    start_date = datetime.date.fromisoformat(os.environ["START_DATE"])
    site_url = os.environ["SITE_URL"]
    to_email = os.environ["TO_EMAIL"]
    from_email = os.environ["FROM_EMAIL"]
    name = os.environ.get("HER_NAME", "Ellen")

    # Use her local date, not the Lambda's UTC date, or the mail arrives
    # on the wrong day for anything scheduled near midnight.
    today = datetime.datetime.now(TIMEZONE).date()
    day = resolve_day(event, start_date, today)

    if day == 0:
        print(f"{today}: outside the countdown, nothing sent")
        return {"sent": False, "day": 0}

    teaser = TEASERS.get(day, "A new light is lit.")
    subject = (
        f"Happy birthday, {name}"
        if day == TOTAL_DAYS
        else f"Day {day} of {TOTAL_DAYS} is open"
    )

    # A bare address reads as bulk mail. Sending as a person helps this
    # land in the inbox rather than the spam folder.
    sender_name = os.environ.get("FROM_NAME", "Mina")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = f"{sender_name} <{from_email}>"
    message["To"] = to_email

    # Plain text first, then HTML. Mail clients show the last part they
    # can render, so this gives HTML to those that support it and a
    # readable message to those that do not.
    message.set_content(
        f"{name}, a new light is lit.\n\n"
        f"{teaser}\n\n"
        f"Open the map here:\n{site_url}\n\n"
        f"— {sender_name}"
    )
    message.add_alternative(
        build_html(name, day, teaser, site_url), subtype="html"
    )

    # App passwords are sometimes copied with the spaces Google shows.
    password = os.environ["GMAIL_APP_PASSWORD"].replace(" ", "")

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20) as smtp:
            smtp.login(from_email, password)
            smtp.send_message(message)
    except smtplib.SMTPAuthenticationError:
        print(
            "Gmail rejected the login. Check GMAIL_APP_PASSWORD is an app "
            "password (not the account password) and that it belongs to "
            f"{from_email}."
        )
        raise
    except OSError as error:
        print(f"Could not reach Gmail to send day {day}: {error}")
        raise

    print(f"{today}: sent day {day} to {to_email}")
    return {"sent": True, "day": day}
