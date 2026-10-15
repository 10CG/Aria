# edits_v6_b.py -- W8, W9, W10, W11, W14, Out of scope.   Executed by apply_edits_v6.py (shares sub1 / after / NUM / t).

# ---------------------------------------------------------------- W8
sub1("按名字拦截的固有上限, 输出侧由 W1 + W2 兜底)", "按名字拦截的固有上限, 输出侧由 W1 + W2 兜底, 成功与失败的调用都经 L3: W1 的失败事件)")
sub1("表外读取器 (`bat`) —— 基线 `.env` 族对其中多数各有专行, `app.ini` 族没有, 输出侧由 W2 的 `kv-secret-assign` 兜底。",
     "表外读取器 (`bat`、`expand`、`unexpand`、`shuf`、`split`、`csplit`) —— 基线 `.env` 族对其中多数各有专行 (表外读取器也被它拦), `app.ini` 族没有, 输出侧由 W2 的 `kv-secret-assign` 兜底 (含失败的调用)。")

# ---------------------------------------------------------------- W9
sub1("项目根 = 非空的 `CLAUDE_PROJECT_DIR`; 否则 stdin 的 `cwd`", "项目根 = 非空的 `CLAUDE_PROJECT_DIR` (置空等同未设, SC-19 19ap); 否则 stdin 的 `cwd`")
sub1("默认大小写不敏感的文件系统上也不会因 ASCII 大小写漏拦)。",
     "默认大小写不敏感的文件系统上也不会因 ASCII 大小写漏拦)。**末行没有换行同样算一行** (SC-19 19an); **对清单与项目根路径的所有展开一律加引号** (项目根可以含空格、括号与非 ASCII 字符: SC-19 19ao)。")
sub1("扩展的函数在命令替换的子 shell 里调用它, 它的状态不泄回主 shell)。",
     "扩展的函数在命令替换的子 shell 里调用它, 它的状态不泄回主 shell; `_sg_core_eval` 在调用方的 locale 下运行 —— 扩展里的 `local -x LC_ALL=C` 只作用于条目读取、匹配与切片, 在各自的命令替换里, 不带进判定函数)。")
sub1("拒绝时复用同一份 BLOCKED 文案 (SC-25 25f), 不为扩展另写文案。",
     "拒绝时复用同一份 BLOCKED 文案 (SC-25 25f), 不为扩展另写文案; 其中 `Matched pattern:` 写 `(extension) .aria/secret-guard.paths`, `Command was:` 与 `Triggering segment:` 回显**原命令文本**, 替身名 `/etc/gitea/app.ini` 永不出现 (SC-25 25i)。")
sub1("- **已知限制**: 扩展失效是静默的; 继承内建判定的盲区与过拦 (见上语义);",
     "- **已知限制**: 扩展失效是静默的; **条目是字面子串: 完整路径条目对 `..` 回绕、`//`、`/./` 与 `cd` 后相对名的写法不命中, 只有最短的特征子串 (如文件名) 能覆盖** (文档要求写最短特征子串); 继承内建判定的盲区与过拦 (见上语义);")
sub1("`secret-guard.sh` 头注释一段。\n",
     "`secret-guard.sh` 头注释一段。§5.6 与 README 段各另写两件事: **保护边界** (覆盖面 = 内建 `app.ini` 行的读取器集 (29 个打印型读取器与 `python3 -c` / `node -e`) 加 Read / Edit; 重定向读 / `source` / `dd` / `xargs cat` / `find -exec` 等写法 (见 W8 已知限制)、Grep 工具、Write 与每条命令里第 64 处之后的出现不受保护) "
     "与 **「条目选最短的特征子串 (如文件名), 不要列完整路径」** (SC-26 26c / 26e 钉关键词)。\n")

# ---------------------------------------------------------------- W10
sub1("这些交给 L3 (W1 + W2 在输出侧兜底: 2026-09-26 事故泄露的那一行正是 SC-5 5a 的形态)。",
     "这些交给 L3 (W1 + W2 在输出侧兜底, 成功与失败的调用都经 L3: 2026-09-26 事故泄露的那一行正是 SC-5 5a 的形态)。")

# ---------------------------------------------------------------- W11
sub1("第 3 类 SysV `-f` / `-F` 簇; 第 4 类 `-o` / `--format` 列表含 `args|cmd|command`;",
     "第 3 类 SysV `-f` / `-F`: 任意位置含 `f` 或 `F` 的短横簇 (`-ef`、`-eF`、`-fp`) 且在**任意操作数位置** (`ps -p 123 -f`); 第 4 类 `-o` / `--format` 列表**任一位置**含 `args|cmd|command` (`-eo args,pid`、`-o pid,args,etime`、`--format cmd,pid`);")
sub1("`pgrep -a` / `--list-full`; `pstree -a` / `--arguments`; `top -c`;",
     "`pgrep` / `pstree` 的 `-a`: 任意位置含 `a` 的短横簇 (`-a` `-af` `-fa` `-la` `-ifa` `-pa` `-ua`) 且在**任意操作数位置** (`pgrep -u root -a`、`pstree -p -a`), 及 `--list-full` / `--arguments`; `top -c`;")
sub1("`docker ps --no-trunc` / `docker container ls --no-trunc` (及 `podman` 同形) (这些写法的各个拼写逐个出行: SC-22 22bl, podman 另见 22bb);",
     "`docker ps` / `docker container ls` 的 `--no-trunc` (出现在 `ps` / `ls` 之后的**任一位置**, 如 `docker ps -a --no-trunc`; 及 `podman` 同形) (这些写法的各个拼写逐个出行: SC-22 22bl, podman 另见 22bb, 簇内字母与操作数位置见 22bu, `-o` 列表见 22bv);")
sub1("数字 / 时长操作数 (`5`、`5s`)", "数字 / 时长操作数 (`5`、`5s`, 时长后缀 `s` `m` `h` `d` 逐个出行: SC-22 22bu)")
sub1("命令位置 = 行首、`;` `&` `|` `(` `{` 与反引号之后、控制字符 (含换行) 之后, 或 `then` `do` `else` `elif` 之后 (沿用 `secret-guard.sh:877` 的关键字位置约定, SC-22 22az)。",
     "命令位置 = 行首; 或下列字符之后: `;` `&` `|` `(` `)` `{` 反引号、控制字符 (含换行) —— 字符集与基线 env / printenv 行 (`secret-guard.sh:867-868`) 相同, 逐成员出行 (SC-22 22bt); 或 `then` `do` `else` `elif` 之后 (沿用 `secret-guard.sh:877` 的关键字位置约定, SC-22 22az)。")
sub1("这些包裹本 Spec 已为进程表家族加进规则; 基线对 `docker|kubectl|podman|lxc exec … env` 已拦, 而 `nomad alloc exec`、`pct exec`、不加引号的 `ssh`、`sh|bash -c`、`watch` 漏 (22ao–22ar、22bo)。",
     "这些包裹本 Spec 已为进程表家族加进规则。基线对其中 `docker` / `docker compose` / `kubectl` / `podman` / `lxc` 的 `exec` 另有各自的行, 覆盖面很窄: `secret-guard.sh:858` (docker) 要求 `env` / `printenv` 前是空白、后只接空白 / 行尾 / 分隔符 "
     "(引号形 `\"env\"`、带变量名的 `printenv NAME` 不在内); `:862-863` (kubectl) 要么带 `--`, 要么 `env` 之后是行尾或 `|` (引号形、`$(…)` 形、重定向形不在内); `:938` (podman) 要求 `env` 前是空白 (引号形不在内; `printenv NAME` 在内); "
     "`:940` (lxc) 要求 `--`。`nomad alloc exec`、`pct exec`、不加引号的 `ssh`、`sh|bash -c`、`watch` 基线没有行 (22ao–22ar)。新的转储备选覆盖**全部 11 个包裹**, 含上述五个基线包裹的引号形、`$(…)` 形、重定向形与不带 `--` 的 lxc 形 "
     "(22bo 逐个出行, 22by 另钉 `$(…)` 与重定向; 基线自己的写法留作反向守卫 22bw)。")
sub1("锚定的 `| grep '^X='` (读一个变量)、`| cut -d= -f1` (列变量名)、`| wc -l`、`>/dev/null` 放行 (SC-22 22br; 这是 10CG/Aria#221 评论 25898 称为正当核对的形态), `| grep -v x` 这类「整份环境减一行」的形态同样放行,",
     "`| cut -d= -f1` (列变量名)、`| wc -l`、`>/dev/null` 放行 (SC-22 22br; 这是 10CG/Aria#221 评论 25898 称为正当核对的形态: 读长度、读 env 变量名), 锚定的 `| grep '^X='` 沿用基线 docker / kubectl 行与共用 BLOCKED 文案 `Acceptable filters` 的口径放行 (22br; 前提是前缀安全, 对凭据名做锚定 grep 会打印其值: 与基线共享的限制), `| grep -v x` 这类「整份环境减一行」的形态同样放行,")
sub1("只拦裸 `env` / `printenv`, `env FOO=1 cmd` 这种 `env` 作 launcher 的形态放行 (22at);",
     "`env` 只拦裸 (`env FOO=1 cmd` 这种 `env` 作 launcher 的形态放行: 22at); **`printenv` 与基线一致, 带变量名也拦** —— 基线对命令位置的 `printenv NAME` 就拦 (`secret-guard.sh:867`), 外壳里的单变量读取与直接执行是同一个动作 "
     "(SC-22 22bx 对 11 个包裹逐个钉住; 「放行」是待复议 23 的备选);")
sub1("W2 之后其输出里的 `Authorization: token …` / `CF-Access-Client-Secret` 由 L3 检出 (SC-6 6g 同形)。",
     "W2 之后其输出里的 `Authorization: token …` / `CF-Access-Client-Secret` 由 L3 检出 (SC-6 6g 同形); 成功与失败的调用都经 L3 —— `systemctl status` 对未运行或失败的单元退出 3, 走失败事件 (W1)。")

# ---------------------------------------------------------------- W14
sub1("(f) / (f0): ≤ 1.5 × max(基线, 100 ms) —— 沿用测试内 SC-8 的 `max(100 ms, …)`: 基线只有几十毫秒时, 固定开销把比值放大;",
     "(f): ≤ 3.0 的纯比值上界 (参考设计约 @fB_r@ / @fR_r@ 倍, 每条条目起一个 grep 的坏实现 @bad_ext_perentry_fB_r@ / @bad_ext_perentry_fR_r@ 倍; 不用绝对地板: 地板让判据退化成「基线 CPU 约 0.09 s 以下」这一主机属性, 主机稍忙时正确实现会随机转红); "
     "(f0): ≤ 1.5 × max(基线, 100 ms) —— 沿用测试内 SC-8 的 `max(100 ms, …)`: 基线只有几十毫秒时, 固定开销把比值放大 (无扩展文件时只多一次命令替换, 参考设计约 @f0B_r@ 倍, 离上界远);")
sub1("(i3): ≤ 2.5 (长单行的匹配与取值是线性的: 固有开销与坏实现的实测倍数见第 5 项);",
     "(i3-a..e): ≤ 2.5 (长单行的匹配与取值是线性的: 固有开销与坏实现的实测倍数见第 5 项); (i3-f / g / h): ≤ 5.0 (300 KB 不带引号的 kv 值: 值的每个字节要过白名单 / 熵下限 / 路径形 / 点分链 / 指纹哈希若干遍线性判定, 固有开销约 @i3f_r@ 倍; 平方级的取值写法 @bad_val_quote_strip_i3-f_r@ 倍);")
sub1("8 KB 的空白串 (export 形)、8 KB 的 bearer 头值 (既有 tag);",
     "8 KB 的空白串 (export 形)、8 KB 的 bearer 头值 (既有 tag); **(i3-f / g / h)** 300 KB 不带引号的 kv 值三形 (`KEY = v`、`export KEY=v`、YAML `  KEY: v`; 基线对它们几乎不做事, 比值反映新 tag 的固有开销);")
sub1("新辅助函数放在 source 闸门之上, 并跑一次测试内 SC-20 风格的未绑定变量注入自测",
     "新辅助函数放在 source 闸门之上 (含基线函数体改名而来的 `_sg_core_eval`), 并跑一次测试内 SC-20 风格的未绑定变量注入自测")
sub1("- **其它耦合**: 测试内 SC-20 注入自测依赖的两段文本",
     "- **其它耦合**: 测试内 SC-8 的抽取装配 (`secret-guard.test.sh`: 先 `source` hook —— 只带入 source 闸门之上的函数 —— 再按锚点 `^_sg_judge_one\\(\\) \\{` / `^_sg_per_segment_eval\\(\\) \\{` / `declare -a risky_patterns=(` 抽三段) "
     "要求 `_sg_judge_one` 与 `_sg_per_segment_eval` 直接或间接调用的**全部**函数 —— 含 `_sg_core_eval`、`_sg_emit_blocked`、`_sg_vx_pass`、`_sg_ext_pass` 及其下游 —— 都定义在 source 闸门**之上** "
     "(基线已在闸门之下的 `_sg_redact_echo` 只产生被丢弃的回显文本, 保持原位); 这两个函数的名字与单独成行的 `}` 收尾格式不变。闸门之下的辅助函数会让该装配对 `_sg_per_segment_eval` 计到 rc=127 的瞬时返回, 五档延迟闸恒绿 "
     "(SC-30 30b 在探针内复刻该装配); 抽取方式、阈值、口径、档位一律不改 (owner 2026-08-24 决策); 测试内 SC-9a 直接运行新旧两份完整 hook 文件、不经抽取, 不受此约束。测试内 SC-20 注入自测依赖的两段文本")

# ---------------------------------------------------------------- Out of scope
sub1("- **Edit / MultiEdit 结果扫描**:",
     "- **失败事件上的脱敏与 matcher 之外的工具**: `PostToolUseFailure` 同 `PostToolUse` 一样只做检测 + 告警 (该事件的 `hookSpecificOutput` 只有 `additionalContext`, 没有 `updatedToolOutput`); matcher 之外的工具 (Grep / PowerShell) 的失败事件同样不在范围 (建议开单 7.7)。\n"
     "- **Edit / MultiEdit 结果扫描**:")
sub1("`docker top` 全放行 (SC-22 基线 0/57)。", "`docker top` 全放行 (SC-22 基线 0/@SC22_N@)。")
