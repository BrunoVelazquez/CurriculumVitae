"""
scripts/profile.py - Generador del fragmento LaTeX para la sección de Perfil Profesional.

Funcionalidad:
    Lee la información de perfiles desde `json/profile.json`. Si existe el archivo
    de configuración `.build_choices.json` con un rol seleccionado ('profile'), utiliza
    dicho perfil; en caso contrario, ofrece retrocompatibilidad o toma el primer rol
    disponible. Genera el código LaTeX correspondiente con el título de sección
    traducido y el texto del perfil.

Inputs:
    - Argumentos CLI: `sys.argv[1]` opcional indicando el idioma ("ES" por defecto o "EN").
    - Archivo de datos: `../json/profile.json`.
    - Archivo de opciones: `../.build_choices.json` (clave 'profile' indicando el rol elegido).

Outputs:
    - Archivo LaTeX generado: `scripts/out_profile.tex` (redirigiendo `sys.stdout`).
"""

import json
import sys
import os

out_path = os.path.join(os.path.dirname(__file__), f"out_{os.path.basename(__file__)[:-3]}.tex")
sys.stdout = open(out_path, 'w', encoding='utf-8')

# Language: default ES, override with first CLI argument (e.g. python3 profile.py EN)
lang = sys.argv[1] if len(sys.argv) > 1 else "ES"

json_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'profile.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

choices_path = os.path.join(os.path.dirname(__file__), '..', '.build_choices.json')
selected_role = None
if os.path.exists(choices_path):
    with open(choices_path, 'r', encoding='utf-8') as cf:
        choices = json.load(cf)
    selected_role = choices.get('profile')

# Si los datos están organizados por rol
if selected_role and selected_role in data:
    role_data = data[selected_role]
    profile_text = role_data.get(lang, role_data.get("ES", ""))
elif "ES" in data or "EN" in data:
    # Retrocompatibilidad: si no está anidado por roles
    profile_text = data.get(lang, data.get("ES", ""))
else:
    # Tomar el primer rol disponible como fallback
    first_role = next(iter(data.values()), {})
    profile_text = first_role.get(lang, first_role.get("ES", ""))

section_title = "Perfil Profesional" if lang == "ES" else "Professional Profile"
print(rf"\section{{{section_title}}}")

print(r"\begin{itemize}[leftmargin=0.15in, label={}]")
print(r"    \small{\item{")
print(rf"        {profile_text}")
print(r"    }}")
print(r"\end{itemize}")
print(r"\vspace{-16pt}")
