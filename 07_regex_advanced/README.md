# Parser de logs avec regex avancée

Ce dossier contient un outil qui lit un fichier de logs et en extrait
les informations importantes : date, heure, niveau, utilisateur, IP, port.

---

## `log_parser.py` — Parse des logs syslog et kernel

**À quoi ça sert ?**
Les logs sont du texte brut. Pour les analyser, il faut en extraire
les informations. Cet outil reconnaît deux formats de logs (syslog et
kernel) et en sort les champs utiles.

**Comment l'utiliser ?**
python3 log_parser.py <fichier_de_logs>


**Exemple :**
$ python3 log_parser.py logs_fictifs.log
[WARNING] 2026-10-22 18:10:01 sshd user=admin ip=203.0.113.50 port=45122
[INFO] 2026-10-22 18:10:12 sshd user=agro ip=192.168.1.20 port=45125
[ERROR] 2026-10-22 18:10:30 kernel src=198.51.100.25 dst=192.168.1.10 proto=TCP dpt=22

Summary: 10 parsed, 0 failed


**Ce qu'il fait :**
1. Lit le fichier ligne par ligne
2. Pour chaque ligne, essaie de reconnaître le format :
   - **Syslog** : date, heure, niveau, processus, message
   - **Kernel** : date, heure, niveau, processus "kernel", message
3. Si c'est du SSH, extrait l'utilisateur, l'IP, le port
4. Si c'est du UFW (firewall), extrait source, destination, protocole, port
5. Affiche les champs de façon unifiée
6. Compte les lignes parsées et les lignes non reconnues

**Formats reconnus :**
- Syslog : `date time level process[pid]: message`
- Kernel : `date time level kernel: message`
- SSH dans le message : `user=X ip=Y port=Z`
- UFW dans le message : `SRC=X DST=Y PROTO=Z DPT=N`

**Techniques utilisées :**
- Groupes nommés `(?P<name>...)` pour nommer les champs
- `groupdict()` pour tout récupérer d'un coup
- `re.match` pour valider la structure
- `re.search` pour chercher dans le message
