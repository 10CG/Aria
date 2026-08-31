---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-31T14:11:49.000Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml (+ linked-issue-field-availability + sibling-spec-probe)
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 0
major_count: 0
minor_count: 0
r3_disposition: {closed: 3, partial: 0, not_addressed: 0}
introduced_by_fix: 0
---

## 摘要

本轮镜头收窄到「本席 R3 三条到实物核 + 红窗完整性不回退 + 三份贴文逐字节 + 统计」四项, 全部亲验, **未发现新 Critical/Major/Minor**。

1. `532e5316` (TASK-018 假引用幂等行为层): 已改为处方 (a) 「如实描述 + 交叉引用」—— `detailed-tasks.yaml:554` 逐字含「行为层 ... 当前**无宿主, 成文不冒充** (R3/A3 532e5316: TASK-035 fixture (a) 测的是 SC-9/12/14(b), 与幂等无关)」。全文件 grep「两条 claim / fixture (a) / 幂等坏臂」只命中这一处, 未留任何仍主张「TASK-035 覆盖幂等」的旧措辞 (fix-the-class 核过)。与 SC 覆盖表交叉: `tasks.md:119` 「SC-22 ①–⑦ | ... | TASK-025 · 被测文本 TASK-017/018」, TASK-025 `verification` 第 3 条逐字含标号「③ 切片内逐字 `check: coordination ref ...`」—— 三处 (TASK-018 新措辞 / 覆盖表 / TASK-025 verification) 互不矛盾, **closed**。
2. `78dc1ece` (「39 tasks」陈旧): `tasks.md:455` 已改「40 tasks」; `proposal.md` Status 行已含「40 tasks; TASK-040 = post_planning R2 补 ...」; 对三份文件 (`tasks.md` / `proposal.md` / `detailed-tasks.yaml`) 全量 grep「39」, 排除版本号/日期/行号锚点后零残留任务计数字面。**closed**。
3. `d935b128` (探针 (e) 检查对未重复 `TASK-` 前缀缩写脆弱): `sibling-spec-probe/tasks.md` 内嵌脚本 `ids_in()` 正则已改 `(?:TASK-)?\b(\d{3})\b` (前缀可选), 且新增「箭头右侧 ⊆ deps[head]」与「『并行』声明间无依赖」两个子检查。**closed**, 详见「实测记录」两组对抗构造。

红窗完整性: 三份文件的 RED/测试组均不依赖 GREEN (脚本自身 (c)/[c]/[c'] 断言全部重跑确认); 母 Group 6 (TASK-025~030) `dependencies` 逐一打印, 全部 ⊆ {TASK-001, TASK-003} ∪ Group 6 自身, 未被 TASK-037/038/039/040 污染; TASK-037 新增的 `TASK-009` 依赖经追踪不产生环、不改变 TASK-037 在图上的下游 (group 8) 位置, RED 不因此被拉出正确位置; TASK-040 六条款 (新鲜度前置 / 本地 merge / 授权门 / 超时 / 逐 remote 核验 / gitlink 后置) 逐条可证伪, 第 1 条「fetch 后三 SHA 不等 ⇒ 停」字面为「不一致先处理, 不合进陈旧基线」, 与字段孪生 TASK-022 六条款主题一一对应 (顺序小异, 语义对齐)。

三份内嵌脚本逐字提取独立重跑, 与贴文 `diff` 程序化比对, 三次 `IDENTICAL`, exit 0/0/0, `RESULT: PASS` 三份一致。

统计: 0 critical / 0 major / 0 minor, 本轮无新 finding, 故 `introduced_by_fix=0`。本席 R3 三条 **全部 closed** (3/3), 无 partial / not_addressed。按契约「若无 C/M, 明确投 PASS」—— 投 **PASS**。

## R3 finding 逐条闭合表

| R3 id | 严重度 | 内容 | 本轮亲验结果 |
|---|---|---|---|
| `532e5316` | major | TASK-018 引用 TASK-035 fixture (a) 作幂等行为层补充, 但 (a) 实际测 SC-9/12/14(b), 与幂等无关 | **closed** — `detailed-tasks.yaml:554` 改为如实措辞「当前无宿主, 成文不冒充」+ 交叉引用本 finding id; 与 SC 覆盖表 (`tasks.md:119`) 及 TASK-025 verification ③ 一致; 全文件 grep 未留旧措辞残留 |
| `78dc1ece` | minor | `tasks.md:455` 仍写「39 tasks」, 与同文件脚本贴文的 40 不一致 | **closed** — `:455` 已改「40 tasks」; 同簇 (`tasks.md:232` 位移后位置 / `proposal.md` Status 行) 一并核实已改 40; 三份文件全量 grep 排除误报后零残留 |
| `d935b128` | minor | 探针 (e) 检查正则 `TASK-\d{3}` 对未重复前缀的缩写枚举 (`001 · 002`) 脆弱, 会静默退化 | **closed** — `ids_in()` 正则改为前缀可选 (`(?:TASK-)?\b(\d{3})\b`); 现行 `execution_order` 内全部缩写用法 (sibling-spec-probe 11 行) 逐一验证零假阳性; 新增两个子检查 (箭头右侧⊆deps / 并行声明无依赖) 均在 scratch 副本对抗构造下正确报错 (见下) |

## Findings

（本轮无新增 Critical / Major / Minor finding。）

## 实测记录

**三份内嵌脚本逐字节核验** (提取方式: 用 python 正则从各 `tasks.md` 的 `## 机械核验` 段程序化切出 ```` ```python ```` 块与紧邻的贴文输出块, 避免手抄误差; 脚本写入 scratch 独立执行, 不改原文件):

- `sibling-spec-probe/tasks.md`: 脚本 105 行 / 贴文输出 60 行 → 独立执行 exit=0, `diff` 与贴文 `IDENTICAL`, `RESULT: PASS`。
- `a1-entry-claim-duplicate-work-guard/tasks.md` (母, 40 任务): 脚本 → 独立执行 exit=0, `diff` `IDENTICAL`, 尾行确认 `[+] total_tasks=40 (metadata 40)`, `RESULT: PASS`。
- `linked-issue-field-availability/tasks.md`: 脚本 docstring 显式要求 `cd /home/dev/Aria && python3 check_c1.py` (相对路径); 按此 cwd 重跑 exit=0, `diff` `IDENTICAL`, `RESULT: PASS`（首次未切 cwd 直接跑触发 `FileNotFoundError`, 换正确 cwd 后核验通过, 非脚本缺陷 —— 与其自身文档化用法一致）。

**探针 (e) 对抗构造** (均在 `sibling-spec-probe` 目录的独立 scratch 副本上做; 完毕后 `md5sum` 核对原文件 `detailed-tasks.yaml`/`tasks.md` 未被触碰):

1. **dep-contradiction 轴**: 真实 `execution_order[0]` 现文 = `"TASK-001 (硬前置断言, 阻塞门) ‖ TASK-002 (基线三态, 只读观测) 可并行 (不同文件); TASK-003 (AB 套件文件, B.1 前置) ← 002 (...)"`（即: 001∥002 并行, 003←002 有依赖, 与真实 `deps[TASK-003]=['TASK-002']` 一致, 现行判定 `dep-contradiction=none`）。将该行整体替换为 brief 指定坏输入字面 `"[并行, 不同文件] TASK-001 · 002 · 003"`（把 003 也错误地并入"并行"集合, 与真实 003←002 矛盾）后独立重跑:
   ```
   (e) parallel claim ['TASK-001', 'TASK-002', 'TASK-003']: dep-contradiction = [('TASK-002', 'TASK-003')]; same-file pairs = none
   ...
   RESULT: FAIL (e) parallel claim contradicts deps [('TASK-002', 'TASK-003')]
   ```
   exit=1, 精确点名矛盾对 `(TASK-002, TASK-003)`。**拒绝能力确认**。
2. **NOT IN deps 轴**: 真实 `execution_order[1]` = `"TASK-004 (测试骨架 + SC-21)  ← 001, 002, 003 (...)"`（`deps[TASK-004]=['TASK-001','TASK-002','TASK-003']`, 三者吻合, 现行判定 `OK`）。在括号前追加一个不在 deps 里的编号 `010`（改为 `← 001, 002, 003, 010`）后独立重跑:
   ```
   (e) TASK-004 ← ['TASK-001', 'TASK-002', 'TASK-003', 'TASK-010']: NOT IN deps ['TASK-010']
   ...
   RESULT: FAIL (e) TASK-004 arrow ['TASK-010'] not in dependencies
   ```
   exit=1, 精确点名多余编号。**拒绝能力确认**。
3. 两组构造后立即 `md5sum` 核对: `sibling-spec-probe/detailed-tasks.yaml` 与构造前一致 (`ddc309c3...`), `git status --short` 仅原有 `??`/`M` 条目, 无新增改动 —— 原文件未被这两组坏输入污染。
4. 补充扫描: 对三份文件真实 `execution_order` 全量提取「未紧邻 `TASK-` 前缀的裸三位数字」, 全部命中都是合法缩写编号 (如 `← 001, 002, 003`), 零假阳性风险 (如 `SC-123` 类三位数字与「並行/←」共现) 在现行文本中实际出现, 本项非新 finding, 仅确认修复后未在真实语料引入副作用。

**红窗完整性**:
- `TASK-025`~`TASK-030` (母 Group 6) `dependencies` 逐一打印: `025:[001,003] 026:[003,025] 027:[003,026] 028:[003,027] 029:[003,028] 030:[003,029]` —— 全部 ⊆ {001,003}∪Group 6 自身, 无一引用 037/038/039/040。
- `TASK-037` `dependencies` 含 25 项, 新增的 `TASK-009` 确认在列 (R3-2 处方落地); `TASK-009` 本身是 Group 2 任务 (`deps=[001,003,008]`), 与 Group 6 (RED) 无关, 不构成"把 RED 拉进发布链外错误位置"。
- `TASK-040 deps=[TASK-037]`; 唯一直接依赖 `TASK-040` 者是 `TASK-038`; `TASK-039 deps=[TASK-003]`。文件字面序 (`- id:` 出现顺序) 核实为 `...035, 036, 037, 038, 039, 040` —— TASK-040 块确认已移至 TASK-039 之后 (R3 minor 位移落地)。
- 全图无环 (母脚本 `[b] 无环: True`, 已含在上方 byte-diff 重跑内, 覆盖 TASK-037/040 新边)。
- `TASK-040` 六条 verification 逐条读: ① 新鲜度前置 (fetch 后三 SHA 相等断言, 不等则「先处理, 不合进陈旧基线」——落地为停止条件) ② 本地 `--no-ff merge` + 双父校验 ③ owner 显式授权门 (未授权停在本地合并态) ④ 双推显式超时 ⑤ 逐 remote `ls-remote` + `rev-parse` 独立核验, 失败重试 ⑥ 两 remote 一致后才允许 TASK-038 bump gitlink。与字段孪生 `TASK-022` 六条 (前置新鲜度/本地merge/双推/逐remote核验/gitlink后置/owner授权门) 主题一一对应, 顺序小异但语义对齐, 六条均可独立证伪 (非散文空话)。

**假引用清除的全文件扫描**: `grep -n "一次 A\.1 两条 claim\|两条 claim\|幂等坏臂\|fixture (a)" detailed-tasks.yaml` 只命中 `:554`（即改写后的 TASK-018 本行, 内容是「不冒充」的如实措辞), 无第二处残留旧主张, 亦未见 TASK-017 (对称任务) 或 TASK-035/036 出现被撤销的旧说法。

## Verdict

**PASS** — 0 critical / 0 major / 0 minor。本席 R3 三条 (`532e5316` major / `78dc1ece` minor / `d935b128` minor) 经实物核验 (文本比对 + 独立重跑 + 两组对抗构造) **全部 closed**, 无 partial、无 not_addressed。红窗四项不变量 (RED 不依赖 GREEN / Group 6 只依赖 001·003 / TASK-037 新边不污染 RED 位置 / TASK-040 六条款可证伪) 均保持成立, 无回退。三份内嵌脚本与贴文逐字节 `diff` 全部 `IDENTICAL`。本轮未发现任何新 finding, `introduced_by_fix=0`。按契约「若无 C/M, 明确投 PASS」。

## Vote

**PASS**
