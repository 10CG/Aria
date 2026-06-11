# Tasks: audit-drift-guard (#17)

> **Spec Level**: 3 | **DEC**: DEC-20260611-001 (§7 触及面表 = 锚点 SOT) | **ship target**: aria-plugin v1.44.0
> **强制首批** (R3 blocking 收口): TG-0 契约 C-1/C-2 须为实施**首个 commit** 内容, post_spec/post_implementation audit 以 grep 核验。
> **每处文档改动**: `grep -n` 锚定真实行 + Edit 后 `grep -c` 验落地 (memory `feedback_verify_edit_landed_grep_count`)。

---

## TG-0 — 契约 C-1/C-2 (强制首批, 首个 commit)

### 0A. 契约 C-1 (config-loader)
- [ ] 0A.1 `config-loader/DEFAULTS.json` audit 块新增 `"drift_guard": {"warn_threshold": 0.2, "refocus_threshold": 0.5, "convergence_mode": false}`
- [ ] 0A.2 `config-loader/SKILL.md` 字段验证规则表补三条: `warn_threshold` (number, [0,1], default 0.2) / `refocus_threshold` (number, [0,1], default 0.5, **约束 >= warn_threshold, 违反 → warn + 单向 clamp**) / `convergence_mode` (boolean, default false, 描述注明 challenge 默认开 + convergence 可选 + post_closure 屏蔽)
- [ ] 0A.3 config-loader SKILL.md `max_rounds` 验证注释补 "drift guard 完整功能需 max_rounds >= 3"

### 0B. 契约 C-2 (report schema)
- [ ] 0B.1 `audit-engine/references/report-format.md` frontmatter template 补 `drift_terminated: false` / `drift_check_skipped: false` / `is_refocus: false` (**无条件默认字段**, 复用 oscillation pattern 同构, 非 all-or-nothing 条件注入)
- [ ] 0B.2 report-format.md 新增 `drift_metrics` 章节骨架: anchor 快照 + per_round 表 (含三类计数 `{on_topic, adjacent, off_topic}` + `anchor_engagement` + `consecutive_refocus_count`) + `converged_on_anchor` 计算规则显式 (`= converged AND 末轮 drift_ratio < warn_threshold; drift_terminated 时恒 false`) + off_topic_ids 保留来源命名空间前缀 (d-/obj-)
- [ ] 0B.3 report-format.md 『特殊标记字段』末尾补 drift_metrics **backward-compat 小节** (缺字段 → drift_ratio=0, converged_on_anchor=null, 不告警); rounds 整数 + is_refocus 组合唯一标识一轮说明; verdict 计算改 **cross-ref report-storage.md (SOT)**
- [ ] 0B.4 `references/report-storage.md` §Verdict (SOT) 加 **drift_terminated override 规则** (`drift_terminated: true → verdict=FAIL`, additive; rationale 锚点示例 "FAIL (drift override) — 连续 2 次 refocus 未回锚, Critical=0"; **frontmatter verdict 恒裸枚举 FAIL**, rationale 仅 body ## Verdict 节, 防 #125/#126 parser); converged×verdict 组合表加 `(converged: false, drift_terminated: true, verdict: FAIL)` 行并**排除该行触发 max_rounds 三路径降级**; owner remediation 路径 (重跑/收窄 context/显式 override, 区别于普通 FAIL 修 finding)
- [ ] 0B.5 report-storage.md frontmatter 字段同步 (drift 三字段 + is_refocus + consecutive_refocus_count 定义) + "drift_metrics 见 report-format.md (SOT)" cross-ref

---

## TG-A — 核心机制文档 (SKILL.md + 数据流/收敛算法)

### A1. SKILL.md
- [ ] A1.1 入口流程加 **Step 0 anchor 固化** (Round 1 前一次性): anchor 结构 + per-checkpoint fallback 链 (`proposal Why/Goal → change_id 解析 proposal.md [复用 pre-write-validation 既有锚点链] → brainstorm_decisions [post_brainstorm: primary_goal=核心议题 / in_scope=已确认决策 / out_of_scope_hints=DEFERRED 条目, 含 issue 链接可升级抓标题] → issue/PR 标题 [source_sha=当前 HEAD, anchor_source=degraded] → 全缺 fail-soft 跳过 + drift_anchor_missing 标注, 不阻塞审计`)
- [ ] A1.2 错误处理表加 drift-checker 行: spawn 失败/超时 → `drift_ratio=null` **fail-open** 按 <warn 档处理 + `drift_check_skipped: true`, consecutive_refocus_count **不增加**; 与 `round_state.incomplete` **正交** (二者独立声明)
- [ ] A1.3 #17 vs #79 边界 NOTE 一行 (#79 文档无落点 → 标注 "#79 文档待定, #17 单向 NOTE 暂可接受")

### A2. challenge-mode-schema.md
- [ ] A2.1 数据流图 + 步骤列表加 **Step 5: Drift Check** (收敛判定前) + 三档处置决策树
- [ ] A2.2 drift_ratio **分母 per-mode 显式定义**: convergence = 当轮 conclusion_records; challenge = `revised_discussion_output.decisions ∪ updated_challenge_output.objections`
- [ ] A2.3 objection 分类规则: 无结构化 scope → 仅基于 point 文本 + anchor in/out 关键词比对, **置信度低于 decision 路径**, 报告区分两类来源
- [ ] A2.4 空结论集除零特判 (findings=∅ → drift_ratio=0 vacuously, 跳过 LLM 调用) + warn 档 challenge 模式语义 (收敛判据 objections_resolved 与 unanimous_pass 无关 → 降格仅标注 `drift_warning`, refocus 档仍 REFOCUS_ROUND) + 时间契约 (drift-checker 独立 30-60s 超时, **不计入审计 agent 300s/轮预算**, 并发控制表加行)

### A3. convergence-algorithm.md
- [ ] A3.1 `check_convergence()` 伪代码: Round-1 guard **之后**嵌 `drift_action = check_drift(round_N, anchor)` 节点 (Round 1 跳过 drift 检查, 边界情况表加行) + REFOCUS_ROUND 独立返回状态
- [ ] A3.2 **refocus 轮语义**: 消耗 max_rounds 配额 (防活锁); 展示标签 R{N}-refocus / per_round[].is_refocus (非冻结重号); `consecutive_refocus_count` 章节 (normal round 归零, >=2 → 终止); refocus 输出**替换** round_N 作下轮 stability 基线
- [ ] A3.3 **四终局优先级链** return 顺序显式: DRIFT_TERMINATED (优先, 含边界轮 round==max_rounds 时优先于 MAX_ROUNDS_EXHAUSTED) / CONVERGED / OSCILLATION / MAX_ROUNDS_EXHAUSTED; converged=false + drift_terminated=true **不触发** max_rounds 三路径降级
- [ ] A3.4 **振荡豁免节**: oscillation N-2 寻址 = normal-round 逻辑序列 (is_refocus 条目剔除), 与 stability 基线同一索引语义; 附 normal→refocus→normal 最小 trajectory 示例 (逐轮标注 stability/oscillation 比较对象)
- [ ] A3.5 warn 档 convergence 实现点 (汇总层强制 unanimous_pass=false 延迟一轮; drift_ratio 回落则正常恢复, 持续触发由 max_rounds 兜底) + 收敛统计表加 drift-checker token 增量 (~+1-2K/轮) + max_rounds<3 时 refocus 机制死代码注明

---

## TG-B — dispatch 契约 + 模式文档

- [ ] B1 `references/agent-dispatch-contract.md`: 8-field 模板后加 "### Drift Guard 字段" 小节 (无条件默认 false + 聚合层覆盖 + dispatch 已知字段注入实值, #126 供给侧同构); refocus 轮 frontmatter 定义 (`rounds: N` 整数 + `is_refocus: true` 注入); drift-checker scope 排除一句 (内部调用, 输出 drift_metrics 非 audit report, 不适用 8-field 契约)
- [ ] B2 `references/execution-modes.md` 核查: 有独立 challenge 步骤列表则同步 Step 5 或 cross-ref; 仅委托则标注 "仅 cross-ref, 无须独立修改" 封闭歧义
- [ ] B3 report-format.md 存储位置节改 cross-ref report-storage.md 单 SOT (drive-by, pre-existing 漂移, 单列防漏)

---

## TG-C — 版本 SOT + 收尾

- [ ] C1 plugin.json → v1.44.0 + marketplace.json (×2, grep -c==2) + VERSION + CHANGELOG.md + README.md
- [ ] C2 主项目 gitlink + VERSION 记录
- [ ] C3 CLAUDE.md 项目状态/footer (ship 时 Phase D 标准流程; 正文免改, 审计两轮 endorse)

---

## 审计检查点
- [ ] post_spec: 本 spec vs DEC 保真 (重点 grep 核验 TG-0 契约条目与 DEC §7 闭合标准逐字对齐)
- [ ] post_implementation: 全 TG 后 (TG-0 在首个 commit 的 grep 证据)
- [ ] pre_merge: Rule #8 (aria-plugin 无 CI → skip_with_warning)
- [ ] post_closure: D.3 handoff (Rule #9); **dogfood**: 本 Spec 自身 post_spec audit 报告产出非空 drift_metrics

## AC 摘要 (完整判定语义见 DEC §4)
- [ ] AC-1: 契约 C-1 落地 — DEFAULTS.json drift_guard 三键 + config-loader 验证表三条 + max_rounds 注释 (grep 可验)
- [ ] AC-2: 契约 C-2 落地 — report-format/report-storage 双文件 drift 字段 + drift_metrics 骨架 + verdict 单 SOT + backward-compat 小节 (grep 可验)
- [ ] AC-3: anchor 固化 Step 0 + fallback 链全 checkpoint 有着落 (post_brainstorm 正向覆盖, fail-soft 非常态)
- [ ] AC-4: 三档处置 + REFOCUS_ROUND/DRIFT_TERMINATED 终局态 + 振荡豁免 + 活锁防护 (refocus 耗配额) 在 convergence-algorithm.md 无歧义可执行
- [ ] AC-5: drift-checker fail-open + 除零 + 时间契约 + scope 排除 (advisory-over-hardlock 一致)
- [ ] AC-6: doc-existence 清单全绿 (DEC §7 表逐行) + Rule #6 substitute (`drift_metrics.per_round 条目数 == 实际轮次数` 结构性标准)
- [ ] AC-7: 向后兼容 — 旧报告缺字段语义 + frontmatter verdict 恒裸枚举 (#125/#126 防护)
