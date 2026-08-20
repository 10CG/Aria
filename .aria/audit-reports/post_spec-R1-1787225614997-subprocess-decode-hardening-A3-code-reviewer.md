---
seat: A3-code-reviewer
round: R1
checkpoint: post_spec
spec: subprocess-decode-hardening
verdict: REVISE
critical_count: 0
major_count: 3
minor_count: 2
timestamp: 2026-08-20T00:00:00Z
---

# post_spec R1 — A3 code-reviewer (spec 与真代码一致性核验席)

审计对象: `openspec/changes/subprocess-decode-hardening/proposal.md` (aria-plugin#147)
基线核验环境: aria submodule HEAD = `3b97c35c45f45ffbdb472658d002e8859545f9ed` (与 spec 冻结 SHA 一致), 工作树干净 → 直接对工作树核验即对冻结快照核验。
方法: 独立重写 AST 普查脚本重跑 (ast.walk 找 `text=True`/`universal_newlines=True` 常量实参 + 逐层枚举词法 enclosing except) + 12+4 处逐文件人工打开核对 + 跨函数调用者追溯 (census 方法声明的盲区补查)。

## 结论

**verdict: REVISE** (0 Critical / 3 Major / 2 Minor; 判据: ≥2 Major → REVISE)

机械数字面全部通过 (census 可完美复现, 16 处 file:line + except 元组 16/16 一致)。REVISE 的原因集中在**语料口径**: §Why 的「12 处接不住 ⇒ 未捕获崩溃」叙述, 经调用者层补查后对 12 处中 5 处不成立 (4 处上游入口有 `except Exception` 顶层守卫, 1 处结构上根本不可抛)。B 方案本身 (统一迁移 16 处 + 机械防再长) 不受影响, 修复面是叙述与语料标注, 不是方案重做。

## Findings

### Major

**[A3-M1] `state-scanner/lib/coordination_ref.py:255` 结构上不可抛 UnicodeDecodeError, 归入「12 接不住」口径错**
该调用带 `encoding="utf-8", errors="replace"` (aria/skills/state-scanner/lib/coordination_ref.py:260-261), 代码注释原文即 "never raise UnicodeDecodeError to the caller" (#61 修复)。census 的 AST 方法只匹配 `text=True` 实参、不看 `errors=` kwarg, 于是把一个已按 #61 加固过的点计入「解码异常从元组底下穿过...崩溃」的缺陷清单。该点作为**统一模式迁移对象**成立 (B 方案目标), 作为**可触发缺陷**不成立。修复: census/spec 对该点加特例标注; 若 SC 或 Why 以「12 处可崩溃」为前提, 改为 11 或分层表述。

**[A3-M2] state-scanner 三处 (custom_checks.py:342 / spec_complete.py:863 / spec_complete.py:874) 的调用者层已捕获 — scan.py 顶层 `except Exception`**
调用链: 三处均经 `build_snapshot` 到 `scan.py main()`, 而 scan.py:476-479 是 `try: build_snapshot(...) except Exception: log.exception(...); return EXIT_INTERNAL_BUG`。解码异常的真实进程行为 = 被捕获 + 整个 scan 降级为 EXIT_INTERNAL_BUG, **不是未捕获崩溃**。census 自己声明了「同文件词法嵌套」方法, 数据无假; 但 spec §Why「收集器...未捕获崩溃」的叙述超出了该方法能支撑的范围。注意修复价值仍然真实存在 (一个收集器的坏字节让整份 snapshot 报废, vs 迁移后单点降级可读), 建议把 Why 的卖点改写成这个更准确的形态。

**[A3-M3] issue-triage `collectors/_common.py:39` 的调用者层已捕获 — triage.py `except Exception`**
调用链: `_run` ← 5 个 collectors ← `build_triage_report` ← triage.py:315-323 `except Exception: log.exception(...); return EXIT_HARD_FAIL`。同 A3-M2: 该点解码异常的进程行为是捕获降级, 非未捕获崩溃。「12 接不住」口径同样对此点不成立。

### Minor

**[A3-m1] `state-scanner/lib/worktree_manager.py:117` 当前无生产调用方**
`_run` 只被本文件与 `lib/__init__.py` 导出面引用; 全仓 grep `create_worktree/remove_worktree/list_worktrees` 无 tests 外消费者 (collectors/handoff_worktrees.py 用的是自己独立的 `_list_worktrees` 实现)。「接不住」词法为真但该路径生产不可达。不影响迁移决定 (导出 API 属可达面), 建议语料注明, 避免叙述把它当活缺陷计数。

**[A3-m2] covered 点 `state-scanner/collectors/_common.py:406` 的「接得住」归因与 A3-M1 同源**
census 归 covered 的理由是 except 元组含 `UnicodeDecodeError`, 但真代码 (aria/skills/state-scanner/scripts/collectors/_common.py:406-440) 的真正防线是 `encoding="utf-8", errors="replace"`, 那个 handler 注释自云 "shouldn't fire"。分类结论碰巧对, 归因口径同样是「census 不看 errors= kwarg」。迁移该点时 (16 处之一) 注意保留 #61/#143 注释语义。

## 核验表

| # | 核验项 | 结果 |
|---|--------|------|
| 1 | 冻结 SHA `3b97c35` = submodule HEAD, 工作树干净 | PASS |
| 2 | census 总数字 (files=25 / sites=46 / prod=16 / uncovered=12 / test=30) 独立重跑 | PASS (逐项相等) |
| 3 | spec §Why 表数字 25/46/16/12/4/1/30 | PASS (与重跑一致; 26/27 初筛数字在 `.aria/triage-report-147.json` 中可定位) |
| 4 | 12 处 uncovered: file:line 处确为 subprocess.run + text=True | PASS 12/12 |
| 5 | 12 处 uncovered: except 元组与真代码逐处一致 | PASS 12/12 |
| 6 | 12 处「接不住 ⇒ 未捕获崩溃」判定 (含调用者层补查, 12/12 全追) | **FAIL 5/12** — 4 处上游 except Exception (M2/M3), 1 处 errors="replace" 不可抛 (M1); 7 处成立 (verify_post_push:65/89, aether:150/173, phase1_gate:240, validate_schema_doc:130, worktree_manager:117†) |
| 7 | 4 处 covered: file:line + except 元组 | PASS 4/4 (fetch_gate:68 `(TimeoutExpired)/(OSError, ValueError)` ✓; closeout_trigger:90 `Exception` ✓; identity:173 `Exception` ✓; ss/_common:406 含 `UnicodeDecodeError` ✓, 但见 m2) |
| 8 | `validate_schema_doc.py:130` 完全无 enclosing try (census 唯一 `<none>`) | PASS (调用者 main 仅 `except RuntimeError`, 解码异常穿透 ✓) |
| 9 | `pre_merge_gate.py:310` 先例主张 | PASS (行号精确: 310-312 即「轴复用...元组」docstring; 315-317 即「⛔ 不传 text=True」局部纪律, 与 spec 第 5(b) 条表述一致) |
| 10 | traps.md #4/#5 原文 (`references/pre-merge-gate-empirical-traps.md` §二 表内坑 4/5) | PASS (#4 issubclass 措辞一致; #5 确为「下游 json.dumps 时才炸」——spec 任务 4 勘正对象存在且原文如所引) |
| 11 | B′ 技术断言实测 (`issubclass(UnicodeDecodeError, OSError)=False`; surrogateescape 后 dumps 默认路径 OK / `ensure_ascii=False`+encode 抛 UnicodeEncodeError; backslashreplace 单步得 `\xff\xfe` 字面且 utf-8 可 encode) | PASS (4/4 实测复现, spec §What-2 三条论据全部成立) |

† worktree_manager:117 词法成立但无生产调用方 (m1)。

调用者层补查覆盖: 12/12 处全部追至进程入口 (超出席位要求的 ≥6)。

## 对修复方向的建议 (只审不改, 供 spec 作者参考)

1. §Why 把「12 接不住 ⇒ 未捕获崩溃”改为三层: 7 处真穿透崩溃 / 4 处被入口 `except Exception` 兜住但整流程报废 (EXIT_INTERNAL_BUG / EXIT_HARD_FAIL) / 1 处已 errors="replace" 结构安全 (仅统一模式迁移)。这比现叙述更强而不是更弱——「一个坏字节让整份 snapshot/triage 报告报废」是更准确的卖点。
2. census 文件补 caller-note 列 (或脚注声明词法口径的已知盲区), 满足「复核可重跑」时口径自明。
3. 迁移 coordination_ref:255 与 ss/_common:406 时保留 #61/#143 注释链 (encoding/locale 语义), 防止统一 helper 抹掉既有决策记录。
