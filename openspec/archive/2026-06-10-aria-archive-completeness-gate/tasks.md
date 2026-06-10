# Tasks: archive-completeness-gate (#134)

> **Spec Level**: 3 | **DEC**: DEC-20260609-001 | **ship target**: aria-plugin v1.42.0
> **ship 顺序约束** (DEC R6): 消费侧 (TG-A) 先 merge → 写入侧 (TG-B) 再 merge; 写入正则与消费正则**同版本号**。
> **sub-PR 三段式** (memory `feedback_sub_pr_scope_splitting_pattern`): (a) TG-A prereq 消费侧 + SOT lib; (b) TG-B 写入侧 gate; (c) TG-C cleanup/docs/version。
> **每处文档改动**: `grep -n` 锚定真实行 (行号 snapshot 已漂移) + Edit 后 `grep -c` 验落地 (memory `feedback_verify_edit_landed_grep_count`)。

---

## TG-A — 消费侧 + 单一可执行 SOT (先 ship, fail-soft)

### A1. `lib/` package 单一 complete SOT (契约 A) — 含 carry_forward 上移消除循环引用
- [x] A1.1a 新建 `aria/skills/state-scanner/scripts/lib/__init__.py` (空文件, 使 `lib` 成 Python package)
- [x] A1.1b 新建 `lib/carry_forward.py`: 将 `_CARRY_FORWARD_RE` (现 `collectors/openspec.py:17-19`) + `_extract_carry_forward_annotations` (现 `openspec.py:22-37`, 调用点 `openspec.py:103`) **物理上移** (~25 行); 把 `collectors/openspec.py` 顶部改为 `from ..lib.carry_forward import _CARRY_FORWARD_RE, _extract_carry_forward_annotations` (消除 spec_complete↔openspec 循环引用)
- [x] A1.1c 新建 `lib/spec_complete.py`: 纯函数 `is_spec_complete(spec_dir) -> {complete: bool, reason: str}` + thin CLI (`python3 spec_complete.py <spec_dir>` → stdout JSON + exit code)。CLI 入口在 import 前 `sys.path.insert(0, str(Path(__file__).parent.parent))` 使 `from collectors._status import _normalize_status` 可解析
- [x] A1.2 逻辑 (无歧义形式): `complete := (tasks.md 存在 AND 全[x] AND 无 inline defer/carry-forward 注释) OR (_normalize_status(Status) == 'done')`。**tasks.md absent → complete 仅由 Status 归一化决定** (绝非 vacuously True, 否则反向击穿 gap(a))。归一化复用 `_status._normalize_status` + `_status._extract_status`; carry-forward 提取 `from lib.carry_forward import _extract_carry_forward_annotations` (**不** 直接 import openspec.py, **非** _status.py)。**`implemented` 不算 complete** (DEC §3 D2 rationale 硬编码)
- [x] A1.3 stdlib-only fail-soft: spec_dir 无 proposal.md / OSError → `complete=False, reason` 诊断; `errors='replace'`
- [x] A1.4 unit test `test_spec_complete.py`: 全 normalized-state × {tasks.md 有/无 × 全[x]/有[ ]} **判定真值表** fixture; carry-forward 子类 (全[x] 但含 defer 注释→complete=False); 验"多入口对同一 spec 一致 verdict"不变量; **+ CLI/import 一致性 fixture** (`subprocess.run python3 spec_complete.py <dir>` 解析 stdout JSON vs `import is_spec_complete(dir)` 直调, 断言 diff==0, 覆盖 complete/incomplete/no-proposal 三类, 锚 AC-1 'Bash 调'不变量)

### A2. openspec.py 标记消费 + design_deferred surface (契约 B + D3)
- [x] A2.1 `collectors/openspec.py` archive 循环新增 "open proposal.md → 读 frontmatter `archive_type`" + fail-soft (stdlib-only, errors=replace, 不引 PyYAML; OSError/缺字段→null + soft_error 诊断, key=`archive_type_unreadable` 稳定命名, 对齐既有 `spec_read_failed`/`tasks_read_failed`/`status_field_truncated`) → `archive_items[].archive_type: str|null`。**Errata (实施定案)**: soft_error 仅 {proposal.md 缺失 / OSError / 未知 archive_type 值}; "frontmatter 存在但无 archive_type 字段 / 无 frontmatter" = 正常 pre-v1.42.0 archive → **静默 null 无诊断** (字面执行会让 100 个历史 archive 每次 scan 刷 100 条 soft_error, 违 C1 向后兼容; code-review Minor-2 留痕)
- [x] A2.2 新增**独立平级字段 `design_deferred[]`** (changes 子树, **非** `requirements.priority_items`): 派生信号 = `is_spec_complete()==False ∩ ( _normalize_status==unknown OR (_normalize_status==approved AND staleness_days >= 30) OR _normalize_status ∈ {reviewed, active, implemented} )`。staleness_days = proposal.md mtime 天数 (frontmatter updated-at 优先若存在), 阈值 N=30 **hardcode 常量** (非 config, stdlib-only)。**排除 in_progress/ready/pending** (别处 priority_items surface)。验收口径: grep 确认不再出现裸 `{approved, unknown}` 无 staleness 限定
- [x] A2.3 import `from ..lib.spec_complete import is_spec_complete` (两级 `..` 因 collectors/ → scripts/ → lib/) — collector 侧直接调纯函数, 不复制逻辑
- [x] A2.4 **gate↔surface 互补** complement-invariant test (可机械验证, 4 合法桶): 对每个 active openspec spec 断言 `is_spec_complete(spec) ∨ in_surface(design_deferred) ∨ (_normalize_status(spec) ∈ {in_progress, ready, pending}) ∨ (_normalize_status(spec)==approved ∧ staleness_days<30)` —— 第 4 析取 = **fresh-approved 合法在飞态** (changes[] 原样可见, 非黑洞)。`{in_progress,ready,pending}` 对齐 `requirements.py:20` 真实 3 态 (**非** 6 态笔误); `{reviewed,active,implemented}∩¬complete` 落 design_deferred (与 A2.2 一致)。测试须对真 Aria 树 changes/ (含 3 个 fresh-approved spec) 绿跑。前置约束: changes/ 不含 terminal 态 (archived/deprecated)
- [x] A2.5 pending_archive 口径一致 (DEC §4): 决定 implemented 不入 archive-ready → `openspec.py:92` 保持 `st=='done'` 不变 + 加注释指向 `_normalize_status` 为唯一 SOT

### A3. schema 文档 (additive)
- [x] A3.1 `references/state-snapshot-schema.md` §openspec: `archive.items[]` 旁加行内注释 `archive_type: str|null # additive (#134, v1.42.0+); null=normal archive or proposal.md unreadable` + 新增 `design_deferred[]` 字段定义
- [x] A3.2 §Additive-change policy 表追加版本行 (两 additive 字段); **不** bump `snapshot_schema_version`; 消费侧 `.get(field, [])` 防 KeyError
- [x] A3.3 sync-check / reference fixture 同步 (否则 sync-check fail)
- [x] A3.4 operations.md 漂移修正 (改文档不改代码): `:81` values 改为 normalized 值枚举 — **实施时以 `_status.py` `_normalize_status` 实际 codomain 为准核验后写入** (注意: `Draft`→`pending` 故 `draft` 不在 codomain; 勿漏 `ready`/`archived`/`deprecated`) + 注释 `# normalized by _normalize_status()`; `:89` condition `status == Complete` → `status == done` (对齐 openspec.py:92 `st=='done'`)

### A4. TG-A round-trip / dogfood fixture
- [x] A4.1 round-trip fixture: archive 写出的真实标记正样本 (`archive_type: implementation-deferred`) + `archive_type='garbage'` fail-soft 负样本 + proposal.md 不存在样本 (两负样本各断言 soft_error 含 key `archive_type_unreadable`)
- [x] A4.2 **block-flip 活体 + staleness 边界 + 第三态 fixture**: (i) 真实 block-flip spec (`Status=DEFERRED`→`unknown`, 无 tasks.md) → 断言**落** design_deferred; (ii) Status=Approved + proposal.md mtime **< 30 天** + 有 open[ ] task 合成 spec → 断言**不落** (活跃 approved 不卷入); (iii) Status=Approved + mtime **>= 30 天** → 断言**落**; (iv) normalized=implemented (或 reviewed) + complete==False 合成 spec → 断言**落** design_deferred (非黑洞、不落 pending_archive)
- [x] A4.3 dogfood: 真 Aria 仓库 changes/ 跑 collector 验 — block-flip(unknown) 落 design_deferred; 近 30 天内 mtime 的 Approved spec (e2e-resilience/release-closeout) **不落** design_deferred (与 A2.2 staleness 谓词一致)

---

## TG-B — 写入侧 gate (后 ship, 同版本号)

### B1. openspec-archive Step1 完成 gate + 逃生舱 (D1)
- [x] B1.1 Step1 最前 already-archived 前置: 若 `openspec/archive/` 已存在对应条目 → 立即 abort (BLOCKED-already-archived), 不进完成度判定、不写标记
- [x] B1.2 完成 gate: prose 硬编码 `Bash: python3 <plugin_root>/.../lib/spec_complete.py <spec_dir>` 读 JSON/exit code (不再 AI 解释 prose); 未完成默认 BLOCK 列缺口
- [x] B1.3 `--archive-design-only` 逃生舱 + `reason` 字段最小有效性约束 (≥10 非空白字符, 拒纯空白); options schema 新增 `archive_design_only:false` + `reason:''`
- [x] B1.4 旧绕过收口: errors 表标 `--force` **DEPRECATED** 指向 `--archive-design-only`; `skip_verification` 仅跳 tasks.md [x] 校验不绕 Status gate (缺 tasks.md 且 Status 非 archive-ready 时 `skip_verification=true` 也 BLOCK); backward-compat shim: 旧 `skip_verification=true` 未配逃生舱 → WARN+abort 不静默降级。**实施前 grep 核验** openspec-archive/SKILL.md 是否真有 `--no-validate` flag — 若无则从本条去掉 (其 DEPRECATED 已由 C1.1 ⑤ 在 phase-d-closure.md 覆盖)
- [x] B1.5 errors 表新增 'reason 不足10字符→BLOCKED-invalid-reason'

### B2. openspec-archive Step2 三路径写 proposal.md
- [x] B2.1 (a) 正常归档: Status 非 done 时更新 (向后兼容); (b) design-only: 不改 Status 仅 frontmatter 追加 `archive_type: implementation-deferred` + `archived_reason`; (c) dry_run: 不写
- [x] B2.2 标记写入为 Step2 一部分 (非 Step1 副作用), abort 路径无残留写入

### B3. dry_run 三路输出
- [x] B3.1 dry_run=true 执行 Step1 全部判断 (already-archived 前置 + tasks.md + Status + 标记读取), 报告三路 (BLOCKED / ALLOWED / ALLOWED-design-only + reason 回显 + "若执行将写入 frontmatter" + 不写入声明)
- [x] B3.2 注释明确 dry_run 三路完全基于 (a) CLI flag (b) 本地 tasks.md (c) proposal.md Status — 不依赖 snapshot 预计算字段
- [x] B3.3 SKILL.md 示例3 拆三子场景 + reason 不足校验拒绝案例

### B4. phase-d-closer skip_evaluation D.2 三路扩展 (修 gap(a) Level 2 旁路)
- [x] B4.1 `phase-d-closer/SKILL.md:80` (`skip_if: has uncompleted tasks`) + `references/execution-steps.md` (真实锚点 line 64-66 `- spec_not_complete: true`, 及 line 27/64/80 skip_if 块): 三路 — 无活跃 Spec→skip / `spec_not_complete` (Bash 调同一 `spec_complete.py`, Level 2 无 tasks.md 走 Status 归一化分支)→skip 不归档 / complete→进 openspec-archive。**不再保留旧裸 `spec_not_complete`/`has uncompleted tasks` 两路**
- [x] B4.2 与 B1 Step1 gate **同 PR/同版本号** ship (否则混存期 phase-d-closer 独立放行)

---

## TG-C — 惯例改写 (D4) + cleanup/version

### C1. standards 文档 D4 改写 (5 处, 每处 grep -n 锚定 + grep -c 验落地)
- [x] C1.1 `standards/core/ten-step-cycle/phase-d-closure.md` Step10 **五处**: ① Trigger Conditions 仅保留时序触发; ② 完成判定移入 Execution 第1步 "Verify All AC Met"; ③ §2 Update Spec Status checklist 整体替换为 Level2/3 两分支条件句; ④ Phase D Checklist 行补 L2/3 分支; ⑤ `--no-validate` Execution 第3步命令行旁标 DEPRECATED
- [x] C1.2 `standards/core/ten-step-cycle/README.md` Quick Reference D.2 行加 "(requires implementation verified, not Approved-only)"
- [x] C1.3 `standards/openspec/project.md` §Specification Lifecycle **改图** (非加脚注): Implemented 后 archive 节点标前置条件; Approved 画 `→[design-only]→archive(implementation-deferred)` 支线; 删/标 DEPRECATED 直接 Approved→archive
- [x] C1.4 改写点 checklist 表 (proposal 用一张表列全部锚点) 逐处核验

### C2. 版本 SOT (5+1) + CHANGELOG
- [x] C2.1 plugin.json (真理来源) → v1.42.0
- [x] C2.2 marketplace.json (×2 缩进 version, `grep -c` 验 ==2 per memory `feedback_marketplace_json_dual_version_indent`) + VERSION + README.md (版本号 + Skills 数)
- [x] C2.3 CHANGELOG.md 新增 v1.42.0 条目
- [x] C2.4 主项目 gitlink + VERSION 插件版本记录

---

## 审计检查点 (audit-engine)
- [x] post_spec: 本 tasks/proposal vs DEC 保真度 + AC 完整性 (4-round L3 baseline) — **本 cycle 用 multi-agent 动态工作流执行**
- [x] mid_implementation: TG-A 完成后 (消费侧 fail-soft + complement-invariant)
- [x] post_implementation: 全 TG 完成后
- [x] pre_merge: Rule #8 C.2.4 gate (aria-plugin 无 CI → skip_with_warning; PR #78 merge 18c6ba3)
- [x] post_closure: D.3 handoff (Rule #9) — `docs/handoff/2026-06-10-archive-completeness-gate-shipped.md` + latest.md pointer 更新

## 验收标准 (AC) 摘要 (完整见 DEC §4-§8)
- [x] AC-1: `is_spec_complete` 单一 SOT 被 scan.py/openspec.py import + 两 SKILL.md Bash 调, 真值表 fixture 全绿 + CLI/import verdict 一致性 fixture (subprocess vs import diff==0) 绿
- [x] AC-2: `implemented` 不放行 archive gate (不重开 gap(b)); carry-forward 子类闭合
- [x] AC-3: phase-d-closer Level 2 旁路堵死 — `execution-steps.md` D.2 skip_if 含 `spec_complete.py` Bash 调引用, 不再保留旧裸 `spec_not_complete`/`has uncompleted tasks` 两路 (SKILL.md:80 同步); B4 三路 + 同版本号
- [x] AC-4: 标记 round-trip (写入 frontmatter ↔ openspec.py 消费) + fail-soft 负样本不 crash (soft_error key=`archive_type_unreadable`)
- [x] AC-5: design_deferred surface 落 openspec collector 独立字段; gate↔surface 互补无*非预期* silent 态 (complement-invariant 4 桶: `is_complete ∨ in_design_deferred ∨ normalized∈{in_progress,ready,pending} ∨ (approved∧staleness<30d)`); block-flip(unknown) + stale(>=30d) approved + {reviewed,active,implemented}∩¬complete 落 design_deferred; **fresh-approved (staleness<30d) 不卷入** (合法在飞, changes[] 原样可见); 真 Aria 树 invariant test 绿跑
- [x] AC-6: D1 旧绕过通道收口 (DEPRECATED + shim WARN+abort)
- [x] AC-7: D4 五处文档与代码同步 (Rule #3); 生命周期图改图
- [x] AC-8: additive schema 不 bump version, 旧消费侧不 KeyError
