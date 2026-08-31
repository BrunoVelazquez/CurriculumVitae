import json
import sys
import os

out_path = os.path.join(os.path.dirname(__file__), f"out_{os.path.basename(__file__)[:-3]}.tex")
sys.stdout = open(out_path, 'w', encoding='utf-8')

# Language: default ES, override with first CLI argument (e.g. python3 education.py EN)
lang = sys.argv[1] if len(sys.argv) > 1 else "ES"

json_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'education.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data.get(lang, data["ES"])

section_title = "Educación" if lang == "ES" else "Education"
print(rf"\section{{{section_title}}}")

print(r"\resumeSubHeadingListStart")

for entry in entries:
    name   = entry["name"]
    start  = entry["start"]
    finish = entry["finish"]
    info   = entry.get("info", "")
    place  = entry["place"]

    date_range = f"{start} -- {finish}" if finish else start

    print(rf"  \resumeSubheading")
    print(rf"    {{{name}}}")
    print(rf"    {{{date_range}}}")
    print(rf"    {{{info}}}")
    print(rf"    {{{place}}}")

print(r"\resumeSubHeadingListEnd")