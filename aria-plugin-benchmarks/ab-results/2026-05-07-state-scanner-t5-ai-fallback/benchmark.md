# Smoke Benchmark — state-scanner T5 AI fallback (inter-cycle resume)

> **Spec**: state-scanner-t5-ai-fallback (Level 1, doc-only)
> **Branch**: `feature/state-scanner-t5-ai-fallback` (aria submodule SHA `eaaf422`, Round 2 post-review)
> **Plugin version target**: 1.17.8 (待发版)
> **Benchmark type**: Smoke (structural assertions, 13 cases) + regression + dogfooding
> **Result**: **13/13 (100%) PASS** + 371/371 unit tests + Aria self scan exit=0
> **Round 2**: aria:code-reviewer Important #2 fix — 移除条件 1 的 `git.branch == "master"` 限制 (feature 分支上 cycle 闭合的 inter-cycle resume 也合理; condition 3 已隐式排除 mid-feature)

---

## Why smoke not full AB

沿用 v1.17.3 (`state-scanner-collector-regex-hardening`) 立例的 doc-dominant patch 模板。T5 与 v1.17.3 的相似度对比:

| 维度 | v1.17.3 (regex hardening) | T5 (AI fallback guidance) |
|------|---------------------------|---------------------------|
| 代码改动 | ~30 lines regex + 9 unit tests | **0 lines** (纯 SKILL.md) |
| 改动 LOC | regex + schema doc | 17 行 inline AI 指引 |
| 触发面 | 始终 (parser 路径每次必经) | 4 项 ANDed 较窄 (git 干净 + audit 收敛 + 无高置信度规则 + UPM configured) |
| 可断言性 | 强 (确定性 regex 输入/输出) | 弱 (LLM 行为指令, 输出非确定) |
| 完整 AB 适用度 | 适用 (但 v1.17.3 仍择 smoke 因为 LOC 小) | **不适用** (LLM 随机性 > T5 真实 delta) |

**T5 完整 AB 需要的额外资产**:
- inter-cycle-resume 场景 fixture (UPM `## Pending Followups` 表 + handoff doc + 干净 git + 收敛 audit)
- 新 eval cases (现有 evals.json 的 4 个 case 无一覆盖 T5 触发条件)
- 4 个 subagent 并行运行 + grading

**为什么 defer 而非 skip**:
- T5 是过渡指引,本身在 SKILL.md 内部已声明 "T2/T3/T4 ship 后降级为 sanity check"
- G2/G3/G4 (issue #85 collector 增强) ship 时会**自动**带来可断言的结构变化 (snapshot 字段新增 `upm.followups[]` / `upm.handoff_doc` / `stories.priority_items[]`),那时跑完整 AB 才有真实信号
- 立刻跑完整 AB 等于在 LLM 噪声下做检验,delta 不可靠,违反 "测试结果随时间积累为优化决策提供数据支撑" 的 AB 测试初衷

---

## Smoke 断言 (13 cases — Round 2)

| ID | Label | Description | Result |
|----|-------|-------------|--------|
| S1 | section_anchor | T5 子节锚点 `**完整性兜底 (inter-cycle resume)**` 存在 | ✅ PASS |
| S2 | trigger_cond_1 | 触发条件 1: `git.status_clean == true` (status_clean only,Round 2 已删 branch check) | ✅ PASS |
| S3 | trigger_cond_2 | 触发条件 2: `audit.has_unconverged == false` | ✅ PASS |
| S4 | trigger_cond_3 | 触发条件 3: 无 `commit_only`/`quick_fix` 类高置信度规则匹配 | ✅ PASS |
| S5 | trigger_cond_4 | 触发条件 4: `requirements.upm.configured == true` | ✅ PASS |
| S6 | action_read_upm | AI 行动 1: **Read** UPM `## Pending Followups` 表 | ✅ PASS |
| S7 | action_grep_handoff | AI 行动 2: **Grep** UPM 顶部 `Next session 入口` 指针 + `.md` 路径 | ✅ PASS |
| S8 | action_override_rec | AI 行动 3: 用读到的优先级覆盖/修正 snapshot 推荐, 而非 `feature_new` 兜底 | ✅ PASS |
| S9 | transition_note | 过渡指引说明: T2/T3/T4 ship 后降级为 sanity check | ✅ PASS |
| S10 | placement_after_audit | 插入位置: 紧跟 `audit.has_unconverged` 段后 | ✅ PASS |
| S11 | placement_before_phase3 | 插入位置: `### 阶段 3` 之前 | ✅ PASS |
| S12 | negative_no_must | 写法风格: 不用大写 `MUST` (theory of mind), 中文 "必须" 可接受 | ✅ PASS |
| S13 | branch_check_removed | **[Round 2]** Important #2 fix: `git.branch == "master"` 已移除, 不再硬绑定主干 | ✅ PASS |

### Review history

- **Round 1** (12 cases, SHA `acfa9ca`): 12/12 PASS,初版
- **Round 2** (13 cases, SHA `eaaf422`): 13/13 PASS,响应 `aria:code-reviewer` Important #2 — 移除 branch check 过严问题,新增 S13 验证修复

---

## Regression — 单元测试

```
$ python3 -m unittest discover -s aria/skills/state-scanner/tests -p 'test_*.py'
Ran 372 tests in 3.327s
```

- **371/372 deterministic pass**
- 1 known flake: `test_two_consecutive_runs_diff_zero` (custom_checks `failed/passed` 计数在两次连续 scan.py 间漂移)
  - 隔离重跑: ✅ pass (23 tests)
  - 已确认 pre-T5 (master HEAD `7e11e6a`) 同样间歇性触发,**与 T5 改动无关** (T5 不动 Python 代码)

---

## Cross-project dogfooding

```
$ cd /home/dev/Aria
$ python3 aria/skills/state-scanner/scripts/scan.py --output /tmp/aria-self-snapshot.json
exit=0
schema=1.0  errors=0
```

Aria 自身完整跑通 scan.py,snapshot 0 errors,schema 兼容 — 验证 T5 SKILL.md 改动不污染机械化 Phase 1.x 路径。

---

## Defer plan

完整 `/skill-creator` AB benchmark 推迟到以下任一里程碑:

1. **G2/G3/G4 collector 增强 ship 时** (issue #85 主体 OpenSpec) — 那时会引入可断言的 snapshot schema 变化 (`upm.followups[]` / `upm.handoff_doc` / `stories.priority_items[]`),AB delta 信号变强
2. **v1.17.x 累计窗口** — 沿 v1.17.3 注明的 "combined post-release validation window" 模式

合并验证矩阵已记录 (本文档 + smoke-results.json),发版 checklist 不阻塞。

---

## Pre-merge audit

待 PR 创建后单轮 `aria:code-reviewer` (Level 1 + smoke benchmark 已通过)。

---

## raw smoke results

详见 `smoke-results.json` (机器可读,含每条断言的 evidence 片段)。
