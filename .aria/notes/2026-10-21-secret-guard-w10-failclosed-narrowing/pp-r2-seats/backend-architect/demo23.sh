#!/usr/bin/env bash
# demo23.sh HOOK : (M2) printed deadline for a remaining time of 2.05 s; (M3) can the here-string loop of _sg_vx_big_judge run zero times?
H=$1
source "$H" </dev/null >/dev/null 2>&1
set +e
# M2: P0 such that exactly ~2.05 s are left (cap 3, anchor 0.95 s ago)
SECRET_GUARD_TIME_BUDGET_S=3
_SG_P0=$(awk -v e="$EPOCHREALTIME" 'BEGIN{sub(",",".",e); printf "%.6f", e-0.95}')
_sg_relax_left; echo "M2 probe: remaining time printed as [$_SG_LEFT] (true value about 2.05)"
# M3: does the line-length loop run when the descriptor table is exhausted?
awk '/^declare -a risky_patterns=\(/,/^\)$/' "$H" > rp.tmp; awk '/^_sg_judge_one\(\) \{/,/^\}$/' "$H" > jo.tmp; awk '/^_sg_redact_echo\(\) \{/,/^\}$/' "$H" > re.tmp
source rp.tmp; source jo.tmp; source re.tmp
z=$(printf '%*s' 9000 '' | tr ' ' z); cfg="/etc/forg""ejo/app"".ini"
cf="cat $cfg | wc -c $z"       # a credential-path read WITH a value-redacting filter on one line > 8192
command="$cf"
( _sg_vx_big_judge "$cf" whole >/dev/null 2>&1; echo "M3 normal fds: big_judge rc=$? (2 = blocked by rows only)" )
( ulimit -n 3; { _sg_vx_big_judge "$cf" whole >/dev/null 2>&1; echo "M3 ulimit -n 3: big_judge rc=$?" >&3; } 3>&2 2>/dev/null ) 2>&1 | head -3
