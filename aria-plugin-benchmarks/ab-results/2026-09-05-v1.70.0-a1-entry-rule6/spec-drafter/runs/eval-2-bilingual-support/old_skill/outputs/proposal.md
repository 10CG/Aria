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
