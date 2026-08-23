## 直接回答：有，`.aria/config.json` 存在且已被 scan.py 实际读取

- 文件: `/home/dev/Aria/.aria/config.json` (5.6 KB, 最后改动 2026-08-22 21:49)，`version: "1.0"`；旁边还有模板 `.aria/config.template.json`。
- 顶层段: `workflow` / `state_scanner` / `tdd` / `benchmarks` / `experiments` / `audit` / `orchestrator` / `phase_c_integrator`。
- 与 state-scanner 相关的生效配置:
  - `state_scanner.confidence_threshold=90`, `auto_execute_enabled=false`, `auto_execute_rules=[commit_only, quick_fix, doc_only]`
  - `state_scanner.issue_scan.enabled=true` (forgejo.10cg.pub, `scan_submodules=true`, 缓存 900s) —— 所以本次 snapshot 里 `issue_status` 真的拉到了 44 个 open issue
  - `state_scanner.coordination.enabled=true, mode=advisory` (Layer L 认领闸门)
  - `state_scanner.sync_check.enabled=true` (注: 该键 sync.py 从不读取, sync_check 恒开)
  - `workflow.auto_proceed=false`
  - `audit`: post_spec / post_planning 已启用, 其余 checkpoint 关闭 (Rule #10: 已启用闸门 AI 不得自行豁免)
- 证据链: snapshot 中 `requirements.configured=true` / `custom_checks.configured=true` / `openspec.configured=true` / `issue_status.fetched_at=2026-08-23T06:24:51Z`，均依赖该配置。注意 `forgejo_config.config_status=missing` 指的是 **forgejo-sync 专用配置** (`.aria/forgejo.json` 一类) 缺失，不是 `config.json` 缺失。

---

## 项目状态扫描 (scan.py exit 10 = 部分软错误，snapshot 可用)

### 1. 当前状态
- 分支: `feature/linked-issue-normalization` (upstream origin 同名, ahead 0 / behind 0)
- 工作区: 2 个未提交项 —— 子模块 `aria` 指针有改动 (unstaged) + 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/`
- UPM: 未配置 (`upm.configured=false`, 无 Phase / Cycle 信息；关联 open issue #188 提到 UPM collector 认不到仓库根 UPM.md)
- 无中断工作流 (`interrupt.status=none`)，无暂停中的 git 操作
- 最近提交: `826b356` docs(spec): linked-issue-normalization R5-fix 九条 + owner override 进 Phase B

### 2. 变更分析
- 变更类型: other x2 (子模块指针 + 未跟踪基准目录)；复杂度 Level 1；无架构影响；无测试覆盖；未检出 SKILL.md 变更 (`skill_changes.detected=false`)

### 3. 需求状态
- 配置状态: 已配置
- PRD: prd-aria-v1 (active) / prd-aria-v2 (Approved, 归一为 pending)
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1

### 4. 架构状态
- `docs/architecture/system-architecture.md` 存在, status Active, 最后更新 2026-05-27 (88 天)
- 需求链路不完整 (`chain_valid=false`, `parent_prd=null`)

### 5. OpenSpec 状态
- 活跃变更 9 个: approved 7 / pending 2 (`linked-issue-normalization`, `a1-entry-claim-duplicate-work-guard`)
- 已归档 138；待归档 0
- 设计未实施 6 个 (approved 但 tasks.md 大量未勾): m6-cost-model-telemetry (44d) / m6-dispatch-input-delivery (49d) / m6-e2e-resilience (41d) / m6-release-closeout (89d) / m7-agent-lifecycle (65d) / m7-fleet-aggregation (34d)

### 6. 审计状态
- 审计系统 enabled；上次审计记录 `.aria/audit-reports/linked-issue-normalization-audit-trail.md` (verdict / 收敛轮数未能机械解析，需读原文)

### 7. 自定义检查
- 10 项全部 OK (含 m6-version-badge-match badge=1.66.4 / i18n-readme-translation-currency 3 语种 @1.66.4 / m6-arch-doc-stale 88d / issue-cache-freshness 等)，0 失败

### 8. 同步状态
- 当前分支与 origin 一致；多远程 enforced = github + origin
- github 对该 feature 分支无本地跟踪引用 (parity unknown, 正常——分支只推到了 origin)；子模块 gitlink 对 origin 全部 ok，对 github 为 no_published_ref
- 软错误 1 条 (`snapshot_consistency_inconclusive`): AC-5 对 164 条 legacy handoff track 的 github 侧校验执行失败，`overall_parity=true` 这一裁决本次视为未验证
- 子模块 README 版本: aria 插件 1.66.4 与 README 一致；standards 子模块已初始化并注册
- Forgejo 专用配置: missing (建议 `/forgejo-sync` 引导创建)

### 9. Open Issues (issue_scan 已开启)
- open 共 44: 10CG/Aria 20 (最新 #188 四维一致性恒假阳性 + UPM collector, #184 brainstorm 被共装插件绕过) / 10CG/aria-plugin 20 / 10CG/aria-standards 2 / 10CG/aria-orchestrator 2

### 交接感知
- 最新 handoff: `docs/handoff/2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md` (约 9 小时前, pointer 来源 latest.md)；无其他 worktree 持有更新交接
- 多终端碰撞: `self_multi_container` (同 owner 的 dev-claude / simonfishgit/dev-claude、aria-runner-bot/023236f2 / simonfish/bfe8285d)，进 Phase B 时需走 advisory 认领闸门

### 10. 推荐工作流
你的问题是查状态 + 确认配置存在，本身不需要启动工作流。若要继续，可选:
- [1] (推荐) 仅查看状态，到此为止 —— 配置已确认存在，工作区只有子模块指针 + AB 基准目录，无待提交代码
- [2] 继续 `linked-issue-normalization` 轨 Phase B —— 该 spec 已经 owner override 进 Phase B (R5 不收敛后留痕)，进入前须过 phase1_gate advisory 认领
- [3] 处理 `aria` 子模块指针变动 —— 先确认是否为本轨有意更新 (`git -C aria status` / `git diff aria`)
- [4] 自定义组合

本次不调用 workflow-runner / phase1_gate。
