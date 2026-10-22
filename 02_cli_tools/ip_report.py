import re
import sys
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
    text = "===IP Activity Report=========================\n"
    text += f"Total number of unique IPs: {len(count)}\n"
    text += "\n"
    for ip, nbre in sorted(count.items(), key=lambda x:x[1], reverse=True):
        text += f"IP {ip} -> {nbre} appearances\n"
    return text

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
    print("report is written to report_ip.txt")

if __name__ == "__main__":
    main()