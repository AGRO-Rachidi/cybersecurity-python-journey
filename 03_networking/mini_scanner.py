# socket permet de tester une connexion réseau.
import socket


def is_port_open(host, port, timeout=1):
    # On prépare une connexion TCP qui se ferme automatiquement après le test.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # On évite d'attendre trop longtemps si le port ne répond pas.
        sock.settimeout(timeout)
        # connect_ex renvoie 0 si la connexion au port a réussi.
        result = sock.connect_ex((host, port))
        return result == 0


def scan_ports(host, ports):
    # Cette liste gardera les ports qui répondent.
    open_ports = []
    # On teste les ports de la liste un par un.
    for port in ports:
        if is_port_open(host, port):
            # Le port répond : on l'affiche et on l'ajoute aux résultats.
            print(f"{port:<6} -> OPEN")
            open_ports.append(port)
        else:
            # La connexion n'a pas abouti : on affiche que le port est fermé.
            print(f"{port:<6} -> CLOSED")
    return open_ports
    
    
if __name__ == "__main__":
    # Ici, le test est lancé sur cette machine uniquement.
    host = "127.0.0.1"
    # Quelques ports sont choisis pour l'exemple.
    ports = [22, 80, 443, 3306, 8080]
    print(f"Scanning {host} ...")
    # On lance le test et on récupère les ports qui ont répondu.
    open_ports = scan_ports(host, ports)
    # On affiche combien de ports ont été trouvés ouverts.
    print(f"\n{len(open_ports)} open ports found on {host}")