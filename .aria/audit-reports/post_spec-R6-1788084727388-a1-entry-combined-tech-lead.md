---
checkpoint: post_spec
round: 6
role: tech-lead
verdict: REVISE
scope_ok: true
counts: 6C/9M/7m
---

# post_spec R6 — a1-entry 三份 Spec 联审 · `tech-lead` 席 (镜头: 实现者试派生 / A.2 dry-run)

> **审计对象**: 主仓工作树 (2026-08-30 rework v4 落版后) 的三份 proposal。
> **代码基线**: aria 子模块 `d50f9c3`。全部代码引文经 `git -C aria show d50f9c3:<path> | sed -n 'Np'` 实读, 未用 grep 拼接。
> **仓状态核验**: 工作树在 `fix/phase1-gate-no-push` @ `007d355`, 与 `d50f9c3` 的差异只在 `phase1_gate.py` / `release_gate.py` / `lib/failure_handlers.py` / `tests/test_coordination_no_push.py` 四文件 — 本席全部引文避开这四个文件的改动区, 或显式标注。
> **只读**: 本席未修改任何仓内文件, 未 `git add/commit/push`。唯一写入 = 本报告。

## (a) 本席镜头

我假装自己是接下来写 `tasks.md` 的那个人, **只**读三份 Spec 的 Success Criteria 表 + Impact 表 + 决策记录 (A.2 的三个派生输入), 逐条问「这条能不能落成一个任务、两个独立实现者会不会写出同一个东西、验收怎么会红」——报告的是**派生不出来 / 派生出两个相反结果 / 派生出的东西与另一条派生结果互斥**的地方。

---

## (b) Findings

### Critical

---

#### 母 C1 — SC-22 第 5 条与它自己的块边界规则互斥; 唯一自洽的落法违反 §2

**位置**: 母 Spec `:605` (SC-22 行)。

块边界规则逐字 (`sed -n '605p'` 截取):

> **块边界 (D17 ①, R5/M5)**: 「步骤块」= 从匹配 ① 的标题行起, 至下一个 `^#{1,4}[ \t]` 行 (或文件尾) 止的切片; ②–⑥ **只在该切片内求值**。

第 5 条逐字 (同行, 原文用带圈数字标为第 5 项):

> ⑤ **仅 `phase-a-planner`**: 其 ```yaml 围栏内 `A.1 - Spec 管理:` 项下含逐字 `precondition: 见「前置: REQUIRE claim」小节 (MUST, 在本表之前执行)` (R5/M3: 按 YAML 表执行的 AI 否则没有任何指针指向围栏外的前置标题)

第 5 条自己的理据就写着断言对象在「**围栏外的前置标题**」之外的另一处 —— 即 YAML 与前置块是两个分离区域。但块边界规则说第 2 到第 6 条**只在切片内求值**。两句话对同一条断言给出两个求值域。

**实读现状** (`git -C aria show d50f9c3:skills/phase-a-planner/SKILL.md | grep -n '^#\{1,4\}[ \t]'`): `### 步骤执行` 在 `:60`, ```` ```yaml ```` 在 `:62`, `A.1 - Spec 管理:` 在 `:63`, 下一个标题 `### 输出` 在 `:101`。

⇒ 两个实现者会得到相反结果:

1. **实现者甲**照块边界规则办 —— 把 `### 前置: REQUIRE claim (A.1, MUST)` 放在 `### 步骤执行` **之前**。切片在 `### 步骤执行` 处终止, YAML 在切片外 ⇒ **第 5 条恒不可满足**, 除非违反「只在切片内求值」。
2. **实现者乙**为了让第 5 条落在切片内, 把前置标题插在 `:61` (`### 步骤执行` 与 ```` ```yaml ```` 之间)。此时切片 = `[:61, :101)`, **整个 A.1/A.2/A.3 YAML 被吞进「前置」小节**。这直接违反 §2 `:125` 逐字要求:

> **触发时机**: A.1 **起草前**, 作为**独立标题级步骤** (…), **不塞进现有 A.1 的 YAML 动作列表**

而且乙的落法下, SC-22 第 4 条「切片内**不得**出现字面 `--phase B`」的作用域从「前置块」扩到了「整张步骤表」—— 一条本意做负控的断言变成了对无关内容的约束 (本仓实测 `phase-a-planner/SKILL.md` 该字面 0 命中, 所以今天不会红, 但这是运气不是设计)。

**为什么是 Critical**: 条款互斥, 且两条落法都能自圆其说 —— 这正是 memory `spec-underdetermination` 的「两独立实现者同规格得相反结果」判据。母 Spec「新表面 #4」(`:743`) 问的是 (逐字, 原文用带圈数字指第 5 条)「切片内出现 ```yaml 围栏时 ⑤ 与「不在围栏内」的关系」—— 问对了地方但问错了那一半: 冲突不在第 5 条 vs 第 1 条的围栏条件, 在第 5 条 vs 「第 2 到第 6 条只在切片内求值」。

**建议处置 (只建议不落版)**: 把第 5 条从「第 2 到第 6 条」里摘出来, 显式声明它是**切片外的独立断言** (断言对象 = `phase-a-planner/SKILL.md` 的 ```` ```yaml ```` 围栏, 与步骤块切片不重叠), 并在块边界规则句里把「第 2 到第 6 条只在切片内求值」改成「**第 2、3、4、6 条**只在该切片内求值; **第 5 条**的断言对象是 ```` ```yaml ```` 围栏内的 YAML, 在切片外独立求值」。

---

#### 母 C2 — SC-22 第 2 条没有把 D17 第 2 要件落下来: 六个独立子串, 一段散文即全绿

**位置**: 母 Spec `:605` (SC-22 第 2 项) 与 `:500` (D17)。

D17 逐字 (`sed -n '500p'`):

> **SKILL.md 指令块的机械断言三要件**: ① 块边界逐字定义 (…); ② 块内须含**至少一条可直接执行的完整命令行** (脚本路径 + 必需参数), 不得只有概念名 / 名词短语; ③ 块内须含 fail 分支的**消费措辞字面** (如 `未能核实`)。

SC-22 第 2 条逐字:

> ② 切片内含**六个字面量**: `phase1_gate.py` / `--linked-issue` / `--include-terminal` / `--phase A.1` / `--raw-track-id "<spec-slug>-<container_uuid>"` / `未能核实`

这是**六次独立子串检查**, 没有任何邻接 / 同行 / 「一条命令行」的要求。SC-22 的「怎么会红」列只处理了**位置**错误 (「把字面量塞进 `## 相关文档` 的实现因**块边界**在切片外 ⇒ 必红」), 没有处理**形态**错误。

**能通过 SC-22 全部六项、但没有任何可执行命令的实现** (我作为实现者三分钟就能写出来):

```
### 前置: REQUIRE claim (A.1, MUST)
本步骤调用 phase1_gate.py。需要的参数: --linked-issue (哨兵时省略) / --include-terminal /
--phase A.1 / --raw-track-id "<spec-slug>-<container_uuid>"。
check: coordination ref 内按 (container_id, session_id) 定位到本 session 的 active claim
      (读 claims/ 下本 session 的文件)
失败或降级时按「未能核实」渲染, 不得写「无碰撞」。
改名 ⇒ release 旧 + acquire 新; 放弃方向 ⇒ release_gate.py --raw-track-id …
```

这段东西第 1 到第 6 条全绿, 而运行时 AI **没有一条可以直接跑的命令**。这与 R5 判 Critical 的探针 C1 (「唯一被机械钉住的指令是一个 9 字名词短语」) 是**同一形状**; D17 就是为消掉这个形状而立的类级处方, 而它在自己的发源地——母 Spec——没有落点。对比探针 SC-20 (`:501`) 把它落对了:

> 切片内含四个字面量 … **且**含一条以 `python3` 起首、含 `sibling_spec_probe.py` 与 `--own-spec-dir` 的完整命令行 (D17 ②)

**为什么是 Critical**: 造出一条可被廉价欺骗的主防线断言 —— 母 Spec「新表面 #4」自己问的「是否仍存在『插几行字面即绿』的实现」, 答案是**是**。memory `fix-the-class`: 类级修复没有推广到发起它的那个实例。

**建议处置**: SC-22 第 2 条追加一句「**且**切片内含一条以 `python3` 起首、含 `phase1_gate.py` 与 `--raw-track-id` 的完整命令 (允许 `\` 续行 —— §2 的模板是六行续行形, 断言须先做续行折叠再判)」。注意这里与探针不同: 母 Spec §2 的模板是**多物理行 + 反斜杠续行**, 单行正则会直接判红, 必须先折叠。

---

#### 母 C3 — SC-32 要求放开 `--raw-track-id` 的 argparse `required`, 而同一份 Spec 的 Impact 表逐字写「零改动」

**位置**: 母 Spec `:615` (SC-32) 对 `:655` (Impact `phase1_gate.py` 行) 与 `:627` (非目标)。

SC-32 场景列逐字:

> 编排层两级来源 (§2.2 ①②) 都取不到 ⇒ **仍**调用 `phase1_gate.py --heartbeat-only --phase A.1 --repo-path <repo>` 且**不传** `--raw-track-id` (该模式下 argparse 不得要求它)

Impact `:655` 逐字:

> **A.1 模板调用的完整 flag 集 = `--raw-track-id` / `--phase A.1` / `--mode advisory` / `--linked-issue` (哨兵时省略) / `--include-terminal` / `--repo-path`** (前四个与 `--repo-path` 为既有参数, **零改动**; 本行只改下列五处)

**实读代码** (`git -C aria show d50f9c3:skills/state-scanner/scripts/phase1_gate.py | sed -n '1185,1191p'`):

```python
    parser.add_argument(
        "--raw-track-id",
        required=True,
        help="用户选定的 carry-id 原始串 (未归一; run_gate 内部 derive_track_id 归一)",
    )
    parser.add_argument(
        "--phase", required=True, help="当前十步循环 phase (如 B / B.1), 写入 claim"
    )
```

⇒ `--raw-track-id` 今天是 `required=True`。SC-32 要红就必须改它, Impact 表说它零改动。**两条派生输入 (SC 表 / Impact 表) 对同一个文件给出相反的任务。**

三重加码:

1. **与本 Spec 对 `--phase` 的处置自相矛盾且无理由**。§2.2 `:233` 逐字: 「本 Spec 取「文档补 `--phase`」而**不**放开该参数: 零代码改动」。同一个 argparse、同一类问题 (heartbeat 模式不需要某个 required 参数), 一个选「不放开」, 一个选「必须放开」, 全文没有一句解释这个不对称。
2. **触 §非目标**。`:627` 逐字: 「**不动** Phase B 入口现有认领 …… **`--heartbeat-only` 是同一 CLI 下的独立模式, 不改 acquire 路径**」。把 `--raw-track-id` 的 `required` 摘掉是**解析层**的改动, 对 `--phase B` 的 acquire 调用同样生效 —— Phase B 少传 track-id 时的 parse-time fail-fast 会消失, 除非另加一个模式条件判断。这不是「不改 acquire 路径」。
3. **落法欠定**。至少三种互不等价的写法: (a) `required=False` + 解析后按 `args.heartbeat_only` 做条件校验; (b) argparse subparsers; (c) 拆成独立脚本 `scripts/heartbeat_gate.py` —— 而 Impact `:656` 对 (c) 只写「若 A.2 落地时改为独立脚本 `scripts/heartbeat_gate.py` 亦属同一变更面」, 把选择丢给 A.2 而没给判据。

**为什么是 Critical**: 条款互斥 + 欠定 + 撞非目标。照 Impact 实现则 SC-32 结构性无法为真 (CLI 在 argparse 层就退出, 到不了 heartbeat 分支, 遥测那一条记录永远写不出来 —— 与 R3/BA-M1 抓到的 `--phase` 那次是同一个坑, 换了个参数原样复发)。

**建议处置**: 二选一并写进 Impact —— 要么把 `--raw-track-id` 的条件化明确登记为 `phase1_gate.py` 的第七处改动 (并写清「非 `--heartbeat-only` 模式下缺参仍须非零退出」这条负控, 否则 acquire 路径的 fail-fast 静默消失), 要么把 SC-32 的场景改成「传一个约定的空哨兵值」从而真的零改动。

---

#### 跨 Spec C4 — 母 SC-12 与字段 E6 的四格表对同一输入给出相反的验收

**位置**: 母 Spec `:578` (SC-12) 对 字段 Spec `:211-218` (E6 verdict 表)。

母 SC-12 逐字:

> | **SC-12** (行为) | spec 有「关联 Issue」但未传 `--linked-issue` | AI 不得跳过该参数 | 定向 fixture …

字段 E6 表逐字 (`sed -n '211,218p'`):

> | verdict | `--linked-issue` |
> |---|---|
> | `OK` 且 token 串为哨兵 (`none` / `无`, §2 集合) | **整个参数省略** (原 NEW-01 条款) |
> | `OK` 且为真 token | 传第一个 token 元素逐字节 |
> | **`BAD_TOKEN`** | **整个参数省略** + 消费面按「字段不合规, 本轮无 issue 输入」呈现 —— **不得**把脏串喂进匹配面 |
> | **`NO_TOKEN` / `NO_FIELD`** | **整个参数省略** (本就无 token 可传) |
>
> **一句话判据**: **只有 `OK` 且非哨兵的那一格产生 `--linked-issue` 实参**, 其余三格一律省略。

「spec **有**「关联 Issue」但值判 `NO_TOKEN` 或 `BAD_TOKEN`」这一类, 字段 Spec 说**必须省略**, 母 SC-12 说**不得跳过, 跳过判红**。

**这不是理论上的边角**: 字段 Spec `:92` 实测「结果 = 14/14 返回 `None`」, 存量真字段**全部**是 markdown 链接形 ⇒ 全判 `NO_TOKEN`。字段 Spec `:289` 逐字: 「**⛔ 本规则**故意**不接受 markdown 链接形 —— 存量 14 条全判 `NO_TOKEN` 是预期, 不是缺陷。**」所以这是主路径不是边路。

**根因是母 Spec 只吸收了 E6 的一半**。本席实测: `grep -c` 母 Spec 全文, `BAD_TOKEN` = **0**, `NO_TOKEN` = **0**, `NO_FIELD` = **0**, `E0` = **0**, `E6` = **0**。母 Spec 里对省略实参的规定只有两处, 都只覆盖哨兵与字段缺席:

- `:111`: 「token 为「无关联」哨兵时 (canonical `none`, alias `无` …): 整个 `--linked-issue` 参数必须省略」
- `:527` rule6_note 点名行为 (a): 「传 `--linked-issue` (token 为哨兵 `none`/`无` 时**省略**该实参)」
- `:655` Impact: 「`--linked-issue` (哨兵时省略)」
- `:458` §6 缺口表首行: 「token 为哨兵 (`none` / `无`) **或字段缺席**」

四处口径一致地漏掉 `BAD_TOKEN` / `NO_TOKEN`。

**为什么是 Critical**: 两份 Spec 的 A.2 会分别派生出两个 AB fixture, 对同一份输入 (存量任意一份 markdown 链接形 proposal) 给出相反的期望臂 —— 实现者无论怎么写都必红一条。而且照母 Spec 单侧实现的结果, 正是把整个 markdown 链接串喂进 `--linked-issue`, 即字段 Spec `:98` 逐字点名的「姊妹 Spec `linked-issue-normalization` 刚治好的格式病在上一层原样复现」。

**建议处置**: 母 Spec 三处 (§2 `:111` blockquote、rule6_note (a) `:527`、Impact `:655`) 的省略条件统一改为引用字段 E6 的一句话判据「只有 `OK` 且非哨兵那一格产生实参」, 并把 SC-12 的场景列限定到「字段值判 `OK` 且非哨兵 但 AI 未传」。

---

#### 跨 Spec C5 — `--emit-arg` 切换在两份 Spec 的 Impact 表里都没有归属; 母 Spec 全文零提及

**位置**: 字段 Spec `:219` 单方面声明, 母 Spec 全文 0 命中。

字段 Spec `:219` 逐字:

> **E6 的机械宿主 (2026-08-30 落版, 母 Spec D17 ②「至少一条可执行命令行」)**: 探针增一个模式 `linked_issue_field_probe.py --emit-arg <proposal.md 路径>` …… **母 Spec 的 A.1 模板在本 Spec ship 后从该 stdout 取实参, 空 ⇒ 省略 `--linked-issue`**; ship 前 AI 按 E6 手工取。

本席实测: `grep -c 'emit-arg'` 母 Spec = **0**; `grep -c 'linked_issue_field_probe'` 母 Spec = **0**。

而两份 Impact 表:

- **母 Spec** `:658` / `:660` 的 `phase-a-planner/SKILL.md` / `spec-drafter/SKILL.md` 行, 描述的是前置块的内容 (锚点 / 六个字面量 / 消费 / release 义务 / skip / unattended), **没有一个字**提到实参来源或后续切换;
- **字段 Spec** Impact 表 (`:568-579`) 里根本没有 `phase-a-planner/SKILL.md` 这一行; 唯一碰 `spec-drafter/SKILL.md` 的行 (`:571`) 只声明 hunk A/hunk B, 并逐字划界「frontmatter `:10` 的 `allowed-tools` hunk **归母 Spec, 本 Spec 一字节不碰**」。字段 Spec 的非目标 `:551` 更逐字写「**不做** A.1 入口认领 / track-id 契约 / heartbeat —— 母 Spec 范围」。

⇒ **「字段 Spec ship 后去改母 Spec 那两个 SKILL.md 块」这件事, 没有任何一份 Spec 的 Impact 表认领它**, 也没有 SC 钉它。这是 memory `split-makes-seams` 的教科书形状 (「实现无归属 / 单侧修复」)。

我作为母 Spec 的 A.2 执笔人, 从三张表派生任务时**根本看不到这个切换的存在** —— 我会写死一个 AI 手工取的模板并给它配 SC-22, 然后就完事了。

字段 Spec 自己在「新表面 #8」(`:602`) 承认了一半:「该切换点未写成 SC (行为面), 请 R6 看是否需要」。但缺的不只是 SC —— 缺的是**实现归属**, 这一半没被承认。

**为什么是 Critical**: 派生不出来 (做不出)。且切换发生时会**第二次编辑同一个 SKILL.md 块**, 那个块被 SC-22 的六字面量 + 幂等谓词 + 块边界钉着, 谁改、改完谁重跑 SC-22 与 rule6_note 的 AB 照跑, 全无定义。

**建议处置**: 三选一, 但必须落到某一张 Impact 表里 —— (1) 母 Spec 的 A.1 模板从第一天就写成两步 (先 `--emit-arg` 取实参, 空则省略), 并把「字段 Spec 未 ship 时该命令不存在 ⇒ fail-soft 回落 AI 手工取」写进块内 (母 Spec Impact 加一行, 字段 Spec 只负责让脚本存在); 或 (2) 字段 Spec 认领这次编辑, 在其 Impact 加 `phase-a-planner/SKILL.md` + `spec-drafter/SKILL.md` 两行并改其非目标; 或 (3) 显式成文「本切换不在两份 Spec 范围内, 开独立 follow-up issue」——但那样母 Spec 的 A.1 就永久停在手工取上, 需要 owner 知情。

---

#### 字段 C6 — hunk B 让预览骨架默认写哨兵 `none`, 把「零证据当正证据」做成了写入侧的默认值

**位置**: 字段 Spec `:142` 与 `:571` (hunk B), 对 `:116` (SOT 模板) 与 `:154` (§2 哨兵语义)。

hunk B 逐字 (`:142`):

> **hunk B (新)**: 预览围栏内 `:140` 后插 `> **Created**: {YYYY-MM-DD}` 与 `` > **Linked Issue**: `none` `` 两行, 使头部与 SOT 逐行对齐

SOT 模板那一行逐字 (`:116`, 在围栏内):

> ```
> > **Linked Issue**: `{<org>/<repo>#<n>}`
> ```

**实读确认漂移前提为真** (`git -C aria show d50f9c3:skills/spec-drafter/SKILL.md | sed -n '139,140p'`):

```
> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
```

以及 `sed -n '3,5p' standards/openspec/templates/proposal-minimal.md`:

```
> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: {YYYY-MM-DD}
```

R5/C1 的事实判定成立 (预览骨架确实缺 `Created`, SOT 三行)。**但落版处方引入了一个新的、更严重的缺陷**:

两个写入侧产物的默认值语义**相反**:

| 产物 | 默认值 | E5 判定 | check 后果 | 语义 |
|---|---|---|---|---|
| SOT 模板 (`standards/.../proposal-minimal.md`) | `` `{<org>/<repo>#<n>}` `` | `BAD_TOKEN` | **FAIL**, 点名该元素, fix 文案催作者填 | 「还没填」 |
| 预览骨架 (`spec-drafter/SKILL.md` 围栏, **AI 运行时真正照抄的那份**) | `` `none` `` | `OK` (哨兵) | **PASS**, 无人被提示 | 「**已核实**无关联」 |

§2 `:154` 与 §Why 反复强调哨兵是**正证据**: 「哨兵的语义是「已核实无关联」(一条正证据)」(母 Spec `:120` 同义)。把它设成骨架默认值, 等于让每一份 AI 起草的 proposal **在作者没做任何核实的情况下断言「我核实过, 没有关联 issue」**。

三条后果, 每条都打在这个 Spec 家族自己的立项目标上:

1. **字段可得性变成 100% 而信息量归零**。check 从此恒绿, 但它绿的原因是所有人都在默认断言「无关联」;
2. **母 Spec 主机制对这些 proposal 恒零输入**。哨兵 ⇒ `--linked-issue` 整参省略 ⇒ `phase1_gate.py:1230` 整块门控 ⇒ 母 Spec §6 缺口表首行那个「**最大的单项缺口**」从「今天基本没人写字段」变成「**结构性地每一份新 Spec 都命中**」;
3. **两条 SC 都测不到它**。SC-7a 只断言字段名字面 (`> **Created**:` / `> **Linked Issue**:`) 和四行顺序, 不断言值; SC-7 的坏臂是「省略该行 / 写成 markdown 链接形 / 留空 / 英文臂里译写成别的字段名」—— 「照抄骨架的 `none` 而其实有关联 issue」不在任何一臂里, 因为骨架就是这么写的。

这与 memory `false_green_dual_is_permanent_red` 与本家族反复援引的「零证据不得当正证据」是**同一条**纪律, 方向反过来用了。

**为什么是 Critical**: 照文实现会做错, 而且做出来的东西会**主动抵消**本 Spec 的立项目标, 同时让母 Spec 的主机制在新语料上恒无输入。

**建议处置**: 预览骨架用与 SOT **相同**的 placeholder `` `{<org>/<repo>#<n>}` `` (真正的「与 SOT 逐行对齐」), 让默认值判 `BAD_TOKEN` 从而被 check 点名 —— 这正是 K8 落版给 `BAD_TOKEN` 定的「整参省略 + 消费面按不合规呈现」那一格, 已经处理好了 placeholder 不会污染匹配面 (字段 SC-9 + 探针 SC-19 常量黑名单)。同时给 SC-7a 补一条负控:「围栏内的 `Linked Issue` 值**不得**是哨兵集合成员」, 这一条 baseline 也必红 (今天该行不存在)。

---

### Major

---

#### 母 M1 — §2.1 把 `derive_track_id` 的「超长」行为写成截断, 实读是 sha256 回落; 引的正是那几行

**位置**: 母 Spec `:138` (§2.1 表 `spec-slug` 行的依据格)。

母 Spec 逐字:

> (拼接侧**不预归一**; 归一由 `derive_track_id` 在 acquire 内部做 —— lower / `./_`→`-` / 截断 `MAX_TRACK_ID_LENGTH`=64 / 非 ASCII 走 sha256, `lib/track_id.py:70-76`)

**实读它自己引的那几行** (`git -C aria show d50f9c3:skills/state-scanner/lib/track_id.py | sed -n '70,76p'`):

```
    1. **Lowercase**: ``raw_id.lower()``
    2. **Translate** ``/``, ``.``, ``_`` → ``-`` via ``str.translate``
    3. **Truncate** to at most ``MAX_TRACK_ID_LENGTH`` (64) characters
    4. **Fallback**: if the *original* ``raw_id`` was longer than 64 characters
       OR contained any non-ASCII character, discard the step-1..3 result and
       return ``NON_ASCII_FALLBACK_PREFIX`` +
       ``sha256(raw_id.encode("utf-8")).hexdigest()[:SHA_HEX_LENGTH]``
```

实现体 (`sed -n '155p;162,169p'`):

```python
    use_fallback = len(raw_id) > MAX_TRACK_ID_LENGTH or not is_ascii(raw_id)
…
    if use_fallback:
        digest = hashlib.sha256(raw_id.encode("utf-8")).hexdigest()[:SHA_HEX_LENGTH]
        return f"{NON_ASCII_FALLBACK_PREFIX}{digest}"
…
    result = result[:MAX_TRACK_ID_LENGTH]            # Step 3  (no-op here since len ≤ 64)
```

同文件 `:147-148` docstring 逐字: 「**65+ chars**: step 4 triggered → sha256 fallback regardless of character content.」

⇒ **超过 64 字符不是截断, 是整串 sha256 回落**。第 3 步的截断在实现里被注释自陈为 no-op。母 Spec 的转述把回落条件砍掉了一半, 而它引的行号里就写着完整条件。

**为什么这在 1A 之后才要紧**: 常量 `NON_ASCII_FALLBACK_PREFIX = "sha256-"` (`:21`) + `SHA_HEX_LENGTH = 16` (`:25`) ⇒ 回落结果是 `sha256-` + 16 hex = 23 字符, **既不含 slug 也不含容器段的可读形式**。而 §2.1 的依据格正是靠「目录名是 A.1 起草时唯一已知且**人类可读**的身份」在论证 D18。1A 把最长的那一段 (Spec 目录名) 放进了 track-id, 所以它把这条回落路径**从冷门变成了近门**:

- 实测 uuid 段 = **8 位 hex** (`identity.py:196` 逐字「a newly generated 8-char hex UUID」) ⇒ 触发阈值 = slug 长度 > 55;
- 本仓 `openspec/changes/` 现有 9 份, 最长 slug 35 字符 (`aria-2.0-m6-dispatch-input-delivery` / `a1-entry-claim-duplicate-work-guard`);
- 本仓 `openspec/archive/` 去掉 `YYYY-MM-DD-` 前缀后最长 slug = **53** 字符 (`aria-2.0-m5-replay-reconciler-drift-review-loop-audit`) ⇒ **历史最大值离触发只差 2 个字符**;
- 而 §2.1 `:142` 成文允许的 hostname 兜底分支 (`identity.py:242` `return _hostname()`) 返回的 hostname 通常远长于 8 字符, **该分支上超阈值是常态而非例外**。

**为什么是 Major 不是 Critical**: 机制本身不坏 —— sha256 取的是**完整原串**, 两个容器仍得到不同 track-id, overlap 通道不死。坏的是 (1) 承重描述与代码不符, (2) 「人类可读」这条 D18 依据在一个近在咫尺的分支上不成立, 而 Spec 没有成文, (3) A.2 写 §2.1a 行为层 fixture 的人会按「截断」造夹具。

**建议处置**: §2.1 依据格改为逐字复述回落条件 (「原串 >64 字符**或**含非 ASCII ⇒ 整串走 sha256, 结果形如 `sha256-<16 hex>`, 不保留 slug 与容器段的可读形式」), 并在 §6 缺口表加一行「slug 长度 > 55 时 track-id 退化为不可读哈希 (已知限, 机制仍成立)」。

---

#### 母 M2 — §2.4b 四态表第 1 行对「键缺席」的定义, 在门控放宽之后为假, 且它恰好是哨兵轨的常态

**位置**: 母 Spec `:342` (四态表第 1 行) 对 `:333` (Impact 落点) 与 `:332` (门控 bullet)。

四态表第 1 行逐字:

> | 键**缺席** | **未检测** (既未传 `--linked-issue` 也未传 `--include-terminal`) | 「本轮**未检测**」 |

但 §2.4a `:333` 落点逐字:

> 把 `scripts/phase1_gate.py:1230` 的 `if args.linked_issue:` 改为 `if args.linked_issue or args.include_terminal:`, 块内 `read_claims(repo)` **只调一次**, 然后按 `args.linked_issue` / `args.include_terminal` 各自填键

⇒ 改完之后, 只传 `--include-terminal` 而不传 `--linked-issue` 时: 块**进入**了, `unknown_schema_claims` **被填**, `linked_issue_overlap` **仍然缺席** (因为它按 `args.linked_issue` 填)。四态表第 1 行的定义 (「既未传 A 也未传 B」) 对这个组合为假。

**而这恰是哨兵轨的唯一形态**: §2 `:111` 要求哨兵时省略 `--linked-issue`; §2.4a `:332` 要求「A.1 模板**恒带**该 flag (`--include-terminal`)」。三份在制 Spec 今天全部是哨兵 (`> **Linked Issue**: \`none\``, 本席逐字核过三份的头部行)。

⇒ 一个照四态表写消费方状态机的实现者会遇到一个「按定义不可能、实际最常见」的状态: 键缺席 + 我明明传了 `--include-terminal`。他会怎么处理? 没有定义。

**为什么是 Major**: 单侧可修, 且渲染出来的措辞 (「本轮未检测」) 恰好仍是对的, 所以不会立刻做错事; 但契约表是 A.2 派生消费方任务的直接输入, 定义错了就没法写可证伪的断言。

**建议处置**: 第 1 行括号改为「**未传 `--linked-issue`**」(单条件), 并在四态表下补一句「`--include-terminal` 独立控制 `unknown_schema_claims`, 与本表正交」。

---

#### 母 M3 — §5.2 退出路径表不穷尽 §2.3 的选项集: 两个会终结本轨的裁决没有 release 行

**位置**: 母 Spec `:441-447` (§5.2 表) 对 `:278-283` (§2.3 选项集表)。

§5.2 表共五行: 探索性放弃一个方向 / 放弃整个 issue / slug 改名 / A.1 成功并走完循环 / D.2b 对偶。

§2.3 的选项集里有两个**会终结本轨**的裁决在 §5.2 里没有对应行:

1. **`active` 档的「并轨」** (`:280` 逐字选项集: 「另起」/「**我去释放对方的 claim 后再开始 (两步人工)**」/「并轨」)。并轨的含义是两条轨合成一条 ⇒ 其中一条的 claim 必须被释放。若是我这条被并掉, 我要 release 自己 (§5.2 无行); 若是对方被并掉, 对方要 release —— 而 D6 / §非目标 `:625` 逐字「**不引入**跨容器 release」, 所以我做不了, 对方的 claim 只能挂到 sweep。**§5.2 一个字都没说。**
2. **`done` 档的「复用对方产出, 本轨不起 Spec」** (`:281`)。§2.3 在那一格里直接给了命令 (「⇒ 按 §5.2 走 `release_gate.py --raw-track-id "<本轨 A.1 原串>" --status abandoned`」) —— 但它指向的 §5.2 **没有这一行**。指针指到一个不存在的行, 是 memory `cross-doc-claim-verify-at-target` 的形状。

另有一条相关但更弱的: **`active` 档的「我去释放对方的 claim 后再开始 (两步人工)」** 在机械上由谁执行、执行什么, 全文无定义。§2.3 自己 `:286` 逐字承认「**无任何函数支持*定向*释放某个指定容器的 claim**」, `:287` 订正后说存在的只有「无差别的陈旧清扫」。⇒ 这个选项被渲染给 owner 之后, AI 拿不出任何可执行动作。SC-11 的坏臂 (「对 `done` 也给出『释放对方 claim』选项」的臂应可分辨) 恰恰把这个选项**保留**在 `active` 档而只在 `done` 档判它不成立。

**为什么是 Major**: 会误导但可单侧修 (§5.2 补两行 + §2.3 那格的措辞收敛)。不判 Critical 是因为 §2.3 的 `done` 档已经把命令写全了, 实现者照它抄不会写错命令, 只是从 §5.2 派生任务时会漏。

**建议处置**: §5.2 表补两行 —— 「**并轨 (§2.3 `active` 档)**: 被并掉的一方各自 release; 对方那条**不由本容器释放** (D6), 成文接受它挂到 sweep」与「**复用对方产出, 本轨不起 Spec (§2.3 `done` 档)**: 同「探索性放弃一个方向」」。并把 §2.3 `active` 档的「我去释放对方的 claim」措辞改成明确的人工动作描述 (「请对方容器的操作者在其侧跑 release; 本容器无可执行动作」)。

---

#### 母 M4 — 「放弃整个 issue = 逐方向 release」没有给出枚举方向的机制, 而机制其实存在

**位置**: 母 Spec `:444` (§5.2 第 2 行) 与 `:630` (非目标)。

逐字:

> | **放弃整个 issue** (不再做这个 issue 的任何方向) | = 对该 issue 下本容器的每个方向各做一次上一行。**没有「按 issue 批量释放」的命令, 也不新增** (那会重新引入按 `linked_issue` 定位的跨轨写入面) |

1A 之后 track-id **不再编码 issue**。所以「该 issue 下本容器的每个方向」这个集合, AI 要从哪里得到? Spec 没说。两个实现者会写出两种东西: 甲写「AI 回忆自己开过哪几个方向」(即本 Spec 立项要消灭的那种依赖), 乙写「跑一次 `phase1_gate.py --linked-issue <该 issue>` 读 overlap」。

**乙是对的, 而且 Spec 的上游文件知道**。owner 决策单第 1 项对 1A 的代价 (b) 逐字: 「同容器在同一 issue 上开多个方向时, 互报一条 `linked_issue_overlap` advisory 噪声 (同 issue 不同 track-id, 语义上正确 —— 它们确实是同 issue 的两条轨)」。母 Spec `:134` 也照抄了这句代价。

**本席实读确认这条通道确实可用** (`git -C aria show d50f9c3:skills/state-scanner/lib/collision.py | sed -n '271,279p'`):

```python
    for c in claims or []:
        if c.status in _TERMINAL:
            continue
        if not getattr(c, "linked_issue", None):
            continue
        if not _linked_issue_matches(own_key, own_linked_issue, c.linked_issue):
            continue
        if c.track_id == own_track_id:
            continue  # same-name collision — reconcile's job, not ours
```

**函数体内没有任何 container 过滤** —— 只按 `track_id` 自排除。所以同容器不同 slug 的 claim **确实**会出现在 overlap 里, 代价 (b) 为真, 枚举通道存在。

⇒ Spec 把这条通道当成「噪声代价」写进了 §2.1 的括号里, 却没有在 §5.2 里把它当成「机制」用。一句话就能补上, 没补 ⇒ 派生出的任务欠定。

**为什么是 Major**: 单侧可修, 且不修的话第 2 行本质上是一条无法执行的指令 (集合来源未定义)。

**建议处置**: §5.2 第 2 行加一句「枚举本容器在该 issue 下的方向 = 跑一次 A.1 认领命令 (带该 `--linked-issue`) 读 `linked_issue_overlap[]` 中 `container` 等于本容器的条目 —— 这正是 §2.1 代价 (b) 那条 advisory 的正当用途; 实读 `lib/collision.py:271-279` 该函数不按 container 过滤」。

---

#### 母 M5 — `--no-push` 修复是事实上的 ship 前置, 但既不在「前置依赖」也不在任何 SC 或闸门

**位置**: 母 Spec `:521` (rule6_note 硬前提)、`:16` (前置依赖行)、`:663` / `:662` (两个 Impact hunk)、`:759` (未做/存疑 #6)。

rule6_note `:521` 逐字:

> ⇒ **跑本表任何一条照跑前, harness 会话必须以 `ARIA_COORDINATION_NO_PUSH=1` 启动** (对应 aria-plugin 修复: `phase1_gate.py --no-push` / 同名 env var, 输出 JSON 记 `push_skipped: true`; …) 该修复是 Level 1 独立变更, **本 Spec 只引用其存在, 不承担它**。

**本席实读该修复的状态**:

```
git -C aria ls-remote origin 'refs/heads/fix/phase1-gate-no-push'   → 空 (未推)
git -C aria merge-base --is-ancestor 007d355 origin/master          → NO
git -C aria rev-parse origin/master                                 → d50f9c3
```

⇒ 该修复**只在本地分支上, 未推任何 remote, 不是 `origin/master` 的祖先**。

母 Spec 对它的依赖有三处, 强度都是硬的:

1. **rule6_note 的六条照跑** (`:675` Impact 行: `phase-a-planner.json` / `spec-drafter.json` / `phase-b-developer.json` / `branch-manager.json` / `phase-d-closer.json` / `state-scanner.json`) 全部以它为前提。Rule #6 的照跑是不可协商规则, 前提不满足就跑不了 ⇒ **Phase B 走不到发版**;
2. **Impact `:663`** 要求给 `phase-b-developer/SKILL.md` 的 `skip_if` 补一句「`--no-push` / `ARIA_COORDINATION_NO_PUSH` 只抑制推送, 不是 skip 条件」—— 描述一个未 ship 的 flag;
3. **Impact `:662`** 要求给 `state-scanner/SKILL.md:168` 的输出键集补 `push_skipped` / `push_skipped_reason`。**本席实读 `:168`** (`git -C aria show d50f9c3:skills/state-scanner/SKILL.md | sed -n '168p'`): 「CLI 输出 `{outcome, proceed, track_id, error, own_claim, competing_winner, surface, push_success}`。渲染规则:」—— 确实无这两个键。若 `--no-push` 未先 ship, 母 Spec 落地后这一行会宣告两个 CLI 从不输出的键, 即造一条假文档。

而母 Spec 的「前置依赖」行 (`:16`) 只列 `linked-issue-normalization`, `grep -c 'no-push'` 该行 = **0**。闸门状态表 (`:767-773`) 也没有它。唯一的痕迹是「未做/存疑 #6」(`:759`) 的一句「若该修复未 ship 而先跑 AB, 前提失效; R6 请核该分支是否真存在」—— 分支确实存在, 但**存在不等于 ship**, 而这一句问的正是那个较弱的问题。

**为什么是 Major**: 单侧可修 (加一行前置依赖 + 一条 Phase B.1 前置断言), 但不修的话 A.2 的任务排序会漏掉一个跨仓 ship 依赖, 而这个依赖卡住的是 Rule #6 —— 不可协商规则。

**建议处置**: 母 Spec 头部「前置依赖」增一行「aria-plugin `--no-push` 修复 (决策单第 4 项; 分支 `fix/phase1-gate-no-push` @ `007d355`, **本席 2026-08-30 核: 未推 origin, 非 `origin/master` 祖先**) —— 它是 rule6_note 六条照跑与两处描述性 hunk 的硬前置」, 并在闸门状态表加一条「Phase B.1 开始前须断言该修复已合入 `origin/master`」。

---

#### 母 M6 — §Why 标注「可当场复核」的那段, 在 2026-08-30 改 dogfood 行之后三处皆假

**位置**: 母 Spec `:78` / `:83`。

`:78` / `:83` 逐字:

```
grep -rl '\*\*关联 Issue\*\*' openspec --include=proposal.md | wc -l   # 15  (14 在 archive/, 1 在 changes/)
```

> **落盘后的现状 (可当场复核)**: 旧 §1 连同那行示例已迁出, 本文件按 FIX-19 补了**真的**字段 (第 12 行) ⇒ `changes/` 下的 1 条命中现在是**真阳**。

**本席逐字复跑该命令**:

```
$ grep -rl '\*\*关联 Issue\*\*' openspec --include=proposal.md | wc -l
17
$ grep -rl '\*\*关联 Issue\*\*' openspec/changes --include=proposal.md
openspec/changes/linked-issue-field-availability/proposal.md
openspec/changes/sibling-spec-probe/proposal.md
openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
```

三处皆假:

1. 「第 12 行」—— 实读 `sed -n '13p'` 才是那一行 (`> **Linked Issue**: \`none\` — 本 Spec 源自 5 次并发起草事故的直接观察 …`), `:12` 是 `> **Spec Level**: 2`;
2. 「`changes/` 下的 1 条命中」—— 实测 **3** 条;
3. 「现在是**真阳**」—— **正好反了**。08-30 把 dogfood 行改成英文 canonical `> **Linked Issue**:` 之后, 它**不再匹配这条中文谓词**; 本席实测 `grep -nE '^> \*\*关联 Issue\*\*:' 母Spec` = **0 命中**。现在 changes/ 下这 3 条全部是讨论式**假阳**, 真字段一条都不在里面。

这一段的整个论证 (「主机制的输入九成缺席」) 结论仍成立, 但它自己标了「可当场复核」, 而当场复核会得到相反答案。这正是 memory `past-summary≠measurement` 与本家族反复自省的形状, 由 08-30 的哨兵改名一并引发而未回灌。

**为什么是 Major**: 不改变任何设计结论, 但它是被显式邀请去复核的一段, 复核即翻车; 且它是字段 Spec 全部语料统计的上游锚点。

**建议处置**: `:78` 的命令改为同时含两拼写 (`grep -rlE '\*\*(Linked Issue|关联 Issue)\*\*'`), `:83` 那句改为「本文件按 FIX-19 补了真字段 (第 **13** 行, 2026-08-30 起用英文 canonical); **中文谓词已不再命中它** —— 复核须用两拼写谓词, 口径见字段 Spec E0 谓词 1」。

---

#### 探针 M7 — SC-17 的「全文恰 2 次」与本 Spec 自己要求在同一文件新增的契约节相冲

**位置**: 探针 Spec `:498` (SC-17) 对 `:526` (Impact `execution-modes.md` 行) 与 `:385`。

SC-17 逐字:

> | **SC-17** ⭐ (§8 双落点) | 代码 | 对 `references/execution-modes.md` **全文**计数字面串 `每轮入口: 竞品 spec 探针` | 出现**恰 2 次**, 且两次分别落在 `## Convergence 模式` 与 `## Challenge 模式` 两节的围栏块内 |

Impact `:526` 逐字 (同一个文件):

> **另新增一节** `## 竞品 spec 探针 (per-round 入口)` 承载 §7 十二字段 stdout 契约 + exit code 三分 + §9 三档消费措辞的**权威可执行版**

**好消息 (本席逐字比对)**: 新节标题 `## 竞品 spec 探针 (per-round 入口)` 与计数串 `每轮入口: 竞品 spec 探针` **逐字节不同** (词序相反), 标题本身不会把计数推到 3。

**坏消息**: 新节的**正文**要承载三档消费措辞的权威版, 而三档措辞的第一档就以「每轮入口」这个概念开头, 任何自然的写法 (例如「每轮入口: 竞品 spec 探针 的 stdout 契约如下」) 都会命中。SC-17 数的是**全文**, 不是「两个模式块围栏内」。⇒ **一个完全正确的实现会因为在同一文件写了本 Spec 自己要求的那一节而判红。**

§8 `:384` 只讨论了「若将来出现第三个模式块」这一种超计数场景, 完全没有意识到本轮同批新增的那一节就在同一个文件里。

**为什么是 Major**: 单侧可修 (把计数域从「全文」收到「两个模式块的围栏内」, 或在新节里禁用该字面), 但不修就是一条会误伤正确实现的断言 —— 而 SC-17 是本 Spec 唯一钉住「Challenge 模式不被漏 patch」的机械护栏, 它一红就会被后来者当成 bug 直接删掉。

**建议处置**: SC-17 的场景列改为「对 `## Convergence 模式` 与 `## Challenge 模式` **两节的围栏块切片**计数, 每块恰 1 次; 并追加一条负控: 除这两处外全文该字面 0 次」。

---

#### 探针 M8 — 没有任何 SC 钉 `execution-modes.md` 新契约节的存在, SKILL.md 的指针可以悬空

**位置**: 探针 Spec `:385` / `:525` / `:526`, 对 SC-17 (`:498`) 与 SC-20 (`:501`)。

`:385` 逐字:

> stdout 契约 (§7 十二字段) 与消费措辞 (§9) 的**权威可执行版**落 `execution-modes.md` 新节 (R5/M3), SKILL.md 放概述 + 指针, 与 `audit-engine/SKILL.md:236-237`「权威可执行版见 references/…」的既有体例一致。

我作为实现者列出全部机械验收:

- SC-17 → `execution-modes.md` 两处插入串;
- SC-20 → `audit-engine/SKILL.md` 的「per-round 入口探针」小节 (四字面量 + 完整命令行);
- SC-15 → 探针运行时的 stdout 契约;
- 其余 SC → 探针脚本行为。

**没有一条断言 `## 竞品 spec 探针 (per-round 入口)` 这一节存在。** ⇒ 一个跳过它的实现在全部 20 条 SC 上全绿, 而 SKILL.md 的「指针」指向一个不存在的小节。

这正是本家族自己反复抓的形状: 母 Spec `:668` 抓 `layer-l-integration.md:45` 的悬空函数名 `update_heartbeat()`; 探针 Spec `:515` / follow-up 1 抓 `fetch_gate.py:21` 的悬空函数名引用; memory `delegate-verify` 的「写『移交 X』前必去 X 核」。这次是**自己新造一个**。

**同形缺陷在母 Spec 也有**: 母 Spec Impact `:662` 逐字「三级回落表 / 遥测分区边界 / fail-CLOSED 新鲜度谓词 **整体落 reference** (否则 `:178`「完整设计意图见 references/…」变假指针…)」, 而 rule6_note 第 10 档的 substitute (`:518`) 只断言「该文件不含字面 `update_heartbeat`, 且含 `heartbeat(`」—— **同样没有一条断言那个新设计段存在**。本席实读 `state-scanner/SKILL.md:178` 确认该指针句今天就是「**完整设计意图 (…)**: 见 [references/layer-l-integration.md](./references/layer-l-integration.md)。」。

**为什么是 Major**: 单侧可修, 各加一条 baseline-必红的结构断言即可。

**建议处置**: 探针 SC-20 追加一臂「`references/execution-modes.md` 含标题 `## 竞品 spec 探针 (per-round 入口)`, 且该节切片内含 §7 的 `verdict` / `status` / `hits` 三个字面与 §9 三档措辞的三个字面」; 母 Spec 的 rule6_note 第 10 档 substitute 同批追加「`layer-l-integration.md` 含标题字面 `Layer L A.1 heartbeat 集成`, 且该节切片内含 `--heartbeat-only` 完整命令行」。两条 baseline 都必红。

---

#### 字段 M9 — D17 声明为「三要件」却没有声明适用范围, 其第 2、第 3 要件对 SC-7a 的被测对象结构性不适用

**位置**: 母 Spec `:500` (D17) 对 字段 Spec `:543` (SC-7a) 与 `:142`。

D17 逐字把自己定位成类级处方并点名三个消费者:

> **两子 Spec 各引用本条, 不各自重发明** (字段 SC-7a / 探针 SC-20)

本席逐条核这三处是否真的落了三要件:

| SC | 第 1 要件 (块边界) | 第 2 要件 (完整命令行) | 第 3 要件 (fail 措辞字面) |
|---|---|---|---|
| 母 SC-22 | 落了 | **没落** (见母 C2) | 落了 (`未能核实`) |
| 字段 SC-7a | 落了 (块边界 = 预览围栏) | **结构上不适用** | **结构上不适用** |
| 探针 SC-20 | 落了 | 落了 (`python3` 起首 + `--own-spec-dir`) | 落了 (`未能核实`) |

字段 SC-7a 的被测对象是 `spec-drafter/SKILL.md` 的 **Level 2 预览骨架** —— 一份 proposal 模板, 不是指令块。它**没有**、也**不应该有**可执行命令行或 fail 分支措辞: 往预览骨架里塞一行 `python3 …` 会被 AI 原样复制进每一份生成的 proposal。字段 Spec `:142` 自己也只引了第 1 要件 (「引母 Spec **D17** (块边界 = 该预览围栏; 断言只在围栏内求值)」) —— 它做对了, 但 **D17 的原文没有给它这个豁免**。

⇒ D17 写成了一条无条件的三要件类级规则, 而它自己点名的三个消费者里有一个只能满足其中一件。一个照 D17 字面办的 A.2 实现者要么给预览骨架加命令行 (害人), 要么发现规则不适用后自行裁量 (Rule #10 忌讳的自作主张)。

**为什么是 Major**: 单侧可修, 且当前执笔已经事实上做对了; 但规则本身的表述会误导下一个引用它的人 (D17 的整个价值就在于「一处定义消掉三处」, 定义不带范围就会在第四处出错)。

**建议处置**: D17 增一句范围限定 —— 「**第 1 要件 (块边界)** 适用于任何被机械断言的块; **第 2、3 要件 (完整命令行 / fail 措辞)** **仅适用于指令块** (块的目的是让 AI 执行动作), 不适用于模板 / 骨架块 (块的目的是被复制成产物)。引用本条的 SC 须写明自己落了哪几件。」

---

### minor

- **母 m1** — Impact `:655` 的 `phase1_gate.py` 行逐字写「本行只改下列五处」, 实际列了六项 (末项是 R4/K5 的「同一 `except` 分支须同时赋 `out["unknown_schema_claims"] = None`")。计数与内容不符, A.2 按「五处」派生会漏第六项。

- **母 m2** — 两处把 `complexity: Level1` 的行号记成 `:66`, 实读是 `:67`。Impact `:658` 逐字「Level 1 (`skip_if: complexity: Level1`, 实读 `:66`)」, 未做/存疑 #2 (`:755`) 逐字「(`skip_if: complexity: Level1` 在 `:66`)」。实读 (`git -C aria show d50f9c3:skills/phase-a-planner/SKILL.md | sed -n '65,67p'`): `:65` = `  skip_if:`, `:66` = `    - has_openspec: true          # 已有活跃 Spec`, `:67` = `    - complexity: Level1          # 简单任务`。同段的 `:62-73` 范围本身正确。

- **母 m3** — FIX-19 对账行 `:728` 逐字「本文件 `> **Linked Issue**: \`none\`` (第 12 行一带…)」与 §Why `:83`「第 12 行」, 实读均为 `:13`。`:728` 有「一带」两字兜着, `:83` 没有 (已并入母 M6)。

- **字段 m4** — §5 作用域表 `:461` 逐字「**OK** (`:12` token 串 `none`, 2026-08-30 改英文 canonical…)」, 母 Spec 实读为 `:13`。

- **字段 m5** — §5 作用域表 `:469` 同一个单元格内自相矛盾: 首列写「**OK** (`:6` token 串 `none`, 2026-08-30 改)」, 末列却写「本席实读其 `:6` 为 `> **关联 Issue**: \`无\` — …」。本席实读探针 Spec `sed -n '6p'` = `> **Linked Issue**: \`none\` — 本 Spec 由母 Spec 的 owner 裁定 …`。那条标了「本席实读」的逐字引文已经失效, 且与同格首列冲突。

- **探针 m6** — `:385` / `:525` 引「`audit-engine/SKILL.md:236-237`「权威可执行版见 references/…」的既有体例」。实读 `sed -n '236,237p'`: `:236` = `# #17 振荡豁免: keys 全部取 normal_rounds 重索引序列 (is_refocus 轮剔除),`, `:237` = `# 本节为简化概述 — 权威可执行版见 references/convergence-algorithm.md 终局 3`。被引的那句只在 `:237`, `:236` 是另一句。引文内容真实, 锚点多含一行。

- **探针 m7** — SC-20 (`:501`) 的块边界正则逐字 `(?m)^#{2,4}[ \t]+.*per-round 入口探针`, 前缀是 `.*` ⇒ 一个写成 `### Step 0.5: per-round 入口探针` 的实现照样匹配, 而 §8 `:362` 逐字明令「**命名 = 「per-round 入口探针」, 不叫「Step 0.5」**」并给了理由 (`:364`: `audit-engine/SKILL.md:85` 逐字「入口逻辑完成后、**Round 1 启动前一次性**执行」与「每轮」自相矛盾)。断言与它要执行的规定之间少一条负控。

---

## (c) 本席核验为真、无 finding (下一轮免重复)

以下每条都由 `git -C aria show d50f9c3:<path> | sed -n 'Np'` 或在主仓工作树逐字复跑得到, **不是 grep 拼接**:

**代码引文全部逐字命中**

- `lib/collision.py`: `:230-234` 三参数签名 `def linked_issue_overlaps(claims, own_track_id, own_linked_issue)` / `:265-266` `if not own_linked_issue:` + `return []` / `:268` `_TERMINAL = ("done", "abandoned", "unknown")` (函数内局部) / `:272-273` / `:274-275` / `:278-279` 含注释 `# same-name collision — reconcile's job, not ours` —— **六处逐字节一致**;
- `lib/identity.py`: `:191` 定义 / `:222` `return label if label else uuid` / `:242` `return _hostname()` / `:244` `return uuid` —— 四处一致; `:196` docstring 逐字「a newly generated 8-char hex UUID」证实 uuid 段 = 8 hex (母 Spec「定长 hex, 碰撞域 16⁸」成立);
- `lib/coordination_ref.py:800` = `boot = bootstrap(repo_path=repo, push=False)` —— 决策单第 4 项对 R5-3 的机制勘正为真;
- `scripts/phase1_gate.py:1190-1191` `--phase` `required=True` (母 Spec `:233` R3/BA-M1 的引用正确);
- `skills/phase-b-developer/SKILL.md`: `:86` B.0 起始行 / `:92` `--raw-track-id "<本 cycle carry-id/Spec id>"` / `:96-97` 那两行 auto_bootstrap push 注释 / `:98` `coordination.enabled 显式 false` —— 母 Spec Impact `:663` 的四个锚点全中;
- `skills/branch-manager/SKILL.md:146` = `### 前置: REQUIRE claim (Part A1, MUST — 与 phase-b-developer B.0 同一条约束)` —— 母 Spec 要改 `Part A1` → `Part B1` 的前提为真;
- `skills/phase-a-planner/SKILL.md:9` = `allowed-tools: Read, Write, Glob, Grep, Task, Skill` / `skills/spec-drafter/SKILL.md:10` = `allowed-tools: Read, Write, Glob, Grep, AskUserQuestion` —— 两处逐字, C1 扩权的变更前值正确;
- `skills/spec-drafter/SKILL.md`: `:127` 围栏开 / `:139` `> **Level**: Minimal (Level 2 Spec)` / `:140` `> **Status**: Draft` —— **R5/C1 的「预览骨架只有两行、缺 `Created`」逐字为真**; 对照 `standards/openspec/templates/proposal-minimal.md:3-5` 确为三行且含 `Created`, 且全文 `Linked Issue` / `关联 Issue` 两拼写命中均为 **0** (字段 SC-6 的 baseline 必红成立);
- `skills/state-scanner/SKILL.md`: `:149` (接线点 = AI 编排层 + 触发条件含 `collision.kind`) / `:168` (输出键集, 确无 `push_skipped`) / `:176` (Layer L 消费契约段) / `:178` (指向 layer-l-integration.md 的指针句) —— 四处一致;
- `skills/audit-engine/`: 全目录 **8 个文件, 无 `scripts/` 无 `tests/`** (探针 Spec `:60` 正确); `SKILL.md:83` = `### Step 0: Anchor 固化 (Drift Guard #17, v1.44.0)`, `:85` = 「入口逻辑完成后、**Round 1 启动前一次性**执行…」—— 探针 §8 的消歧理由成立;
- `skills/config-loader/DEFAULTS.json:124-128` = `adaptive_rules` 含 `"level_3": "challenge"` —— 探针「下游 Level-3 走 Challenge, 只 patch 一块会静默漏」的论证成立。

**探针 §8 的插入位置无歧义** —— 实读 `execution-modes.md`: `## Convergence 模式` `:84`, 围栏开 `:88`, `Round N:` `:89`, `1. 调用 agent-team-audit 单轮引擎` `:90`, 围栏闭 `:111`; `## Challenge 模式` `:113`, 围栏开 `:117`, `Round N (一个完整周期):` `:118`, `Step 1: 讨论组 spawn → discussion_output` `:119`, 围栏闭 `:140`。**六个锚点全部存在且唯一**, 两处插入点可无歧义定位。

**三条机械不变量本席复跑, 全绿**

1. **每个 `SC-NN` 在 SC 表内有一行**: 母 Spec 全文出现 SC-1 到 SC-33 共 33 个编号, 逐个数行首表格行 (`^| \*\*SC-N\*\*` 或 `^| SC-N `), **33 个全部恰 1 行**, 无 0 无 2。R5-1 的「SC-30/31/32/33 在表 0 行」已实质关闭;
2. **每个 `--flag` 在 Impact 表内被点名**: 全文 16 个 `--xxx` 形态串, Impact 表 (`:646-677`) 覆盖 12 个; 差集 4 个经实读全是 grep 假阳性 —— `--flag` 是「CLI flag」这个词组的一部分、`--include` 是 `--include=proposal.md` 的前缀截断、`--is-ancestor` 与 `--stat` 是 git 命令。**实质差集 = 0**;
3. **同一枚举全文一种拼写**: 三份 Spec 合计 `bad_token_union` 4 次**单一拼写** (R4/C-M1 的两侧已统一); `none_sentinel` 10 次单一拼写; `wu_empty` 残留 3 次, 逐条实读**全部在「原 `"wu_empty"`, 2026-08-30 改名」这类撤销说明里**, 无一处是活跃取值。

**1A 残留 grep (母 Spec 新表面 #1 的问题) —— 本席判定不成立**: 全文 `派生形` / `回落形` / `track_form` / `spec_slug` / `--spec-slug` 的每一处命中经逐行实读, **无一处是「按有无 issue 分形态」的活条款**, 全部落在: Status 行的裁定摘要、`:134` 的取消说明、`:158` 的「1A 前另有 `str(int(n))` 归一, 已随 issue 派生形取消」、`:175` / `:425` / `:451` / `:486` / `:495` / `:501` 的撤销与依据、SC-1/4/27/30/31 的 ⛔ 行、`:629` / `:648` / `:650` 的「不新增 / 零改动」、以及新表面表自问。**1A 的结构性移除是干净的。**

**哨兵与字段名跨三份一致 (母 Spec 新表面 #8 / 字段 #7 / 探针 #9 的问题) —— 本席判定不成立**: 三份头部 dogfood 行逐字读过, 全部是 `> **Linked Issue**: \`none\` — …`, 拼写与哨兵一致; `BAD_TOKEN` 在字段 (20) 与探针 (12) 两侧都用同一拼写与同一语义; 层枚举 `none_sentinel` 与哨兵集合 `{none, 无}` 在字段 §2 / 探针 层 1.5 / P5 三处措辞一致。**唯一的跨 Spec 不一致是母 Spec 完全没吸收 E6 的四格 (见跨 C4), 不是哨兵措辞问题。**

**`--no-push` 分支确实存在** (母 Spec 未做/存疑 #6 的问题): `fix/phase1-gate-no-push` @ `007d355`, 相对 `d50f9c3` 改动 4 文件 709 行 (`phase1_gate.py` / `release_gate.py` / `lib/failure_handlers.py` / 新测试 `test_coordination_no_push.py`)。**存在为真, 但未 ship — 见母 M5。**

**`linked_issue_overlaps` 无 container 过滤** ⇒ owner 决策单第 1 项对 1A 的代价 (b)「同容器多方向互报 advisory」**为真**, 且它同时是「放弃整个 issue」唯一现存的方向枚举通道 (见母 M4)。

**探针 SC-17 的计数串与 Impact 新节标题逐字节不同** (`每轮入口: 竞品 spec 探针` vs `## 竞品 spec 探针 (per-round 入口)`) ⇒ **标题本身不会破坏计数**; 破坏计数的风险在新节正文 (见探针 M7)。

**`--phase B` 在 `phase-a-planner/SKILL.md` 全文 0 命中**, `未能核实` 在 `phase-a-planner` / `spec-drafter` 两个 SKILL.md 全文均 0 命中 ⇒ SC-22 第 4 条负控今天不会误触, 第 2 条的 `未能核实` 字面 baseline 必红成立。

---

## (d) 收敛判断

### 落在 2026-08-30 新写文本上的比例

逐条归属 (判据: 该缺陷的**成因文本**是否由 rework v4 / 决策单落版写入):

| 严重度 | 总数 | 落在 08-30 新文本 | 说明 |
|---|---|---|---|
| Critical | 6 | **5** | 母 C1 / 母 C2 (SC-22 按 D17 重写) · 母 C3 (SC-32 08-30 入表, argparse 那句是新写) · 跨 C5 (字段 `:219` 新写) · 字段 C6 (hunk B 新写)。**例外**: 跨 C4 的成因是 2026-08-27 的 K8 四格表, 08-30 只是加宽了它 |
| Major | 9 | **8** | 母 M1 (§2.1 表随 1A 重写) · 母 M3 / M4 (§5 整节 08-30 重写) · 母 M5 (rule6_note ⛔ 段新写) · 母 M6 (由 08-30 改 dogfood 行引发) · 探针 M7 / M8 (Impact 新节 mandate 新写) · 字段 M9 (D17 新写)。**例外**: 母 M2 (四态表是 rework v3) |
| minor | 7 | **6** | 例外: 母 m2 (承前, 行号误记跨轮沿用) |
| **合计** | **22** | **19** | **86%** |

**86% 远超 1/2 的拐点判据** (memory `marginal-return-negative`: 判据是「本轮 fix 引入的 major 占比 > 1/2 即到拐点」)。R5 自己的口径是 skill-reviewer 席「6/8 落在自己新写的条款上 = 75%」, 本轮更高。

### 我是否同意「设计侧已收敛」

**不同意, 但反对的理由与 R5 五席的理由是正交的, 不是「他们错了」。**

R5 五席在 2026-08-29 说「设计侧收敛, 剩机械活」时, 他们审的是**当时那一版**。那句话对**那一版**很可能是对的 —— 本席复跑了 comment-analyzer 提出的三条机械收敛判据, 今天**三条全绿**, R5-1 的五项落版失败已实质关闭。

问题在于 **2026-08-30 的落版本身不是机械清账**:

1. **1A 是结构性重写**, 不是回灌。它改掉了 track-id 的定义、删了 §5.1/§5.3、重写了 §5 整节、撤了 6 条 SC、动了 5 行 Impact。母 Spec 自己的「新表面」表列了 **9 条**, 「未做/存疑」列了 **6 条** —— 一次纯机械清账不会产出 9 条新表面;
2. **D17 是新立的类级处方**, 08-30 才写, 08-30 就同时用在三份 Spec 上, 中间没有任何一轮审计。本席的母 C2 + 字段 M9 都直接落在它身上 (发源地没落全、适用范围没声明);
3. **第 6 项 + O-2 (哨兵与字段名英文化) 是跨三份 Spec 的接缝改动**, 由主控一人执笔未换人 (母 Spec 未做/存疑 #5 自陈)。母 M6 / 字段 m4 / 字段 m5 都是它的余波;
4. **E6 的四格表 (08-27 K8) 从来没被母 Spec 吸收过**。跨 C4 是三份 Spec 里唯一一条**不是** 08-30 新造的 Critical, 它在 R4 与 R5 之间就存在了, 两轮都没被抓到 —— 因为前几轮没有人做过「实现者试派生」这个动作: 你只有在同时拿着母 SC-12 和字段 E6 表去写两个 fixture 的时候, 才会撞到它们互斥。

⇒ **准确的判断是: 「R5 那一版的设计侧收敛了」为真; 「今天这一版的设计侧收敛了」为假 —— 因为今天这一版是新的。**

### 对下一步的建议 (非裁定, 供 owner 与主控判)

按 memory `stop-adding-rounds` 与 `marginal-return-negative`, 我**不建议**在当前落版方式下再加 R7 —— 86% 的自伤率说明再跑一轮通用审计只会产出下一批 86%。三条更有希望的路子, 按我的偏好排序:

1. **换执笔席落 R6 的 6C/9M** (memory `fix-writer-bottleneck`: owner 两轨的处方都是「换人执笔」)。本轮 6 条 Critical 里有 4 条 (母 C1/C2/C3 + 字段 C6) 是**同一形状**: 一条新写的处方/断言与它自己旁边那句话冲突。这不是知识不足, 是同一执笔者在长文档里对自己上一句的盲区;
2. **落版后只做定向复核, 不做通用轮**: 6C/9M 每条我都给了可机械复核的判据 (逐字字面 / 行号 / 三态), 一个新席位拿这张表逐条核比一轮五席通用审计信息量高;
3. **把 D17 从「散文规则」升级成一个共享的断言辅助函数**再谈落版 —— 母 C2 / 字段 M9 / 探针 m7 三条的共同根因是「三个地方各自把同一条规则翻译成正则」。memory `no-code-host-no-assertion`: 没有代码宿主的类级规则, 在每个引用点都会退化成不同的东西。

**Rule #10 留痕**: 以上是本席作为审计席的建议, **不是裁定**。是否加 R7、是否换执笔席、是否采纳任一条处置建议, 都属 owner 权限面。本席也**没有**对三份 Spec 或任何仓内文件做任何修改。

---

## (e) counts

- **Critical: 6** — 母 C1 (SC-22 第 5 条与块边界互斥) · 母 C2 (SC-22 未落 D17 第 2 要件) · 母 C3 (SC-32 与 Impact「零改动」互斥) · 跨 C4 (母 SC-12 与字段 E6 四格互斥) · 跨 C5 (`--emit-arg` 切换无实现归属) · 字段 C6 (预览骨架默认哨兵 = 写入侧零证据当正证据)
- **Major: 9** — 母 M1 (归一超长行为描述错) · 母 M2 (四态表键缺席定义错) · 母 M3 (§5.2 不穷尽 §2.3) · 母 M4 (逐方向枚举机制缺) · 母 M5 (`--no-push` ship 前置未成文) · 母 M6 (「可当场复核」段三处皆假) · 探针 M7 (SC-17 计数域与同文件新节相冲) · 探针 M8 (新契约节无存在断言) · 字段 M9 (D17 未声明适用范围)
- **minor: 7** — 母 m1 (五处/六项) · 母 m2 (`:66` vs `:67`) · 母 m3 (第 12 行 vs `:13`) · 字段 m4 (母 `:12`) · 字段 m5 (`:469` 逐字引文失效且自相矛盾) · 探针 m6 (`:236-237` 锚点多一行) · 探针 m7 (SC-20 正则不禁 `Step 0.5`)

**counts: 6C/9M/7m · verdict: REVISE · scope_ok: true**
