import re
import sys


def parse_syslog(line):
    """Parse la structure syslog de base."""
    pattern = (
        r"(?P<date>\d{4}-\d{2}-\d{2})\s+"
        r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
        r"(?P<level>\w+)\s+"
        r"(?P<process>\w+)\[(?P<pid>\d+)\]:\s+"
        r"(?P<message>.+)"
    )
    m = re.match(pattern, line)
    if m:
        return m.groupdict()
    return None


def parse_kernel(line):
    """Parse la structure kernel/UFW de base."""
    pattern = (
        r"(?P<date>\d{4}-\d{2}-\d{2})\s+"
        r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
        r"(?P<level>\w+)\s+"
        r"(?P<process>kernel):\s+"
        r"(?P<message>.+)"
    )
    m = re.match(pattern, line)
    if m:
        return m.groupdict()
    return None


def extract_ssh_fields(message):
    """Extrait user, ip, port d'un message SSH. Retourne {} si pas SSH."""
    # Cas : Failed password for [invalid user] USER from IP port PORT
    m = re.search(
        r"(?:invalid user\s+)?(?P<user>\w+)\s+from\s+"
        r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+"
        r"port\s+(?P<port>\d+)",
        message,
    )
    if m:
        return m.groupdict()
    return {}


def extract_ufw_fields(message):
    """Extrait src, dst, proto, dpt d'un message UFW. Retourne {} si pas UFW."""
    # Cas : [UFW BLOCK] IN=eth0 OUT= MAC=... SRC=X.X.X.X DST=Y.Y.Y.Y PROTO=TCP DPT=22
    if "[UFW" not in message:
        return {}
    fields = {}
    m = re.search(r"SRC=(?P<src>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", message)
    if m:
        fields["src_ip"] = m.group("src")
    m = re.search(r"DST=(?P<dst>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", message)
    if m:
        fields["dst_ip"] = m.group("dst")
    m = re.search(r"PROTO=(?P<proto>\w+)", message)
    if m:
        fields["proto"] = m.group("proto")
    m = re.search(r"DPT=(?P<dpt>\d+)", message)
    if m:
        fields["dst_port"] = m.group("dpt")
    return fields


def parse_log_line(line):
    """Essaie chaque parser. Enrichit avec les champs extraits du message."""
    result = parse_syslog(line)
    if result:
        result.update(extract_ssh_fields(result["message"]))
        return result

    result = parse_kernel(line)
    if result:
        result.update(extract_ufw_fields(result["message"]))
        return result

    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 log_parser.py <logfile>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r") as f:
            parsed = 0
            failed = 0
            for line in f:
                line = line.strip()
                if not line:
                    continue

                result = parse_log_line(line)

                if result:
                    parsed += 1
                    # Affichage : champs principaux + champs extraits
                    base = f"[{result['level']}] {result['date']} {result['time']} {result['process']}"
                    if "user" in result:
                        base += f" user={result['user']} ip={result['ip']} port={result['port']}"
                    if "src_ip" in result:
                        base += f" src={result['src_ip']} dst={result['dst_ip']} proto={result['proto']} dpt={result['dst_port']}"
                    print(base)
                else:
                    failed += 1
                    print(f"UNPARSED: {line}")

        print(f"\nSummary: {parsed} parsed, {failed} failed")

    except FileNotFoundError:
        print(f"Error: file '{filename}' not found")
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied for '{filename}'")
        sys.exit(1)


if __name__ == "__main__":
    main()