---
checkpoint: post_planning
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-22T15:39:48.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

派单 sha256[:16] = c510dd887510a6cd

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` (全文, 241 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` (全文, 1982 行, 分 7 次读完)
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md`: `Why`(1-69) / `What` 全部 1.0-1.4 (70-324) / §2-§5 (325-392) / `Impact`(393-406) / `Tasks`(407-452) / `Success Criteria` SC-1~SC-16 逐条 (453-472, SC-17~SC-22 未逐条精读, 但通过 tasks.md/yaml 的引用已覆盖其结论) / `rule6_note`(480-487) / `待 owner 复议` 条目 0 摘要 + 全部 13 条逐条 (488-558)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文
- `.aria/audit-reports/post_planning-R5-2026-09-22T034038-000Z-pre-merge-completeness-gate-change-scope-aggregated.md` 全文
- `.aria/audit-reports/post_planning-R2-2026-09-18T162427-983Z-pre-merge-completeness-gate-change-scope-knowledge-manager.md` (仅用于核对 `638d2a0f` 是否为已登记未处置项, 不作为本轮证据来源)
- `standards/conventions/content-integrity.md` §4.4 / §4.5 全文 (940cb5b)
- `aria/skills/phase-c-integrator/SKILL.md` `:50-64` / `:748-759` (1cb3872)
- `aria/skills/audit-engine/SKILL.md` `:418-427` (1cb3872)
- `aria/skills/state-scanner/scripts/lib/spec_complete.py` `:325-374` (checkbox 正则与 `_iter_task_items`)
- `aria/skills/state-scanner/scripts/check_bare_issue_refs.py` `:120-157` (CLI 与退出码)
- `CLAUDE.md`(主仓根) `:135-144` (项目状态段实读, 核 "16 点" 与 CLAUDE.md 引用面)
- `.aria/probes/main-project-version-consistency.py` 全文
- `.aria/state-checks.yaml` `:124-150` (`m6-version-badge-match` / `m6-claude-md-version`) / `:408-436` (`plugin-version-arch-docs-match`) / 全文 grep `CLAUDE.md`
- 实跑: `git diff --stat b686185 e7a1782 -- openspec/changes/.../ .aria/notes/.../gen_yaml.py`(在 scratch 副本 `p199-r6/base/Aria`) 确认三文件改动量; `git diff b686185 e7a1782 -- tasks.md` 全文比对判断清单第 40-45 条与等待点表改动是否逐字落地; `file` 命令核 4 份 SKILL.md 的换行符形态

## R5 对账

| 题 | 判定 | 证据 |
|---|---|---|
| R5-M1 `9c294cca` (owner_gates 第 13 项拆分) | **closed** | yaml `owner_gates` 第 13a/13b 两行已按 "release 前请 / latest.md 提交后请" 拆开 (`detailed-tasks.yaml:218-219`); tasks.md 等待点表同步拆行 (`tasks.md:121-122`, git diff 第 3 个 hunk 逐字核对); 判断清单第 40 条 (`tasks.md:95`) 完整复述拆分动机与"13a 已批 13b 未批"中间态的处置 (记台账); TASK-031 的 claim 条 (`detailed-tasks.yaml:1975`) 与末条 (`:1982`) 均已改指 13a/13b |
| R5-M2 `3e6a8483` (会话入口 claim 核验) | **closed** | `hard_constraints` 第 4 条 (`detailed-tasks.yaml:194`) 新增完整的 "三元组解析→前置检查→强制对齐→重解析→心跳" 序列, 含 TASK-024 会话与 5.9 release 后会话两处例外; owner_gates 14/15 挂载范围已从 "1.1" 扩到 "任一会话的入口 claim 核验" (`:220-221`); TASK-001 心跳条 (`:1351`) 已插入强制对齐步骤; `metadata.v2_state_runs` 新增 N11 (`:1142-1240`), 实测输出显示 v2.4 顺序在本地落后/被 sweep 两态下均误判 (`push_success=False` 或读到过期 `active`), v2.5 顺序正确对齐后得到 `push_success=True` 与 `active=0` (`:1320-1333`) |
| R5-M3 `3782becc` (C.2.4.5 子模块指针闸) | **closed** | TASK-030 新增独立验证条目 (`detailed-tasks.yaml:1944`), 逐字给出触发条件、命令、放行判据 (退出 0 + 逐子模块结论行) 与失败路由 (owner_gates 17); tasks.md 5.8 行、范围边界表、等待点表第 17 行均已同步 (git diff 第 5/8 个 hunk); 判断清单第 42 条给出 SKILL.md 触发段与脚本行为的实读依据 |
| R5-M4 `c287d217` + 同处 `1453c41f` (TASK-027 第 4 步 (b) 与 guard_config_hooks) | **closed** | TASK-027 第 4 步 (b) 已改为与 TASK-001 同口径的 `cat-file -e` 前置 (`detailed-tasks.yaml:1873`); 新增 (c) feature 一侧比对并按 Rule #6 判据表分类 (同一行, 直接闭合 `1453c41f`); `sc12_liveness.guard_config_hooks` 已重写为 `git -C <主仓根> grep ... ; echo rc=${PIPESTATUS[0]}` 形式并要求 "末行 rc= 为 0 或 1 且其前无输出" (`:329`); `metadata.v2_state_runs` N10 补两态, 输出显示旧命令在 "从 aria/skills/audit-engine/tests 跑" 与 "根目录非仓" 两态下误判为 pass, 新命令正确判 stop (`:1314-1319`); TASK-021 重写 a 条与 TASK-031 SC-12 liveness 条均已改用新 guard (`:1749`, `:1973`) |
| R5-M5 `76921ca3` (skill-creator 工作区选址) | **closed** | TASK-024 工作区条款已钉死 "只放 `aria-plugin-benchmarks/ab-workspace/<本次结果目录名>/`" 并给出 SC-13 / `no-unresolved-version-placeholder` 递归检索盲区的具体理由 (`detailed-tasks.yaml:1810`); 判断清单第 44 条完整记录 (a)/(b) 两案取舍与 `aria/skills/issue-triage-workspace/` 这一既存噪声如何被 "两次快照之差" 而非 "断言为空" 正确吸收 |
| `1453c41f` (与 R5-M4 同处) | **closed** | 见上一行 |
| `118d1d64` (TASK-031 deliverables 漏列 `latest.md`) | **closed** | `detailed-tasks.yaml:1964` `deliverables` 列表已含 `docs/handoff/latest.md`, 与 v2.4 对 TASK-029 "只列本任务提交的文件" 同口径 |
| `ac2e8dcb` (owner-container 空值同族) | **closed** | TASK-031 起稿条 (`detailed-tasks.yaml:1977`) 已加 "退出非 0 或输出为空 ⇒ 按 handoff-mechanics.md 回退手填" 分支; 写后自校验条 (`:1978`) 在原 E1 之外新增一条值非空断言 (`grep -cE '...: *[^ ]'` 须 `==5`), 两处均标注 "v2.5, post_planning R5 ac2e8dcb" |
| `11c3a29f` (`aria_shifted` 第 6 条非路径) | **closed** | `metadata.baseline_rebase.aria_shifted` 原三文件连写的一条已拆为 `.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` / `README.md` 三条独立记录 (`detailed-tasks.yaml:77-79`), 拆分注明标注 `v2.5 按 post_planning R5 11c3a29f 拆开`; TASK-001 基线复核条新增 "每个文件另先确认它至少在两个端点之一存在" 的 `cat-file -e` 前置 (`:1355`) |

**未处置项确认未被无据重提**: R5 另三条 minor (`34b92188` / `27cee280` / `ae4753f5`)、R4 另四条独立 minor 与前轮未动 minor, 本轮通读中未发现新证据, 未作为 finding。旧有 R2 minor `638d2a0f` (`main-project-version-consistency` 与本 spec 16 点版本轴正交) 本轮独立复核后结论不变 (见「风险 / 疑问」), 未重复立 finding。

## Findings

| id | severity | type | category | scope | 一句话 | 证据 | 失败场景 | 建议修法 |
|---|---|---|---|---|---|---|---|---|
| M1 `591d8667` | major | issue | documentation | `detailed-tasks.yaml TASK-031` (`commit_attribution` 复核缺口, 已知项 A 升级) | TASK-031 (5.9) 全程未再调用 `metadata.commit_attribution`, 而判断清单与该判据自身都声称 "5.9 周期 handoff 靠 frontmatter track-id 逐字相符兜住"——这句"兜住"对 5.9 自己产生的提交是空头承诺 | (1) `commit_attribution` 全计划仅两处调用点: TASK-001 `detailed-tasks.yaml:1353`("回落前对 origin/master..<起点> 跑 metadata.commit_attribution") 与 TASK-030 `:1941`("对 origin/master..<主仓 feature 分支> 跑 metadata.commit_attribution"); (2) 逐条通读 TASK-031 全部 verification (`:1967`-`:1982`, 含快进、issue、勾选、归档预演、SC-12 liveness、claim/release、回帖、周期 handoff 起稿、E1 自校验、`latest.md` 两子步、末条双推), 无一处再次调用该判据; (3) 该判据自身的 `cannot_catch` 字段 (`:745`) 与 tasks.md 判断清单第 33 条 (`tasks.md:87`) 都写 "5.9 周期 handoff 靠 frontmatter `track-id` 逐字相符兜住" | 执行者手写周期 handoff frontmatter 时把 `track-id` 打错一个字符 (如漏字/多字/大小写, 该字段是逐字手填, 非模板派生) → TASK-031 的 E1 写后自校验 (`:1978`) 只验证 5 个字段**名称行是否存在**且**非空**, 不比对 `track-id` **取值**是否逐字等于 `pre-merge-completeness-gate-change-scope` → 归档 / 周期 handoff / `latest.md` 三个提交在 owner_gates 13b 获批后直接双推 → 没有任何步骤把这段提交范围重新喂给 `commit_attribution` → 若真被喂入, 该提交因 handoff 路径的 `exclusive()` 判据 (`:717`, 正则精确匹配 `^track-id:\s*{SID}\s*$`) 不命中而落 `foreign`, 整体 `verdict=stop` exit 1, 本该触发 owner_gates 16 停下请裁; 而实际因判据从未被调用, 三态里 "坏实现" (即 v2.5 现状) 连一次求值机会都没有——错误的 `track-id` 就此永久留在已推送的 handoff 里, 未来任何按 `track-id` 检索或以 `commit_attribution` 复核该历史提交的机制都会把它误判/漏判 | 在 TASK-031 请求 owner_gates 13b 之前 (`latest.md` 单独提交产生之后) 新增一步: 对 `<TASK-030 合并提交>..<latest.md 提交>` 重跑 `metadata.commit_attribution` (传入本次 ab-results 目录同款 `extra`), 非 `ok` 即停下走 owner_gates 16; 或至少在 E1 之外单独加一条断言, 直接比对 handoff frontmatter 的 `track-id` 字段**取值**与 `pre-merge-completeness-gate-change-scope` 逐字相等 (做法与 R5 `ac2e8dcb` 新增的"非空检查"同款, 只是判据从"非空"换成"等值") |

## 对执笔人自报薄弱点的表态

1. 会话入口"强制对齐"依赖前置检查无盲区 —— **可接受**。我独立读了 `coord_ref_precheck` 全部代码 (`detailed-tasks.yaml:639-669`): 它对每个本地领先的提交都取 `diff-tree` 文件集与逐行 diff, 要求全部文件 ⊆ 本轨 claim 文件集且每行改动都以 `heartbeat_at:` 开头才判 `own-heartbeat`, 任何混杂改动 (即使只多带一个非本轨文件) 都会被判 `other` 而拦下, 方向是 fail-closed。它测不到的只是"git diff 看不出的东西", 这是任何基于内容比对的检查的共同边界, 不构成本条特有缺陷。
2. 会话间隔期 (>24h) 防不住 sweep —— **可接受**。这是"检查只在会话入口跑一次"这一架构选择的必然代价, 没有后台常驻心跳的前提下无法做到实时防护; 计划已如实把后果 (多一次 owner 往返) 写入等待点 14 而非隐藏, 属恰当的风险外化而非缺陷。
3. 13a 已批、13b 未批的中间态只记台账 —— **可接受**。该中间态里协调 ref 上本轨状态已是终态 `done`, 不是"卡死"也不产生外向副作用 (归档与周期 handoff 仍只在本地), 记台账留痕已是相称的处置; 引入额外的"回滚 release"机制成本与收益不成比例。
4. C.2.4.5 判据绑定脚本当前输出行格式, 脚本一改就误停 —— **可接受**。失效方向是 fail-closed (拒绝合并、不是放行合并), 与"宁可多问 owner 一次, 不可漏拦一次子模块回退"的整体设计取向一致。
5. 同族扫描候选生成靠词形, 仍可能漏网 —— **可接受**。自然语言同型判据的穷举本身没有可判定的终止条件; 本轮 v2.5 已完成两轮扫描 (dispatch 点名 2 处 + 交互检查另找 1 处), 且明确承认残余风险而非声称穷尽, 是诚实的自评, 不构成新增缺陷。
6. `hard_constraints` 第 14 条通则依赖执行者知道每条命令的结果码 —— **可接受**。我核对过该条款原文 (`detailed-tasks.yaml:204`) 明确把 `fetch` 纳入"结果码集合为 0"的通用条款覆盖范围, 这正是为了不用在 TASK-023/025 等每一处 `git fetch origin` 后逐字重复"须退出 0"; 通则本身已覆盖, 未落实与"通则不存在"是两回事, 后者才该判缺陷。
7. "Ran 数不得少于基线"在上游合法删测试时会误停 —— **可接受**。同样是 fail-closed 方向: 停下人工核对比"静默吞掉真实的用例减少"更安全, 且该场景本身极罕见 (aria 侧删测试需要独立的 spec)。
8. N11 是合成态、非生产时序证明 —— **可接受**。24 小时级别的真实 `SWEEP_TTL` 等待在自动化验证里不可行, 用固定容器身份 + 手工推进 `heartbeat_at` 到过期值来验证分支逻辑是标准做法; 执笔人如实标注了"证明分支逻辑而非生产时序"而未夸大结论, 是恰当的证据边界声明。
9. 同体自检不能证明没有下一处 —— **可接受**。这是所有自检的认识论共性, 不是本计划特有的弱点; 恰恰因为如此才需要本轮这样的独立多席外部审计, 执笔人如实承认这一点本身是加分项而非减分项。

## 风险 / 疑问

- **`638d2a0f` (R2 minor, 未处置, 非新证据)**: 本轮独立复核确认结论不变——`main-project-version-consistency` 的 9 个 `POINTS` (`.aria/probes/main-project-version-consistency.py:39-49`) 全部指向"主项目版本"这条独立轴 (root `VERSION` 头部 `> **版本**: 1.7.5`, 与 CLAUDE.md "主项目 v(...)" 行、四份 README 的 "Project Version:" 行、两处架构文档的 "Aria main repo" 行), 与本 spec 要同步的"16 个版本点"(aria-plugin 版本轴) 结构上零交叠, 且 TASK-029 唯一改动的 `VERSION:24` 行不在该 9 点清单内。TASK-029 把它与另外 4 个版本类 check 并列写进"复跑…为 OK"不算错误 (它确实不受本 spec 触碰, 复跑必然 OK, 是合理的常规回归复核), 但容易被误读为"16 点已有该 check 兜底"。owner 尚未就此表态, 按规则不重复立 finding, 仅在此复述以便下一轮判断参照。
- **CLAUDE.md 的 "两处" 版本引用无机械兜底**: 实读当前 `CLAUDE.md:138,142` (非计划记录的 `:139/:141`, 印证"行号有保质期"), 确认现状恰为两处 (`v1.52.0–v1.73.3` 与 `版本: aria-plugin v1.73.3 | ...`)。但遍历 `.aria/state-checks.yaml` 全部版本类 check (`m6-version-badge-match` 只比 README badge、`m6-claude-md-version` 只比文件顶部方法论版本"2.0.0"、`plugin-version-arch-docs-match` 只比两份架构文档), 没有一个校验 CLAUDE.md 项目状态段里的 aria-plugin 版本字符串。TASK-029 的手工 `grep -n` 步骤本身足以覆盖 (这不是"漏掉必做项", 该步骤明确要求逐处 grep 后改), 但若执行者误改漏改, 复跑的 5 个 custom checks 里没有一个能捕捉到——这与上一条 `638d2a0f` 同族, 一并留作背景, 不单独立 finding。
- **执笔人十条请裁 (v2.5, 背景事实条目 B)**: 各条均为需要 owner 表态的流程判断, 未见与本席视角 (文档同步 / 映射表 / 裁定 / 写法规范) 直接冲突的内容, 不在此逐条复议。
- **已知项 A 已升级为本轮 M1 finding**, 不再单独在此重复。

## Verdict

verdict: PASS_WITH_WARNINGS
counts: 0C/1M/0m
**Vote: REVISE**

## 是否足以开始 Phase B

**不足以**——原因有二, 层级不同: (1) 外部入口门 (owner_gates 第 1 项) 事实未变: 10CG/Aria#195 仍 `yielded`、其 Phase B 尚未开始, 与本轮 v2.5 修法质量无关, 是先决条件缺失; (2) 就本席审的文档同步面 / 两张映射表 / 13 条裁定 / 22 条读前必看 / 写法规范而言, v2.5 已忠实修复 R5 五题 Major 与两条同处 minor, 新发现的 M1 (`commit_attribution` 在 Phase D 不可达) 是可定点修补的收尾类缺陷, 不影响 Phase A-C 的可执行性, 但在 owner 就 M1 与 `638d2a0f` 表态前, 建议不把本轮计为"最终无保留通过"。
