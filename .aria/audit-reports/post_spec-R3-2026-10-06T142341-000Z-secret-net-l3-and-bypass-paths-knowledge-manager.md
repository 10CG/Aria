---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-10-06T16:18:00.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 — knowledge-manager 席 (文档与规范一致性)

## 已实读文件

**被审对象 (全部实读)**
- `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 全文 1-425 行 (c0a6654, 151287 字节); 另读 `git diff --word-diff b3e3123 c0a6654 -- …/proposal.md` 全部 207 行 (v2 到 v3 的逐词改动)。
- `baseline-evidence.md`: 1-60 行与末尾 16 行; 内嵌 stdout 块用脚本取出 (74072 字节, sha256 前 16 位 `a6e187b50a4f3514`, 与文内声明一致) 后逐 SC 对账。`baseline_probe.py`: 1-120、SC-14 与套件运行器 (1496-1592)、SC-26/27/28 文档判据 (1595-1830), 其余按需。

**必读材料**
- 三个 issue 正文与评论 (aria-plugin-154 / aria-plugin-203 / Aria-221); 决策单 `2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; CLAUDE.md 规则 #6 / #7 / #10 与「多远程推送」两条硬约束。
- R2 聚合报告全文 (「全部 finding」表与「主控记录」)、本席 R2 报告全文、另四席 R2 的「风险 / 疑问」节; 执笔 `v3-writer-report.md` 全文; `writer-v3-proto/README.md`; `PROGRESS.md`。

**规范与源码** (aria `268da8f` / standards `2bc1c4c`; 行号以我实读为准)
- standards: `secret-hygiene.md` 全文; `skill-benchmark-exemption.md` 全文; `content-integrity.md` §4.4 / §4.5; `git-commit.md` §6.1 / §8.1; `version-management.md` §2.2; `openspec/templates/proposal-minimal.md`。
- aria: `hooks/secret-guard.sh` 1-118 行头注释与约 20 个被引行号 (`:405-408`、`:427`、`:626`、`:631-700`、`:815`、`:873-877`、`:893-894`、`:930-933`); `hooks/secret-scan.sh` 1-100 行; `hooks/hooks.json`; `README.md` Hooks 两节; `CHANGELOG.md` 顶部; `VERSION:164`; `skills/commit-msg-generator/COMMIT_FOOTER_GUIDE.md:186-204`; `skills/openspec-archive/SKILL.md` Step 7; `skills/state-scanner/scripts/collectors/custom_checks.py:360-385`; `skills/aria-doctor/scripts/check_secret_guard_install.sh`。
- 主仓: `.aria/probes/plugin-cache-currency.py` 全文与 `.aria/state-checks.yaml` 的 16 个 check 名; `.aria/decisions/DEC-20260703-001`、`2026-08-24-sc8-absolute-latency-gate.md`、`openspec/archive/2026-08-02-secret-guard-nomad-var-put-echo` 的 rule6_note; `.aria/cache/issues.json` (22 个被引 issue 的存在与主题)。

**实跑** (全部在 `…/audit/post_spec-R3-knowledge-manager/` 下; HOME / TMPDIR 私有; 像凭据的值运行时生成、不打印; 真仓零写操作、零子代理; 只用了 `git diff|log|show|grep|ls-remote`)
1. 机械检查: `check_bare_issue_refs.py` 对三份文件 rc 0 (裸引用 0), 另用独立正则扫「仓名 + 空格 + #」写法零命中; 带圈数字 / 希腊字母 / 表情 / 控制字节 / CRLF 全为零; `linked_issue_field_probe.py` 对本 Spec 无报告 (`--emit-arg` 为 `10CG/aria-plugin#154`); 执笔的 `xref_check.py` / `check_counts.py` / `sc_counts.py` 在我的副本上复跑: 引用 224 个标记、`SC-n id` 对 166 个全对, 383 行, 各 SC 的 `×N` 与 stdout 相符 (所谓「不一致」都是 11x / 11y / 11z、18f / 18h、20g / 20l 这类只写 ID 不写数量的行)。
2. 独立形状扫描: 自写正则集 (provider 前缀 / JWT / PEM / URL 口令 / 键值赋值 / 头参数形 / 40 与 64 位 hex) 扫 `0748dbc..c0a6654` 新增的全部 119 个文件, 只打印文件与行号: Spec 三份文件只命中 git SHA、bash 源码包校验和与「点分标识符链」代码示例 (均非凭据); 其余仅 R1 / R2 审计报告里的讨论占位与一份原型脚本里的 PEM 头部字面 (无密钥体)。
3. L3 白名单 16 例 (既有键 `password`, 值运行时生成): 基线 vs 执笔的目标态原型。
4. 探针子集: `WPA_ONLY=SC-7,SC-11` 与 `SC-26,SC-28`, 基线与原型各一次。
5. 12 个坏实现抽样 (用执笔归档的 `patch_l3.py` 生成, 只跑对应行): `drop_name:registration_token` / `drop_kwkv:WEBHOOK` / `drop_flag:apikey` / `drop_scheme:basic` / `drop_vsym:kv:~` / `wl_varname_lc` / `wl_cmdsub` / `wl_dots_ascii` / `wl_angle_prefix` / `wl_brace_noend` / `wl_drop:marker_REDACTED` / `w5_path`, 加对照 `v3`。
6. L1: 26 条 W11 命令基线 vs 原型; Tasks 1.12 的四条惰性腿基线 vs 原型。
7. W5: 14 个敌意 `file_path` 运行 (7 种 × Read / Write) 与几种异常 `tool_name`。
8. Impact 的关闭关键字正则取出实跑 21 例。
9. 平台与工具事实复核: 本机 Claude Code 2.1.285 二进制含 `updatedToolOutput` 39 处与描述原文; curl 7.88.1 的 `-K -` (有配置 rc 7 / 空配置 rc 2) 与 `-H @文件` (rc 7); `nomad var put -h` 含 「consumed as-is」; jq 1.6 `length` 取绝对值 (-4821 得 4821); bash 5.2 与真 bash 3.2.57 对 `${x//b/"$r"}` 分别得 `aZc` 与 `a"Z"c`; procps-ng 4.0.2 下 `ps -aux / -au / -eu / -u` 打印 COMMAND 列完整命令行。
10. W1 成本: Read 信封下整进程 CPU 时间 (每侧交错 5 次取最小): 4 KB 基线 0.136 s / 原型 0.384 s, 60 KB 0.175 s / 0.460 s (主机负载 17-28, 绝对值仅供量级)。
11. 四仓 `ls-remote`: 主仓两端 `0748dbc`, aria `268da8f`, standards `2bc1c4c`, aria-orchestrator `237045a` (与派单一致)。

Rule #7 与过程说明: 本席未读取或打印任何凭据。核对 W11 时对本机跑过两次进程列举 (一次 `ps -ex | grep … | cut -c1-110`, 一次 `ps aux … | cut -c1-200` 看负载), 输出已截断, 可见部分只含 `SHELL` / `TERM_PROGRAM_VERSION` 一类无害变量与程序路径 —— 这恰是 W11 要拦的形态, 现行 v1.74.1 不拦。另有两个一次性临时文件写在 `/tmp/claude-1000/` 下 (curl 头文件与 bash 引号测试脚本), 已删除; 其余文件都在上述目录内。

## Findings

### Critical

无。

### Major

无。

### Minor

#### m1 · id `a6304dd1` · minor · issue · testing
- scope: `proposal.md SC-28`
- summary: SC-28 对「替换文本在场」按单个子串判定, 放过半截改写与新造的悬空锚点 (R1 `a6304dd1` 的残余两个子形态): 28l 的旧文本只取 `version-dependent behaviour`, 同段里的 `Claude Code exposes no field to replace tool_response` 保留也绿; 28b 只验头注释含 `secret-hygiene.md`, 保留不存在的 `§1.3` 也绿。
- 证据:
  1. `baseline_probe.py:1803`: `("28l", SCAN, "version-dependent behaviour", lambda s: "updatedToolOutput" in s, 100, …)`; `:1795`: `("28b", GUARD, "docs/operations/secret-rotation-runbook.md", lambda s: "secret-hygiene.md" in s, 100, …)`。
  2. 基线 `secret-scan.sh:16-17` 的 `Claude Code exposes no field to replace tool_response` 与 `:20` 的 `version-dependent behaviour` 在同一段; 基线 `secret-guard.sh:62` 的原句是 `…secret-rotation-runbook.md §1.3 principles`。`standards/conventions/secret-hygiene.md` 第 1 节只有 §1.1 / §1.2, `grep -n "1\.3"` 零行。
  3. 执笔原型 (`exp/writer-v3b/work/t3/aria/hooks/`) 两处都是这样落地: `secret-scan.sh:16-19` 同时写着「Claude Code exposes no field to replace tool_response」与「The 2.1.285 schema lists updatedToolOutput (unverified end to end, unused here)」; `secret-guard.sh:60` 写成 `standards/conventions/secret-hygiene.md §1.3 principles`。我在该原型上跑 `WPA_ONLY=SC-26,SC-28`: doc-sync 23/23 yes (基线 0/23), 即两处缺陷都被判绿。
- 失败场景: 实现者按 W14「删旧句、加 updatedToolOutput 句、改指 secret-hygiene.md」字面做 (与原型同), SC-28 全绿, 头注释却在同一段里同时断言「没有字段可替换 tool_response」与「schema 列出 updatedToolOutput」, 并用一个不存在的小节替换原悬空引用 —— 修悬空引用时新造悬空引用。三态: 基线红, 目标绿, 半截改写 (留前半句, 或留 `§1.3`) 仍绿。
- 建议修法: 28l 要求两个旧子串 (`exposes no field to replace` 与 `version-dependent behaviour`) 都消失; 28b 增「头注释不含 `§1.3`」(或要求指向实际存在的小节), W14 把「`§1.3` 一并改为 `§1`」写明; 两条各补一个半截改写的坏实现行 (或手工运行) 钉住。

#### m2 · id `cfb2fb14` · minor · issue · testing
- scope: `proposal.md Tasks`
- summary: Tasks 1.12 的执行条件写「`.aria/probes/plugin-cache-currency.py` 报 `PASS`」并把 `STALE` / `SKIP` / `FAIL` / `AHEAD` 并列为其它结果, 但脚本通过时首行是 `OK installed=… sot=…`, `PASS` / `skip` / `fail` 是 state-scanner 自定义检查运行器的状态词, 且 SKIP 也是 exit 0。
- 证据: `.aria/probes/plugin-cache-currency.py:127` `print(f"OK {detail}")` 并 `return 0`; 全文 `PASS` 只在 `:19` 的 docstring 分类里出现 (无输出); SKIP 打印 `##SKIP## …` 并 exit 0; `STALE` / `AHEAD` / `MALFORMED` 经 `_fail` exit 1。`custom_checks.py:373-378`: `rc == 0` 时首行以 `##SKIP##` 起头记 skip, 否则记 pass; 非零记 fail。
- 失败场景: 实施者直接跑脚本并以 `PASS` 判定, 永远对不上 (卡在 1.12 门外); 或只看 exit code, 把 `##SKIP##` (非 marketplace 安装 / 缺 `installed_plugins.json`, 恰是无法确认缓存版本的情形) 当通过, 继续做四条腿。惰性诱饵使后一种不泄露, 但会在缓存未更新时白跑一遍并可能误判 1.12 已通过 (关单前提)。
- 建议修法: 改写成「首行以 `OK ` 开头且 exit 0 (state-scanner 口径 pass) 才算执行条件成立; 首行 `##SKIP##` 或 `STALE` / `AHEAD` / `MALFORMED`、或 exit 非零, 一律记『未生效』并停下」。

#### m3 · id `4447c607` · minor · issue · testing
- scope: `proposal.md What.W14`
- summary: W14 写死「secret-scan 计数: 目标态 K = 50 (49 + 自检本身), `secret-hygiene.md` 同步为 50」, 与同一 Spec 要求向 `secret-scan.test.sh` 新增真实信封用例相矛盾; 50 只是执笔原型 (只加头注释与自检、未落任何 L3 用例) 的产物。
- 证据: `proposal.md:237` (W14 该条); `:52` (W1「新测试一律用真实信封」); `:360` (Tasks 1.2「按 SC 把探针用例落为两个套件的用例」); SC-29 29a「总数 >=49」; 27b / 27c 的判定函数 (`baseline_probe.py` 的 `_scan_header` / `_sot_scan_count`) 比较的是实跑总数, 不是 50; 原型 SOT diff 为 `| 49 regression cases |` 改 `| 50 regression cases |`; 同一节里 secret-guard 的三处计数写的是「同步为实跑数」。
- 失败场景: 实现者按 Tasks 1.2 落新用例后实跑总数是 49 加 N 再加 1; 若照 W14 字面把头注释与 SOT 写成 50, 自检断言与 27b / 27c 转红; 若为守住 50 而不落新用例, 又违反 W1 / Tasks 1.2 (新增检出面无套件内回归)。探针本身不会放过 (判据是实跑总数), 所以只造成一次返工与一处误导性散文。
- 建议修法: 把「目标态 K = 50」改为「K = 实跑总数 (含自检本身), SOT 的 secret-scan 计数同步为同一数」。

## 上一轮对账

R2 的 1 条 critical 与 15 条 major 经主控归并为 7 簇 (定稿键 `e8d39a8a` / `ac42f607` / `ce6fc59c` / `eb350937` / `60f3173a` / `6bd285b1` / `05982c10`); 逐簇对账如下, 证据均为我本轮亲自实跑或实读。

| 簇 | 定稿键 (席位原编号) | 对账 | 我核验的证据 |
|---|---|---|---|
| A W3 白名单撞真值 | `e8d39a8a` (tl C1) / `fc97f926` (cr M1, km M1) | closed | W3 `:80-99`: 裸 `$NAME`、`$(…)`、ASCII `...` 三类已删, 「保留判据」成文, 作用范围与已知限制同步。L3 原型对既有键 `password` 16 例: `$`+小写 / `$`+大写 / `$`+小写数字 / `$(…)` / ASCII `...` 结尾五类基线与原型都告警; `<…>` / `${…}` / Unicode `…` 结尾 / `FAKE_` / `PLACEHOLDER_` / `[REDACTED]` 基线告警、原型静默; 不闭合的 `<` 与 `${`、crypt 哈希形、值中间含 FAKE、小写 `fake_` 两侧都告警。探针子集 SC-7 + SC-11: 基线 baseline-failing 0/11、其余全 yes, 原型全 yes。6 个坏实现各只转红预期行: `wl_varname_lc` / `wl_cmdsub` / `wl_dots_ascii` 红 7h, `wl_angle_prefix` / `wl_brace_noend` 红 7j, `wl_drop:marker_REDACTED` 红 11x 与 11y; 对照 v3 无红行。Impact「新静默 / 不在内」与 W3 一致。 |
| K W11 进程表覆盖 | `ac42f607` (tl M1, ba M3, qa M3) | closed | launcher 集 = `secret-guard.sh:873` 的 13 个词 (我数过) + `command` (`:875`) + `exec` = 15; 关键字位置沿用 `:877`。26 条命令基线 vs 原型 (基线全 0): `ps aux`、`ps -aux \| grep curl`、`sudo -u svc ps -ef`、`timeout 5s ps aux`、`/bin/ps aux`、`while true; do ps aux; done`、`pgrep -f x \| xargs ps -fp`、`python3 -c` 读 `/proc/1/environ`、`cat /proc/1/task/1/environ`、`podman top`、`ssh host 'ps aux'`、`nomad alloc exec … env`、`ps -p $$ -o args=` 原型全 exit 2; `ps -eo pid,comm`、`ps -u dev -o pid,comm`、`pgrep -f x`、`ps -p 1`、`docker ps`、`echo ps aux`、`man ps`、`grep VmRSS /proc/1/status`、`ps aux \| wc -l`、`sudo nice ps aux` (已成文的嵌套 launcher 残余)、`if ps aux …; then` (已成文的条件位置残余) 原型 exit 0; 与 Spec 期望逐条一致。procps-ng 4.0.2 上 `-aux` / `-au` / `-eu` / `-u` 打印完整命令行, 与 W11 第 6 类一致。 |
| L Tasks 1.10 post-ship 腿 | `ce6fc59c` (tl M2, ba M4) / `5fd1f356` (km M2) | closed (带 minor m2) | 头部 Rule #7 声明 (`:14`) 与 Tasks 1.12 现在一致: 四腿都是惰性操作数、拆到发版之后、执行条件写明。四腿基线 vs 原型: `ps aux \| head -c 0` 0 / 2; `cat /nonexistent-wpa-probe/forgejo/app.ini` 与 Read 同路径各 0 / 2; L3 腿用运行时 `secrets.token_urlsafe(32)` 生成的合成值写成 `JWT_SECRET = <值>`, Bash 与 Read 两种信封基线均无告警, 原型均为 `(tags: kv-secret-assign=1; source: Bash|Read)`; 旧 hook 下这些命令只产生零字节输出或 ENOENT, 无泄露面。执行条件的 token 与脚本输出不符见 m2。W13 第 3 点的 `nomad var put` 已限不可达地址或 `-h` 原文。 |
| M 枚举逐成员出行 | `eb350937` (qa M2) / `e7e041c6` (ba M1) / `51e90cab` (ba M2) / `5ce95ecf` (qa M1) | closed | 枚举集合在探针里只列一处、循环即是行; 数字对得上: W8 读取器 13+16=29、W9 读取器 29+2=31、`/proc` 读取器 13+11=24、launcher 13+2=15。5 个缺项类坏实现 (`drop_name:registration_token`、`drop_kwkv:WEBHOOK`、`drop_flag:apikey`、`drop_scheme:basic`、`drop_vsym:kv:~`) 各只红预期行 (4p / 5n / 6i / 6j / 6k); 对照无红行。 |
| N W5 外来文本进 additionalContext | `60f3173a` (qa M4) | closed | W5 现为零外来文本 (只含 hook 自己的 tag 表、计数与 `tool_name`)。14 个敌意 `file_path` 运行 (良性 / `)` 加祈使句 / 换行加伪造 hook 行 / 引号 / U+202E / 5000 字符 / 控制字符, Read 与 Write 各一): 删去严格形状的插入段后与基线 additionalContext 逐字节相等, 且不含任何敌意片段 (14/14); `w5_path` 坏实现红 13a / 13c / 13g。 |
| O 时档对负载不稳 | `6bd285b1` (cr M2) | closed (设计层) | W14 改为同次运行交错的整进程 CPU 时间之比 + 活性断言 + 20 s 宽松兜底 + 基线 CPU 不合格即重测; 参考实现 `timing.py` 用 `RUSAGE_CHILDREN` 的 user+sys 度量, 与文字一致。SC-30 不由探针执行, 我只复量了 W1 的 Read 面 (见实跑 10), 与 W1 句同量级; (f) / (g) / (h) / (i) 全档未重跑。 |
| P 关闭关键字旁路 | `05982c10` (km M3) | closed | Impact「提交页脚 / PR 描述的关键字」条、Tasks 贯穿行与 1.11 / 1.13 已落; 取出正则实跑 21 例: `Closes #154`、`closes 10CG/aria-plugin#154`、`Fixes: #203`、带 `/issues/` 的 URL 形、`(closes #154)`、`Resolves 10CG/Aria#221.` 等正例全命中; `Refs …`、`#1540`、`#15`、`closing #154`、`unfixes #154`、反引号包住的引用、关键字与号分行的写法不命中; 保守误命中只有 `prefix-closes #154` 这类。`${PIPESTATUS[1]}` 是管道第 2 个命令 (grep) 的退出码, 与「无输出且 rc=1 为通过」一致。关键字集合 close / fix / resolve 及 s / d 变体与 `COMMIT_FOOTER_GUIDE.md:193` 的口径一致 (Forgejo 服务端默认集合我未实测, 不作断言)。 |

R2 的 minor (全部 34 条, 含本席 8 条 `eff49510` / `5e342bfd` / `51dded0b` / `4900bccc` / `5d032f7a` / `0033f2f4` / `5d12116d` / `84a82267`) 我逐条对了 v3 文本或探针行: 均已处置。唯一仍有残余的是 R1 `a6304dd1` 同类的 SC-28 (本轮 m1)。

## 对执笔人自报薄弱点与请裁项的表态

**薄弱点 (返修报告 §6)**
1. 原型不是实现、坏实现自构 (同源盲区): 可接受, 条件是 Tasks 1.8 的非作者对抗 review 照做。我抽样 12 个坏实现全部只红预期行; 同源盲区的新证据在文档类: 原型自己的两处头注释补丁就带着 m1 的矛盾与悬空锚点, 而 SC-28 全绿。
2. 体量 +40%: 可接受; 本轮起仍不建议为削字再改 (削字本身造接缝)。
3. 时档阈值由单一共享主机实测: 可接受; 「越界上呈、不放宽」与 Rule #10 及 `2026-08-24-sc8-absolute-latency-gate.md` (阈值硬编码、FAIL 文案要求记全数据请 owner 复议) 同向。请 owner 知悉 (g) 满额档余量约 16%、(f) 靠 100 ms 地板而过。
4. W1 + W2 使每次 Read 成本约 3 倍: 可接受 (W1 与 Impact 已写); 我的实测 (4 KB 0.136 到 0.384 s, 60 KB 0.175 到 0.460 s) 同量级、在 5 s 超时内。请 owner 知悉建议开单 7.6 (PEM 预扫超线性) 的影响面随 Read 一起放大, 且超时的后果是静默丢告警。
5. 已接受误报的钉法 (22bj / 10l): 可接受, 保留 10l。类别语义已在 SC 文字里写明 (基线放行、目标拦; 转红即有人收口, 须同步改 Spec); 删它只会让这五个形态退回散文。可选: 在类别图例里补一句「`baseline-failing` 也用于钉被接受的新行为」。
6. 真 bash 3.2 沿用 v2 构建: 可接受; Tasks 1.1 已写「取不到则上报 owner, 不得以静态检查代之」。我本轮未用 3.2 复跑 (主控已复跑逐字节一致)。
7. 「表里写了、原型没做」只对 W4 表逐项核了: 可接受; 本轮我发现的缺口正落在「其它章节只做抽查」的文档类 (m1 / m3)。
8. cr 的两条未采纳备注: (a) 「零有效条目则不调用 grep」可接受不采纳: GNU 与 BSD 手册都写空模式文件不匹配任何行 (BusyBox 语义我未实测), 作为实现提示零成本, 但不必升为要求。(b) W6「清理对象用 `mktemp -d` 记下的变量, 不写 `rm -rf "$HOME"`」我**不接受不采纳**: 清理是整套件里唯一的 `rm -rf`, 实现者若先恢复 HOME 再触发 trap 就会删真实家目录; 而 SC-14 已在私有「外层 HOME」下跑套件, 可证伪判据很便宜 —— 预置一个 canary 文件, 套件结束后 canary 仍在且套件自建的临时 HOME 已不存在 (坏实现「恢复 HOME 后 `rm -rf "$HOME"`」会让 canary 消失)。建议主控把这一句写进 W6 与 SC-14, 不另计 finding。

**请裁项 (返修报告 §7)**
1. 待复议 19 (W5): 默认 A (只含 tag 与工具名) 可接受, 不建议 B' (新增净化代码); 另见「风险 / 疑问」第 3 条 (W5 非三个 issue 的诉求)。
2. 10l 保留或删除: 保留 (同薄弱点 5)。
3. 时档口径: 可接受 (同薄弱点 3)。
4. W1 的每 Read 成本: 可接受 (同薄弱点 4)。
5. cr 两条备注: (a) 不强求, (b) 建议采纳 (同薄弱点 8)。
6. km 两条风险: (a) A.1 认领: PROGRESS.md 记心跳最近 2026-10-06T10:02:46Z, 该风险已由例行维护消除 (我无权也未 fetch 协调 ref, 只见 `ls-remote` 两端 `refs/aria/coordination` 的 SHA 不同, 见风险第 8 条)。(b) 建议开单 7.1 的「约 1400 个空段」配方: 可接受不改 Spec, 因为研究笔记 `secret-guard.md:20` 与 `:371` 在同一分支里含同一信息, 单改 Spec 无效; 但这是公开 GitHub 镜像上的未修复旁路配方, 须在**首次向 github 远端推送该分支前**由 owner 知悉并裁定整支分支 (含笔记) 的披露范围; 推送在「feature 分支推送」一次性授权类内, 授权时 owner 并未就这条内容表态。
7. 归档落盘 `writer-v3-proto/`: 已入仓 (c0a6654), 可接受; 脚本内绝对路径须改写已在 README 与 Spec 头部说明; 全部 119 个新增文件我独立扫过, 无凭据形状。
8. Rule #10 自作主张 (a) 至 (f): 须由主控写入 handoff 请复议。我的表态: (a) `/proc` 纳入内联解释器可接受 (W8 / W9 已是同一对解释器, 我的 `python3 -c … /proc/1/environ` 样例被拦, 占位词文本提及由 22bf 放行); (b) W5 零外来文本可接受 (14/14 敌意路径); (c) 10l / 12m / 9l-9m 重做可接受; (d) 未写 report.md 可接受; (e) mutbatch 重名处理重写可接受 (我复用该脚本无问题); (f) 变异复跑限于新写行与同族可接受。
9. 观察 (无需动作): 一致; 我同样被活体 L1 以文本提及类误拦过 (本轮一次是读 `.claude/settings.json`, 属真阳性), 均改用无害方式, 未使用 `# guard:ack`。

## 风险 / 疑问

1. **v2.0 Layer 2 无人值守的影响未申报**: aria-runner 容器内嵌 aria-plugin, 升级镜像后会继承新拦截 (进程表、`app.ini`、变量间接)。无人值守时新误拦只能由 AI 自己加 `# guard:ack`; 待复议 5 与 Impact 只讨论交互使用习惯。DEC-20260703-001 的约束表早已把「双上下文 (交互 + 自主)」列为约束。`aria-orchestrator` 内没有任何 secret-guard / ack 的引用, 仓内 Skill 与脚本也没有推荐 `ps aux` 的写法, 所以是未评估而非已知冲突。建议在 Impact 补一句。
2. **Impact 引用精度** (不计 finding): 「仓内约定 (`COMMIT_FOOTER_GUIDE.md`、`git-commit.md` §6.1) 要求修复类提交写 `Closes #N`」「覆盖仓内 §6.1 的默认写法」—— `git-commit.md` §6.1 只并列 `Closes` / `Fixes` / `Refs` 三行、无「要求」, 要求在 `COMMIT_FOOTER_GUIDE.md:199`; 同表 `:201`「部分实现用 `Refs`」对 Spec 自称「部分覆盖」的 10CG/aria-plugin#203 与 10CG/Aria#221 本就成立, 真正偏离默认写法的只有 10CG/aria-plugin#154 在 1.12 之前的 `Refs`。另: Impact 的同步面清单 (standards 条目) 未列 W13 / SC-28 28m 要求的 §5.2 追加句, aria 条目未列 `aria/VERSION:164` 的「output REDACT」改写; 两者由 Tasks 1.9 与 SC-28 承载, 实施无遗漏, 只是清单不逐项对账。
3. **W5 不是三个 issue 的诉求**: 10CG/aria-plugin#154 评论 19339 明说告警措辞「现行已满足」, 三个 issue 与 Why 表都没有对应的洞; W5 来自研究笔记与主控范围裁定 (R2 主控自我订正已承认), 带来 rule6_note 块 B、SC-13 共 14 个运行与待复议 8 / 19。当前版本已收紧到零外来文本, 不改变实现者动作, 故不立 finding; 建议在待复议 19 增列「删除 W5」选项, 由 owner 知悉其为 AI 增补。
4. **(f) / (f0) 上界的「沿用」措辞**: W14 写「沿用测试内 SC-8 的 `max(100 ms, …)`」, 但公式是 `1.5 × max(基线, 100 ms)`, 基线 49 ms 时为 150 ms, 比 SC-8 的 `max(100 ms, 基线 × 1.5)` = 100 ms 宽 50%。两者度量对象也不同 (整进程 CPU 对进程内计时), 本身可辩护, 且已列入待复议 20, 只是措辞不精确。
5. **Tasks 1.1 的「逐字节一致」运行对象**: 未点明在 `268da8f` / `2bc1c4c` 的冻结副本上复跑。若 aria master 在 B.1 前移动 (10CG/Aria#199 同样要改 aria 发版文件), SC-26 / SC-28 / SC-33 的基线「实得」串可能变化而无合法下一步 (Spec 不允许改证据)。建议写明用 `git archive` 取冻结副本。
6. **W5 的 `source` 未白名单**: 原型对 `tool_name` 原样输出 (含换行的 `tool_name` 会原样进 additionalContext), 13g 只测 `file_path`。真实 harness 下 `tool_name` 受两层 matcher 限定、MCP 名字符集受限, 实际不可达; 建议 B.2 把 `source` 限定为 Bash / Read / Edit / Write / MultiEdit, 其余写 `unknown`, 补一行 13h。
7. **平台未实测面**: macOS / BSD (`grep -F -f`、`ps` 的 BSD 语义、`pgrep -fl`)、BusyBox、Windows Git-Bash (10CG/aria-plugin#203 的报告环境 MINGW64) 均无运行腿; W8 / W9 已知限制已写 Windows, 但 W9 的 `grep -F -f` 与 `<()` 进程替换在 Git-Bash 与 BSD 上的行为只在写手报告里提到, Spec 未列。SC-31 31a 的行预算余量只有 1 行 (R1 / R2 已提)。
8. **协调 ref 两端不同**: `ls-remote` 显示 `refs/aria/coordination` 在 origin 为 `f47b60d…`、github 为 `ad0287f…`。属 claim / 心跳例行维护面 (决策单第 4 项), 不在本 Spec; 只请主控确认这是例行心跳只推 origin 的预期状态。
9. **README 表格行**: `aria/README.md:33` 与 `README.zh.md:33` 的表格行仍写「cannot redact (PostToolUse architectural limit)」, 而 28m 只在用法小节追加事实句。这是 Out of scope 已声明的「只增不改」设计, 同一文件内两处说法会并存到第 1 条复议结论落地为止。
10. **未能验证**: SC-30 (带 git 历史与 `af87cae` 的真 checkout 上的计时闸与 SC-9a) 不由探针执行, 我没跑; (f) / (g) / (h) / (i) 时档只复量了 W1 的 Read 面; Forgejo 服务端的关闭关键字默认集合未实测。

## Verdict

- verdict: **PASS**
- counts: `0C/0M/3m`
- Vote: **PASS**

## 是否足以进入 A.2

足以: 从文档与规范一致性视角, R2 的 7 簇 (1 条 critical 与 6 簇 major) 我逐簇实跑 / 实读均已 closed, 本轮无 critical 与 major; 3 条 minor (SC-28 两处判据过弱、Tasks 1.12 的执行条件 token、W14 的 K = 50) 各只需一两句文字或一两个子串判据, 可在 A.2 之前顺手并入, 也可随 task-planner 的 detailed-tasks 一并处置。按本仓口径, 判收敛还看相邻两轮的 Critical + Major 键集与其余四席的投票, 本席不就此表态。
