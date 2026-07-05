---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-07-05T15:56:18.425Z
context: openspec/changes/runtime-probe-archive-gate-integration/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

> **ORCHESTRATOR 核实注记**: 本报告全部关键证据经独立抽查核实为真 (collectors/openspec.py:38 import 拓扑
> + :78 _FRONTMATTER_RE / spec_complete.py:1124-1133 dict 无条件预置 / 全归档 proposal 零 frontmatter /
> openspec-archive SKILL.md already_archived_precheck:102)。CRITICAL 成立。

## 审计结论

### [CRITICAL] frontmatter 持久化交付物无绑定 AC，且"复用同机制"的前提在本仓无任何真实执行证据

**category**: architecture | **scope**: proposal.md 第 3 部件第 3 bullet + tasks.md 2.3 + Success Criteria 章节

proposal.md 第 3 部件承诺"探针结果随 `unverified_claims` 同机制持久化到归档 proposal frontmatter (证据痕迹)" (proposal.md:58; tasks.md:17; DEC:89)。但 SC-1~SC-9 (proposal.md:80-88) **没有任何一条绑定"证据是否真的写入了归档 frontmatter"** — SC-2 只断言内存态字段, SC-7 只断言"探针折入可观测" (CLI 输出)。违反本 proposal 自立规矩 "每条绑可验 metric" (proposal.md:78)。

且该"复用"机制**在本仓迄今没有真实执行成功的痕迹**:
- 全部已归档 spec proposal.md 逐一扫描 (`head -1 | grep '^---$'`): **零命中** (0/118)。
- 全仓 `^archive_type:`/`^unverified_claims:` grep: **零命中**。
- 最有说服力反例 = #95 自身: 其归档 proposal.md:1 开头 `# Proposal:` (非 `---`), 但第 2 行自称 "Dogfood: verdict=warn" — 按设计 warn 应触发 Step2 warn_overlay 写 `unverified_claims` frontmatter (openspec-archive SKILL.md:176-189), 实际文件**无任何 frontmatter 痕迹**。
- 根因可解释: SKILL.md:100-105 `already_archived_precheck` "已存在归档条目 → 立即 abort" — Step 1-7 (含 Step2 写入) 只在 spec 第一次真实归档时触发; 事后对已归档目录跑 `--gate` (纯读) 结构上无法触发写入。#95 的"自身 dogfood"正是事后重跑, 从未真正验证写入路径。
- 本 spec 的 dogfood 计划 (tasks 4.2/4.3) 同样对**已归档** spec 手工加声明 + 跑 `--gate` — **结构上重复同一盲区**, 不会验证写入路径。

结论: "随 unverified_claims 同机制持久化"指向的机制从未真实跑通过一次; 本 spec 计划在无验证地基上叠一层, 且无 AC 兜底发现"写入没发生"。既是 AC 不可证伪, 也是与真实代码历史相矛盾的假设。

### [MAJOR] frontmatter 读取复用会触发 spec_complete.py ↔ collectors/openspec.py 循环 import

唯一现成"只读文件头 --- 块"实现 `_FRONTMATTER_RE`/`_frontmatter_block` 在 collectors/openspec.py:78,83-86; 该文件 :38 已 `from ..lib.spec_complete import is_spec_complete`。tasks 2.1 "复用 #95 TG-2 frontmatter 面"若字面理解为反向 import 即循环 import。项目有明确规避先例 (openspec.py:19-22 注释: carry_forward 下沉 lib/ 避免同型循环)。tasks 4 个 Phase 均无"抽正则到独立共享模块"任务。spec_complete.py 全文无 frontmatter 正则/函数 (grep verified)。

### [MAJOR] task 4.2 dogfood 落点当前零 frontmatter，"追加"措辞掩盖"新建区块"

`_FRONTMATTER_RE` `.match()` 锚定文件绝对起始。coordination 归档 proposal.md:1 首行为 `# Interactive Session Dedup...`, **无 frontmatter 区块**。"追加"易被读成"在已有结构里加字段", 实际需**在文件最前新插入整个 `---...---` 区块** (标题之前)。若按字面加在文末/中部, regex 永远匹配不到 → 探针折入路径认为"无声明"跳过 → SC-7 **静默退化成空跑**, 表面不报错, 易误判"dogfood 通过"。

### [MAJOR] SC-1 逐字节 diff=0 与 gate_result 现有 dict 初始化风格存在实现分叉风险

gate_result 入口一次性预置全部 8 键 (spec_complete.py:1124-1133, 无条件)。proposal 加粗"**新字段** runtime_probe" — 实现者按现有风格直觉把 `"runtime_probe": None` 加进初始化字面量, 与 SC-1 "无声明语料 diff=0" (proposal.md:80) 直接冲突: 每个未声明 spec 平白多出 `"runtime_probe": null` 键。tasks 2.1 "无键→零动作"已给正确答案但需与"新字段"措辞放一起读。建议显式加: "未声明时 runtime_probe key 必须整体不存在于返回 dict (非置 null)"。

### [MINOR] enabled_when dotted-path 对"中间段非 dict"缺显式规定 + 无 fixture

现 _gate_enabled try/except 只包文件读取+JSON 解析 (coordination_probe.py:48-51), 链式 .get 在 try 外 — state_scanner 键值非 dict 时抛 AttributeError。泛化成任意 dotted-path 后风险面扩大。task 2.4 兜底会接住但归"探针崩溃"而非"声明无效"清晰类。SC-2~6 + tasks 3.1/3.2 无此形态 fixture。建议 runtime_probe.py 每级 .get 防御 + 归"声明无效"分类 + 补 fixture。

### [MINOR] max_age_days 缺 range 校验，负数/零产生难归类退化行为

负数/0 是合法 int 能过类型校验, 但 cutoff 落在"现在/未来" → 所有真实记录判"陈旧" → 恒 warn。既非"声明无效"也非真死代码信号。建议校验"正整数 ≥1, 否则声明无效"。

### [MINOR] 大分区文件一次性整读而非流式

count_production_invocations 用 read_text 整读 (coordination_probe.py:86-90)。"沿用既有解析语义"意味泛化库保留此方式。当前规模无问题; 建议文档补一句"已知取舍: 整读非流式, 依赖分区体量保持较小"。

## Verdict

**verdict**: FAIL | **vote**: REVISE
理由: 1 CRITICAL — 持久化承诺无 SC 且复用机制 0/118 从未真实执行, 本 spec 的 dogfood 结构上无法验证写入路径。建议: (a) 补可证伪持久化 SC (非预归档测试 spec 走真实 Step1-7 或等价脚本化流程); (b) 抽 frontmatter 正则到独立共享模块任务; (c) 4.2 改"新建区块 (插入文件最前)" + SC-7 加"声明被解析器识别"中间断言; (d) 显式"未声明时 key 整体不存在"。

## 轮次记录

R1 — Read: proposal/tasks/DEC 全文; coordination_probe.py 全文; spec_complete.py (1-142 + 1112-1326 + def/class/import grep); phase1_gate.py (import 区 + telemetry 写入区); collectors/openspec.py (1-55 + 81-145); openspec-archive SKILL.md (80-320 Step1-7); .aria/state-checks.yaml; .aria/config.json; coordination + #95 归档 proposal 头部。辅助: 全归档 proposal 首行扫描 (零 frontmatter) + archive_type/unverified_claims 全仓 grep (零命中)。
