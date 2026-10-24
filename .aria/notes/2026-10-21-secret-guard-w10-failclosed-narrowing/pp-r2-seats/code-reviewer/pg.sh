source "$1" </dev/null >/dev/null 2>&1; set +e
export SECRET_GUARD_TIME_BUDGET_S=1; _SG_MODE=whole; _SG_P0=$EPOCHREALTIME
_sg_vx_pass() { local me=$BASHPID; sleep 0.31 & local c=$!; sleep 0.05; echo "job $me: members of pgid $me: $(ps -eo pid=,pgid=,args= | awk -v g=$me '$2==g{printf "[%s %s %s] ", $1, $3, $4}')" >&2; wait $c; return 2; }
_sg_relax_run cmd; echo "rc=$?"
