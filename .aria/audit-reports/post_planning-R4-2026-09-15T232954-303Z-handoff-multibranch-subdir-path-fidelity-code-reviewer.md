---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T23:55:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R4 — code-reviewer 席 (字符级正确性)

对象: 主仓 master `edd256d` 上的 `tasks.md` (167 行 / 27 checkbox) + `detailed-tasks.yaml` (895 行 / 35 TASK) + `sc11-predicate-validation.py` (405 行 / 18 态 x 19 谓词)。aria `1cb3872`, standards `8b49562`。本席 R1-R3 未参与。

counts: **0 Critical / 1 Major / 8 Minor** · vote **REVISE**

## 审计结论

### 实读范围

- 三份审计对象全文; R3 聚合报告全文 (`post_planning-R3-2026-09-15T212707-499Z-...-aggregated.md`)。
- 上游依据只读不审: `proposal.md` 的相关段落经 tasks.md「读前必看」转述核对; 决策单未逐字重审 (按任务约束)。
- 被谓词与任务引用的真实源码/文档: `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py` · `scripts/writers/latest_md_writer.py` · `scripts/collectors/_common.py` · `scripts/lib/spec_complete.py` · `scripts/check_bare_issue_refs.py` · `references/{state-snapshot-schema,phase-1-collectors,layer-l-integration}.md` · `tests/fixtures/freeze_corpus.py` · `aria/CHANGELOG.md` · `standards/conventions/{content-integrity,session-handoff}.md` · 主仓 `VERSION` / `CLAUDE.md` / `.aria/state-checks.yaml` / `docs/architecture/*` / `.aria/config.json`。
- 未读: 同轮其他席位的 R4 报告 (按约束)。

### 实跑命令与关键输出

只读; 临时件全部落 `.../scratchpad/r4-code-reviewer/`, `TMPDIR` 指向其 `tmp/` 子目录, 结束时已清。未跑 `scan.py` / `run_tests.py` / `phase1_gate.py` / `release_gate.py`。

1. 验证脚本主跑 — `TMPDIR=<scratch>/tmp python3 -B openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py`
   `rc=0`; stderr 单行 `verdict: OK (mismatch cells 0, stderr notes 0; 18 states x 19 predicates)`; 耗时 3.8s; 运行后 `TMPDIR` 为空 (finally 清理生效)。

2. 两份谓词原文 / 三字段一致性 — 用 `--emit-json` 实跑后与 yaml 逐字节比对 (自写比对脚本, 非目测):
   `MATRIX byte-identical: True` · `PREDICATES byte-identical: True` · `states equal: True` · `expected equal: True` · `matrix equal: True`。
   即 yaml `measured_2026_09_15_at_1cb3872_v4` / `states` / `expected` 与脚本输出四项全部逐字节相同, m11 的机械核验点成立。

3. 退出码六态实跑 (逐条构造):
   - `rc=0` 正常; `rc=1` 改 EXPECTED 一格 -> `mismatch [alt_j4_numeric][a1]: expected FAIL, got PASS`;
   - `rc=2` 三条路径 (`--nope` 未知 flag / `a b` 多参 / 空源目录, 后者打印 usage 并点名 6 个缺失文件);
   - `rc=3` 改锚点 -> `anchor drift: scripts/collectors/handoff_multibranch.py: 锚点应恰出现 1 次, 实际 0 次: ...`;
   - `rc=4` 两条路径 (改 EXPECTED 表头 -> `EXPECTED 表头与 PRED 键序不一致`; 删 docstring 一行 -> `docstring 的状态列表漏列: ['alt_j4_numeric']`);
   - `rc=5` 源文件 chmod 000 -> `unexpected error: PermissionError: ...`。
   `python3 -OO` 下 `rc=0` 且 stdout 与 `-B` 逐字节相同。

4. 独立坏态对抗 (本席自建, 未沿用脚本内建状态) — 见 M1 与 m1。

5. 归档门只读预演 (`spec_complete.py`, 只读: 内部只用 `git grep` / `grep -rn`) — 三态:
   - A: 27 行全勾、5.5 保留父目录 token -> `complete=True verdict=warn unverified_claims=3`;
   - B: 27 行全勾、token 换成尚不存在的结果目录 -> `4` 条 (5.5 行被判 `无可链接产物路径`);
   - C: 27 行全勾、token 换成**已存在**的结果目录 (= 执行时的真实形态) -> `complete=True verdict=warn`, 恰 **3** 条, 理由逐条为
     `symbol 'HEALTHY_TRACKS' unclassified reference form` / `no extractable symbol (fail-soft)` / `dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在`。
   与 TASK-032 写的预期 (complete=True / warn / 三条, 分别落在 2.2 / 4.4 / 4.3) **逐项一致**。A 与 C 的对比也实证了 TASK-032 那句「残留父目录会让抽验恒过」。
   另实跑 CLI 原样写法 `python3 -B aria/skills/state-scanner/scripts/lib/spec_complete.py --gate <change 目录>` 可直接执行 (包内模块直跑不报 import 错), rc=0。

6. 计划里被点名的基线数字逐条复跑: `test_handoff_multibranch_collision_dedupe` Ran 23 · `test_track_board_advisories` Ran 5 · `test_scan_integration` Ran 19 · `test_p1_layer_h` Ran 24 — 与 TASK-014 / TASK-016 / TASK-010 / TASK-013 所写全部吻合。

7. 行号锚点抽样实读 (全部命中): collector `:177/:178` · `:243` · `:246-247` · `:355` · `:368` · `:370` · `:428` · `:430` · `:586-596` · `:619` · `:644` · `:665-676` · `:683-698` · `:36/:332/:494`; writer `:30-35` · `:110/:111` · `:140` · `:151/:152` · `:159` · `:259` · `:277-281` · `:287-290` · `:303` · `:320`; schema `:1106` · `:1124` · `:1138`; `phase-1-collectors.md:102`; `layer-l-integration.md:105`; CHANGELOG `grep -n "^## \[1.70.0\]"` -> 200, `### Fixed` 202 / `### Added` 209 / `### Changed` 215; 主仓 `VERSION:24` 仍是 v1.73.0 · `state-checks.yaml :124/:177/:408` · `CLAUDE.md :139/:141` · `system-architecture.md:189` · `version-scheme.md:23`。

8. 可执行性抽测: TASK-026 的变量探针命令逐字复跑 -> 输出 `False` rc=0 (`lib.failure_handlers.no_push_requested_by_env` 确在 `aria/skills/state-scanner/lib/`, 只插 skill root 即可); `/home/dev/.local/bin/pytest` 存在; `check_bare_issue_refs.py` 确有 `--repo-root=DIR` 且缺 allowlist 时退化为空清单 (不返回 rc 2); TASK-002 命令 1 / 2 逐字复跑 (`find` 无输出; `ls docs/handoff | LC_ALL=C grep -c -P "[^\x00-\x7F]"` 输出 0); `_common._run` 用 `encoding="utf-8", errors="replace"` -> TASK-011 的 `chr(0xFFFD) in rel` 判据成立。

9. 结构核对: yaml 可解析, 35 任务 / 105h / 15·10·10 与 metadata 声明一致; 依赖无悬挂、无环; 27 个 parent 与 tasks.md 27 个 checkbox 双向全等; `.aria/config.json` 实读确认只有 post_spec / post_planning enabled (post_implementation / pre_merge / post_closure 为 off), 故 Phase B/C 不会再产生本 Spec 的审计报告 — TASK-031 有范围核验不会因此卡住。

### R3 处置落地核验 (本席侧重相关项)

| R3 项 | 要求 | 落地 | 证据 |
|---|---|---|---|
| PP3-M7 (1) | (j1)(j3)(j2) 换 `j1x`/`j3x`/`j2x`, 钉 `(parse_ok` 之后含 rel_path | 已落 (**但不充分, 见 M1**) | yaml `:90/:91/:92` 与脚本 `PRED['j1'/'j2'/'j3']` 逐字节一致; `git diff 2b9cb3e edd256d` 显示三条整体替换 |
| PP3-M7 (2) | 新增 `bad_tuples_stale_para` / `bad_j2_tuple_stale_para`, target 补 `_dedupe_sort_key` docstring 元组编辑 | 已落 | 脚本 `:174-189` 两个 builder; `collector_docs` 的 `j1t` 键 (`:100`) 补 docstring 元组; 矩阵两行期望为 `(j1)(j3) FAIL` / `(j2) FAIL`, 实跑一致 |
| PP3-M7 (3) | authoring_rules + TASK-020 补「现状键元组写全五元」 | 已落 | yaml `:123` authoring_rules「(j1)(j3)(j2) 现状键元组写全五元并留在首段」; TASK-020 `:585`「注释块 :370 与 docstring :430 的 (parse_ok, …) 元组各加第 5 元」 |
| m7 | (l1) 换 `l1x` (两处只取「标题到第一个空行」的块) + `bad_l1_module_scenarios` / `bad_l1_neverraises` | 已落 (**标题行余部未排除, 见 m1**) | yaml `:96`; 脚本 `:191-203` 两 builder; 矩阵两行仅 (l1) FAIL, 实跑一致 |
| m8 | authoring_rules 补 (a2) 书写约束 | 已落 | yaml `:123` 开头「(a2) Fail-soft 行保留 ... 改用围栏代码块即假红」 |
| m9 | authoring_rules 改「任何语境都不用」+ (j4) 正则加左边界 + `alt_j4_numeric` | 已落 (**边界语义有窄缺口, 见 m6**) | yaml `:93` `(^|[^0-9a-z])(four|4)[- ]levels?`; 脚本 `:205-209` builder; 实跑 `14-level key` 不命中、`4 levels` / `the four-level key` 命中 |
| m10 | 自检改行首匹配 / 缺文件 rc 2 / 其余异常另设码 / TASK-001 对 rc=1 的口径 | 已落 | `check_doc_lists_states()` 用 `ln.startswith("  ")` + `ln.split()[0]`; `missing_src` 分支返回 2; `except Exception` 返回 5; TASK-001 `:183` 写死五种退出码处置。六态实跑见上 |
| m11 | `--emit-json` 增 `predicates`; TASK-001 与 TASK-029 第 7 步各加逐字节一致 | 已落 | 脚本 `:392`; TASK-001 `:182`; TASK-029 第 7 步 `:797` |
| m12 | TASK-003 补 SC-8 后半按 `(branch, filename)` 取行 | 已落 | TASK-003 `:223` |
| m13 | TASK-001 补检出基线并断言 HEAD / porcelain | 已落 | TASK-001 `:181` |
| m14 | unittest 统一 `cd .../tests && python3 -B -m unittest <module>`; `--repo-root` | 已落 | TASK-007 `:301` / TASK-010 `:357` / TASK-033 `:446` / TASK-016 `:482` 均带 cd; TASK-028 `:768` 带 `--repo-root=<该仓根>` |
| PP3-M1 | 27 行勾选并到 TASK-032 归档预演之前; TASK-026/028 去掉自勾 | 已落且自洽 | TASK-032 `:886`; TASK-028 `:772`; 清单第 15 条; yaml 全文 `tasks.md` 零次出现在任何 deliverables -> 除 Phase D 外无提交点, TASK-031 有范围核验不会被自己踩 |
| PP3-M2 | 干净断言前移到 checkout 之前; 占位检查改查提交内容; 删旧工作树 grep | 已落 (**表述矛盾, 见 m2**) | TASK-029 第 2 步 `:791` 在第 3 步 checkout `:792` 之前, 用 `git -C standards show <feature>:...` 读提交内容 |
| PP3-M3 / M4 | 第 4/5/6 步 fail-closed; `push --atomic` 每远端一条, 禁 `--follow-tags` | 已落 | TASK-029 `:793-796`; TASK-034 `:816` |
| PP3-M5 | delta 写死 mean(with)−mean(old); 删 WITHOUT_BETTER | 已落 | TASK-026 `:717`; 全仓 grep: yaml/tasks.md 里 WITHOUT_BETTER 仅剩 4 处**解释性**提及 (「已删去 / 不适用」), 无一处仍作要求 |
| PP3-M9 | 四任务 deliverables 补台账行 + 标题注释 | 已落 | 自写程序化核对: 对 35 个 TASK 判「verification 提台账 => deliverables 含 verification-ledger.md 且带 `# §...` 注释」, **零违规** |

### 实施者试派生 (只看该任务与其引用文件)

1. **TASK-014 (2.6 排序键第 5 级)** — 可无歧义执行。实现字面给全 (`return (bucket, dt, filename, row.get("branch") or "", (rel == filename, rel))` + 注解 `tuple[int, datetime, str, str, tuple[bool, str]]`)。语义自洽: `max()` 下 `(True, ...)` 胜 `(False, ...)`; 与 TASK-005 两组用例对得上 (`x.md` vs `archive/x.md` 选前者; `archive/x.md` vs `old/x.md` 选 `old/x.md`, `'o' > 'a'`)。缺 `rel_path` 键的行退回 filename 也不抛。无卡点。

2. **TASK-013 (2.5 写侧守卫 + 契约面)** — 可执行。三个布局的分派可从判据字面推出: 布局 6 (缺 filename 且缺 rel_path) 下 `rel = None or None = None`, `rel == filename` 成立 -> 走真指针分支 -> `_render_pointer` 内既有的 `if not filename` 早退 -> `(unavailable 文案, "missing_filename")`, 与 TASK-006 期望的 `action == pointer` + `degraded_reason == "missing_filename"` 一致。布局 3 (只缺 rel_path 键) 下 `rel = filename` -> 真指针, 而 TASK-018 的坏实现 `track.get("rel_path") != filename` 会翻成降级 -> (g)(j) 红, 鉴别力成立。卡点: 无。

3. **TASK-029 (5.2 八步)** — 大体可执行, 两处需临场裁决:
   - 第 2 步的占位检查两个条件字面互斥 (见 m2);
   - 第 5 步只为「退出码非 0 (冲突)」写了 `merge --abort`; 若非冲突性失败 (无 MERGE_HEAD) 则 `--abort` 自身会报错。第 2 步的干净断言使其概率很低, 但计划没写这一支。
   其余步序自洽: 第 3 步记下的 origin/master SHA 被第 5/6 步与回退条、TASK-034 复用; 第 6 步回退条的前置 (`HEAD^1` / `HEAD^2` / porcelain) 在第 5 步成功后确实成立, 而第 5 步冲突中止时前置不成立且计划已显式写「不执行回退, 直接停下上报」。

4. **TASK-035 (3.5 七条反事实补丁)** — 可执行。补丁 1 的「现表现形态」已写死 (`tracks[]` 无该行 + `handoff_multibranch_git_show_failed` + `unreadable_count == 1`), 且与 TASK-011 删 `:644` 的因果链对得上 (实读 `:639-658` 确认 git show 失败支才是 legacy 追加处, `:686` 是无 frontmatter 支 -> 补丁 3 指的是后者, 与 TASK-011 删的不是同一处, 无冲突)。补丁 5 依赖夹具是否带 frontmatter, 而夹具由同一执笔链的 TASK-003 写, 可自洽。卡点: 无。

5. **TASK-020 (4.2 键层级描述整类)** — 可执行, 一处需注意: authoring_rules 说「历史轮次的键用元组表述, 不用层数词」, 而基线 docstring 里的 `round-3 4th level` 属序数不属层数词, (j4) 实测不命中, 脚本 target 也未改它 — 执笔者若为「遵守 authoring_rules」而把它改写成 `four-level`, 反而会踩 (j4)。建议在 TASK-020 里点名「`4th level` 这类序数保留不改」。

### findings

#### M1 [Major] type=issue · category=testing · scope=detailed-tasks.yaml `metadata.sc11_baseline_predicates` (j1)(j2)(j3) + sc11-predicate-validation.py · v4 引入: 部分

**(j1)(j3)(j2) 的 v4 收窄只堵住「另起一段讲 rel_path」, 没堵住「同段 / 同注释块 / 同一行里在元组后面补一句 rel_path」; 三处现状键元组仍可保持四元而 19 条全 PASS。**

R3 PP3-M7 的处置目标是「钉现状键元组」。v4 的实现是「取块 -> 找 `(parse_ok` -> 要求其后出现 `rel_path`」。问题在于「其后」= 该块 / 该行的**全部剩余文本**, 而不是元组本身。于是最自然的一种坏实现 —— 改了句子里的层数词、在元组后面追加一句「第 5 级是 rel_path」、唯独忘了编辑元组 —— 照样为真。

证据 (本席自建三态, 复用脚本自身的 `build_target` 后单点撤回, `TMPDIR` 指向 scratchpad):

```
ADV-1 (j1: docstring 首段内, 元组留四元, 下一句讲 rel_path)
  改动: 保留 ``(parse_ok, updated_at, filename, branch)``., 其后同段追加
        "The 5th level is ``rel_path`` (top-level rows first)."
  实测: j1=PASS  j2=PASS  j3=PASS  j4=PASS  j5=PASS      <-- 应为 j1 FAIL

ADV-2 (j3: # Tie-break 注释块内, 元组留四元, 块内续写 rel_path)
  改动: "# ``(parse_ok, parsed_updated_at, filename, branch)``, with ``rel_path``
         # appended as the 5th level."
  实测: j1=PASS  j2=PASS  j3=PASS  j4=PASS  j5=PASS      <-- 应为 j3 FAIL

ADV-3 (j2: schema 键序行内, 元组留四元, 同一行后缀 plus `rel_path`)
  改动: "the **five-level** compound key `(parse_ok, parsed updated_at, filename, branch)` plus `rel_path`"
  实测: j1=PASS  j2=PASS  j3=PASS  j4=PASS               <-- 应为 j2 FAIL
```

**照计划执行会出的错**: TASK-019 `:562` 与 TASK-020 `:585/:589` 把「(j1)(j3)(j2) 为真」写成验收项, TASK-021 / TASK-029 复跑同一组谓词。上述三种写法下验收全绿, 而 schema `:1124` / collector `:370` / `:430` 三处对外宣告的「现状排序键」仍是四元 —— 正是 R3 PP3-M7 认定的缺陷类原样存活。与 memory `author-to-match-checker` / `redfix-change-quantity` 同形: 两轮都在同一个量 (「块内是否出现 rel_path」) 上挪边界, 没有换量。

**建议改法 (换量: 只看 `(parse_ok` 起的那一对平衡括号之内)**。本席已把三条替换在 10 个状态上实跑, 与现行谓词在既有全部状态上零差异, 且在三个新坏态上正确转红, 对「元组跨两行书写」的合法写法不假红:

```
state                    现行 j1/j2/j3        建议 j1X/j2X/j3X
base                     FAIL/FAIL/FAIL       FAIL/FAIL/FAIL
target                   PASS/PASS/PASS       PASS/PASS/PASS
ADV-1                    PASS/PASS/PASS       FAIL/PASS/PASS
ADV-2                    PASS/PASS/PASS       PASS/PASS/FAIL
ADV-3                    PASS/PASS/PASS       PASS/FAIL/PASS
bad_tuples_stale_para    FAIL/PASS/FAIL       FAIL/PASS/FAIL
bad_j2_tuple_stale_para  PASS/FAIL/PASS       PASS/FAIL/PASS
bad_j3_later_tiebreak    PASS/PASS/FAIL       PASS/PASS/FAIL
元组跨两行 (合法写法)     PASS/PASS/PASS       PASS/PASS/PASS
alt_j3_anchor            PASS/PASS/PASS       PASS/PASS/PASS
```

三条都能写成单行 (已实跑通过), 核心片段:

```
d=list(itertools.accumulate((c=='(')-(c==')') for c in s)); e=next((k+1 for k,x in enumerate(d) if x==0), 0)
sys.exit(0 if i>=0 and e>0 and 'rel_path' in s[:e] else 1)
```

其中 `s = <块或行>[<'(parse_ok' 的下标>:]`, `(j3)` 保留现有的「`# Tie-break` 恰一行且在 `def _dedupe_sort_key(` 之前」fail-closed 前置, `(j2)` 保留现有的「非表格行且同时含 `compound key` 与 `(parse_ok`」取行与 `all()`。

同批需要做的: 新增三个坏态 `bad_j1_same_para` / `bad_j3_same_block` / `bad_j2_same_line` (期望分别仅 (j1) / (j3) / (j2) FAIL), 由脚本 `--emit-json` 重生成 yaml 的 `states` / `expected` / 实测矩阵 (不手改); authoring_rules 里「元组写全五元并留在首段」后面补一句「第 5 元写在元组括号之内, 写在元组之后的说明句不算」。

#### m1 [Minor] type=issue · category=testing · scope=(l1) 谓词 · v4 引入: 是

**`l1x` 的「标题到第一个空行的块」实际包含标题行的余部, 三种「把 degraded_reason 写进标题行括注」的写法仍为真。**

`blk = lambda s,h: s.partition(h)[2].split(chr(10)*2)[0]` 从标题串**之后**开始截, 所以 `Return dict schema: (另含 degraded_reason)` 里的括注落在块内。实测:

```
ADV-4  模块 docstring 写 "Return dict schema: (自 10CG/Aria#195 起另含 ``degraded_reason``)", 字典字面量不动 -> l1=PASS
ADV-5  write_latest_md 写 "Returns:  (另含 ``degraded_reason``)", 键清单不动                     -> l1=PASS
ADV-6  写 "Scenarios: (每支都返回 ``degraded_reason``)", 第四种结局不写                          -> l1=PASS
```

三者比 M1 刻意, 且矩阵里已有的 `bad_l1_module_scenarios` / `bad_l1_neverraises` 覆盖了两种更自然的漏改, 故计 Minor。改法是一个字符级的小改: 把 `s.partition(h)[2]` 换成 `s.partition(h)[2].partition(chr(10))[2]` (丢掉标题行余部), 与 M1 的编辑同批落即可。

#### m2 [Minor] type=issue · category=implementation · scope=TASK-029 第 2 步 · v4 引入: 是

**占位检查的两个条件字面互斥, 且自然负控写死为「输出 1」可能与实际占位处数不符。**

原文 (yaml `:791`): `git -C standards show <feature>:conventions/session-handoff.md | grep -c '#<' 为 0, 且同一输出正向含第三态从句与 10CG/aria-plugin#<n>`。字面上 `10CG/aria-plugin#<n>` 自身含 `#<`, 与「`grep -c '#<'` 为 0」不可同真; 执行者必须临场判定 `#<n>` 是元记号。另: 自然负控写「TASK-025 回填前同一命令输出 1」, 但 TASK-023 要求 `:171-173` 与 `:97` 两处都补限定从句, 若 `:97` 也带跟踪引用则回填前是 2。

改法: 正向条件写成可执行式, 例如 `grep -qE '10CG/aria-plugin#[0-9]+'` (或 TASK-025 的回落形态字面), 负控写成「非 0 (占位处数)」而不是写死 1。

(基线核对: 在 standards `8b49562` 上 `grep -c '#<' conventions/session-handoff.md` 输出 0 / rc=1 — TASK-025 `:691` 那句「v3 执笔时实跑为零命中, 故该检查不会恒红」属实。)

#### m3 [Minor] type=risk · category=testing · scope=TASK-029 第 6 步 · v4 引入: 是

**新加的 CHANGELOG 节计数断言, 其写明的触发场景已被同轮的另一条处置排除, 计划未写出它真正的自然红态。**

yaml `:795` 的断言「合并树 aria CHANGELOG 的 `grep -c '^## \['` 不少于第 3 步所记计数」括注理由是「防解冲突时丢掉对方发版小节」; 但第 5 步 (`:794`) 已写死「退出码非 0 (冲突) -> `merge --abort` ... 不在 master 上解冲突」。本任务内 `--no-ff` 无冲突合并的结果恒为并集, 该计数恒不小于基数 -> 在本任务内是恒绿检查。它真正可红的路径在第 4 步 fail-closed 之后: owner 确认后按 `ec72175` 先例在 feature 分支手工 `merge origin/master` 并解 CHANGELOG 冲突, 再从第 1 步重走本任务 — 那时若手工解冲突丢了对方小节, 第 6 步才抓得到。

R4 处置原则 3 要求「每条新检查须写出其自然红态在哪里出现」, 此条未写。改法: 把括注改为「防第 4 步 fail-closed 后 owner 确认的手工解冲突丢掉对方发版小节 (本任务内第 5 步已排除解冲突, 故该断言只在重走时可红)」。实测基数: 当前 `grep -c '^## \[' aria/CHANGELOG.md` = 138。

#### m4 [Minor] type=issue · category=documentation · scope=metadata.owner_gates · v4 引入: 是

**四处「停下上报」未进 owner_gates, 与 R3 跨簇一致性第 2 条「每条停下上报都能在 owner_gates 里找到对应项」不符。**

owner_gates 共 15 条 (实测)。缺失项: TASK-029 第 2 步 (工作树不干净 / 占位未清 -> 停下或上报) · TASK-029 第 3 步 (`merge --ff-only` 不能快进 -> 停下上报) · TASK-034 (发现同名 `v<vNEXT>` tag -> 回退两个子模块后停下上报) · TASK-032 开头 (本地 master 不能快进到 origin/master -> 停下上报)。tasks.md「外向动作与 owner 等待点」声明「单一来源 = owner_gates, 本文件不复述」, 所以只读该索引的 owner 会看不到这四个可能的停摆点。改法: 各补一行, 或在 owner_gates 顶部注明「仅列需要 owner 动作的点, 纯止损停摆见各任务」。

#### m5 [Minor] type=issue · category=documentation · scope=tasks.md `:31` 读前必看第 14 条 · v4 引入: 是

**第 14 条对 (l1) 的描述停在 v3 口径, 与同文件清单第 12 条、yaml authoring_rules 不同文。**

第 14 条写「(l1) 模块 docstring 与 `write_latest_md` 的 Returns 段各含 `degraded_reason`」—— 这对 v3 谓词 (`'degraded_reason' in ast.get_docstring(模块)`) 成立, 对 v4 谓词不成立 (v4 限定到「`Return dict schema:` 块 / `Returns:` 块, 各取标题到第一个空行」)。本席逐字比对 `2b9cb3e` 与 `edd256d` 的第 14 行, 本轮唯一改动是 (d)(e)(h) 的归属 (m17), (l1) 段未同步。照第 14 条落笔而把 `degraded_reason` 写在模块 docstring 顶部场景列表里, 正是矩阵里 `bad_l1_module_scenarios` 的红态。改法: 第 14 条 (l1) 补「各取标题到第一个空行的块」。

#### m6 [Minor] type=risk · category=testing · scope=(j4) 正则 · v4 引入: 是

**左边界 `[^0-9a-z]` 在 `grep -i` 下连大写字母一并排除, 与 authoring_rules「扫描面内任何语境都不用这些字样」的表述不严格一致。**

实测 (`printf ... | grep -niE '(^|[^0-9a-z])(four|4)[- ]levels?|四级|四层'`):

```
XFOUR levels        -> 不命中   (-i 把 [^0-9a-z] 一并折叠, X 被当作 x)
-FOUR levels        -> 命中
4 levels            -> 命中
the four-level key  -> 命中
14-level key        -> 不命中   (m9 的目标, 正确)
round-3 4th level   -> 不命中   (历史序数, 正确保留)
```

现实里层数词左边一般是空格 / 反引号 / 括号 / 星号, 影响面很窄, 故计 Minor。若要与措辞对齐, 把左边界写成 `(^|[^0-9A-Za-z])` 并保留 `-i`。

#### m7 [Minor] type=issue · category=implementation · scope=TASK-009 与验证脚本 target · v4 引入: 否 (v2 起)

**TASK-009 的「源码中不新增 `docs/handoff/` 字面量」与同批落地的验证脚本 target 自相矛盾, 且该约束无任何检查。**

脚本 `collector_docs` 的 `c` 项把 `_list_handoff_files` docstring 改成 `Returns each file's path relative to ``docs/handoff/`` so callers` —— 新增了一个 `docs/handoff/` 字面量。collector 现有 8 处该字面量 (`:3 :177 :243 :266 :298 :315 :375 :629`) 全在注释/docstring 里, 说明约束本意是「逻辑里不得硬编码路径, 要从 `_HANDOFF_TREE_PATH` 派生」, 但写成了对整个源文件的禁令。(c2) 只要求出现 `path relative to`, 不要求那个路径字面量, 所以谓词侧无冲突; 风险是执行者按字面理解后与 target 的示范打架。改法: 约束改写为「前缀剥离不得硬编码路径字面量, 一律从 `_HANDOFF_TREE_PATH` 派生 (docstring 里引用路径不受限)」。

#### m8 [Minor] type=risk · category=testing · scope=EXPECTED 矩阵覆盖 · v4 引入: 否

**19 条谓词里 10 条没有任何隔离状态, 其中 (c2) 的鉴别面明显偏松。**

矩阵的隔离能力集中在 7 条 (a2 / j1 / j2 / j3 / j4 / k / l1)。`a1 b c1 c2 f1 f2 i1 l2 l3` 只在三个全 FAIL 状态与 target 之间取值, `j5` 只在 `bad_partial` 里。具体地: (c2) 是 `grep -q 'path relative to' <collector 全文>` —— 把新契约句写进**模块** docstring 而不是 `_list_handoff_files` 的 docstring, (c1)(c2) 同样为真, 而 TASK-009 要的是函数自身的契约句。读前必看第 14 条已声明「模块 docstring 两块各归其位不入谓词, 由 4.2 核验」, 属有意为之, 故只作风险登记。若要补, 一个 `bad_c2_module_only` 坏态成本很低 (与「收口」建议合看, 见 `## 边际判断`)。

### 核对无误的部分 (不计 finding)

1. 验证脚本 `rc=0`; 18 态 x 19 谓词矩阵与 yaml `measured_2026_09_15_at_1cb3872_v4` **逐字节一致** (程序比对, 非目测)。
2. `--emit-json` 的 `states` / `expected` / `predicates` / `matrix` 四字段与 yaml 对应块**全部逐字节一致**; 其中 `predicates` 与 `sc11_baseline_predicates` 里 `(label)` 开头的 19 行完全相同 — m11 要的那个唯一机械核验点确实成立。
3. 六个退出码 (0/1/2/3/4/5) 逐条构造实跑, 语义与 docstring / yaml `:100` 描述一致; `finally` 清理实测生效 (运行后 `TMPDIR` 为空); `python3 -OO` 下行为与 stdout 与 `-B` 完全相同; 全文无 `assert`。
4. 归档门全勾预演与 TASK-032 写的预期**逐项一致** (complete=True / verdict=warn / 恰 3 条 unverified_claims / 三条理由与所指行一一对应); TASK-032 对「残留父目录 token 会让抽验恒过」的判断经 A-C 三态实证属实; `classify_artifact_claim` 的 `_ARTIFACT_PATH_TOKEN_RE` 只认含 `ab-results` / `ab-suite` 的 token, 所以 TASK-032 写的「也不出现其它含 ab-results 或 ab-suite 的已存在路径」是精确的, 同行的 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 不会误救。
5. 本轮新增的 5 个坏态都像真实坏情形: `bad_tuples_stale_para` (另起一段) / `bad_j2_tuple_stale_para` (另加 bullet) / `bad_l1_module_scenarios` (顶部场景列表改了、Return dict schema 块没改) / `bad_l1_neverraises` (Never raises 段写了、Returns 段没写) / `bad_j3_later_tiebreak` (后文多一行 `# Tie-break`); 两个 `alt_*` 守卫态 (换措辞 / `14-level`) 期望全 PASS 也实跑通过, 确实在防假红。
6. 35 任务结构、依赖图 (无环无悬挂)、工时与 agent 配额、27 parent 与 27 checkbox 双向全等。
7. 行号锚点与引文抽样近 40 处逐处实读全部命中 (含 `VERSION:24` 仍停在 v1.73.0 这一条 A.2 结论)。
8. 三条被引用的基线测试用例数 (23 / 5 / 19 / 24) 复跑全部吻合; `freeze_corpus.FIELDS` 存在且为 8 字段 (不含 rel_path), SC-2 的「按路径导入不重抄字面」可行。
9. `_common._run` 的 `errors="replace"` 使 `chr(0xFFFD) in rel` 成为有效判据; `-z` + NUL 切分的必要性 (`str.splitlines()` 会在 `\x0b` `\x0c` `\x85` ` ` 等处额外断行) 与计划一致。
10. YAML 引号转义全部正确round-trip: `grep -c '#<'` / `grep -c '^## \['` / `grep -n "^## \[1.70.0\]"` / TASK-026 的 `sys.path.insert(0, ''...'')` 解析后都是可直接执行的 shell 文本 (后者逐字复跑通过)。
11. PP3-M9 的程序化核对 (verification 提台账 => deliverables 含带标题注释的台账行) 35 个 TASK 零违规。
12. `.aria/config.json` 实读: 只有 post_spec / post_planning enabled, 与计划未安排 post_implementation / pre_merge 审计一致 (无 Rule #10 自豁免嫌疑)。

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical / 1 Major / 8 Minor。

判 PASS_WITH_WARNINGS 而非 FAIL: 计划没有会造成不可逆损害或违反不可协商规则的条款; 结构、行号、命令可执行性、退出码契约、归档门预期、两份谓词一致性这几类最容易出错的面, 本轮抽测**全部通过**, 且多处 (归档门三态、退出码六态、基线用例数) 是计划自己写死的预测被实测逐项确认。

判还有 1 个 Major: M1 是同一个缺陷类第三轮未被堵死 —— R3 已经认定「只判块内出现 rel_path」不够, v4 换成「判 `(parse_ok` 之后出现 rel_path」, 仍然是同一个量上挪边界。修法是三条谓词的单行替换 + 三个坏态, 本席已在 10 个状态上实跑验证过与现行谓词零回归, 属边界清楚、不新增流程面的编辑。

## Vote

**REVISE**

理由: M1 让 TASK-019 / TASK-020 / TASK-021 / TASK-029 的一组验收项可被「改了句子、没改元组」的实现骗过, 属严重度口径里的「可被像真实坏情形的坏实现骗过」。但返修面是可界定的: 三条谓词单行替换 (含 (l1) 的一处 `partition` 追加, m1) + 三到四个新坏态 + 由脚本重生成 yaml 三块 + 五条纯文字改动 (m2-m7)。不涉及任务拆分、依赖改动或新流程, 所以本席预期一轮即可收敛, 不建议因此扩大改动面。

## 边际判断

**是, 这套 18 态 x 19 谓词的矩阵已经越过它所保护对象的价值。**

三个可量化的理由:

1. **鉴别力高度集中**。逐格看, 真正被隔离出来的只有 7 条谓词 (a2 / j1 / j2 / j3 / j4 / k / l1); 另外 10 条 (a1 b c1 c2 f1 f2 i1 l2 l3, 加只在 `bad_partial` 里出现的 j5) 没有任何单独坏态。而且 (j4) 有 3 个只针对它的状态、(l1) 也有 3 个。也就是说: 342 个格子里, 承载新信息的是「7 条谓词 x 各自 1-3 个坏态」那一小块, 其余是为了填满矩形而算出来的。
2. **维护成本是 O(状态 x 谓词) 而收益是 O(谓词)**。EXPECTED 是手写的 18 x 19 定值表, 每加一个坏态要人工推 19 个格子; 本轮加 5 个态 = 95 个格子。R3 聚合已把「本轮修订自身引入的 Major 占比 > 1/2」记为拐点信号, 而本轮我找到的那条 Major 又恰恰长在上一轮的修订上 —— 矩阵越大, 每轮要重算的面越大, 出新错的面也越大。
3. **被保护对象的性质是文档同步**。19 条谓词全是 grep / AST-docstring 级的「文档有没有跟着改」检查, 行为正确性由 SC-1..SC-18 的真测试独立承担。用代码级的对抗严格度去守一组文档检查, 边际收益结构性偏低。

**建议的收口形态** (三条, 可分别取):

1. **把 EXPECTED 从「定值矩阵」改成「每态只声明期望 FAIL 的谓词集」**, 由脚本展开成矩阵再比对 —— 断言强度完全不变 (现在 `summarize()` 已经在用这个口径生成散文), 但每加一个坏态从「写 19 格」降到「写一行 `{'bad_x': {'j1'}}`」。矩阵仍由 `--emit-json` 输出并回填 yaml, 对外可见形态不变。这一条直接消掉「每轮重算全矩阵」的成本, 本席认为是性价比最高的一步。
2. **给状态设上限规则**: 同一条谓词的隔离态不超过 2 个, 除非新态验的是**另一种机制**而不是另一个落点。按此, (j4) 的 3 个态 (`bad_stale_synonym` / `bad_stale_header` / `bad_test_docstring_stale`) 验的是同一个正则在三个文件上的行为, 可并成 1 个「三处同时漏改」的态; (l1) 的 3 个态里 `bad_scenarios_missing` 与另两个是不同分支 (Scenarios vs 两个块), 保留 2 个即可。这样 18 态可降到约 12 态。
3. **按争议度分层**: 把从未被任何一轮审计质疑、且结构上难以被绕过的 11 条 (a1 b c1 c2 f1 f2 g i1 i2 l2 l3) 降级为「4.1 / 4.2 / 4.4 执笔后逐条实跑并贴输出」的清单项 (仍要求 base FAIL / target PASS 两态), 脚本只维护被反复攻击的 8 条 (a2 j1 j2 j3 j4 j5 k l1)。矩阵规模落到约 12 x 8, 同时把注意力留在真正出过问题的地方。

需要说清的一点: 收口**不等于放宽**。上面三条都不改任何一条谓词的判定强度, 也不减少 base 全 FAIL / target 全 PASS 这两条底线; 减的只是「为了把矩形填满而人工推导的格子数」。M1 那条修订应当先落, 再做收口 —— 否则会把一个已知可绕过的判据固化进更小的矩阵里。

## 轮次记录

- 本轮 (R4) 本席为新派席位, 未参与 R1-R3, 未读同轮其他席位报告。
- 本席对 R3 code-reviewer 席建议并已落地的 `j1x` / `j3x` / `j2x` / `l1x` 做了独立复核而非默认采信: 四条都按「自建像真实坏情形的坏实现」重测, `j1x` / `j3x` / `j2x` 三条未堵住同段/同行变体 (M1), `l1x` 未堵住标题行括注变体 (m1)。
- 与 R3 相比: R3 的 9 个 Major 簇中, 本席侧重相关的 PP3-M1 / M2 / M7 / M9 与全部 17 条 Minor 里的 m7-m14 逐条核到落地证据 (表见上), 其中 PP3-M7 与 m7 落地但不充分, 其余落地充分。
- 只读约束遵守情况: 未 `git add` / `commit` / `stash` / `checkout` / `reset` / `push`; 未开 issue / 回帖 / 调 Forgejo 写接口; 未派子代理; 未跑 `scan.py` / `run_tests.py` / `phase1_gate.py` / `release_gate.py`; 仓内除本报告外零写入 (所有副本与坏态都在 scratchpad 的临时目录, 已删除); 单元测试只跑了 4 个 unittest 模块 (allowed form)。
