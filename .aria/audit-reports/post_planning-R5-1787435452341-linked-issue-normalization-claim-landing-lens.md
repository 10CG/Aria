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
agents: [claim-landing-lens]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R5 · 席位 B「声称-落地一致性镜头」— linked-issue-normalization

## 1. 镜头与范围

- 审什么: `git show 97a3885 --format=%B` (R4-fix) 与 `git show 09eb919 --format=%B` (2026-08-22 收口) 里的每一条「改了 X」声称, 逐条在 `detailed-tasks.yaml` / `tasks.md` / `proposal.md` 三文件全文核它落没落到**全部**同义落点; 三文件之间的派生值一致性 (程序化算, 不手数); 三处状态头是否互相矛盾; 引用到 aria 子模块 (HEAD `9e6a17c`) 的事实实读核对。
- 不审: 措辞 / 判据能否跑通 / 算法 / 委派对象选择。
- 基线: 主仓 HEAD `09eb919` (实测 `git rev-parse HEAD`), aria 子模块 `9e6a17c` (实测 `git -C aria rev-parse HEAD`), 工作树干净。全程只读; 脚本放 scratchpad。
- 核对方式: 所有 finding 附实跑命令与输出; 派生值一律 python 算 (脚本 `scratchpad/dag.py`, 正文贴输出)。

## 2. 声称清单逐条核验表

N = 该事实在三文件里的同义落点数 (散文 + yaml 字段 + 注释 + tasks.md 对应段 + proposal 对应段); k = 实际已改的落点数。

| # | 声称 | 来源 commit | 应落点 N | 实落 k | 漏处 (file:line) | 结论 |
|---|------|-------------|---------|--------|------------------|------|
| S1 | 「TASK-028 (合并+gitlink) 改到 TASK-026 之前」 | 97a3885 | 4 (yaml deps / yaml DAG 注释 / tasks.md 排序段 / tasks.md 5.13 验收) | 4 | — | 一致 (程序化核: `'TASK-028' in anc('TASK-026') → True`) |
| S2 | 「DAG 注释 20→21, 补 TASK-028, 关键路径改到 026」 | 97a3885 | 3 (yaml :951 / :970 / :974) | 3 | — | 一致 (python 算 active=21, 关键路径 `001→…→010→014→022→023→024→028→026` 与 :970 逐字同) |
| S3 | 「C1: scope_boundary.delegated[0] 改为『仅 PR+闸门, 不含合并/双推/gitlink』; R3-fix **已在 tasks.md 与 TASK-026/028 完成这次切分**」 | 97a3885 | 8 (yaml delegated / TASK-026 / TASK-028 / TASK-023 notes / tasks.md 范围边界表 :42 / :46 交接段 / :118 5.3 / :119 5.4) | 3 | **tasks.md:42, :46, :118, :119; yaml:813-814** | **漏 5 处, 且「R3-fix 已在 tasks.md 完成」这句声称本身为假** → C-1 |
| S4 | 「两条 cancelled 的 superseded_by 指向已更正」 | 97a3885 | 6 (yaml TASK-016/017 superseded_by / tasks.md 重映射表 :23-24 / tasks.md 删除线 :118-119) | 4 | tasks.md:118 (5.3 → C.2.5), :119 (gitlink 归 5.13) | 并入 C-1 |
| S5 | 「账本不变量最终改用『文件行数不减』; (a) 写『全部当前版本声明』而非『头部』; 『历史行原样保留』前提不成立」 | 97a3885 | 8 (yaml append_only_ledger :176-191 / TASK-024 :827 / TASK-022 deliverables 注释 :772 / TASK-022 verification :776 / tasks.md 5.11 :143-145 / tasks.md 5.9 :128 / tasks.md :105 / proposal :271) | 4 | **yaml:772, :776; tasks.md:128, :105; proposal:271** (proposal 仍是 R3-fix 时代的「头部当前版本行 == SOT 且旧值命中数不减」) | → M-4 |
| S6 | 「失明几处: R2-fix 写 7, 实为 10」 | 97a3885 | 5 (yaml mechanical_fix :165 / tasks.md 5.11 :141 / yaml enabled_check_blindness :157 / yaml TASK-023 notes :808-809 / proposal :271) | 2 | **yaml:157「共 7 处」, yaml:808-809「这 7 处结构性失明」, proposal:271「7 处残留…仍全绿」** | → M-5 (同一 yaml 文件 :157 与 :165 相反) |
| S7 | 「ship target 1.66.0→1.67.0 (11 处)」 | 09eb919 | 实际改 13 行 / 14 次出现 | 13 | — (无漏; 但声称的「11 处」数错) | 三头 + proposal Impact 一致 → m-1 |
| S8 | 「ship target 刷新」的**配对旧值** (bump 起点 `1.65.5` → 实际应为 `1.66.4`) | 09eb919 (应随 S7 同批) | 4 (yaml TASK-024 :823 / tasks.md 5.11 :138 / yaml version_reference_surface :137-151「实测 grep 1.65.5」/ TASK-020 :715 cancelled 可不改) | 0 | **yaml:823, tasks.md:138, yaml:137** | → M-2 |
| S9 | 「#137 已修 v1.66.0, 分支存在性 fail-CLOSED, 缺省仍 main (pre_merge_gate.py:547); (b) 腿恒真解除」 | 09eb919 | 2 (yaml gate_leg_caveat :86-94 / tasks.md 5.13 :161) | 2 | tasks.md:161 仍只引旧锚 `:427`, 未补 `:547` (半落) | 一致 (事实实读为真, 见 §5); 锚见 m-8 |
| S10 | 「R4 M3: 既有 6 个 test 按 class/方法名点名 (宿主 34)」 | 09eb919 | 3 (tasks.md :67 / yaml TASK-001 :258 / TASK-014 :560) | 3 | — (proposal :269 用行号锚 `:206-247`/`:527-575`, 在 9e6a17c 实读仍正确) | 一致 |
| S11 | 「R4 M5: TASK-013/025/027 deliverables 补 verification 强制改动的文件」 | 09eb919 | 3 task | 3 | — 但补完后 **TASK-025 与 TASK-027 同写 proposal.md 且无序、跨 owner**; DAG 注释 :973「无同文件并行边」与 `file_domain_serialization` 未同批更新 | → M-1 |
| S12 | 「R4 M7: dangling 指针枚举改 git grep 口径 (三个交付面文件)」 | 09eb919 | 2 (yaml TASK-025 :860 / tasks.md 5.12 :151) | 2 | — | 一致 (实跑 `git grep -l` = 3 文件; 计数 yaml 现为 3 处非 2, 见 m-6) |
| S13 | 「tasks.md『见 5.8』→ 5.12」 | 09eb919 | 1 (tasks.md :187) | 1 | — | 一致 (余下 `5.8` 出现全是「5.2–5.8 已 CANCELLED」范围语或 cancelled 任务自述) |
| S14 | 「scope_repos head: aria 9e6a17c / 主仓 084209f」 | 09eb919 | 2 head 字段 + 随 head 失效的行号锚 ≥ 4 组 | 2 + 1 (pre_merge_gate :427→:547) | **aria/VERSION:56-59 (yaml:188, :827; tasks.md:144); phase1_gate.py:1232/:1235 (proposal:30, :58, :66, :137, :161; yaml:302); phase-c-integrator SKILL.md:253 (yaml:70, :884; tasks.md:157, :160)** | → M-3 |
| S15 | 「.aria/config.json max_rounds 4→5」 | 09eb919 | 1 | 1 | — | 一致 (`grep -n max_rounds .aria/config.json` → `64: "max_rounds": 5`) |
| S16 | 「审计轨 §9 追记」 | 09eb919 | 1 | 1 | — | 一致; 但 §9 写「容器 bfe8285d」, yaml :51 抄成「机械收口 (bfe8285d)」读作 commit SHA → m-2 |
| S17 | 三处状态头一致 (隐含声称: 收口 commit 说「status 段/head 刷新」) | 09eb919 | 3 (proposal :3 / yaml metadata.status :41-53 / tasks.md :4) | 2 | **tasks.md:4** 仍写「A.2 + A.3 R2-fix … 待 R3 (只审组 5)」 | → M-6 |

## 3. 派生值一致性表

脚本 `scratchpad/dag.py` (PyYAML 读 yaml, 传递闭包 + 最长路径 + 同文件并行对), 实跑输出:

```
total 28 metadata.total_tasks 28 active 21
ids TASK-001 .. TASK-028 unique 28
complexity {'M': 6, 'S': 14, 'L': 1} hours 88 agents {'qa-engineer': 10, 'backend-architect': 7, 'knowledge-manager': 4}
groups: Counter({'TG-5': 8, 'TG-1': 6, 'TG-2': 3, 'TG-3': 3, 'TG-4': 1})
critical path by hours 67 001->002->003->004->005->007->008->009->010->014->022->023->024->028->026
longest by edges 14 (同一条)
unordered pairs 32
FILE aria/skills/state-scanner/tests/test_release_by_track.py [001..006] parallel pairs: []
FILE aria/skills/state-scanner/lib/collision.py [007,008,009,010] parallel pairs: []
FILE openspec/changes/linked-issue-normalization/proposal.md ['TASK-025', 'TASK-027'] parallel pairs: [('TASK-025','TASK-027','backend-architect','qa-engineer')]
028 before 026: True   024 before 028: True
```

| 派生值 | yaml 声称 | 程序化结果 | tasks.md / proposal | 判定 |
|---|---|---|---|---|
| total / active / cancelled | 28 / 21 / 7 (:43, :978) | 28 / 21 / 7 | tasks.md checkbox 21 (`grep -c "^- \[ \]"` = 21); 删除线 7 | 一致 |
| active parent 集 vs tasks.md checkbox 编号集 | — | 21 ↔ 21, 对称差 = 空 (`a==b True set()`) | 分组 13 (组 1-4) + 8 (组 5) 与 yaml :100-101 同 | 一致 |
| cancelled parent 集 vs 删除线编号 | 5.2–5.8 | `['5.2'..'5.8'] == ['5.2'..'5.8'] True` | — | 一致 |
| 复杂度 / 工时 / agent | S14·M6·L1 / 88h / qa10·ba7·km4 (:976-977) | 同 | — | 一致 |
| DAG 无环 / 028<026 / 024<028 | :960-967 | True / True / True | tasks.md :60-61 排序段同 | 一致 |
| 关键路径 | :970 | 逐字同 | — | 一致 |
| 无序对数 | :967「32 对」 | 32 | — | 一致 |
| **同文件并行边** | :973「⛔ 无同文件并行边」; `file_domain_serialization` 只列 2 文件 | **proposal.md 上 TASK-025 ∥ TASK-027, 跨 owner (backend-architect / qa-engineer)** | tasks.md 5.12 与 5.14 亦无互序 | **不一致 → M-1** |
| ship_target | :42 `v1.67.0` | 出现 14 次 / 13 行 (yaml 7, tasks.md 3, proposal 3 行) | tasks.md :6 / proposal :3 :8 :272 全 1.67.0; 无 1.66.0 残留 (仅历史叙述) | 一致 |
| bump 旧值 | :823 `1.65.5`; :137「2026-08-08 实测 grep 1.65.5」 | aria `VERSION:3` 实读 `1.66.4`, plugin.json = 1.66.4 | tasks.md :138 `1.65.5` | **不一致 → M-2** |
| scope_repos head | aria 9e6a17c / 主仓 084209f | aria HEAD 9e6a17c ✓; 主仓 HEAD 09eb919, `09eb919^` = 084209f | — | 一致 (主仓头天然落后本 commit 一步, m-5) |
| 既有 test 名/数 | 6 = 4 + 2; 宿主 34 | 9e6a17c 实读: `TestLinkedIssueOverlaps` 4 个、`TestPhase1GateLinkedIssueCli` 2 个 (名逐字同 tasks.md :67); 总 test 方法 34 | proposal :269 行号锚 :206/:247/:527/:575 在 9e6a17c 仍正确 | 一致 |
| 测试基线 | 1322 | `run_tests.py` 实跑 `Ran 1322 tests / OK` | tasks.md :109 同 | 一致 |

## 4. Findings

### Critical

**C-1 · 「合并/双推/gitlink 归谁」在 tasks.md 仍有 4 处 + yaml 1 处写着被推翻的旧答案; R4-fix 的「R3-fix 已在 tasks.md 完成这次切分」声称为假** (R4 C1 同形状第四次)

- 位置: `tasks.md:42` (范围边界表: 「aria 子模块合并 + 双远程推送 → `phase-c-integrator` C.2.5 … 该 Skill (SKILL.md:242) 本就建模子模块合并」); `tasks.md:46` (「由 5.13 交付给 phase-c-integrator: **由它做** aria 子模块合并 + 双推 + 主仓 gitlink bump … 由 C.2.5 的既有机制保证」); `tasks.md:118` (5.3 → 「委派 `phase-c-integrator` C.2.5, 见 5.13」); `tasks.md:119` (「gitlink 归 5.13」); `detailed-tasks.yaml:813-814` (TASK-023 notes 「gitlink … 移交 Phase C (TASK-026)」)。
- 相反落点: `tasks.md:154-160` (5.13 只委派 PR/闸门, 合并由 5.15) / `tasks.md:170-175` (5.15) / `detailed-tasks.yaml:58-66` (delegated 「⛔ 不含 … 由 TASK-028 承载」) / `:872-884` (TASK-026) / `:923-937` (TASK-028) / `tasks.md:23-24` 重映射表 (TASK-016 → TASK-028)。
- 证据:
  ```
  $ grep -n "C\.2\.5\|SKILL.md:242" tasks.md
  42:| **aria 子模块合并 + 双远程推送** | **`phase-c-integrator` C.2.5**, 不在本文件 ...该 Skill (SKILL.md:242) 本就建模子模块合并
  46:...由它做 aria 子模块合并 + 双推 + 主仓 gitlink bump + PR + pre-merge gate ... 由 C.2.5 的既有机制保证
  118:- **~~5.3 aria 子模块分支合并 + 双推~~ **(CANCELLED ...)** → **委派 `phase-c-integrator` C.2.5**, 见 **5.13**
  119:- **~~5.4 主仓 gitlink + VERSION + README 两处~~ ... gitlink 归 **5.13** (随合并一并移交)
  $ sed -n '63,64p' detailed-tasks.yaml
  **R4-fix 更正落地缺口 (R4/delegation-lens C1)**: R3-fix 已在 tasks.md 与 TASK-026/028 完成这次切分, 但本块逐字未改
  $ sed -n '813,814p' detailed-tasks.yaml
  ...**gitlink 不在本任务** — 随合并一并移交 Phase C (TASK-026)。
  ```
- 为什么是 Critical: 这不是措辞, 是「谁执行合并」这个承重事实在 tasks.md 的**范围边界表** (读者进入组 5 的第一个表) 里给了与 5.13/5.15 相反的答案, 并且 R4-fix 在 yaml :63 把 tasks.md 写成「已完成切分」—— 声称与落地相反。与 R4 C1 完全同形: 「fix 落在一部分地方而非全部」, 只是这次落在 tasks.md 与 TASK-023。
- 一行修法: `tasks.md:42` 改为「**本文件 5.15** (硬约束 1+2); phase-c-integrator 仅 PR/闸门 (5.13)」并删 `SKILL.md:242` 引用; `:46` 「由它做…」改为「5.15 本地做合并/双推/gitlink, 5.13 只交 PR+闸门」; `:118` → 「→ **5.15**」; `:119` → 「gitlink 归 **5.15**」; `yaml:814` `TASK-026` → `TASK-028`。
- 引入轮: 漏处本身是 R3-fix 没扫到; **「已在 tasks.md 完成」这句假声称由 R4-fix (97a3885) 引入**。

### Major

**M-1 · 收口补 deliverables 后产生了新的同文件并行边 (proposal.md: TASK-025 ∥ TASK-027, 跨 owner), 而 DAG 注释「无同文件并行边」与 `file_domain_serialization` 未同批更新**

- 位置: `detailed-tasks.yaml:853` (TASK-025 deliverables 含 proposal.md / tasks.md / detailed-tasks.yaml), `:906` (TASK-027 deliverables 含 proposal.md), `:973` (「⛔ 无同文件并行边 (见 metadata.file_domain_serialization)」), `:213-231` (file_domain_serialization 只列 2 个文件)。
- 证据: `dag.py` 输出 `FILE openspec/changes/linked-issue-normalization/proposal.md ['TASK-025','TASK-027'] parallel pairs: [('TASK-025','TASK-027','backend-architect','qa-engineer')]`。TASK-025 deps=[009], TASK-027 deps=[013], 二者互不可达, 且 agent 不同 —— 正是 file_domain_serialization 注释自己定义的「同文件多任务必须串行, 跨 agent 同文件必须换 owner」(`:210-211`) 所禁止的形态。TASK-025 还把 `tasks.md` / `detailed-tasks.yaml` 列为 deliverables, 而这两文件同时是 TASK-027 披露要写 rule6_note 的载体之一 (tasks.md 5.14)。
- 一行修法: 给 TASK-027 加依赖 `[TASK-013, TASK-025]` (或反向), 并在 `file_domain_serialization` 增 `openspec/changes/linked-issue-normalization/{proposal.md,tasks.md,detailed-tasks.yaml}` 条目; `:973` 注释据程序化结果重写。
- 引入轮: **09eb919 (收口)**。

**M-2 · ship target 刷新了「新值」, 没刷新配对的「旧值」: 差集断言仍 grep `1.65.5`, 而 bump 起点已是 `1.66.4`**

- 位置: `detailed-tasks.yaml:823` (TASK-024 「grep 旧版本号 `1.65.5`」), `tasks.md:138` (5.11 同), `detailed-tasks.yaml:137` (version_reference_surface 「2026-08-08 实测 grep -rn 1\.65\.5」—— 18 点计数的取证基线)。
- 证据:
  ```
  $ grep -n "1\.65\.5" detailed-tasks.yaml tasks.md | grep -v "TASK-019\|v1.52.0"
  detailed-tasks.yaml:823: ... grep 旧版本号 `1.65.5` ...
  tasks.md:138: ... grep 旧版本号 `1.65.5` ...
  $ sed -n 3p aria/VERSION            → > **版本**: 1.66.4
  $ git show 09eb919 -- openspec | grep '^+' | grep -c "1\.65\.5"   → 0   (收口未触碰旧值)
  ```
- 后果 (只述事实, 不评判据): 从 1.66.4 bump 到 1.67.0 后, grep `1.65.5` 的命中集合与本次 bump 无关 (1.65.5 早在 #137 ship 时就被换掉), 差集断言对本次 bump 的「旧值残留」零检测力; 18 点 breakdown 也是对 1.65.5 的实测, 未对 1.66.4 复测。
- 一行修法: 旧值改写为「bump 前 `plugin.json` 的实值 (执行时读, 当前 1.66.4)」, 不硬编码; `:137` 注明计数需对 1.66.4 复测。
- 引入轮: **09eb919 (收口, 刷新不完整)**。

**M-3 · 「head 刷新」只改了 head 字段 + 1 个锚; 随 head 失效的其余行号锚未复核, 三组已漂移**

- 位置与证据 (af87cae 时全部正确, 9e6a17c 实读):
  - `aria/VERSION:56-59` 「第二处声明 1.47.0」→ 现在 `:60-63` (`grep -n "## 版本号" aria/VERSION` → 60; `1.47.0` 在 :63; `:56-59` 现为 1.34.0/1.33.0 发布注)。落点: `detailed-tasks.yaml:188`, `:827` (TASK-024 验收判据逐字写 `:56-59`), `tasks.md:144`。
  - `phase1_gate.py:1232` (调用) / `:1235` (except) → 现在 `:1233` / `:1236` (`grep -n "linked_issue_overlaps(\|except Exception" …/phase1_gate.py` → 1233 / 1236; `git diff --stat af87cae 9e6a17c -- …phase1_gate.py` = +1 行)。落点: `proposal.md:30, :58, :66, :137, :161`; `detailed-tasks.yaml:302`。
  - `phase-c-integrator/SKILL.md:253` 「green 后直接调用 branch-manager merge」→ 现在 `:261` (`git show af87cae:…SKILL.md | sed -n 253p` 的那行在 9e6a17c 用 `grep -nF` 定位到 261)。落点: `detailed-tasks.yaml:70, :884`; `tasks.md:157, :160`。
  - 对照: 同一次收口**确实**把 `pre_merge_gate.py:427` 复核成 `:547` (`yaml:92`), 说明作者知道 head 变动会使锚失效, 但只复核了 #137 相关那一个。
- 一行修法: 三组锚按上述新行号改, 或改为内容锚 (`## 版本号` 块 / `out["linked_issue_overlap"] = linked_issue_overlaps(` / 「green → 调用 branch-manager merge action」)。
- 引入轮: **09eb919 (收口)** —— 锚在 R4-fix 时正确, 是 head 刷新使其失效。

**M-4 · 账本不变量的三项更正 (行数不减 / 「全部」而非「头部」/ 「历史行原样保留」前提不成立) 只落在 TASK-024 与 5.11, 产出侧 TASK-022 / 5.9 与 proposal Impact 仍是旧判据**

- 位置: `detailed-tasks.yaml:772` (TASK-022 deliverables 注释「只改头部当前版本行」), `:776` (TASK-022 verification 「头部『当前版本』行 == plugin.json; **历史行原样保留**」), `tasks.md:128` (5.9 同), `tasks.md:105` (「前者是『头部当前版本行 == SOT』」), `proposal.md:271` (「头部当前版本行 == SOT **且旧值命中数不减**」—— 连 R3-fix 时代的「旧值命中数」口径都还在)。
- 证据: `grep -n "头部\|历史行原样保留\|旧值命中数不减" detailed-tasks.yaml tasks.md proposal.md` → 命中 yaml:772, :776; tasks.md:105, :128; proposal:271 (另 yaml:179-191 / tasks.md:144-145 是**更正后**的表述)。`git show 97a3885 -- openspec | grep '^+' | grep -c "全部"` 可见 R4-fix 只在 TASK-024 与 5.11 新增「全部」。
- 同一文件内相反: TASK-022 验收要求「只改头部 + 历史行原样保留」, TASK-024 验收要求「**全部**当前版本声明 == plugin.json (注意第二处声明)」并在 `:196` 写该第二处「不在本 Spec 范围」—— 两任务的判据对同一文件给出不同要求 (由哪一席判其能否同时满足不在本镜头, 此处只报不一致)。
- 一行修法: TASK-022 :772/:776 与 5.9 :128 改为「当前版本声明行 == plugin.json; 不删改历史 (验收由 TASK-024 行数不减兜)」; tasks.md :105 与 proposal :271 的账本判据改抄 5.11 的 (a)+(b)。
- 引入轮: **R4-fix (97a3885) 落地不完整**。

**M-5 · 「失明几处 = 10 (非 7)」只改了 mechanical_fix 与 5.11, 同一 yaml 文件 :157 与 proposal :271 仍写 7**

- 位置: `detailed-tasks.yaml:157` (enabled_check_blindness 「共 **7 处**残留旧版本时两条 enabled check 仍全绿」), `:808-809` (TASK-023 notes 「共 7 处, 而两条 enabled check 对这 7 处结构性失明」), `proposal.md:271` (「**7 处**残留旧版本时二者仍全绿」)。相反落点: `yaml:165` 「R2-fix 写 7, 实为 **10**」, `tasks.md:141` 同。
- 证据: `grep -n "7 处\|实为 \*\*10" detailed-tasks.yaml tasks.md proposal.md` 输出见 §2 S6。
- 一行修法: :157 / :808 / proposal :271 的 7 → 10 (README.md 1 + i18n 6 + CLAUDE.md 2 + VERSION 1), 或统一改为「两条 check 之外的全部引用点」不写数。
- 引入轮: **R4-fix (97a3885) 落地不完整**。

**M-6 · 三处状态头: tasks.md 头仍停在 R2-fix「待 R3 (只审组 5)」, 与 proposal / yaml 的「R5 前机械收口已落, 待 R5」矛盾**

- 位置: `tasks.md:4`; 对照 `proposal.md:3`, `detailed-tasks.yaml:41-53`。
- 证据:
  ```
  $ sed -n 4p tasks.md
  > **Level**: 3 | **Status**: 📝 **A.2 + A.3 R2-fix (组 5 按规律重做)** (2026-08-08) — … 待 R3 (只审组 5)
  $ sed -n 3p proposal.md
  > **Status**: 📝 **Draft (A.3 done, post_planning 未收敛)** — … owner 2026-08-22 裁定加 1 轮 R5 …
  ```
  「当前处于哪一步 / 下一步是什么」: tasks.md 说下一步 R3 只审组 5; 其余两文件说下一步 R5 两席全审。归档门与 handoff_autofill 读的是 tasks.md。
- 一行修法: tasks.md :4 状态改抄 yaml :50-53 (R3→R4→R4-fix→R5 前收口, 待 R5)。
- 引入轮: 非 R4-fix / 收口引入 (R3-fix 起即未更新), 但收口声称刷新 status 面时漏了它。

### Minor

- **m-1** `09eb919` commit message 「ship target … (11 处)」: 实际 `git show 09eb919 -- openspec | grep '^+' | grep -c 1.67.0` = 13 行 (proposal :8 一行含 2 次, 共 14 次出现)。声称数错但无漏改。修法: 不写数, 或写「三文件全部落点」。
- **m-2** `detailed-tasks.yaml:51` 「R5 前机械收口 (bfe8285d)」: 与同行前文 `97a3885` 并列, 读作 commit SHA; `git cat-file -t bfe8285d` 在主仓与 aria 均 `Not a valid object name`, reflog 零命中。审计轨 §9 写的是「容器 bfe8285d」—— 它是容器 id 不是 commit。修法: 改为 `09eb919` 或标明「容器」。
- **m-3** `tasks.md:165` 写 `AB_TEST_OPERATIONS.md:396`, `detailed-tasks.yaml:909` 写 `:397`; 实读 `grep -n "Tier 1: 核心" aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` → 397。修 tasks.md。
- **m-4** `proposal.md:187` 「15/15 与下表逐格一致」 vs `proposal.md:219` 「14/14 一致」(同一节内两个数; 表内实列 15 行含 SC-12 无 baseline 行)。pre-existing, 非本两轮引入。
- **m-5** `scope_repos[主仓].head = 084209f` = `09eb919^`; 写入本 commit 的 head 天然落后一步。可接受, 但 R5 后若再收口请同批改为收口 commit 自身之前最后一个 SHA 并注明此约定。
- **m-6** `tasks.md:151` / `detailed-tasks.yaml:860` 「detailed-tasks.yaml (2 处)」: 现实跑 `grep -c sc-baseline-linked-issue-normalization detailed-tasks.yaml` = 3 (收口把 git grep 口径文本本身写进了 :860)。两处都已写「执行时重跑 git grep, 不抄此清单」, 自愈; 仅提示计数已过期。
- **m-7** memory 指针: 三文件引用的 10 个 memory 名里 9 个在本机 `memory/` 目录与 `MEMORY.md` 索引均零命中 (含 `tasks.md:146` 引的 `feedback_scoped_git_add_splits_claim_from_landing`, 即本席被指定阅读却不存在的那条); 而 `detailed-tasks.yaml:615-617` (TASK-016 notes, cancelled) 断言「`feedback_partial_push_creates_mirror_divergence` **不存在**」—— 该文件现**存在**且在索引 (`ls … | grep partial_push` 命中)。前者可能是 memory 存于另一台机器 (不在本镜头裁断), 后者是已反转的事实断言。修法: :615-617 改为「R3 时不存在, 2026-08-22 已补」。
- **m-8** `tasks.md:161` #137 更新句未同步 yaml 的新锚 `pre_merge_gate.py:547`, 仍只有 `:427` (af87cae 行号)。k=1/N=2。

### 越镜头观察 (不计数, 供判据席)

TASK-024 差集断言的排除集 (aria/VERSION · aria/CHANGELOG.md · .aria/audit-reports/** · Spec 目录订正留痕行) 对当前仓实跑 `git grep -l "1\.65\.5"` 后仍剩 `.aria/decisions/…`, `.aria/probes/…`, `.aria/state-checks.yaml`, `.aria/triage-*`, `.aria/repro/sc-baseline-…py`, `docs/handoff/**` 等命中 —— 排除集枚举与真实数据值域的关系请判据席核。

## 5. 核实为一致的清单 (供下轮免重复)

| 项 | 实跑证据 |
|---|---|
| ship_target 三头 (yaml :42 / tasks.md :6 / proposal :3 :8) + proposal Impact :272 均 v1.67.0; 无 1.66.0 残留 (仅历史叙述) | `grep -n "1\.66\.0"` 4 命中全为「原写 / 已 ship / #137 于 v1.66.0」叙述 |
| total_tasks 28 = 21 active + 7 cancelled; 编号 TASK-001..028 唯一 | dag.py |
| active parent 集 == tasks.md 21 个 checkbox 编号集; 7 cancelled parent == 7 条删除线编号 | dag.py `True set()` / `True` |
| 复杂度 S14·M6·L1 / 88h / qa10·ba7·km4 (yaml :976-977) | dag.py |
| DAG 无环; 028 在 026 之前; 024 在 028 之前; 关键路径逐字同 :970; 无序对 32 同 :967 | dag.py |
| 测试文件 (9e6a17c): 6 个既有 test 方法名逐字同 tasks.md :67; 宿主 34 个; class 起始行 206 / 527 与 proposal :269 锚一致 | python 解析 + `sed -n '206p;527p'` |
| `run_tests.py` 基线 `Ran 1322 tests / OK` | 实跑 90s |
| `pre_merge_gate.py:547` `--main-branch default="main"`; `_verify_main_branch_exists()` 在 :302, `not found on remote` 在 :457; `8683551` = `chore(release): aria-plugin v1.66.0 — #137`; CHANGELOG `## [1.66.0] - 2026-08-16` | grep / `git log -1 8683551` |
| collision.py :155 (内联 tuple) / :210 `_TERMINAL=("done","abandoned","unknown")` / :217 裸 `!=` / :228 回显 / :307 `("done","abandoned")`; docstring :182-206 | `sed -n` |
| claim_schema.py :107-114 逐字含 "Two active claims with the SAME linked_issue" | `sed -n '107,114p'` |
| SKILL.md:176 = claim 生命周期闭环行; test_collision.py :29-30 两个 sys.path.insert | `sed -n` |
| `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate-fixtures/` 存在; `ab-results/` 为主仓普通目录 | `ls -d` |
| AB_TEST_OPERATIONS.md :397 (Tier 1 10 个) / :545 (Tier 1 全量已执行) | grep |
| sc-baseline 脚本 :275-277 `measured_face != EVIDENCE_FACE → exit 1`; FATAL 找不到 proposal.md 在 :215 | `sed -n` |
| `git grep -l sc-baseline-linked-issue-normalization` 减 append-only 史 = 恰 3 个交付面文件 | git grep |
| `aria/VERSION` 第二处声明仍读 `1.47.0` (位置 :63, 见 M-3); 头行 :3 = 1.66.4; 172 行 | `sed -n 3p; wc -l` |
| `.aria/config.json` `max_rounds: 5` | grep |
| C3 更新 (「#137 已修 v1.66.0, 缺省仍 main, (b) 腿解除, (a) 腿归 #152」) 在 yaml :86-94 与 tasks.md :161 两处都落 | grep |
| 5.8 → 5.12 指针 (tasks.md :187); 余下 `5.8` 全为范围语或 cancelled 自述 | grep |
| 收口 diff 未碰 `1.65.5` 旧值 (见 M-2, 反向证据) | `git show 09eb919 … grep -c` = 0 |

## 6. Verdict

- Critical: **1** (C-1)
- Major: **6** (M-1 … M-6)
- Minor: **8** (m-1 … m-8)
- **vote: REVISE** (Critical ≥ 1 且 Major ≥ 3, 两条阈值都触发)

其中「由 R4-fix 或 2026-08-22 收口 (commit 09eb919) 引入」的 major: **5** 条 (M-1 / M-2 / M-3 由 09eb919 收口引入; M-4 / M-5 由 97a3885 R4-fix 落地不完整引入; M-6 为更早遗留, C-1 的假声称句由 R4-fix 引入但不计入 major)。

形状总结 (供 owner 看趋势, 非 finding): 本轮 7 条 C/M 里 6 条仍是同一形状 —— 「改了 k<N 处」(C-1 / M-4 / M-5 / M-6) 与「改了主字段没改随它失效的派生字段」(M-1 deliverables→并行边, M-2 新值→旧值, M-3 head→行号锚)。机械核验 10 项 (R4-fix 自述) 全部再次通过, 但它们核的是派生值, 不核「同一事实的 N 个散文落点」; 散文落点的 N 只能靠 grep 同义词枚举, 本报告 §2 的 N/k 表即可直接当下一次 fix 的清单。
