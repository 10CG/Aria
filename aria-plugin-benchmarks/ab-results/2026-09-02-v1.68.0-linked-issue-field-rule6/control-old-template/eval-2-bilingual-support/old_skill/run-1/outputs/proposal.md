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
