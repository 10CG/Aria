#!/usr/bin/env bash
# seed-aria-auto-issues.sh — B4-label: 为 M6 168h E2E 跑造分层的 aria-auto dispatch 语料
#
# 作用:
#   1. 确保 type 标签存在 (feature/stale 缺则创建; aria-auto/bug 已存在)
#   2. 造 N 个 [DEMO-M6-P*] 合成 issue, 轮流打 bug/feature/stale + aria-auto
#      → tick (aria-layer1-cron) 下个整点起会 dispatch 它们
#      → 配合 PR #28 (issue_type_hint 写入) 满足 AC-2 (≥10 S9_CLOSE, ≥1 每类型)
#
# 用法:
#   ./seed-aria-auto-issues.sh            # dry-run (只打印, 不创建)
#   ./seed-aria-auto-issues.sh --apply    # 真创建
#   COUNT=12 ./seed-aria-auto-issues.sh --apply
#
# 依赖: forgejo CLI wrapper (/home/dev/.npm-global/bin/forgejo)
# 前置: PR #28 已 merge + 部署到 light-1 (否则 dispatch 不带 issue_type_hint, AC-2 分层仍失败)
#
# 清理 (跑完 168h 后): 这些 [DEMO-M6-P*] issue 应关闭/删除, 避免污染真实 backlog。
set -euo pipefail

REPO="${REPO:-10CG/Aria}"
COUNT="${COUNT:-12}"          # ≥10 (AC-2 要 ≥10 S9_CLOSE); 12 给失败留冗余
FORGEJO="${FORGEJO:-/home/dev/.npm-global/bin/forgejo}"
APPLY=0; [ "${1:-}" = "--apply" ] && APPLY=1
TYPES=(bug feature stale)

say() { printf '%s\n' "$*" >&2; }
run() { if [ "$APPLY" = 1 ]; then "$@"; else say "[dry-run] $*"; fi; }

# --- 1. 解析现有标签 name→id ---
say "== 解析 $REPO 标签 =="
LABELS_JSON=$("$FORGEJO" GET "/repos/$REPO/labels" 2>/dev/null)
label_id() { printf '%s' "$LABELS_JSON" | python3 -c "import json,sys;d=json.load(sys.stdin);n='$1';print(next((str(l['id']) for l in d if l['name']==n),''))"; }

# --- 2. 确保 feature/stale 存在 ---
ensure_label() {
  local name="$1" color="$2" id
  id=$(label_id "$name")
  if [ -n "$id" ]; then say "  label '$name' 已存在 (id=$id)"; return; fi
  if [ "$APPLY" = 1 ]; then
    say "  创建 label '$name'"
    "$FORGEJO" POST "/repos/$REPO/labels" -d "{\"name\":\"$name\",\"color\":\"$color\"}" >/dev/null
    LABELS_JSON=$("$FORGEJO" GET "/repos/$REPO/labels" 2>/dev/null)   # 刷新
  else
    say "  [dry-run] 将创建 label '$name' (color $color)"
  fi
}
ensure_label feature "#0e8a16"
ensure_label stale   "#fbca04"

ARIA_AUTO_ID=$(label_id aria-auto)
[ -z "$ARIA_AUTO_ID" ] && { say "ERROR: aria-auto 标签不存在且未创建"; exit 1; }
say "  aria-auto id=$ARIA_AUTO_ID"

# --- 3. 造 N 个分层合成 issue ---
say "== 造 $COUNT 个 [DEMO-M6-P*] aria-auto issue (轮流 ${TYPES[*]}) =="
declare -A TYPE_ID
for t in "${TYPES[@]}"; do TYPE_ID[$t]=$(label_id "$t"); done

for i in $(seq 1 "$COUNT"); do
  t="${TYPES[$(( (i-1) % ${#TYPES[@]} ))]}"
  tid="${TYPE_ID[$t]}"
  if [ "$APPLY" = 1 ]; then
    [ -z "$tid" ] && tid=$(label_id "$t")   # apply 模式下 ensure 后已存在
  fi
  title="[DEMO-M6-P$i] synthetic dispatch fixture ($t)"
  body="M6 168h E2E run 合成 dispatch 语料 (type=$t)。跑完后关闭/删除以免污染 backlog。"
  payload=$(python3 -c "import json;print(json.dumps({'title':'''$title''','body':'''$body''','labels':[int('$ARIA_AUTO_ID'),int('${tid:-0}')]}))")
  if [ "$APPLY" = 1 ]; then
    num=$("$FORGEJO" POST "/repos/$REPO/issues" -d "$payload" | python3 -c "import json,sys;print(json.load(sys.stdin).get('number'))")
    say "  创建 #$num: $title"
  else
    say "  [dry-run] 将创建: $title  labels=[aria-auto:$ARIA_AUTO_ID, $t:${tid:-<新建后取>}]"
  fi
done

say "== 完成 =="
say "下一步: 等 aria-layer1-cron 下个整点 (或 nomad job periodic force aria-layer1-cron),"
say "        查 dispatches.db {\"processed\":N} N>0 + AC-2 分层 (PR #28 部署后 issue_type_hint 才写入)。"
