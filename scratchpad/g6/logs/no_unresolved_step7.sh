[ -d aria/skills ] || { echo "UNVERIFIED — aria/skills 不存在 (子模块未检出?), 无法判定"; exit 1; }
HITS=$(grep -rn '<vNEXT>' aria/ --include='*.md' --include='*.json' --include='*.yaml' --include='*.py')
RC=$?
case $RC in
  1) echo "OK (aria/ 交付面无 <vNEXT> 占位符)"; exit 0 ;;
  0) echo "UNRESOLVED — $(printf '%s\n' "$HITS" | wc -l) 处 <vNEXT>, 首处: $(printf '%s\n' "$HITS" | head -1)"; exit 1 ;;
  *) echo "UNVERIFIED — grep 退出码 $RC, 扫描没跑成"; exit 1 ;;
esac
