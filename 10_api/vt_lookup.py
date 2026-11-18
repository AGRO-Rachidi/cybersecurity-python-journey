import os
import sys
import requests
import base64
from datetime import datetime
import time

def get_api_key():
    """
    Récupère la clé API de l'environnement.
    """
    api_key = os.environ.get("VT_API_KEY")
    
    if not api_key:
        print("Error: VT_API_KEY not set")
        print("Run: export VT_API_KEY='your_key_here'")
        sys.exit(1)
    return api_key

def lookup_hash(file_hash, api_key):
    # construit l'URL
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    # fait la requête avec headers
    # gère 404 → return None
    # gère erreurs → return None
    # sinon → return response.json()
    headers = {"x-apikey": api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
    
def lookup_url(target_url, api_key):
    # encode l'URL en base64 (sans padding =)
    url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
    # construit l'URL avec l'ID
    url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    # fait la requête
    # gère 404 et erreurs
    # return JSON ou None
    headers = {"x-apikey": api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
 

def display_result(target, data):
    # si data is None → NOT FOUND
    if data is None:
        print(f"[?] {target}  NOT FOUND   on VirusTotal")
        return
    # sinon → extrait malicious, harmless, undetected
    # affiche verdict + nom + type + date
    attrs = data["data"]["attributes"]
    stats = attrs["last_analysis_stats"]
    malicious = stats["malicious"]
    harmless = stats["harmless"]
    undetected = stats["undetected"]

    total = malicious + harmless + undetected

    if malicious > 0:
        symbol = "✗"
        verdict = f"MALICIOUS ({malicious}/{total} detections)"
    else:
        symbol = "✓"
        verdict = f"CLEAN (0/{total} detections)"

    print(f"[{symbol}] {target}")
    print(f"    Verdict: {verdict}")

    if "meaningful_name" in attrs:
        print(f"    Name: {attrs['meaningful_name']}")
    if "type_description" in attrs:
        print(f"    Type: {attrs['type_description']}")
    if "first_submission_date" in attrs:
        ts = attrs["first_submission_date"]
        date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        print(f"    First seen: {date}")
   
def main():
    # vérifie les arguments (>= 2)
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 vt_lookup.py <hash>")
        print("  python3 vt_lookup.py --file <hashes_file>")
        print("  python3 vt_lookup.py --url <url>")
        sys.exit(1)
    # récupère la clé API
    api_key = get_api_key()
    arg = sys.argv[1]
    # détecte le mode : --file, --url, ou hash simple
    # appelle la bonne fonction + display_result
    if arg == "--file":
        if len(sys.argv) < 3:
            print("Error: --file requires a filename")
            sys.exit(1)
        with open(sys.argv[2], "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                file_hash = line.split()[0]   # prend le 1er champ (hash)
                data = lookup_hash(file_hash, api_key)
                display_result(file_hash, data)
                time.sleep(15)
    elif arg == "--url":
        if len(sys.argv) < 3:
            print("Error: --url requires a URL")
            sys.exit(1)
        target_url = sys.argv[2]
        data = lookup_url(target_url, api_key)
        display_result(target_url, data)
    else:
        data = lookup_hash(arg, api_key)
        display_result(arg, data)
    
if __name__ == "__main__":
    main()
    