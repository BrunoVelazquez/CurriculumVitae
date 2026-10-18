"""
scripts/education.py - Generador del fragmento LaTeX para la sección de Educación.

Funcionalidad:
    Carga el historial educativo desde `json/education.json` según el idioma configurado.
    Filtra los títulos e instituciones académicas según los índices guardados en
    `.build_choices.json` (si existe). Genera el bloque de LaTeX usando las macros
    `\resumeSubHeadingListStart` y `\resumeSubheading`.

Inputs:
    - Argumentos CLI: `sys.argv[1]` opcional indicando el idioma ("ES" por defecto o "EN").
    - Archivo de datos: `../json/education.json`.
    - Archivo de opciones: `../.build_choices.json` (clave 'education' con lista de índices).

Outputs:
    - Archivo LaTeX generado: `scripts/out_education.tex` (redirigiendo `sys.stdout`).
"""

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

choices_path = os.path.join(os.path.dirname(__file__), '..', '.build_choices.json')
if os.path.exists(choices_path):
    with open(choices_path, 'r', encoding='utf-8') as cf:
        choices = json.load(cf)
    if 'education' in choices:
        entries = [entries[i] for i in choices['education'] if i < len(entries)]

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