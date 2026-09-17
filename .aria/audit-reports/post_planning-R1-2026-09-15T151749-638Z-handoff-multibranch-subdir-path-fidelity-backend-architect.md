---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-15T15:59:00.424Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — backend-architect 审计报告

## 审计结论

### 实读文件 / 实跑命令清单

- `openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md`(全文)、`detailed-tasks.yaml`(全文, 685 行)——审计对象。
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md`(全文)——依据。
- `openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md`——用 `grep -n` / `sed -n` 按需切片读取 §待复议 2 第 4 行(排序键)、§4(`unreadable_count` 三类外延, `:269-273`)、Task 2.2/2.3/2.5、SC-1/2/5/6/9/10/11/13/14/15/16/18 表格与「SC-15 细则」、Task 5.3(遗留 issue 正文)。
- 代码实读全文: `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py`(755 行)、`scripts/writers/latest_md_writer.py`(320 行)、`scripts/scan.py:120-213`、`scripts/collectors/_common.py:308-440`(`CollectorResult`/`_run` 编码策略)。
- 消费方排查: `grep -rln "tracks_multibranch" aria/skills --include="*.py"` → 确认生产消费方只有 6 个文件(`fetch_gate.py` / `lib/collision.py` / `handoff_multibranch.py` / `track_board.py` / `scan.py` / `latest_md_writer.py`),逐一读取相关片段;另读 `collectors/handoff_worktrees.py:74-104,275-300` 核对「第二读侧」缺口的字面依据。
- 测试实跑(全部只读, 未改动任何文件):
  - `python3 -B aria/skills/state-scanner/tests/run_tests.py` → `Ran 1605 tests in 139.447s … OK`
  - `pytest -q tests/test_collision.py`(state-scanner) → `28 passed`
  - `pytest -q tests/`(phase-d-closer) → `11 passed`
  - `python3 -B -m unittest test_handoff_multibranch_collision_dedupe -v` → `Ran 23 tests … OK`
  - `python3 -B -m unittest test_track_board_advisories -v` → `Ran 5 tests … OK`
  - `python3 -B -m unittest test_scan_integration -v` → `Ran 19 tests … OK`
  - `python3 -B -m unittest test_p1_layer_h -v` → `Ran 24 tests … OK`
  - `metadata.sc11_baseline_predicates` 全部 16 条(a/b/c1/c2/f1/f2/g/i/j1/j2/j3/k1/k2/l1/l2/l3)在当前 checkout(`1cb3872`)上逐条实跑 → **全部 FAIL(即全部具备鉴别力, 无恒真判据)**。
  - `grep -rn "handoff_multibranch_unexpected_path_prefix\|handoff_multibranch_undecodable_path"` → 当前代码与文档零命中, 确认两个新 kind 确系新增。
- `/tmp` 一次性脚本(用完即弃, 未在仓内留痕): 用 `python3 -B` 独立复刻 `_dedupe_sort_key` 的现状(4 级)与 TASK-014 拟改(5 级)两版, 构造 4 组夹具(顶层 vs 子目录同键平局 / 两个子目录平局 / 缺 `rel_path` 键 / 4 级键本身的乱序敏感性对照), 分别正序与反序跑 `max()` 验证。
- 直接 `grep -n` 核对 `references/state-snapshot-schema.md:1105-1138` 与 `VERSION:24` 的现状文本, 与 yaml 引用的行号/内容逐字比对。

### Finding 1 — [Minor] [risk] [implementation] [scope: TASK-009 / `handoff_multibranch.py::_list_handoff_files`]

TASK-009 verification 给出两种前缀剥离实现二选一: `rel = path[len(_HANDOFF_TREE_PATH) + 1:]` **或** `PurePosixPath(...).relative_to(...)`。两者在“路径不以预期前缀开头”场景下行为不同:`relative_to()` 会抛 `ValueError`,天然把异常路由到守卫分支;手工切片不会抛异常——若实现者只写切片、不额外加 `startswith` 判断,前缀不匹配的行会被静默切出一段垃圾字符串并当作合法 `rel` 放行,不会触发 `handoff_multibranch_unexpected_path_prefix`。

照计划执行会出的错:选了切片支且漏加显式判断,SC-9(a)(TASK-003 组 1 写好的 RED 用例,断言这个 kind 字面出现)在 TASK-009 落地后仍为红——不是假绿(因为断言本身会失败),而是实现者需要多一轮返工才能发现漏了这个分支。RED→GREEN 纪律本身兜住了这个风险,不会流入 GREEN/回归阶段,故不到 Major。

建议改法:在 TASK-009 verification 里加一句「若选切片支,必须显式 `if not path.startswith(_HANDOFF_TREE_PATH + '/'): <走 reporter>` 再切片,不能只切不判」,把这条防御性要求从「靠红测试撞出来」变成「计划里写明」。

### Finding 2 — [Minor] [issue] [documentation] [scope: TASK-009 deliverables 行号引用]

TASK-009 deliverables 写 `handoff_multibranch.py # :177-178, :240-288, 主循环 :619-626`。实读 `_list_handoff_files` 函数体是 `:240-290`(`:290` 是 `return filenames, None`),`:288`(`filenames.append(basename)`)确实是该任务要改的最后一行有效代码,但引用区间没包住函数自身的收尾 `return` 行。不影响实施者找到该改哪里(`:288` 已在区间内),纯属引用区间少了 2 行,按纪律第 3 条(措辞/小优化归 Minor)处理。

### 正面核实要点(非 finding,记录以说明 PASS 依据)

1. **TASK-014 排序键公式技术正确** ——`(bucket, dt, filename, branch, (rel == filename, rel))` 在 `max()` 下:顶层行(`rel_path == filename`)对任意子目录行必胜(`True > False` 决定第五元组首位,不看后续);两个子目录行之间按 `rel_path` 字典序取大;`rel_path` 键缺失时按 `filename` 处理且不抛异常。四组夹具正反序独立验证,结论与决策单 §2 第 4 行(“`rel_path == filename` 的顶层行优先,其余字典序”)、schema `:1128`(“invariant to the order `tracks[]` happens to be built/passed in”)不变量宣称完全吻合;当前 4 级键在同一夹具下确实是乱序敏感的(复现了决策单指出的缺陷)。`test_handoff_multibranch_collision_dedupe.py` 里全部既有夹具(含 `TestDedupeTiebreakByBranchWhenUpdatedAtAndFilenameTie`)都不设 `rel_path` 键,新增第 5 级不改变其胜负,`Ran 23 … OK` 的回归声明可信。
2. **`unreadable_count` 三类外延**(TASK-011)与 proposal `:269-273` 定案逐字一致: git show 失败计入 / 前缀守卫丢弃不计入 / 不可解码名(`"�" in rel`)不计入但另报 kind。`_common.py:411-412` 的 `encoding="utf-8", errors="replace"` 确认了“不可解码字节必留 U+FFFD”的前提成立,`rel.encode("utf-8") + except UnicodeError` 判据在本 collector 上确系死代码(反事实成立)。
3. **同文件任务串行**:`handoff_multibranch.py` 的编辑链 TASK-009→010→011→012→014→(019/020)完全线性依赖,无并行编辑窗口;`latest_md_writer.py` 的 TASK-013(依赖 010)与 TASK-020(依赖 012/013/014)不与 009/011/012/014 产生文件重叠。TASK-013 只依赖 010(不依赖 011/012)在语义上成立——写侧守卫只需要 `rel_path` 键存在,不依赖 `unreadable_count`/legacy 构造点的变化。
4. **消费方覆盖完整**:全仓 `tracks_multibranch` 生产消费方仅 6 个文件,`track_board.py` 的 `filename` 引用只出现在注释与纯文本 HANDOFF 列(非链接),不受影响、计划未触碰是对的;`handoff_worktrees.py:82,291` 是经独立验证的“第二读侧”(复用 `handoff.py::_resolve_latest`,与本次改动的 `handoff_multibranch.py` 无关),TASK-025 的 issue 正文 (a)-(f) 条目与本次实读结论逐条对应,是已知、已登记、已裁定推迟的缺口,不是本轮计划的遗漏。
5. **行号锚点抽样精确**:TASK-013 引用的 `_render_pointer :110-148`(含内部调用 `:124`)、`_render_pointer_unavailable :151-169`、`write_latest_md :259-320`(唯一调用点 `:303`)与 TASK-019 引用的 schema `:1106`(legacy 公式)/`:1110`(committer date)/`:1124`(four-level 句)/`:1128`(build-order 不变量句)/`:1138`(fail-soft 形状缺 `unreadable_count`/`identity_advisories`),以及 `VERSION:24` 仍为 v1.73.0,均逐一 `grep -n` 核对,字面 100% 命中。
6. **测试基线数字**:1605 / 28 / 11 / 23 / 5 / 19 / 24 六组数字与 yaml declared 值逐一实跑核对,全部一致。
7. **metadata 算术自洽**:`est_hours` 逐任务求和 = 92.5(与 `est_hours_total` 一致);`agents` 计数(qa-engineer 14 / backend-architect 8 / knowledge-manager 10)与逐任务 `agent` 字段计数一致,合计 32 = `total_tasks`。

## Verdict

**PASS** — 0 Critical / 0 Major / 2 Minor。

## Vote

**PASS**(0 Critical 且 0 Major)。

## 轮次记录

Round 1(backend-architect, convergence): PASS — 0C/0M/2m;核心验证点(TASK-014 五级排序键公式的 `max()` 语义、`unreadable_count` 三类外延、同文件任务串行安排、`tracks_multibranch` 消费方完整性、TASK-009/013/019 行号锚点、6 组测试基线数字、metadata 算术)均实读/实跑核实无误;2 条 Minor 均为文档/实现指引层面的边界情况,均有既有 RED/GREEN 纪律兜底,不影响交付正确性。
