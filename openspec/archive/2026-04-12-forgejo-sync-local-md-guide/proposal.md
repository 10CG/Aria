# forgejo-sync 主动引导创建 CLAUDE.local.md

> **Level**: Minimal (Level 2 Spec)
> **Status**: Complete (merged aria-plugin PR #11, 2026-04-12)
> **Created**: 2026-04-12
> **Parent Story**: N/A (Source Issue 直接驱动。无现有 US 覆盖 forgejo-sync DX 改进)
> **Source**: [aria-plugin#10](https://forgejo.10cg.pub/10CG/aria-plugin/issues/10)
> **Target Version**: aria-plugin v1.14.0
> **Release Coupling**: 与 state-scanner-readme-enhancement Spec 同属 v1.14.0，但互相独立，任一可单独发版。开发顺序: 本 Spec 在 state-scanner-readme-enhancement 合并后 rebase。
> **Depends**: state-scanner-readme-enhancement (软依赖 — 开发顺序，非功能阻塞)

## Why

aria 没有任何地方会**主动引导**用户创建 `CLAUDE.local.md` 中的 Forgejo 配置。当前唯一的检测发生在 forgejo-sync 的 PRE_CHECK 步骤——API 调用失败后才被动提示，属于**事后兜底**而非主动引导。

**实际影响**:
- `forgejo.10cg.pub` 前面有 Cloudflare Access，所有 HTTPS API 调用必须带 CF 头
- SSH git 操作不受影响，但 Issue 创建/PR 创建/状态同步等 API 操作会被 302 拦截
- 10 个项目中只有 1 个 (Kino) 有 `CLAUDE.local.md`，且为手动创建
- 缺失配置的项目在调用 forgejo-sync 时必然失败一次才能发现问题

**安全评估**: `CLAUDE.local.md` 中的 forgejo 配置**不含密钥**，仅包含:
1. 开关 (`cloudflare_access.enabled: true`)
2. 环境变量**名**的引用 (`CF_ACCESS_CLIENT_ID` 等)
3. 项目的 repo 标识 (`owner/repo`)

实际密钥已在容器环境变量中配置，自动创建此文件是安全的。

## What

### 方案 A: state-scanner 新增 Forgejo 配置检测 (阶段 1.14)

在现有扫描阶段之后新增检测 (阶段 1.14，当前最高编号 1.13 + 1)。

**编号约束 (D8 遵从声明)**: US-008 D8 规定 state-scanner 子阶段上限为 15。本 Spec 消耗编号 1.14，当前已用 14 个阶段 (0, 1, 1.5~1.13, 2, 3, 4)，剩余配额 1 (仅 1.15 可用)。后续 Spec 新增阶段需注意上限。

**检测逻辑**:
1. 检查 git remote URL 是否为已知 Forgejo 实例 (`forgejo.10cg.pub`，硬编码于 SKILL.md)
2. 检查 `CLAUDE.local.md` 是否存在
3. 如存在，检查是否包含 `forgejo` 配置块

**输出**:
```
# 场景 1: 文件不存在
🔗 Forgejo 配置检查
───────────────────────────────────────────────────────────────
  ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)

# 场景 2: 文件存在但缺少 forgejo 配置块
🔗 Forgejo 配置检查
───────────────────────────────────────────────────────────────
  ⚠️ CLAUDE.local.md 存在但缺少 forgejo 配置块
     建议: 运行 /forgejo-sync 可引导追加配置 (需确认)
```

**Severity**: warning (不阻断推荐，附加提示)

**注意**: state-scanner 与 forgejo-sync 的 Forgejo 实例检测逻辑**各自独立实现**——这是有意为之的设计 (D6)。state-scanner 是只读扫描，forgejo-sync 是写入操作，职责不同，不共享检测工具函数。

### 方案 B: forgejo-sync PRE_CHECK 主动引导创建 (首次使用)

forgejo-sync 的 PRE_CHECK 步骤增加前置检测:

**触发条件**:
- git remote 是已知 Forgejo 实例
- `CLAUDE.local.md` 不存在，**或**文件存在但缺少 `forgejo:` 配置块

**行为 — 文件不存在时**:
1. 从 git remote URL 推断 `owner/repo` (支持 SSH `git@host:owner/repo.git` 和 HTTPS `https://host/owner/repo.git` 两种格式)
2. 对已知实例 (如 `forgejo.10cg.pub`) 默认 `cloudflare_access.enabled: true`
3. **展示**将要生成的完整配置内容
4. **提示用户确认** ("是否创建 CLAUDE.local.md? [y/N]")
5. 用户确认 → 创建文件，继续 PRE_CHECK 后续步骤
6. 用户拒绝 → 输出提示 "跳过配置创建，forgejo-sync 可能因 Cloudflare 拦截而失败"，**继续**执行后续步骤 (不中止)
7. 下次调用 forgejo-sync 时若仍缺失，**再次提示** (不记忆拒绝状态)

**行为 — 文件存在但缺少 forgejo 块时**:
1. **展示**将要追加的 forgejo 配置块内容
2. **提示用户确认** ("检测到 CLAUDE.local.md 已存在但缺少 forgejo 配置，是否追加? [y/N]")
3. 用户确认 → 在文件末尾追加 forgejo 配置块
4. 用户拒绝 → 同上，继续执行

**生成模板** (与 PRE_CHECK.md 配置 schema 字段一致):
```markdown
## Forgejo Integration
forgejo:
  url: "https://forgejo.10cg.pub"
  repo: "{owner}/{repo}"
  cloudflare_access:
    enabled: true
    client_id_env: "CF_ACCESS_CLIENT_ID"
    client_secret_env: "CF_ACCESS_CLIENT_SECRET"
```

### 不做什么

- 不静默创建或修改文件 (必须用户确认)
- 不在 session-start hook 中检测 (避免每次启动都执行 IO 检查)
- 不处理非 Forgejo 的 Git 平台 (GitHub/GitLab 不需要此配置)
- 不存储或传输密钥 (仅引用环境变量名)
- 不修改已有 forgejo 配置块的内容 (只在配置块缺失时创建/追加)
- 不支持自定义 Forgejo 实例白名单 (v1.14.0 硬编码 `forgejo.10cg.pub`，未来可扩展)
- 不记忆用户拒绝状态 (每次调用独立判断，保持无状态)

## Design Decisions

| ID | 决策 | 理由 |
|----|------|------|
| D1 | A+B 结合而非单一方案 | state-scanner 做温和提醒 (扫描时)，forgejo-sync 做即时创建 (按需时)，互补覆盖 |
| D2 | 用户确认后才写入 | 遵循 Aria "人类确认关键节点" 原则，不静默修改工作目录 |
| D3 | 仅对已知 Forgejo 实例启用 | 避免误判其他 Gitea/Forgejo 实例，白名单硬编码于 SKILL.md (v1.14.0 仅 `forgejo.10cg.pub`) |
| D4 | 不在 session-start hook 中检测 | session-start 应保持轻量，配置检测属于 state-scanner 职责 |
| D5 | 模板仅引用环境变量名 | 密钥管理不属于 aria 职责，保持安全边界 |
| D6 | state-scanner 与 forgejo-sync 各自独立检测 | 两者职责不同 (只读扫描 vs 写入操作)，独立实现优于共享工具函数——简单性优先于 DRY |
| D7 | 阶段 1.14 编号 (D8 遵从) | 当前最高编号 1.13，1.14 = 1.13 + 1，符合 US-008 D8 "追加到最大编号 + 1" 规则。已用 14/15 阶段，剩余 1 |
| D8 | 用户拒绝后继续执行 forgejo-sync | PRE_CHECK 引导是增强体验，不应阻塞用户的原有工作流 |

## Scope

### 影响文件

| 文件 | 变更类型 |
|------|---------|
| `aria/skills/state-scanner/SKILL.md` | 新增阶段 1.14 Forgejo 配置检测 |
| `aria/skills/state-scanner/references/output-formats.md` | 新增检测输出示例 |
| `aria/skills/state-scanner/RECOMMENDATION_RULES.md` | 新增 `forgejo_config_missing` 规则 (priority ~1.5, non-blocking) |
| `aria/skills/forgejo-sync/SKILL.md` | PRE_CHECK 增加主动引导创建逻辑 |
| `aria/skills/forgejo-sync/PRE_CHECK.md` | 更新前置检测流程描述 (新增 Forgejo 配置引导步骤) |

### 不影响

- config-loader (配置模板不变)
- session-start hook
- 其他 Skills、Agents

## Acceptance Criteria

- [ ] state-scanner 扫描时检测到 Forgejo 远程但缺少 CLAUDE.local.md 报告 warning
- [ ] state-scanner warning 措辞: 文件缺失时 "运行 /forgejo-sync 可引导创建配置 (需确认)"，文件存在但缺块时 "运行 /forgejo-sync 可引导追加配置 (需确认)"
- [ ] forgejo-sync 首次使用时检测缺失配置并展示完整配置内容，提示用户确认 [y/N]
- [ ] 用户拒绝后 forgejo-sync 继续执行后续步骤 (不中止)，并输出 Cloudflare 拦截风险提示
- [ ] 从 git remote URL 正确推断 owner/repo (覆盖 SSH `git@host:owner/repo.git` 和 HTTPS 两种格式)
- [ ] 生成的配置包含 `forgejo.url`, `forgejo.repo`, `forgejo.cloudflare_access.enabled`, `forgejo.cloudflare_access.client_id_env`, `forgejo.cloudflare_access.client_secret_env` 字段，与 PRE_CHECK.md schema 一致
- [ ] `CLAUDE.local.md` 已存在但缺少 forgejo 块时，提示追加而非跳过
- [ ] `CLAUDE.local.md` 已存在且包含 forgejo 配置时不重复提示
- [ ] 非 Forgejo 远程的项目不触发检测
- [ ] `RECOMMENDATION_RULES.md` 包含 `forgejo_config_missing` 规则
- [ ] AB Benchmark 通过 (Rule #6, SKILL.md 变更)

## Estimation

- **工作量**: 4-6 小时 (含两个 Skill 改动 + RECOMMENDATION_RULES.md + remote URL 解析)
- **风险**: 低 (两个 Skill 独立改动，无跨模块依赖)
