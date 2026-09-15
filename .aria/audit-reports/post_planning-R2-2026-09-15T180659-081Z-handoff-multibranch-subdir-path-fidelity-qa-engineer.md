---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T18:47:50.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

### 已实读文件

- `openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md`（v2 全文 145 行）
- `openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml`（v2 全文 784 行，分两段 offset 读完）
- `openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py`（全文 123 行，新文件）
- `.aria/audit-reports/post_planning-R1-...-aggregated.md`（R1 聚合报告全文）与本席 R1 报告 `...-qa-engineer.md`（全文，用于比对自己 R1 提出的 Finding 是否被正确处置）
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md`（全文 116 行）
- `proposal.md`（v7，252KB；用 `sed -n` / python 按行切片读了 Tasks §364-411 全段、Success Criteria 表 §411-435（含 SC-1/3/4/5/8/9/14/17/18 逐条反事实原句与 SC-18 基线态分析）、SC-15 细则、rule6_note 段）
- `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`（`grep -n` 定位「场景 1」§200-228 全段）
- v1→v2 diff：`git diff 07e0a6e 0f50239 -- openspec/changes/handoff-multibranch-subdir-path-fidelity/`（含针对 TASK-019/TASK-020/TASK-021 等具体任务块的定向 diff）

### 已跑命令（只读；临时实验建在 `/tmp/qa-r2-*`，核验后已 `rm -rf` 清空；未 `git add`/commit/push，未跑 `phase1_gate.py`/`release_gate.py`/`run_tests.py`）

1. `git submodule status` + `git -C aria rev-parse HEAD` → 确认 aria = `1cb3872`（v1.73.3），与文档头部一致。
2. `python3 -B openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py`（仓库根跑，脚本自建临时目录并自动 `shutil.rmtree`）→ 输出 19×5 矩阵，**与 `detailed-tasks.yaml` `metadata.sc11_predicate_validation.measured_2026_09_15_at_1cb3872` 逐行 diff = 0**（python 脚本行级比对，20 行含表头全部相同）；脚本自身 `sys.exit`：19 条谓词的 base/target/bad_codeonly 三态全部满足脚本内建断言，退出码 0。
3. `/tmp` 副本实验：对 `_render_pointer` / `_render_pointer_unavailable` 的 docstring 写一版语义正确但**刻意不含** `target_in_subdir`/`subdir`/`子目录` 三个关键词之一的英文改写（如 "does not sit directly beneath the handoff root"），单独跑谓词 (k) 的 AST 检查 → **两个函数均判 False，谓词 (k) 判假红**（详见 Finding 2）。
4. `/tmp` 副本实验：单独重放 `p1_docs()` 的 `rep()` 调用于真实 `phase-1-collectors.md`，打印替换后的 `Return dict` 整行 → 发现 `content_lines: int` 在结果串中出现两次（详见 Finding 3）。
5. `git for-each-ref --format="%(refname)" refs/remotes/origin/ | wc -l` + 对 13 个 ref 逐个 `git ls-tree -r --name-only <ref> -- docs/handoff` 汇总 grep 子目录形态与引号前缀 → **13 个 ref、子目录命中 0、引号前缀命中 0**，与 TASK-002 verification 第 3 条声称的「A.2 实测 13 个 ref：子目录 0、带引号 0」逐字吻合。
6. `grep -n "four-level\|four levels\|FOUR levels"` 分别在真实 `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py`（命中 `:355`/`:368`/`:429`）与 `references/state-snapshot-schema.md`（命中 `:1124`/`:1134`，非表格行）跑 → 与 TASK-019/TASK-020 的行号引用及 `metadata.baseline_rebase.shifts` 逐字吻合；并确认 `sc11-predicate-validation.py` 的 `rep()` 调用（j1/j3/j4a/j5a/j5b/j5c/j2/j4b）覆盖了这全部 5 处真实命中，脚本运行未触发任何 `assert n>=1` 失败（说明模拟改动的锚点字符串在真实文件里确实唯一存在）。
7. `grep -n '^## \[1.70.0\]'` 等在 `aria/CHANGELOG.md` 上核对 `metadata.baseline_rebase.shifts.changelog_md` 声称的 `:200`/`:202`/`:209`/`:215` → 逐字吻合；`git -C aria diff --stat f314785 1cb3872 -- CHANGELOG.md` → `91 insertions(+)`，与 `baseline_rebase.result` 的「CHANGELOG.md (+91)」吻合。
8. `python3 -B -c` 对 tasks.md / detailed-tasks.yaml 扫描字面 `�` 与转义形式 `chr(0xFFFD)` 计数 → 两文件字面 U+FFFD 均为 0，转义形式分别为 1/3，与 R1 minor m6 的「接受，改为转义文本」处置吻合。
9. `cd aria/skills/state-scanner/tests && python3 -B -m unittest test_handoff_multibranch_collision_dedupe test_track_board_advisories test_p1_layer_h -v` → **Ran 52 tests … OK**（23+5+24），与 TASK-016/TASK-013 verification 的具体数字吻合。
10. `pytest -q tests/test_collision.py`（state-scanner）→ **28 passed**；`pytest -q tests/`（phase-d-closer）→ **11 passed**，与「两腿」口径的既有数字吻合。
11. `grep -c` / `grep -oE` 对 tasks.md 的 checkbox 与 yaml 的 `- id: TASK-` / `parent:` 做机械计数 → tasks.md **26** 个 checkbox（v1 为 25，v2 新增 2.7）；yaml **34** 个 TASK（v1 为 32，v2 新增 TASK-033/TASK-034）；26 个 distinct parent 与 26 个 checkbox 一一对应，无孤儿。
12. `git diff -U2 07e0a6e 0f50239 -- detailed-tasks.yaml` 定向核对 TASK-019/TASK-020/TASK-021/TASK-026/baseline_rebase.shifts 各处 hunk，确认 R1 处置逐条真实写入（而非仅口头声称）。

以上核验的具体数字、行号、diffstat、谓词矩阵**全部与文档自身声称一致**，未发现「数字/行号/转述错误」类问题。下面聚焦结构性与新引入的问题。

---

### R1 处置落地核验（本席聚焦 6 项 + 其余 Major 簇简表）

| 处置编号 | 落地与否 | 证据 |
|---|---|---|
| **PP1-M2**（SC-11 谓词定位 + 三态验证，实测矩阵） | ✅ 落地且正确 | `sc11-predicate-validation.py` 新文件；`detailed-tasks.yaml:84-109` 矩阵块；本席重跑脚本，输出与记录逐行 diff=0；19 条谓词全部定位到具体行区间/AST 节点，不再是整文件 grep |
| **PP1-M3**（反事实证据来源 = 基线回退形态 + 三步法） | ✅ 落地且论证严谨 | `detailed-tasks.yaml:393-408`（TASK-033 收口提交节点）+ TASK-015~018 `dependencies: [TASK-033]`；TASK-007 verification `:262` 反事实标注；逐条对照 proposal.md 原文反事实句（SC-1 `:415`「回退枚举层为basename」/ SC-3 `:417`「去掉-z」/ SC-4 `:418`「回退为basename」/ SC-5 `:419`「保留旧降级分支」/ SC-8 `:422`「回退为basename-only枚举」/ SC-17 `:432`「回退枚举层为basename」）与「基线即该反事实」的等价性逐条成立（基线本就是「未改枚举层/未加-z/未改判据」的状态）；SC-14 的中间态反事实（TASK-011 `:340`）与 proposal `:429`「只改正常路径」逐字对应，且带自纠错兜底（若中间态意外已转绿，改用三步法在副本上补测） |
| **PP1-M9**（组5「5.3→5.5」执行序消歧，本席 R1 提出） | ✅ 落地 | `tasks.md:108` 标题改为「5.3 与 5.5 互不依赖、均先于 5.1」；`TASK-025`/`TASK-026` 互无依赖边 |
| **Minor m3**（hermetic 仓沿用 `update-ref` 手法，本席 R1 提出） | ✅ 落地 | `detailed-tasks.yaml:182`（TASK-003）显式点名 `test_handoff_multibranch_collision_dedupe.py` 的 `_git(tmp, "update-ref", ...)` 范式，并与 TASK-022 的 bare origin 要求对比 |
| **Minor m9**（平铺基线 JSON 防重生成守卫） | ✅ 落地 | `detailed-tasks.yaml:539`（TASK-021）新增 `git -C aria log --format=%H -- <平铺基线JSON>` 只有一次提交 + diff 为空的机械核验；`hard_constraints:115` 同步收录 |
| **Minor m13**（TASK-002 核验范围补 ref 集） | ✅ 落地 | `detailed-tasks.yaml:165`（TASK-002 命令 3）新增对全部 `refs/remotes/origin/*` 逐个 `ls-tree`；本席独立重跑，13 ref / 子目录 0 / 引号 0，与声称吻合 |
| PP1-M1（改键支键层级描述整类改写） | ✅ 落地 | `TASK-020` deliverables 新增 5 处（`:58-61`/`:93-96`/`:355`/`:490-492`/`:716-717`，经 `git diff -U2` 确认为净新增）；`TASK-019` 新增 `:1134` Renderer parity 句；新增谓词 (j4)(j5) 且真实文件命中位置与脚本 `rep()` 锚点逐一对应 |
| PP1-M4（回归/AB 依赖补 023/024） | ✅ 落地 | `TASK-021:531` deps 含 023/024；`TASK-026:626` deps 含 023 |
| PP1-M5（归档门只读预演 + Step 7 授权清单） | ✅ 落地 | `TASK-032:775-776` |
| PP1-M6（`handoff-mechanics.md` 手改路径缺口并入 issue） | ✅ 落地 | `TASK-025:614` 第 (g) 条 |
| PP1-M7（TASK-026 整段重写：通过判据/止损/运维手册三步） | ✅ 落地且与 SOT 核对一致 | `TASK-026:630-639`；与 `AB_TEST_OPERATIONS.md:226-228`「场景1」三步逐句对应（启动/核验 push_skipped/事后 fetch 强制对齐），并额外补了运行前 ls-remote 基线比对（回应 R1 code-reviewer「核验量错对象」） |
| PP1-M8（AI 流程判断清单入 tasks.md + Phase D 承接） | ✅ 落地 | `tasks.md:34-49`；`TASK-032:780` |
| PP1-M10（writer 契约面统一归 TASK-013） | ✅ 落地 | `git diff` 确认 TASK-020 deliverables 已删除 `latest_md_writer.py` 一行 |
| PP1-M11（TASK-024 补依赖 TASK-013） | ✅ 落地 | `TASK-024:589` deps 含 TASK-013 |
| PP1-M12（台账唯一执笔 + 固定骨架） | ✅ 落地 | `metadata.verification_ledger:21-24`；`hard_constraints:118` |
| PP1-M13（偏移表补 CHANGELOG.md） | ✅ 落地且精度提升 | `metadata.baseline_rebase.shifts.changelog_md:50`；独立 `grep`/`git diff --stat` 复核逐字吻合；且本次连带修正了 `:1062`「原位改写」vs 旧版「插入点」的不精确描述 |

R1 的 13 个 Major 簇与本席直接负责的 3 项 Minor，**全部真实落地且核验正确**，未发现「声称已改、实未改」或「改法本身有误」的情形。

---

### Finding 1 — [Major] type=issue category=testing scope=`sc11-predicate-validation.py:118-123` / `detailed-tasks.yaml:148`（TASK-001）／v2 新引入

**证据**：`sc11-predicate-validation.py` 的 docstring（`:2`）自称「三态验证」，但脚本实际在临时目录构造 **5** 种状态（`:8-13`：base / target / bad_codeonly / bad_changelog_only / bad_partial），并把全部 5 态打印到 stdout（`:117-120`）。但决定脚本退出码的最后两行：

```python
bad = [k for k in PRED if not (res["base"][k] == "FAIL" and res["target"][k] == "PASS" and res["bad_codeonly"][k] == "FAIL")]
sys.exit(1 if bad else 0)
```

只校验 `base`/`target`/`bad_codeonly` **三态**，完全不校验 `bad_changelog_only` 与 `bad_partial` 是否符合 `detailed-tasks.yaml:87`（`metadata.sc11_predicate_validation.expected`）文档化的期望值（「`bad_changelog_only` 除 (g) 外全 FAIL」「`bad_partial` 中 (a2)(i2)(j4)(j5)(k)(l1) 为 FAIL, 其余 PASS」）。这两条恰恰是 PP1-M2 要解决的核心问题——「谓词能否识别『看似做了但漏了一半』的坏实现」——的直接检验对象。

`detailed-tasks.yaml:148`（TASK-001 verification）写明：「若 B.1 基线与 1cb3872 在谓词读取的 5 个文件上有 diff, 先重跑 `sc11-predicate-validation.py`, 三态不符同样先修谓词」。Phase A.2（本轮）到 Phase B 实际执行之间存在时间差，`state-scanner` 基线漂移是文档自己承认的常态场景（`metadata.baseline_rebase` 整节就是本轮对 A.2 时点漂移的重新核验）。若届时执行者（很可能是在做别的实现任务、时间/token 都吃紧的 agent）重跑本脚本并只看 `echo $?`（这是最自然的机械化复核方式，脚本本身也以 `sys.exit` 形式暴露了这个用法），**exit code 0 无法保证 `bad_partial`/`bad_changelog_only` 两态仍符合预期**——若基线漂移恰好使某条谓词对「漏改一半」类坏实现失去鉴别力（比如某处 four-level 措辞被上游其它 spec 顺手改写、或 Change history 表格式变化），脚本仍会退出 0，制造一次静默的假绿。

**照计划执行会出的错**：Phase B 若触发 TASK-001 的「重跑」分支，执行者靠退出码判断「三态复核通过」，实际只验证了最弱的正/负控制（“完全没改文档”会被抓到），却可能放过「表面正确、实际漏改」的坏实现，与 PP1-M2 本欲修复的问题同构复发一次。

**建议改法**：把 `bad` 的判定表达式扩展为对全部 5 态、19 条谓词按 `expected` 字段逐项比对（`bad_changelog_only[k]` 除 `g` 外应为 `FAIL`；`bad_partial[k]` 按 `{a2,i2,j4,j5,k,l1}` 集合分别判 FAIL/PASS），退出码覆盖全部 5 态；或至少在 `TASK-001` verification 里明确写「重跑后须目视比对全部 5 列与 `expected` 字段，不得只看退出码」，消除「脚本自称三态、退出码只查三态、文档记录五态」三者不一致带来的操作歧义。

---

### Finding 2 — [Minor] type=risk category=testing scope=`sc11-predicate-validation.py:106`（谓词 k）／`detailed-tasks.yaml:109`（authoring_rules）／v2 新引入

**证据**：谓词 (k) 要求 `_render_pointer` 与 `_render_pointer_unavailable` 的 docstring 含 `target_in_subdir`/`subdir`/`子目录` 三个拼写之一（`sc11-predicate-validation.py:106`）。本席在 `/tmp` 副本上把两处 docstring 改写为语义完全正确但刻意回避这三个拼写的英文句子（如 "...or when the tracked file does not sit directly beneath the handoff root"），单独跑该 AST 检查 → **两处均判 False，谓词判假红**（真实复现，非推测）。

但该风险有两层实质性缓解，均已在 v2 文档内落地：(1) `detailed-tasks.yaml:109`（`authoring_rules`）明文写「(k) 接受 target_in_subdir / subdir / 子目录 三种写法之一」；(2) `TASK-013` verification（`:373`）本身已指示执行者「两处 docstring 写明第二个降级原因 (`target_in_subdir`)」，即任务书直接给出了应写入的字面术语。两者都先于实际编码环节把约束显式交代给执行者，一个按计划走流程的执行者不太会写出本席刻意构造的规避式措辞。

**照计划执行会出的错**：只有当 TASK-013 的执笔者跳过 `authoring_rules` 与自身 verification 里的字面提示、纯自然语言复述降级原因时，才会在 4.3 回归（TASK-021 要求「19 条谓词全部为真」）时意外撞上这条假红，需要回头改措辞——属于「浪费一轮返工」而非「缺陷被放过」，因为红态会被立即看见并倒查修正，不会静默漏检。

**建议改法**：谓词 (k) 的可接受关键词集合可以再放宽一档（例如再加 "not directly under"/"nested" 之类语义等价短语），或者不改脚本，只需在 `TASK-013` verification 里把 `target_in_subdir` 一词加反引号/加粗强调其为「必须逐字出现」的字面要求，进一步降低误解空间（当前写法「补第二个降级原因 (target_in_subdir)」容易被读成「括注只是给执行者的内部提示，不要求出现在最终文本里」）。

---

### Finding 3 — [Minor] type=issue category=implementation scope=`sc11-predicate-validation.py:69`（`p1_docs`）／v2 新引入

**证据**：`p1_docs()` 对 `phase-1-collectors.md` 的替换写成 `rep(r, P, 'content_lines: in', 'content_lines: int, degraded_reason: ..., content_lines: in')`——把待替换的锚点串 `'content_lines: in'` **原样重复插入**在替换文本末尾。本席在 `/tmp` 副本上单独重放这一调用并打印结果行，实测产出：

```
Return dict: `{action: "pointer"|"banner"|"skipped", path: str, content_lines: int, degraded_reason: None|"missing_filename"|"target_in_subdir", content_lines: int}`.
```

`content_lines: int` 在同一行出现两次，是一处查找替换时的复制粘贴残留（把原串 `content_lines: in` 复制到新串末尾时忘记只需保留到不含 `in` 前缀，导致原文件里紧跟的 `t}` 与新插入的完整 `int}` 重复）。

**照计划执行会出的错**：该重复只存在于 `sc11-predicate-validation.py` 自建的 `/tmp` 模拟态里，不进入任何真实交付物——`TASK-020` 自己的 verification（`phase-1-collectors.md:102 Return dict 补 degraded_reason`）并未照抄这段脚本文本，真实执笔者会正常写出无重复的 dict 字面量。谓词 `l2` 只做 `grep 'Return dict' | grep -q degraded_reason` 子串匹配，重复文本不影响其 PASS/FAIL 判定，矩阵数值不受影响。纯属脚本自身的可读性瑕疵，唯一实际风险是将来有人误把这段模拟文本当范例复制进真实文档。

**建议改法**：`p1_docs()` 改成对完整目标串一次性替换（如 `rep(r, P, 'content_lines: int}', 'content_lines: int, degraded_reason: None|"missing_filename"|"target_in_subdir"}')`），消除重复片段。

---

## Verdict

0 Critical / 1 Major / 2 Minor → **PASS_WITH_WARNINGS**（1 Major 全部由 v2 新引入的 `sc11-predicate-validation.py` 自身贡献；R1 的 13 个 Major 簇与本席负责的 3 项 Minor 全部核验为正确落地，未见新的回归）。

## Vote

**REVISE**（存在 1 Major：`sc11-predicate-validation.py` 的退出码语义窄于其自身文档化的「五态」期望，Phase B 若依赖重跑该脚本的退出码做复核会有假绿风险，建议在进入 Phase B 前把 `bad` 判定扩展到全部 5 态，或至少在 `TASK-001` verification 明确「重跑须目视核对五态，不得只看退出码」）

## 轮次记录

Round 2 (qa-engineer, convergence): REVISE — 0C/1M/2m（v2 引入 Major：1）；R1 的 13 个 Major 簇（含本席 R1 提出的 PP1-M9）与本席负责的 3 项 Minor（m3/m9/m13）逐条核验**全部真实落地且改法正确**（含独立重跑 `sc11-predicate-validation.py` 得到与 yaml 记录逐行 diff=0 的矩阵、独立复现 13-ref/0-子目录/0-引号核验、独立复核 CHANGELOG.md 行号与 +91 diffstat）；6 条基线-即-反事实（SC-1/3/4/5/8/17）的论证逐条对照 proposal 原文反事实句成立。新发现 1 Major 全部集中在 v2 新增的 `sc11-predicate-validation.py` 自身：其退出码只校验 5 态中的 3 态（base/target/bad_codeonly），未覆盖 `bad_changelog_only`/`bad_partial`，与 `TASK-001` 「重跑该脚本, 三态不符先修谓词」的复核路径存在假绿风险；另 2 项 Minor（谓词 (k) 的窄关键词匹配经 `/tmp` 实测确有假红可能但被 `authoring_rules` 与 `TASK-013` 自身文本双重充分缓解；`p1_docs()` 存在纯模拟态内的文本重复瑕疵，不影响矩阵正确性）。
