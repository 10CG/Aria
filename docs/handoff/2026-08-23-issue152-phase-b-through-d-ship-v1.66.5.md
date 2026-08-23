---
track-id: pre-merge-gate-no-run-for-branch
owner-container: simonfish/023236f2
phase: D-done
status: done
updated-at: 2026-08-23T06:05:00Z
---

# Cycle Handoff (2026-08-23) — #152 Phase B→C→D 全程: v1.66.5 ship + 归档 (track 终结)

> **一句话**: `/state-scanner` [1] 接上 session 的 B.1-done → Phase B 20/20 任务 (两轨并行 subagent, TDD 成对 RED→GREEN 逐 commit, 13 commits) → Rule #6 AB 真跑 (新 10/10 vs 基线 6/10) → SC-13 活体两 episode → owner 选 A 进 Phase C → aria-plugin **v1.66.5** (`a0fe720`) + 主仓 `2a1a0b2` 双端一致 + 补打两个漏 tag → Phase D: #152 closed / #156 立案 / 归档门 runtime_probe **pass** (首个声明者) / claim 释放。**track 终结。**
>
> ⭐ **这段对话最该留下的一件事**: AB 的两臂喂的是**新代码**产出的 gate JSON — 旧版文档的模型照抄 `raw_message` 就把一半断言做对了, 测前预测 5/10 错, 全错在低估基线。**量文档增量时, 输入必须是旧版代码的输出**; 否则代码侧交付的价值会被算到文档头上 (或者反过来, 让文档看起来没价值)。新 memory `feedback_ab_input_must_be_baseline_output`。

## §0 入口 (新 session 优先读)

- **本轨已终结**: spec 归档 `openspec/archive/2026-08-23-pre-merge-gate-no-run-for-branch/` (gate: complete=true / verdict=pass / runtime_probe pass count 7); claims `s-a637@2033` + `s-adae@2118` 均 `done` (release_gate push_success=true)。
- **版本**: aria-plugin **v1.66.5** @ `a0fe720` (origin==github; tags v1.66.5 + 补打 v1.66.4@`9e6a17c` / v1.66.1@`3b97c35`); 主仓 master `2a1a0b2` + 本 handoff commit (origin==github)。
- **owner action (唯一未清)**: `plugin-cache-currency` STALE (运行时装 1.66.3 < SOT 1.66.5) — `/plugin marketplace update 10CG-aria-plugin` → `/plugin update aria@10CG-aria-plugin` → 重启 session (#172 形状, 本 session 两次 `/state-scanner` 都是从 1.66.3 副本加载 skill 指令)。
- **并发轨**: `simonfish/bfe8285d` 在做 `linked-issue-normalization` (post_planning R5 不收敛 → owner override 进 Phase B, ship target **v1.67.0**); 本 session 合并期间其 master 两次前进 (`914a4c7` / `826b356`), 零交集, 重同步后合。

## §1 已完成 (按时间顺序)

1. `/state-scanner` → handoff awareness 选定本轨 → owner [1] → `phase1_gate` advisory claim `s-adae@2118` passed → 主仓 feature merge master (两份 handoff)。
2. **Phase B** (两轨按文件域并行, subagent 不 commit, 主控统一提交 + 核验):
   - gate 轨: 004 守卫 (基线绿, 三 mutation 红, 主控复跑 m1/m2) + 002 RED `5b9337f` → 003 GREEN `e95b202` (**仅两生产文件**, INV-1 四合取) → 005 RED `a9d148c` → 006 `3b12cc6` → 007a RED `2039162` → 007b `8898518`。
   - helper 轨: 008 RED `f8024c7` → 009 `97915a1` (CLI record/reset/clear)。
   - 文档: 010a RED `33922ef` → 010 `e32c53a` → 011 `c19c284` → 014 `b62354e`。phase-c 119→148 / workflow-runner 22→38; doc-sync 6/6; CRLF 保持 (两 SKILL.md 是 CRLF); INV-5 零命中。
   - 013 (主控): 逐 skill 全量绿; INV-3 true 分支对偶过。
   - 012 (主控, Rule #6 第三行): NEG-4 fixture + catalog v1.2.0 + `/skill-creator` 流程真跑 → `ab-results/2026-08-22-pre-merge-gate-no-run-for-branch/` (PREDICTION 先落, 主控实读 4 份 answer.md 取证); 红窗 `'green' != 'wait'`; #127 评论 19674。
   - 014 (主控): SC-16 (b) warn → SC-13 活体 ep1 (path-matched 首推 **8s 内已 pending**, 盲区二次未复现) + ep2 (`branches` 过滤结构性零 run: `not_found`×3 → `should_prompt` 55s → 处置 (b) 后 15s pending) → SC-16 (c) pass; traps §六 证据行 + SKILL.md 坑计数 7→11; 收尾断言全过。
3. **Phase C** (owner 选 A): 三面 fetch + stale-local-main 断言 (主仓 origin 已前进, aria 本地 master 陈旧 — 均按流程重同步) → aria 5 文件版本同步面 `f90881b` → C.2.4 gate 自 dogfood green (not_applicable; **surface 义务**: 变更路径无 CI workflow 覆盖, main in-flight 已核) → 本地 `--no-ff` merge `a0fe720` + 三 tag → 双推 + 逐 remote `ls-remote` 全一致 → 主仓 14 版本点 + gitlink `de75443` → C.2.4 green + C.2.4.5 PASS (forward bump) → merge `2a1a0b2` 双推一致 → scan: gitlink 6/6 ok, parity true, custom checks 9/10。
4. **Phase D**: #152 收尾评论 19712/19718 + closed (GET 确认); aria-plugin **#156** 立案 ((b) 轴对未被领取 main run 不可见); proposal Status → Complete (含审计轨迹句); yaml 20/20; D.2 gate pass → `git mv` 归档 (openspec CLI 未装, 与既有归档同形) → 归档件复核 gate pass; D.2b release_gate 两 claim done; D.3 本 handoff; D.4 estimator capture (见 §7)。
5. Memory: 新 1 + 追记 2 (§8)。

## §2 未完成 / Carry-forward 清单 (AI 内省, load-bearing)

- 🟡 **owner action**: `plugin-cache-currency` 刷新 (§0)。
- 🟡 **spec 欠定点 (AB 新版 eval-2 抓出, 未改本 spec)**: workflow-runner Exit 2.5 `abort` 取「verdict=fail 语义」, 但 `gate_state.status` 是否从 `waiting` 翻 `fail` 未明说; 现有 CLI 无「翻 status 且保留计数」路径 (`record --verdict fail` 会把 obs 归零)。新版答案选择保留 waiting 用 `session.status=failed` 承载。**请 owner 裁**: 若要翻 status, 属 helper 变更 (Rule #6)。
- 🟡 **既有文档缺口 (AB 旧版 eval-2 抓出)**: workflow-runner Exit 2 `retry_count > max` 的 `max` 在 SKILL.md / §C.2.4 配置表**均未定义** (只有 `wait_check_intervals` 且明写数组耗尽后重复)。本 spec 未触及; 建议立案或在下次 workflow-runner 文档轮勘正。
- 🟡 **既有测试故障 (非本 spec)**: `state-scanner/tests/test_collision.py` + `test_coordination_ref_lib.py` 2 个 collection error (`lib.collision` / `lib.coordination_ref` 模块不存在), **基线 `9e6a17c` 同样**; 其余 1312 passed。建议立案 (可能与 #174/#180 Layer L 轨相关)。
- 🟡 **实测节奏偏差** (traps §六 已记, 未改 spec 数字): 单次 gate ≈17s (两 ls-remote + 两 aether) ⇒ 「~90s 交人」实际 ≈140s。
- ⏸️ 承前: aria-orchestrator 工作树停 `feature/m6-cost-model-telemetry@92acce5` 有意排除 (gitlink 未动); M6 三门; backlog (#138/#180/#182/#154)。

## §3 关键风险 / 已知陷阱

- **INV-1 合取 4 对 commit message 文案敏感**: `git show --stat <c> | grep -c 'aether.py|pre_merge_gate.py'` 把 message 正文也数进去, 写了文件名字面就从 2 变 3; 已 amend + yaml 勘正 (`--format=` 稳健形式)。同形: 任何「`git show` 输出计数」类机检都要先问「message 里会不会出现 pattern」。
- **subagent 因果归因会错**: TASK-006 agent 把 doc-sync 一条转绿归因于自己的 docstring, 实为并行 TASK-010 改了主仓模板 (那 5 条断言没一条读 docstring)。diff 本身正确; 只是「谁让它绿的」说错了。并行派活时, 任何「顺带转绿/转红」的归因都要主控自己复核。
- **aggregate_benchmark.py 要 `run-N/` 层 + `summary` 块**, 与本仓 ab-results 先例 (平铺 `with_skill/old_skill/`) 不兼容, 跑出全 0 不报错 — 按先例手工生成 benchmark.json。
- 两容器并发: 对方本 session 内两次推 master; merge 前 `local==origin==github` 断言 + gate 自带 fetch 各抓到一次。开工前三面 fetch 仍是硬纪律。

## §4 实战教训 (memory 沉淀来源)

```
[候选 memory] — 本 session 已写
- feedback_ab_input_must_be_baseline_output (新): 量文档/指令面增量时 AB 输入必须取**旧版代码**的输出; 喂新代码输出会把代码侧交付算到文档头上 (预测 5/10 错, 全在低估基线)
- feedback_cross_agent_verdict_independent_verify (追记): subagent 对「顺带转绿」的因果归因会错 (TASK-006 归因 docstring, 实为并行 TASK-010 改模板); 归因也要独立复核, 不只结论
- feedback_new_mechanical_check_must_run_at_baseline_first (追记): `git show --stat | grep -c` 类计数把 commit message 数进去 — 三态亲跑时要包含「message 含 pattern」这一态
[未写下经验]
- 「盲区三次活体未复现」: #152 的原始陈述可能本就是 runner 忙闲瞬态 (F4), 机制不依赖它; 但 spec Why 从「恒中」降到「观测一次」是在 Phase B 才发生 — 起草期若先做一次探针 (memory probe-first) 会省掉 7 轮 post_spec 里围绕「恒中」的若干 Major。已有 memory 覆盖 (probe_first_scope_reframe), 不新写
- 一次 dispatch 产生成对 run 同 started_at (TASK-0a): gate 取最近 run 时 tie — 已在 traps + 处方 (a) 文案; 若要机制化 (tie 按 run id / 全 success 才 passing) 另案, 本 session 未立 (spec §2 carry 已列, 等 owner 看是否值得)
```

## §5 多维度同步状态 (机械 + 人工)

| 维 | 状态 |
|---|---|
| UPM | 无 (Aria 不配置) |
| OpenSpec | 活跃 8 (本轨归档后); `openspec/archive/2026-08-23-pre-merge-gate-no-run-for-branch/` 139 归档; pending_archive 0 |
| User Story | 无变动 |
| PRD / 架构 | 无变动 (arch doc 87d, 本 spec 不涉架构) |
| 版本 | aria-plugin v1.66.5 (plugin.json SOT; marketplace/VERSION/CHANGELOG/README 同步; 主仓 14 点 + i18n 标记 — 正文无实质变更不重译) |
| custom checks | 9/10 (plugin-cache-currency owner action) |

## §6 Next session 入口 + 优先级建议

入口: `/aria:state-scanner`。本轨终结, 无 carry-id 可接。候选 (按 owner 排序):
1. owner 侧先刷 plugin cache (§0) — 之后 `/state-scanner` 才是 10/10。
2. 两个 Draft 轨: `a1-entry-claim-duplicate-work-guard` (C1/C2 owner 已裁, 待 rework 进 A.2) / `linked-issue-normalization` (对方容器在做, **勿撞**, 先三面 fetch 看板)。
3. §2 的三件「建议立案」: abort 翻 status 欠定 / `max` 未定义 / state-scanner 2 个 collection error — 立案成本低, 可在下次 session 开头顺手做。

## §7 提交清单 (commit hash + multi-remote parity)

```
[aria master]   9e6a17c (v1.66.4) → 13 feature commits → f90881b (release bump) → a0fe720 (merge, v1.66.5) | origin==github (ls-remote 逐个核验)
[aria tags]     v1.66.1@3b97c35 / v1.66.4@9e6a17c / v1.66.5@a0fe720 | origin==github
[main master]   084209f → (merge 914a4c7/826b356 对方轨) → 2a1a0b2 (merge feature: 模板/gitignore/DEC/benchmarks/spec yaml/gitlink/14 点) → 8ffcc25 (yaml 015) → 本 handoff commit (归档 mv + latest.md + handoff) | origin==github
[main feature]  feature/152-no-run-for-branch 已合入 master (保留分支, 未删)
[coord ref]     claims/023236f2/s-a637@2033 + s-adae@2033 → done (push_success=true)
[aria-orchestrator] feature/m6-cost-model-telemetry@92acce5 (有意排除, 承前)
[estimator]     D.4 capture: work_metric 2,997,521 tokens (cache_creation 2.59M) / wall 32,002s ≈ 8.9h (本 cycle Phase B→D 含 AB 与活体)
```

## §8 Memory entries this session (1 new + 2 追记)

- `feedback_ab_input_must_be_baseline_output.md` (新, 已入索引)
- `feedback_cross_agent_verdict_independent_verify.md` (追记 2026-08-23: 因果归因也要复核)
- `feedback_new_mechanical_check_must_run_at_baseline_first.md` (追记 2026-08-23: commit message 入计数)

## Cross-references

- Spec 归档: `openspec/archive/2026-08-23-pre-merge-gate-no-run-for-branch/{proposal.md,detailed-tasks.yaml}` · 审计 `.aria/audit-reports/post_spec-R{1..7}-1787379154696-*` / `post_planning-R{1..5}-1787403030672-*`
- AB: `aria-plugin-benchmarks/ab-results/2026-08-22-pre-merge-gate-no-run-for-branch/` (PREDICTION.md / RESULT.md / benchmark.json) · catalog `ab-suite/phase-c-integrator-pre-merge-gate.json` v1.2.0 + NEG-4
- Issues: aria-plugin#152 (closed, 评论 19712/19718) · #156 (新, (b) 轴) · #127 (评论 19674)
- traps §六: `aria/skills/phase-c-integrator/references/pre-merge-gate-empirical-traps.md` (含 SC-13 证据行)
- 前序本轨 handoff: [2026-08-22 Phase A 十二轮 + B 三前置](./2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md)
- 并发轨: `linked-issue-normalization` (simonfish/bfe8285d, 主仓 `openspec/changes/linked-issue-normalization/`)
