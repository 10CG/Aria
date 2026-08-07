#!/usr/bin/env python3
"""linked-issue-normalization — SC-1~11 baseline 实测 (Rule #6 substitute 的证据载体)。

用途
----
OpenSpec `linked-issue-normalization` 的 rule6_note 走 **substitute 框定**: 判据表
第一行「描述性 (schema / 字段 / 命令 / 勘正)」⇒ 以「SC 级 baseline-failing 结构化测试」
替代 AB benchmark。owner 2026-08-02 裁定 (`db2e983`) 要求 **substitute 须实证而非声称**。

本脚本就是那份实证: 对**未修复的现状** `lib/collision.py::linked_issue_overlaps`
逐条跑 Spec §Success Criteria 的 SC-1~11, 输出每条的真实红/绿, 与 Spec 的 baseline
表逐格比对。

    baseline 红 = 该 SC 能证伪现状实现 ⇒ 算进 substitute 证据面
    baseline 绿 = 负控 / 已知限 / 回落语义 / 冻结断言 ⇒ 不算证据面 (恒绿是正确的)

用法
----
    python3 sc-baseline-linked-issue-normalization.py <state-scanner 根目录>

例:
    python3 .aria/repro/sc-baseline-linked-issue-normalization.py \\
        aria/skills/state-scanner

SC-8c (既有 6 条测试逐字不改全绿) 不在本脚本内 —— 它是套件级断言, 用:
    python3 -m pytest tests/test_release_by_track.py \\
        -k "TestLinkedIssueOverlaps or TestPhase1GateLinkedIssueCli" -q

零依赖 (stdlib only)。只读, 不写任何文件、不触碰 refs/aria/coordination。

实测史:
  2026-08-05 首次  — aria 子模块 af87cae (v1.65.5), 14/14 与 Spec baseline 表一致
  2026-08-05 R1'后 — 新增 SC-1b / SC-10 / SC-11 三条, 16/16 一致;
                     证据面由 {SC-1,SC-3,SC-4,SC-5b} 扩到 {+SC-1b,+SC-11} 六条

漂移守卫 (R1'/tech-lead-m3)
--------------------------
本脚本此前把 proposal 的 baseline 表**手抄成常量**, proposal 改了它不会红 ——
而本 Spec 却对 SC-7 fixture **强制**要求漂移守卫。对别人强制的守卫必须施加给自己。
现改为从 proposal.md **现场解析**, 三重 fail-CLOSED:
  (a) 解析不到 proposal 或表 -> sys.exit, **绝不回退硬编码**;
  (b) **双向**漂移检查 (脚本测了表里没有的 / 表里有脚本没测), SC-8c 显式豁免
      (它由上面的 pytest 命令另测), 非静默忽略;
  (c) 「实测红集合 == 表声称的证据面」不符即 exit 1。
"""
import itertools
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)

sys.path.insert(0, sys.argv[1])
from lib.claim_schema import ClaimRecord          # noqa: E402
from lib.collision import linked_issue_overlaps   # noqa: E402


def claim(track_id, linked_issue, status="active"):
    return ClaimRecord(
        schema_version="1", track_id=track_id, owner="o", container="c",
        session="s", phase="B.1", status=status,
        claimed_at="2026-08-05T00:00:00Z", heartbeat_at="2026-08-05T00:00:00Z",
        linked_issue=linked_issue,
    )


def hits(theirs, mine):
    """现状实现是否把 theirs 判为与 mine 同一 issue。

    只驱动比较谓词: status=active 绕开 _TERMINAL skip, track_id 相异绕开自排除。
    """
    return len(linked_issue_overlaps([claim("theirs", theirs)], "mine", mine)) > 0


def allpairs(vals, expected):
    return [(a, b, expected) for a, b in itertools.combinations(vals, 2)]


results = []


def case(sc, desc, pairs):
    """pairs: [(a, b, expected_hit), ...] —— 全部相符=绿, 任一不符=红。"""
    fails = []
    for a, b, exp in pairs:
        try:
            act = hits(a, b)
        except Exception as exc:                      # noqa: BLE001
            act = "EXC:%s" % type(exc).__name__
        if act != exp:
            fails.append((a, b, exp, act))
    results.append((sc, desc, "红" if fails else "绿", fails, len(pairs)))


# --- SC-1  四族两两配对 (6 对), 期望两两命中 --------------------------------
case("SC-1", "四族两两配对", allpairs(
    ["aria-plugin#122", "10CG/aria-plugin#122",
     "10CG/aria-plugin #122", "aria-plugin #122"], True))

# --- SC-1b `/` 两侧与整串首尾的空白 (R1'/C1) --------------------------------
# 规则 1 要求三个切分点各段各自 strip; 本条是唯一覆盖第三个切分点 (`/`-split 之后) 的用例。
case("SC-1b", "`/` 两侧与整串首尾空白", [
    ("10CG / aria-plugin#122", "10CG/aria-plugin#122", True),
    ("  10CG/aria-plugin#122  ", "10CG/aria-plugin#122", True),
    ("10CG/ aria-plugin #122", "10CG/aria-plugin#122", True),
])

# --- SC-2  同 org 同号不同仓, 不得命中 --------------------------------------
case("SC-2", "同 org 同号不同仓",
     [("10CG/Aria#147", "10CG/aria-plugin#147", False)])

# --- SC-3  两侧 org 不同, 命中 (org 不参与) ---------------------------------
case("SC-3", "两侧 org 不同",
     [("10CG/aria-plugin#1", "otherorg/aria-plugin#1", True)])

# --- SC-4  (a) 前导零  (b) number_str 段首空白 ------------------------------
case("SC-4", "前导零 + 段首尾空白",
     [("aria-plugin#007", "aria-plugin#7", True),
      ("aria-plugin# 122", "aria-plugin#122", True)])

# --- SC-5  截断型别名, 不命中 (已知限, 非待修项) ----------------------------
case("SC-5", "截断型别名 (已知限)",
     [("10CG/aria-orch#5", "10CG/aria-orchestrator#5", False)])

# --- SC-5b 分隔符型别名 (真实仓 10CG/10cg.local), 两两命中 ------------------
case("SC-5b", "分隔符型别名", allpairs(
    ["10CG/10cg.local#20", "10CG/10cg-local#20", "10CG/10cg_local#20"], True))

# --- SC-5c 段内空格, 不命中 (钉住授权清单只有三条重写) ----------------------
case("SC-5c", "段内空格 (负控)",
     [("10CG/aria plugin#1", "10CG/aria-plugin#1", False)])

# --- SC-6  不可解析值退回原串精确比较 ---------------------------------------
case("SC-6", "不可解析值 5 配对",
     [("#5", "#5", True),
      ("#5", "#7", False),
      ("10CG/#7", "otherorg/#7", False),      # D3 论域划分的承重断言
      ("no-hash-here", "no-hash-here", True),
      ("repo#abc", "repo#abc", True)])

# --- SC-6b number_str 边界: 4 跨值对不命中 + 5 自配对命中 -------------------
# 注: 4301 位那条在**现状**必绿 —— 现状根本不调 int(), 不可能抛 ValueError。
# 那条异常路径是修复自己引入的 (见 Spec 规则 2 的强制 try/except 要求)。
_BIG = "aria-plugin#" + "9" * 4301
case("SC-6b", "number_str 边界", [
    ("aria-plugin#+7", "aria-plugin#7", False),
    ("aria-plugin#1_0", "aria-plugin#10", False),
    ("aria-plugin#１２３", "aria-plugin#123", False),
    ("aria-plugin#²", "aria-plugin#2", False),
    ("aria-plugin#+7", "aria-plugin#+7", True),
    ("aria-plugin#1_0", "aria-plugin#1_0", True),
    ("aria-plugin#１２３", "aria-plugin#１２３", True),
    ("aria-plugin#²", "aria-plugin#²", True),
    (_BIG, _BIG, True),
])

# --- SC-9  回显未归一原串 (R3' 恢复: D2 极性论证的唯一守护) ------------------
_ORIG = "10CG/aria-plugin #122"
_r9 = linked_issue_overlaps([claim("theirs", _ORIG)], "mine", _ORIG)
_echo = _r9[0]["linked_issue"] if _r9 else None
results.append(("SC-9", "回显未归一原串", "绿" if _echo == _ORIG else "红",
                [] if _echo == _ORIG else [_echo], 1))

# --- SC-10 批次内异常隔离 (R1'/C2) -------------------------------------------
# 全表唯一「一条畸形 + 数条良构」混合批次: 抓「一条坏值毒死整批」这一形态。
_MIXED = [
    claim("track-A", "aria-plugin#500"),
    claim("track-bad", "no-hash-here"),      # 畸形: 无 `#`
    claim("track-B", "aria-plugin#500"),
]
try:
    _r10 = linked_issue_overlaps(_MIXED, "mine", "aria-plugin#500")
    _ids = sorted(d["track_id"] for d in _r10)
    _ok10 = _ids == ["track-A", "track-B"]
    _f10 = [] if _ok10 else [_ids]
except Exception as _e10:                                        # noqa: BLE001
    _ok10, _f10 = False, ["EXC:%s" % type(_e10).__name__]
results.append(("SC-10", "批次内异常隔离", "绿" if _ok10 else "红", _f10, 1))

# --- SC-11 多 `#` 值的切分方向 (R1'/qa-M1) ----------------------------------
case("SC-11", "多 `#` 切分方向", [
    ("repo#7#8", "repo#7#008", True),    # 按最后一个 `#`: left 同为 `repo#7`, 8 == 008
    ("repo#7#8", "repo#8", False),       # left 不同 (`repo#7` vs `repo`)
])

# --- SC-13/14/15 Q7-1 穷举变异测试补的三个零覆盖维度 -------------------------
case("SC-13", "casefold 维度", [
    ("10CG/Aria-Plugin#122", "10CG/aria-plugin#122", True),
    ("ARIA-PLUGIN#5", "aria-plugin#5", True)])
case("SC-14", "number 相等条件", [
    ("aria-plugin#122", "aria-plugin#7", False),
    ("aria-plugin#122", "aria-plugin#123", False)])
case("SC-15", "`/` 取最后一段", [
    ("10CG/sub/aria-plugin#5", "aria-plugin#5", True),
    ("10CG/sub/aria-plugin#5", "othergroup/aria-plugin#5", True)])


# --- 与 Spec baseline 表比对 -------------------------------------------------
# 漂移守卫 (R1'/tech-lead-m3): 本脚本此前把 proposal 的 baseline 表**手抄成常量**,
# proposal 改了它不会红 —— 而本 Spec 对 SC-7 fixture **强制**要求漂移守卫。
# 对别人强制的守卫必须施加给自己, 故改为从 proposal.md 现场解析。
# fail-CLOSED: 解析不到就报错退出, 绝不回退到硬编码 (零证据不得当正证据)。
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROPOSAL = os.path.join(
    _HERE, "..", "..", "openspec", "changes",
    "linked-issue-normalization", "proposal.md",
)


def _parse_spec_table(path):
    """从 proposal.md 的 rule6_note baseline 表解析 {SC: 红/绿} 与证据面集合。"""
    if not os.path.isfile(path):
        sys.exit("FATAL: 找不到 proposal.md (%s) —— 漂移守卫无法核对, 拒绝以硬编码"
                 "常量冒充比对基准。" % path)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    # 单元格可能带 markdown 强调与星标, 如 `| **SC-1b** ⭐ |` / `| **红** |`。
    # 一律先剥 `*` 与 `⭐` 再匹配, 否则守卫会对新增行静默失明 (它自己的漂移面)。
    cell = r"[\s*⭐]*"
    row = re.compile(
        r"^\|" + cell + r"(SC-[0-9a-z]+)" + cell + r"\|"          # SC
        + cell + r"(红|绿)" + cell + r"\|"                          # baseline
        r"[^|]*\|\s*(✅|❌)\s*\|",                                  # 性质 + 证据面
        re.M,
    )
    table, face = {}, set()
    for sc, verdict, ev in row.findall(text):
        table[sc] = verdict
        if ev == "✅":
            face.add(sc)
    if not table:
        sys.exit("FATAL: 在 proposal.md 里解析不到 baseline 表 —— 表格式可能已变更。"
                 "请修本脚本的解析器, 不要改回硬编码。")
    return table, face


SPEC_TABLE, EVIDENCE_FACE = _parse_spec_table(_PROPOSAL)

# SC-8c 是套件级断言 (既有 6 条测试逐字不改全绿), 由 docstring 里的 pytest 命令另测,
# 结构上不属于本脚本的用例面。显式豁免而非静默忽略。
# SC-12 是导出单元的返回契约, 该函数 Phase B 才存在 ⇒ baseline 期无法实测。
_EXTERNALLY_MEASURED = {"SC-12"}

# 双向漂移检查: 脚本测了表里没有的 SC, 或表里有 SC 脚本没测 —— 两个方向都要红。
_measured = {sc for sc, _, _, _, _ in results}
_only_script = _measured - set(SPEC_TABLE)
_only_spec = set(SPEC_TABLE) - _measured - _EXTERNALLY_MEASURED

print("%-8s%-9s%-9s%-8s%s" % ("SC", "子用例", "Spec 表", "实测", "一致?"))
print("-" * 48)
mismatch = []
for sc, desc, verdict, fails, n in results:
    spec = SPEC_TABLE.get(sc, "?")
    if spec != verdict:
        mismatch.append((sc, spec, verdict, fails))
    print("%-8s%-11s%-10s%-9s%s"
          % (sc, n, spec, verdict, "OK" if spec == verdict else "MISMATCH"))

print()
measured_face = {sc for sc, _, v, _, _ in results if v == "红"}
print("substitute 证据面 (实测红): %s" % (sorted(measured_face) or "<空>"))
print("Spec 声称的证据面        : %s" % sorted(EVIDENCE_FACE))
print("证据面一致: %s" % ("YES" if measured_face == EVIDENCE_FACE else "NO"))

if _only_script or _only_spec:
    print("\n### 漂移守卫失败 (脚本 ↔ proposal baseline 表 不同步)")
    if _only_script:
        print("  脚本测了但表里没有: %s" % sorted(_only_script))
    if _only_spec:
        print("  表里有但脚本没测  : %s" % sorted(_only_spec))
    sys.exit(1)

if measured_face != EVIDENCE_FACE:
    print("\n### 证据面不符 —— substitute 论证的承重集合与实测不一致")
    sys.exit(1)

if mismatch:
    print("\n### 不符明细")
    for sc, spec, act, fails in mismatch:
        print("\n[%s] Spec 表写 %s, 实测 %s" % (sc, spec, act))
        for f in fails[:6]:
            print("    %r" % (f,))
    sys.exit(1)

print("\n全部与 Spec 的 baseline 表一致 (SC-8c 另跑 pytest, 见 docstring)。")
