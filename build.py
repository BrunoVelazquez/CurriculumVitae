"""
build.py - Orquestador y constructor interactivo de Curriculum Vitae en LaTeX.

Funcionalidad:
    Permite configurar y compilar de manera interactiva el CV en formato PDF.
    Ofrece selección de idioma (ES/EN), selección del perfil/rol profesional deseado,
    y selección múltiple de los ítems a incluir para cada sección (educación, experiencia,
    habilidades, etc.). Invoca los scripts generadores de cada sección en `scripts/`
    y finalmente compila el documento principal LaTeX (`main.tex`) usando `pdflatex`.

Inputs:
    - Interacción por consola / teclado: Selección de idioma, selección de rol y marcado
      de ítems mediante menús interactivos por terminal.
    - Archivos JSON de datos: `json/*.json` (profile.json, education.json, experience.json, etc.).
    - Archivo de configuración previa (opcional): `last_choices.json`.

Outputs:
    - Archivo temporal `.build_choices.json` (eliminado al finalizar la compilación).
    - Archivo `last_choices.json`: Guarda la última configuración seleccionada para reutilizarla.
    - Archivos TeX generados por los scripts auxiliares: `scripts/out_*.tex`.
    - Documento final compilado: `CV_BrunoVelazquez_<Rol>_<Idioma>.pdf`.
"""

import json
import os
import sys
import subprocess

def get_key():
    """
    Captura una única pulsación de tecla de forma síncrona y multiplataforma (Windows y Unix/Linux).

    Funcionalidad:
        Lee la entrada estándar en modo crudo (raw) para capturar teclas especiales como
        flechas de navegación (ARRIBA, ABAJO), ENTER, ESPACIO y ESC sin requerir presionar ENTER.

    Inputs:
        Ninguno (lee desde `sys.stdin` / `msvcrt`).

    Outputs:
        str | None: Identificador de la tecla ('UP', 'DOWN', 'ENTER', 'SPACE', 'ESC') o el carácter leído.
    """
    if os.name == 'nt':
        import msvcrt
        key = msvcrt.getch()
        if key in (b'\xe0', b'\x00'):
            key = msvcrt.getch()
            if key == b'H': return 'UP'
            if key == b'P': return 'DOWN'
            return None
        elif key in (b'\r', b'\n'): return 'ENTER'
        elif key == b' ': return 'SPACE'
        elif key == b'\x1b': return 'ESC'
        return key.decode('utf-8', 'ignore')
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            # Leer directamente del OS para evitar que Python fragmente las secuencias de escape
            b = os.read(fd, 3)
            if b == b'\x1b[A': return 'UP'
            elif b == b'\x1b[B': return 'DOWN'
            elif b == b'\x1b': return 'ESC'
            elif b in (b'\r', b'\n'): return 'ENTER'
            elif b == b' ': return 'SPACE'
            elif b == b'\x03': return 'ESC' # Ctrl+C
            return b.decode('utf-8', 'ignore')
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def single_select_menu(title, items, default_idx=0):
    """
    Despliega un menú interactivo en consola para seleccionar una única opción (radio button).

    Funcionalidad:
        Muestra la lista de opciones navegable con flechas arriba/abajo y confirma con ENTER.
        Permite cancelar con la tecla ESC.

    Inputs:
        title (str): Título o nombre de la sección a mostrar en el encabezado.
        items (list[str]): Opciones disponibles para seleccionar.
        default_idx (int): Índice inicialmente enfocado y seleccionado.

    Outputs:
        str | None: El elemento seleccionado o None si la lista está vacía.
    """
    if not items:
        return None
    
    current_idx = default_idx if 0 <= default_idx < len(items) else 0
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"--- Selección: {title.upper()} ---")
        print("Usa FLECHA ARRIBA/ABAJO para mover, ENTER para confirmar.\n")
        
        for i, item in enumerate(items):
            pointer = ">" if i == current_idx else " "
            check = "(*)" if i == current_idx else "( )"
            print(f" {pointer} {check} {item}")
            
        key = get_key()
        
        if key == 'UP':
            current_idx = (current_idx - 1) % len(items)
        elif key == 'DOWN':
            current_idx = (current_idx + 1) % len(items)
        elif key == 'ENTER':
            break
        elif key == 'ESC':
            print('\nOperación cancelada.')
            sys.exit(0)
            
    return items[current_idx]

def interactive_menu(title, items):
    """
    Despliega un menú interactivo en consola para selección múltiple con casillas (checkboxes).

    Funcionalidad:
        Permite navegar con las flechas, marcar/desmarcar elementos individuales con la barra ESPACIO,
        y confirmar la selección total presionando ENTER.

    Inputs:
        title (str): Nombre de la sección a mostrar en pantalla.
        items (list[str]): Lista descriptiva de los elementos disponibles.

    Outputs:
        list[int]: Lista ordenada de índices de los ítems seleccionados.
    """
    if not items:
        return []
    
    selected = set(range(len(items))) # Por defecto todos seleccionados
    current_idx = 0
    
    while True:
        # Limpiar consola (funciona en cmd y PowerShell y terminales unix)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"--- Sección: {title.upper()} ---")
        print("Usa FLECHA ARRIBA/ABAJO para mover, ESPACIO para marcar/desmarcar, ENTER para confirmar.\n")
        
        for i, item in enumerate(items):
            pointer = ">" if i == current_idx else " "
            check = "(*)" if i in selected else "( )"
            print(f" {pointer} {check} {item}")
            
        key = get_key()
        
        if key == 'UP':
            current_idx = (current_idx - 1) % len(items)
        elif key == 'DOWN':
            current_idx = (current_idx + 1) % len(items)
        elif key == 'SPACE':
            if current_idx in selected:
                selected.remove(current_idx)
            else:
                selected.add(current_idx)
        elif key == 'ENTER':
            break
        elif key == 'ESC':
            print('\nOperación cancelada.')
            sys.exit(0)
            
    return sorted(list(selected))

def main():
    """
    Punto de entrada principal del orquestador de construcción.

    Funcionalidad:
        1. Solicita idioma al usuario (ES/EN).
        2. Permite reanudar la selección previa guardada en `last_choices.json` o realizar una nueva.
        3. Permite elegir el perfil profesional objetivo según `json/profile.json`.
        4. Itera sobre cada sección del CV ejecutando el menú de selección múltiple.
        5. Guarda las elecciones en `.build_choices.json` y `last_choices.json`.
        6. Ejecuta secuencialmente los scripts de `scripts/*.py` pasando el idioma como argumento.
        7. Invoca `pdflatex` para compilar `main.tex` generando el PDF final.
        8. Limpia los archivos temporales de compilación generados por LaTeX.

    Inputs:
        - Respuestas interactivas del usuario por consola (idioma, confirmaciones, selecciones de menú).
        - Archivos de datos `json/*.json`.
        - Archivo `last_choices.json` si existe.

    Outputs:
        - Archivos intermedios `scripts/out_*.tex`.
        - Archivo de configuración persistente `last_choices.json`.
        - Archivo PDF resultante `CV_BrunoVelazquez_<Rol>_<Idioma>.pdf`.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Generador interactivo de CV ===\n")
    
    lang_input = input("¿En qué idioma quieres generar el CV? (ES/EN) [por defecto: ES]: ").strip().upper()
    if lang_input not in ["ES", "EN"]:
        lang = "ES"
    else:
        lang = lang_input
        
    sections = [
        ("education", "name"),
        ("experience", lambda item: f"{item['role']} en {item['company']}"),
        ("projects", "title"),
        ("certifications", "name"),
        ("leadership", lambda item: f"{item['role']} en {item['organization']}"),
        ("skills", "category"),
        ("languages", "language")
    ]
    
    choices = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_dir = os.path.join(base_dir, 'json')
    last_choices_path = os.path.join(base_dir, 'last_choices.json')
    
    use_last = False
    if os.path.exists(last_choices_path):
        resp = input("¿Quieres usar la última configuración guardada? (S/N) [por defecto: N]: ").strip().upper()
        if resp == 'S':
            use_last = True
            with open(last_choices_path, 'r', encoding='utf-8') as f:
                choices = json.load(f)
                
    if not use_last:
        # Selección de perfil profesional por rol
        profile_json_path = os.path.join(json_dir, "profile.json")
        if os.path.exists(profile_json_path):
            with open(profile_json_path, 'r', encoding='utf-8') as pf:
                profile_data = json.load(pf)
            # Solo si contiene roles (es decir, las claves no son directamente 'ES'/'EN')
            if "ES" not in profile_data and "EN" not in profile_data:
                roles = list(profile_data.keys())
                if roles:
                    default_role_idx = 0
                    if "profile" in choices and choices["profile"] in roles:
                        default_role_idx = roles.index(choices["profile"])
                    selected_role = single_select_menu("Perfil Profesional", roles, default_role_idx)
                    choices["profile"] = selected_role

        for sec_name, display_key in sections:
            json_path = os.path.join(json_dir, f"{sec_name}.json")
            if not os.path.exists(json_path):
                continue
                
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            entries = data.get(lang, [])
            if not entries:
                continue
                
            display_items = []
            for i, item in enumerate(entries):
                if callable(display_key):
                    display_items.append(display_key(item))
                else:
                    display_items.append(item.get(display_key, f"Item {i+1}"))
                    
            selected_indices = interactive_menu(sec_name, display_items)
            choices[sec_name] = selected_indices
            
        # Guardar la nueva configuración
        with open(last_choices_path, 'w', encoding='utf-8') as f:
            json.dump(choices, f)
        
    # Guardar opciones temporalmente
    choices_path = os.path.join(base_dir, '.build_choices.json')
    with open(choices_path, 'w', encoding='utf-8') as f:
        json.dump(choices, f)
        
    # Compilar
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Generando secciones en {lang}...")
    
    # Generar perfil profesional (no es una lista, así que va fuera del menú interactivo)
    profile_script = os.path.join(base_dir, 'scripts', 'profile.py')
    if os.path.exists(profile_script):
        subprocess.run([sys.executable, profile_script, lang], check=True)
        
    for sec_name, _ in sections:
        script_path = os.path.join(base_dir, 'scripts', f"{sec_name}.py")
        if os.path.exists(script_path):
            subprocess.run([sys.executable, script_path, lang], check=True)
            
    # Determinar el nombre del rol para el archivo
    selected_role = choices.get("profile")
    if not selected_role:
        # Fallback si no está en choices
        profile_json_path = os.path.join(json_dir, "profile.json")
        if os.path.exists(profile_json_path):
            with open(profile_json_path, 'r', encoding='utf-8') as pf:
                pdata = json.load(pf)
            selected_role = next(iter(pdata.keys()), "General")
        else:
            selected_role = "General"

    role_clean = "".join(selected_role.split())
    job_name = f"CV_BrunoVelazquez_{role_clean}_{lang}"

    print(f"Compilando documento ({job_name}.pdf) con tu selección...")
    cmd = rf'pdflatex -shell-escape -jobname="{job_name}" "\def\cvlang{{{lang}}}\input{{main.tex}}"'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"\n¡CV compilado exitosamente! Revisa el archivo {job_name}.pdf")
    except subprocess.CalledProcessError:
        print("\nHubo un error al compilar el PDF. Revisa los logs.")
    finally:
        if os.path.exists(choices_path):
            os.remove(choices_path)

        # Limpiar archivos temporales de compilación de LaTeX
        temp_extensions = ['.aux', '.log', '.out', '.fls', '.fdb_latexmk', '.synctex.gz']
        for ext in temp_extensions:
            temp_file = os.path.join(base_dir, f"{job_name}{ext}")
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except OSError:
                    pass

if __name__ == "__main__":
    main()
