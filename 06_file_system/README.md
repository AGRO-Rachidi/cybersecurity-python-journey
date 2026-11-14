# Outils de fichiers

Ce dossier contient deux  petits outils pour travailler avec des fichiers
et exécuter des commandes système.

---

## 1. `log_finder.py` — Trouve tous les fichiers .log d'un dossier

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

## 2. `cmd_runner.py` — Exécute une commande système

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
   


