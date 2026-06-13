# Proposal: i18n README 全量重译同步 + 防再漂机制

> **Status**: ✅ **done** (2026-06-13 实施完成 — 英文源校准 + 三语全量重译 + 防再漂 B 档 state-check dogfood PASS + CLAUDE.md checklist; AC-1~7 ✓, AC-8 Phase C/D parity)
> **Level**: 2 (Minimal — proposal.md;含维护策略, 故非 Level 1)
> **防再漂**: **B 档** locked (owner 2026-06-13): translated-from 标记 + state-check `i18n-readme-translation-currency` backstop
> **来源**: Forgejo Issue [#140](https://forgejo.10cg.pub/10CG/Aria/issues/140) (2026-06-04 raised, v1.38.0 ship 收尾发现)
> **Change ID**: `aria-i18n-readme-full-resync`
> **关联**: US-? (docs 维护, 无直接 US);Rule #3 文档同步

---

## Why (为什么)

主仓三个翻译版 README 的**正文内容**严重滞后, 且 badge 数字与正文不一致, 构成"假 current"误导:

| 文件 | badge (修前) | 正文时代 | 行数 | 性质 |
|------|------|---------|------|------|
| `README.md` (英文源) | v1.46.4 ✅ | 当前, 但**自身有数字漂移** | 273 | SOT, 需先校准 |
| `README.zh.md` | **v1.10.0** | v1.10.0 快照 | 267 | 完整翻译伪装权威, **无免责** → 真实债务 |
| `README.ja.md` | **v1.7.2** | v1.7.2 stub | 70 | 已带"翻訳準備中"免责, 仅 badge 假称版本 |
| `README.ko.md` | **v1.7.2** | v1.7.2 stub | 70 | 已带"번역 준비 중"免责, 仅 badge 假称版本 |

**Issue #140 核心论点**: 翻译版正文停留在旧时代 (Skills 数量、功能描述、版本表全旧)。**只刷 badge 数字到最新会造成"current 假象"——徽章宣称最新、正文实际差 30+ 版, 比直接显示旧 badge 更具误导性。**

**根因**: 版本发布检查清单 (CLAUDE.md §版本发布检查清单) **无 i18n README 同步步骤**, 加上全量重译成本高 → 每次发版静默跳过 → 累积滞后 36~39 版。与 root README badge 漂移 (memory `feedback_root_readme_badge_drifts_outside_submodule_sot`) **同类问题**: 派生显示物不在 SOT 内, 无机械闸 → 持续漂移。

**英文源自身漂移** (翻译前必须校准, 否则传播到 3 语种):
- L133 / L223: "33 user-facing + 3 internal (= 36 Skills)" — 旧值
- L221: "aria/ # Aria Plugin (submodule, **v1.13.0**)" — 残留旧版本引用
- L242: "41 Skills + 11 Agents" — 正确但与 L133/L223 自相矛盾

**权威当前数字** (本 session 核实: `find aria/skills -name SKILL.md | wc -l` = 41; `ls aria/agents/*.md` = 11; plugin.json = 1.46.4; aria/README.md L44 "34 user-facing + 7 internal = 41 total"):

```
Plugin v1.46.4 · 34 user-facing + 7 internal = 41 Skills · 11 Agents
```

---

## What Changes (改什么)

### 1. 校准英文源 (`README.md`) — 翻译前置

把英文 README 的 factual 数字/版本引用校准到 SOT (上方权威数字), 使 4 个 README 同一事实基线:
- L133 "Skills (33 user-facing + 3 internal)" → "34 user-facing + 7 internal"
- L221 "submodule, v1.13.0" → 移除硬编码旧版本 (或改 "submodule")
- L223 "36 Skills (33 user-facing + 3 internal)" → "41 Skills (34 user-facing + 7 internal)"
- L242 保持 "41 Skills + 11 Agents" (已对)
- 刷新 Skills 分类表 (L137-146) 使其与当前 41 Skills 名单一致 (补 issue-triage / aria-context-monitor / aria-doctor / ai-native-estimator / git-remote-helper 等新增, 不逐一穷举但消除明显缺漏)
- **保持英文 prose 结构/语气不变** (只校事实, 不重写叙述)

### 2. 三语全量重译 (以校准后英文为源)

- `README.zh.md`: 全量重译, 替换 v1.10.0 快照 → 与英文当前结构/内容对齐 (中文工作语言, 一等公民)
- `README.ja.md`: 从 70 行 stub 升级为**完整翻译** (移除"翻訳準備中"免责, 因不再是 stub)
- `README.ko.md`: 从 70 行 stub 升级为**完整翻译** (移除"번역 준비 중"免责)
- 三语 badge 统一 → **v1.46.4**
- 语种切换导航条 (L1) 保持各文件正确高亮

### 3. 防再漂机制 (Level 2 维护策略 — 核心)

> **决策点 (待 owner 在 approve 时定档)**: 防再漂强度。下方为推荐方案 (B 档)。

| 档 | 内容 | 代价 |
|----|------|------|
| A (advisory-only) | 仅 CLAUDE.md §版本发布检查清单 加一行 "i18n README 同步" | 不防漂 (同 root badge 教训, advisory 漏) |
| **B (推荐: advisory + 机械 backstop)** | A + 每个 i18n README 顶部加 `<!-- translated-from: v1.46.4 -->` 标记 + 新 custom state-check `i18n-readme-translation-currency` 比对标记 vs plugin 版本, 漂移 > 阈值 (默认 build) → warning | 中: 加 1 个 state-check (复用 m6-version-badge-match 模式) |
| C (mechanical hardlock) | B + release gate 阻断 (i18n 未同步不许 ship) | 高: 与 advisory-over-hardlock 哲学 (memory `feedback_concurrency_advisory_over_hardlock`) 冲突, 不推荐 |

**为什么 B 而非"i18n badge-match check"**: #140 核心是"正文滞后比 badge 滞后更糟"。单纯比对 badge 会诱导"只刷 badge 数字"——正是 issue 反对的。`translated-from` 标记比对的是"翻译自哪个版本", 检测**正文**滞后, 命中 #140 真实诉求。

### 4. 文档同步 (Rule #3)

- CLAUDE.md §版本发布检查清单: 加 i18n README 同步条目 (派生文件区)
- standards convention (可选, 视 owner): i18n README 维护策略说明 (full-translation policy + translated-from 标记契约)

---

## Scope / Out of Scope

**In scope:**
- 主仓 root `README.{zh,ja,ko}.md` 全量重译 + 英文源校准
- 防再漂机制 (B 档推荐)
- CLAUDE.md release checklist 更新

**Out of scope:**
- `aria/README.zh.md` (子模块自有 README, 维护良好 v1.46.4, 不在 #140 范围)
- i18n 自动化翻译 pipeline (CI 集成) — 若需要另起 cycle
- README 之外的 i18n (docs/ 正文、Skills 描述等)

---

## Acceptance Criteria

- [x] **AC-1**: `README.md` 英文源校准到 SOT (34+7=41 Skills / 11 Agents / 无 v1.13.0 残留; agent-router 归位 internal, arch-common 归位 internal, issue-triage 补为 user-facing); Skills 分类表无明显缺漏 — grep 验证落地
- [x] **AC-2**: `README.zh.md` 全量重译 (275 行), 结构与英文当前对齐 (12 sections), badge=v1.46.4, 无 v1.10.0 残留 — 主 loop 全文 review
- [x] **AC-3**: `README.ja.md` 升级为完整翻译 (275 行, 原 70 行 stub), badge=v1.46.4, 移除 "翻訳準備中" 免责 — 抽查 intro+表
- [x] **AC-4**: `README.ko.md` 升级为完整翻译 (275 行, 原 70 行 stub), badge=v1.46.4, 移除 "번역 준비 중" 免责 — 抽查 intro+表
- [x] **AC-5**: 四个 README 事实一致 (34+7=41 Skills / 11 Agents / 结构), 语种导航条各自正确高亮 — grep 验证
- [x] **AC-6** (防再漂, B 档): 三 i18n README 含 `<!-- translated-from: v1.46.4 -->` 标记; 新 state-check `i18n-readme-translation-currency` (dogfood via scan.py: PASS "OK 3 i18n READMEs current @ 1.46.4"; 负向测试模拟漂移 → STALE exit 1 确证)
- [x] **AC-7**: CLAUDE.md release checklist 含 i18n 同步条目 (advisory + backstop 注释)
- [ ] **AC-8**: Phase D 多远程 parity (origin + github) 齐平 — 待 Phase C/D

---

## Risks

| 风险 | 缓解 |
|------|------|
| 翻译质量/术语不一致 (3 语种独立) | 以校准英文为单一源; 技术 token (Skill 名/命令/版本) 保留英文不译; agent-team 分工时 disjoint 文件 + 统一术语表 |
| 英文源校准引入新错 (数字烧进 4 文件) | 数字已本 session 权威核实 (find/ls/plugin.json 三源); proposal 固化于此 |
| 防再漂 state-check 误报 | 复用 m6-version-badge-match 成熟模式; warning 级非阻塞; 阈值可配 |
| 重置时钟后再漂 | 正是 B 档防的; translated-from 标记 + check 是 backstop |
| 子模块/根仓混淆 | scope 明确仅 root README; aria/README.* 不碰 |

---

## Level 判定理由

Level 2 (非 Level 1): 虽含大量机械翻译, 但**引入 forward-binding 维护策略** (full-translation policy + 防再漂机制 + release checklist 变更), 属方法论约定层变更, 需 proposal 固化"为什么"与"如何持续"。非 Level 3 (无架构变更, 无需 tasks.md; 任务在本 proposal §What Changes 已枚举)。

---

## 实施提示 (approve 后 Phase B)

- 翻译可用 agent-team 动态工作流 (memory `feedback_agent_team_dynamic_workflow_division`): zh/ja/ko 三文件 disjoint, 低冲突 → 三 agent 并行; 英文源校准 + 术语一致性由主 loop 锚定
- 每 Edit 后 grep -c 验证落地 (memory `feedback_verify_edit_landed_grep_count`)
- Phase D 5+1 SOT: 本 cycle 非 plugin 发版 (不 bump plugin.json), 仅 root docs; 但需双远程 parity (memory `feedback_release_phase_d_5_files_synchronization`)
