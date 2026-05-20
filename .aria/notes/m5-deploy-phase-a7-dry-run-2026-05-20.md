# M5 T-deploy Phase A.7 — Dry-run validation results

> **Created**: 2026-05-20 ~08:00 UTC (post Phase A.5 sign-off, opportunistic derisking pass)
> **Authority**: Phase A.7 (option (c) offered earlier, executed now after Phase A wrap commit)
> **Scope**: All zero prod write. Local HCL validation + migrations structure read + Nomad var existence check (no value read per Rule #7).

---

## §1 Phase B HCL validation (`nomad job validate` in dev container)

| HCL file | nomad validate | driver | constraint |
|----------|----------------|--------|-----------|
| `aria-layer1-cron.nomad.hcl` | ✅ Validation successful | `raw_exec` | `${node.class} = light_exec` |
| `aria-layer1-reconcile.nomad.hcl` | ✅ Validation successful | `raw_exec` | `${node.class} = light_exec` |
| `aria-layer1-comment-poll.nomad.hcl` (sanity, already deployed) | ✅ Validation successful | `raw_exec` | `${node.class} = light_exec` |

**Conclusion**: 2 new Layer 1 Nomad jobs (cron + reconcile) match the deployed sibling pattern (comment-poll) on every structural axis. Drop-in compatible.

## §2 ⚠ aria-orchestrator HCL disambiguation (CRITICAL Phase B trap)

| HCL file | driver | task name | live prod source? |
|----------|--------|-----------|-------------------|
| `aria-orchestrator.nomad.hcl` | **`docker`** | `hermes` | ❌ NOT prod (would flip driver) |
| **`aria-orchestrator-light.nomad.hcl`** | **`raw_exec`** | `hermes-gateway` | ✅ matches A.4 live inspect exactly |

**Phase B Trap**: If Phase B ever needs to re-run the orchestrator HCL (e.g., env block change), **MUST use `aria-orchestrator-light.nomad.hcl`**. Running `nomad job run aria-orchestrator.nomad.hcl` would flip the prod driver from raw_exec to docker. The plain `nomad job restart aria-orchestrator` (in v2 playbook Phase B Step 6) does NOT re-apply HCL — only stops + starts existing job — so v2 playbook Step 6 is safe as written.

**Mitigation**: Phase B playbook user (next session) must read this §2 before any `nomad job run` against aria-orchestrator.

## §3 Migration files structure (004/005/006)

All 3 migrations present in `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/migrations/`:

| Migration | Operation | Risk |
|-----------|-----------|------|
| `004_schema_v4_additive.sql` | ALTER TABLE ADD COLUMN (risk_tier, retry_count, 5 others) + CREATE UNIQUE INDEX `uq_dispatches_dispatch_id` + CREATE TABLE `dispatch_audit_log` (event_type CHECK + FK) + CREATE INDEX | Low — fully additive |
| `005_schema_v4_drop_inline_uq.sql` | DROP overstrict inline UNIQUE on `issue_id` via standard SQLite DROP CONSTRAINT workaround (CREATE TABLE new + copy + RENAME) + replace with `CREATE UNIQUE INDEX uq_issue_active_partial` | **Medium — full table rebuild**; expected since SQLite does not support `ALTER TABLE ... DROP CONSTRAINT`. Standard atomic pattern. |
| `006_schema_v4.2_add_spec_id.sql` | `ALTER TABLE dispatches ADD COLUMN spec_id TEXT` + `UPDATE schema_meta SET value='4.2'` | Low — fully additive |

**Total dispatches operations during Phase B Step 4** (against 16 prod rows):
- 7 ALTER ADD COLUMN (004 risk_tier+retry_count+others, 006 spec_id) — instant on 16 rows
- 1 full table copy (005 DROP inline UNIQUE) — instant on 16 rows
- 4 CREATE INDEX (004 audit FK + 005 partial UQ + 005 state indexes) — instant
- 1 CREATE TABLE (004 dispatch_audit_log)
- All wrapped per `schema_migrate.py` BA-2 fix (R1 M5 audit): atomic conn.execute loop with ALTER rollback

**16 dispatch row preservation**: 005's CREATE TABLE new + copy + RENAME is the riskiest. The copy step must transfer all 16 rows. **Phase B Step 4 must include post-migration row count assert** (`SELECT COUNT(*) FROM dispatches` → expected 16) before proceeding to Step 5.

## §4 Nomad Variable verification (Rule #7 — existence only, NOT values)

`nomad var list` on light-1 confirms:

```
- nomad/jobs/aria-build       (CreateTime ~2026-03-19, ModifyTime ~2026-04-15)
- nomad/jobs/aria-orchestrator (CreateTime ~2026-03-19, ModifyTime ~2026-05-19 — recent)
- ... (other unrelated vars)
```

**Nomad var `nomad/jobs/aria-orchestrator` exists** — the template source for `secrets/aria-layer1.env` rendered into all 3 Layer 1 raw_exec tasks (orchestrator/cron/reconcile/comment-poll). 

Both new HCL files (cron + reconcile) reference the **same Nomad var path**, so:
- ✅ no new var creation needed
- ✅ no new credentials needed (LUXENO_API_KEY / ARIA_FEISHU_WEBHOOK_URL / FORGEJO_BOT_PAT / FORGEJO_BOT_USER already in var per comment-poll's working state)
- ✅ var ModifyTime recent (last write 2026-05-19) — actively maintained

## §5 New env key `M1_VALIDATOR_PATH` (cron-only, non-blocker)

cron HCL adds a second template `secrets/aria-validator.env` and references new key `M1_VALIDATOR_PATH` from Nomad var (with `{{- with nomadVar "nomad/jobs/aria-orchestrator" }}{{ if .M1_VALIDATOR_PATH }}` conditional). If unset in Nomad var, falls through to env block default `/opt/aether-volumes/aria-layer1/data/validate-issue-schema.py`.

**Phase B impact**:
- ✅ job start NOT blocked even if Nomad var key + host file BOTH missing (template renders empty, env block default applies, validate-issue-schema.py file may not exist yet — only fails at validator call site inside cron tick logic)
- ⚠️ First cron tick may fail if tick logic invokes validator and host file missing
- **Recommended Phase B add-on**: after deploy step 6, before declaring cron "live", verify `/opt/aether-volumes/aria-layer1/data/validate-issue-schema.py` exists on light-1. If missing, either (a) install the file from source repo `aria_layer1/scripts/...` or (b) set Nomad var `M1_VALIDATOR_PATH=` to skip via guard logic in tick_runner.

(Not a Phase B blocker. Just an FYI for Step 7 smoke.)

## §6 Phase B derisking summary

| Risk area | Status |
|-----------|--------|
| HCL syntax (cron/reconcile) | ✅ both validate clean |
| HCL pattern match prod (driver / constraint / template / Nomad var path) | ✅ identical to sibling comment-poll |
| Submodule HCL ambiguity (docker vs raw_exec) | ⚠ FLAGGED — Phase B must use `-light.nomad.hcl`, `nomad job restart` safe |
| Migration structure 004/005/006 | ✅ standard SQLite patterns + atomic per file |
| Migration row preservation (16 prod) | ⚠ Phase B Step 4 must assert `COUNT(*) = 16` after 005 (table rebuild) |
| Nomad var `nomad/jobs/aria-orchestrator` | ✅ exists, recent ModifyTime |
| New env `M1_VALIDATOR_PATH` | ⚠ non-blocker; Phase B Step 7 add validator file existence check |
| Phase B prod-write commitment | unchanged from Phase A: ~2-3h dedicated session |

**Net effect**: 3 advisory items surfaced (§2 / §3 row count assert / §5 validator file). 0 blockers. Phase B can execute as drafted in v2 playbook §Phase B Step 1-8 + the 3 advisories above.

---

**Status**: Phase A.7 dry-run done. Phase B remains gated to next dedicated session.
