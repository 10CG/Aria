---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-30T22:49:22.927Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- 被审对象 (47aa15f): `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 全文 (1-366); `baseline-evidence.md` 全文 (1-408); `baseline_probe.py` 全文 (1-1030)。
- issue: `aria-plugin-154.md`、`aria-plugin-203.md`、`Aria-221.md` 全文, 含评论 19339 与 25898。
- 决策单: `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文。
- `CLAUDE.md`: 规则 #6 / #7 / #10, 多远程两条硬约束, 版本管理 (:77-79)。
- 源码 @ aria 268da8f:
  - `hooks/secret-guard.sh` 全文 (1-1120); `hooks/secret-scan.sh` 全文 (1-377); `hooks/hooks.json` 全文。
  - `hooks/host-docker-logout-guard.sh`: exit 点, 以及 `updatedInput` / `permissionDecision` / `hookSpecificOutput` 的 grep。
  - `hooks/tests/secret-guard.test.sh`: 1-12 与 1085-1150; `hooks/tests/secret-scan.test.sh`: 118-124 (值已消隐)。
- 规范与配置:
  - `standards/conventions/skill-benchmark-exemption.md` 全文; `standards/conventions/secret-hygiene.md` 全文; `standards/conventions/version-management.md` (15-75 与 §4.3 相关行)。
  - `.aria/state-checks.yaml` 中四条版本类 check; `.aria/config.json` 的 audit 块。
  - `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` 中启用守卫相关行; `openspec/archive/2026-07-11-secret-guard-bash3-multiline-hardening/proposal.md` 中 bash 3.2 相关行。
- 研究笔记 (背景材料, 不当证据): `cc-hooks.md` 全文; `secret-guard.md` 全文; `secret-scan.md` 1-420 与 492-797; `precedent.md` 1-339。
- 平台事实: 本机 Claude Code 2.1.285 二进制, 用 mmap 做只读字符串探针 (`binprobe.py`)。
- 实跑环境: 全部在 `scratchpad/audit/post_spec-R1-tech-lead/` 下 `cp -a` 出的副本上进行, HOME 指向该目录的 `home/`。命令只作为字符串喂给 hook 的 stdin, 从不执行; 像凭据的值由 `secrets` 在进程内生成, 不打印。
- 实跑脚本: `l1probe.py` + `cases1.tsv`、`perfprobe.py`、`inject.py`、`parse_matrix.sh`、`l3dollar.py`、`w12check.py`、`readcost.py`。
- 收尾核验: 真仓 `git status` 干净, HEAD 仍为 `47aa15f`。

## Findings

### C1 [e8d39a8a] critical · issue · implementation · proposal.md What.W3

**summary**: W3 把 `$` / `<` / `{{` 值前缀放行延伸到既有 `json-secret-field`, 且被放行的 span 仍被哨兵消费。结果是基线能检出的「既有键 + 以 `$` 或 `<` 开头的真实值」(bcrypt / crypt 哈希、带符号的生成口令) 变为静默: 检出回退, 且没有任何 SC 能看见。

**证据**:

- proposal.md:77 原文: 「值以下列任一开头即不计数: … `<`、`$`、`{{` … 被放行的 span 仍被计数哨兵替换, 后序 tag 看不到它。**作用范围** = 6 个新 tag + 既有 `json-secret-field`」。
- proposal.md:56 把新 tag 排在 `json-secret-field` 之后、`bcrypt-hash` 之前。
- proposal.md:83 的已知限制只写了「以白名单词开头的真凭据会被放过 (须人为构造)」。
- 源码:
  - `secret-scan.sh:227`: `json-secret-field` 的值是 `"[^"]{8,}"` (任意字符)。
  - `:230`: `bcrypt-hash` 排在其后。
  - `:296-300`: 命中即用 `sed` 替换为 `<secret-scan-counted:TAG>`。
- 实跑 `l3dollar.py`, 基线副本, 值在运行时生成, 每例 3 次 (输出原样):
  ```
  json:password=<bcrypt $2b$12$...>                    -> exit=0 alert m=1 {json-secret-field=1} ; exit=0 alert m=1 {json-secret-field=1} ; exit=0 alert m=1 {json-secret-field=1}
  json:secret=<sha512-crypt $6$...>                    -> exit=0 alert m=1 {json-secret-field=1} ; ... (3/3 同)
  json:password=<generated pw starting with $>         -> exit=0 alert m=1 {json-secret-field=1} ; ... (3/3 同)
  json:client_secret=<generated pw starting with $>    -> exit=0 alert m=1 {json-secret-field=1} ; ... (3/3 同)
  json:password=<generated pw starting with <>         -> exit=0 alert m=1 {json-secret-field=1} ; ... (3/3 同)
  bare bcrypt line (control)                           -> exit=0 alert m=1 {bcrypt-hash=1} ; ... (3/3 同)
  ```
- SC-29 的零回归网看不到这一点:
  - `secret-scan.test.sh:122` 是套件里唯一的 bcrypt 夹具, 形状是非 JSON 的 `password_hash=$2b$…`, 走的是 `bcrypt-hash`。
  - 全套件中「`json-secret-field` 键 + 以 `$` 或 `<` 起头的值」的夹具数为 0 (脚本计数)。
  - SC-7 与 SC-11 11t 的反向守卫, 值全是字母或数字起头。
- 10CG/aria-plugin#154 评论 19339 规定的白名单只有 `FAKE` / `PLACEHOLDER` / `NOT-REAL` / `[REDACTED`; `$`、`<`、`{{` 是本 Spec 自己加的。

**失败场景**: 实现者照 :77 字面实现:

1. 对 `{"password":"$2b$12$…"}`, `json-secret-field` 取出的值是 `$2b$…`, 以 `$` 起头, 所以不计数。
2. 整个 span 仍被哨兵替换, 后面的 `bcrypt-hash` 看不到它。
3. 结果: 整条静默, 而基线是告警。

任何以 `$` 或 `<` 起头的生成口令, 只要落在 10 个既有键上, 同样由告警变为静默。此时探针目标态仍是「全部 yes」, SC-29 仍全绿, 验收会放过这个回退。

**三态**: 建议新增 reverse-guard 行 `json:password=<bcrypt>` 与 `json:client_secret=<以 $ 起头的 20 位生成口令>`, 期望为告警:

- 基线: yes (已实测);
- 好实现: yes;
- 照 :77 字面的实现: no, 转红。

**建议修法**:

1. 对既有 `json-secret-field`, 只套 19339 列出的标记前缀, 外加**精确**的哨兵前缀 `<secret-scan-counted:`。
2. 对新 tag, 也把 `<` / `$` 收窄为「整个值就是占位或变量引用」的形状: 整值 `<…>`、整值 `${…}` / `$(…)` / `$[A-Za-z_][A-Za-z0-9_]*`, 而不是只看首字符。
3. 把「放行 span 是否仍被消费」以及它与 `bcrypt-hash` 的先后关系写成明文。
4. 改写 :83: 以 `$` / `<` 起头的真实值不是「须人为构造」。
5. 把上述 reverse-guard 行补进探针。

按以上收窄后, SC-8、SC-9 9e / 9l / 9m、SC-11 11f / 11g / 11h / 11m–11r 的期望都不变。

### C2 [7e0343bd] critical · issue · architecture · proposal.md What.W9

**summary**: W9 的扩展代码有一部分必须跑在 per-segment 子 shell 之外: Read/Edit 面, 以及供两面共用的项目根解析与加载。那里一旦发生运行期故障, 脚本以 exit 1 结束, PreToolUse 视为「继续执行」, 内建拦截会一起失效。

- W14 断言「新代码任何未绑定变量都会让所有 Bash 命令 fail-closed」, 这只在子 shell 内成立。
- W9 的两条保证都没有机制兜底, 验收也测不到: 「从不因扩展问题 exit 2」和「内建规则不受扩展影响」。

**证据**:

- 两处文字冲突:
  - proposal.md:131: 「从不因扩展问题 exit 2 … 这**不是**整体 fail-open: 内建规则的判定与其 fail-closed 路径不受扩展影响」。
  - proposal.md:189: 「新代码里任何未绑定变量都会让**所有** Bash 命令 fail-closed」。
- proposal.md:128: 项目根要回落时, 需对 stdin 再做一次 jq 取 `cwd`, 且结果要同时服务 Read/Edit 面。
- 源码:
  - 唯一把故障映射为 exit 2 的地方是 `secret-guard.sh:1111-1120` 的 `( _sg_per_segment_eval "$command" )`, 只包住 Bash 判定。
  - Read/Edit 分派 `:631-694` 在主体里, 不在任何子 shell 内。
  - 全文件没有 `trap` (grep 为 0 行)。
- 平台事实 (本机 2.1.285 二进制文档串原文): PreToolUse 「Exit code 0 - stdout/stderr not shown. Exit code 2 - show stderr to model and block tool call. Other exit codes - show stderr to user only but continue with tool call」。
- 实跑 `inject.py`: 在副本里注入 `: "${W9_EXT_UNSET_VAR}"`, 代表扩展代码中的一个未绑定变量 (输出原样):
  ```
  variant                            Bash cat .env | Bash ls -la | Read /x/.env | Read /x/README.md | Edit /home/u/.ssh/id_rsa
  baseline                           exit=2        | exit=0      | exit=2       | exit=0            | exit=2
  unbound@readedit_branch            exit=2        | exit=0      | exit=1       | exit=1            | exit=1
  unbound@main_before_dispatch       exit=1        | exit=1      | exit=1       | exit=1            | exit=1
  unbound@inside_judge_subshell      exit=2        | exit=2      | exit=2       | exit=0            | exit=2
  ```
- 测试内 SC-20 (`secret-guard.test.sh:1089-1146`) 只在 `_sg_compute_credit` 的 wc 段和 `_sg_safe_to_split` 的 `local nl` 两处注入, 触发命令只有 Bash `cat /opt/.env`。它不覆盖 Read/Edit 面, 也不覆盖主体。
- 本 Spec 的 SC-20 (proposal.md:234) 测的六种情形是**坏输入文件**, 不是**坏代码**。另外 W9 的失败清单列了「不可读」, SC-20 却没测。

**失败场景**:

- 落点一 (最自然): 在主体里解析一次项目根、加载扩展, 供两面共用, 对应上表的 `main_before_dispatch`。只要加载或匹配代码在 SC-19 / SC-20 没覆盖的分支上 (如「不可读」文件、`CLAUDE_PROJECT_DIR` 指向不存在的目录、超长行) 触发未绑定变量:
  - `Read .env`、`Edit ~/.ssh/id_rsa`、`cat .env` 的退出码都由 2 变 1, 即全部放行, 这是安全回退。
- 落点二: 把扩展匹配放进子 shell 内的 `_sg_judge_one`。同样的故障会让所有 Bash 命令 exit 2, 恰是 W9 自己引用的 10CG/Aria#154 死锁类。

两种落点都能满足现有全部 SC。

**三态**: 建议新增「扩展代码故障注入」检查, 性质同 SC-30, 属探针外检查; 也可以在探针里只在加载器存在时执行。做法: 在 B.2 的实现副本里对扩展加载器注入一个未绑定变量, 断言 `Read /x/.env`=2、`cat .env`=2、`Read /x/README.md`=0、`ls -la`=0。

- 基线: 没有加载器。对「仅内建」副本断言同样的值, 已实测为 2 / 2 / 0 / 0。
- 隔离良好的实现: yes。
- 在主体里裸加载的实现: no, 得到 1 / 1 / 1 / 1 (已实测)。

另外给 SC-20 补一对「不可读 (chmod 000)」。

**建议修法**:

1. 在 W9 写明隔离机制和失败方向。例如: 扩展的加载与匹配整体放进独立子 shell 或函数, 用显式返回码映射 (0 = 未命中, 2 = 命中, 其余 = 丢弃扩展、内建照常), 两面都走它。
2. 订正 :189: 那句断言只对子 shell 内的代码成立。
3. 按上面的三态补 SC 行。

扩展被丢弃时的可见性问题见 m6。

### C3 [e600e931] critical · issue · implementation · proposal.md What.W12

**summary**: W12 按字面把三行里的 `\.env` 改为 `\.env(rc)?([^A-Za-z0-9_]|$)` 后, `python3 -c` 中的整环境转储由拦变放, 包括 `print(os.environ)`、`dict(os.environ)`、`.items()`、`os.environ['X']`、`os.environb`。这类命令与 `printenv` 同类:

- hook 本来就拦 `printenv`;
- 本 Spec 的 W11 还新增拦 `ps e` 与 `/proc/*/environ`。

但 Spec 把 `os.environ` 整体当作误报处理。

**证据**:

- proposal.md 里的相关文字:
  - :166-167: 只改三行; fail 方向只提了 `.env_prod`。
  - :289: 「新放行」把 `os.environ` 列为一类, 没有区分「取值给代码用」和「打印整个环境」。
  - :237 (SC-23): 6 条 baseline-failing 全是安全形态 (`len(...)`、`sorted(...)` 只出键、`.get(...) is None`), 没有任何一行钉住转储形态。
- 规范: `secret-hygiene.md` §2.2 把「Show env | `env`, `printenv`, `set` (含 secret env vars 时)」列为受限命令。
- 源码: `secret-guard.sh:867-877` 拦截裸 `printenv` / `env` 及其各种包装形态。
- 实跑 `w12check.py`: 在副本上按 :166 字面只改 `:893` / `:894` / `:974` 三行 (输出原样):
  ```
  baseline | W12-literal | command
  exit=2   | exit=0      | python3 -c "import os; print(os.environ)"
  exit=2   | exit=0      | python3 -c "import os; print(dict(os.environ))"
  exit=2   | exit=0      | python3 -c "import os; [print(k, v) for k, v in os.environ.items()]"
  exit=2   | exit=0      | python3 -c "import os; print(os.environ['FORGEJO_TOKEN'])"
  exit=2   | exit=0      | python -c "import os; print(os.environb)"
  exit=2   | exit=2      | printenv
  exit=2   | exit=0      | python3 -c "import os; print(len(os.environ.get('HOME','')))"
  exit=2   | exit=2      | node -e "console.log(process.env)"
  ```
- L3 兜不住这类输出:
  - Python repr 的形状是 `'KEY': 'value'`, 键后先是 `'` 再接 `:`。
  - W2 的 `kv-secret-assign` (:59) 要求键后直接接空白和 `=` / `:`。
  - `json-env-secret-key` (:58) 要求双引号 JSON 键。

**失败场景**: 照 Spec 实现后, 会话里一条 `python3 -c "import os; print(os.environ)"` (例如排查环境变量) 会被放行, 把 shell rc 导出的 `FORGEJO_TOKEN` 等整个环境打进 tool output; 探针与 SC-29 仍全绿。

**三态**: 建议新增 reverse-guard 行: `python3 -c "import os; print(os.environ)"`、`print(dict(os.environ))`、`os.environ.items()`, 期望 exit 2。

- 基线: yes (已实测);
- 好实现: yes;
- 照 :166 字面的实现: no (已实测为 exit 0)。

**建议修法**:

1. 保留三行的边界修复: 10CG/Aria#221 报告的 `os.environ.get(...)` 误报确实该消。
2. 另加一条窄的「Python 整环境转储」行, 覆盖 `print(` / `dict(` / `json.dumps(` 直接包 `os.environb?`, 以及 `os.environb?.(items|values|copy)(`。这样 SC-23 的 23a–23c 仍然放行。
3. `print(os.environ['X'])` 如果不拦, 就作为 KNOWN-LIMIT 钉住, 并在 :289 如实申报。
4. W12 讲 fail 方向的那段补上这一类。
5. 若 owner 知情后选择整体放行, 也必须用 KNOWN-LIMIT 行钉住, 并在 Impact 写明「新放行: Python 整环境转储」。

### M1 [44b5bb44] major · issue · testing · proposal.md SC-32

**summary**: SC-32 把「bash 3.2 可跑」缩成对 5 个构造的静态 grep。而 bash 版本不兼容造成的**解析类**错误, 会让脚本以「上一条命令的退出码」结束, 即 0 或 1, 对 PreToolUse 来说就是放行:

- 退出码 0 时, stdout 与 stderr 都不显示, 完全静默;
- 退出码 1 时, 只给用户看 stderr。

两种情况都放行。其后果是一整层防护无声失效, 而不是 10CG/Aria#154 那种看得见的死锁。

**证据**:

- proposal.md:64 与 :249: 只要求代码行里不出现 `declare -A` / `mapfile` / `readarray` / `${x,,}` / `${x^^}`。探针 `baseline_probe.py:935-946` 也只查这些。
- 实跑 `parse_matrix.sh` (bash 5.2)。用 5.2 不认识的 `[[ -Q ... ]]` 与 `${y@Z}`, 代替 3.2 不认识的 `[[ -v ]]` 与 `${x@Q}` (输出截断):
  ```
  cond_prior0 placement=top rc=0 stdout=[] stderr=[pm_cond_prior0.sh: line 4: conditional binary operator expected|]
  cond_prior1 placement=top rc=1 stdout=[] stderr=[pm_cond_prior1.sh: line 4: conditional binary operator expected|]
  subst_prior0 placement=top rc=1 stdout=[] stderr=[pm_subst_prior0.sh: line 4: ${y@Z}: bad substitution|]
  tok_prior0 placement=top rc=2 stdout=[] stderr=[pm_tok_prior0.sh: line 4: syntax error near unexpected token `;'|...]
  cond_func placement=func rc=0 ...
  cond_sub placement=subshell rc=0 ...
  ```
- `inject.py` 的变体 `parse_error_fn_above_gate`: 在副本的闸门上方加一个含该构造的新函数, 五个用例全部 `exit=0`, 其中包括 `cat .env`、`Read /x/.env`、`Edit ~/.ssh/id_rsa`。
- 函数在定义时即被解析, 所以把调用放进子 shell 也救不了 (`cond_sub` 的 rc=0)。
- 先例 `openspec/archive/2026-07-11-secret-guard-bash3-multiline-hardening/proposal.md:111` 的 bash 3.2 夹具是 `BASH_ENV` + `enable -n readarray mapfile`, 只模拟缺内建命令, 不模拟语法差异。
- 本机没有 bash 3.2, 本条关于 3.2 的行为是按同一解析错误类推断的 (见「风险 / 疑问」)。

**失败场景**: W9 / W10 / W2 / W4 是本仓最复杂的新 bash 代码。只要实现者用了以下任一构造: `[[ -v VAR ]]`、`${x@Q}`、`declare -n` / `local -n`、`${arr[-1]}`、`|&`、`&>>`:

- 在 Linux 上, 全部 SC 都是绿的;
- 在 macOS 的 `/bin/bash` 3.2 上, secret-guard 对 Bash / Read / Edit / Write / MultiEdit 全部以 0 或 1 退出, 即无声放行;
- secret-scan 则静默, 不再告警。

**三态**: SC-32 现状下:

- 基线: yes;
- 好实现: yes;
- 用了 `[[ -v ]]` 的坏实现: **yes**, 测不出来。

**建议修法**:

1. B.1 准备一个 bash 3.2 (源码编译或容器), 至少对两个 hook 跑一次 `bash -n`。
2. 用它跑 L1 的代表子集: `cat .env`→2、`ls`→0、`Read .env`→2。三态预期: 基线 yes / 好实现 yes / 坏实现 no。
3. 把静态清单扩到上面列出的构造, 并写明它只是启发式检查。

### M2 [e2459206] major · issue · architecture · proposal.md What.W11

**summary**: W11 为 `ps` 族新增了 `nomad alloc exec` / `pct exec` / `ssh` 外壳包裹, 但同一批包裹下的 `env` / `printenv` 整环境转储在基线就放行, Spec 既不补也不申报。对照之下, `docker exec … env`、`kubectl exec … env`、`podman exec … env`、`lxc exec … env` 都已经被拦。

**证据**:

- proposal.md:152 的包裹清单含 `nomad alloc exec` 与 `pct exec`。
- proposal.md:158「同族的进程环境读取」的纳入与不纳入两张清单里, 都没有「经 exec 包裹的 `env` / `printenv`」; 全文 `printenv` 出现 0 次。
- 源码:
  - `:858` docker exec 下的 env/printenv, `:862-863` kubectl exec, `:938` podman exec, `:940` lxc exec 都有对应的行。
  - 没有 nomad alloc exec 或 pct exec 的行。
  - `:867-877` 的裸 env/printenv 行要求出现在命令位置, 跟在包裹参数后面不会命中。
- 实跑 `l1probe.py`, 基线副本 (输出节选, 原样):
  ```
  exit=0	     87ms	B	nomad alloc exec -task server abc123 env
  exit=0	     90ms	B	nomad alloc exec -task server abc123 printenv
  exit=0	    102ms	B	pct exec 101 -- env
  exit=0	     77ms	B	ssh root@pve pct exec 101 -- env
  exit=2	     65ms	B	docker exec forgejo env
  exit=2	     54ms	B	kubectl exec pod -- env
  exit=0	     49ms	B	cat /proc/1/task/1/environ
  ```
- 本仓语境:
  - Aether 跑在 Nomad 上。
  - 10CG/Aria#221 评论 25898 里的命令正是 `nomad alloc exec -task server <alloc> python -c …`。
  - 10CG/aria-plugin#203 的事故链是 `ssh root@pve 'pct exec 101 -- …'`。
  - `secret-hygiene.md` §9 记录的 2026-05-02 事故, 就是任务运行时 env 外泄。

**失败场景**: 照 W11 字面实现后, `nomad alloc exec … ps aux` 被拦, 而暴露面更大的 `nomad alloc exec … env` 仍然放行。采用方读 Spec 会以为「进程 / 环境族」已经覆盖。SC 对这类命令两边都不钉: 既没有 baseline-failing 行, 也没有 known-limit 行。

**建议修法**:

1. 在 W11 新增的包裹行里, 把 `env|printenv` 与 `ps` 族并列。用的是同一批包裹, 不扩大范围。
2. 补 SC-22 的 baseline-failing 行: 上面前四条, 期望 exit 2。再补 allow 行, 如 `nomad alloc exec … ls`。
3. 若决定不纳入, 至少加 KNOWN-LIMIT 行钉住现状, 并放进建议开单清单。
4. 放宽 `/proc` 行的 pid 位时, 一并考虑 `/proc/<pid>/task/<tid>/{environ,cmdline}`。

### M3 [d8e7b380] major · risk · architecture · proposal.md What.W14

**summary**: L1 的 5 秒超时等于放行: Spec 自己在 :337 承认了这点, 研究笔记有活体证据。本 Spec 有多处在加延迟:

- W8 / W11 新增的重正则行;
- W9 每次调用都要读扩展文件, 可能还要多做一次 jq;
- W10 对含 `$` 的段再判一遍替换后的副本。

但没有任何 SC 约束这些新路径的延迟, 也没有钉住「新增判定不得推迟既有判定」的求值顺序。SC-30 的五档都不经过这些路径。

**证据**:

- proposal.md 里的相关文字:
  - :188: 只沿用测试内 SC-8 的五档, 加上结构预算 145→150, 以及 L3 预算「B.2 实测记录」。
  - :142: W10「额外判一次替换后的副本」, 没规定它与原判定谁先谁后。
  - :337: 超时即放行。
- `hooks.json:33`: secret-guard 的 `timeout: 5`。
- 实跑 `perfprobe.py`, 基线副本, 负载约 1, 取中位数 (输出原样):
  ```
  whole-mode script   6385B  original: exit=0   0.60s | pre-substituted copy: exit=0   0.76s | sum=  1.37s
  whole-mode script   9525B  original: exit=0   1.18s | pre-substituted copy: exit=0   1.48s | sum=  2.66s
   600 simple segments: exit=0   3.69s
  ```
  「预替换副本」用来近似 W10 的第二遍判定。研究笔记另有数据: 新增行每段 +1.5–3.5 ms; 负载下「8 赋值 + 40 引用」的命令从 1.7s 变为 3.9s。这两个数是背景材料, 不是本条的证据。

**失败场景**: 有两种实现会把时间预算耗掉:

- 按段交错执行: 段 1 原判, 段 1 替换副本判, 然后段 2 原判……
- 在主体里先做扩展加载。

这样, 一条原本能在 5s 内判到末段 `cat .env` 并拦下的长命令, 会被推过 5s, 超时即放行。这是「原判定不变」在时间维度上被破坏, 而所有 SC 仍是绿的。

**建议修法**:

1. 在 W10 / W9 写死求值顺序: 所有段先按内建规则判完, 再走替换副本和扩展。
2. 在 SC-8 之外新增延迟 SC 行, 不改 SC-8 的阈值和档位:
   - 600 段、末段直接命中: 必须仍然 exit 2, 且耗时 ≤ 基线 ×1.5;
   - 9.5 KB 整串、含赋值与 `$VAR`: 耗时 ≤ 基线 ×2.5;
   - 200 条扩展 + 普通命令: 给出耗时增量上限。
3. 把待开单 #1 标为本 Spec 的前置风险, 不只是附带开单。

### m1 [5ac56a9f] minor · decision · documentation · proposal.md What.W11

**summary**: W11 否决 `updatedInput` 的第一条理由前提偏弱。那条理由是「多个 hook 并行改写时最后完成者生效; 本仓 Bash matcher 下已有两个 hook」, 但另一个 hook 从不产出 `updatedInput`。否决的结论 (选拒绝) 仍可由「静默改写违背使用者意图」单独支撑。

**证据**:

- proposal.md:157。
- `hooks.json:28-39`: Bash matcher 下是 secret-guard 与 host-docker-logout-guard 两个 hook。
- `host-docker-logout-guard.sh` 对 `updatedInput|permissionDecision|hookSpecificOutput` 的 grep 为 0 命中, 只有 exit 0 / 2。

**失败场景**: 不影响实现, 但 owner 复议时可能被一条不成立的平台理由说服。

**建议修法**: 改为「采用方可能另装会改写命令的 hook, 那时存在竞态; 本仓当前没有」, 把主理由放在保持使用者意图上。

### m2 [efd4c1c5] minor · issue · documentation · proposal.md 待 owner 复议.7

**summary**: Grep 工具是 W8.3 / W9 所加 Read 面保护的同族旁路: 两层 hook 的 matcher 都不含 Grep。Spec 只在待开单 #7 记了 L3 这一侧, L1 这一侧没有申报。而 SC-31 31d 冻结了 hooks.json, 本 Spec 结构上也没法修。

**证据**:

- `hooks.json:43`: PreToolUse matcher 为 `Read|Edit|Write|MultiEdit`。
- `hooks.json:55`: PostToolUse matcher 为 `Bash|Read|Edit|Write|MultiEdit`。
- proposal.md:343 只写了「secret-scan matcher 缺 Grep」。
- `l1probe.py` 把 Grep 负载喂给副本, 结果是 exit 0, 落在 `secret-guard.sh:698-699` 的 `*) exit 0`。实际上 Grep 调用根本不会触发这个 hook。

**失败场景**: 采用方把敏感路径写进 `.aria/secret-guard.paths` 后, 以为 AI 读不到这些文件; 但 Grep 工具以 `output_mode content` 输出内容时, 两层都不经过。

**建议修法**: 在 W8 与 W9 的已知限制里各加一句, 并把待开单 #7 扩为「两层 matcher 都缺 Grep」。

### m3 [f410df76] minor · issue · documentation · proposal.md Impact

**summary**: 版本定级的引文不准确, 发版同步面清单也漏了点。

**证据**:

- 引文:
  - proposal.md:285 写「依据 CLAUDE.md §版本管理 (新增能力 = MINOR+ …)」。
  - CLAUDE.md:79 原文是「新增 Skill / Skill 架构重构 = MINOR+」。
  - 真正能支撑 MINOR 的是 `version-management.md` §2.2「功能增强 (向下兼容)」。
- 同步面:
  - proposal.md:292 列的主仓版本点只有 VERSION、root README badge 与两份架构文档。
  - `git grep -F 1.74.1` 还命中: `README.md:242`; 三份 i18n README 的 `:10` badge 与 `:244` Plugin Version 行; `CLAUDE.md:138/:142`。
  - 这些点都不在机械兜底范围内: `m6-version-badge-match` 只取 README.md 的首个 badge, `plugin-version-arch-docs-match` 只看两份架构文档。

**失败场景**: owner 复议第 6 条时, 看到的是被改写过的 SOT 措辞; task-planner 照 :292 派生发版任务会漏掉这些点。

**建议修法**: 把引文改为 version-management.md §2.2; :292 改为列全版本点, 或直接指向 10CG/Aria#195 TASK-030 的清单。

### m4 [68e80369] minor · issue · documentation · proposal.md What.W4

**summary**: 「键形 tag 取分隔符之后的值, 其余 tag 取整个 span」里, 「键形 tag」没有定义: `env-line-secret-keyword`、`bearer-token`、`x-api-key-header` 和各 URL 类 tag 算不算?

- 取整个 span 的 tag, 其指纹无法与 pat-inventory 台账比对。
- 这与 :89 把「可比性」当作不加盐的理由自相矛盾。

**证据**: proposal.md:88-89; `secret-scan.sh:212-224` 这些 tag 的 span 都带键名、头名或 URL scheme。

**建议修法**: 列出按「值」取指纹的 tag 全集, 建议凡有明确值位的 tag 都只哈希值; SC-12 再加一行非 JSON 的 tag, 如 `Authorization: Bearer`。

### m5 [684e9a24] minor · issue · documentation · proposal.md What.W9

**summary**: 扩展条目在 Bash 面只对 W8 的打印型读取器组生效, 不含 W8 自己为 `app.ini` 扩充的 `python3 -c` / `node -e` 源组。这种不对称没有申报。

**证据**: proposal.md:118 (W8 把 app.ini 并入 `:893` / `:894` 源组) vs :130 (扩展只认打印型读取器)。

**建议修法**: 要么同样扩到这两行, 要么写进 W9 的已知限制, 并加一行 KNOWN-LIMIT。

### m6 [ab625935] minor · decision · architecture · proposal.md What.W9

**summary**: 扩展的「超限整体忽略 + 静默」是一道悬崖: 加上第 201 条, 前 200 条会一起失效, 而且没人知道。平台其实有现成的用户可见通道: 所有 hook 都能用 `systemMessage`, exit 0 时也有效。Spec 没考虑它, 直接把可见性推给另开单的 aria-doctor。

**证据**: proposal.md:131 / :136 / :137; 本机 2.1.285 二进制文档串原文「`systemMessage` - Display a message to the user (all hooks)」。

**建议修法**: 扩展被丢弃时, 以 exit 0 + stdout `{"systemMessage": "[secret-guard] .aria/secret-guard.paths ignored: <原因>"}` 告知用户, 消息里不含条目内容; 并在「截断 + 告警」与「整体忽略 + 告警」之间给 owner 一个明确的选项。

### m7 [bdf4778c] minor · issue · documentation · proposal.md Out of scope

**summary**: SC-28 订正了 `secret-scan.sh` 头注释里的多处陈旧陈述, 却保留了 `:15-20` 这一句: 「Claude Code exposes no field to replace tool_response … not a version-dependent behaviour」。它与本 Spec 在 :40 引用的二进制实测直接矛盾。

**证据**: proposal.md:40 与 :197; `secret-scan.sh:15-20`; 二进制里有 3 处 `Replaces the tool output before it is sent to the model`。

**建议修法**: 不必等第 1 条复议, 先把该句改为「该字段存在于 schema (≥ v2.1.220), 端到端未验证, 本 hook 不使用」; 其余「cannot redact」的表述随复议结论再定。

### m8 [60eea71e] minor · issue · testing · proposal.md SC-26

**summary**: SC-26b 写的是「§2.5 有一行含 `pgrep -a`」, 但探针实际是对整个文件的任意一行判定。

**证据**: `baseline_probe.py:822-827`, 判定为 `ok = any("pgrep -a" in l for l in t.splitlines())`。

**三态**:

- 基线: no;
- 好实现: yes;
- 把 `pgrep -a` 写进 §3 正例、而 §2.5 没加的坏实现: **yes**, 测不出来。

**建议修法**: 只在从 `### 2.5` 到下一个 `### ` 之间的区段里判定。

## 对执笔人自报薄弱点与请裁项的表态

**执笔自报薄弱点**

1. SC-30 没有探针基线 — **可接受**。计时闸与依赖 git 历史的用例本就不适合逐字节复现; 任务 1.1 已要求 B.1 在改代码之前实测并记入 handoff。
2. 目标态的自扫描只能在 B.2 验证 — **可接受**。但按 C1 收窄后 `<` / `$` 规则会变, 15e / 15f 要按新规则重验。
3. W2 的最终设计没在语料上普查过 — **可接受**, 条件是 B.2 用同一语料对最终设计复跑, 把新增告警文件的清单与数量写进 handoff。不设阈值, 但结果必须可复算。
4. W11 的外壳包裹形态没有原型 — **可接受**。SC-22 的 22n 与 22y–22E 已经可证伪, 可行性风险在 B.2 暴露即可。新增重行对延迟的影响见 M3, 包裹族的缺口见 M2。
5. W9 的项目根语义 — **可接受** (就「怎么取项目根」而言)。本机二进制文档串原文写明: 「a guard that inspects the project must use $CLAUDE_PROJECT_DIR or the cwd field on stdin」, 两级回落有平台依据。故障隔离是另一个问题, 见 C2。
6. SC 钉得很紧 — **可接受**。「恰好等于」正是可证伪的前提; 若要改措辞或 tag 名, 走 Spec 变更是正确的代价。
7. 用例规模 (326 行) — **可接受**。
8. rule6_note 块 B 的归类 — **可接受**, 见下面第 8 条。
9. Level — **可接受**, 见下面第 4 条。
10. 头部的 `linked_issue_overlap` 取自派单 — **可接受**。派单背景写明主控已核验 claim 与协调 ref; 建议 handoff 附上 gate 输出原文的指针。

**待 owner 复议 · 产品级**

1. L3 是否升级为「检测 + 脱敏」 — **可接受**默认的选项 A, 也认同推荐的选项 B (spike 另立)。补一句: 若将来做脱敏, C1 这类白名单错误会从「漏告警」升级为「漏脱敏且无告警」。所以无论选哪个选项, C1 的收窄都是前提。
2. 拒绝文案 — **可接受**选项 A。改全局共用的 heredoc 会失去 2026-08-02 的可证伪锚点, 还会污染无关的拦截; 选项 C 依赖 10CG/aria-plugin#132。
3. 10CG/aria-plugin#203 与 10CG/Aria#221 的收尾 — **可接受**理解 A。决策单第 4 项授权了 WP-A 的 issue 评论, 第 2 项的「本项之下」指的是轮换话题。条件: 评论只写代码侧的覆盖范围与 KNOWN-LIMIT, 一字不提轮换状态, 两张单都保持 open。
4. Level — **可接受**维持 Level 2。本轮发现的 C2 / M1 / M3 与 2026-07-11 先例的 blast radius 论证同形; 但升到 Level 3 只多一份 tasks.md, 并不能降低这些风险, 降风险靠补 SC 行。不建议拆分: L1 与 L3 共用探针与发版面, 拆开会自造接缝。
5. 进程表拦截会改变日常习惯 — **可接受**。`ps aux | grep` 恰是 10CG/Aria#221 的泄露形态, 替代写法 Spec 已申报。
6. 版本定级 — **可接受** MINOR; 引文按 m3 改正。
7. 建议开单清单 — **可接受**, 另补四条: L1 侧的 Grep (m2); 经 `nomad alloc exec` / `pct exec` 的 env 转储 (若 M2 不在本 Spec 内修); `/proc/<pid>/task/<tid>/*`; bash 3.2 运行腿 (M1)。并建议提高第 1 条「超时即放行」的紧迫度, 因为本 Spec 在增加延迟 (M3)。

**待 owner 复议 · 技术级 (AI 已裁)**

8. rule6_note 分两块, 块 B 判第 1 行 — **可接受**。块 B 插入的是运行期事实 (tag 名、工具名、路径), 没有指示行为的措辞; 处方句由 SC-13 13d 逐字节钉住。W13 的条款落在 standards 规范里, 不是 Skill 的运行时指令面, 与 2026-08-02 先例一样归入块 A。
9. W2 (封闭键表、大小写、值长门槛、熵下限) — **可接受**。
10. W3 (按值前缀的白名单) — **不可接受** (按现行文字)。`$` / `<` / `{{` 的首字符规则延伸到既有 `json-secret-field`, 造成检出回退 (C1)。对新 tag 来说, 它还把「以 `$` 或 `<` 起头的真实随机值」这个自然的漏报类, 错写成了「须人为构造」。按 C1 收窄后可接受。
11. W4 — **可接受** (16 字符门槛与追加字段的做法); 但「键形 tag」须补定义 (m4)。
12. W7 (源头拼装夹具) — **可接受**。不给任何路径豁免是对的, 这样不会留下「真实泄露只进日志」的盲区。
13. W8 (本次只做 app.ini 族) — **可接受**, 语料证据确实不足以扩大名单; 但 Grep 旁路须申报 (m2)。
14. W9 — **部分不可接受**。纯文本、字面子串、项目根的回落顺序都可接受; 但「扩展失败只丢扩展」没有机制兜底, 且与 W14 的断言矛盾 (C2); 「超限整体忽略 + 静默」见 m6。
15. W11 — **可接受**「拒绝」这一决策 (理由的修正见 m1); 包裹族须补 env / printenv (M2)。
16. W12 — **部分不可接受**。`[^A-Za-z0-9_]` 边界与 `(rc)?` 可接受; jq 的锚定写法也可接受 (24h 钉住它不扩大既有漏洞)。但把 `os.environ` 整体放行, 把整环境转储也一起放掉了 (C3)。
17. 探针在无 git 副本上跑, git 腿放到 SC-30 — **可接受**。可复现性优先, git 腿在 B.1 实测。

## 风险 / 疑问

- 本审计有一次 Bash 输出触发了真实的 L3 告警 (`DETECTED 3`)。原因是我打印了 `aria/hooks/tests/secret-scan.test.sh:118-121` 这几行仓内公开的测试夹具, 而我的消隐正则没覆盖到。这些不是凭据, 没有真实凭据外露, 无需轮换。
- M1 中 bash 3.2 的行为, 是用 bash 5.2 模拟同一解析错误类推出来的, 本机没有 3.2。结论方向 (退出码为 0 或 1, 而不是 2) 需要 B.1 在真实 3.2 上确认一次。
- W1 让每次 Read 都走完整扫描。在基线模式集下, 我测得每次 Read 约多 0.09s (`readcost.py`: 4–60 KB 时, 0.10s → 0.19s), W2 分类器与 W4 哈希还会再加。
  - Impact 没有申报这项开销。
  - 在 Windows Git-Bash (10CG/aria-plugin#203 报告者用的是 MINGW64) 上, 进程派生慢一个量级, 而 secret-scan 超时即静默丢告警。本轮没能实测。
- whole 模式下 tight 是整串级的: 一段脚本里只要出现进程表形态或 app.ini 名, 整串的 grep / sed / cut / awk credit 就全部关闭。这会新增一类误拦, Impact 没有列出。具体程度取决于 tight 触发怎么实现, 未实测。
- W11 否决 `ask` 时没有提到 v2.0 的无人值守运行时: Layer 2 容器里没有人能回答 `ask`。补上这条理由会更扎实。`ask` 在 headless 模式下的实际行为我没有核验。
- 关于与 10CG/Aria#199 的接缝: 它的完整性门只在 `pre_merge != off` 时执行, 本仓是 off (已读 `.aria/config.json` 与其 proposal 的 F1)。所以除了串行发版之外没有额外接缝, Spec 现有的表述够用。

## Verdict

- verdict: **FAIL**
- counts: **3C / 3M / 8m**
- **Vote: REVISE**

## 是否足以进入 A.2

**不足以**。C1 与 C3 是照 Spec 字面实现就会发生的检出 / 拦截回退; C2 使 W9 无法按 Spec 所声称的失败方向实现。三者都要先改 W3 / W9 / W12 及对应的 SC 行, task-planner 才有稳定的输入可以派生任务。
