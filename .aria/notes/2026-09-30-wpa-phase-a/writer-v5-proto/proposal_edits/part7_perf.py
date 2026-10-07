# part 7: the two places of proposal.md that quote measured time (W14 item 5 and the Impact performance line).  Every number is read from out/numbers.json (written by proto/mk_numbers.py
# from the raw timing outputs); a missing number stays a @PLACEHOLDER@ and apply_edits.py refuses to finish while one is left.
import json
import os

EDITS = []
_N = {}
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "out", "numbers.json")
if os.path.exists(_p):
    _N = json.load(open(_p, encoding="utf-8"))


def n(k):
    return str(_N[k]) if k in _N else "@" + k.upper().replace("-", "_") + "@"


def pct(b, t):
    if b in _N and t in _N:
        return str(round((float(_N[t]) - float(_N[b])) / float(_N[b]) * 100))
    return "@PCT_" + t.upper() + "@"


def ms(b, t):
    if b in _N and t in _N:
        return str(round((float(_N[t]) - float(_N[b])) * 1000))
    return "@MS_" + t.upper() + "@"


EDITS.append(("line", "  5. 原型实测",
              f"  5. 原型实测 (Linux 6.17, 4 核共享主机, 测量时 1 分钟负载约 1–2; 每侧交错取最小整进程 CPU 时间, 每档 5 对; 数值随主机而变, 只给量级): "
              f"(f) Bash {n('fB_b')} → {n('fB_t')} s、Read {n('fR_b')} → {n('fR_t')} s (都在 100 ms 地板附近, 上界 0.15 s), (f0) {n('f0B_b')} → {n('f0B_t')} s 与 {n('f0R_b')} → {n('f0R_t')} s (比值 {n('f0B_r')} 与 {n('f0R_r')}), "
              f"(f-hit) {n('fha_r')} (出现一次) 与 {n('fhb_r')} (出现 64 次), 无出现的对照档 {n('fh0_r')}, (g-a) {n('ga_r')}、(g-b) {n('gb_r')}, "
              f"(h) {n('h2_r')} (全部放行的对照档 {n('h1_r')}: 内建、W10 第二遍与扩展各判一遍, 不受 (h) 上界约束), (i) {n('i1_r')} 与 {n('i2_r')}, "
              f"(i3) 依 a–e 档为 {n('i3a_r')} / {n('i3b_r')} / {n('i3c_r')} / {n('i3d_r')} / {n('i3e_r')}。"
              f"同法的坏实现: W10 余量用 `${{s#*\"$pat\"}}` 取, 在 (g) 上 {n('bad_vx_quadratic_g-a_r')}× (满额档 {n('bad_vx_quadratic_g-b_r')}×); "
              f"每条扩展条目一个 grep 进程, 在 (f) 上 {n('bad_ext_perentry_fB_r')}× 与 {n('bad_ext_perentry_fR_r')}×; L3 不设迭代上界, 在 (i) 上 {n('bad_no_cap_i1_r')}× 与 {n('bad_no_cap_i2_r')}×; "
              f"第二遍按段交错, 在 (h) 上 {n('bad_vx_interleave_h2_r')}× 且活性断言失败 (内建已拦时它仍调用第二遍); 扩展先于内建在 (h) 上比值只有 {n('bad_ext_first_h2_r')} (没越界), "
              f"由活性断言抓到 (内建已拦时扩展入口仍被调用, SC-20 20l 同样抓到); 逐出现点算阶段的手写实现, 在 (f-hit) 的 64 处出现档上 {n('bad_ext_v4stage_fh-b_r')}×; "
              f"对每个出现点各判一遍内建判定的实现 {n('bad_ext_perocc_judge_fh-b_r')}× (活性断言同样失败: 内建判定函数被调用 65 次而不是 2 次); "
              f"L3 取值用前缀删除写法, 在 (i3) 上 {n('bad_val_quadratic_i3-a_r')}× (8 KB 头值) 与 {n('bad_val_quadratic_i3-e_r')}× (既有 bearer tag 的 8 KB 值); "
              f"参数名前缀无界的 cli pattern 在 (i3) 的 `-` 串档上 {n('bad_cli_unbounded_i3-b_r')}×、无左边界的 {n('bad_cli_noleft_i3-b_r')}×, 键名后缀无界的 kv pattern 在大写连续段档上 {n('bad_kv_unbounded_i3-c_r')}×。"))

EDITS.append(("sub", "@IMP_PERF@",
              f"  - **性能**: Read 面每次多一次扫描 (W1: 整进程 CPU 时间由约 {n('w1a_b')} s 增至约 {n('w1a_t')} s; 60 KB 无命中文本约 {n('w1b_t')} s, 180 KB 稠密 INI 赋值约 {n('w1c_t')} s, 均在 hook 的 5 s 超时之内); "
              f"进程调用延迟的判据与原型实测见 W14: 无扩展文件时 Bash 面约 +{pct('f0B_b', 'f0B_t')}%、Read 面约 +{pct('f0R_b', 'f0R_t')}% CPU 时间; 含 `$VAR` 引用的命令因 W10 第二遍约为基线的 1.5–2.3 倍 "
              f"((g-a) {n('ga_r')}、(g-b) {n('gb_r')}、全部放行的 (h) 对照 {n('h1_r')}; 引用越密越近 2×; 内建先判, 已被内建拦下的命令不付第二遍); "
              f"200 条扩展条目约 +{ms('fB_b', 'fB_t')} ms (Bash 面) / +{ms('fR_b', 'fR_t')} ms (Read 面) CPU / 次调用 (比值 {n('fB_r')} 与 {n('fR_r')}); "
              f"命令里出现列入的路径时扩展多付**一遍**内建判定, 约为基线的 {n('fha_r')} 倍 (4 KB 单行; 出现 64 处仍是 {n('fhb_r')} 倍: 与出现点数无关); 长单行 L3 输入的匹配与取值对长度线性 (W14 (i3))。", 1))

EDITS[0] = EDITS[0] + (1,)    # ("line", prefix, new) -> ("line", prefix, new, 1)
