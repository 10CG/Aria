# TASK-003 第一段报告：非作者独立坏实现（10CG/aria-plugin#217，QA 席）

## 0 结论（每项一句）

1. 盲构造：31 个坏实现（Q-1 至 Q-31），每个是实现加一处像真实执笔错误的改动；What 1 八个、What 2 八个、What 3 四个、What 4 三个、What 5 三个、时间预算三个、锚点两个。生成器逐字替换，替换前断言原文恰出现一次，31 个都过且 `bash -n` 通过。
2. 第一轮（补用例之前，只跑预先写下的用例）：按预期抓住 26，别处抓住 2（Q-7、Q-29），未抓住 3（Q-15、Q-22、Q-31），未判 0。
3. 缺口补了 5 个定向直调用例 `V14-N1 / N2 / G1 / G2 / F1`，不依赖负载；在实现上绿，在各自的坏实现上红，红的原因就是那处错误。
4. 终轮（补用例之后）31 个坏实现：26 个按预期抓住，5 个由补的用例抓住，别处抓住 0，未抓住 0，未判 0。
5. 实现上的各轮全绿：套件 `SG_W10_ONLY=.` PATH 上的 bash 5.2.15 为 141 PASS / 0 FAIL；`SC_BASH=bash-3.2.57` 为 78 PASS + 63 SKIP（全部 `[platform]`）/ 0 FAIL；`v31/sc-cases.sh` 142 PASS / 0 FAIL；整套件（git 检出，含 SC-13）966/966 PASS；`commentsync.py --suite-only … target` GREEN。
6. 没动 hook（sha256 前缀仍是 af4658b6f935），没 commit，只改了允许的文件。
7. 拿不准与未做的见第 7 节；最要紧的一条：Q-16、Q-17、Q-24 只被计时类 e2e 用例抓住，负载 >= 2 时这些用例 SKIP，这三个坏实现在高负载下不会被抓住，我没有为它们补不依赖负载的用例。

## 1 冻结物与顺序

| 文件 | sha256 | 冻结时刻 |
|---|---|---|
| `t003a/w14-mutants.py` | `4327121c903c43995e1b84fe62608d03ea92b398c3663989b749a9529853a5e4` | 2026-10-24T19:04:12Z，阶段 1 结束 |
| `t003a/list.md` | `1cfb36dd3819c3cd2198eff4984a068e1a0376269c546cf1a6cd55e75b388361` | 同上 |
| `t003a/predict.md` | `627580356dcde4e9b108908be687dacebb6290b05f0adc5db4aadf8ef99e3664` | 阶段 2 结束，先于任何一次套件运行（`t003a/FROZEN.sha` 里三行） |

之后这三个文件没有改过。`v31/impl/w14-mutants.py` 与冻结版逐字节相同（sha256 同上）。

阶段 1 只读了：实现与基线的 diff、proposal What 1-7、detailed-tasks 的 INV 与 TASK-003、`run-suite.sh` 头注释。没有读 `hooks/tests/` 下任何东西、`v31/sc-cases.sh`、`v31/sc-direct.sh`、`v31/mutants.py`、`v31/W13-*`、主仓 `b2/`、`pp-r2-seats/`、`evidence/`。（`ls` 过 scratchpad 的目录名，没读里面的任何文件。）

阶段 2 读了：套件 W10 移植块块首注释（`:136-195`，含各组用例编号清单与 `[reference]` 的说明）、`sg_w10_cases` 的前 78 行（`:359-436`，含 e2e 用例调用行，也含它自己的准备代码，没读 `sg_w10_identity/deadline/outcome` 的函数体）、helper 头注释（`:1-24`）与 helper 里含用例编号的行（grep，每行只看前 120-170 字符）。要如实交代一点：grep 出的编号行带出了少量断言片段（例如 V3-G12 的期望串 `"0 2.050000"`、V8 夹具的形状、`one` 调用的期望返回码与文案种类），我的部分预测因此比只看编号更有把握，预测并非完全「盲」；坏实现本身在此之前已冻结，没有受影响。

## 2 清单、预测与逐个结果

「预计」是 `predict.md` 里写下的用例与原因标签；「第一轮」是补用例之前的实际；「终轮」是补用例之后。完整的改动说明（改了什么、哪类执笔错误、什么输入形状、露出来是什么样）在 `t003a/list.md`；逐行的原始结果在 `v31/impl/W14-independent-mutants.txt`。

| 编号 | 改动（执笔错误类） | 预计抓住的用例 [标签] | 第一轮实际 | 第一轮分类 | 终轮 |
|---|---|---|---|---|---|
| Q-1 | 平台：次版本上限 `<= 3` 写成 `< 3`（差一） | V2-G2-platform:…:5.3 [status] | 红 [status] | 按预期 | 按预期 |
| Q-2 | 平台：主版本 `== 5` 写成 `>= 5`（比较符） | V2-G2-platform:…:6.0 [status] | 红 [status] | 按预期 | 按预期 |
| Q-3 | 平台：构建串 `…-linux-gnu*` 放宽成 `…-linux-*`（漏检查） | V2-G2-platform:x86_64-alpine-linux-musl:5.2 [status] | 红 [status] | 按预期 | 按预期 |
| Q-4 | 平台：内核串 `*[Mm]icrosoft*` 写成 `*Microsoft*`（大小写） | V2-G2-platform:…:5.2:osrelease-wsl2-2020 [status] | 红 [status] | 按预期 | 按预期 |
| Q-5 | 准入门：平台串取 `$MACHTYPE` 而不是 `BASH_VERSINFO[5]`（信环境） | V2-G3b-gate-uses-build-facts、V2-E8-ostype-from-environment-ignored [value]/[status]/[bytes] | G3b 红 [value]；E8 红 [fallback] | 按预期 | 按预期 |
| Q-6 | 准入门：`_sg_relax_noext` 的 `\|\|` 写成 `&&` | V2-G4-project-without-extension-file、V2-G15-… [status] | 两条红 [status] | 按预期 | 按预期 |
| Q-7 | 触发点：分段触发点 `if _sg_relax_ok` 写成 `if false`（漏一个触发点） | V2-G12-segment-trigger-asks-gate [status]/[value]/[judged] | G12 绿；整轮红在 V6-S20-segment-fallback-text、V9-E11-tmax-in-rerun | **别处抓住** | V14-G1 抓住 |
| Q-8 | 准入门：`-e` 写成 `-f`（目录态当没有扩展） | V2-G4-extension-path-is-a-directory [status] | 红 [status] | 按预期 | 按预期 |
| Q-9 | 重跑：增长限逐变量按已被改写的 `s` 重算，不用入口的 `${#1}`（BI-9 的反面） | V8-D3-growth-8193-plain / braced [status]/[rc]/[value] | 两条红 [status] | 按预期 | 按预期 |
| Q-10 | 重跑：for 语句计数上限没取消（只取消了赋值的） | V9-C3-for-statements-rerun [count]/[value] | 红 [value] | 按预期 | 按预期 |
| Q-11 | 重跑：`${NAME}` 拼写的 8 次替换上限没取消 | V9-C2-references-rerun-cb12 [value] | 红 [value] | 按预期 | 按预期 |
| Q-12 | 重跑：`$NAME` 拼写的 8 次上限没取消 | V9-C2-references-rerun-c12 [value] | 红 [value] | 按预期 | 按预期 |
| Q-13 | big_judge：`max > _SGV_LMAX` 写成 `>=`（差一） | V7-N11-lmax-edge-normal [rc]/[kind]/[status] | 红 [kind] | 按预期 | 按预期 |
| Q-14 | big_judge：读行漏 `IFS=` | V7-N10-blank-padded-long-line [rc]/[kind]/[status] | 红 [kind][status] | 按预期 | 按预期 |
| Q-15 | judge_one：nocredit 分支挪到 credit 计算之后（顺序颠倒） | V7-E14-long-line-from-expansion [kind]/[wall>hi]（低确信） | 绿；整轮无红 | **未抓住** | V14-N1 抓住 |
| Q-16 | 作业：计时器睡整个预算而不是剩余时间 | V3-E3-anchor-at-hook-start [wall>hi] | 红 [wall>hi] | 按预期（计时类） | 按预期 |
| Q-17 | 作业：丢掉 `exec 2>/dev/null` | V6-E2-deadline-fallback-bytes、V6-S20-… [bytes] | E2 红 [bytes]；S20 绿 | 按预期（计时类 e2e） | 按预期 |
| Q-18 | 作业：回放的拦截文案少最后一个换行 | V4-S19-block-text-bytes [bytes] | 红 [bytes] | 按预期 | 按预期 |
| Q-19 | 作业：去掉 `wait` 之后的整组 kill | V5-S13b-nothing-outlives-the-run、V5-S9-child-left-behind [leftover]/[wall>hi] | S13b 红 [leftover]；S9 红 [wall>hi] | 按预期 | 按预期 |
| Q-20 | 回落：分段触发点存了整串的原因串（相邻两行复制粘贴） | V6-S20-segment-fallback-text [bytes]/[text]/[fallback] | 红 [bytes] | 按预期 | 按预期 |
| Q-21 | 文案：分段 growth 文案用了整串措辞 | V8-D5-growth-text-segment [text] | 红 [text] | 按预期 | 按预期 |
| Q-22 | 文案：longline 调用里 `$pat` 与 `$seg` 对调 | 无（预测的缺口） | 整轮无红 | **未抓住** | V14-N2 抓住 |
| Q-23 | 文案：longline 的 `Command was` 回显 `${seg:0:200}` 而不是 `${command:0:200}` | V11-S7-longline-text-verbatim [text]（低确信） | 红 [text] | 按预期 | 按预期 |
| Q-24 | 锚点：在 `_sg_vx_collect` 开头重取 `_SG_P0` | V3-E3-anchor-at-hook-start [wall>hi] | 红 [wall>hi] | 按预期（计时类） | 按预期 |
| Q-25 | 锚点：`_SG_RELAXED` 初值取自环境 | V2-G11-flag-not-from-environment、V2-E6-… [value]/[bytes]/[wall>hi] | G11 红 [value]；E6 红 [bytes][wall<lo] | 按预期 | 按预期 |
| Q-26 | 预算：封顶 `min(预算, 3)` 写成 `max` | V3-G10-cap-3、V3-E5-budget-2、V3-E4-… [value]/[wall>hi] | G10 红 [value]；E5、E4 红 [wall>hi] | 按预期 | 按预期 |
| Q-27 | 预算：剩余时间 `%d.%06d` 写成 `%d.%d`（单位 / 格式） | V3-G12-time-left-zero-padded [value]/[status] | 红 [value] | 按预期 | 按预期 |
| Q-28 | 预算：去掉「时钟回拨不延长截止」的封顶 | V3-G9-clock-backwards [value]/[status] | 红 [value] | 按预期 | 按预期 |
| Q-29 | 回落：`_sg_per_segment_eval` 里 `-eq 4` 写成 `-eq 3`（退出码映射） | V6-E2、V6-S20、V6-S21 [status]/[rc]/[fallback] | E2 红 [bytes]（标签与预测不符）；S20、S21 绿 | **别处抓住** | V14-F1 抓住 |
| Q-30 | 准入门：去掉 `_sg_relax_left` 检查（hook 输出层面等价，我预测只有直调看得到） | V2-G6-no-time-left、V2-G7-no-anchor、V2-G8-budget-0 [status] | 三条红 [status] | 按预期 | 按预期 |
| Q-31 | 重跑：增长限用 `_SGV_SMAX` 代替 `_SGV_GMAX`（当前两者同为 8192） | 无（预测的缺口，潜伏） | 整轮无红 | **未抓住** | V14-G2 抓住 |

预测命中情况：我预测的两个确定缺口（Q-22、Q-31）都对；低确信的缺口里 Q-15 对，Q-4、Q-17、Q-23 其实被抓住；没料到的是 Q-7 与 Q-29。Q-7 的预测用例 V2-G12 在 `if false` 坏实现上仍是绿的（我按纪律没读它的断言体，推测它只验准入门关闭那一极）。Q-29 的 V6-E2 红了，红的原因就是这处错误，但标签是 [bytes] 而不是我写的 [status]/[rc]/[fallback]；按任务书「标签一致」的字面判为别处抓住，并且当时只有计时类 e2e 抓得到它，所以也补了用例。

第一轮另在 Q-7、Q-15、Q-22、Q-31 上各跑了一次 `SG_W10_ONLY=.` 整轮：Q-7 红在 V6-S20、V9-E11（与分段触发点相关，不是无关断言），其余三个整轮没有任何红。其余坏实现没有跑整轮（见第 7 节）。

## 3 缺口与补的用例

五个用例都是直调类，写进 helper `hooks/tests/lib/secret-guard-w10-direct.sh` 与 `v31/sc-direct.sh`（同一份代码，插在 N 组最后、`else nobelow $N_IDS; fi` 之前），编号进 helper 的 `RELAX_IDS` 与 `N_IDS`、`sc-direct.sh` 的 `N_IDS`、套件的 `SGW_EXP_DIRECT`（V0-H2 清单）与 `sc-cases.sh` 的期望编号清单。全部不依赖负载。

| 用例 | 对应缺口 | 在实现上 | 在坏实现上 |
|---|---|---|---|
| V14-N1-nocredit-never-runs-credit | Q-15：nocredit 拦截先白算了 O(n²) 的 credit，结论不变，只有「credit 被算过」能区分 | PASS（credit-skipped） | Q-15 红 [judged] |
| V14-N2-longline-pattern-is-a-rule | Q-22：longline 文案里 `Matched pattern:` 该是规则，不是上万字符的副本；`one` 一类用例只验返回码与文案种类 | PASS（文案 1171 字节，匹配的是规则） | Q-22 红 [text] |
| V14-G1-triggers-return-4-with-the-baseline-reason | Q-7：两个触发点在准入门打开时都返回 4，并各存各的基线原因串（顺带管住 Q-20 那类复制粘贴） | PASS | Q-7 红 [status][text] |
| V14-G2-growth-limit-follows-gmax | Q-31：把 `_SGV_GMAX`、`_SGV_SMAX` 拉开，增长限只能随 GMAX | PASS | Q-31 红 [status] |
| V14-F1-status-4-falls-back-to-the-baseline-block | Q-29：重跑失败（状态 4）在 `_sg_per_segment_eval` 里落成基线块（状态 2 与原因行），与主机负载无关 | PASS | Q-29 红 [status][text] |

用例代码（缩进是它们在 N 组里的实际缩进）：

```bash
    if sel V14-N1-nocredit-never-runs-credit; then   # Q-15
      if need _sg_compute_credit; then
        r=$( _sg_compute_credit() { : > "$X/n14a.mark"; return 0; }; command="$rd"; _sg_judge_one "$rd" whole nocredit >/dev/null 2>"$X/n14a"; echo "$? $(kindf "$X/n14a") $([[ -e "$X/n14a.mark" ]] && echo credit-run || echo credit-skipped)" )
        [[ $r == "2 longline credit-skipped" ]]; chk $? V14-N1-nocredit-never-runs-credit "nocredit on a matching line over ${_SGV_LMAX:-8192}: status/text/credit [$r] (want [2 longline credit-skipped]); the credit must not be computed before the longline block" "[judged]"
      else miss V14-N1-nocredit-never-runs-credit; fi
    fi
    if sel V14-N2-longline-pattern-is-a-rule; then   # Q-22
      command="$rd"; _sg_judge_one "$rd" whole nocredit >/dev/null 2>"$X/n14b"; n14p=$(sed -n 's/^.*Matched pattern: //p' "$X/n14b" | head -n 1); n14n=$(wc -c < "$X/n14b"); n14m=no
      for n14r in "${risky_patterns[@]}"; do [[ "$n14p" == "$n14r" ]] && { n14m=yes; break; }; done
      [[ $n14m == yes && $n14n -lt 3000 ]]; chk $? V14-N2-longline-pattern-is-a-rule "the longline text: the matched pattern is one of the rules: $n14m; text $n14n bytes (want yes, under 3000: the copy must not stand in for the pattern)" "[text]"
    fi
    if sel V14-G1-triggers-return-4-with-the-baseline-reason; then   # Q-7 (and the copy-paste of the two reason strings)
      if need _sg_vx_pass; then
        g1c="v=$x4; : \$v \$v \$v"; g1S=${_SGV_SMAX:-8192}
        g1w=$( _sg_relax_ok() { return 0; }; command=$g1c; _sg_vx_pass "$g1c" whole >/dev/null 2>&1; echo "$?|$_SG_OV_PAT|$_SG_OV_MODE" )
        g1s=$( _sg_relax_ok() { return 0; }; command=$g1c; _SG_SEGS=("v=$x4" ": \$v \$v \$v"); _sg_vx_pass "$g1c" segment >/dev/null 2>&1; echo "$?|$_SG_OV_PAT|$_SG_OV_MODE" )
        g1wa="4|the command is longer than $g1S characters after variable expansion|whole"; g1sa="4|a command segment is longer than $g1S characters after variable expansion|segment"
        t=''; [[ ${g1w%%|*} == 4 && ${g1s%%|*} == 4 ]] || t+='[status] '; [[ "$g1w" == "$g1wa" && "$g1s" == "$g1sa" ]] || t+='[text]'
        [[ -z "$t" ]]; chk $? V14-G1-triggers-return-4-with-the-baseline-reason "gate stubbed open, baseline pass, a copy over $g1S: whole [${g1w:0:140}] (want [$g1wa]); segment [${g1s:0:140}] (want [$g1sa])" "$t"
      else miss V14-G1-triggers-return-4-with-the-baseline-reason; fi
    fi
    if sel V14-G2-growth-limit-follows-gmax; then   # Q-31
      if need _sg_vx_collect _sg_vx_apply; then
        g2c="v=$(printf '%*s' 300 '' | tr ' ' w); : \$v"
        g2a=$( _SG_RELAXED=1; _SGV_GMAX=100; _sg_vx_collect "$g2c" >/dev/null 2>&1; _sg_vx_apply "$g2c" >/dev/null 2>&1; echo $? )
        g2b=$( _SG_RELAXED=1; _SGV_GMAX=400; _SGV_SMAX=100; _sg_vx_collect "$g2c" >/dev/null 2>&1; _sg_vx_apply "$g2c" >/dev/null 2>&1; echo $? )
        [[ "$g2a $g2b" == "2 0" ]]; chk $? V14-G2-growth-limit-follows-gmax "relaxed _sg_vx_apply, growth 298: _SGV_GMAX 100 -> status $g2a (want 2); _SGV_GMAX 400 with _SGV_SMAX 100 -> status $g2b (want 0); the limit is the growth over the input" "[status]"
      else miss V14-G2-growth-limit-follows-gmax; fi
    fi
    if sel V14-F1-status-4-falls-back-to-the-baseline-block; then   # Q-29
      awk '/^_sg_per_segment_eval\(\) \{/,/^\}$/' "$H" > "$X/pse.sh"
      if [[ ! -s "$X/pse.sh" ]]; then out SETUP V14-F1-status-4-falls-back-to-the-baseline-block "_sg_per_segment_eval not found by anchor"
      elif ! need _sg_emit_blocked _sg_time_budget; then miss V14-F1-status-4-falls-back-to-the-baseline-block
      else
        f1p="the command is longer than ${_SGV_SMAX:-8192} characters after variable expansion"
        f1r=$( source "$X/pse.sh"; _sg_core_eval() { _SG_MODE=whole; return 0; }; _sg_vx_pass() { _SG_OV_PAT="$f1p"; _SG_OV_MODE=whole; return 4; }; _sg_relax_run() { return 4; }; command="$rd"; _sg_per_segment_eval "$rd" >/dev/null 2>"$X/f1"; echo $? )
        f1l=$(head -n 1 "$X/f1"); f1w="[secret-guard] BLOCKED: command too large to scan for secrets. Limit hit: $f1p"
        t=''; [[ $f1r == 2 ]] || t+='[status] '; [[ "$f1l" == "$f1w" ]] || t+='[text]'
        [[ -z "$t" ]]; chk $? V14-F1-status-4-falls-back-to-the-baseline-block "_sg_per_segment_eval with a rerun that falls back (status 4): status $f1r (want 2), first line [${f1l:0:140}] (want [$f1w])" "$t"
      fi
    fi
```

套件约定核对：V0-H2 清单（上面列的四处）；SKIP 的平台原因（新编号在 `RELAX_IDS` 里，非放宽平台的 bash 上报 `SKIP [platform]`，3.2.57 一轮的 63 个 SKIP 全是 `[platform]`，含这五个）；计数（套件头注释 `Coverage: 967 cases (961 without zsh)` 改 `972 (966 without zsh)`，`136 of those cases` 改 `141`，git 检出里整套件 966/966 PASS 即 SC-13 绿）；commentsync（`commentsync.py --suite-only <套件> target` GREEN）。

一个疏漏及处理：补完后第一次跑 `v31/sc-cases.sh` 红了一条 `V0-H2-case-list`（期望 135 个、报告 140 个，多出的正是这五个，`sc-cases.sh` 自己有一份期望编号清单），是我漏加；已把五个编号加进 `sc-cases.sh` 的清单，重跑 142 PASS / 0 FAIL，并因 `sc-cases.sh` 的 sha 变了而重跑了终轮，使 W14 首行的 sha 前缀与交付的文件一致（INV-8）。

## 4 各轮结果与首尾负载

一分钟负载读数，起 → 止。所有计时类判定都是在起止都低于 2 的轮里做的（INV-7）；每个坏实现一行里还记了该次套件自己打印的负载与「timing batch: judged」。

| 轮 | 对象 | 结果 | 负载起 → 止 |
|---|---|---|---|
| 补前：实现整轮 | PATH bash 5.2.15，`SG_W10_ONLY=.` | 136 PASS，0 FAIL，0 SKIP | 0.66 → 1.45 |
| 第一轮：31 个坏实现 | 预计用例，缺口再跑整轮（r1） | 26 / 2 / 3 / 0（按预期 / 别处 / 未抓住 / 未判），19:10:54Z 至 19:16:53Z | 1.47 → 1.08 |
| 补后：5 个缺口坏实现 | 预计用例 + 补的用例（r2g） | 5/5 由补的用例抓住 | 1.34 → 1.25 |
| 补后：实现整轮 | PATH bash 5.2.15 | 141 PASS，0 FAIL，0 SKIP | 1.03 → 1.06 |
| 补后：实现整轮 | `SC_BASH=bash-3.2.57` | 78 PASS，63 SKIP 全部 `[platform]`，0 FAIL | 1.06 → 1.18 |
| 补后：V14 五个用例 | bash 5.0.18、5.1.16、5.3.20 各一轮 | 各 7 PASS（5 个用例加 V0-H1、V0-H2），0 FAIL | 1.25 → 1.25 |
| 整套件 | git 检出，含 SC-13，PATH bash | 966/966 PASS，0 FAIL，0 SKIP；套件内 W10 批负载 1.11 → 1.11 | 调用起 1.11，止 2.30（止读数含套件自己的 SC-8 压测，之后没有计时判定） |
| commentsync | `--suite-only <套件> target` | GREEN | - |
| `sc-cases.sh` 实现，首次 | 清单漏我的五个编号 | 141 PASS，1 FAIL（V0-H2） | 1.20 → 1.62 |
| `sc-cases.sh` 实现，修后 | 实现 | 142 PASS，0 FAIL，0 SKIP | 1.33 → 1.37 |
| 终轮：31 个坏实现 | `w14.sh`（final2），19:40:23Z 至 19:44:07Z | 26 按预期 + 5 由补的用例，0 别处，0 未判，0 未抓住 | 1.37 → 1.35 |

（`final` 那一轮 19:33Z 是在 `sc-cases.sh` 改清单之前跑的，已被 `final2` 取代，交付的 W14 文件是 `final2` 的。）

## 5 交付与文件

- `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14.sh`（新）、`w14-mutants.py`（新，与冻结版同）、`W14-independent-mutants.txt`（新，首行：日期 2026-10-24T19:40:23Z、负载 1.37 1.40 1.29、base e83c5e30f2cc、impl af4658b6f935、suite 3351b47da825、helper 4f467588aef1、sc-cases.sh 7d29c3cd0f5b、sc-direct.sh fb3418921bca、mutants.py 2060d2e0c17f、w14-mutants.py 4327121c903c，另记 predict.md 627580356dcd；之后 31 行，每个一行；末行汇总）。`w14.sh` 的环境开关见它的头注释（`W14_IDS`、`W14_FULL`、`W14_SC_BASH` 等）；它读 scratchpad 里的 `predict.md` 与 `gapmap.tsv`（补用例对应表）。
- 主仓改动（均未 commit）：`v31/sc-cases.sh`（只加期望编号清单里的五个编号）、`v31/sc-direct.sh`（加五个用例与 `N_IDS`）。
- aria worktree（`feature/secret-guard-w10-failclosed-narrowing`，未 commit）：`hooks/tests/lib/secret-guard-w10-direct.sh`（+五个用例与两处编号清单）、`hooks/tests/secret-guard.test.sh`（`SGW_EXP_DIRECT` 加五个编号，头注释两个计数）。`git status` 只有这两个文件；hook 的 sha256 前缀仍是 af4658b6f935。
- scratchpad `r217impl/t003a/`：`w14-mutants.py`、`list.md`、`predict.md`、`FROZEN.sha`、`patch-v14.py`（补用例的补丁脚本）、`gapmap.tsv`、`mut/`（31 个坏实现，只在这里）、`logs/`（每次运行的原始输出，`r1-*` 为第一轮，`final2-*` 为终轮，`impl-*` 为实现各轮）。

## 6 规格与约定核对

- 没有遇到规格两种读法、或照做违反某条 INV 的情形，没有因此停下。
- INV-1、INV-3：hook 未动。INV-2：用例同时进套件、`sc-direct.sh`（与 `sc-cases.sh` 的清单）。INV-5 与 Rule #7：没有打印任何像凭据的值，新用例沿用 helper 里运行时拼装的 `$cfg`，生成器与补丁脚本里没有凭据形字符串。INV-7：见第 4 节。INV-8：W14 首行记了全部 sha 前缀。INV-9：`w14.sh` 每次先断言 `git show 59e333c:hooks/secret-guard.sh` 的 sha256 前缀是 e83c5e30f2cc。
- 进程：没有用过 kill，后台任务都自行结束，`t003a/tmp` 为空，`pgrep` 查不到我留下的进程。

## 7 未做、拿不准与建议

1. **只被计时类 e2e 抓住的三个**：Q-16、Q-24（V3-E3）与 Q-17（V6-E2）。这些用例在负载 >= 2 时 SKIP `[load]`，三个坏实现在高负载下会漏。我没有跑高负载轮（INV-7 不允许据此下结论），也没有为它们补不依赖负载的直调用例（受工具调用上限所限）。建议：Q-16 用桩 `sleep` 记下计时器的参数，断言等于 `_SG_LEFT`；Q-24 断言 `_sg_vx_collect` 前后 `_SG_P0` 不变；Q-17 断言作业被截止杀死时命令替换自己的 stderr 为空。Q-29 原先也属这一类，已由 V14-F1 补掉。
2. **Q-7 的 V2-G12 为什么绿**：我按纪律没读它的断言体，只能推测它只验「准入门关闭」那一极，没验「打开后返回 4」。V14-G1 补了打开的那一极；V2-G12 本身要不要改，请作者看。
3. **整轮红集只做了 4 个**（Q-7、Q-15、Q-22、Q-31）。每个坏实现跑一遍 `SG_W10_ONLY=.` 约 50 秒，全部 31 个约 26 分钟，我没做；所以大多数坏实现除了预计用例之外还红在哪里，报告里没有数据。
4. **标签预测有一部分是猜的**（没读断言体）；Q-29 因此被判为别处抓住，实质上红的原因是对的。
5. **WSL 的 `/proc/sys/fs/binfmt_misc/WSLInterop` 分支**在非 WSL 主机上永远为假，e2e 与直调都造不出这个文件，我没有构造相应坏实现；要覆盖得在 WSL 上跑，或把路径参数化（那是改实现，不在本段范围）。
6. 第一段只要求「坏实现 + 补缺口」，**对抗耗时矩阵不在本段**，没做。
7. 下游文档里凡写着 136、967、961 的计数（CHANGELOG、standards 的 secret-hygiene 三处计数、proposal 里引用套件用例数的地方）要由 TASK-006 同步成 141 / 972 / 966；我没碰（不在允许的文件里）。
8. 补后的实现整轮只在 PATH 的 5.2.15 与 3.2.57 上各跑了完整一轮（任务书的要求）；5.0.18、5.1.16、5.3.20 上只跑了 V14 五个用例（全绿），没有重跑完整一轮。
9. 参照：规格里记的是「作者的 23 个全被抓住，非作者的 60 个漏网 46 个」；这一段非作者的 31 个里 5 个第一轮漏（16%），其中 3 个完全没有红，2 个红在别处，量级比那时小得多，但样本与阶段都不同，不宜直接比。

## 8 工具调用次数

截至写完本报告共 52 次（上限 70，第 55 次之前已停止新工作）。
