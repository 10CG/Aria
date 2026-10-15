---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-06T23:46:50.065Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — qa-engineer 席报告 (WP-A secret-net-l3-and-bypass-paths, proposal v4 @ b07f69a)

视角: 每条 SC 的可证伪性 (基线 / 目标 / 坏实现三态)。

**摘要**: R3 的 12 条 major (8 个簇) 里, Q / P / R / E / S / K 六簇我独立复核后确认关闭, M `eb350937` 与 T `0a8380fd` 两簇只部分关闭, 各留一条 major 残余。另有 3 条 minor。**无 critical**: 我没有找到「照 Spec 字面实现会使现有拦截或检出变成放行」的路径。两条 major 与 R3 同型 —— 验收没拦住一个自然的坏实现, 修法是补行 / 补一条清单项, 不涉设计取舍; 其中 M1 是 v4 新增机制 (`_sg_ext_mask`) 的覆盖缺口, M2 是既有设计里更深的缺口 (供主控按「本轮 fix 引入占比」判断)。

**方法**: (1) 在自己的副本 (aria `268da8f` + standards `2bc1c4c` 的 `cp -a`, 删子模块 gitfile) 上带真 bash 3.2.57 独立全量复跑基线探针; (2) 用执笔归档的补丁脚本在自己的副本上重建目标原型并全量复跑; (3) 抽样复跑对账项的坏实现, 并对 v4 新增 / 被改写的机制各自造「自然的坏实现」找存活者; (4) 手写、不经探针的 L1 / L3 输入核三态; (5) Rule #7 自扫。全程 HOME / TMPDIR 在本席目录; 像凭据的值只在进程内用 `secrets` 生成、未打印; 真仓 `git status` 干净、HEAD 仍是 `b07f69a`, 未做任何 git 写操作。

## 已实读文件

- **被审对象**: `proposal.md` 1-443 全文; `baseline-evidence.md` 头部 1-60 + 全部 SC 行 (411 行, 内嵌 stdout 块与我的实跑逐字节相等); `baseline_probe.py` 1-300、`:1348-1400`、`:1422-1475`、`:1625-1700`、`:1860-1960`、`:2030-2054`、`:2228-2345` (其余行以 evidence 的行描述代替, **未逐行通读 2414 行**)。三份文件 sha256 前 16 位 `f98e719d6036b4f8` / `7da0e53eef5d64da` / `4e0a94aac6e77058`, 与执笔报告一致。
- **issue 与决策**: `aria-plugin-154.md` / `aria-plugin-203.md` / `Aria-221.md` 正文加全部评论; `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; CLAUDE.md 规则 #6 / #7 / #10 与多远程两条硬约束 (会话上下文提供的全文)。
- **源码与规范**: `aria/hooks/secret-scan.sh` 1-377 全文; `secret-guard.sh` 的 `:380-500` `:560-570` `:625-735` `:1104-1120`, 并抽核 proposal 引用的 21 个行号锚点 (`:405/408/427/491/493/564/641/736/815/873/875/877/893/894/930/933/974/1009/1088/1102/1111`) 全部与基线相符; `hooks/tests/secret-guard.test.sh` (Read/Edit 用例与 `:488-520` 逐条) 与 `secret-scan.test.sh:1-60`; `standards/conventions/skill-benchmark-exemption.md` 全文; `secret-hygiene.md` `:1-30` `:108-236` 与全部标题; `git-commit.md` §6.1; `.aria/probes/plugin-cache-currency.py` 全文; `aria-orchestrator/docker/aria-runner/Dockerfile` 的 FROM / ENV; 主仓 `72cb02b` / `a99dd8d` 与 aria `268da8f` 的发版文件清单 (16 个版本点与 6 个发版文件与 Impact 一致)。
- **上一轮与执笔材料**: R3 聚合报告全文; R3 qa 席报告全文; R1 / R2 聚合报告的 critical 行 (校准严重度); `v4-writer-report.md` 全文; `writer-v4-proto/` 的 README、`patch_l1.py` / `patch_l3.py` 的变体清单与关键段、`fuzz_mask.py`、`timing.py` 头部、`mut_summary_v4.txt` 与 v3 汇总格式 (用来统计「从未被任何坏实现转红的守卫行」)。
- **未读**: 四份研究笔记 (只 grep 了 `1400` 一项); R3 其余四席报告原文; 10CG/Aria#199 的 `detailed-tasks.yaml` (本轮只跑了它的守卫命令, 见下)。

### 实跑核验 (三态摘要)

- **基线 (独立复现)**: `WPA_BASH32=<真 3.2.57> python3 baseline_probe.py <副本>/aria`, 非 root, rc 0, stderr 空, stdout 86047 字节, sha256 前 16 位 `e588f9e8a57ed720`, 与执笔 / 主控的值和 evidence 内嵌块逐字节相同。baseline-failing 0/202、doc-sync 0/25、reverse-guard 72/72、allow-guard 67/67、known-limit 35/35、zero-regression 9/9 (30a 按设计 n/a), 基线形态 `holds`。
- **目标原型 (我重建)**: hook 指纹 `d94ddf4d6906734f` / `cf2dd857823baf79` 与执笔相同; 带 `WPA_BASH32` 与 `WPA_REQUIRE_ALL=1` 全量复跑, stdout 83988 字节、sha256 前 16 位 `7360938f57ee82d0` (与执笔的 final_T 逐字节相同): baseline-failing 202/202、doc-sync 25/25、reverse-guard 72/72、allow-guard 67/67、known-limit 35/35、zero-regression 9/9, 410 行 yes + 30a n/a, 目标形态 `holds`; 29a / 29h 50/50, 29b / 29i 584/585 (唯一 FAIL = 测试内 SC-13 无 git 伪影), 31a patterns=149, 31b census 64 = 64, 32c / 32d 在 361 个 hook-direct 行上一致 (en_US.UTF-8)。即「基线红 / 目标绿」两态没有一行说谎。
- **手写、不经探针的复核**: 18 条 L1 命令 (baseline-failing 两个方向、reverse-guard、allow-guard 各取样) 与 15 条 L3 输入, 三态与探针一致 (例: 基线 `cat /etc/forgejo/app.ini` / `ps aux` / `pgrep -af curl` / `docker top abc` / `f=…app.ini; sed … "$f"` 全部 exit 0, 目标全部 exit 2; 基线 `python3 -c "…os.environ.get('DATABASE_URL')…"` exit 2, 目标 exit 0; `cat .env` / `printenv` / `dict(os.environ)` 两侧均 2; L3: 基线对 Read 信封的 AWS 值、`{"token":…}`、`JWT_SECRET = <b64>`、`Authorization: token`、`--token=`、NUL 分隔环境全部静默, 目标分别报 `aws-access-key-id` / `json-credential-field` / `kv-secret-assign` / `auth-header-token` / `cli-secret-flag` / `env-line-secret-keyword`)。
- **Rule #7 自扫 (SC-15 15e / 15f / 15g 的独立复核)**: `proposal.md`、`baseline_probe.py`、`baseline-evidence.md` 各当 Bash 输出与 Read 结果喂基线与目标原型两个 `secret-scan.sh`: 12/12 静默。
- **误拦面**: 我自选的 62 条日常命令 (`kubectl top`、`docker stats`、各种只出 pid / 名字的 `ps` / `pgrep` / `top -bn1`、`cat /proc/cpuinfo`、`python3 -c` 取版本 / json、`ssh host uptime`、`watch 'df -h'` 等) 与基线对比: 目标只新增 1 条拦截 —— `git diff HEAD -- custom/conf/app.ini` (`diff` 属打印型读取器表, 且 diff 输出确实带配置值, 属设计内拦截)。另 46 条 launcher / 包裹 / `ps` 变体 (`sudo --user=… ps aux`、`timeout --signal=KILL 5 ps aux`、`ps -eF`、`pgrep --full -a` …) 目标全拦, 只放行 `ps -ely` (其 CMD 列是 comm, 正确)。
- **坏实现 (我自己写的, 对目标原型单点改动)**: 见下表 (「红」= 转红的行, 「0 行红」= 存活)。

| 坏实现 | 跑的行 | 结果 |
|---|---|---|
| `nul_off` / `nul_delete` / `nul_space` (W1 的 NUL 处理缺 / 删除 / 换空格) | SC-1…3 | 1c / 1d 红 (actual `kv-secret-assign=1` / `=1` / `=3`, 期望 `env-line-secret-keyword=3`) |
| `oldkey_drop` (删 `webhook_secret\|encryption_key`) | 7k | 红 8/10 |
| `drop_extract` (删 `tool_result` 两分支) | 2e 2f | 红 |
| `fp_le16` / `noshasum` | 12n / 12o | 红 |
| `wl_on_bearer` / `dotted_on_envline` | 7m / 7l | 红 |
| `ent_range` (熵下限用 glob 范围) | SC-9 / 10 + 32d (真 3.2, en_US) | 32d 红 `3 of 37 rows differ: SC-9:9p SC-10:10a SC-10:10k` |
| `r_myempty` (删「有效条目为零」守卫) + 执笔 `ext_emptypat` | 20o-20q | 红 |
| 执笔变体抽样 `drop_pid:7` / `drop_pid:2` / `tdrop_remote:watch` / `remote_env_split:ssh` / `vx_eval` / `ext_nostrip` / `tight_ini_literal` | 22bp / 22bp / 22bm / 22bo / 21z / 19ac / 16r | 全红 |
| `mask_nodq` / `mask_nosq` (掩码缺双 / 单引号状态) | SC-19 + SC-20 | 红 (19z / 19aa) |
| **`mask_noesc_q` / `mask_noesc_all` / `mask_noansi`** | SC-19 + SC-20 (46 行) | **各 0 行红 → M1** |
| **`w12_once`** (只替换每个子串第一处) | SC-23 (9 行) | **0 行红 → m1** |
| **`readface16`** (删 16 个基线 Read/Edit 备选) | SC-16…25 (197 行) + 现有 guard 套件 | **0 行红, 套件 584/585 (仅已知伪影) → M2** |
| `ell_lastchar` (按字符判 `…` 后缀) | SC-4…11 (C.UTF-8) | 0 行红; `WPA_LOCALE_B=C` 时 32d 红 → m3 |

## Findings

### Critical

无。

### Major

**M1** — id `0a8380fd` / major / issue / implementation
scope: `proposal.md What.W9` (R3 簇 T 的残余; 沿用该簇四元组)
summary: W9 的引号感知阶段切分 (`_sg_ext_mask`) 对「反斜杠转义」与「`$'…'`」两个状态没有任何行钉住 —— 19z / 19aa 的 8 个形态只含**未转义**的双引号 (python / node) 与单引号 (awk) 程序。三个自然的坏实现在 SC-19 + SC-20 的 46 行上 0 行红, 却对「内建 `app.ini` 行必拦」的同形命令放行, 与 W9 自己写的「与内建 `app.ini` 行对同形命令的判定一致」相反。
证据 (`proposal.md:164` 逐一列出「引号 (单引号、双引号、`$'…'`) … 引号 / 转义状态机与内建 `_sg_split_top` 同一套」; 探针形态在 `baseline_probe.py:1372-1376`, 19z 行在 `:1377-1378`, 无任何 `\"` 或 `$'`; 目标原型的掩码在 `secret-guard.sh:632-659`)。我对掩码函数各改一处造三个坏实现: `mask_noesc_q` (双引号状态删去 `\` 分支)、`mask_noesc_all` (三处 `\` 分支全删)、`mask_noansi` (删去 `$'` 进入 ANSI-C 状态的分支)。直接喂 hook (`CLAUDE_PROJECT_DIR` 指向含 `/srv/billing/conf/prod.toml` 的清单; 退出码依次 = 内建 `app.ini` 行 / 目标原型 / `mask_noesc_q` / `mask_noesc_all` / `mask_noansi`):
```
python3 -c "print(\"a\"); print(open('<P>').read())"                      2 / 2 / 0 / 2 / 2
python3 -c "print(\"a;b\"); print(open('<P>').read())"                    2 / 2 / 0 / 0 / 2
python3 -c $'import os; print(\'x\'); print(open(\'<P>\').read())'        2 / 2 / 2 / 2 / 0
node -e $'const fs=require(\'fs\'); console.log(fs.readFileSync(\'<P>\'))' 2 / 2 / 2 / 2 / 0
```
探针: `runrows.sh <坏实现> SC-19,SC-20` 三个各 `rows: 46 ; non-yes: 0`; 对照 `mask_nodq` 使 19z 与 19aa 转红, `mask_nosq` 使 19z 转红 —— 即引号**种类**钉住了、**转义与 ANSI-C** 没钉住。执笔的 `fuzz_mask.py` 差分 (4000 随机串, 字母表含 `$'` 与 `\`) 恰好覆盖这两个状态, 但它是原型上的一次性证据, 不是验收的一部分。
失败场景: 实现者没有复用 `_sg_split_top` 而是新写一个简化的引号跟踪 (只认成对的 `'` `"`) → 探针 + 套件全绿 → 采用方列入的路径经 `python3 -c "…\"…; …open('<路径>')…"` (AI 写的单行程序里转义内层双引号极常见) 读取时, 扩展按错误的阶段边界放行, 而内建 `app.ini` 同形命令被拦; 扩展失效是静默的 (W9 已知限制)。
建议修法: (a) 19z 增形态 (内建 `app.ini` 与扩展两侧各跑): 双引号程序内 `\"` 之后接 `;`、`\"a;b\"`、`$'…\'…'` 内含 `;` (python 与 node 各一)、引号外 `\"` 后接带 `;` 的引号程序; (b) Tasks 1.8 的越界类清单加 `mask_noesc_q` / `mask_noesc_all` / `mask_noansi` 三个; (c) 或在 W9 写明「掩码**复用**内建 `_sg_split_top` 的扫描函数, 不另写状态机」, 使该机器只有一份。按字面第三条 (「验收放过一个错误实现」) 可升 critical; 与 R3 同类先例 (`eb350937`、`0a8380fd`, 席位自评 major、主控未升级) 保持口径定 major。

**M2** — id `eb350937` / major / issue / testing
scope: `baseline_probe.py` (R3 簇 M 的残余; 沿用该簇四元组)
summary: W8.3 在原位改写 Read/Edit 面正则行 (`secret-guard.sh:641`, 32 个基线备选), 但 W14「原位改写通则」(`proposal.md:239`) 的清单只列了 `/proc` 两行、`python3 -c` / `node -e` 两行、tight 判定三处, 漏了这一行; 该行 32 个基线备选里 **16 个没有任何用例 (现有套件 + 探针) 会因删除而转红**。删掉这 16 个的坏实现通过探针 SC-16…25 全部 197 行与现有套件 584/585 (仅已知无 git 伪影) —— 基线拦的 Read/Edit 由拦变放。
证据: (1) 静态 —— 对现有 `secret-guard.test.sh` 的 39 条 Read/Edit 用例 (`read_case` / `edit_case` / 内联 JSON) 加探针 canary 2 条, 逐个备选核「是否存在一条应拦用例只被该备选命中」: 16 个没有 —— `/credentials?/`、`id_rsa$`、`id_ed25519$`、`id_ecdsa$`、`\.gpg$`、`\.age$`、`\.pfx$`、`\.jks$`、`\.tfstate\.backup$`、`kubeconfig$`、`gcp[_-]key.*\.json$`、`firebase.*\.json$`、`\.ssh/known_hosts$`、`/secret[_-]token`、`/master[_-]key`、`/encryption[_-]key`。(2) 动态 —— 目标原型删去这 16 个备选、其余字节不变 = 坏实现 `readface16`; 16 条只命中各自备选的 Read 路径 (`/srv/backup/id_rsa`、`/home/u/cert.pfx`、`/home/u/keystore.jks`、`/srv/infra/terraform.tfstate.backup`、`/home/u/.ssh/known_hosts`、`/srv/master_key` …): 基线 2 / 目标 2 / 坏实现 0, 16/16。(3) 探针 `runrows.sh <readface16> SC-16,…,SC-25` → `rows: 197 ; non-yes: 0`。(4) 现有 guard 套件 (目标原型版, 无 git 副本) 跑在 `readface16` 上: `PASS: 584 / 585, FAIL: 1` (唯一 FAIL 是 `SC-13: 头注释计数同步`, 与目标原型自身一致)。
失败场景: 实现者为并入 `app.ini` 名字组而重写这条 700 字符的正则 (拆行 / 抽成变量 / 手抖截断), 丢掉任一尾部备选 → B.2 的探针与套件全绿 → 发版后 `Read` / `Edit` `*.pfx` / `*.jks` / `known_hosts` / `firebase*.json` 等由拦变放, 无人察觉 —— 正是 W14 通则自己警告的「合并 / 重写分组时丢成员, 只看新增形态的 SC 看不见」。
建议修法: (a) W14 通则 (`:239`) 把 Read/Edit 面正则行列为第四个原位改写项; (b) SC-18 增一行 `reverse-guard` (例 18j): 对 32 个基线备选各取一条只命中该备选的路径, Read 全量 + Edit 抽样, 期望 exit 2 (基线 32/32, 表在探针里写一处, 循环即是行); (c) Tasks 1.8 缺项类清单加「删掉 Read/Edit 面正则的任一备选」; (d) 实现上以变量保持原串逐字节不变 + `|` + 新名字组。口径同 M1。

### Minor

**m1** — id `65fb3fcf` / minor / issue / testing
scope: `proposal.md SC-23`
summary: SC-23 只钉「四个单键读取子串各出现一次」(23b 五条命令里同一子串从不出现两次); W12 也没有规定「同一子串多处出现全部归一」, 且「BLOCKED 文案里 `Command was:` 仍是原文 (SC-25 不变)」没有可证伪的锚点 —— SC-25 的归一化 (`norm_blocked`) 恰好把 `Command was:` / `Triggering segment:` 两行替换成占位。
证据: 把目标原型 `_sg_judge_one` 里四条归一化循环 `while` 改成 `if` (每个子串只替换第一处) → SC-23 `rows: 9 ; non-yes: 0`; 直接喂 `python3 -c "import os; print(os.environ.get('A'), os.environ.get('B'))"`: 基线 2 / 目标 0 / 坏实现 2, `…os.environ['A'], os.environ['B']…` 同。
失败场景: 实现者单次替换 → 验收全绿 → 含两处同形单键读取的命令 (host / user / password 各读一次, 极常见) 仍被拦, 10CG/Aria#221 评论 25898 点名的「把使用者推向 `# guard:ack`」继续, 只修了单次读取形态。纯误报侧, 无检出回退, 故 minor。
建议修法: 23b 增「同一子串两处」两条; 删去或改写 W12 里「仍是原文 (SC-25 不变)」的锚点说法 (或另加一条不归一化 `Command was:` 的断言)。

**m2** — id `684e9a24` / minor / issue / documentation
scope: `proposal.md What.W9`
summary: W9 格式规则 (`proposal.md:163`) 逐条列了 CR / 首尾空白 / 注释 / 4–200 字节 / ASCII 字母数字, 没有提 UTF-8 BOM。Windows 工具 (PowerShell 5.1 的 `Out-File -Encoding utf8`、旧版记事本「UTF-8」) 写出的清单首行带 BOM, 首行条目静默失效; 10CG/aria-plugin#203 的报告环境就是 MINGW64。
证据 (目标原型, `CLAUDE_PROJECT_DIR` 指向各清单; 命令 `cat /srv/billing/conf/prod.toml`): 无 BOM 的同内容清单 exit 2; EF BB BF + 路径 + LF → **exit 0**; BOM + CRLF → **exit 0**; BOM + `# 注释` 首行 + 路径次行 → exit 2 (BOM 只破坏注释行, 条目仍生效)。
失败场景: 采用方在 Windows 上建清单, 第一条路径恰是最想保护的那条 → 静默不生效, 与 19ae (纯非 ASCII 条目被跳过) 同族但没有成文。
建议修法: 读取条目时剥首行 BOM (`LC_ALL=C` 下一行 sed), 并加一行 19m 同族的行; 或至少写入 W9 已知限制与 SOT §5.6 的「静默」清单。

**m3** — id `aa08f71d` / minor / issue / testing
scope: `proposal.md SC-32`
summary: 32d 的第二 locale 缺省 `en_US.UTF-8`, 仍是 UTF-8; 而 Layer 2 的 aria-runner 镜像 (`aria-orchestrator/docker/aria-runner/Dockerfile:32` `FROM node:20-bookworm-slim`, 全文无 `LANG` / `LC_ALL`) 里 hook 实际跑在 POSIX locale。按字符 (而非字节) 判断多字节后缀的写法在两个 UTF-8 locale 下一致, 只在 C / POSIX 下分叉, 默认 32d 看不见。
证据: 坏实现 `ell_lastchar` (`[[ "${v: -1}" == "…" ]]` 代替 `[[ "$v" == *"…" ]]`) —— SC-4 / 5 / 6 / 9 / 10 / 11 共 107 行在 C.UTF-8 下 0 行红; `WPA_LOCALE_B=C` 时 32d 转红 `3 of 63 rows differ: SC-11:11v SC-11:11x SC-11:11y`。目标原型在 `WPA_LOCALE_B=C` 下 SC-9 / 10 / 11 + 32c / 32d 全 yes, SC-19 / 20 / 32 (L1 扩展行) 在 C 下也一致 —— 只是验收覆盖缺口, 不是原型缺陷。
失败场景: 实现者用字符语义写 `…` 后缀判定 → 验收全绿 → 在 Layer 2 的 POSIX locale 里被截短的占位值不再被白名单放行, 恒告警 (只增误报, 无检出回退)。
建议修法: Tasks 1.1 / 1.10 把 `C` 作为 32d 的固定第三条腿 (无需构造, 总是可用), 与 `en_US.UTF-8` 并行; 一行改动。

## 上一轮对账

R3 聚合报告里 critical 为 0, 12 条 major 按主控记录归并为八簇 (括号内为席位编号):

| 簇 (键) | 状态 | 我核验的证据 |
|---|---|---|
| **Q** `4f713847` (tl/M1) NUL 分隔内容 | **closed** | W1 (`proposal.md:52`) 在提取命令替换内 `jq` 之后接 `tr '\000' '\n'`; 1c / 1d 基线 `silent … no`, 目标 yes; 我的 `nul_off` / `nul_delete` / `nul_space` 各使 1c / 1d 转红 (`kv-secret-assign=1` / `1` / `3` ≠ 期望 `env-line-secret-keyword=3`); 手写 NUL 分隔环境 (Read 与 Bash 两种信封) 基线静默、目标 `env-line-secret-keyword=2`。 |
| **M** `eb350937` (qa/M1 · cr/M2) · `1c49d896` (ba/M5) · `8fbbee80` (ba/M2) 覆盖面 | **partially closed** | 已关闭部分: 7k (10 键) / 2e·2f / 12n / 12o / 19ac / 22bo / 7l·7m / 22bm·16r 逐项由我自己的坏实现转红 (见上表); 残余: **M2** (Read/Edit 面正则行的原位改写没有重放)。 |
| **P** `05982c10` (qa/M2 · cr/M1 · ba/m3) 关闭关键字检查 | **closed** | 在临时仓里逐字运行 Impact 三步命令: 干净范围 `1 / rc=0` + `rc=0,1`; 带 `Closes #221` 的提交 `3:Closes #221 / rc=0,0`; 错起点 `rc=128` / `rc=128,1`; 空起点 `0 / rc=0` (按 Spec = 没跑成); 非仓路径 `rc=128,1`; 空范围 (HEAD == merge-base) `0 / rc=0`; PR 文本三态 `rc=1,` / `rc=0,1` / `rc=0,0`。`closing #154` 不被误判、`Closes #1540` 不被误判。同类 #199 守卫命令在真仓只读运行: `rc=0`, 其前无输出 (通过)。 |
| **R** `28af0372` (qa/M3) 有效条目为零 | **closed** | 20o / 20p / 20q 在场; 我自己的坏实现 `r_myempty` (删 `[[ -n "$out" ]] \|\| return 0`) 与执笔 `ext_emptypat` 都使三行转红 (Read / Edit 由 0 变 2)。 |
| **E** `44b5bb44` (qa/M4) locale | **closed** (外加 m3) | W2 字符类段 + 32d; 我的 `ent_range` 在 32d 转红且点名 9p / 10a / 10k (与我 R3 独立发现的分叉一致); 目标原型 32d 在 361 行上一致。覆盖仍缺 C / POSIX 腿 → m3。 |
| **S** `8d258b19` (ba/M1) 不执行不变量 | **closed** | 19ab / 21z / 23i / 7n 在场; 抽样 `vx_eval` 使 21z 转红 (`1/5 as expected`, 4 个诱饵被创建); 其余三条沿用执笔汇总, 未复跑。 |
| **T** `0a8380fd` (ba/M3) 阶段切分不识别引号 | **partially closed** | 单 / 双引号状态已钉 (`mask_nodq` / `mask_nosq` 红); 转义与 `$'…'` 状态未钉 → **M1**。 |
| **K** `ac42f607` (ba/M4) `/proc` pid 位置 | **closed** | 22bp 在场; `drop_pid:7` (`$$` / `$!`) 使 22bp 红 `5/10`、`drop_pid:2` (glob) 红 `7/10`; 22bf / 22bh 钉放行侧。 |

R3 全部 minor: 我抽核均已落地 (Tasks 1.12 的 `OK ` 判据与 `plugin-cache-currency.py` 真实输出一致; 12k 的 38 个 tag 逐类相加 22+3+1+1+3+1+4+1+1+1 = 38; 28c / 28d 的 `NO_COUNT` 正则能抓 `37 patterns` / `~12 key-shape forms` / `6 new tags`; 28a / 28b / 28e / 28f / 28l 的「全部旧片段须消失」判据在探针里是 `all(o not in t …)`; `K = 50` 已改为实跑总数)。**我认为仍未处置的 minor**: 无 (新发现的见 m1-m3)。

## 对执笔人自报薄弱点与请裁项的表态

执笔报告 §6:
1. 原型不是实现 / 坏实现自构 (同源盲区): **可接受作为披露**; 我的独立坏实现在 535+ 个坏实现之外仍找到 M1 / M2 / m1 / m3 的存活者, 印证 Tasks 1.8 的非作者对抗 review 不可省 —— 但 M1 / M2 应先落成行, 不要全部留给 1.8。
2. 体量 (+21.7% / +19% / 新增 28 行): 可接受; 本轮残余确实集中在新文字与新行的接缝 (M1) 与旧清单的接缝 (M2)。
3. 验收前置变多 (第二 locale / 非 root / 真 bash 3.2): 可接受; `setpriv --reuid --regid --clear-groups` 在本机存在, 我以 uid 1000 运行、未能在 root 下实测, 与执笔相同。
4. 回归复跑是精化的 (只跑 v3 里红过的行): 可接受, 判据「红过的必须仍红」是对的; 我抽样的 13 个对账坏实现都转红, 与汇总一致。
5. 等价变异 (4 + 14): 可接受; 我核了 4 个包裹的理由 —— 基线 `docker exec abc env` / `kubectl exec pod -- env` / `podman exec abc env` / `lxc exec c1 -- env` / `docker compose exec web env` 均 exit 2, 而 `nomad alloc exec` / `pct exec` / `ssh` / `sh -c` / `watch` 基线 0、目标 2 (与 22bo 基线 `10/22` 吻合)。
6. 时档是单机比值: 可接受 (「越界上呈、不放宽」符合 Rule #10); (f) 比值 1.46–1.7 靠 100 ms 地板, 我的提醒仍在风险节。
7. 新增 / 反转的已知限制与误拦面 (19ae、22bj 更宽、`sh -c printenv` 反转): 可接受, 均成文并有行; 我的 62 条日常命令只新增 1 条设计内拦截。
8. 差分核对范围: 可接受; 但见 M1 —— 差分覆盖的恰是验收没钉的状态。
9. L3 的 7n 防的是「去引号捷径」: 可接受保留 (低成本的绊线; 事实上恒绿, 执笔已承认)。
10. 证据运行在高负载主机上: 可接受; 我的两次全量运行各约 15 与 45 分钟 (主机负载 10–38), 逐字节结果与负载无关。

执笔报告 §7:
- 甲 (技术级 21–30): 同意 21 (NUL 纳入)、22 (`/proc` pid 闭集)、23 (`sh -c` / `watch` × env 纳入)、25 (不执行不变量与 4 个诱饵行)、26 (字符类与 locale; 建议并入 C 腿, 见 m3)、27 / 28 / 29 / 30。**24** 的「引号感知阶段切分」同意方向, 但须按 M1 补转义与 ANSI-C 的行; 「纯非 ASCII 条目被跳过」作为默认可接受, 建议同时处理 BOM (m2)。
- 乙 (Rule #10 自作主张): (1) 回归复跑只跑红过的行 —— 可接受; (2) 同批「同族兄弟位置」改动 —— 可接受, 但注意「同族」清单漏了 Read/Edit 面正则的原位改写 (M2); (3) 「没有新增 hook 机制」—— 基本成立, 但 `_sg_ext_mask` 是约 30 行的新 bash 状态机 (经主控裁定 #2 授权), 它正是 M1 所在; (4)「选纳入」三处 —— 可接受; (5) 不交付 `tx_*.py` —— 可接受。
- 丙 (未采纳的备注): 同意不采纳 (1)(2)(4) (W5 的 `source` 取自 harness 的 `tool_name`, MCP 工具名字符集受限); (3) 建议在 10CG/aria-plugin#154 关单评论里一句披露「未在 MINGW64 / macOS 验证」(零成本); (5) 同意不采纳; (6) **不接受只记在报告里**: 见风险节第 1 条, 该决定在 Spec 里没有任何登记。

## 风险 / 疑问 (不计入 finding)

1. **公开镜像上的未修绕过配方没有 owner 门**: 建议开单 7.1 写了「约 1400 个空段使 hook 超时后命令被放行」, 研究笔记 `research/secret-guard.md:20,371` 还有 `:;` 空段与 `pg_dump --version` 的活体细节, 两者都随 feature 分支入仓; 一次性授权覆盖 feature 分支推送 (含 GitHub 镜像), 推送不可撤回。Tasks / 待复议都没有「首次推送前由 owner 决定该配方是否随分支公开」这一等待点。只删 proposal 里的数字不够, 笔记同在分支上。这是 R3 qa 与 km 已提的风险, 执笔未采纳, 我仍认为应在首次推送前由主控 / owner 显式裁。
2. **SC-30 时档的判定靠人读比值**: `timing.py` 只打印比值与活性, 无上界与退出码; (f) 比值 1.46–1.7 靠 100 ms 地板才过 1.5 的比值门, (g-b) 2.03 距 2.5 约 20%。Spec 已如实写明「判据由上面的上界给出」, 但「SC-30 全绿」因此是一步人工判断。建议给 `timing.py` 加上界与 rc。
3. **Layer 2 (aria-runner) 在 POSIX locale 且无人值守**: 见 m3; 另 Impact 没写新拦截对 Layer 2 的影响 —— 我 grep 了仓内 skills / orchestrator / `.aria` 脚本, 没有会被新进程表规则拦下的 `ps aux` / `pgrep -a` 等指令 (只有文档文字提及), 所以不是回退; 但无人值守时 `# guard:ack: <≥8 字符理由>` 是 AI 自助的, 被冻结文案拦住后转向 ack 的风险 (待复议 5 / 2) 在 Layer 2 比在人机会话里更硬。
4. **行内 `# guard:ack:` 对新增 Bash 拦截 (进程表 / `app.ini` / 扩展 / 变量间接) 没有行钉住**: 我在目标原型上逐个验证有效 (带理由 exit 0, 不带 exit 2), 且 ack 处理在 `:715-733`、先于全部 `risky_patterns` 与第二遍, 自然成立; 只是日后把扩展调用提到 ack 之前的实现不会被探针发现。可加四条行。
5. **BSD / macOS / Windows Git-Bash 语义仍未验证**: `grep -F -f` 对空模式文件、`sed -E` 的 `^` 在分组内、`pgrep -fl`、MINGW64 下的每 Read 成本与 `CLAUDE_PROJECT_DIR` 路径形态 (沿用 R3)。
6. **W1 设计取舍文字不精确 (不影响实现者)**: 「不选 B' 把 NUL 换成空格: 行首锚丢失, 修不了」(`proposal.md:53`) —— 我的 `nul_space` 在原型上仍被 `kv-secret-assign` 检出 (`kv-secret-assign=3`, 只是 tag 变了, 且 8–15 字符的值会漏)。
7. **探针的函数注入器靠命名与排版约定** (`^_sg_ext_*() {` 起行): 排版不符的辅助函数里的故障不被 20i–20k 覆盖, 20m 只保证两个入口函数在场。Spec 已写明约定, 仅提示。
8. **dogfood 观察**: 写本席测试脚本时, 现行 L3 对含 `{"client_secret":"' + rnd(32) + '"}` 拼装代码的文本告警过一次 (已知误报类, 同 W3 / W7), 现行 L1 对 heredoc 里含 `.env` 字样的命令拦过一次 (同 22bj); 都与 Spec 成文的误报类一致。

## Verdict

**PASS_WITH_WARNINGS** — counts: **0C/2M/3m**。

Vote: **REVISE** (有 major)。

## 是否足以进入 A.2

不足以: 仍有 2 条 major (M1 给 `_sg_ext_mask` 的转义与 `$'…'` 状态补行或改为复用内建扫描函数; M2 把 Read/Edit 面正则行列入「原位改写通则」并补 32 个基线备选的重放行), 均为补行 / 补一条清单项, 不涉设计取舍; 六个簇已确认关闭, 基线 / 目标两态在我独立全量复跑里没有一行说谎。
