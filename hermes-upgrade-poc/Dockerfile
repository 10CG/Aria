# hermes-upgrade-poc — Aria #262: hermes 0.7.0 → 0.19.0 升级评估 PoC cell
#
# 判据 (P1-P5 详见 README.md; P1 已在 dev 容器实测过):
#   P2a feishu adapter webhook 模式 + url_verification challenge (无伤, 不碰现役 app)
#   P3  cron 真跑 (--no-agent --script 确定性 tick, 零 token)
#   P4  claude -p dispatch 冒烟 (luxeno 路由, 同现役凭据路)
#   P5  独立 job + 独立 hermes-home (容器内 /root/.hermes, 不挂 aria-layer1 卷)
#
# 构建: context = 本目录内容 + wheels/ (pip download 产物, 57MB/83 wheels,
#       hermes-agent[feishu,messaging]==0.19.0 双 extra 离线闭环已验证)。
#       aiohttp 属 messaging extra 而 feishu adapter webhook 模式要用它 — 上游
#       打包缺口, 双 extra 是绕法 (记录在 #262)。
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash curl git ca-certificates nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Claude Code CLI (P4 dispatch 目标): claude.ai/install.sh 跨境失败 (#262 首跑
# 实测) → 改走内网 Verdaccio (.206:4873) npm 镜像装 @anthropic-ai/claude-code
RUN npm config set registry http://192.168.69.206:4873 && \
    npm install -g @anthropic-ai/claude-code && \
    claude --version

# hermes 0.19.0 离线安装 (wheelhouse, 不依赖构建网络)
COPY wheels/ /tmp/wheels/
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-index --find-links=/tmp/wheels \
        "hermes-agent[feishu,messaging]==0.19.0" && \
    rm -rf /tmp/wheels && \
    /opt/venv/bin/hermes --version

# P1 产物: 0.7 config 迁移后 (v33), model 默认改 luxeno custom
# (PoC 无 zai key; zai 键存活已由 P1 在配置层证明)
COPY config.yaml /root/.hermes/config.yaml
COPY poc-tick.sh /root/.hermes/scripts/poc-tick.sh
RUN chmod +x /root/.hermes/scripts/poc-tick.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PATH=/opt/venv/bin:$PATH

CMD ["/entrypoint.sh"]
