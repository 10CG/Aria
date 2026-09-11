---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T17:44:32.904Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [code-reviewer]
---

# post_spec R5 — code-reviewer 席位报告

被审对象: `/home/dev/Aria/openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` (Level 2, `10CG/Aria#195`)
席位透镜: 逐条打开 proposal 引用的 文件:行号 验证真伪 / 改动是否破坏同文件其它调用路径 / 文档同步面是否列全。
核验基准: 插件缓存 `aria/1.71.1` (= `301641b`) 逐文件实读, 并对**当前** aria checkout (`f314785`) 与主仓实况做交叉核对; 涉及测试的结论一律实跑。

## 审计结论

### Decisions

- [minor] documentation/R4 处置落地核验: R4 的 1 critical + 10 major 逐条核到正文落点 (§3 :129-135 · §2.5 :147/:156 · §5 :196/:207 · SC-13 :336 · SC-16 :339 · Task 2.0a-b :282-283 · rule6_note :362), 全部是正文改写而非批注 (证据: proposal.md 上述各行 + scratchpad rework-R4.md:15-25)
- [minor] testing/R4 critical `5c28d58f` 独立复现: 本席在当前 checkout 副本上三步复跑 —— 基线 `Ran 19 tests … OK`; 仅打「`rel_path` 无兜底早退」补丁即 `FAILED (failures=3)` 且 `:270` 报 `0 != 1`; 给 `HEALTHY_TRACKS` 补 `"rel_path"` 后复绿 `Ran 19 tests … OK` (证据: tests/test_scan_integration.py:164-166,270,272,317; scan.py:180-186)
- [minor] architecture/§5 消费方枚举完备性: 全树 grep 复核 `tracks[].filename` 消费点恰 4 处 (scan.py:180 · handoff_multibranch.py:455 · latest_md_writer.py:116 · :213), `tracks_multibranch` 跨 skill 仅 phase-d-closer 三文件 (SKILL.md:218 · handoff-mechanics.md:116,120,121 · fetch_gate.py:187), `_list_handoff_files` 仓内外部消费仅 test_max_branches_resolver.py:286,300,316,332 四处 mock —— §5 表无遗漏 (证据: 上述文件行)
- [minor] testing/SC-11 grep 锚点可证伪性: 基线逐条实测 `'Returns only the basename'`=1 · `'path relative to'`=0 · `'when the filename cannot be'`=1 · `'legacy track missing filename'`=1 · `'Fallback when single active track has no filename'`=1 · `degraded_reason`=0, 无一恒绿 (证据: handoff_multibranch.py:246, latest_md_writer.py:113,114,152)

### Issues

- [major] documentation/头部 2026-09-10 基线复核: 该行称「触点文件 diff 输出为空 ⇒ 全部行号在 `f314785` 上继续有效」, 实测为假 —— `skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py` 在 `301641b→f314785` 变更 (+82/-17), 而它正是 SC-3 / SC-4 / SC-13 的 `_GIT_ENV` 夹具模板与 SC-10 点名集成员: `_GIT_ENV` 由 `:174-183` 移到 `:176-185`, 名/邮箱由 `:176-179` 移到 `:179-182`, `GIT_CONFIG_*` 由 `:181-182` 移到 `:183-184`, 夹具 `:380-382`→`:382-384`, 调用点 `:386`→`:388`; 另 `aria/CHANGELOG.md` 的 v1.70.0 先例整体 +25 (`:84`→`:109`, `:93-97`→`:118-122`, `:99-100`→`:124-125`) (证据: proposal.md:16 vs `git diff --name-status 301641b f314785`)
- [major] testing/SC-10 第三类归因路径 + 待复议 8: 二者建立的「2026-09-09 起自动转红 2 条」已被上游修掉 —— `f314785` 的提交自述「collision_dedupe 16 个 collector 调用点钉 now= (aria-plugin#194)」, 现全部调用点为 `now=_FIXED_NOW` (`:173` 定义), 本席今日 (2026-09-10, 已过 09-09) 实跑该模块得 `Ran 23 tests … OK`。⇒ (a) 一个被列为 Phase B 硬前置的 owner 门失去对象; (b) SC-10 的「基线须在 2026-09-09 之前取, 已过该日先按 §待复议 8 裁定处置」在今天结构上不可满足, 且 fallback 指向已失效的门 (证据: proposal.md:332,388; 当前 checkout test_handoff_multibranch_collision_dedupe.py:173,388)
- [major] documentation/§6.5 CHANGELOG 计划 + F1: §6.5 把 `### Fixed` 钉死为三条 (子目录 / 非 ASCII / 假 legacy) 且 SC-11(e) 按三条机检, `### Changed` 四条也不含 AC-5 面; 但 §Impact 自称「修掉一个跨文件静默失效点 (F1): AC-5 ancestry 检查……变成真检查」。修好路径后子目录 track 会**首次**走到 `git merge-base --is-ancestor` 并可产生顶层 `errors[]` 的 `snapshot_self_contradiction` / `snapshot_consistency_inconclusive` —— 这是第六个被本 spec 改动的量 (spec 自己登记了 `exists` / `len(tracks)` / `legacy_count` / `collision.kind` / `n_active` 五个), 版本 SOT 与 Risk 表零登记 (证据: proposal.md:238,240,264; scan.py:186-213,260-284)
- [major] architecture/§2.5 `degraded_reason` 返回契约: 该键的存在性只在 `n_active == 1` 支被断言 (SC-15 布局 1 (i) / 布局 2 (h) / 布局 3 (j) 全落在 pointer 支), `banner` 与 `skipped` 两支未定义; 措辞也不自洽 —— `:154` 写「optional 返回键 (缺省 None)」, `:239` 却给另两个新字段写「恒存在」。⇒ 只在 pointer 支加键的实现能通过全部 SC, 而 Task 2.5(e) 要改的公开契约 `references/phase-1-collectors.md:102` 将声明一个在 2/3 分支不存在的键 = 本 spec 立意要修的「契约陈述 ≠ 实现」。对照: `unreadable_count` 就配了 SC-14 (错误路径) + SC-16 (成功路径) 两面 (证据: proposal.md:147,154,239,288,344,346,350; latest_md_writer.py:298-320)
- [major] implementation/Phase B/C 起点与版本号段: 实测主仓 `git ls-tree HEAD aria` = `f314785`, 最高 tag = `v1.73.0` (ls-remote 复核), `plugin.json` = 1.73.0; 但 (a) `:9`「Phase B 在 `301641b` 起分支」、`:10`「gitlink bump 起点是 `301641b`」、Task 5.2 `:313`「gitlink bump **从 `301641b` 前进**」三处未 neutralize, 照字面执行即把主仓 gitlink 从 `f314785` 回退 (与头部自己警告的 `0545f86` 回退同型); (b) 待复议 6 仍写「`tag --list 'v1.7*'` 最高为 `v1.71.1`, 两个候选号 `v1.71.2` / `v1.72.0` 当前均未被占用」且推荐默认 = MINOR/`v1.72.0` —— 该号已低于已发布的 v1.73.0, 09-10 复核只顺延了 PATCH 候选 (v1.73.1) 一半 (证据: proposal.md:9,10,16,313,386)
- [minor] implementation/§2.5 与 Task 2.5(e2) 调用点行号: 称 `_render_pointer`「其唯一调用点是 `:302`」; 实读 `latest_md_writer.py:302` 是 `elif n_active == 1:`, 调用在 `:303`; 另 `_render_pointer_unavailable` 有内部调用点 `:124`, 改返回形状时须同批处理 (证据: proposal.md:147,288; latest_md_writer.py:124,302-304)
- [minor] documentation/References 闸门行号: `:396` 与 Task 5.1 表引 `.aria/state-checks.yaml:88 / :141 / :372`; 实测三条 check 的 `name:` 行现在 `:124 / :177 / :408`, 而 `:88` 现属 `silknode-contract-deferral-expiry`、`:141` 属 `m6-claude-md-version`、`:372` 属 `forgejo-app-token-liveness` (漂移自 d2d93da 2026-09-07 与 ed5357f 2026-09-08; 起草时的 fdfb183 上确为 88/141/372) (证据: proposal.md:311,396; .aria/state-checks.yaml:124,177,408)
- [minor] testing/§2.5 R4 `5105b00e` 反证依据: 「全模块 …… 全文件 `rel_path` 零命中 (grep 实证)」为假 —— `tests/test_p1_layer_h.py:115-116` 有两处同名循环变量。结论 (八字段 `_active_track` 夹具无该键) 仍成立, 但机械依据写错, 与本 spec 自身「依据换成实跑取到的真依据」的口径冲突 (证据: proposal.md:156; test_p1_layer_h.py:115-116,230-240)
- [minor] implementation/scan.py 上报面语义: §3 / §5 把 `:193` / `:209` 上报的 `filename` 钉成 basename 且「不需登记」, 但命令行改用 `rel_path` 后, 子目录 track 的 `offenders` / `inconclusive` 报告不再唯一标识**实际被检查的文件** —— 正是 §Why 后果 3「同名不同目录不可区分」被搬到错误报告面。建议至少与 Task 5.3(e) 的 `errors[].tracks[]` schema 缺口一并登记 (证据: proposal.md:133,196,314; scan.py:192-196,207-212)

### Risks

- [minor] documentation/裸 issue 引用纪律: `f314785` 新落 `skills/state-scanner/scripts/check_bare_issue_refs.py` (fail-CLOSED, 封闭豁免集), 主仓 `.aria/bare-issue-ref-allowlist.txt` 今日新建但该 check **尚未**注册进 `.aria/state-checks.yaml`。对本 proposal 实跑报 **18 处**裸 `#<n>` (`:1,:7,:10,:207,:223,:311,:315,:381,:396,:399`)。若本 cycle 内该闸门注册, proposal 与其 handoff 会在 Phase C/D 转红; 预防成本 = 把裸引用写成 `10CG/Aria#195` 形态 (证据: 上述脚本 + 实跑输出)

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 5 / Minor 5 (含 1 条 risk) + 4 条 decision。

理由: 代码级核对面本轮质量很高 —— 我逐条打开了 proposal 引用的全部 SOT 行 (`handoff_multibranch.py` 的 `:16-31`/`:35-44`/`:177-178`/`:240-288`/`:301`/`:321`/`:329-336`/`:428-455`/`:494`/`:521-524`/`:586-596`/`:619-626`/`:645`/`:665-676`/`:687-698`/`:748` · `handoff.py` 的 `:263-266`/`:288`/`:300-327`/`:389`/`:397-404`/`:438-451` · `latest_md_writer.py` 全部被引行 · `scan.py:119-213,255,269,283,388` · `state-snapshot-schema.md` 全部被引行 · `lib/collision.py`/`lib/constants.py`/`_common.py`/`track_board.py`/`handoff_worktrees.py`/四份 references/两份 standards/LEVEL_GUIDE/AB 套件/决策单), **在 `301641b` 基线上无一处符号错、无一处行号错**, SC-11 的每个 grep 锚点都实测过基线可证伪, §5 消费方枚举经全树 grep 证明完备, R4 的 critical 修法本席独立复跑一致。无 critical: 未发现方案性错误、未发现会破坏消费方的设计、未发现恒绿假绿的 SC。

但 5 条 major 都指向同一类问题: **spec 冻结在 `301641b`, 而世界已走到 `f314785`, 09-10 的复核只补了一半**。其中两条 (日历门失效、Phase C 起点/版本号) 会直接影响 Phase B/C 的动作正确性, 一条 (F1 未进 CHANGELOG) 是 Rule #3 的文档同步缺口, 一条 (`degraded_reason` 分支覆盖) 是新公开契约的定义缺口。故投 REVISE: 这些都是低风险、可机械闭合的订正, 不需要重做设计。

## 轮次记录

### Round 5

- Agents: code-reviewer (本报告为五席之一)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions 数: 14 (issue 9 / risk 1 / decision 4; Critical 0 / Major 5 / Minor 9)
- Vote: REVISE
