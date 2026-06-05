# state-scanner-git-operation-awareness

> **Status**: ✅ **SHIPPED 2026-06-05** (aria-plugin v1.39.0, PR #74 merge `49722ef` 双远程 parity; 主仓 gitlink → `49722ef`)。Phase A.2 CONVERGED 2026-06-04 (post_spec R1 REVISE/PWW → Rev1 → R2 全票 PASS 5/5)。Phase B full cycle: TG-A/B/C + 21 新测 (712 全绿零回归) + dogfood (复算 triage case-1) + Phase B.2 code-review PASS (Minor #1 已补)。Closes Forgejo Aria #135。
> **Level**: 2 (Minimal — proposal + tasks)
> **Target skill**: `aria/skills/state-scanner` (aria-plugin)
> **Target version**: v1.38.0 → **v1.39.0** (MINOR) / 主仓 gitlink bump
> **Forgejo issue**: [Aria #135](https://forgejo.10cg.pub/10CG/Aria/issues/135) — triage verdict `confirmed` / `major` / `next-cycle` (`.aria/triage-report.json`)
> **Rev1 (post_spec R1)**: 关 OQ1=(b)/OQ2=git-dir+join/OQ3=不 bump/OQ4=条件求值;补 TG-A 路径解析、TG-C 三文档同步(interrupt-recovery / phase-1-collectors / RECOMMENDATION_RULES)、写实 AC-2/AC-3 + AC-5 dogfood。

## Why

`/state-scanner` 是十步循环统一入口。其 **interrupt 检测**(阶段 0)目前**只感知 Aria 自己的 workflow 中断**(`.aria/workflow-state.json`),**完全不感知 git 层的 in-progress 操作**(rebase / merge / cherry-pick / revert / bisect)。

### Problem — 暂停中的 git 操作被误报为 `interrupt:none`

**dogfood 实证**(2026-05-31,#135 报告):一次 `/state-scanner` 时仓库实际处于**暂停中的 interactive rebase**(`.git/rebase-merge/` 存在,git status: "You are currently editing a commit while rebasing branch 'master'"),但 snapshot 报 `interrupt.status=none`。该 rebase 是 #133 混乱 ship session 遗留的废弃产物,orig-head `b8b9a7f` 甚至不在已 ship 的 master 历史里。

**根因**(已在 v1.38.0 代码核查 + 实测复现确认,triage 2/2):
- `collectors/interrupt.py` 仅读 `.aria/workflow-state.json`(L25-63;虽 import `_current_branch` 取分支名,但无 in-progress git 操作检测)。
- `collectors/git.py` `collect_git_state` 设 `detached_head`(L230)但**不区分**"普通 detached HEAD" vs "因 rebase 暂停而脱离" —— 实测在 rebase-暂停态 `git branch --show-current` 仍返回 `master`,`detached_head` 甚至为 `False`,连"detached"信号都没有。
- 代码全局 `grep` `rebase-merge|rebase-apply|MERGE_HEAD|CHERRY_PICK|REVERT_HEAD|BISECT` 零命中。
- 注:这些标记在 worktree / submodule 下不在字面 `.git/` 而在 gitfile 间接指向的真实 git dir(见 TG-A,故检测必须用 `git rev-parse --git-dir`,不硬编码 `.git`)。

### Impact(若不修)

- 阶段 2 推荐基于 `interrupt:none` 给出常规工作流推荐,**完全忽略 pending git 操作**。
- 若推荐含 checkout / 分支操作,可能 **abort / 破坏 rebase·merge 中间态**或产生混乱。
- 与 handoff 记录的 "rebase auto-merge dropped content" 类故障叠加时静默风险更高(#135 实证已与 #133 ship 混乱、v1.37.0 paper version bump 叠加)。

## What Changes

单一 Level 2 Spec,三 task group(同属 state-scanner skill,同文件面,链式依赖 TG-A→TG-B→TG-C)。

### TG-A — `git.py` 采集 `git_operation_in_progress`

- 在 `collectors/git.py` 加 `_detect_git_operation(project_root) -> dict`:
  - **取 git dir(OQ2 已定)**: `git rev-parse --git-dir`。返回值可能是**相对路径**(superproject 返回字面 `.git`,backend-architect 实测确认)或**绝对路径**(worktree / submodule gitfile 间接)。**必须显式解析**:`git_dir = Path(raw) if Path(raw).is_absolute() else (project_root / raw)`,**不得**依赖进程 CWD。
  - 检测 git dir 下标记:`rebase-merge/` 或 `rebase-apply/` → `rebase`;`MERGE_HEAD` → `merge`;`CHERRY_PICK_HEAD` → `cherry_pick`;`REVERT_HEAD` → `revert`;`BISECT_LOG` → `bisect`;否则 → `none`。
  - **优先级 / 检测顺序**(已定):`rebase > merge > cherry_pick > revert > bisect`,多标记并存(异常态,如中间态文件残留)取最高优先级并记 detail。
- 输出 additive 字段 `git_operation_in_progress`:
  ```
  {
    "operation": "none" | "rebase" | "merge" | "cherry_pick" | "revert" | "bisect",
    "has_conflicts": bool,   # 仅 operation != none 时计算 (OQ4 条件求值)
    "detail": str | null     # e.g. rebase head-name / onto (best-effort, 失败 null)
  }
  ```
- `has_conflicts`(OQ4 已定 = 条件求值):**仅当 `operation != "none"`** 才跑 `git diff --diff-filter=U --name-only`(非空 → true);`operation == "none"` 时直接 `false`,不发 subprocess(省常态开销)。
- fail-soft:`git rev-parse --git-dir` 失败或标记读取异常 → `operation:"none"` + `r.soft_error(...)`(遵 `_common.CollectorResult` 契约),不阻断其余 git 采集。

### TG-B — 阶段 2 消费 git 操作信号(OQ1 已定 = 方案 b,三落点)

> **OQ1 收敛(R1 tech-lead/code-reviewer)**: 方案 (a)「改写 `interrupt.status`」是**伪选项** —— 阶段 0/2 的 status 分支逻辑本身是 SKILL.md prose 而非可单测的 Python 路径,且改写 status 会**弱化 additive 契约**(篡改既有字段语义)。**采纳 (b)**:新增独立 collector 字段(TG-A,可单测)+ 阶段 2 prose 合成,二者与 `interrupt.status` **正交、互不篡改**。落点锁定为以下三处:

1. **collector 字段**(TG-A 产出,可单测): `git.git_operation_in_progress.operation`。
2. **`RECOMMENDATION_RULES.md` 新增降级规则行**(结构化、可做存在性测试): 规则消费 `git_operation_in_progress.operation != "none"` → 降级/阻止含 checkout·分支操作的常规推荐,引导先 `git <op> --continue` / `--abort`;`has_conflicts=true` 时措辞升级。优先级排在中断恢复类规则附近(实施时定具体 priority 值)。
3. **`SKILL.md` 阶段 0 + `references/recommendation-stages.md` prose**: 描述阶段 2 入口断言读该字段、非 none 时的 AI 行为(warning + 降级),与 `interrupt.status` 正交说明。

### TG-C — schema + 文档同步(Rule #3 docs-in-sync)

- **`snapshot_schema_version` 不 bump**(OQ3 已定): 依 `references/state-snapshot-schema.md §Versioning`,新增字段是 `git` 顶层下的 nested optional field(default absent),符合 additive-only 定义(先例:`git.status_clean` / `upm.followups` / `handoff.latest_source` 等均保持 `"1.0"`)→ **保持 `snapshot_schema_version="1.0"`,不 bump**。
- `references/state-snapshot-schema.md` 记录 `git_operation_in_progress` 新字段(source-of-truth)。
- `references/phase-1-collectors.md` collector 表 Phase 1 `git` 行注明新增子字段(additive, v1.39.0+)。
- `references/interrupt-recovery.md` 决策树补 git 层并行感知分支 + "两路信号正交、互不篡改"设计边界说明(major #1)。
- `RECOMMENDATION_RULES.md` 写入 TG-B 第 2 落点的新降级规则条目。
- `SKILL.md` 阶段 0 描述补 git-operation 感知。

## Impact

- **Affected**: `collectors/git.py`(TG-A)+ `RECOMMENDATION_RULES.md` / `SKILL.md` / `references/recommendation-stages.md`(TG-B)+ `references/state-snapshot-schema.md` / `references/phase-1-collectors.md` / `references/interrupt-recovery.md`(TG-C)+ tests。
- **向后兼容**: ✅ 纯 additive 字段(OQ1=b 保证不篡改 `interrupt.status`);`operation:"none"` 时行为与 v1.38.0 完全一致。
- **Downstream 安全**: additive-only —— 现有消费者不读新字段则行为不变;新增阶段 2 warning 仅在真有 pending git 操作时触发(罕见),不影响 clean 仓库常规路径。
- **Rule #6**(deterministic/structural skill substitute = structural fixture + unit tests + dogfood,per [[feedback_deterministic_structural_skill_rule6_substitute]]):TG-A = collector 单测(临时 git repo fixture 模拟各 `.git/*` 标记 + 多标记组合优先级 + worktree 场景 + 冲突态 + fail-soft);TG-B = RECOMMENDATION_RULES.md 新规则的**结构性存在性测试**(规则行存在 + 触发条件引用 `git_operation_in_progress.operation`)+ C3 dogfood 验证推荐降级(prose 行为无机械 gate,靠 dogfood 闭环);description 未改 → 无需 /skill-creator AB。
- **Versioning**: v1.38.0 → **v1.39.0**(MINOR);主仓 gitlink bump。

## Out of scope

- 自动 `--continue` / `--abort` 或任何**修改** git 状态的动作(本 Spec 只**检测 + 警示**,绝不代用户操作 git)。
- `.aria/workflow-state.json` 中断恢复逻辑本身的改动(正交,未坏)。
- 检测 stash / 普通 detached HEAD 的语义增强(潜在后续,本 Spec 不做)。

## Open questions (全部已收敛 — Rev1 post_spec R1)

1. ~~TG-B 落点~~ → **已定 (b)**: 新 collector 字段 + RECOMMENDATION_RULES.md 规则 + SKILL/recommendation-stages prose,与 `interrupt.status` 正交不篡改(R1 tech-lead/code-reviewer:(a) 是伪选项且弱化 additive)。
2. ~~git dir 取法~~ → **已定**: `git rev-parse --git-dir` + 显式 `is_absolute()` 判断后 join project_root(R1 backend-architect:superproject 返回相对 `.git`,不解析则依赖 CWD 静默失效)。
3. ~~schema bump 粒度~~ → **已定 不 bump**: nested optional under `git` 符合 §Versioning additive 定义,保持 `"1.0"`(R1 knowledge-manager:SOT 已有明确答案)。
4. ~~`has_conflicts` 成本~~ → **已定 条件求值**: 仅 `operation != none` 才跑 `git diff --diff-filter=U`。
