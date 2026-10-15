#!/usr/bin/env python3
"""Apply a minimal 'target-state' documentation change to the prototype trees so that the doc-sync rows
(SC-26 / SC-27 / SC-28) can be exercised as 'yes'.  Not a real doc change: the sentences are only as long as the checks need.
usage: python3 patch_docs.py <proto dir> [--bad | --bad-sot | --bad-layer | --no-scope | --hdr-count | --hdr-half-l | --hdr-dangling | --hdr-half-a | --hdr-argon | --hdr-topcontent | --hdr-nohist]
  --bad      the 'token stuffing' bad implementation: facts only in the SOT version-history row, no other document patched
  --bad-sot  the same SOT stuffing, but README / CHANGELOG / hook headers / VERSION patched normally (the case the SC-26 text names)
  --bad-layer  everything patched normally, but the new SOT clause uses this Spec's layer numbers L1 / L3 (SC-26 26i)
  --no-scope   everything patched normally, but the secret-scan.sh header Scope list does not name the 6 new tags (SC-28 28n)
  --hdr-count  everything patched normally, but the secret-scan.sh header gains a NEW pattern / tag count literal (SC-28 28c / 28d)
  --hdr-half-l everything patched normally, but the secret-scan.sh header keeps the first half of the stale sentence `Claude Code exposes no field to replace tool_response` (SC-28 28l)
  --hdr-dangling  everything patched normally, but the secret-guard.sh header re-points the dangling runbook reference at a section of secret-hygiene.md that does not exist (`§1.3`) (SC-28 28b)
  --hdr-half-a  everything patched normally, but the secret-guard.sh header only rewrites the FIRST line of the stale three-line sentence and keeps `... style env lines + redacts —` (SC-28 28a)
  --hdr-argon   everything patched normally, but the secret-scan.sh header still claims argon2 hashes in other words (`bcrypt password hashes, argon2 too`) (SC-28 28e)
  --hdr-topcontent  everything patched normally, but the secret-scan.sh contract keeps a top-level `"content"` key line and only mentions file.content in its comment (SC-28 28f)
  --hdr-nohist  everything patched normally, but the secret-guard.sh History block gets no entry (the change-id appears only in a code comment of the prototype) (SC-28 28j)
  --cl-drop=MARKER  everything patched normally, but the CHANGELOG sentence does not hold the marker word MARKER (SC-26 26g: one marker per disclosure of the Impact section)
  --hdr-count also rewrites the secret-guard.sh header line 8 with a new count literal (`~110 most common patterns`) (SC-28 28o)"""
import os
import re
import sys

root = sys.argv[1]
bad_sot = "--bad-sot" in sys.argv
bad_layer = "--bad-layer" in sys.argv
no_scope = "--no-scope" in sys.argv
hdr_count = "--hdr-count" in sys.argv
hdr_half_l = "--hdr-half-l" in sys.argv
hdr_dangling = "--hdr-dangling" in sys.argv
hdr_half_a = "--hdr-half-a" in sys.argv
hdr_argon = "--hdr-argon" in sys.argv
hdr_topcontent = "--hdr-topcontent" in sys.argv
hdr_nohist = "--hdr-nohist" in sys.argv
cl_drop = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--cl-drop=")), "")
bad = "--bad" in sys.argv or bad_sot
A, S = os.path.join(root, "aria"), os.path.join(root, "standards")


def rw(path, fn):
    t = open(path, encoding="utf-8").read()
    t2 = fn(t)
    assert t2 != t, path
    open(path, "w", encoding="utf-8").write(t2)


def sub1(t, old, new):
    assert t.count(old) == 1, (t.count(old), old[:70])
    return t.replace(old, new, 1)


def sot(t):
    if bad:
        # facts stuffed into the version history table only
        return t.rstrip("\n") + "\n| 1.2.0 | 2026-10-01 | 命令行参数 env --config stdin 长时 存活期 60 秒 pgrep -a Acceptable filters .aria/secret-guard.paths 字面子串 只增不减 32 KiB 200 整体忽略 静默 大小写不敏感 CLAUDE_PROJECT_DIR app.ini updatedToolOutput |\n"
    # 2.2 row
    t = sub1(t, "| Show env | `env`, `printenv`, `set` (含 secret env vars 时) |\n",
             "| Show env | `env`, `printenv`, `set` (含 secret env vars 时) |\n| Read server-side config | `cat`/`grep`/`sed` 等读 Forgejo / Gitea `app.ini` (JWT_SECRET / SECRET_KEY / 数据库口令) |\n")
    # 2.5 rows + the tight-family note
    t = sub1(t, "| Cluster status | `aether status --json` (若 wrap 上述) |\n",
             "| Cluster status | `aether status --json` (若 wrap 上述) |\n| Process table | `ps aux` / `ps -ef` / `pgrep -a` / `top -c` / `/proc/<pid>/cmdline` 与 `environ` (命令行参数里的凭据在进程存活期内可见) |\n")
    t = sub1(t, "> **原则**: 任何输出 contains secret value 的命令 = 受限命令",
             "> **注**: 进程表族 / `app.ini` 族 / 扩展条目按 tight credit 判, 共用 BLOCKED 文案里列出的 `Acceptable filters` (如 `| grep '^SAFE_PREFIX='`) 对这些族无效。\n\n> **原则**: 任何输出 contains secret value 的命令 = 受限命令")
    # 3.8
    new38 = ("### 3.8 长时进程的凭据传递\n\n"
             "长时进程 (后台轮询 / 守护 / watch 循环; 无超时上界, 或预期存活期不少于 60 秒) 的**命令行参数**不得含凭据: 进程表在其存活期内一直可被枚举。改用 env / `--config` 文件 / stdin。"
             "短命令 (预期存活期不足 60 秒) 的 argv 暴露窗口只在其执行期, §3.1-§3.5 与 §4.4 的 `KEY=...` 示例属此类, 保持不变。" + (" 本条对应 L1 / L3 两层。" if bad_layer else "") + "\n\n---\n")
    t = sub1(t, "\n---\n\n## 4. 反例", "\n\n" + new38 + "\n## 4. 反例")
    # 5.6
    new56 = ("### 5.6 项目级扩展入口 `.aria/secret-guard.paths`\n\n"
             "位于项目根 (`CLAUDE_PROJECT_DIR`, 否则 stdin 的 `cwd`)。一行一个**字面子串** (大小写不敏感, 不是正则), `#` 起首为注释; 4-200 字符且含字母或数字才生效; 只增不减: 不能放宽任何内建规则; "
             "文件缺失 / 非普通文件 / 不可读 / 超过 32 KiB / 含 NUL / 有效条目超过 200 条 => 整体忽略扩展 (内建名单照常), 且失效是静默的。\n\n")
    t = sub1(t, "\n---\n\n## 6. Local copy", "\n\n" + new56 + "---\n\n## 6. Local copy")
    # 5.1 (blocker wording + the guard-suite row lists the new families) and 5.2 (additive schema fact)
    t = sub1(t, "PreToolUse Bash + Read/Edit/Write/MultiEdit blocker", "PreToolUse Bash + Read/Edit blocker")
    t = sub1(t, "#179 claude-config 双平面清单 + credit 收紧 + 前置字符白名单)",
             "#179 claude-config 双平面清单 + credit 收紧 + 前置字符白名单; secret-net-l3-and-bypass-paths: `app.ini` 族 / 进程表族 / 扩展入口)")
    t = sub1(t, "**唯一可靠防线 = PreToolUse `secret-guard`**(事前 block)。",
             "**唯一可靠防线 = PreToolUse `secret-guard`**(事前 block)。补充事实: Claude Code 2.1.285 的 PostToolUse schema 含 `updatedToolOutput`, 端到端未验证, 本 hook 不使用。")
    # secret-scan count (the header count is now an assertion that counts itself: 49 + 1)
    t = sub1(t, "| `aria/hooks/tests/secret-scan.test.sh` | 49 regression cases | n/a |", "| `aria/hooks/tests/secret-scan.test.sh` | 50 regression cases | n/a |")
    # version + history
    t = sub1(t, "> **Version**: 1.1.2", "> **Version**: 1.2.0")
    t = sub1(t, "| 1.1.2 | 2026-08-02 |", "| 1.2.0 | 2026-10-01 | **Additive**: §2.2 `app.ini` 行 / §2.5 进程表行 / §3.8 长时进程凭据传递 / §5.1 勘正 / 新增 §5.6 项目级扩展入口; 来源: Spec secret-net-l3-and-bypass-paths。 |\n| 1.1.2 | 2026-08-02 |")
    return t


rw(os.path.join(S, "conventions", "secret-hygiene.md"), sot)


def readme(t, head, line):
    i = t.rindex(head)
    return t[:i] + t[i:].replace("```bash\n", "```bash\n" + line + "\n", 1)


if not bad or bad_sot:
    rw(os.path.join(A, "README.md"), lambda t: readme(t, "### Hooks (Auto-triggered)", "# Project-local sensitive paths: .aria/secret-guard.paths (one literal substring per line); PostToolUse schema lists updatedToolOutput (unverified, unused)"))
    rw(os.path.join(A, "README.zh.md"), lambda t: readme(t, "### Hooks 自动触发", "# 项目级敏感路径: .aria/secret-guard.paths (一行一个字面子串); PostToolUse schema 含 updatedToolOutput (未验证, 不使用)"))
    _CL = "rule6_note: substitute. `.aria/secret-guard.paths` is a new input; `ps aux` and /proc listings and `app.ini` reads are now blocked; Read results (file.content) are scanned for the first time and the new kv-secret-assign tag alerts; placeholder values are now silent; os.environ single-key reads and keys_unsorted are now allowed; the log gains an fp= field; the extra scanning costs CPU; variable indirection is a partial fix."
    _DROP = {"rule6_note": ("rule6_note", "rule 6 note"), ".aria/secret-guard.paths": ("`.aria/secret-guard.paths`", "the project extension file"), "ps aux": ("`ps aux`", "`pgrep -a`"),
             "/proc": ("/proc", "process-table"), "app.ini": ("`app.ini`", "server configuration"), "file.content": ("(file.content) ", ""), "kv-secret-assign": ("kv-secret-assign", "new key-shape"),
             "placeholder": ("placeholder", "dummy"), "os.environ": ("os.environ", "environment"), "keys_unsorted": ("keys_unsorted", "unsorted-key listings"), "fp=": ("an fp= field", "a fingerprint field"),
             "CPU": ("costs CPU", "costs time"), "partial": ("a partial fix", "a fix for some forms")}
    if cl_drop:
        _a, _b = _DROP[cl_drop]
        assert _a in _CL, cl_drop
        _CL = _CL.replace(_a, _b, 1)
        assert cl_drop not in _CL, cl_drop
    rw(os.path.join(A, "CHANGELOG.md"), lambda t: re.sub(r"(?m)^## ", "## [Unreleased]\n\n" + _CL.replace("\\", "\\\\") + "\n\n## ", t, count=1))

    def guard_hdr(t):
        if hdr_half_a:
            t = sub1(t, "Phase 2 would add PostToolUse hook\n#     that regex-scans output for `^[A-Z_]+=.+$` style env lines + redacts —\n#     out of scope for current implementation.",
                     "L3 detect+warn lives in the PostToolUse hook secret-scan.sh,\n#     that regex-scans output for `^[A-Z_]+=.+$` style env lines + redacts —\n#     out of scope for current implementation.")
        else:
            t = sub1(t, "Phase 2 would add PostToolUse hook\n#     that regex-scans output for `^[A-Z_]+=.+$` style env lines + redacts —\n#     out of scope for current implementation.",
                     "L3 detect+warn lives in the PostToolUse hook secret-scan.sh.")
        t = sub1(t, "It covers the ~100\n#   most common patterns: cloud secret managers", ("It covers the ~110\n#   most common patterns: cloud secret managers" if hdr_count else "It covers the\n#   most common patterns: cloud secret managers"))
        t = sub1(t, "docs/operations/secret-rotation-runbook.md \u00a71.3 principles", "standards/conventions/secret-hygiene.md \u00a71.3 principles" if hdr_dangling else "standards/conventions/secret-hygiene.md \u00a71 principles")
        if hdr_nohist:
            return t
        return sub1(t, "# === History ===\n", "# === History ===\n#   secret-net-l3-and-bypass-paths: .aria/secret-guard.paths (project extension); variable indirection is only partly covered; the shared BLOCKED text lists Acceptable filters that do not apply to the tight families; residual gaps: systemctl status, docker inspect\n")
    rw(os.path.join(A, "hooks", "secret-guard.sh"), guard_hdr)

    def scan_hdr(t):
        t = sub1(t, "(49 known bypass classes; effective prevention)", "(effective prevention)")
        t = sub1(t, "(~15 secret-shape patterns; detect + warn only)", "(detect + warn only)")
        t = sub1(t, "#   - bcrypt / argon2 password hashes", ("#   - bcrypt password hashes, argon2 too" if hdr_argon else "#   - bcrypt password hashes") + ("" if no_scope else "\n#   - key-shape tags: json-credential-field json-env-secret-key kv-secret-assign auth-header-token cf-access-client-secret cli-secret-flag"))
        if hdr_topcontent:
            t = sub1(t, "#       \"content\": \"...\"        // Read file content", "#       \"content\": \"...\",       // Read: tool_response.file.content too")
        else:
            t = sub1(t, "#       \"content\": \"...\"        // Read file content", "#       \"file\": {\"content\": \"...\"}   // Read: tool_response.file.content")
        t = sub1(t, "# - Secrets encoded base64 / hex / etc (without telltale prefix)", "# - Secrets encoded base64 / hex / etc (without telltale prefix AND without a credential key name)")
        if hdr_half_l:
            t = sub1(t, "This is an architectural limit, not a\n# version-dependent behaviour.", "The 2.1.285 schema lists updatedToolOutput (unverified end to end, unused here).")
        else:
            t = sub1(t, "the tool result has already been produced: Claude Code exposes no field to\n# replace tool_response, and hook stdout does not substitute the captured\n# result (official hooks-guide line 891: \"PostToolUse hooks can't undo actions\n# since the tool has already executed\"). This is an architectural limit, not a\n# version-dependent behaviour.",
                     "the tool result has already been produced: hook stdout does not substitute the\n# captured result (official hooks-guide line 891: \"PostToolUse hooks can't undo\n# actions since the tool has already executed\"). The 2.1.285 schema lists\n# updatedToolOutput (unverified end to end, unused here).")
        if hdr_count:
            t = sub1(t, "(detect + warn only)", "(detect + warn only; 37 patterns, ~12 key-shape forms, 6 new tags)")
        return sub1(t, "# === Threat model ===", "# change-id: secret-net-l3-and-bypass-paths\n#\n# === Threat model ===")
    rw(os.path.join(A, "hooks", "secret-scan.sh"), scan_hdr)
    rw(os.path.join(A, "VERSION"), lambda t: sub1(t, "output REDACT", "detect + warn"))
print("docs patched", "(bad-sot)" if bad_sot else ("(bad)" if bad else ""))
