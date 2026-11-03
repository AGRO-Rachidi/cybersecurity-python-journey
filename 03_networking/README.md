# mini_scanner.py

A very small TCP port scanner. I wrote it to understand how a port scan works before I use real tools like nmap.

## Warning

It only scans `127.0.0.1` (my own machine) and that's on purpose. Scanning IPs or networks that you don't own, or that you don't have written permission to test, is illegal in a lot of countries. Use it on localhost or on your own lab VMs, nothing else.

## Usage

```bash
cd 03_networking
python3 mini_scanner.py
```

No arguments for now. The host and the ports are written in the code:

```python
host = "127.0.0.1"
ports = [22, 80, 443, 3306, 8080]
```

## Example output

The result depends on what's running on your machine. For example, with only SSH running:

```
Scanning 127.0.0.1 ...
22     -> OPEN
80     -> CLOSED
443    -> CLOSED
3306   -> CLOSED
8080   -> CLOSED

1 open ports found on 127.0.0.1
```

(yes, "1 open ports", I still need to fix the plural)

## How it works

- `socket.socket(AF_INET, SOCK_STREAM)` creates a TCP socket (IPv4). I use it with `with` so it gets closed after each port.
- `settimeout(1)`: if a port doesn't answer, it waits 1 second max instead of hanging.
- `connect_ex((host, port))` tries the connection and returns an error code instead of raising an exception. `0` means it connected, so the port is open.
- `scan_ports()` loops over the list, prints OPEN or CLOSED and returns the open ones.

It's a full TCP connect, so the service on the other side sees the connection. It's not a stealth scan like `nmap -sS`.

## Next steps

- read the ports from the command line with `sys.argv` (still localhost only)
- add `try/except` for socket errors
- try port ranges, and see how slow it gets with a 1s timeout
