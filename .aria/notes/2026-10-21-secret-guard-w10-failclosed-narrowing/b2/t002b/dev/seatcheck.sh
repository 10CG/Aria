#!/usr/bin/env bash
# seatcheck.sh : for every seat mutant folded into BI-24.. (and BI-17b), the changed lines of (seat mutant vs its v3.1 prototype) equal the changed lines of
# (BI vs the implementation). Prints one line per seat mutant.
S=$1; R=$2; P=$S/work/proto.sh; I=$S/work/impl.sh
chg() { diff -U0 "$1" "$2" | grep -E '^[-+]' | grep -vE '^(\+\+\+|---) '; }
while read -r bi seat file; do
  a=$(chg "$P" "$R/$file"); b=$(chg "$I" "$S/dev/mut/$bi.sh")
  if [[ "$a" == "$b" ]]; then echo "SAME   $bi $seat"; else echo "DIFF   $bi $seat"; diff <(printf '%s\n' "$a") <(printf '%s\n' "$b") | head -6 | cut -c1-160; fi
done <<'T'
BI-17b CR-MB code-reviewer/mut/MB.sh
BI-17b QA-M12 qa-engineer/mut/M12.sh
BI-17b TL-M1 tech-lead/mut/TL-M1.sh
BI-24 CR-MA code-reviewer/mut/MA.sh
BI-25 QA-M02 qa-engineer/mut/M02.sh
BI-26 QA-M01 qa-engineer/mut/M01.sh
BI-26 TL-M8 tech-lead/mut/TL-M8.sh
BI-26 BA-M1 backend-architect/mut/M1.sh
BI-27 QA-M24 qa-engineer/mut/M24.sh
BI-28 QA-M06 qa-engineer/mut/M06.sh
BI-29 QA-M07 qa-engineer/mut/M07.sh
BI-30 QA-M08 qa-engineer/mut/M08.sh
BI-31 BA-M8 backend-architect/mut/M8.sh
BI-32 TL-M5 tech-lead/mut/TL-M5.sh
BI-33 CR-MC code-reviewer/mut/MC.sh
BI-33 BA-M4 backend-architect/mut/M4.sh
BI-34 TL-M2 tech-lead/mut/TL-M2.sh
BI-35 CR-MD code-reviewer/mut/MD.sh
BI-35 TL-M3 tech-lead/mut/TL-M3.sh
BI-35 BA-M11 backend-architect/mut/M11.sh
BI-36 QA-M10 qa-engineer/mut/M10.sh
BI-37 QA-M28 qa-engineer/mut/M28.sh
BI-37 TL-M4 tech-lead/mut/TL-M4.sh
BI-38 QA-M18 qa-engineer/mut/M18.sh
BI-38 BA-M9 backend-architect/mut/M9.sh
BI-39 QA-M17 qa-engineer/mut/M17.sh
BI-40 BA-M10 backend-architect/mut/M10.sh
BI-41 BA-M7 backend-architect/mut/M7.sh
BI-42 QA-M20 qa-engineer/mut/M20.sh
BI-43 QA-M30 qa-engineer/mut/M30.sh
BI-44 QA-M04 qa-engineer/mut/M04.sh
BI-44 BA-M14 backend-architect/mut/M14.sh
BI-45 QA-M09 qa-engineer/mut/M09.sh
BI-45 BA-M5 backend-architect/mut/M5.sh
BI-46 QA-M13 qa-engineer/mut/M13.sh
BI-46 TL-M9 tech-lead/mut/TL-M9.sh
BI-46 BA-M6 backend-architect/mut/M6.sh
BI-47 QA-M14 qa-engineer/mut/M14.sh
BI-48 BA-M3 backend-architect/mut/M3.sh
BI-49 QA-M15 qa-engineer/mut/M15.sh
BI-50 BA-M2 backend-architect/mut/M2.sh
BI-51 KM-M1 knowledge-manager/km-m1.sh
BI-52 KM-M2 knowledge-manager/km-m2.sh
BI-53 KM-M3 knowledge-manager/km-m3.sh
BI-54 KM-M6 knowledge-manager/km-m6.sh
T
