#!/usr/bin/env bash
# exp2.sh HOOK : (run under the bash being tested) source the hook, stub _sg_vx_pass to print the process-group layout seen from INSIDE the job,
# run _sg_relax_run, then look for survivors. Positive control for the ps filter included.
H=$1
source "$H" </dev/null >/dev/null 2>&1
set +e
export SECRET_GUARD_TIME_BUDGET_S=3
_SG_MODE=whole
LOG=$(mktemp)
sleep 7.123456 & CTL=$!       # positive control for the filter below
_sg_vx_pass() {
  { printf 'JOB BASHPID=%s PPID=%s\n' "$BASHPID" "$PPID"; ps -eo pid,ppid,pgid,sid,stat,args | awk -v me="$BASHPID" '$1==me || $2==me || $3==me {print "   in-job-view: " $0}'; } >> "$LOG"
  return 0
}
_SG_P0=$EPOCHREALTIME
t0=$EPOCHREALTIME
_sg_relax_run "x" ; rc=$?
t1=$EPOCHREALTIME
echo "bash $BASH_VERSION  _sg_relax_run rc=$rc  wall=$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{printf "%.3f", b-a}')s  load=$(cut -d' ' -f1-3 /proc/loadavg)"
cat "$LOG"
echo "   survivors with a 6-decimal sleep arg (control 7.123456 must show once):"
ps -eo pid,ppid,pgid,stat,args | awk '$5=="sleep" && $6 ~ /^[0-9]+\.[0-9][0-9][0-9][0-9][0-9][0-9]$/ {print "     " $0}'
kill "$CTL" 2>/dev/null; rm -f "$LOG"
