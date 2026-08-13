/* ============================================================
   ELLEN'S 30TH — CONTENT FILE
   ------------------------------------------------------------
   This is the only file you should need to edit day to day.
   Swap the placeholder text/photo/video for the real thing as
   people send it to you. Leave everything else alone.

   FIELD GUIDE
   - day: 1 to 10, controls unlock order (do not change)
   - name / relation: shown on the pin and inside the letter
   - city / country: label shown on the map
   - lat / lon: map position (decimal degrees). Google
     "[city name] latitude longitude" if you move someone.
   - type: "letter" | "photo" | "video" | "giftlist"
   - content:
       letter  -> a string, use \n\n for paragraph breaks
       photo   -> { src: "path-or-url.jpg", caption: "..." }
       video   -> { embedUrl: "https://www.youtube.com/embed/XXXX"
                    or a Google Drive / other embeddable link,
                    caption: "..." }
       giftlist-> array of { gift: "...", reason: "..." }
   ============================================================ */

const COUNTDOWN = {
  // First pin unlocks this date, last pin (day 10) is her birthday
  startDate: "2026-09-17",
  endDate: "2026-09-26",
  herName: "Ellen",
  passcode: "mina" // not case sensitive, edit anytime
};

const PEOPLE = [
  {
    day: 1,
    name: "Your sister",
    relation: "sister",
    city: "Cairo",
    country: "Egypt",
    lat: 30.0444,
    lon: 31.2357,
    type: "letter",
    content:
      "PLACEHOLDER — replace with her sister's letter.\n\nWrite a little about a memory, and one thing about Ellen you love most. Keep it in her own words, this is just a stand-in so you can see how it will look."
  },
  {
    day: 2,
    name: "Marina Henry",
    relation: "friend",
    city: "Alexandria",
    country: "Egypt",
    lat: 31.2001,
    lon: 29.9187,
    type: "letter",
    content:
      "PLACEHOLDER — replace with Marina Henry's message.\n\nCan be text, or swap type to \"photo\" or \"video\" if she'd rather send one of those instead."
  },
  {
    day: 3,
    name: "Alaa",
    relation: "friend",
    city: "Giza",
    country: "Egypt",
    lat: 30.0131,
    lon: 31.2089,
    type: "letter",
    content: "PLACEHOLDER — replace with Alaa's message."
  },
  {
    day: 4,
    name: "Sico",
    relation: "friend",
    city: "Heliopolis",
    country: "Egypt",
    lat: 30.0808,
    lon: 31.3238,
    type: "letter",
    content: "PLACEHOLDER — replace with Sico's message."
  },
  {
    day: 5,
    name: "Ero",
    relation: "friend",
    city: "Houston, TX", // placeholder — swap for the actual city
    country: "USA",
    lat: 29.7604,
    lon: -95.3698,
    type: "letter",
    content: "PLACEHOLDER — replace with Ero's message."
  },
  {
    day: 6,
    name: "Marina Atef",
    relation: "friend",
    city: "Austin, TX", // placeholder — swap for the actual city
    country: "USA",
    lat: 30.2672,
    lon: -97.7431,
    type: "letter",
    content: "PLACEHOLDER — replace with Marina Atef's message."
  },
  {
    day: 7,
    name: "Your brother",
    relation: "brother",
    city: "Amsterdam",
    country: "Netherlands",
    lat: 52.3676,
    lon: 4.9041,
    type: "letter",
    content: "PLACEHOLDER — replace with her brother's message."
  },
  {
    day: 8,
    name: "Miro",
    relation: "friend",
    city: "Lisbon", // placeholder — confirm Portugal vs Spain, swap city
    country: "Portugal",
    lat: 38.7223,
    lon: -9.1393,
    type: "letter",
    content: "PLACEHOLDER — confirm Miro's country/city, then replace with their message."
  },
  {
    day: 9,
    name: "Paula & his wife",
    relation: "friends",
    city: "Prague",
    country: "Czech Republic",
    lat: 50.0755,
    lon: 14.4378,
    type: "letter",
    content: "PLACEHOLDER — replace with Paula and his wife's message."
  },
  {
    day: 10,
    name: "Mina",
    relation: "your husband",
    city: "Texas", // placeholder — swap for your actual city
    country: "USA",
    lat: 31.9686,
    lon: -99.9018,
    type: "giftlist",
    intro:
      "Happy 30th, habibti. Nine people who love you sent their light across the world this week. Here's mine — ten small things, and what each one means.",
    content: [
      { gift: "A candle", reason: "because you are the warmth in every room you walk into." },
      { gift: "A jar of Nile water", reason: "because home followed you here, it didn't stay behind." },
      { gift: "Your favorite coffee", reason: "because our mornings are my favorite part of every day." },
      { gift: "A plane ticket", reason: "because I will always want to take you back, and bring your world to you." },
      { gift: "A blank notebook", reason: "because you've filled the last thirty years with stories worth keeping." },
      { gift: "A house key", reason: "because wherever we live, you are what makes it home." },
      { gift: "A photo of us", reason: "because I still can't believe I get to do life with you." },
      { gift: "A star map of tonight's sky", reason: "because I'd choose this exact night, with you, every time." },
      { gift: "A love letter", reason: "because some things I can only say in writing, without my voice shaking." },
      { gift: "One more year, and every year after", reason: "because thirty is just the beginning of what I want to give you." }
    ]
  }
];
