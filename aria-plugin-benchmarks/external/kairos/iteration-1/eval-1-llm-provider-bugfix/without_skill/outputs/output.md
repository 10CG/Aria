# Commit Message Output

```
fix(llm): disable streaming for Kimi/Doubao and resolve provider priority conflicts

Kimi and Doubao APIs return incomplete JSON in stream mode, causing
parse failures. Added stream: false to chat() in both providers.
Also fixed default priority collisions across 4 providers
(GLM=1, Qwen=2, Kimi=3, Doubao=4) to ensure deterministic fallback
ordering.
```
