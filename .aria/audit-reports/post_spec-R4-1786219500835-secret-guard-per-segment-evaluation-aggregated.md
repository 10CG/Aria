---
checkpoint: post_spec
round: R4
spec: secret-guard-per-segment-evaluation
timestamp: 1786219500835
date: 2026-08-08
seats: 5
verdicts: REVISE×5
converged: false
max_rounds_exhausted: true
critical_raw: 6
critical_deduped: 5
major_raw: 13
minor_raw: 17
owner_decision_required: true
---

# post_spec R4 汇总 — secret-guard-per-segment-evaluation

**R4 是 `.aria/config.json` `audit.max_rounds: 4` 下的最后一轮。5 席 verdict 全部 REVISE, 未收敛, `max_rounds` 耗尽 ⇒ 按 Rule #10 须 owner 裁定, AI 不得自行判定接受。**

## 四轮趋势 (各席 frontmatter 原始加总, 未跨席去重)

| 轮次 | 席数 | Critical | Major | Minor | verdict 分布 |
|------|------|----------|-------|-------|--------------|
| R1 | 5 | 6 | 19 | 16 | REVISE×5 |
| R2 | 5 | 5 | 12 | 13 | REVISE×5 |
| R3 | 5 | 4 | 13 | 17 | PASS×1 + REVISE×4 |
| **R4** | 5 | **6** | 13 | 17 | **REVISE×5** |

Critical 三轮下行 (6→5→4) 后在 R4 **回升到 6**, 且 R3 唯一那席 PASS 在 R4 转为 REVISE。**这不是收敛曲线**。

但趋势数字本身会误导, 必须配合下一节读: R4 新增的 Critical **不是旧问题没修**, 而是 v4 新拉回范围 (`has_filter` 13 处转内建) 引入的新面。旧问题这一轮修得相当好 —— tech-lead 记 `r3_resolved 6/14`, 并称「v4 是四版里第一次把锁改对的」。

## Critical 去重后 5 条

| # | 条目 | 来源席 | 部署可达性 |
|---|------|--------|-----------|
| 1 | **13 处转内建不是语义保持变换** —— `grep` 逐行 vs bash `[[ =~ ]]` 整串, 多行 command 上判定翻转且方向是**漏拦**。SC-15 的 26 条与 SC-11 全语料结构上都抓不到 | tech-lead R4-C-1 **+** backend-architect CRITICAL-1 (**两席独立发现, 高置信**) | 高 — 可端到端复现的 fail-open 安全回归 |
| 2 | **判据表 `exec` / `time` 行漏写「仅命令位置」** —— 按字面实现会让含 `runtime` / `timeout` / `execute` / `timestamp` 的日常命令整条降级, 修复静默失效; 两种读法对 305 条语料产出**完全相同**, 无一 SC 能分辨 | tech-lead R4-C-2 | 高 — 静默失效, 现有 SC 全盲 |
| 3 | **「命令位置」的「换行之后」在朴素 bash ERE 翻译下不成立** —— `^` 不锚定每行行首, 循环体第 2 行起漏检, 重开 v2 那类误报; proposal 自己举的例子并未真正测到换行场景 | backend-architect CRITICAL-2 | 高 |
| 4 | **SC-16 与 §6 的事实前提错误** —— 声称 bash POSIX ERE 不支持 `(?:…)` / `\b` / `\s`; **实测三者中两个是支持的**。13 处 credit 里有 2 处含 `\b`: 逐字搬运违反 SC-16, 改写又动语义违反 SC-15, Rule #10 下两闸都不可自行豁免 | code-reviewer C-1 | 高 — 判据自相矛盾, 实现无合法出路 |
| 5 | **Task 1.9「开转出 1-6 issue」与刷新后的清单矛盾** —— 转出 6 已由 owner 拉回本 spec 范围 (不该开票), 转出 8 (R3-C-2 新增) 漏在范围外没被开票 | knowledge-manager C-1 | **低** — 文档/流程错, 一行改法, 不产出运行时缺陷 |

第 5 条按「部署可达性」判其实达不到 Critical 量级 (改一行文字, 不会 ship 出 bug); 若按可达性重排, **实质 Critical = 4 条, 且全部集中在两个面**: §What.1 判据表的精确性 (2、3) 与 §What.4 13 处转内建的语义保持 (1、4)。

### 独立复验 (主 loop 亲验, 不采信单席结论)

第 4 条影响面最大, 我自己在 bash 5.2.15 / glibc 上复验:

```
\bbar\b  vs 'foo bar'  → MATCH        (正例)
\bbar\b  vs 'foobar'   → no-match     (负例, 词边界真生效)
a\sb     vs 'a b'      → MATCH
\w+      vs 'abc'      → MATCH
(?:a)b   vs 'ab'       → no-match rc=2 (编译失败)
```

**code-reviewer 成立**: 只有 `(?:` 真不支持, `\b` / `\s` / `\w` 都支持 (glibc GNU 扩展)。`secret-guard.sh` 里 19 行含 `\b` 且 366 条测试全绿, 是活证据。该错误可追到 R3 backend-architect M-2, 作者忠实照抄 —— **spec 继承上游审计席的代码级错误**, 忠实不等于正确。

## 本轮的正面结论 (同样是审计产出, 不该只报坏消息)

**owner 2026-08-04 拉回 §What.4 的裁决被三席独立实测证实方向正确**:

| 席 | SC-8 四档实测 | 结论 |
|----|--------------|------|
| tech-lead | −67% ~ −85% | 四档全过 |
| backend-architect | −79.9% ~ −28.7% (两种独立计时法交叉验证) | 阈值达标且有边际 |
| code-reviewer | 最坏档 −38% | 支持拉回 |

R3 的 `+583%` 最坏负载问题**已实质解决**。代价是把风险从性能面移到了语义保持面 (即 Critical 1 与 4) —— 这是一次有明确收益的风险转移, 不是失误。

**留给 R4 的 SC-9 设计问题 (本轮唯一 5/5 收敛的议题)**: 五席方向一致 —— **保留 canonical 直调作主闸, 另加一条 harness / 投递面的腿**, 而非二选一。各席论据互补:

- tech-lead: 实测 harness 链在 Phase B 结构上跑不到本 spec 的改动 ⇒ 新腿应放在 **ship 后的投递面** (SC-9b)
- qa-engineer: **时序矛盾** —— pre-merge 闸验的是 PR 里的代码, 不是已部署的 cache, 两者本就不同物
- code-reviewer: 拆 SC-9a (canonical) + SC-9b (harness 链 + `cmp` 字节相同前置)
- backend-architect / knowledge-manager: 双腿并存; km 另指出与 Aria#178 的边界 (#178 是规范层, 本 spec 是单点应用)

## 范围问题的回答

主 loop 在派单前提出过一个假设: 三轮 Critical 只降 2 条, 可能问题在于 spec 一次吃「分段 + fail-safe 降级 + credit 判据重构」三件事, 该缩范围。

**tech-lead 给出的答案是不缩范围**: 可在一个 cycle 内交付, 但须拆成**两个顺序 PR**。该结论基于其对 v4 全语料的实测 (fail-safe 机制本体全语料仅 1 条设计内翻转), 比主 loop 的曲线外推更有据。记录在此以免该假设被当成结论传下去。

## 席间分歧 (未收敛项, 交 owner)

- **SC-16 的有效性**: code-reviewer 判其前提事实错误 (Critical); qa-engineer 判其「有效, 仅反事实表述夸大」(Minor)。经主 loop 实测, **code-reviewer 正确** —— qa 这一席漏了前提核实, 只审了表述。
- **是否需要 R5**: knowledge-manager 称「两项阻塞均为一行/一句文本改法, 建议 owner 直接采纳后 ship, 无需 R5」—— 该结论**只在 km 自己的镜头内成立**, 未考虑 tech-lead / backend-architect 的 4 条运行时 Critical。不应据此认为可直接 ship。

## 判定

```
converged: false
max_rounds_exhausted: true (4/4)
owner_decision_required: true
```

依 Rule #10 与 `.aria/config.json` audit 段注释: 已 enabled 的 checkpoint 不得由 AI 自行豁免或判定接受。降级策略须由 owner 显式裁定 (先例: `phase-c-integrator-ci-path-coverage` 2026-07-26 owner 裁定 [1] 接受当前结论 ⇒ `converged: false, overridden_by_user: true`, 进 A.2)。
