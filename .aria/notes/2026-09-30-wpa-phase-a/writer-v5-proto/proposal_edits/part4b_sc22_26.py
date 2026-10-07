# part 4b: SC-22, SC-23, SC-25, SC-26.   `E(old, new)` = replace one exact substring (must occur exactly once).
EDITS = []


def E(old, new, count=1):
    EDITS.append(("sub", old, new, count))


def L(prefix, new):
    EDITS.append(("line", prefix, new, 1))


# ---------------------------------------------------------------- SC-22
E("**22av** 带 `-` 或 `-O` 的 14 个 ps 拼写 (`-aux -ax -x -ux -au -axu -auxww -w -x -eO -O -eu -u -ex -xw`) 加事故类 `ps -aux | grep curl`",
  "**22av** 带 `-` 或 `-O` 的 14 个 ps 拼写 (逐个写全: `ps -aux`、`ps -ax`、`ps -x`、`ps -ux`、`ps -au`、`ps -axu`、`ps -auxww`、`ps -w -x`、`ps -eO rss`、`ps -O rss`、`ps -eu`、`ps -u`、`ps -ex`、`ps -xw`) 加事故类 `ps -aux | grep curl`")
E("**22bp** pid 位置的 v4 新增形态 (", "**22bp** pid 位置新增的形态 (")
E("**22bj** 已接受的文本提及误拦 (heredoc 里以 `ps aux` 起行; 含包裹词的文本: 提交信息 / `echo` / 文档检索里先有 `watch`、`sshd`、`ssh`、`stopwatch` 再有进程表形态; 类别算 `baseline-failing`: 基线放行、目标拦; 行转红 = 有人收窄了锚点, 须同步更新 W11 的已知限制) → exit 2, **基线 0/57**;",
  "**22bj** 已接受的文本提及误拦 (14 个独立运行: heredoc 里以 `ps aux` 起行 (2 个); 含包裹词的文本 —— 提交信息 / `echo` / 文档检索里先有 `watch`、`sshd`、`ssh`、`stopwatch` 再有进程表形态 (4 个); "
  "包裹词 (`ssh`、`bash -c`、`sh -c`、`watch`) 之后出现 `env` 这个词的文本 —— `bash -c \"python3 -m venv env && …\"` 的 venv 目录名、`watch -n 5 \"du -sh env\"`、提交信息与 `echo` 里 `ssh` 之后的 `env` 词 (5 个); "
  "对含真实 pid 记号的 `/proc/<pid>/environ|cmdline` 路径文本做 grep / rg / sed 检索或编辑 (3 个); 类别算 `baseline-failing`: 基线放行、目标拦; 行转红 = 有人收窄了其中任一类的锚点, 须同步更新 W11 的已知限制与 Impact) → exit 2, **基线 0/57**;")
E("(`allow-guard` ×9)", "(`allow-guard` ×10)")
E("共 89 个独立运行** → exit 0, **基线 9/9**;",
  "共 89 个独立运行**、**22br 包裹下的转储配正当的行级核对仍放行** (22 个转储成员各接锚定的 `| grep '^PATH='` (读一个变量) 与 `| cut -d= -f1` (列变量名): 44 个独立运行, 与基线对 `docker|kubectl|podman|lxc exec … env` 的 credit 一致) → exit 0, **基线 10/10**;")
E("(`known-limit` ×4)", "(`known-limit` ×5)")
E("`/proc` 行不属 tight: `cat /proc/123/environ | grep '^PATH='` → exit 0)**, **基线 4/4**。怎么会红:",
  "`/proc` 行不属 tight: `cat /proc/123/environ | grep '^PATH='` → exit 0)**、**22bs 包裹下的转储接 `| grep -v x` 放行** (22 个成员 → exit 0: 「整份环境减一行」是基线 docker / kubectl 行的既有限制, 现由新增的包裹共享; "
  "行转红 = 有人把这一族做成 tight, 须同步更新 W11 与 Impact), **基线 5/5**。怎么会红:")
E("包裹的转储备选缺成员 (22bo; `docker` / `kubectl` / `podman` / `lxc` 四个因基线另有独立规则而删除不可观察, 是等价变异)",
  "包裹的转储备选缺成员 (22bo; `docker` / `kubectl` / `podman` / `lxc` 四个因基线另有独立规则而删除不可观察 —— 带过滤的转储 (22br / 22bs) 上同样不可观察, 两条规则对过滤给同一个 credit —— 是等价变异; 缺 `ssh` / `sh` / `bash -c` / `watch` 则同时使 22bj 的 env 词成员转红)")
E("包裹词被锚在命令位置 (22bj 的文本提及转红)。",
  "包裹词被锚在命令位置 (22bj 的文本提及转红)、**包裹下的转储被并入 tight 族** (22br 的 44 个运行与 22bs 的 22 个运行全部转红: 锚定的 `grep` / `cut` 与 `grep -v` 都不再算 credit)。")

# ---------------------------------------------------------------- SC-23
E("(`baseline-failing` ×2) 23a 10CG/Aria#221 评论里的原始多行",
  "(`baseline-failing` ×3) 23a 10CG/Aria#221 评论里的原始多行")
E("23b 五条单键读取 (四个字面子串 `.environ.get(` / `.environ[` / `.environb.get(` / `.environb[` 各一、一条命令里多处) → exit 0, **基线 2/2 exit 2**;",
  "23b 五条单键读取 (四个字面子串 `.environ.get(` / `.environ[` / `.environb.get(` / `.environb[` 各一、另有一条同时含两种不同子串) → exit 0; "
  "**23j 同一子串在一条命令里出现两次** (四个子串各一条命令, 每条里该子串出现两次: 每一处都归一, 不只是第一处; 主机 / 用户 / 口令各读一次是常见写法) → exit 0, **基线 3/3 exit 2**;")
E("怎么会红: 给 `\\.env` 加了右边界 (23c / 23d / 23h 转红, 变异实测)、归一化吃掉了整表导出、漏了 `.environb`。",
  "怎么会红: 给 `\\.env` 加了右边界 (23c / 23d / 23h 转红, 变异实测)、归一化吃掉了整表导出、漏了 `.environb`、**只替换每个子串的第一处出现** (23j 的 4 个命令全部转红, 变异实测: 第二处仍被 `\\.env` 命中而拦)。")

# ---------------------------------------------------------------- SC-25
E("(`reverse-guard` ×3) `cat .env` (分段模式)", "(`reverse-guard` ×4) `cat .env` (分段模式)")
E("后 sha256 前 16 位等于基线常量, **基线 3/3**;",
  "后 sha256 前 16 位等于基线常量; **25h** 同时含单键读取与真实 `.env` 读取的命令被拦, 且 `Command was:` 一行回显的是**原命令文本** (`.environ.get(` 仍在), 不是匹配用的归一化副本 "
  "(上面的归一化把该行换成占位, 钉不住这一点, 所以单列一行), **基线 4/4**;")
E("怎么会红: 改了 heredoc, 或为新拦截另写文案。",
  "怎么会红: 改了 heredoc, 或为新拦截另写文案; 把归一化后的副本回显进 `Command was:` (25h 转红, 变异实测: 在 hook 开头对整条命令做一次归一化的实现, 拦截结果不变而回显变了, 其余 SC-23 / SC-25 行全绿)。")

# ---------------------------------------------------------------- SC-26 26g (the marker list covers every disclosure of the Impact section)
E("26g `aria/CHANGELOG.md` 最上一节含 `rule6_note`、`.aria/secret-guard.paths`、`ps aux`、放行侧 (`os.environ`、`keys_unsorted`)、`fp=`、`partial`;",
  "26g `aria/CHANGELOG.md` 最上一节含 `rule6_note` 与 Impact「行为变更双向申报」每一条的标记词各一 (新输入 `.aria/secret-guard.paths`; 新拦截 `ps aux` / `/proc` / `app.ini`; 新告警 `file.content` / `kv-secret-assign`; "
  "新静默 `placeholder`; 新放行 `os.environ` / `keys_unsorted`; 日志字段 `fp=`; 性能 `CPU`) 与变量间接的 `partial`;")

E("`/proc` 读取器表合并时丢成员 (22bc / 22bd)、", "`/proc` 读取器表合并时丢成员 (22bc / 22bd; 缺 `grep` / `rg` / `sed` 另使 22bj 的 /proc 文本成员转红)、")
# SC-26: the CHANGELOG markers are pinned one by one
E("26g `aria/CHANGELOG.md` 最上一节含 `rule6_note` 与 Impact「行为变更双向申报」每一条的标记词各一",
  "26g (CHANGELOG 缺任一标记词, 13 个逐个删: 各转红) `aria/CHANGELOG.md` 最上一节含 `rule6_note` 与 Impact「行为变更双向申报」每一条的标记词各一")
