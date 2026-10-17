#!/usr/bin/env python3
"""mkplans6.py -- write this round's mutation plans (work/plans6/*.tsv).  Plan line: label <TAB> kind (l3|l1|hj) <TAB> variant <TAB> SC list (WPA_ONLY) <TAB> rows (WPA_ROWS, optional).

Every NEW or CHANGED probe row of this round has at least one bad implementation here that is meant to turn it red; the campaign records which rows really do.
The earlier rounds' plans (plans_v5 / plans_v4 / plans_v3) are copied unchanged from the previous round's archive and re-run as a regression.
Rule #7: no credential-shaped literal in this file."""
import os

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(EXP, "work", "plans6")
os.makedirs(D, exist_ok=True)


def write(name, rows):
    with open(os.path.join(D, name + ".tsv"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write("\t".join(r) + "\n")


# ---- L3 (secret-scan.sh): the failure event (cluster X), the value-extraction code (cluster W), the fingerprint order (12p), the left-boundary known limit (9z)
F35 = "35a,35b,35c,35e"
l3 = [
    ("fail_noextract", "l3", "fail_noextract", "SC-35", F35),
    ("fail_noclassify", "l3", "fail_noclassify", "SC-35", F35),
    ("string_response", "l3", "string_response", "SC-3", "3a,3b"),
    ("fail_event_name", "l3", "fail_event_name", "SC-35", F35),
    ("fail_event_always", "l3", "fail_event_always", "SC-35", F35),
    ("fail_event_substr", "l3", "fail_event_substr", "SC-35", F35),
    ("fp_all_spans", "l3", "fp_all_spans", "SC-12", "12a,12b,12c,12g,12h,12i,12j,12p"),
    ("kv_left_boundary_off", "l3", "kv_left_boundary_off", "SC-9", "9z"),
    ("val_quadratic", "l3", "val_quadratic", "SC-34", "34a,34b"),
    ("val_far_delim", "l3", "val_far_delim", "SC-34", "34a,34b"),
    ("val_quote_strip", "l3", "val_quote_strip", "SC-34", "34a,34b"),
    ("val_kv_blank", "l3", "val_kv_blank", "SC-34", "34a,34b"),
    ("val_json_colon", "l3", "val_json_colon", "SC-34", "34a,34b"),
    ("val_url_at", "l3", "val_url_at", "SC-34", "34a,34b"),
    ("val_envline_eq", "l3", "val_envline_eq", "SC-34", "34a,34b"),
]
write("plan_v6_l3", l3)

# ---- hooks.json (cluster X): the single extra registration
HJ = "35d,31d,31e"
hj = [(v, "hj", v, "SC-35,SC-31", HJ) for v in ("hooks_nofail", "hooks_wrong_matcher", "hooks_two_entries", "hooks_other_hook", "hooks_touch_other", "hooks_gate_literal")]
write("plan_v6_hj", hj)

# ---- L1 (secret-guard.sh)
l1 = [
    # Y: the SC-8 / SC-9a assembly
    ("core_below_gate", "l1", "core_below_gate", "SC-30", "30b"),
    # Z: printenv with a name behind a wrapper, spelling positions, the env wrappers of the dump family
    ("printenv_bare_only", "l1", "printenv_bare_only", "SC-22", "22bx,22bo,22bw,22by"),
    ("docker_notrunc_first", "l1", "docker_notrunc_first", "SC-22", "22bu"),
    ("launcher_dur_s", "l1", "launcher_dur_s", "SC-22", "22bu"),
]
for v, rows in (("pgrep_afirst", "22bu"), ("pgrep_firstonly", "22bu"), ("pstree_afirst", "22bu"), ("pstree_firstonly", "22bu"), ("ps_o_end", "22bv"), ("ps_f_first", "22bu"),
                ("ps_F_lower", "22bu"), ("ps_operand_first", "22bu,22bv")):
    l1.append((v, "l1", v, "SC-22", rows))
# AA: the command-position character set of the process-table rows, member by member
for m in ("amp", "brace", "backtick", "semi", "pipe", "paren_open", "paren_close"):
    l1.append((f"anchor_drop_{m}", "l1", f"anchor_drop:{m}", "SC-22", "22bt"))
# Z: the eleven-wrapper env / printenv family: each wrapper missing from the dump alternative
for w in ("ssh", "docker", "kubectl", "nomad", "pct", "lxc", "podman", "sh", "watch"):          # `sh` stands for the `sh|bash -c` wrapper pair
    l1.append((f"remote_env_split_{w}", "l1", f"remote_env_split:{w}", "SC-22", "22bo,22bw,22by,22br,22bs"))
# Z: the baseline spellings of the five baseline wrappers (22bw) -- a rewrite that folds the baseline rows into the shared alternation and loses the plain blank-separated spelling
l1.append(("envrows_replaced", "l1", "envrows_replaced", "SC-22", "22bw,22bo,22by"))
# AB: the extension file edge cases
l1 += [("ext_nonl", "l1", "ext_nonl", "SC-19", "19an"), ("ext_unquoted", "l1", "ext_unquoted", "SC-19", "19ao"), ("ext_unsetonly", "l1", "ext_unsetonly", "SC-19", "19ap")]
# cr/m3: the BLOCKED text of an extension hit
l1.append(("ext_echo_subst", "l1", "ext_echo_subst", "SC-25", "25i"))
# 17d: a known limit closed by one more print reader
for rd in ("expand", "unexpand", "shuf", "split", "csplit"):
    l1.append((f"add_reader_{rd}", "l1", f"add_reader:{rd}", "SC-17", "17d"))
write("plan_v6_l1", l1)
print("plans6 written:", {n: sum(1 for _ in open(os.path.join(D, n))) for n in sorted(os.listdir(D))})
