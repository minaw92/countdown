# Ten Days to Thirty — setup notes

## What this is
A private website with an interactive world map. Each day, a new pin lights
up over someone's city and a gold thread reaches toward Texas. Clicking an
unlocked pin opens their letter, photo, or video. Day 10, her birthday, is
your gift list.

## Before you publish

**1. Edit `content.js`**
This is the only file you'll touch regularly. Each person is one block with
placeholder text in it right now. As people send you their letters, photos,
or videos, paste them in.

- Text letter: just replace the placeholder string.
- Photo: change `type` to `"photo"` and set `content: { src: "...", caption: "..." }`.
  Put the actual image file in this same folder (e.g. `photos/sister.jpg`) and
  point `src` to it, or use a direct image link.
- Video: change `type` to `"video"` and set `content: { embedUrl: "...", caption: "..." }`.
  Easiest source is an *unlisted* YouTube video, use the embed link, it looks
  like `https://www.youtube.com/embed/VIDEO_ID`.

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
2. Upload these files to it: `index.html`, `app.html`, `content.js`, and this
   `README.md` (plus a `photos/` folder if you added any images).
3. In the repo, go to **Settings → Pages**.
4. Under **Build and deployment**, set **Source** to "Deploy from a branch",
   branch `main`, folder `/ (root)`. Save.
5. GitHub gives you a link, something like
   `https://yourusername.github.io/repo-name/`. That's the link you send her
   on day 1.

`index.html` is a small loader, it just fetches `app.html` fresh on every
visit so nobody gets stuck looking at a cached, outdated page. `app.html` is
the actual site. Every time you edit `content.js` or `app.html` and
re-upload, the live site updates immediately, no waiting on cache.

## Sending her the daily nudge
The site unlocks pins automatically based on the date, so nothing needs to
run on a schedule. Each morning, just send her a quick text or email:
"check the map" with the link. That part's on you, and it's better coming
from you than a notification anyway.

## A note on privacy
The passcode screen keeps this from being wide open to anyone who stumbles
on the link, but it isn't bank-vault security, don't rely on it for anything
truly sensitive.
