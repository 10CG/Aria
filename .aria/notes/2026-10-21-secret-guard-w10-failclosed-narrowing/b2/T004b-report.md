# TASK-004 第二段报告 (10CG/aria-plugin#217)

执行席: 第二段新实例。任务书 `r217impl/BRIEF-T004b.md`。开跑 2026-10-24 22:37:49Z, 收尾 2026-10-24 23:57:41Z (UTC)。
预期先写: `r217impl/t004b/PREDICT.md` 写于改脚本之前 (第 7 次调用), 改脚本在第 9 次调用。未 commit。

## 0. 结论一览

- `run-evidence.sh` 按任务书改了 4 处 (+51 −11), 核对全过, 含负控和旧版对照 (§1)。
- 6 个阶段 (W9、W13 全量、P-0 v31 模式、P-0 套件模式、套件坏实现、W12) 都是第一次就有效: 开跑前一分钟负载都 < 1.2, 首尾读数都 < 2, 没有作废, 也没有重跑 (§2)。
- 验收 3 (W9): 一致 (§3)。
- 验收 2 (W13): 实现在 5 个 bash 上 FAIL 0、SKIP 0; mutants.py 生成的 57 个 BI 在 sc-cases.sh (全量模式) 与移植后的套件上都 CAUGHT; P-0 三次读数都是 GREEN。基线红集按编号逐个比对与 95cf1de7 一致, 但有 3 项要说明: 2 个用例变了色 (都是 R2 补强改写过的)、1 个改名、51 个新编号; 另外 W13 文件第 2 节的 red 行只收 FAIL, 不收 MISSING。见 §4.2 和 §6。
- 验收 5、6 (W12): 一致。SMAX 放行 136 条, 与 95cf1de7 相同, 没有少掉的那条; VMAX 那 1 条照旧拦下; 越界 0 / 138; 第 2、3 节分别是 300 / 300 和 40 / 40。1b 的数见 §5.2。
- 拿不准、需要主控裁的: §6 列了 6 项。最要紧的两项: 1b 字节比对的取法 (§6.1), 「回落成尺寸文案」有两种读法 (§6.2)。

## 1. run-evidence.sh 的改动与核对

diff 全文见附录 A (`t004b/run-evidence.diff`)。改后文件的 sha256 前缀是 54fa8638f1d4; 驱动开跑时记了这个值, 收尾时复核仍是它, 运行期间没有改过。

### 1.1 四处改动

1. **W9 页眉**: 在两轮套件开跑前先取 `H9=$(hdr)` 作为首行, 末行照旧调用 `hdr`。首行从此带上开始时的负载, 与 W11、W12、W13 的做法一致。
2. **W12 缺 TRAFFIC_DIR**: 新增一行前置核对, 和其余核对放在一起, 位于建工作目录之前。选了 W12 而 `TRAFFIC_DIR` 为空、未设, 或者 `$TRAFFIC_DIR/cmds` 不是目录时, 退出 3。头注释同步改了。原来 W12 分支里那句 `:?` 没删, 现在已经执行不到。
3. **`W12-replay-138.tsv` 页眉 (INV-8)**: replay138.sh 现在写 `W12-replay-138.rows`, 之后由 run-evidence.sh 拼成「`H12` 页眉 + 原行」, 存为 `.tsv`。第 1 节的 4 个读者都加了 `/^#/{next}`; 最后一个读者原来用 `NR` 计总数, 改成数非 `#` 行。`W12-real-traffic.txt` 的首行就用同一个 `H12`。
4. **1b. latency cost** (design 8): 同一批 138 条用 replay138.sh 在基线上回放一遍 (喂 base.sh, 没有探针, T_trigger 记 `-`), 得到 `W12-replay-138-base.tsv` (带页眉)。字节比对用 ident.sh 在同一批 138 条上另跑一遍 (基线 vs 未插桩的实现), 得到 `W12-ident-138.txt` (带页眉)。然后用一段 awk 按编号对齐三份文件, 输出三类: 回落、放行、未进入重跑, 外加「进入重跑的其他结局」一类, 免得有结局漏算。最后的 cp 把两份新文件也拷进 OUT。

### 1.2 核对 (`t004b/patch-and-check.sh`, 输出 `t004b/patch-and-check.out`)

- `bash -n` 通过, 没有 CR 字节, 文件权限 755 不变; v31 下除 run-evidence.sh 外没有其他改动。
- **TRAFFIC_DIR, 新版** (OUT 指向空目录 `chk/out`):

  | 用例 | 阶段 | rc | 工作目录 | OUT 文件数 |
  |---|---|---|---|---|
  | tA: 空串 | W12 | 3 | 未建 | 0 |
  | tB: 目录在, 但没有 cmds | W12 | 3 | 未建 | 0 |
  | tC: 未设 | W12 | 3 | 未建 | 0 |
  | tE: 空串 | W8 W12 | 3 | 未建 | 0 (W8 也没有写) |
  | tD: 未设 (正控) | W8 | 0 | 建出 | 1 |

- **旧版对照**: HEAD (51434e44) 的 run-evidence.sh, 用 `bash -c` 以 v31 为 HERE 运行, 空 TRAFFIC_DIR, 阶段 W12。结果 rc 127, 工作目录被建出, 已写入 2 个文件 (base.sh、impl.sh), 然后在第 50 行的 `:?` 处退出。
  预期写的是 1 (第一段报告记的值, 当时作为文件运行)。127 应是 `bash -c` 调用方式造成的, 没有另外核实。这不影响判定: 旧版是「写了文件之后才以非 0 退出」, 新版是「什么都没写就退出 3」。
- **页眉前后第 1 节汇总逐字相同**:
  - 用 95cf1de7 的 tsv: 旧读者吃无页眉版、新读者吃加页眉版, 输出逐字相同 (8 行), 并且与 95cf1de7 `W12-real-traffic.txt` 第 3-10 行逐字相同。负控: 旧读者吃加页眉版, 有 4 行不同, 说明这项检查能红。
  - 本轮 W12: 旧读者吃 `.rows`、新读者吃 `.tsv`, 两者相同; 它们也与本轮文件第 1 节相同。
- **1b 合成输入**: 实现侧用 95cf1de7 的 138 行; 基线侧是编造的, 每条 0.200 s, 结局按 oversize 或 growth 给; ident 侧给放行的那些写 DIFF。结果: 放行 136, extra p50 0.562、max 2.587, 与 95cf1de7 的 allow wall p50 0.76、max 2.79 各减 0.2 吻合。n=1053 归入「回落」, 因为编造的基线在这条上也是 growth。未进入重跑 1 条 (n=666), 相同 1 / 1。awk 在 mawk 下能跑。

## 2. 各阶段首尾负载 (驱动 `t004b/drive.sh`, 日志 `t004b/drive.log`)

所有阶段都加了 `taskset -c 0,1 nice -n 19`, 串行执行, 同一时刻只跑一个重实验。每个阶段开跑前, 驱动都等到一分钟负载 < 1.2。下表「首读数 / 末读数」取自输出文件自己的首行和末行。

| 阶段 | 起止 (UTC) | 耗时 | 首读数 | 末读数 | 判定 |
|---|---|---|---|---|---|
| W9 | 22:37:49 – 22:45:07 | 7 分 18 秒 | 0.45 0.58 0.81 | 1.93 1.61 1.25 | 有效 (末读数离 2 不远) |
| W13, MUT_SCOPE=full | 22:46:07 – 23:44:00 | 57 分 53 秒 | 1.08 1.44 1.21 | 0.81 0.94 1.03 | 有效 |
| P-0, v31 模式 | 23:44:00 – 23:44:50 | 50 秒 | 0.81 0.94 1.03 | 0.61 0.86 0.99 | 有效 |
| P-0, 套件模式 | 23:44:50 – 23:45:39 | 49 秒 | 0.61 0.86 0.99 | 0.89 0.89 1.00 | 有效 |
| 套件坏实现 | 23:45:39 – 23:49:01 | 3 分 22 秒 | 0.90 0.90 1.00 | 1.56 1.22 1.11 | 有效 |
| W12 | 23:49:31 – 23:57:41 | 8 分 10 秒 | 1.00 1.12 1.08 | 1.48 1.50 1.28 | 有效 (开跑前等了 30 秒, 让负载降到 < 1.2) |

- 作废 0 次, 重跑 0 次。
- 没有 NOT-JUDGED, 所以驱动里预备的 NOT-JUDGED 重跑一次也没触发。
- W13 第 1 节在 5 个 bash 上都是 `SKIP 0 (load 0, void 0, inconclusive 0, root 0)`, 即计时批全部判过。
- 收尾时: 驱动已退出, 它的进程组 (PGID 897310) 里没有残留进程; wt217/aria 仍在 2893bcc, 工作树干净。

## 3. 对照 W9 (验收 3) — 一致

- base → impl 之间有变化的组恰好是 SC-21ab、21ac、21ag、21aj、21al、21ao 六组。SC-13 的 FAIL 条目在 base 和 impl 里逐字相同, 不算变化 (它来自非 git 副本)。
- 汇总行: base 是 PASS 813/814、FAIL 1/814, impl 是 PASS 807/814、FAIL 7/814, 与 95cf1de7 相同。
- 与主控低负载的两轮 (`b2/t004a-verify/suite-proto.out`、`suite-impl2.out`) 比, 用主控的 `cmp-w9.py`: 六组的检查数分别是 11 / 3 / 1 / 3 / 3 / 3, 两轮都一样; 检查清单逐条相同 (六组都是 True)。
- 与 95cf1de7 的 W9-suite.txt 比:
  - impl 的 7 个条目里 6 个逐字相同。
  - 只有 SC-21ab 不同: 现在 6 行检查, 95cf1de7 是 3 行。95cf1de7 的 3 行现在都在, 多出的 3 行是 `refused [...]: exit code: want '2', got '0'` 和 `refused [...]: says to split: want 'yes', got 'no'` (去重后 2 种)。
  - 这就是第一段指出的那 3 处: 实现放行了, 原型那一轮 (负载 3.59) 回落拦下。
- W9 页眉的首行时间 22:37:49, 末行 22:45:07, 首读数是开跑前的读数。改动 1 生效。
- 本份替换了第一段那一份 (那份的收尾读数是 2.79)。

## 4. 对照 W13 (验收 2)

### 4.1 第 1 节 — 一致

| bash | PASS | FAIL / MISSING / SETUP / SKIP | relaxation expected |
|---|---|---|---|
| 5.0.18 | 142 | 0 / 0 / 0 / 0 | yes |
| 5.1.16 | 142 | 0 / 0 / 0 / 0 | yes |
| 5.2.15 | 142 | 0 / 0 / 0 / 0 | yes |
| 5.3.20 | 142 | 0 / 0 / 0 / 0 | yes |
| 3.2.57 | 79 | 0 / 0 / 0 / 0 | no |

第 1 节的 FAIL 行数为 0; 没有 SKIP, 所以没有需要单列的。

### 4.2 第 2 节 (基线红集) — 按编号一致, 另有 4 项单列说明

逐个比对用的是工作目录里的 `sc-base.txt`, 已拷到 `t004b/ana/W13-sc-base.txt`。原因: W13 文件第 2 节的 red 行只收 FAIL, 见 §6.3。

- 现在的结果: MISSING 74、FAIL 43、PASS 25, 共 142。95cf1de7: red 73、green 19, 共 92。两边共有的编号 91 个。
- **共有编号里的红**: 95cf1de7 红的 72 个现在都还是红, 其中 51 个是 MISSING (缺失), 21 个是 FAIL (判错)。
- **共有编号里的绿**: 95cf1de7 绿的 19 个里, 17 个现在仍是 PASS。另外 2 个变了色, 都在 8f66e393 (B.2 第二步, R2 补强) 里改写过 (`git log -G` 核过)。按任务书, 它们属于「改写的用例」, 单列:
  - V5-S13b-nothing-outlives-the-run: 绿 → MISSING
  - V7-E15-credit-as-normal: 绿 → FAIL
- **95cf1de7 有、现在没有**: 只有 V3-E5-budget-1。TASK-002 第二步主控裁定 (4) 把它改名为 V3-E5-budget-2, 现在是 FAIL, 计在下面的新编号里。
- **新编号 51 个** (PASS 8、FAIL 21、MISSING 22):
  - V14-F1、V14-G1、V14-G2、V14-N1 (FAIL) 与 V14-N2 (PASS): 来自 382bb001 (TASK-003 第一段)。
  - 其余 46 个: 首次出现在 8f66e393 (R2 补强)。
  - 逐条列表 (编号 / 基线结果 / 首次出现的提交) 见附录 B。

### 4.3 第 3 节 (MUT_SCOPE=full, sc-cases.sh, bash 5.2) — 一致

- 57 caught, 0 missed, 0 wrong reason, 0 not judged, 0 setup (of 57)。
- P-* 中 P-0 以外的 6 个都 CAUGHT; P-0 是 GREEN; perturbation round 0 not as expected。共 64 个变体。
- 其他红 (design 5): 17 个坏实现带其他红, 共 57 个用例次。逐个列在附录 C。

### 4.4 套件坏实现 (`v31/impl/W13-suite-mutants.txt`, MUT_SUITE=wt217/aria, 指定用例) — 一致

- 57 caught, 0 missed, 0 wrong reason, 0 not judged, 0 setup (of 57)。
- P-0 以外的 6 个 P-* 都 CAUGHT, P-0 是 GREEN, perturbation round 0 not as expected, 退出 0。
- 带 red[reference] 的只有 BI-8, 与 TASK-002 3d 相同。
- 文件首行就是 run-mutants.sh 自己的首行, 末行是 `# perturbation round ... | load at the end`。

### 4.5 P-0 的读数 (design 7)

| 运行 | 首读数 → 末读数 | 结果 |
|---|---|---|
| W13 全量连跑里的 P-0 | 连跑末读数 0.81 | GREEN (PASS 142, FAIL 0) |
| 低负载单跑, v31 模式 (`v31/impl/W13-P0-v31.txt`) | 0.81 → 0.61 | GREEN (PASS 142) |
| 低负载单跑, 套件模式 (`v31/impl/W13-P0-suite.txt`) | 0.61 → 0.89 | GREEN (只容 SKIP [platform]) |

全量连跑里的 P-0 这次没有 NOT-JUDGED: 预计的尾部高负载没有出现。

## 5. 对照 W12 (验收 5、6) 与 1b

### 5.1 验收 5、6 — 一致

- **第 1 节 (越界)**: 越界 0 / 138 (`every outcome within max(trigger, 3 s) + 0.3 s: 0 of 138 over the bound`)。
- **第 1 节 (结局)**: allow 136、growth 1、oversize 1。按 W1 分类:
  - size → allow 136
  - size → growth 1 (n=1053)
  - value → oversize 1 (n=666)
- **第 1 节 (放行耗时)**: allow wall p50 0.59、p90 1.18、p99 1.59、max 2.29 s。95cf1de7 是 0.76 / 1.70 / 2.43 / 2.79。
- **SMAX 放行数**: 136, 95cf1de7 也是 136, 下限 135。没有少掉的那条, 所以没有编号要记。和 95cf1de7 比, 放行集合逐个相同: 两个方向都是 0 条。
- **VMAX**: n=666 照旧拦下。实现 oversize、rc 2、没有 relax-start; 基线 oversize; 95cf1de7 也是 oversize。
- **没有进入重跑的与基线逐字节相同**: 1 / 1。这条就是 n=666; 证据来自 ident.sh 另跑的那一遍, 两次回放的结局种类也一致。取法见 §6.1。
- **第 2 节**: identical=300 different=0。
- **第 3 节**: identical=40 different=0。
- **INV-8**: 首行 sha 前缀为基线 e83c5e30f2cc、实现 af4658b6f935, sc-cases.sh、sc-direct.sh、mutants.py 依次为 7d29c3cd0f5b / fb3418921bca / 2060d2e0c17f。`W12-real-traffic.txt` 和三份 TSV / txt 都带这些前缀。

### 5.2 1b 的数 (不设门槛, 随 TASK-006 的 owner 门呈报)

- 基线回放的结局: 138 条全部 oversize。
- **进入重跑后回落成基线的尺寸文案** (relax-start、rc 2、与基线同类文案): **0 条**, 所以没有逐条列表, 也没有分布。
- **进入重跑并放行**: 136 条。比基线多等的秒数: **p50 0.272、p90 0.638、max 1.771** (p50 / p90 按最近秩)。
- **进入重跑后的其他结局**: 1 条。n=1053, rc 2, 实现给的是 growth 文案, 基线给的是 oversize 文案。实现 W 0.255 s, 基线 W 0.131 s, 多等 0.124 s。它的 stderr 与基线不同 (ident 那一遍记为 DIFF)。95cf1de7 里这条也是 growth, 不是本变更引入的新情形。
- **没有进入重跑**: 1 条 (n=666)。rc 与 sha256(stderr) 和基线相同: 1 / 1。
- ident.sh 那一遍 (全部 138 条): identical=1, different=137。
- 「回落」按任务书字面另有一种读法, 得数不同, 见 §6.2。

## 6. 未做 / 拿不准 / 需主控裁的项

1. **1b 的字节比对取自另跑的一遍, 而不是计时那一遍。**
   - replay138.sh 不记 stderr 的 sha256: 它把 stderr 写进 mktemp 目录, 退出时删掉。任务书写的是「需要的话让基线回放也记」, 但实现那一侧同样没有记录, 而本段不许改 replay138.sh。
   - 所以我改用项目已有的 ident.sh (第 2、3 节用的就是它, 比 rc + sha256(stderr)), 在同一批 138 条上另跑一遍: 基线 vs 未插桩的实现。
   - 局限: 对结局随时间变化的条目, 另跑的一遍可能和计时那一遍不同。本轮用到这一点的只有「未进入重跑」的 n=666。它不会进入重跑, 结果是确定的; 两次回放的种类也一致 (oversize 对 oversize)。
   - 若要「同一遍」的读法, 需要改 replay138.sh, 在本段的文件范围之外。这是取法上的选择, 请主控裁定是否认可。
2. **「回落成尺寸文案」有两种读法, 我没有替主控选。**
   - 按任务书字面 (实现那一侧有 relax-start、rc 2、尺寸文案): 如果把 growth 文案也算作尺寸文案, 就是 1 条。即 n=1053, 多等 0.124 s, p50 = p90 = max = 0.124。
   - 按「回落 = 基线字节」: 0 条。n=1053 的文案种类和字节都与基线不同, 是进入重跑后的另一种拦截, 不是回落。
   - 1b 小节的输出把这一条单列在「其他结局」下, 两种读法都能从文件里读出。
3. **W13 文件第 2 节的 red 行只收 FAIL (run-evidence.sh 原有写法)。**
   - sc-cases.sh 现在把基线上缺函数的用例记为 MISSING (74 个), 它们既不在 red 行, 也不在 green 行。因此单看 W13 文件, 「缺失」那一栏不可见, red 行从 95cf1de7 的 73 个变成 43 个。
   - 我的逐个比对用的是 `sc-base.txt` (§4.2)。
   - 这不在任务书列的 4 处改动之内, 我没有改。下一次改 run-evidence.sh 时, 可以让第 2 节另列一行 MISSING。
4. **INV-8 对 run-mutants.sh 自带首行的覆盖不全。**
   - `W13-suite-mutants.txt` 和两份 P-0 输出的首行是 run-mutants.sh 自己写的 (任务书要求「连同它自己的首行」)。首行里有实现 hook 和 mutants.py 的 sha; v31 模式另有 sc-cases.sh 的 sha, 套件模式另有套件三个文件的 sha。
   - 但首行里没有基线 hook 和 sc-direct.sh 的 sha 前缀。只记下, 没有改 (改 run-mutants.sh 在本段文件范围之外)。
5. **v31/impl/ 下新增了 4 个任务书没有点名的文件**, 请主控决定是否收进提交:
   - `W12-replay-138-base.tsv` 和 `W12-ident-138.txt`: 由改动 4 产生, 1b 的原始数据, 带页眉。
   - `W13-P0-v31.txt` 和 `W13-P0-suite.txt`: 驱动拷过去的 P-0 单跑输出, 文件名是我起的。
   - 这 4 个文件都只有编号、rc、种类、墙钟和 sha, 不含命令文本。
6. **预期没说中的项** (照实记; 对照 `PREDICT.md`):
   - 旧版对照的 rc 是 127, 预期是 1 (§1.2)。
   - 3.2.57 是 SKIP 0, 不是预期的「有 SKIP [platform]」: sc-cases.sh 在 3.2 上只跑 79 个用例。
   - 第 2 节有 2 个变色和 1 个改名, 预期写的是「共有编号逐个相同」, 没有想到改写的用例。
   - 全量连跑里的 P-0 是 GREEN, 预期是「可能 NOT-JUDGED」。
   - 1b 放行的 p50 是 0.272 s, 低于预期的 0.4-0.8 s。
7. **过程问题 (我自己的失误, 不影响实验)**:
   - 第 13 次调用里误留了一个没有输入的 `python3 -`。它在 W13 运行期间阻塞在读 stdin 上, 大约 10 分钟, 不占 CPU。随后我按记下的 PID 1041193 清掉; 它所在的那条命令后来自行结束。
   - 另外, W13 运行期间我跑过几次轻量分析 (对小文本文件的 python / awk), 不是重实验。
8. 没有 commit。主仓 `git status` (不带路径) 的结果:
   - run-evidence.sh 显示为已修改 (M)。
   - v31/impl/ 下 9 个未跟踪文件: W9、W12 四个、W13 四个。W8、W11、W14 两个是第一段与 TASK-003 的交付, 未改动。

## 7. 过程材料 (`scratchpad/r217impl/t004b/`, 不含任何命令文本)

| 类别 | 文件 |
|---|---|
| 预期与改脚本 | `PREDICT.md`、`patch-and-check.sh` / `.out`、`run-evidence.diff`、`chk/` (核对用的临时文件和 95cf1de7 的 tsv) |
| 驱动 | `drive.sh`、`drive.log`、`drive.out`、`runs/` (各阶段 stdout) |
| 工作目录 | `wd-W9-a1`、`wd-W13-a1`、`wd-P0v-a1`、`wd-P0s-a1`、`wd-SM-a1`、`wd-W12-a1` |
| 分析 | `analyze.sh`、`ana-*.out`、`ana/` (含 `W13-sc-base.txt`) |
| 实现 hook 拷贝 | `impl-hook.sh` (af4658b6f935) |


## 附录 A: run-evidence.sh 的 diff (`t004b/run-evidence.diff`, 相对 HEAD 51434e44)

```diff
diff --git a/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-evidence.sh b/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-evidence.sh
index ed5bab87..8433bcc0 100755
--- a/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-evidence.sh
+++ b/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-evidence.sh
@@ -4,15 +4,17 @@
 # baseline's). Every output is written into the work dir first and copied to OUT only when its stage has finished, so a failed or partial run never
 # overwrites committed evidence; OUT=<an existing directory> (TASK-004: v31/impl), default this script's directory, which reproduces the evidence of 95cf1de7.
 # Every output's first line records the date, the platform, the sha256 prefixes of both hooks and of sc-cases.sh, sc-direct.sh and mutants.py (INV-8) and
-# the load; the W8 diff starts with that line too (patch and git apply skip the text before a diff).
+# the load, taken before the stage's runs start; W9, W11, W12 and W13 write it again as their last line (the load at the end, INV-7). The W8 diff starts
+# with that line too (patch and git apply skip the text before a diff), and so do the W12 TSVs (their readers skip the lines that start with #).
 # Needs: Linux, bash 5 on PATH, jq, python3, taskset, nice; W13 and W12 also BASH32 (a bash 3.2 binary), W12 also TRAFFIC_DIR (the frozen corpus, outside the
-# repo). A bash under test that is missing or not executable, an OUT that is not a writable directory, or a work dir that cannot be created exits 3 before
-# any file is written.
+# repo, with its cmds directory). A bash under test that is missing or not executable, W12 without TRAFFIC_DIR/cmds, an OUT that is not a writable
+# directory, or a work dir that cannot be created exits 3 before any file is written.
 set -u
 HERE="$(cd "$(dirname "$0")" && pwd)"; W=$(readlink -m "$1"); shift; STAGES=${*:-W8 W13 W11 W12 W9}; OUT=${OUT:-$HERE}
 B13=(/home/dev/.aria/tools/bash-5.0.18/bash /home/dev/.aria/tools/bash-5.1.16/bash /usr/bin/bash /home/dev/.aria/tools/bash-5.3.20/bash)   # W13: one run each, then BASH32
 NB=(); for st in $STAGES; do case $st in W13) NB+=("${B13[@]}" "${BASH32:-}");; W12) NB+=("${BASH32:-}" "$(command -v bash)");; W11|W9) NB+=("$(command -v bash)");; esac; done
 for b in "${NB[@]}"; do [[ -n "$b" && -f "$b" && -x "$b" ]] || { echo "a bash under test is missing or not executable: '$b' (W13 and W12 need BASH32)"; exit 3; }; done
+for st in $STAGES; do [[ $st != W12 || ( -n "${TRAFFIC_DIR:-}" && -d "${TRAFFIC_DIR:-}/cmds" ) ]] || { echo "W12 needs TRAFFIC_DIR, the frozen corpus with its cmds directory: '${TRAFFIC_DIR:-}'"; exit 3; }; done
 for f in sc-cases.sh sc-direct.sh mutants.py; do [[ -f "$HERE/$f" ]] || { echo "missing $HERE/$f (its sha256 goes into every header, INV-8)"; exit 3; }; done
 [[ -d "$OUT" && -w "$OUT" ]] || { echo "OUT is not a writable directory: $OUT"; exit 3; }
 ROOT=$(git -C "$HERE" rev-parse --show-toplevel); [[ -n "$W" ]] && mkdir -p "$W" || { echo "cannot create the work dir: ${W:-<empty>}"; exit 3; }
@@ -49,22 +51,60 @@ W11) mkdir -p "$W/adv" "$W/ext/proj/.aria"; printf '%s\n' "billing/conf/prod.tom
       hdr; } > "$W/W11-adversarial.txt"; cp "$W/W11-adversarial.txt" "$OUT/"; echo "W11 done" ;;
 W12) : "${TRAFFIC_DIR:?W12 needs TRAFFIC_DIR}" "${BASH32:?W12 needs BASH32}"; W1="$HERE/../evidence/W1-classification.tsv"
     python3 "$HERE/mkdbg31.py" "$W/impl.sh" "$W/impl-dbg.sh" >/dev/null || exit 3
-    { hdr; echo "## 1. the W10 size-blocked class (W1: 138 commands; the baseline blocks all of them for size), the hook under test (instrumented copy), bash 5.2"
-      "${N[@]}" bash "$HERE/replay138.sh" "$W/impl-dbg.sh" "$W1" "$W/W12-replay-138.tsv" 2>&1 | grep -v setlocale
-      awk -F'\t' '{c[$3]++} END{for (k in c) printf "  outcome %-10s %d\n", k, c[k]}' "$W/W12-replay-138.tsv" | sort
-      awk -F'\t' 'NR==FNR{cls[$1]=$5; next} {printf "  W1 class %-6s -> %s\n", cls[$1], $3}' "$W1" "$W/W12-replay-138.tsv" | sort | uniq -c
-      awk -F'\t' '$3=="allow"{print $4}' "$W/W12-replay-138.tsv" | sort -n | awk '{a[NR]=$1} END{printf "  allow wall (s): n=%d p50=%.2f p90=%.2f p99=%.2f max=%.2f\n", NR, a[int(NR*.5)], a[int(NR*.9)], a[int(NR*.99)], a[NR]}'
-      awk -F'\t' '{t=($6=="-"?$4:$6); b=(t>3?t:3)+0.3; if ($4>b) {v++; printf "  OVER n=%s wall %.3f > bound %.3f\n", $1, $4, b}} END{printf "  every outcome within max(trigger, 3 s) + 0.3 s: %d of %d over the bound\n", v+0, NR}' "$W/W12-replay-138.tsv"
+    H12=$(hdr)   # the first line of W12-real-traffic.txt and of the TSVs written beside it (INV-8)
+    { printf '%s\n' "$H12"; echo "## 1. the W10 size-blocked class (W1: 138 commands; the baseline blocks all of them for size), the hook under test (instrumented copy), bash 5.2"
+      "${N[@]}" bash "$HERE/replay138.sh" "$W/impl-dbg.sh" "$W1" "$W/W12-replay-138.rows" 2>&1 | grep -v setlocale
+      { printf '%s\n' "$H12"; cat "$W/W12-replay-138.rows"; } > "$W/W12-replay-138.tsv"
+      awk -F'\t' '/^#/{next} {c[$3]++} END{for (k in c) printf "  outcome %-10s %d\n", k, c[k]}' "$W/W12-replay-138.tsv" | sort
+      awk -F'\t' 'NR==FNR{cls[$1]=$5; next} /^#/{next} {printf "  W1 class %-6s -> %s\n", cls[$1], $3}' "$W1" "$W/W12-replay-138.tsv" | sort | uniq -c
+      awk -F'\t' '/^#/{next} $3=="allow"{print $4}' "$W/W12-replay-138.tsv" | sort -n | awk '{a[NR]=$1} END{printf "  allow wall (s): n=%d p50=%.2f p90=%.2f p99=%.2f max=%.2f\n", NR, a[int(NR*.5)], a[int(NR*.9)], a[int(NR*.99)], a[NR]}'
+      awk -F'\t' '/^#/{next} {m++; t=($6=="-"?$4:$6); b=(t>3?t:3)+0.3; if ($4>b) {v++; printf "  OVER n=%s wall %.3f > bound %.3f\n", $1, $4, b}} END{printf "  every outcome within max(trigger, 3 s) + 0.3 s: %d of %d over the bound\n", v+0, m}' "$W/W12-replay-138.tsv"
+      echo "## 1b. latency cost: the same 138 replayed on the baseline hook (replay138.sh fed base.sh: no probes, so no trigger time), aligned by n; extra = wall of the hook under test - wall of the baseline (s; p50 / p90 by nearest rank)"
+      "${N[@]}" bash "$HERE/replay138.sh" "$W/base.sh" "$W1" "$W/W12-replay-138-base.rows" 2>&1 | grep -v setlocale
+      { printf '%s\n' "$H12"; cat "$W/W12-replay-138-base.rows"; } > "$W/W12-replay-138-base.tsv"
+      echo "  bytes: ident.sh (rc + sha256(stderr), the baseline vs the uninstrumented hook under test) on the same 138 in a separate pass (W12-ident-138.txt)"
+      cut -f1 "$W1" > "$W/W12-138.lst"
+      { printf '%s\n' "$H12"; "${N[@]}" bash "$HERE/ident.sh" "$W/base.sh" "$W/impl.sh" "$W/W12-138.lst" 2>&1 | grep -v setlocale; } > "$W/W12-ident-138.txt"
+      awk -F'\t' '
+        function srt(a, n,   i, j, x) { for (i = 2; i <= n; i++) { x = a[i]; for (j = i - 1; j > 0 && a[j] > x; j--) a[j + 1] = a[j]; a[j + 1] = x } }
+        function q(a, n, pc,   i) { i = int(pc * n); if (i < pc * n) i++; if (i < 1) i = 1; return a[i] }
+        function dist(a, n) { if (n == 0) return "n=0"; srt(a, n); return sprintf("n=%d p50=%.3f p90=%.3f max=%.3f", n, q(a, n, .5), q(a, n, .9), a[n]) }
+        FNR == 1 { f++ }
+        /^#/ { next }
+        f == 1 { o[++m] = $1; rc[$1] = $2 + 0; k[$1] = $3; w[$1] = $4; rs[$1] = $6; next }
+        f == 2 { bk[$1] = $3; bw[$1] = $4; bc[$3]++; next }
+        f == 3 && /^DIFF n=/ { split($0, dv, /[ =]/); d[dv[3]] = 1; next }
+        f == 3 && /^identical=/ { idl = $0; next }
+        END {
+          for (x in bc) bl = bl sprintf(" %s %d", x, bc[x]); printf "  baseline replay outcomes:%s\n", bl
+          for (i = 1; i <= m; i++) { x = o[i]
+            if (!(x in bw)) { nb = nb " " x; continue }
+            e = w[x] - bw[x]
+            if (rs[x] == "-") { nr++; if (x in d) nd = nd " " x; else ni++; continue }
+            if (rc[x] == 0) { ea[++na] = e; continue }
+            if (rc[x] == 2 && k[x] == bk[x] && k[x] ~ /^(oversize|longline|growth|tmax)$/) { ef[++nf] = e
+              fl[nf] = sprintf("    n=%-6s W %.3f  base W %.3f  extra %.3f  (%s; ident pass: %s)", x, w[x], bw[x], e, k[x], ((x in d) ? "differs" : "identical")); continue }
+            no++; ol = ol sprintf("\n    n=%-6s rc %d %s (baseline %s)  W %.3f  base W %.3f", x, rc[x], k[x], bk[x], w[x], bw[x])
+          }
+          printf "  entered the rerun, fell back to the size text of the baseline (relax-start, rc 2, the kind of the baseline): %d\n", nf
+          for (i = 1; i <= nf; i++) print fl[i]
+          printf "    extra (s): %s\n", dist(ef, nf)
+          printf "  entered the rerun and allowed: extra (s): %s\n", dist(ea, na)
+          printf "  entered the rerun, any other outcome: %d%s\n", no, ol
+          printf "  did not enter the rerun: %d; rc + sha256(stderr) identical to the baseline (ident pass): %d of %d%s\n", nr, ni, nr, (nd == "" ? "" : "; differ:" nd)
+          printf "  ident pass over the 138: %s%s\n", idl, (nb == "" ? "" : "; not in the baseline replay:" nb)
+        }' "$W/W12-replay-138.tsv" "$W/W12-replay-138-base.tsv" "$W/W12-ident-138.txt"
       echo "## 2. outside the class: rc + sha256(stderr) of base vs the hook under test on 300 sampled commands (ident-300.lst), bash 5.2"
       "${N[@]}" bash "$HERE/ident.sh" "$W/base.sh" "$W/impl.sh" "$HERE/ident-300.lst" 2>&1 | grep -v setlocale | tail -3
       echo "## 3. bash 3.2 (no relaxation): base vs the hook under test on 40 sampled W1 commands (w1-sample40.lst)"
       "${N[@]}" bash "$HERE/ident32.sh" "$BASH32" "$W/base.sh" "$W/impl.sh" "$HERE/w1-sample40.lst" 2>&1 | grep -v setlocale | tail -3
-      hdr; } > "$W/W12-real-traffic.txt"; cp "$W/W12-real-traffic.txt" "$W/W12-replay-138.tsv" "$OUT/"; echo "W12 done" ;;
+      hdr; } > "$W/W12-real-traffic.txt"; cp "$W/W12-real-traffic.txt" "$W/W12-replay-138.tsv" "$W/W12-replay-138-base.tsv" "$W/W12-ident-138.txt" "$OUT/"; echo "W12 done" ;;
 W9) HK="$W/hooks-base"; rm -rf "$HK"; git -C "$ROOT/aria" archive 59e333c hooks | tar -x -C "$W" --transform 's,^hooks,hooks-base,'
     [[ "$(sha256sum < "$HK/secret-guard.sh" | cut -c1-12)" == e83c5e30f2cc ]] || { echo "W9: archived hook is not the baseline"; exit 3; }
     for t in base impl; do rm -rf "$W/tree-$t"; mkdir -p "$W/tree-$t"; cp -r "$HK" "$W/tree-$t/hooks"; done; cp "$W/impl.sh" "$W/tree-impl/hooks/secret-guard.sh"
+    H9=$(hdr)   # before the two suite runs: the first line carries the load at the start, the last line (hdr below) the load at the end (INV-7)
     for t in base impl; do "${N[@]}" bash "$W/tree-$t/hooks/tests/secret-guard.test.sh" > "$W/suite-$t.out" 2>&1; done
-    { hdr; echo "# the suite of aria 59e333c run on a copy with the baseline hook and on a copy with the hook under test (not git checkouts: the cases that read an old hook through git show do not run in either)"
+    { printf '%s\n' "$H9"; echo "# the suite of aria 59e333c run on a copy with the baseline hook and on a copy with the hook under test (not git checkouts: the cases that read an old hook through git show do not run in either)"
       for t in base impl; do echo "## $t"; grep -E '^(PASS|FAIL):' "$W/suite-$t.out"
         grep -E '^  FAIL \[' "$W/suite-$t.out" | python3 -c '
 import sys, re
```

## 附录 B: W13 第 2 节的新编号与改写用例 (编号 / 基线上的结果 / 首次出现于 95cf1de7 之后的提交)

8f66e393 = B.2 第二步 (R2 补强); 382bb001 = TASK-003 第一段 (V14-*)。末行 V7-E15 是改写用例 (绿 -> FAIL); 另一个改写用例 V5-S13b (绿 -> MISSING) 也在 8f66e393 中改动 (`git log -G` 核过)。

| 编号 | 基线结果 | 提交 |
|---|---|---|
| V0-H1-direct-complete | PASS | 8f66e393 |
| V0-H2-case-list | PASS | 8f66e393 |
| V10-N6-filtered-long-line-rows-only | FAIL | 8f66e393 |
| V11-S5-longline-head-verbatim | FAIL | 8f66e393 |
| V11-S6-longline-chinese-line-verbatim | FAIL | 8f66e393 |
| V11-S7-longline-text-verbatim | FAIL | 8f66e393 |
| V14-F1-status-4-falls-back-to-the-baseline-block | FAIL | 382bb001 |
| V14-G1-triggers-return-4-with-the-baseline-reason | FAIL | 382bb001 |
| V14-G2-growth-limit-follows-gmax | FAIL | 382bb001 |
| V14-N1-nocredit-never-runs-credit | FAIL | 382bb001 |
| V14-N2-longline-pattern-is-a-rule | PASS | 382bb001 |
| V2-E17-wsl-mark-keeps-baseline | PASS | 8f66e393 |
| V2-E18-extension-via-stdin-cwd | PASS | 8f66e393 |
| V2-G12-segment-trigger-asks-gate | PASS | 8f66e393 |
| V2-G13-whole-trigger-asks-gate | PASS | 8f66e393 |
| V2-G14-cwd-extension-file-with-entry | MISSING | 8f66e393 |
| V2-G15-cwd-project-without-extension-file | MISSING | 8f66e393 |
| V2-G16-environment-root-before-cwd | MISSING | 8f66e393 |
| V2-G17-wsl-distro-name-closes-gate | MISSING | 8f66e393 |
| V2-G18-wsl-interop-closes-gate | MISSING | 8f66e393 |
| V2-G2-platform:x86_64-pc-linux-gnu:5.2:osrelease-WSL-tag | MISSING | 8f66e393 |
| V2-G2-platform:x86_64-pc-linux-gnu:5.2:osrelease-empty | MISSING | 8f66e393 |
| V2-G2-platform:x86_64-pc-linux-gnu:5.2:osrelease-wsl1 | MISSING | 8f66e393 |
| V2-G2-platform:x86_64-pc-linux-gnu:5.2:osrelease-wsl2 | MISSING | 8f66e393 |
| V2-G2-platform:x86_64-pc-linux-gnu:5.2:osrelease-wsl2-2020 | MISSING | 8f66e393 |
| V2-G2-platform:x86_64-pc-linux-gnu:5.2:three-args | MISSING | 8f66e393 |
| V2-G2-platform:x86_64-pc-linux-gnu:5.2:wsl-mark | MISSING | 8f66e393 |
| V3-E5-budget-2 | FAIL | 8f66e393 |
| V3-G12-time-left-zero-padded | MISSING | 8f66e393 |
| V4-S16-rerun-collect-checkpoint | FAIL | 8f66e393 |
| V4-S17-rerun-whole-checkpoint | FAIL | 8f66e393 |
| V4-S18-rerun-segment-checkpoint | FAIL | 8f66e393 |
| V4-S19-block-text-bytes | MISSING | 8f66e393 |
| V5-E19-deadline-with-term-ignored | FAIL | 8f66e393 |
| V5-S10b-no-judgement-without-timer | MISSING | 8f66e393 |
| V5-S10d-no-judgement-with-dead-timer | MISSING | 8f66e393 |
| V5-S15-job-refuses-outside-group-leader | MISSING | 8f66e393 |
| V6-S20-segment-fallback-text | FAIL | 8f66e393 |
| V6-S21-whole-fallback-text | FAIL | 8f66e393 |
| V7-N10-blank-padded-long-line | MISSING | 8f66e393 |
| V7-N11-lmax-edge-normal | MISSING | 8f66e393 |
| V7-N12-lmax-edge-rows-only | MISSING | 8f66e393 |
| V7-N13-unmeasured-length-rows-only | MISSING | 8f66e393 |
| V7-N7-big-judge-filtered-long-line | MISSING | 8f66e393 |
| V7-N8-whole-branch-returns-big-judge | FAIL | 8f66e393 |
| V7-N9-segment-routes-to-big-judge | FAIL | 8f66e393 |
| V8-D4-growth-text-whole | FAIL | 8f66e393 |
| V8-D5-growth-text-segment | FAIL | 8f66e393 |
| V9-C3-for-statements-rerun | FAIL | 8f66e393 |
| V9-C3b-for-statements-baseline | PASS | 8f66e393 |
| V9-C4-value-limit-in-rerun | FAIL | 8f66e393 |
| V7-E15-credit-as-normal | FAIL | 8f66e393 |

## 附录 C: W13 第 3 节 (MUT_SCOPE=full) 各坏实现的其他红

- BI-2 (CAUGHT): V3-S4-slow-judgement V4-S6-spoofed-tail-0 V5-S9-child-left-behind V5-S13b-nothing-outlives-the-run V5-S15-job-refuses-outside-group-leader V3-E3-anchor-at-hook-start V3-E4-cap-3-at-budget-4 V3-E5-budget-2 V2-E6-flag-from-environment-ignored V5-E19-deadline-with-term-ignored 
- BI-4 (CAUGHT): V4-S3-block-without-text V3-S4-slow-judgement V5-S5-pipe-holder V4-S6-spoofed-tail-0 V0-H1-direct-complete V3-E3-anchor-at-hook-start V3-E4-cap-3-at-budget-4 V3-E5-budget-2 V2-E6-flag-from-environment-ignored V5-E19-deadline-with-term-ignored V0-H2-case-list 
- BI-5 (CAUGHT): V2-G4-empty-extension-file V2-G4-extension-path-is-a-directory V2-G14-cwd-extension-file-with-entry V2-E18-extension-via-stdin-cwd 
- BI-6 (CAUGHT): V2-G12-segment-trigger-asks-gate V2-G13-whole-trigger-asks-gate V2-G17-wsl-distro-name-closes-gate V2-G18-wsl-interop-closes-gate V2-E17-wsl-mark-keeps-baseline 
- BI-7 (CAUGHT): V14-F1-status-4-falls-back-to-the-baseline-block V3-E3-anchor-at-hook-start V3-E4-cap-3-at-budget-4 V3-E5-budget-2 V2-E6-flag-from-environment-ignored V5-E19-deadline-with-term-ignored 
- BI-8 (CAUGHT): V9-C4-value-limit-in-rerun 
- BI-10 (CAUGHT): V7-N8-whole-branch-returns-big-judge V7-N9-segment-routes-to-big-judge 
- BI-12 (CAUGHT): V7-N13-unmeasured-length-rows-only V7-E15-credit-as-normal 
- BI-13 (CAUGHT): V2-E7-no-time-left 
- BI-17 (CAUGHT): V9-C2-references-rerun-cb12 V9-C3-for-statements-rerun V9-C4-value-limit-in-rerun 
- BI-17a (CAUGHT): V9-C4-value-limit-in-rerun 
- BI-17c (CAUGHT): V9-E10-count-axis-read-blocked 
- BI-23 (CAUGHT): V5-S10c-dead-timer-no-judgement V5-S10d-no-judgement-with-dead-timer 
- BI-26 (CAUGHT): V2-E18-extension-via-stdin-cwd 
- BI-33 (CAUGHT): V7-N10-blank-padded-long-line V7-N8-whole-branch-returns-big-judge V7-N9-segment-routes-to-big-judge V7-N13-unmeasured-length-rows-only V14-N1-nocredit-never-runs-credit 
- BI-44 (CAUGHT): V2-E8-ostype-from-environment-ignored 
- BI-45 (CAUGHT): V14-G1-triggers-return-4-with-the-baseline-reason 
