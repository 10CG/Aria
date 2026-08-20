---
round: R1
checkpoint: post_spec
spec: subprocess-decode-hardening
seats: [A1-backend-architect, A2-qa-engineer, A3-code-reviewer]
verdicts: {A1: REVISE, A2: REVISE, A3: REVISE}
converged: false
totals: {critical: 1, major: 8, minor: 7}
dedup_substantive: 9
timestamp: 2026-08-20T02:15:00Z
---

# post_spec R1 聚合 — subprocess-decode-hardening (aria-plugin#147)

三席一致 REVISE。**方案本体 (B/B′ + 16 处迁移目标) 三席均未动摇**; A3 独立重写普查脚本复现全部机械数字 (25/46/16/12/4/1/30), B′ 四条技术断言三席/两席各自实测复现。修复面 = 语料语义口径 + SC 可操作性。

## 去重后实质点 (9 条) 与处置

| # | 来源 | 内容 | v2 处置 |
|---|------|------|---------|
| 1 | A1-m1 = A2-M1 = A3-M1 (+A3-m2) | `coordination_ref.py:255` 带 `errors="replace"` 结构安全, census 漏查 `errors=`/`encoding=` kwarg 轴; `_common.py:406` 真防线同为 errors= 非 except 元组 | §Why 语料表重分层; census 方法论补 kwarg 轴; 新增 SC-9 (census 脚本入库+kwarg 轴) |
| 2 | A3-M2 + A3-M3 | 4 处 (custom_checks:342 / spec_complete:863,874 / triage _common:39) 被调用链顶层 `except Exception` 兜住 → 真实行为是降级 (EXIT_INTERNAL_BUG / EXIT_HARD_FAIL) 非未捕获崩溃 | §Why 分层: 真穿透 7 / 顶层兜住但整流程报废 4 / errors= 结构安全 1 / except 接得住 4 |
| 3 | A2-C1 | SC-4 第二条 sink 链 (文件写) 在 16 目标内无可达路径; verify_post_push 链描述与代码不符 (dumps 默认 ensure_ascii=True 不炸) | SC-4 重写: 仅保留 A2 实追验证的链 aether:150/173 → pre_merge_gate:495/518 → :568 `json.dumps(ensure_ascii=False)`; 并入「fixture 前须静态调用链引用」规则 |
| 4 | A1-M1 | 条目 5(b) docstring 改法会与 pre_merge_gate 自身实现 (surrogateescape+_sanitize_for_json, 不在迁移范围) 矛盾 | 5(b) 重写: 保留其局部机制描述 + 加指向全局约定的 cross-ref; 声明全局约定不要求重写既有结构安全实现 |
| 5 | A1-M2 | 结构检查扫描范围是允许清单非全分割, 新目录静默逃逸 | 谓词反转: 默认全含 aria/**/*.py, 显式排除 tests (结构上不可逃逸) |
| 6 | A2-M2 | SC-3 「对基线树跑」无可执行口径, #181 先例不覆盖三态 | 写死机制: `git -C aria archive 3b97c35 \| tar -x` 到隔离 tmpdir |
| 7 | A2-M3 | SC-6 跨树匹配键未定, file:line 会被行号漂移打破 | 改 per-file except 元组成员集合 multiset 相等 |
| 8 | A1-m2 / A1-m3 / A2-m1 | helper 粒度未定 / SC-8 无 spec 层默认 / SC-5 基线计数未锚冻结快照 | 文件级去重 / 默认 spawn 裸抛+注释 (A.2 可推翻须记理由) / 锚定 3b97c35 |
| 9 | A2-m2 | 30 测试点仅核 7 文件 | R1 后主 loop 机械补验 12/12 文件 30/30 点全部本地 fixture (ext 迹象零命中), 闭合 |

## 收敛判定

R1 三席 REVISE → 按 convergence 模式落 v2 修订后进 R2。L2 基线预期 2 轮。
