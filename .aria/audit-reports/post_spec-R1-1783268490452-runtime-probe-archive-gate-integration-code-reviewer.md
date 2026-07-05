---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-05T16:11:20.093Z
context: openspec/changes/runtime-probe-archive-gate-integration/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

> **ORCHESTRATOR 核实注记**: agent 原报告 verdict 标 FAIL 但自报 "0 Critical / 4 Major / 3 Minor" —
> 按 verdict 公式 (FAIL=≥1 Critical) 纠正为 PASS_WITH_WARNINGS (vote=REVISE 不变)。F3 的 -1 假绿边缘
> 经 orchestrator 对照源码独立确认 (coordination_probe.py:86-89 → main :117/:123/:130 路径), 属实。

## 审计结论

共 7 findings: 0 Critical / 4 Major / 3 Minor。无"照写即 ship 错误契约"级矛盾, 但 4 Major 中 3 个会直接导致实现漂移或声称落空。

**F1 [major, architecture, proposal §What 3 / tasks 2.1]** — "复用 #95 TG-2 frontmatter 写入面"措辞与代码现实错位: 写入面存在但是 SKILL.md AI/Bash 指令面 (openspec-archive SKILL.md:177-188 Step 2 warn_overlay), **无 Python 解析代码可复用**; 全库唯一 Python frontmatter 解析器 `_FRONTMATTER_RE`/`_frontmatter_block` 在 collectors/openspec.py:78-86, 且属 **#134** (v1.42.0 `_read_archive_type`) 非 #95 TG-2。collectors/openspec.py:38,50 已 import lib/spec_complete — 反向复用即循环 import; 项目有规避先例 (openspec.py:20-22 注释: carry_forward 下沉 lib/)。修法: 写明"复用 #134 `_FRONTMATTER_RE` 的**解析语义**, regex 下沉 lib/ 叶子模块或复制, 不得 import collectors.openspec"。

**F2 [major, documentation, proposal §What 4 / tasks 4.2]** — 先例声称 "#95 归档时写 frontmatter unverified_claims" 与归档现实不符: #95 归档 proposal 首字节 `# Proposal` (od 确认无 --- 块), unverified_claims 仅在其正文 prose (:42,49,66,84); 全库归档 proposal **零 frontmatter 实例** (#95 自身归档 verdict=warn 7 条, 按 SKILL.md 机制本应写却没写 — 机制 shipped 后从未真实执行, 讽刺地正是本 spec 要治的"机制挂着没转"形态)。ERRATA.md 先例真实 ✓。影响: dogfood "追加声明"实为**新建全库首个** proposal 头部 --- 块, 应如实陈述 + 把"新建块对既有消费者 (_read_archive_type/_staleness_days) 无扰"列为验证点; _FRONTMATTER_RE 迄今对真实归档语料恒 None 从未被行使 (feedback_validate_convention_assumption_before_gate 同型风险, SC-7 恰可覆盖, 应显式挂钩)。

**F3 [major, implementation, proposal §What 2 / tasks 1.2-1.3 / SC-9]** — "分区缺失 sentinel"单一表述漏掉 **-1 双触发 + 假绿边缘**: coordination_probe.py:79-80 (不存在→-1) 与 :86-89 (存在但 read_text 失败→**同样 -1**); main() 只用 prod.exists() 分流 (:117), read-failure 时 n=-1≠0 落到 :130 输出 `"OK (-1 recent production run_gate invocation(s) recorded)"` **exit 0 假绿**。spec 的 warn 形态清单缺"分区存在但不可读"; SC-9 "逐字节一致"与"三态归 warn 合理实现"在此边缘互相矛盾 (bug-for-bug vs 顺手修复), 两个合理实现产生不同 CLI 行为。spec 须显式裁决该边缘。

**F4 [major, implementation, proposal §What 3 / tasks 2.3+4.4 / SC 全集]** — runtime_probe frontmatter 持久化**无实施落点也无验收**: "同机制" = openspec-archive SKILL.md Step 2 warn_overlay 在归档时刻由 Bash/AI 侧真写入 (SKILL.md:177-188; :309 unverified_claims_written flag) — Python gate_result 只能返回字段写不了归档 frontmatter。但 tasks 2.3 归 Phase 2 (spec_complete.py 侧), tasks 4.4 对 openspec-archive 只承诺 "additive **提及**" (≠ Step 2 写入逻辑扩展); SC-2 只验内存字段, SC-7 只验 dogfood outcome — **持久化零 SC 覆盖**。照 tasks 字面做完, "证据痕迹"声称可落空且无人发现 — 恰是 #95 病根形态自身。修法: tasks 增 openspec-archive Step 2 写入扩展显式任务 + 补持久化 SC。

**F5 [minor, testing, SC-1 / tasks 3.3]** — SC-1 未钉死控制变量: gate_result 输出自身无 volatile 字段 (spec_complete.py:1124-1132 无 timestamp/随机) ✓, 但 classify_symbol_liveness grep 面向全 repo (:759 git grep --recurse-submodules), 本 change 新增文件/文档可改变 ambiguous 符号的 unclassified_files 列表 (warnings 文本嵌入, :1210-1214) → 跨时点比对引入非探针 diff 噪音。建议 SC-1 写明"同一 worktree 上 v1.53.0 代码 vs 新代码双跑对比"。

**F6 [minor, documentation, proposal §Impact]** — "E-sweep 100 spec 零误 block"数字混称: E-sweep = pre-#134 孤儿审计 100 归档 (零死代码孤儿, §Why 用法正确); "零误 block"性质出自 #95 的 **116 归档 re-sweep** (CLAUDE.md)。Impact 把两个 sweep 拼成一个短语, 建议厘清。

**F7 [minor, implementation, proposal §What 3]** — "静态路径逐字节不变"蕴含: 无声明时 runtime_probe 字段须**整体缺席** (不能 null 占位), 且 CLI 两处硬编码 fallback JSON (spec_complete.py:1273-1288, 1294-1309) 不加该字段。spec 未显式写出条件性存在契约; openspec-archive SKILL.md:116 返回 schema 文档同步须注明。

### 核对通过的声称 (简列)

- coordination_probe 硬编码面 4 常量属实 (:41-42,45-53; run_gate 仅在消息文本 :119,125,130) — "symbol 当标签"一致 ✓
- CLI 契约对象真实 (:107-109 可选位置参数 / :113,121,129,131 exit 0·1 / 4 种消息) ✓ (F3 边缘除外)
- 解析语义四项逐行对应 (:94-97 坏行跳过 / :98-99 production 过滤 / :84,100-102 cutoff / :69-71,81-83 注入 now+tz 归一) ✓
- state-checks 消费 (.aria/state-checks.yaml:204-224) "不改一行"可行 ✓; "本仓当前红着" ✓
- gate_result 现有 8 字段 (:1124-1132); --gate exit 0=pass|warn / 1=block (:1311), 探针 warn 折入不改 exit 映射 ✓
- fail-toward-warn 先例真实 (I1/I2 兜底 :1268-1309 + C1 silent-failure fix :954-962) ✓
- ERRATA.md 存在 ✓; Layer L 编排契约 (SKILL.md:128-161 + lib/collision.py:14,52 self_multi_container 合法) ✓
- phase1_gate 生产写入面 (:927-937,962-963 ts 格式与 _parse_ts 兼容; :1090-1093,1191-1200 CLI 唯一 production call site) — "真调 CLI → 产记录 + 转绿 check"可行 ✓
- 版本/目录锚 ✓; "frontmatter 只读文件头 --- 块"与 _FRONTMATTER_RE.match 语义一致 (正文 yaml 示例不会误读) ✓

## Verdict

**verdict: PASS_WITH_WARNINGS** (orchestrator 按公式纠正; agent 原标 FAIL) | **vote: REVISE**

理由: 零 Critical — spec 对核心现状描述准确, out_of_scope 边界干净。但 F1 (解析复用无现成对象 + 循环 import 陷阱)、F3 (-1 假绿边缘使 SC-9 契约内含矛盾)、F4 (持久化无实施落点无验收) 属必须修的实现漂移源; F2 先例失实需如实改写。均为局部修订不动方案 A 骨架, 预期 R2 可收敛。

## 轮次记录

R1 — Read: proposal + tasks + DEC 全文 / coordination_probe.py 全文 / spec_complete.py 全文 (两段) / collectors/openspec.py (L15-140 + grep) / .aria/state-checks.yaml 全文 / phase1_gate.py (定向 grep) / openspec-archive SKILL.md (定向 grep) / state-scanner SKILL.md (Layer L 段) + lib/collision.py (grep)。归档语料: 全归档 proposal frontmatter 扫描 (零实例) + #95/coordination 头部字节级检查 + ERRATA.md + e-sweep 报告存在性 + 活跃 changes 6 proposal 头部 (全无 frontmatter)。
