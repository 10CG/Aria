# spec-drafter A.1 推演: `Add a dark mode feature / 添加深色模式功能`

> 本次为**描述性推演** (descriptive): 只做 A.1 的判断与文稿生成, **未执行 git、未在仓内创建/修改任何文件、未运行脚本**。下面的 proposal 是「待落盘草稿」, 落点路径已给出但尚未写入。

---

## 0. 输入解析 (双语输入处理)

原始需求字符串含一个 `/` 分隔的中英双语对:

| 片段 | 语言 | 语义 |
|------|------|------|
| `Add a dark mode feature` | en | 添加深色模式功能 |
| `添加深色模式功能` | zh | 同上 |

处理判断三条:

1. **这是一个需求, 不是两个**。`/` 在此是「同义翻译对」分隔符而非「并列需求」分隔符 —— 两侧动词 (add / 添加)、名词 (dark mode / 深色模式)、范畴词 (feature / 功能) 逐项对齐, 无一侧携带另一侧没有的信息。因此**不拆成两个 Spec**, 也不把两侧当成 scope 的两半累加。
2. **语义差集为空 → 无信息需要合并**。双语输入的真正风险是「某一侧多说了一句」(例: 中文侧多写「跟随系统」), 那部分只在一种语言里出现的约束最容易在起草时丢失。本例逐项核对后差集为空, 故 What 不需要从中文侧补写。
3. **交付语言 = 英文** (用户显式要求「请生成英文 proposal」)。因此:
   - proposal.md 正文、章节标题、Tasks / Success Criteria **全英文**;
   - feature 目录名取 ASCII kebab-case `dark-mode` (机读 token 一律英文 canonical, 不用中文目录名);
   - 本回复的**叙述层**仍用中文 (工作语言约定: 交付物语言 ≠ 对话语言)。

---

## 1. A.1.0 头脑风暴检查

按流程应先扫 `docs/decisions/technical-*.md` 看有无可预填充的技术决策。本次为描述性推演, 未实际扫描;**假定无相关决策记录**, 对应分支为:

```
建议先运行 brainstorm.technical 讨论技术方案
  [1] 先头脑风暴 (推荐)
  [2] 直接创建 OpenSpec
  [3] 取消
```

用户已明确要 proposal ⇒ 按 **[2] 直接创建**推进。但深色模式有 3 个典型的「早决定省后期返工」的技术分叉, 我把它们显式记在下方「待确认项」而不是在 proposal 里替用户拍板:

- 主题状态机是 2 态 (light/dark) 还是 3 态 (light/dark/follow-system);
- 颜色是否收敛为 semantic token (bg/surface/text/border...), 还是直接给每个组件加一套暗色值;
- 偏好持久化介质 (localStorage / SharedPreferences / 服务端用户配置)。

若用户希望先澄清这三项, 正确顺序是 `brainstorm.technical` → 回到 A.1 由决策记录预填充 Technical Approach 并引用 `DEC-xxx`。

---

## 2. A.1.1 信息提取

| 字段 | 提取结果 | 来源 |
|------|----------|------|
| Feature Name | `dark-mode` (Dark Mode) | 双语对共同名词 |
| Why | 低光环境可读性 / 眼睛疲劳 / 与操作系统主题一致 / 已是现代应用的基线期待 | 由需求语义补全 (输入未给动机) |
| What | 新增深色配色主题 + 主题切换与偏好持久化 | 输入 |
| Deliverables | token 定义 / 主题解析层 / 切换 UI / 持久化 / 组件迁移 / 测试 | 由 What 派生 |
| Constraints | 对比度需达 WCAG AA;不得引入首屏错误主题闪烁 (FOUC);不破坏现有浅色外观 | 由 What 派生 (待用户确认) |
| Framework Constraints | **条件性** —— 需确认技术栈后才能落实(见 proposal 中该节) | A.1.1 可选项 |

> ⚠️ Why / Constraints 属**推断补全**而非原文提取 —— 原始需求只有 8 个词, 未给动机与约束。交互确认时应优先复核这两块。

---

## 3. A.1.2 Level 判断 → **Level 2 (Minimal)**

关键词与评分:

| 因素 | 命中 | 分 | 权重 |
|------|------|----|------|
| 关键词匹配 | `add` / `feature` / `添加` / `功能` → Level 2 触发词组;**无** `refactor / architecture / breaking / migration / 跨模块` 等 Level 3 触发词 | 5 | 40% |
| 文件影响范围 | 单模块 (前端/客户端 UI 层), 不改 API 契约、不动 `shared/` | 4 | 30% |
| 变更类型 | 纯新增 (additive), 非 breaking change | 3 | 20% |
| 历史模式 | 无历史信号, 取中性默认 | 5 | 10% |

`score = 5×0.4 + 4×0.3 + 3×0.2 + 5×0.1 = 4.3` → 落在 `3 ≤ score < 7` ⇒ **Level 2**, 产出物 = `proposal.md` 单文件, **不生成 `tasks.md`**。

**升 Level 3 的可证伪条件** (请在确认时判定, 命中任一即改判):

- 本次要顺带把散落的硬编码颜色重构成设计 token 体系, 且该 token 体系被 2 个及以上模块 (如 web + mobile, 或 `shared/`) 消费 → 跨模块, 升 3;
- 主题偏好需存到后端并进入用户配置 API 契约 → 契约变更, 升 3;
- 现有组件量大到必须分阶段迁移并保持双主题并行 → 迁移型变更, 升 3。

冲突处理留痕: 输入里没有 Level 1 触发词 (`typo/format/config/simple`), 无需走「关键词冲突取高 Level」分支。

---

## 4. A.1.3 模块检测 → **未定, 需确认**

需求文本未出现任何模块指纹词 (无 Flutter/Dart/Widget, 无 Python/FastAPI/API/数据库, 无 Schema/OpenAPI, 无 Skill/规范)。「dark mode」只能定位到「UI 层」这一粗粒度, 无法机械判定是 `mobile` 还是 web 前端。

按错误处理表, 这属于「模块检测失败 → 手动指定 `module` 参数」。我**不猜栈**, 改为在 proposal 的 Key Deliverables 里用 `{ui-module}/` 占位, 并在下方列为待确认项 1。落点路径本身不受影响。

**落点** (Level 2):

```
openspec/changes/dark-mode/proposal.md
```

即**消费方项目自己的** `openspec/changes/`。这里显式点名一个易错点: **不要**写成 `standards/openspec/changes/dark-mode/` —— standards 是共享子模块, 项目自身的功能变更放进去会对所有采用方可见且无人拥有 (Aria 不可协商规则 #5)。只有 standards 仓自身的规范变更才落 standards。
(注: `LEVEL_GUIDE.md` 的示例段仍写着 `standards/openspec/changes/...`, 与 SKILL.md A.1.4 冲突;以 **SKILL.md A.1.4 为准**, 该示例是待勘正的陈旧文本。)

---

## 5. A.1.4 生成的 Spec (草稿, 未落盘)

```
╔══════════════════════════════════════════════════════════╗
║           SPEC DRAFT PREVIEW (Level 2)                   ║
╚══════════════════════════════════════════════════════════╝

Feature: dark-mode
Module: {ui-module}  (待确认: mobile / web-frontend)
Location: openspec/changes/dark-mode/proposal.md
```

```markdown
# Dark Mode

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-04
> **Linked Issue**: `none`

## Why

The product currently ships a single light theme. Users in low-light environments
have no way to reduce screen brightness and glare, and users whose operating
system is set to a dark appearance see the app break visual consistency with the
rest of their desktop or phone. A dark theme is now a baseline expectation for
consumer-facing UI, and it is also an accessibility affordance for users with
light sensitivity.

Adding it now — before the component surface grows further — is cheaper than
retrofitting it later, because every component added in the meantime is one more
component that hard-codes light-only colors.

## What

Add a dark color theme alongside the existing light theme, plus the mechanism
that decides which theme is active and remembers the user's choice.

Scope:

- A semantic color layer (background, surface, text, muted text, border,
  accent, danger, ...) with a light value and a dark value for each token.
- Theme resolution: explicit user preference wins; when the user has expressed
  no preference, follow the operating-system setting.
- A user-visible control to switch theme, and persistence of that choice across
  restarts / reloads.
- Migration of existing components from hard-coded colors to the semantic tokens.

Out of scope (this change):

- Per-component theming or user-authored custom themes.
- High-contrast / accessibility themes beyond the two standard ones.
- Server-side storage of the preference (local persistence only — see Impact).

### Key Deliverables

- `{ui-module}/theme/tokens.*` — semantic color tokens, light and dark values
- `{ui-module}/theme/theme-provider.*` — theme resolution + OS-preference listener
- `{ui-module}/components/theme-toggle.*` — user-facing switch control
- `{ui-module}/theme/persistence.*` — read/write of the stored preference
- Component migration diff — replaces hard-coded color literals with tokens
- `{ui-module}/theme/__tests__/` — contrast and resolution tests
- Documentation update covering how to add a new color token

## Impact

| Type | Description |
|------|-------------|
| **Positive** | Usable in low-light conditions; visual consistency with the OS appearance setting; improved accessibility for light-sensitive users |
| **Positive** | Establishes a semantic color layer, so future components inherit theming for free |
| **Scope** | Touches every component that currently hard-codes a color value — broad but shallow diff |
| **Risk** | Missed components render light-on-dark and become unreadable — mitigated by a lint/grep gate that fails on raw color literals in migrated paths |
| **Risk** | Flash of the wrong theme on first paint when the stored preference is read after the first render — mitigated by resolving the theme before paint |
| **Risk** | Contrast regressions in the dark palette (dark grey on dark grey) — mitigated by an automated contrast check over the token pairs |
| **Neutral** | No API contract change; no data model change; light-theme appearance must stay pixel-identical |

## Framework Constraints

> Applies only if the UI module is built on a web framework. Delete this section
> if the target is a native / Flutter client.

- Theme must be resolved before first paint (inline script or SSR-side cookie
  read); reading the stored preference in a client-side effect causes a
  hydration mismatch plus a visible flash.
- Server-rendered markup must not branch on a client-only value (`localStorage`,
  `window.matchMedia`) during render.
- If the framework exposes a color-scheme/theme-color metadata field, it must be
  updated together with the theme, and only through the framework's documented
  metadata surface.

## Tasks

- [ ] Inventory current color usage and define the semantic token set
- [ ] Define light and dark values for every token
- [ ] Implement theme resolution (explicit preference, else OS setting)
- [ ] Persist and restore the user's preference
- [ ] Add the theme toggle control to the UI
- [ ] Migrate existing components from hard-coded colors to tokens
- [ ] Add contrast and theme-resolution tests
- [ ] Document how to add a token and how to theme a new component

## Success Criteria

- [ ] Every text/background token pair in the dark palette meets WCAG 2.1 AA
      (>= 4.5:1 for body text, >= 3:1 for large text and UI boundaries),
      verified by an automated check over the token set
- [ ] Theme resolution is correct for all three states: explicit light,
      explicit dark, and no-preference (follows the OS setting, and reacts when
      the OS setting changes while the app is open)
- [ ] The chosen theme survives a restart / full reload
- [ ] No flash of the wrong theme on first paint (verified on a cold load)
- [ ] Zero raw color literals remain in the migrated component paths
      (enforced by lint rule or grep gate in CI)
- [ ] Light theme rendering is unchanged — existing UI snapshots pass unmodified
- [ ] Test coverage for the theme module >= the project's current baseline
```

---

## 6. A.1.5 待确认项 (交互确认)

落盘前有 4 项需要用户拍板, 我不代填:

**【1】模块 / 技术栈** — `mobile` (Flutter/Dart) 还是 web 前端? 决定 `{ui-module}/` 占位的实际路径、文件扩展名, 以及 `## Framework Constraints` 一节是保留还是整节删除。

**【2】Linked Issue** — 草稿里按规范逐字写了 `` `none` ``。这个哨兵的正确含义是「**已核实**无关联 issue」, 而我并未核实。若实际存在对应 issue, 请替换为 `` `<org>/<repo>#<n>` `` (例 `` `10CG/Aria#174` ``);多个写在同一个 code span 内用 `, ` 分隔。注意 `N/A` / `TBD` / `-` / 留空 / 删行都不合规, markdown 链接形也会被判 `NO_TOKEN`。

**【3】主题状态机** — 2 态 (light/dark) 还是 3 态 (含 follow-system)? 草稿按 3 态写 (Success Criteria 第 2 条含 no-preference 分支)。改成 2 态需同步收窄该条与 What。

**【4】Level 是否维持 2** — 若本次要连带做跨模块 token 体系重构, 或偏好要进后端用户配置 API, 请改判 Level 3, 届时需追加 `tasks.md`。

另: Why 与 Constraints 是我从 8 个词的需求**推断补全**的, 不是原文提取, 请重点复核这两块是否符合真实动机。

---

## 7. A.1.6 验证提示

落盘后建议运行:

```
openspec validate dark-mode --strict
```

---

## 8. 下一步

1. 回答上面 4 项待确认 → 我据此定稿并写入 `openspec/changes/dark-mode/proposal.md` (本次未写);
2. 之后进入 **A.2 任务规划** (`task-planner`), 由它产出 `detailed-tasks.yaml` (工时/文件路径/Agent 分配都在 A.2/A.3 定, proposal 的 `## Tasks` 保持粗粒度不含这些字段);
3. 再进入 **B.1 分支创建**。
