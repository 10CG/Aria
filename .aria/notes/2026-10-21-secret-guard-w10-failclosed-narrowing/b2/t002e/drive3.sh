#!/usr/bin/env bash
# 3c runs on the patched worktree: I0 patch, I1 five filtered rounds, I2 bad-implementation spot checks, I3 full round, I4 the two constructions
set -u
. /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002e/lib.sh
echo "drive3 pid $$" >> "$O/pids.txt"
judged() { grep -q 'timing batch: judged' "$1" 2>/dev/null; }
log "drive3 begin"
if [[ "${1:-}" != nopatch ]]; then
  python3 "$O/patch3c.py" "$W" "$V/run-suite.sh" >> "$O/drive.log" 2>&1 || { log "I0 patch failed"; exit 3; }
  log "I0 patched; worktree status [$(git -C "$W" status --short | tr '\n' ' ')]"
fi
log "impl hook $(sha256sum < "$W/hooks/secret-guard.sh" | cut -c1-12) suite $(sha256sum < "$W/hooks/tests/secret-guard.test.sh" | cut -c1-12) helper $(sha256sum < "$W/hooks/tests/lib/secret-guard-w10-direct.sh" | cut -c1-12)"
# I1: the implementation, SG_W10_ONLY=., five bash, in the worktree (a git checkout); a round whose timing batch was not judged is run again (at most 3 tries)
for v in 50 51 52 53 32; do
  b=B$v
  for try in 1 2 3; do
    waitlow; log "I1 impl $v try $try start"
    ( cd "$W" && SC_BASH=${!b} SG_W10_ONLY=. SG_W10_LOG=$O/impl-$v.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh > "$O/impl-$v.txt" 2>&1 )
    log "I1 impl $v try $try end rc=$? | $(tail -n 1 "$O/impl-$v.log" 2>/dev/null)"
    judged "$O/impl-$v.log" && break
  done
done
# I2: bad implementations rebuilt from the implementation; the designated cases through run-suite.sh; the same cases on the implementation
python3 "$V/mutants.py" "$W/hooks/secret-guard.sh" "$O/mut" > "$O/mutants-build.txt" 2>&1; log "I2 mutants.py rc=$?"
for m in 'BI-8:^(V9-E12-vmax-unchanged)$' 'BI-5:^(V2-G4-extension-file-with-entry|V2-E9-extension-project)$' 'BI-45:^(V6-S20-segment-fallback-text)$'; do
  id=${m%%:*}; re=${m#*:}; waitlow; log "I2 $id start"
  SG_W10_ONLY=$re SG_W10_LOG=$O/mut-$id.log bash "$V/run-suite.sh" "$W" "$O/mut/$id.sh" "$O/work" > "$O/mut-$id.txt" 2>&1; log "I2 $id end rc=$?"
done
waitlow; log "I2 impl start"
SG_W10_ONLY='^(V9-E12-vmax-unchanged|V2-G4-extension-file-with-entry|V2-E9-extension-project|V6-S20-segment-fallback-text)$' SG_W10_LOG=$O/mut-impl.log \
  bash "$V/run-suite.sh" "$W" "$W/hooks/secret-guard.sh" "$O/work" > "$O/mut-impl.txt" 2>&1; log "I2 impl end rc=$?"
# I3: full round in the worktree, PATH bash (at most 3 tries for a judged timing batch)
for try in 1 2 3; do
  waitlow; log "I3 full try $try start"
  ( cd "$W" && SG_W10_LOG=$O/full.log taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh > "$O/full.txt" 2>&1 ); log "I3 full try $try end rc=$? | $(tail -n 1 "$O/full.log" 2>/dev/null)"
  judged "$O/full.log" && break
done
# I4: the constructions, as hook copies run through run-suite.sh (the whole suite in its copy; SC-13 is red there by design)
python3 - "$W/hooks/secret-guard.sh" "$O" <<'EOF' >> "$O/drive.log" 2>&1
import sys
src, o = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8', newline='').read()
def one(t, old, new, tag):
    n = t.count(old)
    if n != 1:
        sys.exit(f'{tag}: {n} hits')
    return t.replace(old, new)
c1 = one(t, '  [[ -z "${_SG_RELAXED:-}" ]] || return 1\n  local osr= wsl=\n',
         '  return 1   # construction C1 (3c): the admission gate is always closed\n  [[ -z "${_SG_RELAXED:-}" ]] || return 1\n  local osr= wsl=\n', 'c1')
c2 = one(t, '  _SG_RELAXED=1\n  _sg_vx_pass "$1" "$_SG_MODE"\n',
         '  sleep 4   # construction C2 (3c): the rerun is held past the deadline (its timer already runs)\n  _SG_RELAXED=1\n  _sg_vx_pass "$1" "$_SG_MODE"\n', 'c2')
open(o + '/c1-hook.sh', 'w', encoding='utf-8', newline='').write(c1)
open(o + '/c2-hook.sh', 'w', encoding='utf-8', newline='').write(c2)
print('constructions built')
EOF
for c in c1 c2; do
  waitlow; log "I4 $c start"
  bash "$V/run-suite.sh" "$W" "$O/$c-hook.sh" "$O/work" > "$O/$c.txt" 2>&1; log "I4 $c end rc=$?"
done
log "drive3 done"
