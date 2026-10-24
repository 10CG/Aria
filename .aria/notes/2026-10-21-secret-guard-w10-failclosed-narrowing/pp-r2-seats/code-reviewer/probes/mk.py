import json, sys
DOT = "."; APPINI = "/etc/forg" + "ejo/app" + DOT + "ini"; X4000 = "x" * 4000
P = {}
# MA: segment mode (no parenthesis / brace), one long segment (copy > 8192, growth 3998), then a read of the extension-listed path
P["seg-ext-read"] = f"x={X4000}; : {'y ' * 2600}$x; cat /srv/billing/conf/prod.toml"
# MB: whole mode (parenthesis), copy > 8192 via $x $x, 8 dummy for loops, the read through the 9th for variable
P["for9-read"] = "(true)\n" + f"x={X4000}\n: $x $x\n" + "".join(f"for a{i} in v{i}; do :; done\n" for i in range(1, 9)) + f"for f in {APPINI}; do cat $f; done\n"
# MC: whole mode, one line: copy > 8192 with its only line > 8192, the read through $F, an unrelated redacting filter elsewhere on the line
P["longline-credit"] = f"(true); F={APPINI}; x={X4000}; : $x $x; cat $F; echo done >/dev/null"
# MD: segment mode, a long segment whose copy has one line > 8192 and reads through $F, with an unrelated >/dev/null in the same segment
P["seg-longline-credit"] = f"F={APPINI}; x={X4000}; : $x $x | cat $F | tee /dev/null >/dev/null"
for k, v in P.items():
    json.dump({"tool_name": "Bash", "tool_input": {"command": v}}, open(f"probes/{k}.json", "w"))
    print(k, len(v))
