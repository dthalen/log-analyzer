import re

with open ("auth.log") as f:
    for line in f:
        if "failed password" in line.lower():
            ip = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            print(ip.group())
        elif "accepted password" in line.lower():
            ip = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            print(ip.group())
            