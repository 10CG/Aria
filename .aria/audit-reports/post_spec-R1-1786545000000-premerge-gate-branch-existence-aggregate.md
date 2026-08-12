---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-12T14:35:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_spec R1 汇总 — Spec A `premerge-gate-branch-existence`

> 被审对象 = 由 [DEC-20260812-001](../../docs/decisions/DEC-20260812-001-premerge-gate-spec-split.md)
> 拆出的 A 侧 (Level 2, MINOR)。**这是拆分后 A 的第一轮, `max_rounds` 从 4 重新起算。**

## 投票

| 席位 | VOTE | VERDICT | C+M+m | 阻塞 B |
|---|---|---|---|---|
| code-reviewer | REVISE | PASS_WITH_WARNINGS | 0+6+3 = 9 | 2 |
| tech-lead | REVISE | FAIL | 1+4+2 = 7 | 5 |
| knowledge-manager | REVISE | FAIL | 2+2+1 = 5 | 4 |
| qa-engineer | REVISE | FAIL | 2+1+0 = 3 | 2 |
| backend-architect | REVISE | FAIL | 1+1+0 = 2 | 1 |

**5 REVISE / 0 PASS** · verdict **FAIL** · `converged: false`。
原始 **6C + 14M + 6m = 26** · **14 条 `blocks_phase_b`**。

## 🔴 承重发现: 划界的核心论证有洞 (四席独立命中)

**A 的承重句「存在性核验单独就关掉恒绿腿」只在 `gate_check()` 层成立, 在执行路径层不成立。**

实测三条:

| 证据 | 实测 |
|---|---|
| `SKILL.md:243` 逐字 | `aether ci status --branch main --in-flight --json` —— **分支名硬编码**, 且这是 **§C.2.4 执行流程的编号步骤本体** |
| 本仓 `git ls-remote --heads origin main` | **零行 + RC=0** ⇒ **那条命令今日就是恒绿腿的活体** |
| `workflow-runner/SKILL.md` grep `pre_merge_gate.py` | **零命中**; 唯一表述是 `:329`/`:351`「re-invoke: phase-c-integrator C.2.4」⇒ **编排层把执行交回散文流程** |

**根因 (编排层第 10 条错误, 主 loop 自陈)**:
DEC §3 与 Spec A §Why 都只引了 B 侧的 **§症状** (后端不可区分性),
**没引紧邻的 §根因** ——「同一算法有两份实现, 而 **AI 走的是没被加固的那份**」。
⇒ **存在性核验修的是 helper 那份; 而 AI 实际走的是散文那份。**

⚠️ 但**拆分方向本身仍成立** —— 多席明确: 「拆分对」「A 是真实、必要、可独立以 MINOR 交付的增量」
(tech-lead 逐条回源 11/11 命中, 两个受控裸仓实验全部复现)。
**错的不是拆, 是 A 的完成定义与声称。**

⇒ **处方**: A 必须补**残余暴露声明** ——「A 落地后散文裸命令路径仍恒绿, 直到 B 侧 D1 收敛两份实现;
**A ship 不构成 #137 闭环, 不得据此 close #137**」。B 侧抬头逐字称 A 承接「关掉恒绿腿所需的**全部**内容」, 该句同须更正。

## 🔴 第二条 Critical: Rule #6 定档错误 (亦为主 loop 所写)

A 判**第一行** (描述性 ⇒ substitute SC) 并提名 SC-A6 / A13 / A-zero 作 substitute。**三处不成立**:

1. **substitute 对它声称替代的对象恒绿** —— 三条断言的全是 `gate_check()` 返回的 dict
   (`verdict` / `gate_error.kind` / `raw_message`), **无一条读 `SKILL.md`**
   ⇒ 单独回退 `:267`/`:279` 两个 hunk、保留 `.py` 改动, **三条仍全绿**
   ⇒ 不满足 SOT `:26` 的 baseline-failing 定义;
2. **A 自引的先例反向** —— `aria/CHANGELOG.md` v1.65.0 段逐字「Rule #6 **照跑 AB**
   (3 eval × with/old/without 三臂)」, 而 v1.65.0 与 A 是**同形改动** (往 `gate_check` 中间插新步
   + 加 additive 可选输出键 + 同步 schema/早退注记), 其落地实测**给 SKILL.md 执行流程加了编号步骤 2.5**;
3. **文内三处不可能同时为真** —— `:196` 主张第一行 (substitute = AB 豁免通道) ×
   `:201` 逐字「本 Spec 不申请任何豁免」× `:39` 逐字把「Rule #6 AB」整体划归 B 侧。
   而 Rule #6 触发点是**本 change 自己的发版**, A 按 MINOR 独立发版 ⇒ **AB 义务结构上无法转移**
   给一个至今「不具备进 Phase B 条件」的姊妹 Spec。

⇒ SOT `:33` 第四行逐字「**拿不准 ⇒ 照跑 (宁跑勿豁)**」。

## 三条 Major (择要)

- **§3 自称「唯一合法插入点」但 12 条 SC 无一钉住它** —— A 对三个早退用了
  「`assert ls-remote 未被调用`」的因果断言, 对 `evaluate_path_coverage` 这条**同族**顺序约束**零断言**
  ⇒ 把核验插在 `:358` 之后的实现 **12/12 全绿**而 §3 被违反。
  **认出了类只推广了一半** (memory `fix-the-class` 同形 —— 讽刺的是 A 自己 `:179` 就写着
  「兄弟早退不同步则该类只修了一个实例」)。
- **`--remote` 的 CLI 接线零 SC 覆盖** —— 实跑 `grep -n "main(argv" tests/` **零命中**
  (CLI 入口今日无任何测试), 12 条 SC 全走 Python 层 ⇒ 只加 `add_argument` 而漏
  `:435` 的 `remote=args.remote`, 该 flag **静默 no-op 且 12/12 全绿**。
- **「既有 24 处调用零改动」漏计第 25 处** —— 实跑: `tests/test_pre_merge_gate.py` 24 处 +
  `pre_merge_gate.py:435` 的 `main()` 内真实调用 = **25**, 而 `:435` **恰是 `--remote` 唯一的落地点**。

## 两条 A 声称里没想到的破坏面 (backend-architect)

- **行为兼容面未评估**: 凡沿用 `--main-branch` 默认值 `"main"` 的下游 (本仓 origin **实测无 main**;
  `test_sc22:723` 即如此调) 会**从 green 翻为 fail**。§Impact 逐字「零破坏面」**只覆盖了 API 形状,
  未覆盖运行时翻转**, 也无迁移说明;
- **`:6`「无跨仓同步面」被 `:229`「发版同步面: MINOR, 走常规发版流程」自我推翻** ——
  代码落 `aria` 子模块、Spec 落主仓, ship MINOR 必然触发 CLAUDE.md 逐字的
  「子模块 5 文件 + 主仓 gitlink + VERSION + badge + i18n」, 而 **Level 2 无 tasks.md 承载该清单**。

## 一条正向

**A 的事实层面经受住了复核** —— tech-lead 逐条回源 **11/11 命中**;
两个受控裸仓实验 (裸名 glob 命中 RC=0 / 锚定含元字符仍命中 / **零命中 rc=0** / **`--exit-code` rc=2** /
坏 remote RC=128) **全部复现**; 八个插入点行锚逐行实读全部命中;
`SC-A*` 前缀无冲突已实跑核实 (既有为 SC-1/2/4/9/11/14/18/19/22/23/27, 无 `SC-A*`);
SC-A13 的判别力经实验证明有效。

⇒ **问题不在承自八轮的那些事实, 在我为拆分新写的那几句声称。**

## 处置

`max_rounds` = 4 (从 A 重新起算), 已用 **1**。R1-fix 后续 R2。

**A 侧的 Phase B 仍被本闸门阻断** (14 条 `blocks_phase_b`, 含 6 条 Critical)。Rule #10: AI 不得自行豁免。

### R1-fix 的方向 (不是重写, 是补声明与补 SC)

1. **补残余暴露声明** + 更正 B 侧抬头「关掉恒绿腿所需的**全部**内容」那句;
2. **Rule #6 改判第二行** (照跑 AB), 或给出真正 baseline-failing 的 substitute
   (须至少一条断言读 `SKILL.md`); 并消掉 `:196`/`:201`/`:39` 三处互斥;
3. §3 补「存在性核验判 fail 时 `assert evaluate_path_coverage 未被调用`」;
4. 补 CLI 层 SC (走 `main(argv)`), 并把「24 处」更正为 **25 处**且点名 `:435`;
5. 补**行为兼容面**评估与迁移说明 (从 green 翻 fail 的下游);
6. 消掉 `:6` 与 `:229` 关于跨仓同步面的自相矛盾。
