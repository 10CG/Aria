B = "Bash"
CASES = [
    (B, "f=/etc/forgejo/app.ini; sed -n 1,80p \"$f\"", 2),
    (B, "export f=/etc/forgejo/app.ini; cat $f", 2),
    (B, "declare -x f=/etc/forgejo/app.ini; cat $f", 2),
    (B, "local f=/etc/forgejo/app.ini; cat $f", 2),
    (B, 'f="/etc/forgejo/app.ini"; cat "$f"', 2),
]
