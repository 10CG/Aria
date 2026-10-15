#!/usr/bin/env bash
# the document-sync bad implementations (patch_docs.py flags) of the final campaign; see docvariants5.py
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v5
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
python3 proto/docvariants5.py --jobs 3 > mut/final5/doc.log 2>&1
echo "doc done $(date +%T)" >> mut/final5/campaign.log
