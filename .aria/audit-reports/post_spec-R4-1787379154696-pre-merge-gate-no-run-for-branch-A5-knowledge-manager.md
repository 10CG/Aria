---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-22T14:10:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A5-knowledge-manager
critical_count: 0
major_count: 0
minor_count: 2
---

## 摘要

R4 (末轮) 对 v4 做知识管理透镜复核, 聚焦 R3 聚合表归我席/我提出的三个簇 (#1 runtime_probe 探针形态 / #8 版本引用点 cite≠apply / #10 pending_owner 统计口径), 并以新鲜眼睛扫 v4 diff 级新增文字的文档层/可追溯性问题。方法: 实读 `aria @ 400f0bc` 源码 (`pre_merge_gate.py:174-233` `compute_verdict` 现有结构 + `_build_output:236-` 签名 + `ci_backends/aether.py:210-232`) 核对伪码落点真实性; 实读 `docs/decisions/DEC-20260705-001-runtime-probe-into-archive-gate.md` 全文 + `state-scanner/references/runtime-probe-declaration.md` 全文; 对 `openspec/` 全目录 (`changes/` + `archive/`) grep `runtime_probe:` 核验「首个采用者」主张; 实读当前 `CLAUDE.md:1-8,135-145` 与 `README.md:5-10,238-246` + 三个 i18n README 逐行核对 14 点版本引用; 实读 `.gitignore:15-25` 与 `references/pre-merge-gate-empirical-traps.md` 全文 (51 行) 核对 traps §六新增位置的既有格式惯例; 实核 Aria#177 issue 原文。

结论: **三个归我席的簇 (#1/#8/#10) 均已收敛, 落地方式与实读到的代码/文档现状逐字吻合, 无一处「答非所问」或「技术真但靶子错」的复发**。新鲜眼睛扫描发现两条 Minor 级文档同步遗漏 (均为「还能挑」而非「必须改」), 不构成推回理由。0 Critical, 0 Major, 2 Minor。**投 PASS**。

## R3 处置核对

| 簇# | 状态 | 证据 |
|---|---|---|
| #1 (runtime_probe 探针形态: 恒红常驻 state-check → 声明式归档门探针) | **closed** | v4 frontmatter (`:1-6`) 新增 `runtime_probe: {partition, symbol, max_age_days}` 三字段声明, 与 `runtime-probe-declaration.md:49-57` schema 逐字吻合 (`partition`/`symbol` 必填, `max_age_days` 可选默认 14, 本 spec 未用 `enabled_when` 是合法省略); frontmatter 注 (`:10`) 引用 `DEC-20260705-001` + `runtime-probe-declaration.md` 均属实 (本席逐行实读两文件全文确认定性吻合); 旧方案残留 (`.aria/probes/`/`gate-state-helper-invocation`/`state-checks.yaml`) 本席 grep v4 全文**零命中**, 完全清除, 非「新旧并存」半吸收。**「首个采用者」主张核验**: 本席对 `openspec/changes/` + `openspec/archive/` 全目录 grep `runtime_probe:`, 唯一在自己 frontmatter 里**声明**该字段的 proposal.md 就是本 spec; 另两处历史提及 (`2026-07-09-runtime-probe-archive-gate-integration` 设计该机制本身、`2026-07-22-state-scanner-gate-yaml-datasource` 讨论其 yaml-only 子态) 均只是**讨论/实现该机制**, 未在自己 frontmatter 里**使用**它 (前者 frontmatter 是 `unverified_claims:`, 后者无 frontmatter 块) —— 主张成立。**声明放绝对起始是否冲突 SOT**: `standards/openspec/templates/proposal-minimal.md` 模板本身确以 `# Title` 起始、无 frontmatter, 但**实际仓内已有 5 个 archive spec + 本 spec 共 6 例**在 `proposal.md` 绝对起始放 `---...---` 块 (`unverified_claims:`/其它), 且 `runtime-probe-declaration.md:73-75` 明文要求探针声明必须在「文件绝对起始的 `---...---` 块」——**不冲突, 是本项目已确立的既定实践, 非本 spec 新引入的风险面**。**归档去向**: `runtime-probe-declaration.md:129-139`「书写惯例」明文「声明随整个文件移入 `openspec/archive/`, 自然带入, 不需要任何额外动作」, 且已有归档先例 (`2026-07-09` 那份) 证实 frontmatter 确实随归档保留 |
| #8 (`CLAUDE.md:139/:141` + 14 点版本引用) | **closed** | 本席实读当前 `CLAUDE.md:135-141` 逐字核对: `:139` = 「aria-plugin 方法论轨: v1.52.0–v1.66.3 已 ship…」(版本区间), `:141` = 「版本: 插件 aria-plugin v1.66.3 …」(版本行) —— 与 v4 §5 表描述**逐字吻合**, 且与 Aria#177 issue 原文 (`forgejo GET` 实取) 点名的「`CLAUDE.md:139`(版本区间)+`:141`(「版本:」行)」精确对应, 无 R3 时的「引用换成 `:5` 答非所问」问题; `CLAUDE.md:5` = 「> **版本**: 2.0.0」(主项目版本, 与插件版本无关), 「非 #177 所指, 不动」这句现在**准确**——它不再顶替 `:139`/`:141` 的位置, 而是与其并列声明「两件事不同」。**14 点逐一核验**: `VERSION:24` 实读为 `| aria (插件) | v1.66.3 | … |` ✓; `README.md:8` 实读为 badge 行 ✓, `:242` 实读为 `Plugin Version:   1.66.3 …` ✓; 三个 i18n README (`zh`/`ja`/`ko`) 各在 `:3`(`translated-from`)/`:10`(badge)/`:244`(`Plugin Version:`) 三处含 `1.66.3`, 3×3=9 ✓ (本席逐文件 grep 核验); 加 CLAUDE.md 2 处 + VERSION 1 处 = **14**, `gitlink` 作为「引用点」之外的正交同步项单列 (与 #177 原文「另: aria 子模块侧」把 gitlink 类不变量单独讨论的先例一致, 不产生 14 vs 15 的计数矛盾) |
| #10 (pending_owner 三选项 + 34%-43% 统计) | **closed** | v4 `pending_owner` 文本 (`:20`) 「15-19 条 (34%-43%, R3 A5 逐簇点算)」与本席 R3 报告 [A5-R3-m1] 逐簇重算的严格/从宽两档数字 (15/44≈34%, 19/44≈43%) **逐字一致**, 不再沿用 R2 聚合报告「v2 新条款整体 ≥2/3」的错配口径; 且明确标注来源「R3 A5 逐簇点算」, 呈给 owner 的证据可追溯不含糊。三个选项 (i)接受收缩 / (ii)保留自动动作退回 v2 / (iii)接受收缩+另起 follow-up——覆盖「维持/撤回/折中」三个方向, 未见遗漏第四选项或暗中加权某一档 (未再出现 memory `feedback_ai_narrows_owner_decision_space` 描述的「引一个原文没有的限定词」或「漏 SOT 允许的档」模式) |

## 交叉一致性检查 + 新鲜眼睛

对 v4 新增文字逐段核对与既有 Design Decisions / SC 表 / Cross-references 是否互斥: 未发现新的条款间矛盾。伪码落点核对 (`compute_verdict:196` 现有 `raw_message = ""` 哨兵先例、`elif pr_ci_status == "not_applicable":` 与 `elif main_in_flight_runs:` 的真实相邻关系、`_build_output` 现有 `gate_error` 形参) 均与 v4 §2.2 描述的插入点/哨兵写法逐字吻合, 非向壁虚构的伪码。

发现两条 Minor 级文档同步遗漏, 均落在「本 spec 采用了一个此前"尚无人用"的机制」这一新情况带来的连带更新面, R1/R2/R3 此前审的是"要不要采用"而非"采用后遗留哪些连带更新":

### [A5-R4-m1] Minor — `runtime-probe-declaration.md:135-139` 的"尚无采用者"预言性陈述, 本 spec 归档后即失真, §5 同步表未列

**锚点**: `state-scanner/references/runtime-probe-declaration.md:135-139`:「不回改已经封存的归档 proposal.md 去补声明…这意味着: **截至本文档撰写时全部已归档 spec**（含 coordination 自身的 `interactive-session-dedup-coordination`）**都保持无声明状态**，不会被回填。**未来第一个真实声明者，会是下一个自带 telemetry 分区的活跃中 spec**。」

**问题**: 这句话是面向读者的事实性陈述（非纯说明性惯例条款），且带着明确的时间戳「截至本文档撰写时」。本 spec 正是它预言的「下一个自带 telemetry 分区的活跃中 spec」——一旦本 spec 归档（携带 `runtime_probe:` 声明进 `openspec/archive/`），这句话的事实断言部分（「全部已归档 spec 都保持无声明状态」「未来第一个…会是」）就变成过去时态未更新的陈述：读者此后翻到这句话，仍会得到「尚无真实声明者」的印象，而实际上已经有了。v4 全文（含 §5 文档同步面 17 处表、Cross-references）没有一处提到需要回来更新 `runtime-probe-declaration.md` 这句话。

**按 spec 实施会怎样错**：影响有界，纯知识库准确性问题，不影响本 spec 任何运行时行为或验收标准——不满足 R4 Major 门槛（不会造成错误行为/fail-open/契约破坏/实施者分叉）。但下一个考虑是否要用这个机制的 spec 作者读到这句仍标注"未来"的话，会误判该机制仍是零验货的新机制，可能因此更保守地不采用（或误以为要自己去找"第一个例子"而找不到，因为归档后的本 spec 才是那个例子，但文档没有指回它）。

**建议**：Phase D 收尾时（或本 spec §5 顺手加一行）把 `runtime-probe-declaration.md:135-139` 改为「已应验：`pre-merge-gate-no-run-for-branch`（aria-plugin#152，vX.66.4）是第一个真实声明者，归档于 `openspec/archive/…`」，将预言态陈述转为已验证的事实指针，同时说明「不回改已封存归档 proposal.md 本体」这条 owner 决策本身不受影响（改的是 `runtime-probe-declaration.md` 这份活文档，不是回改已归档的旧 proposal）。

---

### [A5-R4-m2] Minor — Cross-references 未点名 `DEC-20260705-001`/`runtime-probe-declaration.md`；traps §六新增证据的日期字段在 SC-13/TASK-0a 两处要求不对称

**锚点**：proposal.md Cross-references 段 (`:284-289`) 与 §3.5 TASK-0a / SC-13 两处证据要求。

**问题（一）**：v4 frontmatter 注 (`:10`) 重度依赖 `DEC-20260705-001` 与 `runtime-probe-declaration.md` 两份文档确立本 spec 是否可以/如何使用该机制，但 Cross-references 段（本 spec 自己按惯例用于列「先例」「决策」的收纳处，已列 `DEC-20260731-001`/`#122`/`#137`/`#126` 等同类引用）未把这两份文档也列进去。不影响实施正确性，纯降低下游读者顺着 Cross-references 找到机制源头的便利性。

**问题（二）**：§3.5 TASK-0a 明确要求「证据（HTTP 码 / run id / Δt / **日期**）写入 traps §6」，但 SC-13（同样落 traps §6 的活体证据：workflow-state 片段 + telemetry 行 + Δt）未同样要求带日期。两条证据落在同一新 §六 内，一条钉日期一条不钉，日后核对"这条证据是哪次跑的"时体验不一致（TASK-0a 的证据因涉及 Forgejo/gitea 服务端行为、有版本漂移风险而需要日期定位历史有效期是合理的，SC-13 是纯代码行为、时效性风险确实更低，但既然两者同属一个新章节，统一格式更利于后续读者扫描）。

**按 spec 实施会怎样错**：两者均不影响验收判定，均属可在 Phase B 落笔 traps §六时顺手处理的细节，不构成推回理由。

**建议**：Cross-references 段追加一行「机制来源: `DEC-20260705-001-runtime-probe-into-archive-gate.md` · `state-scanner/references/runtime-probe-declaration.md`」；SC-13 的证据抄录顺手也带上日期（与 TASK-0a 统一格式），非强制。

## Verdict

**verdict**: PASS (0 Critical / 0 Major / 2 Minor)
**vote**: PASS

归我席的三个 R3 簇 (#1 探针形态 / #8 版本引用点 / #10 统计口径) 经本席逐条实读源码与文档核验, **全部真正收敛**——落地方式与实读到的代码结构、既有项目惯例、issue 原文逐字吻合, 未发现"技术上为真但答非所问"或"半吸收"的复发模式。新鲜眼睛扫描发现的两条 Minor (`runtime-probe-declaration.md` 预言性陈述随本 spec 归档而失真未列入同步表 / Cross-references 与 traps 日期字段的细节不对称) 均为可在 Phase B/D 顺手处理的文档完善项, 不触及 R4 Major 门槛 (不会造成错误行为/fail-open/契约破坏/实施者分叉), 不构成推回理由。本席认为 v4 可批准进 A.2。
