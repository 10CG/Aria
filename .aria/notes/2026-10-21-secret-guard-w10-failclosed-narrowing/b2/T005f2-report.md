# TASK-005 修复轮第二段（5f2）执笔席报告（10CG/aria-plugin#217）

证据在 scratchpad 的 `r217impl/t005f2/`：`pre/`（改前副本）、`edit5f2.py`（改动脚本，每处替换都断言恰好命中 1 次）、`prove-w1.sh` 与 `prove-w1-*.txt`、`prove-34.sh` 与 `prove-34.txt`、`inv4-*`、`cs/`、`bad/`、`expect.md` 与 `expect-proofs.md`（预期，开跑前写）、`runall2.sh`、`runs/`。没有 commit。

## 一、各项结论（一句话）

1. hook：只改了 :796 这一行注释（与 5f 版相比 diff 正好 1 行），宽度 151 -> 152 列（该段最宽 155）；新的 sha256 前缀是 834dee6db0d0。
2. 测试侧 WSL 判据：写了四份独立实现：helper 与 sc-direct.sh 里的 `wslmark`、套件里两处共用的 `sg_w10_wslfs`、sc-cases.sh 里的 `wslmark`。在 W1a-d 和另加的 3 种假表上，它们与 hook 的 `_sg_relax_nowslfs` 逐种一致，5 个 bash 上都是 7/7。在本机真实路径上四份都判「没有」，与旧的 `-e` 判据和 hook 的结果相同。
3. V15-T2：锚点改成「现在减 2.0 s」，断言 0 < `_SG_LEFT` <= 1.0。实现上 helper 与 sc-direct.sh 都 PASS（0.986、0.990）；B5、B7、B8 在两处都 FAIL [static][value]（值约 3.0）。
4. INV-4 静态清单：`_sg_relax_nowslfs` 已加进套件与 sc-cases.sh 的清单，也加进了两处的期望编号清单；套件头注释的计数随之改成 981 (975)、150。B10（把这个函数挪到闸门之下）上，新清单的 V11-S1-above-gate:_sg_relax_nowslfs 变红，实现上是绿的；5f 版套件在 B10 上 9/9 全绿。
5. `impl/w14-mutants.py`：只改了 `IMPL_SHA12`，50ce186a28c9 -> 834dee6db0d0。
6. commentsync：照 5f 的做法从 HEAD 版重新导出。先用 5f 的 hook 和套件重放了一遍，产物与 5f 的文件逐字节相同。第 1 条那句已进站点 10 的 new 清单，旧句进了 untrue（标 p）。target、baseline、proto 都是 GREEN，四个构造都是 RED（77、59、58、57）。
7. 各轮实跑全部达到预期。5.1.16 的 W10 首轮计时批是 void（尾负载 2.09），自动低负载重跑后判过；套件模式 P-0 首轮 NOT-JUDGED，低负载重跑后 GREEN。

## 二、改动明细

### 1. hook :796（逐字）

- 改前：`# returns 4 instead and keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE, and _sg_per_segment_eval re-runs the W10 pass with the relaxed rules`
- 改后：`# returns 4 instead and keeps the baseline reason and mode in _SG_OV_PAT / _SG_OV_MODE; _sg_per_segment_eval re-runs the W10 pass with the relaxed rules`
- 依据：`_SG_OV_PAT` 存的是原因串（:755 / :779，例如 "the command is longer than $_SGV_SMAX characters after variable expansion"），`_SG_OV_MODE` 存 whole 或 segment；回退时由 `_sg_emit_blocked "$_SG_OV_PAT" "$cmd" "$_SG_OV_MODE" oversize` 重新写出文案（:1704）。这与 What 7 补充 2 第 4 处（:724-:725）同义。措辞为什么这样取舍，见第六节第 1 条。

### 2. 测试侧 WSL 判据

四份函数体相同，只有函数名和头注释不同。返回状态 0 表示有 WSL 标记，对应 hook 返回 1：

```
  local t l d="${2:-/proc/sys/fs/binfmt_misc}"
  t=$(cat -- "${1:-/proc/self/mounts}" 2>/dev/null) || return 0
  awk -v d="$d" '$2 == d && $3 == "binfmt_misc" { m = 1 } END { exit !m }' <<< "$t" || return 1
  l=$'\n'$(ls -A -- "$d" 2>/dev/null); [[ $l == *$'\n'WSLInterop* ]]
```

与 hook 的写法刻意不同：挂载表用 cat 整个读出，读不出就算「有」；用 awk 按字段比对挂载点和文件系统类型；看目录用 ls，不用 glob。只有挂载表里写明 DIR 上挂着 binfmt_misc 时才去列 DIR，所以不会触发自动挂载。不 source、也不调用 hook。两个参数（挂载表路径、目录）可省略，默认值就是真实路径，只为验证而设。

- helper :73 与 sc-direct.sh :51：前面加 `wslmark()`（4 行头注释加上面的函数体），原行改成 `OSR=$(cat /proc/sys/kernel/osrelease 2>/dev/null); WSLM=''; wslmark && WSLM=wsl`。两个文件的改动行逐行相同（各 -5 +15，含 V15-T2），符合 INV-2。
- 套件：在 `sg_w10_relax_rule` 前加 `sg_w10_wslfs()`。:375 改成 `WSLF=no; sg_w10_wslfs && WSLF=yes`，:2933 改成 `sg_w10_wslfs && wpa_rx6_wslf=yes`。
- sc-cases.sh：:47 前加 `wslmark()`，原行改成 `WSLF=no; wslmark && WSLF=yes`。头注释 :9 原来写的是「no /proc/sys/fs/binfmt_misc/WSLInterop」，改成新判据的说法，该段重排为 :8-:12（都不超过 155 列）。

### 3. V15-T2（helper 与 sc-direct.sh 同样改）

- 注释 (b) 改成两行：「with the anchor 2.0 s back and budget 3 the judgement inside the job sees 0 < left <= 1.0 s: a fresh anchor in the gate, the run or the job (a bad implementation) gives about 3 s there, and a slow host only makes the value smaller (it reaches 0 only after 1.0 s from here to the judgement)」。
- `e-2.5` 改成 `e-2.0`；`l+0 <= 0.5` 改成 `l+0 <= 1.0`；chk 文案里的 2.5 / 0.5 改成 2.0 / 1.0。

### 4. INV-4

- 套件 :341 的 for 清单与 `SGW_EXP_STATIC`，sc-cases.sh :184 的 for 清单与 `EXP_STATIC`：都在 `_sg_relax_platform` 之后加 `_sg_relax_nowslfs`，与它在 hook 里的位置一致。
- 套件头注释：Coverage 980 (974) 改成 981 (975)，W10 用例数 149 改成 150。SC-13 用这个数核对，整轮实跑总数正好是 975。
- helper 与 sc-direct.sh：`grep -n` 确认这两个文件里没有这份清单（它们靠 need 判断，缺函数时报 MISSING），所以没改。

### 5. w14-mutants.py

只改了 `IMPL_SHA12 = "834dee6db0d0"`。

### 6. commentsync.py

做法：取 HEAD 版，用 `t005f/cs/derive-5f.py` 和新的 hook、新的套件导出。与 5f 版相比，只差 FIX5_HOOK 这一行。

- 各站点：hook 站点 1 删 2 增 2；站点 2 删 1 增 1；站点 5 删 1 增 1；站点 10 删 1 增 2（5f 时是删 0 增 1）；套件站点 9 删 2 增 2。
- 站点 10 的 old（标 p）：「When the relaxation is in effect ... _sg_vx_pass returns 4 instead and keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE, and _sg_per_segment_eval re-runs ... _SGV_GMAX;」
- 站点 10 的 new：「When the relaxation is in effect ... _sg_vx_pass returns 4 instead and keeps the baseline reason and mode in _SG_OV_PAT / _SG_OV_MODE;」，以及 5f 已加的「The one exception (What 4): ...」。
- derive 日志有两类记录：
  - 新单元「_sg_per_segment_eval re-runs the W10 pass with the relaxed rules (_SG_RELAXED: ..., _SGV_GMAX;」是原型 run 的子串，按规则略过。
  - 套件里有两段注释在所有站点之外改动了：头注释计数和新函数的头注释。这与 5f 同类。

## 三、四项证明

1. 测试侧判据与 hook 一致（prove-w1.sh；在 5 个 bash 上各跑一遍；四份实现都从各自文件里抽出函数来跑，hook 在单独的子 shell 里 source）。

| 情形 | hook 返回（判定） | 四份测试侧返回（判定） |
|---|---|---|
| W1a：autofs 挂载点，目录里有 WSLInterop | 0（没有） | 1（没有） |
| W1b：binfmt_misc，目录里有 WSLInterop-late | 1（有） | 0（有） |
| W1c：binfmt_misc，目录里没有 WSLInterop* 项 | 0（没有） | 1（没有） |
| W1d：挂载表读不出 | 1（有） | 0（有） |
| 另加 x1：binfmt_misc，目录里有 WSLInterop | 1（有） | 0（有） |
| 另加 x2：挂载表为空 | 0（没有） | 1（没有） |
| 另加 x3：binfmt_misc 挂在别的目录 | 0（没有） | 1（没有） |

   - 5 个 bash 上都是 7/7 一致，测试侧 stderr 都是 0 字节。
   - 本机真实路径：hook 0，旧的 `-e` 判「没有」，四份测试侧都返回 1（没有）。本机挂载表里没有任何 binfmt_misc 行。
   - 另有一行仅供参考的情形（拿目录当挂载表）结果不一致，见第六节第 2 条。
2. V15-T2（prove-34.txt；bash 5.2，relax 模式；负载 1.08 -> 1.15）：
   - 实现：helper PASS（0.985854），sc-direct.sh PASS（0.989806）。
   - B5（作业里重取锚点）：FAIL [static][value]（2.999859 / 2.999906）。
   - B7（run 里重取锚点）：FAIL [static][value]（2.999920 / 2.999946）。
   - B8（准入门里重取锚点）：FAIL [static][value]（2.995964 / 2.996056）。
   - B5、B7、B8 是用 5f 的 mkbad.py 在新 hook 上重新生成的。
3. INV-4。B10 = 新 hook 把 `_sg_relax_nowslfs`（7 行）从 :838 挪到闸门块（:1064-:1066）之后。
   - 新 sc-cases.sh（`SC_ONLY='^V11-S1'`，`SC_DIRECT=0`）：实现上 8 个都 PASS；B10 上 nowslfs FAIL，其余 7 个 PASS。
   - 新套件：把 hooks 目录拷进 scratchpad，换成 B10 后跑 `SG_W10_ONLY='^V11-S1'`。实现上 10/10；B10 上 9/10，nowslfs FAIL [value]。
   - 5f 版套件在 B10 上 9/9 全绿：旧清单根本没有这一项。
   - 5f 版 sc-cases.sh 在 scratchpad 里没跑起来（SETUP: cannot build the input ext-read-cwd，它需要同目录下的文件），所以没有取得这一行。

## 四、各轮预期与结果（预期在开跑前写入 expect.md；编排脚本 runall2.sh：每步都等 1 分钟负载降到 1.2 以下才开跑，一次只跑一步）

| 轮次 | 预期 | 结果 | 首尾负载（1 分钟） |
|---|---|---|---|
| W10，5.0.18 | PASS 150/150，SKIP 0 | PASS 150/150，FAIL 0，SKIP 0，计时批判过 | 0.72->0.93 |
| W10，5.1.16 首轮 | 同上 | PASS 121，SKIP 29 [void]，FAIL 0；计时批 void（尾负载 2.09） | 0.93->2.09 |
| W10，5.1.16 重跑 | 同上 | PASS 150/150，FAIL 0，计时批判过 | 1.03->1.14 |
| W10，5.2.15 | 同上 | PASS 150/150，计时批判过 | 1.14->1.20 |
| W10，5.3.20 | 同上 | PASS 150/150，计时批判过 | 1.18->0.93 |
| W10，3.2.57 | PASS 83，SKIP 67 [platform] | PASS 83，SKIP 67 全是 [platform]，FAIL 0，计时批判过 | 0.93->1.28 |
| 整轮，PATH 上的 bash | 975/975，SC-13 绿 | PASS 975/975，FAIL 0，SKIP 0（SC-13 计在总数里），计时批判过 | 1.08->1.47 |
| 整轮，`WSL_DISTRO_NAME=Ubuntu` | FAIL 0，SKIP 只许 [void]，6 组走基线支 | PASS 975/975，FAIL 0，SKIP 0；6 组的分支说明行是 baseline branch（PATH 那一轮是 relaxed）；计时批判过 | 1.05->1.93 |
| sc-cases.sh（基线 59e333c） | PASS 151，V0-H2 149 | PASS 151，FAIL / MISSING / SETUP / SKIP 都是 0，V0-H2「all 149 expected case ids of mode relax reported once」，计时批判过 | 1.12->1.33 |
| run-mutants，v31 模式 | 63 CAUGHT，P-0 GREEN | 63 CAUGHT，P-0 GREEN，扰动轮 0 个不如预期 | 1.19->2.22 |
| v31 模式 P-0 单跑（为 INV-7 补跑） | GREEN | GREEN，0 个不如预期 | 1.14->2.23 |
| run-mutants，套件模式 | 63 CAUGHT，P-0 GREEN | 63 CAUGHT；P-0 NOT-JUDGED，扰动轮记 1 个不如预期（就是 P-0 没判） | 1.13->1.98 |
| 套件模式 NOT-JUDGED 重跑（P-0） | GREEN | GREEN，0 个不如预期 | 1.10->1.35 |
| 套件模式 P-0 单跑 | GREEN | GREEN，0 个不如预期 | 1.12->0.65 |
| w14.sh | 31 个全抓住 | as predicted 26，by the added case 5，elsewhere 0，not judged 0，NOT CAUGHT 0 | 0.65->1.12 |
| commentsync | target / baseline / proto GREEN，四个构造 RED | 都如预期（RED 77、59、58、57，与 5f 相同） | - |

5 个 bash 文件在 5 个 bash 上 `bash -n` 都通过，stderr 0 字节。

## 五、首尾负载

- 会话开始时 3.22（当时还没跑任何实验）。各步开跑前都 < 1.2。最后 ALL DONE 时 1.12，v31 模式 P-0 补跑结束时 2.23。
- 步骤级尾负载 >= 2 的有三处：
  - w10-5.1.16 首轮（2.09）：计时批按设计 void，已重跑判过。
  - mut-v31 和它的 P-0 单跑（2.22、2.23），见第六节第 4 条。

## 六、未做或拿不准的项

1. **:796 的措辞**：
   - What 7 补充 2 第 4 处的说法是「the baseline reason string and mode are kept in ... -- not a text」。
   - 照搬「reason string and mode」：保留原来的 ", and" 时这一行 163 列；把 ", and" 换成 "; " 也有 159 列。两种都超过该段的 155 列。
   - 任务书规定 hook 只能改这一行，所以用了「reason and mode」，并把 ", and" 换成 "; "，得 152 列。
   - 如果要逐字写「reason string」，就得允许重排相邻的行（会改不止一行），请主控定。
2. **拿目录当挂载表时，hook 与规格的说法不一致**：
   - hook 的 `< "${1:-/proc/self/mounts}"` 只能抓到「打不开」。目录能打开但读不出来，hook 会把它当成「可读、没有 binfmt_misc」，返回 0（没有标记）。
   - 任务书写的语义（读不出就算有）和测试侧的 cat 都判「有」。
   - 真实的 /proc/self/mounts 不会是目录，W1a-d 也不涉及这种情况。hook 不在本段的改动范围内，没有动，记在这里请复议。
3. **INV-4 清单的位置**：任务书说清单在 helper / sc-direct.sh / 套件里；`grep -n` 的结果是在套件与 sc-cases.sh 里。这两个文件都在允许范围内，已改。helper 与 sc-direct.sh 里没有这份清单，没有新增。
4. **v31 模式 P-0 的 INV-7**：
   - 两次都由 harness 自己判 GREEN（它自带负载闸，负载过高时会报 NOT-JUDGED）。
   - 但这一步收尾时的 1 分钟负载是 2.22 和 2.23。两次开跑负载都 < 1.2，负载主要是这次实验自己拉起来的（P-0 要整个跑一遍 sc-cases）。
   - 按「首尾负载都 < 2 才算数」的字面规定，这两次的计时部分不算数。5f 那一轮是 1.05->1.75。没有再试第三次，请主控定是否需要在更空闲的时段补跑。抓坏实现（CAUGHT）的结论不受影响。
5. **输出标签没改**：套件 :2936 附近的摘要标签「WSLInterop $wpa_rx6_wslf」、helper / sc-direct.sh 里 SKIP [platform] 文案中的「WSLInterop」，现在实际表示「文件系统里有 WSL 标记」（有 WSLInterop* 项，或挂载表读不出）。任务书只要求同步注释，这些是输出标签，没有改。
6. **文件范围外可能需要同步的地方，都没改也没逐字核对**：v31/README.md :41（讲 sc-cases.sh 判据的那行，grep 命中 WSLInterop）；proposal 和计划里的计数（980/974、149）；V15-T2 的 2.5 / 0.5。
7. **新注释的行宽与覆盖**：新函数的头注释最宽 156-158 列（这些测试文件里本来就没有统一的段宽）。commentsync 不检查这些注释。
8. **清理**：runall2（PID 1763550，自记在 runs/runall.pid）自己跑完退出了，monitor 已到期。用 ps 核对过，没有残留进程，没有杀任何进程。
9. **工具调用**：共 31 次（含本次写报告）。
