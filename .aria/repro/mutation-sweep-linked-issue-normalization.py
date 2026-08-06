#!/usr/bin/env python3
"""linked-issue-normalization — 归一谓词的**穷举**变异测试 (Q7-1, owner 2026-08-06)。

为什么是穷举而不是逐轮挖
------------------------
post_spec R1' 与 R2' 各用变异测试挖出覆盖盲区, 每轮一到两个维度:
    R1'  strip 第三点 (`/`-split 之后)   -> 新增 SC-1b
    R1'  `#` 的切分方向                  -> 新增 SC-11
    R2'  casefold 维度                   -> 本轮补
    R2'  number 相等条件                 -> 本轮补
    R2'  `/` 的切分方向                  -> 本轮补
「每轮挖一两个」是不收敛的做法。归一谓词的**维度是有限集** —— 本脚本把它枚举完,
逐维建一个「自然的疏漏实现」, 要求 SC 全集里**至少有一条能杀它**。

判定
----
    每个变异体必须被 ≥1 条 SC 杀死 (killed)。
    SURVIVOR = 该维度零覆盖 ⇒ Spec 必须补 SC。
    exit 1 当且仅当存在 survivor。

用法
----
    python3 mutation-sweep-linked-issue-normalization.py <state-scanner 根目录>

零依赖 (stdlib only)。只读, 不写文件、不触碰 refs/aria/coordination。
本脚本实现的是 Spec §归一规则 的**参照实现**, 不 import 生产代码 ——
生产代码此刻尚未修复 (Spec 停在 A.1), 参照实现代表「Phase B 应当写出来的东西」。
"""
import itertools
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)

MAX_DIGITS = sys.get_int_max_str_digits()


# ---------------------------------------------------------------------------
# 参照实现 —— 逐字照 Spec §归一规则 五步
# ---------------------------------------------------------------------------
def normalize(value, *,
              guard_hash=True,       # 规则1: 先判 `#` 存在性
              rsplit_hash=True,      # 规则1: 取**最后一个** `#`
              strip_left=True,       # 规则1: strip `left`
              strip_number=True,     # 规则1: strip `number_str`
              strip_basename=True,   # 规则1: `/`-split 之后再 strip
              rsplit_slash=True,     # 规则3: 取**最后一段**为 basename
              translate=True,        # 规则3: `./_` -> `-`
              casefold=True,         # 规则5: casefold
              check_digits=True,     # 规则2: isascii and isdigit
              length_bound=True,     # 规则2: limit > 0 and len > limit
              use_number=True):      # 规则5: basename 相等 **且** number 相等
    """返回 (basename, number) 或 None (不可解析)。"""
    if guard_hash:
        if "#" not in value:
            return None
        parts = value.rsplit("#", 1) if rsplit_hash else value.split("#", 1)
        left, number_str = parts[0], parts[1]
    else:
        # 变异: 无存在性守卫且不兜异常 —— Spec 规则1 明令禁止的那种写法
        parts = value.rsplit("#", 1) if rsplit_hash else value.split("#", 1)
        left, number_str = parts[0], parts[1]     # 无 `#` 时抛 IndexError

    if strip_left:
        left = left.strip()
    if strip_number:
        number_str = number_str.strip()

    if check_digits and not (number_str.isascii() and number_str.isdigit()):
        return None
    if length_bound and MAX_DIGITS > 0 and len(number_str) > MAX_DIGITS:
        return None
    try:
        number = int(number_str)
    except ValueError:
        return None

    if "/" in left:
        basename = left.rsplit("/", 1)[1] if rsplit_slash else left.split("/", 1)[1]
    else:
        basename = left
    if strip_basename:
        basename = basename.strip()
    if not basename:
        return None
    if translate:
        basename = basename.replace(".", "-").replace("_", "-")
    if casefold:
        basename = basename.casefold()
    return (basename, number) if use_number else (basename, 0)


def make_matcher(**flags):
    """规则 4/5: 可解析走归一键, 不可解析退回原串精确比较。"""
    def matches(a, b):
        ka, kb = normalize(a, **flags), normalize(b, **flags)
        if ka is None or kb is None:
            return a == b
        return ka == kb
    return matches


# ---------------------------------------------------------------------------
# SC 全集 (Q6 缩范围后保留的 13 条) —— 与 proposal.md §Success Criteria 逐字对应
# ---------------------------------------------------------------------------
def allpairs(vals, exp):
    return [(a, b, exp) for a, b in itertools.combinations(vals, 2)]


_BIG = "aria-plugin#" + "9" * (MAX_DIGITS + 1)

SC = {
    "SC-1": allpairs(["aria-plugin#122", "10CG/aria-plugin#122",
                      "10CG/aria-plugin #122", "aria-plugin #122"], True),
    "SC-1b": [("10CG / aria-plugin#122", "10CG/aria-plugin#122", True),
              ("  10CG/aria-plugin#122  ", "10CG/aria-plugin#122", True),
              ("10CG/ aria-plugin #122", "10CG/aria-plugin#122", True)],
    "SC-2": [("10CG/Aria#147", "10CG/aria-plugin#147", False)],
    "SC-3": [("10CG/aria-plugin#1", "otherorg/aria-plugin#1", True)],
    "SC-4": [("aria-plugin#007", "aria-plugin#7", True),
             ("aria-plugin# 122", "aria-plugin#122", True)],
    "SC-5": [("10CG/aria-orch#5", "10CG/aria-orchestrator#5", False)],
    "SC-5b": allpairs(["10CG/10cg.local#20", "10CG/10cg-local#20",
                       "10CG/10cg_local#20"], True),
    "SC-5c": [("10CG/aria plugin#1", "10CG/aria-plugin#1", False)],
    "SC-6": [("#5", "#5", True), ("#5", "#7", False),
             ("10CG/#7", "otherorg/#7", False),
             ("no-hash-here", "no-hash-here", True),
             ("repo#abc", "repo#abc", True)],
    "SC-6b": [("aria-plugin#+7", "aria-plugin#7", False),
              ("aria-plugin#1_0", "aria-plugin#10", False),
              ("aria-plugin#１２３", "aria-plugin#123", False),
              ("aria-plugin#²", "aria-plugin#2", False),
              ("aria-plugin#+7", "aria-plugin#+7", True),
              ("aria-plugin#1_0", "aria-plugin#1_0", True),
              ("aria-plugin#１２３", "aria-plugin#１２３", True),
              ("aria-plugin#²", "aria-plugin#²", True),
              (_BIG, _BIG, True)],
    "SC-10": [("aria-plugin#500", "aria-plugin#500", True)],   # 批次隔离的比较面
    "SC-11": [("repo#7#8", "repo#7#008", True), ("repo#7#8", "repo#8", False)],
    "SC-12": [],   # 返回契约, 由下方 contract_check 单独验
}

SC.update({
    "SC-13": [("10CG/Aria-Plugin#122", "10CG/aria-plugin#122", True),
              ("ARIA-PLUGIN#5", "aria-plugin#5", True)],
    "SC-14": [("aria-plugin#122", "aria-plugin#7", False),
              ("aria-plugin#122", "aria-plugin#123", False)],
    "SC-15": [("10CG/sub/aria-plugin#5", "aria-plugin#5", True),
              ("10CG/sub/aria-plugin#5", "othergroup/aria-plugin#5", True)],
})

# 已转正进 Spec (2026-08-06), 此表保留为空以维持结构
SC_PROPOSED = {
    "_(已转正)_": [],
    "SC-13 (casefold)": [("10CG/Aria-Plugin#122", "10CG/aria-plugin#122", True),
                         ("ARIA-PLUGIN#5", "aria-plugin#5", True)],
    "SC-14 (number 相等)": [("aria-plugin#122", "aria-plugin#7", False),
                            ("aria-plugin#122", "aria-plugin#123", False)],
}
SC_PROPOSED = {"_(已全部转正进 Spec)_": []}

# 行为不可观测的条款 —— 暴力搜 47,211 个候选串 (单值层全枚举 + 配对层抽样) 零差异。
# 它们的疏漏变异体产出与正确实现**完全相同**的行为 ⇒ 不可能有 SC 杀死它们。
# 显式豁免而非静默忽略; 理由与实证见 proposal.md §两条规范性但行为不可观测的条款。
UNOBSERVABLE = {
    "M03 不 strip left": "org 段不参与匹配, 且 basename 在 /-split 后还会再 strip 一次",
    "M10 漏长度上界": "同条规则强制 int() 包 try/except, 而 int() 抛 ValueError 的充要条件就是超上界",
}


# ---------------------------------------------------------------------------
# 变异体 —— 归一谓词的**全部**维度, 每维一个「自然的疏漏」
# ---------------------------------------------------------------------------
MUTANTS = {
    "M01 无 `#` 不守卫":        dict(guard_hash=False),
    "M02 `#` 取第一个":          dict(rsplit_hash=False),
    "M03 不 strip left":         dict(strip_left=False),
    "M04 不 strip number_str":   dict(strip_number=False),
    "M05 `/` 后不 strip":        dict(strip_basename=False),
    "M06 `/` 取第一段":          dict(rsplit_slash=False),
    "M07 漏 ./_ 译码":           dict(translate=False),
    "M08 漏 casefold":           dict(casefold=False),
    "M09 漏 isdigit 谓词":       dict(check_digits=False),
    "M10 漏长度上界":            dict(length_bound=False),
    "M11 丢 number 相等条件":     dict(use_number=False),
}

REF = make_matcher()


def run_sc(matcher, table):
    """返回被杀死该 matcher 的 SC 名列表。"""
    killed = []
    for name, pairs in table.items():
        for a, b, exp in pairs:
            try:
                act = matcher(a, b)
            except Exception:                                  # noqa: BLE001
                act = "EXC"
            if act != exp:
                killed.append(name)
                break
    return killed


# 参照实现自检: 必须通过全部 SC
ref_fail = run_sc(REF, {**SC, **SC_PROPOSED})
if ref_fail:
    sys.exit("FATAL: 参照实现自己没通过 %s —— 参照实现或 SC 表有错, 先修它" % ref_fail)

print("参照实现自检: 通过全部 %d 条 SC ✅\n" % len({**SC, **SC_PROPOSED}))
print("%-26s %-38s %s" % ("变异体 (维度)", "被现有 SC 杀死?", "被待补 SC 杀死?"))
print("-" * 92)

survivors = []
for label, flags in MUTANTS.items():
    m = make_matcher(**flags)
    by_now = run_sc(m, SC)
    by_new = run_sc(m, SC_PROPOSED)
    if by_now:
        verdict = "✅ " + ", ".join(by_now[:3])
    elif by_new:
        verdict = "⚠️ 仅待补 SC 能杀"
    elif label in UNOBSERVABLE:
        verdict = "⬜ 行为不可观测 (已成文豁免)"
    else:
        verdict = "❌ SURVIVOR (零覆盖)"
        survivors.append(label)
    print("%-26s %-38s %s" % (label, verdict, ", ".join(by_new) or "—"))

print()
if survivors:
    print("### ❌ 存在 SURVIVOR —— 这些维度零覆盖, Spec 必须补 SC:")
    for x in survivors:
        print("   ", x)
    sys.exit(1)

only_new = [l for l, f in MUTANTS.items()
            if not run_sc(make_matcher(**f), SC) and run_sc(make_matcher(**f), SC_PROPOSED)]
if only_new:
    print("### ⚠️ 以下维度只有**待补 SC** 能杀 —— 补进 Spec 后本脚本才应 exit 0:")
    for x in only_new:
        print("   ", x)
    sys.exit(1)

print("全部 %d 个维度均被现有 SC 覆盖 ✅" % len(MUTANTS))
