---
reviewer: aria:code-reviewer (independent third party, read-only)
scope: "aria 400f0bc..0ba4cb0 (hooks/secret-guard.sh + hooks/tests/secret-guard.test.sh) + standards faaede2..HEAD (conventions/secret-hygiene.md)"
spec: openspec/changes/secret-guard-manifest-precision/proposal.md (What.1/1b/2/3 + SC-1..7 + Amendment-1) + detailed-tasks.yaml
verdict: PASS_WITH_WARNINGS   # 首审 REVISE (C-1/I-1..3/M-1..4) → 复核 496dd69: C-1 I-1 I-2 M-1..4 闭合; I-3 (SC-8) 由主 loop 另行低负载单跑, 不在复核范围
critical: 0
important: 1   # I-3 SC-8 待单跑数据
minor: 0
pre_existing_advisory: 2
review_rounds: 2
rechecked_sha: 496dd69 (aria) / b1e6d63 (主仓 Amendment-2)
timestamp: 2026-08-22T07:40Z (首审) / 2026-08-22T08:05Z (复核)
---

# Phase B review — #179 secret-guard-manifest-precision

## Phase 1: 规范合规

**判定: FAIL (一条阻塞) — 但不是「计划没做」, 而是 TASK-010 的白名单套用在一行上反向制造了漏报回归, 违反 SC-6 (零回归) 与 proposal What.4「前置字符类不得放走 `/` 前缀的真路径」。**

检查清单:
- 文件路径: 与 INV-2 一致 (两 hook 文件 + secret-hygiene.md), 无越界文件。
- What.1: claude-config 行 (12 reader + `jq`) 落 :805; `:785/:786` python3/node 源组扩展落 :890-891; 源名组抽成 `$_SG_CLAUDE_CFG` 单点 (TASK-004 notes 满足)。
- What.1b: `_sg_compute_credit` :399-402 对 `$seg` 重匹配 `$_SG_CLAUDE_CFG`, 不依赖 pattern 命中通道; gated 分支 = jq `{` (:426) / grep 锚 (:436) / grep -v (:439) / sed (:442) / cut (:446) / awk `$N` (:450) / awk `/re/` (:453) = 恰 7 条, 与 spec 枚举一致。未 gate: keys/length/paths (:421) / `>/dev/null` 三行 (:462-470) / `wc -[clw]` (:472) / sha*/md5sum (:475) = 四类允许 credit 原样。
- What.2: :635 正则尾部 +3 分支, `$` 锚与同构 sibling 一致。
- What.3 + Amendment-1: 两族变量落 :377-378, **但实展开多了 `~`** (见 Important-1); 14 行改写 = 13 既有 + 1 新增, 与 TASK-007 枚举档一致; 枚举档「明确不动」的行 (:714/:715 `/`-根, :721.. token 起始, find/xargs, 重定向, ssh/kubectl 远程) 实测未动。
- 文档: secret-hygiene.md 三处 558→591 / 552→585 计数 + §2 新增一行; hook 头注释 History + Coverage gaps 三类; 执笔 commit 0ba4cb0 标 knowledge-manager (SC-7 换人形式满足)。

### 阻塞问题 (Blocking)

**C-1. 白名单套到 `/`-根敏感名上, 重开 key-file 行漏报 (基线拦、现在放)**
- 文件: `aria/hooks/secret-guard.sh:791` (原 :700 行, `(cat|head|...|base64)[[:space:]]+([^|]*${_SG_PP_SUFFIX})?(id_rsa|...|/\.aws/(credentials|config)|/\.kube/config|/kubeconfig|/\.docker/config\.json)`)
- 实测 (基线 400f0bc → HEAD):
  - `cat ${HOME}/.aws/credentials` 2 → **0**
  - `cat "${HOME}/.kube/config"` 2 → **0**
  - `cat ${HOME}/.docker/config.json` 2 → **0**
  - `cat $(echo ~)/.aws/credentials` 2 → **0**
  - 同类 `cat ${PREFIX}/etc/profile` (shell-rc 行 :800) 2 → 0 (形态罕见, 顺带)
- 根因: 这几个敏感名本身以 `/` 起头, 「敏感名前一字符」是路径前缀的**最后一字符** (`}` / `)` / 任意目录名字符), 不是 What.3 设想的 basename 前缀。TASK-007 枚举档自己写了 `/`-根 token「自锚, 不适用」, 只对 :714/:715 **整行**排除, 没看到 :700 行**内部**也有 5 个 `/`-根名。实现者碰到 `~/.aws/credentials` 时给两族补了 `~` (Amendment-1 没有) 把这一个症状压下去, `}` `)` 没补 → 露出来。SC-5 守卫全是 basename 形态, 对此盲; 套件 591/591 全绿是假绿。
- 为什么重要: `${HOME}/.aws/credentials` 是 Claude 会自然写出的形态 (非对抗), 属 key-file 真泄露面; 这是 #179 从「修漏报」变成「新造漏报」。
- 修法 (已在 scratch 副本验证, 8/8 回到基线行为, `cat prod.env` / `cat x.key` / `id_rsa` 守卫不变): 把 `/`-根名从白名单组里拆出, 走原来的无白名单 `[^|]*`:
  ```
  "(cat|...|base64)[[:space:]]+(([^|]*${_SG_PP_SUFFIX})?(id_rsa|id_ed25519|id_ecdsa|\.ssh/id_[A-Za-z0-9_]+|\.pem|\.key|\.p12|\.pfx|\.jks|\.gpg|\.age|\.tfstate)|[^|]*(/\.aws/(credentials|config)|/\.kube/config|/kubeconfig|/\.docker/config\.json))(\b|/|$|[[:space:]])"
  ```
  shell-rc 行 :800/:801 的 `/etc/environment|/etc/profile` 同法拆出 (一致性)。拆出后两族的 `~` 成员失去存在理由, 可回到 Amendment-1 原字面 (见 Important-1)。**并补 SC-5 守卫 ≥3 条**: `cat ${HOME}/.aws/credentials` / `cat "${HOME}/.kube/config"` / `cat $(pwd)/.docker/config.json` want=2 (反事实: 当前 HEAD 三条必红)。

## Phase 2: 代码质量 (在 C-1 之外的评估)

### 优点
- 收紧模式机制干净: 单变量 `tight` + 7 处 `[[ $tight -eq 0 ]] &&` 前缀, 分支零改动, 一眼可审; 源名组单点定义两处消费 (:363 / :399 / :805 / :890-891) 确实防了漂移。
- 可选组形态 `([^|]*PP)?` 解 A1-M2 争用很巧: `cat .bashrc` 靠强制空白独立成立, 不与白名单串联; 实测 `cat .bashrc` / `cat ~/.bashrc` / heredoc 中段 / `cat "$HOME/.bashrc"` 全拦。
- SC-4 fixture v2 有反事实纪律 (commit cbb96af 明确换掉两条基线恒绿形态), SC-3 留 46a374f 中间态 SHA 引用。
- ACK 成对块: 备份 → 设置 → 两探针 → 删 marker → 还原, 顺序正确; marker 路径 `${USER:-anon}` 与 hook :651 一致。

### Important (应修)

**I-1. 白名单字符集与 Amendment-1 不一致 (`~`), 且 proposal What.3 明文说 `~` 不入白名单**
- 文件: `secret-guard.sh:377-378`; 实展开 `NAME=(^|[[:space:]"'=/~])`, `SUFFIX=(^|[[:space:]"'=/~*A-Za-z0-9_.-])`; Amendment-1 原文两族均无 `~`。
- 问题: 添加理由 (hook 注释 :374-375「`/` 起头的名前面合法出现 `~`」) 正是 C-1 同一根因的症状补丁; proposal 无 Amendment-2 记录, 与 What.3「`~` 结构性不可达」的论断直接矛盾却未勘正。
- 修法: 按 C-1 拆行后去掉 `~`, 回到 Amendment-1 字面; 或若保留, 追加 Amendment-2 写明 What.3 的「不可达」论断在 `/`-根名上不成立。两者选一, 不能文档说 A 代码做 B。

**I-2. 新名组对 `./` / `//` 路径变体双平面逃逸**
- 文件: `secret-guard.sh:363` (`$_SG_CLAUDE_CFG`) + `:635` (Read 面三分支)
- 实测: `cat ~/.claude/./settings.json` → 0, `cat ~/.claude//settings.json` → 0; Read `$HOME/.claude/./settings.json` → 0, `$HOME/.claude//settings.json` → 0。
- 为什么重要: 既有 sibling (`id_rsa`, `.env`, `.bashrc`) 的识别靠 basename, 目录插 `./` 不影响; claude-config 三条目里两条**完全依赖 `.claude/` + basename 的组合**, `settings.json` 裸名太泛不能单独入清单, 所以这个变体是本 spec 新名组独有的结构弱点, 不是既有清单的同构限制 (头注释 gap (c) 没覆盖它)。成本极低。
- 修法: `_SG_CLAUDE_CFG='\.claude/+(\./+)*settings\.json|\.claude/+(\./+)*settings\.local\.json|\.claude\.json'`; Read 面同样 `/\.claude/+(\./+)*settings\.json$` ×2。加 2 条 SC-1/SC-2 fixture。若 owner 决定归入已知限, 须写进头注释 gap (c)。

**I-3. SC-8 tier (e) 在本次复审全量跑中 FAIL (+83.2% min), 与 21c5000 commit 声称「三点复测 +4%」冲突**
- 文件: `hooks/tests/secret-guard.test.sh:1889` 输出; 本机 load 14-22 / 4 核。
- 我做的交叉验证: 400f0bc vs HEAD 交错各 25 次取 min, tier-e 载荷, 三轮 (base/head us): 164825/149904, 258713/373285, 277675/186606 — 无一致方向, 高负载下不可判。
- 处置: 按测试文件自身 :1889 的文字和 Rule #10, 不能由实现方/复审方自判噪声; ship 前须在低负载 (load < 核数) 单独跑一次 SC-8 并把五档 min 数据落 handoff 请 owner 复议。memory `feedback_perf_regression_min_not_median_and_run_solo` 同款。注意 SC-8 比较对象是 af87cae (pre-#128) 而非 400f0bc, 所以 #179 新增的 14 条可选组正则是在既有 50% 余量上**累加**的, 这次 +58%/+83% 两次出现不宜全归噪声。

### Minor (建议)

- M-1 `secret-guard.sh:99-100` 头注释「12 pre-existing sibling rows + the 2 new claude-config rows」错: 新增行只有 1 条 (:805), python3/node 是既有行扩展; 正确是 13 + 1 (TASK-007 档自己写的就是 13+1)。
- M-2 `secret-guard.test.sh:1961` SC-4「issue 复现」fixture 双引号转义后实际命令是 `grep -oE '\(\\.bashrc\|[^)]*\)' ...`, 敏感名前一字符是 `\` 不是 issue 原形的 `(`; 它实质是「前缀 \」的重复, `(` 形态靠下一条变体撑着。建议改成单引号写法还原 issue 原文 `grep -oE '(\.bashrc|[^)]*)' hooks/secret-guard.sh` (我实测 → 0, 基线 2, 反事实成立)。
- M-3 `secret-guard.test.sh:1939-1940` ACK 还原用 `-n` 判定: 原环境变量「已设但为空」会被还原成 unset; 对本套件无影响, 如要精确可用 `${VAR+x}` 判存在性。
- M-4 `secret-guard.sh:890-891` `node -e` 扩了源组但 `node -p` / `python3 -` (stdin 脚本) 不在面内, 与既有 `.env` 条目同构限制; 可并入头注释 gap (c) 一句。

### 预先存在, 不计入本次 (advisory, 建议开 issue)

- P-1 credit 是「段内任一管道级命中即给整段 credit」, 不看数据流顺序: `cat ~/.claude/settings.json | tee /dev/stderr | jq 'keys'` → 0 (stderr 进 Claude 上下文); `... | jq -r '.env|to_entries[]|"\(.key)=\(.value)"' | jq keys` → 0 (第二个 jq 对字符串输入报错时**把输入值打进 stderr 错误信息**)。收紧模式封闭枚举的四类 credit 本身没问题, 但 credit 的「位置无关」语义让它在 claude-config 上也只是「紧到 credit 机制允许的程度」。`.env` 面同样逃逸, 属 #138 同类架构面, 不是 #179 引入。
- P-2 `jq '.env' f | tee /tmp/o.txt >/dev/null` → 0 (落盘后 Read 非清单路径); 既有 `> file` 路径同款, 文档 NOT-acceptable 列表已知。

## 探针表 (我实跑; `jq -n | bash <hook>`; 命令文本不执行)

| # | 命令 | 基线 400f0bc | HEAD | 判定 |
|---|---|---|---|---|
| 1 | `jq -c '{model, env: (.env // {})}' ~/.claude/settings.json` | 0 | 2 | SC-1 OK |
| 2 | `cat ~/.claude/settings.json` / `cat ~/.claude.json` / `cat ~/.claude/settings.local.json` | 0 | 2 | SC-1 OK |
| 3 | `jq -r '.env' ~/.claude/settings.json` / `jq '.env' < ~/.claude/settings.json` / `jq . .claude/settings.json` / `jq -n 'input' ~/...` | 0 | 2 | 绕过失败 (jq 参数变体全拦) |
| 4 | `cat "$HOME/.claude/settings.json"` / `cat ${HOME}/.claude/settings.json` | 0 | 2 | 路径变体拦 (`/` 前缀) |
| 5 | `python3 -c '...open("/home/x/.claude.json")...'` | 0 | 2 | :785 扩展 OK |
| 6 | `cat ~/.claude/settings.json \| jq '{env: .env}'` | 0 | 2 | SC-3 核心 OK |
| 7 | `... \| grep -v zzz` / `\| grep '^  "model"'` / `\| cut -d: -f1` / `\| sed 's/x/y/'` / `\| awk '{print $1}'` | 0 | 2 | 行级 credit 全 gated |
| 8 | `... \| jq 'keys'` / `\| jq 'keys' \| jq .` / `\| wc -c` / `\| sha256sum` / `>/dev/null` / `\| jq length` / `\| jq '.env \| keys'` | 0 | 0 | 四类允许 credit 放行 (keys 只出键名) |
| 9 | `cat ~/.env ~/.claude/settings.json \| jq '{env: .env}'` | 0 | 2 | 混合源恒收紧 OK |
| 10 | `cat ~/.env \| jq '{a: .a}'` | 0 | 0 | 对照组不变 OK |
| 11 | `head -1 ~/.claude/settings.json \| base64` | 0 | 2 | 绕过失败 |
| 12 | `cat ~/.claude/./settings.json` / `cat ~/.claude//settings.json` | 0 | **0** | **逃逸 (I-2)** |
| 13 | Read `$HOME/.claude/./settings.json` / `//settings.json` | 0 | **0** | **逃逸 (I-2)** |
| 14 | `cat ~/.claude/settings.json \| tee /dev/stderr \| jq 'keys'` | 0 | **0** | 逃逸, 预先存在 (P-1) |
| 15 | `... \| jq -r '.env\|to_entries[]\|"\(.key)=\(.value)"' \| jq keys` | 0 | **0** | 逃逸, 预先存在 (P-1) |
| 16 | `node -p "require(...'/.claude/settings.json').env"` | 0 | 0 | 已知限同构 (M-4) |
| 17 | `cat ~/.claude/settings.jso*` / `cd ~/.claude && cat settings.json` | 0 | 0 | 头注释 gap (c) 已申报 |
| 18 | `grep -oE '(\.bashrc\|[^)]*)' hooks/secret-guard.sh` | 2 | 0 | SC-4 issue 原形 OK |
| 19 | heredoc 内 `pattern: (\.bashrc\|\.zshrc)` | 2 | 0 | SC-4 多行 OK |
| 20 | `cat ~/.bashrc` / `cat .bashrc` / `grep X ~/.zshrc` / `sed -n 1p /etc/profile` / `cat "$HOME/.bashrc"` / 多行中段 `cat ~/.bashrc` | 2 | 2 | SC-5 OK |
| 21 | `cat prod.env` / `find . -name '*.env' -exec cat {} \;` | 2 | 2 | Amendment-1 守卫 OK |
| 22 | `cat ${HOME}/.aws/credentials` | 2 | **0** | **回归 (C-1)** |
| 23 | `cat "${HOME}/.kube/config"` | 2 | **0** | **回归 (C-1)** |
| 24 | `cat ${HOME}/.docker/config.json` | 2 | **0** | **回归 (C-1)** |
| 25 | `cat $(echo ~)/.aws/credentials` | 2 | **0** | **回归 (C-1)** |
| 26 | `cat ${PREFIX}/etc/profile` | 2 | 0 | 回归 (C-1 同类, 形态罕见) |
| 27 | `cat ~/.aws/credentials` / `cat $HOME/.aws/credentials` / `cat ${HOME}/.ssh/id_rsa` / `cat ${HOME}/.bashrc` | 2 | 2 | 未回归 (`~` / `E` / `/` 前缀在集内) |
| 28 | `ssh host cat ~/.bashrc` / `ssh host 'cat .bashrc'` / `ssh host cat ${HOME}/.bashrc` | 2 | 2 | :801 结构 OK |
| 29 | `awk '{print}' .env` / `awk -F= '{print $1}' ~/.env` / `perl -ne 'print' .env` / `python3 -c 'open(".env")'` / `node -e '...(".env")'` | 2 | 2 | 后缀族各行 OK |
| 30 | scratch 副本套 C-1 修法: #22-25 | — | 2 | 修法验证通过, #21/#27 不变 |

全量套件 (HEAD, load≈15): 590/591, 唯一 FAIL = SC-8 tier (e) (I-3)。

## Phase 2 专项核对

- 正则可移植性: 新增构造仅 `(^|[...])` 括号组 + `?` 可选组, 全是 POSIX ERE; `\b` 仅沿用既有位置, 无新增。
- 双引号数组转义: 实展开 (见 I-1 引文) 与意图一致; `\.` / `\b` / `$|` 在双引号内未被 bash 吃掉 (`$` 后跟 `|` 不触发展开)。
- 注释与实现: :399-402 注释与 7 gated 分支一致; 头注释 (3) 段 `~` 描述与代码一致但与 spec 不一致 (I-1); 行数 12+2 错 (M-1)。
- ACK 块环境还原: 正确 (M-3 仅边缘)。

## 评估

**是否可以继续**: 否, 需要修复 C-1 (+ 配套 SC-5 守卫) 后重审; I-1/I-2 建议同批处理 (都在同两行上), I-3 在 ship 前解决。
**理由**: 漏报修复主体 (双平面清单 + 收紧模式) 实现正确且抗住了 10 余种 jq/管道绕过; 但误报收敛那一刀切到了 key-file 行内的 `/`-根名, 把 `${HOME}/.aws/credentials` 这类自然形态从「拦」变成「放」, 恰是 spec What.4 点名不许发生的方向, 而套件全绿没抓到 (守卫集只有 basename 形态)。

## 复核 (496dd69)

对 aria `496dd69` 重跑首审探针表全部 30 组 (+ C-1 修法验证 9 条 + 协调方点名 3 条 + 我加 3 条), `jq -n | bash hooks/secret-guard.sh`, 基线列仍为 400f0bc。

**闭合核实**:

| 项 | 探针 | 基线 | 首审 HEAD | 496dd69 | 状态 |
|---|---|---|---|---|---|
| C-1 | `cat ${HOME}/.aws/credentials` | 2 | 0 | **2** | 闭合 |
| C-1 | `cat "${HOME}/.kube/config"` | 2 | 0 | **2** | 闭合 |
| C-1 | `cat ${HOME}/.docker/config.json` | 2 | 0 | **2** | 闭合 |
| C-1 | `cat $(echo ~)/.aws/credentials` | 2 | 0 | **2** | 闭合 |
| C-1 | `cat ${PREFIX}/etc/profile` (shell-rc 行) | 2 | 0 | **2** | 闭合 |
| C-1 | `ssh h cat ${HOME}/etc/profile` (ssh 行 `/`-根分支) | 2 | 2 | 2 | 守卫不变 |
| C-1 守卫 | `cat ~/.aws/credentials` / `$HOME/...` / `${HOME}/.ssh/id_rsa` / `${HOME}/.bashrc` / `cat prod.env` / `cat x.key` | 2 | 2 | 2 | 无副作用 |
| I-1 | 实展开 `NAME=(^|[[:space:]"'=/])` `SUFFIX=(^|[[:space:]"'=/*A-Za-z0-9_.-])` | — | 含 `~` | **与 Amendment-1 逐字符一致** | 闭合 (主仓 b1e6d63 Amendment-2 记录 `/`-根名分支) |
| I-2 Bash | `cat ~/.claude/./settings.json` / `cat ~/.claude//settings.json` / `cat ~/.claude/.//settings.json` / `cat ~/.claude/./settings.local.json` | 0 | 0 | **2** | 闭合 |
| I-2 Read | `$HOME/.claude/./settings.json` / `//settings.json` / `./settings.local.json` | 0 | 0 | **2** | 闭合 (:546 同步) |
| 点名 | `cat ${HOME}/.claude/settings.json` | 0 | 2 | 2 | OK |
| 点名 | `cat "$D"/etc/profile` | 2 | 2 | 2 | OK (`/`-根分支) |
| SC-4 | issue 原形 / heredoc 字面量 / `grep -E 'foo\|\.env'` | 2/2/0 | 0 | 0 | 误报收敛未回退 |
| SC-5 | 全部 8 条 + 多行中段 | 2 | 2 | 2 | 未回退 |
| SC-3 | jq `{` / 行级 5 种 / 混合源 → 2; keys / wc / sha / `>/dev/null` / `.env` 对照 → 0 | — | 同 | 同 | 收紧模式未受影响 |
| 绕过 | `head -1 … \| base64` / jq 参数 4 变体 / `$HOME` 引号变体 | 0 | 2 | 2 | 仍拦 |

**Minor 核实**: M-1 头注释改 13+1 并加 `/`-根分支说明 (一致); M-2 fixture 标签改为「转义后前缀为 `\`」(如实标注, 未恢复 issue 原文 — 可接受, issue 原形在我的探针 #18 下 → 0 已独立验证); M-3 ACK 还原改 `${VAR+x}` 存在性判定 (正确); M-4 (`node -p`) 未处理, 属既有同构限, 不阻塞。

**新增守卫 7 条核对**: 4 条 `/`-根形态 + Bash `./` `//` 2 条 + Read `./` 1 条, 全部 want=2; 对 0ba4cb0 树这 7 条按首审探针表必红 (C-1 四条 / I-2 三条首审实测均 0), 反事实成立。Read `//settings.json` 未入 fixture (我实测 2, 建议补 1 条, 非阻塞)。

**附带观察 (非问题, 记录设计后果)**: `cat x.profile` 基线 2 → 现 0。这是 NAME 族的设计本意 (`x.profile` 不是 `~/.profile`, Amendment-1 表格「`x.bashrc` 不是该文件」), 属申报的「新放行」方向, 不是回归; 列出供 owner 知悉。

**未闭合项**: 仅 I-3 (SC-8 tier (e) 需低负载单跑数据), 按协调方说明由主 loop 另行处理并记 handoff, 不在本复核范围。P-1/P-2 为预先存在 credit 位置无关弱点, 建议另开 issue (#138 同面)。

**复核判定**: PASS_WITH_WARNINGS — 代码面可进 Phase C; ship 前置条件 = I-3 单跑数据落 handoff + TASK-000 owner 门。
