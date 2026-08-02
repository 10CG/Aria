# secret-guard: 补 `nomad var put` 拦截 (Aria #170 第 3 环, 最小范围)

> **Level**: Minimal (Level 2 Spec)
> **Status**: ✅ **Done** (shipped 2026-08-02: aria-plugin `183836b` v1.65.4 / standards `7e2b48c` v1.1.1 / Aria `5b914c5`; 6 项转出已立案 aria-plugin#128-132 + Aria#171; #170 保持 open — 要求 1 属 owner/infra。Approved owner sign-off 2026-08-02; post_spec R1→R4, R4 = 2 PASS + 3 REVISE 且 0 Critical, 剩余文本项已按审计方逐字建议全部落地; tech-lead 与 code-reviewer 均明示不必开 R5)
>
> ⚠️ **流程留痕 (作者自陈)**: R3 审计进行中 (14:45) 作者改写了本文件与 `secret-hygiene.md`, 违反「审计只审不改、编辑落轮间」纪律 (R3 tech-lead 察觉并按新版复核)。后果 = R3 五方读到**不同版本**, 其 SOT 相关 findings 中 §4.4 一条实为读旧版所致 (已核实工作树该处早已订正)。本轮起严格遵守: R4 期间零编辑。
> **Created**: 2026-08-02
> **Issue**: [Aria #170](https://forgejo.10cg.pub/10CG/Aria/issues/170) (partial-repro → 目标重定向)
> **审计轨迹** (五方合计, **统一口径 = 原始计数**, 去重数另注; R4 code-reviewer m-1 勘正前一版三处混用口径):
> R1 `1C+13M+21m` → 大改 → R2 `4C+13M+24m` (严重度未下降) → **owner 裁定缩到最小可 ship, 架构面另排** → R3 `3C+15M+15m` (去重后 2C; 四类并列: SC 互斥 / 两条 R2 静默丢弃 / SOT 订正三重脱节 / 作者中途改文件引发的文档不一致 —— **前三类与中途改写无关**) → R4 `0C+8M+18m` (2 PASS + 3 REVISE; 全为文本项, 含一条被实测证伪的「不可兼得」断言) → 收尾编辑 (R4 机械项) → ship
>
> **本 cycle 三次「未实测即断言」** (作者自陈, 供转出 4/5 收口者引以为戒): (1) R1「六形态无假阴无假阳」→ R2 证伪 (`curl -v … >/dev/null` 是假阴); (2) R2 采信 `-out=keys` 为合法安全写法 → R3 实机核验为非法 flag; (3) R3「SC-3/SC-4 不可兼得」→ R4 实测可兼得 (放宽字符类)。三次均由审计方实跑推翻, 无一由作者自查发现。

## Why

### 事故第 3 环的真实机制

#170 是真实凭据泄漏 (T4 `aria-build-bot-2026-Q3`, fingerprint `446b79`, 已进 prompt cache)。issue 归因为「回显走 stderr」。核实后真实机制不同 —— nomad CLI v1.11.2 `var put --help`:

```
-out (go-template | hcl | json | none | table)
   Format to render created or updated variable. Defaults to "none" when
   stdout is a terminal and "json" when the output is redirected.
```

**Claude Code Bash 工具的 stdout 是 pipe 而非 terminal** ⇒ nomad 判定「输出被重定向」⇒ 默认渲染完整变量 JSON (含解密 `Items`) 到 **stdout** ⇒ 进 AI 上下文。而 `secret-guard.sh:406` 的 pattern 只列 `nomad[[:space:]]+var[[:space:]]+(get|list)`, **`put` 零覆盖** (140 条 pattern 全文 grep 核实)。

### 不做 issue 要求 2 (前提证伪)

要求 2 是「`/v1/var/` 读写分离 — 写向 PUT 不回显 secret 却被拦」。经 [Nomad Variables API 文档](https://developer.hashicorp.com/nomad/api-docs/variables/variables) 核实: `PUT /v1/var/:var_path` 成功响应 body **含解密后的 `Items`**。故无 redirect 的写向 PUT 确实回显, 拦它正确 ⇒ **要求 2 关闭, 零代码改动**。

### 为什么本 spec 只做最小范围 (owner 裁定 2026-08-02)

R1/R2 两轮审计暴露 hook 的**结构性前提**: 所有判定 (pattern 匹配 / `has_filter` credit / 任何豁免) 都是**整命令字符串扫描**。shell 复合命令 (`a; b`) 下, 命令任一段出现的 credit/豁免串会泄到全部其他段:

```
cat /opt/.env; echo hi >/dev/null                    # 实测 exit=0 — .env 读被放行
nomad var get <真读>; nomad var get -out=X <另一路径>  # 同族双出现, 首条真读被放行
```

我在 R1、R2 各提过一版豁免设计 (全局 credit → pattern 作用域), **两版都被实测推翻**, 且 347 条全量回归对两次退化**都全绿** —— 现有测试集对这一维度结构上无鉴别力。根治需把判定改为「按 shell 分隔符切段逐段独立判定」, 影响全部 140 条 pattern 与 347 条用例语义, 超出 Level 2。

**故本 spec 只做零豁免的最小增量**: 补 pattern, 安全形态沿用**既有** `has_filter` credit (`>/dev/null` / `-o /dev/null`), 不新增任何豁免机制。架构面 + 其余 R1/R2 findings 全部转 §转出。

### 测试面盲区

`hooks/tests/secret-guard.test.sh` 现有 347 条中相关用例全为**读向**, 写向零锁定。两个口径分开说 (R4 code-reviewer m-2 勘正):

- `/v1/var/` **HTTP** 形态: L56-L418 区间内共 **37 处**;
- `nomad var` **CLI** 形态: `:55` / `:601` / `:681` **三条, 全在该区间之外**。

(该文件头部注释当时写「~50 cases」也是陈旧的 —— 本 spec R1 曾据此把基线误记为 ~50, 收尾时一并同步为实况。)

## What

**唯一改动**: risky_patterns 增补一条

```
'nomad[[:space:]]+var[[:space:]]+put([[:space:]]|$)'
```

- 位置: 紧邻既有 `nomad[[:space:]]+var[[:space:]]+(get|list)` (`:406`) 同组。
- **尾边界必带** (R1 backend m-2 实测: 无边界会误配 `nomad var putty`)。既有 `(get|list)` 条同缺陷 → §转出。
- 命中后走**既有** `has_filter` 闸门, 零新增豁免逻辑: `>/dev/null` / `-o /dev/null` / `&>/dev/null` 等既有 credit 继续生效。
- BLOCKED 提示: 沿用现有全局 heredoc, **不加 nomad 专属建议** (R1 qa M1: 该 heredoc 全 pattern 共享, 加专属内容会污染 vault/aws 等无关拦截; 条件插入方案连同 `$pattern_hint` 的 `set -u` 风险 → §转出)。现有清单里的 `>/dev/null` 一行已足够指出正解。

### Key Deliverables

- `aria/hooks/secret-guard.sh` — 1 条 pattern (唯一生产代码变更)
- `aria/hooks/tests/secret-guard.test.sh` — 写向用例族 (SC-1~SC-6 + SC-8 的 hook 断言, 实施后实际 **19 条** = 7 条 baseline-failing + 12 条回归锁; SC-7 是对 SOT 文本的 grep 断言, 不入本文件)
- `standards/conventions/secret-hygiene.md` — **4 个推荐位**的 `-out=keys` 错误示例订正 (§1 Verification 定义行 / §3.3 python / §3.4 bash / §4.4 「正确替代」句) + 新增两段反坑警示 (`-out=keys` 不存在 / `>/dev/null` 单挡 stdout 不够) + Version 1.1.0→1.1.1 (跨仓 co-land, 见下)

### 附带修复: Rule #7 SOT 的错误示例 (owner 裁定本 session 修)

`secret-hygiene.md` 共 **4 个推荐位**教用 `nomad var get -out=keys` 作为 metadata 验证法 (§1 Verification 定义行 L39 / §3.3 python 例 / §3.4 bash 例 / §4.4 「正确替代」句)。实机核验 nomad v1.11.2 **该 flag 值在三个子命令上均非法**:

| 子命令 | `-out` 合法枚举 | 含 `keys`? |
|--------|----------------|-----------|
| `var get` | `go-template \| hcl \| json \| none \| table` | ❌ |
| `var put` | 同上 | ❌ |
| `var list` | `go-template \| json \| table \| terse` | ❌ |

实跑报错: `Invalid value for "-out"; valid values are [go-template, hcl, json, none, table]`。

**且是双重错误**: SOT §3.4 原写法 `keys=$(nomad var get -out=keys … 2>/dev/null)` 即便 flag 合法也会**被 hook 拦** (实测 exit=2) —— `2>/dev/null` 只挡 stderr, 不构成有效 filter。读者 (人与 AI) 照做连撞两次失败后极可能转向不安全替代, 与 #170 事故链第 2→3 环同构。

订正为 `nomad var get -out=json … | jq '.Items | keys'` (实测 exit=0 放行; **不可写成 `keys[]`** — 方括号会破坏 hook 的 jq filter 识别, 实测 exit=2) 与 exit-code 存在性验证两式, 并新增反坑警示段落。

## 关键决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 豁免机制 | **一律不做** | R1/R2 两版豁免设计均被实测推翻 (整命令扫描下必泄漏); 零豁免 = 零新增风险面 |
| 安全形态出路 | 沿用既有 `>/dev/null` credit | 已在 BLOCKED 提示清单内; 与 `secret-hygiene.md` §3.4 现有推荐一致 |
| 要求 2 (读写分离) | 不做, 关闭 | Nomad 官方文档证伪其前提 |
| 提示文案 | **不改** | 全局共享 heredoc, 加专属内容会污染无关拦截 (R1 qa M1)。**验收锚点 (R4 code-reviewer m-5)**: `git diff` 中 `secret-guard.sh` 的改动**仅限** risky_patterns 数组内的新增行, heredoc 区 (`:654-:682`) 零改动 —— 这同时是 rule6_note「未改任何 AI 指令面」论证的可证伪支撑。**实测已核**: 本 cycle `secret-guard.sh` diff 仅 +10 行 (1 条 pattern + 9 行设计意图注释), 全部落在 risky_patterns 数组内 |
| stderr 假阴 / FP 守卫 / ack 文案 | **转出** | 各自独立裁量面, 混入本 spec 会重演 R1/R2 的范围失控 |
| SOT `-out=keys` 订正 | 本 cycle co-land | owner 裁定; 事实性错误, 与本 spec 同源 (都是 nomad var 命令的正确用法) |
| 备选: PostToolUse `secret-scan.sh` 替代 | 否决 (保留为纵深) | 它确在本次事故中检出泄漏, 但 PostToolUse 在执行**之后**运行, 值已进上下文 — 只能告警不能阻断 (本 session 起草时又实证一次) |

## Impact

- 影响面: `secret-guard.sh` 1 行 pattern (140 → **141** 条) + 测试 (347 → **366** 条); `secret-hygiene.md` **4 个推荐位** + 两段警示 + 版本历史行。零 skill / 零 schema。
- **覆盖率上限 (R4 tech-lead M-3)**: 新 pattern 仅对**单命令**有效。复合命令 (`a; b`) 中任一段携带 redirect credit 时全段放行 —— 含「一次写多个 var」这一日常形态 (SC-8 锁定现状, 归转出 1)。故本 spec 是**部分覆盖**, 不宜表述为「`put` 已受保护」。
- 版本: PATCH → aria-plugin **v1.65.2** (SOT `plugin.json` 现 1.65.1)。
- 兼容: 纯新增拦截面 (此前 `put` 零覆盖), 既有放行/拦截行为不变 — 由 SC-5 全量回归 (347 条) 锁定。
- 风险: 新 pattern 的 FP 面 — **实测远小于起草时预估** (R3 三方收敛 + 作者复核): 尾边界 `([[:space:]]|$)` 使「`put` 后紧跟引号」的文本提及**不匹配**, 故 `grep -rn 'nomad var put' aria/` 与 `echo "改用 nomad var put"` 均**放行**; 仅当被引文本里 `put` 后**真有空格**时才拦 (如 `git commit -m "fix: nomad var put 回显"`)。**最高频的一类是 `nomad var put --help` / `-h`** (R4 code-reviewer m-8: 实测均 exit=2, 原版为 0) —— 它落在「`put` 后真有空格」通则内, 而本 cycle 的 dogfood 里就有两次是读 `--help`, 说明这是开发者最常撞的形态, §转出 4 收口时不必重新发现。本 spec 接受该残余 FP, 出路是既有 `# guard:ack` 逃生门 (注意其文案/实现不符, 转出 3)。既有 `(get|list)` 条已有同类且**更宽**的 FP —— 本 session dogfood **五次**实证 (读 `--help` ×2 / 审计 agent 测试命令 / 写文档时 heredoc 内引用命令文本 / grep 搜索词含该串), 故非新增行为类别。
- ship 同步面 (R4 code-reviewer m-6 拆清口径): aria 子模块 = **2 交付文件** (`hooks/secret-guard.sh` + 其测试) **+ 5 版本同步文件**; standards 子模块 1 文件; 主仓双 gitlink + VERSION + README badge (i18n B 档)。
- issue 收尾: ship 后 #170 发进展 comment; **不关闭 issue** — 要求 1 (轮换 T4 + revoke `446b79`) 是 owner/infra 项且仍阻塞 cesura, 须由 owner 决定何时关或拆分。

## 转出 (本 spec 明确不做, ship 时逐条开 issue)

1. **[架构, 高]** hook 判定的**整命令扫描**前提 — 复合命令下 credit/豁免必泄漏 (`cat /opt/.env; echo hi >/dev/null` → exit=0)。根治 = 按 shell 分隔符切段逐段判定, 影响 140 pattern + 347 用例。R1/R2 共 3 方独立命中。
2. **[缺陷, 中]** stderr 假阴家族 — **两个工具族, 修法须一并考虑** (R3 tech-lead 指出前一版只写了 curl 侧, nomad 侧被静默丢弃):
   - **curl 侧**: `-v` / `--verbose` / `-vv` / `--trace*` 与纯 stdout redirect 组合放行, 但请求体回显走 stderr (实测 `curl -v -X PUT … >/dev/null` exit=0)。
   - **nomad 侧**: `nomad var put -verbose … >/dev/null` 同样放行 (实测 exit=0), 而 `-verbose` 的输出**按 nomad 设计走 stderr** (`--help`: "Provides additional information via standard error")。**这一条尤其要紧**: 本 spec 把 `>/dev/null` 作为 `nomad var put` 的**主推安全出路**, 该出路在 `-verbose` 下自身有洞。
   - **重定向顺序陷阱 (R4 tech-lead M-2)**: 判据须显式要求 `2>&1` 出现在 stdout 重定向**之后**才算挡住 stderr。`2>&1 >/dev/null` 是反例 —— `2>&1` 先把 stderr 复制到**当时的** stdout (仍是 chat-visible 管道), 之后 stdout 才被挪走, stderr 根本没挡住; 实测该形态 hook **放行** (exit=0)。任何朴素的「命令里出现 `2>&1`」判据都会误给 credit。
   - **第二条 stdout-only credit 路径**: `-o /dev/null` (`secret-guard.sh:390`) 与 `>/dev/null` 同属只挡 stdout 的 credit, 且该谓词**不锚定 curl** —— 实测 `nomad var put p @f -o /dev/null` 亦 exit=0 (一个 nomad 根本不存在的 flag 换来放行)。同一修法须覆盖两条路径。
   - **注意**: 修法须锚定具体命令语境, 裸扫 `-v` 会撞既有 `grep -v` filter credit (R2 backend M-2)。
   - 缓解 (已做): SOT `secret-hygiene.md` 已补两段警示 — 全 redirect 必要性 + 顺序敏感 (`2>&1 >/dev/null` 无效)。
3. **[缺陷, 中]** `# guard:ack` 文案与实现不符: 实现要求**首 token ≥8 连续非空白** (正则 `[^[:space:]][^[:space:]]{7,}`), 文案写「reason ≥ 8 NON-WHITESPACE chars」(总长语义) ⇒ 合法使用下逃生门失效 (本 session dogfood 实证: 理由首词 `reading` 仅 7 字符即失败)。落点经 R4 全仓实测 = **8 处 5 文件** (前一版写「6 处 3 文件」且把姊妹 hook 行号安到本 hook 上, 已勘正): `aria/hooks/secret-guard.sh` L300/L314/L679 · `aria/hooks/host-docker-logout-guard.sh` L29/L63/L157 · `aria/README.md` L147 · `aria/README.zh.md` L147 (**i18n 同步面, 收口时会触发 i18n 一致性 check**) · `standards/conventions/secret-hygiene.md` L298 (**本 cycle 正在编辑的同一份 SOT 也带该错文案**)。
4. **[缺陷, 中]** 既有 ~140 条 pattern 的尾边界缺失 (`nomad var get` 误配 `nomad var getty` 类) 与 FP 面 (读 `--help`、grep 文本、commit message、写文档时引用命令文本 被拦)。**severity 由「低」升「中」** (R4 tech-lead r4-m-5): 单 session 内实证命中**四次**, 标低会让它长期排不上。
5. **[增强, 低]** BLOCKED 提示的 per-pattern 条件建议 (`$pattern_hint`) — 须先解决 `set -u` 下的缺省初始化 (R2 backend M-1 实测: 未初始化会让**全部** BLOCKED 文案崩成 unbound variable)。
6. **[知识层, 中]** (R1 tech-lead M-4(b), R3 指出前一版被静默丢弃) `standards/conventions/` 缺一条**通用** convention: 「CLI 工具的默认输出格式可能随 stdout 是否为 TTY 而变 —— AI/CI 环境 (stdout=pipe) 下的默认行为常与交互式相反」。本次的 nomad `-out` 只是该类的一个实例 (同类还有 `git --no-pager`、`docker` 的 TTY 检测等), 值得独立成条而非只在 secret-hygiene 里就事论事。

## rule6_note

**Rule #6 不适用 — 走 Rule #10 豁免白名单第四类「结构性前提不成立」** (R2 knowledge PASS 已核: 对照 `configured-gate-authority.md` §2 与 `skill-benchmark-exemption.md` 原文, 未见越界自行豁免):

Rule #6 触发面是 **Skill**, 其 SOT 四分表逐行以「Skill 内容」为主语。本变更对象 `hooks/secret-guard.sh` 是 PreToolUse harness hook — 无 SKILL.md、无 description、不参与 skill 加载或触发, AB 套件被测对象与之无交集, 属「审的对象整个未产生」。本版**未改任何提示文案** (R1 曾拟改, 现转出), 故连「hook 文案是 AI 指令面」这一唯一灰区也不复存在。跨仓核实: 本 cycle 零 SKILL.md 改动。

**substitute**: SC-1 baseline-failing 结构化测试。

## Tasks

- [x] 1.1 `secret-guard.sh` 增补 `nomad var put` pattern (带尾边界) + 设计意图注释
- [x] 1.2 测试族 19 条 hook 断言 + SC-7 SOT grep 断言 — **baseline 已验**: 未加 pattern 时恰 7 条 FAIL (SC-1 五条 + SC-4 commit-msg + 阳性对照), 加后全绿
- [x] 1.3 `secret-hygiene.md` **4 个推荐位** `-out=keys` 订正 + 两段反坑警示 + Version 1.1.0→1.1.1 (standards 子模块; **已预落地于工作树**, 见 Status 流程留痕)
- [x] 1.4 全量回归 366/366 + hooks/tests/ 全部 6 个脚本 PASS
- [x] 1.5 开 §转出 **六项** issue — aria-plugin#128/#129/#130/#131/#132 + Aria#171

## Success Criteria

- [x] SC-1 (baseline-failing, 核心): `nomad var put -in=json <path> @file` / `nomad var put <path> KEY=<literal>` / `nomad var put -out=json <path> @f` / `nomad var put -out=table <path> @f` / `nomad var put -out=none <path> @f` **五条改前实测 exit=0, 改后 exit=2**。第五条含 `-out=none`: 本 spec **无豁免**, 故它同样被拦 — 这是刻意的保守选择, 出路是加 `>/dev/null` (SC-2)
- [x] SC-2 (既有 credit 仍生效, 改前改后均 exit=0): `nomad var put … >/dev/null` / `nomad var put … &>/dev/null` / `nomad var put -out=none … >/dev/null` / **`nomad var put p @f -o /dev/null`** (第四条, 口径经 R4 code-reviewer m-7 精确化: nomad CLI **不接受** `-o` — 实跑 `flag provided but not defined: -o` ⇒ 该形态在真实使用中不可能出现; 但 hook 侧仍放行, 因为 `secret-guard.sh:390` 的 credit 谓词是**无工具语境的裸正则**。用例锁定的是**后者**这个真实放行面。该根因与「裸扫 `-v` 会撞 `grep -v` credit」**同源** — credit 正则不看调用的是哪个工具, 归转出 2 一起修比分两次便宜)。**警示注记 (转出 2 的相邻面)**: `nomad var put -verbose … >/dev/null` 实测亦 exit=0 放行, 但 `-verbose` 的输出**按 nomad 设计走 stderr** ⇒ 该组合仍会泄漏。故 SOT `secret-hygiene.md` §3.4 的 `>/dev/null 2>&1` 全 redirect 才是完整写法; 本 spec 不在 hook 侧收口该面 (转出 2), 但已在 SOT 补警示段
- [x] SC-3 (尾边界, 改后): `nomad var putty foo` **exit=0** (非 nomad var put 调用, 不得误配)
- [x] SC-4 (FP 面**按实测**锁定 — R3 三方收敛勘正): 尾边界使「`put` 后紧跟引号」不匹配, 故 `grep -rn 'nomad var put' aria/` 与 `echo "改用 nomad var put"` **改后仍 exit=0 (放行)**; 仅 `put` 后**真有空格**的文本提及被拦, 以 `git commit -m "fix: nomad var put 回显"` **exit=2** 锁定。附阳性对照: 真执行形态 `nomad var put <path> @f` exit=2 (证明拦截确由新 pattern 产生)。
  > ⚠️ **实现约束 (R3 backend + code-reviewer 提出, R4 tech-lead 勘正论证)**: 尾边界是 SC-3 的硬约束; SC-4 前两条的 `exit=0` 是**当前字符类 `[[:space:]]` 的副产物, 非不可改变** —— 放宽字符类 (如 `([^[:alnum:]]|$)`) 可在保住 SC-3 的前提下把引号收尾的提及也拦住 (作者已实测复现: `nomad var putty` 仍 exit=0, 而 `grep -rn 'nomad var put'` 与 `echo "…"` 转为 exit=2, credit 未破)。但那会**扩大 FP 面**, 与本 spec「接受残余 FP、不扩打击面」的裁定相反, 故本 spec 选择 `[[:space:]]`。实施者不得为凑某条 FP 断言而改动该字符类; 若未来要改, 须连同转出 4 一并重评 FP 面。
  > (前一版此处写「二者不可兼得」—— 未实测的不可能性断言, 已被 R4 证伪并改写。本 cycle 同类错误第三次, 见 §审计轨迹。)
- [x] SC-5 (全量回归, **只承担「无外溢」**): `bash aria/hooks/tests/secret-guard.test.sh` 全绿 (基线 **347** 条 + 新增 **19** → 366); `secret-scan.test.sh` 等 hooks/tests/ 下其余 5 个脚本全绿。**分工声明 (R4 tech-lead r4-m-4)**: 该 347 条对本 spec 的目标行为**零鉴别力** (打 patch 前后均 347/347 — R4 实跑二次确认), 故正确性由 SC-1 (baseline-failing) 承担, SC-5 仅证明新 pattern 未外溢破坏既有判定; 不得把 SC-5 全绿当作「功能正确」的证据
- [x] SC-6 (读向不回归): `nomad var get <path>` / `nomad var list` 仍 exit=2; SOT 订正后推荐的投影写法 (`-out=json` 管道接 jq 的 `.Items` 取 keys, **与 SOT 逐字一致**) 仍 exit=0。附负向锚点: 同写法但 keys 后带方括号 → exit=2 (方括号破坏 hook 的 jq filter 识别, 实测) —— 该锚点防止 SOT 与 hook 再次分裂
- [x] SC-7 (SOT 订正**完备性 + 正确性**双向断言):
  - (a) 正向: 订正后示例的 `-out` 取值逐条在合法枚举内 (集群不可达, 只验 flag 解析层);
  - (b) **负向 (R3 code-reviewer M-2: 正向谓词测不到残留)**: 全文 grep `-out=keys` 的每一处命中都必须位于**警示语境** (即紧邻「不存在 / 不要用 / Invalid value」等否定词), 零处位于推荐语境 — 机械断言, 防订正遗漏
- [x] SC-8 (覆盖率上限 `KNOWN-LIMIT`, **锁现状非断言正确**, R4 tech-lead M-3): `nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2` **改前改后均 exit=0** —— 复合命令任一段携带 redirect 即令全段获 credit, 故第二条 put (正是 #170 的泄漏形态) 零保护。这是「一次写多个 var」的日常形态, 本 spec **已知不覆盖**, 归转出 1。用例以 `KNOWN-LIMIT` 命名: **该用例转红 = 转出 1 已收口**, 届时须同步更新而非无声漂移
