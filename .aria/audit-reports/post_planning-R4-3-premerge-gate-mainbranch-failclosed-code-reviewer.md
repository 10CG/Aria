---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-12T01:49:27.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R4 — code-reviewer 席位报告

## 0. 被审对象的口径更正 (先写, 因为它影响本报告一切数字的可比性)

任务书正文写「被审对象 = R2-fix 后的 A.2 产物 (`0dd26ce`)」, 并要求逐条标 `introduced_by_r2fix`。
**实测该描述已陈旧**:

```
$ git log --oneline -1 -- openspec/changes/premerge-gate-mainbranch-failclosed/
e970943 docs(spec): R3-fix — 不再做第四次同形换量, 改为「停止预写量 + 诚实上报」; xcheck 补齐维度
$ git diff --numstat 0dd26ce..HEAD -- openspec/changes/premerge-gate-mainbranch-failclosed/
305  69  detailed-tasks.yaml
42   14  proposal.md
64   28  tasks.md
```

post_planning **R3 已跑完** (5 席报告 + aggregate 均已落盘, `post_planning-R3-*`), R3-fix 已 commit。
交付契约的文件名 (`R4-3`) 与 frontmatter (`rounds: 4`) 与此一致。

⇒ **本报告审的是 HEAD = `e970943` (R3-fix 产物)**; `introduced_by_r2fix` 字段一律按
「**是否由 R3-fix 这一轮引入**」填写, 每条 finding 的 evidence 里写明依据 (diff 中该句是否为 `+` 行)。
若编排层要的是别的口径, 请以本节为准重新解读该字段, **不要**把它读成 R2-fix。

---

## 1. 投票

**VOTE: REVISE** · **VERDICT: FAIL** (1 Critical + 4 Major + 6 minor = 11) · **blocks_phase_b: 3**

---

## 2. 先说做对的 (逐条实跑核过, 不是客套)

我这一席的职责是逐字核对。**本轮的 file:line 与今日计数质量是八轮里最好的一版**:

- **抽查 77 处行锚, 零错**: `pre_merge_gate.py` 26 处 (`:21 :47-49 :56 :68 :101 :111 :116 :120 :121 :300
  :325 :326 :328 :337 :338 :339 :344 :345 :356 :357 :358 :366 :427 :435`) · `SKILL.md` 33 处
  (`:48 :49 :99 :101 :167 :168 :189-191 :216 :218 :240 :242 :243 :244 :252 :255 :262 :267 :270 :279
  :285 :286 :310 :349 :350 :351 :392 :557 :559 :610 :737 :742`) · `test_pre_merge_gate.py` 8 处 ·
  跨文件 10 处 (`aether.py:38/:164/:168/:176/:180/:187` · `path_coverage.py:78/:93` ·
  `base.py:29` · `__init__.py:17` · `github_actions.py:37-42` · `submodule-gate-telemetry.sh:60-62` ·
  `workflow-runner/SKILL.md:354-357` · `worktree_manager.py:170` · `sync-detection.md:587`)。
  逐行 `sed -n 'Np'` 读过, **全部与文中逐字引用一致**。R3 抓到的 §6.1 承重理由错误 (`:337/:339`
  消费的是翻译后的新键、旧键首个消费者是 `:325`) **已正确闭合**, 且新增的「判定读原始 `config`」
  条款与 `:101/:111/:120/:121/:325/:326` 实读完全吻合。
- **SC 表 20 行的「今日实测」全部可复现**: 我独立复跑 (不采信 CHECK5 的输出),
  `4 / 1 / 0 / 0 / 0 / 1,1,1 / 1 / … / 0 / 2 / 2,4,3,0` **逐个对上**。R3 抓到的 SC-M16 假值 (声称 1
  实为 0) 在 proposal SC 表与 TASK-001 两处**已改对** (但第三处没改, 见 M1)。
- **拓扑声称可复现**: `TASK-001 是其余 20 条全部的传递祖先` ✓ · `与 TASK-015 无序的恰是
  016/017/018 且无一交付 SKILL.md` ✓ · `TASK-009.dependencies=[TASK-008], 008=L5 / 009=L6` ✓。
- **跨仓命令可执行**: `git -C aria rev-parse HEAD:skills/phase-c-integrator/SKILL.md` → rc=0 ✓ ·
  `git rev-parse HEAD:aria` → `af87caeeed88af6af76f29a8002badbe1228d927`, **与 `git -C aria rev-parse
  HEAD` 相等** ⇒ 全部 `af87cae` 基线行锚今日有效 ✓ · 主仓 `VERSION`=1.7.3 vs `plugin.json`=1.65.5 ✓
  (「永远不该相等」的论证成立, `CLAUDE.md:80` 逐字只规定 4 个派生文件)。
- **`TASK-014` 的处置我判「是诚实标注, 不是变相回避」**: 「A.2 阶段预写一个关于未来产物的量」
  这个根因诊断是对的; 把判据产出时点移到 TASK-002、把无法机械表达的残余**显式列为 owner 裁量项**,
  比第五个假量正确。执笔方当场自查抓到「判据串写进正文 ⇒ 它自己恒绿」并换成 `^#### ` 标题锚定,
  实跑今日 = 0 ✓ —— 这段留痕本身是本轮最有价值的产出。
  **但这个处方有一个结构性漏洞, 见 C1 —— 它不是「量对不对」的问题, 是「没人负责交付那个判据」。**

---

## 3. Findings

### C1 (Critical, blocks_phase_b, 本轮引入) — TASK-014 的唯一验收基座没有任何任务负责交付

**位置**: `detailed-tasks.yaml:624-631` (TASK-014 verification (1)) vs `detailed-tasks.yaml:205-227`
(TASK-002 的 deliverables + verification) · `proposal.md:105` · `tasks.md:104` / `tasks.md:35-40`

TASK-014 本轮把全部验收改为「执行 proposal §1 那个小节给出的命令」, 而该小节须由 TASK-002 建:

```
detailed-tasks.yaml:624  '**(1) 验收判据由 TASK-002 随 F 一并产出**: TASK-002 回写 proposal §1 时须建一个**四级标题小节**,
detailed-tasks.yaml:625   标题行逐字为 `#### TASK-014 验收判据 (由 TASK-002 spike 产出)`, 内含**可复跑命令 + 期望值**。
proposal.md:105          1. **TASK-002 的 deliverable 增加一项**: 回写 proposal §1 时 … 必须同时写下 TASK-014 的可复跑验收命令与期望值
```

**实跑核验 TASK-002 那一侧**:

```bash
$ python3 -c "…yaml.safe_load…; t=TASK-002; print(t['deliverables'])"
['spike 结论回写 openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md §1']
$ python3 -c "… print('验收判据' 出现次数:', json.dumps(t,ensure_ascii=False).count('验收判据'))"
0
$ grep -n 'TASK-014 验收判据' proposal.md tasks.md detailed-tasks.yaml
tasks.md:104 / :105 / :106 / :185          ← 全在 TASK-014 自己的段落与「已裁」段
proposal.md:105 / :107 / :108
detailed-tasks.yaml:625 / :629 / :632 / :672   ← 全在 TASK-014 自己的 block
```

⇒ **`proposal.md:105` 逐字声称「TASK-002 的 deliverable 增加一项」, 而三份文件里 TASK-002 的
deliverables 与 verification 对它零提及**。TASK-002 可以完整通过自己全部 7 条 verification
(SC-M12 五 cwd / abort 双向 / 先定锚点 / 变量归属 / `:242` 作用域 / 先例援引 / 行号护栏) 而**不写那个小节**;
届时 TASK-014 的今日红 (`grep -cE '^#### +TASK-014 验收判据' proposal.md` = 0) **永远不会转绿**,
且**没有任何任务的交付面装得下它** ⇒ DAG 上的结构性死锁。

**它怎么会红**: 把该小节写进 `TASK-002.deliverables` (或加一条 verification) 即闭合;
不加则 TASK-014 结构上无法开工 —— 这正是本条可证伪的判据。

**为什么是 Critical**: 这是 R2 命名的两个失效形状里的**第二个 (移交给没核过的下游)** 的原样复发,
发生在**为关闭第一个形状而新写的处方内部**; 更尖锐的是 —— R3-fix **同一轮**刚给 TASK-011 修过
一模一样的东西 (`detailed-tasks.yaml:516-519` 逐字:「上一版这条要求只活在 notes 里而不在 deliverables
⇒ 不回写时**交付面上无任何缺失可被机械发现**」), 却**没把同一条推理用在自己新造的 TASK-002 移交上**。
memory `fix-the-class` + `delegate-verify` 同时命中。

**xcheck 为什么没抓到**: CHECK1 只验「点名的 TASK 与 DAG 方向是否一致」—— TASK-014→TASK-002 的边
方向正确, 故 PASS; 没有任何一项检查问「被移交方的交付面装得下这件事吗」。

---

### M1 (Major, blocks_phase_b, 本轮引入) — SC-M16 三个落点只改了两个, 第三处与前两处直接矛盾

**位置**: `detailed-tasks.yaml:540` (TASK-011, SC-M16 的**唯一转绿 owner**) vs `proposal.md:327` (SC 表)
+ `detailed-tasks.yaml:179` (TASK-001 红窗)

```
proposal.md:327          | **SC-M16** | … | **≥1** | **0** | **必红** —— 它是 **baseline-failing 断言, 不是守恒断言**。
detailed-tasks.yaml:179  **SC-M16** 折叠块外 <MAIN_BRANCH> 取值来源段落数 **今日实测 0** → 期望 ≥1 ⇒ RED (转绿 TASK-011)
detailed-tasks.yaml:540  ⚠️ 今日计数 = 1 但**不是正面证据** (今日无折叠块, 任何行都在块外); 本条守的是「落地后不掉到 0」。
```

**实跑**: `grep -c -- '<MAIN_BRANCH>' aria/skills/phase-c-integrator/SKILL.md` → **0**
⇒ 满足 SC-M16 判据 (同时含 `<MAIN_BRANCH>` 且含「本项目」或 `master` 的块外段落) 的段落数**今日必为 0**。
`:540` 的「今日计数 = 1」用的是 **SC-M16 被重定义之前**的旧判据 (只数含 master 的行)。

**确认由本轮引入**:

```bash
$ git show 0dd26ce:…/detailed-tasks.yaml | grep -n '今日计数 = 1'   → 443: (同一句)
$ grep -n '今日计数 = 1' …/detailed-tasks.yaml                      → 540: (同一句, 本轮 diff 未触及)
$ git show 0dd26ce:…/proposal.md | grep -n 'SC-M16'
  300: … | **≥1** | **1** (`:242` …) | **守恒断言** …
```

⇒ 上一版**三处口径一致地错** (都写 1 / 都叫守恒断言); 本轮把 proposal 与 TASK-001 改成
「0 / baseline-failing / 必红」, **唯独漏了唯一负责让它转绿的 TASK-011** ⇒ **矛盾是这一轮制造出来的**。
读 TASK-011 的实施者会认为该条今日已满足、只需「别弄丢」, 读 TASK-001 的实施者要为它建红窗 ——
两个独立实施者对同一条 SC 得相反的起始状态 (memory `spec-underdetermination`)。

**它怎么会红**: 把 `:540` 改成「今日 0, baseline-failing, 须由本任务从 0 转 ≥1」即闭合。

**xcheck 为什么没抓到**: CHECK5 只对 **proposal SC 表**那一列回源, 对 yaml/tasks.md 里**复述**的
同名今日值零覆盖 —— 这是 CHECK5 自身「只修实例不修类」的直接后果 (R3 抓到的假值恰好在 SC 表里)。

---

### M2 (Major, blocks_phase_b, 本轮引入) — TASK-014 的替代验收违反本轮刚立的 `evaluation_time_convention`

**位置**: `detailed-tasks.yaml:636-638` (verification (2), 本轮新增) 与 `:648` (负控条) vs
`detailed-tasks.yaml:75-84` (本轮新增的全局规则)

```
detailed-tasks.yaml:78   **任一 task 的每条 verification 必须在「该 task 完成的那一刻」可求值。**
detailed-tasks.yaml:636  '**(2) 不新造第 N+1 套**: 本 change 的 diff 里**新增或改动**的每一处 helper 定位表达 … 须符合同一小节给出的判据。'
detailed-tasks.yaml:648  '负控 (封闭白名单, 之外零例外): :310 · :392 · :557 · :610 · :737 在本 change 的 diff 中零改动。'
```

**实跑拓扑**:

```
L4: TASK-005, TASK-014          ← 本任务在此求值
L7: TASK-012, TASK-013, TASK-020
TASK-014 的后代中交付 phase-c-integrator/SKILL.md 的: ['TASK-020']
```

⇒ 在 TASK-014 完成那一刻,「本 change 的 diff」**还缺 L5–L9 全部改动**, 其中 TASK-020 就在改同一个
`SKILL.md`。这**逐字就是本轮用来作废旧量 (d) 的第三条理由**:

```
detailed-tasks.yaml:670  作废 (d) … 且它断言「本 change 的 diff」而本任务在拓扑 L4 求值、同文件还有 L7 的任务在改。
```

⇒ 新写的 (2) 与负控条**继承了被作废量的同一处病灶**, 而杀死旧量的三条理由里就有这一条
(memory `fix-recurs-in-fallback`)。本轮新立的规则 (2)「必须拆成 Phase B 可求值的那半 + 明确移交的那半」
在自己文件里没有被 sweep。

**它怎么会红**: 把 (2) 与负控条按 `evaluation_time_convention` 规则 (1)/(2) 拆半, 或把终局判定
明确移交 TASK-021 (它在 L8, 是唯一同时看得见全部 diff 的点)。

---

### M3 (Major, 本轮引入) — `tasks.md:7` 逐字声称的「R3 那 5 个构造原样复现全部被拒」对 T2 不成立

**位置**: `tasks.md:7` (其依据 `xcheck_adversarial.py` 不在仓内, 但该声称写在被审交付物里)

```
tasks.md:7  … **每项都以「好实现 PASS + 像样的坏实现 FAIL」的对抗 fixture 验过拒绝能力**
            (12/12 构造被拒, 含 R3 那 5 个原样复现)。
```

我复跑了他们的 harness (确认打印 `汇总: 12/12 个坏实现被正确拒绝`), 而 T2 那一行的拒绝理由
**里没有 SC-M6**:

```
[OK] CHECK2  T2 删掉 SC-M6 真 owner(TASK-008) 的 verification → FAIL
     - CHECK2: SC-M7 无转绿认领者 … / SC-M8 … / SC-M14 …
```

他们的 fixture 删的是一整条 bullet, 里面同时装着 M6/M7/M8/M13/M14 五条 SC; 让它变红的是 M7/M8/M14,
**R3/T2 点名的那条 (SC-M6) 仍然 ✓**。

**定点复现** (只删 SC-M6 那半句认领, 其余原样保留) — `scratchpad/cr4/t4b`:

```
$ python3 xcheck.py …/cr4/t4b --repo-root /home/dev/Aria
  SC-M6    转绿认领=TASK-003✗,TASK-008✓,TASK-009✗,TASK-021✗  红窗=-  ✓
RESULT: PASS — 六项交叉检查全部通过        (exit=0)
```

**放行原因**: TASK-008 另一条 bullet 里的**免责句**「⚠️ SC-M6/SC-M13 的场景**都有命中**, 结构上碰不到
这条分支, **不能靠它们代管**」被 CHECK2 记成了对 SC-M6 的**转绿认领** —— 一句语义上说「这两条 SC
覆盖不到」的话, 被当成了「我负责让它绿」。memory `test-claims-vs-verifies` (fixture 的名字声称的 ≠
它真验证的)。

**它怎么会红**: 把 T2 fixture 收窄到只删 SC-M6 那半句 (即 t4b), harness 立刻从 12/12 掉到 11/12。

---

### M4 (Major, 本轮引入) — 机械交叉检查在两条承重维度上仍可被穿过 (我构造的坏实现全绿)

**位置**: `xcheck.py` CHECK4 / CHECK1 (声称落在 `tasks.md:7` 与 `detailed-tasks.yaml:129-131`)

**(a) CHECK4 根本没有解析到 §6.1 承重的那条真指令。** 基线运行打印的三元组里,
`(legacy-key fail-CLOSED, resolve_ci_backend)` **整对缺席**:

```
  legacy-key fail-CLOSED @ _normalize_config   指令: 禁止放于此
  legacy-key fail-CLOSED @ enabled 早退         指令: 之后/放于此
  存在性核验              @ _normalize_config   指令: 禁止放于此
  存在性核验              @ enabled 早退         指令: 之后
  存在性核验              @ path coverage       指令: 之前
```

而 §6.1 的承重半边逐字是「**在 `resolve_ci_backend` 之前**」(`proposal.md:235`) —— 它写成
「以锚点开头的处方句」, 落在 xcheck 自己注释承认的覆盖边界外 (`xcheck.py:365-366`)。
**后果实测** (`scratchpad/cr4/t9`): 往 TASK-020 注入一条与它直接相反的指令
「legacy-key 硬失败的判定点须钉死在 `resolve_ci_backend` **之后**」——

```
  legacy-key fail-CLOSED @ resolve_ci_backend  指令: 之后   ← 只有我注入的这条, 无冲突可判
RESULT: PASS — 六项交叉检查全部通过        (exit=0)
```

而 §6.1 逐字写着这个错法「**正是 TASK-020 要治的那条 fail-OPEN 原样复发**」。
⇒ **本 change 唯一 Critical 的承重半边恰好落在这道检查的盲区里**, 输出还打印一行安心的「指令: 之后」。

**(b) CHECK1 只对 15 个固定句式定向, 其余边完全无向。** 我把**最大位移源** TASK-011 反排到依赖它的
内容锚使用者 TASK-013 **之后** (无环, `scratchpad/cr4/t6`):

```
011 deps ['TASK-002','TASK-003','TASK-013']   013 deps ['TASK-009']
RESULT: PASS — 六项交叉检查全部通过        (exit=0)
```

此时 TASK-013 自己的 verification 仍逐字写着「TASK-011 改动 :99-:216 与 :218 起两段 ⇒ :267/:270/:279
全部前后移」——**文本与 DAG 直接矛盾, 六项检查无一发红**。这是 R3/T6「边反向仍 PASS」在另一条边上的
复现: 改成单向后, 覆盖面从「全部边」缩到「yaml 里恰好用了那 15 个句式的边」。
(他们自己的 CHECK1 fixture `rev_15_21` 被拒, 是因为 TASK-015 文本里恰有 `dependencies += TASK-021`。)

**它怎么会红**: (a) 把 PRESCRIBE 闸改成「锚点开头的处方句也算」, 或把 §6.1 两条指令直接做成断言表;
(b) 对**每条**依赖边要求两侧文本可判方向, 判不出就报「未覆盖」而非静默放过。

---

### m1 (minor, 本轮引入) — CHECK5 有两个放行洞, 其中一个今日就有活着的未核数字

- **洞 1 (非数字即跳过)**: 把 SC-M5 今日实测由 `**1**` 换成 `—` (`scratchpad/cr4/t3b`) ⇒ `RESULT: PASS`。
  静默丢弃比伪造更常见, 而**零证据被当成正证据** (memory `feedback_invariant_needs_failclosed_default`)。
  ⚠️ 主 loop 已在 commit message 自陈过这一条, 我在另一行上独立复现。
- **洞 2 (前缀比较, 主 loop 未自陈)**: `xcheck.py:569` 是 `ok = actual == claimed[:len(actual)]`
  ⇒ 单元格里**第 2 个及以后的数字永不被核**。实测把 SC-M15 的「今日 `<details>` 块数 = 0」改成「= 77」
  (`scratchpad/cr4/t1`) ⇒ `SC-M15 声称 [0, 77] 实跑 [0] ✓` → `RESULT: PASS`。
  **今日就有活实例**: SC-M15 那个「块数 = 0」今日无人回源 (恰好为真, 但不是被验过的真)。

### m2 (minor, 本轮引入) — TASK-001「20 行 = 16 行有红窗 + 4 行结构上不可能有」分类不自洽

`detailed-tasks.yaml:185-188` 把 **SC-M10/M11/M12/M15** 划为「结构上不可能有红窗」(负控 / 今日期望值
已满足 / 空真), 却把 **SC-M3b/SC-M3c** 算进「16 行有红窗」—— 而同一份文件逐字把它们描述为
「**负控, 今日已 0**」(`:151-161`), SC-M3c 更逐字写着「**今日的 0 是空真**」。同性质两组被分到相反两侧,
而「无剩余缺口」的结论正建立在这个分区上。统一口径应是「14 行真红窗 + 6 行结构上不可能」。
**它怎么会红**: 复核者按 title「先看到**全红**」去数 16 行, 会数出 14 红 2 绿。

### m3 (minor, 本轮引入) — TASK-021 与 TASK-005「同步收窄」后仍差一行

`detailed-tasks.yaml:1073` 写「行号锚 (`:710` 至 `:723` = test_sc22 **函数体区间**)」, 而同一 block 上一条
(`:1070`) 与 TASK-005 (`:327`) 都写 `:710-724`, 且 TASK-005 明确要求 **(c) 末行
`self.assertEqual(out["verdict"], "green")` 逐字不变** —— 实读该行正是 `:724`:

```
 723: out = gate.gate_check(pr_branch="feat/x")
 724: self.assertEqual(out["verdict"], "green")
```

**它怎么会红**: 按 `:710-:723` 取函数体的复核者不会核 `:724`, 而 TASK-005 的 (c) 恰好只保护那一行。

### m4 (minor, 本轮引入) — SC-M18 把 `pre_merge_gate.py:68` 的逐字内容说错

`detailed-tasks.yaml:1027-1028` / `tasks.md:148` / `proposal.md:329` 逐字写
「`pre_merge_gate.py:68`/`:116` 的 **`will be removed in v2.0`** 原样留在已发布的 v2.0.0 里」。实读:

```
  68| # Old keys still readable until v2.0; new key wins on conflict (Hard #9).
 116|                     f"will be removed in v2.0",
```

⇒ `:68` 命中的是 pattern 的 `still readable` 分支, **不含** `will be removed in v2.0` 那个串。
计数 (2) 与 SC 本身没错, 错的是承重论证里的逐字引用。
**它怎么会红**: 只在 `:68` 上跑 `grep 'will be removed in v2.0'` ⇒ 0 命中。

### m5 (minor, 非本轮引入) — TASK-010「补完后应为 24/24」在其自陈计数法下对 6 处调用不可达

`detailed-tasks.yaml:488-493` 把 24 的计数法钉为「含 `gate_check(` 的**行数**」, 并要求「补完后应为 24/24」。
实跑该文件 24 个 `gate_check(` 行中 **6 行是多行调用** (`:311 :321 :394 :524 :654 :675`):

```
$ grep -n 'gate_check(' tests/test_pre_merge_gate.py | grep -vc ')'
6
```

⇒ 这 6 处补参后 `main_branch=` 自然落在续行上, 按「行数」重算只能得 18/24。两种读法 (调用点粒度 vs
行粒度) 给出不同结论 = 欠定。**它怎么会红**: 实施者按自陈计数法自查时得 18/24。
⚠️ 顺带核实一条**不是缺陷**的:「显式传 `main_branch` 的 **0** 处」是对的 —— 唯一含 `main_branch` 的
`:669` 属 `self.pc_eval.assert_called_once_with(...)`, 不是 `gate_check(` 调用点。

### m6 (minor, 非本轮引入) — SC-M3b 的拒绝域不含 `--main-branch=main|master`

`proposal.md:311` 的 canonical pattern 要求 `--main-branch` 与值之间有**空格** (` +`)。合成 fixture 实测:

```
$ grep -cE -- "--main-branch +['\"]?(main|master)['\"]?([[:space:]]|$)" m3b.txt
2      ← 命中 `--main-branch "master"` 与 `--main-branch master`
       ← 未命中 `--main-branch=master` / `--main-branch=main`
```

R2 已因「声称强于拒绝域」修过一次 (补引号), **同族第三种形态 (`=`) 没被 sweep**。SC-M3b 是防 PC1 回归的
唯一机械腿, 一条 `--main-branch=main` 示例可从中逃逸且 SC-M1/M2/M3a/M3c/M15 全不覆盖它。
**它怎么会红**: pattern 改成 `--main-branch[ =]+…`。

---

## 4. R3 (上一轮) 闭合情况 — 逐条回源, 不采信「已修」的声称

| R3 结论 | 本轮实测 | 判定 |
|---|---|---|
| C: TASK-014 第四版验收量结构上不可满足 | 已停止预写量, 改由 TASK-002 产出判据; 今日红 `grep -cE '^#### +TASK-014 验收判据'` = **0** 实跑确认 | **方向闭合, 但基座无人交付 ⇒ C1** |
| C(code-reviewer): TASK-005/021「函数体零改动」恒红 | 两处均已收窄为「除 `gate_check(` 那行补必填实参外零改动」; patch 目标 / `_forbidden` / 末行断言三处引用逐字属实 | **闭合** (右端点差一行 → m3) |
| 事实错误 1: §6.1 承重理由与代码不符 | `:101/:111/:120/:121/:325/:326/:328/:337/:339` 全部实读吻合; 新增「判定读原始 `config`」条款正确 | **闭合** |
| 事实错误 2: SC-M16「今日实测 1」是假的 | proposal + TASK-001 已改为 0 / baseline-failing | **两处闭合, 第三处 (TASK-011) 未改且现在自相矛盾 ⇒ M1** |
| 事实错误 3: TASK-015 blob-SHA 命令主仓 rc=128 | `git -C aria rev-parse HEAD:skills/…` rc=0 实跑确认; 已拆成 [Phase B 可求值] + [Phase C 明确移交] | **闭合** |
| 组号↔DAG 7 处倒置 | TASK-005→TG-1 / TASK-021→TG-3 已归位; 现存唯一倒置 (015 dep 019) 有成文理由; CHECK6 实跑仅此一条 | **闭合** |
| 红窗只覆盖 9/20 行 | 扩到 16 行 + 明列 4 行不可能 | **闭合** (分类口径不自洽 → m2) |
| 发版面缺第 9 项 gitlink | 已补, `git rev-parse HEAD:aria` 判据实跑 rc=0 且值与子模块 HEAD 相等 | **闭合** |
| TASK-016 纯散文无量化断言 | 已补 `grep -cE '分支存在性|main-branch-not-found' CLAUDE.md` 今日实跑 **0** → ≥1, 且诚实标注「必要不充分」 | **闭合** |
| SC-M18 (删除面其余四文件) | 今日值 2/4/3/0 实跑确认 | **闭合** (逐字引用错 → m4) |
| **那道机械交叉检查被证伪** | 重写后确有真拒绝能力 (我的 T7a/T7b/T8 被拒), **但我另造的 4 个坏实现全绿** | **部分闭合 ⇒ M3/M4/m1** |

**去重后仍开着的**: C1 (新) · M1 (旧缺陷的新矛盾面) · M2 (新) · M3/M4/m1 (机制) · m2–m6。

---

## 5. 对那道机械交叉检查的评估 (本轮核心问题)

**它比上一版真的强了 —— 但不足以承担被赋予的角色, 且它自己就是「只修实例不修类」的产物。**

**真有拒绝能力的 (我自己造的坏实现被拒, 不是复核当前取值)**:

| 我的构造 | 结果 |
|---|---|
| T7a 给 TASK-013 加一个无护栏的行号锚 `:812` | **FAIL** ✅ `CHECK3(c)` 逐锚点判定生效 |
| T7b 给 TASK-013 写「落地复核一律**以行号为准**」 | **FAIL** ✅ `CHECK3(a)` 反护栏生效 |
| T8 新造「存在性核验须在 `enabled` 早退**之前**」(与既有「之后」相反) | **FAIL** ✅ `CHECK4` 同对冲突生效 |
| T2' SC-M2 今日 1→3 | **FAIL** ✅ `CHECK5` 单数字回源生效 |

**仍被穿过的 (5 个构造)**:

| 我的构造 | 结果 | 病因 |
|---|---|---|
| t4b 定点删掉 SC-M6 真 owner 的认领 (= R3/T2 的真形态) | **PASS** | CHECK2 把「SC-M6/M13 覆盖不到这条分支」这句**免责说明**当成转绿认领 |
| t6 把最大位移源 TASK-011 反排到 TASK-013 之后 (无环) | **PASS** | CHECK1 单向化后只覆盖 15 个固定句式的边 |
| t9 注入「legacy-key 硬失败放在 `resolve_ci_backend` **之后**」 | **PASS** | CHECK4 **从未解析到** §6.1 那条「之前」真指令 |
| t1 把 SC-M15 今日单元格第二个数字改成 77 | **PASS** | CHECK5 前缀比较 |
| t3b 把 SC-M5 今日实测整格换成「—」 | **PASS** | 非数字即跳过 (零证据当正证据) |

**逐条回答任务书的四个问题**:

1. **四(六)项判据覆盖得住 R2 那两个形状吗?** —— **覆盖不全**。「只修实例不修类」**根本没有对应判据**
   (没有任何一项在问「这个形状还有几个兄弟位置」), 我本轮抓到的 M1/m2/m3/m6 全属该形状、全部逃过。
   「移交给没核过的下游」只被 CHECK1 覆盖了**方向**这一半, **没覆盖「被移交方装得下吗」这一半** ——
   C1 就是从这个缺口掉下去的。
2. **有没有恒绿的判据?** —— CHECK4 的**回归性子项**三条仍是硬编码字符串存在性, 只防删除、对新矛盾恒绿
   (脚本自己诚实标注了, `xcheck.py:431`, 我确认属实); CHECK5 对非数字单元格恒绿 (m1)。
3. **它自己是不是「只修实例不修类」的产物?** —— **是, 证据是硬的**: `SUBJECT`/`ANCHOR` (`:339-350`)
   硬编码本 Spec 两个插入点与 `_normalize_config`/`resolve_ci_backend` 等专属符号; `CUSTOM` (`:535`)
   为 SC-M3c/M15/M16 各写一个专用算法; `SC_M18_FILES` (`:523`) 硬编码四个文件路径;
   CHECK5 只覆盖 **proposal SC 表**这一个实例, 对 yaml/tasks.md 复述的同批今日值零覆盖 —— **M1 就活在那里**。
4. **拒绝能力 vs 当前取值** —— 我改了 9 处再跑, 4 拒 5 过, 见上两表。
   `tasks.md:7` 的「12/12 构造被拒, 含 R3 那 5 个原样复现」**对 T2 不成立** (M3)。

**结论**: 这道检查值得保留 (它确实抓到过本轮 fix 自己引入的东西), 但**不能再被写成「R2 两个形状已被
机械杜绝」**; 它当前是「一组对已知实例的回归测试 + 三项有真拒绝力的通用检查」。
memory `invariant-dimension`「机械不变量的维度须匹配错误的维度」在 CHECK4/CHECK1 上**仍然成立**:
本轮补上了「方向」维度的一部分, **没补「类推广性」维度** —— 而本轮 11 条 findings 里有 5 条正是那个维度。

---

## 6. 本轮 fix 引入占比 (量化, 带三项口径)

**总体** = 我这一席在 HEAD (`e970943`) 上开出的 **11 条 findings**;
**范围** = `proposal.md` / `tasks.md` / `detailed-tasks.yaml` 三件套 + `tasks.md:7` 对 xcheck 的声称;
**计数法** = 逐条二分标注「该缺陷是否由 `0dd26ce..e970943` 这次 diff 引入」, 依据写在每条 evidence 里。

| | 条数 |
|---|---|
| 由 R3-fix 引入 | **9** (C1 · M1 · M2 · M3 · M4 · m1 · m2 · m3 · m4) |
| 非本轮引入 | 2 (m5 · m6) |
| **占比** | **9/11 = 82%** |

⚠️ **与 53% / 70% 不可直接比较**: 那两个数是**五席去重后**的总体, 我这个是**单席未去重**的总体
(memory `critique-repeats-error` —— 总体不同就只能写「不可比」)。
可以说的是: **在我这一席的口径下本轮没有低于 50%**, 且最重的两条 (C1/M2) 都长在本轮新写的处方内部 ——
「改动量最大处正是新缺陷最集中处」这条历史规律**在本轮继续成立**。

---

## 7. 阻塞项 (blocks_phase_b = 3)

1. **C1** — TASK-002 的 deliverables/verification 必须写进「`#### TASK-014 验收判据 (由 TASK-002 spike 产出)`
   小节」这一项, 否则 TASK-014 结构上无法开工。
2. **M1** — `detailed-tasks.yaml:540` (TASK-011 的 SC-M16 条) 必须改成「今日 0 / baseline-failing /
   本任务负责由 0 转 ≥1」, 与 proposal SC 表和 TASK-001 对齐。
3. **M2** — TASK-014 的 verification (2) 与负控条必须按本轮自立的 `evaluation_time_convention` 拆半
   (或明确移交 TASK-021)。

非阻塞但建议同批: M3/M4 (把 `tasks.md:7` 的声称降到实测支持得住的强度 + 补 CHECK4 对
「`resolve_ci_backend` 之前」的解析) · m1–m6。

---

## 8. 一句话评估

**方向仍然全对, 逐字质量是八轮最好的一版, 但 R2 命名的第二个形状 (「移交给没核过的下游」) 在
为关闭第一个形状而新写的处方里原样复发, 且同一轮刚给 TASK-011 修过一模一样的东西 ——
真正没被补上的维度不是「方向」而是「类推广性」, 而那道机械检查对这个维度没有任何判据。**
