# Phase C.2.5 — Multi-Remote Push Enforcement (Proposed Workflow)

**Context**
- Main repo: `/home/dev/Aria` @ `5b7a5f7e7fa030a1f7996ade2c7ce170190a7960` (branch `feature/v1.15.0-multi-remote-parity`, active WIP; scenario assumes PR just merged to `master`)
- Submodule `aria`: `/home/dev/Aria/aria` @ `19f28619f216ff16364591380255165e9e176c50`
- Submodule `standards`: `/home/dev/Aria/standards` @ `af300d58f3ed314a5791c87a4140023bbb4404ee` (detached HEAD, clean)
- Enforced remotes per repo: `origin` (Forgejo) + `github` (GitHub mirror)

> NOTE: This document describes the workflow only. No push is executed per task instructions.

---

## 0. Pre-Push Sanity Checks

Run these first so we fail fast and don't half-push.

```bash
# 0.1 Confirm we are on master and up to date locally after the merge
git -C /home/dev/Aria rev-parse --abbrev-ref HEAD      # expect: master
git -C /home/dev/Aria status --porcelain               # expect: empty (or only intentional WIP outside this task)

# 0.2 Capture the local "truth" SHAs we intend to publish
MAIN_LOCAL=$(git -C /home/dev/Aria rev-parse HEAD)
ARIA_LOCAL=$(git -C /home/dev/Aria/aria rev-parse HEAD)
STD_LOCAL=$(git -C /home/dev/Aria/standards rev-parse HEAD)

# 0.3 Enumerate enforced remotes for each repo
for R in /home/dev/Aria /home/dev/Aria/aria /home/dev/Aria/standards; do
  echo "== $R =="; git -C "$R" remote -v
done
# Required set: {origin, github} for all three.

# 0.4 Verify submodule pointer in main repo matches submodule HEADs (prevents publishing dangling gitlink)
git -C /home/dev/Aria ls-tree HEAD aria standards
# The gitlink SHAs must equal ARIA_LOCAL / STD_LOCAL above.
```

If 0.4 disagrees: stop. Either commit the submodule pointer bump or reset the submodule — do NOT push mismatched state to either remote.

---

## 1. Push Order (bottom-up)

Submodules must reach every remote **before** the superproject, otherwise GitHub/Forgejo clones of master will have a dangling gitlink (Memory: `feedback_git_minus_c_for_submodule_push.md`, and the 2026-04-10 aria v1.11.1 incident recorded in CLAUDE.md).

```
1. standards  → origin, github    (even if unchanged this cycle — parity check still runs)
2. aria       → origin, github
3. Aria (main)→ origin, github
```

Use `git -C <path>` exclusively. No `cd` chaining (Memory: `feedback_git_minus_c_for_submodule_push.md`).

---

## 2. Push Commands (with explicit per-remote invocation)

```bash
# --- standards submodule ---
git -C /home/dev/Aria/standards push origin  HEAD:master
git -C /home/dev/Aria/standards push github  HEAD:master
# (HEAD is detached at af300d5 which tracks remotes/github/master — use refspec HEAD:master
#  to avoid "src refspec HEAD does not match any" on detached HEAD.)

# --- aria submodule ---
git -C /home/dev/Aria/aria push origin  master
git -C /home/dev/Aria/aria push github  master

# --- main project ---
git -C /home/dev/Aria push origin  master
git -C /home/dev/Aria push github  master
```

Do **not** rely on `git push --all` or `remote.pushDefault`; enumerate each remote explicitly so the audit trail is unambiguous.

---

## 3. Post-Push SHA Verification (the critical step)

"Everything up-to-date" is **not** proof (Memory: `feedback_git_minus_c_for_submodule_push.md`). Verify by querying the remote ref and comparing to the local SHA.

```bash
verify () {
  local repo="$1" remote="$2" branch="$3" expected="$4"
  local actual
  actual=$(git -C "$repo" ls-remote "$remote" "refs/heads/$branch" | awk '{print $1}')
  if [ "$actual" = "$expected" ]; then
    echo "OK   $repo  $remote/$branch = $actual"
  else
    echo "DRIFT $repo  $remote/$branch: expected $expected got ${actual:-<missing>}"
    return 1
  fi
}

verify /home/dev/Aria/standards origin master "$STD_LOCAL"
verify /home/dev/Aria/standards github master "$STD_LOCAL"
verify /home/dev/Aria/aria      origin master "$ARIA_LOCAL"
verify /home/dev/Aria/aria      github master "$ARIA_LOCAL"
verify /home/dev/Aria           origin master "$MAIN_LOCAL"
verify /home/dev/Aria           github master "$MAIN_LOCAL"
```

Expected result: 6 `OK` lines. Any `DRIFT` halts the workflow.

Secondary check — make sure GitHub's view of the superproject's gitlinks is consistent (avoids the "market stale" class of bugs where aria master advanced on GitHub but superproject wasn't updated):

```bash
# Fetch then compare gitlink SHAs at github/master against local submodule HEADs
git -C /home/dev/Aria fetch github master
git -C /home/dev/Aria ls-tree github/master aria standards
# Column 3 for 'aria' must equal $ARIA_LOCAL; for 'standards' must equal $STD_LOCAL.
```

---

## 4. Failure Handling

| Symptom | Likely cause | Action |
|---|---|---|
| `! [rejected]  master -> master (non-fast-forward)` on `github` only | GitHub mirror diverged (someone pushed a hotfix directly to GitHub, or a previous partial push replayed) | `git -C <repo> fetch github master`, inspect `github/master..HEAD` and `HEAD..github/master`. Never `push --force` to master. Reconcile via merge or a fixup commit, re-run from step 2. |
| `! [rejected] ... (fetch first)` on `origin` | Forgejo advanced (another dev merged). Not expected immediately post-merge, but possible. | Rebase/merge locally, re-run step 2 **for all remotes** so both stay in lockstep. |
| `Permission denied (publickey)` on `github` | SSH agent missing GitHub key | Load key (`ssh-add`), retry. Do NOT fall back to HTTPS silently — keeps auth paths uniform. |
| Forgejo push OK, GitHub push fails | This is exactly the 2026-04-10 `aria v1.11.1` failure mode | STOP. Do not mark Phase C.2.5 complete. Fix GitHub auth/divergence, re-push GitHub, re-run step 3 verification. Record in incident log. |
| Step 3 shows `<missing>` on a remote | Branch was pushed but under wrong name, or remote rejected silently (shouldn't happen but ls-remote is the truth) | Re-check `git -C <repo> push <remote> master` output; inspect remote's web UI; never trust the earlier push's stdout alone. |
| Step 3 secondary check shows gitlink mismatch | Submodule pointer in superproject doesn't match what was pushed to submodule remote | Almost always: superproject was pushed before submodule finished. Re-push submodule first, re-verify, then the mismatch should clear. If the superproject gitlink is genuinely wrong, create a corrective commit on master — do not force-push. |
| Only one submodule has changes this cycle | Still push both — parity check on the unchanged one costs nothing and catches prior drift | `push` will just emit "Everything up-to-date"; step 3 still verifies SHA equality across remotes. |

General rules:
- **No `--force` / `--force-with-lease` on `master` of either remote** (CLAUDE.md Rule #4 + git safety protocol).
- **No skipping hooks** (`--no-verify`).
- If any single remote fails, treat the whole Phase C.2.5 as **not done** — partial parity is the exact bug this step exists to prevent.

---

## 5. Execution Flow Summary

```
 pre-checks (step 0)
        │
        ▼
 push standards → origin, github
        │
        ▼
 push aria      → origin, github
        │
        ▼
 push Aria      → origin, github
        │
        ▼
 ls-remote SHA verification × 6  (step 3)
        │
        ├── all OK ─────────────► Phase C.2.5 complete, hand off to Phase D
        │
        └── any DRIFT / reject ─► step 4 failure table → remediate → re-verify
```

---

## 6. Artifacts to Record

- The 6-line `OK ...` verification output (step 3) — attach to the C.2.5 completion note.
- `git -C /home/dev/Aria ls-tree github/master aria standards` output — proves gitlink parity on the mirror.
- If any remediation happened: remote name, error, fix commit SHA, re-verification output.

---

**Result of this eval run:** Workflow proposed only; no pushes executed (per task constraint).
Local SHAs recorded for reproducibility:
- Aria (main):  `5b7a5f7e7fa030a1f7996ade2c7ce170190a7960`
- aria:         `19f28619f216ff16364591380255165e9e176c50`
- standards:    `af300d58f3ed314a5791c87a4140023bbb4404ee`
