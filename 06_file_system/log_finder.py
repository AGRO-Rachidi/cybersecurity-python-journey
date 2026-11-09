import sys
from pathlib import Path
from file_hasher import hash_file

# Cherche les fichiers .log dans le dossier et ses sous-dossiers.
def find_logs(dossier):
    logs = []
    for files in Path(dossier).rglob("*.log"):
        if files.is_file():
            logs.append(files)
    return logs

# Affiche la taille et le hash de chaque fichier trouvé.
def display_results(logs):
    for file in logs:
        try:
            size = file.stat().st_size
            h = hash_file(file)
            print(f"\n{file}")
            print(f"  Size:   {size} bytes")
            print(f"  SHA256: {h}")
        except PermissionError:
            # On passe au fichier suivant si celui-ci n'est pas accessible.
            print(f"\n{file}")
            print(f"  Permission denied — skipped")

# Vérifie le dossier donné en argument, puis lance la recherche.
def main():
    if len(sys.argv)< 2:
        print("Error!")
        print("Usage: python3 log_finder.py <dossier>")
        sys.exit(1)
    dossier = sys.argv[1]
    dossier_path = Path(dossier)

    if not dossier_path.exists():
        print(f"Error: directory '{dossier}' not found")
        sys.exit(1)

    if not dossier_path.is_dir():
        print(f"Error: '{dossier}' is not a directory")
        sys.exit(1)
    try:
       files = find_logs(dossier)
    except PermissionError:
        # Le dossier ne peut pas être parcouru.
        print(f"Error: accès au dossier {dossier} refusé")
    
    if not files:
        print(f"Aucun fichier log trouvé dans le dossier '{dossier}'")
        sys.exit(0)
    display_results(files)
                 
    print(f"{len(files)} fichiers log trouvé")

# Lance le programme seulement si ce fichier est exécuté directement.
if __name__ == "__main__":
    main()
        
      