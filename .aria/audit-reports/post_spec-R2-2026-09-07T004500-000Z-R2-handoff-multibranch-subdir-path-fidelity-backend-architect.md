---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-07T00:55:02.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [backend-architect]
---

# post_spec R2 单席报告 — backend-architect (handoff-multibranch-subdir-path-fidelity, Aria #195)

席位透镜: 数据契约与实现可行性 (字段语义变更的向后兼容与消费方枚举完整性 / 错误路径穷举 / 伪代码与真代码对齐)。全部行号对插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/skills/state-scanner/` (= aria `origin/master` `301641b`), 实测 `git -C /home/dev/Aria/aria rev-parse HEAD` = `301641b`。proposal 自述一律未采信, 逐条对真文件核。本轮只审不改, 未编辑任何仓库文件 (守卫探针在 scratchpad 内存 monkeypatch, 零落盘到仓内)。

## 审计结论

### Decisions

- [minor] testing/SC-10 基线计数 78 与 R1 major `60e465ad` 落地: 在真 git checkout 跑 SC-10 那条命令得 `Ran 78 tests in 4.695s / OK`, 单跑 `test_p1_layer_h` 得 `Ran 24 tests / OK`。R1 的 73→78 订正属实且已落地 (证据: `/home/dev/Aria/aria/skills/state-scanner/tests`, 本轮实跑)
- [minor] architecture/基线冻结与主仓 gitlink 实况: `aria` HEAD = `origin/master` = `301641b`; 主仓 `git ls-tree HEAD aria` 与 `ls-tree origin/master aria` 均 `301641b` ⇒ 头部「主仓实况」行与 Task 5.2「从 301641b 前进, 严禁回退 0545f86」成立, R1 conflicted `4c05b95a` 已机械闭合
- [minor] implementation/平铺仓零行为变化的数据前提: 主仓 `docs/handoff/` 无子目录、190 份顶层 `.md`; `tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 996 条 track 中 `filename` 含 `/` 为 0、非 ASCII 为 0 ⇒ §7「冻结语料不需重生成」的数据面成立 (证据: `find`/`json` 实测)
- [minor] implementation/F1 与四处硬编码前缀复核: `scan.py:186` 的拼串与 proposal 引用的代码片段逐字一致, `:126` 定义 / `:255` 调用 / `:199-200` 对空 SHA `continue` 并注释判为「a real answer」均属实; collector 只有两个 return 点 (`:596` fail-soft、`:755` 正常), 故 §4「unreadable_count 恒存在」的错误路径面 (Task 2.4 + SC-14) 是完整的
- [minor] implementation/Rule #6 结论侧复核: `lib/collision.py:483-486` 的 `collidable` 过滤确实排除 `owner_container == "unknown"` ⇒ 删掉假 legacy 行不动 `collision.kind`, 闸门面 (`SKILL.md:149`/`:153`) 不受影响 —— 该结论成立 (但其证据句有误, 见下 Issues 第 6 条)

### Issues

- [critical] implementation/§2.5 守卫判据 · Task 2.5 · SC-15: Task 2.5 硬性规定判据为 `relpath != filename` 并禁用替代写法, 但该式对**任何缺 `relpath` 的 track 恒真**。用 `tests/test_p1_layer_h.py:230-240` 的 `_active_track` 形状实跑打了守卫的 `write_latest_md`, 输出行变成 `**Latest**: (pointer 不可用) — track=my-spec`, 即 `:270` 的 `assertIn("2026-05-20-my-spec.md")` 由绿转红; 该测试当前 24 tests OK。spec 未规定「`relpath` 缺失 ⇒ 视为顶层」, 无任何 SC 覆盖该分支 (SC-15 两个布局都由新 collector 端到端产出, `relpath` 恒在), 且 SC-10 点名的回归命令四个模块里**不含** `test_p1_layer_h` —— 而 §2.5 改的正是它唯一覆盖的模块。跨版本读盘快照 (老 collector 产出) 同理会让每一条 pointer 静默降级 (证据: `latest_md_writer.py:110-148`; `tests/test_p1_layer_h.py:230-240,246-270`; proposal.md:201,238,247)
- [major] architecture/§2.5 守卫落点 · SC-15 substitute 权重: 全插件树 + 主仓 grep `write_latest_md`, 命中只有 `latest_md_writer.py:28,259` / `writers/__init__.py:9,12,14` / `references/layer-l-integration.md:101` / `tests/`, **零生产调用方**; 真实的 D.3 `latest.md` 维护是 AI 按 `skills/phase-d-closer/references/handoff-mechanics.md:102-129` 手改 (子步骤 1 History prepend + 子步骤 2 指针判定表 `:114-124`), 该 SOT 全文不提这个 writer。后果两面: (a) A′ 裁定把守卫写成「必需配套」、Impact.Risk 与 rule6_note 把 SC-15 计为第十条 baseline-failing 实体, 三者都建立在「writer 在生产被调」这个未核实前提上 (memory `feedback_completion_signals_vs_runtime_invocation` 形态); (b) 真正会写出指针的那条路径不在本 spec 触点内, 子目录采用方的「诚实降级」承诺在该路径上无着落 (证据: 插件树 grep; handoff-mechanics.md:102-129; layer-l-integration.md:101,107)
- [major] architecture/§5 消费方枚举 · §7 向后兼容: §4 把「读不到」的行移出 `tracks[]` 会同时改动 `exists`(= `len(tracks) > 0`, `handoff_multibranch.py:748`) 与 `len(tracks)`, 而 §5 表与 §7 只讨论了 `filename` / `track_id` / `legacy_count` / `unreadable_count`。自查 grep 出三处未列入的消费方, 且都是**处方性 AI 判定面**: `references/rules/advanced-rules.md:443-444` (`multi_terminal_follower_detected` 以 `tracks_multibranch.exists: true` + `len(tracks) >= 2` 为触发条件)、同文件 `:511-512` (D.3 follower 规则同条件)、`skills/phase-d-closer/references/handoff-mechanics.md:120` (单 track 判定 = `exists == false 或 len(tracks) <= 1`, 直接决定指针改不改)。触达面窄 (只在**真**不可读文件上收缩, 含 §7 自认的非 UTF-8 名) 但确实存在, 而 §5 自称「grep 全 skill 树 + 主仓 + R1 逐行复核」, 表的完整性正是它的载重点 (证据: advanced-rules.md:443-444,511-512; handoff-mechanics.md:120; handoff_multibranch.py:748)
- [major] testing/SC-2 · SC-12 新键豁免清单: 2026-09-07 A′ 修订给每行 TrackEntry 新增 `relpath`, 但两条零差异断言没跟着改 —— SC-12 逐字写「除 `unreadable_count` 新键外**零差异**」(proposal.md:234), SC-2 写「`tracks[]` / `legacy_count` **逐字段相等**」且用例名为 `test_flat_repo_byte_identical_to_frozen_baseline` (:224), Impact.Risk 第 6 条同写「与改前**逐字节相同**」(:191)。改前基线由无 `relpath` 的旧代码产出, 改后每行多一个键 ⇒ 三处断言在采纳的设计下**恒红**, 与「反事实: 解析写错才红」相矛盾。属 rework 后的下游 AC 漂移 (memory `feedback_spec_rework_leaves_downstream_ac_drift`) (证据: proposal.md:191,224,234)
- [major] testing/SC-2 · SC-12 基线的 origin 时变性 (risk): R1 把基线从活文件改成「同工作区双跑」, 但没治时变的**根**。collector 枚举全部 `refs/remotes/origin/*` (`handoff_multibranch.py:202-208`, 按 committerdate 排序后取 cap), `tracks[]` 从不去重、每 (branch, file) 一行 (模块 docstring `:14`,`:54`)。主仓 `docs/handoff/` 现有 190 份顶层 `.md`, 故 Phase B 一旦把 feature 分支推上 origin, 「改后」那次扫描就凭空多约 190 行; 同伴容器 (双子星) 往 master 推交接同样加行, 而 Phase 0.5 `remote_refresh` 会 `fetch --prune` 保证看到最新态。SC-12 的「零差异」与 SC-2 的活体变体因此仍会假红。需要固定分支集 (离线模式 / 只比 before 分支集内的行 / hermetic 临时仓) 而非只换基线的落盘位置 (证据: handoff_multibranch.py:202-208,14,54; `ls docs/handoff/*.md | wc -l` = 190)
- [major] documentation/rule6_note 套件覆盖实测 · 头部 Rule #6 判定行: 「`ab-suite/state-scanner.json` 对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` 四词**零命中**」不成立。实测该文件 (唯一一份, 17551 B, 最后提交 2026-09-05T14:12Z, 早于 R1) 中 `tracks_multibranch` **命中 1 次**, 位于 `:214` 即 `/evals/12/prompt`, 问的正是 `tracks_multibranch.collision.kind` 与 coordination 闸门该跑什么命令; 另三词确为 0。committed blob 复核同为 1, 工作树干净。R1 decision `0f9dc120` 记「四席各自实测全 0 / 文件 15518 B」与现场两项都对不上 ⇒ 该交叉核验是失效的。按 audit-points 横切「数据可用性」条款, 机械 lookup 与 spec 数据断言不符属载重项。结论 (无需跑 AB) 因 `lib/collision.py:483-486` 仍成立, 但证据句必须订正, 且应说明 eval-12 为何不被本变更影响 (证据: aria-plugin-benchmarks/ab-suite/state-scanner.json:214; `git show HEAD:` 同值; proposal.md:11,246)
- [minor] documentation/§6.1 · Task 4.1 (schema `:1136`): Task 4.1 要在 `state-snapshot-schema.md:1136` 的 fail-soft 形状补 `unreadable_count`, 但该行现写 `collision: {"kind": "none", "groups": []}`, 而代码早退 dict 实为 `{"kind": "none", "groups": [], "identity_advisories": []}` (`handoff_multibranch.py:593`) ⇒ 改到同一行却把既有漂移原样留下, 与本 spec「契约与实现对齐」的立意相左 (证据: state-snapshot-schema.md:1136; handoff_multibranch.py:588-596)
- [minor] documentation/§7 additive 声明 · 待 owner 复议 2: 「A 案改既有字段取值语义**不属 additive**, 与 `snapshot_schema_version` 保持 1.0 不相容」与 SOT 自身不符 —— `state-snapshot-schema.md:46-48` 的 Additive/Breaking 两档只列「新增键 / 改名 / 改类型 / 删键 / 可选转必填」, 取值语义变更**不在任一档**; `:1070` 更有既有先例 (`coordination_fetch.success` 语义翻转, 明记「carried by plugin MINOR, NOT a schema_version bump」)。A 未被采纳故不载重, 但该论据同时出现在决策单第 2 条与 §待复议 2, 会污染 owner 的复议判断 (证据: state-snapshot-schema.md:46-48,1070; proposal.md:190; .aria/decisions/2026-09-07-...md:48)

### Risks

- [major] testing/SC-2 · SC-12 基线的 origin 时变性 — 同上 Issues 第 5 条 (以 risk 类型记, 因它不是断言写错而是环境噪声会持续假红)
- [minor] implementation/`_render_pointer_unavailable` 签名: §2.5 要求「增一条原因分支」, 但该函数现签名为 `(track_id, now)` 且原因文案硬编码在 `:164`, 落地必须改签名或加参数; spec 未点名, 属实现期易漏的小契约变更 (证据: latest_md_writer.py:151-169)
- [minor] implementation/`scan.py` offender 字段口径: A′ 下 `:186` 改读 `relpath` 后, 输出到快照的 offender/inconclusive dict 仍只带 `"filename"` (`scan.py:193,209`), 快照里将无法回答「实际探的是哪条路径」; spec 未规定是否同步 (证据: scan.py:184-212)

## Verdict

**FAIL** — Critical 1 / Major 5 / Minor 5 (另 5 条 decision 为核验通过项, 按 R1 同规则不计入缺陷计数)。

rationale: 唯一一条 Critical 落在 2026-09-07 新增的 §2.5 守卫本身 —— spec 用 Task 2.5「判据必须是 `relpath != filename`, 严禁字符串嗅探」把实现钉死在一个对缺字段不安全的谓词上, 实跑证明它会让一条当前为绿的既有断言 (`test_p1_layer_h.py:270`) 转红并把指针静默降级, 而 spec 既没规定缺字段语义, SC-15 又因端到端产出恒带 `relpath` 而覆盖不到, SC-10 点名的回归命令还恰好漏掉了这个模块。这不是措辞问题, 是「按 spec 字面实现就会坏」的方案缺口。

五条 Major 分两类, 都可在 Phase A 内改 spec 消解, 不需推翻 A′ 骨架:

1. **判据面 (3 条)**: SC-2/SC-12 的新键豁免清单没跟上 A′ (`relpath` 未豁免 ⇒ 恒红); 二者的基线仍随 origin 分支集变动 (Phase B 自己推分支即加约 190 行) ⇒ 假红; rule6_note 的「四词零命中」被单条 grep 证伪 (`tracks_multibranch` 在 eval-12 prompt 里命中 1 次, 且 R1 四席交叉核验的文件大小与命中数都对不上现场)。
2. **方案面 (2 条)**: 守卫所在的 `write_latest_md` 全树零生产调用方, 真实 D.3 指针由 AI 按 `handoff-mechanics.md` 手改 ⇒ 「必需配套」与 SC-15 的 substitute 权重前提未核实; §5 消费方表漏掉 `exists` / `len(tracks)` 的三处处方性消费方 (两条推荐规则 + D.3 指针判定表), 而该表的完整性正是 §7「向后兼容」的唯一支撑。

R1 遗留复核: 2 条 critical 与 15 条 major 我逐条对 v3 正文核过, **均已在正文落地而非批注** —— SC-10 计数 78 实跑复核通过、`_same_branch_head_unreachable_tracks` 符号三处已更正且与真代码逐字一致、mv 日期归因与 SC-4 三断言已改写、pointer 任意深度排除已改记为现状、SC-9 已拆 (a)(b) 两条、SC-13/SC-14 已补、主仓 gitlink 实况已订正。新引入的矛盾集中在 A′ 修订这一刀: 它更新了 §2.5 / SC-15 / Tasks, 却没回扫 SC-2 / SC-12 / §5 / rule6_note 这些被它改变前提的下游条目。

## 轮次记录

### Round 2

- Agents: backend-architect (五席之一, 本报告为单席产出; 我是本轮新席位, 不继承 R1 任何结论)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 13 条 (Decisions 5 / Issues 8 [critical 1 · major 5 · minor 2] / Risks 3 [其中 1 条与 Issues 第 5 条同体, 按 type 双记不重复计数]; 计入缺陷计数的为 Critical 1 / Major 5 / Minor 5)
- 机械核验清单 (本轮实跑, 非引用): `python3 -m unittest` 两次 (78 OK / 24 OK) · 全插件树 + 主仓 `grep write_latest_md` · `grep -c tracks_multibranch ab-suite/state-scanner.json` (工作树与 `git show HEAD:` 各一次) · 守卫谓词对 `_active_track` 形状的 in-memory 探针 · `git ls-tree` 三处 SHA 核对 · 冻结语料 996 行的 slash/非 ASCII 统计 · `docs/handoff/*.md` 计数 190 · `refs/remotes/origin/*` 分支枚举
- Vote: **REVISE**
