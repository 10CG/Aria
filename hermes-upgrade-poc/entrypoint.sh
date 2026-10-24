#!/bin/bash
# hermes-upgrade-poc entrypoint — P2a/P3/P4 判据顺序执行, 每步独立 verdict 行,
# 单步失败不拖垮后续 (不 set -e)。结果同时落 /root/poc-verdicts.txt。
set -u
V=/root/poc-verdicts.txt
: > "$V"
verdict() { echo "$1" | tee -a "$V"; }

echo "=== P0 环境 ==="
hermes --version
python --version

# ---------- P2a: feishu adapter, webhook 传输, 无伤自证 ----------
# dummy 凭据: 只验证 adapter 装载 + webhook 监听 + url_verification challenge
# 应答 (飞书协议握手), 全程 127.0.0.1, 不触真实飞书 app, 不碰现役 WS。
export FEISHU_APP_ID="cli_poc_dummy"
export FEISHU_APP_SECRET="poc_dummy_secret"
export FEISHU_VERIFICATION_TOKEN="poc_vt_262"
export FEISHU_CONNECTION_MODE="webhook"
export FEISHU_WEBHOOK_HOST="127.0.0.1"
export FEISHU_WEBHOOK_PORT="8765"
export FEISHU_ALLOWED_USERS=""

echo "=== P2a: gateway run (webhook 模式, 后台) ==="
hermes gateway run -v > /tmp/gw.log 2>&1 &
GW=$!
sleep 20
grep -qi "feishu" /tmp/gw.log && echo "  adapter 装载: 日志含 feishu" || echo "  ⚠ 日志未见 feishu (继续探测端口)"
RESP=$(curl -s -m 10 -X POST http://127.0.0.1:8765/feishu/webhook \
  -H 'Content-Type: application/json' \
  -d '{"type":"url_verification","challenge":"poc-challenge-262","token":"poc_vt_262"}' || true)
echo "  challenge resp: $RESP"
echo "$RESP" | grep -q "poc-challenge-262" \
  && verdict "P2a-PASS: feishu adapter webhook 应答 url_verification challenge" \
  || verdict "P2a-FAIL: challenge 未回显 (resp=$RESP; gw.log 尾: $(tail -3 /tmp/gw.log | tr '\n' ' '))"

# ---------- P3: cron 真跑 (确定性, 零 token) ----------
echo "=== P3: cron create + tick ==="
hermes cron create --name poc-tick --no-agent --script poc-tick.sh '*/1 * * * *' 'poc deterministic tick' 2>&1 | tail -2
hermes cron tick 2>&1 | tail -3
sleep 3
# 注: `cron runs` 无 --name 过滤 (首跑实测), 全表 grep 本 job 的 completed
RUNS=$(hermes cron runs 2>/dev/null || true)
echo "$RUNS" | grep -qi "completed" \
  && verdict "P3-PASS: cron 真跑产生 completed 运行记录" \
  || verdict "P3-FAIL: 未见运行记录 ($RUNS)"

# ---------- P4: claude -p dispatch 冒烟 (luxeno 路由) ----------
echo "=== P4: claude -p ==="
if command -v claude >/dev/null 2>&1; then
  P4=$(timeout 120 claude -p 'Reply with exactly: P4-OK' 2>&1 | tail -3)
  echo "  claude said: $P4"
  echo "$P4" | grep -q "P4-OK" \
    && verdict "P4-PASS: claude -p 经 luxeno 路由应答" \
    || verdict "P4-FAIL: claude -p 未得预期应答 ($P4)"
else
  verdict "P4-SKIP: claude CLI 未装进镜像 (install.sh 失败, 需排查网络)"
fi

# ---------- 汇总 ----------
verdict "=== VERDICTS ==="
cat "$V"
echo "=== PoC 循环驻留 (cron 自然 tick 可观察; 手动复跑判据: docker/exec entrypoint) ==="
exec tail -f /dev/null
