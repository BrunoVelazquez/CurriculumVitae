"""
scripts/skills.py - Generador del fragmento LaTeX para la sección de Habilidades Técnicas.

Funcionalidad:
    Carga las categorías y tecnologías desde `json/skills.json` según el idioma.
    Aplica el filtro de categorías seleccionadas en `.build_choices.json` (si existe).
    Formatea las habilidades agrupándolas en una tabla de dos columnas (`tabular*`)
    para optimizar el espacio vertical del CV.

Inputs:
    - Argumentos CLI: `sys.argv[1]` opcional indicando el idioma ("ES" por defecto o "EN").
    - Archivo de datos: `../json/skills.json`.
    - Archivo de opciones: `../.build_choices.json` (clave 'skills' con lista de índices).

Outputs:
    - Archivo LaTeX generado: `scripts/out_skills.tex` (redirigiendo `sys.stdout`).
"""

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

print(r"\begin{tabular*}{\textwidth}{@{}>{\raggedright\arraybackslash}p{0.46\textwidth}@{\hspace{0.08\textwidth}}>{\raggedright\arraybackslash}p{0.46\textwidth}@{}}")
print(r"  \small")

# Pair entries two per row
for i in range(0, len(entries), 2):
    left = entries[i]
    left_cell = rf"\textbf{{{left['category']}}}: {left['skills']}"
    if i + 1 < len(entries):
        right = entries[i + 1]
        right_cell = rf"\textbf{{{right['category']}}}: {right['skills']}"
    else:
        right_cell = ""
    print(rf"  {left_cell} & {right_cell} \\[2pt]")

print(r"\end{tabular*}")
print(r"\vspace{-10pt}")

