import sys
import re
from collections import Counter
from datetime import datetime


# Formats de timestamp supportés
TIMESTAMP_FORMATS = [
    "%Y-%m-%d %H:%M:%S",        # 2026-10-22 18:10:01
    "%Y-%m-%dT%H:%M:%S",        # 2026-10-22T18:10:01 (ISO)
    "%d/%b/%Y:%H:%M:%S",        # 22/Oct/2026:18:10:01 (Apache)
]


def read_log(filename):
    """Lit le fichier, retourne la liste des lignes."""
    with open(filename, "r", encoding="utf-8") as f:
        lines = []
        for line in f:
            line.strip()
            if line:
                lines.append(line)
    return lines

def parse_timestamp(ts_str):
    """
    Essaie de parser un timestamp avec plusieurs formats.
    Retourne un datetime ou None.
    """
    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(ts_str, fmt)
        except ValueError:
            continue
    return None

def extract_timestamps(lines):
    """
    Extrait tous les timestamps des lignes.
    Retourne une liste de datetime.
    """
    timestamps = []
    for line in lines:
        match = re.search(r"(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})", line)
        if match:
            ts_str = match.group(1)
            ts = parse_timestamp(ts_str)   # ← string → datetime
            if ts:
                timestamps.append(ts)
    return timestamps
    
def analyze_by_hour(timestamps):
    """Compte les événements par heure."""
    hours = [t.hour for t in timestamps]    
    return Counter(hours)


def analyze_by_weekday(timestamps):
    """Compte les événements par jour de la semaine."""
    weekdays = [t.weekday() for t in timestamps]   # 0=lundi, 6=dimanche
    return Counter(weekdays)


def analyze_night_activity(timestamps):
    """Compte les événements entre 22h et 6h."""
    night_count = sum(1 for t in timestamps if t.hour >= 22 or t.hour < 6)
    total = len(timestamps)
    percentage = (night_count / total * 100) if total > 0 else 0
    return night_count, percentage


def analyze_off_hours(timestamps):
    """Compte les événements hors heures ouvrables (< 8h ou > 18h)."""
    off_count = sum(1 for t in timestamps if t.hour < 8 or t.hour > 18)
    total = len(timestamps)
    percentage = (off_count / total * 100) if total > 0 else 0
    return off_count, percentage

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def display_bar_chart(title, counter, total, use_weekdays=False):
    print(f"\n=== {title} ===")
    for key in sorted(counter.keys()):
        count = counter[key]
        pct = (count / total * 100) if total > 0 else 0
        bar = "█" * int(pct // 2)
        
        if use_weekdays:
            label = WEEKDAYS[key]
        else:
            label = f"{key:02d}h"
        
        print(f"{label:<12} {count:5d} ({pct:5.1f}%) {bar}")
        


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 time_analyzer.py <logfile>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        lines = read_log(filename)
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found")
        sys.exit(1)
    
    timestamps = extract_timestamps(lines)
    
    if not timestamps:
        print(f"No timestamps found in '{filename}'")
        sys.exit(0)
    
    print(f"=== Time Analysis: {filename} ===")
    print(f"Total timestamps: {len(timestamps)}")
    print(f"Range: {min(timestamps).strftime('%Y-%m-%d %H:%M:%S')} → {max(timestamps).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Analyse par heure
    by_hour = analyze_by_hour(timestamps)
    display_bar_chart("Activity by Hour", by_hour, len(timestamps))
    
    # Analyse par jour
    by_weekday = analyze_by_weekday(timestamps)
    display_bar_chart("Activity by Day of Week", by_weekday, len(timestamps), use_weekdays=True)
    
    # Activité nocturne
    night_count, night_pct = analyze_night_activity(timestamps)
    print(f"\n=== Night Activity (22h-6h) ===")
    print(f"{night_count} events ({night_pct:.1f}%)")
    
    # Hors heures ouvrables
    off_count, off_pct = analyze_off_hours(timestamps)
    print(f"\n=== Off-Hours Activity (< 8h or > 18h) ===")
    print(f"{off_count} events ({off_pct:.1f}%)")
    if off_pct > 50:
        print("⚠️ HIGH off-hours activity")


if __name__ == "__main__":
    main()