# Kairos — Aria Cross-Project Pilot

> **Selected**: 2026-04-01
> **Status**: Planning
> **Parent**: US-002 (Cross-Project Methodology Validation)

## Project Profile

| Attribute | Value |
|-----------|-------|
| Name | Kairos |
| Type | AI-driven private domain sales automation |
| Tech Stack | TypeScript / Node.js / Vitest |
| Codebase | ~58,000 lines, 1434 tests (86 files) |
| Development | Very active (246 commits in 30 days) |
| Deployment | Forgejo Actions + Nomad (Aether cluster) |
| Team | Solo developer |

## Current Aria Adoption (Partial)

| Component | Status |
|-----------|--------|
| CLAUDE.md | Yes — project context + deployment rules |
| OpenSpec | Yes — `openspec/changes/` + `openspec/archive/` (10+ specs archived) |
| UPM | Yes — `UPM.md` with UPMv2-STATE YAML block |
| Ten-Step Cycle | Partially — uses OpenSpec flow but no automated Phase Skills |
| aria-plugin | **Not installed** |
| standards/ submodule | **Not installed** |
| .aria/config.json | **Not present** |
| AB benchmarks | **Not present** |

## Why Kairos

1. **Partial adoption** — already uses OpenSpec/UPM, validates "upgrade to full" path
2. **Different domain** — sales automation vs methodology research
3. **Real codebase** — 58K LOC, real business logic, not a demo
4. **Active development** — 2 active OpenSpecs, ongoing feature work
5. **No plugin** — tests whether automated Skills add value over manual workflow

## Pilot Plan

### Phase 1: Setup (in Kairos project)
- Install aria-plugin
- Optionally add standards/ submodule
- Create .aria/config.json

### Phase 2: Exercise (pick one pending feature)
- Run `/aria:state-scanner` to assess current state
- Walk through a complete ten-step cycle using Skills
- Compare experience to Kairos's current manual OpenSpec workflow

### Phase 3: Benchmark
- Create Kairos-specific eval cases (commit-msg, state-scanner, spec-drafter)
- Run AB tests via /skill-creator
- Measure delta vs without_skill

### Phase 4: Report
- Complete Adaptation Log
- Submit Adoption Report via Issue Template
- Update US-002 with findings
