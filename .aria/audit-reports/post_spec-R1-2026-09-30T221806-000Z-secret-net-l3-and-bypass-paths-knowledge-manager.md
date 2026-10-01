---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-01T00:22:58.385Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — knowledge-manager 席 (文档与规范一致性)

## 已实读文件

被审对象 (全部实读):
- `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 全文 1-365 行; `baseline_probe.py` 1-100、793-960 行及函数结构; `baseline-evidence.md` 头部 1-30 行, 并把第 29-407 行与我在私有副本上独立复跑的 stdout 做了 `cmp`。
- 三个 issue 正文与评论 (scratchpad/issues 下三份); 另对 `10CG/aria-plugin#131`、`10CG/aria-plugin#92` 做了只读 GET (Spec 未引用, 见 m8)。
- 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; CLAUDE.md 规则 #6 / #7 / #10 与「多远程推送」两条硬约束 (派单上下文已载入)。

规范与源码 (按需实读, 行号以我实读为准):
- standards: `skill-benchmark-exemption.md` 全文; `content-integrity.md` §4.1-§4.5; `secret-hygiene.md` 全文 1-404; `configured-gate-authority.md` §5; `version-management.md` §2 / §4.3 / §5.1; `changelog-format.md`; `openspec/templates/proposal-minimal.md` 与 `README.md`; `openspec/project.md` Level 表; aria 侧 `spec-drafter/LEVEL_GUIDE.md` 与 `SKILL.md` A.1.0。
- aria 268da8f: `hooks/secret-scan.sh` 全文; `hooks/secret-guard.sh` 的 1-140、405-427、491-493、564、612-700、734-738、782、815、865-878、893-894、928-934、974、1005-1011、1036-1103 行; `hooks/hooks.json` 全文; 两个测试文件的头注释与被 Spec 引用的行; `.github/secret_scanning.yml`; `CHANGELOG.md` 1-80 与 [1.66.4] 条; `VERSION` 1-18、150-175; `README.md` / `README.zh.md` 的 hook 行; `check_bare_issue_refs.py`、`linked_issue_field_probe.py`、`phase1_gate.py` 的 `--linked-issue` 部分、`lib/collision.py` 的 `linked_issue_overlaps`。
- 主仓: `.aria/state-checks.yaml` 版本类各 check; `git show --stat` 加 diff 看 72cb02b (v1.74.1) 与 a99dd8d (v1.74.0) 两次发版同步提交, 以及 aria 的 26e644e / 1ad31fa; `openspec/archive` 下 2026-06-19 / 07-03 / 08-02 / 08-18 / 08-22 先例的 Level、rule6_note 与 Rule #7 段; `openspec/changes/pre-merge-completeness-gate-change-scope` 的头部、待 owner 复议与 `detailed-tasks.yaml:336-356`; `docs/handoff/2026-08-20-issue-batch-181-147-145-ship-and-gate-blindspot.md:72`。
- 研究笔记只做了定向 grep (secret-scan.md 前 30 行、precedent.md 若干行), 未通读; 它们是背景材料, 本报告结论不依赖其内容。

独立复核 (无异议项, 供其他席免重复):
1. 复跑 `baseline_probe.py` (aria 268da8f + standards 2bc1c4c 的私有副本): stdout 与 `baseline-evidence.md` 第 29-407 行逐字节相同 (sha256 前 16 位 `1ab63a323da13f45`, 41873 字节); 逐 SC 对照 proposal 的 `×N` 与探针行数, 32 个 SC 的类别计数全部吻合, 共 326 行。
2. `check_bare_issue_refs.py` 对 proposal.md 与 baseline-evidence.md 均 rc 0 (裸引用 0); 带圈数字自查命令零输出; `linked_issue_field_probe.py` 对 proposal.md 输出 OK。
3. 全文引用的 15 个 issue 号 (`10CG/aria-plugin#132/#138/#140/#142/#153/#154/#203/#207`、`10CG/Aria#136/#154/#170/#179/#199/#221/#223`) 与 open-issues 缓存及仓内先例逐个核对, 仓别与主题均对; `10CG/Aria#154` (readarray / bash3 会话死锁) 与 `10CG/aria-plugin#154` 没有混淆。
4. 约 30 处 `file:line` 引用 (secret-scan.sh `:135-144` `:152-231` `:224` `:227` `:355-367`; secret-guard.sh `:405-408` `:427` `:491-493` `:564` `:617-624` `:641` `:698-700` `:736` `:782` `:815` `:893-894` `:930-933` `:974` `:1043-1071` `:1088-1102`; 测试 `:11` `:1620-1622` `:2018-2030`; secret-hygiene.md `:23` `:287` `:288` `:319` `:285`) 全部与实读一致; PATTERNS 实为 31 条。
5. W13 的 curl 示例本机实跑: `curl -K -` 读 stdin 配置得 exit 7、空配置得 exit 2, `curl -H @文件` 得 exit 7 (参数被接受), 与 Spec 所述相同。`host-docker-logout-guard.test.sh` 确实写外层 HOME 的 `guard-bypass.log` (284 字节, 0 个换行), 与 W6 / 待复议 7 第 12 条一致。
6. 三个文件做了 Rule #7 形状扫描: 无凭据形状字面量 (仅 SHA 与目录名命中长串)。

## Findings

### Critical

#### C1 · id e8d39a8a · critical · issue · implementation
- scope: `proposal.md What.W3` (`:74-83`)
- summary: W3 把 `$`、`<`、`{{` 当整体前缀放行并延伸到既有 `json-secret-field`, 使基线可检出的真实形值 (典型: JSON `password` 里的 `$2b$12$…` 口令哈希、`$` 起头的人工口令) 由告警变静默, 而 Spec 的验收与已知限制都放过它。
- 证据:
  1. W3 `:77`: 前缀集含 `<`、`$`、`{{`, 「被放行的 span 仍被计数哨兵替换, 后序 tag 看不到它」; 已知限制 `:83` 只写「以白名单词开头的真凭据会被放过 (须人为构造)」, 没提符号前缀。
  2. 基线实测 (私有副本, 值运行时生成不打印; 脚本 `<我的目录>/w3_prefix_probe.py`): JSON `password` 取 `$2b$12$` 加 53 字符、取 `$` 加 12 位字母数字、取 `<` 加 12 位字母数字加 `>`, 以及 `client_secret` 取 `{{` 加 20 位字母数字加 `}}`, 四条全部检出 `json-secret-field=1`; 对照 `password_hash=<同形 bcrypt>` 检出 `bcrypt-hash=1`。
  3. 按 W3 字面做原型 (脚本 `<我的目录>/w3_simulate.py`: 只对 `json-secret-field` 套用前缀规则, 被放行 span 仍换成哨兵): 上述四条中前三条 `password` 形态全部变静默, 第四条 `{{…}}` 也静默; 对照「12 位字母数字加 `!`」仍告警。同一把 bcrypt 哈希裸出现仍告警 (`bcrypt-hash`), 包进 `"password"` 键反而静默, 原因是后序 `bcrypt-hash` 看不到已被哨兵替换的 span。
  4. 验收放过: SC-7 (`baseline-evidence.md:77-83`) 与 SC-11 (`:112-132`) 的真阳性行只有 12 / 16 / 32 位字母数字或带 `!` 的值, 没有任何 `$` / `<` / `{{` 起头的真值行。
- 失败场景: 实现者按 W3 字面写前缀 `case`, 全部 326 行探针与既有 49 条用例都过; 发布后 psql 或 API 导出的 `{"password":"$2b$…"}` 不再告警 (基线告警)。这是「检出变放行」的安全回退, 且与审计锚点「不引入任何安全回退」相悖。
- 建议修法: 把 `$` 收窄为变量 / 命令替换形 (`$` 后接 `{`、`(` 或字母下划线), `<` 与 `{{` 要求成对闭合 (值以 `>` / `}}` 收尾); 新增 reverse-guard 行 (JSON `password` / `client_secret` 取 `$2b$12$…`、`$6$…`、`$argon2id$…` 形值仍为 `json-secret-field=1`); 已知限制补一句「`$` 加字母起头的口令会被当变量引用放过」。同一原型上, 收窄写法保住 SC-11 全部占位行静默 (`${VAR}`、`{{ … }}`、`<prose>`、`FAKE_…`), 同时保住 `$2b$` 形检出。

### Major

#### M1 · id 5831f8c0 · major · issue · testing
- scope: `proposal.md SC-26` (`:243`)
- summary: SC-26 两条判据是「全文件任一行同时含若干子串」, Spec 自己要求追加的版本历史行即可单独满足, §2.5 行与正例条款不写也绿。
- 证据: `baseline_probe.py:815-827`: `_sot_clause` 为 `any(all(k in l for k in ("命令行参数","env","--config","stdin")) for l in t.splitlines())`, `_sot_ps_row` 为 `any("pgrep -a" in l ...)`, 都不限节。我在私有副本上只追加 Impact `:292` 要求的 `| 1.2.0 | … |` 版本历史行 (行内复述进程表族与「凭据不要放命令行参数, 改用 env / --config / stdin」), 两条判据由基线 False / False 变 True / True; 而 `pgrep -a` 实际并不在 §2.5 内 (节内检查为 False)。
- 失败场景 / 三态: 基线红 (clause-absent、ps-family-row-absent); 目标绿; 坏实现 (只写版本行) 也绿。W13 把 `10CG/Aria#221` 的「拒绝文案加一句」改落 SOT, SC-26 是这条诉求唯一的落地验收, 放过它等于诉求静默丢失。
- 建议修法: 判据按节取块: §2.5 块内要有 `pgrep -a` 行; 正例条款要落在 §3 块内且排除 §10 版本表; 加一条坏实现行 (只改版本表) 必须红。

#### M2 · id ba98e41f · major · issue · documentation
- scope: `proposal.md Impact.同步面` (`:292`)
- summary: Impact 列的主仓版本点与发版同步面少列实际必改项: 近两次发版同步提交各改 8 个内容文件、16 个版本点, Spec 只点名其中约 4 个, Tasks 也没有承载主仓同步面的任务行。
- 证据: `git show --stat 72cb02b` (v1.74.1; 提交说明写明「16 个版本点」): `CLAUDE.md`、`README.md`、`README.zh.md`、`README.ja.md`、`README.ko.md`、`VERSION`、`system-architecture.md`、`version-scheme.md` 加 gitlink。16 点 = `README.md` `:8` `:242` (2) + 三份 i18n README 各 `:3` translated-from、`:10` badge、`:244` 版本行 (9) + `VERSION:24` + `system-architecture.md:189` + `version-scheme.md:23` + `CLAUDE.md:138` `:142`; a99dd8d 同形。Spec `:292` 只列 `VERSION`、root README badge、两处架构文档版本行。`.aria/state-checks.yaml` 的 `i18n-readme-translation-currency` 要求三份 translated-from 标记等于 plugin 版本; CLAUDE.md 两处没有任何机械 check 兜底 (state-checks 里涉及 CLAUDE.md 的只有 `m6-claude-md-version` = 2.0.0 与卫生预算)。aria 子模块侧「README 只在描述变化时改」与 26e644e 不符: `README.md` / `README.zh.md` 每次发版各改一行版本与发布日期。
- 失败场景: 任务按 Impact 字面做完, 三份 i18n 标记留旧版本 → `i18n-readme-translation-currency` 报 STALE (severity warning); CLAUDE.md 两处留旧版本 → 无任何 check 报, 静默过期 (违反 Rule #3)。
- 建议修法: 同步面写成 16 点清单 (或直接指向 72cb02b 的文件集), 点名 `m6-version-badge-match` / `i18n-readme-translation-currency` / `plugin-version-arch-docs-match` / `main-project-version-consistency` 须复跑、CLAUDE.md 两点须人工; Tasks 增一行承载主仓发版同步面; 改正 aria 侧 README 的表述。

#### M3 · id b73ab606 · major · issue · documentation
- scope: `proposal.md What.W9/W13/W14` 与 SC-26 / 27 / 28
- summary: 新增的采用方入口 `.aria/secret-guard.paths`、Spec 自称「对外表述为部分覆盖」的已知限制、以及五向行为变更申报, 都没有指定文档落点, SC-26 / 27 / 28 也不验。
- 证据: proposal 中 `secret-guard.paths` 只出现在 W9、SC-19、Impact、待复议, 没有任何一处写它的文档落点。W13 / W14 / SC-26..28 的文档动作只有: §2.5 一行、一条正例、三处 secret-guard 计数加一处 secret-scan 计数、§5.1 勘正、9 处陈旧表述、两个 change-id。对照仓内先例: `.aria/bare-issue-ref-allowlist.txt` 同时记在 SOT (`content-integrity.md` §4.4) 与脚本 docstring (`check_bare_issue_refs.py:20`); `10CG/Aria#179` 把「已知限三类」写进 hook 头注释 (`secret-guard.sh:38-56`、`:113`), CHANGELOG [1.66.4] (`CHANGELOG.md:415-427`) 带漏报修复 / 误报收敛 / 测试增量三段; `secret-hygiene.md` §5.1 `:287` 的括号逐变更列出新族。W10 `:144` 要求「对外表述为部分覆盖, 不宣称根治」, 但没写对外落在哪。`secret-scan.sh` 头注释 `:42-53` 的 Scope 清单也不在 W14 的 9 处里。
- 失败场景: 实现者做完全部 SC 仍绿; 采用方不知道有扩展文件 (字面子串、4-200 字符、32 KiB、200 条、CRLF、失败静默), 也读不到放行面 (`systemctl status`、`docker inspect`、数组赋值、跨调用变量等), 把「已拦」当「已治」; CHANGELOG 不带「`ps aux | grep` 现被拦」的行为变更说明。
- 建议修法: 补 doc-sync SC: (a) `secret-hygiene.md` 新增小节写 `.aria/secret-guard.paths` 的位置 / 格式 / 只增不减 / 失败整体忽略 / 未被 aria-doctor 校验; (b) 两个 hook 头注释收录 W8 / W10 / W11 / W12 的 KNOWN-LIMIT (按 SC 编号); (c) CHANGELOG 新节含五向行为变更与 rule6_note; (d) §5.1 `:287` 括号补新族; (e) `secret-scan.sh` 头注释 Scope 清单补 6 个新 tag, 且不再写带数字的计数句。

#### M4 · id cf0ae932 · major · issue · documentation
- scope: `proposal.md` 全文 (研究笔记引用)
- summary: Spec 把四份「研究笔记」及其原型 / 普查 / 矩阵当证据引用约 47 处 (40 行), 这些材料只在会话 scratchpad, 不在仓内也无落点声明; 归档后全部悬空, 且「在同一语料上复跑」不可执行。
- 证据: 笔记在 `/tmp/claude-1000/-home-dev-Aria/…/scratchpad/research/` (cc-hooks 6.9 KB、precedent 55 KB、secret-guard 46 KB、secret-scan 80 KB); `git ls-files | grep -i research` 无; 全仓 grep 其独有内容 (如「163/163」) 只命中 Spec 自身与无关旧文件。proposal 直接点名「…笔记」26 次, 另有「研究原型 / 普查 / 矩阵 / 实测」21 次。承重样例: W1「163/163 样本同形」、W3「precedent 笔记 §6.4」、W4「§1.7」、W8「2700 条 docs 语料」、W9 / W10「研究原型 24/24」、W12「465 条探针里 108 条由拦变放」、待复议 7 的 16 条全部「附证据位置」(均指笔记章节)。仓内先例: `openspec/archive/2026-08-18-secret-guard-per-segment-evaluation/proposal.md:438` 明写「复现命令内联 (R2 knowledge M-2: 不得只引用未提交的审计报告)」; `content-integrity.md` §4.1 禁引用不存在的文件。仓内已有可替代源: L2 wrapper 占位 `[REDACTED-BY-WRAPPER len=N]` 见 `docs/handoff/2026-08-20-issue-batch-181-147-145-ship-and-gate-blindspot.md:72`。
- 失败场景: R2 起的席位或 B.1 的实现者 (可能是别的容器) 无法核验 W1 / W3 / W8 / W9 / W10 / W12 的承重数字; B.2 无法按执笔自报薄弱点 3 所说「在同一语料上复跑」W2 误报率 (普查脚本与语料定义不在仓内); 待复议 7 获批开单时无证据可附。
- 建议修法: 三选一或并用: (a) 承重笔记条目入库为本 change 目录附件 (先过 Rule #7 形状扫描), Spec 改引附件路径; (b) 承重事实改指仓内可达源 (源码 `file:line`、handoff、SC 行); (c) 普查脚本与语料清单 (含 git SHA) 入库。待复议 7 每条内联最小复现命令。

#### M5 · id 846b21f8 · major · issue · documentation
- scope: `proposal.md What.W13` (`:177-182`)
- summary: W13 新增的「凭据不要放命令行参数」正例与同一 SOT 现有推荐示例直接冲突 (§3.1 / §3.2 / §3.4 / §3.5 / §4.4 都把值放在 argv 的 `KEY=…`), Spec 没有安排对账, SC-26 也测不出。
- 证据: `secret-hygiene.md:135`、`:151` (`f'KEY={value}'`), `:178`、`:210`、`:267` (`KEY="$VAL"`) 均为被标 ✅ 推荐的示例; SOT 现无任何 argv / 进程表字样 (grep 空)。本机 nomad v1.11.2 `nomad var put -h`: 「Item values provided from file references or stdin are consumed as-is」, 即 `@文件` 或 `-` 可行。W13 `:180` 只写加 §2.5 一行与一条正例。
- 失败场景: 落 W13 后 SOT 一边说「值别放命令行参数」, 一边把 `nomad var put … KEY="$VAL"` 标为推荐; 读 SOT 的 AI 照 §3.4 写出的正是 `10CG/Aria#221` 描述的形态 (值在 argv, 进程表可见)。版本行写「additive」也不实, 需要 Amend 既有示例。
- 建议修法: W13 增「对账」项: 把 §3.1 / §3.2 / §3.4 / §3.5 示例改为 `KEY=@<文件>` 或 stdin (逐条以 `-h` 实跑为据), 或加 argv 暴露窗口警示; SC-26 增机械判据 (SOT 示例块内不再有把秘密值放进 argv 的 ✅ 示例)。

#### M6 · id 2779a016 · major · issue · documentation
- scope: `proposal.md Impact.issue 收尾口径` (`:294`) 与待复议 3 (`:332`)
- summary: 对 `10CG/aria-plugin#203` 与 `10CG/Aria#221` 的 ship 后评论, Spec 默认取「理解 A」(照常评论代码侧进展), 与决策单第 2 项执行注的字面「相关 issue 保持 open、本项之下不评论」相反, 并声明「未裁前按默认执行」。
- 证据: 决策单 §2 执行注: 「不产出轮换清单, 不逐条提示轮换; 相关 issue 保持 open、本项之下不评论」, 其「范围」点名 `10CG/aria-plugin#203` / `10CG/Aria#221` / `10CG/Aria#170` / `10CG/Aria#136`。Spec `:294` 与 `:332` 默认 A, `:326` 写「未裁前按「默认」执行」。字面读法上, 「本项之下不评论」若只指「不就轮换话题评论」, 就与前一分句「不逐条提示轮换」重复, 它新增的信息只能是「不评论」本身; 决策单 §4 的评论授权是通则, §2 的例外针对点名 issue。
- 失败场景: Tasks 1.11「issue 收尾 (按 Impact 口径)」到时无人再问, AI 在 owner 账号下向两张安全 issue 发评论 (外向动作, 不可无痕撤回), 与字面指令相反。歧义的否定性指令不构成放行, 默认应落在更保守一侧。
- 建议修法: 默认翻到理解 B (203 / 221 本 Spec 内不评论; 代码侧进展写在 `10CG/aria-plugin#154` 关闭评论、PR 描述与 handoff, 待 owner 裁后再补); 或把默认改成「未裁前不执行该动作」。

### Minor

#### m1 · id b7387216 · minor · issue · documentation
- scope: `proposal.md Impact.覆盖关系` (`:294-295`)
- summary: 「`10CG/aria-plugin#154` 全覆盖 / 三件交付物全部落地」与 W2 / W4 对评论 19339 字面参数的有意偏离不符。
- 证据: 评论 19339 第 1 件为 `"[^"]{8,}"` 且键含 `token` `sha1`, W2 对这两键定 16, SC-10 10c 把 12 位 `token` 钉成静默; 第 3 件「命中值以 sha256 前 8 位入日志」, W4 对短于 16 位的值只记长度。
- 失败场景: 关单评论沿用「全覆盖」, 对 issue 作者与后来读者不实。
- 建议修法: 覆盖关系写成「全覆盖, 两处有意偏离: …」, 关单评论逐条披露。

#### m2 · id d8e2f426 · minor · issue · documentation
- scope: `proposal.md Impact.同步面 / What.W5` (决策单复述)
- summary: 决策单复述不精确: 授权边界少列两类, 「四枚待轮换凭据」把四张 issue 当成四枚凭据。
- 证据: Impact `:292` 只列「合并 master、推 master、tag、发版」, 决策单 §4 的边界为五类, 少「主仓 PR 的合并」「删除远端分支」; W5 `:97` 的「四枚待轮换凭据 (…四个 issue 号)」, 而 `10CG/Aria#221` 自述三枚凭据。
- 失败场景: 合并后顺手删远端分支或合并主仓 PR 时, 以为在授权内。
- 建议修法: 直接引决策单 §4 / §2 原文, 或改写为「四张 issue」。

#### m3 · id 8e1df30a · minor · issue · documentation
- scope: `proposal.md Impact.版本定级` (`:285`)
- summary: 版本定级依据误引 CLAUDE.md。
- 证据: Spec 写 CLAUDE.md §版本管理为「新增能力 = MINOR+」, 原文是「新增 Skill / Skill 架构重构 = MINOR+; 文档更新 / bug 修复 = PATCH」; 本族先例 v1.66.3、v1.66.4 (新增拦截族) 为 PATCH (`aria/VERSION:19-20`)。MINOR 的合理依据是 `version-management.md` §2.2「功能增强 (向下兼容)」加新输入面。
- 失败场景: owner 拿误引的依据裁号。
- 建议修法: 改引 §2.2 并写全 PATCH 先例的区别; 号仍由 owner 裁。

#### m4 · id 852deadc · minor · issue · testing
- scope: `proposal.md Impact.与 10CG/Aria#199 的接缝` (`:293`)
- summary: 接缝守卫命令用了 `10CG/Aria#199` 已淘汰的弱写法。
- 证据: Spec 写「主仓根 `git grep … | grep …` 无输出」; `10CG/Aria#199` 的 `detailed-tasks.yaml:342` (post_planning R5 R5-M4) 已改为 `git -C <主仓根> grep …; echo "rc=${PIPESTATUS[0]}"`, 并写明不带 `-C` 在子目录跑会「退出 1 且无输出, 真空通过」、rc 非 0 / 1 即没跑成。
- 失败场景: 在 `aria/` 子目录或 git 失败 (rc 128) 时「无输出」同样空过。
- 建议修法: 直接引用该 TASK 的守卫命令与判据, 不复述。

#### m5 · id 381efd94 · minor · risk · documentation
- scope: `proposal.md 执笔自报薄弱点` (`:311-322`)
- summary: 该节是 v1 时点的审计叙事, 不是 Spec 交付面, 随修订必然过时。
- 证据: 10 条里 1、2、3、4、5、7、10 在 B.1 / R2 即变化 (如 1「SC-30 没有探针基线」B.1 实测后不成立)。仓内先例: `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` 因审计叙事与交付面同居一文长到 295 KB。「待 owner 复议」与 rule6_note 与该 Spec 同构, 属惯例, 不在此列; 除本节外正文均为规范性内容。
- 失败场景: 后续轮次不断往这一节追加, 重演同居一文的耦合。
- 建议修法: R1 表态后把本节移出 (派单 / handoff), 或加「v1 时点, 不随修订同步」声明。

#### m6 · id 0f70cf57 · minor · issue · documentation
- scope: `proposal.md header Level 对账` (`:11`)
- summary: Level 对账只引 LEVEL_GUIDE 一条且是合并转述, 未列模板的另两条升级判据, 待复议 4 的选项依据不全。
- 证据: `LEVEL_GUIDE.md:155-162` 是两行 (条件清单含「影响多个子模块」, 下一行「跨模块 → 自动提升为 Level 3」), Spec 把它们并成一句加引号; `proposal-minimal.md` 升级判据含「Changes affecting > 10 files」(本 Spec 触碰 aria 10 个 + standards 1 个 + 主仓 9 个 + Spec 目录 3 个文件, 合计超过 20) 与 `project.md` Level 表「Medium features (1-3 days)」(本 Spec 326 探针行、14 个工作项、11 个任务)。
- 失败场景: owner 复议 Level 时看到的判据被收窄。
- 建议修法: 对账补这两条, 结论仍按决策单第 3 项执行。

#### m7 · id 67e73dab · minor · risk · documentation
- scope: `proposal.md What.W13` (BLOCKED 文案)
- summary: 共享 BLOCKED 文案的「Acceptable filters」把 `| grep '^SAFE_PREFIX='` 列为可接受, 而 tight 族对它仍拦; Spec 把 tight 族由 1 个增至 4 个并冻结文案, 却没记录这处不一致。
- 证据: 基线实测 (`<我的目录>/tight_mismatch.py`): `cat ~/.claude/settings.json | grep '^SAFE_PREFIX='` exit 2 且 stderr 仍列出该过滤器; 对照 `.env` 同形 exit 0。新增 tight 族: app.ini (W8.4)、进程表 (W11)、扩展入口 (W9)。W13 `:182` 的已知限制只写「被拦的当下 AI 看不到这条建议」; 待复议 2 的三个选项都不含这一点。
- 失败场景: AI 按文案重试 `ps aux | grep '^dev'` 仍被拦, 转向 `# guard:ack` —— 恰是 `10CG/Aria#221` 评论 25898 批评的诱因。
- 建议修法: 在 SOT §2.5 / §3.5 与 hook 头注释 Coverage gaps 记「tight 族只认 discard / count / hash / 名字面」, 并把此点补进待复议 2 的代价对比 (它是选项 C 的收益)。

#### m8 · id a1d19fe7 · minor · issue · documentation
- scope: `proposal.md What.W4 / What.W12`
- summary: W4 与 W12 漏链两个在案 issue, 待复议 7 开单前也未去重。
- 证据: `10CG/aria-plugin#92` (open, 「泄露事件记录 → 人工闸门 → 升级 PreToolUse」): 规划的事件记录就是 L3 日志的读取方, 明写「绝不含 secret 值或原始匹配文本」与「去重」, W4 的「仓内零读取方」论据与 `fp=` 设计应说明与它的关系; `10CG/aria-plugin#131` (open, 「既有 pattern 尾边界缺失」, 明写「收口时须明确取哪个」方向): W12 对 `\.env` 右边界的取舍与「465 条探针 108 条翻转」正是它要的输入。Spec 全文无这两个号 (grep 零命中)。
- 失败场景: 后续对 #92 的设计与 W4 的日志字段各走各的; 对 #131 重复立案。
- 建议修法: W4 / W12 各加一句关联与处置; 待复议 7 开单前对 `10CG/aria-plugin#131` / `#139` / `#143` 去重。

#### m9 · id b63b7640 · minor · risk · documentation
- scope: `proposal.md rule6_note / Rule #7`
- summary: Rule #7 申报散落, 且 post-ship 腿的取值规程缺失。
- 证据: Spec 全文无「Rule #7」字样, 实质措施散在 `:22`、`:102`、`:206`; 仓内同类先例 (`openspec/archive/2026-06-19-secret-guard-exfil-coverage-iteration/proposal.md:55`) 有一行集中申报。rule6_note 块 A 的 dogfood 要求 ship 后经 harness hook 链复验 L3, 而 L3 复验必须让「像凭据的值」出现在真实会话输出里, Spec 没写这一腿如何守 Rule #7。
- 失败场景: 实现者因 Rule #7 卡住, 或临场自创取值方式。
- 建议修法: 加一行集中申报; 写明 post-ship 腿只用运行时生成的合成值, 以及是否需要 `# secret-leak-ok-explicit` 三件套。

#### m10 · id a6304dd1 · minor · issue · testing
- scope: `proposal.md SC-28` (`:245`)
- summary: SC-28 的 9 条陈旧表述判据只验「旧串消失」, 删除即绿, 不验「改为」; 计数句被替换成新字面数字会重演陈旧计数。
- 证据: `baseline_probe.py` 的 `doc_absent` (只判 `needle not in text`); 28b 要求改指 `secret-hygiene.md`、28f 要求换成真实 `file.content` 形, 判据都不验; 28c / 28d 把计数句「替换」而不禁新计数, 而 `secret-guard.test.sh:11` 已有「stale count 误导过一次 spec」的专门警示。
- 失败场景: 直接删句通过; 换成新数字后下次增删用例再陈旧。
- 建议修法: 增 present 判据 (28b 含 `secret-hygiene.md`; 28f 含 `file.content`), 并禁止在 hook 头注释写 pattern / 类别总数字面。

## 对执笔人自报薄弱点与请裁项的表态

执笔自报薄弱点:
1. SC-30 没有探针基线: 可接受。B.1 入场实测 (Task 1.1) 合理; 建议实测值同时回填 SC-30 一行 (handoff 随会话, Spec 是后续审计的锚)。
2. 目标态文本自扫描只能 B.2 验: 可接受。SC-15 15e / 15f 即 B.2 闸; 基线只证明现行 hook 静默, 执笔已如实声明。
3. W2 终版设计未在语料上普查: 可接受, 条件是普查脚本与语料定义入库, 否则「B.2 同一语料复跑」不可执行 (见 M4)。
4. W11 外壳包裹形态无原型: 可接受。SC-22 的 35 条 baseline-failing 行是强证伪器, 做不出会红。
5. W9 项目根语义: 可接受; 条件是回落顺序与 `cd` 漂移写进文档落点 (见 M3)。
6. SC 钉得很紧: 可接受。证伪性要求如此; 换措辞 / 换 tag 名本就是 Spec 变更。
7. 用例规模、两边对照: 可接受。我已逐 SC 对照, proposal 的 `×N` 与探针 326 行 100% 吻合。
8. rule6_note 块 B 归类: 可接受 (带条件): 插入严格只含事实 (SC-13 13d / 13e / 13f 钉住); CHANGELOG 写「AI 自行判定, 已交接请 owner 复议」(v1.74.1 先例); 若 owner 判处方性, 按 SOT §3 三件套, 其中「开套件缺口 issue」不在一次性授权内, 须逐次请示。
9. Level: 可接受 (honest, owner 已裁, 已列复议); 判据列举不全, 见 m6。
10. `linked_issue_overlap == []` 取自派单: 可接受; 主控已核协调 ref。

待 owner 复议 (产品级 1-7):
1. L3 脱敏: 可接受 (默认 A, 选项 B 先 spike); 平台事实已标「端到端未验证」。
2. 拒绝文案: 可接受 (默认 A); 选项集补 m7 一点。
3. 203 / 221 收尾评论: **不可接受 (默认方向)**。理由见 M6, 默认应为「不评论」。
4. Level: 可接受 (维持 2); 见 m6。
5. 进程表习惯变化: 可接受。默认是更保守一侧, 代价已申报, 可由 owner 放宽。
6. 版本定级: 可接受 (MINOR 为建议); 依据见 m3。
7. 建议开单清单: 可接受 (清单本身), 条件: 内联复现命令、证据可达 (M4)、开单前去重 (m8)。

待 owner 复议 (技术级 8-17):
8. rule6_note 两块: 可接受 (见上)。
9. W2 键表 / 16 门槛 / 熵下限: 可接受; 与评论 19339 的偏离须在关单时披露 (m1)。
10. W3 值前缀白名单: **部分不可接受**。「按值前缀、大小写敏感、作用于 6 个新 tag 加 `json-secret-field`」的方向可接受; `$` / `<` / `{{` 的宽度不可接受 (C1)。
11. W4 指纹: 可接受; 与 `10CG/aria-plugin#92` 的关系须说明 (m8)。
12. W7 夹具源头拼装: 可接受。
13. W8 只做 app.ini 族: 可接受。
14. W9 纯文本加字面子串加失败整体忽略: 可接受; 文档落点缺 (M3)。
15. W11 拒绝加 tight: 可接受。
16. W12 边界字符类: **不可接受 (作为技术级 AI 已裁)**。理由: python3 / node / lua 读 `.env_prod` 由拦变放, 与审计锚点「不引入任何安全回退」冲突, 应由 owner 明裁风险接受, 或改取 `[^A-Za-z0-9]` (实测零回退, 见风险 1)。
17. 探针在无 git 副本上跑: 可接受。

## 风险 / 疑问

1. W12 边界字符类。我在私有副本上只改 W12 的三行 (python3 / node / lua 源组), 对比三种写法 (退出码, 2 = 拦):

   | 命令形态 | 基线 | W12 现写法 `[^A-Za-z0-9_]` | 备选 `[^A-Za-z0-9]` |
   |---|---|---|---|
   | `os.environ` / `os.environb` / node `cfg.environment` | 2 | 0 | 0 |
   | python3 读 `.env` / `.env.production` / `.envrc` | 2 | 2 | 2 |
   | python3 读 `.env_prod` / `.env_local` | 2 | **0** | 2 |
   | python3 属性 `x.env_file` | 2 | 0 | 2 (与基线同, 非回退) |

   两种写法对 `10CG/Aria#221` 要求的三个误报修复效果一致; 差别只在 `.env_prod` 类。说明: Read/Edit 面与 `cat` 行今天也不拦 `.env_prod`, 所以现写法与设计名集一致; 但它是非请求性的由拦变放, 且被归为技术级。故只列风险, 不计 finding (Spec 已在 Impact 申报并给了理由)。
2. 公开镜像披露。`git ls-remote https://github.com/10CG/Aria.git` 与 `…/aria-plugin.git` 匿名可读 (实测), 已授权的 feature 分支推送会把 Spec 公开; 待复议 7 第 1 条含「约 1400 个空段使 hook 超时后命令被放行并执行」这类未修复的通用旁路配方。仓内无披露规程, 先例 (2026-08-18 Spec 转出节) 同样公开复现命令, 故不计 finding, 请 owner 知悉是否保留该句。
3. A.1 claim 的 TTL: 认领于 2026-09-30T17:57:13Z, SWEEP_TTL 24h, 约 2026-10-01T17:57Z 起可被扫为 abandoned; 多轮审计加 owner 等待可能越界。心跳属已授权的例行维护, 但 Spec / Tasks 无提示。
4. rule6_note 块 A 的 `decision_table_row: n/a` 可能被读成 2026-08-02 被 owner 否决的「Rule #6 不适用」框定 (该 Spec `:128` 明写); 正文已声明沿用 substitute 框定, 建议再加一句「n/a 指本 Spec 不属 Skill 变更, Rule #6 仍按 substitute 框定适用」。
5. 本席目击: 我的两条 Bash 命令被活体 secret-guard 以「正文引用命令文本」误拦, 一次 Write 被活体 secret-scan 对自写脚本里的占位形字符串告警, 与 W3 / W7 同类, 佐证 FP 面真实存在 (非 finding)。
6. 未覆盖 (留给其他席): `updatedToolOutput` 的平台事实 (未验二进制)、W2 / W10 / W11 的原型可行性、SC-8 延迟闸、aria-orchestrator 侧影响。

## Verdict

- verdict: **FAIL**
- counts: `1C/6M/10m`
- Vote: **REVISE**

## 是否足以进入 A.2

不足以: 1 条 critical (W3 符号前缀白名单造成既有检出回退且验收放过) 加 6 条 major (SC-26 假绿、主仓同步面缺项、文档落点缺失、证据悬空、W13 与 SOT 自相矛盾、203 / 221 评论默认方向), 修订后须重审; 方案主体与 Level 2 (owner 已裁) 不在此列。
