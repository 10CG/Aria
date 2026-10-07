#!/usr/bin/env python3
"""Add the ONE new registration of the R5 X cluster to <tree>/aria/hooks/hooks.json: secret-scan.sh under `PostToolUseFailure`, same matcher as its `PostToolUse` entry.

usage: python3 patch_hooks_json.py <proto dir> [--variant NAME]
variants (bad implementations; every one must turn a probe row red):
  v6                 the design (exactly one extra registration; the top-level description string also names the new event)    -> all rows yes
  hooks_nofail       no registration at all (the hook may read `error`, but is never called for a failed call)   -> SC-35 35d
  hooks_wrong_matcher the registration only matches Bash                                                       -> SC-35 35d
  hooks_two_entries  the registration is added twice                                                           -> SC-35 35d
  hooks_other_hook   the failure event also runs submodule-gate-telemetry.sh                                   -> SC-35 35d
  hooks_touch_other  the registration is right but the PostToolUse timeout of secret-scan is changed to 10     -> SC-31 31d
  hooks_gate_literal the file carries the literal of the other Spec's gate key (in the description)                 -> SC-31 31e
Rule #7: no credential-shaped literal here."""
import json
import os
import sys

root = sys.argv[1]
variant = sys.argv[sys.argv.index("--variant") + 1] if "--variant" in sys.argv else "v6"
path = os.path.join(root, "aria", "hooks", "hooks.json")
t = open(path, encoding="utf-8").read()
if variant == "hooks_nofail":
    print("hooks.json untouched (variant hooks_nofail)")
    sys.exit(0)
matcher = "Bash" if variant == "hooks_wrong_matcher" else "Bash|Read|Edit|Write|MultiEdit"
entry = ('      {\n        "matcher": "%s",\n        "hooks": [\n          {\n            "type": "command",\n'
         '            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/secret-scan.sh",\n            "timeout": 5\n          }%s\n        ]\n      }') % (
    matcher, ',\n          {\n            "type": "command",\n            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/submodule-gate-telemetry.sh",\n            "timeout": 30\n          }' if variant == "hooks_other_hook" else "")
block = '    "PostToolUseFailure": [\n' + entry + (",\n" + entry if variant == "hooks_two_entries" else "") + "\n    ]\n"
tail = "    ]\n  }\n}\n"
assert t.endswith(tail), "unexpected end of hooks.json"
t = t[: -len(tail)] + "    ],\n" + block + "  }\n}\n"
if variant not in ("hooks_gate_literal",):          # the description names the new event (a correct implementation would update it; SC-31 31d does not compare it)
    _d = "PostToolUse secret-scan + submodule-gate-telemetry"
    assert t.count(_d) == 1
    t = t.replace(_d, "PostToolUse + PostToolUseFailure secret-scan + PostToolUse submodule-gate-telemetry")
if variant == "hooks_touch_other":
    o = '"command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/secret-scan.sh",\n            "timeout": 5'
    assert t.count(o) == 2, t.count(o)
    t = t.replace(o, o.replace('"timeout": 5', '"timeout": 10'), 1)
if variant == "hooks_gate_literal":
    t = t.replace('"description": "Aria Hooks:', '"description": "completeness_' + 'gate seam. Aria Hooks:', 1)
json.loads(t)
open(path, "w", encoding="utf-8").write(t)
print("hooks.json patched", "(%s)" % variant)
