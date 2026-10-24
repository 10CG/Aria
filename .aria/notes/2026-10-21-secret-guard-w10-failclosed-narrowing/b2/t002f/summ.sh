#!/usr/bin/env bash
# summ.sh <suite output>: the six groups' summary part, the FAIL ids, and per failing group of the six: command prefixes, walls, Tb', verdict words
f=$1
echo "== ${f##*/}: lines with 'FAIL [' $(grep -c 'FAIL \[' "$f")"
grep 'W10 older groups' "$f" | sed 's/.*| deadline fallback/deadline fallback/'
grep -o 'FAIL \[[^]:]*' "$f" | sed 's/FAIL \[//; s/ bf.*//' | sort | tr '\n' ','; echo
grep 'FAIL \[W10 SC-21a' "$f" | while IFS= read -r l; do
  g=$(grep -o 'SC-21a[a-z]' <<<"$l" | head -n 1)
  echo "$g: $(grep -o "{Bash [^:]\{0,22\}\|wall [0-9.]*s\|Tb' [0-9.]*s\|want [^)]*\|这么早结束\|是准入门提前关\|wall under 2.85" <<<"$l" | tr '\n' ' ')"
done
tail -n 1 "$f"
