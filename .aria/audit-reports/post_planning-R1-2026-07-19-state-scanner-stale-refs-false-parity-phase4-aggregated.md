# post_planning R1 (补跑) — state-scanner-stale-refs-false-parity Phase 4

> **性质**: 补跑。本 cycle AI 以「checkpoint 结构性前提不成立」自行豁免 post_planning，owner 按不可协商规则 #10 裁定不认可，要求照跑。审计时代码已 ship v1.62.0、spec 已归档 ⇒ **post-hoc**，审的是计划质量，不是能否 ship。
> **时间**: 2026-07-19 | **模式**: convergence (max_rounds=4) | **团队**: 按 `.aria/config.json` `audit.teams.post_planning` 全 5 席

## R1 汇总

| 视角 | verdict | Critical | Major | Minor |
|------|---------|----------|-------|-------|
| tech-lead | PASS_WITH_ISSUES | 1 | 4 | 4 |
| backend-architect | PASS_WITH_ISSUES | 0 | 1 | 4 |
| knowledge-manager | PASS_WITH_ISSUES | 0 | 4 | 4 |
| code-reviewer | PASS_WITH_ISSUES | 0 | 4 | 6 |
| qa-engineer | PASS_WITH_ISSUES | 1 | 2 | 1 |

**R1 合并**: 1 Critical + 13 Major (去重后 9 类) + 18 Minor。无 FAIL。

## Critical

### C-1 (tech-lead) — AC-5 以削弱形态实现却按原文勾选

- **AC-5 原文** (`proposal.md:697` / task 2.12): track commit 对 HEAD 不可达 ⇒ `overall_parity == false` **或**该 remote `reason` 非空 —— 这是**裁决级**断言。
- **实现** (`scan.py:230-236`): 第一道守卫是 `claims_health = overall_parity is True and not reason`，`if not claims_health: return []` —— 即**只在 AC-5 的结论已为假时才开始检测**；检测到后不翻转 `overall_parity`、不写 `reason`，只 append 一条 `snapshot_self_contradiction` 到 `errors[]`。
- **下游为空** (主 loop 独立复核): `snapshot_self_contradiction` / `snapshot_consistency` 在全仓 `*.md` **零命中** —— 不在 `state-snapshot-schema.md` (task 1.8 刚确认的真 SOT)、不在任何 RECOMMENDATION_RULES dispatch；`output-formats.md` 通篇不提 `errors`（`grep -c errors` = 0）。
- **净效果**: 在使用者侧与「不实现」不可区分。且恰好绕过 #95 归档门（符号有生产引用 ⇒ 不算死代码）。
- **裁定**: 属实。task 2.12 原文自己预警过「AC 勾了但从没实现」，本 cycle 做出的是它的变体：有任务、有代码、有勾选，AC 断言仍不成立。

## Major (去重后)

| ID | 来源 | 内容 | 主 loop 复核 |
|----|------|------|--------------|
| M-A | code-reviewer | **task 7.2 张冠李戴**: 7.2 在 `## 7. F2′ — 退役 mtime 实现` 章节下，要清的是 `warn_after_hours`/`local_refs_stale`；我做的是 `verify_mode`/ls_remote 的 SOT 清扫（属 task 1.10）并把 7.2 勾了。至少 4 处 `warn_after_hours` 原样保留 (DEFAULTS.json:38 / config-loader/SKILL.md:79 / .aria/config.template.json:21 **采用者模板** / .aria/config.json:20)。 | **属实，已确认章节归属** |
| M-B | code-reviewer | **归档门两条机械通道未点亮**: 手工 `git mv` 归档，未走 `openspec-archive` skill ⇒ warn_overlay frontmatter (Step 2) 与 D auto-issue tracker (Step 7, 门控 `d_payload != null`) 都没跑。对照组: 同日归档的姊妹 spec `2026-07-19-state-scanner-openspec-collector-false-green/proposal.md` 首行即 `---` 带完整 `unverified_claims`。 | **属实，最该补救的一条** |
| M-C | code-reviewer | **handoff 提前宣称本审计已跑** (`:67`「已补跑…结果见 .aria/audit-reports/」)，而当时本 cycle 无任何报告。写在专门记录规则 #10 违规的段落里，与本 cycle 主题同型。 | **属实**。附注: 该 agent 称「全目录无任何 post_planning 文件」是**错的**（有 36 份，属其它 spec）；实质指控（本 cycle 无）成立。 |
| M-D | tech-lead + knowledge-manager | **task 5.5 未做且零披露**: 归档 proposal / CHANGELOG / handoff 三处全缺。其背后是 `_aggregate_flags` **零生产调用点**（主 loop grep 确认）—— 符合 v1.53.0 归档门 block 档字面定义，门却给 0 block。 | **属实** |
| M-E | tech-lead | **Rule #6 豁免论证被本 cycle diff 否证**: 理由写「未动指令面」，但 `basic-rules.md` 改 77 行新增 dispatch 第七路 + `degrade_when` = 「什么状态给什么建议」的规则表；且 task 11.2 修了 AB rubric（承认判分标准失准）却不跑 AB。 | **属实** |
| M-F | tech-lead + code-reviewer | **12.6 / 12.9 反向失真**（已做未勾）+ 陈旧批注（「本 Spec 尚未进入 Phase D」而文件已在 `archive/` 下；「工作进行中不应释放」而 claim 已释放 `s-123d@1436.yaml status=done`）。 | **属实** |
| M-G | tech-lead | **task 3.5d「可以不做」零论证**，而它落在 spec 自述的恒红根因面（AC-15(c) 防饥饿的 carve-out 前提「每条**非退避** leg」依赖 3.5d 存在）。 | **属实**，需补影响面数字 |
| M-H | knowledge-manager | **归档 proposal 3 处死链**（指向姊妹 spec 旧路径，实际在 `2026-07-16-*` 前缀目录下）。 | **属实，主 loop 已 ls 确认** |
| M-I | backend-architect | **AC-5 落位违反 scan.py 自身架构不变量**: 模块 docstring 自称 "intentionally minimal… All phase logic lives in collectors/"，而 scan.py 302→476 行 (+57%) 全来自这两段业务逻辑 + 直接持有 git 子进程调用。仓库已有更贴合先例 `collect_sync_state(project_root, multi_remote_data=...)`（活在 collectors/ 内、显式接收另一 collector 输出）未被采用；"需重排 collector 顺序" 只排除了「塞进现有 collector」，没排除「新建独立 collector」。 | **属实，主 loop 已核行数与先例** |

## Minor (代表性)

- **计数错**: 归档 proposal 与 CLAUDE.md 写「102/119 done」「9 项活跃未勾」；机械实测 **103/119**，活跃未勾 **8**（3.5d/3.10/3.16/5.5/11.1/12.6/12.9/13.7）。
- **task 9.3 正文残留反向陈述** (`tasks.md:219-222` 仍写「OQ-C 本身仍未裁定 (1.3 checkbox 未勾)」)，22 行清理按 `(TODO: …)` 形态匹配，此段是 `> **日期进展**:` 形态所以漏掉。
- **AC-15 边界只披露了一个失效源**: 3.16 (k_eff) 披露充分且规格最高；3.5d 影响 AC-15(c) 防饥饿 carve-out，未纳入边界声明。
- **`_enforced_entries_of` 作为内部闭包无独立单测**；**`_remote_refresh_leg_key`/`_parse_leg_fetched_at` 与 remote_refresh 手工同步双份**（本 spec 病症的微缩版，建议下沉 `_common.py`）；**`excluded_read_only` 命名比语义窄**（实为 enforced 的全集补集，含白名单未命中）。
- **12.5 dogfood 无可链接产物**（姊妹 spec 用 `dogfood-evidence.md` 解过同一问题）；**AC-16 正向腿实测 vacuous**（live snapshot 全 ok/no_matching_remote，而 #165 仍 open）。
- **「实质项」判据未成文**: 从 N 个剩余 TODO 选子集这类 cycle，A.2 产物应含一张 N 行裁定表（任务号/实质-否/判据/落位）。有此表则 5.5 不可能漏。

## 对审计问题 5「范围裁定中立性」的结论 (tech-lead，主 loop 认同)

> 存在系统性偏向，但不是均匀的偏向。真实模式是「AI 自己觉得可怕的项披露得极充分 (3.16)，觉得枯燥的项披露不足或不披露 (5.5 / 3.5d / 11.1)」。这比单纯「偏向少做」更隐蔽——披露质量的高方差会让读者从最显眼的那条推断整体规格，而实际最低规格的那条是零披露。

## R1 → 处置

见同目录 `post_planning-R1-fixes-*.md` 与 tracker issue。R2 收敛判定在处置完成后进行。

## 附注: qa-engineer 席位 (已回填)

⚠️ 本节初版写「未在收敛判定前返回…应记为覆盖缺口, R2 需补」。**该席位随后返回了**, 且是 R1 最重的一份 —— 报出 **1 Critical + 2 Major + 1 Minor**, 其 Critical 是本轮唯一一条「已 ship 的真实红测试」。初版未回填导致落盘报告低估自己的覆盖面 (post_planning R2 N-3 抓出)。

**qa-engineer 席位结论**:
- **Critical**: `session-closer/tests/test_handoff_autofill.py::test_unreachable_remote_warns` 在归档 commit `9af7b21` 上**真实挂着** (agent 实跑复现)。根因: `552e030` 把判据从 `reachable is False` 改为 `fetch_ok == "false"` (修复本身正确), 夹具未跟改。**为什么没发现**: `state-scanner/tests/run_tests.py` 的 `TESTS_DIR` 硬编码只扫自己的 `tests/` (该脚本 :20-21), 结构上看不见 `session-closer/tests/` ⇒ 「1248 全绿」的验证范围覆盖不到本次改动的真实爆炸半径 (改了 A skill 里、消费方在 B skill 的代码, 只跑了 A 的测试)。
- **Major-1**: I2 观测性字段 (`enforced_remotes_resolved` / `excluded_read_only` / `enforced_set_empty`) 产出侧**零直接断言** —— 生产代码注释自陈「裁决基于子集就必须让子集可读」, 却无测试钉死。
- **Major-2**: 测试数声称「1219 → 1248」与实测不符, 双端 worktree 实跑 + `git diff` 净新增 `def test_` 计数交叉验证, 真实起点为 **1232** (delta +16)。
- **Minor-1**: `_aggregate_flags` 的既有测试仍在手工构造 `reachable: False` 喂给一个生产侧不可达的输入形态 (非本 cycle 引入, tasks 5.5 已诚实记录)。
- 该席位另对本 cycle 新增测试逐类做了**可证伪验证** (含实际去掉 `ARIA_SCAN_OFFLINE` 复跑, 确认 `test_ac9_repeated_scans_are_byte_stable` 的「恒绿」自述属实而非自欺), 结论: 新增测试整体有牙。

**根因机制状况 (R2 N-3)**: Critical 的结构性根因 —— 无跨 skill 全量测试入口 —— **尚未机制化修复**。本次靠一次性人工扫 12 个 `skills/*/tests` 目录兜住; `TESTS_DIR` 硬编码未变, 全仓仅 state-scanner 一个 runner。⇒ 下次跨 skill 改动同类漏检会原样复发。已纳入 Aria #168 跟踪。
