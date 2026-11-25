"""
log_analyzer.py — Analyseur de logs généraliste

Détecte automatiquement le format (SSH, Apache, firewall, unknown)
et extrait les éléments universels (IPs, emails, URLs, timestamps)
ainsi que les champs spécifiques au format.

Usage:
    python3 log_analyzer.py <logfile>
    python3 log_analyzer.py <logfile> --format ssh
    python3 log_analyzer.py <logfile> --format apache

Formats supportés:
    - ssh      : logs syslog SSH (ex: "Failed password for admin from 10.0.0.5")
    - apache   : logs Apache/Nginx (ex: "10.0.0.5 - - [15/Jan/2024] GET /index.html 200")
    - firewall : logs UFW/iptables (ex: "SRC=10.0.0.5 DST=10.0.0.1 PROTO=TCP DPT=22")
    - unknown  : format non reconnu (extraction universelle seulement)
"""

import sys
import re
from collections import Counter


# ============================================================
# CONSTANTES — Patterns de détection
# ============================================================

# Regex universels (valables pour tous les formats)
IP_PATTERN = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
URL_PATTERN = r"https?://[^\s<>\"']+"

# Regex de timestamps (plusieurs formats courants)
TIMESTAMP_PATTERNS = [
    r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}",           # 2024-01-15 10:23:45
    r"\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}",              # 15/Jan/2024:10:23:45
    r"\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}",              # Jan 15 10:23:45
]

# Regex spécifiques par format
SSH_PATTERNS = {
    "ip": IP_PATTERN,
    "user": r"user=(\w+)",
    "user_alt": r"for (?:invalid user )?(\w+) from",
    "status": r"^\[(\w+)\]",
    "port": r"port (\d+)",
}

APACHE_PATTERNS = {
    "ip": r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
    "method": r'"(\w+) [^"]*"',
    "status": r'" \d{3} (\d{3}) ',
    "path": r'"(?:GET|POST|PUT|DELETE) ([^ ]+) ',
}

FIREWALL_PATTERNS = {
    "src": r"SRC=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
    "dst": r"DST=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
    "proto": r"PROTO=(\w+)",
    "port": r"(?:DPT|DPT=)(\d+)",
}


# ============================================================
# LECTURE DU FICHIER
# ============================================================

def read_log(filename):
    """
    Lit un fichier de logs et retourne la liste des lignes non vides.
    
    Args:
        filename: chemin du fichier
    
    Returns:
        liste de strings (lignes nettoyées)
    """
    lines = []
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line)
    return lines


# ============================================================
# DÉTECTION DU FORMAT
# ============================================================

def detect_format(lines):
    """
    Détecte le format du log en testant chaque ligne sur plusieurs patterns.
    Retourne le format majoritaire.
    
    Args:
        lines: liste de lignes
    
    Returns:
        "ssh" | "apache" | "firewall" | "unknown"
    """
    # Compteurs de matches par format
    ssh_count = 0
    apache_count = 0
    firewall_count = 0

    for line in lines:
        # SSH : lignes avec [LEVEL] ou "sshd[" ou "user="
        if re.match(r"^\[\w+\]", line) or "sshd[" in line or "user=" in line:
            ssh_count += 1
        # Apache : lignes avec IP au début + crochets + méthode HTTP
        elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} .+ \[.+?\] "\w+ ', line):
            apache_count += 1
        # Firewall : lignes avec SRC= ou DST= ou PROTO=
        elif "SRC=" in line or "DST=" in line or "PROTO=" in line:
            firewall_count += 1

    # Majorité
    counts = {"ssh": ssh_count, "apache": apache_count, "firewall": firewall_count}
    max_format = max(counts, key=counts.get)
    max_count = counts[max_format]

    # Si aucun format n'a plus de 10% des lignes → unknown
    if max_count == 0 or max_count < len(lines) * 0.1:
        return "unknown"

    return max_format


# ============================================================
# EXTRACTION UNIVERSELLE
# ============================================================

def extract_ips(lines):
    """
    Extrait toutes les IPs de toutes les lignes.
    Utilise un pattern universel (valable pour tous les formats).
    """
    ips = []
    for line in lines:
        ips.extend(re.findall(IP_PATTERN, line))
    return ips


def extract_emails(lines):
    """Extrait tous les emails de toutes les lignes."""
    emails = []
    for line in lines:
        emails.extend(re.findall(EMAIL_PATTERN, line))
    return emails


def extract_urls(lines):
    """Extrait toutes les URLs de toutes les lignes."""
    urls = []
    for line in lines:
        urls.extend(re.findall(URL_PATTERN, line))
    return urls


def extract_timestamps(lines):
    """
    Extrait tous les timestamps de toutes les lignes.
    Essaie plusieurs formats (voir TIMESTAMP_PATTERNS).
    """
    timestamps = []
    for line in lines:
        for pattern in TIMESTAMP_PATTERNS:
            matches = re.findall(pattern, line)
            timestamps.extend(matches)
    return timestamps


# ============================================================
# EXTRACTION SPÉCIFIQUE PAR FORMAT
# ============================================================

def extract_ssh_fields(lines):
    """
    Extrait les champs spécifiques SSH : users, statuses, ports.
    Retourne un dict {users: [...], statuses: [...], ports: [...]}.
    """
    users = []
    statuses = []
    ports = []

    for line in lines:
        # User : "user=admin" ou "for invalid user admin"
        m = re.search(SSH_PATTERNS["user"], line)
        if not m:
            m = re.search(SSH_PATTERNS["user_alt"], line)
        if m:
            users.append(m.group(1))

        # Status : "[FAILED]" ou "[SUCCESS]"
        m = re.search(SSH_PATTERNS["status"], line)
        if m:
            statuses.append(m.group(1))

        # Port : "port 22"
        m = re.search(SSH_PATTERNS["port"], line)
        if m:
            ports.append(m.group(1))

    return {"users": users, "statuses": statuses, "ports": ports}


def extract_apache_fields(lines):
    """
    Extrait les champs spécifiques Apache/Nginx : methods, status_codes, paths.
    """
    methods = []
    status_codes = []
    paths = []

    for line in lines:
        # Méthode HTTP : "GET", "POST", etc.
        m = re.search(APACHE_PATTERNS["method"], line)
        if m:
            methods.append(m.group(1))

        # Code de statut : 200, 404, etc.
        m = re.search(APACHE_PATTERNS["status"], line)
        if m:
            status_codes.append(m.group(1))

        # Chemin : "/index.html"
        m = re.search(APACHE_PATTERNS["path"], line)
        if m:
            paths.append(m.group(1))

    return {"methods": methods, "status_codes": status_codes, "paths": paths}


def extract_firewall_fields(lines):
    """
    Extrait les champs spécifiques firewall : src, dst, proto, ports.
    """
    src_ips = []
    dst_ips = []
    protos = []
    ports = []

    for line in lines:
        m = re.search(FIREWALL_PATTERNS["src"], line)
        if m:
            src_ips.append(m.group(1))

        m = re.search(FIREWALL_PATTERNS["dst"], line)
        if m:
            dst_ips.append(m.group(1))

        m = re.search(FIREWALL_PATTERNS["proto"], line)
        if m:
            protos.append(m.group(1))

        m = re.search(FIREWALL_PATTERNS["port"], line)
        if m:
            ports.append(m.group(1))

    return {"src_ips": src_ips, "dst_ips": dst_ips, "protos": protos, "ports": ports}


# ============================================================
# AFFICHAGE
# ============================================================

def display_counter(title, counter, limit=10):
    """
    Affiche un Counter de façon formatée.
    
    Args:
        title   : titre de la section
        counter : Counter (ou liste, sera convertie)
        limit   : nombre d'éléments à afficher
    """
    if not counter:
        print(f"\n=== {title} ===")
        print("(none found)")
        return

    if not isinstance(counter, Counter):
        counter = Counter(counter)

    print(f"\n=== {title} ===")
    for item, count in counter.most_common(limit):
        print(f"{item:<30} {count}")


# ============================================================
# MAIN
# ============================================================

def main():
    # 1. Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage: python3 log_analyzer.py <logfile> [--format <format>]")
        print("  Formats: ssh, apache, firewall, unknown (default: auto-detect)")
        sys.exit(1)

    filename = sys.argv[1]

    # 2. Format forcé si --format est passé
    forced_format = None
    if "--format" in sys.argv:
        idx = sys.argv.index("--format")
        if idx + 1 < len(sys.argv):
            forced_format = sys.argv[idx + 1]
            if forced_format not in ["ssh", "apache", "firewall", "unknown"]:
                print(f"Error: unknown format '{forced_format}'")
                print("Valid formats: ssh, apache, firewall, unknown")
                sys.exit(1)

    # 3. Lire le fichier
    try:
        lines = read_log(filename)
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found")
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied for '{filename}'")
        sys.exit(1)

    if not lines:
        print(f"Warning: no lines found in '{filename}'")
        sys.exit(0)

    # 4. Détecter le format (ou utiliser le format forcé)
    if forced_format:
        detected_format = forced_format
        format_source = "(forced)"
    else:
        detected_format = detect_format(lines)
        format_source = "(auto-detected)"

    # 5. En-tête
    print(f"=== Log Analysis: {filename} ===")
    print(f"Format: {detected_format} {format_source}")
    print(f"Total lines: {len(lines)}")

    # 6. Extraction universelle
    ips = extract_ips(lines)
    emails = extract_emails(lines)
    urls = extract_urls(lines)
    timestamps = extract_timestamps(lines)

    print(f"\n=== Universal Patterns ===")
    print(f"IPs:        {len(set(ips))} unique")
    print(f"Emails:     {len(set(emails))} unique")
    print(f"URLs:       {len(set(urls))} unique")
    print(f"Timestamps: {len(timestamps)} found")

    # 7. Affichage des tops universels
    display_counter("Top 10 IPs", Counter(ips), 10)
    display_counter("Top 10 Emails", Counter(emails), 10)
    display_counter("Top 10 URLs", Counter(urls), 10)

    # 8. Analyse spécifique au format
    if detected_format == "ssh":
        fields = extract_ssh_fields(lines)
        display_counter("Top Users (SSH)", Counter(fields["users"]), 10)
        display_counter("Status Distribution (SSH)", Counter(fields["statuses"]), 10)
        display_counter("Top Ports (SSH)", Counter(fields["ports"]), 10)

    elif detected_format == "apache":
        fields = extract_apache_fields(lines)
        display_counter("HTTP Methods (Apache)", Counter(fields["methods"]), 10)
        display_counter("Status Codes (Apache)", Counter(fields["status_codes"]), 10)
        display_counter("Top Paths (Apache)", Counter(fields["paths"]), 10)

    elif detected_format == "firewall":
        fields = extract_firewall_fields(lines)
        display_counter("Top Source IPs (Firewall)", Counter(fields["src_ips"]), 10)
        display_counter("Top Dest IPs (Firewall)", Counter(fields["dst_ips"]), 10)
        display_counter("Protocols (Firewall)", Counter(fields["protos"]), 10)
        display_counter("Top Ports (Firewall)", Counter(fields["ports"]), 10)

    # Si format unknown → on a déjà affiché les universels, c'est tout


if __name__ == "__main__":
    main()