# Proposal: secret-guard-bash3-multiline-hardening

> **⚠️ ADOPTION NOTE (owner 决策 2026-07-11, 双子星撞车和解)**: 本 spec (dev-claude/aria-runner-bot 起草) 经评估**质量高于**并发的 simonfish 侧 Level 2 实现 (已 ship v1.55.2/v1.55.3) —— 本 spec 的 post_spec R1 抓到了那个实现的真实缺陷 (NUL-in-field 绕过 Critical-2)。owner 决策 **B (和解, 非回退)**: 保留已 ship 的实现, 把本 spec 转为**权威设计**, 已 ship 部分标注如下, 未实现部分 (部件 B) 按本 spec 继续。
>
> **已实现 (v1.55.2 + v1.55.3, simonfish 侧)**:
> - 部件 A 字段提取 NUL 分隔 + read -d '' (v1.55.2) ✓
> - **NUL-in-field 守卫** (本 spec Critical-2 / SC-8): 字段数守卫恒 4, 否则 fail-closed (v1.55.3) ✓
> - **log_ack 多行净化** (本 spec qa M-3 / SC-9): CR/LF/TAB→空格 (v1.55.3) ✓
> - **#152 归因订正** (本 spec R1 code-reviewer): e8e847c 非 e9dc0f7 (v1.55.3 changelog) ✓
> - 部件 B **部分**: `^` 锚定前缀含分隔符+换行 + bare dump 后缀 (`;`/`&`/无空格`|`/换行) (v1.55.2/hotfix) ✓ —— 但**未达本 spec 的"命令替换/包装器全覆盖"** (见待实现)
>
> **本 spec 补入 (simonfish 侧发现, 本 spec R1 漏)**: **zsh re-exec guard** —— Claude Code hook runner 用 $SHELL (macOS=zsh) 忽略 shebang, 整 bash-specific 脚本体在 zsh 下 fail-closed 阻断全部工具。**这是 #154 在 macOS 上的真实执行路径, 本 spec SC-1 只测 bash 3.2 夹具、未覆盖 zsh 执行整脚本**。已在 v1.55.2 实现 (顶部 `[ -z "$BASH_VERSION" ] && exec bash`); 本 spec 的部件 A/C 应把 zsh 端到端纳入 SC。
>
> **部件 B 已实现 (v1.55.4, simonfish 侧, 2026-07-11)**: 命令替换 `$(env)`/反引号 + 组合 `{ env; }` + 单层包装器 (sudo/nice/timeout/xargs/nohup/stdbuf/doas/env/time/eval/setsid/ionice/unbuffer, dumper 须首个非 flag token) + `command env` 直接形式 (排除 `command -v env`) + shell 关键字位 (then/do/else/elif) + printenv 始终拦 + env 重定向 gap。**实现前重建 spike 正/反例矩阵 (51/51, 双子星 spike 在其容器本机无) + pre-merge code-review (2 Important 包装器过匹配/关键字位 + 1 Minor 赋值 FP 全修)**。**同时修掉 v1.55.2 引入的 FP 回归** (普通空格被当命令分隔符, `echo env`/`kubectl get env` 误拦)。测试 297→347。
>
> **残留 (fail-safe, 接受)**: 未列包装器 (flock/watch/proxychains 等) + 深层 shell 关键字位仍可能漏拦 —— 按 hook 威胁模型 (防意外泄漏非对抗证明) + 本 spec AD-3 (包装器残留 fail-safe) 接受。AD-3(a) `env FOO=1 printenv` 简单形式已被 wrapper 的 env 分支覆盖。
>
> **本 spec 全部部件已实现** (A 字段提取/re-exec/NUL 守卫/log_ack @ v1.55.2-3 + B 命令位 @ v1.55.4)。**可归档** (post_spec R2 免走 —— 实现已端到端验证 + code-review 收敛, 设计意图已实现)。
>
> **Status**: done (全部件已实现 + 验证 + code-review: A/re-exec/NUL/log_ack @ v1.55.2-3, B 命令位 @ v1.55.4; dev-claude 起草设计, simonfish 侧实现, 双子星撞车和解 owner 决策 B)
> **Spec Level**: 3 (Full — proposal + tasks)。理由: 代码量小 (单文件 ~15 行核心改动), 但 **blast radius 极高** —— 改的是 Rule #7 执行载体 `secret-guard.sh`, 拦在**每一次工具调用**必经路径 (PreToolUse x 两 matcher)。任一回归 = 全工具 fail-closed (死锁) 或 secret 静默泄漏。按 blast radius 定级 L3 (与 `shell-jq-crlf-hardening` #132 精确同型; 对照 `secret-scan-honest-downgrade` L2 因 PostToolUse 非阻塞)。
> **ship target**: aria-plugin (SOT `plugin.json` = v1.55.1) -> 下一 PATCH
> **变更目标**: `aria/` 子模块 (`hooks/secret-guard.sh` + `hooks/tests/`)。Spec 按 Rule #5 置主仓 `openspec/changes/`。
> **关联 Issue**: [#154](https://forgejo.10cg.pub/10CG/Aria/issues/154) (readarray/bash3, partial-repro/critical) + [#157](https://forgejo.10cg.pub/10CG/Aria/issues/157) (多行截断, security) + [#152](https://forgejo.10cg.pub/10CG/Aria/issues/152) (^ 锚定逃逸, confirmed/major) ; [#156](https://forgejo.10cg.pub/10CG/Aria/issues/156) = #154 重复, close
> **triage SOT**: `.aria/triage-comment-154.md` + `.aria/triage-comment-152.md`
> **spike SOT**: scratchpad `spike2.sh` (解析三方案 11/11 + 性能) + `spike_cmdpos.sh` (命令位识别 36/37)
> **审计轨迹 (post_spec, 5-agent convergence)**: R1 4/5 REVISE + 1 PWW [3 Critical: 裸 NUL 文档载体 (四方独立复现) / NUL-in-field 溢出 file_path 绕过 / bash3.2 夹具 enable-n 对子进程无效; Major: #152 归因订正 (git 史证 e8e847c 非 e9dc0f7) / compgen-e 漏 / parse 契约 / log_ack 多行日志破坏 / heredoc 组合误报] -> R1-fix (本 proposal) + owner 2 决策 (分隔符尽量全覆盖 / heredoc 误报接受靠 ack) -> 待 R2

---

## Why

一次性能优化 (`e9dc0f7`, v1.26.0, "O3 closure — jq consolidation + bash builtin regex sweep") 把 PreToolUse 输入解析从「3 次 jq + per-branch 提取」合并为「单次 jq + 四字段逐行 `readarray`」。这一 commit **引入两个 breaking 缺陷** (#154 + #157); 第三个缺陷 (#152) **早于 v1.26.0 即存在**, 但因与 #157 安全联锁而必须一并处理。

| # | 缺陷 | 引入 | 触发 | 后果 | verdict |
|---|------|------|------|------|---------|
| **#154** | `secret-guard.sh:118` 用 `readarray` (bash 4.0 内建) | e9dc0f7 (v1.26.0) | macOS 自带 `/bin/bash` 3.2 (Apple GPLv3 冻结) | `command not found` -> `_sg_fields` 空 -> `tool_type=""` -> `:126` fail-closed `exit 2` -> **两 PreToolUse matcher 全灭, 会话死锁** | critical |
| **#157** | 四字段「逐行」读, 但 `command` 值自身可含换行 | e9dc0f7 (v1.26.0) | heredoc / 多行脚本 | `command` 只截首行, 第 2 行错位成 `file_path` -> **secret-guard 只检查命令第一行** (Rule #7 静默失效) | critical (security) |
| **#152** | `env`/`printenv` 等 pattern 以 `^` 锚定整条命令开头 | **`e8e847c`** (从 SilkNode cherry-pick, **先于 v1.26.0**) | `cd /x && env` / `true; printenv` | 分隔符后 secret 读取逃逸 -> 凭据明文进 transcript + prompt 缓存 | major |

> **#152 归因订正 (R1 code-reviewer, git 史独立核实)**: `git log -S"'^[[:space:]]*printenv"` -> pattern 由 `e8e847c` 引入; `git show e9dc0f7 -- hooks/secret-guard.sh` 的 diff **未触及任何 env/printenv 锚定行**。故 #152 是**先存在的 coverage gap**, 非 v1.26.0 回归。

**三者为何一并修 (安全联锁, 非范围蔓延)**:

1. **#154 与 #157 是同一行** (`:118`): 修 #154 必须重写字段提取, 而「如何捕获多行 command」正是同一行的决策。
2. **#157 与 #152 互补且互相依赖**:
   - 只修 #152 锚定 -> #157「换行第 2 行 printenv」仍逃逸 (那行根本没进正则);
   - 只修 #157 截断 -> #152「`true; printenv`」(单行中段) 仍逃逸 (`^` 只匹配开头);
   - **安全联锁**: 截断修复让 `command` **首次携带换行**, 命令位锚定必须同时把换行当分隔符, 否则第 2 行 secret 读取依然逃逸 (R1 code-reviewer expB 实测)。

**为何长期未被发现 (dual-install 漂移)**: 主仓 `.claude/settings.json` 挂 `.claude/scripts/secret-guard.sh` —— 2026-05-20 (`76abf78`) 的旧本地副本, 用 `command="$(jq -r '.tool_input.command')"` 命令替换**完整捕获多行**, **免于 #154 + #157** (但 `:419-422` 仍含 #152 的 `^` 锚定, 故非「无缺陷」)。即 **Aria 自己 dogfood 免疫 #154/#157 的旧副本, 而经 `hooks/hooks.json` 分发给下游 (及 aria-runner Layer 2 容器) 的是缺陷版**。回归窗口 (#154/#157) **v1.26.0 -> v1.55.x**。

> 附注: triage 期间另发现 `aria-report/SKILL.md:59` 版本抽取缺陷 (所有 aria-report issue 恒报 1.47.0), 已立 [#158](https://forgejo.10cg.pub/10CG/Aria/issues/158)。**与本 Spec 无耦合, 不在范围** (owner 决策)。

---

## What Changes

### 部件 A — 字段提取重写 (修 #154 + #157)

`secret-guard.sh:118` 的 `readarray -t _sg_fields < <(...)` 替换为 **NUL 分隔 + `read -d ''`** (bash 3.2 安全, 无 `readarray`/`mapfile`)。jq 分隔符**必须写字面 `\u0000` (6 个 ASCII 字符), 绝不是裸 NUL 字节**:

```bash
# NUL 分隔 -> 字段值可含任意换行 (#157); read -d '' 自 bash 2.04+ 可用 (bash 3.2 安全)
# jq 用 \u0000 (纯 ASCII 转义, 运行时才产真 NUL) — 源码/git/复制安全
tool_type="" tool="" command="" file_path=""
{ IFS= read -r -d '' tool_type
  IFS= read -r -d '' tool
  IFS= read -r -d '' command
  IFS= read -r -d '' file_path
} < <(jq -j '(.tool_name|type), "\u0000", (.tool_name // ""), "\u0000", (.tool_input.command // ""), "\u0000", (.tool_input.file_path // ""), "\u0000"' 2>/dev/null <<<"$input" | tr -d '\r')
```

> WARNING **分隔符是字面 `\u0000`, 不是裸 NUL 字节** (R1 四方独立复现该 Critical: 裸 NUL 落进 `.sh` 被 bash strip -> 全平台 `exit 2` 死锁; 且令文档被 `file(1)`/`git` 判为二进制)。`jq` 对 `\u0000` 转义在**输出流**产真 NUL (`jq -jn '"a","\u0000","b"' | od -An -tx1` -> `61 00 62`, R1 backend 实测)。**本 proposal 起草曾两度踩此坑 (含首次重生成), 反证「裸 NUL 不可作文档载体」。**

**部件 A parse 契约** (R1 tech-lead M-2 + backend Critical-2):

| 边界 | 行为 | 依据 |
|------|------|------|
| 畸形 JSON (jq 报错) | `2>/dev/null` 吞错 -> 4 字段空 -> `tool_type=""` -> `:126` fail-closed exit 2 | 与旧路径一致 (R1 backend 实测) |
| `.tool_input == null` / 缺失 | jq `.tool_input.command // ""` 返 `""` 非报错 -> 恒 4 字段 | R1 backend 实测 |
| **字段值含 NUL** | **新失效机制**: jq 输出真 NUL 与分隔符同形 -> 字段错位, 危险内容溢出到 `Bash` 分支从不检查的 `file_path` -> 绕过扫描 (R1 backend Critical-2 实测) | **新增一致性校验** (见下) |
| 末尾字段无尾随 NUL (EOF) | 第 4 次 read exit 1 但值仍捕获; 代码不检查 read 退出码, 无影响 | R1 backend 实测 |

**NUL-in-field 防御** (R1 backend Critical-2): 解析后校验 `command` / `file_path` 不含嵌入 NUL (真实 shell 命令不可能合法含 NUL)。检出 -> fail-closed `exit 2` (而非静默错位放行)。

**log_ack 多行日志防御** (R1 qa M-3): `:251` `log_ack` 把 `$command` 写入 `~/.claude/logs/guard-bypass.log`。#157 修复后 `command` 可多行 -> 破坏该日志「一行一条目」不变量。写日志前把 `$command` 内换行转义 (如 `\n` 字面或空格)。

保留全部既有不变量: 单次 jq (保 O3 性能, R1 backend 实测 30ms/call ≈ 旧 readarray) / `tr -d '\r'` (#132 CRLF) / 空字段保留 (`read -d ''` 天然) / `tool_type` 类型校验链 (`:125-134`)。`readarray`/`mapfile` 从热路径彻底消失 (R1 code-reviewer: `:118` 是唯一可执行 bash4 构造, 去掉即 bash 3.2 通过, SC-1 可达)。

### 部件 B — 命令位识别 (修 #152, owner 决策「尽量全覆盖」)

`env`/`printenv`/`compgen -e`/`. .env`/`source .env` 的 `^[[:space:]]*` 前缀锚定, 升级为**命令位识别**。spike (`spike_cmdpos.sh`, 36/37) 验证的覆盖矩阵:

**命令位前缀** = 字符串开头 OR 分隔符 (`;` `&` `|` `(` `)` `{` 反引号) OR 控制字符 (含换行); **结尾收口** = 管道 OR 分隔符 OR 反引号 OR 换行 OR 字符串结尾。覆盖:

- **#152 主体**: `cd /x && env` / `true; printenv` / `false || env`
- **命令替换**: `x=$(env)` / `echo $(printenv KEY)` / 反引号 env
- **组合命令**: `{ env; }` / `{ printenv; }`
- **单层包装器启动器**: `sudo env` / `nice -n 5 printenv` / `timeout 5 env` / `xargs env` / `command env` / `nohup printenv` / `stdbuf -oL env`
- **换行后行首** (#157 联锁): 命令第 2/3 行的 env/printenv
- **compgen -e** (`:566`, R1 tech-lead M-1 + qa M-4): 拉入范围 — 同构的 `^` 锚定 env-dump

**env 双重身份处理** (spike 验证): `env` 严格无参收口 (裸 `env` / `env|grep` 拦; `env python` / `/usr/bin/env python` 启动器**放行**); `printenv` 可带参数 (`printenv KEY` 仍拦)。

**误报防线** (spike 12 反例全 ALLOW): `echo env` / `grep env file` / `envsubst` / `printenv_helper` / `my_env=1 make` / `cd /envs` / `kubectl get env` / `docker run`。结尾收口是防前缀词误伤的**强制项**。

### 部件 C — 回归测试 (不依赖 macOS)

`hooks/tests/` 补充:
- **bash 3.2 模拟夹具**: 用 `BASH_ENV=<临时 rcfile: enable -n readarray mapfile>` 前缀调用 (R1 qa C-2 实测: 裸 `enable -n` 对 exec 子进程无效, 现有 harness 只 exec 不 source, 会令证伪测试空洞通过; `BASH_ENV` 兼容现有 `bash_case`/`run_case` 零改动)。
- **two-state 断言** (SC-6): 复用 `hooks/tests/lib/crlf-shim.sh` 的 `crlf_assert_two_state` — pristine (保留 readarray / 保留 `^` 锚定) 必 FAIL, fixed 必 PASS。
- **字节级断言**: `jq -jn '... \u0000 ...' | od -An -tx1` 确认输出真含 `00` 字节。
- **9 条 missing negative cases** (R1 qa): 见「测试反例清单」段。

### 部件 D — 文档同步

- `secret-guard.sh` 内联注释: `:108-117` readarray 理由块失效 -> 改述 NUL 方案 + parse 契约 + 为何 bash 3.2 安全; 命令位识别意图注释 + `tr -d '\r'` 副作用 (AD-6)。
- `standards/conventions/secret-hygiene.md`: **已核实 (R1 KM + qa N-7 实机 grep): 无 `readarray`/`mapfile`/`^` 锚定实现细节引用, 此项预期 no-op**。
- **不改任何 SKILL.md** -> 不触发 Rule #6。

---

## Architecture Decisions (scope 边界)

- **AD-1 全仓 bash>=4 语法审计** = 后续独立 cycle。本 Spec 只清 `secret-guard.sh` 热路径的 `readarray` (R1 code-reviewer 核实无其他 co-fatal bash4 构造)。
- **AD-2 fail-closed 逃生口**: 不改 fail-closed 语义。部件 A 已消除最大内部错误源 (readarray)。是否为「hook 内部错误」增设 stderr 逃生指引 -> 留 Open Questions。
- **AD-3 命令位识别的诚实残留** (owner「尽量全覆盖」下仍纯正则不可达, spike 隔离): (a) **env 启动 dumper** `env FOO=1 printenv` (env 双重身份); (b) **嵌套/参数化包装器** `sudo -u bob env` / `a=1 sudo env` / `sudo nice env` / `watch -n1 env`; (c) **引号内容**。方向 fail-safe (漏拦非误拦, 除引号外)。部件 C 以这些为**回归锚点反例**。
- **AD-4 heredoc 组合误报接受** (owner 决策): #157 修复后 heredoc 正文含 `env`/`printenv` (作文件内容非命令) 会被命令位锚定误当命令拦截 (R1 qa M-1)。**纯正则无法可靠识别 heredoc body**。明确接受为已知代价, 用户遇到用 `# guard:ack:` 一次性放行。安全优先。
- **AD-5 字段编码 = NUL (`\u0000`) + 一致性校验** (R1 tech-lead m-1): spike 三方案 — NUL 11/11 正确 30ms; per-field 4xjq 129ms 否决; base64 空字段折叠 + macOS BSD `-D` 否决。
- **AD-6 `tr -d '\r'` 剥离命令内字面 `\r`** (R1 backend): 不影响执行 (secret-guard 只分析不改写) 且不制造绕过, 记为已知限制。
- **AD-7 SC-7 dogfood vs 本地副本** (R1 code-reviewer m3): SC-7 dogfood 需一次性同步修复版到 `.claude/scripts/` 验证; 或降级为「经 hooks.json 对下游生效」。owner 批准时定。

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | macOS 用户脱离全工具死锁 (#154); secret-guard 恢复对多行命令 (#157)、分隔符后/命令替换/组合/单层包装器 (#152 owner 全覆盖) 的 secret 读取拦截 |
| **Positive** | 回归测试首覆盖 bash 3.2 兼容面 + 多行 command + 命令位识别 + NUL-in-field 防御 + log_ack 多行日志; two-state 断言防空洞通过 |
| **Risk (误报)** | 命令位识别放宽 -> 新增误报 (heredoc body 已 owner 接受 AD-4; 其他由 spike 12 反例 + 结尾收口防线控制) |
| **Risk (性能)** | 单次 jq 保持, 无回归 (R1 backend 实测 NUL 30ms ≈ readarray 31.5ms) |
| **Risk (CRLF)** | 漏 `tr -d '\r'` -> 回归 #132。缓解: 部件 A 显式保留 + crlf 测试框架回归 |
| **Risk (绕过)** | NUL-in-field 注入 (backend Critical-2) -> 部件 A 一致性校验 fail-closed 堵死 |

---

## Design (spike 结论汇总)

- **解析方案** (`spike2.sh`, bash 5.2 + 模拟 bash 3.2 双跑): NUL 分隔 11/11 (多行/空字段/特殊字符/全缺/性能), per-field 129ms 否决, base64 空字段折叠 + BSD flag 否决。正确 `\u0000` 版接入 `secret-guard.test.sh` 259/260 (唯一 fail 为隔离目录缺 hooks.json, 与本 Spec 无关)。
- **命令位识别** (`spike_cmdpos.sh`, 36/37): 覆盖 #152 主体 + `$(...)` + 反引号 + `{}` 组合 + 单层包装器; 12 反例全放行 (含 env 启动器正确放行); 唯一未覆盖 `env FOO=1 printenv` -> AD-3(a) 残留。
- **联锁验证** (R1 code-reviewer expB): Part A 单独生效时 `ls\nprintenv` 仍 ALLOW (旧锚定只看整串首); Part A+B 后换行第 2 行 printenv MATCH。
- **实施顺序**: A 先于/同 B (B 的多行测试证据需 A 在位)。

---

## Success Criteria

- [ ] **SC-1 (#154)**: bash 3.2 模拟夹具 (`BASH_ENV`) 下, 良性 `Bash`/`Read` 输入 -> `exit 0` 放行 (当前 exit 2)。度量: `secret-guard.sh` 内**函数/行作用域**无 `readarray`/`mapfile` builtin **调用** (非 grep 计数 — `:433-434` 有合法 pattern 字符串)。
- [ ] **SC-2 (#157)**: 多行 command (secret 读取在第 2/3 行) -> BLOCK。字段提取后 `command` 完整保留全部行; `file_path` 不被命令第 2 行污染 (构造性正确: jq 按字段名取值)。
- [ ] **SC-3 (#152 + owner 全覆盖)**: 分隔符后 (`&&`/`;`/`||`) + 命令替换 (`$(env)`/反引号 env) + 组合 (`{ env; }`) + 单层包装器 (`sudo env`/`nice -n 5 printenv`) + 换行后行首 + `compgen -e` -> 全 BLOCK。
- [ ] **SC-4 (误报防线)**: `echo env` / `grep env file` / `envsubst` / `printenv_helper` / `my_env=1 make` / `env python` / `/usr/bin/env python` / `kubectl get env` -> 全 ALLOW。
- [ ] **SC-5 (行为等价)**: 空字段保留 / CRLF (#132) / jq 缺失 fail-closed / `tool_type` 类型校验链 -> **exit code 与修复前等价** (措辞用「行为等价」非「逐字节」— 部件 D 改注释/stderr 文案会破坏字面逐字节); 既有 `secret-guard.test.sh` + crlf 框架全绿。
- [ ] **SC-6 (可证伪, two-state)**: 复用 `crlf_assert_two_state` 写**点名** two-state 测试: readarray-pristine 与 `^`-锚定-pristine 各一条, pristine FAIL + fixed PASS。
- [ ] **SC-7 (dogfood + 留痕)**: 修复版部署 (AD-7 定路径) 后, 本会话多行含 env 命令被正确拦截 + 良性命令放行; **命令+结果留痕**入 tasks.md/PR。
- [ ] **SC-8 (NUL-in-field 防御)**: 合法 JSON 注入 `\u0000` 于 command -> fail-closed exit 2 (非静默错位放行)。
- [ ] **SC-9 (log_ack 多行)**: 多行 command 触发 `# guard:ack:` 放行后, `guard-bypass.log` 仍「一行一条目」。

---

## 测试反例清单 (部件 C 必含, R1 qa)

1. heredoc 正文含 `env`/`printenv` -> 期望 BLOCK (AD-4 接受的误报, 锚定为已知行为回归)
2. heredoc 正文含 `source .env` 文档文本 -> 同上
3. `/usr/bin/env python3 script.py` (shebang 启动器) -> ALLOW
4. `ls; # note: check env vars` (分隔符后是注释) -> ALLOW
5. `echo hi && echo "call env directly"` (分隔符后含 env 的字符串) -> ALLOW
6. `x=$(env)` / `echo $(printenv KEY)` (命令替换) -> BLOCK (owner 全覆盖)
7. `ls -la` 换行 `printenv` (仅换行触发, 无其他分隔符; pattern 用 `$'...'` 或真换行字节构造, 非字面 `\n`) -> BLOCK
8. guard:ack + 3 行 command -> 读 `guard-bypass.log` 断言一行一条目 (需给 test.sh 加日志断言能力)
9. bash 3.2 夹具负控制: readarray-pristine 副本 `BASH_ENV` 禁用下 exit 2; fixed 版 exit 0 (子进程兼容调用)

---

## Open Questions (供 post_spec R2 审议, 不阻塞)

1. **AD-2 逃生口**: 是否为「hook 内部错误」(区别 harness 畸形输入) 增设一行 stderr 逃生指引 (指向 `SECRET_GUARD_BYPASS_NO_JQ` 同款机制)? 抑或部件 A 消除最大错误源后已足够?
2. **AD-7 dogfood 路径**: SC-7 需一次性同步 `.claude/scripts/` 副本 (越过 AD-4 表述), 还是降级为「经 hooks.json 对下游生效」+ 本副本另行同步? owner 批准时定。
