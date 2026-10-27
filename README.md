# log-analyzer

A small Python tool that scans Linux `auth.log` files and flags suspicious SSH
activity — brute-force attacks, successful breaches, and logins at unusual hours.

I built this while learning security through Hack The Box. After analysing auth
logs by hand on a few boxes, I wanted to automate the boring part: spotting which
IPs are hammering the server, whether any of them got in, and whether anyone
logged in when they shouldn't have.

## What it detects

The tool reads an SSH authentication log and produces a short report grouped into
three sections:

- **Breaches** — an IP that failed many times and then successfully logged in
  (the most serious case: a brute force that worked).
- **Brute-force attempts** — an IP with a high number of failed logins.
- **Odd-hour logins** — a *successful* login during the night (00:00–06:00),
  with the IP and the date, since a real login at 4am is worth a second look even
  if it isn't a brute force.

## Example output

```
--- BREACHES ---
[CRITICAL] 141.98.10.60 had 25 failed logins and successfully logged in! - possible brute force successful!

--- BRUTE FORCE ATTEMPTS ---
[WARNING] 193.169.255.12 had 62 failed logins! - possible attempted brute force!
[WARNING] 92.63.197.55 had 70 failed logins! - possible attempted brute force!

--- ODD-HOUR LOGINS ---
[WARNING] successful login from 86.22.30.4 at 04:00 on Oct 24 - unusual hour
[WARNING] successful login from 86.22.30.4 at 04:00 on Oct 25 - unusual hour
```

## How to run it

```
python analyzer.py
```

By default it reads a file called `auth.log` in the same folder. On a real
Linux system, SSH auth events are logged to `/var/log/auth.log`.

## How it works

The script reads the log line by line and, for each login line:

- extracts the source IP with a regular expression
  (`\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}`)
- separates **failed** logins from **successful** ones
- for successful logins, also reads the date and hour from the start of the line

It then counts attempts per IP with `collections.Counter`, builds a list of
alerts for each category, and prints them grouped into sections. A line like:

```
Oct 24 04:21:30 srv-web01 sshd[5532]: Accepted password for deploy from 86.22.30.4 port 57153 ssh2
```

gives the date (`Oct 24`), the hour (`04`), and the IP (`86.22.30.4`).

## Known limitations

- **Threshold-based detection misses "low and slow" attacks.** An attacker making
  only a handful of attempts stays under the alert threshold. A real system would
  also look at timing and patterns, not just volume.
- **Counts are merged across days.** The brute-force counts don't separate attempts
  by date, so an IP that attacked on two days is counted as one total.
- **Basic IP regex.** It matches the shape of an IPv4 address but doesn't validate
  the ranges (it would accept `999.999.999.999`) and doesn't handle IPv6.
- Built for standard OpenSSH `auth.log` format; other formats aren't parsed yet.

## Possible next steps

- Read the log path and thresholds from command-line arguments
- Separate counts per day
- Flag odd-hour logins from external IPs more strongly than internal ones
- Validate IPs properly / support IPv6

## Why I built it

I'm a cybersecurity student aiming to work in security engineering. This project
mirrors the kind of task a threat-detection team does — turning raw logs into
actionable alerts — and it's where I'm practising Python, regular expressions,
and log analysis.