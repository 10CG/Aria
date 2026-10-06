---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-06T15:21:34.013Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 — qa-engineer 席报告 (WP-A secret-net-l3-and-bypass-paths, proposal v3 @ c0a6654)

视角: 每条 SC 的可证伪性 (基线 / 目标 / 坏实现三态)。

**摘要**: R2 的七簇里五簇关闭 (A / K / L / N / O), 两簇部分关闭 (M `eb350937`、P `05982c10`); 另有两条新发现 (SC-20 缺「有效条目为零」、SC-32 差分只跑一个 locale)。**无 critical**: 我没有找到照 Spec 实现会使现有拦截或检出变成放行的路径 (已申报的收窄除外)。四条 major 的共性是「验收 / 检查没拦住一个自然的坏实现」, 修法是补行或改判据, 不涉设计取舍。

**方法**: (1) 在自己的副本上带真 bash 3.2.57 完整复跑基线探针; (2) 用执笔归档的补丁脚本对**我自己的**基线副本重建目标原型 (`aria/` 树与执笔 `work/t3` 逐文件 sha256 相同), 复跑 L1 / L3 行; (3) 对 R2 七簇各自独立构造坏实现复核关闭; (4) 另造 14 个「自然的坏实现」找存活者 (只改一处, `bash -n` 通过, 只跑对应 SC)。全程 HOME / TMPDIR 指向本席目录, 值全部运行时生成、只看退出码 / 是否告警 / tag 名, 未打印任何值; 真仓 `git status` 干净, 主仓 `c0a6654` / aria `268da8f` / standards `2bc1c4c` 未变。

## 已实读文件

- **被审对象**: `proposal.md` 1-425 全文; `baseline_probe.py` 1-2095 全文; `baseline-evidence.md` 头部 1-60, 内嵌输出与我的实跑 stdout 逐字节相同 (见下)。三份文件 sha256 前 16 位 `9e7fbe0bbc86caf9` / `51936cff0a363c7f` / `cb9d8f8482faef16`, 与执笔报告一致。
- **v2 到 v3**: `git diff b3e3123 c0a6654` 词级 diff 读前 110 行 (W2 / W3 / W4 / W5 / W8-W14 的全部实质改动), 其余以 v3 全文通读代替。
- **issue 与决策**: `aria-plugin-154.md` / `aria-plugin-203.md` / `Aria-221.md` 正文加全部评论全文; `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; `CLAUDE.md` 规则 #6 / #7 / #10 与多远程两条硬约束。
- **源码与规范**: `aria/hooks/secret-scan.sh` 1-377 全文; `secret-guard.sh` 的 `:405-410` `:425-429` `:491-494` `:564-566` `:617-626` `:631-700` `:815` `:873-878` `:893-895` `:930-934` `:1043-1046` `:1088-1112`; `hooks.json` (matcher 与 `timeout: 5`); `secret-scan.test.sh` `:20-40` `:88-125`; `secret-guard.test.sh` `:11` `:1618-1624` `:2018-2030` 与 HOME 用法; `standards/conventions/skill-benchmark-exemption.md` 全文; `secret-hygiene.md` 全部标题 + §3.1-3.2 + 版本历史 + `:23` `:287` `:288` `:319`; `aria/README.md` Hooks 表; `.aria/probes/plugin-cache-currency.py` 与 `.aria/state-checks.yaml` 对应条; `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 发版相关段; `pre-merge-completeness-gate-change-scope/detailed-tasks.yaml:341-342` (10CG/Aria#199 的 `guard_config_hooks`); `aria-orchestrator/docker/aria-runner/` 的 Dockerfile 与 `modes/initial.sh:309-311`。
- **上一轮与执笔材料**: R2 聚合报告全文 (含主控记录)、R2 qa 席报告 M1-m5; `v3-writer-report.md` 全文; `writer-v3-proto/` 的 README、`timing.py`、`timing_summary.txt`、`mut_summary_v3.txt` 头部与格式、`plans/`; 原型对基线的 `diff` (两个 hook 全部)。
- **未读**: 四份研究笔记 (背景材料, 与源码冲突时以源码为准, 我只用源码); R2 其余四席报告原文 (只取聚合表); `v3-dispositions.json`。

### 实跑核验 (三态摘要)

- **基线 (独立复现)**: 带 `WPA_BASH32`, rc=0, stderr 空, stdout 74072 字节, sha256 前 16 位 `a6e187b50a4f3514`, 与执笔 / 主控的值逐字节相同; `baseline-failing` 0/190、`doc-sync` 0/25、`reverse-guard` 59/59、`allow-guard` 65/65、`known-limit` 34/34、`zero-regression` 9/9, 基线形态 `holds`。
- **目标原型 (本席重建)**: L3 行 SC-1…SC-13 共 146 行全 `yes` (baseline-failing 73 / reverse 22 / allow 38 / known-limit 13); L1 行 SC-16…SC-25 共 180 行全 `yes` (114 / 25 / 20 / 21); SC-15 7/7; SC-26 与 SC-28 25/25 (SC-32 的 32a / 32b 绿, 32c 未带 bash 3.2); 目标态 `secret-scan.test.sh` 50/50 (默认 bash 5.2 与真 3.2.57 各一遍)。没有一行「该红的在基线绿」或「该绿的在目标红」。
- **逐 SC (行数 / 基线 / 目标原型 / 我的坏实现证据)**:

| SC | 行 | 基线 (本席) | 目标 (本席) | 坏实现 / 备注 |
|---|---|---|---|---|
| 1 | 2 | 2/2 红 | 2/2 绿 | 提取链坏实现存活, 见 M1 |
| 2-3 | 4+2 | 全绿 | 全绿 | 同上 (`tool_result` 分支无行) |
| 4 / 5 / 6 | 19 / 14 / 11 | 全红 | 全绿 | 缺项类由执笔 420 个坏实现覆盖, 我未重跑 L3 缺项 |
| 7 | 10 | 10/10 绿 | 10/10 绿 | 白名单回退三类坏实现均使 7h 转红 |
| 8 | 1 | 红 | 绿 | — |
| 9 | 25 | 25/25 绿 | 25/25 绿 | bash 3.2 + en_US 下 9p 转红, 见 M4 |
| 10 | 12 | 1 红 + 11 绿 | 12/12 | bash 3.2 + en_US 下 10a / 10k 转红, 见 M4 |
| 11 | 26 | 11 红 + 15 绿 | 26/26 | 白名单回退三类坏实现均使 11z 转红 |
| 12 | 13 | 10 红 + 3 绿 | 13/13 | 5 个 W4 坏实现 13/13 绿, 见 M1 |
| 13 | 7 | 4 红 + 3 绿 | 7/7 | 「插入段带净化路径片段」坏实现使 13a / 13b / 13c / 13d / 13g 转红 |
| 14 | 2 | 2/2 红 | 未复跑 | 套件类, 执笔 T 跑 0 行 / 0 条 |
| 15 | 7 | 1 红 + 6 绿 | 7/7 | — |
| 16-18 | 17+4+9 | 红 / 绿符合 | 全绿 | `drop_reader:column` 使 16q 与 19u 转红 |
| 19 | 23 | 16 红 + 7 绿 | 23/23 | `ext_occ65` 使 19y 转红; 不剥空白与零有效条目坏实现 0 行红, 见 M1 / M3 |
| 20 | 14 | 2 红 + 12 绿 | 14/14 | 零有效条目坏实现 0 行红, 见 M3 |
| 21 | 22 | 11 红 + 11 绿 | 22/22 | `vx_assign17` 使 21y 转红 |
| 22 | 67 | 53 红 + 14 绿 | 67/67 | `drop_launch:unbuffer` 使 22aw 转红; `drop_kwpos:elif` 使 22az 转红 |
| 23-25 | 8+9+7 | 符合 | 全绿 | — |
| 26 / 28 | 11 / 14 | 全红 (9 红 + 2 绿) | 11/11, 14/14 | 28c / 28d 判据窄, 见 m1 |
| 27 / 29 / 31 / 33 | 4 / 9 / 5 / 1 | 符合 (33 恒绿, 设计如此) | 未复跑 (只验 scan 套件 50/50) | — |
| 30 | 1 | 探针外 (`n/a`) | 不适用 | 时档: 我跑了基线对基线负控, 见对账簇 O |
| 32 | 3 | 3/3 绿 | 32a / 32b 绿, 32c 未复跑 | locale 轴失明, 见 M4 |

## Findings

### Critical

无。

### Major

**M1** — id `eb350937` / major / issue / testing
scope: `baseline_probe.py`
summary: 枚举 / 边界「逐成员出行」在 v3 补到了 W2-W12 的新增集合, 但**既有且被改写触及的成员**与 W4 / W9 的两处阈值 / 回退腿 / 格式规则仍没有行; 我造的 8 个自然坏实现在对应全部行上 0 行红。
证据 (目标原型 + 单点改动; 退出码 / tag 名为实跑):
1. **既有 `json-secret-field` 的 10 个键只钉了 8 个**。`secret-scan.sh:227` 的键表含 `webhook_secret` 与 `encryption_key`; 探针 `OLD_KEYS` (`baseline_probe.py:531`) 与 4p 只含另外 8 个, 既有套件只有 `password` 与 `api_key` 两键 (`secret-scan.test.sh:120-121`)。基线与目标对 `{"webhook_secret":"<24 alnum>"}`、`{"encryption_key":…}` 均 `alert json-secret-field=1`; 把这两键从 `json-secret-field` 正则里删掉的坏实现 (新表里也没有这两个名干) 静默, 而 SC-1…SC-13 的 146 行全 `yes` (与目标原型的输出只差 hook 自身 sha256 指纹行), 目标态套件 50/50。W2 自己写了「既有 tag 收窄时不丢检出」的动机 (`proposal.md:61` 一带), 但这两键恰在新表之外。
2. **既有提取链 5 个分支只钉了 3 个**。`secret-scan.sh:135-142` 的 `.tool_response.output // .content // .stdout // .tool_result.content // .tool_result.output`; SC-2 的 4 个信封只走前三个。删去两条 `tool_result` 分支的坏实现对 `{"tool_result":{"content":…}}` 与 `{"tool_result":{"output":…}}` 静默 (基线 / 目标均 `alert aws-access-key-id=1`), SC-1 / 2 / 3 共 8 行全 `yes`。W1 正是原位改这条链。
3. **W4 指纹阈值 16 没有边界对**。`proposal.md:104`: 值长 ≥16 记 sha256 前 8 位, <16 记 `L<n>`。SC-12 里最短的取哈希用例是 20 字符 (12i / 12j / 12k), 最长的 `L` 用例是 12 字符 (12b / 12e), 13-20 之间任何门槛都过。三个坏实现 `<= 16` / `< 20` / `< 13` 在 16 字符值上分别得 `L16` / `L16` / 哈希 (目标得哈希), 在 13-15 字符上第三个得哈希 (目标得 `L13`-`L15`), 各自 SC-12 13/13 全 `yes`。这个门槛承载着 W4 的隐私论证 (8 位前缀对短口令构成确认预言机)。
4. **W4 哈希工具回退链没有单腿行**。`proposal.md:104`: `sha256sum` 与 `shasum -a 256` 都取不到才记 `-`; 12c 只钉「两者都缺」。去掉 `shasum` 回退的坏实现在 PATH 里只剩 `shasum` 时得 `fp=-` (目标得哈希), 去掉 `sha256sum` 腿的坏实现在只剩 `sha256sum` 时得 `fp=-`; 两者 SC-12 均 13/13 全 `yes`。这条链就是为 macOS (无 `sha256sum`) 与 Git-Bash (可能无 `shasum`) 而设。
5. **W9 格式规则「剥首尾空白」没有行** (`proposal.md:160`): 19m 只钉 CR。不剥空白的坏实现对 `  /srv/billing/conf/prod.toml  ` 这类缩进条目放行 (目标 exit 2, 坏实现 exit 0), SC-19 / SC-20 共 37 行全 `yes`。

失败场景: 实现者在原位改写提取链 / `json-secret-field` 正则 / 指纹函数时丢掉以上任一成员或把门槛写偏一位, B.2 的探针与套件全绿, 发版后既有检出 (`webhook_secret` / `encryption_key` 键、`tool_result` 信封) 静默变放行, 或日志指纹在 macOS 上恒为 `-`。1-2 是「既有检出变放行」, 按 R2 同类先例 (`5ce95ecf` → `eb350937`, 席位自评 major) 定 major; 若主控从严按「验收放过一个错误实现」字面可升 critical。
建议修法: (a) 4p 或新增一行把既有 10 个键逐个钉 `json-secret-field=1`; (b) SC-2 补 `tool_result.content` / `tool_result.output` 两个信封; (c) SC-12 补 15 / 16 字符的边界对 (15 记 `L15`, 16 记哈希); (d) SC-12 补「只隐去 `sha256sum`」与「只隐去 `shasum`」两腿仍得哈希 (探针已有 `_shadow_bin`); (e) SC-19 补一个带缩进 / 尾随空白条目的文件行; (f) 把这 8 个坏实现名加进 Tasks 1.8 的缺项类 / 差一类清单。

**M2** — id `05982c10` / major / issue / documentation
scope: `proposal.md Impact`
summary: R2 簇 P 的修复 (关闭关键字的机械检查, `proposal.md:352`) 本身在 `git log` 失败或范围为空时**真空通过**: 判据取 `PIPESTATUS[1]` (grep 的退出码), 起点写错 / 起点为空 / `-C` 路径错都得「无输出且 `rc=1` = 通过」; 与它自称照抄的 10CG/Aria#199 判据 (`PIPESTATUS[0]`) 相反。
证据 (临时仓里逐字运行 Impact 的命令, 正则取自 `proposal.md:352`, 仓内有两个提交: 正文 `Refs 10CG/aria-plugin#154` 与正文 `Closes #221`):
```
A 起点正确 (merge-base):     3:Closes #221          rc=0     -> 命中, 判违规 (正确)
B 起点写错 origin/mastr:     stderr "fatal: ambiguous argument ..."   rc=1  无任何 stdout -> 按 Spec 判「通过」
C 起点为空 (变量空): ..HEAD   (无任何输出, 无 stderr)           rc=1  -> 按 Spec 判「通过」, 实际一个提交都没检查
D -C 指向非仓路径:           stderr "fatal: cannot change to ..."       rc=1  -> 按 Spec 判「通过」
E 同输入取 PIPESTATUS[0]:    rc0=128 rc1=1          -> git 失败可见
```
10CG/Aria#199 的 `guard_config_hooks` 取第一条命令的退出码并写明「`<主仓根>` 不是仓 — v2.4 命令 0 行 (放行), v2.5 命令 rc=128 (停)」 (`detailed-tasks.yaml:342`, post_planning R5 R5-M4): 同一类真空通过, 他们已为此改过一次; Impact 一边「写法照 10CG/Aria#199 的 rc 判据」一边反着取下标。
失败场景: `<起点>` 由 `git merge-base HEAD master` 取得而该 ref 不存在 / 未 fetch → 变量为空 → `..HEAD` 空范围; 或手抄起点写错一位 → 判据说「通过」, 一个带 `Closes #221` 的提交被推送 / 合并, 违反决策单第 2 项 (10CG/aria-plugin#203 与 10CG/Aria#221 保持 open), 或在 Tasks 1.12 之前自动关 10CG/aria-plugin#154。合并本身仍有 owner 逐次门, 所以后果可挽回, 但这条检查是簇 P 的唯一机械兜底。
建议修法: 同时回显 `rc0=${PIPESTATUS[0]}` 与 `rc1=${PIPESTATUS[1]}`, 判据改为「rc0=0 且 rc1=1 且无输出」才算通过, 其余一律「没跑成, 停下上报」; 前置一条 `git -C <仓根> rev-list --count <起点>..HEAD` 须非空且 ≥1; 并像 10CG/Aria#199 的 N10 那样记下三态实跑 (干净 / 违规 / 跑坏)。

**M3** — id `28af0372` / major / issue / testing
scope: `proposal.md SC-20`
summary: SC-20 的「扩展失败只丢扩展」矩阵缺**有效条目为零**的扩展文件 (只含注释 / 只含空行 / 条目全被跳过): 一个把空模式喂给 `grep -F -f` 的自然坏实现使每个 Read 与 Edit 都被拦 (exit 2), 与 `proposal.md:165`「从不因扩展问题 exit 2 (10CG/Aria#154 会话死锁教训)」相反, 而 SC-19 / SC-20 的 37 行全绿。
证据: 探针的扩展文件种类 (`baseline_probe.py:1196`) 共 14 种 (ok / meta / junk / crlf / missing / dir / dangling / nul / big / many / unreadable / bound_ok / size32769 / bound_bad), 每种要么有至少一个有效条目要么是上列坏文件, **没有「零有效条目」**。坏实现 = 目标原型 `_sg_ext_entries` 去掉 `[[ -n "$out" ]] || return 0` (无有效条目时输出一个空行, 即空模式)。退出码 (基线 / 目标 / 坏实现), `CLAUDE_PROJECT_DIR` 指向只含两行注释、只含空白行、只含 `abc` / `xy` / `####` 的三种文件:
```
Read /x/README.md      0 / 0 / 2        Edit /x/notes.txt     0 / 0 / 2
Bash cat README.md     0 / 0 / 0 (原型的 Bash 面用 grep -o, 空匹配不输出; 换成 -q 预检的写法 Bash 面同样会全拦)
SC-19 + SC-20: 37 行, 0 行红 (与目标相同)
```
这是用户照 README 新建文件、先写注释头、还没加条目的**第一个自然状态**。BSD grep 对空模式文件的语义执笔自报未实测 (cr 的非编号风险 (a), 见表态 6.8), 在 BSD 上可能连「不写空行」的实现也会全拦。
失败场景: 采用方按 Spec 建 `.aria/secret-guard.paths` 先放注释 → 该项目里 AI 的所有 Read / Edit 被拦, 逃生口只剩 `SECRET_GUARD_ACK_PATH` 逐次 nonce; 发版时全部探针与套件全绿。
建议修法: SC-20 增 `comment-only` / `blank-only` / `all-skipped` 三个坏文件种类 (`reverse-guard`, 金丝雀: Read `/x/README.md`=0、Edit `/x/notes.txt`=0、`ls -la`=0、`cat .env`=2、Read `/x/.env`=2); W9 的失败处理把「有效条目为零 = 扩展不生效」写明; 采纳 cr 的实现注意: 不得把空模式列表交给 `grep -F -f`。

**M4** — id `44b5bb44` / major / issue / testing
scope: `proposal.md SC-32`
summary: SC-32 32c 的 bash 3.2 差分只在 `LC_ALL=C.UTF-8` 一个 locale 里跑 (`baseline_probe.py:113-115` 写死), 而 W2 规定分类只用 builtin 与 `[[ ]]` 却没规定字符类与 locale 无关: 同一个真 bash 3.2.57 在 `en_US.UTF-8` 下, 原型熵下限的 glob 类 `[[ $v == *[a-z]* ]]` 把大写也算小写, 目标原型的 L3 行 9p / 10a / 10k 转红, 差分看不见。(键与 R1 簇 E 的 `44b5bb44` 同四元组: R1 簇 E 的「无 3.2 运行腿」已由 32c 关闭, 本条是同一差分的 locale 轴残余。)
证据 (最小复现, 无任何凭据):
```
LC_ALL        bash     [[ QWERTY == *[a-z]* ]]   [[ qwerty == *[A-Z]* ]]   [[ QWERTY =~ [a-z] ]]
C.UTF-8       3.2.57   no                        no                        no
C.UTF-8       5.2.15   no                        no                        no
en_US.UTF-8   3.2.57   yes                       yes                       no
en_US.UTF-8   5.2.15   no                        no                        no
```
探针副本 (仅把 locale 与解释器参数化, Spec 文件未动) 对目标原型 SC-4…SC-11 共 117 行: bash 5.2 + en_US.UTF-8 为 117/117; **bash 3.2 + en_US.UTF-8 为 114/117, 转红的是 9p (`SECRET_PROMPT_NAME = release-notes-summary-v` 本应静默, 得 `kv-secret-assign=1`)、10a 与 10k (40 个纯小写 / 纯大写的 `token` 值本应静默, 得 `json-credential-field=1`)**。L1 行 SC-16…SC-25 在同一组合下 180/180 不受影响, 基线 hook 在该组合下形态 `holds`。`[[ =~ ]]` 不受影响 (上表第三列)。
影响面: 仅 L3 误报噪声 (熵下限失效), 无检出回退。已验证的是这个 3.2.57 二进制 (探针与差分用的同一个) + glibc 的 `en_US.UTF-8`; bash 4.x (≤4.4, `globasciiranges` 默认关) 预期同型, 未测; macOS 自带 3.2.57 的 libc 排序规则是否复现我没验证。
失败场景: 实现者照 Spec 只用 builtin、用 glob 写字符类 → 探针 (C.UTF-8) 与 32c 全绿 → 发版后在默认 locale 的 bash < 5 环境里熵下限形同虚设, 单一字符类的名字形值普遍告警。
建议修法: 32c 增一条 locale 腿 (`locale -a` 有 `en_US.UTF-8` 时跑, 否则 `n/a` 并计入 `WPA_REQUIRE_ALL`), 或把 L3 行整体在两个 locale 各跑一遍; W2 补一句「字符类判定须与 locale 无关 (用 `[[ =~ ]]`, 或函数内 `LC_ALL=C`)」。

### Minor

**m1** — id `b298cc56` / minor / risk / testing
scope: `proposal.md SC-28`
summary: SC-28 / W14 声称 28c / 28d「头注释不再出现任何 pattern / 类别总数字面」, 探针判据 `~?\d+ (known bypass classes|secret-shape patterns)` (`baseline_probe.py:1792`) 只认两个旧措辞。证据: 目标原型的 `secret-scan.sh` 头注释加一句 `(detect + warn only; 37 patterns, ~12 key-shape forms, 6 new tags)` 后, SC-28 的 14 行全 `yes` (28c / 28d 也是 `yes`)。失败场景: 实现者写入新的总数字面, 正是 W14 要治的陈旧计数病, 检查不报。建议: 判据改成头注释前 100 行里不得有「数字 + patterns / tags / classes / forms / bypass」。

**m2** — id `6ff1d962` / minor / issue / documentation
scope: `proposal.md What.W11`
summary: W11 已知限制 (`proposal.md:197`) 与 22bh 没列同族的进程命令行列举 `w` (WHAT 列)、`systemd-cgls`、`pidstat -l`: 基线与目标原型对它们均 exit 0 (57 条试探里目标放行 16 条, 其中 11 条是已成文的残余 / 只出名字的形态, 这三类共 4 条未成文)。按各命令手册语义它们列出带参数的命令行; 我**没有**实跑它们的输出 (避免把真实 argv 打进会话), 只验证了守卫退出码。失败场景: 不影响实现, 只是 `systemctl status` 已成文而同族更常用的 `systemd-cgls` 没有。建议: 并入 22ah / 22bh 的已知限制清单并建议开单。

**m3** — id `44510e65` / minor / issue / documentation
scope: `proposal.md SC-12`
summary: `proposal.md:118` 的 12k 清单文字写「2 个头 tag」, 逐类相加 22 + 3 + 1 + 1 + 2 + 1 + 4 + 1 + 1 + 1 = 37, 与「共 38 个 tag」不符 (漏了 `x-api-key-header`; 探针 `W4` 表 `baseline_probe.py:889-934` 实为 38 项)。不改变实现者会做什么。建议: 改「3 个头 tag」。

**m4** — id `cfb2fb14` / minor / issue / testing
scope: `proposal.md Tasks`
summary: Tasks 1.12 (`proposal.md:370`) 的执行条件写「`plugin-cache-currency.py` 报 `PASS`」, 实跑该探针成功时输出 `OK installed=1.74.1 (scope=user) sot=1.74.1`、退出码 0; `PASS` 只是其 docstring 里的判定名, 且 `SKIP` (`##SKIP## …`) 的退出码也是 0。按字面找 `PASS` 永远找不到, 按退出码判则把 `SKIP` 当通过。建议: 写成「stdout 以 `OK ` 开头且 rc=0; 其余 (含 `##SKIP##`) 一律未生效」。

**m5** — id `9ce750ed` / minor / risk / testing
scope: `baseline_probe.py`
summary: Tasks 1.10 要求带 `WPA_REQUIRE_ALL=1` 时 20g 不得是 `n/a`, 而 20g 在 root 下不可构造 (`baseline_probe.py:1247-1250`, `os.geteuid()==0` 即 `n/a`)。aria-runner 容器没有 `USER` 指令, 且 `modes/initial.sh:309-311` 的注释写明 claude-code 在该容器内按 root 运行 —— root 执行席位 (例如日后 Layer 2 重跑本验收) 没有合法路径满足 1.10。本轨 B.2 在 `dev` (uid 1000) 容器, 不受影响, 故只记 risk。建议: 1.10 写明 root 下 20g 的处置 (用 `setpriv` / `su` 降权构造, 或按 Rule #10 上报 owner)。

## 上一轮对账

七个定稿簇 (主控记录) 逐簇核验:

| 定稿键 | 簇 | 状态 | 我核验的证据 |
|---|---|---|---|
| `e8d39a8a` critical (含 cr/M1、km/M1 `fc97f926`) | A: W3 白名单越界 | **closed** | W3 (`proposal.md:81-99`) 删去裸 `$NAME`、`$(…)`、ASCII `...` 三类并成文「保留判据」, Impact / 已知限制 / 待复议 10 同步。基线: 7h / 7i / 7j 对既有键 `yes`、11z `no`; 目标原型 SC-7 10/10、SC-11 26/26。独立坏实现: `$` 加 `[A-Za-z0-9_]+` 整值、`$(…)` 整值、ASCII `...` 结尾各一个, 每个都使 7h 与 11z 转红。7j 15 个边界与 11y / 11z 的强制出形生成器无概率性行。 |
| `ac42f607` major (tl/M1、ba/M3、qa/M3) | K: W11 覆盖 | **closed** | W11 (`:187-197`) 现含 15 词 launcher 超集、带参数选项、绝对路径、`then do else elif` 位置、带 `-` 的 BSD 簇与 `-O`、`/proc` 内联解释器; 22av-22bl 基线 53/53 红, 目标 SC-22 67/67 绿。我另试 57 条常见 `ps` / `pgrep` / `pstree` / `top` / `docker top` / `/proc` 写法: 基线 33 条放行 + 8 条已拦, 目标 41 条被拦, 放行的 16 条是已成文残余、只出名字的形态或 m2 所列。独立坏实现 `drop_launch:unbuffer` → 22aw 转红, `drop_kwpos:elif` → 22az 转红。 |
| `ce6fc59c` major (tl/M2、ba/M4、km/M2 `5fd1f356`) | L: post-ship 腿 | **closed** | Tasks 1.10-1.13 (`:368-376`) 重排: 发版前验收 / 发版 / 发版后惰性诱饵 / 收尾; 头部 Rule #7 声明 (`:14`) 与步骤一致。四条腿在 L1 层实测: 旧 hook (基线) `ps aux \| head -c 0`、`cat /nonexistent-wpa-probe/forgejo/app.ini`、Read 同路径均 exit 0 且只产生零字节输出 / ENOENT, 新 hook 均 exit 2; 两条 L3 腿的生成命令 (`secrets.token_urlsafe` 打印 / 写诱饵文件) 在基线与目标都放行。执行条件有 m4 的措辞问题, 不影响关闭。 |
| `eb350937` major (qa/M2、ba/M1 `e7e041c6`、ba/M2 `51e90cab`、qa/M1 `5ce95ecf`) | M: 枚举逐成员出行 | **partially closed** | 逐成员行与差一对确实落地: 4p 58 键、4s / 5n 各 20、6i / 6j / 6k、16q 29 读取器、19u 31 读取器、22aw 15 launcher、22bc 28 运行 (13 个基线 `/proc` 读取器重放)、上界差一对 19v-19y / 21x-21y 等; 我抽样的 5 个执笔式缺项 / 差一坏实现 (`drop_launch:unbuffer`、`drop_reader:column`、`drop_kwpos:elif`、`ext_occ65`、`vx_assign17`) 全部转红, 与执笔汇总一致。但**仍有存活者**, 见 M1 (既有键 / 提取链 / W4 阈值与回退腿 / W9 空白); 另见 M3。 |
| `60f3173a` major (qa/M4) | N: W5 外来文本 | **closed** | W5 (`:123-128`) 只加 tag 与 `tool_name`, 零 `tool_input` 文本; 13g 14 个敌意路径运行, 基线 0/14、目标 14/14, 13d 全串等值。独立坏实现「插入段内带严格字符集净化后的路径片段」使 13a / 13b / 13c / 13d / 13g 五行转红。 |
| `6bd285b1` major (cr/M2、含 tl/m1 / ba/m4 / cr/m1) | O: 时档对负载不稳 | **closed (带一条提醒)** | W14 (`:229-234`) 改为同次运行交错 A/B 的整进程 CPU 比值 + 活性断言 + 20 s 兜底, 并补 L3 稠密 (i) 档。我用归档的 `timing.py` (仅让活性检查在基线上跳过) 跑**基线对基线负控**, 主机 1 分钟负载 13-30 (4 核): (h1) 0.98、(h2) 0.98、(g 满额) 1.02、(f0 Bash) 1.01、(f0 Read) 1.02, 即比值对负载稳健, 判据不会假红。提醒: `timing.py` 只打印比值与活性、没有判据与退出码 (`grep` 无任何阈值), 「SC-30 全绿」要靠人读数; 建议给它加上界与 rc。 |
| `05982c10` major (km/M3) | P: 关闭关键字 | **partially closed** | 约定 (只写 `Refs`)、Tasks 贯穿行、1.11 / 1.13 引用均落地, 机械检查的正则在命中 / 不命中两侧正确 (A 例); 但判据在 git 失败 / 空范围下真空通过, 见 M2。 |

R2 全部 34 条 minor: 我抽核的均已落地 (15g、27d、28m、28n、26i / 26j / 26k 行在基线输出里存在且符合形态; SC-33 预筛 77/77 通过; 形态行点名 `n/a` 行; 附件头部指向 `writer-v3-proto/`), 此外无我认为仍未处置的 minor。

## 对执笔人自报薄弱点与请裁项的表态

执笔报告 §6 薄弱点 1-8:

1. **原型不是实现、坏实现自构 (同源盲区)**: 可接受 (诚实披露), 但已被证实有牙也有洞 —— 我的独立坏实现找到 M1 / M3 / M4 的存活者。Tasks 1.8 的非作者对抗 review 必要, 并请把本席 14 个坏实现的清单并入。
2. **体量 +40%**: 可接受。削字会造接缝 (本仓 memory 有先例); 代价是 B.2 面大、单次探针 8-9 分钟 (我在负载 20-50 的主机上约 22 分钟)。
3. **时档阈值由单机原型实测定**: 可接受。口径「越界上呈、不放宽」符合 Rule #10; (g) 满额档 2.09 距 2.5 有约 16% 余量。我的基线对基线负控支持「对负载稳健」。提醒 `timing.py` 无判据 (簇 O)。
4. **W1 + W2 使每次 Read 约 3× CPU**: 可接受 (已写进 W1 与 Impact, 均在 5 s 超时内)。Windows Git-Bash 的进程派生成本未测是真风险 (10CG/aria-plugin#203 的报告环境就是 MINGW64), 见风险节。
5. **22bj / 10l 把已接受的误报钉成 `baseline-failing`**: 可接受, **建议保留 10l**。它是可证伪的「该类未被收口」声明, 与 22bj 同体例, 转红即须改 Spec; 删掉则 URL / 资源名 / 策略名这类已接受误报没有任何行, 有人悄悄加排除也无信号。类别标签与 `known-limit` 语义略有错位, 属措辞。
6. **真 bash 3.2 沿用 writer-v2 构建; Windows / macOS / BSD 未实测**: 构建复用可接受 (我复用同一二进制得到同一基线哈希)。但「只缺 macOS / BSD 实测」的说法不完整 —— **同一个 3.2.57 二进制换 locale 就能在 Linux 上复现分歧**, 见 M4; 可在本机验证的轴不应归入「未实测」。
7. **「表里写了、原型没做」只对 W4 表逐项核, 其余章节只抽查**: 自报属实且有后果: 我的扫查在 W4 (阈值 / 回退腿)、W9 (空白 / 零有效条目)、SC-28 (总数字面) 各找到「散文要求大于行覆盖」。可接受作为披露, 不可接受作为收口状态; 请在返修时对 W2 / W4 / W9 做一遍「散文要求 → 行」的反向清点。
8. **cr 的两条非编号风险未采纳**: (a) 有效条目为零不调用 grep —— **不可接受**, 它现在有可证伪判据 (M3: 注释头文件下 Read `/x/README.md` 必须 exit 0), 请采纳。(b) W6 清理对象用记下的变量而非 `rm -rf "$HOME"` —— 可接受不入 Spec: 两个套件除作为输入文本外不改 HOME (`secret-guard.test.sh:1973`、`:2006-2007`), 原型也是专用变量 `_TEST_HOME`; 一行实现注意即可。

执笔报告 §7 请裁项:

1. **待复议 19 (W5 带不带文件信息)**: 同意默认 A。零外来文本最稳妥, 13g 全串等值可证伪; B' 日后可作独立 Spec。
2. **10l 保留或删除**: 保留 (见 5)。
3. **时档阈值与「比值越界上呈、不放宽」**: 同意。
4. **W1 每 Read 成本**: 可接受, 附 Windows 实测缺口。
5. **cr 两条是否写进 Tasks**: (a) 写 (M3); (b) 可写可不写。
6. **km 两条风险**: (a) A.1 认领 (2026-09-30T17:57:13Z, TTL 24 h) 早已过期, 需主控按例行维护续心跳 —— 属实 (今天 2026-10-06), 非本席职责, 外向动作已在 2026-09-17 例行授权内。(b) 建议开单 7.1 里「约 1400 个空段使 hook 超时后命令被放行」的配方: 主仓有 GitHub 镜像, feature 分支推送在一次性授权内会**不可撤回地公开**一个未修的绕过配方。建议 owner 在**首次推送前**决定删去具体数字 (保留在私有笔记), 见风险节。
7. **归档落盘**: 已落盘 (`.aria/notes/2026-09-30-wpa-phase-a/writer-v3-proto/` 在场, 我用其补丁脚本重建了目标原型, 脚本无需改路径即可对我的副本运行)。
8. **Rule #10 自作主张 (a)-(f)**: 同意写进 handoff 请复议; 我核对: `/proc` 纳入内联解释器 (22bg)、W5 零外来文本、10l / 12m / 9l-9m 重做、不写 `report.md` 均在 v3 文字中可见, 无遗漏。
9. **观察 (读席位报告时 L3 / L1 被文本提及触发)**: 本席同样遇到 —— 我自己的一条 Bash 命令因 heredoc 里含 `/proc/<pid>/environ` 字样被现行 L1 拦下 (改用 Write 工具落文件), 读 R2 报告时 L3 对文档式占位示例告警; 与 W3 / W11 已成文的误报类一致。

## 风险 / 疑问 (不计入 finding)

- **Windows Git-Bash 的每 Read 成本与 5 s 超时**: 基线 L3 每次约 150 次进程派生, W1 让每次 Read 都跑完整扫描, W2 / W4 再加若干; Linux 约 0.31-0.66 s, Git-Bash 进程派生慢一个量级, 理论上可能触顶超时 (PostToolUse 超时 = 静默丢告警)。Spec 已披露「未实测」; 建议 B.2 在 MINGW64 实测一次或在 Impact 明确不保证。
- **BSD / macOS 语义**: `grep -F -f` 对空模式文件、`sed -E`、`pgrep -fl` 与 locale 排序规则均未在 BSD userland 验证; M3 / M4 在 Linux 可复现的部分已列, macOS 部分仍是疑问。
- **公开镜像上的未修绕过配方** (建议开单 7.1「约 1400 个空段」): 见表态 7.6。主仓 `https://github.com/10CG/Aria` 公开, 推送是一次性授权内的动作, 决定应在推送前而非推送后。
- **A.1 认领过期**: 头部「认领」行是历史事实, 但 claim 心跳 TTL 已过, 起 B.1 前需按例行维护续期或重新认领 (协调 ref 推后 `ls-remote` 核验)。
- **W11 的文本提及误拦 (22bj) 会更常打到 AI 自己的写作流**: 本席一次审计内就被基线 L1 拦过一次; W11 扩大后「heredoc 里以 `ps aux` 起行」也会被拦。Spec 已成文并给出「用 Write 工具落文件」的处置, 但被拦当下 AI 看不到这条建议 (BLOCKED 文案冻结), 与 10CG/Aria#221 评论 25898 的 ack 疲劳担忧同向 —— 待复议第 5 条与第 2 条宜合并裁 (Spec 已建议)。
- **Level 2 与体量**: 14 个工作项 / 383 行探针 / 同步面 16 + 6 个文件, 已由决策单第 3 项裁 Level 2 并列入待复议第 4 条; 从可证伪性看, 体量越大「散文要求 > 行覆盖」的缺口越多 (见 M1 / M3 / m1), 属过程风险而非阻塞。
- **探针与原型的共同盲区**: 我的坏实现与执笔的都在「文本替换出的原型」上, 与真实现的结构可能不同; Tasks 1.8 的非作者审阅仍是最后一道。
- **SC-33 在基线恒绿 (设计如此)**: 鉴别力完全来自「去掉熵下限使清单外 5 个文件命中」的变异, 我未复跑 (控制实验规模)。

## Verdict

**PASS_WITH_WARNINGS** — counts: **0C/4M/5m**。

Vote: **REVISE** (有 major)。

## 是否足以进入 A.2

不足以: 仍有 4 条 major (M1 补 8 个存活坏实现对应的行, M2 修正机械检查的判据, M3 补零有效条目矩阵, M4 给 32c 加 locale 腿并约束字符类), 均为补行 / 改判据 / 补一句约束, 不涉设计取舍, 一轮窄返修后即可复核; R2 的其余五簇已关闭。
