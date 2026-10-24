# build the probe checkout: a copy of the worktree's hooks with three reference entries made wrong (my own construction, not the author's)
import shutil, sys, os
wt, co = sys.argv[1], sys.argv[2]
if os.path.exists(co): shutil.rmtree(co)
shutil.copytree(wt + '/hooks', co + '/hooks', symlinks=True)
def ins(path, anchor_fn, after, lines):
    s = open(path, encoding='utf-8').read().split('\n')
    i = next(k for k, l in enumerate(s) if l.startswith(anchor_fn))
    j = next(k for k in range(i, len(s)) if s[k].strip() == after)
    s[j+1:j+1] = lines
    open(path, 'w', encoding='utf-8').write('\n'.join(s))
ins(co + '/hooks/tests/secret-guard.test.sh', 'sg_w10_ref() {', 'case $1 in',
    ["    V7-E1-benign-big-allowed) echo '2 vmax' ;;", "    V1-E16-p1-small-benign) echo 'unrecorded -' ;;"])
ins(co + '/hooks/tests/lib/secret-guard-w10-direct.sh', '  fbref() {', 'case $1 in',
    ["      V6-S20-segment-fallback-text) echo '2 vmax' ;;"])
print('probe checkout built')
