# Daily email

One Lambda, on a daily schedule, that emails Ellen when a new light is lit.
It works out the day number from the date, and sends nothing before the
countdown starts or after it ends — so you can set it up once and leave it.

Day 1 is `START_DATE`. Day 10 is nine days later, her birthday.

## Before you start

SES begins in **sandbox mode**, where it will only send to addresses you
have verified. That is fine here, but it means you must verify **both**
your sender address and hers, and she has to click a confirmation link.

If you would rather she not get a "verify this address" email, request
production access in the SES console instead. It usually takes a day.

## 1. Verify the addresses

SES console → **Identities** → *Create identity* → Email address.
Do this twice: once for the address you send from, once for hers.
Both must show **Verified** before anything will send.

## 2. Create the Lambda

Lambda console → *Create function* → Author from scratch.

- Runtime: **Python 3.12**
- Name: `ellen-countdown-notify`

Paste in `lambda_function.py` and click **Deploy**.

Under **Configuration → General**, set the timeout to **30 seconds**.
The default of 3 is tight if SES is slow to answer.

## 3. Environment variables

Configuration → **Environment variables**:

| Key | Value |
|---|---|
| `START_DATE` | `2026-09-17` |
| `SITE_URL` | `https://minaw92.github.io/countdown/` |
| `TO_EMAIL` | her address |
| `FROM_EMAIL` | your verified sender |
| `HER_NAME` | `Ellen` |

`START_DATE` must match `startDate` in `content.js`, or the email will
announce a different day from the one the site actually opens.

## 4. Let it use SES

Configuration → **Permissions** → click the execution role → *Add
permissions* → *Create inline policy* → JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ses:SendEmail",
      "Resource": "*"
    }
  ]
}
```

## 5. Schedule it

EventBridge console → **Schedules** → *Create schedule*.

- Occurrence: **Recurring**, cron-based
- Expression: `cron(0 8 * * ? *)`
- Time zone: **America/Chicago**
- Target: your Lambda

That sends at 8am her time. The Lambda reads the date in that same zone,
so the day number always matches what the site shows her.

## Test it

In the Lambda console, **Test** with any event. With today outside the
countdown it will log `outside the countdown, nothing sent` and send
nothing — that is correct.

To see a real email, temporarily set `START_DATE` to today, test again,
then set it back.

## If it does not arrive

- Check her spam folder first, it is usually that
- Both addresses **Verified** in SES?
- CloudWatch Logs for the function will show the reason
- `MessageRejected` almost always means an unverified address
