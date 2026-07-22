---
track-id: session-close-20260722-claude-md-diet-116-root-fix
owner-container: simonfish/bfe8285d
phase: session-close
status: done
updated-at: 2026-07-22
---

# Session Handoff — 会话收尾: CLAUDE.md 官方规格瘦身 (#116 根因修复) + 臃肿进货口双堵 + #165 收窗裁定

> 会话维度增量。承接 [上一份 session-close](./2026-07-21-version-consistency-cleanup-and-meta-repo-tag-convention.md)（已 done 冻结）之后的一段。
> **本段主线是一次完整的「前提被推翻」**: #116 triage → brainstorm 收敛到整套补偿方案 (C+D+生命周期) → owner 朴素质疑「CLAUDE.md 不该描述 skill」→ 官方文档证实 → 根因修复使污染归零, 补偿方案整套降为备选。中途与 bot v1.64.0 ship 撞车一次 (rebase 化解)。

## §0 入口 (新 session 优先读)

- **当前态**: 主仓 `c13a232` / standards `f986a60` / aria `3694871` (v1.64.0, bot ship) — 三仓双远程一致 (逐个 ls-remote 核验)。custom checks **8/8 绿** (双预算新 check 生效)。CLAUDE.md **151 行 / 13.1KB** (曾 639 行)。
- **本段时序**: #165 证据评论 + [10cg.local #20](https://forgejo.10cg.pub/10CG/10cg.local/issues/20) (github egress 抖动) → owner 指示 triage #116 → confirmed/major (repro 3/3, [comment 16750](https://forgejo.10cg.pub/10CG/aria-plugin/issues/116#issuecomment-16750)) → brainstorm 3 问收敛 C+D+生命周期 → **owner 质疑前提** → claude-code-guide agent 查官方文档 (CLAUDE.md ≤200 行, skill 细节归 SKILL.md) → **根因修复** 639→149 行, 污染 4 术语→0 (`32dca5f`, DEC-20260722-001) → 撞车 bot v1.64.0 → rebase 折入 → owner 问「为什么老复发」→ 6 机制分析 → **堵两个进货口** (字节预算 24000 + hygiene §2.4 写入时刻纪律, standards `f986a60` / 主仓 `c13a232`) → #165 三条件盘点 3/3 ([comment 16845](https://forgejo.10cg.pub/10CG/Aria/issues/165#issuecomment-16845)) → **owner 裁定延长观察窗**。
- **下一步**: 见 §6。

## §1 已完成 (本段)

1. **#116 triage** — confirmed / major / next-cycle, repro 3/3 (cited 文件逐字吻合 + 4 污染术语实测 + 无 in-flight)。triage 产物入库 (`.aria/triage-report.json`, schema OK)。
2. **#116 根因修复 (本段最重)** — owner 质疑推翻「in-repo 恒污染」前提; 官方文档调研证实 CLAUDE.md 只该放稳定事实 (≤200 行目标), skill 设计内部归 SKILL.md。CLAUDE.md 按官方规格重写 **639→149 行** (ship 叙事移交 CHANGELOG/handoff/archive/conventions, 全部预先核实 canonical 家; 10 条规则保判据本体+指针, owner 裁决表全保留), 污染 4 术语 (各 1 次) → **全 0**。check 预算 640→**200**。DEC-20260722-001 记录转向: **C/生命周期/A 降为备选**, 裁决门 = 下次真实 Rule #6 AB 实测残余; **D + `:153` 判据修正保留为 #116 剩余 scope** (与污染独立)。#116 已更新 ([comment 16826](https://forgejo.10cg.pub/10CG/aria-plugin/issues/116#issuecomment-16826))。
3. **臃肿进货口双堵 (owner 指示)** — 侦察证实**零 plugin skill 指示写 CLAUDE.md 状态** (不触发 Rule #6): (a) check 加**字节预算 24000** (堵「行数不超单行爆表」长行钻空, 该空子实证被钻过); (b) standards `claude-md-hygiene.md` **v1.1.0 §2.4 写入时刻纪律** (「更新项目状态」定义收窄四条 + 点破 push 频道引力根源); (c) CLAUDE.md 状态段头「写入前读我」现场提示。
4. **#165 收窗盘点 + owner 裁定** — 三关闭条件 3/3 达成 (约束 2 捕获 ✅ / ≥3 干净 cycle ✅ 含**独立复核** bot 的 aria v1.64.0 本地 `--no-ff` 合并 / 无新事故 ✅), [comment 16845](https://forgejo.10cg.pub/10CG/Aria/issues/165#issuecomment-16845) + body 勾选同步。**Owner 裁定: 延长观察窗至 aria-orchestrator 在约束 1/2 下走过一次真实合并** (07-14 事故路径, 窗内未覆盖) — 下一次 orchestrator 合并即收窗判定点 (comment 16848 + body 更新)。
5. **10cg.local #20 开单** — dev box → `ssh.github.com:443` 推送瞬时失败 (误导性 "access rights" 报错, 重试即恢复); 与 #165 正交互链。本段 coordination_fetch 超时再添一例佐证。
6. **撞车处理** — bot 并发 ship v1.64.0 (#113 轨 Phase C+D 闭合) 致双远程拒推; fetch→rebase→冲突仅 CLAUDE.md 状态段 (取我方重写+折入 v1.64.0)→重推核验。aria 子模块同步到 `3694871` (stale checkout 曾致 2 check 假红, 即 memory `feedback_stale_submodule_checkout_masquerades_as_broken_ship` 的实景重演)。

## §2 未完成 / Carry-forward

**AI 内省 (load-bearing)**:

- 🔴 **凭据轮换 — 本段是第七次 surface 无闭环**: `FORGEJO_TOKEN` / `NEXUS_API_TOKEN` / `CF_ACCESS_CLIENT_SECRET`。bot 07-22 handoff 记「第六次未回, **hard cap 2026-08-02 (剩 ~11 天)**」— 唯一带硬期限的 carry。本段开场推荐里我列了它, owner 选了其他工作。**owner-gated, 我无法独立闭环, 但 cap 在倒数。**
- **#116 剩余 scope (可独立小 cycle)**: D 钉产出形态 + `:153` 判据改「三臂全过先语义分档再裁拆/删」— `AB_TEST_OPERATIONS.md` 文档修订, 与污染无关、独立成立。C/生命周期/A 在 DEC-20260722-001 挂备选, **裁决门 = 下次真实 Rule #6 AB** (届时实测 baseline 残余搬运并记回 #116)。
- **#165 观察窗 (owner 已裁)**: 等 **aria-orchestrator** 子模块下一次真实合并走约束 1/2 → 那一刻即收窗判定点。届时核验: 本地合并 (非 Do: merge) + 双推 + ls-remote + gitlink 无 orphan, 然后可关。
- **10cg.local #20**: 等基建响应; 若 coordination_fetch / push 抖动继续可追评佐证。
- **承前 owner 门**: #168 (5 deferred + AC-5 语义, 需 owner 裁三项) / #169 (AC-5 落位重构) / M6 四门 + 168h 跑 / M7 fleet。bot 本段另开 #117-#122 (含 #122 Rule #8 恒-wait 真机制) — 未 triage。

**机械补漏 (backstop)**: `handoff_autofill` 159 条 unfinished 全属 6 个活跃 M6/M7 spec (本段零碰); consistency 6 flags 全结构性 (Aria 无 UPM); sync 零 warning。**本段零机械残留**。

## §3 关键风险 / 已知陷阱 (本段新增)

- **「结构性」断言差点变成基建**: brainstorm 已收敛到 C+D+生命周期三层方案, 若 owner 没质疑一句, 一整套补偿机制会建立在「恒污染」这个假前提上。→ memory `feedback_verify_structural_premise_against_official_docs` (本段核心教训)。
- **撞车三连环的形态更新**: 本段撞车不是 collision.kind 报警 (开场 scan 时 bot 未推), 而是 push 时双远程 non-ff 拒推才发现 — **干活期间远程可以随时被并发推进**, push 前的 parity 自查不替代 push 失败后的 fetch-first 反射。化解全程沿用既有 memory (concurrent_sot_conflict / stale_submodule_checkout), 无新 memory 需要。
- **CLAUDE.md 大重写与并发 bot 编辑的冲突面**: bot 只改一行 (footer 版本), 我改整个文件 — 冲突解法「取重写 + 折入对方新事实」依赖**逐行读对方 diff**, 不能盲取 `--theirs`/`--ours`。本次对方 diff 极小是运气, 下次未必。

## §5 多维度同步状态 (机械核验)

- **git**: 主仓 `c13a232` / standards `f986a60` (v1.1.0 hygiene) / aria `3694871` (v1.64.0) — 全部 origin=github (逐个 ls-remote), aria-orchestrator `86bb684` detached 只读未动。
- **custom checks**: 8/8 绿, 含新双预算 check (`OK 151 lines, 13139 bytes`)。
- **规范/决策新增**: standards `claude-md-hygiene.md` v1.1.0 (§2.4 + 双预算) | 主仓 DEC-20260722-001 | CLAUDE.md 重写 (639→151 行含现场提示)。
- **issue 面**: #116 (triage + 前提改判 + 根因修复, 2 评论) / #165 (盘点 + owner 裁定, 3 评论 + body 2 轮更新) / 10cg.local #20 (新开)。
- **#165 观察窗新证据**: 本段 standards hygiene ship = 第 3 个干净跨子模块 cycle (进 16845 盘点)。

## §6 Next session 入口 + 优先级

1. 🔴 **凭据轮换** (第七次, bot 记 hard cap **2026-08-02**) — owner 亲自操作项, 逾期前最后窗口。
2. **#165 收窗判定点**: 下一次 aria-orchestrator 子模块合并 → 按约束 1/2 走 + 核验 → 三条件复核后可关。
3. **#116 剩余小 cycle**: D 产出形态 + `:153` 语义分档 (AB_TEST_OPERATIONS.md 文档修订, 自包含)。
4. **下次 Rule #6 AB 触发时**: 按 DEC-20260722-001 决策 4 实测 baseline 残余搬运 → 裁 C 去留, 记回 #116。
5. bot 新开 #117-#122 待 triage; 承前 #168 / #169 / M6 门 / M7。

## §7 本段对方法论本身的影响

- **「结构性问题」的核查义务成文**: 为不可消除的问题建补偿机制前, 必须先对官方/上游规范核实「不可消除」是否真的是结构 — #116 的「恒污染」被证实为「文档违反自身规格 (639 行 vs 官方 ≤200)」的条件性产物。修根后测量环境本身变干净, 比任何补偿机制都便宜。
- **臃肿治理从「存量清理」升级为「进货口约束」**: 复发病 (07-03 首瘦 69K 字符 / 07-22 二瘦 639 行) 的根子是六个进货机制 (push 频道垄断 / 加删激励不对称 / 方法论项目身份 / 锚定现状的 enforcement / 成本不可见 / 外部校准缺位)。§2.4 把「更新项目状态」的定义收窄在写入时刻, 双预算堵住度量钻空 — 这是第一次动进货侧。
- **#165 观察窗方法论自洽**: 三条件盘点严格区分「机械事实 (3/3 可勾)」与「收窗决定 (owner 裁)」; owner 选择延长至事故原路径 (orchestrator) 被真实覆盖 — 「条件亮了」≠「立即关」, 覆盖面优先于速度。
- **bot 轨的合规被独立验证**: aria v1.64.0 的 `3694871` 经 merge 形态 + 双远程 SHA 独立复核确认守约束 1/2 — 多远程规范对人类 session 与自主运行时**同时生效**的首个双向实证。

## §8 Memory entries this session (本段)

**已落 (1 条新)**:
- `feedback_verify_structural_premise_against_official_docs` — 为「结构性」问题建补偿机制前先对官方规范核实前提; 「恒污染」实为违规的条件性产物。与 `feedback_perpetual_red_check_may_encode_stale_convention` / `feedback_match_evidence_class_to_solution_class` 成「先质疑前提」三件套。

**本段未落 (已有覆盖)**: 撞车 rebase (`feedback_concurrent_sot_conflict_mechanical_resolve`) / 子模块 stale checkout 假红 (`feedback_stale_submodule_checkout_masquerades_as_broken_ship`) — 两条都在本段实景重演并被正确应用, 覆盖有效。

## Cross-references

- 上一份 session-close: [2026-07-21-version-consistency-cleanup-and-meta-repo-tag-convention.md](./2026-07-21-version-consistency-cleanup-and-meta-repo-tag-convention.md)
- 并发 bot 轨 (同段): [2026-07-22-issue113-ship-v1.64.0-and-rule6-third-row.md](./2026-07-22-issue113-ship-v1.64.0-and-rule6-third-row.md)
- 决策: `docs/decisions/DEC-20260722-001-ab-baseline-pollution-root-fix-first.md`
- 规范: `standards/conventions/claude-md-hygiene.md` v1.1.0 (§2.4)
- issues: [aria-plugin #116](https://forgejo.10cg.pub/10CG/aria-plugin/issues/116) / [Aria #165](https://forgejo.10cg.pub/10CG/Aria/issues/165) (观察窗延长) / [10cg.local #20](https://forgejo.10cg.pub/10CG/10cg.local/issues/20)
