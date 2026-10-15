# edits_v6_c.py -- Success Criteria.   Executed by apply_edits_v6.py (shares sub1 / after / NUM / t).

# ---------------------------------------------------------------- SC introduction
sub1("(共 437 行, 其中 SC-30 一行不执行)", "(共 @ROWS@ 行, 其中 SC-30 一行不执行)")
sub1("验收模式 `WPA_REQUIRE_ALL=1` 下任何本应运行的行是 `n/a` 即 exit 3, 末尾形态行点名全部 `n/a` 行,",
     "验收模式 `WPA_REQUIRE_ALL=1` 下目标形态不成立 (有行是 `no`) 即 exit 4, 否则任何本应运行的行是 `n/a` 即 exit 3, 末尾形态行点名全部 `n/a` 行 (单个用例的 hook 调用超时只记该行为 `no`, 实得 `error: TimeoutExpired`, 其余行照跑),")
sub1("W11 的 launcher / `/proc` 读取器 / 远程包裹 / ps 备选 / pid 位置 / 关键字位置 / 非 ps 拼写", "W11 的 launcher / `/proc` 读取器 / 远程包裹 / ps 备选 / pid 位置 / 关键字位置 / 命令位置字符集 / 非 ps 拼写")
sub1("无界前缀与平方级取值 (34a / 34b / 34c) 各有对应的坏实现并证明转红。",
     "无界前缀与平方级取值 (34a / 34b / 34c)、失败事件只注册不读 `error` / 只读不注册 / 事件名写死 (35a–35d)、判定函数留在 source 闸门之下 (30b) 各有对应的坏实现并证明转红。")

# ---------------------------------------------------------------- SC-3
sub1("- **SC-3** (`known-limit` ×2, W1): Edit 真实信封、字符串形 `tool_response` → 静默。",
     "- **SC-3** (`known-limit` ×2, W1): Edit 真实信封、字符串形 `tool_response` (PostToolUse 上无此形状的平台样本; 失败的调用是 `PostToolUseFailure` 输入, 见 SC-35) → 静默。")

# ---------------------------------------------------------------- SC-9 (9z)
sub1("- **SC-9** (`allow-guard` ×26, W2):", "- **SC-9** (`allow-guard` ×25 + `known-limit` ×1, W2):")
sub1("**9z** kv-secret-assign 的左边界: 紧贴在小写字母之后的大写键、紧贴在小写前缀与下划线之后的键都不是键起点 (`xJWT_…=<值>`、`abc_API_…=<值>`)。**基线 26/26**。",
     "**9z** (`known-limit`) kv-secret-assign 的左边界: 紧贴在小写字母之后的大写键、紧贴在小写前缀与下划线之后的键 (含 `export` 与引号形) 都不是键起点, 凭据形值静默 "
     "(`xJWT_…=<值>`、`abc_API_…=<值>`、`export my_DB_PASSWORD = '<值>'`; 该行转红 = 有人放宽了左边界, 须同步 W2 的已知限制与待复议第 31 条)。**基线 26/26**。")
sub1("kv 没有左边界 (9z: 从词中间读出键)。", "kv 没有左边界 (从词中间读出键: 9z 转红) 或放宽了它 (9z 转红, 须同步已知限制)。")

# ---------------------------------------------------------------- SC-12 (12p)
sub1("- **SC-12** (W4): (`baseline-failing` ×12)", "- **SC-12** (W4): (`baseline-failing` ×13)")
sub1("12c 是两者都藏)。**基线 0/12 无 `fp` 字段**。",
     "12c 是两者都藏); **12p 只对被计数的 span 取指纹** (11 个被白名单排除的占位 span (`<16 位 alnum>`) 后接 1 个真凭据 json:token: 计数恰为 1, 日志 fp 恰为该真值的 sha256 前 8 位一项)。**基线 0/13 无 `fp` 字段**。")
sub1("(12o: 缺 `shasum` 腿与缺 `sha256sum` 腿各转红)、",
     "(12o: 缺 `shasum` 腿与缺 `sha256sum` 腿各转红)、先记指纹再分类 (被排除的占位 span 用掉 10 个指纹名额, 真凭据的指纹被挤掉: 12p 转红)、")

# ---------------------------------------------------------------- SC-17 (17d)
sub1("**17d** (`known-limit`, 21 个独立运行) 读取器表之外的 Bash 读取写法放行 —— 重定向读 6 形、`source` / `.`、`dd` / `cp … /dev/stdout` / `docker cp`、`perl -ne`、`xargs cat` / `find -exec`、目录递归 / 文件名 glob 3 形、`git show`、`bat`、大写目录名、反斜杠路径 → exit 0,",
     "**17d** (`known-limit`, @N17D@ 个独立运行) 读取器表之外的 Bash 读取写法放行 —— 重定向读 6 形、`source` / `.`、`dd` / `cp … /dev/stdout` / `docker cp`、`perl -ne`、`xargs cat` / `find -exec`、目录递归 / 文件名 glob 3 形、`git show`、"
     "表外读取器 6 个 (`bat`、`expand`、`unexpand`、`shuf`、`split`、`csplit`; 基线 `.env` 族会拦这些读取器, `app.ini` 族不拦)、大写目录名、反斜杠路径 → exit 0,")

# ---------------------------------------------------------------- SC-19 (19an / 19ao / 19ap)
sub1("内建里另有两行以 `forgejo` 一词为锚", "内建里另有四行以 `forgejo` 一词为锚 (`secret-guard.sh:778` 与 `:1006-1008`)")
sub1("的临时项目): (`baseline-failing` ×26)", "的临时项目): (`baseline-failing` ×29)")
sub1("ASCII 字母折叠 → 2), **基线 0/26**;",
     "ASCII 字母折叠 → 2); **19an 清单末行没有换行** (proj(nonl_one): 只有一条目且其后无换行; proj(nonl_two): 两条目, 第二条无换行: `cat P` → 2、`cat <第一条目>` → 2); "
     "**19ao 项目根可以是任意字符串** (根目录名含空格、括号与非 ASCII 字符, 清单列 P: `cat P` → 2、Read P → 2); **19ap `CLAUDE_PROJECT_DIR` 置空 (设了但为空串) 且 stdin `cwd` 指向含清单的目录** → `cat P` → 2, **基线 0/29**;")
sub1("、对每个出现点各判一遍内建判定的实现 (34c 转红)。",
     "、对每个出现点各判一遍内建判定的实现 (34c 转红)、**清单读取丢掉无换行的末行** (`while read` 一类: 19an 转红)、**清单或项目根路径的展开不加引号** (19ao 转红: 整个扩展静默失效)、**只在 `CLAUDE_PROJECT_DIR` 未设时才回落 `cwd`** (`${V-}` 一类: 19ap 转红)。")

# ---------------------------------------------------------------- SC-22
sub1("- **SC-22** (W11): (`baseline-failing` ×57)", "- **SC-22** (W11): (`baseline-failing` ×@SC22_N@)")
sub1("**22bo** 11 个包裹 × {`env`, `printenv`} 共 22 个成员 (含 `sh -c` / `bash -c` / `watch`; ssh 取不加引号的写法);",
     "**22bo** 11 个包裹 × {`env`, `printenv`} 共 22 个成员 (含 `sh -c` / `bash -c` / `watch`; ssh 取不加引号的写法; 有基线行的五个包裹取基线行不拦的写法 —— docker / docker compose / podman / kubectl 取加引号的转储 (`docker exec c \"env\"`、`kubectl exec pod 'printenv'`), lxc 取不带 `--` 的写法 —— 所以 22 个成员在基线上全是放行);")
sub1("类别算 `baseline-failing`: 基线放行、目标拦; 行转红 = 有人收窄了其中任一类的锚点, 须同步更新 W11 的已知限制与 Impact) → exit 2, **基线 0/57**;",
     "类别算 `baseline-failing`: 基线放行、目标拦; 行转红 = 有人收窄了其中任一类的锚点, 须同步更新 W11 的已知限制与 Impact); "
     "**22bt 命令位置字符集逐成员** (`true; ps aux`、`true; ps aux &` (逐段判定下段切分已吸收单独的 `;`, 只有整串判定 —— 后台 `&`、块、循环 —— 才靠字符集里的 `;`)、`true & ps aux`、`true | ps aux`、`(ps aux)`、`x=$(true) ps aux`、`{ ps aux; }`、`` echo `ps aux` ``、换行后的 `ps aux`: 9 个独立运行; 行首、`then` / `do` / `else` / `elif` 与 launcher 另见 22az / 22aw); "
     "**22bu 簇内字母与操作数位置** (18 个独立运行: `pgrep -fa` / `-la` / `-ifa`、`pgrep -u root -a`、`pgrep -x -af`、`pstree -pa` / `-ua`、`pstree -p -a`、`ps -eF`、`ps -F -p 123`、`ps -p 123 -f`、`ps -p 1 -F`、`docker ps -a --no-trunc`、`docker container ls -a --no-trunc`、launcher 时长后缀 `5m` / `2h` / `1d` / `30s`); "
     "**22bv `-o` / `--format` 列表任一位置含 `args|cmd|command`** (7 个独立运行: 首位、中间、后接更多列、与另一关键字同现、在 pid 操作数之后); "
     "**22bx 包裹下带变量名的 `printenv <NAME>`** (11 个包裹各一, 取基线包裹行不拦的写法: `docker exec c printenv HOME`、`podman exec c 'printenv HOME'`、`kubectl exec pod 'printenv HOSTNAME'`、`lxc exec c printenv HOME`、`ssh host printenv PATH`、`nomad alloc exec abc printenv HOME`、`pct exec 101 -- printenv HOME`、`sh -c 'printenv HOME'`、`bash -c \"printenv LANG\"`、`watch printenv X` 等); "
     "**22by** kubectl 包裹下写成命令替换或带输出重定向的转储 (`x=$(kubectl exec pod env)`、`kubectl exec pod env > /tmp/x`: 2 个独立运行) → exit 2, **基线 0/@SC22_N@**;")
sub1("(`reverse-guard` ×2) **22J** 既有 `/proc/N/{cmdline,environ}` 的 5 条; **22bc** 被改写的 `/proc` 行保留基线 13 个读取器 × {environ, cmdline} 与两个 `<` 重定向, 共 28 个独立运行 → exit 2, **基线 2/2**;",
     "(`reverse-guard` ×3) **22J** 既有 `/proc/N/{cmdline,environ}` 的 5 条; **22bc** 被改写的 `/proc` 行保留基线 13 个读取器 × {environ, cmdline} 与两个 `<` 重定向, 共 28 个独立运行; "
     "**22bw** 基线自己对五个包裹的写法仍拦 (docker / docker compose / podman exec <c> env|printenv、kubectl exec <pod> -- env|printenv、lxc exec <c> -- env|printenv: 10 个独立运行; `secret-guard.sh:858` / `:862-863` / `:938` / `:940`) → exit 2, **基线 3/3**;")
sub1("包裹的转储备选缺成员 (22bo; `docker` / `kubectl` / `podman` / `lxc` 四个因基线另有独立规则而删除不可观察 —— 带过滤的转储 (22br / 22bs) 上同样不可观察, 两条规则对过滤给同一个 credit —— 是等价变异; 缺 `ssh` / `sh` / `bash -c` / `watch` 则同时使 22bj 的 env 词成员转红)、",
     "包裹的转储备选缺成员 (22bo: 有基线行的五个包裹的引号形 / 不带 `--` 形基线不拦, 删掉任一包裹即转红, 22by 另钉 `$(…)` 与重定向形; 缺 `ssh` / `sh` / `bash -c` / `watch` 则同时使 22bj 的 env 词成员转红)、`printenv` 只拦裸 (22bx 转红)、"
     "命令位置字符集缺成员 (22bt 逐成员)、簇内字母只认首位 / 操作数只认首个 / 列表关键字只认末位 / 时长后缀只认 `s` (22bu / 22bv)、")

# ---------------------------------------------------------------- SC-25 (25i)
sub1("(`baseline-failing` ×4) `ps aux`、`cat /etc/forgejo/app.ini`、扩展条目、Read `/etc/forgejo/app.ini` 被拦时的文本同样等于基线常量, **基线 4/4 未拦 (无文本)**。",
     "(`baseline-failing` ×5) `ps aux`、`cat /etc/forgejo/app.ini`、扩展条目、Read `/etc/forgejo/app.ini` 被拦时的文本同样等于基线常量, **基线 4/4 未拦 (无文本)**; "
     "**25i** 扩展拦截的 `Matched pattern:` 点名 `.aria/secret-guard.paths`, `Command was:` 与 `Triggering segment:` 回显**原命令文本**, 替身名 `/etc/gitea/app.ini` 不出现 (25f 的归一化把这几行抹掉, 所以单列), **基线未拦 (无文本)**。")
sub1("其余 SC-23 / SC-25 行全绿)。\n",
     "其余 SC-23 / SC-25 行全绿); 让内建判定对替换副本的文案直接透传 (用户看到的是一条他从未用过的路径: 25i 转红)。\n")

# ---------------------------------------------------------------- SC-26 / SC-28
sub1("26c §5.6 内含 `.aria/secret-guard.paths`、`CLAUDE_PROJECT_DIR`、字面子串、大小写不敏感、只增不减、32 KiB、200、整体忽略、**静默**;",
     "26c §5.6 内含 `.aria/secret-guard.paths`、`CLAUDE_PROJECT_DIR`、字面子串、大小写不敏感、只增不减、32 KiB、200、整体忽略、**静默**, 以及保护边界与建议 (关键词 `读取器`、`Grep`、`前 64 处`、`最短`);")
sub1("26e aria `README.md` 与 `README.zh.md` 的 Hooks 用法小节各含 `.aria/secret-guard.paths` 与字面子串语法 (`literal substring` / `字面子串`);",
     "26e aria `README.md` 与 `README.zh.md` 的 Hooks 用法小节各含 `.aria/secret-guard.paths` 与字面子串语法 (`literal substring` / `字面子串`)、最短特征子串的建议 (`SHORTEST` / `最短`)、保护边界 (`Grep`) 与失败事件 (`PostToolUseFailure`);")
sub1("26g (CHANGELOG 缺任一标记词, 13 个逐个删: 各转红)", "26g (CHANGELOG 缺任一标记词, 14 个逐个删: 各转红)")
sub1("新告警 `file.content` / `kv-secret-assign`;", "新告警 `file.content` / `PostToolUseFailure` / `kv-secret-assign`;")
sub1("**26k** §5.1 内含 `app.ini` (测试清单括号列新族);", "**26k** §5.1 内含 `app.ini` (测试清单括号列新族) 且 secret-scan 行名 `PostToolUseFailure`;")
sub1("28f 另要求没有顶层 `\"content\":` 契约行;", "28f 另要求没有顶层 `\"content\":` 契约行、契约描述 `PostToolUseFailure` 输入 (有以 `\"error\":` 起头的契约行);")

# ---------------------------------------------------------------- SC-30 / SC-31
sub1("- **SC-30** (`zero-regression`, 探针外):", "- **SC-30** (`zero-regression`, 探针外; 30b 是探针内的 `reverse-guard` 行):")
sub1("判据对主机负载稳健, 见 W14**。", "判据对主机负载稳健, 见 W14**; **30b** (`reverse-guard`, 探针内) 复刻测试内 SC-8 的抽取装配 (`source` hook 闸门之上的部分, 再按锚点抽 `risky_patterns` / `_sg_judge_one` / `_sg_per_segment_eval`): 五档负载的命令各返回 0、两条必拦命令 (`cat /opt/.env`、漏补重定向的迁移写法) 各返回 2, **基线 7/7**, 不需要 git 历史也不计时。")
sub1("或扩展 / 替换判定把内建判定推迟 (h)、", "或 `_sg_core_eval` 一类被 `_sg_per_segment_eval` 调用的辅助函数留在 source 闸门之下 (测试内 SC-8 的抽取装配只计到 rc=127 的瞬时返回, 五档恒绿: 30b 转红)、或扩展 / 替换判定把内建判定推迟 (h)、")
sub1("`hooks/hooks.json` 与基线字节一致; `hooks/hooks.json` 不含字面 `completeness_gate`。**基线 5/5 (145; 61 = 61; 0 行; 一致; 不含)**。怎么会红: 规则膨胀超预算、新族没同步硬编码、用变量整行躲过 census、动了注册面。",
     "`hooks/hooks.json` 的注册 (`hooks` 对象) 去掉 `PostToolUseFailure` 键后与基线相等 (顶层 `description` 字符串不在比较内, 可随之更新); `hooks/hooks.json` 不含字面 `completeness_gate`。**基线 5/5 (145; 61 = 61; 0 行; 相等; 不含)**。怎么会红: 规则膨胀超预算、新族没同步硬编码、用变量整行躲过 census、"
     "动了注册面 (除那一条 `PostToolUseFailure` 注册之外的任何改动: 31d; 那一条本身见 35d)。")

# ---------------------------------------------------------------- SC-34
sub1("**34a** (`reverse-guard`) 基线 tag 的长单行形态 —— 8 KB 的 bearer / X-API-Key 头值、env 行 (长值与长键)、postgres URL (长口令与长用户名)、JSON 口令字段: 7 个独立运行, 每个仍给出基线的检出 (取值与指纹代码对既有 tag 的每个 span 也执行, 平方级的取值会让基线本来检出的凭据在同一输出里失检)。",
     "**34a** (`reverse-guard`) 基线 tag 的长单行形态 —— 8 KB 的 bearer / X-API-Key 头值、env 行长值与 JSON 口令值; 500 KB 的 env 行长键、postgres URL 长口令与长用户名、basic-auth URL 长口令、JSON 口令键与冒号之间的空白串: 9 个独立运行, 每个仍给出基线的检出 "
     "(取值与指纹代码对既有 tag 的每个 span 也执行: 分隔符藏在长串之后、靠逐个试位置去找的写法是平方级, 会让基线本来检出的凭据在同一输出里失检)。")
sub1("**34b** (`baseline-failing`) 新 tag 上让自然写法的 pattern 或取值变成平方级的形态 —— 300 KB 的 `-` 串与 20 KB 的 `a-` 串接在旗标前、8 KB 的旗标值、300 KB 的大写连续段接在键前、export / 头 / JSON 形里 8 KB 的空白串、8 KB 的头值: 9 个独立运行, 每个仍计一次该 tag。",
     "**34b** (`baseline-failing`) 新 tag 上让自然写法的 pattern 或取值变成平方级的形态 —— 300 KB 的 `-` 串与 20 KB 的 `a-` 串接在旗标前、8 KB 的旗标值、300 KB 的大写连续段接在键前、`export` 之后 100 KB 的空白串、键与 `=` 之间 500 KB 的空白串、JSON 键与冒号之间 500 KB 的空白串、"
     "**500 KB 不带引号的 kv 值三形** (`KEY = v`、`export KEY=v`、YAML `  KEY: v`)、头 / JSON 值里 8 KB 的空白串、8 KB 的头值: 14 个独立运行, 每个仍计一次该 tag (取 500 KB: 平方级的取值写法在那里要烧 8 s 以上的单进程 CPU, 离每进程 4 s 的上限有 2 倍以上余量, 线性写法的最长单进程不到 @CAP_LIN_MAX@ s)。")
sub1("值抽取 / 去空白用前导 `*` 的 `#` / `##` 删除 (34a 与 34b 的长值形态转红)、",
     "取值代码里分隔符可能很远或不命中的 `#` / `##` / `%` / `%%` 删除 (引号剥离 `${V#[\"']}`: 34b 的三个长不带引号 kv 值成员; 空白串之后的 `=` / `:` 搜索: 34b 的空白串成员; 长键 / 长口令之后的 `=` / `@` / `:` 搜索: 34a 的 env 行长键、postgres 与 basic-auth 成员) 与前导 `*` 的 `#` / `##` 删除 (34a 与 34b 的长值形态转红)、")

# ---------------------------------------------------------------- SC-35 (new)
after("时档比值 (W14 的 (i3) / (f-hit)) 在探针之外 (SC-30)。\n",
      "- **SC-35** (`baseline-failing` ×3 + `reverse-guard` ×1 + `allow-guard` ×1, W1 失败事件): 失败的工具调用 (Bash 非零退出等) 以 `PostToolUseFailure` 输入到达 secret-scan: 没有 `tool_response`, 文本 (`Exit code N` 加 stderr 与 stdout) 在顶层 `error`; "
      "探针里的失败信封 = `{session_id, hook_event_name: PostToolUseFailure, tool_name: Bash, tool_input, tool_use_id, error, is_interrupt, duration_ms}`, 成功信封另带 `hook_event_name: PostToolUse`。"
      "**35a** `error` = `Exit code 22` 换行加一行凭据 (AWS 密钥 id 行 / `JWT_SECRET = <43 b64url>` / curl -v 回显的 `> Authorization: token <40 hex>`): 3 个独立运行, 各给出该行的 tag (`aws-access-key-id=1` / `kv-secret-assign=1` / `auth-header-token=1`); "
      "**35b** 同三例的输出里 `hookSpecificOutput.hookEventName` 恰为 `PostToolUseFailure` (harness 按触发的事件校验它, 不符即丢告警); "
      "**35c** (`reverse-guard`) 成功调用的输出事件名仍是 `PostToolUse`: Bash / Write 真实信封 (带 `hook_event_name`)、不带该字段的旧信封、文本里只是**提到** `\"hook_event_name\":\"PostToolUseFailure\"` 的成功信封 (4 个独立运行); "
      "**35d** `hooks/hooks.json` 的 `PostToolUseFailure` 恰有一条注册: secret-scan, matcher、命令与超时同其 `PostToolUse` 条目, 没有别的 hook; "
      "**35e** (`allow-guard`) 不含凭据的失败文本静默: 普通 `Exit code 1` 错误、usage 提示, 以及两个文档式占位符 (`FAKE_` 开头的赋值值、`PLACEHOLDER_` 开头的头 token: 分类器与白名单在其它输出上让它们静默, 失败路径同样如此) (4 个独立运行)。**基线: 35a / 35b / 35d 不符 (基线没有注册该事件, 提取链也不读 `error`), 35c / 35e 相符**。"
      "怎么会红: 只注册、不读 `error` (35a / 35b 转红); 只读 `error`、不注册 (35d 转红: 失败的调用根本不会调用 hook); 输出事件名写死 `PostToolUse` (35b) 或写死 `PostToolUseFailure` (35c); 只凭输出文本里的子串判事件、不用 jq 确认 (35c 的「提到」成员转红); "
      "注册了第二个 hook 或错的 matcher (35d); 动了别的注册项 (SC-31 31d); 失败路径漏掉分类器与白名单 (失败文本里的文档式占位符被计数并告警: 35e 转红)。\n")
