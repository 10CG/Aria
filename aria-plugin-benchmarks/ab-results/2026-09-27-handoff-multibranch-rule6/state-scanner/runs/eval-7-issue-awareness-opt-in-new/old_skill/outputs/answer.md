已跑 `scan.py`（退出码 0，全部采集成功，`errors[]` 为空）。你的 `issue_scan` 配置已生效：`enabled=true`、`platform=forgejo`、`scan_submodules=true`、`limit=20`，所以主仓和 3 个子模块仓的 open issues 都扫到了。先说结论，再给完整状态。

**结论（阻塞性 issue）**：按 state-scanner 的判定规则 `open_blocker_issues`（优先级 1.99，只看 label 里有没有 `blocker` / `critical`），**当前 0 个阻塞性 issue**，这条规则没有触发。全部 open issue 里只有 4 个打了 `bug` 标签，没有任何一个打 `blocker` / `critical`。

需要注意两点：
- **"0 个阻塞" 只说明没人给 issue 打阻塞标签，不说明真的没有阻塞项。** 你们仓库几乎不打 label（49 条里只有 4 条有标签），这条规则基本看不到东西。下面我按标题另外标了几条"可能影响开发"的，这是我读标题做的判断，不是机械判定。
- **清单被截断了，实际 open 数量比 49 多。** `limit=20` 是每个仓的上限，`10CG/Aria` 和 `10CG/aria-plugin` 都正好返回 20 条，说明到上限就截断了。旁证：你当前分支对应的 `10CG/Aria#195`、CLAUDE.md 里提到的 `10CG/Aria#168` 都还是 open，但不在清单里（Aria 只返回到 #199）。想看全，把 `.aria/config.json` 里 `state_scanner.issue_scan.limit` 调大（比如 100）再扫一次。

---

## 📍 当前状态

- 分支：`feature/handoff-multibranch-subdir-path-fidelity`（没有设置 upstream；github 和 origin 两个远程的 HEAD 都等于本地 `4f91772`）
- 中断状态：无（`interrupt.status = none`），也没有进行中的 git 操作（rebase/merge 等都是 none）
- UPM：未配置（本仓没有运行时 UPM，这是已知情况）
- 未提交变更：3 项，其中 `aria`、`standards` 两个子模块指针有改动（unstaged），另有 1 个未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- 关联 OpenSpec：`handoff-multibranch-subdir-path-fidelity`（approved，对应 `10CG/Aria#195`）

## 📊 变更分析

- 变更类型：code 0 / test 0 / docs 0 / config 0 / other 3（都是子模块指针和 AB 结果目录）
- 复杂度：Level 2
- 架构影响：无；测试覆盖：无
- Skill 变更：未检出（没有 SKILL.md 改动，不需要 AB 状态块）

## 📄 需求状态

- 已配置
- PRD：`prd-aria-v1.md` = Active；`prd-aria-v2.md` 原始状态是 "Approved (Draft → Approved 2026-04-11 …)"，但归一化结果是 `pending`。这是括号里的历史状态被误读，正好是已登记的 `10CG/aria-plugin#198`，实际应当算 approved
- User Stories：21 份，其中 done 17 / in_progress 2 / approved 1 / pending 1

## 🏗️ 架构状态

- `docs/architecture/system-architecture.md` 存在，status = Active，最后更新 2026-09-02
- 需求链路完整（`chain_valid = true`，上游 PRD v1 + v2）

## 📋 OpenSpec 状态

- 活跃变更 8 个，全部是 approved：
  - `aria-2.0-m6-cost-model-telemetry`
  - `aria-2.0-m6-dispatch-input-delivery`
  - `aria-2.0-m6-e2e-resilience`
  - `aria-2.0-m6-release-closeout`
  - `aria-2.0-m7-agent-lifecycle`
  - `aria-2.0-m7-fleet-aggregation`
  - `handoff-multibranch-subdir-path-fidelity`
  - `pre-merge-completeness-gate-change-scope`
- 已归档 146 个；待归档 0 个
- 设计未实施：⚠️ 5 个
  - `aria-2.0-m6-release-closeout`：approved，124 天，0/41 任务
  - `aria-2.0-m7-agent-lifecycle`：approved，100 天，0/18
  - `aria-2.0-m6-cost-model-telemetry`：approved，79 天，13/38
  - `aria-2.0-m6-e2e-resilience`：approved，77 天，15/40
  - `aria-2.0-m7-fleet-aggregation`：approved，70 天，0/20

## 🛡️ 审计状态

- 审计系统已启用
- 最近一次审计：`post_planning`（`pre-merge-completeness-gate-change-scope`），2026-09-24，verdict = **PASS**，已收敛（R7）

## 🔧 自定义检查

- 16 项全部 ✅ OK，0 项失败（其中 `issue-cache-freshness` 也是 OK）

## 🔄 同步状态

- 当前分支：没有 upstream（`no_upstream`），所以没有 ahead/behind 数据
- 多远程：`overall_parity = true`。主仓和 `standards`、`aria` 等子模块在 github / origin 两端都 `equal`，证据等级都是 fresh
- 子模块 gitlink 完整性：6 项（3 个子模块 × 2 个远程）全部 `ok`
- 📝 README：aria 插件版本 1.73.3，与 README 一致
- 📦 standards 子模块：已注册、已初始化
- 🔗 Forgejo 配置检查：检测到 Forgejo 远程（`forgejo.10cg.pub`），但 **forgejo 配置缺失**，可运行 `/forgejo-sync` 引导创建（需要你确认）
- 交接文档（handoff awareness）：最新交接是 `docs/handoff/2026-09-24-session-close-199-post-planning-converged.md`（由 latest.md 指针定位，距今约 60 小时），`misplaced_files` 为空，没有漂移。交接里和"开发新 feature"直接相关的几条：
  - 开工前先查 claim 心跳年龄，接近或超过 24 小时要先刷新
  - `pre-merge-completeness-gate-change-scope`（`10CG/Aria#199`）虽然 post_planning 已收敛，但入口门要求 `10CG/Aria#195` 先完成 C.2 合并，或 owner 明确改顺序；还有三件事等 owner 裁定
  - `10CG/Aria#195` 属于双子星容器 `simonfish/023236f2`；你当前就在这条分支上，而最近几个提交表明 #195 在这份交接之后又推进了（组 3/组 4 完成、owner 2026-09-27 裁定）。所以这份 09-24 的交接对 #195 的描述已经落后
- 多终端：`tracks_multibranch.collision.kind = self_multi_container`（同一身份 simonfish 在 `023236f2` 和 `bfe8285d` 两台容器上都有轨道）。另有 2 条 ⚪ 同机多身份说明：两个 identity_key 都同时出现了 `aria-runner-bot` 和 `simonfish`。coordination 已启用（advisory 模式），进入 Phase B 时会走认领闸门（见下方推荐）

## 🎫 Open Issues

```
平台: Forgejo — 4 个仓共 49 open（已截断，实际更多，见开头说明）
label 汇总: bug × 4；blocker / critical × 0
数据来源: 本次扫描期间获取 (fetched_at 2026-09-27T17:09:50Z, 字段标 cache) | ttl: 15m
```

**10CG/Aria**（返回 20 条，到上限，已截断）

| # | 标题 | 标签 | 关联 |
|---|---|---|---|
| 221 | secret-guard 缺口: 进程列举可旁路凭据保护 | bug | - |
| 220 | session-closer / phase-d-closer: latest.md History prepend 声明不可跳过却无机械核验 | - | - |
| 219 | [Feature] 提供开发项目进度状态查看的只读机读接口（aria-ops-mcp 在等它） | - | - |
| 218 | state-scanner: handoff 无指针时按 mtime 判最新，rebase/checkout 后指错文件 | bug | - |
| 217 | session-closer: 脚本 stdout 跟随 OS locale，Windows GBK 下崩溃 | bug | - |
| 216 | [Archive Tracker] rule6-description-change-trigger-eval-lane 归档残留 | - | - |
| 214 | [跟进 spec][自主运行时] description 变动的完整处理 | - | - |
| 213 | [benchmark] 41 个 skill 没有 trigger 套件 | - | - |
| 212 | [规范缺口] openspec CLI 的统一口径 | - | - |
| 211 | [AB评测台] description 变动照跑 AB 但触发面按构造被绕过 | - | - |
| 210 | [Archive Tracker] archive-gate-registration-class-and-skill-drift | - | - |
| 208 | [缺陷][归档闸门] C 分级死码检查对非 Python 符号失明 | - | - |
| 207 | [AB结果文档] DEFECTS.md 与 SCORES.md 回归断言分母不一致 | - | - |
| 206 | [缺陷] standards 版本号两处不一致 (v2.2.3 vs 2.2.2) | - | - |
| 205 | [AB评测台] 单个臂可吃光全局 subagent 配额 | - | - |
| 204 | [AB评测台] 评测跑在活仓上，结果不可复现 | - | - |
| 203 | [AB评测台] 语料泄漏三通道 | - | - |
| 201 | [Archive Tracker] a1-entry-claim-duplicate-work-guard | - | - |
| 200 | [bug] issue-triage: version collector 在 monorepo 下全 miss | - | - |
| 199 | pre_merge Checkpoint Completeness Gate 缺 change_id 维度 | bug | - |

**10CG/aria-plugin**（返回 20 条，到上限，已截断）

| # | 标题 | 标签 | 关联 |
|---|---|---|---|
| 204 | [遗留缺口][state-scanner] handoff 读侧仍按扁平布局 | - | OpenSpec: `handoff-multibranch-subdir-path-fidelity`（启发式） |
| 203 | [安全][secret-guard] 真实泄露事件：服务端配置文件不在名单 + 路径经 shell 变量间接即绕过 | - | - |
| 202 | [缺陷][Layer L] phase1_gate self-resume 按 (container, session) 匹配，换 session 会新建第二条 claim | - | - |
| 201 | [缺陷][openspec-archive] 归档不吞未完成对 Level 2 spec 失效 | - | - |
| 200 | [enhancement] spec-drafter / task-planner 模板加 rule6_note 五字段 | - | - |
| 199 | [缺陷][state-scanner] check_bare_issue_refs.py 误判序数 #n | - | - |
| 198 | [缺陷][state-scanner] `_normalize_status` 把 `Approved (Draft → Approved …)` 判成 pending | - | - |
| 195 | [缺陷][Layer L] refs/aria/coordination 权威 remote 无校验，fail-OPEN | - | OpenSpec: `pre-merge-completeness-gate-change-scope`（启发式，可能是误关联） |
| 194 | [缺陷][test] collision_dedupe 测试没冻结 collector 时钟 | - | - |
| 193 | [缺陷][spec-drafter] 指示运行未安装的 openspec validate --strict | - | - |
| 192 | [缺陷][state-scanner] unverified_claims frontmatter 只写不读 | - | - |
| 191 | [AB套件][openspec-archive] eval 缺日期前缀 | - | - |
| 190 | [AB套件][openspec-archive] 固定套件零覆盖 Step 7 | - | - |
| 189 | [缺陷][openspec-archive] Step 7 SHA 回链填充没调用宿主 | - | - |
| 188 | [类级][设计已完成] 归档闸门认不出 `python -m pkg.mod` | - | - |
| 187 | [缺陷][test-harness] run_all_tests.sh 收集到 0 个测试却报 OK | - | - |
| 186 | [类级] 归档闸门调用面识别不全 | - | - |
| 185 | [清理] aria/skills/session-closeout/ 空残留目录 | - | - |
| 184 | [清理][state-scanner] sync_check.* 是死配置 | - | - |
| 183 | [缺陷][文档冲突][state-scanner] README 同步状态区块定义冲突 | - | - |

**10CG/aria-standards**（7 条，完整）

| # | 标题 |
|---|---|
| 21 | [缺陷] openspec/AGENTS.md:57 指示运行不存在的脚本 |
| 20 | [convention] session-handoff.md 两次实质增量未 bump Version |
| 19 | [convention] owner-container 与 claim container 口径不统一 |
| 18 | [缺陷+enhancement] git-commit 禁止 AI 署名但没说与 harness 注入指令谁优先 |
| 17 | [convention] 单 Skill 局部变更的 Rule #6 AB lane 缺成文 |
| 16 | [缺陷] project.md 对 Level 3 交付物两种口径 |
| 15 | [enhancement] fetch 原则扩到以 ref 为输入的写操作 |

**10CG/aria-orchestrator**（2 条，完整）

| # | 标题 |
|---|---|
| 31 | [coordination] 自主 bot dispatch 时强制 claim |
| 5 | feat: abstract reusable "Hermes on Aether" deployment template |

所有 issue 都没有关联 User Story（`linked_us` 全为空）。上面的 OpenSpec 关联是启发式匹配（按标题/正文里的名字），仅供参考。

**我对"可能阻塞"的判断**（读标题得出，不是机械判定，建议你核对后给真正阻塞的打上 `blocker` 或 `critical` 标签，下次扫描就能自动识别）：

- **安全类，建议优先看**：`10CG/Aria#221`（进程列举可旁路凭据保护）、`10CG/aria-plugin#203`（标题写的是"真实泄露事件"）。如果是真实泄露，通常要先轮换凭据，这比开新 feature 优先。
- **会影响你开新 feature 的流程本身**：
  - `10CG/aria-plugin#202`：同容器换 session 再认领会新建第二条 active claim
  - `10CG/aria-plugin#195`：协调 ref 权威 remote 无校验，fail-OPEN，可能漏报冲突

  开新 feature 进 Phase B 时要走认领闸门，这两个缺陷会影响碰撞判断的可信度。
- **影响合并闸门**：`10CG/Aria#199`（pre_merge 完整性闸门缺 change_id 维度）。它本身就是一条进行中的轨道（`pre-merge-completeness-gate-change-scope`），修好之前合并闸门的 PASS 可能被其他 change 的报告冒充。
- **测试可信度**：`10CG/aria-plugin#187`（测试脚本收集到 0 个测试却报 OK）。如果新 feature 要改到 phase-d-closer 附近，测试全绿不可信。
- 其余大多是文档/规范缺口、AB 评测台改进、归档残留跟踪和清理项，一般不阻塞开发新 feature。

## 🎯 推荐工作流

规则匹配结果：
- `git_operation_in_progress`：未触发
- `commit_only`：未触发（有 unstaged 变更）
- `multi_remote_drift`：未触发（parity = true）
- `custom_check_failed` / `custom_check_warning`：未触发（0 失败）
- `audit_unconverged`：未触发（已收敛）
- `handoff_drift`：未触发
- `open_blocker_issues`：**未触发**（0 个 blocker/critical）
- `concurrent_churn_detected`：不适用（coordination 已启用，改为在 Phase B 入口走 phase1_gate）

你要开发的是**新 feature**，它还没有 OpenSpec，因此按规范（Rule #1 需求变更必须有 OpenSpec、Rule #2 不能跳过 Phase A）走完整流程。

**[1] 新功能完整流程 feature-new（推荐）**
- 步骤：
  1. 先处理工作区：当前分支上的 3 项未提交变更（子模块指针 + AB 结果目录）属于 `#195` 这条轨道，先决定是提交到 #195 还是保留，再离开这个分支
  2. A.1 用 `spec-drafter` 为新 feature 起草 `openspec/changes/<新 feature>/proposal.md`
  3. A.2 / A.3 用 `task-planner` 拆任务、分配 Agent
  4. B.1 从 master 建新分支（进入 Phase B 前会调用认领闸门，见下）
  5. B.2 开发和验证
  6. C.1 / C.2 提交和合并
- 跳过项：无
- 理由：新需求没有 Spec；0 个标记为阻塞的 issue，流程上没有硬性拦截
- 置信度：约 65%（兜底规则），不自动执行

**[2] 先处理安全类 issue，再开新 feature**
- 步骤：
  1. 用 `/issue-triage` 核对 `10CG/Aria#221` 和 `10CG/aria-plugin#203`
  2. 如果确认是真实泄露，先轮换凭据
  3. 再回到 [1]
- 理由：标题提示有"真实泄露事件"，但没有阻塞标签，机械规则抓不到

**[3] 继续当前分支上已批准的 Spec（feature_with_spec → feature-dev）**
- 对象：`handoff-multibranch-subdir-path-fidelity`（`10CG/Aria#195`）
- 跳过项：A.1 / A.2 / A.3（Spec 已 approved）
- 理由：当前就在这条分支上，并且有未提交的变更
- 置信度：88%
- 注意：交接文档写明这条轨道属于双子星容器 `simonfish/023236f2`，除非 owner 明确指示，否则本容器不应接手。请先确认这个 session 是否就是那条轨道的持有者

**[4] 只看状态，不启动工作流**
- 可以顺手做的：把 `issue_scan.limit` 调大后重扫，看到完整的 issue 清单；再给真正阻塞的 issue 打 `blocker` / `critical` 标签

也可以自定义组合（例如 "A.1 + A.2"）。

**进入 Phase B 时的认领闸门**：coordination 已启用（advisory），并且检测到 `self_multi_container` 碰撞，所以在 B.1 之前会调用下面这条命令。本次是只读评测，**没有执行**：

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "<新 feature 的 carry-id>" --phase B --mode advisory --repo-path "/home/dev/Aria"
```

另外，交接文档要求开工前先查 claim 心跳年龄，接近或超过 24 小时要先刷新。

请选择 [1]-[4]，或给出自定义组合。
