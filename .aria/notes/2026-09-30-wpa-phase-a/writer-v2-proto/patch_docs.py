#!/usr/bin/env python3
"""Apply a minimal 'target-state' documentation change to the prototype trees so that the doc-sync rows
(SC-26 / SC-28) can be exercised as 'yes'.  Not a real doc change: the sentences are only as long as the checks need.
usage: python3 patch_docs.py <proto dir> [--bad]    (--bad = the 'token stuffing' bad implementation: facts only in the wrong places)"""
import os, re, sys

root = sys.argv[1]
bad = "--bad" in sys.argv
A, S = os.path.join(root, "aria"), os.path.join(root, "standards")


def rw(path, fn):
    t = open(path, encoding="utf-8").read()
    t2 = fn(t)
    assert t2 != t, path
    open(path, "w", encoding="utf-8").write(t2)


def sot(t):
    if bad:
        # facts stuffed into the version history table only
        return t.rstrip("\n") + "\n| 1.2.0 | 2026-10-01 | 命令行参数 env --config stdin 长时 存活期 pgrep -a .aria/secret-guard.paths 字面子串 只增不减 32 KiB 200 整体忽略 app.ini |\n"
    # 2.2 row
    t = t.replace("| Show env | `env`, `printenv`, `set` (含 secret env vars 时) |\n",
                  "| Show env | `env`, `printenv`, `set` (含 secret env vars 时) |\n| Read server-side config | `cat`/`grep`/`sed` 等读 Forgejo / Gitea `app.ini` (JWT_SECRET / SECRET_KEY / 数据库口令) |\n", 1)
    # 2.5 rows
    t = t.replace("| Cluster status | `aether status --json` (若 wrap 上述) |\n",
                  "| Cluster status | `aether status --json` (若 wrap 上述) |\n| Process table | `ps aux` / `ps -ef` / `pgrep -a` / `top -c` / `/proc/<pid>/cmdline` 与 `environ` (命令行参数里的凭据在进程存活期内可见) |\n", 1)
    # 3.8
    new38 = ("### 3.8 长时进程的凭据传递\n\n"
             "长时进程 (后台轮询 / 守护 / watch 循环, 存活期超过数秒) 的**命令行参数**不得含凭据: 进程表在其存活期内一直可被枚举。改用 env / `--config` 文件 / stdin。"
             "短命令 (秒级) 的 argv 暴露窗口只在其执行期, §3.1-§3.5 与 §4.4 的 `KEY=...` 示例属此类, 保持不变。\n\n---\n")
    t = t.replace("\n---\n\n## 4. 反例", "\n\n" + new38 + "\n## 4. 反例", 1) if "\n---\n\n## 4. 反例" in t else t
    # 5.6
    new56 = ("### 5.6 项目级扩展入口 `.aria/secret-guard.paths`\n\n"
             "一行一个**字面子串** (大小写不敏感, 不是正则), `#` 起首为注释; 4-200 字符且含字母或数字才生效; 只增不减: 不能放宽任何内建规则; "
             "文件缺失 / 非普通文件 / 不可读 / 超过 32 KiB / 含 NUL / 有效条目超过 200 条 => 整体忽略扩展 (内建名单照常), 且失效是静默的。\n\n")
    t = t.replace("### 5.5 ", new56 + "### 5.5 ", 1) if False else t.replace("\n---\n\n## 6. Local copy", "\n\n" + new56 + "---\n\n## 6. Local copy", 1)
    # 5.1
    t = t.replace("PreToolUse Bash + Read/Edit/Write/MultiEdit blocker", "PreToolUse Bash + Read/Edit blocker", 1)
    return t


rw(os.path.join(S, "conventions", "secret-hygiene.md"), sot)


def readme(t, head, line):
    i = t.rindex(head)
    j = t.index("```bash", i)
    return t[:j] + "```bash\n" + line + "\n" + t[j + len("```bash\n"):] if False else t[:i] + t[i:].replace("```bash\n", "```bash\n" + line + "\n", 1)


if not bad:
    rw(os.path.join(A, "README.md"), lambda t: readme(t, "### Hooks (Auto-triggered)", "# Project-local sensitive paths: .aria/secret-guard.paths (one literal substring per line)"))
    rw(os.path.join(A, "README.zh.md"), lambda t: readme(t, "### Hooks 自动触发", "# 项目级敏感路径: .aria/secret-guard.paths (一行一个字面子串)"))
    rw(os.path.join(A, "CHANGELOG.md"), lambda t: re.sub(r"(?m)^## ", "## [Unreleased]\n\nrule6_note: substitute. `.aria/secret-guard.paths` is a new input; `ps aux` is now blocked.\n\n## ", t, count=1))

    def guard_hdr(t):
        t = t.replace("Phase 2 would add PostToolUse hook\n#     that regex-scans output for `^[A-Z_]+=.+$` style env lines + redacts —\n#     out of scope for current implementation.",
                      "L3 detect+warn lives in the PostToolUse hook secret-scan.sh.", 1)
        t = t.replace("docs/operations/secret-rotation-runbook.md", "standards/conventions/secret-hygiene.md", 1)
        return t.replace("# === History ===\n", "# === History ===\n#   secret-net-l3-and-bypass-paths: .aria/secret-guard.paths (project extension); residual gaps: systemctl status, docker inspect\n", 1)
    rw(os.path.join(A, "hooks", "secret-guard.sh"), guard_hdr)

    def scan_hdr(t):
        t = t.replace("(49 known bypass classes; effective prevention)", "(effective prevention)", 1).replace("(~15 secret-shape patterns; detect + warn only)", "(detect + warn only)", 1)
        t = t.replace("#   - bcrypt / argon2 password hashes", "#   - bcrypt password hashes", 1)
        t = t.replace("#       \"content\": \"...\"        // Read file content", "#       \"file\": {\"content\": \"...\"}   // Read: tool_response.file.content", 1)
        t = t.replace("# - Secrets encoded base64 / hex / etc (without telltale prefix)", "# - Secrets encoded base64 / hex / etc (without telltale prefix AND without a credential key name)", 1)
        t = t.replace("This is an architectural limit, not a\n# version-dependent behaviour.", "The 2.1.285 schema lists updatedToolOutput (unverified end to end, unused here).", 1)
        return t.replace("# === Threat model ===", "# change-id: secret-net-l3-and-bypass-paths\n#\n# === Threat model ===", 1)
    rw(os.path.join(A, "hooks", "secret-scan.sh"), scan_hdr)
    rw(os.path.join(A, "VERSION"), lambda t: t.replace("output REDACT", "detect + warn", 1))
print("docs patched", "(bad)" if bad else "")
