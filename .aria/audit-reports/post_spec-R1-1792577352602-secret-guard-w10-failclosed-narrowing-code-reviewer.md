---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-21T11:08:55.127Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — code-reviewer 席（规格↔代码一致性 / 执笔歧义）

基线 aria v1.76.1 (59e333c)。所有实验脚本在
`/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217audit/code-reviewer/`
(expA/expB/expC/expD.sh)。本机只有 bash 5.2.15，无 bash 3.2 —— 凡涉及 3.2 的结论标「未核实」。

## 审计结论

### C1 — Critical / implementation+architecture / What.3 (D) + 不变量(:98) + 姿态 D(:110)

**item 3 的「被引用」判据 (`$NAME` 或 `${NAME}` 子串) 漏掉了 bash 的其它展开形式，导致一条读凭据的命令从「基线拦」翻成「新版放行」——一条规格自己否认的新 fail-open。**

- 判据只认子串 `$NAME` 和 `${NAME}`（proposal:75，且 :83 确认用子串匹配）。但 bash 还能经
  `${NAME:-x}` / `${NAME#...}` / `${NAME%...}` / `${NAME/a/b}` / `${!NAME}` / `${NAME[@]}` /
  `$((NAME))` 等形式展开同一个变量——这些文本里**既不含 `$NAME` 也不含 `${NAME}` 子串**。
- 实测 (expA)：`_sg_vx_apply` 对 `cat ${F:-fallback}` 返回 rc=1、`_SG_SUB` 原样不变（对照
  `cat ${F}` rc=0 正常代入）。即 W10 代入引擎从不展开 `${F:-x}`。
- 端到端 (expA，基线 hook)：
  - `F=/etc/forgejo/app.ini; cat ${F:-x}`（小值）→ **exit 0**（基线对此形式本就 fail-open）
  - `F=/<4100 chars>/etc/forgejo/app.ini; cat ${F:-x}`（值 >4096，唯一引用是 `${F:-x}`）→ **exit 2**（基线按 VMAX 拦）
- 按 item 3：值 >VMAX → 查 `$F`/`${F}` 子串 → `cat ${F:-x}` 两者都不含 → 判「未引用」→ 丢弃该值 →
  对 `cat ${F:-x}` 字面判定 → 无 risky 命中 → **放行 (exit 0)**。运行时 `cat ${F:-x}` 读 `/etc/.../app.ini`。
  ⇒ 同一输入 **基线 exit 2 → 新版 exit 0，且确实读凭据配置**。直接命中 BRIEF 的反例判据。
- 这推翻姿态 D 的立论「未被引用的超大值…**不参与任何代入**」(:110)：它参与运行时代入，只是 W10 没代入/没扫到。
  也违反 :98「不新增 fail-open 路径」的字面。
- **缓解背景（供定级参考）**：W10 从不展开 `${NAME:-x}` 形式，故小值下 (≤4096) 这条 fail-open **基线已存在**；
  本改动是把它的边界从 ≤4096 扩到无上限，不是全新泄漏「类」。但「块→放行且读凭据」的回归由本改动引入，
  按 BRIEF 严重度表（新 fail-open）记 **Critical**；若 owner 认为 D 的边界扩张可接受，可降级——这是事实项，照报。
- **改法（低成本）**：引用判据改为开括号 `${NAME`（任意后续字符）**加** `$NAME` 子串；这样 `${NAME:-x}`、
  `${NAME#..}`、`${NAME[@]}` 等一律计为「被引用」→ 继续拦（偏严、fail-closed，与 :83 的偏严方向一致）。
  并补一条 SC：值 >4096 且**仅**经 `${F:-x}` 引用 → 新版仍拦（当前 SC-6 只测「真未引用」与「`$f` 明引用」，覆盖不到本形状）。

### M1 — Major / architecture+testing / Why(:41-44) + What.2(:62) + SC-4(:121)

**「credit 平方级成本只跟单行长度有关、不跟总长」(:43) 以及「最长行 ≤ 8192 ⇒ 逐行 credit 成本有上界」(:62) 与实测不符；分流只按最长行，漏了行数(总长)维度。**

- 实测 `_sg_compute_credit`（expB/expC，taskset 2 核 nice 19）：
  - 40 KB 全短行（每行 ≤5 字符，约 6667 行，benign）= **6.49 s**；20 KB=1.71 s；10 KB=0.88 s（随行数近线性/超线性）。
  - 同为 8192 字节：单条长行 = **1.25 s**，拆成短行 = **2.11 s** ⇒ 相同字节下短行**更贵**。
  - 机制：`_sg_compute_credit` 对约 13 个过滤器各调一次 `_sg_line_match`，每次 `while read` 遍历**每一行**跑一次正则；
    成本 ≈ 过滤器数 × 行数 + Σ(行长²)。bound 单行长度只压住了 Σ(行长²) 项，没压 ×行数 项。
- `:476` tight 检测（唯一整段匹配）本身**不是**成本来源：expB 实测 40 KB 多行 PROCTAB 匹配仅 0.007 s，
  且不跨 `\n` 匹配（见 m4）。所以 :43 括号里为 :476 做的辩护结论没错，但 Why 对 credit 整体的归因错了。
- 实际是否可被做成 >5 s 的二遍 fail-open：本机(快/Linux)**未核实到**干净反例——`_SGV_GMAX` 把副本压到
  `${#S}+8192`，而 S 一大首遍就慢、`SECONDS*2>=budget` 的时间护栏 B 会在二遍前拦。但：
  (a) 规格**没有**用「GMAX+护栏 B」论证安全，只用了那条错误的单行论据；安全结论即便成立也是靠未申报的交互；
  (b) 余量薄且依机器而变：hook 注释自承 Windows ~2.6×，40 KB→~17 s，护栏 B 为 1 s 粒度、公式 `SECONDS*2>=budget`
      在慢机上可能首遍 1 s 放行、二遍再叠加后逼近/越过 CC 5 s；
  (c) **缺 SC**：SC-4 只测「超长单行」一支，没有「最长行 ≤8192 但总长大/行数多」的 big-copy credit 支，
      区分不了好实现与「按最长行放行却在行数上爆炸」的坏实现。
- **改法**：(1) 修正 Why/What.2 的成本论述（credit 随行数×过滤器增长）；(2) big-copy 的 credit 支除了限最长行，
  还应限**总长/行数**（或在 `_sg_judge_one` 中途加一次时间检查），把「不计 credit」支的触发从「有 >8192 的行」
  扩成「最长行 >8192 **或** 总长超过某界」；(3) 补多短行 big-copy 的定向 SC（时间有界 + 路由正确）。

### M2 — Major / implementation / What.1(:50,:53) vs What.5(:92)

**item 1 把 `_sg_vx_apply` 全局改成「增长 >GMAX 即返回 2」，但 item 5 要 W9 扩展的整串检查「维持原口径(副本总长 >SMAX 即拦)」；二者用的是同一个 `_sg_vx_apply`，不能同时成立。**

- `_sg_per_segment_eval:1554` 对**整条命令**调 `_sg_vx_apply "$cmd"`，并在 `ar==2` 时（:1562）发
  "the command is longer than $_SGV_SMAX characters … too large for the project extension" 并 return 2。
  这正是 item 5 说的 :1563「副本总长 >SMAX 即拦」的宿主。
- item 1 (:50/:53) 明确「`_sg_vx_apply` 返回 2 的条件从 总长>SMAX 改为 ${#S}+GMAX」「整串/分段同一口径」，是对该函数的**全局**改写。
- 后果：改完之后，一条**原命令本就很大(总长>SMAX)但展开增长很小**的整串命令，`_sg_vx_apply` 不再返回 2（增长没超 GMAX）
  → 走 :1556 的 `ar==0` 分支 → 对 >SMAX 的 `_SG_SUB` 跑 `_sg_ext_pass`→`_sg_core_eval`（含 O(n²) 首遍）——
  这恰是 item 5「长副本确实贵，所以拦」要避免的昂贵路径。于是 item 5 的「维持原口径」**在当前描述下无法达成**。
- 对执笔席是直接矛盾：同一个函数不能对 W10 二遍返回「增长判的 2」又对扩展返回「总长判的 2」。
- 仅影响启用了 `.aria/secret-guard.paths` 的项目（proposal 称本机 0 个），但属正确性/潜在超时项，不是纯文档。
- **改法**：若要「维持原口径」，需在扩展看 `_SG_SUB` 前**另加**一条独立的 `(( ${#_SG_SUB} > _SGV_SMAX ))`（扩展在用时才拦）
  的尺寸门，并在 proposal 里点明「apply 的 ar==2 语义已变，扩展不再复用它判尺寸」；否则 item 5 的承诺落空。
  同时 SC-8(:129) 只测「整串 >8192 且引用变量」的**高增长**例，没有「大原串/小增长 + 扩展启用」的例，建议补。

### m1 — Minor / implementation / What.3(:75)

「去掉这条赋值本身」语义不清：去掉 LHS `NAME=`、还是整条 `NAME=value`、还是直接在原始 `$1` 里搜？
`_sg_vx_collect` 在 VMAX 检查点 (:645) 的循环态里，`rest` 已前移过本次 `$m`，重建「命令减去本赋值」不便；
执笔席多半会直接搜原始 `$1`，此时被丢弃的大值若**自引用** `$NAME` 会被算作「被引用」(偏严、可接受) ——
两种实现都安全但行为不同，规格该钉死「在原始命令文本上搜、LHS 无 `$` 天然不自命中、被丢值的自引用是否计入」。

### m2 — Minor / testing / What.2(:59) + SC-5(:123)

SC-5 预设有「时间护栏 helper」可设 `SECONDS=k` 单测，但 item 1(:59) 把护栏写成 `_sg_vx_pass` 内联
`(( SECONDS * 2 >= _SG_TIME_BUDGET ))`。要让 SC-5 成为干净的进程内单测，需把它抽成具名 helper（且置于源码闸门之上，
进 SC-30b 闭包）。另：该护栏读**绝对** `SECONDS`（进程起点计；实测 hook 内无任何 `SECONDS=` 赋值，:607/:633/:1542 只赋 `_SG_T0`），
在 source 方式的套件里 `SECONDS` = 套件已跑秒数，会**误触发**时间拦。故新加的 big-copy 端到端 SC 必须走子进程（现有
W10 用例经 `wpa_err/wpa_rc` 子进程跑，天然安全），并在 proposal 明确此约束。

### m3 — Minor / implementation / What.4(:88)

item 4「字符类加入换行」有编码陷阱：bash `[[ =~ ]]` 的 ERE 里 `\n` **不**被解释为换行，必须把**字面换行字节**嵌进括号
（如 `rf=$'...([^;&|)\n]*)'`）；且只能加 `\n`，**不能**用 `[:space:]`（会连空格一起排除，破坏含空格的 for 列表）。
实测 (expD)：现 `([^;&|)]*)` 对多行 for 捕获到整个循环体+`done`；改成 `[^;&|)\n]*` 后只捕到 `a b c`。premise 与 fix 均成立，仅需钉死编码方式。

### m4 — Minor / documentation / Why(:43)

:43 括号「它的通配段不跨空白」措辞不准：`_SG_PROCTAB` 里的 `[^|;&]*` **包含**空白与换行；真正阻止跨行 **匹配** 的是其后的
`[[:blank:]]`（不含 `\n`）锚点。实测 (expB)：`ps\naux` 不匹配 PROCTAB，40 KB 单/多行匹配均 <0.03 s。结论(便宜、有界)对，理由需改。

### m5 — Minor / testing / SC-9(:130-139)

SC-9 用的 2412 条真实语料「命令原文不入库」(:8)，TRAFFIC_DIR 在仓外。故 SC-9 是**单机验收**而非可复现/CI 回归；
判据(四类迁移、尺寸拦 130→≤5、无命令新超 5 s)本身可证伪，但第三方无法复跑。与 #228 做法一致，建议在 proposal 显式标注此复现边界。

### m6 — Minor / documentation / Impact(:147)

standards `secret-hygiene.md:316` 现为「822 regression cases, 816 无 zsh」，而 `secret-guard.test.sh` 头注释当前已是
「831 cases (825 without zsh)」—— 即本改动**之前**就已陈旧 9 条。proposal 的「顺带改正」方向对；只是要回填的权威现值是
831/825（再加本次新增 SC），不是 822/816。(SC-13 以实跑 N 为权威，口径正确。)

### D1 — decision / —— / 已核对无误的代码事实（留痕）

以下 proposal 断言经核对与源码一致：SMAX 数**总长**（:694 `${#out}+${#s} > _SGV_SMAX`）；VMAX 超限立即 return 2 且不看是否被引用
（:645）；`_SG_T0` 在**首遍之后**才重置（首遍 :1539 先于重置 :1542/:633）；`SECONDS` 进程起点计、hook 不赋值；扩展检查重跑
`_sg_core_eval`（:814）；oversize/timeout 文案均为「Nothing was matched」(:836/:855)；死代码 `[[ -z "${_SGV_V[j]}" ]]`(:666)
确为恒假（存值皆非空，链式替换不会清空）——:93 的清理判断正确。真实流量 W1-W3 与 :29-35 的数字一致（137 SMAX/1 VMAX/0 for、最长行 max 4457、无 >8192）。

## Verdict

计数：**Critical = 1，Major = 2，Minor = 6**。按 ≥1C = FAIL ⇒ **FAIL**。

C1 是硬阻断（规格自我否认的新 fail-open，已机械验证块→放行且读凭据），且其对应 SC 覆盖缺失。
M1/M2 为承重设计的事实错误与规格内部矛盾，需在 Approved 前修正。改法均低成本（C1：引用判据改开括号 `${NAME`；
M2：扩展侧另加独立尺寸门；M1：修正成本论述 + 增总长/行数界 + 补多短行 SC）。

## 轮次记录

- R1 (code-reviewer, convergence)：首轮。侧重规格↔代码一致性与执笔歧义。读 proposal 全文 + 基线
  `secret-guard.sh`（W10 段 :565-760、credit :453-563、judge/per-segment :1486-1590、emit :826-900）+
  测试 SC-8/30b harness、W10 预算族 21aa-21ap、SC-T 时间预算族。4 组定向实验（见顶部路径）。
  产 1C + 2M + 6m。converged 由 reconciler 判，本席留 null。
