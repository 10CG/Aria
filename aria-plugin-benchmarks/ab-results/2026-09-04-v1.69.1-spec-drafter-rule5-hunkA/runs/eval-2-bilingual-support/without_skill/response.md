# spec-drafter A.1 推演 — Dark Mode (双语输入)

> 产出形式: **描述性推演** (不落盘、不建分支、不跑脚本)。下面是「若执行 A.1 会生成什么」的完整预览。

---

## 0. 输入解析 (双语)

| 项 | 值 |
|----|----|
| 原始输入 | `Add a dark mode feature / 添加深色模式功能` |
| 结构判定 | **同一需求的中英双语表述**, 不是两条独立需求 (`/` 是语言分隔符, 不是需求分隔符) |
| 英文侧语义 | Add a dark mode feature → 新增功能 (add / feature) |
| 中文侧语义 | 添加深色模式功能 → 新增功能 (添加 / 功能) |
| 语义一致性 | ✅ 一致 —— 「dark mode」≡「深色模式」, 「feature」≡「功能」; 两侧都不含架构级 / 修复级信号 |
| 双侧合并意图 | 为应用增加深色主题 (dark theme), 用户可在浅色 / 深色之间切换, 并可跟随系统外观 |
| **产出语言** | **English** (用户显式要求「请生成英文 proposal」) |
| 叙述语言 | 中文 (本推演的解释部分); proposal 正文全英文, 不留中文残句 |

> 双语输入的取值原则: 两侧语义一致时取**并集**填充 Why/What (避免只读一侧丢信息); 若两侧冲突则必须回问用户, 本例无冲突。

---

## 1. A.1.0 头脑风暴检查

- 扫描 `docs/decisions/technical-*.md` 是否有与 dark mode / theming 相关的技术决策记录。
- 本次输入未引用任何决策记录, 推演按「无 decision-log」分支处理:

```
建议先运行 brainstorm.technical 讨论技术方案
  [1] 先头脑风暴 (推荐) —— 主题建议: 主题 token 方案 / 持久化位置 / 跟随系统的实现方式
  [2] 直接创建 OpenSpec (本次推演走这条)
  [3] 取消
```

- 若后续补做 brainstorm, proposal 头部需追加 `> **决策来源**: [DEC-00x](../../docs/decisions/technical-00x.md)` 并回填 Constraints / Technical Approach。

---

## 2. A.1.1 信息提取

| 字段 | 提取结果 |
|------|----------|
| Feature Name | `dark-mode` (slug) / `Dark Mode` (标题) |
| Why | 长时间 / 低光环境下的可读性与眼睛负担; 深色主题已是主流应用的基线预期; 需尊重系统级外观偏好 |
| What | 主题 token 体系 + 主题切换 (Light / Dark / Follow System) + 偏好持久化 + 全量界面适配 |
| Deliverables | 主题 token 定义、主题 Provider/Context、设置项 UI、持久化读写、对比度与 UI 回归测试 |
| Constraints | 不引入破坏性 API 变更; 首屏不得出现浅色闪白 (FOUC); 深色配色须满足 WCAG AA 对比度 |
| Framework Constraints (Aria #95, 可选) | ⚠️ 本次输入**未指明技术栈** —— 若目标是 framework 项目 (Next.js / Astro / SvelteKit / Vue / Remix 等), 此节须补: SSR/RSC 下的首屏主题注入 (`use client` 边界 / 预渲染前的内联脚本) 与 metadata `color-scheme` 白名单。非 framework 项目跳过。 |

---

## 3. A.1.2 Level 判断

```yaml
关键词匹配 (40%):
  英文侧: "Add" / "feature"        → Level 2 功能开发词
  中文侧: "添加" / "功能"           → Level 2 功能开发词
  Level 1 触发词: 无 (无 typo/format/readme/minor fix)
  Level 3 触发词: 无 (无 refactor/architecture/breaking/migration/跨模块)

文件影响范围 (30%):
  单一关注面 = UI 主题层 (样式 token + 主题状态 + 设置项)
  未触及 shared/ 契约, 无 API 契约变更 → 非跨模块

变更类型 (20%):
  纯增量新增, 向后兼容 (默认保持现有浅色行为)

历史模式 (10%):
  同形状先例: "Implement offline cache" / "Add user authentication feature" → 均为 Level 2

结论: Level 2 (Minimal) —— 产出 proposal.md, 不产出 tasks.md
```

**判定说明**: 关键词冲突检查通过 (无 Level 1 / Level 3 触发词并存)。深色模式虽然「触达所有界面」, 但那是**广度**而非**架构深度** —— 没有模块边界重划、没有 breaking change, 因此不升 Level 3。若后续核对发现需要同时改 shared/ 设计 token 契约并影响 2 个以上模块, 则按跨模块规则**自动升级为 Level 3** (proposal.md + tasks.md), 这是本判定唯一的翻转条件。

---

## 4. A.1.3 模块检测

| 候选 | 匹配信号 | 结论 |
|------|----------|------|
| mobile | UI / 主题 / Widget / 移动端 | 若为 Flutter/移动端项目则命中 |
| frontend/web | 样式 / CSS 变量 / prefers-color-scheme | 若为 Web 项目则命中 |
| backend | 无 | 未命中 |
| shared | 仅当主题 token 进共享契约层才命中 | 未命中 (按当前信息) |

⚠️ **模块检测不确定**: 输入未给出项目/技术栈线索。按错误处理表, 交互模式下应请用户手动指定 `module`; 本推演以 **UI 客户端单模块 (`mobile` 或 `frontend`)** 为假设继续, 该假设写入下方 Open Questions, 不静默定案。

---

## 5. A.1.4 生成的 Spec (Level 2 预览)

```
╔══════════════════════════════════════════════════════════╗
║           SPEC DRAFT PREVIEW (Level 2)                   ║
╚══════════════════════════════════════════════════════════╝

Feature: dark-mode
Module: mobile (assumed — pending user confirmation)
Location: standards/openspec/changes/dark-mode/proposal.md
```

### proposal.md (正文, English)

```markdown
# Dark Mode

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-04
> **Linked Issue**: `none`

## Why

Users spend long sessions in the app, including in low-light environments, where a
permanently light interface causes eye strain and drains battery on OLED displays.
A dark theme is now a baseline expectation: operating systems expose a system-wide
appearance preference, and an app that ignores it feels out of place and forces the
user to leave the app to work around it.

Today the app ships a single light theme with hard-coded colors, so there is no way
for a user to opt into a darker surface, and no way for the app to honor the system
appearance setting.

## What

Introduce a first-class theming layer with a dark variant, plus a user-facing control
to choose between Light, Dark, and Follow System.

Scope:

1. **Theme tokens** — Replace hard-coded colors with a semantic token set (surface,
   background, text primary/secondary, border, accent, error, overlay) defined once
   per theme, so adding a theme never requires touching individual components again.
2. **Dark palette** — A dark token set that meets WCAG AA contrast (>= 4.5:1 for body
   text, >= 3:1 for large text and meaningful UI boundaries).
3. **Theme resolution** — A single source of truth that resolves the effective theme
   from the user preference (`light` / `dark` / `system`) and, when `system`, from the
   OS appearance signal, reacting live when the OS setting changes.
4. **Persistence** — The user preference survives restart; the default for a new
   install is `system`.
5. **Settings UI** — A three-option control in Settings (Light / Dark / Follow System)
   that applies immediately, with no restart and no full-screen reload.
6. **Surface coverage** — All existing screens, dialogs, empty states, charts, and
   status/error surfaces render correctly under the dark palette, including any
   images or icons that assume a light background.

Out of scope: any redesign of layout or information architecture; per-screen or
scheduled ("sunset to sunrise") theming; user-authored custom themes.

### Key Deliverables

- Theme token definitions (light + dark palettes) in the styling layer
- Theme provider / controller exposing the resolved theme and the user preference
- Persistence adapter for the theme preference (local key-value storage)
- Settings screen entry with the three-option theme selector
- Migration of hard-coded colors in existing components to semantic tokens
- Contrast audit checklist and UI regression tests covering both themes

## Impact

| Type | Description |
|------|-------------|
| **Positive** | Better readability in low light; respects the OS appearance preference; the token layer makes any future theme (e.g. high contrast) a data change rather than a code change |
| **Neutral** | Default behavior is unchanged for existing users whose system appearance is light |
| **Risk** | Wide surface area — every screen must be re-checked; hard-coded colors may be missed and only surface as unreadable text in dark mode |
| **Risk** | First-paint flash of the light theme (FOUC) if the stored preference is read after the first render |
| **Risk** | Asset debt — logos, illustrations, and icons baked for a light background may need dark variants |

## Constraints

- Non-breaking: existing public APIs and component signatures stay source-compatible.
- No flash of the wrong theme on cold start; the resolved theme must be known before
  the first meaningful paint.
- Dark palette must pass WCAG AA contrast for text and essential UI boundaries.
- No new runtime dependency solely for theming.

## Tasks

- [ ] Define the semantic token set and the light palette baseline
- [ ] Author the dark palette and verify it against the contrast rules
- [ ] Implement the theme provider with `light` / `dark` / `system` resolution
- [ ] Persist and restore the theme preference across restarts
- [ ] Add the theme selector to the Settings screen
- [ ] Migrate hard-coded colors in existing screens and components to tokens
- [ ] Handle assets that assume a light background
- [ ] Add regression tests and a per-screen visual check for both themes

## Success Criteria

- [ ] A user can switch between Light, Dark, and Follow System, and the change applies
      immediately without a restart
- [ ] The chosen preference survives an app restart; a fresh install defaults to
      Follow System
- [ ] With Follow System selected, changing the OS appearance updates the app live
- [ ] Every screen listed in the surface inventory renders legibly in dark mode, with
      zero remaining hard-coded colors detected by the token lint/grep check
- [ ] All dark-mode text and essential UI boundaries meet WCAG AA contrast
- [ ] No flash of the light theme on cold start when Dark is the resolved theme
- [ ] Test coverage does not regress against the current project baseline
```

### 头部字段自检 (机械 check 对照)

| 规则 | 本稿取值 | 判定 |
|------|----------|------|
| 头部字段顺序 `Level` → `Status` → `Created` → `Linked Issue` | 一致 | ✅ |
| `Linked Issue` 行必填, 不删行 | 已写 | ✅ |
| 无关联时逐字写 `` `none` `` (不用 `N/A` / `TBD` / `-` / 留空) | 输入未给任何 issue 号 ⇒ 取 `` `none` `` | ✅ |
| 值为 inline code span 形, 非 markdown 链接 | `` `none` `` | ✅ |
| 行首无空白, `>` 后恰一个空格, 字段名两侧各两个星号, ASCII 冒号 | 一致 | ✅ |
| 新写用英文 canonical (不写中文 alias `关联 Issue`) | 用 `Linked Issue` | ✅ |

> 说明: 用户的提示词里没有出现任何 tracking issue (无 `#n`、无仓库名), 所以这里**不是「先留占位符」**, 而是按「无关联 (已核实)」写死 `none`; 若之后建了 issue, 再改成 `` `<org>/<repo>#<n>` `` 形。

---

## 6. A.1.5 交互确认 / Open Questions

落盘前需要用户确认的点 (逐章节确认: Level → Why → What → Deliverables → Impact → Tasks → Success Criteria):

1. **目标模块 / 技术栈** —— mobile (Flutter) 还是 Web 前端? 这决定 token 载体 (ThemeData vs CSS 变量)、持久化 API, 以及是否需要补 Framework Constraints 一节。
2. **是否要 Follow System 档** —— 本稿默认三档 (Light / Dark / Follow System) 且新装默认跟随系统; 若产品只想要两档开关, What / Tasks / Success Criteria 三处要同步收窄。
3. **Level 2 是否够** —— 若主题 token 要进 `shared/` 契约并被 2 个以上模块消费, 按跨模块规则应升 Level 3 (补 tasks.md)。
4. **Linked Issue** —— 若实际已有跟踪 issue, 把 `` `none` `` 换成 `` `<org>/<repo>#<n>` `` 形。
5. **是否先跑 brainstorm.technical** —— 无 decision-log 时推荐先跑, 再回填技术方案与约束。

---

## 7. A.1.6 验证提示

```
建议运行 openspec validate dark-mode --strict 验证格式
```

**下一步**: 确认以上内容 → 落盘 proposal.md → 进入 A.2 (task-planner 任务规划)。

---

## 附: 本次推演的关键判断小结

| 问题 | 结论 |
|------|------|
| 双语输入是几条需求? | 1 条 (中英同义表述, 取语义并集) |
| proposal 用什么语言? | 全英文 (用户显式指定); 叙述用中文 |
| Level? | Level 2 (Minimal), 仅 proposal.md |
| Linked Issue? | `` `none` `` (输入未提供任何 issue) |
| 落盘了吗? | 否 —— 描述性推演, 未创建 / 修改任何文件 |
