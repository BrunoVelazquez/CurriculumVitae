import json
import sys
import os

out_path = os.path.join(os.path.dirname(__file__), f"out_{os.path.basename(__file__)[:-3]}.tex")
sys.stdout = open(out_path, 'w', encoding='utf-8')

# Language: default ES, override with first CLI argument (e.g. python3 skills.py EN)
lang = sys.argv[1] if len(sys.argv) > 1 else "ES"

json_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'skills.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data.get(lang, data["ES"])

choices_path = os.path.join(os.path.dirname(__file__), '..', '.build_choices.json')
if os.path.exists(choices_path):
    with open(choices_path, 'r', encoding='utf-8') as cf:
        choices = json.load(cf)
    if 'skills' in choices:
        entries = [entries[i] for i in choices['skills'] if i < len(entries)]

section_title = "Habilidades técnicas" if lang == "ES" else "Technical Skills"
print(rf"\section{{{section_title}}}")

print(r" \begin{itemize}[leftmargin=0.15in, label={}]")
print(r"    \small{\item{")

for entry in entries:
    category = entry["category"]
    skills = entry["skills"]
    print(rf"        \textbf{{{category}}}{{: {skills}}} \\")

print(r"    }}")
print(r" \end{itemize}")
print(r" \vspace{-16pt}")
