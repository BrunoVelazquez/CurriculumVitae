import json
import os
import sys
import subprocess

try:
    import msvcrt
except ImportError:
    print("Este script interactivo requiere Windows (msvcrt).")
    sys.exit(1)

def interactive_menu(title, items):
    if not items:
        return []
    
    selected = set(range(len(items))) # Por defecto todos seleccionados
    current_idx = 0
    
    while True:
        # Limpiar consola (funciona en cmd y PowerShell)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"--- Sección: {title.upper()} ---")
        print("Usa FLECHA ARRIBA/ABAJO para mover, ESPACIO para marcar/desmarcar, ENTER para confirmar.\n")
        
        for i, item in enumerate(items):
            pointer = ">" if i == current_idx else " "
            check = "(*)" if i in selected else "( )"
            print(f" {pointer} {check} {item}")
            
        key = msvcrt.getch()
        
        # Flechas en Windows devuelven 2 bytes: \xe0 o \x00, seguido del código
        if key in (b'\xe0', b'\x00'):
            key = msvcrt.getch()
            if key == b'H': # Flecha arriba
                current_idx = (current_idx - 1) % len(items)
            elif key == b'P': # Flecha abajo
                current_idx = (current_idx + 1) % len(items)
        elif key == b' ': # Espacio
            if current_idx in selected:
                selected.remove(current_idx)
            else:
                selected.add(current_idx)
        elif key in (b'\r', b'\n'): # Enter
            break
            
    return sorted(list(selected))

def main():
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
        
    # Guardar opciones temporalmente
    choices_path = os.path.join(base_dir, '.build_choices.json')
    with open(choices_path, 'w', encoding='utf-8') as f:
        json.dump(choices, f)
        
    # Compilar
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Compilando documento ({lang}.pdf) con tu selección...")
    cmd = rf'pdflatex -shell-escape -jobname="CV-BrunoVelazquez" "\def\cvlang{{{lang}}}\input{{main.tex}}"'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"\n¡CV compilado exitosamente! Revisa el archivo {lang}.pdf")
    except subprocess.CalledProcessError:
        print("\nHubo un error al compilar el PDF. Revisa los logs.")
    finally:
        if os.path.exists(choices_path):
            os.remove(choices_path)

if __name__ == "__main__":
    main()
