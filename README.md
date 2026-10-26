# log-analyzer

A small Python tool that scans Linux `auth.log` files and flags SSH brute-force
attacks — including attempts that eventually succeeded.

I built this while learning security through Hack The Box. After analysing auth
logs by hand on a few boxes, I wanted to automate the boring part: spotting which
IPs are hammering the server and whether any of them got in.

## What it does

- Reads an SSH authentication log line by line
- Pulls the source IP out of each login line with a regular expression
- Separates **failed** logins from **successful** ones
- Counts attempts per IP
- Raises alerts for:
  - IPs with a high number of failed logins (likely brute force)
  - IPs that failed many times **and then succeeded** (a likely breach — the
    most important case)

## Example output

```
[ALERT]   45.142.120.33 had 40 failed logins — possible brute force
[WARNING] 193.169.255.12 had 18 failed logins and then logged in successfully — possible successful brute force
```

## How to run it

```
python analyzer.py
```

By default it reads a file called `auth.log` in the same folder. On a real
Linux system, SSH auth events are logged to `/var/log/auth.log`.

## How it works

The script keeps three lists of IPs — all attempts, successful logins, and
failed logins — and uses `collections.Counter` to tally them. A login line like:

```
Oct 26 14:33:01 server sshd[1123]: Failed password for root from 45.142.120.33 port 4022 ssh2
```

is matched for "Failed password" / "Accepted password", and the IP is extracted
with the pattern `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}`.

## Known limitations

- **Threshold-based detection misses "low and slow" attacks.** An attacker making
  only a handful of attempts stays under the alert threshold. A real detection
  system would also look at timing and patterns, not just volume.
- **Basic IP regex.** The pattern matches the shape of an IPv4 address but
  doesn't validate the ranges (e.g. it would accept `999.999.999.999`), and it
  doesn't handle IPv6.
- Built for standard OpenSSH `auth.log` format; other log formats aren't parsed yet.

## Possible next steps

- Flag logins at unusual hours
- Validate IPs properly / support IPv6
- Read the log path from a command-line argument
- Output a summary report instead of just printing alerts

## Why I built it

I'm a cybersecurity student aiming to work in security engineering. This project
mirrors the kind of task a threat-detection team does — turning raw logs into
actionable alerts — and it's where I'm practising Python, regular expressions,
and log analysis.