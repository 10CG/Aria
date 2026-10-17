#!/usr/bin/env python3
"""Apply a minimal 'target-state' documentation change to the prototype trees so that the doc-sync rows
(SC-26 / SC-27 / SC-28) can be exercised as 'yes'.  Not a real doc change: the sentences are only as long as the checks need.
usage: python3 patch_docs.py <proto dir> [--bad | --bad-sot | --bad-layer | --no-scope]
  --bad      the 'token stuffing' bad implementation: facts only in the SOT version-history row, no other document patched
  --bad-sot  the same SOT stuffing, but README / CHANGELOG / hook headers / VERSION patched normally (the case the SC-26 text names)
  --bad-layer  everything patched normally, but the new SOT clause uses this Spec's layer numbers L1 / L3 (SC-26 26i)
  --no-scope   everything patched normally, but the secret-scan.sh header Scope list does not name the 6 new tags (SC-28 28n)"""
import os
import re
import sys

root = sys.argv[1]
bad_sot = "--bad-sot" in sys.argv
bad_layer = "--bad-layer" in sys.argv
no_scope = "--no-scope" in sys.argv
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
    rw(os.path.join(A, "CHANGELOG.md"), lambda t: re.sub(r"(?m)^## ", "## [Unreleased]\n\nrule6_note: substitute. `.aria/secret-guard.paths` is a new input; `ps aux` is now blocked; os.environ single-key reads and keys_unsorted are now allowed; the log gains an fp= field; variable indirection is a partial fix.\n\n## ", t, count=1))

    def guard_hdr(t):
        t = sub1(t, "Phase 2 would add PostToolUse hook\n#     that regex-scans output for `^[A-Z_]+=.+$` style env lines + redacts —\n#     out of scope for current implementation.",
                 "L3 detect+warn lives in the PostToolUse hook secret-scan.sh.")
        t = sub1(t, "docs/operations/secret-rotation-runbook.md", "standards/conventions/secret-hygiene.md")
        return sub1(t, "# === History ===\n", "# === History ===\n#   secret-net-l3-and-bypass-paths: .aria/secret-guard.paths (project extension); variable indirection is only partly covered; the shared BLOCKED text lists Acceptable filters that do not apply to the tight families; residual gaps: systemctl status, docker inspect\n")
    rw(os.path.join(A, "hooks", "secret-guard.sh"), guard_hdr)

    def scan_hdr(t):
        t = sub1(t, "(49 known bypass classes; effective prevention)", "(effective prevention)")
        t = sub1(t, "(~15 secret-shape patterns; detect + warn only)", "(detect + warn only)")
        t = sub1(t, "#   - bcrypt / argon2 password hashes", "#   - bcrypt password hashes" + ("" if no_scope else "\n#   - key-shape tags: json-credential-field json-env-secret-key kv-secret-assign auth-header-token cf-access-client-secret cli-secret-flag"))
        t = sub1(t, "#       \"content\": \"...\"        // Read file content", "#       \"file\": {\"content\": \"...\"}   // Read: tool_response.file.content")
        t = sub1(t, "# - Secrets encoded base64 / hex / etc (without telltale prefix)", "# - Secrets encoded base64 / hex / etc (without telltale prefix AND without a credential key name)")
        t = sub1(t, "This is an architectural limit, not a\n# version-dependent behaviour.", "The 2.1.285 schema lists updatedToolOutput (unverified end to end, unused here).")
        return sub1(t, "# === Threat model ===", "# change-id: secret-net-l3-and-bypass-paths\n#\n# === Threat model ===")
    rw(os.path.join(A, "hooks", "secret-scan.sh"), scan_hdr)
    rw(os.path.join(A, "VERSION"), lambda t: sub1(t, "output REDACT", "detect + warn"))
print("docs patched", "(bad-sot)" if bad_sot else ("(bad)" if bad else ""))
