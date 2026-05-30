# concurrent-session-upm-safety — 并发多 session UPM/handoff 安全 (convention 主解药 + 检测/fetch 辅助)

> **Level**: 3 (Full — proposal.md + tasks.md;跨 standards convention + state-scanner + phase-d-closer;含 collision 字段持久化 collector 增量)
> **Status**: ✅ **Approved** (合并版 — 双 #133 Spec 对账合并 per owner 2026-05-30; (b) backbone 2-round CONVERGED + (a)/(c) focused re-audit **R1 FAIL(2C)→Rev1→R2 CONVERGED 2026-05-30** [tech-lead PASS / qa PWW / backend PASS, all Critical+Important CLOSED]; ready Phase A.3 → Phase B)
> **Change ID**: `concurrent-session-upm-safety`
> **Source**: Forgejo Aria [#133](https://forgejo.10cg.pub/10CG/Aria/issues/133) (dogfood: SilkNode 双 session;本 session dev-claude 自身亦撞同类: latest.md prepend + 5 SOT 冲突 + 4× index.lock)
> **Supersedes (合并)**: `concurrent-track-proactive-coordination` (sister 终端并发起草, L2 未收敛/banked) —— 其 (a)/(c) 深度机制 + R1/R2 audit findings 已吸收入本 Spec;原 dir 归并删除
> **Target version**: aria-plugin v1.37.0 (tentative — Phase B step 0 必 `cat aria/VERSION+plugin.json` 复核, 不留 ship 时)
> **Risk class**: 防御性 — convention 为主解药;检测/fetch advisory 非阻塞;collision 字段 additive (snapshot schema additive 演进);无 API break
> **既定哲学约束 (不可违背)**: advisory-over-hardlock (DEC-20260519-001, memory `feedback_concurrency_advisory_over_hardlock`) — 无硬锁/无 auto-enable/降级可见

---

## 合并来源 (双 Spec 对账)

本 Spec 由 #133 的两个并发 Spec 合并 (owner 决策"合并为单一 Spec"):

| 来源 | 贡献 | 状态 |
|------|------|------|
| `concurrent-session-upm-safety` (本, dev-claude) | **(b) convention 主解药** + 审计 **C1 因果框架** (检测拦不住 write-time thrash, convention 才是解药) | post_spec CONVERGED (2-round) |
| `concurrent-track-proactive-coordination` (sister) | **(a)/(c) 深度机制**: collision 字段持久化前置 + phase-d fresh-fetch + 切口2 disjointness;R1/R2 9 findings | L2 未收敛 (R2-CARRY 待续) |

**合并立场** (调和两审计): **(b) convention = 主解药 (forcing function)** [本 Spec C1];**(a) 检测 + (c) fetch = advisory 辅助早发现** [吸收 sister 深度机制];collision 字段持久化 = (a)/(c) 的共同前置 (sister R1 C1 发现的 phantom-field bug)。

---

## Why

#133 真实 dogfood (SilkNode 双 session):(1) 并发改同一 UPM/handoff 区 → **PR merge thrash** (反复 mergeable:false);(2) **矛盾记录** (对同一 prod 状态写相反归属,根因 `updated_at`=Prisma @updatedAt 不被 raw SQL 触发 → 软代理误判)。

**因果定位 (本 Spec audit C1, load-bearing)**: Problem-1 thrash 是 **write-time git 冲突**,检测/提示 (scan 时点 advisory) **不能在写入路径阻断它** —— SilkNode 已有 Layer L 1.51-1.53 advisory 却仍 thrash = advisory 在 Problem-1 被实证证伪。**消除 thrash 的 forcing function = convention 结构改写** (让两次编辑不再 textual 重叠)。检测/fetch 是 advisory 辅助 (早发现 + 可对账),非解药。advisory 哲学不变 (跨容器硬锁=假性安全)。

---

## What

### 已存在 vs gap (两审计核实)

| 维度 | 已存在 (v1.36.0) | gap |
|------|------------------|-----|
| collision 分类 | **仅 renderer-local** `track_board.py::_classify_collision` (render 时算, **不入 snapshot**);`collision_type`/`has_collision` 只存在于设计文档 `layer-l-integration.md` (**phantom field, 从未实现** — sister R1 C1) | 需提升为**共享 helper + 持久化** `tracks_multibranch.collision` (additive) — (a)/(c) 的共同前置 |
| 跨 track 检测 | `tracks_multibranch` **无条件采集** (scan.py:112) + 规则 1.51-1.53 advisory (无条件运行) | 只读 handoff frontmatter track,**无 UPM/SOT churn 信号源** (非 opt-in 未启用) |
| 编辑前 fetch | C.2.4.5 merge 前 fetch (**fail-hard**) / C.2.5 post-merge push | phase-d-closer **收尾起点** (写 UPM 前) 无 fetch;现仅**反应式** retry (SKILL.md ~L136) → 需前置 **fetch-before-edit (fail-soft advisory)** |
| 记录约定 | History 表 **prepend-desc (L5 不可改)** + latest.md pointer + 多 track banner | **共享 thrash 区** = line-3 pointer 单行 + followup `#NNN` row + UPM body;无 concurrent-safe 写法规范 |
| 外部状态归属 | — | **AI 记录**用软代理 (`updated_at`) 非硬证据 → 误判 (Problem 2)。与 #54 同源不同物 → **独立 + 交叉引用** |
| coordination 启用 | `coordination.enabled` opt-in (config 键, **非** snapshot 字段 — sister R1 C2) 控制 phase1_gate/claim 写,**不**控制 tracks_multibranch 采集 | (a) 建议默认启用 → **不 auto-enable** (advisory 哲学), 改增强 advisory 检测+提示 |

### 工作项 (convention 主解药先行, 检测/fetch 辅助)

**0. 【前置·共同依赖】collision 字段持久化** (sister R1 C1 — phantom-field fix): **真实管线** (R1 三 agent 对真代码核实) = `tracks[] → _track_to_claim_record(t) [lossy, 可 raise ValueError] → reconcile_all() → _classify_collision(claims: list[ClaimRecord])`,**非**"输入 `tracks[]` 的单函数"。`_classify_collision` 真实签名 `(claims: list[ClaimRecord]) -> tuple[kind, severity_emoji]`,其中 emoji 是 render-only。故本项**不是抽函数**,而是新建共享模块 (e.g. `lib/collision.py`) 封装整条 approximation+reconcile 管线,产出新结构 `classify(tracks) -> {kind: none|cross_owner|self_multi_container, groups: list[list[str]]}` (groups = 各 collision 簇的 `owner_container` 成员列表;**emoji 不持久化**;同 `(owner,container)` 全相同 → none 排除 self-serial)。**TASK 0.4 裁定 (R1 收敛, 不拆独立 Spec)**: 无独立用户价值, 纯属切口1/2 内部前置 → 在本 Spec 内拆 **(0a)** collector 内联管线产 `tracks_multibranch.collision` (additive, bump schema) + **(0b)** `track_board` renderer 改读共享字段 (老 snapshot 无字段→`.get()` fallback 为 `{"kind":"none","groups":[]}`, 回归 0) + **meta-fix 前置**: Phase 0 **最先**修 `layer-l-integration.md:23,69` stale 字段名 `collision_type`/`has_collision` (从未实现的 phantom, 防 AI 读旧文档继续传播)。**持久化的 `collision` 字段 surface 等级 = advisory, 不得作任何 gating 输入** (lossy approximation 不可升格为决策依据)。

**1. 【主解药】UPM/handoff concurrent-safe 约定** (standards convention): 共享 thrash 区 (line-3 pointer / UPM body / followup row) 改 concurrent-safe —— (a) pointer/body 共写区 **append-friendly 或 per-session 隔离** (History 表 prepend-desc **不动**, L5);(b) followup `#NNN` 表避免多 session 改同一 row (per-session sub-row / 轻量标记, **非复用** claim_lifecycle orphan-ref);(c) **AI 记录外部系统状态须引硬证据** (RETURNING/显式 timestamp), 禁 `updated_at` 软代理作 canonical (**作用域=AI 记录自律, 非用户 DB**;#54 交叉引用)。

**2. 【辅助·早发现】并发 churn 检测增强 (state-scanner, advisory)** [吸收 sister 切口2]: 阶段 2 **iff** `tracks_multibranch.collision.kind != none` **且** config `coordination.enabled == false` (config 读非 snapshot — R1 C2) → surface advisory 提示 (建议启用 coordination + 一键 config 片段)。**disjointness** (R1 I3): 切口2 iff `enabled==false`;既有 cross_owner→phase1_gate iff `enabled==true` — `enabled` 上互斥,绝不双触发。判定**不依赖"谁"** (同 email/container 无法区分自他, collision helper 已按 owner+container 归类)。**仍 opt-in 不强制, 不 auto-enable**。

**3. 【辅助·写前同步】phase-d-closer 收尾 fetch-gate (fail-soft advisory)** [吸收 sister 切口1]: D.1 写 UPM **之前** (插入点: `phase-d-closer/references/execution-steps.md` D.1 action 起始, **写 UPM 前**新增 fetch-gate 子步骤): (a) **default-branch 解析** — Phase B **须自实现** `git symbolic-ref refs/remotes/origin/HEAD` → fallback `origin/master` → `origin/main` (**注: state-scanner 内无现成 symbolic-ref resolver 可复用**; sync.py `_ORIGIN_HEAD_REFS` 仅是 fallback **顺序数据** 常量, 非可调函数 [R1 I1]); (b) **fresh fetch** (`timeout=30`, 独立于 1.16 的 30s 缓存 — 收尾时缓存已陈旧; fetch 失败仅复用 `coordination_fetch._classify_error` 的 **error_kind enum** [`network`/`auth_403`/`non_ff`/`git_missing`/`other`] + soft-warn, **不回显 raw stderr** 防 credential 泄漏, 不阻塞); (c) **behind-check** — 复用 `git rev-list --left-right --count` **命令形态** (现于 git.py:147 / sync.py:146, 但其锁死 `@{upstream}`; 切口1 需 `HEAD...origin/<def>`, 故复用 pattern **非直接调函数** [R1 I2])。**触发** (防假阳性): 仅 `behind>0` **且** (`collision.kind!=none` **或** behind commits 触及 UPM 文件 [`git log --name-only <old>..origin/<def>` ∩ `upm.source_file`; **`upm.source_file` 可为 None (无 UPM 项目如 Aria 自身, upm.py:326) → null-guard 跳过 UPM-touch 检查**, R1 I4]) → advisory; 触及 UPM → 强提示。纯 behind>0 → 静默 (防 prompt fatigue)。**fail-soft** ≠ C.2.4.5 fail-hard。

**4. 【验收防线】convention 机械 guard 评估**: 评估轻量 checker (followup 跨 session 重复 row / 共享区违规写法), 至少定 dogfood 验收标准。

**5. 【明确不做】** worktree-per-session (Layer L TASK-024/025 后续线) / 改 Layer L opt-out 默认 / 改 claim-reconcile 既有逻辑。`.git/index.lock` 已立 memory `feedback_stale_git_index_lock_recovery`。

---

## Impact

| 维度 | 影响 |
|------|------|
| advisory 哲学 | **严格遵守** — 无硬锁/无 auto-enable/降级可见 (DEC-20260519-001) |
| 主解药权重 | thrash 消除靠 convention 结构改写 (工作项 1); 检测/fetch advisory 辅助 |
| 改动文件 | standards (convention) + state-scanner (collision helper+持久化 / 切口2 / schema) + phase-d-closer (切口1) + layer-l-integration.md (meta-fix) + 主仓 doc-sync |
| 复用 (精确) | `_classify_collision` 语义 / sync.py default-branch chain / git.py ahead-behind / coordination_fetch error_kind enum (非缓存结果) / upm.source_file 字段 |
| 向后兼容 | opt-out 默认不变; advisory 非阻塞; collision 字段 additive (老 snapshot 无此字段 → renderer fallback); 单 session 无额外提示 |
| 跨仓 | standards + aria-plugin + 主仓 |

### Risk / 开放 (合并后待 audit 复核)

- **scope 重构 (sister R2-CARRY #1)**: collision-field-persistence (工作项 0) 是否拆独立 prereq Spec — Phase B 定。
- **检测信号可靠性**: N 窗口 + "触碰共享区" 误报/漏报 (fixture 含正反+边界)。
- **self-thrash dogfood**: 本 Spec 改 state-scanner+phase-d (高频并发区), ship 须先用自己的 convention (per `feedback_meta_dogfood_solution_validates_self_mid_ship`)。
- **合并 re-validation** ✅ DONE (2026-05-30): (a)/(c) focused re-audit R1 FAIL(2 Critical)→Rev1→R2 CONVERGED (3 agent, all Critical+Important CLOSED, 剩 Minor doc-hygiene)。报告: `.aria/audit-reports/post_spec-R2-*-concurrent-session-upm-safety-merged-consolidated.md`。

---

## Acceptance Criteria

- [ ] **【主解药·thrash 结构性消除】**: convention 应用后两 session 编辑共享区不再 textual 重叠 — 可验: diff 无 conflict marker (旧 prepend/同-row 写法产生 = 翻转)
- [ ] **AC-0 collision 持久化**: `tracks_multibranch.collision` additive 字段由 collector 持久化, 结构 `{kind: none|cross_owner|self_multi_container, groups: list[list[str]]}` (groups = collision 簇 `owner_container` 成员列表; **render-only emoji 不持久化**; **字段 advisory-only, 不作 gating 输入** [R1 I5]); 新 `classify(tracks)` helper 封装真实管线 `tracks[]→_track_to_claim_record→reconcile_all→_classify_collision` (helper 输入是 `list[ClaimRecord]` 经转换, **非** `tracks[]` 直喂 [R1 C1]); helper 配 unit test 跑**真实** `collect_handoff_multibranch` 输出 fixture (非手搓 schema); renderer 改读共享字段, 老 snapshot 无字段→`.get()` fallback `{"kind":"none","groups":[]}`, 回归 0; **meta-fix 前置 Phase 0 最先执行**: `layer-l-integration.md:23,69` stale phantom 字段名修正 [R1 C2]
- [ ] **SC1a 哲学合规 (可机验)**: grep 无 auto-enable / 无 block-on-conflict; coordination opt-in; 离线 fail-soft
- [ ] **AC-2 切口2 检测**: iff `collision.kind!=none` 且 config `enabled==false` → advisory (config 读取插入点须在 tasks 明确: scan 推荐逻辑层, 非 renderer/collector [R1 I8]); **disjointness 三态 fixture** [R1 I6]: (a) `enabled==false`+`collision!=none`→切口2 触发; (b) `enabled==true`+`collision!=none`→切口2 **不**触发 (phase1_gate 处理); (c) `enabled==true`+`collision==none`→两者均不触发 (中间态)
- [ ] **AC-1 切口1 fetch-gate fail-soft**: D.1 前 default-branch resolve (自实现 symbolic-ref+fallback) + fresh fetch (timeout=30, 失败 soft-warn 不回显 raw stderr 不阻塞) + behind-check; 仅 `behind>0 且 (collision!=none 或 触及 upm.source_file)` 提示, 触及 UPM→强提示; 纯 behind>0→静默。**fixture 必含**: (a) `upm.source_file==None` null-guard 路径 (无 UPM 项目, self-thrash dogfood 会撞 [R1 I4]); (b) **credential 不泄漏断言** — 构造含 token 的失败 stderr, 断言 soft-warn 输出**不含**该 token 字面 (机验非仅 code review [R1 I7]); (c) 离线 fail-soft 不阻断
- [ ] **AC-3 无噪音 (负向)**: `collision.kind==none` + `behind==0` → 两切口 advisory 字符串**均不出现** (absence assertion)
- [ ] **convention 落地 standards**: 共享区写法 (History prepend 不动) + followup row 隔离 + AI 记录外部状态硬证据自律 (作用域=AI 非用户 DB); 单 session 降级 + 正/反 pattern + #54 交叉引用 (独立不合并)
- [ ] **Rule #6 substitute**: collision helper + 切口1/2 = deterministic fixture (真实 collector 输出, 含边界) + dogfood; convention = 文档 + (可选) guard
- [ ] 全量回归 PASS (state-scanner + phase-d-closer 零退化); **self-thrash dogfood**: 本 Spec ship 用自己的约定

---

## 关联

- 合并的 sister Spec audit: `.aria/audit-reports/post_spec-R1R2-2026-05-30-concurrent-track-proactive-coordination-consolidated.md`
- 本 Spec audit: `.aria/audit-reports/post_spec-R2-2026-05-30-concurrent-session-upm-safety-consolidated.md`
- 既有 Layer L: `openspec/archive/2026-05-20-multi-terminal-coordination/` + DEC-20260519-001
- advisory 哲学: memory `feedback_concurrency_advisory_over_hardlock`
- #54 (data-availability rubric) — Problem-2 硬证据约定 = #54 领域实例;**独立交叉引用, 不合并**
- 本 session dogfood: handoff `docs/handoff/2026-05-30-shell-jq-crlf-hardening-shipped-v1.36.0.md` §7 + memory `feedback_concurrent_sot_conflict_mechanical_resolve` / `feedback_stale_git_index_lock_recovery`
- Source #133
