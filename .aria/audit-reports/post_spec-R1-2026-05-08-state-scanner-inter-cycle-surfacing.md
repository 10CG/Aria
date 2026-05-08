---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-05-08T02:30Z
context: openspec/changes/state-scanner-inter-cycle-surfacing/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, knowledge-manager]
change_id: state-scanner-inter-cycle-surfacing
spec_branch: feature/state-scanner-inter-cycle-surfacing
spec_pr: 10CG/Aria#88
source_issue: 10CG/Aria#85
predecessor: T5 quick-win shipped 2026-05-07 (aria b22d27d / 主项目 a9a6a6a)
---

# post_spec R1 — state-scanner-inter-cycle-surfacing

## Aggregate Verdict

| Agent | Vote | Critical | Major | Minor | Total |
|-------|------|----------|-------|-------|-------|
| tech-lead | PASS (with reservations) | 0 | 2 | 2 | 4 |
| backend-architect | REVISE (2 blockers) | 2 | 3 | 3 | 8 |
| qa-engineer | REVISE (3 high) | 3 | 5 | 2 | 10 |
| knowledge-manager | REVISE (2 major blockers) | 0 | 2 | 4 + 1 info | 7 |
| **AGGREGATE** | **REVISE / FAIL** | **5** | **12** | **11** | **28** (+ 1 info) |

**Convergence**: R1 是首轮 discovery,无前序四元组对比,**未收敛**。**5 Critical → verdict FAIL**(per audit-engine SKILL.md `verdict = FAIL if ≥1 Critical`)。需 R2 fix-verify。

**Vote 分布**: 1 PASS / 3 REVISE → 不全票 PASS,convergence 条件不满足。

---

## Critical Findings (Blocking)

> 必须在 R2 前修 Spec。每条都可定位到 specific spec line + concrete fix。

### C-1 [BA-01] G4 priority_items 重复解析风险

**Scope**: §G4 Tasks T4.2 / `aria/skills/state-scanner/scripts/collectors/requirements.py:47-63`

**Detail**: `requirements.py` 现有 `story_items[]` 已含 G4 所需全部字段 (`id, path, status_normalized, raw_status`)。Spec 说"增量提取 in_progress + ready + pending 头部 N 项",未声明 `priority_items[]` 是 (a) 从 `story_items[]` 过滤切片 还是 (b) 重新 glob+read 文件系统。后者会重复 read_text() + 引入 mtime 读取时机歧义。

**Fix**: T4.2 显式声明 `priority_items[] = sorted(filter(story_items, status ∈ {in_progress, ready, pending}), key=(_STATUS_ORDER, -mtime))[:limit]`。`story_items[]` 排序后只对入选项 stat() 一次。

### C-2 [BA-02] handoff 备选 regex 过宽

**Scope**: §G3 备选 regex `> .*入口.*\(([^)]+\.md)\)`

**Detail**: 中文 "入口" 在技术文档中极泛 ("函数入口" / "调试入口" / "记录入口" 等)。备选 regex 缺 `^>` 行首锚点 + 无 `.*` 长度上界,会跨行/跨段误命中。

**Fix**: 备选 regex 收紧为 `r"^>\s*.*?(?:入口|handoff|session)[^()\n]{0,80}\(([^)]+\.md)\)"`(加 `^>` + 长度上界 80)。或 G3 仅保留主 regex,alias 机制延后到 follow-up Spec。T3.3 必须含 "函数入口" / "调试入口" 两个误命中负例。

### C-3 [QA-01] `git.status_clean` 字段不存在 — silent failure 风险

**Scope**: T5 SKILL.md L175 (post-merge SKILL.md) + `collectors/git.py` schema

**Detail**: T5 兜底触发条件 1 引用 `git.status_clean == true`,但 `collectors/git.py` 只产出 `staged_files[] / unstaged_files[] / uncommitted_count`,**无 `status_clean` 字段**。降级后 SKILL.md 仍依此字段 → silent always-false → sanity check 永不触发 → Spec 核心价值(从 AI 兜底升级到机械化 sanity check)落空。

**Fix**(任一):
- A(推荐): T2.x 任务前增 prerequisite — `collectors/git.py` 加 derived 字段 `status_clean: staged_files == [] and unstaged_files == []`,schema 文档同步
- B: TX.2 降级文本改用复合条件 `git.staged_files == [] and git.unstaged_files == []`(无新字段,SKILL.md 更冗长)

### C-4 [QA-02] 9 个 test cases 不足以覆盖 G2/G3/G4 三处 ≥17 边界

**Scope**: Success Criteria L217 "≥ 380 pass (371 baseline + ≥9 新增)"

**Detail**: G2 单独 8 类 (T2.3 列出) + G3 5-6 类 + G4 ≥3 类 (排序 + mtime tiebreak + N=0) = 总 ≥16 cases。Spec 只承诺 ≥9。允许实现者只写 G2 的 8 个 case 后宣告 PASS,完全跳过 G3/G4 边界。

**Fix**: Success Criteria 改成分项计数:
- G2 ≥ 8 cases (T2.3 8 场景一一对应)
- G3 ≥ 5 cases
- G4 ≥ 4 cases
- 总计 ≥ 17 → baseline 372 + 17 = ≥389 (注: KM-05 指出 baseline 应为 372 不是 371)

### C-5 [QA-03] `raw_row` 大文本未进 normalize_snapshot DROP_KEYS — 加剧已知 flake

**Scope**: TX.1 / TX.3 / `aria/skills/state-scanner/scripts/normalize_snapshot.py`

**Detail**: G2 每个 followup 含 `raw_row` 逐字 UPM 原文。`normalize_snapshot.py` 现有 10 条规则不处理 `followups[]`。已知 flake `test_two_consecutive_runs_diff_zero` 会因 `raw_row` 引入新 drift 来源 (尾部空白 / 内嵌绝对路径 / timestamp-ish 自由文本均不脱敏)。

**Fix**: TX.1 加子任务 — `followups[*].raw_row` 进 DROP_KEYS (类似 recent_commits 处理),或替换为 `<raw_row>` sentinel。`test_normalize_snapshot.py` 加 followups/handoff_doc/priority_items 的 normalize 规则覆盖 case。

---

## Major Findings (Should Fix)

> 不阻塞 R2,但建议在 R2 前合并修订一次。

| ID | Scope | Issue | Suggested Fix |
|---|---|---|---|
| M-1 [TL-1] | TX.3 AB benchmark | 单次 AB 含 (a) 三新字段 + (b) 两规则 + (c) T5 降级三变量,delta 归因不可分 | 拆三 arm: A=baseline / B=new collectors only / C=new + T5 降级。或 TX.2 拆为 follow-up Spec |
| M-2 [TL-2] | Rule priority 1.85/1.88 | 注释 "介于 multi_remote_drift (1.35) 与 readme_outdated (1.3) 之间" 数学错误 (1.85 远 > 1.35) | 修注释为 "位于 architecture_chain_broken (1.8) 与 audit_unconverged (1.9) 之间";加 priority ordering rationale |
| M-3 [BA-03] | T2.2 heading regex | 大小写敏感性 / 前导空格 / heading 与表间内容均未定义 | T2.2 显式 regex `r"^[ \t]{0,3}#{2,3}\s+Pending Followups\s*$"`;允许 heading 后任意非表格行直至 `\|` 起始行 |
| M-4 [BA-04] | T4.2 排序 tie-break | 同 status + 同 mtime 时 tie-break 未定义,跨 OS jitter | 三级排序 `status_order ASC → mtime DESC → path LEX ASC` 显式;或 mtime 仅 advisory + path/id LEX 作 stable key |
| M-5 [BA-05] | RECOMMENDATION DSL | `condition: ... \| filter ... \| count > 0` 是新 DSL 还是伪代码歧义 | Spec 必须 (A) 引用现有 DSL 格式 / (B) 标注为伪代码 + 等价 Python / (C) 加 DSL 解析器扩展任务 |
| M-6 [QA-04] | TX.3 fixture 简化边界 | "SilkNode 简化版" 简化到何程度未定义 | 显式最小规格: followups 6 行 (P1×2/P2×2/P3×2) + handoff stub + 1 negative no-table + 1 negative path-not-exist + 1 in_progress + 1 pending US |
| M-7 [QA-05] | Success Criteria AB delta | "≥ 0,理想 +5pp 以上" hard 还是 best-effort 未区分 | 拆双层: PASS gate `delta ≥ 0`(阻塞);Quality target `delta ≥ +5pp`(不阻塞,记录 benchmark.md);对比基准明确为 without_skill |
| M-8 [QA-06] | TX.5 backward-compat | "consumer 不抛 KeyError" 无具体 fixture/mock | TX.1 加 — test_upm.py + test_requirements.py 加 ≥2 个 case,验证 `.get('followups', [])` 等防御性访问;TX.5 改成"主项目 submodule 指针 bump"(不变);新增 TX.6 backward-compat verify |
| M-9 [QA-07] | T4.2 mtime 风险未列入 Impact | git clone 平铺 mtime → priority_items 排序退化为 glob 顺序,加剧 issue #61 cross-platform | Impact 风险表加第 4 项;方案 A: tie-break 改 US id 字典序 + mtime 仅 advisory;方案 B: priority_items 进 normalize DROP_KEYS |
| M-10 [QA-08] | T4.2 ready 状态 normalize | `_normalize_status('ready')` 行为未确认,T4.4 测试范围模糊 | T4.4 显式 — 加 `**Status**: Ready` / `**状态**: 就绪` 的 normalize 测试,确保 T4.2 过滤器 ready 命中 |
| M-11 [KM-01] | TX.2 降级措辞无 mock | "降级为 sanity check" 边界模糊 (4 条件 + 3 行动 全删?半删?) | TX.2 加 mock 段落示例 (建议保留单一 sanity check 触发条件 "字段缺失但 UPM 含 Pending Followups 表",约 7 行替换原 17 行) |
| M-12 [KM-02] | system-architecture.md 同步 | CLAUDE.md Rule #3 对齐缺失 | Out of Scope 加一项: "system-architecture.md 不枚举 snapshot 字段,本次新增字段无需修改" 或加入 TX.1 |

---

## Minor Findings (Nice to Have)

| ID | Issue | Fix |
|---|---|---|
| m-1 [TL-3] | dogfooding 时机/CI 接入未声明 | TX.6 任务: PR merge 前在 Aria + Kairos + Aether 三项目本地跑 scan.py 并附日志/截图;CI 接入留 future Spec |
| m-2 [TL-4] | G2/G3/G4 并行策略未声明 | Tasks 段开头加: "G2/G3/G4 三组无文件冲突可并行;Cross-cutting TX.* 串行待 G2-G4 全部 merge 后" |
| m-3 [BA-06] | handoff path 格式覆盖 | T3.2 加 URL/绝对路径/相对路径三态分支 |
| m-4 [BA-07] | upm.py 拆 sub-module | Spec 加一行: 实现者 PR author 自决拆与否,无需另起 Spec |
| m-5 [BA-08] | pipe escape parser | T2.2 显式: 替换 `\\|` 为占位符 `\x00`,split('\|'),还原 |
| m-6 [QA-09] | G3 raw_match 示例 | 补"裸路径无括号"的 negative test 或显式 scope out |
| m-7 [QA-10] | scan.py latency | T2.2/T2.5 加性能预算 < 50ms (200/1000 行 UPM) |
| m-8 [KM-03] | G1 孤儿 issue 时限 | Out of Scope G1 条目加: "保留 issue #85 open;若 2026-05-22 前无数据由 Tech Lead 决策关闭/降优;G1 单独 Spec 不修本 Spec" |
| m-9 [KM-04] | TX.1 schema 顺序 vs 规范先行 | TX.1 描述加: "应在 T2.2/T4.2 实现开始前完成";Tasks 排序提前 |
| m-10 [KM-05] | baseline 371 vs 实际 372 | Success Criteria 改 "372 baseline + ≥17 新增 = ≥389"(配合 C-4) |
| m-11 [KM-06] | priority 注释笔误 | 同 M-2 修复 |

---

## Conclusion Records (4-tuple comparison keys)

> 用于 R2 收敛判定。比较键 = `{type, severity, category, scope}`。

```yaml
round_state:
  round: 1
  conclusions:
    # Critical (5)
    - {type: issue,    severity: critical, category: implementation,  scope: G4-T4.2-priority-items-deduplication}
    - {type: risk,     severity: critical, category: implementation,  scope: G3-handoff-fallback-regex-overmatch}
    - {type: issue,    severity: critical, category: implementation,  scope: TX.2-git-status-clean-field-missing}
    - {type: issue,    severity: critical, category: testing,         scope: success-criteria-test-count-gap}
    - {type: risk,     severity: critical, category: testing,         scope: TX.1-raw-row-normalize-flake-amplifier}
    # Major (12)
    - {type: risk,     severity: major,    category: testing,         scope: TX.3-ab-benchmark-three-variable-confound}
    - {type: issue,    severity: major,    category: documentation,   scope: priority-1.85-1.88-anchor-typo}
    - {type: issue,    severity: major,    category: implementation,  scope: T2.2-heading-regex-case-leading-space}
    - {type: risk,     severity: major,    category: implementation,  scope: T4.2-tie-break-cross-os-jitter}
    - {type: issue,    severity: major,    category: architecture,    scope: recommendation-rule-dsl-pseudocode-ambiguity}
    - {type: issue,    severity: major,    category: testing,         scope: TX.3-fixture-simplification-undefined}
    - {type: issue,    severity: major,    category: testing,         scope: success-criteria-ab-delta-hard-vs-soft}
    - {type: issue,    severity: major,    category: testing,         scope: TX.5-backward-compat-no-fixture}
    - {type: risk,     severity: major,    category: testing,         scope: T4.2-mtime-flakiness-not-in-impact}
    - {type: issue,    severity: major,    category: implementation,  scope: T4.2-ready-status-normalize-undefined}
    - {type: issue,    severity: major,    category: documentation,   scope: TX.2-downgrade-mock-missing}
    - {type: issue,    severity: major,    category: documentation,   scope: system-architecture-md-sync-unstated}
    # Minor (11)
    - {type: issue,    severity: minor,    category: testing,         scope: dogfooding-timing-ci-unstated}
    - {type: decision, severity: minor,    category: implementation,  scope: G2G3G4-parallel-strategy-unstated}
    - {type: issue,    severity: minor,    category: implementation,  scope: T3.2-handoff-path-format-coverage}
    - {type: decision, severity: minor,    category: architecture,    scope: upm-py-submodule-split-decision}
    - {type: issue,    severity: minor,    category: implementation,  scope: T2.2-pipe-escape-strategy-undefined}
    - {type: issue,    severity: minor,    category: testing,         scope: T3.3-bare-path-format-test}
    - {type: risk,     severity: minor,    category: testing,         scope: T2.2-scan-latency-budget}
    - {type: issue,    severity: minor,    category: documentation,   scope: G1-orphan-issue-deadline}
    - {type: decision, severity: minor,    category: documentation,   scope: TX.1-schema-doc-order}
    - {type: issue,    severity: minor,    category: documentation,   scope: success-criteria-baseline-371-vs-372}
    - {type: issue,    severity: minor,    category: documentation,   scope: priority-1.85-1.88-anchor-typo-followon}  # KM-06 follow-on
  vote: REVISE
  incomplete: false
  timestamp: 2026-05-08T02:30Z
```

**总条目: 28** (5 critical + 12 major + 11 minor)

---

## R2 Recommendation

**Path A — 修 Critical + Major 后跑 R2 (推荐)**:
- 5 Critical 必修 (FAIL 阻塞)
- 12 Major 至少修一半 (M-1 / M-2 / M-7 / M-8 / M-11 / M-12 优先,因影响 ship 决策可信度或方法论对齐)
- Minor 可批量批注/不修 (留 implementation 阶段酌情)
- 修订后 R2 用同 4 agent team 跑 fix-verify,期望 R2 收敛 PASS_WITH_WARNINGS 或 PASS

**Path B — 接受当前结论 (overridden_by_user)**:
- 标记 `converged: false, overridden_by_user: true`
- 5 Critical issue 转入 Phase B 实施时由 implementer 自行处理
- 风险: implementer 缺乏 spec 锚点会自由发挥,review 时返工成本高

**Path C — 降级单轮 (degraded)**:
- 取 R1 结论作为最终
- 标记 `converged: false, degraded: true`
- 风险同 Path B 但更弱 (无 fix-verify 信号)

---

## Files Reviewed

- `/home/dev/Aria/openspec/changes/state-scanner-inter-cycle-surfacing/proposal.md` (243 行)
- `/home/dev/Aria/aria/skills/state-scanner/scripts/collectors/upm.py` (136 行)
- `/home/dev/Aria/aria/skills/state-scanner/scripts/collectors/requirements.py` (74 行)
- `/home/dev/Aria/aria/skills/state-scanner/scripts/collectors/_status.py`
- `/home/dev/Aria/aria/skills/state-scanner/scripts/normalize_snapshot.py`
- `/home/dev/Aria/aria/skills/state-scanner/SKILL.md` (T5 段 L172-187)
- `/home/dev/Aria/aria/skills/state-scanner/RECOMMENDATION_RULES.md` (priority 表)
- `/home/dev/Aria/aria/skills/state-scanner/references/state-snapshot-schema.md`
- Forgejo issue 10CG/Aria#85
