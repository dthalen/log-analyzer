import re
from collections import Counter

ip_list = []
ip_list_accepted = []
ip_list_denied = []

with open ("auth.log") as f:
    for line in f:
        if "failed password" in line.lower():
            ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            ip_list.append(ip.group())
            ip_list_denied.append(ip.group())
            #print(ip.group())
        elif "accepted password" in line.lower():
            ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            ip_list.append(ip.group())
            ip_list_accepted.append(ip.group())
            parts = line.split()
            hour = int(parts[2].split(":")[0])
            if hour < 6:
                print(f"[WARNING⚠️ ] successful login from {ip.group()} at {hour:02d}:00 - unusual hour")  
             

result_all = Counter(ip_list)
result_accepted = Counter(ip_list_accepted)
result_denied = Counter(ip_list_denied)

for ip, count in result_denied.items():
    if count >= 10:
        if ip in result_accepted:            
            print(f"[CRITICAL🚨 ] {ip} had {count} failed logins and successfully logged in! - possible attempted brute force successful!")
        else:
            print(f"[WARNING⚠️ ] {ip} had {count} failed logins! - possible attempted brute force!")


# print(f"Combined: {result_all}")
# print(f"Accepted: {result_accepted}")
# print(f"Denied: {result_denied}")