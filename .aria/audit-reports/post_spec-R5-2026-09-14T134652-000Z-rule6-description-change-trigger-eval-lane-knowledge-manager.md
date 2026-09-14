---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-14T14:05:00.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [knowledge-manager]
---

# post_spec Round 5 — knowledge-manager 席

被审 SHA `f169a0b` (rework v5, 仓库 HEAD)。drift_guard 未配置 (`.aria/config.json` 无 `drift_guard` 键), 沿用 R4 判定 ⇒ `drift_check_skipped: true`。

## R4 对账

| # | R4 finding (本席) | 状态 v5 | 依据 |
|---|---|---|---|
| 1 | D2 转述 v5 自然措辞扩张短语漏「整理归档文档」, 与 RESULT.md v4 §v5 表 / 结论 2 不符 | **closed** | v5 proposal.md §D2 (第 48 行) 现列全四项「与相关文档 / 整理项目收尾材料 / 整理归档文档 / 收尾整理」, 并明确点出「其中『整理归档文档』直接带被测 skill 的领域词」; 逐字比对 RESULT.md v5 §v5 表第 55 行 (`原文 + 「与相关文档」「整理项目收尾材料」「整理归档文档」「收尾整理」`) 与 `v5-mildcreep-opus5/PREREGISTRATION.md` 第 9 行的 mildcreep 原文, 四项顺序与文字完全一致, 无遗漏、无新增。同批核对 proposal 另外三处转述该 v5 实验的位置 (§Why 第 2 条第 19 行 / §D6 第 101 行 / OQ-8 第 155 行) —— 三处均只用概括性措辞 ("一次自然措辞扩张实测不判红" / "轻微过宽 description 过门"), 不逐项列举短语, 不存在同类漏项风险 |

**closed 1 / partially 0 / open 0**。

## Findings

- [major] documentation/proposal.md §D6 (issue): D6 待写入 SOT §6 的新句仍引用『RESULT.md v4』, 但本轮 RESULT.md 已同批升至 v5 (头部/§Why/§D2/§D3/Impact/T8 六处均已同步为 v5); 头部「RESULT 再修订须同步重核」清单未列 §D6, 无 SC 兜底, 逐字落地会把过期版本号带进 SOT。
- [major] documentation/proposal.md §D1 (issue): D1 表 SOT §2 新句 (标注「定稿」) 末尾『(依 OQ-7 / OQ-9 裁定, 裁定不同则随之改)』, 逐字写入后 OQ 编号脱离本 proposal 语境即不可定位 (对比同一 SOT 文件 §6 现有「详见 issue #116」式永久引用); 无 SC 检查, 归档后成孤儿引用, 可能被误读为规则仍待裁未定。

## 观察

- **自主运行时 / 自主模式 / 交互模式 三词形仍未统一** (R4 观察延续, 未升级为 finding): SOT §2 新句用「自主运行时 (`state_scanner.coordination.unattended == true`)」(第 39 行), 与 CLAUDE.md 既有词「自主运行时 / 自主执行者」同形一致; §Impact (第 117 行) 同用「自主运行时」; 但 OQ-7 正文 (第 152-160 行) 仍用「交互模式 (v1.x)」「自主模式 (v2.0 Layer 2)」——CLAUDE.md 全文没有「交互模式」原形。三处均各自括注 v1.x / v2.0 Layer 2, 且 SOT 新句自带布尔条件内联定义, 不依赖术语本身即可读, 不致误读, 但 proposal 内部仍是两套字面。建议 Phase B 落地或后续同类 spec 统一复用「自主运行时」, 不再新造「XX 模式」变体。
- **CLAUDE.md 新句字节/行数预算复核**: 旧句 93 字节 → 新句 (含本轮新增「自主运行时的处置见 SOT §2」) 282 字节, 净增 189 字节; 代入模拟后 CLAUDE.md 总量约 13505 字节 / 151-152 行, 远低于 `claude-md-hygiene.md` §3 的 24000 字节 / 200 行双预算, 不触发 `claude-md-changelog-free`。新增末句词汇沿用 CLAUDE.md 已有的「自主运行时」, 不是「skill 设计内部术语」, 不违反 §2.4 第 3 条。但该末句本身是独立主谓句 (自成一个「。」收尾的句子), 与同段第 42 行 proposal 自身的表述「不在 CLAUDE.md 另加句子」字面有张力——实际是在同一张 D1 表格同一格内扩写既有替换目标, 未越出改动范围, 不算违规, 但建议该说明句改「不在 CLAUDE.md 另开新段/新条目」以避免自我矛盾的读感, 非阻断。
- **SOT §2 新句可读性**: 「自主运行时…在场景 4b 于其所用模型上验证之前, 不做 description 改动, 需要改时任务进 S_FAIL」句式较绕 (「其」指代「自主运行时」, 隔了一层定语才接主句), 但可解析、无指代歧义, 与全文一贯的高密度写作风格一致, 不构成阻断。
- **手册「边界与留痕」行**: 经比对本轮 diff, 该行 (D1 第三处) 与 v4 完全一致, 未再变动; 括号配对与「三条→四条」计数语此前已由 R4 验证通过, 本轮复核仍成立。
- **D5.6 新 issue 与 Aria#196 核实**: 「场景 4b 在 Layer 2 (GLM via Luxeno) 上的验证」用词风格与 CLAUDE.md 项目状态段「Layer 2 主力 LLM = glm-5.2 via Luxeno」一致。经 `forgejo GET /repos/10CG/Aria/issues/196` 核实: 标题「[契约][aria-orchestrator] unattended 的 Layer 1→2 env 传递三腿契约未定义 — 缺 import 会静默 fallback 到 false」, state `open`, 与 OQ-7「运行模式怎么判」段「该键从 Layer 1 传到 Layer 2 的契约未定义, 缺失时静默回落 `false`」逐字对应, 无引用漂移。
- **phase-a-planner 约定核实**: `aria/skills/phase-a-planner/SKILL.md` 第 131 行「不得以『AskUserQuestion 现在能不能用』做运行期推断 —— 有没有人可问是**配置事实**」与 OQ-7 引用的括注文字 (「有没有人可问是**配置事实**」) 逐字相符, `state_scanner.coordination.unattended` 键名两处一致, 无引用漂移。
- **OQ-7 自主栏 rework (非本席 R4 finding, 顺带核对)**: 已补 (B)/(C)/(D)/(E) 四选项各带代价, 「事实依据」已更正为「aria-runner-bot 是 AI 会话共用机器身份, handoff 中只与两个开发容器配对 (023236f2 23 份 / bfe8285d 7 份), 抽查两次发版都在开发容器交互会话 ⇒ AD10 流水线至今未改过 aria-plugin」, `aria-orchestrator/docs/architecture-decisions.md` §AD10 引用可定位; §Impact 补「按推荐, 验证完成前一律停在 S_FAIL」。这两条系 R4 tech-lead / code-reviewer 的 major, 不重复计入本轮比较键, 仅供聚合参考。
- **D6/RESULT.md 措辞修复核实 (非本席分内 finding)**: 「已验证判红的破坏有两类 (未穷举)」已替换「判得出的只有两类」的无依据能力上限说法; RESULT.md v5 已改为逐字引用 `PREREGISTRATION.md` 原文「这是对 §D2「只承诺两类破坏」局限的实证确认, 不是守卫失效的证据」, 经比对 `PREREGISTRATION.md` 原文逐字一致。SC-1 / SC-9 也已按行拆分为可转红的断言 (SC-9 「fail」与「不得 ship」同行、「作废」与「不得 ship」同行分别断言)。以上系 R4 code-reviewer / tech-lead 的 minor, 核对后未发现新漂移。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 2 major / 0 minor。本席 R4 唯一遗留项 (D2 四短语转述) 已 closed。本轮新发现 2 项 major, 均属知识库引用完整性问题: (1) D6 拟写入 SOT §6 的文本仍引用「RESULT.md v4」, 与本轮已同批升至 v5 的事实脱节, 且 proposal 头部的「RESULT 再修订须同步重核」清单未覆盖 §D6, 无 SC 兜底; (2) D1 表标注「定稿」的 SOT §2 新句末尾内嵌「(依 OQ-7 / OQ-9 裁定, 裁定不同则随之改)」, 逐字落地后, OQ 编号脱离本 proposal 即无法定位, 一旦本 spec 归档即成孤儿引用, 且与同一 SOT 文件 §6 已有的「issue #116」式永久引用惯例不一致。两项均是「文本一旦逐字落地即错」的具体缺陷, 修法都是一行编辑 (D6 把「v4」改「v5」; D1 的 SOT §2 新句去掉或替换该括注), 不涉及重新设计。其余检查 (三处 D1 新句可读性、CLAUDE.md 卫生双预算、D5.6/Aria#196/phase-a-planner 引用可定位性、OQ-7 自主栏事实依据、D6/RESULT 措辞与 SC-1/SC-9 断言) 均通过, 未发现其他新增阻断性问题。

## Vote

REVISE

## 术语与关系对照表

| 术语/概念 | proposal.md v5 | RESULT.md v5 | SOT/CLAUDE.md/手册 (拟改文本) | 一致性 |
|---|---|---|---|---|
| 核心句「只验证触发面没被改坏, 不验证 description 改得更好」 | D1 表三处新句逐字相同 (第 38-40 行) | 不含逐字句 (语义来源, 非宿主) | 三处落点现状均 0 命中, 待 T1 写入 | 一致 |
| D2 四短语枚举 (与相关文档 / 整理项目收尾材料 / 整理归档文档 / 收尾整理) | §D2 第 48 行四项全列, 点明「整理归档文档」带领域词 | §v5 表第 55 行四项逐字相同, `PREREGISTRATION.md` 第 9 行原文亦一致 | 不涉及 (proposal 转述层问题, 不影响落点文本) | 一致 (R4 major 已 closed) |
| RESULT.md 版本引用 | 头部 / §Why / §D2 / §D3 / Impact / T8 六处均写 v5; **§D6 仍写 v4** | 本次同批升至文件版本 5 (header 自述) | SOT §6 (D6 文本将逐字写入) | **不一致, 见 Findings 1** |
| OQ-7 / OQ-9 内部引用 | D1 表 SOT §2 新句 (标「定稿」) 末尾「(依 OQ-7 / OQ-9 裁定, 裁定不同则随之改)」 | 不涉及 | SOT §2 (逐字写入后脱离语境不可定位; 对比 SOT §6 现有 `issue #116` 式永久引用) | **不一致, 见 Findings 2** |
| 自主运行时 / 自主模式 / 交互模式 | SOT 新句与 §Impact 用「自主运行时」(第 39/117 行); OQ-7 正文用「自主模式 / 交互模式」(第 152-160 行) | 不涉及 | CLAUDE.md 现有「自主运行时 / 自主执行者 / (interactive)」, 无「交互模式」原形 | 不完全同形, 各自括注 v1.x/v2.0 且 SOT 句自带布尔条件不致误读, 见观察 (R4 观察延续, 未升级) |
| `10CG/Aria#196` 引用 | OQ-7「运行模式怎么判」段 (第 160 行) | 不涉及 | 不涉及 | 一致, 已核 issue 标题 (state open) 与引文逐字对应 |
| D5.6 新 issue (Layer 2 GLM 验证) | 「场景 4b 在 Layer 2 (GLM via Luxeno) 上的验证」(第 97 行) | 不涉及 | CLAUDE.md 项目状态段「glm-5.2 via Luxeno」用词风格一致 | 一致 |
| fail / void / provisional 值域 + SC-1/SC-9 按行断言 + D6 能力上限措辞 | 均按 R4 rework 修复 (非本席 R4 finding) | 逐字引 `PREREGISTRATION.md` 原文, 已核对一致 | 不涉及本席分内 finding | 一致, 核对后无新漂移 |
