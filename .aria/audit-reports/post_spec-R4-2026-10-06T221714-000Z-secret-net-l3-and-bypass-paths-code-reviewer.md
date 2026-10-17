---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-06T23:41:30.733Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- 被审文件 (`b07f69a`):
  - `proposal.md` 全文 1-443。
  - v3 → v4 词级 diff (`git diff --word-diff c0a6654 b07f69a`), 逐条对读。
  - `baseline-evidence.md` 1-60 与 480-513; 内嵌 stdout 块用脚本与本席复跑结果逐字节比对。
  - `baseline_probe.py` 1-80 (用法与环境)、hook 环境构造 `base_env`、SC-19 全部行 (1247-1401)、22bm / 22bn / 22bo 的成员构造 (约 1580-1595)、22bj (1629)、SC-28 判据 (约 2030-2082)。
  - 三份文件 sha256[:16] 分别为 `f98e719d6036b4f8` / `7da0e53eef5d64da` / `4e0a94aac6e77058`, 与返修报告一致。
- issue 与决策单: `aria-plugin-154.md` (含评论 19339)、`aria-plugin-203.md`、`Aria-221.md` (含评论 25898) 全文; 决策单全文; CLAUDE.md 规则 #6 / #7 / #10 与多远程两条硬约束。
- 源码与规范 (aria `268da8f` / standards `2bc1c4c`):
  - `secret-scan.sh` 全文; `secret-guard.sh` 全文 1-1120; `hooks.json` 三处 secret hook 的 matcher 与 timeout。
  - `secret-guard.test.sh` :11 / :841 / :1620 / :1622 / :2018-2030; `secret-scan.test.sh` :28 / :93 / :102 / :107 / :123 / :145。
  - `secret-hygiene.md` :23 / :96 / :287 / :288 / :319; `aria/VERSION:164`; `.github/secret_scanning.yml:18-22`。
  - 10CG/Aria#199 `detailed-tasks.yaml:336-346`; `.aria/probes/plugin-cache-currency.py` 的全部 print / return。
- 研究笔记: 在四份笔记里检索 NUL 与二进制相关段落 (`secret-scan.md:11` / `:53` / `:60`、`secret-guard.md:37-38` / `:96`)。
- 上一轮: R3 聚合报告全文 (全部 finding 表与主控记录); R3 code-reviewer 报告全文; R2 聚合报告主控记录 (用于严重度口径校准: 基线已有的拦截 / 检出变成放行 = critical; 新功能的验收放过坏实现 = major)。
- 返修材料:
  - `v4-writer-report.md` 全文。
  - `writer-v4-proto/` 下: README、`build_full.sh`、`runprobe.sh`、`final_runs.sh`、`onemut.sh`、`patch_l1.py` (变体表、`compose()`、tight 拷贝构造)、`patch_l3.py` (变体表)、`refs_check.py`、`fuzz_mask.py`、`timing_summary.txt`、`check_counts.py`、`xref_check.py`、`cases_benign_v4.py`、`equiv_reasons.py`, 以及 `mut_summary_v4.txt` 的等价变异节。

**独立复算 (成立的部分, 不计 finding)**

1. **基线证据逐字节复现**:
   - 在私有副本 (aria `268da8f` + standards `2bc1c4c`, 删去子模块 gitfile) 上带真 bash 3.2.57 跑探针: rc=0, stderr 为空, stdout 86047 字节, sha256[:16] = `e588f9e8a57ed720`, 与 `baseline-evidence.md` 内嵌块逐字节相同。
   - baseline-failing 0/202、doc-sync 0/25、其余类别全 yes, 基线形态 holds。主机负载 6-10, 用时 17 分钟。
   - 不带 `WPA_BASH32` 那一次 (`bd8327a7e971cc4e`) 主控已核, 本席未重复。
2. **目标态原型**:
   - 用 `writer-v4-proto` 的补丁脚本在本席目录重建, 两个 hook 指纹 `d94ddf4d6906734f` / `cf2dd857823baf79` 与返修报告一致。
   - 带真 bash 3.2 与 `WPA_REQUIRE_ALL=1` 全量复跑: rc=0, 83988 字节, `7360938f57ee82d0`, 与执笔的 final_T 逐字节相同。
   - 410 行 yes, 30a 按设计 n/a, 目标形态 holds。其中: 29a 50/50; 29b / 29i 584/585 (唯一 FAIL 是测试内 SC-13 的无 git 伪影); 31a 149; 31b 64 = 64; 32c / 32d 在 361 行上一致; 33a flagged=2, 均在归因清单内; 15e-15g 静默。
   - 主机负载 26-37, 用时 44 分钟。
3. **计数与引用自检**: 用执笔的 `check_counts.py` / `xref_check.py` 对本席的基线输出复跑。「共 411 行」相符; 210 个 `SC-n id` 引用 0 个悬空。6 个 SC 条目的 ×N 差异都能由未带计数的行解释 (11x / 11y / 11z、18f / 18h、20g / 20l / 20o-q 等)。
4. **file:line 抽核全部成立** (上列各行):
   - `:342` 引文「其它值 = git grep 没跑成 (如路径不是仓, 退出 128), 停下上报, 不得当作通过」逐字存在。
   - `plugin-cache-currency.py` 的行为与 Tasks 1.12 一致: 成功打印 `OK …` 并返回 0; `##SKIP##` 返回 0; `MALFORMED` / `STALE` / `AHEAD` 返回 1。
5. **W2 的 locale 声称** (glibc 2.36 上实测):
   - 真 bash 3.2.57: `[[ QWERTY == *[a-z]* ]]` 在 `en_US.UTF-8` 与 `zh_CN.UTF-8` 下为真, 在 `C.UTF-8` / `C` 下为假。
   - bash 5.2.15: 四个 locale 全为假。
   - 两个 bash 的 `[[ QWERTY =~ [a-z] ]]` 在四个 locale 下全为假。
6. **时档数字**: W14 第 5 条、W1 与 Impact 里的掩码成本均与 `timing_summary.txt` 一致 (例外见 m2)。

## Findings

### Major

**M1** `0a8380fd` · major · issue · implementation · `proposal.md What.W9`

**Summary**: W9 的 Bash 面扩展判定没有规定「出现点偏移」与「切片」用同一个单位。
- v4 新文字只要求「读取条目的 `tr` / `sed` / `awk`」在 `LC_ALL=C` 下执行 (`:163`), 同时明文允许「`grep -b` 给出的偏移量」作算术操作数 (`:166`)。
- 照字面实现时, grep 在 `LC_ALL=C` 下给出字节偏移, `${s:off}` 却在 hook 自身的 UTF-8 locale 下按字符切片。命令里出现点之前每有一个中文字符, 切片就多吃 2 个字符。多吃的部分一旦越过出现点之后的分隔符, 阶段就被算到出现点之后, 看不到前面的读取器, 结果漏拦。
- 内建 `app.ini` 行对同形命令照拦, 这与 W9 自称的「与内建 `app.ini` 行对同形命令的判定一致」(`:164`, R3 簇 T 主控裁定 2) 相违。
- 原型能拦, 是因为它在 `_sg_ext_pass` 里另写了 Spec 没有的 `local LC_ALL=C`。
- 探针没有「出现点之前含多字节字符」的行。照字面的坏实现在 SC-19 / 20 / 25 / 32 共 57 行全 `yes`, 含真 bash 3.2 的 32c 与第二 locale 的 32d。

**证据**:
- Spec 原文:
  - `proposal.md:163`:「读取条目的 `tr` / `sed` / `awk` 一律在 `LC_ALL=C` 下执行」。
  - `:165`:「建议 `grep -F -i -f <(条目) <(命令文本)` … 命中的出现点从前往后最多检查 64 处」。
  - `:166`:「算术展开的操作数只许是 hook 自己算出的整数 —— 长度、`grep -b` 给出的偏移量」。
  - 全文对切片与阶段计算没有 locale 或单位要求。v3 原文没有 `grep -b` 这句, 也没有字节语义一节; 两处都是 v4 新增。
- 本席变体 `charslice` 只在原型上改一处: 去掉 `_sg_ext_pass` 内的 `local LC_ALL=C`, 改成 `hits="$(LC_ALL=C grep -oFib …)"`。条目读取 (`_sg_ext_entries`, 仍是 `LC_ALL=C`) 与匹配都在 C locale, 切片在 hook 的 locale, 即 Spec 字面。
- 实跑条件: hook 环境 `LANG=LC_ALL=C.UTF-8`, 与探针相同; 条目为 `/srv/wpa-probe-dir`; 命令只当 stdin 文本。下面是原样输出, 列名为 base / proto / charslice。标签里 `C` = 20 个中文字符, `P` = 条目下的路径。

```
ascii20: echo A; cat P; ls   0          2          2
cjk20: echo C; cat P; ls     0          2          0
cjk20: echo C && cat P && ls 0          2          0
cjk20: echo C; sed -n 1,80p P; ls 0          2          0
cjk20: echo C\ncat P\nls     0          2          0
cjk20 in quotes              0          2          0
builtin app.ini, cjk20       0          2          2
ext, script w/ cjk comments  0          2          0
builtin, same script         0          2          2
```

- `charslice` 上跑 `WPA_ONLY=SC-19,SC-20,SC-25,SC-32` 并带 `WPA_BASH32`, 结果: `== w9_charslice: rows=57 non-yes=0`。

**失败场景**:
1. 实现者照 `:163` / `:166`, 只给条目读取与 grep 加 `LC_ALL=C`, 切片沿用 hook 的 locale。Claude Code 会把用户的 `LANG` 传给 hook, 10CG Lab 是中文环境。
2. 运维命令里常见的中文 echo 提示, 或多行脚本里的中文注释行, 位于读取命令之前。
3. 这时列入的路径不再被拦; 内建名单对同形命令照拦。
4. 探针仍全绿, Tasks 1.10 验收照样通过。

**三态** (按下面修法新增的行, 如 19af, `baseline-failing`: 出现点之前含 ≥ 20 个多字节字符, 单行与多行两形, 期望 exit 2):
- 基线: 0, `no`。
- 原型: 2, `yes`。
- `charslice`: 0, 转红。

**修法**:
- W9 写明: Bash 面扩展的出现点定位、掩码、切片与阶段计算用同一单位。可以整段在 `LC_ALL=C` (字节语义) 下进行 (例如函数内 `local LC_ALL=C`), 也可以全程用字符偏移。
- SC-19 补上面的行。
- Tasks 1.8 的「内容形态」类加「偏移与切片单位不一致」这个坏实现。

**注**: 本条的四元组与 R3 ba/M3 (簇 T) 相同。失败形态相同 (读取器与条目被切进不同阶段, 扩展放行而内建拦), 根因不同 (这里是编码单位, R3 是引号)。

**M2** `8fbbee80` · major · issue · testing · `proposal.md What.W11`

**Summary**: v4 把「包裹 × env / printenv 转储」扩到 11 × 2 (22bo), 但这一族的 credit 是否 tight 没有定。
- Spec 没写这一族是否 tight。
- 22bm / 22bn 的 `TIGHT_MEMBERS` 不含它们, 只含 ps / 非 ps 形态与「包裹 × `ps aux`」。
- 探针对「包裹下转储 + 行级过滤」两个方向都没有行。

后果分两侧:
- **放过坏实现**: 有一种实现把转储写成独立行、不进 tight 拷贝, 沿用基线 docker / kubectl env 行的普通 credit。它在 SC-16 / 17 / 22 / 23 / 24 / 25 / 31 共 124 行全 `yes`, 却放行 `nomad alloc exec … env | grep -v PATH`、`ssh host env | grep -v HOME`、`watch env | grep -v X`、`ssh host printenv | sed 's/^/ /'`、`… env | awk '{print $1}'`。这些过滤都不脱敏, 输出就是整份环境。原型因为 tight 拷贝含该备选, 全部拦下。
- **未申报的外溢**: 原型的 tight 拷贝同时覆盖基线 docker / kubectl / podman / lxc exec 的转储, 使基线放行的「锚定 grep 取单个变量」和「只取键名」的 `sed 's/=.*//'`、`cut -d= -f1` 由放变拦。Impact 没有申报这一项。
- **等价变异论证不成立**: SC-22「怎么会红」(`:289`) 与汇总把 `remote_env_split:{docker,kubectl,podman,lxc}` 论证为等价变异; `mut_summary_v4.txt` 的原文是「The mutated program behaves exactly like the correct one」。这只对裸转储成立: 带过滤的转储上原型拦、变体放, 只是没有行能观察到。

本条是 R3 簇 M 的残余 (ba/M2; 主控裁定 8:「tight credit 在进程表族的全部形态上各有行」)。

**证据**:
- Spec 原文:
  - `proposal.md:194`:「同一批包裹下的整环境转储一并拦: 包裹集 = 上面的 11 个 … × {`env`, `printenv`}, 共 22 个成员逐个出行」。
  - `:196`:「credit 用 tight … 逐成员: 家族的每个成员 (10 类 ps 参数、14 个短横写法、15 个 launcher、14 个带参数 / 管道的 launcher 形、8 个绝对路径形、podman、11 个包裹、13 个非 ps 写法) 后接 `| grep -v x` 仍拦 … `/proc` 行不属 tight 族」。
  - 也就是说, 转储族既没有列入, 也没有排除。
- 探针: `TIGHT_MEMBERS = (... PODMAN_FORMS + WRAP_PS + NONPS_FORMS)`; 22bo 只测裸 `env` / `printenv`。本席用脚本检索 `baseline_probe.py`, 「exec … env|printenv … |」形态的串为 0 处。
- 本席变体 `envnotight`: 原型只改一处, tight 拷贝 `_SG_PROCTAB_ALL` 改用去掉 env / printenv 备选的远程正则, 规则行不动。下面是原样输出, 列为 base / proto / envnotight; `E` = env, `PE` = printenv, `S` = ssh, 词元在运行时拼装 (现行 L1 会拦含这些词的命令文本)。第 6 行的标签写错了, 实际命令是 `<S> host <PE> | sed 's/^/ /'`。

```
nomad alloc exec x E         0          2          2
nomad alloc exec x E | grep -v PATH 0          2          0
pct exec 101 -- E | grep -v LANG 0          2          0
S host E | grep -v HOME      0          2          0
watch E | grep -v X          0          2          0
S host PE | sed -n '/=/p' hmm 0          2          0
nomad alloc exec x E | awk '{print $1}' 0          2          0
ps aux | grep -v grep (ctl tight) 0          2          2
```

- `envnotight` 上的探针结果: `== w11_envnotight: rows=124 non-yes=0`, 其中 22bm 91/91、22bn 89/89、22bo 22/22。
- 原型对基线族的外溢 (列为 base / proto):

```
docker exec c E | grep -v PATH 0          2
docker exec c E | grep '^LANG=' 0          2
kubectl exec p -- E | grep '^HOME=' 0          2
docker exec c E | wc -l      0          0
E | grep '^PATH=' (bare)     0          0
docker exec c PE | sed 's/=.*//' 0          2
docker exec c E | cut -d= -f1 0          2
```

- 「等价变异」实测 (列为 base / proto / split_docker / split_kubectl):

```
docker exec c E (bare)       2          2          2          2
docker exec c E | grep -v PATH 0          2          0          2
docker exec c PE | sed 's/^/ /' 0          2          0          2
kubectl exec p -- E | grep -v X 0          2          2          0
```

**失败场景**:
- 照基线体例实现: 实现者按基线 docker / kubectl env 行的写法, 把新增的转储写成独立行、不进 tight 拷贝。Spec 不禁止, 22bo 照样绿。结果是新包裹下的整环境转储只要加一个 `| grep -v X` 就放行。
- 照原型实现: 基线常用的「锚定 grep 取单个变量 / 只取键名」核对被新拦, Impact 与 CHANGELOG 都不披露。这正是 10CG/Aria#221 评论 25898 所说的误拦疲劳。

**三态** (建议的行: 22bo 的 22 个成员各接 `| grep -v x` 期望 2, 各接 `| wc -l` 期望 0):
- 基线: 0, `no`。
- 原型: `yes`。
- `envnotight`: 0, 转红。

**修法**:
- 首选:
  1. W11 写明包裹下的 env / printenv 转储属 tight 族, 理由与 ps 相同 (行级过滤不脱敏)。
  2. 22bm / 22bn 并入这 22 个成员。
  3. Impact「新拦截」申报: 基线 docker / kubectl / podman / lxc exec 的转储加行级过滤 (含只出键名的 sed / cut) 由放变拦。
  4. 改正 SC-22 里关于这 4 个「等价变异」的论证。
- 另一侧: 不 tight, 保持基线语义, 同时把「包裹转储 + 行级过滤」列为 known-limit 并钉行。
- 两侧都必须有决定性的行。

### Minor

**m1** `6ff1d962` · minor · issue · documentation · `proposal.md What.W11`

**Summary**: W11「新增误拦 (成文)」(`:201`) 与 Impact「新拦截」(`:341`) 只申报了「包裹词之后出现进程表形态」的文本提及 (22bj)。还有两类由放变拦, 既未成文, 也未钉行:
- 同一批不锚定的包裹词之后出现 env / printenv 这个词, 包括文本提及, 也包括普通参数词 (venv 目录名、make 目标)。v4 把包裹集扩到了 `watch`、`sh -c`、`bash -c`、不加引号的 `ssh`、`nomad`、`pct`。
- 新增的 `/proc` 读取器 (grep / rg / sed 等) 加上扩大后的 pid 记号, 对含 `/proc/<真实 pid 记号>/environ|cmdline` 的文本做检索或编辑。

**证据** (原样输出, 列为 base / proto; 词元同 M2, 另 `W` = watch、`SD` = sshd、`SW` = stopwatch、`BC` = `bash -c`、`PS` = `ps aux`、`C` = cmdline):

```
commit: S ... E"             0          2
echo: W out ... E"           0          2
echo: SD ... E'              0          2
grep docs: SW PE             0          2
commit: BC E"                0          2
bash -c venv named E         0          2
sh -c make target E          0          2
watch -n5 'ls E'             0          2
bare python3 -m venv E       0          0
grep docs: /proc/self/E      0          2
grep docs: /proc/$$/E        0          2
rg docs: /proc/[0-9]*/C      0          2
sed doc edit: /proc/1/C      0          2
grep docs: /proc/N/C (placeholder) 0          0
```

基线对 docker exec / ssh 下的同类参数词早已误拦 (两侧都是 2); v4 把这一类带到了新的包裹上。22bj 的 6 个成员都是进程表形态。执笔的 76 条良性样本不含上面任何一类。

**失败场景**: 只影响申报与钉行, 行为与原型一致。发版后, 讨论本功能的提交信息、issue 评论、文档检索, 以及 `bash -c "… venv env"` 这类常规命令会被拦; 采用方从 CHANGELOG 看不到这些误拦。

**修法**: W11「新增误拦」与 Impact 各补一句; 22bj 加两例, 一例是 env / printenv 文本提及, 一例是 `/proc` 路径文本检索。也可以把包裹词锚在命令位置 (待复议 27 已有这个备选)。本席 R3 m2 (同一个键) 只收口了进程表形态这一侧。

**m2** `684e9a24` · minor · issue · documentation · `proposal.md What.W9`

**Summary**: v4 按终测更新了 W14 (`:238`) 的时档数字, 但 W9 与 Impact 各留了一处 v3 的旧数:
- W9 `:165`:「原型实测整进程 CPU 约 +6–9 ms (Bash 面 0.052 → 0.061 s)」。W14 的 (f0) 是「0.048 → 0.058 s 与 0.041 → 0.048 s」, 即 +10 / +7 ms。
- Impact `:346`:「200 条扩展条目约 +27 ms CPU / 次调用」。W14 的 (f) 是「Bash 0.049 → 0.072 s、Read 0.042 → 0.067 s」, 即 +23 / +25 ms。

**证据**:
- 在 v3 → v4 的词级 diff 里, `-0.052 +0.048`、`-0.061 +0.058`、`-0.076 +0.072`、`-0.070 +0.067` 都只出现在 W14。
- 本席在 v4 全文里检索 `0.052` / `0.061` / `27 ms`, 只命中 `:165` 与 `:346`。
- `timing_summary.txt` 15 对复跑的记录: f0 Bash `0.048s → 0.058s`; f Bash `0.049s → 0.072s`、Read `0.042s → 0.067s`。

**失败场景**: 只影响引用精度, 实现者的动作不变 (判据写在 W14)。这是 R3 cr/m8「旧计数未同步」的兄弟位置。

**修法**: W9 改为指向 W14 (f0); Impact 改为 +23–25 ms, 或同样指向 W14。

## 上一轮对账

对账依据是 R3 聚合「主控记录」的簇。

**R3 的 critical 与 major**

| R3 席位 · 编号 | 键 (簇) | 状态 | 本席核验证据 |
|---|---|---|---|
| tl/M1 | `4f713847` (Q) | closed | `:52` 在提取内接了 `tr '\000' '\n'`。本席基线复跑中 1c / 1d 为 `silent`, 目标态复跑中为 yes。复跑坏实现 `nul_off`: 1c / 1d 转红 (实得 `alert m=1 {kv-secret-assign=1}`, 期望 `env-line-secret-keyword=3`)。生产信封里是否真带 NUL, 见风险 1 |
| ba/M1 | `8d258b19` (S) | closed | `:166` 的不变量覆盖 W9 / W10 / W12 与 L3。复跑结果: `vx_eval` 使 21z 转红 (payload-1..4 的诱饵出现); `ext_eval` 使 19ab 转红 (`CANARY-EXECUTED(1,2)`); `ext_glob` 使 19ab 转红; `w12_eval` 使 23i 为 0/2; `val_eval` 使 7n 为 0/10 |
| ba/M2 | `8fbbee80` (M) | partially closed | ps 与非 ps 形态已逐成员出行 (22bm 91 个、22bn 89 个), 复跑 `tdrop_launch:sudo` 使 22bm 的 5 个成员转红。但包裹下 env / printenv 转储的 credit 没写、没钉, 拆行坏实现在 124 行全绿, 见本轮 M2 |
| ba/M3 | `0a8380fd` (T) | partially closed | 引号掩码已成文 (`:164`)。复跑 `ext_nomask`: 19z 8/14 错, 19aa 末形转红。`fuzz_mask.py` 复跑: 4000 个串 0 差异, 2743 个安全串与 `_sg_split_top` 0 差异。但「与内建对同形命令的判定一致」在出现点之前含多字节字符时, 会被照 Spec 字面的实现打破, 见本轮 M1 |
| ba/M4 | `ac42f607` (K) | closed | `:195` 的闭集配 22bp / 22bf / 22bh。复跑 `drop_pid:6` 使 22bp 的 thread-self 两成员转红; `pidtok_placeholders` 使 22bf 转红。直测: `cat /proc/$$/environ`、`cat /proc/[0-9]*/cmdline`、`for f in /proc/[0-9]*/cmdline; …`、`cat /proc/1*/cmdline` 基线 0、原型 2; 花括号形两侧都是 0 (已列入 22bh) |
| ba/M5 | `1c49d896` (M) | closed | `:67` 写了作用面闭集。复跑 `step_on:dot:bearer-token` 使 7l 的 `bearer-token:dotted-chain` 转红; `step_on:wl:postgres-url` 使 7m 的 marker / mask 两成员转红 |
| qa/M1 | `eb350937` (M) | closed | 7k / 2e / 2f / 12n / 12o / 19ac 都在探针里, 基线与目标态均符合。复跑 `oldkey_drop:webhook_secret` 使 7k 转红。其余 7 个坏实现来自执笔汇总, 本席未逐个复跑 |
| qa/M2 | `05982c10` (P) | closed | `:356-360` 改为三步, 判据 `rc=0,1`; `:342` 引文逐字相符。`refs_check.py` 复跑: 9 个场景 v4 全对, v3 写法在 5 个跑坏态下真空通过 |
| qa/M3 | `28af0372` (R) | closed | 见 `:168`。复跑 `ext_emptypat` 使 20o / 20p / 20q 转红 (`exit=0,0,2,2,2,2`)。这也消除了本席 R3 风险 1 (BSD 空模式文件) |
| qa/M4 | `44b5bb44` (E) | closed | `:68` 加 32d, Tasks 1.1 / 1.10 同步。用真 bash 3.2 复跑 `ent_range`: 32d 报「3 of 37 rows differ: SC-9:9p SC-10:10a SC-10:10k」。locale 声称经本席实测成立 |
| cr/M1 | `05982c10` (P) | closed | 同 qa/M2 |
| cr/M2 | `eb350937` (M) | closed | 22bo 有 22 个成员; 复跑 `remote_env_split:ssh` 使 22bo 的 `ssh:env` / `ssh:printenv` 转红。`sh -c 'printenv'` / `bash -c env` / `watch env` 改为纳入, 并在 Impact 申报; 直测基线 0、原型 2。带行级过滤的转储另见 M2 |

**R3 minor 中仍未完全处置的**
- `6ff1d962` (R3 tl/m2 · qa/m2 · cr/m2): partially closed。进程表形态的文本提及与同族列举已成文、已钉行 (22bj / 22bh); env / printenv 一侧与 `/proc` 文本检索一侧没有申报, 见本轮 m1。
- `15da802b` (R3 cr/m8): partially closed。点名的旧数已改; 兄弟位置 W9 `:165` 与 Impact `:346` 仍是 v3 的数, 见本轮 m2。
- 其余 R3 minor 本席逐条对照 v4 文字与探针, 均已处置: `cfb2fb14` (两个问题)、`9ce750ed`、`dcba7939`、`6f503728`、`2f76563e`、`f410df76`、`b298cc56`、`44510e65`、`467c8b54`、`5d12116d`、`5e342bfd`、`26e1a7a9`、`4447c607`、`a6304dd1`。其中 `6f503728` 的字节语义只落到了条目读取, 偏移这一侧就是 M1。

## 对执笔人自报薄弱点与请裁项的表态

**§6 自报薄弱点**

1. **同源盲区**: 可接受。本席构造的两个非作者坏实现 (`charslice`、`envnotight`) 分别在 57 行与 124 行全绿 (M1 / M2), 说明 Tasks 1.8 的非作者对抗 review 不能省。建议把「偏移与切片单位不一致」和「转储族的 tight 缺失 / 外溢」加进 1.8 的清单。
2. **体量**: 可接受。但本轮两个 major 都落在新旧文字的接缝上:
   - M1 落在新写的「字节语义」与新写的「`grep -b` 偏移量」之间。
   - M2 落在扩大后的转储包裹集与 tight 逐成员之间。
3. **验收前置变多**: 可接受。Tasks 1.1 写明了取不到就上报, 符合 Rule #10。
4. **回归复跑是精化的**: 可接受。「v3 红过的行必须仍红」是回归的正确判据。
5. **等价变异**: 对 4 个 `remote_env_split` 不可接受。「行为与正确实现完全相同」不成立 (见 M2 证据), 它们只是对现有行不可观察。v3 的 14 个等价变异本席没有逐个复核。
6. **时档是单机比值**: 可接受。
7. **新增 / 反转的已知限制与误拦面**: 方向可接受, 但申报不全 (m1)。76 条良性样本不含「包裹下 env 作普通词」「docker exec 转储加过滤」「`/proc` 路径文档检索」三类。
8. **差分核对的范围**: 可接受。补充一点: fuzz 的字母表全是 ASCII, 覆盖不到多字节内容下的偏移与切片, M1 恰好落在这里。
9. **L3 的 7n**: 可接受, 建议保留。
10. **负载与时长**: 知悉。本席基线复跑 17 分钟、目标态 44 分钟, 负载 6-37。

**§7 甲: 技术级 (待复议 21-30)**
- 21 NUL → 换行纳入: 同意。生产信封是否带 NUL 见风险 1。
- 22 pid 闭集: 同意。
- 23 `sh -c` / `bash -c` / `watch` × 转储纳入: 同意方向。但必须同时裁定 M2 的 tight 归属, 并申报 m1 里的误拦。
- 24 阶段切分与字节语义: 同意方向。字节语义必须扩到出现点偏移与切片 (M1)。
- 25 不执行不变量与 4 个诱饵行: 同意, 5 个 eval 式坏实现复跑全红。
- 26 32d: 同意, `ent_range` 复跑转红。
- 27 文本提及误拦成文: 同意, 并扩到 env / printenv 与 `/proc` 文本检索 (m1)。
- 28 tight 逐成员: 同意, 但必须扩到包裹下的转储 (M2)。
- 29 关闭关键字三步: 同意, `refs_check` 已复跑。
- 30 SC-28 扩到兄弟位置: 同意。
- 17 / 20 的文字更新: 可接受。

**§7 乙: Rule #10 自作主张 1-5**: 列入 handoff 请复议即可, 可接受。其中第 4 条 (三处选「纳入」) 与 M2 相关: 纳入外壳转储时, 没有同步决定它的 credit。

**§7 丙: 未采纳的席位备注**
1. SC-14 的 canary 与 W6 清理的机械判据: 可接受不入 Spec。
2. W5 的 `source` 形状校验: 可接受 (在 matcher 限定下不可达)。
3. MINGW64 / macOS / BSD 未实测: 可接受。建议 10CG/aria-plugin#154 的关单评论如实写「未在 MINGW64 / macOS 验证」, 因为该 issue 的报告环境就是 MINGW64。
4. km 的诸项风险: 可接受。
5. `timing.py` 不打印判据: 可接受, W14 已写明判据。
6. 7.1 超时配方的公开披露: 交 owner。本席维持 R3 的倾向: 首次推送前裁定, 公开文本只写「长命令可致超时即放行」, 不写段数。

## 风险 / 疑问

不计入 finding。

1. **生产信封是否带 NUL**: W1 与 SC-1 1c / 1d 只用了合成内容配真实信封形状。以下两点研究笔记里没有样本, 本席对二进制的只读字符串探针也没得出结论:
   - Claude Code 2.1.285 的 Read 读 `/proc/<pid>/environ` (stat 大小为 0、含 NUL) 时, 是否返回带 `\u0000` 的 `file.content`。
   - Bash 工具是否保留 `env -0` 输出里的 NUL。

   如果平台已经剥掉 NUL 或拒读, 这一行在生产里是无害的空操作, 但「该形态 … 的唯一事后兜底」的表述偏强。可以在 Tasks 1.12 加一条惰性腿 (Read 一个自写的、合成的 NUL 分隔诱饵文件), 或者改措辞。
2. **W2 与 W14 对字符范围的措辞不一致**: W2 要求点分链判定「一律不用字符范围」, 同时给出带范围的整值正则; W14 又说 `[[ =~ ]]` 的 ERE 范围「同基线写法」。在 glibc ≥ 2.28 上两种写法结果相同 (本席实测)。若实现者改用 W2 建议的 POSIX 类 `[[:alpha:]]`, 在 UTF-8 locale 下非 ASCII 字母也算标识符字符。属边缘情况。
3. **Read/Edit 面的大小写折叠**: 原型的 `_sg_ext_path_pass` 不设 `LC_ALL=C`, 靠 `grep -i` 折叠大小写。在 UTF-8 locale 下非 ASCII 字母也会折叠, 与「只折叠 ASCII、两面一致」的文字略有出入。属边缘情况。
4. **主机负载**: 本机是共享的。多个审计席位并行时负载在 30 以上, 目标态全量复跑要 44 分钟。主控复跑时请按此留出时间。
5. **Rule #7 自律记录**:
   - 本席没有生成或使用任何像凭据的值。
   - 抽核 `secret-scan.test.sh` 的行号时, 打印了含公开假夹具的行, 现行 L3 告警 4 处。这些都是测试套件的公开假值, 不是真实凭据, 正是 W7 的动机; 本报告不复述。
   - 现行 v1.74.1 的 L1 两次拦下本席自己的命令 (一次是含 ssh 与 printenv 测试文本的 heredoc, 一次是含 `|printenv)` 的检索正则), 与 m1 / 22bj 同类。改为运行时拼装词元后通过, 没有用 `# guard:ack`。
   - 真仓未做任何 git 写操作: HEAD `b07f69a`、aria `268da8f`、standards `2bc1c4c`, 工作区干净。全部实验在 `scratchpad/audit/post_spec-R4-code-reviewer/` 下进行。

## Verdict

**PASS_WITH_WARNINGS** —— counts `0C/2M/2m` —— **Vote: REVISE**

## 是否足以进入 A.2

不足以。M1 要在 W9 写明出现点偏移与切片用同一单位, 并补一条 SC-19 行; M2 要裁定包裹下 env / printenv 转储的 credit (建议 tight), 补逐成员行, 并改 Impact 申报与等价变异论证。两处都只是改文字加行, 不新增机制, 预计一轮可收; 若不先落进 proposal, detailed-tasks 会把这两种验收放得过的写法原样编进任务。
