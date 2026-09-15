#!/usr/bin/env python3
"""SC-11 定位谓词的多状态验证 (10CG/Aria#195; v3.1 = post_planning R2 rework + 主控核验返修, 2026-09-15).

用法 (仓库根目录执行, 只读; 副本建在 tempfile 临时目录, 结束时在 finally 中删除):
    python3 -B openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py [aria_state_scanner_dir] [--emit-json]

默认读取 aria/skills/state-scanner 下 FILES 所列 6 个文件, 为下列每个状态各复制一份, 施加该状态的模拟改动后逐条跑 PRED:
  base                      原样, 不改 (19 条应全 FAIL)
  target                    模拟正确实现: 代码 + 全部文档面 (应全 PASS)
  bad_codeonly              只改代码, 文档一处不改 (应全 FAIL)
  bad_changelog_only        只在 schema Change history 表加一行 (除 (g) 外应全 FAIL; (g) 的检查对象就是该表行)
  bad_partial               正确实现但漏改 Fail-soft 形状 dict / TrackEntry 公式 / collector :355 与 schema :1134 的
                            four-level / dedupe docstring 的 dictionary-max 句 / write_latest_md 的 Returns 段 /
                            _render_pointer_unavailable docstring (对应谓词应为 FAIL)
  bad_a2_prose_only         target 基础上撤回 Fail-soft 形状 dict 的编辑, unreadable_count 只写进同行散文 (应仅 (a2) FAIL)
  bad_scenarios_missing     target 基础上撤回 write_latest_md docstring Scenarios 段的第四种结局 (应仅 (l1) FAIL)
  bad_stale_synonym         target 基础上 collector :355 的现状句写成 4-level (应仅 (j4) FAIL)
  bad_stale_header          target 基础上只改 :370 元组, :368 仍写 FOUR levels (应仅 (j4) FAIL)
  bad_test_docstring_stale  target 基础上 dedupe 测试文件 :885 的 docstring 漏改, 仍写 4-level (应仅 (j4) FAIL)
  bad_k_paraphrase          target 基础上 _render_pointer docstring 只写 subdirectory 意译 (应仅 (k) FAIL)
  bad_j3_later_tiebreak     target 基础上 :370 元组不补 rel_path, 另在 dedupe_latest_per_track_container 定义前
                            多出一行 # Tie-break 注释 (应仅 (j3) FAIL)
  alt_j3_anchor             target 基础上注释块首行改写为 round 4 措辞 (去掉 finalized; 语义正确, 应全 PASS)
行号均指 1cb3872 (v1.73.3) 原文。模拟改动按原文逐字替换: count=1 的锚点必须恰出现一次, 否则 rep() 抛出
AnchorDrift, 脚本以退出码 3 结束, stderr 以 anchor drift: 开头并点名文件、出现次数与锚点前 60 字符 ——
表示基线已漂移, 先重写模拟改动, 再判谓词。全部检查用显式判断, 不依赖 assert, python3 -O / -OO 下行为不变。

期望矩阵 EXPECTED 内嵌于本文件 (全部状态 x 全部谓词)。退出码: 0 = 实测与 EXPECTED 逐格一致, 且没有任何谓词
写 stderr; 1 = 任一格不符或任一谓词写 stderr (差异格与 stderr 打印到 stderr); 2 = 参数错误;
3 = 模拟改动的锚点漂移 (见上); 4 = 脚本自身定义不一致 (EXPECTED 的表头 / 行序 / 列数, 或本 docstring 漏列某状态)。
stdout: 默认只打印实测矩阵 (与 detailed-tasks.yaml metadata.sc11_predicate_validation 的实测块逐字节一致);
--emit-json 改为打印 states / expected / matrix 三字段的 JSON, 供由脚本输出重生成 yaml 用 (不手改)。
谓词原文与 detailed-tasks.yaml metadata.sc11_baseline_predicates 逐字一致。
"""
import ast
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

C = "scripts/collectors/handoff_multibranch.py"
W = "scripts/writers/latest_md_writer.py"
S = "references/state-snapshot-schema.md"
P = "references/phase-1-collectors.md"
L = "references/layer-l-integration.md"
T = "tests/test_handoff_multibranch_collision_dedupe.py"
FILES = [C, W, S, P, L, T]

TARGET_J3_HEADER = "# Tie-break, finalized (round 4, 10CG/Aria#195): the sort key is FIVE levels, all"
ALT_J3_HEADER = "# Tie-break (round 4, 10CG/Aria#195; extends the round-3 key): the sort key is FIVE levels, all"


class AnchorDrift(Exception):
    """模拟改动的锚点在副本原文中出现次数不符 ⇒ 退出码 3。"""


class ScriptDefinitionError(Exception):
    """脚本自身定义不一致 (EXPECTED 与 PRED / STATES 对不上, 或 docstring 漏列状态) ⇒ 退出码 4。"""


def rep(root, rel, old, new, count=1):
    p = root / rel
    t = p.read_text(encoding="utf-8")
    n = t.count(old)
    if count == 1:
        if n != 1:
            raise AnchorDrift(f"{rel}: 锚点应恰出现 1 次, 实际 {n} 次: {old[:60]!r}")
        t = t.replace(old, new, 1)
    else:
        if n < 1:
            raise AnchorDrift(f"{rel}: 锚点应至少出现 1 次, 实际 0 次: {old[:60]!r}")
        t = t.replace(old, new)
    p.write_text(t, encoding="utf-8")


def code_changes(r):
    rep(r, C, 'return (bucket, dt, row.get("filename") or "", row.get("branch") or "")',
        'filename = row.get("filename") or ""\n    rel = row.get("rel_path") or filename\n    return (bucket, dt, filename, row.get("branch") or "", (rel == filename, rel))')
    rep(r, W, '        content = _render_pointer(active_tracks[0], now)\n        action = "pointer"',
        '        content, degraded_reason = _render_pointer(active_tracks[0], now)\n        action = "pointer"')
    rep(r, W, '    active_tracks = _get_active_tracks(snapshot)\n    n_active = len(active_tracks)\n',
        '    active_tracks = _get_active_tracks(snapshot)\n    n_active = len(active_tracks)\n    degraded_reason = None\n')
    rep(r, W, '        "content_lines": content_lines,\n    }', '        "content_lines": content_lines,\n        "degraded_reason": degraded_reason,\n    }')


def collector_docs(r, skip=()):
    if "c" not in skip: rep(r, C, "Returns only the basename (not the full path) for each file so callers", "Returns each file's path relative to ``docs/handoff/`` so callers")
    if "i1" not in skip: rep(r, C, "legacy:<branch>:<filename>", "legacy:<branch>:<rel_path>", count=0)
    if "j1" not in skip: rep(r, C, 'sort key: four levels, all-comparable,', 'sort key: five levels (5th = ``rel_path``, top-level first), all-comparable,')
    if "j3h" not in skip: rep(r, C, "# Tie-break, finalized (round 3): the sort key is FOUR levels, all", TARGET_J3_HEADER)
    if "j3t" not in skip: rep(r, C, "# ``(parse_ok, parsed_updated_at, filename, branch)``.", "# ``(parse_ok, parsed_updated_at, filename, branch, (rel_path == filename, rel_path))``.")
    if "j4a" not in skip: rep(r, C, "# greatest under the four-level key below wins", "# greatest under the five-level key below wins")
    if "j5a" not in skip: rep(r, C, "  dictionary-max branch (round 3, finding [M1]; fully deterministic,", "  dictionary-max branch, then top-level ``rel_path`` first (round 3 [M1] / round 4; fully deterministic,")
    if "j5b" not in skip: rep(r, C, "level, ``branch`` (dictionary-max), closing the remaining non-determinism on", "level, ``branch`` (dictionary-max; 10CG/Aria#195 later adds a ``rel_path`` 5th level), closing the remaining non-determinism on")
    if "j5c" not in skip: rep(r, C, "    dictionary-max branch (see module comment above ``_dedupe_sort_key``).", "    dictionary-max branch, then top-level ``rel_path`` first (see module comment above ``_dedupe_sort_key``).")
    if "j5d" not in skip: rep(r, C, "# — newest updated_at wins (filename then branch dictionary-max", "# — newest updated_at wins (filename, branch dictionary-max, then rel_path")


def test_docs(r, skip=()):
    # 仅 docstring 的键层级措辞; 断言不动
    if "j4c" not in skip: rep(r, T, "The fixed 4-level key must pick the SAME row", "The fixed sort key (its ``branch`` level) must pick the SAME row")
    if "j4d" not in skip: rep(r, T, "The 4-level key (parse_ok, updated_at, filename,", "The key prefix (parse_ok, updated_at, filename,")


def writer_docs(r, skip=()):
    if "l1a" not in skip: rep(r, W, '        "content_lines": int,          # number of lines written\n    }', '        "content_lines": int,          # number of lines written\n        "degraded_reason": None | "missing_filename" | "target_in_subdir",\n    }')
    if "l1b" not in skip: rep(r, W, '            ``content_lines`` — number of newline-separated lines written', '            ``content_lines`` — number of newline-separated lines written\n            ``degraded_reason`` — None | "missing_filename" | "target_in_subdir"')
    if "l1s" not in skip: rep(r, W, '        active count == 1  → "pointer" action, backward-compatible pointer\n', '        active count == 1  → "pointer" action, backward-compatible pointer\n        active count == 1, file in a subdirectory\n                           → "pointer" action, degraded body (``degraded_reason`` == "target_in_subdir")\n')
    if "k1" not in skip: rep(r, W, '    determined from the track dict (edge case: legacy track missing filename).\n    """', '    determined from the track dict (edge case: legacy track missing filename),\n    or when the file lives in a subdirectory (reason ``target_in_subdir``).\n    """')
    if "k2" not in skip: rep(r, W, '    """Fallback when single active track has no filename."""', '    """Fallback when the pointer cannot be written: missing filename or ``target_in_subdir``."""')


def schema_docs(r, skip=()):
    if "a1" not in skip: rep(r, S, "  legacy_count: int               # tracks that fell back to legacy (no frontmatter)\n", "  legacy_count: int               # tracks with no frontmatter (git-show failures are NOT counted)\n  unreadable_count: int           # rows enumerated but unreadable (git show failed); ALWAYS present, default 0\n")
    if "a2" not in skip: rep(r, S, '"legacy_count": 0, "collision": {"kind": "none", "groups": []}, "errors": [...]}', '"legacy_count": 0, "unreadable_count": 0, "collision": {"kind": "none", "groups": [], "identity_advisories": []}, "errors": [...]}')
    if "a2p" not in skip: rep(r, S, "Per-branch `git ls-tree` / `git show` / `git log` failures are accumulated into the track's own `errors` and do not abort the scan of other branches.", "Per-branch `git ls-tree` / `git log` failures are accumulated into `errors` and do not abort the scan of other branches; a per-file `git show` failure no longer yields a legacy row — it is reported as soft_error `handoff_multibranch_git_show_failed` and counted in `unreadable_count`.")
    if "b" not in skip: rep(r, S, "  filename: str            # basename of the handoff file\n", "  filename: str            # basename of the handoff file\n  rel_path: str            # path relative to docs/handoff/ (flat repo: == filename)\n")
    if "i2" not in skip: rep(r, S, '  track_id: str          # frontmatter["track-id"] OR "legacy:<branch>:<filename>"', '  track_id: str          # frontmatter["track-id"] OR "legacy:<branch>:<rel_path>"')
    if "f" not in skip: rep(r, S, "never raw stderr in `errors[]`.", "never raw stderr in `errors[]`. Per-item kinds: `handoff_multibranch_unexpected_path_prefix` / `handoff_multibranch_undecodable_path` (both dual-channel).")
    if "j2" not in skip: rep(r, S, "the **four-level** compound key `(parse_ok, parsed updated_at, filename, branch)`", "the **five-level** compound key `(parse_ok, parsed updated_at, filename, branch, (rel_path == filename, rel_path))`")
    if "j4b" not in skip: rep(r, S, "four-level sort key", "five-level sort key")


def changelog_row(r):
    p = r / S
    t = p.read_text(encoding="utf-8").rstrip("\n")
    row = "| 2026-09-20 | 10CG/Aria#195 — `tracks[].rel_path` + `unreadable_count`; legacy track_id `legacy:<branch>:<filename>` → `legacy:<branch>:<rel_path>`; new kinds `handoff_multibranch_unexpected_path_prefix` / `handoff_multibranch_undecodable_path`; five-level compound key (rel_path == filename, rel_path) |"
    p.write_text(t + "\n" + row + "\n", encoding="utf-8")


def p1_docs(r):
    rep(r, P, 'content_lines: int}', 'content_lines: int, degraded_reason: None|"missing_filename"|"target_in_subdir"}')


def l_docs(r):
    rep(r, L, "→ 单 track: 更新 latest.md pointer", "→ 单 track: 更新 latest.md pointer (文件在子目录时降级, 经机械 writer 路径)")


def build_target(r, skip=()):
    code_changes(r)
    collector_docs(r, skip)
    test_docs(r, skip)
    writer_docs(r, skip)
    schema_docs(r, skip)
    changelog_row(r)
    p1_docs(r)
    l_docs(r)


def build_stale_synonym(r):
    build_target(r)
    rep(r, C, "# greatest under the five-level key below wins", "# greatest under the 4-level key below wins")


def build_k_paraphrase(r):
    build_target(r, skip=("k1",))
    rep(r, W, '    determined from the track dict (edge case: legacy track missing filename).\n    """', '    determined from the track dict (edge case: legacy track missing filename),\n    or when the file lives in a subdirectory of docs/handoff/ (the pointer would not resolve).\n    """')


def build_alt_j3(r):
    build_target(r)
    rep(r, C, TARGET_J3_HEADER, ALT_J3_HEADER)


def build_j3_later_tiebreak(r):
    # 主控核验构造的坏态: 注释块元组漏补 rel_path, 但文件后部另有一行以 # Tie-break 开头且含 rel_path 的注释
    build_target(r, skip=("j3t",))
    rep(r, C, "\ndef dedupe_latest_per_track_container(", "\n# Tie-break note: rel_path participates via _dedupe_sort_key.\ndef dedupe_latest_per_track_container(")


STATES = {
    "base": ("原样, 不改", lambda r: None),
    "target": ("模拟正确实现 (代码 + 全部文档面)", build_target),
    "bad_codeonly": ("只改代码, 文档一处不改", code_changes),
    "bad_changelog_only": ("只在 schema Change history 表加一行", changelog_row),
    "bad_partial": ("正确实现但漏改 Fail-soft 形状 dict / TrackEntry 公式 / collector :355 与 schema :1134 的 four-level / dedupe_latest_per_track_container docstring 的 dictionary-max 句 / write_latest_md 的 Returns 段 / _render_pointer_unavailable docstring",
                    lambda r: build_target(r, skip=("j4a", "j5c", "l1b", "k2", "a2", "i2", "j4b"))),
    "bad_a2_prose_only": ("target 基础上撤回 Fail-soft 形状 dict 的编辑, unreadable_count 只写进同行散文", lambda r: build_target(r, skip=("a2",))),
    "bad_scenarios_missing": ("target 基础上撤回 write_latest_md docstring Scenarios 段的第四种结局", lambda r: build_target(r, skip=("l1s",))),
    "bad_stale_synonym": ("target 基础上 collector :355 的现状句写成 4-level", build_stale_synonym),
    "bad_stale_header": ("target 基础上只改 :370 元组, :368 仍写 FOUR levels", lambda r: build_target(r, skip=("j3h",))),
    "bad_test_docstring_stale": ("target 基础上 dedupe 测试文件 :885 的 docstring 漏改, 仍写 4-level", lambda r: build_target(r, skip=("j4c",))),
    "bad_k_paraphrase": ("target 基础上 _render_pointer docstring 只写 subdirectory 意译, 不含字面 target_in_subdir", build_k_paraphrase),
    "bad_j3_later_tiebreak": ("target 基础上 :370 元组不补 rel_path, 另在 dedupe_latest_per_track_container 定义前多出一行含 rel_path 的 # Tie-break 注释", build_j3_later_tiebreak),
    "alt_j3_anchor": ("target 基础上注释块首行改写为 round 4 措辞 (去掉 finalized), 语义正确", build_alt_j3),
}

PRED = {
 "a1": r"sed -n '/^tracks_multibranch:$/,/^TrackEntry:$/p' references/state-snapshot-schema.md | grep -qE '^  unreadable_count: '",
 "a2": r"""grep '^\*\*Fail-soft\*\*: branch-list' references/state-snapshot-schema.md | grep -oE '→ `\{[^`]*\}`' | grep -q '"unreadable_count": 0'""",
 "b":  r"sed -n '/^TrackEntry:$/,/^```$/p' references/state-snapshot-schema.md | grep -qE '^  rel_path: '",
 "c1": r"! grep -q 'Returns only the basename' scripts/collectors/handoff_multibranch.py",
 "c2": r"grep -q 'path relative to' scripts/collectors/handoff_multibranch.py",
 "f1": r"grep -v '^|' references/state-snapshot-schema.md | grep -q handoff_multibranch_unexpected_path_prefix",
 "f2": r"grep -v '^|' references/state-snapshot-schema.md | grep -q handoff_multibranch_undecodable_path",
 "g":  r"sed -n '/^## Change history/,$p' references/state-snapshot-schema.md | grep '^|' | grep -q rel_path",
 "i1": r"! grep -q -F 'legacy:<branch>:<filename>' scripts/collectors/handoff_multibranch.py",
 "i2": r"sed -n '/^TrackEntry:$/,/^```$/p' references/state-snapshot-schema.md | grep '^  track_id:' | grep -q -F 'legacy:<branch>:<rel_path>'",
 "j1": r'''python3 -B -c "import ast,sys; t=ast.parse(open('scripts/collectors/handoff_multibranch.py',encoding='utf-8').read()); f=[n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='_dedupe_sort_key'][0]; sys.exit(0 if 'rel_path' in (ast.get_docstring(f) or '') else 1)"''',
 "j2": r"grep -v '^|' references/state-snapshot-schema.md | grep 'compound key' | grep -q rel_path",
 "j3": r'''python3 -B -c "import sys; L=open('scripts/collectors/handoff_multibranch.py',encoding='utf-8').read().split(chr(10)); t=[i for i,l in enumerate(L) if l.startswith('# Tie-break')]; d=[i for i,l in enumerate(L) if l.startswith('def _dedupe_sort_key(')]; sys.exit(0 if len(t)==1 and len(d)==1 and t[0]<d[0] and any('rel_path' in L[j] for j in range(t[0],d[0])) else 1)"''',
 "j4": r"! { grep -v '^|' references/state-snapshot-schema.md; cat scripts/collectors/handoff_multibranch.py tests/test_handoff_multibranch_collision_dedupe.py; } | grep -qiE 'four[- ]levels?|4[- ]levels?|四级|四层'",
 "j5": r'''python3 -B -c "import sys; L=open('scripts/collectors/handoff_multibranch.py',encoding='utf-8').read().split(chr(10)); hits=[i for i,l in enumerate(L) if 'dictionary-max' in l.lower()]; sys.exit(0 if hits and all(any('rel_path' in L[j] for j in range(i,min(len(L),i+2))) for i in hits) else 1)"''',
 "k":  r'''python3 -B -c "import ast,sys; t=ast.parse(open('scripts/writers/latest_md_writer.py',encoding='utf-8').read()); d={n.name:(ast.get_docstring(n) or '') for n in ast.walk(t) if isinstance(n,ast.FunctionDef)}; sys.exit(0 if all('target_in_subdir' in d.get(f,'') for f in ('_render_pointer','_render_pointer_unavailable')) else 1)"''',
 "l1": r'''python3 -B -c "import ast,sys; t=ast.parse(open('scripts/writers/latest_md_writer.py',encoding='utf-8').read()); w=[n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='write_latest_md'][0]; d=ast.get_docstring(w) or ''; pre,_,scen=d.partition('Scenarios:'); ret=pre.partition('Returns:')[2]; sys.exit(0 if 'degraded_reason' in (ast.get_docstring(t) or '') and 'degraded_reason' in ret and ('degraded_reason' in scen or 'target_in_subdir' in scen) else 1)"''',
 "l2": r"grep 'Return dict' references/phase-1-collectors.md | grep -q degraded_reason",
 "l3": r"grep '单 track' references/layer-l-integration.md | grep -q '子目录\|subdir'",
}

# 全部状态 x 全部谓词的期望 (R3 执笔席实跑前写定; 修改须先写明依据再改, 不得照实测结果回填)
EXPECTED = """\
state                     a1   a2   b    c1   c2   f1   f2   g    i1   i2   j1   j2   j3   j4   j5   k    l1   l2   l3
base                      FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL
target                    PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS
bad_codeonly              FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL
bad_changelog_only        FAIL FAIL FAIL FAIL FAIL FAIL FAIL PASS FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL
bad_partial               PASS FAIL PASS PASS PASS PASS PASS PASS PASS FAIL PASS PASS PASS FAIL FAIL FAIL FAIL PASS PASS
bad_a2_prose_only         PASS FAIL PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS
bad_scenarios_missing     PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS FAIL PASS PASS
bad_stale_synonym         PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS FAIL PASS PASS PASS PASS PASS
bad_stale_header          PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS FAIL PASS PASS PASS PASS PASS
bad_test_docstring_stale  PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS FAIL PASS PASS PASS PASS PASS
bad_k_paraphrase          PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS FAIL PASS PASS PASS
bad_j3_later_tiebreak     PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS FAIL PASS PASS PASS PASS PASS PASS
alt_j3_anchor             PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS PASS
"""


def parse_expected(text):
    lines = [ln.split() for ln in text.strip("\n").split("\n")]
    labels = lines[0][1:]
    if labels != list(PRED):
        raise ScriptDefinitionError(f"EXPECTED 表头与 PRED 键序不一致: {labels}")
    exp = {}
    for cells in lines[1:]:
        if len(cells) != len(labels) + 1:
            raise ScriptDefinitionError(f"EXPECTED 行列数不符: {cells[:1]}")
        if any(c not in ("PASS", "FAIL") for c in cells[1:]):
            raise ScriptDefinitionError(f"EXPECTED 单元格只能是 PASS / FAIL: {cells[0]}")
        exp[cells[0]] = dict(zip(labels, cells[1:]))
    if list(exp) != list(STATES):
        raise ScriptDefinitionError(f"EXPECTED 行序与 STATES 不一致: {list(exp)}")
    return exp


def check_doc_lists_states():
    # 从源文件解析 docstring, 不读 __doc__ (python3 -OO 下 __doc__ 为 None)
    doc = ast.get_docstring(ast.parse(pathlib.Path(__file__).read_text(encoding="utf-8"))) or ""
    missing = [st for st in STATES if st not in doc]
    if missing:
        raise ScriptDefinitionError(f"docstring 未列举状态: {missing}")


def fmt_matrix(res):
    w = max(len(s) for s in STATES)
    def row(name, cells):
        return (name.ljust(w) + "  " + " ".join(c.ljust(4) for c in cells)).rstrip()
    out = [row("state", list(PRED))]
    for st in STATES:
        out.append(row(st, [res[st][k] for k in PRED]))
    return "\n".join(out) + "\n"


def summarize(exp):
    def lab(ks):
        return "".join(f"({k})" for k in ks)
    parts = []
    for st in STATES:
        fails = [k for k in PRED if exp[st][k] == "FAIL"]
        passes = [k for k in PRED if exp[st][k] == "PASS"]
        if not passes:
            parts.append(f"{st} 全 FAIL")
        elif not fails:
            parts.append(f"{st} 全 PASS")
        elif len(fails) > len(passes):
            parts.append(f"{st} 除 {lab(passes)} 外全 FAIL")
        else:
            parts.append(f"{st} 中 {lab(fails)} 为 FAIL, 其余 PASS")
    return "; ".join(parts)


def main(argv):
    flags = [a for a in argv if a.startswith("--")]
    args = [a for a in argv if not a.startswith("--")]
    if set(flags) - {"--emit-json"} or len(args) > 1:
        print("usage: sc11-predicate-validation.py [aria_state_scanner_dir] [--emit-json]", file=sys.stderr)
        return 2
    src = pathlib.Path(args[0]) if args else pathlib.Path("aria/skills/state-scanner")
    try:
        check_doc_lists_states()
        expected = parse_expected(EXPECTED)
    except ScriptDefinitionError as e:
        print(f"script definition error: {e}", file=sys.stderr)
        return 4

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="sc11-validate-"))
    res, stderr_notes = {}, []
    try:
        for st, (_desc, build) in STATES.items():
            root = tmp / st
            for rel in FILES:
                dst = root / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src / rel, dst)
            build(root)
            res[st] = {}
            for k, cmd in PRED.items():
                rr = subprocess.run(["bash", "-c", f"if {cmd}; then echo PASS; else echo FAIL; fi"],
                                    cwd=root, capture_output=True, text=True)
                out = rr.stdout.strip()
                res[st][k] = out if out in ("PASS", "FAIL") else "ERR"
                if rr.stderr.strip():
                    stderr_notes.append(f"stderr [{st}][{k}]: {rr.stderr.strip()[:200]}")
    except AnchorDrift as e:
        print(f"anchor drift: {e}", file=sys.stderr)
        return 3
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    diffs = [f"mismatch [{st}][{k}]: expected {expected[st][k]}, got {res[st][k]}"
             for st in STATES for k in PRED if res[st][k] != expected[st][k]]
    matrix = fmt_matrix(res)
    if "--emit-json" in flags:
        print(json.dumps({"states": " · ".join(f"{st} = {d}" for st, (d, _b) in STATES.items()),
                          "expected": summarize(expected),
                          "matrix": matrix}, ensure_ascii=False, indent=1))
    else:
        sys.stdout.write(matrix)
    for line in diffs + stderr_notes:
        print(line, file=sys.stderr)
    verdict = "OK" if not diffs and not stderr_notes else "FAIL"
    print(f"verdict: {verdict} (mismatch cells {len(diffs)}, stderr notes {len(stderr_notes)}; "
          f"{len(STATES)} states x {len(PRED)} predicates)", file=sys.stderr)
    return 0 if verdict == "OK" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
