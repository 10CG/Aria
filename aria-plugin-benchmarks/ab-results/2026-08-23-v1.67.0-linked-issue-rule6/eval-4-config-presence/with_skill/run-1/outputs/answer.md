## 回答：有，`.aria/config.json` 存在且已被读取

`/home/dev/Aria/.aria/config.json` 存在 (5603 字节, 最后修改 2026-08-22 21:49)。scan.py 已按它执行, 关键配置项:

| 配置项 | 值 |
|--------|-----|
| 顶层键 | `_comment` / `version` / `workflow` / `state_scanner` / `tdd` / `benchmarks` / `experiments` / `audit` / `orchestrator` / `phase_c_integrator` |
| `state_scanner.confidence_threshold` | 90 |
| `state_scanner.auto_execute_enabled` | false |
| `state_scanner.issue_scan.enabled` | true (platform=forgejo, host `forgejo.10cg.pub`, scan_submodules=true, limit 20) |
| `state_scanner.coordination` | enabled=true, mode=advisory (DEC-20260704-002 dogfood) |
| `state_scanner.sync_check` | enabled=true, check_submodules=true |
| 自定义检查 `config-template-key-currency` | OK (8 keys, 0 deprecated, 0 unknown vs DEFAULT_CONFIG) —— 配置键与模板一致 |

注意区分: snapshot 的 `forgejo_config.config_status = "missing"` 指的是 **forgejo-sync 专用配置** (Story↔Issue 同步), 不是 `.aria/config.json`; 后者存在无误。

---

## 项目状态扫描 (scan.py exit 10: 1 条软错误, snapshot 可用)

snapshot: `aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/eval-4-config-presence/with_skill/outputs/state-snapshot.json`

### 1. 当前状态
- 分支: `feature/linked-issue-normalization` (upstream origin, ahead 0 / behind 0), 无 git 中间态操作, 无工作流中断 (`interrupt.status=none`)
- UPM: 未配置 (`upm.configured=false`, 无 Phase/Cycle 信息; 关联 open issue #188 提到 UPM collector 认不到仓库根 UPM.md)
- 变更: 2 个 (未暂存 `aria` 子模块指针 + 未跟踪 `aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/`)
- 最近提交: `826b356 docs(spec): linked-issue-normalization R5-fix 九条 (2C+7M) + owner override 进 Phase B (Rule #10 留痕)`
- 关联 OpenSpec: `linked-issue-normalization` (status pending; issue #177 已链到它)

### 2. 变更分析
- 类型: other x2 (子模块指针 + 基准结果目录); 复杂度 Level 1; 无架构影响; 未检出 SKILL.md 变更 (子模块内部变动不在主仓 diff 范围)

### 3. 需求状态
- 已配置。PRD: prd-aria-v1 (active), prd-aria-v2 (Approved → 归一为 pending)
- User Stories 21 条: done 17 / in_progress 2 / approved 1 / pending 1

### 4. 架构状态
- `docs/architecture/system-architecture.md` 存在, status Active, 最后更新 2026-05-27 (88 天, 检查仍在阈值内); 需求链路 `chain_valid=false` (未声明 parent PRD)

### 5. OpenSpec 状态
- 活跃 9 个: pending 2 (`a1-entry-claim-duplicate-work-guard`, `linked-issue-normalization`) / approved 7
- 已归档 138, 待归档 0
- 设计未实施 6 个 (approved 但 tasks 未勾): m6-cost-model-telemetry (44d) / m6-dispatch-input-delivery (49d) / m6-e2e-resilience (41d) / m6-release-closeout (89d) / m7-agent-lifecycle (65d) / m7-fleet-aggregation (34d) —— 均受 M6 owner/基建门顺序制约, 与 CLAUDE.md 项目状态一致

### 6. 审计状态
- enabled=true; 最近审计轨迹 `.aria/audit-reports/linked-issue-normalization-audit-trail.md` (verdict/checkpoint 字段未解析出, 据提交记录: post_planning R5 不收敛, owner override 进 Phase B 并留痕)

### 7. 自定义检查
- 10/10 通过: issue-cache-freshness / silknode-contract-deferral-expiry / m6-version-badge-match (1.66.4) / m6-claude-md-version (2.0.0) / m6-arch-doc-stale / i18n-readme-translation-currency / claude-md-changelog-free (151 行) / coordination-gate-invocation (4 次生产调用) / config-template-key-currency / plugin-cache-currency (installed 1.66.4 = sot)

### 8. 同步状态
- 当前分支与 origin 对齐 (evidence fresh)
- 多远程: origin=equal; github 无本地跟踪引用 (parity unknown, 功能分支未推 github 属正常); 子模块 standards 处于 detached HEAD (两远程 unknown); aria 子模块 origin 侧 `orphan_unverified` 已连续 2 次 (指针 `0fe2e0d` 为本地未推的 v1.66.3-17 提交, 主仓尚未发布引用)
- 软错误 (唯一): `snapshot_consistency_inconclusive` —— 164 条 handoff track 在 github 侧无法核 AC-5, 本次 `overall_parity=true` 应视为未验证
- README 版本: aria plugin 1.66.4 = README 1.66.4

### 9. Open Issues (issue_scan 已启用)
- 共 44 条 open。头部: #188 四维一致性恒假阳性 + UPM collector / #184 brainstorm 被共装插件绕过 / #182 handoff status 从不收口 / #180 claim collision surface 30 分钟后失效 / #178 hook 类 Spec SC 需声明副本 / #177 CLAUDE.md 发布同步面 (已链 `linked-issue-normalization`)

### Handoff 感知
- 最新交接 `docs/handoff/2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md` (8.9 小时前, 由 latest.md 指针解析, frontmatter 完整), 无错放文件
- 多分支轨道: 扫 8 个分支, 检出 `self_multi_container` 碰撞 (dev-claude 与 simonfishgit/dev-claude; aria-runner-bot/023236f2 与 simonfish/bfe8285d) —— 进 Phase B 时应走 advisory claim 闸门 (coordination 已启用)

### 10. 推荐工作流
当前 intent 为状态查询, 不启动工作流。若接下来要动手, 按状态给的选项:

1. **(推荐) 继续 `linked-issue-normalization` Phase B** —— 当前分支就是它, owner 已 override 进 B; 进入前先跑 phase1_gate advisory claim (有 self_multi_container 碰撞)
2. 先处理 aria 子模块指针: 子模块 `0fe2e0d` 未推远程且主仓未提交, 要么推 aria 子模块并提交 gitlink, 要么回退指针 —— 否则 gitlink orphan 风险持续累积
3. 仅提交当前基准结果目录 (Level 1, commit_only)
4. 转去 triage 新 open issue (#188 的 UPM 认不到根 UPM.md 正解释本次 `upm.configured=false`)

本次只做扫描与推荐, 未调用 workflow-runner / phase1_gate。
