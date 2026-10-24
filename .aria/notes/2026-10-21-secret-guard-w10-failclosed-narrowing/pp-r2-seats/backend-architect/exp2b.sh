#!/usr/bin/env bash
H=$1
source "$H" </dev/null >/dev/null 2>&1
set +e
export SECRET_GUARD_TIME_BUDGET_S=3
_SG_MODE=whole
LOG=$(mktemp)
_sg_vx_pass() {
  { printf 'JOB BASHPID=%s PPID=%s\n' "$BASHPID" "$PPID"; ps -eo pid,ppid,pgid,sid,stat,args | awk -v me="$BASHPID" 'NR==1 || $0 ~ /exp2b.sh/ || $5 ~ /^S/ && $6=="sleep" && $7 ~ /^[0-9]+\.[0-9]{6}$/ {print "   view: " $0}'; } >> "$LOG"
  return 0
}
_SG_P0=$EPOCHREALTIME
_sg_relax_run "x" ; rc=$?
echo "bash $BASH_VERSION rc=$rc"
cat "$LOG"; rm -f "$LOG"
