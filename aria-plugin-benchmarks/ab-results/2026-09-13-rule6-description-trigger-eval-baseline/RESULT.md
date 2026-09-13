# 场景 4 基线实跑 — description 触发率评测对 openspec-archive 两版 description 的区分力 (10CG/Aria#211)

> **本文件版本**: 2 (2026-09-13, post_spec R1 rework: 并入 v4 反事实两臂 / query 级统计 / 负控分布勘正 / 机读探针证据)。**引用方请写「RESULT.md v2 @ <提交 SHA>」**; 本文件修订时版本号递增, 引用了旧版本数字的文本须重核。

| 字段 | 值 |
|---|---|
| 跑于 | 2026-09-13 (四轮: v1 / v2 / v3 / v4, 见下) |
| 目的 | `10CG/Aria#211` 验收第 1–3 条: 在把「description 变动 ⇒ 跑场景 4」写进 Rule #6 之前, 先实跑证明场景 4 (a) 对真实 description 变动区分力非零, (b) 负控 (删光触发词) 显著下降 |
| 工具 | skill-creator `scripts/run_eval.py` (插件缓存 `claude-plugins-official/skill-creator/bb335391eb83`; 该 hash 随插件更新漂移, 重跑时按 `find ~/.claude/plugins -path '*skill-creator*' -name run_eval.py` 重新定位), Claude Code 2.1.269 |
| 模型 | `claude-fable-5-1` (显式传 `--model`, 与本 session 一致; skill-creator 指引) |
| 套件 | `trigger-eval-openspec-archive.json` — 20 query: 10 should-trigger / 10 should-not (近似误触为主)。**未经 owner 审阅** (skill-creator Step 2 要求 HTML 审阅; 本轮 owner 不在线), 见 Spec OQ-3 |
| 每 query | 3 runs, `trigger_threshold=0.5` (3 runs 下即 ≥ 2/3), `timeout=120s` |
| 臂 | **new** = v1.73.0 (= 当前 master) description · **old** = v1.71.1 description · **negctrl** = 删光领域词「对一个已完成的事项做收尾处理，并核对处理结果。」 · **poscontrol** = 「pushy」版 (显式列触发短语 + 「都必须使用本技能」) · **overbroad** (v4) = 过宽版 (触发词覆盖 openspec / 归档 / 整理 / 收尾 / issue / 分支 等) · **realroot** (v4) = new description, 但项目根含 11 个 `openspec/changes/*/proposal.md` 等可探索文件 |
| 隔离 | `claude` 垫片追加 `--setting-sources project`, 临时项目根 (空 `.claude/`)。机读证据 `probe-setting-sources-default.json` / `probe-setting-sources-project.json` (同一探针 query, `--model claude-fable-5-1`): 默认设置源自报 **97** 个技能且含 `openspec-archive` (`total_cost_usd` 0.604); project-only 自报 **12** 个且不含 (0.079) |

## 记分 (should-trigger 命中 / 30; should-not 命中 / 30)

| 轮 | 配置 | 臂 | should | should-not | 说明 |
|---|---|---|---|---|---|
| v1 | 共用项目根, `--num-workers 4`, 合成名 `openspec-archive-skill-<id>` | new / old / negctrl / poscontrol | 4 / 7 / 0 / 6 | 0 / 0 / 0 / 0 | **地板**: 四臂全被显著压低 |
| v2 | 每臂独立项目根, `--num-workers 1`, 合成名不变 | new / old / negctrl / poscontrol | 27 / 30 / 27 / 30 | 0 / 0 / 0 / 0 | **天花板 + 名字泄漏**: 负控也 27/30 |
| v3 | 同 v2 + 合成名中性化 (`name: helper`) | new / old / negctrl / poscontrol | **30 / 30 / 8 / 30** | 0 / 0 / 0 / 0 | **有效轮** |
| v4 | 同 v3 | overbroad | 30 | **22** (query 级 7/10 判红) | should-not 的 FAIL 分支可达 |
| v4 | 同 v3, 项目根含 11 个 spec 目录等文件 | realroot (new desc) | 30 | 0 | 「第一个 tool_use」判据在非空根下未失真 |

### 统计 (v3, 两种单元都给)

同一 query 的 3 次 run 不是独立样本 (伪重复), **独立单元是 query (n=10)**; run 级 (n=30) 只作参考。

| 比较 | run 级 n=30 双侧 Fisher | query 级 n=10 (命中 = `trigger_rate ≥ 0.5`) 双侧 Fisher |
|---|---|---|
| new (30 / 10) vs old (30 / 10) | p = 1.0 | p = 1.0 |
| poscontrol (30 / 10) vs new | p = 1.0 | p = 1.0 |
| new vs negctrl (8 / 3) | p < 0.0001 | **p = 0.0031** |
| old vs negctrl | p < 0.0001 | p = 0.0031 |

负控 8/30 的分布 (勘正: v1 版本文写「两条 3/3」漏计一条 2/3): 集中在 3 条 query —「周期收尾: spec … 落点校验」3/3、「…标记为已完成并放到归档目录, 记得归档后要检查…」2/3、「D.2 归档 + 落点校验」3/3; 其余 7 条 0/3。这 3 条都含「收尾 / 核对 / 校验」动作语义 ⇒ 负控删净了领域词 (归档 / OpenSpec / Spec), **没删净通用动作词** (「收尾」「核对」仍在负控 description 里)。

## 结论

1. **对本次真实 description 变动 (v1.71.1 → v1.73.0) 区分力为零**: new / old / poscontrol 三臂 should-trigger 全部 30/30 (query 级 10/10), p = 1.0。在这 20 条 query 上, 只要 description 含「归档 / OpenSpec / Spec」一族词, 触发就饱和。⇒ 这是**饱和** (三臂都撞天花板, 测不出差异), 不是「无差异」的证明; 在饱和处, 任何「新版 ≥ 旧版」类比较判据退化为以噪声为参照 (负控 8/30 对旧版 30/30 仍会判红, 所以它不是恒绿; 但对任何两个真 description 都打平)。⇒ 按 `10CG/Aria#211` 验收第 2 条, **场景 4 不能作为「description 措辞改动有没有变好」的 A/B 工具**。
2. **场景 4 能当地板守卫, 两个方向都验过**: 负控 (删领域词) should-trigger 掉到 8/30 (query 级 p = 0.0031); 过宽 description 让 should-not 涨到 22/30 (7/10 条判红)。⇒ 「should-trigger 全部 ≥ 0.5 且 should-not 全部 < 0.5」这条门两侧都有真实 FAIL 样本, 不是恒绿门。
3. **skill-creator `run_eval.py` 两处结构性缺陷 + 一处配置建议**, 不按前置运行数字不可解读:
   - (a) **并发 worker 互见**: `--num-workers N > 1` 时 N 个 `claude -p` 共用同一 `.claude/commands/`, 各自看到 N 个同 description、不同 `<id>` 的合成技能; 检测只认本 run 自己的 `<id>`。实证: v1 (共用根 + 4 worker) 4–7/30 vs v2 (独立根 + 1 worker) 27–30/30 —— **注意 v1→v2 同批改了两个变量**, 记分表本身分不开; 机制证据是 `v1-shared-root-4workers/diag02-sibling-command-collision.jsonl`: 手动跑的 query 调用了兄弟 run 的 `openspec-archive-skill-2478f407` / `…-e136a6c3` 而不是自己的 (init 事件同时列出多个兄弟命令)。压低幅度**定性为「显著」, 不定量**为 1/N (v1 负控 0/30 与 1/4 期望不符)。
   - (b) **合成命令名泄漏意图**: 命令文件名与正文 = `<skill_name>-skill-<id>` / `# <skill_name>`, 技能名 `openspec-archive` 本身就回答了 query ⇒ description 被架空。实证: v2 负控 (零领域词) 27/30; v3 只把 `name` 改成 `helper` (run_arms_v2.sh 与 run_arms_v3.sh 仅差 `--skill-path` 与目录名), 负控掉到 8/30。
   - (c) 配置建议: 默认设置源下 `claude -p` 加载全部用户级插件 (97 个技能, 真 `aria:openspec-archive` 与合成技能竞争), 加 `--setting-sources project` 后 12 个; 单次成本 0.60 → 0.08 美元 (探针 json)。该开关会同时改掉默认模型 (用户级 model 设置不再加载), 所以必须**显式 `--model`** —— 这半条是配置推导, 三轮未对照实测。

## 对 Rule #6 处方的含义 (供 spec `rule6-description-change-trigger-eval-lane` 引用)

- 第二行「description 变动 ⇒ 照跑场景 1」的证据面确实为空 (issue 原命题成立: 场景 1 两臂被直接喂 SKILL.md 路径)。
- 补上场景 4 **只能补成地板守卫**: 判据 = `run_eval.py` 的 `pass` 全真 (每条 should ≥ 0.5, 每条 should-not < 0.5), 外加同批负控 query 级显著低于被评 description; **不设**「新版 ≥ 旧版」比较判据 (在饱和处退化)。
- 运行前置必须成文 (每条对应本目录一个机读产物): 独立项目根 + 单 worker (v1 vs v2 + diag02) / 合成名中性化 (v2 vs v3, `neutral-skill-SKILL.md`) / `--setting-sources project` (probe 两份 json) / 显式 `--model` (配置推导) / 同批负控 (v3 negctrl) / 产物形状 (本目录)。

## 原始产物

- `trigger-eval-openspec-archive.json` — 20 条 query (should / should-not 各 10)
- `v1-shared-root-4workers/` · `v2-isolated-root-1worker/` · `v3-isolated-root-1worker-neutral-name/` · `v4-counterfactuals/` — 各臂 `*.json` (run_eval 原始输出, 每 query 的 `trigger_rate` / `triggers` / `runs` / `pass`) + `run.log` (各臂起止时间)
- `run_arms.sh` / `run_arms_v2.sh` / `run_arms_v3.sh` / `run_arms_v4.sh` — 四轮运行脚本 (变量 `S=` 指向当时的 scratchpad, 重跑时改它; 各臂 description 原文在脚本里)
- `claude-shim.sh` — 注入 `--setting-sources project` 的垫片; `neutral-skill-SKILL.md` — v3/v4 的中性名 skill 壳
- `probe-setting-sources-default.json` / `probe-setting-sources-project.json` — 技能数与单次成本的机读证据
- `manifest.json` — v1 时写的运行清单 (v2–v4 差异见本文表格; 保留原样作历史)

## 时长与成本

- 时长 (run.log): 单 worker 一臂 60 次调用 10m39s–13m54s; v3 四臂并行 12 分钟内全完; 两臂 (被评 + 负控) 并行约 12–14 分钟, 串行约 24 分钟。
- 成本: `run_eval.py` 不记录成本; 按探针单次 0.08 美元估, 两臂 120 次约 10 美元 (估算, 非实测)。

## 已知局限

- 20 条 query 未经 owner 审阅; should-trigger 整体偏「清楚」是天花板的一个可能来源。负控与过宽两臂仍能显著变化, 说明套件对「触发词有没有」敏感。
- 只测了一对真实 description; 结论 1 是「这一对零区分力 + 机制上小措辞改动很难在饱和套件上显形」, 不是「任何 description 改动都测不出」。
- 负控没删净通用动作词 (见统计段); 若要更干净的负控, 应删到只剩「处理一件事项」级。
- `run_eval.py` 判「触发」= 第一个 tool_use 就是本合成技能 (Skill 或 Read); v4 realroot 在含 11 个 spec 目录的项目根下 30/30, 但更大的真实仓 (如 Aria 主仓, 有 CLAUDE.md 与数百文件) 未验证。
- 本轮 owner 不在线; 「未经审阅」等流程判断记入本 session 的 handoff (`docs/handoff/`, 与本文件同批提交)。
