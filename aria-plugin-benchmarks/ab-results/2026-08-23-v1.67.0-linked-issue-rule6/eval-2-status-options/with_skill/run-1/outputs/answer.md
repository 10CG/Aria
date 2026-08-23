## 项目状态扫描 (state-scanner v3.0, scan.py 机械采集)

scan.py 退出码 **10** (部分采集软错误, snapshot 可用): `snapshot_consistency` 报 AC-5 在 `origin/feature/linked-issue-normalization` 上对 164 条 legacy track 无法评估 (github remote 侧 git 命令失败), 因此 **多远程 `overall_parity=true` 本次按「未验证」处理** (已知问题 Aria #176, 单 remote 主仓 + 双 remote 子模块布局下恒为 exit 10)。

### 📍 当前状态
- 分支: `feature/linked-issue-normalization` @ `826b356`, upstream `origin/feature/linked-issue-normalization` ahead 0 / behind 0
- 无中断 workflow (`interrupt.status=none`), 无暂停中的 git 操作
- 工作树: 未暂存 1 项 (`aria` 子模块指针漂移: gitlink `9e6a17c`=v1.66.4, 工作树 `0fe2e0d` 在 aria 的同名 feature 分支, 2 个新 commit) + 未跟踪 1 项 (`aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/`, 本轮 AB 结果目录)
- UPM 未配置 (Aria 自身无运行时 UPM, 预期)
- 关联 OpenSpec: `linked-issue-normalization` (Draft, owner 2026-08-23 裁定修完 R5 九条后 override 进 Phase B.1, Rule #10 已留痕)

### 📊 变更分析
- 变更 2 项, 类型 other (子模块指针 + 基准结果目录), 复杂度 Level 1, 无架构影响, 无测试覆盖变化
- 主仓层未检出 SKILL.md 变更; 真正的 Skill 变更在 aria 子模块内 (`8f5f5bd` collision.py 归一 + `0fe2e0d` SKILL.md:176 括注) —— 这正是本轨 tasks 4.1 要求照跑 Rule #6 AB 的 hunk, AB 目录 `2026-08-23-v1.67.0-linked-issue-rule6/` 已建 (12 个 eval 在跑)

### 📄 需求状态
- 已配置。PRD: v1 Active / v2 Approved
- User Stories 21 篇: done 17 / in_progress 2 / approved 1 / pending 1
- 活跃 OpenSpec 9 个

### 🏗️ 架构状态
- `docs/architecture/system-architecture.md` 存在, Active, 最后更新 2026-05-27 (88 天, 检查项 `m6-arch-doc-stale` 仍 OK)
- 需求链路: `chain_valid=false` (未声明 parent PRD), 历史已知

### 📋 OpenSpec 状态
- 活跃 9: approved 7 / pending (Draft) 2
  - Draft: `linked-issue-normalization` (本分支, Phase B 进行中) / `a1-entry-claim-duplicate-work-guard` (C1/C2 owner 已裁, 待 rework 进 A.2)
  - Approved 但本轮未动: `pre-merge-gate-no-run-for-branch` (#152, post_planning R5 CONVERGED, Phase B TASK-004 起未做, 分支 `feature/152-no-run-for-branch`)
- 已归档 138, 待归档 0
- ⚠️ 设计未实施 6 个 (approved 但 tasks 大量未勾): m6-cost-model-telemetry (44d) / m6-dispatch-input-delivery (49d) / m6-e2e-resilience (41d) / m6-release-closeout (89d) / m7-agent-lifecycle (65d) / m7-fleet-aggregation (34d) —— 均卡 M6 owner/基建门, 非本轨范围

### 🛡️ 审计状态
- 审计系统 enabled。最近审计轨 `linked-issue-normalization-audit-trail.md`: post_planning R1→R5 全 FAIL (max_rounds 耗尽), owner override 进 Phase B (机械字段 verdict 为空, 以 proposal Status 行为准)

### 🔧 自定义检查
- 10/10 通过: issue-cache-freshness / silknode 豁免到期 / m6-version-badge-match (1.66.4) / m6-claude-md-version / m6-arch-doc-stale / i18n-readme-translation-currency (3 语种 @1.66.4) / claude-md-changelog-free (151 行) / coordination-gate-invocation (近 14d 4 次真调) / config-template-key-currency / plugin-cache-currency (installed 1.66.4 = SOT)

### 🔄 同步状态
- 当前分支与 origin 一致 (fresh, 远程引用 1 分钟前刷新)
- 子模块: standards / aria-orchestrator 与远程一致; **aria 工作树 `0fe2e0d` 领先 gitlink, 相对 origin master 落后 15** (feature 分支在 aria 上未合并, 预期; 合并后走 5.15 双推 + gitlink bump)
- 多远程 (origin + github): 主仓 origin equal; github 全部 `no_local_tracking_ref` / gitlink `no_published_ref` —— feature 分支只推了 origin, 未推 github (feature 分支不要求双推, master 才要求)
- 📝 aria README 版本 1.66.4 = plugin.json, 一致
- 🔗 Forgejo 配置缺失 (`.aria/forgejo.json` 未建; 检到 forgejo.10cg.pub 远程)

### 🎫 Open Issues (10CG/Aria, 抓取于 2026-08-23 06:24Z)
- open 44。与本轨关联: #133 / #134 / #136 / #137 / #177 → `linked-issue-normalization`; #156 → `pre-merge-gate-no-run-for-branch`
- 近期新开: #188 (四维一致性检查恒假阳性 + UPM collector 认不到根 UPM.md) / #184 (brainstorm 被共装插件绕过) / #182 (handoff frontmatter status 从不收口, 168 条 legacy track 由此而来) / #180 (claim heartbeat 零生产调用) / #176 (AC-5 exit 10 恒发, 即本次软错误)

### 🌲 多轨 / handoff 感知
- 最新 handoff (8.9h 前): `2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md`, **讲的是 #152 轨** (claim `s-a637@2033` active 未释放, 下一步 TASK-004)。**当前分支却是 linked-issue-normalization 轨** —— 同一 owner 容器两条 Phase B 并行, `tracks_multibranch.collision.kind=self_multi_container` (自己的多容器/多分支, 非跨 owner)。两轨都动 `aria/skills/state-scanner`, 合并顺序要定: 谁先 ship 谁占 v1.67.0, 另一个 rebase。
- 跨 worktree: 只有 1 个 worktree, 无他处更新。

---

## 🎯 可选操作

**[1] 继续本分支: linked-issue-normalization Phase B 收尾 → Phase C (推荐)**
- 理由: 代码与文档 (tasks 组 1-3) 已在 aria `8f5f5bd` / `0fe2e0d` 落地, 组 4 的 Rule #6 AB 正在本目录跑; 这是离 ship 最近的轨。
- 步骤: 等 AB 12 个 eval 出结果并记入 `ab-results/` → 把 tasks.md 1.x-3.x 对照实现逐条勾掉 (目前 21 条全未勾, 是「做了没勾」不是没做) → 5.1 全量回归 (`run_tests.py` 基线 1322) → 5.9/5.10 版本引用面 bump v1.67.0 (aria 子模块按引用点 + 主仓 14 点) → 5.11 双向断言 → 5.12 repro 脚本处置 → 5.13 交 phase-c-integrator 建 PR + pre-merge 闸 (不委派合并) → 5.15 本地合并 + 双推 + 逐远端 `ls-remote` 核验 + gitlink bump。
- 跳过: A.x (已 override 进 B), B.1 (分支已有)。
- 注意: 5.14 AB 门范围要 owner 确认; 与 #152 轨的版本号归属先说定。

**[2] 切到 #152 轨: pre-merge-gate-no-run-for-branch Phase B (TASK-004 起)**
- 理由: handoff latest 指向它, claim 仍 active, 前置三项 (claim / 两仓分支 / dispatch 探针 viable) 已清; 但 17 任务约 46h 未开工。
- 步骤: 先把本分支工作树收干净 (aria 子模块 `0fe2e0d` 已推 origin, 可安全切) → `git checkout feature/152-no-run-for-branch` 主仓 + aria → 按 detailed-tasks.yaml v5 双轨并行 (gate 轨 004→002→003→005→006→007a→007b; helper 轨 008→009 / 010a→010)。
- 代价: 两轨同时开会让 aria 子模块两条 feature 分支对 state-scanner 产生合并冲突面; 建议 [1] 先 ship 再做这个。

**[3] 先清环境噪音 (小修, Level 1 或挂既有 issue)**
- scan.py 恒 exit 10 (#176, AC-5 未排除本仓不存在的 remote) 与 168 条 legacy handoff status 不收口 (#182) 是每次扫描都出现的固定噪声; 两者已有 issue, 可作为本轨或 #152 之后的独立 PATCH 周期。
- 顺手项: `.aria/forgejo.json` 缺失 (跑 `/forgejo-sync` 引导建, 需确认)。
- 不推荐现在做: 会打断两条在途 Phase B。

**[4] 只看状态 / 会话收尾**
- 本次仅查看, 不启动工作流; 若要结束对话, 走 `session-closer` 写 `docs/handoff/` (本轨 linked-issue 的 Phase B 进展目前只在 proposal Status 行和 aria 提交里, 没有独立 handoff 记录, 收尾时要补)。

请选编号 (1-4) 或给自定义组合 (例如「5.1 + 5.9」)。按约定本轮到推荐为止, 不调用 workflow-runner / phase1_gate。
