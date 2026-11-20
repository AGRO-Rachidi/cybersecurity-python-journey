import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def fetch_page(url):
    """
    Récupère le HTML d'une URL.
    Retourne response.text (string) ou None en cas d'erreur.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def extract_links(html, base_url):
    """
    Parse le HTML et retourne une liste de liens uniques.
    """
    soup = BeautifulSoup(html, "html.parser")
    
    links = []
    for a in soup.find_all("a"):
        href = a.get("href")
        if not href:
            continue
        if href.startswith("#") or href.startswith("javascript:"):
            continue
        links.append(href)
    
    return list(set(links))


def categorize_links(links, base_url):
    """
    Sépare les liens internes et externes.
    """
    base_domain = urlparse(base_url).netloc
    
    internal = []
    external = []
    
    for link in links:
        parsed = urlparse(link)
        if parsed.netloc == "" or parsed.netloc == base_domain:
            internal.append(link)
        else:
            external.append(link)
    
    return internal, external


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 web_scraper.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"Fetching {url} ...")
    
    html = fetch_page(url)
    if html is None:
        sys.exit(1)
    
    links = extract_links(html, url)
    
    print(f"\n=== Links ({len(links)}) ===")
    for link in links:
        print(link)
    
    internal, external = categorize_links(links, url)
    
    print(f"\n=== Summary ===")
    print(f"Total: {len(links)}")
    print(f"Internal: {len(internal)}")
    print(f"External: {len(external)}")


if __name__ == "__main__":
    main()