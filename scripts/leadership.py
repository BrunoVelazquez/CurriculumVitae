import json
import sys
import os

out_path = os.path.join(os.path.dirname(__file__), f"out_{os.path.basename(__file__)[:-3]}.tex")
sys.stdout = open(out_path, 'w', encoding='utf-8')

# Language: default ES, override with first CLI argument (e.g. python3 leadership.py EN)
lang = sys.argv[1] if len(sys.argv) > 1 else "ES"

json_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'leadership.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data.get(lang, data["ES"])

section_title = "Liderazgo y Actividades" if lang == "ES" else "Leadership and Activities"
print(rf"\section{{{section_title}}}")

print(r"\resumeSubHeadingListStart")

for entry in entries:
    role = entry["role"]
    period = entry["period"]
    organization = entry["organization"]
    location = entry["location"]
    tasks = entry.get("tasks", [])

    print(rf"    \resumeSubheading")
    print(rf"      {{{role}}}")
    print(rf"      {{{period}}}")
    print(rf"      {{{organization}}}")
    print(rf"      {{{location}}}")

    if tasks:
        print(r"      \resumeItemListStart")
        for task in tasks:
            print(rf"        \resumeItem{{{task}}}")
        print(r"      \resumeItemListEnd")

print(r"  \resumeSubHeadingListEnd")
