---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-22T21:50:52.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [executability-lens]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R5 — 席位 A「可执行性镜头」

## 镜头与范围

- 被审: `openspec/changes/linked-issue-normalization/detailed-tasks.yaml` (主仓 HEAD `09eb919`, aria 子模块 `9e6a17c` = v1.66.4) 全部 21 条 active 任务的 verification 条目 + metadata 机械判据 (`test_counting_contract` / `version_reference_surface` / `two_classes_of_file` / `append_only_ledger` / `enabled_check_blindness` / `known_env_trap` / `file_domain_serialization` / DAG 自证命令)。
- 方法: 每条判据在基线上**实跑** (主仓工作树零改动; 重跑的测试输出落 scratchpad), 问三问: 基线是什么色 / 目标态会不会翻色 / 引用的路径·行号·数字在 HEAD 上是否准确。
- 不报: 措辞、结构、委派对象、算法本体。
- 基线事实 (供全文引用): 当前版本 **1.66.4** (不是 1.65.5); `state-scanner/tests/run_tests.py` → `Ran 1322 tests / OK`; `aria/skills/run_all_tests.sh` → `7 OK / 0 FAIL / 2 SKIP (累计 1577)` (本机 python3 无 pytest 模块, issue-triage 与 tdd-enforcer 例子被 SKIP); `sc-baseline` 脚本 rc=0, 实测红集合 8 条 = {SC-1, 1b, 3, 4, 5b, 11, 13, 15}。

## 逐条判据实跑表

| 位置 | 判据 | 基线实跑结果 | 目标态预期 | 结论 |
|---|---|---|---|---|
| metadata `scope_repos[].head` | aria `9e6a17c` / 主仓 `084209f` | `git rev-parse`: aria HEAD = 9e6a17c; 084209f 是 HEAD 09eb919 的直接父 (merge-base ancestor) | 不变量 | OK |
| metadata DAG 自证命令 | `python3 -c ... yaml` 输出 21 active / S14 M6 L1 / 88h / qa10 ba7 km4 | 逐字实跑: `21 active | {'M': 6, 'S': 14, 'L': 1} | 88 h | {'qa-engineer': 10, 'backend-architect': 7, 'knowledge-manager': 4}` | 不变量 | OK |
| metadata DAG「⛔ 无同文件并行边」+ `file_domain_serialization` | 同文件任务两两有序 | 脚本枚举 active 任务 deliverables 两两可达性: **`proposal.md` 上 TASK-025 (backend-architect) 与 TASK-027 (qa-engineer) 无序** | 声称为真 | **判据为假 (M3)** |
| metadata 依赖环 / 指向 cancelled | 无环, 依赖全 active | 脚本: 0 环, 0 条指向 cancelled | 不变量 | OK |
| `test_counting_contract.evidence` | `test_invalid_shapes_and_paths` 1 方法 4 场景 | `tests/test_release_by_track.py:282-291` 4 个 assertEqual | — | OK |
| `test_counting_contract.baseline` | run_tests.py 1322 / OK; run_all 9 OK / 1698 | 1322 OK 复现; run_all 实得 **7 OK / 0 FAIL / 2 SKIP / 1577** | 0 FAIL 不变量 | 数字环境相关 (m5) |
| `test_counting_contract.scenario_count: 45` | 逐 SC 场景合计 | 001(13)+002(5)+003(15)+004(8)+005(1)+006(3) = 45; sc-baseline 脚本 16 条 SC 的场景列合计 42 + SC-12 3 = 45 | — | OK |
| `version_reference_surface.breakdown` 14 + 4 | 主仓 14 点 / aria 4 点 | `grep -rn "1\.66\.4"`: README 2 / zh 3 / ja 3 / ko 3 / CLAUDE 2 / VERSION 1 = 14; aria 侧 plugin.json 1 + marketplace :3/:16 + aria/README.md:5 = 4 | 目标态 1.67.0 同分布 | OK (数字准; 但注释「grep 1.65.5」已过时) |
| `enabled_check_blindness` | 两 check 只比 badge / translated-from | `.aria/state-checks.yaml:95` 只 grep badge; `:160` 只 `translated-from:` 正则 | 不变量 | OK (7 处 / 10 处计数均复核正确) |
| `append_only_ledger.why_not_old_value_count` | aria/VERSION 旧值保留形态不一致 | 实测 1.65.4 0 / 1.65.3 0 / 1.65.2 1 / 1.65.1 1 / 1.64.0 1 (与文档一致); 另 1.66.0 2 / 1.65.5 2 | — | OK (结论「阈值不可靠」成立) |
| `known_stale_second_declaration` `aria/VERSION:56-59` | 第二处声明 1.47.0 | 实为 **`:60-64`** (`## 版本号` 在 60, `1.47.0` 在 63); 文件现 172 行 (文档写 167) | — | 引用漂移 (m1) |
| `known_env_trap` | test_collision.py:29-30 sys.path; 4d87060 | `:29-30` 两条 insert 确认; `4d87060` 存在 (2026-05-30); `run_tests.py collision` → `FAILED (errors=1)` | 不变量 | OK |
| TASK-001 v2/v3 | SC-1/1b/3/4 baseline RED, SC-2 GREEN | sc-baseline 脚本: SC-1 红 / 1b 红 / 2 绿 / 3 红 / 4 红 | 目标态翻绿 | OK |
| TASK-001/014 既有 test 点名 | 6 (4+2) + 28 = 34 | ast 统计: TestLinkedIssueOverlaps 4, TestPhase1GateLinkedIssueCli 2, 全文件 34 | 不变量 (git diff) | OK |
| TASK-002 | SC-5b RED; 5/5c GREEN | 脚本: 5 绿 / 5b 红 / 5c 绿 | — | OK |
| TASK-003 | SC-6/6b/10 全 GREEN; phase1_gate.py:1235 | 脚本: 6 绿 (5) / 6b 绿 (9) / 10 绿; `except Exception` 实在 **:1236** (:1235 是调用的右括号) | 护栏 | OK / m3 |
| TASK-004 | SC-11/13/15 RED, 14 GREEN | 脚本: 11 红 / 13 红 / 14 绿 / 15 红 | — | OK |
| TASK-005 | SC-9 GREEN; collision.py:228 | 脚本 SC-9 绿; `:228` 逐字 `"linked_issue": c.linked_issue,` | 护栏 | OK |
| TASK-006 | 三类不可解析例 | proposal.md:244 逐字同三例 | 目标态才可跑 | OK |
| TASK-007 v1 | `from lib import collision` 可取到 | 在 state-scanner 目录下 import 成功, `hasattr(...,'normalize_linked_issue')` = False (基线红, 目标态绿) | 翻绿 | OK |
| TASK-008 | `:217` `!=`; `:210` / `:307` tuple; `:155` 内联 | 四处逐行核实一致 | — | OK |
| TASK-009 v5 | `sys.get_int_max_str_digits()` | py3.11.2, 返回 4300 | — | OK |
| TASK-010 | docstring `:182-206` | 实读 182-206 正是 docstring 区间 | — | OK |
| TASK-011 | claim_schema.py `:107-114` 原文 | `:109-110` 逐字 "Two active claims with the SAME linked_issue" | — | OK |
| TASK-012 | SKILL.md:176 含「同一件事两个名字」 | 逐字命中 | — | OK |
| TASK-013 deliverables | ab-results/ 普通 tree; ab-suite 先例目录 | `git ls-files -s` 无 160000 条目; 两目录存在; 既有 7 个 state-scanner 结果目录 + 4 个 summary.yaml 先例 | — | OK |
| TASK-014 v1/v2 | run_tests.py OK; run_all 0 FAIL | 见基线事实 | 不变量 | OK |
| TASK-022 | marketplace :3/:16; aria/VERSION 167 行 | :3/:16 确认; 行数现 172 | — | OK / m1 |
| TASK-023 | VERSION:24; 14 点 | `VERSION:24` = 子模块表行; 14 点复核同上 | 翻绿 | OK |
| TASK-024 v1 | 整仓 grep 旧版本号 `1.65.5` 差集为空 | 普通引用文件基线 **0 命中** (它们写的是 1.66.4); 排除集外仍有 .aria/decisions / .aria/probes / .aria/repro / .aria/state-checks.yaml / .aria/triage-* / docs/handoff ×9 / openspec/archive ×2 | 见 C1 / M1 | **恒真 + 恒红** |
| TASK-024 v4 | `1.67.0` 出现次数 == 18 | 基线 0 (只在 spec/audit-trail 里) | 翻绿 | OK (建议按文件而非合计, m6) |
| TASK-024 v5(a) | **全部**当前版本声明 == plugin.json | aria/VERSION:3 = 1.66.4; aria/VERSION:63 = **1.47.0** | 正确实现 (不碰 out-of-scope 块) 仍红 | **恒红 (M2)** |
| TASK-024 v5(b) | 行数不减 | 基线 172 | 不变量 | OK |
| TASK-025 v1/v2 | 脚本 :275-277 exit 1; :205-215 FATAL | `:275-277` 是 `measured_face != EVIDENCE_FACE → sys.exit(1)`; `:205-215` 含 `sys.exit("FATAL: 找不到 proposal.md ...")` | — | OK |
| TASK-025 v3 `git grep -l` 口径 | 08-08 实测 proposal 3 行 + tasks.md + yaml 2 处 | 现 yaml **3** 处 (收口新增的 git grep 命令行自含该 token); 条目已写「执行时重跑」 | — | OK |
| TASK-025 v5 路径二可执行 | 改名 spec 目录后脚本不 FATAL | 基线: 脚本硬编码 `_PROPOSAL` 相对路径, 改名即 FATAL (红); 目标态绿 | 翻绿 | OK |
| TASK-027 notes | AB_TEST_OPERATIONS.md:397 / :545 | 逐字命中「Tier 1: 核心 Skills (10 个, 每次发版必测)」/「Tier 1 Skills 全量 AB 测试已执行」 | — | OK |
| `scope_boundary.blocking_note` | phase-c-integrator `:253` 调 merge; branch-manager `:621-634` | branch-manager 621-634 逐字是两条 curl `Do: squash/merge`; phase-c-integrator **`:253` 现为「5. Verdict 计算」**, 触发条件现在 `:164`, green 路径 `:173` (SKILL.md 在 v1.66.0 后已移位) | — | 引用漂移 (m4) |
| `gate_leg_caveat` 2026-08-22 更新 | `pre_merge_gate.py:547` 缺省 main; 缺省在本仓 fail-CLOSED | `:547` 逐字 `default="main"`; 实跑 `pre_merge_gate.py --pr-branch master` → `verdict: fail, main branch 'main' not found on remote 'origin'` | 不变量 | OK |
| 归档门 | tasks.md 21 checkbox 全对应 active | `spec_complete.py --gate` → `21/21 unchecked`; checkbox id 集合与 21 条 active 的 parent 一一对应, 7 条 cancelled 无 checkbox | 不变量 | OK |

## Critical

### C1 — TASK-024 整仓差集断言的「旧版本号」字面已过时, 对普通引用文件维度恒真

- 位置: `detailed-tasks.yaml:823` (TASK-024 verification 第 1 条, `grep 旧版本号 1.65.5`); 同句 `tasks.md:138`; 连带 `detailed-tasks.yaml` metadata `version_reference_surface` 注释「以下为 2026-08-08 实测 (grep -rn "1\.65\.5")」。
- 实跑证据:
  ```
  $ git grep -n "1\.65\.5" -- README.md README.zh.md README.ja.md README.ko.md CLAUDE.md VERSION \
      aria/.claude-plugin/plugin.json aria/.claude-plugin/marketplace.json aria/README.md
  (零输出)
  $ grep -rn "1\.66\.4" README.md README.zh.md README.ja.md README.ko.md CLAUDE.md VERSION | wc -l
  14
  $ git diff 97a3885 HEAD -- openspec/changes/linked-issue-normalization/detailed-tasks.yaml | grep -E "^[-+].*1\.6[567]\.[05]"
  -  ship_target: "aria-plugin v1.66.0 ..."      +  ship_target: "aria-plugin v1.67.0 ..."
  -      - "**新值计数**: ... `1.66.0` ..."       +      - "**新值计数**: ... `1.67.0` ..."
  (旧值 1.65.5 无任何 +/- 行)
  ```
  2026-08-22 收口把新值 1.66.0→1.67.0, 但旧值仍写 1.65.5; 主仓在此期间 ship 了 v1.66.0–v1.66.4, bump 时真正要清的旧值是 **1.66.4**。
- 坏实现反例: 实施者只改 `plugin.json` 与 badge, 把 README.md:242 / i18n ×6 / CLAUDE.md ×2 / VERSION:24 共 10 处留在 1.66.4 不动。按字面 grep `1.65.5`: 普通引用文件零命中 ⇒ 该维度判绿。这正是 R1 Critical-1 要杀的假绿形态, 而此条是它的「根因修法」。
- 一行修法: 旧值改写为「bump 前 `plugin.json` 的值 (当前 = 1.66.4), 执行时 `jq -r .version` 读取, 不写死字面」; `tasks.md:138` 与 metadata 注释同批改。

## Major

### M1 — TASK-024 差集断言的排除集在基线上即不闭合: 正确实现也恒红, 且条目禁止补排除集

- 位置: `detailed-tasks.yaml:824-825` (排除集 + 「⛔ 不许临时往排除集加条目来凑绿」)。
- 实跑证据 (用正确旧值 1.66.4, 去掉 18 个普通引用点与成文排除集后):
  ```
  $ git grep -n "1\.66\.4" | grep -vE "^(aria/VERSION|aria/CHANGELOG.md|\.aria/audit-reports/|openspec/changes/linked-issue-normalization/)" \
      | grep -vE "^(README\.(zh\.|ja\.|ko\.)?md|CLAUDE\.md|VERSION|aria/README\.md|aria/\.claude-plugin/(plugin|marketplace)\.json):" | cut -d: -f1 | sort | uniq -c
        6 docs/handoff/2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md
        6 docs/handoff/2026-08-22-issue179-secret-guard-manifest-precision-ship-v1.66.4.md
        6 docs/handoff/2026-08-22-session-close-179-full-cycle-and-147-supersession.md
        2 docs/handoff/latest.md
        1 openspec/archive/2026-08-22-secret-guard-manifest-precision/detailed-tasks.yaml
        2 openspec/archive/2026-08-22-secret-guard-manifest-precision/proposal.md
        3 openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
        3 openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
  ```
  同一命令在 R4-fix 树 `97a3885` 上用 1.65.5 跑, 同样非空 (docs/handoff ×3, .aria/decisions, .aria/repro, .aria/triage-*, 另一个 spec 的 proposal) ⇒ 这不是 08-22 漂出来的, R4-fix 写下时就从未在基线上跑过 (memory `feedback_new_mechanical_check_must_run_at_baseline_first` 同形)。
- 坏实现反例不需要: **正确实现**也红 —— `docs/handoff/` 与 `openspec/archive/` 是 append-only 史, 不可能也不应该改写; 而条目明令不得往排除集加条目。实施者要么违反该 ⛔, 要么 TASK-024 永远 pending ⇒ 024→028→026 整条关键路径卡死。
- 一行修法: 排除集按**类**成文 (append-only 史 = `aria/VERSION` · `aria/CHANGELOG.md` · `.aria/audit-reports/**` · `docs/handoff/**` · `openspec/archive/**` · `.aria/decisions/**` · `.aria/triage-*` · `.aria/repro/**` · 其他 change 目录的订正留痕), 并把「加条目须写理由」改成「排除集在基线上先跑一次必须为空, 否则断言本身不成立」。同时注明 `git grep` 不跨子模块, 须 `--recurse-submodules` 或两仓各跑一次 (见 m7)。

### M2 — TASK-024 (a)「全部当前版本声明 == plugin.json」对 `aria/VERSION` 的 1.47.0 围栏块恒红, 与 metadata 自述的「不在本 Spec 范围」自相矛盾

- 位置: `detailed-tasks.yaml:827` (v5 (a)) vs `metadata.two_classes_of_file.append_only_ledger.known_stale_second_declaration` (「该块的陈旧本身是 pre-existing 缺陷, 不在本 Spec 范围」)。
- 实跑证据:
  ```
  $ grep -n '^> \*\*版本\*\*' aria/VERSION        → 3:> **版本**: 1.66.4
  $ sed -n 60,64p aria/VERSION                     → ## 版本号 / ``` / 1.47.0 / ```
  ```
  判据 (a) 措辞刻意写「全部」以纳入该块; 该块 = 1.47.0 ≠ plugin.json。
- 坏实现反例 (反向): 按 Spec 范围纪律不碰该块的**正确**实现判红; 为了判绿去改 1.47.0 的实现是 scope creep (aria-report #158 的 issue 明确修的是消费方, 不是这个块)。两个方向只能选一个, 条目没说选哪个。
- 一行修法: (a) 改为「头部 `> **版本**:` 行 == plugin.json; `## 版本号` 围栏块 (:60-64) 显式列为已知陈旧、本 Spec 不动, 或 owner 裁定顺手修并入 TASK-022 deliverables」—— 二选一写死。

### M3 — DAG 断言「⛔ 无同文件并行边」在当前文件上为假: TASK-025 与 TASK-027 同改 `proposal.md`, 不同 agent, 无依赖边

- 位置: `detailed-tasks.yaml` TASK-025 deliverables (`proposal.md` / `tasks.md` / `detailed-tasks.yaml`, 08-22 收口 M5 补入) 与 TASK-027 deliverables (`proposal.md`, 同批补入); DAG 注释「⛔ 无同文件并行边 (见 metadata.file_domain_serialization)」; `file_domain_serialization` 只登记 collision.py 与 test_release_by_track.py 两个域。
- 实跑证据 (对 21 条 active 任务按 deliverables 两两求依赖可达性):
  ```
  UNORDERED same-file openspec/changes/linked-issue-normalization/proposal.md TASK-025 TASK-027
  ```
  TASK-025 = backend-architect (依赖 009), TASK-027 = qa-engineer (依赖 013); 两者在 DAG 上不可达, 且同为 TASK-028 的前置 ⇒ 可同时落盘。
- 坏实现反例: 两个 agent 在各自 worktree 同时编辑 proposal.md (025 改 artifact 指针 3 行, 027 改 §Impact rule6_note), 合并时冲突或一方覆盖另一方 —— 正是 metadata 引 `feedback_workflow_partition_by_file_domain` 要禁的形态; 而该禁令由 08-22 收口自己补 deliverables 时打破。
- 一行修法: 加边 `TASK-027 depends_on TASK-025` (或反向), 把 `proposal.md` 登记进 `file_domain_serialization` 并指定单一 owner; 同时 TASK-025 把 `detailed-tasks.yaml` 列为自身 deliverable 属自引, 建议注明「仅改指针行」。

## Minor

- m1 — `aria/VERSION:56-59` (metadata + TASK-024 v5) 实为 `:60-64`; TASK-022 notes「实测 167 行」现 172 行 (5 次发版各加 1 行)。实跑: `wc -l aria/VERSION` → 172; `grep -n 1.47.0 aria/VERSION` → 63。修法: 行号改「`## 版本号` 围栏块」这种不随发版漂移的锚。
- m2 — `test_counting_contract.baseline`「跨 skill run_all_tests.sh → 9 OK / 0 FAIL / 累计 1698」在本机不复现: `7 OK / 0 FAIL / 2 SKIP / 1577` (python3 无 pytest 模块, `/home/dev/.local/bin/pytest` 存在但解释器不同)。verification 只要求 0 FAIL, 不致误判; 但数字应注明「装 pytest 后」。
- m3 — TASK-003 notes / proposal.md:58 `phase1_gate.py:1235 的 except Exception` 实在 `:1236` (1235 是调用右括号)。
- m4 — `scope_boundary.blocking_note` 引 `phase-c-integrator/SKILL.md:253` (「green 后 :253 直接调用它」) 与 `:242`: 当前 HEAD `:253` 是「5. Verdict 计算」, 触发条件在 `:164`、green 路径在 `:173`。收口刷新了 `pre_merge_gate.py:547` 却未刷这两处同文件引用。branch-manager `:621-634` 准确。
- m5 — `version_reference_surface` 注释「以下为 2026-08-08 实测 (grep -rn "1\.65\.5")」: 分布数字今日用 1.66.4 复核全部一致, 但口径字面过时 (与 C1 同根)。
- m6 — TASK-024 v4 新值计数写成**合计** 18; `two_classes_of_file.normal_reference.invariant` 写的是**逐文件** == 预期点数。坏实现反例: README.md 多写 1 处、README.ja.md 漏 1 处, 合计仍 18 判绿。修法: v4 改「逐文件按 breakdown 核, 合计仅作交叉和」。
- m7 — TASK-024 v1「对全部 tracked 文件 grep」未给命令; 主仓根 `git grep` **不进子模块** (本次实跑 1.65.5 列表里没有任何 `aria/` 文件即证), 而排除集却列了 `aria/VERSION` / `aria/CHANGELOG.md`, 暗示期望覆盖 aria 侧。修法: 写死 `git grep --recurse-submodules` 或「两仓各跑」。
- m8 — 文件引用的 9 个 memory 名在 `~/.claude` 全树零命中: `feedback_submodule_pointer_post_merge_bump` / `feedback_sync_instruction_not_push_authorization` / `feedback_fix_recurs_in_its_own_fallback_path` / `feedback_invariant_needs_failclosed_default` / `feedback_invariant_dimension_must_match_error_dimension` / `feedback_false_green_dual_is_permanent_red` / `feedback_workflow_partition_by_file_domain` / `feedback_written_exception_exact_condition_match` / `feedback_audit_marginal_return_goes_negative` (实跑 `find ~/.claude -name "<name>*"` 各 0; nexus 搜索亦无)。其中 TASK-028 的「推送授权依据」与 TASK-024 的「判据依据」是承重引用。反讽: cancelled TASK-016 notes 专门声明「不转引不存在的 memory」, 而它点名不存在的 `feedback_partial_push_creates_mirror_divergence` 现已存在 (MEMORY.md 索引 1 命中)。修法: 承重处把依据内联一句, 不靠 memory 指针。

## 核实为正确的清单 (供下轮免重复)

- DAG 自证命令输出 21 / S14 M6 L1 / 88h / qa10 ba7 km4 逐字复现; 无环; 无依赖指向 cancelled; tasks.md 21 checkbox 与 21 条 active parent 一一对应, 7 条 cancelled 为删除线无 checkbox; `spec_complete.py --gate` 读出 21/21 unchecked。
- `scope_repos[].head` 两个 SHA 准确。
- SC baseline 色表 (TASK-001~005 全部 RED/GREEN 声称) 与 `sc-baseline` 脚本实跑 16 条逐格一致, 红集合 8 条与 TASK-025 的「8 条」一致; 场景数 13/5/15/8/1 与脚本场景列一致, 合计 45。
- 既有 test 方法 6 (4+2) + 28 = 34, ast 统计准确; `test_invalid_shapes_and_paths` 4 场景准确。
- collision.py `:155` / `:182-206` / `:210` / `:217` / `:228` / `:307` 六处行号全部准确; claim_schema.py `:107-114` 原文准确; SKILL.md `:176` 准确; test_collision.py `:29-30` 与 `4d87060` 准确; `from lib import collision` 在 state-scanner 目录下可导入。
- `sys.get_int_max_str_digits()` = 4300 (py3.11.2) 存在。
- 主仓 14 点 / aria 4 点 (marketplace :3/:16) 分布用 1.66.4 复核一致; enabled check 失明面 (badge-only / translated-from-only) 读 state-checks.yaml 确认, 7 处 / 10 处计数正确。
- aria/VERSION 旧值保留形态表 (1.65.4 0 / 1.65.3 0 / 1.65.2 1 / 1.65.1 1 / 1.64.0 1) 准确; 「行数不减」基线 172。
- `#137` 修法核实: `pre_merge_gate.py:547` 缺省 main, `_verify_main_branch_exists` 存在, 实跑缺省值 → `verdict: fail / main branch 'main' not found on remote 'origin'` (fail-CLOSED 成立)。
- sc-baseline 脚本 `:205-215` FATAL 与 `:275-277` exit 1 准确; `git grep -l sc-baseline-linked-issue-normalization` 当前 17 文件, 交付面 = proposal.md 3 / tasks.md 2 / detailed-tasks.yaml 3 (收口自引 +1, 条目已要求执行时重跑)。
- AB_TEST_OPERATIONS.md `:397` / `:545` 逐字准确; `aria-plugin-benchmarks/` 为主仓普通 tree; `ab-suite/phase-c-integrator-pre-merge-gate-fixtures/` 存在; state-scanner 既有 7 个结果目录 + 4 个 summary.yaml 先例, TASK-013「与上一次结果比对」非空真。
- branch-manager `:621-634` 两条 `Do: squash/merge` curl 准确。
- `run_tests.py collision` 单模块 `FAILED (errors=1)` 复现 (#134 陷阱仍在); 全量 1322 OK。

## Verdict

**vote: REVISE** (Critical 1 / Major 3 / Minor 8)。

其中「由 R4-fix 或 2026-08-22 收口 (commit 09eb919) 引入」的 major: **3** 条 (M1、M2 由 R4-fix 新写的整仓差集 / 「全部声明」判据引入且从未在基线实跑; M3 由 08-22 收口补 deliverables 引入)。C1 同样由 08-22 收口引入 (改新值未改旧值)。

本轮形态与前四轮相同: 四条 C/M 全部落在「为修上一轮 Major 新写的机械判据本身不成立」—— TASK-024 一条 verification 里集中了恒真 (C1)、恒红 (M1、M2) 两种对偶。建议修法原则: 每条新判据在写进 YAML 前先在基线上跑出预期色 (红/绿), 把命令与输出贴在条目里, 不写字面数字。
