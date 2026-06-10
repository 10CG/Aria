# Proposal: archive-completeness-gate (#134)

> **Status**: ✅ **Complete** — shipped aria-plugin v1.42.0 (PR [#78](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/78) merge `18c6ba3` 双远程 parity + standards `7ecf522`; 全链路: triage → brainstorm 4 决策 → post_brainstorm 19-agent/3 轮 → DEC → post_spec 25-agent/4 轮 → verification 2 轮 PASS → Phase B agent-team 实施 → code-review PASS [I-1/I-2/M-1/3/5/6 已收] → 731 tests + 真树 dogfood)
> **Spec Level**: 3 (Full — proposal + tasks)
> **关联 Issue**: Forgejo [#134](https://forgejo.10cg.pub/10CG/Aria/issues/134) (triage verdict = partial-repro)
> **ship target**: aria-plugin v1.42.0 (当前 SOT plugin.json = v1.41.0)
> **决策 SOT**: `docs/decisions/DEC-20260609-001-archive-completeness-gate.md`

---

## Why

归档闸门存在漏洞,会把"仅 Phase A 设计收敛、实施未做"的 Spec 误判为可归档,把"设计定稿"等同"cycle 完成",致 state-scanner 误判进度为完成、隐藏待实施大工作。triage verdict = partial-repro。

**经代码逐条核验的 4 个漏洞 + 数据流断链** (见 DEC §1):

| gap | 事实锚 |
|-----|--------|
| (a) Level 2 无闸门 | phase-d-closer `skip_evaluation.D.2` line 80 `skip_if: has uncompleted tasks` 对无 tasks.md 求值为 false → 直接归档 |
| (b) checkbox 全勾 ≠ 实施完成 | `tasks.md` 全 `[x]` 但含 inline defer/carry-forward 注释仍误判 |
| (c) `skip_verification`/`--force`/`--no-validate` 无标记无 reason 绕过 | openspec-archive SKILL.md line 83 + 203 |
| (d) state-scanner 无 converged-but-unimplemented vs feature-done 区分 | `priority_items` 派生自 US-*.md 与 openspec collector **物理隔离**; `openspec.py:116-127` archive 循环**从不 open proposal.md** → 原始"进 priority_items"设计是**端到端 no-op** |

**活体存量案例**: block-flip Spec (`Status=DEFERRED`→`_normalize_status`→`unknown`) 既不进 `pending_archive` 也不进 `priority_items`, 端到端静默逃逸。

## What Changes

落地于 DEC 的 **D1=C / D2=A({done} only) / D3=A(两层防御) / D4=A(显式废弃)** + **两条钉死契约**:

1. **契约 A — 单一可执行 complete SOT**: 新建 `state-scanner/scripts/lib/` package (`__init__.py` + `carry_forward.py` + `spec_complete.py`)。`carry_forward.py` 把 `_CARRY_FORWARD_RE` + `_extract_carry_forward_annotations` 从 `collectors/openspec.py` **物理上移** (openspec.py 改 import, 消除循环引用); `spec_complete.py` 纯函数 `is_spec_complete(spec_dir)->{complete,reason}` + thin CLI。`scan.py`/`openspec.py` 直接 import 纯函数; `openspec-archive` Step1 与 `phase-d-closer` D.2 经 **Bash 调同一脚本** 读 JSON/exit code 做 gate (SKILL.md 的 AI 无法 import Python)。消除三处判定分散漂移。
   - `complete := (tasks.md 全[x] 若存在 AND 无 inline defer/carry-forward 注释) OR (_normalize_status(Status) ∈ {'done'})`。归一化复用 `_status._normalize_status`/`_status._extract_status` (i18n/装饰符/word-boundary/#101); carry-forward 注释提取来自新建 `lib.carry_forward` (从 openspec.py 上移, **非** _status.py)。**`implemented` 不算 complete** (=awaiting verify, 入集会重开 gap(b))。

2. **D1 归档 gate + 带标记逃生舱** (openspec-archive Step1):
   - already-archived 前置 abort → 完成度 gate → 未完成默认 BLOCK;
   - `--archive-design-only` + `reason` (≥10 非空白字符) 逃生舱 → Step2 写 proposal.md frontmatter `archive_type: implementation-deferred` + `archived_reason`;
   - 旧绕过收口: `--force`/`--no-validate` DEPRECATED 指向逃生舱; `skip_verification` 仅跳 tasks.md [x] 校验不绕 Status gate; backward-compat shim WARN+abort 不静默降级;
   - dry_run 三路输出 (BLOCKED / ALLOWED / ALLOWED-design-only)。

3. **phase-d-closer skip_evaluation D.2 三路扩展** (修 gap(a) Level 2 旁路, 真实锚点 `references/execution-steps.md:64-66` + `SKILL.md:80`): 无活跃 Spec→skip / `spec_not_complete` (Bash 调共享 `spec_complete.py`)→skip 不归档 / complete→进归档。**与 Step1 gate 同 PR/同版本号**。

4. **契约 B — 单一标记载体 + surface (D3 两层防御)** (openspec.py):
   - archive 循环新增 "open proposal.md → 读 frontmatter `archive_type`" + fail-soft (stdlib-only, errors=replace, 不引 PyYAML, OSError/缺字段→null+soft_error) → `archive_items[].archive_type: str|null`;
   - 新增**独立平级字段 `design_deferred[]`** (changes 子树, **非** priority_items): 派生信号 = `complete==False ∩ ( _normalize_status==unknown OR (_normalize_status==approved AND staleness_days >= 30) OR _normalize_status ∈ {reviewed, active, implemented} )`。staleness = proposal.md mtime 天数 (frontmatter updated-at 优先若存在), 阈值 N=30 hardcode 常量 (非 config, 与 stdlib-only fail-soft 一致); 使 e2e-resilience/release-closeout 这类近 14 天活跃 approved 天然落选;
   - **gate↔surface 互补 (无*非预期* silent 态)**: gate ALLOW ⇔ is_spec_complete; design_deferred surface 纳 `{unknown} ∪ (stale approved, >=30d) ∪ {reviewed,active,implemented}∩¬complete`; 其余 active 非 complete 桶 `{in_progress, ready, pending}` 由 `requirements.priority_items` **别处** surface (实测 `_PRIORITY_STATUSES` (requirements.py:20) 恰此 3 态); **fresh-approved (`approved ∧ staleness<30d ∧ ¬complete`) 是合法在飞态** —— 刚 Approved 实施待起, 由 `changes[]` active 列表**原样可见**, 既非"卡住"亦非"伪装完成", 不入 design_deferred (否则稀释信号)。complement-invariant (4 合法桶, 无第三态): 每个 active spec `is_complete ∨ in_design_deferred ∨ normalized ∈ {in_progress,ready,pending} ∨ (normalized==approved ∧ staleness<30d)`。(前置: changes/ 不含 terminal 态 archived/deprecated)

5. **D4 惯例显式废弃** (5 处 standards/文档, 完整锚点表见 DEC §3 D4 + tasks.md C1): phase-d-closure.md Step10 (5 处, 含 `--no-validate` DEPRECATED) + README.md D.2 + `standards/openspec/project.md` 生命周期图改图 + operations.md 漂移修正 (`:81`/`:89`)。新规: "归档=功能完成; 设计定稿是 in_progress milestone 非归档理由; 确需归档未实施稿走带标记逃生舱"。

## Impact

- **触及面**: 新建 `lib/__init__.py` + `lib/carry_forward.py`(从 openspec.py 迁移) + `lib/spec_complete.py` + `collectors/openspec.py`(改 import + 标记消费 + design_deferred) + `openspec-archive/SKILL.md` + `phase-d-closer/SKILL.md`(+`references/execution-steps.md`) + 5 处 standards/文档 + `state-snapshot-schema.md`(additive, **不** bump `snapshot_schema_version`)。版本 SOT 5+1。
- **ship 顺序** (R6): 消费侧 (openspec.py + spec_complete.py, fail-soft) 先 ship → 写入侧 (标记写入) 再 ship; 写入正则与消费正则**同 PR/同版本号**。
- **向后兼容** (Rule #4): 既有正常归档 (Status 非 done) 不破坏; additive schema 消费侧 `.get(field,[])` 防 KeyError。
- **Rule #6**: deterministic collector/parser → structural fixture + unit tests + dogfood substitute (见 DEC §8 八类 fixture)。
- **Out-of-scope**: 历史无标记 spec bulk migration (backstop 是 surface-only read-only 派生信号, 不写不迁移); GHA 等其他 CI backend; `implemented→done` 自动晋升机制。

> **完整设计/约束/方案评分/风险缓解 (R1-R10)/Rule #6 八类 fixture**: 见 DEC-20260609-001 (设计 SOT, 本 proposal 不复制)。
