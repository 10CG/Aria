---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T22:05:25.788Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R3 — code-reviewer 席 — handoff-multibranch-subdir-path-fidelity (A.2/A.3 v3.1 `2b9cb3e`)

## 审计结论

### 实读范围

- 审计对象全文: `tasks.md` (159 行) / `detailed-tasks.yaml` (867 行) / `sc11-predicate-validation.py` (340 行), 主仓 master `2b9cb3e` (本地未推送)。
- R2 聚合报告全文; R2 code-reviewer 席报告全文 (用于对照其 N-01..N-13 的落地)。未读同轮其他席位的 R3 报告。
- `git diff --stat 0f50239 2b9cb3e`; v2 形态对照 `git show 0f50239:<change 目录>/{sc11-predicate-validation.py,detailed-tasks.yaml}` 中 (j1)(j2)(j3)(l1) 与 TASK-001 / TASK-032 / TASK-033 相关行 (用于判定「v3 引入」)。
- 上游依据 (只核对, 不审取舍): proposal.md :30-99 (触点清单) / :325-335 (§6 第 5、6 项) / :418 / :422 / :425 / :428 (SC-4 / SC-8 / SC-11 / SC-13 行); 决策单 2026-09-12 §2 的 10CG/Aria#195 表与 §5。
- 代码真值 (aria `1cb3872`, 工作树干净): `handoff_multibranch.py` :1-130 / :170-470 / :556-720; `latest_md_writer.py` :1-60 / :100-175 / :255-325; `scan.py` :172-215; `state-snapshot-schema.md` :1060-1171; `test_handoff_multibranch_collision_dedupe.py` :40-100 / :875-895 / :1150-1175; `scripts/lib/spec_complete.py` :180-600 / :775-910 / :1125-1345 / :1453-1823; `scripts/check_bare_issue_refs.py` 全文; `lib/failure_handlers.py` 的 `no_push_requested_by_env`; `renderers/track_board.py` :738-760; `standards/conventions/content-integrity.md` §4.4 / §4.5; `standards/conventions/session-handoff.md` :95-99 / :168-182。

### 实跑命令与关键输出

临时件全部在 `scratchpad/r3-code-reviewer/`, python 一律 `python3 -B`, 验证脚本运行时 `TMPDIR` 指向其下 `tmp/`。

1. 验证脚本原样: `python3 -B openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py` → `rc=0`, stderr 仅 `verdict: OK (mismatch cells 0, stderr notes 0; 13 states x 19 predicates)`; 结束后 `tmp/` 为空。
2. 一致性自己复跑 (PyYAML 读 yaml, `ast.literal_eval` 读脚本 `PRED` / `EXPECTED`): `measured block == stdout (bytes): True 1692 1692` / `keys equal (order): True` / `all preds equal: True` / `EXPECTED == measured block: True`; `--emit-json` 输出: `states equal: True` / `expected equal: True` / `matrix equal: True`。
3. yaml 19 条谓词直接在 aria `1cb3872` 真工作树 (cwd `aria/skills/state-scanner`) 包成 `if <谓词>; then echo PASS; else echo FAIL; fi` 跑: 19 条全部 FAIL, stderr 为空。
4. 脚本边界与变异: `python3 -B -OO` → `rc=0`; 源码中 `assert` 只出现在 docstring :26 一处文字; 副本目录追加一行重复的 `# Tie-break, finalized (round 3)…` 后以该目录为参数 → `rc=3`, stderr `anchor drift: scripts/collectors/handoff_multibranch.py: 锚点应恰出现 1 次, 实际 2 次: '# Tie-break, finalized (round 3): the sort key is FOUR level'`; 删除 docstring 的 `target` 行 / `base` 行 / 两行都删 → 三个变体均 `rc=0` 且 `verdict: OK` (m4); 参数 `/nonexistent/dir` 与 `-h` → `rc=1`, stderr 末行 `FileNotFoundError: [Errno 2] No such file or directory: '-h/scripts/collectors/handoff_multibranch.py'` (m4); `--help` → `rc=2`。异常退出后 `tmp/` 同样为空 (finally 生效)。
5. 自建态 (复用脚本的 `rep` / `build_target` 等函数, 另写改动, 跑脚本 `PRED`):

   ```
   state                   a1   a2   b    c1   c2   f1   f2   g    i1   i2   j1   j2   j3   j4   j5   k    l1   l2   l3
   base                    FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL
   script_target           PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS
   full_target             PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS
   bad_tuples_stale_para   PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS
   bad_l1_module_scenarios PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS
   bad_l1_neverraises      PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS
   ```

   `full_target` = 脚本 target 另把 `_dedupe_sort_key` docstring 的元组改成五元; 三个 `bad_*` 的构造见 M1 / m1。
6. 候选谓词三态 (定义见 M1 / m1 建议改法; 列 `j1x` 在 `script_target` 上为 FAIL 正是因为脚本 target 留着四元元组):

   ```
   state                   j1   j1x  j3   j3x  l1   l1x  j4
   base                    FAIL FAIL FAIL FAIL FAIL FAIL FAIL
   script_target           PASS FAIL PASS PASS PASS PASS PASS
   full_target             PASS PASS PASS PASS PASS PASS PASS
   reflow_target           PASS PASS PASS PASS PASS PASS PASS
   bad_tuples_stale_para   PASS FAIL PASS FAIL PASS PASS PASS
   bad_l1_module_scenarios PASS FAIL PASS PASS PASS FAIL PASS
   bad_l1_neverraises      PASS FAIL PASS PASS PASS FAIL PASS
   bad_j3_later_tiebreak   PASS FAIL FAIL FAIL PASS PASS PASS
   alt_j3_anchor           PASS FAIL PASS PASS PASS PASS PASS
   ```

   另把脚本 target 补上 docstring 元组编辑、以 `j1x` / `j3x` / `l1x` 替换 (j1)(j3)(l1) 后重跑现有 13 态 x 19 谓词: `diffs vs EXPECTED = []`; 新增坏态 `bad_tuples_stale_para FAIL: ['j1', 'j3']` / `bad_l1_module_scenarios FAIL: ['l1']` / `bad_l1_neverraises FAIL: ['l1']`。
7. (j2) 同形: `bad_j2_tuple_stale_para` → `j2 PASS / j4 PASS`, `j2x FAIL`; `j2x` 在现有 13 态上与 `j2` 逐格相同。
8. 语义正确写法的假红: `alt_a2_fenced` → 仅 (a2) FAIL; `alt_j4_depth_phrase` → 仅 (j4) FAIL (m2 / m3)。
9. 归档门只读预演: change 目录复制到 `scratchpad/r3-code-reviewer/gate/openspec/changes/<id>/`, `sed -i 's/^- \[ \]/- [x]/' tasks.md` (26 个未勾 → 27 个全勾), `sys.path.insert(0, "aria/skills/state-scanner/scripts")` 后 `from lib import spec_complete`, `_find_project_root` 指向 `/home/dev/Aria`, 调 `gate_result`:
   `complete: True | tasks.md 全 [x] (27 task(s), 无 carry-forward/defer 注释)` / `verdict: warn` / `blocking: []` / unverified_claims 3 条 = 2.2 行 `symbol 'HEALTHY_TRACKS' unclassified reference form` · 4.4 行 `no extractable symbol (fail-soft)` · 4.3 行 `dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在` / `d_payload` 非 None (deferred 0, unverified 3) / `soft_errors: []`; 含集成关键词的勾选行只有 2.2 与 4.4; 5.5 行路径 token = `['aria-plugin-benchmarks/ab-results/']` (原样 verified, 换成不存在的结果目录后 unverified)。同一副本只把 5.4 留为未勾: `complete: False | tasks.md has 1/27 unchecked task(s); normalized Status = 'approved' (≠ done)`, deferred 1 (m9)。
10. TASK-029 合并冲突模拟 (scratch 临时仓, `GIT_CONFIG_GLOBAL=/dev/null`): base 1.73.3 → master 发 1.74.0 (plugin.json + CHANGELOG 新节) → feature 先写 1.74.0, 再按第 3 步改为 1.75.0 并提交 → master 上 `git merge --no-ff feature`:

    ```
    CONFLICT (content): Merge conflict in CHANGELOG.md
    CONFLICT (content): Merge conflict in plugin.json
    Automatic merge failed; fix conflicts and then commit the result.
    merge rc=1
    UU CHANGELOG.md
    A  collector.py
    UU plugin.json
    ```
11. 结构: 35 任务 / 105h / qa 15 · backend 10 · knowledge 10, 与 metadata 一致; yaml 27 个 parent 与 tasks.md 27 个 checkbox 相等; 依赖无悬空、无环; `parse_detailed_tasks` → `True 35 task(s) parsed`; 传递闭包下 (TASK-033, TASK-019 / 020 / 023 / 024) 均有序, 共享非台账交付物的任务对全部有序。
12. 命令逐字: TASK-002 命令 1 无输出; 命令 2 输出 `0`; 命令 3 共 13 个 ref、子目录行 0、引号行 0; 命令 4 两份冻结语料均为可解析 JSON dict。TASK-026 探针在不带变量时打印 `False`, 带 `ARIA_COORDINATION_NO_PUSH=1` 时打印 `True`。TASK-025 `grep -n '#<' conventions/session-handoff.md` 在 standards `8b49562` 上零命中 (rc=1)。子模块拓扑: aria / standards 均 `* master … [origin/master]`, remotes 为 origin + github。yaml 中 `''` 只出现在单引号标量 :672 / :673 / :690 / :771 与字面块谓词内, 解析结果均为预期命令; `\x00` (:186) 与 `\[` (:725) 在单引号标量中为字面, :53 双引号标量 `\\[` 解析为 `\[`。
13. 用例数静态计数 (AST, 含继承): test_scan_integration 19 / test_handoff_multibranch_collision_dedupe 23 / test_track_board_advisories 5 / test_p1_layer_h 24; SC-10 八个 unittest 模块合计 169; test_collision 28 个裸函数; phase-d-closer test_fetch_gate 11; `/home/dev/.local/bin/pytest` 存在。
14. 写法: `check_bare_issue_refs.py` 对三份文件 → `裸 issue 引用: 0` rc=0; 对 `git diff 0f50239 2b9cb3e` 三文件的 511 行新增行 (导出到 scratch, 带 `--repo-root=/home/dev/Aria`) → rc=0; §4.5 自查命令无输出; 逐字符扫描: 控制字符 0、希腊字母 0、字面 U+FFFD 0、CRLF 0、行尾空白 0。
15. 事后: 主仓 HEAD `2b9cb3e`、`refs/aria/coordination` `4fd07f9`、aria `1cb3872`、standards `8b49562` 均未变, 三处 `status --porcelain` 为空; aria 下无新 `.pyc`。

### R2 处置落地核验 (本席侧重相关)

| R2 簇 | 处置要点 | 落地 | 证据 | 残留 |
|---|---|---|---|---|
| PP2-M7 | 全矩阵 EXPECTED、try/finally、docstring 逐态列举、TASK-001 rc 口径、yaml 由脚本输出重生成 | 落地, 有残留 | script:213-228 与 :231-245; script:298-320; script:7-23; yaml:169; 实跑 1 / 2 | docstring 自检是子串匹配, 参数错误不走 rc=2 (m4); 谓词块不在 `--emit-json` 输出内且无一致性核验步 (m5) |
| PP2-M8 | (a2) 定位形状 dict、加 `bad_a2_prose_only`、TASK-019 注明 | 落地 | yaml:76; script:192 与 :180; yaml:541; 矩阵该行仅 (a2) FAIL | (a2) 的新锚点未进 authoring_rules (m2) |
| PP2-M9 | 反事实统一进组 3 三步法; TASK-035 / 3.5; TASK-007、TASK-011 删旧条; 同步面 | 落地, 有残留 | yaml:503-524; tasks.md:112; yaml:284; yaml:362; yaml:123; yaml:140; tasks.md:46; tasks.md:137-153 中 SC-1 / 3 / 5 / 14 / 17 为「3.5 + 4.3」, SC-4 / SC-8 为「3.5 (后半) + 4.3」; tasks.md:92 / :100 | yaml:431 与 tasks.md:28 的组 3 枚举未含 3.5 (m10); 补丁 5 的首个失败断言依赖 TASK-003 未钉的取行方式 (m7) |
| PP2-M1 | 依赖补边、TASK-033 只 add 四路径、副本生命周期证据 | 落地 | yaml:537 / :558 / :619 含 TASK-033; yaml:428; yaml:501; 实跑 11 | — |
| PP2-M3 | 组 4 提交点、TASK-021 回归前干净、TASK-029 干净加原位回归、TASK-031 | 落地 (TASK-031 口径经 v3.1 主控改为有范围检查) | yaml:548 / :571 / :631 / :649 / :705 / :822; yaml:585; yaml:771 / :775; yaml:837 | TASK-029 第 4 步排在第 2 步 checkout 之后且无失败处置 (m6) |
| PP2-M6 | 记取号 SHA、前进则重算、合并后核号与两远端同名 tag、回归后打 tag、推前查 tag | 落地, 有残留 | yaml:724; yaml:770 / :773 / :774 / :776; yaml:793 | 「只在 feature 分支改号后重走」必然撞上合并冲突, 第 5 步无冲突分支 (M2) |
| m2 | 5.5 父目录 token 整体替换 | 落地 | yaml:704; tasks.md:128; 实跑 9 | — |
| m4 | 归档门三条 unverified_claims | 落地 | yaml:859; tasks.md:49; 实跑 9 三条逐字吻合 | 预演前须已勾 5.4 未写明 (m9) |
| m9 | (j4) 同义词、扫描面、历史元组写法、两个验证态 | 落地, 有残留 | yaml:88; yaml:113; script:17-19 与 :182-184 | 谓词不看语境, authoring_rules 却写「描述排序键」(m3) |
| m11 | (k) 只认字面 `target_in_subdir` | 落地 | yaml:90; yaml:395; script:185 | — |
| m12 | `p1_docs` 去重 | 落地 | script:133-134 单次替换 | — |
| m14 | (j2) 锚点进 authoring_rules; (j3) 换锚点并加 alt 态 | 落地, 有残留 | yaml:113; yaml:87 (v3.1 python 单行); script:186-187 | (j1)(j2)(j3) 均不钉现状键元组 (M1) |
| m15 | (l1) 加 Scenarios、`bad_scenarios_missing`、读前必看第 14 条 | 落地, 有残留 | yaml:91; script:110 与 :181; tasks.md:31 | 模块 docstring 整体检查与 Returns 分区含「Never raises」段的同形遮蔽 (m1) |
| m16 | 冻结语料 diff 分仓 | 落地 | yaml:590 | — |
| m17 | 写法自检覆盖 PR 正文 / RESULT.md / issue 正文 / 主仓 diff 基线 | 落地 | yaml:839; yaml:701; yaml:744-745 | 「新增行」范围的执行方式未写 (m11) |

### 实施者试派生

1. **TASK-001 (1.3)** —— 可照做: yaml:164-168 的 fetch / ls-remote / merge-base 判定与 41 触点导出 (proposal :44-86 实数 41 行, 类别 12 / 2 / 1 / 26)。卡点: (a) yaml:169 / :170 读的是 aria 工作树, 却没有「检出 B.1 基线并断言 HEAD 与 porcelain」这一步 (m8); (b) rc=1 的处置「按差异格先修谓词」覆盖不到参数错误导致的 `FileNotFoundError`, 也不区分差异格来自模拟改动还是谓词 (m4); (c) 需要改谓词时, yaml 谓词块无法由脚本输出重生成, 两份原文一致性无人核 (m5)。
2. **TASK-020 (4.2)** —— 可照做: 行号表 (实读 :20 / :36 / :40 / :42 / :243 / :298 / :313 / :315 / :332 / :494 / :716-717 均命中所述内容); authoring_rules 对 (j3) 前缀唯一、(j4) 字样、(j5) 行邻接写得清楚; dedupe 测试文件只改 :885 / :1162 两处 docstring 可 `git diff` 核。卡点: 全计划没有一处要求把 collector :370 与 :430 的现状键元组改为五元; 验证脚本的 target (script:91) 就留着 :430 的四元元组而 19 条全绿, 执笔人拿脚本 target 当样板会复制这一形态 (M1)。
3. **TASK-013 (2.5)** —— 可照做: 判据字面、三分派前初始化 `degraded_reason = None`、(k) 只认字面。卡点: `_render_pointer_unavailable(track_id, now)` 现签名收不到原因, 须自行加参数 (可推导, 不计); (l1) 会把写进模块 docstring 顶部场景列表 (:4-11) 或「Never raises」段 (:283) 的 `degraded_reason` 当成 `Return dict schema` (:30-35) / Returns 键列表 (:277-281) 已补 (m1)。
4. **TASK-029 + TASK-034 (5.2)** —— 可照做: 八步命令在当前子模块拓扑下逐字可执行 (两仓 `master` 均跟踪 `origin/master`, 两个 remote); 第 6 步回退前置用 `HEAD^1` / `HEAD^2` 与已记录 SHA, 不依赖可能移动的远端跟踪 ref。卡点: 第 3 步「只在 feature 分支改号后从第 1 步重走」在「号被上游占用」这一预期场景下必然使第 5 步冲突, 计划无分支 (M2); 第 2 步 checkout 早于第 4 步的干净断言, 且第 4 步不成立无处置 (m6)。
5. **TASK-035 (3.5)** —— 可照做: 六个补丁各点名一个组件, 所指断言逐条列出; 补丁 3 与代码路径一致 (无 frontmatter 分支 :686 的 `_get_file_commit_date` 路径参数), 首个失败会落在 `updated_at` 非空; 补丁 4 / 补丁 6 无歧义。卡点: 补丁 5 的所指断言可能被「按 `rel_path` 取行」先打断, 而 TASK-003 没有钉取行方式, 补丁已无法再缩小 (m7)。
6. **TASK-032 (5.4)** —— 可照做: CLI 原句与预期在全勾副本上逐字复现 (实跑 9)。卡点: 预期 `complete=True` 要求预演前 5.4 已勾, 而勾选写在后面的 yaml:862 (m9)。

### Findings

#### M1 [Major] type=issue · category=testing · scope=metadata.sc11_baseline_predicates (j1) yaml:85 · (j3) yaml:87 · 同形 (j2) yaml:86 · sc11-predicate-validation.py:91 · TASK-020 yaml:566 · v3 引入: 部分

**证据**:

- 三条谓词都只判「块内 / 行内出现 `rel_path`」, 不钉现状键元组本身: (j1) 判 `_dedupe_sort_key` docstring 全文含 `rel_path`; (j3) 判 `# Tie-break` 行到 `def _dedupe_sort_key(` 之间任一行含 `rel_path`; (j2) 判任一含 `compound key` 的非表格行含 `rel_path`。键元组所在行是 collector :370 / :430 与 schema :1124。
- 验证脚本自己的 target 就是 (j1) 这个形态。script:91 只改 docstring 首行, 副本实际内容为:

  ```
  scripts/collectors/handoff_multibranch.py:429:     """Full dedupe "latest wins" sort key: five levels (5th = ``rel_path``, top-level first), all-comparable,
  scripts/collectors/handoff_multibranch.py:430:     fully deterministic — ``(parse_ok, updated_at, filename, branch)``.
  ```

  script:9 称 target 为「模拟正确实现: 代码 + 全部文档面 (应全 PASS)」, 矩阵中 (j1) 为 PASS。
- 自建 `bad_tuples_stale_para`: target 基础上两处元组都保持四元, 首行层数改成 FIVE / five, 注释块与 docstring 各新增一段讲第 5 级。副本内容:

  ```
  :368 # Tie-break, finalized (round 4, 10CG/Aria#195): the sort key is FIVE levels, all
  :370 # ``(parse_ok, parsed_updated_at, filename, branch)``.
  :401 # Level 4 rel_path (round 4, 10CG/Aria#195): a top-level row
  :433     """Full dedupe "latest wins" sort key: five levels, all-comparable,
  :434     fully deterministic — ``(parse_ok, updated_at, filename, branch)``.
  :458     ``rel_path`` is the round-4 5th level (10CG/Aria#195): a top-level row
  ```

  实跑 19 条全 PASS (实跑 5)。
- (j2) 同形, 可能性较低 (新段落须恰含 `compound key`): `bad_j2_tuple_stale_para` (schema :1124 改成 five-level 而元组仍四元, :1128 后新增一条同时含 `compound key` 与 `rel_path` 的 bullet) → (j2) PASS、(j4) PASS (实跑 7)。
- 计划文字同样不要求改元组: TASK-020 yaml:566 只写「均描述五级键并点名 rel_path」; TASK-014 yaml:410 的五元字面只约束代码。v3 为反方向 (元组改了、首行仍写 FOUR) 加了 `bad_stale_header`, 这一方向没有状态。
- v3 引入判定: (j1)(j2) 谓词与 script:91 的 target 形态沿自 v2 (`0f50239` 脚本 :39 / :101); (j3) 经 v3、v3.1 两次重写仍取「区间内出现 rel_path」, 且区间终点由 v2 的首个 `def ` 改为 `def _dedupe_sort_key(`, 把 `_updated_at_sort_key` (:402-425) 整个函数纳入了区间。

**照计划执行会出的错**: TASK-020 执笔人照「点名 rel_path」的字面或照脚本 target 改写, 首行写五级、另起一段讲 `rel_path`, 键元组停在四元; TASK-020 / TASK-021 / TASK-029 第 7 步按 SC-11 全部验收通过。ship 后 `_dedupe_sort_key` 的 docstring 与模块注释块自相矛盾, 正是决策单 §2 第 4 行附问「改键支 ⇒ 键层级描述整类改写」要消除的文档面。

**建议改法**:

1. 把 (j1)(j3) 定位到首段里的现状键元组: docstring 取第一个空行之前, 注释块取 `# Tie-break` 到第一个只含 `#` 的行; 要求其中 `(parse_ok` 之后的文本含 `rel_path`。(j2) 限定为同时含 `compound key` 与 `(parse_ok` 的非表格行全部满足同一条件。本席已三态实跑的写法 (实跑 6 / 7):

   ```
   (j1x) python3 -B -c "import ast,sys; t=ast.parse(open('scripts/collectors/handoff_multibranch.py',encoding='utf-8').read()); f=[n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='_dedupe_sort_key'][0]; p=(ast.get_docstring(f) or '').split(chr(10)*2)[0]; i=p.find('(parse_ok'); sys.exit(0 if i>=0 and 'rel_path' in p[i:] else 1)"
   (j3x) python3 -B -c "import sys; L=open('scripts/collectors/handoff_multibranch.py',encoding='utf-8').read().split(chr(10)); t=[i for i,l in enumerate(L) if l.startswith('# Tie-break')]; d=[i for i,l in enumerate(L) if l.startswith('def _dedupe_sort_key(')]; ok=len(t)==1 and len(d)==1 and t[0]<d[0]; e=next((j for j in range(t[0]+1,d[0]) if L[j].strip()=='#'), d[0]) if ok else 0; p=chr(10).join(L[t[0]:e]) if ok else ''; i=p.find('(parse_ok'); sys.exit(0 if ok and i>=0 and 'rel_path' in p[i:] else 1)"
   (j2x) python3 -B -c "import sys; L=[l for l in open('references/state-snapshot-schema.md',encoding='utf-8').read().split(chr(10)) if not l.startswith('|') and 'compound key' in l and '(parse_ok' in l]; sys.exit(0 if L and all('rel_path' in l[l.find('(parse_ok'):] for l in L) else 1)"
   ```

2. script:91 之后给 target 补 docstring 元组编辑 (本席用 `fully deterministic — ``(parse_ok, updated_at, filename, branch, (rel_path == filename, rel_path))``.`), 并加 `bad_tuples_stale_para` 态 (期望仅 (j1)(j3) FAIL)。本席实跑: 替换后现有 13 态 x 19 谓词与 EXPECTED 0 处差异; 元组跨两行书写 (`reflow_target`) 仍全 PASS; `alt_j3_anchor` / `bad_j3_later_tiebreak` 结论不变。
3. authoring_rules 与 TASK-020 yaml:566 补一句「现状键元组写全五元, 留在注释块 / docstring 的首段」。yaml 谓词块、脚本 `PRED`、states / expected / 实测块按既定口径由脚本输出重生成。

#### M2 [Major] type=issue · category=implementation · scope=TASK-029 第 3 步 yaml:770 与第 5 步 yaml:772 · TASK-034 yaml:793 · v3 引入: 部分

**证据**:

- yaml:770「aria origin/master 相对 TASK-027 记录的取号时 SHA 已前进 ⇒ 回 TASK-027 重跑取号计算; 取号值变化则先在 aria feature 分支改号并提交, 再从第 1 步重走本任务」。yaml:772 第 5 步只有 `git -C aria merge --no-ff <aria feature 分支>`, 没有合并失败的分支; yaml:774 的回退前置要求「HEAD 是第 5 步产生的合并提交」且 porcelain 为空, 冲突进行中两条都不成立。
- 「取号值变化」意味着上游已发版: 上游改了版本 5 文件的同一行并在 CHANGELOG 顶部插了新节。feature 分支从 B.1 基线出发改同样的行, 只在 feature 分支改号消解不了文本冲突。实跑 10 的临时仓复现: 第 5 步 `merge rc=1`, `UU CHANGELOG.md` / `UU plugin.json`。
- 这一场景在本仓发生过: aria `ec72175 Merge branch 'master' into feature/a1-entry-claim-duplicate-work-guard — 版本重算 1.70.0→1.71.0 (号被同伴轨占用)`; R2 聚合 PP2-M6 也记录了本轨 A.2 期间另一容器连发 v1.73.2 / v1.73.3。TASK-034 yaml:793「出现同名 tag ⇒ 回退 … 然后回 TASK-027 重新取号」之后的再合并落到同一路径。
- 取号未变、但上游改了本 cycle 同一代码或文档文件时, 第 5 步同样可能冲突, 计划同样无分支。standards 侧同理 (TASK-023 若 bump `session-handoff.md` 版本头, 而 10CG/aria-standards#20 在跟踪同一处)。

**照计划执行会出的错**: 第 5 步冲突后执行者只能临场决定。若在 master 上手工解冲突再提交, 合并提交里就混入了未经 TASK-021 回归与 TASK-026 AB 的冲突解决; CHANGELOG 上游节可能在解冲突时被丢, 而第 6 步只核版本值、第 7 步不核 CHANGELOG, 丢节不会被发现。若自行 `merge --abort` / `reset`, 又没有与第 6 步回退同等的前置与记录要求。

**建议改法**:

1. 第 3 步改为: origin/master 前进 ⇒ 在 aria feature 分支 `git merge origin/master` (先例 `ec72175`), 在 feature 分支上解冲突并按重算值改号、提交; 重跑 TASK-021 两腿回归与 SC-11 全部谓词; 上游带进 state-scanner 代码时, 写明 TASK-026 AB 是否重跑的判据, 或列为 `metadata.owner_gates` 的等待点; 然后回第 1 步。
2. 第 5 步补失败分支: `git merge --no-ff` 退出码非 0 ⇒ `git -C aria merge --abort`, 断言 `git -C aria rev-parse HEAD` 等于第 2 步记下的 SHA 且 porcelain 为空, 输出记台账, 转上一条的 feature 分支路径; 不在 master 上解冲突。standards 同形。
3. TASK-034 yaml:793 回退后的去向指向同一条路径。

#### m1 [Minor] type=issue · category=testing · scope=(l1) yaml:91 · script:207 · TASK-013 yaml:395 · v3 引入: 部分

**证据**: v3 把 `write_latest_md` docstring 的检查收窄到 Returns 段, 理由是「Scenarios 里的 degraded_reason 会掩盖 Returns 段漏改」(tasks.md:50)。同形的两个兄弟位置没有收窄:

- 模块 docstring 仍整体判 `degraded_reason`。其顶部 `Three scenarios are handled:` 列表 (writer :4-11) 也是「单 active track ⇒ 写真指针」的无条件陈述, 补第四种结局时自然会写出 `degraded_reason`, 从而掩盖 `Return dict schema:` 块 (:30-35) 漏补。
- `ret = pre.partition('Returns:')[2]` 取到 `Scenarios:` 之前的全部文本, 包含 :283「Never raises for missing/malformed snapshot data — all edge cases produce graceful fallback content」段, 讲的正是降级兜底。
- 实跑 5: `bad_l1_module_scenarios` (撤回 l1a, 在 :4-11 列表加一条含 ``degraded_reason`` 的子目录结局) 与 `bad_l1_neverraises` (撤回 l1b, 在 :283 段补一句含 ``degraded_reason``) 均 19 条全 PASS。

**照计划执行会出的错**: `Return dict schema` 块或 Returns 键列表漏补时 (l1) 仍为真。TASK-013 yaml:395 已逐处点名这两个块, 漏补概率低于 (j) 族, 按 R2 m15 先例定 Minor。

**建议改法**: 两处都只取「标题到第一个空行」的块; 本席三态实跑见实跑 6, 替换后现有 13 态矩阵 0 处差异:

```
(l1x) python3 -B -c "import ast,sys; t=ast.parse(open('scripts/writers/latest_md_writer.py',encoding='utf-8').read()); w=[n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='write_latest_md'][0]; d=ast.get_docstring(w) or ''; m=ast.get_docstring(t) or ''; blk=lambda s,h: s.partition(h)[2].split(chr(10)*2)[0]; pre,_,scen=d.partition('Scenarios:'); sys.exit(0 if 'degraded_reason' in blk(m,'Return dict schema:') and 'degraded_reason' in blk(pre,'Returns:') and ('degraded_reason' in scen or 'target_in_subdir' in scen) else 1)"
```

并把上述两个坏态加进验证脚本。

#### m2 [Minor] type=risk · category=testing · scope=(a2) yaml:76 · authoring_rules yaml:113 · TASK-019 yaml:541 · v3 引入: 是

**证据**: v3 的 (a2) 有三个新锚点: `**Fail-soft**: branch-list` 行首前缀、`→ ` 后接单反引号、形状 dict 与该行同行。authoring_rules 为 (j2)(j3)(j4)(j5)(k)(l1) 都写了保留约束, 唯独没有 (a2)。TASK-019 要往该 dict 再加两个键, 形状变长后改用围栏代码块是语义正确的写法。实跑 8: `alt_a2_fenced` (target 基础上把形状 dict 移到下方 json 围栏块, 键值不变) → 仅 (a2) FAIL。

**照计划执行会出的错**: 可见假红, 计划没有「改措辞还是改谓词」的口径 (与 R2 N-07 同型)。

**建议改法**: authoring_rules 补「(a2): Fail-soft 行保留 `**Fail-soft**: branch-list` 前缀, 形状 dict 以 `→ ` 加单反引号写在同一行, 键值写成 `"unreadable_count": 0`」。

#### m3 [Minor] type=issue · category=documentation · scope=authoring_rules yaml:113 · (j4) yaml:88 · v3 引入: 是

**证据**: authoring_rules 写「生效后扫描面内一律不用层数词描述排序键」, 而 (j4) 不看语境, 扫描面内任何 `four-level` / `4 levels` / `四级` / `四层` 都判 FAIL; `4[- ]levels?` 也无左边界 (如 `14-level`)。本 change 的主题就是子目录深度, 「nested N levels deep」这类措辞有现实出处。实跑 8: `alt_j4_depth_phrase` (target 基础上在 `_list_handoff_files` docstring 写 "nested 4 levels deep") → 仅 (j4) FAIL。

**照计划执行会出的错**: 描述目录深度而非排序键时假红, 执笔人按 authoring_rules 字面会认为没有违规。

**建议改法**: authoring_rules 改成「扫描面内任何语境都不用这些字样 (谓词不看语境)」; 或正则加左边界, 例如 `(^|[^0-9A-Za-z])(four|4)[- ]levels?`。

#### m4 [Minor] type=issue · category=testing · scope=sc11-predicate-validation.py:248-253 与 :284-320 · TASK-001 yaml:169 · v3 引入: 是

**证据**:

- `check_doc_lists_states` 用子串判断 (`st not in doc`)。删除 docstring 的 `target` 行、`base` 行、两行都删的三个变体均 `rc=0` 且 `verdict: OK` (实跑 4): 残留子串 `target` 来自「target 基础上…」, `base` 来自 `sc11_baseline_predicates`。docstring :30 所说「4 = … 或本 docstring 漏列某状态」对这两态不成立。
- 参数错误不走 rc=2: `/nonexistent/dir` 与 `-h` 都是 `rc=1` 加 `FileNotFoundError` 回溯; docstring :29 写「1 = 任一格不符或任一谓词写 stderr (…); 2 = 参数错误」。
- TASK-001 yaml:169 对 rc=1 的处置写死为「按差异格先修谓词」: 既覆盖不到上面这种没有差异格的异常退出, 也不区分「谓词错」与「模拟改动在新基线上不完整」(B.1 基线若在扫描面内新增了文本, target 的模拟改动没覆盖到, 差异格来自模拟而非谓词)。

**照计划执行会出的错**: B.1 时照 rc=1 口径去修谓词, 可能把有鉴别力的谓词改松来迁就不完整的模拟 (memory author-to-match-checker)。

**建议改法**: 自检改为按行首状态名逐行匹配; `src` 缺文件时打印 usage 并返回 2, 其余未预期异常另设退出码; TASK-001 的 rc=1 口径改为「先判差异格来源 (模拟改动 / 谓词), 放宽谓词须附三态实跑」。

#### m5 [Minor] type=risk · category=testing · scope=TASK-001 yaml:169 · 谓词块头注 yaml:71 · script docstring :31-33 与 :325-328 · v3 引入: 部分

**证据**: 谓词原文有两份 (yaml:75-93 与 script:190-210), 两处都只「声明」逐字一致 (yaml:71、script:33), 计划里没有任何一步核验。yaml:169 要求「矩阵因此需变时由脚本输出重生成 yaml 各块 (不手改)」, 但 `--emit-json` 只输出 `states` / `expected` / `matrix` 三字段 (script:326-328), 谓词块重生成不了; TASK-021 yaml:589 与 TASK-029 yaml:775 跑的却是 yaml 那份。本轮逐字一致是本席用 AST 与 PyYAML 比出来的 (实跑 2), 属审计席代劳。

**照计划执行会出的错**: B.1 修谓词时只改了一份, 验证脚本证明的是脚本那份, 验收跑的是 yaml 那份, 两者静默分叉 (memory pasted-evidence-is-derived)。

**建议改法**: `--emit-json` 增加 `predicates` 字段, 按 yaml 块的 `(label) cmd` 行格式输出; TASK-001 与 TASK-029 第 7 步各加一条「yaml 谓词块与 `--emit-json` 的 predicates 逐字节一致」。

#### m6 [Minor] type=issue · category=implementation · scope=TASK-029 第 2 步 yaml:769 与第 4 步 yaml:771 · v3 引入: 是

**证据**: 第 2 步先 `git -C aria checkout master`, 第 4 步才断言两个子模块工作树干净; 第 4 步不成立没有处置, TASK-028 yaml:749 只写「否则 TASK-029 第 4 步的干净工作树断言不成立」。工作树带未提交改动时 checkout 要么被拒, 要么把改动带到 master 上。执笔人已自报此点, 本席确认。

**照计划执行会出的错**: 改动被带到 master 后, 执行者可能直接在 master 上提交修正, 与 yaml:749「在对应仓的 feature 分支改正」相反。

**建议改法**: 把干净工作树断言 (含 standards 的 `grep -n '#<'`) 移到第 2 步之前, 在 feature 分支上做; 补「不成立 ⇒ 在 feature 分支提交 (只 add 被改文件) 后从第 1 步重走」。

#### m7 [Minor] type=risk · category=testing · scope=TASK-035 补丁 5 yaml:520 与首个失败断言规则 yaml:523 · TASK-003 yaml:203-210 · v3 引入: 是

**证据**: 补丁 5 只把 `archive/latest-notes.md` 行的 `rel_path` 退回 basename, 所指断言为 `rel_path == "archive/latest-notes.md"`; yaml:523 规定首个失败断言不属所指时「缩小补丁 … 不得调整测试断言顺序或削断言」。TASK-003 没有规定 SC-8 后半的用例如何取到这一行。若用例按 `rel_path` 取行 (例: 先过滤 `t["rel_path"] == "archive/latest-notes.md"` 再断言长度为 1), 补丁 5 下先失败的是取行, 而补丁已不能再缩小。

**照计划执行会出的错**: TASK-035 在补丁 5 上走进「偏离 + 记台账 + 追加 AI 流程判断清单」分支, 这本可在 TASK-003 写用例时免掉。

**建议改法**: TASK-003 yaml:203 附近补「SC-8 后半按 `(branch, filename)` 取行, 取到后再断言 `rel_path`」; 或在 yaml:520 写明「按 `rel_path` 的成员断言 (`assertIn` 于 `rel_path` 集合) 即属所指断言」。

#### m8 [Minor] type=risk · category=testing · scope=TASK-001 yaml:166-170 · v3 引入: 部分

**证据**: yaml:169 的验证脚本默认读 `aria/skills/state-scanner` 工作树 (script:290), yaml:170 的谓词也在「B.1 基线 (aria/skills/state-scanner 工作树)」上跑; TASK-001 却没有「检出基线并断言 `git -C aria rev-parse HEAD` 等于 B.1 基线 SHA、porcelain 为空」这一步。fetch 只移动远端跟踪 ref, 本地工作树仍停在 `1cb3872` (memory stale-local-main)。v2 的重跑是有条件的, v3 改为无条件并写出「(aria/skills/state-scanner 工作树)」。

**照计划执行会出的错**: aria origin/master 已前进时, yaml:168 的 diff 报出漂移, 脚本与谓词验的却仍是 `1cb3872` 的文件, 两边都显示通过 (memory partial-freeze)。

**建议改法**: yaml:169 之前补一条: aria feature 分支自 B.1 基线建好并检出后, 断言 HEAD 等于基线 SHA 且 porcelain 为空, 输出记台账。

#### m9 [Minor] type=issue · category=documentation · scope=TASK-032 yaml:859 与 :862 · v3 引入: 否

**证据**: yaml:859 预期 `complete=True`, 只在 27 项全勾时成立。实跑 9: 5.4 未勾时得到 `complete: False | tasks.md has 1/27 unchecked task(s); normalized Status = 'approved' (≠ done)` 且 deferred 为 1。勾 5.4 写在后面的 yaml:862, 两条之间没有先后。v2 (`0f50239` yaml:775 / :778) 已是同一形态。

**照计划执行会出的错**: 先预演后勾选时结果与预期不符, 执行者要临场判断是计划错还是门错。

**建议改法**: yaml:859 开头补「预演前 27 项均已勾选 (含 5.4; 5.5 已按 yaml:704 替换路径 token)」。

#### m10 [Minor] type=issue · category=documentation · scope=TASK-033 yaml:431 · tasks.md:28 (读前必看第 11 条) · v3 引入: 是

**证据**: v3 新增 3.5 / TASK-035 后, 两处枚举没跟上 (memory fix-the-class): yaml:431「TASK-015..018 的一次性副本一律 git -C aria worktree add <scratchpad 路径> <该 SHA>」未含 TASK-035, 对照 yaml:123 与 yaml:703 已写「TASK-015..018 与 TASK-035」; tasks.md:28「3.1–3.3 承接实现后的 GREEN 与反事实」, 而 SC 表所列反事实已归 3.5 (tasks.md:46 / :112)。

**照计划执行会出的错**: 按 TASK-033 字面准备副本时漏掉 TASK-035; 读前必看第 11 条与清单第 8 条去向不一致。TASK-035 yaml:515 自带检出指令, 故 Minor。

**建议改法**: yaml:431 改为「TASK-015..018 与 TASK-035」; tasks.md:28 改为「3.1–3.5 承接实现后的 GREEN 与反事实」。

#### m11 [Minor] type=issue · category=documentation · scope=TASK-007 yaml:286 · TASK-010 yaml:342 · TASK-033 yaml:430 · TASK-028 yaml:746 · v3 引入: 否

**证据**:

- `python3 -B -m unittest test_handoff_multibranch_path_fidelity` / `python3 -B -m unittest test_scan_integration` 等以模块名调用的命令都没写 cwd, 只有在 `aria/skills/state-scanner/tests` 下才能导入; metadata.test_runner (yaml:61) 只给了 run_tests.py 与 pytest 两腿的路径。
- TASK-028 要求「新增行中裸 #<n> issue 引用为 0」并以 `check_bare_issue_refs.py` 手动自检; 该脚本只收文件参数 (`usage: check_bare_issue_refs.py [--repo-root=DIR] <file> [<file>...]`), 违规行只打印 basename, 允许清单从被扫文件向上查找。把 diff 新增行导出到 scratch 文件再扫时, 不带 `--repo-root=` 就读不到 `.aria/bare-issue-ref-allowlist.txt` (本席实跑 14 带了该参数)。

**照计划执行会出的错**: 前者在仓库根执行时导入失败; 后者要么扫整份文件 (存量文字恒红, 与 yaml:748 相悖), 要么扫导出文件却因缺允许清单多报。

**建议改法**: 模块名命令统一写成 `cd aria/skills/state-scanner/tests && python3 -B -m unittest <module>`; TASK-028 写明「导出各仓 diff 新增行到 scratch 文件, 以 `--repo-root=<该仓根>` 调用」。

### 核对无误的部分 (不计 finding)

- 验证脚本 rc=0; 实测矩阵与 yaml 实测块逐字节一致 (1692 字节); EXPECTED 与实测块相同; `--emit-json` 的 states / expected / matrix 与 yaml 三字段相同; 脚本 `PRED` 与 yaml 谓词键序及原文逐字相同。
- 退出码 3 路径与 stderr 格式符合 docstring 与 yaml:169; `python3 -B -OO` 下行为不变; 成功与异常两种退出都清掉临时目录。
- `parse_expected` 对表头键序、列数、单元格取值、行序与 STATES 的一致性检查均为显式判断。
- 19 条谓词在 aria `1cb3872` 真工作树上全 FAIL 且无 stderr; bash 引号、YAML 字面块与单引号转义均按预期解析 (实跑 12)。
- 归档门在 27 项全勾副本上的 complete / verdict / blocking / 三条 unverified_claims / d_payload 与 yaml:859、tasks.md:49 的预期逐项吻合; 5.5 行路径 token 替换规则 (yaml:704) 与 `classify_artifact_claim` 行为一致。
- 35 任务 / 105h / 15·10·10; 27 个 parent 与 27 个 checkbox 一一对应; 依赖无悬空、无环; 组 5 标题的执行序与依赖图一致; `parse_detailed_tasks` 解析成功。
- SC-11 归属三处一致: yaml:72-74 归属注释 ↔ tasks.md:147 SC-11 行 ↔ 各 TASK「为真」声明 (yaml:322 / :340 / :395 / :547 / :570 / :628 与 TASK-021 / TASK-029 复跑)。
- TASK-002 四条命令、TASK-026 变量探针、TASK-025 占位号 grep、TASK-029 第 1 / 2 / 6 / 8 步的 git 命令在当前拓扑下逐字可执行。
- 引用行号抽查: collector :20 / :36 / :40 / :42 / :243 / :298 / :313 / :315 / :332 / :494 / :586-596 / :619-626 / :637-658 / :665-676 / :683-700 / :716-717; `scan.py` :180 / :186 / :193 / :209; `test_scan_integration.py` :164-166; `test_max_branches_resolver.py` :286 / :300 / :316 / :332; `phase-1-collectors.md` :102; `layer-l-integration.md` :105; writer :110 / :124 / :148 / :151 / :159 / :169 / :259 / :277-281 / :287-290 / :303 / :320 —— 均命中所述内容。
- 用例数 19 / 23 / 5 / 24、SC-10 八模块 169、pytest 28 与 11, 与 yaml 所写一致 (静态计数)。
- 16 个版本点 (15 处 1.73.3 加 `VERSION:24` 的 v1.73.0) 全部落在 TASK-030 的 10 个 deliverables 内, TASK-031 的有范围 porcelain 清单不会漏判。
- 三份审计对象的新写文字符合 content-integrity §4.4 / §4.5。
- 执笔人自报存疑点的核对结论: (j4) 缺左边界 → 并入 m3; TASK-029 第 2 步早于第 4 步 → m6; TASK-035 补丁 3 与代码路径一致、首个失败落在所指断言, 补丁 5 → m7; TASK-026 的 8h 在 4-8h 粒度内, 不计; owner_gates 列入 release_gate 协调 ref 推送, 与 hard_constraints yaml:117「外向动作执行前逐项请授权」一致, 不计; 脚本 target 保留 `finalized`, 去掉该词的写法已由 `alt_j3_anchor` 覆盖, 不计。

## Verdict

0 Critical / 2 Major / 11 Minor ⇒ **PASS_WITH_WARNINGS**

## Vote

**REVISE** —— M1: SC-11 的 (j1)(j3) (以及同形的 (j2)) 放过「首行写五级、另起一段点名 rel_path、键元组仍是四元」这一坏实现, 验证脚本自己的 target 就留着 `_dedupe_sort_key` docstring 的四元元组; M2: TASK-029 第 3 步「只在 feature 分支改号后重走」在号被上游占用这一计划已预期的场景下必然让第 5 步合并冲突, 而第 5 步没有冲突分支 (本仓 `ec72175` 有过先例)。两条都能在三份规划文件内定点修, 不涉及 proposal 设计取舍; M1 的替换谓词已在现有 13 态上实跑 0 处差异。

## 轮次记录

Round 3 (code-reviewer, convergence, 新派席位): REVISE —— 0C/2M/11m。验证脚本 rc=0, 矩阵与 yaml 实测块逐字节一致, 谓词两份原文逐字一致, 19 条在基线上全假, 归档门全勾预演与计划预期逐项吻合, 新写文字符合 §4.4 / §4.5, R2 本席侧重相关的 15 项处置全部落地, 其中 10 项留有残留 (已计入 M1 / M2 / m1–m11)。两个 Major: (j1)(j3) 不钉现状键元组, 可被陈旧元组骗过 (部分沿自 v2, v3 / v3.1 重写 (j3) 时未补); TASK-029 取号重算路径缺合并冲突分支 (v3 新增的第 3 步直接通向它)。11 个 Minor 中 6 个由 v3 / v3.1 引入、3 个部分引入、2 个沿自 v2。
