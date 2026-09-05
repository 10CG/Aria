---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T14:01:04.375Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — tech-lead 席 (架构与跨模块镜头)

审计对象: `openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md` (commit 144d79e, Level 2)。
本席只审不改, 未修改任何仓内文件。

## 审计结论

### C-1 (critical) 判定键换成 container 主键后, 缺「跨容器 owner 串归并」这一步 ⇒ 本 Spec 主打的那个误报在真实数据上不消解, 且 D-1/D-2 的后果描述写错

- **type**: issue
- **severity**: critical
- **category**: architecture
- **scope**: `proposal.md §What D1 (classify_claims 判定键)` + `proposal.md §What 实验表 C 行` + `proposal.md §决策点 D-1 选项 (a) 后果句` + `lib/collision.py::classify_claims`
- **summary**: D1 只在「同一 container 内」合并多 owner 串; 跨容器比较仍用原始 owner 串集合。真实数据里两台机的 owner 串各自漂移过, 集合天然是 2 个 ⇒ 同一人两台机恒判 cross_owner 🔴。而 §决策点与实验表都声称该 🔴「由 D-1/D-2 裁定后消解」——D-2 只收敛未来提交身份, 历史 frontmatter 按非目标不 rewrite, 故该 🔴 会长期常亮。
- **evidence**:
  - 规则原文: `proposal.md:30`「先按 container 分组; ≥2 个 distinct container 时再看 owner —— owner 全同 → self_multi_container, owner 不同 → cross_owner」; 声称消解的两处: `proposal.md:50` 实验表 C 行「(🔴 — 实为同一 owner 两机, 由 D-1/D-2 裁定后消解)」与 `proposal.md:57` D-1 选项 (a) 后果句。
  - 真实数据 (本席实读全仓 frontmatter, `for f in docs/handoff/*.md; do head -8 $f | grep -m1 '^status:'` 过滤 active): track `state-scanner-stale-refs-false-parity` 的 6 份 active frontmatter = `aria-runner-bot/023236f2` ×2 (2026-07-12) + `simonfish/bfe8285d` ×4 (2026-07-14..07-19), 全部是同一位 owner 的两台机。
  - 按 D1 规则逐字仿真 (本席实跑, 见 §轮次记录 命令 6): `containers=['023236f2','bfe8285d'] owners=['aria-runner-bot','simonfish'] -> proposed kind: cross_owner`。
  - 非目标 `proposal.md:102`「不 rewrite 历史 handoff frontmatter」⇒ 这 6 行的 owner 串不会变; D-2 (a) 只影响新写出的 handoff。
- **可行方向 (供执笔取舍, 不替 owner 决策)**: 在「按 container 分组」与「比 owner」之间插入一步 owner 串归并 —— 由 D3 已经要在采集的 `container -> owners[]` 关系做并查集/传递闭包 (本仓真实数据里 `bfe8285d: [aria-runner-bot, simonfish]` 与 `023236f2: [aria-runner-bot, simonfish]` 两条同容器多 owner 证据足以把两串判为同指), 或改为「每 container 取一个 canonical owner (如 last_seen 那个) 再比较」。两条路都不需要维护映射表, 与 D-1 选项 (a) 的「不引入身份映射表」理由相容。无论取哪条, §What 的 Positive 与实验表 C 行都必须重写。

### M-1 (major) SC-4 要求的 dedupe 折叠与 D1「dedupe 不改逻辑」互斥, 按现 key 结构不可同时成立

- **type**: issue
- **severity**: major
- **category**: implementation
- **scope**: `proposal.md §What D1 第 3 条` vs `proposal.md SC-4`; `scripts/collectors/handoff_multibranch.py:519-522`
- **summary**: dedupe key 含 owner 段。换成两段式解析后, 「同容器不同 owner」两行的 owner 不同 ⇒ key 不同 ⇒ 不折叠。SC-4 却要求它们折叠为 1, 这只能靠改 key (去掉 owner 段) 实现, 与 D1「不改逻辑, 只用 SC 锁住」直接冲突。
- **evidence**:
  - `handoff_multibranch.py:519-522`: `owner, container, _session = _split_owner_container(...)` / `key = (t.get("track_id"), owner, container)`。
  - D1 原文 `proposal.md:31`「`scripts/collectors/handoff_multibranch.py:518` (dedupe key) 与 `scripts/renderers/track_board.py:412` (标签查找) **不改逻辑**」。
  - SC-4 原文 `proposal.md:91`「同容器不同 owner 两行折叠为 1 且产出 advisory」。
  - 本席仿真 (命令 6 第二行输出): 新解析下 key 集合 = `[('aria-runner-bot','023236f2'), ('simonfish','bfe8285d')]` —— 同容器不同 owner 会得到两个不同 key。
- **附带**: 现行 key 还有一个反向效应 Spec 未记: 今天两段串被解析成 `('', <owner 段>)`, 于是**同一 owner 的不同容器**两行会被折成一行 (case-4「同人两机 → none」有一半是 dedupe 造成的, 不只是 classify)。修 parser 后这些行会重新展开, 看板行数会涨; Risk 表只写了 kind 变化, 没写行数/`after_dedupe` 统计变化。

### M-2 (major) `track_board.py` 的标签查找键与 ClaimRecord 的 `"unknown"` 归一不匹配, SC-4「board 标签回显原串」在不改 :412-417 的前提下不可达

- **type**: issue
- **severity**: major
- **category**: implementation
- **scope**: `scripts/renderers/track_board.py:412-417`; `lib/collision.py:132-134`; `proposal.md SC-4`
- **summary**: 渲染器用 `split` 的**原始返回值**建标签表, 用 **ClaimRecord 字段**查表; 而 `track_to_claim_record` 把空段一律填成 `"unknown"`。两段式解析后 session 段为 `""`, 建表键是 `(owner, container, "")`、查表键是 `(owner, container, "unknown")` ⇒ 恒查不中, 标签退化成 `owner/container/unknown`, 不是原串。同一份代码在 `collision.classify()` 里没这个问题 (那边建表查表都用 `rec`)。
- **evidence**:
  - `track_board.py:412` `o, c, s = _split_owner_container(oc)` → `:413` `oc_by_key[(o, c, s)] = oc`;`:416` `key = (claim.owner, claim.container, claim.session)` → `:417` `return oc_by_key.get(key) or f"{claim.owner}/{claim.container}/{claim.session}"`。
  - `collision.py:132-134` `owner=owner or "unknown", container=container or "unknown", session=session or "unknown"`。
  - 对照 `collision.py:353-357`: 那里 `key = (rec.owner, rec.container, rec.session)` 两侧同源, 不受影响。
  - 这处今天就已经是坏的 (三段式解析 2 段串 → 建表键 `('', 'simonfish', 'bfe8285d')` vs 查表键 `('unknown', 'simonfish', 'bfe8285d')`), 只是没人测过 ⇒ SC-4 那半条断言在**改前改后都红**, 需要 T4 显式改 :412-417 (或统一归一函数), 不能挂在「不改逻辑」下。

### M-3 (major) 与 a1-entry 的排序规则只覆盖文本冲突, 覆盖不了语义依赖: 本 Spec 先落会让 a1-entry 已收敛的 SC-3 失去区分力

- **type**: risk
- **severity**: major
- **category**: architecture
- **scope**: `proposal.md §Impact「与 a1-entry 的边界」`; `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:571, :660`; `lib/identity.py:191-222`
- **summary**: a1-entry 的 SC-3 是 baseline-failing 测试, 它「必红」的前提正是 `get_container_id()` 保持 label-over-uuid。本 Spec T3 把它改成恒 uuid 后, a1-entry 那条断言对**旧实现也变绿**, 反事实力归零 —— 这是语义耦合, `git rebase` 不会报冲突, 「谁后进 master 谁 rebase」处理不了。
- **evidence**:
  - a1-entry `proposal.md:571` SC-3: 「直接调 `get_container_id()` (`lib/identity.py:191`, `:222` label 优先) 的实现在设了 label 的夹具上**必红**」。
  - a1-entry `proposal.md:660` Impact 行: 新增 `def get_container_uuid(home_dir: Optional[Path] = None) -> str` (跳过 label), 理由即「现有 `get_container_id()` 在 `:222` 是 `return label if label else uuid`, 不能直接用」。
  - 本 Spec T3 `proposal.md:80`「`get_container_id()` 恒 uuid」。
  - 另一条同形耦合: 本 Spec 改的是 `collision.py` 上游 (`split_owner_container:63` / `classify_claims:143`), a1-entry 全文按行号钉了 `lib/collision.py:265-266` (`if not own_linked_issue:`) 等实读断言并已过 R1–R6 收敛; 上游增删行会让那些行号断言过期, 同样不产生 git 冲突。
- **建议**: §Impact 的排序规则要从「谁后进谁 rebase」升级为**显式方向**: 要么本 Spec 等 a1-entry B.2 落地后再动 `identity.py` (只加 `get_container_label()`, `get_container_id()` 的 flip 挂到 a1-entry 之后), 要么在本 Spec 内承担改写 a1-entry SC-3 的判据并知会对方容器。两条都要写进 §Impact, 不能留给 B.1 临场判断。

### M-4 (major) `get_container_id()` 语义 flip 无迁移/检测面; 且 hostname 兜底分支使「恒返回 uuid」为假, 该假全称会被 D2 写进共享 SOT

- **type**: issue
- **severity**: major
- **category**: architecture
- **scope**: `proposal.md §What D1 第 4 条 / D2 §2.3.1 / T3 / SC-3`; `lib/identity.py:191-244`; `lib/concurrent_tracks.py:133,:200`; `scripts/phase1_gate.py:287-294`
- **summary**: 两个缺口。(1) claim 目录与匹配都以 container 值为键, 一旦某台机在 flip 时**已设 label 且持有在飞 claim**, flip 后 `(container, session)` 匹配落空 ⇒ 在飞 claim 变孤儿、该 track 恒 occupied —— 正是 #135 08-13 事故的镜像形态, 而 Spec 只用 SC-3 复现「先 acquire 后加 label」这一个方向。(2) `get_container_id()` 还有 hostname 兜底分支, 「恒返回 uuid」不成立; D2 要把「`<container-id>` = uuid 字段」写进 standards 共享 SOT, 措辞需要覆盖降级路径, 否则采纳方读到的是一条假全称。
- **evidence**:
  - `phase1_gate.py:287` docstring「Matches on (container, session) because a session that already holds an ...」+ `:294` `verdict.winner.container == identity.container_id`; claim 路径 `claims/<container-id>/<session-id>.yaml` (`claim_schema.py:8`)。
  - `concurrent_tracks.py:133` `container_id = get_container_id()` / `:200` `if c.container == container_id and c.status == _ACTIVE_STATUS`。
  - `identity.py:222` `return label if label else uuid`; 兜底分支在 `:236-244` 区段 (写文件失败 → 打 warning → 回落 hostname), a1-entry `proposal.md:142` 已把该分支落点实读为 `:242 return _hostname()` 并与 `:244 return uuid` 区分。
  - 本机 `~/.aria/container-id` 的 label 为空 (文件头还留着 2026-08-13 的人工告警注释), 所以本机不触发 (1); 但这是**运气**, 不是机制 —— Spec 需要一条「flip 前检测 label 非空 + 该 container 下有 active claim 则先 release/迁移」的任务或 SC。

### M-5 (major) 「与 #182 正交」把依赖说成正交: 全部历史 active 行都超 STALE_TTL 仍参与 collision, 修完 parser 的信号仍不可信

- **type**: risk
- **severity**: major
- **category**: architecture
- **scope**: `proposal.md §What D3 第 2 条 / §Impact Positive / 非目标第 3 条 / SC-6`
- **summary**: Positive 声称「collision 信号第一次同时满足 🔴/🟡/⚪ 三态」。但 Layer H 把 `status: active` 的历史 handoff 一律映射成 active claim, 且 `classify()` 会把 reconcile 因陈旧而降级的 winner 重新捞回当活跃竞争者 ⇒ 2026-05 起的 19 份 active frontmatter 全部参与判定。修完 parser 后, 看板的 🔴/🟡 主要由历史噪声决定, 而不是「谁现在在动」。SC-6 只要求每组**可归因**, 不要求信号可用。
- **evidence**:
  - 实测: 全仓 `docs/handoff/*.md` frontmatter `status: active` = **19 份**, 最早 `2026-05-20-m5-phase-b-shipped.md` (`updated-at: 2026-05-20T14:01:23Z`)。
  - `collision.py:112-116` 把 Layer H 的 `active` / `legacy` 一律映射为 `status="active"`; `:87-92` 用 `updated_at` 同时充当 `claimed_at` 与 `heartbeat_at`。
  - `constants.py:36` `STALE_TTL: int = 1800` ⇒ 上述 19 行全部远超阈值。
  - `collision.py:374-379` 注释与代码: 明确把 `verdict.superseded` 里非终态的 (被降级的陈旧 winner) 重新加回 `active_claims`, 否则「2-claim collision where the winner is stale would mis-classify as none」。
  - C-1 那组 🔴 (`state-scanner-stale-refs-false-parity`) 的 6 行全是 2026-07 的 stale active —— 即本 Spec 的旗舰误报案例本身就是 #182 的产物。
- **建议**: 要么把「Layer H 新鲜度过滤 (只让 N 天内的 active 行参与)」收进本 Spec, 要么把 Positive 降级成「分类逻辑正确, 信号可用性待 #182」并在 §非目标写清依赖方向 —— 现在的写法是把依赖写成了正交。

### M-6 (major) Level 判定: 按 SOT 的判据流程图, 本变更三项触发条件全中, 应为 Level 3

- **type**: decision
- **severity**: major
- **category**: documentation
- **scope**: `proposal.md:3 (> **Level**: Minimal (Level 2 Spec))`; `standards/core/ten-step-cycle/phase-a-spec-planning.md:124-137`
- **summary**: Level 判据不是按天数/文件数, 是按性质三选一。本变更同时命中「architecture」(协调子系统的同一性主键定义)、「cross-module」(aria + standards 两个子模块, 且 `identity.py` 语义面被 phase1_gate / concurrent_tracks / claim 目录结构共同消费)、「breaking」(§2.3.5 判据表是共享 SOT 里给所有采纳方的契约, 判定键从 owner 主键改成 container 主键会改变采纳方的实现)。按流程图字面, 三者任一为 Yes 即 Level 3。
- **evidence**:
  - 判据表 `phase-a-spec-planning.md:126-128`: Level 2 = 「New Skill, medium features (1-3 days)」; Level 3 = 「Architecture changes, cross-module, breaking changes」。流程图 `:131-137`: 「No → Is it architecture/cross-module/breaking? ├─ Yes → Level 3 (Full Spec)」。
  - 跨模块面实证: `proposal.md:8`「`aria/` 子模块 + `standards/` 子模块」; 消费方 `concurrent_tracks.py:133` / `phase1_gate.py:294` / `claim_schema.py:8` 全部消费 container 值。
- **相反意见 (一并记录, 供 owner 裁)**: 交付面只有 4 个代码文件 + 1 份规范, 7 个任务, 起 `tasks.md` 的边际收益可能有限。但本席按 Rule #10 的精神提醒: Level 是判据决定的, 不是按「性价比」下调的; 若维持 Level 2, 应在 proposal 里写明依据哪条判据认为「不算 architecture/cross-module」, 而不是不作声。另: 本 Spec 的任务之间已有真实依赖 (D-1/D-2 裁定 gate T5、T1 gate T2/T4、T6 的冻结快照须在 T1 落地前取), 这正是 `tasks.md` / `detailed-tasks.yaml` 要表达的东西。

### m-1 (minor) 「不改 reconcile」为真但不完整: 两段式解析让 Layer H 的 session 段恒为 `unknown`, reconcile 的 tie-break 键退化

- **type**: risk
- **severity**: minor
- **category**: implementation
- **scope**: `proposal.md 非目标第 1 条`; `lib/reconcile.py:149-151`; `lib/collision.py:134`
- **summary**: Spec 说不动 reconcile 仲裁规则 (文本上确实没动), 但换解析器后所有 Layer H 记录的 `session` 都变成 `"unknown"`, `_tiebreak_key` 从 `container/<uuid>` 退化成 `container/unknown`; `claimed_at` 完全相同的两条同容器记录之间, 确定性 tie-break 退回输入顺序。触发面窄 (需同容器 + 不同 owner + 同秒 `updated_at`, 且要先躲过 dedupe), 但 reconcile 的公开承诺是「identical input → identical output across all containers」, 该退化应在 §Impact 成文。
- **evidence**: `reconcile.py:151` `return f"{claim.container}/{claim.session}"`; `reconcile.py:9` 承诺行「Deterministic: identical input → identical output across all containers」; `collision.py:134` `session=session or "unknown"`。

### m-2 (minor) `identity_advisories[]` 的产出宿主未定, 渲染器按 2-tuple 解包 `classify_claims`

- **type**: issue
- **severity**: minor
- **category**: implementation
- **scope**: `proposal.md D3 第 1 条 / T2`; `scripts/renderers/track_board.py:430`; `lib/collision.py:143`
- **summary**: D3 说 advisory 是「D1 的分组副产物」, 但没说它从 `classify_claims`(现签名返回 2-tuple) 还是从 `classify()`(返回 dict, 加字段是 additive) 出来。若加在 `classify_claims` 上, 渲染器的解包立刻断; 若加在 `classify()` 上, 渲染器需要另一条取数路径 (它不调 `classify()`)。这一条在 B.1 前钉死可以省一次返工。
- **evidence**: `track_board.py:430` `collision_kind, _severity = _classify_collision(active_claims)`; `collision.py:143` `def classify_claims(claims) -> tuple[str, str]`; 渲染器另有 `:459-471` 的 `kind == "none"` 分支直接 `pass` 不出行 —— SC-2 要求「同容器双 owner → `none` + 1 条 advisory」, 那条 ⚪ 行必须走一条与 `collision_kind` 无关的新路径。

### 核验通过、不构成 finding 的几项 (供后续轮次省时)

- **三段式 `superseded_from` 兼容**: D1 保留三段分支即可, `claim_schema._validate_superseded_from` (`:155-158`) 自己 `split("/")` 判 3 段, **不经过** `split_owner_container` ⇒ 解析器改动不触及 Layer L 的 `superseded_from` 契约。Spec 的兼容性判断正确。
- **release_gate / phase1_gate 不消费 `classify_claims`**: 全仓 grep, `classify_claims` 只有 `track_board.py` 与 `collision.classify()` 两个消费方; `phase1_gate.py:126` 只 import `linked_issue_overlaps`。⇒ container 主键**不会**吞掉 Layer L 的占用判定 (占用判定按 winner claim 本身, 与 owner 无关), 「两个人共用一台机」在闸门层仍会互相 BLOCKED_OCCUPIED, 被吞掉的只有看板 advisory 的 🔴 标注。这一条降低了 C-1 与镜头 3 的爆炸半径, 但不改变 C-1 的结论 (Spec 承诺的正是这块 advisory 的正确性)。
- **References 行号**: `split_owner_container:63` / `track_to_claim_record:86` / `classify_claims:143` / `classify:300` / `get_container_id:191` / `handoff_multibranch:518` / `track_board:412` 全部实读命中, 无行号漂移。

## Verdict

**FAIL** — 1 Critical (C-1) + 6 Major (M-1..M-6) + 2 minor。

判据: Critical ≥1 即 FAIL。C-1 是承重的 —— 它打掉的是本 Spec 的主交付承诺 (「同人多机 = 🟡 不再漏报」) 在真实语料上的可达性, 且该错误已经写进了实验表与决策点后果句, 若不改会连带污染 owner 对 D-1/D-2 的判断输入。M-1/M-2 是同一类形状 (D1 声明「不改逻辑」但 SC 要求的行为必须改代码才成立), 会在 B.2 变成「SC 写了却过不了」。M-3 是跨 Spec 的语义耦合, 现在的排序规则处理不了。M-6 是 Level 判据问题, 按 Rule #10 不该由执笔/审计席自行下调, 需 owner 明示。

## Vote

**REVISE** —— 不建议不改直接进 B。

最小返工面 (按优先级):
1. C-1: 在判定算法里补一步跨容器 owner 归并 (并查集或 per-container canonical owner), 重写实验表 C 行与 D-1 (a) 的后果句; 把「历史不 rewrite ⇒ D-2 只影响未来」这一事实写进决策点。
2. M-1 / M-2: 把 `handoff_multibranch.py:519-522` 与 `track_board.py:412-417` 从「不改逻辑」改成显式改动项, 或把 SC-4 的两条断言改成与「不改」相容的写法 (二选一, 现在的组合无解)。
3. M-3: §Impact 的排序规则写成有方向的硬约束 (谁先谁后 + 谁负责改 a1-entry SC-3 判据)。
4. M-4: 加一条 flip 前的 label/在飞 claim 检测任务; D2 文本给 hostname 降级路径留口径。
5. M-5: Positive 降级或把新鲜度过滤收进 scope, 二选一。
6. M-6: 明示 Level 判据 (升 3 或写明为何不算 architecture/cross-module)。

owner 决策点 D-1 / D-2 本身: 本席不代裁。仅报告两点与选项集有关的事实 —— (a) 选项集在「owner 段语义」这一维上是完备的 (提交身份 / 人 / 隐含的第三条「让 owner 段不再承重」实际上已被 D1 的 container 主键部分实现, 建议把它显式写成一个选项, 因为它改变了 D-1 的权重); (b) D-1 (a) 与实验表 C 的后果描述如 C-1 所述是错的, 需订正后再交 owner 裁定, 否则 owner 是在错误的后果预期上做选择。

## 轮次记录

**实读文件** (全部本轮实读, 未凭记忆):

- `openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md` (全文 111 行)
- `.aria/triage-report.json` (issue 原文 + repro case-1..5 + verdict/deviation_note)
- `aria/skills/state-scanner/lib/collision.py` (全文 403 行: 模块 docstring / `split_owner_container:63` / `track_to_claim_record:86-140` / `classify_claims:143-166` / `normalize_linked_issue` / `linked_issue_overlaps` / `classify:300-403`)
- `aria/skills/state-scanner/lib/identity.py` (`:150-244`: `get_owner` / `get_container_id` / label-over-uuid / hostname 兜底)
- `aria/skills/state-scanner/lib/reconcile.py` (`:100-260`: `_tiebreak_key:149-151` / `_is_stale` / rule 1-6)
- `aria/skills/state-scanner/lib/claim_schema.py` (grep + `:155-158` `_validate_superseded_from`)
- `aria/skills/state-scanner/lib/concurrent_tracks.py` (grep container 消费面)
- `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py` (`:505-535` dedupe)
- `aria/skills/state-scanner/scripts/renderers/track_board.py` (`:395-500` 标签表/collision 渲染, `:430` 解包)
- `aria/skills/state-scanner/scripts/phase1_gate.py` (grep container / winner_owner_container)
- `aria/skills/state-scanner/lib/constants.py` (`STALE_TTL`)
- `standards/conventions/session-handoff.md` §2.3.1-§2.3.8 (`:95-240`)
- `standards/core/ten-step-cycle/phase-a-spec-planning.md:118-150` (Level 判据表 + 流程图)
- `standards/openspec/templates/proposal-minimal.md` (Level 2 模板骨架)
- `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (头部 + §1/§2/§2.1 + grep 命中的 `:142` `:144` `:571` `:639` `:660`)
- `~/.aria/container-id` (本机 label 状态)

**跑过的命令** (关键 6 条):

1. `git -C /home/dev/Aria log --oneline -3` — 确认审计对象 commit 144d79e。
2. `grep -rn "get_container_id\|get_owner(" --include=*.py aria/ | grep -v /tests/` — 枚举 identity 消费方 (concurrent_tracks / __init__ / identity 自身)。
3. `grep -rn "classify_claims\|linked_issue_overlaps" --include=*.py aria/` — 确认 classify_claims 只有 2 个消费方, 闸门不消费。
4. `git -C /home/dev/Aria for-each-ref refs/aria/coordination` + `ls-tree -r --name-only` — 实测生产 claim 目录全部是 uuid 形 (`bfe8285d` / `023236f2`), 无 label 形残留。
5. `for f in docs/handoff/*.md; do head -8 "$f" | grep -m1 '^status:' ...` — 统计 frontmatter `status: active` = 19 份并列出其 track-id / owner-container / updated-at (M-5 与 C-1 的数据源)。
6. `python3` 仿真 D1 规则于 track `state-scanner-stale-refs-false-parity` 的 6 行真实数据 — 输出 `proposed kind: cross_owner`, dedupe key 集合 `[('aria-runner-bot','023236f2'), ('simonfish','bfe8285d')]` (C-1 与 M-1 的直接证据)。

**未做**: 未修改任何仓内文件; 未读 Forgejo issue 原文 (triage-report.json 已内嵌 #193 全文 body, aria-plugin#135 的缺口 3 描述以 proposal §Why 第 3 条 + 本机 container-id 文件头的 2026-08-13 人工注释交叉印证, 该注释即 #135 08-13 实证的现场遗留)。
