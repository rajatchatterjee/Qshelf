# Adding books to Qshelf each week

Qshelf (https://rajatchatterjee.github.io/Qshelf/) is Rajat Chatterjee's app of five-minute ideas from great books. Every card is one idea from one book. This guide is for the weekly run that adds new books.

## The job

Add **10 new books** that are not on the shelf yet, with **2 or 3 cards each** (about 25 cards), then publish.

1. See what is already there: `python3 tools/add_ideas.py --books`
2. Choose 10 books that are not listed. Mix the languages each week:
   - about 6 English books (well-known non-fiction, classics, Indian authors writing in English)
   - about 4 from Hindi, Bangla and Marathi literature, at least one of each over a two-week span, written in that language
   - spread them across the themes, and favour themes with fewer cards
   - only real, well-known books, with the correct author and first-publication year. If unsure of a fact, pick a different book.
3. Write the cards into `new.json` (format below), including translations into every other language.
4. Validate: `python3 tools/add_ideas.py --check new.json`. Fix anything it reports.
5. Add: `python3 tools/add_ideas.py new.json`
6. Commit only the changed app files (`index.html`, `tr/*.json`, `sw.js`, `README.md`), not `new.json`, with a message like `Add 10 books: Title, Title, …`, then push to `main`.
7. Confirm the GitHub Pages deploy finished successfully.
8. Tell Rajat which books were added, with one line each.

## How a card reads

Each card has three parts:

- **idea**: the title. 3 to 7 words, a plain statement of the idea, no colon or question.
- **body**: 2 or 3 short sentences, about 30 to 45 words. Say what the idea is and why it matters, in everyday words.
- **try**: one concrete action the reader can do today or this week, one sentence, starting with a verb.

Rules:

- **Paraphrase everything.** Never copy sentences from the book. No quotation marks at all, single or double. For poems, songs and verses, describe the meaning in your own words.
- Write plainly, the way a knowledgeable friend would talk. No hype, no emoji, no exclamation marks.
- The book's own language decides the card's language: a Bangla novel gets a card written in Bangla.
- Translations should read naturally in each language, not word for word. Use the same script and style as existing cards (look at `tr/hi.json` for tone).
- No medical dosing, financial product picks, or anything that reads as professional advice.

Themes: `habits`, `mind` (Thinking), `money`, `work`, `people`, `meaning`, `strategy`, `health`.
Languages: `en`, `hi`, `bn`, `mr`.

## new.json format

```json
[
  {
    "book": "Deep Work", "author": "Cal Newport", "year": 2016,
    "theme": "work", "lang": "en",
    "idea": "Focus is a rare and valuable skill",
    "body": "Hard, uninterrupted concentration produces work others can't easily copy. ...",
    "try": "Block 90 minutes on tomorrow's calendar with notifications off.",
    "tr": {
      "hi": ["...", "...", "..."],
      "bn": ["...", "...", "..."],
      "mr": ["...", "...", "..."]
    }
  }
]
```

`tr` needs every language except the card's own `lang`. Years before the common era are negative (`-300`).

## If something goes wrong

- If the script reports errors, fix the cards and run it again. Do not edit `index.html` by hand.
- If pushing or deploying fails, leave the work committed locally, and tell Rajat what failed and what he can do.
