#!/usr/bin/env python3
"""mkplan_v4.py -- write the v4 mutation plans (work/plans/plan_v4_*.tsv).  Every line = one bad implementation and the probe rows that must turn red.
line format: label <TAB> kind(l3|l1) <TAB> variant <TAB> SC list (WPA_ONLY) <TAB> rows (WPA_ROWS)"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plans")
os.makedirs(OUT, exist_ok=True)


def w(name, lines):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        for l in lines:
            fh.write("\t".join(l) + "\n")
    print(name, len(lines))


# ---------------------------------------------------------------- L3
l3 = []
l3.append(("nul_off", "l3", "nul_off", "SC-1", "1c,1d"))
l3.append(("drop_extract_content", "l3", "drop_extract:tool_result.content", "SC-2", "2e"))
l3.append(("drop_extract_output", "l3", "drop_extract:tool_result.output", "SC-2", "2f"))
l3.append(("oldkey_webhook_secret", "l3", "oldkey_drop:webhook_secret", "SC-7", "7k"))
l3.append(("oldkey_encryption_key", "l3", "oldkey_drop:encryption_key", "SC-7", "7k"))
EX_TAGS = ["env-line-secret-keyword", "bearer-token", "x-api-key-header", "postgres-url", "redis-url", "mongodb-url", "basic-auth-url"]
for t in EX_TAGS:
    for st in ("ent", "path", "dot"):
        l3.append((f"step_{st}_on_{t}", "l3", f"step_on:{st}:{t}", "SC-7", "7l"))
for st in ("path", "dot"):
    l3.append((f"step_{st}_on_json-secret-field", "l3", f"step_on:{st}:json-secret-field", "SC-7", "7l"))
l3.append(("step_dot_on_jwt", "l3", "step_on:dot:jwt", "SC-7", "7l"))
for t in EX_TAGS[1:]:
    l3.append((f"step_wl_on_{t}", "l3", f"step_on:wl:{t}", "SC-7", "7m"))
l3.append(("cls_all", "l3", "cls_all", "SC-7", "7l,7m,7h"))
l3.append(("pd_on_old", "l3", "pd_on_old", "SC-7", "7l"))
for v in ("fp_le16", "fp_lt20", "fp_lt13"):
    l3.append((v, "l3", v, "SC-12", "12n"))
l3.append(("hash_nosha256sum", "l3", "hash_nosha256sum", "SC-12", "12o,12a,12c"))
l3.append(("hash_noshasum", "l3", "hash_noshasum", "SC-12", "12o,12a,12c"))
l3.append(("val_eval", "l3", "val_eval", "SC-7", "7n"))      # L3 no-execution invariant (7n): the value helper strips quotes with eval
w("plan_v4_l3.tsv", l3)

# ---------------------------------------------------------------- L1: W9 / W10 / W12 invariants and the extension fixes
READERS_FOR_STAGE = []
l1a = []
l1a.append(("ext_nomask", "l1", "ext_nomask", "SC-19", "19z,19aa"))
for k in ("semi", "amp", "pipe", "nl"):
    l1a.append((f"ext_mask_no{k}", "l1", f"ext_mask_no{k}", "SC-19", "19z,19aa"))
l1a.append(("ext_mask_all", "l1", "ext_mask_all", "SC-19", "19z,19aa"))
l1a.append(("ext_nostrip", "l1", "ext_nostrip", "SC-19", "19ac"))
l1a.append(("ext_emptypat", "l1", "ext_emptypat", "SC-19,SC-20", "20o,20p,20q,19l,19w"))
l1a.append(("ext_eval", "l1", "ext_eval", "SC-19", "19ab,19j,19k"))
l1a.append(("ext_glob", "l1", "ext_glob", "SC-19", "19ab,19j,19k"))
l1a.append(("vx_eval", "l1", "vx_eval", "SC-21", "21z"))
l1a.append(("w12_eval", "l1", "w12_eval", "SC-23", "23i"))
w("plan_v4_l1_w9w10w12.tsv", l1a)

# ---------------------------------------------------------------- L1: W11 / W8 (tight copy drift, wrappers, pid tokens)
LAUNCH = "sudo doas nice timeout xargs nohup stdbuf env time eval setsid ionice unbuffer command exec".split()
REMOTE = "ssh docker kubectl nomad pct lxc podman sh watch".split()
l1b = []
for p in ("PROCTAB", "REMOTE", "DOCKER"):
    l1b.append((f"tight_without_{p}", "l1", f"tight_without:{p}", "SC-22", "22bm"))
for x in LAUNCH:
    l1b.append((f"tdrop_launch_{x}", "l1", f"tdrop_launch:{x}", "SC-22", "22bm"))
for x in REMOTE:
    l1b.append((f"tdrop_remote_{x}", "l1", f"tdrop_remote:{x}", "SC-22", "22bm"))
for n in range(1, 8):
    l1b.append((f"tdrop_psalt_{n}", "l1", f"tdrop_psalt:{n}", "SC-22", "22bm"))
l1b.append(("tight_plainps", "l1", "tight_plainps", "SC-22", "22bm"))
l1b.append(("notight_proc", "l1", "notight_proc", "SC-22", "22bm"))
l1b.append(("proc_nocredit", "l1", "proc_nocredit", "SC-22", "22bn,22Y"))
l1b.append(("tight_ini_literal", "l1", "tight_ini_literal", "SC-16", "16r"))
l1b.append(("notight_ini", "l1", "notight_ini", "SC-16", "16r,16f"))
l1b.append(("launcher_ps_only", "l1", "launcher_ps_only", "SC-22", "22bq"))
for x in REMOTE:
    l1b.append((f"remote_env_split_{x}", "l1", f"remote_env_split:{x}", "SC-22", "22bo"))
for n in (2, 6, 7):
    l1b.append((f"drop_pid_{n}", "l1", f"drop_pid:{n}", "SC-22", "22bp,22be"))
l1b.append(("pidtok_placeholders", "l1", "pidtok_placeholders", "SC-22", "22bf"))
l1b.append(("drop_dockerform_ctop", "l1", "drop_dockerform:ctop", "SC-22", "22bl"))
l1b.append(("proc_tight", "l1", "proc_tight", "SC-22", "22bh"))
l1b.append(("remote_anchored", "l1", "remote_anchored", "SC-22", "22bj,22bk"))
l1b.append(("anchor_nocntrl_bj", "l1", "anchor_nocntrl", "SC-22", "22bj"))
w("plan_v4_l1_w11w8.tsv", l1b)

# ---------------------------------------------------------------- bash 3.2 + second locale (SC-32 32d): needs --b32
b32 = [("ent_range_32d", "l3", "ent_range", "SC-4,SC-9,SC-10,SC-32", "")]
w("plan_v4_b32.tsv", b32)

# ---------------------------------------------------------------- W9 byte semantics (19ad / 19ae): a character-counting and a Unicode-class bad implementation
w("plan_v4_l1_charsem.tsv", [("ext_charlen", "l1", "ext_charlen", "SC-19", "19ad,19ae"), ("ext_uniclass", "l1", "ext_uniclass", "SC-19", "19ad,19ae")])
