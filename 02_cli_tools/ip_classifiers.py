# Ce module sert à donner une catégorie à une adresse IP.
import ipaddress


def classify(text):
    try:
        # Python transforme le texte en adresse IP pour pouvoir la tester.
        ip = ipaddress.ip_address(text)
    except ValueError:
        # Si ce n'est pas une adresse correcte, on renvoie "invalid".
        return "invalid"

    # On regarde les catégories l'une après l'autre.
    if ip.is_loopback:
        return "loopback"
    if ip.is_private:
        return "private"
    if ip.is_multicast or ip.is_reserved:
        return "other"
    if ip.is_global:
        return "public"
    return "other"


if __name__ == "__main__":
    # Ces exemples montrent le résultat pour quelques adresses.
    print(classify("127.0.0.1"))         
    print(classify("192.168.1.10"))      
    print(classify("8.8.8.8"))           
    print(classify("999.999.999.999"))   
    print(classify("224.0.0.1"))         
    print(classify("::1"))               

    # Cette liste mélange des adresses IP et des textes incorrects.
    candidates = [
    "10.0.0.5",
    "999.999.999.999",
    "192.168.1.1",
    "not_an_ip",
    "1.2.3",
    "8.8.8.8",
    "127.0.0.1",
    "224.0.0.1",
    "::1"
    ]

    # On affiche chaque adresse avec la catégorie trouvée.
    for ip in candidates:
        check = classify(ip)
        print(f"{ip:<20} -> {check:>10}")  