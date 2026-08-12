---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-12
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — backend-architect 独立审计

被审对象: `openspec/changes/premerge-gate-branch-existence/proposal.md`(Spec A, Level 2)。
本轮聚焦实现可行性: 插入点 / 退出码分区 / 异常·重试·解码三轴 / "纯 additive" 代码级复核 /
划界是否自足。

---

## Finding 1 (CRITICAL) — "存在性核验单独就关掉恒绿腿" 在 AI 实际执行的路径上不成立; Spec A 不自足

**结论先行**: Spec A 全部承诺 (`_verify_branch_exists()`) 都插在
`aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` 的 `gate_check()` 函数内。
但 AI 在 C.2.4 实际执行的不是这个函数 —— 是 `SKILL.md` §C.2.4"执行流程"里的裸
`aether ci status` 命令。这条真实执行路径结构上永远不会触达 `gate_check()`,
因此也永远不会触达本 Spec 新增的存在性核验。**Spec A 上线后, #137 报的恒绿症状在生产
AI 执行路径上原样复现, 零改善。**

**证据链 (全部本轮实读/实跑, 非引用旧结论)**:

1. `pre_merge_gate.py:1-445` 全文实读: `gate_check()` 定义于 `:298-407`,
   `_verify_branch_exists()` 按 Spec A §3 (proposal.md:96-113) 将插入 `:345` 后 / `:356` 前 ——
   五个行锚 (`:328/:338/:344/:345/:356/:357/:358/:366`) 逐字命中,
   插入点判断本身是对的 (见下 Finding 2 之前的"核验通过项"记录)。**问题不在插入点选址,
   在于选址所在的这个函数是否会被调用。**

2. 实跑:
   ```
   $ grep -n "pre_merge_gate\|aether ci status\|gate_check(" \
       aria/skills/phase-c-integrator/SKILL.md
   ```
   结果 (SKILL.md §C.2.4"执行流程", `:166-168` 与 `:238-244`):
   - `:167` `- aether ci status --branch main --in-flight --json (查 main 是否有 in-flight)`
   - `:168` `- aether ci status --branch <PR_BRANCH> --json (查本 PR CI 状态)`
   - `:243` `**Query main in-flight**: \`aether ci status --branch main --in-flight --json\` → parse \`data.runs[]\` — …`
   - `:244` `**Query PR CI status**: \`aether ci status --branch <PR_BRANCH> --json\` → …`

   `pre_merge_gate.py` 在 SKILL.md 里只出现于 `:262`(`**Helper 实现**: <路径>` 一句说明,
   非可执行命令)与 `:308/:310/:316`(§C.2.4.X 背景说明)。**全文零处示范
   `python3 …/pre_merge_gate.py --pr-branch … --main-branch …` 这种带参调用**;
   `main()`/`gate_check()`/`_verify_branch_exists()` 均无从被 SKILL.md 指令激活。

3. 排除"服务端/CI 自动调用"这条替代路径: 遍历本仓与 `aria` 子模块全部
   `.forgejo/.gitea/.github/workflows/*.yml`, 无一处调用 `pre_merge_gate.py`
   (`find … -iregex '.*\.(forgejo|gitea|github)/workflows/.*\.(yml|yaml)'` 命中的唯一文件是
   `aria/.forgejo/workflows/issue-triage-tests.yml`, 与本 gate 无关)。⇒ **今天没有任何生产路径
   (AI 手动执行 或 CI 自动触发) 会调用 `gate_check()`**, 只有测试套件调用它。

4. **这不是我的新发现, 是本项目自己在拆分前就已实读并写入审计记录、但拆分时被漏带的事实**:
   `.aria/audit-reports/post_spec-R3-1786222430202-premerge-gate-mainbranch-failclosed-tech-lead.md:46-49`
   逐字:
   > 「但这个结论回答的不是真正的问题。见下方 C1: `main_branch` 参数只存在于 `main()` 与
   > `gate_check()` 两个入口, 而 `SKILL.md` 全文从未示范过带参数的 helper 调用
   > (`grep -n "pre_merge_gate.py" SKILL.md` 只有 `:262` 一处, 是「Helper 实现: <路径>」的
   > 说明句, 不是可执行命令)。AI 被指令执行的是 `:167` 与 `:243` 的 raw aether 命令。
   > 必填参数对那条路径零作用。」

   该轮 tech-lead 是针对 **B 侧的 D5 (`--main-branch` 改必填)** 提出此问题的, 但这条事实
   ("AI 走的是 `:167`/`:243` 的裸命令, 不是 `pre_merge_gate.py`") 与被治理的具体参数/逻辑
   **无关** —— 它讲的是"这整个函数是不是死代码(对生产路径而言)", 对 D5 成立, 对本 Spec 新增
   的 `_verify_branch_exists()` **同样成立、逐字成立**, 因为二者插在同一个从未被调用的函数体内。
   `post_spec-R4-1786244936248-premerge-gate-mainbranch-failclosed-tech-lead.md:113` 独立复核同一
   事实 ("`pre_merge_gate.py` 在 SKILL.md 出现 4 次… 均无带参示范")。**两轮独立审计已把这件事
   钉死为项目共识, Spec A 的 §Why/DEC 却完全没有引用或反驳它。**

5. Spec A 自己的证据也印证了这一点而不自知: §Why"症状"(proposal.md:22-25)
   实测的对象**正是** `aether ci status --branch main` 与 `--branch master`(裸命令), 不是
   `gate_check()` 的输出。也就是说 Spec A 用来论证"问题存在"的实验, 走的正是那条
   `_verify_branch_exists()` 永远碰不到的路径; 而它用来论证"问题已解决"的机制,
   却装在另一条今天无人调用的路径里。**同一份文档的诊断实验与处方实现, 分别验证了两条不同的
   执行路径, 二者从未被证明是同一条。**

**这解释了为什么 DEC-20260812-001 的划界依据 (§3) 站不住**: DEC §3(`docs/decisions/DEC-20260812-001-premerge-gate-spec-split.md:64-83`)
把"参数必填留给 B"的理由建立在"存在性核验单独就足以关掉恒绿腿"这句话上, 直接引用
proposal 的症状段落作依据, 但**没有引用/反驳上面第 4 点那条已经写在同一批审计材料里的
反例**。Spec A 承接了 DEC 的这个结论(proposal.md:27-35), 同样没有讨论"这个 fix 会不会
被实际执行到"这个问题。§非目标(proposal.md:207-208)明确排除 D1
("不改 SKILL.md 两处散文流程"), 但没有承认排除 D1 的直接后果是"本 Spec 交付的代码在
B 落地前对生产症状零作用"。

**怎么会红 (可证伪, 且今天就能复现, 不需要等 Phase B)**:
Phase B 按 Spec A 逐字实现 `_verify_branch_exists()`(不改 SKILL.md 执行流程, 这是 A 自己
的非目标), 合并上线。之后随便一个真实 PR 场景: `.aria/config.json` 里
`main_branch` 配置指向一个远端不存在的分支(或 AI 在 C.2.4 按 SKILL.md 字面指令执行),
AI 会照 `:167`/`:243` 跑 `aether ci status --branch <main> --in-flight --json` ——
这条命令**不经过 `pre_merge_gate.py`**, 新增的存在性核验**不会被执行**, 输出仍是
Spec A 自己在 §Why 实测过的 `status:ok, runs:[]`, RC=0, verdict 仍判 green。
**#137 的原始症状原样复现。** 唯一会体现出 Spec A 效果的路径, 是测试套件与"有人手工
`python3 pre_merge_gate.py --pr-branch … --main-branch …`"这种今天全仓零示范、
不会被 AI 自发执行的用法。

**SC 集合的连带问题**: SC-A6/A13/A-zero/A7/A8/A10/A10b/A10c/A11/A14/A-sc22/A-baseline
(proposal.md:171-184) 全部是对 `gate_check()`/CLI 的直接单元或集成断言 —— **没有一条
断言"AI 沿 SKILL.md 指令执行时会触达这条检查"**。12 条 SC 即使全绿, 也只证明"这个函数
自己对自己正确", 证明不了"这个函数会被用到"。这不是 SC 遗漏了某个边角场景, 是**整个
SC 集合的测量对象与症状的真实发生场所不同源**。

**处置建议**: 三选一, 但不能不选:
(a) 把"至少一处 SKILL.md 执行步骤改为调用 helper(而非裸 `aether` 命令)"最小化地拉回 A
    的范围内(哪怕只改 `:243` 一行, 不做 B 侧的折叠块/五步收敛), 使新增检查在生产路径可达;
(b) 若坚持把它留给 B, Spec A 必须**显式声明**"本 Spec 落地后到 B 落地前, 对生产 AI 执行
    路径的实际效果是零", 把"关掉恒绿腿"的措辞从 Why/DEC 撤下, 换成"为 B 侧消费预先建好
    可复用的核验逻辑与测试", 并让 owner 在知情的前提下确认这个顺序可接受;
(c) 如果两侧都不做, 至少必须在 proposal 里新增一条"生产可达性" SC, 用真实/仿真 SKILL.md
    执行轨迹断言 `_verify_branch_exists()` 被触达, 让这个缺口在 Phase B 交付时机械可查而非
    再次沉默通过八轮审计。

---

## Finding 2 (MAJOR) — Rule #6 定档只套了判据表的通用第一行, 没有套 SOT 的 SKILL.md 专属附加约束

`standards/conventions/skill-benchmark-exemption.md:33` 逐字:

> 「**SKILL.md 有变动时的附加约束**(承前): 仅当变动是**事实性同步**(溯源注释 / 行号勘正 /
> 术语修正)且 frontmatter `description` 零变动, 才可能落进第一行; 须在 spec 里逐行点名该
> 变动并声明非指令语义变更。`description` 或指令流程变动 ⇒ 一律第二行。」

这是比 §2 判据表通用第一行("描述性(schema / 字段 / 命令语法 / 溯源注释 / 行号勘正)")
**更窄**的专属约束, 专门管 SKILL.md 文件本身的改动, 用括号内三项(溯源注释/行号勘正/
术语修正)**穷举**了"事实性同步"的范围。

Spec A 的 `rule6_note`(proposal.md:191-201)只写:

> 「按 `standards/conventions/skill-benchmark-exemption.md` 判据表**第一行**
> (描述性 / schema / 字段) ⇒ substitute」

即只援引了 §2 通用表, **完全没有对照 `:33` 这条 SKILL.md 专属约束逐条核对**。而 Spec A
对 SKILL.md 的两处改动 (proposal.md:224-226):
- `:267 schema 增 gate_error` —— 新增一个此前不存在的输出键, 记录一个**新增能力**,
  不是修正既有文本的溯源/行号/术语, 字面上不落在"事实性同步"三项穷举内;
- `:279 四类早退注记同步` —— 为容纳本 Spec 新增的第五种早退分支而**改写**既有归纳句,
  同样是为反映新行为而改文档, 不是单纯勘正既有陈述的错误。

两处都更接近"为新增行为写新文档", 而不是`:33`定义的"事实性同步"。按`:33`最后一句
"description 或指令流程变动 ⇒ 一律第二行"的 fail-closed 精神(结合 §2 表格第 4 行
"拿不准 ⇒ 照跑"), 这两处改动的定档结论**不能只靠援引 §2 通用表就下, 需要显式核对
`:33` 三项穷举并给出逐条不落入/落入的判断**, 而 Spec A 当前完全没有做这一步。

**怎么会红**: 若 Phase B 执行者照抄 Spec A 现有 `rule6_note` 直接跳过 AB, 而 knowledge-manager
或 tech-lead 在发版审计时逐字核对 `:33`, 会发现"新增 schema 键"不在"溯源注释/行号勘正/
术语修正"三项枚举内, 判定应照跑 AB —— 与 Spec A 已下的结论相反, 届时需要补跑 AB 或论证
豁免, 造成返工。

**处置建议**: 在 A.2 阶段把 `rule6_note` 改为显式核对 `:33` 三项穷举, 对 `:267`/`:279`
各给一句"落入/不落入 X 项, 理由 Y"的判断; 若结论是"不落入三项穷举但仍判第一行", 需要
额外论证为什么 fail-closed 的字面约束在此处不适用, 而不是只引用更宽的 §2 通用表。

---

## 本轮已核验属实的项目 (供交叉参考, 不构成 finding)

以下 Spec A 关键事实性断言经本轮独立实读/实跑复核, 全部准确, 记录如下以示审计范围与
"划界"问题(Finding 1)不是因为其余材料不可靠:

| 断言 | 复核方式 | 结果 |
|---|---|---|
| 五个插入点行锚 `:328/:338/:344/:345/:356/:357/:358/:366` | `Read pre_merge_gate.py` 全文逐行核对 | ✅ 全部逐字命中, 顺序正确 |
| `SKILL.md:255/:259/:260/:267/:279` 引文 | `Read SKILL.md:240-329` 逐字核对 | ✅ 全部逐字命中 |
| `gate_error` 全仓零消费者 | `grep -rn "gate_error" aria/` | ✅ 零命中(退出码1) |
| `path_coverage.py:93` 异常元组 `(TimeoutExpired, FileNotFoundError, OSError)` | `Read path_coverage.py:78-94` | ✅ 逐字命中 |
| `aether.py:38` `RETRY_BACKOFF=(5,15,45)` / `MAX_RETRY_ATTEMPTS=len(...)=3` | `Read aether.py:36-39` | ✅ 逐字命中 |
| `_run_with_retry`(`:164-187`)硬绑 `[self.binary]` / 只捕 `TimeoutExpired` / 无 `cwd` 参数 / `text=True` | `Read aether.py:164-187` | ✅ 全部属实, 签名确无 `cwd`, `:174` 硬绑 `self.binary`, `:180` 只 `except TimeoutExpired`, `:176` `text=True` |
| `test_ci_backends.py` 25 tests 零命中 `_run_with_retry` | `grep -c` 两条命令实跑 | ✅ `_run_with_retry`=0, `def test_`=25 |
| `test_sc22`(`:710`)全局 patch + `:723` 未传 `main_branch` | `Read test_pre_merge_gate.py:705-730` | ✅ `mock.patch.object(pc_module.subprocess, "run", …)` 确为模块级共享对象打桩; `:723` 确 `gate_check(pr_branch="feat/x")` |
| 既有 24 处 `gate_check(` 调用零改动(为 `remote` 新增默认参数) | `grep -c 'gate_check('` + 抽样 10 处调用风格 | ✅ 24 处, 抽样全部 keyword 调用风格, 追加带默认值的新参数不影响任何一处 |
| 测试基线 111 passed | `python3 -m pytest tests/ -q` 实跑 | ✅ `111 passed in 1.10s` |
| `gate_check()` 六键 `_build_output` 结构 + `path_coverage` additive 先例 | `Read pre_merge_gate.py:232-263` | ✅ 结构确认, `gate_error` 追加同一模式风险低 |

---

## 总评

Spec A 在**事实颗粒度**上的打磨质量延续了八轮审计的高水准 —— 本轮抽查的十余条 file:line
与计数全部准确。**但 Finding 1 指出的是更上一层的问题: 划界本身依赖的核心断言("存在性
核验单独关掉恒绿腿")在 AI 真实执行的代码路径上不成立**, 而这条反例信息**已经存在于
本项目自己四轮之前的审计记录里**(post_spec-R3/R4 tech-lead), 拆分时未被带过来核对。
这直接命中 audit 任务书要求核查的判据: "存在性核验单独就关掉了恒绿腿"——**这个声称不成立**。
按 Rule #10 的精神, 这类已被本项目自己确认过的结构性事实不应在新 Spec 里静默丢失,
应作为 Critical 上报并要求 A.2 前处置。
