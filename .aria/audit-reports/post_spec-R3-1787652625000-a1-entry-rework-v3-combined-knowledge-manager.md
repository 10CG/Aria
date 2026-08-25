---
checkpoint: post_spec
round: 3
role: knowledge-manager
verdict: REVISE
scope_ok: true
counts:
  parent(a1-entry-claim-duplicate-work-guard, R3): 0C/0M/1m
  child(linked-issue-field-availability, R1): 0C/2M/1m
  child(sibling-spec-probe, R1): 0C/0M/0m
combined_verdict: REVISE
---

# post_spec R3 (combined) — a1-entry-rework-v3 — knowledge-manager

## 审计对象与实读环境

```
git rev-parse HEAD  # 027a50f24e9309918af2d017824c34d6187e132a (工作树 aria-orchestrator 子模块 dirty, 与本审计无关)
git -C aria show d50f9c3:<path> | sed -n '<N>p'   # aria 基线, 全程使用
grep -c '^  - name:' .aria/state-checks.yaml       # 主仓基线
```
三份 proposal.md 全文通读 (母 734 行 / 字段 490 行 / 探针 523 行)。逐条对 ~35 处 `文件:行号` 断言做了独立实读复核 (aria @ `d50f9c3` + 主仓 HEAD)，覆盖 custom_checks.py / multi_remote.py / fetch_gate.py / remote_refresh.py / scan.py / report-format.md / execution-modes.md / DEFAULTS.json / audit-engine/SKILL.md / collision.py / coordination_probe.py / run_all_tests.sh / session-handoff.md / layer-l-integration.md / .aria/state-checks.yaml / ab-suite 各 json。

## R2 遗留 critical 复核 (C-B / C-C, 我上轮给的)

**C-B (连坐 release)** — 母 Spec §5.1「track-id 形态是否含 slug」二分谓词 + D12 + SC-27。三处逐字核对: §5.1(`:393-402`一带)/ SC-1(`:520`)/ SC-15(`:544`) 用的判据句**逐字相同**「track-id 形态是否含 slug」。**判: 已闭环。**

**C-C (carry-id 断链)** — 母 Spec §2.1b + D13 + SC-23 + Impact 表四行 (phase-b-developer/branch-manager/phase-d-closer/session-handoff.md)。**判: 实质闭环**, 但 Impact 表对 `session-handoff.md` 的section 引用有精度问题, 见下方 finding KM-1。

## 本轮新 findings

| id | severity | category | 定位 | 标题 | 证据 | 处方 |
|---|---|---|---|---|---|---|
| **KM-2** | **Major** | 跨 Spec 一致性 (SOT 与文档) | `linked-issue-field-availability/proposal.md:219-235`(尤其 `:230`/`:232`) vs `sibling-spec-probe/proposal.md:105-134`(`消解 SEAM-2`) | 字段 spec 关于探针 spec「BAD_TOKEN 无对应态」的叙事已对当前探针文本失真 | 字段 spec `:230/:232` 断言「⇒ **唯一实质差异 = `BAD_TOKEN` 在探针的三态契约里无归宿**」并称「归属由主控协调」。但**探针 spec 现文本已解决此项**: `:105`「**消解 SEAM-2** (主控 2026-08-25 核验)…下表逐格补全」+ `:111`(BAD_TOKEN 行: 层1∪层2 取并集) + `:120`「**选择: 层 1 与层 2 都跑, 取并集** —— 即**采纳姊妹席的建议**…并在其上追加一条…姊妹侧四态定义无需任何改动」。即探针 spec 不仅补上了这一格, 还**采纳并扩展**了字段 spec 自己给出的建议映射。字段 spec 的叙事描述的是探针 spec 的**已被取代版本**, 属同批次内的跨文档过期 (与母 Spec §Why 记载的「同批 fetch 后仍可能瞬间过期」同族, 只是这次是文档层面而非 git ref 层面) | 字段 spec §3 该 blockquote 段改写: 删「无对应态/需协调」的现状断言, 换成「探针 spec 已按本席建议扩展解决 (层1∪层2 取并集, 见 sibling-spec-probe `:105-134`), 本席核对一致, 无残留分歧」。同时删/改「新表面」#6 里「**该 Spec 由另一执笔席同批起草, 本席未与其交叉核对** ⇒ 若其最终定稿的返回形态不是三态, …须同批修订」——这句现在也是过期的 (探针定稿已是四态且已交叉核对过) |
| **KM-3** | **Major** | Rule #6 判据事实基线 | `linked-issue-field-availability/proposal.md:239`(`共 **10** 条 check`)/`:262`(`6+2+2=10`)/`:469` | D3 改判依据的「10 条 check / (iii) 类 2 条」计数在当前 HEAD 上已失真, 实测为 11 条 / (iii) 类 3 条 | 独立实跑 `grep -c '^  - name:' .aria/state-checks.yaml` = **11**（非 10）。逐条比对字段 spec `:242-259` 列出的 grep 输出（`issue-cache-freshness`…`plugin-cache-currency` 共 10 条）与当前文件: 缺失第 11 条 **`main-project-version-consistency`**（`:289`, `command: python3 .aria/probes/main-project-version-consistency.py`, 同属「(iii) 项目侧探针」形态）。`git log --follow -- .aria/state-checks.yaml` 确认该条由**同一 session 内**的提交 `2ae012f`（`simonfishgit 2026-08-25 01:27:17 +0000`，标题「fix(version): 主项目版本 SOT 核实...加机械检查防复发」）引入 —— 与本字段 spec 的落盘时间同日, 是并发轨在本轮审计对象之外新增的机械兜底。⇒ (iii) 类应为 **3** 条不是 2, 「也是最近两条新增」应为「最近三条」且顺序上 `main-project-version-consistency` 才是最新。**不影响 D3 的宿主改判逻辑本身**（(ii)/(iii) 并存的论证不因多一条 (iii) 而改变）, 但作为「本轮实核」的计数断言, 在本审计基线上不成立 | 重跑 `grep -c '^  - name:' .aria/state-checks.yaml`, 将 `:239/:262/:469` 三处「10」改为实测值并补第 11 条到 `:242-259` 的枚举列表与形态计数表; `:262` 括注补上 `main-project-version-consistency`。**顺带**: 其余两处「10」引用的语境（`:309`「既有 10 条 check 已在用的键」、`:469` 同句）若键集合本身不受影响则口径无需改, 仅数字要改 |
| **KM-1** | minor | 文档精度 (SOT 章节引用) | `a1-entry-claim-duplicate-work-guard/proposal.md:175,:213,:615` | carry-id `{id, desc}` 结构的 SOT 章节号引用过粗, 且恰好落在会引起混淆的相邻章节上 | 三处均写「`standards/conventions/session-handoff.md` §2.3 结构化 `{id, desc}`」。实读该文件标题结构: `:101` `## 2.3 机读 frontmatter schema`（讲 frontmatter, 5 字段）, 而 `{id, desc}` 结构实际定义在**子章节** `:217` `### 2.3.8 结构化 Carry-id schema (§6 prose 层, **非 frontmatter**, …)`。该文件自身在 `:238` 用一个专门小节强调「层归属: 留 §6 prose, 不进 frontmatter (**硬约束**)」——即 §2.3 与 §2.3.8 讲的是**两件对立的事**（前者是 frontmatter, 后者显式排除 frontmatter）。母 Spec 自己的 §2.1b 也依赖这条硬约束（carry-id 必须留 prose、禁止进 frontmatter）。笼统引「§2.3」而非精确到「§2.3.8」，在一处依赖「非 frontmatter」这一区分的设计文档里是不必要的精度损失 | 三处「§2.3」改为「§2.3.8」 |

## 经本轮实读确认成立的部分 (下轮免重复)

以下逐条实读，与三份 Spec 正文**逐字一致**，未发现偏差（下轮审计席可直接信任，无需重跑）:

- Impact 表完整性: 主控给定的三份 checklist（母: phase-b-developer/branch-manager/phase-d-closer 三处 SKILL.md + session-handoff.md + coordination-ref-schema.md + config-loader/SKILL.md + DEFAULTS.json + layer-l-integration.md；字段: proposal-minimal.md + spec-drafter/SKILL.md + state-checks.yaml + 新探针脚本；探针: audit-engine/SKILL.md + execution-modes.md + 新建 scripts/·tests/）**逐项核对，三份 Impact 表全部覆盖，无遗漏、无多余项**。
- `skills/state-scanner/SKILL.md:119` "Opt-in 子阶段: 1.11 custom_checks" —— 精确支持「custom check 由 Phase 1.11 执行」的判定。
- `collectors/custom_checks.py:63` "Minimal YAML parser" 自陈 —— 精确。
- `skills/state-scanner/references/layer-l-integration.md:15`（Design A 条件触发）与 `:45`（`update_heartbeat()` 悬空引用）—— 两处逐字精确；`git -C aria grep -n update_heartbeat` 全仓确认唯一命中即此行，真实函数名 `heartbeat()` 在 `lib/claim_lifecycle.py:178`。
- `skills/state-scanner/scripts/collectors/multi_remote.py:255`(`def resolve_enforced_remotes(configured, actual_remotes, read_only=())`) 与 `:286`（return 语句）—— 签名与范围精确。
- `skills/phase-d-closer/scripts/fetch_gate.py:50`(`_ORIGIN_HEAD_REFS`)/`:55`(`_DEFAULT_BRANCH_FALLBACKS`)/`:86`(`_classify_error`, docstring "Raw stderr is intentionally never returned" 逐字符合)/`:108`(`_resolve_default_branch`, docstring "no cross-skill runtime import" 逐字符合) —— 四处精确。
- `skills/state-scanner/scripts/collectors/remote_refresh.py:691`(`_write_cache_atomic` 调用点)/`:568`(`collect_remote_refresh` 定义) 与 `scripts/scan.py:312`（唯一生产调用点）—— 三处精确，支持"轮间无缓存保证"的论证。
- `skills/audit-engine/references/report-format.md:50-71` —— 精确且**无歧义**：文件内另两处 `## 轮次记录`（`:245`/`:296`）核实为**示例渲染**（填了具体数值的 PASS/FAIL 样例块），非并行模板，`:50-71` 是唯一真实模板，不存在「只 patch 了一份」的模板遗漏风险。
- `skills/audit-engine/references/execution-modes.md:84`(`## Convergence 模式`)/`:113`(`## Challenge 模式`) 与 `skills/config-loader/DEFAULTS.json:124-128`(`adaptive_rules.level_3 = "challenge"`) —— 三处精确，支持"两块都要改"的论证。
- `skills/audit-engine/SKILL.md:83-85`（Step 0 Anchor 固化，"Round 1 启动前一次性"）—— 精确，支持"不可复用该编号"的论证。
- `skills/state-scanner/lib/collision.py:46`(相对 import) 与 `scripts/coordination_probe.py:80-85`（"Deliberately NOT import lib.runtime_probe" + 指向 `collectors/openspec.py:29`）—— 两处精确，两种 sys.path 写法"各自都对"的论证站得住。
- `skills/run_all_tests.sh:48/50/71` —— 三处精确，"新建 tests/ 自动纳入套件"的委托声明（memory `delegate-verify` 要求的三件事：真做/方式合约/失败会红）经源码核实成立。
- AB 套件计数：`ab-suite/` 恰 **31** 个 `.json`；`phase-a-planner.json`/`spec-drafter.json`/`state-scanner.json` 的 evals 数分别为 **2/2/12**；`spec-drafter.json` 两 eval id 恰为 `level-judgment`/`bilingual-support`（对应「判断规范等级」「双语输入处理」）；`ab-suite/audit-engine.json` **确认不存在**；`skills/audit-engine/` 目录**确认零 `scripts/`、零 `tests/`**（仅 SKILL.md + 7 个 references/*.md，共 8 文件）—— 全部与三份 Spec 的断言精确一致，三份 rule6_note 的判据表落格（母删 audit-engine 档且 substitute 换新 / 字段档论证负担加重 / 探针档三条件不自判豁免）均查无硬伤。
- `config-template-key-currency.py` 已读全文：其断言作用域**明确只限 `phase_c_integrator.pre_merge_gate` 段**（docstring 显式声明「其他段无统一 schema 注册表, 无法 fail-closed 全模板断言」），不覆盖 `state_scanner.coordination.*`，故母 Spec 新增的 `DEFAULTS.json` 三键**不会**触发该既有 check、Impact 表无需为此新增 `.aria/config.template.json` 行——排除了一个我原本怀疑的潜在 Impact 表缺口。

## scope_ok

`true`。三份 Spec 各自变更面与自述范围一致；本席未发现越界改动。

## 一句话结论

母 Spec 的两条 R2 critical（C-B/C-C）经三处判据句逐字核对已闭环（仅 carry-id 的 SOT 章节引用有精度小问题）；三份 Spec 间近 35 处 `文件:行号` 断言逐条实读，准确率极高，探针 spec 全部精确、母 Spec 仅 1 处 minor，但**字段 spec** 有两处 Major：其"BAD_TOKEN 无对应态"的跨 Spec 叙事已被同批探针 spec 的修订超越而失真，且其 D3 改判赖以论证的 `.aria/state-checks.yaml` "10 条 check" 计数在本审计基线上实为 11 条（同 session 内被无关提交 `2ae012f` 抢先改变）。
