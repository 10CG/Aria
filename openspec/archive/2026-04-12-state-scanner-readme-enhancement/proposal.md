# state-scanner 阶段 1.8 README 检查增强

> **Level**: Minimal (Level 2 Spec)
> **Status**: Complete (merged aria-plugin PR #11, 2026-04-12)
> **Created**: 2026-04-12
> **Parent Story**: N/A (Source Issue 直接驱动。US-008 已完成且聚焦于同步检测/Issue 感知，本 Spec 属于 state-scanner 增量改进)
> **Source**: [aria-plugin#9](https://forgejo.10cg.pub/10CG/aria-plugin/issues/9)
> **Target Version**: aria-plugin v1.14.0 (minor, 新增检查能力)
> **Release Coupling**: 与 forgejo-sync-local-md-guide Spec 同属 v1.14.0，但互相独立，任一可单独发版。开发顺序: 本 Spec 先合并，forgejo-sync Spec 在此基础上 rebase。

## Why

state-scanner 阶段 1.8 (README 同步检查) 当前仅检查主项目 README 的版本号和日期。v1.13.0 发版时人工巡检发现 4 类漂移未被检测:

1. **子模块 README 版本号** — `aria/README.md` 停留在 v1.11.1，实际已发布 v1.13.0
2. **Skill 数量** — README 写 "30 Skills"，实际已增至 33
3. **Skill 列表完整性** — 新增 3 个 Skill 未出现在 README Skills 列表中
4. **Plugin badge** — 主项目 README badge 版本与 plugin.json 不一致

**影响**: state-scanner 是十步循环统一入口和发版决策依据。这些漏检意味着发版前的自动化质量保证存在盲区，漂移只能靠人工发现。

## What

### 扩展阶段 1.8 检查项

在现有版本号/日期 2 项检查基础上**新增**以下 4 项:

| 检查项 | 真理来源 | 匹配目标 |
|--------|---------|---------|
| 插件版本 (子模块) | `aria/.claude-plugin/plugin.json` → `version` | `aria/README.md` 中的 Version 行 |
| Skill 数量 | `ls aria/skills/` 目录计数 (排除内部 Skill) | 主项目 + 子模块 README 中 "N Skills" 数字 |
| Skill 列表完整性 | `ls aria/skills/` 目录列表 (排除内部 Skill) | `aria/README.md` Skills 表格/列表 |
| Plugin badge | `aria/.claude-plugin/plugin.json` → `version` | 主项目 README badge URL 中的版本号 |

#### 内部 Skill 排除标准

以 SKILL.md frontmatter 中 `user-invocable: false` 作为判定依据。当前 5 个内部 Skill: `agent-router`, `agent-team-audit`, `arch-common`, `config-loader`, `audit-engine`。面向用户的 Skill 数量 = 总目录数 - `user-invocable: false` 目录数。

#### Skill 列表解析策略

解析 `aria/README.md` 中的 Skills 表格/列表，匹配 `aria/skills/` 下面向用户的目录名。若 README 格式无法识别 (非标准 Markdown 表格/列表)，输出 info 提示 "无法解析 Skill 列表格式" 而非误报缺失项。

#### badge 版本解析策略

匹配主项目 README 中 shields.io 或类似 badge URL 中的版本号 (正则: `Plugin-v[\d.]+`)。若 badge 格式不匹配，降级为 info 提示而非报错。

### 输出格式

在现有阶段 1.8 输出区块中扩展:

```
📄 README 同步检查
───────────────────────────────────────────────────────────────
  ✅ 主项目版本号: 一致 (v1.5.0)
  ✅ 主项目日期: 一致
  ⚠️ 子模块版本号: 不一致 (plugin.json: v1.13.0, aria/README: v1.11.1)
  ⚠️ Skill 数量: 不一致 (实际: 33, README: 30)
  ⚠️ Skill 列表: 缺失 3 项 (project-analyzer, agent-gap-analyzer, agent-creator)
  ✅ Plugin badge: 一致
```

阶段 1.8 输出数据结构 (`readme_status.submodules.aria`) 需扩展新字段:

```yaml
readme_status:
  submodules:
    aria:
      exists: true
      version_match: false          # 已有
      plugin_version: "v1.13.0"     # 新增
      readme_version: "v1.11.1"     # 新增
      skill_count_match: false      # 新增
      skill_count_actual: 33        # 新增
      skill_count_readme: 30        # 新增
      skill_list_missing: [...]     # 新增 (info 级)
  badge:
    version_match: false            # 新增
```

### Severity 联动推荐引擎

| 检查项 | 失败 Severity | 推荐行为 |
|--------|--------------|---------|
| 子模块版本号 | warning | 触发 `readme_outdated` 规则，附加修复提示 |
| Skill 数量 | warning | 触发 `readme_outdated` 规则，附加修复提示 |
| Skill 列表 | info | 仅展示，列出缺失项，不触发推荐规则 |
| Plugin badge | warning | 触发 `readme_outdated` 规则，附加修复提示 |

现有 `readme_outdated` 规则 (priority 1.3) 的触发条件需扩展: 原条件仅覆盖 `readme_version_mismatch` 和 `readme_date_mismatch`，需新增 `readme_skill_count_mismatch` 和 `readme_badge_mismatch` 条件。

### 不做什么

- 不自动修复 README (只报告，修复由人类确认)
- 不检查 README 的 prose 内容质量 (超出范围)
- 不检查 CHANGELOG 条目完整性 (属于不同检查维度)
- 不扩展到非 aria 子模块的 README (当前仅 aria 子模块有此需求)

## Design Decisions

| ID | 决策 | 理由 |
|----|------|------|
| D1 | 扩展阶段 1.8 而非新阶段 | 同属 README 同步检查，逻辑内聚 |
| D2 | Skill 列表检查为 info 而非 warning | 列表格式可能因 README 重构变化，误报风险高；解析失败时降级为"无法解析"提示 |
| D3 | 仅检查 aria 子模块 README | 只有 aria-plugin 有版本号 + Skill 列表的同步需求 |
| D4 | 内部 Skill 以 `user-invocable: false` 判定 | 复用 SKILL.md frontmatter 已有机读字段，当前 5 个内部 Skill: agent-router, agent-team-audit, arch-common, config-loader, audit-engine |
| D5 | 扩展 `readme_outdated` 规则条件 | 新增检查项属于同一 "README 过时" 语义域，不需要独立规则 |

## Scope

### 影响文件

| 文件 | 变更类型 |
|------|---------|
| `aria/skills/state-scanner/SKILL.md` | 扩展阶段 1.8 检查逻辑 + 输出 YAML schema |
| `aria/skills/state-scanner/references/output-formats.md` | 更新阶段 1.8 输出示例 |
| `aria/skills/state-scanner/RECOMMENDATION_RULES.md` | 扩展 `readme_outdated` 规则触发条件 |

### 不影响

- config-loader、其他 Skills、Agents

## Acceptance Criteria

- [ ] 所有 6 项检查 (已有: 主项目版本号、主项目日期 + 4 新增) 均一致时输出全绿 (6 个 ✅)
- [ ] 子模块 `aria/README.md` 版本号与 `plugin.json` 不一致时报告 warning
- [ ] Skill 数量与 README 中声明的数字不一致时报告 warning (排除 `user-invocable: false` 的目录)
- [ ] Skill 列表检查失败时以 info 级别输出缺失项 (不触发 `readme_outdated` 规则)
- [ ] Skill 列表格式无法解析时输出 info "无法解析 Skill 列表格式"，不误报缺失项
- [ ] Plugin badge 版本与 plugin.json 不一致时报告 warning
- [ ] badge 格式不匹配时降级为 info 提示
- [ ] 所有新增检查项在子模块不存在时优雅降级 (跳过，不报错)
- [ ] `RECOMMENDATION_RULES.md` 的 `readme_outdated` 规则包含新增条件
- [ ] AB Benchmark 通过 (Rule #6, SKILL.md 变更)

## Estimation

- **工作量**: 4-6 小时 (含 RECOMMENDATION_RULES.md 扩展和解析策略实现)
- **风险**: 低 (单模块扩展，无跨模块依赖)
