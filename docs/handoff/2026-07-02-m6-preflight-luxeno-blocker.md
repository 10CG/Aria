---
track-id: m6-preflight-luxeno-blocker
owner-container: simonfish/dev-claude
phase: session-close
status: complete
updated-at: 2026-07-02T14:14:36Z
---

# Aria — Session Handoff (2026-07-02) — M6 pre-flight 走查: 抓到 Luxeno 延迟命门 + checklist 配方修正

## §0 入口 (新 session 优先读)

本 session 从 `/state-scanner` 起,一路做到 **M6 168h 跑 pre-flight 走查**,挖出**决定 M6 能否启动的关键阻塞**:

> **🔴 M6 168h 跑现在启动无意义** —— dispatch 会全卡 `S3_BUILD_CMD`,因为 Layer 1 的 LLM call 经 **Luxeno/GLM 严重高延迟 (20s+ read timeout)** 全 fallback 链耗尽 → `S_FAIL`。真正的门 = **Luxeno/GLM 延迟**(owner/基建侧),已记入 **Aria #147**。

`#147` 之前 B1 判 "Luxeno 已配好 resolved" 只验了**配置**;本 session 有 live 证据证明**性能/延迟**才是真阻塞。

## §1 已完成 (按时间顺序)

1. `/state-scanner` → 识别唯一 AI 可做项 = 并发 v1.50.2 遗留的 root README badge drift。
2. **主仓 badge 同步 v1.50.1→v1.50.2**(README L8+L242 / VERSION / CLAUDE.md L532),`m6-version-badge-match` 转绿;双远程 `811c7b8`。i18n 按 #140 B-档跳过。
3. 清理 stale 分支 `spec/session-closer-synthesis`(已合并,无独有 commit)。
4. 发现 **Forgejo API 401**(`user does not exist uid:0`)—— 今天 PAT 双重轮换,本 session env 持旧 token。
5. **核实 Hermes tick Forgejo 认证健康**(4 连续 tick 0×401,运行时容器每 tick 现取新 token;401 只是我 session 的旧快照)。
6. **Aether bug 反馈** Forgejo [#190](https://forgejo.10cg.pub/10CG/Aether/issues/190)(rotation 不刷新在飞 session 的 UX gap)。
7. token 恢复:owner `. ~/.forgejo_env` → 我在自己 Bash 调用里 source 即可用(login simonfish)。
8. **Pre-flight 走查(核心)**:
   - **Canary (manual dispatch)**:DEMO #148 → 派 aria-layer2-runner → 越过历史 S4 镜像坑(registry cold-pull auth 正常)→ **容器 Step 1 FATAL: ISSUE_ID 148 不符合正则**。$0(未到 LLM)。
   - **发现 checklist Phase 0 手动 dispatch 配方是坏的**(两处:ISSUE_ID 正则 `^[A-Z][A-Z0-9-]+$` 拒数字号 + 容器 Step2 从预置 issue.yaml 加载非 ISSUE_URL);manual 工具链 M1 遗留、已分叉。→ **修正 checklist**(`e4df698`)。
   - **Path B (自主路径, owner 选)**:aria-auto issue #149 → force tick → scan/seed(内部 id 1994)+ **issue_type_hint=bug(#28 B4 生效)** + 状态机 S1→S2→S3 → **S3_BUILD_CMD LLM call 经 Luxeno 全链 timeout → S_FAIL**。
9. **Luxeno 延迟命门记入 #147**(comment [#14217](https://forgejo.10cg.pub/10CG/Aria/issues/147#issuecomment-14217),含证据块)。
10. 清理 pre-flight 测试 issue #148 / #149(均关闭)。
11. **诊断 ProviderRouter read timeout 配置**:`silknode_client.py:39` `DEFAULT_TIMEOUT_SECONDS=30` 硬编码、无 env override(唯一漏配, Forgejo/Feishu 都可配)。实测 GLM-via-Luxeno ~20-30s+(一次 `ok (20848ms)` + 多次 >30s timeout),骑 30s 线上。**判定 = 后端延迟, 非 timeout 配紧**。撤销"glm-4.7 discrepancy"(实为文档化 FALLBACK 档, `silknode_client.py:36`)。诊断补 #147 [comment #14222](https://forgejo.10cg.pub/10CG/Aria/issues/147#issuecomment-14222) + SilkNode #830 [comment #14224](https://forgejo.10cg.pub/10CG/SilkNode/issues/830#issuecomment-14224)。
12. **止血: LUXENO_TIMEOUT_SEC env 可配 + 部署**:aria-orchestrator **PR #29** merged(`f4d9128`;env 可配默认仍 30;2 新测 + 36 tests pass)→ 节点 pull(editable 生效)→ **cron + reconcile 两 job 都设 `LUXENO_TIMEOUT_SEC=60`**(`nomad job plan` 零 drift + `-check-index` CAS apply + inspect 确认)。reconcile 当前 mechanical(LLM off)是预防性对称。**止血 only, 不改根因**。

## §2 未完成 / Carry-forward 清单

### 高优先级 (建议下次 session 优先评估)
- **[owner/基建, 真门] 解决 Luxeno/GLM 后端延迟** —— 根因 = GLM-via-Luxeno 单次 20-30s+(健康应 <5s)。查 Portkey 代理排队 / GLM 后端负载 / 国内外路由 / 限流叠加重试。**timeout 止血(LUXENO_TIMEOUT_SEC=60)只让"慢但不挂", 不解决慢**;168h 跑要顺畅必须压低延迟。#147 + SilkNode #830。**M6 168h 跑前置门。**
- **验证止血 + 端到端 glm-5.2**(path B):重跑(新造 aria-auto issue → force tick 推进),看 S3 是否从 S_FAIL 变"慢成功";若过 S4_LAUNCH → 容器跑 **glm-5.2**(读 result.json `claude_usage.model`)可 close SilkNode #830。

### 中优先级
- ~~核实 glm-4.7 discrepancy~~ **已解决**:glm-4.7 是文档化 FALLBACK 档(`silknode_client.py:36`, primary glm-4.5-air → fallback glm-4.7),非配置错。
- **manual dispatch 工具链是否值得修**(checklist A 档):validator 归档失效 + /opt/aria-inputs 在 heavy 节点 + issue.yaml vs prompt.txt 契约分叉。owner 已选 B(自主路径),manual 旁路可能可弃。
- **LUXENO_TIMEOUT_SEC=60 是否合适 / 是否需调**:重试链最坏 8×60s;若 Luxeno 延迟 >60s 仍挂。节点可改(nomad var/HCL)。真门修好后应回落到合理值(如 30)。

### 低优先级 / cleanup
- SilkNode #830 仍 open,待 pre-flight `result.json` model=glm-5.2 端到端验证后 close(受 Luxeno 门阻)。

## §3 关键风险 / 已知陷阱
- **Luxeno 单点**:Layer 1 (triage/S3) + Layer 2 (glm-5.2 dispatch) 共用同一 Luxeno 代理 → 延迟问题同时打两层。
- **PAT rotation 不刷新在飞 session**:交互 session 的 `forgejo` 会 401,需 `. ~/.forgejo_env` re-source 或重启 Claude Code(Aether #190)。
- **checklist manual dispatch 配方**(已修但标注未验证):A 档需先恢复 validator + 理清节点/卷 + 确认 M5 镜像契约才能用。
- **force tick 密集会自撞 advisory lock**(ProhibitOverlap)→ 间隔 ≥30s。

## §4 实战教训 (memory 沉淀来源)
- **pre-flight 的价值实证**:$0 抓到 checklist 配方错(canary Step1 FATAL 未到 LLM)+ 自主路径抓到 Luxeno 延迟命门 —— 若 owner 照旧 checklist 手敲 168h,每次 dispatch 秒挂。
- **"配置 OK" ≠ "健康"**:#147 B1 验了 Luxeno 配置就判 resolved,漏了延迟/性能维度;live 运行才暴露真阻塞。(呼应 `[[feedback_verify_agent_diagnosis_against_live_state]]`)
- **bash 双引号里的反引号会被命令替换**:`python3 -c "...\`\`\`..."` 会吞掉 markdown 代码块 → 用 quoted heredoc (`<<'PYEOF'`) 或 `-d @file`。

## §5 多维度同步状态 (Aria 4 维度)
- **代码/git**:主仓 master `2c99d17`,origin/github parity。**aria-orchestrator 子模块 → `ed66327`**(PR #29 env-config + cron/reconcile timeout HCL);gitlink 已 bump。
- **文档**:checklist Phase 0 已修正;本 handoff 已更新至 timeout 部署后状态。
- **Issue**:Aether #190 (new)、Aria #147 (2 new comments: 命门 #14217 + 诊断 #14222)、SilkNode #830 (follow-up #14224)、Aria #148/#149 (closed)。aria-orchestrator PR #29 (merged)。
- **运行时**:Layer 1 tick 认证健康 / schema v5.0 / 集群基建健康;**Luxeno LLM 延迟降级(根因未修)**;cron+reconcile 已加 `LUXENO_TIMEOUT_SEC=60`(止血)。

## §6 Next session 入口 + 优先级建议
1. **先看 #147** 的 Luxeno **后端延迟**是否已修(owner/基建)。timeout 止血(=60)已部署但只是"慢但不挂";**根因未解前不要启动 168h**。
2. Luxeno 延迟压低后 → 重跑 pre-flight path B(见 §2 高优先级)→ 验 glm-5.2 → close #830 → LUXENO_TIMEOUT_SEC 回落合理值。
3. 全绿后才进 Phase 1 Day-1 anchor(启动 168h 时钟)。

## §7 提交清单 (commit hash + multi-remote parity)
主仓 (origin+github parity):
- `811c7b8` docs(sync): 主仓 badge v1.50.1→v1.50.2
- `e4df698` docs(probes): M6 checklist Phase 0 修正手动 dispatch 配方
- `39cffac` docs(handoff): 本 handoff (Luxeno 命门 + checklist 修正)
- `dfded80` chore(gitlink): aria-orch → f4d9128 (PR #29)
- `666d879` chore(gitlink): aria-orch → 3dd4b5f (cron LUXENO_TIMEOUT_SEC=60)
- `2c99d17` chore(gitlink): aria-orch → ed66327 (reconcile timeout parity)

aria-orchestrator (origin only, 内部不上 GitHub):
- PR #29 merged `f4d9128` fix(silknode): LUXENO_TIMEOUT_SEC env-configurable
- `3dd4b5f` chore(deploy): cron LUXENO_TIMEOUT_SEC=60
- `ed66327` chore(deploy): reconcile LUXENO_TIMEOUT_SEC=60 parity

无 aria-plugin 版本变更。

## §8 Memory entries this session (0 new — 见 §4, 均已被 checklist/#147/现有 memory 覆盖)

本 session 教训已固化进 in-repo 制品(checklist + #147 comment)或呼应现有 memory,无需新 memory 文件。

## Cross-references
- Aria #147 (M6-blocker, Luxeno 延迟 comment #14217) / Aether #190 (PAT rotation UX)
- `.aria/probes/m6-7d-run-startup-checklist.md`(Phase 0 已修正)
- SilkNode #830(glm-5.2 路由,待 pre-flight 端到端验证)
- 前次 handoff: `2026-07-01-glm-5.2-cutover.md`
