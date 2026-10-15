# -*- coding: utf-8 -*-
# Reasons for bad implementations that turned NO probe row red (equivalent mutants), keyed by plan label; a trailing `*` matches a label prefix.
# (v3 reasons are kept: the previous round's bad implementations are re-run on the v4 prototype; v4 adds the env-dump wrappers.)
_LOWER8 = ("The mutated program behaves exactly like the correct one: this lower-case snake spelling is also a key of the EXISTING tag json-secret-field, which sits earlier in "
           "PATTERNS and consumes the span first, so its membership in the NEW json-credential-field name table is not observable (W2 says so; row 4p expects "
           "json-secret-field=1 for these 8 spellings). The table keeps the 8 names only so that a later narrowing of the existing tag does not lose the detection.")
_ENVWRAP = ("The mutated program behaves exactly like the correct one: the baseline already has its own, older rules that block `<this wrapper> ... env` / `... printenv` "
            "(docker / kubectl / podman / lxc exec, secret-guard.sh baseline env-dump rows), so removing the wrapper from the NEW env-dump alternation changes the verdict of no input "
            "(row 22bo exits 2 for it either way). The member is kept in the alternation only so that the wrapper set is one list; the wrappers whose removal IS observable "
            "(ssh, sh -c / bash -c, watch, nomad alloc exec, pct exec) are the ones the baseline misses, and each turns 22bo red.")
EQUIV = {
    "drop_name_access_token": _LOWER8, "drop_name_api_key": _LOWER8, "drop_name_client_secret": _LOWER8, "drop_name_passwd": _LOWER8,
    "drop_name_password": _LOWER8, "drop_name_private_key": _LOWER8, "drop_name_refresh_token": _LOWER8, "drop_name_secret": _LOWER8,
    "drop_assign_*": ("Declaration prefix word (export / declare / local / readonly / typeset): the prototype recognises `NAME=value` after any whitespace or separator, "
                      "so the prefix word is redundant and dropping it from the list changes the verdict of no input (W10 says so; 21j checks that every declaration form is still collected)."),
    "interp_name_v1var": ("The Nomad-variable path name in the rewritten python3 -c / node -e rows duplicates an earlier GENERAL row of the baseline list that blocks any command mentioning that path: the target, "
                          "the variant without the copy and the baseline all exit 2 for the python3 -c, node -e and cat forms (work/cases_v1var.py), so dropping the copy changes no verdict "
                          "(16o still carries both cases; the other six names are not duplicated and each turns 16o red)."),
    "remote_env_split_docker": _ENVWRAP, "remote_env_split_kubectl": _ENVWRAP, "remote_env_split_podman": _ENVWRAP, "remote_env_split_lxc": _ENVWRAP,
}
SUPERSEDED = {}
