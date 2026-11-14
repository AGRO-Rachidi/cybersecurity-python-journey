# Outils de fichiers

Ce dossier contient trois petits outils pour travailler avec des fichiers
et exécuter des commandes système.

---

## 1. `file_hasher.py` — Calcule l'empreinte SHA256 d'un fichier

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

---

## 2. `log_finder.py` — Trouve tous les fichiers .log d'un dossier

**À quoi ça sert ?**
Quand tu analyses un système, les logs sont éparpillés un peu partout.
Cet outil trouve tous les `.log` d'un coup, avec leur taille et leur hash.

**Comment l'utiliser ?**
python3 log_finder.py <dossier>


**Exemple :**
$ python3 log_finder.py ~/logs
/home/user/logs/app.log
Size: 11 bytes
SHA256: 7f8a3c...

/home/user/logs/sub1/system.log
Size: 9 bytes
SHA256: 2b4e1a...

Found 3 log files


**Ce qu'il fait :**
1. Parcourt le dossier et tous ses sous-dossiers
2. Garde seulement les fichiers qui finissent par `.log`
3. Pour chaque fichier : affiche le chemin, la taille et le hash SHA256
4. Compte le total
5. Si un fichier est protégé (pas les droits de lecture), il l'ignore

---

## 3. `cmd_runner.py` — Exécute une commande système

**À quoi ça sert ?**
Parfois, on veut lancer une commande (comme `ls`, `ss`, `grep`) depuis
Python et récupérer le résultat. Cet outil le fait proprement.

**Comment l'utiliser ?**
python3 cmd_runner.py <commande> [arguments...]


**Exemple :**
$ python3 cmd_runner.py ss -tulnp
Command: ss -tulnp
Exit code: 0

--- Output ---
Netid State Local Address:Port ...
tcp LISTEN 0.0.0.0:22 ...


**Ce qu'il fait :**
1. Prend la commande et ses arguments
2. L'exécute
3. Affiche le code de sortie (0 = succès, autre = erreur)
4. Affiche la sortie
5. Gère deux cas d'erreur :
   - La commande existe mais échoue → affiche l'erreur
   - La commande n'existe pas → affiche "Command not found"
   


