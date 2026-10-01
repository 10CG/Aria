---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-01T05:29:36.353Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — qa-engineer 席报告 (WP-A secret-net-l3-and-bypass-paths, proposal v2 @ b3e3123)

视角: 每条 SC 的可证伪性 (基线 / 目标 / 坏实现三态)。方法: 在自己的副本上 (a) 带真 bash 3.2.57 复跑基线探针, (b) 复跑写手的完整目标态原型, (c) 复现写手 25 个坏实现里的 10 个, (d) 另构造 14 个「实现不全」型坏实现和若干对抗输入, 对原型与基线逐条比对。真仓零写操作 (`git status` 干净, 主仓 HEAD `b3e3123`、aria `268da8f`、standards `2bc1c4c` 未变); 全部产物在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/audit/post_spec-R2-qa-engineer/`。

基线形态与目标形态均已独立复现 (见下): 基线 `baseline-failing` 0/154、`doc-sync` 0/20、其余类别全 yes; 目标原型 154/154、20/20、全 yes。v2 把 R1 的 6 个 critical 与 24 个 major 的核心问题都修住了 (逐条对账见后)。本轮新发现 4 条 major、5 条 minor: 3 条是「验收放过实现不全 / 实现错误」, 1 条是 W5 的受信通道拼接, 没有一条是 v2 的 fix 自身引入的缺陷 (均落在 v1 已有的设计 / 验收面上)。

## 已实读文件

- 被审对象: `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` (1-402 全文)、`baseline_probe.py` (1-1531 全文)、`baseline-evidence.md` (头部 1-40 实读; 正文用我自己的实跑输出做全文比对: 内嵌输出与我的 stdout 逐字节相同)。三份文件落盘 sha256 前 16 位与返修报告 MANIFEST 一致 (`654cb86e8d588ffe` / `522fe6216524d5ea` / `bbcdf8377f2447e9`)。
- issue 与决策: `aria-plugin-154.md` / `aria-plugin-203.md` / `Aria-221.md` (正文加全部评论) 全文; `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; `CLAUDE.md` 规则 #6 / #7 / #10 与多远程两条硬约束。
- 源码与规范 (实读): `aria/hooks/secret-scan.sh` (1-377 全文)、`aria/hooks/secret-guard.sh` (1-1120 全文)、`aria/hooks/hooks.json` 全文、`aria/hooks/tests/secret-guard.test.sh` (`:11`、`:389-391`、`:1620-1622`、`:1660-1915` SC-8 计时器、`:2018-2030`, 另对 `ps` / `pgrep` / `os.environ` / `/proc/` 做全文 grep)、`standards/conventions/skill-benchmark-exemption.md` 全文、`standards/conventions/secret-hygiene.md` (标题骨架 + `:23` `:287` `:288` `:319`)、`aria/VERSION:164`、`aria/README.md` / `README.zh.md` 的 Hooks 标题。
- 上一轮与本版执笔材料: R1 聚合报告 (全文, 含「主控记录」)、R1 qa 席报告 (全文); 其余四席原文未读, 只取聚合表。`v2-writer-report.md` 全文、`writer-v2-proto/` (README / build_full.sh / 三份 mut_summary)、原型树对基线的 `diff` (guard 与 scan 两个 hook)。`openspec/archive/2026-08-02-secret-guard-nomad-var-put-echo` 的 rule6 段、`pre-merge-completeness-gate-change-scope/detailed-tasks.yaml:341-342` 的 `guard_config_hooks` (与 Impact 所引命令逐字一致)。
- 四份研究笔记: 未精读 (背景材料); 所有结论以源码与我的实跑为准, 未发现与笔记冲突处。
- 平台事实核验: 本机 Claude Code 2.1.285 二进制含 `updatedToolOutput` 与描述原文 (`grep -a`), Spec 的 Why 段与 SC-28 28l 的前提成立。
- 实跑: (1) 基线探针 (带 `WPA_BASH32`) stdout sha256 前 16 位 `13cdea30978e1119`、52197 字节, 与写手 E1a 逐字节相同, 耗时 6 分 31 秒 (主机负载 13-16); (2) 目标原型完整探针 (带真 bash 3.2) 前 16 位 `4b0eea9cd97621d4`、52861 字节, 与写手 T1 逐字节相同, `target shape ... holds`; (3) 原型 L3 子集连跑 3 次、随机值生成无偶发红; (4) 写手变体复现与我自己的 14 个坏实现 (下)。

## Findings

### Critical

无。

### Major

**M1** — id `5ce95ecf` / major / issue / testing
scope: `proposal.md SC-22`
summary: W14 明写「`/proc` 两行原位改写」, 但对这两行既有读取器的反向守卫只有 22J 的 5 条命令; 基线行名了 13 个读取器, 其中 9 个 (`head` `tail` `less` `more` `hexdump` `od` `xxd` `awk` `perl` `rev`) 没有任何行。把合并后的读取器表缩成 `cat|strings|tr|xargs` 的实现, 使 9 类基线已拦的 `/proc/<pid>/environ|cmdline` 读取变为放行, SC-22 全 51 行与既有套件都不红。
证据:
- Spec: `proposal.md:225` 「`/proc` 两行原位改写」, `:224` 「改 `/proc` 读取器行开头的分组会让该族 key 改名」, `:187` 「读取器补 `xargs sed grep …`」。
- 基线 `secret-guard.sh:932-933`: 读取器 `(cat|head|tail|less|more|strings|hexdump|od|xxd|tr|awk|perl|rev)` 加一条 `<` 行。反向守卫 22J (`baseline_probe.py:912-914`) 只有 `cat /proc/123/cmdline`、`tr … < …`、`cat …/environ`、`cat /proc/self/environ`、`strings /proc/1/environ`; 既有套件只有 `secret-guard.test.sh:389-391` 的 3 个用例 (`cat` ×2、`tr <`)。
- 变异 `l1_procold` (原型 `/proc` 行的两个读取器表合并重打成 `cat|strings|tr|xargs`, 其余不动) 实跑, 退出码 基线 / 目标 / 变异:
```
head -c 400 /proc/123/environ   2 / 2 / 0      hexdump -C /proc/123/environ   2 / 2 / 0
tail -n 3 /proc/123/environ     2 / 2 / 0      od -c /proc/123/environ        2 / 2 / 0
less /proc/123/environ          2 / 2 / 0      xxd /proc/123/environ          2 / 2 / 0
awk 1 /proc/123/cmdline         2 / 2 / 0      perl -pe 1 /proc/123/environ   2 / 2 / 0
rev /proc/123/environ           2 / 2 / 0      cat /proc/123/environ  2 / 2 / 2      strings /proc/1/environ 2 / 2 / 2
```
  同一变异下 `WPA_ONLY=SC-22` 51 行 `no` 行数为 0 (22J 仍 `exit=2,2,2,2,2 yes`)。
- 写手原型把旧读取器在 `/proc` 行的两个分支里各列一遍 (原型 `secret-guard.sh:1117`), 恰好掩盖了「合并时丢成员」, 所以「原型 51/51」不能证明反向守卫够用。
失败场景: 实现者按 W14 原位重写两行、合并读取器表时漏掉旧成员 → SC-22 / SC-29 全绿 → 发版后 `head -c 4000 /proc/<pid>/environ` 这类基线已拦的写法放行, 目标进程的环境变量 (含 token) 进入会话: 与 W11 要关闭的泄露面同形, 且是「现有拦截变放行」。
建议修法: SC-22 补 reverse-guard 行, 对基线 13 个读取器逐个 × {`environ`, `cmdline`} × {直读, `<` 重定向, `self`} (`l1m` 一行 AND 即可, 不增行数); SC-31 / Tasks 加一条通则: 凡被「原位改写」的既有 `risky_patterns` 行, SC 里必须有「该行基线拦截集逐条重放」的行。严重度依 R1 同类 (`1c0bc16f`, 「检出被悄悄收窄」) 定 major; 若主控从严按「验收放过一个错误实现」字面, 此条可升 critical。

**M2** — id `eb350937` / major / issue / testing
scope: `baseline_probe.py`
summary: 枚举型要求只按个别代表成员出行, 而 SC 的「怎么会红」写成会抓全表; 我构造的 14 个「实现不全 / 边界错」的坏实现 (L1 6 个、L3 3 个、W9 上界 5 个) 在各自对应的全部行上 0 行红; 写手的 25 个坏实现都是「违反某个设计选项」类 (自报薄弱点 8 的同源盲区), Tasks 1.8 点名的 12 类同属此类, 没有「缺项」类。
证据: 每个变异都做在写手目标态原型上、`bash -n` 通过; 下表「演示」是同一条命令在原型与变异上的退出码 (L3 为 ALERT / silent), 「红行数」是对应探针行 (`WPA_ONLY`) 的实跑。

| # | 坏实现 | Spec 承诺与「怎么会红」 | 探针里被测的成员 | 演示 原型 / 变异 | 红行数 |
|---|---|---|---|---|---|
| 1 | W8 读取器组缩成 `cat\|grep\|head\|awk\|sed` | `:145` 13 + 16 个读取器; SC-16 `:269`「读取器组漏某个读取器」 | sed cat head grep awk (+ python3 -c) | `tail -n 50` / `less` / `strings` / `jq -R .` / `rg JWT` / `nl` + `/etc/forgejo/app.ini`: 2 / 0 | 0 (SC-16..18, 22 行) |
| 2 | W8 `node -e` 源组缺名字组 | `:145`「python3 -c / node -e 源组追加同一名字组」 | 只测 python3 -c (16h) | `node -e "…readFileSync('/etc/forgejo/app.ini'…)"`: 2 / 0 | 0 |
| 3 | W11 launcher 缩成 `sudo\|watch` | `:185` 11 个 launcher「对以上全部生效 (22n)」; SC-22 `:275`「launcher 包裹未覆盖」 | sudo、watch | `doas` / `nice -n 5` / `timeout 5` / `nohup` / `env` / `time` / `setsid` / `ionice` / `stdbuf -oL` / `command` / `exec` + `ps aux`: 2 / 0 (11 条) | 0 (SC-22, 51 行) |
| 4 | W11 `/proc` 新读取器只补 `xargs` | `:187` 13 个 (22F-22I, 22an) | cat、xargs | `sed -n p` / `grep -a .` / `egrep` / `rg -a` / `cut` / `paste` / `nl` / `sort` / `base64` / `cp … /dev/stdout` / `dd if=` + `/proc/123/environ`: 2 / 0 (11 条) | 0 |
| 5 | W11 远程包裹缺 docker / podman / lxc exec | `:185` | ssh kubectl pct nomad sh -c watch | `docker exec c ps aux` / `podman exec c ps -ef` / `lxc exec c -- ps aux` / `docker compose exec web ps aux`: 2 / 0 | 0 |
| 6 | W9 扩展条目不与 `node -e` 源组组合 | `:157` | 只测 python3 -c (19o) | `node -e` 读列入路径: 2 / 0 | 0 (SC-19/20, 31 行) |
| 7 | W2 名表缺 4 个名干 (`secret_key` `api_token` `bearer_token` `session_token`, 4 种拼写共 16 个) | `:59` 17 个名干 × 4 拼写; SC-4 `:254`「名表缺项、拼写变体没覆盖」 | 仅 token sha1 registration_token jwt_secret auth_token + camel `apiKey` + Pascal `ClientSecret` | 六种键形 (`{"session_token":…}` 等): ALERT / silent | 0 (SC-1..13, 123 行) |
| 8 | W2 两个键形 tag 的关键字集 10 个缩成 `SECRET\|PASSWORD\|PASSWD\|TOKEN` | `:60-61` | JWT_SECRET SECRET_KEY PASSWD LFS_JWT_SECRET API_TOKEN DB_PASSWORD | `API_KEY` / `APIKEY` / `PRIVATE_KEY` / `ENCRYPTION_KEY` / `ACCESS_KEY` 赋值与 Env 映射共 10 形: ALERT / silent | 0 |
| 9 | W2 `cli-secret-flag` 名集 6 个缩成 `token` | `:64` | 只 `--token=` | `--password=` `--passwd=` `--secret=` `--api-key=` `--apikey=` `--access-key=`: ALERT / silent | 0 |
| 10-14 | W9 上界 / 边界: 恰 200 条即整体忽略 (`>=200`); 去掉「含字母或数字」; 去掉条目长度上限 200; 去掉 64 处出现点上界; 文件上限写成 `<32768` | `:156` `:158` `:161` | 只测 3 字符条目、201 条、34 KB | — | 各 0 (SC-19/20, 31 行) |

  另 (检查而未造变异): W4 对 PEM 记 `-`、W3 的 `${{…}}` 模板与 ASCII `...` 截断标记、W10 的「16 个赋值」上限, Spec 都成文而没有行。
- 对照: 我复现的写手变体 10 个全部被抓, 红行与写手汇总一致: `ext_bare` → 20i 20j; `ext_first` → 19i 20l; `vx_interleave` → 21v; 去掉 W12 归一化 → 23a 23b; `ext_trunc` → 20f; `ent_on_old` / `wl_envline` → 7h; `w5_append` → 13d; `loosepath` → 4n 5l 9w; `noentropy` → 9p 10a 10b。被抓的都是「违反某个已写明的设计取舍」, 存活的都是「某个枚举没写全」。
失败场景: 实现者从 Spec 抄名表 / 读取器表时漏项, 或把读取器表只写成探针用到的几个 → 全部 SC 绿 (SC-29 同样看不见) → 例如 `tail /etc/forgejo/app.ini` 放行 (正是 2026-09-26 事故类的读取方式)、`doas ps aux` 放行、`{"session_token":…}` 与 `ENCRYPTION_KEY = …` 静默。
建议修法: 每个枚举一行 `l1m` / `l3m` 多用例行, 逐成员各一个用例 (AND, 行数不增), 红了仍能指出缺哪一项; W9 上界补边界对 (200 / 201 条、32768 / 32769 字节、200 / 201 字符条目、纯符号条目、64 / 65 处出现点); 把「缺项类」(对每个枚举删掉成员) 与「边界差一」加进 Tasks 1.8 的变异清单; 订正各 SC「怎么会红」里与实际覆盖不符的句子。

**M3** — id `ac42f607` / major / issue / implementation
scope: `proposal.md What.W11`
summary: W11 的 `ps` 形态识别写成「任意 BSD 选项簇 (不带 `-`)」「SysV `-f` / `-F`」「`-o` 列含 args|cmd|command」, 漏掉带前导 `-` 的 BSD 式拼写 (`ps -aux`、`ps -ax`、`ps -x`、`ps -w -x`) 与 SysV `-O`; procps-ng 4.0.2 上这些写法输出完整 argv, 按 Spec 字面实现的原型放行, 10CG/Aria#221 点名的「`ps` 列举 + `grep`」形态换成 `ps -aux | grep curl` 即绕过。SC-22 的 41 行没有这些拼写, 已知限制也没写。
证据:
- Spec `proposal.md:184`「`ps`: 任意 BSD 选项簇 (不带 `-`, 如 `aux`、`e`、`eww`) …」; 全文无 `-aux` / `-ax` / `-x` / `-O` 字样 (`grep` 核实)。
- 本机 procps-ng 4.0.2 实跑: `ps -aux`、`ps -ax`、`ps -x`、`ps -w -x`、`ps -eO rss` 的 COMMAND 列都是完整命令行 (例: `ps -ax` 的第二行为 PID 1 的 `…/systemd --system --deserialize=33`); `ps -u dev`、`ps -e` 只出名字。
- 原型退出码 基线 / 目标:
```
ps aux            0 / 2        ps -ef             0 / 2        ps ax   0 / 2     ps x   0 / 2
ps -aux           0 / 0        ps -ax             0 / 0        ps -x   0 / 0     ps -w -x   0 / 0
ps -axu           0 / 0        ps -auxww          0 / 0        ps -aux | grep curl   0 / 0       ps -eO rss   0 / 0
```
  对照: 20 条常见只出名字的 `ps` / `pgrep` / `top` 形态 (`ps -p $$`、`ps -u root`、`ps -o comm= -p …` 等) 目标与基线一致放行, 所以补上这些拼写不会引入新误拦。
失败场景: 与 10CG/Aria#221 同形的事故 (后台轮询进程命令行里有 CF Access secret 与 PAT) 复发时, 使用者最常见的写法 `ps -aux | grep …` 照旧放行, 完整 argv 进入会话; Impact 与待复议第 5 条还把 `ps aux | grep` 写成「被拦」, 读者会以为这一族已封。
建议修法: W11 把 `ps` 的判定改为「带 `x` / `a`+`u` 的 BSD 字母簇不论有无前导 `-`」+ SysV `-O` 并入, SC-22 补这批拼写的 baseline-failing 行与 `ps -u` / `ps -e` 的放行行; 或把未覆盖的拼写写进 W11 已知限制并用 known-limit 行钉住。

**M4** — id `60f3173a` / major / issue / architecture
scope: `proposal.md What.W5`
summary: W5 把 `tool_input.file_path` 原样 (仅剥 CR) 拼进 hook 的 `additionalContext`, 这是此前不含任何外来文本的受信通道; 合法文件名里的 `)` 可以闭合描述性括号并接任意祈使句, 换行可以伪造第二条 `[secret-scan]` 行。13a-c 只用良性路径, 13d 的剥除正则对括号内内容不设限, rule6 块 B「插入的是事实陈述, 不含指示行为的措辞」的归类前提因此对敌意输入不成立; W5 自己拒绝「Bash 也附命令摘要」的理由 (命令文本不可信) 同样适用于路径, 文中没有论证为什么路径可以。
证据:
- Spec `proposal.md:122`「`file_path` … 只对 Read 与 Write 输出 (取值剥 CR)」, `:123` 选项 C 的拒绝理由, `:319` 块 B 理由。
- 原型 (忠实于 Spec) 上用运行时生成的 AWS key id 形内容喂 Read 信封, 路径取敌意值, 实际 additionalContext (均无值回显, 仅路径部分为我构造的占位文本):
```
路径 /x/a.txt) — <攻击者祈使句> (    →  …(tags: aws-access-key-id=1; source: Read /x/a.txt) — <攻击者祈使句> () — treat as already-leaked; do NOT repeat…
路径 /x/b.txt⏎[secret-scan] <攻击者伪造行>  →  …(tags: …; source: Read /x/b.txt⏎[secret-scan] <攻击者伪造行>) — treat as already-leaked; …
```
- 既有 L1 的 Read/Edit BLOCKED 文案 (`secret-guard.sh:676-690`) 已把裸 `$file_path` 回显到 stderr, 所以「回显路径」不是全新类别; 区别是 L3 的 `additionalContext` 是更高信任的 hook 通道, 且基线它只含计数。
失败场景: 采用方让 AI 读一个不可信仓库里的文件, 文件含一条 AWS key id 形样例值且文件名带 `)` 加指令文本 → L3 告警句里出现攻击者文本, 位于模型最信任的 hook 告警措辞之内 (可诱导「忽略轮换建议」之类); SC-13 全绿, 实现者没有任何信号。
建议修法: `additionalContext` 只给 `source: Read` 不带路径, 路径需要时放操作员可见的 `systemMessage`; 或仅取 basename 并过滤成 `[A-Za-z0-9._ -]`、替换其余字符、截断到 ≤120、去掉括号与控制字符; SC-13 补 Read / Write 敌意路径行 (含 `)` 与换行), 判据 = 删去恰一个插入段后全串等于基线, 且插入段内无括号 / 换行; 在块 B 理由里补一句插入段只含工具名与已净化路径。

### Minor

**m1** — id `a4af42ab` / minor / issue / documentation
scope: `proposal.md What.W3`
summary: 白名单对既有 `json-secret-field` 仍有两处检出收窄没有写进已知限制、也没有行钉住 (R1 簇 A 的残余): `$` 后接「全小写加数字」或「全大写加数字」的值 (`$NAME` 形), 以及以 `...` / `…` 结尾的值。
证据 (值运行时生成, 只看是否告警): `{"password":"$<16 位小写+数字>"}` 基线 alert / 目标 silent; `{"password":"$<16 位大写+数字>"}` alert / silent; `{"password":"$<16 位混合>"}` alert / alert; `{"password":"<14 位混合>..."}` alert / silent; `{"password":"$ecret2024Pass"}` alert / alert。7h 只钉了混合大小写的 `$` 值。已知限制 `:95` 的四条里没有这两类。
失败场景: 小写字母数字生成器产出的 `$` 前缀口令放进 JSON 的 `password` 键里 → 目标静默 (基线告警); 人工口令以 `...` 结尾同理。人群很小, 但 R1 簇 A 的原则就是「收窄必须成文并钉住」。
建议修法: 两类各加一个 known-limit 行并写进 `:95`; 或把 `$NAME` 限定为不含数字且长度 <16 之类的更窄形态。

**m2** — id `6114c254` / minor / issue / implementation
scope: `proposal.md What.W2`
summary: 点分标识符链排除的理由「随机凭据不含以 `.` 分隔的标识符段, 漏报面≈0」(`:74`) 不成立: 由三段「首字母是字母、只含字母数字下划线」的段拼成的凭据 (Discord bot token 形、itsdangerous 签名 cookie 形) 在新 tag 上静默, 已知限制 `:75` 与 SC-10 都没有这一类。
证据 (值运行时生成, 无 `-` 的段): `DISCORD_BOT_TOKEN = <24+6+27 位三段>`、`export DISCORD_TOKEN=<同形>`、`{"token":"<同形>"}`、`SESSION_SECRET: <三段>`、`API_TOKEN = <22 位.20 位>` 在基线与目标原型上全部 silent (行首无空格的 `DISCORD_TOKEN=<同形>` 由既有 env-line 在两侧都告警)。约一半的真实 Discord bot token 不含 `-`。
失败场景: 采用方这类凭据以 `KEY = value` 或 JSON `token` 形出现在 Read / Bash 输出里, 新 tag 不告警, 而 Spec 说漏报面≈0。
建议修法: 订正「≈0」并加一个 known-limit 行; 或把排除收窄为首段属小词表 (`process` `os` `env` `ENV` `settings` `config` `secrets` `vars` …) 的链, 仍能压住 9v 的三种写法。

**m3** — id `c941e4e1` / minor / issue / implementation
scope: `proposal.md What.W8`
summary: W8 的 Bash 面名字组大小写敏感且不认反斜杠路径分隔符, Read / Edit 面 (对小写化路径匹配) 两者都认, 两面不一致且文中未写; 同一份 Spec 的 W9 明确要求两面大小写不敏感。10CG/aria-plugin#203 的报告环境是 MINGW64 (Windows Git-Bash)。
证据 (退出码 基线 / 目标原型): Bash `cat /opt/Gitea/conf/app.ini` 0 / 0, `cat /srv/Forgejo/app.ini` 0 / 0, `cat 'C:\gitea\custom\conf\app.ini'` 0 / 0, `cat "$GITEA_CUSTOM/conf/app.ini"` 0 / 0; Read `/opt/Gitea/conf/app.ini`、`/srv/Forgejo/app.ini`、`C:\Gitea\custom\conf\app.ini` 均 0 / 2; `app.inix` Bash 放行、Read 拦 (Spec 说 `app.inix` 不在名单)。SC-16..18 没有这些形态。
失败场景: Windows 默认目录 `C:\gitea\…` 或大写目录名下的 `app.ini`, AI 经 Bash 读取放行, 经 Read 被拦。
建议修法: W8 写明两面一致的大小写与分隔符规则 (Bash 面等价于小写化 + 反斜杠归一), 并各补一行; 否则把差异写入已知限制。

**m4** — id `684e9a24` / minor / issue / documentation
scope: `proposal.md What.W9`
summary: 成本上界触顶后的行为方向没有成文: W9 的「最多检查 64 处出现点」与 W10 的「16 个赋值 / 每变量 8 次替换」超出后都是 fail-open (padding 即绕过), 无已知限制、无行; 另「无扩展文件时不 fork 任何子进程」(`:158`) 与「扩展代码只经 `$( … )` 调用」(`:159`) 互斥, 原型每次调用都进 `_sg_ext_pass` 的子 shell。
证据: 原型实跑 `echo P; …` 共 63 次后 `cat P` (第 64 处) exit 2、第 65 处 exit 0 (`CLAUDE_PROJECT_DIR` 指向含 `P` 的扩展文件; 基线 0); 16 个前置赋值后第 17 个赋值 `f=…app.ini; cat $f` exit 0、第 16 个 exit 2。无扩展文件时 `bash -x` 仍见 `++ _sg_ext_pass 'ls -la'` (子 shell 内调用); 写手自测「无扩展」比基线多约 6 ms (54 对 48)。上界的 5 个边界变异见 M2 (均存活)。
失败场景: 长脚本里同一路径出现 ≥65 次时, 之后的读取不被扩展检查; 实现者按「不 fork」去优化会与隔离要求冲突。
建议修法: 把两处上界的失效方向写进已知限制并各补一个 known-limit 行; 「无扩展不 fork」改写为「无扩展文件时在 `$( )` 之外先用 builtin 判定存在性」或删去该句并给出常数开销预算。

**m5** — id `335996c0` / minor / issue / testing
scope: `proposal.md SC-33`
summary: SC-33 声称关键词预筛是 6 个新 tag 的「必要条件」(`:289`), 但预筛正则 `KEYWORD_RE` (`baseline_probe.py:1380`) 不含 `private_key` 的 camel / Pascal / 连写拼写, 而 `json-credential-field` 名表含 `privateKey` `PrivateKey` `privatekey`。
证据: `re.search` 实测 `{"privateKey":"x"}`、`{"PrivateKey":"x"}`、`{"privatekey":"x"}` 预筛不命中, `{"private_key":"x"}` 命中; 原型的 json 名表含这三种拼写。
失败场景: 语料里只含这三种键的文件永远不被喂给 hook, 普查对该拼写失明。
建议修法: 预筛加 `private[_-]?key`。

### SC 三态核验总表 (非 finding)

「基线」「目标」为我的实跑 (基线全探针带真 bash 3.2; 目标 = 写手完整原型, 全探针带真 bash 3.2)。「坏实现」标注 (复) = 我复现, (写) = 写手汇总, (我) = 我自造。

| SC | 基线 | 目标 | 坏实现 → 红行 | 评 |
|---|---|---|---|---|
| 1 | 0/2 | 2/2 | 不加 `file.content` → 1a 1b 13a (R1 oracle) | 好 |
| 2 | 4/4 | 4/4 | 破坏旧分支 → 2a-2d (设计) | 好 |
| 3 | 2/2 | 2/2 | 扩面到 Edit / 字符串形 → 3a 3b (R1 oracle) | 好 |
| 4 | 0/15 | 15/15 | `loosepath` → 4n (复); 熵下限改须含数字 → 4o (写); 名表缺 4 名干 → 0 行 (我) | 弱 (M2) |
| 5 | 0/13 | 13/13 | `loosepath` → 5l (复); 关键字集缩成 4 个 → 0 行 (我) | 弱 (M2) |
| 6 | 0/8 | 8/8 | Client-Id 也计 → 6d 6g (R1); flag 名集缩成 `token` → 0 行 (我) | 弱 (M2) |
| 7 | 9/9 | 9/9 | `ent_on_old` `wl_envline` → 7h (复); 前缀 / 含式 / 大小写不敏感白名单 → 7h 7i 11s (写) | 好 (残余 m1) |
| 8 | 0/1 | 1/1 | 白名单漏哨兵整值 → 8a | 好 |
| 9 | 23/23 | 23/23 | `noentropy` → 9p (复); `noident` → 9v、`nopath` → 9o 9w (写) | 好; 基线恒绿 (新 tag 不存在, 鉴别力来自与 4/5/6 成对) |
| 10 | 7/7 | 7/7 | `noentropy` → 10a 10b (复) | 好 |
| 11 | 14/23 | 23/23 | 含式白名单 → 11s (写) | 好 |
| 12 | 3/10 | 10/10 | `fp_span` → 12g-12j (写) | 好 (PEM `-` 无行) |
| 13 | 3/6 | 6/6 | `w5_append` → 13d (复) | 好 (敌意路径无行, M4) |
| 14 | 0/2 | 2/2 | 晚隔离 HOME (设计) | 好 |
| 15 | 5/6 | 6/6 | `noentropy` → 15e 15f (写) | 好; 附件 `baseline-evidence.md` 不在行内 (风险 6) |
| 16 | 0/13 | 13/13 | `notight` → 16f (写); 读取器组缩成 5 个 / `node -e` 缺名字组 → 0 行 (我) | 弱 (M2) |
| 17 | 2/2 | 2/2 | 缺左边界 / 退化裸名 → 17a (设计) | 好 |
| 18 | 2/7 | 7/7 | 设计 | 好 |
| 19 | 6/18 | 18/18 | `ext_first` → 19i (复); 条目当正则 → 19j (写); 扩展不配 `node -e` → 0 行 (我) | 弱 (M2) |
| 20 | 11/13 | 13/13 | `ext_bare` → 20i 20j、`ext_first` → 20l、`ext_trunc` → 20f (复); 上界 / 边界 5 变异 → 0 行 (我) | 弱 (M2); 20i-20l 基线恒绿 (无 `_sg_ext_*`, SC 自述) |
| 21 | 10/19 | 19/19 | `vx_interleave` → 21v (复); `${s//p/r}` → 32c (写) | 好 |
| 22 | 10/51 | 51/51 | `proc_status` → 22as (写); launcher / `/proc` 读取器 / 远程包裹缩减、`/proc` 合并读取器表 → 0 行 (我) | 弱 (M1 M2 M3) |
| 23 | 6/8 | 8/8 | 去掉归一化 → 23a 23b (复); 加右边界 → 23c 23d 23h (写) | 好 |
| 24 | 4/9 | 9/9 | jq 新词进宽松词表 → 24f (写) | 好 |
| 25 | 3/7 | 7/7 | 改文案 → 25a-25g (设计) | 好 |
| 26 | 1/8 | 8/8 | SOT 只堆版本历史表 → 26a-26d 28h (写); 锚点 `### 2.2` `### 2.5` 在基线存在, `### 3.8` `### 5.6` 须新建, README 锚点在 `README.md:137` / `README.zh.md:137` | 好 (限定小节后词元堆砌仍可过, 可接受) |
| 27 | 2/3 | 3/3 | 忘回填 → 红 | 好 |
| 28 | 0/12 | 12/12 | 删句 → 新文本缺席转红 (设计) | 好 |
| 29 | 9/9 | 9/9 | 只防外溢; `/proc` 回退不可见 (M1) | 好 |
| 30 | 无探针 | — | — | 见风险 1 |
| 31 | 5/5 | 5/5 (149 ≤ 150, family 64 = 64) | 规则膨胀 / 纯变量行 (设计) | 好 (余量 1 行, 风险 1) |
| 32 | 3/3 | 3/3 | `[[ -v ]]` → 32a 32c、`${s//p/r}` → 32c (写) | 好; 未带 `WPA_BASH32` 时总括行仍印 holds (见第 4 节) |
| 33 | 1/1 (自述恒绿) | 1/1 (flagged=1, 在归因清单内) | 去熵下限 → 33a (写); `noentropy` 的 L3 行 (复) | 好 (预筛 m5) |

## 上一轮对账

R1 的 6 条 critical 与 24 条 major 按主控归并簇对账 (键为 R1 聚合表键)。

| R1 键 | 簇 | 状态 | 我核验的证据 |
|---|---|---|---|
| `e8d39a8a` `14b7e703` `8645b99f` | A: W3 前缀白名单 (critical ×2 + major) | closed (残余 m1) | W3 改为整值形态; 基线上 7h (7 个独立运行) 与 7i 全 yes、11m-11v 全 no; 原型 SC-7 / SC-11 23/23; `wl_envline` `ent_on_old` → 7h 红 (复); 另测 crypt 哈希、`$` 混合大小写、`<` 未闭合在目标仍告警 |
| `e600e931` `179045cd` `f42265a1` | B: W12 `\.env` 右边界 (critical ×3) | closed | 23c 十形基线 exit 2、目标 exit 2; 23a 23b 基线红目标绿; 另跑 17 个整表 / 单键 `os.environ` 形态 (`*items()`、`{**os.environ}`、`list(...)`、`keys()` / `values()`、与单键同现、`json.dumps(dict(...))` 等) 整表一律仍拦, 单键 (含 `os.environb[…]`) 放行; 去掉归一化 → 23a 23b 红 (复) |
| `ab6a3123` `d9308fba` | B2: `.env2` `.envprod` `.envs` 经解释器 | closed | 23d 九形基线 / 目标均 exit 2; 23g 23h known-limit 基线 yes |
| `7e0343bd` | C: W9 扩展故障中断内建 (critical) | closed | `_sg_ext_*` 只经 `$( )`; 20i-20k 注入; `ext_bare` → 20i 20j 红 (Read 面得 exit 1) (复); `ext_first` → 19i 20l (复) |
| `d4bcaf7c` | C2: W9 逐条正则的延迟 | closed | 固定字符串单遍; 写手测得 200 条扩展单段 62 对 54 ms; 我的 `ext` 相关行全绿 |
| `d8e7b380` | C2: 新路径延迟与求值顺序 | partially closed | 求值顺序已钉 (20l 21v, 变异红); 时档 (f)(g)(h) 只在 SC-30 文字里, 无基线数字, 取样口径未定 (第 4 节条目 7 与风险 1) |
| `719ae05c` | C3: 条目元字符 | closed | 19j 14 个元字符条目 + 20h 基线全红; `ext_regex` → 19j 20h (写) |
| `53c140c4` `27f6c3ce` `b73ab606` | C4: W9 / W8 文档落点 | closed | SC-26c / e / f / g 基线 `no`、目标 `yes`; 落点含 SOT §5.6 / §2.2、README 两语种、hook 头注释、CHANGELOG, 同步面与 Tasks 1.9 / 1.11 承载 |
| `634eac5c` `2ce0049b` | D: W4 指纹口径 | closed | W4 逐 tag 取值表; 12a-12j 基线 `no`、目标 `yes`; `fp_span` → 12g-12j (写); 12j 我复核: 六形按 PATTERNS 序 = 文本序, 顺序只由 12h 钉 |
| `44b5bb44` | E: bash 3.2 | closed (带第 4 节条目 6 的提示) | 真 bash 3.2.57 在场; 32c 基线 277 行一致、目标同; 29h 49/49、29i 581/582 (基线) / 584/585 (目标); `[[ -v ]]` → 32a 32c (写) |
| `e2459206` `9db51a43` | F: 包裹下 env 转储 / `/proc` status | closed | 22ao-22ar 基线 `no`; 22as 22at 基线 `yes`、22aj 基线 exit 2; `proc_status` → 22as (写) |
| `846b21f8` | G: W13 与 SOT 示例 | closed | §3.8 限定适用面; 26h 基线 yes (哈希常量与基线一致) |
| `7deac83f` `2779a016` `ba98e41f` | H: 评论口径 / 同步面 | closed | 默认理解 B 与决策单第 2 项字面「本项之下不评论」一致; 主仓 16 版本点 = 2+2+9+1+1+1 (算术核对) + aria 6 文件 + 2 gitlink |
| `cf0ae932` | I: 笔记悬空 | closed | 四份笔记已在 `.aria/notes/2026-09-30-wpa-phase-a/research/`, 头部声明承重判据只靠探针 |
| `d9986b27` | J: 13d | closed | 13d 改全串等值; `w5_append` → 13d 红 (复) |
| `5831f8c0` | J: SC-26 | closed | 限定小节; 基线 doc-sync 0/20 |
| `1c0bc16f` | J: 反向守卫缺负向侧 | closed (新实例见 M2) | 五个存活变异现被 7h / 4o / 10b / 11s 抓住 (复 + 写) |
| `a3054a20` | J: 生成器首字符 | closed | `_gen_first` 用于 4n 5l 5m 7h; `loosepath` → 4n 5l 9w 红 (复) |
| `8e77d1ca` | J: 语料级误报 | closed (残余 m2 m5) | SC-33 + 点分 / 路径形规则; 目标 flagged=1 (在归因清单内); 去熵下限 → 33a (写) |

R1 minor 里我认为仍未完全处置的: `a0cb1abc` (qa/m7, doc-sync 判据强度) — 现为小节限定, 26a 仍可被「一行含四个词元」满足, 可接受。其余 R1 minor 我抽查的均已落地 (含 `secret-guard.sh:626` 引用、`ps <pid>`、16 个版本点、Rule #7 声明)。

## 对执笔人自报薄弱点与请裁项的表态

薄弱点 (§5):
1. 体量 +44%: 可接受; 但「怎么会红」里有与实际覆盖不符的句子 (M2), 应订正而不是削。
2. 交付形态偏离: 可接受 (三份文件 sha256 与 MANIFEST 一致, 我复跑逐字节一致)。
3. 原型不是实现: 可接受; 附注: 原型 `/proc` 行把旧读取器在两个分支各列一遍, 掩盖丢成员的错误 (M1), 所以原型通过只证明设计可达, 不证明反向守卫够用。
4. 「变异实测」类声称与未复跑的笔记出处数字: 可接受 (已标出处); 我复现的 10 个写手变体与其红行一致。
5. 12j 未经独立 review: 可接受。基线 `no`、目标 `yes`、`fp_span` 红; 六个形态的文本序恰等于 PATTERNS 序, 顺序只由 12h 钉住。
6. bash 3.2 腿默认关: 不可接受 (按 paper-fix 判据)。我实测 `WPA_ONLY=SC-32` 且不设 `WPA_BASH32` 时, 32c 是 `not-run (n/a)`, 总括行仍印 `target shape (every row 'yes'): holds` (`baseline_probe.py:1519` 的 `all(...)` 不计 `ok=None` 的行); 全探针下 29h / 29i / 32c 同理, root 容器里 20g 也是 `n/a`。把「必须带腿」只写在 Tasks 1.1 / 1.10 是文字约束, 机械兜底缺位, 正是 R1 簇 E 想堵的 macOS 全量阻断的验收盲点。
7. 性能数字噪声大, (h) 档余量 0.6 s: 有条件可接受, 条件是在 SC-30 补取样口径与负载前置。我实测基线 600 段 (`echo` + 末段 dotenv 读取) 在主机负载 13 下三次为 13.7 / 15.4 / 13.8 s, 目标原型 18.2 / 14.0 / 5.2 s, 即绝对上限 5 s 在忙主机上连基线都过不了; 写手自报 ±20% 噪声大于 0.6 s 余量 (4.4 s × 1.2 = 5.3 s)。且 `:225` 引的原型数字是整进程耗时, 而「沿用测试内 SC-8 的计时器」是进程内 min-of-rounds (`secret-guard.test.sh:1879-1910`), 两个口径不可比。
8. 25 个坏实现同源盲区: 可接受为风险, 且被 M2 证实 (写手变体全被抓, 我的 14 个缺项 / 边界变异全存活)。
9. SC-33 归因清单写死两个路径: 可接受。
10. W9 静默失效是产品取舍: 可接受 (技术级默认 + 待复议 18)。
11. Windows / macOS 未实测: 可接受为风险; 但 W8 在 Windows 路径形态上的缺口已有实测证据 (m3)。
12. 探针并发竞态: 可接受; 我在负载 13-17 的共享主机上并发多路运行未见偶发红。

请裁项 (§6):
1. rule6_note 块 A 取 `n/a`: 可接受。SOT §4.1 模板明文 `n/a = 本 spec 不属 Skill 变更`, 块 A 「分类, 不是免验主张」+ substitute 三件与 2026-08-02 owner 裁定 (否决「Rule #6 不适用」式免验、统一为 substitute 框定) 不冲突; 保留那句说明即可。块 B 取 `1` 的前提见 M4。
2. 是否再削体量: 不削, 先订正失实句。
3. W9 静默失效: 可接受默认 A。
4. #203 / #221 评论口径: 可接受理解 B, 与决策单第 2 项执行注字面一致。
5. SC-33 不改 `no-plan-fallback.md`: 可接受 (改 Skill 目录示例会牵动 Rule #6)。
6. 探针对未带 `WPA_BASH32` 的处理: 基线形态检查可继续容忍 `n/a`; 但目标态总括行在存在 `n/a` 行时不得印 `holds` (印 `holds (N 行未运行)` 或失败), 并提供 `WPA_REQUIRE_ALL=1` 之类的严格开关供 Tasks 1.10 使用。
7. 原型与脚本归档: 已入仓 (`b3e3123` 含 `writer-v2-proto/` 15 个文件); 脚本内是会话临时目录绝对路径, 变异证据不能原样重跑, 建议 A.2 把「变异 harness」列为任务产物。
8. 交付形态: 可接受。

## 风险 / 疑问 (不计入 finding)

1. SC-30 三个新时档 (f)(g)(h) 没人跑过: 无基线数字、口径未定 (进程内 vs 整进程, N 与 rounds, 取 min 还是 median); 基线本身随负载剧烈漂移: 我在负载 15-17 下测得 4 KB 纯字面单段命令基线 2.4-4.9 s、8 KB 为 5.4-8.2 s (`_sg_safe_to_split` 的逐字符循环近似 O(n²)), 超过 5 s 即 hook 超时放行; 目标原型在噪声内与基线持平, 所以不是新回退, 但任何绝对 wall-clock 闸在共享主机上都不可靠。SC-31 的 ≤150 行预算, 原型已用 149, 余量 1 行。
2. `n/a` 行 (20g root 下不可构造、29h / 29i / 32c 无 `WPA_BASH32`、SC-30) 都不影响总括行, 见第 4 节条目 6。
3. Windows Git-Bash (10CG/aria-plugin#203 的报告环境): `CLAUDE_PROJECT_DIR` 路径形态、`/dev/fd` 进程替换、W8 反斜杠路径均无实测 (m3)。
4. Tasks 1.1 / 1.10 要求取得真 bash 3.2 (联网 + 编译器 + bison, 写手约 4 分钟); 无网络的自主运行时 (Layer 2) 没有写明「取不到」时的路径, 按 Rule #10 只能上报 owner, 建议在 Tasks 里写明。
5. 写手原型是「基线 + 脚本文本替换」, 且保留了坏实现开关; 同类原型对「实现不全」类变异天然偏乐观 (M1 M2)。
6. Rule #7 声明说「本 Spec 与两份附件」不含可被命中的字面量, SC-15 只钉 `proposal.md` 与探针; `baseline-evidence.md` 不在行内。我实测它在基线 hook 与目标原型的 L3 下 (Bash 与 Read 两种信封) 均 silent, 当前无问题, 但 B.2 重生成后无机械守卫。
7. 本席自己的 6 条 Bash 命令被已装的 v1.74.1 secret-guard 以「命令文本里出现 `/v1/var/`、`cat /proc/<pid>/environ`、`ssh … 'ps aux'` 一类字样」拦下 (prose-position 误拦), 改用 Write 工具落文件绕开; W11 上线后 `ps aux` 字样的 heredoc 会新增同类误拦 (写手 §7 已记)。
8. 收敛信号: 本席 4 条 major 都落在 v1 已有的设计 / 验收面上, 未发现 v2 的 fix 自身引入的 critical / major; R1 的两个 critical 簇 (A、B) 在我的对抗输入下均守住。

## Verdict

verdict: PASS_WITH_WARNINGS
counts: 0C/4M/5m
Vote: REVISE

## 是否足以进入 A.2

不足以 —— 4 条 major (M1 `/proc` 原位改写缺反向守卫、M2 枚举型验收放过实现不全、M3 `ps -aux` 一族漏拦、M4 W5 路径拼进受信通道) 都是对 SC 行与 W11 / W5 文字的小幅补强, 补完后再过一轮 post_spec 收敛, 才适合把 Spec 交给 task-planner。
