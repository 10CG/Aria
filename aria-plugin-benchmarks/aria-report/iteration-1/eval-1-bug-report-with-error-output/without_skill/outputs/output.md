# Bug Report: state-scanner 报告流程

## Issue 分类

**类型**: Bug Report
**标签**: `bug`

---

## 自动收集的环境信息

| 项目 | 值 |
|------|-----|
| Aria Plugin | 1.8.0 |
| Skills | 29 |
| OS | macOS (用户报告) |
| 项目配置 (.aria/config.json) | yes |

---

## 组合的 Issue 内容

即将提交以下 Issue 到目标仓库:

---

**标题**: bug(state-scanner): "Cannot read property phases of undefined" 导致扫描中断退出

```markdown
## Bug Report

**描述**: state-scanner 在执行项目状态扫描时中途崩溃，抛出 "Cannot read property phases of undefined" 错误后直接退出，未完成扫描也未给出任何推荐结果。

**复现步骤**:
1. 在项目根目录确认 `.aria/config.json` 配置文件存在
2. 调用 `/aria:state-scanner`（或等价触发方式）
3. 扫描开始执行，运行到某个阶段后报错
4. 输出 `Cannot read property phases of undefined`
5. Skill 直接退出，无后续输出

**预期行为**: state-scanner 应完成全部扫描阶段（状态收集 -> 推荐决策 -> 用户确认），输出项目状态报告和工作流推荐选项。如果某个阶段数据缺失，应优雅降级（使用默认值或标记为"未配置"），而非抛出异常退出。

**实际行为**: state-scanner 在扫描中途抛出 `Cannot read property phases of undefined` 错误并立即退出，未完成扫描、未展示任何状态报告或推荐选项。

**错误输出**:
```
Cannot read property phases of undefined
```

**可能的根因分析**:

根据错误消息 "Cannot read property phases of undefined"，问题很可能出在 state-scanner 阶段 0（中断检测）或阶段 2（推荐决策）访问 `workflow.phases` 字段时，`workflow` 对象为 `undefined`。

可能场景包括：
1. **`.aria/workflow-state.json` 存在但不完整**: 阶段 0 读取了一个损坏或格式不符合 `aria-workflow-state/v1` schema 的状态文件，其中缺少 `workflow` 对象或 `workflow.phases` 字段，但未按预期进行容错处理（应备份并跳过）。
2. **推荐规则处理中访问了未初始化的工作流上下文**: 阶段 2 在推荐规则匹配时尝试访问工作流模板的 `phases` 字段，但该模板对象未正确初始化。
3. **config-loader 返回值异常**: `.aria/config.json` 存在但配置加载逻辑返回了不完整的对象，后续代码假设存在 `phases` 属性但实际为 `undefined`。

**附加上下文**:
- 用户确认 `.aria/config.json` 配置文件存在
- 不确定 `.aria/workflow-state.json` 是否存在（可能是前次中断遗留）
- 扫描并非在启动时立即失败，而是"跑到一半"才报错

## 环境信息
- Aria Plugin: 1.8.0
- Skills: 29
- OS: macOS
- 项目配置 (.aria/config.json): yes

---
*由 aria-report 自动生成*
```

---

**标签**: bug
**目标仓库**: Forgejo `10CG/Aria`（内部用户）或 GitHub `10CG/aria-plugin`（外部用户）

---

## 提交前确认

此内容将公开可见。请确认：
  1. **提交** - 直接提交上述 Issue
  2. **编辑后提交** - 修改内容后再提交
  3. **取消** - 放弃提交

---

## 提交路由说明

Issue 的提交路由将按以下优先级自动选择：

| 优先级 | 条件 | 目标 |
|--------|------|------|
| 1 | `forgejo` CLI 可用 + `FORGEJO_TOKEN` 已设置 | Forgejo `https://forgejo.10cg.pub/10CG/Aria` |
| 2 | `GITHUB_TOKEN` 或 `GH_TOKEN` 已设置 | GitHub API `https://github.com/10CG/aria-plugin` |
| 3 | 无 token | GitHub Pre-filled URL（浏览器打开） |

用户确认提交后，系统会自动检测可用的提交通道并路由。

---

## 提交成功后的预期输出

**如果通过 API 提交成功：**

```
Issue 已提交
  URL:   {issue_url}
  类型:  Bug Report
  目标:  {Forgejo / GitHub}
  标题:  bug(state-scanner): "Cannot read property phases of undefined" 导致扫描中断退出
Aria 维护团队会尽快查看。
```

**如果无 token（Pre-filled URL）：**

```
Issue 已准备好
请在浏览器中打开以下链接提交:
  https://github.com/10CG/aria-plugin/issues/new?title=...&body=...&labels=bug
提示: 设置 GITHUB_TOKEN 可直接从终端提交。
```

---

## 临时排查建议

在等待维护团队响应期间，用户可以尝试以下排查步骤：

1. **检查是否存在遗留的 workflow-state.json**:
   ```bash
   cat .aria/workflow-state.json 2>/dev/null || echo "文件不存在"
   ```
   如果文件存在且内容不完整（缺少 `workflow.phases` 字段），可以安全删除：
   ```bash
   rm .aria/workflow-state.json
   ```

2. **验证 config.json 格式正确**:
   ```bash
   python3 -c "import json; json.load(open('.aria/config.json'))" && echo "JSON 格式正确" || echo "JSON 格式错误"
   ```

3. **删除后重试**:
   删除 `.aria/workflow-state.json` 后重新运行 `/aria:state-scanner`，看问题是否复现。
