# Tasks — `premerge-gate-mainbranch-failclosed`

> **Spec**: [proposal.md](./proposal.md) | **审计轨**: [audit-trail](../../../.aria/audit-reports/premerge-gate-mainbranch-failclosed-audit-trail.md)
> **Level**: 3 | **Status**: 📝 **A.2 初稿 (2026-08-09)** — 由 owner「进 Phase B, 用 TDD 接管」裁定产出
> **ship target**: **MAJOR** (见 proposal §版本; 破坏性签名变更)
>
> ⚠️ **本文件的性质与既往不同**: post_spec 跑满 R1–R5 (25 个 agent-run) **未收敛**, owner 裁定停止「审计→改文档」循环。五轮量化证据显示 —— 席位稳定找到真问题, 而**编排层每轮 fix 引入 73–100% 的新 Major**。⇒ 本文件**不再试图在文档层把实现钉死**, 而是把「编排层验证不了的部分」组织成 **TDD 前置 + spike**, 让缺陷在实施时自己发红。
>
> **判据**: proposal 的 SC 表钉住「什么算对」; 本文件钉住「按什么顺序让它发红」。**任何 spike 的结论回写 proposal, 不在本文件里另立规定。**

---

## 组 0 — TDD 前置 (必须先做, 且必须先看到红)

> 这五条对应 R5 后仍阻塞的项。**每条都要求先写出会红的测试, 看到红, 再实现。** 五轮实证: 这些缺陷在代码里分钟级暴露, 在文档里要五个 agent 一轮。

- [ ] **TASK-001** 建**全部机械断言的空壳**, 先跑一次确认**该红的都红**: SC-M1 (`aether ci status`=0) · SC-M2 (`"branch": "main"`=0) · **SC-M3a** (`--main-branch "<MAIN_BRANCH>"`=2) · SC-M4 (三处字面量=0/0/0) · SC-M5 (help 文案=0); 另两条负控 **SC-M3b** (无 `--main-branch main|master`) · **SC-M3c** (折叠块内不含调用) 今日已绿, 属负控。
      **验收**: 贴出实施前实跑输出证明该红的确实红。⚠️ 五轮里编排层两次写出**恒红**、一次**恒绿**的断言, 故**先验红窗**再往下走。
      ⚠️ **另须做对抗性验证**: 建「写死 `--main-branch main`」与「调用藏进折叠块」两个 fixture, **断言集必须拒绝它们** —— post_planning R1 实证上一版全套验收对 `--main-branch` 失明 (写死 main 能全过)。

- [ ] **TASK-002** **spike: helper 路径解析形态**。输入见 proposal §1 (3 个副本位置 / `CLAUDE_PLUGIN_ROOT` 66 处 / `SKILL.md:242` cwd 契约)。
      **验收 = SC-M12**: 四种 cwd (主仓根 / `aria` 子模块根 / `standards` 子模块根 / 模拟 plugin 安装态) **全部可达**; 且不可达时 abort, 但健康常态下不得 abort。
      **产出**: 形态定稿 + 回写 proposal §1。⚠️ 上一版规定的两分支解析在后两种 cwd 下**恒红**, 不得沿用。

- [ ] **TASK-003** **spike: 存在性核验的精确比对实现**。判据已定 (proposal §5): 「返回的 ref 名列表中存在 `== "refs/heads/" + main_branch` 的精确匹配」。spike 决定取列表的方式与解析形态。
      **验收 = SC-M6 + SC-M13**。SC-M13 是 R2 承重 Critical 的**真正闭合腿** —— 锚定 pattern 实现必须在此转红。

- [ ] **TASK-004** **spike: 异常/重试的复用形态**。⛔ **不得再造** —— `path_coverage.py:93` 有 `(TimeoutExpired, FileNotFoundError, OSError)` 三合一; `ci_backends/aether.py:38` 有 `RETRY_BACKOFF=(5,15,45)` / `_run_with_retry`。
      **验收 = SC-M7 + SC-M8**, 且须说明复用/抽取方式。**理由**: 本 Spec 治的就是「同一算法两份实现」, 在其修复里造第二份是自相矛盾 (R5 两席命中)。

- [ ] **TASK-005** **测试隔离接缝**。既有 `test_sc22_no_real_git_subprocess_in_suite` (`:710`) 的 patch **本就全局生效** (`import subprocess` 使模块对象共享 —— 受控实验证实, 编排层早先的相反陈述已作废)。
      ⇒ 新增 gate 层 subprocess 后该守卫会**转红**。本条须建独立打桩接缝, 使守卫**保持有效而非被放宽**; 同时保证 SC-M6/SC-M13 能用真实 git 受控裸仓。**粒度 (函数级 vs subprocess 级) 由 spike 定。**

---

## 组 1 — 实现 (组 0 全绿后)

- [ ] **TASK-006** `pre_merge_gate.py` 三处字面量 (`:21` docstring / `:300` 签名 / `:427` CLI) + **help 文案**; 参数改必填。
- [ ] **TASK-007** 新增 `--remote` / `remote` 参数 (默认 `origin`)。
      **须写下失效方向不对称的理由** (R5): 错 `remote` 走 128 ⇒ fail-CLOSED; 错 `branch` 走 `runs:[]` ⇒ fail-OPEN。这就是为什么 `remote` 可以有缺省而 `main_branch` 不可以。
- [ ] **TASK-008** `_verify_branch_exists()` 按 TASK-003 定稿实现; 插入点 = 三个早退**之后**、`evaluate_path_coverage` **之前**。
- [ ] **TASK-009** 诊断信息写入 **`raw_message` (主通道, `SKILL.md:255` 逐字规定)** + `gate_error` additive 副本。
- [ ] **TASK-010** 既有 **24 处** `gate_check(` 调用补 `main_branch="master"`; `test_sc12_default_true_lock` (`:663`) 断言由 `"main"` 改 `"master"`。

## 组 2 — SKILL.md (承重, D1)

- [ ] **TASK-011** `### 步骤执行` (:99 段) 与 `### C.2.4` (:218 段) **两处**散文流程改为 helper 调用; 5 步移入折叠块并**去掉全部可执行命令字面量**。
      ⚠️ `:99` 段的 C.2.4 条目在 `:101` 开 `:216` 闭的 **yaml 围栏内**且**没有「5 步」结构** (R5/tech-lead) —— 该处的改法须 spike, 不得照搬 `:218` 段的形态。
- [ ] **TASK-012** **步骤 6 (`:252-255`) 不动** —— 纯 AI 义务 + `DEC-20260731-001` owner 交换条件。仅在其 `fail` 分支确认 `raw_message` 会被 surface (若既有措辞已覆盖则**不加句**, 避免 no-op 编辑)。
- [ ] **TASK-013** `:270` 示例 · `:267` schema 增 `gate_error` · `:279` **四类**早退注记同步 (逐字是四类, 含 backend query 失败)。
- [ ] **TASK-014** 核对 `SKILL.md:262` / `:559` / `:610` 的 helper 定位约定 —— **不得与 TASK-002 的定稿并存互斥两套** (R5/code-reviewer)。

## 组 3 — 合规与同步面

- [ ] **TASK-015** **Rule #6 照跑 AB** (判据表第二行, 零裁量): `ab-suite/phase-c-integrator.json` + `phase-c-integrator-pre-merge-gate.json`, 结果存 `ab-results/`。**不得以「套件覆盖薄」降档。**
- [ ] **TASK-016** `CLAUDE.md` 规则 #8 同步 —— 本 change 新增第三条阻断腿。先例: `commit 7661e96` (v1.31.0 在同一提交同步过)。
- [ ] **TASK-017** 发版同步面: **整仓引用点差集**枚举 (非文件白名单), 类级根因见 **Aria #177**。
- [ ] **TASK-018** blast-radius 核验 (含 `pre-merge gate` 这个不含下划线的写法, 否则搜不到 `CLAUDE.md`); 外部采用方 (Kairos 等) 通告项。

## 组 4 — follow-up issue (本 Spec 不修)

- [ ] **TASK-019** 开 issue: (1) `main_branch` 自动解析设计面 (R2 实测 `ls-remote --symref` 有 RC=0 无 `ref:` 行两态); (2) `fetch_gate.py` 字面 `("master","main")` 回落 + `worktree_manager.py:170` 同形; (3) `workflow-runner` `gate_state` 无 `gate_error` 位置; (4)「显式传错分支名」此前零测试覆盖; (5) **C.2.4.5 的 `SKILL.md:189-191` 裸 git 命令 + `submodule_gate.sh`** —— 与 D1 根因**同类**的最近兄弟 (R5/code-reviewer)。

---

## 未决 (须 owner 裁, 本文件不自行决定)

> ✅ **已闭 (2026-08-09)**: `detailed-tasks.yaml` 已建 (owner 裁定「写」); `post_planning` 已跑 R1 (owner 裁定「跑」)。
> 原「detailed-tasks.yaml 是否补」的真正待决项是 **`standards/openspec/project.md` 自身 `:21` (双层) 与 `:118` (单层) 两处表述矛盾** —— 应转记给 standards 维护者, 不属本 Spec (TASK-019 已纳入)。

1. **版本 MAJOR 的确认** —— 或写下「不构成对外破坏性变更」的论证。⚠️ 若确认 MAJOR, 则 v2.0.0 激活 `pre_merge_gate.py:68/:116` 的弃用到期承诺 (TASK-020)。
2. **`ARIA_PLUGIN_ROOT` vs `CLAUDE_PLUGIN_ROOT` 的约定归属** —— `phase-c-integrator/SKILL.md` 内部用 `ARIA_` (3 处), 全仓主流是 `CLAUDE_` (66 处)。TASK-002 spike 需要一个方向。
3. **`SKILL.md:559` / `:610` 的归属** —— 分属 `submodule_gate.sh` 与 `git-remote-helper` 两个无关 helper, TASK-014 是否应覆盖它们。
4. **`ci_backends/aether.py` 是否入 scope** —— TASK-004 若要抽取共享重试逻辑, 该文件不在 `scope_repos.paths` 内。
