---
agent: backend-architect
round: R2
verdict: REVISE
scope_check: SCOPE_OK
critical_count: 1
major_count: 1
minor_count: 2
---

# post_spec 审计 R2 — backend-architect (闭合核验)

## R1 闭合核验

- BA-1 (glob 未建模方向): **CLOSED** — §1 显式判匹配 + SC-14 字符类/否定/大小写。
- BA-2 (仓边界契约): **PARTIAL** — §0 契约文字消除核心风险; 但「主仓 cwd 评估子模块内变更」负向 SC 未落, `git rev-parse --show-toplevel` 机制本身无 SC 锁 → 残留 Minor。
- BA-3 (语料矛盾): **CLOSED** (Bash 实核真实文件一致; SC-23 覆盖)。
- BA-4 (优先级): **CLOSED** (规则 5 + SC-24)。
- BA-5 (unknown 可观测): **CLOSED** (D9, 每次出现即上报, 强于原建议)。
- BA-6 (键范围): **CLOSED** (实码核对: 5 处早退分支全直调 _build_output 六键, compute_verdict 唯一终点 — 与 proposal 精确匹配; Impact 已列 _build_output)。
- BA-7/8/9: **全 CLOSED**。

代码层交叉核验: query 顺序 :317→:330 吻合; CIStatus Literal 不含 not_applicable。规则 1 vs 2 排序表述不精确但不产生行为分叉 (已排除不计 finding)。

## 新 findings

### R2-C1 (Critical) — D7「非自动触发」兜底桶对未建模但真自动的触发键 (pull_request_target 等) 方向不安全

D7「仅 workflow_dispatch / schedule **等**非自动触发」— `pull_request_target` (真自动、常见于 fork PR) 不在 D6 已建模集合, 落进「等」字兜底; 实现 A 按字面归零贡献 → 对只用 pull_request_target 的 workflow 产生**假 not_applicable**, 违反 D2 行为承诺。与 BA-1 同一「未建模输入 fail 方向」缺陷在 `on:` 触发键层复发; 本仓语料不含此键, SC-2/23 测不出。
**修法**: D7 改精确白名单「仅 workflow_dispatch / schedule 两键 → 零贡献; 其余未建模顶层触发键 (pull_request_target / repository_dispatch / workflow_call 等) 一律按未建模构造走 per-workflow covered」; 补 SC 用 pull_request_target 手造 fixture 钉方向。

### R2-M1 (Major) — 规则 5/7 两条主路径 reason 字面值未钉 + 规则 7/8 在 workflows_scanned=0 边界谓词重叠

规则 5 (最常见 covered) 与规则 7 (#122 本尊场景) 无 reason 字面值, SC-3/SC-2 不断言 reason → 合格实现分叉且套件测不出。规则 7 三个全称子条件在空集上 vacuous truth 与规则 8 同时成立 (与 tech-lead Major-1 同一发现)。
**修法**: 规则 5 补 reason (如 matched:<...>); 规则 7 补 reason=`no-triggering-paths` (与规则 8 `no-workflow-files` 区分「有 workflow 但都不命中」vs「压根没 workflow」); 规则 8 显式声明为循环前置短路; 补 SC 锁规则 5/7 reason。

### Minor 残留: BA-2 负向 SC (主仓 cwd 评估子模块内变更) 缺位; `git rev-parse --show-toplevel` 机制无 SC 锁定。

## 结论

R1 9 条中 8 条完整闭合 (全部实码核验), BA-2 残留 Minor。新缺口 R2-C1 (会真实产生假 not_applicable, 同 BA-1 价值判断故标 Critical) + R2-M1 (诊断字段欠定)。**REVISE** — 但预期 R3 只需三处补丁 (D7 白名单 / 规则 5/7 reason / BA-2 残留 SC), 无结构性重写。
