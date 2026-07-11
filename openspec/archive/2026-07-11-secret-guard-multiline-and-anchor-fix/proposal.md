# Proposal: secret-guard 多行字段解析 + `^` 锚定正则修复 (四票并案)

> **Status**: done
> **Shipped**: 2026-07-11 v1.55.2 — aria-plugin PR#103 merged `023351b`; pre-merge review 3 critical 实测正确 + Important#1 后缀逃逸修 + dogfood 生效实证
> **Level**: 2 (Minimal)
> **Created**: 2026-07-11
> **Source**: Aria#154/#156 (macOS 崩溃) + #157 (多行截断) + #152 (中段 env 逃逸)
> **Carry-id**: carry-secretguard-fieldparse-anchor
> **Triage**: `.aria/triage-report-{154,156,157,152}.json` (verdict: #154/#157 confirmed critical, #152 confirmed major, #156 dup closed)

## Why

`hooks/secret-guard.sh` 是 Rule #7 的执行载体 (PreToolUse hook, 默认启用)。`/issue-triage` 四票核对确认**两个独立缺陷**, 均由 `e9dc0f7` (v1.26.0, jq consolidation) 引入, v1.26.0–v1.55.1 全部受影响:

**缺陷 A — `:118` `readarray` 逐行读** (一行两症状):
- **崩溃** (#154/#156, critical): `readarray` 是 bash-4.0+ builtin, macOS 系统 `/bin/bash`=3.2.57 + zsh 均无 → hook 崩溃, `_sg_fields` 空 → `tool_type` 空 → `:125` fail-closed **阻断全部工具**, 会话死锁。
- **截断** (#157, critical): `tool_input.command` 可含换行 (heredoc/多行脚本), 逐行读在第一个换行处截断 → 命令第 2 行起**从未进任何拦截正则**, 且第 2 行被错当 `file_path`。**secret-guard 只检查命令第一行** = Rule #7 静默失效。本机实测: `echo begin\nprintenv` → exit 0 放行 (应 BLOCK)。

**缺陷 B — `^` 锚定正则** (#152, major): `:463-464` `^[[:space:]]*env([[:space:]]+\||[[:space:]]*$)` 只匹配命令开头; `;`/`&&`/`||`/`|` 后的 env/printenv 逃逸。本机实测: `echo hi; env | grep TOKEN` → exit 0 放行 (应 BLOCK)。同类 `^` 锚定 reader pattern (`:438-439` `. .env`/`source .env`, `:465-466` `/bin/printenv`, `:566` `compgen -e`) 需一并排查。

A 与 B **互不覆盖**: 只修 A, 单行中段 env 仍逃逸; 只修 B, 多行首行 env 仍被截断。两者都要修。

**dual-install 漂移** (为何长期未发现): 主仓 `.claude/settings.json` 挂 `.claude/scripts/secret-guard.sh` (2026-05-20 旧本地副本, 逐字段命令替换完整捕获多行、无 `readarray`)。即 **Aria 自己 dogfood 的是好副本, 分发下游 + aria-runner Layer 2 容器的是坏版本**, 漂移掩盖回归。修复必须同步两文件。

## What Changes

`hooks/secret-guard.sh` (分发版, 权威 SOT):

1. **缺陷 A: `:118` 字段提取改 NUL 分隔** (owner 决策 2026-07-11):
   - `jq -j '..., "\u0000"'` 输出 NUL 分隔 (非逐行), `while IFS= read -r -d '' field` 读入数组。
   - bash 3.2 兼容 (不用 `readarray`/`mapfile`); 字段值不可能含 NUL → 多行 command 完整捕获 (根治 #157)。
   - **保留** `tr -d '\r'` 等效行为 (#132 Windows CRLF fail-closed 防护) + 空字段保留 (`:108-110` 原诉求, NUL 分隔天然不折叠)。
1b. **re-exec to bash guard (zsh 端到端实测揭示, #154 更深根因)**:
   - **实测发现**: 只做 NUL 字段提取后, zsh 直接执行脚本仍对**所有输入** fail-closed (合法 `ls` 也 exit 2) —— zsh 对 bash-ism (`read -d ''` / `[[ =~ ]]` / 数组下标从 1 起 / 进程替换) 处理不同, 整个脚本体在 zsh 下错乱。Claude Code hook runner 用 `$SHELL` (macOS = zsh) 忽略 shebang, 故 #154 deadlock 根因**不止 `readarray`**, 是整个 bash-specific 脚本体在 zsh 下崩。
   - **修复**: 脚本顶部 (POSIX-sh 语法) 加 `if [ -z "${BASH_VERSION:-}" ]; then exec bash "$0" "$@"; fi` —— 无论 hook runner 用何 shell, 脚本体永远在 bash (3.2+, macOS 有 /bin/bash) 执行。zsh 实测: 加 guard 后合法命令 exit 0 / secret exit 2, 与 bash 等价。
2. **缺陷 B: `^` 锚定正则改分隔符后也匹配**:
   - env/printenv/`. .env`/source/compgen 等 `^[[:space:]]*` 锚定 pattern 改前缀 `(^|[;&|]|[[:space:]])[[:space:]]*` (命令分隔符**及换行**后也匹配)。**关键**: 前缀含 `[[:space:]]` (覆盖换行) 而非 issue 建议的 `(^|[;&|]|&&|\|\|)` —— 缺陷 A 修好后多行第 2 行的 env 前是 `\n`, issue 前缀漏换行仍逃逸 (实测验证)。
   - 全文件排查, 命中 7 处锚定 reader pattern 全改。
   - **bare dump 后缀重构** (pre-merge code-review Important#1): 原后缀 `([[:space:]]+\||[[:space:]]*$)` 只 block "env 后跟 ` |`/行尾", 漏了 env 后跟 `;`/`&`/无空格 `|` (如 `echo hi; env; echo done`、`env|grep` 仍逃逸 —— 与 #152 同类, canonical 测试过仅因管道前恰有空格)。后缀改 `([[:blank:]]*($|[;&|]|[[:cntrl:]]))`: env 后可选水平空白然后 (行尾 | 分隔符 | 控制字符[换行]) → block; env 后 "空格+参数" (`env FOO=bar cmd` / `printenv PATH`) 三分支均不匹配 → ALLOW 保持。tab 分隔参数 (`printenv\tPATH`, 极罕见) 落 `[[:cntrl:]]` 分支被保守 over-block —— 接受为 fail-safe (拦 dump 比漏 dump 安全)。4 处 dump 后缀 (env/printenv/compgen/docker-exec) 一并对称加固。

`.claude/scripts/secret-guard.sh` (主仓 dogfood 副本): 同步等效修复, 消除 dual-install 漂移 (否则 dogfood 继续掩盖回归)。

`hooks/tests/secret-guard.test.sh`: 新增 26 回归 case (260 → 286, **RED-first**, 修复前 11 FAIL):
- 中段 env (7): `echo hi; env | grep X` / `echo hi;env` / `&& printenv` / `|| env` / `| env` / `; /bin/printenv` / `; compgen -e` 期望 BLOCK。
- 多行 command (5): `echo x\nenv` / `set -e\necho x\nprintenv` / `printenv\necho done` (首行保持) / mid-line `\necho two; env` / heredoc `nomad var get` 第 4 行 期望 BLOCK。
- 不误拦 (4): `echo myenv` / `cat environment.txt` / `echo begin\necho done` / `echo "run printenv to debug"` 期望 ALLOW。
- **静态断言 (4)**: 脚本不含 `readarray`/`mapfile` 字段提取 + 含 re-exec-to-bash guard + `BASH_VERSION` 检测 (不依赖 zsh/macOS)。
- **zsh 端到端 (6, 条件跑)**: `command -v zsh` 存在时用 zsh 直接执行 hook 验证 re-exec guard (secret BLOCK / 合法 ALLOW 与 bash 等价); CI 无 zsh 则 SKIP, 静态断言兜底。

## Impact

- **版本**: aria-plugin v1.55.1 → **v1.55.2** (PATCH — bug fix, 无新功能/无破坏); 5 版本文件同步。
- **行为变化**: 缺陷修复方向 = **收紧** (原漏放行 → 现拦截), 无放松; 现有 260 case 全绿保持 (回归防误伤合法命令)。
- **Rule #6 / #7**: secret-guard 是安全 hook, 走 deterministic structural substitute (bash 回归测试 260→286) + RED-first (先证修复前 11 FAIL) + zsh 端到端 + pre-merge code-review。属 Rule #7 载体加固。
- **风险 (已实测消解)**: NUL 分隔 `read -r -d ''` 的 zsh 兼容性经实测**确认不足** —— zsh 直接执行时整脚本 fail-closed。故追加 re-exec-to-bash guard (脚本体永远在 bash 跑), zsh 实测通过。残余: bash 3.2 本机不可得 (Linux/bash 5.2), 但 `read -d ''` 自 bash 2.04 文档保证 + re-exec 确保永在 bash, 且静态断言兜底 (无 readarray/mapfile)。

## Verification

- RED-first: 新 case 修复前 11 FAIL (证测试真抓缺陷), 修复后 286/286。
- 基线不回归: 原 260 case 保持 PASS。
- zsh 端到端实测: 加 re-exec guard 前 zsh 全 fail-closed (合法 ls 误拦), 加 guard 后 zsh 与 bash 等价 (secret BLOCK / 合法 ALLOW)。
- 双文件一致: `hooks/` 与 `.claude/scripts/` 覆盖后**字节一致** (`diff -q` IDENTICAL), 副本 bash+zsh 端到端通过。
- 源码卫生: 无真 NUL 字节 (jq 程序用可见 `\u0000` escape, 运行时产生 NUL)。
- pre-merge code-review (安全修复) + 版本 5 文件同步检查。
