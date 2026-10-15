# audit-engine Round 2 入口 — 描述性推演 (descriptive)

**场景参数**: convergence 模式 | checkpoint = `post_planning` | spec 目录 `openspec/changes/demo-spec/` | repo root `/work/Demo` | Round 1 已结束, 进入 Round 2 入口。
**产出形态声明**: 本文为描述性推演, 未实际执行任何命令 (含探针本身; 其 stdout 按题设逐字采信, exit code 0)。

**前置事实回顾** (Round 1 已结束时引擎持有的状态):

- Step 0 anchor 已在 Round 1 启动前一次性固化 (proposal 类 checkpoint 的 anchor 来源 = `demo-spec/proposal.md` 的 Why/Goal 段), 写入报告 body `drift_metrics.anchor`, **审计周期内不可变** —— Round 2 入口**不重做** anchor 固化, 也不存在 mid-audit re-anchor。
- Round 1 的 `round_state` 已落: `round: 1` + conclusions (含 finding 8-char ID) + comparison_keys 集合 + vote + timestamp; Round 1 无前序轮 ⇒ 判定只能返回 CONTINUE (若 R1 为 ∅, 同样强制进入 Round 2 作 stability confirmation, 不视为收敛)。
- Round 1 入口也跑过一次竞品探针 (每轮入口含 Round 1); Round 2 入口**重跑**, 不复用上一轮结果、不复用 `remote_refresh` 缓存 (审计跨天时首轮结论会陈旧)。

---

## (1) Round 2 入口执行的步骤清单 (含完整命令行)

### Step A — 每轮入口: 竞品 spec 探针 (Round 2 入口唯一规定的 shell 命令)

Convergence 模式围栏块内逐字调用串 (`references/execution-modes.md` `## Convergence 模式` Round N 第 1 行; 与 Challenge 块同字面, SC-17 机械护栏计数恰 2):

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/sibling_spec_probe.py" \
  --own-spec-dir "demo-spec" \
  --repo-path "/work/Demo"
```

- `--own-spec-dir` = 本轨 spec 目录名 (自命中排除键); `--repo-path` = `/work/Demo` (探针不假定 cwd)。
- `${CLAUDE_PLUGIN_ROOT:-aria}`: 经 Plugin 安装时取环境变量绝对路径; Aria 仓内直调时回退相对前缀 `aria/skills/...`。
- 本命令即 Round 2 入口的**全部** shell 命令面: completeness gate 是 `pre_merge` 专属且不随 Round 重跑 (本 checkpoint 为 `post_planning`, 不跑); agent dispatch 经 agent-team-audit 的 Agent spawn 走 Agent 工具非 shell; 探针自身的 fetch (`--no-tags --prune` 进私有命名空间 `refs/aria/sibling-probe/<remote>/<branch>`, 不动 `refs/remotes/*`) 是脚本内部行为, 不是我另行发出的命令。

题设采信其 stdout 逐字为给定 JSON、exit 0。作为消费方, 按契约依序做:

1. **fail-closed 三查**: exit == 0 ✓ → stdout 可解析为单一 JSON 对象 ✓ → `schema_version == "1"` 为已知值 ✓。三项任一不满足都要按 `not_established` 渲染「未能核实」; 本例全部通过, 不走该分支。
2. **读一等字段 `verdict`** (不从 `hits == []` 反推结论 —— 「扫完没有」与「没扫到」在 `hits` 上取值相同): `verdict == "sibling_found"`。
3. **措辞选择所需的旁证读取**: `status == "ok"` (remotes[].error_kind 全 null、capped=false、caps_applied=[] 自洽; `reason: null` 在 status==ok 且 verdict!=not_established 时合法) ⇒ **不追加**「(覆盖不完整: <reason>)」后缀 (该后缀仅 `status == "degraded"` 时追加; 正证据不因覆盖不完整而降级, 但本例无缺口)。`hits` 恰 1 项, 去重后 `spec_dir` 数 **N = 1** (同一 Spec 在双镜像各成一条 hits 项时计数须去重; 本例单 remote 单条)。命中项 `corpus == "archive"` ⇒ 须标注**「已完成的 Spec」**。
4. **渲染**进当轮 `### Round 2` 记录的 `- Sibling probe:` 行 (见 (2)), 并进聚合报告。

### Step B — 探针结果不阻断, 直接进入 Round 2 审计本体

探针是 advisory 副机制: 不改 verdict 计算、不改收敛判定、不改轮次路由。渲染完成后即继续, 不因 🔴 停轮、跳轮或改派。

### Step C — Drift check 分支 (#17, 条件性)

convergence 模式下 drift guard 非默认: 仅当 `.aria/config.json` 的 `audit.drift_guard.convergence_mode == true` (opt-in) 时, Round 2 起 (Round 1 有 Round-1 guard, 跳过 drift 计算) 每轮收敛判定前 spawn 独立 drift-checker, 持不可变 anchor 对当轮结论分类 → `drift_ratio` → 三档处置 (NONE/WARN/REFOCUS/TERMINATE; 独立 30-60s 超时配额, 不占 300s/轮)。drift-checker 失败/超时 ⇒ fail-open: `drift_ratio=null` 按 `< warn` 档处理 + `drift_check_skipped: true`, `consecutive_refocus_count` 不增加。未 opt-in (默认) 则本分支整体不激活, 报告无 `drift_metrics` 章节义务。

### Step D — 调用 agent-team-audit 单轮引擎 (Round 2 的步骤 1)

- spawn `post_planning` 的 convergence_agents 分组 (取参优先级: `agents_config` 参数 > config `audit.teams[post_planning]` > 默认分组); 单轮并发 max_parallel 2 / hard_cap 3; 单 spawn 超时 120s; 每轮 300s wall-clock 独立计时。
- 各 Agent 独立分析 `openspec/changes/demo-spec/` 的 tasks 产物, 返回原始 issues 列表。
- **dispatch 契约 (v1.30.1+, 不可协商)**: 每个 agent prompt 原文嵌入 8-field YAML frontmatter template (checkpoint/mode/rounds/converged/oscillation/overridden_by_user/degraded/verdict/timestamp/context/agents —— 逐字模板见 `references/agent-dispatch-contract.md`), 并**无条件追加**三个 drift 字段默认 false (`drift_terminated` / `drift_check_skipped` / `is_refocus`); dispatch 时已知字段注入实值 —— Round 2 为 normal 轮, `is_refocus: false` (若上一轮 `drift_check_skipped` 为 true 亦注入)。`rounds` 填当前轮号 2。drift-checker 是 audit-engine 内部调用, 不适用本 8-field 契约。

### Step E — 汇总引擎 (Round 2 的步骤 2)

合并所有 Agent 输出 → 按 `{category, scope}` 去重 (合并 `found_by`, 取最高 severity) → 同 scope 矛盾意见保留双方并标 `conflicted: true` (不自动裁决) → 结构化提取为 conclusion_record (`id = sha256(category:scope:severity:type)[:8]`, summary 截 50 词不参与哈希)。Agent spawn 失败/超时 ⇒ 跳过该 Agent, 当轮 `incomplete: true`, 不阻塞收敛; 全部失败 ⇒ 当轮作废不计入 max_rounds。

### Step F — 收敛判定 (Round 2 的步骤 3)

- **四元组集合比较**: `keys_2 == keys_1` (严格集合相等; 单元素差异/severity 升级均不收敛)。
- **∅ 双轮稳定性 gate**: 若 `keys_2 = ∅ ∧ keys_1 = ∅ ∧ round >= 2` ⇒ 允许收敛; Round 1 = ∅ 本就强制进了 Round 2 作 stability confirmation。
- **振荡检测**: 需 `len(normal_rounds) >= 3`, Round 2 时 normal 序列长度仅 2 ⇒ 结构上不可达, 不检查。
- **全票 PASS**: `convergence_agents` 全员 vote == PASS (skipped Agent 不参与投票)。
- (若 Step C 激活且 drift_action == WARN) convergence 模式特有分支: 强制 `unanimous = false`, 该轮不允许全票 PASS 收敛 —— 实现点限汇总层, 不注入 agent prompt。

### Step G — 路由 (Round 2 的步骤 4)

按四终局优先级链 `CONVERGED → DRIFT_TERMINATED → OSCILLATION → MAX_ROUNDS_EXHAUSTED` (Round 2 处 OSCILLATION 不可达):

- `conclusions_stable AND unanimous` ⇒ **CONVERGED**: 按 Critical/Major 计数出 verdict, 生成审计报告 (R2 即 `### Round 2 (Final)`), 不进 Round 3。
- drift TERMINATE (连续 2 次 refocus, 仅 Step C 激活时可达) ⇒ `drift_terminated: true → verdict=FAIL` override, 不触发降级三路径。
- drift REFOCUS ⇒ 下一轮为 R3-refocus (消耗 max_rounds 配额, 输出替换 stability 基线)。
- 未收敛 + `2 < max_rounds` ⇒ **CONTINUE → Round 3** (Round 3 入口**再次**重跑 Step A 探针)。
- `round_N.number >= max_rounds` 未收敛 ⇒ **MAX_ROUNDS_EXHAUSTED** → 降级策略: AskUserQuestion 三路径 ([1] 接受当前结论 `overridden_by_user: true` / [2] `max_rounds += 2` 续跑 / [3] 降级单轮 `degraded: true`)。

报告按 5-field uniqueness schema 落盘 `.aria/audit-reports/post_planning-R2-{timestamp_ms}-{spec_id}-{agent_role}.md`; 写盘前过 change_id 锚点校验 (`demo-spec` 有 `openspec/changes/demo-spec/proposal.md` 背书, 通过)。

---

## (2) 本轮审计报告 `### Round 2` 记录的内容

按 `references/report-format.md` 轮次记录模板。探针行是本问核心, 逐字给出; 其余行为推演占位 (Round 2 实际数值由当轮 Agent 输出决定):

**形态一 — Round 2 非终轮 (之后还有 Round 3):**

```markdown
### Round 2
- Agents: {agent_list}
- Sibling probe: 🔴 检测到 1 份同 issue 的竞品 Spec: 2026-08-22-phase-c-integrator-ci-path-coverage (已完成的 Spec)
- Conclusions: {count}
- Delta vs Round 1: +{added} / -{removed}
- Vote: {PASS/REVISE}
- Duration: {seconds}s
```

**形态二 — Round 2 即终轮 (R2 收敛/终局):**

```markdown
### Round 2 (Final)
- Agents: {agent_list}
- Sibling probe: 🔴 检测到 1 份同 issue 的竞品 Spec: 2026-08-22-phase-c-integrator-ci-path-coverage (已完成的 Spec)
- Conclusions: {count}
- Converged: {true/false}
- Duration: {seconds}s
```

`- Sibling probe:` 行的推导依据 (消费措辞三档中取 `sibling_found` 档):

- **N = 1**: hits 去重后 `spec_dir` 恰 1 个 (`2026-08-22-phase-c-integrator-ci-path-coverage`); 计数按 spec_dir 去重, 不按 hits 条数。
- **「已完成的 Spec」标注**: 唯一命中项 `corpus == "archive"` (`path = openspec/archive/2026-08-22-phase-c-integrator-ci-path-coverage/proposal.md`) ⇒ 命中的是 `archive/` 语料, 语义为对方轨已 ship 并归档。命中键 `["k","aria-plugin",122]` 与本轨 `own_keys` 的 canonical 键相同 (对方 proposal 走 `url_fallback` 层, 第 22 行 URL 归一化后与本轨 canonical token 撞同一 issue 键)。
- **无 degraded 后缀**: `status == "ok"` ⇒ 不追加「(覆盖不完整: <reason>)」; 若是 `degraded` 则必须追加 (正证据不因覆盖不完整降级, 缺口用 reason 说明)。
- **未走另两档**: `no_sibling_found` 档措辞「本轮已完整扫描, 未发现同 issue 竞品」与 `not_established` 档措辞「未能核实 (原因: <reason>)」均不适用 —— 本例 exit 0、JSON 可解析、schema_version 已知、verdict 一等字段为 `sibling_found`。
- 该行同时进入**聚合报告** (不只在单轮记录); 报告模板的聚合写法 `🔴 检测到 N 份同 issue 的竞品 Spec (含 M 份已完成的 Spec)` 在本例即 N=1、M=1, 与上面的逐 spec_dir 列表写法同义。
- 若 Step C 激活, 报告 body 的 `drift_metrics.per_round` 另有 Round 2 条目 (on_topic/adjacent/off_topic 计数 + `drift_ratio`; R1 条目为 `drift_ratio: null` 跳过计算) —— 与 Sibling probe 行互不相干。

---

## (3) 探针结果对本轮 verdict / 收敛判定 / 是否继续 Round 3 的影响

**结论先行: 三项均零影响 —— 探针是 advisory 副机制, 「不阻断」是契约条款, 不是裁量。**

1. **对 verdict: 无影响。** verdict 由末轮去重后结论的 severity 计数机械得出 (0 Critical + 0 Major ⇒ PASS; 0 Critical + ≥1 Major ⇒ PASS_WITH_WARNINGS; ≥1 Critical ⇒ FAIL; 唯一 override 是 #17 的 `drift_terminated: true → FAIL`, 与探针无关)。探针命中**不进入** conclusion_record —— 它没有 type/severity/category/scope 四元组, 不是 finding, 结构上连间接污染 comparison_keys 或 severity 统计的通道都不存在, 也不写入 frontmatter 任何字段。
2. **对收敛判定: 无影响。** `converged = conclusions_stable AND unanimous_pass` (含 ∅ 双轮稳定性 gate; convergence+drift-WARN 时强制 `unanimous=false`)。判定输入 = R2/R1 四元组集合 + agent 投票 (+ opt-in 时的 drift_ratio); 探针结果不在输入集内。🔴 不会把收敛判成不收敛, 也不会反过来。
3. **对是否继续 Round 3: 无影响。** 路由只看 Step F/G 的四终局优先级链: R2 未收敛且 `2 < max_rounds` ⇒ 照常进 Round 3 (且 Round 3 入口**重跑**探针 —— 每轮重跑, 跨天陈旧性是设计动机之一); R2 收敛 ⇒ 照常出终版报告, 🔴 行留在报告里, 不因它多发一轮或提前停轮。同样不存在「探针失败 (not_established/exit≠0) ⇒ 中止」的反向分支 —— 那只改渲染措辞为「未能核实」。

**它的实际作用面是信息通道, 服务于人**: 「同 issue」≠「重复劳动」(#137 簇是有意拆分的先例), 命中是**告警不是判决**。本例的告警内容相当具体 —— 与 `demo-spec` 共享 issue 键 `aria-plugin#122` 的 Spec **已由别人完成并归档** (`archive/` 语料, 2026-08-22), 即「这件事可能已经有人做完」被摆上了台面。按设计这由人一眼可辨、由人裁: 该信息出现在每轮 `### Round N` 记录与聚合报告中, 恰好在两个决策时点天然可见 —— (a) 审计正常收敛后的报告消费时点; (b) `max_rounds` 耗尽触发降级策略 AskUserQuestion 时 (owner 在三路径里裁决前, 报告中的 🔴 行就是「是否还值得继续/是否撞车」的上下文)。AI 侧不得据此自行豁免审计轮次或改判 verdict —— 引擎层由「不阻断」条款机械保证, 行为层则是「告警交人裁」的分工。

---

## 附: 本推演引用的规范来源

- `aria/skills/audit-engine/SKILL.md` §per-round 入口探针 / §执行流程 / §收敛判定算法 / §降级策略 / §错误处理 / §配置依赖
- `aria/skills/audit-engine/references/execution-modes.md` §Convergence 模式 (Round N 围栏块) + §竞品 spec 探针 (per-round 入口) —— stdout 十二字段契约 / verdict 取值表 / exit code / 消费措辞三档 / fail-closed 义务 / 不阻断条款的权威可执行版
- `aria/skills/audit-engine/references/report-format.md` 轮次记录模板 (`- Sibling probe:` 行) / drift_metrics 骨架
- `aria/skills/audit-engine/references/convergence-algorithm.md` 四元组比较 / ∅ 双轮稳定性 gate / 振荡不可达条件 / 完整判定流程 (四终局优先级链)
- `aria/skills/audit-engine/references/report-storage.md` 5-field 落盘 schema / Verdict 计算 SOT
- `aria/skills/audit-engine/references/agent-dispatch-contract.md` 8-field frontmatter + 3 drift 字段追加
- `aria/skills/audit-engine/scripts/sibling_spec_probe.py` (只读源码核验: `run_probe` 的 verdict 判定次序 —— hits 非空 ⇒ `sibling_found`, 先于 status/own_keys 分支; `assemble_hits` 的 (remote, corpus, spec_dir, key) 去重)
