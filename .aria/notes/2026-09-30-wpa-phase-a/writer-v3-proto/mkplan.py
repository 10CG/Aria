#!/usr/bin/env python3
"""mkplan.py OUTDIR -- write the mutation plans (TSV) for proto/mutbatch.py"""
import os
import sys

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
names = []
multi = [("auth", "token"), ("api", "token"), ("bearer", "token"), ("session", "token"), ("registration", "token"), ("jwt", "secret"),
         ("secret", "key"), ("api", "key"), ("access", "token"), ("refresh", "token"), ("client", "secret"), ("private", "key")]
for a, b in multi:
    names += [f"{a}_{b}", f"{a}{b.capitalize()}", f"{a.capitalize()}{b.capitalize()}", f"{a}{b}"]
for w in ["token", "sha1", "secret", "password", "passwd"]:
    names += [w, w.capitalize()]
names = sorted(set(names))
KW = ["SECRET", "PASSWORD", "PASSWD", "TOKEN", "API_KEY", "APIKEY", "PRIVATE_KEY", "WEBHOOK", "ENCRYPTION_KEY", "ACCESS_KEY"]
FLAGS = ["token", "password", "passwd", "secret", "api-key", "apikey", "access-key"]
READERS = "cat grep egrep fgrep rg head tail less more strings awk sed jq nl tac rev sort uniq cut paste diff cmp comm xxd od hexdump base64 column fold".split()
LAUNCH = "sudo doas nice timeout xargs nohup stdbuf env time eval setsid ionice unbuffer command exec".split()
PROC_OLD = "cat head tail less more strings hexdump od xxd tr awk perl rev".split()
PROC_NEW = "xargs sed grep rg cut paste nl sort base64 cp dd".split()
TAGS = ("jwt silknode-api-key anthropic-api-key openrouter-api-key openai-api-key openai-legacy-key stripe-live-secret stripe-test-secret stripe-publishable "
        "stripe-webhook stripe-restricted github-pat github-oauth github-user github-fine-grained gitlab-pat aws-access-key-id aws-session-token aliyun-access-key-id "
        "gcp-private-key-id discord-webhook slack-webhook postgres-url redis-url mongodb-url basic-auth-url bearer-token x-api-key-header env-line-secret-keyword "
        "json-secret-field bcrypt-hash json-credential-field json-env-secret-key kv-secret-assign auth-header-token cf-access-client-secret cli-secret-flag pem-private-key-block").split()


def w(fn, rows):
    with open(os.path.join(out, fn), "w") as f:
        for r in rows:
            f.write("\t".join(r) + "\n")


# ---- L3 whitelist (W3)
wl = ["wl_varname_lc", "wl_varname_uc", "wl_varname_any", "wl_cmdsub", "wl_dots_ascii", "wl_angle_prefix", "wl_angle_suffix", "wl_angle_loose", "wl_angle_noend",
      "wl_brace_prefix", "wl_brace_noend", "wl_tmpl_prefix", "wl_tmpl_suffix", "wl_tmpl_noend", "wl_red_prefix", "wl_red_anybracket", "wl_mask_prefix", "wl_mask_mixed",
      "wl_ell_contains", "wl_ell_prefix", "wl_prefix", "wl_contains", "wl_nocase", "wl_envline"]
rows = [(v, "l3", v, "SC-7,SC-11") for v in wl]
for c in ["angle", "brace", "tmpl", "tmpl_dollar", "red", "mask_star", "mask_x", "mask_X", "ellipsis", "marker_FAKE", "marker_PLACEHOLDER", "marker_NOT-REAL", "marker_NOT_REAL", "marker_NOTREAL", "marker_REDACTED"]:
    rows.append((f"wl_drop_{c}", "l3", f"wl_drop:{c}", "SC-7,SC-11"))
w("plan_l3_wl.tsv", rows)

# ---- L3 enumerations (W2) and classifier
rows = [(f"drop_name_{n}", "l3", f"drop_name:{n}", "SC-4", "4p") for n in names]
rows += [(f"drop_kwjson_{k}", "l3", f"drop_kwjson:{k}", "SC-4", "4l,4m,4s") for k in KW]
rows += [(f"drop_kwkv_{k}", "l3", f"drop_kwkv:{k}", "SC-5", "5a,5c,5d,5e,5f,5n") for k in KW]
rows += [(f"drop_flag_{s}", "l3", f"drop_flag:{s}", "SC-6", "6f,6g,6i") for s in FLAGS]
rows += [(f"drop_scheme_{s}", "l3", f"drop_scheme:{s}", "SC-6", "6a,6b,6e,6j") for s in ("token", "Token", "basic", "Basic")]
rows += [("hdr_case_sensitive", "l3", "hdr_case_sensitive", "SC-6", "6h,6j")]
for v in ("ent_digit", "ent_on_old", "noentropy", "noident", "nopath", "loosepath", "path_firstlower", "floor15", "floor17"):
    rows.append((v, "l3", v, "SC-4,SC-5,SC-6,SC-7,SC-9,SC-10,SC-11"))
rows += [(f"ent_drop_{c}", "l3", f"ent_drop:{c}", "SC-4,SC-10", "4a,4o,4t,10a,10b,10k") for c in ("lower", "upper", "digit")]
rows += [(f"drop_lead_{c}", "l3", f"drop_lead:{c}", "SC-9", "9w,9y") for c in ("/", "~/", "./", "../")]
rows += [("path_plus", "l3", "path_plus", "SC-4,SC-5", "4n,5l"), ("path_eq", "l3", "path_eq", "SC-4,SC-5", "4n,5l"), ("cli_dash2", "l3", "cli_dash2", "SC-6", "6i")]
rows += [(f"drop_vsym_kv_{s}", "l3", f"drop_vsym:kv:{s}", "SC-6", "6k") for s in ("+", "/", "=", ".", "_", "~", "-")]
rows += [(f"drop_vsym_hdr_{s}", "l3", f"drop_vsym:hdr:{s}", "SC-6", "6k") for s in (".", "_", "/", "+", "=", "-")]
w("plan_l3_enum.tsv", rows)

# ---- L3 W4 / W5
rows = [("fp_span", "l3", "fp_span", "SC-12", "12g,12h,12i,12j,12k"), ("hdronly_fp", "l3", "hdronly_fp", "SC-12", "12l")]
rows += [(f"fp_wrong_{t}", "l3", f"fp_wrong:{t}", "SC-12", "12a,12g,12h,12i,12j,12k") for t in TAGS]
rows += [("w5_append", "l3", "w5_append", "SC-13"), ("w5_path", "l3", "w5_path", "SC-13")]
w("plan_l3_w4w5.tsv", rows)

# ---- L1 W8 / W9 / W10 / old
rows = [(f"drop_reader_{r}", "l1", f"drop_reader:{r}", "SC-16,SC-19", "16q,19u") for r in READERS]
rows += [(f"drop_extreader_{r}", "l1", f"drop_extreader:{r}", "SC-19", "19u") for r in READERS]
for i in ("python3", "node"):
    rows.append((f"drop_interp_{i}", "l1", f"drop_interp:{i}", "SC-16,SC-19,SC-22", "16h,16n,16o,19o,19u,22bg"))
for v in ("ext_max199", "ext_max201", "ext_size32767", "ext_size32769", "ext_minlen3", "ext_minlen5", "ext_maxlen199", "ext_maxlen201", "ext_nosym", "ext_occ63", "ext_occ65",
          "ext_bare", "ext_first", "ext_regex", "ext_trunc"):
    rows.append((v, "l1", v, "SC-19,SC-20"))
for v in ("vx_assign15", "vx_assign17", "vx_repl7", "vx_repl9", "vx_noquote", "vx_interleave", "vx_start_only"):
    rows.append((v, "l1", v, "SC-21"))
rows += [(f"drop_assign_{a}", "l1", f"drop_assign:{a}", "SC-21", "21j") for a in ("export", "declare", "local", "readonly", "typeset")]
rows += [("read_noboundary", "l1", "read_noboundary", "SC-18", "18a,18b,18d,18h,18i"), ("notight", "l1", "notight", "SC-16", "16f,16p"),
         ("jq_loose", "l1", "jq_loose", "SC-24"), ("env_boundary", "l1", "env_boundary", "SC-23")]
rows += [(f"drop_w12_{i}", "l1", f"drop_w12:{i}", "SC-23", "23a,23b") for i in range(4)]
w("plan_l1_w8w9w10.tsv", rows)

# ---- L1 W11
rows = [(f"drop_launch_{x}", "l1", f"drop_launch:{x}", "SC-22", "22n,22x,22y,22z,22aw,22ax") for x in LAUNCH]
rows += [(f"drop_procreader_{x}", "l1", f"drop_procreader:{x}", "SC-22", "22F,22G,22H,22I,22J,22aj,22an,22bc,22bd,22be") for x in PROC_OLD + PROC_NEW]
rows += [(f"drop_remote_{x}", "l1", f"drop_remote:{x}", "SC-22", "22v,22z,22A,22B,22C,22D,22E,22ao,22ap,22aq,22ar,22bk") for x in ("ssh", "docker", "kubectl", "nomad", "pct", "lxc", "podman", "sh", "watch")]
rows += [(f"drop_psalt_{i}", "l1", f"drop_psalt:{i}", "SC-22") for i in range(1, 8)]
rows += [(f"drop_pid_{i}", "l1", f"drop_pid:{i}", "SC-22", "22F,22G,22H,22I,22an,22bd,22be,22bg,22bf") for i in range(6)]
rows += [(f"drop_kwpos_{x}", "l1", f"drop_kwpos:{x}", "SC-22", "22az") for x in ("then", "do", "else", "elif")]
rows += [(f"drop_pgrep_{i}", "l1", f"drop_pgrep:{i}", "SC-22", "22bl,22k,22l,22m") for i in (0, 1)]
rows += [(f"drop_pstree_{i}", "l1", f"drop_pstree:{i}", "SC-22", "22bl") for i in (0, 1)]
rows += [(f"drop_dockerform_{x}", "l1", f"drop_dockerform:{x}", "SC-22", "22bl,22bb") for x in ("top", "notrunc", "compose", "container", "ls")]
for v in ("drop_bin", "drop_larg", "drop_procinterp", "nodocker_podman", "pidtok_any", "proc_status", "anchor_nocntrl", "launcher_any"):
    rows.append((v, "l1", v, "SC-22"))
w("plan_l1_w11.tsv", rows)
for f in sorted(os.listdir(out)):
    print(f, sum(1 for _ in open(os.path.join(out, f))))
