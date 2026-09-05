---
checkpoint: post_spec
round: 3
mode: convergence
verdict: PASS_WITH_WARNINGS
converged: false
scope_ok: true
counts: 0C/16M/10m (五席原始合计, 去重前)
clusters: 0C
teams: [aria:tech-lead, aria:backend-architect, aria:qa-engineer, aria:code-reviewer, aria:knowledge-manager]
sibling_probe: no_sibling_found
timestamp: 2026-09-05T15:50:00.000Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
drift_terminated: false
drift_check_skipped: true
oscillation: false
overridden_by_user: false
degraded: false
---

# post_spec R3 — owner-container-identity-key-and-collision-parser (v3 `91b86fb`)

> **对象**: v3 (撤销等价类, 纯输入确定性规则, 新增 D-0)。**Sibling probe**: `no_sibling_found`, 双远端 152/156 全扫。**drift-checker**: 未 opt-in。
> **R2 处置核对**: 五席合计 closed 为主、partial 少数、open 0; R2 的三个 Critical 簇全部闭合 (等价类整体撤销后前提消失; 五席各自按 v3 字面在冻结语料上复现实验表三行与 7 个合成用例, **全部逐字一致**; 回归面经 monkeypatch 实跑只剩点名的测试)。
> **frontmatter 归一**: backend-architect 写 `verdict: REVISE`、qa-engineer 写 `verdict: FAIL`, 均为 0 Critical ⇒ 按 report-storage.md 判据归一为 PASS_WITH_WARNINGS (席位 vote 仍为 REVISE, 不改)。

## 判定

| 席 | verdict (归一) | counts | 一句话 |
|---|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | 0C/4M/2m | D-0(a)「语料中出现过」把语料依赖装回判定键 (纯形状剥离结论相同); 族键落点只能是 `track_to_claim_record`; S1 两条缓解不成立; D-3(a) 零落点 |
| backend-architect | PASS_WITH_WARNINGS | 0C/1M/0m | T3b 在 `release_gate` 侧无 identity 耦合、`release_claim_by_track` 内部重解析 ⇒ 会重演 #135 孤儿; SC-3 只点名 phase1_gate |
| qa-engineer | PASS_WITH_WARNINGS | 0C/4M/0m | SC-7 零回归与 SC-8 无条件存在互斥 (两条未点名测试断 keys 恰为 {kind, groups}); advisory「dedupe 前调用」无端到端锁; D-0(a) 无反例夹具 (语料现成 `-20260719` 尾段); SC-6 归因判据缺失且「真撞车」零样本 |
| code-reviewer | PASS_WITH_WARNINGS | 0C/3M/7m | 与 TL 同簇三条 (D-0(a) / S1 缓解 / D-3(a)); minor: 计数与行号精度、SC-2 统领句、fetch_gate 夹具类别错、SC-5 grep 未枚举 token、「基线 104」是语料 active 行数非测试数 |
| knowledge-manager | PASS_WITH_WARNINGS | 0C/4M/1m | 试写 standards 文本抓到: D2 判据丢「非 `unknown`」排除 (owner 真会取值 `unknown`); advisory 语料作用域 (同 track vs 全局) 未注明; `SKILL.md:149-154` 实含取值字面, 「只引用字段名」为假; 缺 aria-plugin 版本 bump 与发布同步面任务 |

**合并判定: PASS_WITH_WARNINGS / 五席 REVISE, 未收敛 (非全票 PASS)。** 与 R2 比较键集合不同 (R2 三 Critical 簇全闭合, 无一重开); 本轮零 Critical, Major 全部是 v3 新文本的**落点与判据精度**, 五席对判定模型本身无异议 (三席独立复现一致)。

## Major 簇 (去重后 9 条) 与处置 (rework v4)

| # | 簇 | 席位 | 处置 |
|---|---|---|---|
| M1 | D-0(a) 族键子句「仅当该 8hex 是语料中出现过的 identity_key」重新引入语料依赖; 冻结语料 117 个 track_id 只 1 个带 8hex 尾段 (日期 `20260719`), 纯形状剥离结论完全相同 | TL M-1 · CR M1 · QA M3 | **接受**: 改为**纯形状剥离** `-[0-9a-f]{8}$` (行内确定), 成文已知限制 (日期形尾段会被剥, 语料上零合并); 作用点**只在 `track_to_claim_record`** (Layer H 两条路径同源; Layer L claim 不经它); 加反例夹具: `x-20260719` 剥后不得与语料任何 key 碰撞、`slug-abcdefg` (7 位) 不剥、`slug-aaaa1111` + `slug-bbbb2222` 归同组 |
| M2 | S1 形态两条缓解不成立: ⚪ 只对 uuid key 产出 (label 形态 key 是 `owner/label`, 结构性零 ⚪); T3b 在 S1 无 flip 可拒、S2 管不到 session-closer 进程; SC-3 只断告警不断抑制 | TL M-3 · CR M2 | **接受**: 删除 Positive 的「⚪ 缓解」半句; T3b 重定义 = **两态**: S1 = 纯 inventory 告警 (label 非空 → 告警 + 列 `claims/<label>/` active 数, 无抑制); S2 = **发布门** (检查不过则本次发布不含 flip), 不是运行时开关。SC-3 拆 S1/S2 子句; Rule #6 substitute 集注明 SC-3 的 flip 臂只在 S2 |
| M3 | D-3(a) 选中即写代码, 但 Tasks / SC / collector-renderer 同源三处全零 | TL M-4 · CR M3 | **接受**: 新增条件任务 T13 + SC-11: 截止谓词做成共享函数 `layer_h_is_fresh(row, now, days)` (lib), collector 与 renderer 同一调用; 断言「被截止的行不出现在 groups」+「两处结论一致」; 常量 `LAYER_H_ACTIVE_WINDOW_DAYS` 与 `STALE_TTL` (秒) 分名分量纲 |
| M4 | SC-6「归因表由测试计算」缺可执行判据; 「真撞车」档冻结语料零样本 | QA M4 · CR m | **接受**: 判据机械化: 组内全部行 `updated_at` 早于 N 天 → `stale(#182)`; 否则按 kind: `cross_owner` → 真撞车, `self_multi_container` → 同人多机。零样本档: fixture 副本**注入**一组合成真撞车行, 显式标注为注入 (不冒充语料) |
| M5 | SC-7 零回归 vs SC-8 无条件存在: `test_real_collector_emits_cross_owner_collision` / `test_real_collector_no_collision_is_none` 断 `keys == {kind, groups}` | QA M1 | **接受**: 保留无条件存在 (additive 字段恒在, 空时 `[]`), **点名改写这两条测试** (T2); SC-7 措辞改为「点名改写后零回归」 |
| M6 | advisory「dedupe 前调用」接线无端到端锁: 接错则漂移信号 100% 消失 | QA M2 | **接受**: SC-2 加端到端夹具: 同 uuid 容器两串跨两份 handoff, dedupe 折叠后 advisory 仍恰 1 条; 反事实 (对 deduped 调用) → 0 |
| M7 | `release_gate` 侧 T3b 不可实现 (零 identity 耦合, `release_claim_by_track` 内部重解析) | BA R3-1 | **接受**: T3b 拆 phase1_gate / release_gate 两子任务; release_gate 需 import identity + 用公开 `get_container_label()` + `read_claims` 枚举 + 传 `identity=` 覆盖; SC-3 两处都点名 |
| M8 | D2 standards 文本漂移: 丢「非 `unknown`」排除 (owner 真会取 `unknown`, `identity.py:165-188`); advisory 语料作用域未注明 | KM A/B | **接受**: §2.3.5 判据句写「非空且非 `unknown`」; `same-identity-multi-owner` 作用域 = 采用方仓 handoff 全集 (跨 track, 跨分支) |
| M9 | `SKILL.md:149-154` 实含取值字面 `cross-owner` / `self_multi_container`, 「只引用字段名」为假; 缺 aria-plugin 版本 bump + 发布同步面任务 | KM C/D · CR m | **接受**: D4 改写为「SKILL.md 含取值字面但取值不变, 无需改动 ⇒ Rule #6 零 SKILL.md 改动成立 (取值语义变更经 §2.3.5 + CHANGELOG 明示)」; 新增 T12 发布同步 (aria-plugin PATCH, 按 CLAUDE.md §版本管理同步面; standards 版本口径按对方容器 M2 待裁项处理) |

## Minor (10 条, 全部纳入 v4)

D-2(c) 缺 `cross_owner` 可达性句 (TL m-1) · 「两人同机同 track → none」漏报镜像未进 Risk (TL m-2) · 头部计数 (12 checkbox; .py 六个含 phase1_gate/release_gate) (CR) · 行号精度 `track_board.py:743-747` 调用 / `collision.py:367` 分组 (CR) · SC-2 统领句「经 dedupe → classify」不适用 advisory 子句 (CR) · `advanced-rules.md:578` 保留在同步面 (CR) · T7 fetch_gate 夹具是 kind 字符串非两段式 (CR) · SC-5 grep 枚举 token (CR) · 「pytest 基线 104」= 4 文件子集, 全套 1492 个 test 定义 (CR) · Aether 指针落点建议 `docs/decisions/` 或 `.aria/decisions/` (KM m)。

## 收敛判断

R3 零 Critical, 五席对判定模型一致; 剩余为文本精度。v4 按上表闭合后进 R4; R4 若仍为「仅 minor / 可 B 期顺手」则按 SKILL 判据可投 PASS。max_rounds=5 剩 2 轮。

## 归档

席位报告: 同目录 `post_spec-R3-2026-09-05T150825-299Z-owner-container-identity-key-and-collision-parser-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md`
