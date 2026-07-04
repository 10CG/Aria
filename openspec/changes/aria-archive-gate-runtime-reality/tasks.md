# Tasks: archive-gate-runtime-reality (#95)

> **Spec Level**: 3 | **决策 SOT**: DEC-20260704-003 (含 Amendment 1: B 化入 C) | **关联**: aria-plugin #95
> 双层架构: 本 tasks.md = 粗粒度功能层; 细粒度 (agent/时间/文件/verification↔AC 映射) 由 A.2/A.3 `detailed-tasks.yaml` 承载。
> Success Criteria 见 `proposal.md`(模板惯例: 验收标准在 proposal 非 tasks)。编号不可变 (创建后不改)。

## Phase 1 — lib 基础 + tri-state 契约 (共享判定 SOT)

- [ ] 1.1 在 `lib/spec_complete.py` 扩展纯函数, 复用 #134 既有归一化与 carry-forward 提取, 不重复实现
- [ ] 1.2 符号提取纯函数: 提取源 = 集成声称映射的 **deliverables** (detailed-tasks.yaml `deliverables` + proposal Key Deliverables + tasks.md 行内代码路径/backtick identifier), **非**仅 prose 声称行 (Layer L 反例符号只在 deliverables 具名); 无法提取 → 明确返回"不可核验"而非猜
- [ ] 1.3 生产语义引用核验纯函数 (**语义级, 非朴素 grep**): 核验符号有无"生产语义引用" —— 算引用 = 代码引用(import/调用/属性/装饰器/别名)+ dynamic-dispatch(getattr/importlib/globals)+ aria-plugin 集成面(SKILL.md Bash / hooks.json·config)+ **通用调用面**(shell/cron/Makefile/CI 按字面路径调用); **不算** = 注释/docstring/散文字符串(任何文件含 *.md/CHANGELOG/audit-reports)+ 测试文件 + dogfood·ops 核验脚本目录 + 符号自身定义文件。实现须剥注释/docstring 后匹配 + 单独扫集成/调用面
- [ ] 1.3b **非穷尽 → fail-toward-warn 默认**: 落两清单之外的生产出现形态 → 降 block 为 warn (非 hard-block); hard-BLOCK 只在"全属不算引用类 或 零出现" (误分类恒偏向不误 block)
- [ ] 1.4 产物抽验纯函数: 给定声称类型 (ab-results/遥测/部署), 核验可链接产物存在
- [ ] 1.5 tri-state 输出契约: CLI 沿用 #134 exit code (0/1) + stdout JSON `gate_result:{verdict:pass|warn|block, blocking_reasons, warnings}`; 两 Bash 消费方读同一 verdict 字段
- [ ] 1.6 全部新增判定 fail-soft (stdlib-only + grep shell-out; 解析/grep 失败 → 放行 + soft_error, 不硬崩归档)

## Phase 2 — C-block: 高置信死代码闸 (block)

- [ ] 2.1 识别 tasks.md `[x]` 行的代码集成类声称 (关键词: 集成/接线/wire/integration/调用/registered/hook)
- [ ] 2.2 对提取到具体符号且**零生产语义引用** (1.3 + 1.3b fallback 定义) 的声称 → 判 block (dead-code-on-arrival)
- [ ] 2.3 误报防护: dynamic-dispatch / 集成面 (SKILL.md·hooks.json) / 通用路径调用 (shell·cron·Makefile·CI) / 注释-docstring-剥离 / 未分类形态 fail-toward-warn —— 均使合法接线不误 block
- [ ] 2.4 openspec-archive Step1 + phase-d-closer D.2 集成: verdict=block → BLOCK 归档; 复用 #134 `--archive-design-only`+reason 逃生舱显式豁免

## Phase 3 — C-warn: 模糊声称持久标记 + ack (warn)

- [ ] 3.1 无可链接产物的 dogfood/benchmark/deploy 声称, 或未点名符号无法静态核验 → 判 warn
- [ ] 3.2 warn 写 proposal frontmatter `unverified_claims:[...]` **持久标记** (对比 #134 `--archive-design-only`, 非临时)
- [ ] 3.3 交互模式归档者可 `--ack-unverified <reason>` 记录人工确认; **但 D 兜底不依赖 ack** (见 4.1)
- [ ] 3.4 C-warn 恒不 block (启发式误报风险); 持久标记 + D 兜底 (无论是否 ack) 使残留可追踪 (非静默绕过)

## Phase 4 — D: 归档不吞未完成 → open issue (auto-issue)

- [ ] 4.1 归档时检出 deferred/未勾实施项 **或任何** C-warn `unverified_claims` (无论是否 ack) → 触发 auto-issue; **headless 默认自动创建** (无人 ack 时不 stall 不静默, 防 fleet 重现 gap D)
- [ ] 4.2 单一 owner: openspec-archive Step2 为唯一 issue 创建点; phase-d-closer D.2 委托不各自建 (防双入口重复)
- [ ] 4.3 issue-tracker backend 抽象: Forgejo 默认; 非-Forgejo 降级为输出草稿 + 提示手动创建
- [ ] 4.4 API 失败路径不静默: 建 issue 失败 → 打印 issue 草稿 + WARN (归档不 abort 但残留可见)
- [ ] 4.5 幂等: issue body 埋 `<!-- archive-tracker:{spec_id} -->` marker; 建前搜同 spec 既有 open issue, 存在不重复开
- [ ] 4.6 body 含 spec_id + 未完成项/unverified 清单 + 归档 SHA 回链

## Phase 5 — 文档 + schema + 自身 dogfood

- [ ] 5.1 openspec-archive SKILL.md 增 C-gate (Step1) + D-auto-issue (Step2) 描述
- [ ] 5.2 phase-d-closer SKILL.md + references 同步 D.2 gate 扩展 (委托 Step2 语义)
- [ ] 5.3 若新增 snapshot 字段则 additive 更新 `state-snapshot-schema.md` (不 bump `snapshot_schema_version`)
- [ ] 5.4 standards 归档惯例补"完成=可核实完成 (有 call-site/产物支撑)"
- [ ] 5.5 dogfood 本 gate: 确认本 change proposal 已含 `## Success Criteria` 段 (符合模板惯例)

## Phase 6 — 测试 (Rule #6)

- [ ] 6.1 C-block structural fixture + unit: golden 负例 (phase1_gate 剥注释/docstring 后零生产语义引用应 block, 尽管有 3 生产 collector 注释/108 单测/docs 提及); 4 类正控 (真实代码引用 / SKILL.md·hooks.json 集成面 / dynamic-dispatch / shell·cron 通用路径调用) 均不误 block; 未分类形态 fail-toward-warn
- [ ] 6.2 C 误报有界 + 判别力测试: 语料库 N≥8 已归档正常 spec (覆盖 4 类正控各 ≥1, 防 vacuous-pass), 全 N C-block 触发 0 例 (逐 spec 列 verdict)
- [ ] 6.3 C-warn + 标记测试: 无产物声称 → warn + 写 unverified_claims + 无论是否 ack 都传递 D
- [ ] 6.4 C fail-soft 降级路径 unit (R1 F6): 符号提取失败/生产引用核验 grep 失败/**产物抽验失败**/解析异常 → 放行 + soft_error
- [ ] 6.5 D 测试: 单一 owner 不重复建 / backend 降级 / API 失败草稿可见 / 幂等去重 / fail-soft
- [ ] 6.6 tri-state 契约测试: 两消费方读同一 gate_result.verdict 判定一致
- [ ] 6.7 真树 dogfood: 对既有归档 spec 跑 gate, 确认既有正常归档不被误 block
