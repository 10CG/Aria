# Tasks: runtime-probe-archive-gate-integration (#95 follow-up A)

> **Spec Level**: 3 | **决策 SOT**: DEC-20260705-001 + owner 决策 2026-07-05 (dogfood 不回改归档) + R2 裁决 (仅 warn 落盘, probe-warn 并入 unverified_claims) + R3 裁决 (键写入取决于探针自身 outcome, 非门级 verdict 来源) | **关联**: aria-plugin #95 (closed) follow-up A
> 双层架构: 本 tasks.md = 粗粒度功能层; 细粒度 (agent/时间/文件/verification↔AC 映射) 由 A.2/A.3 `detailed-tasks.yaml` 承载。
> Success Criteria 见 `proposal.md` (模板惯例)。编号不可变 (创建后不改; R1/R2-fix 为 approve 前修订, 新任务只追加编号)。

## Phase 1 — 通用探针库 (泛化, 零消费方破坏)

- [ ] 1.1 新增 `lib/runtime_probe.py` descriptor 解析 + 校验: 4 字段 schema (partition/symbol 必填, max_age_days 默认 14, enabled_when 可选 dotted-path); 无效形态 → 明确「声明无效」结果, 不猜不硬崩。无效判定含: 缺必填 / 类型错 / **max_age_days 非正整数 (≥1)** / **partition 绝对路径或 resolve 后逃逸 repo (`is_relative_to` 校验, 防 pathlib 拼接静默丢前缀)** / **enabled_when dotted-path 中间段类型不对 (每级 `.get` 防御)**
- [ ] 1.2 `probe(descriptor, repo, now)` 三态判定 (pass/warn/skipped + count/reason/symbol): 沿用 coordination_probe 既有解析语义 (JSONL 坏行跳过 / source==production 过滤 / 新鲜度 cutoff / 注入 now); **warn 四形态** = 分区缺失 / **存在但不可读 (IO error, 修正既有 -1 假绿边缘)** / 全陈旧 / 仅非生产记录; enabled_when 开关关或 config 文件缺失 → skipped (缺失附低调 note)
- [ ] 1.3 `coordination_probe.py` 改薄壳: 委托通用库 + 硬编码 coordination descriptor; **三态→二元 exit 映射 (pass/skipped→0, warn→1) + coordination 专用消息模板重格式化 (不透传通用 reason)** — **四种既有可达状态 (disabled / 缺失 / 正常 / 陈旧)** CLI 输出逐字节保持 → `.aria/state-checks.yaml` 零改动; **唯一有意行为变化 = read-failure 假绿修复 (unreadable → STALE 类消息 + exit 1)**
- [ ] 1.4 frontmatter 块提取 helper **物理 move** 到 `scripts/lib/` 叶子模块 + `collectors/openspec.py` 反向 re-import (行为不变; 复用 #134 `_FRONTMATTER_RE` 解析语义, `carry_forward.py` 同型先例, **单一 SOT 不复制不双写**; **禁止 spec_complete.py import collectors.openspec** — 循环 import) + 块内 `runtime_probe` 受限 YAML 子集手写解析 (顶层键 + 4 scalar 子键, 2-space 缩进; **行尾注释剥离** — 值中首个 ` #` 起丢弃; 超形态 [更深嵌套/flow-style/锚点/多行值] → 声明无效; **stdlib-only, 不引 PyYAML**; §What 1 官方示例原样可解析)

## Phase 2 — 归档门折入 (gate_result 扩展, fail-toward-warn)

- [ ] 2.1 `gate_result` 读 proposal frontmatter `runtime_probe` 键 (经 1.4 lib helper, 只读文件头 `---` 块, 正文代码块不误读): 无键 → 零动作, 静态路径逐字节不变 — **`runtime_probe` 键整体不存在于返回 dict (禁 null 占位; 不得加入 `spec_complete.py:1124-1133` 入口预置字面量; CLI 两处 fallback JSON [usage/crash 错误路径] 同样不含)**; **proposal.md 缺失/读失败 → 等同无声明零动作 + soft_errors 记录 (对齐 tasks.md 读失败 fail-soft 先例); 两个既有早退路径 (tasks.md 缺失/不可读) 不评估探针 (designed, 等同零动作)**
- [ ] 2.2 折入裁决: pass → verdict 不变 + note; warn → verdict 抬至 ≥warn **绝不 block** (已 block 保持 block); skipped → verdict 不变 + 低调 note; 声明无效 → warn「无法核验」
- [ ] 2.3 warn routing (R2 裁决): probe-warn (含声明无效) 条目除 warnings[] 外, 以 `{claim: "runtime_probe:<symbol>", reason, symbols: [<symbol>]}` 形态**并入 `unverified_claims[]`** → 自然复用 #95 双下游 (warn_overlay 持久化 + d_payload/Step 7 D auto-issue 兜底), 零机制签名改动; 探针结果作为**条件性新字段** `gate_result.runtime_probe` 返回 (仅声明存在时; gate 纯函数只产 JSON **不写文件**)
- [ ] 2.4 全异常兜底: 探针任何未预期异常 → gate catch → 降级 warn + 照常产出完整裁决 (杜绝新 block 源 / silent failure; #95 pre-merge Critical 教训)
- [ ] 2.5 `openspec-archive/SKILL.md` 写入契约扩展 + schema 补注: **Step 2 warn_overlay 触发条件对齐宿主原语义 (`verdict=="warn"`) 不扩展** — warn 时 `runtime_probe` 结构化结果 (outcome/count/ts/symbol) 作为额外键与 `unverified_claims` (含 probe-warn 条目, list-of-object 契约格式) **同批写入**; **内容归属 (R3): `runtime_probe` 键仅当探针自身 outcome ∈ {warn, 声明无效} 才写 (与门级 verdict 来源无关 — 他因 warn 时 pass 探针键不写)**; **pass/skipped 不落盘** (干净归档零噪音); **无既有 frontmatter 块时 (118/118 现状) → 在文件绝对起始插入新 `---...---` 块, 原内容整体下移; 已有块则追加键**; **dry_run 回显契约同步扩展 (`:188`): 回显将写入的 unverified_claims 列表 + (若将写入) runtime_probe 结构化结果 (归档前所见即所得)**; **Step 1 `--gate` stdout JSON 读取 schema (`:115-116`) 补注条件字段 runtime_probe**; **`claim` 字段注释 (`:180`) 泛化为「tasks.md 声称原文行, 或 runtime_probe:<symbol> 合成标签」**; `unverified_claims_written` 邻域 flag 语义 additive 扩展 (写入路径由 3.6 E2E 行使)

## Phase 3 — 测试 (合成 fixture 钉契约)

- [ ] 3.1 单元测试 (runtime_probe 库 + 1.4 解析器): 三态 × descriptor 值层五形态 (缺必填/类型错/max_age_days≤0/路径逃逸/dotted-path 中间段非 dict) × **文本层形态 (更深嵌套/flow-style/锚点/多行值 → 声明无效; 行尾注释剥离正确; §What 1 官方示例原样解析成功)** × 注入 now 确定性 × 坏 JSON 行/坏 ts × 自定义 max_age_days (SC-2/SC-5)
- [ ] 3.2 集成测试 (gate 折入): 无声明逐字节回归 + pass (SC-2, 含不落盘断言) / warn 四形态 (SC-3, 含 unverified_claims routing + d_payload 断言) / skipped (SC-4) / 声明无效 (SC-5) 各折入路径 + **IO 边界 (SC-5): proposal.md 缺失 / OSError → 无声明零动作 + soft_errors 断言** + block+warn 组合不降不升 + fault-injection (SC-6)
- [ ] 3.3 SC-1 零回归 re-sweep: 全归档 + 活跃 changes 语料, **同一 worktree 同一树内容** v1.53.0 代码 vs 新代码双跑 `--gate` 输出 diff=0 (排除 grep 语料漂移噪音; 脚本化可复现)
- [ ] 3.4 可证伪 harness: 注入「探针恒 pass」变体 → 测试套至少 1 例 FAIL (anti-false-green) (SC-8)
- [ ] 3.5 CLI 向后兼容回归: coordination_probe.py 薄壳化前后, **四种既有可达状态 (disabled/缺失/正常/陈旧)** 输出 + exit code 逐字节一致; **read-failure 假绿修复新行为独立回归锁定** (SC-9)
- [ ] 3.6 持久化 E2E (SC-10, warn-outcome + 对称负控): 扩展 `test_archive_gate_integration.sh` — **正控**: 含活跃期声明 + warn 形态分区的合成 spec fixture 走 openspec-archive Step 1-2 脚本化流程 → 断言 `runtime_probe` 键真落盘 (**无既有块时验证块插入文件绝对起始**) + probe-warn 条目在 `unverified_claims` 同批 (**list-of-object 契约格式, 顺带修正既有 §3 precedent 的 `unverified_claims: %d` 计数偏差**) + `d_payload` 含该条目 + **断言经 `_frontmatter_block()`/`_read_archive_type()` 真实解析路径** (非裸 grep) + `_staleness_days` 无扰; **对称负控 (R3)**: (a) pass-outcome fixture 同流程 → 断言归档 frontmatter **无** runtime_probe 键; (b) 混合场景 fixture (probe=pass ∧ 无关声称致 verdict=warn) → 断言 unverified_claims 写入但 runtime_probe 键缺席

## Phase 4 — dogfood (不回改归档) + 文档 + 版本

- [ ] 4.1 Phase B-entry 真调 `phase1_gate` CLI (advisory claim, Layer L 编排契约; collision=self_multi_container + enabled=true 场景合法) → 产 production telemetry 记录 (顺带转绿 coordination-gate-invocation check); **失败 fallback**: 重试一次, 仍失败 → 记 known-limitation, 不阻塞其余 Phase 4 (SC-7 fallback)
- [ ] 4.2 lib 层真分区 dogfood: 以代码内构造的 coordination descriptor 对真实 `.aria/coordination-telemetry.jsonl` 直跑 `runtime_probe`, 记录 outcome+ts 于 closure 报告/handoff (一次性 ship-time 观测, **不固化为永久 pytest 断言**) (SC-7)
- [ ] 4.3 零回归真语料确认: coordination 归档 spec **保持无声明** (不回改归档, owner 决策), 作为 3.3 re-sweep 语料一部分核验零动作路径
- [ ] 4.4 文档同步 (Rule #3): state-scanner references 声明 schema 文档 (含活跃期自写声明惯例 + stdlib-only 受限子集 + 注释剥离规则 + known-tradeoff 整读非流式) + phase-d-closer SKILL.md additive 提及 + standards `openspec/project.md` 归档惯例一行 **+ 同步新增该文件自身 Version History 行 (#95 编辑同文件留有 2.2.1 行先例)** (openspec-archive SKILL.md 写入契约扩展由 2.5 承载, 非本条)
- [ ] 4.5 版本发布全 surface: aria 侧 5 文件 (plugin.json + marketplace.json + VERSION + CHANGELOG + README) + 主仓 3 surface (**/VERSION 插件版本行** + README badge + Project Status 段) + **子模块指针 bump: aria (必) + standards (project.md 变更故亦须)** — 逐面核对 CLAUDE.md 版本发布检查清单
