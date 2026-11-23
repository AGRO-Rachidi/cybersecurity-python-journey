# Vérificateur d’intégrité

`integrity_checker.py` compare le hash SHA256 de fichiers avec ceux enregistrés dans un fichier témoin. Il cherche les fichiers dans le dossier indiqué, y compris dans ses sous-dossiers, puis affiche s’ils sont intacts, modifiés ou introuvables.

## Pré-requis

`file_hasher.py` doit être dans le même dossier que `integrity_checker.py`, ou accessible depuis Python. Le vérificateur importe la fonction `hash_file` de ce fichier pour calculer les SHA256.

## Utilisation

```bash
python3 integrity_checker.py <hashes_file> <directory>
```

Par exemple :

```bash
python3 integrity_checker.py hashes.txt ./documents
```

## Fichier témoin

Le fichier de hash suit le format de `sha256sum` : le hash d’abord, puis le nom du fichier. Il faut une ligne par fichier.

```text
b4f3c7a2d8e19f06a3b5c4d2e8f7190a6c3d5b7e9f1a2c4d6e8f0b3a5c7d9e12  notes.txt
f28a6c1d9e4b7f03a5c8d2e6f1b9a4c7d0e3f6b8a2c5d9e1f4b7c0a3d6e9f215  rapport.pdf
```

Les noms de fichiers doivent correspondre à ceux du dossier à vérifier. Le script cherche aussi dans les sous-dossiers. Pour les noms contenant des espaces, ce format n’est pas pris en charge par le découpage actuel des lignes.

## Exemple de sortie

```text
[✓] notes.txt                OK
[✗] rapport.pdf              MODIFIED
[?] ancien.txt               NOT FOUND

Summary: 1 OK, 1 modified, 1 missing
```

`OK` signifie que le hash correspond à celui du fichier témoin. `MODIFIED` indique qu’il est différent, et `NOT FOUND` que le fichier n’a pas été trouvé dans le dossier.

## Ce que j’ai appris

Le plus délicat a été de faire circuler les données entre les étapes : je lis les lignes du fichier témoin, je garde les hash dans un dictionnaire avec le nom du fichier comme clé, puis je récupère la bonne valeur au moment de la comparaison.

J’ai aussi utilisé `Path.rglob()` pour chercher dans les sous-dossiers. Si deux fichiers ont le même nom dans des sous-dossiers différents, le script n’en vérifie qu’un seul : le premier qu’il trouve.
