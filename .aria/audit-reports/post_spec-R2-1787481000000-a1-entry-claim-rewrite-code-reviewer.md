---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-23T11:29:50.000Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 (重写 v2 + C1/C2 落版) — code-reviewer

> **席位**: code-reviewer · **处置**: **REVISE** (frontmatter `verdict` 按 `verdict-format.md` 机械映射填 `FAIL` —— 1 条 R1 Critical 仍开; post_spec `blocking: false`, 仅记录不阻断)
> **scope_ok**: true
> **counts (本席)**: critical=**1** (R1 still-open) · major=**15** (R1 still-open 10 + 新 5) · minor=**10** (R1 still-open 4 + 新 6)
> **审查视角** (与 R1 同): 欠定检测 + 条款交叉一致性 + 事实断言逐条实读。

## 审计对象与工作树

| 项 | 值 |
|---|---|
| 主仓 HEAD | `1205ec3` (master); 被审 `proposal.md` 为**工作树未提交版** (474 行, md5 `04a62a9f1920`), 相对 HEAD `86540f2` +123/−42 (= rework 第 3 轮) |
| aria 子模块 | 工作树 `cb6bd5d` (分支 `fix/issue-batch-149-151-155-134`, #149/#151/#155 并行在改, 与本 Spec 引用文件无交集 —— 已核: 改动集为 state-scanner `collectors/{architecture,audit,handoff_multibranch}.py` / `renderers/track_board.py` / 两份 references / tests, 不含 `lib/*.py` `phase1_gate.py` `release_gate.py`) |
| `origin/master` | `ca52d1c` (v1.67.0, 2026-08-23T09:14:07Z, `feature/linked-issue-normalization` 已合入; `merge-base --is-ancestor` 实测成立) |
| 实读范围 | Spec 全文 17 条清单断言 + §4 未入清单的 5 处引用 + `git show 86540f2` 两段 owner 裁定原文 + 语料 147 篇 |

## 判定

**REVISE — 未收敛。** 本轮 Spec 新写部分 (C1/C2 落版、请复议段、事实清单) 质量明显高于 R1: **17 条清单断言逐条实读全部成立**, 两段 owner 裁定经 `diff` 与 `86540f2` 逐字一致, 三处「请 owner 复议」上呈内容本身事实正确 (gc.py:341 默认 `SWEEP_TTL` / release_gate.py:141 未传覆盖 / 两 AB 套件各 2 eval 实存)。

但**R1 的 major 簇绝大多数未处置**: 聚合报告 10 个 major 簇里 **9 条原样开着**, R1 本席 9 major 里 7 条开着; 而 Spec `:470` 与 `:451` 自述「R1-fix 已全量吸收」。R1/C3 (字段抽取) 只订正了事实、机制本身被 Spec 自己宣告「现有措辞不足以实现」并移交 A.2, **未入「请 owner 复议」段** —— 保持 Critical。C2 落版的 (ii)/(iii) 两段各引入 1-2 条新 major (输入欠定 / 「无条件」与 §2.5 互斥 / `STALE_TTL` 消费者漏查)。

## R1 finding 逐条 closed / open

### 聚合报告 critical 簇 (5+1)

| R1 | 状态 | 证据 |
|---|---|---|
| C1 allowed-tools | ✅ **closed** | owner 采 (a); Impact `:421`/`:423` 逐字前后值; 实读 `phase-a-planner:9` / `spec-drafter:10` 与「变更前」列一致 |
| C2 heartbeat 谁调 | ✅ **closed (谁调已定)** → 落版引入新 major R2-CR-M1/M2/M3 | `--heartbeat-only` + 编排层挂载 + SC-20/21 |
| C3 字段格式 0/13 | ❌ **still-open, Critical** | 见 R2-CR-C1 |
| C4 `_TERMINAL` 事实 | ✅ 事实订正 closed → **残余 Major** R2-CR-M5 (`unknown` 处方不可达) | `:180-182` |
| C5 D6 跨容器断言 | ✅ **closed** (残余 minor R2-CR-m4: D6 依据格未随动) | `:172` 订正准确 (实读 `release_gate.py:225` / `gc.py:341`) |
| C6 `include_terminal` 第 0 段 | ✅ **closed** | `:186` + Impact `:415`; 实读签名三参数 (cb6bd5d:177-181 / origin/master:230-234) |

### 聚合报告 major 簇 (10) + 「另」4 条

| R1 | 状态 | 证据 |
|---|---|---|
| M1 归一职责真空 | ⚠️ **外部事件 closed, Spec 未随动 (minor)** | 姊妹 D9 已导出 `normalize_linked_issue()` (`origin/master:178`); §2.1 `:117` 仍只写「经前置 Spec 归一」不点名函数 |
| M2 §5 放弃必 release × §2.1 无 slug 连坐 | ❌ **still-open** | `:264` / `:113` 一字未动; `release_claim_by_track` 仍释放全部匹配 (`claim_lifecycle.py:398-401` docstring「ALL matching」) |
| M3 §4 探针「同 issue」谓词未定义 | ❌ **still-open** | §4 `:240-258` 无匹配谓词; `无` 归属 (editlist FIX-10) 未落 |
| M4 进模板只做一半 (standards 模板 SOT) | ❌ **still-open** | Impact 无 `standards/openspec/templates/proposal-minimal.md` |
| M5 `:1229` 门控 + §6 缺口表漏最大项 | ❌ **still-open, 且新增内部矛盾** | `:103` 逐字「该已知限须写进 §6 缺口表」, 而 §6 `:270-275` 仍是原 4 行 —— Spec 自己宣称要做的事没做 |
| M6 `:1235-1237` `except → []` 真实落点 | ❌ **still-open** | §2.5 `:199` 只治 `GateResult.error`; 实读 `:1235-1237` 不变 |
| M7 §4 只扫默认分支 ⇒ in-flight 不可见 | ❌ **still-open** | `:256` / `:258` 盲区声明未勘正 |
| M8 §3 双落点 SC 零覆盖 | ❌ **still-open** | 仅加了 `### B.0` 非实存锚点注 (`:109`); 无结构化 SC |
| M9 SC-9/SC-14 标「代码」实测对象是散文 | ❌ **still-open** | `:367` / `:377` 未改 |
| M10 SC-8/SC-10 捆绑 CLI 字段与措辞 | ❌ **still-open** | `:366` / `:368` 未改 |
| 另·`coordination.enabled` 未在 `DEFAULTS.json` 注册 (CR/M8) | ❌ **still-open** | 实读 `DEFAULTS.json` 仍无 `coordination` 键; Impact 无该文件 |
| 另·SC-1 无分支限定 (CR/M1) | ❌ **still-open** | `:354` 逐字「slug 改名前后 track-id 不变」无限定 |
| 另·§2.3 强制请裁 × AD10 / Layer 2 未定义 (CR/M5) | ❌ **still-open** | §2.3 `:174` 无无人值守分支 |
| 另·KM `session-handoff.md` / `coordination-ref-schema.md` 未入 Impact | ❌ **still-open (minor)** | Impact 表无两文件 |

### 本席 R1 其余 (不在聚合簇内)

| R1 | 状态 |
|---|---|
| CR/M2 §2.1 三段拼接无代码落点 (SC-1/SC-4 无被测对象) | ❌ still-open — Impact 仍无 compose 函数行, §2 模板仍让 AI 手写串 |
| CR/M3 §2.2「改」匹配键 × Impact「增并存变体」两读 | ❌ still-open — `:130` / D4 `:317` 仍「改」, Impact `:413` 仍「增」 |
| CR/M4 终态可见后 §2.3 选项集未随动 (恒提示) | ❌ still-open — `:170` 三选项不变, 无 status × 处置矩阵 |
| CR/M6 §4 无 stdout 契约 + 无远端恒非 0 | ❌ still-open — `:257` / SC-18 `:381` 不变 |
| CR/M9 §1 回声只落主仓 | ❌ still-open (并入 M4) |
| CR/m1 裸 `(:210)` 指针 | ❌ still-open (`:199` 仍裸) — minor |
| CR/m2 `derive_track_id` 超长 sha 替换未说明 | ❌ still-open — minor |
| CR/m3 §4 插入点两套编号未定名 | ❌ still-open — minor |
| CR/m4 本 Spec 缺「关联 Issue」字段 | ❌ still-open — `:3-8` 仍无 (姊妹 `linked-issue-normalization:6` 已补, 本 Spec 未补) — minor |
| CR/m5 `error` 单槽位优先级 | ❌ still-open — minor |
| BA/minor `release_gate.py --status abandoned` 缺 `--raw-track-id` | ❌ still-open — `:264` 仍省略 (实读 `:236-237` 为必需三选一) — minor |
| TL/minor `layer-l-integration.md:45` `update_heartbeat()` 不存在 | ❌ still-open — Impact `:427` 未点名; 实读 `:45` 仍引该不存在函数 — minor |
| KM/minor S3 `identity.py:244` 误差 | ✅ closed — 清单 #11 已给 `:242` |

> **计数口径**: 上表 still-open 的 R1 项在本席 counts 中按 **去重后** 计: critical 1 (C3) · major 10 (M2/M3/M4/M5/M6/M7/M8/M9/M10 + CR-M1/M5/M8-DEFAULTS 合并计 1 簇「另」) · minor 4 (CR/m4 dogfood · BA `--raw-track-id` · TL `:45` · KM Impact 两文件)。CR/M2/M3/M4/M6 与聚合簇有重叠, 不重复计数。

## 本轮新 findings

| id | severity | category | scope | title | evidence | 处方 |
|---|---|---|---|---|---|---|
| **R2-CR-C1** | Critical (R1/C3 still-open) | mechanical-check-viability / rule10-process | `:71-79` (§1.2-1.4) · SC-13 `:376` · Impact `:429` | §1「抽取规则」被 Spec 自己宣告「现有措辞不足以实现」并移交 A.2, **未入「请 owner 复议」段**; check 作用域 / `无` 判据 / 多 issue 三项仍未定义 ⇒ R1 的「上线即恒红 = 零信息」原样存在 | 本席实跑 147 篇语料 14 条字段行: Spec 候选正则 `[\w.-]+/[\w.-]+\s*#\d+` 仅救 **4/13** (`无` 除外), 9 条落空样本全为 `Forgejo [#134](…)` / `aria-plugin [#95](…)` / `[aria-plugin #137](…)` 形 (无 `org/` 段或被 `[` 隔开); 姊妹已 ship 的 `normalize_linked_issue` (`origin/master:178`, `rsplit("#",1)`) 对 markdown 链接形同样返回 `None` ⇒ 「直接喂归一 OK=0」在 v1.67.0 上复现。`:71` 仍写「单一形态」与 `:72`「抽出的 token」并存未调和; `:79` 仍写 128 篇豁免而对会被判红的 13 篇零表态; check 作用域全文未定义 | (1) 抽取规则写回 Spec 钉到字符级 (先剥 markdown 链接语法再套 org-可选正则, 本席同语料实测可达 12/13); (2) `:71` 二选一消除「单一形态」×「抽出 token」并存; (3) 定 check 作用域 (建议仅 `openspec/changes/`) + 存量 13 篇处置; (4) 若仍要 defer, 把 defer 本身列入「请 owner 复议」并在 §6 记「§1 回声在规则定前不可上线」 |
| **R2-CR-M1** | Major | spec-underdetermination | `:148-150` (§2.2 (ii)) · SC-21 `:391` · Impact `:418` | `--heartbeat-only`「只刷新**本容器本 track**」—— **track 从哪来未定义**; 且 SC-21 用「**本会话**持有 active claim」作触发谓词, 而 claim 以 `(container, session)` 键控、每个 subprocess 都是 FRESH session (`claim_lifecycle.py:387-393` docstring 自陈), 「本会话持有」跨 subprocess **不可判定** | 两实现者分叉 (输入 X = A.1 认领后隔天新 session 跑 `/state-scanner`): **A** 要求 `--heartbeat-only --raw-track-id <串>` ⇒ 编排层必须从 handoff/记忆里找回 A.1 原串 ⇒ 回到「依赖 AI 记性」, 正是 (ii) 要消灭的; **B** 不带 track, 刷新本容器**全部** active claim ⇒ 任何被遗忘未 release 的 claim 只要该容器还在做别的事就**永不 stale、永不被 sweep** (僵尸 keep-alive), 与 §5「各自显式 release」+ SC-7 的设计意图相反 | 钉死输入来源: 推荐「按 `container` 刷新全部 active claim」并**成文承认**僵尸 keep-alive 代价 + 在 §5 把「未 release 即悬挂」升为义务; 或钉「A.1 原串持久化到 `.aria/` 本地文件, `--heartbeat-only` 读它」。SC-21 谓词改「本**容器**」 |
| **R2-CR-M2** | Major | clause-contradiction | `:150` (§2.2 (ii)「无条件」) × `:198` (§2.5) × SC-9 `:367` | (ii) 逐字把 B-entry 的条件写成「`coordination.enabled==true` 且 collision.kind 非空」, 再说 heartbeat 是「**无条件**」—— 字面包含 `enabled` 也不看; 而 `--heartbeat-only`「复用既有 identity/fetch/push 管道」⇒ opt-out 项目每次 `/state-scanner` 都 fetch/push coordination ref | 两读: A 读「无条件」= 不看 collision 结果但仍受 `enabled` 门控; B 读字面 = 不看 `enabled` ⇒ 对未配 coordination ref 的第三方每次扫描产生 §2.5 自己点名的「外向副作用」。SC-9「`enabled==false` ⇒ 零调用」测的是 A.1 acquire, 对 heartbeat-only 路径**无断言** | (ii) 改写为「在 `coordination.enabled==true` 前提下无条件 (不依赖碰撞结果)」; SC-9 加一臂「`enabled==false` 时 `/state-scanner` 不调 `--heartbeat-only`」 |
| **R2-CR-M3** | Major | impact-analysis-incomplete / fact-assertion | `:155` `:161` (「`STALE_TTL` 实际控制的是 `reconcile._is_stale()`」) · Impact `:416` `:419` · 非目标 `:402` | `STALE_TTL` 的消费者**不止** `_is_stale()`; 改 30min→24h 还改变: (a) `renderers/track_board.py` `_freshness_status` 的 🟡/🔴 分档 (工作树 cb6bd5d `:289`; `origin/master` `:234` —— 该文件在 #149/#151/#155 批里有 in-flight 改动, 但此消费点两版都在) —— `/state-scanner` 看板上「🔴 abandoned? 可接管」从 30min 推到 24h (用户可见输出变更, Impact 零覆盖); (b) `phase1_gate.py:283-295` `_takeover_eligible` 经 reconcile `+stale_takeover_eligible` 消费 `STALE_TTL` ⇒ **Phase B 入口** 7c 分支 (`:650-652`) 的「occupied / takeover-eligible」判定窗从 30min 变 24h (advisory_surface kind 与 `takeover_eligible` 输出字段随之变) —— 撞 §非目标「不动 Phase B 入口现有认领」; (c) 既有测试硬钉: `test_reconcile_golden_table.py:438` `assertEqual(STALE_TTL, 1800)` **必红**, `test_release_by_track.py:409` `assertGreater(7200, STALE_TTL)` **必红**; (d) 文档 `coordination-ref-schema.md:198` `STALE_TTL=1800` / `phase1_gate.py:525` 注释 | 全仓 `grep -rn STALE_TTL` 实测 (excluding constants.py): `track_board.py` 4 处 (cb6bd5d `:100/128/143/289` ↔ origin/master `:78/106/121/234`), `phase1_gate.py:525`, `reconcile.py:48/163`, 两 test 文件 5 处断言, `coordination-ref-schema.md:198`, `lib/__init__.py` 导出 | (1) `:155` 事实断言补全消费者清单; (2) Impact 补 `track_board.py` (分档语义) + 两个既有 test 文件 (钉值须改) + `coordination-ref-schema.md:198`; (3) 非目标 `:402` 加限定「`STALE_TTL` 变更会改 Phase B 7c 的 takeover 窗, 属已知副作用, 非目标条款仅指 `include_terminal` 默认值」—— 或把 (b) 列入「请 owner 复议」 |
| **R2-CR-M4** | Major | self-description-accuracy | `:3` (Status) · `:451` · `:470` (闸门状态 #2「R1-fix 已全量吸收」) | Spec 三处自述「R1-fix 已全量吸收」, 实际聚合报告 10 major 簇 **9 条未动**, R1-fix editlist 的 FIX-03/06/07/08/10/12/13/14/15/16/17/19 均未落 (见上表) | 本报告「R1 finding 逐条」表 | 改为如实表述:「R1-fix 吸收 C1~C6 事实订正 + NEW-01; major 簇 M2~M10 及『另』4 条**待下一版**」; 闸门状态 #2 同步。owner 批准前读到「全量吸收」会误判收敛度 |
| **R2-CR-M5** | Major | unreachable-prescription (R1/C4 残余) | `:182` (§2.4 `unknown` 处置) · SC-8 `:366` | §2.4 规定「`unknown` 命中时须按『未能核实对方状态』呈现」, 但 `unknown` **结构性不可能命中** `linked_issue_overlap[]`: `parse_claim` 的 sentinel 分支 (`claim_schema.py:212-230`) 不传 `linked_issue` ⇒ dataclass 默认 `None` ⇒ `collision.py` (origin/master `:273`) `if not getattr(c, "linked_issue", None): continue` 在 `_TERMINAL` 之后**第二道**丢弃, 与 `include_terminal` 无关。§2.4 把 skip 全归因 `_TERMINAL` 是**不完整的事实断言**; 处方无任何 SC 钉住 (SC-8 场景列只有 done/abandoned/yielded) | 实读 `claim_schema.py:219-229` sentinel 全字段空串、无 `linked_issue`; `collision.py:271-275` 两道过滤 | 二选一成文: (a) `unknown` 走独立 additive 键 (editlist FIX-03 方案, 仅 `--include-terminal` 时出现, 保 Phase B 输出逐字节不变) + 补 SC; (b) 明写「`unknown` 在本通道不可见, 属已知限」并从 §2.4 处方删去「命中时」措辞 |
| **R2-CR-m1** | Minor | sc-bound | SC-20 `:390` | `STALE_TTL >= 86400` **无上界** ⇒ 允许 `STALE_TTL > SWEEP_TTL`, 此时 claim 会先被 `--sweep-stale` **不可逆**判死、再被 reconcile 标 advisory-stale —— 软信号晚于硬动作, 与 `constants.py:37-42` 注释的排序前提相反 | — | SC-20 加 `STALE_TTL <= SWEEP_TTL` 断言 (或钉等值) |
| **R2-CR-m2** | Minor | number-consistency | `:77` (129) vs `:79` / `:405` (128) | 同文两套「存量无字段」数字: R1-fix 块用 TL/CR 口径 129 (141−12), §1.4/非目标用 S4 口径 128 (141−13); editlist FIX-06 曾点名此形状。另: 本轮语料已 147 篇 / 14 条字段行, 三数皆陈旧 | 本席 `find`/`grep` 实跑 | 统一口径 + 加「可一条命令复核」注 |
| **R2-CR-m3** | Minor | fact-list-completeness | `:281-306` 清单 | 清单自称「逐条列出 Spec 全文引用的 `文件:行号`」, 但 §4 的 `audit-engine/SKILL.md:85` / `execution-modes.md:84-111`/`:113-144` / `DEFAULTS.json:124-128` / `remote_refresh.py:691` 与 §2.2 的 `constants.py:43-44` / `gc.py:361-363` 均未入表 | 本席已复读: 5 处 §4 引用在 cb6bd5d 上**全部成立** (非缺陷, 仅清单不自洽) | 补入或把清单范围声明改为「§1-§3」 |
| **R2-CR-m4** | Minor | decision-table-drift | D6 `:319` | `:172` 已订正为「只有无差别 sweep, 没有定向 release」, D6 依据格仍写「S3 实测无该函数」 | — | D6 依据改「无**定向**释放函数; `--sweep-stale` 属无差别 GC」 |
| **R2-CR-m5** | Minor | stale-coordination-text | `:187` (§2.4 item 0 blockquote) | 仍写「该协调项须 owner 确认」; 姊妹 `linked-issue-normalization/proposal.md:255` 已逐字「`include_terminal` 形参由 `a1-entry-claim` 引入 (owner 裁定 2026-08-08)」—— 协调项早已由 owner 在姊妹侧关闭, 本 Spec 下一段「已解」只讲合并与签名未改, 未引这条授权 | 实读姊妹 `:255-257` | 删「须 owner 确认」句, 改引姊妹 `:255` |
| **R2-CR-m6** | Minor | cost-disclosure | `:148` (ii) | `--heartbeat-only`「复用 fetch/push 管道」⇒ 每次 `/state-scanner` 新增一次双远端 fetch (S2 实测 ~13.8s) + push; §4 探针的同量级代价被 Spec 要求「不得称轻量」, 本处未做同等披露 | S2 `:250` | 补一行代价 + 是否复用 `/state-scanner` Phase 0.5 的 fetch |

## 经本轮实读确认**成立**的新写部分 (下轮免重复)

1. **事实断言清单 #1-#17 全部成立** (逐条实读 cb6bd5d + origin/master): allowed-tools 两行 / `_TERMINAL` 两处同名 (`:210`/`:307` ↔ master `:268`/`:366`) / 签名三参数 / `:207-208` `:219-220` / `:1233` 调用处 / `heartbeat` `:178` / `release_claim_by_track` `:377` docstring `:387-393` / `:425` / `identity.py:191`/`:222`/`:242` / `phase1_gate.py:210` + `:475` / `constants.py:28`/`:32`/`:36`/`:51` / `gc.py:341` 默认 `SWEEP_TTL` / `release_gate.py:141` 未传覆盖 / `reconcile.py:154-163` / `release_gate.py:225` + `state-scanner/SKILL.md:176` + `phase-d-closer/SKILL.md:56` 三处 `STALE_TTL` 误写 / `SKILL.md:149` + `layer-l-integration.md:15` / `_run_gate_impl` `:335`-`:1032`;
2. **两段 owner 裁定逐字一致** (`diff` 对 `git show 86540f2` `:150` / `:214`, 零差异);
3. **三处「请 owner 复议」上呈内容事实正确**: (iii) 理据矛盾 (sweep 阈值确为 `SWEEP_TTL`) / Rule #6「申报 benchmark」读法 / 两套件实存各 2 eval (`aria-plugin-benchmarks/ab-suite/{phase-a-planner,spec-drafter}.json` 实核; `state-scanner.json` 存在, `880060d` 在 aria 子模块实存);
4. **NEW-01 (`无` truthy 误报) 在 v1.67.0 上仍成立**: `normalize_linked_issue('无')` → `None` → 回退原串相等比较 → 两个 `无` 仍互相命中;
5. **`ca52d1c` diff --stat 订正准确** (9 文件, 一个 test 文件, 不含 `gc.py`/`constants.py`);
6. **`phase-d-closer/SKILL.md:52` 逐周期带 `--sweep-stale`** 属实, `:173` 的「不是理论风险」成立。

## scope_ok

**true** — 变更面仍严格落在自述范围 (A.1 认领前移 + 字段可得性 + 探针 + C1/C2 落版)。`STALE_TTL` 变更 (R2-CR-M3) 是 owner 裁定项, 其副作用溢出到 Phase B 入口属**未披露**而非**越界**。

## 一句话结论

新写部分的事实纪律达标 (17/17 断言实读成立、裁定原文逐字、复议点上呈正确), 但 R1 的 10 个 major 簇 9 条原样未动而 Spec 自述「全量吸收」, C3 的机制由 Spec 自判「不足以实现」移交 A.2 未上呈复议 (Critical 保持), C2 落版的 `--heartbeat-only` 输入来源与 `enabled` 门控欠定、`STALE_TTL` 消费者漏查 3 类 —— **REVISE, 未收敛**; 下一版应先逐条处置 R1 major 清单再进 R3。
