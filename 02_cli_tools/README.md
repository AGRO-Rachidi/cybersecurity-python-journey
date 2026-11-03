# Week 2: CLI tools

My first real scripts, run from the terminal. `week2.ipynb` is the draft where I first wrote `ip_report` as notebook cells, before I moved it into a `.py` file.

Files in this folder:
- `ip_report.py`: the main tool
- `ip_classifiers.py`: module imported by `ip_report.py`
- `is_valid_ip.py`: my first test with `ipaddress`
- `fake-access.log`, `logs_fictifs.log`: fake logs to test with (I made them myself, they're not real logs)

---

## ip_report.py

### What it does

Reads a log file, finds every IPv4 address in it, counts how many times each one appears and sorts them, most frequent first. Each IP gets a type (private, public...). The report is printed and saved in 3 formats: `report_ip.txt`, `report_ip.json`, `report_ip.csv`.

### Usage

```bash
cd 02_cli_tools
python3 ip_report.py fake-access.log
```

### Example output

```
===IP Activity Report==========
Total number of unique IPs: 3

IP 10.0.0.5           -> 3  appearances (private)
IP 10.0.0.6           -> 2  appearances (private)
IP 203.0.113.7        -> 1   appearance (private)

report is written to report_ip.txt

json report is written in report_ip.json

CSV report is written in report_ip.csv
```

The JSON looks like this:

```json
{
  "total_unique_ips": 3,
  "generated_at": "2026-11-03T18:05:11.972668",
  "ips": [
    {
      "ip": "10.0.0.5",
      "count": 3,
      "type": "private"
    },
    ...
```

If the file doesn't exist:

```
$ python3 ip_report.py nope.log
Error: file 'nope.log' not found.
Usage: python3 ip_report.py <logfile>
```

### How it works

- `extract_ip()` reads the file line by line, uses `re.findall` to find IPs and counts them in a dict `{ip: count}`.
- `build_report()` sorts the dict by count and builds the text. `build_json()` and `build_csv()` do the same thing for the other formats.
- every IP goes through `classify()` from `ip_classifiers.py`.
- `main()` checks `sys.argv`, catches `FileNotFoundError` and `PermissionError`, and stops if no IP was found so it doesn't write empty reports.

### Limitations / next steps

- the regex still matches things like `999.999.999.999`. `classify()` marks them "invalid", but they still get counted.
- the reports are written in the current folder, with fixed names. Running it twice overwrites the old report.
- 203.0.113.x and 198.51.100.x show as "private". This surprised me. They are documentation ranges (TEST-NET), and Python's `ipaddress` puts them in `is_private`. So my fake "attacker" IPs are not really public. For a real log I'd need a better check.
- IPv4 only for the extraction.
- next: an option to choose the output file, and only count lines with FAILED.

---

## ip_classifiers.py

### What it does

One function, `classify(text)`, that returns `loopback`, `private`, `public`, `other` (multicast, reserved...) or `invalid`.

### Usage

As a module (that's how `ip_report.py` uses it):

```python
from ip_classifiers import classify
classify("8.8.8.8")   # 'public'
```

Or run it directly to see the test examples:

```bash
python3 ip_classifiers.py
```

### Example output

```
10.0.0.5             ->    private
999.999.999.999      ->    invalid
192.168.1.1          ->    private
not_an_ip            ->    invalid
1.2.3                ->    invalid
8.8.8.8              ->     public
127.0.0.1            ->   loopback
224.0.0.1            ->      other
::1                  ->   loopback
```

### How it works

`ipaddress.ip_address()` turns the text into an IP object. If it can't, it raises `ValueError` and I return "invalid". Then I test the properties in order: loopback, private, multicast/reserved, global. Order matters: 127.0.0.1 is loopback but it's also private, so loopback has to come first.

### Limitations / next steps

- the file name is plural but there is only one function. I'll rename it to `ip_classifier.py` at some point.
- see the TEST-NET note above.

---

## is_valid_ip.py

My first small script with `ipaddress`, before I wrote the classifier. It just prints `True` or `False` for a few test values. I keep it because it shows the step between the regex check from week 1 and `classify()`.

```bash
python3 is_valid_ip.py
```
