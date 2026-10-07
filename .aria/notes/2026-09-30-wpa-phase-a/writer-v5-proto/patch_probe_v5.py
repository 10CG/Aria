#!/usr/bin/env python3
"""patch_probe_v5.py -- derive baseline_probe.py (v5) from the v4 probe: every edit is an anchored, asserted text replacement (a missing anchor stops the script).
usage: python3 patch_probe_v5.py <v4 probe> <out probe>
The v4 probe is kept next to the output (spec/baseline_probe.v4.py); this script is the audit trail of what changed."""
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (n, old[:100])
    s = s.replace(old, new)


# ===================================================================== docstring / imports / helpers
rep("import re\nimport secrets\n", "import re\nimport resource\nimport secrets\n")
rep('''    WPA_REQUIRE_ALL=1                               acceptance mode: exit 3 when any row that should have run is `n/a`''',
    '''    WPA_REQUIRE_ALL=1                               acceptance mode: exit 3 when any row that should have run is `n/a`''')

# run_scan / run_guard: an optional CPU-time cap (RLIMIT_CPU through `ulimit -t` in a wrapper shell: no preexec_fn, which is not safe with threads); an env_extra value of None REMOVES the variable
rep('''def run_scan(env_obj, path=SYS_PATH):
    home, tmpd = fresh_dirs()
    p = subprocess.run([BASH_BIN, SCAN], input=json.dumps(env_obj).encode(), capture_output=True,
                       env=base_env(home, tmpd, path), cwd=WORK, timeout=300)''', '''def _cpu_capped(argv, cpu):
    """argv, run under a CPU-time limit of `cpu` seconds PER PROCESS (the hook and every process it starts): `ulimit -t` sets RLIMIT_CPU, which counts CPU time, not wall time,
    so the limit does not move with the load of the host.  A process that burns more is killed, exactly what the 5 s hook timeout does to a hook that is too slow."""
    return argv if not cpu else ["sh", "-c", 'ulimit -t "$0"; exec "$@"', str(cpu)] + argv


def run_scan(env_obj, path=SYS_PATH, cpu=None):
    home, tmpd = fresh_dirs()
    p = subprocess.run(_cpu_capped([BASH_BIN, SCAN], cpu), input=json.dumps(env_obj).encode(), capture_output=True,
                       env=base_env(home, tmpd, path), cwd=WORK, timeout=300)''')
rep('''def run_guard(tool, payload, env_extra=None, cwd_field=None, hook=None):
    home, tmpd = fresh_dirs()
    env = base_env(home, tmpd)
    if env_extra:
        env.update(env_extra)
    ti = {"command": payload} if tool == "Bash" else {"file_path": payload}
    obj = {"tool_name": tool, "tool_input": ti}
    if cwd_field is not None:
        obj["cwd"] = cwd_field
    p = subprocess.run([BASH_BIN, hook or GUARD], input=json.dumps(obj).encode(), capture_output=True, env=env, cwd=WORK, timeout=300)''',
    '''def run_guard(tool, payload, env_extra=None, cwd_field=None, hook=None, cpu=None):
    home, tmpd = fresh_dirs()
    env = base_env(home, tmpd)
    if env_extra:
        for _k, _v in env_extra.items():
            if _v is None:
                env.pop(_k, None)             # a None value removes the variable (e.g. LC_ALL: the harness may export only LANG)
            else:
                env[_k] = _v
    ti = {"command": payload} if tool == "Bash" else {"file_path": payload}
    obj = {"tool_name": tool, "tool_input": ti}
    if cwd_field is not None:
        obj["cwd"] = cwd_field
    p = subprocess.run(_cpu_capped([BASH_BIN, hook or GUARD], cpu), input=json.dumps(obj).encode(), capture_output=True, env=env, cwd=WORK, timeout=300)''')

# _scan_ok / l3 with an optional set of tags that MAY also appear
rep('''def _want_text(want):
    if want is None:
        return "silent"
    if want == "any":
        return "alert (any tag)"
    return "alert m=%d {%s}" % (sum(want.values()), " ".join(f"{k}={v}" for k, v in sorted(want.items())))

def _scan_ok(r, want):
    if want is None:
        return r["parse_ok"] and not r["alert"] and r["rc"] == 0
    if want == "any":
        return r["parse_ok"] and r["alert"] and r["rc"] == 0
    return r["parse_ok"] and r["alert"] and r["rc"] == 0 and r["tags"] == want and r["m"] == sum(want.values())

def l3(sc, cid, cat, desc, builder, shape, want, path=None):
    """want: None = silent; "any" = some alert (tag not pinned); dict = exact tag breakdown (matches = sum)."""
    def job():
        content, _vals = builder()
        r = run_scan(envelope(shape, content, path))
        return fmt_scan(r), _scan_ok(r, want)
    row(sc, cid, cat, desc, _want_text(want), job, hook=True)''', '''def _want_text(want, extra=None):
    if want is None:
        return "silent"
    if want == "any":
        return "alert (any tag)"
    txt = "alert m=%d {%s}" % (sum(want.values()), " ".join(f"{k}={v}" for k, v in sorted(want.items())))
    if extra:
        txt += " (+ optionally " + " ".join(f"{k}<={v}" for k, v in sorted(extra.items())) + ")"
    return txt

def _scan_ok(r, want, extra=None):
    if want is None:
        return r["parse_ok"] and not r["alert"] and r["rc"] == 0
    if want == "any":
        return r["parse_ok"] and r["alert"] and r["rc"] == 0
    if not (r["parse_ok"] and r["alert"] and r["rc"] == 0):
        return False
    got = dict(r["tags"])
    for t, mx in (extra or {}).items():          # tags that may ALSO appear (at most mx each); the wanted tags themselves are always exact
        if t not in want and got.get(t, 0) <= mx:
            got.pop(t, None)
    return got == want and r["m"] == sum(r["tags"].values())

def l3(sc, cid, cat, desc, builder, shape, want, path=None, extra=None):
    """want: None = silent; "any" = some alert (tag not pinned); dict = exact tag breakdown (matches = sum); extra = {tag: max} = tags that may also appear."""
    def job():
        content, _vals = builder()
        r = run_scan(envelope(shape, content, path))
        return fmt_scan(r), _scan_ok(r, want, extra)
    row(sc, cid, cat, desc, _want_text(want, extra), job, hook=True)''')

# ===================================================================== SC-1: 1c / 1d (union of the two views), 1e / 1f UTF-16-shaped text, 1g literal \u0000 text
rep('''l3("SC-1", "1c", "baseline-failing", "Read real envelope file.content = a NUL-separated process environment (the /proc/<pid>/environ shape): HOME / PATH / DB_PASSWORD / LANG / JWT_SECRET / API_TOKEN records, NUL after each",
   environ_nul, "read_real", {T_ENVLINE: 3})
l3("SC-1", "1d", "baseline-failing", "Bash real envelope stdout = the same NUL-separated records (the `env -0` shape): bash command substitution would drop the NULs and glue the records into one line",
   environ_nul, BR, {T_ENVLINE: 3})''',
    '''l3("SC-1", "1c", "baseline-failing", "Read real envelope file.content = a NUL-separated process environment (the /proc/<pid>/environ shape): HOME / PATH / DB_PASSWORD / LANG / JWT_SECRET / API_TOKEN records, NUL after each; the baseline view (NUL dropped) glues the records into one line, the second view (NUL -> newline) restores one record per line: `env-line-secret-keyword=3`; the glued baseline view may add ONE `kv-secret-assign` hit for the last record (the same credential seen twice: counts may be higher, never lower)",
   environ_nul, "read_real", {T_ENVLINE: 3}, extra={T_KV: 1})
l3("SC-1", "1d", "baseline-failing", "Bash real envelope stdout = the same NUL-separated records (the `env -0` shape): bash command substitution drops the NULs and glues the records into one line; same expectation as 1c",
   environ_nul, BR, {T_ENVLINE: 3}, extra={T_KV: 1})
def utf16le(text):
    """text as it reaches the hook when UTF-16LE bytes are shown by a tool: a NUL after every ASCII character"""
    return "".join(ch + "\\x00" for ch in text)
UTF16_CASES = [
    ("aws-key-line", lambda: (utf16le("aws_access_key_id = " + akia()), []), AWS1),
    ("env-line", lambda: (utf16le("JWT_" + "SECRET=" + b64std44()), []), {T_ENVLINE: 1}),
    ("github-pat", lambda: (utf16le("token " + gh_like()), []), {"github-pat": 1}),
    ("json-client-secret", lambda: (utf16le('{"client_' + 'secret":"' + alnum(32) + '"}'), []), {T_JSON_OLD: 1}),
]
l3m("SC-1", "1e", "reverse-guard", "UTF-16LE-shaped text (a NUL after every ASCII character) through the Bash real envelope still scans as the ASCII it spells -- the baseline view drops the NULs: an AWS key line, an env line, a `token <PAT>` line and a JSON client_secret each keep the detection they have at baseline (the NUL view must ADD a view, never replace the baseline one)",
    UTF16_CASES, shape=BR)
l3m("SC-1", "1f", "baseline-failing", "the same four UTF-16LE-shaped texts through the Read real envelope (file.content): the Read result is scanned (1a) and its NUL-shaped text keeps the detection the Bash view has (baseline: Read is not scanned at all)", UTF16_CASES, shape="read_real")
l3("SC-1", "1g", "reverse-guard", "text that merely MENTIONS the six characters `\\\\u0000` (no NUL byte at all) next to a credential: the second view equals the first, so it is not appended and the count stays 1 (not 2)",
   lambda: ("docs: a NUL byte is written \\\\u0000 in JSON\\n" + "AWS_ACCESS_KEY_ID=" + akia(), []), BR, AWS1)''')
# the 1e expectation helper needs the envelope's JSON to carry a real \\u0000: json.dumps does that for a NUL character

# ===================================================================== SC-9 9z, SC-10 10m / 10n / 10o
rep('''# SC-10 -- documented false-negative classes (pinned)''', '''l3m("SC-9", "9z", "allow-guard", "left boundary of kv-secret-assign: a credential key GLUED to a preceding word character is not a key start (a lower-case letter in front of an upper-case key; a lower-case prefix joined to the key by an underscore) -- an implementation without the boundary reads the key out of the middle of the word",
    [("lower-glued", T("x" + "JWT_" + "SECRET=@V0@", "alnum24"), None), ("prefix-glued", T("abc_API_" + "TOKEN=@V0@", "alnum24"), None)])

# SC-10 -- documented false-negative classes (pinned)''')
rep('''l3("SC-10", "10k", "known-limit", "json:token=<40 uppercase letters> (single char class)", T('{"token":"@V0@"}', "upper40"), BR, None)''',
    '''l3("SC-10", "10k", "known-limit", "json:token=<40 uppercase letters> (single char class)", T('{"token":"@V0@"}', "upper40"), BR, None)
def _l3_both_envelopes(sc, cid, cat, desc, cases):
    """known-limit style row over BOTH envelopes (Bash stdout and Read file.content): every case must be silent"""
    def job():
        res = []
        for label, builder in cases:
            for shape in (BR, "read_real"):
                content, _v = builder()
                res.append((f"{label}/{'bash' if shape == BR else 'read'}", _scan_ok(run_scan(envelope(shape, content)), None)))
        return _compact(res)
    row(sc, cid, cat, desc, f"{2 * len(cases)}/{2 * len(cases)} as expected", job, hook=True)
_FJ = "FORGE" + "JO__"
_GT = "GIT" + "EA__"
_l3_both_envelopes("SC-10", "10m", "known-limit", "KNOWN-LIMIT: the Forgejo / Gitea container environment overrides `FORGEJO__<section>__<KEY>` / `GITEA__<section>__<KEY>` (the section name is lower case: the same credentials as app.ini, another carrier) are silent in both layers: a compose env list, a compose env map, a docker inspect Env array",
    [("compose-list", T("      - " + _FJ + "security__SECRET_" + "KEY=@V0@", "alnum40")), ("compose-map", T("      " + _GT + "oauth2__JWT_" + "SECRET: @V0@", "alnum40")),
     ("inspect-env-array", T('"Env": ["' + _FJ + 'database__PAS' + 'SWD=@V0@"]', "alnum40"))])
l3m("SC-10", "10n", "known-limit", "KNOWN-LIMIT: a kv key longer than the bounds (64 key characters before and after the keyword) is not read -- 70 upper-case letters + `_TOKEN` in the middle of a line (the bounds are what keeps the pattern linear on long runs, W2)",
    [("long-key", T(" " + "A" * 70 + "_" + "TO" + "KEN=@V0@", "alnum24"), None)])
l3m("SC-10", "10o", "known-limit", "KNOWN-LIMIT: the flag-name forms the left boundary / prefix bound of cli-secret-flag do not read: a flag glued to a preceding letter (`abc--token=<value>`) and a flag name with more than 40 characters before the keyword (`--` + 45 letters + `token=<value>`)",
    [("glued", T("abc--" + "tok" + "en=@V0@", "alnum24"), None), ("long-name", T("--" + "a" * 45 + "tok" + "en=@V0@", "alnum24"), None)])''')

# ===================================================================== SC-18 18j / 18k: every alternative of the Read / Edit path regex
rep('''NONCE_FILES = []''', '''# the 32 alternatives of the baseline Read / Edit path regex (the `grep -qE` on the lower-cased file_path), one path each that matches ONLY that alternative
# (proto/readface_check.py verifies that from the hook source): the rewrite of that regex must not lose any of them
READ_ALT_PATHS = [
    ("env", "/srv/app/.env"), ("envrc", "/srv/app/.envrc"), ("secrets-dir", "/srv/app/secrets/db"), ("credentials-dir", "/srv/app/credentials/db"),
    ("id_rsa", "/home/u/id_rsa"), ("id_ed25519", "/home/u/id_ed25519"), ("id_ecdsa", "/home/u/id_ecdsa"), ("ssh-id", "/home/u/.ssh/id_custom"),
    ("pem", "/home/u/cert.pem"), ("key", "/home/u/server.key"), ("gpg", "/home/u/backup.gpg"), ("age", "/home/u/backup.age"), ("p12", "/home/u/store.p12"),
    ("pfx", "/home/u/cert.pfx"), ("jks", "/home/u/keystore.jks"), ("tfstate", "/srv/infra/terraform.tfstate"), ("tfstate-backup", "/srv/infra/terraform.tfstate.backup"),
    ("aws-credentials", "/home/u/.aws/credentials"), ("aws-config", "/home/u/.aws/config"), ("kube-config", "/home/u/.kube/config"), ("kubeconfig", "/home/u/kubeconfig"),
    ("docker-config", "/home/u/.docker/config.json"), ("service-account", "/srv/svc/service-account.json"), ("gcp-key", "/srv/svc/gcp-key.json"),
    ("firebase", "/srv/svc/firebase-adminsdk.json"), ("known-hosts", "/home/u/.ssh/known_hosts"), ("secret-token", "/srv/app/secret-token"),
    ("master-key", "/srv/app/master_key"), ("encryption-key", "/srv/app/encryption-key"), ("claude-settings", "/home/u/.claude/settings.json"),
    ("claude-settings-local", "/home/u/.claude/settings.local.json"), ("claude-json", "/home/u/.claude.json"),
]
l1e("SC-18", "18j", "reverse-guard", "the rewritten Read / Edit path regex keeps every one of its 32 baseline alternatives: one Read of a path that only that alternative matches, for each of the 32 (`.env`, `.envrc`, secrets / credentials directories, id_rsa / id_ed25519 / id_ecdsa / .ssh/id_*, .pem .key .gpg .age .p12 .pfx .jks, .tfstate and its backup, .aws credentials / config, .kube/config, kubeconfig, .docker/config.json, service-account / gcp-key / firebase json, known_hosts, secret-token / master-key / encryption-key, the three claude-config names)",
    READ_ALT_PATHS, 2, tool="Read")
l1e("SC-18", "18k", "reverse-guard", "the same 32 paths through the Edit tool (the same regex line serves both)", READ_ALT_PATHS, 2, tool="Edit")

NONCE_FILES = []''')

# ===================================================================== SC-19 / SC-20
# projects: bom, fold
rep('''    elif kind == "canary":''', '''    elif kind == "bom":
        # a file written by a Windows tool: a UTF-8 byte-order mark in front of the first entry, CRLF line ends
        open(f, "wb").write(b"\\xef\\xbb\\xbf" + P.encode() + b"\\r\\n/srv/bom/second.conf\\r\\n")
    elif kind == "fold":
        open(f, "wb").write("/srv/caf\\u00e9/menu\\n".encode("utf-8"))
    elif kind == "canary":''')
rep('''"ws", "cjk", "canary", "comment_only", "blank_only", "all_skipped")}''', '''"ws", "cjk", "bom", "fold", "canary", "comment_only", "blank_only", "all_skipped")}''')

# 19z: only the shapes where the built-in row and the extension agree on a block; the quoted-pipe shapes move to the known-limit row 19al
rep('''l1x("SC-19", "19z", "baseline-failing", "[CLAUDE_PROJECT_DIR=proj(ok)] separators inside quotes do not cut a stage: python3 -c / node -e / awk programs holding `;` / `&` / a newline, and quoted `|`: the listed path is blocked (exit 2) wherever the built-in app.ini row blocks the same command shape with the app.ini path (6 shapes x built-in and extension), and in the 2 quoted-pipe shapes (extension only)",
    [("Bash", t % APPINI, 2) for _l, t in STAGE_SHAPES] + [("Bash", t % P, 2) for _l, t in STAGE_SHAPES + STAGE_PIPE_SHAPES], env_extra=env_proj("ok"))''',
    '''l1x("SC-19", "19z", "baseline-failing", "[CLAUDE_PROJECT_DIR=proj(ok)] separators inside quotes do not cut a stage: python3 -c / node -e / awk programs holding `;` / `&` / a newline: the listed path is blocked (exit 2) exactly where the built-in app.ini row blocks the same command shape with the app.ini name (6 shapes x built-in and extension = 12 runs)",
    [("Bash", t % APPINI, 2) for _l, t in STAGE_SHAPES] + [("Bash", t % P, 2) for _l, t in STAGE_SHAPES], env_extra=env_proj("ok"))''')
rep('''l1m("SC-19", "19aa", "allow-guard", ["cat x; echo " + P, "ls | grep y; echo " + P, 'echo "see ' + P + '"; cat y', "cat x\\necho " + P, "cat x & echo " + P, "cat x | echo " + P, "echo " + P, "cat " + P + ' ";" | wc -l'], 0,
    "[CLAUDE_PROJECT_DIR=proj(ok)] separators OUTSIDE quotes still cut a stage: a reader in an earlier stage (`;` / `|` / `&` / newline) or after the quoted mention does not make a later mention of the path a read; a bare mention is no read; and a real count pipe that follows a QUOTED separator is still a credit (`cat <path> \\";\\" | wc -l`, as the built-in rows judge it)", env_extra=env_proj("ok"))''',
    '''l1m("SC-19", "19aa", "allow-guard", ["cat x; echo " + P, "ls | grep y; echo " + P, 'echo "see ' + P + '"; cat y', "cat x | echo " + P, "echo " + P, "cat " + P + ' ";" | wc -l'], 0,
    "[CLAUDE_PROJECT_DIR=proj(ok)] separators OUTSIDE quotes still cut where the built-in rows cut: a reader in an earlier segment (`;`) or in an earlier pipeline stage (`|`), or after the quoted mention, does not make a later mention of the path a read; a bare mention is no read; and a real count pipe that follows a QUOTED separator is still a credit (`cat <path> \\";\\" | wc -l`, as the built-in rows judge it)", env_extra=env_proj("ok"))''')
# 19ae: a pure non-ASCII entry is effective now
rep('''l1("SC-19", "19ae", "known-limit", "cat /srv/\\u914d\\u7f6e\\u5bc6\\u94a5/x", 0, desc="[CLAUDE_PROJECT_DIR=proj(cjk)] KNOWN-LIMIT: an entry without any ASCII letter or digit (here 4 CJK characters) is skipped silently: cat /srv/<4 CJK chars>/x (0)", env_extra=env_proj("cjk"))''',
    '''l1("SC-19", "19ae", "baseline-failing", "cat /srv/\\u914d\\u7f6e\\u5bc6\\u94a5/x", 2, desc="[CLAUDE_PROJECT_DIR=proj(cjk)] an entry that holds a non-ASCII byte is effective even without any ASCII letter or digit (here 4 CJK characters, 12 bytes): cat /srv/<4 CJK chars>/x (2); only an entry of ASCII symbols alone is skipped (19w)", env_extra=env_proj("cjk"))''')
# the new SC-19 rows (after 19ae)
rep('''# SC-20 -- extension failure only drops the extension (bad files, bad entries, faulty extension code, evaluation order)
for cid, k, note in [("20a", "missing", "file absent"),''', '''# 19af -- the extension is judged by the BUILT-IN judgement: command shape by command shape, the listed path is blocked exactly where the built-in app.ini name is blocked.
# Each template is run twice: with the built-in name as {P} (no extension involved) and with the listed path as {P} (extension); both exit codes must be equal.  A few anchor shapes also
# pin the built-in answer itself (a row that only compared the two would be green on a hook that blocks / allows everything).  The table covers escapes, `$'...'`, continuation
# lines, `||`, redirections with `&`, quoted pipes, heredocs, the degraded whole-command mode, wrappers and variable indirection.
APPINI_G = "/etc/gitea/app.ini"
DIFF_SHAPES = [
    ("cat", "cat {P}", 2), ("sed-n", "sed -n '1,80p' {P}", None), ("cat-wc", "cat {P} | wc -l", 0), ("cat-sha", "cat {P} | sha256sum", None), ("cat-grep-v", "cat {P} | grep -v '^#'", None),
    ("cat-grep-anchored", "cat {P} | grep '^KEY'", None), ("cat-devnull", "cat {P} >/dev/null", None), ("cat-2devnull", "cat {P} 2>/dev/null", None),
    ("semi-before", "echo hi; cat {P}", 2), ("semi-after", "cat {P}; echo hi", None), ("and-and", "true && cat {P}", None), ("or-or", "false || cat {P}", 2),
    ("or-or-pipe", "cat {P} || echo bad | wc -l", None), ("pipe-first", "ls | grep y; echo {P}", None), ("bare-mention", "echo {P}", 0), ("reader-then-mention", "cat x; echo {P}", None),
    ("mention-then-reader", "echo {P}; cat {P}", None), ("newline-sep", "cat x\\necho {P}", None), ("background-amp", "cat x & echo {P}", None), ("pipe-reader-later", "cat x | echo {P}", None),
    ("cont-cat", "cat \\\\\\n  {P}", 2), ("cont-sed", "sed -n '1,80p' \\\\\\n  {P}", None), ("cont-after-pipe", "cat {P} \\\\\\n  | wc -l", None), ("cont-mid", "cat \\\\\\n  -n \\\\\\n  {P}", None),
    ("redir-2to1-wc", "cat {P} 2>&1 | wc -l", 0), ("redir-2to1-sha", "cat {P} 2>&1 | sha256sum", None), ("redir-amp-gt", "cat {P} &>/dev/null", None),
    ("redir-2to1-devnull", "cat {P} 2>&1 >/dev/null", None), ("redir-1to2-wc", "cat {P} 1>&2 | wc -c", None), ("redir-pipe-amp", "cat {P} |& wc -l", None),
    ("redir-2to1-plain", "cat {P} 2>&1", None), ("redir-2to1-cont", "cat {P} \\\\\\n  2>&1 | wc -l", None),
    ("dq-path", 'cat "{P}"', None), ("sq-path", "cat '{P}'", None), ("quoted-semicolon-after", 'cat {P} ";" | wc -l', 0), ("quoted-semicolon-before", 'echo ";" && cat {P}', None),
    ("escaped-semicolon", "cat x\\\\; cat {P}", None), ("escaped-amp", "cat x\\\\& {P}", None),
    ("py-semi", "python3 -c \\"import os; print(open('{P}').read())\\"", None), ("py-escaped-dq", "python3 -c \\"print(\\\\\\"a\\\\\\"); print(open('{P}').read())\\"", None),
    ("py-escaped-dq-semi", "python3 -c \\"print(\\\\\\"a;b\\\\\\"); print(open('{P}').read())\\"", 2),
    ("py-ansi-c", "python3 -c $'import os; print(\\\\'x\\\\'); print(open(\\\\'{P}\\\\').read())'", 2), ("node-ansi-c", "node -e $'const fs=require(\\\\'fs\\\\'); console.log(fs.readFileSync(\\\\'{P}\\\\'))'", None),
    ("node-semi", "node -e \\"const fs=require('fs'); console.log(fs.readFileSync('{P}','utf8'))\\"", None), ("awk-semi", "awk 'BEGIN{x=1; while ((getline l < \\"{P}\\") > 0) print l}'", None),
    ("py-newline", "python3 -c \\"import os\\nprint(open('{P}').read())\\"", None), ("py-amp", "python3 -c \\"a=1 & 2; print(open('{P}').read())\\"", None),
    ("py-quoted-pipe", "python3 -c \\"print(1|2); print(open('{P}').read())\\"", None), ("grep-quoted-pipe", "grep -E 'A|B' {P}", None), ("sh-c-inner-pipe-wc", "bash -c 'cat {P} | wc -l'", None),
    ("py-dq-in-sq", "python3 -c '\\"; print(open(\\"{P}\\").read())'", None), ("sq-in-dq", "echo \\"it's\\"; cat {P}", None),
    ("cmdsubst", "x=$(cat {P})", None), ("cmdsubst-wc", "x=$(cat {P} | wc -l)", None), ("backticks", "x=`cat {P}`", None), ("subshell", "(cat {P})", None), ("brace-group", "{ cat {P}; }", None),
    ("heredoc", "cat <<EOF\\n{P}\\nEOF", None), ("dbl-bracket", "[[ -f {P} ]] && cat {P}", None), ("if-block", "if true; then cat {P}; fi", None), ("for-block", "for i in 1 2; do cat {P}; done", None),
    ("degraded-semicolon", "x=$(true); echo hi; cat x; echo {P}", None), ("degraded-mention", "x=$(true); echo {P}", None),
    ("ssh-quoted", "ssh host 'cat {P}'", None), ("docker-exec", "docker exec c cat {P}", None), ("sh-c", "sh -c 'cat {P}'", None), ("sudo", "sudo cat {P}", None), ("xargs", "echo {P} | xargs cat", None),
    ("var-indirect", "f={P}; cat \\"$f\\"", None), ("var-indirect-wc", "f={P}; cat \\"$f\\" | wc -l", None), ("ls-l", "ls -l {P}", None),
    ("cat-multi-occurrence", "cat {P} {P}", None), ("cat-then-ls-occurrence", "ls {P}; cat {P}", None),
]
def _diff_ext_builtin():
    bad, anchors_bad = [], []
    for lab, tpl, anchor in DIFF_SHAPES:
        b = run_guard("Bash", tpl.replace("{P}", APPINI_G))[0]
        e = run_guard("Bash", tpl.replace("{P}", P), env_proj("ok"))[0]
        if b != e:
            bad.append(lab)
        if anchor is not None and b != anchor:
            anchors_bad.append(lab)
    n = len(DIFF_SHAPES)
    txt = f"{n - len(bad)}/{n} shapes equal" + (f"; DIVERGE: {', '.join(bad[:6])}" + (", ..." if len(bad) > 6 else "") if bad else "")
    txt += "; anchors ok" if not anchors_bad else f"; anchor shapes the built-in row does not answer as pinned: {', '.join(anchors_bad[:6])}"
    return txt, (not bad) and (not anchors_bad)
row("SC-19", "19af", "baseline-failing", "[CLAUDE_PROJECT_DIR=proj(ok)] differential against the built-in app.ini row over " + str(len(DIFF_SHAPES)) + " command shapes (escapes, $'...', continuation lines, `||`, `&` redirections, quoted pipes, heredocs, the whole-command mode, wrappers, variable indirection): the exit code with the listed path equals the exit code with the built-in name for EVERY shape; 10 anchor shapes (6 blocked, 4 allowed) also pin the built-in answer itself",
    f"{len(DIFF_SHAPES)}/{len(DIFF_SHAPES)} shapes equal; anchors ok", _diff_ext_builtin, hook=True)
# 19ag -- offsets and slices use one unit: more than 20 multi-byte characters in front of the listed path
C20 = "\\u914d\\u7f6e" * 10
l1x("SC-19", "19ag", "baseline-failing", "[CLAUDE_PROJECT_DIR=proj(ok)] byte offsets and slices: 20 CJK characters (60 bytes) in front of the listed path must not shift the stage: `echo <C>; cat P; ls` / `echo <C> && cat P && ls` / `echo <C>; sed -n '1,80p' P; ls` / a script whose first line is a CJK comment / a CJK text inside quotes before the read -> exit 2 each",
    [("Bash", "echo " + C20 + "; cat " + P + "; ls", 2), ("Bash", "echo " + C20 + " && cat " + P + " && ls", 2), ("Bash", "echo " + C20 + "; sed -n '1,80p' " + P + "; ls", 2),
     ("Bash", "# " + C20 + "\\nls\\ncat " + P + "\\nls", 2), ("Bash", 'echo "' + C20 + '; x"; cat ' + P, 2)], env_extra=env_proj("ok"))
# 19ah -- byte semantics of the entry reader do not depend on the harness exporting LC_ALL: the environment holds only LANG (UTF-8)
_LANG_ONLY = {"LC_ALL": None, "LANG": "C.UTF-8"}
l1x("SC-19", "19ah", "baseline-failing", "[CLAUDE_PROJECT_DIR=proj(cjk); the hook's environment holds only LANG=C.UTF-8 -- no LC_ALL] entry length counts BYTES and the letter rule counts ASCII even when the caller does not export LC_ALL: `a<2 CJK>` (7 bytes) and `/srv/<2 CJK>/prod` are effective, a pure non-ASCII entry is effective too -> exit 2 x3",
    [("Bash", "cat /srv/a\\u914d\\u7f6e/x", 2), ("Bash", "cat /srv/\\u914d\\u7f6e/prod", 2), ("Bash", "cat /srv/\\u914d\\u7f6e\\u5bc6\\u94a5/x", 2)], env_extra=dict(env_proj("cjk"), **_LANG_ONLY))
# 19ai -- a UTF-8 byte-order mark in front of the first entry
l1x("SC-19", "19ai", "baseline-failing", "[CLAUDE_PROJECT_DIR=proj(bom): the file starts with a UTF-8 byte-order mark and has CRLF line ends, the first entry is P] the BOM is not part of the first entry: cat P (2) ; the second entry works too (2)",
    [("Bash", "cat " + P, 2), ("Bash", "cat /srv/bom/second.conf", 2)], env_extra=env_proj("bom"))
# 19aj -- an entry is a literal SUBSTRING, wherever it ends
l1x("SC-19", "19aj", "baseline-failing", "[CLAUDE_PROJECT_DIR=proj(ok)] an entry is a literal substring: the listed path followed by a word character or a dot suffix is still a hit: cat P.bak (2) ; cat Px (2) ; cat P_old (2)",
    [("Bash", "cat " + P + ".bak", 2), ("Bash", "cat " + P + "x", 2), ("Bash", "cat " + P + "_old", 2)], env_extra=env_proj("ok"))
# 19ak -- what the substitution puts into the command for the built-in judgement must not make OTHER built-in rows fire
l1m("SC-19", "19ak", "allow-guard", ["echo " + P + " runners/registration-token", "echo " + P + " /users/alice/tokens"], 0,
    "[CLAUDE_PROJECT_DIR=proj(ok)] a mention of the listed path is no read, and the name it is judged under does not drag other built-in rows in (the registration-token and PAT-creation rows match the word `forgejo`: the substituted name must not hold it)", env_extra=env_proj("ok"))
# 19al -- the inherited blind spot of the built-in rows
l1x("SC-19", "19al", "known-limit", "[CLAUDE_PROJECT_DIR=proj(ok)] KNOWN-LIMIT, inherited: a quoted `|` blinds the built-in `[^|]*` rows (W8, suggested issue 7.2) and the extension is judged by those same rows: `python3 -c \\"print(1|2); print(open('<path>').read())\\"` and `grep -E 'A|B' <path>` -> exit 0 for the app.ini name and for the listed path",
    [("Bash", t % APPINI, 0) for _l, t in STAGE_PIPE_SHAPES] + [("Bash", t % P, 0) for _l, t in STAGE_PIPE_SHAPES], env_extra=env_proj("ok"))
# 19am -- the Read / Edit face folds ASCII letters only (byte semantics, as the Bash face)
l1x("SC-19", "19am", "baseline-failing", "[CLAUDE_PROJECT_DIR=proj(fold): entry `/srv/caf<e-acute>/menu`; only LANG=C.UTF-8 in the environment] case-insensitivity is ASCII-only on the Read face too: Read /SRV/CAF<E-acute upper>/MENU (0: the non-ASCII letter is not folded) ; Read /SRV/CAF<e-acute>/MENU (2: the ASCII letters are)",
    [("Read", "/SRV/CAF\\u00c9/MENU", 0), ("Read", "/SRV/CAF\\u00e9/MENU", 2)], env_extra=dict(env_proj("fold"), **_LANG_ONLY))

# SC-20 -- extension failure only drops the extension (bad files, bad entries, faulty extension code, evaluation order)
for cid, k, note in [("20a", "missing", "file absent"),''')

# ===================================================================== SC-22: 22br / 22bs credit of the wrapped dumps, 22bj members
rep('''l1e("SC-22", "22bq", "baseline-failing",''', '''# 22br / 22bs: the env / printenv dumps under the wrappers are NOT part of the tight family: they keep the credit of the baseline `docker|kubectl|podman|lxc exec ... env` rows
# (an anchored grep / cut / grep -v / sed counts as a filter), so the legitimate "read one variable / list the variable names" checks stay allowed.
DUMP_MEMBERS = [(f"{w}:{d}", t.replace("CMD", d)) for w, t in WRAP_T_ENV for d in ("env", "printenv")]
l1e("SC-22", "22br", "allow-guard", "wrapped dumps with the legitimate checks: each of the 22 dump members followed by an anchored `| grep '^PATH='` (read ONE variable) and by `| cut -d= -f1` (list the variable NAMES) stays allowed -- the same credit the baseline gives `docker|kubectl|podman|lxc exec ... env` (44 runs)",
    [(f"{lab}|grep", cmd + " | grep '^PATH='") for lab, cmd in DUMP_MEMBERS] + [(f"{lab}|cut", cmd + " | cut -d= -f1") for lab, cmd in DUMP_MEMBERS], 0)
l1e("SC-22", "22bs", "known-limit", "KNOWN-LIMIT (the baseline's own limit, now shared by the wrappers added in W11): a wrapped dump followed by `| grep -v x` is allowed (the filter prints the whole environment minus one line, but a row-level filter is credit for these rows) -- 22 members; red = somebody made the dump family tight, update W11 and Impact then",
    [(f"{lab}|grep-v", cmd + " | grep -v x") for lab, cmd in DUMP_MEMBERS], 0)
l1e("SC-22", "22bq", "baseline-failing",''')
rep('''     ("grep-doc-search", 'grep -n "ssh host ps aux" README.md'), ("stopwatch-substring", "echo 'stopwatch: ps -ef'")], 2)''',
    '''     ("grep-doc-search", 'grep -n "ssh host ps aux" README.md'), ("stopwatch-substring", "echo 'stopwatch: ps -ef'"),
     ("env-word-commit", 'git commit -m "refactor ssh helper to read the token from env"'), ("env-word-echo", 'echo "configure sshd, then source env"'),
     ("venv-bash-c", 'bash -c "python3 -m venv env && env/bin/pip install -r requirements.txt"'), ("venv-sh-c", 'sh -c "cd /srv/app; python3 -m venv env"'),
     ("du-watch", 'watch -n 5 "du -sh env"'), ("proc-text-grep", "grep -rn /proc/self/environ docs/"), ("proc-text-rg", "rg '/proc/$$/environ' notes/"),
     ("proc-text-sed", "sed -i 's#/proc/1/cmdline#x#' notes.md")], 2)''')
rep('''("heredoc-after-text", "cat <<'EOF'\\nlist the processes with\\nps -ef\\nEOF"),''', '''("heredoc-after-text", "cat <<'EOF'\\nlist the processes with\\nps -ef\\nEOF"),''')
rep('''the row turns red when someone narrows either (update W11 and this row then)",''',
    '''so is text in which a wrapper word comes before the word `env` / `printenv` (a venv directory named env after `bash -c` / `sh -c` / `watch`, a commit message that ends in the word env after `ssh`), and a grep / rg / sed over text that holds a /proc/<pid>/environ|cmdline path whose pid position is a real pid token (`self`, `$$`, a digit string); the row turns red when someone narrows any of these (update W11 and this row then)",''')

# ===================================================================== SC-23 23j, SC-25 25g
rep('''def _w12_noexec():''', '''l1m("SC-23", "23j", "baseline-failing",
    ["python3 -c \\"import os; print(os.environ.get('A'), os.environ.get('B'))\\"", "python3 -c \\"import os; print(os.environ['A'], os.environ['B'])\\"",
     "python -c \\"import os; print(os.environb.get(b'A'), os.environb.get(b'B'))\\"", "python -c \\"import os; print(os.environb[b'A'], os.environb[b'B'])\\""], 0,
    "the same single-key substring TWICE in one command: every occurrence is normalised, not only the first (host / user / password each read once is the usual shape)")
def _w12_noexec():''')
rep('''row("SC-25", "25g", "baseline-failing", "Read /etc/forgejo/app.ini: new Read block reuses the unchanged Read/Edit BLOCKED text", "text=baseline-identical", blocked("Read", "/etc/forgejo/app.ini", H_READ), hook=True)''',
    '''row("SC-25", "25g", "baseline-failing", "Read /etc/forgejo/app.ini: new Read block reuses the unchanged Read/Edit BLOCKED text", "text=baseline-identical", blocked("Read", "/etc/forgejo/app.ini", H_READ), hook=True)
def _blocked_echoes_original():
    """the single-key normalisation only changes what the rows are matched against: the BLOCKED text still echoes the ORIGINAL command (`Command was:`)"""
    rc, err = run_guard("Bash", "python3 -c \\"import os; print(os.environ.get('A')); open('.env')\\"")
    line = [l for l in err.splitlines() if l.startswith("Command was: ")]
    ok = rc == 2 and bool(line) and ".environ.get(" in line[0]
    return ("blocked; `Command was:` shows the original text" if ok else f"rc={rc}; echo={'original' if ok else 'normalised or absent'}"), ok
row("SC-25", "25h", "reverse-guard", "a command that holds a single-key read AND a real `.env` read is blocked, and its `Command was:` line echoes the original text (`.environ.get(` is still there), not the normalised copy the rows were matched against",
    "blocked; `Command was:` shows the original text", _blocked_echoes_original, hook=True)''')

# ===================================================================== SC-26 26g, SC-28 28o
rep('''    miss = [k for k in ("rule6_note", ".aria/secret-guard.paths", "ps aux", "os.environ", "keys_unsorted", "fp=", "partial") if k not in first]''',
    '''    miss = [k for k in ("rule6_note", ".aria/secret-guard.paths", "ps aux", "/proc", "app.ini", "file.content", "kv-secret-assign", "placeholder", "os.environ", "keys_unsorted", "fp=", "CPU", "partial") if k not in first]''')
rep('''row("SC-26", "26g", "doc-sync", "aria CHANGELOG.md, topmost version section: names rule6_note, the new `.aria/secret-guard.paths` input, the `ps aux` behaviour change, the loosening side (`os.environ` single-key reads, `keys_unsorted`), the `fp=` log field and the `partial` coverage of variable indirection", "top-section-complete", _changelog_doc)''',
    '''row("SC-26", "26g", "doc-sync", "aria CHANGELOG.md, topmost version section: names rule6_note and one marker word of each disclosure of the Impact section -- the new input (`.aria/secret-guard.paths`), the new blocks (`ps aux`, `/proc`, `app.ini`), the new alerts (Read results scanned: `file.content`; the new tag `kv-secret-assign`), the new silence (`placeholder`), the loosening (`os.environ` single-key reads, `keys_unsorted`), the log field (`fp=`), the performance note (`CPU`) and the `partial` coverage of variable indirection", "top-section-complete", _changelog_doc)''')
rep('''    ("28l", SCAN, ("version-dependent behaviour", "exposes no field to"),''', '''    ("28o", GUARD, "~100", lambda s: "most common patterns" in re.sub(r"\\s*\\n#\\s*", " ", s) and not NO_COUNT.search(re.sub(r"\\s*\\n#\\s*", " ", s)), 25, "secret-guard.sh header: the stale count `~100 most common patterns` is gone (the rule table is 145 rows at baseline, 149 after this change) and no new count literal is written in its place (the header sentence is joined across its comment line breaks before the check)"),
    ("28l", SCAN, ("version-dependent behaviour", "exposes no field to"),''')

# ===================================================================== SC-34: linear time under a CPU limit (new)
rep('''# ================================================================ run + print''', '''# SC-34 -- linear-time rows: the new scanning code must stay linear in the input.  Each run is capped at 4 s of CPU time per process (`ulimit -t`: CPU time, not wall time, so the
# verdict does not move with the load of the host); a hook that is quadratic on the shape is killed before it can report, exactly what the 5 s hook timeout does to it.
CPU_CAP = 4
def _long(unit, n):
    return unit * (n // len(unit))
_TOK = "tok" + "en"
def _lin_job(cases, shape, kind):
    def job():
        res = []
        for label, builder, want in cases:
            content = builder()
            if kind == "l3":
                r = run_scan(envelope(shape, content), cpu=CPU_CAP)
                res.append((label, _scan_ok(r, want)))
            else:
                rc = run_guard("Bash", content[0], content[1], cpu=CPU_CAP)[0]
                res.append((label, rc == want))
        return _compact(res)
    return job
LIN_BASE = [   # baseline tags: the detection the baseline has on a long single line must survive the new value-extraction / fingerprint code
    ("bearer-long-value", lambda: "Authorization: " + "Bear" + "er " + _long("aA1", 8000), {"bearer-token": 1}),
    ("x-api-key-long-value", lambda: "X-Api-" + "Key: " + _long("aA1", 8000), {"x-api-key-header": 1}),
    ("env-line-long-value", lambda: "DB_" + "PASSWORD=" + _long("aA1", 8000), {T_ENVLINE: 1}),
    ("env-line-long-key", lambda: "A" * 8000 + "_" + "TO" + "KEN=" + alnum(24), {T_ENVLINE: 1}),
    ("postgres-long-password", lambda: "postgres://u:" + "p" * 8000 + "@h", {"postgres-url": 1}),
    ("postgres-long-user", lambda: "postgres://" + "u" * 8000 + ":" + alnum(8) + "@h", {"postgres-url": 1}),
    ("json-secret-long-value", lambda: '{"' + "pass" + 'word":"' + _long("aA1", 8000) + '"}', {T_JSON_OLD: 1}),
]
LIN_NEW = [    # the 6 new tags on the shapes that make a careless pattern or extraction quadratic
    ("cli-dash-run", lambda: "-" * 300000 + " -" + _TOK + "=" + alnum(24), {T_FLAG: 1}),
    ("cli-letter-dash-run", lambda: "a-" * 10000 + " --" + _TOK + "=" + alnum(24), {T_FLAG: 1}),
    ("cli-long-value", lambda: "--" + _TOK + "=" + _long("aA1", 8000), {T_FLAG: 1}),
    ("kv-upper-run", lambda: "A" * 300000 + " JWT_" + "SECRET=" + alnum(24), {T_KV: 1}),
    ("kv-export-blank-run", lambda: "export" + " " * 8000 + "SVC_" + "TOKEN=" + alnum(24), {T_KV: 1}),
    ("auth-long-value", lambda: "Authorization: " + _TOK + " " + _long("aA1", 8000), {T_AUTH: 1}),
    ("auth-blank-run", lambda: "Authorization:" + " " * 8000 + _TOK + " " + alnum(24), {T_AUTH: 1}),
    ("cf-blank-run", lambda: "CF-Access-Client-" + "Secret:" + " " * 8000 + hexs(64), {T_CF: 1}),
    ("json-blank-run", lambda: '{"' + _TOK + '":"' + " " * 8000 + alnum(24) + '"}', {T_JSON_NEW: 1}),
]
row("SC-34", "34a", "reverse-guard", "linear time, baseline tags: a long single line (8 KB values or keys) through the Bash real envelope under a 4 s CPU cap per process still gives the baseline detection -- bearer / X-API-Key header, env-line (long value and long key), postgres URL (long password and long user), json password: 7 shapes",
    "7/7 as expected", _lin_job(LIN_BASE, BR, "l3"))
row("SC-34", "34b", "baseline-failing", "linear time, new tags: shapes that make a pattern or the value extraction quadratic -- a 300 KB run of `-` and a 20 KB run of `a-` in front of a flag, a long flag value, a 300 KB upper-case run in front of a key, 8 KB blank runs in the export / header / JSON forms, 8 KB header and flag values -- under a 4 s CPU cap per process: the tag is still counted (9 shapes)",
    "9/9 as expected", _lin_job(LIN_NEW, BR, "l3"))
_PAD4K = "padding-text " * 320
_TIMES_RE = re.compile(r"(\d+)m([0-9.]+)s\s+(\d+)m([0-9.]+)s")
def run_guard_cpu_total(cmd, env_extra, cap):
    """exit code and TOTAL CPU seconds (user + sys of the hook and every process it started, read with the shell builtin `times`: per run, so it is safe with the probe's threads)
    of one Bash-command hook run; every process is also capped at `cap` CPU seconds"""
    home, tmpd = fresh_dirs()
    env = base_env(home, tmpd)
    env.update(env_extra or {})
    wrapper = 'ulimit -t "$0"; "$@" >/dev/null 2>&1; rc=$?; times >&2; exit $rc'
    p = subprocess.run(["sh", "-c", wrapper, str(cap), BASH_BIN, GUARD], input=json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}).encode(),
                       capture_output=True, env=env, cwd=WORK, timeout=300)
    ms = _TIMES_RE.findall(p.stderr.decode("utf-8", "replace"))
    cpu = (int(ms[-1][0]) * 60 + float(ms[-1][1]) + int(ms[-1][2]) * 60 + float(ms[-1][3])) if ms else 1e9
    return p.returncode, cpu
LIN_L1 = [("64-occurrences-after-4KB", "echo " + _PAD4K + " " + " ".join([P] * 63) + "; cat " + P), ("one-occurrence-after-4KB", "echo " + _PAD4K + "; cat " + P)]
def _l1_hit_cost():
    """the extension's HIT path must cost about one more built-in judgement of the same command, not a loop over the occurrences: the total CPU of the run with the listed path
    present (extension in effect) over the total CPU of the SAME command with no extension file stays within 3.5x (the hit path is designed at about 2x); the exit code is 2 under a
    4 s per-process CPU cap (a quadratic stage computation is killed by it).  The ratio itself is not printed (it moves with the host); only whether the bound holds."""
    res = []
    for label, cmd in LIN_L1:
        hit, nohit = [], []
        rcs = set()
        for _ in range(3):                                     # interleaved, the minimum of each side is compared
            rc, c = run_guard_cpu_total(cmd, env_proj("ok"), CPU_CAP); hit.append(c); rcs.add(rc)
            _rc2, c2 = run_guard_cpu_total(cmd, env_proj("missing"), CPU_CAP); nohit.append(c2)
        ratio = min(hit) / max(min(nohit), 0.05)
        res.append((label + ("" if rcs == {2} else "[exit!=2]") + ("" if ratio <= 3.5 else "[cost>3.5x]"), rcs == {2} and ratio <= 3.5))
    return _compact(res)
row("SC-34", "34c", "baseline-failing", "linear time, the extension's hit path: a 4 KB single line with the listed path 64 times (the last one behind `cat`), and the same with one occurrence: the read is found (exit 2) under a 4 s CPU cap per process, and the TOTAL CPU of the run with the extension in effect stays within 3.5x of the same command with no extension file (a hit costs one more built-in judgement of the same command, about 2x; a loop over the occurrences or a per-occurrence stage computation costs tens of times)",
    "2/2 as expected", _l1_hit_cost)

# ================================================================ run + print''')
rep('''DEFERRED_ROWS = {("SC-32", "32c"), ("SC-32", "32d")}                      # bash-3.2 differential: needs every hook-direct row's first result''',
    '''DEFERRED_ROWS = {("SC-32", "32c"), ("SC-32", "32d"), ("SC-32", "32e")}    # bash-3.2 / second-locale / POSIX-locale differentials: need every hook-direct row's first result''')

# ===================================================================== SC-32 32e: a POSIX-locale leg
rep('''# SC-33 -- L3 false-positive census over a frozen corpus (the 6 new tags only)''', '''row("SC-32", "32e", "reverse-guard", "the same differential in the POSIX locale (LC_ALL=C: bytes, no multi-byte characters; the locale of a container image without LANG, e.g. the aria-runner image), default bash: every hook-direct row gives the same result string as in the first locale (C.UTF-8) -- code that counts characters where it must count bytes (or the reverse) differs here and nowhere else",
    "identical over all hook-direct rows in the POSIX locale", lambda: ("not-run", None))

# SC-33 -- L3 false-positive census over a frozen corpus (the 6 new tags only)''')
rep('''    order = {}
    for i, r in enumerate(ROWS):
        if i in results or (not ONLY):''', '''    # SC-32 32e: the same hook-direct rows in the POSIX locale (default bash only), compared with the first-locale result string.
    e32_i = [i for i, r in enumerate(ROWS) if (r[0], r[1]) == ("SC-32", "32e")]
    if e32_i and want("SC-32"):
        LOCALE, LOCPATH_EXTRA = "C", None
        BASH_BIN = "bash"
        leg_res = {}
        with cf.ThreadPoolExecutor(max_workers=6) as ex:
            futs = {ex.submit(r[5]): i for i, r in enumerate(ROWS) if r[6] and i in results and results[i][1] is not None and want(r[0])}
            for f in cf.as_completed(futs):
                leg_res[futs[f]] = f.result()
        LOCALE = "C.UTF-8"
        differ = sorted({f"{ROWS[i][0]}:{ROWS[i][1]}" for i in leg_res if leg_res[i][0] != results[i][0]}, key=lambda x: (int(re.match(r"SC-(\\d+)", x).group(1)), x))
        if differ:
            results[e32_i[0]] = (f"{len(differ)} of {len(leg_res)} rows differ: {' '.join(differ)}", False)
        else:
            results[e32_i[0]] = (f"identical over {len(leg_res)} hook-direct rows (locale C)", True)

    order = {}
    for i, r in enumerate(ROWS):
        if i in results or (not ONLY):''')

open(out_path, "w", encoding="utf-8").write(s)
print("wrote", out_path, len(s), "bytes")
