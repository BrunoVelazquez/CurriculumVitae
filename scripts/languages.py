"""
scripts/languages.py - Generador del fragmento LaTeX para la sección de Idiomas.

Funcionalidad:
    Carga los idiomas y niveles de dominio desde `json/languages.json` según el idioma configurado.
    Filtra los idiomas marcados en `.build_choices.json` (si existe).
    Genera el formato en LaTeX usando `\resumeProjectHeading` indicando idioma, nivel y año/detalle.

Inputs:
    - Argumentos CLI: `sys.argv[1]` opcional indicando el idioma ("ES" por defecto o "EN").
    - Archivo de datos: `../json/languages.json`.
    - Archivo de opciones: `../.build_choices.json` (clave 'languages' con lista de índices).

Outputs:
    - Archivo LaTeX generado: `scripts/out_languages.tex` (redirigiendo `sys.stdout`).
"""

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

choices_path = os.path.join(os.path.dirname(__file__), '..', '.build_choices.json')
if os.path.exists(choices_path):
    with open(choices_path, 'r', encoding='utf-8') as cf:
        choices = json.load(cf)
    if 'languages' in choices:
        entries = [entries[i] for i in choices['languages'] if i < len(entries)]

if not entries:
    sys.exit(0)

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
