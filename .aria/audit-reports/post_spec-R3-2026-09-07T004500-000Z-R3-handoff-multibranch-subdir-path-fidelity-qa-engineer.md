---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-07T03:50:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [qa-engineer]
---

# post_spec R3 — qa-engineer 单席报告

> 路径约定: 下文 `SS/` = `/home/dev/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/skills/state-scanner/` (= aria 子模块 `301641b` 对应副本, 行号以此为准); `PROP` = `/home/dev/Aria/openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md`。
> 席位透镜: SC 可证伪性 (逐条反事实) / hermetic 用例可构造性 / 既有测试与冻结语料受影响面 / 缺哪些负向测试 / 已知失败项处置。
> 本席为 R3 新席位, 不继承 R1 / R2 结论; 全部断言经实读或实跑。

---

## 审计结论

### Decisions

- [minor] testing/R2 处置落地复核: R2 的 3 critical + 10 major + 9 minor 逐条比对聚合报告与 v4 正文, **全部落进正文而非批注**, 未见「改一处引入另一处矛盾」。抽验: `6f8fa9f7` → §2.5 缺键兜底行 + Task 2.5 (b)(c) + SC-15 布局 3 + SC-10 补 `test_p1_layer_h`; `88a49037` → SC-15 细则布局 2 夹具组成 + (f) 移除; `d1f01126` → §2.5 可达性块 + §5 writer 行 + Impact.Risk + 待复议 2; `112b4299` → SC-12a / SC-12b 拆分; `94935605` → §6.6 + Task 4.4 + SC-11(h); `d58dfb65` → Task 5.1 16 行表 + References 删除错误兜底句 (证据: `PROP:12,124-146,183-195,237-238,247,281-296`; `.aria/audit-reports/post_spec-R2-…-aggregated.md:37-182`)
- [minor] testing/载重事实独立复跑一致: (1) `aria-plugin-benchmarks/ab-suite/state-scanner.json` 现 **17551 B / `tracks_multibranch` 命中 1** (`:214`), `handoff_multibranch`/`legacy`/`basename` 均 0; `git show 5697477^:` 得 **15518 B / 命中 0**; `813e82c` 得 17551 B / 命中 1 —— 头部与 rule6_note 的机械闭合成立, 且该 prompt 确把 `collision.kind` 的值写死在题面 (结构上测不到 collector 输出变化)。(2) F2: 临时仓实跑 `git ls-tree -r --name-only` 输出 `"docs/handoff/2026-\346\265\213\350\257\225.md"`, `Path(path).name` 得带尾引号串并在 `.endswith(".md")` 处 DROPPED —— **静默漏扫**成立, `-z` 输出为原样路径 + 尾随 NUL。(3) 子目录 hermetic 仓跑 `scan.py`: **exit 10**, 产出 `legacy:master:2026-09-05-sub.md` 假 track、`updated_at` 为**空串**、`legacy_count=1`、kind `handoff_multibranch_git_show_failed` —— §Why 三层后果与 SC-1/SC-4 后半的前提全部成立。(4) 真 git checkout `/home/dev/Aria/aria` (HEAD 实测 `301641b1c893477f387a1f85d1e90d105ebf0db9`) 跑 SC-10 五模块得 **`Ran 102 tests … OK`** (证据: `SS/scripts/collectors/handoff_multibranch.py:277-288`, `SS/scripts/scan.py:119`)
- [minor] testing/A′ 与来源一致性核实通过: issue-195 原文第 41 行「`filename` / `track_id` 等需要 basename 的字段**另行派生**」与 `.aria/triage-comment-195.md:53`「`filename` 字段另派生 basename … `legacy:<branch>:<filename>` 建议相对路径防同名碰撞」逐字复核, A′ + legacy track_id 用 `rel_path` 忠实于两个来源; triage-report-195.json `verdict=confirmed / severity=major` 属实 (证据: `PROP:80-95`)
- [minor] testing/hermetic 可构造性总体通过: 五族用例的构造技术在仓内均有先例 —— 临时仓 + `git update-ref refs/remotes/origin/<branch>` (`SS/tests/test_handoff_multibranch_collision_dedupe.py::_build_repo`)、monkeypatch `_run` / `_list_origin_branches` (模块级全局, 可直接改属性)、`collect_handoff_multibranch(now=…)` 入参 (`SS/scripts/collectors/handoff_multibranch.py:559`)。`scan.py` 在 hermetic 仓 0.23s 跑完 (SC-12b 可行); `_same_branch_head_unreachable_tracks` 的四道前置 (`SS/scripts/scan.py:166-174`) 均可在夹具里配齐, 且全树**无既有测试**调用该函数 ⇒ SC-6 是该跨文件消费方的首个覆盖 (证据: `PROP:227-229`)
- [minor] testing/冻结语料不受影响核实通过: `SS/tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 996 行, `filename` 含 `/` 者 **0**、非 ASCII **0**、行键恰为八字段; `SS/tests/fixtures/freeze_corpus.py:29` `FIELDS` 八元组不含 `rel_path` ⇒ SC-2 走投影的口径成立。主仓 `docs/handoff/` 顶层 `.md` **190 份**、子目录 `.md` **0 份** ⇒ §7 平铺仓零变化与 SC-12a 的 190 行推算属实。另: `SS/tests/fixtures/reference-snapshot-aria.json` 虽仍是六键/八字段旧形状, 但 `references/json-diff-normalizer.md:196-200` 明记它「not wired into automated tests」且 `state-snapshot-schema.md:475-481` 有「不作为副作用重采样」的成文先例 ⇒ 本 spec 不动它是正确的, 不构成 finding

### Issues

- [major] testing/SC-10 既有测试基线 (日历时效性): SC-10 把 `Ran 102 tests … OK` 钉成验收判据, 并明写「出现任何失败都要逐条 `git log -- <file>` 归因, **不得预先豁免**」。但点名集里的 `SS/tests/test_handoff_multibranch_collision_dedupe.py` 有两条测试**只靠墙上时钟**: 夹具行 `:381-382` 写死 `2026-08-15` / `2026-08-10`, 调用处 `:386` 未 pin `now`, 而 `lib/collision.py:225-241` 的 `layer_h_is_fresh` 按 `LAYER_H_ACTIVE_WINDOW_DAYS = 30` (`lib/constants.py:88`) 丢弃过窗行。本席实测: 今天 (2026-09-07) 21/21 OK; 把 `lib.collision.datetime.now` 换成 2026-09-09 后 **2 条转红** (`TestCrossOwnerRealCollisionSurvivesDedupe::test_both_latest_active_different_owners_still_reports_cross_owner` 得 `'none' != 'cross_owner'`; `TestBoardAndCollectorAgreeOnCollisionCount::test_real_collision_produces_matching_board_collision_line_count`), 零代码改动。⇒ Phase B 若在 2026-09-09 之后执行, SC-10 **结构上不可满足**, 而它给的归因手段 (`git log -- <file>`) 只能证明「本 cycle 没碰这个文件」, 说不出为什么红, 于是最省事的出路正是本文自己警告过的「实施者顺手削断言」。建议: SC-10 的基线口径补第三类既有失败的归因路径 (Layer H 30 天窗 + 夹具未 pin `now`, 附本条复现法), 并明确该类红**不阻断本 spec**; 是否顺手给这两条测试补 `now=` 属另一变更面, 交 owner 裁 (Rule #10, 不得由实施者临场判) (证据: `SS/tests/test_handoff_multibranch_collision_dedupe.py:366-404`, `SS/lib/collision.py:241`, `SS/lib/constants.py:88`, `PROP:232`)
- [major] testing/SC 集缺 `collision.kind` 覆盖: 本文把 `collision.kind` 由 `none` 翻到 `cross_owner` 列为 (a) Rule #6 从 substitute 改判**照跑**的唯一新证据 (头部 Rule #6 行 + rule6_note 反证 2)、(b) 一条独立 Impact.Risk、(c) §5 中 `SKILL.md:149/153` 闸门 / `advanced-rules.md:544` 规则 1.54 / `fetch_gate.py:175-188` 三个处方消费方的**触发条件本体**。本席独立复跑确认翻转为真: 临时仓 (顶层 `2026-09-01-x.md` = `simonfish/c1` active + `archive/2026-09-02-y.md` = `aria-runner-bot/c2` active, 同 track_id, `now=2026-09-05`) 改前 `kind=none / groups=0 / legacy_count=1 / 1 条 git_show_failed`, 枚举层改交相对路径后 `kind=cross_owner / groups=1 / legacy_count=0 / 零 soft_error`。**但 SC-1…SC-16 无一条断言 `collision.kind`, Tasks 也无对应条目** —— 全 spec 唯一涉 collision 的 SC-7 还被明标为「假想输入的特性化测试」。⇒ 一个自认会改动、且改动面直通闸门的量, 验收上零覆盖: 实现若因 Layer H 过窗、`owner_container` 解析路径变化或 collidable 过滤改动而没翻转, 没有任何断言抓得到。建议补 SC-17 (顶层+归档同 track_id 异 owner 的 hermetic 仓, 改前 `none`、改后 `cross_owner`, **必须 pin `now`**, 入参已存在于 `SS/scripts/collectors/handoff_multibranch.py:559`), 并把它记进 rule6_note 的 baseline-failing 实体 (证据: `PROP:12,169-171,190,301-303`; `SS/lib/collision.py:483-486`)
- [major] testing/SC-15 与 rule6_note 的 baseline-failing 资格记述有误: rule6_note 写「SC-15 的资格改由布局 2 的 (d)(e) + 布局 3 的 (g) 撑住」。本席按 SC-15 细则的夹具规格在 `301641b` 上实跑三布局: **布局 2** (归档 active + 顶层一份 `status=done`) 基线下归档件因 git show 走错路径降级为 `legacy` ⇒ active 数为 0 ⇒ `write_latest_md` 返回 `action="skipped"` 写零 track 占位页 ⇒ `**Latest**: [` 不出现、`collect_handoff` 的 kinds `[]`、`latest_source="mtime"` ⇒ **(e) 恒绿**, (d) 的第一个合取项也恒绿, 只有第二个合取项 (文案含「目标在子目录」) 是红的; **布局 3** (八字段无 `rel_path` 的 dict) 基线下 `_render_pointer` 无守卫必写真指针 ⇒ **(g) 恒绿**。⇒ 三个被点名的断言里两个在基线上就成立, SC-15 的实体资格只由 (d) 后半撑住; 连带 Task 1.2「新测试文件 … 对 `301641b` **全红**且红在正确断言上」对 `::test_pointer_roundtrip_toplevel` 与 `::test_pointer_written_when_rel_path_key_absent` 不可满足。修法 (零设计改动): 把 (e)(g) 与布局 1 按本文既有口径标成「过修守卫 / 回归锁」(与 SC-7、SC-4 前半、SC-8 前半同级, 不计入实体), 并把 Task 1.2 的「全红」限定到它自己列举的四族 (证据: `PROP:283-296,304`; `SS/scripts/writers/latest_md_writer.py:110-124,151-169`; `SS/scripts/collectors/handoff.py:437-451`)
- [major] testing/SC-13(b) 与 SC-4 依赖的提交日期未给 pin 机制, 不满足时 (b) 变假绿: SC-13(b) 断言「两行 `updated_at` **各自等于自己那条路径的提交日**, 互不相同」, 括注里只写「两文件在不同提交里落盘, 提交日期不同」, 没说怎么做到。本仓现成夹具模板 `_GIT_ENV` (`SS/tests/test_handoff_multibranch_collision_dedupe.py:174-183`) 只 pin 姓名/邮箱, **不 pin `GIT_AUTHOR_DATE`**, 而 `%aI` 是秒级: 本席实测同一脚本内先后两次 commit, `git log -1 --format=%aI` 对顶层与归档两条路径返回**同一值**。此时基线 (拼顶层 basename 路径) 读到的也正好是同一日期 ⇒ (b) 在改前**也成立** ⇒ 该断言从 baseline-failing 退化成恒绿。SC-4 的三条断言 (顶层 2026-05-09 → `git mv` 2026-08-15) 同样依赖逐 commit 可控日期。建议在 SC-4 / SC-13 的夹具描述里显式要求逐 commit 设 `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` (证据: `PROP:226,239`; `SS/scripts/collectors/handoff_multibranch.py:310-327`)
- [minor] architecture/§5 消费方枚举漏 `handoff_worktrees` collector: §5 标题自述「起草时 grep 全 skill 树 + 主仓; R1 rework 逐行复核」, 且 §7「向后兼容」以该表完整性为唯一支撑。但表内无 `SS/scripts/collectors/handoff_worktrees.py` —— 它 `:82` 直接 import 复用 `handoff.py::_resolve_latest`, `:291` 对每个 worktree 调用, `:59-60` 明记会按 worktree 路径前缀发出同一条 `handoff_pointer_target_missing`。即 latest.md 的 pointer 往返有**两个**读侧消费面, §5 与 SC-15 只覆盖 `collect_handoff` 一个。影响同型 (守卫修好即两者同修), 故记 minor; 但既然表被当成向后兼容的证明面, 应补一行 (证据: `SS/scripts/collectors/handoff_worktrees.py:59-60,82,291`; `PROP:160-172`)
- [minor] testing/SC-10 点名集仍漏三个直接消费面: R2 把 `test_p1_layer_h` 补进点名集的判据是「它是唯一 import `write_latest_md` 的测试, 也是改动落点」。同一判据下仍漏: `SS/tests/test_collision.py:439,460` (端到端真 `collect_handoff_multibranch`, 且 `:445` pin `set(coll.keys())`)、`SS/tests/test_max_branches_resolver.py` (同样 import 该 collector)、`SS/tests/test_scan_integration.py` (读 `tracks_multibranch`, 而本 spec 改 `scan.py:186`)。三者目前只被尾句「全量 discover 另跑」兜底 —— 与被点名的五模块不是同一强度的判据 (证据: `PROP:232`)

### Risks

- [minor] testing/dedupe tie 的新可观测面无断言 (已知并已交 owner): A′ 下同 `(track_id, identity_key)`、同 `updated_at`、同 `branch`、同 basename 而目录不同的两行, 四级键 (`SS/scripts/collectors/handoff_multibranch.py:428-455`) 全并列 ⇒ `max()` 回退迭代顺序, 与 docstring `:438-452` 及 `state-snapshot-schema.md:1126` 宣称的 build-order 不变性相悖。本文已在 §5、Impact.Risk、待复议 4 附问里三处登记并明确「本 spec 不加断言」, 处置合规 (Rule #10 交 owner); 本席只记风险: 改前两行因串读逐字段相同故选谁都一样, 改后代表行的 `status`/`phase` 可不同并经共享 dedupe 传导到 collision 与 track_board —— 与上面「collision.kind 零覆盖」叠加, 意味着 collision 侧的行为变化在本轮**完全没有测试面** (证据: `PROP:167,190,331`)
- [minor] testing/SC-12b 的退出码不可控已正确删除, 但 hermetic `scan.py` 仍恒 exit 10: 本席实测子目录临时仓跑 `scan.py` 得 exit 10 (`remote_refresh` 等 collector 在无真 remote 的临时仓必 soft_error)。SC-12b 已按 R2 `112b4299` 把断言收敛到 kind 级, 结论正确; 仅提示 Phase B 记录证据时不要顺手写「exit 0」当佐证 (证据: `PROP:238`; `SS/scripts/scan.py:431`)

---

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **4** / Minor **4** (含 2 条 risk; 另 5 条 decision 不计入缺陷计数)。

rationale: 方案骨架 (A′ = `filename` 保持 basename + additive `rel_path` + 四个 git 路径消费方改读 `rel_path` + git show 失败不再伪造 legacy + 写侧守卫) 经本席逐条实读与四组独立 hermetic 复跑, **未发现设计错误, 也未发现会破坏既有消费方的改动**: 冻结语料零子目录零非 ASCII、既有五模块今日 102 OK、`reference-snapshot-aria.json` 按成文先例不需重采、`_render_pointer_unavailable` 的文案无测试断言依赖、fail-soft 早退只有一处 (`:596`) 故「`unreadable_count` 恒存在」两处改到即闭合。R2 的 3 critical + 10 major 全部在正文落地且未引入回填矛盾。

四条 Major 全部落在**验收面而非设计面**, 且两条是本轮新透镜 (日历时效性 / 反事实基线实跑) 才照出来的: (1) SC-10 的固定基线在 2 天后自行不可满足; (2) 本 spec 自认最要紧的行为变化 `collision.kind` 零 SC 覆盖; (3) SC-15 三个被点名的实体断言里两个在基线上恒绿; (4) SC-13(b) 在夹具日期同秒时退化为恒绿。四条修法都不触碰设计, 只改 SC/Task 措辞与夹具规格, 合计工作量小。

post_spec `blocking: false`, 本 verdict 不硬阻断流程; 但按 Rule #10, 上述四条不得由实施者以「代码面小 / 时间紧」自行降格或跳过, 尤其 SC-10 那条的处置 (是否给既有测试补 `now=`) 属另一变更面, 须 owner 裁。

---

## 轮次记录

### Round 3

- Agents: qa-engineer (本报告为五席之一, 单席视角)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: **10** (Decisions 5 / Issues 6 / Risks 2 中去重后 Issues 6 + Risks 2, 合计缺陷类 8, decision 5 不计入; Critical 0 / Major 4 / Minor 4)
- Vote: **REVISE** (Major > 0)

本轮实跑清单 (全部在 scratchpad 内执行, 未改动任何仓库文件):

1. `SS/tests` 跑 `test_handoff_multibranch_collision_dedupe` → 21 OK; 把 `lib.collision.datetime.now` 换成 2026-09-09 重跑 → 21 run / **2 failures**
2. `filter_layer_h_fresh` + `classify` 直调,  now = 09-07 / 09-09 / 09-10 / 09-15 → `cross_owner → none → none → none`
3. 临时仓复现 collision 翻转: 改前 `none/0/legacy_count=1/1 soft_error` → 枚举层交相对路径后 `cross_owner/1/0/0`
4. 临时仓复现 F2: 默认 ls-tree 引号+八进制转义, `Path().name` 带尾引号 → `.endswith(".md")` DROPPED; `-z` 输出原样路径 + 尾随 NUL
5. 子目录 hermetic 仓跑 `scan.py` → exit 10 / 假 legacy / `updated_at=''` / `handoff_multibranch_git_show_failed`
6. SC-15 三布局在 `301641b` 上的基线行为 → 布局 2 `action=skipped`、kinds `[]`; 布局 3 真指针照写
7. 同秒双 commit 的 `%aI` → 顶层与归档两条路径取值相同
8. 真 checkout `/home/dev/Aria/aria` (HEAD `301641b`) 跑 SC-10 五模块 → `Ran 102 tests … OK`
9. `ab-suite/state-scanner.json` 三版本字节数与命中数 (`当前` / `5697477^` / `813e82c`)
10. 冻结语料 996 行的 `filename` 斜杠与非 ASCII 统计; 主仓 `docs/handoff/` 190 顶层 / 0 子目录
