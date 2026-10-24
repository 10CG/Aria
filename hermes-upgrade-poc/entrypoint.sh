#!/bin/bash
# hermes-upgrade-poc entrypoint — P2b v2 (全量日志, 无过滤, allow-all)
# 差分修正: 生产工作配置 GATEWAY_ALLOW_ALL_USERS=true (空 allowlist 时 hermes 0.19
# 的 DM 走 pairing fail-close — v1 沉默的头号嫌疑); 本版镜像生产选择器。
set -u
V=/root/poc-verdicts.txt
: > "$V"
verdict() { echo "$1" | tee -a "$V"; }

echo "=== P0 环境 ==="
hermes --version
echo "app: ${FEISHU_APP_ID:-MISSING} | domain: ${FEISHU_DOMAIN:-unset} | allow_all: ${GATEWAY_ALLOW_ALL_USERS:-unset}"

export FEISHU_CONNECTION_MODE="websocket"
echo "=== P2b-v2: gateway run (websocket + allow-all) — 全量日志尾随, 不过滤 ==="
hermes gateway run -v -v > /tmp/gw.log 2>&1 &
GW=$!
tail -f /tmp/gw.log &
TAILER=$!

for i in $(seq 1 18); do
  sleep 5
  grep -q "connected to wss" /tmp/gw.log && break
done
grep -q "connected to wss" /tmp/gw.log \
  && verdict "P2b-CONNECTED-PASS: $(grep 'connected to wss' /tmp/gw.log | tail -1 | head -c 100)" \
  || verdict "P2b-CONNECTED-FAIL: $(tail -3 /tmp/gw.log | tr '\n' ' ' | head -c 150)"

verdict "P2b-WAITING-DM (allow-all, 无 pairing 阻塞; 全量日志在上面实时滚动)"

# 宽松活动判定: 消息类动词出现即报 (不再用窄过滤)
while :; do
  sleep 5
  if grep -qiE "im\.message|message\.receive|send_message|reply|pairing|intake" /tmp/gw.log; then
    verdict "P2b-ACTIVITY: 消息类日志出现 (见上方全量日志)"
    sleep 15
    verdict "P2b-DONE: 请对照全量日志核对应答链路"
    break
  fi
done
exec tail -f /dev/null
