"""b1_shapes.py -- the single source of the B.1 padding shapes (imported by b1_curve.py and b1_fn_audit.py).

kind: secret (a credential-file read heads the segment: a risky pattern hits) / benign (no credential-shaped token) / floor
shape (padding appended to the head; the whole string stays ONE segment -- no top-level ; && || or newline):
  A one long path token   B many short words   C a long `| cat` pipeline   D pipes inside one quoted grep -F argument
  E a jq program full of pipes (targets the jq credit regex)   F runs of 400 random alnum bytes (a W10-substitution-like copy)
  S the head is its OWN first segment (`; echo done` follows it) and the `| cat` padding lives in the SECOND segment
The credential path is assembled at run time; it is never a contiguous literal in this source.
"""
import secrets
import string

ALNUM = string.ascii_letters + string.digits
CRED = "~/" + ".aw" + "s/cre" + "dentials"
HEAD = {"secret": "cat " + CRED, "benign": "cat /tmp/notes.txt"}


def pad(shape, n):
    """Padding of about n bytes in the given shape."""
    if shape == "A":
        return " /tmp/" + "a" * n
    if shape == "B":
        return " " + ("word " * (n // 5 + 1))[:n]
    if shape == "C":
        return " | cat" * (n // 6 + 1)
    if shape == "D":
        return ' | grep -F "' + "x|" * (n // 2 + 1) + '"'
    if shape == "E":
        return " | jq '" + "a|" * (n // 2 + 1) + "'"
    if shape == "F":
        k = n // 401 + 1
        return " " + " ".join("".join(secrets.choice(ALNUM) for _ in range(400)) for _ in range(k))
    if shape == "S":
        return " ; echo done" + " | cat" * ((n - 12) // 6 + 1)
    raise SystemExit("unknown shape " + shape)


def build(kind, shape, kb):
    if kind == "floor":
        return "echo hi"
    head = HEAD[kind]
    return head + pad(shape, kb * 1024 - len(head))
