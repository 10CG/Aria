---
checkpoint: post_planning
round: 2
mode: convergence
verdict: FAIL
converged: false
scope_ok: true
counts: 2C/3M/1m (三席原始 6 条; 反驳席推翻 2)
clusters: 2C
teams: [aria:code-reviewer, aria:backend-architect, aria:qa-engineer]
sibling_probe: no_sibling_found
timestamp: 2026-09-07T07:27:11.638Z
context: openspec/changes/archive-gate-registration-class-and-skill-drift/tasks.md
drift_terminated: false
drift_check_skipped: true
oscillation: false
overridden_by_user: false
degraded: false
max_rounds: 5
rounds_total: 2
---

# post_planning R2 — archive-gate-registration-class-and-skill-drift

## 逐席 verdict

| 席 | verdict | 结论 |
|---|---|---|
| aria:code-reviewer (R1 修订落地核验) | **FAIL** | 11 条 **9 条完全落地 / 1 条部分 / 1 条把阻塞面写错**; 另发现 R1 修订自身引入的回归 |
| aria:backend-architect (Phase B 阻塞性) | PASS_WITH_WARNINGS | 「可以进入 Phase B」; 11/11 落地; 1 Major (B-14 丢失) |
| aria:qa-engineer (顺序依赖与并发安全) | **FAIL** | 顺序图逐条核对**除 F1 外全部写对**; 并发写集合**完全 disjoint 零冲突** |

## 两条 Critical — **都是我 R1 修订自己造的**

### F-1: R1 修订静默删除了 B-14, 且把计数改到自洽

`git show 240ea4c` 的 diff 逐字:

```
-## TG-B — CLI 漂移类级收口 (20 行, 两个 SKILL.md + 两份 README)
+## TG-B — CLI 漂移类级收口 (17 条, 两个 SKILL.md + 两份 README)
-- [ ] **B-14** `:622` 悬空引用 → `openspec/archive/2026-07-05-aria-archive-gate-runtime-reality/`
```

**同一 hunk 里删任务 + 改计数 ⇒ 删完自洽, 数数根本核不出来。**

而它是 proposal 在册交付物 (`:67` 有 B14, `:159` 的 Rule #6 范围写「B1-B14」), 且 **SC-1 的 pattern 对 `:622` 实测命中 0** ⇒ **现有验收零覆盖**。R1 报告全文对 `B-14`/`622` 零命中 ⇒ 该条从未被提出过。

**已补回** + 新增专属验收 **B-V8** (基线实测为红: `:622` 现指 `openspec/changes/aria-archive-gate-runtime-reality/`, 该目录不存在; 正确目标 `openspec/archive/2026-07-05-...` 存在)。标题计数 17 → **18**。

### F-2: E-0 的不阻塞范围允许在 owner 裁定前双推发布

R1 版逐字: 「E-0 不阻塞 TG-B/TG-C/TG-D 与 **E-2..E-8**; 它只挡 E-9。停在 E-8 之后」。

但 **E-7b 就是「aria 子模块本地 merge → master + 双推」** —— 它会在 owner 对 SC-11 表态前, 把 v1.72.0 (**含 SC-11 正要问的 B-15 phase-d-closer 与 C-1/C-9 state-scanner 改动**) 不可逆地发布到两个公共 remote。

proposal SC-11 明写「取得答复前**不得进入 C.2**」, 而按 CLAUDE.md 与本仓惯例, **子模块合并推送就是 C.2 的一部分**, 不只是主仓 PR 合并。

⇒ 这是 **R4 GOV 刚抓过的「自行豁免闸门」换个任务粒度重演**。我 R1 为「解决阻塞问题」加的那条修复, 自己造了一个新的自行豁免 —— memory `fix-recurs-in-fallback` (修复类改动最易在自己新写的兜底路径重犯要治的病), **本 cycle 第四次**。

**已订正**: 不阻塞范围收窄到 **E-1..E-6**; E-0 挡 **E-7a 起的全部步骤**; 「停在 E-6 之后, 不合并也不推任何 remote」。

## 其余处置

- **F-3** (Major): E-5 写「贴 12 行计数」而 proposal `:147` 写「贴 **13** 行 (不留不对称缺口)」⇒ 改为贴全 13 行, `aria/CHANGELOG.md` 那行标注「历史条目, 不改」。
- **ORD F2** (Major): 已知风险 5 (负控夹具还原) 是一句无验收的忠告 ⇒ 新增 **C-V4** (跑完核 `git status` 确认 `spec_complete.py` 未被修改)。

## 三席一致确认的正面结果 (供收敛判断)

- **顺序依赖图**: 除 F1 外**逐条写对** —— C-3 基线态先于 B-1/B-2 ✓ / C-4 在 B-2 后 ✓ / E-7a→E-7b→E-8→E-9→E-10 五步递推关系正确且必要 ✓。「未写出的顺序依赖: 除 F1 外未再发现」。
- **并发安全**: TG-B 与 TG-C 的写集合**完全 disjoint, 零写写冲突**; 唯一交叉是 TG-C 对 SKILL.md 的两次**读**, 均已被显式排序保护。
- **R1 的 11 条修订实测复现**: SC-1 区段外 15 ✓ / 版本串 23 处 13 文件 (减 CHANGELOG 历史条目 = 22/12) ✓ / 主仓 master **仍落后 origin/master 8 个** ✓ / aria 子模块 `3a28339` **仍未推任何 remote** ✓ / E-V1 四串**写全且均可 grep** (串内无 markdown 强调符) ✓ / C-V3 的判据输入实测存在 (`custom_checks.results[]` 有 `name`/`status`, `enabled:false` 会被 `collectors/custom_checks.py:437` 整条 continue 掉 ⇒ 非恒真) ✓。

## 收敛趋势

| 轮 | Critical | Major | 性质 |
|---|---|---|---|
| R1 | 1 | ~20 | 转写时丢承重限定词 + 顺序/时点 |
| **R2** | **2** | **3** | **两条 Critical 都是 R1 修订自身引入** (一条静默删任务并改计数到自洽, 一条修复自造新豁免) |

Major 20 → 3 大幅下降; 但 Critical 1 → 2 且**全部自造** ⇒ 与 post_spec R4 同形 (「看起来快收敛了」时最容易漏)。**照开 R3。**
