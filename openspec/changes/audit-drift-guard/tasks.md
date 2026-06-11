# Tasks: audit-drift-guard (#17)

> **Spec Level**: 3 | **DEC**: DEC-20260611-001 (§7 触及面表 = 锚点 SOT; 本 tasks 含 §7 两处勘误标注) | **ship target**: aria-plugin v1.44.0
> **强制首批** (R3 blocking 收口): TG-0 全部条目 (0A.1~0A.4 + 0B.1~0B.6) 须为实施**首个 commit** 内容, 首批项全部在首个 commit 的 grep 证据中覆盖。
> **每处文档改动**: `grep -n` 锚定真实行 + Edit 后 `grep -c` 验落地 (memory `feedback_verify_edit_landed_grep_count`)。

---

## TG-0 — 契约 C-1/C-2 (强制首批, 首个 commit)

### 0A. 契约 C-1 (config 侧)
- [ ] 0A.1 `config-loader/DEFAULTS.json` audit 块新增 `"drift_guard": {"warn_threshold": 0.2, "refocus_threshold": 0.5, "convergence_mode": false}`
- [ ] 0A.2 `config-loader/SKILL.md` 字段验证规则表补三条: `warn_threshold` (number, [0,1], default 0.2) / `refocus_threshold` (number, [0,1], default 0.5, **约束 >= warn_threshold, 违反 → warn + 单向 clamp**) / `convergence_mode` (boolean, default false, 描述逐字: "challenge 默认开 + convergence 可选 (本字段) + post_closure 由模式选择阶段屏蔽")
- [ ] 0A.3 config-loader SKILL.md `max_rounds` 验证注释补 "drift guard 完整功能需 max_rounds >= 3"
- [ ] 0A.4 `audit-engine/SKILL.md` **§配置依赖** (真实锚点 line ~302; **DEC §7 勘误**: 表中此项误归 config-loader, 实属 audit-engine) 补 convergence_mode 语义 (challenge 默认开 / convergence opt-in / post_closure 屏蔽)

### 0B. 契约 C-2 (report schema)
- [ ] 0B.1 `audit-engine/references/report-format.md` frontmatter template 补 `drift_terminated: false` / `drift_check_skipped: false` / `is_refocus: false` (**无条件默认字段**, oscillation pattern 同构, 非条件注入)
- [ ] 0B.2 report-format.md 新增 `drift_metrics` 章节骨架 (嵌套层级按 DEC §4.5): **per_round 表内** = 三类计数 `{on_topic, adjacent, off_topic}` + `off_topic_ids` (namespace 前缀 d-/obj-); **drift_metrics 顶层兄弟字段** = anchor 快照 + `anchor_engagement` (none = 末轮 on_topic_count==0 时标注, annotation only) + `consecutive_refocus_count` + `converged_on_anchor` (计算规则显式: `= converged AND 末轮 drift_ratio < warn_threshold; drift_terminated 时恒 false`)
- [ ] 0B.3 report-format.md 『特殊标记字段』末尾补 drift_metrics **backward-compat 小节** (缺字段 → drift_ratio=0, converged_on_anchor=null, 不告警); rounds 整数 + is_refocus 组合唯一标识说明; verdict 计算改 **cross-ref report-storage.md (SOT)**
- [ ] 0B.4 `references/report-storage.md` §Verdict (SOT) 加 **drift_terminated override 规则** (`drift_terminated: true → verdict=FAIL`; rationale 锚点示例 "FAIL (drift override) — 连续 2 次 refocus 未回锚, Critical=0"; **frontmatter verdict 恒裸枚举 FAIL**, rationale 仅 body ## Verdict 节, 防 #125/#126 parser); converged×verdict 表加 `(converged: false, drift_terminated: true, verdict: FAIL)` 行并**排除该行触发 max_rounds 三路径降级**; owner remediation 路径 (重跑/收窄 context/显式 override, 区别普通 FAIL 修 finding)
- [ ] 0B.5 report-storage.md frontmatter 字段同步 (drift 三字段 [drift_terminated/drift_check_skipped/is_refocus] + consecutive_refocus_count 定义) + "drift_metrics 见 report-format.md (SOT)" cross-ref
- [ ] 0B.6 report-format.md **§阻塞行为** (真实锚点 line 98) 表后补注: drift-FAIL (`drift_terminated: true → FAIL`) **继承本表 per-checkpoint 既有处置**, blocking checkpoint 的 remediation 路径 cross-ref report-storage.md §Verdict (**DEC §7 勘误**: report-format 行漏列此项, 设计内容在 DEC §4.4)

---

## TG-A — 核心机制文档

### A1. SKILL.md
- [ ] A1.1 入口流程加 **Step 0 anchor 固化** (Round 1 前一次性): anchor 结构 `{checkpoint, primary_goal, in_scope[], out_of_scope_hints[], source_sha}`; **anchor 写入报告头 + 审计周期内不可变, mid-audit re-anchor 不支持 (cross-ref DEC §9)**; per-checkpoint fallback 链 (带 checkpoint 归属标签, 非单线性): `[proposal 类: post_spec/post_planning] proposal Why/Goal → [diff/UPM 类: mid_implementation/post_implementation/pre_merge] 经 change_id 解析 proposal.md (复用 pre-write-validation 既有锚点链) → [post_brainstorm] brainstorm_decisions (见 A1.1b) → issue/PR 标题 (source_sha=当前 HEAD, anchor_source=degraded) → 全缺 fail-soft 跳过 + drift_anchor_missing 标注, 不阻塞审计`。调用契约见 A1.1b
- [ ] A1.1b SKILL.md Step 0 节单独写 **post_brainstorm 调用契约三点** (DEC §4.1): (a) caller 侧 context 传入决策记录文件路径 (如 `.aria/brainstorm-{id}.md` 或 docs/decisions/DEC-*.md); (b) 提取器识别"已确认决策"段 → in_scope / "DEFERRED"条目 → out_of_scope_hints / 核心议题 → primary_goal; (c) context 为 Forgejo issue URL 时降级 issue_title; (可选 upgrade) 决策记录文件内含 issue 链接时可升级抓 issue 标题作 primary_goal 补充 (DEC §4.1)
- [ ] A1.2 错误处理表加 drift-checker 行: spawn 失败/超时 → `drift_ratio=null` **fail-open** 按 <warn 档处理 + `drift_check_skipped: true`, consecutive_refocus_count **不增加**; 与 `round_state.incomplete` **正交** (独立声明); **整轮超时耗尽场景的归因规则一并写入正交声明** (DEC §3 D2 fail-open bullet)
- [ ] A1.3 #17 vs #79 边界 NOTE 一行 (#79 文档无落点 → 标注 "#79 文档待定, #17 单向 NOTE 暂可接受")

### A2. challenge-mode-schema.md
- [ ] A2.1 数据流图 + 步骤列表加 **Step 5: Drift Check** (收敛判定前) + **本次新增 drift-checker 节 (对应 DEC §3 D2; A2.3/A2.5 的 'D2 节' 即指此新增节)** + 三档处置决策树 (**区间边界与 DEC §4.3 逐字**: `< warn` / `[warn, refocus)` / `>= refocus_threshold` 含等号)
- [ ] A2.2 drift_ratio **公式本体 + 分母 per-mode 显式**: `drift_ratio = off_topic / all; adjacent 不计入分子 — 公式与阈值语义不改 (DEC §9 守界句一并写入)`; convergence 分母 = 当轮 conclusion_records (实施映射真实 token: `round_N.conclusions` @ convergence-algorithm.md:44); challenge 分母 = `revised_discussion_output.decisions ∪ updated_challenge_output.objections`
- [ ] A2.3 objection 分类规则: 无结构化 scope → 仅基于 point 文本 + anchor in/out 关键词比对, **置信度低于 decision 路径**; **两类来源经 off_topic_ids namespace 前缀字面区分 (d-=decision, obj-=objection), D2 节字面说明**
- [ ] A2.4 空结论集除零特判 (精确条件按 DEC D2: convergence = conclusion_records=∅; challenge = `decisions=∅ AND objections=∅` 联合判空 → drift_ratio=0 vacuously, 跳过 LLM 调用) + warn 档 challenge 模式语义 (收敛判据 objections_resolved 与 unanimous_pass 无关 → 降格仅标注 `drift_warning`, refocus 档仍 REFOCUS_ROUND) + 时间契约: drift-checker 独立 30-60s 超时, **不占 300s/轮 wall-clock** (并发控制条目注真实锚点 `audit-engine/SKILL.md §并发控制 line ~261`, 不在本文件造第二张并发表; 勘误不在此处理, 见 A3.5)
- [ ] A2.5 D2 节补 **partial anchor 分类规则** (DEC §4.1 / R5): anchor 结构完整但 `in_scope=[] AND out_of_scope_hints=[]` → drift-checker 降为 primary_goal 语义相似度单维分类 (语义相关→on-topic 否则 adjacent) + 报告标注 `anchor_scope_empty: true` + `drift_classification_confidence: low`; **不触发 fail-soft skip** (区别于全缺 anchor 的 drift_anchor_missing 路径)

### A3. convergence-algorithm.md
- [ ] A3.1 `check_convergence()` 伪代码: Round-1 guard **之后**嵌 `drift_action = check_drift(round_N, anchor)` 节点 (Round 1 跳过 drift 检查, 边界情况表加行) + REFOCUS_ROUND 独立返回状态 + **warn 档独立分支显式落伪代码** (**仅 convergence 模式分支**: `drift_action == WARN → 强制 unanimous_pass=false → return CONTINUE`; challenge 模式 warn=仅标注 见 A2.4, 共享伪代码须带模式限定词防双模式误阻塞。非仅散文; 实现点限**汇总层覆盖, 不注入 agent prompt** — R10 防 agent 知晓 drift 产生迎合性副作用)
- [ ] A3.2 **refocus 轮语义**: 消耗 max_rounds 配额 (防活锁); 展示标签 R{N}-refocus / per_round[].is_refocus (非冻结重号); `consecutive_refocus_count` 章节 (normal round 归零, >=2 → 终止); refocus 输出**替换** round_N 作下轮 stability 基线
- [ ] A3.3 **四终局优先级链 return 顺序显式 (与 DEC §4.4 逐字)**: `CONVERGED → DRIFT_TERMINATED (含边界轮 round==max_rounds 时优先于 MAX_ROUNDS_EXHAUSTED) → OSCILLATION → MAX_ROUNDS_EXHAUSTED`; "(优先)" 限定仅 vs MAX_ROUNDS_EXHAUSTED 语境; converged=false + drift_terminated=true **不触发** max_rounds 三路径降级
- [ ] A3.4 **振荡豁免落伪代码层** (非仅示例): oscillation 检测中 `keys_N / keys_N_1 / keys_N_2` 均取 **normal-round 逻辑序列** (is_refocus==true 轮剔除后重新索引), 落在振荡检测伪代码 (加注或改 `keys_N_2` 取法; 统一用真实 token 拼法 keys_N_2); 附 trajectory 示例两则: normal→refocus→normal + **normal→refocus→refocus** (标注第二次连续 refocus 当轮不作 keys_N, 防 DRIFT_TERMINATED 误判为 OSCILLATION), 逐轮标注 stability/oscillation 比较对象
- [ ] A3.5 收敛统计表加 drift-checker token 增量 (~+1-2K/轮) + **区分单次 spawn 超时与整轮 wall-clock** (challenge 整轮 = 4×串行 spawn + drift-checker 独立配额; 超时数字以 audit-engine/SKILL.md 真实值为准 [spawn 120s / 每轮 300s]; **勘误注明 DEC §4.2 "spawn-300s" 为误标, 仅此处处理**) + 边界情况表补行 (DEC §4.4 逐字): "max_rounds<3 时 DRIFT_TERMINATED 不可达 (consecutive_refocus>=2 需至少 3 轮), drift guard 降级为 max_rounds 兜底"

---

## TG-B — dispatch 契约 + 模式/调用方文档

- [ ] B1 `references/agent-dispatch-contract.md`: 8-field 模板后加 "### Drift Guard 字段" 小节 (无条件默认 false + 聚合层覆盖 + dispatch 已知字段注入实值, #126 供给侧同构); refocus 轮 frontmatter 定义 (`rounds: N` 整数 + `is_refocus: true` 注入); drift-checker scope 排除一句 (内部调用, 输出 drift_metrics 非 audit report, 不适用 8-field 契约)
- [ ] B2 `references/execution-modes.md` challenge 步骤列表 (**已核验 line 117-127 存在独立 Step 1-4**): Step 4 后加 "Step 5: Drift Check (详见 challenge-mode-schema.md)" cross-ref (确定性指令, 非"核查")
- [ ] B3 report-format.md 存储位置节改 cross-ref report-storage.md 单 SOT (drive-by, pre-existing 漂移, 单列防漏)
- [ ] B4 `brainstorm/SKILL.md` 注明 post_brainstorm audit 应传入的 context 类型 (决策记录文件路径, 与 A1.1b anchor 提取链对齐) — **DEC §7 表遗漏的补充触及面** (设计内容在 DEC §4.1)

---

## TG-C — 版本 SOT + 收尾

- [ ] C1 plugin.json → v1.44.0 + marketplace.json (×2, grep -c==2) + VERSION + CHANGELOG.md + README.md
- [ ] C2 主项目 gitlink + VERSION 记录
- [ ] C3 CLAUDE.md 项目状态/footer (ship 时 Phase D 标准流程; 正文免改, 审计两轮 endorse)

---

## 审计检查点
- [ ] post_spec: 本 spec vs DEC 保真 (TG-0 vs C-1/C-2 闭合标准逐字)
- [ ] post_implementation: 全 TG 后; **TG-0 在首个 commit 的 grep 证据**
- [ ] pre_merge: Rule #8 (aria-plugin 无 CI → skip_with_warning)
- [ ] post_closure: D.3 handoff (Rule #9); **dogfood (可执行时点)**: 机制文档落地后**首个 challenge 模式审计 (本 Spec 的 post_implementation audit)** 须产出非空 drift_metrics; 以 post_spec 名义补跑 re-run 亦可, 报告注明 re-run

## AC 摘要 (完整判定语义见 DEC §4; grep 模式串 = 机械验收, memory `feedback_verify_edit_landed_grep_count`)
- [ ] AC-1: 契约 C-1 — `grep -c 'drift_guard' config-loader/DEFAULTS.json >=1` + `grep -c 'refocus_threshold' config-loader/SKILL.md >=1` + `grep -c 'drift guard 完整功能' config-loader/SKILL.md >=1` + `grep -c 'convergence_mode' aria/skills/audit-engine/SKILL.md >=1` (0A.4); 全部首批项在首个 commit grep 证据覆盖
- [ ] AC-2: 契约 C-2 — `grep -c 'drift_terminated' report-format.md >=1` 且 `report-storage.md >=1` + `grep -c 'drift_metrics' report-format.md >=1` + `grep -c 'backward-compat' report-format.md >=1` + 0B.6 `grep -c 'per-checkpoint 既有处置' report-format.md >=1` + verdict 单 SOT 归属
- [ ] AC-3: anchor 固化 Step 0 + fallback 链全 checkpoint 有着落 (post_brainstorm 调用契约 A1.1b 三点齐) + partial anchor 规则 (`grep -c 'anchor_scope_empty' challenge-mode-schema.md >=1`) + 来源区分 (`grep -c 'obj-' challenge-mode-schema.md >=1`)
- [ ] AC-4: 三档处置 + REFOCUS_ROUND/DRIFT_TERMINATED 终局态 (优先级链 DEC §4.4 逐字) + **振荡豁免在伪代码层** (keys_N 系列 normal-round 重索引) + warn 档伪代码独立分支 + 活锁防护 — convergence-algorithm.md 无歧义可执行
- [ ] AC-5: drift-checker fail-open + 除零 + 时间契约 + scope 排除 (advisory-over-hardlock 一致)
- [ ] AC-6: doc-existence 清单全绿 (DEC §7 表逐行 + 本 tasks B4/0A.4/0B.6 三处勘误补充) — 代表性锚点: `grep -c 'Step 0' audit-engine/SKILL.md >=1` / `grep -c 'Step 5' challenge-mode-schema.md >=1` / `grep -c 'DRIFT_TERMINATED' convergence-algorithm.md >=1`; Rule #6 substitute = `drift_metrics.per_round 条目数 == 实际轮次数` 结构性标准
- [ ] AC-7: 向后兼容 — 旧报告缺字段语义 + frontmatter verdict 恒裸枚举 (#125/#126 防护)
