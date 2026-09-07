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
timestamp: 2026-09-07T03:24:48.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [backend-architect]
---

# post_spec R3 — backend-architect (数据契约与实现可行性)

审计对象: `openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` (v4, R2 rework 后)。本席为 R3 新席位, 不继承 R1/R2 结论; 全部事实自行实读或实跑, 行号一律以插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` 副本 (= `301641b`) 为准。

## 审计结论

### Decisions

- [minor] testing/R2 3 critical + 10 major 正文落地复核: 逐条核对 13 条, **全部落进正文而非批注**, 且未见「改一处引入另一处矛盾」。抽验: `6f8fa9f7` → §2.5 表新增「`rel_path` 缺失语义」行 + Task 2.5(b) + SC-15 布局 3 + SC-10 并入 `test_p1_layer_h`; `d1f01126` → §2.5 可达性块 + §5 writer 行限定 + Impact.Risk + 待复议 2; `88a49037` → SC-15 细则布局 2 + 「为什么必须留顶层那一份」+ (f) 移除; `112b4299` → SC-12a/SC-12b 拆分; `d02ec3f0` → SC-2 投影口径 + SC-16 新增; `94935605` → §6.6 + Task 4.4 + SC-11(h); `d58dfb65` → Task 5.1 十六处表 + 删除「三条 check 兜底」假陈述 (证据: proposal.md:16,124-145,177-190,226-244,264-294)
- [minor] architecture/载重事实独立复跑: 本席自建探针与临时仓复跑, 六项全部与 proposal 陈述一致 —— (1) `collision.kind` 改前 `none` / 改后 `cross_owner`(groups 1), legacy 假行确因 `owner_container == "unknown"` 被 collidable 过滤排除; (2) 两条同 id legacy 行 2 进 2 出、`legacy_passthrough=2`, 「不折叠」为恒真 (R2 `3cb2cf2b` 的订正成立); (3) `git ls-tree` 默认对非 ASCII 名加引号 + 八进制转义, `-z` 原样输出; (4) pathspec `-- docs/handoff` 不外泄 `docs/handoff-extra/c.md` (前缀守卫确属「理论上不会出现」); (5) SC-10 五模块 `Ran 102 tests ... OK`; (6) `ab-suite/state-scanner.json` 17551 B / `tracks_multibranch` 命中 1 (`:214` 且题面写死 `collision.kind` 取值), `git show 5697477^:` = 15518 B / 0 命中, `813e82c` = 17551 B / 1 命中 —— rule6_note 的机械闭合叙述准确 (证据: `handoff_multibranch.py:480-486,521-524`; `lib/collision.py` `filter_layer_h_fresh`/`classify`; `aria-plugin-benchmarks/ab-suite/state-scanner.json:214`)
- [minor] architecture/A′ 骨架与真代码结构对得上: 自 grep 复核 —— 四个 git 路径消费方 (`handoff_multibranch.py:301` / `:321` / `:329-336` / `scan.py:186`) 确为全部, 无第五处硬编码前缀; `filename` 的代码消费方恰为六处 (`scan.py:180,193,209` · `latest_md_writer.py:116,143,213`) 加 dedupe 排序键 `:455`; `legacy_count` 在 `tests/` 外零代码消费方; 全树无对 `tracks_multibranch` 精确 key set 的断言, `validate_schema_doc.py` 自述只做顶层 key 粒度 ⇒ 新增 `unreadable_count` / `rel_path` 不会机械打红既有断言 (证据: `scripts/validate_schema_doc.py:8-23`; `references/json-diff-normalizer.md:196-200` 记 `reference-snapshot-aria.json` 为「manual-compare, 未接自动测试」)
- [minor] architecture/`collision.kind` 翻转的窗口限定 (支持性观察, 不构成缺陷): `filter_layer_h_fresh` 的窗口为 30 天 (`lib/constants.py::LAYER_H_ACTIVE_WINDOW_DAYS`), 探针实测把归档行日期改成 2026-05-02 后 `fresh=1`、`kind` 回到 `none` ⇒ 「归档件转真 track 就翻 `cross_owner`」只在归档行 `updated_at` 落在 30 天窗内时成立。proposal 用的是「**可能**突然开始看到并发碰撞告警」, 措辞没有过度承诺, 本项仅记录

### Issues

- [major] testing/Task 2.1 枚举层返回契约 · SC-10 点名集: Task 2.1 与 SC-9(b) 要求 `_list_handoff_files` 从「分支级错误通道」改成可携带 per-item 错误 (proposal 举例「第三个返回位」), 而 `tests/test_max_branches_resolver.py` 有**四处** `mock.patch.object(hmb, "_list_handoff_files", return_value=([], None))` —— 返回 2-tuple。主循环 `filenames, ls_err = ...` 一旦改成三值解包, 这四处必抛 `ValueError: not enough values to unpack`, 而 `collect_handoff_multibranch` 自述 "Never raises"。该模块本席实跑 **39 tests OK** (今为绿), 且**不在 SC-10 的五模块点名集**, 全文零次提及 (`grep -c` = 0) ⇒ 与 R2 critical `6f8fa9f7`(a) / minor `7cba5aa4` 同型 (点名集漏掉正被改动的那个消费方的测试), 只是换到另一条契约上。SC-10 尾句「全量 discover 另跑」是唯一兜底, 而 R2 已判定该兜底对同型问题不足。建议: SC-10 点名集补 `test_max_branches_resolver`, 或 Task 2.1 明写「保持 2-tuple + 注入 reporter」这一不破契约的实现路径 (证据: `tests/test_max_branches_resolver.py:286,300,316,332`; `collectors/handoff_multibranch.py:619-626`; proposal.md:104,272,273)
- [major] implementation/§3 · Task 2.2 · SC-6 — `scan.py:186` 的 `rel_path` 缺键契约未规定: §2.5 用四行篇幅为 writer 定死了缺键兜底 (`rel = track.get("rel_path") or track.get("filename")`), 但同一批改动里**第二个**新字段消费方 `scan.py:186` 只写了「必须显式改读新的 `rel_path` 字段」, 缺键行为空白。实测该行唯一的测试模块 `test_scan_integration.py::TestSnapshotSelfConsistencyAC5` (11 tests, 本席实跑 OK) 的夹具 `HEALTHY_TRACKS` 是三键手搓 dict (`track_id`/`filename`/`branch`), **无 `rel_path`**, 且其 `_mock_run` 对任何 `git log -1` 都返回同一个 SHA、**完全不看路径参数** ⇒ 两个方向都坏: 实现若照 `scan.py:181-182` 既有防御风格写 `if not rel: continue` 或写 `t["rel_path"]`, 这些今为绿的用例翻红; 实现若写 `.get()`, 用例照绿但**结构上无法分辨** `filename` 与 `rel_path` 谁被拼进了命令行。该模块同样不在 SC-10 点名集。诚实限定: 生产路径上 `tracks_data` 恒来自本次 collector 输出 (`scan.py:388`), 缺键不可达, 故这是 Phase B 的实施面与回归面缺口, 不是生产缺陷 —— 但正因不可达, spec 应显式写明「此处不需要 writer 那样的兜底」并把模块纳入点名集, 否则实施者只能猜 (证据: `tests/test_scan_integration.py:164-167,176-186`; `scripts/scan.py:180-187,388`; proposal.md:120,228,269)
- [major] documentation/Task 4.2 · SC-11(c) — `rel_path` 被记进错误的 docstring 块: collector 模块 docstring 有两个独立块 —— **顶层返回键表** `:16-31` (`exists`/`tracks`/`branches_scanned`/`legacy_count`/`collision`/`errors`) 与 **TrackEntry 块** `:35-44` (`track_id` … `filename` 在 `:42` … `legacy`)。`unreadable_count` 是顶层键, 记进前者正确; 而 `rel_path` 按本 spec 自身定义是**每行 track 多一个键** (§7), 归属后者。Task 4.2 写「`:14-31` 键表补 `unreadable_count` + `rel_path`」, SC-11(c) 更把它固化成验收断言「模块 docstring `:14-31` 键表已新增 `rel_path` 行」⇒ 照正确位置写文档的实现**判红**, 照 SC 写的实现则在机读契约里声明了一个并不存在的顶层键。§6 第 2 条原文只对 `:14-31` 提 `unreadable_count` (正确), 是 Task 与 SC 这两层把两个字段合并成一句时漂掉的 —— 与 R2 `d02ec3f0`「断言在采纳的设计下自我打红」同族 (证据: `collectors/handoff_multibranch.py:16-31,35-44`; proposal.md:186,199,235,274)
- [major] documentation/§6 · Task 4.1 · Task 4.2 — `track_id` 的机读格式无同步项: 本 spec 经 §What.2 与 SC-13 把 legacy id 从 `legacy:<branch>:<basename>` 改成 `legacy:<branch>:<rel_path>` (SC-13 直接断言 `legacy:<branch>:archive/x.md`), 但既有格式声明共四处 —— `handoff_multibranch.py:36` (TrackEntry 契约)、`:332` (`_make_legacy_track_id` **自身** docstring「Format: ``legacy:<branch>:<filename>``」)、`:494` (dedupe 的「legacy track_id 已内嵌 branch+filename」论据)、`state-snapshot-schema.md:1104` —— **无一进入 §6 的同步清单, 也不在 Task 4.1/4.2 的逐项列表里**, SC-11 亦无对应 grep。其中 `:332` 就在 Task 2.2 要改的函数头上, 改代码不改它等于当场留一条自相矛盾的注释。与 R2 `94935605` (standards SOT 第三态) 同型: 变更把一条既有文档陈述改成假, 而同步面没登记 (Rule #3) (证据: `collectors/handoff_multibranch.py:36,332,494`; `references/state-snapshot-schema.md:1104`; proposal.md:114,177-190,234-235,277)

### Risks

- [minor] architecture/§5 dedupe 行 · 待复议 4 推荐默认 — `schema:1126` 的 build-order 不变量: 本席探针实证 A′ 下的 tie 面确实可观测 —— 同 `(track_id, identity_key)`、同 `updated_at`、同 `branch`、同 basename 而 `rel_path` 不同的两行, 四级键 `(parse_ok, updated_at, filename, branch)` 全并列, `max()` 回退迭代顺序: 正序选中顶层那行 (`status=active`), 逆序选中 `archive/` 那行 (`status=done`)。改前两行因串读逐字段相同, 选谁都一样; 改后代表行的 `status`/`phase` 真会不同并经共享 dedupe 传导到 collision 与 track_board。proposal 已在 §5 与 Impact.Risk 记述此事并交待复议 4, 但**推荐默认是「不改排序键」**, 而该默认支下 §6/Task 4.1 没有任何一项去订正 `state-snapshot-schema.md:1126` 与 docstring `:438-452` 宣称的「pure function of the row's own fields / invariant to build order」—— 落地后这句对该输入形态即为假。建议: 默认支加一条文档订正项 (把不变量限定为「同 `rel_path` 前提下」), 与「改排序键」支互斥 (证据: 本席 dedupe 探针; `collectors/handoff_multibranch.py:428-455,438-452`; `references/state-snapshot-schema.md:1126`; proposal.md:165,212,318)
- [minor] architecture/§5 消费方表 — `collision.identity_advisories` 未登记: `identity_drift_advisories` 对 `status == "legacy"` 行直接 `continue`、只吃带真 owner 的行, 故 §4 删假 legacy 行不动它 (减法为零), 但**加法有**: 子目录件转成带真 `owner_container` 的 track 后可新增/改写 advisory 条目 (含 `first_seen`/`last_seen`)。该字段有自己的处方性消费面 (`references/rules/advanced-rules.md:574` 把它作为规则输入; `references/layer-l-integration.md:29` 规定 AI 见到非空该怎么说), 而 §5 表只登记了 `collision.kind`。性质是信息级 ⚪、不进 `kind`/`groups`, 故按 minor 记; 但 §7「向后兼容」的唯一支撑就是 §5 表的完整性, 与 R2 `cecc06af` 同一判据 ⇒ 建议在 §5 补一行并在 CHANGELOG 的 Changed 段一并写明 (证据: `lib/collision.py::identity_drift_advisories`; `collectors/handoff_multibranch.py:731`; `references/rules/advanced-rules.md:574`; `references/layer-l-integration.md:29`; proposal.md:167-172)

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 4 / Minor 2 (另 4 条 decision 不计入)。

rationale: 方案骨架经本席独立复核**站得住**: A′ 的三件套 (`filename` 保持 basename + additive `rel_path` + 四个 git 路径消费方改读它) 与 issue-195 原案一致, 与真代码结构逐处对得上, 且四个硬编码前缀确无第五处; R2 的三条 critical 与十条 major 全部落进正文, 没有一条被本轮重开; 本轮据以改判 Rule #6 的两条载重事实 (ab-suite 命中数、`collision.kind` 由 `none` 翻 `cross_owner`) 本席独立复跑**全部复现**。四条 major 全部落在**同一族**: 契约改了, 但「谁在消费这个契约、消费方的测试在不在回归面里、文档里那句旧格式谁去改」这三问没走完 —— 两条是回归面盲区 (`test_max_branches_resolver` 39 tests 会被返回契约改动确定性打红; `test_scan_integration` 的 AC-5 夹具既可能翻红又对路径无鉴别力), 两条是文档面 (`rel_path` 被指派到错误的 docstring 块并被 SC 固化; `track_id` 的四处格式声明零同步项)。四条都可在正文与 SC 层一次性修完, 不触碰设计骨架, 也不需要 owner 裁决; 无一条构成 critical (无消费方在生产上被打断, 无 SC 因此恒绿假绿)。post_spec 为 `blocking: false`, 本 verdict 不硬阻断, 但按 audit-points 横切「数据可用性」条款, 上述 major 均为机械核实所得的载重项, 不得只记一笔。

- Critical: 0
- Major: 4 (2 testing/implementation 回归面 · 2 documentation 契约同步)
- Minor: 2 (均为 risk)
- Decisions: 4 (不计入)

## 轮次记录

### Round 1 (承前)

- Agents: 5/5 — Conclusions 33 (Critical 2 / Major 15 / Minor 10 / Decisions 6), Vote REVISE 5 / PASS 0, verdict FAIL
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品

### Round 2 (承前)

- Agents: 5/5 — Conclusions 31 (去重前 55; Critical 3 / Major 10 / Minor 9 / Decisions 9), Vote REVISE 5 / PASS 0, verdict FAIL; 与 R1 交集 0
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品

### Round 3

- Agents: [backend-architect] (本报告为五席之一, 未聚合)
- Sibling probe 行: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions 数: 10 (Issues 4 / Risks 2 / Decisions 4); 缺陷类计数 Critical 0 / Major 4 / Minor 2
- Delta vs 上轮: R2 的 22 条缺陷类本席**无一重开** (13 条 critical/major 逐条复核已落地); 4 条 major 全为新增, 其中 2 条 (`test_max_branches_resolver` / `test_scan_integration`) 是 R2 已定型缺陷族 (SC-10 点名集不含被改文件的测试) 在另外两条契约上的复发, 2 条 (docstring 块归属 / `track_id` 格式) 是 R2 未测到的机械事实
- 机械核验清单 (本轮实跑, 非引用): `python3 -m unittest` 四次 (五模块 102 OK · `test_max_branches_resolver` 39 OK · `TestSnapshotSelfConsistencyAC5` 11 OK) · dedupe/classify/`filter_layer_h_fresh` in-memory 探针五组 · hermetic 临时仓 `git ls-tree` 默认与 `-z` 对照 + pathspec 外泄检查 · `git show 5697477^:` 与 `813e82c:` 两版 ab-suite 字节数与命中数 · 全插件树 `tracks_multibranch` / `filename` / `legacy_count` / `identity_advisories` / `_list_handoff_files` 消费方 grep · 主仓 (排除 aria 子模块) `tracks_multibranch` 消费方 grep
- Vote: **REVISE** (Major 4 > 0)
