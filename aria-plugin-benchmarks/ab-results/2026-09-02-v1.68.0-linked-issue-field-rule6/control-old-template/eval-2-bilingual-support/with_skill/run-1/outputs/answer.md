收到双语输入 "Add a dark mode feature / 添加深色模式功能", 按要求 proposal 正文用英文起草; 以下叙述用中文。

## A.1.0 头脑风暴检查

- `docs/decisions/` 下无任何 dark mode / 主题相关的 technical decision-log。
- 存在父级决策 `DEC-20260402-001-aria-dashboard.md` (mode: technical), 它约束了交付形态 (Skill 交付、零依赖、单文件 HTML), 但不涉及主题。
- 无决策记录时 skill 会询问「先 brainstorm 还是直接建 OpenSpec」; 本次按选项 [2] 直接创建, 约束从 DEC-20260402-001 继承, 已在 proposal 头部注明。

## A.1.1–A.1.3 需求提取 / Level 判断 / 模块检测

**关键实况 (起草前实读)**: Aria 仓内唯一的 UI 面是 `aria-dashboard` skill 生成的单文件看板。它的模板 `aria/skills/aria-dashboard/templates/dashboard.html` (1184 行) **已经是硬编码深色** (`:root` 内 `--bg-primary: #0f1117` 等, 11–41 行), 但没有浅色对应、不识别 `prefers-color-scheme`、没有切换开关、没有持久化。所以「添加深色模式」在这里的真实含义不是「刷成深色」, 而是把外观做成可切换的**主题模式** (system / dark / light)。proposal 按这个含义起草, 并保持现有深色输出不变 (向后兼容)。

- **Level 判断**: 触发词 add / feature / 添加 / 功能 → Level 2 词; 单模块 (仅 `aria-dashboard` skill 的模板 + 文档 + 一个新测试), 无 API 契约变更、无 breaking、不碰 `standards/` → 不满足跨模块提升条件。**结论: Level 2 (Minimal)**, 只出 proposal.md, 不出 tasks.md。
- **模块**: `aria` 子模块 (aria-plugin), skill `aria-dashboard`。LEVEL_GUIDE 的四桶里属 "standards (Skill)" 桶, 但落盘位置按 CLAUDE.md Rule #5 放**主仓** `openspec/changes/`, 不放 `standards/openspec/changes/`。
- **Linked Issue**: 对 `10CG/Aria` 与 `10CG/aria-plugin` 做了只读 issue 搜索 ("dark mode" / "dark"), 只有无关模糊命中 (#187 归档 tracker、aria-plugin #133 `_TERMINAL_STATUSES`), 无关联 issue → 逐字写 `` `none` `` (不留空、不删行)。
- **Framework Constraints**: 非 framework 项目, 跳过。

## 预览

```
+----------------------------------------------------------+
|           SPEC DRAFT PREVIEW (Level 2)                   |
+----------------------------------------------------------+

Feature:  aria-dashboard-dark-mode
Module:   aria (aria-plugin) / skill aria-dashboard
Location: openspec/changes/aria-dashboard-dark-mode/proposal.md
Language: English (per request)
```

---

# Aria Dashboard Dark Mode

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-02
> **Linked Issue**: `none`

> **Decision source**: no theming-specific decision log exists under `docs/decisions/`. Delivery-shape constraints are inherited from the parent dashboard decision [DEC-20260402-001](../../../docs/decisions/DEC-20260402-001-aria-dashboard.md) (Skill-delivered, zero-dependency, single-file HTML). `Linked Issue` is `none` after a read-only Forgejo issue search on `10CG/Aria` and `10CG/aria-plugin` for "dark mode" / "dark" returned only unrelated fuzzy matches (#187, aria-plugin #133).
> **Module**: `aria` submodule (aria-plugin) — skill `aria-dashboard` only. Spec lives in the project's `openspec/changes/` (Rule #5), not in `standards/`.

## Why

The `aria-dashboard` skill renders the project progress board from `templates/dashboard.html`. Today that template ships a single, hard-coded dark palette (`:root` token block, `--bg-primary: #0f1117` and friends, lines 11–41) with no light counterpart, no `prefers-color-scheme` handling, no user toggle, and no persistence. "Dark" is therefore not a *mode* — it is the only rendering. Users on a light-themed OS or projecting the board in a bright room get no alternative, and there is no way to configure or switch the appearance per project or per viewer.

This change turns appearance into an explicit **theme mode** (`system` / `dark` / `light`) that respects the viewer's OS preference, can be toggled from the board, remembers the choice, and can be defaulted per project via `.aria/config.json`.

## What

Add a theme-mode system to the single-file dashboard template without introducing any build step or external dependency.

### Design (technical decisions)

1. **Token-based theming.** The existing `:root` block stays the dark baseline (visual output for dark mode is unchanged). A `:root[data-theme="light"]` block overrides the same custom-property names with a light palette. All 6 color literals currently outside the token block (three `rgba(...,0.3)` glow variants, `#fff`, `#4a7de0`, `#3a6dd0`) are moved onto tokens so the light theme cannot leak dark-only literals.
2. **Mode resolution before first paint.** A small inline `<script>` in `<head>` sets `document.documentElement.dataset.theme` by this precedence: stored viewer preference → generator default (`{{THEME_DEFAULT}}` placeholder, filled from `dashboard.theme`) → `matchMedia('(prefers-color-scheme: ...)')`. Running in `<head>` avoids a flash of the wrong theme. `<meta name="color-scheme">` is kept in sync so native controls and scrollbars match.
3. **`system` mode is live.** When the effective mode is `system`, a `matchMedia` change listener re-applies the theme when the OS preference changes; explicit `dark` / `light` ignore OS changes.
4. **Toggle + persistence.** A three-state control (System / Dark / Light) is added to the existing `header-right` block. The choice is written to `localStorage` under key `aria-dashboard-theme`; every read/write is wrapped in `try/catch` and the page renders correctly with no stored value (the board is commonly opened from `file://`, where storage may be unavailable).
5. **Per-project default.** New optional config key `dashboard.theme` (`"system"` | `"dark"` | `"light"`) read at generation time and injected as `{{THEME_DEFAULT}}`. Unknown values fall back to the built-in default and are reported as a warning in the generator output, never as a hard failure.
6. **Data-driven colors stay tokenized.** The KPI progress fill already maps thresholds to `accent-green` / `accent-yellow` / `accent-red` (`references/html-templates.md:18`); generation must keep emitting `var(--accent-*)` rather than hex so both themes recolor it.

### Key Deliverables

- `aria/skills/aria-dashboard/templates/dashboard.html` — light token block, `{{THEME_DEFAULT}}` placeholder, inline head theme-init script, header toggle, `matchMedia` listener, literal colors tokenized.
- `aria/skills/aria-dashboard/SKILL.md` — new `dashboard.theme` row in the config table (default, allowed values) and header version footer bump; the emitted `header-right` version string in the template follows.
- `aria/skills/aria-dashboard/references/html-templates.md` — document the theme token set (dark + light values), the `{{THEME_DEFAULT}}` placeholder, and the toggle markup; `references/execution-flow.md` — add `dashboard.theme` to the config-read step.
- `aria/tests/test_dashboard_theme.py` — structural test over the committed template (baseline-failing before this change): light token block present with the same property names as `:root`, head theme-init script precedes `<body>`, toggle element present, zero color literals outside the two token blocks, light-palette text/background pairs meet WCAG AA contrast (>= 4.5:1, computed in-test with no external dependency).
- `aria/CHANGELOG.md` + version SOT `aria/.claude-plugin/plugin.json` and derived files — release entry (see Impact).

### Constraints

| Type | Constraint | Source |
|------|-----------|--------|
| Delivery | Single self-contained HTML file; no npm / Node / CDN at generation or view time | DEC-20260402-001 |
| Compatibility | Dark rendering is byte-for-byte the same palette as today; existing `{{PLACEHOLDER}}` set unchanged, only `{{THEME_DEFAULT}}` added | CLAUDE.md "向后兼容" |
| Accessibility | Light palette text/background pairs >= 4.5:1 (WCAG AA); focus styles visible in both themes | Project quality bar |
| Storage | `localStorage` optional; page must render correctly when storage throws or is empty | `file://` viewing reality |
| Documentation | Template, SKILL.md config table, and references stay in sync in the same change | Rule #3 |

### Non-Goals

- No redesign of layout, typography, or component structure — palette and mode only.
- No per-section or per-widget theming; a single global mode.
- No server-side or CLI flag for theme (config key + in-page toggle are sufficient for Level 2; a `--theme` flag can be a follow-up if requested).
- No changes to Issue-form backends or data parsers.

## Impact

| Type | Description |
|------|-------------|
| **Positive** | Board respects viewer OS preference and is readable in bright environments; per-project default via config; zero new dependencies; dark output unchanged for existing users. |
| **Risk** | Light palette leaks a dark-only literal (unreadable element). Mitigation: tokenize all literals and enforce "zero literals outside token blocks" in the structural test. |
| **Risk** | Flash of wrong theme on load. Mitigation: mode resolved by inline head script before body renders; test asserts script position. |
| **Risk** | Storage unavailable on `file://` in some browsers. Mitigation: guarded access, `system`/config default used when storage is empty or throws. |
| **Versioning** | New backward-compatible capability inside an existing skill → aria-plugin **MINOR** bump (v1.67.2 → v1.68.0) per SemVer; release sync surface per CLAUDE.md (5 plugin files + main-repo gitlink + VERSION + README badge). Downgrade to PATCH is an owner call. |

## Tasks

- [ ] Define the light token set (same property names as `:root`) and add the `[data-theme="light"]` override block
- [ ] Move the 6 out-of-block color literals onto tokens; keep KPI fill emitting `var(--accent-*)`
- [ ] Add inline head theme-init script (stored → `{{THEME_DEFAULT}}` → `prefers-color-scheme`) and `color-scheme` meta sync
- [ ] Add the System / Dark / Light toggle to `header-right`, wire persistence (`aria-dashboard-theme`, guarded) and the `matchMedia` change listener for `system`
- [ ] Read `dashboard.theme` at generation, inject `{{THEME_DEFAULT}}`, warn on invalid value
- [ ] Write `aria/tests/test_dashboard_theme.py` (baseline-failing structural + contrast test)
- [ ] Sync docs: SKILL.md config table + version footer, `references/html-templates.md`, `references/execution-flow.md`
- [ ] Version bump + CHANGELOG entry on the release sync surface

## Success Criteria

- [ ] Generating the dashboard with no `dashboard.theme` config and no stored preference on a light-OS browser renders the light palette; on a dark-OS browser renders the current dark palette (manual check, both recorded in the PR).
- [ ] Toggling to Light, reloading, and re-opening the file keeps Light; clearing storage returns to the resolved default (manual check recorded in the PR).
- [ ] `test_dashboard_theme.py` fails on the pre-change template and passes on the post-change template; it asserts: identical token-name sets in `:root` and `[data-theme="light"]`; head theme-init script appears before `<body>`; toggle element present; `grep` count of `#hex` / `rgb(a)` literals outside the two token blocks equals 0; every light text/background pair >= 4.5:1.
- [ ] Dark-mode computed palette is unchanged: the `:root` token values after the change equal the values at the pre-change commit (asserted in-test against a frozen list).
- [ ] Existing placeholder set is unchanged except for the added `{{THEME_DEFAULT}}` (asserted in-test).
- [ ] SKILL.md config table documents `dashboard.theme` with default and allowed values; `html-templates.md` documents both token sets and the placeholder.

## Open Item for Owner (product-level)

**Default mode when neither config nor stored preference exists.** Two defensible options, both fully specified above; only the default differs:

1. `system` — conventional dark-mode UX; light-OS viewers see the new light palette by default (a visible change for them).
2. `dark` — preserves today's rendering for every viewer; light mode is opt-in via toggle or `dashboard.theme`.

This proposal is written with option 1 as the built-in default; switching to option 2 changes one constant and one line of the SKILL.md config table. Please confirm before A.2.

## Rule #6 Note

`rule6_note`: The change surface is (a) HTML/CSS/JS template content and (b) a descriptive config-table row + version footer in `SKILL.md` and reference docs. Neither hunk alters the skill `description` or its instruction flow, so the AB suite cannot observe the change. Per the exemption table this is the **substitute** lane: the SC-level baseline-failing structural test `aria/tests/test_dashboard_theme.py` is the substitute evidence. If Phase B ends up editing any prescriptive text in `SKILL.md` (e.g., the Step 2 HTML-generation instructions beyond the config row), that hunk is prescriptive and the AB benchmark must be run for it — 宁跑勿豁.

## References

- [DEC-20260402-001 — Aria Dashboard design decision](../../../docs/decisions/DEC-20260402-001-aria-dashboard.md)
- `aria/skills/aria-dashboard/SKILL.md` (v1.1.0) and `templates/dashboard.html` (current dark-only token block, lines 11–41)
- `standards/openspec/templates/proposal-minimal.md` (header SOT)
- `standards/conventions/skill-benchmark-exemption.md` (Rule #6 lanes)
- `standards/conventions/version-management.md` (release sync surface)

---

## 待你确认

Create this file? [Yes / No / Edit]

本次未向仓库写入任何文件; 上面即 `openspec/changes/aria-dashboard-dark-mode/proposal.md` 的完整内容, 你确认 Yes 后再落盘。

**需要你裁的一项 (产品级)**: 无 config、无已存偏好时的默认模式 —— 选 `system` (跟随系统, 浅色 OS 用户会看到新浅色) 还是 `dark` (维持现状, 浅色靠开关/配置 opt-in)。proposal 以 `system` 起草, 改成 `dark` 只动一个常量和 SKILL.md 配置表一行。

**技术级我已直接裁定** (写在 Design 段, 可证伪判据在 Success Criteria): 保留现有深色 token 为 `:root` 基线不动; 用 `[data-theme="light"]` 覆盖同名 token; `<head>` 内联脚本先于首帧决定模式 (存储偏好 → `dashboard.theme` → `prefers-color-scheme`) 防闪烁; `localStorage` 全部 try/catch 包裹; 6 处游离色值全部 token 化; 版本按 SemVer 建议 MINOR (v1.68.0)。

**Rule #6**: 本变更不改 skill `description` 与指令流, 属描述性内容 → substitute 通道 (baseline-failing 结构化测试 `aria/tests/test_dashboard_theme.py`), `rule6_note` 已写入 proposal; 若 Phase B 触及 SKILL.md 处方性文字则该 hunk 照跑 AB。

**A.1.6 验证提示**: 落盘后建议运行 `openspec validate aria-dashboard-dark-mode --strict` 验证格式; 之后进入 A.2 (`/task-planner`) 做任务规划。
