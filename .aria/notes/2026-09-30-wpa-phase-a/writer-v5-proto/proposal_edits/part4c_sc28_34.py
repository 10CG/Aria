# part 4c: SC preface (判定命令), SC-28, SC-30, SC-32, SC-34.   ("sub" = exact substring, "line" = whole line, "after" = new line inserted after the line that starts with `prefix`)
EDITS = []


def E(old, new, count=1):
    EDITS.append(("sub", old, new, count))


def L(prefix, new):
    EDITS.append(("line", prefix, new, 1))


def A(prefix, new):
    EDITS.append(("after", prefix, new, 1))


# ---------------------------------------------------------------- preface: 判定命令
E("调试用 `WPA_ONLY=SC-4,…` 选 SC、`WPA_ROWS=4p,…` 选行)。L3 行:",
  "调试用 `WPA_ONLY=SC-4,…` 选 SC、`WPA_ROWS=4p,…` 选行; SC-32 32e 用默认 bash 在 `LC_ALL=C` 下运行, 不需要任何环境变量)。"
  "耗时类的行 (SC-34) 用每进程 CPU 时间上限 (`ulimit -t 4`, 计 CPU 时间而非墙钟, 不随主机负载移动) 判「是否线性」, 34c 另以整进程 CPU 总量之比 (shell 内建 `times`, 上界 3.5 倍) 判扩展命中路径的代价; "
  "时档比值 (W14) 在探针之外 (SC-30)。L3 行:")

# ---------------------------------------------------------------- SC-28
E("(`doc-sync` ×14, W14): W14 所列陈旧 / 悬空表述各一行 (28a–28i、28l),",
  "(`doc-sync` ×15, W14): W14 所列陈旧 / 悬空表述各一行 (28a–28i、28l、28o),")
E("**28m** 三处「无法 redact」陈述 (SOT §5.2 与 aria README 两语种) 各追加一句 `updatedToolOutput` 事实、",
  "**28m** 三处「无法 redact」陈述 (SOT §5.2 与 aria README 两语种; README 里是每个文件的**第二个** Hooks 小节, 见 W9 的文档落点) 各追加一句 `updatedToolOutput` 事实、")
E("**28n** `secret-scan.sh` 头注释 Scope 清单点名 6 个新 tag。替换文本的英文字面见 W14。**基线 0/14**。",
  "**28n** `secret-scan.sh` 头注释 Scope 清单点名 6 个新 tag、**28o** `secret-guard.sh` 头注释里「~100 most common patterns」一句 (基线 145 行规则、目标 149 行; 句子跨两行注释, 判据先把注释行拼成一句): "
  "`~100` 消失、`most common patterns` 仍在、拼合后的句子不含任何数量字面。替换文本的英文字面见 W14。**基线 0/15**。")
E("把计数句换成新的字面数字 (`37 patterns` 之类: 28c / 28d)、",
  "把计数句换成新的字面数字 (`37 patterns` 之类: 28c / 28d; 把 `~100` 换成 `~150` 之类: 28o)、")

# ---------------------------------------------------------------- SC-30 (the new time tiers)
E("**另含 W14 的五个新时档 (f) / (f0) / (g) / (h) / (i), 判据对主机负载稳健, 见 W14**。",
  "**另含 W14 的新时档 (f) / (f0) / (f-hit) / (g) / (h) / (i) / (i3), 判据对主机负载稳健, 见 W14**。")
E("对稠密输入逐 span 无上界迭代 (i)、W10 余量用二次写法 (g)、扩展按条目起进程 (f)。",
  "对稠密输入逐 span 无上界迭代 (i)、长单行上 pattern 或取值带无界前缀 (i3)、W10 余量用二次写法 (g)、扩展按条目起进程 (f)、扩展命中路径上对每个出现点重判或重算阶段 (f-hit)。")

# ---------------------------------------------------------------- SC-32
E("- **SC-32** (`reverse-guard` ×4, bash 3.2):", "- **SC-32** (`reverse-guard` ×5, bash 3.2 与 POSIX locale):")
E("构造不了则该行 `n/a` 并在汇总行上报)。**基线 4/4** (32c / 32d 在基线上各 361 行一致)。",
  "构造不了则该行 `n/a` 并在汇总行上报); **32e** (**POSIX locale 腿**) 同一个比对在 `LC_ALL=C` 下再做一遍 (字节语义、没有多字节字符: 没有 `LANG` 的容器镜像里 hook 实际所处的 locale, 如 Layer 2 的 aria-runner 镜像), "
  "只用默认 bash (不需要构造第二个 locale): 全部 hook-direct 行的结果字符串须与第一个 locale 的逐行相同。32d 的第二个 locale 默认也是 UTF-8 系, 看不出「按字符与按字节混用」这一类差别, 32e 补这一格。"
  "**基线 5/5** (32c / 32d / 32e 在基线上各 @HOOKROWS@ 行一致)。")
E("变异实测: 往 hook 里加一个 `[[ -v … ]]` 函数, 32a 与 32c 同时转红;",
  "变异实测: 往 hook 里加一个 `[[ -v … ]]` 函数, 32a 与 32c 同时转红; 按**最后一个字符**判 `…` 后缀的实现 (UTF-8 locale 下是一个字符、POSIX locale 下是一个字节; 默认 32d 的第二个 locale 同属 UTF-8, 看不出), 32e 转红并点名 11v / 11x / 11y;")

# ---------------------------------------------------------------- SC-34 (new)
A("- **SC-33** (`allow-guard` ×1, W2 / W3):",
  "- **SC-34** (`reverse-guard` ×1 + `baseline-failing` ×2, W2 / W9 / W14): 新增的 pattern、取值与匹配代码对输入长度**线性** (为什么线性见 W2 的「线性」段与 W9 的匹配实现)。判据是每进程 CPU 时间上限, 不是墙钟: `ulimit -t 4` 计 CPU 时间, "
  "不随主机负载移动; 超限的 hook 被杀、读不到结果, 与 5 s 的 hook 超时对它的处置相同。**34a** (`reverse-guard`) 基线 tag 的长单行形态 —— 8 KB 的 bearer / X-API-Key 头值、env 行 (长值与长键)、postgres URL (长口令与长用户名)、JSON 口令字段: "
  "7 个独立运行, 每个仍给出基线的检出 (取值与指纹代码对既有 tag 的每个 span 也执行, 平方级的取值会让基线本来检出的凭据在同一输出里失检)。**34b** (`baseline-failing`) 新 tag 上让自然写法的 pattern 或取值变成平方级的形态 —— "
  "300 KB 的 `-` 串与 20 KB 的 `a-` 串接在旗标前、8 KB 的旗标值、300 KB 的大写连续段接在键前、export / 头 / JSON 形里 8 KB 的空白串、8 KB 的头值: 9 个独立运行, 每个仍计一次该 tag。"
  "**34c** (`baseline-failing`) 扩展命中路径的代价 —— 4 KB 单行里列入的路径出现 64 次 (最后一处在 `cat` 之后) 与出现 1 次: 都读到 (exit 2), 且命中时整进程 CPU 总量 (shell 内建 `times`, 交错取 3 次的最小值) "
  "不超过同一命令在无扩展文件时的 3.5 倍 (设计值约 2 倍: 多一遍内建判定; 对每个出现点各判一遍或各算一次阶段的实现是数十倍)。**基线: 34a 为 `yes`; 34b / 34c 因新 tag 与扩展尚不存在为 `no`**。"
  "怎么会红: `cli-secret-flag` 的参数名前缀无界或没有左边界、`kv-secret-assign` 没有左边界或键名后缀无界 (34b 的对应形态转红, 同时 10n / 10o 与 9z 钉住边界的语义)、值抽取 / 去空白用前导 `*` 的 `#` / `##` 删除 "
  "(34a 与 34b 的长值形态转红)、扩展对每个出现点各判一遍内建判定或各算一次阶段 (34c 转红)。时档比值 (W14 的 (i3) / (f-hit)) 在探针之外 (SC-30)。")
