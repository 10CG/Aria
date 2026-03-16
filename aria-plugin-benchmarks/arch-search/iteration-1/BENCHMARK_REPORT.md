# Arch-Search Skill Benchmark Report

> **Version**: 1.1.0 | **Iteration**: 1 | **Date**: 2026-03-13

## 📊 Executive Summary

| Metric | With Skill | Without Skill | Improvement |
|--------|------------|---------------|-------------|
| **Pass Rate** | 93% (14/15) | 53% (8/15) | +40% |
| **Avg Tokens** | ~450 | ~1800 | -75% |
| **Layer 1 Success** | 80% | N/A | - |
| **Output Format** | Consistent | Variable | ✅ |

## 🎯 Key Findings

### Layer 1 (快速路由) Performance
- **Success Rate**: 100% (4/4 tests)
- **Avg Tokens**: ~280
- **Token Savings**: 75-87% vs baseline
- **Best Case**: Auth keyword routing (320 tokens vs 2500 baseline = 87% savings)

### Layer 2 (架构文档搜索) Performance
- **Success Rate**: 100% (2/2 tests)
- **Avg Tokens**: ~650
- **Use Case**: Unknown keywords that still map to architecture docs

### Layer 3 (传统搜索回退) Performance
- **Triggered**: 1/15 tests (rare keyword "foo-bar-baz")
- **Behavior**: Correctly indicated fallback with clear messaging
- **Tokens**: ~1600 (still 20% savings vs pure traditional)

## 📈 Per-Category Results

| Category | Tests | Passed | Pass Rate |
|----------|-------|--------|-----------|
| Layer 1 Routing | 4 | 4 | 100% |
| Layer 2 Search | 2 | 2 | 100% |
| Layer 3 Fallback | 1 | 1 | 100% |
| Format Validation | 1 | 1 | 100% |
| i18n Support | 2 | 2 | 100% |
| Token Efficiency | 2 | 1 | 50% |
| Module Entry | 1 | 1 | 100% |
| Domain Specific | 1 | 1 | 100% |
| Complex Query | 1 | 1 | 100% |

## ✅ Strengths

1. **Excellent Token Efficiency** - 75-87% savings on Layer 1 queries
2. **Consistent Output Format** - Emoji headers, structured sections, clear layer indicators
3. **Smart Layer Selection** - Correct routing to appropriate search layer
4. **Bilingual Support** - Chinese/English keyword handling
5. **Clear Fallback Mechanism** - Layer 3 triggers with useful feedback
6. **Accurate Code Pointers** - Correct file path references

## ⚠️ Weaknesses

1. **Token Budget Exceeded** - One efficiency test failed due to Layer 3 fallback (1600 tokens)
2. **Complex Query Handling** - Could benefit from more aggressive early token estimation

## 📝 Recommendations

1. Add token budget warning before Layer 3 fallback
2. Consider caching frequently accessed DOMAINS.md entries
3. Test with larger real-world codebases to validate scalability

## 🔬 Sample Output Comparison

### With Skill (eval-1)
```
## 🔍 架构搜索结果

**查询**: 搜索认证功能在哪里实现的
**搜索层级**: Layer 1
**匹配置信度**: 高

### 📄 相关文档
| 文档 | 相关度 | 关键内容 |
|------|--------|----------|
| `mobile/docs/architecture/security.md` | ⭐⭐⭐ | Mobile App 认证与安全架构 |

### Token 使用: ~320 tokens
```

### Without Skill (baseline)
```
Traditional Search Method Evaluation
=== Search Method 1: Grep for '认证' ===
...
=== Token Usage: ~2500 tokens ===
```

## 📊 Comparison: commit-msg-generator vs arch-search

| Metric | commit-msg-generator | arch-search |
|--------|---------------------|-------------|
| Pass Rate (with skill) | 100% | 93% |
| Improvement vs baseline | +87% | +40% |
| Primary Benefit | Format compliance | Token efficiency |

**Note**: arch-search shows lower improvement percentage because baseline already found some results. The key value is in token savings (75% average).

---

**Next Steps**:
1. ✅ commit-msg-generator: Benchmark complete (100% pass rate)
2. ✅ arch-search: Benchmark complete (93% pass rate)
3. 🔜 Recommended: Test state-scanner, branch-manager, task-planner skills
