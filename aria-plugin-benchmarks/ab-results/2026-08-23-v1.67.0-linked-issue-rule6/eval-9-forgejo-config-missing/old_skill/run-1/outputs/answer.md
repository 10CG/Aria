已按 state-scanner Step 0 机械跑完 `scan.py` (退出码 10 = 有软错误但 snapshot 可用), 下面是扫描结果和 Forgejo 配置的结论。

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: feature/linked-issue-normalization (upstream origin/同名, ahead 0 / behind 0)
  HEAD: 826b356 "docs(spec): linked-issue-normalization R5-fix 九条 (2C+7M) + owner override 进 Phase B"
  工作区: 2 处未提交 — 子模块 `aria` 指针变动 (unstaged) + 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-08-23-.../`
  UPM: 未配置 (collector 没认到仓库根 UPM.md, 即 issue #188 描述的已知问题)
  中断检测: 无 (`.aria/workflow-state.json` 不存在); git 无 rebase/merge 中间态

📊 变更分析
───────────────────────────────────────────────────────────────
  变更文件: 2 (类型 other) | 复杂度: Level 1 | 架构影响: 无 | Skill 变更: 未检出

📄 需求状态 / 🏗️ 架构状态
───────────────────────────────────────────────────────────────
  PRD: prd-aria-v1 (active), prd-aria-v2 (Approved, 归一为 pending)
  User Stories: done 17 / in_progress 2 / approved 1 / pending 1
  System Architecture: 存在, status Active, 最后更新 2026-05-27; `chain_valid=false` (未声明 parent PRD, 链路不完整)

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 0 | 待归档: 0 | 已归档: 多条 (最早 2025-12-16 spec-drafter)
  注: 当前分支名对应的 linked-issue-normalization 变更未出现在 active 列表, 审计轨迹在 `.aria/audit-reports/linked-issue-normalization-audit-trail.md`

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  审计系统: enabled | 上次审计: linked-issue-normalization-audit-trail.md (verdict / 收敛轮数字段未解析出来)

🔧 自定义检查 (`.aria/state-checks.yaml`)
───────────────────────────────────────────────────────────────
  10/10 通过: issue-cache-freshness / silknode-contract-deferral-expiry / m6-version-badge-match (badge=1.66.4) /
  m6-claude-md-version (2.0.0) / m6-arch-doc-stale (88d) / i18n-readme-translation-currency / claude-md-changelog-free /
  coordination-gate-invocation / config-template-key-currency / plugin-cache-currency

🔄 同步状态
───────────────────────────────────────────────────────────────
  origin (forgejo.10cg.pub): parity equal (826b356) | github: 无本地 tracking ref, parity unknown
  子模块 gitlink: origin 三个子模块全 ok; github 三个 `no_published_ref` (本分支未推 github, 属正常)
  ⚠️ scan.py 软错误 (errors[0], snapshot_consistency_inconclusive): AC-5 一致性检查对 164 条 legacy handoff track 在 github 上 git 命令失败, 本次 `overall_parity=true` 视为未经验证。这就是 issue #176 记录的已知缺陷, 不影响你的问题。
  📝 README 版本: aria 子模块 plugin.json 1.66.4 = README 1.66.4 ✅ | 📦 standards 子模块: 已初始化且已注册 ✅

  🔗 Forgejo 配置检查
  ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)

🎫 Open Issues (issue_scan 已启用, 平台 forgejo, 2026-08-23T06:24:51Z 实时拉取)
───────────────────────────────────────────────────────────────
  open 44 (10CG/Aria), 较新的几条:
  #188 四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md (本次扫描 upm.configured=false 正是此症状)
  #184 aria:brainstorm 被共装插件静默绕过
  #182 handoff frontmatter status 从不收口 (本次 tracks_multibranch 里 legacy_count=168 即此现象)
  #180 coordination claim collision surface 30 分钟后静默失效
  #177 CLAUDE.md 发布同步面那行是漏同步面的类级根因 (linked_openspec=linked-issue-normalization)
  #176 AC-5 一致性检测未排除本仓不存在的 remote → 退出码恒为 10 (本次退出码 10 的来源)

🌲 多终端协调
───────────────────────────────────────────────────────────────
  `tracks_multibranch.collision.kind = self_multi_container`: 同 owner 多容器 (dev-claude / simonfishgit/dev-claude; aria-runner-bot/023236f2 / simonfish/bfe8285d)。按 SKILL 契约这只在你确认进 Phase B 时才触发 phase1_gate advisory; 本次只读扫描不调用。
  最新 handoff: docs/handoff/2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md (9 小时前, frontmatter 完整); 跨 worktree 无其他活跃交接。

───────────────────────────────────────────────────────────────

## 回答你的问题: 遗漏了什么配置, 怎么设置 Forgejo 集成

**遗漏的只有一项**: `CLAUDE.local.md` 里的 `forgejo:` 配置块 (文件本身也不存在)。其余 Forgejo 相关配置已经齐了:

| 项目 | 状态 | 依据 |
|------|------|------|
| git remote 指向 Forgejo | ✅ | origin = `ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git` |
| `.aria/config.json` 的 `issue_scan` | ✅ 已启用 | platform=forgejo, platform_hostnames.forgejo=["forgejo.10cg.pub"]; 本次成功实时拉到 44 条 issue, 说明 `forgejo` CLI wrapper 和 CF Access 凭据在当前 shell 里是通的 |
| `CLAUDE.local.md` 的 `forgejo:` 块 | ❌ 缺失 | forgejo_config collector: `config_status=missing` |

影响范围要说清楚: 只读的 issue 扫描 (state-scanner Phase 1.13) **不依赖** CLAUDE.local.md, 它走 `forgejo` CLI wrapper, 现在已经能用。CLAUDE.local.md 的 `forgejo:` 块是给 **写操作** 的 `/forgejo-sync` 用的 (User Story 同步成 Issue、PRD 发布到 Wiki)。所以如果你暂时不用 forgejo-sync, 这个缺失不会卡住任何流程; 要用就补上。

**设置步骤 (两种方式任选一)**

方式 A: 让 skill 引导创建 (推荐)
1. 运行 `/forgejo-sync`
2. 它会检测到 CLAUDE.local.md 缺失, 从 origin URL 推断出 `10CG/Aria`, 对已知实例默认打开 `cloudflare_access`, 展示完整内容后问你 [y/N]
3. 确认后写入文件, 然后继续原有流程

方式 B: 手工创建 `/home/dev/Aria/CLAUDE.local.md`, 内容:

```yaml
## Forgejo Integration
forgejo:
  url: "https://forgejo.10cg.pub"
  api_token: "${FORGEJO_TOKEN}"
  repo: "10CG/Aria"
  cloudflare_access:
    enabled: true
    client_id_env: "CF_ACCESS_CLIENT_ID"
    client_secret_env: "CF_ACCESS_CLIENT_SECRET"
```

并保证三个环境变量在 shell 里已导出: `FORGEJO_TOKEN` / `CF_ACCESS_CLIENT_ID` / `CF_ACCESS_CLIENT_SECRET`。注意 forgejo.10cg.pub 在 Cloudflare Access 后面, `cloudflare_access.enabled` 必须为 true, 否则 API 调用会收到 403 + Cloudflare challenge。

两点提醒:
- 文件里只写 `${ENV}` 引用, 不要把 token 字面值写进去 (Rule #7 secret 卫生)。验证时看 HTTP 状态码和 key 名, 不要 echo 变量值。
- 我检查了一下, `CLAUDE.local.md` 目前**没有**被 `.gitignore` 忽略 (`git check-ignore` 返回 1)。创建前建议先把它加进 `.gitignore`, 否则配置文件会出现在 `git status` 的未跟踪列表里, 也有误提交的风险。
- 写成 `forgejo:` YAML 键或 `## forgejo` 标题都能被 collector 识别; 但别只放在 ``` 代码块里, 代码块内的示例会被当作文档样例而不算真配置。

配置好以后重跑 `/state-scanner`, 🔗 Forgejo 配置检查那行应变成 `✅ Forgejo 配置: 已配置 (forgejo.10cg.pub)`。

🎯 推荐工作流
───────────────────────────────────────────────────────────────
  ➤ [1] 补 Forgejo 配置 (推荐, 不进十步循环): 把 `CLAUDE.local.md` 加进 `.gitignore` → 运行 `/forgejo-sync` 引导创建 (或按方式 B 手写) → 重跑 `/state-scanner` 确认 ✅
  [2] 仅查看状态, 不做任何事 (当前工作区的 2 处变更都是 benchmark 产物, 不需要提交流程)
  [3] 继续当前分支的开发工作 (linked-issue-normalization 已 owner override 进 Phase B) — 确认后会先跑 phase1_gate advisory 认领 (collision=self_multi_container)
  [4] 自定义组合

理由: 你的问题是配置缺口, 不涉及代码变更 (变更分析 Level 1, 全是 benchmark 输出), 不需要启动 Phase A-D 工作流; 补配置是单文件动作, 由 `/forgejo-sync` 自己的引导流程完成即可。
