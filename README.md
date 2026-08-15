# Ten Days to Thirty — setup notes

## What this is
A private website with an interactive world map. Each day, a new pin lights
up over someone's city and a gold thread reaches toward Texas. Clicking an
unlocked pin opens their letter, photo, or video. Day 10, her birthday, is
your gift list.

## The one rule

`content.js` holds the letters and the photo/video links **in plain text**.
It is gitignored and must never be committed. What gets published is
`content.enc`, the same file encrypted with the passcode.

That matters because the repo and the published site are both public.
Before, anyone could open `.../content.js` in a browser and read every
letter and every Drive link without a password. Now that file isn't on the
server at all — only ciphertext is.

**Every time you edit `content.js`, run:**

```
node build.js
```

Then commit `content.enc`. If you forget, the site keeps showing the old
content, because the site never reads `content.js`.

## Before you publish

**1. Edit `content.js`**
This is the only file you'll touch regularly. Each person is one block with
placeholder text in it right now. As people send you their letters, photos,
or videos, paste them in. The file's own header has the full field guide.

- Text letter: just replace the placeholder string.
- Photo: `content: { src: "...", caption: "..." }`
- Video: `content: { embedUrl: "...", caption: "..." }`
- Several things from one person: use an `items: [ ... ]` array.

Do **not** put real photos or videos in this repo. Host them and link:

| | link to use |
|---|---|
| Drive photo | `https://drive.google.com/thumbnail?id=FILE_ID&sz=w1200` |
| Drive video | `https://drive.google.com/file/d/FILE_ID/preview` |
| YouTube video | `https://www.youtube.com/embed/VIDEO_ID` (upload as *unlisted*) |

Get `FILE_ID` from the Drive share link, the part between `/d/` and `/view`.
**The file must be shared as "Anyone with the link"** or it shows up broken.
Pasting the `/view` link itself will not work — that's a web page, not an image.

**2. Confirm two open details**
- Miro: Portugal or Spain, and which city, then update `city`, `country`,
  `lat`, `lon` for that entry.
- Your own city in Texas, and Ero's and Marina Atef's actual cities, currently
  placeholders (Houston, Austin, generic Texas center).

**3. Double check the dates**
`COUNTDOWN.startDate` and `endDate` in `content.js` should be set so day 10
lands on her birthday. Day 1 unlocks on the start date automatically,
nothing else to configure.

**4. Change the passcode if you want**
It's currently `mina`, edit `COUNTDOWN.passcode` in `content.js`.

## Publishing to GitHub Pages

1. Create a new repository on GitHub (keep it public, or private if you're
   on a paid plan, Pages works with either).
2. Upload these files to it: `index.html`, `content.js`, `sw.js`, and this
   `README.md` (plus a `photos/` folder if you added any images).
3. In the repo, go to **Settings → Pages**.
4. Under **Build and deployment**, set **Source** to "Deploy from a branch",
   branch `main`, folder `/ (root)`. Save.
5. GitHub gives you a link, something like
   `https://yourusername.github.io/repo-name/`. That's the link you send her
   on day 1.

GitHub Pages tells browsers they're allowed to cache `index.html` for up to
10 minutes, so a fresh edit can take a little while to show up on its own.
`sw.js` is a small service worker that fixes this: after someone's first
visit, it takes over and forces every later visit to fetch fresh from the
network, so edits show up immediately after that. `content.js` also gets a
cache-busting query string on every load for the same reason. First visit
ever can still lag up to 10 minutes behind a brand new deploy; every visit
after that is instant.

## Sending her the daily nudge
The site unlocks pins automatically based on the date, so nothing needs to
run on a schedule. Each morning, just send her a quick text or email:
"check the map" with the link. That part's on you, and it's better coming
from you than a notification anyway.

## A note on privacy
The passcode screen keeps this from being wide open to anyone who stumbles
on the link, but it isn't bank-vault security, don't rely on it for anything
truly sensitive.
