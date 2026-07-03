---
track-id: m6-blocker3-spec-approved-claude-md-hygiene
owner-container: simonfish/dev-claude
phase: session-close
status: complete
updated-at: 2026-07-03T14:21:31Z
---

# Aria — Session Handoff (2026-07-03) — M6 Blocker 3 Spec 起草→审计→Approved + CLAUDE.md 瘦身立规矩

## §0 入口 (新 session 优先读)

本 session 两条独立主线, 均闭环:

1. **M6 Blocker 3 输入投递 Level 3 OpenSpec**: 承 2026-07-02 pre-flight 的「自主 E2E 从未闭环」阻塞链, 据 `DEC-20260702-001` (C' 双通道) 走十步循环 Phase A → **A.1 起草 + A.2 post_spec 3 轮 CONVERGED 审计 + owner sign-off Approved + 提交** (`15ab2e2`)。Spec = `openspec/changes/aria-2.0-m6-dispatch-input-delivery/`。
2. **CLAUDE.md 瘦身 + 立规矩**: owner 问 CLAUDE.md 是否符合 CC + Aria 规范 → 实测 73% 是时效流水 → **瘦身 762→552 行 (-71%, `a4f9340`) + 立 claude-md-hygiene Option A 规矩 + enforcement check** (standards `3e38449` + 主仓 `739cb67`)。

> **主线现实**: M6 168h 自主跑仍**三门未清** —— Blocker 3 实施 (本 Spec Phase B) + Blocker 4 (Luxeno 延迟, owner/基建) + 遥测 Spec (AC-6 评分, 独立未起)。三者清前不可端到端评分。

## §1 已完成 (按时间顺序)

1. `/state-scanner` → 识别 Blocker 3 Phase A 为唯一 AI 可独立推进的主线项 (承 2026-07-02 handoff §6)。
2. **A.1 起草** (spec-drafter): 独立 Level 3 Spec (Rule #5 主仓, 非 #2 补丁)。起草前 **Explore recon 4 个 DEC 待核实项全落地** + 纠正 DEC 2 处措辞: DB 键 = 值重格式化**非结构迁移** (issue_id 单 TEXT 列 + 复合 PK); AC-2 分层用 `json_extract` **非 issue_id join**。proposal 378 行 + tasks 6 TG/30 task。
3. **A.2 post_spec 审计** (audit-engine convergence, 5-agent [tech-lead/backend-architect/qa/code-reviewer/km], 全对 aria-orchestrator `daf7c79` **真代码 code-grounded**):
   - **R1 5/5 REVISE** (3 Critical + 4 Major + 1 Minor): AD-M0-5 误归属 [从 DEC 继承, 实际在 AD4 风险表 cell] / fetch-outcome↔状态机死锁 [空 expected→ASSERTION_MISMATCH→exit1→S_FAIL 新形态 100% S_FAIL] / AC-6 fetch-fail 不可区分 / ISSUE_URL 未真修 [4-agent] / retry 分类漏 / META R7 64KB 事实错 [R7 实为辟谣 64KB, 真限 128 KiB] / compute-assertions call-site → 全落地。
   - **R2 4 PASS + 1 REVISE**: backend-architect 抓 **2 个修复引入的 Critical** —— corpus 排除标记搁浅 result.json [跨节点不可读 + Layer1 从不读 + AC-2 只看 state] / B.3↔D.1 raw-number 自相矛盾 → 落地 (outcome-class stderr marker → DB 持久化 [reuse #147 B4 json_extract] → sibling acceptance 分层 + seed additive 列 [既有 M3/M4/M5 迁移范式])。
   - **R3 5/5 unanimous PASS CONVERGED**: 两 Critical CLOSED code-verified + 无新回归; 非阻塞 (fail-closed marker 默认 / base_branch 措辞 / 单载体) folded in。
4. **owner sign-off → Approved**。提交 `15ab2e2` (spec proposal/tasks + 15 份 per-agent 审计报告 + 1 CONVERGED 汇总 + CLAUDE.md M6 状态订正 make-ready→阻塞链) 双远程 parity。
5. **CLAUDE.md 深度审计** (owner 问是否符合 CC + Aria 规范): 实测 762 行 / 69K 字符 (每 session ~2-3 万 token 税), **73% 是时效性状态/历史流水** (footer 22 条前次 45% + 插件版本内联 changelog 22%)。判定: 稳定方法论部分 (27%) 合格; 状态+footer 不合格 —— 违 **CC 极简推荐 + Aria 自定义文档边界 + Rule #9 (session 记录归 docs/handoff/) + SOT 纪律 (changelog 归 CHANGELOG.md)**。
6. **瘦身** (`a4f9340`, 主仓): 762→552 行 (**-71%**)。footer 22 前次流水→纯指针; 插件版本 15K blob→当前版本 + CHANGELOG 指针; 当前阶段/运行时/PRD ~200 行 run-on→~12 行 tight 现状 + 指针 (原地覆写); 检查清单冗长注释→单行。稳定方法论/9 规则/信息地图**原样保留**; 零信息丢失 (全在 docs/handoff + CHANGELOG + git)。大块用 line-range 重组 (Edit 无法胜任 15-31K 字符 old_string), 先备份 + 验 fence 配平 + 边界。
7. **立规矩 Option A** (owner 选"彻底移交", 理由: 本就用 handoff + `/state-scanner` 查状态): `standards/conventions/claude-md-hygiene.md` (`3e38449` 双远程) + `.aria/state-checks.yaml` 新 check `claude-md-changelog-free` (检出 footer 滚动条目 / 行数超预算 → warn, **根因兜底防回涨**) + CLAUDE.md 文档边界段引用 (主仓 `739cb67`, gitlink→3e38449)。
8. **复扫确认**: 7 checks, 5 pass / 2 advisory red。新 check `claude-md-changelog-free` **绿** (555 行, 0 滚动条目)。两 red 留着 (owner 认可): `issue-cache-freshness` (长 session 里 TTL 老化, 探针正常态) + `i18n-readme-translation-currency` (#140 B 档有意 advisory, patch-only 免重译)。

## §2 未完成 / Carry-forward 清单

### 高优先级
1. ⭐ **Blocker 3 → Phase A.3 + Phase B** (M6 自主 E2E 闭环主线): Spec 已 Approved, 待 A.3 (task-planner detailed-tasks.yaml + agent 分配) → Phase B 实施 aria-orchestrator: 容器 `initial.sh` (regex + dual-mode input + fetch + 三态 outcome) + Layer1 `extension.py` (ARIA-<repo>-<number> id + seed additive 列 + ISSUE_URL 重建 + outcome-class 消费) + schema 迁移 + sibling acceptance 分层。30 tasks 见 tasks.md (6 TG)。**与 Blocker 4 正交但工作量大** (改容器+Layer1+schema+镜像重建)。
2. **Blocker 4 (Luxeno 后端延迟 45-54s)**: owner/基建/SilkNode 门。查 Portkey server-side (prompt 大小/模型/后端路由)。**别优化 mihomo (实测无效)**。timeout=60 只"慢但不挂"。#147 + SilkNode #830。
3. **遥测 Spec (AC-6 评分依赖, 独立未起)**: 容器如何把 cost/model 经 logs 标记回报 Layer 1。本 Blocker 3 Spec 只修 input; 168h 跑可评分还依赖它 (写进 spec §Out of Scope 防隐性掉线)。
4. **168h 自主跑三门未清** (Blocker 3 impl + Blocker 4 + 遥测), 全绿前无法端到端评分 (AC-5/AC-6)。

### 中/低优先级
- **claude-md-hygiene 规矩传播**: 已在 standards, 第三方 vendor aria-standards 的项目自动获得 convention; 但 `claude-md-changelog-free` check 在主仓 `.aria/state-checks.yaml` 仅 Aria 生效 (第三方需自行加 check 或作为 opt-in)。
- `issue-cache-freshness` red: advisory TTL 探针, `rm .aria/cache/issues.json` + 重扫刷绿 (会再老化, 设计如此)。
- `i18n` red: 有意 advisory, 仅当 README.md **正文实质变更** 才需同步 (#140 B 档)。

## §3 关键风险 / 已知陷阱
- **Luxeno 单点**: Layer 1 (triage/S3) + Layer 2 (glm-5.2 dispatch) 共用同一 Luxeno 代理 → 延迟同时打两层。
- **Spec 继承 DEC 错误**: Approved/审议过的 DEC 仍可含代码级错误 (本 session DEC 3 处错全被 spec 继承); post_spec 必须 code-grounded 才抓得出。见 memory `feedback_spec_inherits_upstream_dec_errors`。
- **CLAUDE.md footer-as-changelog 反模式**: 已用 `claude-md-changelog-free` check + Option A 规矩堵死回涨; 后人往 footer 加流水会被 `/state-scanner` 亮黄。

## §4 实战教训 (memory 沉淀来源)
- **Spec 忠实 ≠ 正确**: 据 Approved DEC 起草会原样继承 DEC 自身代码级错误; 起草前 recon DEC 每处 AD/行号/数值断言, post_spec 须 code-grounded (memory 已写)。
- **CLAUDE.md 卫生审计**: 用**两把尺子** (CC 官方推荐 + 项目自定 charter/规范) 审 meta-doc; 先用硬数据 (per-section 字符/行占比) 量化再判臃肿; 时效内容归各自 canonical 家; **规矩 + 自动 check 才是根因修复** (一次性清理会回涨)。规矩已入 standards, 非 memory (不复制 repo 内容)。
- **多轮审计抓 fix-introduced Critical**: R2 抓到 R1 修复自身引入的 2 个 Critical (复用 `feedback_multiround_audit_catches_fix_introduced_regression`)。

## §5 多维度同步状态 (Aria 4 维度)
- **代码/git**: 主仓 master `739cb67` / standards `3e38449` / aria `021670a` / aria-orchestrator `daf7c79` —— **全 4 仓 origin+github parity** (aria-orch 仅 origin)。无待 push。
- **文档**: 新 Spec (proposal+tasks) + CLAUDE.md 瘦身 + `standards/conventions/claude-md-hygiene.md`。
- **决策**: 消费 `DEC-20260702-001` (起 Blocker 3 Spec); **Option A** (CLAUDE.md 卫生, owner sign-off 2026-07-03)。
- **一致性** (consistency_check): 5 条 advisory「active change 未列入 UPM in-progress」= **Aria 自身无 runtime UPM 的预期态** (memory `project_aria_no_runtime_upm`), 非缺陷。
- **运行时**: 无变更 (aria-orchestrator `daf7c79` 未动; 无插件版本变更)。

## §6 Next session 入口 + 优先级建议
1. ⭐ **Blocker 3 → A.3 agent 分配** (task-planner) → **Phase B 实施** (aria-orchestrator 容器 + Layer1 + schema)。这是 M6 自主 E2E 闭环主线。
2. **Blocker 4 (Luxeno)** owner/基建/Portkey server-side; **遥测 Spec** 待起 (AC-6 依赖)。
3. **三门清前 168h 自主跑不可评分** —— 别当"差启动"。

## §7 提交清单 (commit hash + multi-remote parity)
主仓 (origin+github parity):
- `15ab2e2` docs(spec): M6 Blocker 3 输入投递 Level 3 OpenSpec — A.1 起草 + post_spec 3 轮 CONVERGED
- `a4f9340` docs(claude): 瘦身 CLAUDE.md — footer 流水/版本 changelog 移交 canonical 家 (762→552 行, -71%)
- `739cb67` docs(convention): 立 CLAUDE.md 卫生规矩 (Option A) + enforcement check + gitlink

standards (origin+github parity):
- `3e38449` docs(conventions): 新增 claude-md-hygiene 规范 (Option A 彻底移交)

无 aria / aria-orchestrator 变更。无插件版本变更。

## §8 Memory entries this session (1 new)
- `feedback_spec_inherits_upstream_dec_errors` — 据 Approved DEC 起草的 spec 会原样继承 DEC 自身代码级错误 (忠实≠正确); 起草前 recon DEC 每处断言, post_spec 须 code-grounded (M6 Blocker3 实证: DEC 3 处错全被 spec 继承 → 审计抓出)。
- (CLAUDE.md 卫生规矩 = `standards/conventions/claude-md-hygiene.md`, 入 repo 非 memory, 避免复制)

## Cross-references
- Decision: `docs/decisions/DEC-20260702-001-layer2-input-delivery-architecture.md`
- Spec: `openspec/changes/aria-2.0-m6-dispatch-input-delivery/`
- 审计报告: `.aria/audit-reports/post_spec-{R1,R2,R3,CONVERGED}-*-dispatch-input-delivery-*.md`
- 规范: `standards/conventions/claude-md-hygiene.md` + check `claude-md-changelog-free`
- Aria #147 (M6 阻塞链) / SilkNode #830 (Luxeno/glm-5.2)
- 前次 handoff: `2026-07-02-m6-preflight-luxeno-blocker.md`
