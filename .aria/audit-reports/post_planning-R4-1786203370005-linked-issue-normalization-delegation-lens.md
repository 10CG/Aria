---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T15:36:10.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [delegation-lens]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R4 — 单镜头审计: 「委派 / 兜底 是否真的拦得住」

**席位**: delegation-lens (R4 新鲜眼睛, 未参与 R1/R2/R3)
**HEAD**: `72923de`
**范围**: `tasks.md` 「## 5.」整段 (:97–:169, 含紧随的三条已知限段 :170–:188 中的工具定位表述) + `detailed-tasks.yaml` `TASK-014` / `TASK-022..028` + `metadata` 的 `scope_boundary` / `version_reference_surface` / `known_env_trap` / `file_domain_serialization`
**镜头外**: 组 1–4 · 文字表述/措辞/一致性 · 算法本体
**方法**: 逐条列出「依赖外部单元/机制/检查来保证某件事」的表述 → 去外部单元源码/配置实读 → 答 (a) 真做吗 (b) 方式相容吗 (c) 失败/不触发时会发红吗

**已排除重复**: R3 已修的两条 (合并整体委派 + `:242` 误引 / gitlink bump 零归属) 不再作为形状复报。**但 F1 是那次 fix 的落地缺口** —— 同一文件里 `metadata.scope_boundary` 未跟改, 仍逐字承载被推翻的委派与被推翻的引用, 且它是本文件的「范围声明」入口。

---

## 委派表述清单 (22 处)

| # | 位置 | 委派对象 | 结论 |
|---|------|---------|------|
| 1 | tasks.md:108 | `run_tests.py` (state-scanner runner) 基线 1322 | ✅ 真做 |
| 2 | tasks.md:108 | `run_all_tests.sh` 9 OK / 累计 1698 / 0 FAIL | ✅ 真做 (条件见 F11) |
| 3 | tasks.md:110 + `known_env_trap` | 「验收一律以 tests/ 内全量 `run_tests.py` 为准」 | ✅ 真做 |
| 4 | tasks.md:114 | `spec_complete.py --gate` checkbox 分支 + `handoff_autofill` | ✅ 真做 (实跑双向验证) |
| 5 | tasks.md:114 | `DUAL_LAYER_SPEC.md:258` 示例 | ✅ 真做 |
| 6 | tasks.md:117 | `pre_merge_gate` (Rule #8) = 默认开的闸门 | ⚠️ **做但两条腿对本 Spec 都不触发, 且失败方向是绿** → F3 |
| 7 | tasks.md:117 + `delegated.why` | `submodule_gate=block` = 默认开的闸门 | ⚠️ **做但维度不匹配 + 被 DAG 顺序绕过** → F5 |
| 8 | tasks.md:127 / TASK-022 | `aria/VERSION` 账本口径 + CHANGELOG 追加 | ✅ 真做 (配套断言见 F4) |
| 9 | tasks.md:133 / TASK-023 | `#140 B 档` 不重译 + `i18n-readme-translation-currency` | ✅ 真做 |
| 10 | tasks.md:134 / TASK-023 | `claude-md-hygiene.md` 预算 + `claude-md-changelog-free` | ⚠️ 覆盖面不含段级预算 → F8 |
| 11 | tasks.md:142 / `enabled_check_blindness` | `m6-version-badge-match` / `i18n-readme-translation-currency` 失明面 | ✅ 真做 (两条 check body 逐字核实, 结论正确) |
| 12 | tasks.md:138 / `breakdown` | 主仓 14 点 + aria 4 点计数表 | ✅ 真做 (与磁盘逐文件精确吻合) |
| 13 | tasks.md:139 / `append_only_ledger` | 账本双向不变量 (a) 头部行 (b) 旧值命中数不减 | ❌ **(b) 恒红; 且 (b) 未落进 TASK-024** → F4 |
| 14 | tasks.md:141 / TASK-024 | 不带路径的 `git status` | ⚠️ 子模块只有单行粒度 → F7 |
| 15 | tasks.md:146 / TASK-025 | sc-baseline 脚本 `:275-277` / `:205-215` + proposal `:181/:183/:219` | ✅ 真做 (三个指针全部实存) |
| 16 | tasks.md:150 / TASK-026 | `phase-c-integrator` = 「只 PR + pre-merge 闸门, 不含合并」 | ❌ **该 Skill 无 gate-only 形态, 闸门触发条件本身就是「即将 merge」** → F2 |
| 17 | tasks.md:158 / TASK-027 | `AB_TEST_OPERATIONS.md:397` Tier 1 (10 个, 含 state-scanner) + `:545` 发版前清单 | ✅ 真做 |
| 18 | tasks.md:164-166 / TASK-028 | CLAUDE.md 多远程两条硬约束 (自承载) + 「aria/skills 零处编码」 | ✅ 真做 (零编码属实; 兜底见 F5/F6) |
| 19 | tasks.md:168 | memory `sync≠push-auth` + AD10 反驳 (`architecture-decisions.md:752-756`) | ✅ 真做 |
| 20 | `scope_boundary.delegated[0]` | `phase-c-integrator` 承载 **合并 + 双推 + ls-remote + gitlink bump** | ❌ **R3-fix 未落地到此处; 逐字仍是被四席推翻的版本** → F1 |
| 21 | `scope_boundary.delegated[1]` | `phase-d-closer` 承载 D.1/D.2/D.3 | ✅ 真做 |
| 22 | `file_domain_serialization` | 「本版加真依赖边串成链」 | ✅ 真做 (10 条 edge 逐条核) |

另: 组 5 尾部「三件工具是辅助不是闸门」的定位 —— 实核 `.aria/state-checks.yaml` / `.claude/settings*.json` / `aria/hooks/` 对三件脚本**零 wiring**, 定位属实 (它们不会误发红, 也不会替谁发红)。发布面 tag 一项见 F10。

---

## CRITICAL

```
- 表述位置: detailed-tasks.yaml:53-62 (metadata.scope_boundary.delegated[0]) + :545 (TASK-016.superseded_by)
  委派对象: phase-c-integrator (C.2.5)
  核实结论: 不做 + 做但方式违约 (R3-fix 的落地缺口, 非形状复报)
  证据:
    该字段逐字仍写「what: Phase C — **aria 子模块分支合并 + 双远程推送 + 逐远端 ls-remote 核验**
    (C.2.5) + **主仓 gitlink bump** (须指向合并后 master SHA)」, why 里逐字仍写
    「该 Skill (SKILL.md:242) 本就建模子模块合并, C.2.5 正是 TASK-016 手工重写的东西」
    + 「**本文件不复述其判据**」。而同文件 TASK-026:825 逐字写「⛔ **未**把 aria 子模块的合并动作 /
    双推 / ls-remote 核验 / gitlink bump 交出去 —— 那些由 TASK-028 承载」。
    实读外部单元:
      · phase-c-integrator/SKILL.md:570-580 — C.2.5 = "Multi-Remote Push Enforcement",
        触发条件「Phase C.2 合并成功 (master 已 fast-forward)」⇒ 它是**合并之后的推送**,
        全段无「合并」动作; §C.2.5 全文亦无 gitlink bump 步骤 (grep gitlink 于该 SKILL.md
        只命中 C.2.4.5 的 ls-tree 读取与 nil-SHA 说明)。
      · SKILL.md:242 实为 §C.2.4 步骤 2.5 path_coverage 的**执行上下文契约**, 与合并无关。
    ⇒ 同一文件两处权威声明互相矛盾, 且**陈旧那处是「本文件范围声明」入口**, 还附带
    「不复述其判据」= 明示读者不要在本文件找判据。
  隐藏错误: Phase B/C 实施者按 metadata 读范围 → 把合并与 gitlink bump 交给
    phase-c-integrator → 走 branch-manager 服务端 `Do: merge` (见下条证据) → 本地 master
    从未 fast-forward → 主仓 bump gitlink = orphaned gitlink (2026-07-14 事故形态)。
  User Impact: R3 四席花一轮抓出的 Critical 在 yaml 侧原样存活; 十份报告对 metadata 的引用
    与 task 层结论分叉。
  Recommendation: 把 delegated[0] 的 what 收窄为「PR 创建 + pre-merge gate (C.2.4) + 主仓自身
    PR 流程」; 删 `SKILL.md:242` 引用与「C.2.5 正是 TASK-016 手工重写的东西」一句; 新增
    delegated[1] 之前的 `retained:` 段点名「子模块合并 / 双推 / ls-remote / gitlink bump 由
    TASK-028 自承载」; `TASK-016.superseded_by` 改为 `TASK-026 + TASK-028`。
  Example:
    delegated:
      - who: "phase-c-integrator"
        what: "PR 创建 + pre-merge gate (Rule #8, C.2.4) + 主仓自身 PR 流程"
        not_delegated: "aria 子模块合并动作 / 双推 / 逐远端 ls-remote / 主仓 gitlink bump → TASK-028"
```

```
- 表述位置: tasks.md:149-151 + detailed-tasks.yaml TASK-026 (:814, :824-825)
  委派对象: phase-c-integrator §C.2.4 (pre-merge gate) — 「只委派闸门, 不委派合并动作」
  核实结论: 做但方式违约 —— 该 Skill 不存在 gate-only 形态, 闸门的触发条件就是「即将合并」
  证据:
    · phase-c-integrator/SKILL.md:163-166 — C.2.4「触发条件: … **即将调用 branch-manager
      merge action** (auto_merge=true 或 user-triggered continue)」⇒ 不打算 merge 时闸门不触发。
    · SKILL.md:253 — 「`green` → **调用 branch-manager merge action**, 进入 C.2.5」⇒ 闸门一旦
      放行就自动进入合并, 无中途返回点。
    · SKILL.md:236 表格 — 「branch-manager (C.2.4-C.2.5) | wait approval + **merge API call** |
      gate green 后」。
    · branch-manager/SKILL.md:621-634 — merge action 的**唯一**实现是
      `curl -X POST .../pulls/{n}/merge -d '{"Do": "squash"}'` / `'{"Do": "merge"}'`,
      无子模块例外分支。
    · SKILL.md:746-770「跳过规则」只有 C.1 无变更 / C.2 不需 PR / develop 直推三条, **没有**
      「跑闸门但不合并」这一档。
  隐藏错误: 二难 —— (i) 真按 5.13 调用它: 闸门 green 后立刻服务端合并 aria PR ⇒ 违 CLAUDE.md
    硬约束 1, 且 TASK-028 的本地 merge 变成空操作/事后补, 恰好复现它要防的事故;
    (ii) 为守住「不委派合并」而不进入 merge 路径: C.2.4 按其触发条件根本不会跑 ⇒ Rule #8
    闸门未过, 而 TASK-026 的验收项照样可以勾。
  User Impact: 计划里唯一的 Rule #8 归属点在两种执行路径下都落空, 且两种落空都不发红。
  Recommendation: 拆成两个可执行动作而不是一个不可分的委派:
    (1) 直接调用闸门脚本 `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
        --pr-branch <aria feature> --main-branch master` 取 verdict (纯读, 不触发 merge);
    (2) 主仓 PR 才交给 phase-c-integrator 全流程 (主仓可走 Forgejo merge, CLAUDE.md 例外条款)。
    并把 verdict!=green 的处置写进验收 (fail → 阻塞; wait → 按 workflow-runner 等待)。
  Example:
    - "aria 侧: python3 aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
       --pr-branch feature/linked-issue-normalization --main-branch master → verdict 落盘,
       green 才允许 TASK-028 本地合并 (⛔ 不调用 phase-c-integrator 编排层, 它会自动 merge)"
```

```
- 表述位置: tasks.md:150 / TASK-026 verification[2] (「pre-merge gate … 本 PR CI passing + main 无 in-flight run」)
  委派对象: pre_merge_gate 的两条判据腿
  核实结论: 做但两条腿对本 Spec 均结构性不触发, 且两边的失败方向都是**绿**
  证据:
    (a) PR CI 腿 — `.aria/config.json:phase_c_integrator.pre_merge_gate.path_coverage_enabled`
        缺省 true (SKILL.md:54)。实核两仓 workflow 的 paths 过滤:
          · aria/.forgejo/workflows/issue-triage-tests.yml:20-24 → 仅 `skills/issue-triage/**`
          · Aria/.forgejo/workflows/issue-triage-tests.yml → 仅 `aria/skills/issue-triage/**`
          · build-aria-runner.yaml → 仅 `aria-orchestrator/docker/aria-runner/**`
          · submodule-gate-tripwire.yml → 头注逐字「DEPRECATED for execution … FAILED 5/5」, dispatch-only
        本 Spec 变更面 = `aria/skills/state-scanner/**` + 根 README*/VERSION/CLAUDE.md +
        `.aria/repro/` ⇒ **零覆盖** ⇒ decision=not_applicable ⇒ SKILL.md:249 逐字
        「decision=not_applicable 时**本步跳过**」, verdict 计算 (SKILL.md:255) 逐字
        「not_applicable AND main_in_flight==[] → **green**」。
    (b) main in-flight 腿 — `scripts/pre_merge_gate.py:427`
        `parser.add_argument("--main-branch", default="main", …)`, 而本项目主分支是 **master**
        (`git remote -v` + CLAUDE.md 全文用 master)。SKILL.md:169 的示例命令逐字也是
        `aether ci status --branch main --in-flight --json`。**实跑**该命令:
          {"status":"ok","data":{"filters":{"branch":"main","in_flight":true},
           "repo":"10CG/Aria","runs":[]}}   RC=0
        ⇒ 查一个不存在的分支返回 ok + 空 runs ⇒ 「main 无 in-flight」恒真。
    ⇒ 两腿相加: verdict 恒 green, 唯一痕迹是 SKILL.md:253 要求 AI 手打的一行警告文字。
    (旁证: 同 config 的 `no_ci_fallback = "skip_with_warning"` 且键名自带
     `_open_question_no_ci_fallback` 未决注记 ⇒ 无 backend 时也是静默降级放行。)
  隐藏错误: PR CI 从未跑过 / 跑红了但没被查 / main 上真有 in-flight run (在 master 上) —
    三种都读成 green。
  User Impact: TASK-026 的 Rule #8 验收项**不可能红** = 验收假绿; 而 tasks.md:117 正是拿
    「手写会绕开这个闸门」作为整个委派切分的理由。
  Recommendation: 在 TASK-026 verification 里把两腿都钉成可证伪判据:
    (1) 显式传 `--main-branch master` (写进命令字面, 不依赖 CLI default);
    (2) 记录 `path_coverage.decision`; decision=not_applicable 时**必须**落盘那行警告 +
        在交接里写明「本 PR 无 CI 覆盖, Rule #8 的 (a) 轴本次为空」, 不得让「gate 通过」
        一句话吞掉它;
    (3) 若要 (a) 轴真有内容, 另开 issue 提「state-scanner 测试进 CI paths」(套件缺口, 不并入本 Spec)。
  Example:
    - "python3 …/pre_merge_gate.py --pr-branch <b> --main-branch master → 落盘 verdict +
       path_coverage.decision; decision=not_applicable ⇒ 交接必含警告行「(a) 轴为空: 变更路径零 CI 覆盖」"
```

```
- 表述位置: detailed-tasks.yaml:136-147 (metadata…append_only_ledger.invariant (b)) ↔ TASK-024 verification[2] (:777) / tasks.md:139
  委派对象: 「旧值命中数不减 (aria/VERSION ≥2, aria/CHANGELOG.md ≥1)」这条兜底断言
  核实结论: 做但恒红 (aria/VERSION 一侧); 且该子句根本没落进任务的验收 ⇒ 另一侧留着假绿
  证据:
    实测 `grep -c "1\.65\.5" aria/VERSION` = **2**, 两处逐字为:
      :3  `> **版本**: 1.65.5`                      ← 头部「当前版本」行, bump 必须改
      :4  `> **发布日期**: 2026-08-02  # patch: v1.65.5 收尾 …`   ← 发布注 (历史)
    TASK-022 verification[1] 逐字「头部「当前版本」行 == plugin.json; **历史行原样保留**」
    ⇒ 正确执行后 `1.65.5` 命中数 = **1**, 恒 < 阈值 2 ⇒ 该断言**判红且无法通过**。
    (对照 `aria/CHANGELOG.md` 命中数 = 1, 唯一命中 `:13 ## [1.65.5] - 2026-08-02` 是纯历史,
     追加新条目后仍 = 1 ≥ 1 ⇒ 阈值只在 aria/VERSION 那一侧坏。根因: aria/VERSION 的 2 处
     命中里有 1 处是**必须变的当前版本行** —— 文件级的两类划分没有下推到行级。)
    同时 TASK-024 verification 第 3 条与 tasks.md:139 都**只有** (a) 头部行 == plugin.json,
    (b) 子句只活在 metadata ⇒ 实施者照任务执行时, R3-fix/X3 要堵的作弊路径
    (覆写 `发布日期` 行 / 改写 `## [1.65.5]` 标题) 依旧全绿。
  隐藏错误: 分支一 —— 按 metadata 判 ⇒ 恒红 ⇒ TASK-024 是 TASK-026 的硬前置, 交付被永久卡住,
    实施者最省力的解法正是「把 1.65.5 再塞回 VERSION 凑数」或「豁免这条」, 两者都是它要防的病;
    分支二 —— 按 TASK-024 判 ⇒ 销毁发布注/改写 CHANGELOG 标题判绿。
  User Impact: 本 Spec 全程在打「恒红/假绿对偶」, 这条兜底在两条读法下各占一头。
  Recommendation: 把 (b) 改成**行级、与「必须变的那行」互斥**的判据, 并同步落进 TASK-024 与
    tasks.md 5.11 (三处同口径):
      · aria/VERSION: 旧值在**除头部当前版本行以外**的行中命中数 **≥ bump 前的同口径计数**
        (今天 = 1); 且 `发布日期(旧)` 行数不减;
      · aria/CHANGELOG.md: `^## \[1\.65\.5\]` 标题**仍存在**且新条目插在其**上方**。
  Example:
    - "aria/VERSION: 旧值 1.65.5 在 `2,$` 行内命中数 >= 1 (bump 前同口径实测 1) 且
       `grep -c '发布日期(旧)'` 不减; 头部 :3 == plugin.json"
    - "aria/CHANGELOG.md: `grep -n '^## \[1\.65\.5\]'` 仍命中, 且新 `## [1.66.0]` 行号小于它"
```

---

## MAJOR

```
- 表述位置: tasks.md:117 + detailed-tasks.yaml:59-62 (delegated.why) / TASK-016.cancel_reason (:547)
  委派对象: submodule_gate (`mode="block"` 默认) 作为「手写合并会绕开」的第二个闸门
  核实结论: 做但维度不匹配 —— 它审的既不是「谁执行子模块合并」也不是「是否推到全部 remote」
  证据:
    · phase-c-integrator/SKILL.md:376-390 + `scripts/submodule_gate.sh` — 它在**主仓 PR** 的
      C.2.4.5 位置运行, 核心判据 (script:266/273):
        `git -C "$SUB" merge-base --is-ancestor "$MASTER_PTR" "$FEATURE_PTR"`
      即「本 PR 的 gitlink 是否是 origin/master 现 gitlink 的后代」—— 检测的是**指针回退/分叉**
      (SKILL.md:189「regression 或 divergence」)。
    · 该 ancestry 在**本地 object DB** 里判 (`git -C "$SUB" merge-base`), 仅 best-effort
      `fetch origin` (script:245 后接 `|| true`) ⇒ 一个**只存在于本地、从未推到 github 的合并
      SHA 同样是合法后代 ⇒ PASS**。
    · 全段无任何「合并由谁执行」「是否服务端 merge」的判据 (与 F1 的 grep 一致: 两个 SKILL.md
      对「本地 git merge / ls-remote」零命中)。
  隐藏错误: 「手写子模块合并」实际上**不**绕开 submodule_gate (它照跑, 只要主仓 PR 走 Phase C);
    真正没人拦的是「服务端合并」与「半推 (只推 origin)」—— 而后者恰是 #165 三次复发的形状。
    这条错误的前提正是当初推动「删任务改委派」的两条理由之一。
  User Impact: 计划把一个正交闸门当成合并方式的守卫, 读者会高估自动化覆盖面;
    真实的唯一守卫是 TASK-028 的 prose 纪律。
  Recommendation: 把 :117 与 delegated.why 里的 submodule_gate 论证改写为它真实的维度
    (「主仓 PR 的 gitlink 前向性」), 并在 TASK-028 注明「本条的两条硬约束**无机械闸门**,
    仅有事后探针: state-scanner `gitlink_integrity` 的 `orphaned` 分支是 blocking
    (`collectors/multi_remote.py:706-717`), 但它在 Phase A.0 扫描时才发红 = **推之后**」。
  Example:
    > submodule_gate 审的是「主仓 PR 的 gitlink 是否前向」(本地 ancestry), 对「服务端 merge」
    > 与「只推 origin」结构性失明; 后两者本 Spec 内**无前置闸门**, 只有 state-scanner
    > gitlink_integrity=orphaned 的事后 blocking 探针。
```

```
- 表述位置: detailed-tasks.yaml TASK-028.dependencies = [TASK-026] (:871) + DAG :903-905 + tasks.md:167
  委派对象: TASK-026 委派出去的「主仓自身 PR 流程」与 TASK-028 自留的 gitlink bump 之间的顺序
  核实结论: 做但顺序把唯一相关的闸门排到了动作之前 (gitlink bump 落在主仓 PR 之外)
  证据:
    · TASK-026 (交主仓 PR 流程给 phase-c-integrator) 在 TASK-028 (合并 + **主仓 gitlink bump**)
      **之前**; TASK-026 deliverables = [] (:820) ⇒ 026 阶段主仓工作树里没有 gitlink 变更。
    · submodule_gate.sh:248-249 取 `FEATURE_PTR=git ls-tree HEAD "$SUB"` 与
      `MASTER_PTR=git ls-tree origin/master "$SUB"`; 两者相等时 script 逐字输出
      `OK: $SUB unchanged` ⇒ 026 的主仓 PR 上, 唯一审 gitlink 的闸门只会说「未变」。
    · 028 之后的 gitlink commit 在计划里**没有第二个 PR / 第二次闸门**归属 (组 5 无后继任务)。
    · 对照 memory `feedback_submodule_pointer_post_merge_bump` 与
      `feedback_coupled_pr_merge_discipline`: 正确顺序是「子模块 PR 合并 → 主仓显式 bump 到
      post-merge master SHA → 主仓 PR/闸门」, 本 DAG 恰好反过来。
  隐藏错误: gitlink bump 直接落 master 或落在一个无人审的补 PR 上; C.2.4.5 全程看不到它;
    C.2.5 的 ls-remote parity 也不覆盖它 (它在 026 的合并后就跑完了, 那时子模块还在 feature 分支)。
  User Impact: 「主仓宣称 v1.66.0 / gitlink 指向未合并或未推的 SHA」这一状态在本 DAG 下可以走完
    全部 21 条勾选。
  Recommendation: 反转依赖 —— TASK-028 (子模块本地合并 + 双推 + ls-remote + gitlink bump 落
    主仓工作树) 排在 TASK-026 **之前**, 让 gitlink 变更进入主仓 PR 从而被 C.2.4.5 审;
    TASK-026 依赖改为 [TASK-024, TASK-025, TASK-027, TASK-028]。若坚持现顺序, 必须新增
    TASK-029「gitlink bump 的独立 PR + 再过一次 C.2.4.5」并写进 DAG 与关键路径。
  Example:
    TASK-028: dependencies: [TASK-024, TASK-025]
    TASK-026: dependencies: [TASK-024, TASK-025, TASK-027, TASK-028]
    # DAG: … 024 ─┬─▶ 028 (子模块合并+双推+gitlink bump) ─▶ 026 (主仓 PR + C.2.4/C.2.4.5)
```

---

## MINOR

```
- 表述位置: tasks.md:141 / TASK-024 verification[3] (:778)
  委派对象: 不带路径的 `git status`
  核实结论: 做但粒度不足 (对 aria 侧只有单行)
  证据: 实跑 `git status --short` → ` M aria-orchestrator` —— 子模块整体一行, 不展开文件。
    aria 侧有 3 个普通引用文件 (4 点) + 2 个账本文件, 主仓根的 git status 无法区分「5 个文件改了 3 个」。
  User Impact: memory `scoped_git_add_splits_claim_from_landing` 要防的「声称 global 而动作 scoped」
    在跨仓场景下只被拦住一半。
  Recommendation: 验收改为两条: `git status --short` (主仓) **且** `git -C aria status --short`,
    并要求两侧落地文件清单与 breakdown 表逐文件对齐。
```

```
- 表述位置: TASK-023 verification[3] (:757) / tasks.md:134
  委派对象: `claude-md-hygiene.md` 的「项目状态段 15-20 行 + 覆写非追加」+ enabled check `claude-md-changelog-free`
  核实结论: 做但覆盖面是**全文级**, 不含段级
  证据: `.aria/state-checks.yaml:198-210` 的 command 只判三件事: footer 滚动 changelog 正则
    (`^> 前次|^\*\*更新\*\*:|^\*\*最近更新\*\*:`) · 全文 `wc -l > 200` · 全文 `wc -c > 24000`。
    「项目状态」段的行数与覆写/追加语义**无任何机械判据** (规范 §2.3:44 定预算, §2.4:48 定写入
     纪律, 两者都只是文档)。
  User Impact: 该验收项由写它的同一个 AI 自评, 与 F3 同形状 (声称有 check 兜, 实际 check 维度更粗)。
  Recommendation: 验收里点明「本项无机械判据, 靠人工/交接复核」, 或加一条 repro 断言
    (`awk` 取「## 项目状态」到下一 `^## ` 之间行数 ≤20 且 diff 无净增行)。
```

```
- 表述位置: tasks.md:180
  委派对象: 「唯一可当作证据的是 sc-baseline-*.py —— 但见 **5.8**」
  核实结论: 不做 (5.8 已 CANCELLED, 活的承载者是 5.12 / TASK-025)
  证据: tasks.md:122 逐字「~~5.8 sc-baseline 脚本处置~~ (CANCELLED) → 由 **5.12** 取代」。
  User Impact: Phase B 实施者按 :180 的指引跳到 5.8 会落到一条明示不执行的条目上, 处置判据
    (含 R3-fix 新加的「路径二须可执行验证」与「(a)/(b) 择一是 owner 裁量项」) 全在 5.12。
  Recommendation: :180 的指针改成 5.12。
```

```
- 表述位置: tasks.md:126-127 / TASK-022 (aria 子模块「版本面」= 5 文件) + metadata.ship_target
  委派对象: standards/conventions/version-management.md §4.3 的发布面规则
  核实结论: 做但本 Spec 落在它的**分发型**分支, 该分支要求的动作在组 5 里零归属, 且两侧都无机械检测
  证据: `version-management.md:159-172` 逐字「**分发型组件 (如 aria 插件 — 市场/下游按 tag 拉取)**:
    VERSION 文件必须与 Git Tag 保持一致 … 3. 打对应的 Git Tag」。组 5 (5.9/5.15, TASK-022/028)
    无 tag 创建/推送步骤; `.aria/state-checks.yaml` 无 VERSION↔tag 比对 check。
    实测 `git -C aria tag | wc -l` = **10**, 最新 `v1.21.3 (2026-05-17)` ⇒ 自 v1.22.0 起约 44 个
    版本从未打 tag, 该条款事实上已长期偏离。
  User Impact: 非本 Spec 引入的偏离, 但按 memory `feedback_written_exception_exact_condition_match`
    (「N 次非正式援引 ≠ 成文 lane」), 第 45 次不披露地偏离与 TASK-027 正在处理的 Rule #6
    门范围问题是同一形状。
  Recommendation: 在 5.9 加一句「aria 插件自 v1.22.0 起不打 per-version tag (实测 tag 停在
    v1.21.3), 与 version-management §4.3 分发型分支不一致 —— 本次沿用现状, 已记入交接请 owner
    裁定是否修订该条款」(不在本 Spec 内修)。
```

```
- 表述位置: tasks.md:108 / TASK-014 verification[1] (:506)
  委派对象: `run_all_tests.sh` 的「0 FAIL」与「9 OK / 累计 1698」
  核实结论: 真做, 但绿的强度是**环境依赖**的, 判据没写进验收
  证据: 实跑 → `9 OK / 0 FAIL / 0 SKIP (累计 1698)` RC=0, 与声称逐字吻合; 本机 `pytest 8.3.4` 在场。
    但脚本头注自陈 (run_all_tests.sh:19-26)「缺依赖 => SKIP … **exit 0 是环境依赖的绿** ——
    未装 pytest 的环境里 pytest 套件全走 SKIP」。换到无 pytest 环境, 同一条验收会在
    `7 OK / 2 SKIP` 下仍然判绿。
  User Impact: 「9 OK / 1698」这组数今天是硬证据, 但验收文本没把「0 SKIP」写成必要条件,
    换环境后同一句话变成弱得多的断言 (假绿方向)。
  Recommendation: verification 补 `0 SKIP` 与 `pytest 在场` 两个必要条件:
    "bash aria/skills/run_all_tests.sh → 汇总行 `9 OK / 0 FAIL / **0 SKIP**` 且累计 1698
     (⚠️ SKIP>0 = 环境缺 pytest, 该绿不成立)"。
```

---

## 已核实为真 (不需动作, 留证以免下一轮重复劳动)

| 表述 | 实读证据 |
|------|---------|
| 5.1 基线 1322 | 实跑 `run_tests.py` → `Ran 1322 tests` + `OK` |
| 5.1 跨 skill 9 OK / 1698 | 实跑 `run_all_tests.sh` → `9 OK / 0 FAIL / 0 SKIP (累计 1698)` |
| :114 归档门读 tasks.md checkbox, `_DONE_FAMILY` 不含 cancelled | `detailed_tasks.py:83`; 实跑 gate → `21/21 unchecked`; **全 [x] 模拟** → `complete=True, verdict=pass, d_payload=None, 21 task(s)` ⇒ 加粗删除线方案的 tasks 分支真的活着 |
| :114 `handoff_autofill` 会误报 phantom | `session-closer/scripts/handoff_autofill.py:160-180` 逐字 grep tasks.md `- [ ]` (yaml 仅 fallback) ⇒ 若留 `- [ ]` 确实永久误报 7 条 |
| :114 `DUAL_LAYER_SPEC.md:258` | 逐字 `- [ ] 1.2 Define responsibilities (CANCELLED)   # 保留编号，标记取消` |
| :142 两条 enabled check 的失明面 | `state-checks.yaml:95` badge-only 正则; `:161` 只读 `translated-from` ⇒ 7 处残留可全绿, 结论正确 (补充: 二者 `severity: warning`, 即便发现漂移也只 warn) |
| breakdown 14 + 4 点 | 逐文件实测: 主仓 VERSION 1 / README.md 2 / zh 3 / ja 3 / ko 3 / CLAUDE.md 2 = **14**; aria plugin.json 1 / marketplace.json 2 (:3/:16) / README.md 1 = **4** — 与表逐格吻合 |
| TASK-025 三处 proposal 指针 | `proposal.md:181` / `:183` / `:219` 三处实存且都是 sc-baseline 引用; 脚本 `:205-215` FATAL fail-CLOSED 实读确认, `:275-277` `measured_face != EVIDENCE_FACE → exit 1` 实读确认; `_PROPOSAL` 相对路径 = `.aria/repro/../../openspec/...` ⇒ 「改名 spec 目录重跑仍不 FATAL」是 Phase B 可执行的 |
| TASK-027 的 AB 事实 | `AB_TEST_OPERATIONS.md:397` 逐字「Tier 1: 核心 Skills (10 个, 每次发版必测)」, 表内第 3 行 `state-scanner`; `:545` 逐字「Tier 1 Skills 全量 AB 测试已执行」。补充: 唯一机械面是 `branch-finisher/references/ab-benchmark-gate.md` (触发 `skills/*/SKILL.md` 变更 + 查 ab-results 时间戳新于 SKILL.md), 单 hunk 定向 AB 即可满足它 ⇒ Tier 1 全量确实只是文档要求, 「披露」路线与机械面不冲突 |
| TASK-026 notes 的三条引用 | `branch-manager/SKILL.md:621-634` 服务端 `Do: merge`/`Do: squash` 属实; `phase-c-integrator/SKILL.md:242` 确为 path_coverage 执行上下文契约; `grep -rn "本地 git merge\|ls-remote"` 于两个 SKILL.md **零命中** ⇒「aria/skills 全仓零处编码」属实 |
| TASK-028 对 AD10 的反驳 | `aria-orchestrator/docs/architecture-decisions.md:752-756` 逐字为 S7_AWAITING_MERGE / Feishu / 产品负责人签字 ⇒ 治无人值守流水线, 反驳成立 |
| phase-d-closer 委派 | `phase-d-closer/SKILL.md:40-43` D.1 progress-updater / D.2 openspec-archive (+#95 tri-state) / D.2b release_gate / D.3 handoff 硬编码 `docs/handoff/` ⇒ 与 delegated[1] 逐项吻合 |
| `known_env_trap` | 实跑 `python3 -m pytest test_collision.py` → `ImportError: cannot import name 'collision' from 'lib'` + collection error; `4d87060` 日期 `2026-05-30` ⇒「已破 70 天」精确; 且 `run_all_tests.sh` 走 `run_tests.py` 全量路径 ⇒ 该 trap 对 TASK-014 两条命令都不发红, 声称一致 |
| `file_domain_serialization` | 实读 10 条 edge: 001→002→003→004→005 串行 ✓; 006 deps [007] ✓; 007 deps [001..005] ✓; 008→009→010 串行 ✓ ⇒「本版加真依赖边」属实 |
| 三件工具「不当作闸门」 | `.aria/state-checks.yaml` / `.claude/settings*.json` / `aria/hooks/` 对 `spec-consistency-check` / `mutation-sweep` / `sc-baseline` **零 wiring** ⇒ 定位属实 |

---

## 结论

**4 CRITICAL / 2 MAJOR / 5 MINOR**

四条 critical 的共同形状不是「委派给了错的对象」, 而是**委派的粒度与被委派单元的真实接缝不对齐**:
F2 要求一个不可分割流程的前半段; F3 委派的闸门两条腿在本 Spec 的变更面上都不通电;
F1 是上一轮 fix 只落在 task 层没落在 metadata 层; F4 是自建兜底的阈值把「必须变的行」和
「必须留的行」算进了同一个计数。三条 (F2/F3/F4) 都在**本轮 fix 新造或新写**的条文里 ——
与 memory `feedback_fix_recurs_in_its_own_fallback_path` 同向。

**vote: REVISE**
