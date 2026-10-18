"""
scripts/projects.py - Generador del fragmento LaTeX para la sección de Proyectos.

Funcionalidad:
    Carga los proyectos desde `json/projects.json` según el idioma configurado.
    Filtra los proyectos seleccionados en `.build_choices.json` (si existe).
    Genera el formato en LaTeX mediante `\resumeProjectHeading` especificando
    nombre del proyecto, stack tecnológico, año y lista de características/tareas (`\resumeItem`).

Inputs:
    - Argumentos CLI: `sys.argv[1]` opcional indicando el idioma ("ES" por defecto o "EN").
    - Archivo de datos: `../json/projects.json`.
    - Archivo de opciones: `../.build_choices.json` (clave 'projects' con lista de índices).

Outputs:
    - Archivo LaTeX generado: `scripts/out_projects.tex` (redirigiendo `sys.stdout`).
"""

import json
import sys
import os

out_path = os.path.join(os.path.dirname(__file__), f"out_{os.path.basename(__file__)[:-3]}.tex")
sys.stdout = open(out_path, 'w', encoding='utf-8')

# Language: default ES, override with first CLI argument (e.g. python3 projects.py EN)
lang = sys.argv[1] if len(sys.argv) > 1 else "ES"

json_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'projects.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data.get(lang, data["ES"])

choices_path = os.path.join(os.path.dirname(__file__), '..', '.build_choices.json')
if os.path.exists(choices_path):
    with open(choices_path, 'r', encoding='utf-8') as cf:
        choices = json.load(cf)
    if 'projects' in choices:
        entries = [entries[i] for i in choices['projects'] if i < len(entries)]

section_title = "Proyectos" if lang == "ES" else "Projects"
print(rf"\section{{{section_title}}}")

print(r"\resumeSubHeadingListStart")

for entry in entries:
    title = entry["title"]
    tech = entry["tech"]
    year = entry["year"]
    tasks = entry.get("tasks", [])

    print(r"  \resumeProjectHeading")
    print(rf"      {{\textbf{{{title}}} $|$ \emph{{{tech}}}}}{{{year}}}")

    if tasks:
        print(r"      \resumeItemListStart")
        for task in tasks:
            print(rf"        \resumeItem{{{task}}}")
        print(r"      \resumeItemListEnd")

print(r"\resumeSubHeadingListEnd")
