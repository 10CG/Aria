# Pre-merge Completeness Gate 描述性推演 (change-scope + Phase-A-only 场景)

> 依据: `skills/audit-engine/SKILL.md` + `references/execution-modes.md` `## Pre-merge: Checkpoint Report Completeness Gate` (Forgejo Issue #26)。全程描述性推演, 未执行任何命令。
>
> **先声明一个版本事实, 它直接决定 (1)(2)(3) 的答案形态**: 在本快照的 audit-engine 里, completeness gate **不是独立脚本, 没有独立命令行**。`scripts/` 下只有 `sibling_spec_probe.py` (竞品 spec 探针, 另一机制); 全文 grep `--diff-repo-path` 零命中, `--repo-path` 仅出现在探针调用里。gate 是 audit-engine 执行流程第 (2) 阶段 (入口逻辑之后、任何审计 Agent 之前) 的 **inline 5-step 过程**, 其判定粒度是 **checkpoint 名 (二值: 命中/缺失)**, **没有 change_id 维度, 没有 PR diff 维度, 也没有 `[OK]`/`[INFO]`/ERROR 三态人读行** —— 成功时静默放行, 失败时输出聚合 ERROR block。题目给的 `--repo-path` / `--diff-repo-path` 同仓形态、(checkpoint, change_id) 配对三态、逐对人读行, 都不是本版本 gate 的输出面; 下文按本版本实际语义推演, 并在每一问标注语义真值与本版本输出面的差距。

---

## (1) 会执行的调用命令行

**本版本不存在 completeness gate 的独立命令行。** 忠实于快照的答案是: gate 随 audit-engine 的 pre_merge 调用自动进入, 入口参数是 audit-engine 自身的输入参数:

```
audit-engine(
  checkpoint = "pre_merge",
  context    = "openspec/changes/widget-export-pipeline/proposal.md",  # 被审 change 的 spec 锚点
  mode       = <未显式传, 从 config 解析>,                               # 见下
  agents_config = <未传, 取 config teams 或默认分组>
)
```

入口逻辑推演:

- `audit.enabled == true` → 不静默返回; `checkpoints.pre_merge == "convergence"` ≠ off → checkpoint 已启用。
- mode 解析: config `audit.mode == "manual"` (非 adaptive, 不走 adaptive_rules 推导); 按优先级「checkpoints 显式配置 > adaptive_rules > 默认 off」, `pre_merge` 显式 `"convergence"` → `resolved_mode = convergence`。
- file-scope 二次过滤 (#58): 变更文件 = 3 个 `.md` (diff 恰为 proposal.md / tasks.md / post_spec 报告)。若 `scope_skip_paths` 含 `*.md` 则 cap 到 convergence —— 本来就是 convergence, 幂等; 该过滤只影响 mode, **不影响 gate**。
- 随后进入第 (2) 阶段 Pre-merge gate, 等价的机械动作 (本版本若落成命令即此):

```
读取 .aria/config.json → audit.checkpoints + audit.allow_incomplete_checkpoints (缺省 false)
扫描 {project_root}/.aria/audit-reports/
对每个纳入校验的 checkpoint_name 做前缀存在性匹配: {checkpoint_name}-*.md
```

注意: `sibling_spec_probe.py --own-spec-dir ... --repo-path ...` 是**每轮入口**的探针, 在 gate 之后 (Round 1 入口) 才会跑 —— 本场景 gate 中止, 探针根本不会执行。

---

## (2) 三个 checkpoint 的判定结论

**Step 3 (枚举)**: `audit.checkpoints` 四个 key 中, value 均为非 `"off"` 的模式字符串, 排除 `pre_merge` (自身) 后, 纳入校验集合 = **{post_spec, post_planning, post_implementation}** (`post_closure` / `mid_post_spec` 本就按规则排除, 且未出现在 config)。

**Step 4 (存在性匹配)** + 题目要求的 (checkpoint, change_id=widget-export-pipeline) 三态语义:

| checkpoint | gate 匹配 (`{checkpoint}-*.md`) | gate 判定 (二值) | (checkpoint, change_id) 语义真值 | 三态映射 |
|---|---|---|---|---|
| post_spec | `post_spec-R2-widget-export-pipeline.md` 命中 | 通过 | 报告存在**且恰好属于** widget-export-pipeline | **[OK]** (真 pass; 但 gate 并未校验归属, 纯属巧合一致) |
| post_planning | `post_planning-R1-catalog-sync-retry.md` 命中 | 通过 | 该文件属于 **catalog-sync-retry**, widget-export-pipeline 自己的 post_planning 报告**不存在** | gate 输出面 = [OK] (**跨 change 假 pass**); 语义真值应为缺失。本版本无 change_id 维度, 无法区分, 也不可能产生 [INFO] 档 |
| post_implementation | 无任何 `post_implementation-*.md` | **missing_checkpoint** | 无报告 (且本 PR 为 Phase-A-only, 实现从未发生) | **ERROR** |

- post_spec / post_planning 两个变体 pattern (`{checkpoint}-*.md` 与 `{checkpoint}-*-*.md`) 在本场景都退化为同一前缀判定: 文件名以 `post_planning-` 开头即命中, gate **不解析也不比对文件名中的 change_id 段** —— 这正是 `post_planning-R1-catalog-sync-retry.md` 能替 unrelated change「顶名额」的机制。
- 「Phase-A-only PR (零实现代码)」在本版本 gate 里**没有任何减免费**: Step 3 只看 config 声明, 不看 PR diff 里有没有实现产物; 不存在「该 phase 的被审对象未产生 ⇒ 前置报告可免」的分支。config 声明 `post_implementation: "convergence"` ⇒ 一律要求报告存在。

---

## (3) 人读行措辞

**本版本的成功路径是静默的** —— 对 post_spec / post_planning 两对, gate **不输出任何人读行** (没有 `[OK]`, 也没有 `[INFO]`; 这两个 token 在本快照全文零命中)。若强行按题目的三态格式补写, 只能是我自拟的 (非快照规定):

```
[OK] post_spec: .aria/audit-reports/post_spec-R2-widget-export-pipeline.md 存在
[OK] post_planning: .aria/audit-reports/post_planning-R1-catalog-sync-retry.md 存在   ← 实为 catalog-sync-retry 的报告, gate 不查归属
```

**本版本唯一规定的人读输出**是失败时的聚合 ERROR block (Step 5), 逐字代入本场景:

```
ERROR: pre_merge audit 前序 checkpoint 报告缺失:
  - post_implementation 配置 "convergence" 但未找到 .aria/audit-reports/post_implementation-*.md

Fix 任一:
  1. 补跑缺失 checkpoint 审计 (对应 Phase Skill 重新调用)
  2. 在 .aria/config.json 将该 checkpoint 改为 "off" (若本轮确实不需要)
  3. 在 .aria/config.json 设 audit.allow_incomplete_checkpoints: true
     (不推荐, 豁免需 audit trail 记录 [WARN])
```

(模板原文写 `配置 "on"` —— `"on"` 是「已启用值」的占位; Step 3 接受 `"on"` 或任意非 `"off"` 模式字符串, 本场景实际值为 `"convergence"`。本题只有一处缺失, 不存在「多个缺失逐行列出」的行。)

---

## (4) 最终 verdict、exit code、是否放行

- **Step 5 路由**: `missing_checkpoints = [post_implementation]` 非空 → **拒绝执行 pre_merge 审计, 输出上述 ERROR, 中止**。
- **verdict**: pre_merge 审计的 report 级 verdict (PASS / PASS_WITH_WARNINGS / FAIL) **根本不会产生** —— 任何审计 Agent 未被 spawn, Round 1 未启动, 无报告写盘。本步的结论是 gate 层的: **校验失败 / 拒绝放行**。
- **exit code**: 本版本未给 gate 定义数值 exit code (它不是脚本; 快照中唯一的 exit code 契约属于 sibling_spec_probe)。行为语义 = 阻断性中止, 调用方 (phase-c-integrator 的 pre_merge 调用点) 必须按非零/失败处置, 停下并把 Fix 三选一交给操作者。
- **是否允许进入正常 pre_merge 审计流程**: **否**。

---

## 推演结论: 本场景对本版本 gate 的两面性

1. **假 pass 面 (change-scope 盲区)**: post_planning 靠 unrelated change `catalog-sync-retry` 的既有报告通过了完整性校验 —— gate 只做 checkpoint 名前缀匹配, 「该跑的 checkpoint 都跑了」被降读成「该名字的文件存在过」, 横向完整性在多 change 并存的仓里失真。
2. **假 block 面 (Phase-A-only 盲区)**: post_implementation 因 config 启用而报告缺失被拒 —— gate 不感知 PR diff 范围 (本次 PR 只有 spec 两件套 + 一份 post_spec 报告, 零实现代码), 没有「被审对象未产生 ⇒ 前置依赖不适用」的分支; 操作者只能走 Fix 2 (改 off, 但那会动 owner 的配置决定) 或 Fix 3 (开 `allow_incomplete_checkpoints` 豁免, 默认 false 且需 audit trail 记 [WARN]), 二者都不是「这本来就是 Phase-A-only PR」的自然语义。
