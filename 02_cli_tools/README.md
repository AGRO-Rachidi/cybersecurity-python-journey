# ip_report.py

Petit outil qui lit un fichier de log, extrait toutes les adresses IP
présentes et produit un rapport trié par nombre d'apparitions.

## Utilisation

```bash
python3 ip_report.py <fichier.log>
Exemple:
$ python3 ip_report.py fake-access.log
===IP Activity Report=========================
Total number of unique IPs: 3

IP 10.0.0.5 -> 3 appearances
IP 10.0.0.6 -> 2 appearances
IP 203.0.113.7 -> 1 appearances

report is written to report_ip.txt

Comment ça marche ?
extract_ip() ouvre le fichier, parcourt chaque ligne avec re.findall
et compte les apparitions dans un dict {ip: count}

build_report() trie le dict par valeur décroissante et formate le texte

main() vérifie qu'un argument a été fourni (sys.argv), appelle les
deux fonctions précédentes, écrit le rapport dans report_ip.txt et
l'affiche à l'écran

Ce que je veux améliorer: 
valider les IP avec ipaddress au lieu d'une regex simple

gérer proprement le cas où le fichier n'existe pas (try/except FileNotFoundError)

nettoyer le format du rapport (accents, singulier/pluriel)

