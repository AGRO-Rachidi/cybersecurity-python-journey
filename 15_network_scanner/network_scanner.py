"""
network_scanner.py — Scanner de réseau local

Découvre les hôtes actifs sur un subnet en combinant :
  1. TCP scan sur ports configurables (défaut: 22, 80, 443, 8080)
  2. Ping ICMP en fallback (désactivable avec --no-ping)

Usage:
    python3 network_scanner.py 192.168.1.0/24
    python3 network_scanner.py 192.168.1.0/24 --no-ping
    python3 network_scanner.py 192.168.1.0/24 --ports 22,80,443
    python3 network_scanner.py 192.168.1.0/24 --timeout 2
    python3 network_scanner.py 192.168.1.0/24 --quiet
    python3 network_scanner.py --help

AVERTISSEMENT LÉGAL:
    Scanner uniquement votre propre réseau local (celui que vous possédez
    ou sur lequel vous avez une autorisation écrite). Scanner un réseau
    qui n'est pas le vôtre est illégal dans la plupart des juridictions.
"""

import sys
import subprocess
import asyncio
import time
import ipaddress


# Ports courants à tester par défaut
DEFAULT_PORTS = [22, 80, 443, 8080]
DEFAULT_TIMEOUT = 0.5


def print_help():
    """Affiche l'aide complète."""
    print("""Usage: python3 network_scanner.py <network> [options]

Arguments:
    <network>              Subnet à scanner (ex: 192.168.1.0/24)

Options:
    --no-ping              Désactive le ping (TCP only, plus rapide)
    --ports PORT1,PORT2    Ports TCP à tester (défaut: 22,80,443,8080)
    --timeout SECONDS      Timeout par port (défaut: 0.5)
    --quiet                Pas de confirmation avant le scan
    --help                 Affiche cette aide

Exemples:
    python3 network_scanner.py 192.168.1.0/24
    python3 network_scanner.py 192.168.1.0/24 --no-ping
    python3 network_scanner.py 192.168.1.0/24 --ports 22,80,443
    python3 network_scanner.py 192.168.1.0/24 --timeout 2 --quiet

AVERTISSEMENT:
    Scanner uniquement votre propre réseau local.
    Scanner un réseau sans autorisation est illégal.
""")


def parse_args():
    """
    Parse les arguments de la ligne de commande.
    
    Returns:
        dict avec les clés: network_str, use_ping, ports, timeout, quiet
        ou None si --help
    """
    args = {
        "network_str": None,
        "use_ping": True,
        "ports": DEFAULT_PORTS,
        "timeout": DEFAULT_TIMEOUT,
        "quiet": False,
    }
    
    # --help ?
    if "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        return None
    
    # Le premier argument non-flag = le subnet
    if len(sys.argv) < 2:
        print("Error: missing network argument")
        print("Usage: python3 network_scanner.py <network> [options]")
        print("Try: python3 network_scanner.py --help")
        sys.exit(1)
    
    args["network_str"] = sys.argv[1]
    
    # --no-ping
    if "--no-ping" in sys.argv:
        args["use_ping"] = False
    
    # --quiet
    if "--quiet" in sys.argv:
        args["quiet"] = True
    
    # --ports 22,80,443
    if "--ports" in sys.argv:
        idx = sys.argv.index("--ports")
        if idx + 1 < len(sys.argv):
            try:
                ports_str = sys.argv[idx + 1]
                args["ports"] = [int(p) for p in ports_str.split(",")]
            except ValueError:
                print(f"Error: invalid ports '{sys.argv[idx + 1]}'")
                sys.exit(1)
        else:
            print("Error: --ports requires a value (ex: --ports 22,80,443)")
            sys.exit(1)
    
    # --timeout 2
    if "--timeout" in sys.argv:
        idx = sys.argv.index("--timeout")
        if idx + 1 < len(sys.argv):
            try:
                args["timeout"] = float(sys.argv[idx + 1])
            except ValueError:
                print(f"Error: invalid timeout '{sys.argv[idx + 1]}'")
                sys.exit(1)
        else:
            print("Error: --timeout requires a value (ex: --timeout 2)")
            sys.exit(1)
    
    return args


async def is_port_open(host, port, timeout):
    """Teste si un port TCP est ouvert (asynchrone)."""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False


def ping_host(host, timeout=1):
    """Ping un hôte via subprocess."""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), str(host)],
            capture_output=True,
            text=True,
            timeout=timeout + 1
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


async def scan_host(host, ports, use_ping, timeout):
    """
    Teste si un hôte est actif.
    TCP d'abord, ping en fallback si aucun port ne répond.
    """
    host_str = str(host)
    
    # TCP scan en parallèle
    tasks = [is_port_open(host_str, port, timeout) for port in ports]
    results = await asyncio.gather(*tasks)
    
    if any(results):
        return host_str, True, "tcp"
    
    # Ping fallback
    if use_ping:
        loop = asyncio.get_event_loop()
        ping_result = await loop.run_in_executor(None, ping_host, host_str)
        if ping_result:
            return host_str, True, "ping"
    
    return host_str, False, None


async def scan_network(network, ports, use_ping, timeout):
    """Scanne tous les hôtes en parallèle."""
    tasks = [scan_host(host, ports, use_ping, timeout) for host in network.hosts()]
    results = await asyncio.gather(*tasks)
    return results


def display_results(results):
    """Affiche les résultats."""
    active = [(host, method) for host, is_active, method in results if is_active]
    inactive_count = len(results) - len(active)
    
    print("\n=== Active Hosts ===")
    if active:
        for host, method in active:
            print(f"[UP]   {host}  (via {method})")
    else:
        print("(no active hosts found)")
    
    print(f"\n=== Summary ===")
    print(f"Total scanned: {len(results)}")
    print(f"Active:        {len(active)}")
    print(f"Inactive:      {inactive_count}")
    
    return len(active)


def main():
    # 1. Parser les arguments
    args = parse_args()
    if args is None:
        sys.exit(0)  # --help affiché, on sort proprement
    
    network_str = args["network_str"]
    
    # 2. Valider le subnet
    try:
        network = ipaddress.ip_network(network_str, strict=False)
    except ValueError as e:
        print(f"Error: invalid network '{network_str}': {e}")
        sys.exit(1)
    
    # 3. Afficher la configuration
    print(f"=== Network Scanner ===")
    print(f"Target: {network}")
    print(f"Hosts to scan: {network.num_addresses - 2}")
    print(f"Ports tested: {args['ports']}")
    print(f"Timeout: {args['timeout']}s")
    print(f"Ping fallback: {'enabled' if args['use_ping'] else 'disabled'}")
    print(f"\n⚠️  Vous devez posséder ce réseau ou avoir une autorisation écrite.")
    
    # 4. Confirmation (sauf si --quiet)
    if not args["quiet"]:
        answer = input("\nContinue? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            sys.exit(0)
    
    # 5. Lancer le scan
    print(f"\nScanning {network} ...\n")
    
    start_time = time.time()
    results = asyncio.run(scan_network(network, args["ports"], args["use_ping"], args["timeout"]))
    elapsed = time.time() - start_time
    
    # 6. Afficher les résultats
    active_count = display_results(results)
    
    print(f"Time: {elapsed:.2f}s")
    
    if active_count > 0:
        print(f"\n✅ {active_count} active host(s) found.")
    else:
        print(f"\n❌ No active hosts found.")


if __name__ == "__main__":
    main()