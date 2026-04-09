# scan.sh 复杂度分析器安全 gap 修复 + Level 语义澄清

> **Level**: Minimal (Level 2 Spec)
> **Status**: Complete
> **Created**: 2026-04-09
> **Parent Story**: [US-007](../../docs/requirements/user-stories/US-007.md)
> **Target Version**: v1.4.2
> **Priority**: P0 (Security)

## Why

Agent Team 讨论 (R1-R3) 中 QA 实测发现 `aria-orchestrator/scan.sh` 的复杂度分析器存在**两个独立缺陷**:

### 缺陷 1: 安全关键词 gap (P0 Security)

当前 L65 的关键词列表:
```bash
grep -qiE '(architecture|breaking|migration|refactor|security)'
```

**问题**: 只包含 `security` 一个安全相关词汇, 大量高危场景不匹配:
- **"Fix SQL injection in login"** → 不含 `security` → 仅按长度判定 (可能被定为 L1)
- **"Patch XSS vulnerability"** → 同样漏判
- **"Authentication bypass"** → 漏判
- **"RCE via file upload"** → 漏判

**后果**: 在 Aria 2.0 自主 dispatch 模式下, L1 会被自动派发, 绕过人类审批。高危安全 issue 会进入自主开发闭环, 可能被 AI 错误修复后直接进 PR 待合并, 给审批者错觉"这只是个小修复"。

### 缺陷 2: Level 语义漂移 (P1 Naming)

scan.sh 的 `level` 变量 (1/2/3 = 复杂度等级) 与 `standards/openspec/project.md` 的 `Level` (1/2/3 = OpenSpec 规范深度) 语义**完全不同**:

| 概念 | scan.sh level | OpenSpec Level |
|------|--------------|----------------|
| 1 | quick-fix (简单) | Skip (无规范) |
| 2 | 需 OpenSpec (中等) | Minimal (proposal.md) |
| 3 | 需讨论 (复杂) | Full (proposal + tasks) |

虽然数值范围相同, 但**含义不同且不对应**。这造成:
- 文档读者困惑 (以为 scan 的 Level 2 = OpenSpec Level 2, 实际不是)
- Aria 2.0 Layer 1 的 LLM 可能混淆这两个概念
- 可重现性研究的知识污染

## What

### 修复 1: 扩展安全关键词 + L3 兜底

**修改 `aria-orchestrator/scan.sh` 的 `analyze_complexity` 函数**:

```bash
analyze_complexity() {
    local body="$1"
    local labels="${2:-}"
    local body_lines
    body_lines=$(echo "$body" | wc -l)
    local combined="$body $labels"

    local tier=1

    # Length-based
    if [ "$body_lines" -gt 20 ]; then
        tier=3
    elif [ "$body_lines" -gt 5 ]; then
        tier=2
    fi

    # 安全关键词 → 强制 L3 (bypass human approval 风险)
    if echo "$combined" | grep -qiE '(security|vulnerabilit|cve|exploit|injection|xss|csrf|rce|sqli|auth.*bypass|privilege.*escalat|credential|secret|password.*leak|token.*leak|data.*leak)'; then
        tier=3
    # 架构/破坏性变更 → L3
    elif echo "$combined" | grep -qiE '(architecture|breaking|migration|refactor)'; then
        [ "$tier" -lt 3 ] && tier=3
    # 功能性变更 → L2
    elif echo "$combined" | grep -qiE '(feature|new|add|implement|enhance)'; then
        [ "$tier" -lt 2 ] && tier=2
    fi

    echo "$tier"
}
```

**关键变化**:
1. 安全关键词独立为 **硬性规则** (不是 boost), 任何匹配 → 强制 L3
2. 扩展安全关键词集合 (vulnerability, cve, exploit, injection, xss, csrf, rce, sqli, auth bypass, privilege escalation, credential, secret leak, token leak, data leak)
3. 变量 rename `level` → `tier` (见修复 2)

### 修复 2: 变量重命名 `level` → `complexity_tier`

为消除与 OpenSpec Level 的语义混淆, 重命名:

| 旧名 | 新名 | 含义 |
|------|------|------|
| `level` (变量) | `tier` (变量) / `complexity_tier` (字段) | issue 复杂度等级 |
| `complexity_level` (JSON 字段) | `complexity_tier` | 同上 |
| `by_level` (聚合字段) | `by_complexity_tier` | 聚合统计 |
| `level_1/2/3` (聚合 key) | `tier_1/2/3` | 同上 |
| 显示 `[Level N]` | `[Complexity Tier N]` | 人类输出 |
| `recommend_action` 的 level 参数 | `tier` 参数 | 函数内变量 |

**修改范围**:
- `aria-orchestrator/scan.sh` (~19 处引用)
- `aria-orchestrator/schema/scan-result.json` (字段名)
- `aria-orchestrator/skills/heartbeat-scan/SKILL.md` (文档描述)
- `aria-orchestrator/heartbeat.sh` (解析 scan 输出时的字段名)

### 修复 3: 文档说明两个 Level 的区别

在 `aria-orchestrator/README.md` 或 `aria-orchestrator/docs/` 中添加说明:

```markdown
## 命名区分: Complexity Tier vs OpenSpec Level

- **Complexity Tier** (scan.sh / heartbeat-scan):
  issue 复杂度等级 (1/2/3), 用于 dispatch 路由决策
  - Tier 1: quick-fix (少行数 + 非安全)
  - Tier 2: 功能变更 (中等行数 或 feature 关键词)
  - Tier 3: 架构/安全/复杂 (长描述 或 安全关键词)

- **OpenSpec Level** (standards/openspec/):
  规范文档的深度要求 (1/2/3)
  - Level 1 (Skip): 简单修复, 无需规范
  - Level 2 (Minimal): proposal.md
  - Level 3 (Full): proposal.md + tasks.md

**两者数值相同但概念无关**, 不要混用。
```

## Decision Records

| ID | 决策 | 理由 |
|----|------|------|
| D1 | 安全关键词单独成为硬性 L3 规则 | 避免长度驱动绕过安全检查 |
| D2 | 扩展关键词集合 (10+ 安全词汇) | 覆盖常见漏洞类型, 降低漏判率 |
| D3 | rename `level` → `tier` 而非引入 standards 依赖 | 独立修复, 不增加 standards 子模块耦合 |
| D4 | 同 OpenSpec 同时修两个缺陷 | 两者在同一函数内, 分开 2 个 Spec 额外开销 |
| D5 | v1.4.2 patch 发布 | bug fix + 安全加固, 非新功能 |
| D6 | 保留原 `type` 字段 (bug/feature) | 不破坏外部消费者 |

## Acceptance Criteria

### 安全 gap 修复
- [ ] `scan.sh` 对 "fix SQL injection" 描述返回 tier=3
- [ ] `scan.sh` 对 "XSS vulnerability" 返回 tier=3
- [ ] `scan.sh` 对 "auth bypass" 返回 tier=3
- [ ] `scan.sh` 对 "credential leak" 返回 tier=3
- [ ] 短描述 (≤5 行) + 无关键词的普通 issue 仍为 tier=1
- [ ] 中等描述 (6-20 行) 或 feature 关键词 仍为 tier=2

### Rename 修复
- [ ] `scan.sh` 所有 `level` 变量 rename 为 `tier` 或 `complexity_tier`
- [ ] JSON 输出字段 `complexity_level` → `complexity_tier`
- [ ] 聚合字段 `by_level` → `by_complexity_tier`
- [ ] 聚合 key `level_N` → `tier_N`
- [ ] `schema/scan-result.json` 字段名同步
- [ ] `skills/heartbeat-scan/SKILL.md` 文档同步
- [ ] `heartbeat.sh` 解析 scan 输出的字段名同步
- [ ] 人类可读输出 `[Level N]` → `[Complexity Tier N]`

### 向后兼容
- [ ] 如有外部消费者依赖旧字段名, 在 CHANGELOG 说明 break change
- [ ] 或者: scan.sh 同时输出新旧字段 (带 deprecated 标记)

### 测试
- [ ] 手动 `bash scan.sh /home/dev/Aria --json` 输出正确
- [ ] 回归测试: heartbeat.sh 能正确解析新字段
- [ ] 测试用例覆盖 tier=1/2/3 的 3 种场景
- [ ] 测试用例覆盖安全关键词匹配
