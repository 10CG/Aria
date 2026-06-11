# Proposal: audit-drift-guard (#17)

> **Status**: ✅ **Complete** — shipped aria-plugin v1.44.0 (PR [#80](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/80) merge `5871e17` 双远程 parity; 全链路: triage → brainstorm 4 决策 → post_brainstorm 19-agent/3 轮 → DEC → post_spec R3 PASS → agent-team 实施 [TG-0 契约首 commit b67ccb5] → code-review PASS [I-1~I-3 收] → **dogfood: Drift Guard 机制首跑产出非空 drift_metrics, 抓 2I+4m 全收**)
> **Spec Level**: 3 (Full — proposal + tasks)
> **关联 Issue**: Forgejo [aria-plugin#17](https://forgejo.10cg.pub/10CG/aria-plugin/issues/17) (triage `confirmed`, [comment-12282](https://forgejo.10cg.pub/10CG/aria-plugin/issues/17#issuecomment-12282))
> **ship target**: aria-plugin v1.44.0 (当前 SOT plugin.json = v1.43.0, 已验)
> **决策 SOT**: `docs/decisions/DEC-20260611-001-audit-drift-guard.md` (本 proposal 不复制设计细节)

## Why

audit-engine challenge 多轮循环的收敛判定 = 四元组 `(type,severity,category,scope)` 集合稳定性比较,**结构性盲点:只测"结论集合是否稳定",不测"是否还在讨论最初那个问题"** — 集合稳定 ≠ 命中原始目的。triage confirmed:v1.43.0 全 skill 目录 `grep -ric 'anchor|drift'` 零命中,机制完全缺位。高风险检查点:post_spec/post_brainstorm(开放式讨论最易漂)/post_planning/pre_merge;post_closure(max_rounds=1)不适用。与 #79 边界:#17=审计讨论轮内 drift,#79=mid-implementation spec drift,机制独立。

## What Changes

落地 DEC 的 **D1=B / D2=A / D3=A / D4=B** + 两条 R3 收口契约:

1. **Anchor 固化**(SKILL.md 新 Step 0,Round 1 前一次性): `{checkpoint, primary_goal, in_scope[], out_of_scope_hints[], source_sha}`,per-checkpoint fallback 链 `proposal Why/Goal → change_id 解析 → brainstorm_decisions(post_brainstorm 正向覆盖) → issue/PR 标题(anchor_source=degraded) → 全缺 fail-soft 跳过 + drift_anchor_missing 标注`。
2. **每轮 Drift Check**(challenge-mode-schema 新 Step 5,收敛判定前): **独立轻量 drift-checker**(audit-engine 内部调用,**非** agent-team-audit 审计 agent,不适用 8-field 契约)对 anchor + 本轮结论(分母 per-mode 显式:challenge = `decisions ∪ objections`)逐条分类 → `drift_ratio`。空集 → vacuously 0 跳过调用;checker 瞬断 → **fail-open** 按 <warn 处理 + `drift_check_skipped` 标注;独立 30-60s 超时不占审计 agent 预算;Round 1 跳过(无前序基线)。
3. **三档处置**(阈值可配 C-1): `<warn` 正常;`warn–refocus` Warning + 该轮收敛语义 per-mode(convergence = 强制 `unanimous_pass=false` 延迟一轮;challenge = 仅标注);`>= refocus`(含等号, DEC §4.3)→ **REFOCUS_ROUND**(消耗 max_rounds 配额防活锁,`is_refocus` 标签,输出替换 round_N 作 stability 基线,剔出 oscillation N-2 序列)+ `consecutive_refocus_count>=2` → **DRIFT_TERMINATED** 独立终局态(优先于 MAX_ROUNDS_EXHAUSTED)→ verdict=FAIL(drift override,走既有 FAIL owner 决策流程,不发明硬中止)。
4. **契约 C-1**(config-loader,**强制首批**): DEFAULTS.json `audit.drift_guard {warn_threshold:0.2, refocus_threshold:0.5, convergence_mode:false}` + SKILL.md 验证规则表三条(number [0,1] / `refocus>=warn` 违反 warn+单向 clamp / boolean)+ max_rounds 注释 ">=3"。
5. **契约 C-2**(report schema,**强制首批**): report-format.md frontmatter 补 `drift_terminated/drift_check_skipped/is_refocus`(无条件默认 false,oscillation pattern 同构)+ `drift_metrics` 章节骨架(anchor 快照/per_round 三类计数/anchor_engagement/consecutive_refocus_count/`converged_on_anchor = converged AND 末轮 drift_ratio<warn`)+ backward-compat 小节;report-storage.md §Verdict(SOT)加 drift override 规则 + converged×verdict 表 drift_terminated 行 + owner remediation 路径;verdict 双文件单 SOT 归属。
6. **scope**: challenge 默认开 / convergence opt-in 默认关 / post_closure 屏蔽。dispatch 契约:agent-dispatch-contract.md 加 Drift Guard 字段小节 + refocus 轮 frontmatter 定义 + drift-checker scope 排除。

## Impact

- **触及面**(纯 prose + schema,完整锚点表 = **DEC §7**,本 proposal 不复制): audit-engine SKILL.md + 6 references (challenge-mode-schema/convergence-algorithm/report-format/report-storage/agent-dispatch-contract/execution-modes) + brainstorm/SKILL.md (B4, DEC §7 遗漏补充) + config-loader SKILL.md/DEFAULTS.json + 版本 SOT 5+1 → v1.44.0。CLAUDE.md 免改(审计两轮 endorse)。
- **Rule #6**: prose/schema 类 → doc-existence 可验证清单 + schema 骨架 fixture + **本 Spec 实施后首个 challenge 审计作 dogfood**(可执行时点 = post_implementation audit, 见 tasks 审计检查点;产出非空 drift_metrics)。
- **向后兼容**: 旧报告缺字段视为 `drift_ratio=0, converged_on_anchor=null` 不告警;新 frontmatter 字段 additive 默认 false(防 #125/#126 dashboard parser 破坏,verdict 恒裸枚举)。
- **Out-of-scope**: #79 实施期 drift / anchor 语义校验(只验提取与分类流程)/ drift 历史跨审计聚合分析 / mid-audit re-anchor / 旧报告 backfill 等(全表 = DEC §9)。
