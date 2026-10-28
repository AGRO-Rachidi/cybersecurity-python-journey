import ipaddress
def classify(text):
    try:
        ip = ipaddress.ip_address(text)
    except ValueError:
        return "invalid"
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
    print(classify("127.0.0.1"))         
    print(classify("192.168.1.10"))      
    print(classify("8.8.8.8"))           
    print(classify("999.999.999.999"))   
    print(classify("224.0.0.1"))         
    print(classify("::1"))               

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

    for ip in candidates:
        check = classify(ip)
        print(f"{ip:<20} -> {check:>10}")  