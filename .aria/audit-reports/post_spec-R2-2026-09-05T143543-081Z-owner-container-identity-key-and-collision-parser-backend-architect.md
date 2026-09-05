---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T14:35:43.081Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R1 处置核对

对照 `.aria/audit-reports/post_spec-R1-2026-09-05T140104-375Z-owner-container-identity-key-and-collision-parser-backend-architect.md` 的 5 条 finding, 逐条核对 v2 proposal.md：

- **Finding 1 (critical, dedupe 键结构性不可能折叠同容器不同 owner)** — **closed**。v2 D1 步骤 2/T4 (proposal.md:34) 显式把 dedupe 键改为 `(track_id, identity_key)`，不再是 `(track_id, owner, container)`。实测：用 v2 的 `identity_key`（container 匹配 `^[0-9a-f]{8}$` 时 `identity_key=container`，owner 不参与）对冻结语料重跑 `dedupe_latest_per_track_container` 等价实现，`bfe8285d`/`023236f2` 两个 uuid 容器上 `aria-runner-bot` vs `simonfish` 两串确实折叠为 1 行（脚本 `/tmp/claude-1000/.../scratchpad/r2_repro.py` 输出 `after_dedupe=122`，与 A 的 121 相比多出的 1 行差额可解释为该折叠动作）。R1 指出的结构性冲突已经被显式改动解除。**但见下方新 Critical 1/2 — 折叠本身做到了，折叠后的分类判定引入了新的、同等严重的误报缺口，不是同一个 bug 但同一处代码。**

- **Finding 2 (major, `.aria/state-snapshot.json` 被 gitignore 且会漂移, 无冻结 fixture)** — **closed**。v2 proposal.md 头部新增「冻结语料」条目 (line 10)，指向 `.aria/repro/handoff-tracks-frozen-2026-09-05.json`；实测 `git check-ignore -v .aria/repro/handoff-tracks-frozen-2026-09-05.json` 退出码 1（未被忽略），`git log --oneline -1 -- .aria/repro/handoff-tracks-frozen-2026-09-05.json` 命中提交 `d23f103`（已入库，996 行非 legacy 行）。T6 (line 102) 计划把它复制为 `tests/fixtures/handoff-tracks-frozen-2026-09-05.json`，SC-6 也改为对这份冻结文件断言。

- **Finding 3 (major, `get_container_id()` 消费方列举不全 + 迁移期风险未评估)** — **partial**。v2 Impact 表新增「`get_container_id()` 消费方 (全列)」一节 (proposal.md:90)，覆盖 `claim_lifecycle.py:39,88` / `phase1_gate.py:294` / `concurrent_tracks.py:25,133`（与我 R1 grep 结果一致）并补充 `release_gate.py`（实读该文件：本身不直接调用 `get_container_id`/`get_identity`，是通过 `from ..lib.claim_lifecycle import release_claim_by_track` 间接消费，标注为消费方成立）与 `session-closer/scripts/handoff_autofill.py`（实读：`:407-409` `from lib.identity import get_identity` / `ident = get_identity()`，行号较 proposal 引用的 `:391` 略有漂移，不影响消费方成立性）。且新增 T3b 守卫任务正面回应「迁移期在飞 claim 变孤儿」的风险。**Enumeration 与风险识别本身已闭合；但守卫的调用时机/挂载点仍未写清，见下方新 Major 3。**

- **Finding 4 (minor, §2.3.7/§2.3.8 已占用, 新章节应编号 §2.3.9)** — **closed**。v2 D2 (proposal.md:42) 与 T5 (line 101) 均已改为「新增 §2.3.9」。

- **Finding 5 (minor, `oc_by_tid_key` 三元组键在未 dedupe 输入上可能撞键, 静默丢行)** — **closed（记为已知限制 + 契约锁定）**。v2 Impact/Risk (3) (proposal.md:89) 逐字对应我 R1 的措辞（"`oc_by_tid_key` 三元组键在未 dedupe 输入上可能撞键 (BA m)"），裁定「生产路径恒先 dedupe, SC 锁『classify 只接受 dedupe 后输入』的契约注释」。这是可接受的处置（生产路径本来就恒先 dedupe，我在 R1 也只把它标为 minor risk 而非阻断项）。

**R1 处置三态计数：closed 3 / partial 1 / open 0**（partial 项已转化为下方 R2 新 finding，不重复计数为 open）。

## 审计结论

### Finding R2-1 (critical / issue / architecture)
- **scope**: proposal.md D1 步骤 3 (line 35) + 实验表变体 D (line 58) + SC-6 (line 114)；`aria/skills/state-scanner/lib/collision.py:143-168` (`classify_claims`)
- **summary**: 对 D1 步骤 3「先按 identity_key 分组，比较 owner 等价类代表」的字面算法在冻结语料上直接实现，对「同一物理机零段 (`dev-claude`) 与两段 (`simonfishgit/dev-claude`) 混写」这组真实数据给出 `cross_owner`（响亮误报），**不是**实验表声称的 `self_multi_container`/🟡。该组恰是 Why 段明确点名「B 只修 parser 会产生的误报」且声称 D 三步齐全能修复的**同一组数据**。proposal 未写明「不可归属 (空/unknown) owner」在 classify_claims 内部与真实 owner 比较时应被排除计数还是当作独立字符串参与比较——两种读法都符合步骤 3 的字面描述，但只有「排除计数」一种能得到 D 行声称的结果，proposal 没有挑明选哪种。
- **evidence**: 脚本 `/tmp/claude-1000/-home-dev-Aria/660cdd00-d2ad-4227-a5bb-5312810322f1/scratchpad/r2_repro.py`，方法论先用同一套基础设施核对 A/B 两行（均与 proposal 逐字一致，见下），再跑 D：
  - Variant A（当前代码, 未改动）: `after_dedupe=121`, `{"kind": "self_multi_container", "groups": [["dev-claude", "simonfishgit/dev-claude"]]}` — 与 proposal line 56 逐字一致。
  - Variant B（只改步骤 1, 沿用旧 dedupe 键）: `after_dedupe=122`, `{"kind": "cross_owner", "groups": [["simonfish/dev-claude", "simonfish/dev-claude2"], ["dev-claude", "simonfishgit/dev-claude"]]}` — 与 proposal line 57 逐字一致。
  - Variant D（三步齐全, 按 proposal 字面算法实现——container 段 `^[0-9a-f]{8}$` 判定 identity_key；全语料并查集按「同一 uuid 容器共现过的 owner 两两等价，空 owner 不入类」；classify_claims 改为按 identity_key 分组后比较 owner 等价类代表, 空/unknown owner 作为普通字符串参与比较）: `after_dedupe=122`（与 proposal 一致），但 `{"kind": "cross_owner", "groups": [["simonfish/dev-claude", "simonfish/dev-claude2"], ["dev-claude", "simonfishgit/dev-claude"]]}` —— 与 proposal line 58 声称的 `self_multi_container` **不一致**。
  - 逐 track_id 下钻定位到具体冲突: `aria-submodule-gate-block-flip cross_owner [('simonfish', 'dev-claude'), ('unknown', 'dev-claude')]`（脚本输出）——这条 track 的两行 identity_key 分别是 `simonfishgit/dev-claude` 与 `/dev-claude`（owner 空, `track_to_claim_record` 现有代码本就把空 owner 填成 `"unknown"`, `lib/collision.py:132`），二者是不同 identity_key（主机名容器, 保留 owner 段区分, 符合步骤 2 设计），比较 owner 类时 `"simonfishgit"` 与 `"unknown"` 是两个不同字符串（`"unknown"` 从未在任何 uuid 容器上与别的 owner 共现过, 不会被并查集合并）→ 判定 2 个类 → cross_owner。
- **为什么这不是我的实现选择偏差**: A/B 两行的复现与 proposal 逐字吻合，证明脚本方法论正确；D 行唯一变化的是步骤 3 的新增逻辑，且我采用的是该逻辑「组内 identity_key 分组 + 逐个比较 owner 类」最直接的字面实现，没有额外发明规则。proposal 步骤 3 里「空/unknown owner 不可归属, 不构成独立类」这句话只出现在「建并查集」的语境（不给空 owner 分配类, 不参与合并), 从未说清它在 classify_claims **比较阶段**该被排除计数还是当普通字符串处理——两种读法都不违反字面文本，但只有前者能兑现 D 行的 self_multi_container 结果。
- **影响**: SC-6「改后 D = 2 组，逐组归因，无不可解释组」与 Impact/Positive「真两人撞车 = 🔴（不再降级）、同人多机 = 🟡（不再漏报）」的核心叙事，在冻结语料的真实第二组上不成立（除非实现者自己发现并补上这条未写明的排除规则）。这正是 Why 段点名要防止的「响亮误报」在 D 组重演一次。

### Finding R2-2 (critical / issue / architecture)
- **scope**: proposal.md D1 步骤 3 (line 35) + D3 (line 46)；`aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py:700-723`；`aria/skills/state-scanner/lib/collision.py:300-345` (`classify`)
- **summary**: 步骤 3 要求并查集建在「全语料 (collector 扫到的全部非 legacy 行, 不是 dedupe 后的行)」上，但生产路径唯一调用点 `_classify_collision_summary(deduped_tracks)` (`handoff_multibranch.py:714`) 只把 **dedupe 后** 的 `deduped_tracks` 传给 `classify()`，`classify(tracks, *, now=None)` 签名也只接受一个 `tracks` 参数 (`collision.py:300`)。全语料（跨 track_id、跨时间、dedupe 前）在这条调用链上任何一处都不可达 `classify()` 内部——dedupe 已经按 `(track_id, identity_key)` 把同 track 内的旧 owner 行丢弃, 而漂移证据本身（`bfe8285d` 34 份 `simonfish` + 2 份 `aria-runner-bot`, 跨越 07-05 到 09-03 多个不同 track_id）需要的正是跨 track_id、跨时间的原始行共现关系。proposal 的 Tasks/SC (T2/SC-2/SC-8) 均未提出给 `classify()` 或 `_classify_collision_summary` 增加第二个参数（如全量 `tracks`）、也未提出在 collector 里把全量 `tracks` 单独跑一次并查集再注入 `classify()`。`classify_claims(claims) -> tuple[str,str]` 本身也没有任何形参能接收「owner 等价类代表」这份跨语料信息——它只能拿到当前一个 track_id 已 reconcile 出的几条 `ClaimRecord`。
- **evidence**: 实读 `handoff_multibranch.py:709-714`:
  ```
  deduped_tracks, dedupe_stats = dedupe_latest_per_track_container(tracks)
  ...
  collision = _classify_collision_summary(deduped_tracks)
  ```
  只有一个位置调用 `classify`/`_classify_collision_summary`，只传 `deduped_tracks`；`tracks`（全量非 legacy 行）在此调用之后再未被引用。实读 `collision.py:300` `def classify(tracks: "list[dict]", *, now=None) -> dict:` 与 `:143` `def classify_claims(claims: "list[ClaimRecord]") -> tuple[str, str]:`——均为单一数据入口, 没有第二参数位置放等价类信息。要让 D3 的 `identity_advisories[]`（声称「从步骤 3 的全语料并查集产出」）与 classify_claims 的「比较 owner 等价类代表」都工作, 唯一可行路径是给 `classify()` 新增形参（例如 `classify(tracks, all_tracks=None)`）或让调用方先算好等价类映射再传入——这是一个未在 T2/SC-2/SC-8/Impact 中出现过的签名变更, Tasks 对「谁在哪一层建这张等价类表、以什么形式传进 `classify()`/`classify_claims()`」完全没有着墨。
- **影响**: 这不是可以「实现时顺手决定」的细节——它决定 `classify()` 是否需要破坏性签名变更（影响 `track_board.py` 等既有调用方）、collector 是否要在 dedupe 前后各跑一次全量扫描（性能）、以及 `identity_advisories` 的产出层级到底是 collector 还是 `lib/collision.py`。SC-2 的「同容器双 owner → `identity_advisories` 恰 1 条」这类断言在**单元测试**层面（直接构造小语料喂 `classify()`）能通过, 但生产路径（真实 996 行语料, collector 唯一入口）按当前签名和调用点**结构上拿不到**建等价类所需的全语料, SC-6 的端到端断言若不先做上述签名改动就无法在生产路径上被满足。

### Finding R2-3 (major / issue / architecture)
- **scope**: proposal.md D1 (T3b, line 37) + Tasks T3/T3b (line 98-99)；`aria/skills/state-scanner/lib/identity.py:191-244` (`get_container_id`)；`aria/skills/state-scanner/lib/coordination_ref.py:596-716` (`read_claims`/`write_claim`)
- **summary**: T3b「flip 前守卫」未写明由谁在什么时机调用；把它挂进 `get_container_id()` 本身（该函数被 `claim_lifecycle` 的 acquire/heartbeat/release、`phase1_gate.py:294`、`concurrent_tracks.py:25,133` 每次身份解析都调用）会让 `identity.py`（现状零内部依赖, 纯 stdlib）新增对 `coordination_ref.py`（git 子进程 `ls-tree` + 每个 claim 文件一次 `git show`）的下游依赖, 且让每一次身份解析都多一趟 git 子进程调用——这是未预算的性能/分层倒置回归。同时 T3b 允许「拒绝 flip」的运行时分支, 与 T3「`get_container_id()` 改为 uuid 优先」（proposal 原文未写「恒 uuid」但语义是无条件优先, D1 步骤 3 未描述任何条件分支）存在张力：如果 flip 可以在运行时被「拒绝」, `get_container_id()` 就不是无条件 uuid 优先, 而是「视迁移状态而定」——这个条件分支本身该长在哪个函数、状态如何持久化（每次都重新 `read_claims()` 判断，还是只在启动时判断一次并缓存），proposal 未描述。
- **evidence**: 实读 `identity.py` 头部 import 块 (`:19-29`)，只有 `os/secrets/socket/subprocess/sys` 等标准库, 无 `coordination_ref`/`claim_schema` 等内部依赖；`grep -n "^from \.\|^import" identity.py` 确认。实读 `coordination_ref.py:606-620` `read_claims()` docstring 与实现：机制是 `git ls-tree -r` 全量枚举 + 对每个匹配路径 `git show` 一次——这是一趟或多趟子进程调用, 非内存查表。实读 T3b 原文「若本机 container-id 文件 `label` 非空且 `claims/<label>/` 下存在 active claim ⇒ 先按 D1 前的口径 release 或迁移到 `claims/<uuid>/`, **否则 flip 会让在飞 claim 变孤儿**」——这句话本身只描述后果, 未指定挂载点（`get_container_id()` 内部 / 一次性迁移脚本 / `phase1_gate` 启动钩子三者语义完全不同：前者是每调用一次的运行时守卫, 后两者是一次性迁移动作), Tasks T3b 的验收落点 SC-3「label 非空且 `claims/<label>/` 有 active 时守卫拒绝 flip 并输出告警」用词「拒绝 flip」暗示的是运行时决策而非部署前迁移脚本。
- **影响**: 若实现者把守卫写进 `get_container_id()`（最贴合 proposal 字面「flip 前守卫」措辞的读法), `claim_lifecycle.acquire_claim`/`heartbeat`/`release_claim`（每次会话操作都调）、`phase1_gate.py`（每次 gate 判定）、`concurrent_tracks.py`（每次计数）都会新增一趟 git 子进程调用；若不这样写, SC-3 的「拒绝 flip」断言就无处附着（没有函数在运行时做这个决策）。两种读法互斥, proposal 没有二选一。

## Verdict

FAIL — 2 Critical + 1 Major + 0 Minor（2C/1M/0m）。R1 处置：3 closed / 1 partial / 0 open。

## Vote

REVISE

## 轮次记录

**读了什么**: proposal.md v2 全文逐行核对（Why/What/D1-D4/实验表/决策点/Impact/Tasks/SC/非目标/References）；R1 五份报告（本席 + aggregated）；`lib/collision.py` 全文（split_owner_container / track_to_claim_record / classify_claims / classify / linked_issue_overlaps）；`scripts/collectors/handoff_multibranch.py` 的 dedupe 模块注释块、`dedupe_latest_per_track_container` 全函数、`collect_handoff_multibranch` :690-730 装配段（含 `_classify_collision_summary` 调用点与 import 块 :135-149）；`lib/identity.py` 全文；`lib/coordination_ref.py` 的 `read_claims`/`write_claim` 段（:596-800 附近）；`lib/claim_lifecycle.py` 的 import 与 acquire/heartbeat/release 函数签名段；`scripts/release_gate.py` 的 import 块（核实是否直接消费 `get_container_id`）；`session-closer/scripts/handoff_autofill.py` 的 `get_identity` 调用行；`tests/test_handoff_multibranch_collision_dedupe.py` 的 `_build_repo` 端到端夹具、`test_both_latest_active_still_reports_self_multi_container`、`test_owner_segment_participates_in_grouping_key`；`RECOMMENDATION_RULES.md` rule 1.54 表格行；`.aria/repro/handoff-tracks-frozen-2026-09-05.json` 结构与首条记录。

**跑了什么**（均在 `/tmp/claude-1000/-home-dev-Aria/660cdd00-d2ad-4227-a5bb-5312810322f1/scratchpad/` 内脚本, 未改仓内文件, import 顺序 `sys.path.insert(0, ".../scripts"); sys.path.insert(0, ".../state-scanner")` 规避双 lib 包遮蔽）：
1. `r2_variantA.py`：用现有生产代码（未改动）在冻结语料上跑 `dedupe_latest_per_track_container` + `classify` — 复现 proposal 实验表 A 行（121, self_multi_container, 1 组），逐字一致。
2. `r2_variantB.py`：monkeypatch `split_owner_container` 为 v2 步骤 1 的两段式语义、dedupe 键沿用旧公式（不改），在冻结语料上跑 — 复现 proposal 实验表 B 行（122, cross_owner, 2 组），逐字一致。
3. `r2_repro.py`：完整实现 v2 D1 三步（两段式 split + `identity_key` + 全语料并查集 + 按 identity_key 分组比较 owner 等价类的新 `classify_claims`/`classify`）在冻结语料上跑生产路径 — dedupe 数字对（122，与 D 行一致），但 `kind`/`groups` 与 proposal D 行声称的 `self_multi_container` 不一致，实得 `cross_owner`（Finding R2-1）；逐 track_id 下钻定位到 `aria-submodule-gate-block-flip` 是分歧根源。
4. 全仓 grep `get_container_id`/`get_identity` 消费方 + 实读 `release_gate.py`/`handoff_autofill.py` — 核实 v2 Impact 表新增的两个消费方条目成立（Finding 3 partial 判定的依据）。
5. `git check-ignore` / `git log --oneline -- .aria/repro/...` — 核实冻结语料已入库、未被 gitignore（Finding 2 closed 依据）。

**未发现问题的项**: T1/SC-1 三条断言（`simonfish/bfe8285d`、`solo`、`a/b/c`）在 v2 两段式语义下核验成立；`_build_repo` 端到端夹具足以构造 SC-2 的「真实两段式两人两机」用例，不构成阻断；T6 冻结语料入库与 gitignore 状态核实无误；SC-8 的 additive 兼容声称因为 `identity_advisories` 字段和读取代码目前均不存在，无法找到「已违反」的证据，不构成可报告的 finding（既非 closed 也非可判定 open，不计入 R1 三态，因为它不是 R1 遗留项）。
