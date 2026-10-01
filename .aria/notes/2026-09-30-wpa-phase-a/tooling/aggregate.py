#!/usr/bin/env python3
"""Land per-seat audit reports verbatim from a workflow journal and build a mechanical aggregate.

usage: aggregate.py <journal.jsonl> <checkpoint> <round> <round-ts> <spec-id> <context-path>
                    <out-dir> <prev-round-summary.json|-> <summary-out.json> <sibling-json>

- per-seat file: <out>/<checkpoint>-R<round>-<round-ts>-<spec-id>-<role>.md  (report_markdown verbatim)
- aggregate:     <out>/<checkpoint>-R<round>-<round-ts>-<spec-id>-aggregated.md  (mechanical part only;
                 the controller appends its own section afterwards)
- summary json:  per-seat verdict/counts/vote/findings + CM key set, for the next round's comparison.

Convergence (repo precedent, 10CG/Aria#199 R1-R10): conclusions_stable = (Critical+Major key set of this
round == that of the previous round) AND unanimous PASS vote; Round 1 can never converge.
Finding ids are recomputed from the 4-tuple (sha256("category:scope:severity:type")[:8]) and compared
with the id each seat wrote; mismatches are reported, the recomputed id is authoritative.
"""
import hashlib
import json
import sys
from pathlib import Path

(journal, checkpoint, rnd, round_ts, spec_id, context, out_dir, prev_path, summary_out, sibling_path) = sys.argv[1:11]
rnd = int(rnd)
out = Path(out_dir)
out.mkdir(parents=True, exist_ok=True)

labels, seats = {}, {}
for line in Path(journal).read_text(encoding="utf-8").splitlines():
    e = json.loads(line)
    if e.get("type") == "started":
        labels[e["agentId"]] = e["label"]
    elif e.get("type") == "result":
        lab = labels.get(e["agentId"], "")
        role = lab.split(":", 1)[1] if ":" in lab else lab
        if isinstance(e.get("result"), dict) and "report_markdown" in e["result"]:
            seats[role] = e["result"]

ORDER = ["tech-lead", "backend-architect", "qa-engineer", "code-reviewer", "knowledge-manager"]
roles = [r for r in ORDER if r in seats] + sorted(r for r in seats if r not in ORDER)


def fid(f):
    return hashlib.sha256(f"{f['category']}:{f['scope']}:{f['severity']}:{f['type']}".encode("utf-8")).hexdigest()[:8]


summary = {"round": rnd, "seats": {}, "cm_keys": [], "all_keys": []}
id_mismatch = []
for role in roles:
    s = seats[role]
    p = out / f"{checkpoint}-R{rnd}-{round_ts}-{spec_id}-{role}.md"
    p.write_text(s["report_markdown"], encoding="utf-8")
    fs = []
    for f in s["findings"]:
        rid = fid(f)
        if rid != f["id"]:
            id_mismatch.append((role, f["label"], f["id"], rid))
        fs.append({**f, "id": rid, "seat_id": f["id"]})
    # counts cross-check: structured counts vs findings list
    n = {k: sum(1 for f in fs if f["severity"] == k) for k in ("critical", "major", "minor")}
    summary["seats"][role] = {
        "verdict": s["verdict"], "vote": s["vote"], "counts": s["counts"], "counted_from_findings": n,
        "report_file": p.name, "findings": fs,
        "frontmatter_ok": s["report_markdown"].lstrip().startswith("---"),
    }

cm = sorted({f["id"] for r in summary["seats"].values() for f in r["findings"] if f["severity"] in ("critical", "major")})
allk = sorted({f["id"] for r in summary["seats"].values() for f in r["findings"]})
summary["cm_keys"], summary["all_keys"] = cm, allk
prev = json.loads(Path(prev_path).read_text(encoding="utf-8")) if prev_path != "-" else None
unanimous = all(v["vote"] == "PASS" for v in summary["seats"].values()) and len(summary["seats"]) == 5
stable = (prev is not None) and (set(cm) == set(prev["cm_keys"]))
converged = bool(stable and unanimous and rnd >= 2)
summary.update({"unanimous_pass": unanimous, "cm_stable_vs_prev": stable if prev else None, "converged": converged,
                "incomplete": len(summary["seats"]) < 5})
tot = {k: sum(v["counted_from_findings"][k] for v in summary["seats"].values()) for k in ("critical", "major", "minor")}
dedup = {k: len({f["id"] for v in summary["seats"].values() for f in v["findings"] if f["severity"] == k}) for k in ("critical", "major", "minor")}
verdict = "FAIL" if dedup["critical"] else ("PASS_WITH_WARNINGS" if dedup["major"] else "PASS")
summary.update({"counts_raw": tot, "counts_dedup": dedup, "verdict": verdict})
Path(summary_out).write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")

sib = json.loads(Path(sibling_path).read_text(encoding="utf-8")) if sibling_path != "-" else {}
L = []
L += ["---", f"checkpoint: {checkpoint}", "mode: convergence", f"rounds: {rnd}", f"converged: {str(converged).lower()}",
      "oscillation: false", "overridden_by_user: false", "degraded: false", "drift_terminated: false",
      "drift_check_skipped: true", "drift_warning: false", "is_refocus: false", f"verdict: {verdict}",
      f"timestamp: {round_ts[:10]}T{round_ts[11:13]}:{round_ts[13:15]}:{round_ts[15:17]}.000Z", f"context: {context}",
      f"agents: [{', '.join(roles)}]",
      f"counts_raw: {tot['critical']}C/{tot['major']}M/{tot['minor']}m",
      f"counts_dedup: {dedup['critical']}C/{dedup['major']}M/{dedup['minor']}m",
      f"sibling_probe: {sib.get('verdict', 'n/a')}", "---", ""]
L += [f"# {checkpoint} R{rnd} 聚合 — {spec_id} — {'**CONVERGED**' if converged else '未收敛'}", ""]
L += ["> 本节为机械聚合 (脚本从运行记录生成; 各席报告原文见同目录同轮次文件)。主控独立核验与处置意见见文末「主控记录」节。", ""]
L += ["## 判定", "", "| 席 | verdict | counts (自报) | counts (按 findings 计) | vote | 报告文件 |", "|---|---|---|---|---|---|"]
for role in roles:
    v = summary["seats"][role]
    c, n = v["counts"], v["counted_from_findings"]
    L.append(f"| {role} | {v['verdict']} | {c['critical']}C/{c['major']}M/{c['minor']}m | {n['critical']}C/{n['major']}M/{n['minor']}m | {v['vote']} | `{v['report_file']}` |")
L += ["", "## 全部 finding (按席位原编号, 不转述)", "", "| 席 | 编号 | 键 (重算) | 席位所写 id | severity | type | category | scope | summary (席位原文) |", "|---|---|---|---|---|---|---|---|---|"]
for role in roles:
    for f in summary["seats"][role]["findings"]:
        esc = lambda t: str(t).replace("|", "\\|").replace("\n", " ")
        L.append(f"| {role} | {f['label']} | `{f['id']}` | `{f['seat_id']}` | {f['severity']} | {f['type']} | {f['category']} | {esc(f['scope'])} | {esc(f['summary'])} |")
L += ["", "## 收敛计算 (本仓先例口径: 相邻两轮 Critical+Major 键集相等 且 全票 PASS)", ""]
L.append(f"- 本轮 Critical+Major 键集 ({len(cm)}): {', '.join('`'+k+'`' for k in cm) or '∅'}")
if prev:
    L.append(f"- 上一轮 Critical+Major 键集 ({len(prev['cm_keys'])}): {', '.join('`'+k+'`' for k in prev['cm_keys']) or '∅'}")
    L.append(f"- conclusions_stable = {stable}")
else:
    L.append("- 第 1 轮无上一轮可比, 按算法不可收敛, 必须进入下一轮")
L.append(f"- unanimous_pass = {unanimous} ({sum(1 for v in summary['seats'].values() if v['vote']=='PASS')} PASS / {sum(1 for v in summary['seats'].values() if v['vote']!='PASS')} REVISE)")
L.append(f"- converged = {converged}")
L += ["", "## 机械核对", ""]
L.append(f"- 席位数 {len(roles)} / 5; incomplete = {summary['incomplete']}")
L.append(f"- frontmatter 开头: {', '.join(r + ('=ok' if summary['seats'][r]['frontmatter_ok'] else '=MISSING') for r in roles)}")
mism = [r for r in roles if summary['seats'][r]['counts'] != summary['seats'][r]['counted_from_findings']]
L.append(f"- 自报 counts 与 findings 计数不一致的席: {', '.join(mism) or '无'}")
L.append(f"- finding id 与四元组重算不一致: {len(id_mismatch)} 条" + ("" if not id_mismatch else " — " + "; ".join(f"{r} {l} 写 `{a}` 重算 `{b}`" for r, l, a, b in id_mismatch)))
L.append(f"- 竞品 Spec 探针 (本轮入口): status={sib.get('status','n/a')} / verdict={sib.get('verdict','n/a')}")
L += ["", "## 主控记录", "", "(主控在落盘后追加)", ""]
(out / f"{checkpoint}-R{rnd}-{round_ts}-{spec_id}-aggregated.md").write_text("\n".join(L), encoding="utf-8")
print(json.dumps({"roles": roles, "counts_raw": tot, "counts_dedup": dedup, "verdict": verdict, "cm_keys": cm,
                  "unanimous": unanimous, "stable": stable if prev else None, "converged": converged,
                  "id_mismatch": len(id_mismatch), "count_mismatch_seats": mism}, ensure_ascii=False))
