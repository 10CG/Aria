#!/usr/bin/env python3
"""SC-11 定位谓词的多状态验证 (10CG/Aria#195; v5 = post_planning R4 rework, 2026-09-16).

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
  bad_j3_later_tiebreak     :370 元组不补 rel_path, 另在 dedupe_latest_per_track_container 前多一行 # Tie-break (应仅 (j3) FAIL)
  bad_tuples_stale_para     两处现状键元组都留四元, 首行写五级并另起一段讲 rel_path (应仅 (j1)(j3) FAIL)
  bad_j2_tuple_stale_para   schema 键序句只改层数词、元组仍四元, 另加一条含 compound key 与 rel_path 的 bullet (应仅 (j2) FAIL)
  bad_l1_module_scenarios   模块 docstring 的 Return dict schema 块漏补, 顶部场景列表写了 degraded_reason (应仅 (l1) FAIL)
  bad_l1_neverraises        write_latest_md 的 Returns 段漏补, Never raises 段写了 degraded_reason (应仅 (l1) FAIL)
  bad_j1_same_para          docstring 元组留四元, 同一段内元组之后补一句讲 rel_path (应仅 (j1) FAIL)
  bad_j3_same_block         注释块元组留四元, 同一块内元组之后续写 rel_path (应仅 (j3) FAIL)
  bad_j2_same_line          schema 键序句元组留四元, 同一行末尾补 plus rel_path (应仅 (j2) FAIL)
  bad_l1_title_paren        三处补充都只写进标题行括注 / 旁白, 块内与 Scenarios 结局行未改 (应仅 (l1) FAIL)
  bad_c2_module_only        契约句只写进模块 docstring, _list_handoff_files 自己的 docstring 未写 (应仅 (c2) FAIL)
  alt_j3_anchor             target 基础上注释块首行改写为 round 4 措辞 (去掉 finalized; 语义正确, 应全 PASS)
  alt_j4_numeric            target 基础上枚举层 docstring 出现 14-level (讲目录深度, 非排序键层数; 应全 PASS)
  alt_tuple_wrapped         target 基础上 docstring 与注释块的五元元组各跨两行书写 (合法写法, 应全 PASS)
行号均指 1cb3872 (v1.73.3) 原文。模拟改动按原文逐字替换: count=1 的锚点必须恰出现一次, 否则 rep() 抛出
AnchorDrift, 脚本以退出码 3 结束, stderr 以 anchor drift: 开头并点名文件、出现次数与锚点前 60 字符 ——
表示基线已漂移, 先重写模拟改动, 再判谓词。全部检查用显式判断, 不依赖 assert, python3 -O / -OO 下行为不变。

期望以 EXPECTED_FAILS 内嵌于本文件: 每个状态只声明期望 FAIL 的谓词集, 其余谓词一律期望 PASS, 由
expand_expected() 展开成全矩阵再逐格比对 (断言强度与 v4 的定值矩阵相同, 加一个状态从写 19 格降到写一行)。
退出码: 0 = 实测与展开后的期望逐格一致, 且没有任何谓词写 stderr; 1 = 任一格不符或任一谓词写 stderr (差异格与
stderr 打印到 stderr); 2 = 参数错误或源目录缺 FILES 所列文件 (打印 usage); 3 = 模拟改动的锚点漂移 (见上);
4 = 脚本自身定义不一致 (EXPECTED_FAILS 的状态集或顺序与 STATES 不符 / 含未知或重复的谓词标签,
或本 docstring 的状态列表漏列某状态); 5 = 其余未预期异常 (打印异常类型与首行)。
stdout: 默认只打印实测矩阵 (与 detailed-tasks.yaml metadata.sc11_predicate_validation 的实测块逐字节一致);
--emit-json 改为打印 states / expected / predicates / matrix 四字段的 JSON, 供由脚本输出重生成 yaml 用 (不手改);
predicates 按 yaml 谓词块的 (label) 行格式输出, 供核验两份谓词原文逐字节一致。
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
    if "j1t" not in skip: rep(r, C, "    fully deterministic — ``(parse_ok, updated_at, filename, branch)``.", "    fully deterministic — ``(parse_ok, updated_at, filename, branch, (rel_path == filename, rel_path))``.")
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


def build_tuples_stale_para(r):
    # 首行写五级、另起一段讲 rel_path, 两处现状键元组都留四元 (R3 code-reviewer 席构造)
    build_target(r, skip=("j3t", "j1t"))
    rep(r, C, "# Level 2 filename (round 2, major finding a): round 1's sort key was",
        "# Level 4 rel_path (round 4, 10CG/Aria#195): a top-level row wins over a\n# subdirectory row; among subdirectory rows the greatest ``rel_path`` wins.\n#\n# Level 2 filename (round 2, major finding a): round 1's sort key was")
    rep(r, C, "    ``filename`` is the round-2 tie-break (see the module-comment block above",
        "    ``rel_path`` is the round-4 5th level (10CG/Aria#195): a top-level row\n    wins, then dictionary-max ``rel_path``.\n\n    ``filename`` is the round-2 tie-break (see the module-comment block above")


def build_j2_tuple_stale_para(r):
    # schema 键序句只改层数词, 元组留四元; 另起一条同时含 compound key 与 rel_path 的 bullet
    build_target(r, skip=("j2",))
    rep(r, S, "the **four-level** compound key", "the **five-level** compound key")
    rep(r, S, "- **Branch tie-break (round 3, finding [M1])**:",
        "- **Path tie-break (round 4, 10CG/Aria#195)**: the compound key gains a 5th level on `rel_path` — top-level rows first.\n- **Branch tie-break (round 3, finding [M1])**:")


def build_l1_module_scenarios(r):
    # 模块 docstring 的 Return dict schema 块漏补, 顶部场景列表却写了 degraded_reason
    build_target(r, skip=("l1a",))
    rep(r, W, '    * **Zero active track** (count == 0): writes a minimal "no active tracks"\n      placeholder.\n',
        '    * **Zero active track** (count == 0): writes a minimal "no active tracks"\n      placeholder.\n    * **Single active track in a subdirectory**: writes the degraded body and\n      reports ``degraded_reason`` == "target_in_subdir".\n')


def build_l1_neverraises(r):
    # write_latest_md 的 Returns 段漏补, Never raises 段却写了 degraded_reason
    build_target(r, skip=("l1b",))
    rep(r, W, "    Never raises for missing/malformed snapshot data — all edge cases\n    produce graceful fallback content.",
        "    Never raises for missing/malformed snapshot data — all edge cases\n    produce graceful fallback content and always report ``degraded_reason``.")


def build_j4_numeric(r):
    # 讲目录深度而非排序键层数的 14-level, 不应触发 (j4) —— 左边界守卫
    build_target(r)
    rep(r, C, "    Excludes ``latest.md`` (navigation pointer).\n",
        "    Excludes ``latest.md`` (navigation pointer).\n    A path nested 14-level deep is enumerated unchanged.\n")


def build_j3_later_tiebreak(r):
    # 主控核验构造的坏态: 注释块元组漏补 rel_path, 但文件后部另有一行以 # Tie-break 开头且含 rel_path 的注释
    build_target(r, skip=("j3t",))
    rep(r, C, "\ndef dedupe_latest_per_track_container(", "\n# Tie-break note: rel_path participates via _dedupe_sort_key.\ndef dedupe_latest_per_track_container(")


def build_j1_same_para(r):
    # 元组留四元, 同一段内紧跟其后补一句讲 rel_path (R4 code-reviewer 席 ADV-1 / qa-engineer 席 A)
    build_target(r, skip=("j1t",))
    rep(r, C, "    fully deterministic — ``(parse_ok, updated_at, filename, branch)``.",
        "    fully deterministic — ``(parse_ok, updated_at, filename, branch)``.\n    The 5th level compares ``rel_path`` when the first four tie.")


def build_j3_same_block(r):
    # 元组留四元, 同一注释块内元组之后续写 rel_path (R4 code-reviewer 席 ADV-2 / qa-engineer 席 C)
    build_target(r, skip=("j3t",))
    rep(r, C, "# ``(parse_ok, parsed_updated_at, filename, branch)``.",
        "# ``(parse_ok, parsed_updated_at, filename, branch)``, with ``rel_path``\n# appended as the 5th level.")


def build_j2_same_line(r):
    # 元组留四元, 同一行末尾补 plus rel_path (R4 code-reviewer 席 ADV-3 / qa-engineer 席 B)
    build_target(r, skip=("j2",))
    rep(r, S, "the **four-level** compound key `(parse_ok, parsed updated_at, filename, branch)`",
        "the **five-level** compound key `(parse_ok, parsed updated_at, filename, branch)` plus `rel_path`")


def build_l1_title_paren(r):
    # 三处补充都只写进标题行括注 / 旁白: 字典字面量、键清单、第四种结局都没改 (R4 code-reviewer 席 ADV-4/5/6)
    build_target(r, skip=("l1a", "l1b", "l1s"))
    rep(r, W, "Return dict schema:", "Return dict schema: (10CG/Aria#195 起另含 ``degraded_reason``)")
    rep(r, W, "    Returns:\n        dict with keys:", "    Returns: (另含 ``degraded_reason``)\n        dict with keys:")
    rep(r, W, "    Scenarios:\n", "    Scenarios: (每支都返回 ``degraded_reason``)\n")


def build_c2_module_only(r):
    # 契约句只写进模块 docstring 的 TrackEntry 块, _list_handoff_files 自己的 docstring 改成不含契约句的说法
    build_target(r, skip=("c",))
    rep(r, C, "Returns only the basename (not the full path) for each file so callers",
        "Returns the enumerated handoff entries for each file so callers")
    rep(r, C, '        "filename": str,          # basename of the handoff file\n',
        '        "filename": str,          # basename of the handoff file\n        "rel_path": str,          # path relative to docs/handoff/ (flat repo: == filename)\n')


def build_tuple_wrapped(r):
    # 合法写法: 五元元组跨两行书写 (docstring 与注释块各一处), 不得假红
    build_target(r)
    rep(r, C, "    fully deterministic — ``(parse_ok, updated_at, filename, branch, (rel_path == filename, rel_path))``.",
        "    fully deterministic —\n    ``(parse_ok, updated_at, filename, branch,\n    (rel_path == filename, rel_path))``.")
    rep(r, C, "# ``(parse_ok, parsed_updated_at, filename, branch, (rel_path == filename, rel_path))``.",
        "# ``(parse_ok, parsed_updated_at, filename, branch,\n#   (rel_path == filename, rel_path))``.")


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
    "bad_tuples_stale_para": ("target 基础上注释块与 docstring 的现状键元组都留四元, 首行写五级并另起一段讲 rel_path", build_tuples_stale_para),
    "bad_j2_tuple_stale_para": ("target 基础上 schema 键序句只改层数词、元组仍四元, 另加一条同时含 compound key 与 rel_path 的 bullet", build_j2_tuple_stale_para),
    "bad_l1_module_scenarios": ("target 基础上模块 docstring 的 Return dict schema 块漏补, 顶部场景列表写了 degraded_reason", build_l1_module_scenarios),
    "bad_l1_neverraises": ("target 基础上 write_latest_md 的 Returns 段漏补, Never raises 段写了 degraded_reason", build_l1_neverraises),
    "bad_j1_same_para": ("target 基础上 docstring 元组留四元, 同一段内元组之后补一句讲 rel_path", build_j1_same_para),
    "bad_j3_same_block": ("target 基础上注释块元组留四元, 同一块内元组之后续写 rel_path", build_j3_same_block),
    "bad_j2_same_line": ("target 基础上 schema 键序句元组留四元, 同一行末尾补 plus rel_path", build_j2_same_line),
    "bad_l1_title_paren": ("target 基础上三处补充都只写进标题行括注 / 旁白, 字典字面量与键清单与第四种结局都没改", build_l1_title_paren),
    "bad_c2_module_only": ("target 基础上契约句只写进模块 docstring 的 TrackEntry 块, _list_handoff_files 自己的 docstring 未写", build_c2_module_only),
    "alt_j3_anchor": ("target 基础上注释块首行改写为 round 4 措辞 (去掉 finalized), 语义正确", build_alt_j3),
    "alt_j4_numeric": ("target 基础上枚举层 docstring 出现 14-level (讲目录深度, 非排序键层数)", build_j4_numeric),
    "alt_tuple_wrapped": ("target 基础上 docstring 与注释块的五元元组各跨两行书写 (合法写法)", build_tuple_wrapped),
}

PRED = {
 "a1": r"sed -n '/^tracks_multibranch:$/,/^TrackEntry:$/p' references/state-snapshot-schema.md | grep -qE '^  unreadable_count: '",
 "a2": r"""grep '^\*\*Fail-soft\*\*: branch-list' references/state-snapshot-schema.md | grep -oE '→ `\{[^`]*\}`' | grep -q '"unreadable_count": 0'""",
 "b":  r"sed -n '/^TrackEntry:$/,/^```$/p' references/state-snapshot-schema.md | grep -qE '^  rel_path: '",
 "c1": r"! grep -q 'Returns only the basename' scripts/collectors/handoff_multibranch.py",
 "c2": r'''python3 -B -c "import ast,sys; t=ast.parse(open('scripts/collectors/handoff_multibranch.py',encoding='utf-8').read()); f=[n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='_list_handoff_files']; sys.exit(0 if f and 'path relative to' in (ast.get_docstring(f[0]) or '') else 1)"''',
 "f1": r"grep -v '^|' references/state-snapshot-schema.md | grep -q handoff_multibranch_unexpected_path_prefix",
 "f2": r"grep -v '^|' references/state-snapshot-schema.md | grep -q handoff_multibranch_undecodable_path",
 "g":  r"sed -n '/^## Change history/,$p' references/state-snapshot-schema.md | grep '^|' | grep -q rel_path",
 "i1": r"! grep -q -F 'legacy:<branch>:<filename>' scripts/collectors/handoff_multibranch.py",
 "i2": r"sed -n '/^TrackEntry:$/,/^```$/p' references/state-snapshot-schema.md | grep '^  track_id:' | grep -q -F 'legacy:<branch>:<rel_path>'",
 "j1": r'''python3 -B -c "import ast,itertools,sys; g=lambda s: next((k+1 for k,x in enumerate(itertools.accumulate((c=='(')-(c==')') for c in s)) if x==0), 0); ok=lambda s: g(s)>0 and 'rel_path' in s[:g(s)]; t=ast.parse(open('scripts/collectors/handoff_multibranch.py',encoding='utf-8').read()); f=[n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='_dedupe_sort_key'][0]; p=(ast.get_docstring(f) or '').split(chr(10)*2)[0]; i=p.find('(parse_ok'); sys.exit(0 if i>=0 and ok(p[i:]) else 1)"''',
 "j2": r'''python3 -B -c "import itertools,sys; g=lambda s: next((k+1 for k,x in enumerate(itertools.accumulate((c=='(')-(c==')') for c in s)) if x==0), 0); ok=lambda s: g(s)>0 and 'rel_path' in s[:g(s)]; L=[l for l in open('references/state-snapshot-schema.md',encoding='utf-8').read().split(chr(10)) if not l.startswith('|') and 'compound key' in l and '(parse_ok' in l]; sys.exit(0 if L and all(ok(l[l.find('(parse_ok'):]) for l in L) else 1)"''',
 "j3": r'''python3 -B -c "import itertools,sys; g=lambda s: next((k+1 for k,x in enumerate(itertools.accumulate((c=='(')-(c==')') for c in s)) if x==0), 0); ok=lambda s: g(s)>0 and 'rel_path' in s[:g(s)]; L=open('scripts/collectors/handoff_multibranch.py',encoding='utf-8').read().split(chr(10)); t=[i for i,l in enumerate(L) if l.startswith('# Tie-break')]; d=[i for i,l in enumerate(L) if l.startswith('def _dedupe_sort_key(')]; pre=len(t)==1 and len(d)==1 and t[0]<d[0]; e=next((j for j in range(t[0]+1,d[0]) if L[j].strip()=='#'), d[0]) if pre else 0; p=chr(10).join(L[t[0]:e]) if pre else ''; i=p.find('(parse_ok'); sys.exit(0 if pre and i>=0 and ok(p[i:]) else 1)"''',
 "j4": r"! { grep -v '^|' references/state-snapshot-schema.md; cat scripts/collectors/handoff_multibranch.py tests/test_handoff_multibranch_collision_dedupe.py; } | grep -qiE '(^|[^0-9A-Za-z])(four|4)[- ]levels?|四级|四层'",
 "j5": r'''python3 -B -c "import sys; L=open('scripts/collectors/handoff_multibranch.py',encoding='utf-8').read().split(chr(10)); hits=[i for i,l in enumerate(L) if 'dictionary-max' in l.lower()]; sys.exit(0 if hits and all(any('rel_path' in L[j] for j in range(i,min(len(L),i+2))) for i in hits) else 1)"''',
 "k":  r'''python3 -B -c "import ast,sys; t=ast.parse(open('scripts/writers/latest_md_writer.py',encoding='utf-8').read()); d={n.name:(ast.get_docstring(n) or '') for n in ast.walk(t) if isinstance(n,ast.FunctionDef)}; sys.exit(0 if all('target_in_subdir' in d.get(f,'') for f in ('_render_pointer','_render_pointer_unavailable')) else 1)"''',
 "l1": r'''python3 -B -c "import ast,sys; t=ast.parse(open('scripts/writers/latest_md_writer.py',encoding='utf-8').read()); w=[n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name=='write_latest_md'][0]; d=ast.get_docstring(w) or ''; m=ast.get_docstring(t) or ''; blk=lambda s,h: s.partition(h)[2].partition(chr(10))[2].split(chr(10)*2)[0]; a=[x for x in blk(d,'Scenarios:').split(chr(10)) if chr(8594) in x]; sys.exit(0 if 'degraded_reason' in blk(m,'Return dict schema:') and 'degraded_reason' in blk(d,'Returns:') and len(a)>=4 and any('target_in_subdir' in x for x in a) else 1)"''',
 "l2": r"grep 'Return dict' references/phase-1-collectors.md | grep -q degraded_reason",
 "l3": r"grep '单 track' references/layer-l-integration.md | grep -q '子目录\|subdir'",
}

# 每个状态期望 FAIL 的谓词集 (未列出的谓词一律期望 PASS); 实跑前写定, 修改须先写明依据, 不得照实测结果回填。
# 全矩阵由 expand_expected() 展开, 断言强度与逐格定值表相同。
ALL = tuple(PRED)
EXPECTED_FAILS = {
    "base": ALL,
    "target": (),
    "bad_codeonly": ALL,
    "bad_changelog_only": tuple(k for k in PRED if k != "g"),
    "bad_partial": ("a2", "i2", "j4", "j5", "k", "l1"),
    "bad_a2_prose_only": ("a2",),
    "bad_scenarios_missing": ("l1",),
    "bad_stale_synonym": ("j4",),
    "bad_stale_header": ("j4",),
    "bad_test_docstring_stale": ("j4",),
    "bad_k_paraphrase": ("k",),
    "bad_j3_later_tiebreak": ("j3",),
    "bad_tuples_stale_para": ("j1", "j3"),
    "bad_j2_tuple_stale_para": ("j2",),
    "bad_l1_module_scenarios": ("l1",),
    "bad_l1_neverraises": ("l1",),
    "bad_j1_same_para": ("j1",),
    "bad_j3_same_block": ("j3",),
    "bad_j2_same_line": ("j2",),
    "bad_l1_title_paren": ("l1",),
    "bad_c2_module_only": ("c2",),
    "alt_j3_anchor": (),
    "alt_j4_numeric": (),
    "alt_tuple_wrapped": (),
}


def expand_expected(fails):
    if list(fails) != list(STATES):
        raise ScriptDefinitionError(f"EXPECTED_FAILS 的状态集或顺序与 STATES 不一致: {list(fails)}")
    exp = {}
    for st, ks in fails.items():
        unknown = [k for k in ks if k not in PRED]
        if unknown:
            raise ScriptDefinitionError(f"EXPECTED_FAILS[{st}] 含未知谓词标签: {unknown}")
        if len(set(ks)) != len(ks):
            raise ScriptDefinitionError(f"EXPECTED_FAILS[{st}] 有重复的谓词标签")
        exp[st] = {k: ("FAIL" if k in ks else "PASS") for k in PRED}
    return exp


def check_doc_lists_states():
    # 从源文件解析 docstring, 不读 __doc__ (python3 -OO 下 __doc__ 为 None); 按行首状态名匹配, 不用子串
    doc = ast.get_docstring(ast.parse(pathlib.Path(__file__).read_text(encoding="utf-8"))) or ""
    listed = {ln.split()[0] for ln in doc.split("\n") if ln.startswith("  ") and ln.split()}
    missing = [st for st in STATES if st not in listed]
    if missing:
        raise ScriptDefinitionError(f"docstring 的状态列表漏列: {missing}")


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
    missing_src = [rel for rel in FILES if not (src / rel).is_file()]
    if missing_src:
        print(f"usage: sc11-predicate-validation.py [aria_state_scanner_dir] [--emit-json]\n"
              f"源目录 {src} 缺 FILES 所列文件: {missing_src}", file=sys.stderr)
        return 2
    try:
        check_doc_lists_states()
        expected = expand_expected(EXPECTED_FAILS)
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
    except Exception as e:  # 未预期异常: 与矩阵不符 / 锚点漂移 / 参数错误区分开
        print(f"unexpected error: {type(e).__name__}: {str(e).splitlines()[0] if str(e) else ''}", file=sys.stderr)
        return 5
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    diffs = [f"mismatch [{st}][{k}]: expected {expected[st][k]}, got {res[st][k]}"
             for st in STATES for k in PRED if res[st][k] != expected[st][k]]
    matrix = fmt_matrix(res)
    if "--emit-json" in flags:
        print(json.dumps({"states": " · ".join(f"{st} = {d}" for st, (d, _b) in STATES.items()),
                          "expected": summarize(expected),
                          "predicates": "".join(f"({k}) {v}\n" for k, v in PRED.items()),
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
