---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-13T17:36:16.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [backend-architect]
---

## Findings

- [major] testing/RESULT.md §已知局限 · proposal.md §D3.1 (issue): 场景 4 的地板守卫只在完全空白项目根 (无其余可探索文件, 仅 `.claude/`) 下验证; `run_eval.py::run_single_query` 第 133-141 行判「触发」要求**第一个** tool_use 就是本合成技能, 探索式开局 (先 `ls`/`Bash`) 直接 `return False`。真实 Rule #6 适用场景 (skill 活在有大量文件的真仓, 如 aria-plugin) 下该判据可能系统性把「先探索再触发」计为未触发, 使地板守卫失真。RESULT.md 已如实标注"未在真实项目根验证", 但 D3 前置只写「独立项目根 (空 `.claude/`)」, 没有把"项目根须整体为空"钉为长期约束或反过来限定地板守卫结论的适用范围, 二者衔接处留白。
- [major] architecture/proposal.md §D4 · standards/conventions/skill-benchmark-exemption.md §4 (issue): D4 称在 SOT §4 给 rule6_note "模板加两栏", 但实读 §4 (`skill-benchmark-exemption.md:47-56`) 全文只是一句散文式要求 ("都要在 spec/tasks 留 `rule6_note` 引用本规范"), 没有任何结构化字段/模板可"加栏"。全仓 `grep -rn rule6_note` 核对: 历史用法清一色是自由文本 (`## rule6_note` 标题或行内散文), 唯一见到字段化形态是 task-planner `detailed-tasks.yaml` 里的 `metadata.rule6_note` (不同文件、不同层级, proposal 未引用)。SC-3 的反事实检验 ("按模板文字能判出不合规") 要成立, 前提是这份"模板"确实存在且有可判读的字段语法 —— 目前看这是要**新建**一份结构化 rule6_note 字段规范, 而不是"加两栏", T3 落地前需先定位/新建这份模板的确切文件与形状。
- [minor] testing/proposal.md §D3.3 · manifest.json `harness.isolation` (risk): "`claude -p` 自报技能数 97 → 13" 这条量化证据在交付产物目录里找不到对应的原始记录 (仅见于 `manifest.json` 与 `RESULT.md` 的叙述性文字)。唯一可查的原始 transcript (`v1-shared-root-4workers/diag02-sibling-command-collision.jsonl` 的 `system/init` 事件) 显示的是 `skills` 18 条、`plugins` 0 个, 与 97、13 两个数都对不上, 且未说明该 transcript 用的是第三种环境配置。SC-2 要求 D3 每条前置都能对应 RESULT.md 里一个实证, (c) 这条的证据链比 (a)(b) 弱一档。
- [minor] documentation/RESULT.md §结论 3(a) · run_arms.sh vs run_arms_v2.sh (risk): v1→v2 同一步里**同时**改变了「共享根 vs 独立根」与「`--num-workers 4→1`」两个变量, 记分表本身 (4-7/30 → 27-30/30) 不足以把 (a) 的因果贡献从"并发度下降本身"里单独分离出来。好在 `diag02-sibling-command-collision.jsonl` 提供了独立于聚合分数的直接机制证据 (人工 query 实际调用了兄弟 worker 的 `openspec-archive-skill-2478f407` / `-e136a6c3`, 已核实), 弥补了这层不精确; 但 RESULT.md/proposal.md 都没有点破"数字本身有此局限, 结论靠 diag02 兜底"这一层论证结构, 单看记分表容易误把相关性当因果。
- [minor] architecture/proposal.md §D5 · SC-6 (risk): 上游反馈的验收只要求"发出证据"存在 (反馈 ID 或截图), 未要求反馈内容含可复现材料 (diag jsonl / 复现脚本) 或具体修复方向。若反馈过薄, D3.1 "或上游修好 (a)" 这条分支可能永远不会兑现, 单 worker workaround 的运行成本 (~8 美元/12 分钟/次) 变相永久化, 且没有后续追踪机制 (无 issue 挂钩、无重估时间点)。

## Verdict

PASS_WITH_WARNINGS — critical: 0, major: 2, minor: 3。两条 major 都是"处方在实施阶段会撞到落点不对/前提缺证据"的结构性缺口 (地板守卫外部效度边界未钉死; rule6_note 模板的物理落点与形状待明确), 不构成推翻本 Spec 结论 (场景 4 恒打平、不能当区分力尺子、只能当地板守卫) 的理由, 但 Phase B 落地 D3/D4 前应先解决。

## Vote

REVISE

## 机制核实记录

- 读 `run_eval.py:22-32` (`find_project_root`, 向上找 `.claude/` 目录) + `:35-181` (`run_single_query`, `clean_name = f"{skill_name}-skill-{unique_id}"` 第 52 行; 命令文件名/正文嵌入 `skill_name` 第 52/65-66 行; 触发判据「首个 tool_use 必须是 Skill/Read 且含 `clean_name`」第 128-154 行, 非目标 tool_use 直接 `return False` 第 137-141 行) + `:184-256` (`run_eval`, `ProcessPoolExecutor` 按 `eval_set × runs_per_query` 一次性提交所有 future, `project_root` 对所有 worker 共享同一值, 第 198-211 行; `did_pass` 计算第 230-234 行, 与 D2 判据文字逐字对应)。
- 读 `utils.py:7-46` (`parse_skill_md`, 从 SKILL.md frontmatter 抽 `name`/`description`)。
- 跑 `python3 -c` 脚本统计 `v1-shared-root-4workers/diag02-sibling-command-collision.jsonl` (570 行) 里 `assistant` 消息的 `tool_use` 事件: 命中两次 `Skill {'skill': 'openspec-archive-skill-2478f407', ...}` / `'openspec-archive-skill-e136a6c3'`, 均非本命令自己的 `-diag02` 后缀, 之后才 `Read` 自己的命令文件路径 —— 直接证实缺陷 (a) 「跨 worker 看到兄弟合成命令并被调用」在真实 transcript 里成立, 独立于 v1→v2 聚合分数。
- `diff run_arms.sh run_arms_v2.sh`: 确认 v1→v2 同时改了共享根→独立根 (`cd $S/trigger-proj` → 每臂 `$root=$S/trigger-proj-$name`) 与 `--num-workers 4` → `--num-workers 1`, 且从串行 (`run new; run old; ...`) 改成 `run new & run old & ... & wait` 并行四臂 (各自独立根)。
- `diff run_arms_v2.sh run_arms_v3.sh`: 确认唯一差异是 `--skill-path` 从 `/home/dev/Aria/aria/skills/openspec-archive` 换成 `.../scratchpad/neutral-skill` (`name: helper` 壳) + 输出目录改名, 其余 (num-workers/独立根/`--description` 显式覆盖) 逐字未变 —— 与 proposal.md D1/D3.2「v2→v3 只改中性名」的表述一致。
- 读 `neutral-skill-SKILL.md`: `name: helper`, `description` 复用 v3 的 `new` 臂原文; 结合 `run_arms_v3.sh` 的 `--description "$1"` override, 确认 `parse_skill_md` 只从这份壳取 `name`, 真正测的 description 来自命令行覆盖, 机制成立。
- 读 `claude-shim.sh` (`exec .../claude "$@" --setting-sources project`); 对照系统 init 事件里 `permissionMode:"default"`、`model` 字段显式传参不受 `--setting-sources` 影响, 未发现该 shim 会连带扰动 (a)/(b) 之外的行为面。
- 核对 `v1/v2/v3` 三个 `negctrl.json` 的 `summary.passed/failed` (10/10 → 19/1 → 13/7) 与 RESULT.md 记分表「负控 0/27/8 (should-trigger triggers/30)」互相能反推一致 (should-not 10 条全程 pass, 差值落在 should-trigger 侧), 未发现记分表与原始 JSON 矛盾。
- `find`/`ls` 核对 `trigger-proj-v3-*` 三个项目根目录内容: 均只含空 `.claude/`, 无其余文件 —— 印证第一条 finding「地板守卫只在完全空白根验证」的事实前提。
- `grep -rn skill-benchmark-exemption.md` 全文读: 确认 D1 落点引用 (`§2 SKILL.md 有变动时的附加约束`, 第 33 行) 存在且逐字对应; D4 引用的 `§4` (`与规则 #10 的关系`, 第 47-56 行) 无字段化模板, 支撑第二条 finding。
- `grep -rn "rule6_note"` 跨仓 (排除本 spec 自身与 archive) 抽样 20+ 处历史 spec/audit-report 用法, 确认均为散文/自由文本形态, 无先例证明 SOT 存在可"加栏"的结构化模板。
