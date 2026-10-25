#!/usr/bin/env bash
# analyze.sh <W9|W13|MUT <files...>|W12> (T004b, 10CG/aria-plugin#217): the comparisons; aggregates, ids and verdicts only, no command text of the corpus
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; T=$S/r217impl/t004b; A=$T/ana; C=$T/chk; mkdir -p "$A"
REPO=/home/dev/Aria; NR=.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing; V31=$REPO/$NR/v31; OUTD=$V31/impl; B2=$REPO/$NR/b2
g95() { git -C "$REPO" show 95cf1de7:"$NR/v31/$1"; }
ends() { echo "$(basename "$1"): $(head -1 "$1" | grep -oE '^# [0-9T:-]+Z') $(head -1 "$1" | grep -oE 'load [0-9. ]+') -> $(tail -1 "$1" | grep -oE '^# [0-9T:-]+Z') $(tail -1 "$1" | grep -oE 'load (at the end )?[0-9. ]+')"; }
mut() { python3 - "$@" <<'PY'
import sys, re, collections
V = {'CAUGHT', 'MISSED', 'WRONG-REASON', 'NOT-JUDGED', 'SETUP', 'GREEN', 'RED'}
for p in sys.argv[1:]:
    c = collections.Counter(); bad = []; oth = []; heads = []; ids = []
    for l in open(p, encoding='utf-8', errors='replace').read().split('\n'):
        if l.startswith(('# run-mutants.sh', '# perturbation round')) or re.match(r'# \d+ caught', l): heads.append(l[:150])
        f = l.split()
        if len(f) >= 2 and f[1] in V:
            c[f[1]] += 1; ids.append(f[0])
            if f[1] not in ('CAUGHT', 'GREEN'): bad.append(f[0] + ' ' + f[1] + ' | ' + ' '.join(re.findall(r'load start [0-9.]+', l))[:40] + ' | ' + l.split('|')[-1].strip()[:90])
            m = re.search(r'other red: (.*)$', l)
            if m: oth.append((f[0], len(m.group(1).split())))
    print('%s: %s | ids %d (BI %d, P %d) | with other red: %d (cases %d)' % (p.split('/')[-1], dict(c), len(ids), sum(i.startswith('BI') for i in ids), sum(i.startswith('P') for i in ids), len(oth), sum(n for _, n in oth)))
    for h in heads: print('   ', h)
    for b in bad: print('    not caught/green:', b)
PY
}
case $1 in
W9) f=$OUTD/W9-suite.txt; wd=$(ls -d "$T"/wd-W9-a* | sort | tail -1); ends "$f"; g95 W9-suite.txt > "$A/W9-95.txt"
  python3 - "$f" "$A/W9-95.txt" <<'PY'
import re, sys
def parse(p):
    secs = {}; sec = None; cur = None
    for l in open(p, encoding='utf-8', errors='replace').read().split('\n'):
        if l.startswith('## '): sec = l[3:].strip(); secs[sec] = {'sum': [], 'ent': {}}; cur = None; continue
        if sec is None: continue
        if l.startswith(('PASS:', 'FAIL:')): secs[sec]['sum'].append(l.strip()); continue
        if l.startswith('  FAIL '): cur = l[7:]; secs[sec]['ent'][cur] = []; continue
        if l.startswith('      ') and cur is not None: secs[sec]['ent'][cur].append(l.strip())
    return secs
def gid(n):
    m = re.search(r'SC-\d+[a-z]*', n); return m.group(0) if m else n[:40]
new, old = parse(sys.argv[1]), parse(sys.argv[2])
b, i, oi = new['base']['ent'], new['impl']['ent'], old['impl']['ent']
print('summary base:', ' / '.join(new['base']['sum']), '| impl:', ' / '.join(new['impl']['sum']))
print('95cf1de7 summary base:', ' / '.join(old['base']['sum']), '| impl:', ' / '.join(old['impl']['sum']))
print('groups that change base -> impl:', ' '.join(sorted(set(gid(k) for k in set(b) ^ set(i)) | set(gid(k) for k in set(b) & set(i) if b[k] != i[k]))))
print('FAIL entries identical in base and impl:', ' '.join(sorted(gid(k) for k in set(b) & set(i) if b[k] == i[k])))
print('impl vs 95cf1de7 impl (entries that differ):')
for k in sorted(set(i) | set(oi), key=gid):
    x, y = i.get(k), oi.get(k)
    if x == y: continue
    if x is None or y is None: print('   ', gid(k), 'only in', 'now' if y is None else '95cf1de7'); continue
    print('   ', gid(k), '| checks now', len(x), '95cf1de7', len(y), '| check lines only now', len(set(x) - set(y)), 'only 95cf1de7', len(set(y) - set(x)))
print('impl entries identical to 95cf1de7:', sum(1 for k in i if oi.get(k) == i[k]), 'of', len(i), '(95cf1de7 has', len(oi), ')')
PY
  echo "-- cmp-w9.py (lead): mine vs proto, mine vs impl2 (low load)"
  python3 "$B2/t004a-verify/cmp-w9.py" mine "$wd/suite-impl.out" proto "$B2/t004a-verify/suite-proto.out" > "$A/cmpw9-proto.txt" 2>&1
  python3 "$B2/t004a-verify/cmp-w9.py" mine "$wd/suite-impl.out" impl2 "$B2/t004a-verify/suite-impl2.out" > "$A/cmpw9-impl2.txt" 2>&1
  cut -c1-160 "$A/cmpw9-proto.txt" | head -12; echo "--"; cut -c1-160 "$A/cmpw9-impl2.txt" | head -12 ;;
W13) f=$OUTD/W13-sc-cases.txt; ends "$f"; g95 W13-sc-cases.txt > "$A/W13-95.txt"
  awk '/^## 1\./{s=1; next} /^## 2\./{s=0} s && /^bash /' "$f" | cut -c1-150
  echo "  FAIL lines in section 1: $(awk '/^## 1\./{s=1; next} /^## 2\./{s=0} s && /^FAIL/' "$f" | wc -l)"
  python3 - "$f" "$A/W13-95.txt" <<'PY'
import sys
def s2(p):
    red = green = tot = None
    for l in open(p, encoding='utf-8', errors='replace').read().split('\n'):
        if l.startswith('  red:'): red = l.split()[1:]
        if l.startswith('  green:'): green = l.split()[1:]
        if l.startswith('# totals:') and tot is None: tot = l
    return tot, set(red or []), set(green or [])
tn, rn, gn = s2(sys.argv[1]); to, ro, go = s2(sys.argv[2])
print('section 2 now:', tn, '| 95cf1de7:', to)
print('  red in both', len(rn & ro), '| green in both', len(gn & go), '| flipped red->green', sorted(ro & gn), '| green->red', sorted(go & rn))
print('  in 95cf1de7, missing now:', sorted((ro | go) - (rn | gn)))
nw = sorted((rn | gn) - (ro | go))
print('  new ids:', len(nw), '| red:', ' '.join(sorted(set(nw) & rn)), '| green:', ' '.join(sorted(set(nw) & gn)))
PY
  awk '/^## 3\./{s=1; next} s' "$f" > "$A/W13-s3.txt"; mut "$A/W13-s3.txt" ;;
MUT) shift; for f in "$@"; do ends "$f"; done; mut "$@" ;;
W12) f=$OUTD/W12-real-traffic.txt; wd=$(ls -d "$T"/wd-W12-a* | sort | tail -1); ends "$f"
  sed -n '2,60p' "$f" | grep -v '^# ' | cut -c1-170 | head -40
  g95 W12-replay-138.tsv > "$A/W12-95.tsv"; W1F=$REPO/$NR/evidence/W1-classification.tsv
  awk -F'\t' 'FNR==1{f++} /^#/{next} f==1{p[$1]=$3; next} f==2{k[$1]=$3; rc[$1]=$2; rs[$1]=$6; w[$1]=$4; next} f==3{bk[$1]=$3; next} f==4 && /^DIFF n=/{split($0, dv, /[ =]/); d[dv[3]]=1; next} f==5{cls[$1]=$5}
    END{for (x in k) { if (cls[x]=="size" && k[x]=="allow") a++; if (cls[x]=="size" && p[x]=="allow") a95++
        if (p[x]=="allow" && k[x]!="allow") printf "  allowed in 95cf1de7, not now: n=%s now %s rc %s relax-start %s W %s | baseline %s | ident pass %s\n", x, k[x], rc[x], rs[x], w[x], bk[x], ((x in d) ? "differs" : "identical")
        if (p[x]!="allow" && k[x]=="allow") printf "  allowed now, not in 95cf1de7: n=%s (95cf1de7 %s)\n", x, p[x]
        if (cls[x]=="value") printf "  VMAX n=%s now %s rc %s relax-start %s | baseline %s | 95cf1de7 %s\n", x, k[x], rc[x], rs[x], bk[x], p[x] }
      printf "  SMAX allowed: now %d, 95cf1de7 %d (floor %d)\n", a, a95, a95 - 1 }' "$A/W12-95.tsv" "$wd/W12-replay-138.tsv" "$wd/W12-replay-138-base.tsv" "$wd/W12-ident-138.txt" "$W1F"
  export W1=$W1F; TSV="$wd/W12-replay-138.rows" bash "$C/s1-old.sh" > "$A/s1-old-now.txt"; TSV="$wd/W12-replay-138.tsv" bash "$C/s1-new.sh" > "$A/s1-new-now.txt"
  awk '/^## 1\./{s=1; next} /^## 1b\./{s=0} s' "$f" > "$A/s1-file-now.txt"
  echo "  section 1 readers, this run: old-on-rows vs new-on-tsv $(cmp -s "$A/s1-old-now.txt" "$A/s1-new-now.txt" && echo SAME || echo DIFFER) | vs the file $(cmp -s "$A/s1-new-now.txt" "$A/s1-file-now.txt" && echo SAME || echo DIFFER) | tsv first line $(head -1 "$wd/W12-replay-138.tsv" | cut -c1-12) rows $(grep -vc '^#' "$wd/W12-replay-138.tsv")"
  for x in W12-replay-138.tsv W12-replay-138-base.tsv W12-ident-138.txt; do echo "  $x: header sha prefixes $(head -1 "$OUTD/$x" | grep -oE 'sha256 [0-9a-f]{12}' | cut -d' ' -f2 | paste -sd' ')"; done ;;
esac
