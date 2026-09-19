---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-19T11:47:03.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md`(全文, 228 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml`(全文, 1675 行, 分 4 段读)
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md`: `## Why` 全部 (`:23-69`)、`## What` 全部含 §1.0–§1.4 / §2 / §3 / §4 / §5 (`:70-406`)、`## Impact` (`:393-406`)、`## Tasks` 全文 (`:407-451`)、`## Success Criteria` SC-1~SC-22 逐条全文 (`:455-478`)、`## rule6_note` (`:480-486`)、`## 待 owner 复议` 标题与结构 (`:488-557`, 逐条判据以 `.aria/decisions/...` 全文替代复核, 未逐条重读原文正文)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md`(全文, 117 行)
- `.aria/audit-reports/post_planning-R2-2026-09-18T162427-983Z-pre-merge-completeness-gate-change-scope-aggregated.md`(全文)
- `.aria/audit-reports/post_planning-R2-2026-09-18T162427-983Z-pre-merge-completeness-gate-change-scope-qa-engineer.md`(我自己上一轮的报告, 全文, 用于独立重判前的基线对照)
- `aria/skills/audit-engine/tests/test_sibling_spec_probe.py:1-5,290-340`(两条既有守卫 `TestNoPytestImport` / `TestRunAllTestsDiscovery`, 复核未变)
- `aria/skills/run_all_tests.sh:1-60`(`is_pytest_suite()` 判据, 复核未变)
- `aria/skills/state-scanner/scripts/lib/spec_complete.py:705-745`(`_is_hooks_or_config_path` / `_is_aria_check_registry_path`)、`:895-994`(`_classify_file_occurrence`, SC-12 liveness 分类器逐支核对)
- `aria/skills/state-scanner/lib/identity.py:1-80`(`get_container_id` 存在性)
- `aria/skills/state-scanner/lib/claim_lifecycle.py`(grep 全文 + `:475-545` `heartbeat_by_track` 全文, 核验多 claim all-matching 语义)
- `aria/skills/state-scanner/scripts/release_gate.py`(grep `choices=["done","yielded","abandoned"]` @`:253`)
- `standards/conventions/skill-benchmark-exemption.md`(全文, 92 行, 核 §4.1 五字段模板与 rule6_note 合规判据)
- `CLAUDE.md`(经 system prompt 全文, 复核「多远程推送」两条硬约束与规则 #3/#6/#8/#10)
- **git 历史实读 (只读命令)**: `refs/aria/coordination` 上 `claims/023236f2/s-86f7@1836.yaml` 与 `claims/bfe8285d/s-73b9@1606.yaml`、`claims/bfe8285d/s-9762@1447.yaml` 三份 claim 文件全文；`git diff 5d435e9 12c870d -- tasks.md detailed-tasks.yaml` 全文（v2.1→v2.2 逐行 diff）；`git -C standards diff --shortstat 21748d4 940cb5b` 对 6 个被引文件逐一核验
- **实跑核验**（在 `/tmp/claude-1000/.../scratchpad/audit-R3/qa-engineer/verify/` 下，真仓内零写入）：从 yaml 原样抽取 `metadata.commit_attribution.code` 与其变体，对真仓 `338418d..5fd7e08`（300 个提交）实跑，逐提交打印分类并与 yaml `revision_log` 点名的六个提交（`1b9734a`/`5fe15b0`/`c9fe08f`/`9de3074`/`5d435e9`/`1b6f9ad`）逐一核对

## Findings

| id | severity | type | category | scope | 摘要 |
|---|---|---|---|---|---|
| 699adf2f | major | issue | documentation | detailed-tasks.yaml TASK-001 | 基线复核步骤 (verification 第 8 条) 遗漏对 standards 四文件的重新 diff, 与 metadata.baseline_rebase.standards 及 tasks.md 读前必看第 5 条自己写的「1.1 在 B.1 对当时 gitlink 重跑」互相矛盾 |

### M1 · 699adf2f · TASK-001 的基线复核清单遗漏 standards 重测, 与本文件自己的承诺矛盾

- **证据**: `detailed-tasks.yaml` TASK-001 的 `verification` 第 8 条（我用 `python3 -B -c "import yaml; ..."` 精确取出该 bullet 逐字打印核对过）逐字为:

  > 基线复核: 对 metadata.baseline_rebase.aria_zero_diff 的每个文件与 aria_shifted 各条冒号前的文件跑 git -C aria diff --shortstat 301641b <aria 起点> -- <文件>, 对 main_repo 的文件跑 git diff --shortstat a563192 <主仓起点> -- <文件>; 与 A.2 记录比对, 新出现 diff 的文件逐处实读 proposal 所引行号并在台账写偏移表; aria 若有新发布, tasks.md 读前必看第 3 条的取号前提同步更新

  这条只点名了 `metadata.baseline_rebase` 下的两个子键 —— `aria_zero_diff`/`aria_shifted`（对 aria 新起点重跑）与 `main_repo`（对主仓新起点重跑）—— **完全没有提及 `standards` 这第三个子键**。而 `metadata.baseline_rebase.standards` 本身的文本（v2.2 刚改写的那句, 即 PP2-M4 的返修内容）逐字写着：「standards 是并发轨随时会动的共享子模块, **TASK-001 必须对 B.1 当时的 gitlink 重测**, 不得沿用本行数值」；`tasks.md` 读前必看第 5 条同样逐字写着「1.1 在 B.1 对当时 gitlink 重跑」（1.1 即 TASK-001）。两处「承诺」与 TASK-001 实际的验收清单**不一致**——承诺写在 `metadata.baseline_rebase.standards` 与读前必看表里, 但操作化为可执行步骤的地方（TASK-001 的 verification 列表）没有对应的第三条子步骤。
- **失败场景**: Phase B 执行者进入 B.1（TASK-001）时严格按其 `verification` 的 10 条 bullet 逐条执行（这正是本计划反复强调的「单一 SOT」纪律, hard_constraints 也写「期望值不由实现者现算」）。第 8 条只会让执行者跑两条命令族（针对 aria 与主仓), 不会想到去跑 `git -C standards diff --shortstat 21748d4 <当时 standards gitlink> -- openspec/project.md openspec/templates/proposal-minimal.md conventions/configured-gate-authority.md conventions/version-management.md`。若 B.1 真正开工时（可能是几天甚至几周后）standards 又前进了（这正是它「随时会动」的字面意思, 且它已经在 A.2 到 A.3 短短两天内动过一次——从 `8b49562` 到 `940cb5b`), 台账里就不会出现任何 standards 偏移记录, 而 proposal 与 tasks.md 里引用这四个文件行号的论证（如「重写 b」引用 `standards/openspec/project.md:117-118`、多处引用 `configured-gate-authority.md:35/38/40`）就可能悄悄指向错误的行, 且没有任何机制会让这件事「变红」被发现——这正是 PP2-M4 想要根治的那类失效, 只是这次换了个子键（standards）在同一份文件里重新出现, 且是在修复 PP2-M4 的同一次改动里留下的。
- **它怎么会红**: 目标态——若 TASK-001 补上第三条子步骤（对 standards 的四个被引文件重新 `git diff --shortstat`), 一旦 standards 在 B.1 之前又发生了新的语义变更（如 `configured-gate-authority.md` 再改一次), 该步骤会产出新的 diff 输出, 与 A.2 记录的「零 diff」不符, 执行者据此在台账写偏移表并逐处核对行号——这与 aria/main_repo 两支路径已经具备的机制完全对称。当前坏实现（现状）：不管 standards 在 B.1 之前有没有再动, TASK-001 的清单都不会产生任何检测信号, 「重测」这件事结构上不会被执行, 除非执行者主动跳出 verification 清单去读 metadata 里的另一段散文——而这恰恰与本计划反复强调的「不靠临场判断, 靠清单」相悖。
- **建议修法**: 在 TASK-001 verification 第 8 条（基线复核）里加一个并列子句, 例如：「对 `metadata.baseline_rebase.standards` 点名的四个文件跑 `git -C standards diff --shortstat 21748d4 <standards 当时 gitlink> -- <文件>`；有 diff 即读取新增内容对应的当时行号并入台账偏移表, 无 diff 则维持现状记录」, 使其与 aria/main_repo 两支子步骤同构、同样可执行、同样会在 standards 再次漂移时产生可观察信号。

## R2 对账

- **PP2-M1（claim 身份钉死 + 对 `yielded` 失明）—— closed**。TASK-001 verification 第 1-2 条已改为「按 (本容器, 归一 track_id, `active`) 三元组运行时解析」, 不再引用任何写死文件名；owner_gates 第 14 项触发条件从「只认 `abandoned`」扩到「解析到 `done`/`yielded`/`abandoned` 任一终态, 或本容器该轨无任何 claim」。**我独立复核的证据**：(1) 读 `aria/skills/state-scanner/lib/claim_lifecycle.py` 确认 `_TERMINAL_STATUSES = frozenset({"done","yielded","abandoned"})` 恰好三态, 与 owner_gates 第 14 项列出的三态逐字一致；(2) 直接对真仓 `refs/aria/coordination` 跑 `git show` 读取 `claims/023236f2/s-86f7@1836.yaml`, 实测其 `status: yielded`（与 yaml 记录一致, 印证「钉死写法今天已失效」不是推断而是事实）；同样读取 `claims/bfe8285d/s-73b9@1606.yaml`, 实测其 `status: active`、`track_id: pre-merge-completeness-gate-change-scope`（无容器后缀）, 与新设计「运行时解析出的那一条」完全吻合。
- **PP2-M2（`own_claim_files` 参数化错, 与 M1 同处不同视角）—— closed**。`metadata.coord_ref_precheck.own_claim_files` 已改写为「TASK-001 在运行时按三元组解析出的 claim 文件, 可能不止一条…不是写死的路径」, 并补了「反向指针」说明 `v2_state_runs` 的 N6 取证脚本与生产路径的关系（这是 R2 (d) 条自报薄弱点的可读性建议, 已采纳）。**我独立复核的证据**：读 `heartbeat_by_track` 全文（`claim_lifecycle.py:475-545`), 其文档字符串明确把「同容器多条 active（换 session 再跑认领闸）」称为「the NORMAL case」并对全部匹配项一并刷新（`matches = [rec for rec in ... if rec.container == resolved.container_id and rec.track_id == norm and rec.status == "active"]`), 与 TASK-001「解析到多条 active 不假设唯一…全部纳入」的设计逐字对应, 不是臆造行为。
- **PP2-M3（commit_attribution 把「整条落 FIXED 集」的提交全判 own）—— closed**。路径判据从两分（FIXED/非 FIXED）改三分（exclusive/shared/foreign), 单亲提交判 `own` 需「无 foreign 且（有 exclusive 或提交信息带本轨 `Spec:` trailer）」。**我独立复核的证据（非转述, 亲自重跑）**：把 yaml 里 `metadata.commit_attribution.code` 原样抽出存成脚本, 对真仓 `338418d..5fd7e08`（300 个提交）实跑, 结果 `{"foreign": 251, "foreign-merge": 24, "own": 14, "shared-only": 11}`, 与 revision_log 声称的「近 300 个提交里整条只落 shared 集的有 11 条」完全对上；另写一版带提交哈希输出的变体逐一核对 revision_log 点名的六个提交, 结果 `1b9734a→shared-only`、`5fe15b0→shared-only`、`c9fe08f→shared-only`、`9de3074→foreign`、`5d435e9→own`、`1b6f9ad→own`, 六个全部与声称吻合, 且这 11 条 `shared-only` 中没有一条带本轨 `Spec:` trailer（因为本轨尚未产生任何发布同步提交）。
- **PP2-M4（standards 零 diff 断言已为假；rule6_note 是散文不含 SOT 五字段）—— closed（针对 R2 原始指出的两点）, 但我审查中发现一个与其同族的新缺口, 见上方 Finding 699adf2f**。`metadata.baseline_rebase.standards` 已重写为「`21748d4..940cb5b` 区间实测: 全仓只两个文件变动」并把「零 diff」的断言收窄限定到另外四个被引文件、限定在这两个 SHA 之间；`metadata.rule6_note` 已从散文改写为 SOT `skill-benchmark-exemption.md` 1.1.0 §4.1 的五字段结构（`decision_table_row`/`description_changed`/`scenario1`/`scenario4b`/`negctrl`), 原散文保留为 `note`。**我独立复核的证据**：(1) 直接对真仓跑 `git -C standards diff --shortstat 21748d4 940cb5b -- <四个文件>`, 四个文件输出全为空（零 diff, 与断言相符); 对 `content-integrity.md` 与 `skill-benchmark-exemption.md` 分别跑, 得 `+56/-2` 与 `+21/-3`, 与 yaml 声称的数字逐字相符；(2) 直接读 `standards/conventions/skill-benchmark-exemption.md` §4.1 原文模板, 逐字段核对 yaml 的 `rule6_note`：`decision_table_row: 3` 落在模板允许的 `1|2|3|4|n/a` 内；`description_changed: 'no'` 落在 `yes|no` 内；`scenario4b: not_required` 与 `negctrl: n/a` 在 `description_changed=no` 时不触发 SOT 唯一写死的合规检查（该检查逐字只在 `description_changed: yes` 时才要求 `scenario1`/`scenario4b` 非空), 故当前取值不违反 SOT 的字面合规判据。**但**：TASK-001 的基线复核清单本身没有对 standards 设置对应的重测步骤（Finding 699adf2f), 这是与 PP2-M4「让冻结断言别再悄悄变假」这一诉求同族但更深一层的缺口——R2 只指出了「现在的值是假的」, 我指出的是「即便这次改成真的, 也没有机制防止它在 B.1 之前再次变假而不被发现」。这不影响我判定 R2 原始两点已 closed, 但请一并处理 M1。
- **PP2-M5（`spec_level_undetermined` 的 explicit-only 收窄未成文, 断言恒不变红）—— closed**。读前必看第 8 条把 explicit-only 规则从只覆盖 (S4, `no_spec_unverifiable`) 扩到 `spec_level_undetermined`, 并给 SC-9(4) 的 fixture 新钉 `checkpoints: {post_spec: 'convergence'}`, 新增逐字断言 `checked_checkpoints == ['post_spec']`。**我独立复核的证据（分析性验证, 非仅转述 yaml 自述）**：(1) 我逐行核对了 §1.0 的短路语义——`spec_level_undetermined` 属于三类短路早退之一, 在 P3 阶段发生, 严格早于 P4（逐 checkpoint 求值 `resolved_mode`/装配 `checked_checkpoints` 的阶段）——因此任何「在 P4 末尾统一装配 `checked_checkpoints`」的实现在这一格上必然给出 `[]`（P4 从未开始过, 没有东西可以「统一装配」)；(2) 若不钉 `checkpoints:{post_spec:'convergence'}`, 原 fixture（纯 adaptive, 零 explicit key）下, 哪怕是**正确**的 explicit-only 实现（静态读取原始 config 里非 off 的 explicit 键, 与控制流完全无关）也会得到 `[]` —— 与「批处理式」错误实现的结果撞在一起, 断言 `checked_checkpoints == []` 对两种实现都成立, 没有区分力；补上 `post_spec: convergence` 这个 explicit key 之后, 正确实现给 `['post_spec']`（explicit-only 是纯静态读取, 不依赖 P4 是否跑过), 错误的「批处理式」实现仍给 `[]`（因为 P4 确实从未开始）——两者第一次产生真实分叉, 断言获得区分力。(3) 我还确认了这个补丁手法（钉一个 explicit checkpoint 换取区分力）并非本轮首创——`SC-17(5)` 更早的改写（第 (c) 分支, `no_spec_unverifiable` 的 bypassed 格）已经用同一手法（`checkpoints: {post_spec: 'convergence'}` + `checked_checkpoints == ['post_spec']`），v2.2 只是把它一致地延伸到 `spec_level_undetermined` 这一格，是同一套已验证过的设计模式的自然延伸，不是新发明的、未经检验的手法。

## 对执笔人自报薄弱点的表态

- **(a) trailer 把归属从路径事实降级为提交者声明, 守不住「trailer 写在纯 shared 提交上」**: 可接受。我读了 `commit_attribution.py` 的 `klass()`/主循环逐行确认：只要 diff 里出现任一 `foreign` 路径, 整条提交直接判 `foreign`（在检查 `exclusive`/trailer 之前短路), trailer 永远不能把一个混有 foreign 路径的提交洗白成 `own`——它能扩大的唯一范围是「整条只落 shared 集」这一类提交, 且 owner_gates 第 2/9 项仍要求把 `git log` 清单呈给 owner, 人工复核这一关没有被绕过。
- **(b) M4 的修复是记录更新+范围限定, 不是机制, standards 会再变旧**: **不可接受**。这条自报的担忧我验证是真实存在且具体可定位的——TASK-001 的基线复核清单（verification 第 8 条）确实没有覆盖 standards 的重新 diff, 见 Finding 699adf2f。建议在进入 Phase B 之前补一条子步骤。
- **(c) SC-9(4) 的触发前提是读出来的不是跑出来的（被测脚本要到 Phase B 才存在）**: 可接受。这是 A.3 阶段全部验收判据共有的结构性限制（实现不存在, 无法真的跑一遍确认变绿/变红), 不是可以绕开的缺陷；我在「R2 对账」PP2-M5 条已给出对这条新断言区分力的独立分析性验证（不依赖实际执行), 结论是它确有区分力。
- **(d) N9 新 fixture 用普通文件冒充 shared 路径, 没有复现真正的 gitlink 形态**: 可接受。`commit_attribution.py` 的判据只看 `git diff-tree --no-commit-id --name-only -r <commit>` 输出的路径字符串是否落在 `SHARED` 集合里, 不关心该路径在磁盘上是 gitlink（`160000`）还是普通文件——`git diff-tree --name-only` 对两者输出同样的裸路径名, 判据看不出区别。我自己的验证脚本同样用真实仓库（其中 `aria` 是不折不扣的真 gitlink）跑出了与 fixture 声称完全一致的结果（11 条 shared-only 等), 印证了用普通文件模拟 `aria` 路径不影响这个判据的可信度。
- **(e) 只改了五条 Major 指到的地方, 跨节交叉引用是读着核的加 grep 计数**: 可接受。我自己独立跑了 `git diff 5d435e9 12c870d -- tasks.md detailed-tasks.yaml` 全文逐行核对（而非信任执笔人的自述), 确认改动精确限定在五条 Major + 两条明说的连带 minor（`revision_log` 补条目、版本标识四处), 没有发现任何越界改动；对这种范围明确、可用 `git diff` 完整核验的定点返修，「读着核」是恰当的核验方式，机械全量核对的边际收益不高。
- **(f) 一次自造的路径失误（拼错 scratch 路径), 无实质影响**: 可接受, 与本轮被审文件的内容无关。

### 执笔实例六条请裁项 (owner 尚未裁定, 我的表态)

1. **rule6_note.scenario1 在 A.3 只能是占位, 回填与齐备性断言放 TASK-031**: 可接受——TASK-031 有「断言五字段齐备、无占位尖括号残留」的收口检查, 在 A.3 阶段留占位符合「先声明后回填」的合理设计。
2. **scenario4b/negctrl 依赖 description 零改动、无机械触发器**: 可接受——`TASK-015`/`016`/`017`/`018` 对三份 SKILL.md 的 frontmatter 做逐字比对本身就是事实上的触发器（description 若真的被意外改动, 该比对会失败并挡住组 3 提交); SOT 自己在「已知局限」里也承认「rule6_note 五字段无机械 enforcement」是既有局限, 不是本 spec 应该单独补的债。
3. **M3 的 `Spec:` trailer 是声明不是证明, 替代方案（砍掉 trailer 分支、要求每条提交都含 exclusive 路径）被否决**: 可接受——TASK-029 的交付物（版本号同步）结构上不可能有任何 exclusive 路径, 「每条提交都要 exclusive 路径」这个替代方案会让 TASK-029 永远无法通过 `commit_attribution`, 现有设计（trailer + foreign 优先 + 人工复核不撤）是在给定约束下更合理的取舍。
4. **M3 新增停点（5.7 漏写 trailer 会停在等待点 16）**: 可接受——这是有意选择的 fail-closed 代价（多一次请裁), 不是设计缺陷。
5. **M1 多条 active claim 选「全部纳入+上报」不挑不删**: 可接受——与 `heartbeat_by_track` 的 all-matching 语义完全一致（见上方证据), 是唯一不需要改动底层原语就能自洽的选择。
6. **TASK-030 只改 standards 半句、不碰未裁的 minor 边界切法**: 可接受——这半句本身精确对应 PP2-M4 的返修范围, 边界切得对；但由此连带发现的问题（TASK-001 基线复核缺 standards 子步骤）不是 TASK-030 的责任范围, 而是 TASK-001 自己的缺口, 已单列 Finding 699adf2f, 不应算在这条「边界切法」的账上。

## 风险 / 疑问

- R2 未动的 8 条 minor（`TASK-018` title 不全 / `TASK-029` 版本点行号漂移 / `TASK-030` aria-orchestrator detached 记录过期 / `c25_five_questions` 精度差 / 读前必看第 4 条已消解可收紧 / `TASK-022` SC-11 无区分力子断言 / `guard_config_hooks` 口径窄于分类器 / `v2_state_runs` 硬编码路径）本轮均未获得新证据, 我未重新提出, 状态与 R2 聚合报告一致。
- 我的新 Finding 699adf2f 与 PP2-M4 同族但不是它的直接延续——R2 从未检查过 TASK-001 的 verification 清单是否真的把 `metadata.baseline_rebase.standards` 的「必须重测」承诺操作化, 这是我本轮新做的交叉核对, 不是「PP2-M4 没修完」。
- N5 / N6 / N9 编号缺口（`new_checks` 只有 N1-N4/N7/N8/N10, 中间跳过 N5, N6/N9 其实是 `v2_state_runs` 内部脚本分块的命名而非 proposal 意义上的机检序列）与 R2 时观察到的现象相同, 未变化, 不计入 finding。
- 「§待 owner 复议」条目 1-13 的原文正文本轮未逐条重读（用决策单 §2 的裁定全文替代复核), 若某条原文与决策单转述之间存在我未察觉的偏差, 不在我本轮核验范围内。

## Verdict

verdict: **PASS_WITH_WARNINGS**（0C / 1M / 0m）

**Vote: REVISE**

## 是否足以开始 Phase B

**基本足以，但建议先给 TASK-001 补一条子步骤（Finding 699adf2f）再进 B.1**。这是一处一行级别的清单补漏，不涉及任何 SC、判据代码或任务结构改动，PP2-M1~M5 五条 Major 经我独立复核（含对真仓与真代码的实跑验证，非仅转述）全部确认已闭合；从测试设计与可证伪性视角看，SC-1~SC-22 与 N1/N2/N3/N4/N7/N8/N10 的映射、RED 批次的 AssertionError 机制、反事实设计、三处 Level 3 重写的区分力均无新问题。
