# DEC-20260609-001: 禁止/告警归档"仅 Phase A 收敛、实施未做"的 Spec (#134)

> **状态**: Approved (owner 已选 D1-D4 + 审计累计修订并入)
> **关联 Issue**: Forgejo #134 (triage verdict = partial-repro)
> **brainstorm 模式**: technical (4 决策 + 3 轮收敛审计)
> **ship target**: aria-plugin v1.42.0 (当前 SOT = plugin.json v1.41.0, A.1 spec-drafter 须 re-verify)
> **决策日期**: 2026-06-09

---

## 1. 背景

### 1.1 触发与 triage verdict

#134 报告: openspec-archive 归档闸门存在漏洞, 会把"仅 Phase A 设计收敛、实施未做"的 Spec 误判为可归档, 把"设计定稿"等同于"cycle 完成"。triage verdict = **partial-repro**: 部分场景可复现 (Level 3 有 tasks.md 时闸门有效), 但存在多处旁路。

活体案例: **block-flip** Spec (`Status='DEFERRED'`) — 这是设计未实施却需要被持续 surface 的真实存量样本, 在当前架构下 `_normalize_status('DEFERRED')` → `'unknown'`, 既不进 `pending_archive` 也不进 `priority_items`, 端到端**静默逃逸**。

### 1.2 现状闸门的四个漏洞 (issue gap a-d)

| gap | 描述 | 经代码核验的事实锚 |
|-----|------|---------|
| (a) | 仅 Level 3 有 `tasks.md` 才生效, Level 2 无闸门 | phase-d-closer `skip_evaluation.D.2` line 80 `skip_if: has uncompleted tasks` 对无 `tasks.md` 的 Level 2 spec 求值为 false (文件不存在→无未完成项) → 直接归档 |
| (b) | checkbox 全勾 ≠ 实施 merged/verified | `tasks.md` 全 `[x]` 但含 inline defer/carry-forward 注释时仍误判 complete |
| (c) | `skip_verification` / `--force` / `--no-validate` 可无标记无 reason 绕过 | openspec-archive SKILL.md `skip_verification:false` (line 83) + 错误表"使用 --force" (line 203) |
| (d) | state-scanner 无 "converged-but-unimplemented" vs "feature-done" 区分 | 见 1.3 数据流断链 |

### 1.3 经代码逐条核验的数据流断链 (3 轮收敛关键证据)

- `openspec.py:92` — `pending_archive` **仅** `st=='done'` 触发, 无 `implemented` 桶, 无 `design_deferred` 区。
- `openspec.py:116-127` — archive 扫描循环**仅** `re.match` 目录名 (`date`+`feature` 正则), **从不 open proposal.md** → 消费侧零读标记 I/O 路径; `archive_items` 仅 `path/date/feature` 三字段。
- `requirements.py:20/53` — `priority_items` **独占**派生自 `user-stories/US-*.md`, `_PRIORITY_STATUSES={in_progress,ready,pending}` 硬编码, 与 openspec collector **物理隔离** → 原始设计"未实施 spec 进 priority_items"在当前架构是**端到端断链 no-op**。
- `_status.py` — grep 零 `deferred` 分支 → block-flip 活体 `Status='DEFERRED'` 必归 `unknown` 继续逃逸。
- `_status.py:158` — 注释明确把 `implemented` 定义为 "post-merge, awaiting verify/archive", 且 `pending_archive` 刻意**不在** `implemented` 触发 → 让 `normalize=implemented` 放行 archive gate = **重引 gap(b)**。

---

## 2. 约束条件

| # | 约束 | 来源 |
|---|------|------|
| C1 | 向后兼容 (Rule #4): 既有正常归档流程 (Status 非 implemented/done 的旧 spec) 不可被破坏 | CLAUDE.md 不可协商规则 |
| C2 | 复用 `_status.py` 既有归一管线, 不在 gate 里另写字面字符串匹配 (已处理 i18n/装饰符/word-boundary/#101 substring shadow) | 审计核验 |
| C3 | additive schema 变更**不** bump `snapshot_schema_version`, 消费侧 `.get(field, [])` 防 KeyError | state-snapshot-schema.md §Additive-change policy |
| C4 | Rule #6: scan.py 标记消费 = deterministic collector → structural fixture + unit tests substitute (非 capability AB) | 不可协商规则 #6 + memory `feedback_deterministic_structural_skill_rule6_substitute` |
| C5 | stdlib-only fail-soft: 读 proposal.md frontmatter 不引 PyYAML, `errors='replace'`, OSError/缺字段 → null + soft_error 诊断条目 (与 `status_field_truncated` 模式一致) | 审计核验 + 既有 collector 模式 |
| C6 | 标记不开 sidecar: 单一权威载体 = 归档后 proposal.md frontmatter 单文件 | 收敛裁定契约 B |
| C7 | surface backstop 必须 surface-only (read-only), 不做 legacy bulk backfill (anti-scope-creep) | D3 + 收敛裁定 |
| C8 | complete 判定必须可执行 SOT, 非声明: SKILL.md 的 AI agent 无法 import Python | 收敛裁定契约 A |

---

## 3. 考虑的方案 (D1-D4 候选 + 评分 + 选定)

### D1 — 归档闸门强度

| 候选 | 描述 | 评分 | 选定 |
|------|------|------|------|
| A | 纯告警 (warn-only), 不阻断 | 低 — 无法堵住误归档, 等同现状 | |
| B | 默认硬阻断, 无逃生舱 | 中 — 但"确需归档设计稿"无合法出口, 会逼出 `--force` 绕过 | |
| **C** | **默认阻断 + 带标记逃生舱**: 归档未实施稿须显式 `--archive-design-only` + 强制 reason, 写 `implementation-deferred` 标记 | **高 — 默认安全 + 可追溯逃生 + 标记驱动 surface** | **✅** |

**D1 选定 = C**。配套收口 (收敛 blocking 收口): `--archive-design-only` 的 `reason` ≥10 非空白字符 (拒纯空白); 旧绕过通道 (`skip_verification=true` / `--force` / `--no-validate`) 必须收口, 否则带标记逃生舱追溯价值归零 — **本 Spec AC 二选一**:
- 收口方案 (推荐): `--force`/`--no-validate` 在 errors 表标 **DEPRECATED** 指向 `--archive-design-only` + reason; `skip_verification` 仅保留跳过 `tasks.md [x]` 校验, **不绕过** Status 归一化 gate (缺 tasks.md 且 Status 非 archive-ready 时 `skip_verification=true` 也须 BLOCK 提示改用 `--archive-design-only`)。
- backward-compat shim: 传旧 `skip_verification=true` 未配 `--archive-design-only` → **WARN+abort, 不静默降级**。

### D2 — 完成信号定义

| 候选 | 描述 | 评分 | 选定 |
|------|------|------|------|
| **A (修订后)** | `complete := (tasks.md 全[x] 若存在) OR (_normalize_status(Status) ∈ archive-ready 集)` | **高 — 复用既有归一管线, 锚 normalized 值非 raw 字面** | **✅** |
| B | 仅看 checkbox | 低 — Level 2 无 tasks.md 时无信号 |  |

**D2 选定 = A (审计强修订)**。关键修订:
- 锚定 **normalized 值** 而非 raw 字面: 原始设计的 raw 集合 `{Implemented, Shipped, Complete}` 跨两个 normalized 桶且漏掉 `Delivered`, 对装饰符/大小写 (`✅ **Implemented**`) 脆弱。改为复用 `_normalize_status()`。
- **archive-ready 集成员定论 = `{done}` only (方案 A)**, `implemented` 归 surface/awaiting-verify, `pending_archive` 不变。**禁止默认 `{implemented,done}`** — `_status.py:158` 明确把 `implemented` 定义为 "post-merge, awaiting verify/archive", 让 `implemented` 放行 archive = 等价重开 gap(b)。此为 spec rationale **硬编码**, 禁止实现时自判。
- carry-forward 子类闭合 gap(b): `is_spec_complete` 在 `tasks.md 全[x]` 分支额外**复用 `_extract_carry_forward_annotations` 同一正则** (避免双写) 检查是否含 defer/carry-forward inline 注释, 若有则 `complete=False`, `reason='全[x] 但含 N 条 carry-forward/defer 注释'`。

### D3 — 防御范围 (scope)

| 候选 | 描述 | 评分 | 选定 |
|------|------|------|------|
| **A (修订后)** | **两层防御**: ① 归档 gate; ② state-scanner 派生信号 surface "设计定稿/未实施" 区 | **高 — gate 堵住未来 + surface 兜住存量** | **✅** |
| B | 仅 gate | 中 — 存量无标记 spec (block-flip) 继续逃逸 |  |

**D3 选定 = A (审计强修订, 修正跨 collector 字段错配)**:
- surface 落点 = **openspec collector 新增独立平级字段** (changes 子树下 `design_deferred[]`), **绝非 `requirements.priority_items`** (经核验物理隔离, 原始设计是端到端断链 no-op)。D3 所有"进 priority_items"文案全部改写为"进 openspec collector 的 design_deferred surface 字段"。
- surface 触发 = **派生信号** (非标记必要): `active changes/ 中 complete==False 的 spec` 进 surface 区。标记只是增强分类。这样 block-flip (`Status=DEFERRED`→`normalize=unknown`) 也被兜住。
- **gate↔surface 互补 (无*非预期* silent 态)**: `gate ALLOW ⇔ is_complete`。design_deferred surface 谓词 (与 §7 一致, 精确): `complete==False ∩ ( unknown ∪ (approved ∧ staleness>=30d) ∪ {reviewed,active,implemented} )`。其余 active 非 complete 桶分流: `{in_progress,ready,pending}` 由 `requirements.priority_items` 别处 surface; **fresh-approved (`approved ∧ staleness<30d ∧ ¬complete`) 是合法在飞态** (刚 Approved 实施待起, changes[] active 原样可见, 非黑洞非卡住), 不入 design_deferred 以免稀释信号。complement-invariant (4 合法桶): `is_complete ∨ in_design_deferred ∨ ∈{in_progress,ready,pending} ∨ (approved∧staleness<30d)`。前置: changes/ 不含 terminal 态。staleness = proposal.md mtime 天数 (frontmatter updated-at 优先), N=30 hardcode。
- backstop **surface-only (read-only)**, 不写不迁移历史, 不做 legacy bulk backfill (anti-creep)。

### D4 — 惯例 (convention)

| 候选 | 描述 | 评分 | 选定 |
|------|------|------|------|
| **A** | **显式废弃** "Phase-A-converged 即归档", 新规 "归档=功能完成; 设计定稿是 in_progress milestone 非归档理由; 确需归档未实施稿走带标记逃生舱" | **高 — 心智模型 + 文档 SOT 对齐代码** | **✅** |
| B | 仅改代码不改文档 | 低 — 违反 Rule #3 文档同步, AI 见旧文档继续误归档 |  |

**D4 选定 = A**。文档改写覆盖点 (高频漏改区, 每处 `grep -n` 锚定 + Edit 后 `grep -c` 验落地):

| 文档 | 改写点 |
|------|--------|
| `standards/core/ten-step-cycle/phase-d-closure.md` Step 10 | ① Trigger Conditions 仅保留时序触发 (Step9 完成); ② 完成判定移入 Execution 第1步 "Verify All Acceptance Criteria Met"; ③ §2 Update Spec Status checklist 由 checkbox 序列整体替换为 Level2/3 两分支条件句 (L3: `tasks 全[x]`→可归档; L2: `Status normalized ∈ archive-ready`→可归档; Approved-only→需 `--archive-design-only`+reason); ④ Phase D Checklist 行补 L2/3 分支; ⑤ `--no-validate` 在 Execution 第3步命令行旁标 **DEPRECATED** |
| `standards/core/ten-step-cycle/README.md` Quick Reference D.2 行 | 加 "(requires implementation verified, not Approved-only)" |
| `standards/openspec/project.md` §Specification Lifecycle 图 | **改图非加脚注**: Implemented 后 archive 节点标前置条件 (`tasks全[x] ∨ Status∈archive-ready`); Approved 画带标支线 `→[design-only]→archive(implementation-deferred)`; 删/标 DEPRECATED 直接 `Approved→archive` |
| operations.md (openspec collector 文档) | 修正 `:81` values 枚举 + `:89` condition (写 `status==Complete` 已与代码 `st=='done'` 漂移), 与 gate 口径一致 + 加注释指向 `_normalize_status` 为唯一 SOT |
| `state-snapshot-schema.md` | §openspec `archive.items[]` 旁加行内注释 `archive_type: str|null # additive (#134, v1.42.0+); null=normal archive or proposal.md unreadable` + §Additive-change policy 表追加版本行 (两 additive 字段: `archive_type` + `design_deferred`) |

---

## 4. 最终选择 (综合 D1-D4 + 两条核心契约)

**D1=C / D2=A({done} only) / D3=A(两层, openspec 独立字段) / D4=A(显式废弃)**, 落地于**两条经收敛裁定钉死的契约**:

### 契约 A — 单一可执行 complete SOT

下沉为单一脚本/纯函数 **`state-scanner/scripts/lib/spec_complete.py`** (thin CLI), 暴露 `is_spec_complete(spec_dir) -> JSON{complete: bool, reason: str}`:
- `scan.py` (openspec collector) 直接 **import 纯函数**;
- `openspec-archive` Step1 与 `phase-d-closer` D.2 在 prose 中**硬编码** `Bash: python3 <plugin_root>/.../spec_complete.py <spec_dir>` 读 JSON/exit code 做 gate (**不再 AI 解释 prose**, 因 SKILL.md 的 AI agent 无法 import Python)。
- 不变量两层验证: (1) Python unit test 直调函数验三组输入一致; (2) "都调同一脚本"结构事实保证两 SKILL.md 入口一致 ("scan.py import + 两 SKILL.md 经 Bash 调同一脚本")。

### 契约 B — 单一标记载体 round-trip

- 唯一权威载体 = 归档后 **proposal.md frontmatter 新机读字段 `archive_type: implementation-deferred`** (单文件, 不开 sidecar)。
- `openspec.py` archive 扫描循环**显式新增** "open proposal.md → 读 frontmatter `archive_type`" 步骤 + OSError/缺字段 fail-soft 返回 null (stdlib-only, `errors=replace`, 不引 PyYAML), 写入 `archive_items[].archive_type: str|null`。
- changes/ 侧 surface 落 **openspec collector 新增独立平级字段 `design_deferred[]`**, 绝非 `requirements.priority_items`。

### 关键执行细节

- **already-archived 前置**: Step1 gate 最前增 "若 `openspec/archive/` 已存在对应条目 → 立即 abort (BLOCKED-already-archived), 不进入完成度判定也不写任何标记"。标记写入为 **Step2 一部分** (非 Step1 副作用), 确保 abort 路径无残留写入。
- **Step2 写 proposal.md 三路径分叉**: (a) 正常归档 — Status 非 implemented/done 时更新 (向后兼容); (b) design-only — 不改 Status 仅 frontmatter 追加 `archive_type: implementation-deferred` + `archived_reason`; (c) dry_run — 不写。
- **dry_run 语义扩展**: `dry_run=true` 执行新 Step1 gate 全部判断 (already-archived 前置 + tasks.md + Status + 标记读取), 报告**三路输出** (BLOCKED / ALLOWED / ALLOWED-design-only + reason 回显 + "若执行将写入 frontmatter: archive_type: implementation-deferred" + 不写入声明), 保持"不实际写入"不变量。SKILL.md 示例3 拆为三子场景 + reason 不足校验拒绝案例。dry_run 三路完全基于 (a) CLI flag (b) 本地 tasks.md (c) proposal.md Status — 均 SKILL 内部直接读取, **不依赖** state-scanner snapshot 预计算字段。
- **phase-d-closer skip_evaluation D.2 三路扩展** (修 gap(a) Level 2 旁路真实代码漏洞): (1) 无活跃 Spec→skip; (2) `spec_not_complete` (调共享 `is_spec_complete()`, Level 2 无 tasks.md 走 Status 归一化分支)→skip 不触发 archive; (3) complete→进 openspec-archive。共享函数 Level 2 分支与 Step1 gate **同 PR/同版本号** ship。

---

## 5. 理由

1. **D1=C 默认安全 + 可追溯**: 默认阻断堵住未来误归档, 带标记逃生舱给"确需归档设计稿"合法出口, 同时收口旧绕过通道使逃生舱追溯价值不被架空。
2. **D2 archive-ready={done} only 不重引 gap(b)**: `_status.py:158` 已把 `implemented` 语义定义为"post-merge, awaiting verify/archive", `pending_archive` 刻意只在 `done` 触发。若让 `implemented` 放行 archive = 堵了 Approved 却开了等价的 implemented 漏洞。`{done}` only 保持与既有代码契约一致。
3. **契约 A/B 把"声明"升级为"可执行架构"**: 原始设计的"单一 SOT"跨 4 个判定点 (Step1 prose / D.2 YAML 伪码 / scan.py Python) 无机制保证。下沉为单一脚本 + 三处共同调用, 才真正消除 data-flow 断裂。
4. **D3 surface 落 openspec 独立字段修正端到端断链**: 经核验 `priority_items` 派生自 US-*.md 与 openspec collector 物理隔离, 原始"进 priority_items"是 no-op; 派生信号 (`complete==False`) 而非标记必要, 兜住 block-flip 这类存量无标记 spec。
5. **gate↔surface 互补消除*非预期* silent 态**: 保证每个 active spec 落 4 合法桶之一 (complete / design_deferred / priority_items / fresh-approved 在飞), 无 spec 既不可归档又对工具不可见。fresh-approved 显式视为合法在飞态 (changes[] 原样可见), 非黑洞。
6. **D4 文档同步 (Rule #3)**: 代码改了文档不改 = AI 见旧 lifecycle 图继续误归档; 故 5 处权威文档 (含 project.md 生命周期图改图) 全覆盖。

---

## 6. 风险与缓解

| # | 风险 | 缓解 |
|---|------|------|
| R1 | complete 判定逻辑分散三处再次漂移 | 契约 A: 单一 `spec_complete.py` 纯函数, scan.py import + 两 SKILL.md Bash 调同一脚本; fixture 验"多入口对同一 spec 一致 verdict"不变量 |
| R2 | 标记载体跨 collector 字段错配 (priority_items vs openspec) 致 surface no-op | 契约 B: surface 落 openspec collector 独立 `design_deferred[]`; D3 全文案改写; round-trip fixture 含真实标记正样本 |
| R3 | archive_type 读取引入 proposal.md I/O 异常致 collector crash | C5 fail-soft: stdlib-only, `errors=replace`, OSError/缺字段→null + soft_error 诊断条目 (与 `status_field_truncated` 一致); fixture 含 `archive_type='garbage'` + proposal.md 不存在负样本 |
| R4 | phase-d-closer Level 2 旁路独立放行 (即使 Step1 gate 正确) | skip_evaluation 三路扩展, 共享函数与 Step1 gate 同 PR/同版本号 ship |
| R5 | 旧 `--force`/`skip_verification` 架空新 gate | D1 收口: errors 表标 DEPRECATED + backward-compat shim WARN+abort 不静默降级 |
| R6 | ship 顺序错误致消费侧读不到写入侧标记 | **消费侧先 ship** (能读且对未知格式 fail-soft) → **archive 写入侧再 ship**; 写入正则与消费正则**同 PR/同版本号** |
| R7 | surface backstop 卷入正常活跃 approved/in_progress, 稀释信号 | surface 集 = `complete==False ∩ ({unknown} ∪ stale-approved(>=30d) ∪ {reviewed,active,implemented})` 排除 in_progress/ready/pending + fresh-approved (合法在飞); complement-invariant 测试 |
| R8 | additive schema 致旧消费侧 KeyError | C3: 不 bump `snapshot_schema_version`, 消费侧 `.get(field, [])`; schema change history 追加记录 |
| R9 | 文档多锚点高频漏改 (行号 snapshot 已漂移) | proposal 用一张表把所有改写点列 checklist; 每处 `grep -n` 锚定真实行 + Edit 后 `grep -c` 验落地 (memory `feedback_verify_edit_landed_grep_count`) |
| R10 | already-archived spec 再归档写标记致状态不一致 | Step1 gate 最前 already-archived 前置 abort, 标记写入为 Step2 (非 Step1 副作用) |

---

## 7. 实现触及面

| 文件 | 改动 |
|------|------|
| `aria/skills/state-scanner/scripts/lib/__init__.py` (新) | 空文件使 `lib` 成 Python package |
| `aria/skills/state-scanner/scripts/lib/carry_forward.py` (迁移) | `_CARRY_FORWARD_RE` + `_extract_carry_forward_annotations` 从 `collectors/openspec.py` 上移; openspec.py 改 `from ..lib.carry_forward import ...` (消除循环引用) |
| `aria/skills/state-scanner/scripts/lib/spec_complete.py` (新) | `is_spec_complete(spec_dir)->JSON{complete,reason}` 纯函数 + thin CLI; 复用 `_status._normalize_status` + `lib.carry_forward._extract_carry_forward_annotations` |
| `aria/skills/state-scanner/scripts/collectors/openspec.py` | ① 改 import carry_forward from lib + import `is_spec_complete`; ② archive 循环新增 open proposal.md 读 frontmatter `archive_type` + fail-soft (key=`archive_type_unreadable`) → `archive_items[].archive_type:str|null`; ③ 新增独立 `design_deferred[]` surface 字段 (changes 子树, `complete==False ∩ ({unknown} ∪ stale-approved(>=30d) ∪ {reviewed,active,implemented})`, 排除 in_progress/ready/pending); ④ operations.md 文档漂移修正 (`:81`/`:89`) |
| `aria/skills/openspec-archive/SKILL.md` | Step1 完成 gate (Bash 调 `spec_complete.py`) + already-archived 前置 + design-only 逃生舱 (`--archive-design-only` + reason ≥10 非空白) + Step2 三路径写 proposal.md + dry_run 三路输出 + options schema (`archive_design_only:false` + `reason:''`) + errors 表 (reason 不足→BLOCKED-invalid-reason; `--force`/`--no-validate`→DEPRECATED; skip_verification 收口) + 示例3 三子场景 |
| `aria/skills/phase-d-closer/SKILL.md:80` + `references/execution-steps.md` (D.2 skip_if line 64-66) | D.2 skip_evaluation 三路扩展, Bash 调同一 `spec_complete.py` |
| `standards/core/ten-step-cycle/phase-d-closure.md` | Step 10 五处改写 + Level2/3 分支判定 + `--no-validate` DEPRECATED |
| `standards/core/ten-step-cycle/README.md` | Quick Reference D.2 行加 "(requires implementation verified, not Approved-only)" |
| `standards/openspec/project.md` | §Specification Lifecycle 图改图 (前置条件 + design-only 支线 + 删/标 DEPRECATED) |
| `state-snapshot-schema.md` | additive 字段注释 (`archive_type` + `design_deferred`) + §Additive-change policy 表版本行; **不 bump** `snapshot_schema_version` |
| 版本 SOT (5+1) | plugin.json (真理来源) + marketplace.json (×2 缩进) + VERSION + CHANGELOG.md + README.md + 主项目 gitlink/VERSION |

**ship 顺序**: 消费侧 (openspec.py + spec_complete.py, fail-soft) 先 ship → 写入侧 (openspec-archive 标记写入) 再 ship; 写入正则与消费正则同 PR/同版本号。

---

## 8. Rule #6 验证策略

`spec_complete.py` + openspec.py 标记消费 = **deterministic collector/parser 类 Skill** → 按 memory `feedback_deterministic_structural_skill_rule6_substitute`, Rule #6 substitute = **structural fixture + unit tests + dogfood** (非 capability AB):

1. **complete SOT unit test**: 直调 `is_spec_complete` 验三组输入一致; 覆盖全 normalized-state × {tasks.md 有/无 × 全[x]/有[ ]} 判定**真值表**作 fixture 骨架。
2. **round-trip 锚**: structural fixture 含 archive 写出的**真实标记正样本** (`archive_type: implementation-deferred`) + `archive_type='garbage'` fail-soft 负样本 + proposal.md 不存在样本 (返回 null + soft_error, 与 `status_field_truncated` 模式一致)。
3. **block-flip 活体 fixture**: 以 block-flip 真实 spec (`Status=DEFERRED`→`normalize=unknown`, 无 tasks.md) + 一个 checkbox 全勾但 Status 非 done 的合成样本共同作 fixture, 显式标注落 surface 行, 验证目标命中且**不卷入**正常活跃 approved/in_progress spec。
4. **complement-invariant 测试**: 对每个 active spec 断言落 4 合法桶之一 `is_complete ∨ in_design_deferred ∨ ∈{in_progress,ready,pending} ∨ (approved∧staleness<30d)`, 无第三态; 须对真 Aria 树 (含 3 个 fresh-approved spec) 绿跑。
5. **两入口一致性**: fixture 覆盖 "scan.py + 两 SKILL.md 经 Bash 调同一脚本对同一 spec 给出一致 verdict" 不变量。
6. **carry-forward 子类**: fixture 验 `tasks.md 全[x] 但含 defer 注释 → complete=False`。
7. **sync-check**: state-snapshot-schema.md §openspec + reference fixture 同步 (否则 sync-check fail)。
8. **dogfood**: 真 Aria 仓库 changes/ 跑 collector 验 block-flip 落 design_deferred、e2e-resilience/release-closeout 不被误卷入。

---

## 9. Out-of-Scope

- **历史无标记 spec 的 bulk migration / backfill**: D3 backstop 是 **surface-only (read-only)** 派生信号, 不写不迁移历史。存量无标记 deferred spec 由派生信号 (`complete==False`) 自动 surface, **不**在本 issue 顺手做 legacy bulk backfill (anti-scope-creep), 留 follow-up migration。
- **GitHub Actions / 其他 CI backend 的 archive gate 集成**: 本 Spec 仅覆盖 openspec-archive + phase-d-closer + state-scanner 三处。
- **`implemented` → `done` 的自动晋升机制 (实施验证闭环)**: `implemented` (awaiting verify) 仅 surface, 何时晋升 `done` 不在本 Spec 范围。
