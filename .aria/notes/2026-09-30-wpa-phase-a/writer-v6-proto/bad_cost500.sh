#!/usr/bin/env bash
# bad_cost500.sh -- total CPU of each bad value-extraction variant on the 500 KB member it is meant to be caught by (the "8 s or more" statement of the SC-34 members); output out/bad_cost500.txt
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
mkdir -p work/vh
{
  echo "== bad value-extraction variants, one 500 KB member each, TOTAL cpu (hook + children), load $(cut -d' ' -f1-3 /proc/loadavg) $(date +%T)"
  for pair in val_quote_strip:kv-eq val_quote_strip:kv-export val_quote_strip:kv-yaml val_kv_blank:kv-blank-before-eq val_json_colon:json-blank-before-colon val_url_at:pg-long-password val_url_at:pg-long-user val_url_at:basicauth-long val_envline_eq:envline-long-key; do
    v=${pair%%:*}; shape=${pair##*:}
    mkdir -p work/vh/$v
    [ -f work/vh/$v/secret-scan.sh ] || python3 proto/patch_l3.py base/aria/hooks/secret-scan.sh work/vh/$v/secret-scan.sh --variant $v > /dev/null
    echo "-- $v"
    python3 proto/scale_try.py work/vh/$v/secret-scan.sh $shape 500 2>&1 | tail -1
  done
  echo "-- target (for comparison)"
  for shape in kv-eq kv-export kv-yaml kv-blank-before-eq json-blank-before-colon pg-long-password pg-long-user basicauth-long envline-long-key; do
    python3 proto/scale_try.py work/t6/aria/hooks/secret-scan.sh $shape 500 2>&1 | tail -1
  done
  echo "== done $(date +%T)"
} > out/bad_cost500.txt 2>&1
