#!/usr/bin/env python3
"""T5 重判 dogfood — rule6-4b 分类修订的门判定前后对比。

数据源: ab-results/2026-10-19-issue-groomer-trigger/ 三轮 run_eval.json (只读)。
套件: ab-suite/trigger/issue-groomer.json (含 type 标注, T4 落地)。
路径解析自脚本位置 (spec 目录), 可在任意 CWD 复跑; 输出 idx = 套件条目行号 (should-not 为 10-19)。
旧门: 每条 should-not trigger_rate >= 0.5 判 fail (SOT 修订前)。
新门: 仅 capability 类 should-not 计入门; routing 类转观察面 (呈现不计 fail)。
证伪路径: 若分类修订无实际门效果, 各臂新旧门判定不变 (SC-2 转 red)。
"""
import json, sys

BASE = __file__.rsplit("/", 4)[0] + "/"
SUITE = BASE + "aria-plugin-benchmarks/ab-suite/trigger/issue-groomer.json"
AB = BASE + "aria-plugin-benchmarks/ab-results/2026-10-19-issue-groomer-trigger/"

def main():
    suite = json.load(open(SUITE, encoding="utf-8"))
    sn = [it for it in suite if not it.get("should_trigger")]
    types = [it.get("type") for it in sn]
    if any(t not in ("capability", "routing") for t in types):
        sys.exit(f"SC-1 FAIL: should-not 条目缺合法 type: {types}")
    rows = []
    changed = False
    for arm in ("real-v1-prefix", "real-v2-broad", "real"):
        d = json.load(open(AB + arm + "/run_eval.json", encoding="utf-8"))
        by_q = {r["query"]: r.get("trigger_rate") for r in d["results"] if not r.get("should_trigger")}
        rates = [by_q.get(it["query"]) for it in sn]
        old_fail = [i + 10 for i, r in enumerate(rates) if r is not None and r >= 0.5]
        cap_fail = [i + 10 for i, r in enumerate(rates) if r is not None and r >= 0.5 and types[i] == "capability"]
        rout_hit = [i + 10 for i, r in enumerate(rates) if r is not None and r >= 0.5 and types[i] == "routing"]
        rows.append((arm, old_fail, cap_fail, rout_hit))
        if old_fail != cap_fail:
            changed = True
        print(f"== {arm}")
        print(f"   旧门 fail 条目 (idx): {old_fail}  -> 门判定 {'FAIL' if old_fail else 'PASS'}")
        print(f"   新门 capability fail: {cap_fail} -> 门判定 {'FAIL' if cap_fail else 'PASS'}")
        print(f"   观察面 routing 误触:  {rout_hit} (呈现, 不判 fail)")
    print()
    print("SC-2 (分类修订有实际门效果):", "GREEN — 至少一轮新旧门判定不同" if changed else "RED — 前后门判定无变化, 修订无门效果")

if __name__ == "__main__":
    main()
