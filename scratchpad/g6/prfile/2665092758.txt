# audit-engine pre_merge completeness gate — 描述性推演 (eval-3: change-scope + Phase A-only)

> 产出形态: descriptive。按 `aria/skills/audit-engine/SKILL.md` §Pre-merge completeness gate、
> `references/execution-modes.md` `## Pre-merge: Checkpoint Report Completeness Gate` 与
> `scripts/completeness_gate.py` 源码逐阶段推演, 未实际执行任何命令。
> Spec SOT: `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` §1.0–§1.4。

## 前置: 门为什么会被调到 (两道启用守卫均放行)

- 守卫一 (调用方 phase-c-integrator 步骤 2): `audit.enabled == true` → 不早退。
- 守卫二 (步骤 3 / audit-engine 入口逻辑级 1): 原始 `audit.checkpoints` 自身含 `pre_merge` 显式键
  且值为 `"convergence"` (非 `"off"`) → pre_merge 判定启用, 照常进入, 调用 completeness gate。
- 门在**调用任何审计 Agent 之前**跑一次, 不随 Round 重演 (与 per-round 竞品 spec 探针是两回事;
  本推演门 fail 后不进入任何 Round, 探针/Step 0 anchor/Agent 全不发生)。

---

## (1) completeness gate 调用命令行 (完整参数)

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/completeness_gate.py" \
  --repo-path "<主仓 root>" \
  --diff-repo-path "<主仓 root>" \
  --base origin/master \
  --change-id widget-export-pipeline
```

参数逐项依据:

| 参数 | 取值 | 依据 |
|---|---|---|
| `--repo-path` | 主仓 root (锚点面: 报告目录 / config / `openspec/{changes,archive}` 锚点链) | argparse `required=True`, 无缺省, 不取 cwd |
| `--diff-repo-path` | **与 `--repo-path` 同值** | 同仓形态显式传相同值 (SKILL.md 参数表); 两面 `git rev-parse --show-toplevel` 逐字相等 ⇒ `same_repo=True` |
| `--base` | `origin/master` | diff 仓主干的远程跟踪 ref, 必传无缺省; 含 `/` ⇒ 结构上不触发 base 轴陈旧 WARN |
| `--anchor-base` | **省略** | 可选, 缺省 = `--base`; 同仓且未显式传入时陈旧比对折叠为一条且以 "base" 命名 —— 本场景该一条也因 ref 含 `/` 不触发, stderr 零 WARN |
| `--change-id` | `widget-export-pipeline` | pre_merge 必传 `change_id` / `--no-spec` 二者其一; 本 cycle 有 spec ⇒ 传前者 (与 `--no-spec` argparse 互斥, 同时给出 exit 2) |
| `--no-spec` | 不传 | 本 cycle 非 Level 1 无 spec 周期 |

---

## (2) 三态判定推演 (逐 (checkpoint, change_id=widget-export-pipeline))

### 2.0 机械求值链 (P0 → P6)

1. **P0 config 直读 + 内联缺省合并**: `enabled=true`; `mode="manual"`; 原始 `checkpoints` 显式四键
   (`post_spec`/`post_planning`/`post_implementation`/`pre_merge` 均 `"convergence"`), 其余 checkpoint 无显式键
   (合并视图里由内联 DEFAULTS 填 `"off"`); `allow_incomplete_checkpoints=false`、`allow_dangling_change_ids=false`
   (两键不在 config, 缺省 false)。
2. **P1 格 A**: `enabled is True` → 不触发 `audit_not_enabled`。
3. **同仓判定**: 两面 toplevel 相等 → `same_repo=True` ⇒ `not_applicable` (b) 通道**允许**触发。
4. **ref 解析**: `origin/master` 在 diff 仓解析成功 (失败会是 `git_failed` exit 2); 含 `/` 不做陈旧比对;
   同仓 + `--anchor-base` 未显式传 → 只查 base 一轴。
5. **P2a**: 未给 `--no-spec` → no-op。
6. **P2 作用域 S1 (first-match 第一支)**: `--change-id widget-export-pipeline` 给出 ⇒ 逐 id 验锚:
   `openspec/changes/widget-export-pipeline/proposal.md` 存在 ⇒ 有锚 ⇒ `scope_source="explicit"`,
   `change_ids=["widget-export-pipeline"]`, dangling 集空。
7. **P3 (lazy Level)**: 三对全部在 P4 落**级 1**, Level 解析**从不发生** —— `mode="manual"` 与 proposal 的
   Level 行在本场景均不影响结果。
8. **P4 纳入**: 8 个已知 checkpoint 去掉五项排除 (`pre_merge` 自身 / `post_closure` / `mid_post_spec` /
   `mid_implementation` / `post_brainstorm`) = `post_spec` / `post_planning` / `post_implementation` 三个。
   三者在**原始** `audit.checkpoints` 里均有显式键 ⇒ 级 1 first-match 命中:
   `resolved_mode="convergence"`, `enabled_by="explicit"` (注意: `mode="manual"` 的级 2d 根本轮不到 ——
   显式键优先于 mode 档)。三对全部纳入 ⇒ `checked_checkpoints=["post_implementation", "post_planning", "post_spec"]`
   (sorted 字典序), 纳入集非空 ⇒ **不进 P5 格 B/C/D/E 分格**, 直接进 P6。
9. **P6 归属匹配**: `C` (已知 id 全集) = `openspec/changes/*` 目录名 = `{widget-export-pipeline, catalog-sync-retry}`。
   报告目录顶层两份文件:
   - `post_spec-R2-widget-export-pipeline.md`: 规则 1 (`post_spec-` 前缀 + `.md`) ✓; 规则 2 末段界定
     (stem `post_spec-R2-widget-export-pipeline` 以 `-widget-export-pipeline` 结尾) ✓; 规则 3 有界包含排除
     不命中 (`-widget-export-pipeline-` 不是 `-catalog-sync-retry-` 的子串) ⇒ **归属 (post_spec, widget-export-pipeline)**。
   - `post_planning-R1-catalog-sync-retry.md`: 对 `widget-export-pipeline` 规则 2 双侧/末段均不命中
     (不含 `-widget-export-pipeline-`, stem 也不以 `-widget-export-pipeline` 结尾) ⇒ **不归属本 change 的任何对**
     (它是 catalog-sync-retry 的报告 —— change 维度正是本门的语义: 他人 change 的报告不能为本 change 充数)。
   - 排除计数: 两份文件都以纳入 checkpoint 名开头且都被 `C` 中某个 id 命中 ⇒ `excluded_legacy_count=0`,
     `unattributed_count=0`, 无 unattributed WARN 行。
10. **(b) 通道求值** (仅 same_repo 且 `post_implementation` 纳入时算): diff 面
    (`--diff-repo-path` + `--base`, merge-base 后 `--name-only --no-renames`) 恰 3 文件且全部落在
    `openspec/changes/widget-export-pipeline/**` ∪ `.aria/audit-reports/**` 之下, diff 非空 ⇒ `phase_a_only=True`。

### 2.1 逐对结论 (三态 first-match: present → (a) → (b) → (c) → missing)

| (checkpoint, change_id) | 判定 | 推演 |
|---|---|---|
| `post_spec@widget-export-pipeline` | **present** (1 份) | 归属匹配命中 `post_spec-R2-widget-export-pipeline.md` (本次 PR 新增的自有 post_spec 报告)。`post_spec` 无 not_applicable 通道 (有 change_id 即有 proposal, 对象必存在)。 |
| `post_planning@widget-export-pipeline` | **missing** | 零归属文件。三态 first-match 逐支排除: (a) 非 `--no-spec`; (b) 专属 `post_implementation`, 此对不适用; (c) 要求「不存在任何 A.2 产物」—— 但 `openspec/changes/widget-export-pipeline/tasks.md` 存在 (本次 PR 带来), `_has_a2_artifact` 返回 True ⇒ (c) 不触发 ⇒ 落 missing。目录里唯一的 `post_planning-R1-catalog-sync-retry.md` 属 `catalog-sync-retry`, 按 §1.2 规则 2 不归属本对。 |
| `post_implementation@widget-export-pipeline` | **not_applicable** (reason=`phase-a-only-no-implementation`) | 零归属文件 (无 `post_implementation-` 前缀文件) → present 不成立; (b) 通道三合取全满足: 同仓 (toplevel 相等) ∧ diff 非空 (3 文件) ∧ 全部路径在 `openspec/changes/{作用域 id}/**` ∪ `.aria/audit-reports/**` 之下 (Phase A-only PR: B.2 实现工序整个未发生, 报告对象结构性不存在 —— 「结构性前提不成立」的合法侧, 不是「存在但简单」)。 |

---

## (3) 人读行逐句措辞 (全部走 **stderr**; stdout 只出 JSON)

按 pairs 顺序 (`sorted` 字典序: post_implementation → post_planning → post_spec) 依次输出三行;
本场景**没有**第四行 (unattributed_count=0 ⇒ 无 unattributed WARN; allow 键全 false ⇒ 无 bypass WARN;
base 含 `/` 且同仓折叠 ⇒ 无陈旧 WARN; 报告目录存在 ⇒ 无「按零报告评估」WARN):

```text
[INFO] completeness gate: post_implementation@widget-export-pipeline not_applicable (phase-a-only-no-implementation); 依据 = diff 3 文件全部在 openspec/changes/widget-export-pipeline/ 或 .aria/audit-reports/ 下 (Phase A-only)
```

```text
ERROR: pre_merge audit 前序 checkpoint 报告缺失: post_planning@widget-export-pipeline 配置 "convergence" 但未找到 .aria/audit-reports/ 下含 "-widget-export-pipeline-" 或以 "-widget-export-pipeline.md" 结尾的 post_planning 报告 (真 legacy 不计入: 0; 归属不明: 0, 见下方清单)。Fix: (1) 补跑缺失 checkpoint 审计 (对应 Phase Skill 重新调用); (2) 或在 audit.checkpoints 里显式写该 checkpoint —— adaptive 推导出的 checkpoint 其报告在产出侧调用链上不产出, 重新调用 Phase Skill 会再次早退; (3) 把该 checkpoint 改 "off"; (4) 临时开 allow_incomplete_checkpoints
```

```text
[OK] post_spec@widget-export-pipeline: 1 份
```

措辞要点:

- not_applicable 行**必须 surface**, 不得折叠进「校验通过」(§1.4); 依据段是运行时渲染的机械事实
  (diff 3 文件 + 具体 id), 不是静态占位串。
- missing 行用**不带方括号的 `ERROR:` 前缀** —— 它是 fail/exit 1 的逐对留痕, 与 GateError 的
  `[ERROR] completeness gate: ...` (error/exit 2 终局诊断) 刻意不是同一种行。两个计数 (真 legacy 不计入: 0;
  归属不明: 0) 是全局单值原样复述, 不按本行重算。
- present 行逐行列出使「通过」可核对归属。

---

## (4) 最终 verdict / exit code / 路由

- **verdict = `fail`, exit code = 1** (§1.4: 任一 missing → fail, exit 1)。本场景恰有一对 missing
  (`post_planning@widget-export-pipeline`); post_spec 的 present 与 post_implementation 的 not_applicable
  不能抵消它 —— 多 change / 多对下**全部**非 missing 才 pass。
- **是否允许放行进入正常 pre_merge 审计流程: 不允许。** Step 5 路由: `verdict == "fail"` → 拒绝执行
  pre_merge 审计, 输出 ERROR, 中止; 消费方负 fail-closed 义务 (exit≠0 或 stdout 非 JSON 或
  `schema_version` 未知 ⇒ 一律按 fail 处置, 不得按 PASS)。下游一切 (Step 0 anchor 固化、per-round
  竞品 spec 探针、convergence/challenge 轮次、Agent dispatch) 均不发生, merge 被本门阻塞。
- 正交说明: 「门放行 ≠ pre_merge 该跑」。本场景即便门过了, pre_merge 本身按级 1 显式
  `"convergence"` (非 off) 会进入正常 convergence 审计 —— 但门没过, 这一分支不可达。
- 修复路径 = ERROR 行的 Fix 四项 (补跑 post_planning 审计 / 显式写 checkpoint / 改 off /
  临时开 `allow_incomplete_checkpoints`)。按 Rule #10, 后三类涉及配置面的处置属 owner 决定,
  AI 不得以「变更小」自行豁免; 本推演不改任何配置。
- stdout 恰一个 JSON 对象 (16 键, `sort_keys`):

```json
{
  "bypassed": false,
  "change_ids": ["widget-export-pipeline"],
  "checked_checkpoints": ["post_implementation", "post_planning", "post_spec"],
  "elapsed_ms": 12,
  "error_kind": null,
  "excluded_legacy_count": 0,
  "gate": "completeness_gate",
  "no_prior_checkpoints": false,
  "results": [
    {
      "change_id": "widget-export-pipeline",
      "checkpoint": "post_implementation",
      "enabled_by": "explicit",
      "matched": [],
      "matched_count": 0,
      "reason": "phase-a-only-no-implementation",
      "status": "not_applicable"
    },
    {
      "change_id": "widget-export-pipeline",
      "checkpoint": "post_planning",
      "enabled_by": "explicit",
      "matched": [],
      "matched_count": 0,
      "reason": null,
      "status": "missing"
    },
    {
      "change_id": "widget-export-pipeline",
      "checkpoint": "post_spec",
      "enabled_by": "explicit",
      "matched": ["post_spec-R2-widget-export-pipeline.md"],
      "matched_count": 1,
      "reason": null,
      "status": "present"
    }
  ],
  "scan_status": "ok",
  "scanned_dir_depth": 1,
  "schema_version": "1",
  "scope_source": "explicit",
  "unattributed": [],
  "unattributed_count": 0,
  "verdict": "fail"
}
```

(`elapsed_ms` 为真实墙钟毫秒 int, 此处为示意值; 其余字段值均为推演确定值。)
