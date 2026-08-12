---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-12T00:35:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — code-reviewer 席位

被审对象 = R2-fix 后的 A.2 三件套 (工作树 == HEAD `0dd26ce`, spec 目录 `git status --porcelain` 干净;
R2-fix 落在 `878ee44`)。视角: 逐字核对 file:line · 计数可复现且标计数法 · 条款间自相矛盾 ·
TASK-014 第三版验收量是否站得住。

**VOTE: REVISE · VERDICT: FAIL (1 Critical + 5 Major + 3 minor = 9)**
**本轮 9 条中 5 条由 R2-fix 引入 = 55.6%** (C-1 · M-1 · M-2 · M-3 · m-1) (总体 = 本席位 R3 全部 findings / 范围 = 三件套 /
计数法 = 逐条判 `introduced_by_r2fix`)。基线: post_spec 五轮 73–100%, R1→R2 53%。
**⇒ 没有跌破 50%; 那道机械检查没有起到它被寄予的作用 —— 下面第 4 节给出实验证据。**

---

## 0. 先说结论: 机械交叉检查在本轮的实际拒绝能力

四项里 **三项被实验证明检不出它们各自被写来检的那类缺陷**, 且第四项有一半结构上不含断言。
详见 §4 (含三个可复跑的对抗实验)。最刺眼的一条:

> 把 R2 那条 Major (TASK-010 把全量收口移交给不依赖它的 TASK-008) **原样恢复**,
> `xcheck.py` 返回 **PASS**。

---

## 1. Critical

### C-1 「test_sc22 函数体零改动」与「24/24 补参」在同一行上要求相反结果 ⇒ 该验收恒红

**locator**: `detailed-tasks.yaml:256-261` (TASK-005 验收 2) · `:838` (TASK-021 验收 3) ·
`:395` (TASK-010 验收 1) | `tasks.md:54` · `:76` · `:71`

实读 (`detailed-tasks.yaml:256-261`):
> 「**守卫未被放宽** (机械判据): 本 change 的 diff 中 test_sc22_no_real_git_subprocess_in_suite
> 函数体 (`:710-724`) **零改动** — `git diff -- tests/test_pre_merge_gate.py` 中该函数区间命中即红。」

实跑 (aria @ af87cae):

```
$ cd aria/skills/phase-c-integrator
$ grep -c 'gate_check(' tests/test_pre_merge_gate.py
24
$ grep -n 'gate_check(' tests/test_pre_merge_gate.py | awk -F: '$1>=705 && $1<=730'
708:                gate.gate_check(pr_branch="feat/x")
723:                out = gate.gate_check(pr_branch="feat/x")
$ grep -n 'gate_check(' tests/test_pre_merge_gate.py | grep -c 'main_branch'
0
$ awk 'NR==710||NR==723||NR==724' tests/test_pre_merge_gate.py
    def test_sc22_no_real_git_subprocess_in_suite(self) -> None:
                out = gate.gate_check(pr_branch="feat/x")
        self.assertEqual(out["verdict"], "green")
```

⇒ `:723` 既在那 **24 处**之内, 又在被要求「零改动」的 `:710-724` 函数体之内。
而 TASK-010 (`yaml:395`) 逐字「实测 24 处 gate_check( 调用点、显式传 main_branch 的 0 处 —
**补完后应为 24/24**」; TASK-005 的 `dependencies` 实测含 TASK-010, `tasks.md:53` 更逐字写
「接缝要在**已补完 24 处参数的调用形状**上验证红/绿才有意义」——**求值时该函数体必然已被改**。

**怎么会红**: 任何正确实现下 `git diff -- tests/test_pre_merge_gate.py` 在 `:710-724` 区间必有命中
⇒ TASK-005 验收 2 判红 (恒红); 反向若为满足它而独独跳过 `:723`, 则 TASK-010 的 24/24 判红,
且 D5 (`main_branch` 必填) 下 test_sc22 直接 TypeError。**两个独立实施者得相反结果**
(memory `spec-underdetermination`), 而这条正卡在 owner 指定的 TG-0 TDD 闸门上。

**归属**: `git diff 6818773..HEAD` 中该量以 `+` 出现 (本轮新写), 是用来替换上一版被 R2/code-reviewer
判「恒真」的那条验收 —— **把恒真换成了恒红**, 正是 memory `false_green_dual_is_permanent_red`
(「假绿的反面是恒红, 同样零信息量」) 与 `redfix-change-quantity` 的合体。
且同一个坏量被**复制进本轮唯一新增的 TASK-021** (`yaml:838`) ⇒ 一次修法造了两个恒红点。

**闭合建议 (仅供参考)**: 换成「函数体内除 `gate_check(` 调用行的参数补全外零改动」,
或钉「`_forbidden` 桩与 `mock.patch.object(pc_module.subprocess, "run", ...)` 两行逐字不变」——
那是「放宽守卫」真正会动的行, 而 TASK-010 的补参不会动它们。

---

## 2. Major

### M-1 TASK-014 第三版验收量「路径表达式逐字 == F」对 `:559` 结构上不可满足, 且求值时点早于 diff 定稿

**locator**: `detailed-tasks.yaml:512-528` (验收 1/2) | `tasks.md:92-93`

实读 (aria @ af87cae):
```
$ sed -n '262p;559p' aria/skills/phase-c-integrator/SKILL.md
**Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py` (stdlib + subprocess only)
**Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/submodule_gate.sh` (Bash, stdlib + git only)
```
两处**路径表达式的尾段指向不同文件** (`pre_merge_gate.py` vs `submodule_gate.sh`),
不可能同时「逐字 ==」同一个 F。而 F 的定义 (`yaml:515`) 是「TASK-002 回写 proposal §1 的定稿形态」,
`proposal.md:296` 的 SC-M12 验的又恰是 §1 那条 **`pre_merge_gate.py` 调用** ⇒ F 最自然的取值是
含 `pre_merge_gate.py` 尾段的具体串。

**怎么会红**: 实施者甲把 F 读成完整路径串 ⇒ `:559` 永远 ≠ F ⇒ **恒红**;
实施者乙把 F 读成「前缀机制模板 + 可变尾段」⇒ 全绿。同一条验收两个相反结果。
注意「逐字 ==」这三个字排除了乙的读法, 而甲的读法使验收不可满足 —— 两边都不成立。

**加重**: 验收 (2) 断言的是「**本 change 的 diff** 里新增或改动的每一处 helper 定位路径表达式」,
而实跑拓扑 (xcheck CHECK0 输出) 得 **TASK-014 在 L4**, 同改 `SKILL.md` 的 TASK-012/013/020 在 **L7**
⇒ 该断言在 TASK-014 完成那一刻**不可求值** —— 正是 R2/tech-lead 点名却未闭合的「求值时点」类。

**归属**: 本轮第三次换量 (`yaml:517` 逐字「2026-08-11 第三次换量」), R2-fix 引入。
Spec 自己写着「若第四次再出现, 请优先怀疑『拿 grep 计数当验收』这个手段本身」——
本次换的虽不是 grep 计数而是关系量, 但**同一处第四次不成立**这个事实本身已到判据线。

### M-2 TASK-001 里 SC-M3b 的 pattern 仍是未扩拒绝域的旧版 —— 而 TASK-001 正是交付那条断言的任务

**locator**: `detailed-tasks.yaml:111` vs `proposal.md:284` vs `detailed-tasks.yaml:426-429`

三处逐字实读:
- `yaml:111` (TASK-001, 红窗建造): ``grep -cE -- '--main-branch +(main|master)([[:space:]]|$)' SKILL.md``
- `proposal.md:284` (SC 表, canonical): ``grep -cE -- "--main-branch +['\"]?(main|master)['\"]?([[:space:]]|$)"``
- `yaml:426-429` (TASK-011): 「2026-08-11 pattern 扩了拒绝域 (加 `["']?`)」

拒绝能力实测 (合成 fixture 三行):
```
x --main-branch "master"
y --main-branch master
z --main-branch "<MAIN_BRANCH>"
$ grep -cE -- '--main-branch +(main|master)([[:space:]]|$)' fixture   → 1   ← 旧 pattern (TASK-001 用的)
$ grep -cE -- "--main-branch +['\"]?(main|master)['\"]?([[:space:]]|$)" fixture → 2   ← 新 pattern (SC 表)
两 pattern 对今日 SKILL.md 均 = 0 (与 Spec 自陈一致)
```
**怎么会红**: 实施者照 TASK-001 逐字建断言 ⇒ 落地一条 `--main-branch "master"` 示例时 SC-M3b 仍 0,
而 SC 表逐字声称「写死字面值 (**裸的与带引号的都算**) 的实现在此必红」——**声称再次强于拒绝域**,
即 R2/code-reviewer 抓的那条逃逸原样存活。一条「TASK-001 的 SC-M3b pattern 串 == SC 表的 pattern 串」
的机械检查今日红。

**归属**: R2-fix 只改了 SC 表与 TASK-011 两处散文, 漏了**唯一真正交付那条断言的任务**
⇒ 教科书式的「修实例不修类」(memory `fix-the-class`)。

### M-3 「已裁」段仍把已作废且恒红的 `{:610}` 写成「现行量」; 换量次数三处口径不一

**locator**: `tasks.md:148-149` (已裁 3) vs `tasks.md:91` / `tasks.md:99` / `detailed-tasks.yaml:547` / `:553`

逐字实读 `tasks.md:149`:
> 「🔴 **验收量换过两次, 两次作废理由都在 TASK-014 正文留痕**: … **现行量 = 旧形态命中集合恰为 `{:610}`**
> + **`:262`/`:559` 各恰 1 处新形态** + **封闭白名单负控**。」

而同文件 `tasks.md:99` (本轮新增) 逐字:
> 「🔴 **作废 (c) — 第三次换量**: R1-fix 轮的「旧形态命中集合恰为 `{:610}`」作废 … **改用与 F 的相等关系**」

`git diff 6818773..HEAD` 显示: 本轮**删掉**了 TASK-014 里的 `{:610}` 验收 (`-` 行) 并**新增**作废(c)
(`+` 行), 但 `:148-149` 这段摘要未同批改。另 `tasks.md:91` 与 `yaml:547` 仍写「验收量已被换过**两次**」,
而 `yaml:526`/`tasks.md:99` 写「**第三次**更换」, `tasks.md:148` 写「**第二次**换掉」——同一件事三个数。

**怎么会红**: 读「已裁」段的执行者按 `{:610}` 落地 ⇒ 恒红 (正是本轮判定要废掉的量);
读 TASK-014 正文的执行者按 `== F` 落地 ⇒ 两个独立执行者对同一输入得相反结果。
**这与 R2/code-reviewer#1 (metadata.ship_target 陈旧摘要 vs TASK-020 正文) 是同一形状** ——
那条被修了, 这个兄弟位置没修。**归属**: 矛盾由本轮制造 (R2 基线上「换过两次」是准确的)。

### M-4 R2「求值时点」那一类未补规则, 在 TASK-008/009 这对上仍在: SC-M6 的 raw_message 半边由下游交付

**locator**: `detailed-tasks.yaml:330` (TASK-008) · `:375` (TASK-009) · `proposal.md:290` (SC-M6 定义)

- `proposal.md:290` SC-M6 逐字期望: 「`verdict=fail` + `kind=="main-branch-not-found"` + **`raw_message`** 含分支名与 remote 名」
- `yaml:330` (TASK-008 验收 1): 「SC-M6 / SC-M13 / SC-M7 / SC-M8 / SC-M14 **全绿**」
- `yaml:365` TASK-009 title: 「诊断信息写入 raw_message (主通道)」, 其 `dependencies` 实测 = `[TASK-008]`
  ⇒ 拓扑 TASK-008 = L5, TASK-009 = L6 (xcheck CHECK0 实跑输出)

**怎么会红**: TASK-008 完成点跑 SC-M6 时 raw_message 尚无诊断内容 ⇒ 红; 若 TASK-008 为转绿自行写入,
则 TASK-009 退化为 no-op。R2/tech-lead 的处方逐字是「**统一补一条规则**」(∀task: 其 verification 引用的
每个 SC, 被测代码与测试文件须 ⊆ 本任务 ∪ 传递依赖的 deliverables), 本轮**只修了 004/006/007 三个实例**,
metadata 里只补了 `line_anchor_convention` 一条全局约定, **没有求值时点的对应约定** ⇒ 类未修。
**归属**: 残余 (非本轮引入)。

### M-5 TDD 红窗只覆盖 19 行 SC 中的 9 行, 而 TASK-001 的 title 逐字自称「全部机械断言」

**locator**: `detailed-tasks.yaml:99` (title) vs `:107-126` (清单) vs `proposal.md` SC 表

- title 逐字: 「TDD 前置 — **全部机械断言**的空壳, 先看到全红」
- 清单实测覆盖: SC-M1 / M2 / M3a / M3b / M3c / M4 / M5 / **M9** / **M17** = **9 条**
- SC 表定义 (xcheck CHECK2 实跑输出): 「SC 表定义 **19** 条」(按行计; 按编号计 17, proposal:410 已标计数法 ✅)
- 缺红窗且**今日即会红**的: SC-M6 / M7 / M8 / M13 / **M14** —— 全部由 TASK-008 (实现任务) 同批交付
  代码与测试 ⇒ test-after

**怎么会红**: 一条「TASK-001 的红窗清单 ⊇ 今日已红的 SC 集合」的机械检查今日红 (缺 5 条)。
**归属**: 残余 (R2/code-reviewer#5 未闭合), 但本轮新增的 SC-M14 又落进同一缺口。
(SC-M15/M16 今日为空真且期望值已满足, 结构上无法先红, **不计入本条**。)

---

## 3. minor

### m-1 TASK-015 的 blob SHA 断言命令在主仓不可执行 (aria 是 gitlink)

`detailed-tasks.yaml:580-582` 逐字: 「ab-results 里记录本次 run 所对应的
`git rev-parse HEAD:aria/skills/phase-c-integrator/SKILL.md`」。实跑:
```
$ git rev-parse HEAD:aria/skills/phase-c-integrator/SKILL.md
fatal: path 'aria/skills/phase-c-integrator/SKILL.md' exists on disk, but not in 'HEAD'
exit=128
$ git -C aria rev-parse HEAD:skills/phase-c-integrator/SKILL.md
4c1fd90f60faab1821a876a8ffbcbd806fc23a08     ← 正确形式
```
**怎么会红**: 照抄即 128 报错。归属 R2-fix (`+` 行)。定 minor 因为它**响亮地失败**而非静默假绿,
但它是 R2/tech-lead「AB 跑的 SHA ≠ ship 的 SHA」那条 blocking Major 的唯一闭合腿, 值得一并改。

### m-2 est_hours 粒度: 13/21 条 < 4h, 本轮新增的 TASK-021 又是 2h

实跑 (总体 = yaml 21 条 task / 计数法 = `est_hours` 字段 < 4):
`13/21`, total 65h。`CLAUDE.md:35` 逐字「小步迭代 (任务 4-8h 粒度)」。R2/tech-lead 的同条 minor 未闭合,
且本轮唯一新增任务又是一条 2h。归属: 大部分残余。

### m-3 CHECK 通过的 metadata `head` 已比主仓 HEAD 落后 2 commit

`yaml:46` `head: 98ad1f5`, 实测主仓 HEAD = `0dd26ce`。我逐条复跑了主仓侧的全部行锚
(`.aria/config.template.json:75/:78` · `README.md:8` badge) —— **今日仍全部命中**, 故仅 minor。
`aria` 侧 `head: af87cae` 与 `git -C aria rev-parse --short HEAD` 实测**一致** ✅。

---

## 4. 那道机械交叉检查真的有效吗 (本轮被要求重点回答)

**基础事实**: 当前三件套上 `python3 xcheck.py openspec/changes/premerge-gate-mainbranch-failclosed`
→ `RESULT: PASS — 四项交叉检查全部通过` (EXIT=0)。而我在同一份文件上找到 1C+5M+3m。
**它对本席位这 9 条的检出率 = 0/9。** 下面是逐项的可复跑证据。

### 4.1 CHECK1 是**无向**的 ⇒ 检不出它被写来检的那条方向错误

规则实现 (`xcheck.py:93`): `ok = n in ANC[tid] or tid in ANC[n]` —— 只要**任一方向**存在传递依赖即 ✓。
而 R2 那条 Major 的病是**方向错**, 不是「无序」。

**对抗实验 (可复跑)**: 拷一份当前 yaml, 把 R2 那条 Major 原样恢复 ——
`TASK-008.dependencies -= TASK-010` / `TASK-005.dependencies -= TASK-010` / `TASK-010.dependencies += TASK-008`
(即 TASK-008 的「重跑全量」重新排到 TASK-010 补参之前, 24 条 TypeError 重现):

```
$ python3 xcheck.py <adv2>
  TASK-008  -> TASK-010   ✓ (它依赖本任务)
  TASK-010  -> TASK-008   ✓ (本任务依赖它)
RESULT: PASS — 四项交叉检查全部通过
```

⇒ **被这道检查「当场抓到」的那条缺陷, 把它原样放回去, 检查返回 PASS。**
第二个实验 (反转 TASK-015 ↔ TASK-021 的方向, 使 AB 的收口边失效) 同样 PASS。
形状 = memory `invariant-dimension`:「无向检查 (存在/覆盖/连通) 对**方向性**错误天然免疫」。

### 4.2 CHECK3 检的是**有没有写那句护栏**, 不是**验收量是否随实施位移**

规则实现 (`xcheck.py:143-144`): 在 verification+notes 里找 `内容锚 / 按锚重定位 / 不得按行号核 /
行号必然位移 / 以 af87cae 为准` 五个**关键词**之一。

**对抗实验**: 直接拿 R2 基线 (`6818773`) 跑 —— 那一版 TASK-014 的验收第 1 条逐字就是
「命中集合**恰为 {:610}**」(两个席位独立判它为 Major/恒红), 同时它也写了「⚠️ 行号必然位移 … 不得按行号核」:

```
$ python3 xcheck.py <r2base> | grep 'CHECK3'
  … 12 条 "无位移护栏" 失败 …
  (TASK-014 不在其中)
```
⇒ **全 Spec 最严重的那个「量随位移」实例, CHECK3 判它通过。**
形状 = memory `selfcheck-values-not-questions`:「机械自检抓错值抓不了错问题」。
本轮的 C-1 也验证了同一点: TASK-005 既写了护栏句 (`yaml:263`) 又写下一条恒红的量, CHECK3 ✓。

### 4.3 CHECK4 有一半**结构上不含断言**, 另一半是本轮自己那些句子的字面复读

- `xcheck.py:163-169` 那个 `INSERT` 循环**只有 print, 没有一次 `fails.append`**
  ⇒ 「插入点是否被多条条款同时管辖」这半**恒绿**, 判据是「该信号在健康常态下应是什么值」——
  它在任何输入下都是同一个值 (打印计数), 零信息量 (memory `false_green_dual_is_permanent_red`)。
- 剩下的 9 条断言全是 `pat in prop_txt` 形式的**硬编码字面串** (「在 `enabled` 早退之后」
  「两节不得互相援引」「含任一 legacy key 的 config」…), 逐字取自 R2-fix 本轮写下的句子。
  ⇒ 它验的是「你有没有把这几句话写进去」, 从今往后**永久为绿**, 对**下一个**插入点冲突完全失明。
  这道检查本身就是「只修实例不修类」的产物 —— 它编码的是本轮撞到的那一个插入点冲突, 不是那个类。

### 4.4 CHECK2 的 `any` 语义放过「本任务认领 SC 却不交付测试」

`xcheck.py:126`: `ok = any(r.endswith("✓") for r in rows)` —— 只要**任一** owner 交付测试文件即通过。
于是它自己的输出里就明晃晃写着 `SC-M6 owners=TASK-003✗,TASK-005✓,TASK-008✓,TASK-009✗ ✓` ——
**TASK-009 认领 SC-M6 却零测试交付**这件事 (本报告 M-4) 被 `any` 吸收掉了。
另: `TESTISH` 里的 `"ab-results"` 与 `"收口实跑输出"` 两个 token 恰是本轮新增/改动任务
(TASK-015 / TASK-021) 的**散文型 deliverable** 字面 —— 判据被放宽到能容纳本轮的 fix 本身。
公平起见我实测了敏感性: 去掉这两个 token **今日不改变任何一条 SC 的判定** (无 SC 失去 owner),
故这条只是**判据被削弱**, 不构成当前的掩盖, 不单列 finding。

### 4.5 覆盖面: R2 的两个形状里, 它只覆盖了各自最外层的一圈

| R2 诊断的形状 | 检查覆盖的 | 检查漏掉的 (本轮实证) |
|---|---|---|
| 只修实例不修类 | 「用了行号锚却没写护栏句」 | 量本身仍是行号 (C-1 / R2 基线 TASK-014) · 同一 pattern 在另一任务没同步 (M-2) · 陈旧摘要 (M-3) |
| 移交给没核过的下游 | 「点名了 TASK-xxx 却完全无序」 | **方向反了** (§4.1) · 移交对象交付面不含所需产物 (M-4) |

⇒ 结论: **这道检查抓的是 R2 findings 的「症状表面」而非其判据。**
它在 R2-fix 当场报出的 FAIL(6)/FAIL(10) 是真的 (那些确实是缺失), 但那是一次性的补齐,
之后它对同类新缺陷的拒绝能力经三个实验实测为零。**它现在是一道恒绿闸门。**

---

## 5. R2 的 1C + ~13M 逐条回源

| R2 finding | 状态 | 回源证据 (逐字/实跑) |
|---|---|---|
| **C (2 席): TASK-020 fail-CLOSED 无插入点/信号通道** | ✅ **真闭合** | `proposal.md §6.1` (:205-231) 新建; 实读 `pre_merge_gate.py:325/:328/:337/:338-339` 与 §6.1 的框图逐行一致 (`:325 user_normalized=_normalize_config(...)` / `:328 if not cfg["enabled"]` / `:337 backend=resolve_ci_backend(cfg)` / `:339 return _no_ci_output(cfg["no_ci_fallback"])`); 「两个别名键的首个消费者分别在 :337 与 :339」经读 `resolve_ci_backend` docstring (`:124-136`, 逐字 `config["ci_backends"]`) 确认成立; 三条唯一确定用例 + CLI 真实路径断言 (:771-778) 均在位 |
| tech-lead#2 TASK-010→008 无依赖序 | ✅ | `TASK-008.dependencies` 实测含 TASK-010 |
| tech-lead#3 config-loader 无 Rule#6 / TASK-015 排序 | ✅ | `proposal §Rule #6` 三件套齐 (点名行为 + SC-M17 + TASK-019(8)); `TASK-015.dependencies` 含 TASK-019/TASK-021; SC-M17 实跑 `grep -cE …  config-loader/SKILL.md` = **2** (:249/:257 逐字命中) |
| tech-lead#4 发版同步面 8 文件 | ✅ | TASK-017 deliverables 列全 8 件; `scope_repos` 两侧均补; 实测 `README.md:8` = `Plugin-v1.65.5-blue`, `plugin.json` = `1.65.5`, `state-checks.yaml:88` m6-version-badge-match 在位 |
| tech-lead#5 SC-M12 只挂 spike | ✅ | TASK-011 认领 SC-M12 且 deliverables 补入 test 文件 |
| tech-lead#6 / cr#2 TASK-014 `{:610}` | ⚠️ **换了量但新量不成立** | 见 **M-1**; 且旧量仍活在 `tasks.md:149` (**M-3**) |
| tech-lead#7 SKILL.md:242 被折叠 | ✅ | SC-M16 新增 (proposal:300); 实读 `:242` 确为步骤 2.5 且是全文件唯一「本项目 `master`」出处 |
| tech-lead#8 求值时点「补一条规则」 | ❌ **只修实例未补规则** | 见 **M-4** |
| tech-lead#9 yaml 围栏 spike 在 notes | ⚠️ 部分 | `yaml:453` 补了可求值收口 + 显式声明「未提升为独立任务, 请 handoff 复议」—— 留痕合规 |
| tech-lead#10 §3 确定式/条件式 | ✅ | `proposal.md:116-118` 已改条件式 |
| tech-lead#11 TASK-020 行号护栏 + 依赖边 | ✅ | `yaml:749-752` 护栏在位; deps 含 011 |
| tech-lead#12 est_hours | ❌ | 见 **m-2** (13/21) |
| qa#1 D9 两条兄弟早退缺因果断言 | ✅ | `yaml:339-344` + `proposal:345` 均补「各带同款 `assert ls-remote 未被调用`」 |
| qa#2 UnicodeDecodeError 无编号 | ✅ | SC-M14 建号 (proposal:298) |
| ba#1 (C 的另一角度) 信号传播 | ✅ | `yaml:771-778` + `proposal:229` 要求走 `main()`/CLI 真实路径, 逐字排除 `_normalize_config` 上的 assertRaises |
| ba#2 SC-M12 无持久化测试 | ✅ | 同 tech-lead#5 |
| ba#3 TASK-002 缺先例引用 | ✅ | `yaml:153-161` 补入 `submodule-gate-telemetry.sh:60-62`, 且正确区分「可移植的是结构不是 BASH_SOURCE」 |
| km#1 project.md 矛盾未入 TASK-019 | ✅ | 成为第 (7) 项 (`yaml:705-709`), `tasks.md:141` 同步改口 |
| km#2 `main_branch_resolved` | ✅ | 全 change 目录只剩 1 处命中, 就是记载其删除的那句留痕 |
| cr#1 metadata「不再是条件触发」 | ✅ | `yaml:75-80` 让 metadata 一侧改口 |
| cr#3 §2 委派 SC-M2 是误派 | ✅ | SC-M15 新增 (proposal:299) 且 `proposal:109` 改口 |
| cr#4 无终局收口 | ✅ | TASK-021 新建, 依赖 008/009/010/011/012/013/014/020, 拓扑 L8; 实跑确认无任何改被测文件的任务排在它之后 |
| cr#5 SC-M9/M12 无测试交付 + 无红窗 | ⚠️ 部分 | SC-M9 红窗移入 TASK-001 ✅ / TASK-006 deliverables 补测试文件 ✅; 但「先看到红」整体仍是 9/19 (**M-5**) |
| cr#6 ab-results 不在 scope | ✅ | `scope_repos[Aria].paths` 已含 |
| cr#7 TASK-005 恒真验收 | ❌ **换成了恒红** | 见 **C-1** |
| cr#8「非零非 2」凿洞 | ✅ | 现 `yaml:217` 已改为 catch-all + SC-M14 编号, 「非零非 2」措辞已消失 |
| cr#9 `:557` 误归 | ✅ | 已从 TASK-019(6) 枚举移除, 留白名单并逐字更正 (`yaml:538-542`); 实读 `:557` 确为 tripwire host-cron 记述 |
| cr#10 SC-M3b 拒绝域 | ⚠️ **只修了 2/3 处** | SC 表与 TASK-011 已扩, **TASK-001 未扩** (**M-2**) |
| cr#11 TASK-012/013 行号锚 | ✅ | 两条均补内容锚 + 位移护栏 |

**净**: 1 Critical 真闭合 (且闭得扎实——§6.1 的每一行锚我都回源实读过);
~13 Major 中 **约 9 条真闭合 · 3 条换了量但新量不成立或只修一半 · 1 条类未修**。

---

## 6. 该记的优点 (不是客套, 是本轮少数可复现为真的东西)

1. **§6.1 是本轮最扎实的产出**: 五个行锚 (`:325/:328/:337/:338/:339`) 我逐行 `awk` 实读, 全部命中;
   两侧理由 (为何在 enabled 之后 / 为何在 resolve_ci_backend 之前) 各自成立且互不援引;
   三条用例确实把插入点**唯一确定**。这条 Critical 的闭合质量高于本 Spec 历史平均。
2. **计数法纪律真的守住了**。我复跑了 proposal §1 那 8 个数, **全部逐字复现**:
   ```
   总体=aria 子模块 · 范围=git-tracked · 计数法=行数:      CLAUDE_ 65 / ARIA_ 5
   计数法=occurrence (git grep -o):                        CLAUDE_ 66 / ARIA_ 7
   单文件 SKILL.md 行数: ARIA_ 3 / CLAUDE_ 1 · occurrence: 4 / 1
   ```
   TASK-020 的五对删除面计数同样全部复现 (`pre_merge_gate.py 6/2` · `phase-c-integrator/SKILL.md 6/4` ·
   `config-loader/SKILL.md 2/2` · `test_pre_merge_gate.py 17/3` · `config.template.json 2/0`),
   且中英并列口径确实必要 (`SKILL.md:49` 逐字含中文「v2.0 移除」)。
   proposal:410「按编号计 17 / 按 SC 表行计 19」也标了计数法且与 xcheck 实测的 19 一致。
3. **空真被诚实标注**: SC-M3c / SC-M15 / SC-M16 三处都写明「今日的 0(1) 不是正面证据」,
   这是本项目历史上反复踩的坑, 本版处理正确。
4. 测试基线复跑 `111 passed in 1.17s` ✅; `git -C aria rev-parse --short HEAD` = `af87cae` 与
   `scope_repos[aria].head` 一致 ✅。

---

## 7. 阻塞项 (blocks_phase_b)

- **C-1** TASK-005 / TASK-021 的恒红验收 (卡 TG-0 出口与终局收口)
- **M-1** TASK-014 验收量对 `:559` 不可满足 + 求值时点早于 diff 定稿
- **M-2** TASK-001 的 SC-M3b pattern 与 SC 表不一致 (红窗建的是弱断言)
- **M-3** 「已裁」段把恒红的 `{:610}` 写作现行量

M-4 / M-5 / m-1..m-3 不单独阻塞, 但 M-4 是 R2 明确要求「补规则」而未补的那一条, 建议一并处置。

## 8. 给编排层的一句话

本轮的数据是: **fix 引入占比 55.6% (5/9), 略高于 R1→R2 的 53%**; Critical 1→1 (换了位置);
Major ~13→5 (**在降**)。按 memory `stop-adding-rounds`「加轮判据是 major 数是否还在降」, 数据首次转正向;
但按 `marginal-return-negative`「本轮 fix 引入的 major 占比 > 1/2 即到拐点」, 仍在拐点之上。
**真正的新信息是 §4**: 上一轮寄予厚望的那道机械检查, 经三个对抗实验实测**拒绝能力为零** ——
它不该被当作下一轮的闸门, 除非按 §4 逐项换量 (CHECK1 加方向、CHECK3 判量本身而非关键词、
CHECK4 的前半补上真断言、CHECK2 改成 per-owner 而非 any)。
