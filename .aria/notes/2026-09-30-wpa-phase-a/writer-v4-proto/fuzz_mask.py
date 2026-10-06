#!/usr/bin/env python3
"""fuzz_mask.py [N] -- differential test: the quote state machine of the W9 prototype mask (_sg_ext_mask) against the built-in _sg_split_top (the contract the Spec names:
"same state machine").  N random strings (default 4000) over a small alphabet of quotes / escapes / separators; for every string that _sg_safe_to_split judges safe and that has
no `&&` / `||` (the only separators _sg_split_top treats beyond `;`):
   segments_from_mask = split the ORIGINAL string at the `;` positions that the mask left alone (an unquoted `;`), drop whitespace-only pieces
   segments_builtin   = _SG_SEGS of _sg_split_top
the two lists must be equal.  Also checked on EVERY string (safe or not): the mask changes only the four separator characters, keeps the byte length, and terminates.
Prints counts only (no hook output text)."""
import os
import random
import subprocess
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(EXP, "work", "t4f", "aria", "hooks", "secret-guard.sh")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
rnd = random.Random(20261006)
ALPHA = ["a", "b", " ", ";", "&", "|", "\n", "'", '"', "$", "\\", "x y", "$'", "\\;", '"|"', "';'", "echo ", "cat "]
strings = []
while len(strings) < N:
    s = "".join(rnd.choice(ALPHA) for _ in range(rnd.randint(1, 14)))
    if "&&" in s or "||" in s:
        continue
    strings.append(s)
work = os.path.join(EXP, "work", "fuzz_mask")
os.makedirs(work, exist_ok=True)
with open(os.path.join(work, "in.bin"), "wb") as fh:
    for s in strings:
        fh.write(s.encode() + b"\0")
driver = r'''
source "$HOOK"
set +u
while IFS= read -r -d '' s; do
  if _sg_safe_to_split "$s" >/dev/null 2>&1; then safe=0; else safe=1; fi
  m="$(_sg_ext_mask "$s")"
  segs=""
  if [[ $safe -eq 0 ]]; then _sg_split_top "$s"; for g in "${_SG_SEGS[@]}"; do segs+="${g}"$'\x02'; done; fi
  printf '%s\x01%s\x01%s\x01' "$safe" "$m" "$segs"
  printf '\0'
done < "$IN"
'''
env = {"PATH": os.environ["PATH"], "HOME": os.path.join(EXP, "home"), "TMPDIR": os.path.join(EXP, "tmp"), "LC_ALL": "C.UTF-8", "HOOK": HOOK, "IN": os.path.join(work, "in.bin")}
p = subprocess.run(["bash", "-c", driver], capture_output=True, env=env, timeout=1800)
recs = p.stdout.split(b"\0")[:-1] if p.stdout.endswith(b"\0") else p.stdout.split(b"\0")
if len(recs) != len(strings):
    print("RECORD COUNT MISMATCH", len(recs), len(strings), "stderr bytes", len(p.stderr))
    sys.exit(2)

def oracle(s):
    """-> (positions of ; & | newline that sit INSIDE quotes, positions of top-level ; (unquoted, not escaped)).  Rules: single quotes have no escapes; double quotes and $'..' honour
    backslash; outside quotes a backslash escapes the next character."""
    inside, top = set(), []
    state, i, n = "u", 0, len(s)
    while i < n:
        ch = s[i]
        if state == "u":
            if ch == "\\":
                i += 2
                continue
            if ch == "'":
                state = "s"
            elif ch == '"':
                state = "d"
            elif ch == "$" and i + 1 < n and s[i + 1] == "'":
                state = "a"
                i += 1
            elif ch == ";":
                top.append(i)
        elif state == "s":
            if ch == "'":
                state = "u"
            elif ch in ";&|\n":
                inside.add(i)
        elif state == "d":
            if ch == "\\":
                if i + 1 < n and s[i + 1] in ";&|\n":
                    inside.add(i + 1)
                i += 2
                continue
            if ch == '"':
                state = "u"
            elif ch in ";&|\n":
                inside.add(i)
        else:                                  # $'...'
            if ch == "\\":
                if i + 1 < n and s[i + 1] in ";&|\n":
                    inside.add(i + 1)
                i += 2
                continue
            if ch == "'":
                state = "u"
            elif ch in ";&|\n":
                inside.add(i)
        i += 1
    return inside, top


safe_n = cmp_n = bad_len = bad_pos = bad_segs = 0
examples = []
for s_full, rec in zip(strings, recs):
    safe_s, masked_b, segs_b = rec.split(b"\x01")[:3]
    masked = masked_b.decode()
    inside, top = oracle(s_full)
    # the mask is captured with $( ), which strips TRAILING newlines of its output: a trailing newline that the mask turned into a space (it sat inside a quote) survives as a
    # space, an unquoted one is stripped.  Accept exactly the two lengths and check the positions on the common prefix; the stripped tail must hold unquoted newlines only.
    n_m = len(masked)
    if n_m != len(s_full) and n_m != len(s_full.rstrip("\n")):
        bad_len += 1
        if len(examples) < 5:
            examples.append(("LEN", s_full, len(s_full), n_m))
        continue
    changed = {i for i in range(n_m) if s_full[i] != masked[i]}
    want_changed = {i for i in inside if i < n_m}
    stripped_tail_ok = all(i not in inside for i in range(n_m, len(s_full)))
    if changed != want_changed or not stripped_tail_ok or any(masked[i] != " " for i in changed):
        bad_pos += 1
        if len(examples) < 5:
            examples.append(("MASK", s_full, sorted(inside), sorted(changed)))
        continue
    if safe_s != b"0":
        continue
    safe_n += 1
    pieces, start = [], 0
    for i in top:
        pieces.append(s_full[start:i])
        start = i + 1
    pieces.append(s_full[start:])
    want = [x for x in pieces if x.strip()]
    got = [x for x in segs_b.decode().split("\x02") if x != ""]
    cmp_n += 1
    if want != got:
        bad_segs += 1
        if len(examples) < 5:
            examples.append(("SPLIT", s_full, want, got))
print("strings:", N, "| mask output length in {full, trailing-newline-stripped}, changed positions == oracle (separators inside quotes) -- mismatches:", bad_pos + bad_len, "(length", bad_len, "/ positions", bad_pos, ")")
print("strings judged safe by _sg_safe_to_split and compared against _sg_split_top:", cmp_n, "| segment lists differ from the oracle:", bad_segs)
for e in examples:
    print("  EXAMPLE", e)
sys.exit(1 if (bad_len or bad_pos or bad_segs) else 0)
