---
verdict: REVISE
agent: knowledge-manager
round: R1
critical_count: 0
major_count: 1
minor_count: 1
---

# post_spec R1 审计报告 — secret-guard-nomad-var-put-echo (knowledge-manager 视角)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md`

## 结论摘要

- Level 2 Minimal 模板符合度: **通过**。章节顺序 (Why→What→关键决策→Impact→rule6_note→Tasks→Success Criteria) 与本项目近期两份同类 Level 2 spec (`archive/2026-08-01-session-closer-autofill-yaml-datasource`、`archive/2026-07-31-phase-c-gate-path-coverage-not-applicable`) 的既定扩展惯例一致, `关键决策` 段非模板原生但已是项目内已确立的惯例扩展, 非本 spec 自创。`Created: 2026-08-02` 与审计当日日期一致, `Status: Draft (待 post_spec 审计)` 标注方式与其他 spec 一致。
- Rule #5 (spec 位置): **通过**。位于 `/home/dev/Aria/openspec/changes/`, 非 `standards/openspec/changes/`。目录命名无日期前缀, 核对 `standards/openspec/project.md:130` 确认日期前缀格式仅适用于 **归档时** (`openspec/archive/{YYYY-MM-DD}-{feature}/`), 活跃 `changes/` 目录本就不带日期前缀 (与同批次 `aria-2.0-m6-*` 等目录一致) —— 不是缺陷。
- Impact 段版本管理: **通过**。`ship 同步面: aria 子模块 5 文件 + 主仓 gitlink + VERSION + README badge (i18n 正文无实质变更, #140 B 档)` 与 `/home/dev/Aria/CLAUDE.md` 版本管理段「发布同步面」逐字一致。版本号 `v1.65.2` = 当前 SOT (`aria/.claude-plugin/plugin.json` 实测 1.65.1, aria 子模块 HEAD `52d6f22` 已是 #121 merge) 的下一个 PATCH, 与「bug 修复 = PATCH」规则吻合。
- 交叉引用: **通过**。已用 forgejo API 直接核实 issue #170 原文、issuecomment-17187 (初版 triage)、issuecomment-17269 (更正) 三份原文，proposal 的"事故真实机制"「六形态实测表」「`nomad var put --help` 引文」均与 issuecomment-17269 逐字/逐行对应，未发现转述失真。`aether-plugin#11` 已用 API 核实存在、open、标题与「前提已修正」的说法一致。
- 命名/谱系: **通过**。change_id 描述性、无带圈数字/希腊字母编号 (已用脚本全文扫描确认零命中)。
- rule6_note 事实基底: **通过**。已核实 `aria/hooks/` 目录确无 `SKILL.md`，`hooks.json` 将 `secret-guard.sh` 注册为 PreToolUse hook (与 Skills/Agents 并列的第三类插件组件，见 `plugin.json` description「42个 Skills + 11个 Agents + Hooks系统」)，「不是 Skill」的事实陈述准确。

## 特别核查: 「关闭要求 2」的可追溯性证据链

**通过，且证据链质量高于一般水平**。核实结果:

1. proposal 头部同时链接 issuecomment-17187 (**初版**误判) 和 issuecomment-17269 (**更正**)，未只留最终结论链接、抹掉推翻过程 —— 未来读者能看到"错误判断本身"，而不只是"正确结论"，这正是可独立复核而非只信结论所需的最低条件。
2. 关闭理由引用的是**可独立验证的外部事实** (HashiCorp Nomad Variables API 官方文档 `PUT /v1/var/:var_path` 成功响应含解密 `Items`；本机 `nomad var put --help` 关于 `-out` 默认值随 TTY/重定向切换的原文) —— 而不是"AI 判断该前提不成立"这种不可复核的主观结论。读者可自行拉官方文档、自行跑 `nomad var put --help` 复核，不依赖信任本 spec 作者。
3. 六形态实测表在 issuecomment-17269 与 proposal 中逐行一致，构成可复算的证据矩阵。

**minor 缺口** (见下)。

## 详细发现

### Major-1: rule6_note 的判定框架存在双线论证、未落满其中任一行的完整义务

原文 (proposal.md L82-84):

> **Rule #6 不适用 (结构性前提不成立)**: 变更对象是 `hooks/secret-guard.sh` (PreToolUse shell hook), **不是 Skill** — 无 SKILL.md、无 description、不参与 skill 触发/加载, AB 套件的评测对象...与之无交集。判据表对照: 内容性质 = 处方性但作用于 harness 执行层而非 AI 指令面, AB 结构上测不到。**substitute: SC 级 baseline-failing 结构化测试**

这段同时使用了**两条不同规范的不同词汇**且未挑明用哪一条:

- **论证 A (out-of-scope)**: 「不是 Skill ⇒ Rule #6 不适用」。「结构性前提不成立」一词并非 `skill-benchmark-exemption.md` 决策表 (§2) 里的任何一行标签, 而是逐字借自 `configured-gate-authority.md` §2 白名单第 4 类 (「闸门自身的结构性前提不成立」)——那是**另一条规则 (Rule #10 已配置闸门权限)** 的豁免白名单, 针对的是"审计对象整个未产生", 不是 Rule #6 的判据表词汇。这个类比本身有一定道理 (Rule #6 原文「Skill 基准测试必须用 skill-creator」的适用前提就是"变更对象是 Skill", hook 确实结构上在此之外), 但**跨规则借用措辞而不点破**, 会让未来审计者误以为这是 `skill-benchmark-exemption.md` 决策表本身就有的一档 (它没有——该文档只有三行 + 「拿不准」, 见 §2)。
- **论证 B (in-scope 分类)**: 紧接着又写「判据表对照: 内容性质 = 处方性...AB 结构上测不到」——这句话的措辞对应的是决策表**第三行** ("处方性, 但套件覆盖范围外")。但决策表 §3 明确「第三行不是逃生舱」, 要求**同时满足三条**才算 substitute 成立: (1) 点名行为 + 为何套件结构上测不到; (2) **为该行为新建**可证伪定向 fixture (需实证：把改动回退, fixture 必须转红); (3) **把"套件缺该维度"开成 issue**。本 spec 给出了 SC-2/SC-3 baseline-failing 用例 (满足条件 1、2 的实质), 但**没有开出"AB 套件结构上无法覆盖 hook 层"这个套件缺口的追踪 issue** (条件 3 缺失)。

两条论证挑一条即可自洽, 混用会削弱可复核性:
- 若走论证 A (更贴合 Rule #6 原文「Skill 基准测试」的字面适用范围, 本审计认为这是更准确的定性): 不需要再对照决策表第三行, 也不需要开套件缺口 issue —— 但 spec 里"判据表对照"那句话应删除或改写, 否则读者会误认为本 spec 在主张走第三行却漏了强制条件。
- 若走论证 B (决策表第三行): 则条件 3 (开 issue 记录套件缺口) 是硬性要求, 目前**未满足**, 需要补开一个类似「AB 固定测试集结构上不覆盖 Hooks 组件」的 issue。

**这不是"本 spec 越界自行豁免"的实锤** —— 最终处置 (substitute + SC 级 baseline-failing 测试) 无论走哪条论证, 结果都合理, 且 SC-2/SC-3 提供了真实的可证伪红灯锁定, 不是空转的"照单全收"。但两条框架混用且都没有完整落地到其规范自身要求的形式, 属于 `skill-benchmark-exemption.md` §4 警惕的「决策表之外自创理由」的边缘情形 (哪怕不是恶意规避)。**建议**: owner/作者二选一并补齐: (a) 明确写「Rule #6 原文适用对象=Skill, hook 非 Skill, 结构性不适用, 不进入决策表」并删掉"判据表对照"那句, 顺带把这次判定沉淀为「Hooks 类变更结构性排除在 Rule #6 外」的可引用先例 (类似决策表 §5 worked examples 的写法, 供未来 hook 改动复用而非每次重新论证); 或 (b) 保留决策表第三行框架并补开套件缺口 issue。

### Minor-1: 官方文档引用无可点击链接

「经 HashiCorp Nomad Variables API 官方文档核实」(proposal.md L29) 与 issuecomment-17269 一样只有文字转述 + 手打的响应体示例, 未附官方文档 URL。虽然复核者可以自行搜索到 (Nomad 官方文档站点的 Variables HTTP API 页面), 但缺一步会略微提高复核门槛, 与本 spec 其余证据链 (issue 链接、`nomad --help` 可本地复验) 的严谨度不完全一致。建议在后续（哪怕是 Tasks 收尾阶段）补一条官方文档直链，使这处证据闭合到"点击即可核对"而非"文字转述 + 自行搜索"。

## 未发现问题的检查项 (供归档留痕)

- 未发现带圈数字 / 希腊字母编号违规。
- 未发现 Impact 段与 CLAUDE.md 版本管理段冲突。
- 未发现命名惯例偏离 (change_id 目录无日期前缀, 与项目现有活跃 spec 一致; 日期前缀属归档时行为)。
- 未发现「issue 要求 2 关闭」缺乏证据链的情况 —— 反而是本 spec 证据链质量的亮点 (保留了错误初判 + 更正的完整推翻轨迹, 而非只留结论)。
- CLAUDE.md 顶部「项目状态」段落写的插件版本号 (v1.65.0) 与 aria 子模块实际 HEAD (v1.65.1, `52d6f22`, 已含 #121 merge) 不一致 —— 但这是**既有的、非本 spec 引入的** CLAUDE.md 项目状态段落 staleness, 不在本 spec 变更范围内, 且不影响本 spec 自身 `v1.65.2` (相对 1.65.1 的下一个 PATCH) 的正确性, 故不计入本报告 critical/major/minor, 仅作旁注供后续 CLAUDE.md 维护参考。
