#!/usr/bin/env python3
"""Build the v3-design PROTOTYPE of hooks/secret-guard.sh from the baseline copy.

usage: python3 patch_l1.py <baseline secret-guard.sh> <out secret-guard.sh> [--variant NAME[:ARG]]

The prototype is not the implementation: it is generated from the baseline by text substitution and only shows that the
design written into proposal v3 is reachable, and which bad implementations the probe rows catch.

variants (every non-v3 variant is a 'bad implementation' that the probe rows must catch):
  v3                 the design written into proposal v3
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
variant = "v3"
if "--variant" in sys.argv:
    variant = sys.argv[sys.argv.index("--variant") + 1]
vname, _, varg = variant.partition(":")
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
PID_ALTS = ["self", "[0-9]+", "\\*", "\\$\\{[^}]*\\}", "\\$[A-Za-z_][A-Za-z0-9_]*", "\\$\\([^)]*\\)"]
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
if vname == "pidtok_any":
    pid_alts = ["[^/[:space:]$]+", "\\$\\{[^}]*\\}", "\\$[A-Za-z_][A-Za-z0-9_]*", "\\$\\([^)]*\\)"]
if vname == "drop_kwpos":
    kwpos = drop(kwpos, varg, "kwpos")
if vname == "drop_interp":
    assert varg in interps, varg
    interps.pop(varg)

SQ = "'\"'\"'"            # a single quote inside a single-quoted bash string
BIN = "" if vname == "drop_bin" else "(/[^[:space:]|;&\"" + SQ + "`$()<>]*/)?"
LAUNCH_RE = "(" + "|".join(launch) + ")"
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
PS_ARGS = "(" + "|".join(ps_alts) + ")"
KWPOS_RE = "" if not kwpos else "((" + "|".join(kwpos) + ")[[:space:]]+)?"
PS_CMD = ("(" + BIN + "(ps[[:blank:]]+" + PS_ARGS + "|pgrep[[:blank:]]+([^|;&]*[[:blank:]])?(" + "|".join(PGREP_ALTS) + ")"
          "|pstree[[:blank:]]+([^|;&]*[[:blank:]])?(" + "|".join(PSTREE_ALTS) + ")|top[[:blank:]]+([^|;&]*[[:blank:]])?-[a-zA-Z]*c))")
_ANCHOR = "(^|[;&|(){]|`)" if vname == "anchor_nocntrl" else "(^|[;&|(){]|`|[[:cntrl:]])"
PROCTAB = (_ANCHOR + "[[:blank:]]*" + KWPOS_RE + "(" + BIN + LAUNCH_RE + "([[:space:]]+" + LARG + ")*[[:space:]]+)?" + PS_CMD)
if vname == "launcher_any":
    # bad implementation (over-broad): ANY command behind a launcher is a process-table command
    PROCTAB = (_ANCHOR + "[[:blank:]]*" + KWPOS_RE + "(" + BIN + LAUNCH_RE + "([[:space:]]+" + LARG + ")*[[:space:]]+)" + "[a-z]+")
REMOTE_RE = ("(" + "|".join(remote.values()) + ")[^|]*[[:space:]" + SQ + "\"(`](" + PS_CMD + "|printenv([[:space:]" + SQ + "\"]|[;&|)}<>`]|$)"
             "|env([[:blank:]]*($|[;&|)}<>" + SQ + "\"`])))")
_dk_tool = "docker" if vname == "nodocker_podman" else "(docker|podman)"
_dk_compose = "" if (vname == "drop_dockerform" and varg == "compose") else "(compose[[:space:]]+)?"
_dk_container = "" if (vname == "drop_dockerform" and varg == "container") else "(container[[:space:]]+)?"
_dk_psls = "ps" if (vname == "drop_dockerform" and varg == "ls") else "(ps|ls)"
_dk_top = "" if (vname == "drop_dockerform" and varg == "top") else _dk_tool + "[[:space:]]+" + _dk_compose + "top([^[:alnum:]_-]|$)"
_dk_nt = "" if (vname == "drop_dockerform" and varg == "notrunc") else _dk_tool + "[[:space:]]+" + _dk_container + _dk_psls + "[[:space:]]+([^|;&]*[[:space:]])?--no-trunc"
DOCKER_RE = "|".join(x for x in (_dk_top, _dk_nt) if x)
PIDTOK = "(" + "|".join(pid_alts) + ")"
READERS_RE = "|".join(readers)
EXT_READER_RE = ("(^|[^[:alnum:]_.-])((" + "|".join(extreaders) + ")[[:space:]]|(" + "|".join(v for v in interps.values()) + ")([[:space:]]|$))")
INTERP_NAME_ALT = lambda extra: "(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG}|${_SG_SRVCFG}" + extra + ")"

vars_block = r'''
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
_SG_PS_DOCKER='@DOCKER@'
_SG_PROCTAB_ALL="(${_SG_PROCTAB}|${_SG_PS_REMOTE}|${_SG_PS_DOCKER})"
_SG_PIDTOK='@PIDTOK@'
'''
for k, v in (("@READERS@", READERS_RE), ("@BIN@", BIN), ("@PS_ARGS@", PS_ARGS), ("@PS_CMD@", PS_CMD), ("@PROCTAB@", PROCTAB),
             ("@REMOTE@", REMOTE_RE), ("@DOCKER@", DOCKER_RE), ("@PIDTOK@", PIDTOK)):
    vars_block = vars_block.replace(k, v)
rep('_SG_PP_SUFFIX="(^|[[:space:]\\"\'=/*A-Za-z0-9_.-])"\n', '_SG_PP_SUFFIX="(^|[[:space:]\\"\'=/*A-Za-z0-9_.-])"\n' + vars_block)

# ------------------------------------------------------------------ B. credit: tight set + anchored jq forms (W8 / W11 / W9 / W12)
rep('''  local tight=0
  if [[ "$seg" =~ ($_SG_CLAUDE_CFG) ]]; then
    tight=1
  fi
''', '''  local tight=0
  if [[ "$seg" =~ ($_SG_CLAUDE_CFG|$_SG_SRVCFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]] || [[ "${2:-}" == tight ]]; then
    tight=1
  fi
''')
if vname == "notight":
    src = src.replace('[[ "$seg" =~ ($_SG_CLAUDE_CFG|$_SG_SRVCFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]', '[[ "$seg" =~ ($_SG_CLAUDE_CFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]', 1)
if vname == "claude_notight":
    src = src.replace('[[ "$seg" =~ ($_SG_CLAUDE_CFG|$_SG_SRVCFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]', '[[ "$seg" =~ ($_SG_SRVCFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]', 1)
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
sym_req = "" if vname == "ext_nosym" else " && /[a-z0-9]/"

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
_SG_EXT_READER_RE='@EXTREADER@'
_sg_ext_root() {   # prints the project root (CLAUDE_PROJECT_DIR, else stdin cwd) or nothing
  local r="${CLAUDE_PROJECT_DIR:-}"
  if [[ -z "$r" && "$input" == *'"cwd"'* ]]; then
    r="$(printf '%s' "$input" | jq -r '.cwd // ""' 2>/dev/null | tr -d '\r')"
  fi
  printf '%s' "$r"
}
_sg_ext_entries() {   # prints the valid entries (lower-cased, one per line); prints nothing when the extension is not in effect
  local root f size
  root="$(_sg_ext_root)"
  [[ -n "$root" ]] || return 0
  f="$root/.aria/secret-guard.paths"
  [[ -f "$f" && -r "$f" ]] || return 0
  size="$(wc -c < "$f" | tr -d ' ')"
  (( size <= @MAXSIZE@ )) || return 0
  tr -d '\000' < "$f" | cmp -s - "$f" || return 0
  local out
  out="$(tr -d '\r' < "$f" | tr '[:upper:]' '[:lower:]' | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' | awk '!/^#/ && length($0) >= @MINLEN@ && length($0) <= @MAXLEN@@SYMREQ@')"
  [[ -n "$out" ]] || return 0
  local n
  n="$(printf '%s\n' "$out" | wc -l | tr -d ' ')"
  if (( n > @MAXENTRIES@ )); then
    if [[ "$SGVARIANT" == ext_trunc ]]; then printf '%s\n' "$out" | head -n @MAXENTRIES@; fi
    return 0
  fi
  printf '%s\n' "$out"
}
# _sg_ext_pass TEXT : whole-command check, ONE fixed-string multi-pattern pass (grep -F -f). prints BLOCK + stage text on a hit.
_sg_ext_pass() {
  local text="$1" hits line off match before stage tail segtxt n=0
  local LC_ALL=C
  hits="$(grep -oFib -f <(_sg_ext_entries) <(printf '%s' "$text") 2>/dev/null)"
  [[ -n "$hits" ]] || return 0
  local lc
  lc="$(printf '%s' "$text" | tr '[:upper:]' '[:lower:]')"
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
        printf 'BLOCK\n%s' "$segtxt"
        return 0
      fi
    fi
  done <<< "$hits"
  return 0
}
_sg_ext_path_pass() {   # Read/Edit face: entry (lower-cased) as a literal substring of the path (grep -F -i, one pass)
  local p="$1"
  if grep -qFi -f <(_sg_ext_entries) <(printf '%s' "$p") 2>/dev/null; then printf 'BLOCK'; fi
  return 0
}
'''
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
for k, v in (("@AFTER_REPLACE@", after("s", "pre", "pat")), ("@AFTER_COLLECT@", after("rest", "pre", "m")), ("@AFTER_APPLY@", after("s", "pre", "m")),
             ("@MAXREPL@", str(max_repl)), ("@MAXASSIGN@", str(max_assign)), ("@MAXOCC@", str(max_occ)), ("@MAXSIZE@", str(max_size)),
             ("@MINLEN@", str(min_len)), ("@MAXLEN@", str(max_len)), ("@SYMREQ@", sym_req), ("@MAXENTRIES@", str(max_entries)),
             ("@EXTREADER@", EXT_READER_RE), ("@ASSIGNKW@", assign_kw), ("@QUOTEDVAL@", quoted)):
    funcs = funcs.replace(k, v)
rep('# Unit-test sourcing gate (#128): when sourced (not executed), stop here —', funcs + '\n# Unit-test sourcing gate (#128): when sourced (not executed), stop here —')
rep('set -uo pipefail   # NOT -e — we control exit codes\n', 'set -uo pipefail   # NOT -e — we control exit codes\nSGVARIANT="' + variant + '"\n')

# ------------------------------------------------------------------ D. Read/Edit face
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
if vname == "w12_quadratic":
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

# ------------------------------------------------------------------ G. _sg_per_segment_eval: ordering + extension pass
rep('''_sg_per_segment_eval() {
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
}''', '''_sg_per_segment_eval() {
  local cmd="$1" seg rc _x
  if [[ "$SGVARIANT" == ext_first ]]; then
    _x="$( _sg_ext_pass "$cmd" 2>/dev/null )"
    if [[ "$_x" == BLOCK* ]]; then _sg_emit_blocked "(extension) .aria/secret-guard.paths" "${_x#BLOCK$'\\n'}" segment; return 2; fi
  fi
  if ! _sg_safe_to_split "$cmd"; then
    _sg_judge_one "$cmd" whole
    rc=$?
    [[ $rc -ne 0 ]] && return "$rc"
    _sg_vx_pass "$cmd" whole
    rc=$?
    [[ $rc -ne 0 ]] && return "$rc"
  else
    _sg_split_top "$cmd"
    if [[ ${#_SG_SEGS[@]} -gt 0 ]]; then
      if [[ "$SGVARIANT" == vx_interleave ]]; then
        _sg_vx_collect "$cmd"
        for seg in "${_SG_SEGS[@]}"; do
          _sg_judge_one "$seg" segment
          rc=$?
          [[ $rc -ne 0 ]] && return "$rc"
          _sg_vx_pass "$seg" one
          rc=$?
          [[ $rc -ne 0 ]] && return "$rc"
        done
      else
        for seg in "${_SG_SEGS[@]}"; do
          _sg_judge_one "$seg" segment
          rc=$?
          [[ $rc -ne 0 ]] && return "$rc"
        done
        _sg_vx_pass "$cmd" segment
        rc=$?
        [[ $rc -ne 0 ]] && return "$rc"
      fi
    fi
  fi
  if [[ "$SGVARIANT" == ext_bare ]]; then
    _sg_ext_pass "$cmd" > "${TMPDIR:-/tmp}/sgy.$$"
    _x="$(cat "${TMPDIR:-/tmp}/sgy.$$")"; rm -f "${TMPDIR:-/tmp}/sgy.$$"
  elif [[ "$SGVARIANT" != ext_first ]]; then
    _x="$( _sg_ext_pass "$cmd" 2>/dev/null )"
  else
    _x=""
  fi
  if [[ "$_x" != BLOCK* && "$SGVARIANT" != ext_first ]] && (( ${#_SGV_N[@]} )) && _sg_vx_apply "$cmd"; then
    _x="$( _sg_ext_pass "$_SG_SUB" 2>/dev/null )"
  fi
  if [[ "$_x" == BLOCK* ]]; then
    _sg_emit_blocked "(extension) .aria/secret-guard.paths" "${_x#BLOCK$'\\n'}" segment
    return 2
  fi
  return 0
}
_sg_dbg_vx_marker() { :; }''')

if vname == "vx_patsub":
    _o = '  _SG_RP="${out}${s}"\n}'
    assert src.count(_o) == 1
    src = src.replace(_o, '  _SG_RP="${1//"$pat"/"$rep"}"\n}', 1)
if vname == "b4":
    _o = "# Unit-test sourcing gate (#128): when sourced"
    assert src.count(_o) == 1
    src = src.replace(_o, '_sg_wpa_b4() { [[ -v HOME ]] && return 0; return 1; }\n' + _o, 1)
if vname == "ext_regex":
    for _a, _b in (("grep -oFib -f", "grep -oEib -f"), ("grep -qFi -f", "grep -qEi -f")):
        assert src.count(_a) == 1, _a
        src = src.replace(_a, _b, 1)
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
if vname == "ext_perentry":
    # timing bad implementation, the per-entry process class: one grep process per extension entry (Bash and Read faces)
    _o = '''  hits="$(grep -oFib -f <(_sg_ext_entries) <(printf '%s' "$text") 2>/dev/null)"'''
    assert src.count(_o) == 1
    src = src.replace(_o, '''  hits=""; local _e _h
  while IFS= read -r _e; do _h="$(printf '%s' "$text" | grep -oFib -e "$_e" 2>/dev/null)"; [[ -n "$_h" ]] && hits="${hits}${_h}"$'\\n'; done < <(_sg_ext_entries)''', 1)
    _o = '''  if grep -qFi -f <(_sg_ext_entries) <(printf '%s' "$p") 2>/dev/null; then printf 'BLOCK'; fi'''
    assert src.count(_o) == 1
    src = src.replace(_o, '''  local _e
  while IFS= read -r _e; do
    if printf '%s' "$p" | grep -qFi -e "$_e" 2>/dev/null; then printf 'BLOCK'; return 0; fi
  done < <(_sg_ext_entries)''', 1)
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
    out = subprocess.run(["bash", "-c", vars_block + '\nprintf %s "${' + name + '}"'], capture_output=True, text=True)
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
