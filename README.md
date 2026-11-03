# cybersecurity-python-journey

My notes and small scripts from learning Python, with a SOC analyst job as the goal.

## Why this repo

I started Python from zero a couple of weeks ago. I want to work in a SOC, and almost every job post asks for some scripting, so I'm learning it with security examples instead of the usual "hello world" stuff. I push everything here, mistakes included, so I can look back and see where I started.

## Progress

**Week 1: fundamentals** ([01_fundamentals](01_fundamentals/))

One big notebook, `week1.ipynb`. Variables, lists, tuples, dicts, if/elif/else, for and while loops, functions, string methods, reading files, and my first regex. The exercises are all about ports, IPs and fake login logs. It ends with a small script that counts failed logins per IP.

**Week 2: command line tools** ([02_cli_tools](02_cli_tools/), [03_networking](03_networking/))

This is where I started writing real `.py` files instead of notebook cells:
- `sys.argv` to pass a file name from the terminal
- the `ipaddress` module to check and classify IPs
- writing reports in TXT, JSON and CSV
- `try/except` so the script doesn't crash on a missing file
- `socket` for a tiny port scanner (localhost only)

## Skills acquired

Week 1
- basic types and conversions
- lists, tuples, dicts and when to use which one
- loops with `break` / `continue`
- writing functions that `return` something instead of just printing
- `strip()`, `split()`, slicing
- `with open(...)` to read and write files
- `re.findall` and `re.search`, capture groups

Week 2
- splitting a script into functions with a `main()`
- `if __name__ == "__main__":` and importing my own module
- reading arguments with `sys.argv`, exiting with `sys.exit()`
- `ipaddress.ip_address()` and properties like `is_private`, `is_loopback`
- `json.dump` and `csv.DictWriter`
- catching `FileNotFoundError` and `PermissionError`
- TCP sockets: `settimeout()` and `connect_ex()`

## Tools built

| Tool | Folder | What it does |
|------|--------|--------------|
| `ip_report.py` | [02_cli_tools](02_cli_tools/) | counts the IPs in a log file and writes a report (txt, json, csv) |
| `ip_classifiers.py` | [02_cli_tools](02_cli_tools/) | says if an IP is loopback, private, public, other or invalid |
| `is_valid_ip.py` | [02_cli_tools](02_cli_tools/) | first try with `ipaddress`: valid IP or not |
| `mini_scanner.py` | [03_networking](03_networking/) | checks a few TCP ports on 127.0.0.1 |

## Roadmap

- [x] Python basics (week 1)
- [x] regex basics
- [x] CLI script with `sys.argv`
- [x] IP validation with `ipaddress`
- [x] JSON / CSV output
- [x] error handling with `try/except`
- [x] small TCP scanner on localhost
- [ ] files and strings in more depth (bigger, messier logs)
- [ ] `subprocess`
- [ ] `hashlib` (hashing files, checking hashes)
- [ ] `scapy`
- [ ] `paramiko`
- [ ] `impacket`

## Environment

- Python 3.13
- Linux
- VS Code + Jupyter extension
- no external packages so far, only the standard library

---

Slow progress is still progress. I write every script myself, then I go back and fix it.
