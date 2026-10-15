#!/usr/bin/env python3
"""Build the v3-design PROTOTYPE of hooks/secret-scan.sh from the baseline copy.

usage: python3 patch_l3.py <baseline secret-scan.sh> <out secret-scan.sh> [--variant NAME[:ARG]]

The prototype is not the implementation: it is generated from the baseline by text substitution and only shows that the
design written in proposal v3 is reachable, and which bad implementations the probe rows catch.

Variants (every non-v3 variant is a 'bad implementation' that the probe rows must catch):
  v3                the design written into proposal v3
  -- whitelist (W3), v3 whitelist = <...> / ${...} / {{...}} / [REDACTED...] / mask / unicode-ellipsis suffix / marker words
  wl_varname_lc     re-adds the removed bare $name (lower-case + digits + _) class
  wl_varname_uc     re-adds the removed bare $NAME (upper-case + digits + _) class
  wl_varname_any    re-adds a bare variable reference of ANY case ($ + identifier)
  wl_cmdsub         re-adds the removed $(...) class
  wl_dots_ascii     re-adds the removed ASCII '...' suffix class
  wl_angle_prefix / wl_angle_suffix / wl_angle_loose / wl_angle_noend    angle form: '<' only / '>' only / inner <> allowed / no end anchor
  wl_brace_prefix / wl_brace_noend                                       ${...}: '${' only / no end anchor
  wl_tmpl_prefix / wl_tmpl_suffix / wl_tmpl_noend                        {{...}}: '{{' only / '}}' only / no end anchor
  wl_red_prefix / wl_red_anybracket                                      [REDACTED...]: '[REDACTED' only / any [...]
  wl_mask_prefix / wl_mask_mixed                                         mask: leading '*' only / any mix of * x X
  wl_ell_contains / wl_ell_prefix                                        unicode ellipsis: anywhere / leading
  ell_lastchar                                                           unicode ellipsis tested on the last CHARACTER (locale-dependent: wrong in the POSIX locale)  -> SC-32 32e
  wl_prefix wl_contains wl_nocase wl_envline                             (v2) single-char prefixes / marker words anywhere / case-insensitive / applied to env-line
  wl_drop:CLASS     the class is missing: angle brace tmpl tmpl_dollar red mask_star mask_x mask_X ellipsis
                    marker_FAKE marker_PLACEHOLDER marker_NOT-REAL marker_NOT_REAL marker_NOTREAL marker_REDACTED
  -- classifier (W2)
  ent_digit ent_on_old noentropy noident nopath loosepath path_firstlower     (v2)
  floor15 / floor17 value length floor 15 / 17 instead of 16 for the new tags
  ent_drop:C        the entropy floor does not count character class C (lower upper digit)
  drop_lead:L       path-form rule lacks the lead marker L ('/' '~/' './' '../')
  path_plus / path_eq   the path-form character class wrongly admits '+' / '='
  name_loose        the JSON key table matches a key that merely CONTAINS a table stem (prefix / suffix word characters allowed): SC-9 9x
  kv_lowercase      the kv key accepts lower-case keywords (closes the lower-case YAML / INI known limits 10d / 10j)
  add_dollar:G      the value character class of group G (kv = kv-secret-assign + cli-secret-flag, hdr = the two header tags) also admits '$' (variable references become spans): SC-9 9l / 9m
  fp_relpath / fp_kebab  close an accepted false-positive class: any value with an inner '/' (no '+' '=') treated as a path / a lower-case kebab-case value treated as an identifier (SC-10 10l)
  drop_vsym:G:S     value character class lacks the symbol S (G = kv for kv-secret-assign and cli-secret-flag, hdr for the two header tags)
  cli_dash2         cli-secret-flag needs a double dash (single-dash -token=... not counted)
  drop_name:N       json-credential-field name table lacks the name N
  drop_kwjson:K     json-env-secret-key keyword set lacks K
  drop_kwkv:K       kv-secret-assign keyword set lacks K
  drop_flag:S       cli-secret-flag suffix set lacks S
  drop_scheme:W     auth-header-token scheme words lack W (token Token basic Basic)
  hdr_case_sensitive  header names matched in one fixed spelling
  no_cap            no iteration cap: every span is iterated (v2 cost model)
  -- fingerprint (W4)
  fp_span fp_wrong:TAG (TAG = any tag of the value-body table except the two PEM tags, whose fp item is `-` and does not go through the table)
  hdronly_fp (a hash item for the PEM header-only fallback) hdronly_noitem (the header-only fallback records no item) pem_nofp (the PEM block records no fp item) pem_hash (the PEM block records a hash item instead of `-`)
  pem_last (the PEM block's `-` item is recorded after the pattern items, not first)
  -- alert text (W5)
  w5_append w5_path
  -- v5 additions (R4 findings)
  nul_replace       the NUL bytes are replaced by newlines INSIDE the extraction, replacing the baseline view (the previous design: UTF-16-shaped text loses its baseline detection)  -> SC-1 1e / 1f
  nul_always_append the NUL view is appended whenever the input holds the 6 characters `\u0000`, without comparing it with the baseline view (a literal text mention doubles every count)  -> SC-1 1g
  nul_always_view   a second view (NUL -> newline) is appended to every input (no NUL pre-check): every count doubles
  nul_space         NUL bytes become spaces in the second view (the record anchors are lost)                                       -> SC-1 1c / 1d
  cli_unbounded     cli-secret-flag with an unbounded flag-name prefix, left boundary kept (still quadratic on a long run of `-` or of `--x`)                  -> SC-34 34b
  kv_unbounded      kv-secret-assign with unbounded key prefix / suffix (quadratic on a long upper-case run)                       -> SC-34 34b
  val_quadratic     value extraction with the O(n^2) prefix-removal idioms (`##*[[:space:]]`, `#*=`, `#"${V%%...}"`)               -> SC-34 34a / 34b
  cli_v4            the cli-secret-flag pattern of the previous design: no left boundary, unbounded flag-name prefix (quadratic on a long run of `-`)            -> SC-34 34b
  cli_noleft        cli-secret-flag with the prefix bound but WITHOUT the left boundary (linear, but 20 us per `-` of a long run: a 300 KB run costs seconds)         -> SC-34 34b / SC-10 10o
  kv_left_boundary_off  kv-secret-assign without its left boundary (a word character before the key is accepted)                   -> SC-9 9z
Rule #7: this file holds no credential-shaped literal.
"""
import re
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
variant = "v5"
if "--variant" in sys.argv:
    variant = sys.argv[sys.argv.index("--variant") + 1]
vname, _, varg = variant.partition(":")
KNOWN = set("""v5 v4 v3 wl_varname_lc wl_varname_uc wl_varname_any wl_cmdsub wl_dots_ascii wl_angle_prefix wl_angle_suffix wl_angle_loose wl_angle_noend
wl_brace_prefix wl_brace_noend wl_tmpl_prefix wl_tmpl_suffix wl_tmpl_noend wl_red_prefix wl_red_anybracket wl_mask_prefix wl_mask_mixed wl_ell_contains
wl_ell_prefix ell_lastchar wl_prefix wl_contains wl_nocase wl_envline wl_drop ent_digit ent_on_old noentropy noident nopath loosepath path_firstlower floor15 floor17
ent_drop drop_lead path_plus path_eq name_loose kv_lowercase add_dollar fp_relpath fp_kebab drop_vsym cli_dash2 drop_name drop_kwjson drop_kwkv drop_flag
drop_scheme hdr_case_sensitive no_cap fp_span fp_wrong hdronly_fp hdronly_noitem pem_nofp pem_hash pem_last w5_append w5_path
nul_off ent_range step_on cls_all pd_on_old oldkey_drop drop_extract fp_le16 fp_lt20 fp_lt13 hash_nosha256sum hash_noshasum val_eval
nul_replace nul_always_append nul_always_view nul_space cli_unbounded cli_v4 cli_noleft kv_unbounded val_quadratic kv_left_boundary_off""".split())
if vname not in KNOWN:
    sys.stderr.write("unknown variant %r\n" % vname)
    sys.exit(64)
src = open(src_path, encoding="utf-8").read()

KW = ["SECRET", "PASSWORD", "PASSWD", "TOKEN", "API_KEY", "APIKEY", "PRIVATE_KEY", "WEBHOOK", "ENCRYPTION_KEY", "ACCESS_KEY"]
FLAGS = ["token", "password", "passwd", "secret", "api-key", "apikey", "access-key"]


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


def ci(word):
    return "".join(f"[{c.lower()}{c.upper()}]" if c.isalpha() else c for c in word)


names = sorted(set(stems()))
kw_json, kw_kv, flags = list(KW), list(KW), list(FLAGS)
if vname == "drop_name":
    assert varg in names, varg
    names.remove(varg)
if vname == "drop_kwjson":
    assert varg in kw_json, varg
    kw_json.remove(varg)
if vname == "drop_kwkv":
    assert varg in kw_kv, varg
    kw_kv.remove(varg)
if vname == "drop_flag":
    assert varg in flags, varg
    flags.remove(varg)
floor = 16
if vname == "floor15":
    floor = 15
if vname == "floor17":
    floor = 17

KV_SYMS, HDR_SYMS = ["+", "/", "=", ".", "_", "~", "-"], [".", "_", "/", "+", "=", "-"]
if vname == "drop_vsym":
    _g, _, _s = varg.partition(":")
    assert _g in ("kv", "hdr"), varg
    if _g == "kv":
        assert _s in KV_SYMS, varg
        KV_SYMS = [x for x in KV_SYMS if x != _s]
    else:
        assert _s in HDR_SYMS, varg
        HDR_SYMS = [x for x in HDR_SYMS if x != _s]


def _cls(syms):
    s = [x for x in syms if x != "-"] + (["-"] if "-" in syms else [])
    return "[A-Za-z0-9" + "".join(s) + "]"


KVC, HDRC = _cls(KV_SYMS), _cls(HDR_SYMS)
if vname != "drop_vsym":
    assert KVC == "[A-Za-z0-9+/=._~-]" and HDRC == "[A-Za-z0-9._/+=-]", (KVC, HDRC)
if vname == "add_dollar":
    assert varg in ("kv", "hdr"), varg
    if varg == "kv":
        KVC = KVC.replace("[A-Za-z0-9", "[A-Za-z0-9$", 1)
    else:
        HDRC = HDRC.replace("[A-Za-z0-9", "[A-Za-z0-9$", 1)
DASH = "--" if vname == "cli_dash2" else "--?"
CLI_PREFIX = "[A-Za-z0-9-]*" if vname in ("cli_unbounded", "cli_v4") else "[A-Za-z0-9-]{0,40}"
CLI_LEFT = "" if vname in ("cli_v4", "cli_noleft") else "(^|[^A-Za-z0-9-])"
KEYS = "|".join(names)
KWJ = "|".join(kw_json)
KWK = "|".join(kw_kv)
KEYCLS_JSON_LEFT = KEYCLS_JSON_RIGHT = ""
KVKEY = "[A-Z0-9_]*" if vname == "kv_unbounded" else "[A-Z0-9_]{0,64}"
KVLEFT = "" if vname == "kv_left_boundary_off" else "(^|[^A-Za-z0-9_])"
if vname == "name_loose":
    KEYCLS_JSON_LEFT = KEYCLS_JSON_RIGHT = "[A-Za-z0-9_]*"
if vname == "kv_lowercase":
    KWK = KWK + "|" + "|".join(k.lower() for k in kw_kv)
    KVKEY = "[A-Za-z0-9_]*" if vname == "kv_unbounded" else "[A-Za-z0-9_]{0,64}"
FLG = "|".join(flags)
AUTH = ci("authorization")
CF = ci("cf-access-client-secret")
if vname == "hdr_case_sensitive":
    AUTH, CF = "Authorization", "CF-Access-Client-Secret"
# scheme words: token / Token / basic / Basic = four members of two letter classes
tok_alt = "[Tt]oken"
bas_alt = "[Bb]asic"
if vname == "drop_scheme":
    assert varg in ("token", "Token", "basic", "Basic"), varg
    if varg == "token":
        tok_alt = "Token"
    elif varg == "Token":
        tok_alt = "token"
    elif varg == "basic":
        bas_alt = "Basic"
    else:
        bas_alt = "basic"
SCHEME = f"({tok_alt}|{bas_alt})"

new_patterns = f"""  # ── v3 prototype: new generic key-shape tags (W2). Inserted after json-secret-field, before bcrypt-hash.
  'json-credential-field|"{KEYCLS_JSON_LEFT}({KEYS}){KEYCLS_JSON_RIGHT}"[[:space:]]*:[[:space:]]*"[^"]{{{floor},}}"'
  'json-env-secret-key|"[A-Z0-9_]*({KWJ})[A-Z0-9_]*"[[:space:]]*:[[:space:]]*"[^"]{{{floor},}}"'
  'kv-secret-assign|{KVLEFT}(export[[:space:]]+)?{KVKEY}({KWK}){KVKEY}[[:space:]]*[=:][[:space:]]*["'"'"']?{KVC}{{{floor},}}'
  'auth-header-token|{AUTH}:[[:space:]]*{SCHEME}[[:space:]]+{HDRC}{{{floor},}}'
  'cf-access-client-secret|{CF}:[[:space:]]*{HDRC}{{{floor},}}'
  'cli-secret-flag|{CLI_LEFT}{DASH}{CLI_PREFIX}({FLG})={KVC}{{{floor},}}'

"""

anchor = "  # bcrypt hash\n  'bcrypt-hash|"
assert anchor in src
src = src.replace(anchor, new_patterns + anchor, 1)

# W1: extraction
old_ext = "  .tool_response.stdout //\n"
assert old_ext in src
src = src.replace(old_ext, old_ext + "  .tool_response.file.content //\n", 1)
# v5 (R4 U cluster): the extraction keeps its baseline form (bash drops NUL bytes inside the command substitution: that is the BASELINE view, and it is what makes text
# with a NUL between every two ASCII characters -- UTF-16LE -- scan as plain ASCII).  A NUL-delimited body (/proc/<pid>/environ, `env -0`) is glued into one line by that
# view, so when the raw envelope holds a JSON `\u0000` escape a SECOND view is appended: the same extraction with NUL -> newline.  The second view is appended only when it
# differs from the first, so every input without a real NUL is scanned exactly as at baseline.
_prog_o = "content=\"$(printf '%s' \"$input\" | jq -r '  # crlf-ok: data body being SCANNED (internal counting scratch only) — must NOT CR-strip (would corrupt user content, Spec C2)\n"
assert src.count(_prog_o) == 1, src.count(_prog_o)
_i0 = src.index(_prog_o)
_i1 = src.index("' 2>/dev/null)\"\n", _i0) + len("' 2>/dev/null)\"\n")
_prog_body = src[_i0 + len(_prog_o): _i1 - len("' 2>/dev/null)\"\n")]       # the jq filter lines after the comment line
_PROG = ("_content_prog='  # crlf-ok: data body being SCANNED (internal counting scratch only) — must NOT CR-strip (would corrupt user content, Spec C2)\n"
         + _prog_body + "'\n")
if vname == "nul_replace":      # the previous design: NUL -> newline inside the extraction, replacing the baseline view
    _NEW = src[_i0:_i1].replace("' 2>/dev/null)\"\n", "' 2>/dev/null | tr '\\000' '\\n')\"\n")
elif vname == "nul_off":
    _NEW = src[_i0:_i1]
else:
    _NEW = (_PROG
            + "content=\"$(printf '%s' \"$input\" | jq -r \"$_content_prog\" 2>/dev/null)\"   # crlf-ok: data body being SCANNED (same filter as the baseline extraction)\n")
    _tr = "tr '\\000' ' '" if vname == "nul_space" else "tr '\\000' '\\n'"
    _view = ("  _nul_view=\"$(printf '%s' \"$input\" | jq -r \"$_content_prog\" 2>/dev/null | " + _tr + ")\"   # crlf-ok: data body being SCANNED\n")
    if vname == "nul_always_view":
        _NEW += "{\n" + _view + "  content=\"${content}\"$'\\n'\"${_nul_view}\"\n}\n"
    else:
        _guard = "" if vname == "nul_always_append" else "  [[ \"$_nul_view\" != \"$content\" ]] && "
        _NEW += ("# NUL bytes (a JSON \\u0000 escape in the envelope): the NUL-delimited view is scanned IN ADDITION to the baseline view\n"
                 "if [[ \"$input\" == *'\\u0000'* ]]; then\n" + _view
                 + ("  [[ \"$_nul_view\" != \"$content\" ]] && content=\"${content}\"$'\\n'\"${_nul_view}\"\n" if vname != "nul_always_append"
                    else "  content=\"${content}\"$'\\n'\"${_nul_view}\"\n")
                 + "fi\n")
src = src[:_i0] + _NEW + src[_i1:]
if vname == "drop_extract":
    assert varg in ("tool_result.content", "tool_result.output"), varg
    _de = "  ." + varg + " //\n"
    assert src.count(_de) == 1, src.count(_de)
    src = src.replace(_de, "", 1)
if vname == "oldkey_drop":
    _ok = "|webhook_secret|encryption_key)\"[[:space:]]*:[[:space:]]*\"[^\"]{8,}\"'"
    assert src.count(_ok) == 1, src.count(_ok)
    assert varg in ("webhook_secret", "encryption_key"), varg
    src = src.replace(_ok, _ok.replace("|" + varg, "", 1), 1)

OLD_VALUE_HELPERS = r'''_trimV() { V="${V#"${V%%[![:space:]]*}"}"; V="${V%"${V##*[![:space:]]}"}"; }
_value_of() {   # $1 tag  $2 span  -> V (value, no quotes)
  local tag="$1" span="$2"
  case "$tag" in
    json-secret-field|json-credential-field|json-env-secret-key)
      V="${span#*:}"; _trimV; V="${V#\"}"; V="${V%\"}" ;;
    kv-secret-assign)
      V="${span#"${span%%[ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_]*}"}"; V="${V#*[=:]}"; _trimV; V="${V#[\"\']}" ;;
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
'''
helpers = r'''
# ── v3 prototype helpers: value extraction, whitelist (W3), classifier (W2), fingerprint (W4) ─────────
# No command substitution on the classification path (fork-free): helpers return through the global V.
CLASSIFIED_TAGS=" json-secret-field json-credential-field json-env-secret-key kv-secret-assign auth-header-token cf-access-client-secret cli-secret-flag "
NEW_TAGS=" json-credential-field json-env-secret-key kv-secret-assign auth-header-token cf-access-client-secret cli-secret-flag "
V=""
_RE_TRIM='^[[:space:]]*(.*[^[:space:]])[[:space:]]*$'
_RE_LASTWORD='([^[:space:]]+)$'
# Value extraction is LINEAR: the text after the first delimiter is taken by LENGTH (`${s%%X*}` finds the delimiter by one left-to-right scan, `${s:N}` cuts), and the
# last word / the trimmed value come from a `[[ =~ ]]` capture.  NOT `${s#*X}` / `${s##*X}` / `${V#"${V%%...}"}`: bash tries the prefixes one by one and each try costs O(length), so
# on a long run (a 16 KB token, a 16 KB blank run) they are O(n^2) -- seconds to a minute of CPU, past the hook's 5 s timeout.
_trimV() { if [[ "$V" =~ $_RE_TRIM ]]; then V="${BASH_REMATCH[1]}"; else V=""; fi; }
_value_of() {   # $1 tag  $2 span  -> V (value, no quotes)
  local tag="$1" span="$2" k
  case "$tag" in
    json-secret-field|json-credential-field|json-env-secret-key)
      k="${span%%:*}"; V="${span:${#k}+1}"; _trimV; V="${V#\"}"; V="${V%\"}" ;;
    kv-secret-assign)
      k="${span%%[ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_]*}"; V="${span:${#k}}"; k="${V%%[=:]*}"; V="${V:${#k}+1}"; _trimV; V="${V#[\"\']}" ;;
    auth-header-token|bearer-token) if [[ "$span" =~ $_RE_LASTWORD ]]; then V="${BASH_REMATCH[1]}"; else V="$span"; fi ;;
    cf-access-client-secret|x-api-key-header) k="${span%%:*}"; V="${span:${#k}+1}"; _trimV ;;
    cli-secret-flag|env-line-secret-keyword) k="${span%%=*}"; V="${span:${#k}+1}" ;;
    postgres-url|redis-url|mongodb-url|basic-auth-url)
      k="${span%%://*}"; V="${span:${#k}+3}"; V="${V%%@*}"; k="${V%%:*}"; V="${V:${#k}+1}" ;;
    gcp-private-key-id) k="${span%%:*}"; V="${span:${#k}+1}"; _trimV; V="${V#\"}"; V="${V%\"}" ;;
    pem-private-key-block|pem-header-only) V="" ;;
    *) V="$span" ;;
  esac
}
_RE_RED='^\[REDACTED[^]]*\]$'
_RE_ANGLE='^[<][^<>]*[>]$'
_RE_VARB='^\$\{[^}]*\}$'
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
  [[ "$v" =~ $_RE_TMPL ]] && return 0
  [[ "$v" =~ $_RE_MASK ]] && return 0
  [[ "$v" == *"…" ]] && return 0
  return 1
}
_entropy_ok() { local v="$1" n=0; [[ "$v" == *[abcdefghijklmnopqrstuvwxyz]* ]] && n=$((n+1)); [[ "$v" == *[ABCDEFGHIJKLMNOPQRSTUVWXYZ]* ]] && n=$((n+1)); [[ "$v" == *[0123456789]* ]] && n=$((n+1)); (( n >= 2 )); }
_RE_PATHLEAD='^(/|~/|\./|\.\./)'
_AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'; _az='abcdefghijklmnopqrstuvwxyz'; _09='0123456789'   # enumerated, no ranges: locale-independent in every bash
_RE_PATHCH="^[${_AZ}${_az}${_09}._~/-]+\$"
_RE_DOTID="^[${_AZ}${_az}_][${_AZ}${_az}${_09}_]*(\\.[${_AZ}${_az}_][${_AZ}${_az}${_09}_]*)+\$"
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

# ------------------------------------------------------------------ variants (textual substitution inside the helpers)
h = helpers
if vname == "val_quadratic":       # bad implementation: the O(n^2) prefix-removal idioms (the extraction is otherwise the same)
    _i0 = h.index("_RE_TRIM=")
    _i1 = h.index("_RE_RED='^")
    h = h[:_i0] + OLD_VALUE_HELPERS + h[_i1:]
if vname == "val_eval":      # bad implementation: strip the quotes of the extracted value with eval (executes the text)
    _ve = '    *) V="$span" ;;\n  esac\n}\n_RE_RED='
    assert h.count(_ve) == 1
    h = h.replace(_ve, '    *) V="$span" ;;\n  esac\n  V="$(eval "printf \'%s\' \\"$V\\"")"\n}\n_RE_RED=')


def sub(old, new, count=1):
    global h
    assert h.count(old) == count, f"{vname}: anchor {old[:60]!r} found {h.count(old)}x"
    h = h.replace(old, new)


WL_LINES = {
    "red": "  [[ \"$v\" =~ $_RE_RED ]] && return 0\n",
    "angle": "  [[ \"$v\" =~ $_RE_ANGLE ]] && return 0\n",
    "brace": "  [[ \"$v\" =~ $_RE_VARB ]] && return 0\n",
    "tmpl": "  [[ \"$v\" =~ $_RE_TMPL ]] && return 0\n",
    "mask": "  [[ \"$v\" =~ $_RE_MASK ]] && return 0\n",
    "ellipsis": "  [[ \"$v\" == *\"…\" ]] && return 0\n",
}
MARKERS = ["FAKE", "PLACEHOLDER", "NOT-REAL", "NOT_REAL", "NOTREAL", "REDACTED"]

# re-added (removed-by-v3) classes -------------------------------------------------------------
if vname == "wl_varname_lc":
    sub("  [[ \"$v\" =~ $_RE_MASK ]] && return 0\n", "  [[ \"$v\" =~ ^\\$[a-z_][a-z0-9_]*$ ]] && return 0\n  [[ \"$v\" =~ $_RE_MASK ]] && return 0\n")
if vname == "wl_varname_uc":
    sub("  [[ \"$v\" =~ $_RE_MASK ]] && return 0\n", "  [[ \"$v\" =~ ^\\$[A-Z_][A-Z0-9_]*$ ]] && return 0\n  [[ \"$v\" =~ $_RE_MASK ]] && return 0\n")
if vname == "wl_varname_any":
    sub("  [[ \"$v\" =~ $_RE_MASK ]] && return 0\n", "  [[ \"$v\" =~ ^\\$[A-Za-z_][A-Za-z0-9_]*$ ]] && return 0\n  [[ \"$v\" =~ $_RE_MASK ]] && return 0\n")
if vname == "wl_cmdsub":
    sub("_RE_MASK='^(\\*+|x+|X+)$'\n", "_RE_MASK='^(\\*+|x+|X+)$'\n_RE_CMDS='^\\$\\([^)]*\\)$'\n")
    sub("  [[ \"$v\" =~ $_RE_MASK ]] && return 0\n", "  [[ \"$v\" =~ $_RE_CMDS ]] && return 0\n  [[ \"$v\" =~ $_RE_MASK ]] && return 0\n")
if vname == "wl_dots_ascii":
    sub("  [[ \"$v\" == *\"…\" ]] && return 0\n", "  [[ \"$v\" == *\"…\" || \"$v\" == *\"...\" ]] && return 0\n")
# boundary mutants -----------------------------------------------------------------------------
if vname == "wl_angle_prefix":
    sub("_RE_ANGLE='^[<][^<>]*[>]$'", "_RE_ANGLE='^[<]'")
if vname == "wl_angle_suffix":
    sub("_RE_ANGLE='^[<][^<>]*[>]$'", "_RE_ANGLE='[>]$'")
if vname == "wl_angle_loose":
    sub("_RE_ANGLE='^[<][^<>]*[>]$'", "_RE_ANGLE='^[<].*[>]$'")
if vname == "wl_angle_noend":
    sub("_RE_ANGLE='^[<][^<>]*[>]$'", "_RE_ANGLE='^[<][^<>]*[>]'")
if vname == "wl_brace_prefix":
    sub("_RE_VARB='^\\$\\{[^}]*\\}$'", "_RE_VARB='^\\$\\{'")
if vname == "wl_brace_noend":
    sub("_RE_VARB='^\\$\\{[^}]*\\}$'", "_RE_VARB='^\\$\\{[^}]*\\}'")
if vname == "wl_tmpl_prefix":
    sub("_RE_TMPL='^\\$?\\{\\{.*\\}\\}$'", "_RE_TMPL='^\\$?\\{\\{'")
if vname == "wl_tmpl_suffix":
    sub("_RE_TMPL='^\\$?\\{\\{.*\\}\\}$'", "_RE_TMPL='\\}\\}$'")
if vname == "wl_tmpl_noend":
    sub("_RE_TMPL='^\\$?\\{\\{.*\\}\\}$'", "_RE_TMPL='^\\$?\\{\\{.*\\}\\}'")
if vname == "wl_red_prefix":
    sub("_RE_RED='^\\[REDACTED[^]]*\\]$'", "_RE_RED='^\\[REDACTED'")
if vname == "wl_red_anybracket":
    sub("_RE_RED='^\\[REDACTED[^]]*\\]$'", "_RE_RED='^\\[.*\\]$'")
if vname == "wl_mask_prefix":
    sub("_RE_MASK='^(\\*+|x+|X+)$'", "_RE_MASK='^\\*'")
if vname == "wl_mask_mixed":
    sub("_RE_MASK='^(\\*+|x+|X+)$'", "_RE_MASK='^[*xX]+$'")
if vname == "wl_ell_contains":
    sub("[[ \"$v\" == *\"…\" ]] && return 0", "[[ \"$v\" == *\"…\"* ]] && return 0")
if vname == "wl_ell_prefix":
    sub("[[ \"$v\" == *\"…\" ]] && return 0", "[[ \"$v\" == \"…\"* ]] && return 0")
if vname == "kv_lowercase":      # the value extraction of this bad implementation is widened together with its pattern (an implementation that reads lower-case keys skips the key with the same class)
    sub('k="${span%%[ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_]*}"; V="${span:${#k}}"', 'k="${span%%[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_]*}"; V="${span:${#k}}"')
if vname == "ell_lastchar":      # bad implementation (locale-dependent): the ellipsis suffix is tested on the LAST CHARACTER -- one character in a UTF-8 locale, one BYTE in the POSIX locale
    sub("[[ \"$v\" == *\"…\" ]] && return 0", "[[ \"${v: -1}\" == \"…\" ]] && return 0")
# v2 mutants -------------------------------------------------------------------------------------
if vname == "wl_nocase":
    sub("  local v=\"$1\"\n  case \"$v\" in\n    FAKE*|PLACEHOLDER*|NOT-REAL*|NOT_REAL*|NOTREAL*|REDACTED*) return 0 ;;\n  esac",
        "  local v=\"$1\" vu; vu=\"$(printf '%s' \"$v\" | tr '[:lower:]' '[:upper:]')\"\n  case \"$vu\" in\n    FAKE*|PLACEHOLDER*|NOT-REAL*|NOT_REAL*|NOTREAL*|REDACTED*) return 0 ;;\n  esac")
if vname == "wl_contains":
    sub("    FAKE*|PLACEHOLDER*|NOT-REAL*|NOT_REAL*|NOTREAL*|REDACTED*) return 0 ;;",
        "    *FAKE*|*PLACEHOLDER*|*NOT-REAL*|*NOT_REAL*|*NOTREAL*|*REDACTED*) return 0 ;;")
if vname == "wl_prefix":
    old = "  [[ \"$v\" =~ $_RE_RED ]] && return 0\n"
    sub(old, "  [[ \"$v\" == \\[REDACTED* ]] && return 0\n  [[ \"$v\" == \\<* || \"$v\" == \\$* || \"$v\" == \\{\\{* ]] && return 0\n")
# drop-a-member ----------------------------------------------------------------------------------
if vname == "wl_drop":
    if varg.startswith("marker_"):
        w = varg[len("marker_"):]
        assert w in MARKERS, w
        sub("    FAKE*|PLACEHOLDER*|NOT-REAL*|NOT_REAL*|NOTREAL*|REDACTED*) return 0 ;;",
            "    " + "|".join(m + "*" for m in MARKERS if m != w) + ") return 0 ;;")
    elif varg == "tmpl_dollar":
        sub("_RE_TMPL='^\\$?\\{\\{.*\\}\\}$'", "_RE_TMPL='^\\{\\{.*\\}\\}$'")
    elif varg == "mask_star":
        sub("_RE_MASK='^(\\*+|x+|X+)$'", "_RE_MASK='^(x+|X+)$'")
    elif varg == "mask_x":
        sub("_RE_MASK='^(\\*+|x+|X+)$'", "_RE_MASK='^(\\*+|X+)$'")
    elif varg == "mask_X":
        sub("_RE_MASK='^(\\*+|x+|X+)$'", "_RE_MASK='^(\\*+|x+)$'")
    else:
        assert varg in WL_LINES, varg
        sub(WL_LINES[varg], "")
# classifier ---------------------------------------------------------------------------------------
if vname == "noident":
    sub("_dotted_ident() { [[ \"$1\" =~ $_RE_DOTID ]]; }", "_dotted_ident() { return 1; }")
if vname == "nopath":
    sub("_path_form() {", "_path_form() { return 1; }\n_path_form_unused() {")
if vname == "loosepath":
    sub("_path_form() {", "_path_form() { [[ \"$1\" == /* || \"$1\" == ~/* ]]; }\n_path_form_unused() {")
if vname == "fp_relpath":
    sub("_path_form() {", "_path_form() { [[ \"$1\" == */* && \"$1\" != *[+=]* ]] && return 0; _path_form_orig \"$1\"; }\n_path_form_orig() {")
if vname == "fp_kebab":
    sub("_dotted_ident() { [[ \"$1\" =~ $_RE_DOTID ]]; }", "_RE_KEBAB='^[a-z0-9]+(-[a-z0-9]+)+$'\n_dotted_ident() { [[ \"$1\" =~ $_RE_DOTID ]] || [[ \"$1\" =~ $_RE_KEBAB ]]; }")
if vname == "path_firstlower":
    _o = '  [[ "$v" == */*/* ]]\n}'
    sub(_o, '  [[ "$v" == */*/* ]] || return 1\n  [[ "$v" == /[a-z]* ]]\n}')
if vname == "ent_drop":
    assert varg in ("lower", "upper", "digit"), varg
    _pat = {"lower": '[[ "$v" == *[abcdefghijklmnopqrstuvwxyz]* ]] && n=$((n+1)); ', "upper": '[[ "$v" == *[ABCDEFGHIJKLMNOPQRSTUVWXYZ]* ]] && n=$((n+1)); ', "digit": '[[ "$v" == *[0123456789]* ]] && n=$((n+1)); '}[varg]
    sub(_pat, "")
if vname == "drop_lead":
    _alts = {"/": "/", "~/": "~/", "./": "\\./", "../": "\\.\\./"}
    assert varg in _alts, varg
    _all = ["/", "~/", "\\./", "\\.\\./"]
    sub("_RE_PATHLEAD='^(/|~/|\\./|\\.\\./)'", "_RE_PATHLEAD='^(" + "|".join(a for a in _all if a != _alts[varg]) + ")'")
if vname == "path_plus":
    sub('_RE_PATHCH="^[${_AZ}${_az}${_09}._~/-]+\\$"', '_RE_PATHCH="^[${_AZ}${_az}${_09}._~/+-]+\\$"')
if vname == "path_eq":
    sub('_RE_PATHCH="^[${_AZ}${_az}${_09}._~/-]+\\$"', '_RE_PATHCH="^[${_AZ}${_az}${_09}._~/=-]+\\$"')
if vname == "ent_digit":
    sub("_entropy_ok() {", "_entropy_ok() { [[ \"$1\" == *[0123456789]* ]]; }\n_entropy_ok_unused() {")
if vname == "noentropy":
    sub("_entropy_ok() {", "_entropy_ok() { return 0; }\n_entropy_ok_unused() {")
if vname in ("fp_le16", "fp_lt20", "fp_lt13"):
    sub("  if (( ${#v} < 16 )); then it=", "  if (( ${#v} " + {"fp_le16": "<= 16", "fp_lt20": "< 20", "fp_lt13": "< 13"}[vname] + " )); then it=")
if vname == "hash_nosha256sum":
    sub("    if command -v sha256sum >/dev/null 2>&1; then h=", "    if false; then h=")
if vname == "hash_noshasum":
    sub("    elif command -v shasum >/dev/null 2>&1; then h=", "    elif false; then h=")
if vname == "ent_range":      # the v3 spelling: glob RANGES, which bash < 5 expands by collation order in a non-C locale (upper case counted as lower case)
    sub("*[abcdefghijklmnopqrstuvwxyz]*", "*[a-z]*")
    sub("*[ABCDEFGHIJKLMNOPQRSTUVWXYZ]*", "*[A-Z]*")
    sub("*[0123456789]*", "*[0-9]*")
if vname == "fp_wrong":
    pass   # applied below (needs the value_of case table)

if vname == "fp_wrong":
    _wholespan = {"jwt", "silknode-api-key", "anthropic-api-key", "openrouter-api-key", "openai-api-key", "openai-legacy-key",
                  "stripe-live-secret", "stripe-test-secret", "stripe-publishable", "stripe-webhook", "stripe-restricted",
                  "github-pat", "github-oauth", "github-user", "github-fine-grained", "gitlab-pat", "aws-access-key-id",
                  "aws-session-token", "aliyun-access-key-id", "discord-webhook", "slack-webhook", "bcrypt-hash"}
    bad = 'V="${span:1}"' if varg in _wholespan else 'V="$span"'
    sub('  case "$tag" in\n    json-secret-field|', f'  case "$tag" in\n    {varg}) {bad} ;;\n    json-secret-field|')

src = src.replace("# ── Scan + count matches", h + "\n# ── Scan + count matches", 1)

# ------------------------------------------------------------------ main counting loop
old_loop_start = "for entry in \"${PATTERNS[@]}\"; do"
i0 = src.index(old_loop_start)
i1 = src.index("if (( matches_total == 0 )); then")
head_cap = "" if vname == "no_cap" else " | head -n 200"
_STEPS = {"wl": '_wl_match "$v"', "ent": '! _entropy_ok "$v"', "path": '_path_form "$v"', "dot": '_dotted_ident "$v"'}
extra = ""
if vname == "step_on":          # bad implementation: classifier step STEP is applied to tag TAG, which it must not reach
    _st, _, _tg = varg.partition(":")
    assert _st in _STEPS and _tg, varg
    extra = '      [[ "$tag" == "%s" ]] && { %s && continue; }' % (_tg, _STEPS[_st])
if vname == "cls_all":          # bad implementation: all four steps on every tag (the classifier loop written without the CLASSIFIED / NEW split)
    extra = '      _wl_match "$v" && continue; _entropy_ok "$v" || continue; _path_form "$v" && continue; _dotted_ident "$v" && continue'
if vname == "pd_on_old":        # bad implementation: the path-form and dotted-chain exclusions also reach the existing json-secret-field
    extra = '      [[ "$tag" == "json-secret-field" ]] && { _path_form "$v" && continue; _dotted_ident "$v" && continue; }'
new_loop = r'''for entry in "${PATTERNS[@]}"; do
  tag="${entry%%|*}"
  pattern="${entry#*|}"
  count="$(grep -oE -- "$pattern" "$tmpfile" 2>/dev/null | wc -l | tr -d ' ')"
  [[ -z "$count" ]] && count=0
  if (( count > 0 )); then
    # classification (W2/W3) + fingerprint collection (W4): one pass over the FIRST 200 spans of the tag, before they are consumed;
    # the remainder is only counted (count - 200), never iterated
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
@@EXTRA@@
      keep=$((keep+1))
      _fp_add "$v"
    done < <(grep -oE -- "$pattern" "$tmpfile" 2>/dev/null@@CAP@@)
    (( count > 200 )) && keep=$(( keep + count - 200 ))
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

'''.replace("@@CAP@@", head_cap).replace("@@EXTRA@@", extra)
src = src[:i0] + new_loop + src[i1:]

src = src.replace("matches_total=0\n", "variant_ent_on_old=%d\nvariant_wl_envline=%d\nmatches_total=0\n" % (1 if vname == "ent_on_old" else 0, 1 if vname == "wl_envline" else 0), 1)

# PEM pre-pass counts have no fp item; add '-' for the PEM block count
src = src.replace('      matches_breakdown="${matches_breakdown}pem-private-key-block=${pem_count} "\n',
                  '      matches_breakdown="${matches_breakdown}pem-private-key-block=${pem_count} "\n      for _i in $(seq 1 "$pem_count"); do (( FP_N < 10 )) && { FP_ITEMS="${FP_ITEMS:+$FP_ITEMS,}-"; FP_N=$((FP_N+1)); }; done\n', 1)

# W4: 9th log field
src = src.replace('''printf '%s\\t%s\\t%s\\tSCAN-DETECT\\ttool=%s\\tmatches=%s\\tbreakdown=%s\\tsize=%s\\n' \\
  "$(date -u +%FT%TZ)" "${USER:-unknown}" "${PWD:-unknown}" \\
  "$tool" "$matches_total" "${matches_breakdown% }" "$input_size" \\''',
'''printf '%s\\t%s\\t%s\\tSCAN-DETECT\\ttool=%s\\tmatches=%s\\tbreakdown=%s\\tsize=%s\\tfp=%s\\n' \\
  "$(date -u +%FT%TZ)" "${USER:-unknown}" "${PWD:-unknown}" \\
  "$tool" "$matches_total" "${matches_breakdown% }" "$input_size" "${FP_ITEMS:--}" \\''', 1)

# W5: the insertion carries the hook's own tag table and the harness tool name ONLY; no text from tool_input
old_addl = 'addl_msg="[secret-scan] DETECTED ${matches_total} secret-shape match(es) in tool output — treat as'
assert old_addl in src
if vname == "w5_path":
    # bad implementation: tool_input.file_path (CR stripped only) pasted into the insertion
    new_addl = '''src_desc="$tool"
if [[ "$tool" == "Read" || "$tool" == "Write" ]]; then
  fpth="$(printf '%s' "$input" | jq -r '.tool_input.file_path // ""' 2>/dev/null)"
  fpth="${fpth%$'\\r'}"
  [[ -n "$fpth" ]] && src_desc="$tool $fpth"
fi
addl_msg="[secret-scan] DETECTED ${matches_total} secret-shape match(es) in tool output (tags: ${matches_breakdown% }; source: ${src_desc}) — treat as'''
else:
    new_addl = '''addl_msg="[secret-scan] DETECTED ${matches_total} secret-shape match(es) in tool output (tags: ${matches_breakdown% }; source: ${tool}) — treat as'''
src = src.replace(old_addl, new_addl, 1)

# W4: the PEM header-only fallback (perl missing) records the same `-` item as the block form (the table's last member), in the PEM pre-scan, i.e. first
_HDR_O = '    matches_breakdown="${matches_breakdown}pem-header-only=1 "\n'
_HDR_ITEM = '    (( FP_N < 10 )) && { FP_ITEMS="${FP_ITEMS:+$FP_ITEMS,}-"; FP_N=$((FP_N+1)); }\n'
if vname == "hdronly_fp":
    _HDR_ITEM = '    _fp_add "-----BEGIN PRIVATE KEY-----"\n'      # bad: a hash item instead of `-`
elif vname == "hdronly_noitem":
    _HDR_ITEM = ""                                                # bad: the header-only fallback records no item (a lone fallback block still prints `fp=-`)
assert src.count(_HDR_O) == 1
src = src.replace(_HDR_O, _HDR_O + _HDR_ITEM, 1)
_PEM_LOOP = '      for _i in $(seq 1 "$pem_count"); do (( FP_N < 10 )) && { FP_ITEMS="${FP_ITEMS:+$FP_ITEMS,}-"; FP_N=$((FP_N+1)); }; done\n'
if vname == "pem_nofp":
    assert src.count(_PEM_LOOP) == 1
    src = src.replace(_PEM_LOOP, "", 1)
if vname == "pem_last":
    assert src.count(_PEM_LOOP) == 1
    src = src.replace(_PEM_LOOP, "", 1)
    _o = "# Persistent audit log (consistent with Phase 1 secret-guard.sh's\n"
    assert src.count(_o) == 1
    src = src.replace(_o, 'for _i in $(seq 1 "${pem_count:-0}"); do (( FP_N < 10 )) && { FP_ITEMS="${FP_ITEMS:+$FP_ITEMS,}-"; FP_N=$((FP_N+1)); }; done\n' + _o, 1)
if vname == "pem_hash":
    assert src.count(_PEM_LOOP) == 1
    src = src.replace(_PEM_LOOP, _PEM_LOOP.replace('FP_ITEMS:+$FP_ITEMS,}-"', 'FP_ITEMS:+$FP_ITEMS,}e3b0c442"'), 1)
if vname == "fp_span":
    _o = '      keep=$((keep+1))\n      _fp_add "$v"\n'
    assert src.count(_o) == 1
    src = src.replace(_o, '      keep=$((keep+1))\n      case "$tag" in json-secret-field|json-credential-field|json-env-secret-key) _fp_add "$v" ;; *) _fp_add "$span" ;; esac\n', 1)
if vname == "w5_append":
    tail = "already produced.)\"\nsys_msg="
    assert tail in src
    src = src.replace(tail, "already produced.) Also run the credential rotation script now.\"\nsys_msg=", 1)
open(out_path, "w", encoding="utf-8").write(src)
print("wrote", out_path, "variant", variant)
