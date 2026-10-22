#!/usr/bin/env python3
"""TASK-027 step 7, part P2: TASK-018 doc checks on the merged tree (aria master 500e6c2).

- SC-13 entries: real `grep -c` (subprocess /usr/bin/grep) so exit-code criteria hold
  (rc 0/1 allowed; rc 2 = file missing = stop; the two "=0" greps require rc==1 and count 0).
- n1/n2/n3/n4/n8: metadata.new_checks.code exec'd verbatim from the yaml.
- crlf_guard: metadata.crlf_guard.code exec'd verbatim, run for both files.
- frontmatter: four SKILL.md vs feature HEAD a4e7028 (awk per metadata.crlf_guard.frontmatter_rule;
  CRLF files de-CR'd first), both sides non-empty and containing a description: line.
Run from the main repo root. Read-only.
"""
import subprocess, sys, yaml

MAIN = "/home/dev/Aria"
ARIA = MAIN + "/aria"
YAML_PATH = MAIN + "/openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml"
GREP = "/usr/bin/grep"
EM = ARIA + "/skills/audit-engine/references/execution-modes.md"
RS = ARIA + "/skills/audit-engine/references/report-storage.md"
AESK = ARIA + "/skills/audit-engine/SKILL.md"
PCSK = ARIA + "/skills/phase-c-integrator/SKILL.md"
GATE = ARIA + "/skills/audit-engine/scripts/completeness_gate.py"
REF = "a4e7028"  # feature branch HEAD = merge second parent
PASS, FAIL = [], []


def check(num, desc, ok, detail=""):
    (PASS if ok else FAIL).append(num)
    print(f"{'PASS' if ok else 'FAIL'}  [{num}] {desc}" + (f"\n        {detail}" if detail and not ok else ""))
    if detail and ok:
        print(f"        {detail}")


def gcount(pattern, path):
    """grep -c with real exit code; returns (count, rc). count None when rc==2."""
    p = subprocess.run([GREP, "-c", pattern, path], capture_output=True, text=True)
    cnt = int(p.stdout.strip()) if p.stdout.strip().isdigit() else None
    return cnt, p.returncode


def read(p):
    return open(p, encoding="utf-8").read()


M = yaml.safe_load(open(YAML_PATH, encoding="utf-8"))

print("=" * 72)
print("[P2] TASK-018 doc checks — merged tree (aria master 500e6c2)")
print("=" * 72)
print("\n-- P2.a SC-13 entries (proposal :469; baseline = metadata.sc13_baseline)")

# 1. EM wildcard count 0 (rc must be 1 and output 0)
c, rc = gcount(r"{checkpoint_name}-\*\.md", EM)
check("SC13.1", f"EM '{'{checkpoint_name}-*.md'}' wildcard count 0 (rc=1,count=0); got rc={rc} count={c}",
      rc == 1 and c == 0)

# 2. AE fenced bash blocks contain exactly 1 'scripts/completeness_gate.py'
ae_text = read(AESK)
import re as _re
blocks = _re.findall(r"```(?:bash|sh)\s*\n([\s\S]*?)```", ae_text)
inblock = sum(b.count("scripts/completeness_gate.py") for b in blocks)
whole = ae_text.count("completeness_gate.py")
check("SC13.2", f"AE fenced bash/sh blocks contain 'scripts/completeness_gate.py' exactly 1; got {inblock}",
      inblock == 1, f"blocks={len(blocks)}, whole-file 'completeness_gate.py' mentions={whole}")

# 3. PC change_id count >= baseline 3 + 1
c, rc = gcount("change_id", PCSK)
check("SC13.3", f"PC 'change_id' >= 4 (baseline 3, +>=1); got rc={rc} count={c}", rc == 0 and c >= 4)

# 4. timestamp leftovers grep -rn over aria/skills/ : rc must be 1, no output
p = subprocess.run([GREP, "-rn", r"audit-reports/[a-z_]*-{timestamp}\.md", MAIN + "/aria/skills/"],
                   capture_output=True, text=True)
check("SC13.4", f"grep -rn timestamp pattern over aria/skills/: rc={p.returncode} (expect 1), "
      f"stdout {'empty' if not p.stdout else 'HAS OUTPUT: ' + p.stdout[:120]}",
      p.returncode == 1 and p.stdout == "")

# 5-7. report-storage three literals
c5, rc5 = gcount("不计入", RS)
check("SC13.5", f"RS '不计入' >= 1; got rc={rc5} count={c5}", rc5 == 0 and c5 >= 1)
c6, rc6 = gcount("子目录内的报告不计入完整性证据", RS)
check("SC13.6", f"RS '子目录内的报告不计入完整性证据' == 1; got rc={rc6} count={c6}", rc6 == 0 and c6 == 1)
c7, rc7 = gcount("三个桶都不收", RS)
check("SC13.7", f"RS '三个桶都不收' == 1; got rc={rc7} count={c7}", rc7 == 0 and c7 == 1)

# 8. EM adaptive_rules >= baseline 3 + 1
c, rc = gcount("adaptive_rules", EM)
check("SC13.8", f"EM 'adaptive_rules' >= 4 (baseline 3, +>=1); got rc={rc} count={c}", rc == 0 and c >= 4)

# 9. EM two bypassed WARN message texts identical (baseline two spellings: ":44 by config"
#    vs ":82 missing="). Executable form: old spelling count 0, unified spelling exactly 2.
em_text = read(EM)
OLD_SPELL = "bypassed by config"
UNI_SPELL = "bypassed: missing={cp}@{change_id},... ; scope_unresolved={0|1}"
n_old = em_text.count(OLD_SPELL)
n_uni = em_text.count(UNI_SPELL)
check("SC13.9", f"EM bypassed: old spelling count 0 (got {n_old}), unified spelling exactly 2 (got {n_uni})",
      n_old == 0 and n_uni == 2)

# 10. EM Step4:..Step5: slice exactly 1 call-string line with script path
L = em_text.split("\n")
try:
    s = next(i for i, l in enumerate(L) if _re.match(r"\s*Step 4:", l))
    e = next(i for i in range(s + 1, len(L)) if _re.match(r"\s*Step 5:", L[i]))
    sl = L[s:e]
    n10 = sum("scripts/completeness_gate.py" in l for l in sl)
except StopIteration:
    sl, n10, s, e = None, -1, -1, -1
check("SC13.10", f"EM Step4:..Step5: slice 'scripts/completeness_gate.py' exactly 1; got {n10} "
      f"(slice lines {s}..{e})", n10 == 1)

# 12. R4 seam greps
c, rc = gcount("checkpoints 显式值 > adaptive_rules 推导值", PCSK)
check("SC13.12a", f"PC 'checkpoints 显式值 > adaptive_rules 推导值' >= 1; got rc={rc} count={c}", rc == 0 and c >= 1)
c, rc = gcount("anchor_base", PCSK)
check("SC13.12b", f"PC 'anchor_base' >= 1; got rc={rc} count={c}", rc == 0 and c >= 1)

# 13. R5(1): EM 'stdout 非 JSON' == 1 AND its paragraph contains '不得按 PASS'
c, rc = gcount("stdout 非 JSON", EM)
hit_lines = [i for i, l in enumerate(L) if "stdout 非 JSON" in l]
para_ok = False
if len(hit_lines) == 1:
    i = hit_lines[0]
    a = i
    while a > 0 and L[a - 1].strip():
        a -= 1
    b = i
    while b < len(L) - 1 and L[b + 1].strip():
        b += 1
    para_ok = any("不得按 PASS" in L[j] for j in range(a, b + 1))
check("SC13.13", f"R5(1) EM 'stdout 非 JSON' ==1 (rc={rc}, count={c}) and paragraph contains '不得按 PASS': {para_ok}",
      rc == 0 and c == 1 and para_ok)

# 14. R5(2)
c, rc = gcount("4.5 completeness gate 三态处置", PCSK)
pc_text = read(PCSK)
check("SC13.14a", f"PC '4.5 completeness gate 三态处置' == 1; got rc={rc} count={c}", rc == 0 and c == 1)
c1, rc1 = gcount("not_applicable → workflow report 必带", PCSK)
c2, rc2 = gcount("unattributed_count > 0", PCSK)
check("SC13.14b", f"PC 'not_applicable → workflow report 必带' >=1 ({c1}) and 'unattributed_count > 0' >=1 ({c2})",
      rc1 == 0 and c1 >= 1 and rc2 == 0 and c2 >= 1)

# 15. R5(3): EM '## 入口逻辑' section
try:
    s2 = next(i for i, l in enumerate(L) if l.startswith("## 入口逻辑"))
    e2 = next(i for i in range(s2 + 1, len(L)) if L[i].startswith("## "))
    sec = "\n".join(L[s2:e2])
except StopIteration:
    sec, s2, e2 = "", -1, -1
check("SC13.15", f"R5(3) EM 入口逻辑 section contains both literals (lines {s2}..{e2})",
      "checkpoints 显式值 > adaptive_rules 推导值" in sec and "入口层不解析" in sec)

# 16. R5(4)
c, rc = gcount("跳过校验, 继续执行 pre_merge 审计", EM)
check("SC13.16a", f"R5(4) EM old sentence count 0 (rc must be 1); got rc={rc} count={c}", rc == 1 and c == 0)
c, rc = gcount("仍逐对评估三态并全部留痕", EM)
check("SC13.16b", f"R5(4) EM '仍逐对评估三态并全部留痕' >= 1; got rc={rc} count={c}", rc == 0 and c >= 1)

# 17. R5(5)
c1, r1 = gcount('mode == "convergence"', PCSK)
c2, r2 = gcount('mode == "challenge"', PCSK)
c3, r3 = gcount("照常调用门", PCSK)
check("SC13.17", f"R5(5) PC convergence {c1} / challenge {c2} / 照常调用门 {c3} all >=1",
      r1 == 0 and c1 >= 1 and r2 == 0 and c2 >= 1 and r3 == 0 and c3 >= 1)

MD = M["metadata"]

print("\n-- P2.b metadata.new_checks exec'd verbatim (n1/n2/n3/n4/n8)")
ns = {}
exec(MD["new_checks"]["code"], ns)
n1 = ns["n1"](em_text)
n2 = ns["n2"](em_text)
n3 = ns["n3"](GATE)
canonical_lines = MD["canonical_call"].rstrip("\n").split("\n")
n4 = ns["n4"](ae_text, em_text, canonical_lines)
n8 = ns["n8"](pc_text, ae_text)
check("N1", "n1 (Step3 exclusion lines) on execution-modes.md", n1)
check("N2", "n2 (Step2 rewrite sentence) on execution-modes.md", n2)
check("N3", "n3 (stdlib-only imports) on completeness_gate.py", n3)
check("N4", "n4 call strings == canonical_call (AE blocks + EM Step4..5 slice)", n4)
check("N8", "n8 (no literal-key gate, priority-chain anchors)", n8)

print("\n-- P2.c metadata.crlf_guard exec'd verbatim (both CRLF files)")
ns2 = {}
exec(MD["crlf_guard"]["code"], ns2)
cg = ns2["crlf_guard"]
for rel in MD["crlf_guard"]["files"]:
    rel_in_aria = rel.split("aria/", 1)[1]
    try:
        v = cg(ARIA, rel_in_aria)
    except subprocess.CalledProcessError as ex:
        v = f"CALLED-PROCESS-ERROR: {ex}"
    eol = subprocess.run(["git", "-C", ARIA, "ls-files", "--eol", "--", rel_in_aria],
                         capture_output=True, text=True, check=True).stdout.strip()
    check(f"CRLF[{rel_in_aria}]", f"crlf_guard() -> {v} (eol: {eol})", v is True,
          "eol half discriminative; numstat half vacuous-true on committed tree (5.1/5.3 same-form reading)")

print("\n-- P2.d frontmatter of four SKILL.md vs feature HEAD a4e7028 (merge must not touch it)")
FM_FILES = [  # (path-in-aria, eol)
    ("skills/audit-engine/SKILL.md", "lf"),
    ("skills/phase-c-integrator/SKILL.md", "crlf"),
    ("skills/phase-b-developer/SKILL.md", "crlf"),
    ("skills/phase-a-planner/SKILL.md", "lf"),
]
AWK = r"""awk 'NR==1&&$0=="---"{f=1;next} f&&$0=="---"{exit} f'"""
for rel, eol in FM_FILES:
    def fm(txt):
        t = txt.replace("\r", "") if eol == "crlf" else txt
        lines = t.split("\n")
        if not lines or lines[0] != "---":
            return None
        out = []
        for l in lines[1:]:
            if l == "---":
                return "\n".join(out)
            out.append(l)
        return None
    cur = fm(read(ARIA + "/" + rel))
    show = subprocess.run(["git", "-C", ARIA, "show", f"{REF}:{rel}"], capture_output=True, text=True, check=True)
    ref = fm(show.stdout)
    ok = (cur is not None and ref is not None and cur == ref
          and "description:" in cur and "description:" in ref)
    detail = (f"cur_block={'None' if cur is None else str(len(cur.splitlines())) + ' lines, desc=' + str('description:' in cur)}, "
              f"ref_block={'None' if ref is None else str(len(ref.splitlines())) + ' lines, desc=' + str('description:' in ref)}")
    check(f"FM[{rel}]", f"frontmatter identical to {REF} ({eol.upper()}, non-empty, has description:)", ok, detail)

print("\n-- P2.e (supporting) merge did not touch group-3 seven files + four SKILL.md vs a4e7028")
grp3 = subprocess.run(["git", "-C", ARIA, "show", "97d4d0eb", "--name-only", "--format="],
                      capture_output=True, text=True, check=True).stdout.split()
targets = sorted(set(grp3) | {rel for rel, _ in FM_FILES})
d = subprocess.run(["git", "-C", ARIA, "diff", "--stat", REF, "HEAD", "--", *targets],
                   capture_output=True, text=True, check=True)
check("P2.e", f"git diff {REF}..HEAD over group-3 files + 4 SKILL.md is empty", d.stdout == "",
      d.stdout[:400])
print(f"        group-3 commit 97d4d0eb files: {grp3}")

print()
print(f"[P2 summary] pass={len(PASS)} fail={len(FAIL)}" + (f"  FAILED: {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
