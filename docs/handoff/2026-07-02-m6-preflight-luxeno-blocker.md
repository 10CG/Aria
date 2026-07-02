---
track-id: m6-preflight-luxeno-blocker
owner-container: simonfish/dev-claude
phase: session-close
status: complete
updated-at: 2026-07-02T21:40:59Z
---

# Aria — Session Handoff (2026-07-02) — M6 pre-flight 走查: 抓到 Luxeno 延迟命门 + checklist 配方修正

## §0 入口 (新 session 优先读)

本 session 从 `/state-scanner` 起,一路做到 **M6 168h 跑 pre-flight 走查**,挖出**决定 M6 能否启动的关键阻塞**:

> **🔴 M6 168h 跑现在启动无意义** —— dispatch 会全卡 `S3_BUILD_CMD`,因为 Layer 1 的 LLM call 经 **Luxeno/GLM 严重高延迟 (20s+ read timeout)** 全 fallback 链耗尽 → `S_FAIL`。真正的门 = **Luxeno/GLM 延迟**(owner/基建侧),已记入 **Aria #147**。

`#147` 之前 B1 判 "Luxeno 已配好 resolved" 只验了**配置**;本 session 有 live 证据证明**性能/延迟**才是真阻塞。

> **⚠️ 更大的重定义(session 后段深挖,§2 Blocker 3 / #147 #14265)**:pre-flight 逐层剥出**阻塞链** —— Luxeno timeout(止血 #29 ✅)→ 镜像 sha(#30 ✅)→ **自主容器路径从未闭环**(数据铁证:唯一 S9 是字母前缀 manual dispatch,所有数字-id 自主 dispatch 100% S_FAIL;Layer1↔容器输入契约从未对齐)。**M6 自主 E2E 不是"差启动",是从未跑通** → 需先取部署镜像确认契约 + 决策 tick-staging vs 镜像重建。

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
13. **验证止血 (path B 重跑, issue #150/内部 1998)**:**铁证成功** —— 两 Layer 1 LLM call `ok (44567ms)` + `ok (53944ms)`(**都会在旧 30s 下 timeout,在 60s 下通过**)→ dispatch 推进 S1→S2→S3→**S4_LAUNCH 派容器**。原 Luxeno S3 命门解除。**但 Luxeno 45-54s 延迟 → 60s 仅勉强,坐实根因必须修**。
14. **Blocker 2 (镜像 sha) — ✅ 修复 (PR #30)**:S4_LAUNCH 后容器 Driver Failure —— 自主 dispatch 传 `IMAGE_SHA=91b8975`(git 短sha)→ `@sha256:91b8975` 无效。根因 `_read_m1_image_sha` 读错字段(读 `image_sha_final` git-sha 而非 `image_sha256_final` digest;数据本对,代码 bug = "m5-handoff F1 bug")。**PR #30** merged(`daf7c79`):改读 digest + 剥 sha256: 前缀 + 回退;2 新测 + 95 pass;节点验证返回 bare 64-hex。
15. **Blocker 3 发现 (未修): ISSUE_ID 正则**:自主 ISSUE_ID=数字内部 id(1998)撞容器 `initial.sh:106` `^[A-Z][A-Z0-9-]+$` → FATAL(同 manual canary '148')。正则在 **M5 镜像**内 → 改需重建镜像 或 tick 改 ID 格式。记 #147 [comment #14260](https://forgejo.10cg.pub/10CG/Aria/issues/147#issuecomment-14260)。
16. **部署镜像 Step2 契约 byte 级确认**(一次性 nomad docker job `cat` 镜像内 initial.sh,#147 [comment #14270](https://forgejo.10cg.pub/10CG/Aria/issues/147#issuecomment-14270)):部署 M5 镜像确有正则(line 106)+ 读 **`inputs/<ISSUE_ID>/issue.yaml` 就地 envsubst 渲染**(line 145-147),**不吃 prompt.txt / 不用 dispatch_id 键**。→ **修法收敛 Option A**:容器契约稳定已知(= dispatch-issue.sh),让 Layer 1 复刻(letter-prefixed ISSUE_ID + stage issue.yaml),**放弃 prompt.txt 方向,不重建镜像**。
17. **Luxeno 慢 = 网络诊断**(owner 疑 mihomo,#147 [#14270](https://forgejo.10cg.pub/10CG/Aria/issues/147#issuecomment-14270) + 更正 [#14272](https://forgejo.10cg.pub/10CG/Aria/issues/147#issuecomment-14272)):Aria **已接** mihomo;**绕过 mihomo 实测不变快**(直连真 IP 1.36s = mihomo 1.38s)。luxeno.ai=Cloudflare(104.21/172.67),从 Aria 网络访问 **CF 整体慢**(cloudflare.com 本身 1.8-3.4s),非 mihomo/luxeno-origin。**且网络仅占 44-54s call 的 ~3%,真瓶颈是 GLM 推理**。owner 后台 "Aria 慢" = server-side(推理/路由),需 Portkey 日志,是 Blocker 4 真战场。**结论:别优化 mihomo(无效)。**
18. **Blocker 3 输入投递架构 brainstorm → 4-agent 审议 → DEC**(`docs/decisions/DEC-20260702-001-layer2-input-delivery-architecture.md`, `ee83401`):recon 发现 **Option A(纯 tick 侧)不可行** —— aria-runner-inputs 是每-heavy-节点本地卷,Layer 1(light-1 本地 ext4)物理写不到。brainstorm(technical)收敛方向 **C-fetch**(容器从 ISSUE_URL 自取,对称既有输出节点无关通道;否 D 共享存储/E 节点钉定)。**post_brainstorm 拉 4 agent 并行审议**(tech-lead/backend-architect/qa-engineer/knowledge-manager)→ **1 OBJECTION(qa)+ 3 CONCERNS**,全折入升级版 **C' 双通道**。**qa 抓 2 个代码级 showstopper**:① Layer1 侧改动被漏(Step1 正则先于 Step2 → 只改容器则修复不生效)② `files`≠`expected_changes`,fetch 模式空 expected_changes → compute-assertions 恒判 SUCCESS = **静默污染 168h corpus**。tech-lead 升级:metadata 走 META 保跨-repo 解耦 + (repo,number) 复合键 + always-fetch 杀 stale-read。km:**Level 3** + amend **AD-M0-5** + layer-boundary-contract §5 缺口。DEC 含 11 决策点 + 连带文档同步 + 遥测依赖边 + 4 项 spec 前置待核实。

## §2 未完成 / Carry-forward 清单

### 高优先级 (建议下次 session 优先评估) — 168h 跑阻塞链
pre-flight 逐层剥出的阻塞链(每层 $0-低成本抓到):
1. ~~Luxeno S3 timeout~~ → **止血** LUXENO_TIMEOUT_SEC=60 (PR #29) ✅ 验证过
2. ~~镜像 sha 无效~~ → PR #30 ✅
3. **[未实施, milestone 级 Level 3] Blocker 3: 自主 E2E 从未闭环 → 架构已定 (C' 双通道, DEC-20260702-001)**:Option A(纯 tick 侧)recon 判**不可行**(输入卷每-heavy-节点本地,Layer1 写不到)→ brainstorm + 4-agent 审议收敛 **C' 双通道**(见 §1 item18)。**下一步 = Phase A**:spec-drafter 据 DEC-20260702-001 起 **Level 3 OpenSpec**(proposal + tasks,主仓 `openspec/changes/`,**独立 Spec 非 #2 补丁**)。**实施必含**(否则重演坑):① Layer1 侧同 scope 改动(发 ARIA-<repo>-<number> + metadata META + head_branch 统一)② compute-assertions 空-expected 禁恒真(假绿修)③ fetch 失败契约可区分 infra/agent-fail ④ title/body 消毒。**spec 前置待核实 4 项**(DEC §待核实): heavy 节点 NFS(诚实否 D)/ envsubst 白名单 byte 核 / RENDERING_CONTRACT expected_changes / DB 键迁移对 #147 AC-2 影响。
4. **[owner/基建, 真门] Luxeno/GLM 后端延迟** —— 45-54s/call(健康 <5s)。**网络已排除**(§1 item17:mihomo 无辜,CF-access 固有慢 ~1.5s 但只占 ~3%)。真瓶颈 = GLM **推理**(thinking 模型 + prompt 大小 + 后端路由);owner 后台 "Aria 慢" = server-side → 查 **Portkey/luxeno 日志**(prompt 大小 / z.ai 国际 vs bigmodel 国内路由 / 限流)。timeout=60 只"慢但不挂"。#147 + SilkNode #830。**别去优化 mihomo(实测无效)。**
5. **[doc-sync, Rule #3] CLAUDE.md 项目状态段现已实质误导** —— 仍写 "M6 168h 跑 now make-ready / 只剩 owner 运营仪式";本 session 根本性推翻(自主 E2E **从未闭环**, 4 层阻塞链, Blocker3 需 Level 3 Spec)。CLAUDE.md 项目状态 + footer 需更新反映阻塞链现实。**注意高 contention 区**(`[[feedback_claude_md_project_status_high_contention]]`), fetch 后再改。本 handoff (latest.md 指向) 是准的 canonical 入口; CLAUDE.md 是滞后的二级参考。可并入 Blocker3 Phase A 的 CLAUDE.md M6 依赖链更新一并做。
5. (清 3+4 后) **端到端 glm-5.2 真跑** → 读 result.json `claude_usage.model` → close #830 → 才进 Day-1 anchor。

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
- **代码/git**:主仓 master `ee83401`,origin/github parity。aria-orchestrator 子模块 `daf7c79`(PR #29+#30)。
- **文档**:checklist Phase 0 修正;本 handoff 更新至 DEC;**新增 `docs/decisions/DEC-20260702-001`**(Blocker 3 输入投递架构 C')。
- **决策**:**DEC-20260702-001**(Layer2 输入投递 C' 双通道,4-agent 审议,Level 3,待 Phase A)。
- **Issue**:Aether #190、Aria #147 (6 comments: 命门 #14217 / 诊断 #14222 / 止血+阻塞链 #14260 / Blocker3 评估 #14265 / 镜像契约+网络 #14270 / 网络更正 #14272)、SilkNode #830 (#14224)、Aria #148/#149/#150 (closed)。aria-orchestrator PR #29+#30 (merged)。
- **运行时**:Layer 1 tick 认证健康 / schema v5.0 / 集群基建健康;cron+reconcile `LUXENO_TIMEOUT_SEC=60`(止血, 已验证 44.6/53.9s call 通过);tick image digest 修复(读 bare 64-hex)。**待清: Blocker 3 ISSUE_ID 正则(镜像) + Luxeno 根因**。

## §6 Next session 入口 + 优先级建议
1. **Blocker 3 → Phase A**:据 **DEC-20260702-001** 起 Level 3 OpenSpec(spec-drafter,proposal+tasks,主仓 `openspec/changes/`,独立 Spec)。实施必含 §2 item3 的 4 项 + 4 项 spec 前置核实。这是 M6 自主 E2E 闭环的主线。
2. **Blocker 4(Luxeno 后端延迟)**:owner/基建/SilkNode 侧;查 Portkey server-side(prompt 大小/模型/后端路由)。**别优化 mihomo(实测无效)**。timeout 止血=60 只"慢但不挂"。
3. **两者(Blocker 3 实施 + Blocker 4 根因)清前,168h 自主跑无法闭环**。全绿后才进 Phase 1 Day-1 anchor。
4. 遥测(cost/model 回报)独立 Spec(DEC 依赖边),AC-5 评分依赖它。

## §7 提交清单 (commit hash + multi-remote parity)
主仓 (origin+github parity):
- `811c7b8` docs(sync): 主仓 badge v1.50.1→v1.50.2
- `e4df698` docs(probes): M6 checklist Phase 0 修正手动 dispatch 配方
- `39cffac` docs(handoff): 本 handoff (Luxeno 命门 + checklist 修正)
- `dfded80` chore(gitlink): aria-orch → f4d9128 (PR #29)
- `666d879` chore(gitlink): aria-orch → 3dd4b5f (cron LUXENO_TIMEOUT_SEC=60)
- `2c99d17` chore(gitlink): aria-orch → ed66327 (reconcile timeout parity)
- `41e2da7` docs(handoff): 更新 handoff — timeout 止血部署
- `4963ef3` chore(gitlink): aria-orch → daf7c79 (PR #30 image digest fix)
- `a88cafb` docs(handoff): Blocker3 评估 + `0f2f0f5`/`e46d42f` 收尾/memory
- `ee83401` docs(decision): **DEC-20260702-001 输入投递架构 C' 双通道** (4-agent 审议)

aria-orchestrator (origin only):
- PR #29 `f4d9128` LUXENO_TIMEOUT_SEC env-configurable + `3dd4b5f`/`ed66327` cron/reconcile =60
- **PR #30 `daf7c79`** fix(tick): read image_sha256_final digest for IMAGE_SHA (#147 Blocker 2)

aria-orchestrator (origin only, 内部不上 GitHub):
- PR #29 merged `f4d9128` fix(silknode): LUXENO_TIMEOUT_SEC env-configurable
- `3dd4b5f` chore(deploy): cron LUXENO_TIMEOUT_SEC=60
- `ed66327` chore(deploy): reconcile LUXENO_TIMEOUT_SEC=60 parity

无 aria-plugin 版本变更。

## §8 Memory entries this session (4 new)

- `feedback_dryrun_peels_blocker_chain` — make-ready 断言≠端到端跑通;pre-flight 逐层剥阻塞链
- `feedback_fix_target_verify_data_vs_code` — 被要求"修数据"先核实真错;bug 常在代码读错字段 → pivot 改代码 (M1 handoff digest 案例)
- `feedback_attribute_latency_by_measurement_not_hypothesis` — 归因慢前测分解+绕嫌疑层验证;别优化占比小的层 (Luxeno 网络非主因)
- `feedback_code_grounded_multiagent_review_catches_altitude_misses` — 里程碑架构决策的多-agent 审议须让 agent 读真代码, 才能抓设计者 altitude 漏的 showstopper (C' DEC 4-agent 实证)

## Cross-references
- Aria #147 (M6-blocker, Luxeno 延迟 comment #14217) / Aether #190 (PAT rotation UX)
- `.aria/probes/m6-7d-run-startup-checklist.md`(Phase 0 已修正)
- SilkNode #830(glm-5.2 路由,待 pre-flight 端到端验证)
- 前次 handoff: `2026-07-01-glm-5.2-cutover.md`
