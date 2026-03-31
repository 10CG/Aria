# Feature Request: YAML Config File Support

## Submission Details

- **Repository**: https://github.com/10CG/Aria
- **Type**: Feature Request (GitHub Issue)
- **Suggested Label**: `enhancement`

---

## Proposed Issue

### Title

feat: Support YAML as an alternative config format alongside JSON

### Body

**Is your feature request related to a problem? Please describe.**

The current project-level configuration at `.aria/config.json` works well for simple settings, but as configurations grow more complex, JSON's limitations become apparent:

1. **No inline comments** -- JSON does not support comments. The current workaround is a `_comment` field at the top level, but this cannot annotate individual fields. For example, in the current `config.template.json`:

```json
{
  "_comment": "Aria project-level config -- all fields optional, unset uses defaults. Copy to config.json and modify.",
  "state_scanner": {
    "confidence_threshold": 90,
    "auto_execute_enabled": false,
    "auto_execute_rules": ["commit_only", "quick_fix", "doc_only"],
    "audit_log_path": ".aria/audit.log"
  }
}
```

Users cannot explain *why* they chose `confidence_threshold: 90` or which `auto_execute_rules` they excluded and why. This is especially painful for the `experiments` section where field-level context is crucial.

2. **Readability of nested structures** -- The config already has 6 top-level sections (`workflow`, `state_scanner`, `tdd`, `benchmarks`, `experiments`, and `version`). As the configuration surface grows, YAML's indentation-based syntax is easier to scan than JSON's brace-heavy nesting.

3. **Alignment with existing conventions** -- The `config-loader` Skill's own SKILL.md already uses YAML to document its validation rules. Many developers working with Claude Code and similar tools are already familiar with YAML from CI/CD configs, Kubernetes manifests, and similar tooling.

**Describe the solution you'd like**

Support `.aria/config.yaml` (or `.aria/config.yml`) as an alternative to `.aria/config.json`, with the following behavior:

1. **Discovery priority**: The `config-loader` Skill should look for config files in this order:
   - `.aria/config.yaml`
   - `.aria/config.yml`
   - `.aria/config.json`
   - If multiple exist, use the first found and emit a warning about the others being ignored.

2. **Provide a YAML template**: Add `.aria/config.template.yaml` alongside the existing `config.template.json`, with rich inline comments explaining each field:

```yaml
# Aria project-level configuration
# All fields are optional -- unset fields use defaults from DEFAULTS.json
version: "1.0"

workflow:
  # Whether to auto-proceed through workflow steps without user confirmation
  auto_proceed: false

state_scanner:
  # Minimum confidence (0-100) required for auto-execution recommendations
  confidence_threshold: 90

  # Enable automatic execution of high-confidence recommendations
  auto_execute_enabled: false

  # Which recommendation types can be auto-executed
  # Valid values: commit_only, quick_fix, doc_only, feature_with_spec
  auto_execute_rules:
    - commit_only
    - quick_fix
    - doc_only

  # Path for the audit log (relative to project root)
  audit_log_path: ".aria/audit.log"

tdd:
  # TDD enforcement level: advisory | strict | superpowers
  strictness: advisory

benchmarks:
  # Require skill benchmarks before merging skill changes
  require_before_merge: true

  # How to handle missing benchmarks: warn | block | off
  skill_change_block_mode: warn

experiments:
  # Enable Agent Team audit at integration points
  agent_team_audit: false

  # When to run Agent Team audits
  # Valid values: pre_merge, post_implementation, post_spec
  agent_team_audit_points:
    - pre_merge
```

3. **Update config-loader**: Modify the `config-loader` Skill (`aria/skills/config-loader/SKILL.md`) to handle YAML parsing:
   - Update the loading flow (Section "Loading Flow") to include YAML discovery
   - Add a YAML parse error scenario to the error handling table
   - Document the priority order when both formats exist

4. **Backward compatibility**: `.aria/config.json` continues to work exactly as before. This is purely additive -- no breaking changes.

**Describe alternatives you've considered**

- **JSONC (JSON with Comments)**: Would solve the comment problem but is not as widely standardized. Many parsers don't support it natively.
- **TOML**: More structured than YAML but less familiar to the target audience (developers using Claude Code, CI/CD tools, etc.).
- **JSON5**: Supports comments and trailing commas, but has a smaller ecosystem than YAML.
- **Keep JSON only**: Users can use the `_comment` field convention, but this does not scale to per-field annotations and clutters the config structure.

**Affected components**

| Component | File/Path | Change Required |
|-----------|-----------|-----------------|
| Config loader Skill | `aria/skills/config-loader/SKILL.md` | Update discovery logic, add YAML parsing flow |
| Defaults | `aria/skills/config-loader/DEFAULTS.json` | No change (format-agnostic) |
| Config template | `.aria/config.template.json` | No change (keep as-is) |
| New YAML template | `.aria/config.template.yaml` | New file |
| CLAUDE.md | `CLAUDE.md` | Update references to mention both formats |
| Consumer Skills | Various (state-scanner, tdd-enforcer, etc.) | No change (they consume parsed config objects, not raw files) |

**Impact assessment**

- **Scope**: This affects the `config-loader` internal infrastructure Skill and the `.aria/` project configuration directory.
- **Risk**: Low -- purely additive, no existing behavior changes.
- **Effort estimate**: Small (4-8 hours), aligning with Aria's incremental iteration principle.
- **OpenSpec level**: Level 2 (Minimal) -- a `proposal.md` should suffice given the limited scope.

**Additional context**

This aligns well with Aria's core principles:
- **Backward Compatible**: JSON config continues to work unchanged.
- **Docs in Sync**: The YAML template itself serves as living documentation with inline comments.
- **Spec First**: This request proposes a clear scope before any implementation work.

The `config-loader` Skill currently only reads files via the `Read` and `Glob` tools (as declared in its frontmatter `allowed-tools`), and parses JSON in-prompt. YAML parsing would follow the same pattern -- the Skill reads the raw file content and interprets the YAML structure. No new tool dependencies are required.

---

## How to Submit

To file this as a GitHub Issue, run:

```bash
gh issue create \
  --repo 10CG/Aria \
  --title "feat: Support YAML as an alternative config format alongside JSON" \
  --label "enhancement" \
  --body-file /path/to/this/file.md
```

Or navigate to https://github.com/10CG/Aria/issues/new and paste the content above (from "Is your feature request related to a problem?" onward) into the issue body.
