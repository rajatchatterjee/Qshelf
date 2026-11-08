# Qshelf

Five minutes a day of big ideas from great books. Swipe through one idea per card, each paraphrased from a well-known book and ending with a small "try this" action.

- **Today**: twelve ideas a day, each from a different book, reshuffled daily
- **350 ideas from 205 books**: 262 in English, 31 in Hindi, 29 in Bangla and 28 in Marathi, across Habits, Thinking, Money, Work, People, Meaning, Strategy and Health
- **Languages**: choose English, हिन्दी, বাংলা and मराठी in any mix. Hindi, Bangla and Marathi books appear in their own language
- **Choose your books**: tick which books go in your daily deck on the Books shelf
- **Translate on demand**: the ••• menu on a card translates it on the phone where supported, otherwise opens Google Translate
- **Recall quiz**: two quick questions on ideas from earlier days, before today's deck
- **Book deep-dives**: tap a book's name, or open Books, to read all its ideas in order
- **Notes**: write what an idea means for you; find them all under Notes
- **Share as image**: turn any card into a picture for WhatsApp or Instagram
- **Daily reminder**: add a recurring event to Google Calendar or any calendar app
- **5-minute clock** that starts on your first swipe, plus a daily streak
- **Save and copy** any card, or double-tap a card to save it
- **Reading themes**: Sepia (default), Auto, Paper, Night, Midnight, Forest
- **Reader settings**: text size, Serif / Sans / Easy-read typeface, line spacing
- **Focus mode**: tap a card to hide everything but the idea
- **Listen**: read-aloud with a voice picker and speed control, and it can move through the deck on its own
- **Ambience**: generated rain, ocean or hearth sound while you read

## Install

Open https://rajatchatterjee.github.io/Qshelf/ on your phone.

- Android (Chrome): ⋮ menu, then Install app
- iPhone (Safari): Share, then Add to Home Screen

It opens full screen and works offline after the first load.

## Adding ideas

New books are added every Sunday by a scheduled task that follows `tools/WEEKLY.md` and uses `tools/add_ideas.py`. To add cards by hand, write them to a JSON file in the format described there and run `python3 tools/add_ideas.py new.json`.


Ideas live in the `IDEAS` array in `index.html`, one line each: book, author, year (negative for BC), theme, idea, explanation, try-this, and an optional language code (`hi`, `bn`, `mr`; English when left out).

## Usage counts

Anonymous visits and a few events (sessions started and finished, listens, shares, quiz answers, saves) go to the tidycorners GoatCounter dashboard under paths starting with `/qshelf`. Nothing is counted in the Claude preview, and notes and saved ideas stay on the device.

## Credits

Made by Rajat Chatterjee, Pune. Ideas are paraphrased from the books named on each card.
