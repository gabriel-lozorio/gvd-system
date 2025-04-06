import os

IGNORAR = ["venv", "debug", "pycache", ".git", ".vscode", ".idea", ".gitignore", ".gitattributes", ".editorconfig", ".env.example"]

def get_structure(base_path, prefix="", lines=None):
    if lines is None:
        lines = []

    try:
        entries = os.listdir(base_path)
    except PermissionError:
        return lines  # Ignora diretórios sem permissão

    dirs = []
    files = []
    for e in entries:
        if any(term in e for term in IGNORAR):
            continue
        
        full_path = os.path.join(base_path, e)
        if os.path.isdir(full_path):
            dirs.append(e)
        else:
            files.append(e)

    dirs.sort()
    files.sort()
    sorted_entries = dirs + files

    for index, entry in enumerate(sorted_entries):
        path = os.path.join(base_path, entry)
        connector = "└──" if index == len(sorted_entries) - 1 else "├──"
        
        if os.path.isdir(path):
            lines.append(f"{prefix}{connector} {entry}/")
            new_prefix = f"{prefix}{'    ' if index == len(sorted_entries) - 1 else '│   '}"
            get_structure(path, new_prefix, lines)
        else:
            lines.append(f"{prefix}{connector} {entry}")
    
    return lines

def save_structure_as_MD(base_path, MD_file_name="estrutura_projeto.MD"):
    structure_lines = get_structure(base_path)
    # Cria a pasta de destino, se não existir
    os.makedirs(os.path.dirname(MD_file_name), exist_ok=True)
    
    with open(MD_file_name, "w", encoding="utf-8") as f:
        f.write("# Estrutura do Projeto\n\n")
        for line in structure_lines:
            f.write(line + "\n")

    print(f"Arquivo '{MD_file_name}' criado com a estrutura do projeto.")

if __name__ == "__main__":
    # Define o diretório raiz que deseja analisar:
    BASE_PATH = "."  # Diretório atual ou qualquer outro caminho absoluto/relativo
    
    # Define o nome do arquivo (dentro da pasta 'debug')
    OUTPUT_FILE = "debug/estrutura_projeto.MD"
    
    save_structure_as_MD(BASE_PATH, OUTPUT_FILE)
