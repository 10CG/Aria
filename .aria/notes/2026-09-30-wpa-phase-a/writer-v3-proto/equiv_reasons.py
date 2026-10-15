# -*- coding: utf-8 -*-
# Reasons for bad implementations that turned NO probe row red (equivalent mutants), keyed by plan label; a trailing `*` matches a label prefix.
# SUPERSEDED: first-pass results that are stale because the variant or the probe was fixed afterwards; the replacing run is named.
_LOWER8 = ("The mutated program behaves exactly like the correct one: this lower-case snake spelling is also a key of the EXISTING tag json-secret-field, which sits earlier in "
           "PATTERNS and consumes the span first, so its membership in the NEW json-credential-field name table is not observable (W2 says so; row 4p expects "
           "json-secret-field=1 for these 8 spellings). The table keeps the 8 names only so that a later narrowing of the existing tag does not lose the detection.")
EQUIV = {
    "drop_name_access_token": _LOWER8, "drop_name_api_key": _LOWER8, "drop_name_client_secret": _LOWER8, "drop_name_passwd": _LOWER8,
    "drop_name_password": _LOWER8, "drop_name_private_key": _LOWER8, "drop_name_refresh_token": _LOWER8, "drop_name_secret": _LOWER8,
    "drop_assign_*": ("Declaration prefix word (export / declare / local / readonly / typeset): the prototype recognises `NAME=value` after any whitespace or separator, "
                      "so the prefix word is redundant and dropping it from the list changes the verdict of no input (W10 says so; 21j checks that every declaration form is still collected)."),
}
SUPERSEDED = {
    "plan_l3_wl/wl_cmdsub": "first pass ran a broken draft of the variant (the hook failed to parse, 15 unrelated rows red); re-run in plan_extra with the fixed variant: 7h dollar-cmd and 11z dollar-cmd red.",
    "plan_l3_w4w5/fp_wrong_pem-private-key-block": "the variant edited an unreachable case-table entry (the PEM block's fp item `-` does not go through the value-body table), i.e. it was a no-op; replaced by the real PEM bad implementations pem_nofp and pem_hash in plan_extra.",
    "plan_l3_enum/path_eq": "first pass ran before the padded-value generator of rows 4n / 5l was made to exclude '+' (a random '+' rescued the loose class about half of the time, so the row was only probabilistic); re-run as path_eq__r2 in plan_repeat and 10 times by hand: 4n and 5l red 10/10.",
    "plan_l3_enum/path_plus": "re-run after the generator fix, see path_plus__r2 in plan_repeat (4n and 5l red 10/10 by hand).",
    "plan_l3_enum/loosepath": "re-run after the generator fix, see loosepath__r2 in plan_repeat (4n and 5l red 10/10 by hand).",
}
SUPERSEDED.update({
    "plan_l3_enum/drop_vsym_*": "work-directory name collision in the first pass and in the repeat pass: the sanitised labels of the symbols `+ / = _ ~` (kv) and `+ / = _` (hdr) coincide, so concurrent jobs clobbered each other's tree; re-run as vsym_<group>_<symbol> in plan_vsym with unique names (mutbatch.py now appends a hash to every sanitised name).",
    "plan_extra/pem_nofp": "run against row 12k only: a PEM block alone prints `fp=-` both with the item and with no item at all (the log writes `${FP_ITEMS:--}`), so 12k cannot see the difference; replaced by pem_nofp_12m in plan_extra2 after row 12m (PEM block after a kv credential) was added.",
    "plan_extra/pem_hash": "run against row 12k only; replaced by pem_hash_12m in plan_extra2 (12k and 12m).",
    "plan_extra_b32/b4": "run with WPA_ONLY=SC-32 only: 32c compares the hook-direct rows that ran in the same process, and none had run; replaced by b4_32c in plan_extra2_b32 (SC-16 + SC-32).",
    "plan_extra_b32/vx_patsub": "run with WPA_ONLY=SC-32 only (no hook-direct rows to compare); replaced by vx_patsub_32c in plan_extra2_b32 (SC-21 + SC-32).",
})
SUPERSEDED["plan_extra/noentropy_sc33"] = ("mutbatch builds each bad implementation as a tree that holds only aria/hooks (no skills/ documents), so the SC-33 census had no corpus and the row could not turn red; "
                                "re-run by hand on a FULL copy of the target tree with the noentropy hook (see manual_runs.txt): 33a red, flagged=7, 5 files outside the attribution list.")
EQUIV["interp_name_v1var"] = ("The Nomad-variable path name in the rewritten python3 -c / node -e rows duplicates an earlier GENERAL row of the baseline list that blocks any command mentioning that path: the target, "
                              "the variant without the copy and the baseline all exit 2 for the python3 -c, node -e and cat forms (work/cases_v1var.py), so dropping the copy changes no verdict "
                              "(16o still carries both cases; the other six names are not duplicated and each turns 16o red).")
SUPERSEDED["plan_repeat/drop_vsym_*"] = SUPERSEDED["plan_l3_enum/drop_vsym_*"]
