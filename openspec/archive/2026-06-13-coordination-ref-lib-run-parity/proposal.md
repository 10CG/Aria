# coordination-ref-lib-run-parity

> **Status**: ✅ **SHIPPED 2026-06-13** (aria-plugin **v1.46.3**, PR [#85](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/85) merge `0ccf42e` + release `82e0e75`; 主仓 gitlink → `82e0e75`)。post_spec R1 REVISE (2/3, 3 major: 测试落点太松) → Rev1 (TG-C 强制 lib-直测) → **R2 PASS 3/3 unanimous**。Phase B: TG-A/B/C + 7 lib-直测 (97 coordination 测试 + 818 全绿) + code-review PASS。F1 收口。
> **Rev1 (post_spec R1)**: 3 major 全为测试落点太松 (允许加 mock 路径绕过真代码) → **TG-C 强制 3 个 lib-直测** (env 断言 patch `lib.coordination_ref.subprocess.run` host-locale-agnostic + benign-absent 真打 fetch_coordination_ref + crash-safe errors=replace); TG-A "对齐"措辞收窄 (只加 #61/#143 两项, timeout/None-guard 属 F2-class 不在 scope, code-reviewer-m3); env merge **LC_ALL=C 末位非覆盖** (qa-m1); 保留 `import os as _os_run` (m5); benign ref_updated=False 语义 + health_check trace 锁定 (m2/qa-m2)。
> **Level**: 2 (Minimal — proposal + tasks)
> **Target skill**: `aria/skills/state-scanner` (aria-plugin), Layer L `lib/coordination_ref.py`
> **Target version**: v1.46.2 → **v1.46.3** (PATCH — consistency 硬化 + benign-absent, 无新能力)
> **Forgejo issue**: F1 (未开 issue — #141 code-review silent-failure-hunter M2 派生的 out-of-scope follow-up; 本 Spec 收口)
> **owner 决策 (2026-06-13)**: 验证 F1 真实可修但 opt-in (phase1_gate 默认关) 低可达; (b) 平行 _run 缺 #61/#143 是真实潜在崩溃隐患 → 选 "修 a+b 一致性"。

## Why

`lib/coordination_ref.py` 是 Layer L 多终端协调的 ref CRUD 库 (init/read/write/push/fetch claims)。它有**自己的 `_run`** (L214-256), **独立于** `collectors/_common._run` —— 而 #61 (UTF-8 crash-safe) 与 #143 (LC_ALL=C locale) 两次 `_run` 加固**只改了 collectors 的那个**, 这个平行 _run 两者都没拿到。

### Problem (a) — `fetch_coordination_ref` 无 benign-absent (与 collector 修前同病)

`fetch_coordination_ref` (L1065-1163) 跑 `git fetch <remote> refs/aria/coordination:refs/aria/coordination`, 失败时分类 auth_failed / network / **else→`fetch_failed`** (L1141)。**无** "couldn't find remote ref"→benign 分支。coordination ref 不存在 (未发布) 被误判为 `fetch_failed`。

调用链: `phase1_gate` (急切认领闸门, **opt-in 默认关**) → collision → `health_check_fetch` (failure_handlers.py:606) → `fetch_coordination_ref`。fetch_failed → health_check 标 `partial_fetch=True`。**可达性低** (opt-in 默认关 + health_check 在 acquire_claim 写完 ref 之后跑 → benign-absent 罕见), impact graceful, 但与 #142 不同 (那是 git 不可解), 这是**可修的真实分类缺口**。

### Problem (b) — 平行 `_run` 缺 #61 + #143 加固 (真实潜在崩溃/locale 隐患)

`lib/coordination_ref.py::_run` (L214-256) 用 `subprocess.run(... text=True)` 但:
1. **无 `encoding="utf-8", errors="replace"`** (#61): `text=True` 用 locale 默认编码严格解码 → C-locale + 非 ASCII 协调内容 (claim YAML 含 owner 名 / notes 可能 CJK, 经 `git show refs/aria/coordination:<path>` L651 读) → **UnicodeDecodeError 崩溃** (try 只 catch FileNotFoundError/OSError, **不接** decode 错 → 传播)。这正是 #61 当初要防的崩溃, 在此 _run 上仍在。
2. **无 `env LC_ALL=C`** (#143): 非英文 git locale 下 `fetch_coordination_ref` 的 auth/network 英文 stderr 匹配 (+ (a) 新加的 benign 匹配) 失灵 → 误分类。

`_run` 被 **10+ coordination 操作** 共用 (L258/273/362/422/459/482/518/617/651/790: init/read/write/push/fetch/ls-tree/show) → blast-radius 广 (Level 2 + 全 coordination 测试验证)。

## What Changes

单一 Level 2 Spec, 三 task group (TG-A 代码 _run / TG-B benign / TG-C 强制 lib-直测)。

### TG-A — `lib/coordination_ref.py::_run` 加 #61 + #143 两项加固

- `subprocess.run(...)` 加 `encoding="utf-8", errors="replace"` (#61 crash-safe) + env 始终含 `LC_ALL=C` (#143 locale)。
- env 合并 (qa-m1, **LC_ALL=C 末位非覆盖**): `env = {**os.environ, **(extra_env or {}), "LC_ALL": "C"}` —— LC_ALL=C 放最后, **始终生效不可被 extra_env 覆盖** (我们永远要 C locale 出英文诊断; extra_env 仅 `GIT_INDEX_FILE` 正交 key)。保留 inline `import os as _os_run` (L233, code-reviewer-m5: 勿引 NameError)。
- 保留 `.strip()` 返回契约 + FileNotFoundError/OSError catch (UnicodeDecodeError 经 errors="replace" 不再 fire)。
- **scope 限定** (code-reviewer-m3, 收窄"对齐"措辞): **只加 #61/#143 两项**。collector `_run` 还有 `timeout=` + `TimeoutExpired→124` + `(p.stdout or "")` None 守卫 —— 这三项 lib `_run` 仍缺, 属 **F2-class 后续 (本 Spec 不做)**, 不声称"完全 parity"。
- **不 import collectors/_common._run** (layering: lib 低于 collectors 不可反向依赖) → 平行加固 + 注释互引同源。

### TG-B — `fetch_coordination_ref` 加 benign-absent (镜像 collector triple-AND)

- 现有 auth/network/else 分类**之前**加 benign 闸: `rc == 128 AND "couldn't find remote ref" in err_lower AND REF_NAME.lower() in err_lower` (REF_NAME=`"refs/aria/coordination"`, **lib 自己的常量**非 import collector 的 COORDINATION_REF; src:dst refspec 的 stderr 仍是 `couldn't find remote ref refs/aria/coordination` rc=128, code-reviewer 本地复现确认) → `return FetchResult(success=True, error_kind=None, error_msg=None, ref_updated=False)`。
- **health_check trace 锁定** (code-reviewer-m2/qa-m2): benign→success=True 跳过 Step4 partial_fetch; sha_before=="" (ref 从未存在) → Step5 regression 被 `sha_before and ...` 短路 → Step6 success=True/partial_fetch=False (test_ref_newly_appeared 已证此链路)。`ref_updated=False` 语义 = "无 ref 可更新" (与 "ref 存在未变" 同值, 双义); **当前无 caller 在 success=True 时 branch on ref_updated 区分二者** (backend-arch 确认), 故不加新字段; 在 docstring 注明此双义供未来 caller 知悉。
- 仅 `fetch_coordination_ref`; **不碰** `init_coordination_ref` 的 fetch (L422, ref absent 是 bootstrap 触发非 gap, 已正确处理=创建 orphan)。

### TG-C — 测试 (**强制 lib-直测, 非 mock 绕过**)

> post_spec R1 3 major 全因测试落点太松: 现有 test_failure_injection **mock 掉** fetch_coordination_ref/FetchResult (boundary mock), test_common 的 env 断言只打 **collector** 的 _run。lib 的 `_run` + `fetch_coordination_ref` 当前**零直测**。本 TG **MUST 新增 lib-直测** (打真实被改 code path, 非 mock fetch_coordination_ref/_run wholesale)。

- **C1 env 断言** (host-locale-agnostic 可证伪, 闭合 #143 教训 [[feedback_noop_in_test_env_hardening_needs_mechanism_assertion]]): patch **lib.coordination_ref 模块内的** `subprocess.run` (实施期按 test sys.path 解析确切模块名, 非 collectors) 捕获 `call_args.kwargs["env"]`, 断言 `env["LC_ALL"]=="C"` + `encoding=="utf-8"` + `errors=="replace"` + os.environ superset; **并测 extra_env 路径** (传 GIT_INDEX_FILE → env 含 GIT_INDEX_FILE **且** LC_ALL 仍 C)。
- **C2 benign-absent 真路径** (打 `fetch_coordination_ref` 本身, 仅 mock 其内部 _run 返回 rc/stderr): rc=128 + "couldn't find remote ref refs/aria/coordination" → 断言 `success=True, error_kind=None, ref_updated=False`; **converse**: rc=128 + 非 benign stderr (无 "couldn't find") → fetch_failed; rc=128 + benign 措辞但**别的 ref 名** → 非 benign (防绕闸)。
- **C3 crash-safe** (#61 落到此 _run): lib `_run` 喂非 UTF-8 字节 → 断言不抛 UnicodeDecodeError (errors="replace" 生效, 返回 U+FFFD)。
- **全 coordination 回归**: `python3 tests/run_tests.py` (canonical runner) 全绿 (test_failure_injection + test_reconcile_golden_table + 全套件; modulo 已知 timing flake)。

## Impact

- **Affected**: `lib/coordination_ref.py::_run` (TG-A) + `::fetch_coordination_ref` (TG-B) + **新增 lib-直测** (TG-C, 新 test 文件或 test_failure_injection 内**非-mock**类)。
- **向后兼容**: ✅ TG-A 正常 (UTF-8 + 英文/C-locale) 路径**无可观测变化** (encoding/errors 仅影响坏字节; LC_ALL=C 已 C-locale no-op); 非 ASCII 内容从"C-locale 崩溃"变 crash-safe, 非英文 locale 从误分类变可靠 = 纯修复。TG-B benign-absent: absent ref 从 fetch_failed 变 success → health_check 不再误标 partial_fetch (opt-in gate 内修复)。
- **Cross-cutting 安全**: 本地 _run 被 10+ coordination 操作共用 → TG-C 全 coordination 回归是硬闸。操作解析 rc / ASCII SHA·ref / UTF-8 claim YAML (git show blob byte-passthrough; LC_ALL=C 只改 git 诊断文本非 blob, backend-arch 确认) → LC_ALL=C 安全。
- **Rule #6**: deterministic lib → C1 env 断言 + C2 benign 真路径 + C3 crash-safe + 全 coordination 回归, 无 AB。
- **Versioning**: v1.46.2 → **v1.46.3** (PATCH)。consistency 硬化 + benign-absent 分类修复, 无新字段/能力/API。

## Out of scope

- **合并两个 _run** (lib 用 collectors/_common._run): layering inversion + 签名不同 → 平行加固不合并 (F2-class)。
- **lib _run 的 timeout / None-guard** (collector _run 有, lib 缺): F2-class 后续, 本 Spec 只加 #61/#143 (code-reviewer-m3)。
- **phase1_gate / health_check / reconcile 逻辑本身** + collector coordination_fetch (已 #141/#143 修)。

## Resolved (Rev1 — post_spec R1)

1. ~~benign-absent return success=True 正确?~~ → **是** (health_check trace 锁定: success→不标 partial_fetch; backend-arch+code-reviewer 经链路实证; ref_updated=False 双义 docstring 注明, 无 caller 受影响)。
2. ~~LC_ALL=C 与 extra_env 合并~~ → **LC_ALL=C 末位非覆盖** (`{**environ, **extra_env, "LC_ALL":"C"}`, 始终 C; GIT_INDEX_FILE 正交)。
3. ~~是否需 env 断言单测~~ → **MUST** (TG-C C1, host-locale-agnostic + extra_env 路径)。
