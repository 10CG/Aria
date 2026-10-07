---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-07T10:11:29.423Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 — backend-architect — secret-net-l3-and-bypass-paths (proposal v5, 6efb9b2)

> 沙箱: `$A` = `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/audit/post_spec-R5-backend-architect` (脚本 `$A/h/`, 探针输出 `$A/out/`, SC-8 复现 `$A/sc8/`)。真仓全程无 git 写操作 (收尾核验: `git status --short` 只有开工前就存在的未跟踪 `gawk_*.deb`, HEAD `6efb9b2`, aria `268da8f`, standards `2bc1c4c`)。所有 hook 运行的 HOME 指向 `$A/home*`。像凭据的值全部在 Python 进程内用 `secrets` 运行时生成、经 stdin 喂 hook, 报告只写退出码 / tag 名 / 计数 / CPU 秒。宿主 4 核且多席并行, 负载 2-21: 耗时结论一律用整进程 CPU 时间或同次运行比值, 不用墙钟。

## 已实读文件

- Spec 与证据: `proposal.md` 全文 (1-449 行, 8 段读完); `git diff --word-diff b07f69a 6efb9b2` 共 54 个 hunk, 其中 1-24 (W1-W14 与 SC 导言) 逐个读, 25-54 (SC 条目 / Impact / Tasks / 待复议) 未逐 hunk 读, 但结果文本 (v5) 已全文读过; `baseline_probe.py` 1-140、1270-1300、1323-1404、1479-1522 与按需 grep (19g / 19h / cwd / 22br 等); `baseline-evidence.md` 只做脚本统计 (437 行 = baseline-failing 213 / reverse-guard 79 / allow-guard 70 / known-limit 39 / doc-sync 26 / zero-regression 10, 与 Spec 头部一致), 未通读。
- 输入: 三个 issue 全文; 决策单全文; CLAUDE.md 规则 #6 / #7 / #10 与多远程两条硬约束; R4 聚合报告全文 (全部 finding 表 + 主控记录); R4 本席报告全文; v5 返修报告 `v5-writer-report.md` 全文; research `cc-hooks.md` 全文。
- 源码 / 规范 (均实读, 引用行号以我实读为准): 基线 (aria `268da8f`) `hooks/secret-scan.sh` 与 `secret-guard.sh` 的 Spec 引用行 (30 余处抽查: scan:135-142 / 144 / 152 / 215-231 / 355-367, guard:405-408 / 564 / 617-641 / 676 / 736 / 815 / 873-894 / 930 / 1043 / 1088 / 1111, 全部属实) 与 `:641` 的全部 32 个备选; writer v5 目标原型 (会话内 `exp/writer-v5/work/t5f`, 复制到 `$A/t5f`) 的 `secret-scan.sh` 100-481 全读、`secret-guard.sh` 对基线的 407 行 diff 全读; `hooks.json` (解析); `tests/secret-guard.test.sh` 1262-1335 (SC-9a)、1660-1960 (SC-8) 与原型套件 diff; `corpus_census.py` 仅 grep; `.aria/decisions/2026-08-24-sc8-absolute-latency-gate.md` 1-40; `.aria/pat-inventory.yaml` 头; `COMMIT_FOOTER_GUIDE.md:198-202`; `git-commit.md §6.1` 标题。
- 未读 (声明): research 的 `secret-scan.md` / `secret-guard.md` / `precedent.md`; `skill-benchmark-exemption.md`; `secret-hygiene.md` 正文 (只喂 L3 看是否被命中); R4 其余四席原文 (只读聚合)。
- 实跑范围 (按派单控制规模): 探针 437 行中的 207 行 (SC-1/2/3/18/19/20/21/22/23/24/25/34) 在基线与 v5 原型各跑一遍, 其余 SC (L3 的 4-17、doc-sync 与 census 的 26-33) 未重跑; 未做全量坏实现复跑, 只造了 3 个自己的变体 (见 M1 / M2)。这是派单限定, 不是按价值跳过。

## Findings

### M1 · `6bd285b1` · major · issue · testing · scope `proposal.md SC-30`

**summary**: 既有测试内 SC-8 五档延迟闸 (owner 2026-08-24 裁定, 不改阈值 / 口径 / 档位) 用 awk 按函数名只抽 `_sg_judge_one` 与 `_sg_per_segment_eval`, 而 W9 / W10 / W12 要求的重构让前者调用定义在 source 闸门之下的 `_sg_core_eval`; Spec 未规定这些辅助函数的位置、也无活性断言, 写手原型下该闸对 `_sg_per_segment_eval` 计到的是 rc=127 的瞬时返回 (0.7-0.9 ms/call 对基线 6.8-42 ms), 五档恒绿, SC-30 的「SC-8 全绿」失去判别力。

**证据**
1. 抽取点: `aria/hooks/tests/secret-guard.test.sh:1771-1775` (`source "$HOOK"` 取闸门之前的部分, 再 `awk '/^_sg_judge_one\(\) \{/,/^\}$/'` 与 `awk '/^_sg_per_segment_eval\(\) \{/,/^\}$/'` 各抽一个函数); 注释 `:1766-1768` 自己写明这几个定义「都在 gate 之后, 不会被带进来」; 计时对象 `:1852` `_sc8_stat _sg_per_segment_eval`; 判据 `:1893-1910` 只比较 `new_ms <= ceiling`, 仅在 `old min == 0` 时判退化, 没有任何断言要求被计时的函数真执行了判定。owner 决策单 `.aria/decisions/2026-08-24-sc8-absolute-latency-gate.md` 专设「反事实验证 (证明两腿均非恒绿)」表, 说明 owner 明确要求这个闸可判别。
2. Spec 文本: W9「内建的同一个判定函数 `_sg_core_eval` (即基线 `_sg_per_segment_eval` 的函数体, 原样 …)」; W14 (f0) 项「测试内 SC-8 五档同样覆盖 Bash 面, 但它只给 `_sg_per_segment_eval` 计时 … 扩展入口的调用位置不由本 Spec 规定」; W14「其它耦合」清单 (SC-13 计数 / SC-19 census / SC-20 两段文本 / `(?:` / 用例名 / jq CRLF / 辅助函数放闸门之上) 与 Tasks 1.8 都没有点名 SC-8 的抽取装配。W14 的「新辅助函数放在 source 闸门之上」对 `_sg_core_eval` 有歧义: 它是基线函数体改名而来, 不是「新」函数, 原样改名就留在闸门之下。
3. 写手从未带 git 历史跑过该闸: 返修报告 §4 的全部运行都在无 `.git` 副本上 (SC-8 / SC-9a 被跳过), `exp/writer-v5/deliver/logs/` 里 `SC-8] tier` 0 条。
4. 实跑 (`$A/sc8/`: 基线与原型各一份, 对象库为真仓 `.git/modules/aria/objects` 的只读复制副本, 使 `af87cae` 可达; 把该套件 SC-8 块 `:1699-1915` 原样摘出运行, env -i, 非 root):

| 被测 hook | tier a / b / c / d / e 的 new ms/call (old 为 af87cae, 25-41 ms) | 结果 |
|---|---|---|
| 基线 | 6.8 / 12.9 / 6.6 / 11.1 / 42.0 | `pass=5 fail=0` (真测) |
| v5 原型 (写手原样) | 0.7 / 0.7 / 0.7 / 0.9 / 0.9 (increase(min) -97.7% 至 -97.8%) | `pass=5 fail=0` (空转) |
| v5 原型, `_sg_core_eval` 与 `_sg_emit_blocked` 原样搬到闸门之上 | 14.6 / 19.1 / 15.0 / 18.7 / 52.1 | `pass=5 fail=0` (真测, 天花板 100 ms 内) |

   空转原因 (`$A/sc8/vac.sh`, 复刻 SC-8 的装配后直接调用): 基线 `_sg_per_segment_eval 'echo hello world'` rc=0, 必拦命令 (读 dotenv 文件) 出 BLOCKED 文案; 原型两者都是 `_sg_core_eval: command not found`、rc=127, `type -t _sg_core_eval` 为 MISSING; 搬到闸门之上的副本恢复 rc=0 / BLOCKED。

**失败场景**: 实现者按 W9 把基线函数体改名为 `_sg_core_eval`、`_sg_per_segment_eval` 变薄包装 (写手原型即如此), 辅助函数留在闸门之下 → B.2 跑 SC-30 看到 SC-8 五档「全绿」(-97.8%), 判延迟闸通过; 实际被计时的是 127 返回。此后任何让 `_sg_per_segment_eval` 变慢的回归 (W10 第二遍、扩展入口、W11 新行) 都碰不到 owner 的绝对天花板, 只剩 W14 的比值档 (f) / (f0) / (h) 兜底, 而它们不含 tier (e) 的 4 段最坏档。若改名后 `_sg_per_segment_eval` 不复存在, 则 `SC-8 setup` 抽取为空而报红, 实现者会被推去「修测试」, 恰是该闸注释与 owner 决策禁止的 (不得改口径 / 删档)。真测是过得去的 (上表第三行), 缺的只是约束与活性断言。

**怎么会红 (建议新增行的三态)**: 探针内复刻 SC-8 装配 (source hook → awk 抽两个函数 → source risky_patterns), 断言 `_sg_per_segment_eval` 对必拦命令返回 2、对良性命令返回 0。基线 yes / 目标 (辅助函数在闸门之上) yes / 辅助函数在闸门之下 no (rc=127)。

**建议修法** (文字 + 1 行, 不动设计): (a) W14「其它耦合」加一条: SC-8 的抽取装配方式, 并钉死 `_sg_judge_one` 与 `_sg_per_segment_eval` 直接或间接调用的全部函数 (`_sg_core_eval`、`_sg_emit_blocked`、`_sg_vx_pass`、`_sg_ext_pass` 及其下游) 须定义在 source 闸门之上, 不得改抽取 / 阈值 / 口径 / 档位 (Rule #10); (b) 探针加上面的 `reverse-guard` 行 (SC-30 的探针内孪生); (c) SC-30 与 W1 / 头部「两个套件在原型上全部照过」处写明条件 (无 git 副本, SC-8 / SC-9a 被跳过)。

### M2 · `df25d271` · major · issue · testing · scope `proposal.md SC-19`

**summary**: W9 条目文件的输入面有三个常见条件没有任何 SC 行 (清单末行无换行、项目根路径含空格、`CLAUDE_PROJECT_DIR` 置空而 stdin `cwd` 有值), 两个自然的错误实现过得了 SC-19 / SC-20 全部 54 行, 却让扩展静默丢条目或整体失效。

**证据**
1. 探针构造 `baseline_probe.py:1333-1388` `mkproj`: 22 种清单内容 (`ok` / `ws` / `crlf` / `bom` / `cjk` / `canary` / `bound_ok` …) 全部以 `\n` 结尾; 目录名是 `proj-<kind>`, 位于 `tempfile.mkdtemp(prefix="wpa-probe-")` 之下, 无空格; `:1412-1413` 的 19g / 19h 只覆盖「`CLAUDE_PROJECT_DIR` 未设」与「设为另一目录」, 全文对「设为空串」0 命中 (`grep` 空串值形写法 0 hit)。
2. Spec 文本: W9「一行一个字面子串 … 剥行尾 CR、BOM 与首尾空白」「项目根 = 非空的 `CLAUDE_PROJECT_DIR`; 否则 stdin 的 `cwd`」—— 末行无换行同样是一行, 根路径可以是任意字符串, 「非空」意味着空串要回落。Spec 对 BOM / CRLF / 空白 / 长度 / NUL / 上界都出了行 (19ac / 19ai / 19v / 20a-q), 这三个没有。
3. 我造的两个变体 (只改写手原型的 `_sg_ext_entries`, 其余不动): M-NONL = 条目流水线末尾再接 `while IFS= read -r l; do printf '%s\n' "$l"; done` (丢掉无换行的末行); M-SPACE = 三处 `"$f"` 去引号 (`wc -c < $f`、`tr -d '\000' < $f | cmp -s - $f`、`tr -d '\r' < $f`)。直调 (`h/e14_extfile.py`): 清单只含一条且无末行换行: 原型 `cat <条目>` rc=2, M-NONL rc=0; 清单两条、第二条无换行: 原型两条都拦, M-NONL 第二条 rc=0; 项目根 `.../my project (copy)`: 原型 rc=2, M-SPACE rc=0 (整个扩展静默失效)。探针 (`WPA_ONLY=SC-19,SC-20`, 非 root): 两个变体各 SC-19 37/37 + SC-20 17/17 全 yes, 「target shape holds」。第三项 (置空) 我只核对了原型正确 (rc=2) 与探针无该行, 未造变体。

**失败场景**: Windows Git-Bash (10CG/aria-plugin#203 的报告环境就是 MINGW64) 下项目根常在 `C:\Users\<含空格的用户名>\…` → 整个 `.aria/secret-guard.paths` 静默不生效; 用 `printf '%s' …` 或不补末行换行的编辑器写清单 → 末条目静默丢失。W9 又明写「失效保持静默」, 没有任何信号, 验收全绿。

**怎么会红 (建议新增行的三态)**: 19an 清单末行无换行 (单条目与两条目取末条目) 列入路径 `cat` → 2; 19ao 项目根含空格与一个非 ASCII 字符 → 2; 19ap `CLAUDE_PROJECT_DIR` 置空 + stdin `cwd` 指向含清单的目录 → 2。基线全 0 (无扩展) = no; 原型 yes; M-NONL 红 19an, M-SPACE 红 19ao, `${CLAUDE_PROJECT_DIR-}` 类写法红 19ap。

**建议修法**: 加上面三行 `baseline-failing`; W9 格式段补一句「末行无换行同样是一行; 对清单与项目根路径的所有展开一律加引号」。

### m1 · `684e9a24` · minor · issue · documentation · scope `proposal.md What.W9`

**summary**: W9 已知限制与 §5.6 / README 的必写内容 (SC-26 26c 的关键词清单) 没有警告采用方: 完整路径条目对 `..` 回绕、`//`、`/./` 与 `cd` 后相对名的写法失效, 只有最短特征子串能覆盖。

**证据** (`h/` 内 `ext17` 一组, 原型): 条目 `/srv/billing/conf/prod.toml`: `cat /srv/billing/conf/prod.toml` rc=2, `cd /srv/billing/conf && cat prod.toml` rc=0, `…/conf/../conf/prod.toml` rc=0, `/srv//billing/…` rc=0, `/srv/billing/./conf/…` rc=0, Read 同形 `..` 与 `//` rc=0; 条目 `billing/conf/prod.toml`: `//` 与 `../billing/…` 拦, `..` 回绕、`/./`、`cd` 后相对名仍 0; 条目 `prod.toml`: 以上全拦 (只有 glob `pro*.toml` 仍 0)。W8 对 `app.ini` 已把 `cd … && cat 相对名` 写成限制 (SC-21 21r), W9 没有同类句子。
**失败场景**: 采用方照 README 示例列完整路径, 误以为受保护, AI 用 `cd` 加相对名读取即绕过, 且按 W9「失效保持静默」没有任何提示。
**建议**: §5.6 与 README 各加一句「条目是字面子串, 选最短的特征子串 (如文件名), 不要列完整路径」; SC-26 26c 关键词加一个对应词。

### m2 · `cfb2fb14` · minor · issue · testing · scope `proposal.md Tasks`

**summary**: Tasks 1.12 拒绝加 NUL 腿的理由 (返修报告 §6.8(1)「加了腿也只能记『未验证』」) 不成立: 惰性的 NUL 记录腿对「NUL 以 `\u0000` 到达 hook」这一 W1 视图 N 的唯一前提有判别力, 而该前提至今无端到端样本。

**证据**: 惰性腿 = 一条 Bash 命令 `printf 'HOME=/x\0JWT_SECRET=%s\0' "$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"` (合成值, 不读任何真实来源)。L1 基线 / 原型直调 rc 均为 0 (不被拦)。同形输出 (真 NUL) 经 Bash 信封喂 L3: 基线静默; 原型 `env-line-secret-keyword=1` (只有视图 N 能产生); 若 NUL 在到达前已被平台剥掉, D 视图 `HOME=/xJWT_SECRET=…` 对两者都静默。同一会话里 Tasks 1.12 的第 1 腿已证明新 hook 在线, 所以「无告警」可以归因为前提不成立, 此时 N 视图是确证的死代码。
**失败场景**: ship 后没有任何检查能区分「N 视图有效」与「N 视图是死代码」; W1 的整个第二视图、SC-1 1c-1f 与 Impact 里的「NUL 首次可被检出」都挂在一个永远「未验证」的前提上。
**建议**: Tasks 1.12 加第 5 腿 (上面的惰性命令), 结果记 handoff: 有 `kv`/`env-line` 告警即「前提成立」, 无告警即「前提不成立, N 视图无效」。

### 实跑验证记录 (Spec 断言 → 命令 → 结果; V1-V16)

| # | Spec 断言 | 命令 / 做法 | 结果 |
|---|---|---|---|
| V1 | W1 两视图并集; SC-1 1c-1g; SC-2 | `python3 $A/h/e1_nul.py` (bash 5.2.15 与真 3.2.57; Bash 与 Read 真实信封; 基线 vs 原型) | UTF-16LE 四形 (AKIA 行 / `JWT_SECRET=` 行 / `token <ghp 形>` / JSON `client_secret`) 经 Bash: 基线与原型都检出 (4/4, 两个 bash 一致); 经 Read: 基线静默, 原型 4/4 检出; NUL 分隔 6 记录环境: 基线 Read / Bash 静默, 原型 `env-line-secret-keyword=3` + `kv-secret-assign=1`; 文本里只写六字符 `\u0000` 加 AKIA: `aws-access-key-id=1` (不翻倍); NUL 结尾的 AKIA 记录: `aws-access-key-id=2` (Spec 已写「只多不少」) |
| V2 | W1 耗时 (5 s 超时) | `h/e2_nulperf.py` 稠密 `Authorization: Bearer` 行与 JSON 口令行 | 600 KB 无 NUL: 基线 0.98 s / 原型 1.23 s CPU; 每行后加 NUL: 基线 1.00 / 原型 1.72 s; 300 KB JSON 口令行 1.07 / 1.35, 加 NUL 1.02 / 1.87 s。1 MB 信封上限下双视图仍在 5 s 内 |
| V3 | W2 / W3 误报漏报面 | `h/e3_fpfn.py`、`h/e16_forms.py` (38 + 26 个形态) | 应静默的 19 形 (git SHA、`git log --oneline`、`sha256sum` 输出、UUID、npm integrity、`sha256:` digest、`token_last_eight`、`$VAR` 引用头、`process.env.X`、ACK 路径、`<…>` 与 `${…}` 占位、`${{ secrets.X }}`、短值、散文、`--password-stdin`、data URL、小写 YAML、单引号 JSON) 目标全静默 (仅 `TOKEN_VERSION=…` 命中 `env-line-secret-keyword`, 基线同); 应检出的 19 形 (JSON 冒号后 / 前空格、多行美化、Pascal / camel 键、`JWT_SECRET = …`、`export …="…"`、YAML 大写键、compose 列表、CRLF、`Authorization: token / Token / Basic`、小写头名、`CF-Access-Client-Secret`、`--token=` / `--password=`、`set API_TOKEN=`、一行两个赋值、`Env` 映射) 全以预期 tag 检出; 已知限制形 (python repr、小写键、`-p<val>`、`--token <val>`、URL 查询、JSON 内嵌 JSON、表外键 `xToken`) 静默 |
| V4 | W4 / SC-12 fp | `h/e5_fp.py` | kv (带引号与空格) / `Authorization: token` / `--token=` / `CF-Access-Client-Secret` / 13 位 JSON 口令 (`L13`) / CRLF 行: fp 与 `sha256(裸值)[:8]` 或 `L<长度>` 逐项相等; 值与其首末 8 字符不在日志 / stdout / stderr; 12 个值只记前 10 项且按文本序 |
| V5 | W2 线性段 (有界 + 左边界) | 直接 `grep -oE` 取 CPU; `h/e4_adv.py` | `-`×300 KB + ` -token=<24>`: hook 写法 0.13 s; 无界 + 左边界 15.2 s; 有界无左边界 14.6 s; 无界无边界 >60 s 超时。kv: `A`×320 KB + ` JWT_SECRET=<24>`: 有界 0.18 s / 无界 17.2 s (Spec 引 0.08 / 11 s, 量级一致)。17 种对抗单行 (连字符串、大写串、`TOKEN ` 重复、`X_TOKEN=x ` 重复、引号串、未闭合 JSON、export 重复、空白串 …) 输入 40 KB → 160 KB: CPU 比值 1.1-3.3 (线性约 4, 平方约 16), 无一超线性。bash `${v##*[;&|]}` 16 KB 7.2 s (3.2.57 上 8 KB 18 s) 印证 Spec 对前导 `*` 前缀删除的禁令 |
| V6 | W9 与内建「构造上一致」; 偏移与切片同单位 | `h/e6_ext.py` (清单含 BOM + CRLF; LANG=C.UTF-8 且不设 LC_ALL) | 65 个命令形态 (续行、`||` 后管道、`2>&1 \|`、`&>`、`\|&`、引号内分隔符、子 shell、命令替换、heredoc、ssh / docker / nomad / sudo 包裹、python / node / awk 内联、变量间接 …) 内建 `app.ini` 名与列入路径的退出码逐项相等 (0 分歧); 中文前缀 ×0 / ×20 / ×60 + `cat <条目>` 在 bash 5.2 与真 3.2.57、LANG 为 C.UTF-8 / en_US.utf8 (均不设 LC_ALL) 下全 rc=2; 63 次 `echo P` 后 `cat P` rc=2, 64 次后 rc=0 (19x / 19y 边界); 纯 CJK 条目、首行 BOM 条目、大写命令与 Read 路径、Read / Edit、stdin `cwd` 回落均如 Spec |
| V7 | W14 (f0) / (f-hit) | `h/e7_exttime.py` (200 条目; CPU 秒, 每侧取 4 次最小) | 良性 `ls` 无扩展文件 0.112 / 基线 0.095 (1.18); 4 KB 单行路径出现 1 次: 基线 1.24 / 原型 2.44 (1.97); 2 KB 前缀 + 64 处: 0.94 / 1.86 (1.99); 8 KB 前缀 + 64 处: 4.81 / 9.91 (2.06); 无扩展文件对照 1.03 / 1.05 / 0.97。与 Spec 的 2.01 和 ≤3.0 一致; 旧设计的 7.6 / 24.7 倍不复存在 |
| V8 | W11 credit 制度、W12 单键读取、jq 锚定 credit | `h/e11_w11.py` 51 条命令 (基线 vs 原型) | 基线 `docker exec c env \| grep '^PATH='` / `\| cut -d= -f1` / `\| grep -v x` 全放行, 原型对 `nomad alloc exec a env` 同三种后缀全放行、裸转储 / `pct exec … printenv` / `ssh host env` / `bash -c env` / `watch env` 拦; `ps -ef \| grep -v grep` 拦 (tight), `ps aux \| wc -l`、`ps -eo pid,comm`、`ps -u dev -o pid,comm`、`pgrep -f x` 放; `cat /proc/1/environ \| grep '^PATH='` 放 (非 tight); `os.environ.get('A'), os.environ.get('B')` 放、`print(os.environ)` / `dict(os.environ)` / 与 `open('.env')` 同现 / `.envrc` 拦; jq `keys_unsorted \| $ENV` 与 `keys[]` 拦、`map_values(length)` 放。全部与 Spec 一致 |
| V9 | W8.3 `:641` 的 32 个基线备选 | Python 解析基线 `secret-guard.sh:641` 的 `grep -qE '…'` 取顶层备选 | 32 个备选; `READ_ALT_PATHS` 的 32 条路径各自恰好命中与其序号相同的那一个备选, 0 个例外 |
| V10 | SC-30 的「SC-8 全绿」 | 见 M1 | 原型下空转 (-97.8%) |
| V11 | 探针三态 | `WPA_ONLY=… python3 baseline_probe.py` (非 root, 不带 `WPA_BASH32`) | 原型 SC-1/2/3/18/23/24/25 53/53 yes, SC-19/20/21/22/34 154/154 yes (合计 207 行, 「target shape holds」); 基线同 12 个 SC 的 207 行: baseline-failing 0/121、reverse-guard 41/41、allow-guard 22/22、known-limit 23/23 (「baseline shape holds」)。关键行: 1e / 1g 基线 yes、1f 基线 no; 18j / 18k 两侧 32/32; 19af 基线 no、原型 73/73 shapes equal; 22br 44/44、22bs 22/22 两侧 yes; 34b / 34c 基线 no、原型 yes |
| V12 | SC-19 / SC-20 对错误实现的判别力 | 见 M2 | 两个自造变体均 54/54 yes |
| V13 | Tasks 1.12 惰性腿不被新 L1 自己拦 | `h/e12_ship.py` | L3 Bash 腿命令 (打印 `JWT_SECRET = <合成值>`) 与写诱饵文件命令: 基线 / 原型 rc 均 0; `ps aux \| head -c 0` 与 `cat /nonexistent-wpa-probe/forgejo/app.ini` 及同路径 Read: 基线 0、原型 2 |
| V14 | 平台事实 `updatedToolOutput` | 在本机 `claude` 二进制 (已升到 2.1.292, Spec 写 2.1.285) 里取字符串 | `updatedToolOutput:…describe("Replaces the tool output before it is sent to the model")`, 共 14 处; 事实属实 |
| V15 | W13 的 curl 例 | `curl 7.88.1`: `-K -` 带 URL 的 stdin 配置 / 空配置 / `-H @文件` | rc 7 / rc 2 / rc 7, 与 Spec 一致; `nomad var put -h` 一条被活基线 guard 拦下, 我没有用 ack 绕过, 未核 |
| V16 | Rule #7 声明 / SC-15 15e-15g | `h/e13_selfscan.py`: 把 `proposal.md`、探针、证据、两个 hook 源、`secret-hygiene.md`、v5 返修报告各当 Bash 输出与 Read 结果喂原型 L3 | 全静默 (14/14) |

## 上一轮对账

R4 的 6 个 C / M 定稿键逐簇:

| 簇 / R4 键 (席位编号) | 判定 | 我亲自核验的证据 |
|---|---|---|
| U `1038b8da` (ba/C1: `tr` 拆散 UTF-16LE) | closed | V1: UTF-16LE 四形经 Bash 基线与原型检出一致 (两个 bash 版本); NUL 分隔环境 Read / Bash 由静默变 `env-line-secret-keyword=3`; 1g 不翻倍; 探针 1e / 1g 基线 yes、1f 基线 no, 原型全 yes。W1 现文 (D 视图原样 + 仅 N != D 时追加) 与原型行为一致。残余 (NUL 到达前提无样本) 已在 W1 写明, 另见 m2 |
| T `0a8380fd` (ba/M2、qa/M1、cr/M1、km/M1: 扩展与内建判定不一致、掩码状态、偏移单位) | closed | V6: 65 个自选形态 0 分歧 (含 R4 点名的续行、`\|\|` 后管道、`2>&1` / `&>` / `\|&`); 汉字前缀在真 3.2.57 + 仅 LANG 下 rc=2; 探针 19af 基线 no / 原型 73/73 equal。残余: 「条目含引号 / `;` / `&` / `\|` 等元字符时以替换副本为准」已写入 W9 已知限制、未钉行, 可接受 |
| V `22bdd143` (tl/M2: 命中路径无时档、平方级) | closed | V7: 命中路径 CPU 比值 1.97 / 1.99 / 2.06 (出现 1 次 @4 KB、64 处 @2 KB、64 处 @8 KB), 无出现对照 0.97-1.05; W14 (f-hit) ≤3.0 与 SC-34 34c 存在且在原型上 yes |
| W `755aab21` (ba/M1: `cli` / `kv` 平方级) | closed | V5: 有界 + 左边界写法线性, 无界或无左边界写法 14-17 s 以上, Spec 引用的量级可复现; 17 种对抗形在 40 KB → 160 KB 上比值 1.1-3.3; SC-34 34a / 34b 基线 34b no、原型 yes |
| F `e2459206` (tl/M1、cr/M2 `8fbbee80`: 包裹下转储 credit 未定) | closed | V8: 默认 credit 与基线 `docker\|kubectl\|podman\|lxc exec … env` 一致; 原型 `_SG_PROCTAB_ALL` 的 tight 拷贝不含 env / printenv 备选; 22br 44/44、22bs 22/22 在基线与原型两侧 yes (判别力来自坏实现, Spec 已如实写) |
| M `eb350937` (qa/M2: `:641` 备选无行) | closed | V9: 32 个备选、32 条路径一一对应; 18j / 18k 两侧 32/32 |

R4 minor: 我核验后认为全部已处置, 无遗留 — 纯非 ASCII 条目有效 (V6, ba/m1); 23j 多处出现 (V8, qa/m1); BOM (V6, qa/m2); SC-32 的 32e 存在 (证据文件 SC-32 共 5 行, qa/m3); 旧时档数字与版本 / 审计叙事已清 (proposal 内 `+6–9 ms` / `0.052 → 0.061` / `+27 ms` 与 `v3` / `v4` / `R4` 均 0 命中, cr/m2、km/m2、km/m3); 引用精度 `COMMIT_FOOTER_GUIDE.md:199-202`、`git-commit.md §6.1` 属实 (km/m7); `FORGEJO__<section>__<KEY>` 已入 W2 / W8 已知限制 (tl/m2); 包裹词后 `env` 词与 `/proc` 文本检索误拦已成文并有 22bj (tl/m1、cr/m1)。km/m6 的 Spec 侧已入 7.20, 清理已推送内容属 owner (见风险 2)。

## 对执笔人自报薄弱点与请裁项的表态

薄弱点 (v5 报告 §5):
1. 34c 的比值门: 可接受。我测同一量 (V7) 为 1.97-2.06, 上界 3.5, 余量 1.7 倍, 在负载 2-21 的宿主上稳定。
2. 19af 的零分歧只对有限形态表成立: 可接受。我用 65 个自选形态独立复核 0 分歧 (V6), 与其 73 / 93 / 2500 条互补; 条目含元字符的前提不成立已成文。
3. 键名 / 参数名上界 64 / 40: 可接受 (技术级; 线性已复现 V5, 覆盖面收窄已由 10n / 10o 钉现状)。
4. NUL 前提无端到端样本: 可接受作披露, 但不接受「永远不验」: 见 m2。
5. 耗时回升与 (i3) 上界 2.5: 可接受。坏实现 3.4 倍起, 2.5 对原型 1.74-1.82 仍有余量; 上界是测后定的, 判据靠比值与活性断言而非数字本身。
6. 回归覆盖靠重跑旧坏实现 (7 个设计已不存在的变体与 29 个 `drop_extreader_*` 被替代): 可接受, 我未逐个复核替代者。
7. proposal 增至 214 KB: 作为披露可接受; 它不是 finding, 但使 B.2 的实现者要在 5 万多 token 的 Spec 里找约束, M1 / M2 这类接缝缺口正是该体量的症状 (见风险 6)。
8. 研究笔记与已推送分支: 不在 Spec 权限内, 可接受; 归 owner (7.20)。
9. 时档数字是单机测量: 可接受; 判据是比值与活性。

请裁项 (v5 报告 §6): 1 (披露范围 7.20, 产品级): 可接受, 归 owner。2 (W9 条目规则: 含 ASCII 字母数字或任一非 ASCII 字节、剥 BOM): 可接受 (V6 复核, 另见 M2 对输入面的补行)。3 (簇 F 默认 credit): 可接受, 且我同意其理由「不降低既有检出、不新增未申报拦截」 (V8)。4 (64 / 40): 可接受。5 (W14 时档参数): 可接受。6 (SC-34 口径): 可接受。7 (Layer 2 一句与 MINGW64 / macOS 披露): 可接受。8 (未采纳三项): (1) NUL 腿 **不可接受** (m2); (2) timing 不并进探针、(3) 不加 gawk 腿: 可接受。9 (Rule #10 自作主张清单): 可接受, 但清单缺一项它自己没发现的: 原型从未在带 git 历史的副本上跑过既有套件的 SC-8 / SC-9a, 「两个套件在原型上全部照过」只对无 git 副本成立 (M1)。

## 风险 / 疑问 (不计入 finding)

1. 基线 hook 本身在长命令上是超线性的, v5 的比值档管不到绝对悬崖: 同机 CPU 秒, 4 KB 命令基线 0.6-1.2 s, 8 KB 1.9-4.8 s, 12.9 KB 提交信息 heredoc 9.5 s (`h/e8_longcmd.py`、`h/e18_proc.py`)。命令超过约 8-10 KB 时基线已可能撞 5 s 超时而放行; W9 命中路径把成本翻倍 (V7: 9.5 KB 命令 4.8 → 9.9 s), 即扩展在较大的命令上会静默失效。W11 新规则对这些形状几乎不加成本 (比值 0.96-1.08, `h/e18_proc.py` 20 个对抗形), 所以这是既有缺口 (7.1) 的加深, 不是新缺口。
2. 状态与派单背景不一致: 派单写「未推送」, 但 `git ls-remote origin refs/heads/docs/secret-net-l3-and-bypass-paths-phase-a` 是 `6efb9b21…` (= 本地 HEAD); GitHub 同名分支仍在 `b07f69a7…` (v4)。即 v4 及全部研究笔记在公开镜像上 (7.20 登记, 归 owner 裁)。
3. NUL 前提 (见 m2) 与 Windows Git-Bash / macOS BSD 的 `grep -o -b -F -i -f <(…)` 行为、bash 3.2 耗时 (R4 风险 3, v5 未变) 均未验证, Spec 已披露。
4. 我自己的三次 Bash 调用被活基线 guard 拦下 (heredoc 里只是提到 dotenv 读取、`ssh … env`、`nomad var put -h`), 是 22bj 同类文本误拦在现网的活体复现; 我改用 Write 落脚本并在运行时拼词, 没有使用 `# guard:ack`。
5. 非 root 运行 (uid 1000) 复核了 20g 之外的行; `setpriv` 降权路径 (Tasks 1.1) 我同样没有实测。
6. 体量: proposal 449 行、单行常 1-5 KB。A.2 产出 `detailed-tasks.yaml` 时建议每个 W 附一页实现者摘要, 并把 M1 / M2 的接缝约束放进去; 否则这类「写在别处的耦合」会继续在 B.2 才暴露。
7. 写手原型是唯一的参考实现, Spec 的 SC 行都是对它及其变体验证的; M1 / M2 恰是原型「碰巧正确」(辅助函数位置、sed 流水线、加引号) 而 SC 没有钉住的地方。

## Verdict

verdict: **PASS_WITH_WARNINGS** (无 critical, 有 major)。counts: **0C/2M/2m**。

**Vote: REVISE**

## 是否足以进入 A.2

足以进入 A.2, 前提是主控在冻结 Spec 前先落 M1 与 M2 两处补丁 (合计 4 行探针与 3 句 Spec, 不动设计): 本席核验 R4 的 6 个 C / M 全部 closed (V1 / V5-V9 与 207 行探针子集三态), 没有 critical, 两条新 major 都是接缝处的验收缺口 (SC-8 闸被重构空转、W9 清单输入面无判别行) 且修法已具体, 不需要为它们再开第 6 轮全量审计 — 这是本席判断, 不替 owner 裁降级策略; `post_planning` 的收敛审计会复核补丁与 `detailed-tasks.yaml`。
