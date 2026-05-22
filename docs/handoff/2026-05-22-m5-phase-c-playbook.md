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
ssh light-1
export PATH=$PATH:/usr/local/bin
# aria-build alloc 实测 = 7ae8ecff (18d 常驻 service)。若变更,从 Allocations 表取
# running 那行的 ID (注意别用 awk '{8}' 区间 — light-1 是 mawk,不支持)
nomad alloc exec -task build -i -t 7ae8ecff /bin/sh
# 容器内确认已登录: cat ~/.docker/config.json | jq '.auths|keys' → ["forgejo.10cg.pub"]
```

**Step 3 — 取源 + build**

> ⚠️ **§4 #2 实测**:aria-build 容器的 `FORGEJO_BOT_PAT` 是 registry-scoped(或已过期),**不能 git clone 仓库**;且 forgejo.10cg.pub 集群内是自签证书(`git` 需 `-c http.sslVerify=false`)。下面两条取源路线 **owner 选一**。
> aria-runner Dockerfile **必须从 Aria 仓库根目录** build(`COPY aria/` + `COPY aria-orchestrator/docker/aria-runner/`)。

**路线 A — 给 bot 一个 repo-read PAT(推荐,一劳永逸)**
1. Forgejo:`aria-runner-bot` 账号 → PAT 加 `read:repository` scope(保留原 `write:package`)
2. `aether env set --job aria-build FORGEJO_BOT_PAT <new-pat>` → `nomad job restart aria-build`
3. 容器内 clone:
```sh
cd /tmp && rm -rf Aria-build
git -c http.sslVerify=false clone --recurse-submodules \
  "https://${FORGEJO_BOT_USER}:${FORGEJO_BOT_PAT}@forgejo.10cg.pub/10CG/Aria.git" Aria-build
cd Aria-build && git -c http.sslVerify=false submodule update --init --recursive
```

**路线 B — light-1 host 取源 tar-pipe 进容器(不动 PAT)**
> ⚠️ 别用 `/root/Aria` —— 它是 aria-layer1 的 editable install 源,改它会动到运行中的 Layer 1。在 host clone 独立 scratch:
```sh
# light-1 host (root 已有 forgejo git 凭据)
git clone --recurse-submodules <forgejo-Aria-url> /tmp/Aria-build-src
nomad alloc exec -task build 7ae8ecff mkdir -p /tmp/Aria-build
tar -C /tmp/Aria-build-src -cf - . | nomad alloc exec -i -task build 7ae8ecff tar -C /tmp/Aria-build -xf -
```

**build(两条路线汇合 — 容器内,从仓库根目录)**
```sh
cd /tmp/Aria-build
TAG=claude-m5-91b8975-v11   # Step 1 决定的 ref/tag
docker build -f aria-orchestrator/docker/aria-runner/Dockerfile \
  --build-arg DEPLOY_ENV=internal \
  -t "forgejo.10cg.pub/10CG/aria-runner:$TAG" .
docker tag "forgejo.10cg.pub/10CG/aria-runner:$TAG" forgejo.10cg.pub/10CG/aria-runner:claude-latest
docker push "forgejo.10cg.pub/10CG/aria-runner:$TAG"
docker push forgejo.10cg.pub/10CG/aria-runner:claude-latest
# 记下 sha256 digest — Step 4 更新 m1-handoff.yaml + Layer 2 dispatch IMAGE_SHA 用
docker inspect --format='{{index .RepoDigests 0}}' "forgejo.10cg.pub/10CG/aria-runner:$TAG"
exit
```

**Step 4 — 更新 `m1-handoff.yaml`**
在 `aria-orchestrator/docs/m1-handoff.yaml` 改:
- `image_sha_final:` → 新构建 ref 短 sha
- `image_sha256_final:` → Step 3 拿到的 `sha256:...` digest
- `image_history:` 追加 final_tag = `claude-m5-carry-09ff364-v11`
> 这是一个 commit(aria-orchestrator 子模块 + 主仓 submodule bump),走正常 Phase C 提交流程。

**Step 4.5 — 填 Nomad var `nomad/jobs/aria-layer2-runner`(注册前必须)**
`aria-layer2-runner.hcl` 的 `template` stanza 从此 var 渲染 secrets,不填 → runner 启动无凭据。8 keys(HCL header L244-252 钦定):
```bash
# Rule #7: 用 -in stdin / @file 传值,别在命令行明文 echo 密钥
nomad var put -in=json nomad/jobs/aria-layer2-runner <<'EOF'
{ "Items": {
  "FORGEJO_BOT_PAT": "...", "ANTHROPIC_API_KEY": "...",
  "ANTHROPIC_BASE_URL": "...", "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-4.5-air",
  "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.1", "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5-turbo",
  "ZHIPU_API_KEY": "...", "ZHIPU_BASE_URL": "https://open.bigmodel.cn/api/paas/v4" } }
EOF
nomad var get -out=keys nomad/jobs/aria-layer2-runner   # 验证 8 keys 在,不读值
```
> ⚠️ `ANTHROPIC_BASE_URL` + model alias **以 Luxeno 当前实际配置为准** —— HCL header 给的是 M3 草案值(`https://luxeno.ai/api`),与 aria-layer1 实际用的 `api.luxeno.ai/v1` 可能有出入,owner 核对。

**Step 5 — 注册 `aria-layer2-runner` parameterized template**
```bash
# HCL 源:用 Step 3 路线 B 的 /tmp/Aria-build-src (master 全量),或 scp 一份过来
# —— 别用 prod /root/Aria (停在 244151e,且 editable-install 耦合勿动)
ssh light-1 'export PATH=$PATH:/usr/local/bin; cd /tmp/Aria-build-src/aria-orchestrator/nomad/jobs && \
  nomad job validate aria-layer2-runner.hcl && nomad job run aria-layer2-runner.hcl && \
  nomad job status aria-layer2-runner | head -10'
```
> aria-layer2-runner.hcl 经 §4 #4 review 确认:job 是 batch+parameterized,image 在 **dispatch 时**用 `IMAGE_SHA` meta 做 sha-digest pin(注册时不需要 image 存在;dispatch 时才拉)。注册成功 = `nomad job status aria-layer2-runner` 显示 parameterized job 就绪。

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

## §4 核实项 (2026-05-22 SSH recon 已核实 #2/#3/#4)

| # | 项 | 状态 |
|---|----|------|
| 1 | Layer 1 `reconcile`/`cron` 是 Hermes-internal 还是漏部署 | ⏳ **未核实** — recon 显示不在 Nomad job 列表,2026-05-21 handoff §5 称 "running"。属 Phase B 完整性,不阻塞 O2 |
| 2 | aria-build 容器 clone 仓库能力 | ✅ **RESOLVED** — git 2.52.0 ✓ / docker 29.4.1 ✓ / 67.9G 磁盘 ✓ / FORGEJO_BOT_* env ✓。**但 `FORGEJO_BOT_PAT` 不能 git clone**(实测 "Credentials are incorrect or have expired" — registry-scoped 或已过期);且 forgejo.10cg.pub 集群内自签证书需 `http.sslVerify=false`。→ O2 取源见 §O2 Step 3 路线 A/B |
| 3 | `GLM_API_KEY` 现状 | ✅ **RESOLVED** — O1 Step 5 已处理:Z.AI 旧 key 经 Hermes→Luxeno 重定向架构性退役;`.env` 的 `GLM_API_KEY` var 现持 Luxeno key。旧 Z.AI 账户 owner 可自行注销(非紧急) |
| 4 | `aria-layer2-runner.hcl` 内容 | ✅ **RESOLVED** — job `aria-layer2-runner` (batch+parameterized);image **dispatch 时 sha-digest pin** (`@sha256:${NOMAD_META_IMAGE_SHA}`,非硬编码 tag);constraint `node.class==heavy_workload`。注册前**必须先填 Nomad var** `nomad/jobs/aria-layer2-runner` 8 keys(见 §O2 Step 4.5)。`aria-runner-template.hcl` 是 M1 legacy,不用它 |
| 5 | O3 real smoke 的 test issue + dispatch 参数 + 预期产物 | ⏳ **未核实** — v2-accurate playbook §Phase C 只给 scope;O3 单独 session 时再 ground |

> 建议:O1 已完成。O2 = Step 1→2→3(取源路线 A/B 选一)→4→4.5→5。O3 在 O2 完成 + Phase B 稳定 ≥24h 后单独 session。

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
