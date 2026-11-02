import argparse
from detector import analyze_log

parser = argparse.ArgumentParser(description="Analyze an SSH auth.log for suspicious activity")
parser.add_argument("logfile", help="path to the auth.log file")
parser.add_argument("-t", "--threshold", type=int, default=10, help="failed login count to flag as brute force")
args = parser.parse_args()

breaches, brute_force, odd_hours, stats = analyze_log(args.logfile, args.threshold)

if breaches:
    print("--- BREACHES ---")
    for item in breaches:
        print(f"{item}\n")

if brute_force:
    print("--- BRUTE FORCE ATTEMPTS ---")
    for item in brute_force:
        print(f"{item}\n")

if odd_hours:
    print("--- ODD-HOUR LOGINS ---")
    for item in odd_hours:
        print(f"{item}\n")