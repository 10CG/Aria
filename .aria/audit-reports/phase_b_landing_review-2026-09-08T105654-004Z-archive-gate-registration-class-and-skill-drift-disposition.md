---
checkpoint: phase_b_landing_review
round: 1
mode: agent_team_domain_split
verdict: FAIL
converged: false
counts: 六席 37 原始 / 33 去重 / 23 存活 / 10 证伪; 完备性批评席另 10 条 (1C/6M/3m)
teams: [aria:code-reviewer, aria:qa-engineer, aria:backend-architect, aria:knowledge-manager, aria:tech-lead, aria:ai-engineer, aria:context-manager(完备性批评)]
timestamp: 2026-09-08T10:56:54.005Z
context: aria 2b67ac6 + 主仓 d2d93da 的落地产物 (非 Spec 文本)
safe_to_ship: false
agents: 58 (0 error) / subagent_tokens 6.9M / tool_uses 1721
---

# Phase B 落地复审 — 逐条处置台账

> 为什么有这份台账: 完备性批评席指出 handoff 声称「28 条存活全部处置」但**仓内无任何逐条记录**,
> 且「唯一可机械核验的那条 Major 既没修也没记为驳回」。无台账的「全部处置」= 不可核验的自证。

> 为什么复审这批产物: TG-B/TG-C/TG-D 全部由主控**单线**完成, 没有第二双眼睛。依据本 cycle 自己
> 沉淀的判据 (「席位都看过前几轮时 0C+PASS 不是收敛证据」), 拉 6 席按**交付域**分工复审。

## 六席 verdict

| 席 | verdict | findings |
|---|---|---|
| `aria:code-reviewer` | **FAIL** | 9 |
| `aria:qa-engineer` | **PASS_WITH_WARNINGS** | 2 |
| `aria:backend-architect` | **FAIL** | 6 |
| `aria:knowledge-manager` | **FAIL** | 4 |
| `aria:tech-lead` | **FAIL** | 8 |
| `aria:ai-engineer` | **FAIL** | 8 |
| `aria:context-manager` (完备性批评) | **safe_to_ship: false** | 10 (1C/6M/3m) |

## 六席 finding 处置 (23 条存活)

| # | 严重度 | 位置 | 结论 | 处置 |
|---|---|---|---|---|
| 1 | Critical | `SKILL.md:49` | 三处交付物硬编码 `v1.72.0` —— 正是 proposal 逐字 ⛔ 禁止的那个号, 且已被并发轨 10CG/Aria#195 占用; 无任何验收项或同步步骤能抓到它 | ✅ fixed |
| 2 | Major | `CHANGELOG.md:1` | CHANGELOG.md 整文件被静默 CRLF→LF 重写 (72 行行尾全改), 18 行插入产出 90+/72− 的 diff —— memory `preserve-crlf` 逐字点名的形状 | ✅ fixed |
| 3 | Major | `SKILL.md:313` | B-2 插进 Step 7 的 6 行破坏了 ```yaml 块的缩进层级 —— 子项 (3 空格) 比父项 `行为:` (4 空格) 还浅, 新键 `约束:`/`校验:` 与同级键错位 | ✅ fixed |
| 4 | Major | `SKILL.md:601` | B-11 新增的错误行「`git mv` 失败: 目标已存在」描述了一个不存在的失败态 —— 实测 git mv 返回 0 并把源目录嵌进目标里, 而 Step 4 三条断言对这个坏结果全绿 | ✅ fixed |
| 5 | Major | `tasks.md:120` | C-10 勾了但 SC-12 钉死的正控数不成立: `d81873b^` 上实测 4 处而非规格逐字写的「恰为该版 3 处真裸引用」 | ✅ fixed |
| 6 | minor | `proposal.md:137` | D6 行自称「唯一条目逐字为」的那段实测输出漏了结尾的 `, soft_error=None`; 提交信息里的版本偏得更远 | ✅ fixed |
| 7 | minor | `SKILL.md:583` | 已退役配置项表里「全仓仅本文件出现过 2 次」在落地那一刻就已失效 (现在是 1 次) | ✅ fixed |
| 8 | Major | `check_bare_issue_refs.py:41` | 白名单豁免用整行子串包含判定, 会连带放行未来追加到同一行的新裸引用 | ✅ fixed |
| 9 | Critical | `check_bare_issue_refs.py:25` | "fail-CLOSED" QUALIFIED 正则对「路径+#数字」误判为全限定引用, 断言实际不 fail-closed | ✅ fixed |
| 10 | Major | `check_bare_issue_refs.py:37` | check_bare_issue_refs.py 主调用路径上任何文件读取异常都未捕获, rc=1 与「有违规」语义冲突 | ✅ fixed |
| 11 | Major | `archive_tracker_verify.py:20` | archive_tracker_verify.py 的 --body-file 分支对非 UTF-8 输入未捕获异常, rc=1 与「NO_SHA/MISSING」语义冲突 | ✅ fixed |
| 12 | Major | `check_bare_issue_refs.py:30` | TARGET_LITERALS 把本 Spec 专属的字面串硬编码进随插件分发给第三方的脚本, 违反本仓已有的同类先例 | ✅ fixed |
| 13 | minor | `archive_tracker_verify.py:49` | --repo/--issue 未标 required, 缺省时会真的发起一次垃圾 forgejo 请求而不是立即报参数错误 | ✅ fixed |
| 14 | Critical | `proposal.md:126` | check_bare_issue_refs.py 负控 (`d81873b^`) 的命中数声称『恰是 3 处』，实测为 4 处，且同句自证『不该写死数字』后自己写死了数字 | ✅ fixed |
| 15 | Major | `SKILL.md:42` | 『核心功能』表与『输出格式』schema 残留 CLI-bug 时代的清理/自动修正描述，逃出了 Spec 自己的 SC-1 关键词验收网 | ✅ fixed |
| 16 | Critical | `proposal.md:137` | 10CG/Aria#208 的中心事实句「两种引用形态都落 unclassified, 都不 block」两半皆被实跑推翻：:353 那种形态从未进入分类, 而它真被分类时判的是 dead(会 block) | ✅ fixed |
| 17 | Critical | `spec_complete.py:1000` | 10CG/Aria#208 根因误引：它的唯一举证物 check-m6-e2e-acceptance.py 是一个**已交付的 Python 文件**, warn 的真因是 definition_path 解析失败, 不是「非 P | ✅ fixed |
| 18 | Critical | `proposal.md:144` | 10CG/aria-plugin#191 与 10CG/aria-plugin#193 把 v1.72.0 当既成事实对外发布, 而该版本不存在, 且本 Spec 的 Part E 用 ⛔ 明文禁止了这个字面值 (并发轨 10CG/Aria#195 正在争同一号) | ✅ fixed |
| 19 | Major | `tasks.md:131` | 10CG/aria-plugin#191 只覆盖了 tasks.md D-2 明列三条子缺陷中的一条半, 第三条「断言首句零判别力」完全没写进去, 而 D-2 已勾 [x] | ✅ fixed |
| 20 | Major | `version.yaml:6` | 10CG/aria-plugin#191 的修复建议只覆盖派生文件 ab-suite (2 个 eval / 3 处字面), 漏掉它的源 evals.json (4 个 eval, 同病且是并列的 benchmark 输入); 且 | ✅ fixed |
| 21 | Major | `AB_TEST_OPERATIONS.md:224` | 10CG/aria-plugin#190 建议新增的 Step 7 eval, 在这个「真仓 + 真 origin + 无 sandbox」的评测台上会让被测臂真的 POST 出 tracker issue, 而不是产出「草稿」 | ✅ fixed |
| 22 | Critical | `SKILL.md:49` | 交付物硬编码了 Spec ⛔ 明禁、并发轨已宣告的版本号 v1.72.0 (三处), 且落在全部版本同步机制的覆盖面之外 | ✅ fixed |
| 23 | Critical | `SKILL.md:356` | 「CLI 漂移类级收口」后, 输出契约仍指令 AI 输出 `cli_bug_fixed: true` —— 它逃出了 SC-1 判据自己的 grep (大小写), 也在 SC-1b 的复核射程之外 | ✅ fixed |

## 被反驳席证伪 (10 条, 不改)

- **[Major] `tasks.md:106`** — C-3 / C-8 / C-10 三项「留实跑输出」的验收全部勾了, 但仓内 (tasks.md / proposal.md / handoff) 没有留下任何一态的输出
- **[minor] `SKILL.md:58`** — B-6 语义本身站得住 (非 author-to-match-checker 假绿), 但「自 v1.72.0 起改走 git mv」与九行之上的「本仓从未安装该 CLI」互相矛盾
- **[minor] `CHANGELOG.md:19`** — 新增的 Step 7 断言宿主脚本 archive_tracker_verify.py + 6 个单测 + 4 份夹具未单列为 Added 条目
- **[Major] `spec_complete.py:401`** — 10CG/Aria#208 的建议处置在实现层不可执行：它的触发条件「符号形如路径或带扩展名」对提取器产出的 symbol 恒为假, 而改按 definition_paths 判会把它自己的举证案例变成假 block
- **[minor] `tasks.md:135`** — 10CG/Aria#208 开在 10CG/Aria, 而同日同批、针对同一个文件 spec_complete.py 的 10CG/aria-plugin#192 开在 10CG/aria-plugin — 同一代码面的缺陷分居两个看板
- **[Critical] `SKILL.md:318`** — Step 7 新插的校验行占位符 `{number}` 全文无绑定, 且校验被放在「创建 issue」之前 —— 逐字执行必 rc 2, 而 :319 规定 rc≠0 判 FAIL
- **[Major] `CHANGELOG.md:1`** — CHANGELOG.md 被静默 CRLF→LF 全文件重写 —— 18 行插入变成 90+/72− 的整文件 diff, 且它成了全仓唯一 LF 的 skill CHANGELOG
- **[Major] `SKILL.md:601`** — 错误表新写的「git mv 失败: 目标已存在」是一个 git mv 不会产生的失败; 真实行为是成功并嵌套, 而 Step 4 新写的三条断言在嵌套后全部为真
- **[minor] `SKILL.md:249`** — Step 3 的 `{YYYY-MM-DD}` 无来源定义; 且目标父目录 `openspec/archive/` 不存在时 git mv 硬失败, 三分支错误表未覆盖这一支
- **[minor] `SKILL.md:282`** — B-14 修掉的悬空引用同字面还剩两处未修, 其中一处就在本次改过的 phase-d-closer/SKILL.md 里

> ⚠️ **其中一条我复核后判定反驳席杀错了**: 「C-3/C-8/C-10 三项『留实跑输出』的验收全部勾了, 但仓内没留下任何一态的输出」。
> 验收逐字写「留证」, 而证据只在对话里 —— 对话会消失。**已按成立处置**, 补 `evidence/phase-b-probe-runs.md` (12 态, 脚本重新实跑生成)。
> 依据: 本 session 已确立「反驳席的 `refuted=true` 不是终审」。

## 完备性批评席新增 (10 条)

| 严重度 | 位置 | 结论 | 处置 |
|---|---|---|---|
| Critical | `SKILL.md:378` | 输出契约残留 `wrong_dir_cleaned: true` —— 与已被判 Critical 的 `cli_bug_fixed` 同一个类, 距修复它的那一行只有 7 行, 逃出同一张 grep | ✅ fixed |
| Major | `proposal.md:196` | 加断言 4 的洞见只落到 Step 4 正文, 没落到 SC-3(c) 钉死的示例字面 / tasks.md B-8a / 交付的示例行 —— 三处仍写「三条断言」 | ✅ fixed |
| Major | `check_bare_issue_refs.py:74` | 白名单外置引入了静默的 cwd 依赖 —— Spec 自己规定的落地前必跑自检, 换个 cwd 就红两条假阳性 | ✅ fixed |
| Major | `proposal.md:18` | 规格描述的封闭豁免集 (a)/(c) 与落地脚本已不是同一套; 新增的主仓交付物 `.aria/bare-issue-ref-allowlist.txt` 在 proposal/tasks 里零登记 | ✅ fixed |
| Major | `check_bare_issue_refs.py:30` | QUALIFIED 的左边界 lookbehind 把 CJK 当 `\w` —— 中文紧邻的全限定引用被判成裸引用, 与脚本自己 docstring 的豁免 (a) 矛盾 | ✅ fixed |
| Major | `2026-09-07-archive-gate-drift-phase-b-landed-blocked-on-two-owner-gates.md:84` | handoff 声称 28 条存活 finding「全部处置」, 但仓内无任何逐条处置台账, 且唯一可机械核验的那条 Major 既没修也没记为驳回 | ✅ fixed |
| Major | `evals.json:58` | 「CLI 漂移类级收口」只扫了 4 个文件; integration-tests 套件里同类的归档路径断言与 CLI-bug 语料无人扫、无人开单, 而它正是 Rule #6 闸门要评的语料 | ✅ fixed |
| minor | `SKILL.md:323` | SHA 回链替换模板把「7-40 位十六进制」这个写给 AI 的约束写进了发到 Forgejo issue 的正文 | ✅ fixed |
| minor | `phase-b-probe-runs.md:4` | 新增留证文件的出处头标错版本 —— 声称 aria `2b67ac6`, 而添加它的同一个 commit 把 gitlink 推到了 `d650f8d` (三个探针全被重写) | ✅ fixed |
| minor | `SKILL.md:417` | 示例 1 输出段留下两行取值完全相同的输出 (`📍 位置:` 与 `📦 归档路径:`) | ✅ fixed |

## 批评席给的三条可证伪放行判据 — 当前取值

| # | 判据 | 现值 |
|---|---|---|
| 1 | `grep -c 'wrong_dir_cleaned' SKILL.md` == 0 | **0** ✅ |
| 2 | Step 4「四条断言」在四处一致 (SKILL.md 正文 / 示例行 / proposal SC-3(c) / tasks B-8a) | **四处一致** ✅ |
| 3 | 换 cwd 跑 `check_bare_issue_refs.py` 仍 rc 0 | **rc 0** ✅ (清单改为从被扫文件向上找) |

## 没人审的面 (批评席枚举, 已全部落地或显式声明)

- **The fix round itself.** All 6 seats reviewed aria `2b67ac6` + main `d2d93da`. The tree has since moved 4 commits: aria `d650f8d` (216 lines — all three probes rewritten, SKILL.md Step 3/4/7 restructured, CHANGELOG re-done) and main `539f875` (new evidence file + new `.aria/bare-issue-ref-allowlist.txt` + spec corrections) + 2 handoff commits. `git -C /home/dev/Aria/aria log --oneline master..HEA
- **A third aria commit nobody was told about.** The branch carries `3a28339 fix(phase-d-closer): 补 conftest.py`, which adds `skills/phase-d-closer/tests/conftest.py` and moved the suite baseline 2111→2122. It appears in the net diff `301641b..d650f8d` but in neither reviewed commit's `--stat`, so the code-reviewer seat's 'no scope creep' verdict was computed on an incomplete file set.
- **Net diff against the true release baseline** `301641b` (= aria master = v1.71.1) rather than against the two named commits. `git -C /home/dev/Aria/aria diff --numstat 301641b d650f8d` — 15 files, confirms CHANGELOG CRLF was genuinely restored (20+/0−, 92/92 CRLF lines) and surfaces the extra conftest.py.
- **Provenance and reproducibility of `evidence/phase-b-probe-runs.md`** (added by `539f875`, no seat saw it). I re-ran all 12 states against the *shipping* scripts, not the ones the file names.
- **Disposition audit** — is the handoff's claim '28 条存活, 全部处置' true? No per-finding ledger exists anywhere (`ls /home/dev/Aria/.aria/audit-reports/` has nothing for this round).
- **Concurrent-track collision at branch level.** Enumerated every local+origin ref and diffed `master...<ref>` for `.aria/state-checks.yaml` and the `aria` gitlink — only this branch touches either. Clean.
- **Already-archived historical corpus** vs the new Step 4/6 assertions: 145 dirs under `/home/dev/Aria/openspec/archive/`, 1 without a `YYYY-MM-DD-` prefix, 0 missing top-level `proposal.md`, 117 missing `detailed-tasks.yaml`. New assertions are forward-only, so no retroactive breakage — clean.
- **Rollback / merge-order coupling** between the main-repo check registration and the submodule script it invokes.
- **The AB/benchmark corpus** (`/home/dev/Aria/aria-plugin-benchmarks/`) — the surface the mandatory Rule #6 gate will actually grade against. Never swept by SC-1, never audited by any seat.
- **Rule #6 / SC-7 ship-gate readiness** — whether the mandatory benchmark can even run.

## 仍未解除的 ship 阻塞 (与本轮无关, 需 owner)

1. **`SC-11` owner 裁定** — ⛔ 挡 E-7a 起全部步骤 (含子模块双推, 不可逆)
2. **`ARIA_COORDINATION_NO_PUSH` 进程级前置** — ⛔ 挡 E-2 起全部步骤 ⇒ 按 Rule #6 连带挡 E-4 起的发版

批评席独立复证了第二条: `ls aria-plugin-benchmarks/ab-results/ | grep archive-skill-drift` 零命中,
SC-7 要求的 `RESULT.md` 不存在; 且本次改动动了 `openspec-archive` 的 frontmatter `description`,
按 Rule #6「`description` 或指令流程变动一律照跑」, AB 是硬前提。
