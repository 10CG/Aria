# post_spec R6 (aggregated) — state-scanner-snapshot-stderr-secret-leak

> **轮次**: R6 (Spec B 自身独立 post_spec 首个落盘聚合; R5 为内联 FAIL 无独立文件)
> **日期**: 2026-07-15
> **对象**: `openspec/changes/state-scanner-snapshot-stderr-secret-leak/proposal.md` (Draft v2)
> **模式**: 3-agent 对抗审计 (code-grounded, 实读 aria-plugin 真代码)
> **聚合裁决**: **PASS-with-fixes (含 1 Critical) — 未完全收敛, 需 v3 折入后签字**

## 三视角裁决

| 视角 | verdict | Critical | Major | minor |
|------|:---:|:---:|:---:|:---:|
| security-rule7 | PASS-with-fixes | 0 | 3 | 2 |
| silent-failure-correctness | PASS-with-fixes | 0 | 2 | 3 |
| spec-completeness | PASS-with-fixes | 1 | 1 | 3 |

`r5_reasons_fixed = [yes, yes, yes]` (spec-completeness 视角逐条验尸确认)。

## 正向确认 (三视角实读真代码一致)

- R5 三个 FAIL 原因 (词表互斥无裁定 / tasks 未跟正文 / 0-failed 假前提) **逐条真修**, 非自述糊弄。
- OQ-B1 (保留旧词表) / OQ-B2 (不合并 issue_scan) 两裁定 **load-bearing 正确**: `coordination_fetch.py:235-268` 的 `other` catch-all 返回 `f"git fetch failed with rc={rc}"`, 结构上不回传 stderr 原文; `issue_scan.py:311-326` 返回 ERR_ 枚举, 已 Rule#7-clean。
- AC-3 豁免 **合法非循环**: 母 spec `tasks.md:254` 真认领消除 `test_two_consecutive_runs_diff_zero`。
- 今天 **无活跃泄露**: 全部裸 stderr 站点 argv 无 remote URL (纯本地命令)。
- 枚举定义域完整, 对 Rule#7 **fail-CLOSED**; Level 2 定级站得住。

## 聚合 findings (按修复优先级)

### C1 (Critical) — AC-2 防复发 grep 不 sound, 只命中 9 处清单里的 3 处
- **三视角三角定位**: security-rule7 / silent-failure 各评 Major, spec-completeness 因 spec 拿 AC-2 当"完整性权威闸"(§2/§Why) 升为 Critical。
- pattern `soft_error(..., err` / `..., stderr` 命中: `sync.py:150` / `git.py:184` / `git.py:356`。
- **漏检** (都在 task 2.1 清单内): `handoff_multibranch.py:298`(`list_err`) / `:334`(`msg`) / `handoff_worktrees.py:348`(`enum_err`) / `sync.py:232`+`:244` (stderr 埋进 f-string `f"path=... err={err.strip()}"`, 变量名非 `err`/`stderr`)。
- **失败场景**: Phase B 作者写 `soft_error(kind, f"detail {err.strip()}")` 或先 `msg=f"...{stderr}"` 再传 → AC-2 零匹配绿通过, token 进 snapshot。防复发闸假绿。
- **修法**: AC-2 改 sound 检测 — 反向白名单 (断言 `soft_error` 第二实参只能是分类器调用结果/字面模板/`f"rc={rc}"` 已知安全形, AST/结构化) 或收窄 `soft_error(_common.py:309)` 签名使原始 stderr 从 API 不可达 (结构级, 贴合 §Why 野心, 见 memory `feedback_structural_antispoof_unreachable_not_safe_default`)。

### M-a (Major) — tasks 2.1 指向转发点而非 stderr 烘焙点
- task 2.1 列 `handoff_multibranch.py:298/334/354` + `handoff_worktrees.py:348` (转发点); 真烘焙点在助手 `handoff_multibranch.py:146/198/233` + `handoff_worktrees.py:140`。
- 照转发点行号改而助手仍拼原文 stderr = 修复无效。R5「tasks 未跟正文」的残留变体 (行号对不上污点源)。要真收口需助手返回 `(rc, stderr)` 再 callsite 分类。

### M-b (Major) — 提炼分类器 message 硬编码 "git fetch", 被 AC-4 锁死
- `coordination_fetch.py:242-268` detail 全含 "git fetch"; `test_p1_layer_h.py:446` 断言逐字 → AC-4 要求既有测试全绿即锁死此措辞。
- naive 提炼复用到 `git log`/`status`/`rev-list` → snapshot `errors[].detail = "git fetch network error"`, 排障者被指向错误子系统 (脱敏没丢 secret 却指错根因)。
- **修法**: spec 明确"提炼 (rc,stderr)→label 映射; human-readable detail 由各 callsite 用 (label, rc, 命令名) 现构; coordination_fetch 保留自己 fetch 措辞包装层"。AC-4 不破, 新站点不误报。

### M-c (Major) — multi_remote.py 第三套词表漏普查 + Impact 复用溢美
- §2b 称"既有两套 `_classify_error`", 漏 `multi_remote.py:255-266` 第三套 (`network_timeout`/`auth_failed`/`not_found`, 与 coordination_fetch 信号词不同)。multi_remote 恰是母 spec F3′ per-remote collector。
- 对本 spec Rule#7 攻击面无害 (multi_remote 落 `reason` 结构化字段非裸 stderr), 但 Impact"母 spec 直接复用同一分类器"是过度声称。
- **修法**: §2b 补 multi_remote 行; Impact 降级为"母 spec 需另裁 multi_remote 词表归一"。

### M-d (Major) — "结构上不可能承载 secret"措辞溢美
- §What.3 称结构级, 实际只加 docstring 契约 (task 2.2) + 顾问 grep (task 3.1), `soft_error` 签名 `detail: str` 未收窄。
- **修法**: 要么收窄签名 (与 C1 结构级修法合流, 首选), 要么措辞降级为"约定 + 机械检查"。

### minors (聚合)
- m1: `permission denied → auth_403` 误吞本地 FS 权限错 (三视角都提); 收紧为 `permission denied (publickey)` 或加 SSH 上下文守卫。
- m2: OQ-B2 理由第 1 条"下游已消费"核不实 (只被 issue_scan 自身测试消费); 应改挂"已发布 schema 字段 + kind 面暴露"。
- m3: AC-4"枚举标签集合不变"无指定机械断言载体 (无 fixture/task)。
- m4: §3b signal 扩充未证分支互斥+全覆盖分割不变量 (memory `feedback_predicate_tiers_need_total_partition_proof`); 风险低 (`other` catch-all fail-CLOSED) 但应补分割证明句。
- m5: 两套词表长期共存漂移风险, docstring 留痕是弱缓解 (可接受已知代价)。

## 收敛判据

R5 三根因真修 + 裁定 load-bearing 正确 + 无 design flaw, 但 C1 (AC-2 unsound) 是 load-bearing 完整性闸缺陷 → **本轮不判 PASS-converged**。修法明确且窄 (spec 措辞 + AC 收紧 + 首选 `soft_error` 签名结构级收窄), 折入 v3 后应收敛。建议 v3 折入 C1 + M-a~M-d + minors, 供 owner sign-off。

**关键 file:line (供 v3 + Phase B)**:
- 提炼源 (干净分类器): `coordination_fetch.py:235-268`
- 裸 stderr callsite (可直接分类): `git.py:184`, `git.py:356`, `sync.py:150`, `sync.py:232-235`, `sync.py:244-247`
- **stderr 烘焙点 (tasks 漏列的真 sanitize 位)**: `handoff_multibranch.py:146/198/233`, `handoff_worktrees.py:140`
- 签名 (未收窄): `_common.py:309`
- AC-4 措辞锁: `test_p1_layer_h.py:446`
- 安全对照 (无需改): `issue_scan.py:311`, `multi_remote.py:255-266`
