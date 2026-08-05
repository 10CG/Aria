---
verdict: REVISE
agent: tech-lead
round: R1
critical_count: 3
major_count: 6
minor_count: 5
---

# post_spec R1 — secret-guard-per-segment-evaluation (tech-lead 视角)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-per-segment-evaluation/proposal.md`
被审代码: `/home/dev/Aria/aria/hooks/secret-guard.sh` (v1.65.5) / `/home/dev/Aria/aria/hooks/tests/secret-guard.test.sh`

## 方法

所有结论均为实测, 不是推理。做法:

1. 用 collector 覆盖 `bash_case`/`read_case`/`edit_case`/`run_case` 后 source 测试文件, 拿到 shell 真实解析后的 305 条 `bash_case` 三元组 (避免截断 grep 造伪语料, 见 memory `feedback_grep_window_truncation_breeds_false_corpus_evidence`)。
2. 按 proposal §1/§2 的规则实现了一个参照分段器 (顶层 `;` `&&` `||` `&` 换行切; 管道不切; 引号/转义感知; `$( )`/反引号保护), 对每条用例做「整条喂 hook」vs「逐段喂 hook, 任一段 2 即整体 2」的对照跑, 得到端到端的翻转清单。
3. 对「保守」「不会少拦」「零覆盖」等断言逐条构造反例证伪。

参照分段器与探针脚本在 scratchpad `/tmp/claude-1000/-home-dev-Aria/b794d1d8-ace8-4691-ad8c-c62ded9713a5/scratchpad/work/`。**仓库文件零改动。**

## 数字口径复核 (逐个实测)

| proposal 的数 | 实测 | 判定 |
|---|---|---|
| 141 条 pattern | 141 | 准确 |
| 305 条 `bash_case` | 305 | 准确 |
| 366 条用例 | 347 (函数用例) + 19 (内联) = 366 | 准确, **但仅当 zsh 在场** (6 条 `zsh_case` 条件跳过; 无 zsh = 360) |
| 2 条分隔符在引号内 | 切分集分隔符在引号/转义内的 = **3** (漏 `R2-C-3: find -exec cat .env` 的 `\;`); 计入 `\|` 则 **9** | 偏低 |
| 68 含分隔符 / 52 拦 / 16 放 | 只在「口径 = `;` `&&` `\|\|` `\|`, 排除 `&` 与换行」下才复现。按 spec 自己的切分集 (含 `&`/换行) 顶层实测 = **72 / 53 / 19** | 口径与 spec 自身规则不一致 |
| 15 条纯管道 `expected=0` | 15 | 准确 |
| 1 条含真命令边界 `expected=0` | **4** (口径修正后); 端到端模拟实测 **3 条**由 0 翻 2 | **证伪, 见 C-1/C-2** |
| 「切管道会毁 15 条正确用例」 | 实测 **13** 条翻转 (`echo hello \| base64`、`tar ~/.sshconfig \| ssh host` 不受影响) | 高估 2 条 |
| `:653` = 全局开关 | 实际在 **`:663`** (`:405` / `:390` 的引用正确) | 行号错 |
| 69ms / 76ms 基线 | 本机同负载 20 次均值轮间散布 100–158ms (~50%) | 见 M-6 |

---

## Critical

### C-1 「`&` 是切分记号」与 `&>` / `>&` / `\|&` / `2>&1` 冲突 — 实测打红 2 条 `expected=0` 语料用例

§1 分段规则表把 `&` 列进「切」。`&>` 是 hook 自己在 `:386` 明确承认的 credit 形式, `&` 一切就把它从被判定命令里切走。端到端实测 (逐段喂 hook):

```
cat /opt/.env &>/dev/null                     现状 exit=0 → 逐段 exit=2   [R2-C-10 语料用例]
  段: 'cat /opt/.env'(2) | '>/dev/null'(0)
nomad var put -in=json ... @/tmp/pv.json &>/dev/null   现状 exit=0 → 逐段 exit=2  [put: &>/dev/null 语料用例]
cat /opt/.env >/dev/null 2>&1                 被切成 'cat /opt/.env >/dev/null 2>' + '1'
cat /opt/.env |& wc -c                        被切成 'cat /opt/.env |' + 'wc -c'  (管道 credit 被拆掉)
```

这不是「设计成收口后转红」, 是纯误报: 两条命令都正确地丢弃了 stdout。规则表必须把 `&` 限定为「不在 `&&` / `&>` / `>&` / `\|&` 上下文中的单独 `&`」(后台执行符), 并在 SC 里点名锁这四种邻接形态。

### C-2 迁移面「`expected=0` 只有 1 条受影响」被端到端实测证伪

全量 305 条对照跑 (逐段判定, 按 spec 规则):

```
不变 302   0->2 = 3   2->0 = 0
0->2:  R2-C-10: cat .env &>/dev/null            ← 误报 (C-1)
       put: &>/dev/null                          ← 误报 (C-1)
       put: KNOWN-LIMIT compound credit leak     ← 设计内转红 (SC-5)
```

即 Impact 表的「└ 含真命令边界 | **1** | 即 KNOWN-LIMIT — 本就设计成收口后转红」是错的: 实际 3 条翻转, 其中 2 条是回归。加上口径修正 (`&`/换行) 后, 顶层含真命令边界的 `expected=0` 用例共 4 条 (还有 `#152 FP: multiline benign` = `echo begin\necho done`, 该条恰好两段都不命中所以不翻)。

连带影响: SC-3 的「52 条」是同一错口径下的数, 应改为按 spec 切分集重数 (顶层 53 条 `expected=2`), 且像 SC-2 那样**逐条列名**而非只报总数。

### C-3 「子 shell / 反引号 / heredoc 保守不切 = 可能多拦, 不会少拦」方向标反了; 且与 Tasks 1.1 自相矛盾

**证伪实测**:

```
x=`cat /opt/.env; true >/dev/null`
   不切 (spec 的决定)  → exit=0   ← credit 泄漏原样保留
   盲切               → exit=2
```

「不切」把更多文本留在同一段里, 既提高了命中 pattern 的概率, **也同样提高了段内出现 credit 串的概率** —— 而 credit 恰恰是本 spec 要根治的东西。所以「不切」相对「切」是**少拦**, 不是多拦。正确表述应是「不切 = 维持现状 (子 shell 内部的 credit 泄漏不在本 spec 收口范围)」, 这是一个范围让渡, 不是 fail-safe 论证。按现在的写法, 决策表给出的是一个错误的安全依据。

**第二处硬伤**: 该行写「本 spec **不解析**, 保守**不切**」—— 这两件事不可兼得。要做到「不在 `$( )` / 反引号 / heredoc 内部切」, 分段器就必须先识别这些结构 (追踪 `$(` 嵌套深度、反引号配对、heredoc 定界符)。而 Tasks 1.1 只写了 "quote-aware + 转义感知", 没有任何 `$( )`/heredoc 追踪要求 ⇒ **按 1.1 实现出来的分段器会在 `$( )`/反引号内部切**, 与决策表的裁定相反。必须二选一并写进 1.1:
- (a) 真追踪这些结构 → 承认「子 shell 内的 credit 泄漏本 spec 不收口」, 并把它写进已知限制 + issue;
- (b) 盲切 → 更严 (上面实测), 但要重新评估 FP 面并给 SC 覆盖。

顺带: heredoc 的「语料零覆盖」不成立 —— `#157 heredoc-style nomad get` (test:603, `cat <<EOF\nsecret\nEOF\nnomad var get ...`) 的 heredoc 体内就有换行分隔符 (实测切成 4 段, 结论仍 exit=2)。SC-7 应以这条既有用例为起点而不是宣称零覆盖。

---

## Major

### M-1 逐段判定会静默关掉「跨顶层分隔符才成立」的 pattern — 这是 fail-open 方向, 且语料零覆盖

79 条 pattern 用 `[^|]*` (只挡管道, 可自由跨 `;` `&&` 换行), 另有 1 条用无界 `.*`:

```
'set[[:space:]]+-o[[:space:]]+posix.*set[[:space:]]*\|[[:space:]]*grep'   (:636)
```

实测:

```
set -o posix; set | grep foo        现状 exit=2 → 逐段 exit=0    ← 安全回归
set -o posix && set | grep buildid  现状 exit=2 → 逐段 exit=0    ← 安全回归
```

(`set -o posix; set | grep pass` 仍 2, 因为兄弟 pattern 兜住了 —— 所以语料**测不出**这个回归。)

spec 完全没有「pattern 可能跨段」这一维度。至少要: 枚举 `.*` / 跨段依赖的 pattern (目前 1 条明确 + 79 条 `[^|]*` 需逐条判是否有跨段意图), 逐条裁定改写或保留, 并加定向 SC。否则 SC-3 全绿 = 假绿 (这正是 issue 自己吐槽的「347 条对两次退化全绿」的同型陷阱)。

### M-2 组 / 循环 / 条件的整体重定向被逐段判定误伤 — 5/5 实测翻红, 语料零覆盖

§1 写「重定向的作用域 = 它所在的那个 pipeline 单元」。这个建模对复合结构是错的: `{ …; …; } >/dev/null` 的重定向作用于整个组。实测:

```
{ nomad var put p1 @f1; nomad var put p2 @f2; } >/dev/null     0 → 2
( cat /opt/.env; cat /opt/.env2 ) >/dev/null                    0 → 2
for f in a b; do nomad var put $f @x; done >/dev/null           0 → 2
if true; then cat /opt/.env; fi >/dev/null                      0 → 2
while read l; do nomad var put $l @x; done < list >/dev/null    0 → 2
```

五条都是**正确丢弃了全部 stdout 的安全写法**, 修复后全部被拦。这是 AI 与运维脚本的常见形态 (spec 自己在 Why 里说「AI 与运维脚本天然大量使用」)。语料里没有任何 `expected=0` 的组/循环用例 ⇒ SC-2/SC-3 结构上抓不到。

处置建议 (任选并写进 spec): 承认为已知限制 + 迁移写法明确指导 (把 `>/dev/null` 下沉到组内每条命令), 或对 `{ }` / `( )` / `do…done` / `then…fi` 的尾部重定向做一次「组级 credit 继承」。**不接受默认不写** —— 拦截面扩大的告知段目前只提了 `;`/`&&`, 没提这一类。

### M-3 quote-aware 的必然副作用未告知: 引号包裹的复合命令 100% 逃逸修复

引号内不切 ⇒ 一整类**日常** (非对抗性) 形态在修复后仍然 exit=0。实测 5/5:

```
ssh root@host 'cat /opt/.env; echo done >/dev/null'                       0 → 0
ssh root@host 'nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2'      0 → 0
bash -c 'cat /opt/.env; echo x >/dev/null'                                 0 → 0
sh -c "cat /opt/.env; true >/dev/null"                                     0 → 0
docker exec c sh -c 'cat /run/secrets/db; echo ok >/dev/null'              0 → 0
对照 cat /opt/.env; echo done >/dev/null                                    0 → 2
```

注意第二行: 那正是 #170 的泄漏形态本身, 只是加了 `ssh host '…'` 外壳。hook 的 threat model 说「对抗性 quoting 出范围」, 但 `ssh host '…'` / `sh -c '…'` 不是对抗性 quoting, 是 AI 每天写的形态, 而且语料里有 10+ 条 ssh-quoted 用例。spec 必须把这条写进已知限制并给出裁定 (是否对已知 shell wrapper 递归分段 / 是否开跟进 issue), 否则「根治 #128」的声称与实际覆盖面不符。

### M-4 「管道不切」结论正确, 但论证漏掉了决定性的那半 (fail-open 证据)

我独立验证了这个决策 —— **成立, 但作者给的理由是较弱的那个**。

作者的理由「切了会毁 15 条正确用例」实测是 13 条 (FP 方向)。更硬的理由在 fail-open 方向, spec 完全没提: **12 条 pattern 把 `\|` 编码进正则本身** (`base64 -d\|bash`、`find\|xargs cat`、`\.env\|xargs`、`tar ~/.ssh\|ssh`、`set\|grep`、3 条 jq 家族、`kubectl exec env\|`…)。按 `|` 切等于把这 12 条 pattern 整体废掉。实测 4 条 `expected=2` 的真泄漏用例由 2 翻 0:

```
base64 -d | bash bypass        2 → 0
R2-C-3: find | xargs cat       2 → 0
R2-C-3: xargs cat .env         2 → 0
#69 tar .ssh piped to ssh exfil 2 → 0
```

把这条写进关键决策表, 该决策就不可再被动摇; 不写, 将来有人拿「13 条 FP 可以接受 / 可以逐条加白」重开这个决定 —— 而真正的代价是安全回归。

**关于反面 (brief 点名的 `cat .env | tee /tmp/x`)**: 我实测了。`cat /opt/.env | tee /tmp/x` 现状就 exit=2 (无 credit)。真正的洞是 `cat /opt/.env | tee /tmp/x >/dev/null` (0) 与 `cat /opt/.env >&2 | wc -c` (0) —— 即「管道内某一级的输出经文件/stderr 逃逸, 而 credit 由另一级授予」。但这是 **credit 模型 (filter 语义) 的洞, 不是分段边界的洞**: 按 `|` 切并不能修它 (`tee /tmp/x >/dev/null` 段本身仍有 credit)。所以它**不构成**「管道该切」的论据, 应记为 credit 模型的独立限制 (BLOCKED 文案里已提过 `> /tmp/x` 一半)。结论: 管道不切正确, 反面不成立。

### M-5 quote-aware 在现有语料上零鉴别力 — 缺一条可证伪的行为级 fixture

spec §2 把这一条标为「未验证项 (Phase B 必测)」—— **标注是对的, 现已核实, 推测成立**:

```
ssh find env         切错(2 段) → exits=[2, 0] → 整体仍 2   (被 'ssh[^|]*\.env\.production' 兜住)
python -c HTTP wrapper 切错(2 段) → exits=[0, 2] → 整体仍 2  (被 :405 裸 /v1/var/ 兜住)
```

后果: 整个 305 条语料对 quote-aware **零鉴别力**, SC-4 的机制断言 (断言返回单段) 是唯一防线。这不符合 Rule #6 substitute 要求的 baseline-failing 结构 (memory `feedback_deterministic_structural_skill_rule6_substitute`)。建议补一条实测可证伪的定向 fixture, 我已验证候选:

```
python3 -c 'import os; print(open("/opt/.env").read())'     整条=2, 切错=0   ← 可证伪
(对照: ssh root@host 'cd /tmp; cat /opt/.env' 与 echo 'a; cat /opt/.env' 都是巧合兜住, 不可用)
```

### M-6 SC-8 的性能闸近乎真空, 且阈值低于本机噪声

spec 自述 69ms 中约 60ms 是 bash 进程启动固定成本 ⇒ 变量部分仅约 9ms。30% 预算 = 20.7ms = 变量部分的 **2.3 倍**: 即使 pattern 匹配开销翻三倍, 这个闸照样绿。反方向, 我在本机测同一负载 20 次均值的轮间散布是 100–158ms (约 50%), 已超过 30% 阈值 ⇒ 也会假红。两个方向都不可信。

建议改法 (任选): (a) 测「扣除固定启动后的增量」; (b) 直接在 hook 内计时 pattern 循环段; (c) 给 N=1/4/16 段的曲线并断言近似线性且 16 段仍在预算内。另外把「为何手写 bash 字符扫描而非外部解析器」写进决策表 —— 实测 `python3 -c pass` = 40ms vs `bash -c 'exit 0'` = 6ms, 外置解析器一次就吃掉 SC-8 的全部预算 (对齐 memory `feedback_bash_hook_perf_subprocess_fork_dominates`)。不写下来, 将来必然有人「优化」成 `shlex`。

---

## Minor

- **m-1** `:653` 行号错 —— `if [[ $has_filter -eq 0 ]]` 实际在 `:663`。(`:405` / `:390` 引用正确。)
- **m-2** 「366 条」只在 zsh 在场时成立 (6 条 `zsh_case` 条件跳过, 无 zsh = 360)。Task 1.4「全量回归 (366 + 新增)」应写成「以 runner 报的 total 为准」, 或明确 zsh 前置。
- **m-3** `guard:ack` 维持命令级 —— 决策正确, 但 Tasks 1.2 没写明「ack 判定必须留在分段**之前**」, 且语料无「复合命令 + ack」用例。实现若把 ack 下沉到段级会静默破坏该决策 (实测: 逐段跑 `cat /opt/.env; nomad var get x  # guard:ack: <reason>` 时 ack 只落在最后一段)。建议加一条 SC 锁 `cat /opt/.env; nomad var get x  # guard:ack: <8+ 非空白>` 改后仍 exit=0。
- **m-4** Impact 写了「bump 前须 re-check 版本号」但没落成 task。对齐 #170 撞版号教训, 建议进 Tasks 1.5 或新增 1.6。
- **m-5** BLOCKED 消息要补段落定位 (SC-6) 是对的, 但没说清「段落字面是否可能自身含 secret」。触发段可能就是 `nomad var put p2 @f2` 这类含路径/参数的文本, 回显到 stderr 即进 LLM 上下文 —— 与 Rule #7 的取向有张力。建议 SC-6 补一句边界: 回显段落原文 (与现状回显整条命令同级风险, 不升级), 但不得额外回显 credit reason / 文件内容。
---

## 结论

核心方向 (逐段判定 + 管道不切) **成立且值得做**, 管道不切经独立验证正确 (且有比 spec 更硬的理由, 见 M-4)。但当前 proposal 有三处必须先改才能进 Phase B:

1. `&` 切分规则与 `&>` 冲突, 已实测打红 2 条本该放行的语料用例 (C-1);
2. 迁移面数字 (`expected=0` 受影响 = 1) 被端到端实测证伪, 口径与 spec 自身切分表不一致 (C-2);
3. 子 shell/heredoc 那一行的安全方向标反, 且「不解析 + 不切」在实现契约上不可兼得, 与 Tasks 1.1 冲突 (C-3)。

另有两类 spec 完全未建模、且语料结构上抓不到的变更面: 跨段 pattern 失效 (fail-open, M-1) 与组/循环整体重定向误伤 (fail-close, M-2)。这两类如果不在 spec 里裁定, Phase B 的 SC-2/SC-3 全绿将是假绿。

verdict: **REVISE**
