import socket
def is_port_open(host, port, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        return result == 0

def scan_ports(host, ports):
    
    open_ports = []
    for port in ports:
        if is_port_open(host, port):
            print(f"{port:<6} -> OPEN")
            open_ports.append(port)
        else:
            print(f"{port:<6} -> CLOSED")
    return open_ports
    
    
if __name__ == "__main__":
    host = "127.0.0.1"
    ports = [22, 80, 443, 3306, 8080]
    print(f"Scanning {host} ...")
    open_ports = scan_ports(host, ports)
    print(f"\n{len(open_ports)} open ports found on {host}")