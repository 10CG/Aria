#!/usr/bin/env python3
"""M6 168h 跑 — 旧/stale dispatch 只读摘要 (pre-flight 决策辅助).

目的: 168h 跑启动前, live DB (`dispatches.db`) 里已存在 #28 部署之前的旧
dispatch 行。它们对 AC-2 分层无害 (acceptance 用 json_extract '$.issue_type_hint',
旧行返回 NULL 不计入), 但 Day-7 **corpus 采样** (Phase 4 从 dispatches 挑 10 个
"完成" dispatch) 可能误采到这些旧行。本脚本让 owner 看清存量, 决定:
  (a) 启动前清空旧行, 或
  (b) 采样时按 Day-1 alloc anchor 时间窗过滤。

严格只读: 以 SQLite `mode=ro` 打开, 仅 SELECT/PRAGMA, 绝不写。
Secret-hygiene (Rule #7): 只取 dispatch_id / state / is_synthetic / model_used /
时间戳 / issue_type_hint (label) 等非敏感字段; 绝不打印 payload_json value、
fail_detail 全文、凭据或 webhook。

用法 (在 light-1 节点上跑, 或 scp 后跑):
    python3 m6-list-stale-dispatches.py
    python3 m6-list-stale-dispatches.py --db /path/to/dispatches.db
    python3 m6-list-stale-dispatches.py --since 2026-07-01T00:00:00   # 模拟 Day-1 anchor 过滤
    python3 m6-list-stale-dispatches.py --limit 50

注意: 本脚本 **不做任何清理**。清理 (DELETE) 应由 owner 显式确认后另行执行。
"""
from __future__ import annotations

import argparse
import sqlite3
import sys

DEFAULT_DB = "/opt/aether-volumes/aria-layer1/data/dispatches.db"
ISSUE_TYPE_HINT_KEY = "$.issue_type_hint"  # 与 acceptance/check-m6-e2e-acceptance.py 一致
TERMINAL_COMPLETE = "S9_CLOSE"             # corpus "完成" 判据 (Phase 4)


def connect_ro(db_path: str) -> sqlite3.Connection:
    """只读打开; DB 不存在 / 无法打开则给出清晰错误。"""
    uri = f"file:{db_path}?mode=ro"
    try:
        return sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError as e:
        sys.exit(f"[ERR] 无法只读打开 DB ({db_path}): {e}")


def cols_of(cur: sqlite3.Cursor, table: str) -> list[str]:
    return [r[1] for r in cur.execute(f"PRAGMA table_info({table})").fetchall()]


def has_table(cur: sqlite3.Cursor, table: str) -> bool:
    row = cur.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone()
    return row is not None


def pick_time_col(available: list[str]) -> str | None:
    """选一个最有意义的时间列做排序/过滤 (优先 cycle_start_ts)。"""
    for c in ("cycle_start_ts", "state_entered_at", "last_heartbeat_at"):
        if c in available:
            return c
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="M6 旧 dispatch 只读摘要 (不清理)")
    ap.add_argument("--db", default=DEFAULT_DB, help=f"DB 路径 (默认 {DEFAULT_DB})")
    ap.add_argument(
        "--since",
        default=None,
        help="只统计该时间戳之后的行 (模拟 Day-1 anchor 过滤); 比较基于所选时间列字面值",
    )
    ap.add_argument("--limit", type=int, default=100, help="逐行明细最多显示数 (默认 100)")
    args = ap.parse_args()

    conn = connect_ro(args.db)
    cur = conn.cursor()

    if not has_table(cur, "dispatches"):
        sys.exit("[ERR] 表 dispatches 不存在 — DB 路径是否正确?")

    dcols = cols_of(cur, "dispatches")
    has_audit = has_table(cur, "dispatch_audit_log")
    time_col = pick_time_col(dcols)

    print(f"# M6 旧 dispatch 摘要 (只读)")
    print(f"DB: {args.db}")
    print(f"排序/时间列: {time_col or '(无可用时间列)'}")
    print(f"corpus '完成' 判据: state == {TERMINAL_COMPLETE}")
    print()

    # ---- 聚合 ----
    total = cur.execute("SELECT COUNT(*) FROM dispatches").fetchone()[0]
    print(f"总 dispatch 行: {total}")

    if "is_synthetic" in dcols:
        syn = cur.execute(
            "SELECT SUM(CASE WHEN is_synthetic=1 THEN 1 ELSE 0 END), COUNT(*) FROM dispatches"
        ).fetchone()
        print(f"  synthetic: {syn[0] or 0} / real: {(syn[1] or 0) - (syn[0] or 0)}")

    print("  按 state:")
    for state, n in cur.execute(
        "SELECT state, COUNT(*) FROM dispatches GROUP BY state ORDER BY COUNT(*) DESC"
    ).fetchall():
        flag = "  ← corpus 可采 (完成态)" if state == TERMINAL_COMPLETE else ""
        print(f"    {state or '(null)':<24} {n}{flag}")

    complete_n = cur.execute(
        "SELECT COUNT(*) FROM dispatches WHERE state=?", (TERMINAL_COMPLETE,)
    ).fetchone()[0]
    print()
    print(f"⚠ 已达 {TERMINAL_COMPLETE} 的旧行 (corpus 采样误采风险): {complete_n}")

    if time_col:
        rng = cur.execute(
            f"SELECT MIN({time_col}), MAX({time_col}) FROM dispatches "
            f"WHERE {time_col} IS NOT NULL"
        ).fetchone()
        print(f"时间范围 ({time_col}): {rng[0]}  →  {rng[1]}")
        if args.since:
            after = cur.execute(
                f"SELECT COUNT(*) FROM dispatches WHERE {time_col} > ?", (args.since,)
            ).fetchone()[0]
            print(
                f"过滤模拟: {time_col} > {args.since} → {after} 行保留, "
                f"{total - after} 行被过滤掉 (= 视为旧行)"
            )

    # ---- 逐行明细 ----
    print()
    print(f"## 逐行明细 (最多 {args.limit} 行)")
    order = f"ORDER BY {time_col} DESC" if time_col else ""
    sel_cols = [c for c in ("dispatch_id", "state", "is_synthetic", "model_used", "spec_id") if c in dcols]
    if time_col:
        sel_cols.append(time_col)
    rows = cur.execute(
        f"SELECT {', '.join(sel_cols)} FROM dispatches {order} LIMIT ?", (args.limit,)
    ).fetchall()

    # 逐行附 issue_type_hint (来自 audit log, 仅 label 值, 安全)
    hint_map: dict[str, str] = {}
    if has_audit and "dispatch_id" in dcols:
        try:
            for did, hint in cur.execute(
                "SELECT dispatch_id, "
                f"json_extract(payload_json, '{ISSUE_TYPE_HINT_KEY}') "
                "FROM dispatch_audit_log "
                f"WHERE json_extract(payload_json, '{ISSUE_TYPE_HINT_KEY}') IS NOT NULL"
            ).fetchall():
                hint_map[did] = hint
        except sqlite3.OperationalError:
            pass  # 旧 schema 无 json 支持等, 容错

    header = sel_cols + ["issue_type_hint"]
    print("  | " + " | ".join(header) + " |")
    did_idx = sel_cols.index("dispatch_id") if "dispatch_id" in sel_cols else None
    for r in rows:
        vals = [str(v) if v is not None else "" for v in r]
        did = r[did_idx] if did_idx is not None else None
        vals.append(hint_map.get(did, "") if did is not None else "")
        print("  | " + " | ".join(vals) + " |")

    print()
    print("提示: 本脚本只读, 未做任何修改。如需清理旧行, 请 owner 显式确认后另行执行 DELETE。")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
