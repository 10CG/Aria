# Proposal: handoff-frontmatter-enforcement (#137)

> **Status**: ✅ **Complete** — shipped aria-plugin v1.43.0 (PR [#79](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/79) merge `7214ae8` 双远程 parity + standards `1be388b`; Level 2 链路: triage → proposal → post_spec R1/R2 FAIL→落地→R3 PASS → inline 实施 → code-review PASS [4 Minor 收] → 739 tests + 真树 dogfood)
> **关联 Issue**: Forgejo [#137](https://forgejo.10cg.pub/10CG/Aria/issues/137) (triage `partial-repro`, [comment-12236](https://forgejo.10cg.pub/10CG/Aria/issues/137#issuecomment-12236))
> **ship target**: aria-plugin v1.43.0 (当前 SOT plugin.json = v1.42.0, 已验)

## Why

multi-terminal frontmatter **注入机制已存在** (模板 v1.22.x+ 含 5 字段 + 派生规则), 但**三层全部零 enforcement**: D.3 无写后校验 / L1 hook 只管路径 / collector 静默 legacy fallback 无告警 → 不经模板的 ad-hoc handoff **静默**丢失多终端识别能力 (SilkNode 2026-05-31 实地: 两份并发 handoff 全落 legacy, 看板无法区分且无人知道)。修复方向 = **enforcement 而非注入** (triage case-2/case-3)。覆盖边界分工: D.3 自校验仅覆盖经 phase-d-closer 的路径; **ad-hoc handoff 路径由 collector warning 兜底** (两层互补)。

## What Changes

1. **D.3 写后自校验子步** (`phase-d-closer/references/execution-steps.md` D.3 action + `references/handoff-mechanics.md`): fill template 写出后, 机械验证 5 字段齐全 —
   `head -8 <handoff> | grep -cE '^(track-id|owner-container|phase|status|updated-at):'` 须 ==5; 不足 → 补齐后重验, **不得带缺字段 handoff 进 latest.md pointer 更新子步** (warn-then-fix, 非硬 abort — handoff 是 prose 范畴, advisory-over-hardlock per DEC-20260519-001)。
   *(口径括注: grep 与 `parse_handoff_frontmatter` 判定略有差异 — 后者允许 frontmatter 内注释/空行; 模板实践无注释行故无影响, 但不应在 frontmatter 内插注释行以免 grep 误报。)*
2. **collector soft warning** (`collectors/handoff.py`): Phase 1.15 解析 **resolved latest doc 时 (`latest_path`, 无论 `latest_source` 为 pointer 还是 mtime fallback)** — mtime 路径正是 SilkNode ad-hoc 事故主场景, 不得只锚 pointer 路径。若 `parse_handoff_frontmatter` 判 legacy → `soft_error("handoff_frontmatter_missing", "<filename>: latest handoff lacks §2.3.1 frontmatter — multi-track board will show owner=unknown")`。**仅 latest 目标** (历史 legacy 不刷屏); snapshot additive 字段 `handoff.latest_frontmatter_missing: bool`, 不 bump `snapshot_schema_version`。
   - **实施注记**: `collect_handoff()` 当前只读 latest.md 指针文件本身、**不读目标 doc 内容** — 实现需在 latest 最终确定之后、`r.data` 构建之前, 对已解析的 latest `Path` 额外 `read_text()` 再传入 `parse_handoff_frontmatter`, 与 `latest_source` 值无关。
   - **fail-soft**: 新增 `read_text` 须 try/except OSError → 静默跳过 warning (与 `handoff_stat_failed` 同哲学, 不阻断 collect_handoff 返回); ~15 行估算含此 guard。
   - **边界**: `exists=False` (无 canonical handoff 文件) 时 `latest_frontmatter_missing=False` (文件不存在, 字段不适用, 与 `latest_path=None` 语义对齐)。
3. **standards 同步** (`standards/conventions/session-handoff.md` §2.3): 新增两层标注为 **"frontmatter content enforcement"** 独立小节/加注, 与既有 location enforcement 5 层明确区分, **不混入同一编号序列**。

## Impact

- **触及面**: `execution-steps.md` + `handoff-mechanics.md` (prose) / **`collectors/handoff.py` (复用同文件既有 `parse_handoff_frontmatter`, ~15 行; 本 Spec 不改 `handoff_multibranch.py`)** / 新测 / `state-snapshot-schema.md` additive 注释 / standards §2.3 / SOT 5+1 → v1.43.0。
- **测试清单**: ① pointer 路径: legacy latest → warning + 完整 frontmatter → 无 warning; ② **mtime-only 路径用例对: 无 latest.md pointer + latest 文件无 frontmatter → warning 触发 / 无 pointer + 有完整 frontmatter → 无 warning** (防 pointer-only 误实施时全绿漏网); ③ 历史 legacy (非 latest) 不告警; ④ exists=False → 字段 False 无 warning; ⑤ read_text OSError → fail-soft 无 crash。
- **不做**: 硬阻断 hook (advisory 哲学); 历史 legacy handoff backfill; frontmatter 内容语义校验 (只验字段存在); 不改 `handoff_multibranch.py`。
- **Rule #6**: deterministic collector → unit tests + dogfood substitute。
- **向后兼容**: legacy fallback 行为不变, 仅加可见性。
