已按 state-scanner Step 0 机械跑完 `scan.py` (退出码 10 = 部分软错误, snapshot 可用)。先回答你最关心的问题, 再给完整状态。

## 结论: 有一处配置遗漏, 且已被扫描器明确检出

```
🔗 Forgejo 配置检查
───────────────────────────────────────────────────────────────
  ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
```

snapshot 原始字段: `forgejo_config = {forgejo_remote_detected: true, instance: "forgejo.10cg.pub", config_status: "missing"}`。

一个要先说清的事实: **缺这个文件不影响 state-scanner 本身的 issue 扫描** —— 本次扫描已经通过 `forgejo` CLI wrapper (CF Access 后) 实时拉到 44 个 open issue (`issue_status.fetch_error = null`, `fetched_at = 2026-08-23T06:24:51Z`)。`CLAUDE.local.md` 里的 `forgejo:` 块是给 **forgejo-sync Skill** (Story → Issue 同步 / PRD → Wiki 发布) 用的; 没有它, forgejo-sync 会因为 Cloudflare Access 拦截而 403。

## 如何设置 Forgejo 集成

两条路, 推荐第一条:

**路 1 (推荐): 让 /forgejo-sync 引导创建**

```
/forgejo-sync
```

它会检测到 `CLAUDE.local.md` 不存在, 从 `git remote get-url origin` 推断出 `owner/repo` (本仓 = `10CG/Aria`), 对已知实例默认开启 `cloudflare_access`, 把将要写入的内容展示给你, 你确认 `[y]` 才落盘。拒绝则跳过继续 (无状态, 下次还会再问)。

**路 2: 手工创建** 在仓库根目录写 `CLAUDE.local.md`:

```yaml
## Forgejo Integration
forgejo:
  url: "https://forgejo.10cg.pub"
  repo: "10CG/Aria"
  api_token: "${FORGEJO_TOKEN}"
  cloudflare_access:
    enabled: true
    client_id_env: "CF_ACCESS_CLIENT_ID"
    client_secret_env: "CF_ACCESS_CLIENT_SECRET"
```

然后在 shell 里设三个环境变量 (值不要写进任何文件; Rule #7 secret 卫生):

```bash
export FORGEJO_TOKEN="<Forgejo 个人 token>"
export CF_ACCESS_CLIENT_ID="<CF Access service token id>"
export CF_ACCESS_CLIENT_SECRET="<CF Access service token secret>"
```

两个注意点:

1. `CLAUDE.local.md` 是个人本地配置, 不要提交进 git (确认 `.gitignore` 覆盖它)。
2. 扫描器判定「已配置」靠的是文件里**正文**出现 `forgejo:` YAML 键或 `# forgejo` 标题; 放在 ``` 代码围栏里的示例不算数 (防止粘贴文档示例造成假配置)。写完重跑 `/state-scanner` 看到 `✅ Forgejo 配置: 已配置 (forgejo.10cg.pub)` 即完成。

可选字段 (按需追加到同一块): `default_labels: ["user-story"]` / `auto_create_milestone: true` / `wiki: {enabled: true, page_prefix: "PRD-", generate_index: true}`。

---

## 完整项目状态 (snapshot 摘要)

### 📍 当前状态
- 分支: `feature/linked-issue-normalization` (upstream `origin/feature/linked-issue-normalization`, ahead 0 / behind 0)
- 模块: UPM 未配置 (`upm.configured = false`, 无 Phase / Cycle 数据)
- 变更文件: 2 (类型 other, 工作树基本干净)
- 无 git 中间态操作 (rebase / merge 等), 无中断的 workflow-state
- 最近提交: `826b356 docs(spec): linked-issue-normalization R5-fix 九条 (2C+7M) + owner override 进 Phase B`

### 📊 变更分析
- 复杂度: Level 1 | 架构影响: 无 | 测试覆盖: 无 | Skill 变更: 未检出

### 📄 需求状态
- 已配置。PRD: `prd-aria-v1.md` (active) / `prd-aria-v2.md` (pending)
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1

### 🏗️ 架构状态
- `docs/architecture/system-architecture.md` 存在, status Active, 最后更新 2026-05-27
- 需求链路: `chain_valid = false` (parent_prd 未声明) —— 非本次关注点, 顺带标注

### 📋 OpenSpec 状态
- 已归档 138 个, 待归档 0
- ⚠️ 设计未实施 6 个 (approved 但 tasks 大量未勾): m6-cost-model-telemetry (44 天) / m6-dispatch-input-delivery (49 天) / m6-e2e-resilience (41 天) / m6-release-closeout (89 天) / m7-agent-lifecycle (65 天) / m7-fleet-aggregation (34 天)。与 CLAUDE.md 项目状态一致 (卡 owner / 基建门)。

### 🛡️ 审计状态
- 启用。最近审计报告: `.aria/audit-reports/linked-issue-normalization-audit-trail.md` (verdict / 收敛轮数字段解析为空, 需读原文)

### 🔧 自定义检查
- 10/10 通过: issue-cache-freshness / silknode-contract-deferral-expiry / m6-version-badge-match / m6-claude-md-version / m6-arch-doc-stale / i18n-readme-translation-currency / claude-md-changelog-free / coordination-gate-invocation / config-template-key-currency / plugin-cache-currency

### 🔄 同步状态
- 当前分支与 origin 同步 (0/0)
- 多远程 (origin + github): `overall_parity = true`, 三个子模块 gitlink 在 origin 均 ok; github 侧本分支无已发布引用 (feature 分支只推 origin, 正常)
- 📝 README 版本一致: aria 插件 1.66.4 = README 1.66.4
- 🔗 Forgejo 配置: **缺失** (见顶部)
- ⚠️ 软错误 (退出码 10 的来源): `snapshot_consistency` 对 164 个 legacy handoff track 在 github 远程无法评估 AC-5, 本次 parity 判决按「未验证」对待。这是已知问题 (Aria #176 / #169 在 open issue 里), 不影响本次 Forgejo 结论。

### 🎫 Open Issues
- 平台 Forgejo (10CG/Aria) — 44 open, 数据来源 live
- 与本话题直接相关: #167 「Forgejo API 调用层支持可插拔 HTTP 传输」(FR)
- 其余为 secret-guard / state-scanner / coordination 缺陷串 (#188 / #184 / #182 / #176 / #173 ...), 详见 snapshot `issue_status.items`

### 🌲 多终端协调
- `tracks_multibranch.collision.kind = self_multi_container` (组: dev-claude 与 simonfishgit/dev-claude; aria-runner-bot/023236f2 与 simonfish/bfe8285d)。进 Phase B 前 phase1_gate 会做 advisory 认领; 本次只读扫描不触发。

### 🎯 推荐工作流
你的意图是「补 Forgejo 配置」, 不是开发周期, 所以不推荐进十步循环:

- **[1] 运行 `/forgejo-sync` 引导创建 `CLAUDE.local.md` (推荐)** —— 交互确认, 零手写
- [2] 手工按上面模板创建 + 设 3 个环境变量, 然后重跑 `/state-scanner` 验证
- [3] 只看状态, 暂不配置 (state-scanner 的 issue 扫描不受影响, 仅 forgejo-sync 不可用)
- [4] 自定义

理由: `forgejo_config.config_status = missing` 是唯一检出的配置遗漏; 其他检查 10/10 通过, 工作树干净, 无在途 workflow。
