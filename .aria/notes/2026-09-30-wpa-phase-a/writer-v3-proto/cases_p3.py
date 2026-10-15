B = "Bash"
F = "/etc/forgejo/app.ini"
CASES = [(B, c, 2) for c in (f"true; export f={F}; cat $f", f"true; declare f={F}; cat $f", f"true; local f={F}; cat $f", f"true; readonly f={F}; cat $f", f"true; typeset f={F}; cat $f",
    f"true; declare -x f={F}; cat $f", f'true; f="{F}"; cat "$f"', f"true; f='{F}'; sed -n 1,80p \"$f\"", f'true; export f="{F}"; cat $f')]
