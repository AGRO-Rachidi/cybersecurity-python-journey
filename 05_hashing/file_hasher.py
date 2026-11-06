import hashlib
import os
import sys

# On lit le fichier par petits blocs pour éviter de tout charger en mémoire.
def hash_file(filename):
    # Objet utilisé pour calculer le hash SHA-256.
    h = hashlib.sha256()

    # On ouvre le fichier en mode binaire pour lire des octets.
    with open(filename, "rb") as f:
        while True:
            # On prend 8192 octets à chaque tour.
            chunk = f.read(8192)
            if chunk == b"":
                break
            else:
                # On ajoute ce morceau au calcul du hash.
                h.update(chunk)

    # On retourne le hash final en version hexadécimale.
    return h.hexdigest()

# On récupère la taille du fichier pour l’afficher ensuite.
def file_size(filename):
    size = os.path.getsize(filename)
    return size

# Point d’entrée du script.
def main():
    # Si le bon argument n’a pas été donné, on affiche l’usage du script.
    if len(sys.argv) < 2:
        print("Error!")
        print("Usage: python3 file_hasher.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        # On calcule le hash du fichier demandé.
        h = hash_file(filename)
    except FileNotFoundError:
        # Le fichier n’existe pas.
        print(f"Error: file '{filename}' not found")
        sys.exit(1)
    except PermissionError:
        # On n’a pas les droits pour lire ce fichier.
        print(f"Error: permission for '{filename}' denied")
        sys.exit(1)

    # On récupère la taille avant d’afficher le résultat final.
    size = file_size(filename)
    print(f"File: {filename}")
    print(f"Size: {size}")
    print(f"Hash: {h}")

# Ce code ne s’exécute que si le script est lancé directement.
if __name__ == "__main__":
    main()