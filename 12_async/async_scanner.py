import sys
import asyncio
import time


DEFAULT_START = 20
DEFAULT_END = 1000


async def scan_port(host, port, timeout=1):
    """
    Teste si un port est ouvert.
    Retourne (port, status) où status est "OPEN", "CLOSED" ou "FILTERED".
    """
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return port, "OPEN"
    except ConnectionRefusedError:
        return port, "CLOSED"
    except asyncio.TimeoutError:
        return port, "FILTERED"
    except OSError:
        return port, "CLOSED"


async def scan_ports(host, ports):
    """
    Scanne tous les ports en parallèle.
    Retourne la liste des résultats (port, status).
    """
    tasks = []
    for port in ports:
        tasks.append(scan_port(host, port))
    
    results = await asyncio.gather(*tasks)
    return results


def parse_ports(port_args):
    """
    Parse les arguments ports.
    Si "20-100" → range(20, 101)
    Si ["22", "80", "443"] → [22, 80, 443]
    Si vide → range(DEFAULT_START, DEFAULT_END + 1)
    """
    if not port_args:
        return list(range(DEFAULT_START, DEFAULT_END + 1))
    
    if len(port_args) == 1 and "-" in port_args[0]:
        start, end = port_args[0].split("-")
        return list(range(int(start), int(end) + 1))
    
    return [int(p) for p in port_args]


def display_results(results):
    """
    Affiche les résultats triés.
    Retourne les compteurs (open, closed, filtered).
    """
    open_count = 0
    closed_count = 0
    filtered_count = 0
    
    for port, status in sorted(results):
        print(f"[{status:<8}] Port {port}")
        if status == "OPEN":
            open_count += 1
        elif status == "CLOSED":
            closed_count += 1
        else:
            filtered_count += 1
    
    return open_count, closed_count, filtered_count


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 async_scanner.py <host> [ports...]")
        print("  Examples:")
        print("    python3 async_scanner.py 127.0.0.1")
        print("    python3 async_scanner.py 127.0.0.1 22 80 443")
        print("    python3 async_scanner.py 127.0.0.1 20-1000")
        sys.exit(1)
    
    host = sys.argv[1]
    port_args = sys.argv[2:]
    
    ports = parse_ports(port_args)
    
    print(f"Scanning {host} ({len(ports)} ports) ...\n")
    
    start_time = time.time()
    results = asyncio.run(scan_ports(host, ports))
    elapsed = time.time() - start_time
    
    open_count, closed_count, filtered_count = display_results(results)
    
    print(f"\nSummary: {open_count} open, {closed_count} closed, {filtered_count} filtered")
    print(f"Time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()