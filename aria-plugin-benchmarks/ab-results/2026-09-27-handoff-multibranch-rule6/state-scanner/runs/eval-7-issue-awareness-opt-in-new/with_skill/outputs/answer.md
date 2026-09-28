已按 state-scanner 流程跑完 `scan.py`（退出码 0，全部采集成功，`errors[]` 为空，`snapshot_schema_version = "1.0"` 与契约一致）。你的 `issue_scan.enabled=true`、`platform=forgejo`、`scan_submodules=true`，所以这次 Issue 区块覆盖了主仓 + 3 个子模块仓。

先说结论：**目前没有任何 open issue 带 `blocker` / `critical` 标签，`open_blocker_issues` 规则（priority 1.99）没有触发，不会压低新 feature 的推荐**。但有两点需要你知道：一是有 2 个仓的数量正好顶到了抓取上限 20 条，列表可能不全；二是只有 4 条打了 `bug` 标签，其余 45 条都没打标签，所以「按标签判阻塞」这个机制在你的仓里其实判不出多少东西（详见第 9 节）。

---

## 📍 当前状态

- 分支: `feature/handoff-multibranch-subdir-path-fidelity`（HEAD `4f91772`，没有设置上游跟踪分支）
- 模块 / Phase·Cycle: UPM 未配置（本仓无运行时 UPM），无 Phase/Cycle 数据
- 变更文件: 3 个 —— `aria`、`standards` 两个子模块指针改动（子模块工作区 HEAD 与主仓记录的 gitlink 不一致）+ 1 个未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- 关联 OpenSpec: `handoff-multibranch-subdir-path-fidelity`（approved，分支同名）
- 中断检测: `interrupt.status = none`，无未完成工作流；git 操作 `none`，无 rebase/merge 暂停态
- 上次 handoff: `2026-09-24-session-close-199-post-planning-converged.md`（60.3h 前，来源 pointer，status `done`，owner-container `simonfish/bfe8285d`）
  - 它记的是 `10CG/Aria#199`（`pre-merge-completeness-gate-change-scope`）那条轨：post_planning 已收敛，但**收敛不等于能开工**，要等 owner 门；并提醒「开工先查 claim 心跳年龄」。
  - 它把你当前分支这条轨（`10CG/Aria#195`）列为「仍 yielded、B.1 待起，谁接手谁先认领」；从分支上今天（09-27）的新提交看，这条轨已有人在推进。

## 📊 变更分析

- 变更类型: other × 3（code 0 / test 0 / docs 0 / config 0）
- 复杂度: Level 2
- 架构影响: 无
- 测试覆盖: 无
- Skill 变更: 未检出（无 SKILL.md 改动，不触发 Rule #6 AB 状态块）

## 📄 需求状态

- 配置: 已配置
- PRD: `prd-aria-v1.md`（active）；`prd-aria-v2.md` 原文写的是 `Approved (Draft → Approved 2026-04-11, …)`，但被归一成 **pending** —— 这正是 open issue `10CG/aria-plugin#198` 描述的误判（括号里的 Draft 把状态带偏了），实际应视为 approved
- User Stories: 21 份 —— done 17 / in_progress 2（US-007、US-026）/ approved 1（US-028）/ pending 1（US-003）

## 🏗️ 架构状态

- System Architecture: 存在，`docs/architecture/system-architecture.md`，status Active，最后更新 2026-09-02
- 需求链路: 完整（关联 prd-aria-v1 与 prd-aria-v2）

## 📋 OpenSpec 状态

- 活跃变更: 8 个，全部 approved
- 已归档: 146 个；待归档: 0 个
- ⚠️ 设计未实施（design_deferred）: 5 个
  - `aria-2.0-m6-release-closeout` —— approved，41/41 任务未勾，搁置 124 天
  - `aria-2.0-m7-agent-lifecycle` —— approved，18/18 未勾，100 天
  - `aria-2.0-m6-cost-model-telemetry` —— approved，25/38 未勾，79 天
  - `aria-2.0-m6-e2e-resilience` —— approved，25/40 未勾，77 天
  - `aria-2.0-m7-fleet-aggregation` —— approved，20/20 未勾，70 天

## 🛡️ 审计状态

- 审计系统: 已启用
- 上次审计: `post_planning` R7（`pre-merge-completeness-gate-change-scope`），verdict **PASS**，`converged: true`（2026-09-24）

## 🔧 自定义检查

- 16 项全部 ✅ OK（0 失败 / 0 跳过），含 `issue-cache-freshness`、`forgejo-app-token-liveness`、`m6-version-badge-match`、`plugin-version-arch-docs-match` 等

## 🔄 同步状态

- 当前分支: 未设置上游（ahead/behind 无法计算）；但多远程比对显示本分支在 `origin` 和 `github` 两端都是 `4f91772`，parity equal，证据新鲜
- 多远程总体 parity: ✅ true；子模块 gitlink 可达性 6/6 ok
- 子模块: `aria` 工作区在 `b181678`、主仓记录 `1cb3872`；`standards` 工作区在 `d86fc91`、主仓记录 `940cb5b` —— 即 `git status` 里的 ` M aria` / ` M standards`（子模块检出的是本 feature 分支，gitlink 尚未提交）
- 📝 README 版本: aria-plugin 1.73.3，与 plugin.json 一致
- 📦 standards 子模块: 已初始化、已注册
- 🔗 Forgejo 配置检查: 检测到 Forgejo 远程（`forgejo.10cg.pub`），但项目级 Forgejo 配置 **missing** —— 可运行 `/forgejo-sync` 引导创建（需你确认）

## 🎫 Open Issues

```
🎫 Open Issues
───────────────────────────────────────────────────────────────
  平台: Forgejo — 4 个仓, 共 49 open (下限, 见下方截断提示)
  阻塞性 (blocker / critical 标签): 0 个  → open_blocker_issues 未触发
  标签分布: bug × 4, 其余 45 条无标签
  数据来源: cache (刚刚获取, 2026-09-27T17:09:50Z) | ttl: 15m | 4 个仓均无 fetch_error
```

⚠️ **截断提示**：你的 `issue_scan.limit = 20`（按仓计）。`10CG/Aria` 和 `10CG/aria-plugin` 各抓到正好 20 条 —— 顶到上限，说明这两个仓**可能还有更早的 open issue 没抓到**，49 只是下限。想看全量，把 `.aria/config.json` 里的 `state_scanner.issue_scan.limit` 调大后重扫。

**10CG/Aria — 20 open（可能截断）**

- 📌 #221 secret-guard 缺口: 进程列举可旁路凭据保护 (拦得住读取路径, 拦不住进程表)  [bug]
- 📌 #218 state-scanner: handoff 无指针时按工作树 mtime 判最新 — rebase/checkout/新建 worktree 后指错文件  [bug]
- 📌 #217 session-closer: handoff_autofill.py / consistency_check.py 的 stdout 跟随 OS locale — Windows GBK 下遇 ⏸ 即崩  [bug]
- 📌 #199 pre_merge Checkpoint Completeness Gate 缺 change_id 维度 —— PASS 可由其他 change 的报告满足  [bug]
- #220 session-closer / phase-d-closer: latest.md History prepend 声明不可跳过却无机械核验
- #219 [Feature] 提供「开发项目进度状态查看」的只读机读接口（aria-ops-mcp 在等它）
- #216 [Archive Tracker] rule6-description-change-trigger-eval-lane — 上游反馈未发出
- #214 [跟进 spec][自主运行时] description 变动的完整处理
- #213 [benchmark] 41 个 skill 没有 trigger 套件 — 下一次 description 变动会被挡住
- #212 [规范缺口] openspec CLI 的统一口径
- #211 [AB评测台] description 变动照跑 AB 但触发面被按构造绕过
- #210 [Archive Tracker] archive-gate-registration-class-and-skill-drift
- #208 [缺陷][归档闸门] C 分级死码检查对非 Python 符号结构性失明
- #207 [AB结果文档] DEFECTS.md 与 SCORES.md 的回归断言分母不一致
- #206 [缺陷] standards 版本号两处不一致 (v2.2.3 vs 2.2.2)
- #205 [AB评测台] 单个臂可吃光全局 subagent 配额
- #204 [AB评测台] 评测跑在活仓上, 结果不可复现
- #203 [AB评测台] 语料泄漏三通道
- #201 [Archive Tracker] a1-entry-claim-duplicate-work-guard
- #200 [bug] issue-triage: version collector 在 monorepo 下 5 条路径全 miss（标题写了 [bug] 但没打标签）

**10CG/aria-plugin — 20 open（可能截断）**

- #204 [遗留缺口][state-scanner] handoff 读侧仍按扁平布局：子目录下的指针读不回
  → 已关联 OpenSpec（启发式）: `handoff-multibranch-subdir-path-fidelity`（= 你当前分支）
- #195 [缺陷][Layer L] refs/aria/coordination 的权威 remote 无校验 — 读到死 ref 即恒判无碰撞 (fail-OPEN)
  → 已关联 OpenSpec（启发式）: `pre-merge-completeness-gate-change-scope`
- #203 [安全][secret-guard] 真实泄露事件：服务端配置文件不在名单 + 路径经 shell 变量间接即绕过
- #202 [缺陷][Layer L] phase1_gate 的 self-resume 按 (container, session) 匹配 — 换 session 会新建第二条 claim
- #201 [缺陷][openspec-archive] 「归档不吞未完成」对 Level 2 spec 结构性失效
- #200 [enhancement] spec-drafter / task-planner 模板加 rule6_note 五字段
- #199 [缺陷][state-scanner] check_bare_issue_refs.py 把序数形态的 #<n> 判为裸 issue 引用
- #198 [缺陷][state-scanner] `_normalize_status` 把 `Approved (Draft → Approved …)` 判成 pending
- #194 [缺陷][state-scanner/test] collision_dedupe 测试只冻结了 renderer 时钟
- #193 [缺陷][spec-drafter] SKILL.md 三处指示运行未安装的 openspec validate --strict
- #192 [缺陷][state-scanner] unverified_claims / unverified_ack frontmatter 只写不读
- #191 [AB套件][openspec-archive] 三个 eval 缺 YYYY-MM-DD- 前缀
- #190 [AB套件][openspec-archive] 固定套件零覆盖 Step 7 / auto-issue
- #189 [缺陷][openspec-archive] Step 7 的 SHA 回链填充没有调用宿主
- #188 [类级][设计已完成] 归档闸门认不出 `python -m pkg.mod` 调用
- #187 [缺陷][test-harness] run_all_tests.sh 收集到 0 个测试却报 OK
- #186 [类级] 归档闸门调用面: `python -m pkg.mod` 与非 CI runtime yaml 不被识别
- #185 [清理] aria/skills/session-closeout/ 空的未跟踪残留目录
- #184 [清理][state-scanner] state_scanner.sync_check.* 是死配置
- #183 [缺陷][文档冲突][state-scanner] README 同步状态区块定义冲突

**10CG/aria-standards — 7 open**

- #21 [缺陷] openspec/AGENTS.md:57 指示运行一个不存在的脚本
- #20 [convention] session-handoff.md 两次实质增量未 bump Version
- #19 [convention] owner-container 与 claim container 段口径不统一
- #18 [缺陷+enhancement] git-commit 禁止 AI 署名, 但没说与 harness 注入指令谁优先
- #17 [convention] skill-benchmark-exemption: 单 Skill 局部变更的 AB lane 缺成文
- #16 [缺陷] openspec/project.md 对 Level 3 交付物给出两种口径
- #15 [enhancement] concurrent-session-write-safety 的 fetch 原则应扩展

**10CG/aria-orchestrator — 2 open**

- #31 [coordination] 自主 bot dispatch 时强制 claim
- #5 feat: abstract reusable "Hermes on Aether" deployment template

**关于「哪些是阻塞性的」**

- **按机制（标签）判**：0 条阻塞。state-scanner 只认 `blocker` / `critical` 两个标签，你的 49 条里一条都没有。
- **这个结论的局限**：45/49 条没有任何标签，很多标题写着 `[缺陷]` / `[安全]` / `[bug]` 却没打标签（如 aria-plugin#203 安全泄露、Aria#200）。所以「0 个阻塞」的真实含义是「没人用标签标过阻塞」，不是「确认没有阻塞」。
- **按标题粗看（我的阅读判断，不是机械信号，供你 triage 参考）**，值得先看一眼的是：
  - 安全类: `aria-plugin#203`（真实泄露事件）、`Aria#221`（secret-guard 缺口）
  - 与你当前分支直接相关: `aria-plugin#204`（启发式关联到 `handoff-multibranch-subdir-path-fidelity`）
  - 会让扫描结果本身失真的: `aria-plugin#198`（本次扫描里 prd-aria-v2 就被它误判成 pending）、`aria-plugin#195`（协调板 fail-OPEN，碰撞检测可能漏报）
- **想让以后的扫描能自动判阻塞**：给真正阻塞的 issue 打上 `blocker` 或 `critical` 标签，下次扫描 `open_blocker_issues` 规则就会生效并在推荐区降级提示。

## 🎯 推荐工作流

没有 blocker 标签 issue，推荐不被降级。但开新 feature 前有两件事先要处理：当前分支是 `10CG/Aria#195` 那条轨，工作区里还有未提交的子模块指针改动和一个 AB 结果目录；另外多终端碰撞检测报 `self_multi_container`（同一 owner 的两个容器 `simonfish/023236f2` / `simonfish/bfe8285d` 都有 track，并且与 `aria-runner-bot` 共用身份键），开新轨要走认领。

**[1] 先 triage 再开 feature（推荐）**
- 步骤: 用 `/issue-triage` 核对上面「值得先看一眼」的 4-5 条（尤其安全类两条），确认哪些真阻塞你的新 feature、顺手补 `blocker`/`critical` 标签 → 然后按 [2] 开 feature
- 理由: 你明确说「不知道哪些是阻塞性的」，而标签机制在本仓基本失效（45/49 无标签），只能人工核一轮
- 跳过项: 暂不进 Phase A

**[2] 直接开新 feature（feature_new：A.1 → A.2 → A.3 → B.1 …）**
- 步骤: 先把当前分支的改动处理掉（提交 `aria`/`standards` gitlink 与 AB 结果目录，或确认它们属于 #195 轨留在原处）→ 从 master 开新分支 → A.1 `/spec-drafter` 写 proposal → A.2/A.3 → B.1
- Phase B 入口会走 Layer L 认领闸（`coordination.enabled` 缺省 true 且 `collision.kind = self_multi_container`）。**本次评测不实际执行**，会执行的命令是：
  ```bash
  python3 "/home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py" \
    --raw-track-id "<新 feature 的 carry-id>" --phase B --mode advisory --repo-path "/home/dev/Aria"
  ```
- 理由: 无 blocker 标签阻挡；A.0 状态扫描已完成
- 跳过项: A.0（本次扫描即是）

**[3] 继续当前分支这条轨（`handoff-multibranch-subdir-path-fidelity` / `10CG/Aria#195`）**
- 步骤: 先确认这条轨的认领归属（handoff 说它由双子星 `simonfish/023236f2` 手上，另一容器不碰）→ 处理未提交改动 → 按该 spec 的 tasks.md 继续
- 理由: 当前分支今天有新提交、工作区有未提交改动，属进行中的轨；且 `aria-plugin#204` 就关联它

**[4] 自定义**
- 例如只做「补 Forgejo 项目配置（`/forgejo-sync`）+ 调大 `issue_scan.limit` 后重扫」，或输入步骤组合如 `A.1 + A.2`

请回复 1 / 2 / 3 / 4 或自定义步骤。（本次无法交互，以上选项已完整列出，未代你选择；也未执行任何写操作。）
