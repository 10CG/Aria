---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-31T13:52:44.000Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml (+ linked-issue-field-availability + sibling-spec-probe)
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 0
major_count: 1
minor_count: 2
r2_disposition: {closed: 5, partial: 1, not_addressed: 0}
introduced_by_fix: 1
---

## 摘要

本轮四项收窄镜头逐一亲验, 方法同 R2: 不读文档「输出」文本, 逐字复制脚本到 scratch 文件独立重跑, 并用 `diff` 程序化比对 (非目视)。

1. 三份文件各自嵌入的机械核验脚本 (`sibling-spec-probe` / `a1-entry` / `linked-issue-field-availability`) 逐字复制重跑, `diff` 三次全部 `IDENTICAL` (贴出输出与实跑输出逐字节相同), `RESULT: PASS` / exit 0 三份一致 —— R2-2 (探针脚本过度转义) 与 R2-3 (母脚本贴文陈旧) 确认闭合。探针 (e) 检查在真实现行文本上按брief 指示的三种改法测试: 按 brief 给的**原文字符串**「[并行, 不同文件] TASK-001 · 002 · 003」构造坏输入 (scratch 副本, 未改原文件), 该检查**仍不产生 fail**, 且比现状更退化 (正则 `TASK-\d{3}` 只抓到 `['TASK-001']`, 丢了未重复 `TASK-` 前缀的 002/003, 从「3 元素 0 冲突」退化成「1 元素数学上不可能有对」); 换成每项都带 `TASK-` 前缀的等价写法后正确抓全 3 项且判定正确 (仍无冲突); 再注入一个真实同文件冲突 (TASK-001/TASK-002 共写一个文件) 后该检查正确报 `RESULT: FAIL` 并精确点名冲突对 (exit 1)。三组对照证明 (e) 检查本身不是恒假/恒空的死代码, 但对「未重复 `TASK-` 前缀的枚举式简写」这一种输入格式脆弱 (细节见 Findings `d935b128`, minor, 非本轮回归, 现行文件未用到该写法)。
2. 红窗完整性: 三份文件的 RED (探针 G2 / 母 Group 6 / 字段 TG-1) 均**不**依赖任何 GREEN, 与 R2 一致, 无回退; 母 Group 6 (TASK-025~030) 祖先集仍 ⊆ {TASK-001, TASK-003} ∪ Group 6 (脚本 `[c]` 断言 True); 新增 TASK-040 (task_group 8, deps=[TASK-037]) 唯一直接依赖方是 TASK-038 (同为 group 8), 亲验 RED 任务 (Group 6 全部 6 个) 的 `dependencies` 字段均不含 `TASK-040`, 传递闭包上也不可能 (TASK-040 在依赖图末端)。TASK-032/033/035 与 TASK-031/034 的 `ARIA_COORDINATION_NO_PUSH=1` 前置措辞: 032/033/035 均以逐字相同的一句 (`运行前置 (Rule #7 射程 + R1 C5): 会话以 \`ARIA_COORDINATION_NO_PUSH=1 claude …\` 启动 (AB_TEST_OPERATIONS.md:222-228), transcript 核验 \`push_skipped: true\` — R2/A4 残留补`) 独立复述 + 一句「同 TASK-031」引用; TASK-034 只有「同 TASK-031」引用, 没有独立复述那一句。两种写法实质等价 (TASK-031 本身有完整三条, 「同 TASK-031」在 032/033/034/035 四处统一使用), 判定为非缺陷的措辞繁简差异, 不计入 Findings, 仅在实测记录留痕。
3. 母 TASK-018 → TASK-025 的委派: TASK-025 的 `verification` 列表逐字含标号 `③` 的一条 (`③ 切片内逐字 check: coordination ref ...`), 确认 SC-22 ③ 真实落在 TASK-025 (非仅 TASK-018 单方声称)。但深入核对「TASK-035 fixture (a) 仍存在作行为层」时发现: fixture (a) **确实存在** (未被误删), 但其**内容与 TASK-018 引用的场景不符** —— TASK-035 自身的 `SC 映射逐条` 明确把 (a) 记为 `SC-9 (A)(B) + SC-12 两臂 + SC-14(b)` (claim 派生字符串正确性), `deliverables` 里 spec-drafter.json 的 (a) 也写的是「拼串 + 省略门」, 全都不是「一次 A.1 两条 claim」(幂等/重复写入) 场景; 平行任务 TASK-017 (phase-a-planner 对称位) 自己的 verification 里把 SC-22 全部记为「由 TASK-025 验」, 完全没有引用 TASK-035 作行为层补充 —— 三方交叉核对 (TASK-018 声称 vs TASK-035 自身定义 vs 对称任务 TASK-017 的处理方式) 一致指向: TASK-018 那句「TASK-035 fixture (a) 的『一次 A.1 两条 claim』坏臂为行为层补充」是一条**不成立的引用**, 系 R2/A1 那次「委派 TASK-035 → TASK-025」编辑随手写错了附带说明。详见 Findings `532e5316` (major)。
4. 统计: 0 critical / 1 major / 2 minor。1 major (`532e5316`) 由本轮 (R2 那次委派编辑) 引入, 非 R1 遗留; 2 minor 中 1 条 (`78dc1ece`, a1-entry「39 tasks」陈旧字面) 由 R2 (TASK-040 新增) 引入未同步, 1 条 (`d935b128`, (e) 检查前缀脆弱性) 是脚本自 R1 起的既有设计属性, 与本轮无关。由于存在 1 条 major (非 0 C/0 M), 不满足「明确投 PASS」的条件, 本席投 REVISE。

## R2 finding 逐条闭合表

| R2 id/簇 | 严重度 | 内容 | 本轮亲验结果 |
|---|---|---|---|
| R2-1 (探针展示文本追记两边) | major | `execution_order[0]` 是否仍正确反映 003←002 | **closed** — 现行 `execution_order[0]` 原文含「002 ... 可并行 (不同文件); TASK-003 ... ← 002」, `TASK-\d{3}` 抓取到 `['TASK-001','TASK-002','TASK-003']`, `deliv` 集合层面三者两两无交集 (002 的 deliverable 是目录前缀字符串, 003 的是目录下具体文件字符串, 精确字符串比较不算重合), 脚本判定 same-file pairs=none 与贴出输出一致 |
| R2-2 (探针脚本过度转义) | major | 逐字复制脚本亲跑是否 PASS 且与贴文一致 | **closed** — `diff` 程序化比对贴出输出 (`tasks.md:261-304`) 与独立重跑 stdout, `IDENTICAL`; `RESULT: PASS`, exit 0 |
| R2-3 (母脚本贴文陈旧) | major | 母 40-task 版脚本贴文是否与实跑一致 | **closed** — `diff` 比对贴出输出 (`tasks.md:425-452`) 与独立重跑, `IDENTICAL`; `[+] total_tasks=40 (metadata 40)`, `RESULT: PASS` |
| R2-4 (TASK-040 新增, 子模块发布链宿主) | major | TASK-040 接线正确, 不被 RED 依赖 | **closed** — `TASK-040` task_group=8, deps=[TASK-037]; 唯一直接依赖方 `TASK-038` (同 group 8); Group 6 (RED, TASK-025~030) 六个任务的 `dependencies` 均不含 TASK-040, 图上不可达 |
| 母 TASK-018 幂等坏臂委派 TASK-035→TASK-025 (A1 minor) | minor→**升级见下** | SC-22③ 宿主是否真落 TASK-025; TASK-035 fixture (a) 是否仍在 | **partial** — SC-22③ 确认真实落在 TASK-025 (verification 第 3 条标号 ③); TASK-035 fixture (a) 存在但**内容对不上**引用场景, 见 Findings `532e5316` |
| 母 TASK-032/033/035 补 `ARIA_COORDINATION_NO_PUSH=1` (A4 minor) | minor | 措辞与 TASK-031/034 是否一致 | **closed** (含非阻塞观察) — 032/033/035 逐字相同的独立复述句 + 「同 TASK-031」双重; 034 只有「同 TASK-031」引用, 无独立复述; 因 TASK-031 本身完整、「同 031」全组统一使用, 判定语义等价, 非缺陷 |

## Findings

### `532e5316` — TASK-018 引用 TASK-035 fixture (a) 作幂等坏臂行为层补充, 但 fixture (a) 实际内容不覆盖该场景 (major, 由 R2 委派编辑引入)

**证据** (亲读三方交叉核对, 非单方文本采信):

- `openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml` TASK-018 `verification` 第 4 条逐字: 「正常委派路径 (phase-a-planner → spec-drafter) 下幂等谓词使只写一条 claim: 由 TASK-025 (SC-22 ③ 幂等谓词结构测试) 验; **TASK-035 fixture (a) 的『一次 A.1 两条 claim』坏臂为行为层补充** (R2/A1 minor: SC 映射里该臂宿主是 TASK-025)」。
- 但 TASK-035 自身 `verification` 里的 `SC 映射逐条` 一条逐字: 「(a) ⇒ SC-9 (A)(B) + SC-12 两臂 + SC-14(b); (b) ⇒ SC-11 (...); (c) ⇒ SC-25 ② 行为臂; (e) ⇒ SC-26 — **六条行为 SC 的唯一验证宿主**」—— 六条枚举完毕, 全程无 SC-22, 无「两条 claim」字样。
- TASK-035 `deliverables` 里 `spec-drafter.json` 那行的行内注释逐字: 「追加 (a) 拼串 + 省略门 (直调路径) 与 (b) 请裁两条 (同上, 去掉 Level 1 子场景)」—— spec-drafter.json 自己的 (a) 也是「拼串 + 省略门」(claim 派生字符串 / `--linked-issue` 省略逻辑), 同样不是幂等重复写入场景。
- 对称任务 TASK-017 (phase-a-planner 侧, 与 TASK-018 处理的是同一个 SC-22 概念的另一文件臂) 自己的 `verification` 第 1 条: 「本任务落文本后, 对应 TASK-025 (SC-22 ①–⑦, phase-a-planner 臂) 由红转绿」, 第 2 条把「行为臂由 TASK-035 定向 fixture 验」精确限定为 `SC-9(A)(B) / SC-11 / SC-12 / SC-26` 四项 —— 与 TASK-035 自陈的六条完全对齐, **没有**把 SC-22 或「两条 claim」归给 TASK-035。
- `proposal.md:384` 对 SC-22③ 的重要性有明文: 「幂等谓词 ... 保证正常委派路径上只写一条 claim —— 没有它, 一次 A.1 会写两条 claim + 两次外向推送, 该实现必须能被 SC-22 判红」—— 即该场景在设计者自己眼里是需要认真守住的属性。
- 结论: TASK-035 现行六条 fixture 里没有一条测「一次 A.1 是否真的只写一条 claim」这件事; SC-22③ 目前只有 TASK-025 的**结构断言** (SKILL.md 文本里是否含 `check:`/`if_missing:` 幂等谓词块), 没有任何**行为断言** (实跑 A.1 委派路径, 数一数到底写了几条 claim) —— 与 TASK-018 暗示的「有行为层补充」相反。

**影响**: 不影响任何一份文件当前机械核验脚本的 PASS 结果 (三份脚本都不检查这条跨任务引用的语义正确性); 影响的是「SC-22③ 的测试覆盖完整性」这条判断本身失真 —— Phase B 实现者或后续复核者读 TASK-018 会误以为幂等属性已有行为层兜底, 实际只有文本存在性检查, 若 AI 在 Phase B 把幂等谓词文本写对但委派逻辑本身仍误触发两次 A.1 (例如 skip 条件判断错误), 现有任务集合里没有任何 fixture 会抓到。

**处方**: 二选一 —— (a) 改 TASK-018 那句为如实描述 (「TASK-035 六条 fixture 均不覆盖幂等重复写入场景; SC-22③ 目前只有 TASK-025 的结构断言, 无行为层」), 若判定这是可接受的覆盖外档缺口则比照 TASK-036 的模式追加一行交叉引用; (b) 在 TASK-035 六条之外新增第 7 条定向 fixture (phase-a-planner.json 或 spec-drafter.json, 夹具 = 幂等谓词文本存在但委派路径故意触发两次调用的坏臂), 使「行为层补充」的声称落到真实宿主上。两者均为文本/任务级改动, 不影响已锁定的依赖图。

### `78dc1ece` — a1-entry/tasks.md:455 prose 仍写「39 tasks」, 与同文件自身的 40 (TASK-040 新增后) 不一致 (minor, 由 R2 TASK-040 追加未同步)

**证据**:

- `openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md:455` 逐字: 「解析器: PyYAML `safe_load` 通过; `aria/skills/state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_tasks` ⇒ `parse_ok=True`, **39 tasks**, status 集合 `{pending}`」。
- 同文件 `:451` (机械核验脚本贴出的真实输出, 本轮 `diff` 核实逐字节一致) 已经是: 「`[+] total_tasks=40 (metadata 40)`」。
- 亲跑 `parse_detailed_tasks(...)` (`aria/skills/state-scanner/scripts/lib/detailed_tasks.py`) 对当前 `detailed-tasks.yaml`: `parse_ok=True n=40 reason='40 task(s) parsed'`, `TASK-040 in ids = True`。
- 三者对照: 实际值与紧邻两行前的脚本贴文均为 40, 只有 `:455` 这一处散文仍停留在 R2 加入 TASK-040 之前的「39」。

**影响**: 纯文档内部数字不一致, 不影响任何依赖图/覆盖表判定 (`parse_detailed_tasks` 本身未被任何机械核验脚本拿来做 fail 判据, 只用于 `[+]` 一行展示 + 这句独立散文); 但与本文件同一小节自相矛盾, 读者会疑惑到底是 39 还是 40。

**处方**: `:455` 「39 tasks」→「40 tasks」, 一处字符级改动。

## 实测记录

- 三份文件机械核验脚本逐字复制到 scratch (`verify_sibling_r3.py` / `verify_a1_r3.py` / `check_c1_r3.py`), 独立执行 (linked-issue-field-availability 那份按其自身脚注 cwd=/home/dev/Aria 执行), 用 `diff` 与文档贴出的输出代码块比对, 三次均 `IDENTICAL`, exit code 分别为 0/0/0。
- (e) 检查三组对照 (均在 scratch 副本 YAML 上做, 未改任何原文件):
  1. 按 brief 原文坏输入「[并行, 不同文件] TASK-001 · 002 · 003」写入 `execution_order[0]`: `(e) parallel line ['TASK-001']: same-file pairs = none`, `RESULT: PASS`, exit 0 —— 正则 `TASK-\d{3}` 未重复前缀的 002/003 抓不到, 退化为 1 元素。
  2. 改写为每项均带前缀「TASK-001 · TASK-002 · TASK-003」: `(e) parallel line ['TASK-001', 'TASK-002', 'TASK-003']: same-file pairs = none`, `RESULT: PASS`, exit 0 —— 正确抓全 3 项, 正确判定无冲突。
  3. 在变体 2 基础上另给 TASK-002 的 `deliverables` 追加一个与 TASK-001 相同的文件路径 (真实注入同文件冲突): `(a) same-file pairs = 35; all with edge = False`; `(e) parallel line [...]: same-file pairs = [('TASK-001', 'TASK-002')]`; `RESULT: FAIL (a) ... TASK-002 shares [...] with TASK-001 but does not depend on it; (e) [...]`, exit 1 —— (a)(e) 均正确报错并精确点名冲突对。
- 红窗: 三份脚本自身的 (c)/[c] 断言均为 True/none (探针 `RED depending on GREEN = none`; 母「Group 6 祖先集 ⊆ {TASK-001,TASK-003} ∪ Group 6: True」; 字段「测试任务 ... 违反=[]」)。
- TASK-040 依赖面: 亲跑 python 遍历 `dependencies` 字段, `TASK-040` 的直接依赖方唯一为 `TASK-038`; Group 6 (`TASK-025`~`TASK-030`) 六个任务的 `dependencies` 字段逐一打印, 均不含 `TASK-040` 字面。
- `ARIA_COORDINATION_NO_PUSH=1`: TASK-031/032/033/034/035 五个任务 `verification` 全量打印比对, 032/033/035 三个各自独立复述 R2/A4 那句 (逐字相同) + 「同 TASK-031」引用二选一都有; 034 仅有「同 TASK-031」引用, 无独立复述; TASK-031 本身三条完整 (`ARIA_COORDINATION_NO_PUSH=1 claude …` / `push_skipped` / `git ls-remote` 核远端)。
- SC-22③ / TASK-035 fixture (a) 三方交叉: TASK-018 (声称方) / TASK-025 (verification 逐字含标号 ③) / TASK-035 (自身 SC 映射六条枚举 + deliverables 行内注释) / TASK-017 (对称任务, 精确限定行为臂四项 SC 且不含 SC-22) / TASK-036 (缺口 issue 任务, 复述「TASK-035 六条 TARGETED eval」印证六条已穷举) 五个任务全部亲读, 无一处提及 TASK-035 覆盖幂等重复写入场景。

## Verdict

**PASS_WITH_WARNINGS** — 0 critical, 1 major (`532e5316`), 2 minor (`78dc1ece` / `d935b128`)。R2 四大簇 (R2-1~R2-4) 与「ARIA_COORDINATION_NO_PUSH=1 补齐」minor 经独立重跑 + `diff` 程序化核验, 全部**实质闭合**, 无回退。红窗不变量 (RED 不依赖 GREEN / Group 6 只依赖 001·003 / TASK-040 不被 RED 依赖) 三份文件均保持成立。但深查「TASK-018 幂等坏臂委派」这条 R2 minor 时, 发现其**附带的行为层引用本身不成立** (TASK-035 六条 fixture 内容与引用场景不符, 三方交叉证实), 属新的、由 R2 那次编辑引入的 major; 另有 1 处 R2 未同步的陈旧数字 (minor)。均为文本/任务级改动, 修复成本低 (前者两个选项均不涉及依赖图重排, 后者一处数字), 但在改前不满足 0C/0M 门槛, 不投 PASS。

## Vote

**REVISE**
