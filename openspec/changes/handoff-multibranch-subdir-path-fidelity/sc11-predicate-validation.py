#!/usr/bin/env python3
"""SC-11 定位谓词的三态验证 (10CG/Aria#195 post_planning R1 rework, 2026-09-15).

用法 (仓库根目录执行, 只读; 副本建在临时目录, 结束后删除):
    python3 -B openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py [aria_state_scanner_dir]

默认读取 aria/skills/state-scanner 下 5 个文件, 在临时目录各复制出五种状态:
  base               原样 (谓词应全假)
  target             模拟正确实现 (应全真)
  bad_codeonly       只改代码不改文档 (应全假)
  bad_changelog_only 只在 schema Change history 表加一行 (除 (g) 外应全假; (g) 的检查对象就是该行)
  bad_partial        正确实现但漏改 Fail-soft 形状 / TrackEntry 公式 / 两处 four-level /
                     dedupe docstring 键序句 / 两个 writer docstring (对应谓词应为假)
模拟改动按 1cb3872 (v1.73.3) 的原文逐字替换; 原文不匹配时断言失败, 说明基线已变, 需重写模拟。
谓词原文与 detailed-tasks.yaml metadata.sc11_baseline_predicates 逐字一致。
"""
import pathlib, subprocess, sys, shutil, tempfile
C = "scripts/collectors/handoff_multibranch.py"; W = "scripts/writers/latest_md_writer.py"
S = "references/state-snapshot-schema.md"; P = "references/phase-1-collectors.md"; L = "references/layer-l-integration.md"

def rep(root, rel, old, new, count=1):
    p = root / rel; t = p.read_text(encoding="utf-8")
    n = t.count(old)
    assert n >= 1, (rel, old[:60])
    t = t.replace(old, new) if count == 0 else t.replace(old, new, count)
    p.write_text(t, encoding="utf-8")

def code_changes(r):
    rep(r, C, 'return (bucket, dt, row.get("filename") or "", row.get("branch") or "")',
        'filename = row.get("filename") or ""\n    rel = row.get("rel_path") or filename\n    return (bucket, dt, filename, row.get("branch") or "", (rel == filename, rel))')
    rep(r, W, '        content = _render_pointer(active_tracks[0], now)\n        action = "pointer"',
        '        content, degraded_reason = _render_pointer(active_tracks[0], now)\n        action = "pointer"')
    rep(r, W, '    n_active = len(active_tracks)\n', '    n_active = len(active_tracks)\n    degraded_reason = None\n')
    rep(r, W, '        "content_lines": content_lines,\n    }', '        "content_lines": content_lines,\n        "degraded_reason": degraded_reason,\n    }')

def collector_docs(r, skip=()):
    if "c" not in skip: rep(r, C, "Returns only the basename (not the full path) for each file so callers", "Returns each file's path relative to ``docs/handoff/`` so callers")
    if "i1" not in skip: rep(r, C, "legacy:<branch>:<filename>", "legacy:<branch>:<rel_path>", count=0)
    if "j1" not in skip: rep(r, C, 'sort key: four levels, all-comparable,', 'sort key: five levels (5th = ``rel_path``, top-level first), all-comparable,')
    if "j3" not in skip:
        rep(r, C, "# Tie-break, finalized (round 3): the sort key is FOUR levels, all", "# Tie-break, finalized (round 4, 10CG/Aria#195): the sort key is FIVE levels, all")
        rep(r, C, "# ``(parse_ok, parsed_updated_at, filename, branch)``.", "# ``(parse_ok, parsed_updated_at, filename, branch, (rel_path == filename, rel_path))``.")
    if "j4a" not in skip: rep(r, C, "# greatest under the four-level key below wins", "# greatest under the five-level key below wins")
    if "j5a" not in skip: rep(r, C, "  dictionary-max branch (round 3, finding [M1]; fully deterministic,", "  dictionary-max branch, then top-level ``rel_path`` first (round 3 [M1] / round 4; fully deterministic,")
    if "j5b" not in skip: rep(r, C, "level, ``branch`` (dictionary-max), closing the remaining non-determinism on", "level, ``branch`` (dictionary-max; 10CG/Aria#195 later adds a ``rel_path`` 5th level), closing the remaining non-determinism on")
    if "j5c" not in skip: rep(r, C, "    dictionary-max branch (see module comment above ``_dedupe_sort_key``).", "    dictionary-max branch, then top-level ``rel_path`` first (see module comment above ``_dedupe_sort_key``).")
    if "j5d" not in skip: rep(r, C, "# — newest updated_at wins (filename then branch dictionary-max", "# — newest updated_at wins (filename, branch dictionary-max, then rel_path")

def writer_docs(r, skip=()):
    if "l1a" not in skip: rep(r, W, '        "content_lines": int,          # number of lines written\n    }', '        "content_lines": int,          # number of lines written\n        "degraded_reason": None | "missing_filename" | "target_in_subdir",\n    }')
    if "l1b" not in skip: rep(r, W, '            ``content_lines`` — number of newline-separated lines written', '            ``content_lines`` — number of newline-separated lines written\n            ``degraded_reason`` — None | "missing_filename" | "target_in_subdir"')
    if "k1" not in skip: rep(r, W, '    determined from the track dict (edge case: legacy track missing filename).\n    """', '    determined from the track dict (edge case: legacy track missing filename),\n    or when the file lives in a subdirectory (reason ``target_in_subdir``).\n    """')
    if "k2" not in skip: rep(r, W, '    """Fallback when single active track has no filename."""', '    """Fallback when the pointer cannot be written: missing filename or ``target_in_subdir``."""')

def schema_docs(r, skip=()):
    if "a1" not in skip: rep(r, S, "  legacy_count: int               # tracks that fell back to legacy (no frontmatter)\n", "  legacy_count: int               # tracks with no frontmatter (git-show failures are NOT counted)\n  unreadable_count: int           # rows enumerated but unreadable (git show failed); ALWAYS present, default 0\n")
    if "a2" not in skip: rep(r, S, '"legacy_count": 0, "collision": {"kind": "none", "groups": []}, "errors": [...]}', '"legacy_count": 0, "unreadable_count": 0, "collision": {"kind": "none", "groups": [], "identity_advisories": []}, "errors": [...]}')
    if "b" not in skip: rep(r, S, "  filename: str            # basename of the handoff file\n", "  filename: str            # basename of the handoff file\n  rel_path: str            # path relative to docs/handoff/ (flat repo: == filename)\n")
    if "i2" not in skip: rep(r, S, '  track_id: str          # frontmatter["track-id"] OR "legacy:<branch>:<filename>"', '  track_id: str          # frontmatter["track-id"] OR "legacy:<branch>:<rel_path>"')
    if "f" not in skip: rep(r, S, "never raw stderr in `errors[]`.", "never raw stderr in `errors[]`. Per-item kinds: `handoff_multibranch_unexpected_path_prefix` / `handoff_multibranch_undecodable_path` (both dual-channel).")
    if "j2" not in skip: rep(r, S, "the **four-level** compound key `(parse_ok, parsed updated_at, filename, branch)`", "the **five-level** compound key `(parse_ok, parsed updated_at, filename, branch, (rel_path == filename, rel_path))`")
    if "j4b" not in skip: rep(r, S, "four-level sort key", "five-level sort key")

def changelog_row(r, full=True):
    p = r / S; t = p.read_text(encoding="utf-8").rstrip("\n")
    row = "| 2026-09-20 | 10CG/Aria#195 — `tracks[].rel_path` + `unreadable_count`; legacy track_id `legacy:<branch>:<filename>` → `legacy:<branch>:<rel_path>`; new kinds `handoff_multibranch_unexpected_path_prefix` / `handoff_multibranch_undecodable_path`; five-level compound key (rel_path == filename, rel_path) |"
    p.write_text(t + "\n" + row + "\n", encoding="utf-8")

def p1_docs(r): rep(r, P, 'content_lines: in', 'content_lines: int, degraded_reason: None|"missing_filename"|"target_in_subdir", content_lines: in')
def l_docs(r): rep(r, L, "→ 单 track: 更新 latest.md pointer", "→ 单 track: 更新 latest.md pointer (文件在子目录时降级, 经机械 writer 路径)")

SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("aria/skills/state-scanner")
FILES = [C, W, S, P, L]
TMP = pathlib.Path(tempfile.mkdtemp(prefix="sc11-validate-"))
SP = TMP
for st in ("base", "target", "bad_codeonly", "bad_changelog_only", "bad_partial"):
    for rel in FILES:
        dst = TMP / st / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SRC / rel, dst)
states = {}
r = SP/"target"; code_changes(r); collector_docs(r); writer_docs(r); schema_docs(r); changelog_row(r); p1_docs(r); l_docs(r); states["target"] = r
r = SP/"bad_codeonly"; code_changes(r); states["bad_codeonly"] = r
r = SP/"bad_changelog_only"; changelog_row(r); states["bad_changelog_only"] = r
r = SP/"bad_partial"; code_changes(r)
collector_docs(r, skip=("j4a", "j5c")); writer_docs(r, skip=("l1b", "k2")); schema_docs(r, skip=("a2", "i2", "j4b")); changelog_row(r); p1_docs(r); l_docs(r)
states["bad_partial"] = r
states = {"base": SP/"base", **states}

PRED = {
 "a1": r"sed -n '/^tracks_multibranch:$/,/^TrackEntry:$/p' references/state-snapshot-schema.md | grep -qE '^  unreadable_count: '",
 "a2": r"grep '^\*\*Fail-soft\*\*' references/state-snapshot-schema.md | grep -q unreadable_count",
 "b":  r"sed -n '/^TrackEntry:$/,/^```$/p' references/state-snapshot-schema.md | grep -qE '^  rel_path: '",
 "c1": r"! grep -q 'Returns only the basename' scripts/collectors/handoff_multibranch.py",
 "c2": r"grep -q 'path relative to' scripts/collectors/handoff_multibranch.py",
 "f1": r"grep -v '^|' references/state-snapshot-schema.md | grep -q handoff_multibranch_unexpected_path_prefix",
 "f2": r"grep -v '^|' references/state-snapshot-schema.md | grep -q handoff_multibranch_undecodable_path",
 "g":  r"sed -n '/^## Change history/,$p' references/state-snapshot-schema.md | grep '^|' | grep -q rel_path",
 "i1": r"! grep -q -F 'legacy:<branch>:<filename>' scripts/collectors/handoff_multibranch.py",
 "i2": r"sed -n '/^TrackEntry:$/,/^```$/p' references/state-snapshot-schema.md | grep '^  track_id:' | grep -q -F 'legacy:<branch>:<rel_path>'",
 "j1": r"""python3 -B -c "import ast,sys; t=ast.parse(open('scripts/collectors/handoff_multibranch.py',encoding='utf-8').read()); f=[n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='_dedupe_sort_key'][0]; sys.exit(0 if 'rel_path' in (ast.get_docstring(f) or '') else 1)" """,
 "j2": r"grep -v '^|' references/state-snapshot-schema.md | grep 'compound key' | grep -q rel_path",
 "j3": r"sed -n '/^# Tie-break, finalized/,/^def /p' scripts/collectors/handoff_multibranch.py | grep -q rel_path",
 "j4": r"! { grep -v '^|' references/state-snapshot-schema.md; cat scripts/collectors/handoff_multibranch.py; } | grep -qiE 'four-level|four levels'",
 "j5": r"""python3 -B -c "import sys; L=open('scripts/collectors/handoff_multibranch.py',encoding='utf-8').read().split(chr(10)); hits=[i for i,l in enumerate(L) if 'dictionary-max' in l.lower()]; sys.exit(0 if hits and all(any('rel_path' in L[j] for j in range(i,min(len(L),i+2))) for i in hits) else 1)" """,
 "k":  r"""python3 -B -c "import ast,sys; t=ast.parse(open('scripts/writers/latest_md_writer.py',encoding='utf-8').read()); d={n.name:(ast.get_docstring(n) or '') for n in ast.walk(t) if isinstance(n,ast.FunctionDef)}; ok=lambda s: any(k in s for k in ('target_in_subdir','subdir',chr(23376)+chr(30446)+chr(24405))); sys.exit(0 if ok(d.get('_render_pointer','')) and ok(d.get('_render_pointer_unavailable','')) else 1)" """,
 "l1": r"""python3 -B -c "import ast,sys; t=ast.parse(open('scripts/writers/latest_md_writer.py',encoding='utf-8').read()); w=[n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='write_latest_md'][0]; sys.exit(0 if 'degraded_reason' in (ast.get_docstring(t) or '') and 'degraded_reason' in (ast.get_docstring(w) or '') else 1)" """,
 "l2": r"grep 'Return dict' references/phase-1-collectors.md | grep -q degraded_reason",
 "l3": r"grep '单 track' references/layer-l-integration.md | grep -q '子目录\|subdir'",
}
res = {}
for st, root in states.items():
    res[st] = {}
    for k, cmd in PRED.items():
        rr = subprocess.run(["bash", "-c", f"if {cmd}; then echo PASS; else echo FAIL; fi"], cwd=root, capture_output=True, text=True)
        res[st][k] = rr.stdout.strip() or ("ERR " + rr.stderr.strip()[:60])
hdr = "pred  " + " ".join(f"{s[:13]:>13}" for s in states)
print(hdr)
for k in PRED:
    print(f"{k:5} " + " ".join(f"{res[s][k]:>13}" for s in states))
shutil.rmtree(TMP)
bad = [k for k in PRED if not (res["base"][k] == "FAIL" and res["target"][k] == "PASS" and res["bad_codeonly"][k] == "FAIL")]
sys.exit(1 if bad else 0)
