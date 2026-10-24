#!/usr/bin/env python3
"""gen_literal.py derived.json : prints the HOOK_TEXT literal for commentsync.py (per site: the locator, the removed sentences with where they occur, the new
sentences with whether the prototype already holds them). Derived mechanically by derive.py from the baseline, the prototype and the spec target."""
import json, sys
D = json.load(open(sys.argv[1], encoding='utf-8'))
print('HOOK_TEXT = [  # site, locator, untrue sentences (b = in the baseline run, p = in the prototype run), new sentences (p = the prototype has it, s = What 7 supplement)')
for d in D:
    loc = tuple(d['loc'])
    print(f" ({d['site']!r}, {loc!r},")
    print('  [' + ',\n   '.join(repr(('b' if ib else '') + ('p' if ip else ''), ) [:-1] + ', ' + repr(u)[0:] + ')' if False else repr((('b' if ib else '') + ('p' if ip else ''), u)) for u, ib, ip in d['untrue']) + '],')
    print('  [' + ',\n   '.join(repr(('p' if ip else 's', u)) for u, ip in d['new']) + ']),')
print(']')
