#!/usr/bin/env python3
"""linked-issue-normalization — Spec 机械一致性检查器 (Q7-2, owner 2026-08-06)。

为什么需要它
------------
post_spec R1′/R2′ 两轮里, **「机械同步缺失」是数量最多的一类缺陷**, 且它有一个
关键性质: **加轮只能发现, 不能防止** —— 每一轮 fix 都会再造一批。实测账目:

    R1′  SC-1~6 baseline 假声明 · 「≥12」按旧表算 · terminal 站点漏 4 处
    R2′  artifact 四处行号在同 commit 内全部失效 · 「14/14」vs「17/17」文内打架
         · 「12 项」vs 实际 16 项 · Impact 表仍写「SC-1~9」· 「141 篇」已 142
         · 「≥35」加总本身算错 (应 36)

⇒ 这类缺陷不该由审计席位去抓。本脚本把它们变成**可执行的红**。

检查项 (全部 fail-closed: 数不出来就报错, 不猜)
-----------------------------------------------
  C1  §Success Criteria 表的 SC 集合  ==  baseline 表的 SC 集合 ∪ 外部实测集合
  C2  子用例下界推导的**逐项加总**  ==  它自己写的那个总数
  C3  下界推导枚举的 SC 集合  ==  §Success Criteria 表的 SC 集合
  C4  Impact 表点名的 SC 枚举  ⊇  §Success Criteria 表的 SC 集合
  C5  全文引用的每个 SC-N 都有定义 (或落在 §移出范围 的说明性引用里)
  C6  proposal 引用的 `.aria/repro/*.py` 行号确实指向它声称的内容
  C7  substitute 证据面声称集合  ==  baseline 表里标 ✅ 的集合
  C8  自指语料计数 (141 篇 / 250 文件 等) 必须带 SHA-pin 或「随仓增长」免责

用法
----
    python3 spec-consistency-check.py                 # 用默认路径
    python3 spec-consistency-check.py <proposal.md>

零依赖 (stdlib only)。只读。exit 1 当且仅当有检查项失败。
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.join(HERE, "..", "..", "openspec", "changes",
                       "linked-issue-normalization", "proposal.md")
PROPOSAL = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else DEFAULT)

if not os.path.isfile(PROPOSAL):
    sys.exit("FATAL: 找不到 %s" % PROPOSAL)
TEXT = open(PROPOSAL, encoding="utf-8").read()
LINES = TEXT.split("\n")

failures = []
notes = []


def fail(cid, msg):
    failures.append("[%s] %s" % (cid, msg))


def section(title_re):
    """返回某二级/三级标题到下一个同级标题之间的文本。"""
    m = re.search(r"^(#{2,3}) .*%s.*$" % title_re, TEXT, re.M)
    if not m:
        return None
    level = len(m.group(1))
    start = m.end()
    nxt = re.search(r"^#{1,%d} " % level, TEXT[start:], re.M)
    return TEXT[start:start + nxt.start()] if nxt else TEXT[start:]


CELL = r"[\s*⭐]*"
SC_ROW = re.compile(r"^\|\s*\**\s*(SC-[0-9a-z]+)\**[^|]*\|", re.M)


# --- C1: SC 表 vs baseline 表 -------------------------------------------------
sc_sec = section("Success Criteria")
bl_sec = section("决策记录")          # rule6_note 的 baseline 表在决策记录节内
if sc_sec is None or bl_sec is None:
    fail("C1", "找不到 §Success Criteria 或 §决策记录 —— 标题可能已改名")
    sc_set = bl_set = set()
    bl = []
else:
    sc_set = set(SC_ROW.findall(sc_sec))
    bl_rows = re.compile(r"^\|\s*\**\s*(SC-[0-9a-z]+)\**[^|]*\|\s*\**\s*(红|绿)"
                         r"\s*\**\s*\|[^|]*\|\s*(✅|❌)", re.M)
    bl = bl_rows.findall(bl_sec)
    bl_set = {x[0] for x in bl}
    # 显式标记: SC 行里写「baseline 期无法实测」的, 豁免 baseline 表要求
    ext_sc = {m.group(1) for m in
              re.finditer(r"\|\s*\**\s*(SC-[0-9a-z]+)\**[^\n]*baseline 期无法实测", TEXT)}
    missing_in_bl = sc_set - bl_set - ext_sc
    extra_in_bl = bl_set - sc_set
    if missing_in_bl:
        fail("C1", "SC 表有而 baseline 表无 (且未声明外部实测): %s" % sorted(missing_in_bl))
    if extra_in_bl:
        fail("C1", "baseline 表有而 SC 表无: %s" % sorted(extra_in_bl))
    notes.append("C1: SC 表 %d 条, baseline 表 %d 条" % (len(sc_set), len(bl_set)))

# --- C2 + C3: 下界推导 --------------------------------------------------------
m = re.search(r"下界推导[^\n]*?: (.+?) = \*\*≥(\d+)\*\*", TEXT, re.S)
if not m:
    fail("C2", "找不到「下界推导 … = **≥N**」")
else:
    body, claimed = m.group(1), int(m.group(2))
    terms = []
    for seg in re.split(r"\s\+\s(?![^(]*\))", body):
        sc = re.search(r"(SC-[0-9a-z]+)", seg)
        num = re.findall(r"\*\*(?:≥)?(\d+)\*\*", seg)
        if sc and num:
            terms.append((sc.group(1), num[-1]))
    total = sum(int(v) for _, v in terms)
    if total != claimed:
        fail("C2", "下界逐项加总 = %d, 但文中写 ≥%d" % (total, claimed))
    enum = {t for t, _ in terms}
    if sc_set and enum != sc_set:
        fail("C3", "下界推导枚举的 SC 集合 != SC 表 (少: %s / 多: %s)"
             % (sorted(sc_set - enum), sorted(enum - sc_set)))
    notes.append("C2: 下界逐项加总 %d == 声称 ≥%d" % (total, claimed))

    hdr = re.search(r"子用例下界 \*\*≥(\d+)\*\*", TEXT)
    if hdr and int(hdr.group(1)) != claimed:
        fail("C2", "测试基线行写 ≥%s, 推导行写 ≥%d" % (hdr.group(1), claimed))

# --- C4: Impact 表的 SC 枚举 --------------------------------------------------
imp = re.search(r"^\|[^|\n]*tests/test_release_by_track\.py[^|\n]*\|([^|\n]*)\|", TEXT, re.M)
if not imp:
    fail("C4", "Impact 表里找不到 test_release_by_track.py 行")
elif sc_set:
    listed = set(re.findall(r"SC-[0-9a-z]+", imp.group(1)))
    # 支持「SC-1 / 1b / 2 …」缩写: 把裸编号补全
    listed |= {"SC-" + x for x in re.findall(r"[/·]\s*([0-9]+[a-z]?)\b", imp.group(1))}
    gap = sc_set - listed
    if gap:
        fail("C4", "Impact 表的 SC 枚举漏了: %s" % sorted(gap))
    else:
        notes.append("C4: Impact 表覆盖全部 %d 条 SC" % len(sc_set))

# --- C5: 悬空 SC 引用 ---------------------------------------------------------
moved = section("移出范围") or ""
referenced = set(re.findall(r"SC-[0-9a-z]+", TEXT))
moved_refs = set(re.findall(r"SC-[0-9a-z]+", moved))
dangling = referenced - sc_set - moved_refs
if dangling:
    fail("C5", "被引用但既无定义、也不在 §移出范围 里说明: %s" % sorted(dangling))
else:
    notes.append("C5: 无悬空 SC 引用 (引用 %d 种, 定义 %d, 移出说明 %d)"
                 % (len(referenced), len(sc_set), len(moved_refs)))

# --- C6: artifact 行号引用 ----------------------------------------------------
for m in re.finditer(r"artifact `:(\d+)(?:-(\d+))?`", TEXT):
    fail("C6", "仍存在裸 artifact 行号引用 `:%s` —— R2′ 实证这类引用会在同 commit "
               "内失效, 应改为符号名 (如「SC-7 的 case 块」) 而非行号" % m.group(1))
if not re.search(r"artifact `:\d+", TEXT):
    notes.append("C6: 无裸 artifact 行号引用")

# --- C7: substitute 证据面 ----------------------------------------------------
if bl_sec:
    face_measured = {x[0] for x in bl if x[2] == "✅"}
    fm = re.search(r"substitute 的证据面 = ([^*]*(?:\*\*[^*]*\*\*[^*]*)*?)(?:八|七|六|五|四|三|二|一)?条 baseline-failing", TEXT)
    if fm:
        claimed_face = set(re.findall(r"SC-[0-9a-z]+", fm.group(1)))
        if claimed_face != face_measured:
            fail("C7", "证据面声称 %s, baseline 表标 ✅ 的是 %s"
                 % (sorted(claimed_face), sorted(face_measured)))
        else:
            notes.append("C7: 证据面 %d 条, 与 baseline 表 ✅ 一致" % len(face_measured))
    else:
        fail("C7", "找不到「substitute 的证据面 = …」句")

# --- C8: 自指语料计数须带免责 --------------------------------------------------
# ⚠️ 空真守卫: 若一条检查的**触发模式在文档里零命中**, 它就是恒绿装饰 ——
# 必须当作失败而非通过 (memory feedback_verify_predicate_inputs_exist: 判据打磨
# 到位而它要判的输入不存在)。C8 初版正是如此: 正则要求 `**N 篇**` 而文档写的是
# `**N 篇 tracked proposal**`, 零命中 ⇒ 空真通过, 由负向测试抓出。
C8_PAT = re.compile(r"(\d{2,4})\s*篇\*{0,2}\s*tracked proposal")
c8_hits = list(C8_PAT.finditer(TEXT))
if not c8_hits:
    fail("C8", "触发模式零命中 —— 本检查恒绿, 属装饰。要么文档措辞已变 (修正则), "
               "要么该语料已移除 (删本检查)。**不允许空真通过。**")
for m in c8_hits:
    ctx = TEXT[max(0, m.start() - 400): m.end() + 600]
    if not re.search(r"git archive|随仓增长|只承载定性|SHA", ctx):
        fail("C8", "自指语料计数「%s 篇」附近无 SHA-pin / 「随仓增长」免责 —— "
                   "该语料含本文件自身, 必然漂移" % m.group(1))
if not any(f.startswith("[C8]") for f in failures):
    notes.append("C8: 自指语料计数 %d 处, 均带免责或 SHA-pin" % len(c8_hits))


# --- 输出 ---------------------------------------------------------------------
print("Spec 一致性检查 — %s\n" % os.path.relpath(PROPOSAL, os.path.join(HERE, "..", "..")))
for n in notes:
    print("  ✅ %s" % n)
if failures:
    print("\n### ❌ %d 项失败\n" % len(failures))
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("\n全部检查通过 ✅")
