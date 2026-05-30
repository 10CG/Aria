#!/usr/bin/env python3
"""Rule #6 deterministic structural substitute for #58 (emergency-hotfix + audit file-scope).

#58 is all prose/config/convention changes — no LLM AB. This grep-verifies the
doc-existence Success Criteria. Behavior-conformance SC (advisory lane execution,
file-scope actual filtering) are dogfood-only (NOT covered here — see README).

Run: python3 aria-plugin-benchmarks/emergency-hotfix-audit-file-scope/test_doc_existence.py
"""
import os
import sys

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def read(rel):
    try:
        with open(os.path.join(_REPO, rel), "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


CHECKS = [
    # (description, file, required substrings (all must be present))
    ("emergency_hotfix rule fields (priority 1.85 / confidence 85% / auto_execute No)",
     "aria/skills/state-scanner/references/rules/basic-rules.md",
     ["emergency_hotfix", "priority: 1.85", "confidence: 85%", "auto_execute: No", "hotfix/*"]),
    ("emergency_hotfix index row in RECOMMENDATION_RULES main table",
     "aria/skills/state-scanner/RECOMMENDATION_RULES.md",
     ["`emergency_hotfix`", "1.85", "emergency-hotfix"]),
    ("scope_skip_paths default list in DEFAULTS.json",
     "aria/skills/config-loader/DEFAULTS.json",
     ['"scope_skip_paths"', '"deploy/"', '"docs/"', '"*.md"']),
    ("scope_skip_paths match semantics in config-example.md",
     "aria/skills/config-loader/config-example.md",
     ["audit.scope_skip_paths", "startswith", "endswith", "降级", "pass-through"]),
    ("Prod-Validated single-line trailer + hotfix commit format in git-commit.md",
     "standards/conventions/git-commit.md",
     ["Prod-Validated:", "hotfix(", "根因:", "单行", "Submodule-Rollback"]),
    ("phase-b-developer Prod-Validated trailer gate (block if absent)",
     "aria/skills/phase-b-developer/SKILL.md",
     ["Prod-Validated", "trailer", "BLOCK", "回标准 lane", "manual prod validation"]),
    ("audit-engine file-scope: merge-base self-fetch + 0-file pass-through + min(resolved,convergence)",
     "aria/skills/audit-engine/SKILL.md",
     ["scope_skip_paths", "merge-base", "len(changed_files) == 0", "pass-through",
      "min(resolved_mode, convergence)", "不读 snapshot"]),
    ("audit-engine emergency hotfix pre_merge→convergence (only audit-on)",
     "aria/skills/audit-engine/SKILL.md",
     ["emergency hotfix lane", "pre_merge", "convergence", "audit.enabled"]),
    ("phase-a-planner hotfix lane overview (skip A.1-A.3 + cross-ref)",
     "aria/skills/phase-a-planner/SKILL.md",
     ["emergency hotfix lane", "A.1-A.3", "Prod-Validated", "phase-b-developer"]),
    ("phase-c-integrator pre_merge→convergence call point (CI gate not exempt)",
     "aria/skills/phase-c-integrator/SKILL.md",
     ["emergency_hotfix", "pre_merge", "convergence", "不豁免"]),
]


def main():
    passed = failed = 0
    for desc, rel, subs in CHECKS:
        content = read(rel)
        missing = [s for s in subs if s not in content]
        if not content:
            print(f"  FAIL - {desc}\n         (file not found: {rel})")
            failed += 1
        elif missing:
            print(f"  FAIL - {desc}\n         missing in {rel}: {missing}")
            failed += 1
        else:
            print(f"  ok   - {desc}")
            passed += 1
    print(f"\ndoc-existence checks: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
