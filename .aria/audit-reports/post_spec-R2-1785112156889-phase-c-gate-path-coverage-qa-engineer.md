---
agent: qa-engineer
round: R2
verdict: REVISE
scope_check: SCOPE_OK
critical_count: 0
major_count: 2
minor_count: 3
---

# QA 审计 R2 (闭合核验)

方法: R1 逐条复核 + 实读 test_pre_merge_gate.py / pre_merge_gate.py / 4 份真实 workflow; 沙箱实测 --no-renames 与 gitlink-only diff。

## R1 闭合核验

QA-1~QA-8 **全部一次性 CLOSED** (规则 1+D10+SC-16 / SC-9/10 assert_not_called / §4 mock 入口+SC-22 / OR 语义+SC-17 / SC-23 联合语料 (触发形态与原文比对准确) / --no-renames+SC-18 (沙箱复测: 确实吐新旧两路径; 不加 flag 默认只吐新路径) / matched_workflows 类型钉死 / SC-14 大小写)。

## 新 Findings

### QA-9 (Major)｜reason 在最常见两条路径 (规则 5 covered / 规则 7 not_applicable) 未定义字面值 — 未构成可断言封闭集
SC-2/3/4/5/20/23/24 均不断言 reason (spec 没给可断言的值)。返回契约隐含 reason 恒有意义填充; 实现者会各自发明措辞, 下游依赖 reason 精确匹配会漂移。
**修法**: 规则 5/7 补 reason 字面值 (如 workflow-trigger-matched / no-trigger-matches-change), 对应 SC 补 reason 断言, 8 规则 × reason 构成封闭集。

### QA-10 (Major)｜SC-19 期望是非承诺式散文, 不构成可编译断言
「按其余规则判」未钉终态 decision/reason; 恰落在 QA-9 未定义的规则 7 分支, 双重欠费。手工推演终态应为 not_applicable, 但 spec 没替测试作者钉下来。
**沙箱可行性结论**: gitlink 语料构造完全可行 (真实 submodule add + bump commit → diff 精确吐单 token `aria`); 更轻量做法是直接给分类纯函数喂 changed_files=["aria"]。问题在断言值未定, 非语料不可建。
**修法**: SC-19 改具体断言行 (decision=not_applicable + reason 字面值); 可选: 另建 paths 含 `aria/**` 的合成 workflow 正面验证 gitlink 不展开政策 (正证优于反证)。

### QA-11 (Minor)｜规则 1/2/3 枚举顺序与数据依赖顺序不一致
规则 1 依赖 diff 已成功; 实际执行必然 diff 先行。规则 1/3 互斥不能同时发生 (已论证)。「实现按此序求值」字面会误导。
**修法**: 改写为「判定优先级/输出裁决顺序, 非执行时序」或按数据依赖重排。

### QA-12 (Minor)｜集成入口符号名未点名
SC-9/10/21/22 依赖可 mock 符号; 既有先例 mock.patch.object(gate, "resolve_ci_backend")。建议显式点名 (如 evaluate_path_coverage) 消除命名随意性。

### QA-13 (Minor)｜test_path_coverage.py 临时仓 fixture 隔离提醒缺位
memory `feedback_test_worktree_fixture_isolated_tmpdir` 已录坑 (须独立 tempdir 非 repo.parent); 新增测试大量 IO fixture, 正文应留指针。

## 结论

R1 全部结构性收敛, 骨架站得住 (两处沙箱实测吻合)。新 2 Major 均文字补完级 (reason 封闭集 + SC-19 具体化), 不涉架构重开。**REVISE**: 进 Phase B 前补 QA-9/QA-10, Minor 随手带上。
