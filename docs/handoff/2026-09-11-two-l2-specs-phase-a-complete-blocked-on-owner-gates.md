---
track-id: two-l2-specs-195-199-phase-a
owner-container: aria-runner-bot/bfe8285d
phase: A
status: done
updated-at: 2026-09-13T03:20:00Z
---

# Aria — Session Handoff (2026-09-11, 会话收尾) — 两份 Level 2 Spec 的 Phase A 各跑满 5 轮 post_spec, 双双停在 owner 裁决面

> **⇒ 本轨终结 (2026-09-13, simonfish/023236f2)**: §2 的 H1–H4 已全部裁决 —— owner 对两份 Spec 的 max_rounds 终局均取路径 [1], 22 条待复议项按「产品级 owner / 技术级 AI」分工归类裁定 (决策单 `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md`), 两份 Spec 升 Level 3 转 Approved, 由本容器以各自 change-id 重新认领 (`handoff-multibranch-subdir-path-fidelity` 先 / `pre-merge-completeness-gate-change-scope` 后)。后续见 `docs/handoff/2026-09-13-owner-gates-cleared-195-199-approved-level3.md`。本文件其余内容保持原样。
>
> **一句话**: 本对话 (2026-09-06 14:20Z → 2026-09-11 00:20Z, 容器 `aria-runner-bot/bfe8285d`) 从 `/aria:state-scanner` 入口起, 按 owner 的 `/goal`「创建 agent team + 动态工作流, 一口气完成当前推荐的所有工作流」执行: **Aria#200 triage 全闭环交付**; **Aria#195 与 Aria#199 两份 Level 2 Spec 各自走完 A.1 起草 + post_spec convergence 五轮五席审计 + 五次换人 rework**。两份**同时**在 R5 到达「Critical 0 / 五席自报一致 / 骨架无人推翻」, 也**同时**因 `max_rounds = 5` 耗尽而 `converged = false`。**Phase B 目前一条合法动作都没有** —— 两份的下游全部卡在 owner 裁决面, 按 Rule #10 不得由 AI 自行降格。
>
> **本 session 最该记住的一件事**: **收敛判据的分母不是「审计还能不能找到问题」, 而是「Major 能不能归零」**。`unanimous_pass` 要求 `vote == PASS`, 而 `vote == PASS` 要求 Critical **与 Major 同时**为 0。两份 spec 的 Major 序列分别是 15/10/19/10/9 与 9/9/12/14/15 —— 从未归零, 所以五轮 Vote 恒为 `REVISE 5 / PASS 0`, 与「质量是否在改善」完全脱钩 (#195 的 Critical 已经 2→3→0→1→0)。**把 max_rounds 用完 ≠ 审计失败**, 但现行判据下它也**不可能**自然收敛, 除非有人把 Major 清到 0。这条已入 memory。

> **Session period**: 2026-09-06 14:20Z → 2026-09-11 00:20Z (跨 5 天, 中间被**周限额**中断约 62 小时)
> **Next session 入口**: 优先读本 doc → `/aria:state-scanner` → §6

---

## §0 入口 (新 session 优先读)

1. 运行 `/aria:state-scanner`。主仓 master **`bf42cf4`** (origin/github 两端 MATCH); gitlink `aria` = **`f314785`** (v1.73.0, 同伴轨所发) / `standards` = `21748d4` / `aria-orchestrator` = `237045a`。四仓两端 parity 全 equal, 零 pending push。
2. **本容器持有两条 active claim, 都停在 Phase A 出口**:
   - `handoff-multibranch-subdir-path-fidelity-bfe8285d` (Aria#195)
   - `pre-merge-completeness-gate-change-scope-bfe8285d` (Aria#199)
   两条都**不是 done, 也不是 abandoned** —— 是「Phase A 完成, 等 owner 开门」。会话结束后心跳停止, `--sweep-stale` 迟早会把它们标 abandoned, 这是设计行为; 下个 session 用**同一串 raw track-id** 重新认领即可。
3. **两份 spec 都不能进 Phase B**, 不是因为没做完, 是因为每一条合法下一步都需要 owner 先裁。具体门见 §6, 优先级已排好。
4. 同伴容器 `simonfish/023236f2` 在本对话被中断期间 (09-07…09-09) ship 了 **aria-plugin v1.73.0** 并归档了 `archive-gate-registration-class-and-skill-drift`; 其主仓同步已合 (PR #202 `9f25a666`)。本容器已 merge 并对齐, 两份 spec 的基线已重冻到 `f314785`。

---

## §1 已完成 (按时间顺序, UTC)

| 时间 | 事件 | 证据 |
|------|------|------|
| 09-06 14:2x | `/aria:state-scanner` 入口, scan.py exit 0 零 soft error; 推荐三条工作流 | `.aria/state-snapshot.json` |
| 09-06 14:4x | **Aria#200 triage** 全闭环: `confirmed / major / next-cycle`, 3 条 hermetic case 全中 (含拿本机 `/home/dev/Aether` 真实 monorepo 布局做对照), 回帖 **22421** | `bda0238`; `.aria/triage-report-200.json` + `triage-comment-200.md` |
| 09-06 14:47 | 两条轨经 `phase1_gate --phase A.1 --mode advisory --include-terminal` 认领, `outcome=passed`, `linked_issue_overlap=[]`, push ok | coordination ref |
| 09-06 15:0x | #199 proposal A.1 起草 (subagent) | `3f4b379` |
| 09-06 15:4x | #195 proposal A.1 **主 loop 亲自起草** (原起草席撞 Fable 额度挂掉, proposal 从未产出) | `3f4b379` |
| 09-06 16:2x | **coordination ref 分叉手工并集合并** (aria-plugin#169 活体复现), 两端 MATCH; 证据回帖 **22609** | ref `60a5870` |
| 09-06 17:0x–09-07 02:4x | #195 post_spec R1→R4 (五席 + 聚合 + 换人 rework ×4) | `813e82c` `f634d83` `e58ac22` `1a40579` `cf6f56a` |
| 09-06 17:0x–09-07 ~07:0x | #199 post_spec R1→R2 | `2f7ad0c` `020421f` |
| 09-07 ~07:2x | **两条流因周限额中止** —— 失败上限生效, 干净返回 (47 / 31 agent, 非上次的 989) | 见 §4 教训 1 |
| 09-10 17:0x | 恢复: merge 同伴推进 (`c115fd4`), 子模块对齐 v1.73.0, 两份 spec 基线重冻核验 | `fe703c5` |
| 09-10 17:2x–19:1x | #195 **R5 (终轮)** + 换人 rework | `2bc97f1` `5341aa9` `4bed54e` |
| 09-10 17:2x–09-11 00:0x | #199 **R3→R5 (终轮)** + 换人 rework ×3 | `fa77405` `0483c69` `3d83be4` `be4d1eb` `bf42cf4` |

**两份 spec 的 post_spec 全周期账**:

| | R1 | R2 | R3 | R4 | R5 | 终局 |
|---|---|---|---|---|---|---|
| **#195** C / M | 2 / 15 | 3 / 10 | 0 / 19 | 1 / 10 | **0 / 9** | `max_rounds` 耗尽, `converged=false` |
| **#195** verdict | FAIL | FAIL | PASS_WITH_WARNINGS | FAIL (仅一席定级) | **PASS_WITH_WARNINGS (五席一致)** | |
| **#199** C / M | 5 / 9 | 2 / 9 | 3 / 12 | 0 / 14 | **0 / 16** | 同上 |
| **#199** verdict | FAIL | FAIL | FAIL | PASS_WITH_WARNINGS | **PASS_WITH_WARNINGS (五席一致)** | |

两份都是 **连续三轮零重复提出** (每轮缺陷全部锚在上一轮 rework 的新文本上, 与前轮四元组交集近零), 且 **骨架五轮无一席主张推翻**。

---

## §2 未完成 / Carry-forward 清单

### 高优先级 (下个 session 第一件事)

| # | 项 | 说明 | 来源 |
|---|---|------|------|
| H1 | **owner 裁 `max_rounds` 三路径 ×2** | 两份 spec 的待复议 **条目 0** 各自载完整五轮表 + 收敛判据分析 + `audit-engine §降级策略` 三路径逐字原文 + 支持 [1]/[2] 的客观分列。**建议一并裁**, 因为两份同期同终局且**同抢下一个版本号** | 两份 proposal §待 owner 复议 条目 0 |
| H2 | **#195 另外三道门** | 待复议 7 (Level 2 vs 3) · 待复议 6 (版本级别 PATCH `v1.73.1` vs MINOR `v1.74.0`) · 待复议 2 第 (3)(5) 问 (子目录采用方只拿降级 pointer 是否接受 / 是否本 cycle 动 `handoff-mechanics.md` 处方面 —— 后者会把 Rule #6 的 AB 范围扩到 phase-d-closer 与 session-closer) | `openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` |
| H3 | **#199 另外两道门** | post_planning (A.2 后必跑的 enabled 闸) · 复议 #1/#7/#8/#10(含新 (d))/#11/#13 与版本级别 #4b 未裁前不得进 TDD RED (已成文为 B.0 第 5 项前置门) | `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` |
| H4 | **追认或推翻 DEC-20260907-001** | 我在 owner 不在场时裁了 #195 的 `filename` 语义三选一 (取 A′ + 写侧守卫)。决策单载完整理由、反证据、代价与三点请复议。不追认则回退 `rel_path` 字段与守卫, 成本约一个 commit | `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md` |

### 中优先级

- **#195 的 Task 5.3**: 让 `handoff.py::_parse_latest_pointer` (`:288` 剥目录段) 与 `_scan_md_files` (`:300,318` 非递归) 支持子目录 —— 本 spec 只用写侧守卫使其**诚实降级**, 缺口本体另开 issue (仓别未定, 见 proposal 待复议)。
- **`check_bare_issue_refs.py` 有一整类假阳性**: 表格行号 (`#1` / `#2` / `#12` …) 被判为裸 issue 引用。该 check 是 **fail-CLOSED** 的 ⇒ 会卡住**任何带编号表格的 spec**。#195 已记进 Task 5.4a; #199 的 R3 rework 另记「归属先确认再决定跑不跑」。**两份都没解决它**, 建议单独一条 issue 给 check owner。
- **aria-plugin#169** 已补活体复现证据 (comment 22609) 并给出「恢复必须是并集而非重试」+「`push_success=false` 应在编排层可见」两条修法观察, 待该 issue 的负责轨处置。

### 低优先级 / cleanup

- 两份 spec 的 rework 记录 (R1–R5 共 10 份) 目前只在 scratchpad (`/tmp/.../scratchpad/*-rework-R*.md`), **会随机器清理消失**。若要长期可审, 需搬进仓内 (但它们体量大, 搬之前先定归属目录)。
- `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 与临时复现脚本 (`repro195_baseline.py` / `exp_sc3_quotepath.py` 等) 同在 scratchpad, Phase B 写测试时可直接搬 `build_repo()` 五族 fixture 构造器。

### 机械补漏 (autofill backstop, AI 内省未列)

- autofill `unfinished` 列出 **132 条**, 全部来自 **M6/M7 六份 spec 的 `tasks.md`** (cost-model-telemetry 25 / e2e-resilience 25 / release-closeout 41 / m7-agent-lifecycle 18 / m7-fleet-aggregation 20 / dispatch-input-delivery 3), **不是本 session 的承诺** —— 本 session 两份 spec 用 proposal 内联 `## Tasks` (Level 2 形态), autofill 看不到。按 Rule #9 归各自轨的 handoff。
- consistency_check 6 条 `active_change_not_in_upm` (advisory): 本仓无运行时 UPM (memory `project_aria_no_runtime_upm`), 已知恒出。
- autofill `sync`: **零告警**, 四仓两端全 equal。

---

## §3 关键风险 / 已知陷阱

1. **收敛判据与质量脱钩** (本 session 最重要的结构性发现): 见头部「最该记住的一件事」。在 Major 归零之前, 任何 spec 都**不可能**自然收敛, 无论 Critical 曲线多好看。owner 裁 [2] 加轮次时要意识到: 加轮只在「Major 真能被清空」时才导向收敛, 否则只是多烧一轮。
2. **「基线陈旧」是会自我再生的缺陷族**: #195 的 R5 有 5 条 major 属此族, 席位明写「若不重冻基线, 后续每多一天都会再生一批同族 major, 收敛不可能发生」。**长周期 spec 必须把「触点文件集」成表**, 否则每次基线复核的过滤面由执笔者临场重建 —— 我 09-10 那次就因此漏检 (只 diff 了 5 个代码落点, 完整引用面实为 7 文件 / 118 增 / 27 删)。
3. **勘正动作由原作者执笔时错误系统性逃逸**: #195 R5 有一族 4 条全是 R4 落地内容自身的缺口 (SC-3 的环境隔离处方够不到子进程 / 「不可解码名跳过」在 `errors="replace"` 通路上恒不触发 / 「上报 filename 逐字节不变」全 SC 零覆盖 / `degraded_reason` 两支未定义), 均经 hermetic 实跑证伪。**本 session 起五次 rework 全部换非原作者执笔**, 建议固化为默认。
4. **自引行号在长文档里会整体腐坏**: #199 R5 对 469 行全文回扫, **26 处自引 / 18 个不同行号, 无一处指向它自称的内容** (4 处指空行)。五轮审计没人发现, 因为每轮席位只核自己关注的那几处。处置是全部改为**锚点式** (小节号 + 逐字标题串), 并把「自引锚点」补进 rework 核对轴 (五轴 → 六轴)。**建议所有长 spec 禁用自引行号**。
5. **额度是这类工作流的真实约束面**, 且有两层: 单模型额度 (Fable 5.1 耗尽 ⇒ 换模型即可) 与**周限额** (整账号, 只能等重置)。两者都表现为 subagent 批量失败。
6. **写死的模块可能零生产调用点**: #195 的写侧守卫要加在 `write_latest_md` 上, 而该函数全插件树零非测试调用点 —— 这是 `phase-1-collectors.md:95` 白纸黑字的既有设计决定 (deliberately D.3-scoped), 生产 D.3 的 pointer 由 AI 按散文处方手改。**加防御到死代码上 = 测试全绿的循环论证**。

---

## §4 实战教训 (memory 沉淀来源)

[候选 memory] — **收尾第二轮 (16:2x) 已落 4 条新文件 + 1 条扩写, 详见 §8; 索引零新增行**

- **收敛判据的分母是 Major 归零, 不是「还能不能找到问题」** —— `unanimous_pass` 要求 `vote == PASS`, 而 `vote == PASS` 要求 C 与 M 同时为 0。两份 spec 的 Critical 都已归零 (2→3→0→1→0 / 5→2→3→0→0) 而 Major 从未归零, 于是五轮 Vote 恒 `REVISE 5`。**「max_rounds 耗尽」与「审计失败」是两件事**, 报告时不可混。建议 type: `feedback`
- **长周期 spec 必须把「触点文件集」成表** —— 否则每次基线复核的过滤面由执笔者临场重建, 必然漏检。我 09-10 只 diff 了 5 个代码落点就断言「触点零漂移」, 完整引用面实为 7 文件 / 118 增 / 27 删。建议 type: `feedback`
- **长文档禁用自引行号** —— #199 实测 26 处自引 / 18 个不同行号无一正确, 4 处指空行, 五轮五席均未发现 (每席只核自己关注的那几处)。改锚点式 (小节号 + 逐字标题串)。建议 type: `feedback`
- **workflow 脚本里「本轮作废 + round--」必须配连续失败上限** —— 否则持久性失败 (额度/限流) 会让它无限重试。修复前那次空转 989 个失败 agent 撞 1000 上限; 加上限后同样场景只用 47 / 31 个就干净中止并返回完整历史。建议 type: `feedback`
- **AI 在 owner 不在场时做设计裁定, 必须同时产出可证伪的反证据** —— 我裁 A′ 时推翻了 R1 自己「A′ 不新增失败面」的结论 (实读 `latest_md_writer.py:78-95`: 候选集只收 `status == "active"`, 子目录文件今天恒为 legacy 故永不入选, 路径修好后即入选)。**裁定的价值不在结论, 在它附带的那条实读证据**。建议 type: `feedback`
- **coordination ref 分叉的恢复必须是「并集」而非「重试」** —— 远端多出的是对方的新文件, 本地多出的是我的新内容, 任何一侧覆盖都丢 claim。按 (container, session) 路径粒度做并集天然无写写冲突。已回帖 aria-plugin#169。建议 type: `feedback`

[未写下经验]

- 「五席审计」的边际产出在 R3 之后明显从「找设计缺陷」转向「找文本/行号/计数不一致」。两份 spec 的 R4/R5 里 major 绝大多数是后者。这暗示**审计轮次的透镜应随轮次演进** (前两轮设计面, 后三轮机械面), 而不是每轮都用同一组五席。未写: 这是对 audit-engine 的设计建议, 需要先有第三份 spec 的数据才够立论。
- 两份 spec 同时到达终局并**同抢一个版本号**这件事, 说明 `<vNEXT>` 的取号协调在**同容器内多轨**场景也需要机制 (现有 memory 只覆盖跨容器)。未写: 等这次 owner 定了取号顺序再看是否成规律。

---

## §5 多维度同步状态

| 维度 | 存在? | 状态 | 备注 |
|------|-------|------|------|
| UPM (进度) | no | — | 本仓无运行时 UPM; consistency 6 条 advisory 恒出 (缺维跳维) |
| User Stories | yes | 未动 | 21 条 (done 17 / in_progress 2 / approved 1 / pending 1), 本 session 不涉及 |
| OpenSpec | yes | 活跃 **8** (含本 session 两份新增), 待归档 **0** | 两份新 spec 均 Draft, 停在 Phase A 出口 |
| PRD | yes | 未动 | — |
| Standards / conventions | yes | **未动** | 两份 spec 都还没到 Phase B, 无 standards 改动 |
| Skill docs | yes | **未动** | 同上 —— 本 session 零代码改动, 全部是 spec 与审计产物 |
| 审计报告 | yes | **新增 60 份** (两份 spec × 5 轮 × 6 文件) | `.aria/audit-reports/post_spec-R{1..5}-*-{195,199 slug}-*.md` |
| Decision memos | yes | 1 新 | `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md` |
| Auto-memory | yes | **0 新** (6 条候选见 §4, 未写) | 本 session 未写 memory 文件 |
| Issues | yes | #200 triaged + 回帖 22421 · aria-plugin#169 补活体复现 22609 · #195 / #199 仍 open (spec 在飞) | — |

---

## §6 Next session 入口 + 优先级建议

```
/aria:state-scanner
```

1. **先把 H1 摆给 owner**: 两份 spec 的 `max_rounds` 三路径, **建议一并裁** (同期同终局 + 同抢版本号)。裁完才谈别的 —— 在此之前两份 spec 连 A.2 都进不去。
2. **H4 追认 / 推翻 DEC-20260907-001** (#195 的 `filename` 语义)。不追认的成本是一个 commit, 拖着的成本是 Phase B 的所有测试都建在一个未追认的前提上。
3. **H2 / H3 的其余门**按 proposal 里的编号逐条过。#199 的 rework 席已明写: 这些门未裁前 **Phase B 一条合法动作都没有**。
4. **不要碰**: M6/M7 六份 spec 的 132 条 tasks (属其各自轨); 同伴容器在飞面。
5. 若 owner 短期不可达, **可做的独立小事**: 给 `check_bare_issue_refs.py` 的假阳性开 issue (§2 中优先级第 2 条) —— 它 fail-CLOSED 且会卡住任何带编号表格的 spec, 与本 session 两份 spec 的裁决面无耦合。

---

## §7 提交清单 (commit hash + multi-remote parity)

本 session 主仓 15 个 commit, 全部 origin/github 两端 `ls-remote` 逐个核验 MATCH:

```
bda0238  docs(triage): Aria #200
3f4b379  docs(spec): A.1 两份 Level 2 proposal 起草
ecb6296  merge origin/master (同伴 v1.71.1 主仓同步 PR #202)
813e82c  docs(spec): post_spec R1 五席 + rework v2 (两份)
2c8eaa6  docs(spec): #195 v3 — 前置门裁定 A′ + 写侧守卫 (DEC-20260907-001)
8da3518  docs(spec): #199 v3 — §1.2b 枚举范围两条边界 + SC-19
f634d83  docs(spec): #195 R2 五席 + rework v4
e58ac22  docs(spec): #195 R3 — Critical 归零
2f7ad0c  docs(spec): #199 R2 五席
1a40579  docs(spec): #195 R4 — 四席 PASS_WITH_WARNINGS
cf6f56a  docs(spec): #195 R4 rework v6
c115fd4  merge origin/master (同伴 v1.73.0)
fe703c5  docs(spec): 两份 spec 补基线复核块 (触点重测 + 版本顺延 v1.73.1)
2bc97f1  docs(audit): #195 R5 终局
5341aa9  docs(spec): #195 R5 rework v7 (换非 R4 执笔者)
4bed54e  docs(spec): #195 R5 rework 收尾
fa77405  docs(audit): #199 R3
020421f  docs(spec): #199 R3 rework v4
0483c69  docs(audit): #199 R4 — Critical 归零
3d83be4  docs(spec): #199 R4 rework v5
be4d1eb  docs(audit): #199 R5 终局
bf42cf4  docs(spec): #199 R5 rework v6 — 终局记录 + 全文自引锚点化
```

**parity (收尾时 autofill 机械核)**: `[main] bf42cf4 | github=equal origin=equal` · `[standards] 21748d4 equal/equal` · `[aria] f314785 equal/equal` · `[aria-orchestrator] 237045a equal/equal` · 零 pending push · 零告警。

另: `refs/aria/coordination` 于 09-06 做过一次手工并集合并 (`60a5870`), 两端 MATCH。

---

## §8 Memory entries this session (4 new + 1 扩写, 索引零新增行)

收尾第二轮 (2026-09-11 16:2x) 补齐了 §4 的候选, **4 条新 memory + 1 条扩写**, 索引条目**全部并入既有同主题行** (MEMORY.md 仍 148 行, 20483 → 21535 bytes, 硬上限 24.4KB 内):

| 文件 | 一句话 | 并入索引哪一行 |
|---|---|---|
| `feedback_convergence_denominator_is_major_zero.md` | 收敛的分母是 Major 归零 (vote=PASS 要求 C 与 M 同时为 0) ⇒ Major 不清空则结构上不可能收敛, 与质量曲线脱钩; 「max_rounds 耗尽」≠「审计失败」 | 与 `audit_convergence_patterns` / `convergence_needs_zero_rework_round` 同行 |
| `feedback_spec_must_enumerate_touchpoint_file_set.md` | 长周期 spec 必须把触点文件集按仓成表, 否则每次基线复核的过滤面临场重建必漏检; 「零漂移」全称句要限定到实际 diff 过的集合 | 与 `baseline_corpus_stat_must_run_against_frozen_snapshot` 同行 |
| `feedback_long_docs_must_not_self_reference_line_numbers.md` | 长文档禁用自引行号 (每轮编辑集体腐坏, 多轮多席审计抓不到 — 469 行里 26 处自引无一正确); 改锚点式 | 与 `grep_window_truncation_breeds_false_corpus_evidence` 同行 |
| `feedback_coordination_ref_divergence_needs_union_merge.md` | `refs/aria/coordination` 分叉须按 claim 路径做并集合并 (非重试非 force); `phase1_gate` exit 0 仍可能 `push_success=false`, 必读 JSON | 与 `partial_push_creates_mirror_divergence` 同行 |
| `feedback_workflow_transient_api_null_guard.md` (**扩写**) | 追加第 4/5 条: 轮次「作废重试」必须配连续失败上限 (持久故障如额度耗尽会空转到 1000 agent 上限, 989 vs 47 实测); 额度有单模型与周限额两层, 表现相同处置不同 | 原行 description 补句 |

**仍未写下的两条** (§4 末段): 「审计轮次的透镜应随轮次演进」(需第三份 spec 的数据才够立论) 与「同容器内多轨的 `<vNEXT>` 取号协调」(等本次 owner 定了取号顺序再看是否成规律)。这两条**有意不写** —— 证据量还不够支撑一条通则。

§4 六条候选中另两条 (「AI 裁定须附可证伪反证据」) 经复核与既有 `feedback_never_write_unverified_impossibility_claims` / `feedback_ai_must_not_self_exempt_enabled_gates` 覆盖面重叠, 不另立条目。

---

## Cross-references

- **两份 spec**: `openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` (563 行前身 v7) · `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` (563 行, v6)
- **决策单**: `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md`
- **审计报告**: `.aria/audit-reports/post_spec-R{1..5}-*-handoff-multibranch-subdir-path-fidelity-*.md` (30 份) · `…-pre-merge-completeness-gate-change-scope-*.md` (30 份)
- **rework 记录 (scratchpad, 非持久)**: `/tmp/claude-1000/-home-dev-Aria/b455927b-db31-4765-a7d8-7736e5cad6d3/scratchpad/{handoff-multibranch-subdir-path-fidelity,pre-merge-completeness-gate-change-scope}-rework-R{1..5}.md`
- **issue**: [Aria#195](https://forgejo.10cg.pub/10CG/Aria/issues/195) · [Aria#199](https://forgejo.10cg.pub/10CG/Aria/issues/199) · [Aria#200](https://forgejo.10cg.pub/10CG/Aria/issues/200) (triaged 22421) · [aria-plugin#161](https://forgejo.10cg.pub/10CG/aria-plugin/issues/161) · [aria-plugin#169](https://forgejo.10cg.pub/10CG/aria-plugin/issues/169) (活体复现 22609)
- **前序 handoff**: [2026-09-09 (同伴, 会话收尾)](./2026-09-09-session-close-three-review-rounds-and-two-self-inflicted-gates.md) · [2026-09-06 (本容器, 会话收尾)](./2026-09-06-session-close-v1.70.0-shipped-170-closed-195-199-triaged.md)
