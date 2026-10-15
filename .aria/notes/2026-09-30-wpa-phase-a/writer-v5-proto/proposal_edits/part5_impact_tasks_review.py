# part 5: Level 对账, Why table, Impact, Tasks, 待 owner 复议.   ("sub" = exact substring, "line" = whole line, "after" = new line after the line that starts with `prefix`)
EDITS = []


def E(old, new, count=1):
    EDITS.append(("sub", old, new, count))


def L(prefix, new):
    EDITS.append(("line", prefix, new, 1))


def A(prefix, new):
    EDITS.append(("after", prefix, new, 1))


# ---------------------------------------------------------------- header: Level 对账 counts
E("(14 个工作项 / 33 组 SC / 411 行探针)", "(14 个工作项 / 34 组 SC / @ROWS@ 行探针)")

# ---------------------------------------------------------------- Why table
E("同一内容经 Bash / Write 真实信封与四种旧信封 (含 `tool_result` 两种) 6/6 检出 | SC-1 / SC-2 |",
  "同一内容经 Bash / Write 真实信封与四种旧信封 (含 `tool_result` 两种) 6/6 检出; ASCII 字符之间夹 NUL 的文本 (UTF-16LE 经 Bash 输出) 基线已检出, 不得回退 | SC-1 / SC-2 |")

# ---------------------------------------------------------------- Impact
E("`CHANGELOG.md` (新节带 rule6_note 行与上面「行为变更双向申报」六条的逐条披露, 含放行侧与日志侧, SC-26 26g)",
  "`CHANGELOG.md` (新节带 rule6_note 行与上面「行为变更双向申报」六条 (新拦截 / 新告警 / 新放行 / 新静默 / 日志 / 性能) 加新输入的逐条披露, 每条至少一个标记词, 含放行侧与日志侧, SC-26 26g)")
E("`nomad alloc exec` / `pct exec` / `ssh` / `sh -c` / `bash -c` / `watch` 包裹下的裸 `env` / `printenv`; **含 `ssh` / `watch` 这类包裹词 (含 `sshd` / `stopwatch` 子串) 的文本提及 (提交信息、`echo`、文档检索) 在其后出现进程表形态时被拦** (W11 已知误拦, SC-22 22bj)。",
  "`nomad alloc exec` / `pct exec` / `ssh` / `sh -c` / `bash -c` / `watch` 包裹下的裸 `env` / `printenv` (转储之后接锚定的 `grep` / `cut` 等行级过滤沿用基线 `docker|kubectl|podman|lxc exec … env` 的 credit, 仍放行: SC-22 22br / 22bs; 以往放行的日常核对形态不变); "
  "**文本提及的误拦** (W11 已知误拦, SC-22 22bj): 含 `ssh` / `watch` 这类包裹词 (含 `sshd` / `stopwatch` 子串) 的文本 (提交信息、`echo`、文档检索) 在其后出现进程表形态时被拦; 包裹词 (含 `bash -c` / `sh -c`) 之后出现 `env` / `printenv` 这个词的文本被拦 "
  "(如 `bash -c \"python3 -m venv env && …\"`、提交信息里 `ssh` 之后的 `env` 词); 对含真实 pid 记号的 `/proc/<pid>/environ|cmdline` 路径文本做 grep / rg / sed 检索或编辑被拦。"
  "**新拦截在 Layer 2 (aria-runner 容器, 无人值守) 里同样生效**: BLOCKED 文案里的 `# guard:ack: <理由>` 一次性逃生口在那里由执行方 AI 自己写、没有人复议, 本 Spec 不改这一既有机制。")
E("NUL 分隔的内容 (`/proc/<pid>/environ`、`env -0` 的输出) 首次可被检出 (W1);",
  "NUL 分隔的内容 (`/proc/<pid>/environ`、`env -0` 的输出) 首次可被检出 (W1: 含 NUL 的输入在两个视图上各扫一遍, 同一凭据的计数可能多一份, 只会多不会少);")
L("  - **性能**:", "@IMP_PERF@")
E("仓内约定 (`COMMIT_FOOTER_GUIDE.md`、`git-commit.md` §6.1) 要求修复类提交写 `Closes #N`, 而推送 / 合并到默认分支会自动关闭被引用的 issue",
  "仓内约定 `aria/skills/commit-msg-generator/COMMIT_FOOTER_GUIDE.md:199-200` 要求修复 Bug / 完成功能类提交写 `Closes #N` (`:201-202`: 部分实现与只是引用写 `Refs`; `standards/conventions/git-commit.md` §6.1 只并列 `Closes` / `Fixes` / `Refs` 三种写法, 不作要求), "
  "而推送 / 合并到默认分支会自动关闭被引用的 issue")
E("该约定覆盖仓内 §6.1 的默认写法。",
  "该约定覆盖 `COMMIT_FOOTER_GUIDE.md` 对修复类提交的默认写法 (部分覆盖类的提交本就写 `Refs`)。")
E("三态 (干净 / 违规 / 跑坏: 错起点、空起点、非仓路径、空文本) 在临时仓里的实跑与 v3 写法的真空通过对照见 `writer-v4-proto/refs_check.py`。",
  "三态 (干净 / 违规 / 跑坏: 错起点、空起点、非仓路径、空文本) 在临时仓里的实跑, 以及只看 grep 退出码的写法会真空通过的对照, 见 `writer-v5-proto/refs_check.py`。")

# ---------------------------------------------------------------- Tasks
E("默认 `en_US.UTF-8`: `locale -a` 列出即可;", "默认 `en_US.UTF-8`: `locale -a` 列出即可; 32e 用 `LC_ALL=C`, 无需准备;")
E("- [ ] 1.7 W10 变量展开 (`_sg_vx_pass`, 前后缀拼接替换) + W9 扩展入口 (`_sg_ext_pass` / `_sg_ext_path_pass`, 全部扩展代码只经 `$( )` 调用)",
  "- [ ] 1.7 W10 变量展开 (`_sg_vx_pass`, 前后缀拼接替换) + W9 扩展入口 (`_sg_ext_subst` 把条目的出现换成内建 `app.ini` 名, `_sg_ext_pass` / `_sg_ext_path_pass` 经内建的同一个 `_sg_core_eval` 判定; 不另写阶段切分; 全部扩展代码只经 `$( )` 调用)")
L("- [ ] 1.8 W14 元耦合同步",
  "- [ ] 1.8 W14 元耦合同步 (测试内 SC-13 / SC-19 / SC-20 注入自测 / census) + 对抗 review: 坏实现由非作者构造, 至少覆盖「白名单写成单字符前缀 / 含 / 大小写不敏感」「熵下限写成必须含数字」「路径形写宽」「tight 漏并入」「扩展条目拼成正则」「扩展代码裸调用」"
  "「扩展先于内建」「第二遍按段交错」「W12 给 `\\.env` 加右边界」「`/proc` 连 status 一起放宽」「jq 新词进宽松词表」「bash 4+ 构造」十二种, **另含下列十四类**: "
  "「执行了命令文本、条目或被扫描内容的 eval 式实现」(21z / 19ab / 23i / 7n)、「扩展另写阶段切分 (含完全不切) 而不复用内建判定」(19af / 19aa)、「偏移与切片单位不一致」(19ag)、「字节语义依赖调用方导出 `LC_ALL`」(19ah / 19am)、"
  "「有效条目为零时把空模式交给 grep」(20o–20q)、「字符类用 glob 范围而与 locale 相关」(32d)、「按字符判后缀而与 locale 相关」(32e)、「分类器步骤套到不该套的既有 tag」(7l / 7m)、「tight 拷贝与规则行漂移」(22bm)、"
  "「包裹下的转储并入 tight」(22br / 22bs)、「对输入做的变换使既有检出变静默或使计数翻倍」(NUL 视图替换基线视图: 1e / 1f; 无条件追加视图: 1g / 2a–2d)、「无界前缀与平方级取值」(34a / 34b)、「对每个出现点各判一遍」(34c)、"
  "「内容形态」(NUL 分隔 / CR / UTF-16LE / 超长单行的信封内容: 1c / 1d / 1e / 1f、SC-29 的 `crlf-shim` / `jq-crlf-guard` 两个套件、(i) 与 (i3) 档); "
  "另须对每个枚举集合做「删掉任一成员」的缺项类坏实现、对每个上界做「差一」的边界坏实现 (起草期对这些逐一做过变异实测, 转红的行已在各 SC 的「怎么会红」里点名, 构造脚本与汇总见 `writer-v5-proto/`; 复核其复现)")
E("(带 `WPA_BASH32` 且 `WPA_REQUIRE_ALL=1`: 32c / 32d / 29h / 29i、12o 与 20g 不得是 `n/a`;",
  "(带 `WPA_BASH32` 且 `WPA_REQUIRE_ALL=1`: 32c / 32d / 32e / 29h / 29i、12o 与 20g 不得是 `n/a`;")
E("SC-30 全绿 (含 W14 的时档 (f) / (f0) / (g) / (h) / (i), 判据见 W14)",
  "SC-30 全绿 (含 W14 的时档 (f) / (f0) / (f-hit) / (g) / (h) / (i) / (i3), 判据见 W14)")

# ---------------------------------------------------------------- 待 owner 复议: 7.x
E("W1 的 NUL → 换行之后 L3 能事后检出其中的凭据形键, SC-1 1c, L1 的预防仍缺)", "W1 的 N 视图里 L3 能事后检出其中的凭据形键, SC-1 1c, L1 的预防仍缺)")
E("`env -0` 输出里的凭据形键由 L3 在 NUL → 换行后事后检出, SC-1 1d)", "`env -0` 输出里的凭据形键由 L3 在 N 视图里事后检出, SC-1 1d)")
E("   1. secret-guard 超时即放行: `hooks.json` timeout 5s, 约 1400 个空段使 hook 超时后命令被放行并执行 (`guard §0` 第 7 条、`§6.2` 第 1 条, 活体证实); 同源的延迟悬崖。",
  "   1. secret-guard 超时即放行: `hooks.json` 的 hook 超时 (5 s) 之后命令被放行 —— 既有设计缺口, 与延迟悬崖同源 (证据位置 `guard §0` 第 7 条、`§6.2` 第 1 条; 复现细节只留在研究笔记, 不在本 Spec 复述)。")
E("   2. 参数里引号内的 `|` 让所有「读取器 + `[^|]*` + 文件名」行失明: `grep -E 'A|B' ~/.bashrc` → exit 0 (`guard §0` 第 6 条 (ii))。",
  "   2. 参数里引号内的 `|` 使一族「读取器 + `[^|]*` + 文件名」规则对该形态失明 —— 既有设计缺口 (证据位置 `guard §0` 第 6 条 (ii); 本 Spec 的 SC-19 19al 钉现状, 复现命令只留在研究笔记与探针)。")
E("本 Spec 在加延迟 (新行使多段命令的 CPU 时间约 +20–25%, 含 `$VAR` 引用的命令约 1.4–2.3 倍, 见 W14), 建议提高优先级",
  "本 Spec 在加延迟 (量级见 W14 与 Impact「性能」), 建议提高优先级")
A("   19. L1 的 BLOCKED 文案把外来文本裸回显",
  "   20. **未修复旁路的披露范围 (产品级, 请裁)**: 本 Spec、研究笔记与探针的已知限制行 (如 SC-19 19al、SC-22 22ah / 22aj / 22au / 22bh、SC-21 21n–21u) 按设计列出了尚未修复的旁路形态及其现状 (这是「已知限制逐项钉住」的代价: 钉住现状就要写出现状); 这些文件所在的工作分支可能已被推到可匿名读取的公开镜像。"
  "选项 A (**默认**): 现状保留 —— 本 Spec 的 7.1 / 7.2 只写类别与证据位置、不写可复现的量化与命令; 已公开的内容不动。选项 B: 先修后披露 —— 含可直接复现配方的段落 (研究笔记里的对应两处、探针里最直接的几个已知限制行) 在对应修复发版之前不再推到公开镜像; "
  "已推送内容的清理 (改写历史 / 删除远端分支) 是破坏性动作, 不在任何一次性授权内, 只能 owner 决定并执行。选项 C: 把披露规则成文 (如在 `standards/conventions/` 加一份未修复缺陷的披露规范) 再按它处置。")

# issue 收尾: the verification range is disclosed in one sentence (three seats asked for it)
E("以 `[REDACTED` 开头但不闭合的值仍检出 (SC-7 7j; 理由见 W3 保留判据)。",
  "以 `[REDACTED` 开头但不闭合的值仍检出 (SC-7 7j; 理由见 W3 保留判据)。关单评论另用一句披露验证范围: 探针与原型只在 Linux (GNU grep / sed, bash 5.2 与 3.2) 上跑过, 未在 MINGW64 / macOS (BSD grep / sed) 验证 (该 issue 的报告环境是 MINGW64)。")
E("评论逐条披露三处有意偏离后关闭;", "评论逐条披露三处有意偏离与验证范围 (未在 MINGW64 / macOS 验证) 后关闭;")
