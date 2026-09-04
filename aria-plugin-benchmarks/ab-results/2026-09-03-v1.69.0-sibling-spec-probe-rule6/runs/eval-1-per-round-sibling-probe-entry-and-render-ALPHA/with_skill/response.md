# audit-engine Round 2 入口推演 (convergence · post_planning · `openspec/changes/demo-spec/` · repo `/work/Demo`)

> 产出形态: 描述性推演。本文没有运行任何命令 (无 git / 无探针 / 无 agent spawn), 所有步骤都是按 `audit-engine/SKILL.md` + `references/execution-modes.md` + `references/report-format.md` + `references/convergence-algorithm.md` + `references/report-storage.md` 的规定推演「我在 Round 2 入口会做什么」。题面给定的探针 stdout 与 exit code 视为已发生的事实。

---

## 0. 前提与依据

| 项 | 值 | 依据 |
|---|---|---|
| checkpoint | `post_planning` (A.2, 质量保障, 调用方 task-planner) | SKILL.md 检查点列表 |
| mode | `convergence` | 题面 |
| 本轨 spec 目录名 | `demo-spec` (探针参数用**目录名**, 不是路径) | execution-modes.md `--own-spec-dir = 本轨 openspec/changes/<目录名> 的目录名` |
| repo root | `/work/Demo` | 题面; `--repo-path` 探针不假定 cwd |
| 当前位置 | Round 1 已结束, 进入 Round 2 **入口** | 题面 |
| Step 0 anchor | 已在 Round 1 启动前一次性固化, **审计周期内不可变**, Round 2 不重做、不 re-anchor | SKILL.md §Step 0 |
| per-round 探针 | **每轮入口**都跑 (Round 1, 2, …, N), 不沿用 Step 编号, 不复用上一轮结果 / 不复用 `remote_refresh` 缓存 | SKILL.md §per-round 入口探针; execution-modes.md §竞品 spec 探针 |

---

## 1. Round 2 入口步骤清单 (含完整命令行)

### 步骤 1 — 不重做 Step 0

Round 2 入口**不**重新固化 anchor, 也不做 mid-audit re-anchor (换锚 = 另起一次审计)。Round 1 固化的 `drift_metrics.anchor` 快照原样沿用。

### 步骤 2 — 入口第一动作: 跑竞品 spec 探针

在调用 agent-team-audit (spawn 任何 Agent) **之前**, 先跑探针。这是 Convergence 模式块 `Round N:` 的首行动作 (execution-modes.md §Convergence 模式 `每轮入口:` 行)。

完整命令行 (经 Bash 工具执行, 不 cd, 探针自己按 `--repo-path` 定位):

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/sibling_spec_probe.py" --own-spec-dir "demo-spec" --repo-path "/work/Demo"
```

参数核对:

- `--own-spec-dir "demo-spec"`: 自命中排除键, 传目录名。传成 `openspec/changes/demo-spec/` 会让脚本在 `repo/openspec/changes/openspec/changes/demo-spec/proposal.md` 找不到本轨 proposal → exit 2 → 「未能核实」, 白跑一轮。
- `--repo-path "/work/Demo"`: 仓库根。脚本先检查 `/work/Demo/.git` 存在, 再检查 `/work/Demo/openspec/changes/demo-spec/proposal.md` 存在。

我**不会**在探针之外自己另跑 `git fetch` / `git ls-remote` / 分支枚举: 探针自带 fetch (`--no-tags --prune`, 写进私有命名空间 `refs/aria/sibling-probe/<remote>/<branch>`, 不动 `refs/remotes/*`; 每个 git 子进程 30s, fetch 腿最多 2 次)。成本预期双远端约 25s/轮, 不称轻量; 题面本例 `elapsed_ms: 18342` (单远端 origin, 约 18s), 在预期范围内。git 原始 stderr 由探针吞掉不回显 (Rule #7), 我也不去 cat 任何 fetch 日志。

### 步骤 3 — 消费探针输出: fail-closed 三道门 + 读一等字段

按 execution-modes.md 「消费方 fail-closed 义务」逐道判定, 任一道不过 ⇒ 一律按 `not_established` 处置, 渲染「未能核实」, **禁止**渲染为「无竞品」:

| 门 | 本例取值 | 判定 |
|---|---|---|
| (a) exit code == 0 | `0` | 过。(非 0 语义: `2` = 非 git 仓 / 本轨 proposal 不存在 / 参数错; `3` = `extract_linked_issue_field` 不可导入; `1` = 探针内部异常, 此时 stdout 不保证是 JSON) |
| (b) stdout 可解析为恰一个 JSON 对象 | 题面逐字 JSON, 可解析 | 过 |
| (c) `schema_version == "1"` | `"1"` | 过 |
| (d) 读**一等字段** `verdict` (不从 `hits` 推断) | `"sibling_found"` | 走「🔴 检测到」档 |
| (e) `status` / `reason` | `"ok"` / `null` | 覆盖完整, **不**追加「(覆盖不完整: …)」后缀 |
| (f) N = 去重后 `spec_dir` 数 | `hits` 仅 1 项, `spec_dir = 2026-08-22-phase-c-integrator-ci-path-coverage`; 仅 1 个 remote (origin), 无镜像重复 | N = 1 |
| (g) M = `corpus == "archive"` 的项数 | 该项 `corpus: "archive"` | M = 1 → 标「已完成的 Spec」 |

顺带读取、用于措辞里的旁注 (不影响判定):

- `own_keys = [["k","aria-plugin",122]]`, `own_layer = "canonical"`: 本轨 demo-spec 的 linked-issue 字段是规范写法, 指向 `aria-plugin#122`。
- 命中项 `key = ["k","aria-plugin",122]` 与本轨键完全相等; 命中项 `layer = "url_fallback"` (对方 proposal 是经 URL 回退解析出同一 issue 的), `field_line: 22`, `refs: ["origin/master"]` (只在默认分支命中, 即已合入 master 的归档语料)。
- `remotes[0]`: `default_branch: master` 由 `ls_remote_symref` 解析 (非猜测), `error_kind: null`, `scanned: 149` 份 proposal, `refs_scanned: 3` 个分支, `capped: false`, `stale_skipped: 0`, `caps_applied: []` —— 与 `status: ok` 自洽。

### 步骤 4 — 渲染进当轮 `### Round 2` 记录, 并进聚合报告

把结果写成 report-format.md 模板行 `- Sibling probe:` (逐字见 §2)。落点只有两处: 当轮 `### Round 2` 记录 + 最终聚合报告的「轮次记录」节。

**不做的事** (由「不阻断」条款倒推):

- **不**把命中生成为 `conclusion_record` / 不分配 `severity` / 不进 `### Decisions / Issues / Risks`。否则它会多出一个四元组 `comparison_key`, 直接改变 R2 vs R1 的集合比较与 verdict 计数, 与「不改 verdict 计算、不改收敛判定」矛盾。
- **不**因命中阻断、暂停或改轮次路由; **不**弹 AskUserQuestion。
- **不**改 anchor / `in_scope` / `out_of_scope_hints`。
- **不**把探针结果注入 agent dispatch prompt。SKILL 与 references 都没有规定注入; 注入会改变审计输入面 (Agent 可能围绕「重复劳动」发散, 偏离 anchor)。这是我的处置判断而非成文条款, 如需复议应写进 handoff。

### 步骤 5 — 继续 Round 2 正文 (探针之后, 照 Convergence 模式块 1→4)

1. **调用 agent-team-audit 单轮引擎**: spawn `convergence_agents` (来源优先级 `agents_config` 参数 > `config.json audit.teams.post_planning` > 默认分组); 并发 `max_parallel: 2, hard_cap: 3`; 单 spawn 超时 120s, 整轮 wall-clock 300s。dispatch prompt **必须**嵌入 8-field frontmatter 模板原文 (agent-dispatch-contract, 防 #126 无 frontmatter 报告)。
2. **每个 Agent 报告落盘前**做 pre-write validation: `change_id = demo-spec` 须有 `openspec/changes/demo-spec/proposal.md` 或 `openspec/archive/*-demo-spec/proposal.md` 背书 (探针能走到 exit 0 已经旁证前者存在)。存储路径 `.aria/audit-reports/post_planning-R2-{timestamp_ms}-demo-spec-{agent_role}.md` (5-field uniqueness)。
3. **汇总引擎**: 合并 → `{category, scope}` 去重 (取最高 severity, 合并 found_by) → 同 scope 矛盾标 `conflicted: true` → 结构化提取为 conclusion_record (`id = sha256(category:scope:severity:type)[:8]`)。
4. **收敛判定** (`check_convergence`, Round 2 起可判): `keys_R2 == keys_R1` → `conclusions_stable`; 全员 `vote == PASS` → `unanimous`; drift 节点仅在 `audit.drift_guard.convergence_mode: true` 时存在 (convergence 模式默认不开; 若开, WARN 档强制 `unanimous=false`); 振荡检测此时 `normal_rounds` 长度 2 < 3, 不触发。
5. **路由**: `CONVERGED` → 计算 verdict → 生成聚合报告; 否则 `CONTINUE` → Round 3 (入口再跑一次探针) / `max_rounds` (默认 5) 耗尽 → 降级策略三路径。

---

## 2. 本轮审计报告里 `### Round 2` 记录的内容

模板 (report-format.md §完整报告模板 `### Round 2` 段) 逐行填充。Agent 侧字段 (Agents / Conclusions / Delta / Vote / Duration) 取决于本轮 Agent 实际输出, 推演中以占位符保留; `- Sibling probe:` 行是本题可确定的部分, 逐字如下:

```markdown
### Round 2
- Agents: {agent_list, 例 4/4}
- Sibling probe: 🔴 检测到 1 份同 issue 的竞品 Spec (含 1 份已完成的 Spec): 2026-08-22-phase-c-integrator-ci-path-coverage [archive → 已完成的 Spec; origin/master; 同 issue 键 aria-plugin#122 (本轨 canonical / 对方 url_fallback, proposal.md:22)]。覆盖完整 (status=ok; origin 默认分支 master 经 ls-remote symref 解析; 扫描 149 份 proposal / 3 个分支; 无 cap; 18.3s)。advisory, 不改 verdict / 收敛 / 路由。
- Conclusions: {count}
- Delta vs Round 1: +{added} / -{removed}
- Vote: {PASS/REVISE}
- Duration: {seconds}s
```

措辞来源核对:

- 「🔴 检测到 N 份同 issue 的竞品 Spec: <spec_dir 列表>」← execution-modes.md 三档表 `sibling_found` 行; 「(含 M 份已完成的 Spec)」← report-format.md 模板行的括注形态; 「已完成的 Spec」← `corpus == "archive"` 的强制标注。
- 无「(覆盖不完整: …)」后缀 ← `status == "ok"`。
- 方括号内的分支 / 键 / 层 / 行号是从 `hits[0]` 与 `remotes[0]` 抄的事实旁注, 便于 owner「一眼可辨」是不是同一件事; 不属于三档措辞本体, 删掉也不违反契约。

若 Round 2 就收敛 (成为末轮), 标题与字段按模板 `### Round N (Final)` 形态合并 (示例见 report-format.md PASS 输出示例 `### Round 2 (Final)`):

```markdown
### Round 2 (Final)
- Agents: {agent_list}
- Sibling probe: 🔴 检测到 1 份同 issue 的竞品 Spec (含 1 份已完成的 Spec): 2026-08-22-phase-c-integrator-ci-path-coverage [archive → 已完成的 Spec; origin/master; 同 issue 键 aria-plugin#122]
- Conclusions: {count}
- Delta vs Round 1: +{added} / -{removed}
- Converged: true
- Duration: {seconds}s
```

聚合报告其他位置: frontmatter **不新增**字段 (11/14 字段保持扁平, #125/#126 parser 防护); `## 审计结论` 三节**不**出现探针条目; 「统计」表不为探针加行。探针只活在「轮次记录」的每轮一行里 (Round 1 那行按 Round 1 当时的探针结果保留原样, 不回改)。

---

## 3. 这个探针结果对 verdict / 收敛判定 / 是否继续 Round 3 的影响

### 3.1 对 verdict: 零影响

`verdict = PASS (0 Critical + 0 Major) / PASS_WITH_WARNINGS (0 Critical + ≥1 Major) / FAIL (≥1 Critical)` (report-storage.md §Verdict 计算 SOT), 输入只有 Agent 结论的 severity 计数。探针命中不是 conclusion_record, 没有 severity, 不进计数; 也不是 `drift_terminated` 那种 override 通道。**同 issue 的已归档竞品 Spec 存在**这一事实, 不会把一份本来 PASS 的 post_planning 审计变成 PASS_WITH_WARNINGS 或 FAIL。

### 3.2 对收敛判定: 零影响

`converged = (keys_R2 == keys_R1) AND unanimous_pass` (+ 首轮 ∅ 的 stability 守卫), 全部取自 conclusion_record 四元组与 Agent 投票。探针结果:

- 不进 `comparison_keys` 集合 → 不影响 `conclusions_stable`;
- 不是 Agent 投票 → 不影响 `unanimous`;
- 不进 `normal_rounds` 的 keys 序列 → 不影响振荡检测;
- 不是 drift-checker 的分类对象 (`decisions ∪ objections`) → 不影响 `drift_ratio` / refocus / DRIFT_TERMINATED。

推论一: 即使 Round 1 的探针行是「未能核实 (原因: fetch_failed)」或「未发现同 issue 竞品」, 而 Round 2 变成「🔴 检测到 1 份」, 这个**探针行的跨轮变化不算结论不稳定, 不算振荡, 不延长审计**。这恰是「审计跨天时首轮结论会陈旧, 所以每轮重跑」设计的预期效果 —— 新鲜度靠每轮重取, 而不是靠把它纳入收敛条件。差异只在轮次记录里以两行不同措辞自然呈现, 可在 `## Verdict` 的 rationale 散文里点一句, 不改任何机读字段。

推论二: 若 Round 3 发生, 入口会**再跑一次**探针 (再花约 20s), 归档语料不会消失, 几乎必然再次 🔴 命中同一 `spec_dir`。重复出现是预期, 不是新信号, 也不触发任何升级处置。

### 3.3 对是否继续 Round 3: 零影响, 完全由 `check_convergence(R2, R1)` 决定

- `keys_R2 == keys_R1` 且全员 PASS (且若开了 drift guard, `drift_action != WARN`) → `CONVERGED`, Round 2 即末轮, 不进 Round 3。Round 2 满足 `round_number >= 2`, 所以即使 R1 = R2 = ∅ 也算收敛 (双轮稳定性确认已达成)。
- 否则 (集合有差 / 有 REVISE / WARN 档强制 `unanimous=false`) → `CONTINUE` → Round 3 (max_rounds 默认 5, 余量充足); 若开了 drift guard 且 `drift_action == REFOCUS` → `REFOCUS_ROUND` (R3-refocus, 消耗配额)。
- 探针在这条优先级链 (`CONVERGED → DRIFT_TERMINATED → OSCILLATION → MAX_ROUNDS_EXHAUSTED`) 里**没有任何分支**。

### 3.4 它真正影响的是什么: 一条给人看的 advisory 告警, 而且是最强的那一档

- 探针的定位是 advisory 副机制 (「同 issue」≠「重复劳动」, 命中是告警不是判决, 由人一眼可辨)。post_planning 本身在阻塞行为表里连 FAIL 都「继续 (仅记录)」, 探针更不可能阻塞。
- 但**信号本身很重**: `corpus == "archive"` + 只在 `origin/master` 命中 = 一份**已经 ship 并归档**的 Spec `2026-08-22-phase-c-integrator-ci-path-coverage` 曾经针对同一个 issue `aria-plugin#122` 做过事。这是 Spec §Why 里「对方已 ship 归档时, 只有语料通道能把『这件事别人做完了』摆到台面上」的那类情形 —— 认领 (claim) 通道对已归档 Spec 天然失明, 此处正是这条通道存在的理由。
- 时点也对: post_planning = A.2 任务规划刚完成、Phase B 尚未开工, 是最便宜的停下来核对的时刻。
- 我在 Round 2 入口能做的处置到此为止: 把 🔴 行写清楚 (spec_dir / 已完成 / 键 / 分支), 让 caller (task-planner) 与 owner 在读报告时自行裁定 demo-spec 是「重复已 ship 的工作 (应收窄或撤回)」还是「有意拆分的同族 sibling (如 `#137` 簇, 继续)」。**这是产品级裁定, 不由 audit-engine 代做**; 我不会把它升级成 finding、不会改 verdict、不会阻断 Round 2, 也不会自作主张去读那份归档 proposal 做「是否重复」的技术级判断 (那超出 post_planning 审计的 anchor 与 scope)。

### 3.5 一句话总结

Round 2 入口: 先跑 `python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/sibling_spec_probe.py" --own-spec-dir "demo-spec" --repo-path "/work/Demo"`, exit 0 + JSON + `schema_version "1"` + `verdict sibling_found` + `status ok` ⇒ 在 `### Round 2` 写一行「🔴 检测到 1 份同 issue 的竞品 Spec (含 1 份已完成的 Spec): 2026-08-22-phase-c-integrator-ci-path-coverage」; 然后照常 spawn Agent、汇总、按四元组 + 全票判收敛。探针对 verdict、收敛、Round 3 路由三者**都不施加影响**, 它影响的是人: 一份已归档的同 issue Spec 摆上了台面, 由 owner 决定 demo-spec 是重复还是有意 sibling。
