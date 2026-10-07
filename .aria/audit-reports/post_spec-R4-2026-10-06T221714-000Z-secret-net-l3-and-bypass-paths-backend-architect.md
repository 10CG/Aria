---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-07T00:44:10.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — backend-architect — secret-net-l3-and-bypass-paths (proposal v4, b07f69a)

> 全部实跑只在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/audit/post_spec-R4-backend-architect/` 下进行 (下称 `$A`; 脚本在 `$A/h/`)。真仓未做任何 git 写操作 (收尾核验: `git status --short` 0 行, HEAD `b07f69a`, aria `268da8f`, standards `2bc1c4c`)。像凭据的值全部在 Python 进程内用 `secrets` 运行时生成, 报告只写退出码 / tag 名 / 计数 / 耗时。

## 已实读文件

Spec 与证据:
- `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 全文 (1-443 行, 分段读完); `git diff --stat c0a6654 b07f69a` 与差异抽读。
- `baseline-evidence.md` 前 60 行 (环境 / 读法 / 输出头); `baseline_probe.py` 按需 (grep 行定位 + 分 SC 子集实跑, 未通读 2414 行)。
- 三个 issue 全文 (aria-plugin-154 / aria-plugin-203 / Aria-221); 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; R3 聚合报告全文 (全部 finding 表 + 主控记录); v4 返修报告全文 (处置表 / 同族扫描 / 改变实现者动作 / 证据复跑 / 薄弱点 / 请裁项)。

源码与规范:
- `aria/hooks/secret-scan.sh` 全文 377 行; `secret-guard.sh` 全文 1120 行; `hooks.json` 全文; `tests/secret-scan.test.sh` 1-60 行; 两个套件里 `HOME=` / `rm -rf` 用法 (grep)。
- `standards/conventions/secret-hygiene.md` 章节结构与被引行 (:23 :96 :287 :288 :319, §5.1-§5.5, 版本行 1.1.2)。
- v4 目标原型树 (writer 会话内 `exp/writer-v4/work/t4f`, 我 `cp -a` 到 `$A/t4f`; 指纹与证据一致: 原型 `secret-guard.sh` `d94ddf4d6906734f` / `secret-scan.sh` `cf2dd857823baf79`, 基线 `448b1f71a2af06d7` / `c5f53f7a164fa72e`) 与基线 hook 的全量 diff; `writer-v4-proto/README.md`、`timing.py`; `.aria/probes/plugin-cache-currency.py` 文件头。
- 本轮在原型上跑探针的行数: SC-1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16-25/26/27/28/29a-g/31 共 403 行, 全部 yes (没跑: SC-30 不执行; SC-32 四行、29h / 29i 需真 bash 3.2 全量; SC-33 只在变异体上跑)。与 writer 自报「目标态 holds」一致。

未读 (声明): R3 五份席位原文 (只读聚合); 四份研究笔记 (背景材料, 本轮结论以源码与实跑为据); `skill-benchmark-exemption.md` / `version-management.md` (Rule #6 申报与发版同步面不在我的视角, 由其它席复核)。

## Findings

### C1 · `1038b8da` · critical · issue · implementation · scope `proposal.md What.W1`

**summary**: W1 的 `tr '\000' '\n'` 使 ASCII 字符间夹 NUL 的文本 (UTF-16LE 经 Bash 输出) 的基线检出变成静默, 而 Spec 称「命中不会因此减少」, 与实跑相反, 构成安全回退。

**证据**
1. Spec 原文 `proposal.md:53`: 「不含 NUL 的内容逐字节不变, 含 NUL 的内容里没有任何字符消失 (NUL 只是变成换行), 命中不会因此减少」。基线 `secret-scan.sh:135-142` 的提取在命令替换里, bash 丢弃 NUL (5.2 在 stderr 报 `ignored null byte`), 所以 `A\0K\0I\0A\0…` 被拼回 `AKIA…`; v4 把每个 NUL 换成换行, 每个字符各占一行, 全部模式 (含与锚点无关的 provider 前缀) 一并失效。
2. 实跑 (`$A/h/t14_utf16.py`、`t14b_utf16_b32.py`; Bash 真实信封 `{stdout, stderr, interrupted, isImage, noOutputExpected}`; 内容 = `"".join(c + "\0" for c in <文本>)`):

| 内容 (UTF-16LE 形) | 基线 hook | v4 原型 |
|---|---|---|
| `aws_access_key_id = <AKIA+16>` | `aws-access-key-id=1` | silent |
| `JWT_SECRET=<b64>` 行 | `env-line-secret-keyword=1` | silent |
| `token <gh PAT 形>` | `github-pat=1` | silent |
| json `client_secret` | `json-secret-field=1` | silent |
| 同内容, 无 NUL (对照) | 同样检出 | 同样检出 |

   bash 5.2 与真 bash 3.2.57 结果相同 (基线 `aws-access-key-id=1`, 原型 silent)。
3. 探针对此无行: 我在原型上跑了 403 行 (含 SC-1 1c/1d、SC-2、SC-29a-g), 全绿 —— 没有任何一行是「ASCII 夹 NUL」的内容。「基线检出变静默」与「探针全绿」同时成立。
4. 前提与 Spec 的 1c/1d 相同 (NUL 以 `\u0000` 到达 hook)。若 harness 在到达前就去掉 NUL, 则 `tr` 是空操作, W1 对 NUL 环境的收益与这条回退同时消失; 无论哪种, Spec 现无端到端样本, Tasks 1.12 也没有 NUL 腿 (见风险 1)。

**失败场景**: 实现者照 W1 写 `| tr '\000' '\n'` → Windows Git-Bash (10CG/aria-plugin#203 的报告环境正是 MINGW64) 上 `cat` 一个 UTF-16LE 文件 (Windows PowerShell 5.1 的 `>` 重定向产物、`.reg` 导出) 且文件含凭据 → 基线告警、目标静默; 值已进模型上下文却无告警。这是「现有的检出变成放行」, 违反本审计锚点的「不引入任何安全回退」, 也违反主控 R3 裁定 10「不得为了少改而降低既有检出」(writer 的复核只核了既有测试行, 没核既有检出域)。

**怎么会红 (建议新增行)**: `reverse-guard`, Bash 真实信封内容为 UTF-16LE 形的 `aws_access_key_id = <AKIA+16>`: 基线 alert / 修正后 alert / v4 现写法 silent (红)。

**建议修法** (技术级, 任选其一):
- (a) 两视图: 视图 D = 基线行为 (NUL 被丢弃, 逐字节同基线) 保持不变; 仅当原文含 NUL 时, 把视图 N (NUL→换行) 用换行接在 D 后一并扫。我在副本 `$A/t4f-fixC` 上验证 (`$A/h/t22_fixC.py`): UTF-16LE 各形恢复为基线检出, NUL 环境 1c/1d 仍检出, 无 NUL 内容不变。代价: 含 NUL 的内容里同一 provider 前缀凭据会被两视图各计一次 (如 `aws-access-key-id=2`), 且粘连视图多出 `kv-secret-assign=1`, 所以 1c/1d 的「恰好 `env-line-secret-keyword=3`」须改成包含式期望, 或改用「D 视图无命中才扫 N」。
- (b) 退回方案 B: NUL 分隔环境列为已知限制 (主控 R3 裁定 6 允许), 不动提取链, 1c/1d 改 `known-limit`。零回退, 放弃该形态的事后检出。
- 无论选哪个: W1 设计取舍里的论据要改对 (NUL 变换会改变相邻关系), 并补上面的 `reverse-guard` 行。

### M1 · `755aab21` · major · issue · implementation · scope `proposal.md What.W2`

**summary**: W2 称 6 个新模式是线性 ERE, 但 `cli-secret-flag` 的自然写法 (及去掉左边界的 `kv-secret-assign`) 在单行长连续段上是二次方的, 8 KB 行即超过 5 s 超时使同一输出里基线可检出的凭据失检; 全部 SC 与 W14 时档 (i) 都放过这类实现。

**证据**
1. `proposal.md:59`: 「线性 ERE (`grep -E` 与 `sed -E` 通用), 不引入 perl 或回溯」; `:65` 第 6 项 `cli-secret-flag` 只写「`-` / `--` 参数名 … 以关键词结尾」, 没写左边界或前缀上界。v4 原型写成 `--?[A-Za-z0-9-]*(token|password|passwd|secret|api-key|apikey|access-key)=…` (`t4f/aria/hooks/secret-scan.sh`, 即 Spec 所验证的写法)。
2. 实跑 (`$A/h/t2_perf.py`、`t2b_scale.py`、`t2c_fix.py`; 单行, Bash 信封, 值运行时生成; 基线 hook vs 原型):
   - `'-'*n + " -token=<24 alnum>"`: n=1000 / 2000 / 4000 / 6000 / 8000 / 12000 → 原型 0.32 / 0.57 / 1.50 / 3.23 / 5.34 / 11.90 s, 基线 0.18-0.23 s; n=20000 → 32.7 s。`a-` 重复 20 KB: 19.1 s; `1a2b3c4d-` 重复 18 KB: 3.1 s。
   - 13 种对抗单行 x 6 个新模式 (`$A/h/t20_ere_battery.py`, GNU grep 3.8 单次, N=6000): 只有 `cli-secret-flag` 超线性 (2.66 s), 其余五个 ≤ 0.13 s。
   - 检出回退的直接演示 (`$A/h/t21_timeout_regress.py`): 输出 = 12000 个 `-` + ` -token=<24>` 一行, 再加一行 `aws_access_key_id = <AKIA+16>`; 用 5 s 超时模拟 harness (`hooks.json:55-60`, PostToolUse secret-scan `"timeout": 5`): 基线 0.35 s 告警 `aws-access-key-id=1`; 原型被杀, 无任何告警。
3. 同类坏实现过得了全部验收: 我自构的变异体「`kv-secret-assign` 去掉左边界 `(^|[^A-Za-z0-9_])`」(`$A/t4m-a`), 在 L3 全部行 (SC-1..13、SC-15、SC-33, 共约 190 行) 上 yes, 探针输出「target shape holds」; 但 20 KB 的 `A1` 重复行 42.9 s (原型 0.35 s), 20 KB 大写连续段 >100 s (原型 1.8 s; `$A/h/t15_mutperf.py`)。W2 对该左边界只有一句「左侧为行首或非词字符」, 探针里没有任何行钉它 (grep 无「词字符在前的键」类行)。
4. W14 时档 (i) (`proposal.md:237`) 只含两种稠密多行输入, 没有超长单行; 而 Tasks 1.8 已点名「超长单行」内容形态类。

**失败场景**: 实现者照 W2 第 6 项写自然的无界前缀 (或丢掉 kv 左边界), 全部 SC 与 (i) 档全绿; 一行含长连字符串 / 字母数字连字符串加 `-token=` 的输出 (含恶意仓库文件) 使 PostToolUse 超时 → 该输出里的全部凭据无告警。触发条件偏病态 (约 ≥ 7K 字符的高连字符密度连续段 + 同行后部的旗标形), 所以定 major; 但回退方向与 C1 同类。

**怎么会红 (建议新增)**: 1. `allow-guard`: 词字符在前的键 (如小写字母 + `JWT_SECRET` 粘连) 静默 —— 无左边界的坏实现转红 (先确认该形态按 W2 本意应静默); 2. 时档 (i'): 单行 20 KB `-` 串 + ` -token=<24>`、单行 20 KB 大写连续段 + ` X_TOKEN=<24>`, 目标 / 基线 CPU 比 ≤ 2.0, 带活性断言 (仍计 `cli-secret-flag=1` / `kv-secret-assign=1`)。三态: 基线 0.2 s (仅作分母); v4 原型 32.7 s (红); 有界写法 0.64 s、左边界写法 0.32 s (绿); 无左边界 kv 变异体 >100 s (红)。

**建议修法**: W2 第 6 项明写前缀有界 `{0,40}` 或左边界 `(^|[^A-Za-z0-9-])`; 我在副本 (`$A/t4f-fixA`、`t4f-fixB`) 验证两种写法对 7 种常见旗标 (`--token=` `-token=` `--db-password=` `--api-key=` `--client-secret=` `--access-key=` `--apikey=`) 的检出与原型一致, 8 KB 病态行分别 0.64 s / 0.32 s; 「线性 ERE」改成可检验表述并补上面两类行。

### M2 · `0a8380fd` · major · issue · implementation · scope `proposal.md What.W9`

**summary**: W9 声称扩展对同形命令的判定与内建 `app.ini` 行一致, 但扩展自写的阶段 / 尾部切分与内建分段不同: 反斜杠换行续行与 `||` 后管道被放行 (内建拦), `2>&1` / `&>` 等重定向与引号内计数管道被误拦 (内建放), 差分 324 对中 36 对相反, 而 SC-19 只钉了引号一类。

**证据** (R3 簇 T 残余; v4 只修了引号一类)
1. `proposal.md:164`: 「与内建 `app.ini` 行对同形命令的判定一致」; 阶段左切 = 最近的未被引号包住的 `| ; &` 或换行, 右切集合没写。内建分段是 `_sg_split_top` (`;` `&&` `||`, 反斜杠后一字符整体跳过; `secret-guard.sh:276-359`), 且 `_sg_safe_to_split` 把 `>&` `&>` `|&` `<&` 的 `&` 排除出分隔符 (`:242-265`); 原型扩展右切 = `[;&换行]`, 左切 = `[;&|换行]`, `\<换行>` 留作边界。
2. 扩展更松 (`$A/h/t4_ext.py`, 项目 `.aria/secret-guard.paths` 列 `/etc/myapp/secret.conf`; 对照内建 `app.ini` 同形):

| 命令形 | 内建 app.ini | 扩展条目 |
|---|---|---|
| `cat \<换行>  <路径>` | exit 2 | exit 0 |
| `sed -n '1,80p' \<换行>  <路径>` | exit 2 | exit 0 |
| `cat <路径> \|\| echo bad \| wc -l` | exit 2 | exit 0 |
| `docker exec -i web \<换行>  cat <路径>` (读取器与路径同行) | exit 2 | exit 2 |

3. 扩展更严 (`$A/h/t18_parity.py`、`t19_redir.py`): `cat <路径> 2>&1 | wc -l`、`2>&1 | sha256sum`、`&>/dev/null`、`2>&1 >/dev/null`、`1>&2 | wc -c`、`cat <路径> \<换行> | wc -l`、`bash -c 'cat <路径> | wc -l'` —— 内建 exit 0 (计数 / 哈希 / 丢弃 credit), 扩展 exit 2 (右切在 `2>&1` 的 `&` 处截断, 或掩码把引号内的 `|` 变成空格)。这些是 SOT 推荐的「只验不读」写法, 误拦会把使用者推向 `# guard:ack` (Aria#221 评论 25898 的批评)。
4. 差分总表: 6 个读取器 x 54 个命令形 = 324 对, 36 对判定相反 (6 个形状 x 6 个读取器); 其余 288 对一致, 其中含 `$( )` / 括号 / 花括号 / `if` / `for` / `while` / `ssh` / `docker exec` / `sh -c` / 重定向 / `xargs` 等。locale 与字节偏移无问题: CJK 前缀 + 引号内 `;` 在 bash 5.2 / 3.2.57 x C.UTF-8 / en_US.utf8 四组合下判定全对 (`$A/h/t5_loc.py`)。
5. SC 没钉: 探针里没有续行或含 `&` 的重定向形态的扩展行 (grep 无命中); 19z 钉 6 个引号内程序形 + 2 个引号内 `|`, 19aa 钉 8 个引号外分隔形, 19e 只有 `cat P | wc -l`; `fuzz_mask.py` 的独立 oracle 只核引号状态 (v4 报告第 5 节第 5 点)。

**失败场景**: 项目把一个服务端配置路径列进扩展 → AI 写 `sed -n '1,80p' \<换行> <路径>` (长命令续行排版很常见) 照读, 内建同形被拦、扩展放行; 反之 `cat <路径> 2>&1 | wc -l` 被误拦。扩展的存在理由是「内建名单之外的同类路径」, 现在比内建既弱又怪, 且 Spec 对外声称一致。

**怎么会红 (建议新增)**: 一行差分家族 (不逐例枚举): 对一张命令模板表 (续行 3 形、`2>&1` / `&>` / `>&` / `|&` 5 形、`||` 后管道、引号内管道、引号内 `;`, 我的 54 个模板可直接作底), 各用 `app.ini` 名与扩展条目跑一遍, 断言两侧退出码逐项相等。基线不适用 (两侧都无规则); v4 原型 36 对不等 (红); 修正后全等 (绿)。

**建议修法**: 扩展的阶段 / 尾部切分复用内建同一套 (`_sg_split_top` 分段 + 内建 `&` 判定); 最少: 把 `\<换行>` 视为空白、把 `>&` `&>` `|&` `<&` 的 `&` 排除出右切集合、右切加上 `||`; W9 把右切集合写出来 (现仅写左切); `fuzz_mask` 的 oracle 扩到这三类。

### m1 · `6f503728` · minor · issue · implementation · scope `proposal.md What.W9` (R3 ba/m2 残余)

**summary**: 纯非 ASCII 条目被静默跳过 (19ae 钉现状), 对中文环境是默认静默失效; 替代 (含任一非 ASCII 字节即有效) 只是一处条件且同样与 locale 无关, 属技术级可直接裁定。

**证据**: `proposal.md:163` 与待复议 24; 原型 `_sg_ext_entries` 的 awk 条件 `length($0) >= 4 && length($0) <= 200 && /[a-z0-9]/` (`LC_ALL=C` 下)。
**失败场景**: 采用方列入 `/srv/<汉字>/密钥` 一类条目, 无任何提示地不生效。
**建议**: 默认取备选 (`/[a-z0-9]|[\200-\377]/` 一类), 19ae 改 `baseline-failing`; 若坚持现状, README 示例点名这个陷阱。

### 实跑验证记录 (Spec 断言 -> 命令 -> 结果)

| # | Spec 断言 | 命令 / 做法 | 结果 |
|---|---|---|---|
| 1 | W1 / SC-1 1c / 1d: NUL 分隔环境经 Read / Bash 信封在基线静默、目标检出 | `$A/h/t1_nul.py`: 6 条记录各以 NUL 结尾, 基线 vs 原型 x Read / Bash x bash 5.2 / 3.2.57 | 基线 4/4 silent; 原型 4/4 `env-line-secret-keyword=3`; 变异体 `tr '\000' ' '` 使 1c / 1d 红 (2 行); **成立** |
| 2 | W1 论据「命中不会因此减少」 | `t14_utf16.py` (见 C1) | **不成立** |
| 3 | W2「线性 ERE」 | `t2*.py`, `t20_ere_battery.py`, `t21_timeout_regress.py` (见 M1) | **不成立** (`cli-secret-flag`) |
| 4 | W9「与内建 app.ini 行一致」 | `t4_ext.py`, `t18_parity.py`, `t19_redir.py` (见 M2) | **不成立** (324 对中 36 对相反) |
| 5 | W4 / SC-12: fp 第 9 字段 = sha256(裸值) 前 8 位; < 16 字符记 `L<长度>`; 值与首末 8 字符不进日志 / stdout / stderr; 缺哈希工具 `fp=-` 且日志照写 | `t13_fp.py` | 32 字符 json 值: fp 等于 sha256 前 8 位, 值 / 前 8 / 后 8 均不在任何输出; 12 字符 `L12` 且无哈希; 15 → `L15`、16 → 哈希; kv 取裸值哈希相等; 无哈希工具 `fp=-`; **成立** |
| 6 | Impact 关闭关键字三步检查: 干净 `rc=0,1`; 违规 `rc=0,0`; 跑坏 = 没跑成 | `t8_refs.sh` (scratch 仓, 非真仓) | 干净: 步骤 1 输出 `1` rc=0, 步骤 2 `rc=0,1` 且无输出; 违规: `rc=0,0` + 命中行; 错起点 `rc=128,1`; 空起点步骤 1 输出 `0`; 非仓 `rc=128`; 6 个关键字变体全命中, 6 个近邻全不命中; **成立** |
| 7 | W2 字符类 locale 无关 (SC-32 32d 前提) | `t9_locale.py` | 真 bash 3.2.57 + en_US.utf8 下 `[[ QWERTY == *[a-z]* ]]` 为 TRUE, 其余三组合 false (前提复现); 原型 L3 在 4 个 (bash, locale) 组合下 10 个样例结果逐项一致; **成立** |
| 8 | W11 / SC-22 pid 位置闭集与包裹下 env 转储 | `t6_clusters.py` | `$$` `$!` `[0-9]*` `*` `1?` `thread-self` `task/1/` `$pid` 基线 0 → 原型 2; `{1,2}`、占位词 `N` / `<pid>` 放行 (已知限制); `sh -c 'printenv'` / `watch env` / `ssh host env` / `nomad alloc exec x env` / `pct exec 101 -- env` 基线 0 → 2; **成立** |
| 9 | W10 / W9 / W12 不执行不变量 | `t7_decoy.py`: 赋值值里命令替换 / 反引号 / 算术展开 / 链式引用 / `.environ.get('$(…)')` / 条目里的 `$(…)`、反引号、通配 | 8 个诱饵路径全部不存在; 条目内的命令替换与反引号按字面匹配 (exit 2), 通配保持字面 (exit 0); **成立** |
| 10 | W9 有效条目为零不得 exit 2 | `t6_clusters.py` Cluster R: 缺失 / 只有注释 / 只有空白 / 全被跳过 | 四种均 `ls`=0、`cat README`=0、Read / Edit 无关路径=0、`cat dotenv`=2、Read dotenv=2; **成立** |
| 11 | 全探针目标态 | `WPA_ONLY=… python3 baseline_probe.py $A/t4f/aria` (分 5 次, 见上) | 403 行全 yes; **成立** |
| 12 | 关键形态误报 / 漏报 (git SHA、sha256sum 输出、UUID、npm integrity、`token_last_eight`、`${…}` / `{{ }}` 占位、JSON 冒号后空格 / 多行、INI 等号两侧空格、YAML 大写键、`Authorization` 头、CRLF) | `t10_fp.py` | 17 个应静默的形态: 仅 `TOKEN_ID: <uuid>` 告警 (Spec 已列已知误报类); 基线对 `${…}` / `{{ }}` 占位的 FP 在原型静默; 10 个应检出形态全部检出; 单引号 JSON 与小写 YAML 静默 (已知限制); **与 Spec 一致** |

## 上一轮对账

| R3 键 | 簇 | 判定 | 证据 |
|---|---|---|---|
| `4f713847` | Q (W1 NUL) | closed (对 R3 所述 NUL 失明); 修法引入 C1 | 基线 4/4 silent -> 原型 4/4 `env-line-secret-keyword=3` (Read / Bash x bash 5.2 / 3.2.57); SC-1 4/4; 变异体 NUL→空格使 1c / 1d 红 |
| `eb350937` | M (覆盖面: 既有被改写成员 / 阈值 / 回退腿 / 包裹下 env) | closed (抽样) | SC-2 6/6 (2e / 2f)、SC-7 14/14 (7k)、SC-12 15/15 (12n / 12o)、SC-19 29/29 (19ac)、SC-22 72/72 (22bo 等) 在原型上全 yes; 手验见实跑 8。残余: 逐成员删除类坏实现我只抽 2 个, 且 M1 第 3 点证明「无左边界」这类越界变异体存活 |
| `1c49d896` | M (分类器 / 白名单作用面) | closed | SC-7 14/14 (7h / 7j / 7k / 7l / 7m / 7n 在内) |
| `8fbbee80` | M (tight credit 逐成员) | closed (抽样) | SC-22 72/72、SC-16 18/18 (16r); 手验 `ps -ef \| grep -v grep` 2、`ps aux \| wc -l` 0、`sudo -u svc ps -ef` 2、`/bin/ps aux` 2、`pgrep -af` 2、`top -b -n1 -c` 2、`docker top` / `docker container top` 2 |
| `05982c10` | P (关闭关键字检查) | closed | 实跑 6 |
| `28af0372` | R (有效条目为零) | closed | 实跑 10; SC-20 17/17 |
| `44b5bb44` | E (locale) | closed (L3) | 实跑 7; 新增行里无字符范围 (原型 `_entropy_ok` 等用显式枚举) |
| `8d258b19` | S (不执行不变量) | closed | 实跑 9; SC-19 29/29 (19ab)、SC-21 23/23 (21z)、SC-23 9/9 (23i)、SC-7 14/14 (7n) |
| `0a8380fd` | T (W9 阶段切分) | **partially closed** -> M2 | 引号一类已修 (19z / 19aa 绿, 引号内 `;` 的实跑正确); 续行 / `&` 重定向 / `||` 未修, 见 M2 |
| `ac42f607` | K (`/proc` pid 位置) | closed | 实跑 8; SC-22 22bp |

R3 minor: 仅 `6f503728` 部分处置 (见 m1)。其余 (Tasks 1.1 / 1.12 的非 root 与 `OK ` 执行条件、Impact 三处偏离、W4 的 38 tag 与「3 个头 tag」、W14 的 K = 实跑总数与 (f0) 两面、W7 订正、W8 / W11 旧计数、W11 同族列举与 `docker container top`、SC-28 判据加强、Impact 三步检查) 我在 v4 文字里逐项核到落实, 未发现未处置项。

## 对执笔人自报薄弱点与请裁项的表态

薄弱点 (v4 报告第 6 节):
1. 原型不是实现 / 坏实现自构 (同源盲区): 作为披露可接受; 但本轮三条 C/M 正是它挡不住的那类 (C1 的既有检出域、M1 的超长单行、M2 的续行), Tasks 1.8 的非作者对抗 review 不能只当后手, 本版就应补上面三类行。
2. 体量 +21.7%: 可接受; 见风险 8。
3. 验收前置变多 (第二 locale / 非 root / 真 bash 3.2): 可接受。我以 uid 1000 跑通; `setpriv` 降权路径我同样没有实测。
4. 回归复跑精化 (只复跑 v3 红过的行): 可接受 (单调判据正确)。
5. 等价变异 (4 + 14): 可接受; 我未逐个复核。
6. 时档是单机比值: 不可接受为「足够」—— 缺超长单行档 (M1), 且 bash 3.2 上基线本身已很慢 (风险 3)。
7. 新增 / 反转的已知限制: 19ae 默认值不可接受 (m1, 技术级应直接裁); 22bj 文本提及误拦可接受 (已成文并钉住, 我自己的 heredoc 命令被活基线拦了 3 次, 见风险 6); `sh -c 'printenv'` 反转为拦截可接受 (手验成立)。
8. fuzz 只覆盖引号状态: 不可接受为「与内建一致」的证据 (M2)。
9. 7n 是预防性行: 可接受 (成本低, 无代码宿主)。
10. 证据在高负载主机上跑: 可接受 (逐字节相等性与负载无关)。

请裁项:
- 技术级 21 (NUL→换行纳入): 不可接受 (C1); 改 (a) 两视图或 (b) 已知限制。
- 22 (`/proc` pid 闭集): 可接受。23 (`sh -c` / `bash -c` / `watch` x env): 可接受。
- 24 (W9 阶段切分与字节语义): 字节语义可接受 (m1 另提默认值); 阶段切分不可接受 (M2)。
- 25 (不执行不变量 + 4 个诱饵行): 可接受。26 (字符类 locale 无关 + 32d): 可接受。27 (文本提及误拦): 可接受。28 (tight 逐成员 / 作用面逐 tag x 步骤): 可接受。29 (关闭关键字三步检查): 可接受。30 (SC-28 判据扩到兄弟位置): 可接受。
- Rule #10 自作主张乙 1-5: 1、2、4、5 可接受; 3「没有新增 hook 机制」措辞不准: `_sg_ext_mask` 是约 30 行的新 bash 状态机, 且 NUL 变换是新行为, 应写成「没有新增机制类别」。
- 未采纳的席位备注丙 1 (SC-14 canary / W6 清理用记下的变量): 可接受不采纳 —— 现有两个套件已用 `rm -rf "$记下的变量"` (`secret-guard.test.sh:589 / 1145 / 1325 / 1915`, `secret-scan.test.sh:188`), 没有写 `rm -rf "$HOME"` 的先例。丙 2 (W5 `source` 的 `case` 白名单): 可接受 (现行 matcher 下不可达)。丙 3 (在 #154 关单评论披露 MINGW64 / macOS 未实测): 建议采纳, 一句话, 且本轮另有 BSD grep 与 bash 3.2 耗时两项未测面 (风险 2、3)。丙 4-6: 无异议 (不在我的视角)。

## 风险 / 疑问 (不计入 finding)

1. NUL 到达前提无端到端样本: W1 与 C1 共用同一前提 (NUL 以 `\u0000` 到达 PostToolUse hook; Read 的 `/proc/<pid>/environ` 是否有内容也未验, 该文件 `st_size` 为 0)。Spec 应写明前提来源, 或在 Tasks 1.12 加一条 NUL 腿; 我无法在不读取真实环境变量的前提下验证 (Rule #7)。
2. macOS / BSD 未验: W9 依赖 `grep -F -f <(条目)` 在空文件时「匹配无」(GNU 成立, FreeBSD 近年也是, 但未验)、以及 `grep -o -b` 给出匹配本身的字节偏移。若某实现把空 `-f` 当匹配一切, Read / Edit 面会全部 exit 2 (与「从不因扩展问题 exit 2」相反)。SC-20 20o-20q 只在 Linux 上跑; 建议实现里显式 `[[ -n 条目 ]]` 守卫后再调 grep。
3. bash 3.2 耗时: 我测到基线 hook 在真 bash 3.2.57 上 2.5 KB 多段命令 5.76 s、3.8 KB 12.5 s (v4 原型 7.37 s / 16.45 s, 比值 1.28-1.31; 主机负载 5-8, 只看比值), 即 macOS `/bin/bash` 3.2 用户上 L1 对约 2 KB 以上命令已超过 5 s 超时而放行; v4 把悬崖前移约 30%。W14 时档只跑默认 bash, 且只提 Windows 未测。
4. 未普查目录的 L3 误报: 对 `docs/`、`openspec/`、`.aria/`、`aria-orchestrator/` 共约 2585 个 ≤ 200 KB 文件做关键词预筛得 19 个候选, 按 Read 信封喂基线与原型 (`$A/h/t11_census.py`, 只记 tag): 11 个在 Read 扫描下新告警 —— 5 个是本工作流自己的审计报告 (讨论文本里引用的示例形态, 命中既有 `json-secret-field` 与新 tag)、2 个 skill 工作区副本 (命中既有 `env-line-secret-keyword`, 不在 SC-33 的「6 个新 tag」口径里)、4 个 orchestrator 文件 (1 个配置、1 个证据文档、2 个脱敏测试夹具; 我没有判定真 / 假阳性, 不读值)。即 W1 之后读这些文件会注入「按已泄露处理」提示; 待复议 7.17 已承认该语料缺口, 建议至少把审计报告目录与 skill 工作区纳入归因清单。
5. 部分计数算术: 原型 `actual_counted=$(( keep - residual ))` 在「有被白名单放过的 span 且 sed 未能消费全部 span」同现时可能得 0 或负数, 使真命中不计 (基线用 `count - residual`)。residual 需要 grep 与 sed 对同一正则判定不一致, 我没有构造出来, 但回归方向值得实现者注意。
6. 活体观察: 我自己的 3 次 Bash 命令被活基线 secret-guard 拦下 (heredoc 里只是提到 `ssh … printenv` / `cat … .env` 一类文本, 即 22bj 同类); 3 次 Write (脚本源码里含占位式 / 拼装的 JSON 字符串) 触发活基线 secret-scan 告警。均无真实凭据, 属 W3 / W11 描述的误报类, 我改用 Write 工具落脚本并运行时拼装词, 没有使用 `# guard:ack`。
7. SC-33 的口径只数 6 个新 tag: Read 扫描上线后既有 tag 的误报 (如上 skill 工作区的 `env-line-secret-keyword`) 不在任何 SC 内。
8. 收敛判断: 本轮 3 个 C/M 中 2 个 (C1、M2) 是 v4 对 R3 的修复本身引入或未修净 (簇 Q 的 `tr`、簇 T 的掩码), 第 3 个 (M1) 是 v3 前就有、至今没人量过的设计面。按本仓 marginal-return 判据 (本轮修复引入的 major 占比 > 1/2) 已到拐点; 建议 v5 只做三处定向收窄 (C1 / M1 / M2 各一处文字 + 行), 不加新机制。
9. Windows Git-Bash 的 `grep -f <(…)` 进程替换与 UTF-16 实际形态未测。

## Verdict

verdict: **FAIL** (有 critical)。counts: **1C/2M/1m**。

**Vote: REVISE**

## 是否足以进入 A.2

不足以: C1 是 Spec 自己强制的检出回退 (论据与实跑相反), 必须先改 W1 并补 `reverse-guard` 行; M1 / M2 各需一处文字收窄加行 (超长单行时档与左边界行; 扩展与内建同形差分家族), 否则实现者按 Spec 字面会得到全绿的探针与有缺陷的 hook。
