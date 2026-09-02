# Spec Level 判断: 「修复登录页面一个 typo」

```
═══════════════════════════════════════════════════════════
  LEVEL 1 DETECTED - SKIP SPEC
═══════════════════════════════════════════════════════════

此需求为简单修复，建议直接跳过 A.1：
- 类型: 文档格式/Typo 修复
- 影响: 单文件
- 风险: 极低

📋 推荐操作:
   直接进入 B.1 (分支创建) 开始开发
```

## 判断依据 (按 LEVEL_GUIDE.md 决策流程 + SKILL.md A.1.2 三项分析)

1. **决策流程图 Q1「是否简单修复/配置/文档格式?」→ YES**。请求原文「修复登录页面一个 typo」: `typo` 是 Level 1 高置信度触发词; 「修复」= fix; 「一个」是上下文限定词 (just/only 语义, 明示只改一处)。Q1 为 YES 即终止, 不进入 Q2。
2. **关键词冲突检查**: 无 Level 3 词 (架构 / 重构 / 跨模块 / breaking / migration), 无 Level 2 词 (feature / add / implement / 新建 / 组件)。「登录页面」只描述变更的**位置**, 不是变更**类型**, 不构成冲突; 「冲突时取更高 Level」规则不触发。
3. **文件影响范围**: 单模块 (登录页面 UI, 归 mobile / frontend), 预期单文件文本改动; 不改 `shared/`, 不改 API 契约, 不涉及第二个模块 → 不触发「跨模块 → 自动提升 Level 3」。
4. **变更类型**: 非功能性文本修正, 无行为变化, 非 breaking change。
5. **综合评分**: 关键词 (Level 1 触发词)、范围 (单文件)、变更类型 (minor fix) 三项均处最低档, score < 3 → Level 1。与 LEVEL_GUIDE.md 示例 3「Fix typo in README → Level 1」同形, 也对应 SKILL.md「不使用场景: 简单的 typo/格式修复 → Level 1, 直接跳过 A.1」。

## 附注

- Level 1 跳过的是 A.1 的 Spec 产出: 不生成 proposal.md, 不需要 `openspec validate`, A.1.0 头脑风暴检查亦不适用。提交本身仍须遵守 Conventional Commits (例: `fix(login): 修正登录页面 typo`)。
- **重判条件**: 若动手时发现这个「typo」实际落在跨模块共享物上 (如 `shared/` 里的 i18n key / API 契约字符串), 或修正会改变行为 (路由路径、字段名), 它就不再是纯文本修复 —— 回到 Q2 重判: 跨模块直接 Level 3, 否则 Level 2。
- 如自动判断与实际不符, 可用 `level_override=1|2|3` 强制指定。
