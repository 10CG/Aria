---
track-id: m6-preflight-luxeno-blocker
owner-container: simonfish/dev-claude
phase: session-close
status: complete
updated-at: 2026-07-02T05:29:00Z
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

## §2 未完成 / Carry-forward 清单

### 高优先级 (建议下次 session 优先评估)
- **[owner/基建] 解决 Luxeno/GLM 延迟**(#147 新 comment)—— 20s+ read timeout,dispatch 卡 S3。查:Portkey 代理过载 / GLM 后端慢 / ProviderRouter read timeout 配太紧(若 GLM 合法需 20-40s)。可能在 SilkNode #830 一并提。**这是 M6 168h 跑的前置门。**
- **Luxeno 恢复后重跑 pre-flight**(path B):新造 1 个 aria-auto issue → force tick 推进 → 验到 S4_LAUNCH 容器跑 **glm-5.2**(读 result.json `claude_usage.model`,端到端验证可 close SilkNode #830)。

### 中优先级
- **核实 Layer 1 模型配置**:dispatch `model_used=glm-4.7` 记录,但 router 实试 `glm-4.5-air`/`glm-5-turbo`,与 footer "Layer 1=glm-4.5-air" 不一致 —— 待核实 glm-4.7 出处。
- **manual dispatch 工具链是否值得修**(checklist A 档):validator 归档失效 + /opt/aria-inputs 在 heavy 节点 + issue.yaml vs prompt.txt 契约分叉。owner 已选 B(自主路径),manual 旁路可能可弃。

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
- **代码/git**:主仓 master `e4df698`(badge 同步 + checklist 修正),origin/github parity。aria/standards/aria-orchestrator 子模块指针未变。
- **文档**:checklist `.aria/probes/m6-7d-run-startup-checklist.md` Phase 0 已修正。
- **Issue**:Aether #190 (new)、Aria #147 (new comment)、Aria #148/#149 (closed)。
- **运行时**:Layer 1 tick 认证健康 / schema v5.0 / 集群基建健康,**但 Luxeno LLM 延迟降级(阻塞)**。

## §6 Next session 入口 + 优先级建议
1. **先看 #147** 的 Luxeno 延迟状态 —— owner/基建是否已处理。**未解决前不要启动 168h**。
2. Luxeno 恢复 → 重跑 pre-flight path B(见 §2 高优先级)→ 验 glm-5.2 → close #830。
3. 全绿后才进 Phase 1 Day-1 anchor(启动 168h 时钟)。

## §7 提交清单 (commit hash + multi-remote parity)
- `811c7b8` docs(sync): 主仓派生显示 v1.50.1→v1.50.2 (badge) — origin+github parity
- `e4df698` docs(probes): M6 checklist Phase 0 修正手动 dispatch 配方 (canary 实证坏) — origin+github parity
- 无子模块 / 无插件版本变更。

## §8 Memory entries this session (0 new — 见 §4, 均已被 checklist/#147/现有 memory 覆盖)

本 session 教训已固化进 in-repo 制品(checklist + #147 comment)或呼应现有 memory,无需新 memory 文件。

## Cross-references
- Aria #147 (M6-blocker, Luxeno 延迟 comment #14217) / Aether #190 (PAT rotation UX)
- `.aria/probes/m6-7d-run-startup-checklist.md`(Phase 0 已修正)
- SilkNode #830(glm-5.2 路由,待 pre-flight 端到端验证)
- 前次 handoff: `2026-07-01-glm-5.2-cutover.md`
