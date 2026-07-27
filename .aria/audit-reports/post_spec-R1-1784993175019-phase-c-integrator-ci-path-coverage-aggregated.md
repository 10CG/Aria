---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-07-25T16:05:00.000Z
context: phase-c-integrator-ci-path-coverage
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 (aggregated) — phase-c-integrator-ci-path-coverage

## Anchor (Step 0, 固化于 R1 启动前, 审计周期内不可变)

- **checkpoint**: post_spec / **mode**: convergence / **max_rounds**: 4
- **primary_goal**: 消除 C.2.4 gate 对路径过滤型 CI 的结构性恒 wait, 且不放过任何真该拦的 CI
- **in_scope**: `pre_merge_gate.py` verdict 链路 / `aether.py::_normalize_pr_ci_status` / 新增 `lib/ci_path_coverage.py` / `SKILL.md §C.2.4` 契约 / 测试 / 配置键 `path_coverage_aware`
- **out_of_scope_hints**: N1 `branches:` 感知 / N2 `github_actions.py` stub / N3 `_open_question_no_ci_fallback` (owner 待裁, 正交) / N4 race condition
- **source_sha**: `194a73b`

## 各 agent verdict

| Agent | Verdict | Critical | Major | Minor | SCOPE |
|-------|---------|----------|-------|-------|-------|
| tech-lead | FAIL | 3 | 8 | 4 | SCOPE_OK |
| backend-architect | FAIL | 2 | 4 | 3 | SCOPE_OK |
| qa-engineer | FAIL | 2 | 3 | 5 | SCOPE_OK |
| code-reviewer | FAIL | 5 | 8 | 5 | SCOPE_OK |
| knowledge-manager | PASS_WITH_WARNINGS | 0 | 1 | 4 | SCOPE_OK |

**聚合 verdict: FAIL** (≥1 critical)。5/5 agent 完成, `incomplete: false`。5/5 SCOPE_OK, 无 drift。

## Finding 簇 (跨 agent 去重后, comparison_key = {type, severity, category, scope})

| 簇 | severity | category | scope | 命中席位 | 摘要 |
|----|----------|----------|-------|----------|------|
| **A** | critical | architecture | `pre_merge_gate.py:184-194` | tech-lead, code-reviewer | `compute_verdict` catch-all 是 `else → green`。`not_found` 上岗把它从不可达变可达。**code-reviewer 实跑**: `compute_verdict([], "not_found") → green`, `([], "totally_bogus") → green`。附带: AC-1/AC-3 在「一行不改」的实现上也通过 ⇒ AC 集合无法区分正确实现与白嫖 fail-OPEN |
| **B** | critical | implementation | proposal §What 4 × §What 1 | tech-lead, backend-architect, code-reviewer, knowledge-manager | `path_coverage_aware=false` 语义自相矛盾。`_normalize_pr_ci_status` 是 staticmethod 拿不到 config ⇒ `not_found` 无条件生产 ⇒ 照字面「完全跳过 §2/§3」实现则落簇 A 的 catch-all ⇒ green。**向后兼容出口成为唯一假绿入口, 用户越保守越危险** |
| **C** | critical | architecture | proposal §What 2/3 × `pre_merge_gate.py:261-265`,`:365-374` | tech-lead, backend-architect, qa-engineer, code-reviewer | `changed_files`/`repo_root` 无落点、无 git 命令定义、游离于「永不 raise」保护外。实测: `--main-branch` 默认 `main` 而本仓是 `master` → `git diff main...HEAD` exit 128; dogfood 惯例 CWD=主仓而 PR 在子模块 ⇒ 扫错 workflow ⇒ green 而子模块 CI 在跑; **空 `changed_files` ⇒ ∃ 恒假 ⇒ `covered=False, confident=True` = 最高置信 skip**; `core.quotePath` 非 ASCII 转义 |
| **D** | critical | architecture | proposal §What 2 步骤 2 | qa-engineer, code-reviewer | 事件白名单是正向枚举 + 省略号 catch-all。`pull_request_target` / `merge_group` 真会 gate PR 却判「不贡献覆盖」⇒ 误 skip |
| **E** | critical | implementation | proposal §What 2 步骤 3/4 + P3 自审段 | tech-lead, backend-architect, qa-engineer, code-reviewer | P3 自审只审了 4 条**安全**兜底, 漏了经量词静默落 `covered=False` 的危险默认: `paths: []` (而 `paths-ignore: []` 方向相反 — 同一手滑安全性相反) / `workflows_seen==0` (与「目录不存在」认知等价却结论相反) / 静默误解析 / `{covered:false, confident:false}` 组合被接线直接读绿 |
| **F** | major | architecture | `pre_merge_gate.py:205-226` + 7 个构造点 | tech-lead, backend-architect, code-reviewer, knowledge-manager | `path_coverage` 穿不透封闭 6 键 dict。6 条早退路径缺该键 ⇒ KeyError 或 `.get()` 静默 None 分不清「没算」与「算了为空」 |
| **G** | major | implementation | proposal §What 3 × `pre_merge_gate.py:187-194` | tech-lead, backend-architect, code-reviewer | 「插在 in-flight 判定之前」措辞把实现者推向复制 (b) 判定; 既有 fall-through **本就**产出正确 4 行, 正确实现是**不加分支** |
| **H** | major | architecture | proposal §非目标 N1 × `build-aria-runner.yaml:22-26` | tech-lead, backend-architect, qa-engineer, code-reviewer | N1 方向性论证 **4 席独立验证无反例** ✅; 但残留未披露: 该 workflow 仅 push+branches+paths 无 pull_request ⇒ 其它分支改该路径恒 wait 复发, 而 M6 aria-orchestrator 轨活跃 |
| **I** | major | documentation | `SKILL.md:160-179`,`:240` + `config-loader/SKILL.md` + `config.template.json` + AB suite | tech-lead, backend-architect, code-reviewer, knowledge-manager | 漏列 5+ 处同步落点。**最重: AB 套件 6 fixture 结构上摸不到新分支 ⇒ AC-9 在瞎套件上通过** |
| **J** | major | implementation | proposal §What 2 步骤 6 + AC-8 | tech-lead, backend-architect, qa-engineer, code-reviewer | `?` 语义写反 (GH filter-pattern 的 `?` = 前一字符 0/1 次, 非 glob 单字符), 方向是误 skip; 零段边界 (`a/**` vs `a`, `**/x` vs `x`, `**/*.md` vs 根 `README.md`) 未定义; 裸目录名/尾随斜杠/前导 `/`/大小写/空 pattern 未定义 |
| **K** | major | implementation | proposal §What 2 步骤 2 × 语料 | backend-architect, code-reviewer | YAML parser 零规格。语料实证: pattern **全带单引号** (忘剥 ⇒ 全面假绿); `build-aria-runner.yaml` 的 `workflow_dispatch` 3 层嵌套 + 空行后才是 `push:` (朴素解析器读丢) |
| **L** | major | testing | proposal AC-7 / AC-2 / AC-6 / AC-9 / AC-5 / AC-1 / AC-4 | tech-lead, qa-engineer, code-reviewer | **AC-7 按现写法不可满足** (4 workflow 分属两仓, 单一 root 下三断言不能同时真) + 用 live checkout 致漂移; AC-2/6「逐字段相同」与「path_coverage 必须输出」互斥; AC-9「无回归」不可证伪; AC-5 捆 4 条件; AC-1 raw_message 未钉精确串; AC-4 guard 需对抗性测试 |
| **M** | minor | documentation | 多处 | 各席 | `.gitea/workflows/` 漏列; `confident` 无消费者; `custom_checks.py` 先例行号 (三席读数 62/63/64 不一); backend-state 与 gate-status 两套枚举无映射 SOT (含无生产者的 `"error"`); CLAUDE.md 拟写文本未预先给出供 owner 核验 |

## R1-fix 处置

全部 5 个 critical 簇 + 8 个 major 簇 + minor 簇**全量吸收**, proposal 重写。关键结构性改动:

1. **新增原则 P5**「一切枚举取安全侧极性」—— 白名单列**不贡献**的封闭集、未知一律贡献; 匹配歧义一律取**匹配更多**的读法。簇 A/D/J 同根。
2. **P3 自审方法论改写**: 从「枚举 `except` 分支」改为「**枚举全部产出 `covered=False` 的路径**」, 并证明其为**单出口** (AC-11 钉死)。这是对 R1 元教训的吸收 —— 上一版自审范围本身有遗漏。
3. `compute_verdict` catch-all 极性反转 (fail-OPEN → fail-CLOSED), 配 **baseline-failing AC-10** (在 v1.64.0 上实测为红)。
4. `changed_files` 计算**移进** `ci_path_coverage.py` 内部, 纳入「永不 raise」契约; 新增 `--repo-root` + **作用仓硬不变量**。
5. `not_applicable` 判定改为**四重合取** (`not covered ∧ confident ∧ workflows_seen≥1 ∧ changed_files_count≥1`)。
6. `path_coverage` 经 **keyword-only 参数**穿透全部 7 个构造点, 键恒存在 (null = 未判定)。
7. `?`/`+`/`[]` 移出支持集 → fail-CLOSED; 零段补偿明确取扩大匹配。
8. AC 重写: 9 条 → 18 条 (AC-5 拆 5a~5h, 新增 AC-10 catch-all / AC-11 单出口 / AC-7b drift guard)。
9. N1 残留**显式披露**并点名 `build-aria-runner.yaml`; **拒绝** R1 提出的「便宜版 branches 布尔检测」(方向与 P2 相反 — 基于部分信号收窄覆盖)。
10. AB 套件新增 2 个 `not_applicable` fixture + suite 版本 bump, 作为 AC-9 的**前置条件**。
11. CLAUDE.md 拟写文本**预先给出**供 owner 逐字核验 (防 #116 baseline 污染) + 预算核算。

## 未收敛原因

R1 无前序轮可比 (`conclusions_stable` 不适用)。进入 R2。
