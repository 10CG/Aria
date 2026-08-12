---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-12T00:20:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R3 汇总 — premerge-gate-mainbranch-failclosed

> 被审对象 = R2-fix 后的 A.2 产物 (`0dd26ce`)。本轮**首次把「机械交叉检查」这个处方本身送上审判席**。

## 投票

| 席位 | VOTE | VERDICT | C+M+m | 阻塞 B | 由 R2-fix 引入 |
|---|---|---|---|---|---|
| tech-lead | REVISE | FAIL | 1+6+3 = 10 | 6 | 8 |
| code-reviewer | REVISE | FAIL | 1+5+3 = 9 | 4 | 5 |
| qa-engineer | **PASS** | PASS_WITH_WARNINGS | 0+3+1 = 4 | 0 | 4 |
| knowledge-manager | REVISE | PASS_WITH_WARNINGS | 0+2+1 = 3 | 0 | 2 |
| backend-architect | REVISE | PASS_WITH_WARNINGS | 0+1+0 = 1 | 0 | 0 |

**4 REVISE / 1 PASS** · verdict **FAIL** · `converged: false` · 零 spawn 失败。
原始 **2C + 17M + 8m = 27** · **10 条 `blocks_phase_b`**。

## 🔴 决定性数据: 三种结构性干预, 三次都没收敛, 且最后一次让指标**回升**

| 轮次 | 干预手段 | fix 引入新缺陷占比 | Critical |
|---|---|---|---|
| post_spec R1–R5 (5 轮) | 原作者执笔 | **73–100%** | — |
| post_planning R1→R2 | **换人执笔** | **53%** ↓ | 3 → 1 ↓ |
| post_planning R2→R3 | 换人执笔 + **机械交叉检查** | **70%** ↑ | 1 → **2** ↑ |

原始条数 R1 52 → R2 30 → R3 27 (缓降), 但**去重后 Major 三轮持平**, 且
**fix 引入率与 Critical 双双回升**。

⇒ memory `feedback_stop_adding_rounds_when_major_count_flattens` 与
`feedback_audit_marginal_return_goes_negative` 的判据**同时且更强地成立**。

## 🔴 那道机械交叉检查被证伪 —— 维度错配

R3/tech-lead 在副本上做了 **5 个构造验其拒绝能力**, **4 个被放行**:

| 构造 | 结果 |
|---|---|
| T5 把护栏句换成「一律按 `:21/:300/:427` 三个行号逐字核」(**明令按行号核**) | **PASS** —— 因该句含「内容锚」三字 ⇒ CHECK3 验的是**词是否出现**, 不是性质 |
| T2 删掉 SC-M6 真 owner 的 verification | **PASS** —— CHECK2 把**作废/否定语境**的提及算作 owner |
| T6 把 TASK-017↔TASK-020 的边**反向** (先 bump 版本再执行 v2.0 删除) | **PASS** 并打印 ✓ —— CHECK1 判据 `n in ANC or tid in ANC` 是**无向**的 |
| T7 新造插入点冲突 (与 §6.1 相反) | **PASS** |
| T4 删掉护栏句 | FAIL ✅ (唯一真有拒绝能力的一项) |

**两处恒绿判据**: CHECK4 前半段只 print 六个插入点的提及次数、**零断言**;
后半段 9 条硬编码字符串存在性检查全部抄自**产生它的那次 fix 刚写下的句子** ⇒ 相对于该 fix 是**重言式**。

**它自己就是「只修实例不修类」的产物**: CHECK4 硬编码 `### 6.1` 等本 Spec 专属串;
CHECK2 的 TESTISH 元组里塞了 `收口实跑输出` 这个**为放行 TASK-021 一个任务而加的字面量**。
同族缺席至少三项: `task_group ↔ DAG 方向一致性` (本轮 7 处倒置全漏检) ·
`deliverables ⊆ scope_repos.paths` · `SC 表「今日实测」列是否回源` (本轮那条假值四项判据无一能碰)。

**根因** (席位逐字): 它是**无向存在性**检查, 而 R2 两个形状的失效是**方向性**与**类推广性**的
—— memory `feedback_invariant_dimension_must_match_error_dimension` 逐字预言了这个结果。

> ⚠️ **编排层自陈**: 主 loop 曾声称「已验其拒绝能力」。那个验证**不充分** ——
> 我用的两个 fixture (删依赖边 / 删护栏句) 恰好只打在它覆盖得住的「有没有」维度上,
> 而缺陷活在方向性维度。**我用一个无向的 fixture 去"证实"它能防方向性错误。**
> 这是本 session 第三次同形 (前两次: `set -e` 使实验恒真 · 抽冗余边当对抗 fixture)。

## 两条 Critical

1. **`TASK-014` 第三次换的验收量结构上不可满足** —— 「`:262`/`:559` 两处路径表达式**逐字**
   == 同一个定稿形态 F」, 而实读两处尾段是**两个不同脚本名** (`pre_merge_gate.py` / `submodule_gate.sh`)
   ⇒ 不可能同时逐字等于同一个 F。且 F 的类型是「多候选探测**结构**」, 写不进一行 markdown。
   ⚠️ 该任务自己的 notes 逐字写着「这是第三次更换 —— 若第四次再来, 请优先怀疑『拿 grep 计数当验收』
   这个手段本身在此不适用」。**第四次已经来了。**
2. (code-reviewer 席位另一条 Critical, 见其报告)

## 三条事实错误 (R2-fix 新引入, 均实测)

- **§6.1 的承重理由与代码不符**: 实读 `_normalize_config` 在 `:111`/`:120` 就 `del`/`pop` 掉旧键,
  **两个 legacy key 的首个消费者是 `:325` 而非 `:337`/`:339`** ⇒ 在被钉死的插入点上,
  手边的 `cfg` **结构上不含旧键名**, 而条款只规定了位置、未规定「判定须读未归一化的原始 config」。
- **`SC-M16` 的「今日实测 = 1」是假的** —— 实跑 `grep -n -- '<MAIN_BRANCH>' SKILL.md` **零命中**
  ⇒ 今日值 0。SC 表抬头逐字「每条 grep 断言的 pattern 与今日计数均已实跑」, 本条**未实跑**。
- **`TASK-015` 的 blob-SHA 命令在主仓结构上不可执行** —— 实跑
  `git rev-parse HEAD:aria/skills/phase-c-integrator/SKILL.md` → `fatal ... but not in 'HEAD'` rc=128
  (aria 是 gitlink, superproject tree 无其子路径)。**「求值时点」这一类在关闭该类的同一轮里原样复发。**

## 一条正向

**`TASK-021` (终局全量收口) 是本轮最扎实的修复** —— 席位实测其依赖闭包**真覆盖**全部改被测文件的任务
(五个面的改动者全在闭包内), 其后只剩 TASK-015/016/017 且无一触及被 SC 断言的文件。

## 轮次记录

| 轮 | vote | 原始 | 去重 | 阻塞 B | fix 引入 | converged |
|---|---|---|---|---|---|---|
| R1 | 4R/1P | 52 | 3C+12M+8m | 6 | — | false |
| R2 | 4R/1P | 30 | 1C+~13M | 12 | 53% | false |
| R3 | 4R/1P | **27** | 2C+~13M | **10** | **70%** | **false** |

`max_rounds` = 4, 已用 **3**。**只剩 1 轮。**

## 处置 — 已超出 AI 可自决范围, 须 owner 裁

三轮 post_planning + 五轮 post_spec = **八轮 40 席**, 期间试过**三种**结构性干预
(原作者执笔 → 换人执笔 → 换人执笔+机械检查), **无一收敛**, 且最后一种让指标回升。

**AI 不再自行发起 R4。** 理由:
- `max_rounds` 只剩 1 轮, 用掉它之后按 audit-engine 必须进入**降级策略**, 那是 owner 裁量;
- 把最后一轮花在**已被证伪的同形策略**上, 是可预见的浪费;
- 本轮已实证「结构性干预」这条路的边际产出为负 —— 继续需要的是**不同类的决定**, 不是又一轮。

**Phase B 仍被本闸门阻断** (10 条 `blocks_phase_b`, 含两条 Critical)。按 Rule #10 AI 不得自行豁免。

### 供 owner 参考的三个方向 (AI 不代裁)

1. **拆 Spec** —— 证据: 缺陷密度跟着范围扩张走 (R2 席位逐字「新引入缺陷高度集中在改动量最大的 TASK-020」);
   原始缺陷 (aria-plugin #137 那条恒绿腿) 可用**小时级**的最小改关掉, 其余 65h 的范围继续走审计;
2. **用掉 R4 + 接受降级** —— 按 `phase-c-integrator-ci-path-coverage` 的先例 (owner 2026-07-26 裁定
   「接受当前结论」+ `converged: false` 留痕);
3. **换判据** —— 本 Spec 已三次证明「拿 grep 计数当验收」在 D1 这个对象上不适用 (TASK-014 换了三次量),
   或许该换的是**验收手段的类别**而不是又一个量。
