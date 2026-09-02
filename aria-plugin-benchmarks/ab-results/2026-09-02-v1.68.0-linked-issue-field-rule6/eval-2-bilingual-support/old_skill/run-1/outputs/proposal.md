# Aria Dashboard Dark Mode

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-02
> **Linked Issue**: `none` — verified 2026-09-02: Forgejo issue search on `10CG/Aria` (q=dark, q=theme) and `10CG/aria-plugin` (q=dark, q=dashboard) returned only substring false positives (e.g. Aria#173 "gate_result ... 静默 pass", aria-plugin#133 "_TERMINAL_STATUSES"); no open or closed issue asks for dashboard theming.
> **Change ID**: `aria-dashboard-dark-mode`
> **Source request (bilingual, verbatim)**: "Add a dark mode feature / 添加深色模式功能" — the two halves are equivalent; this proposal is written in English as requested.
> **Code location**: `aria/` submodule, skill `skills/aria-dashboard/` (template + SKILL.md + references). The Spec lives in the main repo `openspec/changes/` per CLAUDE.md Rule #5 (precedent: `sibling-spec-probe`, "代码落点 aria/ 子模块; Spec 落主仓").
> **Decision source**: none — `docs/decisions/` holds 21 DEC records, none about dashboard theming; `brainstorm.technical` was not run. The single product-level choice is surfaced explicitly under "Open decision" below.

## Why

The aria-dashboard skill is the only user-facing HTML surface in the Aria plugin: it renders `.aria/dashboard/index.html` for stakeholders who do not use the CLI. Today that page has exactly one appearance, and it is a hard-wired dark palette:

| Fact (state scan 2026-09-02) | Evidence |
|------|------|
| Single palette, dark values only, defined once | `templates/dashboard.html:11-40` — `:root { --bg-primary: #0f1117; ... --text-primary: #e4e6ed; ... }` (28 tokens) |
| No light counterpart, no system-preference handling | `grep -i 'prefers-color-scheme\|data-theme\|dark\|light\|theme'` over the template returns 0 hits; the only `@media` rules are width breakpoints (lines 261 / 362 / 643 / 853) |
| No theme toggle, no persistence | the `<script>` block (lines 1084-1182) contains only section collapse, status-badge tweaks and the Issue form; `localStorage` is never referenced |
| Six color literals bypass the token layer | lines 128 / 134 / 140 (`rgba(...,0.3)` status-badge borders) and 710 / 721 / 725 (`#fff`, `#4a7de0`, `#3a6dd0` in `.btn-generate`) |

So, taken literally, "the dashboard is dark" is already true — but dark is not a *mode*: it cannot be chosen, and it cannot be left. Viewers on a light OS theme, on projectors, or printing the page get a dark-only render with no alternative, and any future light variant would have to fork the whole stylesheet because the token layer leaks. The value of this change is to make dark mode a first-class, user-selectable theme: a light/dark token pair, a system-preference default, an in-page toggle that persists, and a configuration default — while keeping the existing dark look token-for-token identical for anyone who prefers it.

## What

Turn the dashboard's single hard-coded palette into a two-theme token system with dark mode as an explicit, persisted, user-selectable mode. No changes to data collection, parsers, or Issue backends.

1. **Theme tokens** — Keep the existing dark values verbatim and scope them to `:root[data-theme="dark"]`, plus an `@media (prefers-color-scheme: dark)` block that applies the same dark values when no explicit choice is stored (`:root:not([data-theme="light"])`). Define a complete light token set on bare `:root` using the same 28 token names (`--bg-*`, `--border*`, `--text-*`, `--accent-*`, `--accent-*-dim`, `--shadow-*`, `--radius-*`, `--transition`). Replace the six residual color literals with tokens so both themes are driven entirely by the token layer.
2. **Toggle + persistence** — Add a small control in `.header-right` with three states: `system` / `light` / `dark`. The selection is stored in `localStorage` (key `aria-dashboard-theme`) inside `try/catch`; on read failure or absence the page falls back to `system`. A tiny inline boot script in `<head>` applies the stored `data-theme` before first paint, so there is no flash of the wrong theme.
3. **Configuration default** — New optional key `dashboard.theme` in `.aria/config.json` (`"system"` default; `"light"` / `"dark"` accepted), alongside the existing `dashboard.*` keys. Step 2 of the generation flow injects it through a new `{{THEME_DEFAULT}}` placeholder; an unknown value falls back to `system` with a one-line warning in the generation summary. A stored viewer preference always wins over the config default.
4. **Light-theme legibility** — Status / verdict / priority chips and KPI progress colors rely on `accent-*` tokens tuned for dark backgrounds (e.g. `--accent-yellow: #f0c351`). The light set gets its own accent values so every text-on-background pair meets WCAG AA (contrast >= 4.5:1). The documented rule "pct >= 80 -> accent-green, >= 50 -> accent-yellow, < 50 -> accent-red" in `html-templates.md` is unchanged; only the resolved colors differ per theme.
5. **Documentation + version** — The SKILL.md config table gains the `dashboard.theme` row and Step 2 mentions `{{THEME_DEFAULT}}`; `execution-flow.md` Step 2 and `html-templates.md` gain a "Theme tokens" section; skill version 1.1.0 -> 1.2.0; aria-plugin bump per `standards/conventions/version-management.md` (a new user-visible capability in an existing skill -> MINOR proposed).

### Key Deliverables

- `aria/skills/aria-dashboard/templates/dashboard.html` — light + dark token sets, six literals tokenized, header theme control, `<head>` boot script, `{{THEME_DEFAULT}}` placeholder
- `aria/skills/aria-dashboard/SKILL.md` — `dashboard.theme` config row, Step 2 wording, version 1.2.0
- `aria/skills/aria-dashboard/references/execution-flow.md` — Step 2 theme injection + unknown-value fallback
- `aria/skills/aria-dashboard/references/html-templates.md` — "Theme tokens" table (token -> light value / dark value) + contrast rule
- `aria-plugin-benchmarks/aria-dashboard/` — directed, baseline-failing fixture for theme output (Rule #6; see `rule6_note`)
- (Conditional) `.aria/config.template.json` — `dashboard.theme` example, only if a `dashboard` block is introduced; today the template has no `dashboard` block and the skill already runs with every `dashboard.*` key absent

### Out of Scope

- Restyling or layout changes beyond what theming requires; no new sections, charts, or data sources
- Any external asset (`<link>`, `<script src>`, web fonts) — the single-file, self-contained contract of the dashboard is preserved
- Theming of Issue backends (git / GitHub API / Forgejo API) — server-side, unaffected
- Syncing the viewer's theme preference across devices (`localStorage` is per browser by design)

### Open decision (product-level, owner)

Default when nothing is stored and `dashboard.theme` is absent: **`system`** (proposed — matches platform convention and the light-OS use case that motivates this change) vs **`dark`** (zero visible change for every existing viewer; light becomes opt-in). Nothing else in this proposal depends on the choice; the token / toggle / config work is identical either way.

## Impact

| Type | Description |
|------|-------------|
| **Positive** | The dashboard becomes usable on light OS themes, projectors and paper; the existing dark appearance is preserved token-for-token and stays one click (or one config line) away; the six token leaks are closed, so future palette work touches one block per theme instead of the whole stylesheet |
| **Risk** | Light-theme contrast regressions on status / verdict / priority chips — mitigated by a separate light accent set and a scripted WCAG AA check (SC-5). Flash of the wrong theme on load — mitigated by the `<head>` boot script (SC-3). `localStorage` unavailable (some `file://` contexts, sandboxes) — mitigated by `try/catch` fallback to `system` (SC-4). A `system` default is user-visible for viewers on light OS themes — surfaced as the open decision above rather than decided silently |
| **Compatibility** | All 31 existing `{{...}}` placeholders consumed by Step 2 are untouched (one new placeholder added); parsers, data schema, Issue form and backends are unchanged; `dashboard.theme` is optional, so existing `.aria/config.json` files keep working |

## Tasks

- [ ] Split `:root` into a light base set and a dark set (`[data-theme="dark"]` + `prefers-color-scheme` fallback), keeping the current dark values verbatim; tokenize the six residual color literals
- [ ] Add the header theme control (system / light / dark), the `<head>` boot script, and `localStorage` persistence with `try/catch` fallback
- [ ] Add `dashboard.theme` (default `system`) and the `{{THEME_DEFAULT}}` placeholder to the Step 2 generation flow, with unknown-value fallback + warning
- [ ] Define light accent tokens and verify contrast (WCAG AA) for every text-on-background pair in both themes with a small script; attach its output to the PR
- [ ] Update SKILL.md (config table, Step 2, version 1.2.0), `execution-flow.md` and `html-templates.md`
- [ ] Rule #6: build the baseline-failing directed fixture, run the AB on `aria-plugin-benchmarks/aria-dashboard/`, and open the suite-gap issue on `10CG/aria-plugin` (see `rule6_note`)
- [ ] Regenerate the dashboard from this repository and spot-check both themes plus print preview; bump the aria-plugin version per `version-management.md`

## Success Criteria

- [ ] SC-1 Both token sets present: in the generated `.aria/dashboard/index.html`, `grep -c ':root {'` >= 1 and `grep -c '\[data-theme="dark"\]'` >= 1, and the dark block's 28 `--*:` lines are byte-identical to the pre-change `:root` block (diff is empty)
- [ ] SC-2 No token leaks: outside the `:root` / `[data-theme]` / `@media (prefers-color-scheme)` blocks, `grep -nE '#[0-9a-fA-F]{3,6}\b|rgba\('` over `dashboard.html` returns 0 lines (today: 6)
- [ ] SC-3 System default + no flash: with storage cleared and `dashboard.theme` absent, DevTools emulation of `prefers-color-scheme: light` renders the light set and `dark` renders the dark set, and `<html>` already carries the resolved `data-theme` when `DOMContentLoaded` fires
- [ ] SC-4 Toggle + persistence: switching theme changes the rendered palette without reload; the choice survives a reload; clearing site data returns to the system default; with `localStorage` access throwing (simulated), the page still renders in `system` mode with no console error
- [ ] SC-5 Contrast: every text token on every background token it is paired with, in both themes, measures >= 4.5:1 (scripted check, results attached to the PR); the KPI color rule still maps green / yellow / red as documented
- [ ] SC-6 Self-contained: the generated HTML has zero `<link rel="stylesheet">` and zero `<script src=...>` (same as today)
- [ ] SC-7 Config knob: `dashboard.theme: dark` yields `data-theme="dark"` in the generated file; an unknown value (e.g. `"blue"`) yields `system` plus a warning line in the generation summary; absence yields `system`
- [ ] SC-8 Rule #6 evidence attached per `rule6_note`; SKILL.md frontmatter `description` unchanged (the diff shows no change in that field)
- [ ] SC-9 Documentation in sync (CLAUDE.md Rule #3): `SKILL.md` config table, `execution-flow.md` Step 2 and `html-templates.md` all describe `dashboard.theme` / `{{THEME_DEFAULT}}` / the token pair — verified by grep on each file

## rule6_note (Skill benchmark, CLAUDE.md Rule #6)

Judged hunk by hunk, per `standards/conventions/skill-benchmark-exemption.md`:

| Hunk | Nature | Disposition |
|------|--------|-------------|
| `SKILL.md` frontmatter `description` | unchanged | no description-triggering AB needed (SC-8 proves it) |
| `templates/dashboard.html` CSS/JS, `html-templates.md` token table | descriptive asset — does not change how the AI decides anything | substitute: SC-1 / SC-2 / SC-6 / SC-7 are structural, baseline-failing checks (the pre-change template has no `[data-theme]`, six literals, no placeholder) |
| `SKILL.md` Step 2 + `execution-flow.md` Step 2 ("read `dashboard.theme`, inject `{{THEME_DEFAULT}}`, fall back on unknown value") | prescriptive runtime instruction | AB is run, no discretion. The existing suite `aria-plugin-benchmarks/aria-dashboard/` is a single `iteration-1/eval-1` (last archived result `ab-results/2026-04-23-v1.16.4-patch/aria-dashboard/`, prompt file not preserved) and does not observe theme output — so per the "suite does not cover it" row: name the behavior (theme injection + unknown-value fallback), add a falsifiable directed fixture (the old skill emits no `data-theme` and no warning on `"blue"`), and open a suite-gap issue on `10CG/aria-plugin` (context: aria-plugin#150) |

Running the benchmark itself needs no OpenSpec.

## References

- Template under change: `aria/skills/aria-dashboard/templates/dashboard.html` (1184 lines; tokens at 11-40, width breakpoints 261 / 362 / 643 / 853, script 1084-1182)
- Generation flow: `aria/skills/aria-dashboard/references/execution-flow.md` — Step 2 (template + placeholder substitution) and Step 3 (writes `.aria/dashboard/index.html`)
- Level rationale: spec-drafter `LEVEL_GUIDE.md` — "add / feature / 添加 / 功能" are Level 2 trigger words; single module (one skill), no architecture / cross-module / breaking change -> not Level 3; not a typo / format / config-only change -> not Level 1
- Rule #5 placement precedent: `openspec/changes/sibling-spec-probe/proposal.md`
- Rule #6 SOT: `standards/conventions/skill-benchmark-exemption.md`; operations manual: `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`
- Versioning: `standards/conventions/version-management.md`
