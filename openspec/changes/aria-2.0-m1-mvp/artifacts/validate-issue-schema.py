#!/usr/bin/env python3
"""
validate-issue-schema.py — Aria 2.0 M1 issue schema v0.1 validator

Python stdlib only (no PyYAML), following M0 validate-m0-handoff.py pattern.

Checks:
  - Required fields (top-level + expected_changes + metadata subblocks)
  - Type conformance (string / list / enum)
  - id regex + filename match
  - description action verb (新增/修改/删除) + 至少 1 个 file/function-like token
  - ip_classification enum (M1: only "synthetic" allowed, per AD-M1-9)
  - expected_file_touched non-empty
  - expected_diff_contains non-empty
  - metadata.target_repo slug format
  - metadata.created_by format (human:<user> | ai:<agent>)
  - metadata.created_at RFC 3339

Usage:
  python3 validate-issue-schema.py <path/to/issue.yaml>

Exit codes:
  0 = PASS
  1 = FAIL (see stderr for details)
  2 = Usage error (missing argument, file not found)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


# ---------- Minimal YAML subset parser (stdlib-only) ----------
# Supports: mappings, lists, literal-block scalars (|), plain scalars, quoted scalars
# Does NOT support: anchors, tags, flow style mappings/sequences, merge keys

def parse_yaml(text: str) -> dict:
    """Parse a minimal YAML subset sufficient for Aria issue schema."""
    lines = [(i, line) for i, line in enumerate(text.splitlines(), 1) if line.strip() and not line.lstrip().startswith("#")]
    return _parse_block(lines, indent=0, idx=0)[0] if lines else {}


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _parse_block(lines: list, indent: int, idx: int):
    """Return (parsed_value, next_idx). Supports mapping and list blocks."""
    if idx >= len(lines):
        return None, idx

    first_line_no, first_line = lines[idx]
    first_content = first_line.strip()

    # List block?
    if first_content.startswith("- "):
        result = []
        while idx < len(lines):
            line_no, line = lines[idx]
            line_indent = _indent(line)
            if line_indent < indent:
                break
            if line_indent != indent or not line.lstrip().startswith("- "):
                break
            item_content = line.lstrip()[2:].strip()
            # Simple scalar list item
            if ":" not in item_content or item_content.startswith(("'", '"')):
                result.append(_parse_scalar(item_content))
                idx += 1
            else:
                # Nested mapping as list item (not used in issue schema v0.1, fail loud)
                raise ValueError(f"Line {line_no}: nested mapping in list not supported in v0.1 schema parser")
        return result, idx

    # Mapping block
    result = {}
    while idx < len(lines):
        line_no, line = lines[idx]
        line_indent = _indent(line)
        if line_indent < indent:
            break
        if line_indent != indent:
            idx += 1
            continue

        content = line.strip()
        if ":" not in content:
            raise ValueError(f"Line {line_no}: expected 'key: value' in mapping; got {content!r}")

        key, _, rest = content.partition(":")
        key = key.strip()
        rest = rest.strip()

        if not rest:
            # Block value (mapping / list / literal block)
            idx += 1
            if idx >= len(lines):
                result[key] = None
                break
            next_line_no, next_line = lines[idx]
            next_indent = _indent(next_line)
            if next_indent <= indent:
                result[key] = None
            else:
                value, idx = _parse_block(lines, indent=next_indent, idx=idx)
                result[key] = value
        elif rest == "|":
            # Literal block scalar
            idx += 1
            block_indent = None
            block_lines = []
            while idx < len(lines):
                bl_no, bl = lines[idx]
                bl_indent = _indent(bl)
                if bl_indent <= indent:
                    break
                if block_indent is None:
                    block_indent = bl_indent
                block_lines.append(bl[block_indent:] if bl_indent >= block_indent else bl)
                idx += 1
            result[key] = "\n".join(block_lines)
        else:
            result[key] = _parse_scalar(rest)
            idx += 1

    return result, idx


def _parse_scalar(s: str):
    """Parse a scalar (string/int/bool/null/empty-inline-collection)."""
    if not s:
        return None
    if s.lower() in ("null", "~"):
        return None
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    if s == "[]":
        return []
    if s == "{}":
        return {}
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    try:
        return int(s)
    except ValueError:
        pass
    return s


# ---------- Validation logic ----------

ID_RE = re.compile(r"^[A-Z][A-Z0-9-]+$")
REPO_SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*$")
CREATED_BY_RE = re.compile(r"^(human|ai):\S+")
RFC3339_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
ACTION_VERBS = ("新增", "修改", "删除")
IP_CLASSIFICATION_M1 = {"synthetic"}  # M1 only accepts synthetic


def validate(data: dict, filename_stem: str) -> list:
    errors = []
    warnings = []

    def err(msg):
        errors.append(msg)

    def warn(msg):
        warnings.append(msg)

    # --- Top-level required fields ---
    required_top = ["id", "title", "description", "files", "expected_changes", "ip_classification", "metadata"]
    for field in required_top:
        if field not in data:
            err(f"missing required field: {field}")
            return errors, warnings  # Can't continue

    # --- id ---
    if not isinstance(data["id"], str):
        err(f"id must be string, got {type(data['id']).__name__}")
    elif not ID_RE.match(data["id"]):
        err(f"id {data['id']!r} does not match regex {ID_RE.pattern}")
    elif data["id"] != filename_stem:
        err(f"id {data['id']!r} does not match filename stem {filename_stem!r}")

    # --- title ---
    if not isinstance(data["title"], str):
        err(f"title must be string, got {type(data['title']).__name__}")
    elif len(data["title"]) > 120:
        err(f"title length {len(data['title'])} exceeds 120 chars")
    elif "\n" in data["title"]:
        err("title must not contain newlines")

    # --- description + action verb + file/function token (per AD-M1-3 + QA-F4) ---
    if not isinstance(data["description"], str):
        err(f"description must be string, got {type(data['description']).__name__}")
    else:
        desc = data["description"]
        if not any(verb in desc for verb in ACTION_VERBS):
            err(f"description missing required action verb (one of {ACTION_VERBS})")
        # Heuristic file/function token: contains "." or "/" (file extension / path)
        # or camelCase / snake_case identifier followed by "(" (function-like)
        if not re.search(r"[.\/_a-zA-Z]+\.[a-zA-Z]{1,6}\b", desc) and not re.search(r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*\(", desc):
            warn("description may lack concrete file or function name (reduces CLAUDE_NO_OP risk; not fatal)")

    # --- files ---
    if not isinstance(data["files"], list):
        err(f"files must be list, got {type(data['files']).__name__}")
    elif not all(isinstance(f, str) for f in data["files"]):
        err("all files[] entries must be strings")

    # --- expected_changes ---
    exp = data["expected_changes"]
    if not isinstance(exp, dict):
        err(f"expected_changes must be mapping")
    else:
        for sub in ["expected_file_touched", "expected_diff_contains"]:
            if sub not in exp:
                err(f"expected_changes.{sub} missing")
            elif not isinstance(exp[sub], list):
                err(f"expected_changes.{sub} must be list")
            elif len(exp[sub]) == 0:
                err(f"expected_changes.{sub} must be non-empty (per AD-M1-3)")
            elif not all(isinstance(item, str) for item in exp[sub]):
                err(f"expected_changes.{sub}[] entries must all be strings")

    # --- ip_classification (AD-M1-9 enforcement) ---
    ip = data["ip_classification"]
    if not isinstance(ip, str):
        err(f"ip_classification must be string")
    elif ip not in IP_CLASSIFICATION_M1:
        err(f"ip_classification {ip!r} not allowed in M1; only {IP_CLASSIFICATION_M1} (per AD-M1-9, M2+ unlock requires external counsel review)")

    # --- metadata ---
    meta = data["metadata"]
    if not isinstance(meta, dict):
        err("metadata must be mapping")
    else:
        for sub in ["target_repo", "created_by", "created_at"]:
            if sub not in meta:
                err(f"metadata.{sub} missing")
        if "target_repo" in meta and isinstance(meta["target_repo"], str) and not REPO_SLUG_RE.match(meta["target_repo"]):
            err(f"metadata.target_repo {meta['target_repo']!r} not in 'org/repo' slug format")
        if "created_by" in meta and isinstance(meta["created_by"], str) and not CREATED_BY_RE.match(meta["created_by"]):
            err(f"metadata.created_by {meta['created_by']!r} not in 'human:<user>' or 'ai:<agent>' format")
        if "created_at" in meta and isinstance(meta["created_at"], str) and not RFC3339_RE.match(meta["created_at"]):
            err(f"metadata.created_at {meta['created_at']!r} not RFC 3339 format")

    return errors, warnings


def main(argv):
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <path/to/issue.yaml>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    if not path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2

    try:
        data = parse_yaml(path.read_text(encoding="utf-8"))
    except ValueError as e:
        print(f"YAML parse error in {path}: {e}", file=sys.stderr)
        return 1

    filename_stem = path.stem
    errors, warnings = validate(data, filename_stem)

    print(f"Validating: {path}")
    print("─" * 60)

    if warnings:
        for w in warnings:
            print(f"  ⚠ WARN: {w}")

    if errors:
        for e in errors:
            print(f"  ✗ ERROR: {e}", file=sys.stderr)
        print("─" * 60)
        print(f"✗ FAIL: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1

    print("─" * 60)
    print(f"✓ PASS: 0 errors, {len(warnings)} warning(s) — schema v0.1 compliant")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
