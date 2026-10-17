---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-06T16:33:00.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 backend-architect 报告 — secret-net-l3-and-bypass-paths (proposal v3 @ c0a6654)

> 视角: 实现可行性与正确性。结论: R2 七簇里 A / L / M / N / O / P 六簇在 v3 确已收口 (逐簇实跑复核, 见「上一轮对账」); K 簇**部分**收口 (R2 列出的项全部闭合, 但 `/proc` pid 位置枚举仍漏掉最常见的写法)。本轮新增 0 critical / 5 major / 5 minor。5 条 major 的性质: 3 条是「验收对一类坏实现没有鉴别力」(M1 / M2 / M4: 本席自构的三个非作者坏实现各自让全部对应 SC 行与未改动目标逐项一致地全绿), 2 条是「Spec 文字规定的语义与 W8 / 基线约定不一致」(M3 / M5)。修法都小 (补一句规定加几行用例), 不涉及设计重做。

## 已实读文件

**被审 (全文)**: `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 1-425。`baseline_probe.py` (2095 行) 读了头注释 1-60、SC-16 / 17 / 18 / 19 / 20 / 21 / 22 / 33 的行定义与 20g / 形态行 / 退出码逻辑 (1236-1275、2040-2095) 以及按需检索的全部命中, **未逐行通读**; `baseline-evidence.md` 读了 1-31 (环境与 bash 3.2 构建配方) 与 427-437 (SC-29 / SC-32 行), 其余按探针 stdout 的逐字节包含关系采信 (主控已核)。

**必读材料**: 三个 issue 正文与评论 (全文); 决策单 (全文); CLAUDE.md #6 / #7 / #10 与多远程两条 (上下文原文); R2 聚合报告 (全文含「主控记录」); 本席 R2 报告 (全文); 执笔 v3 返修报告 §0-§7 (全文); `cc-hooks.md` 1-140; `secret-scan.md` / `secret-guard.md` / `precedent.md` **未读** (背景材料, 以源码与二进制实测为准)。

**源码与规范 (aria `268da8f` / standards `2bc1c4c`)**: `hooks/secret-scan.sh` 1-377 全文; `hooks/secret-guard.sh` 1-1120 全文 (重点 `_sg_safe_to_split` / `_sg_compute_credit` `:386-487` / Read·Edit 面 `:631-694` / `risky_patterns` `:736-1009` / `_sg_judge_one` 与逐段入口 `:1029-1120`); `hooks/hooks.json` 全文; `hooks/tests/*.test.sh` 的 `HOME=` 与 `rm -rf` 用法; `standards/conventions/skill-benchmark-exemption.md` 全文; `secret-hygiene.md` 的 `:23 / :285 / :287-288 / :319 / :402-403`; `aria/VERSION:164`; `.aria/state-checks.yaml` 的 `plugin-cache-currency` 条; `.aria/pat-inventory.yaml:11-21`; `aria-orchestrator/docker/aria-runner/Dockerfile` (无 `USER` 指令)。执笔产物: `writer-v3-proto/timing.py` 与 `README.md` 全文、目标态原型 (`exp/writer-v3b/work/t3`) 对基线的 `secret-scan.sh` 全量 diff 及 `secret-guard.sh` 的 W8 / W9 / W10 / W11 / tight 段。

### 实跑验证 (命令与结果; 全部在 `$A` = `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/audit/post_spec-R3-backend-architect` 内; `$A/aria` + `$A/standards` = 真仓 `268da8f` / `2bc1c4c` 的 cp -a 副本; `$A/target` = 执笔目标态原型的 cp -a 副本; `$A/spec` = 被审目录副本; 值全部运行时 `secrets` 生成、只经 stdin、`capture_output=True`, 只打印退出码 / tag / alert-or-silent)

- **V1 (W1 / SC-1)**: Read 真实信封 `{type,file:{content,…}}` + 运行时生成的 AWS key id 形文本: 基线 silent / 目标 `aws-access-key-id=1`; Read 旧合成信封、Bash 真实、Write 真实 三种基线与目标都 `aws-access-key-id=1`。成立。
- **V2 (簇 A)**: 既有键 `{"password":"<值>"}`: crypt 哈希形 / `$`+11 位小写数字 / `$`+11 位大写数字 / `$(`+14 位+`)` / 18 位+ASCII `...` / `<` 开头不闭合 → 基线与目标**都** `json-secret-field=1`; 18 位+U+2026 / `<…>` / `${…}` / `{{…}}` / `[REDACTED]` / wrapper 占位 / 8 个 `*` / `FAKE_` 前缀 → 基线告警、目标静默; 小写 `fake_` 仍告警。新 tag (`"token"`, ≥16 两类): `$`+17 位、crypt、ASCII `...` 结尾仍 `json-credential-field=1`, U+2026 结尾与 `<…>` 静默。
- **V3 (W4 指纹, 独立重算)**: 10 个 tag (postgres-url 口令分量 / bearer 末词 / x-api-key 冒号后 / gcp key id 引号内 / cf-access / auth-header / cli 旗标 `=` 后 / kv 去引号 / env-line `=` 后 / aws 整 span) 的日志 `fp=` 全部等于我在 Python 里对「Spec 表所列凭据本体」算的 sha256 前 8 位; 日志恰 9 字段; 12 位值 → `fp=L12` 且日志不含其哈希; app.ini 五值 → `jwt=1 kv-secret-assign=4`、fp 顺序「jwt 先、其余按文本序」; 11 值恰 10 项; PATH 里只留无 sha 工具的符号链接 → `fp=-` 且告警与日志照常; 值与任意 8 字符片段都不在日志行里。成立。
- **V4 (簇 N)**: Read 与 Write 各 7 种敌意 `file_path` (良性 / `)`+祈使句 / 换行+伪造 hook 行 / 引号反引号 `$` / U+202E / 5000 字符 / 控制字符含 ESC) 共 14 次: additionalContext **全串等于**「基线文本 + ` (tags: aws-access-key-id=1; source: <Read|Write>)`」14/14; 路径任何字节都没进输出。
- **V5 (Spec 的 bash 论断)**: 真 bash 3.2.57 `x=abc; r=Z; echo "${x//b/"$r"}"` → `a"Z"c` (5.2.15 → `aZc`); 前后缀拼接式两者都 `aZ&c`; `[[ "$v" =~ ^<[^<>]*>$ ]]` 在 3.2 **与 5.2** 都 `syntax error in conditional expression: unexpected token '<'`, 正则放进变量两者都可; `${s#*"$pat"}` 对 4000 字节串 200 次 7.87 s (user 5.44 s) vs 前后缀切片 0.20 s。W2 / W10 的论据全部成立。
- **V6 (簇 L, Tasks 1.12 诱饵腿)**: L1 直调 (基线 / 目标): 腿 1 的 `python3 -c "…token_urlsafe(32)…"` = 0 / 0、腿 2 的写诱饵文件命令 = 0 / 0、Read 诱饵路径 = 0 / 0 (三者都不会被新旧 L1 误拦, 腿可执行); 腿 3 `ps aux | head -c 0` = 0 / 2; 腿 4 Bash `cat /nonexistent-wpa-probe/forgejo/app.ini` = 0 / 2、Read 同路径 = 0 / 2。纯 shell 实跑: 腿 3 输出 0 字节、腿 4 只有 ENOENT, 即 hook 未生效时无害。L3 腿: `JWT_SECRET = <token_urlsafe(32)>` 经 Bash / Read 信封 → 基线 silent / 目标 `kv-secret-assign=1` 且 additionalContext 含 `(tags: kv-secret-assign=1; source: Bash|Read)`; 100 次抽样 (含以 `-` `_` 起头的值) 0 次未检出。
- **V7 (簇 P)**: 把 Impact 里的关键字检查命令原样取出, 在临时 git 仓里对 10 条正例 (`Closes #154`、`closes: 10CG/aria-plugin#203`、`Fixes 10CG/Aria#221`、URL 形、大写 `FIX`、双空格、制表符、`(resolves #203)` 等) 全部 `rc=0`, 对 8 条反例 (`Refs …`、`Prefixes #154`、`closed-loop #154`、`disclosed #154`、`fixes #1544`、`closes #2210`、`Closes aria-plugin#154` 等) 全部 `rc=1`。Aria#199 接缝守卫命令在真仓: 无输出、`rc=0` (= 通过); 非 git 目录不带 `-C` → `rc=128` (= 没跑成)。
- **V8 (簇 K)**: R2 三席点名的 22 条写法 (`ps -aux|-ax|-x|-ux|-au`、`-eO`、`pgrep -f x | xargs ps -fp`、`unbuffer|eval|timeout 5 ps aux`、`sudo -u svc ps -ef`、`/bin/ps`、`/usr/bin/sudo /bin/ps`、`then|do` 关键字位置三条、`podman top|ps --no-trunc`、`python3 -c`/`node -e` 读 `/proc/self/environ`) 基线全 0、目标全 2; 15 个 launcher × 8 个形态族 (ps / pgrep -af / pstree -a / top -c / docker top / docker ps --no-trunc / `cat /proc/1/environ` / `ssh h 'ps aux'`) 共 120 条目标全 2; 放行侧 (`ps -e`、`-eo pid,comm`、`-p 1`、`-u dev`、`pgrep -l|-f`、`pstree -p`、`top -b -n1`、`docker ps`、`systemctl status`) 目标全 0。过拦 / 漏拦的新发现见 M4 / m1。
- **V9 (簇 O 时档, `timing.py` 同次运行交错 A/B, N=5 取 CPU 最小; 主机负载 2-18 波动)**: (f) Bash 0.048→0.073 s (1.52)、Read 0.043→0.072 s (1.68), 均在 `1.5×max(基线,100ms)=0.15 s` 内且活性断言 `ok(_sg_ext_pass)` / `ok(_sg_ext_path_pass)`; (f0) 0.052→0.057 / 0.051→0.053 (1.10 / 1.04); (i) 900 KB bearer 0.617→0.799 (1.29)、600 KB JSON 口令 0.770→0.949 (1.23), 仍告警; (h2) 150 段 + 末段读 dotenv 2.215→2.627 (1.19) 且 `live-calls=ok()` (内建先判, 扩展与第二遍零调用); (g) 满额 16×8 档 1.453→2.913 (2.00)、`live-calls=ok(_sg_vx_pass)`; w1 Read 4 KB / 60 KB / 180 KB 稠密 INI 0.135→0.386 / 0.162→0.423 / 0.141→0.668。与 Spec 数字同量级。(h1 全部放行档 2.157→5.041, 比值 2.34, 与 Impact 自述「引用越密越近 2×」一致, 不在任何档的判据内, 见风险。)
- **V10 (簇 M / 簇 A 的非作者缺项坏实现, 本席自选成员)**: 8 个缺项类: json 名表去 `PrivateKey` → 仅 4p 红; kv 关键字去 `ENCRYPTION_KEY` → 仅 5n 红; cli 旗标后缀去 `access-key` → 仅 6i 红; W8 读取器去 `column` → 仅 16q 红; W9 读取器 (扩展拷贝) 去 `fold` → 仅 19u 红; W11 launcher 去 `ionice` (规则行) → 仅 22aw 红; W12 去 `.environb[` → 仅 23b 红; 基线 `/proc` 读取器组去 `rev` → 仅 22aj 红。7 个分类器类: 去 `{{…}}` 模板 → 11h/11v/11x/11y 红; 去 `NOT_REAL` → 11x/11y; 去 `…` 结尾 → 11v/11x/11y; 尖括号写宽 (允许内部定界符) → 7j; 掩码去 `X` → 11x; 熵下限改「必须含数字」→ 4o/4t/10b; span 上限 200 改 300 → 11w。**15/15 全部被其对应行转红**。
- **V11 (L3 误报电池, 29 种常见良性文本: git log SHA、sha256sum、docker digest、npm integrity、go.sum、UUID、k8s Secret 小写键、GH Actions secret 引用、terraform sensitive、`.env.example`、curl bearer 变量、`sk-...` 文档示例、`os.environ[...]`/`process.env`、HF 配置、compose `_FILE`、markdown 表、CLI help、AWS UserId、docker inspect Env、证书 PEM 正文、ssh 公钥、无 eyJ 的三段点分等)**: 相对基线**新增告警只有 2 种**, 均是 Spec 已成文的已知误报类 (`TOKEN_ID: <uuid>` → `kv-secret-assign`; 文档里的 `Authorization: Basic <b64>` 示例 → `auth-header-token`)。成立。
- **V12 (W1 设计选项 A 的前提「stderr 只装 harness 提示」)**: 主会话 transcript 里 195 条 Bash `toolUseResult`, 28 条 `stderr` 非空, **全部**只是 `Shell cwd was reset to /home/dev/Aria`; 本会话命令的 stderr 文本出现在合并输出里 → stderr 已并入 stdout, 选项 A 成立。
- **V13 (平台事实)**: `claude` 2.1.285 二进制 `grep -a -c updatedToolOutput` = 14, 描述原文 `Replaces the tool output before it is sent to the model` 在场 → W5 / 28l / 28m 的事实订正成立。
- **V14 (SC-15 独立复核)**: 把 `proposal.md` / `baseline_probe.py` / `baseline-evidence.md` / 目标态两套测试与两个 hook 各当 Bash 输出与 Read 结果喂目标 L3: 14/14 静默; 基线 `secret-scan.test.sh` 仍告警 (W7 的动机); 两个 SC-33 归因文件在目标 Read 下告警 (`kv-secret-assign=1` / `json-credential-field=1`+既有键), 归因非空洞。目标态两套测试跑完: `secret-scan` 50/50, `secret-guard` 584/585 (唯一 FAIL 为测试内 SC-13 头注释计数的无 git 伪影), 套件自身输出喂 L3 静默。

## Findings

### Critical

无。R2 唯一的 critical (`e8d39a8a`, W3 白名单作用于既有键) 已收口 (V2 / V10); v3 没有引入「照 Spec 实现会让现有拦截或检出变成放行」的文字。

### Major

#### M1 — id `8d258b19` / major / issue / testing / scope `proposal.md What.W10`
**summary**: W10 的变量展开是本 hook 第一处「解析并改写命令文本」的新代码, Spec 没有「hook 不得执行命令文本的任何部分」这条不变量, 全部 L1 SC 行也没有副作用 canary: 本席构造的 eval 式实现 (非作者) 让 SC-16..25 / 29 / 31 / 32 全绿, 却在 hook 里真的执行了命令文本。

**证据**:
- Spec 与探针里没有这条要求: `proposal.md` 中 `eval` 只出现在 launcher 词表 (`:189`) 与时档说明; W10 全节 (`:176-182`) 只描述「字面赋值收集 + 前后缀拼接替换」, 未写「禁 eval / declare / printf -v 解释 / 对命令文本做命令替换」。`baseline_probe.py` 对 `canary / side effect / executed / touch / not execute / command substitution` 检索均 0 命中 (仅有的 `CANARY` 是 20i-20k 的五条金丝雀命令, 验的是退出码, 不是执行)。
- 坏实现 `mut_eval` (`$A/mut_eval`, 本席在目标原型 `_sg_vx_collect` 的链式引用解析处把字符串切片换成 `eval "${NAME}=\"${VALUE}\""` 再 `${!NAME}` 取值 —— 「让 shell 帮忙展开链式引用」的自然写法): 直调 canary (命令里是 `touch <私有路径>`, 只喂 stdin、从不由 harness 执行): 5 种载荷 (`f=$(touch C); cat "$f"`、`f="$(touch C)"; …`、反引号、`d=/etc/forgejo; f="$d/app.ini$(touch C)"; …`、`f=$((1+$(touch C >/dev/null; echo 1)))`) 里 **4 种创建了 canary**; 基线与原型 5 种都不创建。
- `WPA_ONLY=SC-16,…,SC-25,SC-31 python3 baseline_probe.py $A/mut_eval/aria` → SC-16 17/17 · SC-17 4/4 · SC-18 9/9 · SC-19 23/23 · SC-20 14/14 · SC-21 22/22 · SC-22 67/67 · SC-23 8/8 · SC-24 9/9 · SC-25 7/7 · SC-31 5/5, 与同一命令对**未改动目标**的对照跑逐项相同; `WPA_ONLY=SC-29,SC-32` + 真 bash 3.2 → SC-29 9/9 · SC-32 3/3, `target shape holds`。

**失败场景**: 实现者要实现「单层链式 `d=…; f=$d/…`」(W10), 用 eval 一次解决 → 全部 SC 绿; 之后 hook 在内建判定放行、命令真正执行**之前**, 就以 hook 进程的权限执行了命令文本里的任意 `$(…)` / 反引号 (绕过权限提示与 deny 规则, 无人值守的 Layer 2 里更无人复议)。同类面 W9 (条目文件是仓内文件, 比命令文本更靠近信任边界: 克隆来的仓库可带 `.aria/secret-guard.paths`) 与 W12 (归一化) 同样没有「不执行」的行。

**建议修法**: W10 与「其它耦合」各加一句不变量: 展开只许字符串切片 / 拼接, 禁 `eval` / `declare` / `printf -v` 对命令文本求值、禁对命令文本做命令替换; SC-21 增一条 `reverse-guard` 行 (**基线绿 / 目标绿 / `mut_eval` 红**, 三态已实测): 上述 5 种载荷在 hook 运行后 canary 路径必须不存在; W9 增同形行 (条目文件含 `$(touch C)`、反引号、`*` 且 cwd 下有可被 glob 命中的文件); W12 增同形行。严重度取 major 而非 critical 的理由: Spec 正文指向的是切片实现, 缺口在验收与不变量表述, 不是实现指令; 若主控按口径第 3 条字面读 (「验收会放过错误实现」), 此条是候选升级项。

#### M2 — id `8fbbee80` / major / issue / testing / scope `proposal.md What.W11`
**summary**: W11 写明「credit 用 tight」适用整个进程表族, 但 SC-22 只用三个 plain `ps` 行 (22q-22s) 钉 tight; 把 tight 判据收窄成「只认行首 plain `ps`」的坏实现让 SC-16..25 / 31 全绿, 却把 13 种 pgrep / pstree / top / docker / launcher / 远程包裹 + 行过滤的形态放行; 且规则行与 tight 判据是两份必须字节同源的正则 (SC-31 31c 迫使规则行内联), 任一份漂移全绿。

**证据**:
- Spec: W11 `:192`「credit 用 tight: `ps -ef | grep -v grep` 打印的仍是整行命令, 行级过滤不算 (22q-22s)」与 `:197`「tight 族 (claude-config / `app.ini` / 进程表 / 扩展条目) 只认 discard / count / hash / 名字面 credit」。探针里对进程表族带行过滤的行**只有** 22q `ps aux | grep curl`、22r `ps -ef | grep -v grep`、22s `ps aux | grep '^dev'` 三条 (检索全部 `grep|awk|cut|sed` 命中确认)。
- 原型 (`$A/target/aria/hooks/secret-guard.sh`) 里同一份 launcher / ps / 远程包裹正则出现两次: `_SG_PROCTAB` 等变量 (`:394-397`, 供 `_sg_compute_credit:420` 的 tight 判定) 与规则行字面 (`:1122` 等)。
- 坏实现 `mut_tight`: 只把 `:397` 的 `_SG_PROCTAB_ALL` 改成「行首 plain `ps`」: SC-16 17/17 · SC-17 4/4 · SC-18 9/9 · SC-19 23/23 · SC-20 14/14 · SC-21 22/22 · SC-22 **67/67** · SC-23 8/8 · SC-24 9/9 · SC-25 7/7 · SC-31 5/5, 与对照逐项相同; 但 13 种形态由 exit 2 变 0: `sudo ps -ef | grep -v grep`、`timeout 5 ps aux | grep '^root'`、`/bin/ps aux | grep -v grep`、`pgrep -af curl | grep -v pgrep`、`pgrep -a x | grep '^1'`、`pstree -a | grep -v grep`、`top -b -n1 -c | grep '^ *1 '`、`docker ps --no-trunc | grep '^abc'`、`ssh host 'ps aux' | grep '^root'`、`docker exec c1 ps aux | grep -v grep`、`sh -c 'ps aux' | grep -v grep`、`pgrep -af x | cut -d' ' -f1`、`pgrep -af x | sed 's/a/b/'`。
- 最小漂移 `m_w11_launcher_ionice_tightcopy_only` (只从 tight 拷贝里去掉 `ionice`): 相关 7 行 (22aw / 22q / 22r / 22s / 22Y / 22O / 22bi) **零红**; `ionice ps aux | grep -v grep` 目标 2 → 变异 0。
- W8 同形: `mut_ini` (tight 只认字面 `/etc/forgejo/app.ini`): SC-16 17/17 · SC-17 4/4 · SC-18 9/9 (16f 是唯一一行, 单路径单读取器单过滤); `cat /srv/git-forgejo/app.ini | grep '^JWT_SECRET'`、`cat /etc/gitea/app.ini | grep -v '^;'`、`ssh …'pct exec … cat …'` 之外的 4 种目标 2 → 变异 0。

**失败场景**: 实现者补 tight 时只覆盖 plain `ps` (10CG/Aria#221 的叙事就是 ps), 或日后改一份漏改另一份 → 全部 SC 绿; 被拦的 AI 照共用 BLOCKED 文案的 `Acceptable filters` (列了 `| grep '^SAFE_PREFIX='`) 重试 `pgrep -af x | grep '^1'` 即放行, 10CG/Aria#221 的泄露路径在验收全绿下重开。另: Spec 没说 `/proc/*/environ|cmdline` 行是否属 tight 族 (基线与目标对 `cat /proc/self/environ | grep -v xx` 都放行), 两种读法都无行钉住。

**建议修法**: SC-22 对每个族成员 (ps 六类 / `pgrep -a|--list-full` / `pstree -a` / `top -c` / `docker|podman top` / `ps --no-trunc` / 远程与外壳包裹 / 15 个 launcher) 各配 `| grep -v x` → 2 与 `| wc -l` → 0 一对 (由探针循环生成, 沿用 `l1e`), SC-16 对每个 `app.ini` 路径形配 `| grep '^K'` → 2; 三态: 基线 0 (放行) 红 / 目标 2 绿 / `mut_tight`、漂移变异、`mut_ini` 红 (均已实测)。可选: W11 写明规则行与 tight 判据须同源 (规则行内嵌同一变量, 31c 只禁「整行只由变量组成」), 并声明 `/proc` 行是否属 tight。

#### M3 — id `0a8380fd` / major / issue / implementation / scope `proposal.md What.W9`
**summary**: W9 对 Bash 面的读取器判定是「同一管道阶段内 (最近的 `|` `;` `&` 换行之后) 位于条目前面有一个读取器」, 阶段切分不识别引号: `python3 -c` / `node -e` / `awk` 程序文本里只要出现 `;` `&` 或换行, 读取器就与条目被切开而放行; Spec 同时声称这两个解释器源组「与 W8 对 `app.ini` 的作用面一致」, 事实相反。

**证据**: 项目 `.aria/secret-guard.paths` 含条目 `/srv/private/zone.cfg` (本席造的诱饵路径), `CLAUDE_PROJECT_DIR` 指向该项目; 同一命令骨架分别对内建 `app.ini` 行 (W8) 与扩展条目 (W9) 直调目标原型 (退出码, 内建 / 扩展):
`python3 -c "print(open('PATH').read())"` 2 / 2; `python3 -c "import os; print(open('PATH').read())"` **2 / 0**; `python3 -c "import os\nprint(open('PATH').read())"` **2 / 0**; `python3 -c "x=1; y=2; print(…)"` **2 / 0**; `python3 -c "a=1 & 2; print(…)"` **2 / 0**; `node -e "const fs=require('fs'); console.log(fs.readFileSync('PATH','utf8'))"` **2 / 0**; `awk 'BEGIN{x=1; while ((getline l < "PATH") > 0) print l}'` **2 / 0**; `cat PATH`、`echo start; cat PATH`、`ls; python3 -c "print(open('PATH').read())"` 均 2 / 2。真 bash 3.2 下相同。Spec 原文: `:161`「同一管道阶段内 (最近的 `|` `;` `&` 换行之后)」与「读取器 = W8 打印型读取器组 (29 个) 或 `python3 -c` / `node -e` 源组 (与 W8 对 `app.ini` 的作用面一致; 31 个成员逐个出行, SC-19 19u)」; 19o / 19u 的探针骨架都是单语句形 (无 `;`)。

**失败场景**: 采用方把敏感路径列入扩展清单; AI 日后写最常见的 Python 一行式 `python3 -c "import json; print(open('<列入的路径>').read())"` → 放行并泄露, 而 W8 内建名单对同形命令是拦的; 扩展失效又被设计成静默, 使用者无从察觉。

**建议修法**: 把「阶段」改成与内建逐段评估同一套 quote-aware 切分 (复用 `_sg_split_top`) 或对解释器源组直接用「`python3 -c`/`node -e` 之后、同一 `|` 之内出现条目」的内建行语义 (`[^|]*`); 并补 19o / 19u 的含 `;` 形态行 (基线 0 红 / 目标 2 绿 / 现原型 0 红)。若决定不修, 则必须订正「作用面一致」并在已知限制与 SC-19 各钉一条 known-limit。

#### M4 — id `ac42f607` / major / issue / implementation / scope `proposal.md What.W11`
**summary**: (R2 K 簇残余) W11 重写的 `/proc` pid 位置枚举 (`self`、数字、`*`、`$name`、`${…}`、`$(…)`) 漏掉同族最常见的写法: `$$` / `$!`、`[0-9]*` 一类 glob (全进程 argv 的惯用写法)、brace 展开与 `thread-self`; 既无用例也未列已知限制。

**证据** (直调, 基线 / 目标原型退出码): `cat /proc/$$/environ` 0 / **0**; `cat /proc/$!/environ` 0 / 0; `cat /proc/[0-9]*/cmdline` 0 / **0**; `cat /proc/[0-9]*/environ` 0 / 0; `cat /proc/1?/environ` 0 / 0; `cat /proc/{1,2}/environ` 0 / 0; `cat /proc/thread-self/environ` 0 / 0; `tr "\0" "\n" < /proc/$$/environ`、`strings /proc/$$/environ`、`xargs -0 -a /proc/$$/environ echo`、`python3 -c "…open('/proc/$$/environ')…"`、`for p in /proc/[0-9]*; do cat "$p/environ"; done` 均 0 / 0; 对照: `cat /proc/self/environ` 2 / 2、`cat /proc/$PPID/environ` 0 / 2、`cat /proc/*/cmdline` 0 / 2。`$$` 是「当前 shell 的 pid」的标准写法, `/proc/$$/environ` 打印 Bash 工具所在 shell 的启动环境, 与基线已拦的 `/proc/self/environ`、`printenv` 同一信息量。探针与 Spec 对 `/proc/$$`、`[0-9]*`、`thread-self`、`{…}` 检索 0 命中, 22bh 的残余清单 (find -exec / lua / 嵌套 launcher / 非首位 BSD 簇 / `if` 位置 / `pgrep -fl` / 容器内裸 ps) 不含它们。

**失败场景**: 被拦在 `cat /proc/self/environ` 或 `cat /proc/*/cmdline` 的 AI 改写成 `/proc/$$/environ` 或 `/proc/[0-9]*/cmdline` 即放行 (基线同样放行, 故不是回退, 但 W11 正是为收这类旁路而改写 `/proc` 行, 且 R2 K 簇裁定「纳入或列为已知限制均可, 但每一侧都要有决定性的 SC 行」)。

**建议修法**: pid 位置补 `$$`、`$!`、`[0-9]…` / `?` 起头的 glob 段与 `thread-self` (22be 加行, 基线 0 / 目标 2), 或把这些写法列入 22bh 并各钉一行 known-limit; brace 与路径归一化变体 (`/proc/./self/…`、`//`) 属黑名单固有上限, 在已知限制里一句话带过即可。

#### M5 — id `1c49d896` / major / issue / testing / scope `proposal.md SC-7`
**summary**: 「新分类器的哪几步作用于哪些 tag」只被钉了一部分: 熵下限不得套到既有键 (7h) 与 FAKE 不得套到 env-line / provider (7h / 11) 有行, 但路径形 / 点分标识符链套到既有 `json-secret-field`、白名单套到既有 bearer / x-api-key / URL tag 两类坏实现让全部 L3 行全绿, 却让基线检出的真值变静默。

**证据**: Spec `:66`「6 个新 tag 与既有 `json-secret-field` (后者只过第 2 步)」与 W3 `:91`「作用范围 = 6 个新 tag + 既有 `json-secret-field`; 不作用于 provider 前缀类、`env-line-secret-keyword` 与其余既有 tag」。坏实现 `mut3a` (路径形与点分链排除也套到既有 `json-secret-field`) 与 `mut3b` (白名单也套到 bearer-token / x-api-key-header / 四个 URL tag / gcp-private-key-id) 各跑 `WPA_ONLY=SC-1..13,SC-15`: SC-1 2/2 · SC-2 4/4 · SC-3 2/2 · SC-4 19/19 · SC-5 14/14 · SC-6 11/11 · SC-7 10/10 · SC-8 1/1 · SC-9 25/25 · SC-10 12/12 · SC-11 26/26 · SC-12 13/13 · SC-13 7/7 · SC-15 7/7, 与对照目标逐项相同。行为差 (基线 / 正确目标 / mut3a / mut3b): 既有键 `"api_key":"SG.<22>.<43>"` (SendGrid 形, 段内无 `-`)、`"access_token":"<24>.<6>.<27>"`、`"password":"correct.horse.battery.staple"`、`"password":"/tR0ub4dor/<6>/<6>"` → ALERT / ALERT / **silent** / ALERT; `Authorization: Bearer FAKE…`、`X-API-Key: PLACEHOLDER…`、`postgres://svc:FAKE…@db/app` → ALERT / ALERT / ALERT / **silent**; 对照 `"password":"<20 位随机>"` 四者都 ALERT。

**失败场景**: 实现者在分类循环里把五步统一套给所有被分类的 tag (原型为此专门分了 `CLASSIFIED_TAGS` 与 `NEW_TAGS`, 说明统一套用是顺手写法) → 既有键下约 1/4 的 SendGrid 形 key、点分口令、路径形口令由基线检出变静默, 全部 SC 绿; 这正是 Spec 头号目标「不引入任何安全回退」要防的。

**建议修法**: SC-7 7h 增「既有键 × {路径形值, 点分标识符值}」两个 `reverse-guard` 独立运行 (基线告警 / 目标告警 / `mut3a` 静默), 另对既有非 JSON tag 循环生成「标记词开头的值仍告警」(bearer / x-api-key / 四个 URL / gcp / webhook, 对 `mut3b` 转红)。

### Minor

#### m1 — id `dcba7939` / minor / issue / implementation / scope `proposal.md SC-22`
`docker container top <c>` (`docker top` 的长写法, 输出同样含完整命令行) 基线 0 / 目标 0; Spec 与 22bl 覆盖了 `docker top`、`docker compose top`、`docker container ls --no-trunc`, 唯独漏它, 也未列入 22bh。按 K 簇裁定应纳入或钉 known-limit。附带: `ps aux | grep -c X` 是新增误拦 (`grep -c` 只出计数, 但 tight 不认), W11 的「新增误拦」成文清单未列 (Impact 的 `ps aux | grep …` 泛指涵盖, 精度问题)。

#### m2 — id `6f503728` / minor / issue / implementation / scope `proposal.md What.W9`
扩展条目的「长度 4-200」「含字母或数字」未说明单位与字母类: 本机 `awk` 是 mawk (按字节计), 条目 `a配置` (3 字符 / 7 字节) 被接受 (`cat /srv/a配置/x` → 2), 而 Spec 与 gawk-UTF-8 会跳过; 纯中文条目 `配置密钥` (4 字符、无 ASCII 字母数字) 被**静默跳过** (`cat /srv/配置密钥/x` → 0)。10CG Lab 是中文环境, 中文目录名的敏感路径无法列入且无提示。W9 应写明按字节还是字符、`[[:alnum:]]` 取哪个 locale, 并加一行非 ASCII 条目用例或成文为已知限制。

#### m3 — id `2f76563e` / minor / issue / testing / scope `proposal.md Impact`
关闭关键字机械检查用 `echo "rc=${PIPESTATUS[1]}"` (grep 的退出码), 看不见 `git log` 本身失败: 对不存在的 `<起点>` (`git log --format=%B nonexistent..HEAD | grep -niE '…'`) 实跑得 `rc=1` 而 git 为 128; 判据「无匹配输出且 `rc=1` = 通过」在 git 的 `fatal:` 走 stderr 时只靠使用者把它当「有输出」才不被误判。Spec 自称「写法照 Aria#199 的 rc 判据」, 而 #199 的守卫监视的是生产者 (`git grep`) 的 `PIPESTATUS[0]`; 此处应同时校验 `${PIPESTATUS[0]}`。(V7 的正反例本身全部正确, 仅此一处精度问题。)

#### m4 — id `cfb2fb14` / minor / issue / testing / scope `proposal.md Tasks`
Tasks 1.10 要求 `WPA_REQUIRE_ALL=1` 下「32c / 29h / 29i 与 20g 不得是 `n/a`」, 但 20g 在 root 下按设计不可构造 (`baseline_probe.py` 的 `_unreadable()`: `os.geteuid() == 0` → `not-constructible`, 随后 exit 3); `aria-runner` 容器 Dockerfile 无 `USER` 指令 (默认 root)。1.10 / 1.1 没写「须以非 root 运行探针」, 在 root 容器里验收会无故卡在 exit 3。补一句即可。

#### m5 — id `f410df76` / minor / issue / documentation / scope `proposal.md Impact`
10CG/aria-plugin#154 关单评论须披露的「与评论 19339 字面参数的两处有意偏离」不全: 评论 19339 第 2 条写的是「`[REDACTED` 前缀值跳过」, Spec W3 只放行括号闭合的 `[REDACTED…]` (`:87`), 未闭合的 `[REDACTED` 开头值明确要求仍检出 (`:91`、SC-7 7j), 这是第三处偏离 (收窄), 关单评论清单只列了 8 位 vs 16 位门槛与指纹 16 字符门槛。关单评论是不可撤回的外发动作, 披露清单应补全。

## 上一轮对账

对 R2 聚合报告的七个定稿簇 (键为主控定稿键) 逐一核验; 其它归并键 (`fc97f926`→`e8d39a8a`、`51e90cab` / `5ce95ecf` / `e7e041c6`→`eb350937`、`5fd1f356`→`ce6fc59c`) 随簇。

| 簇 (R2 键 / 席位) | 状态 | 本席核验 |
|---|---|---|
| A `e8d39a8a` (tl C1, cr M1, km M1; critical) | **closed** | V2: 基线检出的 `$`+小写数字 / `$`+大写数字 / `$(…)` / ASCII `...` 结尾 / `<` 不闭合 / crypt 哈希在既有键上目标仍全部告警; 整值占位七类静默; 新 tag 同形真值仍检出。V10: 7 个自选分类器坏实现全部被其决定性行转红 (7j / 11h / 11v / 11x / 11y / 4o / 4t / 10b / 11w)。W3 的 1e-4 / 1e-6 概率估算按 94 字符口令字母表重算量级成立。残余: M5 (作用域未钉全)。 |
| K `ac42f607` (tl M1, ba M3, qa M3; major) | **partially closed** | R2 点名项全部闭合 (V8: 22 条写法基线 0 / 目标 2; 120 条 launcher × 族全 2; 放行侧全 0; `python3 -c` / `node -e` 读 `/proc` 已纳入; `/proc/N/cmdline`、`<pid>` 占位词文本提及放行 (22bf))。但 `/proc` pid 位置枚举仍漏 `$$` 等最常见写法 (M4), 同簇另有 m1 与 W11 tight 的跨族缺口 (M2)。 |
| L `ce6fc59c` (tl M2, ba M4, km M2; major) | **closed** | V6: 四条腿全部为惰性诱饵 (hook 未生效时输出 0 字节 / ENOENT / 合成值); 腿 1 / 2 不被新旧 L1 误拦 (可执行); L1 腿 3 / 4 与 Read 腿对新 L1 拦、对基线放行 (有鉴别力); 执行条件 `plugin-cache-currency.py` 存在且 PASS / STALE / SKIP / FAIL / AHEAD 五态齐全; 1.10 与 1.12 已拆; 头部 Rule #7 声明改写后与步骤一致。 |
| M `eb350937` (qa M2 / M1, ba M1 / M2; major) | **closed** (对「缺成员」维度) | V10: 本席自选 8 个缺项成员 (跨 W2 / W8 / W9 / W11 / W12 / 基线 `/proc`) 逐个被其对应行转红, 15/15 坏实现全部转红; 执笔的 420 个坏实现 / 14 个等价变异本席未重跑。新的未覆盖维度是「规则族 × 附属判据」的交叉积, 见 M2 (tight)、M5 (分类器作用域) 与 M1 (执行安全), 属 R2 簇 M 的同类延伸 (枚举集合逐成员出行已做到, 交叉维度没做)。 |
| N `60f3173a` (qa M4; major) | **closed** | V4: 14 次敌意路径全串等值; additionalContext 里没有任何 `tool_input` 文本, 且 13d / 13g 判据是全串等值而非正则 (我 R2 提的「`[^()]*` 允许插入段内自由文本」缺口随之消失)。风险: `source` 取 `tool_name` 原样, 无形状校验 (见风险)。 |
| O `6bd285b1` (cr M2, tl m1, ba m4, cr m1; major) | **closed** | V9: 判据改为同次运行交错的整进程 CPU 时间比 + 活性断言 + 20 s 墙钟兜底, 与主机负载无关; (f)/(f0)/(g)/(h)/(i) 全部复测在界内 (f 的比值 1.52 / 1.68 靠 100 ms 地板而过, Spec W14 已如实写出); L3 稠密输入已设档并规定每 tag 前 200 个 span 的迭代上界 (11w, 变异 `m_cap_300` 转红)。 |
| P `05982c10` (km M3; major) | **closed** | V7: 机械检查正反例各 10 / 8 全部正确; Impact 与 Tasks 贯穿行 / 1.11 / 1.13 一致 (三张 issue 只用 `Refs`, #154 关单在 1.12 之后, 归档 D.2 排在 1.12 / 1.13 勾选之后以免 `openspec-archive` 自动开 tracker issue); 残余只有 m3 / m5 两处精度。 |

**R2 minor 里我认为仍未处置的**: 无。本席 R2 的 7 条 minor (cffa7c09 / b4230080 / 984b1c3d / cfb24732 / 467c8b54 / 15da802b / a305732c) 经实跑均已按 v3 处置 (7h 决定性、ASCII `...` 已删、已知限制成文、L3 迭代上界与 (i) 档、`/proc` pid 位置收窄与文本提及成文 (V8)、17d 的 21 条放行写法、形态行点名未运行行并有 `WPA_REQUIRE_ALL`)。

## 对执笔人自报薄弱点与请裁项的表态

**自报薄弱点 (v3 报告 §6)**
1. 原型不是实现、坏实现自构 (同源盲区): **可接受, 且被本轮印证**。本席三个非作者坏实现 (`mut_eval` / `mut_tight` / `mut3a`) 各自存活, 恰是执笔 campaign 的盲区 (交叉维度)。建议 Tasks 1.8 的必测坏实现清单加上「执行安全 / tight 跨族与拷贝漂移 / 分类器作用域」三类。
2. 体量 (+40%): **可接受**。体量不改变实现者动作; 但实现者要读 proposal 151 KB + 探针 160 KB, 理解成本是真实的 (见风险)。
3. 时档阈值由单机原型实测: **可接受**。本席复测在界内 (V9), 「比值越界上呈、不放宽」符合 Rule #10; (g) 满额档 2.00 距 2.5 余量约 20%, 在更慢的真实现上可能触界, 届时按 Spec 上呈即可。
4. W1 + W2 使每次 Read 的 hook 成本约 3×: **可接受**。复测 0.135→0.386 / 0.162→0.423 / 0.141→0.668 s, 5 s 内; Windows Git-Bash 进程派生慢一个量级未实测 (见风险), 建议 B.1 请 owner 在 MINGW64 上测一次。
5. 已接受误报的钉法 (22bj / 10l) 是取舍: **可接受, 建议保留 10l**。这些行是「该类被收口时强制同步 Spec」的绊线, 与 known-limit 同体例; V11 的电池显示新增误报面确实很小。
6. 真 bash 3.2 沿用 writer-v2 构建: **可接受**。本席用同一二进制复现 (V5), 配方在证据文件; 配方里补丁文件只有主 tarball 有 sha256、`curl -fLO` + `patch -p0` 补丁无校验 (低风险, 见风险)。
7. 「表里写了、原型没做」: **可接受**。本席对 W4 表 10 个 tag 独立重算 fp 全部相等 (V3)。
8. cr 两条未采纳备注: (a) W9 有效条目为零时不调用 grep: **可接受**——GNU grep 下 3 字符 / 注释-only 文件已被 19w 与 allow-guard 行钉住 (空模式 bug 会使 `cat abc` → 2), BSD / macOS grep 空模式文件语义未验, 建议写进 B.2 实现注意事项; (b) W6 清理不写 `rm -rf "$HOME"`: **不可接受其理由** (「无可证伪判据」不成立: `! grep -nE 'rm -rf[[:space:]]+"?\$\{?HOME' hooks/tests/*.sh` 即机械判据), 但不阻塞——现有套件无 `HOME=` 赋值 (已核), 建议并入 1.3 实现注意事项。

**请裁项 (§7)**
1. 待复议 19 (W5 默认 A, 只含 tag 与工具名): **可接受**。V4 证实零外来文本; 唯一不确定的是 `tool_name` 无形状校验 (风险 1)。
2. 10l 保留或删除: **保留**。
3. 时档阈值与口径: **可接受**。
4. W1 的每 Read 成本: **可接受** (含 Windows 未实测的风险, 见风险)。
5. cr 两条未采纳备注: 见上 8。
6. km 两条风险: (a) A.1 认领 (2026-09-30T17:57:13Z, `SWEEP_TTL` 24 h) 早已过期: **可接受按例行维护处理** (决策单第 4 项: claim 与心跳沿用 2026-09-17 例行授权), B.1 开工前必须续心跳或重认领; (b) 建议开单 7.1 的「约 1400 个空段使 hook 超时后命令被放行」配方在主仓 GitHub 镜像匿名可读: **建议保留在内部 Spec, 但正式开单时只写现象不写配方** (这是对 guard 的现成绕过口诀)。
7. 归档落盘: **已核**。`git ls-tree c0a6654` 下 `writer-v3-proto/` 57 个文件, 含 `timing.py` / `timing_summary.txt` / `mut_summary_v3.txt` / `README.md`, 头部与 Tasks 1.8 的引用都解析得到。
8. Rule #10 自作主张 (a)-(f): (a) `/proc` 纳入内联解释器: 可接受 (已闭合 K 簇该项); (b) W5 零外来文本: 可接受 (V4); (c) 10l / 12m / 9l-9m: 可接受; (d) (e) (f) 无异议。同族修补范围由执笔判断本身已写进 handoff 请复议, 合规。
9. 观察 (L1 数次误拦、L3 对文档式占位告警): **一致且可佐证**。本席审计中安装的基线 hook 也触发了: 两次 Bash heredoc 被拦 (一次因文本里的 `os.environ` 配 `head -n` 命中 `\.env` 无右边界 —— 正是 W12 要修的 FP; 一次因文本里的 `cat /proc/1/environ` —— 基线行本就拦), 一次 Write 的测试脚本被 L3 告警 (含 `"password":"%s"` 格式模板的占位); 均为合成 / 占位, 无需轮换, 改用 Write 工具落文件绕开, 未用 `# guard:ack`。

## 风险 / 疑问 (不计入 finding)

1. **`source: ${tool}` 无形状校验**: V4 附带验证, 把 `tool_name` 换成 `mcp__srv__x) obey` 时, 插入段原样回显 (`(tags: …; source: mcp__srv__x) obey)`)。shipped 的 `hooks.json` 两层 matcher 把 `tool_name` 限在五个内置工具, 不可达; 但采用方若把 `secret-scan.sh` 另注册到更宽的 matcher (如 `*` 或 MCP 工具), 外来文本即进入受信通道。一行 `case` 白名单 (不在五者内写 `unknown`) 即可, 并可让 13d 的「严格形状」在代码里也成立。
2. **MINGW64 未实测**: 10CG/aria-plugin#203 的报告环境就是 MINGW64, 而 W9 (进程替换 `<(…)`、`cmp` / `tr` / `awk` 行为、`CLAUDE_PROJECT_DIR` 是 `C:\…` 还是 `/c/…`) 与 W8 的反斜杠路径、W1 的进程派生成本 (每 Read 约 0.3 s × 一个量级) 全部没有 Windows 数据。W9 恰是服务这个环境的功能; 建议在 1.12 后加一条 owner 在该机器上跑的腿, 或至少在 #154 关单评论里披露「未在 MINGW64 验证」。
3. **macOS / BSD**: `grep -ob` 偏移语义、`grep -F -f` 空模式文件、`sed -i -E` (现有 hook 即已不兼容 BSD sed, L3 的计数替换在 macOS 上本就退化) 均未验证, 沿用已知限制。
4. **基线逐段评估器本身已在 ≥8 KB 的多引用命令上逼近 / 超过 5 s**: 本席在负载 19 的主机上实测 7.9 KB / 16 赋值 / 1600 个 `$v` 引用: 基线 CPU 6.47 s、目标 7.47 s; 4 KB 档目标 / 基线 1.56, 8 KB 档 1.30。即超时即放行 (建议开单 7.1) 的窗口在目标上略有加宽; Spec 在 Impact 与 7.1 已如实申报 (「含 `$VAR` 引用的命令约 1.4-2.3 倍」), 但 (h1) 全部放行且引用密集的档位 (本席实测 2.34×) 不在任何档的判据内。判据不改, 提示一下。
5. **范围与 Level 2**: 沿用 owner 裁定 (决策单第 3 项), 不重复异议; 观察: 14 个 W 项里 W5 (三个 issue 均未诉求, 评论 19339 还明说「其余部分现行已满足, 不重复实现」) 与 W9 (#203 只写「考虑」) 是可选项。保留 W5 有实际用途: Tasks 1.12 的 L3 腿用其插入段区分新旧 hook, 因此不建议删。
6. **owner 等待点登记**: 合并 (两个子模块与主仓)、推 master、tag 与发版、开新 issue (7.x 全部) 均逐次请示; 1.12 的缓存更新 + 重启会话是明确的 owner 门; 允许的四类 (feature 分支推送 / 开 PR / issue 评论 / 关闭) 在 Impact 里只有 #154 一处评论 + 一处关闭, 并推迟到 1.12 之后。登记齐全。
7. **bash 3.2 构建配方的完整性**: 主 tarball 有 sha256, 57 个补丁 `curl -fLO` 后 `patch -p0` 无校验和 (同源 HTTPS, 低风险), 且需要 bison / m4 (无 root 时取 `.deb` 解包)。
8. 本席复测 (g) / (h) 均在负载 15-19 的共享 4 核主机上, 绝对值偏高, 只看比值; 其余席位同时在跑探针, 墙钟不作判据。
9. W9 `4-200`、`含字母或数字` 与 `grep -F -i` 的 locale 行为 (m2) 之外, 条目大小写折叠对非 ASCII 依赖 locale, 与 `tr '[:upper:]' '[:lower:]'` 是否同折叠未验。

## Verdict

- verdict: **PASS_WITH_WARNINGS**
- counts: **0C/5M/5m**
- **Vote: REVISE**

## 是否足以进入 A.2

**不足以** —— 5 条 major 须在 v4 处理后再进 A.2, 但都是「补一句规定 + 补若干行用例」的小改: M1 加不执行命令文本的不变量与 canary 行; M2 把 SC-22 / SC-16 的 tight 行按族成员循环出行; M3 修 W9 阶段切分或订正「作用面一致」并钉 known-limit; M4 补 `$$` / `[0-9]*` / `thread-self` 或钉 known-limit; M5 补既有键 × 路径形 / 点分值与既有非 JSON tag × 标记词的 `reverse-guard` 行。R2 七簇中六簇已收口, 方案取舍与 Level 2 范围本身成立, 没有需要重做的设计; 本轮新 finding 的类型 (验收交叉维度、文字规定与既有约定不一致) 与 R2 簇 M / K 同源, 建议 v4 只做这五处加法, 不扩大机制。
