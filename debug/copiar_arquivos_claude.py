import os
import shutil

def copiar_arquivos(origem: str, destino: str, ignorados=None, selecionados=None, tipos_ignorados=None):
    """
    Copia recursivamente os arquivos do diretório 'origem' para o diretório 'destino',
    aplicando três filtragens:
    
    1. Ignora arquivos ou pastas especificadas na lista 'ignorados'.
    2. Copia somente os arquivos que estejam dentro de pastas selecionadas, conforme a lista 'selecionados'.
       - A lista 'selecionados' deve conter os caminhos (relativos à 'origem') das pastas a serem copiadas.
       - É possível especificar pastas internas, como "agents/definition".
       - Se a lista 'selecionados' contiver a string "todos", todos os arquivos (exceto os ignorados) serão copiados.
    3. Ignora arquivos com extensões especificadas na lista 'tipos_ignorados'.
       - Por exemplo: [".json", ".log", ...]
       
    Além disso, o nome do arquivo copiado será o caminho relativo (da 'origem') com os separadores de diretório 
    substituídos por underlines. Por exemplo:
      agents/definition/atena.py  ->  agents_definition_atena.py
    
    :param origem: Caminho do diretório de origem.
    :param destino: Caminho do diretório de destino (será criado se não existir).
    :param ignorados: Lista de caminhos ou nomes de arquivos/pastas a serem ignorados.
    :param selecionados: Lista de pastas (caminhos relativos) a serem copiadas ou ["todos"] para copiar tudo.
    :param tipos_ignorados: Lista de extensões de arquivos a serem ignoradas, como [".json", ".log"].
    """
    if ignorados is None:
        ignorados = []
    if selecionados is None:
        selecionados = ["todos"]
    if tipos_ignorados is None:
        tipos_ignorados = []

    # Normaliza os itens ignorados: remove barras no final e converte barras invertidas para normais.
    ignorados_norm = [item.replace("\\", "/").rstrip("/") for item in ignorados]

    # Normaliza os itens de seleção
    selecionados_norm = [sel.replace("\\", "/").rstrip("/") for sel in selecionados]

    # Normaliza os tipos de arquivos ignorados (para comparação em minúsculo)
    tipos_ignorados_norm = [tipo.lower() for tipo in tipos_ignorados]

    origem = os.path.abspath(origem)
    os.makedirs(destino, exist_ok=True)

    for raiz, dirs, arquivos in os.walk(origem):
        rel_root = os.path.relpath(raiz, origem)
        if rel_root == ".":
            rel_root = ""
        else:
            rel_root = rel_root.replace("\\", "/").rstrip("/")

        # Atualiza a lista de diretórios, ignorando os especificados
        dirs[:] = [
            d for d in dirs 
            if os.path.join(rel_root, d).replace("\\", "/").rstrip("/") not in ignorados_norm
            and d not in ignorados_norm
        ]

        for arquivo in arquivos:
            # Verifica se a extensão do arquivo deve ser ignorada
            ext = os.path.splitext(arquivo)[1].lower()
            if ext in tipos_ignorados_norm:
                continue

            # Calcula e normaliza o caminho relativo do arquivo
            rel_file = os.path.join(rel_root, arquivo).replace("\\", "/").rstrip("/")
            if arquivo in ignorados_norm or rel_file in ignorados_norm:
                continue

            # Verifica se o arquivo pertence a uma das pastas selecionadas
            if "todos" not in selecionados_norm:
                permitido = False
                for sel in selecionados_norm:
                    if rel_file.startswith(sel + "/") or rel_file == sel:
                        permitido = True
                        break
                if not permitido:
                    continue

            caminho_origem = os.path.join(raiz, arquivo)
            # Novo nome: caminho relativo com separadores substituídos por underlines.
            novo_nome = rel_file.replace("/", "_")
            caminho_destino = os.path.join(destino, novo_nome)
            shutil.copy2(caminho_origem, caminho_destino)
            print(f"Copiado: {caminho_origem} -> {caminho_destino}")

if __name__ == "__main__":
    diretorio_origem = r"C:\projects\financial-system\financial-system"
    diretorio_destino = r"C:\projects\financial-system\financial-system-claude"
    
    lista_ignorados = [
        # Ambientes e pastas do sistema
        "venv", ".git", ".env", "__pycache__", ".gitignore",

        # Logs e debug
        "debug/",

        # Arquivos de lock e controle de dependências
        "requirements.txt",

        # Documentação
#        "docs/",

        # Outros
        ".gitgnore", "db.sqlite3",

        #APIs e serviços

        # Itens específicos
        
    ]

    
    # Exemplo de seleção: copiar todas as pastas (exceto as ignoradas)
    selecionados = ["todos"]
    
    # Exemplo de tipos de arquivos a serem ignorados
    tipos_ignorados = [".json", ".log", ".lock", ".md", ".txt", ".csv", ".xlsx", ".xls", ".docx", ".pptx",".pyc", ".pyo", ".egg-info", ".whl", ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z",".git",".env", ".idea", ".vscode", ".DS_Store", ".coverage", ".pytest_cache", "__pycache__", ".mypy_cache", ".tox", ".eggs", ".eggs-info",".conf",".toml"]
    
    copiar_arquivos(diretorio_origem, diretorio_destino, lista_ignorados, selecionados, tipos_ignorados)

print(f"Total de arquivos copiados: {len(os.listdir(diretorio_destino))}")
print("Arquivos copiados com sucesso!")