---
agent: backend-architect
round: R1
verdict: REVISE
scope_check: SCOPE_OK
critical_count: 2
major_count: 4
minor_count: 3
---

# post_spec 审计 R1 — backend-architect

## Critical

### BA-1 — glob matcher 对「未建模语法」的 fail 方向未落到 matcher 层, D2 骨架在最细粒度处出现缺口

proposal §1 把 fail-toward-covered 写在 workflow 文件级与触发块级, 但 `paths:` 列表内部单条 glob pattern 本身若含 matcher 未建模的语法 (forgejo/GHA 实际支持字符类 `[abc]`、否定前缀 `!` 等, proposal 只承诺 `**`/`*`/`?`), matcher 该怎么判未规定。两个合格实现会分叉: A 对未知语法片段按「命中」处理 (与 D2 一致); B 按「不匹配」处理 (常见 glob 库默认) — B 会让「变更命中一个用了字符类的 workflow」被错判 not_applicable, 产生真正的假绿, 且 SC-14 (只测三种已建模语法) 抓不到。
**修法**: §1 补显式规则「matcher 对任何未建模 glob 语法片段一律判定为匹配 → 该 workflow 落 covered」; SC-14 增补字符类/否定前缀用例钉方向。

### BA-2 — 仓边界/CWD 契约未声明, 本项目结构下会真的扫错 workflow 集合

主仓与 aria 子模块各有一棵 `.forgejo/workflows/` 树, 同名 `issue-triage-tests.yml` 的 paths 前缀不同 (`aria/skills/issue-triage/**` vs `skills/issue-triage/**`); `git diff --name-only` 输出天然相对当前仓根。若在主仓根评估落点在子模块内的变更, 会扫错 workflow 集合 — 判定「恰好也 not_applicable」是从错误仓边界看的巧合, 非设计意图。既有 pre_merge_gate.py 隐含「从目标仓根调用」契约但从未写明; path_coverage.py 是第一个同时触碰 git 历史 + 文件系统扫描的组件, 对仓边界敏感度远高于旧代码。
**修法**: 显式声明仓边界契约 (以 `git rev-parse --show-toplevel` 为仓根, 调用方负责在正确的仓内以正确 cwd 调用); SC 加「主仓 cwd 评估子模块内变更」负向用例。

## Major

### BA-3 — Why 表格 build-aria-runner.yaml 语料表述与真实文件矛盾

该文件同时有 `push` 自动触发 (branches: [feature/aria-2.0-m0-prerequisite] + paths: aria-orchestrator/docker/aria-runner/**), 不是 dispatch-only。仅 submodule-gate-tripwire.yml 是真 dispatch-only。若实现者依错表写死「build-aria-runner 恒零覆盖」测试, 对触碰该 paths 的变更产生假 not_applicable。
**修法**: 更正表格; D7 只引 tripwire; build-aria-runner 改作「push 有 paths 且 branches 在场 → branches 不建模、按 paths 交集判」的正例 fixture。

### BA-4 — covered 与 unknown 整体判定优先级在混合结果下未声明

「任一 workflow covered → 整体 covered」与「任一环节不确定 → unknown」在 {某 workflow covered ∧ 另一 workflow 文件级解析失败} 场景同时成立, 输出只能一个值 — 重叠格由实现顺序裁决 = 未定义。gate 层行为一致故不威胁合并安全, 但诊断字段值在合规实现间不唯一。
**修法**: 显式优先级 (建议 covered 优先于 unknown — 已证明真实覆盖是更强信号), 补 SC 覆盖重叠场景。

### BA-5 — unknown 态没有 D8 式可观测性义务, 长期无声退化风险

unknown 在 gate 层与 covered 不可区分且无 surface 义务 — parser 若因 workflow 写法演进长期识别不出, 机制永久失效而无信号。与本 spec 批评的「零信息量→被忽略」同病换位。
**修法**: unknown 时 raw_message/log 留痕 reason; SKILL.md 指令面加轻量要求 (连续 unknown 应上报)。

### BA-6 — path_coverage 字段在 gate_check 多个早退分支的出现范围未定义

_build_output 现为固定六键。评估点之后的 backend-query-failure 早退分支 (AetherQueryError → FAIL) 是否携带 path_coverage 键, 两个实现会分叉。SC-15 只断言老键保留, 不约束新键分支范围。Impact 表遗漏 _build_output 签名变更。
**修法**: 明确键出现范围 (建议仅 compute_verdict 产出的最终路径携带; 早退分支保持六键); Impact 表补 _build_output。

## Minor

### BA-7 — gate_check docstring「matches current Aether subprocess invocation count」在 not_applicable 分支上线后失真, 需纳入变更范围。

### BA-8 — compute_verdict 现有 fallthrough 恰好已产生期望行为; 要求写显式 `elif pr_ci_status == "not_applicable":` 分支而非依赖隐式兜底, 防未来改兜底逻辑时悄悄改变语义。

### BA-9 — SC-4/SC-5 未显式点名块映射三形态 (本仓 4 份真实 workflow 全部形态); `git diff 三点` 需声明非浅克隆前提 (本仓 CI workflow 用 fetch-depth:1, 但 gate 运行环境是本地 clone, 风险低; 写进 §1 前提)。

## 结论

核心骨架扎实, 衔接点选得对。但 BA-1/BA-2 两处若不显式约束会真的产生假 not_applicable (违反 D2 骨架本身); BA-3~BA-6 让 SC 套件在关键场景失去唯一答案或让机制重蹈静默失效。按 BA-1/BA-2 补硬约束文字, BA-3~BA-6 各补判定规则/SC 后再进 B.2。**REVISE**。
