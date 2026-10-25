# drive-mut.sh: the V15 cases of the suite on the 5f3 hook (control) and on each of my mutants, one at a time, with load readings
V=$1; W=$2; N=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
waitload() { local i=0; while :; do read -r l1 _ < /proc/loadavg; awk -v a="$l1" 'BEGIN{exit !(a < 1.2)}' && return 0; i=$((i+1)); (( i > 180 )) && return 0; sleep 10; done; }
mkdir -p "$V/runs"
for h in "$V/hook-5f4.sh" "$V"/mut-5f4/*.sh; do
  n=$(basename "$h" .sh); waitload
  s=$(cut -d' ' -f1-3 /proc/loadavg)
  SG_W10_ONLY='^V15-' SG_W10_LOG="$V/runs/$n.log" taskset -c 0,1 nice -n 19 bash "$N/run-suite.sh" "$W" "$h" "$V/runs/wd-$n" > "$V/runs/$n.out" 2>&1; rc=$?
  e=$(cut -d' ' -f1-3 /proc/loadavg)
  echo "$n rc=$rc load-start $s load-end $e" >> "$V/runs/drive.log"
done
echo done >> "$V/runs/drive.log"
