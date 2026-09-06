# Aria Versioning Scheme — Four Independent Streams

> **Status**: Active
> **Created**: 2026-05-27
> **Last Updated**: 2026-05-27
> **Parent Document**: [system-architecture.md](system-architecture.md)
> **Related**: [docs/release-notes-v2.0.0.md](../release-notes-v2.0.0.md)

---

## Overview

Aria 项目包含四个**独立**的版本流。这四个版本号在语义上互不依赖，各自按照自己的节奏演进。理解这一点对于避免误操作（例如误以为 aria-plugin 需要随 Aria 2.0 一起 bump 到 v2.0）至关重要。

---

## Four Independent Versioning Streams

| 版本流 | 仓库 / 路径 | 当前版本 | SoT 文件 | Bump 触发 | 备注 |
|--------|------------|----------|----------|-----------|------|
| **Aria main repo** | `/home/dev/Aria/` | v1.7.5 | `VERSION` | 里程碑 M0-M6；MAJOR on autonomous runtime 正式发布 | 方法论 + 运行时的整体版本 |
| **Aria 2.0 runtime (aria-orchestrator)** | `aria-orchestrator/` | v2.x (M6 in progress) | `aria-orchestrator/pyproject.toml` 或 VERSION | MINOR on new Layer 1/2 capability | 10CG Lab 内部，不公开发布 |
| **aria-plugin** | `aria/` (子模块) | v1.70.0 | `aria/.claude-plugin/plugin.json` | MINOR on new Skill/Agent; PATCH on bug fix | 独立于 Aria main repo；**不随 Aria 2.0 同 bump** |
| **Aria 2.0 PRD** | `docs/requirements/prd-aria-v2.md` | v2.0.0 | PRD frontmatter `**Version**:` 字段 | 文档修订（需求变化时更新） | 文档版本，非代码版本 |

---

## Why Streams Are Independent

### 语义边界

这四个版本流代表的是**不同维度**的演进：

```
Aria main repo (v1.x → v2.0):
  └─ 方法论成熟度 + 自主运行时里程碑
     └─ 例：M5 ship (US-025) → v1.7.0 → v2.0.0 (M6 closeout)

aria-plugin (v1.15.x → v1.28.x → ...):
  └─ Claude Code 插件的 Skills / Agents 能力迭代
     └─ 例：新增 Skill → MINOR bump；bug fix → PATCH bump
     └─ 与 Aria main repo 里程碑完全解耦

aria-orchestrator (v2.x):
  └─ 自主运行时内部能力（Layer 1 / Layer 2 新功能）
     └─ 例：新增崩溃恢复模式 → MINOR bump

Aria 2.0 PRD (v2.0.0):
  └─ 产品需求文档修订版本
     └─ 例：PRD patch e884e62 修正 §656 rubric metric → PRD 版本注记更新
```

### 受众分离

| 版本流 | 受众 | 是否公开 |
|--------|------|----------|
| Aria main repo | 任何使用 Aria 方法论的开发者 + 10CG Lab | 是（GitHub 公开） |
| aria-plugin | 任何安装 aria-plugin 的 Claude Code 用户 | 是（插件市场） |
| aria-orchestrator | 10CG Lab 内部 | 否（内部基础设施） |
| Aria 2.0 PRD | Aria 项目研究人员 | 是（公开文档） |

aria-plugin 的用户群体**远大于** Aria main repo v2.0 的受众。全球任何 Claude Code 用户都可以安装 aria-plugin，但 aria-orchestrator（自主运行时）仅限 10CG Lab 内部使用。因此，将 aria-plugin 版本号绑定到 Aria main repo 版本号没有意义——这会给大量插件用户造成不必要的困惑（"我需要升级插件到 v2.0 吗？"——不需要）。

---

## Plugin Compatibility Clarification

### aria-plugin 不随 Aria 2.0 同 bump

**重要结论**: 当 Aria main repo 发布 v2.0.0 时，aria-plugin **不会** bump 到 v2.0。

aria-plugin 目前处于 v1.28.x 系列。当 Aria v2.0.0 发布时：
- aria-plugin 保持在 v1.28.x（或该时间点的最新 v1.x 版本）
- 插件用户无需做任何操作
- 已安装的 aria-plugin 继续正常工作，无任何变化

这不是一个临时决定，而是**设计原则**：两个版本流在语义上永久解耦。

### 详细说明

跨版本兼容说明请参阅：[docs/release-notes-v2.0.0.md §Plugin Compatibility](../release-notes-v2.0.0.md#plugin-compatibility--aria-plugin-不随-aria-20-同-bump)

该章节（TG-DOCS-A，2026-05-27 via PR #129 已 ship）包含：
- Plugin Compatibility 完整说明
- Forgejo Discussion FAQ（含"是否需要升级插件"的答复）

---

## Version Lookup Reference

对于每个版本流，以下是获取当前版本的**精确**命令或文件路径：

### Stream 1: Aria main repo

```bash
cat /home/dev/Aria/VERSION
```

输出示例：`1.7.0`（VERSION 文件顶部的版本号字段）

### Stream 2: Aria 2.0 runtime (aria-orchestrator)

```bash
cat docs/release-notes-v2.0.0.md | head -3
```

输出示例（当 v2.0.0 完成后）：`Aria v2.0.0 Release Notes` + 状态行

或查询 aria-orchestrator 子目录内部版本文件（如存在）：

```bash
# 若 aria-orchestrator 有 pyproject.toml:
grep -m1 "version" /home/dev/Aria/aria-orchestrator/pyproject.toml 2>/dev/null || echo "see aria-orchestrator/ root"
```

### Stream 3: aria-plugin

```bash
python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"
```

输出示例：`1.28.0`

该命令是**动态读取**的规范方式，不得硬编码版本号（per Spec #3 Diff 9 / AC-3 规定）。

### Stream 4: Aria 2.0 PRD

```bash
git -C /home/dev/Aria rev-parse --short HEAD
```

PRD 文档版本由 frontmatter `**Version**:` 字段追踪（当前 v2.0.0）。子模块 standards 版本：

```bash
git -C standards rev-parse --short HEAD
```

---

## Version Consistency Checks

下列检查由 `.aria/state-checks.yaml` 自动监控（M6 state-checks probes，TG-DOCS-A 交付）：

| Probe 名 | 检查内容 | 严重级别 |
|---------|----------|----------|
| `m6-version-badge-match` | README.md 中的 Plugin badge 版本 == aria/.claude-plugin/plugin.json | warning |
| `m6-claude-md-version` | CLAUDE.md 顶层 `**版本**:` 字段 == `2.0.0` | warning |
| `m6-arch-doc-stale` | system-architecture.md `**Last Updated**` 距今 < 90 天 | warning |

执行 state-scanner 可获取上述检查的实时结果：`/state-scanner` 或 `/aria:state-scanner`

---

## Submodule Pointer vs Package Version

注意区分**子模块指针 SHA** 和**包版本号**：

| 概念 | 位置 | 示例 |
|------|------|------|
| `aria/` 子模块指针 | 主 repo git tree 中 `.gitmodules` + git 对象 | `1b8ec3f`（SHA） |
| aria-plugin 版本号 | `aria/.claude-plugin/plugin.json` 的 `version` 字段 | `1.28.0` |
| `standards/` 子模块指针 | 主 repo git tree | `4b834d0`（SHA） |
| aria-standards 版本 | standards 内部 CHANGELOG（若有） | 无正式 semver |

子模块指针 bump 和包版本 bump 是两件独立的事。每次 aria-plugin 发版（版本 bump）后，主 repo 需要额外执行 `git add aria` 来更新子模块指针（参见 CLAUDE.md §版本发布检查清单）。

---

## Related Documents

- [system-architecture.md](system-architecture.md) — §2.8 版本方案交叉引用
- [../release-notes-v2.0.0.md](../release-notes-v2.0.0.md) — v2.0.0 发版说明 + Plugin Compatibility
- [../requirements/prd-aria-v2.md](../requirements/prd-aria-v2.md) — Aria 2.0 PRD
- CLAUDE.md §版本管理规范 — 版本发布检查清单
- CLAUDE.md §项目状态 — 当前运行时版本状态
