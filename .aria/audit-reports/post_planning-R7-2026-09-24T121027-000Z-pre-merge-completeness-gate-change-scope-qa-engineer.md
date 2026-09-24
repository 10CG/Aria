---
checkpoint: post_planning
mode: convergence
rounds: 7
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-24T12:58:23.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R7 — qa-engineer 席报告

## 已实读文件

派单 sha256[:16] = 24cda7a220add7e4

**派单与背景**
- `/tmp/claude-1000/-home-dev-Aria/82379761-f707-4902-a23a-45070cee8ae7/scratchpad/r7-prompts/qa-engineer.md` (全文, 109 行)
- `.aria/audit-reports/post_planning-R6-2026-09-22T142418-000Z-pre-merge-completeness-gate-change-scope-aggregated.md` (全文)

**被审文件 (全文)**
- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` (246 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` (2067 行; `metadata` 全部键逐一定位读, 31 个 TASK 逐条读 verification, 重点通读 TASK-001~013 / 019~022 / 024 / 029~031)
- `git diff e7a1782 320d523 -- openspec/changes/pre-merge-completeness-gate-change-scope/ .aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py` 全量 diff (v2.5→v2.6)

**proposal.md / 决策单**
- `## Why` `:23`、`## What` 各节 `:70-392` (含 §1.2 `:409-428` B.0 语料冻结全文)、`## Tasks` `:407-452`、`## Success Criteria` `:453-479`、`## rule6_note` `:480-487`、`## 待 owner 复议` `:488-` 起始段 (核对 #1-#13 编号范围)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文 116 行

**CLAUDE.md**: 多远程推送两条硬约束、不可协商规则 #3/#6/#8/#10 (随会话常驻内容核对)

**源码实读 (真仓 `/home/dev/Aria`, 只读, 未做任何写操作)**
- `aria/skills/run_all_tests.sh` 全文 88 行 (`is_pytest_suite()` 精确到 `:41-46`)
- `aria/skills/audit-engine/tests/test_sibling_spec_probe.py` `:1-45`、`:303-336` (`TestNoPytestImport` / `TestRunAllTestsDiscovery` 两条守卫)
- `aria/skills/state-scanner/tests/test_heartbeat_only_cli.py:190-230`
- `aria/skills/state-scanner/tests/test_coordination_no_push.py` (grep 定位 `ARIA_COORDINATION_NO_PUSH` 用法)
- `aria/skills/phase-c-integrator/scripts/submodule_gate.sh` 全文 335 行 (`check_override_trailer:96-126`、`check_pr_label:128-150`、`check_override:152-158`、逐子模块输出 `:253-312`)
- `aria/skills/state-scanner/scripts/lib/spec_complete.py:850-1050` (`_grep_symbol_occurrences` / `_classify_file_occurrence` / `classify_symbol_liveness`)
- `aria/skills/state-scanner/scripts/collectors/custom_checks.py` 全文 (SKIP 语义 `:319-321` 附近)
- `.aria/state-checks.yaml:408-430` (`plugin-version-arch-docs-match` 完整 command)
- `aria/skills/state-scanner/scripts/{release_gate.py,phase1_gate.py}`、`lib/{claim_lifecycle.py,gc.py,coordination_ref.py}` (grep 定位调用关系, 核 `write_claim` / `apply_tree_edits` 的封闭调用集)

**实跑 (全部在我自己的 scratch 目录, 两份共享基准均先 `cp -a` 到自己目录再用, 未碰共享副本)**
- `metadata.v2_state_runs` 脚本 (`a2_v2_checks.py`) 独立重跑两次: 一次基于 `base-Aria` (真仓 `9a3ac24` 全量副本), 一次基于 `state-base-mine` (主仓 `a563192` + aria `1cb3872` 嵌套 clone, `cp -a` 自 `p199-r7/state-base`) —— 两次均与 yaml 内嵌 `output` **逐字节一致** (含 v2.6 新增 N12)
- `metadata.a2_state_runs` 脚本 (`a2_state_runs.py`) 重跑: 用 `state-base-mine` (与脚本设计前提 `a563192+1cb3872` 一致) 得到与 yaml 内嵌 `output` **逐字节一致**；另外用 `base-Aria` 重跑会不一致 (根因 = `base-Aria` 含本轨自己的 `.aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py`, 使 `classify_symbol_liveness` 判定提前变 `alive`) —— 这是**测试环境选择问题**, 已由 R4 (`0dd2d3f2`) 发现、R5 用官方 `state-base` 重跑坐实"环境选错"并结案, 我用正确环境复核到位, 不构成新证据, 不重开
- `grep -cxF` 对 track-id 精确匹配 (`pre-merge-completeness-gate-change-scope`) 与拼写错误 (`...scopes`) 两态的独立复验
- custom check `plugin-version-arch-docs-match` 的实际 shell 命令在 `base-Aria` 的主仓根与 `aria/skills/audit-engine/tests` 两个工作目录下独立实跑

---

## R6 对账

逐条给出我亲验的证据 (对照 `git diff e7a1782 320d523`、当前 yaml/tasks.md 正文、及对应真实源码)。

**`354faf33` (已知项 A: track-id 逐字断言 + 删不可达停点) — closed**
- `tasks.md` 判断清单第 46 条与 5.9 checkbox 行、`detailed-tasks.yaml` TASK-031 的「写后五字段自校验」条均已加 `head -8 <handoff> | grep -cxF 'track-id: pre-merge-completeness-gate-change-scope'` 须为 1 的逐字断言, 且删去了 v2.5 原写的「写成别的或漏写 ⇒ 判 foreign, 停在 owner_gates 第 16 项」(diff 第 279-281 行确认)。
- 我独立验证该 grep 的判别力: 精确值 → 打印 `1`、exit 0; 拼写为 `...change-scopes` (与执笔报告反事实 CF-1 相同的错法) → 打印 `0`、exit 1。E1 (字段是否存在) 与 v2.5 的「值非空」检查对这个拼写错误都会给满分 (仅检查有没有值), 只有新加的逐字比对能拦住 —— 与计划自述一致。
- 残留缺口 (提交归属仍无 `commit_attribution` 覆盖) 执笔人已在自报薄弱点 (1) 中承认, 我的表态见下文。

**`6ad0a84b` (条目序号引用改锚点式) — closed**
- diff 确认至少 5 处具体替换: `TASK-024 末条`→`TASK-024 的『结束后先取第二次快照』条` (2 处)、`TASK-023 末条`→`TASK-023 的『开 AB 会话之前』条` (2 处)、`TASK-001 第 1 条`→`TASK-001 的 claim 身份条 (三元组运行时解析那一条)` (2 处, `metadata.claim` 与 `coord_ref_precheck.own_claim_files`)、`完成上条比较`→`按本任务的快照比较条完成比较`。
- 我独立用 `grep -noE "(末条|上一条|下一条)"` 对当前 tasks.md + yaml 重新扫描, 剩余命中里我抽查了 `tasks.md:79`「5.9 末条 Phase D 提交经授权双推」—— 核对当前 5.9 checkbox 行原文, 最后一句确实是「获授权后 Phase D 提交双推并逐 remote 核验」, 该引用现在仍然指对; 其余大量 `第 N 条` 引用 (判断清单 / owner_gates 两个全局列表) 属于**只追加、不在中间插入**的稳定列表 (v2.6 版本标识条自陈"等待点编号不变…31 个 TASK 与各任务条目数不变, 全文既有『第 N 条/第 N 项』引用不因本轮增删而移位"), 与本轮修的"TASK 内部小列表相对引用"不是同一失效机制, 未见新的错误锚点。
- v2.6 版本记录条 (yaml revision_log) 给出的扫描口径与分类闭合 (299 处 = 139 正确 + 28 上下文核过 + 8 自身编号 + 2 泛指 + 22 计划外 + 11 历史原… + 79 revision_log 历史 + 10 本轮改) 算术自洽 (139+28+8+2+22+11+79+10=299)。

**`2c2e8931` (写协调 ref 前一律先强制对齐, 覆盖 release/重新认领) — closed, 有独立实跑证据**
- `hard_constraints` 第 4 条已从"仅覆盖心跳"改写为通则; TASK-031 的 D.2b claim 条与 TASK-001 的重新认领段均已加入"前置检查退出 0 后先强制对齐再解析/推送"的步骤 (diff 确认)。
- **我独立重跑了 `metadata.v2_state_runs` 的完整脚本** (含新增 `n12_block()`), 两次不同基准环境下输出均与 yaml 内嵌 `output` 逐字节相同, 包括关键的 N12 结果: `[as-written (v2.5 order): release_gate straight after precheck] exit=0 ... released.success=True push_success=False remote_equals_local=False` 与 `[v2.6 order: forced alignment, re-resolve] ... [v2.6 order: release_gate after alignment] exit=0 ... push_success=True remote_equals_local=True`。这直接坐实了修复前后的行为差异是真实可复现的, 不是叙述性断言。
- 我另外验证了"写入路径封闭集"的前提: 全仓 `grep` 确认 `claim_lifecycle` 与 `gc` 两个模块只被 `phase1_gate.py` 与 `release_gate.py` 两个脚本 import (`release_gate.py:42,46,56,60` 的延迟 import), 其余 `aria/skills/*/scripts/` 下无第三方入口, 支持"8 条写入路径"结构性封闭的说法。

**`749f8d15` (C.2.4.5 override 口径按调用时机改写) — closed, 有源码验证**
- TASK-030 与 owner_gates 第 17 项已改为: override trailer 须落在 PR head 提交上或改用 PR 标签 `submodule-rollback-approved`; 放行判据改为"退出 0 且被 override 的子模块有 `GATE:` 行与其后的 `ALLOW:` 行"。
- 我直接读了 `submodule_gate.sh` 源码验证: `check_override_trailer()` (`:101`) 确实是 `git log -1 --format=%B HEAD` (读运行时 HEAD, 不是合并提交), `check_pr_label()` (`:128-150`) 确实经 `forgejo GET /repos/.../issues/$PR/labels` 判定、API 失败或无 `ARIA_PR_NUMBER` 均 `return 1` (fail-closed)。逐子模块的真实输出顺序 (`:263` `GATE:` → 有 override 时 `:297` `ALLOW: ... overridden by per-PR marker`, 无 override 且 block 模式则 `:308` `BLOCK:`) 与计划新写的判据逐字符合。

**`29325b2c` (custom checks 看输出首行, `##SKIP##` 算没跑成) — closed, 有源码 + 实跑验证**
- TASK-029 已改为逐条列出六个 check 的期望首行 (四条 `OK`、`no-unresolved-version-placeholder` 通过时无输出、`plugin-cache-currency` 预期 `STALE`), `hard_constraints` 第 (3) 条已把 `##SKIP##`+退出 0 的形态补进已知清单。
- 我读了 `collectors/custom_checks.py` 源码确认: `status = "skip" if first_line.lstrip().startswith(SKIP_MARKER) else "pass"` (仅当 `rc==0`), 三态里 `skip` 既不计 `passed` 也不计 `failed` —— 与计划描述完全一致。
- 我直接实跑了 `.aria/state-checks.yaml` 里 `plugin-version-arch-docs-match` 的真实 shell 片段: 在 scratch 副本主仓根跑, `PLUGIN=1.73.3`, 走"非 SKIP"分支; 切到 `aria/skills/audit-engine/tests` 目录跑同一段代码, `PLUGIN=` 为空, 打印 `##SKIP## aria/.claude-plugin/plugin.json 不可读` 且 `exit=0` —— 与计划里"六条在主仓根 OK/OK/OK/OK/无输出/OK, 换到 audit-engine/tests 目录后 plugin-version-arch-docs-match 变 `##SKIP##` 仍退出 0"的具体断言完全吻合。

**结论: R6 五条 minor 全部 closed, 均有本席亲验证据 (2 条含独立脚本重跑, 3 条含真实源码/命令核对), 无一条降级为 partially 或 open。**

---

## Findings

无。逐项独立复核 (两次完整脚本重跑 + 十余处源码 `file:line` 核对 + 若干条实际命令执行) 未发现新的、满足"影响执行者会不会做错/做漏/卡住"严重度口径的问题。

说明: 我在验证"三处重写"机制时,最初用真仓当前全量副本 (`base-Aria`, 含本轨自己的 `gen_yaml.py`) 重跑 `a2_state_runs.py`,得到与 yaml 内嵌证据不一致的结果 (`status=ambiguous` vs `alive`)。深入排查后确认这是**我自己的测试环境选择错误**——`a2_state_runs.py` 设计上要求跑在不含 `gen_yaml.py` 的 `a563192` 冻结快照上 (脚本 docstring 逐字写明),而非当前全量副本；换成派单指定的 `state-base` (`a563192`+`1cb3872`) 重跑即逐字节一致。进一步查证这条排查路径本身在 R4 (`0dd2d3f2`) 已被发现、R5 已用同样的正确环境复核并结案(结论:根因是"取证环境用错",不是"嵌入证据失实";且即便 `status` 字段被 `gen_yaml.py` 干扰,真正决定 TASK-021/031 通过与否的 `L2 = status=="alive" and "aria_plugin_integration" in alive_categories` 不受影响)。因此这不是新证据,不重开为 finding,仅在此说明我做过这项核查、结果与 R5 一致。

---

## 对执笔人自报薄弱点的表态

**(1) track-id 断言只守 handoff 文件内容, 不守提交归属** — 可接受。`commit_attribution` 全计划只在 TASK-001/TASK-030 调用, TASK-031 本就不跑它 (本轮已把这一点写清楚, 见 R6 对账 `354faf33`); 残留风险是"提交打了正确 track-id 但提交本身被误分类", 这一面确实只剩 owner 在 13b 项人工看 diff 一道关, 但这是显式、有记录的人工检查点, 不是静默漏检; knowledge-manager 提的"13b 之前重跑判据"是可选的加固而非必须, owner 未采纳已是明确裁定, 不应在本轮重提。

**(2) 协调 ref 对齐通则只枚举了两处例外, 未来新窗口会冲突** — 可接受。这是对**未来假设性扩展**的坦诚风险披露, 不是本计划当前范围内的缺陷 —— 本计划内确实只有 AB 会话与 release 之后这两处不允许 fetch 的窗口 (我未找到第三处), 通则与两个例外目前互斥完备; 若将来真的出现新窗口, 那时候修改通则即可, 不构成现在就要处理的问题。

**(3) PR 标签路径未实跑, 只按代码断言** — 可接受。我直接读了 `check_pr_label()` 源码 (`submodule_gate.sh:128-150`): 逻辑简单 (检查 `ARIA_PR_NUMBER` 是否存在、调 `forgejo GET`、匹配标签名), 且方向 fail-closed (无 `ARIA_PR_NUMBER`/`forgejo` 命令缺失/API 失败一律 `return 1` 即视为无标签, 不会误放行); trailer 路径 (更复杂、涉及 git 提交信息正则匹配与 SHA 解析) 才是真正需要活体验证复杂分支覆盖的地方, 已做三臂实跑。标签路径缺活体证据是可控的剩余风险, 不影响执行方向的安全性。

**(4) custom checks 首行口径依赖现有 16 条实际形态, 未来新 check 用 stderr/第二行输出 SKIP 会漏** — 可接受。本轮的同族扫描已完整覆盖当前 16 条 (含唯一命中 `##SKIP##` 形态的一条), 这是对**现有**形态的完整覆盖; "未来新增 check 用不同位置输出 SKIP" 是对新增内容的前瞻性提醒, 不是本计划遗漏, 本计划也没有新增任何 custom check。

**(5) 序号引用清单 38 行是人工判定** — 可接受。这类"引用消歧"任务 (判断一处"上一条"具体指向哪个位置) 本质上需要读懂上下文语义, 不可能纯用正则机械穷举; 执笔人已如实披露判定词写在扫描脚本字典里、可逐行复核, 这是恰当的透明度, 不是遮掩。我自己抽查的 `tasks.md:79` 一处即在此类"上下文核过"范围内, 复核结果正确。

**(6) N12 用 `git update-ref` 把协调 ref 拨回, 是取证手法非真实场景** — 可接受, 且描述准确。我读了 `n12_block()` 源码, 确认 `update-ref` 那一行确实只是为了让"as-written"与"aligned-first"两条路径从**同一个**分叉起点分别起跑,以便做受控 A/B 对比 (排除掉"两次 release 面对不同初始状态"这个混淆变量),这是标准的单变量对照法,不代表生产环境会真的对同一状态 release 两次; 计划全文我没有找到依赖"同一状态两次 release"这个假设的其它地方。

---

## 风险 / 疑问 (不计入 finding)

1. **`submodule_gate.sh` 自身的提示文案可能过时**: 脚本在 block 模式下打印的 `Override 1: add commit trailer ... to merge commit message` (`:309`) 字面上仍指"合并提交", 但按本计划这次调用方式 (Forgejo 合并前、HEAD=PR head) 该提示已不准确 —— 这是脚本自身 (源自更早的 spec #124, 不属本计划交付物) 的文案与本次新增调用场景不完全贴合, 不属于本计划的缺陷; 计划自身在 TASK-030/owner_gates 第 17 项的文字已经正确覆盖了这个细节, 呈给 owner 的请求会用计划自己的准确描述, 而非仅转述脚本这行提示, 因此不构成执行风险, 仅供 owner/后续维护 `submodule_gate.sh` 时参考。
2. **`a2_state_runs` 证据对测试环境敏感**: 如上所述, 该三态证据必须在不含 `.aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py` 的冻结快照上跑才能复现, 这一前提已经写在脚本自己的 docstring 里且被 R4/R5 坐实, 不需要本轮改动; 仅提醒任何后续想复核这份证据的人 (包括 owner) 务必使用 `state-base` 而非"当前真仓完整副本"。
3. **协调 ref 写入路径的"8 条封闭集"**: 我用全仓 grep 独立验证了 `claim_lifecycle`/`gc` 只被 `phase1_gate.py`/`release_gate.py` 引用, 支持了 `2c2e8931` 同族扫描"44 候选单元、7 处执行落点"的结构性前提; 我没有把 44 个候选单元逐条重新过一遍 (那份逐条清单只在执笔报告里, 不在仓内), 只做了"封闭集边界是否成立"这一结构性核验, 供 owner 参考此核验的范围边界。
4. **未处置项** (R5 另三条 minor `34b92188`/`27cee280`/`ae4753f5`、R4 另四条独立 minor、v2.4/v2.5/v2.6 执笔实例提请 owner 裁定的各条): 本轮未发现超出既有记录范围的新证据, 不重提为 finding。

---

## Verdict

**0C/0M/0m**

verdict: PASS

**Vote: PASS**

---

## 是否足以开始 Phase B

**从验收设计与可证伪性的视角: 足以。** R6 五条 minor 在 v2.6 全部 closed 且有独立复核证据 (含两次脚本级逐字节重跑), 本轮未发现新的 critical/major/minor 问题; SC-1~SC-22 与 N1-N10 的 RED/转绿/反事实映射表与各 TASK 的 verification 逐一核对一致, 三处重写与新检查的三态证据在正确测试环境下可靠复现, 测试风格约束与 `run_all_tests.sh`/`test_sibling_spec_probe.py` 的真实分类逻辑相符。**但入口门 (owner_gates 第 1 项: 10CG/Aria#195 已完成 C.2 合并或 owner 明示改序) 仍未满足** —— 这是外部客观事实, 与本计划自身质量无关, 不构成对本计划验收设计的否定。
