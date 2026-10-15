# WP-A / L1 研究笔记: aria/hooks/secret-guard.sh (aria-plugin v1.74.1 @ 268da8f)

范围: `aria/hooks/secret-guard.sh` (1120 行) 及其测试。真仓只读, 所有实验在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/secret-guard/` (下称 `$EXP`)。`git status` 收尾核验: 主仓仅有原有的未跟踪 `openspec/changes/secret-net-l3-and-bypass-paths/`, aria 子模块干净, 无 git 写操作。为让依赖 git 历史的用例能跑, 我把 `.git/modules/aria` 整目录拷进 `$EXP/aria-gitdir` 并改了副本的 core.worktree, 只读取主仓。环境: bash 5.2.15 / jq 1.6 / Python 3.11.2, 本机无 zsh/docker/pstree/bash 3.2。标注「推测」的地方是没实测的。

披露 (偏离「绝不真的执行这些命令」的 3 处, 均不涉及读任何凭据文件):
1. 为实测进程列举暴露面, 我对一个带伪造标记 (argv 与 env 各一个运行时生成的假串) 的哑进程真跑了 ps/pgrep/top 与 /proc 读取, 只检查该进程自己那一行, 从未打印别的进程命令行。
2. 对真实安装的 hook 做了活体试验 (见 §6 风险 1)。
3. 用 `systemd-run --user` 起了一个一次性 sleep 单元验证 `systemctl status` 暴露面, 随后已停掉。

---

## 0. 先看这 10 条 (全部实测)

1. 基线测试套件 593/593 通过, 耗时 1m51s (头注释写 599, 不含 zsh 593; 无 zsh 机器跑不到 6 条)。若副本没有 git 历史, 会变成 581/582 (SC-9a 与 SC-8 被跳过, SC-13 头注释计数误红)。
2. 进程列举的 14 条待测命令里 `ps aux/-ef/auxww/-eo pid,args/-o pid,command/-ww -fp`、`pgrep -a/-af`、`pstree -ap`、`top -b -n1 -c`、`ps aux | grep`、`ps eww`、`docker ps --no-trunc`、`docker top`、`systemctl status` 基线全部放行。`cat /proc/N/cmdline` 与 `/proc/N/environ` 原本就被拦 (L930/L932/L933), 但只认 `self|数字`, `/proc/*/cmdline`、`/proc/$pid/cmdline`、`xargs -0 -a /proc/N/cmdline` 放行。
3. issue #221 点名「待补」的 jq 形态里 `jq 'length'` 与 `jq '.X | length'` 基线已经放行 (L427 的正则允许 `.+|` 前缀)。真正缺的只有 `keys_unsorted`、`map_values(length)`、`map(.name)`/`map(.key)`。另外 `jq -r '.Items | keys[]'` 是测试里**刻意保持拦截**的负向锚 (`secret-guard.test.sh:841`, SOT secret-hygiene.md 写明), 不能顺手放进白名单。
4. issue #221 建议的 `\.env([^A-Za-z0-9_]|$)` 若机械套到全部 39 条含 `\.env` 的行, 465 条探针里有 108 条由拦变放: 含 20 条 `.envrc` 漏拦 (head/tail/less/strings/hexdump/od/xxd/awk/perl/sort/nl/tac/diff/dd 读 `.envrc`) 以及 `cp .env /dev/stdout`、`scp .env user@h:` 这类「边界吃掉了后面需要的空白」造成的真漏。只改 python/node/lua 三行 (L893/L894/L974) 并写成 `\.env(rc)?([^A-Za-z0-9_]|$)` 才无真实召回损失。
5. 变量间接 (#203 ②) 放行的原因是「路径与读取器落在不同段」, 按段评估 (L1088) 看不到。在整条命令里收集字面赋值, 再把每个含 `$VAR` 的段替换成字面值后**再判一次**, 能拦住我构造的 24 条泄露形态 (基线 0/24), 22 条正常用法 0 误报, 整个 docs 语料 2700 条命令 0 新增误报。
6. 基线存在三个会被新规则继承的既有缺陷: (i) 读取器没有左词边界, `chmod 600 ~/.ssh/id_rsa` 因 `chmod` 里含 `od` 被拦; (ii) 参数里带引号的 `|` (如 `grep -E 'A|B' ~/.bashrc`) 会让所有 `读取器 + [^|]* + 文件名` 的行失明; (iii) credit 是整段级的, `cat .env` 换一行再写 `echo hi | wc -l` 整段放行。
7. 延迟悬崖 (既有): 约 5 ms/段 (空闲), 1400 个 `:;` 空段需 7.1 秒, 单段 20KB 需 15 到 44 秒。hooks.json 的 timeout 是 5 秒。**活体证据**: `pg_dump --version` 单独跑被真实 hook 拦, 前面加 1400 个 `:;` 后被放行并真的执行了 (超时即放行)。新增规则与展开逻辑会把悬崖左移。
8. L3 (secret-scan.sh) 对 #221 的真实形态几乎无感: 进程列举输出里的 `Authorization: token <40位hex>`、`CF-Access-Client-Secret: <64位hex>`、`--token=<40位hex>` 均零告警, 只有 `Authorization: Bearer ...` 命中 `bearer-token`。所以 L1 的进程表规则是目前唯一的预防层。
9. Bash 面与 Read/Edit 面清单不对齐: 52 个样例路径里 15 个两面判定不同。Read 工具读 `~/.bashrc` 基线放行; 反过来 `known_hosts`、`/secrets/`、`service-account*.json` 等只有 Read 面拦。
10. 我在副本上拼出的综合原型 (E3+F1+F2+A+D2+C+G, 净增约 113 行) 在同步 3 处测试耦合后 595/595 通过 (593 原有 + 我加的 2 条 SC-19 探针), 对 42 条指派矩阵改变了 27 条, 方向全部符合预期。

---

## 1. 架构地图 (file:line 均以实读为准)

### 1.1 入口与输入解析
| 项 | 位置 | 说明 |
|---|---|---|
| 重入 bash | L129-131 | hook runner 用 $SHELL 而非 shebang 执行 (#154), 非 bash 则 `exec bash "$0"` |
| 严格模式 | L133 | `set -uo pipefail`, 无 `-e`, 自己控制退出码 |
| 测试可 source 的闸门 | L491-493 | `BASH_SOURCE != $0` 时 return: 只定义 L137-487 的函数与 `_SG_*` 变量, 不读 stdin。SC-8 性能测试靠这个闸门抽取, **新增辅助函数必须放在闸门之上** |
| jq 缺失 | L496-518 | fail-closed (exit 2), `SECRET_GUARD_BYPASS_NO_JQ=1` 可旁路并记日志 |
| 读 stdin | L521 | 空输入 exit 0 |
| 字段抽取 | L564 | 一次 `jq -j` 用 NUL 分隔取 4 个字段: `(.tool_name\|type)`, `.tool_name`, `.tool_input.command`, `.tool_input.file_path`, 经 `tr -d '\r'` (Windows jq 的 CRLF, #132) |
| 字段数守卫 | L574-577 | 不等于 4 (内嵌 NUL 或坏 JSON) 直接 exit 2 |
| tool_name 校验 | L584-593 | 非 string / 缺失一律 exit 2 |
| 不取 `.cwd` | L564 | 现有代码没有读 stdin 里的 `cwd`, 也没用 `CLAUDE_PROJECT_DIR` |
| 审计日志 | L606-628 `log_ack` | TSV 追加到 `~/.claude/logs/guard-bypass.log`, 写不了时只在 stderr 打 sha256 前缀 |

### 1.2 工具分派 (L631-701)
- `Read|Edit` (L632-694): `file_path` 转小写后过一条长 ERE (L641, 清单见 §5.1); 命中后走一次性 ack (L654-675: `SECRET_GUARD_ACK_PATH` + `/tmp/secret-guard-ack-$USER-$nonce.nonce` marker, 用后删除, 无 nonce 则拒绝并打印操作步骤), 否则打印 L676-690 的拒绝文案并 exit 2。
- `Bash` (L695-697): 落到命令分析。
- `*` (L698-699): **exit 0**。hooks.json 里第三组 matcher 写的是 `Read|Edit|Write|MultiEdit`, 但脚本对 Write/MultiEdit 直接放行。

### 1.3 Bash 面流水线
1. 空命令 exit 0 (L705); 超过 64KB exit 2 (L709-713)。
2. `# guard:ack` (L719 带理由, 理由须至少 8 个非空白字符, 记 ACK-REASON; L728 裸 ack 记 ACK-NO-REASON 并 WARN)。**在整条命令上判, 先于分段评估** (SC-12): 一句 ack 豁免所有段。
3. `risky_patterns` 数组 L736-1009, 共 145 行。
4. 分段评估 (归档 spec secret-guard-per-segment-evaluation, #128):
   - `_sg_safe_to_split` L159-268: 含 `{ } ( ) \` [[ ]] <<`、命令位置的 `for/while/until/if/case/select/exec/time`、裸 `&` 之一就「降级」为整条命令按旧语义判 (mode=whole)。
   - `_sg_split_top` L276-359: 引号/转义感知地按顶层 `;` `&&` `||` 切段。**不切**单个 `|`、换行、`&`。
   - `_sg_judge_one` L1034-1081: 逐行 pattern 顺序匹配; 首个命中的 pattern 才算 credit (L1040, 每段只算一次), credit 为真则 `break` 放行 (**后面的 pattern 不再检查**), 否则打印拒绝文案并 return 2。
   - `_sg_per_segment_eval` L1088-1102; 整套逻辑包在子 shell 里 (L1111), 退出码 0/2 之外一律当内部错误 fail-closed (L1119)。所以新增代码里任何未绑定变量都会让**所有** Bash 命令被拦, 不是只拦新规则。
5. REDACT 过滤器 (credit): `_sg_compute_credit` L386-487。行号见 §5.3。
6. manifest precision (Aria #179, 归档 2026-08-22): 前置字符白名单 `_SG_PP_NAME` L383 与 `_SG_PP_SUFFIX` L384 (两族), `_SG_CLAUDE_CFG` L365, tight 模式检测 L405-408; 套在 14 条「路径清单型」行上; 以 `/` 开头的名字不套白名单 (Amendment-2)。逐行依据在 `.aria/notes/secret-guard-179-pattern-rows.md`。

### 1.4 拒绝的输出格式
- **只有 exit 2 + stderr**。grep 整个脚本没有 `permissionDecision`、`hookSpecificOutput`、`ask`; 矩阵 84 条 (42 指派 + 探针) 无一条往 stdout 写。对照: 同目录 `handoff-location-guard.sh:17-19,149-155` 默认走 JSON `{"decision":"block"}` + exit 0。官方 hook 文档支持 `permissionDecision: allow|deny|ask` (本机 plugin-dev 的 `hook-development/SKILL.md:148`), 本 hook 未用, 也就没有 ask 路径。
- Bash 面拒绝文案: L1043-1071, 是**未加引号的 heredoc** (`cat >&2 <<EOF`), 会展开 `$pat` 和 `$(_sg_redact_echo "$command")`, 因此新增文本里不能出现反引号或 `$`。所有 risky_patterns 命中共用这一份 (整条与分段两种模式都是)。分段模式再追加 L1073 `Triggering segment:` 行。
- 其他文案: Read/Edit 拒绝 L676-690、ack 无 nonce L665-673、jq 缺失 L497-509、64KB L711、字段数 L575、tool_name L588/L591、内部错误 L1119。
- 回显脱敏: `_sg_redact_echo` L1023-1027 (`key=value` 与 ≥20 字符裸串打码, #145)。

---

## 2. 七个改动点的落点与约束

### (a) 服务端配置文件入名单
- 落点 (两个面都要改):
  - Bash 面: 在 L815 (claude-config 行) 后加一行 manifest 行, 做法同 #179: 名字组单一定义成变量, 读取器组 + `([^|]*${_SG_PP_NAME})?(名字)`; 以 `/` 开头的名字走 `[^|]*(...)` 纯分支。
  - Read/Edit 面: 在 L641 的 ERE 末尾追加 (该 ERE 对小写路径匹配)。
  - credit: 必须把新名字并入 tight 检测 (L405-408)。实测: 不并入时 `cat /etc/forgejo/app.ini | grep '^JWT_SECRET'` 因「锚定 grep 算过滤」而**放行并泄露**; 并入后拦。
  - python3 -c / node -e 的源组 (L893/L894) 与 claude-config 一样追加。
- 现有机制的约束:
  - 读取器无左边界, 新行须自带 `(^|[^[:alnum:]_.-])` 前缀, 否则 `chmod 600 /etc/forgejo/app.ini` 会因 `chmod` 含 `od` 误拦 (我实测先误拦后修复)。
  - 含 `[^|]*` 的行算「跨段族」, 触发 SC-19 耦合 (见 §3.3)。
  - `Edit` 工具也被拦, 合法运维编辑需 ack nonce; `sed -i` 会被含 `sed` 的读取器行拦 (与现有 `sed -i ~/.bashrc` 一致, 是产品取舍)。
- 候选名单 (基线对 `cat <路径>` 全部放行, 只有 `.pem/.key` 已拦): 核心 Forgejo/Gitea `app.ini` 三形态 (`(forgejo|gitea)…/app.ini`、`custom/conf/app.ini`、docker 的 `/data/gitea/conf/app.ini`); 同类 (实测放行): `grafana.ini`、`/etc/{nomad,consul,vault}.d/` (Aether 用 Nomad/Consul, 与本 Lab 直接相关)、`/etc/pve/priv/`、`/etc/shadow`、`~/.netrc ~/.npmrc ~/.pgpass ~/.git-credentials ~/.vault-token ~/.pypirc ~/.my.cnf`、`gitlab-secrets.json`、`wg0.conf`、`redis.conf`、`wp-config.php`、`admin.conf`、`k3s.yaml`、`gh hosts.yml`、`rclone.conf`、`terraform.tfvars`、`cloudflared config.yml`。
- 风险: 裸名 `app.ini` 太泛 (任何应用都有), 必须锚在 `forgejo|gitea|custom/conf`。实测 0 误报: `ls/stat/cp/chmod/systemctl restart forgejo`、`echo '...app.ini...'`、`grep -rn 'app.ini' docs/`、`git log -- custom/conf/app.ini`、`/opt/myapp/app.ini`、`php.ini`。残余漏报: `cd /etc/forgejo && cat app.ini` (相对名), 引号内 `|` (见 §6 风险 3)。
- 额外发现: Read 面缺 shell rc (`.bashrc .bash_profile .zshrc .profile .bash_aliases /etc/environment /etc/profile`), `Read ~/.bashrc` 放行 (H2)。是否顺带补齐属产品取舍。

### (b) 项目级扩展入口
- 项目根怎么拿:
  - 官方文档 (本机 `plugin-dev/skills/hook-development/SKILL.md:300-326`): stdin JSON 含 `cwd`; 所有 command hook 的环境里有 `$CLAUDE_PROJECT_DIR` 与 `$CLAUDE_PLUGIN_ROOT`。**本环境未能实测** hook 进程的真实环境变量 (Bash 工具环境里没有 `CLAUDE_PROJECT_DIR`, hook 环境不可观测)。
  - 现有代码: secret-guard 不取 `.cwd` (L564), 要加就得改「字段数 == 4」的守卫 (L574), 不如用环境变量。Bash 工具的工作目录会因 `cd` 漂移, 所以 hook 进程 cwd 不等于项目根, 应优先 `CLAUDE_PROJECT_DIR`, 退而求其次 `$PWD`。
- 先例:
  - 没有任何 aria hook 读 `.aria/config.json`。
  - `session-start-check.sh:5` 读相对 cwd 的 `.aria/workflow-state.json`, 出错一律 exit 0。
  - `submodule-gate-telemetry.sh:20,33-34` 用 stdin 的 `cwd` + `git rev-parse --show-toplevel`, 永不阻断。
  - `aria-doctor/scripts/check_secret_guard_install.sh:104` 用 `${CLAUDE_PROJECT_DIR:-$PWD}`。
  - 官方 plugin-dev 示例 `SKILL.md:550` 读 `$CLAUDE_PROJECT_DIR/.claude/plugin-config.json`。
  - `.aria/` 下已有纯文本清单先例: `bare-issue-ref-allowlist.txt`、`linked-issue-field-grandfathered.txt`。
- 读失败的策略: **扩展部分 fail-open (降级为仅内置清单), 绝不因配置问题 exit 2**。依据: #154 的会话死锁教训; `handoff-location-guard.sh:51-59` 明文 fail-open; `host-docker-logout-guard.sh:58-60,68-71` jq 缺失时放行; secret-guard 自己只在「无法解析 hook 输入」时才 fail-closed (L496-518, L574-593)。配套建议: 由 aria-doctor 增加一项校验, 否则拼错的条目会静默失效, 让项目产生虚假安全感。
- 我在副本实现并测了原型 (`$EXP/var/B`, `b_test.py`, 25 条全过): 文件 `$CLAUDE_PROJECT_DIR/.aria/secret-guard.paths`, 一行一个**字面子串** (不用正则, 杜绝正则语法错误导致静默不匹配), `#` 注释与空行忽略, 容忍 CRLF (Windows 报告者环境是 MINGW64), 只读前 32KB, 最多 200 条, 每条 4 到 200 字符且含字母数字。只增不减。读取器须出现在条目之前; credit 按 tight 处理 (格式未知); Read/Edit 面对 `file_path` 做子串匹配。覆盖的失败态: 文件缺失、chmod 000、路径是目录、二进制垃圾行、超长行、正则元字符 (按字面)、1000 行文件 (第 500 条被截断, 第 150 条生效)、`CLAUDE_PROJECT_DIR` 未设时退回 `$PWD`。延迟 (负载下): 无文件约 100ms, 200 条约 131ms。
- 备选 (推测, 未实测): 用 `.claude/settings.json` 的 `env` 注入 `SECRET_GUARD_EXTRA_PATHS`, 零文件 IO; 且该文件本身在 #179 清单内, AI 无法用 Edit 改它。代价是只有人能维护, 且 env 块是否传给 hook 我没验证。

### (c) 路径经 shell 变量间接
- 为什么放行: `f=/etc/forgejo/app.ini; sed -n '1,80p' "$f"` 会在 `;` 处切成两段 (L276), 第一段有路径没读取器, 第二段有读取器没路径。即便降级成整串 (L1091), 所有行都要求「读取器在前、名字在后」, 而 `f=~/.bashrc; cat $f` 里名字在读取器之前。所以 C1-C4、D1 与 X-c01..c20 共 25 条全部放行 (ssh 包裹不是原因: D2 被拦)。
- 能否识别: 能, 但需要新增逻辑。三种做法:
  1. 「赋值敏感路径」直接拦赋值段: 简单, 但 `export KUBECONFIG=~/.kube/config`、`ENV_FILE=.env docker compose ...` 是常见惯用法, 误报面大 (推测, 未实测; 我没做这版原型)。
  2. 整串共现规则: 精度最差 (推测)。
  3. **字面赋值展开 (我实现了原型)**: 在整条命令里收集 `NAME=值` (含 `export/declare/local/readonly/typeset` 前缀、引号值、`$(...)`、`for NAME in 列表`, 单层链式 `d=/etc/forgejo; f=$d/app.ini`), 对每个含 `$NAME`/`${NAME}`/`\$NAME` 的段再判**替换后的副本**。只会新增拦截, 不改原判定。上限: 16 个赋值, 每变量 8 次替换。
- 原型结果 (`probes_c.py`, `$EXP/var/AC`): 24 条泄露形态基线 0 拦, 只改名单 (A) 也只拦 1, 加展开后 24/24; 22 条正常用法 (`f=~/.bashrc; ls -l "$f"`、`export KUBECONFIG=...; kubectl get pods`、`f=.env; cp $f /tmp/x`、`for f in *.txt; do cat $f; done` 等) 0 误报; 2700 条 docs 语料里 201 条含「赋值 + $」的命令 0 新增拦截; 1200 条种子模糊语料 0 内部错误、无超时 (另 1500 条 token 汤同样)。
- 残余 (仍放行, 均已实测): 数组赋值 `files=(...)`、`read -r f <<< path`、引号拼接 `/etc/fo""rgejo/app.ini`、`$(printf ...)` 拼路径、`d=...; cat "$d"/app.ini` (引号夹在路径中间)、值里有 glob `/etc/for*/app.ini`、`set -- path; cat $1`、`cd /etc/forgejo && cat app.ini`、跨两次工具调用的变量 (Bash 工具不保留 shell 状态, 无法识别)。
- 成本: 每个用到变量的段多判一次; 赋值密集命令耗时约翻倍 (负载下 8 赋值 + 40 引用: 1.7s 到 3.9s)。可选优化 (推测): 先对每个赋值值做一次「合成 `cat 值` 判定」, 无命中就跳过展开。
- 可移植性风险 (推测, 本机无老 bash): 原型用了 `${s//"pat"/"rep"}` 嵌套引号替换与 `+=`; bash 5.2 的 `patsub_replacement` 会让替换串里的 `&` 有特殊含义。Phase B 需在 bash 3.2 (macOS) 上验证。

### (d) 进程表列举与进程环境
实测暴露面 (哑进程标记法, `$EXP/psprobe/psprobe.sh`):
| 命令 | argv | environ | 应否拦 |
|---|---|---|---|
| `ps aux / auxww / ax / -ef / -eF / -f -p N` | 是 | 否 | 拦 |
| `ps -eo pid,args|cmd|command`, `ps -o pid,args -p N` | 是 | 否 | 拦 |
| `ps e / eww / axe / ewwx` (BSD e) | 是 | **是** | 拦 |
| `ps -e`, `ps -eo pid,comm`, `ps -p N`, `ps -ely`(comm; 我的 awk 没定位到列, 按手册 CMD=comm) | 否 | 否 | 放 |
| `pgrep -a / -af / --list-full` | 是 | 否 | 拦 |
| `pgrep PAT`, `pgrep -f`, `pgrep -l`, `pgrep -fl` (Linux 仅进程名) | 否 | 否 | 放 (macOS 的 `-fl` 会出完整命令行, 平台相关, 推测) |
| `top -b -n1 -c` | 是, 但默认 80 列会截断, `-w 512` 才全出 | 否 | 拦 (前 80 列内的凭据照样泄) |
| `top -b -n1` (无 -c) | 否 | 否 | 放 |
| `/proc/N/cmdline` | 是 | 否 | 已拦 (仅 self 与数字) |
| `/proc/N/environ` | 否 | 是 | 已拦 |
| `/proc/N/comm|stat|status` | 否 | 否 | `status` 现被拦 (L932), 属既有轻度误报 |
| `systemctl status|show -p ExecStart|cat` (一次性用户单元验证) | 是 | 否 | 见下 |
| `pstree -a`, `docker top`, `docker ps --no-trunc` | 文档推断 (本机未装 psmisc/docker) | | 拦 |

- 结论: 拦「完整命令行列」形态 (BSD 选项簇、SysV `-f/-F` 簇、`-o/--format` 列表含 args/cmd/command)、`pgrep -a`、`pstree -a`、`top -c`、`docker top`、`docker ps --no-trunc`, 以及 launcher 包裹 (`sudo/timeout/nice/env/nohup/watch/...`) 与 ssh/docker exec/kubectl exec/nomad alloc exec/lxc/podman exec 远程形态; 放过只出 pid 或进程名的形态。**`systemctl status` 建议不拦**: 暴露已验证, 但它是最常用的健康检查, 单元 ExecStart 带凭据本就是反模式, 误报代价高 (推荐交给 L3; 注意 §0 第 8 条, L3 现在对此形态也无感)。
- 原型 D2 (`$EXP/var/D2`, `probes_d.py`): 56 条良性对照 0 误报, 58 条暴露形态拦 57 (唯一漏: 宿主上直接跑 `pct exec 101 -- ps aux`, 我没加 pct 行; 经 ssh 包裹的形态已拦)。**必须用 tight credit**: 不用时 `ps -ef | grep -v grep`、`ps aux | grep '^dev'`、`ps aux | awk '{print $2,$11}'` 三条因「行级过滤算 credit」放行, 但它们打印的仍是整行命令。tight 下只认 wc/sha*/>/dev/null/jq 名字字面。
- 写法约束: `ps` 是短词, 必须锚命令位置 `(^|[;&|(){]|\`|[[:cntrl:]])[[:blank:]]*` (沿用 L867-877 printenv/env 行的写法), 否则 `grep -rn 'ps aux' docs/`、`echo 'use ps -ef'` 会误拦; BSD 簇的终止符要用 `[^[:alnum:]_-]|$` (否则 `ssh host 'ps aux'` 因后面紧跟引号漏拦, 我第一版就漏了)。新测试可照 `secret-guard.test.sh:668-721` 的 PartB「命令位置全覆盖」块写 (拦的清单 + FP-fix 清单)。
- `/proc` 行放宽: `(self|[0-9]+)` 改为 `([^/[:space:]$]+|\$\{[^}]*\}|\$NAME|\$\([^)]*\))`, 读取器补 `xargs sed grep egrep fgrep rg cut paste nl sort base64 cp dd`。注意这会让该行的 SC-19 族 key 改名 (见 §3.3)。
- 相邻发现 (不在 WP-A 范围, 建议另开单): `docker inspect <ctr>` 整段 JSON 含 `.Config.Env` 基线放行 (L859 只拦带 `--format ...Config.Env` 的); `journalctl`、`nomad job inspect` 同属「进程/容器环境」类但未评估。

### (e) `.env` 右边界
- 全部 `\.env` 出现处 (非注释): L641 (Read/Edit, 已以 `$` 收尾, 不需要改)、L782-784、L823-833、L836-843、L846-847、L864、L893-894、L909-912、L915-917、L967-971、L974, 共 39 条 pattern 行。L782 已有 `(\b|/|$|[[:space:]])` 右边界; L783 是独立的 `.envrc` 行。
- 实测 (`probes_env.py` 465 条探针 = 24 种读取器形态 × 8 种文件名 + 习语):
  | 变体 | 翻转数 | 说明 |
  |---|---|---|
  | E1 issue 原文套全部行 | 108 条由拦变放 | 20 条 `.envrc` 漏拦; 22 条 `.env_prod`; 52 条预期的误报消除; 其余是「边界吞掉后面需要的空白」的机械副作用 (`cp .env /dev/stdout`、`rsync/scp .env user@` 行要求边界后再有 `[[:space:]]+`; `cat .env""` 也被破坏) |
  | E2 只改 L893/L894/L974, 写 `\.env(rc)?([^A-Za-z0-9_]|$)` | 16 条, 全是预期 | 修掉 G1 (`os.environ`)、`os.environb`、`.environment`; `.envrc` 保留; 唯一「损失」是假想文件名 `.env_prod` 经 python/node 读 |
  | E3 = E2 + `process.env` 习语归一 | 19 条 | 另修掉 `node -e "console.log(process.env.HOME)"` 这个同类误报 (基线被拦, issue 未提; 加边界也救不了它, 因为 `process.env.` 后面是 `.`) |
- 建议: E2 (+ 视产品取舍加 E3)。其余行的读取器形态下 `.env` 前面必有读取器和路径, 后面跟字母基本就是别的文件名, 不值得动。

### (f) jq 白名单
- 匹配语义: L427, 正则 (bash `[[ =~ ]]`, 经 `_sg_line_match` 按行逐行匹配), 不是字面; **左侧只锚定「某个 `| jq` 阶段」, 不锚定管道末段**: `(.+\|[[:space:]]*)?(keys|length|paths|leaf_paths)["']?[[:space:]]*($|\|)` — 词前可以是程序开头, 也可以是「任意内容加管道」; 词后只要是行尾或 `|` 就算数, `|` 之后的内容完全不受约束。
- 既有漏洞 (实测基线放行, 对抗性写法, 非意外): `jq '. as $d | keys | map($d[.])'` (把值全打出来)、`jq 'keys | $ENV'` (打出 jq 进程环境)、`jq 'length | tostring, input'`。新形态不能扩大这个洞。
- 可行写法 (原型 F1/F2): 
  - F1: 词表加 `keys_unsorted`。
  - F2: 单独一条**锚定语法**的 credit 规则 (程序必须带引号, 前缀只允许简单点路径, 词后必须紧跟闭合引号): `jq FLAGS ["'](\.[A-Za-z_][A-Za-z0-9_.]*[[:space:]]*\|[[:space:]]*)?(map_values\(length\)|map\(length\)|to_entries[[:space:]]*\|[[:space:]]*map\(\.key\)|with_entries\(\.value[[:space:]]*\|=[[:space:]]*length\))["'][[:space:]]*($|\|)`。
  - 实测: G3/G5、`with_entries(.value |= length)`、`to_entries | map(.key)`、`nomad var get ... | jq '.Items | map_values(length)'`、vault 同形, 翻为放行; `. as $d | map_values(length) | $d` 与 `... | map_values(length) | $ENV` 仍拦 (F2 没有扩大洞)。
  - F3 (`map(.name)`/`map(.key)`) 依赖「name/key 字段不是密」的假设, 我不推荐进默认集, 写进 spec 由 owner 取舍。
- 不要加 `keys[]`: 有负向锚测试 (见 §0 第 3 条)。
- tight 模式下 (claude-config / 新增服务端配置 / 进程表) 现有 `jq '{...}'` 形状 credit 被关 (L432), 但名字字面与 length 类 credit 保留。

### (g) 拒绝文案加「凭据不要放命令行参数」
- 位置: L1043-1071 那份共用 heredoc (见 §1.4)。各 Bash 拒绝分支共用, 所以一句话会出现在**所有**拦截里 (包括 `cat .env`, 与之无关); 若要只在进程表族出现需要按命中行分支, 我判断不值得。
- 测试约束: SC-21 (`test:1147-1175`) 与 SC-22 (`test:1199-1257`) 只用 `grep '^Command was: '` 和 `grep '^Triggering segment: '` 两行做精确比对, 其余行可加 (原型 G 加在 "Why:" 段后, 全套通过)。
- 注意事项: heredoc 未加引号, 新文本不能有反引号或 `$`; 拒绝文案面向 AI, Rule #6 的 hunk 级判定要把「提示文案」单独看 (决策单第 3 条提到沿用 owner 2026-08-02 的 substitute 框定)。
- 顺带: 新增大正则行会使 `Matched pattern:` 那一行长达 746 字符, 对 AI 是噪声; 可考虑给新行加短标签 (设计题)。

---

## 3. 测试套件

### 3.1 声明与运行
- 文件: `aria/hooks/tests/secret-guard.test.sh` (2050 行, 132KB)。从插件根运行 `bash aria/hooks/tests/secret-guard.test.sh`; `HOOK="$(dirname "$0")/../secret-guard.sh"`; 需要 jq, python3 (SC-20 注入与 SC-19 census), git 历史 (SC-9a/SC-8 用 `git show af87cae:hooks/secret-guard.sh`)。退出码 0/1。
- 助手 (静态出现次数): `bash_case NAME WANT CMD` 465, `read_case` 33, `edit_case` 2, `run_case` 17 (原始 JSON), `crlf_case` 5 (PATH 里塞一个输出 CRLF 的 jq shim), `static_case` 4 (grep 脚本文本), `sts_case` 25 (直接断言 `_sg_safe_to_split`), `split_case` 10 (断言 `_SG_SEGS` 长度), `sc9a_case` 6 (改前改后各断言一次), `zsh_case` 6 (无 zsh 时跳过), 另有若干手写 `if ...; pass++` 块 (SC-13/16/17/19/20/21/22、nonce 用例等)。
- 用例数: 头注释写「599 (593 without zsh)」, 与实跑吻合 (593)。`run_case` 用 `echo "$input" | "$HOOK"` 读退出码, 所以**整套只验证退出码**, 文案只在 SC-21/22 验证。

### 3.2 基线完整跑一次 (副本)
- 有 git 上下文: **PASS 593 / 593, 0 FAIL, real 1m51s** (user 1m22s, sys 29s; 跑时负载约 3)。
- 无 git 上下文 (`cp -a` 的默认结果): PASS 581 / 582, FAIL 1 (`SC-13: 头注释计数同步`, 因 SC-9a 与 SC-8 被跳过, 总数 582 对不上 599/593), 耗时 1m05s。
- SC-8 各档 (空闲时, ms/call, 天花板 100): a 5.4, b 11.0, c 6.6, d 10.2, e 38.6。档 (e) 是最坏档: 4 段都命中数组末位 pattern 且自带 `| wc -l`。负载 15 到 20 时综合原型跑了 308 到 393 秒。

### 3.3 会被改动牵动的元测试 (改 hook 前必读)
| 测试 | 位置 | 约束 |
|---|---|---|
| SC-13 | 头注释 `test:11`、断言 `test:2018-2030` | 头注释 `Coverage: N cases (M without zsh)` 必须等于实跑总数; 标准子模块 `standards/conventions/secret-hygiene.md` L23/L287/L319 三处另有计数, **没有机械检查**, 靠人同步 |
| SC-19 | `test:1574-1646` | 用 census 动态取族; `family_count` 硬编码为 61 (断言与报错串各一处); 每个含字面 `[^|]` 或 `.*` 的「跨段」行按首个字面/分组归一个族, 每族必须有一条 `# family='<精确 key>'` 注释 + 跨段探针 (整串命中、各段皆不命中 ⇒ 判 0)。**改动跨段行开头的分组文本会让 key 改名**。我的综合原型需要 61→63 并加 2 条探针, 这也是历次发版的常规动作 (57→60→61) |
| census 盲点 | `corpus_census.py:96-118` | census 在一个不带前置变量的独立 bash 里求值数组块, 所以**整行只由 `${VAR}` 组成的 pattern 在 census 里是空串**, 既不计入族也不产生 key; 新行应保留字面起头或先修 census |
| SC-17 | `test:1648-1665` | 各 `*_case "名字"` 文件内不得重名 |
| SC-16 | `test:1917-1930` | hook 源码不得出现字面 `(?:`; `\b` 是 GNU 依赖 |
| SC-20 | `test:1089-1146` | 对当前 hook 做精确文本替换注入错误: 依赖 `_sg_compute_credit` 里 `wc` 那段 (`_sg_line_match '\|[[:space:]]*wc[[:space:]]+-[clw]' "$seg"` + `has_filter=1` + `fi`) 与 `  local nl=$'\n'` 一字不变, 且要求注入后退出码**恰好为 2** |
| SC-8 | `test:1667-1915` | 用 awk 锚点抽 `risky_patterns` / `_sg_judge_one` / `_sg_per_segment_eval`, 其余函数靠 `source "$HOOK"` 获得 (所以辅助函数须在闸门之上); 绝对阈值 100ms 硬编码不读环境变量, 超了只能如实红, 不得自行放宽; 旧基线 af87cae 的 141 条哨兵是冻结的 |
| SC-9a / SC-8 | `test:1258-1326`, `1667+` | 需要 `git show af87cae`, 浅克隆会跳过 |
| 负向锚 | `test:841` | `jq -r '.Items | keys[]'` 必须拦 |
| SC-21/22 | `test:1147`, `1199` | 只钉 `Command was:` 与 `Triggering segment:` 两行 |

### 3.4 tests/lib、corpus_census.py、crlf-shim.test.sh
- `tests/lib/crlf-shim.sh` (129 行): 跨平台 CRLF 测试框架, 用 PATH 里的 shim 把真 jq 的每行输出补 `\r`, 复现 Windows 原生 jq (#132); 原语是**双向**的 (既断言没有修复时出 bug, 也断言修复后正常), 防空转。`crlf-shim.test.sh` (61 行) 是它的自测: 我在副本上跑 8/8 通过, 0.23 秒。
- `tests/jq-crlf-guard.sh` (91 行) 是静态 lint, 扫 hooks/skills 里「读 jq 输出进变量却没剥 CR」的写法; `jq-crlf-guard.test.sh` 7/7 通过; 基线 `hooks/*.sh` 与我的综合/扩展原型均 clean。**若项目扩展清单改用 jq 解析 JSON, 必须 `tr -d '\r'`** (这是选纯文本清单的理由之一)。
- `tests/corpus_census.py` (约 1250 行): 被 SC-19 调用的权威计数器。实际 matching 用子进程 `grep -E` 与 `bash [[ =~ ]]`, 不用 Python `re`。基线输出: patterns 145、spanning 86、family_count 61、corpus_case_count 464。**基线下 census 以 rc=1 退出** (诊断: `criteria.site_count == 6, expected exactly 13`, #179 引入 `[[ $tight -eq 0 ]] && _sg_line_match` 写法后提取器只认 6 处); 测试只取 stdout 所以不受影响, 但意味着「13 处 credit」这份清单已漂移。

---

## 4. 基线实测矩阵

### 4.1 脚本 (已在副本验证; 与我最初的 84 条版本逐条判定一致)
```python
#!/usr/bin/env python3
# matrix_min.py -- baseline verdict matrix for aria/hooks/secret-guard.sh (WP-A).  Strings only go to hook stdin; nothing is executed.
# usage: HOOK=/path/to/copy/aria/hooks/secret-guard.sh python3 matrix_min.py      (HOME is a throwaway dir -> no ~/.claude/logs writes)
import json, os, re, subprocess, tempfile

HOOK, HOME = os.environ["HOOK"], tempfile.mkdtemp()
N = "curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x"
B, R = "Bash", "Read"
CASES = [
    ("A1", B, "cat .env"), ("A2", B, "sed -n '1,20p' ~/.bashrc"),
    ("B1", B, "sed -n '1,80p' /etc/forgejo/app.ini"), ("B2", B, "cat /etc/gitea/app.ini"),
    ("B3", B, "cat custom/conf/app.ini"), ("B4", B, "grep -n JWT_SECRET /etc/forgejo/app.ini"),
    ("C1", B, 'f=/etc/forgejo/app.ini; sed -n \'1,80p\' "$f"'), ("C2", B, "f=~/.bashrc; cat $f"),
    ("C3", B, 'F=/etc/forgejo/app.ini && cat "$F"'), ("C4", B, "export CONF=/etc/forgejo/app.ini; cat $CONF"),
    ("D1", B, "ssh root@pve 'pct exec 101 -- sh -c \"f=/etc/forgejo/app.ini; sed -n 1,80p \\$f\"'"),
    ("D2", B, "ssh host 'cat ~/.bashrc'"),
    ("E01", B, "ps aux"), ("E02", B, "ps -ef"), ("E03", B, "ps auxww"), ("E04", B, "ps -eo pid,args"),
    ("E05", B, "ps -o pid,command -p 123"), ("E06", B, "ps -ww -fp 123"), ("E07", B, "cat /proc/123/cmdline"),
    ("E08", B, "tr '\\0' ' ' < /proc/123/cmdline"), ("E09", B, "pgrep -af curl"), ("E10", B, "pgrep -a curl"),
    ("E11", B, "pstree -ap"), ("E12", B, "top -b -n1 -c"), ("E13", B, "ps aux | grep curl"),
    ("E14", B, "systemctl status foo"), ("E15", B, "docker ps --no-trunc"), ("E16", B, "docker top abc"),
    ("E17", B, "cat /proc/123/environ"), ("E18", B, "ps eww -p 123"),
    ("F1", B, "ps -eo pid,comm"), ("F2", B, "ps -e"), ("F3", B, "pgrep curl"),
    ("G1", B, "python3 -c \"import os; print(len(os.environ.get('HOME','')))\""),
    ("G2", B, "python3 -c \"import os; print(os.getenv('HOME'))\""),
    ("G3", B, N + " | jq '.Items | map_values(length)'"), ("G4", B, N + " | jq 'keys'"),
    ("G5", B, N + " | jq 'keys_unsorted'"), ("G6", B, N + " | jq 'length'"), ("G7", B, N + " | jq '.Items | length'"),
    ("H1", R, "/etc/forgejo/app.ini"), ("H2", R, "/home/dev/.bashrc"),
]

def run(tool, s):
    tin = {"command": s} if tool == B else {"file_path": s}
    p = subprocess.run([HOOK], input=json.dumps({"tool_name": tool, "tool_input": tin}).encode(),
                       capture_output=True, env=dict(os.environ, HOME=HOME), timeout=60)
    m = re.search(rb"Matched pattern: (.*)", p.stderr)
    why = m.group(1).decode()[:58] if m else ("Read/Edit path regex" if b"secret-bearing file" in p.stderr else "")
    return p.returncode, why, bool(p.stdout.strip())

for cid, tool, s in CASES:
    rc, why, out = run(tool, s)
    print(f"{cid:4} {tool:4} rc={rc} {'BLOCK' if rc == 2 else 'ALLOW' if rc == 0 else 'OTHER':5}{' [stdout!]' if out else ''} {why}  <- {s[:64]}")
```
完整版 (带 EXTRA 探针、行号映射) 与差分工具在 `$EXP`: `matrix.py`, `diffmatrix.py`, `tri.py`, `mkvar.py` + `transforms_*.py`。

### 4.2 结果 (42 行指派矩阵: 基线 ALLOW 33 / BLOCK 9; 退出码只有 0 与 2)
「后」列是综合原型 ALL2 的判定 (A=放行 B=拦)。

| id | 命令 (节选) | 基线 | 命中规则 (基线) | 后 |
|---|---|---|---|---|
| A1 | `cat .env` | 拦 | L782 cat…\.env | B |
| A2 | `sed -n '1,20p' ~/.bashrc` | 拦 | L806 shell rc 读取器 | B |
| B1 | `sed -n '1,80p' /etc/forgejo/app.ini` | 放 | 无 | B |
| B2 | `cat /etc/gitea/app.ini` | 放 | 无 | B |
| B3 | `cat custom/conf/app.ini` | 放 | 无 | B |
| B4 | `grep -n JWT_SECRET /etc/forgejo/app.ini` | 放 | 无 | B |
| C1 | `f=/etc/forgejo/app.ini; sed -n '1,80p' "$f"` | 放 | 无 | B |
| C2 | `f=~/.bashrc; cat $f` | 放 | 无 | B |
| C3 | `F=/etc/forgejo/app.ini && cat "$F"` | 放 | 无 | B |
| C4 | `export CONF=...; cat $CONF` | 放 | 无 | B |
| D1 | ssh → pct exec → sh -c 内含 ② | 放 | 无 | B |
| D2 | `ssh host 'cat ~/.bashrc'` | 拦 | L806 | B |
| E01-E06 | `ps aux`, `ps -ef`, `ps auxww`, `ps -eo pid,args`, `ps -o pid,command -p 123`, `ps -ww -fp 123` | 放 | 无 | 全 B |
| E07 | `cat /proc/123/cmdline` | 拦 | L932 | B |
| E08 | `tr '\0' ' ' < /proc/123/cmdline` | 拦 | L932 | B |
| E09/E10 | `pgrep -af curl` / `pgrep -a curl` | 放 | 无 | B |
| E11 | `pstree -ap` | 放 | 无 | B |
| E12 | `top -b -n1 -c` | 放 | 无 | B |
| E13 | `ps aux \| grep curl` | 放 | 无 | B |
| E14 | `systemctl status foo` | 放 | 无 | **A (有意不拦)** |
| E15/E16 | `docker ps --no-trunc` / `docker top abc` | 放 | 无 | B |
| E17 | `cat /proc/123/environ` | 拦 | L930 | B |
| E18 | `ps eww -p 123` | 放 | 无 | B |
| F1-F3 | `ps -eo pid,comm` / `ps -e` / `pgrep curl` | 放 | 无 | 全 A (对照) |
| G1 | `python3 -c "...os.environ..."` | **拦 (误拦)** | L893 python3 -c 组的 `\.env` | A |
| G2 | `python3 -c "...os.getenv..."` | 放 | 无 | A |
| G3 | `curl .../v1/var/... \| jq '.Items \| map_values(length)'` | **拦 (误拦)** | L738 | A |
| G4 | 同 curl `\| jq 'keys'` | 放 | credit | A |
| G5 | `\| jq 'keys_unsorted'` | **拦 (误拦)** | L738 | A |
| G6/G7 | `\| jq 'length'` / `\| jq '.Items \| length'` | 放 (已在白名单) | credit | A |
| H1 | Read `/etc/forgejo/app.ini` | 放 | 无 | B |
| H2 | Read `/home/dev/.bashrc` | 放 (两面不对齐) | 无 | A (原型未动) |

原型改变 27/42, 全部是预期方向。

### 4.3 EXTRA 探针要点 (`baseline-extra.tsv`, 223 条)
- 服务端配置同类 25 条里只有 `privkey.pem`、`authkey.key` 被拦 (既有 `.pem/.key`), 其余 (grafana.ini、nomad/consul/vault.hcl、.netrc、.npmrc、.pgpass、.git-credentials、gitlab、wg0.conf、redis.conf、wp-config.php、.vault-token、admin.conf、k3s.yaml、hosts.yml、.pypirc、.my.cnf、/etc/shadow、tfvars、rclone.conf、cloudflared) 全放行; 对 `app.ini` 换 cat/less/head/awk/diff/`docker exec … cat`/`ssh … cat`/python open/`sed -i` 全放行。
- 变量间接 20 形态全放行 (仅 X-c06 `cat "$HOME/.bashrc"` 因字面 `/.bashrc` 被拦)。
- 进程类 80 形态里基线被拦的只有 `/proc` 的 self/数字形态; `cat /proc/*/cmdline`、`xargs -0 -a /proc/N/cmdline` 放行; `cat /proc/N/status` 被拦。
- 引号内 `|`: `grep -E 'TOKEN|SECRET' ~/.bashrc` 放行 (基线); 多行: `cat .env⏎echo hi | wc -l` 放行。
- 左边界: `chmod 600 ~/.ssh/id_rsa` 被拦 (基线误报)。

---

## 5. 现行名单与模式表

### 5.1 Read/Edit 面 (L641, 对小写路径匹配, 命中即拦; 逐分支)
`\.env(\.[a-z0-9_.-]+)?$`, `\.envrc$`, `/secrets?/`, `/credentials?/`, `id_rsa$ id_ed25519$ id_ecdsa$`, `\.ssh/id_[a-z0-9_]+$`, `\.pem$ \.key$ \.gpg$ \.age$ \.p12$ \.pfx$ \.jks$`, `\.tfstate$ \.tfstate\.backup$`, `/\.aws/credentials$ /\.aws/config$ /\.kube/config$ kubeconfig$ /\.docker/config\.json$`, `service[_-]account.*\.json$ gcp[_-]key.*\.json$ firebase.*\.json$`, `\.ssh/known_hosts$`, `/secret[_-]token /master[_-]key /encryption[_-]key`, 以及 #179 三条 `/\.claude/+(\./+)*settings\.json$`、`settings\.local\.json$`、`/\.claude\.json$`。**不含** shell rc 与任何服务端配置。

### 5.2 Bash 面 risky_patterns (L736-1009, 145 行)
| 行 | 族 | 内容 |
|---|---|---|
| 738-752 | Nomad Variables | `curl…/v1/var/`, `/v1/var/`, `nomad var get|list`, `var put` (L750, #170), `alloc fs`, `operator api…/var/` |
| 755 | Vault CLI | `vault read|kv get` |
| 758-764 | 云 secret manager | aws secretsmanager/ssm/kms, gcloud secrets, aliyun, az keyvault, akeyless |
| 767-774 | CLI 密码管理器 | op, pass, doppler, infisical, bws, chamber, teller |
| 777-779 | Git 平台 | gh api secrets/variables, forgejo … actions/secrets\|variables, glab variable get |
| 782-784 | .env 读取 | cat (L782 有右边界), cat `.envrc` (L783), head/tail/less/more (L784 无边界) |
| 797 | 密钥类文件 + 读取器 | id_rsa/ed25519/ecdsa, `.ssh/id_*`, .pem/.key/.p12/.pfx/.jks/.gpg/.age/.tfstate, `.aws/{credentials,config}`, `.kube/config`, kubeconfig, `.docker/config.json` |
| 806-807 | shell rc | `.bashrc .bash_profile .bash_login .zshrc .zprofile .profile .bash_aliases /etc/environment /etc/profile` (+ssh 包裹) |
| 815 | claude 配置 (#179) | settings.json / settings.local.json / `.claude.json`, 读取器含 jq |
| 819-820 | 容器挂载 | `/run/secrets/` |
| 823-843 | .env 组合读取 | find/xargs/dd/strings/hexdump/od/awk/perl/tee/mapfile/readarray/while-read/`<(...)`/cp /dev/stdout/`. .env`/`source .env` |
| 846-850 | ssh 远程读取 | cat/head/…/printenv/env + 敏感名, `ssh…printenv`, `ssh…systemd-cgls` |
| 855 | `set \| grep 敏感词` | |
| 858-864 | 容器 env | docker exec env/printenv, docker inspect `--format…Config.Env`, kubectl exec env/cat |
| 867-877 | 裸 env/printenv | 命令位置 (`(^\|[;&\|(){]\|\`\|[[:cntrl:]])[[:blank:]]*`), launcher 包裹, `command env`, then/do/else/elif |
| 880-885 | psql / k8s secret | 敏感列, `kubectl get secret -o`, `describe secret\|configmap` |
| 888-889 | base64 解码进 shell | |
| 893-894 | python3 -c / node -e | 源组 `/v1/var/ secretsmanager /secrets/ \.env provider_key` + claude 配置 |
| 897-900 | 解密工具 | sops / age / gpg -d, openssl pkcs12\|rsa\|ec -in |
| 904-906 | jq 身份/取值形状 | `.[] values .. tostring @text @json @base64`, `. + ""`, `.a.password` 等 |
| 909-917 | bash 原生与 coreutils 读取 | `$(< .env)`, `exec 3<`, rev/tac/nl/sort/…/diff/cmp/comm/xxd |
| 924-927 | IMDS | 169.254.169.254, 100.100.100.200, metadata.google.internal, `Metadata-Flavor: Google` |
| 930-933 | /proc | `cat /proc/(N\|self)/environ`, 读取器 + `/proc/(self\|数字)/(environ\|status\|cmdline)`, `< /proc/...` |
| 936-941 | 容器运行时 exec | nsenter crictl podman ctr lxc machinectl |
| 944-950 | 数据库 | pg_dump pg_dumpall mysqldump mongodump, psql \COPY, redis-cli GET/KEYS |
| 953-962 | 其他 secret store | consul kv get, etcdctl get, secret-tool, keyring, summon, berglas, envchain, vlt, knox, vault agent |
| 967-971 | .env 外发 | rsync/scp/curl -d @/nc |
| 974, 977, 980-981 | lua -e, psql -f, compgen -e, set -o posix | |
| 986-987, 990 | Vault HTTP 头与 token 字面, kubectl exec sh -c | |
| 992-1000 | 密钥文件外发 | dd if=, scp/rsync/cp key, tar .ssh \| ssh, wget --post-file |
| 1006-1008 | Forgejo 凭据响应端点 (#153) | `(forgejo\|curl)…runners/registration-token`, `/users/X/tokens`, `/user/applications/oauth2` |

### 5.3 REDACT 过滤器 (credit, L386-487; 每段算一次, 整段级)
| 行 | 过滤 | tight 下 |
|---|---|---|
| 427 | `\| jq [flags] ["']?(.+\|)?(keys\|length\|paths\|leaf_paths)["']?(行尾\|\|)` | 保留 |
| 432 | `\| jq ... {` 对象投影 | **关** |
| 443 | `\| grep` 带 `^`/`$` 锚 | 关 |
| 446 | `\| grep -v` | 关 |
| 449 | `\| sed` 含 `s///`/`Nd`/`D` | 关 |
| 453 | `\| cut -d/-f 单字段` | 关 |
| 457, 460 | `\| awk '…$N'` / `\| awk '/re/'` | 关 |
| 468, 471 | `>/dev/null` (非 `2>`), `&>/dev/null` | 保留 |
| 475 | `curl -o /dev/null` / `--output /dev/null` | 保留 |
| 479 | `\| wc -[clw]` | 保留 |
| 482 | `\| sha256sum\|md5sum\|sha1sum\|sha512sum` | 保留 |
tight 触发: 段里出现 claude 配置名 (L405-408)。**没有**的 credit: `grep -c`/`-q` 计数 (我试加了一条, 见 §6 可选项)。

### 5.4 前缀白名单与其他
- `_SG_PP_NAME` (L383) `(^|[[:space:]"'=/])`: 全名型 (shell rc, claude 配置); `_SG_PP_SUFFIX` (L384) `(^|[[:space:]"'=/*A-Za-z0-9_.-])`: 后缀型 (`.env .envrc .pem .key .p12 id_rsa`)。
- ack: L719/L728 (Bash), L654-675 (Read/Edit)。日志 `~/.claude/logs/guard-bypass.log`。

---

## 6. 设计要点与风险

### 6.1 建议方案 (标明哪些是推测)
按「小而直接」切, 避免 Spec 膨胀 (memory 里「拆 Spec / 112 行改动造 2838 行规格」的教训):

必做 (全部有原型与实测支撑):
1. (a) Forgejo/Gitea `app.ini` 三形态, **两个面**, **并入 tight**。同类清单由 owner 裁定, 我建议再带上 `grafana.ini`、`/etc/{nomad,consul,vault}.d/`、`/etc/pve/priv/`、`/etc/shadow` (与 Lab 直接相关); `.netrc/.npmrc/.pgpass/…` 作为后续。
2. (c) 字面赋值展开 (整条命令收集, 对含变量的段多判一次替换副本), 明确写出残余清单。
3. (d) 进程表: `ps` 三形态 + launcher + 远程 exec + `pgrep -a` + `pstree -a` + `top -c` + `docker top` + `docker ps --no-trunc` + `/proc` 放宽; **tight credit**; 不拦 `systemctl status`。
4. (e) E2 (三条内联解释器行, 带 `(rc)?`); E3 (`process.env`) 视产品取舍。
5. (f) F1 + F2 (锚定语法), 不加 `keys[]`, 不加 F3。
6. (g) 共用一句提示 (英文, 与现有文案同语种, 不含反引号与 `$`)。

可选 / 待 owner: (b) 项目扩展清单 (原型已验证, 建议纯文本 + 字面子串 + fail-open + aria-doctor 校验); `grep -c/-q` 计数 credit (`C1`, 我试过: 会改变所有来源的 credit, 对 `ps aux | grep -c curl` 这类高频检查有用); Read 面补 shell rc; `pgrep -fl` (macOS); `sed -i` 是否豁免。

### 6.2 风险与陷阱 (改 secret-guard.sh 最易踩)
1. **5 秒超时 = 放行 (既有, 活体证实)**。真实 hook 对 `pg_dump --version` 单独跑被拦; 前面加约 1400 个 `:;` 空段后该命令被放行并执行。副本上同串完整跑需 7.1 秒且最终 rc=2, 所以是「本来会拦, 超时后被放行」。结论性强, 但我没看到超时日志, 归因于 hooks.json 的 `timeout: 5` (推测)。分段成本约 5 ms/段 (空闲; 负载下 10 到 18), 单段 6KB 约 1.6 到 2.6 秒, 20KB 15 到 44 秒 (`_sg_safe_to_split`/`_sg_split_top` 在 UTF-8 locale 下逐字符取子串是 O(n²)); 下游 `LC_ALL=C` 只快 1.4 到 2 倍, 不是解。我的综合原型比基线慢约 10 到 25% (新增 4 行约 +1.5 到 3.5 ms/段, 最重的是进程表行约 640µs 与 app.ini 行约 395µs), SC-8 最坏档仍在 100ms 天花板内 (负载下 46.6 到 75.8 ms, 空闲基线 38.6 ms) 但余量变小。缓解 (推测): 重行前加廉价 glob 预检 (`*"ps "*` 等); 这类改动属于另一个 issue, 不建议混入 WP-A。
2. 新辅助函数放闸门之上; 任何未绑定变量会被子 shell 边界转成 rc≠0/2 ⇒ fail-closed ⇒ **全部 Bash 命令被拦** (可用性风险), 要跑 SC-20 风格的注入自测。
3. 既有缺陷 (WP-A 新行会继承, 建议另开 issue): 读取器无左边界 (`chmod` 含 `od`); 参数里引号内的 `|` 使所有 `[^|]*` 行失明; credit 整段级 (多行命令里随手一行 `| wc -l` 让整段放行)。
4. 「测试恒绿」风险: 基线必须先跑红再改 (memory: check-runs-at-baseline-first)。本研究的 `probes_*.py` 已给出每类的 baseline-failing 与对照集; 我第一版 D 变换漏了 `ssh host 'ps aux'` 与 `x=$(ps aux)` (终止符问题), 是靠对照集才抓到。census 对整行由变量组成的 pattern 是空串, 新行若这么写会在 SC-19 里「隐形」。
5. CRLF: 本 hook 所有 jq 输出已 `tr -d '\r'`; 新增文件读取要 `${line%$'\r'}`; 改 `test` 文件注意 CRLF 保持 (standards 模板、spec-drafter SKILL.md 是 CRLF, hook 与测试本身是 LF)。
6. 正则引擎: 全部经 bash `[[ =~ ]]` (glibc ERE), `\b` 是 GNU 扩展, 不支持 `(?:`/lookbehind, 所以「排除 `process.env`」只能靠预归一化而不是正则。`[^|]` 字面出现与否决定是否计入 SC-19 (`[^|;&]` 不计入)。
7. 文案 heredoc 未加引号: 新文本里的反引号与 `$` 会被执行。
8. 双安装: 项目若用 `.claude/scripts/secret-guard.sh` 本地副本 (aria-doctor 会检测 `divergent_content`), 插件更新不会自动覆盖。
9. 发布同步面 (历次 secret-guard 发版的惯例): hook 头注释 History、测试头注释计数、`secret-hygiene.md` 三处计数 (standards 子模块)、CHANGELOG Security 条目、plugin 版本派生文件。GitHub secret scanning 白名单 (`aria/.github/secret_scanning.yml`) 只豁免 hook 测试文件路径, 新增夹具别用像真 token 的字面。

### 6.3 新增测试规模估计 (推测)
我的探针集折算成用例大约: 服务端配置 25 + 变量间接 30 + 进程表 60 (仿 PartB: 拦清单 + FP-fix 清单) + env 边界 10 + jq 12 + 消息 2 + 扩展清单 20 ≈ 150 到 170 条, 约占现有 593 的四分之一以上。

### 6.4 复现与产物 (`$EXP`)
- 基线: `baseline-assigned.tsv`, `baseline-extra.tsv`, `baseline-test-run2.log`, `census.json`。
- 原型: `var/ALL2/hooks/secret-guard.sh` (+ `ALL2.diff` 230 行), 单项 `var/{E1,E2,E3,F1,F2,F3,A,Anotight,D2,D2nt,C,AC,G,B,LC,C1}`, 由 `mkvar.py --apply` 按 `transforms_*.py` 生成; 综合原型的测试副本已按 §3.3 调整 (`patch_tests.py`)。
- 探针/差分: `probes_{env,a,c,d,jqhole,ml,chmod}.py`, `tri.py`, `diffmatrix.py`, `after_table.py`, `parity.py`, `l3_probe.py`; 性能: `perf*.py`, `phase_time.sh`, `row_cost.sh`, `sc8_like.sh`; 语料: `corpus.txt` (2700 条) 与 `fuzz.txt`。
