# Dark Mode Support

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-05
> **Linked Issue**: `none`

## Why

The dashboard UI ships one hard-coded palette. Today that palette happens to be dark
(`aria/skills/aria-dashboard/templates/dashboard.html:12-16` defines `--bg-primary: #0f1117`
and friends), which means "dark" is an implicit constant rather than a mode: users cannot
follow their OS appearance, cannot switch to a light palette for daylight/projector use, and
the theme cannot be tested or regressed because nothing selects it. Making dark an explicit,
switchable mode is cheap because the stylesheet is already fully tokenized with CSS custom
properties.

## What

Introduce an explicit theme layer with three states — `dark` (current look, stays the default),
`light`, and `system` (follow `prefers-color-scheme`) — plus a visible toggle in the dashboard
header and per-viewer persistence. No visual change to the default rendering.

### Key Deliverables

- `aria/skills/aria-dashboard/templates/dashboard.html` — split the existing `:root` token block
  into a light palette and a dark palette, selected by `[data-theme]` and by
  `@media (prefers-color-scheme: dark)`; today's values become the dark palette verbatim
- `aria/skills/aria-dashboard/templates/dashboard.html` — header theme toggle (dark / light /
  system) with an accessible label and keyboard operation
- `aria/skills/aria-dashboard/templates/dashboard.html` — inline pre-paint script that resolves
  the stored preference from `localStorage` before first paint (no flash of wrong theme), wrapped
  in try/catch so a browser that blocks site data still renders correctly
- `aria/skills/aria-dashboard/SKILL.md` — document the theme states and the persistence key

## Impact

| Type | Description |
|------|-------------|
| **Positive** | Dashboard becomes usable in daylight and matches OS appearance; the palette becomes a named, testable contract instead of an unlabeled constant |
| **Risk** | Token split can silently change the current dark rendering — mitigate by diffing the resolved dark values against today's `:root` block and requiring byte-identical color values for the dark state |
| **Risk** | Light palette can fail contrast requirements — mitigate by checking every text/background pair against WCAG AA (4.5:1) before merge |

## Tasks

- [ ] Extract the current `:root` token block into an explicit dark palette (values unchanged)
- [ ] Author the light palette and verify contrast on every text/background pair
- [ ] Add `[data-theme]` + `prefers-color-scheme` selection and the pre-paint resolver
- [ ] Add the header toggle (dark / light / system) with `localStorage` persistence
- [ ] Update `aria-dashboard` SKILL.md with the theme contract

## Success Criteria

- [ ] Default rendering (no stored preference, no OS preference) is byte-identical in color values
      to the pre-change dashboard — verified by diffing the resolved custom properties
- [ ] Toggling to light and back to dark restores the dark palette with no page reload
- [ ] Preference survives a reload and a dashboard regeneration; a browser with site data blocked
      still renders the default theme without a console error
- [ ] Every text/background pair in the light palette meets WCAG AA (>= 4.5:1)
- [ ] No flash of the wrong theme on first paint in either stored state

## Open Questions

- [ ] Target surface: this draft assumes the `aria-dashboard` generated HTML, the only UI surface
      in this repository. If the intended target is a different application, the module must be
      specified and the deliverables re-scoped (a multi-surface target would also raise this to
      Level 3 per the cross-module rule).
