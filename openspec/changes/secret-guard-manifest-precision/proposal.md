# secret-guard: claude 配置文件入敏感清单 (双平面) + 参数位置误报收敛 (Aria #179)

> **Level**: Minimal (Level 2 Spec)
> **Status**: 📝 **Draft (v3) — post_spec CONVERGED (R1→R2, 2 轮), 待 owner 批准进 A.2**
>
> ```yaml
> converged: true    # R1 3×REVISE (3C+6M+6m) → v2/v2.1 → R2 (A1 REVISE 2M / A2·A3 APPROVE) → v3 → 终判 3/3 PASS
> rounds: 2
> pending_owner:
>   - 批准进 A.2
>   - "TASK-0 安全门 (ship 前置, 独立于批准): 核实 2026-08-09 泄露的 *_API_TOKEN 轮换状态 — R1 A3-C1: handoff 全量检索无轮换记录, 疑似活凭据"
> ```
> **Issue**: [Aria#179](https://forgejo.10cg.pub/10CG/Aria/issues/179) (triage: confirmed / major / next-cycle, 复现 4/4 @ 1.66.3, `.aria/triage-report-179.json`)
> **认领**: track `secret-guard-manifest-precision` @ simonfish/bfe8285d (phase1_gate advisory, 2026-08-22, 无碰撞无同 issue 重叠)
> **基线冻结**: aria @ `400f0bc` (v1.66.3+2) — 行号/计数均对此 SHA
> **代码落点**: `aria/hooks/secret-guard.sh` + `aria/hooks/tests/secret-guard.test.sh`; Spec 落主仓 (Rule #5)

---

## Why

secret-guard 一漏一误, 方向相反, 2026-08-09 实际使用中同日命中, 当前版本 4/4 全量复现:

**漏报 (优先, 已致真实泄露)**: `~/.claude/settings.json` 的 `env` 节点是 Claude Code 存放 API token 的标准位置, 但它不在任何敏感清单里。triage 侦察发现缺口比 issue 报的**更宽 — 双平面**:

| 平面 | 位置 (@ `400f0bc`) | 现状 |
|---|---|---|
| Bash 命令面 | `:709-710` shell-rc 两 pattern | 只覆盖 shell 启动文件; 且 reader 列表 (12 个: cat…sed) **不含 `jq`** — 而 jq 是 JSON 配置的天然读取器, 真实泄露命令就是 `jq -c '{model, env: (.env // {})}' ~/.claude/settings.json` (实测 exit 0; R1 A2 席独立复测一致) |
| Read/Edit 路径面 | `:546` lower_path 正则 | 覆盖 .env/ssh key/aws/kube 等 **29 个分支**, **同样无 claude 配置文件** — `Read ~/.claude/settings.json` 今天直接放行 (R1 A2 席以嵌套 tool_input 探针实测 exit 0) |

**误报**: `:709` 形态 `(readers)[[:space:]]+[^|]*(敏感名)` 对敏感名出现在**命令行任意位置**都触发 — 包括正则/alternation 字面量位置 (`grep -oE '(\.bashrc|...)' <hook自身>` 被拦, issue 复现)。本 cycle triage 期间主 loop 写报告命令 (heredoc 文本含敏感名字面量) 亦被同类误拦, **活体二次复现**; 该类误报迫使正当操作走 `# guard:ack:` 通道, 磨损 ack 的信号价值。

## What Changes

**1. Bash 面新增 claude-config pattern (漏报修复主体)**: 新 pattern 行, 敏感名组 = `\.claude/settings\.json` / `\.claude/settings\.local\.json` / `\.claude\.json` (legacy 全局配置, 含 MCP token), reader 组 = **既有 12 reader + `jq`**。python3/node **不并入** (R1 A1-M1: 会重开 prose 误报) — 改为扩展既有窄先例 `:785/:786` (`python3? -c` / `node -e` + 源组) 的源组, 追加三条 claude-config 条目。

**1b. claude-config 作用域 credit 收紧 (R1 A1-C1, 本版新增)**: 字段白名单形状 credit (`\| jq '{...}'`, `:337`) 是**纯形状判定不查字段名**, 对 claude-config 源构成直接逃逸 — `cat ~/.claude/settings.json | jq '{env: .env}'` 恰好整块泄走 env 节点 (A1 席代理实测 exit 0)。「与 .env 同类已知面」的类比**不成立**: .env 非 JSON, 该逃逸在彼处实际死路; settings.json 是真 JSON 且有字面 `env` 键。⇒ **对 claude-config 源, `jq '{` 形状 credit 不适用**。**机制写死 (R2 A1-R2-1: 无顺序依赖)**: 判定**不依赖**「哪条 pattern 触发」的信息通道 (`_sg_compute_credit` 只接收 `$seg`, 无此通道) — 在 credit 计算内**对 `$seg` 重匹配 claude-config 源名组**, 命中即进入收紧模式; 混合源 segment (同段含 claude-config + .env) 因此**恒收紧** (更严方向, 无旁路)。

**收紧模式下的 credit 白名单 (R2 A1-R2-2 消歧, 封闭枚举)**: 仅 (1) jq 名字面类 (`keys`/`length`/`paths`, :332); (2) 计数 `wc -[clw]` (:384); (3) 哈希 `sha*/md5sum` (:387); (4) 丢弃族 (`>/dev/null`/`&>`/`-o /dev/null`, :373-380)。**行级过滤 credit 一并不适用** — grep 锚 (:348) / `grep -v` (:351) / sed (:354) / cut (:358) / awk (:362/:365): JSON 值可跨行、可内嵌同行, 行/列级过滤对 JSON 不构成可靠脱敏 (如 `grep '^  "model"'` 仍可整行带出同缩进的 token 行)。非 claude-config 源的全部 credit 规则**不变**。

**2. Read/Edit 面清单补齐**: `:546` 正则追加 `/\.claude/settings\.json$|/\.claude/settings\.local\.json$|/\.claude\.json$` (lowercased 匹配面, 与既有条目同构)。既有 ACK-PATH-ONESHOT 逃生舱原样适用。

**3. 误报收敛 — 前置字符白名单 (标签: 「非路径前缀位置」不触发)**: 敏感名组前加**单一白名单**判定 (R1 A3-M2: 不设并存排除集, 语义唯一): **仅当**敏感名前一字符 ∈ {**串首**, 空白, `"`, `'`, `=`, `/`} 时触发; 其余任何前缀字符 (`(` `|` `\` 及域内一切其他字符) 一律不触发。`~` 不入白名单 (R1 A2-m1: 真实 tilde 语法后必跟 `/`, 由 `/` 成员覆盖, `~` 成员结构性不可达)。

- **适用面点名 (R1 A2-M1/A3-M1)**: 全部**路径清单型** pattern 行 — `:709` shell-rc 行、本 spec 新增 claude-config 行、以及 `.env`/`id_rsa` 等同构 sibling 行 (B.1 入场时对 pattern 数组逐行枚举并在 detailed-tasks 列清单; 活体误拦命中的正是 .env 面, 只改 shell-rc 行治不到)。命令注入型 pattern (base64/sops 等) 不适用。
- **实现路径语义 (R1 A2-C1)**: 拦截路径对 risky_patterns 用裸 `[[ =~ ]]` **整串匹配** (非 `_sg_line_match` 逐行) — `^` 只锚**整串首**; 多行命令 (heredoc/换行) 中段行首不享受「串首」成员。fixture 必须含多行形态 (见 SC-4/SC-5)。
- **ERE 陷阱点名 (R1 A1-M2)**: 白名单类与既有 `[[:space:]]+[^|]*` 争用空白字符 — `cat .bashrc` (单空格+裸文件名) 形态下若实现为串联会结构性失配; SC-5 显式含此形态作守卫, Task 顺序先写 SC-5 再动 pattern。
- **范围边界 (已知限双类, 写入 hook 头注释)**: (a) **prose 位置完整路径文本** (heredoc 里含 `cat ~/.bashrc` 字样) 正则层不可分辨, 不治, 走 `# guard:ack:`; (b) **引号定界裸敏感名** (`grep '.bashrc' f` — 前一字符 `'` 在白名单内) 同样不治 (R1 A3-M1: v1 的「正则字面量位置」标签宽于机制, 本版标签已收窄为「非路径前缀位置」)。根治两类均需参数位置解析, 属 #138 同类架构面。

**4. 测试 (baseline-failing)**: 每个新拦截/新放行形态一条 fixture, 修复前红→修复后绿留痕; 全量回归既有套件 (基线计数对 `400f0bc` 实测记录)。误杀守卫: 既有 shell-rc 真实读取形态 (`cat ~/.bashrc` 等) 必须仍拦 — 前置字符类不得放走 `/` 前缀的真路径。

**5. 文档同步**: `standards/conventions/secret-hygiene.md` 自测计数回填 (#128 先例, 现值以 B.1 入场实测为准); hook 头注释补 claude-config 条目 + What.3 误报已知限双类 + **漏报结构限一类** (R1 A3-m2): bare-filename/glob 变体 (`cat settings.json` 相对路径裸名 / `cat ~/.claude/settings.*`) 与既有清单同构地不在匹配面内, 属清单型防线的结构限, 非本 spec 引入。

## Out of scope

- ~~credit 系统语义不动~~ **(v1 该条已被 R1 A1-C1 推翻并撤销)** — claude-config 作用域的 credit 收紧已入 What.1b; **通用面** (非 claude-config 源的 `jq '{` 形状 credit) 仍不动, 若要全局治理属独立 spec。
- **prose 位置误报 + 引号定界裸名误报** (What.3 已知限双类)。
- **跨段 fail-open 架构面** (#138 在案)。

## Success Criteria

> 每条过反事实 (「不实现会红吗」); 基线 = `400f0bc` 冻结树。

- **SC-1 (漏报主体, Bash 面)**: 真实泄露形态 `jq -c '{model, env: (.env // {})}' ~/.claude/settings.json` → exit 2 (基线 0, baseline-failing); 变体: `cat ~/.claude/settings.json` / `grep TOKEN ~/.claude/settings.local.json` / `python3 -c ... ~/.claude.json` 各 ≥1 条同断言。
- **SC-2 (漏报, Read/Edit 面)**: 探针**嵌套结构写死** (R1 A2-M2: 扁平结构 file_path 提取为空恒 exit 0 假窗口): `jq -n '{tool_name:"Read", tool_input:{file_path:"'$HOME'/.claude/settings.json"}}' | secret-guard.sh` → exit 2 (基线 0); settings.local.json / .claude.json 同; ACK-PATH-ONESHOT 对新条目可用 (nonce 流程走通 1 例)。
- **SC-3 (credit 面, 按 What.1b 新语义)**: 对 claude-config 源逐条写死: `cat ~/.claude/settings.json | jq 'keys'` → **0** (名字面 credit 有效); `... | jq '{env: .env}'` → **2** (形状 credit 不适用, 基线 0, baseline-failing — What.1b 核心断言); `... | wc -c` → 0; `jq '{model}' <file> >/dev/null` → 0; 直读无管道 (`jq '{model}' <file>`) → 2; **行级过滤排除 ≥2 条** (R2 A1-R2-2): `... | grep '^  "model"'` → **2**, `... | cut -d: -f1` → **2**; **混合源无顺序依赖 ≥1 条** (R2 A1-R2-1): `cat ~/.env ~/.claude/settings.json | jq '{env: .env}'` → **2** (恒收紧)。对照组: `.env` 源单独的 `| jq '{...}'` 行为**不变** (通用面不动守卫)。
- **SC-4 (误报收敛)**: issue 复现形态 `grep -oE '(\.bashrc|[^)]*)' <hook路径>` → exit 0 (基线 2, baseline-failing); alternation/转义位置变体 ≥3 条; **多行形态 ≥1 条** (heredoc 内含同形字面量, R1 A2-C1 整串匹配语义下验证); **`.env` 面字面量位置 ≥1 条** (R2 A2 carry: 适用面点名不只进人工枚举清单, 须有 SC 直接锁定 — 活体误拦命中的正是该面)。
- **SC-5 (误杀守卫, 反事实关键)**: `cat ~/.bashrc` / `grep X ~/.zshrc` / `sed -n 1p /etc/profile` / **`cat .bashrc` (单空格裸文件名, R1 A1-M2 争用形态)** / `cat "$HOME/.bashrc"` (引号+`/` 前缀) 全部仍 exit 2; **多行真实读取 ≥1 条** (heredoc 中段行首的 `cat ~/.bashrc` — 「串首」成员不覆盖时仍须由空白/`/` 成员拦住) — 前置白名单写错方向本条必红。
- **SC-6 (零回归)**: 全量既有测试绿, 计数不低于 `400f0bc` 基线实测值。
- **SC-7 (文档同步)**: secret-hygiene.md 计数与 hook 头注释更新落地; 勘正执笔人 ≠ 实现执笔人。

## rule6_note (Rule #6 申报)

变更为 hook bash 代码 + 测试 + 文档计数, **零 SKILL.md description/指令面变更**。hook 判定逻辑 AB 套件结构上测不到 (#128 同款先例) → substitute = 上述 SC-1..SC-6 baseline-failing 结构化测试 (红绿窗口留痕)。SOT: `standards/conventions/skill-benchmark-exemption.md`。

## Impact

- **版本**: aria-plugin PATCH; 目标版本不写死, bump 前 re-check SOT 顺延重算 (#128/#147 两次撞车教训)。
- **行为变更申报 (两向)**: (1) 新拦截: claude 配置文件三条目双平面 + claude-config 源 credit 收紧 (从放行→拦截, 收紧向, 无 fail-open 面); (2) 新放行: 敏感名在**非路径前缀位置**的命令 (口径同 What.3 白名单语义; 从误拦→放行, **须 SC-5 反向守卫**证明只放白名单外前缀)。
- **同步面**: aria 子模块 (hook + tests) + standards (secret-hygiene.md 计数) + 主仓 gitlink; CHANGELOG 两类。
- **关联**: #179 (Closes)。**凭据轮换 = TASK-0 owner 门** (R1 A3-C1 撤销 v1 的错误引证: 08-20 handoff 闭环的是 registration-token 另案; #179 的 2026-08-09 泄露 `*_API_TOKEN` 经 docs/handoff/ 全量检索**无轮换记录** — 按 secret-hygiene「代码脱敏不闭环, 须轮换」, ship 前 owner 须核实该凭据已轮换或当场轮换)。

## Tasks (A.2 细化; 骨架)

- [ ] **TASK-0 (owner 安全门, ship 前置; 即 Status 头与 Impact 所称 TASK-0, 编号统一)**: 核实 2026-08-09 泄露的 `*_API_TOKEN` 已轮换; 未轮换则先轮换再 ship
- [ ] 1.1 Bash 面 claude-config pattern + What.1b credit 收紧 + SC-1/SC-3 fixtures; python3/node 走 :785/:786 源组扩展
- [ ] 1.2 Read/Edit 面清单 + SC-2 fixtures (含 nonce 流程 1 例)
- [ ] 1.3 前置字符类误报收敛 + SC-4/SC-5 fixtures (先写 SC-5 守卫再动 pattern)
- [ ] 1.4 全量回归 + 基线计数实测 (SC-6)
- [ ] 1.5 文档同步 (SC-7, 换人执笔)
- [ ] 1.6 ship: 版本 re-check + bump + 三仓双推 + ls-remote + gitlink 核验
- [ ] 1.7 release claim (D.2b) + close #179

---

**起草**: 2026-08-22 (主 loop, 基于 triage 4/4 复现 + 双平面代码侦察 @ `400f0bc`)
