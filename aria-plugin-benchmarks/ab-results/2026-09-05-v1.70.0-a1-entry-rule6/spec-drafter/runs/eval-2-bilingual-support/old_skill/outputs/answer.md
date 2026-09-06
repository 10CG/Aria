先说明我怎么读这条输入: `Add a dark mode feature / 添加深色模式功能` 是**同一个需求的中英两种表述**, 不是两件事, 所以只起一份 Spec; 按你的指示, proposal 正文全部用英文, 我这边的说明用中文。

**A.1.0 头脑风暴检查**: 扫了 `docs/decisions/`, 没有与 dark mode / 深色模式相关的 technical decision-log。按流程这里应该先问一句:

- 【1】先跑 `brainstorm.technical` 讨论技术方案 (推荐: 主题分发机制、token 命名、是否跟随系统这几项还没有决策记录)
- 【2】直接起 proposal
- 【3】取消

你已经明确要 proposal, 所以我按【2】直接起草, 但把没有决策记录这件事记在这里 —— 下面「待你确认」里的开放问题, 本来是 brainstorm 该收敛掉的。

**A.1.2 Level 判断**: **Level 2 (Minimal)**, 只出 `proposal.md`。

| 判据 | 命中 | 结论 |
|------|------|------|
| 关键词 | `add` / `feature` / `添加` / `功能` → 功能开发词 | Level 2 |
| 架构级词 | 无 (refactor / breaking / migration / 跨模块 均未出现) | 不升 Level 3 |
| 影响范围 | 单模块 UI + 一层 color token | 单模块 |

**升级条件** (命中任一就改判 Level 3, 需要你确认): 深色模式要同时落到 mobile + web 两端并共用 `shared/` 的设计 token; 或者 token 层重构会改动公共契约 / 造成 breaking change。

**A.1.3 模块检测**: 关键词 `dark mode` / UI / 主题 指向前端 UI 模块, 但需求里没有点名端 (mobile 还是 web), 我按单端 UI 起草。**如果是双端共享 token, 请告诉我, 我改判 Level 3 并补 `tasks.md`。**

---

```
╔══════════════════════════════════════════════════════════╗
║           SPEC DRAFT PREVIEW (Level 2)                   ║
╚══════════════════════════════════════════════════════════╝

Feature: dark-mode
Module: ui (待确认 mobile / web)
Location: openspec/changes/dark-mode/proposal.md
```

```markdown
# Dark Mode

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-05
> **Linked Issue**: `none`

## Why

The product currently ships a light theme only, so users who set their operating system to dark appearance get a bright, out-of-place UI. A dark theme reduces eye strain in low-light environments, saves power on OLED displays, and matches the platform-level appearance setting users already expect every app to honor.

## What

Add a user-selectable dark theme with three modes — Light / Dark / Follow system — backed by a semantic color token layer so components stop hard-coding colors. The chosen mode is persisted and applied before first paint, and switching modes re-themes the running app without a restart.

### Key Deliverables

- Semantic color token set with light and dark palettes (surface / on-surface / border / accent / status roles)
- Theme controller supporting Light / Dark / System, subscribed to OS appearance changes
- Persisted theme preference, read and applied before first paint (no flash of the wrong theme)
- Settings screen entry with a three-option theme selector
- Migration of existing components from hard-coded color literals to tokens
- Contrast and visual-regression tests covering both palettes

## Impact

| Type | Description |
|------|-------------|
| **Positive** | Honors the OS appearance setting; reduces eye strain and OLED power draw; the token layer makes any future theme (high-contrast, branding) cheap to add |
| **Risk** | Component migration touches many files and can regress the light theme — mitigated by keeping light values byte-identical during migration and gating on visual-regression snapshots; contrast regressions mitigated by an automated WCAG AA check over every token pair |

## Tasks

- [ ] Define the semantic color token set and derive the light palette from current hard-coded values (no visual change)
- [ ] Design the dark palette against the same token roles
- [ ] Implement the theme controller with Light / Dark / System and OS-change subscription
- [ ] Persist the preference and apply it before first paint
- [ ] Add the theme selector to the settings screen
- [ ] Migrate components off hard-coded color literals
- [ ] Add contrast checks and dual-palette visual-regression tests

## Success Criteria

- [ ] Selecting Light / Dark / System re-themes the whole UI immediately, without restart
- [ ] In System mode, changing the OS appearance switches the app live
- [ ] The preference survives a restart and the correct theme is painted on the first frame (no flash of the wrong theme)
- [ ] Every text/icon-on-background token pair in both palettes meets WCAG AA (>= 4.5:1 normal text, >= 3:1 large text), verified by an automated check
- [ ] Zero hard-coded color literals remain in migrated component code (lint/grep check reports 0)
- [ ] Visual-regression snapshots exist for both palettes on all primary screens, and the light-theme snapshots are unchanged from the pre-change baseline
```

---

**待你确认的三件事** (确认后我才落盘):

1. **Linked Issue**: 我暂填哨兵 `none` (Level 2 头部必填, 不能留空也不能删行)。如果已有 issue, 给我编号, 我按 `` `<org>/<repo>#<n>` `` 形式改写 (例 `` `10CG/Aria#174` ``)。
2. **落点模块**: 单端 UI 还是 mobile + web 共享 token? 后者要改判 Level 3, 我会补出 `tasks.md`。
3. **落点路径**: `openspec/changes/dark-mode/proposal.md` —— 消费方项目**自己仓内**的 `openspec/changes/`, 不是 `standards/openspec/changes/` (Aria 不可协商规则 #5: standards 是共享子模块, 项目自身的变更写进去会对所有采用方可见且无人拥有)。

🤔 Create this file? [Yes / No / Edit]

落盘后建议跑 `openspec validate dark-mode --strict` 验证格式, 然后进入 A.2 (task-planner) 做任务分解。
