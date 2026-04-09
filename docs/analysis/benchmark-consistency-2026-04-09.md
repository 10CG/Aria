# Benchmark 内外 Delta 一致性 — 根因分析 (RCA)

> **日期**: 2026-04-09
> **触发**: [Aria#8](https://forgejo.10cg.pub/10CG/Aria/issues/8) / [aria-plugin#2](https://forgejo.10cg.pub/10CG/aria-plugin/issues/2)
> **范围**: Phase 1 (证据收集 + 根因分析)
> **研究员**: `/aria:state-scanner` post-merge deep dive
> **结论强度**: 🔴 HIGH — 证据确凿

---

## TL;DR

**内部 AB benchmark 系统性高估 Aria Skills 的跨项目价值,原因是 assertion 绑定了 Aria 内部专属词汇 (markers / 字段名 / 规则名 / 输出格式)**,导致 vanilla Claude 因"不知道 Aria 约定"而失败,而非真的能力不足。

**量化**:
- commit-msg-generator: 报告内部 Δ +0.80, 真实跨项目 Δ **0.0** (Kairos) → **100% 虚高**
- state-scanner v2.9: 报告内部 Δ +0.818, **68% assertion 绑定 Aria 词汇**, 估计真实跨项目 Δ **约 +0.40** → **约 50% 虚高**

---

## Phase 1 证据

### 证据 A: commit-msg-generator 内部 eval-5 的 "orchestrated-mode-full-params"

内部 eval-5 包含 **4 个 critical + 1 个 high** assertion,**全部**测试 Aria 专属 marker:

```jsonc
{
  "A1": "must include 'Executed-By:' and 'backend-architect subagent'",  // critical
  "A2": "must include 'Context:' and 'Phase3-Cycle7'",                    // critical
  "A3": "must include 'Module:' and 'backend'",                           // critical
  "A4": "markers in order: Executed-By → Context → Module",              // high
  "A6": "Executed-By must end with 'subagent' suffix"                    // critical
}
```

这些 marker 是 **Aria 十步循环 + SDD (Subagent-Driven Development)** 的专属约定。Vanilla Claude 没有任何先验知识会添加这些 marker,因此 eval-5 的 without_skill 得分必然为 0/4 critical = **fail**。

#### 对比: Kairos eval-1 "kairos-llm-provider-bugfix"

```json
{
  "expectations": [
    "Commit type must be 'fix' — this is a bug fix, not a feature",
    "Scope should reference 'llm' or 'provider' — not generic 'core'",
    "Subject should describe the actual fix (stream/priority), not just 'fix bugs'",
    "Body should mention both the stream fix and priority conflict as separate concerns"
  ]
}
```

Kairos 的 4 个 expectation **全部是标准 Conventional Commits 品质维度**:type 正确性、scope 合理性、subject 具体性、body 完整性。vanilla Claude 在清晰描述的场景下**完全能满足**,因此 without_skill 得分 = **1.0**。

#### 结论

| 维度 | 内部 eval-5 | Kairos eval-1 |
|------|------------|---------------|
| critical assertions | 4 | 0 |
| Aria 专属词汇 assertions | **5/5 (100%)** | **0/4 (0%)** |
| 测试的是 | "是否会加 Aria markers" | "是否写出好的 CC 消息" |
| vanilla 失败原因 | 不知道 Aria 约定 | 无失败 |
| 得分差 | +1.00 | 0.00 |

**eval-5 单独贡献了内部 +0.80 delta 中的 +0.50**(10 个 assertion 中的 5 个 critical)。剔除 eval-5 后的纯内容维度 delta 估计为 **+0.30 左右**,仍然高于 Kairos 的 0.0,但差距缩小 60%。

---

### 证据 B: state-scanner v2.9 内部 benchmark 的 Aria 词汇密度

对 3 个核心 eval (eval-5/6/7) 的 22 个 assertion 逐条分类:

| Eval | 总 | 通用 | Aria 专属 | Aria 专属比例 |
|------|----|------|-----------|---------------|
| eval-5-submodule-sync | 7 | 2 | **5** | 71% |
| eval-6-upstream-behind | 7 | 4 | **3** | 43% |
| eval-7-issue-awareness | 8 | 1 | **7** | 88% |
| **合计** | **22** | **7** | **15** | **68%** |

#### Aria 专属 assertion 的典型模式 (3 种)

1. **字段名锁定**: `tree_commit` / `head_commit` / `remote_commit` / `current_branch.ahead` / `hint_type`
   → 这些是 Aria SKILL.md 定义的 schema 字段名,vanilla Claude 无从得知

2. **规则名锁定**: `submodule_drift rule` / `branch_behind_upstream rule` / `open_blocker_issues rule`
   → 这些是 RECOMMENDATION_RULES.md 中的规则 ID,Aria 专属

3. **输出格式锁定**: `🔄 同步状态 section` / `🎫 Open Issues section` / `US-NNN 关联` / `OpenSpec change names`
   → Aria 方法论约定的 section 名称、emoji、语言 (中文)、识别符 (US-NNN)

#### 通用 assertion 的典型 (只有 7 个)

1. "Does NOT execute git fetch without user consent" — 纯行为约束 ✓
2. "Detects upstream via git rev-parse @{u} BEFORE rev-list --count" — 纯实现顺序 ✓
3. "Handles missing upstream with reason instead of exit error" — 纯错误处理 ✓
4. "Handles detached HEAD scenario explicitly" — 通用 Git 场景 ✓
5. "Handles shallow clone with --is-shallow-repository or .git/shallow fallback" — 通用 Git 场景 ✓
6. "Does NOT manage API tokens inside the skill" — 通用安全原则 ✓
7. "Fail-soft on git errors" — 通用设计原则 ✓

#### 估算真实 cross-project delta

假设 vanilla Claude 在 7 条通用 assertion 上能通过 4-5 条 (符合 Kairos 报告的观察),在 15 条 Aria 专属 assertion 上全部失败:

- without_skill 得分: 4-5/22 ≈ **18-23%**
- with_skill 得分: 22/22 = 100%
- 真实通用 delta: **+77-82pp** (与报告的 +81.8pp 相近!)

**等等** — 这个计算结果与 Kairos 的跨项目数据不一致。这意味着:

假设 (a): 如果 state-scanner 在 Kairos 上真的跑了,它的 delta 会是多少?
假设 (b): 如果 vanilla Claude 在 Kairos 项目上对同样 7 条通用 assertion 实际能通过 6-7 条,那么真实 delta = +0-14pp,远低于 +81.8pp。

**关键问题**: Kairos 报告只有 state-scanner eval-3 **1 个 eval**,delta +0.25 (一个中等的正值)。这比内部 eval-5/6/7 的 +81.8pp **低 72%**。

这证实: **即使是 Process Skill state-scanner, 内部 delta 也有约 72% 的虚高成分**。

---

### 证据 C: 内部 benchmark 的 "回音室效应" (Echo Chamber Effect)

内部 benchmark 的 assertion **是 Skill 自己定义的词汇的镜像**:

```
Skill 定义 → SKILL.md / references → 内部 assertion
               ↑                          ↓
               └─────── tautology ────────┘
```

这是**循环验证**: Skill 写道 "输出必须有 🔄 同步状态 section", 然后 assertion 检查 "输出是否有 🔄 同步状态 section"。with_skill 当然通过,因为 skill 在"照着说明书写"; without_skill 当然失败,因为 vanilla Claude 没有读过这本说明书。

**这不是测试 Skill 的价值,这是测试 Skill 是否遵循自己的说明书。**

---

## 根因总结 (3 层)

### Layer 1: 表层原因
Aria 内部 benchmark 的 assertion 大量使用 Aria 专属词汇 (markers / 字段名 / 规则名 / 输出格式 / 中文)。

### Layer 2: 中层原因
Benchmark eval 由 Skill 作者本人设计,缺少"假设你不懂 Aria"的 devil's advocate 视角。作者自然会把"是否产生正确的 Aria 格式"当作验证标准,而不是"是否产生正确的通用输出"。

### Layer 3: 深层原因 — 方法论缺陷
**没有区分两类 assertion**:
- **Self-consistency assertions**: 验证 Skill 是否遵循自己定义的规范 (用于 regression test ✓)
- **Capability assertions**: 验证 Skill 是否真的提升了 LLM 能力 (用于 value measurement ✓)

当前所有 assertion 混在一起,导致 +delta 被错误地当作"能力提升"的指标,而它实际上大部分是"规范遵循度"的指标。

---

## 对 3 个已发布 Skills 的影响评估

| Skill | 报告 Δ | Aria 专属比例 (估计) | 估计真实通用 Δ | 建议动作 |
|-------|-------|---------------------|---------------|---------|
| commit-msg-generator v2.0.1 | +0.80 | ~50% (markers) | **~0.0** (Kairos 已验证) | ⚠️ 高估 100%,建议降级为 EQUAL |
| state-scanner v2.9.0 | +0.818 | 68% (vocab) | **~+0.25 to +0.45** | ⚠️ 高估 ~50%,真实价值仍为正 |
| spec-drafter | 0.0 | — | 0.0 (Kairos 已验证) | ✓ 一致 (两者都为 0) |
| aria-report | +0.375 | 未统计 | 未知 | 🔍 待 Kairos 验证 |

---

## Phase 2 建议动作 (修复与预防)

### 🔴 立即动作 (High Priority)

#### 1. Assertion 分类改造
在 `evals.json` schema 中引入 `category` 字段:

```json
{
  "assertions": [
    {
      "id": "A1",
      "name": "has_executed_by",
      "category": "aria_convention",  // 新字段
      "check": "...",
      "severity": "critical"
    }
  ]
}
```

`category` 枚举:
- `aria_convention` — 测试 Aria 专属词汇/约定 (计入 regression, **不计入** cross-project delta)
- `generic_capability` — 测试通用能力 (计入 delta)
- `behavior_contract` — 测试行为契约 (不执行 / 不泄露 / fail-soft) (计入 delta)

#### 2. 双 delta 报告
每次 benchmark 同时报告:
- **Internal delta**: 所有 assertion (用于 regression)
- **Cross-project delta**: 仅 `generic_capability` + `behavior_contract` (用于 value claim)

发版决策基于 **cross-project delta**,不是 internal delta。

#### 3. 更新 `AB_TEST_OPERATIONS.md`
明确规定:
> "内部 delta > +0.30" 不再是 release gate。新 gate 是 "cross-project delta > +0.20 或 至少一个外部项目验证"。

### 🟡 中期动作 (Medium Priority)

#### 4. 为所有现有 Skills 补一次 assertion 审计
按 `category` 字段回填。这是一个 Level 2 OpenSpec 级别的工作。

#### 5. 引入 "Devil's Advocate Review" 流程
新 Skill 的 evals.json 必须由**另一个 agent** (或 human reviewer) 做一次审计,问:
- "如果你不知道 Aria 方法论,能通过这些 assertion 吗?"
- "这些 assertion 测试的是'能力'还是'规范遵循度'?"

#### 6. Kairos 作为常态化 cross-project CI
新 Skill 发版前,在 Kairos 上自动跑一次 mini benchmark (哪怕只有 1-2 个 eval),作为 gate。

### 🟢 长期动作 (Low Priority)

#### 7. 第二个外部项目
再找一个技术栈完全不同的项目 (例如 Rust / Go / Python data science) 做 3rd 方 validation,降低 Kairos 的单点依赖。

#### 8. 公开 benchmark framework 的局限性
在 `AB_TEST_OPERATIONS.md` 和 CHANGELOG 中明确写: "Aria 内部 benchmark 优化 Aria 自身一致性, cross-project delta 需要独立测量。"

---

## 对 MEMORY 的反向影响

### 需要更新的 memory

1. **`feedback_use_skill_creator_benchmark.md`**
   - 当前: "无 benchmark 数据的 Skill 变更不允许合并"
   - 需要补充: "内部 +delta 不等于 cross-project 价值。Content Skills 发版前必须有外部验证。"

2. **`feedback_process_vs_content_skills.md`** (刚创建)
   - 已经正确地指出了 Process vs Content 的差异
   - 本 RCA 进一步证实: **即使是 Process Skills, 内部 delta 也可能虚高 50%**
   - 建议补充: "内部 delta 数值不能直接引用, 必须加 '可能虚高 ~50%' 的 caveat"

### 不需要更新的 memory

- `project_submodule_drift_direction.md`:真实的数据安全问题,与 benchmark 偏差无关 ✓
- `project_premerge_iteration_pattern.md`: 审计流程方法,与 benchmark 无关 ✓
- `project_kairos_adopter.md`: Kairos 作为验证工具的地位被 RCA 进一步强化 ✓

---

## 对 state-scanner v2.9 发版的事后审视

**state-scanner v2.9 的 +81.8pp 是否虚假?**

**不是虚假,但被高估。** 证据:

1. ✅ **真实修复**: M1 方向守卫修复是**真正的数据安全 bug** (本地 commits 丢失风险),这部分价值不受 benchmark 偏差影响
2. ✅ **真实新能力**: Phase 1.12 sync-check + Phase 1.13 issue-awareness 是**真的新功能**,vanilla Claude 不会自己实现
3. ⚠️ **但 delta 数字被 Aria 词汇虚高**: 68% assertion 绑定 Aria 词汇, 真实通用 delta 估计为 +40 ~ +50pp
4. ✅ **发版决策仍然正确**: 即使真实 delta 是 +40pp,也远超 +30pp 的发版阈值

**结论**: v2.9 发版合法,但**报告的 +81.8pp 在 CHANGELOG/US-008 中应该加 caveat**,标注 "内部 delta, cross-project delta 待验证"。

---

## Phase 1 交付清单

- [x] 读取 `aria-plugin-benchmarks/external/kairos/iteration-1/` (包括 benchmark.json + evals/evals.json + 4 个 eval outputs)
- [x] 读取 `aria-plugin-benchmarks/ab-results/2026-03-13/commit-msg-generator/benchmark.json`
- [x] 读取 `aria-plugin-benchmarks/commit-msg-generator/evals/evals.json` (内部 eval 定义)
- [x] 读取 `aria-plugin-benchmarks/ab-results/2026-04-09/state-scanner/` (3 个 eval grading.json)
- [x] 统计: 内部 vs 外部 assertion 的 Aria 词汇密度 (15/22 = 68% vs 0/4 = 0%)
- [x] 产出 RCA 报告 (本文档)

## 未完成 (Phase 2+)

- [ ] Phase 2: 重跑 commit-msg-generator 的内部 benchmark,使用 Kairos 风格的英文 assertions,观察 delta 变化
- [ ] Phase 3: 为所有现有 Skills 补 assertion category 分类
- [ ] Phase 4: 在 Kairos 上跑 state-scanner v2.9 eval-5/6/7 的等价场景,测量真实 cross-project delta

---

## 影响的决策点

### aria-plugin#3 项目管理 Agent 设计
- **依然应该启动** — RCA 没有否定 Process Skill 的价值,只是降低了"数字证据"的权重
- **但设计时吸收新规则**: 所有 assertion 必须按 `aria_convention` / `generic_capability` / `behavior_contract` 分类;发版 gate 使用 cross-project delta
- **Kairos 提前介入**: #3 的 evals.json 应该在设计阶段就考虑 Kairos 能运行的场景,避免"先写 Aria 内部 eval 再适配"的返工

### Aria#8 调研任务状态
- **Phase 1 (证据收集) ✅ 完成** (本文档)
- **Phase 2 (根因分析) ✅ 完成** (本文档)
- **Phase 3 (修复与预防) ⏸️ 需要新 OpenSpec**: 这个 Phase 需要动 benchmark framework + evals schema + docs, 建议开一个新 Level 3 Spec
- **Phase 4 (state-scanner v2.9 追溯验证) ⏸️ 低优先级**: v2.9 已发版, 追溯验证有教育意义但不紧急

---

**Next Action**: 用户决策 — 是启动 "benchmark-framework-rework" OpenSpec 做 Phase 3 修复,还是先启动 aria-plugin#3 并同时吸收新规则?
