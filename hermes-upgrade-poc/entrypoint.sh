#!/bin/bash
# hermes-upgrade-poc entrypoint — P2b: 真实 feishu WS 实连 (Aria #262 最后一格)
# 凭据来自 template env (nomad var nomad/jobs/hermes-upgrade-poc, 测试 app)。
set -u
V=/root/poc-verdicts.txt
: > "$V"
verdict() { echo "$1" | tee -a "$V"; }

echo "=== P0 环境 ==="
hermes --version
echo "app: ${FEISHU_APP_ID:-MISSING} | mode: ${FEISHU_CONNECTION_MODE:-unset}"

# P2b: WS 长连 (真实飞书)
export FEISHU_CONNECTION_MODE="websocket"
echo "=== P2b: gateway run (websocket 实连) ==="
hermes gateway run -v -v > /tmp/gw.log 2>&1 &
GW=$!

# 连接判定: 90s 窗口等 wss 连接日志
CONNECTED=""
for i in $(seq 1 18); do
  sleep 5
  LINE=$(grep -i "connected to wss\|websocket.*connect\|feishu.*started" /tmp/gw.log | tail -1)
  [ -n "$LINE" ] && { CONNECTED="$LINE"; break; }
done
[ -n "$CONNECTED" ] \
  && verdict "P2b-CONNECTED-PASS: $CONNECTED" \
  || verdict "P2b-CONNECTED-FAIL: 90s 未见 WS 连接日志 (gw.log 尾: $(tail -5 /tmp/gw.log | tr '\n' ' ' | head -c 200))"

# 消息往返监控: 等 owner DM 测试 bot; 收到 receive + 后续 send/reply 即 PASS
verdict "P2b-WAITING-DM: 请给测试 bot 发一条私信 (观察中, 无超时)"
SEEN=0
LAST_MARK=0
while :; do
  sleep 5
  NEW=$(tail -n +$((LAST_MARK+1)) /tmp/gw.log 2>/dev/null)
  LAST_MARK=$(wc -l < /tmp/gw.log)
  if [ -n "$NEW" ]; then
    echo "$NEW" | grep -iE "receive|message.*from|open_id|send|reply" | grep -v "^$" | head -5
    echo "$NEW" | grep -qiE "open_id|message.*receive" && [ "$SEEN" = "0" ] && {
      SEEN=1
      verdict "P2b-RECEIVED: 收到入站消息 (见上日志, open_id 已捕获)"
    }
    if [ "$SEEN" = "1" ] && echo "$NEW" | grep -qiE "send|reply|respond"; then
      verdict "P2b-PASS: feishu WS 实连 + 消息收发往返全通"
      break
    fi
  fi
done
verdict "=== P2b DONE ==="
exec tail -f /dev/null
