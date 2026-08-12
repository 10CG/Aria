---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T04:30:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R4 — knowledge-manager 席位报告

## 0. 被审对象的更正 (与 R4-0/R4-1/R4-2 同一口径, 独立复核)

任务书正文写「R3 — 被审对象 = R2-fix 后的 A.2 产物 (commit `0dd26ce`)」。实跑核验:

```
$ git rev-parse HEAD
e9709435e71d88bc4524ace7073298cfc602e793
$ git status --short openspec/changes/premerge-gate-mainbranch-failclosed/
(空 — 工作树干净)
$ git log --oneline 0dd26ce..HEAD -- openspec/changes/premerge-gate-mainbranch-failclosed/
e970943 docs(spec): R3-fix — 不再做第四次同形换量, 改为「停止预写量 + 诚实上报」; xcheck 补齐维度
$ ls .aria/audit-reports/ | grep 'post_planning-R3-.*premerge-gate' | grep -v R3-1786
post_planning-R3-0-...tech-lead.md / R3-1-...backend-architect.md / R3-2-...qa-engineer.md /
R3-3-...code-reviewer.md / R3-4-...knowledge-manager.md (+ aggregate)
```

`.aria/audit-reports/` 内已存在一轮完整真实 **post_planning R3** (5 席 + aggregate, 判 FAIL, `2C+17M+8m=27`, 10 条 `blocks_phase_b`)，随后 R3-fix 已落地 (`e970943`)。交付契约要求的文件名是 **`R4-4`**、frontmatter 要求 `rounds: 4`。

⇒ **我审的是 R3-fix 后的产物 (`e970943`, HEAD)，是 R4 的 knowledge-manager 席位。** 任务书的「R2/R2-fix」措辞是 R3 轮提示词的陈旧复制 (与 R4-0/R4-1/R4-2 三席独立复核一致)。本报告下文把 schema 字段 `introduced_by_r2fix` 读作「**由本轮被审的那次 fix (= R3-fix) 引入**」。

这本身是本 session **又一次**「共享 Spec 每次实质动作前必 fetch」的实证 (memory `feedback_concurrent_duplicate_audit_fetch_before_start`)。

---

## 1. 投票

| 项 | 值 |
|---|---|
| VOTE | **REVISE** |
| VERDICT | **PASS_WITH_WARNINGS** (0 Critical + 4 Major，我的席位范围内) |
| findings | 0C + 4M + 0m = 4 (全部知识管理/合规角度，全部新发现，未与 R4-0/1/2 已报条目重复) |
| `converged` | `null` (单席无权判收敛) |

---

## 2. R2 的 1C+~13M 是否真闭合 —— 我的角度独立抽查

R4-0 (tech-lead) 已逐条回源全部 13 条并给出完整表；R4-2 (qa-engineer) 已做独立方法抽查 3 条。我不重复整表，只用**我的席位**的方法 (合规/三件套/同步面) 独立核 4 条与知识管理直接相关的：

| R2/R3 条目 | 我的独立核验命令 | 结果 |
|---|---|---|
| config-loader 的 Rule #6 三件套 (点名行为 + 可证伪 fixture + 套件缺口 issue) | `ls aria-plugin-benchmarks/ab-suite/ \| grep -i config` → 空 (确认结构上不能照跑)；`grep -cE 'still (readable\|works)\|removed in v2\.0\|仍读\|v2\.0 移除' aria/skills/config-loader/SKILL.md` → **2** (`:249` `:257`，行号实读吻合 SC-M17 声称)；yaml `TASK-015.dependencies` 含 `TASK-019` (issue 先于归档) | ✅ 三件套齐全，闭合 |
| SC-M18 (删除面其余四文件 "→0" 断言) 今日实测 | `grep -cE '...' pre_merge_gate.py`=2 / `phase-c-integrator/SKILL.md`=4 / `test_pre_merge_gate.py`=3 / `.aria/config.template.json`=0 | ✅ 与表内声称 `2/4/3/0` 逐位吻合 |
| TASK-015 blob-SHA 命令主仓可执行性 | `git rev-parse HEAD:aria/skills/.../SKILL.md` → `fatal: ... but not in 'HEAD'` rc=**128** (确认旧版不可执行)；`git -C aria rev-parse HEAD:skills/.../SKILL.md` → rc=**0** (确认新版可执行) | ✅ R3-fix 的更正属实 |
| §Rule #6 SOT 逐字引用 (「description 或指令流程变动 ⇒ 一律第二行」/「典型: authoring 向导」) | `grep -n` `standards/conventions/skill-benchmark-exemption.md` | ✅ 两处引文逐字命中，无断章取义 |
| Rule #5 (Spec 落点) | `openspec/changes/premerge-gate-mainbranch-failclosed/` 位于主仓，非 `standards/openspec/changes/`；proposal 抬头显式声明「代码落点跨 `aria/` 子模块，Spec 落主仓 (Rule #5)」 | ✅ 合规 |

**结论**: 我核到的这几条 R2/R3 遗留在我的角度上**确已闭合**，与 R4-0/R4-2 的整体判断一致，没有发现"声称已修但实际未修"的情形。

---

## 3. 那道机械交叉检查 (`xcheck.py`) 真的有效吗 —— 我的角度: 它自己是不是一个"知识资产从未进知识库"的产物

R4-0/R4-1/R4-2 已经从**拒绝能力** (对抗构造 4/9 放行)、**维度覆盖** (只做"三份 Spec 互相对照"从不做"Spec 断言 vs 真实源码"对照)、**近邻绑定** (CHECK6 无邻近约束可被无关文本蒙混) 三个角度实证它仍是"只修实例不修类"的产物。我独立复跑确认了这些结果没有变化 (`RESULT: PASS`／对抗套件 12/12／r4_adv.py 4/9)，不再重复其分析。

**我从知识管理角度补的第四个角度、三席均未覆盖**: 这个工具本身在这个项目的知识库里**不存在**。

```
$ git ls-files | grep -i xcheck
(空)
$ find /home/dev/Aria -iname "*xcheck*" | grep -v '\.git/'
(空)
$ find /tmp/claude-1000/-home-dev-Aria/.../scratchpad -iname "*xcheck*"
.../scratchpad/xcheck.py
.../scratchpad/xcheck_adversarial.py
```

`xcheck.py`/`xcheck_adversarial.py` 只存在于**本次会话容器本地**的临时 scratchpad，从未 `git add` 进本仓任何位置 (不在 `openspec/changes/.../` 下，不在 `.aria/audit-reports/` 下，也不在 `standards/` 下)。但三份**已提交**的 Spec 文件把它当成具名、稳定、可引用的机械判据来源:

```
$ grep -n "xcheck.py" openspec/changes/premerge-gate-mainbranch-failclosed/tasks.md \
    openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
tasks.md:19:      机械判据 (xcheck.py CHECK6): 任一任务的 task_group 编号 < ...
detailed-tasks.yaml:71,84,117,129,299,896,941: (七处，含 "机械判据见 xcheck.py CHECK1" 等)
```

且它的头部 docstring 自证**已经被静默重写过一次**、没有任何 diff/版本号，唯一的变更记录是写在自己文件里的散文:

```
$ sed -n '1,19p' .../scratchpad/xcheck.py
"""条款间机械交叉检查 (post_planning R2 处置建议四项 + R3 证伪后的重写)。
⚠️ 2026-08-12 R3-fix 重写。post_planning R3/tech-lead 在副本上做 5 个对抗构造, 4 个被放行, 该版本被证伪。
   CHECK1 无向 ... → 本版按语境线索定方向, 单向断言。
   ...
```

**这是一个真实、可证伪的知识管理缺陷，不是风格问题**:

1. `tasks.md`/`detailed-tasks.yaml` 里对 `xcheck.py CHECKn` 的引用，其语义稳定性完全依赖一个**从未纳入版本控制**的文件；
2. 该文件**已经**在不留 diff 的情况下改变过语义 (4 项→6 项，CHECK1 从无向改单向等)；未来任何一轮 (含 owner 复议后可能的 R5，或 Phase C 落地前的复核) 若再次改写它，**没有任何机制能重建"当初 PASS 是在哪个版本的 CHECK 定义下取得的"**；
3. 这与本 Spec 反复强调的原则直接冲突: proposal §待 R4 重点审 第 4 条要求"请继续构造新的坏实现而不是复核它当前取值"——但连"当前取值"对应哪个源码版本都无法在仓库历史里定位，**这本身就比"复核当前取值"更弱一层**；
4. 路径本身 (`/tmp/claude-1000/-home-dev-Aria/a87f33ea-9a9d-49e2-a762-18d0fd38bfc4/scratchpad/`) 绑定到**本次会话容器 ID**，是 memory `feedback_memory_store_is_container_local_not_shared` 描述的同一类风险的更严重版本 (那条讲的是"记忆条目跨容器不可比"，这里是"被三份已提交文档具名引用的可执行判据跨容器直接消失")。

**怎么会红 (可证伪，且已实证)**: 任何非本会话容器的 agent (例如 R4-0/R4-1/R4-2 三个不同席位各自 `Task` 子进程，或未来的 Phase C 审计) 若要按 `tasks.md:19` 或 `detailed-tasks.yaml:71` 的字面指示"用 `xcheck.py CHECK6` 核验"，在**不知道这个隐藏路径**的前提下无从执行 —— 我能读到这个路径纯粹是因为本轮任务书 (§⭐ 段) 把它写在了给我的 prompt 里，这条信息**不在任何已提交文件中**，仅存在于编排层对 R3/R4 两轮的一次性口头传递。

**严重度判断**: 不阻塞 Phase B 写代码本身 (`xcheck.py` 检查的是 Spec 文档间一致性，不是被测代码的运行时正确性)，但直接损害本 Spec 自己反复强调的"可证伪 / 不采信声称 / 审计轨迹 append-only"这套方法论的可执行性 —— 定为 **Major**。

**处置建议 (供 owner 参考，我不代裁)**: 若 owner 认为这道机械检查仍要在后续轮次 (若有) 或 Phase C 收口前使用，至少应把它连同一份对抗套件提交到 `.aria/audit-reports/` 或本 change 目录下 (类似 `scripts/` 子目录)，并让 `tasks.md`/`detailed-tasks.yaml` 里的引用改指向仓内可解析路径；若不再使用，三处引用应改为纯叙事描述而非"机械判据"措辞，避免误导未来读者以为这是可复跑的东西。

---

## 4. 新发现 (本轮，均为 R4-0/R4-1/R4-2 三份报告未覆盖的角度，已逐条 grep 交叉核对)

### F-KM-1 🟠 Major — `tasks.md` 与 `detailed-tasks.yaml` 对"全局行号约定"的主仓基线 SHA 互相矛盾，且矛盾由 R3-fix 本轮新造 (只改了三处引用中的两处)

**locator**: `openspec/changes/premerge-gate-mainbranch-failclosed/tasks.md:14` vs `detailed-tasks.yaml` `metadata.line_anchor_convention` + `metadata.scope_repos[1].head`

**证据 (已实跑)**:

```
$ grep -n "主仓 = " openspec/changes/premerge-gate-mainbranch-failclosed/tasks.md
14: ... (aria = af87cae, 主仓 = 98ad1f5) ...

$ python3 -c "import yaml; d=yaml.safe_load(open('openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml')); \
  print(d['metadata']['line_anchor_convention'][:200]); print(d['metadata']['scope_repos'][1]['head'])"
...(aria = af87cae, 主仓 = 7582238)...
7582238
```

两份**同一 Level-3 三件套**内的文档，对同一个约定 (「全部 `:NNN` 行号锚以哪个主仓 commit 为基线」) 给出两个不同的字面值。追查历史:

```
$ git log -p --follow -- openspec/changes/premerge-gate-mainbranch-failclosed/tasks.md | grep -n "主仓 = "
1 处命中，出现在 R2-fix (878ee44)，此后未再改动 (含 R3-fix e970943 在内)
```

`detailed-tasks.yaml.metadata.scope_repos[1]` 自带一段说明，逐字承认这是**本轮 (R3-fix) 才做的更正**:

> 「🔴 2026-08-12 更正 (post_planning R3/code-reviewer 指出上一版 98ad1f5 已落后 2 commit)。」

即: R3-fix 把 `detailed-tasks.yaml` 里的**两处**副本 (`metadata.line_anchor_convention` 与 `metadata.scope_repos[1].head`) 都更新到了 `7582238`，但漏改了 `tasks.md:14` 里的**第三处**副本——这正是本 Spec 全程被审计追打的"只修实例不修类" (memory `fix-the-class`) 在**这一轮**、**这一处**的新实例。

**次要观察 (不单独算一条 finding，但值得记录以防被误用为"已核实"的依据)**: 该更正说明自称"落后 **2** commit"，实跑：

```
$ git merge-base --is-ancestor 98ad1f5 7582238 && echo "98ad1f5 是 7582238 的祖先"
98ad1f5 是 7582238 的祖先
$ git rev-list --count 98ad1f5..7582238
13
```

总体 = 主仓 `master` 分支、范围 = 两 SHA 之间全部可达 commit、计数法 = `git rev-list --count` → 实测 **13**，与声称的 "2" 不符 (三项口径下不可比，按字面数值判即为错误)。

**为什么最终无害 (但不因此降级为"非缺陷")**: 我核对了两个 SHA 之间 `CLAUDE.md` 与 `.aria/config.template.json` (仅有的两个被按行号引用的主仓文件) 的实际内容：

```
$ git diff 98ad1f5 7582238 -- CLAUDE.md | wc -l
0
$ git diff 98ad1f5 7582238 -- .aria/config.template.json | wc -l
0
```

两文件字节级相同，故今天不会有人因为读了不同的 SHA 而得到不同的行号锚点结果。**但这只是运气**——这套"全局行号约定"存在的**唯一目的**就是防止"两个独立执行者对同一约定得到不同答案" (`tasks.md:14` 自己的措辞)，而它自己内部现在就存在两个不同答案，只是当前恰好无行为差异。下一次任一文件在两个 SHA 之间发生真实改动 (哪怕只是给 `CLAUDE.md` 加一段) 而没人注意到这个矛盾，两个执行者就会核对出不同结果。

**怎么会红**: 让一名不知情的实施者在落地阶段核对 `CLAUDE.md:81`（发版同步面清单）是否仍命中——若他照抄 `tasks.md:14` 的 `98ad1f5` 去 `git show 98ad1f5:CLAUDE.md`，与照抄 `detailed-tasks.yaml` 的 `7582238` 去 `git show 7582238:CLAUDE.md`，得到的是两个不同 commit 的快照；虽然今天字节相同，但这条判据本身「必须只有一个基线」的**结构不变量**已经被违反，可用 `assert tasks.md 与 detailed-tasks.yaml 的主仓基线字面量相等` 这条极简机械断言直接判红（今日实测：不相等）。

**introduced_by_r3fix**: 是。

---

### F-KM-2 🟠 Major — TASK-017「主仓 gitlink」判据 (本轮新增) 没有被赋予 SC 编号，因而对本 Spec 自己的收口机制 (TASK-021 终局扫描 / xcheck CHECK2) 结构性不可见；即便 tech-lead 的 F-1 (评估时点 Critical) 被修好，这一条仍会保持不可见

**locator**: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` Impact 表「🔴 第 9 项落点 = 主仓 gitlink」段 + `detailed-tasks.yaml` `TASK-017.verification`

我已看到 tech-lead (F-1) 与 qa-engineer (F-QA-1) 独立收敛出的 Critical——「主仓 gitlink 本 change 落地 commit」这个量在 Phase B 结构上不存在，字面求值要么无法判定要么诱导 orphaned gitlink (Aria #165 同族)。这是一个真实 Critical，我认同，不重复其证据。

**我从知识管理角度补的独立缺口**: 抛开"何时能求值"这个问题不谈，即使这个判据被改写成完全可求值的形式，它现在仍然**没有 SC 编号**，因而结构上够不到本 Spec 自己的收口机制：

**证据 1 — 不在 SC 表内**:

```
$ grep -n "gitlink" openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md | grep "SC-M"
(空)
```

`SC-M1`..`SC-M18` (proposal §Success Criteria) 逐条覆盖 `phase-c-integrator`/`config-loader` 的文本断言，**没有一条**覆盖 gitlink。gitlink 判据只以自由散文的形式出现在 Impact 表与 `TASK-017.verification` 里。

**证据 2 — TASK-021 (「终局全量收口」) 的验收范围不含它，且 DAG 上无法含它**:

```
$ python3 -c "
import yaml
d=yaml.safe_load(open('openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml'))
t={x['id']:x for x in d['tasks']}
print('TASK-021 deps:', t['TASK-021']['dependencies'])
print('谁依赖 TASK-017:', [x['id'] for x in d['tasks'] if 'TASK-017' in x.get('dependencies',[])])
"
TASK-021 deps: ['TASK-008', 'TASK-009', 'TASK-010', 'TASK-011', 'TASK-012', 'TASK-013', 'TASK-014', 'TASK-020']
谁依赖 TASK-017: []
```

TASK-021 的 verification 逐字是「(1) pytest 零 failure (2) **SC-M1…SC-M18** 全部为期望值 (3) test_sc22 仍 PASS (4) 不得引入被测文件改动」——即便字面上不缺 gitlink（因为它本来就没编号），TASK-021 也在 DAG 上**排在 TASK-017 之前**（`TASK-017.dependencies` 含 `TASK-021`），结构上不可能回头核 TASK-017 的产出。而**没有任何任务依赖 TASK-017**——它是 DAG 的终端叶节点，完成后无人复核。

**证据 3 — `xcheck.py` 的 CHECK2 (SC 归属交叉检查) 结构上看不到它**（与 R4-1/backend-architect 独立指出的"CHECK2 的 `SCS` 集合逐字取自 proposal SC 表已存在的行"是同一机制，我从"gitlink 缺编号"这个具体实例复核了同一结论）:

```
$ python3 .../scratchpad/xcheck.py openspec/changes/premerge-gate-mainbranch-failclosed 2>&1 | grep -i gitlink
(空)
```

**这正是本 Spec 自己在**同一轮**创造并修复过的那个失效类**: `SC-M14` 就是"§5 catch-all 里唯一无编号的行为要求，因而不被任何机械勾稽点找到"这个问题的补丁 (proposal §Rule #6 段 / TASK-020 备注)。但 gitlink 要求——**同一轮** (R3-fix) 新增、**同一份文档**、由「post_planning R3 tech-lead 与 knowledge-manager 独立交叉命中」这样高优先级的方式引入——却没有被套上同一个补丁。这是"修类"动作本身也只修了一个实例 (SC-M14 那个) 而没有推广到这一轮新造的同形兄弟 (gitlink) 的一次新复发。

**怎么会红**: 假设 F-1 (评估时点) 被正确修复——例如判据改写为"Phase C 交接材料须包含把主仓 gitlink bump 到 aria 落地 SHA 这一步的显式清单项"。即使这样改了，因为它没有 SC 编号，`TASK-021` 完成时打印的「SC-M1..SC-M18 全部为期望值」不会包含它、`xcheck.py CHECK2` 遍历 SC 表时不会看到它，任何仅信任这两个机械勾稽点的复核者都会误以为"全部机械断言都已核验"而实际漏了这一条。这是**在关闭该类的同一轮里，由同一份文档，对同一类问题产出的又一个未覆盖实例**——与本 Spec 反复出现的模式完全同构。

**introduced_by_r3fix**: 是 (gitlink 要求本身是 R3-fix 本轮新增，故"缺 SC 编号"这个缺口也随之新造)。

---

### F-KM-3 🟡 Major — `docs/handoff/latest.md` 对本 Spec 所在 track 的指针已过期两个真实里程碑 (真实 R3 FAIL + R3-fix)，Rule #9 机读 5 字段与仓内实况不同步

**locator**: `docs/handoff/latest.md` 顶部表格行 + `docs/handoff/2026-08-11-adjudication-authoring-swap-and-the-mechanical-crosscheck.md` frontmatter

**证据 (已实跑)**:

```
$ head -15 docs/handoff/latest.md
**Latest**: [2026-08-11-adjudication-authoring-swap-and-the-mechanical-crosscheck.md](...) —
  premerge-gate-mainbranch-failclosed @ phase=A.2-audit updated=2026-08-11
...
| premerge-gate-mainbranch-failclosed | aria-runner-bot/023236f2 | A.2-audit (blocked) | [2026-08-11](...) |

$ sed -n '1,7p' docs/handoff/2026-08-11-adjudication-authoring-swap-and-the-mechanical-crosscheck.md
---
track-id: premerge-gate-mainbranch-failclosed
owner-container: aria-runner-bot/023236f2
phase: A.2-audit
status: blocked
updated-at: 2026-08-11T01:20:00Z
---
```

但该文件**本身**在 `7582238` (2026-08-12T00:26:06Z) 被追加了 24 行新内容 (§10.5，一次 Rule #10 自纠正)：

```
$ git show 7582238 --stat | grep 'crosscheck.md'
 ...authoring-swap-and-the-mechanical-crosscheck.md | 24 ++++++++++++++++++++++
$ git log -1 --format="%H %ai" -- docs/handoff/latest.md
0dd26cedb391fefe0b081a6b0544b9e6ddc3c90b 2026-08-11 01:28:31 +0000
```

即：这份 handoff 文件的正文在 08-12 追加过内容，但其 frontmatter 5 字段 (`updated-at`/`phase`/`status`) 仍停在 08-11T01:20，且 `latest.md` 本身自 `0dd26ce` (08-11 01:28) 起从未再被 touch。而仓内实况自那以后已经推进了两个真实里程碑：

```
$ git log --oneline 0dd26ce..HEAD -- openspec/changes/premerge-gate-mainbranch-failclosed/
e970943 R3-fix
（另: 真实 post_planning R3 五席 + aggregate 已于 47f94ae 前落盘, 判 FAIL）
```

`latest.md` 表格里的 `phase=A.2-audit (blocked)` 与实际当前状态 (`post_planning R3 已判 FAIL → R3-fix 已落地 → R4 五席审计进行中，本报告即其中之一`) 不符。

**为什么这是我的角度而非 R4-0/1/2 已覆盖的角度**: 三份报告聚焦 Spec 三件套本身与 `xcheck.py`；`docs/handoff/` 是 Rule #9 明确划归的 canonical 交接通道，属知识管理席位职责范围。三份报告均未提及 `latest.md` 或该 handoff 文件的 frontmatter 陈旧问题 (已 grep 交叉确认零命中)。

**不将其计入"R3-fix 引入的新缺陷"**: `e970943` (R3-fix 的实际 diff) 完全没有触碰 `docs/handoff/`，此项是一个持续存在、独立于 Spec 内容本身的编排层流程缺口。

**怎么会红**: 任何新 session/新容器若信任 `latest.md` 的机读指针 (`H5 pointer-first`，`latest.md` 自己的注释称之为"给 `collectors/handoff.py` 用的机读锚") 决定要不要认领本 track，会读到 `phase=A.2-audit (blocked)`——这与"post_planning R3 已 FAIL 且 R3-fix 已落地，当前在跑 R4 审计"这一真实阶段相差两个里程碑，存在触发 memory `feedback_concurrent_duplicate_audit_fetch_before_start` 描述的重复劳动/踩踏风险的具体路径。

**introduced_by_r3fix**: 否 (预先存在、持续未闭合的编排层流程缺口，R3-fix 本身未触及)。

---

## 5. 汇总

| # | 严重度 | 一句话 | R3-fix 引入? |
|---|---|---|---|
| F-KM-1 | Major | `tasks.md`/`detailed-tasks.yaml` 对主仓行锚基线 SHA 互相矛盾 (98ad1f5 vs 7582238)，R3-fix 只改了 yaml 侧两处副本 | 是 |
| F-KM-2 | Major | TASK-017 gitlink 判据无 SC 编号，对 TASK-021 终局收口与 `xcheck CHECK2` 结构性不可见 | 是 |
| F-KM-3 | Major | `docs/handoff/latest.md` 对本 track 的指针落后两个真实里程碑，Rule #9 5 字段与文件正文本身也不同步 | 否 (持续存在) |
| (§3) | Major | `xcheck.py`/`xcheck_adversarial.py` 从未提交进仓库，三份已提交文档具名引用一个容器本地、已被静默重写过的可执行判据 | 否 (预先存在，R3-fix 重写时未修) |

本席位在**我核到的范围内**未发现 R2/R3 遗留 Critical 未闭合的情形，也未在 SC-M17/M18/gitlink-rc0/Rule#6 引文/Rule#5 落点这几条上发现"声称已修实未修"。**我发现的 4 条都是本轮 (或历史上一直存在但本轮未修) 的新缺口，且都不与 R4-0/R4-1/R4-2 已报条目重复** (已逐条 grep 交叉确认)。

**阻塞项**: F-KM-2 与 tech-lead 的 F-1 (Critical) 属同一对象 (TASK-017 gitlink 判据)，我认为在 F-1 被正确处置之前无法独立评估 F-KM-2 是否也需要 `blocks_phase_b`——但即使 F-1 被修好，F-KM-2 描述的"无 SC 编号因而对收口机制不可见"这一问题**不会被 F-1 的修复自动带走**，需要单独处理 (建议: 若 gitlink 判据保留，赋予其一个 SC 编号并纳入某个下游收口任务的可达闭包；若因结构性不可求值而移交 follow-up，则不必赋编号，但需在 TASK-019 或对应 follow-up 里明确点名"这条不进 SC 表的理由")。

**对"那道机械交叉检查真的有效吗"的回答 (§3 之外，综合 R4-0/1/2 与本席位)**: 不。它在**当前取值**上对本 Spec 三件套返回 PASS，且有真实的、非零的拒绝能力 (对已知失效模式能报红)，但 (a) 对新构造的对抗样本仍有约一半放行率 (4/9)，(b) 结构上只能核对"三份文档互相是否自洽"、从不核对"文档断言是否与真实源码相符"，(c) 它自己作为一项知识资产从未进入版本控制，本身就是本 Spec 反复诊断的"知识与代码不同步"问题的一个实例。三轮 (post_spec 5 轮 + post_planning 3 轮) 量化数据显示的"fix 引入新缺陷占比 73–100% → 53% → 70%"这个回升趋势，我认为**不应该归咎于"换人执笔"这个手段本身**，而更可能是因为验收手段 (grep 计数 / 机械交叉检查) 与被验收对象 (自然语言 Spec 对未来代码结构的预测性主张) 之间存在根本的表达能力错配——这与 proposal 自己对 TASK-014 的诊断 ("拿 grep 计数当验收在此不适用") 是同一类问题在 Spec 全篇的推广，而不只是 TASK-014 一个任务的特例。
