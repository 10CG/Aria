#!/usr/bin/env python3
"""Build the v5-design PROTOTYPE of hooks/secret-guard.sh from the baseline copy.

usage: python3 patch_l1.py <baseline secret-guard.sh> <out secret-guard.sh> [--variant NAME[:ARG]]

The prototype is not the implementation: it is generated from the baseline by text substitution and only shows that the
design written into proposal v5 is reachable, and which bad implementations the probe rows catch.

variants (every non-default variant is a 'bad implementation' that the probe rows must catch; an unknown name is an error):
  v5                 the design written into proposal v5
  -- v5 additions (R4 findings)
  ext_v4stage[:A]    the previous W9 design kept as a bad implementation: a hand-written quote mask + a stage cut per occurrence (A = noesc_q | noesc_all | noansi | nopipe | nonl: a mask that lacks
                     one state)                                                                                           -> SC-19 19af (differential) / SC-34 34c (time)
  ext_perocc_judge   one full built-in judgement per occurrence instead of one for the substituted copy                       -> SC-34 34c
  ext_charslice      grep runs in C (byte offsets) but the slicing runs in the hook's locale                                  -> SC-19 19ag
  ext_localnoexp     `local LC_ALL=C` without export: the children keep the caller's locale when the environment has no LC_ALL -> SC-19 19ah
  ext_noc            no byte semantics at all in the extension code                                                           -> SC-19 19ad / 19ag / 19ah
  ext_nobom          a leading UTF-8 byte-order mark is not stripped                                                          -> SC-19 19ai
  ext_ascii_only     an entry must hold an ASCII letter or digit (a pure non-ASCII entry is skipped)                          -> SC-19 19ae
  ext_subst_first    only the first occurrence of an entry is substituted                                                     -> SC-19 19r
  ext_subst_nosep    the substituted name is not followed by a blank (the right boundary of the name group breaks)             -> SC-19 19aj
  ext_subst_forgejo  the substituted name holds the word `forgejo` (other built-in rows match that word)                      -> SC-19 19ak
  env_tight          the env / printenv dump alternative of the remote wrappers is part of the TIGHT copy too                  -> SC-22 22br
  w12_once           the W12 normalisation replaces only the first occurrence of each single-key substring                    -> SC-23 23j
  readface16         16 of the 32 baseline alternatives of the Read / Edit path regex are lost                                  -> SC-18 18j
  -- v4 additions (R3 findings)
  vx_eval            W10 resolves chained references with `eval` (executes command text)                         -> SC-21 21z
  ext_eval           W9 builds the grep argument list as text and `eval`s it (executes entries / command text)    -> SC-19 19ab
  ext_glob           W9 loops over the entries unquoted (word splitting + file-name globbing of the entries)      -> SC-19 19ab
  w12_eval           W12 normalisation double-evaluates the command text                                          -> SC-23 23i
  ext_nostrip        W9 does not strip leading / trailing white space of an entry                                 -> SC-19 19ac
  ext_charlen        alias of ext_noc (the entry length is counted in characters of the caller's UTF-8 locale)       -> SC-19 19ad
  ext_emptypat       W9 hands an empty pattern line to grep -F -f when there is no valid entry                     -> SC-20 20o-20q
  tight_without:P    the tight copy of the process-table definition lacks part P (PROCTAB REMOTE DOCKER); the rule rows keep it  -> SC-22 22bm
  tdrop_launch:X     launcher X missing from the TIGHT copy only (the rule row keeps it)                          -> SC-22 22bm
  tdrop_remote:X     remote wrapper X missing from the TIGHT copy only                                            -> SC-22 22bm
  tdrop_psalt:N      ps alternative N missing from the TIGHT copy only                                            -> SC-22 22bm
  tight_plainps      the tight copy only recognises a line-leading plain `ps`                                     -> SC-22 22bm
  tight_ini_literal  the app.ini tight condition only knows the literal /etc/forgejo/app.ini                      -> SC-16 16r
  notight_proc       the process-table family has NO tight condition (every row-level filter counts as credit)     -> SC-22 22bm
  notight_ini        the app.ini family has no tight condition (the claude-config one stays)                      -> SC-16 16r
  launcher_ps_only   a launcher prefix is honoured for `ps` only (not for pgrep / pstree / top)                   -> SC-22 22bq
  remote_env_split:X the env / printenv dump alternative lacks wrapper X (the ps alternative keeps it)            -> SC-22 22bo
  drop_envwrap:X     alias of remote_env_split (kept for the plan files)
  proc_tight         the /proc rows are made tight (a baseline-different behaviour)                               -> SC-22 22bh
  pidtok_placeholders the pid token also accepts any bracket / brace token, so `[pid]` / `{pid}` placeholders are read   -> SC-22 22bf
  proc_nocredit      the process-table family gets NO credit at all (not even a count / hash / discard)           -> SC-22 22bn
  remote_anchored    the remote / shell wrapper words are anchored at command position (narrows the text-mention over-block)  -> SC-22 22bj
  -- ordering / isolation / bounds (W9, W10)
  ext_bare ext_first vx_interleave ext_regex ext_trunc vx_patsub b4
  -- timing bad implementations (W14 / SC-30; not probe rows -- measured with proto/timing.py)
  vx_quadratic                 remainder after a hit taken with ${s#*"$pat"} (O(n^2) when the hit sits late in a long string), in W10 only
  w12_quadratic                the same idiom in the W12 normalisation loops
  vx_collect_per_seg           the assignment collection is redone for every segment
  ext_perentry                 one grep process per extension entry (Bash and Read faces)
  ext_max199 / ext_max201      entry count limit 199 / 201 instead of 200
  ext_size32767 / ext_size32769 file size limit 32767 / 32769 instead of 32768
  ext_minlen3 / ext_minlen5    shortest entry 3 / 5 instead of 4
  ext_maxlen199 / ext_maxlen201 longest entry 199 / 201 instead of 200
  ext_nosym                    pure-symbol entries accepted (no letter-or-digit requirement)
  ext_occ63 / ext_occ65        occurrences checked: 63 / 65 instead of 64
  vx_assign15 / vx_assign17    assignments collected: 15 / 17 instead of 16
  vx_repl7 / vx_repl9          replacements per variable: 7 / 9 instead of 8
  vx_noquote                   quoted assignment values not collected
  anchor_nocntrl               the command-position anchor of the process-table row lacks the control-character (newline) alternative
  launcher_any                 over-broad: any command behind a launcher is blocked
  vx_start_only                assignments recognised only at the start of a segment (no whitespace boundary: every declaration prefix hides the assignment)
  drop_assign:X                assignment prefix X missing (export declare local readonly typeset)
  -- W8 / W9 readers, W11 tables
  drop_reader:X                reader X missing from the shared print-reader table (W8 row and W9 extension)
  drop_extreader:X             reader X missing from the W9 extension reader table only
  drop_interp:X                inline interpreter X missing from the W8 / W9 source groups (python3 node)
  drop_launch:X                launcher X missing (the 15 launcher words; `watch` is a shell wrapper, see drop_remote)
  drop_procreader:X            reader X missing from the /proc reader table (13 baseline + 11 added; egrep / fgrep / zgrep are matched by `grep`)
  drop_remote:X                remote wrapper X missing (ssh docker podman kubectl lxc nomad pct sh bash watch)
  drop_psalt:N                 ps argument alternative N missing (1..7)
  drop_pid:N                   pid token alternative N missing (0..5: self digits star ${..} $name $(..))
  drop_kwpos:X                 keyword position X missing (then do else elif)
  drop_pgrep:N / drop_pstree:N pgrep alternative N missing (0 = -a cluster, 1 = --list-full) / pstree alternative N missing (0 = -a cluster, 1 = --arguments)
  drop_dockerform:X            docker / podman form X missing (top compose container ls notrunc)
  drop_bin                     no absolute-path prefix on the target / launcher
  drop_larg                    launcher options may not take arguments (v2 grammar)
  drop_procinterp              /proc not added to the inline-interpreter groups
  nodocker_podman              podman top / podman ps --no-trunc missing
  pidtok_any                   v2 pid token (any token) instead of the narrowed one
  -- W8 / W11 / W12 old variants
  notight jq_loose env_boundary proc_status
  read_noboundary              Read/Edit face has no right boundary after app.ini (the v2 prototype flaw)
  bash_boundary_wide           Bash face has no right boundary after app.ini (app.inix / app.ini2 are blocked too): SC-17 17c
  appini_anywhere              Bash face blocks the app.ini name behind ANY command / no reader needed: SC-17 17a / 17d
  read_case_sensitive          Read/Edit face matches the path in its original case (the Bash-face behaviour): SC-18 18h
  claude_notight               the claude-config tight-credit condition was lost in the rewrite: SC-16 16p
  drop_interp_name:N           the rewritten python3 -c / node -e rows lost one baseline name (v1var secretsmanager secrets env provider_key claudecfg): SC-16 16o
  pgrep_wide                   pgrep -f (prints pids only) is blocked too: SC-22 22S / 22O
  drop_w12:N                   W12 single-key normalisation lacks substring N (0..3)
Rule #7: this file holds no credential-shaped literal.
"""
import subprocess
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
variant = "v5"
if "--variant" in sys.argv:
    variant = sys.argv[sys.argv.index("--variant") + 1]
vname, _, varg = variant.partition(":")
KNOWN = set("""v5 v4 v3 vx_eval ext_eval ext_glob w12_eval ext_nostrip ext_charlen ext_emptypat ext_v4stage ext_perocc_judge ext_charslice ext_localnoexp ext_noc ext_nobom ext_ascii_only
ext_subst_first ext_subst_nosep ext_subst_forgejo ext_nocut env_tight w12_once readface16 readface_drop
tight_without tdrop_launch tdrop_remote tdrop_psalt tight_plainps tight_ini_literal notight_proc notight_ini launcher_ps_only remote_env_split drop_envwrap proc_tight
ext_bare ext_first vx_interleave ext_regex ext_trunc vx_patsub b4 vx_quadratic w12_quadratic vx_collect_per_seg ext_perentry ext_max199 ext_max201
ext_size32767 ext_size32769 ext_minlen3 ext_minlen5 ext_maxlen199 ext_maxlen201 ext_nosym ext_occ63 ext_occ65 vx_assign15 vx_assign17 vx_repl7 vx_repl9
vx_noquote anchor_nocntrl launcher_any vx_start_only drop_assign drop_reader drop_extreader drop_interp drop_launch drop_procreader drop_remote drop_psalt
drop_pid drop_kwpos drop_pgrep drop_pstree drop_dockerform drop_bin drop_larg drop_procinterp nodocker_podman pidtok_any notight jq_loose env_boundary
w12_echo_norm proc_status pidtok_placeholders proc_nocredit remote_anchored read_noboundary bash_boundary_wide appini_anywhere read_case_sensitive claude_notight drop_interp_name pgrep_wide drop_w12""".split())
if vname not in KNOWN:
    sys.stderr.write("unknown variant %r\n" % vname)
    sys.exit(64)
src = open(src_path, encoding="utf-8").read()


def rep(old, new, count=1):
    global src
    n = src.count(old)
    assert n == count, f"anchor count {n} != {count} for: {old[:80]!r}"
    src = src.replace(old, new)


# ------------------------------------------------------------------ tables (members are listed once, composed below)
READERS = "cat grep egrep fgrep rg head tail less more strings awk sed jq nl tac rev sort uniq cut paste diff cmp comm xxd od hexdump base64 column fold".split()
LAUNCH = "sudo doas nice timeout xargs nohup stdbuf env time eval setsid ionice unbuffer command exec".split()
PROC_OLD = "cat head tail less more strings hexdump od xxd tr awk perl rev".split()
PROC_NEW = "xargs sed grep rg cut paste nl sort base64 cp dd".split()
KWPOS = "then do else elif".split()
REMOTE = {"ssh": "ssh", "docker": "docker[[:space:]]+(compose[[:space:]]+)?exec", "kubectl": "kubectl[[:space:]]+exec",
          "nomad": "nomad[[:space:]]+alloc[[:space:]]+exec", "pct": "pct[[:space:]]+exec", "lxc": "lxc[[:space:]]+exec",
          "podman": "podman[[:space:]]+exec", "sh": "(sh|bash|zsh|dash)[[:space:]]+-c", "watch": "watch"}
PS_ALTS = [
    "[a-zA-Z]+([^[:alnum:]_-]|$)",
    "[0-9]+([^[:alnum:]_.-]|$)",
    "([^|;&]*[[:blank:]])?-[a-zA-Z]*[fF]",
    "([^|;&]*[[:blank:]])?(-[a-zA-Z]*[oO]|--format)[[:blank:]=]*[^[:blank:]|;&]*(args|cmd|command)",
    "([^|;&]*[[:blank:]])?-[a-zA-Z]*O",
    "([^|;&]*[[:blank:]])?-[a-zA-Z]*x[a-zA-Z]*([^[:alnum:]_-]|$)",
    "([^|;&]*[[:blank:]])?-[a-zA-Z]*u[[:blank:]]*($|[|;&)<>])",
]
# pid-position tokens of the widened /proc rows.  v4 (R3 K cluster): index 2 is the general glob token (any path component holding `*` or `?`, so `*`,
# `[0-9]*`, `1*`, `1?`); 6 = `thread-self` (an alias of `self`); 7 = `$$` / `$!`.  Not covered (known limits, SC-22 22bh): brace expansion, a bare
# bracket class without `*` / `?`, a back-quote command substitution, path normalisation (`/proc/./self`, `//`).
PID_ALTS = ["self", "[0-9]+", "[^/[:space:]]*[*?][^/[:space:]]*", "\\$\\{[^}]*\\}", "\\$[A-Za-z_][A-Za-z0-9_]*", "\\$\\([^)]*\\)",
            "thread-self", "\\$[$!]"]
EXT_READER_EXTRA = None


def drop(lst, x, what):
    assert x in lst, f"{what}: {x!r} not in {lst}"
    return [y for y in lst if y != x]


readers, extreaders, launch, proc_old, proc_new = list(READERS), list(READERS), list(LAUNCH), list(PROC_OLD), list(PROC_NEW)
remote, kwpos, ps_alts, pid_alts = dict(REMOTE), list(KWPOS), list(PS_ALTS), list(PID_ALTS)
interps = {"python3": "python3?[[:space:]]+-c", "node": "node[[:space:]]+-e"}
if vname == "drop_reader":
    readers = drop(readers, varg, "reader"); extreaders = drop(extreaders, varg, "reader")
if vname == "drop_extreader":
    extreaders = drop(extreaders, varg, "extreader")
if vname == "drop_launch":
    launch = drop(launch, varg, "launch")
if vname == "drop_procreader":
    if varg in proc_old:
        proc_old = drop(proc_old, varg, "procreader")
    else:
        proc_new = drop(proc_new, varg, "procreader")
if vname == "drop_remote":
    assert varg in remote, varg
    remote.pop(varg)
if vname == "drop_psalt":
    i = int(varg)
    ps_alts = ps_alts[:i - 1] + ps_alts[i:]
if vname == "drop_pid":
    i = int(varg)
    pid_alts = pid_alts[:i] + pid_alts[i + 1:]
if vname == "pidtok_placeholders":
    pid_alts = pid_alts + ["\\[[^]/[:space:]]*\\]", "\\{[^}/[:space:]]*\\}"]
if vname == "pidtok_any":
    pid_alts = ["[^/[:space:]$]+", "\\$\\{[^}]*\\}", "\\$[A-Za-z_][A-Za-z0-9_]*", "\\$\\([^)]*\\)"]
if vname == "drop_kwpos":
    kwpos = drop(kwpos, varg, "kwpos")
if vname == "drop_interp":
    assert varg in interps, varg
    interps.pop(varg)

SQ = "'\"'\"'"            # a single quote inside a single-quoted bash string
BIN = "" if vname == "drop_bin" else "(/[^[:space:]|;&\"" + SQ + "`$()<>]*/)?"
if vname == "drop_larg":
    LARG = "(-[^[:space:]]*|[0-9]+)"
else:
    LARG = ("(-[^[:space:]]+([[:space:]]+[^-[:space:]|;&()<>`\"" + SQ + "][^[:space:]|;&()<>`\"" + SQ + "]*)?"
            "|[0-9][0-9.]*[smhd]?|[A-Za-z_][A-Za-z0-9_]*=[^[:space:]]*)")
PGREP_ALTS, PSTREE_ALTS = ["-[a-zA-Z]*a", "--list-full"], ["-[a-zA-Z]*a", "--arguments"]
if vname == "pgrep_wide":
    PGREP_ALTS = PGREP_ALTS + ["-[a-zA-Z]*f"]
if vname == "drop_pgrep":
    PGREP_ALTS = PGREP_ALTS[:int(varg)] + PGREP_ALTS[int(varg) + 1:]
if vname == "drop_pstree":
    PSTREE_ALTS = PSTREE_ALTS[:int(varg)] + PSTREE_ALTS[int(varg) + 1:]
KWPOS_RE = "" if not kwpos else "((" + "|".join(kwpos) + ")[[:space:]]+)?"
_ANCHOR = "(^|[;&|(){]|`)" if vname == "anchor_nocntrl" else "(^|[;&|(){]|`|[[:cntrl:]])"
_dk_tool = "docker" if vname == "nodocker_podman" else "(docker|podman)"
_dk_tops = [a for a in ("compose", "container") if not (vname == "drop_dockerform" and varg == ({"compose": "compose", "container": "ctop"}[a]))]
_dk_compose = "((" + "|".join(_dk_tops) + ")[[:space:]]+)?" if _dk_tops else ""
_dk_container = "" if (vname == "drop_dockerform" and varg == "container") else "(container[[:space:]]+)?"
_dk_psls = "ps" if (vname == "drop_dockerform" and varg == "ls") else "(ps|ls)"
_dk_top = "" if (vname == "drop_dockerform" and varg == "top") else _dk_tool + "[[:space:]]+" + _dk_compose + "top([^[:alnum:]_-]|$)"
_dk_nt = "" if (vname == "drop_dockerform" and varg == "notrunc") else _dk_tool + "[[:space:]]+" + _dk_container + _dk_psls + "[[:space:]]+([^|;&]*[[:space:]])?--no-trunc"
DOCKER_RE = "|".join(x for x in (_dk_top, _dk_nt) if x)
PIDTOK = "(" + "|".join(pid_alts) + ")"
READERS_RE = "|".join(readers)
EXT_READER_RE = ("(^|[^[:alnum:]_.-])((" + "|".join(extreaders) + ")[[:space:]]|(" + "|".join(v for v in interps.values()) + ")([[:space:]]|$))")
INTERP_NAME_ALT = lambda extra: "(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG}|${_SG_SRVCFG}" + extra + ")"


def compose(launch_, ps_alts_, remote_, env_remote_=None, ps_only_launch=False):
    """the pieces of the process-table definition for one set of tables.  The RULE ROWS use compose(<the real tables>); the shell variables that the
    tight-credit condition reads are normally the same text, and only the `tdrop_*` / `tight_*` drift variants make the two copies differ."""
    launch_re = "(" + "|".join(launch_) + ")"
    ps_args = "(" + "|".join(ps_alts_) + ")"
    ps_part = "ps[[:blank:]]+" + ps_args
    other_part = ("pgrep[[:blank:]]+([^|;&]*[[:blank:]])?(" + "|".join(PGREP_ALTS) + ")"
                  "|pstree[[:blank:]]+([^|;&]*[[:blank:]])?(" + "|".join(PSTREE_ALTS) + ")|top[[:blank:]]+([^|;&]*[[:blank:]])?-[a-zA-Z]*c")
    ps_cmd = "(" + BIN + "(" + ps_part + "|" + other_part + "))"
    lpfx = "(" + BIN + launch_re + "([[:space:]]+" + LARG + ")*[[:space:]]+)"
    if ps_only_launch:
        proctab = _ANCHOR + "[[:blank:]]*" + KWPOS_RE + "((" + lpfx + "?" + BIN + "(" + ps_part + ")|" + BIN + "(" + other_part + ")))"
    else:
        proctab = _ANCHOR + "[[:blank:]]*" + KWPOS_RE + lpfx + "?" + ps_cmd
    if vname == "launcher_any":
        # bad implementation (over-broad): ANY command behind a launcher is a process-table command
        proctab = _ANCHOR + "[[:blank:]]*" + KWPOS_RE + lpfx + "[a-z]+"
    env_part = ("printenv([[:space:]" + SQ + "\"]|[;&|)}<>`]|$)" "|env([[:blank:]]*($|[;&|)}<>" + SQ + "\"`]))")
    sep = "[[:space:]" + SQ + "\"(`]"
    if env_remote_ is None and vname == "remote_anchored":
        remote_re = _ANCHOR + "[[:blank:]]*(" + "|".join(remote_.values()) + ")[^|]*" + sep + "(" + ps_cmd + "|" + env_part + ")"
    elif env_remote_ is None:
        remote_re = "(" + "|".join(remote_.values()) + ")[^|]*" + sep + "(" + ps_cmd + "|" + env_part + ")"
    else:    # `remote_env_split`: the ps alternative keeps every wrapper, the env / printenv alternative uses `env_remote_`
        remote_re = ("(" + "(" + "|".join(remote_.values()) + ")[^|]*" + sep + "(" + ps_cmd + ")|"
                     "(" + "|".join(env_remote_.values()) + ")[^|]*" + sep + "(" + env_part + "))")
    # v5 (R4 F cluster): the TIGHT copy holds the ps family only.  The env / printenv dump alternative of the wrappers is in the rule row but NOT in the tight predicate: a dump
    # followed by a row-level filter keeps the credit it has at baseline for `docker|kubectl|podman|lxc exec ... env` (anchored grep / cut / sed / grep -v count)
    if vname == "remote_anchored":
        remote_t = _ANCHOR + "[[:blank:]]*(" + "|".join(remote_.values()) + ")[^|]*" + sep + "(" + ps_cmd + ")"
    else:
        remote_t = "(" + "|".join(remote_.values()) + ")[^|]*" + sep + "(" + ps_cmd + ")"
    return {"PS_ARGS": ps_args, "PS_CMD": ps_cmd, "PROCTAB": proctab, "REMOTE": remote_re, "REMOTE_T": remote_t}


def make_vars(pieces):
    vb = r"""
# ── secret-net-l3-and-bypass-paths prototype: shared names (single definition, several consumers) ──
# W8: server-side config (Forgejo / Gitea app.ini).
_SG_SRVCFG='[A-Za-z0-9._-]*(forgejo|gitea)[^[:space:]|;&"'"'"']*app\.ini|custom/conf/app\.ini'
_SG_READERS_PRINT='@READERS@'
# W11: process-table enumeration (argv / environ exposing forms). comm-only forms stay allowed.
_SG_BIN='@BIN@'
_SG_PS_ARGS='@PS_ARGS@'
_SG_PS_CMD='@PS_CMD@'
_SG_PROCTAB='@PROCTAB@'
_SG_PS_REMOTE='@REMOTE@'
_SG_PS_REMOTE_T='@REMOTE_T@'
_SG_PS_DOCKER='@DOCKER@'
_SG_PROCTAB_ALL="(${_SG_PROCTAB}|${_SG_PS_REMOTE_T}|${_SG_PS_DOCKER})"
_SG_PIDTOK='@PIDTOK@'
"""
    for k, v in (("@READERS@", READERS_RE), ("@BIN@", BIN), ("@PS_ARGS@", pieces["PS_ARGS"]), ("@PS_CMD@", pieces["PS_CMD"]), ("@PROCTAB@", pieces["PROCTAB"]),
                 ("@REMOTE@", pieces["REMOTE"]), ("@REMOTE_T@", pieces["REMOTE_T"]), ("@DOCKER@", DOCKER_RE), ("@PIDTOK@", PIDTOK)):
        vb = vb.replace(k, v)
    return vb


# env / printenv dump wrappers: normally the same set as the ps wrappers; `remote_env_split:X` drops X from the dump alternative only
env_remote = None
if vname in ("remote_env_split", "drop_envwrap"):
    assert varg in remote, varg
    env_remote = {k: v for k, v in remote.items() if k != varg}
ROW_PIECES = compose(launch, ps_alts, remote, env_remote, vname == "launcher_ps_only")
vars_block_rows = make_vars(ROW_PIECES)                 # the text the three inline rows are made of
DEF_PIECES = dict(ROW_PIECES)
# --- drift variants: the TIGHT copy (shell variables) differs from the rule rows
if vname == "tdrop_launch":
    DEF_PIECES = compose(drop(launch, varg, "tdrop_launch"), ps_alts, remote, env_remote)
elif vname == "tdrop_remote":
    assert varg in remote, varg
    DEF_PIECES = compose(launch, ps_alts, {k: v for k, v in remote.items() if k != varg}, env_remote)
elif vname == "tdrop_psalt":
    _i = int(varg)
    DEF_PIECES = compose(launch, ps_alts[:_i - 1] + ps_alts[_i:], remote, env_remote)
vars_block = make_vars(DEF_PIECES)
_PTALL = '_SG_PROCTAB_ALL="(${_SG_PROCTAB}|${_SG_PS_REMOTE_T}|${_SG_PS_DOCKER})"'
if vname == "env_tight":           # bad implementation: the dump alternative is part of the tight predicate too (every row-level filter after a wrapped dump is no credit)
    vars_block = vars_block.replace(_PTALL, '_SG_PROCTAB_ALL="(${_SG_PROCTAB}|${_SG_PS_REMOTE}|${_SG_PS_DOCKER})"')
if vname == "tight_plainps":
    vars_block = vars_block.replace(_PTALL, "_SG_PROCTAB_ALL='^[[:space:]]*ps[[:space:]]'")
if vname == "tight_without":
    _part = {"PROCTAB": "${_SG_PROCTAB}", "REMOTE": "${_SG_PS_REMOTE_T}", "DOCKER": "${_SG_PS_DOCKER}"}[varg]
    _all = ["${_SG_PROCTAB}", "${_SG_PS_REMOTE_T}", "${_SG_PS_DOCKER}"]
    vars_block = vars_block.replace(_PTALL, '_SG_PROCTAB_ALL="(' + "|".join(x for x in _all if x != _part) + ')"')
rep('_SG_PP_SUFFIX="(^|[[:space:]\\"\'=/*A-Za-z0-9_.-])"\n', '_SG_PP_SUFFIX="(^|[[:space:]\\"\'=/*A-Za-z0-9_.-])"\n' + vars_block)

# ------------------------------------------------------------------ B. credit: tight set + anchored jq forms (W8 / W11 / W9 / W12)
rep('''  local tight=0
  if [[ "$seg" =~ ($_SG_CLAUDE_CFG) ]]; then
    tight=1
  fi
''', '''  local tight=0
  if [[ "$seg" =~ ($_SG_CLAUDE_CFG|$_SG_SRVCFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]@TIGHTARG@; then
    tight=1
  fi
''')
src = src.replace("@TIGHTARG@", ' || [[ "${2:-}" == tight ]]' if vname == "ext_v4stage" else "")
if vname == "notight":
    src = src.replace('[[ "$seg" =~ ($_SG_CLAUDE_CFG|$_SG_SRVCFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]', '[[ "$seg" =~ ($_SG_CLAUDE_CFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]', 1)
if vname == "claude_notight":
    src = src.replace('[[ "$seg" =~ ($_SG_CLAUDE_CFG|$_SG_SRVCFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]', '[[ "$seg" =~ ($_SG_SRVCFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]', 1)
if vname == "proc_nocredit":
    _t = '  local tight=0\n  if [[ "$seg" =~ ($_SG_CLAUDE_CFG|$_SG_SRVCFG) ]]'
    assert src.count(_t) == 1
    src = src.replace(_t, '  [[ "$seg" =~ $_SG_PROCTAB_ALL ]] && return 1\n' + _t, 1)
if vname == "notight_proc":
    _t = ' || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]'
    assert src.count(_t) == 1
    src = src.replace(_t, '', 1)
if vname == "notight_ini":
    src = src.replace('[[ "$seg" =~ ($_SG_CLAUDE_CFG|$_SG_SRVCFG) ]]', '[[ "$seg" =~ ($_SG_CLAUDE_CFG) ]]', 1)
if vname == "tight_ini_literal":
    src = src.replace('($_SG_CLAUDE_CFG|$_SG_SRVCFG)', '($_SG_CLAUDE_CFG|/etc/forgejo/app\\.ini)', 1)
if vname == "proc_tight":
    src = src.replace('|| [[ "$seg" =~ $_SG_PROCTAB_ALL ]]', '|| [[ "$seg" =~ $_SG_PROCTAB_ALL ]] || [[ "$seg" =~ /proc/[^[:space:]]*(environ|cmdline) ]]', 1)
if vname == "jq_loose":
    _old = "(keys|length|paths|leaf_paths)[\\\"']?[[:space:]]*(\\$|\\|)"
    assert src.count(_old) == 1, src.count(_old)
    src = src.replace(_old, "(keys|keys_unsorted|length|paths|leaf_paths)[\\\"']?[[:space:]]*(\\$|\\|)", 1)

rep('''  # Whitelisted: `jq '{alias: .safe_field}'` — single-line allowlist projection.''',
    '''  # W12: anchored metadata-only forms: quoted program, optional simple dotted-path prefix, ONE token, closing quote.
  if _sg_line_match "\\|[[:space:]]*jq([[:space:]]+(-[a-zA-Z]+|--[a-z-]+))*[[:space:]]+[\\"'](\\.[A-Za-z_][A-Za-z0-9_.]*[[:space:]]*\\|[[:space:]]*)?(keys_unsorted|map_values\\(length\\))[\\"'][[:space:]]*(\\$|\\|)" "$seg"; then
    has_filter=1
  fi
  # Whitelisted: `jq '{alias: .safe_field}'` — single-line allowlist projection.''')

# ------------------------------------------------------------------ C. new functions above the sourcing gate
def after(var, pre, pat):
    """bash text for 'the remainder of $var after its first occurrence of $pat' ($pre = the text before that occurrence).
    v3: by length (linear).  variant vx_quadratic: the shortest-prefix removal ${var#*"$pat"} (quadratic when the hit sits late in a long string)."""
    if vname == "vx_quadratic":
        return '${%s#*"$%s"}' % (var, pat)
    return '${%s:$(( ${#%s} + ${#%s} ))}' % (var, pre, pat)


max_assign = {"vx_assign15": 15, "vx_assign17": 17}.get(vname, 16)
max_repl = {"vx_repl7": 7, "vx_repl9": 9}.get(vname, 8)
max_occ = {"ext_occ63": 63, "ext_occ65": 65}.get(vname, 64)
max_entries = {"ext_max199": 199, "ext_max201": 201}.get(vname, 200)
max_size = {"ext_size32767": 32767, "ext_size32769": 32769}.get(vname, 32768)
min_len = {"ext_minlen3": 3, "ext_minlen5": 5}.get(vname, 4)
max_len = {"ext_maxlen199": 199, "ext_maxlen201": 201}.get(vname, 200)

funcs = r'''
# ── W10 (prototype): literal-assignment expansion. Second pass runs only after EVERY built-in verdict allowed. ──
_SGV_N=(); _SGV_V=()
_SG_SUB=""
# portable literal replace-all (prefix / suffix concatenation; NO ${x//p/r}: bash 5.2 patsub_replacement and the quote
# semantics of bash < 4.3 disagree about quotes and '&' inside the replacement). at most @MAXREPL@ replacements.
# the remainder after a hit is taken BY LENGTH (${s:N}), never with ${s#*"$pat"}: that form is O(n^2) when the hit sits late in a long string.
_SG_RP=""
_sg_vx_replace() {
  local s="$1" pat="$2" rep="$3" out="" g=0 pre
  while (( g < @MAXREPL@ )) && [[ "$s" == *"$pat"* ]]; do
    g=$((g+1)); pre="${s%%"$pat"*}"; out="${out}${pre}${rep}"; s="@AFTER_REPLACE@"
  done
  _SG_RP="${out}${s}"
}
_sg_vx_collect() {
  local rest="$1" m name val i j n=0 dup pre
  local _q="'" _d='"' _b='`'
  _SGV_N=(); _SGV_V=()
  [[ "$rest" == *'$'* && "$rest" == *=* ]] || [[ "$rest" == *'$'* && "$rest" == *' in '* ]] || return 0
  local re="(^|[;&|[:space:](${_d}${_b}${_q}])((@ASSIGNKW@)[[:space:]]+(-[a-zA-Z]+[[:space:]]+)*)?([A-Za-z_][A-Za-z0-9_]*)=(@QUOTEDVAL@\\\$\\([^)]*\\)|${_b}[^${_b}]*${_b}|[^[:space:];&|)${_d}${_b}${_q}]*)"
  while (( n < @MAXASSIGN@ )) && [[ "$rest" =~ $re ]]; do
    (( n += 1 ))
    m="${BASH_REMATCH[0]}"; name="${BASH_REMATCH[5]}"; val="${BASH_REMATCH[6]}"
    pre="${rest%%"$m"*}"; rest="@AFTER_COLLECT@"
    [[ "$val" == \"*\" && ${#val} -ge 2 ]] && val="${val:1:${#val}-2}"
    [[ "$val" == \'*\' && ${#val} -ge 2 ]] && val="${val:1:${#val}-2}"
    [[ -z "$val" || "$val" == *"\$$name"* || "$val" == *"\${$name}"* ]] && continue
    dup=0
    for (( i = 0; i < ${#_SGV_N[@]}; i++ )); do
      [[ "${_SGV_N[i]}" == "$name" && "${_SGV_V[i]}" == "$val" ]] && dup=1
    done
    (( dup )) || { _SGV_N+=("$name"); _SGV_V+=("$val"); }
  done
  rest="$1"; n=0
  local rf="(^|[;&|[:space:](])for[[:space:]]+([A-Za-z_][A-Za-z0-9_]*)[[:space:]]+in[[:space:]]+([^;&|)]*)"
  while (( n < 8 )) && [[ "$rest" =~ $rf ]]; do
    (( n += 1 ))
    m="${BASH_REMATCH[0]}"; name="${BASH_REMATCH[2]}"; val="${BASH_REMATCH[3]}"
    pre="${rest%%"$m"*}"; rest="@AFTER_COLLECT@"
    [[ -z "$val" ]] && continue
    _SGV_N+=("$name"); _SGV_V+=("$val")
  done
  for (( i = 0; i < ${#_SGV_N[@]}; i++ )); do
    for (( j = 0; j < ${#_SGV_N[@]}; j++ )); do
      (( i == j )) && continue
      _sg_vx_replace "${_SGV_V[i]}" "\${${_SGV_N[j]}}" "${_SGV_V[j]}"; _SGV_V[i]="$_SG_RP"
      _sg_vx_replace "${_SGV_V[i]}" "\$${_SGV_N[j]}" "${_SGV_V[j]}"; _SGV_V[i]="$_SG_RP"
    done
  done
  return 0
}
_sg_vx_apply() {
  local s="$1" i n v m tail pre post guard changed=1
  _SG_SUB="$s"
  (( ${#_SGV_N[@]} )) || return 1
  [[ "$s" == *'$'* ]] || return 1
  for (( i = 0; i < ${#_SGV_N[@]}; i++ )); do
    n="${_SGV_N[i]}"; v="${_SGV_V[i]}"
    if [[ "$s" == *"\${$n}"* ]]; then _sg_vx_replace "$s" "\${$n}" "$v"; s="$_SG_RP"; changed=0; fi
    guard=0
    while (( guard < @MAXREPL@ )) && [[ "$s" =~ \$${n}([^A-Za-z0-9_]|$) ]]; do
      (( guard += 1 ))
      m="${BASH_REMATCH[0]}"; tail="${BASH_REMATCH[1]}"
      if [[ -z "$tail" ]]; then pre="${s%"$m"}"; post=""; else pre="${s%%"$m"*}"; post="@AFTER_APPLY@"; fi
      [[ "$pre" == *\\ ]] && pre="${pre%\\}"
      s="${pre}${v}${tail}${post}"; changed=0
    done
  done
  _SG_SUB="$s"
  return $changed
}
# _sg_vx_pass CMD MODE : judge substituted copies. Entry point named in the Spec (fault / ordering probes hook it).
_sg_vx_pass() {
  local cmd="$1" mode="$2" seg rc
  _sg_vx_collect "$cmd"
  (( ${#_SGV_N[@]} )) || return 0
  if [[ "$mode" == whole ]]; then
    if _sg_vx_apply "$cmd"; then _sg_judge_one "$_SG_SUB" whole; return $?; fi
    return 0
  fi
  for seg in "${_SG_SEGS[@]}"; do
    if _sg_vx_apply "$seg"; then
      _sg_judge_one "$_SG_SUB" segment
      rc=$?
      [[ $rc -ne 0 ]] && return "$rc"
    fi
  done
  return 0
}

# ── W9 (prototype): project-level extension .aria/secret-guard.paths. ALL extension code lives in _sg_ext_* functions
#    that run ONLY inside command substitutions: any internal error (set -u, exit, command not found) kills that
#    subshell only; the caller maps the output to "BLOCK" or "nothing". ──
@EXTREADERDEF@_sg_ext_root() {   # prints the project root (CLAUDE_PROJECT_DIR, else stdin cwd) or nothing
  local r="${CLAUDE_PROJECT_DIR:-}"
  if [[ -z "$r" && "$input" == *'"cwd"'* ]]; then
    r="$(printf '%s' "$input" | jq -r '.cwd // ""' 2>/dev/null | tr -d '\r')"
  fi
  printf '%s' "$r"
}
_sg_ext_entries() {   # prints the valid entries (lower-cased, one per line); prints nothing when the extension is not in effect
  local root f size
  @LCSET@
  root="$(_sg_ext_root)"
  [[ -n "$root" ]] || return 0
  f="$root/.aria/secret-guard.paths"
  [[ -f "$f" && -r "$f" ]] || return 0
  size="$(wc -c < "$f" | tr -d ' ')"
  (( size <= @MAXSIZE@ )) || return 0
  tr -d '\000' < "$f" | cmp -s - "$f" || return 0
  local out
  out="$(tr -d '\r' < "$f" | tr '[:upper:]' '[:lower:]' | @FILTER@)"
  @EMPTYGUARD@
  local n
  n="$(printf '%s\n' "$out" | wc -l | tr -d ' ')"
  if (( n > @MAXENTRIES@ )); then
    if [[ "$SGVARIANT" == ext_trunc ]]; then printf '%s\n' "$out" | head -n @MAXENTRIES@; fi
    return 0
  fi
  printf '%s\n' "$out"
}
@W9CORE@
_sg_ext_path_pass() {   # Read/Edit face: entry (lower-cased) as a literal substring of the path (grep -F -i, one pass)
  local p="$1"
  @LCSET@
  @PATHHIT@
  return 0
}
'''
# ---- W9 v5 pieces: the byte-semantics scope, the entry reader's filter, the substitution core, and the bad implementations
_APPINI_TOKEN = "/etc/gitea/app.ini"       # the built-in app.ini name the entry occurrences are replaced by (no `forgejo` word: that word sits in other built-in rows)
if vname == "ext_subst_forgejo":
    _APPINI_TOKEN = "/etc/forgejo/app.ini"
_SEP = "" if vname == "ext_subst_nosep" else " "       # one blank after the token: the right boundary of the name group holds even when the entry is followed by a word character
LCSET = "local -x LC_ALL=C"
if vname == "ext_localnoexp":
    LCSET = "local LC_ALL=C"          # bad implementation: not exported when the environment has no LC_ALL, so the children (sed / grep) keep the caller's locale
elif vname in ("ext_noc", "ext_charlen"):
    LCSET = ":"                       # bad implementation: no byte semantics at all (characters counted, ranges and case folding by the caller's locale)
_FILT = []
if vname != "ext_nobom":
    _FILT.append("-e $'1s/^\\xef\\xbb\\xbf//'")
if vname != "ext_nostrip":
    _FILT += ["-e 's/^[[:space:]]+//'", "-e 's/[[:space:]]+$//'"]
_FILT.append("-e '/^#/d'")
_FILT.append("-e '/^.{@MINLEN@,@MAXLEN@}$/!d'")
if vname == "ext_ascii_only":         # bad implementation: the entry must hold an ASCII letter or digit (a pure non-ASCII entry is skipped)
    _FILT.append("-e '/[a-z0-9]/!d'")
elif vname != "ext_nosym":
    _FILT.append("-e $'/[a-z0-9\\x80-\\xff]/!d'")
FILTER = "sed -E " + " ".join(_FILT)
EMPTYGUARD = "" if vname == "ext_emptypat" else '[[ -n "$out" ]] || return 0'
HITS = '''hits="$(grep -oFib -f <(_sg_ext_entries) <(printf '%s' "$text") 2>/dev/null)"'''
PATHHIT = '''if grep -qFi -f <(_sg_ext_entries) <(printf '%s' "$p") 2>/dev/null; then printf 'BLOCK'; fi'''
if vname == "ext_eval":       # bad implementation: the grep argument list is built as TEXT and eval'd -- a command substitution inside an entry runs
    HITS = '''local _a="" _e; while IFS= read -r _e; do _a="$_a -e \\"$_e\\""; done < <(_sg_ext_entries)
  hits="$(eval "grep -oFib $_a <<< \\"\\$text\\"" 2>/dev/null)"'''
    PATHHIT = '''local _a="" _e; while IFS= read -r _e; do _a="$_a -e \\"$_e\\""; done < <(_sg_ext_entries)
  if eval "grep -qFi $_a <<< \\"\\$p\\"" 2>/dev/null; then printf 'BLOCK'; fi'''
if vname == "ext_glob":       # bad implementation: unquoted loop over the entries -- word splitting and file-name globbing of the entries
    HITS = '''hits=""; local _e _h
  for _e in $(_sg_ext_entries); do _h="$(printf '%s' "$text" | grep -oFib -e "$_e" 2>/dev/null)"; [[ -n "$_h" ]] && hits="${hits:+$hits$'\\n'}${_h}"; done'''
    PATHHIT = '''local _e
  for _e in $(_sg_ext_entries); do if printf '%s' "$p" | grep -qFi -e "$_e" 2>/dev/null; then printf 'BLOCK'; return 0; fi; done'''
if vname == "ext_regex":      # bad implementation: the entries are handed to grep as extended regular expressions
    HITS = HITS.replace("grep -oFib", "grep -oEib")
    PATHHIT = PATHHIT.replace("grep -qFi", "grep -qEi")
if vname == "ext_perentry":   # timing bad implementation, the per-entry process class: one grep process per extension entry (Bash and Read faces)
    HITS = '''hits=""; local _e _h
  while IFS= read -r _e; do _h="$(printf '%s' "$text" | grep -oFib -e "$_e" 2>/dev/null)"; [[ -n "$_h" ]] && hits="${hits:+$hits$'\\n'}${_h}"; done < <(_sg_ext_entries)'''
    PATHHIT = '''local _e
  while IFS= read -r _e; do
    if printf '%s' "$p" | grep -qFi -e "$_e" 2>/dev/null; then printf 'BLOCK'; return 0; fi
  done < <(_sg_ext_entries)'''
_LCSUBST = LCSET
if vname == "ext_charslice":          # bad implementation (offset and slice in different units): grep runs in C and gives BYTE offsets, the slicing runs in the hook's locale
    _LCSUBST = ":"
    HITS = HITS.replace("grep -oFib", "LC_ALL=C grep -oFib")
_ONLYFIRST = "break" if vname == "ext_subst_first" else ":"      # bad implementation: only the first occurrence is replaced
W9CORE_S = r'''# _sg_ext_subst TEXT : TEXT with the first @MAXOCC@ occurrences of any entry (fixed strings, one grep pass, case-insensitive) replaced by the built-in app.ini name;
# prints nothing when no entry occurs.  Byte semantics: `grep -b` gives BYTE offsets, so the slicing counts bytes too (LC_ALL=C, exported).
_sg_ext_subst() {
  local text="$1" hits line off match out="" pos=0 n=0
  @LCSUBST@
  @HITS@
  [[ -n "$hits" ]] || return 0
  while IFS= read -r line; do
    n=$((n+1)); (( n > @MAXOCC@ )) && break
    off="${line%%:*}"; match="${line#*:}"
    out="${out}${text:pos:off-pos}@TOKEN@"
    pos=$(( off + ${#match} ))
    @ONLYFIRST@
  done <<< "$hits"
  printf '%s' "${out}${text:pos}"
}
# _sg_ext_pass TEXT : the BUILT-IN judgement (_sg_core_eval: _sg_safe_to_split / _sg_split_top / _sg_judge_one, tight credit by the app.ini name) of the substituted copy
_sg_ext_pass() {
  local sub
  sub="$(_sg_ext_subst "$1")"
  [[ -n "$sub" ]] || return 0
  _sg_core_eval "$sub" >/dev/null 2>&1
  [[ $? -eq 2 ]] && printf 'BLOCK'
  return 0
}
'''
W9CORE_S = (W9CORE_S.replace("@LCSUBST@", _LCSUBST).replace("@HITS@", HITS).replace("@ONLYFIRST@", _ONLYFIRST)
            .replace("@TOKEN@", _APPINI_TOKEN + _SEP))
if vname == "ext_perocc_judge":       # timing bad implementation: one full built-in judgement per occurrence (64 passes instead of one)
    W9CORE_S = r'''_sg_ext_pass() {
  local text="$1" hits line off match sub n=0
  local -x LC_ALL=C
  hits="$(grep -oFib -f <(_sg_ext_entries) <(printf '%s' "$text") 2>/dev/null)"
  [[ -n "$hits" ]] || return 0
  while IFS= read -r line; do
    n=$((n+1)); (( n > @MAXOCC@ )) && break
    off="${line%%:*}"; match="${line#*:}"
    sub="${text:0:off}@TOKEN@${text:$(( off + ${#match} ))}"
    ( unset LC_ALL; _sg_core_eval "$sub" >/dev/null 2>&1 ); [[ $? -eq 2 ]] && { printf 'BLOCK'; return 0; }
  done <<< "$hits"
  return 0
}
'''.replace("@TOKEN@", _APPINI_TOKEN + _SEP)
if vname == "ext_nocut":       # bad implementation: no stage logic at all -- a reader word ANYWHERE in the command plus an entry ANYWHERE = block (separators outside quotes do not cut)
    W9CORE_S = r'''_sg_ext_pass() {
  local text="$1"
  local -x LC_ALL=C
  if grep -qFi -f <(_sg_ext_entries) <(printf '%s' "$text") 2>/dev/null && [[ "$text" =~ (^|[^A-Za-z0-9_])(cat|head|tail|sed|grep|awk|less|more|strings|python3|node)([^A-Za-z0-9_]|$) ]]; then printf 'BLOCK'; fi
  return 0
}
'''
EXTREADERDEF = ""
if vname == "ext_v4stage" or vname.startswith("ext_v4stage"):     # the previous design, kept as a bad implementation: a hand-written quote mask + stage cut per occurrence
    EXTREADERDEF = "_SG_EXT_READER_RE='@EXTREADER@'\n"
    W9CORE_S = r'''# _sg_ext_mask TEXT : TEXT with every ; & | and newline that sits INSIDE quotes replaced by a space (same byte length).
_sg_ext_mask() {
@MASKFN@
}
# _sg_ext_pass TEXT : whole-command check by a hand-written stage cut (the previous design).  prints BLOCK on a hit.
_sg_ext_pass() {
  local text="$1" hits line off match before stage tail segtxt n=0
  local -x LC_ALL=C
  hits="$(grep -oFib -f <(_sg_ext_entries) <(printf '%s' "$text") 2>/dev/null)"
  [[ -n "$hits" ]] || return 0
  local lc
  lc="$(printf '%s' "$text" | tr '[:upper:]' '[:lower:]')"
  lc="$(_sg_ext_mask "$lc")"
  while IFS= read -r line; do
    n=$((n+1)); (( n > @MAXOCC@ )) && break
    off="${line%%:*}"; match="${line#*:}"
    match="$(printf '%s' "$match" | tr '[:upper:]' '[:lower:]')"
    before="${lc:0:off}"
    stage="${before##*[;&|$'\n']}"
    tail="${lc:$((off + ${#match}))}"; tail="${tail%%[;&$'\n']*}"
    if [[ "$stage" =~ $_SG_EXT_READER_RE ]]; then
      segtxt="${stage}${match}${tail}"
      if ! _sg_compute_credit "$segtxt" tight; then
        printf 'BLOCK'
        return 0
      fi
    fi
  done <<< "$hits"
  return 0
}
'''
    _MC = "';'|'&'|'|'|$'\\n'"
    _MALL = ""
    _drop = {"noesc_q": "q", "noesc_all": "all", "noansi": "ansi", "nopipe": "pipe", "nonl": "nl"}
    _arg = varg
    _bs_u = "          '\\') _o=\"${_o}${_s:_i:2}\"; (( _i += 2 )); continue ;;\n"
    _bs_q = "           '\\') _o=\"${_o}${_c}\"; (( _i += 1 )); _c=\"${_s:_i:1}\"; case \"$_c\" in @MC@) _c=' ' ;; esac ;;\n"
    _dollar = "          '$') if [[ \"${_s:_i+1:1}\" == \"'\" ]]; then _st=d; _o=\"${_o}${_s:_i:2}\"; (( _i += 2 )); continue; fi ;;\n"
    MASKFN = r'''  local _s="$1" _n=${#1} _i=0 _c _st=u _o=""
  while (( _i < _n )); do
    _c="${_s:_i:1}"
    case "$_st" in
      u)
        case "$_c" in
@UBS@@UDOLLAR@          "'") _st=s ;;
          '"') _st=q ;;
        esac ;;
      s) case "$_c" in "'") _st=u ;; @MC@) _c=' ' ;; esac ;;
      q) case "$_c" in
@QBS@           '"') _st=u ;;
           @MC@) _c=' ' ;;
         esac ;;
      d) case "$_c" in
@QBS@           "'") _st=u ;;
           @MC@) _c=' ' ;;
         esac ;;
    esac
    _o="${_o}${_c}"; (( _i += 1 ))
  done
  printf '%s' "$_o"'''
    _ubs, _qbs, _ud = _bs_u, _bs_q, _dollar
    if _arg == "noesc_q":
        _qbs = ""
    elif _arg == "noesc_all":
        _qbs = ""; _ubs = ""
    elif _arg == "noansi":
        _ud = ""
    if _arg == "nopipe":
        _MC = "';'|'&'|$'\\n'"
    elif _arg == "nonl":
        _MC = "';'|'&'|'|'"
    MASKFN = MASKFN.replace("@UBS@", _ubs).replace("@UDOLLAR@", _ud).replace("@QBS@", _qbs).replace("@MC@", _MC)
    W9CORE_S = W9CORE_S.replace("@MASKFN@", MASKFN)
assign_kw = "export|declare|local|readonly|typeset"
if vname == "drop_assign":
    kws = assign_kw.split("|")
    assert varg in kws, varg
    assign_kw = "|".join(k for k in kws if k != varg)
if vname == "vx_start_only":
    # bad implementation: an assignment is recognised only at the start of a segment / after a separator -- no whitespace boundary, so a
    # declaration prefix (export declare local readonly typeset, with options) hides the assignment
    _o = "(^|[;&|[:space:](${_d}${_b}${_q}])((@ASSIGNKW@)"
    assert funcs.count(_o) == 1
    funcs = funcs.replace(_o, "(^|[;&|(${_d}${_b}${_q}])((@ASSIGNKW@)")
quoted = "" if vname == "vx_noquote" else "${_d}([^${_d}]*)${_d}|${_q}([^${_q}]*)${_q}|"
for k, v in (("@W9CORE@", W9CORE_S), ("@EXTREADERDEF@", EXTREADERDEF), ("@LCSET@", LCSET), ("@FILTER@", FILTER), ("@AFTER_REPLACE@", after("s", "pre", "pat")),
             ("@AFTER_COLLECT@", after("rest", "pre", "m")), ("@AFTER_APPLY@", after("s", "pre", "m")),
             ("@MAXREPL@", str(max_repl)), ("@MAXASSIGN@", str(max_assign)), ("@MAXOCC@", str(max_occ)), ("@MAXSIZE@", str(max_size)),
             ("@MINLEN@", str(min_len)), ("@MAXLEN@", str(max_len)), ("@MAXENTRIES@", str(max_entries)),
             ("@EXTREADER@", EXT_READER_RE), ("@ASSIGNKW@", assign_kw), ("@QUOTEDVAL@", quoted),
             ("@PATHHIT@", PATHHIT), ("@EMPTYGUARD@", EMPTYGUARD)):
    funcs = funcs.replace(k, v)
rep('# Unit-test sourcing gate (#128): when sourced (not executed), stop here —', funcs + '\n# Unit-test sourcing gate (#128): when sourced (not executed), stop here —')
rep('set -uo pipefail   # NOT -e — we control exit codes\n', 'set -uo pipefail   # NOT -e — we control exit codes\nSGVARIANT="' + variant + '"\n')

# ------------------------------------------------------------------ D. Read/Edit face
_READ_RE_BASE = ("\\.env(\\.[a-z0-9_.-]+)?$|\\.envrc$|/secrets?/|/credentials?/|id_rsa$|id_ed25519$|id_ecdsa$|\\.ssh/id_[a-z0-9_]+$|\\.pem$|\\.key$|\\.gpg$|\\.age$|\\.p12$|\\.pfx$|\\.jks$|"
                 "\\.tfstate$|\\.tfstate\\.backup$|/\\.aws/credentials$|/\\.aws/config$|/\\.kube/config$|kubeconfig$|/\\.docker/config\\.json$|service[_-]account.*\\.json$|gcp[_-]key.*\\.json$|"
                 "firebase.*\\.json$|\\.ssh/known_hosts$|/secret[_-]token|/master[_-]key|/encryption[_-]key|/\\.claude/+(\\./+)*settings\\.json$|/\\.claude/+(\\./+)*settings\\.local\\.json$|/\\.claude\\.json$")
READ_ALTS = _READ_RE_BASE.split("|")
assert len(READ_ALTS) == 32

rep('''    if echo "$lower_path" | grep -qE '\\.env(\\.[a-z0-9_.-]+)?$|''',
    '''    _sg_hit=0
    if echo "$lower_path" | grep -qE '\\.env(\\.[a-z0-9_.-]+)?$|''')
_rb = "" if vname == "read_noboundary" else "([^a-z0-9_]|$)"
rep('''|/\\.claude\\.json$'; then
      # (last three branches''', '''|/\\.claude\\.json$|[a-z0-9._-]*(forgejo|gitea)[^ ]*app\\.ini''' + _rb + '''|custom/conf/app\\.ini''' + _rb + '''\'; then
      _sg_hit=1
    fi
    if [[ $_sg_hit -eq 0 ]]; then
      if [[ "$SGVARIANT" == ext_bare ]]; then
        _sg_ext_path_pass "$file_path" > "${TMPDIR:-/tmp}/sgx.$$"
        _sgx="$(cat "${TMPDIR:-/tmp}/sgx.$$")"; rm -f "${TMPDIR:-/tmp}/sgx.$$"
      else
        _sgx="$( _sg_ext_path_pass "$file_path" 2>/dev/null )"
      fi
      [[ "$_sgx" == "BLOCK" ]] && _sg_hit=1
    fi
    if [[ $_sg_hit -eq 1 ]]; then
      # (last three branches''')
if vname in ("readface16", "readface_drop"):      # bad implementations: some of the 32 baseline alternatives of the Read / Edit path regex are lost in the rewrite
    _drop = {4, 5, 6, 7, 11, 12, 14, 15, 17, 21, 24, 25, 26, 27, 28, 29} if vname == "readface16" else {int(varg)}
    _kept = [a for i, a in enumerate(READ_ALTS, start=1) if i not in _drop]
    assert src.count(_READ_RE_BASE) == 1, src.count(_READ_RE_BASE)
    src = src.replace(_READ_RE_BASE, "|".join(_kept), 1)
if vname == "read_case_sensitive":
    _a = '    if echo "$lower_path" | grep -qE \'\\.env(\\.[a-z0-9_.-]+)?$|'
    assert src.count(_a) == 1, src.count(_a)
    src = src.replace(_a, '    if echo "$file_path" | grep -qE \'\\.env(\\.[a-z0-9_.-]+)?$|', 1)

# ------------------------------------------------------------------ E. risky_patterns edits
_w8_bnd = "" if vname == "bash_boundary_wide" else "([^[:alnum:]_]|$)"
_w8_row = ('  "(${_SG_SRVCFG})' + _w8_bnd + '"') if vname == "appini_anywhere" else ('  "(^|[^[:alnum:]_.-])(${_SG_READERS_PRINT})[[:space:]]+(([^|]*${_SG_PP_NAME})?(${_SG_SRVCFG}))' + _w8_bnd + '"')
rep('''  # R4-C-4 fix: K8s / Docker container-mounted secret paths in Bash''',
    '''  # W8 (prototype): server-side config files (Forgejo / Gitea app.ini), printing readers only, own left boundary.
''' + _w8_row + '''

  # R4-C-4 fix: K8s / Docker container-mounted secret paths in Bash''')
py_proc = "|/proc/${_SG_PIDTOK}/(task/[^/[:space:]]+/)?(environ|cmdline)"
if vname == "drop_procinterp":
    py_proc = ""
py_old = '''  "python3?[[:space:]]+-c([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG})"
  "node[[:space:]]+-e([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG})"'''
rows = []
if "python3" in interps:
    rows.append('  "python3?[[:space:]]+-c([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG}|${_SG_SRVCFG}' + py_proc + ')"')
else:
    rows.append('  "python3?[[:space:]]+-c([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG})"')
if "node" in interps:
    rows.append('  "node[[:space:]]+-e([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG}|${_SG_SRVCFG}' + py_proc + ')"')
else:
    rows.append('  "node[[:space:]]+-e([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG})"')
if vname == "drop_interp_name":
    _lit = {"v1var": "/v1/var/|", "secretsmanager": "secretsmanager|", "secrets": "/secrets/|", "env": "\\.env|", "provider_key": "provider_key|", "claudecfg": "|${_SG_CLAUDE_CFG}"}[varg]
    rows = [r.replace(_lit, "", 1) for r in rows]
    assert all(_lit not in r for r in rows)
rep(py_old, "\n".join(rows))

if vname == "env_boundary":
    rep('''  "python3?[[:space:]]+-c([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key''',
        '''  "python3?[[:space:]]+-c([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env(rc)?([^A-Za-z0-9_]|$)|provider_key''')
    rep('''  "node[[:space:]]+-e([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key''',
        '''  "node[[:space:]]+-e([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env(rc)?([^A-Za-z0-9_]|$)|provider_key''')
    rep("""  'lua[[:space:]]+-e[^|]*(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key)'""",
        """  'lua[[:space:]]+-e[^|]*(/v1/var/|secretsmanager|/secrets/|\\.env(rc)?([^A-Za-z0-9_]|$)|provider_key)'""")

st = "(environ|status|cmdline)" if vname == "proc_status" else "(environ|cmdline)"
OLD_RE = "|".join(proc_old)
ALL_RE = "|".join(proc_old + proc_new)
rep('''  '(cat|head|tail|less|more|strings|hexdump|od|xxd|tr|awk|perl|rev)[[:space:]]+[^|]*/proc/(self|[0-9]+)/(environ|status|cmdline)'
  '<[[:space:]]*/proc/(self|[0-9]+)/(environ|status|cmdline)\'''',
    '''  "((''' + OLD_RE + ''')[[:space:]]+[^|]*/proc/(self|[0-9]+)/(environ|status|cmdline)|(''' + ALL_RE + ''')[[:space:]]+[^|]*/proc/${_SG_PIDTOK}/(task/[^/[:space:]]+/)?''' + st + ''')"
  "(<[[:space:]]*/proc/(self|[0-9]+)/(environ|status|cmdline)|<[[:space:]]*/proc/${_SG_PIDTOK}/(task/[^/[:space:]]+/)?''' + st + ''')"
  # W11 (prototype): process-table enumeration rows (credit is TIGHT, see _sg_compute_credit)
  "${_SG_PROCTAB}"
  "${_SG_PS_REMOTE}"
  "${_SG_PS_DOCKER}"''')

# ------------------------------------------------------------------ F. _sg_judge_one: blocked text as a function + W12 normalisation
old_heredoc_start = '''      if [[ "$credit" == "0" ]]; then
        cat >&2 <<EOF
[secret-guard] BLOCKED: command reads a secret-bearing source without a'''
i0 = src.index(old_heredoc_start)
i1 = src.index("        return 2\n", i0) + len("        return 2\n")
block = src[i0:i1]
h0 = block.index("        cat >&2 <<EOF\n") + len("        cat >&2 <<EOF\n")
h1 = block.index("\nEOF\n", h0) + 1
heredoc_body = block[h0:h1]
new_block = '''      if [[ "$credit" == "0" ]]; then
        _sg_emit_blocked "$pat" "$seg" "$mode"
        return 2
'''
src = src[:i0] + new_block + src[i1:]
emit_fn = '''# _sg_emit_blocked PAT SEG MODE : the (unchanged) BLOCKED text, shared by every block path.
_sg_emit_blocked() {
  local pat="$1" seg="$2" mode="$3"
  cat >&2 <<EOF
''' + heredoc_body + '''EOF
  if [[ "$mode" == "segment" ]]; then
    echo "Triggering segment: $(_sg_redact_echo "$seg")" >&2
  fi
}

'''
rep("_sg_judge_one() {\n", emit_fn + "_sg_judge_one() {\n")
# W12 normalisation: the four single-key read substrings are cut out by PREFIX / SUFFIX concatenation (no ${s//p/r})
w12 = [(".environ.get(", ".ek_("), (".environb.get(", ".ek_("), (".environ[", ".ek_["), (".environb[", ".ek_[")]
if vname == "drop_w12":
    w12 = [x for i, x in enumerate(w12) if i != int(varg)]
if vname == "w12_once":        # bad implementation: `if` instead of `while`: only the first occurrence of each single-key substring is replaced
    w12_code = "\n".join(
        '    if [[ "$subj" == *"%s"* ]]; then _w="${subj%%%%"%s"*}"; subj="${_w}%s${subj:$(( ${#_w} + %d ))}"; fi' % (a, a, b, len(a)) for a, b in w12)
elif vname == "w12_echo_norm":
    w12_code = "    :"
elif vname == "w12_quadratic":
    w12_code = "\n".join(
        '    while [[ "$subj" == *"%s"* ]]; do subj="${subj%%%%"%s"*}%s${subj#*"%s"}"; done' % (a, a, b, a) for a, b in w12)
else:   # v3: the remainder is taken by length (linear), see after()
    w12_code = "\n".join(
        '    while [[ "$subj" == *"%s"* ]]; do _w="${subj%%%%"%s"*}"; subj="${_w}%s${subj:$(( ${#_w} + %d ))}"; done' % (a, a, b, len(a)) for a, b in w12)
rep('''  local seg="$1" mode="$2" pat
  local credit=""
  for pat in "${risky_patterns[@]}"; do
    if [[ "$seg" =~ $pat ]]; then''', '''  local seg="$1" mode="$2" pat
  local credit="" subj="$1" _w
  if [[ "$SGVARIANT" != env_boundary && "$subj" == *environ* ]]; then
''' + w12_code + '''
  fi
  for pat in "${risky_patterns[@]}"; do
    if [[ "$subj" =~ $pat ]]; then''')

# ------------------------------------------------------------------ G. _sg_per_segment_eval: the baseline body becomes _sg_core_eval; ordering + W10 + W9 passes
_ORCH_OLD = """_sg_per_segment_eval() {
  local cmd="$1" seg rc
  if ! _sg_safe_to_split "$cmd"; then
    _sg_judge_one "$cmd" whole
    return $?
  fi
  _sg_split_top "$cmd"
  [[ ${#_SG_SEGS[@]} -eq 0 ]] && return 0
  for seg in "${_SG_SEGS[@]}"; do
    _sg_judge_one "$seg" segment
    rc=$?
    [[ $rc -ne 0 ]] && return "$rc"
  done
  return 0
}"""
_CORE = r"""# _sg_core_eval CMD : THE built-in judgement -- the baseline body of _sg_per_segment_eval, unchanged (safe-to-split check, top-level split, one _sg_judge_one per segment);
# it only records how it judged (_SG_MODE) so that the W10 pass knows whether _SG_SEGS holds segments.  The W9 extension calls this same function.
_SG_MODE=segment
_sg_core_eval() {
  local cmd="$1" seg rc
  if ! _sg_safe_to_split "$cmd"; then
    _SG_MODE=whole
    _sg_judge_one "$cmd" whole
    return $?
  fi
  _SG_MODE=segment
  _sg_split_top "$cmd"
  if [[ ${#_SG_SEGS[@]} -eq 0 ]]; then _SG_MODE=none; return 0; fi
  for seg in "${_SG_SEGS[@]}"; do
    _sg_judge_one "$seg" segment
    rc=$?
    [[ $rc -ne 0 ]] && return "$rc"
  done
  return 0
}
"""
_FIRST = ""
if vname == "ext_first":          # bad implementation: the extension is judged BEFORE the built-ins (the built-in verdict can be pushed past the 5 s timeout)
    _FIRST = """  _x="$( _sg_ext_pass "$cmd" 2>/dev/null )"
  if [[ "$_x" == BLOCK* ]]; then _sg_emit_blocked "(extension) .aria/secret-guard.paths" "$cmd" segment; return 2; fi
"""
if vname == "vx_interleave":      # bad implementation: the substituted copy of segment i is judged right after the built-in verdict of segment i
    _BUILTIN = """  if ! _sg_safe_to_split "$cmd"; then
    _sg_judge_one "$cmd" whole
    rc=$?
    [[ $rc -ne 0 ]] && return "$rc"
    _sg_vx_pass "$cmd" whole
    rc=$?
    [[ $rc -ne 0 ]] && return "$rc"
  else
    _sg_split_top "$cmd"
    if [[ ${#_SG_SEGS[@]} -gt 0 ]]; then
      _sg_vx_collect "$cmd"
      for seg in "${_SG_SEGS[@]}"; do
        _sg_judge_one "$seg" segment
        rc=$?
        [[ $rc -ne 0 ]] && return "$rc"
        _sg_vx_pass "$seg" one
        rc=$?
        [[ $rc -ne 0 ]] && return "$rc"
      done
    fi
  fi
"""
else:
    _BUILTIN = """  _sg_core_eval "$cmd"
  rc=$?
  [[ $rc -ne 0 ]] && return "$rc"
  if [[ "$_SG_MODE" != none ]]; then
    _sg_vx_pass "$cmd" "$_SG_MODE"
    rc=$?
    [[ $rc -ne 0 ]] && return "$rc"
  fi
"""
if vname == "ext_bare":           # bad implementation: the extension function is called directly (not inside a command substitution)
    _EXT = """  _sg_ext_pass "$cmd" > "${TMPDIR:-/tmp}/sgy.$$"
  _x="$(cat "${TMPDIR:-/tmp}/sgy.$$")"; rm -f "${TMPDIR:-/tmp}/sgy.$$"
"""
elif vname == "ext_first":
    _EXT = '  _x=""\n'
else:
    _EXT = """  _x="$( _sg_ext_pass "$cmd" 2>/dev/null )"
"""
_VXEXT = "" if vname == "ext_first" else """  if [[ "$_x" != BLOCK* ]] && (( ${#_SGV_N[@]} )) && _sg_vx_apply "$cmd"; then
    _x="$( _sg_ext_pass "$_SG_SUB" 2>/dev/null )"
  fi
"""
_ORCH_NEW = _CORE + """_sg_per_segment_eval() {
  local cmd="$1" seg rc _x
""" + _FIRST + _BUILTIN + _EXT + _VXEXT + """  if [[ "$_x" == BLOCK* ]]; then
    _sg_emit_blocked "(extension) .aria/secret-guard.paths" "$cmd" segment
    return 2
  fi
  return 0
}
_sg_dbg_vx_marker() { :; }"""
rep(_ORCH_OLD, _ORCH_NEW)

if vname == "vx_eval":
    # bad implementation (a natural one: "let the shell resolve the chained references"): every assignment is eval'd, so a command substitution /
    # back-quote / arithmetic expansion inside an assigned value RUNS inside the hook
    _o = """  for (( i = 0; i < ${#_SGV_N[@]}; i++ )); do
    for (( j = 0; j < ${#_SGV_N[@]}; j++ )); do
      (( i == j )) && continue
      _sg_vx_replace "${_SGV_V[i]}" "\\${${_SGV_N[j]}}" "${_SGV_V[j]}"; _SGV_V[i]="$_SG_RP"
      _sg_vx_replace "${_SGV_V[i]}" "\\$${_SGV_N[j]}" "${_SGV_V[j]}"; _SGV_V[i]="$_SG_RP"
    done
  done
"""
    assert src.count(_o) == 1, src.count(_o)
    src = src.replace(_o, """  for (( i = 0; i < ${#_SGV_N[@]}; i++ )); do
    eval "${_SGV_N[i]}=\\"${_SGV_V[i]}\\"" 2>/dev/null
  done
  for (( i = 0; i < ${#_SGV_N[@]}; i++ )); do
    _SGV_V[i]="${!_SGV_N[i]}"
  done
""", 1)
if vname == "w12_eval":
    # bad implementation: the single-key normalisation additionally evaluates the command text itself (the side effect is all that matters here)
    _o = '''  for pat in "${risky_patterns[@]}"; do
    if [[ "$subj" =~ $pat ]]; then'''
    assert src.count(_o) == 1, src.count(_o)
    src = src.replace(_o, '''  [[ "$seg" == *environ* ]] && : "$(eval "$seg" >/dev/null 2>&1)"
''' + _o, 1)
if vname == "w12_echo_norm":
    # bad implementation: the single-key normalisation rewrites the command ONCE at the top of the hook, so everything downstream -- including the `Command was:` line of the
    # BLOCKED text -- shows the rewritten copy instead of the original text
    _o = '( _sg_per_segment_eval "$command" )'
    assert src.count(_o) == 1, src.count(_o)
    _glob = "\n".join('  while [[ "$command" == *"%s"* ]]; do _w="${command%%%%"%s"*}"; command="${_w}%s${command:$(( ${#_w} + %d ))}"; done' % (a, a, b, len(a)) for a, b in w12)
    src = src.replace(_o, 'if [[ "$command" == *environ* ]]; then\n  _w=""\n' + _glob + '\nfi\n' + _o, 1)
if vname == "vx_patsub":
    _o = '  _SG_RP="${out}${s}"\n}'
    assert src.count(_o) == 1
    src = src.replace(_o, '  _SG_RP="${1//"$pat"/"$rep"}"\n}', 1)
if vname == "b4":
    _o = "# Unit-test sourcing gate (#128): when sourced"
    assert src.count(_o) == 1
    src = src.replace(_o, '_sg_wpa_b4() { [[ -v HOME ]] && return 0; return 1; }\n' + _o, 1)
if vname == "vx_interleave":
    # bad implementation: the substituted copy of segment i is judged right after the built-in verdict of segment i (the entry point
    # `_sg_vx_pass` is called once per segment, in mode `one`: assignments were collected once before the loop)
    _o = '''  local cmd="$1" mode="$2" seg rc
  _sg_vx_collect "$cmd"
'''
    assert src.count(_o) == 1
    src = src.replace(_o, '''  local cmd="$1" mode="$2" seg rc
  if [[ "$mode" == one ]]; then
    (( ${#_SGV_N[@]} )) || return 0
    if _sg_vx_apply "$cmd"; then _sg_judge_one "$_SG_SUB" segment; return $?; fi
    return 0
  fi
  _sg_vx_collect "$cmd"
''', 1)
if vname == "vx_collect_per_seg":
    # timing bad implementation: the assignment collection is redone for every segment (instead of once per command)
    _o = '''  for seg in "${_SG_SEGS[@]}"; do
    if _sg_vx_apply "$seg"; then'''
    assert src.count(_o) == 1
    src = src.replace(_o, '''  for seg in "${_SG_SEGS[@]}"; do
    _sg_vx_collect "$cmd"
    if _sg_vx_apply "$seg"; then''', 1)

# ------------------------------------------------------------------ Z. inline the three process-table rows (SC-31 31c: no row made only of a "${VAR}")
def _expand(name):
    out = subprocess.run(["bash", "-c", vars_block_rows + '\nprintf %s "${' + name + '}"'], capture_output=True, text=True)
    assert out.returncode == 0 and out.stdout, name
    return out.stdout


def _shq(s):
    return "'" + s.replace("'", "'\"'\"'") + "'"


for _n in ("_SG_PROCTAB", "_SG_PS_REMOTE", "_SG_PS_DOCKER"):
    _row = '  "${' + _n + '}"\n'
    assert src.count(_row) == 1, _n
    src = src.replace(_row, "  " + _shq(_expand(_n)) + "\n")

open(out_path, "w", encoding="utf-8").write(src)
print("wrote", out_path, "variant", variant)
