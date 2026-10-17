#!/usr/bin/env python3
"""fuzz_value_of.py OLD_SCAN_SH NEW_SCAN_SH [--n 3000] [--bash BASH]  -- equivalence of the L3 value-extraction helpers (`_value_of` / `_trimV`) of two prototype hooks.

The spans are REAL spans: random lines are built from fragments (keys, delimiters, quotes, blanks, value runs, URLs, headers, non-ASCII), the hook's own PATTERNS
(all of them, baseline and new) are run over each line with `grep -oE`, and every (tag, span) is fed to both helper sets; the extracted values V must be byte-identical.
The helper blocks are cut out of the two hook files (from `_trimV()` / `_RE_TRIM=` up to `_RE_RED=`), sourced in a fresh bash, and run on the same record stream.
Nothing credential-shaped is printed (only counts and, on a difference, the tag and the span LENGTH and a hash)."""
import hashlib
import random
import re
import subprocess
import sys
import tempfile

old_hook, new_hook = sys.argv[1], sys.argv[2]
n_lines = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 3000
bash = sys.argv[sys.argv.index("--bash") + 1] if "--bash" in sys.argv else "bash"
random.seed(int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7)


def helpers(path):
    t = open(path, encoding="utf-8").read()
    i0 = t.find("_RE_TRIM=")
    if i0 < 0:
        i0 = t.index("_trimV() {")
    i1 = t.index("_RE_RED='^")
    return t[i0:i1]


def patterns(path):
    t = open(path, encoding="utf-8").read()
    out = []
    for m in re.finditer(r"^  '([a-z0-9-]+)\|(.*)'$", t, re.M):
        out.append((m.group(1), m.group(2).replace("'\"'\"'", "'")))
    return out


PATS = patterns(new_hook)
AL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
KEYS = ["JWT_" + "SECRET", "DB_" + "PASSWORD", "API_" + "TOKEN", "SVC_ACCESS_" + "KEY", "X_WEB" + "HOOK_V2", "tok" + "en", "pass" + "word", "client_" + "secret", "api_" + "key",
        "auth" + "Token", "Sec" + "ret", "sha1", "reg" + "istration_token", "private" + "_key", "ENCRYPTION_" + "KEY", "TO" + "KEN"]
BLANKS = ["", " ", "  ", "\t", " " * 5, " " * 40]
QUOTES = ["", '"', "'"]


def val(n=None):
    n = n or random.choice([8, 16, 20, 24, 40, 44, 64, 200])
    return "".join(random.choice(AL + "+/=._~-") for _ in range(n))


def frag():
    k = random.choice(KEYS)
    q = random.choice(QUOTES)
    r = random.random()
    if r < 0.18:
        return f'"{k}"{random.choice(BLANKS)}:{random.choice(BLANKS)}"{val()}"'
    if r < 0.38:
        return f"{random.choice(['', 'export ', 'export' + ' ' * 7])}{k.upper()}{random.choice(BLANKS)}{random.choice('=:')}{random.choice(BLANKS)}{q}{val()}"
    if r < 0.46:
        return f"{random.choice(['--', '-'])}{random.choice(['', 'db-', 'a-b-', 'x' * 30])}{random.choice(['token', 'password', 'api-key', 'secret', 'passwd', 'apikey', 'access-key'])}={val()}"
    if r < 0.58:
        return f"{random.choice(['Authorization', 'authorization', 'AUTHORIZATION'])}:{random.choice(BLANKS)}{random.choice(['token', 'Basic', 'Bearer', 'bearer'])}{random.choice(BLANKS[1:])}{val(random.choice([16, 24, 40, 300]))}"
    if r < 0.64:
        return f"{random.choice(['CF-Access-Client-Secret', 'cf-access-client-secret'])}:{random.choice(BLANKS)}{val(random.choice([16, 24, 64]))}"
    if r < 0.68:
        return f"{random.choice(['X-Api-Key', 'x-api-key'])}:{random.choice(BLANKS)}{val(random.choice([16, 24, 64]))}"
    if r < 0.72:
        return f"{k.upper()}={val(random.choice([8, 12, 24, 44]))}"
    if r < 0.82:
        return f"{random.choice(['postgres', 'postgresql', 'redis', 'rediss', 'mongodb', 'mongodb+srv', 'https', 'http'])}://{random.choice(['u', 'user', 'a.b-c', 'x' * 40])}:{val(random.choice([6, 12, 30]))}@{random.choice(['h', 'host.example', 'db:5432/x'])}"
    if r < 0.86:
        return '"private_key_id": "' + "".join(random.choice("0123456789abcdef") for _ in range(40)) + '"'
    if r < 0.90:
        return random.choice(["AKIA" + "".join(random.choice("0123456789ABCDEF") for _ in range(16)), "ghp_" + val(36).replace("+", "a").replace("/", "b").replace("=", "c").replace(".", "d").replace("_", "e").replace("~", "f").replace("-", "g")])
    if r < 0.94:
        return "\u00e9\u914d\u7f6e " + random.choice(KEYS).upper() + "=" + val()
    return random.choice(["", " ", "text ", "\u2026", "{{ x }}", "<tag>", "${VAR}"]) + "".join(random.choice("abc ;,|") for _ in range(random.randint(0, 8)))


lines = []
for _ in range(n_lines):
    k = random.randint(1, 4)
    lines.append(random.choice(["", " ", "x", "\t"]).join(frag() for _ in range(k)))

records = []
for line in lines:
    for tag, pat in PATS:
        p = subprocess.run(["grep", "-oE", "--", pat], input=line.encode(), capture_output=True)
        for span in p.stdout.decode("utf-8", "replace").split("\n"):
            if span:
                records.append((tag, span))
print(f"lines={len(lines)} spans={len(records)} tags={len({t for t, _ in records})}")


def run_helpers(path):
    code = "set -u\nV=''\n" + helpers(path) + '\nwhile IFS= read -r -d $\'\\x1f\' tag && IFS= read -r -d $\'\\x1e\' span; do _value_of "$tag" "$span"; printf \'%s\\x1e\' "$V"; done\n'
    payload = "".join(t + "\x1f" + s + "\x1e" for t, s in records).encode("utf-8")
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as f:
        f.write(code)
        name = f.name
    p = subprocess.run([bash, name], input=payload, capture_output=True, timeout=1800)
    assert p.returncode == 0, p.stderr.decode()[:300]
    return p.stdout.decode("utf-8", "replace").split("\x1e")[:-1]


a, b = run_helpers(old_hook), run_helpers(new_hook)
assert len(a) == len(b) == len(records), (len(a), len(b), len(records))
bad = [(records[i][0], len(records[i][1]), hashlib.sha256(records[i][1].encode()).hexdigest()[:8]) for i in range(len(records)) if a[i] != b[i]]
print("differences:", len(bad))
for t in bad[:12]:
    print("  tag=%s span-len=%d sha=%s" % t)
sys.exit(1 if bad else 0)
