# Outils de fichiers
Ce dossier contient un outil pour travailler avec un fichier

---

##  `file_hasher.py` — Calcule l'empreinte SHA256 d'un fichier

**À quoi ça sert ?**
Un hash, c'est comme une empreinte digitale de fichier. Si quelqu'un
modifie le fichier, le hash change complètement. Ça permet de vérifier
qu'un fichier n'a pas été altéré.

**Comment l'utiliser ?**
python3 file_hasher.py <nom_du_fichier>


**Exemple :**
$ python3 file_hasher.py fake-access.log
File: fake-access.log
Size: 254 bytes
SHA256: 66c00833f0e9686a9af55310967ac9d371caaa5ab099ced6179e1f1e3e241086


**Ce qu'il fait :**
1. Ouvre le fichier en mode binaire (octet par octet)
2. Lit le fichier par petits blocs de 8 Ko (pour ne pas saturer la mémoire)
3. Calcule le SHA256 au fur et à mesure
4. Affiche le résultat

**Validé :** le hash produit est identique à celui de `sha256sum` sur Linux.

