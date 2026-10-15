import os
P = "/srv/billing/conf/prod.toml"
APPINI = "/etc/forgejo/app.ini"
proj = os.environ.get("WPA_PROJ", "/nonexistent")
ENV = {"CLAUDE_PROJECT_DIR": proj}
SK = [
    ("py-semi", 'python3 -c "import os; print(open(\'%s\').read())"'),
    ("py-semis", 'python3 -c "x=1; y=2; print(open(\'%s\').read())"'),
    ("py-amp", 'python3 -c "a=1 & 2; print(open(\'%s\').read())"'),
    ("py-newline", 'python3 -c "import os\nprint(open(\'%s\').read())"'),
    ("node-semi", 'node -e "const fs=require(\'fs\'); console.log(fs.readFileSync(\'%s\',\'utf8\'))"'),
    ("awk-semi", "awk 'BEGIN{x=1; while ((getline l < \"%s\") > 0) print l}'"),
    ("py-quoted-pipe", 'python3 -c "print(1|2); print(open(\'%s\').read())"'),
    ("grep-quoted-pipe", "grep -E 'A|B' %s"),
]
CONTROLS = [
    "cat x; echo %s",
    "ls | grep y; echo %s",
    'echo "see %s"; cat y',
    "cat x\necho %s",
    "cat x & echo %s",
    "cat x | echo %s",
    "echo %s",
]
CASES = []
for lab, t in SK:
    CASES.append(("Bash", t % P))
for lab, t in SK:
    CASES.append(("Bash", t % APPINI))
for t in CONTROLS:
    CASES.append(("Bash", t % P, 0))
