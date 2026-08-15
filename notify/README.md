# Daily email

One Lambda, on a daily schedule, that emails Ellen when a new light is lit.
It works out the day number from the date, and sends nothing before the
countdown starts or after it ends — so you can set it up once and leave it.

Day 1 is `START_DATE`. Day 10 is nine days later, her birthday.

## Why Gmail and not SES

This started on SES and the mail never arrived — no bounce, nothing in
spam, while SES reported successful delivery every time.

The cause is DMARC. Gmail publishes a policy saying only Google may send
mail from a `@gmail.com` address. Mail claiming to be from your Gmail but
sent by Amazon fails that check and receiving servers discard it silently.
Nothing in the AWS config can fix it — the only SES route is a domain you
own, with DKIM set up.

Sending through Gmail's own SMTP server means the mail genuinely comes
from that account, so it authenticates and lands in the inbox. Gmail
allows around 500 a day; this needs ten.

## 1. Create a Gmail app password

An app password is a 16-character code that lets a program sign in to your
Gmail without your real password.

1. The account needs **2-Step Verification** switched on
2. Go to **myaccount.google.com/apppasswords**
3. Name it something like `countdown`, and create it
4. Copy the 16 characters — Google only shows it once

It is a live credential to your email account. Keep it out of the repo, and
delete it at **myaccount.google.com/apppasswords** once the ten days are
over.

## 2. Create the Lambda

Lambda console → *Create function* → Author from scratch.

- Runtime: **Python 3.12**
- Name: `send_email`

Paste in `lambda_function.py` and click **Deploy**.

Under **Configuration → General**, set the timeout to **30 seconds**.
The default of 3 seconds is not enough to open an SMTP connection.

## 3. Environment variables

Configuration → **Environment variables**:

| Key | Value |
|---|---|
| `START_DATE` | `2026-09-17` |
| `SITE_URL` | `https://minaw92.github.io/countdown/` |
| `TO_EMAIL` | her address |
| `FROM_EMAIL` | the Gmail the app password belongs to |
| `GMAIL_APP_PASSWORD` | the 16 characters from step 1 |
| `HER_NAME` | `Ellen` |
| `FROM_NAME` | `Mina` — the name she sees in her inbox |
| `TEST_DAY` | leave unset — see *Test it* below |

`START_DATE` must match `startDate` in `content.js`, or the email will
announce a different day from the one the site actually opens.

`FROM_EMAIL` must be the same account the app password came from. Gmail
will not let you send as a different address.

No IAM permissions are needed — the function talks to Gmail, not to any
AWS service.

## 5. Schedule it

EventBridge console → **Schedules** → *Create schedule*.

- Occurrence: **Recurring**, cron-based
- Expression: `cron(0 8 * * ? *)`
- Time zone: **America/Chicago**
- Target: your Lambda

That sends at 8am her time. The Lambda reads the date in that same zone,
so the day number always matches what the site shows her.

## Test it

Out of season the function sends nothing, which makes it awkward to check.
So you can force a day two ways.

**Either** run a test with this event, in the Lambda console's *Test* tab:

```json
{ "day": 3 }
```

**Or** add an environment variable and press *Test* with any event:

| Key | Value |
|---|---|
| `TEST_DAY` | `3` |

Both send that day's email immediately, whatever today's date is. Use `10`
to see the birthday version. The event payload wins if you set both.

Anything invalid — a word, `0`, a number above 10 — is ignored with a note
in the logs, and it falls back to the real date rather than sending
something wrong.

> **Delete `TEST_DAY` when you are done.** While it is set, every
> scheduled email announces that same day. The event payload does not have
> this problem, since the scheduler sends its own event — which is the
> safer of the two if you are likely to forget.

With no override and today outside the countdown, the log reads
`outside the countdown, nothing sent`. That is correct, not a failure.

## If it does not arrive

Read the log first. Gmail either accepts the message or refuses the
connection, so the log usually says plainly which happened.

**`sent day 3 to ...`** — Gmail accepted it. Check the inbox, then Spam,
then search `in:anywhere "light is lit"`. Plain Gmail search skips All
Mail, Spam and Trash, so use `in:anywhere`.

**`Gmail rejected the login`** — the app password is wrong. Common causes:

- It is the account password, not an app password
- It belongs to a different account than `FROM_EMAIL`
- It was revoked, or 2-Step Verification was switched off
- Extra characters were pasted; the code strips spaces, but nothing else

**`Could not reach Gmail`** — a network or timeout problem. Confirm the
timeout is 30 seconds, not the default 3.

**Timed out with no log line at all** — almost always the 3 second
default timeout. Raise it.

### Sending to yourself

If `FROM_EMAIL` and `TO_EMAIL` are the same address, Gmail often keeps
the copy out of the inbox and files it under All Mail instead. That is
Gmail deduplicating, not a failure. Test with a different address if you
can, or search `in:anywhere`.

### Before the real run

Send yourself a test a few days early and confirm it reaches the inbox
rather than spam.
