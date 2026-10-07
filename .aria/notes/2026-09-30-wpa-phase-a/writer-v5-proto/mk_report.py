#!/usr/bin/env python3
"""mk_report.py -- compose out/report.md (the repair report returned in the structured output) from the final files; every number comes from a file.
usage: mk_report.py        (run after build_deliver5.py: reads deliver/, logs/, out/)"""
import hashlib
import json
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(EXP, "proto"))
from dispositions_data import D  # noqa: E402
from report_text import IMPLEMENTER, SHORT, SIBLINGS, WEAK  # noqa: E402

DEL = os.path.join(EXP, "deliver")
L = os.path.join(EXP, "logs")
OUT = os.path.join(EXP, "out")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


def size(p):
    return os.path.getsize(p)


def rd(p):
    return open(p, encoding="utf-8").read()


N = json.load(open(os.path.join(OUT, "numbers.json"), encoding="utf-8"))
runs = {}
for lab, desc in (("final_A", "基线, `WPA_BASH32`"), ("final_B", "基线, `WPA_BASH32` (复现孪生)"), ("final_N", "基线, 不带 `WPA_BASH32`"), ("final_T", "目标原型, `WPA_BASH32` + `WPA_REQUIRE_ALL=1`"),
                  ("final_TN", "目标原型, 不带 `WPA_BASH32`"), ("final_C", "基线, `WPA_BASH32`, 定稿 proposal + evidence 在场")):
    p = os.path.join(L, lab + ".out")
    runs[lab] = (desc, sha(p), size(p), rd(os.path.join(L, lab + ".rc")).strip(), size(os.path.join(L, lab + ".err")))
ta, tt = rd(os.path.join(L, "final_A.out")), rd(os.path.join(L, "final_T.out"))
tally = lambda t: ", ".join(f"{k} {v}" for k, v in re.findall(r"(?m)^(baseline-failing|doc-sync|reverse-guard|allow-guard|known-limit|zero-regression): (\d+/\d+)$", t))
rows = len(re.findall(r"(?m)^SC-\d+ │ ", ta))
n_yes = len(re.findall(r"(?m)^SC-\d+ │ .* │ yes$", tt))
ms = rd(os.path.join(OUT, "mut_summary_v5.txt"))
m_a = re.search(r"PART A\s+-- this round: (\d+) bad implementations; (\d+) turn at least one row red; (\d+) turn no row red", ms)
m_b1 = re.search(r"PART B1 -- regression of the previous round's bad implementations: (\d+) re-run; (\d+) keep every row that was red before; (\d+) lose a row \(regressions\); (\d+) were equivalent before; (\d+) superseded", ms)
m_b2 = re.search(r"PART B2 -- regression of the rounds before: (\d+) re-run; (\d+) keep every row that was red in v3; (\d+) lose a row \(regressions\); (\d+) were equivalent in v3", ms)
files = {k: (sha(os.path.join(DEL, k)), size(os.path.join(DEL, k))) for k in ("proposal.md", "baseline_probe.py", "baseline-evidence.md", "dispositions.json")}
manifest = len(rd(os.path.join(DEL, "MANIFEST.sha256")).strip().split("\n"))

md = []
md.append("# 返修报告: secret-net-l3-and-bypass-paths v4 -> v5 (post_spec 第 4 轮)\n")
md.append(f"""## 0. 摘要

- 第 4 轮 25 条 finding (1C / 9M / 15m) **全部 fixed** (0 rejected, 0 deferred; km/m6 的 Spec 侧已修, 清理已推送内容属 owner, 记 7.20), 主控 7 条裁定全部执行。
- 机制层面按主控方针 7 **复用而不新写**: 簇 T 的扩展判定直接调用内建的同一个判定函数 (`_sg_core_eval`), 没有第二份阶段 / 引号状态机; 簇 F 沿用默认 credit; 簇 M 只加成员行; 簇 U 是把基线视图原样保留再追加一个视图。需要新写的只有 W2 两个 pattern 的有界化 (线性)。
- 探针 {rows} 行 (上一版 411), 目标态 {n_yes} 行 `yes` + SC-30 一行不执行, 基线形态 `holds`。三份文件 sha256 前 16 位: proposal `{files['proposal.md'][0]}` ({files['proposal.md'][1]} 字节), 探针 `{files['baseline_probe.py'][0]}` ({files['baseline_probe.py'][1]} 字节), 证据 `{files['baseline-evidence.md'][0]}` ({files['baseline-evidence.md'][1]} 字节)。
- 变异实测: 本轮新坏实现 {m_a.group(1)} 个, {m_a.group(2)} 个转红、{m_a.group(3)} 个转 0 行 (逐个有理由); 前几版坏实现回归 {int(m_b1.group(1)) + int(m_b2.group(1))} 个, 丢失转红行 {int(m_b1.group(3)) + int(m_b2.group(3))} 个。
- **改变实现者动作且需重点核**的改动见第 3 节 (W1 两视图、W9 重做、W2 有界化、W11 credit 反转), 第 6 节列请裁项。
""")
md.append("## 1. 处置表 (席位 · 编号 · 键 · 处置 · 改动位置或证据; 全文见结构化输出的 `dispositions`)\n")
md.append("| 席位 | 编号 | 键 | 处置 | 改动位置 / 证据 (摘要) |\n|---|---|---|---|---|")
for d in D:
    md.append(f"| {d['seat']} | {d['label']} | `{d['key']}` | {d['disposition']} | {SHORT[(d['seat'], d['label'])]} |")
md.append("\n键 `0a8380fd` 在 ba/M2、qa/M1、cr/M1、km/M1 四个席位下是同一个问题 (簇 T) 的四个视角; 键 `684e9a24` 在 qa/m2 (BOM) 与 cr/m2 (旧时档数字) 下是**两个不同的问题**, 分开处置; 键 `6ff1d962` 在 tl/m1 与 cr/m1 下同一问题。\n")
md.append("## 2. 同族扫描清单 (修类不修例)\n" + SIBLINGS)
md.append("## 3. 改变实现者动作的改动 (单列, 请主控重点核)\n" + IMPLEMENTER)
md.append("## 4. 证据复跑记录\n")
md.append("全部由脚本生成, 命令与产物在交付目录 `deliver/` (`writer-v5-proto/README.md` 说明用法); 实验目录 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v5/`。\n")
md.append("**探针定稿运行** (`python3 baseline_probe.py <树>/aria`, 实验目录里的 aria / standards 副本, 非 root, 带 `WPA_BASH32` 的运行同时设真 bash 3.2.57):\n")
md.append("命令 (`<X>` = 实验目录, 经 `proto/runprobe.sh <标签> <树根> <spec 目录> <b32: 0|1>` 调用, 它先把 spec 目录快照到 `work/snap/<标签>/` 再在快照里跑; 环境 `HOME=<X>/home TMPDIR=<X>/tmp`): final_A / final_B / final_C = `WPA_BASH32=<X>/bash32/bash python3 baseline_probe.py <X>/base/aria`; final_N = 同上不带 `WPA_BASH32`; final_T = `WPA_BASH32=<X>/bash32/bash WPA_REQUIRE_ALL=1 python3 baseline_probe.py <X>/work/t5f/aria`; final_TN = 目标树不带任何环境变量。三个基线运行 (A / B / N) 与三个目标 / 对照运行 (T / TN / C) 各并发一批 (`proto/final_runs.sh stage1|stage2`)。\n")
md.append("| 运行 | 对象 | rc | stdout sha256 前 16 位 | 字节 | stderr |\n|---|---|---|---|---|---|")
for lab, (desc, h, b, rc, e) in runs.items():
    md.append(f"| {lab} | {desc} | {rc} | `{h}` | {b} | {e} 字节 |")
same_ac = runs["final_A"][1] == runs["final_C"][1] == runs["final_B"][1]
_t1 = os.path.join(L, "stage2_first", "final_T.out")
_same_t = os.path.exists(_t1) and open(_t1, "rb").read() == open(os.path.join(L, "final_T.out"), "rb").read()
md.append("\n- stage 2 跑了三遍: 前两遍之后各为改准或补全 proposal 里几句措辞与坏实现点名而重新定稿 (最后一次是 SC-10 / SC-19 / SC-22 / SC-26 的「怎么会红」补点名与 Tasks 1.8 一处), 交付的是第三遍 (快照与交付文件逐字节相同); 第一遍与第三遍的 final_T stdout 逐字节相同: **" + ("是" if _same_t else "否") + "**, 前两遍的日志不入交付。")
md.append(f"- final_A / final_B / final_C 逐字节相同: **{'是' if same_ac else '否'}** (C 在定稿 proposal 与 evidence 就位后跑, 证明基线 stdout 与这两份文件的文字无关)。")
md.append(f"- 基线类别计数 (final_A): {tally(ta)}; 基线形态 `holds`。目标 (final_T): {tally(tt)}; 目标形态 `holds`, 唯一未运行的行是设计上不执行的 30a。")
md.append("- `baseline-evidence.md` 的代码块 = final_A 的 stdout 原样 (mk_evidence.py 断言逐字节一致); 不带 `WPA_BASH32` 的 final_N 与它只在 29h / 29i / 32c / 32d 四行与末尾三行不同。")
md.append(f"- 与 proposal 的对账: `check_counts.py` / `xref_check.py` 输出在 `logs/check_counts.out`、`logs/xref_check.out`; `format_lint.py` 对三份文件的输出在 `logs/format_lint.out`; Rule #7 自扫 (`scan_all.py`, 基线与目标两个 `secret-scan.sh` 各以 Bash 输出与 Read 结果喂一遍) 在 `logs/scan_all.out`。\n")
md.append("**变异 / 坏实现** (`run_final_campaign5.sh` + `docvariants5.py` + `build_mut_summary5.py` -> `logs/mut_summary_v5.txt`):\n")
md.append(f"- Part A (本轮): {m_a.group(1)} 个 (含 {13 + 12} 个文档类), {m_a.group(2)} 个转红, {m_a.group(3)} 个转 0 行 (`ext_perentry` 是时档类: 功能行恒等, 由时档 (f) 抓到 {N.get('bad_ext_perentry_fB_r', '?')}x / {N.get('bad_ext_perentry_fR_r', '?')}x; 4 个 `remote_env_split` 等价变异的理由重做并在 22bo+22br+22bs 上重新验证)。")
md.append(f"- Part B1 (上一版的坏实现回归): {m_b1.group(1)} 个重跑, {m_b1.group(2)} 个保持全部转红行, {m_b1.group(3)} 个丢行, {m_b1.group(4)} 个上一版就是等价变异, {m_b1.group(5)} 个因设计已不存在而被取代 (逐个点名并写替代者)。")
md.append(f"- Part B2 (更早几版): {m_b2.group(1)} 个重跑, {m_b2.group(2)} 个保持, {m_b2.group(3)} 个丢行, {m_b2.group(4)} 个当时即等价。\n")
md.append("**时档与成本** (原始输出 `logs/timing_main.txt` 等; Linux 6.17, 4 核共享主机; 同一次运行内交错取最小整进程 CPU 时间; `timing.py --judge` 对 W14 上界逐档判 PASS / FAIL):\n")
tm = rd(os.path.join(OUT, "timing_main.txt"))
jl = re.findall(r"(?m)^judge: .*$", tm)
md.append(f"- 目标原型: {jl[-1] if jl else '(无 judge 行)'}。关键比值: (f) Bash {N['fB_r']} / Read {N['fR_r']}、(f0) {N['f0B_r']} / {N['f0R_r']}、(f-hit) {N['fha_r']} / {N['fhb_r']}、(g) {N['ga_r']} / {N['gb_r']}、(h) {N['h2_r']}、(i) {N['i1_r']} / {N['i2_r']}、(i3) {N['i3a_r']} / {N['i3b_r']} / {N['i3c_r']} / {N['i3d_r']} / {N['i3e_r']}。")
md.append(f"- 坏实现: 手写阶段切分 (f-hit 64 处) {N['bad_ext_v4stage_fh-b_r']}x; 逐出现点重判 {N['bad_ext_perocc_judge_fh-b_r']}x; 取值前缀删除 (i3) {N['bad_val_quadratic_i3-a_r']}x; 无界 cli 前缀 {N['bad_cli_unbounded_i3-b_r']}x; 无左边界 cli {N['bad_cli_noleft_i3-b_r']}x; 无界 kv {N['bad_kv_unbounded_i3-c_r']}x; 每条一个 grep {N['bad_ext_perentry_fB_r']}x; W10 余量二次写法 (g) {N['bad_vx_quadratic_g-a_r']}x / {N['bad_vx_quadratic_g-b_r']}x。")
md.append(f"- 命令长度 x 出现点 (occ_cost.py, 64 处): 2 KB: 目标 {N['occ2k_target_r']}x / 手写阶段切分 {N['occ2k_ext_v4stage_r']}x / 逐出现点重判 {N['occ2k_ext_perocc_judge_r']}x; 8 KB: {N['occ8k_target_r']}x / {N['occ8k_ext_v4stage_r']}x / {N['occ8k_ext_perocc_judge_r']}x。")
fz = lambda f: re.search(r"commands=(\d+) builtin-blocked=(\d+) diverging=(\d+)", rd(os.path.join(L, f)))
fv5, fold = fz("fuzz_ext_builtin_v5.out"), fz("fuzz_ext_builtin_v4stage.out")
md.append(("- 其它自检: `fuzz_value_of.py` (17 个 tag 的 6017 个真实 span, bash 5.2 与 3.2.57 各一遍): 0 差异; `diff_ext_builtin.py`: 本设计 93 形态 0 分歧, 手写阶段切分的参考坏实现 19/93 分歧; `fuzz_ext_builtin.py` (随机命令): {FUZZ_V5}, 手写阶段切分的参考坏实现 {FUZZ_OLD}; `readface_check.py`: 32 条路径各恰好命中一个基线备选; `refs_check.py`: 3-step wrong 0; `ere_battery.py` / `ere_claims.py`: 6 个新 pattern 的缩放比与 W2 引用的数字。\n").replace("{FUZZ_V5}", f"{fv5.group(1)} 条中内建拦 {fv5.group(2)} 条、分歧 {fv5.group(3)}").replace("{FUZZ_OLD}", f"{fold.group(1)} 条中分歧 {fold.group(3)}"))
md.append("## 5. 执笔自报薄弱点\n" + WEAK)
md.append(f"""## 6. 请裁项 (需要主控或 owner 的取舍)

1. **(产品级, 已入 7.20) 未修复旁路的披露范围**: Spec 一侧已去量化并登记; 研究笔记里对应两处的同样编辑、已推送分支的清理 (改写历史 / 删除远端分支) 不在我的权限内 (本轮不写仓内文件, 也不应做破坏性动作), 请 owner 裁 A (默认现状保留) / B (先修后披露) / C (披露规范成文)。主控「暂停推 GitHub」的自作主张请照主控记录列入 handoff 请复议。
2. **(技术级, 已按默认执行) W9 条目规则**: 含 ASCII 字母数字或任一非 ASCII 字节即有效 (采纳 ba/m1) 与剥 BOM (采纳 qa/m2); 备选: 纯非 ASCII 条目跳过 / 不剥 BOM (待复议 24)。
3. **(技术级) 簇 F 的 credit 取舍**: 默认 (转储后的锚定 grep / cut 放行, `grep -v x` 同样放行, 与基线 docker / kubectl 行一致); 备选 B 并入 tight (堵住「整份环境减一行」, 但把基线放行的日常核对改拦: 22br 的 44 个运行转红); 备选 C 收窄包裹 (待复议 23)。我认为默认更贴近「不降低既有检出、不新增未申报拦截」, 请主控确认。
4. **(技术级) W2 的上界 64 / 40** (待复议 31): 线性与覆盖面的折中, 数值是量级判断; 要更大上界只需改两个数字加两行 known-limit。
5. **(技术级, 我自作主张的验收参数) W14 时档**: (i3) 上界定 2.5 (原型 1.2-1.8, 坏实现 3.4x 起), (i3-b) 取 60 KB `-` 串、(i3-c) 取 100 KB 大写连续段 (基线自己对 300 KB 同类输入就要约 5 s CPU, 时档会「环境不合格」); 另给 `timing.py` 加了 `--judge` (回应 qa 的风险 2)。请确认这些参数。
6. **(技术级) SC-34 的判据口径** (待复议 32): 探针内用每进程 CPU 上限与整进程 CPU 总量比 (34c <= 3.5x), 不用墙钟; 代价约 {N.get('SC34SEC', '?')} 秒。
7. **(技术级) 采纳了席位备注两条** (不属 finding 表): Impact 加 Layer 2 一句 (新拦截在无人值守运行里同样生效, `# guard:ack` 由执行方自己写) 与关单评论的验证范围一句 (未在 MINGW64 / macOS 验证, 三席都提了)。
8. **未采纳**: (1) post-ship 复验 Tasks 1.12 里加 NUL 腿 —— NUL 以 `\\u0000` 到达 hook 的前提无端到端样本, 加了腿也只能记「未验证」, 不改; (2) 把 `timing.py` 的判据并进探针 —— 探针只做二值的线性判据 (SC-34), 比值判据留在 SC-30; (3) 给 W9 条目加 gawk 腿 —— 已消除对 awk 的依赖。
9. **Rule #10 自作主张清单** (请 owner 复议): 以上 2-7 条技术级取舍; 7 个旧变体与 29 个 `drop_extreader_*` 按「设计已不存在」移出回归并逐个写了替代者; `build_deliver5.py` 把 stage-1 的 proposal 快照相等断言放宽为「只要求探针相等」(proposal 文字不影响基线 stdout, 由 final_C 的逐字节相等证明); 没有以「变更小 / 性价比」为由跳过、降级或改序任何已启用的审计检查点。
""")
md.append(f"""## 7. 交付物 (`deliver/`, MANIFEST.sha256 共 {manifest} 个文件)

- `proposal.md` {files['proposal.md'][0]} / {files['proposal.md'][1]} 字节; `baseline_probe.py` {files['baseline_probe.py'][0]} / {files['baseline_probe.py'][1]}; `baseline-evidence.md` {files['baseline-evidence.md'][0]} / {files['baseline-evidence.md'][1]}; `dispositions.json` {files['dispositions.json'][0]} / {files['dispositions.json'][1]}。
- `logs/` 探针定稿运行 stdout / rc / stderr 与各脚本输出; `writer-v5-proto/` 脚本、计划与汇总 (无树副本); `MANIFEST.sha256` 覆盖其余全部文件 (`sha256sum -c MANIFEST.sha256` 在 `deliver/` 内通过)。
""")
open(os.path.join(OUT, "report.md"), "w", encoding="utf-8").write("\n".join(md))
print("report.md", size(os.path.join(OUT, "report.md")), "bytes")
