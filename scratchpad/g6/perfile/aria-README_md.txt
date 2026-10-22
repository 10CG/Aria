> **Version**: 1.76.0 | **Released**: 2026-10-15
| `PostToolUse` + `PostToolUseFailure` | Bash\|Read\|Edit\|Write\|MultiEdit | **secret-scan.sh** | Rule #7 Layer 2 — detect secret-shaped output + warn (additionalContext/systemMessage); cannot redact (PostToolUse architectural limit), real defense = PreToolUse secret-guard, v1.24.0+ |
# Project-local sensitive paths (optional): <project root>/.aria/secret-guard.paths
# → one literal substring per line (case-insensitive, `#` starts a comment); it can only
#   ADD blocks on top of the built-in list
# → list the SHORTEST distinctive substring (e.g. a file name), not a full path
# → covers the readers of the built-in Forgejo/Gitea app.ini rule + Read/Edit; the Grep
#   tool is NOT covered
# → an invalid file (over 32 KiB, over 200 entries, unreadable) is ignored as a whole, silently

# → Claude Code 2.1.285's PostToolUse output schema lists updatedToolOutput — unverified end to end, unused by this hook
# PostToolUseFailure — the same scan runs on the error text of failed tool calls (non-zero exit)
