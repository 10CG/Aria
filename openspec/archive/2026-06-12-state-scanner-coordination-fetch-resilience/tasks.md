# Tasks — state-scanner-coordination-fetch-resilience

> ✅ **SHIPPED 2026-06-12** (aria-plugin v1.46.0, `e45ed3c`). 全 in-scope 任务完成; F1-F5 为 out-of-scope follow-up (新 issue, 不属本 cycle)。

## TG-A — coordination_fetch.py 拆两条 fetch (主 loop 亲自, 零回归核心) ✅

- [x] A1. `_branch_heads_refspec` / `COORDINATION_REF` 分离两路 refspec。
- [x] A2. 双 fetch: Fetch1 (分支头, 载重, 先跑) → Fetch1 失败短路 (`coordination_ref_present=None`)。
- [x] A3. Fetch2 benign 三重 AND 闸 (先于 `_classify_error`) → False 无 soft_error / rc==0 → True / 非 benign → None + `coordination_ref_fetch_failed`。
- [x] A4. `coordination_ref_present` 三态写入 cache payload + cache-hit/stale-serve 读回; pure-failure → None。
- [x] A5. success/degraded 重锚定 Fetch1; `refs_fetched` 只含实际成功 refspec; error_msg 不嵌 raw stderr; `_write_cache` OSError fail-soft。

## TG-B — 测试 (主 loop 亲自, 新建 test_coordination_fetch.py) ✅

- [x] B1. 新建 `tests/test_coordination_fetch.py` (mock `_run`, 隔离 tmpdir fixture)。
- [x] B2. 场景 (a)-(g) + benign 闸 4 单测 + legacy cache 兼容 = 12 测试。
- [x] B3. 全 state-scanner 套件 803 全绿 (1 已知预存 timing flake `test_two_consecutive_runs_diff_zero` 无关)。
- [x] B4. dogfood: no-coord sandbox (真 git) → success+present=False+无 error; Aria 自身 → present=True 零回归。

## TG-C — 文档同步 (Rule #3 docs-in-sync) ✅

- [x] C1. `references/state-snapshot-schema.md`: 新建 coordination_fetch section + 表行 + change history + benign 限制注记。
- [x] C2. `collectors/coordination_fetch.py` 模块 docstring: return schema + 双 fetch + benign 三重闸 + 短路 + 已知限制。
- [x] C3. `references/phase-1-collectors.md` L41: 重写为双 fetch 描述 (修双重 stale)。
- [x] C4. `docs/coordination-ref-schema.md`: 核查 = 仅 lib CRUD 无 collector 行为 → 无需改 (审计判定正确)。
- [x] C5. `normalize_snapshot.py`: coordination_ref_present 不进 DROP_KEYS 裁定注释 (None 由 null-drop 仍稳定)。

## Phase C/D ✅

- [x] D1. aria submodule: 分支 → commit `b29751f` → PR #82 merge `2d9bbb3` → 双远程 parity。
- [x] D2. 主仓 gitlink → `e45ed3c` + 5+1 SOT v1.46.0 + CHANGELOG (release `e45ed3c`)。
- [x] D3. close aria-plugin #75 (PR Closes) + Aria #141 (comment + PATCH state); 归档 Spec。

## follow-up (out-of-scope, 新 issue — 不属本 cycle 完成度)

- [ ] F1. `lib/coordination_ref.py::fetch_coordination_ref` benign 处理 (Layer L 路径, 低优)。
- [ ] F2. coordination_fetch 分支头载重耦合解耦 (架构, 低优)。
- [ ] F3. benign 闸 `git ls-remote --exit-code` 硬化 — 区分 "ref 真不存在" vs "ref 被 server ACL/hideRefs 隐藏" (code-review silent-failure #1)。
- [ ] F4. `_run` 注入 `LC_ALL=C` — 锁定 git stderr 英文输出 (跨切, 独立 change; code-review #2)。
- [ ] F5. `track_board.py` 补黄条 — coordination_ref_present=None + coordination_ref_fetch_failed 时渲染"协调数据可能陈旧" (render-side; code-review #5)。
