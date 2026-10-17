# audit-engine convergence 模式 Round 2 入口 — 描述性推演

**场景参数**: checkpoint = `post_planning` (A.2, 调用方 task-planner) | mode = `convergence` | context = `openspec/changes/demo-spec/` | repo root = `/work/Demo` | Round 1 已结束, 现处 Round 2 入口。以下全部为推演, 不实际执行任何命令。

## 0. Round 2 入口前的既有状态 (本轮不重复执行的部分)

- **入口逻辑** (config-loader 读 `audit.*` 块、mode 解析含 file-scope 二次过滤、agents 加载) 在审计启动时 (Round 1 前) 已完成, 每轮不重复。本轮按已解析的 `convergence` + `post_planning` team 配置继续。
- **Step 0 Anchor 固化** (Drift Guard #17) 在 Round 1 启动前**一次性**执行过: `post_planning` 属 proposal 类, anchor 来源 = `openspec/changes/demo-spec/proposal.md` 的 Why/Goal 段。anchor 审计周期内不可变, Round 2 入口**不**重新固化 (换锚 = 另起一次审计)。
- **Pre-merge completeness gate** 仅 `checkpoint == "pre_merge"` 时运行, 本例 `post_planning` 不适用。
- Round 1 的 `round_state` 已落: conclusions + comparison_keys (四元组集合) + vote; Round 1 的 drift check 按边界规则**跳过** (无前序稳定基线, `drift_ratio` 不计算)。
- Round 1 结构上无法判定收敛 (无上一轮) —— 这正是必须进 Round 2 的原因。

---

## (1) Round 2 入口执行的步骤清单

### Step A — 竞品 spec 探针 (每轮入口, Round 2 含; 与 Step 0 显式消歧: 本探针每轮跑, 不沿用 Step 编号)

完整命令行:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/sibling_spec_probe.py" \
  --own-spec-dir "demo-spec" --repo-path "/work/Demo"
```

这是 Round 2 入口唯一由引擎直接调用、有完整命令行的外部命令。给定 stdout 为题面那行 JSON, exit code 0。

(探针脚本自身内部行为 —— 引擎只消费 stdout/exit code, 以下仅为读源码所得的推演注记: 对 enforced remote `origin` 先 `ls-remote --symref` 解析默认分支 (fail-closed, 不猜分支名), 再 `fetch --no-tags --prune` 进**私有命名空间** `refs/aria/sibling-probe/origin/*` (不动 `refs/remotes/*`、不动 remote 配置、不读写 claim), 然后 `for-each-ref` + `ls-tree` + `git show` 枚举并分类 `openspec/{changes,archive}/*/proposal.md` 语料; 每个 git 子进程 30s 超时, fetch 腿最多 2 次。)

**stdout 消费判定** (按 `references/execution-modes.md ## 竞品 spec 探针 (per-round 入口)` 的 fail-closed 义务逐条过):

1. exit code == 0 → 探针完成了一次**有定义的判定** (命中也是 0), 非探针自身失败。
2. stdout 可解析为恰一个 JSON 对象, `schema_version == "1"` 为已知值 → **不**落入「未能核实」处置。
3. 读**一等字段** `verdict == "sibling_found"` → 取 (α) 档渲染 (🔴)。不从 `hits == []` 反推任何结论 (本例 hits 也非空)。
4. N = 去重后的 `spec_dir` 数 = **1** (`2026-08-22-phase-c-integrator-ci-path-coverage`; 本例仅 origin 一个 enforced remote、一条 hit, 不涉及「同一 Spec 在 origin/github 两镜像各成一条 hits[] 项须去重计数」的情形)。
5. 唯一命中项 `corpus == "archive"` → 追加标注**「已完成的 Spec」** (M = 1)。
6. `status == "ok"` (非 degraded; `reason == null`, `caps_applied == []`, remotes 无 `error_kind`/`capped`) → **不**追加「(覆盖不完整: …)」后缀。
7. 探针 advisory: 渲染进当轮 `### Round 2` 记录与聚合报告后**继续**正常流程 —— 不改 verdict、不改收敛判定、不改轮次路由 (见 (3))。

辅助解读 (供推演完整性, 不进报告行): 本轨 `own_layer == "canonical"`, 对方命中 `layer == "url_fallback"` —— 两侧经规范化后落到同一比较键 `["k","aria-plugin",122]`, 键交集命中与层无关; remotes 显示 origin 默认分支 master 经 `ls-remote --symref` 解析、扫 149 个唯一 proposal blob / 3 refs / 0 stale skip / 无 cap, 覆盖完整。

### Step B — 调用 agent-team-audit 单轮引擎 (Round 2 主体)

- spawn `convergence_agents` (来源优先级: `agents_config` 参数 > config `audit.teams[post_planning]` > 默认分组), 各 Agent **独立**分析 context (`openspec/changes/demo-spec/` 的 proposal/tasks 产物), 返回原始 issues 列表。
- dispatch prompt 按 `references/agent-dispatch-contract.md` **原文嵌入** 8-field YAML frontmatter 模板, 并无条件追加 3 个 drift 默认字段 (`drift_terminated` / `drift_check_skipped` / `is_refocus` 全 `false`; `rounds: 2`) —— 否则 dashboard parser 不可见 (Aria #126)。
- 并发与超时: 单轮 max_parallel 2 / hard_cap 3; 单 spawn 超时 120s; 整轮 wall-clock 300s (轮间串行)。Agent spawn 失败/超时 → 跳过该 Agent + 当轮 `incomplete: true`, 不阻塞收敛; 全部 Agent 失败 → 当轮作废、输出错误报告、不计入 max_rounds。
- 各 agent 报告落盘 (5-field uniqueness schema):
  `/work/Demo/.aria/audit-reports/post_planning-R2-{timestamp_ms}-demo-spec-{agent_role}.md`

### Step C — 汇总引擎

1. 合并所有 Agent 输出到统一列表;
2. `{category, scope}` 去重 (相同 → 合并 `found_by`, 取最高 severity; 复用 agent-team-audit 算法);
3. 同 scope 矛盾意见 → 保留双方 + `conflicted: true` (不自动裁决, 留给下一轮或人工);
4. 结构化提取为 conclusion_record, `id = sha256(category:scope:severity:type)[:8]` (`summary`/`timestamp`/`agent_role` 不入哈希 → 跨轮跨 agent 同 finding 同 ID)。

### Step D — 收敛判定 (Round 2 是首个可判定轮)

- **Drift Check 节点** (#17): convergence 模式**默认不开** (`audit.drift_guard.convergence_mode` 默认 false; challenge 才默认开)。若本项目显式 opt-in, 则由独立 drift-checker 持 Round 1 前固化的 anchor 对 Round 2 结论分类 → `drift_ratio` (drift-checker spawn 失败/超时 → fail-open: `drift_check_skipped: true`, `drift_ratio=null` 按 <warn 档, `consecutive_refocus_count` 不增加; 独立 30-60s 配额, 不占 300s/轮)。
- **四元组集合比较**: `keys(R2) == keys(R1)` → `conclusions_stable`; 空集守卫: `keys(R2) = ∅` 时须 `round_number >= 2` 且 R1 也为 ∅ (双轮稳定性确认, v1.17.5+)。
- **全票 PASS**: `convergence_agents` 全员 `vote == PASS` (skipped Agent 不投票)。
- **振荡检测**: normal_rounds 长度 < 3 → Round 2 结构上不可达。
- **四终局优先级链** `CONVERGED → DRIFT_TERMINATED → OSCILLATION → MAX_ROUNDS_EXHAUSTED` (+ 独立非终局状态 `REFOCUS_ROUND`): Round 2 上 DRIFT_TERMINATED 不可达 (R1 drift 跳过 ⇒ `consecutive_refocus_count` 至多 1 < 2), OSCILLATION 不可达 (<3 normal 轮), MAX_ROUNDS_EXHAUSTED 不可达 (默认 `max_rounds=5`, R2 < 5)。

### Step E — 路由

- `conclusions_stable AND unanimous_pass` → **CONVERGED**: 计算 verdict (0 Critical + 0 Major = PASS / 0C + ≥1M = PASS_WITH_WARNINGS / ≥1C = FAIL), 生成最终报告 (frontmatter `rounds: 2, converged: true`, 11 字段)。`post_planning` 的 FAIL 处置 = **继续 (仅记录)**, 不阻塞 (阻塞仅 mid_implementation / post_implementation / pre_merge)。
- 部分收敛 (结论集合无变化但有 REVISE) → 继续下一轮。
- 未收敛 + 有余量 → **Round 3** —— 其入口**再次**执行 Step A 同一探针命令 (每轮重跑; 不复用 `remote_refresh` 缓存, 也不复用本轮结果 —— 审计跨天时首轮结论会陈旧)。
- (仅当 convergence drift guard 已 opt-in 且 `drift_ratio >= refocus_threshold` 且 R2 < max_rounds) → **REFOCUS_ROUND**: Round 3 为 `R3-refocus` (`is_refocus: true`, 消耗 max_rounds 配额; 其输出替换作下轮 stability 基线, 不进振荡序列)。
- max_rounds 耗尽的三路径降级策略 (AskUserQuestion: 接受/加轮/降级单轮) 在 Round 2 不可达。

---

## (2) 本轮审计报告 `### Round 2` 记录的内容

按 `references/report-format.md` 完整报告模板 (Round 2 非 Final 形态):

```markdown
### Round 2
- Agents: {agent_list}                    # 如 [tech-lead, backend-architect, qa-engineer, knowledge-manager], 完成数/总数
- Sibling probe: 🔴 检测到 1 份同 issue 的竞品 Spec: 2026-08-22-phase-c-integrator-ci-path-coverage (已完成的 Spec)
- Conclusions: {count}                    # 汇总引擎去重后的结论数
- Delta vs Round 1: +{added} / -{removed} # 四元组集合差 (新增/移除的键)
- Vote: {PASS/REVISE}                     # 全员 PASS, 或有 REVISE (附来源 agent)
- Duration: {seconds}s                    # 本轮审计耗时 (探针 elapsed_ms=18342 是探针自身成本, 不混入本行)
```

`- Sibling probe:` 行的推导依据 (SKILL.md (α)/(β)、execution-modes.md 三档消费措辞、report-format.md 模板行三处交集):

| 输入事实 | 推导 |
|---|---|
| exit 0 + stdout 合法 JSON + `schema_version == "1"` | 不取「未能核实」档 (fail-closed 义务未触发) |
| `verdict == "sibling_found"` (一等字段) | 🔴 档; **禁止**渲染为「无竞品」 |
| hits 按 `spec_dir` 去重后 = 1 个 | N = 1 |
| 唯一命中 `corpus == "archive"` | 标注「已完成的 Spec」, M = 1 (等价模板形: 「检测到 1 份同 issue 的竞品 Spec (含 1 份已完成的 Spec)」) |
| `status == "ok"` / `reason == null` / `caps_applied == []` | 无「(覆盖不完整: …)」后缀 |

同一措辞同时进**聚合报告** (三档消费措辞规定: 写进当轮 `### Round N` 记录并进聚合报告)。若 Round 2 恰为终局 (Step E 判 CONVERGED), 该节改用 `### Round 2 (Final)` 形态: 以 `- Converged: true/false` 替代 Delta 行, Sibling probe 行不变。

---

## (3) 探针结果对本轮 verdict / 收敛判定 / 是否继续 Round 3 的影响

**结论: 三者全部零影响 —— 探针是 advisory 副机制, 「不阻断」。**

| 判定面 | 探针是否参与 | 实际决定因素 |
|---|---|---|
| verdict (PASS / PASS_WITH_WARNINGS / FAIL) | 否 | 最后轮 Critical/Major 计数 (0C+0M / 0C+≥1M / ≥1C) + `drift_terminated` override (本例不涉及) |
| 收敛判定 (`converged`) | 否 | 四元组集合相等 AND 全票 PASS (含空集双轮稳定守卫) |
| 轮次路由 (是否 Round 3) | 否 | 四终局优先级链 → CONVERGED / REFOCUS_ROUND / CONTINUE |

规范依据: SKILL.md「per-round 入口探针」**不阻断**条 + execution-modes.md「**不阻断**: 探针是 advisory 副机制 —— 不改 verdict 计算、不改收敛判定、不改轮次路由; 「同 issue」≠「重复劳动」(Spec §Why 的 `#137` 簇是有意拆分), 命中是告警不是判决, 由人一眼可辨」。

它的实际作用面只有**报告渲染 + 人的注意**: 本例命中落在 `archive/` 语料 —— 即在同一 issue (规范化比较键 `aria-plugin#122`) 下, 远端 master 上已存在一条**已 ship 归档**的竞品 Spec (`2026-08-22-phase-c-integrator-ci-path-coverage`)。这把「这件事别人做完了」摆上台面, 供 owner 读报告后自行裁断 (例如中止本轨、转向复用归档成果) —— 但那是**人的决定**: 引擎不会因此停轮、降级、改 PASS/FAIL。Round 2 照常 spawn agents、照常汇总、照常按 keys(R2) vs keys(R1) + 全票 PASS 判收敛; 若未收敛且有 REVISE/集合变动, 照常进 Round 3, 且 Round 3 入口会**重新**跑探针 (每轮重跑, 不复用本轮结果)。

边界对照 (若题面 stdout 换形态): exit ≠ 0 / stdout 无法解析为 JSON / `schema_version` 未知 ⇒ 一律按 `not_established` 处置, 渲染「**未能核实** —— 本轮竞品扫描未取到完整证据 (原因: …)」, 且**禁止**渲染为「无竞品」—— 零证据不当正证据。本题给的是 exit 0 + 合法 JSON + `sibling_found`, 走 (α) 档, 无此分支; `status == "degraded"` 时的「正证据不降级」追加后缀路径 likewise 未触发。
