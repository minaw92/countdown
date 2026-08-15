/* ============================================================
   BUILD — encrypts content.js into content.enc
   ------------------------------------------------------------
   Run this whenever you edit content.js:

       node build.js

   It reads the passcode out of content.js, encrypts the whole
   file with it, and writes content.enc. Commit content.enc.
   NEVER commit content.js — it is listed in .gitignore.

   The published site only ever downloads content.enc, which is
   meaningless without the passcode, so the Drive links, videos
   and letters are not readable by anyone who finds the URL.
   ============================================================ */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const SRC = path.join(__dirname, "content.js");
const OUT = path.join(__dirname, "content.enc");

// Must match the values used by the browser in index.html
const ITERATIONS = 250000;
const KEY_LENGTH = 32;
const DIGEST = "sha256";

function fail(message) {
  console.error("\n  ERROR: " + message + "\n");
  process.exit(1);
}

if (!fs.existsSync(SRC)) {
  fail("content.js not found. It must sit next to this script.");
}

const source = fs.readFileSync(SRC, "utf8");

// Pull the passcode straight out of content.js so there is only one
// place to change it.
const match = source.match(/passcode:\s*["'](.+?)["']/);
if (!match) {
  fail('Could not find a passcode in content.js (expected  passcode: "..." ).');
}
const passcode = match[1];

if (!passcode.trim()) {
  fail("The passcode in content.js is empty.");
}

// Fresh salt and IV every build so the same content never encrypts
// to the same bytes twice.
const salt = crypto.randomBytes(16);
const iv = crypto.randomBytes(12);
const key = crypto.pbkdf2Sync(passcode, salt, ITERATIONS, KEY_LENGTH, DIGEST);

const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
const ciphertext = Buffer.concat([cipher.update(source, "utf8"), cipher.final()]);
const tag = cipher.getAuthTag();

// salt + iv + tag + ciphertext, base64 encoded as one blob
const payload = Buffer.concat([salt, iv, tag, ciphertext]).toString("base64");

fs.writeFileSync(OUT, payload, "utf8");

const kb = (n) => (n / 1024).toFixed(1) + "KB";
console.log("\n  Encrypted content.js -> content.enc");
console.log("  passcode : " + passcode.replace(/./g, "*") + "  (" + passcode.length + " chars)");
console.log("  size     : " + kb(source.length) + " -> " + kb(payload.length));
console.log("\n  Commit content.enc. Do NOT commit content.js.\n");
