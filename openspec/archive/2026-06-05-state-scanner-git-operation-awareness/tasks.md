# Tasks — state-scanner-git-operation-awareness

> Spec: `state-scanner-git-operation-awareness` (Level 2)
> Target: `aria/skills/state-scanner` → v1.39.0
> 依赖链: TG-A → TG-B → TG-C(后者消费前者输出)
> Rev1 (post_spec R1): OQ 全收敛;补 A1 路径解析 / A5 多标记+worktree / B 落点明确 / C4·C5 文档同步 / AC 写实
> 路径约定: 本文档简写 `collectors/git.py` = 实际 `aria/skills/state-scanner/scripts/collectors/git.py`(R2 code-reviewer note);测试在 `scripts/tests/`

## TG-A — git.py 采集 `git_operation_in_progress`

- [x] **A1** `collectors/git.py` 加 `_detect_git_operation(project_root) -> dict`:
  - 取 git dir = `git rev-parse --git-dir`,**显式解析**:`git_dir = Path(raw) if Path(raw).is_absolute() else (project_root / raw)`(superproject 返回相对 `.git`,不得依赖 CWD)
  - 检测 `git_dir` 下:`rebase-merge/`·`rebase-apply/`(→rebase)·`MERGE_HEAD`(→merge)·`CHERRY_PICK_HEAD`(→cherry_pick)·`REVERT_HEAD`(→revert)·`BISECT_LOG`(→bisect);否则 none
  - 优先级 rebase>merge>cherry_pick>revert>bisect,多标记取最高
- [x] **A2** `has_conflicts`:**仅** `operation != none` 才跑 `git diff --diff-filter=U --name-only`,非空→true;none 时直接 false 不发 subprocess(OQ4)
- [x] **A3** `detail`:best-effort 取 rebase head-name/onto 等,失败 null
- [x] **A4** fail-soft:git-dir 解析失败 / 读取异常 → `operation:"none"` + `r.soft_error(...)`,不阻断其余 git 采集;`collect_git_state` data 加 `git_operation_in_progress` 字段 + 更新 docstring output shape
- [x] **A5** 单测 `tests/test_git_operation_detection.py`,临时 git repo fixture,**必含以下 case 且断言确切枚举值**:
  - 各单一标记 → 对应 operation(rebase-merge→rebase / rebase-apply→rebase / MERGE_HEAD→merge / CHERRY_PICK_HEAD→cherry_pick / REVERT_HEAD→revert / BISECT_LOG→bisect)
  - **多标记组合断言优先级**:`rebase-merge/`+`MERGE_HEAD` → `operation=="rebase"`;`MERGE_HEAD`+`CHERRY_PICK_HEAD` → `operation=="merge"`
  - **worktree 场景**(qa minor + #139 关联):`git worktree add` 后在 worktree git dir(`.git/worktrees/<name>/`)放 rebase-merge 标记,断言从 worktree CWD 跑 `_detect_git_operation` 报 rebase(验证 git-dir 解析正确)
  - 冲突 vs 无冲突:`has_conflicts` true/false 各一例
  - none / fail-soft(git-dir 解析失败模拟)

## TG-B — 阶段 2 消费(OQ1=b,三落点)

- [x] **B1** collector 字段已由 TG-A 产出(`git.git_operation_in_progress.operation`),**不**改写 `interrupt.status`(正交)
- [x] **B2** `RECOMMENDATION_RULES.md` 新增降级规则行:消费 `git_operation_in_progress.operation != "none"` → 降级/阻止含 checkout·分支操作的常规推荐,引导先 `git <op> --continue`/`--abort`;`has_conflicts=true` 措辞升级;定具体 priority(中断恢复类附近)
- [x] **B3** `SKILL.md` 阶段 0 + `references/recommendation-stages.md` prose:阶段 2 入口断言读该字段、非 none 行为(warning+降级)、与 interrupt.status 正交说明
- [x] **B4** 测试:RECOMMENDATION_RULES.md 新规则的**结构性存在性测试**(规则行存在 + 触发条件字段引用 `git_operation_in_progress.operation`);**(R2 qa 非阻塞建议)**低成本补:断言规则条目含 `has_conflicts=true` 措辞升级字段引用;推荐降级的 AI 行为由 C3 dogfood 验证(prose 无机械 gate)

## TG-C — schema + 文档同步(Rule #3)

- [x] **C1** `references/state-snapshot-schema.md` 记录 `git_operation_in_progress` 字段(SOT);明确 `snapshot_schema_version` **保持 "1.0" 不 bump**(OQ3:nested optional additive)
- [x] **C2** `SKILL.md` 阶段 0 描述补 git-operation 感知(与 B3 同处)
- [x] **C4** `references/interrupt-recovery.md` 决策树补 git 层并行感知分支 + "两路信号正交、互不篡改"边界(R1 km major #1)
- [x] **C5** `references/phase-1-collectors.md` collector 表 Phase 1 `git` 行注明新增 `git_operation_in_progress` 子字段(additive, v1.39.0+)
- [x] **C3** dogfood:临时真 rebase 态跑 `scan.py`,确认 exit + snapshot 暴露 git 操作 + 阶段 2 警示/降级(复算 triage case-1 → 满足 AC-5)

## 收尾(Phase C/D)

- [x] **D1** 5+1 SOT bump v1.38.0 → v1.39.0(plugin.json / marketplace.json ×2 / VERSION / README.md+README.zh.md / CHANGELOG.md + 主仓 VERSION 插件记录)
- [x] **D2** 全量测试零回归 + Phase C 双远程 parity + 主仓 gitlink bump
- [x] **D3** 关 #135(POST comment + PATCH state)+ 归档 Spec + handoff(若触发 Rule #9)

## 验收 (AC)

- **AC-1**: rebase/merge/cherry_pick/revert/bisect 暂停态下 `scan.py` snapshot `git.git_operation_in_progress.operation` 准确报对应值(triage case-1 复现场景由报 none 变为报 rebase)
- **AC-2**(写实,可机械验证 — R1 qa major):
  - (a) `git_operation_in_progress.operation != "none"` 时,阶段 2 推荐**不含** checkout·新分支类常规推荐规则(由 B4 结构性测试 + C3 dogfood 验证规则触发);
  - (b) 警示载体明确:snapshot 暴露 `git_operation_in_progress`(非 null/非 none)字段,阶段 2 prose 据此渲染 warning。
- **AC-3**(写实 — R1 qa minor): clean 仓库下 `git_operation_in_progress == {"operation":"none","has_conflicts":false,"detail":null}` 字段**存在且为 none 形态**(非仅"不崩溃"),其余 snapshot 行为与 v1.38.0 完全一致
- **AC-4**: 新单测全绿 + 现有 state-scanner 测试零回归
- **AC-5**(dogfood 臂闭环 — R1 qa info): C3 dogfood 在真 rebase 中间态实测 `scan.py` snapshot 报 rebase + 阶段 2 给出降级警示(Rule #6 substitute 的 dogfood 臂在验收矩阵显式闭环)
