import sys
from pathlib import Path
from file_hasher import hash_file

def load_hashes(hashes_file):
    # Je vais ranger ici chaque fichier avec le hash auquel je le comparerai.
    hashes_original = {}
    # Je parcours le fichier témoin ligne par ligne.
    with open(hashes_file, "r") as f:
        for line in f:
            # Je nettoie la ligne, notamment pour enlever le retour à la ligne.
            line = line.strip()
            # Une ligne vide n'a rien à ajouter, je passe donc à la suivante.
            if not line:
                continue
            # Dans ce fichier, le hash est écrit avant le nom du fichier.
            parts = line.split()
            hash_attendu = parts[0]
            nom_du_fichier = parts[1]
            # Je pourrai ainsi retrouver le hash attendu à partir du nom du fichier.
            hashes_original[nom_du_fichier] = hash_attendu
    # J'ai terminé la lecture : je renvoie tous les noms et leurs hashes.
    return hashes_original


def check_file(directory, name, expected_hash):
    """
    Je cherche le fichier dans le dossier, puis je compare son hash
    à celui enregistré dans le fichier témoin.
    """
    # rglob me permet de chercher aussi dans les sous-dossiers.
    fichiers = list(directory.rglob(name))
    # Sans résultat, je sais que le fichier témoin n'est pas dans ce dossier.
    if not fichiers:
        return "NOT_FOUND"
    # Je garde le premier fichier trouvé pour faire la comparaison.
    fichier_a_checker = fichiers[0]
    # La fonction de hash attend le chemin du fichier sous forme de texte.
    hash_fichier = hash_file(str(fichier_a_checker))
    # Si les deux hashes diffèrent, le contenu a changé depuis la référence.
    if expected_hash == hash_fichier:
        return "OK"
    else:
        return "MODIFIED"


def display_result(name, status):
    # J'associe un symbole facile à repérer à chaque résultat.
    if status == "OK":
        print(f"[✓] {name:<25} OK")
    elif status == "MODIFIED":
        print(f"[✗] {name:<25} MODIFIED")
    elif status == "NOT_FOUND":
        print(f"[?] {name:<25} NOT FOUND")


def main():
    """
    Je vérifie les fichiers indiqués et je termine par un petit bilan.
    """
    # Il me faut le fichier témoin et le dossier à vérifier.
    if len(sys.argv) < 3:
        print("Usage: python3 integrity_checker.py <hashes_file> <directory>")
        sys.exit(1)

    # Je récupère les deux chemins transmis au lancement du programme.
    hashes_file = sys.argv[1]
    directory = Path(sys.argv[2])

    # Je vérifie les chemins avant de commencer, pour expliquer clairement
    # ce qui manque plutôt que de laisser le programme échouer plus loin.
    if not Path(hashes_file).exists():
        print(f"Error: hashes file '{hashes_file}' not found")
        sys.exit(1)

    if not directory.exists():
        print(f"Error: directory '{directory}' not found")
        sys.exit(1)

    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory")
        sys.exit(1)

    # Je charge les références qui serviront aux comparaisons.
    hashes = load_hashes(hashes_file)

    # Je compte séparément les fichiers intacts, modifiés et introuvables.
    ok_count = 0
    modified_count = 0
    missing_count = 0

    # Je vérifie chaque fichier référencé et j'affiche son résultat.
    for name, expected_hash in hashes.items():
        status = check_file(directory, name, expected_hash)
        display_result(name, status)

        # Je mets à jour le compteur correspondant au résultat obtenu.
        if status == "OK":
            ok_count += 1
        elif status == "MODIFIED":
            modified_count += 1
        else:
            missing_count += 1

    # Le bilan me donne le nombre de fichiers dans chaque catégorie.
    print(f"\nSummary: {ok_count} OK, {modified_count} modified, {missing_count} missing")


if __name__ == "__main__":
    main()