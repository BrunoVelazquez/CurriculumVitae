"""
scripts/experience.py - Generador del fragmento LaTeX para la sección de Experiencia Laboral.

Funcionalidad:
    Carga la experiencia laboral desde `json/experience.json` según el idioma seleccionado.
    Filtra los puestos de trabajo según los índices especificados en `.build_choices.json`
    (si existe). Genera el bloque de LaTeX usando los comandos de formato `\resumeSubheading`
    y viñetas de tareas/logros `\resumeItem`.

Inputs:
    - Argumentos CLI: `sys.argv[1]` opcional indicando el idioma ("ES" por defecto o "EN").
    - Archivo de datos: `../json/experience.json`.
    - Archivo de opciones: `../.build_choices.json` (clave 'experience' con lista de índices).

Outputs:
    - Archivo LaTeX generado: `scripts/out_experience.tex` (redirigiendo `sys.stdout`).
"""

import json
import sys
import os

out_path = os.path.join(os.path.dirname(__file__), f"out_{os.path.basename(__file__)[:-3]}.tex")
sys.stdout = open(out_path, 'w', encoding='utf-8')

# Language: default ES, override with first CLI argument (e.g. python3 experience.py EN)
lang = sys.argv[1] if len(sys.argv) > 1 else "ES"

json_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'experience.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data.get(lang, data["ES"])

choices_path = os.path.join(os.path.dirname(__file__), '..', '.build_choices.json')
if os.path.exists(choices_path):
    with open(choices_path, 'r', encoding='utf-8') as cf:
        choices = json.load(cf)
    if 'experience' in choices:
        entries = [entries[i] for i in choices['experience'] if i < len(entries)]

section_title = "Experiencia" if lang == "ES" else "Experience"
print(rf"\section{{{section_title}}}")

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
