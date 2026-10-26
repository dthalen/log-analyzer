with open ("auth.log") as f:
    for line in f:
        if "failed password" in line.lower():
            print(line.strip())
        elif "accepted password" in line.lower():
            print(line.strip())
            