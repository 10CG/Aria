# Commit Message Generator Output

## Generated Commit Message

```
fix(llm): disable stream mode for Kimi/Doubao and resolve provider priority conflicts

- add stream: false to Kimi provider chat() to prevent incomplete JSON responses
- apply same stream: false fix to Doubao provider chat()
- resolve default priority conflicts in config.ts (GLM=1, Qwen=2, Kimi=3, Doubao=4)

Kimi API returns malformed JSON when streaming is enabled, causing parse
failures downstream. Doubao exhibits the same behavior. Priority values
were previously duplicated across providers, leading to nondeterministic
provider selection order.
```

## Analysis

### Type: `fix`
All three changes address existing bugs -- stream mode producing broken responses and duplicate priority values causing unpredictable behavior.

### Scope: `llm`
All modified files reside under `src/core/llm/` (providers + config), making `llm` the appropriate scope.

### Files Changed
| File | Change |
|------|--------|
| `src/core/llm/providers/kimi.ts` | Added `stream: false` to `chat()` method |
| `src/core/llm/providers/doubao.ts` | Added `stream: false` to `chat()` method |
| `src/core/llm/config.ts` | Fixed duplicate priority values for 4 providers |

### Decision Notes
- Combined into a single commit because all changes fix LLM provider reliability issues and are logically cohesive.
- Used `llm` scope rather than listing individual providers, since the fix spans the provider subsystem.
- Subject line is imperative mood, lowercase, no trailing period, under 72 characters.
- Body explains both the "what" (bullet points) and the "why" (paragraph).
