# 在主仓根执行: python3 -B sc12_liveness.py [--force-checked]
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
