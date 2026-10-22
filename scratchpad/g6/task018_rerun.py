#!/usr/bin/env python3
# TASK-018 合并后重跑 (v1.75.0 并入 merge b1634dc 后) — 只读核验脚本
# 判据源: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
#   TASK-018 verification 第 1/2/3 条 + metadata.{sc13_baseline,new_checks,canonical_call,crlf_guard}
#   重跑范围对齐 verification-ledger §5.1「合并后重跑」先例 (第 4 条七文件提交不重做, 改为确认合并未碰)
# 纪律: 不 fetch / push / commit / 改 tracked 文件; 只写本 scratchpad 日志。
# 遇 grep 退出 2 或判据不成立: 停在该条, 如实记录。
import subprocess, sys, yaml, hashlib, re, datetime

ROOT = "/home/dev/Aria"
ARIA = ROOT + "/aria"
LOGP = ROOT + "/scratchpad/g6/logs/task018-rerun.log"
REF = "d9097cf"           # 派单指定的 frontmatter 参照 (aria B.1 侧轨点; 5.1 先例用 5215cf2, 见判读备注)
REF_ALT = "5215cf2"       # 台账 1.1 记录的 B.1 起点, 仅辅助对照
GG = "/usr/bin/grep"

EM   = "aria/skills/audit-engine/references/execution-modes.md"
AESK = "aria/skills/audit-engine/SKILL.md"
PCSK = "aria/skills/phase-c-integrator/SKILL.md"
PASK = "aria/skills/phase-a-planner/SKILL.md"
PBSK = "aria/skills/phase-b-developer/SKILL.md"
RS   = "aria/skills/audit-engine/references/report-storage.md"
CG   = "aria/skills/audit-engine/scripts/completeness_gate.py"
SEVEN = [EM, AESK, PCSK, PASK, PBSK, RS,
         "aria/skills/audit-engine/references/pre-write-validation.md"]
FOUR = [AESK, PCSK, PASK, PBSK]

log_f = open(LOGP, "a", encoding="utf-8")
results = []   # (编号, 名称, verdict, note)

def hdr(t):
    line = "\n" + t
    print(line); log_f.write(line + "\n"); log_f.flush()

def rec(no, name, verdict, note=""):
    results.append((no, name, verdict, note))
    line = f"VERDICT[{no}] {name}: {verdict} {note}"
    print(line); log_f.write(line + "\n"); log_f.flush()

def run(cmd, cwd=ROOT):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

def show_cmd(no, name, cmd):
    line = f"=== ({no}) {name}\nCMD: {' '.join(cmd)}"
    print(line); log_f.write(line + "\n")
    return None

def log_rc_out(rc, out, err=""):
    line = f"RC: {rc}\nOUT:\n{out.rstrip(chr(10)) if out.strip() else '<empty>'}"
    if err.strip():
        line += f"\nERR:\n{err.rstrip(chr(0x0a))}"
    print(line); log_f.write(line + "\n"); log_f.flush()
    return rc, out

def gcount(no, name, pattern, path, expect):  # expect: int 期望计数
    cmd = [GG, "-c", pattern, path]
    show_cmd(no, name, cmd)
    rc, out, _e = run(cmd)
    log_rc_out(rc, out)
    if rc == 2:
        rec(no, name, "STOP", "grep 退出 2 (文件不存在或路径写错), 不得读作 0")
        return False
    if rc not in (0, 1):
        rec(no, name, "STOP", f"grep 退出 {rc} 不在 0/1 集合, 没跑成")
        return False
    try:
        n = int(out.strip())
    except ValueError:
        rec(no, name, "STOP", f"grep -c 输出非数字: {out!r}")
        return False
    ok = (n == expect) if isinstance(expect, int) else expect(n)
    if expect == 0 and isinstance(expect, int):
        ok = (rc == 1 and n == 0)   # 「为 0」判据: 退出 1 且输出 0
    rec(no, name, "PASS" if ok else "FAIL",
        f"计数 {n} (rc={rc}); 期望 {expect if not callable(expect) else '满足谓词'}")
    return ok

M = yaml.safe_load(open(f"{ROOT}/openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml", encoding="utf-8"))["metadata"]

hdr(f"# TASK-018 合并后重跑 — {datetime.datetime.now().isoformat()}")
hdr("# aria HEAD 预备核验")
rc, out, err = run(["git", "-C", ARIA, "rev-parse", "HEAD"]); log_rc_out(rc, out)
assert_ok = out.strip() == "b1634dc76ce003ee50b1873c4ae1db88f6f07db3"
rc2, out2, _ = run(["git", "-C", ARIA, "status", "--porcelain"]); n_por = len([l for l in out2.splitlines() if l.strip()])
rec("0a", "aria HEAD == b1634dc", "PASS" if assert_ok else "FAIL", out.strip())
rec("0b", "aria porcelain 干净", "PASS" if (rc2 == 0 and n_por == 0) else "FAIL", f"rc={rc2} 行数={n_por}")

em_t   = open(f"{ROOT}/{EM}",   encoding="utf-8").read()
ae_t   = open(f"{ROOT}/{AESK}", encoding="utf-8").read()
pc_t   = open(f"{ROOT}/{PCSK}", encoding="utf-8").read()

def fenced_bash_lines(text):
    """返回 (bash/sh 围栏内行号集合 1-based, 全部围栏行号->lang)"""
    lines = text.split("\n"); inb = False; lang = ""; inner = set(); fence = {}
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if s.startswith("```") and not inb:
            inb = True; lang = s[3:].strip(); fence[i] = lang
        elif s.startswith("```") and inb:
            inb = False; fence[i] = "close"
        elif inb and lang in ("bash", "sh"):
            inner.add(i)
    return inner

# ---------------- 派单 (1) SC-13 全部条目 ----------------
hdr("## (1) SC-13 全部条目 (计数在主仓根以全路径跑; grep -c rc 须 0/1, rc=2 停)")

gcount("1-R1", "EM 通配模式计数=0 (基线 2; 须 rc=1 且输出 0)", r"{checkpoint_name}-\*\.md", EM, 0)

# R2: completeness_gate.py >=1 且至少一行命中在 bash 块内
cmd = [GG, "-n", "completeness_gate.py", AESK]; show_cmd("1-R2", "AE SKILL 含 completeness_gate.py 且命中行在 bash 块内", cmd)
rc, out, _e = run(cmd); log_rc_out(rc, out)
hit_lines = [int(l.split(":", 1)[0]) for l in out.splitlines() if l.strip()]
bashset = fenced_bash_lines(ae_t)
inb_hits = [h for h in hit_lines if h in bashset]
rec("1-R2", "AE completeness_gate.py 命中行在 bash 块内", "PASS" if (rc in (0,1) and hit_lines and inb_hits) else "FAIL",
    f"全文命中 {len(hit_lines)} 行 {hit_lines}, 其中 bash 块内 {inb_hits}; 判读: SC-13 原文「块外不设计数约束……属有意的提及」+ 5.1 先例按「至少一处在块内」判成立")

# R3: PC change_id >= 基线 3 + 1 = 4
cmd = [GG, "-c", "change_id", PCSK]; show_cmd("1-R3", "PC change_id 计数较基线 3 至少 +1 (>=4)", cmd)
rc, out, _e = run(cmd); log_rc_out(rc, out)
rec("1-R3", "PC change_id >= 4", "PASS" if (rc == 0 and int(out.strip()) >= 4) else "FAIL",
    f"计数 {out.strip()} (rc={rc}, 基线 3)")

# R4 (与派单 (5) 同一条命令, 双引用): timestamp 残留
hdr("## (5) = SC-13 timestamp 条 — 原文第 3 条 grep -rn (零命中 = rc=1 且无输出)")
cmd = [GG, "-rn", r"audit-reports/[a-z_]*-{timestamp}\.md", "aria/skills/"]
show_cmd("5/1-R4", "主仓根 grep -rn timestamp 残留 (零命中)", cmd)
rc, out, _e = run(cmd); log_rc_out(rc, out)
if rc == 2:
    rec("5/1-R4", "timestamp 残留", "STOP", "退出 2: aria/skills/ 不在当前目录下或不可读, 没查成")
elif rc == 1 and not out.strip():
    rec("5/1-R4", "timestamp 残留 = 0", "PASS", "退出 1 且无输出")
else:
    rec("5/1-R4", "timestamp 残留", "FAIL", f"rc={rc}, 输出:\n{out}")

gcount("1-R5", "RS 不计入 >=1 (基线 0)", "不计入", RS, lambda n: n >= 1)
gcount("1-R6", "RS 子目录句 =1 (基线 0)", "子目录内的报告不计入完整性证据", RS, 1)
gcount("1-R7", "RS 三个桶都不收 =1 (基线 0)", "三个桶都不收", RS, 1)
gcount("1-R8", "EM adaptive_rules >= 基线 3 + 1 = 4", "adaptive_rules", EM, lambda n: n >= 4)

# R9: EM 内 bypassed 两处 WARN 文案逐字相同 (基线 :44 by config / :82 missing= 两种拼法)
hdr("### 1-R9 EM bypassed 两处文案逐字相同")
warn_re = re.compile(r"\[WARN\] incomplete checkpoint gate bypassed:.*?\{0\|1\}")
matches = warn_re.findall(em_t)
line = f"提取 (regex \\[WARN\\] incomplete checkpoint gate bypassed:.*?{{0|1}}): {len(matches)} 处"
print(line); log_f.write(line + "\n")
for m_ in matches:
    print("  >> " + m_); log_f.write("  >> " + m_ + "\n")
rec("1-R9", "EM bypassed 两处逐字相同", "PASS" if (len(matches) == 2 and matches[0] == matches[1]) else "FAIL",
    f"{len(matches)} 处, 逐字相同={matches[0] == matches[1] if len(matches) == 2 else 'n/a'} (基线两种拼法)")

# R10: AE SKILL 的 bash 块切片内 scripts/completeness_gate.py 恰 1
bashlines = sorted(fenced_bash_lines(ae_t))
n_in = sum(1 for i in bashlines if "scripts/completeness_gate.py" in ae_t.split("\n")[i-1])
line = f"bash/sh 围栏内行数 {len(bashlines)}, 其中含 scripts/completeness_gate.py 的行数 = {n_in}"
print(line); log_f.write(line + "\n")
rec("1-R10", "AE bash 切片内调用串恰 1", "PASS" if n_in == 1 else "FAIL", f"{n_in} (期望恰 1)")

# R11: EM Step4:..Step5: 行区间内恰 1 (与 n4/slice_lines 同口径)
L = em_t.split("\n")
try:
    s = next(i for i, l in enumerate(L) if re.match(r"\s*Step 4:", l))
    e = next(i for i in range(s + 1, len(L)) if re.match(r"\s*Step 5:", L[i]))
    sl = L[s:e]
    n_em = sum(1 for l in sl if "scripts/completeness_gate.py" in l)
    line = f"Step4 起行 {s+1} 至 Step5 前行 {e} (不含), 区间 {len(sl)} 行, 含调用串行数 = {n_em}"
    print(line); log_f.write(line + "\n")
    rec("1-R11", "EM Step4 区间内调用串恰 1", "PASS" if n_em == 1 else "FAIL", f"{n_em} (期望恰 1)")
except StopIteration:
    rec("1-R11", "EM Step4 区间内调用串恰 1", "FAIL", "Step 4:/Step 5: 锚点行未找到, 没切出来")

# R12pre: PC checkpoints 显式值串 + anchor_base (SC-13 R5 前置两条)
gcount("1-R12a", "PC 含『checkpoints 显式值 > adaptive_rules 推导值』>=1 (基线 0)", "checkpoints 显式值 > adaptive_rules 推导值", PCSK, lambda n: n >= 1)
gcount("1-R12b", "PC 含 anchor_base >=1 (基线 0)", "anchor_base", PCSK, lambda n: n >= 1)

# R13 (R5 rework 五条):
gcount("1-R13a1", "EM『stdout 非 JSON』=1 (基线 0)", "stdout 非 JSON", EM, 1)
# 命中行所在段落含 不得按 PASS
hit = [i for i, l in enumerate(L) if "stdout 非 JSON" in l]
para_ok = False
if len(hit) == 1:
    i = hit[0]; a = i
    while a > 0 and L[a-1].strip(): a -= 1
    b = i
    while b < len(L)-1 and L[b+1].strip(): b += 1
    para = "\n".join(L[a:b+1]); para_ok = "不得按 PASS" in para
    line = f"命中行 {i+1} 所在段落 ({a+1}-{b+1}) 含『不得按 PASS』= {para_ok}"
    print(line); log_f.write(line + "\n")
rec("1-R13a2", "EM stdout-非-JSON 命中行段落含『不得按 PASS』", "PASS" if para_ok else "FAIL", "")
gcount("1-R13b1", "PC『4.5 completeness gate 三态处置』=1 (基线 0)", "4.5 completeness gate 三态处置", PCSK, 1)
gcount("1-R13b2", "PC『not_applicable → workflow report 必带』>=1 (基线 0)", "not_applicable → workflow report 必带", PCSK, lambda n: n >= 1)
gcount("1-R13b3", "PC『unattributed_count > 0』>=1 (基线 0)", "unattributed_count > 0", PCSK, lambda n: n >= 1)
# 入口逻辑节
L2 = em_t.split("\n")
try:
    a = next(i for i, l in enumerate(L2) if re.match(r"##\s*入口逻辑", l))
    b = next(i for i in range(a + 1, len(L2)) if L2[i].startswith("## "))
    sec = "\n".join(L2[a:b])
    c1 = sec.count("checkpoints 显式值 > adaptive_rules 推导值"); c2 = sec.count("入口层不解析")
    line = f"## 入口逻辑 节 (行 {a+1}-{b}) 内: checkpoints 显式串 {c1} / 入口层不解析 {c2}"
    print(line); log_f.write(line + "\n")
    rec("1-R13c", "EM 入口逻辑节两串 >=1", "PASS" if (c1 >= 1 and c2 >= 1) else "FAIL", f"{c1}/{c2}")
except StopIteration:
    rec("1-R13c", "EM 入口逻辑节两串 >=1", "FAIL", "## 入口逻辑 节未切出")
gcount("1-R13d1", "EM 旧句『跳过校验, 继续执行 pre_merge 审计』=0 (基线 1; 须 rc=1 且输出 0)", "跳过校验, 继续执行 pre_merge 审计", EM, 0)
gcount("1-R13d2", "EM 新句『仍逐对评估三态并全部留痕』>=1 (基线 0)", "仍逐对评估三态并全部留痕", EM, lambda n: n >= 1)
gcount("1-R13e1", "PC『mode == \"convergence\"』>=1 (基线 0)", 'mode == "convergence"', PCSK, lambda n: n >= 1)
gcount("1-R13e2", "PC『mode == \"challenge\"』>=1 (基线 0)", 'mode == "challenge"', PCSK, lambda n: n >= 1)
gcount("1-R13e3", "PC『照常调用门』>=1 (基线 0)", "照常调用门", PCSK, lambda n: n >= 1)

# ---------------- 派单 (2) new_checks n1/n2/n3/n4/n8 ----------------
hdr("## (2) metadata.new_checks: n1/n2/n3/n4/n8 (代码自 yaml 原样 exec)")
ns = {}
exec(M["new_checks"]["code"], ns)
CANON = M["canonical_call"].rstrip("\n").split("\n")   # 5.1 先例: 末尾换行先 rstrip 再 split
hdr("canonical_call 按行切分 (%d 行):" % len(CANON))
for cl in CANON:
    print("  | " + cl); log_f.write("  | " + cl + "\n")

r1 = ns["n1"](em_t); rec("2-n1", "n1(EM) Step3 区间两条排除行各恰 1", "PASS" if r1 else "FAIL", f"n1 -> {r1}")
r2 = ns["n2"](em_t); rec("2-n2", "n2(EM) Step2 区间改写句", "PASS" if r2 else "FAIL", f"n2 -> {r2}")
r3 = ns["n3"](f"{ROOT}/{CG}"); rec("2-n3", "n3(completeness_gate.py) stdlib-only", "PASS" if r3 else "FAIL", f"n3 -> {r3}")
r4 = ns["n4"](ae_t, em_t, CANON); rec("2-n4", "n4 = 两段调用串 == canonical (= SC-13 R12)", "PASS" if r4 else "FAIL", f"n4 -> {r4}")
r8 = ns["n8"](pc_t, ae_t); rec("2-n8", "n8(PC+AE) 无旧字面键 + 三锚点", "PASS" if r8 else "FAIL", f"n8 -> {r8}")

# ---------------- 派单 (3) crlf_guard ----------------
hdr("## (3) metadata.crlf_guard 对两个 CRLF 文件 (代码自 yaml 原样 exec; 在 aria 仓内跑)")
g = {}
exec(M["crlf_guard"]["code"], g)
for rel in M["crlf_guard"]["files"]:
    rel_in_aria = rel[len("aria/"):]   # files 键是主仓根相对路径; guard 在 aria 仓内跑
    cmd = ["git", "-C", ARIA, "ls-files", "--eol", "--", rel_in_aria]
    show_cmd("3-crlf", f"crlf_guard 前置 ls-files --eol {rel_in_aria}", cmd)
    rc, out, _e = run(cmd, cwd=ARIA); log_rc_out(rc, out)
    try:
        ok = g["crlf_guard"](ARIA, rel_in_aria)
        rec("3-crlf", f"crlf_guard({rel_in_aria})", "PASS" if ok else "FAIL",
            f"-> {ok}; 判读: 改动已提交 (porcelain 空), numstat 两侧同为空串 ⇒ 后半真空成立, 有区分力的是 eol 断言 i/crlf w/crlf; 同形态判读见 5.1 先例")
    except Exception as ex:
        rec("3-crlf", f"crlf_guard({rel_in_aria})", "STOP", f"guard 抛异常 (git 失败): {ex!r}")

# ---------------- 派单 (4) 四份 SKILL.md frontmatter vs d9097cf ----------------
hdr(f"## (4) 四份 SKILL.md frontmatter 与 {REF} 逐字相同 (CRLF 先去 CR; 两侧块非空且含 description: 行)")
CRLF_FILES = {"phase-b-developer", "phase-c-integrator"}
def frontmatter_block(data: bytes, is_crlf: bool):
    if is_crlf:
        data = data.replace(b"\r", b"")
    lines = data.split(b"\n")
    if not lines or lines[0] != b"---":
        return None
    for i in range(1, len(lines)):
        if lines[i] == b"---":
            return b"\n".join(lines[1:i])
    return None

for path in FOUR:
    name = path.split("/")[2]
    is_crlf = name in CRLF_FILES
    wt = open(f"{ROOT}/{path}", "rb").read()
    rc_ref, ref_b, _ = run(["git", "-C", ARIA, "show", f"{REF}:skills/{name}/SKILL.md"], cwd=ROOT)
    rc_alt, alt_b, _ = run(["git", "-C", ARIA, "show", f"{REF_ALT}:skills/{name}/SKILL.md"], cwd=ROOT)
    ref_b = ref_b.encode("utf-8"); alt_b = alt_b.encode("utf-8")
    line = f"git -C aria show {REF}:skills/{name}/SKILL.md -> rc={rc_ref} ({len(ref_b)}B); {REF_ALT} rc={rc_alt} ({len(alt_b)}B); 工作树 {len(wt)}B; CRLF={is_crlf}"
    print(line); log_f.write(line + "\n")
    bw = frontmatter_block(wt, is_crlf); br = frontmatter_block(ref_b, is_crlf)
    if bw is None or br is None:
        rec("4-fm", f"{name} frontmatter", "FAIL", "切块为 None (首行非 --- 或无闭合)")
        continue
    nonempty = len(bw.strip()) > 0 and len(br.strip()) > 0
    hasdesc = any(l.strip().startswith(b"description:") for l in bw.split(b"\n")) and \
              any(l.strip().startswith(b"description:") for l in br.split(b"\n"))
    same = bw == br
    sha_w = hashlib.sha256(bw).hexdigest()[:16]; sha_r = hashlib.sha256(br).hexdigest()[:16]
    ba = frontmatter_block(alt_b, is_crlf)
    alt_note = f"; 对照 {REF_ALT} 块 sha256[0:16]={hashlib.sha256(ba).hexdigest()[:16] if ba else 'None'}" if rc_alt == 0 else ""
    rec("4-fm", f"{name} frontmatter vs {REF}", "PASS" if (nonempty and hasdesc and same) else "FAIL",
        f"非空={nonempty} 含description:={hasdesc} 逐字相同={same}; 工作树块 sha256[0:16]={sha_w} 参照块={sha_r}{alt_note}")

# ---------------- 派单 (6) b1634dc 改动清单不含七文件与四份 SKILL.md ----------------
hdr("## (6) 合并提交 b1634dc 改动文件清单核验")
cmd = ["git", "-C", ARIA, "show", "--name-only", "--format=", "b1634dc"]
show_cmd("6-merge", "git -C aria show --name-only b1634dc", cmd)
rc, out, _e = run(cmd, cwd=ARIA); log_rc_out(rc, out)
changed = [l.strip() for l in out.splitlines() if l.strip()]
watch = {p[len("aria/"):] for p in SEVEN + FOUR}
inter = sorted(set(changed) & watch)
rec("6-merge", "b1634dc 名单不含组 3 七文件与四份 SKILL.md", "PASS" if (rc == 0 and not inter) else "FAIL",
    f"名单 {len(changed)} 个文件; 与七文件+四 SKILL.md 交集 = {inter if inter else '空'}")

# ---------------- 汇总 ----------------
hdr("## 汇总")
fails = [r for r in results if r[2] != "PASS"]
for no, name, v, note in results:
    line = f"[{v}] ({no}) {name}" + (f" — {note}" if note and v != "PASS" else "")
    print(line); log_f.write(line + "\n")
hdr(f"TOTAL={len(results)} PASS={len(results)-len(fails)} FAIL/STOP={len(fails)}")
hdr("# 判读备注 (两处, 供主控摘录):")
hdr(f"# 备注 A — 参照点: 派单指定 frontmatter 参照为 {REF}; 台账 1.1 与 5.1 先例记的 aria B.1 起点为 {REF_ALT} (v1.74.0), {REF} 是 5.1 阶段并入 v1.74.1 后的 merge commit。因 v1.74.1 (5.1 已核, 14 文件不触组 3 七文件) 与组 3 改动均不动四份 frontmatter, 两参照应同块; 上表 (4-fm) 各行附 {REF_ALT} 块 sha256 佐证。")
hdr("# 备注 B — crlf_guard: 本轮跑在已提交态 (porcelain 空), guard 的 numstat 比较两侧同为空串 ⇒ 后半真空成立, 有区分力的是 eol 断言 i/crlf w/crlf; 有区分力的完整运行在组 3 提交前 (主控与 3.5 机检各一次, 均真), 与 5.1 先例判读同形态。")
hdr("# 备注 C — SC-13 completeness_gate.py 全文计数: 命中含散文处 (块外属有意提及, 原文不设计数约束), 判据按『至少一处在 bash 块内』判, 同 5.1 先例判读。")
log_f.close()
sys.exit(0 if not fails else 1)
