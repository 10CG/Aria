#!/usr/bin/env python3
"""
Commit Message Validator for commit-msg-generator benchmark tests.

This script validates commit messages against the assertions defined in evals.json.

Usage:
    python validate_commit.py <commit_message> <eval_id>
    python validate_commit.py --all <commit_messages_dir>
"""

import re
import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class AssertionResult:
    """Result of a single assertion check."""
    id: str
    name: str
    description: str
    passed: bool
    severity: str
    evidence: Optional[str] = None


@dataclass
class EvalResult:
    """Result of a complete evaluation."""
    eval_id: int
    eval_name: str
    passed: bool
    pass_rate: float
    results: List[AssertionResult]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "eval_id": self.eval_id,
            "eval_name": self.eval_name,
            "passed": self.passed,
            "pass_rate": self.pass_rate,
            "results": [
                {
                    "id": r.id,
                    "name": r.name,
                    "description": r.description,
                    "passed": r.passed,
                    "severity": r.severity,
                    "evidence": r.evidence
                }
                for r in self.results
            ]
        }


class CommitMessageValidator:
    """Validates commit messages against benchmark assertions."""

    VALID_TYPES = {'feat', 'fix', 'docs', 'style', 'refactor', 'test', 'perf', 'build', 'ci', 'chore', 'revert'}

    def __init__(self, evals_path: str):
        with open(evals_path, 'r', encoding='utf-8') as f:
            self.evals_data = json.load(f)
        self.evals = {e['id']: e for e in self.evals_data['evals']}

    def validate(self, commit_message: str, eval_id: int) -> EvalResult:
        """Validate a commit message against a specific eval."""
        if eval_id not in self.evals:
            raise ValueError(f"Eval ID {eval_id} not found")

        eval_config = self.evals[eval_id]
        assertions = eval_config.get('assertions', [])

        results = []
        for assertion in assertions:
            result = self._check_assertion(commit_message, assertion)
            results.append(result)

        passed = all(r.passed for r in results if r.severity == 'critical')
        critical_passed = sum(1 for r in results if r.passed and r.severity == 'critical')
        critical_total = sum(1 for r in results if r.severity == 'critical')

        pass_rate = critical_passed / critical_total if critical_total > 0 else 1.0

        return EvalResult(
            eval_id=eval_id,
            eval_name=eval_config['name'],
            passed=passed,
            pass_rate=pass_rate,
            results=results
        )

    def _check_assertion(self, commit_message: str, assertion: Dict[str, Any]) -> AssertionResult:
        """Check a single assertion against the commit message."""
        check = assertion.get('check', '')
        passed = False
        evidence = None

        # Parse the commit message
        first_line = commit_message.split('\n')[0]
        subject_match = re.match(r'^\w+\([^)]+\):\s*(.+)$', first_line)
        subject = subject_match.group(1) if subject_match else first_line
        first_line_length = len(first_line)

        # Build evaluation context
        context = {
            'commit_message': commit_message,
            'first_line': first_line,
            'first_line_length': first_line_length,
            'subject': subject,
        }

        try:
            # Evaluate the check expression
            passed = self._evaluate_check(check, context)
            evidence = f"Check: {check}"
        except Exception as e:
            evidence = f"Error evaluating check: {e}"
            passed = False

        return AssertionResult(
            id=assertion['id'],
            name=assertion['name'],
            description=assertion['description'],
            passed=passed,
            severity=assertion.get('severity', 'medium'),
            evidence=evidence
        )

    def _evaluate_check(self, check: str, context: Dict[str, Any]) -> bool:
        """Evaluate a check expression against the context."""
        commit_message = context['commit_message']
        first_line = context['first_line']
        first_line_length = context['first_line_length']
        subject = context['subject']

        # Handle common check patterns
        # Pattern: commit_message.matches(/regex/)
        match_result = re.match(r'commit_message\.matches\(/(.+)/\)', check)
        if match_result:
            pattern = match_result.group(1)
            return bool(re.search(pattern, commit_message))

        # Pattern: commit_message.includes('text')
        include_result = re.match(r"commit_message\.includes\(['\"](.+?)['\"]\)", check)
        if include_result:
            text = include_result.group(1)
            return text in commit_message

        # Pattern: first_line_length <= N
        length_result = re.match(r'first_line_length\s*(<=|>=|==|<|>)\s*(\d+)', check)
        if length_result:
            op = length_result.group(1)
            value = int(length_result.group(2))
            if op == '<=':
                return first_line_length <= value
            elif op == '>=':
                return first_line_length >= value
            elif op == '==':
                return first_line_length == value
            elif op == '<':
                return first_line_length < value
            elif op == '>':
                return first_line_length > value

        # Pattern: !commit_message.match(/regex/)
        not_match_result = re.match(r'!commit_message\.match\(/(.+)/\)', check)
        if not_match_result:
            pattern = not_match_result.group(1)
            return not re.search(pattern, commit_message)

        # Pattern: subject.toLowerCase().includes('text')
        subject_include = re.match(r"subject\.toLowerCase\(\)\.includes\(['\"](.+?)['\"]\)", check)
        if subject_include:
            text = subject_include.group(1).lower()
            return text in subject.lower()

        # Pattern: commit_message.indexOf('X') < commit_message.indexOf('Y')
        index_compare = re.match(r"commit_message\.indexOf\(['\"](.+?)['\"]\)\s*(<|>|==)\s*commit_message\.indexOf\(['\"](.+?)['\"]\)", check)
        if index_compare:
            text1 = index_compare.group(1)
            op = index_compare.group(2)
            text2 = index_compare.group(3)
            idx1 = commit_message.find(text1)
            idx2 = commit_message.find(text2)
            if idx1 == -1 or idx2 == -1:
                return False
            if op == '<':
                return idx1 < idx2
            elif op == '>':
                return idx1 > idx2
            elif op == '==':
                return idx1 == idx2

        # Pattern: commit_message.split('\n\n').length >= N
        split_check = re.match(r"commit_message\.split\(['\"](.+?)['\"]\)\.length\s*(>=|<=|==)\s*(\d+)", check)
        if split_check:
            sep = split_check.group(1)
            op = split_check.group(2)
            value = int(split_check.group(3))
            parts = commit_message.split(sep)
            if op == '>=':
                return len(parts) >= value
            elif op == '<=':
                return len(parts) <= value
            elif op == '==':
                return len(parts) == value

        # Pattern: true (always pass)
        if check == 'true':
            return True

        # Pattern: !subject.match(/regex/) || subject.match(/regex/)
        compound_check = re.match(r'!subject\.match\(/(.+)/\)\s*\|\|\s*subject\.match\(/(.+)/\)', check)
        if compound_check:
            pattern1 = compound_check.group(1)
            pattern2 = compound_check.group(2)
            return (not re.search(pattern1, subject)) or bool(re.search(pattern2, subject))

        # Default: try to evaluate as Python expression (with safety)
        # This is a fallback for complex expressions
        return self._safe_eval(check, context)

    def _safe_eval(self, check: str, context: Dict[str, Any]) -> bool:
        """Safely evaluate a check expression."""
        # Build a safe namespace with only the context values
        safe_namespace = {
            'commit_message': context['commit_message'],
            'first_line': context['first_line'],
            'first_line_length': context['first_line_length'],
            'subject': context['subject'],
        }

        # Convert JS-style expressions to Python
        py_check = check
        py_check = py_check.replace('.includes(', ' in ')
        py_check = py_check.replace('.match(', 're.search(')
        py_check = py_check.replace('.indexOf(', '.find(')
        py_check = py_check.replace('.toLowerCase()', '.lower()')
        py_check = py_check.replace('.split(', 'split(')
        py_check = py_check.replace('.length', 'len()')

        try:
            # Very basic evaluation - only for simple cases
            # For complex cases, implement specific handlers above
            return eval(py_check, {"__builtins__": {}}, safe_namespace)
        except:
            # If we can't evaluate, default to False with a warning
            print(f"Warning: Could not evaluate check: {check}")
            return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python validate_commit.py <commit_message_file> <eval_id>")
        print("       python validate_commit.py --all <commit_messages_dir>")
        sys.exit(1)

    # Find evals.json
    script_dir = Path(__file__).parent
    evals_path = script_dir / "evals.json"

    if not evals_path.exists():
        print(f"Error: evals.json not found at {evals_path}")
        sys.exit(1)

    validator = CommitMessageValidator(str(evals_path))

    if sys.argv[1] == "--all":
        # Validate all commit messages in a directory
        messages_dir = Path(sys.argv[2])
        results = []

        for msg_file in sorted(messages_dir.glob("*.txt")):
            eval_id = int(msg_file.stem.replace("eval-", ""))
            with open(msg_file, 'r', encoding='utf-8') as f:
                commit_message = f.read()

            result = validator.validate(commit_message, eval_id)
            results.append(result)

        # Output aggregate results
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        avg_pass_rate = sum(r.pass_rate for r in results) / total if total > 0 else 0

        print(f"\n{'='*60}")
        print(f"Benchmark Results: commit-msg-generator")
        print(f"{'='*60}")
        print(f"Total Evals: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Pass Rate: {avg_pass_rate:.1%}")
        print(f"{'='*60}\n")

        # Output individual results
        for result in results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"[{status}] Eval {result.eval_id}: {result.eval_name}")
            for r in result.results:
                mark = "✓" if r.passed else "✗"
                print(f"    [{mark}] {r.id}: {r.name} ({r.severity})")

        # Save results to JSON
        output_path = messages_dir / "benchmark_results.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "skill_name": "commit-msg-generator",
                "summary": {
                    "total": total,
                    "passed": passed,
                    "failed": total - passed,
                    "pass_rate": avg_pass_rate
                },
                "results": [r.to_dict() for r in results]
            }, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {output_path}")

    else:
        # Validate a single commit message
        msg_file = Path(sys.argv[1])
        eval_id = int(sys.argv[2])

        with open(msg_file, 'r', encoding='utf-8') as f:
            commit_message = f.read()

        result = validator.validate(commit_message, eval_id)

        print(f"\nEval {result.eval_id}: {result.eval_name}")
        print(f"Status: {'✅ PASSED' if result.passed else '❌ FAILED'}")
        print(f"Pass Rate: {result.pass_rate:.1%}\n")

        print("Assertion Results:")
        for r in result.results:
            status = "✓" if r.passed else "✗"
            print(f"  [{status}] {r.id}: {r.name}")
            print(f"      {r.description}")
            print(f"      Severity: {r.severity}")


if __name__ == "__main__":
    main()
