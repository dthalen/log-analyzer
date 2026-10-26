import re
from collections import Counter

ip_list = []

with open ("auth.log") as f:
    for line in f:
        if "failed password" in line.lower():
            ip = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            ip_list.append(ip.group())
            print(ip.group())
        elif "accepted password" in line.lower():
            ip = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            ip_list.append(ip.group())
            print(ip.group())

result = Counter(ip_list)
print(result)