---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-06T15:19:51.095Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- 被审对象 (`c0a6654`):
  - `proposal.md` 全文 (1-425)。
  - `baseline_probe.py`: 960-1035 (SC-12 尾段与 SC-13, 含 13d / 13g), 1495-1590 (套件执行、SC-14、SC-29), 2040-2095 (汇总、形态行、`WPA_REQUIRE_ALL` 退出码); 其余行经 grep 定位 (`:25` / `:77` / `:117-118` / `:1249` / `:1518-1519`)。
  - `baseline-evidence.md`: 1-60; SC-7 / SC-9 / SC-11 / SC-19 至 SC-22 各行; 末尾计数段。
  - v2 → v3: `git diff --stat b3e3123 c0a6654`; v2 proposal 的 Tasks 节 (`git show b3e3123:…`)。
- 三个 issue 全文与全部评论 (10CG/aria-plugin#154 含评论 19339; 10CG/aria-plugin#203; 10CG/Aria#221 含评论 25898)。
- 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文。
- `CLAUDE.md`: 规则 #6 / #7 / #10、多远程推送两条硬约束、版本管理段。
- R2: 聚合报告全文 (全部 finding 表、收敛计算、主控记录); 本席 R2 报告全文。
- 返修报告 `v3-writer-report.md` 全文。
- 源码 @ aria `268da8f`: `hooks/secret-scan.sh` 全文 (1-377); `hooks/secret-guard.sh` 1-140、380-1120; `hooks/hooks.json` 全文; `hooks/tests/secret-guard.test.sh` `:11` / `:841` / `:1620-1622`; `hooks/tests/secret-scan.test.sh` 的 HOME 相关行; `.github/secret_scanning.yml:18-22`。
- 规范 @ standards `2bc1c4c`: `secret-hygiene.md` 1-30、277-300、397-420 与节目录; `skill-benchmark-exemption.md` 12-86。
- 研究笔记: `cc-hooks.md` 全文; `secret-scan.md` 1-130。
- 接缝与流程: 10CG/Aria#199 的 `detailed-tasks.yaml:342` (`guard_config_hooks`) 与其 proposal 头部; `.aria/probes/plugin-cache-currency.py` 全文; `.aria/state-checks.yaml` 的 plugin-cache-currency 条 (317-338); state-scanner `custom_checks.py` 状态取值; `release_gate.py` 头注释。
- 归档 `writer-v3-proto/`: `README.md`、`build_full.sh`、`runprobe.sh`、`refs_check.py`、`timing_summary.txt`。
- 实跑 (全部在 `scratchpad/audit/post_spec-R3-tech-lead/` 下, HOME / TMPDIR 指向该目录; 命令只作字符串喂 hook、从不执行; 像凭据的值在进程内由 `secrets` 生成、不打印):
  - 用仓内归档脚本 (只改 `EXP` 路径) 重建目标态原型 `t3`: 两个 hook、两个套件、aria README、SOT 与执笔的树逐字节相同。
  - 完整目标态探针 (真 bash 3.2 + `WPA_REQUIRE_ALL=1`): rc 0, 72649 字节, sha256 前 16 位 `0e1d2eb9ea1522fb`, 与执笔的运行 T 逐字节相同; 382 行全 yes, 30a 按设计 n/a, 目标形态 holds。
  - 对照脚本 `l3cmp.py` (用例 `cases_l3_a.py` / `cases_l3_nul.py`) 与 `l1cmp.py` (用例 `cases_l1_k.tsv` / `cases_ext0.tsv`)。
  - 非作者构造的坏实现: `mU` (W11 launcher 集删 `unbuffer`)、`mA` (W3 尖括号分支允许内部定界符)、`mE` / `mE2` (扩展条目经 `printf '%s\n'` 喂 `grep -f`); 修法验证变体 `t3nul`。
  - 平台事实 (本会话, 合成良性内容): Read 工具读 procfs; Read / Bash 工具对 NUL 字节的处理; `pgrep -fl` 与 `-af`; `ps -o '%p %a'` (只对本 shell)。
  - `refs_check.py`; 对本分支实跑 Impact 的关键字机械检查; `git ls-remote` 查 aria 两端。
  - 收尾: 真仓 `git status` 干净, HEAD `c0a6654`, aria `268da8f`, standards `2bc1c4c` 均未变; 未做任何 git 写操作。

## Findings

### M1 [4f713847] major · issue · architecture · proposal.md What.W1

**summary**: L3 对 NUL 分隔的内容结构性失明。提取链 `content="$( … jq -r … )"` 的命令替换会丢弃 NUL 字节, 把一条条 `KEY=value` 记录首尾粘连; 新旧键形 tag 的左边界与行首锚因此都锚不上。而进程环境的标准形态 (`/proc/<pid>/environ`、`env -0`) 恰好是 NUL 分隔, 结果是两条路径在基线与目标态都两层皆盲:

- Read 工具读 `/proc/<pid>/environ`: L1 Read 面放行 (22au);
- `env -0`: L1 放行 (7.10)。

Spec 没有意识到这一点:

- 22au 把「两层都不拦」只归因于 Read 面与 Bash 面名单不对齐;
- W1 的设计取舍与已知限制都没提 NUL;
- 也没考虑在 W1 正在改的同一条管道里加一段 NUL→换行。

**证据**:
- 源码与 Spec 原文:
  - `secret-scan.sh:135-142`: 内容经 `$( … jq -r … )` 取得;
  - `secret-scan.sh:224`: `env-line-secret-keyword` 锚行首 `^`;
  - proposal `:62`: `kv-secret-assign`「左侧为行首或非词字符」;
  - `:53`: W1「选 A 只加 `file.content` 一个分支」;
  - `:54`: 已知限制只列 Edit / MultiEdit、字符串形、notebook / PDF / 图片;
  - `:196`: 同族纳入 `/proc/*/environ`;
  - `:197`:「Read 工具读 `/proc/<pid>/cmdline|environ` 两层都不拦 (22au; Read 面名单与 Bash 面名单不对齐是既有问题…)」;
  - `:338`: Impact「Read 工具结果首次被扫描」;
  - `:400`: 7.10 只记 `env -0` 在 L1 放行。
- 实跑 L3 (三条凭据变量的 environ 形内容, 值运行时生成; 列依次为基线 | 原型 `t3` [| `t3nul`]; 输出原样节选):
```
  N1 NUL-separated environ (3 credential vars) via Read | exit=0 silent | exit=0 silent
  N2 NUL-separated environ (3 credential vars) via Bash stdout | exit=0 silent | exit=0 silent
  N3 same, newline-separated, via Read (control) | exit=0 silent | exit=0 alert m=3 {env-line-secret-keyword=3}
N1 NUL-separated environ via Read  [base | t3 | t3nul] | exit=0 silent | exit=0 silent | exit=0 alert m=3 {env-line-secret-keyword=3}
N2 NUL-separated environ via Bash  [base | t3 | t3nul] | exit=0 silent | exit=0 silent | exit=0 alert m=3 {env-line-secret-keyword=3}
```
- `t3nul` = 原型只在提取的命令替换内追加一段 NUL→换行 (`diff`: `< ' 2>/dev/null)"` / `> ' 2>/dev/null | tr '\000' '\n')"`)。对它的核验:
  - secret-scan 套件 `PASS: 50 / 50` (`t3` 同);
  - `jq-crlf-guard: clean (2 files scanned)`;
  - 探针 L3 全部行 (SC-1 至 SC-13、SC-15、SC-33) 154/154 yes, SC-33 `flagged=2` 均在归因清单内。
- 实跑 L1 (基线 | 目标):
```
exit=0 | exit=0 | B | 'env -0'
exit=0 | exit=0 | B | 'nomad alloc exec -task server abc123 env -0'
exit=0 | exit=0 | B | 'docker exec web env -0'
exit=0 | exit=0 | R | '/proc/1234/environ'
exit=0 | exit=0 | R | '/proc/self/environ'
```
- 平台事实 (本会话实测):
  - Read 工具能读 procfs 文件 (`/proc/version` 正常返回);
  - Read 一个 NUL 分隔的合成文件, 模型面 tool_result 保留 NUL: `nul= 3 '1\tALPHA_VAR=one\x00BETA_VAR=two\x00GAMMA_VAR=three\x00'`;
  - Bash 输出同样保留: `nul_count= 3 'NULPROBE_A=1\x00NULPROBE_B=2\x00NULPROBE_C=3\x00'`。
  - 即这两条路径确实会把整份进程环境送进上下文。

**失败场景**:
1. 实现者照 W1 字面, 只加 `.tool_response.file.content`。
2. AI 想确认后台服务的配置: Bash 面 `cat /proc/<pid>/environ` 已被拦, Read 是自然的下一个工具。或者它直接跑 `env -0`。
3. L1 放行。含 DB 口令 / token 的整份环境进入上下文, L3 静默。
4. 383 行验收全绿, Impact 宣称 Read 已被扫描; owner 以为进程环境族已由「Bash 面拦截 + L3 兜底」覆盖。

**三态** (建议新增行, 如 SC-1 1c: Read 真实信封, `file.content` 为 NUL 分隔的三条 `KEY=<值>`, 期望 `env-line-secret-keyword=3`; Bash 信封同形一行):
- 基线: no;
- 照 Spec 字面的目标 (原型 `t3`): no —— 这正是缺口;
- 加修法 (`t3nul`): yes;
- 坏实现 (缺修法): no。

**建议修法**:
1. W1 提取管道在命令替换内追加一段 NUL→换行。只改内部扫描缓冲, 与既有 `# crlf-ok` 同性质, 已验证零回归。
2. 补上述 SC 行。
3. 22au 与 7.10 文案如实写明 L3 一侧的原因。
4. 可选: Read/Edit 面 `:641` 追加 `/proc/<pid>/(task/<tid>/)?(environ|cmdline)$` (W8 已在改同一行); 不做则明确并入 7.5。

### m1 [cfb2fb14] minor · issue · testing · proposal.md Tasks

**summary**: Tasks 1.12 的执行条件写的是「`python3 .aria/probes/plugin-cache-currency.py` 报 `PASS`」, 但探针从不输出 `PASS`:

- 相等时输出的是 `OK installed=… sot=…`, 退出码 0;
- `PASS` 只是 docstring 里的状态名;
- `##SKIP##` 的退出码同样是 0。

**证据**:
- proposal `:370`;
- 探针 `:19` (docstring「== SOT → PASS」)、`:127` `print(f"OK {detail}")`、`:42-44` (`_skip` 打印 `##SKIP## …` 并 `return 0`);
- state-scanner 的 custom check 把「退出码 0 且非 skip」记为小写 `pass`。

**失败场景**:
- 照字面执行: 永远等不到 `PASS` → 记「未生效」并停下 → 1.13 (10CG/aria-plugin#154 关单) 与 D.2 归档都卡住。
- 改按退出码判断: `##SKIP##` 会被当成通过。后续四腿自带新旧 hook 的鉴别, 不至于误关单, 所以定 minor。

**建议**: 写成「stdout 首行以 `OK ` 开头且退出码 0 = 通过; 首行以 `##SKIP##` 开头或退出码非 0 = 未生效」。

### m2 [6ff1d962] minor · issue · documentation · proposal.md What.W11

**summary**: W11 的同族扫描漏列了几种会打印完整 argv 的进程列举写法:

- 本地 `systemd-cgls` —— 基线 `secret-guard.sh:850` 已把 ssh 包裹下的它视为暴露;
- `pidstat -l`;
- `w`;
- 宿主上的 `busybox ps`;
- AIX 格式描述符 `ps -o '%p %a'` —— 第 4 类只认 `args|cmd|command`。

它们在基线与目标都放行, 但没有写进 W11 已知限制、22bh 或 7.10。

**证据**:
- 实跑 L1 (基线 | 目标):
```
exit=0 | exit=0 | B | 'systemd-cgls'
exit=0 | exit=0 | B | 'busybox ps'
exit=0 | exit=0 | B | 'pidstat -l 1 1'
exit=0 | exit=0 | B | 'w'
exit=0 | exit=0 | B | "ps -eo '%p %a'"
```
- `ps -o '%p %a' -p $$` (只对本 shell) 实测输出 `PID COMMAND` 列, 内容为完整命令行 (`/bin/bash -c source …`)。
- man 原文:
  - `w`:「the command line of their current process」;
  - `pidstat`:「-l Display the process command name and all its arguments」;
  - `systemd-cgls`:「-l, --full Do not ellipsize process tree members」。
- proposal 全文 grep 计数: `cgls` 0、`pidstat` 0、`busybox` 0 (`BusyBox` 只在容器内裸 `ps` 一处)、`%a` 0。

**失败场景**:
- 实现者照 W11 的清单实现, 这几种写法照样放行, 也没有任何 known-limit 行钉住现状。
- Impact `:353`「10CG/Aria#221 部分覆盖 (进程表列举已做)」在 owner 读来比实际更完整。

**建议**: 列入 22bh 与 7.10 (不必改代码)。`systemd-cgls` 二选一: 与 `:850` 对齐 (本地也拦), 或写明为何只拦 ssh 包裹形。

## 上一轮对账

按主控记录的七簇逐条对账 (R2 的 Critical + Major 全部归入这七个定稿键):

| 簇 | 定稿键 (含映射) | 状态 | 本席核验的证据 |
|---|---|---|---|
| A | `e8d39a8a` (critical; 含 `fc97f926`) | closed | :89 删除裸 `$NAME` / `$(…)` / ASCII `...` 三类; 原型 `_wl_match` 无这三个分支。本席 L3 对照: R2 本席 C1 的 7 种形态 (A1–A7, 每种 2–3 次运行) 基线与目标全为 `alert m=1 {json-secret-field=1}`, 如 `A5 json:client_secret=<'$'+lower+23 lower/digit> \| exit=0 alert m=1 {json-secret-field=1} \| exit=0 alert m=1 {json-secret-field=1}`。非作者坏实现 `mA` 使 7j 转红 (`14/15 as expected; wrong: angle-inner`)。附注: 保留分支 K1 (Unicode `…` 结尾) 与 K2 (整值尖括号) 实测为基线告警、目标静默, 已写进 W3 已知限制 (:99); 裁定 1 的「不与任何 ASCII 随机值重合」被执笔操作化为「与标准生成器不重合; 与含符号的口令生成器约 1e-4 重合, 已成文」, 本席接受 |
| K | `ac42f607` | closed | :189 launcher 集 = `secret-guard.sh:873` 的 13 词 + `command` + `exec`。本席 L1 对照共 11 条, 全部基线 exit=0 → 目标 exit=2: R2 本席 M1 点名的 9 条 (`pgrep curl \| xargs ps -fp`、`eval ps aux`、`unbuffer ps aux`、`sudo -u forgejo ps -ef`、`/bin/ps aux`、`/usr/bin/ps -ef`、python3 / node 读 `/proc/1/environ` 等), 加上 `ps -aux \| grep curl` 与 `while true; do ps aux; …; done`。非作者坏实现 `mU` (删 `unbuffer`) 使 22aw 转红 (`14/15 as expected; wrong: unbuffer`) |
| L | `ce6fc59c` (含 `5fd1f356`) | closed (残余 1 条 minor, 见 m1) | Tasks 1.12 (:370-375) 的四腿全是惰性诱饵: `ps aux \| head -c 0`、不存在目录下的 `forgejo/app.ini`、合成诱饵文件的 Read 腿 (经 harness 验 Read 提取)。它排在 1.11 发版之后, 执行条件已写明。头部 Rule #7 声明 (:14) 与 rule6_note 的 dogfood 句 (:316) 已同步; 10CG/aria-plugin#154 的关单前提已改指 1.12 (:350)。残余: 执行条件里的 `PASS` 字面不存在于探针输出 |
| M | `eb350937` (含 `51e90cab` / `5ce95ecf` / `e7e041c6`) | closed | 本席完整运行中全 yes 的有: 逐成员行 4p / 4s / 5n / 6i / 6j / 6k / 9x / 9y / 12k / 16q / 19u / 21j / 22aw–22bl, 以及上界差一对 19v–19y / 20f / 20n / 21x / 21y。`mut_summary_v3.txt` 记 420 个坏实现、406 个转红、14 个等价变异 (逐个点名)。本席的非作者坏实现 `mU`、`mA` 各在对应的枚举行 / 边界行转红 |
| N | `60f3173a` | closed | :126 插入段只含 tag 与 `tool_name`; 原型 `addl_msg` 只拼 `matches_breakdown` 与 `tool`。探针 13d (`baseline_probe.py:990-1000`) 在去掉严格形状的插入段后做全串等值; 13g (`:1003-1023`) 用 14 个敌意路径运行做整串等值。完整运行中 13a–13g 全 yes |
| O | `6bd285b1` (含 `c9357eb5` / `cfb24732`) | closed | :230-233 改为同次运行交错的整进程 CPU 时间比, 配活性断言、20 s 宽松墙钟、「基线 ≥5 s 判环境不合格」; (i) 档覆盖 L3 稠密输入; `timing_summary.txt` 记有各档与坏实现的比值。(f) 档依赖 100 ms 地板, 见下节 §6 第 3 条 |
| P | `05982c10` | closed | :352 规定只写 `Refs`, 并给出机械检查 (rc 判据照 10CG/Aria#199)。`refs_check.py` 正例 11、反例 12, `wrong: 0`。本席对本分支实跑同一检查: `merge-base=0748dbc HEAD=c0a6654 count=6`, 无匹配输出, `rc=1`。Tasks 贯穿行 (:357)、1.11、1.13 均已同步 |

上一轮 minor 中本席认为仍未处置的: 无。本席 R2 的 m1–m6 依次落在:

- m1 → :230-233;
- m2 → :162 与待复议 14;
- m3 → :161;
- m4 → :153 与 17d;
- m5 → :400;
- m6 → 头部「术语」行与 26i。

## 对执笔人自报薄弱点与请裁项的表态

**§6 自报薄弱点**

1. **原型不是实现, 坏实现是自构的** —— 可接受。本席非作者构造的 `mU`、`mA` 都在对应行转红, 与执笔的汇总一致。但本轮新发现 M1 落在「信封内容的形态」维度, 而不是「规则成员」维度。建议 Tasks 1.8 的非作者对抗 review 增加内容形态类变异: NUL 分隔、CR、超长单行。
2. **体量 +40%** —— 可接受, 不建议再削。
3. **时档阈值由单一主机定** —— 有条件可接受。「越界上呈、不放宽」本身符合 Rule #10, 问题在 (f) 档:
   - 原型实测比值 1.48–1.91 (`timing_summary.txt` 各次运行), 只是靠 100 ms 地板才过;
   - 在 CPU 比本机慢约 2.1 倍以上的主机上, 符合 Spec 的实现也会让 (f) 转红并被迫上呈。
   - 建议 owner 复议第 20 条时直接裁定 (f) 的上界 (例如 2.0 × max(基线, 100 ms)), 或写明 SC-30 只在与基线同类的主机上判。
4. **W1 使每次 Read 的成本升约 3 倍** —— Linux 上可接受 (约 +0.2 s CPU)。但 PostToolUse 是同步执行的, 而 10CG/aria-plugin#203 的报告者在 MINGW64。建议 B.2 在 Windows Git-Bash 实测一次 Read, 或把它作为已知风险明示 owner。
5. **已接受误报钉成 baseline-failing 行 (22bj / 10l)** —— 可接受, 建议保留: 它能防止有人为降误报而悄悄收窄检出。
6. **真 bash 3.2 沿用旧构建; Windows / macOS / BSD 未实测** —— 作为已声明的限制可接受。补一点: 32c 用的 bash 3.2 链接的是 glibc 正则, 而 macOS 上 `[[ =~ ]]` 走系统 libc 正则, W11 那几条超长行在 macOS 上的语义与耗时都未验证 (见风险第 1 条)。
7. **「表里写了、原型没做」** —— 可接受, 由 Tasks 1.8 覆盖。
8. **cr 两条备注未采纳** —— **不可接受**「没有可证伪的判据」这个理由。两条都有可证伪的判据:
   - **(a) 有效条目为零。**
     - 本席构造了 `mE2`: 先做存在 / 大小 / NUL / 条目数校验, 之后总是用 `printf '%s\n' "$entries"` 喂 `grep -f`。
     - 它在现有验收上全绿: `SC-18: 9/9`、`SC-19: 23/23`、`SC-20: 14/14`、`SC-25: 7/7`。
     - 但项目里只要有一个只含注释的 `.aria/secret-guard.paths`, Read / Edit 就一律 exit 2 —— 空行即空模式, 匹配一切。实跑 (列依次为基线 | 原型 | `mE2`):
```
exit=0 | exit=0 | exit=2 | R | '/x/README.md'
exit=0 | exit=0 | exit=2 | R | '/home/u/notes/todo.txt'
exit=0 | exit=0 | exit=2 | E | '/x/main.py'
```
     - 这违反 W9 自己的「从不因扩展问题 exit 2」(10CG/Aria#154 会话死锁教训)。
     - 建议在 SC-20 补一行: 文件存在、有效条目为 0 (仅注释、空行, 或坏条目全被跳过) → 两面金丝雀不变。三态为基线 yes / 原型 yes / `mE2` no。
     - 若计入 finding, 本席定级 major (testing, SC-20): 验收会放过一个错误实现。
   - **(b) 套件清理。**
     - 判据: 外层 HOME 预置一个 canary 文件和一份已知行数的日志, 跑完核对两者。
     - 现 SC-14 把外层日志缺失记作 0 行 (`baseline_probe.py:1518-1519`), 因此一个把外层 HOME 整个删掉的套件会被判绿。
     - 建议加强 SC-14, 并写进 B.2 实现注记。若计入 finding, 本席定级 minor。

**§7 请裁项**

1. **待复议 19 (W5)** —— 可接受默认 A。另提一个可供 owner 选的 B'': 若需要文件信息, 放进操作员通道 `systemMessage` (需先核实它对模型不可见), 而不是 additionalContext。
2. **10l 保留或删除** —— 保留, 理由同 §6 第 5 条。
3. **时档阈值与口径** —— 见 §6 第 3 条。
4. **W1 的每 Read 成本** —— 见 §6 第 4 条。
5. **cr 两条备注** —— 见 §6 第 8 条。建议写进 Spec 作为 SC 行, 而不只是实现注记。
6. **km 的两条风险**:
   - (a) A.1 认领心跳 (2026-09-30T17:57:13Z, `SWEEP_TTL` 24 h) 早已过期。这属于主控的例行维护 (2026-09-17 授权), 进 A.2 前应续心跳或重新认领。
   - (b) 7.1 的超时配方是否保留 —— 交 owner。本席倾向保留: hook 头注释已声明不防恶意操作者, 同一信息已在仓内研究笔记 `guard §0` 第 7 条。
7. **归档落盘** —— 可接受。本席用仓内归档 (只改 `EXP` 路径) 重建的原型与执笔的树逐字节相同, 完整运行与执笔的运行 T 逐字节相同。
8. **Rule #10 自作主张 (a)–(f)** —— 均可接受:
   - (a) 在裁定 2「纳入或列已知限制均可」之内;
   - (b) 比裁定 5 更严, 且满足其约束;
   - (c) 属同族修补;
   - (d) 是 harness 的限制;
   - (e) 是复跑修正;
   - (f) 变异范围与簇 M 的要求相称, 余量由 Tasks 1.8 承担。
9. **观察** —— 与本席一致:
   - 本席读取 R2 本席报告原文时, 现行 v1.74.1 的 L3 告警 1 次 (文档式占位, 已知误报族);
   - 本席一条写辅助脚本的 heredoc 被现行 L1 的 `\.env` 行拦下 (`os.environ` 加单词 `strings`, 正是 W12 治的误拦族), 改用 Write 工具落文件, 未用 `# guard:ack`。

## 风险 / 疑问

1. **macOS 正则引擎**:
   - W11 的三条新行与 `/proc` 改写行是带嵌套可选组的长 ERE;
   - SC-32 32c 的真 bash 3.2 链接 glibc, 不覆盖 macOS libc 正则的语义与耗时;
   - hook 超时等于放行;
   - 10CG/Aria#154 的死锁就发生在 macOS, 若有 macOS 采用方, 建议 B.2 跑一次。
2. **W9 的首要诉求方 (10CG/aria-plugin#203) 在 MINGW64**: `CLAUDE_PROJECT_DIR` 的路径形态未验证, 而失效是静默的, 扩展可能对它的主要用户静默不生效。建议 B.2 记录一次实值, 或在 §5.6 写明。
3. **W9 静默失效的归类**: 待复议第 18 条仍是「技术级 (已裁)」。本席仍认为它决定采用方能否得知自己配置的保护已失效, 属产品级; 只提示, 不重报。
4. **超时余量**:
   - 原型 h1 (150 段、全部放行) 的整进程 CPU 为 2.28 s, 基线 1.01 s;
   - 在慢 2 倍以上的主机上, 长命令的 W10 第二遍与扩展判定会逼近 5 s, 一旦被截断即放行;
   - 7.1 已列, 开单时宜写进这一具体量。
5. **Read 面 `/proc`**: M1 的修法只补检出, 不补预防; Read 面仍放行 (22au / 7.5)。
6. **本席自身操作**:
   - 全程未读取或打印任何真实凭据;
   - `pgrep -fl/-af` 只对本席自起的、带标记参数的 python 进程 (输出只见本席自己的 shell 包装命令);
   - `ps -o '%p %a'` 只对本 shell;
   - 本席运行期间主机负载约 17–50 (其他席位的探针并发运行)。

## Verdict

- verdict: **PASS_WITH_WARNINGS**
- counts: **0C / 1M / 2m**
- **Vote: REVISE**

## 是否足以进入 A.2

**不足以。** M1 要先回写 W1 的提取管道, 补一行 SC, 并订正 22au / 7.10 的文案; 建议同批补上 §6 第 8 条的两行 SC。这些改动都是局部的、一行级的, 七个 R2 簇已全部关闭, 不需要扩大返修面。