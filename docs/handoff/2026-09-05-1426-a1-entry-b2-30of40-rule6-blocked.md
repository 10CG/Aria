---
track-id: a1-entry-claim-duplicate-work-guard
owner-container: simonfish/023236f2
phase: B.2
status: active
updated-at: 2026-09-05T14:26:58Z
---

# Aria — Session Handoff (2026-09-05, 会话收尾) — 母 Spec B.1→B.2 推进到 30/40, Rule #6 AB 卡在会话级前置

> **一句话**: 本对话从 `/aria:state-scanner` 起 → 推送收口(守卫拦下并发提交 `94db971`, 多 track 合表后双推 MATCH)→ B.0 认领 → 母 Spec `a1-entry-claim-duplicate-work-guard` **B.1 + Group 2/3/4/5/6 共 30/40 任务落地**(三仓 15 个提交, 全 skill 套件 10 OK / 2078 tests)→ Group 7 的**套件编辑半**落地、**跑评测半阻塞于会话级前置**。
> **本 session 最该记住的一件事**: 我按 Spec 写完测试后**真跑了负控**, 于是逐个撞见了 Spec 自己写不成立的验收项 —— TASK-006 的夹具结构上恒绿、TASK-008 的注入手段 (a) 结构上做不到、TASK-013 的 verification 在它自己的时点不可满足、TASK-021 的「零命中」与守卫测试的存在互斥。**四处都不是读出来的, 是跑出来的。**

> **Status**: Active — cycle 未完成 (30/40), claim 保持 active 供下次接力; 三仓 15 个提交全部**未推**(外向, 待授权)
> **Session period**: 2026-09-05T07:17Z (state-scanner 入口) → 2026-09-05T14:26Z
> **Next session 入口**: 优先读本 doc → §6

---

## §0 入口 (新 session 优先读)

1. 三仓都在 **feature 分支**上, 且**都未推**: 主仓 `feature/a1-entry-claim-duplicate-work-guard` @ `5697477` (origin 停在 `fadb111`, 落后 7) · aria 同名分支 @ `ab3dbd0` (两端皆无该分支) · standards 同名分支 @ `bb5d375` (同上)。`git status` 应见 ` M aria`, ` M standards`, ` M aria-orchestrator` 三个 dirty 子模块 —— **全部有意**, 不要 `git add`(gitlink bump 归 TASK-038/8.2, 要等各自合 master 之后)。
2. **本 session 的 claim 仍 active 且 heartbeat 冻结在 `10:25:37Z`** —— 认领后没刷过。SWEEP_TTL 24h ⇒ **2026-09-06T10:25Z 之后会被 sweep 成 abandoned**。这正是本 Spec 要治的病, 而治它的 `--heartbeat-only` 本 session 刚实现、编排层还没接上(TASK-020 只落了文档)。下次 session 进 `/state-scanner` 时按新文档跑一次 `--heartbeat-only` 即可, 顺带 dogfood。
3. **Rule #6 AB 未跑, 且不是豁免** —— 见 §2 H1 与 §3 第 1 条。发版 (Group 8) 按 Spec 排在 AB 之后, **不要跳过 AB 直接发版**。
4. 硬约束不变: 子模块推送须 owner 逐条授权; 禁带圈数字 (memory `no-tiny-glyphs`)。
5. 多 track: 本仓另有 `aria-runner-bot/bfe8285d` 的 M6 轨在飞(门在 owner/基建), 见 `latest.md` 看板。

---

## §1 已完成 (本对话, 按时间顺序 UTC)

| 时间 | 事项 | 落点 |
|------|------|------|
| 07:17 | `/aria:state-scanner` 全量扫描 → 10 区块报告 + 4 选项 | — |
| 07:2x | owner 选**选项 1**。推前 ancestry 守卫**拦下并发提交** `94db971`(另一容器 M6 轨) → `latest.md` 三处冲突按多 track 逐处合表(先写预期再实测, 四项全中)→ rebase → 双推 → 逐 remote `ls-remote` **`788fac8` MATCH** | 主仓 master |
| 07:3x | B.0 `phase1_gate` 认领 `a1-entry-claim-duplicate-work-guard`(`outcome: passed`, `surface: null`, push ok) | `refs/aria/coordination` |
| 07:4x | **B.1**: 主仓 + aria 建 feature 分支; Group 1 三项前置断言(TASK-001/002/003)—— **零真漂移**, 决策单 C8 接缝担忧证伪 | `fadb111` |
| 08:xx | TASK-004 + **011** `get_container_uuid()`(5 用例 + 2 负控) | aria `4b75921` |
| 09:xx | TASK-005/006 + **012** `heartbeat_by_track()`(12 用例 + 6 负控)—— 发现 TASK-006 夹具恒绿并补 | aria `0ae207f` |
| 10:xx | TASK-007 + **013** `include_terminal`(分支进入设计中的 TDD 红态) | aria `4465fca` |
| 11:xx | TASK-008 + **014** + **015**: `--include-terminal` / `unknown_schema_claims` / `fetch_degraded` —— **红态关闭** | aria `a0d4a6c` |
| 12:xx | TASK-009/010 + **016** `--heartbeat-only` 模式 + carry-id 往返守卫 | aria `9c00aa5` |
| 13:xx | **Group 5 + Group 6** 14 条: 两个前置块 / carry-id 三处措辞 / state-scanner 与 layer-l 文档 / config 三键 / schema §3.2 / standards §2.3.8.1 + 六条结构化断言 | aria `ab3dbd0` · standards `bb5d375` |
| 14:xx | **Group 7 套件编辑半**: 7 条定向 fixture + `version.yaml` 程序化重算; 跑评测半判定阻塞并成文 | `5697477` |
| 14:2x | 会话收尾(本 doc) | — |

**规模**: 三仓 15 个提交 · 30/40 任务 · 全 skill 套件从 2012 → **2078 tests**(state-scanner 1476 → 1542)· 全程 10 OK / 0 FAIL。

---

## §2 未完成 / Carry-forward

> cycle **未完成**(30/40)。以下 H1/H2 是本 cycle 的剩余工作, M 段是溢出到别处的。

### 高优先级 — 本 cycle 剩余 10 条

| # | 项目 | 状态 |
|---|------|------|
| **H1** | ⛔ **Group 7 跑评测半 (7.1/7.2/7.4 + 7.3·7.5 后半)** —— 阻塞于会话级前置, 见 §3 第 1 条。**处置 = owner 以 `ARIA_COORDINATION_NO_PUSH=1 claude ...` 重启会话后, 经 `/skill-creator` 跑六个套件**(`phase-a-planner` / `spec-drafter` / `state-scanner` / `phase-b-developer` / `branch-manager` / `phase-d-closer`), 结果落 `ab-results/2026-XX-XX-v1.70.0-a1-entry-rule6/<skill>/`(每个目录跑前先写 `PREDICTION.md`)。跑完**必做**手册第 3 条 `git fetch origin +refs/aria/coordination:refs/aria/coordination` | 阻塞 |
| **H2** | 7.6 套件缺口 issue(aria-plugin, 标题与正文要点见 TASK-036 verification; 交叉引用 #117/#127 且**不归并**) | 外向待授权 |
| **H3** | Group 8 发版四条: 8.1 CHANGELOG + 版本 SOT 5 文件(**`<vNEXT>` = `1.70.0`**, MINOR 已由决策单 §H1 裁定)→ 8.4 aria 本地 merge + 双推 + 逐 remote 核验 + tag → 8.2 主仓 16 版本点 + gitlink bump → 8.3 follow-up 开单。**执行序 8.1 → 8.4 → 8.2**(编号不代表顺序) | 待 AB 过关 |
| **H4** | 三仓 15 个提交**全部未推**; standards 与 aria 的 feature 分支两端都还没有 | 外向待授权 |

### 中优先级 — 溢出项

| # | 项目 | 备注 |
|---|------|------|
| M1 | **8.3 的 follow-up 开单 (Impact #1–#7)** —— 机械 backstop 补漏出来的, 我内省时漏了 | `owner-container` 口径 / `SWEEP_TTL`→`STALE_TTL` 三处措辞 / `unknown_schema_claims` 路径 / B.0 YAML-键形态 / `unattended` Layer 1→2 env 三腿 / 跨容器定向 release / `ClaimRecord` swept 标记 |
| M2 | **`issue_scan.open_count` 静默截断** —— 扫描阶段实测: config `limit=20`, `open_count = len(items)`, `warning` 只覆盖 `stage_timeout` ⇒ repo 开放 issue >20 时恒报 20 且零截断标记。实测 Aria 24 / aria-plugin 34, 合计 63 而非报的 45 | 未开单; 与 #182/#173「证据越少越宽松」同族 |
| M3 | **Spec 正文的行号引用未同步** —— 本 cycle 三处锚点位移只回写了 `tasks.md` 的行号复核表, `proposal.md` 正文里引的 `phase1_gate.py` / `collision.py` 行号仍是 d69091d 口径 | 归档前应扫一遍 |
| M4 | **四处 Spec 验收项不成立已记 notes, 但 Spec 原文未改** —— TASK-006 夹具恒绿 / TASK-008 注入手段 (a) / TASK-013 verification 时序 / TASK-021「零命中」。建议 Group 4/7 复核时逐条订正 yaml 文字 | 见 §3 第 2 条 |
| M5 | 上轮原样: Aria#192 真修 / AB 套件断言补强 / Aria#182 类级修 / `.aria/repro/` 测试不在任何 gate 路径 | 09-05 前一份 handoff §2 |

### 机械补漏 (autofill backstop, AI 内省未提及)

- `handoff_autofill.py` 从 tasks.md 汇编出 **8.3** 那条(已升为上表 M1)。其余 unfinished 项与我的内省逐条吻合。
- `consistency_check.py`: 7 条 `active_change_not_in_upm` advisory —— UPM 未配置导致的恒亮 flag, 与本 session 无关。

---

## §3 关键风险 / 已知陷阱

1. **⛔ AB 运行前置是会话级的, 在会话内补不上。** `AB_TEST_OPERATIONS.md` §场景 1 第 1 条要求会话**以** `ARIA_COORDINATION_NO_PUSH=1 claude ...` **启动**(subagent 继承会话 env)。本会话未带该变量启动(纯 shell 判空实测); 会话内 `export` 只影响那一个 Bash 子进程, 改不了 subagent 的继承环境。硬跑的后果成文且有实证: 被测 Skill 会把**合成 claim 推到生产 `refs/aria/coordination`**(2026-08-02 `postspec-r1-delete-me-a1-entry-claim-audit-test` 落到过远端)。**这不是 Rule #6 豁免** —— 本批改了 `allowed-tools`(能力面扩权), 照跑档不变, 只是执行条件不具备。
2. **Spec 的验收项有四处结构上不成立, 都是跑出来的不是读出来的。** 逐条已写进 `tasks.md` 与 yaml `b2_evidence`, 但 **Spec 原文未改**:
   - TASK-006: 要求第三方 claim「与旧/新不共享任何前缀后缀」又要它在「去掉 container 合取」时变红 —— `track_id` 走精确相等, 二者不相容 ⇒ 该断言**恒绿**。已**只增不改**地补了「容器 B 中同 track_id」夹具。
   - TASK-008: 三个注入手段里的 (a)「把 ref 指向非 tree 对象」**做不到** —— `read_claims` 通篇 fail-soft, 只进 `errors[]` 不抛。钉了 (c) 且须**按调用方栈帧限定**(`read_claims` 也被闸门自身调用)。
   - TASK-013: verification 第 1 条「TASK-007 的 SC-8 臂绿」在它自己的时点不可满足 —— SC-8 是 CLI 层断言, 需 TASK-014 的 flag, 而 TASK-014 反过来依赖 TASK-013。
   - TASK-021: 「`git grep update_heartbeat aria/` 零命中」与「存在一个断言该字面量不在文档里的守卫测试」互斥 —— 守卫自己必须含有它。
3. **TASK-014 的 yaml deliverable 与 SC-33 直接矛盾**, 已按 proposal 实现(三处 proposal 口径一致: SC-33 `:623` + Impact ④⑥ `:663` + §2.4b 四态表 `:340`)。建议 Group 4 复核时订正 deliverable 文字。
4. **`phase1_gate.py` 行号大幅位移且分区段非均匀**: 相对 `d69091d` —— `logger :61` 不动 / docstring +4 / `_run_gate_impl` +16 / 7a·7d·`_telemetry_path` +24 / `_gated`·`run_gate`·`_main`·两个 flag **+152**; 文件 1349 → 1566 行。`claim_lifecycle.py` 统一 +1, `collision.py` 统一 +13。**引用行号前先查 `tasks.md` 行号复核表**。
5. **claim heartbeat 冻结在 `10:25Z`**, 2026-09-06T10:25Z 后会被 sweep。见 §0 第 2 条。

---

## §4 实战教训 (memory 沉淀来源)

```
[候选 memory]
- 「规格里写好的验收项」与「我新写的检查」是两类东西, 但同一个判据管用: 没在基线上跑过就不知道它
  能不能红。本 cycle 四处 Spec 验收项结构上不成立, 全部是跑负控/跑基线时撞见的, 没有一处是读出来的。
  建议 type: feedback (与 check-runs-at-baseline-first 同族, 但对象是**别人写好的规格**, 不是自己新写的检查)
- 会话级前置(必须在进程启动时设定的 env)在会话内无法满足, 只能上报 —— 判据是「该前置是否作用于
  subagent 继承的环境」。这是一类新的阻塞形状, 与「缺权限」「缺凭据」不同: 它不可在当前进程内补救。
  建议 type: feedback
- `if p not in sys.path: sys.path.insert(0, p)` 这种守卫会**破坏插入顺序不变量** —— 当 runner 已把该
  路径放进 sys.path 时守卫跳过插入, 最终次序由「谁没被跳过」决定。两个同名包场景下报出的
  ModuleNotFoundError 与真因毫无关系。处方 remove-then-insert。建议追记进 ss-two-lib-pkgs
- 秒精度时间戳的「是否被刷新」断言不能依赖两次调用跨秒(常同秒 ⇒ 假红); 回拨初值比 sleep 好, 确定且不慢。
  建议 type: feedback (小条, 可并入既有测试类 memory)

[未写下经验]
- preserve-crlf 我这次是「查了一批就没查另一批」踩的 —— 前一步刚确认 config-loader 那批是 LF, 就对
  三个 SKILL.md 直接动手, 结果两个是 CRLF, 造成 2133 / 1862 行的整文件 diff。那条 memory 已经写着
  「编辑前查 HEAD 行尾」, 缺的是**逐文件查、不按批推断**这半句。应追记。
- 「Spec 的 deliverable 与 SC 矛盾时以 proposal 为准」这条在本 cycle 用了一次(TASK-014), 判据是
  proposal 的 SC 表 + Impact 表 + 契约表三处口径一致而 yaml 只有一处。与 derived-instruction-outranks-spec
  同族但更细: 那条讲「主控派生指令 vs 已收敛 Spec」, 这条讲「A.2/A.3 派生的 yaml vs proposal 正文」。
```

---

## §5 多维度同步状态

| 维度 | 状态 |
|---|---|
| OpenSpec | `a1-entry-claim-duplicate-work-guard` **30/40**, 仍 active(未归档, cycle 未完成) |
| UPM | 未配置 ⇒ `consistency_check` 7 条 `active_change_not_in_upm` 恒亮 advisory, 与本 session 无关 |
| User Story | 本 cycle 无 US 变更 |
| PRD / 架构 | 无变更(发版时 8.2 会动主仓 16 版本点与架构文档版本行) |

---

## §6 Next session 入口 + 优先级建议

```bash
/aria:state-scanner
```

1. ⭐ **`{id: a1-entry-claim-duplicate-work-guard}`** —— 本 cycle 续做。**先决**: owner 授权推三仓 15 个提交(H4), 以及以 `ARIA_COORDINATION_NO_PUSH=1` 重启会话跑 Rule #6 AB(H1)。AB 过关后才走 Group 8 发版(`<vNEXT>` = **1.70.0**)。
2. **`{id: carry-issue-scan-open-count-truncation}`** —— M2: `open_count` 静默截断(实测 63 vs 报 45), 开单或直接修。
3. **`{id: carry-a1-entry-spec-text-corrections}`** —— M3 + M4: Spec 正文行号同步 + 四处不成立验收项的文字订正, 归档前做。
4. **`{id: carry-spec-complete-symbol-extraction}`** —— 上轮 M1: Aria#192 真修(触归档 gate 极性, 单独一轮 + 审计)。

**不应该做的**: 不要在 owner 逐条授权外推任何仓; 不要跳过 Rule #6 AB 直接发版(照跑档, 非豁免); 不要 `git add` 三个 dirty 子模块(gitlink bump 归 8.2); 不要把 §3 那四处 Spec 缺陷当成「已修复」—— **代码侧绕过了, Spec 原文还没改**。

---

## §7 提交清单 (commit hash + multi-remote parity)

| Repo | 分支 | SHA | origin | github |
|------|------|-----|--------|--------|
| Aria (主仓) | master | `788fac8` | ✅ MATCH(本 session 已推并核验) | ✅ MATCH |
| Aria (主仓) | `feature/a1-entry-claim-duplicate-work-guard` | `5697477` | ⚠️ 落后 7(停在 `fadb111`) | ⚠️ 无该分支 |
| aria | `feature/a1-entry-claim-duplicate-work-guard` | `ab3dbd0` | ⚠️ 两端皆无该分支 | ⚠️ 同左 |
| standards | `feature/a1-entry-claim-duplicate-work-guard` | `bb5d375` | ⚠️ 两端皆无该分支 | ⚠️ 同左 |
| aria-orchestrator | `feature/m6-cost-model-telemetry` | `92acce5` | equal(停泊, 非本轨) | — |

> scan.py exit 10: AC-5 对 `github` 求值失败, 因该 remote 上不存在本 feature 分支 —— 正是已知的 **Aria #176**(AC-5 未排除本仓不存在的 remote), 非本 session 引入。

---

## §8 Memory entries this session (2 new + 2 追记)

| File | Type | Theme |
|------|------|-------|
| `feedback_spec_acceptance_criteria_need_baseline_run_too.md` | feedback | **新** — 已收敛 Spec 里写好的验收项同样会恒绿/不可满足; 判据同 `check-runs-at-baseline-first` 但对象是审过多轮的规格。本 cycle 4 处全靠跑负控才现形; 只增不改, 且「代码侧绕过」≠「规格修好」 |
| `feedback_session_level_precondition_cannot_be_met_in_session.md` | feedback | **新** — 须在进程启动时设定的前置 (env 传 subagent) 会话内补不上; 上报不绕过, 说清「非规则豁免, 是执行条件不具备」; 不依赖它的部分先做掉 |
| `feedback_preserve_crlf_when_scripted_editing.md` | feedback | 追记 — 缺的是「**逐文件**查行尾」这半句; 本次是**按批推断**踩的 (同目录同类文件行尾并不一致), 附 `newline=''` 处方与「diff 里出现内容相同的 -/+ 配对」这个早期征兆 |
| `reference_state_scanner_two_lib_packages_sys_path_order.md` | reference | 追记 — `if p not in sys.path` 守卫会**破坏插入顺序不变量** (`-m unittest` 下 cwd 已在 path[0] ⇒ root 那次插入被跳过, 次序反转), 症状是与真因无关的 ModuleNotFoundError; 处方 remove-then-insert |
| `MEMORY.md` | index | 24402 B (≤24576); 移 `forgejo-newbranch-no-run` / `nomad-docker-auth` / `hermes-plugin-loading` 三条窄条目入 archive 腾位; 零悬空指针 |

> §4 的「[未写下经验]」两条已在本轮落盘 (preserve-crlf 追记 + derived-instruction 同族的那条并入
> `spec-acceptance-needs-baseline-run` 的 How to apply)。

---

## Cross-references

- 上一份(会话收尾): `docs/handoff/2026-09-05-session-close-level1-batch-shipped-and-192-rescoped.md`
- 并行 track(M6, 另一容器): `docs/handoff/2026-09-05-m6-six-test-hardenings-landed-awaiting-submodule-push-auth.md`
- Spec: `openspec/changes/a1-entry-claim-duplicate-work-guard/`(`tasks.md` 含本 cycle 新增的三行「行号复核」与第 7 组阻塞说明)
- AB 运维手册: `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 1(三条前置/核验/清理)
- 决策单: `.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md`(§H1 = MINOR 档位)

---

**Created**: 2026-09-05 14:26Z
**Session duration**: ~7h 挂钟 (2026-09-05T07:17Z → 14:26Z)
**Status**: Active — cycle 30/40 未完成, claim 保持 active 供接力; 三仓 15 提交待授权推送
