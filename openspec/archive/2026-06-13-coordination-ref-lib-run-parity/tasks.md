# Tasks — coordination-ref-lib-run-parity

> ✅ **SHIPPED 2026-06-13** (aria-plugin v1.46.3, `82e0e75`). F1 收口。

## TG-A — 本地 `_run` 加 #61 + #143 ✅
- [x] A1. `_run` subprocess.run 加 encoding=utf-8/errors=replace (#61) + env `{**os.environ, **(extra_env or {}), "LC_ALL": "C"}` (LC_ALL 末位非覆盖); 保留 inline import os。
- [x] A2. 保留 .strip() + catch; 注释互引 collector 同源 + timeout/None-guard 留 F2。

## TG-B — `fetch_coordination_ref` benign-absent ✅
- [x] B1. 分类前加 benign 闸 (rc==128 + couldn't-find-remote-ref + REF_NAME) → success=True/ref_updated=False。
- [x] B2. docstring 注明 ref_updated=False 双义; 仅 fetch_coordination_ref 不碰 init。

## TG-C — 强制 lib-直测 ✅
- [x] C1. env 断言 patch lib.coordination_ref.subprocess.run (LC_ALL=C + encoding + errors + superset + extra_env 共存)。
- [x] C2. benign-absent 真路径 (打 fetch_coordination_ref mock 内部 _run): benign + converse + wrong-ref + auth。
- [x] C3. crash-safe 真 subprocess 喂坏字节不抛 UnicodeDecodeError。
- [x] C4. 全 coordination 回归 (97 coordination 测试 + 818 全绿 via run_tests.py; modulo 已知 flake)。

## Phase C/D ✅
- [x] D1. aria submodule: 分支 → commit `84f582f` → PR #85 merge `0ccf42e` → 双远程 parity。
- [x] D2. 主仓 gitlink → `82e0e75` + 5 SOT v1.46.3 + CHANGELOG (release `82e0e75`)。
- [x] D3. 归档 Spec; 主仓 VERSION/CLAUDE.md 同步 v1.46.3。F1 无 issue (handoff 记收口)。

## F2 (out-of-scope, 派生)
- [ ] F2-extend. lib _run 与 collector _run 完全 parity (timeout / TimeoutExpired→124 / None-guard / FileNotFoundError rc 统一) + 考虑提取共享差异表防再次单边漂移 (code-review 建议)。
