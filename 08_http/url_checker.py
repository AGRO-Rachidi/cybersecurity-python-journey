import sys
import requests


SECURITY_HEADERS = [
    # Ceux que je veux repérer en premier.
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]


def check_url(url):
    response = requests.get(url, timeout=5)
    return response


def display_result(response, url):
    print(f"URL: {url}")
    print(f"status: {response.status_code}")
    print(f"URL finale : {response.url}")
    print(f"Server: {response.headers.get('Server', 'Unknown')}")
    print(f"Elapsed: {response.elapsed.total_seconds():.3f}s")


def check_security_headers(response):
    print("\n=== Security Headers ===")
    for header in SECURITY_HEADERS:
        value = response.headers.get(header)
        if value:
            print(f"[✓] {header}: {value}")
        else:
            print(f"[✗] {header}: MISSING")

from http.cookies import SimpleCookie


def check_cookies(response):
    print("\n=== Cookies ===")
    set_cookie_header = response.headers.get("Set-Cookie", "")
    if not set_cookie_header:
        print("No cookies set")
        return

    cookie = SimpleCookie()
    cookie.load(set_cookie_header)
    for name, morsel in cookie.items():
        issues = []
        if not morsel["secure"]:
            issues.append("missing Secure")
        if not morsel["httponly"]:
            issues.append("missing HttpOnly")
        if not morsel["samesite"]:
            issues.append("missing SameSite")

        # Comme ça, on voit tout de suite ce qui manque au cookie.
        status = "✓" if not issues else "✗"
        print(f"[{status}] {name}" + (f" ({', '.join(issues)})" if issues else ""))


def check_server_version(response):
    print("\n=== Server Version ===")
    server = response.headers.get("Server", "unknown")
    print(f"Server: {server}")

    # Ça couvre le format le plus courant : logiciel/version.
    import re
    m = re.search(r"([\w.-]+)/([\d.]+)", server)
    if m:
        software, version = m.groups()
        print(f"Detected: {software} {version}")
        # Pour l'instant, je ne fais qu'afficher la version.
    else:
        print("No version detected")
    


def check_redirects(response):
    print("\n=== Redirects ===")
    if not response.history:
        print("No redirects")
        return

    print(f"{len(response.history)} redirect(s):")
    for i, r in enumerate(response.history, 1):
        print(f"  {i}. {r.status_code} → {r.url}")
    print(f"  Final: {response.url}")
    
    
import ssl
import socket
from urllib.parse import urlparse


def check_tls(url):
    print("\n=== TLS Certificate ===")
    parsed = urlparse(url)
    if parsed.scheme != "https":
        print("Not HTTPS — no TLS")
        return

    host = parsed.hostname
    port = parsed.port or 443

    try:
        # Python vérifie le certificat avec les autorités de confiance du système.
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=5) as sock:
            # J'indique aussi le nom du site, pas seulement son adresse IP.
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

        print(f"Subject: {dict(x[0] for x in cert['subject'])}")
        print(f"Issuer: {dict(x[0] for x in cert['issuer'])}")
        print(f"Valid from: {cert['notBefore']}")
        print(f"Valid until: {cert['notAfter']}")

        # Je calcule le délai restant pour voir rapidement s'il expire bientôt.
        from datetime import datetime
        expiry = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
        days_left = (expiry - datetime.now()).days
        print(f"Days left: {days_left}")
        if days_left < 30:
            print("⚠️ Certificate expires soon!")

    except ssl.SSLError as e:
        print(f"SSL error: {e}")
    except Exception as e:
        print(f"Error: {e}")  


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 url_checker.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        response = check_url(url)
    except requests.exceptions.Timeout:
        print(f"Error: timeout for '{url}'")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"Error: connection failed for '{url}'")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    display_result(response, url)
    check_security_headers(response)
    check_cookies(response)
    check_server_version(response)
    check_redirects(response)
    # Après une redirection, c'est l'URL finale qui compte pour le certificat.
    check_tls(response.url)
    


if __name__ == "__main__":
    main()