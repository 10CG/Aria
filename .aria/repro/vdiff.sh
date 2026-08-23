#!/bin/bash
# TASK-024 整仓差集 (行级, 按类排除). 用法: vdiff.sh <OLD>
OLD="$1"; cd /home/dev/Aria
DIRS='^(aria/VERSION|aria/CHANGELOG\.md|\.aria/audit-reports/|\.aria/decisions/|\.aria/notes/|\.aria/repro/archive/|docs/handoff/|docs/decisions/|openspec/archive/|openspec/changes/|aria-plugin-benchmarks/ab-results/)'
ANNOT="${OLD//./\\.}\+|\"_(comment|description|ships_with)\""
echo "[main]"; git grep -nF "$OLD" | grep -vP "$DIRS" | grep -vP "$ANNOT"
echo "[aria]"; git -C aria grep -nF "$OLD" | grep -vP '^(VERSION|CHANGELOG\.md):' | grep -vP "$ANNOT"
echo "[end]"
