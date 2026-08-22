---
seat: A3-code-reviewer
agent: code-reviewer
round: R2
verdict: APPROVE
critical_count: 0
major_count: 0
minor_count: 3
r1_verdict: REVISE
r1_counts: {critical: 1, major: 2, minor: 2}
---

# post_spec R1 — secret-guard-manifest-precision (A3 code-reviewer: spec vs 真代码一致性)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-manifest-precision/proposal.md`
参照物: `aria/hooks/secret-guard.sh` @ `400f0bc` (git log 确认当前树即基线) / `.aria/triage-report-179.json` / `docs/handoff/2026-08-20-issue-batch-181-147-145-ship-and-gate-blindspot.md`
方法: 逐条 file:line 打开原文核对 + python 对正则做分支/reader 机械计数 + handoff 全文检索。**只审未改** (本报告除外)。

---

## 核验表 (逐项 PASS/FAIL)

| # | spec 主张 | 核验方式 | 结果 |
|---|---|---|---|
| 1 | 基线 = aria @ `400f0bc` | `git -C aria log --oneline -1` = 400f0bc, 工作树 clean | PASS |
| 2 | `:709-710` 是 shell-rc 两 pattern, 只覆盖 shell 启动文件 | 实读: 709 (直读) + 710 (ssh 远程) 恰两条; 敏感名组 = .bashrc/.bash_profile/.bash_login/.zshrc/.zprofile/.profile/.bash_aliases//etc/environment//etc/profile, 无 claude 条目 | PASS |
| 3 | `:709` reader 列表不含 `jq` (漏报关键主张) | 机械枚举: 12 readers = cat/grep/egrep/fgrep/rg/head/tail/less/more/strings/awk/sed, **无 jq** | PASS |
| 4 | What.1 「既有 11 reader」 | 同上枚举 = **12** 非 11 (:700 面是 10, :710 面是 8, 无任何列表等于 11) | FAIL (计数错, 见 A3-m1) |
| 5 | `:546` lower_path 正则「17 类」 | 机械计数 = **29 个 alternation 分支**; 语义分组约 18-20 组, 无自然分组得 17 | FAIL (计数错, 见 A3-m1) |
| 6 | `:546` 无 claude 配置条目; `:545` lowercased 匹配 | 29 分支逐条过目, 零 claude; `grep -c 'settings\.json'` 全文件 = 0; :545 tr upper→lower 属实 | PASS |
| 7 | `:709` 误报形态 = `(readers)[[:space:]]+[^|]*(敏感名)` 命令行任意位置触发 | 与 :709 原文结构逐字符一致 | PASS |
| 8 | `_sg_line_match` @ `:82-88` 存在且为逐行 `=~` 基建 | 实读 :82-88, while read + `[[ =~ ]]`, 与 What.3 引用一致 | PASS |
| 9 | credit 系统 @ `:306+`; 「管道后 jq 'keys' / 字段白名单 / >/dev/null 放行」 | `_sg_compute_credit` 起 :306; :332 keys/length 白名单 + :337 `jq {…}` 投影 + :368+ stdout→/dev/null 均在 | PASS |
| 10 | Out-of-scope 「`\| jq '{env: .env}'` 因字段白名单形态获 credit」是既有语义 | :337 正则 `\|[[:space:]]*jq…[\"']?\{` 确实对任意对象构造给 credit, 主张代码级准确 | PASS |
| 11 | SC-3 「jq 直读无管道无 credit → 应拦」 | :332/:337 均要求前导 `\|`, 无管道形态拿不到 filter credit, 与代码一致 | PASS |
| 12 | triage 4/4 复现 @ 1.66.3/400f0bc | 报告 hit_rate 4/4; case-1 (jq exit 0) = SC-1 基线, case-3 (grep -oE exit 2) = SC-4 基线, case-4 (settings.json 计数 0) 均与 spec §Why 逐条一致; 「triage 期间活体二次误拦」在 case-3 actual_behavior 有载 | PASS |
| 13 | Impact 「泄露凭据轮换已由事故处置完成 (并发轨 08-20 handoff 凭据事故闭环)」 | 实读 08-20 handoff §2/§3: 闭环的是 **Forgejo registration-token** (2026-08-21 UI 重置, #153 事故, 08-20/21 当场泄漏); #179 的泄露凭据是 **2026-08-09 从 ~/.claude/settings.json env 节点泄出的 *_API_TOKEN** — 两码事。docs/handoff/ 全量检索无该 token 轮换记录 | **FAIL (A3-C1)** |

通过率: **11/13** (2 FAIL: 1 Critical + 1 Minor 计数类)。

## 路径变体完备性核验 (任务 3, 三条目逐面列表)

Bash 面 (spec 条目 `\.claude/settings\.json` / `\.claude/settings\.local\.json` / `\.claude\.json`, 无锚定子串匹配):

| 变体 | 覆盖? | 依据 |
|---|---|---|
| `~/.claude/settings.json` | 覆盖 | 子串命中; What.3 前置字符 `/` ∈ 触发集 |
| `$HOME/.claude/settings.json` / `${HOME}/…` | 覆盖 | 子串命中, 前置 `/` |
| 绝对路径 `/home/x/.claude/settings.json` | 覆盖 | 同上 |
| 相对 `.claude/settings.json` (cwd 下) | 覆盖 | 无锚定, 子串命中 |
| 引号包裹 `"…/.claude.json"` | 覆盖 | `"` `'` ∈ What.3 触发集 |
| `cd ~/.claude && cat settings.json` (bare 文件名) | **漏** | 三条目均要求 `.claude` 前缀; 与既有条目 (如 `/\.aws/credentials`) 同构的既有限 |
| glob `cat ~/.claude/*.json` / `settings*.json` | **漏** | star 打断字面量 |
| 变量间接 `CFG=…; cat "$CFG"` | **漏** | 结构性 (#138 类), 全清单共病 |

Read/Edit 面 (spec 条目 `/\.claude/settings\.json$` 等, 前导 `/` + `$` 锚定, lowercased):

| 变体 | 覆盖? | 依据 |
|---|---|---|
| 绝对路径 (CC Read 规范形态) | 覆盖 | `/` 锚命中 |
| `~/.claude/settings.json` (tilde 未展开透传) | 覆盖 | `~/` 中的 `/` 满足前导锚 |
| 相对 `file_path=".claude.json"` | **漏** | 无前导 `/`; CC Read 强制绝对路径, 风险低, 且与既有条目同构 |
| 大小写变体 | 覆盖 | :545 lowercased, 条目本身全小写 |

结论: spec 条目写法对现实主要形态覆盖充分, 漏项均为与既有清单同构的结构限; 建议 What.5 hook 头注释「已知限」把 bare-filename/glob 两类点名 (见 A3-m2)。

## Findings

### [A3-C1] Impact 轮换闭环主张张冠李戴 — 引证的 handoff 闭环的是另一枚凭据 (Critical)

- 位置: proposal.md:64 「泄露凭据轮换已由事故处置完成 (并发轨 08-20 handoff 凭据事故闭环), 本 spec 不含轮换动作」。
- 事实: 08-20 handoff 的凭据闭环 (§2 「registration token 事件闭环 2026-08-21」) 处置的是 **该 session 自己泄漏的 Forgejo runner registration-token** (§3.1, GET …/actions/runners/registration-token 回显事故, 短时效 token)。#179 需轮换的凭据是 **2026-08-09** 经 `jq … ~/.claude/settings.json` 泄入对话的 `*_API_TOKEN` (issue 原文: 「已导致一次真实 token 泄露…该凭据需轮换」)。handoff 中 #179 仅作类比出现 (「这正是 #179 描述的…形态」), 非同一事故。docs/handoff/ 全量检索 (轮换/rotat/settings.json/api_token) 无 08-09 泄露 token 的轮换记录。
- 为什么 Critical: spec 据此主张把轮换动作排除出范围。若 08-09 token 实际从未轮换, 则一枚已入对话上下文的活凭据处于**无人认领**状态 — 这正是 memory `feedback_secret_in_logs_fix_requires_rotation` 点名的「代码脱敏不闭环」形态; 且违反「事实断言写进 spec 前必实跑/实证」纪律。
- 修复: 向 owner 核实 08-09 泄露 token 是否已轮换。已轮换 → 改引真实证据 (具体 handoff/记录); 未轮换/无法证实 → Impact 改为「轮换状态待 owner 确认」, Tasks 增加一条轮换确认 gate (可仍由 owner 执行, spec 不必自做, 但不得凭错误引证宣告闭环)。

### [A3-M1] What.3 「正则字面量位置」类标签宽于机制实际覆盖 + 适用 pattern 行集合未言明 (Major)

- 位置: proposal.md:31 (What.3)。
- (a) 排除集 {`(`, `|`, `\`} 只覆盖 alternation/转义上下文。引号起头的裸正则字面量 — 如 `grep '.bashrc' hooks/secret-guard.sh` (审计 hook 自身的同类正当命令, 前一字符 `'` ∈ **触发**集) — 仍误拦, 但按 spec 自己的分类它属「敏感名在正则字面量位置」。范围边界段只切了 prose 类, 没切这一类 → 类标签过宽, 验收时会争议 SC-4 变体该不该含它。修复: 明写「引号定界的裸正则字面量 (引号紧邻敏感名) 不在治, 与 prose 同走 guard:ack」或把 SC-4 变体扩到该形态并调整触发集语义。
- (b) spec 未言明前置字符类施加于**哪些** pattern 行。issue 的活体二次误拦 (heredoc) 命中的是 `.env` pattern 而非 :709 shell-rc; :700 ssh-key 面 / :714+ secrets 面同样是 `[^|]*(敏感名)` 结构。若实现者理解为「全部敏感名组」而 SC-5 只守 shell-rc 形态, 其他行的误杀风险无守卫; 若只施于 :709, 应明写。修复: What.3 点名目标行集合 (建议: 仅 :709-710 + 新增 claude-config pattern), SC-5 fixture 集与之对齐。

### [A3-M2] What.3 触发集/排除集双集并存, 语义可被读反 (Major)

- 位置: proposal.md:31。「仅当前一字符 ∈ {行首, 空白, ", ', =, /, ~} 时视为路径位置; 前一字符为 ( | \ 时不触发」— 前半句是白名单语义 (触发集外一律不触发), 后半句又给排除集。两集并集不全分割字符域 (字母/数字/`:`/`,` 等两边都不在), 实现者若读成「非排除即触发」则字母前缀 (`cat my.bashrc`) 行为与白名单语义相反。memory `feedback_predicate_tiers_need_total_partition_proof` 同款。修复: 明示单一语义 — 「白名单式: 仅触发集内触发; 排除集仅为动机示例, 非独立判据」, 并为一个「两集之外」前缀字符写死一条 fixture 期望。

### [A3-m1] 两处计数与基线实测不符 (Minor)

- proposal.md:21 「:546 …17 类」: 实测 29 个 alternation 分支 (语义分组亦为 18-20, 无分组方案得 17)。核心主张 (无 claude 条目) 不受影响, 但基线冻结 spec 里的计数应可机械复算 (SC-6 同样依赖计数纪律)。改为「29 分支」或删数字。
- proposal.md:27 「既有 11 reader」: :709 实为 **12** readers; 无任何既有列表 = 11。此数直接进实现 (新 pattern reader 组 = 既有 + jq + python3?), 写错会造成实现者对「既有」取哪张表的歧义。改为「:709 的 12 reader」。

### [A3-m2] 变体已知限建议入 hook 头注释 (Minor)

- What.5 已计划头注释补「claude-config 条目与误报已知限」; 建议把变体表中 bare-filename (`cd ~/.claude && cat settings.json`) 与 glob (`~/.claude/*.json`) 两类漏项一并点名 (与既有清单同构的结构限, #138 类), 免得下次 triage 又当新缺口报。

## 无发现项 (核对过且干净)

- :709-710/:546/:82-88/:306+ 四处 file:line 引用全部准确 (行号零漂移)。
- spec §Why 表格与 triage report 4 case 逐条一致; SC-1/SC-4 的基线 exit 码主张与 triage 实测吻合。
- SC-3 与 credit 语义无冲突 (直读拦 / 管道 credit 放, 与 :332/:337/:368+ 代码一致); Out-of-scope 第 1 条的 credit 既有语义描述代码级准确。
- rule6_note 的 substitute 处置与 #128 先例及 skill-benchmark-exemption 判据表相符 (hook bash 代码, 零 SKILL.md 指令面)。

## Verdict

**REVISE** — C1 (轮换闭环引证错位) 必须在 owner 批准前解决; M1/M2 属实现歧义面, 修 spec 文本即可, 不动方案骨架。方案主体 (双平面补条目 + 前置字符类 + baseline-failing SC) 与代码现状对得上, 骨架成立。

---

## R2 (v2) 复核

对象: proposal.md v2 (post_spec R1 修订版) + 处置表 `post_spec-R1-1787375602111-…-aggregated.md`。方法: 逐 finding Q1 (落地忠实?) / Q2 (原处方对?) + v2 新增引用对 `400f0bc` 真代码复核。

### Q1/Q2 逐条 (对我 R1 五条)

| Finding | Q1: v2 落地忠实? | Q2: 原处方对? |
|---|---|---|
| A3-C1 (轮换引证张冠李戴) | **忠实**: Impact:71 撤销错误引证并明写事实链 (08-20 = registration-token 另案 / #179 token 无轮换记录, 与我 R1 检索结论逐字相符); Tasks 1.0 owner 安全门 ship 前置; Status header 二次点名 | 对 (v2 采纳「gate 化」路径) |
| A3-M1 (标签过宽+适用面未点名) | **忠实**: What.3 标签改「非路径前缀位置」; 引号定界裸名归已知限 (b) 并保留归因; 适用面点名 = 全部路径清单型行 (:709 + 新 claude-config + .env/id_rsa sibling, B.1 逐行枚举入 detailed-tasks), 命令注入型排除 — 正是我要的两点 (与 A2-M1 合流) | 对 |
| A3-M2 (双集并存语义歧义) | **忠实**: What.3 改单一白名单语义 (「其余任何前缀字符一律不触发」, 不设并存排除集); `~` 删除另有 A2-m1 独立依据 (结构性不可达), 成立。我 R1 附带建议「域外前缀字符写死 fixture」由 SC-4 变体 ≥3 条 (alternation/转义位置即域外字符) 实质覆盖 | 对 |
| A3-m1 (29/12 计数) | **忠实**: Why 表改「12 个: cat…sed」/「29 个分支」, What.1 改「既有 12 reader」— 与我 R1 机械计数一致 (本轮对码复确认) | 对 |
| A3-m2 (bare-filename/glob 入头注释已知限) | **未落地**: 处置表 row 10 声称「What.5 补注」, 但 v2 What.5 (:42) 与 v1 逐字相同 (「hook 头注释补 claude-config 条目与**误报**已知限」) — bare-filename/glob 是**漏报**变体限, 不被「误报已知限」措辞覆盖。见 [A3-R2-m2] | 对 (处方维持) |

### v2 新增引用 · 一致性核验表

| # | 核验项 | 方式 | 结果 |
|---|---|---|---|
| 1 | `:337` 形状 credit「纯形状判定不查字段名」(What.1b) | R1 已验 regex `\|[[:space:]]*jq…[\"']?\{`, 复确认无字段名检查; 处置表 `:335-339` 行位亦准 | PASS |
| 2 | `:785/:786` 窄先例 = `python3? -c` / `node -e` + 源组 `(/v1/var/\|secretsmanager\|/secrets/\|\.env\|provider_key)` | 实读 785-786, 与 v2 描述一致; 「扩展源组加 claude-config 三条目」与该结构相容 | PASS |
| 3 | What.1b 四类有效 credit 在代码中全部真实存在 | 实测: 名字面 `:332` (keys/length/paths/leaf_paths) / 计数 `:384` (`wc -[clw]`) / 哈希 `:387` (sha256/md5/sha1/sha512sum) / 丢弃 `:378` (`>/dev/null`) + `&>` + curl `-o /dev/null` — SC-3 的 `\| wc -c` → 0 有代码根基 | PASS |
| 4 | What.1b ↔ SC-3 ↔ Out-of-scope 三处 credit 表述互恰 | 逐条对照: SC-3 五条期望恰好 = What.1b 语义 (keys→0 / `{env: .env}`→2 基线红 / wc→0 / >/dev/null→0 / 直读→2); `.env` 对照组「行为不变」= Out-of-scope「通用面不动」的 fixture 化守卫; 「跳过 :337 分支」与保留 :332 分支互不冲突 | PASS |
| 5 | SC-1 `python3 -c … ~/.claude.json` 变体与 What.1「python3 不入 reader 组」相容? | 相容 — 该变体由 :785 源组扩展承载 (Tasks 1.1 亦点名), 非 reader 组路径 | PASS |
| 6 | 29 分支 / 12 reader 勘正后数字 | 对 R1 机械计数脚本结果复核 | PASS |
| 7 | TASK-0 措辞 vs Tasks 1.0 | **语义一致** (核实已轮换 / 未轮换先轮换再 ship / ship 前置, 三处无矛盾); **编号标签不一致**: header/Impact 称「TASK-0」, Tasks 列表编号「1.0」, 全文无 TASK-0 字样的任务项 | PASS (语义) / 标签见 m3 |
| 8 | Impact 行为变更申报与 What.3 新标签同步? | **FAIL**: Impact:69 (2) 仍用 v1 标签「敏感名在**正则字面量位置**」+「证明只放字面量位置」— v2 已把该类收窄为「非路径前缀位置」且引号定界裸名移入已知限, 申报口径残留旧标签 | FAIL → m1 |
| 9 | What.5 落 A3-m2 补注 (处置表 row 10 声称) | 文本 diff: What.5 v1↔v2 逐字相同 | FAIL → m2 |

通过率: **7/9** (2 FAIL 均 minor 级; #7 半项计 PASS)。

### R2 Findings (全部 Minor, 不阻收敛)

- **[A3-R2-m1] Impact 申报标签残留 v1 口径**: proposal.md:69 「新放行: 敏感名在正则字面量位置的命令…证明只放字面量位置」→ 应改「非路径前缀位置」(两处), 否则 ship 时行为变更申报与 What.3 已知限 (b) 矛盾 — 引号定界裸名按旧标签属「放行」, 按 v2 实际机制仍拦。
- **[A3-R2-m2] A3-m2 未落地但处置表记为已落**: What.5 未增 bare-filename (`cd ~/.claude && cat settings.json`) / glob (`~/.claude/*.json`) 漏报变体已知限; 且现措辞「误报已知限」类别上盖不住漏报变体。补一短句即可 (或并入 What.3 范围边界段改「已知限三类」)。
- **[A3-R2-m3] TASK-0 / 1.0 编号标签不一致**: 三处引用「TASK-0」但任务列表编号「1.0」; 机读/检索 TASK-0 会落空。统一其一 (建议任务项改标 `1.0 (TASK-0, owner 安全门…)` 或全文改 1.0)。

### R2 Verdict

**APPROVE** — 我 R1 全部 C/M 级 finding 忠实落地且落法正确 (C1 gate 化 / M1 双点 / M2 单一白名单); 他席合流项 (A1-C1 credit 收紧 / A2-C1 整串匹配语义) 在 v2 中与代码事实核对无矛盾, What.1b 三处表述互恰。残余 3 条均 minor 文本修 (m1 申报标签 / m2 What.5 补注 / m3 编号统一), 建议随 R2 收敛批注一次性微修, 不需 R3。
