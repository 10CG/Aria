# compare the six groups' baseline (else) branches between HEAD (fee1a65) and the working tree; list each relaxed-branch wpa_x6 call with the else-branch line for the same command
import subprocess, sys, re
wt = sys.argv[1]
head = subprocess.run(['git', '-C', wt, 'show', 'HEAD:hooks/tests/secret-guard.test.sh'], capture_output=True, text=True).stdout.split('\n')
cur = open(wt + '/hooks/tests/secret-guard.test.sh', encoding='utf-8').read().split('\n')
def blocks(lines):
    out = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('if [[ $wpa_rx6 == yes ]]; then'):
            j = i + 1; depth = 0; els = None
            while j < len(lines):
                l = lines[j]
                if re.match(r'^if\b', l): depth += 1
                if l.startswith('else') and depth == 0 and els is None: els = j
                if l.startswith('fi') and depth == 0: break
                if l.startswith('fi') and depth > 0: depth -= 1
                j += 1
            out.append((i, els, j, lines[i+1:els], lines[els+1:j]))
            i = j
        i += 1
    return out
bh, bc = blocks(head), blocks(cur)
print('groups HEAD', len(bh), 'worktree', len(bc))
for (hi, he, hj, hr, hb), (ci, ce, cj, cr, cb) in zip(bh, bc):
    print(f'group at HEAD:{hi+1} / wt:{ci+1}: else-branch identical = {hb == cb} ({len(cb)} lines); relaxed lines HEAD {len(hr)} wt {len(cr)}')
    for l in cr:
        for m in re.finditer(r'wpa_x6 (\w+) "(\$wpa_L_\w+)" "([^;]*?)"(?:;|$)', l):
            print('   x6', m.group(1), m.group(2), m.group(3)[:60])
    for l in cb:
        if 'wpa_x_toolarge' in l or 'wpa_x ' in l:
            print('   else:', l[:200])
