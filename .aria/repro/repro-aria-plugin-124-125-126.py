#!/usr/bin/env python3
"""aria-plugin v1.65.0 path_coverage.py — 三个缺陷的自包含复现。

用法:
    python3 repro_122.py /path/to/aria/skills/phase-c-integrator/scripts/path_coverage.py

零依赖 (stdlib only)。每个用例自建临时 git 仓, 不触碰任何现有仓库。
"""
import importlib.util
import os
import subprocess
import sys
import tempfile
from unittest import mock

if len(sys.argv) < 2:
    sys.exit(__doc__)

spec = importlib.util.spec_from_file_location("pc", sys.argv[1])
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)


def sh(args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


WF = """name: t
on:
  pull_request:
    paths:
      - 'skills/**'
jobs:
  a:
    runs-on: ubuntu-latest
    steps: [{run: echo hi}]
"""

WF_SAME_INDENT = """name: t
on:
  pull_request:
    paths:
    - 'skills/**'
jobs:
  a:
    runs-on: ubuntu-latest
    steps: [{run: echo hi}]
"""


def build(workflow_text, changed_file):
    d = tempfile.mkdtemp(prefix="pc-repro-")
    sh(["git", "init", "-q", "-b", "main"], d)
    sh(["git", "config", "user.email", "t@t"], d)
    sh(["git", "config", "user.name", "t"], d)
    sh(["git", "config", "core.quotePath", "true"], d)  # git 默认值
    os.makedirs(f"{d}/.forgejo/workflows", exist_ok=True)
    with open(f"{d}/.forgejo/workflows/w.yml", "w") as fh:
        fh.write(workflow_text)
    sh(["git", "add", "-A"], d)
    sh(["git", "commit", "-qm", "base"], d)
    sh(["git", "checkout", "-qb", "pr"], d)
    target = os.path.join(d, changed_file)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w") as fh:
        fh.write("x")
    sh(["git", "add", "-A"], d)
    sh(["git", "commit", "-qm", "change"], d)
    return d


fails = 0

# ---------------------------------------------------------------- 缺陷 1
print("=" * 72)
print("缺陷 1 [fail-OPEN] 非 ASCII 路径 → 误判 not_applicable (闸门跳过 PR CI)")
print("=" * 72)
for label, fname, expect in [
    ("ASCII   ", "skills/issue-triage/x.py", "covered"),
    ("非 ASCII", "skills/测试/x.py", "covered"),
]:
    d = build(WF, fname)
    raw = sh(["git", "diff", "--name-only", "--no-renames", "main...pr"], d).stdout.strip()
    r = pc.evaluate_path_coverage("main", "pr", d)
    ok = r["decision"] == expect
    fails += 0 if ok else 1
    print(f"  {label} 变更 {fname}")
    print(f"     git diff 输出 : {raw}")
    print(f"     decision      : {r['decision']}  (期望 {expect})  {'OK' if ok else '<<< BUG'}")
print("  根因: git diff 缺 -z, core.quotePath(默认 true) 八进制转义路径 ⇒ 与 glob 恒不匹配")

# ---------------------------------------------------------------- 缺陷 2
print()
print("=" * 72)
print("缺陷 2 [恒 wait] 同缩进块序列的 paths: 解析不出 ⇒ #122 对该类仓未生效")
print("=" * 72)
d = build(WF_SAME_INDENT, "docs/a.md")
r = pc.evaluate_path_coverage("main", "pr", d)
ok = r["decision"] == "not_applicable"
fails += 0 if ok else 1
print("  workflow 用同缩进块序列 (合法 YAML):")
print("      paths:")
print("      - 'skills/**'")
print("  变更 docs/a.md (明显不命中 skills/**)")
print(f"     decision : {r['decision']}  reason: {r['reason']}")
print(f"     期望 not_applicable  {'OK' if ok else '<<< BUG — 恒 wait 复发'}")
print("  根因: _extract_paths 用 `_indent_of(nraw) <= base_ind: break`,")
print("        同缩进序列项被判出块 ⇒ items 空 ⇒ uncertain ⇒ covered")

# ---------------------------------------------------------------- 缺陷 3
print()
print("=" * 72)
print("缺陷 3 [误诊] 评估器内部异常上报为 git-diff-failed")
print("=" * 72)
d = build(WF, "docs/a.md")
with mock.patch.object(pc, "_find_workflow_files", side_effect=RuntimeError("boom in parser")):
    r = pc.evaluate_path_coverage("main", "pr", d)
ok = not r["reason"].startswith("git-diff-failed")
fails += 0 if ok else 1
print("  注入 parser 内部 RuntimeError:")
print(f"     reason : {r['reason']}")
print(f"     {'OK' if ok else '<<< BUG — 真因是 parser, 上报却指向 git/main ref'}")

print()
print("=" * 72)
print(f"复现到的缺陷数: {fails} / 3")
sys.exit(1 if fails else 0)
