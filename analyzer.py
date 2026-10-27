import re
from collections import Counter

ip_list = []
ip_list_accepted = []
ip_list_denied = []

brute_force_alerts = []
breaches_alert = []
odd_hour_alert = []

with open ("auth.log") as f:
    for line in f:
        if "failed password" in line.lower():
            ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            ip_list.append(ip.group())
            ip_list_denied.append(ip.group())
            
        elif "accepted password" in line.lower():
            ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            ip_list.append(ip.group())
            ip_list_accepted.append(ip.group())
            parts = line.split()
            hour = int(parts[2].split(":")[0])
            if hour < 6:
                odd_hour_alert.append(f"[WARNING⚠️ ] successful login from {ip.group()} at {hour:02d}:00 - unusual hour")  
             

result_all = Counter(ip_list)
result_accepted = Counter(ip_list_accepted)
result_denied = Counter(ip_list_denied)

for ip, count in result_denied.items():
    if count >= 10:
        if ip in result_accepted:            
            breaches_alert.append(f"[CRITICAL🚨 ] {ip} had {count} failed logins and successfully logged in! - possible attempted brute force successful!")
        else:
            brute_force_alerts.append(f"[WARNING⚠️ ] {ip} had {count} failed logins! - possible attempted brute force!")


if breaches_alert:
    print("--- BREACHES ---")
    for item in breaches_alert:
        print(f"{item}\n")

if brute_force_alerts:
    print("--- BRUTE FORCE ATTEMPTS ---")
    for item in brute_force_alerts:
        print(f"{item}\n")

if odd_hour_alert:
    print("--- ODD-HOUR LOGINS ---")
    for item in odd_hour_alert:
        print(f"{item}\n")