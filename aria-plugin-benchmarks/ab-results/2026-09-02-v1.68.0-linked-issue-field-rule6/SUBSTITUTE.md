# SUBSTITUTE 留痕 — Rule #6 判据表第一行 (描述性 / 不改 AI 行为面 hunk) 的 baseline-failing 结构化测试证据 (Spec linked-issue-field-availability TASK-019)

> 适用 hunk: SOT 模板 `standards/openspec/templates/proposal-minimal.md` (SC-6) · 探针 `scripts/linked_issue_field_probe.py` (SC-4 / SC-5 / SC-9) · 注册 `.aria/state-checks.yaml` (SC-8) · 纯函数 `lib/linked_issue_field.py` (SC-1~4, SC-9)。
> 处方 = 同一测试文件在**基线 worktree 上红、实现后绿**; 命令与输出逐字, 2026-09-02 执行容器 simonfish/023236f2。

## 1. 基线红 (aria `d69091d` = v1.67.2, 独立 worktree, 只复制测试文件进去)

```
$ git -C aria worktree add -q --detach <scratch>/aria-base d69091d
worktree @ d69091d
$ cp aria/skills/state-scanner/tests/test_linked_issue_field.py <scratch>/aria-base/skills/state-scanner/tests/
$ cd <scratch>/aria-base/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
  File "/usr/lib/python3.11/unittest/loader.py", line 407, in _find_test_path
    module = self._get_module_from_name(name)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/unittest/loader.py", line 350, in _get_module_from_name
    __import__(name)
  File "/tmp/claude-1000/-home-dev-Aria/94994160-11fa-4759-806c-602e16b505fe/scratchpad/aria-base/skills/state-scanner/tests/test_linked_issue_field.py", line 62, in <module>
    from lib.linked_issue_field import (  # noqa: E402
ModuleNotFoundError: No module named 'lib.linked_issue_field'
----------------------------------------------------------------------
Ran 1 test in 0.000s
FAILED (errors=1)
BASELINE_EXIT=1
$ ls <scratch>/aria-base/skills/state-scanner/scripts/linked_issue_field_probe.py <scratch>/aria-base/skills/state-scanner/lib/linked_issue_field.py
ls: cannot access '.../scripts/linked_issue_field_probe.py': No such file or directory
ls: cannot access '.../lib/linked_issue_field.py': No such file or directory
$ git -C aria worktree remove --force <scratch>/aria-base && git -C aria worktree list
/home/dev/Aria/.git/modules/aria  d69091d [feature/linked-issue-field-availability]      # 无残留
```

**红因 (逐 SC)**: 模块顶部 `from lib.linked_issue_field import …` ⇒ `ModuleNotFoundError` ⇒ 整个测试模块 ERROR ⇒ SC-1 / SC-2 / SC-3 / SC-4 / SC-5 / SC-6 / SC-7a / SC-8 / SC-9 与坏实现矩阵 全部不可达 = 红。基线上 SC-5 / SC-9 的被测脚本亦不存在 (`ls` 两行); SC-6 / SC-7a / SC-8 的被测文本在基线也是 0 命中 (proposal SC 表「baseline 必红」列的三处 `grep = 0` 实读: 模板 @ standards 334c609 / spec-drafter @ d69091d / state-checks.yaml @ c120f9e 无该条目)。

## 2. 实现后绿 (feature/linked-issue-field-availability; 主仓布局, SC-6 / SC-8 为真 OK 非 skip)

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
................................................
----------------------------------------------------------------------
Ran 48 tests in 1.627s

OK
$ cd aria/skills/state-scanner/tests && python3 run_tests.py            # 全量
Ran 1457 tests in 58.354s

OK
$ grep -rh '^\s*def test_' aria/skills/state-scanner/tests/*.py | wc -l
1473                                                                   # = 基线 1425 + 新增 48 (静态定义计数; 与 Ran 1457 差 16 = test_collision.py 16 个 pytest 风格裸函数不被 unittest 收集, 本 PR 前已存在)
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt; echo EXIT=$?
OK (9 份在范围内, 6 条在册)
EXIT=0
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | od -c | head -2
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4
0000015
```

## 3. 逐 hunk 处置表 (与 RESULT.md 共用; Rule #6 判据表五格)

| hunk | 判据表落格 | 处置 | 证据 |
|---|---|---|---|
| `spec-drafter/SKILL.md` hunk A + hunk B | 处方性·运行时指令面 | **照跑 AB** (`ab-suite/spec-drafter.json` 全部 3 eval, 每 eval 两臂各 1 run) | RESULT.md §1 |
| 同 hunk 的新增 authoring 行为「新建 proposal 必须写出该字段」 | 处方性·套件覆盖外 | 三件套: 点名行为 SC-7 ✓ / 定向 fixture = eval id 3 (中文臂) + eval id 2 更新 (英文臂) ✓ / 套件缺口 issue = aria-plugin#117 归并评论 ✓ | RESULT.md §2 + §3 |
| `standards/openspec/templates/proposal-minimal.md` | 描述性 (schema / 字段) | **substitute = SC-6** | 本文 §1 红 / §2 绿 (`test_sc6_template_field_and_usage_note_and_reference` OK) |
| `scripts/linked_issue_field_probe.py` (新建) | 确定性 Python, 不进任何 SKILL.md / frontmatter (与同目录两条既有探针同性质) | **substitute = SC-4 / SC-5 / SC-9** | 本文 §1 红 / §2 绿 |
| `.aria/state-checks.yaml` 注册 | 机械读取的 opt-in 数据, 非 AI 指令 (`state-scanner/SKILL.md` 零改动, `git diff` 为空) | **substitute = SC-8** | 本文 §1 红 / §2 绿 (`test_sc8_registered_and_runnable` OK) |
| `lib/linked_issue_field.py` (新建) | 确定性 Python | **substitute = SC-1~4 + SC-9 + 13 个坏实现拒绝矩阵** | 本文 §1 红 / §2 绿 |

**不申请豁免**: 上表五格全部有对应证据; hunk A/B 照跑而非 substitute。
