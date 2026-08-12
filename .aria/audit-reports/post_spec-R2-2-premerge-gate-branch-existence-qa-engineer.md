---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T15:42:27.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — Spec A `premerge-gate-branch-existence` — qa-engineer

角度: SC 可证伪性 (16 条红窗是否真实存在 / 有无恒红恒绿空真 / 打桩边界自洽 / 三条负控早退能否真拒绝坏实现)。

## 0. 方法

对 R1-fix (commit `e165df4`) 的每条自称逐字核实 + 独立实跑; 对全部 16 条 SC (不是任务书写的"12 条" —— R1-fix 新增 4 条, 12→16, 已核实计数法) 做 mutant 级复核: 为每条设想至少一个"像样的坏实现", 判断该 SC 是否真的会转红。凡本节给出命令输出的, 均本轮独立复跑 (非引用 R1 或 commit message 的转述)。

## 1. C-1 (划界承重句) —— 判定: **真闭合, 非纸面修复**

三处交叉核验, 全部命中且日期一致 (2026-08-12):

- Spec A `§根因` (`:35-39`) 逐字补引「同一算法有两份实现, AI 走的是没被加固的那份」+ 承重句加「`gate_check()` 这份实现里的」限定 (`:43`) + 新增 `§残余暴露` 整节 (`:73-94`)。
- B 侧 `proposal.md` 抬头 (`:11-18`) 独立核实: 已加**带日期的更正块**, 逐字撤回「关掉恒绿腿所需的**全部**内容」, 改述为「关掉 `gate_check()` 那份实现里的恒绿腿」。
- `DEC-20260812-001` (`:80-102`) 独立核实: 同样加了带日期的更正块, **owner 原文逐字保留在上**, 只追加限定, 不改写裁定原文 —— 这是正确的裁决记录纪律 (不擅自篡改 owner 已签发的文本)。

`git ls-remote --heads origin main` 本轮独立复跑: **零行 + RC=0**(与 Spec 声称一致)。`SKILL.md:243` 独立 grep 确认逐字硬编码 `aether ci status --branch main --in-flight --json` 且落在 §C.2.4 执行流程编号步骤 3 本体 (非注释/折叠块)。

**判「写下来」还是「闭合」的判据**: C-1 的本质是"划界承重句的可信度"(一个**范围声称**是否准确), 不是"代码缺了一块行为"。对声称类 Critical, 正确的闭合形式就是把声称改准 + 如实标注残余, 而不是发明假机械信号去掩盖散文路径测不到的事实 (`§残余暴露` 明确拒绝为此编造 SC, 理由成立: 没有 harness 能"执行 SKILL.md 散文")。三文档一致、无自相矛盾、无回避 —— 判定**真闭合**。

## 2. C-2 (Rule #6 定档) —— 判定: **改判正确, SOT 引用现已精确**

逐字核对 SOT (`standards/conventions/skill-benchmark-exemption.md`, 本轮独立 `grep -n`):

| Spec A 引用 | SOT 实际行 (本轮复核) | 结论 |
|---|---|---|
| `:28` "deterministic substitute...SC 级 baseline-failing" | `:28` 逐字命中 | ✅ 精确 |
| `:31` "拿不准 ⇒ 照跑 (宁跑勿豁)" | `:31` 逐字命中 | ✅ 精确 |
| `:33` "`description` 或指令流程变动 ⇒ 一律第二行" | `:33` 逐字命中 | ✅ 精确 |

R1 aggregate 原引用 `:26`(实为表头行) 与 `:33`(实为 SKILL.md 附加约束, 非"拿不准"那句) —— **R1-fix 指出的引用错误属实**, 现已订正到位。

`aria/CHANGELOG.md` v1.65.0 段本轮独立 grep 确认逐字「Rule #6 照跑 AB (3 eval × with/old/without 三臂...)」且该版确实同批给 `SKILL.md` 加了编号步骤 2.5 (`SKILL.md:242` 本轮独立核实命中)。三处互斥 (`:196`/`:201`/`:39` 原文) 现已消除 —— proposal.md 现文只有一处定档声明 (`§Rule #6` 逐字"第二行, 零裁量, 不申请任何豁免"), 与 §Why 的 ⛔ 清单("B 侧自己的 Rule #6 AB")一致。**改判成立, 依据充分。**

## 3. 两条「新发现」—— 均本轮独立复跑验证为真

**UnicodeDecodeError**: `python3 -c "print(issubclass(UnicodeDecodeError, OSError))"` → `False` (本轮复跑确认); 进一步用真实 subprocess 验证 `text=True` 会使其**裸抛**而非被 `(TimeoutExpired, FileNotFoundError, OSError)` 三合一 except 捕获 (本轮构造含非法 UTF-8 字节的子进程输出, 确认 `UnicodeDecodeError` 穿过该 except 元组)。§5/SC-A14 的处置(显式点名 + 参数化探针, 不规定具体修法)判定合理充分。

**SC-A11 打桩退化恒真**: 若把核验入口本身打桩为"返回 found", 则该 SC 不再测"真实 ls-remote 对已存在分支的判定", 而是测"mock 返回值被正确透传"——这是恒真陷阱, 判定成立。现文打桩边界表已把 SC-A11 列入"真实 ls-remote + 受控裸仓 (不得打桩)"档并附限制说明, 修法正确。

## 4. R1 aggregate 的两条"元错误" —— 均本轮独立回源验证为真

**归属错误**: 独立读取原始 journal (`wf_d165b8cd-ed6/journal.jsonl`) 的 `additive_claim` 字段核实 ——「行为兼容面未评估」与「`:6` 与 `:229` 自相矛盾」两条**逐字出自 tech-lead 的 `additive_claim` 字段**, 不在 backend-architect 的 `additive_claim`(该字段只讨论 additive/MINOR 的技术层面, 未提这两点) —— R1 aggregate `## 两条 A 声称里没想到的破坏面 (backend-architect)` 一节标题误署, 属实。

**未去重**: 独立统计 journal 中 5 席原始 findings —— 6 条 Critical 实际映射到 **2 个不同论点** (划界承重句 ×3 席、Rule#6 substitute ×3 席); 14 条 Major 中至少「CLI --remote 零 SC 覆盖」被 tech-lead / code-reviewer / knowledge-manager **三席**各报一次、「Rule#6 落第一行」被 code-reviewer / backend-architect **两席**各报一次、「Level2/无跨仓同步面矛盾」被 tech-lead / knowledge-manager 两席各报一次 —— 去重后确实明显少于 6C+14M 的表面数字, R1-fix "约 2C+10M" 的估计量级合理 (未做逐条精确核账, 但方向与幅度经本轮独立统计验证站得住)。

## 5. SC 集合可证伪性审计 (16 条全覆盖)

逐条 mutant 检验 (真实裸仓实验见下), 结论: **16 条中 15 条红窗真实、边界自洽、无恒红恒绿空真**; **1 条新发现的覆盖缺口** (见 Finding QA-M1)。

关键实证 (本轮独立复跑, 非转述):

- `git ls-remote --heads /tmp/does-not-exist-repo-xyz master` → `rc=128` (SC-A7 的"确定性 128"声称验真);
- 受控裸仓仅含 `refs/heads/wip/master`: `git ls-remote --heads <r> master` → 命中且 `rc=0` (SC-A6 场景, glob 尾段匹配验真); `--exit-code` 同场景仍 `rc=0`(验证"两条都绿"这句的前提);
- 受控裸仓仅含 `master`: `mast*` / `m[a]ster`(含锚定 `refs/heads/` 前缀) / `maste?` 四种写法**全部** `rc=0` 且命中(SC-A13 anti-anchoring 声称验真);
- 受控裸仓仅含 `refs/heads/wip/master`(零 `master`/`develop`): `--exit-code` 查询 `develop` → `rc=2`; 不带 `--exit-code` → `rc=0` 零行输出(SC-A-zero 是唯一能捕获 `--exit-code` 误用这一声称, 逻辑与实测均验真);
- 主仓 `origin`→`10CG/Aria.git`(有 master), `aria` 子模块 `origin`→`10CG/aria-plugin.git`(有 master) ——两个不同仓、两边都有 `master`, SC-A-cwd 的现实落点验真;
- `pre_merge_gate.py:435` (`main()` 内唯一真实调用) 未传 `main_branch`/`remote`, 测试文件 24 处 `gate.gate_check(` 逐一 grep 确认无一传 `main_branch=`(唯一命中的 `main_branch=` 字符串在 `:669` 是断言参数, 非调用参数) —— "24 处零改动漏计第 25 处"及"25 处全部落默认值"两条声称均验真。

**三条负控早退 (SC-A10/A10b/A10c) 是否真拒绝坏实现**: 用位置 mutant 检验 —— 若把核验错放在 `:328`(enabled 检查)与 `:338`(backend-None 检查)之间, SC-A10b(backend-None 早退场景)会在该分支实际调用核验入口, 触发 `assert ls-remote 未被调用` 失败 → 红; 若错放在 `:338` 与 `:345`(precheck 检查)之间, SC-A10c 同理会红。三条负控**逐一钉住自己那个早退之前的位置**, 组合起来能拒绝"核验放在任一早退之前"的全部错误位置 —— 不是摆设。

**打桩边界表自洽性**: 16 行 SC 与边界表 6 类目逐一核对(真实 ls-remote 6 条 / 两种手段皆可 1 条 / 必须 mock 2 条 / mixin 打桩 4 条 / 纯文件读取 1 条 / 元断言 2 条 = 16), 无遗漏无重复, 且每条的分类与其"怎么会红"列描述的验证机制一致, 无矛盾。

## 6. Finding QA-M1 (Major, 新发现, `introduced_by_r1fix=false`)

**16 条 SC 无一验证"存在性核验必须独立于 `path_coverage_enabled` 运行"** —— 一个把核验错误嵌套进 `if cfg.get("path_coverage_enabled", True):` 代码块内部的实现(即误当成"path coverage 评估的一部分"而非独立步骤), 会在 **全部 16 条 SC** 默认配置(`path_coverage_enabled` 未显式设为 `False`)下与正确实现**行为完全不可区分**, 16/16 全绿。

这与 SC-A-order 修复的缺口是**同一个类的另一个维度**: SC-A-order 钉住了"核验必须在 `evaluate_path_coverage` **之前**"(顺序轴), 但没有任何 SC 钉住"核验必须**不受 `path_coverage_enabled` 门控**"(条件轴) —— 该 Spec 自己在 `:191` 引用 memory `fix-the-class`("认出了类只推广了一半")描述的正是这个模式, 而它自己在补 SC-A-order 时, 对同一插入点风险的另一维度留了同形空当。全文 grep `path_coverage_enabled` 只出现在行锚图(`:180`)与 §6 既有 mixin 讨论(`:278`)两处, 16 条 SC 表无一提及。

**怎么会红**: 补一条 SC(可并入 SC-A6 的变体, 或独立编号), 用受控裸仓(分支确实不存在)+ `config={"path_coverage_enabled": False}`, 断言仍 `verdict=fail` + `kind=="main-branch-not-found"`。今日(Spec 落地前)必然 `—`(功能不存在); 落地后, 把核验错误嵌进 `path_coverage_enabled` 门控块内的实现, 在此配置下核验被跳过 → 不产生 `fail` → 该 SC 转红。

严重度评级为 Major(非 Critical): 属于**新发现的覆盖缺口**, 不是已声称行为的失效; 且 §3 正面规定"唯一合法插入点"的散文表述本身足够清楚, 只是缺一条机械锚 —— 与 R1 中 SC-A-order 所处理的缺口同级(R1 当时也评为 Major, 非 Critical)。

## 7. 结论与投票

- R1 两条 Critical: **真闭合**(§1、§2), 非纸面修复;
- 两条新发现(UnicodeDecodeError / SC-A11 恒真风险): **均验证为真**, 修法充分(§3);
- R1 aggregate 的两条元错误(归属 / 未去重): **均验证为真**(§4), R1-fix 的自我更正诚实且有据;
- SC 集合本轮共发现 **1 条新 Major**(§6), 不影响 §1/§2 的 Critical 闭合判断, 但须在下一轮补上再进 Phase B;
- 未发现任何恒红 / 恒绿 / 空真的既有 SC(除已被 R1 自己识别并修复的 SC-A11 打桩边界外); 打桩边界表自洽, 三条负控早退具备真实拒绝坏实现的能力。

`0 Critical + 1 Major` ⇒ **verdict = PASS_WITH_WARNINGS**。

`vote = PASS`(相对上一轮): C-1/C-2 两条 Critical 真闭合, 新发现的 Major 不构成继续 REVISE 的理由(与 R1→R2 的既有工作量级不对称, 且是增量式"补一条 SC"而非结构性返工), 但记录在案供下一轮/Phase B 收口。
