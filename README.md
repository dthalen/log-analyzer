# log-analyzer

A Python tool that scans Linux `auth.log` files and flags suspicious SSH activity
— brute-force attacks, successful breaches, and logins at unusual hours. It has
two interfaces: a **command-line tool** and a **web dashboard**.

I built this while learning security through Hack The Box. After analysing auth
logs by hand on a few boxes, I wanted to automate the boring part: spotting which
IPs are hammering the server, whether any of them got in, and whether anyone
logged in when they shouldn't have.

## Web dashboard

Upload a log file and get a colour-coded breakdown: summary stats, the raw log
with failed/accepted logins highlighted and the detected alerts grouped by type.

![Dashboard screenshot](images/dashboard.png)

Run it with:

```
python app.py
```

Then open `http://localhost:5000` in your browser and upload a log file.

## What it detects

Both the CLI and the dashboard report three things:

- **Breaches** — an IP that failed many times and then successfully logged in
  (the most serious case: a brute force that worked).
- **Brute-force attempts** — an IP with a high number of failed logins.
- **Odd-hour logins** — a *successful* login during the night (00:00–06:00),
  with the IP and the date, since a real login at 4am is worth a second look even
  if it isn't a brute force.

## Command-line tool

```
python analyzer.py <path-to-log-file>

# examples
python analyzer.py auth.log
python analyzer.py /var/log/auth.log
python analyzer.py auth.log -t 5      # set the brute-force threshold (default 10)
```

Use `-t` / `--threshold` to change how many failed logins count as a brute-force
attempt. On a real Linux system, SSH auth events are logged to `/var/log/auth.log`.

### Example CLI output

```
--- BREACHES ---
[CRITICAL] 141.98.10.60 had 25 failed logins and successfully logged in!

--- BRUTE FORCE ATTEMPTS ---
[WARNING] 193.169.255.12 had 62 failed logins!
[WARNING] 92.63.197.55 had 70 failed logins!

--- ODD-HOUR LOGINS ---
[WARNING] successful login from 86.22.30.4 at 04:00 on Oct 24 - unusual hour
```

## How it works

The detection logic lives in `detector.py` as a reusable `analyze_log()` function,
so both the CLI (`analyzer.py`) and the web app (`app.py`) share the same engine.

For each login line it:

- extracts the source IP with a regular expression
  (`\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}`)
- separates **failed** logins from **successful** ones
- for successful logins, also reads the date and hour from the start of the line

It then counts attempts per IP with `collections.Counter`, builds the alert lists,
and returns them (plus summary stats) to whichever interface called it.

## Project structure

```
analyzer.py          # command-line interface
app.py               # Flask web dashboard
detector.py          # shared detection logic
templates/
    dashboard.html   # dashboard page
static/
    style.css        # dashboard styling
```

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

- Separate counts per day
- Flag odd-hour logins from external IPs more strongly than internal ones
- Validate IPs properly / support IPv6
- Add charts to the dashboard (e.g. top attacker IPs)

## Why I built it

I'm a cybersecurity student aiming to work in security engineering. This project
mirrors the kind of task a threat-detection team does — turning raw logs into
actionable alerts — and it's where I'm practising Python, regular expressions,
log analysis, and (now) a bit of web development with Flask.