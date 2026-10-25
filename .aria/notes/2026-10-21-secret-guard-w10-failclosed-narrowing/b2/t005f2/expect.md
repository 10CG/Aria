# t005f2 runs: expectations written before the runs (2026-10-25; reasons in brackets)
1. W10-only (SG_W10_ONLY=.), SC_BASH = bash 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20: PASS 150/150, FAIL 0, SKIP 0, timing batch judged [5f had 149; +1 = V11-S1-above-gate:_sg_relax_nowslfs]. bash 3.2.57: FAIL 0, PASS 83, SKIP 67 all [platform], timing batch judged [5f 82/67; the new static case runs in every mode].
2. Full round, bash on PATH: PASS 975/975, FAIL 0, SKIP 0, SC-13 PASS (header now 981 (975)), timing batch judged.
3. Full round with WSL_DISTRO_NAME=Ubuntu exported: FAIL 0, total 975, SKIP only [void] (5f: 29), the 6 groups print "baseline branch" [wpa_rx6 requires empty WSL variables]; the ported cases still run relax [they clear the WSL variables by design, R2 PP2-m14].
4. sc-cases.sh on the implementation, BASE = 59e333c: PASS 151, FAIL / MISSING / SETUP / SKIP 0, V0-H2 "all 149 expected case ids of mode relax reported once" [5f 150 / 148, +1 static id], timing batch judged.
5. run-mutants.sh, v31 mode and suite mode: 63 CAUGHT each, P-0 GREEN (if P-0 is NOT-JUDGED for load: rerun alone at load < 1.2, GREEN), no perturbation worse than predicted [the hook change is one comment line; the static list only adds a case].
6. impl/w14.sh (W14_DIR / W14_OUT under runs/): 31 caught = as predicted 26 + by the added case 5, NOT CAUGHT 0, not judged 0 [IMPL_SHA12 = 834dee6db0d0].
expectation (written before the run): mut-v31 P-0 alone at load < 1.2 -> GREEN, 0 not as expected [first run judged GREEN but its step ended at load 2.22, INV-7]
