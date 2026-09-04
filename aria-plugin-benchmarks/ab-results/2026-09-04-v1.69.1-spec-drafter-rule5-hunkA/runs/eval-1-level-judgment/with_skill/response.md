# Spec 等级判断: "修复登录页面一个 typo"

## 结论

**Level 1 (Skip) —— 不创建 Spec, 跳过 A.1, 直接进入 B.1。**

这条判断直接落在 spec-drafter 自己写明的「不使用场景」上: SKILL.md「我应该使用这个 Skill 吗？」一节把「简单的 typo/格式修复 → Level 1，直接跳过 A.1」列为**不使用本 Skill** 的第一条。也就是说, 本次调用的正确产出不是一份 proposal.md, 而是一个「不需要 proposal.md」的判定 + 移交动作。

---

## 判断依据 (按 A.1.2 三步推演)

### 1. 关键词匹配

| 命中项 | 出处 | 权重方向 |
|--------|------|----------|
| `typo` | LEVEL_GUIDE.md「Level 1 触发词 · 高置信度触发词」首条 (`typo, fix typo`) | → Level 1 |
| `修复` / `fix` | 同上 (`minor fix`) | → Level 1 |
| 数量限定「一个」 | 上下文限定词 (`"just", "only"`, `"small"`, `"tiny"`) 的中文等价 | → Level 1 (强化) |

**反向核对 (有没有更高级别的触发词?)**:

- Level 2 触发词表 (feature/功能, add/implement/添加/实现, new/新建/创建, Skill, component/组件, improve/改进, extend/扩展, optimize) —— **零命中**。请求里的动词是「修复」, 不在 Level 2 的功能开发词/增强改进词任一子表中。
- Level 3 触发词表 (architecture/架构, refactor/重构, redesign, breaking, migration/迁移, cross-module/跨模块, integration/集成, system-wide, global, core) —— **零命中**。

因此 LEVEL_GUIDE「边界情况处理 · 关键词冲突: 优先级 Level 3 > Level 2 > Level 1」这条**不被触发** —— 冲突消解规则只在两级以上同时命中时才生效, 本例只有单级命中, 无需上调。这点值得点明: 常见的误判是看到「登录页面」这类业务名词就以为沾了 authentication 而联想到 Level 2, 但 LEVEL_GUIDE 的示例 `"Add simple authentication feature"` 之所以升到 Level 2, 靠的是 **`feature` 这个功能开发词**, 不是 `authentication` 这个领域名词。本例没有那个动词。

### 2. 文件影响范围 (模块检测 + 跨模块判断)

- **模块**: 「登录页面」指向 UI 层。按 LEVEL_GUIDE 模块映射, 若是 Flutter/Dart 页面则归 `mobile` (关键词 UI/Widget/移动端), 若是 Web 前端则落在项目自身的前端目录 —— **具体归属需在 B.1 前扫一眼实际路径确认, 但无论落在哪一边, 都是单模块。**
- **跨模块条件逐条否定** (满足任一即升 Level 3):
  1. 涉及 2 个及以上模块 —— 否 (单页面文案)。
  2. 修改 `shared/` 目录 —— 否。
  3. 需要 API 契约变更 —— 否 (typo 不改契约)。
  4. 影响多个子模块 —— 否。
- **预期改动面**: 单文件, 大概率单行 (一处展示文案 / 一处注释)。

### 3. 变更类型识别

- 类型: 文案/文档格式修复, 非行为变更。
- Breaking change: 否 —— 不改函数签名、不改路由、不改数据结构。
- 风险: 极低; 无需 state-scanner 上下文增强 (SKILL.md「上下文增强」是为填充 Impact.Risk / Success Criteria 服务的, Level 1 无这两节, 拉取上下文是空转)。

### 4. 综合评分推演

LEVEL_GUIDE 给出的公式:

```
score = keyword_score*0.4 + scope_score*0.3 + change_type_score*0.2 + history_score*0.1
阈值: score < 3 → Level 1 | 3 <= score < 7 → Level 2 | score >= 7 → Level 3
```

**说明一处规格空白**: LEVEL_GUIDE 未定义四个分因子各自的量表 (只定义了加权后的阈值落在 0–10 区间), 所以这里按「四因子与总分同尺度 (1–10)」代入 —— 这是推演假设, 不是规范原文。

| 因子 | 取值 | 理由 |
|------|------|------|
| keyword_score | 1 | 命中 Level 1 最高置信度词, 且无更高级别词竞争 |
| scope_score | 1 | 单文件、单模块、不触 `shared/` |
| change_type_score | 1 | 纯文案, 非 breaking, 无行为变更 |
| history_score | 1 | 无相似历史高成本先例可引 |

score = 0.4 + 0.3 + 0.2 + 0.1 = **1.0**, 远低于 3 → **Level 1**。判定与关键词直判一致, 两条路径互相印证, 不落入「Level 判断不确定 → 默认 Level 2」的兜底分支。

---

## 本次判定的标准输出

```
═══════════════════════════════════════════════════════════
  LEVEL 1 DETECTED - SKIP SPEC
═══════════════════════════════════════════════════════════

此需求为简单修复，建议直接跳过 A.1：
- 类型: 文档格式/Typo 修复 (登录页面文案)
- 影响: 单文件
- 风险: 极低

📋 推荐操作:
   直接进入 B.1 (分支创建) 开始开发
```

---

## 因此**不**产出的东西 (逐条对应, 避免过度交付)

| 产出物 | 本次是否产出 | 依据 |
|--------|-------------|------|
| `openspec/changes/<feature>/proposal.md` | 否 | Level 1 产出物 = 「无 Spec」(三级策略表) |
| `tasks.md` | 否 | 仅 Level 3 产出 |
| 头部 `Linked Issue` 字段 | 不适用 | 该要求的宿主是 Level 2 / Level 3 的 proposal.md; 无 proposal 即无该字段的落点 |
| `openspec validate <feature> --strict` | 不适用 | 没有生成 Spec 目录可供校验 |
| A.1.0 头脑风暴检查 (`docs/decisions/technical-*.md`) | 跳过 | 该检查服务于 Spec 预填充; 无 Spec 则无预填充对象 |
| 框架约定段 (Framework Constraints, Aria #95) | 跳过 | 同上, 它是 proposal 里的一段, 供 post_spec/post_impl 审计对照 |
| state-scanner 上下文增强 | 跳过 | 无 Impact.Risk / Success Criteria 可填 |

顺带记一条路径纪律 (虽然本次不落盘, 但它是最容易在 typo 类小改动上被顺手违反的一条): 一旦后续复核把等级抬到 Level 2/3, proposal 必须落到**消费方项目自己的** `openspec/changes/`, 不能写进 `standards/openspec/changes/` —— standards 是共享子模块, 项目变更写进去会对所有采用方可见且无人拥有 (Aria 不可协商规则 #5)。只有 standards 自身的规范变更才落 standards 仓。

---

## 复核问题 (改动落地前值得花 30 秒确认, 任一为「是」则重判等级)

Level 1 的正当性建立在「这个 typo 只是给人看的字符串」上。以下三种情况下, 同一个词的拼写错误**不再是 Level 1**, 因为它改的是被机器消费的 token, 而不是展示文案:

1. **拼错的字符串是否被机器解析?** —— 例如它其实是一个 i18n key、一个表单 `name` 属性、一个 CSS class、一个路由路径、一个事件名或枚举值。改它等于改契约, 会静默打断引用方; 此时按「需要 API 契约变更」升到 Level 3, 或至少 Level 2 并做全仓引用点 grep。
2. **同一处拼写是否在多处重复?** —— 若这个 typo 是从某个共享常量/翻译文件扩散出去的, 那修的就不是「一个 typo」而是一处源头 + N 个引用点, 影响面跨模块, 判定输入 (「单文件」) 本身已不成立。
3. **它是否出现在对外可见的合规/法务文案里?** —— 登录页常承载条款、隐私提示、品牌名。这类文案的修改可能需要留痕而非单纯 typo fix。

三条都为「否」 → 维持 Level 1, 按上面的推荐操作走 B.1。任一为「是」→ 回到 A.1.2 用新的影响范围重跑判断, 别沿用本次结论。

---

## 移交建议 (下一步)

1. 进入 **B.1 分支创建** (branch-manager), 分支名建议 `fix/login-page-typo`。
2. B.2 改动后照常走 Conventional Commits (Aria 不可协商规则 #4), 建议 `fix(login): 修正登录页面文案拼写`; typo 修复通常对应 PATCH 级。
3. Level 1 跳过的是 **A.1 (Spec 创建)**, **不是** Phase A 本身 —— 规则 #2「十步循环不能跳过 Phase A」要求的「先理解现状再行动」仍然成立, 上面那三条复核问题就是本次 Phase A 的最小履行形态。
