# Cybersecurity Python Journey

Mon carnet d'apprentissage de Python orienté cybersécurité.
Je documente tout ici : exercices, scripts, erreurs, corrections.

L'objectif : construire au fil des semaines de petits outils concrets
pour progresser vers un profil analyste SOC (Security Operations Center).

## Comment lire ce dépôt

- Chaque dossier numeroté correspond à un sujet.
- Chaque dossier contient un `README.md` qui explique ce qu'il y a dedans.
- Les notebooks `.ipynb` sont mes notes de travail, avec les erreurs et corrections.

---

## Progression

### Semaine 1 — Fondamentaux Python

**Fichiers :**
- [`01_fundamentals/week1.ipynb`](01_fundamentals/week1.ipynb) — notebook de travail
- [`01_fundamentals/README.md`](01_fundamentals/README.md) — notes

**Sujets couverts :**
- Variables et types (`str`, `int`, `bool`, `None`)
- Listes, tuples, dictionnaires
- Conditions et boucles (`if/elif/else`, `for`, `while`, `break`, `continue`)
- Fonctions (`def`, `return`, paramètres)
- Chaînes de caractères (`strip`, `split`, slicing, f-strings)
- Lecture et écriture de fichiers (`with open(...)`)
- Premiers pas en regex avec `re` (`findall`, `search`)
- Mini-outil : détection de brute-force dans un fichier de log (compte les FAILED par IP, seuil 3)

### Semaine 2 — Outils en ligne de commande

**Fichiers :**
- [`02_cli_tools/ip_report.py`](02_cli_tools/ip_report.py) — analyse de logs IP
- [`02_cli_tools/ip_classifiers.py`](02_cli_tools/ip_classifiers.py) — classification d'IP
- [`02_cli_tools/week2.ipynb`](02_cli_tools/week2.ipynb) — notebook de travail
- [`03_networking/mini_scanner.py`](03_networking/mini_scanner.py) — scanner TCP localhost

**Sujets couverts :**
- `sys.argv` — arguments en ligne de commande
- `sys.exit()` — codes de sortie
- `if __name__ == "__main__"` — point d'entrée
- `ipaddress` — validation et classification d'IP (private/public/loopback/invalid)
- JSON (`json.dump`, `json.load`)
- CSV (`csv.DictWriter`)
- `try/except` — gestion d'erreurs (`FileNotFoundError`, `PermissionError`, `CalledProcessError`)
- `socket` — créer une socket TCP, timeout, `connect_ex`, scanner des ports sur localhost

**Outils construits :**
- `ip_report.py` : lit un log, extrait les IPs, les classe, produit 3 rapports (txt, json, csv)
- `ip_classifiers.py` : module réutilisable pour valider et classer une IP
- `mini_scanner.py` : teste si des ports TCP sont ouverts sur `127.0.0.1`

### Semaine 3 — Outils système et web

**Fichiers :**
- [`05_hashing/file_hasher.py`](05_hashing/file_hasher.py) — SHA256 d'un fichier
- [`06_file_system/log_finder.py`](06_file_system/log_finder.py) — trouve tous les `.log`
- [`06_file_system/cmd_runner.py`](06_file_system/cmd_runner.py) — exécute une commande système
- [`07_regex_advanced/log_parser.py`](07_regex_advanced/log_parser.py) — parse des logs syslog et kernel
- [`08_http/url_checker.py`](08_http/url_checker.py) — vérifie les headers de sécurité d'un site

**Sujets couverts :**
- `hashlib` — SHA256, lecture de fichier par blocs
- `pathlib` — parcours récursif (`rglob`), `Path.stat()`
- `subprocess` — exécuter des commandes, capturer sortie, gérer erreurs
- Regex avancée — groupes nommés `(?P<name>...)`, `groupdict()`, groupes non-capturants `(?:...)`
- `requests` — requêtes HTTP, status, headers, cookies, redirections
- `ssl` — certificat TLS

**Outils construits :**
- `file_hasher.py` : calcule le SHA256 d'un fichier par blocs (validé contre `sha256sum`)
- `log_finder.py` : trouve tous les `.log` d'une arborescence avec taille et hash
- `cmd_runner.py` : wrapper autour de `subprocess.run`, affiche sortie et code de retour
- `log_parser.py` : parse des logs syslog, kernel, SSH et UFW en un dict structuré
- `url_checker.py` : analyse une URL (status, 6 headers de sécurité, cookies, redirections, certificat TLS)

---

## Structure du dépôt

cybersecurity-python-journey/
├── README.md ← ce fichier
├── .gitignore
├── 01_fundamentals/ ← notebook semaine 1
├── 02_cli_tools/ ← ip_report, ip_classifiers, week2
├── 03_networking/ ← mini_scanner
├── 05_hashing/ ← file_hasher
├── 06_file_system/ ← log_finder, cmd_runner
├── 07_regex_advanced/ ← log_parser
└── 08_http/ ← url_checker


---

## Compétences travaillées

**Python :**
- Structurer un script en fonctions
- Arguments en ligne de commande (`sys.argv`)
- Gestion d'erreurs (`try/except`)
- Lecture/écriture de fichiers (texte, binaire, JSON, CSV)
- Regex simple et avancée
- Modules standards (`hashlib`, `pathlib`, `subprocess`, `socket`, `ssl`)
- Modules externes (`requests`)
- Connexions réseau (TCP, HTTP, TLS)

**Cybersécurité :**
- Analyse de logs (extraction, comptage, classification)
- Détection de brute-force (seuil de tentatives échouées)
- Validation et classification d'IP (private/public/loopback/invalid)
- Hachage de fichiers (intégrité, comparaison avec `sha256sum`)
- Scan de ports sur localhost
- Parsing de logs système (syslog, kernel, SSH, UFW)
- Reconnaissance web (headers de sécurité, cookies, TLS)

---

## Roadmap

- [x] Fundamentals (variables, types, listes, tuples, dicts)
- [x] Conditions et boucles
- [x] Fonctions
- [x] Chaînes de caractères
- [x] Lecture/écriture de fichiers
- [x] Regex simple
- [x] CLI (sys.argv, sys.exit)
- [x] `ipaddress` (validation, classification)
- [x] Rapports JSON et CSV
- [x] Gestion d'erreurs (try/except)
- [x] Sockets TCP (scanner localhost)
- [x] Hachage SHA256
- [x] `pathlib` (parcours de fichiers)
- [x] `subprocess` (exécution de commandes)
- [x] Regex avancée (groupes nommés, non-capturants)
- [x] HTTP et reconnaissance web (requests, ssl)
- [ ] Hachage avancé (intégrité multi-fichiers, API VirusTotal)
- [ ] Web scraping (BeautifulSoup)
- [ ] Programmation asynchrone (asyncio)
- [ ] Frameworks de sécurité (`scapy`, `paramiko`, `impacket`)

---

## Environnement

- Python 3.13
- Linux (Ubuntu / Debian)
- VS Code
- Package externe : `requests` (installé via `pip`)

---

## Notes personnelles

Je progresse lentement mais je refais chaque exercice moi-même.
Les erreurs que j'ai rencontrées sont documentées dans les notebooks.
Prochaine étape : approfondir le hachage (intégrité de fichiers,
détection de malware par hash) puis attaquer le web scraping.

---

*"Slow is smooth. Smooth is fast."*
