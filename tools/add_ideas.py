#!/usr/bin/env python3
"""Add new idea cards (with translations) to Qshelf.

Usage:
  python3 tools/add_ideas.py new.json            # add cards, update translations, bump caches
  python3 tools/add_ideas.py --books             # list books already on the shelf
  python3 tools/add_ideas.py --check new.json    # validate only, change nothing

new.json is a list of cards:
  {
    "book": "Deep Work", "author": "Cal Newport", "year": 2016,   # negative year = BC
    "theme": "work",            # habits mind money work people meaning strategy health
    "lang": "en",               # en hi bn mr : the language the card is written in
    "idea": "...", "body": "...", "try": "...",
    "tr": {"hi": ["idea", "body", "try"], "bn": [...], "mr": [...]}   # every language except "lang"
  }
"""
import json, re, sys, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
THEMES = {"habits", "mind", "money", "work", "people", "meaning", "strategy", "health"}
LANGS = ["en", "hi", "bn", "mr"]
SCRIPT = {"hi": r"[ऀ-ॿ]", "mr": r"[ऀ-ॿ]", "bn": r"[ঀ-৿]"}

def load_ideas(html):
    a = html.index("const IDEAS=[")
    b = html.index("\n];", a) + 3
    rows = json.loads(html[a + len("const IDEAS="):b - 1])
    return a, b, rows

key = lambda book, idea: f"{book}|{idea}"
lang_of = lambda r: r[7] if len(r) > 7 else "en"

def validate(cards, rows):
    have = {key(r[0], r[4]) for r in rows}
    errs = []
    for n, c in enumerate(cards, 1):
        tag = f"card {n} ({c.get('book')} / {c.get('idea')})"
        for f in ["book", "author", "year", "theme", "lang", "idea", "body", "try", "tr"]:
            if f not in c: errs.append(f"{tag}: missing {f}")
        if errs and errs[-1].startswith(tag): continue
        if c["theme"] not in THEMES: errs.append(f"{tag}: unknown theme {c['theme']}")
        if c["lang"] not in LANGS: errs.append(f"{tag}: unknown lang {c['lang']}")
        if not isinstance(c["year"], int): errs.append(f"{tag}: year must be a whole number")
        if key(c["book"], c["idea"]) in have: errs.append(f"{tag}: already on the shelf")
        have.add(key(c["book"], c["idea"]))
        for s in [c["book"], c["author"], c["idea"], c["body"], c["try"]]:
            if '"' in s: errs.append(f"{tag}: remove double quotes from text")
        if c["lang"] != "en" and not re.search(SCRIPT[c["lang"]], c["idea"] + c["body"]):
            errs.append(f"{tag}: text is not in {c['lang']} script")
        for l in LANGS:
            if l == c["lang"]: continue
            t = c["tr"].get(l)
            if not (isinstance(t, list) and len(t) == 3 and all(isinstance(x, str) and x.strip() for x in t)):
                errs.append(f"{tag}: translation '{l}' must be [idea, body, try]"); continue
            if l != "en" and not re.search(SCRIPT[l], "".join(t)):
                errs.append(f"{tag}: translation '{l}' is not in {l} script")
            if l == "en" and re.search(r"[ऀ-৿]", "".join(t)):
                errs.append(f"{tag}: English translation contains Indian script")
    return errs

def main():
    html_p = ROOT / "index.html"; html = html_p.read_text()
    a, b, rows = load_ideas(html)
    if sys.argv[1:] == ["--books"]:
        seen = {}
        for r in rows: seen.setdefault(r[0], [r[1], lang_of(r), 0])[2] += 1
        for k, (au, l, n) in sorted(seen.items()): print(f"{l}\t{n}\t{k} — {au}")
        print(f"\n{len(seen)} books, {len(rows)} ideas"); return
    check = sys.argv[1] == "--check"
    cards = json.loads(pathlib.Path(sys.argv[-1]).read_text())
    errs = validate(cards, rows)
    if errs:
        print("Not added. Fix these:"); [print(" -", e) for e in errs]; sys.exit(1)
    if check: print(f"OK: {len(cards)} cards are valid."); return
    # 1. ideas array
    for c in cards:
        r = [c["book"], c["author"], c["year"], c["theme"], c["idea"], c["body"], c["try"]]
        if c["lang"] != "en": r.append(c["lang"])
        rows.append(r)
    body = "const IDEAS=[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n];"
    html = html[:a] + body + html[b:]
    # 2. bump translation cache version
    html = re.sub(r'const TR_VER="(\d+)"', lambda m: f'const TR_VER="{int(m.group(1)) + 1}"', html, count=1)
    html_p.write_text(html)
    # 3. translations
    for l in LANGS:
        p = ROOT / "tr" / f"{l}.json"; d = json.loads(p.read_text())
        for c in cards:
            if l != c["lang"]: d[key(c["book"], c["idea"])] = c["tr"][l]
        p.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
    # 4. offline cache version
    sw = ROOT / "sw.js"; s = sw.read_text()
    sw.write_text(re.sub(r"qshelf-v(\d+)", lambda m: f"qshelf-v{int(m.group(1)) + 1}", s, count=1))
    # 5. README counts
    langs = {l: sum(1 for r in rows if lang_of(r) == l) for l in LANGS}
    books = len({r[0] for r in rows})
    rd = ROOT / "README.md"; t = rd.read_text()
    t = re.sub(r"- \*\*\d+ ideas from \d+ books\*\*: \d+ in English, \d+ in Hindi, \d+ in Bangla and \d+ in Marathi",
               f"- **{len(rows)} ideas from {books} books**: {langs['en']} in English, {langs['hi']} in Hindi, {langs['bn']} in Bangla and {langs['mr']} in Marathi", t)
    rd.write_text(t)
    # 6. script still parses
    js = html.split("<script>")[-1].split("</script>")[0]
    try:
        subprocess.run(["node", "-e", "new Function(require('fs').readFileSync(0,'utf8'))"], input=js, text=True, check=True)
    except FileNotFoundError:
        print("note: node not found, skipped script check")
    print(f"Added {len(cards)} cards. Shelf now has {len(rows)} ideas from {books} books "
          f"({langs['en']} en, {langs['hi']} hi, {langs['bn']} bn, {langs['mr']} mr).")

if __name__ == "__main__":
    main()
