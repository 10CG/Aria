# sc-baseline-linked-issue-normalization — 冻结存档报告 (TASK-025 路径 (b), owner 裁定 2026-08-23)

> **用途**: Rule #6 substitute 论证的承重证据 (proposal §rule6_note 第一行: collision.py / claim_schema.py docstring 走 substitute)。
> 本报告是**一次性冻结**: 对两个钉死的 SHA 各跑一次脚本, 原样记录输出。脚本本身已退役 (同目录 `.py`, 头部有退役注), 不再随 Spec / 代码演进; 复现须 `git -C aria worktree add <dir> <SHA>` 后对该 worktree 跑, 且 proposal.md 须取 `1205ec3`~本报告提交时的版本 (脚本从 proposal 现场解析 baseline 表)。

## 1. 基线 (实现前) — aria `9e6a17c` (v1.66.4), 主仓 proposal @ `a6cdeef`

命令: `python3 .aria/repro/sc-baseline-linked-issue-normalization.py <worktree@9e6a17c>/skills/state-scanner` → rc=0

```
SC      子用例      Spec 表   实测      一致?
------------------------------------------------
SC-1    6          红         红        OK
SC-1b   3          红         红        OK
SC-2    1          绿         绿        OK
SC-3    1          红         红        OK
SC-4    2          红         红        OK
SC-5    1          绿         绿        OK
SC-5b   3          红         红        OK
SC-5c   1          绿         绿        OK
SC-6    5          绿         绿        OK
SC-6b   9          绿         绿        OK
SC-9    1          绿         绿        OK
SC-10   1          绿         绿        OK
SC-11   2          红         红        OK
SC-13   2          红         红        OK
SC-14   2          绿         绿        OK
SC-15   2          红         红        OK

substitute 证据面 (实测红): ['SC-1', 'SC-11', 'SC-13', 'SC-15', 'SC-1b', 'SC-3', 'SC-4', 'SC-5b']
Spec 声称的证据面        : ['SC-1', 'SC-11', 'SC-13', 'SC-15', 'SC-1b', 'SC-3', 'SC-4', 'SC-5b']
证据面一致: YES

全部与 Spec 的 baseline 表一致 (SC-8c 另跑 pytest, 见 docstring)。
```

## 2. 实现后 — aria `880060d` (feature/linked-issue-normalization, 含 TASK-007..009)

同一脚本对实现后代码跑: 证据面 8 条 **全部转绿** (这正是路径一「落地后恒红」的形态 —— 脚本的职责是证明基线红, 不是回归测试; 回归由 `tests/test_release_by_track.py::TestLinkedIssueNormalizationSC` 承担)。

```
SC-14   2          绿         绿        OK
SC-15   2          红         绿        MISMATCH

substitute 证据面 (实测红): <空>
Spec 声称的证据面        : ['SC-1', 'SC-11', 'SC-13', 'SC-15', 'SC-1b', 'SC-3', 'SC-4', 'SC-5b']
证据面一致: NO

### 证据面不符 —— substitute 论证的承重集合与实测不一致
```

## 3. 结论

- substitute 证据面 = {SC-1, SC-1b, SC-3, SC-4, SC-5b, SC-11, SC-13, SC-15} 在基线上**实测红**, 与 Spec 声称一致 (16/16 格)。
- 实现后同 8 条转绿, 其余 8 条护栏保持绿 ⇒ 实现没有破坏任何 baseline-GREEN 断言。
- 脚本退役理由: 路径一 (落地后恒红) + 路径二 (Spec 归档后 proposal 路径失效 ⇒ FATAL) 两条失效面都不值得再维护一份 runner; 冻结报告 + SHA 即可复核。
