# Ces modules servent à lire le fichier, préparer les rapports et les enregistrer.
import re
import sys
from ip_classifiers import classify
import json
from datetime import datetime
import csv


def extract_ip(filename):
    # Le dictionnaire gardera chaque adresse avec son nombre d'apparitions.
    count = {}

    # On parcourt le fichier une ligne à la fois.
    with open(filename, "r") as f:
        for line in f:
            # Cette expression repère les textes qui ressemblent à des IPv4.
            IPs = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            for ip in IPs:
                # Si l'adresse est déjà là, on augmente son compteur.
                if ip in count:
                    count[ip] += 1
                else:
                    # Sinon, on la range dans le dictionnaire pour la première fois.
                    count[ip] = 1
                    
    if not count:
        print(f"Warning: no IP found in {filename}!")
        return {}
    return count

def build_report(count):
    # Le rapport en texte commence par son titre et le nombre d'adresses différentes.
    text = "===IP Activity Report==========\n"
    text += f"Total number of unique IPs: {len(count)}\n"
    text += "\n"

    # On affiche d'abord les adresses qui apparaissent le plus souvent.
    for ip, nbre in sorted(count.items(), key=lambda x:x[1], reverse=True):
        # Le mot change un peu quand il n'y a qu'une seule apparition.
        label = "appearance" if nbre == 1 else "appearances"
        type_ip = classify(ip)
        text += f"IP {ip:<18} -> {nbre} {label:>12} ({type_ip})\n"
    return text


def build_json(count):
    # Le JSON contient un résumé, la date de création et la liste des IP.
    data = {
        "total_unique_ips": len(count),
        "generated_at": datetime.now().isoformat(),
        "ips": []
    }

    # Chaque adresse est ajoutée avec son compteur et sa catégorie.
    for ip, nbre in sorted(count.items(), key=lambda x:x[1], reverse= True):
        data["ips"].append({
            "ip": ip,
            "count":nbre,
            "type": classify(ip)
        })
    return data


def build_csv(data):
    # On crée un fichier CSV avec une colonne pour chaque information.
    with open("report_ip.csv","w",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames =["ip", "count","type"])
        writer.writeheader()
        # Une ligne du rapport devient une ligne du fichier CSV.
        for entry in data["ips"]:
            writer.writerow(entry)
    return writer


def main():
    # Le nom du fichier à analyser doit être donné après le nom du script.
    if len(sys.argv) < 2:
        print("Usage: python ip_report.py <logfile>")
        sys.exit(1)
    filename = sys.argv[1]

    # On récupère les adresses et on prépare le rapport lisible.
    try:
        extract = extract_ip(filename)
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        print("Usage: python3 ip_report.py <logfile>")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied for '{filename}'.")
        sys.exit(1)
    
    if not extract:
        print("No IPs to report. Exiting...")
        sys.exit(0)    
    report = build_report(extract)
    # On enregistre le rapport en texte, puis on l'affiche aussi à l'écran.
    with open("report_ip.txt","w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    print("report is written to report_ip.txt\n")

    # On prépare et enregistre la version JSON du même rapport.
    data = build_json(extract) 
    with open("report_ip.json","w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)     
    print("json report is written in report_ip.json\n")

    # Enfin, on crée le rapport CSV.
    build_csv(data)
    print("CSV report is written in report_ip.csv")


if __name__ == "__main__":
    # Cette condition lance main() quand on exécute directement ce fichier.
    main()