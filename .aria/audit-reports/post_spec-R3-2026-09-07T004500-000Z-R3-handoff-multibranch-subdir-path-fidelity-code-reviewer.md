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
timestamp: 2026-09-07T03:46:56.220Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [code-reviewer]
---

# post_spec R3 单席报告 — code-reviewer (handoff-multibranch-subdir-path-fidelity)

席位透镜: 代码级核对。本轮对 proposal 引用的每一处 `文件:行号` 逐条打开验证, 对方案改动做了「同文件其它调用路径会不会坏」与「文档同步面是否列全」的穷举, 并对每条 SC 反问「基线上会红吗」。基线 = 插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= aria 子模块 `origin/master` `301641b`, 已用 `git -C /home/dev/Aria/aria rev-parse HEAD` 实测同值)。

## 审计结论

### Decisions

- [minor] implementation/行号与符号引用复核: 逐条实读 30 余处引用**全部命中且行号准确** —— `handoff_multibranch.py:36,40,42,177-178,246-247,277-280,301,313-322,329-336,428-455,493-499,521-524,586-596,619-626,637-658,683-700,748,753` · `handoff.py:288,300,318-323,389,397-404,438-451,455` · `latest_md_writer.py:72-95,143,151,164,208-217,259` · `scan.py:119-120,126,166-213,255,382-383` · `_common.py:312-313,411-412` · `track_board.py:183,188,254,559,753` · `state-snapshot-schema.md:46-48,1070,1104,1108,1110,1125-1136,1156-1168`。`_check_handoff_ancestry` 全树零命中 (R1 订正属实), `_same_branch_head_unreachable_tracks` 三处 (定义 `:126` / 拼串 `:186` / 调用 `:255`) 逐字对上。
- [minor] testing/R2 缺陷落地与机械底座复核: R2 的 3 critical + 10 major + 9 minor **全部落进正文而非批注**, 逐条比对未见「改一处引入另一处矛盾」; 头部保留的 `relpath` 字面只剩两处必要的证据句 (`:16`, `:316`), 判据代码 7 处均已是 `rel_path`。独立实跑复核: SC-10 五模块在真 checkout 得 `Ran 102 tests … OK`; 主仓 `docs/handoff/` = 190 份顶层 `.md` / 0 子目录 / 0 非 ASCII; Task 5.1 的 16 个版本点逐处 `grep -n` 命中且值均 `1.71.1`; `ab-suite/state-scanner.json` = 17551 B, `tracks_multibranch` 命中 1 (`:214` 且值写死在题面), 另三词 0; `git diff --name-status 0545f86 301641b` = 5 added + 24 modified, 5 个触点文件 `--stat` 空输出; `\brelpath\b` 全树零命中; `validate_schema_doc.py:18-22` 自述不检查嵌套键 ⇒ 新增 `rel_path` / `unreadable_count` 的文档同步确实只能靠 SC-11 的 grep 兜。
- [minor] architecture/A′ 骨架代码级成立: `filename` 保持 basename + additive `rel_path` + 四个消费方改读 —— 与 `handoff.py:389` 按 `p.name` 建索引、`_dedupe_sort_key:455` 第 3 级吃 `filename`、`schema:1125` 的日期前缀论据三处既有不变量相容; 守卫判据 `rel = track.get("rel_path") or track.get("filename")` 后比 `rel == filename` 对缺键、平铺、子目录三态均给出正确分支。本席不主张推翻骨架。

### Issues

- [major] testing/SC-11 (c) 文档同步机检: SC-11(c) 用 `grep -q 'callers compose the full git-object path' collectors/handoff_multibranch.py` **无命中**来验证旧契约句已删, 但该句在基线上就是跨行的 —— `:246` 结尾是 "so callers", `:247` 才是 "compose the full git-object path as needed."。实测基线 `grep -c` = **0** (python 侧确认单行子串不存在、`callers\n    compose…` 存在) ⇒ 该判据**恒绿**, 实现即使原样保留旧句也照过。它正是 v1「`grep -c basename` 计数」那条被判「不定位」的代理判据的替代品, 替代后反而更弱。修法: 改 grep 单行子串 (例 `'Returns only the basename'`) 或多行匹配, 并加一条「新契约句存在」的正向断言 (证据: proposal.md:274; handoff_multibranch.py:246-247)。
- [major] testing/Task 2.1 枚举层返回契约 / SC-10 点名集: §What.1 与 Task 2.1 要求 `_list_handoff_files` 从分支级错误通道改成能携带 per-item 错误, 示例是「第三个返回位」。但 `tests/test_max_branches_resolver.py::TestCapApplicationPath` 在 `:286,:300,:316,:332` 四处 `mock.patch.object(hmb, "_list_handoff_files", return_value=([], None))` 后真调 `collect_handoff_multibranch` —— 主循环 `:619` 是二元解包, 改三元组即 4 条现绿用例 `ValueError`。本席实跑该模块基线 `Ran 39 tests … OK`。该模块**不在 SC-10 的五模块点名集**, 只剩「全量 discover」兜底 —— 与 R2 `7cba5aa4` 同型 (点名集漏掉唯一会被打红的模块)。注: 若 Phase B 取「注入 reporter (带默认值)」那条路径则不破坏; 但 spec 未点名该触点, 选型后果不可见 (证据: proposal.md:227,273; test_max_branches_resolver.py:286)。
- [major] documentation/§6 与 Task 4.1/4.2 漏 legacy track_id 公式: §What.2 与 SC-13 要求 `_make_legacy_track_id` 改吃 rel_path (`legacy:<branch>:archive/x.md`), 但三处机读契约仍写 `legacy:<branch>:<filename>` —— `state-snapshot-schema.md:1104` (TrackEntry 表) · `handoff_multibranch.py:36` (模块 docstring) · dedupe docstring `:493-496` 的论据句。§6 的六条同步清单、Task 4.1/4.2 的逐项、SC-11 的八条 grep **无一条覆盖**。落地后 schema SOT 会对子目录采用方陈述一条假公式, 与本 spec「契约与实现对齐」的立意相左, 也踩 Rule #3 (证据: proposal.md:114,176-187,234-235,277)。
- [major] architecture/§2.5 与 Task 2.5 未定义守卫后的返回值语义: 守卫落在 `_render_pointer`, 而 `write_latest_md` 的 `action` 仍由 active 计数决定 (`latest_md_writer.py:302-304`), 于是「单 active track + 目标在子目录」会返回 `action="pointer"` 却写出降级横幅 —— 与公开契约 `:277-290`「active count == 1 → "pointer" action, backward-compatible pointer」矛盾。§2.5 反复强调「诚实降级、不得静默退化」, 但只约束正文文案, **机读半边仍在说谎**; 而守卫存在的理由正是「writer 一旦在 D.3 接线就命中」, 接线方最可能消费的就是 `action` (`handoff-mechanics.md:114-124` 的子步骤 2 判的就是「pointer 更新了没有」)。Task 2.5 的 (a)-(d) 与 SC-15 三个布局全部只断内容, 无一条断返回值。请在 spec 内裁: 新增 action 取值 / 加 `degraded_reason` 键 / 或明写「action 保持 pointer 是有意为之」(证据: proposal.md:129,226,279-294; latest_md_writer.py:277-290,302-304)。
- [major] documentation/SC-15 细则布局 2 的机制句是 A 案残留: `proposal.md:288` 写「去掉守卫时 writer 会写出 `[archive/x.md](./archive/x.md)`, `_parse_latest_pointer` (`:288`) **剥成** `x.md` 在候选集里查不到」。A′ 下 `_render_pointer` 读的是 `track.get("filename")` = basename (`latest_md_writer.py:116,143`), 无守卫时写出的是 `[x.md](./x.md)`, **没有目录段可剥**; 该 kind 仍会出现 (候选集只有 `2026-05-01-old.md`), 故结论不变, 但机制与字面双错。危害: 该段被本文自己声明为「夹具组成是判据的一部分」, 实施者照字面写反事实断言会断言一个永不出现的字符串, 或反向「修」成让 writer 输出 rel_path —— 那等于把 A′ 在 pointer 面上悄悄改回 A (证据: proposal.md:286-294)。
- [minor] documentation/Task 4.2 与 SC-11(c) 把 `rel_path` 归错 docstring 块: 两处均写「模块 docstring `:14-31` 键表补 `unreadable_count` + `rel_path`」。`:14-31` 是 `tracks_multibranch` 顶层键表 (`unreadable_count` 归它没错), 而 TrackEntry 字段表在 `:33-44` (`:42` 的 filename 契约就在那里)。照字面实现会把 per-track 字段登记成顶层键 (证据: proposal.md:235,274; handoff_multibranch.py:14-31,33-44)。
- [minor] testing/SC-2 用例名与判据口径不一致: 判据已按 R2 `d02ec3f0` 改成走 `freeze_corpus.py:29` 的八字段投影 (不含 `rel_path`), 核验列的用例名却仍是 `test_flat_repo_byte_identical_to_frozen_baseline`。名字里的「byte identical」正是那条在 A′ 下恒红的旧口径, 留着会诱导后来者改回整字典比对 (证据: proposal.md:265)。
- [minor] documentation/rule6_note 对 SC-15 的 baseline-failing 归因不准: 该行写「SC-15 的资格改由布局 2 的 (d)(e) + 布局 3 的 (g) 撑住」。按代码推演: 基线上布局 2 的归档件读不出 ⇒ 无 active track ⇒ `write_latest_md` 走 `_render_zero_tracks` (`:298-300`) ⇒ latest.md 无 `**Latest**` 行 ⇒ `_parse_latest_pointer` 返回 None ⇒ (e) 绿; 布局 3 基线照写真指针 ⇒ (g) 绿。真正在基线转红的只有 (d) 的「文案含目标在子目录」那半。实体资格不受影响 (AB 已改判照跑), 但 substitute 账目应订正 (证据: proposal.md:306,286,290; latest_md_writer.py:298-304)。

### Risks

- [minor] testing/冻结语料重生成: §7 把「两份冻结语料不需重生成」写成省事结论, 实际是**硬约束** —— `tests/test_collision_frozen_corpus.py:51` 断言 `payload["fields"] == [八字段]`, `:112` 断言每行 key 集恰为那八个。若 Phase B 觉得「新增字段就该刷新语料」而用改后代码重生成, 这两条立刻红, 且该模块不在 SC-10 点名集。建议在 §7 或 Task 4.3 明写「不得重生成 (会打红 test_collision_frozen_corpus)」(证据: proposal.md:196,236,273; test_collision_frozen_corpus.py:51,112; freeze_corpus.py:29)。

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 5 / Minor 4 (另 3 条 decision 不计入)。

rationale: A′ 骨架与 §2.5 守卫的代码级前提本轮**全部复核成立**, R2 的 3 critical + 10 major 逐条落进正文且未见回填矛盾, 30 余处行号引用零错误, 三项载重实跑 (102 tests / 190 顶层交接 / 16 版本点) 独立复现一致 —— 无一条本轮发现指向方案错误或消费方破坏, 故不判 FAIL。5 条 Major 分三类: (1) **判据本身失效** —— SC-11(c) 的 grep 在基线上就无命中, 恒绿 (按字面鲁棒性讲这是本轮最实的一条, 因为它是 R1 加固动作的产物, 属「加固自身重开同类洞」形态); (2) **触点/文档面漏列** —— Task 2.1 的签名变更会打红 `test_max_branches_resolver` 的 4 处二元组 mock 而 SC-10 未点名, legacy track_id 公式的三处机读契约无人同步; (3) **A 案残留与机读契约缺口** —— SC-15 细则的 writer 输出字符串仍是 A 案形态, `write_latest_md` 的 `action` 在守卫降级后仍报 "pointer"。五条均可在 Phase A 内改 spec 消解, 无需动骨架。

关于 SC-11(c) 的定级: 按「SC 恒绿 ⇒ critical」的字面口径它够 critical, 本席据爆炸半径下调为 major —— 它守的是 docstring 卫生 (非机制), 且 Task 2.1 独立要求改该 docstring, diff 上肉眼可见。若汇总席按字面口径上调为 critical, 本席不反对。

计算依据: Critical 0 / Major 5 (全 issue) / Minor 4 (3 issue + 1 risk) / Decisions 3 (不计入)。

## 轮次记录

### Round 3

- Agents: code-reviewer (本报告为五席之一)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 12 (Issues 8 / Risks 1 / Decisions 3) — Critical 0 / Major 5 / Minor 4 (+3 decision)
- Vote: REVISE
- Delta vs R2: 未重开 R2 的 31 条中任何一条 (交集 0)。本轮 5 条 Major 中 3 条落在 R2 rework 的**下游** (SC-11(c) 是 R1 加固的产物; SC-15 细则与 Task 4.2 的归位错误是 R2 新写的段落), 另 2 条是前两轮未测到的机械事实 (`test_max_branches_resolver` 的 mock 契约、`write_latest_md` 的返回值语义)。形态与 R2 判词一致: 缺陷集中在同一处 rework 的下游, 不在调研质量。
