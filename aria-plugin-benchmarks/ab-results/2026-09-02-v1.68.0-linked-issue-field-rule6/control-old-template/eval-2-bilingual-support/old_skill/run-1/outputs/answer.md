# spec-drafter (A.1) — "Add a dark mode feature / 添加深色模式功能"

## 1. 输入处理 (双语)

输入的两半是同一需求的中英文表述, 归一为一条需求: **为项目的 UI 表面添加深色模式功能**。你明确要求 **英文 proposal**, 所以下方 proposal 正文全英文; 本回复的叙述按项目工作语言用中文。

## 2. A.1.0 决策记录检查

扫描 `docs/decisions/` (21 份 DEC-*), 没有任何 technical decision-log 涉及 theme / dark mode / 深色。按 skill 流程应询问「先 brainstorm [1] / 直接创建 [2] / 取消 [3]」; 本次取 **[2] 直接创建**, 理由: 范围是 Level 2 单 skill 改动, 技术路径 (CSS token 分层 + `prefers-color-scheme` + localStorage) 无争议, 不需要 brainstorm.technical。已把这条记为假设 A-2 写进 proposal。

## 3. A.1.2 Level 判断

| 因素 | 观察 | 指向 |
|------|------|------|
| 关键词 | `Add` / `添加` + `feature` / `功能` | Level 2 触发词 (功能开发) |
| 影响范围 | 单一 skill `aria-dashboard`, 3-5 个文件 (模板 + 1 份 references 文档 + SKILL.md 版本行 + CHANGELOG) | 单模块 |
| 变更类型 | 非架构 / 非跨模块 / 非 breaking (生成流程与占位符集合不动) | 不升 Level 3 |

**结论: Level 2 (Minimal) → 只产出 `proposal.md`, 不生成 `tasks.md`。**

## 4. A.1.3 模块检测 + 一个关键发现

Aria 是方法论仓, 没有 mobile / backend 模块。仓内唯一的图形 UI 表面是 `aria-dashboard` skill 生成的单文件 HTML 看板 (`aria/skills/aria-dashboard/templates/dashboard.html` → `.aria/dashboard/index.html`)。模块记为 **`aria` (aria-plugin 子模块) / skill `aria-dashboard`**。

**关键发现**: 这个看板**现在就是深色的, 而且只有深色** —— `:root` 里 `--bg-primary: #0f1117` 等全套 token 只有一组, 没有 light 对应、没有 `prefers-color-scheme` 处理、没有任何 theme JS。所以「添加深色模式功能」在这里的真实含义是 **把深色变成可选模式**: 保留现有调色板作为 dark, 新增 light 调色板 + 三态切换 (System / Light / Dark) + 跟随系统偏好 + localStorage 持久化。proposal 按这个理解起草, 并把「目标表面 = aria-dashboard」记为假设 A-1, 如果你指的是别的产品, 请带 `module` 参数重跑。

顺带量了基线, 让成功标准可证伪: 模板 `:root` 之外还有 **6 处** 硬编码颜色字面量 (第 88/94/100 行 rgba 边框, 670 行 `#fff`, 681/685 行按钮蓝), proposal 要求归零。

## 5. 位置

SKILL.md 里写的 `standards/openspec/changes/{feature}/` 是过期路径; 按 CLAUDE.md 不可协商规则 5 和 `standards/openspec/project.md` 的「两个 openspec 目录」表, 项目变更放 **`openspec/changes/dashboard-dark-mode/proposal.md`**。已确认该目录不存在, 无同名 Spec。

## 6. Rule #6 / 版本

- 改动全是描述性 (静态 HTML 资产 / 片段文档 / 版本行), 不触及 AI 指令流或 skill `description` → Rule #6 表「描述性 → substitute」: 用 SC 级 baseline-failing 结构化检查 (token 对等 / 字面量归零 / 版本串一致) 替代 AB。`ab-suite/` 下没有 `aria-dashboard.json`, 已把「开套件缺口 issue」列为任务。`rule6_note` 已写进 proposal。
- 版本: 既有 skill 新增用户可见功能 → aria-plugin **MINOR** (`version-management.md` §2.2); skill 1.1.0 → 1.2.0。

## 7. 需要 owner 裁的一条产品级决策

**D-1**: 没有存储偏好的用户默认看什么? 推荐 **`system`** (跟随系统, 深色模式功能的常规语义); 备选 **`dark`** (对现有用户零渲染变化, 直到主动切换)。技术工作量相同, 只差初始回退值。

---

```
╔══════════════════════════════════════════════════════════╗
║           SPEC DRAFT PREVIEW (Level 2)                   ║
╚══════════════════════════════════════════════════════════╝

Feature:  dashboard-dark-mode
Module:   aria (aria-plugin submodule) / skill aria-dashboard 1.1.0 -> 1.2.0
Location: openspec/changes/dashboard-dark-mode/proposal.md
Level:    2 (Minimal) - proposal.md only
──────────────────────────────────────────────────────────
```

# Dashboard Dark Mode (Theme Toggle)

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-02
> **Change ID**: `dashboard-dark-mode`
> **Module**: `aria` (aria-plugin submodule) — skill `aria-dashboard` v1.1.0 → v1.2.0
> **Context**: v2.0 M6 executing (per CLAUDE.md project-status snapshot; no live `/state-scanner` run) · aria-plugin v1.67.2 · no related active risk · no related decision log in `docs/decisions/`
> **Source requirement**: "Add a dark mode feature / 添加深色模式功能" (bilingual input, both halves express the same requirement; normalized to one feature; proposal written in English by explicit request)
> **Target surface (assumption A-1)**: the aria-dashboard HTML output (`.aria/dashboard/index.html`, rendered from `aria/skills/aria-dashboard/templates/dashboard.html`) — the only user-facing UI surface in this repository

---

## Why

The Aria dashboard is the project's only graphical surface, and today it ships a **single, hard-wired dark palette**: `templates/dashboard.html` defines every color once in `:root` (`--bg-primary: #0f1117` …) with no light counterpart, no `prefers-color-scheme` handling, and no user control. Users on light-themed desktops, users who print or screenshot the board for documents, and users with light-preferring accessibility settings currently have no way to switch.

"Add a dark mode feature" therefore means making dark a **selectable mode** rather than the only mode: keep the current palette as *dark*, add a *light* palette, follow the operating-system preference by default, and let the viewer override and persist the choice. Doing this now, while the template still routes almost all colors through CSS custom properties, is cheap; every additional hard-coded literal added later makes it more expensive.

## What

Make the dashboard template theme-aware with a three-state theme control (**System / Light / Dark**), implemented entirely inside the single self-contained HTML file so the generator flow of the `aria-dashboard` skill (`references/execution-flow.md` Step 2, `{{PLACEHOLDER}}` replacement) needs **no changes**.

### Design

1. **Token layering** — Keep the existing `:root` block as the dark token set (unchanged values). Add a `[data-theme="light"]` block that redefines *every* token declared in `:root` (backgrounds, borders, text, `--accent-*` and `--accent-*-dim`, `--shadow-*`). Add an `@media (prefers-color-scheme: light)` rule scoped to `:root:not([data-theme="dark"])` so the system preference applies when no explicit choice exists, and an explicit `[data-theme="dark"]` override so a stored choice wins in both directions.
2. **Literal migration** — Move the 6 color literals that currently live outside `:root` into tokens (baseline measured 2026-09-02 on `templates/dashboard.html`: lines 88/94/100 `rgba(...,0.3)` KPI borders → `--accent-*-border`; line 670 `#fff` → `--text-on-accent`; lines 681/685 button blues → `--accent-blue-hover` / `--accent-blue-active`). Result: zero color literals outside the token blocks.
3. **No-flash initialization** — A tiny inline `<script>` in `<head>` (before the stylesheet is applied to the body) reads `localStorage["aria-dashboard-theme"]` inside `try/catch` and stamps `data-theme` on `<html>` before first paint; on any storage error or missing value it stamps nothing and lets the media query decide. Dark remains the final fallback when neither storage nor `matchMedia` is available (preserves today's rendering exactly).
4. **Toggle control** — A compact segmented control (System / Light / Dark) mounted in the existing `.header-right` block next to the `Aria Dashboard v1.x` / `Generated:` lines. Clicking writes `data-theme` (or removes it for System) and persists to `localStorage["aria-dashboard-theme"]` (values: `light` | `dark`; System = key absent). Behavior lives in the existing IIFE at the bottom of the template, alongside the section-collapse handlers.
5. **Generated-fragment hygiene** — `references/html-templates.md:18` says the KPI progress fill uses `accent-green / accent-yellow / accent-red` but the fragment on line 14 renders `style="…; background:{COLOR}"`; clarify the doc so `{COLOR}` is emitted as `var(--accent-green)` etc. (a token reference, never a hex literal), so generator output is themable without touching generator logic.
6. **Contrast check** — Both palettes are checked against WCAG AA (4.5:1 for `--text-primary`/`--text-secondary` on `--bg-primary`/`--bg-card`; 3:1 for `--text-muted` and for badge/accent text on `--accent-*-dim`). A small standalone script computes the ratios from the token values; failing pairs are adjusted in the same change.

### Key Deliverables

- `aria/skills/aria-dashboard/templates/dashboard.html` — light token block + system-preference media query + explicit dark override; 6 literals migrated to tokens; head-inline theme-init script; header toggle control + handler; header version string → `Aria Dashboard v1.2.0`
- `aria/skills/aria-dashboard/references/html-templates.md` — new "Theme tokens" section (token list, light/dark values, rule that fragments reference tokens only); line 18 clarified to `var(--accent-*)`
- `aria/skills/aria-dashboard/SKILL.md` — version banner 1.1.0 → 1.2.0 and a one-line mention of the theme control under the HTML-generation summary (descriptive only; no procedural change)
- `aria/CHANGELOG.md` — MINOR entry (new user-visible skill feature, `version-management.md` §2.2)
- Structural check (Rule #6 substitute, see `rule6_note`) — a script/test asserting token parity between `:root` and `[data-theme="light"]`, zero color literals outside token blocks, and version-string agreement between SKILL.md and the template header

### Surface Constraints (analog of Framework Constraints, Aria #95)

No web framework is involved; the surface is a vanilla single-file HTML/CSS/JS template. Constraints audit agents should check against:

- **Self-contained single file**: no external stylesheets, scripts, fonts, or network requests may be introduced (the file is opened via `file://` / `xdg-open`, often offline).
- **Placeholder contract intact**: the set of `{{PLACEHOLDER_NAME}}` tokens consumed by `execution-flow.md` Step 2 must not change (no new placeholders, none removed); theme default is resolved client-side, not injected by the generator.
- **`file://` storage semantics**: `localStorage` under `file://` may be shared across all local files in some browsers or throw in restricted contexts — the key is namespaced (`aria-dashboard-theme`) and every read/write is wrapped in `try/catch`.
- **Existing JS style**: ES5-compatible IIFE, no build step, no dependencies (matches the template's current `<script>` block).

## Impact

| Type | Description |
|------|-------------|
| **Positive** | Dashboard becomes usable on light desktops and in printed/screenshotted reports; follows OS preference by default; user choice persists per browser. Removes all hard-coded color literals, so future palette work is token-only. |
| **Risk** | Default-theme change for existing users: a light-OS user who never chose a theme would now see light instead of the familiar dark. Mitigation: owner decision **D-1** below (recommend `system`; alternative `dark`-default keeps today's rendering byte-identical for everyone until they toggle). Light palette may fail contrast where dark passes — mitigated by the contrast check being a Success Criterion, not a manual glance. |
| **Compatibility** | Non-breaking. Generator flow, data parsers, placeholder set, output path and issue-form behavior are untouched. Browsers without `matchMedia`/`localStorage` render exactly as today (dark). |
| **Version** | aria-plugin **MINOR** (new feature in an existing skill, `standards/conventions/version-management.md` §2.2); skill `aria-dashboard` 1.1.0 → 1.2.0; the 5-file release sync face applies. |

## Tasks

- [ ] Derive the light palette and define the `[data-theme="light"]` block covering every `:root` token; add `@media (prefers-color-scheme: light)` scoped to `:root:not([data-theme="dark"])` and the explicit `[data-theme="dark"]` override
- [ ] Migrate the 6 out-of-`:root` color literals (lines 88/94/100/670/681/685) to new tokens defined in both palettes
- [ ] Add the head-inline theme-init script (try/catch storage read, `data-theme` stamp before first paint, dark as final fallback)
- [ ] Add the System / Light / Dark control to `.header-right` and its handler in the bottom IIFE (write/remove `data-theme`, persist to `localStorage["aria-dashboard-theme"]`)
- [ ] Clarify `html-templates.md:18` so the KPI progress fill emits `var(--accent-*)`; add the "Theme tokens" section
- [ ] Write the contrast-ratio script over the specified token pairs for both palettes; adjust any failing pair
- [ ] Docs sync (Rule #3): SKILL.md banner + template header string → 1.2.0; aria `CHANGELOG.md` MINOR entry
- [ ] Rule #6 substitute: add the structural check (token parity / zero literals / version match) and confirm it **fails on the current template** before the change and passes after; open an AB-suite gap issue for `aria-dashboard` (no `aria-plugin-benchmarks/ab-suite/aria-dashboard.json` exists today)
- [ ] Manual verification in one Chromium-based and one Firefox browser: toggle each state, reload (persists), clear storage (follows OS), print preview in light

## Success Criteria

- [ ] **SC-1 Token parity**: the set of `--*` custom-property names declared in `:root` equals the set declared in `[data-theme="light"]` (regex-extracted, compared as sets). Baseline 2026-09-02: light block absent → check fails (baseline-failing by construction).
- [ ] **SC-2 Zero literals**: count of `#[0-9a-fA-F]{3,8}` or `rgba?(` occurrences outside the token blocks in `templates/dashboard.html` is **0**. Baseline 2026-09-02: **6** (lines 88, 94, 100, 670, 681, 685).
- [ ] **SC-3 Three-state control**: the template contains a `prefers-color-scheme` media query, reads and writes `localStorage` key `aria-dashboard-theme`, and sets/removes `data-theme` on `document.documentElement`; manually, in two browsers, choosing Light/Dark survives reload and choosing System follows a change of OS preference.
- [ ] **SC-4 No flash / safe fallback**: the theme-init script appears inside `<head>` before `</head>`; with storage disabled (throwing) and `matchMedia` absent the page renders the current dark palette unchanged (verified by opening the file with storage blocked and comparing computed `--bg-primary` = `#0f1117`).
- [ ] **SC-5 Generator untouched**: `references/execution-flow.md` diff is empty; the `{{PLACEHOLDER}}` set extracted from the template before and after the change is identical; the KPI fill rule in `html-templates.md` names `var(--accent-*)` and contains no hex literal.
- [ ] **SC-6 Contrast**: every pair listed in Design item 6 meets its WCAG AA threshold in **both** palettes, as output by the contrast script (script output attached to the PR; a dark-palette pair that fails today is fixed here too, not waived).
- [ ] **SC-7 Version agreement**: the version string in `SKILL.md` banner, the template header (`Aria Dashboard vX.Y.Z`) and the `CHANGELOG.md` entry are identical (`1.2.0`).
- [ ] **SC-8 Still self-contained**: number of `https?://` references inside `<style>`/`<script>` in the template is unchanged from baseline (no external assets introduced).

## Out of Scope

- A config-driven default theme (e.g. `.aria/config.json → dashboard.theme`) — would require a new placeholder and a Step-2 generator instruction (prescriptive change, Rule #6 full run); deferred to a follow-up once this client-side version ships.
- Re-theming the issue form's markdown output or any non-dashboard surface.
- Translating dashboard UI strings (the template keeps its current English labels under `lang="zh-CN"`; the new control uses English labels to match the existing header).

## Decisions and Assumptions

| ID | Kind | Statement | Status |
|----|------|-----------|--------|
| A-1 | Assumption (technical) | Target surface is the `aria-dashboard` HTML template, the only UI surface in the repo. If the request concerns a different product, re-run spec-drafter with an explicit `module`. | Stated; confirm at A.1.5 |
| A-2 | Assumption (process) | A.1.0 brainstorm check found no technical decision log for this topic; option [2] "create OpenSpec directly" was taken because scope is Level 2 and well understood. | Stated |
| A-3 | Assumption (language) | Bilingual input normalized to one requirement; proposal in English per the explicit request. | Stated |
| D-1 | **Owner decision (product-level)** | Default for viewers with no stored choice: **`system`** (recommended — conventional meaning of a dark-mode feature) vs **`dark`** (zero rendering change for existing users until they toggle). Technical work is identical; only the initial fallback differs. | Open — owner |

`rule6_note`: The change touches `templates/dashboard.html` (static asset), `references/html-templates.md` (descriptive fragment documentation), the `SKILL.md` version banner and `CHANGELOG.md`. None of these alter an AI-facing instruction flow or the skill `description`; per the Rule #6 table this is **descriptive → substitute**: an SC-level baseline-failing structural check (SC-1/SC-2/SC-7) replaces an AB run. No `ab-suite/aria-dashboard.json` exists, so if a later hunk does change Step-2 generation instructions (e.g. the deferred config-driven default), it falls in the "prescriptive, outside suite coverage" row: name the behavior, build a falsifiable directed fixture, and open the suite-gap issue (already a task above). Any hunk that is unclear is run, not exempted.

## Next Steps

- A.2 / A.3: `/task-planner` to expand the Tasks above into `detailed-tasks.yaml` (Level 2 — no `tasks.md`).
- Validation: the skill suggests `openspec validate dashboard-dark-mode --strict`; inside the Aria repo `standards/openspec/project.md` directs validation to `/audit-engine` (post_spec) instead of the npm CLI.

```
──────────────────────────────────────────────────────────
Create this file? [Yes/No/Edit]
```

**本次为评估运行, 未在仓库创建任何文件**; `openspec/changes/dashboard-dark-mode/proposal.md` 的完整正文即上方内容, 已同时存为输出目录下的 `proposal.md`。

## 8. 交互确认清单 (A.1.5, 请逐项看)

1. **Level** = 2 — 若你认为要连带改生成流程 (config 驱动默认主题), 会升 Level 并触发 Rule #6 全跑, 我建议留到后续。
2. **Why / What** — 是否接受「深色变可选模式 (含 light 调色板 + 三态切换)」这个理解 (假设 A-1)。
3. **Deliverables** — 5 项, 全在 `aria/skills/aria-dashboard/` + `aria/CHANGELOG.md`。
4. **Impact** — 唯一实质风险是 D-1 默认主题, 需要你裁。
5. **Tasks / Success Criteria** — 8 条 SC 全部可机械或双浏览器手工验证, 基线已量 (6 处字面量)。

## 9. 下一步

- 你确认 (或 Edit) 后 → 落盘 `openspec/changes/dashboard-dark-mode/proposal.md` → `/task-planner` 做 A.2/A.3。
- skill 建议 `openspec validate dashboard-dark-mode --strict`; 但 Aria 仓内按 `standards/openspec/project.md` 用 `/audit-engine` (post_spec) 验证, 不装 npm CLI。
