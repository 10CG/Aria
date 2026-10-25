#!/usr/bin/env python3
# mkreport5f3.py CALLS: assembles T005f3-report.md from the files of t005f3/ (nothing typed from memory except the prose).
import sys, os, re, subprocess
S = '/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad'
O = S + '/r217impl/t005f3'; R = O + '/runs'; WT = S + '/wt217/aria'
V = '/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31'
OUT = S + '/r217impl/T005f3-report.md'
calls = sys.argv[1] if len(sys.argv) > 1 else '?'
def rd(p):
    try: return open(p, encoding='utf-8', errors='replace').read()
    except OSError as e: return '<missing: %s>' % e
def fence(t, lang=''): return '```' + lang + '\n' + t.rstrip('\n') + '\n```\n'
def grab(t, start, end):
    i = t.find(start); j = t.find(end, i)
    return t[i:j + len(end)] if i >= 0 and j >= 0 else '<not found: %r>' % start[:60]
def lines(p, pat): return '\n'.join(x for x in rd(p).split('\n') if re.search(pat, x))
helper = rd(WT + '/hooks/tests/lib/secret-guard-w10-direct.sh')
w1block = grab(helper, '# What 1 supplement 2 (v3.4; TASK-005 D-1', '  else miss V15-W1m-mount-table-read-only-after-platform-and-time; fi\nfi\n')
w1eblock = grab(helper, '  if sel V15-W1e-gate-closed-by-wsl-file-system; then', '      fi\n    fi\n  fi\n')
wm = grab(helper, 'wslmark() {', '\n}\n')
t2 = grab(helper, '  if sel V15-T2-anchor-taken-once-at-hook-start; then', 'a false red)\n')
steps = rd(R + '/steps.log')
def summ(n):
    t = rd(R + '/' + n + '.txt')
    keep = [x for x in t.split('\n') if re.match(r'^(SKIP: |# totals|W10 ported cases|PASS V0-H2|# perturbation round|# end \|)', x)]
    nf = len([x for x in t.split('\n') if re.match(r'^(FAIL|MISSING|SETUP)\b', x)])
    return '- %s: FAIL/MISSING/SETUP 行 %d；%s' % (n, nf, ' / '.join(k[:230] for k in keep[-4:]) or '(无摘要行)')
rounds = ['w10-5.0.18', 'w10-5.1.16', 'w10-5.2.15', 'w10-5.3.20', 'w10-3.2.57', 'full-path', 'full-wsl', 'sc-cases']
mut = '\n'.join('- %s：%s' % (m, ' '.join('%s %s' % (v, k) for k, v in sorted(
    __import__('collections').Counter(x.split()[1] for x in rd(R + '/' + m + '.txt').split('\n') if re.match(r'^(BI|P)-', x) and len(x.split()) > 1).items())))
    for m in ('mut-v31', 'mut-suite', 'mut-suite-nj', 'mut-suite-p0') if os.path.exists(R + '/' + m + '.txt'))
p0 = lines(R + '/mut-suite.txt', r'^P-0 ') + '\n' + lines(R + '/mut-suite-nj.txt', r'^P-0 ') + '\n' + lines(R + '/mut-suite-p0.txt', r'^P-0 ') + '\n' + lines(R + '/mut-v31.txt', r'^P-0 ')
perf = '\n'.join('%s: %s' % (f, lines(R + '/' + f, r'^(TIMED|SKIP|FAIL|MISSING)')) for f in sorted(os.listdir(R)) if f.startswith('perf-') and f.endswith('.txt'))
w14 = lines(R + '/W14-independent-mutants.txt', r'^# end') or '<none>'
w14prev = lines(S + '/r217impl/t005f2/runs/W14-independent-mutants.txt', r'^# end') or '<none>'
cmpall = '\n'.join(lines(O + '/proofs/' + f, r'^# ') for f in sorted(os.listdir(O + '/proofs')) if f.startswith('cmp-'))
P = rd(O + '/prove5f3.out')
rep = f'''# TASK-005 修复轮第三段（5f3）执笔席报告（10CG/aria-plugin#217）

执笔席：5f3（全新实例），2026-10-25。aria worktree 基线 `710a36d`（hook `834dee6db0d0`），改后 hook sha256 前缀 **`16996eb7db21`**，未 commit。工具调用 {calls} 次（上限 60）。
脚本与证据都在 `r217impl/t005f3/`：`edit5f3.py`（全部改动，从 `pre/` 的改前副本出发，可重放）、`prove5f3.sh`（坏实现、能红、判据对照、变异生成、commentsync）、`runall3.sh`（各轮）、`expect.md`（先写的预期）、`proofs/`、`runs/`、`diffs/`、`cs/`。

## 一、各项结论

- **A1** `_sg_relax_ok`：环境变量那一行原本已与 v3.4 第一行逐字相同（脚本断言后照换，零字节变化）；删掉 v3.3 那行 `[[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl`；在 `_sg_relax_left || return 1` 之后加 v3.4 第二行。两行都由脚本从 proposal「v3.4 的做法」之后的第一个代码块机械取出。
- **A2** `_sg_relax_nowslfs` 整个换成 proposal 第二个代码块（机械取出，逐字）。
- **A3** 头注释「Shell variable indirection」补 D-3 例外一句（与重跑块头那句同义：「inside the rerun」对应块头的「inside the job」，「instead of the size block's text」对应「instead of the baseline text」——头注释里回落就叫 that size block），只重排了原来那一短行，宽度取该条目最宽的 91 列。
- **A4** hook 其余一字未改：完整 diff 见第二节（3 个 hunk）。
- **B1** V15-W1a-d 结论仍为 a 0、b 1、c 0、d 1；只改了 W1c 的说明文字（两个名字）和 `w1` 的实现（拆出通用的 `w1x`，见下）。
- **B2** V15-W1e 改成两面（id 不变）：子壳里新 source hook、`unset _SG_RELAXED WSL_DISTRO_NAME WSL_INTEROP`、预算显式 3、新锚点、`_sg_relax_noext` 桩成 none，平台用本 bash（MODE relax）；桩返回 0 须开门（标签 `[open]`），返回 1 须关门（`[closed]`）。
- **B3** 新增 9 条：W1f 空表、W1g 叠 autofs、W1h 目录当表、W1i noglob、W1j failglob、W1k 不可查（uid 0 下 SKIP [platform]）、W1l 可查不可列（结束前改回权限）、W1m 顺序（两种模式），W1n 开销（MODE relax）。全部在目标 hook 上 PASS（5 个 bash 的过滤轮、整轮、sc-cases）。
- **B4** 能红：全部按预期——v3.3 函数使 f g h i j k l 变红；去 `-x` 行只红 k；挪回平台判据之前只红 m（`[platform] [time]`）；W1e 两面各一个坏实现分别红 `[closed]` 与 `[open]`；v3.3 函数下 W1n 墙钟 2.219 s（soft bad）。见第三节。
- **B5** 四份测试侧判据（helper / sc-direct.sh 的 `wslmark`、套件 `sg_w10_wslfs`、sc-cases.sh 的 `wslmark`）改为同一函数体（另写，不 source hook）；在主控的 12 种情形上与 hook 函数逐种对照，5 个 bash 都是 12 条 0 不一致，hook 结论与 proposal 列的 12 个值一致、stderr 全 0。
- **B6** V15-T2 注释改为：值由准入门与 run 里那两次 `_sg_relax_left` 定，从设锚点到这两次调用超过 1.0 s 时门关上或 run 回落、判定根本不运行（`_SG_LEFT []` 的假红）。
- **B7** 编号进了 helper `RELAX_IDS`（W1n）、套件 `SGW_EXP_DIRECT`、sc-cases.sh 的 `EXP_DIRECT_BOTH` / `EXP_DIRECT_RELAX`；套件头注释 981 (975) -> 990 (984)。本机无 zsh，整轮实数 984，与「无 zsh」计数相符。
- **C** `mutants.py` 一个锚点（删 `_sg_relax_left || return 1` 那个变异）改成新原文；`impl/w14-mutants.py` 的 Q-30 锚点同样改、`IMPL_SHA12` 834dee6db0d0 -> 16996eb7db21；两者在新 hook 上都能全部生成（57 + 7；31）。commentsync 照前两段的做法从 eeb67786 版用 `t005f/cs/derive-5f.py` 重新导出，与 5f2 版只差 FIX5_HOOK 一行（站点 1 由删 2 增 2 变为删 2 增 3：D-3 那句是新单元）；target / baseline / proto GREEN，四个构造 RED（78、60、58、57；5f2 为 77、59、58、57）。
- **各轮**：全部绿。5 个 bash 过滤轮 0 FAIL；整轮两轮 0 FAIL；sc-cases 160 PASS 0 FAIL；run-mutants v31 模式 63 CAUGHT + P-0 GREEN，套件模式 63 CAUGHT、P-0 首轮 NOT-JUDGED（负载），低负载单跑两次都 GREEN；w14 预测内 26、新增用例抓到 5、未判 0、未抓到 0（与 5f2 同）。

## 二、hook 完整 diff（相对 710a36d）

{fence(rd(O + '/diffs/hook.diff'), 'diff')}
## 三、新用例与改过的用例（helper 与 v31/sc-direct.sh 同一份代码，INV-2）

两种模式的部分（W1a-d 改说明、W1f-l 新增、W1m 新增；`w1` 拆成通用的 `w1x` 加只管 `$w1d` 的 `w1`）：

{fence(w1block, 'bash')}
MODE relax 的部分（W1e 两面、W1n 开销）：

{fence(w1eblock, 'bash')}
V15-T2 注释（m-3）：

{fence(t2, 'bash')}
### 能红证明（`prove5f3.sh`，PATH 上的 bash 5.2.15，MODE relax，`SC_ONLY='^V15-W1[a-m]'`；W1n 另跑，见第五节）

坏实现（只在 `t005f3/bad/`，由 `prove5f3.sh` 里的 Python 段从改后 hook 生成）：`v33fn` = 函数换回 v3.3（与 `spec-probe2/old.sh` 逐字相同，已断言）；`nox` = 去掉 `[[ -x "$d" ]] || return 1` 一行；`order` = 删第二行、在环境变量行后放回 v3.3 那行（挪回平台判据之前）；`w1e-a` = 删 `_sg_relax_nowslfs || return 1`（W1e 关门面的坏实现）；`w1e-b` = 改成 `! _sg_relax_nowslfs || return 1`（开门面的坏实现）。

{fence(chr(10).join(x for x in P.split(chr(10)) if re.match(r'^(load|mkbad|good|v33fn|nox|order|w1e)', x)))}
## 四、测试侧 WSL 判据与 hook 函数的对照（主控 12 种情形，`spec-probe2/` 的假挂载表与 fx 目录）

四份判据的函数体相同（`edit5f3.py` 的 WM_BODY）：`cat` 读表（读不出或 0 字节算有标记）、`awk` 取该挂载点各行的类型再 `tail -n 1`（最上层）、不是 binfmt_misc 就没有标记、`( cd -- DIR )` 失败算有（不可查）、再逐个 `[ -e ]` 两个名字。与 hook 的写法不同（hook 用 awk 的 NR、`-x`），结论相反为一致。

{fence(chr(10).join(x for x in helper.split(chr(10)) if False) or wm, 'bash')}
5.2.15 的逐条结果：

{fence(rd(O + '/proofs/cmp-5.2.15.txt'))}
五个 bash 的汇总：

{fence(cmpall)}
## 五、各轮预期、结果与首尾负载

预期（开跑前写，`expect.md`）：

{fence(rd(O + '/expect.md'), 'markdown')}
`runall3.sh` 的步骤记录（每步开跑前等一分钟负载 < 1.2；load0 / load1 是该步首尾）：

{fence(steps)}
各轮摘要：

{chr(10).join(summ(n) for n in rounds)}

run-mutants：

{mut}

{fence(p0)}
w14（本段 / 5f2）：

{fence(w14 + chr(10) + w14prev)}
开销用例单跑（helper 直跑，TIMED 行的判定按 INV-7 看该步首尾负载，均 < 2）：

{fence(perf)}
commentsync 与变异生成（`prove5f3.sh`，首尾负载见上面 load0 / load1 行）：

{fence(chr(10).join(x for x in P.split(chr(10)) if re.match(r'^(gen|derive|commentsync|constr|cs |load|runall3)', x)))}
derive 日志：

{fence(rd(O + '/cs/derive.out'))}
INV-2 与清理核对：

{fence(rd(O + '/checks.txt'))}
## 六、未做或拿不准的项（请主控复核）

1. **W1n 放在 MODE relax**（RELAX_IDS / EXP_DIRECT_RELAX）：proposal 没说哪种模式；我按「v3.4 只在放宽平台、有时间时才读表，开销只在那里要紧」放进 relax，非放宽 bash 上记 SKIP [platform]。若主控要它两种模式都跑，只需挪编号与代码块。
2. **W1n 的「单独跑」只做到一半**：5 个 bash 的过滤轮用 `SG_W10_ONLY` 把它排除（正则 `^(V([0-9]|1[0-46-9])-|V15-T|V15-W1[a-m]-)`，过滤轮因此 158 条），在各轮之间对 4 个放宽 bash 单跑、另对 v3.3 单跑一次；但整轮、sc-cases 与两种模式的 P-0 没有排除单条用例的开关，它们里面照样含 W1n。实测单跑一次墙钟约 2 s、负载几乎不动（1.08 -> 1.07），未见影响别的计时用例。
3. **W1k 的 root 探测**只沿用了 helper 既有探测里的 `id -ru` 一项（uid 0 时 SKIP [platform]）；非 root 但带 CAP_DAC_OVERRIDE / CAP_DAC_READ_SEARCH 的进程也能查 000 目录，那时这条会假红（不会假绿）。既有的 CapEff 位检查（21、24 位）管的是另一种能力，没有照搬。
4. **W1e 的前置**：为保证「前面的判据都过」，我在子壳里加了 `unset _SG_RELAXED WSL_DISTRO_NAME WSL_INTEROP` 与显式预算 3（变量名运行时拼装写入），这超出原 W1e 的写法；id 保持不变。
5. **W1m 多了一条对照腿**（平台与时间都过时须恰好调用 1 次，标签 `[control]`），防止桩没接上时整条恒绿；`w1e-a` 坏实现证明它能红。任务书只要求前两腿。
6. 套件 `full-wsl` 轮里套件自己的判定仍是「relaxation expected: yes」（套件对每次运行 hook 都清掉 WSL 环境变量，与 5f2 相同），所以该轮也跑了 W1n。
7. 头注释那句的措辞是我拟的（同义而非逐字照抄块头），commentsync 把它当站点 1 的新单元收录。
'''
open(OUT, 'w', encoding='utf-8').write(rep)
print('report', OUT, len(rep), 'chars')
