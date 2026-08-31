---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-31T13:56:02.572Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml (+ linked-issue-field-availability + sibling-spec-probe)
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 1
minor_count: 5
r2_disposition: {closed: 2, partial: 1, not_addressed: 0}
introduced_by_fix: 3
---

# post_planning R3 — A4 code-reviewer (机械一致性镜头, combined-mode 三份, R2 清账后版本; 本次为 API 限额中断后的重跑)

> 工作树: 主仓 HEAD c120f9e / aria d69091d, 2026-08-31 13:40–13:55 UTC。六份被审文件 sha256 见「实测记录 [0]」(审前) 与 [9] (审后, 逐行一致); 本席未改任何被审文件, 全部脚本跑在 scratchpad `r3a4/`, 坏输入跑在 scratchpad 副本 (`r3a4/adv/`, 只改脚本里的路径常量)。R2 → R3 六份的变化: linked tasks.md 0 hunk; linked yaml 6 hunk; sibling tasks.md 7 hunk; sibling yaml 3 hunk; a1 tasks.md 7 hunk; a1 yaml 8 hunk (+21 行 TASK-040) — 逐 hunk 见 [8]。带圈数字在引用被审文本时一律改写为 (n)。

## 摘要

R1 八项机械检查在三份终版 (25 / 18 / **40** = 83 任务) 全部重跑 [1][1b][5]: `yaml.safe_load` 与归档门 `parse_detailed_tasks` 三份 parse_ok, status 集合 = {pending}; 必需字段 12 项零缺席; `estimated_hours` 三份全为 `"a-b"` 串且逐任务求和 = metadata (50-86 / 55-87 / **97-158**, a1 = 94-153 + TASK-040 3-5); 依赖悬空 / 自依赖 / 环 = 0, 后向边只剩 R1 已裁定的 9 条 RED 边; 覆盖表 (SC, TASK) 28 / 46 / 55 对在 verification 层零缺, yaml 无表外 SC (linked 的 `SC-19` 是限定了的跨 Spec 引用, R2 已证伪); deliverables 实存性与 R2 同 (差异只在 TASK-040 新增 `aria` gitlink 作 deliverable — 本席口径: gitlink「实存」= index 条目 mode 160000 + 工作树目录 + `git submodule status` 可解析三者同时成立, 而非 `os.path.exists` 单独判; 三者均成立 [4]); agent 集合 = roster, linked / sibling 的 summary 与 agent_allocation 计数与实况相等。**parent 1:1: 集合三份相等; 序列 linked / sibling 相等, a1 自 R2 起不再相等** — TASK-040 块物理插在 TASK-037 与 TASK-038 之间 (yaml 尾 4 = 037, 040, 038, 039), 见 finding 09795e71。

R2 本席三条 finding: **2 closed + 1 partial** (逐条见闭合表)。三份「机械核验」贴出脚本从 tasks.md 逐字抽出原样执行, 全部 exit 0 且 stdout 与贴出输出**逐行相等** (30 / 44 / 28 行, 0 diff) [2]; 探针脚本无 `\\d` 转义残留, (e) 不再恒空 (坏输入 v2 → `RESULT: FAIL (e)` 10 对, exit 1) [6b]; 探针 `execution_order` 全部 `←` 箭头集合 ⊆ 该任务 `dependencies`, `TASK-001 ‖ TASK-002` 互不在对方传递 deps, `phase_b1_preconditions` 两条声称的上游边与实况集合相等 [3]; 母 (d) 55 对 / [a] 38 对 20 文件与亲跑一致; 母 TASK-032 / 033 / 035 已补 `ARIA_COORDINATION_NO_PUSH=1` 字面, **TASK-034 仍只靠「运行前置 / 核验 / 清理三条同 TASK-031」引用, 两字面零命中** ⇒ 9db42f0a (3) partial [5]。

残留 grep [6]: `未自行加边` / `13 项` 三份零命中; `1.68.0` / `1.67.3` / `README.zh-CN` / `est_hours:` / `parallelizable` 的命中**全部**是「不写 X / 曾同写 X / 已改 X」留痕句或脚本正文 (`parallelizable` 是 linked 脚本 (d) 要拒绝的字样), 两份 yaml 里前四项零命中、`README.zh-CN` 仅 a1 yaml TASK-038 notes 留痕 1 处; `<vNEXT>` 六份均在 (3 / 4 / 5 / 5 / 5 / 11 行)。

本轮 **0 critical / 1 major / 5 minor**。major (1a45ef41, **残留**, 由 TASK-040 试派生浮出): 母 Spec 发布链 TASK-037 (版本 bump) → TASK-040 (本地 merge + 双推 + tag) → TASK-038 (gitlink bump) **不 (传递) 依赖 TASK-009** (2.6, SC-23 / SC-14(a) 回归守卫, 覆盖表里 SC-14(a) 的唯一落点; `aria/` 侧 30 个写任务里唯一的漏网者; 直接依赖者 = 空) — 依图可在 2.6 未落盘时完成 merge / tag / bump; TASK-037 的 deps 自 R1 清账起未变, 故判残留而非 fix 引入。5 minor 里 3 条由 R2 fix 引入 (a1 yaml 块序 09795e71 / a1 tasks.md 三处陈旧句 64cf8dd9 / linked 5.5 与 TASK-024 title 停在 12 点而 verification 已改 14 点 e9ffaefe), 1 条 R2 partial (TASK-034 字面 199aa25c), 1 条 R1 追记残留 (探针 tasks.md :25 组间门漏 TASK-004 边 10e7cea4)。**introduced_by_fix = 3 / 6** (恰在 memory `marginal-return-negative` 的 1/2 拐点上, 未超)。

勘正本席 R2 一处数字: 9db42f0a (2) 写「实为 19 行、2 行标只读」, 实为 **16 行 / 2 行只读** (14 写入 + phase1_gate.py / release_gate.py 只读) [7]; 母 :265「16 条」数字对, 只有「未标只读」半句陈旧 (memory `critique-repeats-error`: 指别人数字陈旧时自己也数错了)。

## R2 finding 逐条闭合表 (本席 R2 3 条, 程序化判)

| R2 id | 严重度 | 判定 | 证据 (实测记录编号) |
|-------|--------|------|---------------------|
| 4a669876 | major | **closed** | [2] 探针贴出脚本 92 行逐字抽出: `double_backslash=False`, 原样亲跑 exit 0, stdout 44 行与 tasks.md :261-304 贴文逐行相等 (0 diff); (e) 行输出 `parallel line ['TASK-001', 'TASK-002', 'TASK-003']: same-file pairs = none` (非空); [6b] 坏输入 v2 (第 3 行改回「[并行, RED]」) ⇒ `RESULT: FAIL (e) [10 对]` exit 1 — 拒绝能力成立。处方里的「(e) 无并行行时打印 0 parallel lines」未采, 当前有并行行故不可见性不复现, 不计 |
| ea33f282 | major | **closed** | [3] `execution_order[0]` 现为 `TASK-001 ‖ TASK-002 可并行 (不同文件); TASK-003 ← 002 (…)`, `[1]` 为 `TASK-004 ← 001, 002, 003 (…)`; 全部 17 段箭头集合 ⊆ deps (0 MISMATCH, 且 deps 不多于箭头); 并列组 001 ‖ 002 互不在对方传递 deps; `phase_b1_preconditions[1]` 上游边声称 {004, 015, 016, 017} = 实际直接含 TASK-003 的任务集合; tasks.md :309 已知限尾句含「主控已追记加边」, `未自行加边` 零命中 [6]。处方第 4 项「加 (f) 有边却标并行检查」未采 — 观察 1 记其结构盲区, 因当前文件正确不计 finding。**处方外**同形残留: tasks.md :25 组间门的 TASK-003 子句仍只列 015 / 016 / 017 ⇒ 新 minor 10e7cea4 |
| 9db42f0a | minor | **partial** | (1) closed: 贴出脚本 (d) 已展开 `TASK-013/014` 缩写 (tasks.md :395-397), 亲跑 `[d] 覆盖表 (SC, TASK) 对 55` 与贴文一致 [2]; (2) closed 半: 贴文 `[a] 38 对 (共写文件 20 个)` / `phase1_gate.py: TASK-014 -> 015 -> 016` 与亲跑一致 [2], 但处方点名的「出入 #5」:265 一句未改, 仍写「TASK-003 的 16 条 deliverable 未标只读」而实况 2 条已标 (计入 64cf8dd9); (3) **partial**: 032 / 033 / 035 各补一条「运行前置 … `ARIA_COORDINATION_NO_PUSH=1 claude …`」(R2→R3 diff +3 行 [8]), **TASK-034 未补**, 两字面零命中 [5] (计入 199aa25c) |

## Findings

| id | severity | 来源 | category | scope | type | 描述 + 证据 + 处方 |
|----|----------|------|----------|-------|------|-------------------|
| 1a45ef41 | **major** | **残留** (TASK-037 deps R1 起未变; TASK-040 试派生浮出) | implementation | openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml#TASK-037 | issue | **发布链 TASK-037 → TASK-040 → TASK-038 不 (传递) 依赖 TASK-009, 图允许在 2.6 未落盘时 merge / tag / bump。** 证据 [4]: `TASK-037.dependencies` = 011–023 + 025–035 (不含 004–010, 作者显然假定第 2 组经实现任务传递到达); `TASK-040.dependencies = [TASK-037]`, `TASK-038 = [TASK-037, TASK-040]`; 全部 deliverables 以 `aria/` 起首的 30 个任务里, 不在 anc(TASK-040) 的**只有 TASK-009**; TASK-009 的直接依赖者 = `[]` (004→011, 005→006/012, 006→012, 007→008/013, 008→009/014/015, 010→016 都有下游, 唯独 009 是汇点); TASK-009 = 「SC-23 / SC-14(a) 回归守卫 (CLI 全链路, baseline 即绿) + SC-2 ↔ SC-23 相容性断言」, deliverable `aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py` (aria 子模块内), 覆盖表里 **SC-14(a) 的唯一落点**。为什么重要: tasks.md :26 逐字「全部顺序约束已编码进 detailed-tasks.yaml `dependencies` (非散文)」, 图即契约 (v2.0 Layer 2 无人复议时尤其如此); 依图 TASK-037 (5 文件版本 bump) → TASK-040 (`merge --no-ff` + 双推 + `tag v<vNEXT>`) → TASK-038 (gitlink bump 到「post-merge master SHA」) 可在 TASK-009 未落盘时全部 done ⇒ 要么 tag / gitlink 不含 SC-14(a) 守卫, 要么 TASK-009 之后 master 再前进一次, 使刚 bump 的 gitlink 落后 master (第二次 merge / bump 无任务宿主, 与 TASK-040 「两 remote 一致后才 bump」的时序承诺也被绕过)。与 R1 bd55ab9c 同维度 (发布 / 顺序边), 血 radius 小一档 (一条守卫测试) ⇒ major 非 critical。同类只此一个: 其余「baseline 即绿」守卫 (TASK-006 SC-15 经 TASK-012、TASK-007 经 008/013) 都有下游。处方: `TASK-037.dependencies` 加 `TASK-009` (一 token; 或加到 TASK-040); 顺手在贴出脚本加 (f)「anc(TASK-040) ⊇ 全部 deliverables 以 `aria/` 起首的任务」并在坏输入 (删该边) 上验红 — 现有 (c') 只查「向上可达 TASK-001/003」, 对「向下可达发布链」这一方向免疫 (memory `invariant-dimension`) |
| 09795e71 | minor | **fix 引入** (R2-4 TASK-040 插入) | implementation | openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml#TASK-040 | issue | **TASK-040 块插在 TASK-037 与 TASK-038 之间 (:956; 038 :977, 039 :1003), yaml 任务序不再单调, `parent` 序列与 tasks.md checkbox 序列不再相等。** 证据 [1][1b]: chk1 `parent 1:1: seq_equal=False set_equal=True`, 首个不等位 index 37 (yaml 8.4 vs md 8.2); yaml 尾 4 ids = 037, 040, 038, 039; `id 单调递增=False`。tasks.md 侧 8.4 正确追加在末尾 (:92), 编号纪律「新增只追加」在 yaml 侧没有对称执行; 贴出的母脚本 `[+]` 只断言 `parent ⊆ tasks.md 编号` (集合), 结构上看不见此项, 而 R2 本席与探针贴出脚本都以**序列**相等作健康证据。影响: 归档门 `parse_detailed_tasks` 不看序, 不致失败; 但读者按块序读 yaml 会在 8.1 之后看到 8.4 再回到 8.2, 与 tasks.md / execution 叙述打架。处方: 把 TASK-040 块整体移到 TASK-039 之后 (纯移动, 0 内容改动), 或在母脚本 `[+]` 改为序列相等断言并声明「块序 = tasks.md 序」为不变量 |
| 64cf8dd9 | minor | **fix 引入** ×2 (:232 / :455, TASK-040 后未扫) + R2 partial ×1 (:265) | documentation | openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md#L232,L265,L455 | issue | **母 tasks.md 三处陈旧句。** [7] :232 Notes「…覆盖全部 **39** 任务」与 :455「`parse_detailed_tasks` ⇒ `parse_ok=True`, **39** tasks」— TASK-040 后实为 40 (yaml `total_tasks: 40`, 贴文 `[+] total_tasks=40` 已改, 这两句没扫到, memory `fix-the-class`); :265 出入 #5「TASK-003 (锚点核对) 的 16 条 deliverable **未标只读**」— 实况 16 条里 `phase1_gate.py` / `release_gate.py` 2 条已标「只读核验」(贴文 [a] 因此从 40 对降到 38 对, 该句是本席 R2 9db42f0a (2) 处方点名要改的一句, 未改)。处方: 39 → 40 两处; :265 改为「16 条里 2 条 (phase1_gate.py / release_gate.py) 标只读, 其余 14 条计为上游写入方」 |
| 199aa25c | minor | **R2 partial** (9db42f0a (3) 四块补三) | implementation | openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml#TASK-034 | issue | **TASK-034 块内 `--no-push` / `ARIA_COORDINATION_NO_PUSH` 两字面零命中, 而 tasks.md :164 映射行仍写 (001, 031–035)。** [5] 032 / 033 / 035 各已补「运行前置 (Rule #7 射程 + R1 C5): 会话以 `ARIA_COORDINATION_NO_PUSH=1 claude …` 启动 (AB_TEST_OPERATIONS.md:222-228), transcript 核验 `push_skipped: true`」; 034 的 verification[0] 逐字 = 「运行前置 / 核验 / 清理三条同 TASK-031; phase-d-closer 的 release_gate 输出亦须 push_skipped: true」— 语义经引用覆盖 (TASK-031 含字面), 但 (i) 三兄弟块已改成自含字面, 034 成了唯一靠引用的 (同形不同写法, R2 三席 fix 又各修一处的形状); (ii) 034 是唯一直调 `release_gate.py --sweep-stale/--gc` 会改写真实 claim 的套件 (其 deliverables 注释自述), 恰是最不该靠转引的那块。处方: 034 verification[0] 前半改为与 032/033/035 同款字面句 (复制一行) |
| e9ffaefe | minor | **fix 引入** (R1 C2 补 CLAUDE.md deliverable 未扫 title / tasks.md; R2 A1 把 verification 12 → 14 点后成显性矛盾) | documentation | openspec/changes/linked-issue-field-availability/tasks.md#5.5 | issue | **字段 Spec 双层对同一任务的口径不一: yaml TASK-024 `verification[0]` 已改「14 个引用点 (CLAUDE.md:139/:141 + VERSION + README.md:8/:242 + i18n ×3 各 :3/:10/:244)」且 deliverables 含 `CLAUDE.md`, 但 yaml TASK-024 `title` 仍「VERSION:24 + README.md 2 点 + i18n ×3 各 3 点」(= 12 点, 无 CLAUDE.md), tasks.md 5.5 (:82) 同样只列 VERSION / README.md / i18n ×3 (12 点) 且 custom checks 列表缺 yaml 已列的 `m6-claude-md-version`。** [5][8] R2→R3 linked yaml diff @@ -627 只改了 verification[0]; tasks.md 0 hunk。为什么重要: tasks.md 是归档门与 handoff 消费的 checkbox 载体, 执行者按 5.5 做完 12 点会漏 CLAUDE.md 两处, 然后 yaml verification[0] 的 `grep … CLAUDE.md` 零命中断言红; 同一 14 点口径在探针 TASK-018 / 母 TASK-038 两份都是 title + deliverables + tasks.md 三处同步的。处方: yaml TASK-024 title 加「+ CLAUDE.md 2 点」; tasks.md :82 加「`CLAUDE.md:139/:141` 两处版本串」并把 `m6-claude-md-version` 补进 check 列表 (该 check 名在 `.aria/state-checks.yaml:104` 实存) |
| 10e7cea4 | minor | **残留** (R1 主控追记引入, R2 清账扫了 yaml 三处 + tasks.md :157/:309, 漏此处) | documentation | openspec/changes/sibling-spec-probe/tasks.md#L25 | issue | **探针 tasks.md :25「组间门」段的 TASK-003 子句仍只列「边: TASK-015 / 016 / 017 `dependencies` 各含 TASK-003, 主控裁量落第 4/5 组」, 漏了追记后最强的那条门边 TASK-004 ← TASK-003 (proposal :473「Phase B.1 不得开始」的落点)。** [7] 子句内 TASK-004 零命中; yaml `phase_b1_preconditions[1]` 已改为「上游边: TASK-004 (第 2 组起点 …) 与 TASK-015 / 016 / 017」, 两层不一致; 「主控裁量落第 4/5 组」半句也已被追记推翻 (现落第 2/4/5 组)。附 :11「`execution_order` 里『并行』只剩第 1 组 (三任务不同文件)」— 追记后第 1 组只剩 001 ‖ 002 两任务并行 (003 ← 002), 措辞不假但不再精确, 顺手改「(001 ‖ 002, 不同文件; 003 ← 002)」。处方: :25 子句改为「边: TASK-004 (第 2 组起点) 与 TASK-015 / 016 / 017 `dependencies` 各含 TASK-003」 |

**观察 (不计 finding, 留痕)**:

1. 探针贴出脚本 (e) 的结构盲区仍在 (本席 R2 预判): 坏输入 v3 把有依赖边的 002 / 003 改标「TASK-002 ‖ TASK-003 可并行」, 原样脚本 `RESULT: PASS` (exit 0) [6b] — (e) 只查行内同文件对, 对「有边却标并行」免疫。当前文件正确 (本席 [3] 独立箭头 / 并列检查 0 MISMATCH), 故不计; 若执笔席采处方 (f), 用 v3 验红。
2. linked yaml TASK-017 title「spec-drafter.json 新增 **新 eval** (id = ship 时 max(id)+1, 今日观测 3)」— 「新增 新」是 `eval id 3` → `新 eval (…)` 机械替换留下的叠字 (全文 1 处), 无语义影响。
3. 母贴出脚本 `[+]` 行用 `^- \[ \] (\d+\.\d+) ` 只匹配未勾选框, Phase B 勾选后该行会报 `parent ⊆ tasks.md 编号=False` — 它是规划期一次性核验, 不计; 若要留作 B 期复跑, 改 `\[[ x]\]`。
4. 已证伪的怀疑: linked TASK-024 verification 引用的 4 个 custom check 名 (`m6-version-badge-match` / `m6-claude-md-version` / `main-project-version-consistency` / `i18n-readme-translation-currency`) 在 `.aria/state-checks.yaml` 全部实存 [5]; TASK-040 命令行点名的 `origin` / `github` 两 remote 在 aria 子模块实存, `tag v<vNEXT>` 形态与既有 tag (`v1.67.2` …) 一致, `AB_TEST_OPERATIONS.md:222-228` 锚点实读 = 「场景 1 运行前置 (`ARIA_COORDINATION_NO_PUSH=1`)」段 [4]; a1 TASK-018 幂等坏臂改委派 TASK-025 — TASK-025 verification 第 3 条即 SC-22 (3)「切片内逐字 `check: coordination ref 内按 (container_id, session_id) 定位到本 session 的 active claim` 且含 `claims/`」, 宿主成立 [7]; TASK-040 估时 / agent / complexity 与 metadata 一致 (97-158; tech-lead ∈ roster; M) [4]; linked / sibling `summary` / `complexity_summary` / `agent_allocation` 计数与实况全等 [5]。
5. 不在本轮镜头、本席不评: TASK-024 (standards 侧) / TASK-036 / TASK-039 也不在 anc(TASK-038) — 它们不写 `aria/`, 且 TASK-024 自带 standards 的 merge / 双推 / gitlink, 与 TASK-038 是两个主仓 commit, 顺序无关 (R1/R2 已见, 未判缺陷)。

## 实测记录 (脚本 + 逐字输出; 主仓 HEAD c120f9e / aria d69091d; 2026-08-31 13:40–13:55 UTC)

### [0] 被审六份 sha256 (审前, 13:40:48Z)

```
d5b1429e030a2e8e5cffdcdab53ca408aa92e8e3d00ce2e4b63363db64281250  openspec/changes/linked-issue-field-availability/tasks.md
824c6a11db6a0cfc598e278c3b155225df16eeaa22ec5f10a364cae053c3cb72  openspec/changes/linked-issue-field-availability/detailed-tasks.yaml
2de1da5716d8e219d9454763c962596611880594d7252403eb207fc6d5946574  openspec/changes/sibling-spec-probe/tasks.md
26beac498ed367d1aee47a726c8c3defa0d6dcf1ee4ceaeddf10c00c242889d8  openspec/changes/sibling-spec-probe/detailed-tasks.yaml
b83cc8d3496c61c7c4d09db1bbcb9fa31469d96b7a642667d879841b10e0e81f  openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md
99a9baeaa6d10d105890ca7c7a1e8a799af00de196f384092109bebf460f7161  openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml
```

与 R2 [8] 比: linked tasks.md 未变; 其余五份已变 (R2→R3 diff 见 [8])。

### [1] 检查 1/3/6/7 — 字节卫生 · 两解析器 · status 枚举 · parent 1:1 · 必需字段 · estimated_hours 形态与求和 · deps 悬空/自依赖/环 · 后向边 · RED→GREEN 方向 · agent 集合

脚本 `r2a4/chk1_battery.py` 逐字复用 (sha256 `1126bb3f…45de`, 全文见 R2 报告 [1]), 对当前三份亲跑, 输出 (逐字):

```

===== linked-issue-field-availability
  CRLF=0 tab=0 ctrl=0
  safe_load OK: tasks=25 dup_ids=[] total_tasks(meta)=25
  parse_detailed_tasks: parse_ok=True n=25 statuses=['pending'] reason='25 task(s) parsed'
  status 枚举=['pending']
  parent 1:1: parents==25 boxes==25 seq_equal=True set_equal=True orphan_parent=[] orphan_box=[]
  必需字段缺失=none
  estimated_hours 全为 'a-b' 串: True bad=[]; est_hours 残留=[]; meta.estimated_hours='50-86'
  逐任务求和 lo-hi = 50-86
  deps: 悬空=[] 自依赖=[] 环=[]
  后向边 (依赖编号更大者) = []
  RED 任务=['TASK-005', 'TASK-006']
  RED 传递依赖 GREEN (实现/文本) = none
  agents=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']; agent_allocation keys=['backend-architect', 'knowledge-manager', 'new_agents', 'note', 'qa-engineer', 'tech-lead']

===== sibling-spec-probe
  CRLF=0 tab=0 ctrl=0
  safe_load OK: tasks=18 dup_ids=[] total_tasks(meta)=18
  parse_detailed_tasks: parse_ok=True n=18 statuses=['pending'] reason='18 task(s) parsed'
  status 枚举=['pending']
  parent 1:1: parents==18 boxes==18 seq_equal=True set_equal=True orphan_parent=[] orphan_box=[]
  必需字段缺失=none
  estimated_hours 全为 'a-b' 串: True bad=[]; est_hours 残留=[]; meta.estimated_hours='55-87'
  逐任务求和 lo-hi = 55-87
  deps: 悬空=[] 自依赖=[] 环=[]
  后向边 (依赖编号更大者) = []
  RED 任务=['TASK-004', 'TASK-005', 'TASK-007', 'TASK-008', 'TASK-009', 'TASK-014']
  RED 传递依赖 GREEN (实现/文本) = [('TASK-014', ['TASK-010', 'TASK-011', 'TASK-012', 'TASK-013'])]
  agents=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']; agent_allocation keys=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']

===== a1-entry-claim-duplicate-work-guard
  CRLF=0 tab=0 ctrl=0
  safe_load OK: tasks=40 dup_ids=[] total_tasks(meta)=40
  parse_detailed_tasks: parse_ok=True n=40 statuses=['pending'] reason='40 task(s) parsed'
  status 枚举=['pending']
  parent 1:1: parents==40 boxes==40 seq_equal=False set_equal=True orphan_parent=[] orphan_box=[]
  必需字段缺失=none
  estimated_hours 全为 'a-b' 串: True bad=[]; est_hours 残留=[]; meta.estimated_hours='97-158'
  逐任务求和 lo-hi = 97-158
  deps: 悬空=[] 自依赖=[] 环=[]
  后向边 (依赖编号更大者) = [('TASK-017', 'TASK-022'), ('TASK-017', 'TASK-025'), ('TASK-018', 'TASK-025'), ('TASK-019', 'TASK-026'), ('TASK-020', 'TASK-030'), ('TASK-021', 'TASK-028'), ('TASK-021', 'TASK-030'), ('TASK-022', 'TASK-027'), ('TASK-023', 'TASK-029')]
  RED 任务=['TASK-004', 'TASK-005', 'TASK-007', 'TASK-008', 'TASK-009', 'TASK-010', 'TASK-025', 'TASK-027', 'TASK-028', 'TASK-029', 'TASK-030']
  RED 传递依赖 GREEN (实现/文本) = none
  agents=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']; agent_allocation keys=None
```

> 注: sibling「RED 传递依赖 GREEN = TASK-014 → 010~013」仍为启发式误捕 (TASK-014 task_group=G3, GREEN 收口任务), R2 同注; a1 `agent_allocation keys=None` 因 a1 用 `metadata.agent_roster` 列表 (集合相等见 [5])。**a1 `seq_equal=False`** 是本轮相对 R2 唯一的结构层变化 → [1b]。

### [1b] a1 yaml 块序 vs tasks.md checkbox 序 (定位 seq_equal=False)

脚本 `s1b_parent_seq.py`:

```python
#!/usr/bin/env python3
"""R3/A4 [1b] a1 yaml 任务块物理顺序 vs tasks.md checkbox 顺序 (chk1 seq_equal=False 的定位)."""
import yaml, re
p="/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/"
raw=open(p+"detailed-tasks.yaml",encoding="utf-8").read(); T=yaml.safe_load(raw)["tasks"]
md=open(p+"tasks.md",encoding="utf-8").read()
ps=[t["parent"] for t in T]; ids=[t["id"] for t in T]
boxes=re.findall(r"^- \[[ x]\] (\d+\.\d+) ", md, re.M)
print("yaml ids 尾 4:", ids[-4:], "| yaml parents 尾 4:", ps[-4:], "| tasks.md boxes 尾 4:", boxes[-4:])
k=next((i for i,(a,b) in enumerate(zip(ps,boxes)) if a!=b),None)
print(f"首个不等位置 index={k}: yaml={ps[k]} md={boxes[k]}; set_equal={set(ps)==set(boxes)}; id 单调递增={ids==sorted(ids)}")
print("TASK-040 块起始行:", raw[:raw.find("  - id: TASK-040")].count("\n")+1, "; TASK-038 块起始行:", raw[:raw.find("  - id: TASK-038")].count("\n")+1, "; TASK-039 块起始行:", raw[:raw.find("  - id: TASK-039")].count("\n")+1)
```

输出:

```
yaml ids 尾 4: ['TASK-037', 'TASK-040', 'TASK-038', 'TASK-039'] | yaml parents 尾 4: ['8.1', '8.4', '8.2', '8.3'] | tasks.md boxes 尾 4: ['8.1', '8.2', '8.3', '8.4']
首个不等位置 index=37: yaml=8.4 md=8.2; set_equal=True; id 单调递增=False
TASK-040 块起始行: 956 ; TASK-038 块起始行: 977 ; TASK-039 块起始行: 1003
```

### [2] 三份 tasks.md「机械核验」贴出脚本逐字抽出 → 原样执行 → 与贴出输出逐行 diff (R2 4a669876 / 9db42f0a (1)(2) 闭合)

脚本 `extract_run_pasted.py` (sha256 `b8f5fc00…0fda`):

```python
#!/usr/bin/env python3
"""R3/A4: 从各 tasks.md `## 机械核验` 段抽第一个 ```python 块逐字落盘并原样执行 (cwd=/home/dev/Aria), 再抽贴出输出块与亲跑 stdout 逐行 diff."""
import re, subprocess, sys, difflib, pathlib
ROOT="/home/dev/Aria/openspec/changes/"
OUT=pathlib.Path("/tmp/claude-1000/-home-dev-Aria/0335d8a8-ad33-4d3d-9787-8f5ca5adea98/scratchpad/r3a4")
SPECS={"linked-issue-field-availability":"linked","sibling-spec-probe":"sibling","a1-entry-claim-duplicate-work-guard":"a1"}
for s,short in SPECS.items():
    md=open(ROOT+s+"/tasks.md",encoding="utf-8").read()
    sec=md.split("机械核验",1)[1] if "机械核验" in md else ""
    # 找 `## 机械核验` 或 `### 机械核验` 标题之后的段
    m=re.search(r"^#{2,3} 机械核验.*?$", md, re.M)
    sec=md[m.end():]
    code=re.search(r"```python\n(.*?)```", sec, re.S).group(1)
    # 贴出输出: 第一个 ```(text)?\n 块 (代码块之后)
    after=sec[sec.find("```python"):]
    after=after[after.find("```", 10)+3:]  # skip code block
    outm=re.search(r"```(?:text)?\n(.*?)```", after, re.S)
    pasted=outm.group(1)
    p=OUT/f"pasted_{short}.py"; p.write_text(code,encoding="utf-8")
    dbl=("\\\\d" in code) or ("\\\\[" in code) or ("\\\\." in code)
    r=subprocess.run([sys.executable,str(p)],cwd="/home/dev/Aria",capture_output=True,text=True)
    (OUT/f"pasted_{short}_stdout.txt").write_text(r.stdout,encoding="utf-8")
    (OUT/f"pasted_{short}_expected.txt").write_text(pasted,encoding="utf-8")
    print(f"===== {s}: code_lines={code.count(chr(10))} double_backslash={dbl} exit={r.returncode}")
    if r.stderr.strip(): print("  STDERR:", r.stderr.strip()[:600])
    got=[l.rstrip() for l in r.stdout.splitlines()]
    exp=[l.rstrip() for l in pasted.splitlines()]
    d=list(difflib.unified_diff(exp,got,fromfile="pasted-in-tasks.md",tofile="actual-run",lineterm="",n=0))
    print(f"  pasted_lines={len(exp)} actual_lines={len(got)} identical={got==exp}")
    if d: print("  DIFF:\n    "+"\n    ".join(d[:80]))
    print(f"  last line actual: {got[-1] if got else None!r}")
```

输出 (逐字; `identical=True` = 亲跑 stdout 与 tasks.md 贴出输出块逐行相等):

```
===== linked-issue-field-availability: code_lines=90 double_backslash=False exit=0
  pasted_lines=30 actual_lines=30 identical=True
  last line actual: 'RESULT: PASS'
===== sibling-spec-probe: code_lines=92 double_backslash=False exit=0
  pasted_lines=44 actual_lines=44 identical=True
  last line actual: 'RESULT: PASS'
===== a1-entry-claim-duplicate-work-guard: code_lines=129 double_backslash=False exit=0
  pasted_lines=28 actual_lines=28 identical=True
  last line actual: 'RESULT: PASS'
```

亲跑 stdout 落盘 `r3a4/pasted_{linked,sibling,a1}_stdout.txt`, 贴文落盘 `pasted_*_expected.txt`, 三对文件 `identical=True`。

### [3] 探针 `execution_order` 箭头 / 并列 vs `dependencies`; `phase_b1_preconditions` 声称边 vs 实况 (R2 ea33f282 闭合)

脚本 `s2_execorder.py`:

```python
#!/usr/bin/env python3
"""R3/A4 [3] sibling execution_order 箭头/并列 vs dependencies; phase_b1_preconditions 声称边 vs 实况 (R2 ea33f282 闭合)."""
import yaml,re
S="/home/dev/Aria/openspec/changes/sibling-spec-probe/detailed-tasks.yaml"
d=yaml.safe_load(open(S,encoding="utf-8")); T={t["id"]:t for t in d["tasks"]}
deps={i:list(t.get("dependencies") or []) for i,t in T.items()}
def anc(i,seen=None):
    seen=set() if seen is None else seen
    for j in deps[i]:
        if j not in seen: seen.add(j); anc(j,seen)
    return seen
fails=[]
for ln,line in enumerate(d["execution_order"]):
    body=re.sub(r"^\[[^\]]*\]\s*","",line)
    for seg in [s for s in re.split(r"\s*(?:→|;)\s*",body) if s.strip()]:
        heads=re.findall(r"TASK-(\d{3})",seg.split("←")[0])
        if "←" in seg and heads:
            tail=seg.split("←",1)[1].split("(")[0]
            want={f"TASK-{n}" for n in re.findall(r"\b(\d{3})\b",tail)}; h=heads[-1]; have=set(deps[f"TASK-{h}"])
            print(f"  L{ln} TASK-{h} ← {sorted(want)} ⊆ deps {sorted(have)} : {'OK' if want<=have else 'MISMATCH '+str(sorted(want-have))}" + (f"  (deps 多于箭头: {sorted(have-want)})" if have-want else ""))
            if not want<=have: fails.append((h,sorted(want-have)))
    for a,b in re.findall(r"TASK-(\d{3})[^‖→;]*‖\s*TASK-(\d{3})",body):
        A,B=f"TASK-{a}",f"TASK-{b}"; bad=(A in anc(B)) or (B in anc(A))
        print(f"  L{ln} 并列组 {A} ‖ {B}: 互不在对方传递 deps = {not bad}")
        if bad: fails.append(("par",A,B))
    if "并行" in line:
        ts=re.findall(r"TASK-\d{3}",line)
        print(f"  L{ln} 含「并行」字样, 行内任务={ts}; 行内有直接依赖边的对: {[(x,y) for x in ts for y in ts if x!=y and x in deps[y]]}")
print("箭头/并列 fails:",fails or "none")
for i,p in enumerate(d["metadata"]["phase_b1_preconditions"]):
    up=re.match(r"(TASK-\d{3}) done",p).group(1); tail=p.split("上游边:",1)[1]; ids=set()
    for m in re.finditer(r"TASK-(\d{3})((?: / \d{3})*)",tail):
        ids.add("TASK-"+m.group(1)); ids|={"TASK-"+x for x in re.findall(r"\d{3}",m.group(2))}
    ids.discard(up); actual=sorted(t for t in T if up in deps[t])
    print(f"  precond[{i}] {up} 声称上游边 {sorted(ids)}; 不含该边的: {[t for t in sorted(ids) if up not in deps[t]] or 'none'}; 实际直接含 {up} 的: {actual}; 声称未列: {sorted(set(actual)-ids) or 'none'}")
```

输出 (逐字):

```
  L0 TASK-003 ← ['TASK-002'] ⊆ deps ['TASK-002'] : OK
  L0 并列组 TASK-001 ‖ TASK-002: 互不在对方传递 deps = True
  L0 含「并行」字样, 行内任务=['TASK-001', 'TASK-002', 'TASK-003']; 行内有直接依赖边的对: [('TASK-002', 'TASK-003')]
  L1 TASK-004 ← ['TASK-001', 'TASK-002', 'TASK-003'] ⊆ deps ['TASK-001', 'TASK-002', 'TASK-003'] : OK
  L2 TASK-005 ← ['TASK-001', 'TASK-004'] ⊆ deps ['TASK-001', 'TASK-004'] : OK
  L2 TASK-006 ← ['TASK-001', 'TASK-005'] ⊆ deps ['TASK-001', 'TASK-005'] : OK
  L2 TASK-007 ← ['TASK-001', 'TASK-006'] ⊆ deps ['TASK-001', 'TASK-006'] : OK
  L2 TASK-008 ← ['TASK-001', 'TASK-007'] ⊆ deps ['TASK-001', 'TASK-007'] : OK
  L2 TASK-009 ← ['TASK-001', 'TASK-008'] ⊆ deps ['TASK-001', 'TASK-008'] : OK
  L3 TASK-010 ← ['TASK-004', 'TASK-008'] ⊆ deps ['TASK-004', 'TASK-008'] : OK
  L4 TASK-011 ← ['TASK-005', 'TASK-006', 'TASK-010'] ⊆ deps ['TASK-005', 'TASK-006', 'TASK-010'] : OK
  L4 TASK-012 ← ['TASK-007', 'TASK-010', 'TASK-011'] ⊆ deps ['TASK-007', 'TASK-010', 'TASK-011'] : OK
  L5 TASK-013 ← ['TASK-007', 'TASK-012'] ⊆ deps ['TASK-007', 'TASK-012'] : OK
  L6 TASK-014 ← ['TASK-009', 'TASK-011', 'TASK-012', 'TASK-013'] ⊆ deps ['TASK-009', 'TASK-011', 'TASK-012', 'TASK-013'] : OK
  L7 TASK-015 ← ['TASK-003', 'TASK-009'] ⊆ deps ['TASK-003', 'TASK-009'] : OK
  L8 TASK-016 ← ['TASK-003', 'TASK-009', 'TASK-015'] ⊆ deps ['TASK-003', 'TASK-009', 'TASK-015'] : OK
  L9 TASK-017 ← ['TASK-003', 'TASK-014', 'TASK-015', 'TASK-016'] ⊆ deps ['TASK-003', 'TASK-014', 'TASK-015', 'TASK-016'] : OK
箭头/并列 fails: none
  precond[0] TASK-001 声称上游边 ['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']; 不含该边的: none; 实际直接含 TASK-001 的: ['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']; 声称未列: none
  precond[1] TASK-003 声称上游边 ['TASK-004', 'TASK-015', 'TASK-016', 'TASK-017']; 不含该边的: none; 实际直接含 TASK-003 的: ['TASK-004', 'TASK-015', 'TASK-016', 'TASK-017']; 声称未列: none
```

### [4] TASK-040 试派生: deps / 发布链祖先闭包 vs `aria/` 侧写任务 / gitlink 实存口径 / remote 与 tag 形态 / 锚点

脚本 `s3_task040.py`:

```python
#!/usr/bin/env python3
"""R3/A4 [4] TASK-040 试派生: deps / 发布链祖先闭包 vs aria 侧写任务 / gitlink 实存口径 / remote 名实存 / tag 形态."""
import yaml,re,os,subprocess
A="/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml"
raw=open(A,encoding="utf-8").read(); d=yaml.safe_load(raw); T={t["id"]:t for t in d["tasks"]}
deps={i:list(t.get("dependencies") or []) for i,t in T.items()}
def anc(i,seen=None):
    seen=set() if seen is None else seen
    for j in deps[i]:
        if j not in seen: seen.add(j); anc(j,seen)
    return seen
print("TASK-040 deps:",deps["TASK-040"],"| TASK-038 deps:",deps["TASK-038"],"| TASK-037 deps:",deps["TASK-037"])
a40=anc("TASK-040")
aria_side=sorted(i for i,t in T.items() if any(str(x).startswith("aria/") for x in (t.get("deliverables") or [])))
print(f"aria/ 侧写任务 {len(aria_side)} 个; 不在 anc(TASK-040) 的: {[i for i in aria_side if i not in a40 and i!='TASK-040']}")
print("不在 anc(TASK-038) 的任务 (除自身):", sorted(i for i in T if i!="TASK-038" and i not in anc("TASK-038")))
for x in ["TASK-004","TASK-005","TASK-006","TASK-007","TASK-008","TASK-009","TASK-010"]:
    print(f"  {x} 的直接依赖者: {sorted(i for i in T if x in deps[i])}")
t=T["TASK-009"]; print("TASK-009:",t["title"],"| deps:",deps["TASK-009"],"| deliverables:",t["deliverables"])
print("anc(TASK-038) ⊇ anc(TASK-040) ∪ {040}:",(a40|{"TASK-040"})<=anc("TASK-038"),"; 依赖 TASK-040 的任务:",sorted(i for i in T if "TASK-040" in anc(i)))
print("估时: metadata", d["metadata"]["estimated_hours"], "; TASK-040", T["TASK-040"]["estimated_hours"], "; agent", T["TASK-040"]["agent"], "∈ roster", T["TASK-040"]["agent"] in d["metadata"]["agent_roster"], "; complexity", T["TASK-040"]["complexity"])
run=lambda c: subprocess.run(c,shell=True,capture_output=True,text=True,cwd="/home/dev/Aria").stdout.strip()
print("gitlink 实存口径 = index 条目 mode 160000 + 工作树目录 + `git submodule status` 可解析 (非 os.path.exists 单独判):")
print("  git ls-files -s aria ->", run("git ls-files -s aria")); print("  isdir(aria) ->", os.path.isdir("/home/dev/Aria/aria")); print("  git submodule status aria ->", run("git submodule status aria"))
print("aria remotes (TASK-040 命令行点名 origin / github):"); print("  "+run("git -C aria remote -v").replace("\n","\n  "))
print("aria tag 形态 (TASK-040 写 `git -C aria tag v<vNEXT>`):", run("git -C aria tag --sort=-v:refname | head -3").split())
print("AB_TEST_OPERATIONS.md:222 ->", run("sed -n '222p' aria-plugin-benchmarks/AB_TEST_OPERATIONS.md")[:90])
```

输出 (逐字):

```
TASK-040 deps: ['TASK-037'] | TASK-038 deps: ['TASK-037', 'TASK-040'] | TASK-037 deps: ['TASK-011', 'TASK-012', 'TASK-013', 'TASK-014', 'TASK-015', 'TASK-016', 'TASK-017', 'TASK-018', 'TASK-019', 'TASK-020', 'TASK-021', 'TASK-022', 'TASK-023', 'TASK-025', 'TASK-026', 'TASK-027', 'TASK-028', 'TASK-029', 'TASK-030', 'TASK-031', 'TASK-032', 'TASK-033', 'TASK-034', 'TASK-035']
aria/ 侧写任务 30 个; 不在 anc(TASK-040) 的: ['TASK-009']
不在 anc(TASK-038) 的任务 (除自身): ['TASK-009', 'TASK-024', 'TASK-036', 'TASK-039']
  TASK-004 的直接依赖者: ['TASK-011']
  TASK-005 的直接依赖者: ['TASK-006', 'TASK-012']
  TASK-006 的直接依赖者: ['TASK-012']
  TASK-007 的直接依赖者: ['TASK-008', 'TASK-013']
  TASK-008 的直接依赖者: ['TASK-009', 'TASK-014', 'TASK-015']
  TASK-009 的直接依赖者: []
  TASK-010 的直接依赖者: ['TASK-016']
TASK-009: SC-23 / SC-14(a) 回归守卫 (CLI 全链路, baseline 即绿) + SC-2 ↔ SC-23 相容性断言 | deps: ['TASK-001', 'TASK-003', 'TASK-008'] | deliverables: ['aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py', 'aria/skills/state-scanner/scripts/release_gate.py']
anc(TASK-038) ⊇ anc(TASK-040) ∪ {040}: True ; 依赖 TASK-040 的任务: ['TASK-038']
估时: metadata 97-158 ; TASK-040 3-5 ; agent tech-lead ∈ roster True ; complexity M
gitlink 实存口径 = index 条目 mode 160000 + 工作树目录 + `git submodule status` 可解析 (非 os.path.exists 单独判):
  git ls-files -s aria -> 160000 d69091dfdeb0c6cd83b03da2492812d33cec3712 0	aria
  isdir(aria) -> True
  git submodule status aria -> d69091dfdeb0c6cd83b03da2492812d33cec3712 aria (v1.67.2)
aria remotes (TASK-040 命令行点名 origin / github):
  github	git@github.com:10CG/aria-plugin.git (fetch)
  github	git@github.com:10CG/aria-plugin.git (push)
  origin	ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git (fetch)
  origin	ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git (push)
aria tag 形态 (TASK-040 写 `git -C aria tag v<vNEXT>`): ['v1.67.2', 'v1.67.1', 'v1.67.0']
AB_TEST_OPERATIONS.md:222 -> #### 场景 1 运行前置: 协调 ref 推送隔离 (`ARIA_COORDINATION_NO_PUSH=1`)
```

TASK-040 raw 块 (yaml :956-976, 逐字节选 deliverables / verification):

```
    dependencies: [TASK-037]
    deliverables:
      - aria   # 子模块 master: 本地 `git -C aria merge --no-ff feature/<branch>` (禁 Forgejo 服务端合并, CLAUDE.md 硬约束 1) + `git -C aria tag v<vNEXT>`
    verification:
      - "合并在本地做: `git -C aria log -1 --format=%P master` 有两个父 (merge commit 本地生成), Forgejo PR 页面若存在只作审阅, 不点 Do: merge"
      - "双推给足超时: `git -C aria push origin master --tags && git -C aria push github master --tags` (memory partial-push: 命令超时 ≥ 300s)"
      - "推后逐个核验, 不信 push 回执: `git -C aria ls-remote origin master` / `git -C aria ls-remote github master` / `git -C aria rev-parse master` 三者 SHA 逐字节相等; tag 同法 (`ls-remote --tags`); ls-remote 自身失败 ⇒ 重试再下结论 (CLAUDE.md 硬约束 2)"
      - "两 remote 一致后才允许 TASK-038 bump 主仓 gitlink (否则 orphaned gitlink, GitHub clone --recursive 断裂, 2026-07-14 事故形状)"
```

TASK-038 `dependencies: [TASK-037, TASK-040]   # TASK-040 = aria 子模块双推核验一致后才 bump gitlink (R2/A1)` (yaml :986)。

### [5] 检查 4/5/8 — 覆盖表 token / deliverables 实存性 / roster (脚本复用) + flag 字面 (9db42f0a (3)) + summary / agent_allocation / check 名实存

脚本 `r2a4/chk3_cov_deliv.py` 逐字复用 (sha256 `e5cb00f3…5bcc`, 全文见 R2 报告 [3]), 输出 (逐字):

```

===== linked-issue-field-availability
  覆盖表行=10 (SC,TASK) 对=28
  verification 无 token: 0 []
  整块 (title/verification/deliverables 注释/notes) 无 token: 0 []
  yaml verification 出现但表无行: ['SC-19']
  deliverables 行=36
  agent 字段分布={k:len(v) for k,v in ag.items()}
    roster type: list ['qa-engineer', 'backend-architect', 'knowledge-manager', 'tech-lead']

===== sibling-spec-probe
  覆盖表行=21 (SC,TASK) 对=46
  verification 无 token: 0 []
  整块 (title/verification/deliverables 注释/notes) 无 token: 0 []
  yaml verification 出现但表无行: []
  deliverables 行=41
    ⚠ 未标新建但不存在: TASK-001 aria/skills/state-scanner/lib/linked_issue_field.py | # 由姊妹 Spec 交付; 本 Spec 只核验, 零改动 (今天不存在)
    ⚠ 未标新建但不存在: TASK-005 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # 夹具以字符串字面量内嵌 (逐字原文)
    ⚠ 未标新建但不存在: TASK-006 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # 三臂对照 + 第四臂合成夹具
    ⚠ 未标新建但不存在: TASK-007 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # runner 体例仿 phase-d-closer/tests/test_fetch_gate.py:22 `_runner(seq)`: run(args
    ⚠ 未标新建但不存在: TASK-008 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # subprocess.run([sys.executable, <script>, ...]) 体例仿 state-scanner/tests/test_c
    ⚠ 未标新建但不存在: TASK-009 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # 读同 skill 的 SKILL.md 与 references/execution-modes.md (Path(__file__).parents[1]
    ⚠ 未标新建但不存在: TASK-011 aria/skills/audit-engine/scripts/sibling_spec_probe.py | # 纯分类函数 + 键构造 + 求交
    ⚠ 未标新建但不存在: TASK-012 aria/skills/audit-engine/scripts/sibling_spec_probe.py | # remote/default-branch/fetch 段
    ⚠ 未标新建但不存在: TASK-013 aria/skills/audit-engine/scripts/sibling_spec_probe.py | # corpus 段
    ⚠ 未标新建但不存在: TASK-014 aria/skills/audit-engine/scripts/sibling_spec_probe.py | 
    ⚠ 未标新建但不存在: TASK-014 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | 
    ⚠ 未标新建但不存在: TASK-017 aria-plugin-benchmarks/ab-suite/audit-engine.json | # 若三臂语义分档显示断言措辞过宽 ⇒ 拆条不删 (手册 :142-159), 并 version.yaml 再升
  agent 字段分布={k:len(v) for k,v in ag.items()}
    roster type: list ['tech-lead', 'qa-engineer', 'backend-architect', 'knowledge-manager']

===== a1-entry-claim-duplicate-work-guard
  覆盖表行=33 (SC,TASK) 对=55
  verification 无 token: 0 []
  整块 (title/verification/deliverables 注释/notes) 无 token: 0 []
  yaml verification 出现但表无行: []
  deliverables 行=86
    ⚠ 标新建但已存在: TASK-001 docs/handoff/
    ⚠ 未标新建但不存在: TASK-006 aria/skills/state-scanner/tests/test_heartbeat_by_track.py | # 同文件加 TestRenameTwoStep 类 (改名是 claim_lifecycle 语义, 与 heartbeat 同宿主); 串行于 TASK-0
    ⚠ 未标新建但不存在: TASK-008 aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py | # 同文件加四个测试类; 串行于 TASK-007 之后
    ⚠ 未标新建但不存在: TASK-009 aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py | # 同文件加 TestA1CarryIdRoundTrip; 串行于 TASK-008 之后
    占位路径 TASK-031 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/phase-a-planner/
    占位路径 TASK-032 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/spec-drafter/
    占位路径 TASK-033 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/state-scanner/
    占位路径 TASK-034 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/phase-b-developer/
    占位路径 TASK-034 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/branch-manager/
    占位路径 TASK-034 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/phase-d-closer/
    占位路径 TASK-035 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/targeted/
  agent 字段分布={k:len(v) for k,v in ag.items()}
    roster type: list ['backend-architect', 'qa-engineer', 'knowledge-manager', 'tech-lead']
```

> 与 R2 [3] 比: a1 `deliverables 行=85 → 86` (TASK-040 的 `aria`), 其余逐行相同; 「未标新建但不存在」12+3 处仍全是同 Spec 上游任务新建的同一文件 (R1/R2 同口径剔除); 占位路径 7 处为 `<vNEXT>` 形态。

脚本 `s4_flags_summary.py`:

```python
#!/usr/bin/env python3
"""R3/A4 [5] a1 flag 字面 (R2 9db42f0a (3) 闭合) + linked/sibling summary 与 agent_allocation 一致性 + linked 引用 check 名实存."""
import re,yaml,subprocess
from collections import Counter
A="/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml"; raw=open(A,encoding="utf-8").read()
def block(i): return re.search(rf"  - id: {i}\n(.*?)(?=\n  - id: TASK-|\Z)", raw, re.S).group(1)
for i in ["TASK-001","TASK-031","TASK-032","TASK-033","TASK-034","TASK-035"]:
    b=block(i); print(f"  {i}: --no-push={'Y' if '--no-push' in b else 'N'}  ARIA_COORDINATION_NO_PUSH={'Y' if 'ARIA_COORDINATION_NO_PUSH' in b else 'N'}")
print("  TASK-034 verification[0] 逐字:", yaml.safe_load(open(A,encoding="utf-8"))["tasks"][33]["verification"][0])
md=open("/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md",encoding="utf-8").read()
print("  tasks.md 映射行:", re.search(r"`--no-push` / `ARIA_COORDINATION_NO_PUSH` \([^)]*\)", md).group(0))
for i,flags in (("TASK-018",["--raw-track-id","--phase A.1","--mode advisory","--linked-issue","--repo-path"]),("TASK-019",["--status abandoned","--sweep-stale","--gc"])):
    b=block(i); print(f"  {i}: "+"  ".join(f"{f}={'Y' if f in b else 'N'}" for f in flags))
L=yaml.safe_load(open("/home/dev/Aria/openspec/changes/linked-issue-field-availability/detailed-tasks.yaml",encoding="utf-8"))
print("linked summary.by_complexity:",{k:v["count"] for k,v in L["summary"]["by_complexity"].items()},"actual:",dict(Counter(t["complexity"] for t in L["tasks"])),"; summary.estimated_hours:",L["summary"]["estimated_hours"])
for k,v in L["agent_allocation"].items():
    lst=v.get("tasks") if isinstance(v,dict) else v
    if isinstance(lst,list): print(f"  linked agent_allocation {k}: n={len(lst)} match={sorted(lst)==sorted(t['id'] for t in L['tasks'] if t['agent']==k)}")
Sb=yaml.safe_load(open("/home/dev/Aria/openspec/changes/sibling-spec-probe/detailed-tasks.yaml",encoding="utf-8"))
print("sibling complexity_summary:",{k:v["count"] for k,v in Sb["complexity_summary"].items() if isinstance(v,dict)},"actual:",dict(Counter(t["complexity"] for t in Sb["tasks"])),"; total:",Sb["complexity_summary"]["total_estimated_hours"])
for k,v in Sb["agent_allocation"].items():
    lst=v.get("tasks") if isinstance(v,dict) else v
    if isinstance(lst,list): print(f"  sibling agent_allocation {k}: n={len(lst)} match={sorted(lst)==sorted(t['id'] for t in Sb['tasks'] if t['agent']==k)}")
sc=open("/home/dev/Aria/.aria/state-checks.yaml",encoding="utf-8").read()
for n in ["m6-version-badge-match","m6-claude-md-version","main-project-version-consistency","i18n-readme-translation-currency"]:
    print(f"  state-checks.yaml 含 name {n}: {sc.count(chr(34)+n+chr(34))}")
TL={t["id"]:t for t in L["tasks"]}
print("linked TASK-024 title:",TL["TASK-024"]["title"]); print("  deliverables:",TL["TASK-024"]["deliverables"]); print("  verification[0][:60]:",TL["TASK-024"]["verification"][0][:60])
lmd=open("/home/dev/Aria/openspec/changes/linked-issue-field-availability/tasks.md",encoding="utf-8").read().splitlines()
print("  tasks.md :82 (5.5) 含 CLAUDE.md:", "CLAUDE.md" in lmd[81], "| 含 m6-claude-md-version:", "m6-claude-md-version" in lmd[81])
print("linked TASK-017 title:",TL["TASK-017"]["title"])
```

输出 (逐字):

```
  TASK-001: --no-push=Y  ARIA_COORDINATION_NO_PUSH=N
  TASK-031: --no-push=N  ARIA_COORDINATION_NO_PUSH=Y
  TASK-032: --no-push=N  ARIA_COORDINATION_NO_PUSH=Y
  TASK-033: --no-push=N  ARIA_COORDINATION_NO_PUSH=Y
  TASK-034: --no-push=N  ARIA_COORDINATION_NO_PUSH=N
  TASK-035: --no-push=N  ARIA_COORDINATION_NO_PUSH=Y
  TASK-034 verification[0] 逐字: 运行前置 / 核验 / 清理三条同 TASK-031; phase-d-closer 的 release_gate 输出亦须 push_skipped: true
  tasks.md 映射行: `--no-push` / `ARIA_COORDINATION_NO_PUSH` (001, 031–035)
  TASK-018: --raw-track-id=Y  --phase A.1=Y  --mode advisory=Y  --linked-issue=Y  --repo-path=Y
  TASK-019: --status abandoned=Y  --sweep-stale=Y  --gc=Y
linked summary.by_complexity: {'S': 14, 'M': 10, 'L': 1, 'XL': 0} actual: {'M': 10, 'S': 14, 'L': 1} ; summary.estimated_hours: 50-86
  linked agent_allocation qa-engineer: n=11 match=True
  linked agent_allocation backend-architect: n=5 match=True
  linked agent_allocation knowledge-manager: n=6 match=True
  linked agent_allocation tech-lead: n=3 match=True
  linked agent_allocation new_agents: n=0 match=True
sibling complexity_summary: {'S': 4, 'M': 11, 'L': 3, 'XL': 0} actual: {'S': 4, 'M': 11, 'L': 3} ; total: 55-87
  sibling agent_allocation tech-lead: n=1 match=True
  sibling agent_allocation qa-engineer: n=9 match=True
  sibling agent_allocation backend-architect: n=5 match=True
  sibling agent_allocation knowledge-manager: n=3 match=True
  state-checks.yaml 含 name m6-version-badge-match: 1
  state-checks.yaml 含 name m6-claude-md-version: 1
  state-checks.yaml 含 name main-project-version-consistency: 1
  state-checks.yaml 含 name i18n-readme-translation-currency: 1
linked TASK-024 title: 主仓版本引用面 — VERSION:24 + README.md 2 点 + i18n ×3 各 3 点 (仅版本串)
  deliverables: ['VERSION', 'README.md', 'CLAUDE.md', 'README.zh.md', 'README.ja.md', 'README.ko.md']
  verification[0][:60]: 14 个引用点 (与 086ee32 同口径: CLAUDE.md:139/:141 + VERSION + READM
  tasks.md :82 (5.5) 含 CLAUDE.md: False | 含 m6-claude-md-version: False
linked TASK-017 title: 可证伪定向 fixture ×1 (SC-7 双臂) — spec-drafter.json 新增 新 eval (id = ship 时 max(id)+1, 今日观测 3) (中文臂); 英文臂 = 更新后的 eval id 2
```

### [6] 残留 grep (六份, 逐字命中行, 截 150 列)

脚本 `s5_residual_grep.sh`:

```bash
#!/bin/bash
# R3/A4 [6] 残留 grep (逐字命中; 六份). 截列用 python 按字符截 (不用 cut/sed 的字节截, 避免切坏 UTF-8)
cd /home/dev/Aria/openspec/changes
F="linked-issue-field-availability/tasks.md linked-issue-field-availability/detailed-tasks.yaml sibling-spec-probe/tasks.md sibling-spec-probe/detailed-tasks.yaml a1-entry-claim-duplicate-work-guard/tasks.md a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml"
trunc() { python3 -c 'import sys
for l in sys.stdin.buffer.read().decode("utf-8").splitlines(): print(l[:150]+(" …" if len(l)>150 else ""))'; }
for pat in '1\.68\.0' '1\.67\.3' 'README\.zh-CN' 'est_hours:' 'parallelizable' '未自行加边' '13 项'; do
  echo "--- $pat :"; grep -n -E "$pat" $F | trunc || echo "  (零命中)"
done
echo "--- <vNEXT> 行数:"; grep -c '<vNEXT>' $F
echo "--- 「39」(a1 两份):"; grep -n -E '\b39\b' a1-entry-claim-duplicate-work-guard/tasks.md a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml | trunc
```

输出:

```
--- 1\.68\.0 :
linked-issue-field-availability/tasks.md:7:> **ship target**: aria-plugin **`<vNEXT>`** (R1/C3 三份统一占位, 本文件**不写** v1.68.0 / v1.67.3 字面; proposal §Impac …
linked-issue-field-availability/tasks.md:177:| 3221f943 | A1 | major | closed (本 Spec 侧, 方案 C3) — 版本字面 v1.68.0 / v1.67.3 全部改 `<vNEXT>` 占位; TASK-021 no …
linked-issue-field-availability/tasks.md:178:| 970d3368 | A1 | minor | closed — TASK-008 SKIP 文案「版本 < v1.68.0」改 `<vNEXT>` + 「落地时以 plugin.json 实际号回填并在  …
sibling-spec-probe/tasks.md:121:5. **版本号档位与号 (R1 C3 三份统一句)**: 本 Spec 新增运行时指令面 (audit-engine SKILL.md + execution-modes.md) + 新脚本, CLAUDE.md「新增 Skill / …
a1-entry-claim-duplicate-work-guard/tasks.md:196:6. **版本号**: A.2 倾向 MINOR; 号 = `<vNEXT>` 落地时计算, 不预写 (R1 C3: 字段 Spec 与本 Spec 曾同写 v1.68.0 而串行 ship 三档必撞号 …
a1-entry-claim-duplicate-work-guard/tasks.md:249:| `3221f943` | A1 (major) | C3 版本档撞号 + ab-results 字面量 | **closed** (留痕, 不拍板) | yaml: TASK-031~035 五处  …
--- 1\.67\.3 :
linked-issue-field-availability/tasks.md:7:> **ship target**: aria-plugin **`<vNEXT>`** (R1/C3 三份统一占位, 本文件**不写** v1.68.0 / v1.67.3 字面; proposal §Impac …
linked-issue-field-availability/tasks.md:177:| 3221f943 | A1 | major | closed (本 Spec 侧, 方案 C3) — 版本字面 v1.68.0 / v1.67.3 全部改 `<vNEXT>` 占位; TASK-021 no …
sibling-spec-probe/tasks.md:121:5. **版本号档位与号 (R1 C3 三份统一句)**: 本 Spec 新增运行时指令面 (audit-engine SKILL.md + execution-modes.md) + 新脚本, CLAUDE.md「新增 Skill / …
--- README\.zh-CN :
a1-entry-claim-duplicate-work-guard/tasks.md:247:| `73809784` | A1 (critical) | C2 TASK-038 发布同步面 | **closed** | yaml TASK-038: 删 `.gitmodules` (不承载 g …
a1-entry-claim-duplicate-work-guard/tasks.md:248:| `518a7d7f` | A4 (major) | C2 `README.zh-CN.md` | **closed** | 同上 (与 A1 73809784 同一改动) |
a1-entry-claim-duplicate-work-guard/tasks.md:455:解析器: PyYAML `safe_load` 通过; `aria/skills/state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_ …
a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml:1001:    notes: "子模块 aria 的合并一律本地 merge + 双推 (CLAUDE.md 硬约束 1), 禁 Forgejo 服务端合并。R1 C2: 清单以字段 S …
--- est_hours: :
linked-issue-field-availability/tasks.md:179:| df090b25 | A4 | major | closed — 25/25 `est_hours: int` → `estimated_hours: "a-b"` (S "1-2" / M "3-5" / …
sibling-spec-probe/tasks.md:151:| df090b25 (A4) / C9 | A4 · major | **closed** — 18 处 `est_hours: <int>` → `estimated_hours: "a-b"` (S "1-2" / M "3-5" …
--- parallelizable :
linked-issue-field-availability/tasks.md:171:| 9b64d749 | A2 | critical | closed — 同文件任务全部串行 (同文件): 组 1 六条链式 001→…→006, 008→009, 014→015, 016→017→018→ …
linked-issue-field-availability/tasks.md:192:> 脚本 (`check_c1.py`, 在主仓根执行; exit 0 = PASS)。断言: (a) 任意两任务 deliverables 交集非空 ⇒ 后者依赖前者 (直接或传递); (b) 无环 / 无悬 …
linked-issue-field-availability/tasks.md:230:# (d) execution_order 任何并行标记 (parallelizable 列表 / {A, B} / A ‖ B) 内无同文件对
linked-issue-field-availability/tasks.md:234:    if isinstance(v.get("parallelizable"), list): groups.append(list(v["parallelizable"]))
linked-issue-field-availability/tasks.md:242:bad_word = [ln.strip() for ln in eo_txt.splitlines() if re.search(r"并行|parallelizable", ln) and "不同文件" no …
--- 未自行加边 :
--- 13 项 :
--- <vNEXT> 行数:
linked-issue-field-availability/tasks.md:4
linked-issue-field-availability/detailed-tasks.yaml:5
sibling-spec-probe/tasks.md:3
sibling-spec-probe/detailed-tasks.yaml:5
a1-entry-claim-duplicate-work-guard/tasks.md:5
a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml:11
--- 「39」(a1 两份):
a1-entry-claim-duplicate-work-guard/tasks.md:232:- **Phase A.3**: 无需新 Agent — 既有 roster `backend-architect` (lib / CLI) · `qa-engineer` (红测 / 结构测试 / A …
a1-entry-claim-duplicate-work-guard/tasks.md:455:解析器: PyYAML `safe_load` 通过; `aria/skills/state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_ …
a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml:134:        `grep -n no_push aria/skills/state-scanner/scripts/phase1_gate.py` 非空 (:35-39 docs …
```

判读: 7 个残留模式里 `未自行加边` / `13 项` 零命中; 其余命中逐行核: sibling :121 / linked :7 / a1 :196 = 「不写 / 不预写 v1.68.0 / v1.67.3」统一句, linked :177-179 / sibling :151 / a1 :247-249 = R1 清账对账留痕行, a1 :455 = 残留字面量声明句, linked :171 = 对账留痕, linked :192 / :230 / :234 / :242 = 贴出脚本 (d) 的正文 (它要拒绝的字样), a1 yaml :1001 = TASK-038 notes 「已改」留痕。两份 yaml 里 `1.68.0` / `1.67.3` / `est_hours:` / `parallelizable` 零命中。`\b39\b` 命中: a1 tasks.md :232 / :455 (陈旧, 见 64cf8dd9), a1 yaml :134 是 `phase1_gate.py :35-39` 行号, 无关。

### [6b] 探针贴出脚本拒绝能力 (坏输入跑在 `r3a4/adv/` 副本; 脚本只改 `ROOT` / `Y` 两个路径常量, extras 段 `sys.path` 指回真仓 state-scanner)

坏输入 v2 = 当前 yaml 的 `execution_order` 第 3 行 `[串行 (同文件 tests/test_sibling_spec_probe.py), RED] TASK-005` → `[并行, RED] TASK-005` (R2 同款); v3 = 第 1 行 `TASK-001 (…) ‖ TASK-002 (…) 可并行 (不同文件); TASK-003 (…) ← 002 (…)` → `TASK-001 (…); TASK-002 (…) ‖ TASK-003 (…) 可并行 (不同文件)` (保留 003 ← 002 的 deps 边, 只改自述 = 「有边却标并行」)。输出 (只截 (e) / RESULT 行):

```
===== 坏输入 v2 =====
(e) parallel line ['TASK-001', 'TASK-002', 'TASK-003']: same-file pairs = none
(e) parallel line ['TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']: same-file pairs = [('TASK-005', 'TASK-006'), ('TASK-005', 'TASK-007'), ('TASK-005', 'TASK-008'), ('TASK-005', 'TASK-009'), ('TASK-006', 'TASK-007'), ('TASK-006', 'TASK-008'), ('TASK-006', 'TASK-009'), ('TASK-007', 'TASK-008'), ('TASK-007', 'TASK-009'), ('TASK-008', 'TASK-009')]
RESULT: FAIL (e) [('TASK-005', 'TASK-006'), ('TASK-005', 'TASK-007'), ('TASK-005', 'TASK-008'), ('TASK-005', 'TASK-009'), ('TASK-006', 'TASK-007'), ('TASK-006', 'TASK-008'), ('TASK-006', 'TASK-009'), ('TASK-007', 'TASK-008'), ('TASK-007', 'TASK-009'), ('TASK-008', 'TASK-009')]
exit=1
===== 坏输入 v3 =====
(e) parallel line ['TASK-001', 'TASK-002', 'TASK-003']: same-file pairs = none
RESULT: PASS
exit=0
```

### [7] 杂项 — TASK-003 只读计数 (勘正本席 R2「19 行」) / 母三处陈旧句 / 探针 :25 子句 / TASK-018 委派宿主 / linked 叠字

脚本 `s7_misc.py`:

```python
#!/usr/bin/env python3
"""R3/A4 [7] 杂项: TASK-003 只读计数 (:265 出入 #5 核对, 并勘正本席 R2 的「19 行」) / a1 tasks.md :232/:455 / sibling :25 / TASK-018 委派句 / linked 「新增 新 eval」."""
import re,yaml
A="/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/"
raw=open(A+"detailed-tasks.yaml",encoding="utf-8").read()
b=re.search(r"  - id: TASK-003\n(.*?)(?=\n  - id: TASK-|\Z)", raw, re.S).group(1)
dl=[l for l in b.split("deliverables:")[1].split("verification:")[0].splitlines() if l.strip().startswith("- ")]
print(f"TASK-003 deliverables 行={len(dl)}; 含「只读」={sum('只读' in l for l in dl)} ({[l.strip().split()[1] for l in dl if '只读' in l]})")
md=open(A+"tasks.md",encoding="utf-8").read().splitlines()
for n in (232,265,455): print(f"a1 tasks.md :{n} ->", md[n-1][:150].replace("\n"," "), "…")
print("a1 tasks.md :265 含「未标只读」:", "未标只读" in md[264])
T={t["id"]:t for t in yaml.safe_load(open(A+"detailed-tasks.yaml",encoding="utf-8"))["tasks"]}
print("a1 TASK-018 verification 委派句:", [v[:120] for v in T["TASK-018"]["verification"] if "TASK-025" in v and "幂等" in v])
smd=open("/home/dev/Aria/openspec/changes/sibling-spec-probe/tasks.md",encoding="utf-8").read().splitlines()
seg=smd[24].split("1.3 (TASK-003)")[1][:130]; print("sibling tasks.md :25 「1.3 (TASK-003) …」节选:", seg)
clause=smd[24].split("1.3 (TASK-003)")[1].split("; 2.x")[0]
print("sibling tasks.md :25 TASK-003 子句含 TASK-004:", "TASK-004" in clause, "| 子句列的边:", re.findall(r"TASK-\d{3}(?: / \d{3})*", clause), "| :11 含「只剩第 1 组 (三任务不同文件)」:", "只剩第 1 组 (三任务不同文件)" in smd[10])
print("sibling tasks.md :309 已知限尾句含「主控已追记加边」:", "主控已追记加边" in smd[308])
L=open("/home/dev/Aria/openspec/changes/linked-issue-field-availability/detailed-tasks.yaml",encoding="utf-8").read()
print("linked yaml 「新增 新 eval」出现次数:", L.count("新增 新 eval"))
```

输出 (逐字):

```
TASK-003 deliverables 行=16; 含「只读」=2 (['aria/skills/state-scanner/scripts/phase1_gate.py', 'aria/skills/state-scanner/scripts/release_gate.py'])
a1 tasks.md :232 -> - **Phase A.3**: 无需新 Agent — 既有 roster `backend-architect` (lib / CLI) · `qa-engineer` (红测 / 结构测试 / AB) · `knowledge-manager` (SKILL.md / references / …
a1 tasks.md :265 -> 5. 同文件核验 (a) 的排除规则: deliverable 注释含「只读」或路径以 `/` 结尾 (`docs/handoff/` 追加型宿主, TASK-001/002/036/039 共用) 不计为写入方; 为此把 TASK-002 三条存在性断言的注释补了「只读」字样。TASK-003 ( …
a1 tasks.md :455 -> 解析器: PyYAML `safe_load` 通过; `aria/skills/state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_tasks` ⇒ `parse_ok=True`, 39 tasks, status 集合 `{p …
a1 tasks.md :265 含「未标只读」: True
a1 TASK-018 verification 委派句: ['正常委派路径 (phase-a-planner → spec-drafter) 下幂等谓词使只写一条 claim: 由 TASK-025 (SC-22 (3) 幂等谓词结构测试) 验; TASK-035 fixture (a) 的「一次 A.1']
sibling tasks.md :25 「1.3 (TASK-003) …」节选:  是 B.1 前置 (proposal :473 逐字: 「该任务未 done 则 Phase B.1 不得开始」; 边: TASK-015 / 016 / 017 `dependencies` 各含 TASK-003, 主控裁量落第 4/5 组); 2.x 
sibling tasks.md :25 TASK-003 子句含 TASK-004: False | 子句列的边: ['TASK-015 / 016 / 017', 'TASK-003'] | :11 含「只剩第 1 组 (三任务不同文件)」: True
sibling tasks.md :309 已知限尾句含「主控已追记加边」: True
linked yaml 「新增 新 eval」出现次数: 1
```

TASK-025 verification 第 3 条 (yaml, 圈码改写): 「(3) 切片内逐字 `check: coordination ref 内按 (container_id, session_id) 定位到本 session 的 active claim` 且含 `claims/`; (4) 切片内**不含** `--phase B`; (6) …」— 即 proposal SC-22 (3)「保证正常委派路径上只写一条 claim」的结构断言宿主; TASK-018 verification 改指它成立。

### [8] R2 → R3 六份 diff (基线 = 本席 R2 scratch 副本; 三份 tasks.md 副本 sha256 与 R2 [0] 逐字相等, 三份 yaml 副本各含 1 处本席 R2 坏输入改动, 已在下方标出剔除)

```
== linked-issue-field-availability/tasks.md: hunks=0 +0 -0  (R2 lines=320 R3 lines=320)
== linked-issue-field-availability/detailed-tasks.yaml: hunks=7 +8 -8  (R2 lines=724 R3 lines=724)
== sibling-spec-probe/tasks.md: hunks=7 +40 -6  (R2 lines=275 R3 lines=309)
== sibling-spec-probe/detailed-tasks.yaml.v1: hunks=3 +4 -4  (R2 lines=620 R3 lines=620)
== a1-entry-claim-duplicate-work-guard/tasks.md: hunks=7 +11 -6  (R2 lines=466 R3 lines=471)
== a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml: hunks=9 +29 -5  (R2 lines=995 R3 lines=1019)
```

a1 yaml (hunk `@@ -688` 的 `TASK-025 deps 含 TASK-017` 是本席 R2 坏输入, 剔除; 其余 8 hunk = R2 fix):

```
--- R2/detailed-tasks.yaml
+++ R3/detailed-tasks.yaml
@@ -22 +22 @@
-  total_tasks: 39
+  total_tasks: 40
@@ -24 +24 @@
-  estimated_hours: "94-153"
+  estimated_hours: "97-158"
@@ -553 +553 @@
-      - "正常委派路径 (phase-a-planner → spec-drafter) 下幂等谓词使只写一条 claim: 由 TASK-035 fixture (a) 的「一次 A.1 两条 claim」坏臂验"
+      - "正常委派路径 (phase-a-planner → spec-drafter) 下幂等谓词使只写一条 claim: 由 TASK-025 (SC-22 (3) 幂等谓词结构测试) 验; TASK-035 fixture (a) 的「一次 A.1 两条 claim」坏臂为行为层补充 (R2/A1 minor: SC 映射里该臂宿主是 TASK-025)"
@@ -688 +688 @@
-    dependencies: [TASK-001, TASK-003, TASK-017]   # 与 Group 2 同款 (R1/A3 bd55ab9c 处方 (a)); 不再依赖 TASK-017/018 — 它们反过来依赖本任务
+    dependencies: [TASK-001, TASK-003]   # 与 Group 2 同款 (R1/A3 bd55ab9c 处方 (a)); 不再依赖 TASK-017/018 — 它们反过来依赖本任务
@@ -830,0 +831 @@
+      - "运行前置 (Rule #7 射程 + R1 C5): 会话以 `ARIA_COORDINATION_NO_PUSH=1 claude …` 启动 (AB_TEST_OPERATIONS.md:222-228), transcript 核验 `push_skipped: true` — R2/A4 残留补"
@@ -850,0 +852 @@
+      - "运行前置 (Rule #7 射程 + R1 C5): 会话以 `ARIA_COORDINATION_NO_PUSH=1 claude …` 启动 (AB_TEST_OPERATIONS.md:222-228), transcript 核验 `push_skipped: true` — R2/A4 残留补"
@@ -892,0 +895 @@
+      - "运行前置 (Rule #7 射程 + R1 C5): 会话以 `ARIA_COORDINATION_NO_PUSH=1 claude …` 启动 (AB_TEST_OPERATIONS.md:222-228), transcript 核验 `push_skipped: true` — R2/A4 残留补"
@@ -952,0 +956,21 @@
+  - id: TASK-040
+    parent: "8.4"
+    task_group: 8
+    title: "aria 子模块本地 merge → master + 双推 + 逐 remote ls-remote 核验 + tag (硬约束 1/2 的任务宿主)"
+    status: pending
+    complexity: M
+    estimated_hours: "3-5"
+    agent: tech-lead
+    reason: "多远程 / 跨仓指针协调 (AGENT_MAPPING: cross-module, integration → tech-lead); 硬约束 1/2 的执行责任 (R2/A1 3221f943: 此前只活在 notes 散文里, 无任务宿主 — #165 那条腿)"
+    dependencies: [TASK-037]
+    deliverables:
+      - aria   # 子模块 master: 本地 `git -C aria merge --no-ff feature/<branch>` (禁 Forgejo 服务端合并, CLAUDE.md 硬约束 1) + `git -C aria tag v<vNEXT>`
+    verification:
+      - "合并在本地做: `git -C aria log -1 --format=%P master` 有两个父 (merge commit 本地生成), Forgejo PR 页面若存在只作审阅, 不点 Do: merge"
+      - "双推给足超时: `git -C aria push origin master --tags && git -C aria push github master --tags` (memory partial-push: 命令超时 ≥ 300s)"
+      - "推后逐个核验, 不信 push 回执: `git -C aria ls-remote origin master` / `git -C aria ls-remote github master` / `git -C aria rev-parse master` 三者 SHA 逐字节相等; tag 同法 (`ls-remote --tags`); ls-remote 自身失败 ⇒ 重试再下结论 (CLAUDE.md 硬约束 2)"
+      - "两 remote 一致后才允许 TASK-038 bump 主仓 gitlink (否则 orphaned gitlink, GitHub clone --recursive 断裂, 2026-07-14 事故形状)"
+    notes: >
+      R2/A1 残留 major: 字段 Spec 有 TASK-022、探针 Spec 落 TASK-018, 母 Spec 缺此宿主而 TASK-038 却断言「gitlink SHA 在两 remote 均可取到」
+      (断言了无人执行的动作的后置条件)。本任务补齐; 版本号沿 <vNEXT> 占位, 档位待 owner (TASK-037 notes 统一句)。
+
@@ -962 +986 @@
-    dependencies: [TASK-037]
+    dependencies: [TASK-037, TASK-040]   # TASK-040 = aria 子模块双推核验一致后才 bump gitlink (R2/A1)
```

a1 tasks.md (7 hunk):

```
--- R2/tasks.md
+++ R3/tasks.md
@@ -91,0 +92 @@
+- [ ] 8.4 aria 子模块本地 merge → master + 双推 + 逐 remote `ls-remote` 核验 + tag (CLAUDE.md 硬约束 1/2 的任务宿主; 两 remote 一致后才做 8.2 gitlink bump) — R2/A1 3221f943 残留补
@@ -393 +394,4 @@
-    scs = re.findall(r"SC-(\d+)", cells[0]); ts = re.findall(r"TASK-\d{3}", cells[3])
+    scs = re.findall(r"SC-(\d+)", cells[0])
+    ts = []  # 展开 `TASK-013/014` 缩写 (R2/A4 minor 9db42f0a)
+    for m in re.finditer(r"TASK-(\d{3})((?:/\d{3})*)", cells[3]):
+        ts.append(f"TASK-{m.group(1)}"); ts += [f"TASK-{x}" for x in m.group(2).split("/") if x]
@@ -418 +422 @@
-输出 (逐字, exit 0):
+输出 (逐字, exit 0; R2 后重跑 2026-08-30: TASK-003 只读标注 + TASK-040 + (d) 缩写展开后):
@@ -421 +425,2 @@
-[a] 同文件写入对 40 对 (共写文件 19 个) — 全部有边: True
+[a] 同文件写入对 38 对 (共写文件 20 个) — 全部有边: True
+      aria: TASK-040 -> TASK-038
@@ -436 +441 @@
-      aria/skills/state-scanner/scripts/phase1_gate.py: TASK-003 -> TASK-014 -> TASK-015 -> TASK-016
+      aria/skills/state-scanner/scripts/phase1_gate.py: TASK-014 -> TASK-015 -> TASK-016
@@ -444 +449 @@
-[d] 覆盖表 (SC, TASK) 对 51; verification 无 token 的对: []
+[d] 覆盖表 (SC, TASK) 对 55; verification 无 token 的对: []
@@ -446 +451 @@
-[+] total_tasks=39 (metadata 39); parent 唯一=True; parent ⊆ tasks.md 编号=True; 编号数=39
+[+] total_tasks=40 (metadata 40); parent 唯一=True; parent ⊆ tasks.md 编号=True; 编号数=40
```

sibling yaml (hunk `@@ -224` 的 `TASK-005 deps 少 TASK-001` 是本席 R2 坏输入, 剔除; 其余 2 hunk = R2 fix):

```
--- R2/detailed-tasks.yaml.v1
+++ R3/detailed-tasks.yaml.v1
@@ -40 +40 @@
-    - "TASK-003 done: aria-plugin-benchmarks/ab-suite/audit-engine.json 存在, 含 α/β 两 eval (proposal :473 逐字「该任务未 done 则 Phase B.1 不得开始」; 建不成 ⇒ 上呈 owner, 不自判豁免)。上游边: TASK-015 / 016 (指令面接线) 与 TASK-017 (AB 实跑) 的 dependencies 各含 TASK-003 (R1 C1 第 3 条, 主控裁量落第 4/5 组)"
+    - "TASK-003 done: aria-plugin-benchmarks/ab-suite/audit-engine.json 存在, 含 α/β 两 eval (proposal :473 逐字「该任务未 done 则 Phase B.1 不得开始」; 建不成 ⇒ 上呈 owner, 不自判豁免)。上游边: TASK-004 (第 2 组起点, proposal :473 逐字, 主控 R1 追记) 与 TASK-015 / 016 (指令面接线) / TASK-017 (AB 实跑) 的 dependencies 各含 TASK-003 (R1 C1 第 3 条)"
@@ -224 +224 @@
-    dependencies: [TASK-004]                                  # 同文件串行链首 (R1 C1); TASK-001 = 硬前置边
+    dependencies: [TASK-001, TASK-004]                                  # 同文件串行链首 (R1 C1); TASK-001 = 硬前置边
@@ -582,2 +582,2 @@
-  - "[并行, 不同文件] TASK-001 (硬前置断言, 阻塞门) · TASK-002 (基线三态, 只读观测) · TASK-003 (AB 套件文件, B.1 前置)"
-  - "TASK-004 (测试骨架 + SC-21)  ← 001, 002"
+  - "TASK-001 (硬前置断言, 阻塞门) ‖ TASK-002 (基线三态, 只读观测) 可并行 (不同文件); TASK-003 (AB 套件文件, B.1 前置) ← 002 (主控 R1 追记: 002 断言「无 audit-engine.json」须先于 003 建文件)"
+  - "TASK-004 (测试骨架 + SC-21)  ← 001, 002, 003 (003 = B.1 前置, proposal :473 逐字, 主控 R1 追记)"
```

sibling tasks.md (7 hunk; :145 一行只是行尾字节差异, `@@ -234/-245/-250` 三行 = 去转义, `@@ -258` = 贴文标题, `@@ -261` = 重贴 34 行 OK, `@@ -275` = 已知限尾句):

```
--- R2/tasks.md
+++ R3/tasks.md
@@ -145 +145 @@
-| a257ffa4 (A1) | A1 · critical | **closed** — TASK-018 发布同步面补齐主仓 `VERSION` / `README.md` / i18n ×3 / gitlink `aria`, 「不重译」改为「正文不重译, 标记与两处版本串必改」, 两条 check 改为「全部文件完成后才断言绿」 | yaml TASK-018 deliverables (13 项, 与字段 TASK-024 12 点 + `086ee32` 7 文件对齐) + verification 4 条 + notes; tasks.md 5.2 / Impact 对账表  …
+| a257ffa4 (A1) | A1 · critical | **closed** — TASK-018 发布同步面补齐主仓 `VERSION` / `README.md` / i18n ×3 / gitlink `aria`, 「不重译」改为「正文不重译, 标记与两处版本串必改」, 两条 check 改为「全部文件完成后才断言绿」 | yaml TASK-018 deliverables (12 项, 与字段 TASK-024 12 点 + `086ee32` 7 文件对齐) + verification 4 条 + notes; tasks.md 5.2 / Impact 对账表  …
@@ -234 +234 @@
-        ts = re.findall(r"TASK-\\d{3}", line)
+        ts = re.findall(r"TASK-\d{3}", line)
@@ -245 +245 @@
-md_ids = re.findall(r"^- \\[[ x]\\] (\\d+\\.\\d+) ", MD.read_text(encoding="utf-8"), re.M)
+md_ids = re.findall(r"^- \[[ x]\] (\d+\.\d+) ", MD.read_text(encoding="utf-8"), re.M)
@@ -250 +250 @@
-HRS_RE = re.compile(r"\\d+-\\d+")
+HRS_RE = re.compile(r"\d+-\d+")
@@ -258 +258 @@
-**输出 (清账后, 2026-08-30)** — 34 对同文件全部有边 (`OK` 行略, 覆盖 test 文件 2.1~2.6→3.5 / script 文件 3.1~3.5 / TASK-002 观测目标→4.1/4.2 / TASK-003→5.1):
+**输出 (清账后, 2026-08-30)** — R2 后重跑 (2026-08-30, 转义修正 + 主控追记两条边后), 逐字:
@@ -261,0 +262,34 @@
@@ -275 +309 @@
-**已知限 (诚实声明)**: (a) 按 deliverables **路径逐字相等**判同文件; TASK-002 的观测目标 `aria-plugin-benchmarks/ab-suite/` (目录) 与 TASK-003 新建的 `ab-suite/audit-engine.json` 路径不等 ⇒ 不触发, 但 TASK-002 verification 断言「无 `audit-engine.json`」在 TASK-003 先跑时会红 —— 第 1 组「并行」在此语义上有时序依赖, 已上报主控 (未自行加边)。
+**已知限 (诚实声明)**: (a) 按 deliverables **路径逐字相等**判同文件; TASK-002 的观测目标 `aria-plugin-benchmarks/ab-suite/` (目录) 与 TASK-003 新建的 `ab-suite/audit-engine.json` 路径不等 ⇒ 不触发, 但 TASK-002 verification 断言「无 `audit-engine.json`」在 TASK-003 先跑时会红 —— 第 1 组「并行」在此语义上有时序依赖, 主控已追记加边 TASK-003 ← TASK-002 (见「主控追记」段))。
(+34 行「TASK-xxx -> TASK-yyy  OK  [...]」贴文新增行略, 与本席 [2] 亲跑一致)
```

linked yaml (hunk `@@ -465` 的 `TASK-017 deps 少 TASK-016` 是本席 R2 坏输入, 剔除; 其余 6 hunk = R2 fix: eval id 3 → `max(id)+1` ×5, TASK-024 12 → 14 点):

```
--- R2/detailed-tasks.yaml
+++ R3/detailed-tasks.yaml
@@ -459 +459 @@
-    title: "可证伪定向 fixture ×1 (SC-7 双臂) — spec-drafter.json 新增 eval id 3 (中文臂); 英文臂 = 更新后的 eval id 2"
+    title: "可证伪定向 fixture ×1 (SC-7 双臂) — spec-drafter.json 新增 新 eval (id = ship 时 max(id)+1, 今日观测 3) (中文臂); 英文臂 = 更新后的 eval id 2"
@@ -465 +465 @@
-    dependencies: [TASK-014, TASK-015]   # +TASK-016: 同写 ab-suite/spec-drafter.json 与 ab-results 子目录, 串行 (R1/C1+C5, A1 35dad35d)
+    dependencies: [TASK-016, TASK-014, TASK-015]   # +TASK-016: 同写 ab-suite/spec-drafter.json 与 ab-results 子目录, 串行 (R1/C1+C5, A1 35dad35d)
@@ -471,2 +471,2 @@
-      - "eval id 3 prompt (中文): 请 spec-drafter 为一个无关联 issue 的小功能新建 Level 2 proposal; expectations 锚定 SC-7: 头部含一条过 E0+E2+E5 的 `> **Linked Issue**:` 行 / 无关联逐字 ``none`` / 不写 markdown 链接形 / 不留空 / 不译写成别的字段名"
-      - "双臂 = eval id 3 (中文) + eval id 2 (英文, TASK-016 更新后) — 裁量 2; 两臂各自对 baseline (aria @ d69091d, 无 hunk A/B) 与新版实跑; 会话同 TASK-016 以 `ARIA_COORDINATION_NO_PUSH=1` (等价 `--no-push`) 启动"
+      - "新 eval (id = ship 时 max(id)+1, 今日观测 3) prompt (中文): 请 spec-drafter 为一个无关联 issue 的小功能新建 Level 2 proposal; expectations 锚定 SC-7: 头部含一条过 E0+E2+E5 的 `> **Linked Issue**:` 行 / 无关联逐字 ``none`` / 不写 markdown 链接形 / 不留空 / 不译写成别的字段名"
+      - "双臂 = 新 eval (id = ship 时 max(id)+1, 今日观测 3) (中文) + eval id 2 (英文, TASK-016 更新后) — 裁量 2; 两臂各自对 baseline (aria @ d69091d, 无 hunk A/B) 与新版实跑; 会话同 TASK-016 以 `ARIA_COORDINATION_NO_PUSH=1` (等价 `--no-push`) 启动"
@@ -483 +483 @@
-    title: "套件缺口 issue — 归并 aria-plugin#117 (评论追加本 Spec 为第二实例 + eval id 3 登记)"
+    title: "套件缺口 issue — 归并 aria-plugin#117 (评论追加本 Spec 为第二实例 + 新 eval (id = ship 时 max(id)+1, 今日观测 3) 登记)"
@@ -493 +493 @@
-      - "A.2 裁量 (owner 可改判): **不新开** issue; 用 `forgejo POST /repos/10CG/aria-plugin/issues/117/comments` 追加评论: (1) 第二实例 = spec-drafter authoring 时是否写出必填字段 `Linked Issue` (Spec linked-issue-field-availability rule6_note 第三格); (2) 首条已落地 authoring fixture = ab-suite/spec-drafter.json eval id 3 (TASK-0 …
+      - "A.2 裁量 (owner 可改判): **不新开** issue; 用 `forgejo POST /repos/10CG/aria-plugin/issues/117/comments` 追加评论: (1) 第二实例 = spec-drafter authoring 时是否写出必填字段 `Linked Issue` (Spec linked-issue-field-availability rule6_note 第三格); (2) 首条已落地 authoring fixture = ab-suite/spec-drafter.json 新 eval (id = ship …
@@ -496 +496 @@
-      - "RESULT.md 「逐 hunk 处置表」覆盖外格写明: 点名行为 SC-7 ✓ / 定向 fixture eval id 3 ✓ / 套件缺口 issue #117 (归并) ✓ — 三件齐"
+      - "RESULT.md 「逐 hunk 处置表」覆盖外格写明: 点名行为 SC-7 ✓ / 定向 fixture 新 eval (id = ship 时 max(id)+1, 今日观测 3) ✓ / 套件缺口 issue #117 (归并) ✓ — 三件齐"
@@ -627 +627 @@
-      - "12 个引用点全部改为 ship 号 <vNEXT> (owner 裁定规则见 TASK-021 notes; 行号按 c120f9e 实读, 落地时以 grep 为准); `grep -rn '1\\.67\\.2' VERSION README.md README.*.md` 零命中"
+      - "14 个引用点 (与 086ee32 同口径: CLAUDE.md:139/:141 + VERSION + README.md:8/:242 + i18n ×3 各 :3/:10/:244) 全部改为 ship 号 <vNEXT> (owner 裁定规则见 TASK-021 notes; 行号按 c120f9e 实读, 落地时以 grep 为准); `grep -rn '1\\.67\\.2' VERSION README.md README.*.md CLAUDE.md` 零命中"
```

由 R2 fix 引入占比的计法: 六条 finding 逐条问「R2 版本里这个矛盾在不在」— 09795e71 (块序) / 64cf8dd9 (39 ×2) / e9ffaefe (12 vs 14) 在 R2 版本不存在 ⇒ 3 条 fix 引入; 1a45ef41 (TASK-037 deps 未变) / 10e7cea4 (:25 在 R2 版本已陈旧) / 199aa25c (R2 已报, 未修全) ⇒ 3 条残留或 partial。

### [9] 审后 sha256 复核 (2026-08-31T13:56:02.572Z; 与 [0] 逐行一致)

```
d5b1429e030a2e8e5cffdcdab53ca408aa92e8e3d00ce2e4b63363db64281250  openspec/changes/linked-issue-field-availability/tasks.md
824c6a11db6a0cfc598e278c3b155225df16eeaa22ec5f10a364cae053c3cb72  openspec/changes/linked-issue-field-availability/detailed-tasks.yaml
2de1da5716d8e219d9454763c962596611880594d7252403eb207fc6d5946574  openspec/changes/sibling-spec-probe/tasks.md
26beac498ed367d1aee47a726c8c3defa0d6dcf1ee4ceaeddf10c00c242889d8  openspec/changes/sibling-spec-probe/detailed-tasks.yaml
b83cc8d3496c61c7c4d09db1bbcb9fa31469d96b7a642667d879841b10e0e81f  openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md
99a9baeaa6d10d105890ca7c7a1e8a799af00de196f384092109bebf460f7161  openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml
```

finding id 生成串 (sha256(...)[:8]):

```
1a45ef41  implementation:openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml#TASK-037:major:issue
09795e71  implementation:openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml#TASK-040:minor:issue
64cf8dd9  documentation:openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md#L232,L265,L455:minor:issue
199aa25c  implementation:openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml#TASK-034:minor:issue
e9ffaefe  documentation:openspec/changes/linked-issue-field-availability/tasks.md#5.5:minor:issue
10e7cea4  documentation:openspec/changes/sibling-spec-probe/tasks.md#L25:minor:issue
```

(scope 带 `#锚点` 是为了与 R1/R2 同 scope 的旧 id 区分 — 不带锚点时 a1 tasks.md minor 会再次算出 R2 的 9db42f0a、linked / sibling tasks.md minor 会算出 R1 的 62285020 / 4bf32c17, 聚合时会串。)

## Verdict

**PASS_WITH_WARNINGS** (0 critical / 1 major / 5 minor)。计划本体在机械层继续收敛: R2 四簇里本席 scope 的三条 2 closed + 1 partial, 三份贴文与实跑逐行相等, 依赖图无环无悬空、自述与边一致。唯一 major 是发布链漏一条上游边 (TASK-037 ↛ TASK-009), 是残留非 fix 引入, 一 token 可闭; 5 条 minor 全是文本层同步 (块序 / 三处计数句 / 一处字面 / 一处 12-vs-14 / 一处组间门子句), 各一行到几行, 不触 proposal、不改编号、不改 SC。

## Vote

**REVISE (定点, 6 处; 不需 R4 全席)**。理由: (a) R2 本席 finding 2/3 closed + 1 partial (034 一行), 无 not_addressed; (b) 本轮 fix 引入占比 3/6, 恰在 1/2 拐点 (memory `marginal-return-negative`), 且三条 fix 引入的全是「改了一处没扫兄弟位置」的文本同步 (memory `fix-the-class`), 再开通用轮只会审到更多同形; (c) 但 1a45ef41 是依赖图本体的发布链缺边 (与 R1 主簇同维度), 不能以「一 token」之名 PASS 掉 — 它恰是 R1/R2 五席 × 2 轮都没问的方向 (向上可达查了, 向下到发布链没查); (d) 建议主控收账方式 = 执笔席落 6 处定点改动后**定向复核**: 重跑本席 `chk1_battery.py` (a1 应回到 `seq_equal=True`) + `s3_task040.py` (「不在 anc(TASK-040) 的」应为 `[]`) + `s4_flags_summary.py` (034 两字面 Y) + `s7_misc.py` (:232/:455 无 39, :25 子句含 TASK-004) + 三份贴出脚本 exit 0 且贴文与亲跑一致 — 五件全绿即可判本席 scope 收敛, 不必再派五席。
