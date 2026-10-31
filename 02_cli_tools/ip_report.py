import re
import sys
from ip_classifiers import classify
import json
from datetime import datetime
import csv
def extract_ip(filename):
    count ={}
    with open(filename, "r") as f:
        for line in f:
            IPs = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            for ip in IPs:
                if ip in count:
                    count[ip]+=1
                else:
                    count[ip]=1
    return count
 

def build_report(count):
    text = "===IP Activity Report==========\n"
    text += f"Total number of unique IPs: {len(count)}\n"
    text += "\n"
    
    for ip, nbre in sorted(count.items(), key=lambda x:x[1], reverse=True):
        label = "appearance" if nbre == 1 else "appearances"
        type_ip = classify(ip)
        text += f"IP {ip:<18} -> {nbre} {label:>12} ({type_ip})\n"
    return text

def build_json(count):
    data = {
        "total_unique_ips": len(count),
        "generated_at": datetime.now().isoformat(),
        "ips": []
    }
    for ip, nbre in sorted(count.items(), key=lambda x:x[1], reverse= True):
        data["ips"].append({
            "ip": ip,
            "count":nbre,
            "type": classify(ip)
        })
    return data

def build_csv(data):
    with open("report_ip.csv","w",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames =["ip", "count","type"])
        writer.writeheader()
        for entry in data["ips"]:
            writer.writerow(entry)
    return writer

def main():
    if len(sys.argv) < 2:
        print("Usage: python ip_report.py <logfile>")
        sys.exit(1)
    filename = sys.argv[1]
    extract = extract_ip(filename)
    report = build_report(extract)
    with open("report_ip.txt","w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    print("report is written to report_ip.txt\n")
    data = build_json(extract) 
    with open("report_ip.json","w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)     
    print("json report is written in report_ip.json\n")
    build_csv(data)
    print("CSV report is written in report_ip.csv")

if __name__ == "__main__":
    main()