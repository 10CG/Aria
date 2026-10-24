| 编号 | v31 判定 (mut-summary) | 套件首跑判定 | 首跑计时批 (起始一分钟负载) | 低负载重跑 (计时批, 起始负载) | 指定用例 = 套件首跑状态 (\* = 走关门臂) | 与 v31 |
|---|---|---|---|---|---|---|
| BI-1 | CAUGHT | CAUGHT | judged (1.07) | — | `V4-S6-spoofed-tail-0`=red | 同 |
| BI-2 | CAUGHT | CAUGHT | judged (1.07) | — | `V5-S5-pipe-holder`=red `V6-E2-deadline-fallback-bytes`\*=red | 同 |
| BI-3 | CAUGHT | CAUGHT | judged (0.99) | — | `V5-S10c-dead-timer-no-judgement`=red `V5-S10d-no-judgement-with-dead-timer`=red | 同 |
| BI-4 | CAUGHT | CAUGHT | judged (0.99) | — | `V6-E2-deadline-fallback-bytes`\*=red | 同 |
| BI-5 | CAUGHT | CAUGHT | judged (0.99) | — | `V2-G4-extension-file-with-entry`=red `V2-E9-extension-project`\*=red | 同 |
| BI-6 | CAUGHT | CAUGHT | judged (0.99) | — | `V2-G3-gate-calls-platform`=red `V2-G3b-gate-uses-build-facts`=red `V2-E8-ostype-from-environment-ignored`\*=red | 同 |
| BI-7 | CAUGHT | CAUGHT | judged (0.99) | — | `V6-E2-deadline-fallback-bytes`\*=red | 同 |
| BI-8 | CAUGHT | CAUGHT | judged (1.07) | — | `V9-E12-vmax-unchanged`\*=red[reference] | 判定同；原因由 [reference] 认定 |
| BI-9 | CAUGHT | CAUGHT | judged (1.07) | — | `V8-D3-growth-8193-plain`=red `V8-D3-growth-8193-braced`=red | 同 |
| BI-10 | CAUGHT | CAUGHT | judged (1.07) | — | `V7-E14-long-line-from-expansion`\*=red | 同 |
| BI-11 | CAUGHT | CAUGHT | judged (1.15) | — | `V10-N3-environ-big-judge`=red `V11-S4-one-rule-loop`=red | 同 |
| BI-12 | CAUGHT | CAUGHT | judged (1.15) | — | `V7-N5-read-big-judge-short-lines`=red `V7-E13-multiline-copy-normal-text`\*=red | 同 |
| BI-13 | CAUGHT | CAUGHT | judged (1.15) | — | `V3-E3-anchor-at-hook-start`\*=red | 同 |
| BI-14 | CAUGHT | CAUGHT | judged (1.05) | — | `V3-G10-cap-3`=red `V3-E4-cap-3-at-budget-4`\*=red | 同 |
| BI-15 | CAUGHT | CAUGHT | judged (0.97) | — | `V5-S9-child-left-behind`=red `V5-S13b-nothing-outlives-the-run`=red | 同 |
| BI-16 | CAUGHT | CAUGHT | judged (1.05) | — | `V2-G11-flag-not-from-environment`=red `V2-E6-flag-from-environment-ignored`\*=red | 同 |
| BI-17 | CAUGHT | CAUGHT | judged (1.05) | — | `V9-C1-assignments-rerun`=red `V9-C2-references-rerun-c12`=red `V9-E10-count-axis-read-blocked`\*=red | 同 |
| BI-17a | CAUGHT | CAUGHT | judged (1.21) | — | `V9-C1-assignments-rerun`=red | 同 |
| BI-17b | CAUGHT | CAUGHT | judged (1.21) | — | `V9-C3-for-statements-rerun`=red | 同 |
| BI-17c | CAUGHT | CAUGHT | judged (1.21) | — | `V9-C2-references-rerun-c12`=red `V9-C2-references-rerun-cb12`=red | 同 |
| BI-18 | CAUGHT | CAUGHT | judged (1.21) | — | `V9-E11-tmax-in-rerun`\*=red | 同 |
| BI-19 | CAUGHT | CAUGHT | judged (1.27) | — | `V4-S11-bare-zero`=red | 同 |
| BI-20 | CAUGHT | CAUGHT | judged (1.27) | — | `V2-G4-empty-extension-file`=red | 同 |
| BI-21 | CAUGHT | CAUGHT | judged (1.27) | — | `V3-G9-clock-backwards`=red | 同 |
| BI-22 | CAUGHT | CAUGHT | judged (1.27) | — | `V2-G6-no-time-left`=red `V2-G7-no-anchor`=red `V2-G8-budget-0`=red | 同 |
| BI-23 | CAUGHT | CAUGHT | judged (1.25) | — | `V5-S14-failing-sleep-kills-at-once`=red | 同 |
| BI-24 | CAUGHT | CAUGHT | judged (1.29) | — | `V2-G12-segment-trigger-asks-gate`=red | 同 |
| BI-25 | CAUGHT | CAUGHT | judged (1.29) | — | `V2-G12-segment-trigger-asks-gate`=red | 同 |
| BI-26 | CAUGHT | CAUGHT | judged (1.27) | — | `V2-G14-cwd-extension-file-with-entry`=red | 同 |
| BI-27 | CAUGHT | CAUGHT | judged (1.27) | — | `V9-C4-value-limit-in-rerun`=red | 同 |
| BI-28 | CAUGHT | CAUGHT | judged (1.27) | — | `V4-S17-rerun-whole-checkpoint`=red | 同 |
| BI-29 | CAUGHT | CAUGHT | judged (1.27) | — | `V4-S18-rerun-segment-checkpoint`=red | 同 |
| BI-30 | CAUGHT | CAUGHT | judged (1.27) | — | `V4-S16-rerun-collect-checkpoint`=red | 同 |
| BI-31 | CAUGHT | CAUGHT | judged (1.48) | — | `V4-S16-rerun-collect-checkpoint`=red `V4-S17-rerun-whole-checkpoint`=red `V4-S18-rerun-segment-checkpoint`=red | 同 |
| BI-32 | CAUGHT | CAUGHT | judged (1.48) | — | `V4-S18-rerun-segment-checkpoint`=red | 同 |
| BI-33 | CAUGHT | CAUGHT | judged (1.48) | — | `V10-N6-filtered-long-line-rows-only`=red `V7-N7-big-judge-filtered-long-line`=red | 同 |
| BI-34 | CAUGHT | CAUGHT | judged (1.48) | — | `V7-N8-whole-branch-returns-big-judge`=red | 同 |
| BI-35 | CAUGHT | CAUGHT | judged (1.45) | — | `V7-N9-segment-routes-to-big-judge`=red | 同 |
| BI-36 | CAUGHT | CAUGHT | judged (1.45) | — | `V7-N9-segment-routes-to-big-judge`=red | 同 |
| BI-37 | CAUGHT | CAUGHT | judged (1.45) | — | `V7-N10-blank-padded-long-line`=red | 同 |
| BI-38 | CAUGHT | CAUGHT | void (SKIP [void]): run again (1.45) | CAUGHT (judged, 0.79) | `V8-D4-growth-text-whole`=red | 同 |
| BI-39 | CAUGHT | CAUGHT | SKIP [load] (2.05) | CAUGHT (judged, 0.79) | `V8-D5-growth-text-segment`=red | 同 |
| BI-40 | CAUGHT | CAUGHT | SKIP [load] (2.05) | CAUGHT (judged, 0.79) | `V8-D5-growth-text-segment`=red | 同 |
| BI-41 | CAUGHT | CAUGHT | SKIP [load] (2.05) | CAUGHT (judged, 0.79) | `V5-S15-job-refuses-outside-group-leader`=red | 同 |
| BI-42 | CAUGHT | CAUGHT | SKIP [load] (2.37) | CAUGHT (judged, 0.79) | `V5-E19-deadline-with-term-ignored`\*=red | 同 |
| BI-43 | CAUGHT | CAUGHT | SKIP [load] (2.22) | CAUGHT (judged, 1.20) | `V5-E19-deadline-with-term-ignored`\*=red | 同 |
| BI-44 | CAUGHT | CAUGHT | judged (1.88) | — | `V2-G3b-gate-uses-build-facts`=red | 同 |
| BI-45 | CAUGHT | CAUGHT | judged (1.88) | — | `V6-S20-segment-fallback-text`\*=red | 同 |
| BI-46 | CAUGHT | CAUGHT | SKIP [load] (2.29) | CAUGHT (judged, 1.01) | `V7-N11-lmax-edge-normal`=red | 同 |
| BI-47 | CAUGHT | CAUGHT | SKIP [load] (2.29) | CAUGHT (judged, 1.01) | `V7-N13-unmeasured-length-rows-only`=red | 同 |
| BI-48 | CAUGHT | CAUGHT | SKIP [load] (2.29) | CAUGHT (judged, 1.01) | `V7-N13-unmeasured-length-rows-only`=red | 同 |
| BI-49 | CAUGHT | CAUGHT | SKIP [load] (2.29) | CAUGHT (judged, 1.09) | `V4-S19-block-text-bytes`=red | 同 |
| BI-50 | CAUGHT | CAUGHT | SKIP [load] (2.29) | CAUGHT (judged, 1.09) | `V3-G12-time-left-zero-padded`=red | 同 |
| BI-51 | CAUGHT | CAUGHT | SKIP [load] (2.27) | CAUGHT (judged, 1.09) | `V11-S5-longline-head-verbatim`=red `V11-S7-longline-text-verbatim`=red | 同 |
| BI-52 | CAUGHT | CAUGHT | SKIP [load] (2.27) | CAUGHT (judged, 1.09) | `V8-D4-growth-text-whole`=red | 同 |
| BI-53 | CAUGHT | CAUGHT | SKIP [load] (2.27) | CAUGHT (judged, 1.09) | `V8-D5-growth-text-segment`=red | 同 |
| BI-54 | CAUGHT | CAUGHT | SKIP [load] (2.27) | CAUGHT (judged, 1.17) | `V11-S6-longline-chinese-line-verbatim`=red `V11-S7-longline-text-verbatim`=red | 同 |
| P-0 | GREEN | NOT-JUDGED | SKIP [load] (2.09) | GREEN (judged, 1.03) | （全部移植用例） | 首跑因负载不同，重跑同 |
| P-M29 | CAUGHT | CAUGHT | SKIP [load] (2.09) | CAUGHT (judged, 1.17) | `V7-N11-lmax-edge-normal`=red | 同 |
| P-L-sentinel | CAUGHT | CAUGHT | SKIP [load] (2.08) | CAUGHT (judged, 1.17) | `V7-N13-unmeasured-length-rows-only`=red | 同 |
| P-L-text | CAUGHT | CAUGHT | SKIP [load] (2.08) | CAUGHT (judged, 1.17) | `V11-S5-longline-head-verbatim`=red `V11-S7-longline-text-verbatim`=red | 同 |
| P-G-limit | CAUGHT | CAUGHT | SKIP [load] (2.08) | CAUGHT (judged, 1.15) | `V8-D3-growth-8193-plain`=red `V8-D3-growth-8193-braced`=red | 同 |
| P-G-text-whole | CAUGHT | CAUGHT | SKIP [load] (2.08) | CAUGHT (judged, 1.15) | `V8-D4-growth-text-whole`=red | 同 |
| P-G-text-segment | CAUGHT | CAUGHT | SKIP [load] (2.08) | CAUGHT (judged, 1.15) | `V8-D5-growth-text-segment`=red | 同 |
