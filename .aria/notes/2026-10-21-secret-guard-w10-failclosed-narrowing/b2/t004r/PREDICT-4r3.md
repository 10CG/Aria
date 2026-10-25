# 4r third attempt: expectations written before reading any result (2026-10-25 ~10:07 UTC; W8 file already produced, not yet read)
W8  : proto(9f61db0e7b8b)->impl(628652570ce3) = 5 kinds only: (1) What 1 supplement (_sg_relax_ok / _sg_relax_platform), (2) What 6 (the :666 continue line deleted),
      (3) What 7 supplement (4 comments), (4) What 1 supplement 2 (WSL line of _sg_relax_ok rewritten, one line after _sg_relax_left, new _sg_relax_nowslfs),
      (5) What 7 supplement 2 (review comments, verbatim text back-filled in the proposal). Every added line found verbatim in its What section; nothing else.
      prev impl(af4658b6f935, aria 2893bcc)->impl: only kinds (4) and (5).
W11 : 18 outcome lines; rc and text kind per shape identical to prev and to 95cf1de7; only header and wall differ.
W9  : exactly 21ab 21ac 21ag 21aj 21al 21ao change; per-check lists identical to prev (11 checks in 21ab); vs 95cf1de7 only the 3 SC-21ab checks (load).
W13 : sec1 FAIL 0 on 5 bashes; per-bash totals = prev + 10 (V15-W1f..W1o: PASS, or SKIP [platform] where the platform cannot host them, e.g. no private mount ns);
      sec2 baseline red set = prev, plus the 10 new ids (on the baseline: MISSING/FAIL expected for the direct-call ones); sec3 every BI CAUGHT, P-0 GREEN, every P-* CAUGHT;
      other-red lists = prev for old ids (new ids may add to them).
P-0 : v31 mode GREEN, suite mode GREEN, timing batch judged.
Msuite: every BI / P verdict identical to prev (CAUGHT / GREEN).
W12 : 138 outcomes, rc+kind per n identical to prev: allow 136, growth 1 (n=1053), VMAX 1 blocked, 1 not entering the rerun identical to the baseline;
      over-bound 0/138; 1b close to prev (p50 0.272, p90 0.638, max 1.771 s) within a few ms..tens of ms; fallback-to-baseline 0; sec2 300/300; sec3 40/40.
W14i: 31 mutants: 26 caught as predicted + 5 caught by the added case; verdicts identical to prev.
W14m: 0 over the bound; readings of the same order as prev.
