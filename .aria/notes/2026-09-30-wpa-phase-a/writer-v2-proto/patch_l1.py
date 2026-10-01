#!/usr/bin/env python3
"""Build the v2-design prototype of hooks/secret-guard.sh from the baseline copy.

usage: python3 patch_l1.py <baseline secret-guard.sh> <out secret-guard.sh> [--variant NAME]

variants (mutation runs; every non-v2 variant is a 'bad implementation' that the probe rows must catch):
  v2           the design written into proposal v2
  ext_bare     extension code called as a plain function in the main shell (no command-substitution isolation)
  ext_first    extension pass evaluated before the built-in verdict
  vx_interleave  variable-expansion second pass interleaved per segment (original, substituted, next segment ...)
  env_boundary W12 as in v1: right boundary on the three interpreter rows (no normalisation)
  proc_status  /proc widening also widens status
  ext_regex    extension entries compiled into a regular expression instead of matched as fixed strings
  ext_trunc    more than 200 entries: only the first 200 are used (instead of ignoring the whole file)
Rule #7: this file holds no credential-shaped literal.
"""
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
variant = "v2"
if "--variant" in sys.argv:
    variant = sys.argv[sys.argv.index("--variant") + 1]
src = open(src_path, encoding="utf-8").read()


def rep(old, new, count=1):
    global src
    n = src.count(old)
    assert n == count, f"anchor count {n} != {count} for: {old[:80]!r}"
    src = src.replace(old, new)


# ------------------------------------------------------------------ A. shared variables (above _sg_compute_credit)
vars_block = r'''
# ── secret-net-l3-and-bypass-paths prototype: shared names (single definition, several consumers) ──
# W8: server-side config (Forgejo / Gitea app.ini).
_SG_SRVCFG='[A-Za-z0-9._-]*(forgejo|gitea)[^[:space:]|;&"'"'"']*app\.ini|custom/conf/app\.ini'
_SG_READERS_PRINT='cat|grep|egrep|fgrep|rg|head|tail|less|more|strings|awk|sed|jq|nl|tac|rev|sort|uniq|cut|paste|diff|cmp|comm|xxd|od|hexdump|base64|column|fold'
# W11: process-table enumeration (argv / environ exposing forms). comm-only forms stay allowed.
_SG_PS_ARGS='([a-zA-Z]+([^[:alnum:]_-]|$)|[0-9]+([^[:alnum:]_.-]|$)|([^|;&]*[[:blank:]])?-[a-zA-Z]*[fF]|([^|;&]*[[:blank:]])?(-[a-zA-Z]*[oO]|--format)[[:blank:]=]*[^[:blank:]|;&]*(args|cmd|command))'
_SG_PS_CMD='(ps[[:blank:]]+'"${_SG_PS_ARGS}"'|pgrep[[:blank:]]+([^|;&]*[[:blank:]])?(-[a-zA-Z]*a|--list-full)|pstree[[:blank:]]+([^|;&]*[[:blank:]])?(-[a-zA-Z]*a|--arguments)|top[[:blank:]]+([^|;&]*[[:blank:]])?-[a-zA-Z]*c)'
_SG_PROCTAB='(^|[;&|(){]|`|[[:cntrl:]])[[:blank:]]*((sudo|doas|nice|timeout|nohup|stdbuf|env|time|setsid|ionice|watch|command|exec)([[:space:]]+-[^[:space:]]*|[[:space:]]+[0-9]+)*[[:space:]]+)?'"${_SG_PS_CMD}"
_SG_PS_REMOTE='(ssh|docker[[:space:]]+(compose[[:space:]]+)?exec|kubectl[[:space:]]+exec|nomad[[:space:]]+alloc[[:space:]]+exec|pct[[:space:]]+exec|lxc[[:space:]]+exec|podman[[:space:]]+exec|(sh|bash|zsh|dash)[[:space:]]+-c|watch)[^|]*[[:space:]'"'"'"(`]('"${_SG_PS_CMD}"'|printenv([[:space:]'"'"'"]|[;&|)}<>`]|$)|env([[:blank:]]*($|[;&|)}<>'"'"'"`])))'
_SG_PS_DOCKER='docker[[:space:]]+(compose[[:space:]]+)?top([^[:alnum:]_-]|$)|docker[[:space:]]+(container[[:space:]]+)?(ps|ls)[[:space:]]+([^|;&]*[[:space:]])?--no-trunc'
_SG_PROCTAB_ALL="(${_SG_PROCTAB}|${_SG_PS_REMOTE}|${_SG_PS_DOCKER})"
_SG_PIDTOK='([^/[:space:]$]+|\$\{[^}]*\}|\$[A-Za-z_][A-Za-z0-9_]*|\$\([^)]*\))'
'''
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

if variant == "notight":
    # bad implementation: the app.ini name group is NOT merged into the tight set (anchored grep / sed / awk count as filters)
    src = src.replace('[[ "$seg" =~ ($_SG_CLAUDE_CFG|$_SG_SRVCFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]', '[[ "$seg" =~ ($_SG_CLAUDE_CFG) ]] || [[ "$seg" =~ $_SG_PROCTAB_ALL ]]', 1)
if variant == "jq_loose":
    # bad implementation: the new metadata-only word goes into the loose credit vocabulary (any text may follow the word)
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
funcs = r'''
# ── W10 (prototype): literal-assignment expansion. Second pass runs only after EVERY built-in verdict allowed. ──
_SGV_N=(); _SGV_V=()
_SG_SUB=""
# portable literal replace-all (prefix / suffix concatenation; NO ${x//p/r}: bash 5.2 patsub_replacement and the quote
# semantics of bash < 4.3 disagree about quotes and '&' inside the replacement). at most 8 replacements.
_SG_RP=""
_sg_vx_replace() {
  local s="$1" pat="$2" rep="$3" out="" g=0
  while (( g < 8 )) && [[ "$s" == *"$pat"* ]]; do
    g=$((g+1)); out="${out}${s%%"$pat"*}${rep}"; s="${s#*"$pat"}"
  done
  _SG_RP="${out}${s}"
}
_sg_vx_collect() {
  local rest="$1" m name val i j n=0 dup
  local _q="'" _d='"' _b='`'
  _SGV_N=(); _SGV_V=()
  [[ "$rest" == *'$'* && "$rest" == *=* ]] || [[ "$rest" == *'$'* && "$rest" == *' in '* ]] || return 0
  local re="(^|[;&|[:space:](${_d}${_b}${_q}])((export|declare|local|readonly|typeset)[[:space:]]+(-[a-zA-Z]+[[:space:]]+)*)?([A-Za-z_][A-Za-z0-9_]*)=(${_d}([^${_d}]*)${_d}|${_q}([^${_q}]*)${_q}|\\\$\\([^)]*\\)|${_b}[^${_b}]*${_b}|[^[:space:];&|)${_d}${_b}${_q}]*)"
  while (( n < 16 )) && [[ "$rest" =~ $re ]]; do
    (( n += 1 ))
    m="${BASH_REMATCH[0]}"; name="${BASH_REMATCH[5]}"; val="${BASH_REMATCH[6]}"
    rest="${rest#*"$m"}"
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
    rest="${rest#*"$m"}"
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
    while (( guard < 8 )) && [[ "$s" =~ \$${n}([^A-Za-z0-9_]|$) ]]; do
      (( guard += 1 ))
      m="${BASH_REMATCH[0]}"; tail="${BASH_REMATCH[1]}"
      if [[ -z "$tail" ]]; then pre="${s%"$m"}"; post=""; else pre="${s%%"$m"*}"; post="${s#*"$m"}"; fi
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
_SG_EXT_READER_RE='(^|[^[:alnum:]_.-])((cat|grep|egrep|fgrep|rg|head|tail|less|more|strings|awk|sed|jq|nl|tac|rev|sort|uniq|cut|paste|diff|cmp|comm|xxd|od|hexdump|base64|column|fold)[[:space:]]|(python3?[[:space:]]+-c|node[[:space:]]+-e)([[:space:]]|$))'
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
  (( size <= 32768 )) || return 0
  tr -d '\000' < "$f" | cmp -s - "$f" || return 0
  local out
  out="$(tr -d '\r' < "$f" | tr '[:upper:]' '[:lower:]' | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' | awk '!/^#/ && length($0) >= 4 && length($0) <= 200 && /[a-z0-9]/')"
  [[ -n "$out" ]] || return 0
  local n
  n="$(printf '%s\n' "$out" | wc -l | tr -d ' ')"
  if (( n > 200 )); then
    if [[ "$SGVARIANT" == ext_trunc ]]; then printf '%s\n' "$out" | head -n 200; fi
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
    n=$((n+1)); (( n > 64 )) && break
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
rep('# Unit-test sourcing gate (#128): when sourced (not executed), stop here —', funcs + '\n# Unit-test sourcing gate (#128): when sourced (not executed), stop here —')

# variant switch variable (defined near the top of the body so every function sees it)
rep('set -uo pipefail   # NOT -e — we control exit codes\n', 'set -uo pipefail   # NOT -e — we control exit codes\nSGVARIANT="' + variant + '"\n')

# ------------------------------------------------------------------ D. Read/Edit face
rep('''    if echo "$lower_path" | grep -qE '\\.env(\\.[a-z0-9_.-]+)?$|''',
    '''    _sg_hit=0
    if echo "$lower_path" | grep -qE '\\.env(\\.[a-z0-9_.-]+)?$|''')
rep('''|/\\.claude\\.json$'; then
      # (last three branches''', '''|/\\.claude\\.json$|[a-z0-9._-]*(forgejo|gitea)[^ ]*app\\.ini|custom/conf/app\\.ini'; then
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

# ------------------------------------------------------------------ E. risky_patterns edits
# W8 row (after the claude-config row) + python3/node groups
rep('''  # R4-C-4 fix: K8s / Docker container-mounted secret paths in Bash''',
    '''  # W8 (prototype): server-side config files (Forgejo / Gitea app.ini), printing readers only, own left boundary.
  "(^|[^[:alnum:]_.-])(${_SG_READERS_PRINT})[[:space:]]+(([^|]*${_SG_PP_NAME})?(${_SG_SRVCFG}))([^[:alnum:]_]|$)"

  # R4-C-4 fix: K8s / Docker container-mounted secret paths in Bash''')
rep('''  "python3?[[:space:]]+-c([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG})"
  "node[[:space:]]+-e([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG})"''',
    '''  "python3?[[:space:]]+-c([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG}|${_SG_SRVCFG})"
  "node[[:space:]]+-e([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key|${_SG_CLAUDE_CFG}|${_SG_SRVCFG})"''')

if variant == "env_boundary":
    rep('''  "python3?[[:space:]]+-c([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key''',
        '''  "python3?[[:space:]]+-c([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env(rc)?([^A-Za-z0-9_]|$)|provider_key''')
    rep('''  "node[[:space:]]+-e([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key''',
        '''  "node[[:space:]]+-e([^|]*${_SG_PP_SUFFIX})?(/v1/var/|secretsmanager|/secrets/|\\.env(rc)?([^A-Za-z0-9_]|$)|provider_key''')
    rep("""  'lua[[:space:]]+-e[^|]*(/v1/var/|secretsmanager|/secrets/|\\.env|provider_key)'""",
        """  'lua[[:space:]]+-e[^|]*(/v1/var/|secretsmanager|/secrets/|\\.env(rc)?([^A-Za-z0-9_]|$)|provider_key)'""")

# /proc rows (widening only for environ|cmdline; status stays on the narrow reader group)
if variant == "proc_status":
    st = "(environ|status|cmdline)"
else:
    st = "(environ|cmdline)"
rep('''  '(cat|head|tail|less|more|strings|hexdump|od|xxd|tr|awk|perl|rev)[[:space:]]+[^|]*/proc/(self|[0-9]+)/(environ|status|cmdline)'
  '<[[:space:]]*/proc/(self|[0-9]+)/(environ|status|cmdline)\'''',
    '''  "((cat|head|tail|less|more|strings|hexdump|od|xxd|tr|awk|perl|rev)[[:space:]]+[^|]*/proc/(self|[0-9]+)/(environ|status|cmdline)|(cat|head|tail|less|more|strings|hexdump|od|xxd|tr|awk|perl|rev|xargs|sed|grep|egrep|fgrep|rg|cut|paste|nl|sort|base64|cp|dd)[[:space:]]+[^|]*/proc/${_SG_PIDTOK}/(task/[^/[:space:]]+/)?''' + st + ''')"
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
# extract heredoc body
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
# the old block also contained the "Triggering segment" echo after the heredoc; remove duplicates handled above
rep("_sg_judge_one() {\n", emit_fn + "_sg_judge_one() {\n")
# fix the leftover: the original code after the heredoc printed the segment line; our slice removed up to 'return 2'
# W12 normalisation (global, single-key read forms only) + subject selection
rep('''  local seg="$1" mode="$2" pat
  local credit=""
  for pat in "${risky_patterns[@]}"; do
    if [[ "$seg" =~ $pat ]]; then''', '''  local seg="$1" mode="$2" pat
  local credit="" subj="$1"
  if [[ "$SGVARIANT" != env_boundary && "$subj" == *environ* ]]; then
    subj="${subj//".environ.get("/".ek_("}"; subj="${subj//".environb.get("/".ek_("}"
    subj="${subj//".environ["/".ek_["}"; subj="${subj//".environb["/".ek_["}"
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
          _sg_vx_pass "$cmd" segment
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

if variant == "vx_patsub":
    # bad implementation of W10: literal replace-all written as ${s//"$pat"/"$rep"} (bash >= 4.3 drops the inner quotes of the
    # replacement, bash 3.2.57 keeps them as literal characters -> chained assignments are judged on a corrupted copy)
    _o = '  _SG_RP="${out}${s}"\n}'
    assert src.count(_o) == 1
    src = src.replace(_o, '  _SG_RP="${1//"$pat"/"$rep"}"\n}', 1)
if variant == "b4":
    # bad implementation: a bash 4.2+ construct ([[ -v ]]) sitting in a function body
    _o = "# Unit-test sourcing gate (#128): when sourced"
    assert src.count(_o) == 1
    src = src.replace(_o, '_sg_wpa_b4() { [[ -v HOME ]] && return 0; return 1; }\n' + _o, 1)
if variant == "ext_regex":
    # bad implementation of W9: the extension entries are compiled as regular expressions (grep -E) instead of fixed strings
    for _a, _b in (("grep -oFib -f", "grep -oEib -f"), ("grep -qFi -f", "grep -qEi -f")):
        assert src.count(_a) == 1, _a
        src = src.replace(_a, _b, 1)

# ------------------------------------------------------------------ Z. inline the three process-table rows (SC-31 31c: no row made only of a "${VAR}")
import subprocess


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
