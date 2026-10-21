#!/bin/bash
# deadline-estimate.sh -- of the 138 real commands base v1.76.1 blocks with the W10 size text, how many would a hard deadline time-block
# once #217 judges them in full: total = base seconds (E12, first pass + collect) + full-judgement seconds (W1 judge_s); slow platforms by
# the E12 multipliers (Windows ~x2.6, bash 3.2 ~x4: rough, borrowed, not re-measured for #217). Every one of these is blocked by base anyway.
D=$(cd "$(dirname "$0")/../evidence" && pwd)
E=$D/../../2026-10-20-secret-guard-scan-cost-and-firstpass-cap/evidence/E12-base-all.tsv
awk -F'\t' 'NR==FNR{e[$1]=$3; next} ($1 ~ /^[0-9]+$/) && ($1 in e) {n++; t=e[$1]+$12; tot[n]=t; if(t>m)m=t}
END{printf "joined=%d (expected 138) max total on Linux=%.2fs\n", n, m; split("3 4",D," "); split("1 2.6 4",M," "); split("linux windows-x2.6 bash3.2-x4",L," ");
for(i=1;i<=3;i++) for(j=1;j<=2;j++){c=0; for(k=1;k<=n;k++) if(tot[k]*M[i]>D[j]) c++; printf "  %s, deadline %ss: %d of %d would be time-blocked\n", L[i], D[j], c, n}}' "$E" "$D/W1-classification.tsv"
