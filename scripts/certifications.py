import json
import sys
import os

out_path = os.path.join(os.path.dirname(__file__), f"out_{os.path.basename(__file__)[:-3]}.tex")
sys.stdout = open(out_path, 'w', encoding='utf-8')

# Language: default ES, override with first CLI argument (e.g. python3 certifications.py EN)
lang = sys.argv[1] if len(sys.argv) > 1 else "ES"

json_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'certifications.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data.get(lang, data["ES"])

choices_path = os.path.join(os.path.dirname(__file__), '..', '.build_choices.json')
if os.path.exists(choices_path):
    with open(choices_path, 'r', encoding='utf-8') as cf:
        choices = json.load(cf)
    if 'certifications' in choices:
        entries = [entries[i] for i in choices['certifications'] if i < len(entries)]

section_title = "Certificaciones" if lang == "ES" else "Certifications"
print(rf"\section{{{section_title}}}")

print(r"\resumeSubHeadingListStart")

for entry in entries:
    name = entry["name"]
    date = entry["date"]
    issuer = entry["issuer"]
    location = entry["location"]

    print(rf"        \resumeSubheading")
    print(rf"        {{{name}}}")
    print(rf"        {{{date}}}")
    print(rf"        {{{issuer}}}")
    print(rf"        {{{location}}}")

print(r"  \resumeSubHeadingListEnd")
