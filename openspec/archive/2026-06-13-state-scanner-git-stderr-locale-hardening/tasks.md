# Tasks — state-scanner-git-stderr-locale-hardening

> ✅ **SHIPPED 2026-06-13** (aria-plugin v1.46.1, `528d4af`). #143 fixed + #142 wont-fix 收口。

## TG-A — `_run` 注入 `LC_ALL=C` ✅
- [x] A1. `collectors/_common.py::_run` 加 `env={**os.environ, "LC_ALL": "C"}` (drop LANG=C); 保留 6 既有 kwarg。
- [x] A2. 不改任何 collector 匹配逻辑; custom_checks.py:320 独立 subprocess 确认不在范围。

## TG-B — 测试 ✅
- [x] B1. env 断言单测 (`mock.patch("collectors._common.subprocess.run")` 捕获 env kwarg, LC_ALL=C + os.environ superset + 6 kwarg; host-locale-agnostic 可证伪)。
- [x] B3. CJK 直通真测 (实际 `git log --oneline` 路径, 隔离 tmpdir, 含 CJK+emoji+箭头全 subject 断言 [M-1 加固])。
- [x] B4. 全套件 `python3 tests/run_tests.py` 805 全绿 (modulo 已知 timing flake); 138 git-解析 collector 测试 under LC_ALL=C 零回归。
- [~] B2. (可选) 非英文 locale 集成 — B1 mock 已 host-locale-agnostic 证伪, 集成测试未单独加 (B1 充分)。

## TG-C — 文档同步 ✅
- [x] C1. `_common.py::_run` docstring: LC_ALL=C + 与 #61 正交 + LANG 冗余。
- [x] C2. `coordination_fetch.py::_is_benign_coordination_absent` docstring: 英文假设 → LC_ALL=C 强制保证; absent-vs-hidden → #142 wont-fix。
- [x] C3. `references/state-snapshot-schema.md` coordination_fetch benign 闸注记同步。

## Phase C/D ✅
- [x] D1. aria submodule: 分支 → commit `3a77118` → PR #83 merge `2976dc3` → 双远程 parity。
- [x] D2. 主仓 gitlink → `528d4af` + 5 SOT v1.46.1 + CHANGELOG (release `528d4af`)。
- [x] D3. close #143 (fixed, comment-12811) + #142 (wont-fix, comment-12815); 归档 Spec。

## #142 wont-fix 收口 ✅
- [x] W1. #142 POST wont-fix comment (git 协议不可解 ls-remote rc=2 覆盖 absent+hidden + ls-remote decline + auth-masked documented-limitation + locale 由 #143 解) + PATCH state=closed。
