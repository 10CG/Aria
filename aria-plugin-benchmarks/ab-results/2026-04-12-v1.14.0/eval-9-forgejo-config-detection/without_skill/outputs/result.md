# Forgejo Configuration Detection - Project State Scan

## 1. Git Remote Configuration

| Remote | URL | Purpose |
|--------|-----|---------|
| `origin` | `ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git` | Primary (Forgejo) |
| `github` | `git@github.com:10CG/Aria.git` | Mirror (GitHub) |

**Status**: Origin correctly points to Forgejo at `forgejo.10cg.pub`. The default push/pull target is the Forgejo instance.

## 2. CLAUDE.local.md Status

**CLAUDE.local.md does NOT exist** at the project root (`/home/dev/Aria/CLAUDE.local.md`).

This is a configuration gap. The `CLAUDE.local.md` file is the expected location for project-local Forgejo API configuration that should not be committed to the repository (machine-specific settings like API URLs, repo identifiers, and Cloudflare Access flags).

Note: `.claude/local.md` exists at `/home/dev/Aria/.claude/local.md`, but this is a different file -- it contains general workflow instructions, not Forgejo API configuration.

## 3. Environment Variables (Forgejo API)

| Variable | Status |
|----------|--------|
| `FORGEJO_TOKEN` | SET (40 chars) |
| `CF_ACCESS_CLIENT_ID` | SET (39 chars) |
| `CF_ACCESS_CLIENT_SECRET` | SET (64 chars) |
| `FORGEJO_API` | SET (`https://forgejo.10cg.pub/api/v1`) |

**All required environment variables are present.** The `forgejo` CLI wrapper at `/home/dev/.npm-global/bin/forgejo` is installed and functional.

## 4. Forgejo API Connectivity Test

**API connectivity is WORKING.** A test call to `GET /repos/10CG/Aria` returned valid JSON with full repository metadata. The internal network route (`192.168.69.200:3000`) is reachable, so API calls do not need to traverse Cloudflare Access.

Open issues were also successfully retrieved (1 open issue: #5 - Pulse project integration).

## 5. Aria Config (.aria/config.json)

The `.aria/config.json` already has Forgejo-aware settings:

```json
"issue_scan": {
  "enabled": true,
  "platform": "forgejo",
  "platform_hostnames": {
    "forgejo": ["forgejo.10cg.pub"],
    "github": ["github.com"]
  }
}
```

This means the state-scanner's issue scanning feature is enabled and configured for Forgejo.

## 6. Submodule Status

| Submodule | Status |
|-----------|--------|
| `aria` | `1a29d15` (v1.6.0-47-g1a29d15) |
| `aria-orchestrator` | `f051a7d` (heads/master) |
| `standards` | `af300d5` (remotes/origin/HEAD) |

All submodules are checked out. No detached or missing submodules.

## 7. Identified Gap: Missing CLAUDE.local.md

The project has a Forgejo remote configured, environment variables set, and API connectivity working, but **lacks a `CLAUDE.local.md`** file with the `forgejo:` configuration block. This file is referenced by multiple skills (forgejo-sync, state-scanner, branch-manager) as the expected location for Forgejo integration metadata.

Without this file, skills that need Forgejo API access (like `forgejo-sync` for syncing User Stories to Issues, or `branch-manager` for PR operations) will either:
- Fall back to auto-detection (less reliable)
- Prompt you to create the configuration on first use
- Fail when Cloudflare Access headers are needed but not configured

## 8. How to Set Up Forgejo Integration

Create a `CLAUDE.local.md` file at the project root (`/home/dev/Aria/CLAUDE.local.md`) with the following content:

```yaml
forgejo:
  url: "https://forgejo.10cg.pub"
  api_token: "${FORGEJO_TOKEN}"
  repo: "10CG/Aria"

  cloudflare_access:
    enabled: true
    client_id_env: "CF_ACCESS_CLIENT_ID"
    client_secret_env: "CF_ACCESS_CLIENT_SECRET"

  default_labels: ["user-story"]
  wiki:
    enabled: true
    page_prefix: "PRD-"
```

**Important notes:**
- `CLAUDE.local.md` is NOT in `.gitignore` currently. Since it contains no secrets (only environment variable references, not actual values), this is by design -- the forgejo configuration block is safe to commit. However, if you prefer to keep it local-only, add `CLAUDE.local.md` to `.gitignore`.
- The `forgejo` CLI wrapper (`/home/dev/.npm-global/bin/forgejo`) already handles the dual-path routing (internal 192.168.69.200:3000 first, external via Cloudflare Access as fallback). The `CLAUDE.local.md` configuration is primarily for Aria skills that make their own API calls.
- Environment variables (`FORGEJO_TOKEN`, `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET`) are already set in your shell environment.

## 9. Summary

| Component | Status |
|-----------|--------|
| Git remote (origin -> Forgejo) | OK |
| `forgejo` CLI wrapper | OK (installed, functional) |
| Environment variables | OK (all 3 set) |
| API connectivity | OK (internal route works) |
| `.aria/config.json` issue_scan | OK (enabled, platform=forgejo) |
| `CLAUDE.local.md` with `forgejo:` block | **MISSING** |
| Submodules | OK |

**The only missing piece is `CLAUDE.local.md`.** Everything else needed for Forgejo integration is already in place and working. Creating this file will enable Aria skills (forgejo-sync, state-scanner, branch-manager) to use Forgejo API features without falling back to auto-detection or prompting you each time.
