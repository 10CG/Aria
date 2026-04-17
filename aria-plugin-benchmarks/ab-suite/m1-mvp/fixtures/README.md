# M1 MVP Synthetic Fixture Repo

> **Purpose**: Synthetic codebase for US-021 M1 MVP DEMO-001/002 executions
> **IP classification**: `synthetic` (合成, 无 10CG 真实业务 IP, per AD-M1-9 / LA-I1)
> **Established**: 2026-04-17 (T0.2)
> **Consumer**: `.aria/issues/DEMO-001.yaml` + `.aria/issues/DEMO-002.yaml` (T3.2)

## 结构

```
fixtures/
├── README.md           ← DEMO-001 target (modify single line)
├── src/
│   ├── python/         ← DEMO-002 target language
│   ├── node/           ← reserved for M2+
│   └── go/             ← reserved for M2+
└── tests/              ← DEMO-002 test output 目录
```

## DEMO-001 scenario

**Action**: Modify one line of this README (e.g., change date stamp)
**Expected diff**: 1 line `+` in README.md
**Verification**: `expected_file_touched: [README.md]` + `expected_diff_contains: ["<new line content>"]`

## DEMO-002 scenario

**Action**: Add 1 utility function to `src/python/` + corresponding test in `tests/`
**Expected diff**: 2 new files (utility.py + test_utility.py) with net additions
**Verification**: `expected_file_touched: [src/python/utility.py, tests/test_utility.py]` + `expected_diff_contains: ["def ", "def test_", "assert"]`

## Stability contract

- **No real IP**: All code synthetic / generated; no 10CG internal business logic
- **No credentials / secrets**: Never commit API keys, tokens, or env vars
- **Forward compatibility**: DEMO-002 scenario may extend to new function types; baseline function signature is `def <name>(input: T) -> T`

## 继承自 M0

本 fixture 继承 M0 T3.5 合成 fixture 模式 (`aria-plugin-benchmarks/ab-suite/glm-smoke/templates/`); owner (simonfish) 已按 AD-M0-9 签字批准此类 synthetic fixture 用途。

---

**Signed-by**: human:simonfish @ 2026-04-17 (IP classification verification, per T3.2.3)
**Next step**: T3.2 起草 `.aria/issues/DEMO-001.yaml` + `.aria/issues/DEMO-002.yaml` 具体描述
