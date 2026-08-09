# 审计轨迹 — premerge-gate-mainbranch-failclosed

> **本文件是 append-only 审计史, 与 `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (收敛型交付面) 分居两文。**
> 依据: 2026-08-07 owner 对姊妹 Spec `linked-issue-normalization` 的裁定 —— append-only 叙事与收敛型交付面不能同居一文。R3 (tech-lead / knowledge-manager) 指出本 Spec 违背该先例, 本文件为处置结果。
>
> **四条不同步声明**: 本文件 (a) 只追加不重写; (b) 记录的是**当时**的判断, 可能已被后续轮次推翻; (c) 与 proposal.md 的当前内容**不保证一致** —— proposal.md 是唯一交付面 SOT; (d) 引用的行号是**记录时**的行号, 不随 proposal.md 演进更新。

---

## 汇总

| 轮 | 席位 | vote | 去重 C+M+m | Major | 本轮 fix 引入 (Major) | cut_too_much | converged |
|---|---|---|---|---|---|---|---|
| R1 | 5 | 5/5 REVISE | 5+10+6 = 21 | 10 | — | — | false |
| R2 | 5 | 5/5 REVISE | 3+15+8 = 26 | 15 ↑ | **100%** | — | false |
| R3 | 5 | 4 REVISE / 1 PASS | 3+10+9 = 22 | 10 ↓ | 9/10 | **41%** | false |

配置: `audit.enabled=true` · `checkpoints.post_spec=convergence` · `max_rounds=4` · 5 席 (`audit.teams.post_spec`) · `max_parallel_agents=2` (2+2+1 分批) · `drift_guard` 配置块不存在 ⇒ `convergence_mode` 默认 false ⇒ drift-checker 未启用 (配置默认, 非 AI 裁量)。三轮均零 spawn 失败 / 零超时 ⇒ `incomplete: false`。

逐轮汇总报告 (同目录):
- `post_spec-R1-1786216818583-premerge-gate-mainbranch-failclosed-aggregate.md`
- `post_spec-R2-1786220900000-premerge-gate-mainbranch-failclosed-aggregate.md`
- `post_spec-R3-1786223900000-premerge-gate-mainbranch-failclosed-aggregate.md`

十五份席位原始报告: `post_spec-R{1,2,3}-*-premerge-gate-mainbranch-failclosed-{role}.md`。

---

## 三轮的实质产出: 范围前提被推翻

**R3/TC1 (2 席独立命中 + 编排层实跑复现)** 是本次审计最重要的产出, 它推翻了 R1/R2/R3 三个版本**共同的**范围前提:

```
SKILL.md 提到 pre_merge_gate.py 只有 :262 一处 —— 「Helper 实现: ...」, 从无带参调用示范。
而 C.2.4 那一段的标题逐字是「执行流程」, 步骤 1-5 是逐条裸命令, 步骤 3 逐字:
    aether ci status --branch main --in-flight --json

编排层实跑占位符版本:
    $ aether ci status --branch '<main-branch>' --in-flight --json
    {"status":"ok","data":{"filters":{"branch":"<main-branch>",...},"runs":[]}}   RC=0
```

| 症状 | Rule #8 那条腿恒绿 |
|---|---|
| 病因 (a) | helper 缺省 `main` — **#137 报的是它, 前三个版本全都只治它** |
| 病因 (b) | `SKILL.md:243` 裸命令字面量 — AI 照抄时 **helper 根本不参与** |

**根因 (R3 后确认)**: 同一个算法有**两份实现** —— SKILL.md 的散文流程 + `gate_check()`。编排层实测 `gate_check` 完整实现全部 5 步; 而 AI 走的是散文那份。所有加固都做在 helper 那份上, 因此对真实执行路径无效。

⇒ R2-fix 砍掉的**存在性核验**是唯一对两条路径都有效的拦截物 (它作用在「实际被查询的分支名」上, 与该名字如何得来无关) —— `cut_too_much` 字段抓到的正是它。

---

## 逐轮要点

### R1 (5/5 REVISE, FAIL, 21 条)

5 Critical: `verdict="error"` 使 fail-OPEN 从消费侧复发 · 只改 `:242` 留下 `:243` · 「既有用例逐字不改」证伪 (24/24 依赖旧缺省) · `main_branch` 双消费者致 (a) 腿行为变化 · `<remote>` 全篇未绑定。

### R2 (5/5 REVISE, FAIL, 26 条, Major 10→15)

R1-fix 采用「结构性重写」(owner 裁定)。结果: **Major 净增 5, 且 100% 由 fix 新造**。

3 Critical: `ls-remote --exit-code --heads <裸分支名>` 是**尾段 glob** ⇒ 远端只有 `refs/heads/wip/master` 时判「master 存在」(编排层受控仓复现, 锚定 `refs/heads/master` 得 RC=2) · `ls-remote --symref` 存在 **RC=0 但无 `ref:` 行**两态 (unborn / detached, 编排层复现) · Rule #6 归档依据证伪。

**四元组收敛比较在本轮失效**: 两轮共有 key = 0, 因结构性重写换掉了全部 scope 字符串。⇒ 收敛算法测的是「同一批结论是否稳定」, 而重写换掉了结论的载体。真正起作用的是 R2 才引入的 `introduced_by_r1fix` 字段。

### R3 (4 REVISE / 1 PASS, FAIL, 22 条, Major 15→10)

R2-fix 采用「大幅减法」(owner 裁定)。Major 由升转降, 出现整场首张 PASS 票 (backend-architect), 但 **`cut_too_much` = 41%, 3 条 Critical 里 2 条属之**。

3 Critical: TC1 (见上) · TC2 Rule #6 定档 · TC3 SC-M4 两种自然 grep 实现都失效。

---

## Rule #6 定档的三次摆动 (方法论教训)

| 版本 | 结论 | 依据 | 结果 |
|---|---|---|---|
| R1-fix | 照跑 AB | 「存在专属 AB 套件 (7 fixtures)」 | 依据浅 —— 只核了套件存在, 未核它能否测量该行为 |
| R2-fix | 第三行 (套件覆盖外) | 套件 0 prompt/0 双臂 + 历史记录自证 `structural_verification` + 「C.2.4 零命中」 | **实证方向错**: grep 只扫 prompt 未扫答卷; 且 mis-citation (`benchmark.md:173` 的确切条件是 multi-PR concurrent CI 不可测) |
| R3 后 | **第二行「照跑 AB, 零裁量」** | SOT 附加约束段: **「`description` 或指令流程变动 ⇒ 一律第二行」** —— **直接管辖条款** | 定档 |

**教训**: 判据表里存在 dispositive 的成文规则时, **先读规则, 再考虑实证**。实证路径有更多出错处 —— 本例两次实证方向相反地都错了, 而 SOT 那一句从第一次就足以定档。与既有 `exact-exception-condition` (援引成文豁免须逐字核对确切触发条件) 同族, 但形状不同: 那条是引错了条件, 这条是**根本没去读条件就自己动手测**。

另: SOT 强制要求「无论走哪一行都要在 spec/tasks 留 `rule6_note`」, R1/R2 两版均缺失。

---

## 编排层 (AI) 自身错误留痕

| # | 错误 | 性质 | 处置 |
|---|---|---|---|
| 1 | Rule #6 定档两次都错且方向相反 | 有 dispositive 成文规则时绕开规则去实证 | 已更正为第二行; owner 两次裁定的前提均由我提供且均被推翻 |
| 2 | 把席位报对的行号「修正」成错的 (`_ProbeCacheResetMixin` `:59-80` → `:59-88`) | 用了比对方更差的启发式 (以「下一个 class 行号」为边界, 把中间注释块算入) | 已更正回 `:59-80` |
| 3 | `cut -c1-150` 截断致误判 `SKILL.md:242` 引用有误 | 读取方式导致的假阳 | 已在流入 Spec 前自我推翻 |
| 4 | 受控实验脚本漏 `git init --bare`, 差点把脚本错误当证据 | 实验设计错误 | 已重跑更正 |
| 5 | SC-M4 声称「实测 3/3」用的是**未写进 SC 的复合 grep 模式** | 自陈与交付物不符 | R3/TC3 抓出; 新版改为逐条列出**字面 grep 模式与期望计数** |
| 6 | R3 汇总报告首次写盘失败 (cwd 被受控实验带跑) | 回执不等于落盘 | 同命令内 `ls` 计数抓到, 已重写并独立核验 |
| 7 | R1-fix 引入 23 条新缺陷 (Major 100% 新造); R2-fix 砍掉承重件 (`cut_too_much` 41%) | fix 环节质量 | 见 R2/R3 汇总 |

**R1 五席只漏了 1 条 Critical** (R2/RC1 的尾段 glob) —— 审计环节质量不是瓶颈, fix 环节是。

---

## owner 裁定记录

| 时点 | 裁定 | 依据 |
|---|---|---|
| R1 后 | R1-fix 用**结构性重写**而非逐条补丁 | 上一个 Spec 四轮实测逐条补丁 fix 引入占比 80%+ |
| R1 后 | Rule #6 改判**照跑 AB** | 编排层提供的「AB 套件存在」—— **前提后被证伪** |
| R2 后 | 停止「审计→重写」循环, 改**大幅减法 + spike-first** | major 10→15 上升 + fix 引入占 major 100%, 两条成文判据同时点亮 |
| R2 后 | Rule #6 改判**第三行** | 编排层提供的套件结构实证 —— **前提后被证伪** |
| R3 前 | 跑 R3 (减法版仍须过闸门) | — |
| R3 后 | **重定范围: 改治 SKILL.md 层** | R3/TC1 推翻三版共同的范围前提 |

**闸门状态**: post_spec `max_rounds=4`, 已用 3 轮, `converged: false`。范围重定后的版本是新的被审对象。
