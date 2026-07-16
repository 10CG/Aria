# post_spec R7 + R8 (trail) — state-scanner-snapshot-stderr-secret-leak

> **轮次**: R7 + R8 (均单聚焦 code-grounded confirm 轮; 承 R6 3-agent 聚合)
> **日期**: 2026-07-15
> **对象**: `openspec/changes/state-scanner-snapshot-stderr-secret-leak/proposal.md`
> **收尾裁定**: owner meta 裁定 **option B (AC-2 重框 best-effort)** → **v5**, 退出 sound-AC-2 审计循环

## 轮次链

| 轮 | verdict | 关键 finding | 折入版本 |
|----|---------|-------------|---------|
| R6 (3-agent) | PASS-with-fixes 1C+4M+5m | C1 AC-2 name-grep 不 sound (3/9) | v3 (option A 结构级: 类型化通道) |
| R7 (单聚焦) | PASS-with-fixes **1C fix-introduced** +2M+2m | v3 AC-2 `.stderr` grep 建在不存在的数据流 (0/9); M-1 白名单窄; M-2 M-b/AC-4 矛盾 | v4 (`_run` 第三返回值污点追踪 + 委托) |
| R8 (单聚焦) | PASS-with-fixes **1C fix-introduced** +3M+1m | v4 `_run` 第三返回值 intra-procedural 漏 M-a 自己的跨函数逃逸; Major multi_remote/整包 return/benign 刻画 | v5 (option B: 助手内部自分类 + AC-2 best-effort) |

## Meta 观察 (驱动 option B)

连续三轮 fix-introduced Critical **全集中在同一处**: 把 AC-2 做成**可证明 sound 的全目录静态检查**。演化: v2 name-grep 命中 3/9 → v3 `.stderr` grep 命中 0/9 (真代码元组解包无属性访问) → v4 `_run` 第三返回值 intra-procedural 漏跨函数逃逸 (恰是本 spec M-a 自己让 stderr 经 return 逃逸)。**根因**: AC-2 被要求当"完整性权威闸"("清单可能不全但 AC-2 兜住"), 而"无原始 stderr 到达 snapshot"的 sound 静态判定极难精确规约。memory `feedback_selfreferential_antifalsegreen_plan_needs_more_audit_rounds` 实证。

## owner option B 裁定 (2026-07-15)

- **真正的结构级保证 = GitErrorClass 类型化通道本身** (返回类型无 stderr 字段, 凡经它 stderr 结构上到不了 snapshot)。
- **AC-2 降为 best-effort lint** (只扫本 spec 改动的 in-scope 文件 intra-procedural + known-bad grep), **完整性靠 refactor 被 code-review** (Task 3.1b), 非 AC-2 可证 sound。
- **退出 sound-AC-2 审计循环** —— 不跑 R9; 以"类型化通道即保证"为基础 sign off。

## R8 C-1 干净解 (v5 采纳, 两路都需要)

M-a 助手改**内部自分类** (取代 v3/v4 的"助手 return (rc,stderr) 到 callsite 再分类"):
```
if rc:
    if benign(stderr): return [], None
    else: return [], classify_git_error(rc, stderr, cmd)   # 返回 label, 非裸 stderr
```
stderr + benign-gate 全留助手内 → stderr 不跨函数逃逸 → (1) intra-procedural, best-effort lint 单文件可确认; (2) 消解"benign-skip 搬 callsite"; (3) 消解多跳盲区 (`:332` `ls_err` 变 label)。

## R8 正向确认 (code-grounded)

- R7 C-1 属实: 全目录 `.stderr` 属性访问只 2 处 (都在 `_common.py:338/366` `_run` 内部), 零 callsite 属性访问, callsite 全用三名位置解包无 `*rest`/`[2]`。
- 结构概念 (GitErrorClass 类型层消灭 stderr) sound; §2 泄露站点清单实为完整 (67 处 soft_error 普查交叉核对无漏)。
- 委托 (M-2) 可行不破测试 (但 R8 minor-1 勘误: `test_p1_layer_h.py:446` 是手搓 fixture 不 call `_classify_error`, "不破"更弱)。

## v5 已知局限 (option B 有意接受)

- AC-2 best-effort lint 不覆盖: `return _run(...)` 整包逃逸 (`issue_scan.py:461/466`, out-of-scope 已枚举不泄) + out-of-scope 结构化 collector (`multi_remote.py:253-266` reason-label)。记为已知盲区 (R8 Major-1/3), 不泄 stderr 故可接受。
- 完整性权威闸 = Task 3.1b code-review, 非 AC-2。

**相关真 file:line**: `_common.py:314-366` (`_run`) / `handoff_multibranch.py:146/195/198/233/298/332/352` / `handoff_worktrees.py:138-140/348` / `multi_remote.py:253-266` / `issue_scan.py:461/466` / `coordination_fetch.py:114/235-268` / `test_p1_layer_h.py:435-446`。
