---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-01T05:17:40.438Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- 被审对象 (`b3e3123`):
  - `proposal.md` 全文 (1-402)。
  - `baseline_probe.py`: 1-381 (生成器、信封、执行器); SC-4 至 SC-15 的行定义 (含 7h / 11v); 710-1011 (L1 全部 SC 行、SC-25 归一化); 1012-1100 (套件行); 1100-1200 (文档判据); 1425-1531 (main、32c、形态计数)。
  - `baseline-evidence.md`: 1-31 与末尾计数段。
- v1 → v2: `git diff --stat 47aa15f b3e3123 -- openspec/changes/secret-net-l3-and-bypass-paths/`; v1 的相关段经本席 R1 报告对照。
- issue 全文: `aria-plugin-154.md` (含评论 19339)、`aria-plugin-203.md`、`Aria-221.md` (含评论 25898)。
- 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文。
- `CLAUDE.md`: 规则 #6 / #7 / #10、多远程两条硬约束、版本管理段。
- R1: 聚合报告全文 (含「全部 finding」表与「主控记录」); 本席 R1 报告全文。
- 返修材料: `v2-writer-report.md` 全文; `writer-v2-proto/` 下的 `README.md`、`build_full.sh`、`mut_summary.txt` / `mut_summary2.txt` / `mut_summary3.txt`。
- 源码 @ aria `268da8f`:
  - `hooks/secret-guard.sh` 全文 (1-1120); `hooks/hooks.json` 全文。
  - `hooks/tests/secret-guard.test.sh` 1667-1800 (测试内 SC-8 计时闸)。
  - 原型 `secret-guard.sh` 与基线的全文 diff; 原型 `secret-scan.sh` 244-300 (白名单与分类器)。
- 规范:
  - `secret-hygiene.md`: 1-30、§2.2、节目录。
  - `skill-benchmark-exemption.md` 1-100。
  - `version-management.md` §2.2-§2.3。
- 研究笔记: `cc-hooks.md` 全文; `secret-scan.md` 1-80。
- 发版面:
  - `git show --stat`: 主仓 `72cb02b` / `a99dd8d`, aria `26e644e`。
  - VERSION / CLAUDE.md / README.md 的 diff; 主仓 `VERSION` 1-40。
  - `.aria/state-checks.yaml` 的 plugin-cache-currency 条。
  - #199 的 `detailed-tasks.yaml:342` (`guard_config_hooks`)。
- 实跑:
  - 全部在 `scratchpad/audit/post_spec-R2-tech-lead/` 下进行, 用的是 `cp -a` 出的 aria / standards / spec 副本与原型副本, HOME / TMPDIR 指向该目录。
  - 命令只作为字符串喂给 hook 的 stdin, 从不执行; 像凭据的值由 `secrets` 在进程内生成, 不打印。
  - 脚本: `l1cmp.py` + `cases_ps.tsv` / `cases_ps2.tsv` / `cases_appini.tsv` / `cases_env2.tsv` / `cases_rb.tsv`; `l3edge.py`; `perf600.py`; `perfnoext.py`。
  - 探针子集 `WPA_ONLY=SC-7,SC-11,SC-20,SC-21,SC-22,SC-23,SC-24,SC-25` 与 `WPA_ONLY=SC-12,SC-13,SC-19,SC-26,SC-28`, 各在基线副本与原型副本上跑一次。
  - 结果: 基线形态 holds / 原型目标形态 holds, 与 `baseline-evidence.md` 的分组计数一致。
- 收尾: 真仓 `git status` 干净; HEAD `b3e3123`、aria `268da8f`、standards `2bc1c4c` 均未变。

## Findings

### C1 [e8d39a8a] critical · issue · implementation · proposal.md What.W3

**summary**: R1 簇 A 只部分关闭。W3 白名单的两类形态照样作用于既有 `json-secret-field`, 按 W3 字面实现后, 基线能检出的两类真实值会变为静默 (检出回退):

- 第 2 类的裸 `$NAME` (`$` 后为单一大小写字母、数字、下划线);
- 第 5 类的截断标记 (值以 `…` / `...` 结尾)。

已知限制没写这两类, 也没有 SC 钉住; Impact「新静默」那句话对单一大小写子集不成立。

**证据**:
- proposal.md 原文:
  - :82「`$NAME` (NAME 全大写或全小写, 加数字与下划线; **不含混合大小写**)」;
  - :85「截断标记: 值以 `…` 或 `...` 结尾」;
  - :88「**不是**白名单的: 以 `$` 开头的随机值 (`$` 后是混合大小写或夹杂符号) … 作用范围 = 6 个新 tag + 既有 `json-secret-field`」;
  - :95 已知限制只列了四项: FAKE 开头、小写 fake_、尖括号包住、夹带哨兵;
  - :330 Impact「`$` / `<` 开头的随机值与 crypt 口令哈希**不**在内 (仍检出)」。
- 主控裁定 1 (R1 聚合报告「主控记录」): 「`$2b$…` 口令哈希与 `$` / `<` 开头的随机值必须仍被检出」。截断标记这一类不在裁定的列举里, 是 v2 新加的。
- 原型就是 W3 的字面译本 (`secret-scan.sh`): `_RE_VARU='^\$[A-Z_][A-Z0-9_]*$'`、`_RE_VARL='^\$[a-z_][a-z0-9_]*$'`、`[[ "$v" == *"…" || "$v" == *"..." ]] && return 0`。
- 实跑 `l3edge.py`。值在运行时生成, 每例跑 3–4 次。前四行每行依次为「例 | 基线 | 原型」, 后四行逐行标出基线 / 原型。输出原样:
```
json:password=<'$' + 11 lower/digit (human leet form)> | exit=0 alert m=1 {json-secret-field=1} | exit=0 silent
json:password=<20 mixed alnum + '...'> | exit=0 alert m=1 {json-secret-field=1} | exit=0 silent
json:api_key=<32 mixed alnum + '...'> | exit=0 alert m=1 {json-secret-field=1} | exit=0 silent
json:password=<'$' + 20 mixed alnum> (control: must stay detected) | exit=0 alert m=1 {json-secret-field=1} | exit=0 alert m=1 {json-secret-field=1}
json:client_secret=<'$' + lower letter + 23 lower/digit> | base | exit=0 alert m=1 {json-secret-field=1}
json:client_secret=<'$' + lower letter + 23 lower/digit> | proto | exit=0 silent
json:password=<'$' + UPPER letter + 19 UPPER/digit> | base | exit=0 alert m=1 {json-secret-field=1}
json:password=<'$' + UPPER letter + 19 UPPER/digit> | proto | exit=0 silent
```
- 守卫看不见这两类:
  - 7h 的 `dollar20` 用混合大小写生成器 (`baseline_probe.py:198` 的 `_gen_first("$", ALNUM, 20, [LOW, UP, DIG])`, 由 :451 引用);
  - 11v (:531-535) 只有 8 字符的 `$2b$12$…` 与带花括号的 `${DB_PASSWORD}`。

**失败场景**: 实现者照 :82 / :85 实现, 然后读到一份配置 dump, 例如:

- `{"password":"$<字母开头的单一大小写字母数字>"}` (人选口令里用 `$` 代 S 是常见写法);
- `{"api_key":"<真值>..."}`。

基线对两者都告警; 实现后两者都静默, span 还被哨兵吞掉。此时探针目标态仍全 yes, SC-29 仍全绿。这直接违反审计锚点「不引入任何安全回退」。

**三态** (建议在 7h 加两个独立运行, 期望 `json-secret-field=1`):
- 基线: yes (已实测);
- 收窄后的实现: yes;
- 照 W3 字面的实现 (原型): no (已实测)。

**建议修法** (任一即可; 现有 SC 行都不受影响 —— 9l / 9m 是新 tag, 11v 用花括号与 8 字符前缀):
1. 既有 `json-secret-field` 只认带花括号的 `${…}`; 裸 `$NAME` 只作用于 6 个新 tag。
2. 截断标记收窄为「省略号前不超过 16 字符」(仍覆盖 11v), 或只作用于新 tag。
3. 补上述两个反向守卫运行。
4. 若 owner 要保留这两种形态: 写进 W3 已知限制与 Impact「新静默」, 补 known-limit 行, 并改正 :330 的措辞。

### M1 [ac42f607] major · issue · implementation · proposal.md What.W11

**summary**: W11 的包裹文法有三个缺口, 都没有论证:

1. 它的 launcher 集是现有 `secret-guard.sh:873` launcher 集的子集, 少了 `xargs` / `eval` / `unbuffer`;
2. 不接受带参数的选项 (`sudo -u <用户>`) 和绝对路径调用 (`/bin/ps`);
3. `/proc` 放宽行没有纳入 `python3 -c` / `node -e` 源组, 而 W8 / W9 都纳入了。

结果是 `pgrep -f X | xargs ps -fp` 这类自然写法, 在按 Spec 写的原型上照样放行; SC 不测, 已知限制也没写。

**证据**:
- proposal.md:
  - :185 launcher 列表为 `sudo doas nice timeout nohup stdbuf env time setsid ionice watch command exec`;
  - :187 `/proc` 行只补了 `xargs sed grep … cp dd` 等读取器;
  - :193 已知限制不含上述任何一项;
  - SC-22 中 launcher 只有 22n 一行 (`sudo pgrep -af curl`)。
- 源码 `secret-guard.sh:873` 既有 launcher 交替: `(sudo|doas|nice|timeout|xargs|nohup|stdbuf|env|time|eval|setsid|ionice|unbuffer)\b([[:space:]]+-[^[:space:]]*|[[:space:]]+[0-9]+)*`。
- 对照: W8 (:145) 与 W9 (:157) 都纳入了 `python3 -c` / `node -e` 源组 (16h、19o)。
- 实跑 `l1cmp.py`, 每行左为基线、右为原型 (输出原样节选):
```
exit=0 | exit=0 | Bash | 'pgrep curl | xargs ps -fp'
exit=0 | exit=0 | Bash | 'pgrep -f curl | xargs ps -o pid,args -p'
exit=0 | exit=0 | Bash | 'eval ps aux'
exit=0 | exit=0 | Bash | 'unbuffer ps aux'
exit=0 | exit=0 | Bash | 'sudo -u forgejo ps -ef'
exit=0 | exit=0 | Bash | '/bin/ps aux'
exit=0 | exit=0 | Bash | '/usr/bin/ps -ef'
exit=0 | exit=0 | Bash | 'python3 -c "print(open(\'/proc/1/environ\').read())"'
exit=0 | exit=0 | Bash | 'node -e "console.log(require(\'fs\').readFileSync(\'/proc/1/environ\',\'utf8\'))"'
exit=0 | exit=0 | Bash | 'find /proc -maxdepth 2 -name environ -exec cat {} +'
对照 (exit=0 | exit=2): 'ps -fp $(pgrep curl)' ; 'nice ps aux' ; 'timeout 5 ps aux' ; 'sudo -E ps aux'
```

**失败场景**:
1. 实现者照 :185 / :187 的清单写规则。
2. 10CG/Aria#221 的场景是「想看看后台在跑什么」。这时常见的写法 `pgrep -f curl | xargs ps -fp`、`sudo -u <服务用户> ps -ef` 都被 L1 放行, 后台 curl 带的 `Authorization` / `CF-Access-Client-Secret` 进入会话。
3. L3 只能事后告警; 对 `--token <值>` 这种空格分隔形, L3 本身就是 KNOWN-LIMIT (SC-10 10e)。
4. Impact :342 写着「10CG/Aria#221 部分覆盖 (进程表列举已做)」, owner 与采用方会以为这些形态已被覆盖。

**三态** (建议加 baseline-failing 行: 上面前九条, 期望 exit 2):
- 基线: no (行就是这样设计的);
- 补齐文法的实现: yes;
- 照 Spec 字面的实现 (原型): no (已实测)。

**建议修法**:
1. launcher 集取 `:873` 的集合, 再并上 `watch command exec`。
2. 至少让 `sudo` / `doas` 接受 `-u <用户>` / `-g <组>`。
3. 允许可选的 `(/usr)?/bin/` 前缀。
4. `/proc` 的 `environ|cmdline` 行并入 `python3 -c` / `node -e` (以及 `find … -exec cat`)。

以上都是 W11 自己的族, 不扩大范围。若有意不纳入, 就逐项写进 W11 已知限制, 加 known-limit 行, 并列入 7.10。

### M2 [ce6fc59c] major · issue · testing · proposal.md Tasks

**summary**: Tasks 1.10 的 post-ship 腿有两处缺口:

1. **不经 harness 验 Read 路径。** W1 修的恰是只有端到端才看得见的形状错配; 而 Impact 把 10CG/aria-plugin#154 的关单条件写成「Read 提取修复…经 post-ship 端到端复验之后」。照 Tasks 字面执行, 会在 Read 从未经 harness 验证的情况下关单。
2. **用真实的危险命令验 L1 拦截** (`ps aux`、读 `/etc/forgejo/app.ini`)。插件缓存 STALE 或超时放行时, 真实的 argv / 配置值会进入会话; 而本仓发版后缓存 STALE 是常态。

**证据**:
- proposal.md:
  - :355 (Tasks 1.10): post-ship 腿 =「用一条 Bash 命令打印运行时生成的合成值 (… 不写任何文件 …)」+「再对 `ps aux` 与 `/etc/forgejo/app.ini` 的读取各验一次拦截」; 它的回退口径自己列了「超时放行」。
  - :340: 10CG/aria-plugin#154「Read 提取修复落地并**经 post-ship 端到端复验 (Tasks 1.10) 之后**, 才按一次性授权评论并关闭」。
  - :306: rule6_note 的 dogfood 也落在这条腿上。
  - :21:「生产中 Read 从未被扫描, 现有 Read 用例用合成形状所以一直绿」。
- 研究笔记 `secret-scan.md:60`:「同一份 `toolUseResult` 与 hook 入参 `tool_response` 同源是**推测**」。SC-1 的 `read_real` 信封 (`baseline_probe.py:249-252`) 正是按这个推测构造的。
- 缓存 STALE 是常态:
  - `72cb02b` 与 `a99dd8d` 的提交说明都写着「plugin-cache-currency 预期 STALE (本机插件缓存待更新)」;
  - `.aria/state-checks.yaml:317-336` 记有 Aria#172 的实例: 缓存停在 1.63.0 而 SOT 已是 1.65.5, 原文「仓内一切 hook/skill dogfood 验收失真」。
- 存在一个无写入、无泄露的 Read 金丝雀: 把 SC-33 归因清单里的公开示例文件 `aria/skills/requesting-code-review/examples/no-plan-fallback.md` 按真实 Read 信封喂 hook (本人实测):
  - 基线: `silent`;
  - 原型: `Detected 1 secret-shape match(es) (kv-secret-assign=1)`, additionalContext 含 `(tags: kv-secret-assign=1; source: Read …)`。

**失败场景**:
1. 缺口 1: Bash 合成值在基线上就会告警, 两个拦截也照常生效, post-ship 腿全过。于是按 :340 关闭 10CG/aria-plugin#154, 并宣告「Read 已端到端复验」—— 但 harness 送来的 Read 入参一次也没被测过。若真实入参与 transcript 的形状不同, 生产中 Read 继续失明, 而单已经关了。
2. 缺口 2: ship 当时缓存仍是 v1.74.1 (常态), 于是 `ps aux` 被放行并执行, 后台进程的 argv 进入会话。这正是 10CG/Aria#221 的场景: CI 轮询用的 curl 带着 CF Access 与 PAT 头。若有人为了「贴近真实」去 PVE 上复现 (`ssh root@pve 'pct exec 101 -- cat /etc/forgejo/app.ini'`), 事故里那份 `JWT_SECRET` 会再泄一次。

两种后果都不可撤回。

**建议修法**:
1. post-ship 腿加一条 Read 腿: Read 上述归因文件, 期望 L3 告警且 additionalContext 含 `source: Read`; 10CG/aria-plugin#154 的关单以它为前提。
2. 加前置条件: `plugin-cache-currency` 报告为当前版本, 才开始这条腿; STALE 时记「未生效」, 不得关单。
3. 拦截探针一律改成不泄露的形态, 如 `ps aux | head -c 0`、`cat /etc/forgejo/app.ini | head -c 0`。新 hook 下 tight credit 不认 `head`, 照样拦截; 旧 hook 下会放行, 但什么也不打印。同时写明不得在真实主机上复现。

### m1 [c9357eb5] minor · issue · testing · proposal.md SC-30

**summary**: W14 (h) 档「< 5 s」这条绝对上界会随主机负载漂移。本机负载 4–10 时, 基线自己跑 600 段整进程就要 7.15 s, 因此该档会在与实现无关的条件下转红。

- 测试内 SC-8 的 owner 裁定, 正是为防这类恒红才设计成「绝对腿 + 相对腿取宽」; (h) 反过来取 AND, 也没有退路。
- 另外, hooks.json 的 5 s 超时作用于整个进程, 而 (h) 沿用的是只计判定段的进程内计时器。

**证据**:
- proposal.md:225 (h) 的定义; :286 SC-30。
- `secret-guard.test.sh:1678-1691`: 判据与双腿设计的理由。
- 实跑 `perf600.py` (整进程墙钟, 每格取 3 次中的最小值; 输出原样):
```
3.94 6.46 8.61 1/1171 3591176
segments=600 | base exit=2 7.15s | proto exit=2 8.78s
segments=700 | base exit=2 7.26s | proto exit=2 8.34s
segments=800 | base exit=2 9.40s | proto exit=2 13.09s
loadavg: 10.84 7.21 8.38 16/1208 3634539
```

**三态**:
- 安静主机: 基线约 3.8 s, yes; 好实现约 4.4 s, yes; 按段交错的坏实现, no。
- 负载主机: 三者都是 no, 没有鉴别力。

**建议修法**:
1. 闸只保留相对腿: 同场测量, 不超过改前 × 1.5。
2. 「< 5 s」改为附带 loadavg 的记录项; 或换成「5 s 内能判完的最大段数, 下降不得超过 X%」。
3. 写明基线自身已 ≥ 5 s 时怎么处置: 记录并上报, 不判红。

### m2 [d65a895f] minor · issue · architecture · proposal.md What.W9

**summary**: W9 有两条字面上不可兼得的要求:

- 扩展的全部代码 (含项目根解析) 只能经 `$( … )` 调用;
- 无扩展文件时, 不 fork 任何子进程。

bash 5.2 及以前的命令替换必然 fork, 所以两者不能同时满足。

- 原型选了前者: 即使没有扩展文件, 每次 Bash / Read 调用也多 1 次 exec 和若干子 shell。
- 若实现者为满足后者, 把存在性预检放进主 shell, 那段代码就落在 `_sg_ext_*` 故障注入 (20i–20k) 的范围之外, 重新打开 C2 那一类故障面。

**证据**:
- proposal.md:158:「无扩展文件时 (项目根下没有该文件) 不 fork 任何子进程 (`[[ -f ]]` 是 builtin)」。
- proposal.md:159:「扩展的全部代码 —— 项目根解析 … —— 只经命令替换 `$( … )` 调用」。
- 实跑 `perfnoext.py` (用 PATH 垫片计外部 exec; 不设 `CLAUDE_PROJECT_DIR`, 也无 cwd 字段):
```
Bash ls -la | base | exit=0 | external execs=5 (cat,grep,jq,tr)
Bash ls -la | proto | exit=0 | external execs=6 (cat,grep,jq,tr)
Read /x/README.md | base | exit=0 | external execs=5 (cat,grep,jq,tr)
Read /x/README.md | proto | exit=0 | external execs=6 (cat,grep,jq,tr)
```
- 负载约 10 时墙钟数字无法解读。Windows Git-Bash 上的 fork 代价未测, 而 10CG/aria-plugin#203 的报告者用的正是 MINGW64。

**建议修法**: 二选一:
1. 删去「零 fork」断言, 并为 Read/Edit 的无扩展路径补一个时档;
2. 明文允许主 shell 里有一行纯 builtin、用 `${…:-}` 默认值的存在性预检, 并把这一行纳入故障注入。

### m3 [684e9a24] minor · issue · documentation · proposal.md What.W9

**summary**: W9 Bash 面的语义写的是「且其**每一处出现**之前…有一个读取器 … 则按 tight credit 判」, 可以读作全称: 每一处之前都有读取器才判。19r 要求的却是「任一处」: 第一处在非读取器之后、第二处在读取器之后, 结果应为 exit 2。措辞与 SC 方向相反, 目前全靠 19r 兜住。

**证据**: proposal.md:157; SC-19 19r (:272); `baseline_probe.py` 的 19r 行 `echo P; cat P` → 2。

**建议修法**: 改为「对每一处出现分别判断; 任一处在同一管道阶段内前面有读取器, 即按 tight credit 判」。

### m4 [c941e4e1] minor · issue · implementation · proposal.md What.W8

**summary**: W8 的 `app.ini` 读取器组沿用 claude-config 行 (Aria#179) 的打印型集合, 比既有 `.env` 家族窄。`dd if=`、`<` 重定向读取、`cp … /dev/stdout`、`perl -ne`、`tee <` 在原型上都放行, W8 的已知限制没有列出。

**证据**:
- proposal.md:145 / :149。
- 源码中 `.env` 家族的对应行: `secret-guard.sh:828` (`dd if=`)、`:833` (`perl -ne`)、`:836` (`tee <`)、`:839` (`while … <`)、`:841` (`cp … /dev/stdout`)、`:909` (`$(< …)`)。
- 实跑, 每行左为基线、右为原型:
```
exit=0 | exit=0 | Bash | 'dd if=/etc/forgejo/app.ini'
exit=0 | exit=0 | Bash | 'while IFS= read -r l; do echo "$l"; done < /etc/forgejo/app.ini'
exit=0 | exit=0 | Bash | 'echo "$(< /etc/forgejo/app.ini)"'
exit=0 | exit=0 | Bash | 'cp /etc/forgejo/app.ini /dev/stdout'
exit=0 | exit=0 | Bash | 'perl -ne print /etc/forgejo/app.ini'
exit=0 | exit=0 | Bash | 'tee < /etc/forgejo/app.ini'
```

**建议修法**: 写进 W8 已知限制并补一行 known-limit; 或与 `.env` 家族的读取器对齐。

### m5 [0033f2f4] minor · issue · documentation · proposal.md 待 owner 复议

**summary**: 同族扫描漏列了几条既有的整环境 / 进程环境旁路。它们在基线与原型上都放行, 不是本 Spec 引入的, 但建议开单清单第 10 条也没有收录:

- `export -p`、`declare -x` / `-p`、`typeset -x`、裸 `set` —— 其中 `set` 在 SOT `secret-hygiene.md:96` 被明列为受限命令;
- `env -0` / `env -u X` / `env --null`, 包括新包裹下的 `nomad alloc exec … env -0` 与 `docker exec … env -0`;
- `systemctl show -p Environment`、`systemctl cat`;
- `kubectl get pod -o yaml|json`。

**证据**: 实跑上列各式均为 `exit=0 | exit=0` (基线 | 原型)。对照: `kubectl exec pod -- env -0` 为 `exit=2 | exit=2`。

**建议修法**: 并入 7.10, 不改代码。

### m6 [5d032f7a] minor · issue · documentation · proposal.md What.W13

**summary**: 层次术语对不上:

- Spec 用 10CG/aria-plugin#154 的 L1 / L2 / L3 编号来叙述两层分工;
- 而 W13 / W9 要写入的 SOT `secret-hygiene.md` 自有一套「Path 1–3 / Layer 0 / Layer 2」, 并明文写着「Why no Layer 1」。

Spec 没有给出落 SOT 时的术语映射。实现者若把「L1 / L3」写进 §2.5 / §3.8 / §5.6, 就会与 §0 自相矛盾。

**证据**: `secret-hygiene.md:15-29` (§0 的表, 以及 :27「Why no "Layer 1"?」); proposal.md:214-216 (W13 落 SOT 的条目)、:163 (W9 的 §5.6)。

**建议修法**: 二选一:
1. 写明「SOT 内沿用 Path 3 / Layer 2 (PreToolUse / PostToolUse) 术语, 不引入 L1/L3」;
2. 在 §0 补一行映射。

## 上一轮对账

按主控记录的归并簇逐条对账, 覆盖全部 30 个 Critical + Major 键:

| 簇 | 键 | 状态 | 本人核验的证据 |
|---|---|---|---|
| A | `e8d39a8a` · `14b7e703` · `8645b99f` | **partially closed** | 首字符规则已改为整值形态。原型上 7h 的 crypt60 / dollar20 / lt16-unclosed 均告警, 7i 也告警 (本人探针子集 SC-7 9/9)。残余两类见 C1, 沿用 `e8d39a8a` |
| B | `e600e931` · `179045cd` · `f42265a1` | closed | :200 只归一化四个单键读取子串; 23c 的十条整表导出与 printenv 在基线与原型上均 exit 2 (本人跑原型 SC-23 8/8); `nomad alloc exec … python3 -c "…print(os.environ)"` 两边均 2。`os.environ['X']` 放行已写进 :202 与 Impact :329 |
| B2 | `d9308fba` · `ab6a3123` | closed | 23d 的九条 (含 `.env_prod` / `.env2` / `.envprod` / `.envs/`) 在原型上均 exit 2; 23g 钉住现状 |
| C | `7e0343bd` | closed | :159 规定扩展代码全部只经 `$( )` 调用。本人复跑 20i / 20j / 20k, 原型上均为 `exit=2,0,2,0,2`; 20l 为 `calls=none`; writer 的变异 ext_bare 使 20i / 20j 转红 |
| C2 | `d4bcaf7c` · `d8e7b380` | closed | 求值顺序由 20l / 20m / 21v / 21w 钉住 (本人在原型上复跑全 yes), 并新增 (f)(g)(h) 三档。残余见 m1 (h 档受负载支配) 与 m2 (无扩展也 fork) |
| C3 | `719ae05c` | closed | 19j (14 个元字符条目) / 19k / 20h 原型 yes、基线 no; writer 的变异 ext_regex 使 19j / 20h 转红 |
| C4 | `53c140c4` · `27f6c3ce` · `b73ab606` | closed | SC-26c / e / f / g 按小节判定 (`baseline_probe.py:1122-1200`), 原型 SC-26 8/8、基线 1/8; 五向行为变更申报见 Impact :326-332 |
| D | `634eac5c` · `2ce0049b` | closed | W4 有逐 tag 取值表 (:102-112); SC-12 原型 10/10、基线 3/10 |
| E | `44b5bb44` | closed | 新增真 bash 3.2 差分腿 32c 与 29h / 29i; 32a 扩到 13 类构造 (:288); writer 的变异 b4 使 32a / 32c 转红。附带条件见下节 §6 第 6 条 |
| F | `e2459206` · `9db51a43` | closed | 22ao–22ar、22at、22as / 22aj 齐全 (本人跑原型 SC-22 51/51, 基线 10/51)。带选项的 `env -0` / `env -u` 仍放行, 属既有缺口, 见 m5 |
| G | `846b21f8` | closed | §3.8 限定为长时进程; 26h 钉住 §3.1–§3.7、§4.1–§4.4 逐字节不变 |
| H | `7deac83f` · `2779a016` · `ba98e41f` | closed | :341 默认理解 B。版本点已核: `72cb02b` / `a99dd8d` 各 16 个版本点, aria `26e644e` 恰好改 6 个文件; Tasks 1.11 承载 |
| I | `cf0ae932` | closed | 四份研究笔记已入仓 (`git ls-files` 可见), 引用已改指仓内路径 (:9) |
| J | `d9986b27` · `5831f8c0` · `1c0bc16f` · `a3054a20` · `8e77d1ca` | closed | 13d 改为全串等值 (原型 SC-13 6/6, 变异 w5_append 转红); SC-26 按小节判定; 7h 拆成七个独立运行; 新增强制首字符生成器 `_gen_first`; SC-33 有固定 SHA 与归因清单 (语料普查本人未复跑, 依据 writer 的 noentropy 变异结果) |

上一轮的 minor 中, 本人认为仍未处置的: 无。本席 R1 的 m1–m8 都已落进 v2, 依次见 :191、:149 与 :169、:325 与 :335、:102-112、:157、:162 与 :402、:228, 以及 SC-26 改为按小节判定。

## 对执笔人自报薄弱点与请裁项的表态

**§5 自报薄弱点**

1. **文字体量未收紧 (+44%)** —— 可接受。本轮不建议再削: 削减本身会造出新接缝; 收敛看的是判据强度, 不是字节数。
2. **交付形态偏离 (三份文件按母本路径交付)** —— 可接受。主控已按 MANIFEST 校验, 并逐字节复跑过。
3. **原型不是实现** —— 可接受, 但补一个实例。原型 Read 面的 `app.ini` 正则缺右边界: Read `/etc/forgejo/app.inix` 在原型上 exit 2, 而 Bash `cat` 同一路径 exit 0。这违反 :144 的「单一定义、两处消费」; SC-18 又没有 Read 面的边界行, 所以探针看不见。实现者不得照抄原型。
4. **「变异实测」声称已更正 5 处, 但仍有研究笔记里的数字没复跑** —— 可接受。这些数字已标出处, 不承重。
5. **12j 未经独立 review** —— 可接受。由 Tasks 1.8 的非作者 review 覆盖。
6. **bash 3.2 腿默认不开** —— 有条件可接受。现在「target shape (every row 'yes')」的计数会跳过 n/a 行 (`baseline_probe.py:1498-1519`), 所以不带 `WPA_BASH32` 跑、或以 root 身份跑 (20g 不可构造) 时, 它照样打印 holds。条件是改为: 只要存在 n/a 或 not-run 行, 就输出 does not hold, 或附上未运行行的清单。
7. **性能数字噪声大** —— 作为自报可接受; 实测结论见 m1。
8. **25 个坏实现都由作者构造** —— 可接受。Tasks 1.8 要求由非作者构造。
9. **SC-33 归因清单写死了两个路径** —— 可接受。而且其中一个文件恰好可以作 M2 建议的 post-ship Read 金丝雀。
10. **W9 静默失效是产品取舍** —— 可接受列入复议, 见 §6 第 3 条。
11. **Windows / macOS 未实测** —— 作为已声明的限制可接受。但 W9 正是 MINGW64 报告者要的入口, 且失效是静默的。建议在 §5.6 写明「Windows 下项目根形态未验证」, 并在 B.2 记录一次 `CLAUDE_PROJECT_DIR` 的实值形态。
12. **探针自身的并发竞态** —— 可接受。探针已改为每个套件用私有 `USER`, 套件本身的缺陷已列入 7.18。

**§6 请裁项**

1. **rule6_note 块 A 取 `n/a`** —— 可接受。SOT §4.1 把 `n/a` 定义为「不属 Skill 变更」, :306 也写明这是分类而非免验。
2. **文字体量是否再削** —— 不削, 理由同 §5 第 1 条。
3. **W9 静默失效** —— 默认 A 可接受, 但建议改分类。它决定的是采用方能否得知自己配置的安全清单已经失效, 属于用户可见的产品行为, 应从「技术级 (已裁)」第 18 条移到产品级「请裁」。主控裁定 3(e) 把它交给执笔论证, 并不改变它的性质。
4. **10CG/aria-plugin#203 / 10CG/Aria#221 的评论口径** —— 可接受理解 B。本席 R1 曾接受理解 A, 现依主控裁定与决策单字面改为 B: 评论不可撤回, 含糊的授权不构成放行。
5. **SC-33 是否改写 `no-plan-fallback.md`** —— 不改, 只归因, 可接受; 改它会牵动 Rule #6。
6. **未带 `WPA_BASH32` 时取 n/a 还是失败** —— 逐行保持 `n/a`, 以保住基线可复现; 但目标态判定行必须把 n/a 视为「未完成」, 见 §5 第 6 条。
7. **原型与脚本是否归档** —— 可接受现状: 脚本与汇总已入仓 `writer-v2-proto/`, 树副本不入仓。
8. **交付形态** —— 可接受。

## 风险 / 疑问

- **BusyBox / macOS 的 `ps`**: 在 Alpine 容器里 (如 `docker exec <alpine 容器> ps`) 和 macOS 上, 裸 `ps` 的默认输出含完整命令行; 而 W11 按 Linux procps 语义放行裸 `ps`。本机没有 busybox / docker, 未能实测。
- **超时即放行比 Spec 写的更紧** (对应建议开单第 1 条): 本机负载 4–10 时, 基线 600 段就要 7.15 s。也就是说今天在负载下, 几百段的长命令就会被超时放行。W8 / W11 新增的行又增加了 15–39% (同场实测, 噪声大)。建议在 ship 前把它作为已知风险告知 owner。
- **规模与 Level**: proposal 加探针合计约 210 KB。W10 在热路径上加了第二遍判定, 而 10CG/aria-plugin#203 的报告者自己说第 2 类「在命令侧基本堵不住」, 应交给 L3。本席不建议拆分 Spec (拆分会自造接缝), 但 owner 复议第 4 条时宜知道这一成本。
- **两处上限的方向没写明**: W9 的「命中点最多检查 64 处」、W10 的「最多 16 个赋值」, 超过上限后是放行还是拦截, Spec 没写; 按「扩展失败只丢扩展」推测是放行。在防意外的威胁模型下影响小。
- **新误拦叠加冻结文案, 会诱发 ack 疲劳**:
  - W11 会新增误拦, 本人实测 `ps aux | grep X`、`ps -ef | grep [c]url` 等都被拦;
  - W13 又冻结了 BLOCKED 文案, 文案里的 Acceptable filters 对 tight 族无效;
  - 结果是被拦时 AI 手里没有可用的替代提示, 容易转向 `# guard:ack` —— 这正是 10CG/Aria#221 评论 25898 警告的「ack 疲劳」。
  - owner 裁第 2 条 (文案) 与第 5 条 (习惯改变) 时宜合并考虑; 选项 C 能同时解决两者。
- **本席自身的操作**: 全程未读取或打印任何真实凭据; 本席的工具输出中未见 L3 告警。

## Verdict

- verdict: **FAIL**
- counts: **1C / 2M / 6m**
- **Vote: REVISE**

## 是否足以进入 A.2

**不足以。** 理由有三:

1. C1 是照 W3 字面实现就会出现的检出回退, 违反审计锚点「不引入任何安全回退」;
2. M2 使 10CG/aria-plugin#154 的关单前提无法由 Tasks 兑现, 并在验证步骤里留下泄密口;
3. M1 是 W11 包裹文法的缺口。

这三处都要先改 Spec 与对应的 SC 行, task-planner 才有稳定的输入。
