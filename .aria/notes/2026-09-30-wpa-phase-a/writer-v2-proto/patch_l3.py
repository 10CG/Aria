#!/usr/bin/env python3
"""Build the v2-design prototype of hooks/secret-scan.sh from the baseline copy.

usage: python3 patch_l3.py <baseline secret-scan.sh> <out secret-scan.sh> [--variant NAME]
variants (for mutation / falsifiability runs):
  v2            the design written into proposal v2
  noident       v2 minus the dotted-identifier exclusion
  nopath        v2 minus the path-form exclusion
  loosepath     path form = any value starting with / (the 'loose reading')
  wl_prefix     v1 whitelist ($ / < / {{ single-char prefixes), applied to existing json key too
  wl_contains   marker words matched anywhere in the value
  wl_nocase     marker words matched case-insensitively
  ent_digit     entropy floor = must contain a digit
  ent_on_old    entropy floor also applied to json-secret-field
  wl_envline    whitelist also applied to env-line-secret-keyword
  noentropy     v2 minus the entropy floor
  w5_append     a prescriptive sentence appended to the additionalContext text (SC-13 13d must catch it)
Rule #7: this file holds no credential-shaped literal.
"""
import re
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
variant = "v2"
if "--variant" in sys.argv:
    variant = sys.argv[sys.argv.index("--variant") + 1]
src = open(src_path, encoding="utf-8").read()

KW = "SECRET|PASSWORD|PASSWD|TOKEN|API_KEY|APIKEY|PRIVATE_KEY|WEBHOOK|ENCRYPTION_KEY|ACCESS_KEY"


def stems():
    multi = [("auth", "token"), ("api", "token"), ("bearer", "token"), ("session", "token"),
             ("registration", "token"), ("jwt", "secret"), ("secret", "key"), ("api", "key"),
             ("access", "token"), ("refresh", "token"), ("client", "secret"), ("private", "key")]
    single = ["token", "sha1", "secret", "password", "passwd"]
    names = []
    for w1, w2 in multi:
        names += [f"{w1}_{w2}", f"{w1}{w2.capitalize()}", f"{w1.capitalize()}{w2.capitalize()}", f"{w1}{w2}"]
    for w in single:
        names += [w, w.capitalize()]
    return names


KEYS = "|".join(sorted(set(stems())))


def ci(word):
    return "".join(f"[{c.lower()}{c.upper()}]" if c.isalpha() else c for c in word)


AUTH = ci("authorization")
CF = ci("cf-access-client-secret")

new_patterns = f"""  # ── v2 prototype: new generic key-shape tags (W2). Inserted after json-secret-field, before bcrypt-hash.
  'json-credential-field|"({KEYS})"[[:space:]]*:[[:space:]]*"[^"]{{16,}}"'
  'json-env-secret-key|"[A-Z0-9_]*({KW})[A-Z0-9_]*"[[:space:]]*:[[:space:]]*"[^"]{{16,}}"'
  'kv-secret-assign|(^|[^A-Za-z0-9_])(export[[:space:]]+)?[A-Z0-9_]*({KW})[A-Z0-9_]*[[:space:]]*[=:][[:space:]]*["'"'"']?[A-Za-z0-9+/=._~-]{{16,}}'
  'auth-header-token|{AUTH}:[[:space:]]*([Tt]oken|[Bb]asic)[[:space:]]+[A-Za-z0-9._/+=-]{{16,}}'
  'cf-access-client-secret|{CF}:[[:space:]]*[A-Za-z0-9._/+=-]{{16,}}'
  'cli-secret-flag|--?[A-Za-z0-9-]*(token|password|passwd|secret|api-key|apikey|access-key)=[A-Za-z0-9+/=._~-]{{16,}}'

"""

anchor = "  # bcrypt hash\n  'bcrypt-hash|"
assert anchor in src
src = src.replace(anchor, new_patterns + anchor, 1)

# W1: extraction
old_ext = "  .tool_response.stdout //\n"
assert old_ext in src
src = src.replace(old_ext, old_ext + "  .tool_response.file.content //\n", 1)

# helper functions inserted before the counting loop
helpers = r'''
# ── v2 prototype helpers: value extraction, whitelist (W3), classifier (W2), fingerprint (W4) ─────────
# No command substitution on the classification path (fork-free): helpers return through the global V.
CLASSIFIED_TAGS=" json-secret-field json-credential-field json-env-secret-key kv-secret-assign auth-header-token cf-access-client-secret cli-secret-flag "
NEW_TAGS=" json-credential-field json-env-secret-key kv-secret-assign auth-header-token cf-access-client-secret cli-secret-flag "
V=""
_trimV() { V="${V#"${V%%[![:space:]]*}"}"; V="${V%"${V##*[![:space:]]}"}"; }
_value_of() {   # $1 tag  $2 span  -> V (value, no quotes)
  local tag="$1" span="$2"
  case "$tag" in
    json-secret-field|json-credential-field|json-env-secret-key)
      V="${span#*:}"; _trimV; V="${V#\"}"; V="${V%\"}" ;;
    kv-secret-assign)
      V="${span#"${span%%[A-Z0-9_]*}"}"; V="${V#*[=:]}"; _trimV; V="${V#[\"\']}" ;;
    auth-header-token|bearer-token) V="${span##*[[:space:]]}" ;;
    cf-access-client-secret|x-api-key-header) V="${span#*:}"; _trimV ;;
    cli-secret-flag|env-line-secret-keyword) V="${span#*=}" ;;
    postgres-url|redis-url|mongodb-url|basic-auth-url)
      V="${span#*://}"; V="${V%%@*}"; V="${V#*:}" ;;
    gcp-private-key-id) V="${span#*:}"; _trimV; V="${V#\"}"; V="${V%\"}" ;;
    pem-private-key-block|pem-header-only) V="" ;;
    *) V="$span" ;;
  esac
}
_RE_RED='^\[REDACTED[^]]*\]$'
_RE_ANGLE='^[<][^<>]*[>]$'
_RE_VARB='^\$\{[^}]*\}$'
_RE_VARU='^\$[A-Z_][A-Z0-9_]*$'
_RE_VARL='^\$[a-z_][a-z0-9_]*$'
_RE_CMDS='^\$\([^)]*\)$'
_RE_TMPL='^\$?\{\{.*\}\}$'
_RE_MASK='^(\*+|x+|X+)$'
_wl_match() {   # whitelist (W3): whole-value placeholder forms + deliberate marker words. rc 0 = placeholder
  local v="$1"
  case "$v" in
    FAKE*|PLACEHOLDER*|NOT-REAL*|NOT_REAL*|NOTREAL*|REDACTED*) return 0 ;;
  esac
  [[ "$v" =~ $_RE_RED ]] && return 0
  [[ "$v" =~ $_RE_ANGLE ]] && return 0
  [[ "$v" =~ $_RE_VARB ]] && return 0
  [[ "$v" =~ $_RE_VARU ]] && return 0
  [[ "$v" =~ $_RE_VARL ]] && return 0
  [[ "$v" =~ $_RE_CMDS ]] && return 0
  [[ "$v" =~ $_RE_TMPL ]] && return 0
  [[ "$v" =~ $_RE_MASK ]] && return 0
  [[ "$v" == *"…" || "$v" == *"..." ]] && return 0
  return 1
}
_entropy_ok() { local v="$1" n=0; [[ "$v" == *[a-z]* ]] && n=$((n+1)); [[ "$v" == *[A-Z]* ]] && n=$((n+1)); [[ "$v" == *[0-9]* ]] && n=$((n+1)); (( n >= 2 )); }
_RE_PATHLEAD='^(/|~/|\./|\.\./)'
_RE_PATHCH='^[A-Za-z0-9._~/-]+$'
_RE_DOTID='^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)+$'
_path_form() {
  local v="$1"
  [[ "$v" =~ $_RE_PATHLEAD ]] || return 1
  [[ "$v" =~ $_RE_PATHCH ]] || return 1
  [[ "$v" == */*/* ]]
}
_dotted_ident() { [[ "$1" =~ $_RE_DOTID ]]; }
FP_ITEMS=""; FP_N=0
_fp_add() {   # $1 value
  (( FP_N >= 10 )) && return 0
  local v="$1" h="" it
  if (( ${#v} < 16 )); then it="L${#v}"
  else
    if command -v sha256sum >/dev/null 2>&1; then h="$(printf '%s' "$v" | sha256sum 2>/dev/null | cut -c1-8)"
    elif command -v shasum >/dev/null 2>&1; then h="$(printf '%s' "$v" | shasum -a 256 2>/dev/null | cut -c1-8)"; fi
    it="${h:--}"
  fi
  FP_ITEMS="${FP_ITEMS:+$FP_ITEMS,}$it"; FP_N=$((FP_N+1))
}
'''

variant_code = {
    "v2": "",
}

# variant adjustments by textual substitution inside helpers
h = helpers
if variant == "noident":
    h = h.replace("_dotted_ident() { [[ \"$1\" =~ $_RE_DOTID ]]; }", "_dotted_ident() { return 1; }")
if variant == "nopath":
    h = h.replace("_path_form() {", "_path_form() { return 1; }\n_path_form_unused() {")
if variant == "loosepath":
    h = h.replace("_path_form() {", "_path_form() { [[ \"$1\" == /* || \"$1\" == ~/* ]]; }\n_path_form_unused() {")
if variant == "path_firstlower":
    # bad implementation: path form = absolute path whose FIRST segment is lower-case (macOS /Users/..., ~/Library/... fall out)
    _o = '  [[ "$v" == */*/* ]]\n}'
    assert h.count(_o) == 1
    h = h.replace(_o, '  [[ "$v" == */*/* ]] || return 1\n  [[ "$v" == /[a-z]* ]]\n}', 1)
if variant == "ent_digit":
    h = h.replace("_entropy_ok() {", "_entropy_ok() { [[ \"$1\" == *[0-9]* ]]; }\n_entropy_ok_unused() {")
if variant == "noentropy":
    h = h.replace("_entropy_ok() {", "_entropy_ok() { return 0; }\n_entropy_ok_unused() {")
if variant == "wl_nocase":
    h = h.replace("  local v=\"$1\"\n  case \"$v\" in\n    FAKE*|PLACEHOLDER*|NOT-REAL*|NOT_REAL*|NOTREAL*|REDACTED*) return 0 ;;\n  esac",
                  "  local v=\"$1\" vu; vu=\"$(printf '%s' \"$v\" | tr '[:lower:]' '[:upper:]')\"\n  case \"$vu\" in\n    FAKE*|PLACEHOLDER*|NOT-REAL*|NOT_REAL*|NOTREAL*|REDACTED*) return 0 ;;\n  esac")
if variant == "wl_contains":
    h = h.replace("    FAKE*|PLACEHOLDER*|NOT-REAL*|NOT_REAL*|NOTREAL*|REDACTED*) return 0 ;;",
                  "    *FAKE*|*PLACEHOLDER*|*NOT-REAL*|*NOT_REAL*|*NOTREAL*|*REDACTED*) return 0 ;;")
if variant == "wl_prefix":
    # v1 whitelist: single-character prefixes < $ {{ (applied to every classified tag incl. the existing json key)
    old = "  [[ \"$v\" =~ $_RE_RED ]] && return 0\n"
    assert old in h
    h = h.replace(old, "  [[ \"$v\" == \\[REDACTED* ]] && return 0\n  [[ \"$v\" == \\<* || \"$v\" == \\$* || \"$v\" == \\{\\{* ]] && return 0\n")

src = src.replace("# ── Scan + count matches", h + "\n# ── Scan + count matches", 1)

# replace the main counting loop body
old_loop_start = "for entry in \"${PATTERNS[@]}\"; do"
i0 = src.index(old_loop_start)
i1 = src.index("if (( matches_total == 0 )); then")
new_loop = r'''for entry in "${PATTERNS[@]}"; do
  tag="${entry%%|*}"
  pattern="${entry#*|}"
  count="$(grep -oE -- "$pattern" "$tmpfile" 2>/dev/null | wc -l | tr -d ' ')"
  [[ -z "$count" ]] && count=0
  if (( count > 0 )); then
    # classification (W2/W3) + fingerprint collection (W4): one pass over the spans, before they are consumed
    keep=0; seen=0
    while IFS= read -r span; do
      seen=$((seen+1))
      if (( seen > 200 )); then keep=$((keep+1)); _value_of "$tag" "$span"; _fp_add "$V"; continue; fi
      _value_of "$tag" "$span"; v="$V"
      if [[ "$CLASSIFIED_TAGS" == *" $tag "* ]]; then
        if [[ "$tag" == "json-secret-field" && "$variant_ent_on_old" == 1 ]] && ! _entropy_ok "$v"; then continue; fi
        _wl_match "$v" && continue
        if [[ "$NEW_TAGS" == *" $tag "* ]]; then
          _entropy_ok "$v" || continue
          _path_form "$v" && continue
          _dotted_ident "$v" && continue
        fi
      elif [[ "$tag" == "env-line-secret-keyword" && "$variant_wl_envline" == 1 ]]; then
        _wl_match "$v" && continue
      fi
      keep=$((keep+1))
      _fp_add "$v"
    done < <(grep -oE -- "$pattern" "$tmpfile" 2>/dev/null)
    sed -i -E "s${SEP}${pattern}${SEP}<secret-scan-counted:${tag}>${SEP}g" "$tmpfile" 2>/dev/null || {
      echo "[secret-scan] WARN: counting-substitution failed for pattern tag=${tag}; skipping" >&2
      continue
    }
    residual="$(grep -oE -- "$pattern" "$tmpfile" 2>/dev/null | wc -l | tr -d ' ')"
    [[ -z "$residual" ]] && residual=0
    if (( residual > 0 )); then
      partial_warns="${partial_warns}[secret-scan] NOTE: pattern ${tag} still present after counting-substitution (${residual} span(s) could not be isolated for exact counting); match count may be under-reported."$'\n'
      actual_counted=$(( keep - residual ))
      if (( actual_counted > 0 )); then
        matches_total=$(( matches_total + actual_counted ))
        matches_breakdown="${matches_breakdown}${tag}=${actual_counted}+${residual}-uncounted "
      else
        matches_breakdown="${matches_breakdown}${tag}=0+${residual}-uncounted "
      fi
      continue
    fi
    if (( keep > 0 )); then
      matches_total=$(( matches_total + keep ))
      matches_breakdown="${matches_breakdown}${tag}=${keep} "
    fi
  fi
done

'''
src = src[:i0] + new_loop + src[i1:]

# variant flags
src = src.replace("matches_total=0\n", "variant_ent_on_old=%d\nvariant_wl_envline=%d\nmatches_total=0\n" % (1 if variant == "ent_on_old" else 0, 1 if variant == "wl_envline" else 0), 1)

# PEM pre-pass counts have no fp item; add '-' for the PEM block count
src = src.replace('      matches_breakdown="${matches_breakdown}pem-private-key-block=${pem_count} "\n',
                  '      matches_breakdown="${matches_breakdown}pem-private-key-block=${pem_count} "\n      for _i in $(seq 1 "$pem_count"); do (( FP_N < 10 )) && { FP_ITEMS="${FP_ITEMS:+$FP_ITEMS,}-"; FP_N=$((FP_N+1)); }; done\n', 1)

# W4: 9th log field; W5: addl insertion
src = src.replace('''printf '%s\\t%s\\t%s\\tSCAN-DETECT\\ttool=%s\\tmatches=%s\\tbreakdown=%s\\tsize=%s\\n' \\
  "$(date -u +%FT%TZ)" "${USER:-unknown}" "${PWD:-unknown}" \\
  "$tool" "$matches_total" "${matches_breakdown% }" "$input_size" \\''',
'''printf '%s\\t%s\\t%s\\tSCAN-DETECT\\ttool=%s\\tmatches=%s\\tbreakdown=%s\\tsize=%s\\tfp=%s\\n' \\
  "$(date -u +%FT%TZ)" "${USER:-unknown}" "${PWD:-unknown}" \\
  "$tool" "$matches_total" "${matches_breakdown% }" "$input_size" "${FP_ITEMS:--}" \\''', 1)

old_addl = 'addl_msg="[secret-scan] DETECTED ${matches_total} secret-shape match(es) in tool output — treat as'
assert old_addl in src
new_addl = '''src_desc="$tool"
if [[ "$tool" == "Read" || "$tool" == "Write" ]]; then
  fpth="$(printf '%s' "$input" | jq -r '.tool_input.file_path // ""' 2>/dev/null)"
  fpth="${fpth%$'\\r'}"
  [[ -n "$fpth" ]] && src_desc="$tool $fpth"
fi
addl_msg="[secret-scan] DETECTED ${matches_total} secret-shape match(es) in tool output (tags: ${matches_breakdown% }; source: ${src_desc}) — treat as'''
src = src.replace(old_addl, new_addl, 1)

if variant == "fp_span":
    # bad implementation of W4: the fingerprint of every tag other than the JSON key-shape tags is taken over the WHOLE span
    # (the rule 'key-shape tags take the value, everything else the span'); classification keeps using the real value
    _o = '      keep=$((keep+1))\n      _fp_add "$v"\n'
    assert src.count(_o) == 1
    src = src.replace(_o, '      keep=$((keep+1))\n      case "$tag" in json-secret-field|json-credential-field|json-env-secret-key) _fp_add "$v" ;; *) _fp_add "$span" ;; esac\n', 1)
if variant == "w5_append":
    # bad implementation of W5: a prescriptive sentence appended after the original text (13d must catch it)
    tail = "already produced.)\"\nsys_msg="
    assert tail in src
    src = src.replace(tail, "already produced.) Also run the credential rotation script now.\"\nsys_msg=", 1)
open(out_path, "w", encoding="utf-8").write(src)
print("wrote", out_path, "variant", variant)
