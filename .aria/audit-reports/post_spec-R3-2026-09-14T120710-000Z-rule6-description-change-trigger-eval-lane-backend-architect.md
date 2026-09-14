---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-14T13:15:00.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [backend-architect]
---

# post_spec Round 3 — backend-architect

被审对象: proposal.md v3 (HEAD `0c41e53`) + RESULT.md v3 (含 v4-counterfactuals / probe json / manifest.json / neutral-skill-SKILL.md / run_arms_v4.sh)。逐条核对 R2 中本席提出的 4 条 minor, 并按任务书对 v3 §D2/§D3 做机制复核, 排查新引入问题。

## R2 对账

1. **realroot 合成规模 → partially closed (未变化, 沿承 v2)**。RESULT.md v3 §已知局限第 5 条逐字: 「`run_eval.py` 判「触发」= 第一个 tool_use 就是本合成技能 (Skill 或 Read)。v4 realroot 在约 25 个合成文件的项目根下 30/30, 但该根没有 CLAUDE.md、没有竞争技能、没有深层目录, 比 Aria 主仓小一到两个量级; 真实大仓下未验证。」与我在 R2 提出的措辞几乎逐字对应, 诚实限定了适用范围。但 `git diff 55bc9f3 0c41e53` 显示这一段落实质内容自 v2 起未变 (仅标点/断句微调), 即「真实大仓验证」这个底层动作本身仍未做, 也未新开动作项承接。判 partially closed, 移入观察 (非阻塞: 诚实标注已到位, 补验证的成本与「真实仓」规模不成比例, 不应卡本 cycle)。
2. **§D5.4 修复方向覆盖面 → closed (覆盖面按要求扩大), 但引入新的机制误述, 见 Findings**。v3 D5.4 (ii) 现文: 「合成技能不嵌入真技能名, **文件名、`# <skill_name>` 标题、`This skill handles:` 首句三处都要改**」——已从 v2 的「命令文件名不嵌技能名」(只点 1 处) 扩为逐字点名 3 处, 直接回应了我在 R2 的诉求（扩大覆盖面）。闭合动作本身合格。但把三处一并断言为「都嵌入技能名」引入了新的不准确表述 (详见 Findings 唯一条)。
3. **manifest 97→13 与 97→12 → closed**。RESULT.md v3 新增「技能数口径」段: 「两份机读探针…自报 97 / 12; `manifest.json` 里的「97→13」来自本 session 首次探针 (未传 `--model`, project-only 下实际走了 `claude-opus-5[1m]`, 未落机读文件)。可靠的机械事实只有一条: 默认设置源下列表含真 `openspec-archive`, project-only 下不含。」——把「13 vs 12」的数字漂移完整归因 (不同探针批次 + 未传 `--model` 导致模型切换 + 该批次未落机读文件), 并把结论收窄到「只用 result 字段的含/不含, 技能数不作证据」, 认识论上比 v2 更稳健。经核对两份 probe json 的 `result` 字段实际为 `"97,yes"` / `"12,no"`, 与该段描述完全一致。closed。
4. **过宽臂机制 (自然措辞扩张未验证的限定) → closed**。proposal v3 §Why 第 2 条、§D2「只承诺已验证的两类破坏」与 RESULT.md v3 结论 2 均已加上「显式强制过宽」限定语并明确「**未验证**: 自然措辞扩张…能否让某条 should-not 越过 0.5」, OQ-8 专门讨论此项残留风险且给出不阻塞 ship 的理由。RESULT.md v3 还新增「过宽臂 should-not 22/30 的分布」整段, 逐类别 (3/3 六条 / 2/3 一条 / 1/3 两条 / 0/3 一条) 复核并点名「触发与词表相关但不是逐词线性」。用 python 解析 `v4-counterfactuals/overbroad.json` 逐条核对: 3/3 六条、2/3 一条、1/3 两条、0/3 一条 (即含「分支」+「归档」两个关键词却 0/3 的那条 query, 原文确认同时含这两词) 与该段描述逐条吻合, summary `passed=13/total=20` 与「22/30 (7/10 判红)」等价 (20-13=7)。closed。

汇总: **closed 3 (2/3/4) / partially 1 (1) / open 0**。

## Findings

- [major] architecture/proposal.md §D5.4 (issue): D5.4 (ii) 与 RESULT.md §结论3(b)、§Why 第 3 条三处同源断言「文件名、`# <skill_name>` 标题、`This skill handles:` 首句」三处「都嵌入技能名」; 但 `run_single_query` 该三行模板 (`run_eval.py:52-54,65-66`) 实为: 文件名 `clean_name=f"{skill_name}-skill-{unique_id}"` 与标题 `f"# {skill_name}"` 确实嵌入 `skill_name`, 而首句模板是 `f"This skill handles: {skill_description}\n"` —— 嵌入的是 `skill_description` 参数, 不是 `skill_name`; 本轮全部实测 arm (new/old/negctrl/overbroad/realroot) 的 description 原文均不含技能名字面串, 该行结构上从未泄漏技能名。若上游按字面理解, 会被引导去修改一处并不产生泄漏的代码, 属于给外部 Key Deliverable (T6 上游反馈) 的技术断言错误, 需在 ship 前订正三处同源表述 (改为「两处结构性嵌入 skill_name (文件名/标题), 需连同 uuid 检测串一并去标识化」, 首句是否需要改动应换一个不依赖「嵌入技能名」的理由, 或从「三处都要改」中移出)。

## 观察

- realroot 合成规模的「真实大仓验证」缺口仍未闭合 (见 R2 对账 1), 但 RESULT.md 已诚实标注适用范围, 且补验证成本 (需要接近 Aria 主仓量级的合成或真实项目根) 与当前 cycle 的边际价值不成比例, 不建议卡本次收敛; 建议留一句「后续若在其他 skill 上复用场景 4b, 首次遇到大仓可顺手补验证」即可, 不必单开动作项。
- D2「同批负控」判据「负控 query 级命中…须 ≤5/10」未显式点名是针对 should-trigger 10 条 (而不是 should-not 10 条或 20 条全集); 从上下文 (基线 v3 负控 3/10 与记分表的对应关系) 可以唯一确定所指, 但字面表述留了一丝可省略的歧义空间, 若要更严谨可在 D2 该句后加「(should-trigger 子集)」六字, 不阻塞。
- 正向复核 (未发现问题, 记录以备查): (1) 独立用 hypergeometric 公式手算「10 对 5」「10 对 6」两个 Fisher 单侧 p 值, 结果分别为 0.01626→0.016、0.04334→0.043, 与 D2 正文数字一致; (2) `aria/skills/` 实测 43 个目录 / 42 个含 `SKILL.md` / 唯一例外 `issue-triage-workspace`, 与 D5.2 新口径逐字一致; (3) `ab-suite/trigger/` 目录当前不存在 (0 个), 与 D5.2「现有 trigger 套件 0 个」一致; `ab-suite/version.yaml` 当前 `version: "1.5.0"`, 与 SC-4「改前 1.5.0」一致; (4) D3 六行前置表新指定的 9 个具体机读文件路径逐一 `test -e` 均存在, SC-2 的可判定性成立。这些核对均未发现新问题, 说明 v3 在数字/路径类精度上普遍有改进, 目前定位到的机制误述集中在 D5.4 这一处。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 1 major / 0 minor (本席视角)。

## Vote

REVISE

## 机制核实记录

- 读 `proposal.md` v3 全文 (D1–D6、Tasks、SC-1~10、OQ-1~8、rule6_note), 逐条对照 R2 聚合报告与本席 R2 报告的措辞变化。
- 读 `RESULT.md` v3 全文 (字段表 / 技能数口径 / 记分 / 统计 / 结论 1-3 / 对 Rule #6 处方的含义 / 原始产物 / 时长与成本 / 已知局限)。
- `git diff 55bc9f3 0c41e53 -- openspec/changes/.../proposal.md` 与 `-- aria-plugin-benchmarks/.../RESULT.md` 逐段比对 v2→v3 的全部改动, 定位「结论 3(b)」由两处扩为三处的确切增量文字 (新增 `正文首句 This skill handles: <description>` 一句), 确认这是 v3 rework 新引入的表述, 非 R1/R2 已讨论过的旧问题延续。
- 逐行重读 `run_eval.py::run_single_query` (`bb335391eb83/skills/skill-creator/scripts/run_eval.py:51-67`): `clean_name = f"{skill_name}-skill-{unique_id}"` (行52) → 文件名 (行54) 嵌入 `skill_name`; `f"# {skill_name}\n\n"` (行65) 嵌入 `skill_name`; `f"This skill handles: {skill_description}\n"` (行66) 嵌入的是**函数参数 `skill_description`**, 与 `skill_name` 是两个独立形参, 代码里无交叉引用, 结构上不可能通过该行泄漏 `skill_name`。核对本轮全部 5 个 arm (`run_arms.sh`~`run_arms_v4.sh` 里的 new/old/negctrl/poscontrol/overbroad 描述原文, 以及 `neutral-skill-SKILL.md` 的 `name: helper`) 的描述文本, 均不含各自 `skill_name` (`openspec-archive` 或 `helper`) 的字面子串, 确认该行在全部已跑实验里都未发生过技能名泄漏, 不是「理论上不泄漏、实际泄漏」的反例被掩盖。
- 核对 D2「作废语义」决策树相对 `run_eval()`(:184-256) 的 `did_pass` 逐行语义: 被评 arm 与负控 arm 是两次独立 `run_eval.py` 调用 (各自独立的 `ProcessPoolExecutor`), 互不读取对方输出; 「门」(全部 20 行 `pass` 为真) 完全是被评 arm 自身 JSON 的函数, 「作废」阈值完全是负控 arm 自身 JSON 的函数, 两者在数据流上零耦合, spec 定义的「门先于作废」优先级只是一条外部解释顺序, 不依赖 `did_pass` 内部有任何特殊分支即可自洽; 枚举 (门通过∧负控≤5)/(门通过∧负控≥6)/(门不通过, 负控任意) 三分支覆盖全部整数域 [0,10] 且两两不重叠, 无空集真空、无遗漏格。
- 用 python 独立按超几何分布公式手算两个 Fisher 单侧 p 值核对 D2 数字: 10 对 5 (P(X=10), K=15,N=20,n=10) = C(15,10)*C(5,0)/C(20,10) = 3003/184756 ≈ 0.01626, 四舍五入 0.016, 与正文一致; 10 对 6 (K=16) = C(16,10)*C(4,0)/C(20,10) = 8008/184756 ≈ 0.04334, 四舍五入 0.043, 与正文「不取」的备选数字一致。
- `python3 json.load` 解析 `v4-counterfactuals/overbroad.json`, 逐条打印 10 条 should-not query 的 `triggers/runs`, 与 RESULT.md v3 新增的「过宽臂 should-not 22/30 的分布」段逐条核对 (3/3 六条·2/3 一条·1/3 两条·0/3 一条), 并确认「0/3 且同时含「分支」与「归档」」指向的具体 query 文本属实; `summary.failed=7` 与「7/10 条判红」一致。
- `test -e` 核对 D3 六行前置表新指定的具体文件 (`v1-shared-root-4workers/new.json`、`v2-isolated-root-1worker/new.json`、`v1-shared-root-4workers/diag02-sibling-command-collision.jsonl`、`v2-isolated-root-1worker/negctrl.json`、`v3-isolated-root-1worker-neutral-name/{new,negctrl}.json`、`neutral-skill-SKILL.md`、`probe-setting-sources-{default,project}.json`) 全部存在。
- `cat` 两份 probe json, 确认 `result` 字段分别为 `"97,yes"` / `"12,no"`, 与 D3 第 3 行「实证看两份 json 的 `result` 字段: …其中的技能数是模型自报, 不作证据」的新表述完全对应。
- `find`/`ls -d` 核对 `aria/skills/` 现状: 43 个目录、42 个含 `SKILL.md`、唯一例外 `issue-triage-workspace`, 与 D5.2「41 个 skill 无 trigger 套件」新口径 (43 目录/42 skill/0 现有套件/41 余量) 逐字一致; 核对 `aria-plugin-benchmarks/ab-suite/trigger/` 当前不存在 (0 个套件) 与 `ab-suite/version.yaml` 当前 `version: "1.5.0"`, 均与 proposal 相应数字吻合。
- 复核 D3 第 1 行「`--num-workers 1` 与独立项目根两者正交」: 文字实质与 R2 时相同 (仅重新分句), 沿用本席 R2 报告已完成的代码级论证 (`ProcessPoolExecutor(max_workers=num_workers)` 提交范围与 `command_file` 的 `finally: unlink()` 生命周期分析), 结论不变, 未发现新问题。
