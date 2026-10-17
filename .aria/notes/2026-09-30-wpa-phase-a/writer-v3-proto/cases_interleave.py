CASES = [
    ("Bash", 'f=/etc/forgejo/app.ini; sed -n "1,80p" "$f"', 2),
    ("Bash", 'f=/etc/hosts; cat "$f"; cat .env', 2),
    ("Bash", 'f=/etc/hosts; cat "$f"', 0),
    ("Bash", 'ls -la', 0),
    ("Bash", 'd=/etc/forgejo; f=$d/app.ini; cat "$f"', 2),
]
