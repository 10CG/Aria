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
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-07T01:15:23.099Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [code-reviewer]
---

# post_spec R2 单席报告 — code-reviewer (handoff-multibranch-subdir-path-fidelity)

审查方式: 不采信 proposal 自述, 逐条打开被引用的 文件:行号 实读; 另做三组独立 hermetic 复跑与两次真仓实跑测试。基线副本 = 插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/skills/state-scanner/` (= aria `origin/master` 301641b)。本轮**只审不改**, 未编辑任何仓库文件。

## 审计结论

### Decisions

- [minor] testing/R1 critical·major 正文落地核验: R1 的 2 critical + 15 major 全部在正文落地而非批注。逐条抽验: SC-10 两条「已知失败」豁免已删且我在真仓 `/home/dev/Aria/aria/skills/state-scanner/tests` 实跑得 `Ran 78 tests ... OK` (与 proposal.md:232 一致); `_check_handoff_ancestry` 已全文改为 `_same_branch_head_unreachable_tracks` 且该符号在 scan.py:126 定义、:186 拼串、:255 被调用; SC-13 / SC-14 / SC-15 与 Task 2.4 / 4.2 / 5.1 均已补入。头部机械事实亦复核: `git ls-tree HEAD aria` = `301641b`、`git -C aria diff --name-status 0545f86 301641b | wc -l` = 29、5 个触点文件 `diff --stat` 输出为空、`.aria/state-checks.yaml:88/:141/:372` 三条 check 名称对得上、决策单 `.aria/decisions/2026-09-07-...md` 实际存在 (证据: proposal.md:9-15,232; scan.py:126,186,255)
- [minor] implementation/行号与 hermetic 事实复核: 我打开的全部引用点属实 —— `handoff_multibranch.py:177-178` (注释说 trailing slash 而值无斜杠)、`:246-247` docstring 原句、`:277` `Path(path).name`、`:278` `.endswith(".md")`、`:280` pointer 比对、`:301`/`:321` 拼串、`:329-336`、`:455` 四级键第三级、`:586-596` 六键早退 dict、`:637-658` 假 legacy 分支; `handoff.py:288/300/318/389/399/438-451`; `latest_md_writer.py:89-95/143/151-169`; `track_board.py:183,188` import dedupe、`:254,559` 只吃 updated_at。独立 hermetic 复跑三条: 非 ASCII 路径经 `ls-tree -r --name-only` 得 `"docs/handoff/2026-\346...md"`、basename 带尾引号并在 `.md` 过滤处丢弃 (`DROPPED(.md filter)`); `git mv` 后旧 basename 路径 / 新相对路径 / `--follow` 三者 `git log -1 --format=%aI` 均返回 mv 日 `2026-08-15T12:00:00+00:00`, 而「从未在顶层存在」的文件错误路径返回空串、正确路径返回 `2026-06-01T09:00:00+00:00`; 顶层与 `archive/` 两个 `latest.md` 在基线循环上均被排除 (证据: 复跑脚本落 scratchpad/h195, h195b)

### Issues

- [major] implementation/§2.5 · Task 2.5 pointer 写侧守卫判据: 守卫判据被规定为 `relpath != filename` 且严禁字符串嗅探, 但**没有定义 `relpath` 缺失时的取值**。缺键取 `None` ⇒ 判据恒真 ⇒ 任何不带该字段的 track (老 `.aria/state-snapshot.json`、其它版本产出的快照、既有手搓夹具) 的 pointer 全部退化成「(pointer 不可用)」。实证: `tests/test_p1_layer_h.py:230-240` 的 `_active_track()` 构造八字段 dict 无 `relpath`, `:271` `assertIn("2026-05-20-my-spec.md", content)` 在该实现下必红 —— `_render_pointer_unavailable` 只印 track_id, 不印文件名 (`latest_md_writer.py:154-169`)。附带: 该函数签名是 `_render_pointer_unavailable(track_id, now)` (`:151`), 要带「目标在子目录」的新原因文案必须改签名或新增函数, Task 2.5 未点名此契约变更。修法: spec 里写死「缺 `relpath` ⇒ 视同顶层, 照写真指针」, 并把该缺省补进 SC-15 的第三条反事实 (证据: latest_md_writer.py:116-124,151-169; tests/test_p1_layer_h.py:230-240,261-271; proposal.md:128,201)
- [major] testing/SC-2 · SC-12 零差异断言与 A′ 新键: A′ 给**每一行** track 追加 `relpath`, 而 SC-12 只豁免 `unreadable_count`「除该新键外零差异」⇒ 实现正确时 `tracks_multibranch` 的逐字段 diff 依然满屏 `relpath`, SC-12 必假红; SC-2 的测试名更强 (`test_flat_repo_byte_identical_to_frozen_baseline`) 且正文写「`tracks[]` / `legacy_count` 逐字段相等」, 同样不成立 —— 除非 baseline 与改后输出都经 `tests/fixtures/freeze_corpus.py:29` 的八字段投影 (`FIELDS` 硬编码, 不含 relpath), 而 SC-2 只说「用它的形态」没说走投影。这类假红最危险的下场是实施者顺手削断言 (memory `feedback_ab_baseline_contaminated_by_auto_loaded_context` 同族)。另: 决策单 §落地约束第 1 条要求「平铺仓 `relpath == filename` 要有一条 SC 钉住」, 现 SC 集无任何一条承接 (证据: proposal.md:224,234; freeze_corpus.py:8-12,29,35; .aria/decisions/2026-09-07-...md:58)
- [major] testing/SC-15 子目录布局夹具与反事实: SC-15 子目录布局只规定「唯一 active track 的文件在 `archive/`」, 未规定顶层是否另有交接。取最自然的最小夹具 (顶层只剩 writer 写的 latest.md), 则 `collect_handoff` 的 `_scan_md_files` 非递归且排除 latest.md ⇒ `canonical_files` 为空 ⇒ `handoff.py:438-451` 直接返回 `exists: False` 并**根本不进入 pointer 解析**, 于是: (a) 「去掉守卫 ⇒ (e) 因 `handoff_pointer_target_missing` 出现而红」这条反事实为假, (e) 在有无守卫下都绿 = 恒绿断言; (b) (f)「`handoff.exists` 与 `tracks_multibranch.exists` 不互相矛盾」即使守卫落地也是 False vs True, 结构上不可满足。proposal 自己在 §5 case (b) 已写清这个机制, 只是没回灌到 SC-15。修法: 夹具显式要求另有一份**顶层非-active** 交接 (让候选集非空), 或把 (f) 改写成「矛盾时必须有信号」这类可满足谓词 (证据: proposal.md:151,237; handoff.py:300,318,323,438-451)
- [major] documentation/rule6_note 套件覆盖实测: 「`ab-suite/state-scanner.json` 对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` 四词零命中」不成立。我实跑 `grep -c`: 前者 0、后者 **1**、`legacy` 0、`basename` 0; 命中处是 eval 12 的 prompt, 恰好在问「`tracks_multibranch.collision.kind` 为空是否改变 coordination 闸门答案」。该断言是 Rule #6 substitute 的载重证据 (CLAUDE.md 规则 6 判据表第一行), 同一句在头部 :12 与 rule6_note :244 重复两次。结论未必倒 (本变更不动 `collision.kind`, 我复核 `lib/collision.py:483-486` 的 `collidable` 过滤确排除 `owner_container == "unknown"`), 但必须按实测改写, 否则复议方拿到的是一条经不起 grep 的事实 (证据: aria-plugin-benchmarks/ab-suite/state-scanner.json:214; proposal.md:12,244; lib/collision.py:480-486)
- [major] architecture/§5 · Impact · 待复议 2 的 pointer 失败面可达性: proposal 通篇把「D.3 的 `latest_md_writer` 写出 pointer」当既成事实, 并据此把 pointer 往返定为「本 spec 引入的新失败面」、据此裁 A′、据此向 owner 要「子目录采用方只拿降级 pointer」的代价确认。实况: 该 writer **全仓零生产调用点** —— `references/phase-1-collectors.md:95` 明写「deliberately D.3-scoped, 不在 scan.py 内自动触发, 不在 P1 内引入 production call-site」; 全仓 grep `write_latest_md|latest_md_writer` 的 `.py` 命中只有它自己、`writers/__init__.py` 的再导出与 `tests/test_p1_layer_h.py`; phase-d-closer 的 D.3 pointer 更新是 AI 按 3 行决策表**手改** latest.md (`references/handoff-mechanics.md:114-124`); 本仓 `docs/handoff/latest.md:103-107` 甚至明记「机械 `latest_md_writer` 当前不可用」并声明这是一处对约定的有意偏离。守卫本身依然值得做 (writer 是已发布的公开 API), 但可达性必须写明, 否则 owner 是在一个被高估的影响面上做取舍 (memory `feedback_adversarial_finding_severity_by_deployment_reachability`) (证据: references/phase-1-collectors.md:95,102; phase-d-closer/references/handoff-mechanics.md:114-124; docs/handoff/latest.md:103-107; proposal.md:151,189,255)
- [major] documentation/Task 4.1 · SC-7 · Task 3.2 的 A 案遗留: A′ 裁定后 `filename` 仍是 `YYYY-MM-DD-` 前缀的 basename, 因此 `state-snapshot-schema.md:1125` 那句「lexicographically greater name is also the later-authored one」**并未变假**; 但 Task 4.1 仍把「`:1125` tie-break 论据订正」写成无条件必做项, 照做就是往 schema 里写一条错误勘正。§6 第 1 条与 Impact.Risk 第 1 条已经条件化成「A 案下」, 任务面没跟上 —— 这是 memory `feedback_rework_leaves_downstream_ac_drift` 的典型形态。同族: SC-7 的用例要求构造 `filename = "archive/2026-07-19-x.md"` 的 track 行, 在 A′ 下 collector 结构上不可能产出该形状, 该 SC 与 Task 3.2 应改成显式标注「假想输入的特性化测试」或随 A 案一并删除 (证据: proposal.md:165,188,207,209,229; state-snapshot-schema.md:1125)
- [minor] testing/SC-10 回归模块清单: SC-10 点名的 4 个模块我实跑复核为 `Ran 78 tests ... OK` (与 proposal 一致, 该条 R1 修复有效), 但 v3 新增的 Task 2.5 改的是 `latest_md_writer.py`, 而全树唯一 import `write_latest_md` 的测试是 `tests/test_p1_layer_h.py` (24 tests, 我实跑 OK), 不在这 4 个模块里。现只靠 SC-10 尾句「全量 discover 另跑并与改前基线逐条对比」兜底; 建议把该模块并入点名集, 因为它正是上面第一条 major 会翻红的地方 (证据: proposal.md:232; tests/test_p1_layer_h.py:51,244-271)
- [minor] documentation/Task 4.2 docstring 勘正清单: `_get_file_commit_date` 的 docstring `:313` 写 "ISO 8601 UTC **committer** date", 而实现用 `%aI` = author date (`:316` 自己就写了 author date, `:322` 是命令行), 模块 docstring `:40` 与 `state-snapshot-schema.md:1108` 也都写 committer。这与 Task 4.2 已收入的 `:20` legacy_count 注释、`:177` trailing slash 属同一族「既有 code/doc 不一致, 顺手勘正」, 且 §Why 与 SC-4 的全部日期结论都建立在 author date 语义上, 建议一并纳入 (证据: handoff_multibranch.py:40,313,316,322; state-snapshot-schema.md:1108; proposal.md:210)

### Risks

- [minor] architecture/§5 dedupe 行「A′ 案下无此面」: A′ 保留 basename 后, 同 `(track_id, identity_key)`、同 `updated_at`、同 `branch`、同 basename 而目录不同的两行, 四级键 `(parse_ok, updated_at, filename, branch)` **全并列**, `max()` 回退到迭代顺序 —— 与 `_dedupe_sort_key` docstring `:438-452` 与 schema `:1126` 宣称的「a pure function of the row's own fields / invariant to build order」直接相悖 (那正是 round 3 finding [M1] 建立的不变量)。改前这两行因 §Why 后果 3 的串读而逐字段相同, 选谁都一样; 改后 `relpath` 与真实 frontmatter 不同 ⇒ 代表行的 `status` / `phase` 可能不同 ⇒ 经共享 dedupe 传导到 collision 与看板。触发需要「同名不同目录 + 同日期粒度 updated_at」, 窄但不是不可达 (schema `:1125` 自述本仓真出现过同日 date-only 并列)。建议把 §5 该行由「A′ 案下无此面」改成「A′ 消除字典序翻转风险, 但把 tie 的可观测性打开了」, 并在待复议 4 里附带问一句是否把 `relpath` 加进排序键 (证据: handoff_multibranch.py:428-455,438-452; state-snapshot-schema.md:1125-1126; proposal.md:153)

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 6 / Minor 3 (另 2 条 decision 不计入缺陷计数)。

rationale: 这一版的事实底座与 R1 修复质量确实上来了 —— 我逐条打开的 30 余个 文件:行号 引用**无一处错误**, 三组 hermetic 结论我独立复跑全部一致, SC-10 的 78 与主仓 gitlink `301641b` 机械复核吻合, R1 的两条 critical 与 15 条 major 都是正文改写而非批注。没有 critical 的理由是: 方案骨架 (A′ + relpath + 守卫 + 不再伪造 legacy) 与真代码自洽, 也没有一条 SC 因恒绿而把整块修复放行。

6 条 major 集中在**同一处 rework 的下游**: 2026-09-07 的 A′ 裁定与 §2.5 守卫是本版新增物, 而它带来的三处连带面没有回灌 —— 守卫判据缺省未定义 (会翻红既有 writer 测试)、新增 `relpath` 键与两条「零差异」SC 冲突、SC-15 子目录夹具下 (e) 恒绿且 (f) 不可满足; 另有两条是 A 案遗留没随裁定收敛 (Task 4.1 的 `:1125` 订正、SC-7 的不可达输入形状)。这正是 memory `feedback_multiround_audit_catches_fix_introduced_regression` 说的形态: 加固动作自身重开同类缺口。剩下两条是可机械证伪的事实面: rule6_note 的「四词零命中」被一次 grep 推翻 (`ab-suite/state-scanner.json:214`), 以及 `latest_md_writer` 零生产调用点使 pointer 失败面的可达性被系统性高估 —— 后者直接影响 owner 对待复议 2 第 (1) 点的裁决口径。按 audit-points 横切「数据可用性」条款, 事实性断言核实不通过即载重投 REVISE, 即使 post_spec 非阻塞。

全部 6 条都能在 Phase A 内改 spec 消解, 不需要推翻 A′ 裁定本身。

## 轮次记录

### Round 2

- Agents: code-reviewer (本报告为五席之一的单席产出)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品 (扫描面: `openspec/changes/` 8 个在制 spec 中只有本 spec 引用 Aria#195; 全仓 grep `10CG/Aria#195` 无第二份 proposal)
- Conclusions: 11 (Major 6 / Minor 3 / Decisions 2)
- Delta vs 上轮: R1 的 2 critical + 15 major 经逐条核验均已在正文落地, 我未重开其中任何一条; 本轮 6 条 major 中 4 条 (守卫缺省 / 零差异 SC / SC-15 夹具 / Task 4.1 遗留) 是 R1 修复动作自身引入的新面, 2 条 (rule6_note 零命中 / writer 可达性) 是 R1 五席未测到的机械事实
- Vote: REVISE
