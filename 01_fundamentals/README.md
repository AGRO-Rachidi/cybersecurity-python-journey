# Week 1: Python fundamentals

Everything is in `week1.ipynb`. Each exercise has the instructions in a markdown cell and my answer under it. I left my wrong attempts and comments in, on purpose.

`suspicious.txt` is the output of the brute-force exercise (IPs with 3 or more failed logins).

Note: the notebook reads `fake-access.log` from the same folder. That file is in `02_cli_tools/`, so copy it here if you want to run the cells again.

## What I covered

- variables and types, `int()`, `str()`, `type()`
- lists: indexing, `[-1]`, `append`, `remove`, `len`, `in`
- tuples: you can't change them, and unpacking
- dicts: access by key, `.get()`, `.items()`
- `if / elif / else`, `and` / `or`, checking if a port is in a range
- `for` and `while`, with `break` and `continue`
- functions: `is_insecure(port)`, `port_info(port)`, `scan_ports(ports)`
- strings: `strip()`, `split()`, `split("=")` to get the value after `ip=`
- reading a log file line by line with `with open(...)`
- regex with `re.findall` and `re.search`: IPs, dates, `user=...`, `port=...`
- last exercise: read the log, count the IPs in a dict, write a report

## What was hard

- `x = x.append(...)`: append changes the list in place and returns `None`, so I lost my list. Took me a while to understand why.
- calling `line.split()` and not saving the result anywhere.
- naming a variable `list`. It works, until you need the real `list()`.
- `sorted(d.items(), key=lambda x: x[1], reverse=True)`. I had to read it several times before I understood what `x[1]` was.
- `re.search` returns `None` when nothing matches, so `.group()` crashes. I need an `if` first.
- my IP regex `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}` accepts `999.999.999.999`. It only checks the shape. That's why I moved to `ipaddress` in week 2.

## What clicked

- dicts as counters (`if ip in count: count[ip] += 1`). I use this everywhere now.
- `with open(...)`: no need to think about closing the file.
- once I got the habit of writing small functions, the last exercise was a lot easier.
