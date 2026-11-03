# Ce module sait vérifier si un texte correspond à une adresse IP.
import ipaddress


def is_valid_ip(text):
    try:
        # Python vérifie si le texte est une adresse IPv4 ou IPv6 correcte.
        ipaddress.ip_address(text)
        return True
    except ValueError:
        # Si Python ne reconnaît pas l'adresse, elle n'est pas valide.
        return False


# Quelques exemples pour voir ce que la fonction répond.
print(is_valid_ip("10.0.0.5"))
print(is_valid_ip("999.999.999.999"))
print(is_valid_ip("1.2.3"))
print(is_valid_ip("192.168.1.1"))
print(is_valid_ip("not_an_ip"))
print(is_valid_ip("::1"))