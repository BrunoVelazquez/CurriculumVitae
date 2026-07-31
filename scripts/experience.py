import json
import sys
import os

# Language: default ES, override with first CLI argument (e.g. python3 experience.py EN)
lang = sys.argv[1] if len(sys.argv) > 1 else "ES"

json_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'experience.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data.get(lang, data["ES"])

print(r"\resumeSubHeadingListStart")

for entry in entries:
    role    = entry["role"]
    start   = entry["start"]
    finish  = entry.get("finish", "")
    company = entry["company"]
    place   = entry["place"]
    tasks   = entry.get("tasks", [])

    date_range = f"{start} -- {finish}" if finish else start

    print(rf"  \resumeSubheading")
    print(rf"    {{{role}}}{{{date_range}}}")
    print(rf"    {{{company}}}")
    print(rf"    {{{place}}}")

    if tasks:
        print(r"    \resumeItemListStart")
        for task in tasks:
            print(rf"      \resumeItem{{{task}}}")
        print(r"    \resumeItemListEnd")
    print()

print(r"\resumeSubHeadingListEnd")
