# 场景 4 基线实跑 — description 触发率评测对 openspec-archive 两版 description 的区分力 (10CG/Aria#211)

| 字段 | 值 |
|---|---|
| 跑于 | 2026-09-13 (三轮: v1 / v2 / v3, 见下) |
| 目的 | `10CG/Aria#211` 验收第 1–3 条: 在把「description 变动 ⇒ 跑场景 4」写进 Rule #6 之前, 先实跑证明场景 4 (a) 对真实 description 变动区分力非零, (b) 负控 (删光触发词) 显著下降 |
| 工具 | skill-creator `scripts/run_eval.py` (插件缓存 `claude-plugins-official/skill-creator/bb335391eb83`), Claude Code 2.1.269 |
| 模型 | `claude-fable-5-1` (显式传 `--model`, 与本 session 一致; skill-creator 指引) |
| 套件 | `trigger-eval-openspec-archive.json` — 20 query: 10 should-trigger / 10 should-not (近似误触为主: git 分支归档 / handoff 归档 / 起新 spec / openspec CLI 口径 / Archive Tracker 单 / tar 归档 / 改 Status / state-scanner / archive 重组 / changelog 归档) |
| 每 query | 3 runs, `trigger_threshold=0.5`, `timeout=120s` |
| 四臂 | **new** = v1.73.0 (= 当前 master) description · **old** = v1.71.1 description · **negctrl** = 删光触发词「对一个已完成的事项做收尾处理，并核对处理结果。」 · **poscontrol** = 「pushy」版 (显式列出触发短语 + 「都必须使用本技能」) |
| 隔离 | `claude` 垫片追加 `--setting-sources project`, 临时项目根 (空 `.claude/`): 用户级 27 个插件不加载 (`claude -p` 自报技能数 97 → 13, 真 `aria:openspec-archive` 不在列), 单次成本 0.54 → 0.06 美元 |

## 记分 (should-trigger 命中 / 30; should-not 四臂三轮全部 0/30)

| 轮 | 配置 | new | old | negctrl | poscontrol | 结论 |
|---|---|---|---|---|---|---|
| v1 | 共用项目根, `--num-workers 4`, 合成名 `openspec-archive-skill-<id>` | 4 | 7 | 0 | 6 | **地板**: 四臂都被压到 ≤ 23% |
| v2 | 每臂独立项目根, `--num-workers 1`, 合成名不变 | 27 | 30 | 27 | 30 | **天花板 + 名字泄漏**: 负控也 27/30 |
| v3 | 同 v2 + 合成名中性化 (`name: helper`) | **30** | **30** | **8** | **30** | **有效轮**: 负控显著下降, 三个真 description 打平 |

v3 Fisher 精确检验 (n=30 vs 30): new vs old p = 1.0; poscontrol vs new p = 1.0; new vs negctrl **p < 0.0001**; old vs negctrl **p < 0.0001**。

## 三个结论

1. **对本次真实 description 变动 (v1.71.1 → v1.73.0, 删「自动修正 CLI bug」改「并做归档后落点校验」) 区分力为零** —— 两版都 30/30, 「pushy」正控也 30/30。在这套 20 条 query 上, 只要 description 里还有「归档 / OpenSpec / Spec」这一族词, 触发就饱和。⇒ 按 `10CG/Aria#211` 验收第 2 条, **场景 4 不能作为「description 措辞改动有没有变好」的 A/B 工具写进 Rule #6** —— 那是又一个测量剧场。
2. **场景 4 能抓「把 description 毁掉」**: 负控 8/30, 与三个真 description 的差距 p < 0.0001; should-not 全程 0/30 (无误触)。⇒ 它可以当**地板守卫** (触发面没被改坏), 不能当区分力尺子。
3. **skill-creator `run_eval.py` 有两处结构性缺陷, 不修正则场景 4 的数字没有意义**:
   - (a) **并发 worker 互见**: `--num-workers N > 1` 时 N 个 `claude -p` 共用同一 `.claude/commands/`, 各自看到 N 个同 description、不同 `<id>` 的合成技能, 随机选一个; 检测只认本 run 自己的 `<id>` ⇒ 命中率被压到约 1/N。实证: v1 (4 worker) 4–7/30 vs v2 (1 worker) 27–30/30; 直接证据 `v1-shared-root-4workers/diag02-sibling-command-collision.jsonl` —— 手动跑的 query 调用了兄弟 run 的 `openspec-archive-skill-2478f407` / `…-e136a6c3`, 而不是自己的。
   - (b) **合成命令名泄漏意图**: 命令文件名 = `<skill_name>-skill-<id>`, 技能名 `openspec-archive` 本身就回答了 query ⇒ description 被架空。实证: v2 负控 (零触发词) 27/30; v3 只把 `name` 改成 `helper`, 负控掉到 8/30。
   - (c) 附带: 默认设置源下 `claude -p` 加载全部用户级插件 (97 个技能, 含真 `aria:openspec-archive` 与合成技能竞争), 单次 0.54 美元; 加 `--setting-sources project` 后 13 个、0.06 美元。

## 对 Rule #6 处方的含义 (供 spec `rule6-description-change-trigger-eval-lane` 引用)

- 第二行「description 变动 ⇒ 照跑场景 1」的证据面确实为空 (`10CG/Aria#211` 原命题成立, 场景 1 两臂被直接喂 SKILL.md 路径)。
- 补上场景 4 **只能补成地板守卫**: 「should-trigger 触发率不低于阈值 且 should-not 为 0」, 而不是「新版触发率 ≥ 旧版」—— 后者在真实措辞改动上恒打平, 写成判据会恒绿。
- 场景 4 的运行前置必须成文: 每臂独立项目根 + 单 worker (或修 run_eval.py) + 合成名中性化 + `--setting-sources project` + 显式 `--model`; 缺任一条, 数字不可解读。

## 原始产物

- `trigger-eval-openspec-archive.json` — 20 条 query (should / should-not 各 10)
- `v1-shared-root-4workers/` · `v2-isolated-root-1worker/` · `v3-isolated-root-1worker-neutral-name/` — 各含四臂 `*.json` (run_eval 原始输出, 每 query 的 `trigger_rate` / `triggers` / `runs` / `pass`) + `run.log`
- `run_arms.sh` / `run_arms_v2.sh` / `run_arms_v3.sh` — 三轮的运行脚本 (逐字可重跑; 路径指向 scratchpad, 重跑时改 `S=`)
- `claude-shim.sh` — 注入 `--setting-sources project` 的垫片; `neutral-skill-SKILL.md` — v3 的中性名 skill 壳
- `manifest.json` — v1 时写的运行清单 (v2/v3 差异见上表)

## 已知局限

- 20 条 query 是本 session 按 skill-creator 指引编写, **未经 owner 审阅** (skill-creator Step 2 要求 HTML 审阅; 本轮 owner 不在线, 已如实登记, 见 handoff)。should-trigger 条目可能整体偏「清楚」, 这是天花板的一个可能来源; 但负控仍能显著下降, 说明套件对「有没有触发词」敏感。
- 只测了一对真实 description。结论 1 是「这一对零区分力」+「机制上小措辞改动很难在饱和套件上显形」, 不是「任何 description 改动都测不出」。
- run_eval 判「触发」= **第一个** tool_use 是本合成技能 (Skill 或 Read); 探索式开局 (先 `ls`) 会被判未触发。v3 里 30/30 说明在隔离项目根下这条严格判据没有压低命中, 但在真实项目根 (有文件可探索) 下未验证。
