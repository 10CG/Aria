#!/usr/bin/env python3
"""
Arch-Search Benchmark Validator

Validates arch-search skill outputs against expected assertions.
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple

def load_eval_metadata(eval_id: int, base_path: str) -> dict:
    """Load evaluation metadata from evals.json"""
    evals_path = Path(base_path) / "evals" / "evals.json"
    with open(evals_path, 'r', encoding='utf-8') as f:
        evals_data = json.load(f)

    for eval_item in evals_data['evals']:
        if eval_item['id'] == eval_id:
            return eval_item
    return None

def check_assertion(output: str, assertion: dict) -> Tuple[bool, str]:
    """Check a single assertion against the output"""
    check = assertion.get('check', '')
    severity = assertion.get('severity', 'medium')
    name = assertion.get('name', 'unnamed')

    # Token-based checks
    if 'tokens_used' in check:
        match = re.search(r'tokens_used\s*([<>=!]+)\s*(\d+)', check)
        if match:
            op, threshold = match.group(1), int(match.group(2))
            # Extract token count from output if present
            token_match = re.search(r'tokens?[：:\s]*(\d+)', output, re.IGNORECASE)
            if token_match:
                tokens_used = int(token_match.group(1))
                if op == '<':
                    result = tokens_used < threshold
                elif op == '<=':
                    result = tokens_used <= threshold
                elif op == '>':
                    result = tokens_used > threshold
                elif op == '>=':
                    result = tokens_used >= threshold
                else:
                    result = tokens_used == threshold
                return result, f"Tokens used: {tokens_used} {op} {threshold}"
            # If no token count found, estimate from output length
            estimated_tokens = len(output) // 4
            return estimated_tokens < threshold, f"Estimated tokens: ~{estimated_tokens}"

    # Output length check
    if 'output.length' in check:
        match = re.search(r'output\.length\s*([<>=!]+)\s*(\d+)', check)
        if match:
            op, threshold = match.group(1), int(match.group(2))
            length = len(output)
            if op == '>':
                result = length > threshold
            elif op == '>=':
                result = length >= threshold
            else:
                result = length < threshold
            return result, f"Output length: {length} {op} {threshold}"

    # Regex match checks
    if 'output.match' in check:
        match = re.search(r'output\.match\(/(.+?)/([i]?)\)', check)
        if match:
            pattern = match.group(1)
            flags = re.IGNORECASE if 'i' in match.group(2) else 0
            try:
                found = bool(re.search(pattern, output, flags))
                return found, f"Pattern '{pattern}' {'found' if found else 'not found'}"
            except re.error:
                return False, f"Invalid regex pattern: {pattern}"

    # Includes checks
    if 'output.includes' in check:
        # Handle multiple includes in one check (&&)
        includes = re.findall(r"output\.includes\('([^']+)'\)", check)
        includes += re.findall(r'output\.includes\("([^"]+)"\)', check)

        if includes:
            all_found = all(inc in output for inc in includes)
            found_items = [inc for inc in includes if inc in output]
            missing_items = [inc for inc in includes if inc not in output]
            evidence = f"Found: {found_items}" if all_found else f"Missing: {missing_items}"
            return all_found, evidence

    # Negation checks
    if '!output.includes' in check:
        excludes = re.findall(r"!output\.includes\('([^']+)'\)", check)
        excludes += re.findall(r'!output\.includes\("([^"]+)"\)', check)

        if excludes:
            none_found = all(exc not in output for exc in excludes)
            found_items = [exc for exc in excludes if exc in output]
            evidence = "None found (pass)" if none_found else f"Unexpectedly found: {found_items}"
            return none_found, evidence

    # OR logic checks (||)
    if '||' in check and 'output.includes' in check:
        includes = re.findall(r"output\.includes\('([^']+)'\)", check)
        includes += re.findall(r'output\.includes\("([^"]+)"\)', check)

        if includes:
            any_found = any(inc in output for inc in includes)
            found_items = [inc for inc in includes if inc in output]
            evidence = f"Found at least one: {found_items}" if any_found else "None found"
            return any_found, evidence

    return False, f"Could not evaluate check: {check}"

def validate_eval(eval_id: int, run_type: str, base_path: str) -> dict:
    """Validate a single eval run"""
    output_path = Path(base_path) / "iteration-1" / f"eval-{eval_id}" / run_type / "outputs" / "search_result.txt"

    if not output_path.exists():
        return {
            "eval_id": eval_id,
            "run_type": run_type,
            "verdict": "error",
            "error": "Output file not found",
            "assertions": []
        }

    with open(output_path, 'r', encoding='utf-8') as f:
        output = f.read()

    eval_meta = load_eval_metadata(eval_id, base_path)
    if not eval_meta:
        return {
            "eval_id": eval_id,
            "run_type": run_type,
            "verdict": "error",
            "error": "Evaluation metadata not found"
        }

    assertions = eval_meta.get('assertions', [])
    results = []

    for assertion in assertions:
        passed, evidence = check_assertion(output, assertion)
        results.append({
            "id": assertion.get('id', 'unknown'),
            "name": assertion.get('name', 'unnamed'),
            "severity": assertion.get('severity', 'medium'),
            "passed": passed,
            "evidence": evidence
        })

    # Calculate verdict based on severity
    critical_failed = any(r['severity'] == 'critical' and not r['passed'] for r in results)
    high_failed = sum(1 for r in results if r['severity'] == 'high' and not r['passed'])

    if critical_failed:
        verdict = "fail"
    elif high_failed > 1:
        verdict = "fail"
    elif high_failed == 1:
        verdict = "partial"
    else:
        verdict = "pass"

    return {
        "eval_id": eval_id,
        "eval_name": eval_meta.get('name', f'eval-{eval_id}'),
        "category": eval_meta.get('category', 'unknown'),
        "run_type": run_type,
        "verdict": verdict,
        "assertions": results,
        "output_length": len(output)
    }

def generate_benchmark(base_path: str) -> dict:
    """Generate full benchmark report"""
    evals_path = Path(base_path) / "evals" / "evals.json"
    with open(evals_path, 'r', encoding='utf-8') as f:
        evals_data = json.load(f)

    total_evals = len(evals_data['evals'])

    with_skill_results = []
    without_skill_results = []

    for eval_item in evals_data['evals']:
        eval_id = eval_item['id']

        with_skill = validate_eval(eval_id, "with_skill", base_path)
        without_skill = validate_eval(eval_id, "without_skill", base_path)

        with_skill_results.append(with_skill)
        without_skill_results.append(without_skill)

    # Calculate summary
    with_skill_passed = sum(1 for r in with_skill_results if r['verdict'] == 'pass')
    without_skill_passed = sum(1 for r in without_skill_results if r['verdict'] == 'pass')

    benchmark = {
        "benchmark_name": "arch-search",
        "skill_version": "1.1.0",
        "iteration": 1,
        "timestamp": "2026-03-13T05:00:00Z",
        "total_evals": total_evals,
        "summary": {
            "with_skill": {
                "passed": with_skill_passed,
                "failed": total_evals - with_skill_passed,
                "pass_rate": round(with_skill_passed / total_evals, 2) if total_evals > 0 else 0
            },
            "without_skill": {
                "passed": without_skill_passed,
                "failed": total_evals - without_skill_passed,
                "pass_rate": round(without_skill_passed / total_evals, 2) if total_evals > 0 else 0
            },
            "improvement": {
                "pass_rate_delta": round((with_skill_passed - without_skill_passed) / total_evals, 2) if total_evals > 0 else 0,
                "pass_count_delta": with_skill_passed - without_skill_passed
            }
        },
        "by_category": {},
        "eval_results": []
    }

    # Group by category
    categories = {}
    for i, eval_item in enumerate(evals_data['evals']):
        cat = eval_item.get('category', 'unknown')
        if cat not in categories:
            categories[cat] = {"total": 0, "passed": 0}
        categories[cat]["total"] += 1
        if with_skill_results[i]['verdict'] == 'pass':
            categories[cat]["passed"] += 1

    for cat, data in categories.items():
        data["pass_rate"] = round(data["passed"] / data["total"], 2) if data["total"] > 0 else 0

    benchmark["by_category"] = categories

    # Individual results
    for i, eval_item in enumerate(evals_data['evals']):
        benchmark["eval_results"].append({
            "eval_id": eval_item['id'],
            "name": eval_item.get('name', f'eval-{eval_item["id"]}'),
            "category": eval_item.get('category', 'unknown'),
            "with_skill": with_skill_results[i]['verdict'].upper(),
            "without_skill": without_skill_results[i]['verdict'].upper(),
            "key_finding": f"Layer used: {eval_item.get('expected_layer', 'unknown')}"
        })

    return benchmark

if __name__ == "__main__":
    import sys

    base_path = sys.argv[1] if len(sys.argv) > 1 else "F:/work2025/cursor/Aria/aria-plugin-benchmarks/arch-search"

    benchmark = generate_benchmark(base_path)

    output_path = Path(base_path) / "iteration-1" / "benchmark.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(benchmark, f, indent=2, ensure_ascii=False)

    print(f"Benchmark saved to: {output_path}")
    print(f"\nSummary:")
    print(f"  With Skill: {benchmark['summary']['with_skill']['passed']}/{benchmark['total_evals']} passed ({benchmark['summary']['with_skill']['pass_rate']*100:.0f}%)")
    print(f"  Without Skill: {benchmark['summary']['without_skill']['passed']}/{benchmark['total_evals']} passed ({benchmark['summary']['without_skill']['pass_rate']*100:.0f}%)")
    print(f"  Improvement: +{benchmark['summary']['improvement']['pass_rate_delta']*100:.0f}%")
