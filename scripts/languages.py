import json
import sys
import os

out_path = os.path.join(os.path.dirname(__file__), f"out_{os.path.basename(__file__)[:-3]}.tex")
sys.stdout = open(out_path, 'w', encoding='utf-8')

# Language: default ES, override with first CLI argument (e.g. python3 languages.py EN)
lang = sys.argv[1] if len(sys.argv) > 1 else "ES"

json_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'languages.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data.get(lang, data["ES"])

section_title = "Idiomas" if lang == "ES" else "Languages"
print(rf"\section{{{section_title}}}")

print(r"\resumeSubHeadingListStart")

for entry in entries:
    language = entry["language"]
    level = entry["level"]
    year = entry["year"]
    
    print(r"    \resumeProjectHeading")
    print(rf"        {{\textbf{{{language}}} $|$ \emph{{{level}}}}}{{{year}}}")

print(r"  \resumeSubHeadingListEnd")
