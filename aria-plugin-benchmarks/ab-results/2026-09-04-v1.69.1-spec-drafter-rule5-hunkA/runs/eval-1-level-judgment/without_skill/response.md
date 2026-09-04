# 规范等级判断: "修复登录页面一个 typo"

> 依据: spec-drafter SKILL.md (v2.2.0) A.1.2 Level 判断 + LEVEL_GUIDE.md (v1.0.0)
> 形式: 描述性推演 (不落盘任何仓库文件, 不执行 git/脚本)

---

## 结论

```
═══════════════════════════════════════════════════════════
  LEVEL 1 DETECTED - SKIP SPEC
═══════════════════════════════════════════════════════════

此需求为简单修复，建议直接跳过 A.1：
- 类型: 文档格式/Typo 修复 (登录页面文案拼写)
- 影响: 单文件 (登录页 UI 文案/模板)
- 风险: 极低

推荐操作:
   直接进入 B.1 (分支创建) 开始开发
```

**判定: Level 1 (Skip) —— 不产出 proposal.md, 不产出 tasks.md。**

---

## 推演过程 (按 A.1.2 三条判据)

### 【1】关键词匹配

LEVEL_GUIDE.md「Level 1 触发词 (简单修复)」高置信度触发词列表中直接命中:

| 命中项 | 出处 | 说明 |
|--------|------|------|
| `typo` / `fix typo` | Level 1 高置信度触发词 | 用户请求逐字含「typo」, 且动词为「修复」 |

反向核对另外两级触发词, 均**无**命中:

- Level 2 触发词 (feature / add / implement / new / Skill / component / improve / extend / optimize): 「修复」不属功能开发词或增强改进词, 「登录页面」只是定位而非新增能力。
- Level 3 触发词 (architecture / refactor / redesign / breaking / migration / 跨模块 / system-wide / core): 全无命中。

按 LEVEL_GUIDE.md「关键词冲突」优先级规则 (Level 3 > Level 2 > Level 1) 检查: 本例**不存在冲突**, 无需升级仲裁。对比该文档给的冲突范例 "Add simple authentication feature" (simple 暗示 L1 但 authentication feature 暗示 L2 ⇒ 取高者 L2), 本例请求里没有任何功能性名词与 typo 竞争。

### 【2】文件影响范围分析 (跨模块检测)

```yaml
需求描述: 修复登录页面一个 typo
模块检测 (A.1.3 / LEVEL_GUIDE.md 模块映射):
  命中: 单一 UI 模块 (若为 Flutter/Dart 前端 → mobile: mobile/**;
        若为 Web 前端 → 对应前端模块; 若文案在后端模板 → backend/**)
  跨模块条件核对:
    - 涉及 2 个及以上模块?          否 (一个页面的一处文案)
    - 修改 shared/ 目录?            否
    - 需要 API 契约变更?            否
    - 影响多个子模块?               否
  ⇒ 不触发「跨模块 → 自动提升 Level 3」
影响面: 单文件, 甚至单行 (一个拼写错误)
```

注: 模块具体归属不影响本次 Level 判定 —— 无论落在 mobile 还是 backend, 都是**单模块单文件**, 结论一致。因此不必为了定级而先做模块消歧。

### 【3】变更类型识别 (breaking change)

- 变更类型: 文案/拼写更正, 属**非功能性文本修复**。
- 无接口变更、无数据结构变更、无行为语义变更 ⇒ 非 breaking change。
- 无向后兼容风险。

### 综合评分 (LEVEL_GUIDE.md 评分机制对照)

```yaml
keyword_score:      极低 (纯 Level 1 触发词, 无 L2/L3 词)
scope_score:        极低 (单模块单文件)
change_type_score:  极低 (非 breaking, 非功能变更)
history_score:      低   (typo 修复是历史上高频的 Level 1 常规模式)

score = 0.4*低 + 0.3*低 + 0.2*低 + 0.1*低  ⇒  score < 3
阈值判定: score < 3 → Level 1
```

三条判据 + 综合评分四者**一致指向 Level 1**, 无「不确定 → 默认 Level 2」的兜底触发条件。

---

## 处置建议 (Level 1 后续动作)

1. **跳过 A.1**: 不创建 proposal.md, 不创建 tasks.md, 不需要 `openspec validate`。SKILL.md「不使用场景」首条即写明: 简单的 typo/格式修复 → Level 1, 直接跳过 A.1。
2. **直接进入 B.1 (分支创建)**: 建议分支名如 `fix/login-page-typo`。
3. **B.2 验证**: 改动虽小, 仍应跑一次相关页面的现有测试/构建 (确认没有把文案键名、i18n key 或模板变量一起改坏)。
4. **C.1 提交**: 遵循 Conventional Commits, 例如 `fix(login): 修正登录页文案拼写错误`。
5. Level 1 跳过的是 **Spec 文档**, 不是十步循环本身 —— B/C/D 各步照常。

---

## 需要升级 Level 的例外情形 (判定前值得快速确认)

以下任一成立时, 该请求就**不再是**教科书式 typo, 应重判为 Level 2 (个别情形 Level 3):

- **拼错的是标识符而非展示文案**: 例如 i18n key、CSS class、表单 field name、事件埋点名、API 参数名。改它会波及调用方 ⇒ 属功能性变更, 可能跨模块 ⇒ 按跨模块规则升 Level 2/3。
- **同一处文案在多语言资源/多端各有副本**: 需要同步 mobile + web + 后端模板 ⇒ 触发「涉及 2 个及以上模块」⇒ Level 3。
- **文案属对外契约或合规文本**: 如登录页的服务条款/隐私声明措辞, 变更需法务或产品确认 ⇒ 至少 Level 2 留痕。
- **「一个 typo」实为一批**: 若实际是全站文案批量校对 ⇒ 影响面从单文件放大, 按 Level 2 处理。

若上述均不成立 (最常见的情况: 登录页某句提示语少写/多写一个字母), 维持 **Level 1**。

---

## 若被升级为 Level 2 时的产出位置 (仅备查)

按本 Skill A.1.4 的产出路径约定:

```
Level 2: standards/openspec/changes/{feature}/proposal.md
Level 3: proposal.md + tasks.md
```

并且 proposal.md 头部 blockquote 必须含 `Linked Issue` 行 (顺序 `Level` → `Status` → `Created` → `Linked Issue`), 值写 inline code span 形 `` `<org>/<repo>#<n>` ``; 确无关联时逐字写 `` `none` ``, 不留空、不删行, `N/A`/`TBD`/`-` 均判不合规。

本例判为 Level 1, 以上不适用。

---

## 一句话回答

「修复登录页面一个 typo」命中 Level 1 高置信度触发词 `typo`, 单模块单文件、非 breaking、综合评分 < 3, 判为 **Level 1 (Skip)**: 不写 Spec, 直接进入 B.1 建分支修复并按 Conventional Commits 提交; 仅当拼错的是标识符/i18n key、或需跨端多副本同步时才升级为 Level 2/3。
