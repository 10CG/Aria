# Spec Level 判断: "修复登录页面一个 typo"

```
═══════════════════════════════════════════════════════════
  LEVEL 1 DETECTED - SKIP SPEC
═══════════════════════════════════════════════════════════

此需求为简单修复，建议直接跳过 A.1：
- 类型: Typo 修复 (登录页面文案)
- 影响: 单文件 (登录页面所在的单个 UI 文件)
- 风险: 极低 (纯文本修正, 不改行为, 不改接口)

📋 推荐操作:
   直接进入 B.1 (分支创建) 开始开发
```

**结论: Level 1 (Skip) —— 不创建 OpenSpec proposal.md, 直接进入 B.1。**

---

## 判断依据 (按 LEVEL_GUIDE.md 规则逐项)

### 1. 决策流程图 Q1

> Q1: 是否简单修复/配置/文档格式? → YES → LEVEL 1 (Skip)

"修复 ... 一个 typo" 是典型的简单修复, 在 Q1 即命中 YES, 不再进入 Q2 (架构变更/跨模块/Breaking 判断)。

### 2. 关键词匹配 (权重 40%)

| 命中词 | 归类 | 说明 |
|--------|------|------|
| `typo` | Level 1 高置信度触发词 | LEVEL_GUIDE 明列 `typo, fix typo` |
| `修复` | Level 1 (对应 `fix` / `minor fix`) | 修复动作, 非功能开发 |
| `一个` | Level 1 上下文限定词 | 对应 `just` / `only` / `small`, 强调范围极小 |

未命中任何 Level 2 触发词 (feature / 功能 / add / 添加 / implement / 实现 / new / 新建 / 创建 / component / 改进 / 扩展), 也未命中任何 Level 3 触发词 (架构 / 重构 / redesign / breaking / migration / 跨模块 / system-wide / core)。

关于 "登录页面": "登录" 只是 typo 的**位置**, 不是变更类型。请求里没有 "添加 / 实现 / 改造 登录功能" 这类功能动词, 因此不构成 LEVEL_GUIDE 边界情况里 "Add simple authentication feature" 那种 Level 1 与 Level 2 的关键词冲突, 无需按 "冲突时取更高 Level" 提升。

### 3. 文件影响范围 (权重 30%)

- 模块检测: "页面 / 登录页面" → UI 侧单一模块 (按 LEVEL_GUIDE 模块映射, UI 关键词归 `mobile`; 若项目为 Web 前端则对应前端模块), 只涉及 1 个模块。
- 不修改 `shared/`, 不涉及 API 契约变更, 不影响多个子模块 → 不满足任何 "跨模块条件", 不触发自动提升为 Level 3。
- 预期改动: 单文件内一处文案字符串。

### 4. 变更类型 (权重 20%)

纯文本勘正, 非功能性变更, 无 breaking change, 无数据 / 接口 / 行为变化。

### 5. 历史模式 (权重 10%)

与 LEVEL_GUIDE 示例 3 "Fix typo in README → Level 1" 同形状, 仅载体从 README 换成登录页面文案, 判定不变。

### 6. 综合评分

四项因素全部落在最低档, 综合得分 < 3 → **Level 1**。

---

## 与 Skill 使用边界的一致性

spec-drafter SKILL.md "不使用场景" 明确写: **简单的 typo/格式修复 → Level 1, 直接跳过 A.1**。本请求正是该场景, 因此本 Skill 的产出到此为止 (只给出 Level 判定与推荐动作), 不生成 proposal.md, 也不生成 tasks.md。

## 推荐后续动作

1. 跳过 A.1 (Spec 创建) 与 A.2/A.3 (任务规划 / Agent 分配)。
2. 直接进入 B.1: 用 `branch-manager` 创建修复分支 (如 `fix/login-page-typo`)。
3. B.2 修正文案后, C.1 提交遵循 Conventional Commits, 建议类型 `fix:` (若该 typo 位于纯文档/注释则用 `docs:`), 例如 `fix(login): correct typo on login page`。

## 需要重新判断的情形 (覆盖条件)

以下任一成立时请回到 A.1 重新评估, 或用 `level_override=2` 强制指定:

- 所谓 "typo" 实际是**代码标识符 / i18n key / 路由名**等, 修正后会牵连多个文件或改变运行行为 (此时变更类型不再是纯文本修正)。
- 修正需要同步改动多个模块 (例如前后端共用的文案常量、`shared/` 契约里的字段名) → 满足跨模块条件。
- 修复顺带引入了新文案、新校验或新交互 (即出现 Level 2 功能开发词)。

在没有上述情形的前提下, 本判定为 **Level 1 (Skip)**。
