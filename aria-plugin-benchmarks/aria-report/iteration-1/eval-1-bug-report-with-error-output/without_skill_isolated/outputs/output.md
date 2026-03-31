# Bug Report: state-scanner crashes with "Cannot read property phases of undefined"

Below is a ready-to-submit bug report for the Aria maintenance team. You can file it as a GitHub Issue on [10CG/aria-plugin](https://github.com/10CG/aria-plugin/issues/new) or, if you have internal Forgejo access, on `10CG/Aria`.

---

## Issue Title

`state-scanner: crashes with "Cannot read property phases of undefined" when config exists`

---

## Issue Body

### Bug Report

**Skill**: `state-scanner`
**Plugin Version**: v1.8.0 (aria-plugin)
**OS**: macOS
**Claude Code**: (please fill in your Claude Code version -- run `claude --version` to check)

### Description

Running `/state-scanner` (or any workflow that triggers state-scanner) crashes midway through execution with the following error:

```
Cannot read property phases of undefined
```

The skill exits immediately after the error -- no partial output is returned, no recovery is attempted.

### Steps to Reproduce

1. Have a project with `.aria/config.json` present and properly configured.
2. Invoke the state-scanner skill (e.g., `/state-scanner` or any workflow that triggers it such as "check project status").
3. The skill begins scanning, then crashes partway through with the error above.

### Expected Behavior

The state-scanner should complete all scan phases (git status, branch analysis, config detection, README sync check, plugin dependency detection, etc.) and produce a status summary with workflow recommendations.

### Actual Behavior

The skill starts execution, runs partially, then throws:

```
Cannot read property phases of undefined
```

and terminates without producing any output or recommendations.

### Environment

| Item | Value |
|------|-------|
| OS | macOS |
| aria-plugin version | v1.8.0 |
| `.aria/config.json` present | Yes |
| Claude Code version | (fill in) |
| Project type | (fill in -- e.g., Node.js, Python, etc.) |

### Configuration

The `.aria/config.json` file exists in the project root. If your config was copied from `config.template.json`, the relevant section looks like:

```json
{
  "state_scanner": {
    "confidence_threshold": 90,
    "auto_execute_enabled": false,
    "auto_execute_rules": ["commit_only", "quick_fix", "doc_only"],
    "audit_log_path": ".aria/audit.log"
  }
}
```

Please paste your actual `.aria/config.json` content here (redact any sensitive values):

```json
(paste your config here)
```

### Analysis / Possible Cause

The error message `Cannot read property phases of undefined` suggests that somewhere in the state-scanner logic, code accesses `.phases` on an object that is `undefined`. Likely scenarios:

1. **Config structure mismatch**: The skill expects a specific nested structure (e.g., `config.workflow.phases` or `config.state_scanner.phases`) that is not present in the user's config file. The config-loader may return a merged config object where a parent key exists but the `phases` sub-key does not.

2. **Missing default value**: The config-loader skill (v1.7.0+) is supposed to merge user config with defaults. If the `phases` property was added in a newer version of the skill but the default-merging logic does not account for it, the property could be `undefined`.

3. **Schema evolution**: The config template (`config.template.json`) does not include a `phases` field. If state-scanner was recently updated to reference `phases` from config without updating the template or the default values, projects with older configs would hit this error.

### Additional Context

- The `.aria/config.json` file **is present** -- this is not a missing-config issue.
- The error occurs midway through execution, meaning earlier scan phases complete successfully before the crash.
- The state-scanner has been working in previous plugin versions (pre-1.8.0).

### Labels

`bug`, `state-scanner`, `config-loader`

---

## How to Submit

**Option A -- GitHub (recommended for public projects)**

Go to: https://github.com/10CG/aria-plugin/issues/new

- Title: `state-scanner: crashes with "Cannot read property phases of undefined" when config exists`
- Body: Copy everything under "Issue Body" above.
- Labels: `bug`

**Option B -- Forgejo (internal)**

If you have access to the internal Forgejo instance:

```bash
forgejo POST /repos/10CG/Aria/issues -d '{
  "title": "state-scanner: crashes with \"Cannot read property phases of undefined\" when config exists",
  "body": "(paste the issue body here)",
  "labels": [0]
}'
```

**Option C -- If you have the aria-plugin installed (v1.8.0+)**

You can use the new `aria-report` skill:

```
/aria:aria-report
```

This will interactively collect environment info and submit the issue for you.

---

## Before Submitting -- Checklist

- [ ] Confirm your `.aria/config.json` is valid JSON (run `python3 -m json.tool .aria/config.json` or `jq . .aria/config.json`)
- [ ] Note your exact Claude Code version (`claude --version`)
- [ ] Note your macOS version (`sw_vers`)
- [ ] Paste your actual `.aria/config.json` content (redacted if needed) into the report
- [ ] If possible, note which scan phase was the last to produce output before the crash
