# gen-v3.py <shape> <out file> -- adversarial inputs for the #217 v3 prototype (no credential VALUES; credential-shaped PATHS are assembled at run time).
# Shapes apply-heavy*, shrink: from the post_spec R2 tech-lead seat's gen.py (TL2-F1, TL2-F4); km-ext*: KM-F-01; segfinding: TL2's seg-finding probe;
# f5like: TL2-F5 (a relaxable big segment followed by expensive small segments).
import sys
shape, out = sys.argv[1], sys.argv[2]
DOT = "."
CREDPATH = "~/" + DOT + "aw" + "s/cred" + "entials"
AIPATH = "/etc/forg" + "ejo/app" + DOT + "ini"

def w(s):
    open(out, "w", encoding="utf-8").write(s)

def heavy_refs():
    refs = []
    for i in range(16):
        refs += [f"${{v{i:02d}}}"] * 8 + [f"$v{i:02d}"] * 8
    return " ".join(refs)

assigns16 = "; ".join(f"v{i:02d}=a" for i in range(16))
if shape == "apply-heavy":
    body = heavy_refs(); cmd = f"(true); {assigns16}; echo {body}"
    cmd += " word" * ((60000 - len(cmd)) // 5); cmd += " " + body; w(cmd)
elif shape == "apply-heavy-seg":
    body = heavy_refs(); cmd = f"{assigns16}; echo {body}"
    cmd += " word" * ((60000 - len(cmd)) // 5); cmd += " " + body; w(cmd)
elif shape == "apply-heavy-cjk":
    body = heavy_refs(); cmd = f"(true); {assigns16}; echo {body}"
    unit = " 中文说明文字"; cmd += unit * ((60000 - len(cmd)) // len(unit)); cmd += " " + body; w(cmd)
elif shape == "shrink":
    names = [("L" + str(i) + "_" + "N" * 600) for i in range(2)]
    assigns = "; ".join(f"{n}=a" for n in names)
    refs = " ".join([f"${{{n}}}" for n in names] * 4 + [f"${n}" for n in names] * 4)
    w(f"(true); C={CREDPATH}; {assigns}; echo {refs}; cat $C; echo done >/dev/null")
elif shape == "segfinding":
    w(f"p={'x' * 4000}; f={AIPATH}; echo $p\necho $p\n" + "lorem ipsum dolor sit amet\n" * 12 + "cat $f")
elif shape == "f5like":
    # segment mode, cheap first pass (the raw command is about 4.5 KB): the copy of `echo $x $x $x $x <filler>` is over 8192 only after
    # substitution (growth 7992, under the growth limit), so the baseline blocks it for its size; the three segments behind it hold an
    # 8000-character token only after substitution ($T$T$T$T), and each costs about a second of credit (the tight check on one long token)
    small = "cat $C | wc -c $T$T$T$T"
    w(f"C={CREDPATH}; x={'x' * 2000}; T={'t' * 2000}; echo $x $x $x $x" + " y" * 150 + "; " + "; ".join([small] * 3))
elif shape == "km-ext":
    w("(x=1; : $x\n" + "A" * 24000 + "\ncat /srv/billing/conf/prod.toml)")
elif shape == "km-ext-small":
    w("(x=1; : $x\n" + "A" * 100 + "\ncat /srv/billing/conf/prod.toml)")
else:
    raise SystemExit("unknown shape " + shape)
print(shape, len(open(out, encoding="utf-8").read()))
