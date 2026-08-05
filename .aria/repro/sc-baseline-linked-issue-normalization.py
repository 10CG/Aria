#!/usr/bin/env python3
"""linked-issue-normalization — SC-1~9 baseline 实测 (Rule #6 substitute 的证据载体)。

用途
----
OpenSpec `linked-issue-normalization` 的 rule6_note 走 **substitute 框定**: 判据表
第一行「描述性 (schema / 字段 / 命令 / 勘正)」⇒ 以「SC 级 baseline-failing 结构化测试」
替代 AB benchmark。owner 2026-08-02 裁定 (`db2e983`) 要求 **substitute 须实证而非声称**。

本脚本就是那份实证: 对**未修复的现状** `lib/collision.py::linked_issue_overlaps`
逐条跑 Spec §Success Criteria 的 SC-1~9, 输出每条的真实红/绿, 与 Spec 的 baseline
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

首次实测: 2026-08-05, aria 子模块 af87cae (v1.65.5) —— 14/14 与 Spec baseline 表一致。
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

# --- SC-7  等价关系三性质 ----------------------------------------------------
# 判别力自陈: 任何「算 key 再比较」的实现都自动满足三性质 ⇒ 回归护栏, 不是主判据。
# 现状 (裸 != ) 平凡满足, 故 baseline 必绿。
_CORPUS = ["aria-plugin#122", "10CG/aria-plugin#122", "10CG/aria-plugin #122",
           "aria-plugin #122", "10CG/Aria#147", "#5", "repo#abc", "aria-plugin#007"]
_viol = []
for _a in _CORPUS:
    if not hits(_a, _a):
        _viol.append(("自反", _a, _a))
for _a, _b in itertools.permutations(_CORPUS, 2):
    if hits(_a, _b) != hits(_b, _a):
        _viol.append(("对称", _a, _b))
for _a, _b, _c in itertools.permutations(_CORPUS, 3):
    if hits(_a, _b) and hits(_b, _c) and not hits(_a, _c):
        _viol.append(("传递", "%s|%s" % (_a, _b), _c))
results.append(("SC-7", "等价关系三性质", "红" if _viol else "绿",
                _viol[:3], len(_CORPUS) * 3))

# --- SC-8a 签名冻结 ----------------------------------------------------------
import inspect                                                    # noqa: E402
_params = list(inspect.signature(linked_issue_overlaps).parameters)
_EXP_PARAMS = ["claims", "own_track_id", "own_linked_issue"]
results.append(("SC-8a", "签名冻结", "绿" if _params == _EXP_PARAMS else "红",
                [] if _params == _EXP_PARAMS else [(_EXP_PARAMS, _params)], 1))

# --- SC-8b 返回 key-set 冻结 -------------------------------------------------
_r = linked_issue_overlaps([claim("theirs", "A#7")], "mine", "A#7")
_keys = sorted(_r[0].keys()) if _r else []
_EXP_KEYS = ["claimed_at", "container", "linked_issue", "owner",
             "session", "status", "track_id"]
results.append(("SC-8b", "返回 key-set 冻结", "绿" if _keys == _EXP_KEYS else "红",
                [] if _keys == _EXP_KEYS else [(_EXP_KEYS, _keys)], 1))

# --- SC-9  回显未归一原串 ----------------------------------------------------
_ORIG = "10CG/aria-plugin #122"
_r = linked_issue_overlaps([claim("theirs", _ORIG)], "mine", _ORIG)
_echoed = _r[0]["linked_issue"] if _r else None
results.append(("SC-9", "回显未归一原串", "绿" if _echoed == _ORIG else "红",
                [] if _echoed == _ORIG else [_echoed], 1))


# --- 与 Spec baseline 表比对 -------------------------------------------------
SPEC_TABLE = {
    "SC-1": "红", "SC-2": "绿", "SC-3": "红", "SC-4": "红", "SC-5": "绿",
    "SC-5b": "红", "SC-5c": "绿", "SC-6": "绿", "SC-6b": "绿", "SC-7": "绿",
    "SC-8a": "绿", "SC-8b": "绿", "SC-9": "绿",
}
EVIDENCE_FACE = {"SC-1", "SC-3", "SC-4", "SC-5b"}

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

if mismatch:
    print("\n### 不符明细")
    for sc, spec, act, fails in mismatch:
        print("\n[%s] Spec 表写 %s, 实测 %s" % (sc, spec, act))
        for f in fails[:6]:
            print("    %r" % (f,))
    sys.exit(1)

print("\n全部与 Spec 的 baseline 表一致 (SC-8c 另跑 pytest, 见 docstring)。")
