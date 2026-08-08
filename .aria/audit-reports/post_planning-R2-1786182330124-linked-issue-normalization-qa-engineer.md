---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-08T09:45:30.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — qa-engineer 审计报告

## 审计对象与方法

对比 R1 (`a52ab81`, 17 任务) 与 R1-fix (`3fc6f3f`, 21 任务): 实读 `tasks.md` (136 行)、`detailed-tasks.yaml` (662 行)、`git diff a52ab81 3fc6f3f -- detailed-tasks.yaml` 全量 hunk、R1-fix commit message。逐条核我自己 R1 的 2 Major + 2 Minor 是否真闭合 (读实际文本, 非读 commit message 自陈)。对新增 TASK-018~021 做同等严格度的「它怎么会红?」审查。**实跑** TASK-020 的 grep 命令与 yaml 底部派生值重算命令 (只读, 不改任何文件), 并用脚本核验 DAG 无环/无悬空依赖/同文件任务全部有序。

## Part 1 — R1 四条闭合核验

### Major-1 (`Ran ≥1367` 混淆场景数与 Ran 计数) — **CLOSED**

`metadata.test_counting_contract` (yaml:64-79) 新增, 显式区分 `scenario_count: 45` (人工语义计数) 与 `ran_n_counts`("test 方法数 — 一个方法可含多个场景"), 并把验收拆成两条正交判据: 「场景齐备性 = 逐 SC 清单核对」+「回归 = run_tests.py OK 且 0 failures/errors」。TASK-001~006 verification 逐条从 `子用例 ≥N` 改写为 `场景数 ≥N ... 不用 Ran 数换算` (diff 逐条核对确认全部 6 处都改)。TASK-014 (5.1) 同步改写, 且全文再无 "Ran ≥1367" 作为活判据出现 (仅 2 处历史叙述引号引用, 见下方证据)。

**核「这两条各自怎么会红」**:
- 「回归」条: 命令+期望输出都是字面量, 机械可证伪。
- 「场景齐备性」条: **仍是人工逐条核对, 无机械 backstop** —— 这是比"Ran 换算"更正确但仍非全自动的判据 (详见 Part 2-B, 记为新的轻量级发现, 非阻塞)。

```
$ grep -n "1367" tasks.md detailed-tasks.yaml
detailed-tasks.yaml:73:      ⛔ 验收不得用 `Ran N` 数换算场景数 (原写 "Ran ≥1367" = 1322+45 预设 1 场景 = 1 方法,
detailed-tasks.yaml:459:      ⛔ 不得用 `Ran N` 换算场景数 (首版写 "Ran ≥1367" 被三席同时命中)。
```
两处均为带引号的历史叙述 (说明"首版曾经这样写、现在不这样"), 不是活判据。**判定: closed**。

### Major-2 (「9 处落点」vs 自身分解 11) — **CLOSED, 独立复核数字吻合**

fix 改口径为「版本引用点」而非「文件数」, `metadata.version_reference_surface.main_repo_points: 14`, breakdown 逐文件给出 (README.md:2 / zh:3 / ja:3 / ko:3 / CLAUDE.md:2 / VERSION:1 = 14)。**实跑** TASK-020 (5.7) 的零命中断言语句 (提前跑, 只读):

```
$ grep -rn "1\.65\.5" README.md README.zh.md README.ja.md README.ko.md CLAUDE.md VERSION \
    aria/.claude-plugin/plugin.json aria/.claude-plugin/marketplace.json aria/VERSION aria/README.md
```
主仓 6 个文件 (README.md/zh/ja/ko/CLAUDE.md/VERSION) 命中数逐文件为 **2/3/3/3/2/1 = 14**, 与 `version_reference_surface.breakdown` **逐文件精确吻合**, 独立验证非抄述。全文再无 "9 处" 作为落点总数出现 (唯一残留的 "9" 在 TASK-018 verification `"共 9 处"` = i18n ×3 文件 × 每份 3 处 = 9, 这是自洽的**子集**计数, 与 R1 那条错误的「9 处落点」总数无关, 不是同一处遗留)。**判定: closed**。

### minor-1 (TASK-007「建议按此顺序书写」混入 verification) — **CLOSED**

verification 列表原文里的措辞已改写为 `"归一 = 每段 strip → repo_basename 内 ./_ → - 译码 → casefold() 三步复合"` (陈述三步组成, 不带「建议」字样); 「顺序不影响结果」的论证与「首版把这句话混进 verification 是不可证伪措辞」的自我诊断被移入 notes 段, 以第三人称回顾方式呈现 (`已移入本 notes 作为 review 便利建议`)。全文 grep `建议按此顺序` 只剩 1 处, 且是这句回顾性叙述本身 (引号内), 非活判据。

残留软点 (不构成独立发现, 记在此供参考): verification 里那条箭头记法本身仍是「strip → 译码 → casefold」的顺序书写, 若审阅者只读 verification 不读 notes, 仍可能读成"要求这个顺序"; notes 里"顺序不影响结果"的澄清与它物理分离。这是表达清晰度的边际问题, 不是原 minor-1 指控的那种"不可证伪判据混入"结构性问题 —— 原问题已解决。**判定: closed**。

### minor-2 (1.6 反向依赖只在 yaml notes, 人读层无提示) — **CLOSED**

`tasks.md:56` 现有:
```
- [ ] 1.6 SC-12 — 导出单元返回契约: ... (3)
      > ⚠️ 本条是组 1→组 2 RED-first 排序的唯一例外: 依赖 2.1 (被测函数在此之前不存在)。
```
人读层已有提示, 与 `Group Overview` 段 (`tasks.md:39`) 的 "例外: 1.6 (SC-12) 反向依赖 2.1" 呼应, 双处一致。**判定: closed**。

**Part 1 小结**: 我 R1 的 4 条 (2 Major + 2 Minor) **全部 closed**, 且 Major-2 用独立实跑数据核验非抄述, Major-1 的两条正交判据本身可各自独立评估"它怎么会红"。

---

## Part 2 — 新发现 (R2, 均 `new`)

- type: issue
  severity: minor
  category: testing
  scope: detailed-tasks.yaml TASK-021 (parent 5.8)
  new_or_carryover: new
  summary: 「(a) 加 post-implementation 模式 / (b) 显式退役」二选一的验收条件本身是可证伪的 (两条分支各自有明确判据), 但分支 (b) 的「带 SHA 的存档报告」缺具体路径/命名/格式约定, 留出解读空间
  evidence: >
    verification 原文: "(b) 显式退役: baseline 结果冻结成带 SHA 的存档报告, 脚本移出 .aria/repro/。
    无论哪条, substitute 论证的可复核性必须仍然成立 (指向一个可执行或带 SHA 的存档)"。
    对照脚本本体 (`.aria/repro/sc-baseline-linked-issue-normalization.py:277`) 的实际逻辑:
    它比较 `measured_face`(实测红集合) 与 `EVIDENCE_FACE`(声称红集合), 不等则 `sys.exit(1)`。
    走 (a) 需要新增一个显式模式让 `EVIDENCE_FACE` 反映"实现后应转绿", 这是具体、可实现、
    可通过重跑验证的 (exit 0 即通过) —— 这条分支验收扎实。但走 (b) 时, "存档报告" 没有
    规定落在哪 (`.aria/audit-reports/`? 内联进 audit-trail? 新建独立文件?), "带 SHA" 没有
    规定是脚本文件末次修改 SHA、collision.py 落地 SHA、还是归档 commit SHA。审阅者拿到
    交付物后, 无法机械判断"是否满足 (b) 的要求", 只能靠主观印象。
  recommendation: >
    为 (b) 补一句具体路径与 SHA 语义, 如: "存档报告写入
    .aria/audit-reports/sc-baseline-linked-issue-normalization-archived-<merge-SHA>.md,
    内容 = 本脚本 2026-08-05/08-08 两次实测的完整输出 + 指向哪个 collision.py SHA 使其转绿"。
    不阻塞 Phase B, 建议在真正执行 TASK-021 前(它可在 TASK-009 后随时执行)补一句。

- type: issue
  severity: minor
  category: testing
  scope: detailed-tasks.yaml metadata.test_counting_contract; TASK-001~006 verification 首条
  new_or_carryover: new
  summary: Major-1 的修法(逐 SC 清单核对)严格优于原「Ran 换算」, 但「场景齐备性」判据本身仍无机械 backstop —— 审阅者只能靠人工比对 proposal SC 表与测试代码, 没有可 grep 的锚点
  evidence: >
    `test_counting_contract.rule` 原文: "场景齐备性判据 = 逐 SC 清单核对 17 条 SC 的场景全部
    落盘"。搜索既有测试文件 `test_release_by_track.py` 及 proposal.md, **未发现任何 SC-ID
    与测试代码的显式关联标记**(如内联注释 `# SC-1`), 即:

        $ grep -rn "# SC-\|SC-[0-9]" aria/skills/state-scanner/tests/test_release_by_track.py
        (无输出)

    这意味着"逐 SC 清单核对"目前只能靠审阅者阅读整段测试代码、凭语义判断每个断言对应
    proposal 表里的哪一条 SC, 而不是"grep SC-1 出现几次、和期望场景数比对"这种半机械
    核对。比原缺陷(单位错配导致假红/假绿)轻得多, 但仍是纯人工判据, 不满足
    memory `feedback_falsifiable_evidence_for_binary_acceptance` 的最高标准。
  recommendation: >
    建议(不阻塞): Phase B 实施 TASK-001~006 时, 每个场景断言前加内联注释 `# SC-1`/`# SC-1b`
    等, 使"逐 SC 清单核对"降级为可脚本辅助的 `grep -c "# SC-1" test_release_by_track.py`
    与该 SC 的场景数下界比对, 把审查负担从"通读代码"降到"数注释"。可留给 Phase B 实施者
    自行决定, 不必回 A.2 返工。

- type: observation
  severity: minor
  category: process
  scope: detailed-tasks.yaml metadata.file_domain_serialization["...test_release_by_track.py"]; TASK-001~005 dependencies
  new_or_carryover: neither (R2 首次审视, 内容并非 R1-fix 新引入 — 6 任务粒度在首版 A.3 已存在, R1-fix 只是把「建议串行」换成真依赖边使其可核验)
  summary: TG-1 六任务 (001→002→003→004→005 串行, 006 另挂在 007 之后) 是同一 agent (qa-engineer)、同一文件 (`test_release_by_track.py`)、无跨 agent 集成点、无中间 review checkpoint 的顺序写入; 串行化本身是对的(同文件必须有序, memory `feedback_workflow_partition_by_file_domain`), 但**拆成 5 个独立 task 而非 1 个「按 17 条 SC 逐条写测试」的复合 task** 是否过度切分, R1-fix 未重新评估
  evidence: >
    001~005 除 SC 覆盖范围外, task 结构(agent/deliverables/文件)完全相同, 依赖链是纯直线
    (无分支、无并行、无外部输入), 每个任务的"完成信号"只是"又插入了几个测试方法到同一
    文件", 没有独立的可交付边界(如不同 PR、不同 reviewer、不同 commit 时点的强制要求)。
    机械核验显示该链无环、无悬空依赖、任务粒度内部自洽(已用脚本核实), 所以**不是正确性
    缺陷**; 但 5 个"pending → in_progress → done"状态切换、5 次上下文加载, 相对"1 个
    task 内含 6 个 verification 子块(每块对应一个 parent 编号)"这种设计, 在**没有任何
    task 边界价值**(无并行、无跨 agent 交接)的前提下, 纯增加流程开销。
  recommendation: >
    不要求本轮返工(不是缺陷, 是设计选择, 且已过机械一致性检验)。留给 owner/task-planner
    参考: 未来同类「单 agent 单文件顺序写用例」场景, 可考虑用 1 个 task + 多个 verification
    子块表达, 而非 N 个强制串行的独立 task。仅供记录, 不计入本轮 Major/Critical。

## 派生值重算 (只读命令验证, 均通过)

```
$ python3 -c "import yaml,collections as c; t=yaml.safe_load(open('detailed-tasks.yaml'))['tasks']; \
  x=c.Counter(i['complexity'] for i in t); a=c.Counter(i['agent'] for i in t); \
  print(len(t),'tasks |',dict(x),'|',x['S']*3+x['M']*6+x['L']*10,'h |',dict(a))"
21 tasks | {'M': 6, 'S': 14, 'L': 1} | 88 h | {'qa-engineer': 9, 'backend-architect': 7, 'knowledge-manager': 5}
```
与 yaml 底部 footer 文本 (`S ×14 · M ×6 · L ×1 | ≈88h | qa-engineer×9 · backend-architect×7 · knowledge-manager×5`) **逐字段吻合** —— commit message 自陈的「footer 派生值连续两次写错」这次没有复发。额外核: 每个 task 的 `est_hours` 字段与其 `complexity` 映射 (S=3/M=6/L=10) 逐条核对**零不匹配**; 21 个 `id` 无重复; 21 个 `parent` 与 tasks.md 21 个 checkbox 一一对应; DAG 脚本核验**无环、无悬空依赖、同文件任务间无缺失的先后边** (collision.py 的 007/008/009/010 与 test_release_by_track.py 的 001..005 均已可达排序，无并行冲突对)。

17 条 SC 的场景分摊 13/5/15/8/1/3=45 在 fix 后**未被触碰** (R1-fix commit 只改了 tasks.md 与 detailed-tasks.yaml, 未碰 proposal.md); 独立重算仍为 45, 与 proposal.md:276 的下界推导行**逐条一致**, 无drift。

## TASK-020 零命中断言的鉴别力与覆盖完整性核验

正控验证 (只读, fix 前状态): 命令**当前会命中** 20 处 (6 个主仓文件共 14 处 + aria 相关 4 个文件共 6 处), 逐主仓文件命中数 (2/3/3/3/2/1) 与 `version_reference_surface.breakdown` 精确吻合 —— 该断言在当前(未 bump)状态下有区分力, bump 后归零才是真正完成。

覆盖完整性反查: 排查是否有"该歸零却未纳入清单"的版本史类文件误漏。确认 `aria/CHANGELOG.md` 正确不在 grep 清单内(它本身对 "1.65.5" 有真实命中, 若被纳入会造成永久假红, R1-fix 的排除是对的)。额外发现两个**未在清单内但确实含 "1.65.5"** 的文件: 主仓 `CHANGELOG.md`(项目自身版本号 1.7.x 序列, 全文查无 "1.65.5" 字面出现, 与 aria-plugin 版本无关, 无需纳入) 与 `.aria/triage-comment.md`/`.aria/triage-report.json`(2026-08-05 `/issue-triage` 对 aria-plugin#128 的时点快照, 记录"triage 当时的当前版本", 语义上是历史存档而非"当前版本声明", 与 `aria/CHANGELOG.md` 同类, 不应纳入零命中断言, 否则同样造成永久假红)。**结论: TASK-020 的 14 点清单既不多算也不少算, 无需修改**。

## Verdict

**PASS_WITH_WARNINGS**(0 Critical + 0 Major + 2 minor(new) + 1 observation)。

判据: 我 R1 的全部 4 条(2 Major + 2 Minor)均已 **closed**, 且 Major-2 用独立实跑数据核验(非抄述 commit message), TASK-020 零命中断言正控确认有鉴别力、覆盖面既不多算也不少算, 派生统计(21 任务/88h/agent 分摊)重算精确吻合、连续两次的"footer 写错"未复发。本轮新发现的 2 条 minor 均是**残留的可证伪性软点**(TASK-021 二选一的存档格式未钉死、场景齐备性判据仍纯人工无机械锚点), 均不阻塞、均有具体可执行的收尾建议, **不构成 Critical/Major**。TG-1 六任务粒度作为流程观察记录, 不计入返工要求。**fix 引入占比(本轮新增 Critical/Major 计数 / R1 该四条总数)= 0/4 = 0%** —— 本席位视角下收敛良好, 未发现"fix 自身按同一规律再生成缺陷"的迹象。

## 轮次记录

- Round 1 (qa-engineer): 2 Major + 2 Minor, verdict PASS_WITH_WARNINGS。
- Round 2 (qa-engineer, 独立席位, 同一视角保持可比): 逐条核 R1 四条闭合(全部 closed, 含独立实跑复核); 对新增 TASK-018~021 做同等严格度审查; 实跑 TASK-020 grep(确认正控命中且清单不多不少)与 footer 派生值重算脚本(确认吻合); 脚本核验 DAG 无环/无悬空/同文件全有序。产出 2 minor(new) + 1 process observation, 0 Critical, 0 Major。verdict PASS_WITH_WARNINGS。
