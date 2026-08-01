---
verdict: PASS
agent: knowledge-manager
round: R1
critical_count: 0
major_count: 0
minor_count: 3
---

# post_spec R1 审计报告 — knowledge-manager (文档一致性 / 规范符合度)

审计对象: `/home/dev/Aria/openspec/changes/session-closer-autofill-yaml-datasource/proposal.md` (aria-plugin #121, Level 2 Minimal)

## 核对项与结论

### 已核对、无 finding

1. **Rule #5 (Spec 落位)**: 满足 — 文档位于本项目 `openspec/changes/`, 非 `standards/openspec/changes/`。
2. **命名谱系惯例**: `session-closer-autofill-yaml-datasource` 与母 spec `state-scanner-gate-yaml-datasource` (#113, 已归档 `openspec/archive/2026-07-22-state-scanner-gate-yaml-datasource/`) 遵循同一 `<skill>-<动作>-yaml-datasource` 命名模式, 一致。归档路径本身核验存在。
3. **Status 字段归一化**: `Status: Draft` 经 `collectors/_status.py::_normalize_status` (pending family, 含 draft/pending/placeholder) 可正确归一, 且与模板默认值 (`proposal-minimal.md` L4 `> **Status**: Draft`) 字面一致。
4. **rule6_note 与 `skill-benchmark-exemption.md` 判据对表**: 本次改动对象是 `handoff_autofill.py` 的纯代码函数 (`grep_unchecked_tasks`), 非 SKILL.md / references/rules 指令面, SKILL.md description 零变动。这与 SOT §5 已裁定样例表中 `state-scanner-stale-refs-false-parity` v1.59.0/v1.60.0 (「纯代码」→ substitute) 同型, rule6_note 的 "substitute: SC 级 baseline-failing 结构化测试" 措辞与 §2 决策表第一行处置描述吻合 (「SC-1 必须在未修代码上 FAIL、修后 PASS」对应「baseline-failing 单元/集成测试, 必须在场」)。判据归类正确, 不属于会被 §3 「第三行不是逃生舱」拦下的场景。
5. **Impact 段 ship 同步面 vs CLAUDE.md 版本管理段**: proposal 写「aria 子模块 5 文件 + 主仓 gitlink + VERSION + README badge (i18n 正文无实质变更, #140 B 档免重译)」, 与 CLAUDE.md「发布同步面: aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION + root README badge + i18n README (仅正文实质变更才重译, #140 B 档)」逐项对应, #140 B 档援引正确。
6. **版本号推导**: `aria/.claude-plugin/plugin.json` 当前 SOT = 1.65.0 (已核验); proposal 声称 bug 修复 = PATCH → v1.65.1, 与 CLAUDE.md「文档更新/bug 修复 = PATCH」惯例及算术均正确。
7. **交叉引用真实性 (代码行号/函数签名)**: 逐条核对 `aria/skills/session-closer/scripts/handoff_autofill.py` —
   - `grep_unchecked_tasks` def 落在 L160 (proposal 引「L160-175」, 下一函数 `_normalize_followup` 起于 L178, 引用区间贴合);
   - `owner_container()` 内 `Path(__file__).resolve().parents[2]` 绑定块精确落在 L317-321 (proposal 引「L317-321」, 逐行核对: 317 注释/318 `_ss_root=`/319 `if`/320 `insert`/321 `import`, 完全命中);
   - `_benign_unconditional_reasons()` 内同类绑定块落在 L46-50 (proposal 引「L46-50」, 同样逐行命中)。
   三处行号引用均为一次性精确核验通过, 非估读。
   - `parse_detailed_tasks(text) -> dict` 返回 `{"parse_ok", "tasks":[{"id","raw_status","title"}], "reason"}`、`is_done_status(raw_status) -> bool` 两个签名与 proposal §What 第 2 点描述的取数/判据字面一致 (`state-scanner/scripts/lib/detailed_tasks.py` L104/L225 核验)。
   - Key Deliverables 声称的两个落点文件 (`handoff_autofill.py` / `tests/test_handoff_autofill.py`) 均存在; 现有测试对 `grep_unchecked_tasks` 仅覆盖 tasks.md 路径与不存在目录两态 (L242-253), 与 proposal 「yaml fallback 当前未测, SC-1 应在未修代码上 FAIL」的基线声称相符。

### Finding 1 (Minor) — 章节顺序与 Level 2 Minimal 模板不一致

**位置**: proposal.md 全篇章节顺序 (## Why → ## What → ## 关键决策 → ## Impact → ## rule6_note → ## Success Criteria → ## Tasks)。

**主张**: `standards/openspec/templates/proposal-minimal.md` 规定顺序为 Why → What → Impact → **Tasks → Success Criteria** (模板 L27-37, Tasks 段先于 Success Criteria 段)。本 proposal 把 Success Criteria (L53-61) 放在 Tasks (L63-67) **之前**, 与模板顺序相反。

**证据**: 模板原文 L27 `## Tasks` 早于 L33 `## Success Criteria`; 本 proposal L53 `## Success Criteria` 早于 L63 `## Tasks`。

**影响**: 纯结构性, 不影响机读 (state-scanner 不解析章节顺序), 内容完整无缺失。母 spec (#113) 也是 Success Criteria 先于 Impact/无独立 Tasks 段的非模板顺序 (量级更大, Level 2 标签下实质走了 Level 3 结构), 说明本谱系两代 spec 都对模板顺序有自由发挥的先例, 非本 spec 独创偏离, 建议知会但不阻塞。

### Finding 2 (Minor) — 缺失模板要求的 `Created` 字段

**位置**: proposal.md 头部 metadata 块 (L3-6)。

**主张**: `proposal-minimal.md` L5 规定 `> **Created**: {YYYY-MM-DD}` 为头部必填字段之一。本 proposal 头部仅有 `Level` / `Status` / `Issue` / `根因谱系` 四行, 无 `Created` 行。

**证据**: 对比同谱系母 spec `2026-07-22-state-scanner-gate-yaml-datasource/proposal.md` L4 `> **Created**: 2026-07-19` (有); 但横向抽查当前 `openspec/changes/` 下其余全部 6 个在飞 spec (aria-2.0-m6-*/m7-*) 头部同样均无 `Created` 字段 — 说明这是近期活跃 spec 的普遍性模板漂移, 并非本 proposal 独有问题 (已归档的历史 spec 普遍保留该字段, 提示 `Created` 字段可能是在 Phase D 归档时才补齐, 而非 Draft 阶段惯例)。若该假设成立则不算真缺陷; 若不成立则应在本 spec 定稿前补一行。建议 Phase B 前补齐以维持模板合规, 不阻塞 Phase A 收敛。

### Finding 3 (Minor) — import 先例引用的精确度可再收紧

**位置**: proposal.md 「关键决策」表第 3 行 (「import 路径 | sys.path 插 `scripts/lib` + 裸模块名 | ... spec_complete L342 同款先例」) 及正文第 3 点。

**主张**: `spec_complete.py` L342-356 的 `try: from detailed_tasks import ... except ImportError: sys.path insert(自身父目录) + import` 处理的是「包内相对导入 vs. CLI 独立运行」的**同目录**双上下文, 而本 spec 需要的是**跨 skill**（`session-closer/scripts` → `state-scanner/scripts/lib`）路径定位, 后者的正确先例是本文件自身已有的 `owner_container()` / `_benign_unconditional_reasons()` 两处 `Path(__file__).resolve().parents[2]` 模式 (proposal 也已正确单独引用这一半)。把 spec_complete.py 引作「同款 dual-context 模式」的先例, 对应的应仅是「sys.path 插入后用裸模块名导入以规避顶层名污染」这一子技术, 而非「跨 skill 定位」整体模式；两者共同出现在同一句先例引用里, 容易让 Phase B 实施者误读为 spec_complete.py 本身处理过跨 skill 场景。

**证据**: `spec_complete.py:342` `_LIB_DIR_DT = str(Path(__file__).resolve().parent)` — 是 `.parent` (同目录), 非 `.parents[2]` (跨 skill 兄弟目录); 注释原文明确「pragma: no cover - CLI sys.path bootstrap (mirrors carry_forward)」, 场景是 CLI 独立调用引导, 不涉及跨 skill。

**影响**: 不改变最终代码落地方向 (proposal 决策本身正确, 两条技术线都已各自引用到位), 纯属先例归因的措辞精度问题, 不阻塞实施, 建议 Phase B 编码时以 `owner_container()`/`_benign_unconditional_reasons()` 为主要先例, spec_complete.py 仅作「裸模块名导入」技术点的旁证。

## 结论

0 Critical / 0 Major / 3 Minor。三条 Minor 均不涉及事实性错误或规范违反的阻塞项, 核心决策表、rule6_note 分类、版本/同步面声称、交叉引用行号与函数签名均逐一核验通过。判定 **PASS**。
