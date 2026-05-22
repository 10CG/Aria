# Aria 2.0 M5 — Phase C playbook (Layer 2 image + Tier-1 live LLM + Feishu secret)

> **Status**: Owner-runnable — 填补 `2026-05-20-m5-deploy-playbook-v2-accurate.md` §Phase C 缺失的 step-by-step
> **Authority**: 2026-05-22 light-1 实地 SSH 侦察 (read-only, Rule #7 compliant) + decision §2.5 + aria-build-README + aria-runner Dockerfile
> **Predecessor**: `2026-05-20-m5-deploy-playbook-v2-accurate.md` (Phase A + B 已执行完毕)
> **Scope**: 3 个 owner gate (O1 / O2 / O3) + Phase D.2 close
> **Created**: 2026-05-22 by AI recon

---

## §0 Prod state snapshot (2026-05-22 实地核实)

| 项 | 实测值 |
|----|--------|
| `/root/Aria` (light-1) | `244151e` on `master` (M5 Phase A era — Phase B 从此 deploy;现 master 已更新,prod 未跟) |
| `aria-orchestrator` alloc | `d43c2a7e` running, healthy (Hermes,走 Luxeno) |
| `aria-build` | service running (alloc `7ae8ecff`, 18d uptime, 历史 23 次成功 build) |
| `aria-layer1-comment-poll` | Nomad periodic, running (60s tick) |
| `aria-layer1-reconcile` / `-cron` | **不在 Nomad job 列表** — 见 §4 待核实 #1 |
| `aria-layer2-runner` | **未注册** — Phase C O2 要注册 |
| 当前 aria-runner 镜像 | `m1-handoff.yaml::image_sha_final = 5154c13` (M1 镜像 `claude-m1-5154c13-v9`) — Phase C 要 rebuild |
| Layer 2 HCL | `aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl` + `aria-runner-template.hcl` 存在 |
| Layer 2 Dockerfile | `aria-orchestrator/docker/aria-runner/Dockerfile` |

---

## §O1 — FEISHU_APP_SECRET 轮换 (owner-runnable,**独立,可现在做**)

> 出处:`.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md §2.5`。因 Lark WebSocket `access_key`/`ticket` 间接 leak,`FEISHU_APP_SECRET` 轮换紧迫性升级。重建 Feishu app 会同时换发 4 个 FEISHU_* key。
> **与 O2/O3 无依赖** — 这件事可以独立、最先做。

**Step 1 — Feishu 开发者后台 (~30-45min)**
1. 登录飞书开放平台 → 找到 Hermes 用的 app
2. **删除现有 app → 重建** → 拿到新的 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_VERIFICATION_TOKEN` / `FEISHU_ENCRYPT_KEY`
3. ⚠️ **APP_ID 也会变** → callback URL / event 订阅 / 机器人权限需在新 app 重新配置
4. secret 值**不要**粘进任何对话/聊天 (Rule #7) — 直接在下一步落盘

**Step 2 — light-1 改写 `/root/.hermes/.env`**
```bash
ssh light-1
# Rule #7: 用 heredoc + 显式 redirect 改写,不要用 nano/vim (会留 swap 文件)
# 先备份当前 .env (与 §S6 的 .env.bak-* 同机制)
cp /root/.hermes/.env /root/.hermes/.env.bak-feishu-rotate-$(date -u +%Y%m%dT%H%M%S)
# 改写 4 个 FEISHU_* 键 — 在 owner 本地编辑后整体 heredoc 写入,
# 或逐键用 `sed -i` (注意 sed 也别把值 echo 到 stdout)
```
> 具体改哪几行:`/root/.hermes/.env` 里所有 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_VERIFICATION_TOKEN` / `FEISHU_ENCRYPT_KEY`。改完 `grep -c FEISHU /root/.hermes/.env` 确认键数不变 (不读值)。

**Step 3 — Hermes restart**
```bash
ssh light-1 'export PATH=$PATH:/usr/local/bin; nomad job restart aria-orchestrator; sleep 30; nomad job status aria-orchestrator | tail -6'
# 确认新 alloc running
```

**Step 4 — 验证**
- 等 aria-heartbeat 下一次 cron tick (或 `hermes cron run` 手动触发) → 确认仍能成功投递 Feishu 通知
- Hermes gateway.log 应出现新的 Lark WS 连接 (新 access_key)

**Step 5 — 更新决策记录**
- `.aria/decisions/2026-05-02-*` (deferral decision) 把 `FEISHU_APP_SECRET` + `FEISHU_VERIFICATION_TOKEN` + `FEISHU_ENCRYPT_KEY` 状态改 `Resolved 2026-05-22`(重建 app 一并轮换);仅 `GLM_API_KEY` 仍 deferred(且已因 Hermes→Luxeno 弃用,见 §4 待核实 #3)

---

## §O2 — Layer 2 aria-runner 镜像 build + push (owner + aria-build 容器)

> 目标:rebuild aria-runner 镜像(含 Spec X+Y 的 Layer 2 changes/redo mode 代码)→ push forgejo registry → 更新 `m1-handoff.yaml`。
> aria-build 是常驻 build 容器(docker.sock 挂载 + entrypoint 自动 `docker login` forgejo)。

**Step 1 — 确定构建 ref + tag** ⚠️ 需 owner 确认
- v2-accurate playbook 写的 tag 是 `claude-m5-carry-09ff364-v11`(`09ff364` = aria-orchestrator Spec Y T8 merge)
- 当前 aria-orchestrator master = `91b8975` ("docs(m5-handoff): Phase B done")
- **决策点**:从 `09ff364` 还是当前 master `91b8975` build?建议 master(含最新 m5-handoff + 任何 post-Spec-Y 修正)。tag 相应改 `claude-m5-91b8975-v11` 或保留 playbook 的 `-09ff364-`。

**Step 2 — exec 进 aria-build 容器**
```bash
ssh light-1   # 或任一能到 Nomad 的节点
export PATH=$PATH:/usr/local/bin
ALLOC=$(nomad job status aria-build | awk '/running/{print $1; exit}')
nomad alloc exec -task build -i -t "$ALLOC" /bin/sh
# 容器内:确认已登录 — cat ~/.docker/config.json | jq '.auths|keys' → ["forgejo.10cg.pub"]
```

**Step 3 — 容器内 clone Aria 仓 (含 submodule) 并 build**
> aria-runner Dockerfile **必须从 Aria 仓库根目录** build(`COPY aria/` 烤入 aria-plugin + `COPY aria-orchestrator/docker/aria-runner/`)。
```sh
# 容器内 shell — 用 FORGEJO_BOT_PAT clone (env 已注入)
cd /tmp && rm -rf Aria-build && \
  git clone --recurse-submodules https://forgejo.10cg.pub/10CG/Aria.git Aria-build   # ⚠️ VERIFY: clone 是否需 PAT 凭据 — 见 §4 待核实 #2
cd Aria-build
# checkout 目标 ref (Step 1 决定);默认 master 已是最新
git submodule update --init --recursive

# build (Dockerfile L13-16 钦定命令 — 从仓库根目录 + -f 指定 Dockerfile)
docker build -f aria-orchestrator/docker/aria-runner/Dockerfile \
  --build-arg DEPLOY_ENV=internal \
  -t forgejo.10cg.pub/10CG/aria-runner:claude-m5-carry-09ff364-v11 .

# 双 tag (AD-M1-2: immutable + mutable)
docker tag forgejo.10cg.pub/10CG/aria-runner:claude-m5-carry-09ff364-v11 \
           forgejo.10cg.pub/10CG/aria-runner:claude-latest

# push 两个 tag
docker push forgejo.10cg.pub/10CG/aria-runner:claude-m5-carry-09ff364-v11
docker push forgejo.10cg.pub/10CG/aria-runner:claude-latest

# 记下 image digest (更新 m1-handoff.yaml 用)
docker inspect --format='{{index .RepoDigests 0}}' \
  forgejo.10cg.pub/10CG/aria-runner:claude-m5-carry-09ff364-v11
exit
```

**Step 4 — 更新 `m1-handoff.yaml`**
在 `aria-orchestrator/docs/m1-handoff.yaml` 改:
- `image_sha_final:` → 新构建 ref 短 sha
- `image_sha256_final:` → Step 3 拿到的 `sha256:...` digest
- `image_history:` 追加 final_tag = `claude-m5-carry-09ff364-v11`
> 这是一个 commit(aria-orchestrator 子模块 + 主仓 submodule bump),走正常 Phase C 提交流程。

**Step 5 — 注册 `aria-layer2-runner` parameterized template**
```bash
ssh light-1 'export PATH=$PATH:/usr/local/bin; cd /root/Aria/aria-orchestrator/nomad/jobs && \
  nomad job validate aria-layer2-runner.hcl && nomad job run aria-layer2-runner.hcl && \
  nomad job status aria-layer2-runner | head -10'
```
> ⚠️ 前提:prod `/root/Aria` 需先更新到含最新 HCL 的 ref(现停在 `244151e`)。`aria-runner-template.hcl` 与 `aria-layer2-runner.hcl` 的关系、HCL 里的 image tag 是否引用 `claude-latest` — 见 §4 待核实 #4。

---

## §O3 — Tier-1 live LLM gate + Layer 2 real smoke (owner 触发,~¥0.10)

> 用**真实 Layer 2 dispatch** 替换 Phase B 的合成 SQL-inject Smoke A/B/C。

**Step 1 — Layer 2 real dispatch smoke**(B.1.live / C.2.live)
```bash
# Nomad dispatch 一个真实 issue 到 aria-layer2-runner
ssh light-1 'export PATH=$PATH:/usr/local/bin; nomad job dispatch -meta ISSUE_ID=<test-issue> aria-layer2-runner'
```
- 验证三类 Layer 2 行为:force-push / close-old-PR / commit-lint retry
- 这会触发真实 LLM 调用(claude-code in container)→ 实际花费 ~¥0.10
> ⚠️ 具体 test issue 选择、dispatch meta 参数、预期产物验证 — 见 §4 待核实 #5。

**Step 2 — 观测 + 验收**
- `nomad alloc logs` 看 runner 执行
- 确认 issue → PR 闭环成功;Layer 1 dispatch 记录正确写 `dispatches.db`

**Step 3 — Tier-2 累积**(被动)
- O4:Tier-2 需 N≥3 真实 dispatch 累积 — 随 owner 日常 workload 自然攒,不是单次动作

---

## §Phase D.2 — close (O1+O2+O3 完成后,AI-runnable)

- 勾 M5 Spec `tasks.md` 6.21.1 (verify aria-runner-template stub alloc) + 6.27-6.30 (Tier-2 累积型验收)
- `m5-handoff.yaml::go_decision` 从 `<pending>` 改 final Go
- 归档 M5 proposal.md → `openspec/archive/{date}-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/`
- US-025 状态 → done
- 写 M5 closeout handoff

---

## §S6 — 时间敏感 hygiene(与 close gate 无关)

`/root/.hermes/.env` 的 3 个 `.env.bak-*`(含旧死 key):Hermes→Luxeno 重定向 ~2026-05-21 11:26 UTC + 24h = **~2026-05-22 11:26 UTC 之后**可 `shred`。注:O1 Step 2 又会新增一个 `.env.bak-feishu-rotate-*`,那个保留到 O1 验证稳定后再清。

---

## §4 待核实项(执行前需 owner 或下一 recon session 确认)

| # | 项 | 为什么 |
|---|----|--------|
| 1 | Layer 1 `reconcile`/`cron` 是 Hermes-internal 还是漏部署 | recon 显示它们不在 Nomad job 列表,但 2026-05-21 handoff §5 称 "running"。若 OD-2 当初选 (a) Hermes-internal 则正常;否则 Phase B 不完整需补 |
| 2 | aria-build 容器内 clone Aria 仓的凭据 | README 只证实容器有 docker push 的 FORGEJO_BOT_PAT;`git clone` 私仓是否复用同 PAT 需实测(`https://<user>:<pat>@forgejo...` 或 SSH key) |
| 3 | `GLM_API_KEY` 现状 | Hermes 已重定向 Luxeno,旧 Z.AI GLM_API_KEY 是 orphan;O1 Step 5 更新 deferral 时确认是否一并标弃用 |
| 4 | `aria-layer2-runner.hcl` / `aria-runner-template.hcl` 内容 | 注册前需 review:image tag 引用方式(`claude-latest` 还是 pinned sha)、parameterized meta 字段、prod `/root/Aria` 需先更新 |
| 5 | O3 real smoke 的 test issue + dispatch 参数 + 预期产物 | v2-accurate playbook §Phase C 只给 scope,未给具体 dispatch 脚本;v11 addendum Step 5(real)有雏形但已 SUPERSEDED |

> 建议:O1 可立即独立执行。O2 执行前先 SSH 把 §4 #2 #4 核实掉(~15min recon)。O3 在 O2 完成后单独 session。

---

## §Rollback

| 失败 | Rollback |
|------|----------|
| O1 Hermes 起不来 | `cp /root/.hermes/.env.bak-feishu-rotate-* /root/.hermes/.env` + restart |
| O2 docker build 失败 | 无 prod 影响(build 在隔离容器);查 aria-build-README §故障排查 |
| O2 push 401 | FORGEJO_BOT_PAT 过期 → 按 aria-build-README §PAT 轮换流程 |
| O3 smoke 失败 | 记入 m5-handoff.yaml,**不**推 Phase D.2 final Go;Layer 2 image 可保留(rollback-friendly) |

---

**Created**: 2026-05-22 ~02:30 UTC by AI(light-1 实地侦察 grounded)
**Authority**: 补全 v2-accurate playbook 缺失的 §Phase C;§0 prod snapshot 实测,§O2 build 命令引自 aria-runner Dockerfile L13-16
**Cross-refs**: `2026-05-20-m5-deploy-playbook-v2-accurate.md` · `.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md §2.5` · `aria-orchestrator/nomad/jobs/aria-build-README.md`
