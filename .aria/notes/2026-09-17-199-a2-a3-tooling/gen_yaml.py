#!/usr/bin/env python3
"""Generate detailed-tasks.yaml for pre-merge-completeness-gate-change-scope (A.3 v1).

usage: python3 gen_yaml.py <out.yaml> <a2_state_runs.py> <state-runs output file or '-'>
Lists are always indented (the archive gate's line parser drops indentless `- ` items).
"""
import sys
import yaml

OUT, SCRIPT, RUNOUT, SCRIPT2, RUNOUT2 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
SID = "pre-merge-completeness-gate-change-scope"
SPEC = f"openspec/changes/{SID}"
LEDGER = f"{SPEC}/verification-ledger.md"
AE = "aria/skills/audit-engine"
PC = "aria/skills/phase-c-integrator"


class Dumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def _str(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


Dumper.add_representer(str, _str)

script_text = open(SCRIPT, encoding="utf-8").read()
run_output = "(pending)\n" if RUNOUT == "-" else open(RUNOUT, encoding="utf-8").read()
script2_text = open(SCRIPT2, encoding="utf-8").read()
run_output2 = "(pending)\n" if RUNOUT2 == "-" else open(RUNOUT2, encoding="utf-8").read()

SC12_CODE = r'''# 在主仓根执行: python3 -B sc12_liveness.py [--force-checked]
# --force-checked: 4.3 用 (tasks.md 尚未勾选时把副本文本临时视为全勾选, 只影响 L3; L1 须在全勾选的 scratch 副本里跑)
import json, re, subprocess, sys
from pathlib import Path
root = Path.cwd()
sys.path.insert(0, str(root / "aria/skills/state-scanner/scripts"))  # 包上下文; 直接 import spec_complete 会循环导入
from lib import spec_complete as sc
spec = root / "openspec/changes/pre-merge-completeness-gate-change-scope"
text = (spec / "tasks.md").read_text(encoding="utf-8")
if "--force-checked" in sys.argv:
    text = re.sub(r"^(\s*[-*]\s*)\[ \]", r"\1[x]", text, flags=re.M)
item = next(i for i in sc._iter_task_items(text) if i["parent_id"] == "3.2")
L3 = (item["checked"] and sc._line_has_integration_keyword(item["line"])
      and "completeness_gate" in sc.extract_claim_symbols(spec, item)["symbols"])
lv = sc.classify_symbol_liveness("completeness_gate", root, {"aria/skills/audit-engine/scripts/completeness_gate.py"})
L2 = lv["status"] == "alive" and "aria_plugin_integration" in lv["alive_categories"]
p = subprocess.run([sys.executable, "-B", str(root / "aria/skills/state-scanner/scripts/lib/spec_complete.py"),
                    "--gate", str(spec)], capture_output=True, text=True)
g = json.loads(p.stdout)
L1 = g["verdict"] != "block" and not any("completeness_gate" in b for b in g["blocking_reasons"])
print(json.dumps({"L1": L1, "L2": L2, "L3": L3, "status": lv["status"],
                  "alive_categories": lv["alive_categories"], "gate_verdict": g["verdict"],
                  "unverified_claims": [u["reason"] for u in g["unverified_claims"]]}, ensure_ascii=False))
'''

NEW_CHECKS = r'''# N1 / N2 的输入 = execution-modes.md 全文; N3 的输入 = completeness_gate.py 路径
import ast, re, sys
def slice_lines(text, a, b):
    L = text.split("\n")
    s = next(i for i, l in enumerate(L) if re.match(a, l))
    e = next(i for i in range(s + 1, len(L)) if re.match(b, L[i]))
    return L[s:e]
def n1(text):  # Step 3 行区间内两条同构排除行各恰 1 行
    try:
        sl = slice_lines(text, r"\s*Step 3:", r"\s*Step 4:")
    except StopIteration:
        return False
    return all(sum(bool(re.match(rf'\s*- key != "{k}"', l)) for l in sl) == 1
               for k in ("post_brainstorm", "mid_implementation"))
def n2(text):  # Step 2 行区间内唯一的改写句: 分号前含 no_spec_unverifiable, 分号后不含它且含 no_spec_contradicted 与 不被本键豁免
    try:
        sl = slice_lines(text, r"\s*Step 2:", r"\s*Step 3:")
    except StopIteration:
        return False
    hits = [l for l in sl if "仍逐对评估三态并全部留痕" in l]
    if len(hits) != 1:
        return False
    head, sep, tail = hits[0].partition(";")
    return (bool(sep) and "no_spec_unverifiable" in head and "no_spec_unverifiable" not in tail
            and "no_spec_contradicted" in tail and "不被本键豁免" in tail)
def n3(path):  # 顶层 import 全属 stdlib; 相对导入算不合格
    from pathlib import Path
    path = Path(path)
    if not path.is_file():
        return False
    mods = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add("<relative>" if node.level else (node.module or "").split(".")[0])
    return bool(mods) and mods <= set(sys.stdlib_module_names)
def _call_lines(lines):  # 恰一行含脚本路径; 从该行起连续取以 \\ 结尾的续行, 到第一行不以 \\ 结尾为止, 逐行 strip()
    idx = [i for i, l in enumerate(lines) if "scripts/completeness_gate.py" in l]
    if len(idx) != 1:
        return None
    out, i = [], idx[0]
    while i < len(lines):
        out.append(lines[i].strip())
        if not lines[i].rstrip().endswith("\\"):
            break
        i += 1
    return out
def n4(skill_text, em_text, canonical_lines):  # SKILL.md 全部 ```bash/```sh 块 与 execution-modes.md 的 Step 4: 至 Step 5: 行区间, 各自抽出的调用串都等于 canonical
    blocks = [l for b in re.findall(r"```(?:bash|sh)\s*\n([\s\S]*?)```", skill_text) for l in b.split("\n")]
    try:
        em = slice_lines(em_text, r"\s*Step 4:", r"\s*Step 5:")
    except StopIteration:
        return False
    want = [l.strip() for l in canonical_lines]
    return _call_lines(blocks) == want and _call_lines(em) == want
P8 = "pre_merge 按 C.2 pre_hook 步骤 3 的优先级链判为启用"
def _anchored(text, anchor):
    hits = [l for l in text.split("\n") if anchor in l]
    return len(hits) == 1 and P8 in hits[0] and '!= "off"' not in hits[0] and "!= off" not in hits[0]
def n8(pc_text, ae_text):  # pc = phase-c-integrator/SKILL.md 全文, ae = audit-engine/SKILL.md 全文
    return ('audit.checkpoints.pre_merge != "off"' not in pc_text
            and _anchored(pc_text, "C.2 合并前触发 audit-engine")
            and _anchored(pc_text, "C.2 的 pre_merge audit 调用点")
            and _anchored(ae_text, "与 file-scope 过滤双降级时幂等"))
'''

CANONICAL_CALL = '''python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/completeness_gate.py" \\
  --repo-path "<主仓 root>" --diff-repo-path "<C.2 合并目标仓 root>" \\
  --base "<diff 仓主干的远程跟踪 ref>" [--anchor-base "<主仓主干的远程跟踪 ref>"] \\
  [--change-id <id> ...] [--no-spec]
'''

CELL_STATUS_CODE = r'''# 用法: cd aria/skills/audit-engine/tests && python3 -B <scratch>/cell_status.py test_completeness_gate <cell>...
# 列出的每个 cell 恰被执行一次且通过 ⇒ 退出 0; 未执行 / 失败 / 执行多次 ⇒ 退出 1。本文件放 scratch, 不进仓
import json, sys, unittest
module, cells = sys.argv[1], sys.argv[2:]
sys.path.insert(0, ".")
seen = {}
class Result(unittest.TestResult):
    def addSubTest(self, test, subtest, outcome):
        super().addSubTest(test, subtest, outcome)
        cell = subtest.params.get("cell") if hasattr(subtest, "params") else None
        if cell is not None:
            seen.setdefault(cell, []).append("pass" if outcome is None else "fail")
unittest.defaultTestLoader.loadTestsFromName(module).run(Result())
status = {c: seen.get(c, ["not-run"]) for c in cells}
ok = bool(cells) and all(v == ["pass"] for v in status.values())
print(json.dumps(status, ensure_ascii=False, sort_keys=True))
sys.exit(0 if ok else 1)
'''

COORD_PRECHECK_CODE = r'''# 用法 (在主仓根): python3 -B <scratch>/coord_precheck.py <本轨 claim 文件>...   例: claims/023236f2/s-86f7@1836.yaml
# 退出 0 = 本地协调 ref 相对 origin 只领先本轨心跳 (可强制对齐; 对齐后才可推送 —— 该态含「与 origin 分叉」, 分叉时
# 不对齐直接推必被拒, v2.6 post_planning R6 2c2e8931); 1 = 含其它写入 (停下请授权); 2 = 取不到远端值 (按 1 处置)
# v2.5 (post_planning R5 同族扫描): rev-parse FETCH_HEAD 与 rev-list 的失败也退出 2 —— 旧写法里它们的失败落成空串 / 空列表,
# 被读成「无领先提交」而判 ok
import json, subprocess, sys
own = set(sys.argv[1:])
def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True)
if git("fetch", "origin", "refs/aria/coordination").returncode != 0:  # 只写 FETCH_HEAD
    print(json.dumps({"verdict": "error", "reason": "fetch failed"})); sys.exit(2)
rp = git("rev-parse", "FETCH_HEAD")
remote = rp.stdout.strip()
if rp.returncode != 0 or not remote:
    print(json.dumps({"verdict": "error", "reason": "FETCH_HEAD unresolved"})); sys.exit(2)
local = git("rev-parse", "--verify", "-q", "refs/aria/coordination").stdout.strip()
ahead = []
rl = git("rev-list", "--reverse", f"{remote}..{local}") if local else None  # local 为空 = 本地没有该 ref, 无可领先
if rl is not None and rl.returncode != 0:
    print(json.dumps({"verdict": "error", "reason": "rev-list failed"})); sys.exit(2)
for c in (rl.stdout.split() if rl is not None else []):
    files = git("diff-tree", "--no-commit-id", "--name-only", "-r", c).stdout.split()
    body = git("diff", "-U0", f"{c}^", c, "--", *files).stdout.splitlines() if files else []
    changed = [l for l in body if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    hb = (bool(files) and set(files) <= own and len(changed) == 2 * len(files)
          and all(l[1:].startswith("heartbeat_at:") for l in changed))
    ahead.append({"files": files, "kind": "own-heartbeat" if hb else "other"})
ok = all(a["kind"] == "own-heartbeat" for a in ahead)
print(json.dumps({"verdict": "ok" if ok else "stop", "local_ahead": len(ahead), "ahead": ahead}, ensure_ascii=False))
sys.exit(0 if ok else 1)
'''

CRLF_GUARD_CODE = r'''import subprocess
def crlf_guard(repo, rel):  # 在改动未暂存时跑: 工作树仍全为 CRLF, 且忽略行尾 CR 与否的 numstat 相同
    def run(*a):  # check=True (v2.5): git 失败即抛异常, 不再让两侧同为空串的 numstat 比较恒真
        return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout
    eol = run("ls-files", "--eol", "--", rel).split()
    return eol[:2] == ["i/crlf", "w/crlf"] and run("diff", "--numstat", "--", rel) == run("diff", "--ignore-cr-at-eol", "--numstat", "--", rel)
'''

ATTRIB_CODE = r"""# 用法 (在主仓根): python3 -B <scratch>/commit_attribution.py <基准 ref> <目标 ref> [<本次 ab-results 目录>]
# 退出 0 = 基准..目标 之间只有本轨提交与同步合并; 1 = 含非本轨提交 (停下请裁); 2 = git log 读不出 基准..目标 (ref 写错
# 或对象缺失), 没跑成 —— v2.5 (post_planning R5 同族扫描) 补: 旧写法把 git log 的失败读成零提交而判 ok
# v2.2 收紧 (post_planning R2 PP2-M3): 路径分三类 —— exclusive (本轨专属) / shared (主仓发布同步面,
# 并发发版轨同样会整条改) / foreign。单亲提交判 own 需同时满足 (a) 无 foreign 文件, 且 (b) 有 exclusive
# 文件, 或提交信息带本轨 Spec: trailer (git-commit.md §6.2 既有写法)。「整条提交全落 shared 集」不再
# 单独构成 own —— 那正是他轨 chore(release) 主仓同步面的形态。
# v2.3 补正 (post_planning R3 R3-M2): exclusive 前缀集补入本轨工具目录 TOOLING。v2.2 漏了它, 真提交
# 12c870d (工具目录的 gen_yaml.py + 本目录 tasks.md 与 detailed-tasks.yaml) 因此被判 foreign。
import json, re, subprocess, sys
SID = "pre-merge-completeness-gate-change-scope"
TOOLING = ".aria/notes/2026-09-17-199-a2-a3-tooling/"  # 本轨 A.2/A.3 工具目录 (生成器 + 席位提示词), 结构上本轨专属
base, tip, extra = sys.argv[1], sys.argv[2], [d.rstrip("/") + "/" for d in sys.argv[3:]]
SHARED = {"aria", "VERSION", "README.md", "README.zh.md", "README.ja.md", "README.ko.md", "CLAUDE.md",
"docs/architecture/system-architecture.md", "docs/architecture/version-scheme.md",
"aria-plugin-benchmarks/ab-suite/audit-engine.json", "aria-plugin-benchmarks/ab-suite/version.yaml"}
TRAILER = re.compile(r"^Spec:\s+openspec/changes/" + re.escape(SID) + r"(?:\s|$)", re.M)
def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True)
def exclusive(c, p):
    if p in SHARED:
        return False
    if p.startswith(f"openspec/changes/{SID}/") or p.startswith(TOOLING) or (extra and p.startswith(tuple(extra))):
        return True
    seg = p.split("/")
    if p.startswith("openspec/archive/") and len(seg) > 2 and seg[2].endswith(f"-{SID}"):
        return True
    if p.startswith(".aria/audit-reports/") and SID in p:
        return True
    if p.startswith("docs/handoff/") and p.endswith(".md"):  # 本轨周期 / 会话 handoff: frontmatter track-id 为本轨
        head = git("show", f"{c}:{p}").stdout[:2000]
        return re.search(rf"^track-id:\s*{re.escape(SID)}\s*$", head, re.M) is not None
    return False
def klass(c, p):
    if exclusive(c, p):
        return "exclusive"
    return "shared" if p in SHARED else "foreign"
kinds = []
lg = git("log", "--format=%H %P", f"{base}..{tip}")
if lg.returncode != 0:
    print(json.dumps({"verdict": "error", "reason": "git log failed", "commits": 0, "kinds": []})); sys.exit(2)
for line in lg.stdout.splitlines():
    c, *parents = line.split()
    if len(parents) > 1:
        sync = all(git("merge-base", "--is-ancestor", p, base).returncode == 0 for p in parents[1:])
        kinds.append("sync-merge" if sync else "foreign-merge")
        continue
    ks = [klass(c, p) for p in git("diff-tree", "--no-commit-id", "--name-only", "-r", c).stdout.split()]
    if not ks or "foreign" in ks:
        kinds.append("foreign")
    elif "exclusive" in ks:
        kinds.append("own")
    elif TRAILER.search(git("show", "-s", "--format=%B", c).stdout):
        kinds.append("own-release-sync")
    else:
        kinds.append("shared-only")
ok = all(k in ("own", "own-release-sync", "sync-merge") for k in kinds)
print(json.dumps({"verdict": "ok" if ok else "stop", "commits": len(kinds), "kinds": kinds}))
sys.exit(0 if ok else 1)
"""

DERIV_SCRIPT = r'''# 用法 (在主仓根): python3 -B standards_files_derivation.py
# 输入只取冻结快照 (standards 940cb5b, 主仓 71c500e), 与工作树当前内容无关; 输出无路径、无时间
import collections, re, subprocess
STD_REV, PLAN_REV = "940cb5b", "71c500e"
PLAN = ["openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md",
        "openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md",
        ".aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py"]
EXCLUDE = {  # 封闭清单: 命中处都不指 standards 内的同名文件 (理由逐族写在 standards_files_basis)
    "README.md": "主仓 README.md / aria/README.md / archive 目录的 README.md, 另有本排除说明自身的点名",
    "README.zh.md": "主仓 i18n README (TASK-029 的版本同步面)",
    "tasks.md": "本目录 tasks.md, 另有本排除说明自身的点名",
}
def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout
md = [f for f in git("-C", "standards", "ls-tree", "-r", "--name-only", STD_REV).split() if f.endswith(".md")]
fam = collections.defaultdict(list)
for f in md:
    fam[f.rsplit("/", 1)[-1]].append(f)
texts = [git("show", f"{PLAN_REV}:{p}") for p in PLAN]
print(f"step 1 (literal): standards {STD_REV} .md = {len(md)} files / {len(fam)} basename families; plan files @ {PLAN_REV} = {len(PLAN)}")
hit = {}
for b in sorted(fam):
    c = [t.count(b) for t in texts]
    if sum(c):
        hit[b] = c
        print(f"  hit {b}: members={len(fam[b])} counts(proposal, tasks, generator)={c} excluded={'yes' if b in EXCLUDE else 'no'}")
literal = sorted(fam[b][0] for b in hit if b not in EXCLUDE)
print(f"  families hit = {len(hit)}; excluded = {len([b for b in hit if b in EXCLUDE])} (closed list); kept = {len(literal)}")
print(f"  kept: {literal}")
claude = git("show", f"{PLAN_REV}:CLAUDE.md").split("## 不可协商规则", 1)[1].split("\n## ", 1)[0]
sot = {}
for chunk in re.split(r"(?m)^(?=\d+\. \*\*)", claude):
    m = re.match(r"(\d+)\. \*\*", chunk)
    if m:
        s = re.search(r"SOT: `([^`\s]+)", chunk)
        sot[int(m.group(1))] = s.group(1) if s else None
cited = sorted({int(n) for t in texts for n in re.findall(r"Rule #(\d+)", t)})
print(f"step 2 (Rule #N -> SOT, CLAUDE.md @ {PLAN_REV}): cited = {cited}")
extra = []
for n in cited:
    s = sot.get(n)
    where = "none" if s is None else ("standards" if s.startswith("standards/") else "outside standards")
    rel = s[len("standards/"):] if where == "standards" else None
    new = rel is not None and rel not in literal
    print(f"  Rule #{n} -> {s} [{where}]" + (" [not found by step 1]" if new else ""))
    if new:
        extra.append(rel)
print(f"  standards-resident SOT not found by step 1: {extra}")
print(f"result (step 1 kept + step 2 candidates judged dependent): {len(literal) + len(extra)} files")
'''

DERIV_OUTPUT = r'''step 1 (literal): standards 940cb5b .md = 102 files / 88 basename families; plan files @ 71c500e = 3
  hit README.md: members=7 counts(proposal, tasks, generator)=[3, 0, 8] excluded=yes
  hit README.zh.md: members=1 counts(proposal, tasks, generator)=[0, 0, 3] excluded=yes
  hit configured-gate-authority.md: members=1 counts(proposal, tasks, generator)=[8, 1, 2] excluded=no
  hit content-integrity.md: members=1 counts(proposal, tasks, generator)=[0, 2, 5] excluded=no
  hit git-commit.md: members=1 counts(proposal, tasks, generator)=[0, 2, 6] excluded=no
  hit project.md: members=1 counts(proposal, tasks, generator)=[3, 2, 2] excluded=no
  hit proposal-minimal.md: members=1 counts(proposal, tasks, generator)=[3, 2, 2] excluded=no
  hit skill-benchmark-exemption.md: members=1 counts(proposal, tasks, generator)=[2, 1, 5] excluded=no
  hit tasks.md: members=1 counts(proposal, tasks, generator)=[21, 6, 52] excluded=yes
  hit version-management.md: members=1 counts(proposal, tasks, generator)=[1, 1, 2] excluded=no
  families hit = 10; excluded = 3 (closed list); kept = 7
  kept: ['conventions/configured-gate-authority.md', 'conventions/content-integrity.md', 'conventions/git-commit.md', 'conventions/skill-benchmark-exemption.md', 'conventions/version-management.md', 'openspec/project.md', 'openspec/templates/proposal-minimal.md']
step 2 (Rule #N -> SOT, CLAUDE.md @ 71c500e): cited = [3, 5, 6, 8, 9, 10]
  Rule #3 -> None [none]
  Rule #5 -> None [none]
  Rule #6 -> standards/conventions/skill-benchmark-exemption.md [standards]
  Rule #8 -> aria/skills/phase-c-integrator/SKILL.md [outside standards]
  Rule #9 -> standards/conventions/session-handoff.md [standards] [not found by step 1]
  Rule #10 -> standards/conventions/configured-gate-authority.md [standards]
  standards-resident SOT not found by step 1: ['conventions/session-handoff.md']
result (step 1 kept + step 2 candidates judged dependent): 8 files
'''

SC17_5 = ("SC-17(5) 改写后全文 (裁定 11; 替换 proposal :473 的 (5) 格): --repo-path tmpA --diff-repo-path tmpB --no-spec, "
          "tmpA 的 feature 分支相对 --anchor-base 无提交 (锚点面零 diff), config {audit: {enabled: true, mode: manual, "
          "checkpoints: {post_spec: convergence}}}。(a) 不加豁免键 ⇒ verdict error, error_kind no_spec_unverifiable, exit 2; "
          "(b) 只加 allow_dangling_change_ids: true ⇒ 同 (a); (c) 加 allow_incomplete_checkpoints: true ⇒ verdict bypassed, "
          "exit 0, error_kind 为 None, scope_source 为 None, change_ids == [], results == [], bypassed 为 True, "
          "checked_checkpoints == ['post_spec'], stderr 逐字含 scope_unresolved=1 与 [WARN] bypassed: no_spec_unverifiable; "
          "(d) 对照: 沿用 (c) 的旗标, 把 tmpA 的锚点面 diff 改为触 openspec/changes/x/ ⇒ error_kind no_spec_contradicted, exit 2。"
          "反事实: 不给该 error 挂豁免 ⇒ (c) exit 2 ⇒ 红; 豁免误挂到 allow_dangling_change_ids ⇒ (b) exit 0 ⇒ 红; "
          "no_spec_contradicted 也被豁免 ⇒ (d) exit 0 ⇒ 红")


def T(id_, parent, title, complexity, hours, deps, deliverables, agent, reason, verification, notes=None):
    t = {"id": id_, "parent": parent, "title": title, "status": "pending", "complexity": complexity,
         "estimated_hours": hours, "dependencies": deps, "deliverables": deliverables,
         "agent": agent, "reason": reason, "verification": verification}
    if notes:
        t["notes"] = notes
    return t


COUNTERFACTUAL_METHOD = (
    "做法 (TASK-019 / 020 / 022 共用): git -C aria worktree add <scratch>/cf-<SC> <TASK-013 SHA> → 未打补丁跑对应用例, 绿 (留输出) "
    "→ 只回退该组件后再跑, 红 (留输出, 记首个失败断言文本) → 记副本 HEAD 与补丁 diff (以副本路径为根) → 在副本里 git checkout -- . 撤掉补丁 → git -C aria worktree remove <副本> (带补丁直接 remove 会 rc=128); "
    "一律 python3 -B; 不在 feature 分支工作树上改; 副本创建与移除记台账")

tasks = [
    # ---------------- 组 1 ----------------
    T("TASK-001", "1.1", "B.1 入口: owner 等待点、读 claim 并心跳、fetch 定分支起点、基线复核、台账骨架", "S", "2-3", [],
      [LEDGER], "qa-engineer", "核验与记录; git 与 claim 动作由主控执行",
      [
          "入口前置 (owner_gates 第 1 项): 10CG/Aria#195 已完成 C.2 —— 判据 = 该轨台账或周期 handoff 记下的主仓 PR 合并提交 M, 与 git fetch origin 后 git ls-remote origin master 取得的 R 满足 git merge-base --is-ancestor M R 退出 0; 或 owner 在会话里明示改序 (原话记台账)。两者都没有 ⇒ 不进 B.1",
          "claim 身份 (按 (本容器, 归一 track_id, active) 三元组运行时解析, 不钉死文件名): 本容器 id = python3 -c \"import sys; sys.path.insert(0, 'aria/skills/state-scanner'); from lib.identity import get_container_id; print(get_container_id())\"; 候选集 = git ls-tree -r --name-only refs/aria/coordination 中前缀为 claims/<本容器 id>/ 的条目, 逐条 git show 读 YAML (ls-tree 与每次 show 的退出码都须为 0 —— 本地没有该 ref 或对象缺失时 ls-tree 退出 128、输出为空, 与「一条都没有」同形, 不得当作 0 条走第 14 项, 先停下查明; v2.5, post_planning R5 同族扫描), 留下 track_id 逐字等于 pre-merge-completeness-gate-change-scope 的条目 (derive_track_id 对该串为恒等, 已实测)。按 status 分流: 恰 1 条 active ⇒ 该文件即本轨 claim 文件; 0 条 active (解析到 done / yielded / abandoned, 或本容器该轨一条都没有) ⇒ 以强制对齐后的重解析为准 —— 本地协调 ref 可能落后 origin: 照下面的前置检查条 (本轨文件集为空) 与心跳条的对齐步做完再解析一次 (v2.5), 仍为 0 条才走 owner_gates 第 14 项, 未获授权不心跳、不认领, 停在本任务; 2 条及以上 active ⇒ 不假设唯一 —— 这是已知缺陷 10CG/aria-plugin#202 的形态 (同容器换 session 再跑认领闸会新建第二条), 判据 = 全部列入本轨 claim 文件集 (heartbeat_by_track 按同一三元组全匹配刷新, 与 coord_ref_precheck 的 own 集必须一致), 条数与文件名记台账并上报, 不自行删除或释放多余条目",
          "claim 身份的实测锚 (为什么必须运行时解析, 不是写死): A.2 2026-09-17 在容器 023236f2 上该三元组解析到 claims/023236f2/s-86f7@1836.yaml (active, phase A.2); 同一三元组 2026-09-19 在容器 bfe8285d 上解析到 claims/bfe8285d/s-73b9@1606.yaml (active, phase A.2), 而前者已转 yielded ⇒ 任何写死文件名的读法在换容器或换认领后即失效, 且会让 coord_ref_precheck 首跑就判 other 而停",
          "协调 ref 前置检查: 跑 metadata.coord_ref_precheck, 参数 = 上一步解析出的本轨 claim 文件 (可多条), 输出原样记台账: 退出非 0 ⇒ 停在本任务 (owner_gates 第 15 项), 不调 /state-scanner、不心跳推送、不强制对齐。本地落后 origin 不影响判定 (检查只看本地领先的提交)",
          "心跳 (precheck 退出 0 之后): 先把本地协调 ref 强制对齐到 origin —— git fetch origin +refs/aria/coordination:refs/aria/coordination (即 TASK-024 的「结束后先取第二次快照」条所引 AB_TEST_OPERATIONS.md 场景 1 第 3 步的命令, 须退出 0): 上一条的前置检查刚证实本地领先 origin 的只有本轨心跳, 对齐丢掉的也只是它们; 不对齐时, 心跳不自己 fetch, 提交叠在落后的本地值上, 推送是非快进, 而 resilient_push 的重取用非强制 refspec, 分叉即被拒, 推送必然失败 (v2.5, post_planning R5 R5-M2; metadata.v2_state_runs 的 N11 实测)。对齐后按本任务的 claim 身份条重跑三元组解析: 0 条 active ⇒ owner_gates 第 14 项 —— 被 sweep 成 abandoned 的 claim 在落后的本地值上仍显示 active, 只有对齐后才看得见 (N11 实测)。然后 python3 -B aria/skills/state-scanner/scripts/phase1_gate.py --heartbeat-only --raw-track-id pre-merge-completeness-gate-change-scope --phase B --repo-path <主仓根>, 按 metadata.coord_push_verify 核验推送: 期望 outcome == refreshed 且 push_success == true 且 push_skipped == false, 再独立跑 git ls-remote origin refs/aria/coordination 与本地 git rev-parse refs/aria/coordination 比对 (不等时不直接判失败: 先 git fetch origin refs/aria/coordination, 本地值是 FETCH_HEAD 的祖先 ⇒ 他容器在本次推送后又叠加, 属正常; 否则停); 任一不成立 ⇒ 停在本任务并按 owner_gates 第 15 项上报, 不重试、不 force。outcome 为 error 且 reason 为 claim_not_found ⇒ 本容器该轨已无 active claim (heartbeat_by_track 只匹配 active, 对三个终态一律不刷新), 按上一步的 0 条分流走 owner_gates 第 14 项。心跳只推 origin 的 refs/aria/coordination, owner 2026-09-17 裁定免逐次授权, 不加 --no-push —— 因此 push_skipped 为 true 即说明会话环境不对 (带了 ARIA_COORDINATION_NO_PUSH), 按 owner_gates 第 15 项停; 第 15 项自身那条降级路径要求心跳加 --no-push, 那一跑的期望值相反 (push_skipped == true 且 push_success == false) 且不做 ls-remote 核验 —— 它本来就没推。心跳只写 heartbeat_at, 不改 claim 的 phase (track board 在 B–D 期间仍显示 A.2), 台账注明。重新认领 (获 owner_gates 第 14 项授权后): 再跑一次 precheck, 退出 0 后同样先强制对齐 (同本条上面那条 git fetch origin +refs/aria/coordination:refs/aria/coordination, 须退出 0 —— 认领写的也是协调 ref, 分叉态下不对齐照样推不出去; v2.6, post_planning R6 2c2e8931), 才用同一原串认领 phase1_gate.py --raw-track-id pre-merge-completeness-gate-change-scope --phase B --mode advisory --linked-issue 10CG/Aria#199 --include-terminal --repo-path <主仓根>, 认领的推送同样按 metadata.coord_push_verify 核验 (认领路径输出同样带 push_success / push_skipped 三键); 认领后重跑三元组解析并以解析结果替换本轨 claim 文件集; 未获授权 ⇒ 不认领, 停在本任务。会话入口核验 (hard_constraints 第 4 条) 走到这里时, 重新认领的 --phase 取当时所在阶段 (B / C / D), 停点是当前任务 (v2.5)。不补容器后缀; 解析到 active 时不重跑认领 (tasks.md 判断清单第 11 条)。输出原样记台账",
          "会话环境: [ -n \"${ARIA_COORDINATION_NO_PUSH+x}\" ] 的结果记台账; 组 1–4 的会话应不带该变量 (tasks.md 读前必看第 12 条), 带则换会话",
          "分支起点: git fetch origin 与 git -C aria fetch origin (两者都须退出 0, 否则下面记下的 origin/master 是旧值; v2.5) 后, 记 git rev-parse origin/master、git -C aria rev-parse origin/master、git ls-tree HEAD aria, 另对 github 各跑 git ls-remote github master 比对; aria feature 分支从 aria origin/master 起。主仓: 本目录规划文件与 post_planning 报告所在的最新提交 P 满足 git merge-base --is-ancestor P <origin 与 github 各自 ls-remote SHA> 均退出 0 ⇒ 从 origin/master 起; 否则按 owner_gates 第 2 项的步骤请授权推送规划提交; 未获授权则从含 P 的本地 master 起, 起点 SHA 与未推送事实记台账, 推送随 TASK-030 的 PR 发生。回落前对 origin/master..<起点> 跑 metadata.commit_attribution, 退出非 0 ⇒ 停 (第 16 项), 输出原样记台账",
          "建分支并检出后断言 git -C aria rev-parse HEAD 等于 aria origin/master 实测值, 且 git -C aria status --porcelain 退出 0 且输出为空",
          "基线复核 (aria / 主仓 / standards 三组同口径; post_planning R4 R4-M1): 先定两端点 —— aria 组 = 301641b 与 <aria 起点> (分支起点条在 git -C aria fetch origin 之后记下的值); 主仓组 = a563192 与 <主仓起点>; standards 组先跑 git -C standards fetch origin (本任务别处没有显式 fetch standards 的步骤; 主仓 git fetch 在默认的 on-demand 递归下会顺带拉取 gitlink 有变且已检出的子模块, 但关掉递归、子模块未检出或递归拉取失败时就不会 —— 取决于本机配置与子模块状态, 不作前提, 2026-09-21 临时仓三态实测), 端点 = 21748d4 与 B.1 当时的 standards gitlink —— git ls-tree HEAD standards 的输出是整行 160000 commit <sha><TAB>standards, gitlink 取第三字段 (git ls-tree HEAD standards | awk '{print $3}'), 整行照抄进 diff 会得到下述同一种假绿。每组跑 diff 之前对两个端点各跑 git cat-file -e <端点>^{commit} (aria 组与 standards 组分别带 -C aria / -C standards, 主仓组在主仓根), 任一退出非 0 ⇒ 停下上报, 不得当作零 diff。每个文件另先确认它至少在两个端点之一存在: git cat-file -e <端点>:<文件> (同组的 -C), 两端都退出非 0 ⇒ 路径写错或不是单个路径, 停下上报 —— 对两端都不存在的路径, git diff 同样退出 0 且输出为空, 与真零 diff 同形, 退出码判据拦不住 (v2.5, post_planning R5 11c3a29f; aria_shifted 原第 6 条冒号前是三个文件名连写, 已拆成三条)。然后对 metadata.baseline_rebase.aria_zero_diff 的每个文件与 aria_shifted 各条冒号前的文件跑 git -C aria diff --shortstat 301641b <aria 起点> -- <文件>, 对 main_repo 的文件跑 git diff --shortstat a563192 <主仓起点> -- <文件>, 对 metadata.baseline_rebase.standards_files 各条冒号前的文件跑 git -C standards diff --shortstat 21748d4 <gitlink> -- <文件>; 零 diff 的判据 = 退出码为 0 且输出为空, 退出非 0 一律停下上报 —— 端点对象不在本地 (或 SHA 抄错、整行误喂、子模块未检出时 git -C standards 落到主仓上) 时 git diff 的 stdout 同样是空串、退出 128, 只看输出为空会把「没比成」读成「零 diff」; standards 组要抓的正是并发轨推进 standards 并 bump 主仓 gitlink 的那一次, 对象此时若不在本地, 旧判据恰在该红时判过 (2026-09-21 临时仓实测: 两态 stdout 都是空串, 只有退出码分得开)。aria 组与主仓组的端点按构造已在本地 (起点刚 fetch, 旧端点是它的祖先; 2026-09-21 实测 cat-file 与 merge-base --is-ancestor 均退出 0), 同口径在正常路径上不会误停, 另拦 SHA 抄错一类同形失败。与 A.2 记录比对, 新出现 diff 的文件逐处实读被引位置并在台账写偏移表 (aria 与主仓侧 = proposal 所引行号; standards 侧 = standards_files 各条冒号后点名的节与用途); standards 组必须对 B.1 当时的 gitlink 重测, 不得沿用 metadata.baseline_rebase.standards 记下的 940cb5b 数值 —— 它是并发轨随时会动的共享子模块; aria 若有新发布, tasks.md 读前必看第 3 条的取号前提同步更新",
          "台账骨架: 二级标题固定为 基线 / 语料冻结 / fixture 矩阵 / RED / 组 2 收口 / 文档机检 / 反事实 / 回归 / 活体运行 / AB / 发布 / 写法自检 / 外向动作与授权 / 停下与上报; 此后只在对应标题下追加",
      ]),
    T("TASK-002", "1.2", "语料冻结 corpus-freeze.md: 六族样本、双列标注与机械仲裁", "L", "5-7", ["TASK-001"],
      [f"{SPEC}/corpus-freeze.md"], "qa-engineer", "标注者须与实现者不同 (proposal 内联 Tasks B.0); 由非实现席完成",
      [
          "取样: 记主仓提交 F 与 UTC 时刻; 文件集 = git ls-tree --name-only F -- .aria/audit-reports/ 中的顶层 .md (由命令重生成, 不手抄); 同时记 C = F 上 openspec/changes/* 与 openspec/archive/* (去 YYYY-MM-DD- 前缀) 的目录名集合及大小 (A.2 时在 a563192 上为 154, 口径 = 两处目录名去日期前缀后的集合, 含本 spec 自身)",
          "六族 (proposal SC-2): F-a 末段族 / F-b role 后缀族 / F-c aggregated 族 / F-d 无 -R<n>- 族 / F-e 真 2-field legacy / F-f unattributed; 同一 id 须同时有 F-a 与 F-b, 下界 F-a ≥ 2 且 F-b ≥ 3, 候选 state-scanner-inter-cycle-surfacing (以冻结时实测为准); 其余四族各 ≥ 3",
          "第一列算法 (proposal :416-419): 来源定序 change_id > spec_id > context, 取第一个存在且非空的字段; 归一化 = strip 并去首尾反引号或引号, 匹配 ^openspec/changes/([^/\\s]+) 或 ^openspec/archive/(?:\\d{4}-\\d{2}-\\d{2}-)?([^/\\s]+) 取捕获组, 否则取第一个空白分隔 token; 空串即取不到。第一列只读 frontmatter, 不读文件名",
          "仲裁 (proposal :414-426): F-a~F-d 两列不一致或第一列取不到 ⇒ 当场剔出样本池, 进争议表并逐份记两列取值与理由; F-e / F-f 不做双列, 独立源归一化值属于 C 的 F-f 候选改归 F-a~F-d 按上句处理, F-e 按文件名形态照留并记名; 剔除后不足下界 ⇒ 换 id 重采, 换不到则按实测上限记名降下界; 不得把争议条目放回, 不得用 --change-id 自造样本",
          "标注列就是 SC-2 / SC-4 的期望值来源: TASK-004 以字面量写进测试, 测试里不调用被测谓词求期望值",
          "可复现: 由未参与标注的另一实例 (台账记两个实例的标识) 从 F 重跑取样与第一列算法, 文件集与第一列取值逐字相同, 输出记台账; 同一实例复算不算",
      ]),
    T("TASK-003", "1.3", "fixture 前提矩阵与测试风格约束", "S", "2-3", ["TASK-001"], [LEDGER], "qa-engineer",
      "把四条硬约束与裁定派生的期望值先落成表, 防实现者按自己的实现重算期望",
      [
          "矩阵每个 SC 格一行, 列 = audit.mode 取值 / 锚点 Level 行 / audit.enabled / 两个路径参数 / 作用域来源 / carve-out / 期望值出处; 规则取自 proposal §1.0 末段四条硬约束与 :140-149 对照表",
          "mode 取值: SC 正文逐字给出 mode 的格按正文 (SC-9(2) 第二跑与 SC-15(8)(9) 为 adaptive, SC-15(5)(7) 为 convergence —— §1.0 :122 的例外清单漏列这几格, tasks.md 读前必看第 9 条), 其余按硬约束 (1) 钉 manual; carve-out 三格 SC-15(1) / SC-15(4) / SC-21(2) 照 :130-136",
          "子格约定: 每个 SC 的每一格包在 self.subTest(cell='<SC>.<子格>') 里, 断言 (含脚本存在断言) 一律写在 subTest 内; metadata.stage_cells.cells 所列格名逐字照用并进矩阵",
          "正文没给 checkpoint 配置、而断言需要纳入集非空的格 (如 SC-22(1) 的 other 那对判 missing), 矩阵钉最小配置 checkpoints: {post_spec: convergence} 并注明期望值不变 (tasks.md 读前必看第 23 条); 发现某格期望值确须变化 ⇒ 停下记台账并上报, 走 spec 修订, 不当场改断言",
          "tasks.md 读前必看第 6、7、8 条的期望值 (SC-15(5) 三个 checkpoint / SC-17(5) 改写全文见 TASK-006 / SC-18 只留排除分支 / SC-9(4) 钉 checkpoints: {post_spec: 'convergence'} 且 checked_checkpoints 期望 ['post_spec']) 逐字进矩阵",
          "测试风格: 新文件只含 unittest.TestCase 子类, 用例名沿用 SC 核验列 (test_completeness_gate.CompletenessGateTests.test_*); 不 import pytest, 不建 conftest.py —— run_all_tests.sh:41-46 按整个 tests/ 目录判 pytest 套件, 无 pytest 时整套 SKIP",
      ]),
    T("TASK-004", "1.4", "RED 第一批: 新建 tests/test_completeness_gate.py, 写 SC-1~SC-6", "L", "6-8", ["TASK-002", "TASK-003"],
      [f"{AE}/tests/test_completeness_gate.py"], "qa-engineer", "hermetic git 夹具与反事实设计; 测试与实现分由不同 agent 执笔",
      [
          "用例名与 proposal SC-1~SC-6 核验列一致: test_issue_case1_other_change_reports_do_not_count / test_real_corpus_shapes_token_bounded_match / test_bounded_containment_excludes_all_three_shapes / test_legacy_vs_unattributed_counts_split / test_phase_a_only_not_applicable / test_md_and_docs_diff_still_missing / test_empty_diff_is_missing / test_post_planning_a2_artifact_includes_inline_tasks",
          "夹具: tmp 仓一律 git init -b master; config 按 TASK-003 矩阵; 每次调用显式传 --repo-path 与 --diff-repo-path; 脚本经 subprocess 以 sys.executable -B 调用, stdout 用 json.loads 解析, 人读行只从 stderr 断言",
          "helper 内先 self.assertTrue(脚本路径.is_file()); helper 只在 subTest 内调用, 脚本缺失时每个格以 AssertionError 失败",
          "SC-2 期望值取 corpus-freeze.md 标注列的字面量; F-e / F-f 只断言三桶两两不交 (proposal SC-2 (ii))",
          "SC-4 的 WARN 行按 §1.2 模板与连接符「逗号加一个空格」逐字拼出期望串, 整行相等比对",
          "SC-6 只写 hermetic 四格 (1)-(4); tasks.md 重写 c 的快照格不进单测 (快照 295KB, 不随插件分发), 由 TASK-022 活体执行",
      ], notes="TASK-004 / 005 / 006 串行编写同一文件"),
    T("TASK-005", "1.5", "RED 第二批: SC-7~SC-10 与 SC-18 (排除分支)", "L", "6-8", ["TASK-003", "TASK-004"],
      [f"{AE}/tests/test_completeness_gate.py"], "qa-engineer", "同上",
      [
          "用例名: test_scope_resolution_matrix / test_rename_and_anchor_semantics / test_allow_dangling_inherited / test_step3_enumeration / test_bypass_semantics / test_stdout_contract / test_post_brainstorm_exclusion_decision",
          "SC-7 的 --no-spec 合法格先断言 len(results) >= 1 与 checked_checkpoints == ['post_spec'], 再断言 not_applicable 与 change_id is None (防空集上的全称谓词)",
          "SC-9(2) 两跑与短路断言照 proposal 原文; SC-9(4) 另断言 stderr 含 [WARN] bypassed: spec_level_undetermined (tasks.md 读前必看第 8 条, 只增), 并按同条钉 checkpoints: {post_spec: 'convergence'} 后逐字断言 checked_checkpoints == ['post_spec'] (explicit-only 收窄的可证伪落点, 见 TASK-011)",
          "SC-10: 四种 verdict 下 stdout 可 json.loads 且顶层键集逐字等于 §1.4 的 16 项; --base / --repo-path / --diff-repo-path 各自缺失 ⇒ exit 2; --change-id 与 --no-spec 同传 ⇒ exit 2 且 stderr 逐字含互斥文案; 坏 JSON ⇒ config_unreadable exit 2; 报告目录存在时 scan_status == 'ok'",
          "SC-18 只写排除分支 (裁定 1): config 含 post_brainstorm: convergence ⇒ checked_checkpoints 不含它; 不写不采纳分支",
      ]),
    T("TASK-006", "1.6", "RED 第三批: SC-15~SC-17 与 SC-19~SC-22", "L", "6-8", ["TASK-003", "TASK-005"],
      [f"{AE}/tests/test_completeness_gate.py"], "qa-engineer", "同上",
      [
          "用例名: test_empty_checkpoint_set_three_buckets / test_legacy_config_mapping_inlined / test_dangling_skip_bucket_e / test_multi_change_axis_reduction / test_mid_implementation_excluded / test_split_repo_and_diff_paths / test_cross_repo_no_spec_and_anchor_scope / test_cross_repo_missing_diff_repo_path_is_argparse_error / test_enumeration_boundaries / test_step3_priority_chain / test_pairwise_not_cross_product / test_inlined_defaults_equal_upstream / test_inlined_legacy_mapping_equal_upstream / test_env_boundaries",
          "SC-15(5) 按 tasks.md 读前必看第 6 条: checked_checkpoints == ['post_implementation', 'post_planning', 'post_spec'], len(results) == 3, 三对 missing, verdict fail, exit 1; fixture 的内联 ## Tasks 与零 diff 照原文",
          SC17_5,
          "SC-21 在测试期读插件树的 config-loader/DEFAULTS.json 与 config-loader/SKILL.md §旧配置兼容层, 用 importlib 按文件路径载入脚本取常量比对",
          "SC-22(1) 的 WARN 断言逐字含「作用域解析 (S2/S3, 锚点面) 与 not_applicable (b) 通道的路径集判据 (diff 面) 会被弱化」; (iii) 跨仓格断言文案点名 anchor-base",
      ]),
    T("TASK-007", "1.7", "RED 台账与提交", "S", "1-2", ["TASK-004", "TASK-005", "TASK-006"], [LEDGER], "qa-engineer", "机械核验",
      [
          "cd aria/skills/audit-engine/tests && python3 -B -m unittest test_completeness_gate -v: 全部用例失败且失败形态为 AssertionError; 出现 ImportError 或夹具建仓异常 ⇒ 先修夹具再记; 原样输出记台账",
          "在同目录跑 metadata.stage_cells.code, 参数 = stage_cells.cells 的全部格: 退出 1, 且输出里每个格都是 [\"fail\"] (出现 not-run 说明格名没按约定写进测试, 先修测试)",
          "同目录既有测试 python3 -B -m unittest test_sibling_spec_probe 仍 OK (A.2 实测整个目录 Ran 104 OK)",
          "在 aria 根执行 bash skills/run_all_tests.sh --list, audit-engine 行含 (unittest)",
          "grep -nE '^(import|from)[[:space:]]+pytest' aria/skills/audit-engine/tests/test_completeness_gate.py 的退出码恰为 1 (0 = 命中 import pytest; 2 = 文件缺失, 不能按「无输出」放行; A.2 在 scratch 三态实跑: unittest 文件 1 / 含 import pytest 0 / 缺文件 2), 且 aria/skills/audit-engine/tests/conftest.py 不存在",
          "主控只 add 测试文件 (aria feature 分支) 与 corpus-freeze.md (主仓 feature 分支) 并分别提交, SHA 记台账",
      ]),
    # ---------------- 组 2 ----------------
    T("TASK-008", "2.1", "CLI 与 P0 / P1: 参数契约、config 直读与内联映射、格 A、同仓判定、输出通道与短路框架", "M", "4-6", ["TASK-007"],
      [f"{AE}/scripts/completeness_gate.py"], "backend-architect", "stdlib CLI 与契约设计",
      [
          "argparse: --repo-path / --diff-repo-path / --base 为 required=True; --anchor-base 缺省取 --base; --change-id 可重复; --change-id 与 --no-spec 互斥, 文案逐字为「--change-id 与 --no-spec 互斥 —— 前者声明本 cycle 有 spec, 后者声明没有」",
          "config: 直读 <repo-path>/.aria/config.json; 文件缺失 ⇒ 全套内联缺省; 坏 JSON ⇒ config_unreadable exit 2; 内联常量 = DEFAULTS.json 的 audit 子集 (enabled / mode / adaptive_rules / 八个 checkpoint) 与旧配置兼容映射 (触发 = experiments.agent_team_audit 为 true 且无 audit 块); 两个 allow_* 缺省 false",
          "P1: audit.enabled 不为 true ⇒ audit_not_enabled exit 2, 早于任何 git 调用",
          "同仓判定: 在 P1 之后求值; 两面各自 git -C <路径> rev-parse --show-toplevel 的输出逐字相等; 任一失败 ⇒ git_failed exit 2",
          "stdout 恰一个 JSON (schema_version \"1\", gate \"completeness_gate\", 16 键); 全部 [OK] / [INFO] / [WARN] / ERROR 行走 stderr; exit 映射 fail=1, pass 与 bypassed=0, error=2; 在 P6 之前终止的运行按 tasks.md 读前必看第 8 条填非判定键",
          "stdlib only: metadata.new_checks 的 n3 对脚本为真",
          "验收: 在 aria/skills/audit-engine/tests 下跑 metadata.stage_cells.code, 参数 = TASK-008 所列格, 退出 0; 其余格失败属预期",
      ]),
    T("TASK-009", "2.2", "P2a 与 P2: --no-spec 前置核验、S1–S4、两个 base 轴的陈旧告警", "L", "5-7", ["TASK-008"],
      [f"{AE}/scripts/completeness_gate.py"], "backend-architect", "git 子进程与作用域解析",
      [
          "P2a 只在给出 --no-spec 时执行, 求值面 = --repo-path 与 --anchor-base: 锚点面 diff 为 0 行 ⇒ no_spec_unverifiable; 触 openspec/changes/** ⇒ no_spec_contradicted; 两者都在 P2 之前",
          "S1: 锚点 = openspec/changes/<id>/proposal.md, 或 openspec/archive/ 下去掉 ^\\d{4}-\\d{2}-\\d{2}- 前缀后逐字等于 <id> 的目录里的 proposal.md (不用 glob); 无锚 ⇒ change_id_unanchored exit 2; allow_dangling_change_ids 为 true 时降为 [WARN] dangling change_id: <id> 并按零报告继续",
          "S2: git -C <repo-path> diff --name-only --no-renames $(git -C <repo-path> merge-base HEAD <anchor-base>) 取 openspec/changes/<id>/ 前缀去重, scope_source=diff; S3: 通过 P2a 后 scope_source=no_spec, change_ids=[], Level 视为 1; S4: change_scope_unresolved exit 2, 三个 fix 文案照 §1.1 (第二个为「在锚点仓 (主仓) 的分支里带上 openspec/changes/<id>/ 变更」)",
          "ref 解析与陈旧比对在同仓判定之后、P2a 之前无条件执行。陈旧告警: --base 与 --anchor-base 各比一次 (不含 / 且同名远程跟踪 ref 存在且 SHA 不同), 文案逐字照 proposal §1 的 --base 条款并点名是哪根轴; 同仓且 --anchor-base 缺省时只出一条; ref 或 merge-base 解析失败 ⇒ git_failed exit 2",
          "验收: stage_cells 命令, 参数 = TASK-008 与 TASK-009 所列格, 退出 0",
      ]),
    T("TASK-010", "2.3", "P3 与 P4: Level 三条判据、五档优先级链、五项排除、逐对纳入、dangling-skip", "L", "5-7", ["TASK-009"],
      [f"{AE}/scripts/completeness_gate.py"], "backend-architect", "配置语义与解析规则",
      [
          "Level: 全文件扫描取文档序第一条命中行; 行首去掉 > - # 空白 * 后以 Level 或 Spec Level 开头, 可选 **, 再接半角或全角冒号; 取值前剥 ~~…~~ 片段; 取冒号后第一个 1 / 2 / 3; 解析不到 ⇒ spec_level_undetermined exit 2; --no-spec ⇒ 1",
          "优先级链 (§1.3 表): 级 1 = 原始 config 的 audit.checkpoints 自身含该键; 2a adaptive ⇒ adaptive_rules.level_<N>; 2b convergence; 2c challenge; 2d manual ⇒ off; mode 键存在但不属四值 ⇒ config_unreadable exit 2; enabled_by 为六值封闭集",
          "排除五项: pre_merge / post_closure / mid_post_spec / mid_implementation / post_brainstorm (裁定 1)",
          "Level 按需: 只在某对落到级 2a 时才对该 change 求 Level",
          "dangling-skip: allow_dangling_change_ids 为 true 且锚点缺失或 Level 不可解析 ⇒ 该 id 的非 explicit 对取 resolved_mode off 与 enabled_by dangling-skip, 并记 [WARN] dangling change_id: <id> — Level 不可解析, 跳过 adaptive 推导",
          "checked_checkpoints = 各 change 纳入集的并集并 sorted(); results 只含真正纳入的对 (不叉乘)",
          "验收: stage_cells 命令, 参数 = TASK-008~010 所列格, 退出 0",
      ]),
    T("TASK-011", "2.4", "P5 与早退型豁免: 格 B / C / D / E、归约 R-1 / R-2、S4 / spec_level_undetermined / no_spec_unverifiable 的豁免与短路", "M", "4-6", ["TASK-010"],
      [f"{AE}/scripts/completeness_gate.py"], "backend-architect", "判定表实现",
      [
          "P5 只在纳入集为空且未短路时求值: 格 B (归约后 resolved(pre_merge) 非 off) ⇒ pass 与 no_prior_checkpoints; 格 C (off 且各 change 的 enabled_by 全属 explicit / manual-default) ⇒ pre_merge_not_enabled exit 2; 格 D (存在 adaptive:level_N) ⇒ pass, 逐 change 一行 [INFO]; 格 E (存在 dangling-skip 且无 adaptive) ⇒ pass 与双留痕; 各格文案逐字照 §1.4 表, 归约照 R-1 / R-2",
          "allow_incomplete_checkpoints 为 true: S4 / spec_level_undetermined / no_spec_unverifiable 降为 bypassed exit 0 并短路 (missing 的降级在 TASK-012); no_spec_contradicted 与 change_id_unanchored 不降 (裁定 11)",
          "统一 WARN 行 [WARN] incomplete checkpoint gate bypassed: missing=<cp>@<id>,... ; scope_unresolved=<0|1> (本任务的三类早退 missing= 后为空), S4 与 no_spec_unverifiable 取 1; no_spec_unverifiable 与 spec_level_undetermined 另各加一行 [WARN] bypassed: <error_kind>",
          "explicit-only 收窄 (读前必看第 8 条, v2.2 扩面): S4 / no_spec_unverifiable / spec_level_undetermined 三类早退被豁免时, checked_checkpoints 一律只收原始 config 的 audit.checkpoints 里显式写出、值非 off 且不属五项排除的键并 sorted(), 不取「已产出值」—— 「已产出值」由实现装配该字段的时机决定 (边算边收 vs P4 末尾统一收), 两个字面合规的实现会给不同值; 其余非判定键照 tasks.md 读前必看第 8 条",
          "上一条的可证伪落点 (格 SC-9.4-level-undetermined-bypassed): SC-9(4) 的 fixture 按读前必看第 8 条钉 checkpoints: {post_spec: 'convergence'} (mode 仍按第 9 条为 adaptive, 期望的 verdict bypassed / exit 0 / WARN 两行不变), 断言 checked_checkpoints == ['post_spec'] 逐字相等。反事实: 在 P4 末尾才统一装配该字段的实现在此格给 [] ⇒ 本断言红; 不钉 checkpoints 或不写本断言 ⇒ 两种实现都不红 (这正是 post_planning R2 PP2-M5 指出的缺陷)",
          "验收: stage_cells 命令, 参数 = TASK-008~011 所列格, 退出 0",
      ]),
    T("TASK-012", "2.5", "P6: 归属规则、非递归枚举、两个排除计数、三态与 trail 行", "L", "6-8", ["TASK-011"],
      [f"{AE}/scripts/completeness_gate.py"], "backend-architect", "核心匹配逻辑",
      [
          "规则 1: 文件名以 <checkpoint>- 开头且以 .md 结尾; 规则 2: 含 -<id>- 或去 .md 后以 -<id> 结尾, 逐字且大小写敏感; 规则 3: 有界包含排除按前缀 / 后缀 / 中缀三型对称实现, C = openspec/changes/* 并上去日期前缀的 openspec/archive/*",
          "枚举: <repo-path>/.aria/audit-reports 用 iterdir() 只取顶层文件; 目录不存在 ⇒ 按零报告, scan_status dir_missing, stderr 记 [WARN] completeness gate: .aria/audit-reports/ 不存在, 按零报告评估",
          "计数: excluded_legacy_count 只收匹配 ^<cp>-[0-9TZ:.\\-]+\\.md$ 且不含 C 中任何 id 的文件; unattributed 收以纳入 checkpoint 前缀开头、对 C 中任何 id 规则 2 都不命中且不属 legacy 的文件; 统计面 = 纳入 checkpoint 的并集; 三个 list 一律 sorted()",
          "三态 first-match: present / not_applicable ((a) scope_source=no_spec; (b) post_implementation 且同仓且 diff 非空且全部路径在 openspec/changes/<作用域 id>/** 或 .aria/audit-reports/** 下; (c) post_planning 且无 tasks.md、无 detailed-tasks.yaml、proposal 无 ^#{2,}\\s*Tasks 小节, 归档态同理) / missing (含 diff 为空)",
          "trail 行 (stderr): missing 的 ERROR 与四项 Fix; unattributed 的 WARN 全局一行、前 20 个文件名、连接符为逗号加一个空格; not_applicable 的 [INFO] (S3 渲染为 (无 change_id)); present 的 [OK] 逐行",
          "S3 态 results 每条的 change_id 为 None (JSON null, 不是占位串), 与 stderr 的 (无 change_id) 渲染分别核验",
          "missing 的豁免: allow_incomplete_checkpoints 为 true 且有 missing ⇒ 仍逐对评估并全部留痕, 走完 P6 后 verdict 降为 bypassed exit 0, results 照常输出, 统一 WARN 行的 missing= 列出全部 <cp>@<id>, scope_unresolved=0",
          "验收: python3 -B -m unittest test_completeness_gate 全绿 (SC 方法级); stage_cells 命令对全部所列格退出 0",
      ]),
    T("TASK-013", "2.6", "组 2 收口: 全绿后提交并记 SHA", "S", "1-2", ["TASK-012"], [LEDGER], "qa-engineer", "收口核验; 提交由主控执行",
      [
          "cd aria/skills/audit-engine/tests && python3 -B -m unittest discover -s . -p 'test_*.py' 零失败, Ran 数 = 104 + 新文件用例数",
          "metadata.new_checks 的 n3 对 aria/skills/audit-engine/scripts/completeness_gate.py 为真",
          "主控在 aria feature 分支只 add scripts/completeness_gate.py 与 tests/test_completeness_gate.py 并提交; 提交后不带路径的 git -C aria status --porcelain 退出 0 且输出为空; SHA 记台账 (组 4 的副本从它检出)",
      ]),
    # ---------------- 组 3 ----------------
    T("TASK-014", "3.1", "execution-modes.md: 入口守卫、Step 1–5、三态模板、豁免文案", "M", "4-6", ["TASK-013"],
      [f"{AE}/references/execution-modes.md"], "knowledge-manager", "运行时处方文档",
      [
          "§入口逻辑: :9 保留; :10 改为按 :15 的优先级链判是否启用, adaptive 档取上界 (任一档非 off 即照常进入), 逐字含「checkpoints 显式值 > adaptive_rules 推导值」与「入口层不解析」",
          "Step 2: :43 改为 tasks.md 读前必看第 7 条的逐字句; :44 的 WARN 与 :82 统一为 §1.1 的同一句",
          "Step 3: 在 mid_post_spec 条款之后追加 - key != \"mid_implementation\"(…) 与 - key != \"post_brainstorm\"(…) 两行, 与既有条款同构; 枚举源改为过优先级链 (与 :15 同句)",
          "Step 4-5: 删除两个通配行; 改为经 scripts/completeness_gate.py 的调用串 (逐行照抄 metadata.canonical_call, 行首缩进随所在围栏; N4 逐行去首尾空白后比较; 该区间内脚本路径只出现在调用行) + §1.2 规则 + §1.3 三态 + §1.4 契约; Step 5 路由段逐字写入消费方 fail-closed 义务 (含「stdout 非 JSON」与「不得按 PASS」)",
          "保留: Step 1: 到 Step 5: 五个行首标记原样保留 (N1 / N2 按标记切片), :34 开 / :66 闭的围栏不拆不增",
          "校验失败输出改三态模板, missing 的 Fix 四项 (第二项逐字附 adaptive 推导的理由)",
          "互补说明 (:25-30) 补一句「完整性门自本 spec 起带 change 维度」(新写文字不用裸 issue 编号, 以小节名指代); Step 1 补脚本侧等价实现注",
          "机检由 TASK-018 统一跑",
      ]),
    T("TASK-015", "3.2", "audit-engine SKILL.md: 输入参数五项、fenced bash 调用块、两个 allow_* 注释、:423、相关文档", "S", "2-3", ["TASK-014"],
      [f"{AE}/SKILL.md"], "knowledge-manager", "Skill 入口文档",
      [
          "## 输入参数 表补 change_id / repo_path / diff_repo_path / base / anchor_base 五行, 必填列照 proposal §2 表 (repo_path 与 diff_repo_path 为「必传」)",
          "## 执行流程 第 (2) 阶段描述改为经 completeness_gate.py 机械执行; 在 sibling_spec_probe 调用块之后新增 ```bash 围栏块, 块内顶格照抄 metadata.canonical_call (N4)",
          ":423 (emergency hotfix lane) 的条件改为「仅 `audit.enabled=true` 且 pre_merge 按 C.2 pre_hook 步骤 3 的优先级链判为启用时」, 与 TASK-016 的 :754 同一短语 (N8)",
          ":381-384 与 :385-388 两个注释块各补一句: allow_dangling_change_ids —— completeness gate 的 S1 锚点校验继承本键; allow_incomplete_checkpoints —— 豁免 missing / scope_unresolved / spec_level_undetermined / no_spec_unverifiable, 不豁免 no_spec_contradicted 与 change_id_unanchored",
          ":427-433 相关文档加 completeness gate 契约指针 (块外提及不计数)",
          "frontmatter (含 description) 零改动: 以 awk 'NR==1&&$0==\"---\"{f=1;next} f&&$0==\"---\"{exit} f' 切出首个 --- 与下一个 --- 之间的块, 对 git -C aria show <aria 起点>:skills/audit-engine/SKILL.md 与工作树文件各切一次, 两条命令都退出 0 且两侧切出的块都非空、各含一行以 description: 开头 (git show 失败、路径写错或 CRLF 文件未去 CR 时切出的都是空串, 两侧同空则 sha256 恒相等; v2.5, post_planning R5 同族扫描), sha256 相等 (A.2 在 scratch 三态实跑: 1cb3872 对当前文件相等, 改 description 后不等)",
      ]),
    T("TASK-016", "3.3", "phase-c-integrator SKILL.md (CRLF): 步骤 3 五档链与同形两处、pre_hook 五参数、4.5、:157", "M", "3-4", ["TASK-015"],
      [f"{PC}/SKILL.md"], "knowledge-manager", "调用方处方文档",
      [
          "步骤 3 (:132) 改为 proposal §3 的逐档写法: 级 1 显式值非 off 即调用门; 2a adaptive 取上界; mode == \"convergence\" 与 mode == \"challenge\" 视为启用、照常调用门; manual 视为 off 早退; 其余 mode 照常调用门、由门判 config_unreadable; 逐字含「checkpoints 显式值 > adaptive_rules 推导值」「mode == \"convergence\"」「mode == \"challenge\"」「照常调用门」",
          ":57 的触发条件摘要与 :754 的 hotfix 降级条件改为「pre_merge 按 C.2 pre_hook 步骤 3 的优先级链判为启用时」, 两处不再单独写 audit.checkpoints.pre_merge != \"off\" (tasks.md 读前必看第 19 条); 该短语只用于这两处与 audit-engine/SKILL.md:423 (N8 按锚点行判定); :42 配置表的缺省值行不动",
          "pre_hook 步骤 4 追加 change_id / repo_path / diff_repo_path / base / anchor_base (两个路径参数必传、base 为远程跟踪 ref), 文字照 proposal §3; 步骤 5 前插「4.5 completeness gate 三态处置」, 逐字含「not_applicable → workflow report 必带」与「unattributed_count > 0」",
          ":157 的 pre_merge-{timestamp}.md 改为 report-storage.md 的 5-field 形态; 步骤 2 (:131) 不动",
          "CRLF: 编辑前 git -C aria ls-files --eol -- skills/phase-c-integrator/SKILL.md 为 i/crlf w/crlf; 用保留行尾的方式编辑; 编辑后、暂存前 metadata.crlf_guard 为真; frontmatter 去 CR 后与 aria 起点逐字相同 (metadata.crlf_guard.frontmatter_rule)",
      ]),
    T("TASK-017", "3.4", "旧 schema 散文残留三处、report-storage 四句、pre-write-validation 关联行", "S", "1-2", ["TASK-016"],
      ["aria/skills/phase-a-planner/SKILL.md", "aria/skills/phase-b-developer/SKILL.md",
       f"{AE}/references/report-storage.md", f"{AE}/references/pre-write-validation.md"],
      "knowledge-manager", "文档勘正",
      [
          "phase-a-planner/SKILL.md:267 与 phase-b-developer/SKILL.md:204、:277 的 {timestamp} 形态改为 report-storage.md:8 的 5-field 形态; report-storage.md:37,43 与 report-format.md:5 的向后兼容描述不动",
          "report-storage.md §向后兼容追加 proposal §4 表所列四句; 第 (3) 句逐字含「子目录内的报告不计入完整性证据」, 第 (4) 句逐字含「三个桶都不收」",
          "CRLF: phase-b-developer/SKILL.md 按 TASK-016 的 CRLF 条款处理 (编辑前 i/crlf w/crlf, 编辑后暂存前 crlf_guard 为真, frontmatter 去 CR 后不变); phase-a-planner/SKILL.md 是 LF (2026-09-19 实测 i/lf w/lf), 不需去 CR",
          "frontmatter (含 description) 零改动 —— 本任务改的两份 SKILL.md 各做一次, 做法同 TASK-015: 以 awk 'NR==1&&$0==\"---\"{f=1;next} f&&$0==\"---\"{exit} f' 切出首个 --- 与下一个 --- 之间的块, 对 git -C aria show <aria 起点>:skills/<name>/SKILL.md 与工作树文件各切一次, 两侧切出的块须非空且含 description: 行 (同 TASK-015, v2.5), sha256 相等; phase-a-planner 直接切 (LF), phase-b-developer 先 tr -d '\\r' 再切。这两份与 TASK-015 / TASK-016 的两份合起来即本 cycle 被改 SKILL.md 的全集, 是 metadata.rule6_note.description_changed 取 no 的机械证据面 (TASK-018 复核)",

          "pre-write-validation.md:3 关联行补「完整性门自本 spec 起带 change 维度」的等义句 (新写文字不用裸 #n)",
      ]),
    T("TASK-018", "3.5", "文档机检 (SC-13 + N1 / N2) 与组 3 提交", "S", "1-2",
      ["TASK-017"], [LEDGER], "qa-engineer", "机械核验",
      [
          "SC-13 逐条 (proposal :469) 在组 3 改动后全真 (计数一律在主仓根以全路径跑, grep -c 的退出码须为 0 或 1 —— 退出 2 是文件不存在或路径写错, 此时 stdout 为空, 不得读作 0; 下面两条「为 0」的 grep -c 判据 (通配模式、旧句) 要求退出 1 且输出 0; timestamp 残留那条是 grep -rn, 判据见本任务第 3 条; v2.5, post_planning R5 同族扫描); A.2 在 1cb3872 的基线值见 metadata.sc13_baseline (全部为红态), 组 3 后应为: 通配模式计数 0 (基线 2); timestamp 残留 0 (基线 4); report-storage 三条逐字计数 ≥1 / =1 / =1 (基线 0); phase-c-integrator 的 change_id 计数较基线 3 至少 +1; execution-modes 的 adaptive_rules 计数较基线 3 至少 +1; 两处 bypassed 文案逐字相同 (基线两种拼法); audit-engine/SKILL.md 的 ```bash 块切片内 scripts/completeness_gate.py 恰 1、execution-modes.md 的 Step 4: 至 Step 5: 行区间内恰 1, 两段调用串由 N4 比较; 调用方接缝与 R5 五条 grep 全真 (基线全 0; 旧句「跳过校验, 继续执行 pre_merge 审计」基线 1 → 0)",
          "metadata.new_checks: n1 与 n2 对 execution-modes.md 为真, n3 对 completeness_gate.py 为真, n4 (canonical = metadata.canonical_call 按行切分) 与 n8 为真 (三态见 metadata.a2_state_runs 与 metadata.v2_state_runs); metadata.crlf_guard 对两个 CRLF 文件为真 (暂存前跑); audit-engine / phase-c-integrator / phase-b-developer / phase-a-planner 四份 SKILL.md 的 frontmatter 与 aria 起点逐字相同 (phase-c-integrator 与 phase-b-developer 是 CRLF, 先去 CR; audit-engine 与 phase-a-planner 是 LF, 直接切; 两侧切出的块须非空且含 description: 行, 同 TASK-015 的 frontmatter 条, v2.5) —— 这四份是本 cycle 被改 SKILL.md 的全集 (TASK-015 audit-engine / TASK-016 phase-c-integrator / TASK-017 phase-a-planner 与 phase-b-developer), 缺一即 metadata.rule6_note.description_changed 取 no 失去证据 (post_planning R3 R3-M3: v2.2 只列三份, 漏掉 TASK-017 交付的 phase-a-planner —— 它带 description frontmatter, 且其 AB 套件不在照跑面上); 这三条与 SC-13 守的是文本落点, 拦不住语义写错, 语义由组 2 单测与组 4 反事实守",
          "在主仓根跑 grep -rn 'audit-reports/[a-z_]*-{timestamp}\\.md' aria/skills/: 零命中 = 退出 1 且无输出 (退出 0 = 有命中; 退出 2 = aria/skills/ 不在当前目录下或不可读, 没查成, 停下 —— 原写「零命中」对后两者读法相同; v2.5, post_planning R5 同族扫描)。该检索递归扫被 git 忽略的文件, skill-creator 工作区因此不得放在 aria/skills/ 下 (见 TASK-024 快照比较条, post_planning R5 R5-M5)",
          "主控只 add TASK-014~017 的七个文件并提交 (提交前完成上两条); 提交后 git -C aria status --porcelain 退出 0 且输出为空; SHA 记台账",
      ]),
    # ---------------- 组 4 ----------------
    T("TASK-019", "4.1", "反事实第一批: SC-1~SC-10 与 SC-18", "L", "5-7", ["TASK-018"], [LEDGER], "qa-engineer",
      "补丁由既非实现者也非测试作者的实例构造",
      [
          COUNTERFACTUAL_METHOD,
          "补丁由 qa-engineer 的新实例构造, 该实例未参与 TASK-004~006 与组 2 (台账记实例标识); 首个失败断言不是 SC 原句所指的那条 ⇒ 原样记台账并上报, 不为凑结果改补丁",
          "SC-1: 归属退回 {checkpoint}-*.md 通配 ⇒ post_implementation@x 判 present",
          "SC-2: 规则 2 退回纯中缀 ⇒ F-a 少计; 按第 4 段取 spec_id ⇒ A1- 与 R5.5 形态少计",
          "SC-3: 有界排除退回 c.startswith(id + '-') 单向写法 ⇒ 后缀与中缀两格判 present",
          "SC-4: 两个计数合并定义 ⇒ excluded_legacy_count 变 4; 不截断、缺尾巴或换连接符 ⇒ WARN 整行比对红",
          "SC-5: proposal SC-5 的八条反事实逐条, 其中 (8) = S3 不做非空短路",
          "SC-6: (c) 退回只看两个文件 ⇒ case (3) 判 not_applicable (该补丁 diff 供 TASK-022 复用)",
          "SC-7: 去掉 --no-renames ⇒ rename 格落 S4; 锚点用裸 glob ⇒ 判有锚; 不继承 allow_dangling_change_ids ⇒ exit 2; Level 失败不走同一降级 ⇒ exit 2; 不实现 not_applicable 通道 ⇒ missing; adaptive Level 1 落格 C ⇒ exit 2",
          "SC-8: 去掉 mid_implementation 排除 ⇒ checked_checkpoints 多出该键; 按 config 键序输出 ⇒ 顺序不等",
          "SC-9: 不短路 ⇒ 第一跑落格 C exit 2; adaptive 跑照常枚举 ⇒ checked_checkpoints 非空; spec_level_undetermined 不降级 ⇒ (4) exit 2",
          "SC-10: --repo-path 取 cwd 缺省或 --diff-repo-path 取 --repo-path 缺省 ⇒ 缺参不 exit 2; 不设互斥 ⇒ 同传不 exit 2; 经「坏 JSON 返默认值」读 config ⇒ 非 config_unreadable",
          "SC-18: 去掉 post_brainstorm 排除 ⇒ checked_checkpoints 含它",
      ]),
    T("TASK-020", "4.2", "反事实第二批: SC-15~SC-17 与 SC-19~SC-22", "L", "5-7", ["TASK-019"], [LEDGER], "qa-engineer", "同上",
      [
          "做法与实例要求同 TASK-019",
          "SC-15: 空集一律 error ⇒ (3) 红; 级 2 只处理 adaptive ⇒ (5) 落格 B; mode 拼错静默 off ⇒ 非 config_unreadable; 不拆格 D ⇒ (6) 落格 C; 保留 enabled_by 全称前置 ⇒ (7) 未落格 B; 格 E 落格 C 或 enabled_by 留空 ⇒ (8) 红; enabled_by 当标量 ⇒ (9) 的 [INFO] 只 1 条; 归约量化到全体 checkpoint ⇒ (9)(ii) 误落格 D; 不内联映射 ⇒ (4) 空集",
          "SC-16: 不排除 mid_implementation ⇒ missing 与 fail",
          "SC-17: 核验面绑 --diff-repo-path ⇒ (4) 判 not_applicable; S2 绑 diff 面 ⇒ (6) 落 S4; --diff-repo-path 有缺省 ⇒ (7) 不 exit 2; 字符串比同仓 ⇒ (2) 误判跨仓; (5) 按 TASK-006 改写后的三条反事实",
          "SC-19: iterdir 换 rglob ⇒ matched_count 2; unattributed 不要求 checkpoint 前缀 ⇒ (b) 计数 1; 去掉规则 1 ⇒ (c) matched_count 1",
          "SC-20: 字面枚举合并视图 ⇒ (1)(2) 缺项或空集; 不剥删除线 ⇒ (4) 取 2; 任何 head-window ⇒ (5) 落 undetermined; 窄正则 ⇒ (6) 三格落 undetermined; 叉乘 ⇒ (7) fail",
          "SC-21: 改脚本常量任一缺省或删映射一条 ⇒ (1)(2) 红",
          "SC-22: 不做陈旧比对 ⇒ 无 WARN; 只比 --base ⇒ (iii) 无 WARN; 不判目录直接 iterdir ⇒ crash; 保留旧 WARN 文案 ⇒ 逐字断言红",
      ]),
    T("TASK-021", "4.3", "回归: SC-12 三套、SC-12 liveness (重写 a)、catalog 5/8 单测", "S", "2-3", ["TASK-018", "TASK-019", "TASK-020"],
      [LEDGER], "qa-engineer", "回归与接线核验",
      [
          "会话不带 ARIA_COORDINATION_NO_PUSH (判法同 TASK-001)",
          "SC-12 三条: cd aria/skills/audit-engine/tests && python3 -B -m unittest discover -s . -p 'test_*.py'; state-scanner/tests 与 phase-c-integrator/tests 同命令; 三者零失败 (A.2 在副本的基线: Ran 104 OK / Ran 1605 OK (skipped=1) / Ran 148 OK); Ran 数变化逐条归因; Ran 数不得少于基线 —— python 3.11 的 unittest discover 找不到任何用例时照样输出 OK 并退出 0 (从错误目录跑即此形态, 2026-09-22 实测), 少了先停下查明; 三条各放子 shell (形如 (cd <目录> && python3 -B -m unittest …)), 跑完当前目录仍是主仓根, 下一条的 guard 不受影响 (v2.5, post_planning R5 同族扫描与 R5-M4)",
          "重写 a: 先在 bash 里跑 metadata.sc12_liveness.guard_config_hooks (命令自带 git -C <主仓根>, 与当前目录无关), 按该键判据: 末行 rc= 为 0 或 1 且其前无输出才继续, rc 为其它值 (没跑成) 或有输出一律停下 (v2.5, post_planning R5 R5-M4: 原写「须无输出」, 而上一条刚 cd 进 aria 子目录, 顺序执行时 guard 只搜 aria 仓、看不到主仓 .aria/config.json, 退出 1 且无输出 —— 真空通过); 再在主仓根 (aria 工作树为 feature 分支 HEAD, 含组 2 与组 3 提交) 执行 metadata.sc12_liveness 的代码并加 --force-checked, 要求 L2 与 L3 为真; L1 在一次性副本 (主仓 feature 分支 clone, aria 为 feature 分支 HEAD 的嵌套 clone 并 git submodule init, 做法同 metadata.a2_state_runs) 里把本目录 tasks.md 全部勾选后跑, 要求为真; 三项输出原样记台账 (A.2 预演见 metadata.a2_state_runs 的 C 态)",
          "catalog 5/8: cd aria/skills/phase-c-integrator/tests 后 python3 -B -m unittest test_pre_merge_gate.GateCheckTests -v 与 test_pre_merge_gate.NotFoundVerdictTests.test_sc2_trigger_matched_message -v 与 test_path_coverage.InternalErrorReasonTests.test_internal_error_has_own_reason -v 全 OK (A.2 实测 GateCheckTests 7 条 OK); catalog 字面 node id test_pre_merge_gate.GateCheckTests.test_case_e_malformed_aether_routes_fail 报 AttributeError 属已知缺口 (真实方法 test_case_e_malformed_aether_main_leg_routes_fail, test_pre_merge_gate.py:266), 记台账",
      ]),
    T("TASK-022", "4.4", "活体运行 (SC-11) 与 SC-6 自证 (重写 c)", "S", "1-2", ["TASK-021"], [LEDGER], "qa-engineer", "活体证据",
      [
          "在主仓根 (aria 为 feature 分支 HEAD, 一分钟内 fetch 过 origin) 跑 proposal SC-11 的命令 (两个路径参数都是主仓根, --base origin/master --anchor-base origin/master, --change-id pre-merge-completeness-gate-change-scope): stderr 不含 [WARN] base ref 陈旧 (传远程跟踪 ref 时该告警结构上不会出现, 这一条只防命令被改回裸 master); post_spec 为 present 且 matched_count ≥ 6; post_planning 为 present (tasks.md 读前必看第 16 条; 实跑为 missing 属新发现: 记台账并上报, 本任务不判失败, 也不改断言); unattributed_count > 0 且 unattributed 非空 (不写死数值)",
          "同命令改 --change-id zz-not-a-change ⇒ change_id_unanchored exit 2",
          "重写 c (i): 在 scratch 建 hermetic 仓 (git init -b master, 一次提交), 写入 git show a563192:openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md 的原样字节并核 sha256 = d3c9b4f2089031bd1adcc95aeba964a3991d99f16c50026b07795119607d6f34, 按重写 c 的配置以 TASK-013 SHA 的脚本跑 ⇒ post_planning 该对恰为 missing; 再在按 TASK-019 记下的 SC-6 补丁重建的副本上跑 ⇒ not_applicable 且 reason no-a2-artifact",
          "重写 c (ii): 对当前目录同命令的 post_planning 行为 present 或 missing, 且 reason 不是 no-a2-artifact",
          "输出原样记台账, 周期 handoff 摘录",
      ]),
    # ---------------- 组 5 ----------------
    T("TASK-023", "5.1", "AB 套件编辑: eval id 3、audit-engine.json 文件版本、version.yaml", "S", "2-3", ["TASK-022"],
      ["aria-plugin-benchmarks/ab-suite/audit-engine.json", "aria-plugin-benchmarks/ab-suite/version.yaml"],
      "qa-engineer", "定向 fixture 设计",
      [
          "eval id 3 (descriptive, 与 id 1 / 2 同结构: id / name / prompt / expected_output / expectations): prompt 给定目录清单 (含他人 change 的同 checkpoint 报告、本 change 的末段形态报告、一份 Phase A-only 的 diff)、config 与 change_id, 要求写出调用命令行、逐对三态结果与 [INFO] / [WARN] / ERROR 措辞; expectations 至少三条: 不得把其它 change 的报告当证据 / 末段形态 …-<id>.md 必须计入 / not_applicable 必须以 [INFO] 行 surface",
          "audit-engine.json 文件内 version 由 1.0.0 改为 1.1.0",
          "version.yaml: git fetch origin 后读 git show origin/master:aria-plugin-benchmarks/ab-suite/version.yaml 的 version 与 changelog 顶条, 新值 = 该值的下一个 MINOR (A.2 时 1.5.0 → 1.6.0), 已被占 ⇒ 顺延; 在飞轨 (如 10CG/Aria#211 的 T4) 未合并前看不到, 以 TASK-030 合并时的冲突或合并后复读为准; changelog 顶部加本 spec 条目; skills_covered = ls aria-plugin-benchmarks/ab-suite/*.json | wc -l (在主仓根跑, 且管道首段 ls 退出 0 —— 看 bash 的 PIPESTATUS: 从别的目录跑时 ls 报错而 wc -l 照样输出 0 并退出 0; v2.5), total_eval_cases = 各 json 的 len(evals) 之和 (A.2 实测 32 / 84, 加 eval 后应为 32 / 85), 由命令重生成",
          "两文件 json / yaml 均可解析; 主仓 PR 合并后再读一次 version.yaml, 核「这个值现在该是什么」",
          "开 AB 会话之前 (本会话不带 ARIA_COORDINATION_NO_PUSH): 按 TASK-025 第一条的做法把 aria origin/master 并入 feature 并重跑 TASK-018 与 TASK-021, 使 TASK-024 开跑时 feature 已含上游",
          "提交信息必须带本轨 trailer: 单起一行 Spec: openspec/changes/pre-merge-completeness-gate-change-scope (10CG/Aria#199), 写法与 TASK-029 同, 提交后当场 git log -1 --format=%B 回读确认。理由: 本任务两个交付物 (ab-suite/audit-engine.json 与 ab-suite/version.yaml) 都在 metadata.commit_attribution 的 shared 集里, 结构上不可能含 exclusive 路径 ⇒ 不带 trailer 时该提交恒判 shared-only, 在 TASK-030 的提交范围核验里停在 owner_gates 第 16 项 —— 一切都做对也会停 (post_planning R3 R3-M2 形态 1)",
          "主控在主仓 feature 分支提交",
      ]),
    T("TASK-024", "5.2", "Rule #6 照跑 (两读法并集): audit-engine 与 phase-c-integrator 两个套件", "L", "5-8", ["TASK-023"],
      ["aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-pre-merge-completeness-gate-rule6/", LEDGER],
      "qa-engineer", "AB 编排与区分力判读",
      [
          "前置 (owner_gates 第 4 项): 开 AB 会话之前的最后一个普通会话 (不带该变量) 结束前补一次核验过的心跳 —— 即 hard_constraints 第 4 条的会话入口 claim 核验 (解析 → 前置检查 → 强制对齐后重跑解析 → 心跳并按 metadata.coord_push_verify 核验), 结果记台账; AB 会话自身推不出心跳, 按本任务第 2 条两次快照之间也不得 fetch, 不做入口核验 (v2.5, post_planning R5 R5-M2)。会话以 ARIA_COORDINATION_NO_PUSH=1 启动; 用与 CLI 同一判据在子进程核: cd aria/skills/state-scanner && python3 -B -c 'import sys; sys.path.insert(0, \".\"); from lib.failure_handlers import no_push_requested_by_env as f; sys.exit(0 if f() else 1)' 退出 0 (取值须为 1 / true / yes, 仅已设置不算); 不满足 ⇒ 停在本步 (会话内补不上)",
          "本会话从第一次快照到第二次快照之间不调 /state-scanner、不执行任何 fetch (否则他人推送的对象会进本地, 使远端比较误判为本机推出)",
          "AB 基线 (第一次快照之前): git -C aria fetch origin; git -C aria merge-base --is-ancestor origin/master <feature 分支 HEAD> 退出 0 (TASK-023 的「开 AB 会话之前」条已并入); 不成立 (其间上游又前进) ⇒ 停下上报, 由 owner 决定是否回到不带该变量的会话再并入; 记 A = aria origin/master SHA、W = feature 分支 HEAD (TASK-027 第 4 步用)",
          "臂: with_skill = W 的工作树 (skills/audit-engine 与 skills/phase-c-integrator); without_skill = git -C aria worktree add <scratch> A 的快照 (old_skill 语义, 先例 aria-plugin-benchmarks/ab-results/2026-09-03-v1.69.0-sibling-spec-probe-rule6)",
          "形态: 两个套件的全部 eval 按 descriptive 下发 (AB_TEST_OPERATIONS.md 规则 1: 未声明即 descriptive); 执行器提示逐字附「只做描述性推演: 不得执行 git fetch / pull 与任何 git 写命令 (commit / merge / push / tag / reset / checkout 等), 不得调用 forgejo 的写接口」; 不改任何 remote 配置",
          "快照 (开跑前与结束后各一次): 主仓与 aria 的 git rev-parse HEAD、不带路径的 git status --porcelain、git branch --list; 主仓与三个子模块各自 git ls-remote origin 与 github 的 refs/heads/master; git -C aria ls-remote --tags origin 与 github; refs/aria/coordination 的本地值与 origin 的 ls-remote 值; forgejo GET /repos/10CG/Aria/pulls?state=open 与 /repos/10CG/aria-plugin/pulls?state=open 的编号与 head 分支; 主仓根的 find aria/skills -maxdepth 1 -name '*-workspace' 排序后的输出 (2026-09-22 实测本机主仓 aria/skills/ 下已有一个早年 AB 留下的被忽略工作区 issue-triage-workspace/, 故比两次快照之差, 不要求为空; v2.5, post_planning R5 R5-M5)。每条快照命令的退出码都须为 0 (forgejo GET 另须输出可解析的 JSON 数组): 任一不成立 ⇒ 该快照无效 —— 开跑前的不开跑, 结束后的停下上报; 两次都失败会得到两份相同的空记录, 比较恒为「无变化」(v2.5, post_planning R5 同族扫描)",
          "快照比较: 本地面 (HEAD / porcelain / 分支) 除结果目录外有变化 ⇒ 停下上报。skill-creator 工作区不入库、不单列例外 (post_planning R4 R4-M3 按 (b) 裁, 证据见 metadata.revision_log 的 v2.4 R4-M3 条与 tasks.md 判断清单第 35 条), 且只放主仓 aria-plugin-benchmarks/ab-workspace/ 下 (v2.5, post_planning R5 R5-M5 按 (a) 裁, 依据见 tasks.md 判断清单第 44 条): skill-creator 的工作区位置由调用方决定 —— 其 SKILL.md 只以散文给出默认「as a sibling to the skill directory」, 两个脚本都只收调用方传入的目录 —— 主控调用时把工作区指到 aria-plugin-benchmarks/ab-workspace/<本次结果目录名>/ (主仓 .gitignore 该条注释为「结果已落 ab-results/, 无需入库」, 先例 3d3c820 与 2026-09-03-v1.69.0-sibling-spec-probe-rule6 的 PREDICTION.md, 其旧版快照即放在 ab-workspace/…/skill-snapshot), 不用默认落点 aria/skills/<skill>-workspace/: 那里虽被 aria/.gitignore 忽略、不进 porcelain, 却在 TASK-018 的 grep -rn … aria/skills/ 与 no-unresolved-version-placeholder 的 grep -rn … aria/ 两个递归检索面上 (grep -r 不认 .gitignore), AB 之后重跑这两类检查时, 工作区里的旧版快照或 old_skill 臂输出会让它们误红; 作为结果依据的产物 (逐 eval 的 eval_metadata.json 与两臂的 grading.json / response.md / timing.json, 以及 benchmark.json / benchmark.md) 复制进结果目录, 形状对齐先例 2a46d08 (该提交零 workspace 路径); porcelain 出现 *-workspace/ 行 ⇒ 工作区放在了未忽略的位置 (如手册示例的 aria-plugin-benchmarks/<skill>/<skill>-workspace/, 主仓未忽略该模式), 按本条停下; 两次快照的 find aria/skills -maxdepth 1 -name '*-workspace' 之差非空 ⇒ 本次工作区落进了 aria 侧, 停下上报, 不自行删除或移动 (删不删、挪不挪由 owner 定)。远端值有变化 ⇒ 对每个新值在它所属的仓里跑 git cat-file -e <新 SHA> (aria 与另两个子模块的值带 -C <子模块>, 主仓的在主仓根; 在别的仓里查, 对象一律不在, 会被误读成「他人推送」; v2.5): 退出 0 = 本地已有该对象 ⇒ 视为本机推出, 停下上报; 退出 1 = 本地没有 ⇒ 他人推送, 记台账继续; 其它退出码 ⇒ 没查成, 停下; 新增 PR 的 head 分支在本地存在且 SHA 相同 ⇒ 停下上报",
          "开跑前在结果目录写 PREDICTION.md: 逐套件、逐 eval 预测两臂分数; audit-engine 套件另预测 delta",
          "套件: audit-engine.json (eval 1 / 2 / 3) 与 phase-c-integrator.json (eval 1 / 2 / 3) 两臂各跑, 经 /skill-creator; phase-c-integrator-pre-merge-gate.json 不进 AB 臂 (裁定 9), 其 5/8 可执行单测已在 TASK-021",
          "判据 (逐套件): 两个套件都逐 eval 判回归 —— with < without 的 eval 复跑两次, 三个样本中两个以上仍劣即回归; audit-engine 套件另要求 delta.pass_rate = mean(with) − mean(without) > 0 (三条 eval 的均值, 由脚本从两臂 grading 汇总并与 benchmark.json 核对符号) 且 eval id 3 的 without 分数低于 with; phase-c-integrator 套件不看 delta。任一不满足 ⇒ 阻断 TASK-025, 请 owner 裁 (owner_gates 第 5 项)",
          "README / RESULT: catalog 三条命令与 TASK-021 的输出、三条缺口 (wait_then_green 与 NEG-2-timeout 无 node id; NEG-1-malformed 的 node id 过期)、rule6_note 的并集说明、A 与 W; RESULT.md 分套件登记 AB_TEST_OPERATIONS.md 场景 1 验收 delta.pass_rate > 0 的达成情况 (phase-c-integrator 套件预期约 0, 如实登记, 不作阻断); 按场景 1 第 2 步核 transcript 的 push_skipped",
          "结束后先取第二次快照并按本任务的快照比较条完成比较, 然后才跑 metadata.coord_ref_precheck (它会 fetch); 退出 0 才按场景 1 第 3 步强制对齐 (被丢弃的只有本轨 --no-push 心跳); 退出非 0 ⇒ 不对齐, 停下请授权 (owner_gates 第 15 项); 对齐前后的值记台账; 换不带该变量的会话继续, 该会话第一步是 hard_constraints 第 4 条的会话入口 claim 核验 (对齐后解析不到 active 或心跳返回 claim_not_found ⇒ owner_gates 第 14 项; v2.5, post_planning R5 R5-M2)",
          "结果目录与台账由主控在主仓 feature 分支提交, 提交 SHA 记台账 (TASK-027 第 4 步 (c) 用, v2.5)。归属口径 (2026-09-19 实测, 不要按直觉推): 结果目录 aria-plugin-benchmarks/ab-results/ 不在 metadata.commit_attribution 的任何静态集里, 含它的提交一律判 foreign —— 把台账 (exclusive 路径) 放进同一提交也救不了, 因为聚合里 foreign 短路优先于 exclusive (实测「结果目录 + 台账同提交」仍得 foreign)。唯一放行机制 = 调用该判据时把本次结果目录作 extra 传入, TASK-030 的提交范围核验已这样传 (第三个及之后的参数); 故本任务的提交只在传了 extra 的调用面上评判, 不要另找「同提交捎带 exclusive 路径」的替代做法",
      ]),
    T("TASK-025", "5.3", "版本 MINOR 与 CHANGELOG 十三条迁移文案", "S", "2-3", ["TASK-024"],
      ["aria/.claude-plugin/plugin.json", "aria/.claude-plugin/marketplace.json", "aria/VERSION", "aria/CHANGELOG.md", "aria/README.md"],
      "knowledge-manager", "发布文档",
      [
          "并入上游 (改任何版本文件之前): git -C aria fetch origin; git -C aria merge-base --is-ancestor origin/master HEAD 不成立 ⇒ git -C aria merge origin/master (不 rebase); 冲突 ⇒ git -C aria merge --abort, 停下上报 (owner_gates 第 6 项, 恢复指针 aria ec72175); 合并后在不带 ARIA_COORDINATION_NO_PUSH 的会话重跑 TASK-018 与 TASK-021, 全部通过才继续; 合并提交与重跑输出记台账",
          "取号: 记此刻 aria origin/master SHA (即刚并入的值, 供 TASK-027 复核); 读 plugin.json 现值、git -C aria ls-remote --tags origin 与 github 的最高 tag (两条 ls-remote 都须退出 0 —— 失败时输出为空, 会漏掉远端已占的号; 失败先重试再下结论, v2.5)、10CG/Aria#195 的发布号; 新号 = 三者最高者的下一个 MINOR (patch 归 0); 依据记台账",
          "五文件改为新号 (逐处 grep -n 实测后改), 改后复验五处取值一致且都等于新号 (五处都取不到时也「一致」, 故另比新号; v2.5)",
          "CHANGELOG 新节: ### Added (completeness_gate.py、五个输入参数、16 键 stdout 契约) / ### Changed (Step 3-5 改为按 change 匹配与三态) / 迁移文案十三条 = proposal §5 第 1–12 条 (第 2 条的豁免列表补 no_spec_unverifiable; 第 10 条按裁定 11 改写为可由 allow_incomplete_checkpoints 豁免; 两条都以 tasks.md 读前必看第 7 条为准; 第 11 条写明另有跟踪 issue, 号在 Phase D 开出后记周期 handoff) 加「post_brainstorm 不再作为前置依赖」; 用 grep -n '^## \\[' 定位插入点",
          "description 零改动, rule6_note 的 substitute 集不变; 主控在 aria feature 分支提交",
      ]),
    T("TASK-026", "5.4", "引用与编号写法自检 (两次)", "S", "1-2", ["TASK-025"], [LEDGER], "knowledge-manager", "写法规范",
      [
          "第一次 (TASK-027 之前): 把本 cycle 的新增行导出到 scratch 文件 (aria: git -C aria diff <aria 起点>..HEAD 的 + 行; 主仓: git diff <主仓起点>..HEAD 的 + 行), 导出命令退出 0 且导出文件非空 (两仓本 cycle 都有新增行; 导出失败时文件为空, 检查器对空文件照样报 0); 以 python3 -B aria/skills/state-scanner/scripts/check_bare_issue_refs.py --repo-root=<该仓根> <导出文件> 自检: 退出 0 且末行为「裸 issue 引用: 0」= 零命中; 退出 1 = 有命中, 逐条改为全限定写法或注明属 Rule #N 例外; 退出 2 = 读不了文件或参数错 (stdout 为空), 没查成, 停下查明; 带圈与带框编号用 standards/conventions/content-integrity.md §4.5 的自查命令查 —— 该命令对命中与否都退出 0, 有输出即命中, 退出非 0 (如文件不存在) = 没查成, 停下 (v2.5, post_planning R5 同族扫描)",
          "第二次 (在 TASK-031 内, 周期 handoff、回帖与 issue 正文落笔前): 对这些正文做同样两项自检",
          "不以整份文件 rc 0 为门槛 (tasks.md 读前必看第 11 条); A.2 时本目录 tasks.md 与本文件两项自检均零命中; 结果记台账",
      ]),
    T("TASK-027", "5.5", "aria 本地合并、取号复核与终核、合并树回归、打 tag (不推送)", "M", "2-4", ["TASK-026"],
      ["aria master 本地合并提交与 tag v<vNEXT> (未推送)", LEDGER], "backend-architect",
      "多远程硬约束 1: 子模块一律本地合并; 推送前在合并树上重验",
      [
          "步骤固定 1–8, 每步输出记台账; 任一步不成立 ⇒ 停在本步上报 (owner_gates 第 6 项); 恢复只给先例指针 aria ec72175 (owner 确认后在 feature 分支 merge origin/master、重新取号、重跑 TASK-018 / TASK-021 / TASK-026, 台账追加新的取号记录), 做完从 TASK-025 开头重走 (第 2 步的本地可修复分支除外)",
          "第 1 步: git -C aria fetch origin",
          "第 2 步: 仍在 feature 分支, git -C aria status --porcelain 退出 0 且输出为空; 有输出 ⇒ 查明归属后在 feature 分支只 add 被改文件提交, 或上报; 退出非 0 ⇒ 停在本步; 不 stash",
          "第 3 步: git -C aria checkout master, 断言 rev-parse master 等于 rev-parse origin/master; 不等 ⇒ git -C aria merge --ff-only origin/master 后再断言一次, 仍不等 (本地领先) ⇒ 停; 记下此刻 SHA S3 与 git -C aria show master:CHANGELOG.md | grep -oE '^## \\[[0-9]+\\.[0-9]+\\.[0-9]+\\]' | sort -u 的集合 (写入 scratch 文件); 该管道首段 git show 退出 0 (bash 的 PIPESTATUS) 且集合文件非空 (aria 1cb3872 上为 138 个小节, 2026-09-22 实测) —— 集合为空时第 6 步的 comm -23 恒输出为空, 那条检查落空 (v2.5)",
          "第 4 步 取号与 AB 复核: (a) S3 不等于 TASK-025 记下的取号时 SHA ⇒ 停下上报; (b) 上游一侧: 先对 A (TASK-024 记下的 aria origin/master) 与 S3 各跑 git -C aria cat-file -e <SHA>^{commit}, 任一退出非 0 ⇒ 停下上报 —— A 是全计划唯一隔会话从台账抄回的 SHA, 抄错时下面的 diff 输出为空、退出 128, 与真零 diff 同形 (与 TASK-001 基线复核同口径, v2.5, post_planning R5 R5-M4); 再跑 git -C aria diff --stat A S3 -- skills/audit-engine skills/phase-c-integrator: 退出非 0 ⇒ 没比成, 停下上报; 退出 0 且有输出 ⇒ AB 实测的处方文本与将要合并的不同, 停下, 按 owner_gates 第 4 项重跑 TASK-024 后从 TASK-025 重走; 退出 0 且输出为空才过; (c) feature 一侧 (v2.5, post_planning R5 1453c41f —— TASK-026 第一次自检按设计会改本 cycle 的新增行, AB 实测的文本可能不是最终合并的文本): 先对 W (TASK-024 记下的 feature 分支 HEAD) 与 feature 分支现值 (git -C aria rev-parse <feature 分支>; 此刻工作树已切到 master) 跑 git -C aria cat-file -e <SHA>^{commit}, 对 TASK-024 记下的结果提交在主仓根跑 git cat-file -e <SHA>^{commit}, 任一退出非 0 ⇒ 停下上报; 再跑 git -C aria diff --stat W <feature 分支> -- skills/audit-engine skills/phase-c-integrator 与主仓根的 git diff --stat <TASK-024 结果提交> -- aria-plugin-benchmarks/ab-suite/audit-engine.json (比到工作树: 主仓侧没有像第 2 步那样先提交 TASK-026 改动的一步, 比到 HEAD 会漏掉未提交的改动), 退出码判据同 (b); 两者都退出 0 且输出为空 ⇒ 过; 有输出 ⇒ 逐 hunk 按 Rule #6 判据表 (CLAUDE.md 不可协商规则 6, SOT standards/conventions/skill-benchmark-exemption.md) 分类并记台账: 描述性 (schema / 字段 / 命令 / 勘正) ⇒ substitute, 写明覆盖该 hunk 的结构化检查 (如 TASK-026 的写法自检或 TASK-018 的文档机检), TASK-031 勾选时写进 metadata.rule6_note 的 note; 处方性或拿不准 ⇒ 停下, 按 owner_gates 第 4 项重跑 TASK-024 后从 TASK-025 重走",
          "第 5 步: git -C aria merge --no-ff <feature 分支>, 断言 rev-parse HEAD 不等于 S3 且 rev-parse HEAD^2 等于 feature 分支 HEAD (防「Already up to date」退出 0; 两次 rev-parse 都须退出 0 —— 失败时输出为空, 「不等于 S3」会被空串满足, v2.5); 冲突或断言不成立 ⇒ 有 MERGE_HEAD 则 merge --abort, 已产生本轮合并提交则 reset --hard S3 (只丢未推送的本地合并), 以「HEAD 等于 S3 且 porcelain 退出 0、输出为空」收尾后停 (恢复指针同上)",
          "第 6 步 取号终核: 五文件取值等于台账记录的新号; 在 bash 下 comm -23 <第 3 步集合文件> <(git -C aria show master:CHANGELOG.md | grep -oE '^## \\[[0-9]+\\.[0-9]+\\.[0-9]+\\]' | sort -u) 输出为空 (对方发版小节没丢); git -C aria ls-remote --tags origin 与 github 两条都退出 0 且均无 v<vNEXT> (ls-remote 失败时输出为空, 「均无」照样成立; 失败先重试再下结论, v2.5); 不成立 ⇒ 按第 5 步回退后停",
          "第 7 步 合并树原位回归: 仅当 git -C aria status --porcelain 退出 0 且输出为空、且 HEAD 等于合并 SHA 时, 在该工作树跑 TASK-021 第 2 条的三条命令 (会话不带 ARIA_COORDINATION_NO_PUSH; 各放子 shell, 跑完当前目录仍是主仓根)、TASK-018 的全部文档机检、metadata.sc12_liveness 的 L2 (之前先按该键的 guard_config_hooks 判据跑一次, 同 TASK-021 第 3 条; v2.5 补, 交互检查查出), 以及在主仓根跑已启用检查 no-unresolved-version-placeholder 的 command (.aria/state-checks.yaml:29-46): 该 command 以 ! 反转 grep 的退出码并丢弃 stderr, grep 找不到 aria/ 时的退出码 2 会被反转成 0 且无输出、与通过同形, 故先跑 test -d aria/skills 须退出 0 (确认当前目录是主仓根), 再以「退出 0 且无输出」为通过 (v2.5, post_planning R5 同族扫描); Ran 数不得少于 TASK-021 的记录, 差值逐条归因",
          "第 8 步: 回归通过后打附注 tag: git -C aria tag -a v<vNEXT> -m '<一行摘要>'; 回归不通过 ⇒ 不打 tag, 不进 TASK-028",
      ], notes="合并与打 tag 由主控执行 (subagent 不 commit)"),
    T("TASK-028", "5.6", "aria 双推与逐 remote 核验", "S", "1", ["TASK-027"], ["aria master 与 tag v<vNEXT> (origin 与 github)", LEDGER],
      "backend-architect", "多远程硬约束 2; 授权是等待点, 与合并拆开",
      [
          "推送前对 origin 与 github 各跑 git -C aria ls-remote --tags <remote> (都须退出 0; 失败先重试再下结论, v2.5), 确认无 v<vNEXT>; 有 ⇒ git -C aria tag -d v<vNEXT> 后按 TASK-027 第 5 步回退, 停下上报",
          "owner 逐项授权后 (owner_gates 第 7 项) 每个远端一条原子推送, 先 origin 后 github: git -C aria push --atomic <remote> master refs/tags/v<vNEXT>; 禁 --follow-tags 与非原子的多 ref 推送 (master 被拒时 tag 会照样发布成孤儿); 命令超时不少于 300 秒",
          "推后对每个 remote 各跑 git -C aria ls-remote <remote> refs/heads/master 'refs/tags/v<vNEXT>*', 逐行核名字: master 等于本地合并 SHA, tag 行等于 git -C aria rev-parse v<vNEXT>, ^{} 行等于合并 SHA; ls-remote 失败先重试再下结论; 不信 push 回执",
          "被拒或只推成一个远端 ⇒ 不 force、不重打 tag、不改写历史, 原样记台账并停下上报 (owner_gates 第 8 项); 两个远端未都核验一致前不进 TASK-029",
      ], notes="由主控执行"),
    T("TASK-029", "5.7", "主仓发布同步面: aria gitlink、16 个版本点、custom checks", "S", "2-3", ["TASK-028"],
      ["aria", "VERSION", "README.md", "README.zh.md", "README.ja.md", "README.ko.md", "CLAUDE.md",
       "docs/architecture/system-architecture.md", "docs/architecture/version-scheme.md"],
      "knowledge-manager", "主仓同步面多处无机械兜底",
      [
          "前置: TASK-028 已对 origin 与 github 双方核验一致; 否则不 bump (半推后 bump 出的 gitlink 在 github 侧指向不存在的对象, clone --recursive 即断)",
          "gitlink: aria 工作树 HEAD 等于合并 SHA 时 git add aria; 断言 git -C aria merge-base --is-ancestor <动手时 git ls-tree HEAD aria 的值> <合并 SHA> 退出 0 (只前进)",
          "16 个版本点逐处 grep -n 实测后改为新号: README.md 两处 (A.2 时 :8 / :242); README.zh.md / README.ja.md / README.ko.md 各三处 (:3 translated-from / :10 / :244); CLAUDE.md 两处 (:139 / :141); VERSION:24 (A.2 时仍为 v1.73.0, 直接写新号); docs/architecture/system-architecture.md:189; docs/architecture/version-scheme.md:23; 行号以执行时 grep 为准",
          "i18n README 只改版本处 (正文无实质变更, 不重译)",
          "提交信息必须带本轨 trailer: 单起一行 Spec: openspec/changes/pre-merge-completeness-gate-change-scope (10CG/Aria#199) (git-commit.md §6.2 的既有写法)。本任务的**九个版本同步面交付物** (aria gitlink / VERSION / 四份 README / CLAUDE.md / 两份 architecture 文档) 整条落在 metadata.commit_attribution 的 shared 集里, 按本任务的「主控在主仓 feature 分支只 add」条只提交这九个文件 ⇒ 该提交就是纯 shared 集, 不带 trailer 会在 TASK-030 的提交范围核验里判 shared-only 而停在 owner_gates 第 16 项。trailer 无条件必带, 不得因为「台账 (exclusive 路径) 可能同提交捎上去而自动判 own」就省掉 (post_planning R3 minor 638d2a0f: deliverables 含台账与本条「整条落 shared 集」的表述自相矛盾, 此处按「本提交只含九个版本同步面文件」的执行口径消解; v2.4 起 deliverables 也不再列台账, 与姊妹任务 TASK-025 同口径, 矛盾在 deliverables 一侧同样消解); 提交后当场 git log -1 --format=%B 回读确认 trailer 在位",
          "复跑 custom checks: m6-version-badge-match / i18n-readme-translation-currency / plugin-version-arch-docs-match / main-project-version-consistency / no-unresolved-version-placeholder 五条须通过 (逐条判据见本条下半; v2.6 改: no-unresolved-version-placeholder 通过时无输出, 原并列写作「为 OK」与它的实际输出不符); plugin-cache-currency 在 owner 更新插件缓存前预期 STALE; 在主仓根跑, 其中 no-unresolved-version-placeholder 以 ! 反转 grep 的退出码并丢弃 stderr, 跑前先 test -d aria/skills 须退出 0 (做法同 TASK-027 第 7 步, v2.5); 判通过一律看输出首行、不看退出码 (v2.6, post_planning R6 29325b2c): 前四条 (m6-version-badge-match / i18n-readme-translation-currency / plugin-version-arch-docs-match / main-project-version-consistency) 首行须为 OK; no-unresolved-version-placeholder 通过时无输出 (它以 ! 反转 grep 退出码, 故有上句的 test -d 前置); plugin-cache-currency 在 owner 更新插件缓存前首行为 STALE 属预期。首行为 ##SKIP## 的一律算没跑成, 停下查明 —— plugin-version-arch-docs-match 读不到 aria/.claude-plugin/plugin.json 时就打印它并仍退出 0, collectors/custom_checks.py 把它映射为 skip (既不算 pass 也不算 fail); 2026-09-24 在副本实测: 六条在主仓根分别为 OK / OK / OK / OK / 无输出 / OK, 退出码都是 0; 换到 aria/skills/audit-engine/tests 起跑, plugin-version-arch-docs-match 变 ##SKIP## 且仍退出 0、no-unresolved-version-placeholder 仍无输出且退出 0, 其余四条退出 1 或 2",
          "主控在主仓 feature 分支只 add 上述九个版本同步面文件提交; 台账的本任务追加不进这一提交 (它随 TASK-030 第 1 条一并提交), 使本提交的归属判定不依赖台账是否捎带, 与本任务的「提交信息必须带本轨 trailer」条自洽。SHA 记台账",
      ]),
    T("TASK-030", "5.8", "主仓 PR、pre-merge gate (Rule #8)、合并、C.2.5 双推与核验", "S", "2-3", ["TASK-029"],
      ["主仓 PR (Forgejo) 与 master 合并提交", LEDGER], "backend-architect", "主仓集成; C.2.5 委派前核五问",
      [
          "开 PR 前: 主控把台账截至此刻的追加提交到主仓 feature 分支; 不带路径的 git status --porcelain (须退出 0 —— 失败时输出为空, 下面的「不得有行触及」会被空输出满足; v2.5) 原样记台账, 其中不得有行触及本 cycle 交付物 (本目录; .aria/audit-reports/ 下文件名含 pre-merge-completeness-gate-change-scope 的 post_planning 报告; 本次 ab-results 目录; TASK-023 与 TASK-029 的交付物), 其余行逐条记归属; 不 stash, 不顺带提交他人文件",
          "提交范围: git fetch origin 后对 origin/master..<主仓 feature 分支> 跑 metadata.commit_attribution (第三个及之后的参数 = 本次 ab-results 目录; skill-creator 工作区不入库、不作参数 —— 见 TASK-024 快照比较条, post_planning R4 R4-M3), 退出非 0 ⇒ 停 (owner_gates 第 16 项); 输出与 git log --oneline origin/master..<feature 分支> 随第 9 项的授权请求一并呈上",
          "PR 正文与主仓 PR diff 新增行先过 TASK-026 的自检",
          "合并方式: 同步 origin/master 用 git merge (不 rebase); PR 以 merge commit 合并 (不 squash); 经 phase-c-integrator 过 C.2.4 pre-merge gate, 结论记台账, 无可用 backend 时按 no_ci_fallback 显式降级; 本仓 audit.checkpoints.pre_merge 为 off, pre_hook 早退属配置决定 (Rule #10 白名单第一类)",
          "C.2.4.5 子模块指针闸 (v2.5, post_planning R5 R5-M3; SOT = aria/skills/phase-c-integrator/SKILL.md 的 C.2.4.5 段与 scripts/submodule_gate.sh): 本仓 .aria/config.json 未配置 phase_c_integrator.submodule_gate ⇒ 取缺省 mode=block, 该闸已启用 (Rule #10)。其触发条件 (SKILL.md 的 C.2.4.5 段) 是 C.2.4 verdict=green 且即将调用 branch-manager merge action, 而主仓 PR 按 CLAUDE.md 多远程约束 1 的主仓例外走 Forgejo 合并, 不经 branch-manager merge action, 不会被自动触发 ⇒ 由主控在上一条的 C.2.4 green 之后、Forgejo 合并 (owner 合并, 或经第 9 项授权自行合并) 之前显式跑: 在主仓根 (cd <主仓根>)、HEAD 为已推送的主仓 feature 分支 (即 PR head) 时执行 ARIA_SUBMODULE_GATE_MODE=<mode> ARIA_PR_NUMBER=<PR 号> bash aria/skills/phase-c-integrator/scripts/submodule_gate.sh —— <mode> 取执行时 .aria/config.json 的 phase_c_integrator.submodule_gate.mode, 未配置即 block (脚本自身不读配置, 环境变量缺省同为 block; 读到 off 按配置跳过, Rule #10 白名单第一类, 原样记台账)。退出码与完整输出原样记台账, 逐子模块结论行 (OK: / GATE: 及其后的 PASS: 或 BLOCK:) 与末行另摘进台账。放行 = 退出 0, 且 aria 有 GATE: 行与其后的 PASS: aria forward bump (本 PR 前进了 aria gitlink), standards 与 aria-orchestrator 各有一行 OK: … unchanged 或 GATE: 加 PASS: … forward bump; owner 按第 17 项裁了 override 之后重跑的放行判据 = 退出 0, 且被 override 的子模块有 GATE: 行与其后的 ALLOW: … overridden by per-PR marker 行 (脚本的 override 分支打印这一行并继续), 其余子模块照上句 (v2.6, post_planning R6 749f8d15) —— 脚本在没有 .gitmodules 的目录里跑 (如误在 aria 子模块里) 会打印「no .gitmodules in repo; gate trivially passes」并退出 0, 子模块目录缺失时打印「directory absent; skipping」, 只看退出码会放行。退出 1 (block: 某子模块的 feature 指针相对 origin/master 回退或分叉且无 override)、退出 2 / 3 / 4 / 64 / 65 (fetch 失败、origin/master 被改写、子模块对象不全、用法或环境错误: 闸没跑成) 或放行条件缺任一项 ⇒ 不合并, 停下上报 owner_gates 第 17 项; 不自行给任何提交加 Submodule-Rollback: trailer 或给 PR 加 submodule-rollback-approved 标签。本调用方式下 trailer 必须落在 PR head 那个提交上: 闸的 override 检查读的是运行时 HEAD 的提交信息 (check_override_trailer 取 git log -1 --format=%B HEAD), 而闸跑在 Forgejo 合并之前, 那时合并提交还不存在, 写进合并提交的 trailer 闸看不见 (v2.6, post_planning R6 749f8d15); owner 若裁 override, 两个修法各有代价: 把 trailer 放进 PR head 提交 = 改提交信息 = 重写并强推已推送的 feature 分支, 与 owner_gates 第 8 项「不 force、不改写历史」直接冲突, 须 owner 另行裁准, 且分支 SHA 变了之后 C.2.4、本闸、本任务的提交范围核验条与台账记的 SHA 都要重做; 改用 PR 标签则不动提交 (闸经 forgejo GET 读标签, 需要 ARIA_PR_NUMBER; API 失败按无标签处置, 方向 fail-closed) —— 两者相权, 先请 owner 考虑标签。遥测写 aria/metrics/*.jsonl, 被 aria/.gitignore 忽略, 不影响两层 porcelain",
          "合并后: git fetch origin → git checkout master → git merge --ff-only origin/master, 断言 Forgejo 回执里的合并提交 M 是 HEAD 的祖先 (git merge-base --is-ancestor M HEAD) 且 git rev-parse M^2 等于 feature 分支 HEAD; 不能快进或断言不成立 ⇒ 停 (C.2.5 以合并后本地 HEAD 为 expected_sha)",
          "调 C.2.5 前逐条核 metadata.c25_five_questions 的事实并记台账",
          "C.2.5 会对 git submodule status --recursive 的每个子模块执行 git push <remote> master 并以子模块 HEAD 判成功: 调用前对 aria / aria-orchestrator / standards 各自 fetch origin 与 github, 断言本地 master 等于 HEAD 等于 origin/master 等于 github/master (A.2 实测 aria-orchestrator 为 detached 的 237045a、其 master 与两端相同; standards A.2 为 8b49562, 2026-09-19 已前进到 940cb5b ⇒ 两个他轨子模块的 SHA 一律以执行当时实测为准, 不用本文记录值做断言); 任一不成立 ⇒ 停下上报, 不让 C.2.5 顺带推他轨内容",
          "C.2.5 的 per-remote 矩阵对 origin 与 github 均成功且 verify_parity_post_push 为 match, 矩阵原样记台账; 之后再独立 git ls-remote origin master 与 git ls-remote github master 与本地 HEAD 比对; 任一不符 ⇒ 停下上报, 不 force",
          "台账所记主仓提交 SHA 均为 origin/master 的祖先 (git merge-base --is-ancestor)",
          "合并后复核「这个值现在该是什么」: 在合并后的 master 上复跑 TASK-029 的 custom checks; 按 TASK-023 的命令重算 ab-suite 的 skills_covered / total_eval_cases 并与 version.yaml 比对, 再读 version.yaml 的 version 与 changelog 顶条; 任一不一致 ⇒ 停下上报 (他轨同期改动在此显形)",
      ]),
    T("TASK-031", "5.9", "Phase D: 开 issue、勾选、归档预演与 liveness 复跑、归档、释放 claim、回帖关单、周期 handoff、双推", "M", "3-5", ["TASK-030"],
      [f"{SPEC}/tasks.md", f"{SPEC}/detailed-tasks.yaml",
       f"openspec/archive/<YYYY-MM-DD>-{SID}/verification-ledger.md", "docs/handoff/<周期 handoff>.md", "docs/handoff/latest.md"],
      "tech-lead", "跨仓收尾与外向动作协调",
      [
          "先 git fetch origin, 本地 master 快进到含 TASK-030 合并提交的 origin/master; 不能快进 ⇒ 停",
          "不调 phase-d-closer, 逐步对应 (它的全部子步与各自的落点见 tasks.md 判断清单第 25 条): D.1 跳过 (本仓无运行时 UPM, 记台账) / D.post = 按 phase-d-closer 的触发条件 (audit.enabled == true 且 audit.checkpoints.post_closure != off) 执行时读 .aria/config.json 判定: 不成立 ⇒ 按配置跳过 (Rule #10 白名单第一类; 2026-09-21 实读 post_closure 为 off), 成立 ⇒ 照跑 (convergence, max_rounds=1, 不阻断), 读到的值原样记台账 / D.2 = 下方归档预演与 openspec-archive / D.2b = release_gate, 不带 --sweep-stale 与 --gc (sweep / gc 须另行授权) / D.3 = 下方周期 handoff 五条 (子步 2 按模板起稿、2b 写后五字段自校验、3 latest.md 两子步; 子步 1 的触发评估不做 —— 本计划无条件写周期 handoff; 子步 4 的提示提交 = 末条 Phase D 提交) / D.4 = estimator capture 照跑: python3 -B aria/skills/ai-native-estimator/scripts/estimator.py --project-root . capture --spec-slug pre-merge-completeness-gate-change-scope --spec-level 3 --n-tasks 31 (非阻塞, 数据在已忽略的 .aria/estimator/, 失败记台账)",
          "issue (owner_gates 第 10 项, 逐张授权; 开前按关键词定向查重, 不依赖截断清单): (1) 10CG/aria-plugin: --no-spec 声明与 refs/aria/coordination 的 active claim 交叉核验 (裁定 2); (2) 10CG/aria-plugin: 产出侧四个 checkpoint 调用方 (phase-a-planner:246 / task-planner:123 / phase-b-developer:255 / brainstorm:141) 按字面键早退, 对 adaptive 推导失明 (裁定 13); (3) 10CG/aria-plugin: F8 config 注册面缺口 (两个 allow_* 未进 DEFAULTS.json, config.template.json 无 audit 块); (4) 10CG/aria-plugin: 写侧报告命名约定无强制 (附 corpus-freeze.md 争议表与 unattributed 计数); (5) 10CG/aria-plugin: config-loader 无程序化入口 (内联第二副本); (6) 10CG/aria-plugin: audit-engine AB 套件对 pre_merge completeness gate 的覆盖缺口 (rule6_note 义务之三), 附 phase-c-integrator 与 audit-engine 两个套件都不覆盖 hotfix lane; (7) 10CG/Aria: ab-suite/phase-c-integrator-pre-merge-gate.json 的三条 node id 缺口。正文先过 TASK-026 第二次自检; 号回填台账与 ab-results README",
          "勾选: 主控一次把 tasks.md 全部 31 行改为 [x], 同时把 5.2 行的 aria-plugin-benchmarks/ab-results/ 换成本次结果目录全路径 (git ls-files 有输出); 本文件各任务 status 改为 completed; metadata.rule6_note.scenario1 的占位换成该结果目录全路径; TASK-027 第 4 步 (c) 判为描述性、按 substitute 处置的 hunk (若有) 逐条写进 metadata.rule6_note.note (文件、hunk 范围、覆盖它的结构化检查), 无则不写 (v2.5), 并断言五字段 (decision_table_row / description_changed / scenario1 / scenario4b / negctrl) 齐备、无占位尖括号残留 —— SOT §4.1 无机械 enforcement, 这一条是本 cycle 唯一的合规检查点",
          "归档预演 (只读): python3 -B aria/skills/state-scanner/scripts/lib/spec_complete.py --gate openspec/changes/pre-merge-completeness-gate-change-scope, 记 complete / verdict / blocking_reasons / unverified_claims; verdict 为 block ⇒ 停下上报; 预期 unverified_claims 含 4.4 行 dogfood 无可链接产物一条 (A.2 预演见 metadata.a2_state_runs 的 C 态)",
          "SC-12 liveness: 先在 bash 里跑 metadata.sc12_liveness.guard_config_hooks (钉在主仓根) 并按该键判据通过 (末行 rc= 为 0 或 1 且其前无输出; v2.5, post_planning R5 R5-M4), 再在主仓根不加 --force-checked 复跑 sc12_liveness 的代码, L2 与 L3 为真才算 SC-12 通过, L1 为真",
          "D.2 之前请 owner 裁归档 Step 7 建不建 tracker issue (owner_gates 第 11 项), 裁不建则只跳过 Step 7; 其余按 openspec-archive 执行 (git mv 整个目录与归档后落点断言); 归档后的台账写 openspec/archive/<日期>-pre-merge-completeness-gate-change-scope/verification-ledger.md",
          "claim (D.2b): release 之前单独请 owner_gates 第 13a 项 —— 只含这一次协调 ref 推送, 不与 Phase D 提交双推同批 (v2.5, post_planning R5 R5-M1); 获授权后先跑 metadata.coord_ref_precheck, 退出 0 后先把本地协调 ref 强制对齐到 origin (git fetch origin +refs/aria/coordination:refs/aria/coordination, 须退出 0; 命令与理由同 TASK-001 心跳条 —— 前置检查退出 0 含「与 origin 分叉、本地只领先本轨心跳」态, 不对齐直接 release 会把 release 写在本地却推不出去, 留下与第 13a 项「不写仅本地的 release」相反的提交; v2.6, post_planning R6 2c2e8931, metadata.v2_state_runs 的 N12 实测), 再按 TASK-001 的 claim 身份条 (三元组运行时解析那一条) 重跑三元组解析 (0 条 active 直接走下面 claim_not_found 那一分支), 然后才跑 python3 -B aria/skills/state-scanner/scripts/release_gate.py --raw-track-id pre-merge-completeness-gate-change-scope --status done --repo-path <主仓根>; release 的推送按 metadata.coord_push_verify 核验 (released.success 为 true 且 push_success == true 且 push_skipped == false, 再 ls-remote 比对), 任一不成立 ⇒ 停下上报 owner_gates 第 15 项, 不重试、不 force。唯一例外: released.success 为 false 且 released.error 为 claim_not_found —— release_gate 把它记为 benign, 什么都不写也不推, push_success 为 null, 退出 0 (metadata.v2_state_runs 的 N11 实测) —— 不是推送失败, 不落第 15 项: 它说明本轨 claim 已不是 active (中途被 sweep 成 abandoned 等), 原 JSON 与三元组解析结果按 owner_gates 第 14 项的呈递口径呈 owner, 由 owner 裁「先按第 14 项重新认领, 再照本条重跑 release」或「不补认领, 记周期 handoff」(v2.5, post_planning R5 R5-M2)。未获 13a 授权或检查不过 ⇒ 不 release (不写仅本地的 release), 记周期 handoff",
          "10CG/Aria#199 与 10CG/aria-plugin#161 回帖 (版本号、合并 SHA、按 change 匹配与三态的行为变更要点) 后关闭 (owner_gates 第 12 项)",
          "周期 handoff 写 docs/handoff/ (Rule #9), 按模板 aria/templates/session-handoff.md 起稿 (phase-d-closer D.3 子步 2); frontmatter 放在文件最顶部, 五字段 track-id / owner-container / phase / status / updated-at 全写 (Rule #9 SOT standards/conventions/session-handoff.md §2.3.1, 取值域照该节), frontmatter 内不插注释行: track-id 逐字写 pre-merge-completeness-gate-change-scope —— 它同时是 metadata.commit_attribution 判该提交为 exclusive 的唯一依据; 但本任务自身不跑该判据 (调用点只有 TASK-001 与 TASK-030, 见本任务的 latest.md 单独成提交条), 所以 track-id 写错在本任务并不会触发 owner_gates 第 16 项 —— v2.6 删去 v2.5 原写的那个停点 (在 5.9 不可达), track-id 的取值改由写后五字段自校验条的逐字断言守 (post_planning R6 354faf33); owner-container 逐字粘贴 python3 aria/skills/session-closer/scripts/handoff_autofill.py --owner-container 的输出 (handoff-mechanics.md: 机械填, 勿手动组装) —— 该命令失败时打印空串并退出 1 (handoff_autofill.py 的 --owner-container 分支), 粘贴前先看退出码: 退出非 0 或输出为空 ⇒ 按 handoff-mechanics.md 同段的回退, 照模板派生规则手填 (<owner> = git config user.email 的 @ 前段; <container-id> 按 standards/conventions/session-handoff.md §2.3.1 的三态), 回退事实记台账 (v2.5, post_planning R5 ac2e8dcb); 照录 tasks.md 的 AI 流程判断清单并追加 Phase B–D 新增项, 摘录 TASK-022 的活体输出与各 issue 号",
          "写后五字段自校验 (phase-d-closer D.3 子步 2b, 即 session-handoff.md §2.3.7 的 E1; 命令逐字照抄 aria/skills/phase-d-closer/references/execution-steps.md, 含 head -8 窗口): head -8 <handoff> | grep -cE '^(track-id|owner-container|phase|status|updated-at):' 须 ==5; 不足 → 按模板派生规则补齐后重验。不得带缺字段 handoff 进子步 3 (即下面两条的 latest.md 维护)。(口径注: 勿在 frontmatter 内插注释行, 可能把字段推出 head -8 窗口致误报。) 不得改写成对整份文件检索 —— 正文里的同名行会被计入而假绿 (2026-09-21 实测: frontmatter 只有 track-id、正文另有四个同名行时, 整份文件检索得 5, head -8 得 1)。E1 只验字段在不在, 本计划另加一次值非空检查 (不改 E1 原文): head -8 <handoff> | grep -cE '^(track-id|owner-container|phase|status|updated-at): *[^ ]' 须 ==5 —— owner-container 为空串时 E1 照样得 5, 此检查得 4 (v2.5, post_planning R5 ac2e8dcb)。再加一条取值断言 (v2.6, post_planning R6 354faf33): head -8 <handoff> | grep -cxF 'track-id: pre-merge-completeness-gate-change-scope' 的打印值须为 1 —— E1 与上面的值非空检查对多写一个字母的 track-id 都照样得 5, 只有逐字比对拦得住 (本轮反事实实测); 本任务不跑 metadata.commit_attribution, 这条断言是 track-id 取值在 5.9 的唯一守卫, 不为 1 ⇒ 改对后重验, 不得带错值进 latest.md 两子步。按打印值判不按退出码判: 零命中时 grep -c 打印 0 并退出 1 (不是没跑成); 行尾带 CR 时 -x 不匹配, 同样得 0, 方向 fail-closed。输出原样记台账",
          "docs/handoff/latest.md 子步骤 1 (always, 不可跳过; aria/skills/phase-d-closer/references/handoff-mechanics.md「latest.md 维护」, 同文件 Forbidden patterns 逐字「任何 cycle 都不可跳过」): History 表格 prepend 新条目, 格式 - {YYYY-MM-DD HH:MM} — [{name}](./{filename}) ({scope-note} — {summary}); {scope-note} 标 leader / follower:{track-id} / 单轨留空, {summary} 一句 ≤ 80 字符, 时间用 UTC (date -u)。本仓 latest.md 没有字面名为 History 的表 (2026-09-21 实读): 起 History 作用的是 track 表的本轨行与表下按日倒序的说明段 (71c500e 那次维护即改 track 表并在说明段顶部加一段) —— 按执行时实读的版式落这一条, 落点记台账。该节并非本仓从未有过: 16b5bf1 (2026-09-06) 按 SOT 加入 History 节, 同日的合并提交 ecb6296 丢了它 (第一父提交 3f4b379 含该节, 第二父提交 9f25a66 与合并结果都不含, 2026-09-22 实测) —— owner_gates 第 13b 项的请求里注明这段来历, 恢复与否由 owner 裁 (v2.5, post_planning R5 聚合对执笔自报薄弱点第 3 条的裁断)。做完断言 grep -cF '<新 handoff 文件名>' docs/handoff/latest.md 非 0",
          "latest.md 子步骤 2 (conditional): pointer 行 (**Latest**: 字段) 按 handoff-mechanics.md 的三行判定表 —— single-track (tracks_multibranch.exists == false 或 len(tracks) <= 1) ⇒ 更新到新 doc; multi-track 且本 cycle 是项目主线 (其他 container 在 tracks_multibranch 里没有 status==active 的 track) ⇒ 更新到新 doc; multi-track 且本 cycle 是 follower (其他 container 有 status==active 的 track, 且当前 pointer 指向该 leader doc) ⇒ 不更新 pointer (follower 不抢主线; 没有 leader doc 的 follower 退化为 single-track, 照更新)。snapshot.tracks_multibranch 取自本会话过了 metadata.coord_ref_precheck 之后跑的 /state-scanner (hard_constraints 第 4 条; precheck 不通过即按 owner_gates 第 15 项停下, 本子步不做判定), 判定结论与所据字段原样记台账。判为更新 ⇒ **Latest**: 行含新文件名, 前一 Latest 改为 Active (parallel predecessor) 或 superseded (由 owner 判断); 判为 follower ⇒ **Latest**: 行改前改后逐字相同",
          "latest.md 的改动单独成一个提交, 不与周期 handoff、归档同提交: latest.md 是 tasks.md 判断清单第 28 条所称的共享指针 —— 不在 metadata.commit_attribution 的任何静态集, 前 2000 字符里也没有行首的 track-id 行 (2026-09-21 实读全文零处), 含它的提交按该判据判 foreign (v2_state_runs 的 N9 有改共享指针一态, 实测 foreign), 这是维护共享指针的预期结果, 不是执行出错。单独成提交的作用是让 owner 在第 13b 项里看到一份只含共享指针改动的独立 diff, 可以单独否决而不牵连归档与周期 handoff 两个提交; 本任务自身不跑 commit_attribution (它只在 TASK-001 与 TASK-030 调用), 这里不以该判据的归属结果为理由 (v2.5 改写, post_planning R5 聚合对执笔自报薄弱点第 4 条的裁断)。该提交按第 28 条「一律请裁」呈 owner: owner_gates 第 13b 项在本提交产生之后才请, 请求内附它的 diff (v2.4 写的是在原第 13 项的授权请求里点明, 而原第 13 项须在更早的 D.2b 用掉、那时本提交还不存在, 按 post_planning R5 R5-M1 拆为 13a / 13b); 未获授权 ⇒ 与归档、handoff 一样留本地 (第 13b 项的未授权分支), 记台账",
          "Phase D 提交 (归档、周期 handoff、单独成提交的 latest.md) 在上一条的 latest.md 提交产生之后请 owner_gates 第 13b 项, 获授权后双推 (git push origin master 与 git push github master), 推后逐 remote 跑 git ls-remote <remote> refs/heads/master 与本地 master 比对 (ls-remote 须退出 0, 失败先重试再下结论); 被拒或只推成一个 ⇒ 停下上报 (owner_gates 第 8 项), 不 force",
      ]),
]

hours_low = sum(float(str(t["estimated_hours"]).split("-")[0]) for t in tasks)
hours_high = sum(float(str(t["estimated_hours"]).split("-")[-1]) for t in tasks)
agents = {}
for t in tasks:
    agents[t["agent"]] = agents.get(t["agent"], 0) + 1

metadata = {
    "feature": SID,
    "title": "pre_merge Completeness Gate 加 change 维度 (A.2 / A.3 v2.6)",
    "level": 3,
    "spec": f"{SPEC}/proposal.md",
    "datasource": "tasks.md",
    "created": "2026-09-17",
    "updated": "2026-09-24",
    "linked_issue": ["10CG/Aria#199", "10CG/aria-plugin#161"],
    "container": "执笔容器 (非执行期身份): v1 / v1.1 / v2 在 simonfish/023236f2; v2.1 / v2.2 / v2.3 返修在 simonfish/bfe8285d (v2.3 的执笔实例与 v2.2 同, 按 R1 判据: R3 四题 Major 中仅 1 题由 v2.2 返修自身引入, 未过半); v2.4 返修在 simonfish/bfe8285d (v2.4 的执笔实例是 2026-09-21 新会话新派的实例, 与 v2.2 / v2.3 不是同一实例, 跨会话必然换人; 按 R1 判据: R4 四题 Major 中 R4-M1 与 R4-M4 两题由 v2.3 返修自身引入, 2/4 恰一半、未过半, 本不触发换人); v2.5 返修在 simonfish/bfe8285d (owner 2026-09-22 裁定由 v2.4 的执笔实例保留全部上下文续写, 与 v2.4 是同一实例; 按 R1 判据: R5 五题 Major 中 R5-M1 与 R5-M5 两题由 v2.4 返修自身引入, 2/5 未过半); v2.6 返修在 simonfish/bfe8285d (同一执笔实例续写; post_planning R6 按主控定级 0 Major / 5 minor, R1 的换人判据不适用 —— 判据只看 Major 里由上一轮返修引入的占比)。Phase B–D 的执行容器由 TASK-001 在运行时解析, 不由本字段决定",
    "claim": "记录时事实, 不是执行期身份: A.2 2026-09-17 在容器 023236f2 上解析到 claims/023236f2/s-86f7@1836.yaml (track_id pre-merge-completeness-gate-change-scope, 无容器后缀, status active, phase A.2); 该条已于 2026-09-17 转 yielded。2026-09-19 在容器 bfe8285d 上同一三元组解析到 claims/bfe8285d/s-73b9@1606.yaml (status active, phase A.2, linked_issue 10CG/Aria#199)。执行期一律按 TASK-001 的 claim 身份条 (三元组运行时解析那一条) 重新解析, 不引用本行的文件名",
    "total_tasks": len(tasks),
    "estimated_hours": f"{hours_low:g}-{hours_high:g}",
    "agents": agents,
    "verification_ledger": {
        "path": LEDGER,
        "path_after_archive": f"openspec/archive/<YYYY-MM-DD>-{SID}/verification-ledger.md (TASK-031 归档后)",
        "writer": "主控唯一执笔; subagent 只交回命令与原样输出",
    },
    "scope_repos": [
        {"repo": "aria (10CG/aria-plugin 子模块)", "head_at_a2": "1cb3872 (v1.73.3, 与 origin / github 的 master 相同)",
         "proposal_freeze": "301641b", "branch_base": "B.1 实测 origin/master (TASK-001)",
         "surface": "skills/audit-engine/{scripts/completeness_gate.py 新增, tests/test_completeness_gate.py 新增, SKILL.md, references/execution-modes.md, references/report-storage.md, references/pre-write-validation.md} · skills/phase-c-integrator/SKILL.md · skills/phase-a-planner/SKILL.md · skills/phase-b-developer/SKILL.md · 版本 5 文件"},
        {"repo": "Aria (主仓)", "head_at_a2": "a563192 (origin 与 github 两端 ls-remote 相同)",
         "branch_base": "B.1 实测 origin/master; 规划提交未推送时回落为含规划提交的本地 master (TASK-001)",
         "surface": f"{SPEC}/ (tasks.md / detailed-tasks.yaml / corpus-freeze.md / verification-ledger.md) · aria-plugin-benchmarks/ab-suite/{{audit-engine.json, version.yaml}} · aria-plugin-benchmarks/ab-results/<本次目录> · aria gitlink 与 16 个版本点"},
        {"repo": "standards", "head_at_a2": "8b49562 (A.2 2026-09-17 实测); 2026-09-19 复测已前进到 940cb5b (并发轨 10CG/Aria#211 合并所致) —— 本轨不改 standards, 但基线复核与 TASK-030 的子模块断言都以执行当时实测为准; 基线复核的可执行落点 = metadata.baseline_rebase.standards_files (八个被引文件, TASK-001 逐个对 B.1 当时 gitlink 重测)",
         "surface": "不改"},
    ],
    "baseline_rebase": {
        "measured": "2026-09-17, git -C aria diff --shortstat 301641b 1cb3872 -- <文件>",
        "aria_zero_diff": [
            "skills/audit-engine/references/execution-modes.md", "skills/audit-engine/SKILL.md",
            "skills/audit-engine/references/report-storage.md", "skills/audit-engine/references/pre-write-validation.md",
            "skills/audit-engine/references/report-format.md", "skills/audit-engine/references/convergence-algorithm.md",
            "skills/audit-engine/scripts/sibling_spec_probe.py", "skills/audit-engine/tests/test_sibling_spec_probe.py",
            "skills/phase-c-integrator/SKILL.md", "skills/phase-c-integrator/scripts/path_coverage.py",
            "skills/phase-c-integrator/scripts/pre_merge_gate.py", "skills/phase-c-integrator/tests/test_pre_merge_gate.py",
            "skills/phase-c-integrator/tests/test_path_coverage.py", "skills/phase-a-planner/SKILL.md",
            "skills/phase-b-developer/SKILL.md", "skills/task-planner/SKILL.md", "skills/brainstorm/SKILL.md",
            "skills/config-loader/SKILL.md", "skills/config-loader/DEFAULTS.json", "skills/config-loader/config-example.md",
            "skills/agent-team-audit/references/audit-points.md", "skills/state-scanner/scripts/collectors/audit.py",
            "skills/aria-dashboard/references/parse-rules.md", "skills/spec-drafter/LEVEL_GUIDE.md",
            "skills/spec-drafter/SKILL.md", "skills/run_all_tests.sh", "skills/git-remote-helper/SKILL.md",
        ],
        "aria_shifted": [
            "skills/state-scanner/scripts/lib/spec_complete.py: 1 insertion / 1 deletion, 原位改 :1636 注释; 被引的 :924 (if name == \"SKILL.md\") 与 :1642 (两文件皆缺早退) 不移",
            "skills/state-scanner/scripts/collectors/multi_remote.py: 3 / 3, 原位改 :674-675 与 :1158 注释; 被引的 :107-113 不移",
            "skills/state-scanner/scripts/check_bare_issue_refs.py: 301641b 上不存在 (v1.73.0 新增)",
            "CHANGELOG.md: +116; [1.73.0] 现 :104 (proposal 写的 :36 是 f314785 上的号), [1.70.0] 现 :200, 完整性门条目 (301641b :3020) 现 :3136",
            "VERSION: +7 / -3; v1.73.0 的 minor 行现 :7, v1.71.1 的 patch 行现 :8",
            ".claude-plugin/plugin.json: 版本号 (本条与下两条原为一条, 冒号前三个文件名以 / 连写、不是一个路径, 字面代入 git diff 得退出 0 且输出为空; v2.5 按 post_planning R5 11c3a29f 拆开)",
            ".claude-plugin/marketplace.json: 版本号",
            "README.md: 版本号; 另: skills/openspec-archive/SKILL.md 与 skills/phase-d-closer/SKILL.md 有改动但 proposal 未按行号引用 (不在逐文件重测范围)",
        ],
        "standards_files": [
            "conventions/content-integrity.md: §4.4 (check_bare_issue_refs.py 是手动自检工具不是门, tasks.md 读前必看第 11 条) 与 §4.5 (带圈 / 带框编号自查命令, TASK-026 与 hard_constraints 第 12 条) —— 21748d4..940cb5b 实测 +56 / -2",
            "conventions/skill-benchmark-exemption.md: SOT 1.1.0 §4.1 的 rule6_note 五字段模板与 §2 的场景 4b 触发条件; metadata.rule6_note 与 fields_basis 整体建立在它上面 —— 21748d4..940cb5b 实测 +21 / -3",
            "conventions/git-commit.md: §6.2 的 Spec: trailer 写法; metadata.commit_attribution 的 TRAILER 正则与 TASK-023 / TASK-029 的 trailer 要求都引它 —— 2026-09-19 实测该区间零 diff。本条是 v2.3 新补进集合的第七个文件 (v2.2 漏列); 该引用本身措辞是否准确属 post_planning R3 minor 31b4c0f1, 本轮未处置",
            "conventions/session-handoff.md: Rule #9 的 SOT —— §2.3.1 机读 frontmatter 五字段 (track-id / owner-container / phase / status / updated-at) 与 track-id 的字段名和语义 (与该 handoff 所属的 OpenSpec change 1:1 绑定); metadata.commit_attribution 的 exclusive() 判周期 / 会话 handoff 是否本轨完全依赖这个字段名 (按 frontmatter 的 track-id 行逐字比对本 spec id), 其 cannot_catch 与 TASK-031 的周期 handoff 条都逐字引用它, TASK-031 的写后五字段自校验 (§2.3.7 的 E1) 也以这五个字段为准 —— 21748d4..940cb5b 实测零 diff (2026-09-21, 退出码 0 且输出为空)。本条是 v2.4 补进集合的第八个文件: v2.3 的三份计划文件只写 Rule #9 与字段名、零处写该文件名 (冻结快照 71c500e 上三份合计计数为 0), 字面求法因此看不见它, 由 standards_files_basis 的第二步补入 (post_planning R4 R4-M4)",
            "conventions/configured-gate-authority.md: Rule #10 的豁免白名单与「已启用闸门不得 AI 自行豁免」判据 (proposal :510 与 TASK-030 的 pre_hook 早退理由) —— 零 diff",
            "conventions/version-management.md: 版本与 tag 规则 (裁定 4 的 MINOR, TASK-025 取号与 TASK-027 终核) —— 零 diff",
            "openspec/project.md: Level 2 的 A.2 产物形态 (:117), tasks.md 重写 b 的论证前提 —— 零 diff",
            "openspec/templates/proposal-minimal.md: 模板自带 ## Tasks (:28-32), 同上 —— 零 diff",
        ],
        "standards_files_basis": "集合判据 = 本计划实际依赖其内容的 standards 文件 (语义判据, 不是「当初被记过的文件」)。求法分两步, 输入只取冻结快照 (standards 940cb5b 与主仓 71c500e, 与工作树当前内容无关), 脚本与实跑输出见下方 standards_files_derivation, 独立复跑应逐字节得到同一输出。第一步字面计数: 枚举 standards 全仓 102 份 .md (88 个 basename 族), 对三份计划文件 (proposal.md / tasks.md / 生成器) 逐族做区分大小写的子串计数, 三份合计非零即命中 —— 命中 10 族; 排除清单封闭为三族, 各族命中处都不指 standards 内的同名文件: README.md 族 (主仓 README.md、aria/README.md 与归档目录的 README.md, 另有本条排除说明自身对 standards/README.md 与 core/*/README.md 的点名)、README.zh.md 族 (主仓 i18n README, 即 TASK-029 的版本同步面; v2.3 的排除清单漏列此族, post_planning R4 f5b3afad)、tasks.md 族 (本目录 tasks.md, 另有本条排除说明自身对 standards/openspec/templates/tasks.md 的点名) ⇒ 余 7 份。v2.3 只写了「逐条读上下文剔除同名误命中」并点名两族, 剔除步骤是开放判断, 不同复跑者因此得出 7 与 8 两种结果 (post_planning R4 0f027861); 现排除清单封闭, 命中新族即须先判断, 并入上表或入排除清单, 理由记在本条。第二步语义补足: 字面计数只找得到被点名的文件, 以规则号间接引用的 SOT 不写文件名, 它看不见 —— 取三份计划文件引用的 Rule #N (实跑为 Rule #3 / Rule #5 / Rule #6 / Rule #8 / Rule #9 / Rule #10), 按 CLAUDE.md「不可协商规则」各条的 SOT 指针映射, 落在 standards 内的是 Rule #6 / Rule #9 / Rule #10 三份, 其中第一步没有的只有 conventions/session-handoff.md (Rule #3 与 Rule #5 没有 SOT 指针, Rule #8 的 SOT 在 aria 子模块、已在 aria_zero_diff); 它的内容是否被依赖属判断 —— 是 (依赖点见上表该条) ⇒ 补入。两步合计 8 份即上表, TASK-001 对这 8 份逐个重测。两步都覆盖不到的形态 (以概念名间接引用、既不写文件名也不经规则号) 仍靠人读, 不在本求法的保证范围内",
        "standards_files_derivation": {
            "command": "python3 -B standards_files_derivation.py  (在主仓根执行; 脚本全文见 script; 下方 output 由该命令生成, 未手改; 输入只取冻结快照, 工作树改动不影响结果)",
            "script": DERIV_SCRIPT,
            "output": DERIV_OUTPUT,
        },
        "standards": "2026-09-19 实测 git -C standards diff --shortstat 21748d4 940cb5b -- <文件> (21748d4 = proposal 定稿时的 gitlink, 940cb5b = 当前 gitlink): 该区间 standards 全仓只有两个文件变动 —— conventions/content-integrity.md +56 / -2 (新增 §4.4 / §4.5, 须遵守) 与 conventions/skill-benchmark-exemption.md +21 / -3 (本容器 2026-09-17 合并 10CG/Aria#211 所致, SOT 升 1.1.0, 新增 §4.1 rule6_note 五字段最小模板 —— 本文件 metadata.rule6_note 已按其重写)。零 diff 的断言限定在其余六个被引文件 {openspec/project.md, openspec/templates/proposal-minimal.md, conventions/configured-gate-authority.md, conventions/version-management.md, conventions/git-commit.md, conventions/session-handoff.md}, 各自 shortstat 输出为空 (git-commit.md 是 v2.3 新补进被引集合的第七个文件, v2.2 漏列; 2026-09-19 实测同区间同样零 diff; session-handoff.md 是 v2.4 补进的第八个文件, v2.3 漏列, 2026-09-21 实测同区间同样零 diff。2026-09-21 对这六个文件复测, 退出码都是 0 —— 空串是真零 diff、不是没比成, 见 TASK-001 基线复核条的退出码判据, post_planning R4 R4-M1)。**这是对上述六个文件、在 21748d4..940cb5b 之间的断言, 不是对 standards 全仓、也不是对任意时点的全称句** —— v1 / v2 / v2.1 写的「standards 被引文件零 diff」在 940cb5b 落地后即已为假 (post_planning R2 的 PP2-M4)。standards 是并发轨随时会动的共享子模块, TASK-001 必须对 B.1 当时的 gitlink 重测, 不得沿用本行数值; 可执行落点 = 上方 standards_files (post_planning R3 R3-M1: v2.2 只有本句指令, 而 TASK-001 的基线复核条里 standards 零出现, 指令有、落点无)",
        "main_repo": [
            "aria-plugin-benchmarks/ab-suite/audit-engine.json", "aria-plugin-benchmarks/ab-suite/phase-c-integrator.json",
            "aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json", "aria-plugin-benchmarks/ab-suite/version.yaml",
            "aria-plugin-benchmarks/AB_TEST_OPERATIONS.md", ".aria/config.json", ".aria/state-checks.yaml",
        ],
        "main_repo_note": "上列文件 git diff --shortstat bf42cf4 a563192 均为空; proposal.md 自 0a2ae53 起未变 (a563192 上 sha256 d3c9b4f2…6f34)",
    },
    "rulings_applied": [
        "1 追加排除 post_brainstorm ⇒ TASK-010 / 014; SC-18 只留排除分支 (TASK-005); SC-15(5) 期望改为三个 checkpoint (TASK-006); CHANGELOG 加一条 (TASK-025)",
        "2 --no-spec 残余弱点接受 ⇒ 不加固; TASK-031 开 issue 到 10CG/aria-plugin",
        "3 可配置下界不做 ⇒ 无任务",
        "4 MINOR, 号 ship 时重算 ⇒ TASK-025; version.yaml 顺延 ⇒ TASK-023 (复核方式改读 origin/master 上的文件)",
        "5 Rule #6 第三行标签 + 并集执行 ⇒ metadata.rule6_note, TASK-021 / 023 / 024 / 031; AB 判据按套件分 (TASK-024)",
        "6 §1.3(c) 维持 fail-closed ⇒ TASK-012",
        "7 保留收窄后的 (b) ⇒ TASK-012; SC-5 八条反事实 (TASK-019)",
        "8 格 B pass, 格 D 成立 ⇒ TASK-011; SC-15 只留 pass 分支",
        "9 catalog 不进 AB 臂, 跑 5/8 单测, 三条缺口开 issue ⇒ TASK-021 / 024; issue 开在 10CG/Aria (决策单写的仓不存在)",
        "10 两键各自覆盖 spec_level_undetermined; 格 E pass ⇒ TASK-010 / 011; SC-7(d) / SC-9(4) / SC-15(8) 保留",
        "11 allow_incomplete_checkpoints 覆盖 no_spec_unverifiable, no_spec_contradicted 不豁免 ⇒ TASK-011 / 014 / 015; SC-17(5) 改写 (TASK-006); CHANGELOG 的 §5 第 2 条与第 10 条同步改 (TASK-025); proposal 受影响位置全表见 tasks.md 读前必看第 7 条",
        "12 Level 3 ⇒ 本文件与 tasks.md; 三处重写见 tasks.md「读前必看」",
        "13 产出侧调用方不对齐 ⇒ TASK-031 开 issue 到 10CG/aria-plugin; CHANGELOG 第 11 条 (TASK-025)",
    ],
    "test_runner": "新测试一律 unittest.TestCase, 由 skills/run_all_tests.sh 按 unittest 分类。A.2 在 scratch 主仓副本 (aria = 1cb3872) 的基线: audit-engine/tests unittest discover Ran 104 OK; phase-c-integrator/tests Ran 148 OK; state-scanner/tests 不带 ARIA_COORDINATION_NO_PUSH 时 Ran 1605 OK (skipped=1), 带该变量时 FAILED (failures=1, test_heartbeat_only_cli.TestHeartbeatPush.test_refresh_without_no_push_publishes_to_remote) —— 该条断言推送未被跳过, 与环境变量互斥。phase-c-integrator catalog 的五个可执行 node id 与更正后的 NEG-1 方法共 6 条 OK, catalog 字面 NEG-1 node id 报 FAILED (errors=1)",
    "hard_constraints": [
        "子模块合并一律本地 git merge 并双推, 禁 Forgejo 服务端合并 (CLAUDE.md 多远程硬约束 1); 本 cycle 只合并 aria",
        "推后逐 remote ls-remote 核 master 与 tag, 不信 push 回执; push 显式给足超时 (硬约束 2)。协调 ref refs/aria/coordination 的推送 (心跳 / 认领 / release) 同样纳入本口径, 落点 = metadata.coord_push_verify —— v2.2 之前它是全计划唯一推后不做任何核验的推送类 (post_planning R3 R3-M4)",
        "外向动作逐项请 owner 授权, 授权与结果记台账; 全部外向动作与等待点列于 metadata.owner_gates, 各任务里的条目与之一致。唯一例外 = 本容器已有 claim 的心跳刷新 (phase1_gate.py --heartbeat-only, 只推 origin 的 refs/aria/coordination), owner 2026-09-17 裁定免逐次授权; 适用前提 = 推送前 metadata.coord_ref_precheck 退出 0 (本地协调 ref 领先 origin 的只有本轨心跳), 不满足 ⇒ 心跳加 --no-push 并停下请授权 (第 15 项)。免授权只覆盖「发起这次推送」, 不覆盖「推成了没有」—— 推后必须按 metadata.coord_push_verify 核验 (push_success == true 且 push_skipped == false, 再 ls-remote 与本地比对), 与硬约束 2 对 master / tag 的做法同口径, 核验不过按第 15 项停下上报, 不重试、不 force。新写 claim、release_gate 的 release / sweep / gc、推 master / tag / gitlink 仍逐项授权",
        "任何会写或推协调 ref 的动作 (心跳、获授权的认领与重新认领、release) 与任何强制对齐之前, 先跑 metadata.coord_ref_precheck; 退出 0 之后、动手写或推之前, 先把本地协调 ref 强制对齐到 origin (git fetch origin +refs/aria/coordination:refs/aria/coordination, 须退出 0) 并在对齐后重跑三元组解析 —— 前置检查退出 0 覆盖「与 origin 分叉、本地领先的只有本轨心跳」这一态 (metadata.v2_state_runs 的 N6 就有该态), 分叉态下不对齐直接写 / 推, 写得进本地却推不出去 (v2.6, post_planning R6 2c2e8931; N12 实测: 该态下 release 得 released.success 为 true 而 push_success 为 false, 留下与 owner_gates 第 13a 项「不写仅本地的 release」相反的本地提交); Phase B–D 的每个会话在调用 /state-scanner 之前也先跑前置检查并对齐 (它的入口心跳会推送, aria/skills/state-scanner/SKILL.md:182), 不通过则本会话不调 /state-scanner。v2.5 起每个会话的第一步是会话入口 claim 核验 (post_planning R5 R5-M2; 隔日续做、换会话继续都算新会话): 按 TASK-001 的 claim 身份条 (三元组运行时解析那一条) 做三元组解析 → 协调 ref 前置检查条 → 心跳条 (它先把本地协调 ref 强制对齐到 origin 并在对齐后重跑解析, 再 --heartbeat-only, 推后按 metadata.coord_push_verify 核验); 对齐后解析到 0 条 active 或心跳返回 claim_not_found ⇒ owner_gates 第 14 项 (停在当前任务), 前置检查或推后核验不过 ⇒ 第 15 项; 入口核验通过前本会话不调 /state-scanner。理由: TASK-001 之后 claim 的存活原先只靠 /state-scanner 的入口心跳, 而它只在本会话已持 active claim 时才触发 (SKILL.md:182)、失败只记遥测 (SKILL.md:191); claim 超过 SWEEP_TTL (24h, lib/constants.py:58) 不刷新就可能被任一容器的 sweep 改成 abandoned。两处例外: TASK-024 的 AB 会话 (带 ARIA_COORDINATION_NO_PUSH, 心跳推不出去, 两次快照之间也不得 fetch) 不做入口核验, 期间只写本地的心跳也不按上面的通则先对齐 (对齐要 fetch, 与「两次快照之间不得 fetch」冲突; 这些本地心跳推不出去, 由 AB 之后的对齐整体丢弃, 见 TASK-024 的对齐条, v2.6 写明), 由 TASK-024 的前置条让 AB 会话之前的最后一个普通会话补一次核验过的心跳、由它的「结束后先取第二次快照」条让 AB 之后的第一个普通会话先做入口核验; TASK-031 的 release 之后本轨已无 active claim, 此后的会话不再做入口核验, 心跳得 claim_not_found 属预期, 不走第 14 项",
        "执行序 = metadata.execution_order (编号序串行)",
        "CRLF 文件 aria/skills/phase-b-developer/SKILL.md 与 aria/skills/phase-c-integrator/SKILL.md 保持 CRLF: 编辑后、暂存前 metadata.crlf_guard 为真; 对它们比较 frontmatter 前先去掉 CR",
        "主仓 gitlink 只前进, 任何情况下不回退",
        "subagent 不 commit、不写台账; 提交与台账由主控执行",
        "反事实一律三步法 (TASK-019 做法), 补丁由非实现席构造; 基线 RED 只作 RED 证据",
        "期望值不由实现者现算: SC-2 / SC-4 取 corpus-freeze.md 字面量, 其余取 proposal 与 tasks.md 读前必看的字面值; 发现期望值须变 ⇒ 停下走 spec 修订",
        "组 1–4、TASK-023 / TASK-025 的回归重跑与合并树回归在不带 ARIA_COORDINATION_NO_PUSH 的会话里跑; AB (TASK-024) 在带该变量的会话里跑",
        "新写或改动的文字: issue / PR 引用写 <org>/<repo>#<n>, 文内编号不用 # 与带圈字符 (standards content-integrity.md §4.4 / §4.5)",
        "B.2 出现 spec 漂移信号 ⇒ 停在该任务请 owner 裁 (tasks.md 读前必看第 17 条)",
        "判据命令的通用口径 (v2.5, post_planning R5「空输出即通过」同族扫描): (1) 退出码先于输出 —— 判据里的每条命令先看退出码是否落在该命令的结果码集合里 (本计划用法下的 git diff / status / ls-tree / show / ls-remote / fetch / rev-parse 为 0; grep 为 0 = 有命中、1 = 零命中; git merge-base --is-ancestor 与 git cat-file -e 的 0 / 1 本身就是判据; python3 -m unittest 为 0 / 1; 本文件各脚本见其用法注释), 落在集合外 ⇒ 命令没跑成, 停下上报, 不得按「无输出 / 输出为空 / 零命中 / 两侧相同」放行; 管道逐段看 (bash 的 PIPESTATUS: 首段失败时末段照样可能退出 0 并输出空串或 0); 两个命令的输出相比较时, 两侧的退出码都须落在集合里。(2) 运行目录钉死 —— 判据命令默认在主仓根起跑, 仓内命令写成 git -C <路径> …; 含 cd 的命令跑完回到主仓根 (或放子 shell), 下一条判据不依赖上一条留下的当前目录; git -C <子模块> 在子模块未检出 (目录为空) 时会落到主仓上且退出 0, 涉及子模块的判据先确认该子模块已检出。(3) 退出 0 仍可能「没比成」的已知形态逐处写在对应条目里, 不靠本条兜: 路径在两个端点都不存在的 git diff (TASK-001 基线复核条)、以 ! 反转退出码且丢弃 stderr 的已启用检查 no-unresolved-version-placeholder (TASK-027 第 7 步与 TASK-029 的 custom checks 条)、找不到用例仍输出 OK 并退出 0 的 unittest discover (TASK-021 的 SC-12 三条)、对命中与否都退出 0 的 content-integrity §4.5 自查命令 (TASK-026 第一次自检条)、失败时打印空串并退出 1 的 handoff_autofill.py (TASK-031 的周期 handoff 起稿条)、对未去 CR 的 CRLF 文件输出为空的 frontmatter 切片 (metadata.crlf_guard.frontmatter_rule)、读不到 aria/.claude-plugin/plugin.json 时打印 ##SKIP## 并仍退出 0 的 custom check plugin-version-arch-docs-match (.aria/state-checks.yaml 该条 command 的第二行; collectors/custom_checks.py 把「退出 0 且首行 ##SKIP##」映射为 skip, 既不算 pass 也不算 fail; v2.6, post_planning R6 29325b2c)。custom checks 一律以输出首行判, 不以退出码判: 首行为 ##SKIP## 或无输出 (那条以 ! 反转退出码的除外) 都算没跑成, 见 TASK-029 的 custom checks 条",
    ],
    "owner_gates": [
        "1 · TASK-001 · owner 裁定 · 10CG/Aria#195 已完成 C.2 合并或 owner 明示改序; 未满足 ⇒ 不进 B.1",
        "2 · TASK-001 · 外向推送 · 主仓规划提交推 origin 与 github。步骤: git fetch origin 与 git fetch github (两者都须退出 0; 失败 ⇒ 停 —— 远程跟踪 ref 停在旧值, 拿旧值比「两端相同」会放行; v2.5) → 两端 master 相同 (不同 ⇒ 停) → 本地 master 落后或分叉 ⇒ 在本地 master 上 git merge origin/master (不 rebase), 冲突 ⇒ 停 → metadata.commit_attribution origin/master master 退出 0 (否则第 16 项), 其提交清单随授权请求呈上 → 授权后 git push origin master 与 git push github master → 逐 remote git ls-remote <remote> refs/heads/master 等于本地 master。未授权 ⇒ 主仓 feature 分支回落为含规划提交的本地 master, 规划提交随 TASK-030 的 PR 推送 (本容器已有 claim 的心跳刷新免逐次授权, owner 2026-09-17, 不在本项)",
        "3 · 组 1–4 (条件) · owner 裁定 · B.2 出现 spec 漂移信号: 跑单轮 mid_post_spec 还是按 off 处置; 未裁 ⇒ 停在该任务",
        "4 · TASK-024 · owner 启动动作 · 以 ARIA_COORDINATION_NO_PUSH=1 启动 AB 会话, AB 结束后换不带该变量的会话; 未满足 ⇒ 不开跑 / 不进 TASK-025",
        "5 · TASK-024 · owner 裁定 · 任一套件有 eval 判回归 (逐 eval, 三取二); 或 audit-engine 套件的 delta.pass_rate ≤ 0; 或 eval id 3 的 without 臂未低于 with 臂; 未裁 ⇒ 不进 TASK-025。phase-c-integrator 套件只判回归, 不看 delta",
        "6 · TASK-023 / TASK-025 / TASK-027 · 停下上报 · feature 并入 aria origin/master 时冲突 (TASK-023 的「开 AB 会话之前」条 / TASK-025 的并入上游条) / 取号被占 / 合并冲突 / 取号终核不符 / 合并树回归不通过 / 第 2–3 步前提不成立 / AB 之后上游改了 skills/audit-engine 或 skills/phase-c-integrator, 或 feature 一侧在 W 之后对这两个目录与主仓 ab-suite/audit-engine.json 的改动含处方性或拿不准的 hunk (两者都须按第 4 项重跑 TASK-024; feature 一侧 v2.5 补, post_planning R5 1453c41f) / TASK-027 第 4 步的 cat-file 或 diff 退出非 0 (没比成; v2.5, post_planning R5 R5-M4); 恢复只给先例指针 aria ec72175, owner 确认后执行, 做完从出问题的任务开头重走",
        "7 · TASK-028 · 外向推送 · aria master 与 tag 双推; 未授权 ⇒ 本地合并与 tag 保持未推送, 不进 TASK-029",
        "8 · TASK-028 / 030 / 031 · 停下上报 · 推送被拒或只推成一个远端; 不 force、不改写历史、不 bump gitlink",
        "9 · TASK-030 · 外向推送与发帖 · 主仓 feature 分支推送、PR、合并、C.2.5 双推; 未授权 ⇒ 不进 TASK-031",
        "10 · TASK-031 · 外向发帖 · 七张 issue 逐张授权; 未授权的不开, 记周期 handoff",
        "11 · TASK-031 · owner 裁定 · 归档 Step 7 建不建 tracker issue; 裁不建 ⇒ 只跳过 Step 7",
        "12 · TASK-031 · 外向发帖 · 10CG/Aria#199 与 10CG/aria-plugin#161 回帖并关闭; 未授权 ⇒ 记周期 handoff",
        "13a · TASK-031 (D.2b, release 之前请) · 外向推送 · release_gate 释放本轨 claim 的协调 ref 推送, 单独一项授权, 不与 Phase D 提交双推同批 —— owner 2026-09-17 的原意是「新写 claim、release_gate 的 release / sweep / gc … 仍逐项授权」(hard_constraints 第 3 条; v2.5 拆分, post_planning R5 R5-M1)。未授权 ⇒ 不 release (不写仅本地的 release), 该事实写进之后起稿的周期 handoff 并记台账, Phase D 其余步骤照常",
        "13b · TASK-031 (latest.md 的单独提交产生之后才请) · 外向推送 · Phase D 提交双推 —— 归档提交、周期 handoff 提交与单独成提交的 docs/handoff/latest.md 改动; 请求内附 latest.md 那一提交的 diff (tasks.md 判断清单第 28 条「共享指针一律请裁」的落点), 并注明 latest.md 的 History 节来历 (见 TASK-031 的 latest.md 子步骤 1 条)。未授权 ⇒ Phase D 提交全部留本地, 记台账; owner 对 latest.md 那一提交另有裁定 (撤回、改写后再请等) ⇒ 照裁定执行, 改写过的 diff 重新随本项呈上后再推。13a 已批并已 release 而本项未批 ⇒ 协调 ref 上本轨已是 done、归档与周期 handoff 只在本地: 这一中间态原样记台账",
        "14 · TASK-001, 以及 Phase B–D 任一会话的入口 claim 核验 (hard_constraints 第 4 条) 与 TASK-031 的 release (条件: 三元组解析不到本容器同轨的 active claim —— 解析到 done / yielded / abandoned 任一终态, 或本容器该轨无任何 claim; 或心跳 / release 返回 claim_not_found。v2.5 起挂载从 TASK-001 扩到任意会话, post_planning R5 R5-M2) · 外向推送 · 用原串 pre-merge-completeness-gate-change-scope 重新认领 (--mode advisory --linked-issue 10CG/Aria#199 --include-terminal, --phase 取当时所在阶段), 认领前 metadata.coord_ref_precheck 退出 0; 未授权 ⇒ 不重新认领 (不写仅本地的 claim), 停在当前任务等授权 (TASK-031 的 release 另见其 release 条: 可由 owner 裁为不补认领)。四态里三个终态的下一步相同 (都必须重新认领: heartbeat_by_track 只刷新 active, 终态 claim 既不被心跳续命也不被 sweep 再动, 继续干活等于无 claim 在场), 差别只在呈递 owner 的事实与措辞: abandoned = 被 sweep 判超时, 呈递「本轨仍在进行」的证据; yielded = 前一容器主动让出 (本轨 2026-09-17 即此形态: 023236f2 让出、bfe8285d 接手), 呈递接手方身份; done = 已被判完成, 呈递为何继续 (误释放, 或范围外新增)。--include-terminal 对三态同样必要 —— 不带它, takeover 判据看不见终态 claim",
        "15 · TASK-001 / TASK-024 / TASK-031 与 Phase B–D 各会话的入口 claim 核验 (hard_constraints 第 4 条, 须在调用 /state-scanner 之前) · 停下请授权 · metadata.coord_ref_precheck 退出非 0 (本地协调 ref 领先 origin 的提交含本轨心跳以外的写入, 或取不到远端值): 心跳加 --no-push 或本会话不调 /state-scanner, 不强制对齐, 不认领、不 release; 领先提交涉及的文件列表随请求呈上。v2.3 起本项另一触发条件 = 协调 ref 推后核验不过 (metadata.coord_push_verify: 心跳 / 认领 / release 返回 push_success 非 true, 或在不带 --no-push 的会话里 push_skipped 为 true, 或 ls-remote 与本地不一致且本地值不是远端的祖先): 不重试、不 force, 原样 JSON 与两侧 SHA 随请求呈上",
        "16 · TASK-001 / TASK-030 · owner 裁定 · metadata.commit_attribution 退出非 0: 待推送的主仓提交里含 foreign / foreign-merge (非本轨提交), 或含 shared-only (整条只落发布同步面、又没带本轨 Spec: trailer —— 典型是并发发版轨的 chore(release) 主仓同步面, 也可能是本轨 TASK-029 或 TASK-023 漏写 trailer —— 这两个任务的交付物结构上都不含 exclusive 路径): 逐条清单与 kinds 呈 owner; 未裁 ⇒ 不推送、不开 PR。退出 2 (v2.5 起: git log 读不出 基准..目标, ref 写错或对象缺失) 是没跑成, 不呈 owner 裁归属: 查明基准 / 目标 ref 后重跑, 仍为 2 ⇒ 停下上报",
        "17 · TASK-030 · 停下上报 · C.2.4.5 子模块指针闸 (aria/skills/phase-c-integrator/scripts/submodule_gate.sh, 本仓缺省 mode=block) 没放行: 退出 1 (block —— 某子模块的 feature 指针相对 origin/master 回退或分叉, 且无 override), 或退出 2 / 3 / 4 / 64 / 65 (闸没跑成), 或退出 0 却缺 TASK-030 该条要求的逐子模块结论行: 不在 Forgejo 合并, 原样输出随请求呈上; override 只由 owner 决定, 执行者不自行添加: 本调用方式下闸读运行时 HEAD 的提交信息, 所以 Submodule-Rollback: trailer 须落在 PR head 那个提交上 (写进 Forgejo 合并提交的 trailer 闸看不见) —— 这等于改写并强推已推送的 feature 分支, 与本表第 8 项「不 force、不改写历史」冲突, 须 owner 一并裁准并重做 C.2.4、本闸与提交范围核验; 或改用 PR 标签 submodule-rollback-approved (不动提交; 需 ARIA_PR_NUMBER, API 失败按无标签)。owner 裁 override 后重跑, 放行 = 退出 0 且被 override 的子模块有 GATE: 加 ALLOW: 行、其余子模块照 TASK-030 该条 (v2.6, post_planning R6 749f8d15); 闸拿 HEAD 与 origin/master 的 gitlink 直接比, 同步合并之后 origin/master 又前进 (他轨 bump 了某子模块) 也会判 block, 是否重新同步后重跑同样由 owner 裁; 未裁 ⇒ 不合并 (v2.5, post_planning R5 R5-M3)",
    ],
    "rule6_note": {
        "decision_table_row": 3,
        "description_changed": "no",
        "scenario1": "aria-plugin-benchmarks/ab-results/<TASK-024 本次结果目录> (TASK-024 跑完记目录名, TASK-031 勾选时回填全路径; 两个套件 ab-suite/audit-engine.json 与 ab-suite/phase-c-integrator.json 各两臂)",
        "scenario4b": "not_required",
        "negctrl": "n/a",
        "fields_basis": "逐字段依据 (SOT standards/conventions/skill-benchmark-exemption.md 1.1.0 §4.1): decision_table_row 取第三行 = 裁定 5 的档位标签 (套件覆盖外), 但执行上取两读法并集、不取任何豁免 ⇒ scenario1 照跑并填结果目录而非 n/a; description_changed 为 no 的判据 = TASK-015 / 016 / 017 改前改后比**四份**被改 SKILL.md 的 frontmatter, 逐字相同 (逐字列名: audit-engine / phase-c-integrator / phase-b-developer / phase-a-planner; TASK-018 复核, 四份即本 cycle 被改 SKILL.md 的全集); 据 §2 只有 description 变动才须跑场景 4b ⇒ scenario4b 记 not_required, 据 §4.1 的合规判据 (description_changed 为 yes 时 scenario1 / scenario4b 不得为空或 not_required) 本组合合规; negctrl 是场景 4b 触发率评测的被评/负控命中数, 无 4b 即无该数 ⇒ n/a。第三行的三条义务另行满足, 见 note",
        "note": "档位标签 = 判据表第三行 (裁定 5), 执行两读法的并集, 不取任何豁免。tasks.md 读前必看第 19 条新增的同形改写 (phase-c-integrator/SKILL.md:57 与 :754、audit-engine/SKILL.md:423) 属处方性 · 运行时指令面, 与步骤 3 同批随两个照跑套件跑; 两个套件都不覆盖 hotfix lane, 该缺口写进 TASK-031 第 6 张 issue, 文本落点由 N8 守。照跑面: ab-suite/audit-engine.json (加 eval id 3 后 3 evals) 与 ab-suite/phase-c-integrator.json (3 evals) 两臂照跑 (TASK-024)。phase-c-integrator-pre-merge-gate.json 不进 AB 臂 (裁定 9: 无 evals 键, total_eval_cases 计 0), 改跑其 5/8 可执行 fixture 单测 (TASK-021), 三条缺口开 issue 到 10CG/Aria (TASK-031)。第三行三义务: 点名行为 = proposal rule6_note 的 A / B / C; 定向 fixture = eval id 3, 可证伪判据 = without 臂 (AB 开跑时 aria origin/master 的快照) 分数低于 with 臂; 套件缺口 issue 开到 10CG/aria-plugin (TASK-031)。substitute 实体 = SC-1~SC-10 + SC-13 + SC-15~SC-17 + SC-19~SC-22, 另加本文件的 N1–N4 / N7 / N8。description 字段零改动 (TASK-015 / 016 / 017 的 frontmatter 比较)。",
    },
    "new_checks": {
        "why": "裁定 1 / 11、stdlib-only、调用串逐字相等与同形改写在 proposal 的 SC-13 里没有可执行的落点; 只增不改。n1–n3 的三态见 metadata.a2_state_runs, n4 / n8 的见 metadata.v2_state_runs",
        "code": NEW_CHECKS,
        "cannot_catch": "N1 / N2 / N8 只看文本落点, 拦不住条款语义写错或同义改写 (由 SC-16 / SC-18 / SC-17(5) 的运行时断言守); N3 拦不住 importlib 或 __import__ 的动态导入; N4 只比两处调用串与 canonical, 不看调用串周围的说明文字",
    },
    "sc13_baseline": "A.2 在 aria 1cb3872 实测: execution-modes.md 中 {checkpoint_name}-*.md 计数 2; audit-reports/[a-z_]*-{timestamp}.md 残留 4 处 (phase-a-planner:267 / phase-b-developer:204,277 / phase-c-integrator:157); audit-engine/SKILL.md 中 completeness_gate.py 0; phase-c-integrator/SKILL.md 中 change_id 3、「checkpoints 显式值 > adaptive_rules 推导值」0、anchor_base 0、「4.5 completeness gate 三态处置」0、「not_applicable → workflow report 必带」0、「unattributed_count > 0」0、mode == \"convergence\" 0、mode == \"challenge\" 0、「照常调用门」0; report-storage.md 中「不计入」0、「子目录内的报告不计入完整性证据」0、「三个桶都不收」0; execution-modes.md 中 adaptive_rules 3、「stdout 非 JSON」0、「跳过校验, 继续执行 pre_merge 审计」1、「仍逐对评估三态并全部留痕」0, §入口逻辑内两条逐字串 0, bypassed 文案两种拼法 (:44 by config / :82 missing=)。另: phase-c-integrator/SKILL.md 按字面键判 pre_merge 的还有 :57 与 :754, audit-engine/SKILL.md:423 同一条件另一写法 (见 TASK-015 / 016, N8 基线为假)",
    "sc12_liveness": {
        "acceptance": "L2 与 L3 同真; L1 只作归档门不拦的确认 (tasks.md 重写 a)",
        "code": SC12_CODE,
        "blind_spots": "L1 在脚本缺失 (ambiguous) 与「散文 + ab-suite json 字面路径」(generic_path_call) 两态下为真; L2 对「phase-c-integrator/SKILL.md 的 bash 块调用」同样为真, audit-engine/SKILL.md 这一处由 SC-13 的分块计数单独守。另: 分类器把任何 */.aria/config.json 与 hooks.json 中出现的符号名判为 aria_plugin_integration (spec_complete.py:733-744); A.2 时仓内这类文件都不含该符号, 本计划也不改 config, 故 TASK-021、TASK-027 第 7 步与 TASK-031 复跑 L2 前先跑 guard_config_hooks 并按其判据通过 (末行 rc= 为 0 或 1 且其前无输出; v2.5 起钉在主仓根并看退出码, post_planning R5 R5-M4; 各态见 metadata.v2_state_runs 的 N10)",
        "guard_config_hooks": "git -C <主仓根> grep --recurse-submodules -l -F completeness_gate | grep -E '(^|/)(hooks\\.json|\\.aria/config\\.json)$'; echo \"rc=${PIPESTATUS[0]}\" —— 在 bash 里跑, <主仓根> 写主仓根的绝对路径: 钉在主仓根执行, 与当前目录无关 (v2.5, post_planning R5 R5-M4: 不带 -C 时 git grep 只搜当前目录所在的仓、且只搜当前目录以下 —— TASK-021 的 SC-12 三条那一条刚 cd 进 aria 子目录, 顺序执行时它看不到主仓 .aria/config.json, 退出 1 且无输出, 真空通过)。判据: 末行 rc= 的值须为 0 或 1 (0 = 仓内有文件含该符号, 1 = 一处都没有), 其它值 = git grep 没跑成 (如路径不是仓, 退出 128), 停下上报, 不得当作通过; rc= 行之前有任何输出 ⇒ L2 可能被配置文件带绿, 停下查明; rc 为 0 或 1 且其前无输出 ⇒ 通过 (各态见 metadata.v2_state_runs 的 N10)",
    },
    "a2_state_runs": {
        "what": "tasks.md 重写 a 的三态 (另加两个对照态) 与 N1 / N2 / N3 的三态, 在 scratch 主仓副本 (主仓 a563192 + aria 1cb3872 嵌套 clone) 上实跑; 副本外零写入",
        "command": "python3 -B a2_state_runs.py <scratch 主仓副本根> <本目录 tasks.md> <本文件>  (脚本全文见 script; 下方 output 由该命令重生成, 未手改)",
        "script": script_text,
        "output": run_output,
    },
    "c25_five_questions": [
        "做不做: 对每个 enforced remote 先推子模块 (git push <remote> master) 再推主仓 master, 然后仅对主仓调 verify_parity_post_push (phase-c-integrator/SKILL.md:612-623)",
        "怎么做: git-remote-helper/scripts/push_all_remotes.sh 推的是本地分支 master, 成功判据 = 退出码 0 且本地 refs/remotes/<remote>/master 等于 HEAD (:103-119), 子模块不做 ls-remote 核验 ⇒ aria 的硬约束 2 由 TASK-028 承担",
        "失败会不会红: 本仓 .aria/config.json 没有 multi_remote 段, phase_c_integrator 下也没有 multi_remote_push, 取 config-loader/DEFAULTS.json:6-15 的缺省 —— fail_on_partial_push 为 true, read_only_remotes 为 [] ⇒ 阻断并给修复命令 (SKILL.md:625-630)",
        "何时触发: 「Phase C.2 合并成功 (master 已 fast-forward)」, expected_sha = 合并后本地 master HEAD (SKILL.md:603, :613) ⇒ 服务端合并后本地未快进会拿陈旧 SHA, 故 TASK-030 先快进",
        "枚举哪些对象: git submodule status --recursive (SKILL.md:614) ⇒ 本仓三个 (aria / aria-orchestrator / standards, A.2 实测); 子模块 detached 时比 HEAD (:638) ⇒ aria-orchestrator 属他轨, TASK-030 事前断言其无待推内容",
    ],
    "execution_order": "编号序串行: tasks 列表顺序即 tasks.md 编号序 1.1 → 5.9, 单执行席依次执行 (决策单 Q3)。dependencies 只标数据依赖, 不表示可以并行。唯一例外 = TASK-026 分两次, 第二次在 TASK-031 内",
    "canonical_call": CANONICAL_CALL,
    "stage_cells": {
        "rule": "组 2 的中间任务 (TASK-008~011) 只验收本段完成后即可在命令行观测到的子格; 这些子格的运行都在 P6 之前以终局结束 (error / bypassed / 格 A–E) 或只依赖参数与常量。每个 SC 的每一格都包在 self.subTest(cell=<名字>) 里, 断言一律写在 subTest 内 (含脚本存在断言), 格名形如 <SC>.<子格>; 下表所列格名逐字照用。验收 = code 的命令对本任务及之前各任务所列的格退出 0; 其余格失败属预期。SC 方法级全绿只在 TASK-012",
        "cells": {
            "TASK-008": ["SC-10.argparse-missing-base", "SC-10.argparse-missing-repo-path", "SC-10.argparse-missing-diff-repo-path", "SC-10.argparse-mutex", "SC-10.config-unreadable", "SC-10.error-verdict-keyset", "SC-15.1-empty-config", "SC-15.1-no-audit-block", "SC-15.1-no-config-file", "SC-17.7-missing-diff-repo-path", "SC-21.1-defaults-equal", "SC-21.2-mapping-table-equal", "SC-21.3-bad-json"],
            "TASK-009": ["SC-5.8-no-spec-empty-diff", "SC-7.S4-unresolved", "SC-7.no-spec-contradicted", "SC-7.typo-unanchored", "SC-7.b-anchor-literal", "SC-17.4-cross-no-spec-contradicted", "SC-17.5a-no-flag", "SC-22.3-base-unresolvable"],
            "TASK-010": ["SC-15.5-typo-mode", "SC-20.3-level-undetermined"],
            "TASK-011": ["SC-7.e-adaptive-level1", "SC-9.2-S4-bypassed-manual", "SC-9.2-S4-bypassed-adaptive", "SC-9.3-unanchored-not-exempt", "SC-9.4-level-undetermined-bypassed", "SC-15.2-cell-C", "SC-15.3-cell-B", "SC-15.4-legacy-pre-merge-only", "SC-15.6-cell-D", "SC-15.7-cell-B-convergence", "SC-15.8-cell-E", "SC-15.9-two-changes-cell-D", "SC-15.9-explicit-pre-merge-cell-C", "SC-17.5b-dangling-only", "SC-17.5c-bypassed", "SC-17.5d-contradicted-with-flag"],
        },
        "code": CELL_STATUS_CODE,
        "cannot_catch": "只证明所列格按其断言通过, 不证明断言写对 (由 TASK-019 / 020 的反事实守); 格名是约定, 改名会显示为 not-run 而判红",
    },
    "coord_push_verify": {
        "why": "协调 ref (refs/aria/coordination) 的推送在 v2.2 之前是全计划唯一推后不做任何核验的推送类, 与 CLAUDE.md 多远程硬约束 2「推后逐 remote ls-remote 核验, 不信 push 回执」直接冲突; 它偏偏又是 owner 2026-09-17 免逐次授权的那一类, 免授权的隐含前提「它会发布出去」从未被验证。失败后果: 心跳没推出去而验收通过, 24 小时后 origin 侧 claim 被 sweep 成 abandoned, 他容器据此接手本轨 (post_planning R3 R3-M4)",
        "assert": "心跳 / 认领 / release 三类推送共用: (a) 本次确实写了 ref (心跳 outcome == refreshed; 认领 proceed 为 true; release released.success 为 true); (b) push_success == true; (c) push_skipped == false; (d) 推后独立跑 git ls-remote origin refs/aria/coordination, 与本地 git rev-parse refs/aria/coordination 逐字相等。(d) 不等时不得直接判失败 —— 协调 ref 是多容器共写的: 先 git fetch origin refs/aria/coordination, 本地值是 FETCH_HEAD 的祖先 ⇒ 他容器在本次推送之后又叠加了自己的 claim, 属正常; 否则停。任一不成立 ⇒ owner_gates 第 15 项, 不重试、不 force",
        "no_push_branch": "带 ARIA_COORDINATION_NO_PUSH 的会话或显式 --no-push 时期望值相反, 且不算失败: push_skipped == true 且 push_success == false 且 push_skipped_reason 为 env_var 或 cli_flag, 此时不做 (d) —— 它本来就没推。组 1–4 的会话按 tasks.md 读前必看第 12 条不带该变量, 故这几个任务里跑出 push_skipped == true 即说明会话环境不对; TASK-024 的 AB 会话按 owner_gates 第 4 项必须带该变量, 那一段的期望值就是本行",
        "measured": "2026-09-19 在 scratch 临时仓实测 (git init -b master, 裸仓作 origin, 先认领再心跳), 四态互不相同: (1) 正常推送 ⇒ outcome=refreshed / push_success=true / push_skipped=false, exit 0, ls-remote 与本地 rev-parse 相等; (2) ARIA_COORDINATION_NO_PUSH=1 ⇒ refreshed / false / true, reason=env_var, exit 0; (3) --no-push ⇒ refreshed / false / true, reason=cli_flag, exit 0; (4) origin 指向不存在路径 (push 真失败) ⇒ refreshed / false / false, reason=null, exit 0。release_gate.py 三态同形: 正常 true / false; 带环境变量 false / true / env_var; push 失败 false / false / null (另 fetch_success=false)。(4) 与 (1) 只在 push_success 上分得开 —— 这正是 v2.2 只断言「期望 outcome refreshed」会假绿的原因",
        "cannot_catch": "只核「这一次推送到没到 origin」: 协调 ref 只推 origin, 硬约束 2 的双远端口径不适用于它; ls-remote 自身失败要重试几次再下结论 (与硬约束 2 同); 推成功后他容器随即 force 覆盖不在本检查面内 (那是 coord_ref_precheck 与 reconcile 的事)",
    },
    "coord_ref_precheck": {
        "code": COORD_PRECHECK_CODE,
        "own_claim_files": "TASK-001 在运行时按 (本容器, 归一 track_id, active) 三元组解析出的 claim 文件, 可能不止一条 (见 TASK-001 的 claim 身份条 (三元组运行时解析那一条) 里的多条分流), 不是写死的路径 —— A.2 记录的 claims/023236f2/s-86f7@1836.yaml 只是当时的解析样例, 该条已于 2026-09-17 转 yielded; 重新认领后以新的解析结果整体替换。反向指针 (生产用法 vs fixture 做法): metadata.v2_state_runs 的 N6 在临时仓自造一条本轨 claim, 并从 phase1_gate 返回的 own_claim 回填本参数 —— 那是取证脚本为了不依赖执笔容器身份与真仓此刻的认领状态而做的等价构造, 等价对象正是本字段在生产里的运行时解析; 生产路径不自造 claim, 只解析",
        "cannot_catch": "只看本地领先 origin 的提交; 远端已有而本地没有的内容不在检查面 (那是 fetch 的事); 心跳 commit 若由其它工具改写了格式 (不止 heartbeat_at 一行) 会判 other 而停下, 方向是 fail-closed",
    },
    "crlf_guard": {
        "code": CRLF_GUARD_CODE,
        "files": ["aria/skills/phase-b-developer/SKILL.md", "aria/skills/phase-c-integrator/SKILL.md"],
        "frontmatter_rule": "awk 'NR==1&&$0==\"---\"{f=1;next} f&&$0==\"---\"{exit} f' 对 CRLF 文件直接跑输出为空 (两侧同为空串, 比较恒真); 先 tr -d '\\r' 再切; 比较前另断言两侧切出的块都非空、各含一行以 description: 开头 —— 忘了去 CR、git show 失败或路径写错时切出的都是空串, 两侧同空则比较恒真, 这条正向断言把三种情形都拦下 (v2.5, post_planning R5 同族扫描)",
    },
    "commit_attribution": {
        "code": ATTRIB_CODE,
        "cannot_catch": "只按路径、handoff 的 track-id 与提交信息的 Spec: trailer 判归属, 不看改动内容; 本轨路径集内的他轨改动仍会判 own。收紧后的代价 (v2.3 按 31 个 TASK 的 deliverables 全量重跑路径分类后改写 —— v2.2 写的「代价只有 TASK-029 漏写 trailer」漏了另外两个形态, post_planning R3 R3-M2): 主仓侧结构上不含 exclusive 路径的交付物共两组, 都必须靠 trailer 才判 own-release-sync —— TASK-029 的九个版本同步面文件, 与 TASK-023 的 ab-suite/{audit-engine.json, version.yaml}; 任一漏写即停在 owner_gates 第 16 项 (fail-closed, 代价是多一次请裁, 不是漏放)。另三类不靠 trailer, 各有自己的兜法: 本轨工具目录 .aria/notes/2026-09-17-199-a2-a3-tooling/ 自 v2.3 起进 exclusive 前缀集 (v2.2 漏列, 真提交 12c870d 因此判 foreign); 本次 ab-results 目录不在任何静态集里, 含它的提交一律判 foreign, 且 foreign 在聚合里短路优先于 exclusive (与台账同提交也不改判, 2026-09-19 实测) ⇒ 唯一放行机制是调用时把它作 extra 传入: TASK-030 的调用已这样传, 而 TASK-001 与 owner_gates 第 2 项这两个调用点都发生在 ab-results 产生之前, 结构上不受影响; TASK-031 的周期 handoff 判 exclusive 的充要条件是 frontmatter 的 track-id 逐字为本 spec id (Rule #9 五字段之一; 2026-09-19 实测仓内 207 份 handoff 有 178 份带该字段), 写成别的或漏写即判 foreign —— 这是该判据被调用时的判法; TASK-031 自身不调用它 (调用点只有 TASK-001 与 TASK-030), 所以 5.9 周期 handoff 的 track-id 取值改由 TASK-031 写后五字段自校验条的逐字断言 (grep -cxF 须为 1) 守 (v2.6, post_planning R6 354faf33)。trailer 是声明不是证明: 他轨若在只落 shared 集的提交里写上本轨 trailer 会被判 own —— 需要伪造意图, 且 owner_gates 第 2 / 9 项仍要求把 git log 清单呈给 owner, 人这一关不撤。docs/handoff/latest.md 这类共享指针一律判 foreign (由 owner 裁)",
    },
    "revision_log": [
        "v1 (2026-09-17): 首版, 31 项 / 5 组",
        "v1.1 (2026-09-17): 主控核验返修 —— 本容器已有 claim 的心跳刷新免逐次授权 (owner 2026-09-17), 条件性重新认领单列为等待点第 14 项",
        "v2 PP1-M1 (聚合表 PP1-M1): TASK-008~011 改为按 stage_cells 验收, SC 级全绿与 missing 的豁免降级移到 TASK-012, SC-7(e) 归到 TASK-011。自检: 格表由 P 阶段终局推出, 每格的运行在 P6 前结束或只依赖常量; cell_status 三态 (含未执行与执行两次) 已跑, 不会因格名缺失而假绿",
        "v2 PP1-M2: TASK-014~018 串成链且以 TASK-013 为起点, TASK-019 / 020 依赖 TASK-018, 新增 execution_order。自检: 所有依赖指向更小编号, 与 tasks.md 编号序一致; TASK-013 的 porcelain 断言此时不再受组 3 影响",
        "v2 PP1-M3: AB 判据按套件分, delta > 0 只要求 audit-engine 套件; owner_gates 5 / TASK-024 / tasks.md 等待点表同步。自检: phase-c-integrator 套件健康态 delta≈0 不再触发等待点; 两套件的回归仍逐 eval 判, 未放宽",
        "v2 PP1-M4: 按「降为 / 不被豁免 / 豁免 / 逃生口 / no_spec_unverifiable」检索 proposal 全文, 受裁定 11 影响的 9 处与 1 处论证句列进读前必看第 7 条; TASK-025 写明 §5 第 2 条同步。自检: 第 7 条的逐字改写句未变, 只加位置; 未新增措辞",
        "v2 PP1-M5: TASK-024 两套件按 descriptive 下发并在提示中逐字禁止 fetch / pull、git 写命令与 forgejo 写接口; 快照面扩到三个子模块两端、aria tag 与两仓 open PR; 远端变化按「新值对象是否已在本地」判是否本机推出; 两次快照之间本会话不调 /state-scanner、不 fetch, precheck 在第二次快照之后才跑; 上游并入挪到开 AB 会话之前 (TASK-023 末条); 不改 remote 配置。自检: 他人推送的新对象在两次快照之间不会进本地, 不会假停; 本机推出的对象本地必有, 不会漏判; 初稿把 precheck 放在快照之间、把并入放进 AB 会话, 自检时发现会误判或多一次换会话, 已改",
        "v2 PP1-M6: 新增 coord_ref_precheck, 心跳 / 认领 / release 推送与强制对齐前必跑, 写进 hard_constraints 的心跳例外; 第 14 项未授权改为停在 TASK-001; 新增等待点第 15 项。自检: 三态 (相等 / 只领先本轨心跳 / 分叉但本地只领先心跳 / 领先新 claim / 领先本轨 release / 对齐后) 已跑; 获授权的 release 在推送前单独跑 precheck, 不会被自身 release commit 挡住",
        "v2 PP1-M7: 新增 commit_attribution, TASK-001 回落与推送前、TASK-030 开 PR 前各跑一次, 清单随授权请求呈上; 新增等待点第 16 项。自检: 三态 (只有本轨 / 本轨加同步合并 / 合并了基准外分支 / 改共享指针 / 他轨 handoff) 已跑; latest.md 判 foreign 会让共享指针改动每次都请裁, 属有意的 fail-closed",
        "v2 PP1-M8: 开 AB 会话前 (TASK-023 末条) 与 TASK-025 取号前各把 aria origin/master 并入 feature (后者只在上游又前进时发生) 并重跑回归; TASK-024 开跑前断言 origin/master 是 feature 的祖先并记 AB 基线 SHA; TASK-027 第 4 步增加两个 skill 目录的 diff 判断, 非空则重跑 AB; 冲突恢复统一为 ec72175 先例; 判断清单第 19 条改写。自检: TASK-025 的 merge 在改版本文件之前, 不会与自己的版本改动冲突; TASK-027 第 5 步在 feature 已含 S3 时是无冲突合并",
        "v2 PP1-M9: 新增 crlf_guard, TASK-016 / 017 改前改后必跑, TASK-018 复核; CRLF 文件的 frontmatter 比较先去 CR。自检: 四态 (原样 / 保 CRLF 的编辑 / 插入一行 LF / 整文件转 LF) 与 description 改动态已跑; guard 须在暂存前跑, 已写明",
        "v2 PP1-M10: 新增 canonical_call 与 N4, TASK-014 / 015 照抄 canonical, 缩进不限。自检: N4 七态已跑, 缩进 4 与 6 都为真, 参数换序 (单侧或双侧)、放错区间、只写散文、少一行都为假",
        "v2 minor m1–m20 与顺带三项: 按聚合表逐条落在对应 TASK (m1 TASK-012; m2 TASK-002; m3 TASK-022; m4 TASK-015 / 016 / 018 与 N8; m5 c25; m6 读前必看第 8 条; m7 TASK-031; m8 判断清单与读前必看第 23 条; m9 TASK-019 / 020; m10 rule6_note; m11 TASK-023; m12 TASK-002; m13 TASK-019; m14 TASK-024; m15 TASK-024; m16 TASK-027 / 029; m17 TASK-030; m18 TASK-001; m19 owner_gates 2 与 TASK-001; m20 头注释与 title; 顺带: sc12_liveness 的 guard_config_hooks 与 N10、TASK-030 合并后复核计数与版本点)。自检: N8 与 N10 三态已跑; 其余为措辞或步骤补全, 未新增判据",
        "v2.1 (2026-09-18): 证据层返修 (主控 C1 核验查出) —— 只改 metadata.v2_state_runs 的 script 与 output 两块: N6 同秒心跳写出空 diff commit 被判 other、N9 同秒提交使 git log 顺序不稳定, 两处不可复现已修 (脚本钉死时钟并等过秒边界); 判据代码与生成器一字未动, 计划内容与 v2 完全相同",
        "v2.2 PP2-M1 + PP2-M2 (post_planning R2 聚合表同名键, 两席同处不同视角): TASK-001 的 claim 身份从钉死 claims/023236f2/s-86f7@1836.yaml 改为按 (本容器, 归一 track_id, active) 三元组运行时解析, 0 条与 2 条及以上各有明确处置 (多条 = 10CG/aria-plugin#202 形态, 不假设唯一); owner_gates 第 14 项的触发条件从只认 abandoned 扩到三个终态加「本容器无该轨 claim」, 并写明三态下一步相同、差别只在呈递事实; own_claim_files 改为运行时解析结果并补 fixture 反向指针 (R2 自报薄弱点 (d) 的可读性建议一并采纳); metadata.claim / container 改为记录时事实。自检: 三元组解析在真仓实跑, A.2 容器解析到已 yielded 的旧文件、当前容器解析到 claims/bfe8285d/s-73b9@1606.yaml —— 钉死写法失效是实测而非推断",
        "v2.2 PP2-M3: commit_attribution 把路径分三类 (exclusive / shared / foreign), 整条只落 shared 发布同步面的提交不再单独构成 own —— 需同一提交另有 exclusive 路径, 或提交信息带本轨 Spec: trailer; 新增 kind own-release-sync 与 shared-only, owner_gates 第 16 项同步改写; TASK-029 新增「提交必须带 Spec: trailer 并回读确认」。自检: 真仓实测 1b9734a / 5fe15b0 / c9fe08f 由 ok/[own] 翻为 stop/[shared-only], 9de3074 仍 foreign, 本轨 5d435e9 / 1b6f9ad 仍 own; 近 300 个提交里整条只落 shared 集的有 11 条, 无一带 Spec: trailer ⇒ 收紧不会把他轨发版提交放行, 代价是本轨自己的 5.7 提交漏写 trailer 会停在第 16 项 (fail-closed)",
        "v2.2 PP2-M4: baseline_rebase.standards 的零 diff 断言按 21748d4..940cb5b 实测重写并限定到四个被引文件与两个 SHA (该区间 standards 只有 content-integrity.md 与 skill-benchmark-exemption.md 变动, 后者即 SOT 升 1.1.0); scope_repos 与 TASK-030 的 standards SHA 改为「执行当时实测为准」; rule6_note 按 SOT §4.1 五字段模板重写 (decision_table_row 3 / description_changed no / scenario1 待回填 / scenario4b not_required / negctrl n/a), 原散文保留为 note, 逐字段依据写进 fields_basis, 回填与齐备性断言落在 TASK-031。自检: aria 侧 27 个 aria_zero_diff 文件在当前 gitlink 1cb3872 下复测仍全部零 diff, main_repo 七个文件同样零 diff ⇒ 失效的只有 standards 那一句",
        "v2.2 PP2-M5: 读前必看第 8 条把 checked_checkpoints 的 explicit-only 收窄从 (S4, no_spec_unverifiable) 扩到 spec_level_undetermined —— 原措辞让它落回「取已产出值」, 由实现装配时机决定, 两个字面合规的实现给不同值; 并给 SC-9(4) 的 fixture 钉 checkpoints {post_spec: convergence} 使两种读法可区分, 新增逐字断言 checked_checkpoints == ['post_spec'] (TASK-003 矩阵 / TASK-005 RED / TASK-011 验收, 落在既有格 SC-9.4-level-undetermined-bypassed, 不新增格名 ⇒ stage_cells 与 C1 证据不受影响)。自检: 反事实 = 在 P4 末尾统一装配的实现给 [] ⇒ 该断言红; 未加断言前两个实现都不红, 这正是 R2 指出的「现有 SC 与全部 stage_cells 都不会因此变红」",
        "v2.2 minor (只做返修必然连带的两条, 其余 8 条 minor 未动、等 owner 裁): revision_log 补 v2.1 与 v2.2 条目; 版本标识四处 (yaml 头注释 / metadata.title / metadata.updated / tasks.md Status 行) 由 v2 / 2026-09-17 更新为 v2.2 / 2026-09-19",
        "v2.3 R3-M1 (post_planning R3 聚合表, 四席同题): TASK-001 的基线复核条补第四组命令 —— 对 metadata.baseline_rebase.standards_files 逐个跑 git -C standards diff --shortstat 21748d4 <B.1 当时 gitlink>, 与 aria / 主仓两组同构; 新增 standards_files (七个被引文件 + 各自依赖点) 与 standards_files_basis (集合的机械求法); standards 那句的零 diff 断言由四文件扩到五文件 (补 conventions/git-commit.md) 并写明可执行落点; scope_repos 的 standards 行与 tasks.md 读前必看第 5 条、1.1 checkbox 同步。集合判据 = 本计划实际依赖其内容的 standards 文件, 不是当初被记过的文件。自检: 反事实 = 若 B.1 时 skill-benchmark-exemption.md 又被并发轨改动 (它 2026-09-17 刚被改过一次), 新加的 standards 组会给出非空 shortstat ⇒ TASK-001 红并触发逐处实读; 未加之前 31 个任务无一会看该文件一眼 (TASK-030 只核 gitlink SHA 两端可推、不核文本)",
        "v2.3 R3-M2 (两席同键): commit_attribution 的三分路径集与本轨自己的交付物足迹对齐 —— (1) 新增模块常量 TOOLING = .aria/notes/2026-09-17-199-a2-a3-tooling/ 并入 exclusive() 前缀集 (本轨 A.2/A.3 工具目录, 全仓只有本轨两个提交碰过它); (2) TASK-023 补与 TASK-029 同款的 Spec: trailer 要求与回读确认 (其两个交付物都在 shared 集, 结构上不可能含 exclusive 路径 ⇒ 不带 trailer 恒判 shared-only); (3) TASK-024 写明 ab-results 的真实归属口径 —— 含它的提交判 foreign, 且 foreign 短路优先于 exclusive, 唯一放行靠调用时传 extra (本轮初稿一度写成「与台账同提交即判 own」, 实测证伪后改正); (4) TASK-029 的 trailer 条与提交条改写, 消解「deliverables 含台账」与「整条落 shared 集」的自相矛盾 (R3 minor 638d2a0f); (5) cannot_catch 与 tasks.md 判断清单第 33 条的代价陈述按 31 个 TASK 全量分类结果重写, 不再写成「唯一代价是 TASK-029 漏写 trailer」; owner_gates 第 16 项补 TASK-023。自检: 真提交 12c870d 由 foreign 翻 own; 构造的 TASK-023 形态 (只改两个 ab-suite 文件) 无 trailer 判 shared-only、带 trailer 判 own-release-sync; 三条他轨发版同步面提交 (1b9734a / 5fe15b0 / c9fe08f) 仍 shared-only, 9de3074 与 d75e61b 仍 foreign, 四条本轨提交仍 own ⇒ 放行面没被这次放宽",
        "v2.3 R3-M3 (两席同题): rule6_note.description_changed 取 no 的机械证据面由三份 SKILL.md 补到四份 —— TASK-018 的 frontmatter 复核条与 fields_basis 逐字列名 audit-engine / phase-c-integrator / phase-b-developer / phase-a-planner, 并写明四份即本 cycle 被改 SKILL.md 的全集; TASK-017 新增一条与 TASK-015 同款的 frontmatter 比对断言 (phase-a-planner 是 LF, 实测 i/lf w/lf, 不需去 CR; phase-b-developer 是 CRLF, 先去 CR); tasks.md 的 3.5 行同步改四份。自检: 反事实 = B.2 若真改了 phase-a-planner 的 description, 改前 31 个任务无一会红 (scenario4b: not_required 与 negctrl: n/a 照常成立), 改后 TASK-017 的 sha256 比对与 TASK-018 的四份复核同时红 ⇒ Rule #6 合规链有了可证伪落点",
        "v2.3 R3-M4 (一席, 与 CLAUDE.md 多远程约束 2 冲突): 协调 ref 的推送补推后核验 —— 新增 metadata.coord_push_verify (assert / no_push_branch / measured / cannot_catch 四段), TASK-001 的心跳与重认领、TASK-031 的 release 三处改为断言 push_success == true 且 push_skipped == false 并逐个 ls-remote 与本地 rev-parse 比对 (不等时先 fetch 判本地是否为远端祖先, 多容器共写属正常); hard_constraints 第 2 条把协调 ref 纳入「推后逐 remote 核验」口径, 心跳例外句补上「免授权只覆盖发起推送, 不覆盖推成了没有」; owner_gates 第 15 项增加「推后核验不过」这一触发条件; tasks.md 判断清单第 27 条、外向动作引言、等待点第 15 行、1.1 与 5.9 checkbox 同步。自检: 2026-09-19 临时仓实测四态 —— 正常 push_success=true/push_skipped=false; 带 ARIA_COORDINATION_NO_PUSH 或 --no-push 时 false/true (reason env_var|cli_flag, 属预期不判红, 单列 no_push_branch); origin 指向不存在路径时 false/false 而 outcome 仍 refreshed、exit 仍 0 —— 正是 v2.2 只断言 outcome refreshed 会假绿的那一态; release_gate.py 三态同形。反事实 = 心跳 push 全失败时, 改前唯一断言 (期望 outcome refreshed) 照常通过, 改后 push_success 断言红",
        "v2.3 minor (只做与四题同处、不改就自相矛盾的两条, 其余 5 条 R3 minor 与 R2 未动的 8 条一律未动、等 owner 裁): 638d2a0f 随 R3-M2 一并理顺 (TASK-029 的 deliverables 与 verification 表述); revision_log 补本轮条目, 版本标识四处 (yaml 头注释 / metadata.title / metadata.container / tasks.md Status 行) 由 v2.2 更新为 v2.3, metadata.updated 仍为 2026-09-19 (同日)",
        "v2.4 R4-M1 (post_planning R4 聚合表, cr 一席; 由 v2.3 返修自身引入): TASK-001 的基线复核条改为 aria / 主仓 / standards 三组同口径 —— standards 组先 git -C standards fetch origin (本任务别处没有显式 fetch standards 的步骤; 主仓 fetch 会不会顺带递归拉到子模块对象取决于本机配置与子模块状态, 见本条末的另测), gitlink 写明取 git ls-tree HEAD standards 的第三字段; 三组各自两个端点先 git cat-file -e <端点>^{commit}, 不成立即停; 零 diff 判据由「输出为空」改为「退出码为 0 且输出为空」, 非 0 一律停。aria 组与主仓组按同口径一并改, 而不是只论证它们不受影响 (两组端点按构造已在本地, 同口径在正常路径上不误停, 另拦 SHA 抄错一类同形失败)。baseline_rebase.standards 的零 diff 记录补注 2026-09-21 复测退出码均为 0。自检: 2026-09-21 在执笔草稿目录的临时仓实跑四态 —— 真零 diff (gitlink 在本地) 两版都判零 diff, 新判据不误停; R4-M1 场景 (上游 standards 另有一提交改 git-commit.md, 本机 clone 未 fetch, 主仓 gitlink 已指向它) v2.3 做法 stdout 空串、退出 128, 按「输出为空」判零 diff (假绿), v2.4 做法 fetch 后 cat-file 通过、diff 给出 1 file changed ⇒ 红; gitlink 指向 origin 也没有的对象 ⇒ fetch 后 cat-file 仍退出 128 ⇒ 停; 把 ls-tree 整行喂给 diff ⇒ v2.3 假绿、v2.4 停。aria / 主仓两组: 真实端点 cat-file 与 merge-base --is-ancestor 均退出 0; 端点抄错一位 ⇒ diff 退出 128、stdout 空串, 与 standards 组同形。另测 (勘正审计席的一句前提): 默认的 fetch.recurseSubmodules=on-demand 下, 主仓 git fetch 会顺带把新 gitlink 对象拉进已检出的 standards 子模块; 关掉递归时不会; 子模块从未检出时 git -C standards 落到主仓上, diff 同样 stdout 空串、退出 128 —— 对象缺失态取决于本机配置与子模块状态, 故本条不以该递归为前提, 显式 fetch 并以 cat-file 与退出码判",
        "v2.4 R4-M2 (tl / cr 两席同键; v1 遗留): TASK-031 的周期 handoff 条展开为五条 —— 按模板 aria/templates/session-handoff.md 起稿, Rule #9 五字段写全 (owner-container 取 handoff_autofill.py --owner-container 的机械值, track-id 那句原文保留); 写后五字段自校验逐字照抄 phase-d-closer D.3 子步 2b 的命令 (head -8 <handoff> | grep -cE ... 须 ==5, 连同 frontmatter 内勿插注释行的口径注, 并写明不得改写成整份文件检索); latest.md 子步骤 1 (History prepend, 恒做) 与子步骤 2 (pointer 按三行判定表, 多轨 follower 不改) 各附一条可机械核对的完成断言; latest.md 的改动单独成提交, 在 owner_gates 第 13 项的授权请求里点明 (判断清单第 28 条「共享指针 `docs/handoff/latest.md` 的改动一律请裁」在 5.9 的落点)。TASK-031 的逐步对应条补 D.post (按 phase-d-closer 的触发条件执行时读配置判定, 不成立才跳过) 并把 D.3 拆到子步; tasks.md 判断清单第 25 条按 phase-d-closer 全部子步 (D.1 / D.post / D.2 三路 / D.2b / D.3 子步 1-4 / D.4) 逐一写明落点或不做的理由; 5.9 checkbox 同步。自检: 2026-09-21 在草稿目录对四份样例跑该命令 —— 只写 track-id 得 1, 五字段齐全得 5, frontmatter 内插三行注释把 updated-at 挤出窗口得 4, frontmatter 只有 track-id 而正文另有四个同名行时整份文件检索得 5 (假绿)、head -8 得 1; latest.md 两条完成断言在它的拷贝上两态实跑 (未做 prepend 时 grep -cF 新文件名得 0, 做了得 1; 判 follower 时 pointer 行改前改后相同)。改前 TASK-031 没有任何断言看得见这些形态",
        "v2.4 R4-M3 (ba 一席; v1 遗留): 二选一按代码级证据裁为 (b) —— 工作区会产生, 但按仓内 SOT 不入库。证据: 生效 skill-creator 的 SKILL.md 以散文规定工作区为与 skill 目录同级的 <skill-name>-workspace/, aggregate_benchmark.py 与 generate_review.py 只收调用方传入的目录, 不自定路径; aria/.gitignore 忽略 skills/*-workspace/ 并注明 kept locally, archived in aria-plugin-benchmarks/ab-results/ (e83be99, 2026-05-13); 主仓 .gitignore 忽略 aria-plugin-benchmarks/ab-workspace/ 并注明「结果已落 ab-results/, 无需入库」(3d3c820, 本身是一次 Rule #6 AB 结果提交); AB_TEST_OPERATIONS.md 目录用途表把 {skill}/{skill}-workspace/ 定为「随时可改，不计入基线」; 2026-04-10 之后触及 ab-results/ 的 51 个提交零 workspace 路径, 仓内 23 个被追踪的 state-scanner-workspace/ 文件全部出自 2026-04-09 的 2892c6f (提交说明自称工作区副本), 早于上述三条忽略规则; 先例 2a46d08 同样零 workspace 路径。改动: TASK-030 删掉「以及被选作结果一部分的 skill-creator 工作区目录」那半句; TASK-024 快照比较条去掉工作区例外, 改写为工作区放在已忽略位置、结果依据的逐 eval 产物复制进结果目录 (形状对齐 2a46d08)、porcelain 出现 *-workspace/ 行即停。自检: TASK-030 的参数只剩本次结果目录, 与 commit_attribution 用法注释 (只收一个结果目录) 一致; 上列证据均为 2026-09-21 在返修副本实跑 (git log --diff-filter=A、git log -S 与逐提交的路径计数), 未跑整轮 AB",
        "v2.4 R4-M4 (km 判 major、tl 判 minor, 聚合取 major; 由 v2.3 返修自身引入): standards_files 补第八条 conventions/session-handoff.md, 依赖点写 Rule #9 五字段与 track-id 的字段名和语义 (commit_attribution 的 exclusive()、TASK-031 的周期 handoff 条与写后自校验都建立在它上面); 21748d4..940cb5b 的实测值亲跑: 退出码 0 且输出为空 (零 diff) ⇒ 进零 diff 组, 零 diff 集合由五个变六个, 所有数到这组文件的地方同步改 (见 v2.4 minor 条的 cb1529a3)。自检: 同一命令对八个文件逐个复跑 —— content-integrity.md 与 skill-benchmark-exemption.md 分别为 +56 / -2 与 +21 / -3, 其余六个退出码 0 且输出为空; git diff --name-only 全仓仍只这两个文件。集合为什么漏它、今后怎么不漏, 见 standards_files_basis 的第二步",
        "v2.4 minor (只做与四题同处的四条; R4 的另四条独立 minor 与前轮待 owner 裁的 minor 一律未动 —— 唯一触及的前轮条目是 R3 minor 638d2a0f, 因 f0e78a1e 要求实证判定它的原意, 见下): f5b3afad 与 0f027861 —— standards_files_basis 改写为可独立复跑的两步求法, 新增 baseline_rebase.standards_files_derivation (command / script / output): 第一步字面计数, 输入钉在冻结快照 (standards 940cb5b、主仓 71c500e), 排除清单封闭为三族 (补上 v2.3 漏列的 README.zh.md 族); 第二步把三份计划文件引用的 Rule #N 按 CLAUDE.md 的 SOT 指针映射, 补足字面计数看不见的间接引用 (本轮据此补入 session-handoff.md)。cb1529a3 —— baseline_rebase.standards 那句粗体范围句随新集合改为「六个文件」, 前句、scope_repos 的 standards 行与 tasks.md 读前必看第 5 条的计数同步 (零 diff 组六个 / 被引全集八份)。f0e78a1e —— v2.3 条所称「638d2a0f 随 R3-M2 一并理顺 (TASK-029 的 deliverables 与 verification 表述)」不实: 当时 deliverables 十项一项未动, 只改了 verification 两条; 该条原文保留不改, 此处勘正。本轮实证判定 deliverables 该改: 去掉台账 —— 姊妹任务 TASK-025 (aria 侧版本 5 文件) 同样写台账而不列台账, TASK-029 自己的 verification 已把台账追加移到 TASK-030 第 1 条提交, owner_gates 第 16 项与 commit_attribution.cannot_catch 都把 TASK-029 的交付物当作结构上不含 exclusive 路径 —— 改后这些字面都成立; 同任务 trailer 条的 638d2a0f 括注补一句。版本标识四处 (yaml 头注释 / metadata.title / metadata.updated / tasks.md Status 行) 更新为 v2.4 / 2026-09-21; metadata.container 于 2026-09-22 补记 v2.4 的执笔记录 (owner 裁定; 主控初版派单只列了上述四处而漏列该字段, v2.3 先例维护过它), 四处的日期仍取 v2.4 主体返修完成的 2026-09-21, 未因补记改动; 判断清单补第 35–39 条 (v2.4)。自检: 派生脚本在返修副本与另一份独立克隆里各跑一次, 输出逐字节相同 (字面 10 族 → 排除 3 族 → 7 份; Rule #N 映射补出 1 份 → 8 份); 用 commit_attribution 自带的 SHARED 集按 deliverables 字面分类, 主仓侧交付物全落 SHARED 的任务由 v2.3 的一个 (TASK-023) 变为 v2.4 的两个 (TASK-023 / TASK-029), 与 cannot_catch 的「共两组」及 owner_gates 第 16 项的措辞一致",
        "v2.5 R5-M1 (post_planning R5 聚合表, tl 判 major、cr 判 minor, 聚合取 major; 由 v2.4 返修 R4-M2 自身引入): owner_gates 原第 13 项拆为 13a (D.2b release_gate 的协调 ref 推送, 单独一项, release 之前请) 与 13b (Phase D 提交双推, 在 latest.md 的单独提交产生之后请, 请求附其 diff 并注明 History 节来历); TASK-031 的 claim 条、latest.md 单独提交条与末条双推改指 13a / 13b; latest.md 单独提交条的理由改写 (聚合对执笔自报薄弱点第 4 条: 原理由依赖 TASK-031 不跑的 commit_attribution), latest.md 子步骤 1 条补 History 节来历 (薄弱点第 3 条: 16b5bf1 加入、合并提交 ecb6296 丢失, 两个父提交逐个实测); tasks.md 等待点表第 13 行拆两行, 判断清单第 25 / 38 条改指 13b、5.9 行同步, 新增第 40 条写明拆分与 owner 2026-09-17「release 逐项授权」原意的关系以及「13a 已批、13b 未批」的中间态。自检: 按 TASK-031 的 verification 顺序核请求时点 —— v2.4 的原第 13 项在第 8 条 (release 之前) 就须请, 要求附 diff 的句子在第 14 条, latest.md 提交也在第 14 条; v2.5 的 13a 在第 8 条只含 release, 13b 在第 15 条请、晚于第 14 条的 latest.md 提交; 全文「第 13 项」「等待点 13」引用脚本检索逐处改完, 只剩 revision_log 的 v2.4 历史条目 (不改)",
        "v2.5 R5-M2 (tl 判 major、cr 判 minor, 聚合取 major; v1 遗留): hard_constraints 第 4 条补会话入口 claim 核验 —— Phase B–D 每个会话第一步按 TASK-001 做三元组解析 → 协调 ref 前置检查 → 心跳并按 coord_push_verify 核验; 对齐后 0 条 active 或 claim_not_found ⇒ 第 14 项 (挂载从 TASK-001 扩到任意会话与 TASK-031 的 release, 停点改为当前任务, --phase 取当时阶段), 前置检查或推后核验不过 ⇒ 第 15 项 (措辞同步); 例外为 TASK-024 的 AB 会话 (前置条改为由其前一个普通会话补一次核验过的心跳, 末条改为其后第一个普通会话先做入口核验) 与 TASK-031 release 之后的会话。TASK-001 心跳条补一步 (交互检查查出, 席位修法里没有): 心跳前把本地协调 ref 强制对齐到 origin 并在对齐后重跑解析, claim 身份条的 0 条分流以对齐后的解析为准 —— 心跳不自己 fetch, 本地落后时推送非快进必失败, 被 sweep 的 claim 在落后的本地值上仍显示 active。TASK-031 的 claim 条单列 release 遇 claim_not_found (benign, 退出 0, 不推) 的处置: 呈 owner, 可先按第 14 项补认领再 release, 不落第 15 项。tasks.md 等待点表第 14 / 15 行、表前说明、判断清单第 11 条加注、新增第 41 条。v2_state_runs 新增 N11。自检 (N11, 临时仓实跑两遍逐字节相同): 本地落后时按 v2.4 顺序心跳 push_success=False, 按 v2.5 顺序 (前置检查退出 0、强制对齐、重解析) 为 True 且 ls-remote 与本地相等; claim 被 sweep 后按 v2.4 顺序在旧值上仍解析到 active、心跳 push_success=False, 按 v2.5 顺序对齐后解析到 abandoned (0 条 active); 其后心跳 outcome=error reason=claim_not_found, release 得 released.error=claim_not_found / benign=True / push_success=None, 均退出 0",
        "v2.5 R5-M3 (tl 一席; v1 遗留, 前四轮零提及): TASK-030 在 C.2.4 条之后新增 C.2.4.5 条 —— 本仓未配置 phase_c_integrator.submodule_gate ⇒ 缺省 block (已启用); 其自动触发挂在 branch-manager merge action 上, 主仓 PR 走 Forgejo 合并不经过它 ⇒ 由主控在 C.2.4 green 之后、Forgejo 合并之前在主仓根、HEAD 为 PR head 时显式跑 ARIA_SUBMODULE_GATE_MODE=<执行时配置值, 缺省 block> ARIA_PR_NUMBER=<PR 号> bash aria/skills/phase-c-integrator/scripts/submodule_gate.sh; 放行 = 退出 0 且逐子模块结论行齐 (aria 须为 GATE 加 PASS forward bump); 退出 1 / 2 / 3 / 4 / 64 / 65 或缺结论行 ⇒ 新立 owner_gates 第 17 项 (override 只由 owner 决定)。tasks.md 5.8 行、范围边界表、等待点表第 17 行与判断清单第 42 条同步。依据全部实读 aria 1cb3872 的 phase-c-integrator/SKILL.md C.2.4.5 段与 scripts/submodule_gate.sh: 退出码表; 模式只读环境变量 ARIA_SUBMODULE_GATE_MODE、缺省 block (脚本头注释写的「读 .aria/config.json、缺省 warn」与代码不符, 以代码为准); 无 .gitmodules 时打印 trivially passes 并退出 0; 遥测写被 aria/.gitignore 忽略的 aria/metrics/*.jsonl。自检: 在临时超级仓实跑该脚本 —— 子模块指针前进 ⇒ 退出 0 且有 GATE 与 PASS 行; 回退 ⇒ 退出 1 且 BLOCK; 在子模块目录里跑 ⇒ 退出 0 且只有 trivially passes 一行 (只看退出码会放行, 新判据因缺结论行而停); 不在仓内 ⇒ 退出 65",
        "v2.5 R5-M4 (qa / km 判 major, tl / cr 判 minor, 聚合取 major; 已知项 B 升级) 与 1453c41f (tl minor, 同一行): TASK-027 第 4 步 (b) 改为与 TASK-001 同口径 —— A 与 S3 先 cat-file -e, diff 退出非 0 即停, 退出 0 且有输出才重跑 TASK-024; 补 (c) feature 一侧 —— W、feature 分支现值与 TASK-024 结果提交先 cat-file -e, 再比 aria 两个 skill 目录 (W..feature 分支) 与主仓 ab-suite/audit-engine.json (结果提交..工作树; 比到工作树是对席位写法的改进: 主仓侧没有先提交 TASK-026 改动的一步), 非空时逐 hunk 按 Rule #6 判据表分类 (描述性 ⇒ substitute, TASK-031 勾选时写进 rule6_note 的 note; 处方性或拿不准 ⇒ 按第 4 项重跑 TASK-024); TASK-024 末条补记结果提交 SHA; owner_gates 第 6 项补两类触发, tasks.md 等待点表第 6 行、5.5 行、判断清单第 19 条加注与新增第 43 条同步。sc12_liveness.guard_config_hooks 钉在主仓根 (git -C <主仓根> grep …; echo rc=${PIPESTATUS[0]}), 判据改为末行 rc 为 0 或 1 且其前无输出; blind_spots、TASK-021 重写 a 条 (SC-12 三条改为各放子 shell)、TASK-031 的 SC-12 liveness 条与 tasks.md 4.3 行同步; 交互检查另查出 TASK-027 第 7 步复跑 L2 前不跑 guard, 已补。v2_state_runs 的 N10 按新 guard 重写并加两态。自检 (N10): 基线 rc=0 无命中, 放行; config / hooks 含符号各 1 行, 停; 从 aria/skills/audit-engine/tests 跑且 config 含符号 —— v2.4 命令 0 行 (按旧读法放行), v2.5 命令 rc=0 且 1 行 (停); <主仓根> 不是仓 —— v2.4 命令 0 行 (放行), v2.5 命令 rc=128 (停); 4(b) 的抄错一位与 4(c) 的 feature 一侧处方改动另有临时仓反事实",
        "v2.5 R5-M5 (cr 一席; 由 v2.4 返修 R4-M3 的选址自身引入): 二选一按「新增交互更少」裁为 (a) —— skill-creator 工作区只放主仓 aria-plugin-benchmarks/ab-workspace/<本次结果目录名>/, 不再用 aria 侧 skills/*-workspace/。证据: 生效 skill-creator (ea0a38e1d671) 的 SKILL.md:167 只以散文给默认落点, :186 的快照写法相对于工作区, aggregate_benchmark.py (benchmark_dir) 与 generate_review.py (workspace) 都只收调用方传入的目录 ⇒ 选址可由调用方指定; 先例 3d3c820 (把 ab-workspace/ 加进主仓 .gitignore) 与 v1.69.0 那次 AB 的旧版快照落在 ab-workspace/…/skill-snapshot; 主仓 custom checks 里唯一的递归扫描 (no-unresolved-version-placeholder) 只扫 aria/, SC-13 只扫 aria/skills/, 归档门的产物路径抽取只认 ab-results / ab-suite, 都不碰 ab-workspace/。TASK-024 快照条补 find aria/skills -maxdepth 1 -name '*-workspace' 与每条快照命令的退出码, 比较条改写 (选址、两次 find 之差、新 SHA 在它所属的仓里 cat-file); TASK-018 的递归检索条注明工作区不得放在 aria/skills/ 下; 判断清单第 35 条加注、新增第 44 条。(b) 不选: 它要多一个删除动作与至少两处断言, 且本机主仓已有早年 AB 留下的被忽略工作区 aria/skills/issue-triage-workspace/ (2026-09-22 实测), 「断言无 *-workspace 目录」会误停。自检 (临时副本): 工作区放 aria 侧时 porcelain 0 行、check-ignore 命中 .gitignore:7、SC-13 检索由 4 处变 5 处, 两次 find 之差非空 ⇒ 停; 放主仓 ab-workspace/ 时 porcelain 0 行、SC-13 仍 4 处、no-unresolved-version-placeholder 退出 0",
        "v2.5 minor (只做两条同处 minor; R5 另三条 minor 34b92188 / 27cee280 / ae4753f5、R4 另四条独立 minor 与前轮未动 minor、v2.4 执笔九条请裁里本轮未覆盖的项一律未动): 118d1d64 —— TASK-031 的 deliverables 补 docs/handoff/latest.md (与 v2.4 对 TASK-029 采用的「只列本任务提交的文件」同口径); 1453c41f 见 R5-M4 条",
        "v2.5「空输出即通过」同族扫描 (owner 2026-09-22 点名的两项动作之一; 扫描面 = tasks.md 全文 + tasks[*].verification / notes + metadata 中除 revision_log 与两份三态脚本外的全部字符串, 另对 baseline_rebase 四组 48 条路径逐条 cat-file -e; 逐条清单与处置由 v2.5 执笔报告呈主控): hard_constraints 新增第 14 条判据命令的通用口径; 已知成员 ac2e8dcb (TASK-031 周期 handoff 起稿条: autofill 退出非 0 或输出为空 ⇒ 按 SOT 回退手填; 自校验条另加值非空检查) 与 11c3a29f (aria_shifted 第 6 条拆为三条, TASK-001 基线复核补「路径至少在一端存在」) 已处置; 另改: 各处 porcelain 补退出码 (TASK-001 / 013 / 018 / 027 / 030)、ls-remote --tags 三处与主仓两处 fetch 补退出码、TASK-001 的三元组解析看 ls-tree / show 退出码、TASK-018 的 SC-13 计数与递归检索补退出码语义、TASK-015 / 017 / 018 与 crlf_guard.frontmatter_rule 的 frontmatter 比较补两侧非空且含 description: 的断言、TASK-021 与 TASK-027 第 7 步的 Ran 数不得少于基线、TASK-023 的计数管道看首段退出码、TASK-024 快照命令看退出码、TASK-025 取号看 ls-remote 退出码且五处须等于新号、TASK-026 检查器与 §4.5 命令的退出码语义与导出文件非空、TASK-027 第 3 步集合非空与第 5 步 rev-parse 退出码、第 7 步与 TASK-029 的 no-unresolved-version-placeholder 先确认当前目录 (该 command 以 ! 反转 grep 退出码); coord_ref_precheck 的 rev-parse FETCH_HEAD 与 rev-list、commit_attribution 的 git log 失败改为退出 2 (owner_gates 第 16 项注明退出 2 = 没跑成), crlf_guard 的 run() 改为 check=True。v2_state_runs 的 N9 加一态 (基准 ref 不存在 ⇒ 退出 2); N4 / C1 / N6 / N7 / N8 与 N9 原 13 态的输出与 v2.4 逐字节相同; a2_state_runs 的输出与 v2.4 逐字节相同",
        "v2.5 版本标识与记录: 版本标识四处 (yaml 头注释 / metadata.title / metadata.updated / tasks.md Status 行) 由 v2.4 / 2026-09-21 改为 v2.5 / 2026-09-22; metadata.container 补 v2.5 执笔记录 (owner 2026-09-22 裁定由 v2.4 的执笔实例保留全部上下文续写, 同一实例; 按 R1 判据, R5 五题 Major 中 R5-M1 与 R5-M5 两题由 v2.4 返修自身引入, 2/5 未过半)。等待点编号因拆分而变: 13 → 13a / 13b, 新增 17; 全文「第 N 项」「等待点 N」引用用脚本检索并逐处改到一致 (revision_log 的历史条目不改)。本轮自作的流程判断登记为判断清单第 40–45 条 (v2.5)",
        "v2.6 354faf33 (post_planning R6 已知项 A; km 一席立案、另两席同判, owner 2026-09-24 定级 minor 并指定三席的最小修法, km 另提的「13b 之前重跑 commit_attribution」本轮不采): TASK-031 起稿条删去不可达句「写成别的或漏写 ⇒ 判 foreign, 停在 owner_gates 第 16 项」—— commit_attribution 的调用点只有 TASK-001 与 TASK-030, 本任务自身不跑它 (v2.5 已在 latest.md 单独成提交条写明), 那个停点在 5.9 不可达; 改写为指向写后五字段自校验条新增的取值断言, commit_attribution.cannot_catch 同步注明 5.9 周期 handoff 的 track-id 取值改由该断言守。自校验条新增断言: head -8 <handoff> | grep -cxF 'track-id: pre-merge-completeness-gate-change-scope' 须为 1, 不为 1 ⇒ 改对后重验, 不得带错值进 latest.md 两子步。tasks.md 5.9 行的同一不可达理由 (原写「否则该提交判他轨」) 一并改为断言口径, 判断清单第 33 条加链接注。反事实 (执笔报告 CF-1): 把 track-id 写成 pre-merge-completeness-gate-change-scopes, E1 的字段在不在检查得 5、v2.5 的值非空检查也得 5, 新断言得 0 ⇒ 只有它拦得住",
        "v2.6 6ad0a84b (tl 一席 minor; 三组错位里两组由 v2.5 返修自身引入): 条目序号引用一律改锚点式, 共 10 处 —— TASK-001 心跳条与 hard_constraints 第 4 条的「TASK-024 末条」(实际要指的是 TASK-024 第 12 条「结束后先取第二次快照」, 末条是第 13 条的结果提交) 改「TASK-024 的『结束后先取第二次快照』条」; TASK-024 AB 基线条与 owner_gates 第 6 项的「TASK-023 末条」(实为第 5 条「开 AB 会话之前」, 末条是第 7 条的结果提交) 改锚点式; metadata.claim 与 coord_ref_precheck.own_claim_files 的「TASK-001 第 1 条」(第 1 条是入口前置, claim 三元组解析在第 2 条) 改「TASK-001 的 claim 身份条」; TASK-024 对齐条的「完成上条比较」改指本任务的快照比较条 (相邻上一条是 README / RESULT 三条命令); TASK-029 trailer 条的「按下一条」与提交条的「与上一条」改指具体条 (两者相隔一条, 中间是 custom checks 条); sc12_liveness.guard_config_hooks 从 TASK-021 外部用「TASK-021 的上一条」改指「SC-12 三条那一条」。同族扫描 (逐条清单见执笔报告): 扫描面 = tasks.md 全文 + 整份 yaml 树 (含 revision_log 与两份冻结脚本, 不留视野外), 一条主正则按特指到泛指排序、finditer 逐处唯一命中, v2.5 上共 299 处; 判定闭合 (无未分类行): 正确 139 / 按上下文逐条核过 28 / 本条自身编号 8 / 泛指非引用 2 / 计划外文档编号 22 / 历史编号 (原…) 11 / revision_log 历史条目 79 / 本轮改 10。revision_log 里另有两处「TASK-023 末条」属历史条目, 按不改写历史不动",
        "v2.6 2c2e8931 (tl 一席 minor; 由 v2.5 返修 R5-M2 自身引入 —— 强制对齐当时只写进了会话入口心跳): hard_constraints 第 4 条升为通则 —— 任何会写或推协调 ref 的动作 (心跳、获授权的认领与重新认领、release) 在前置检查退出 0 之后、动手写或推之前, 先 git fetch origin +refs/aria/coordination:refs/aria/coordination (须退出 0) 再重跑三元组解析; TASK-031 的 claim (D.2b) 条按「前置检查 → 强制对齐 → 重解析 (0 条 active 直接走 claim_not_found 分支) → release_gate」落地, TASK-001 的重新认领段同补; coord_ref_precheck.code 的注释由「退出 0 = 可推送」改为「可强制对齐, 对齐后才可推送」; tasks.md 判断清单第 27 条、等待点表前说明、1.1 与 5.9 两个 checkbox 行同步。证据 = 新增 v2_state_runs 的 N12 (同一分叉态下两种顺序各跑一次): 照 v2.5 顺序直接 release 得 exit 0 / fetch_success false / released.success true / push_success false / 远端不等于本地, 之后再跑前置检查得退出 1 (kinds own-heartbeat 与 other) —— 即写下一个推不出去的本地 release, 与 owner_gates 第 13a 项「不写仅本地的 release」相反, 并把下一个会话卡在第 15 项; 先强制对齐再 release 得 push_success true 且远端等于本地。分叉态本身在 N6 早有实测 (remote advanced + local own heartbeat ⇒ 前置检查退出 0), 即前置检查退出 0 不蕴含「可直接推」。同族扫描 (逐条清单见执笔报告): 先按代码定出写入路径的封闭集 (lib/claim_lifecycle.py 与 lib/gc.py 是 write_claim / apply_tree_edits 的唯一调用方, 二者只经 phase1_gate.py 与 release_gate.py 到达) 共 8 条路径, 再扫计划文本得 44 个候选单元并逐条判定 (无未分类行): 执行落点 7 处, 其中本轮补对齐 4 处 (TASK-031 release、TASK-001 重新认领、tasks.md 1.1 与 5.9 两行), 其余为授权条、说明性或明令不执行 (sweep / gc 本计划不做)",
        "v2.6 749f8d15 (cr 一席 minor; 由 v2.5 返修 R5-M3 自身引入): C.2.4.5 的 override 描述与调用时机对齐 —— 闸的 check_override_trailer 读的是运行时 HEAD 的提交信息 (submodule_gate.sh:101 的 git log -1 --format=%B HEAD), 而本计划让它跑在 Forgejo 合并之前、HEAD 为 PR head 时, 写进合并提交的 Submodule-Rollback: trailer 闸根本看不见; TASK-030 该条与 owner_gates 第 17 项都改为: trailer 须落在 PR head 那个提交上, 或改用 PR 标签 submodule-rollback-approved (闸经 forgejo GET 读标签, 需要 ARIA_PR_NUMBER, API 失败按无标签处置, 方向 fail-closed); 两个修法的代价一并写明 —— 改 PR head 的提交信息等于改写并强推已推送的 feature 分支, 与 owner_gates 第 8 项「不 force、不改写历史」冲突, 须 owner 一并裁准, 且分支 SHA 变了之后 C.2.4、本闸与 TASK-030 的提交范围核验都要重做, 走标签则不动提交。同时补上 owner 裁了 override 之后重跑的放行判据: 退出 0, 且被 override 的子模块有 GATE: 行与其后的 ALLOW: … overridden by per-PR marker 行 (脚本 :263 先打 GATE:, :297 打 ALLOW: 后 continue, 不置退出码), 其余子模块照原判据 —— v2.5 的放行判据只认 PASS: 与 OK:, owner 裁了 override 也仍判「缺结论行」而停, 无合法下一步。本轮在临时仓实跑三臂 (执笔报告 CF-2): 无 trailer ⇒ 退出 1 BLOCK; trailer 只写在合并提交上而 HEAD 仍是 PR head ⇒ 仍退出 1 BLOCK; trailer 落在 PR head 提交上 ⇒ 退出 0 并打印 GATE: 与 ALLOW: 行、没有 PASS: 行。tasks.md 等待点表第 17 行与 5.8 行同步, 判断清单第 42 条加链接注",
        "v2.6 29325b2c (cr 一席 minor; v2.5「空输出即通过」同族扫描的漏网形态): custom checks 一律以输出首行判、不以退出码判 —— plugin-version-arch-docs-match 读不到 aria/.claude-plugin/plugin.json 时打印 ##SKIP## 并仍退出 0 (.aria/state-checks.yaml 该条 command 的第二行), collectors/custom_checks.py 把「退出 0 且首行 ##SKIP##」映射为 skip, 既不算 pass 也不算 fail, 只看退出码就会把没跑成当成过。hard_constraints 第 14 条 (3) 的已知形态清单补入该形态并写明首行口径; TASK-029 的 custom checks 条逐条写明期望首行 (前四条须 OK, no-unresolved-version-placeholder 通过时无输出, plugin-cache-currency 在 owner 更新缓存前首行 STALE 属预期), 首行为 ##SKIP## 一律算没跑成; 该条开头 v2.5 原把五条并列写作「为 OK」, 与第五条通过时无输出不符, 一并改为「五条须通过 (逐条判据见本条下半)」; tasks.md 5.7 行同步, 判断清单第 45 条加链接注。2026-09-24 副本实测: 六条在主仓根分别为 OK / OK / OK / OK / 无输出 / OK 且退出码都是 0; 换到 aria/skills/audit-engine/tests 起跑, plugin-version-arch-docs-match 变 ##SKIP## 且仍退出 0、no-unresolved-version-placeholder 仍无输出且退出 0, 其余四条退出 1 或 2。同族扫描 (逐条清单见执笔报告): 16 条 custom checks 逐条静态看哨兵串与「##SKIP## 配退出 0」形态 (只有这一条有), 计划点名的六条再逐条实跑两个目录; 另扫计划点名的 7 个机械探针, 其中三个有「退出 0 却没跑成」形态 (submodule_gate.sh 的 trivially passes 与 directory absent、run_all_tests.sh 的整套 SKIP、handoff_autofill.py 的空串; 前两者已由 v2.5 与 TASK-003 / TASK-007 处置, 第三者退出 1 不属本形态), 其余四个命中数为 0",
        "v2.6 版本标识与记录: 版本标识四处 (yaml 头注释 / metadata.title / metadata.updated / tasks.md Status 行) 由 v2.5 / 2026-09-22 改为 v2.6 / 2026-09-24; metadata.container 补 v2.6 执笔记录 (同一执笔实例续写; post_planning R6 按主控定级 0 Critical / 0 Major / 5 minor, R1 的换人判据只看 Major 里由上一轮返修引入的占比, Major 为 0 时不适用 —— 5 条 minor 里有 3 条长在 v2.5 新建机制的接缝上, 已在各条注明来历)。本轮自作的流程判断登记为判断清单第 46–50 条 (v2.6), 旧条目只加链接注不改原意 (第 33 / 41 / 42 / 45 条)。等待点编号不变 (仍 1–12 / 13a / 13b / 14–17), 31 个 TASK 与各任务条目数不变, 故全文既有的「第 N 条 / 第 N 项」引用不因本轮增删而移位 (机器复核见执笔报告的序号引用清单)。v2_state_runs 新增 N12, 其余 N4 / C1 / N6 / N7 / N8 / N9 / N10 / N11 的输出与 v2.5 逐字节相同; a2_state_runs 的输出与 v2.5 逐字节相同",
    ],
    "v2_state_runs": {
        "what": "v2 新增的 N4 / C1 (cell_status) / N6 (coord_ref_precheck) / N7 (crlf_guard) / N8 / N9 (commit_attribution) / N10 (guard_config_hooks), 以及 v2.5 新增的 N11 (会话入口 claim 核验: 落后的本地协调 ref、强制对齐、claim 被 sweep 成 abandoned 后的心跳与 release), 在同一 scratch 主仓副本与临时仓上实跑; 代码取自本文件对应键, 副本外零写入 (N6 与 N11 的远端是临时裸仓)。v2.5 另改 N9 (加一态: 基准 ref 不存在 ⇒ 退出 2) 与 N10 (按钉在主仓根、看退出码的新 guard 重写, 加两态并并列 v2.4 命令的读法)。v2.6 新增 N12 (协调 ref 与 origin 分叉时的 release: 照 v2.5 写法直接 release vs 先强制对齐再 release), 同样在临时仓里跑",
        "command": "python3 -B a2_v2_checks.py <scratch 主仓副本根> <scratch 工作目录> <本文件>  (脚本全文见 script; 下方 output 由该命令重生成, 未手改)",
        "script": script2_text,
        "output": run_output2,
    },
}

header = ("# Generated by task-planner (A.3) — pre-merge-completeness-gate-change-scope, v2.6 (2026-09-24, post_planning R6 rework)\n"
          "# Dual-layer: tasks.md (coarse, 31 checkboxes) + this file (fine, 31 tasks). `tasks:` stays the LAST\n"
          "# top-level key: the archive gate's line parser lets the last task block run to EOF.\n")
doc = yaml.dump({"metadata": metadata}, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=100000)
doc += yaml.dump({"tasks": tasks}, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=100000)
open(OUT, "w", encoding="utf-8").write(header + doc)
print(f"tasks={len(tasks)} hours={hours_low:g}-{hours_high:g} agents={agents}")
