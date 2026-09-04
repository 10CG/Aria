Level 判定: **Level 2 (Minimal)** —— 关键词「加一个可选参数」属功能增强 (add / 扩展), 影响范围限于 state-scanner 单个 Skill 的 Open Issues 区块, 无架构变更 / 无跨模块 / 无 breaking change, 故只产出 `proposal.md`, 不生成 `tasks.md`。
头部 `Linked Issue` 字段: 本需求经核实无关联 issue, 按「无关联 (已核实)」写法逐字填哨兵 `none` —— 不留空、不删行、不用 `N/A` / `TBD` / `-`。

以下为 proposal.md 全文:

---

# state-scanner Open Issues 区块 label 过滤参数

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-04
> **Linked Issue**: `none`

## Why

`/state-scanner` 的 🎫 Open Issues 区块目前一次性列出仓库全部 open issue。随着 issue 数量增长, 该区块在扫描输出里占比越来越大, 而使用者在具体场景下通常只关心其中一类:

- 走 triage 时只想看 `bug`
- 判断能不能开工时只想看 `blocker` / `P0`
- 做周期收尾时只想看 `deferred` / 某 milestone 相关标签

现在只能靠人眼在完整清单里筛, 既拉长了扫描输出 (占 context), 又容易漏看真正阻塞的那几条。给该区块加一个**可选**的 label 过滤参数, 可以在不改变默认行为的前提下把这段输出收敛到当下真正相关的子集。

## What

为 state-scanner 增加一个可选输入参数 `issue_label`, 只作用于 🎫 Open Issues 区块的 issue 收集与渲染:

- **不传时行为与现状逐字一致** (向后兼容, 这是本变更的硬约束)。
- 传入时, issue 查询在数据源侧 (Forgejo API `labels=` 查询参数) 就完成过滤, 而非拉全量后本地筛 —— 避免大仓下的无谓分页开销。
- 区块标题回显当前过滤器, 例如 `🎫 Open Issues (label: bug)`, 让读者一眼看出这是**过滤后的子集**, 不会误把它当全量。
- 过滤后为空时输出明确的「该 label 下 0 条 open issue」文案, 而不是隐藏区块或静默回退到全量 —— 静默回退会让「筛出来是空」与「参数没生效」不可分辨。
- 多 label 语义在本次一并钉死 (见 Success Criteria), 不留给实现者裁量。

**非目标 (本 Spec 不做)**:

- 不改 state-scanner 其它区块 (分支 / Spec / handoff / 版本面) 的任何输出。
- 不加 label 之外的过滤维度 (assignee / milestone / state), 需要时另开 Spec。
- 不引入配置文件持久化的默认 label —— 参数只在单次调用生效。

### Key Deliverables

- `aria/skills/state-scanner/SKILL.md` —— 输入参数表新增 `issue_label` 行 + 过滤态输出示例 + 空结果文案说明
- state-scanner 的 issue 收集实现 (Forgejo issue 查询处) —— 透传 `labels=` 查询参数, 并做取值规范化
- state-scanner 的 🎫 区块渲染实现 —— 标题回显过滤器 + 空结果分支
- 回归证据: 不传参场景的输出与基线逐字比对结果

> 具体脚本文件名 / 函数落点在 A.2 任务规划时按 state-scanner 实际目录结构确认, 本 Spec 只钉行为契约。

## Impact

| Type | Description |
|------|-------------|
| **Positive** | triage / 开工前判断 / 收尾三类高频场景下, 🎫 区块从全量清单收敛到相关子集, 减少扫描输出体积与漏看风险 |
| **Risk** | 过滤后的输出可能被误读成全量 (「我看到 open issue 只有 2 条」) → 由标题强制回显 label 缓解 |
| **Risk** | 数据源侧过滤依赖 Forgejo API `labels=` 的实际语义 (多值是 AND 还是 OR), 若假设错会静默给出错误子集 → 须在实现前对真实仓库实证, 不得凭文档推定 |
| **Compatibility** | 参数可选, 缺省路径不变 ⇒ 对现有调用方 (含十步循环 A.0 与 Layer 2 自主运行时) 无破坏性变更; 版本按 MINOR |
| **Process** | 变更触及 state-scanner 的 `SKILL.md` 指令面 (新增参数 + 行为描述) ⇒ 属处方性 · 运行时指令面, 按 Rule #6 **须跑 AB benchmark**, 不申请豁免 |

## Constraints

| 类型 | 约束 | 来源 |
|------|------|------|
| technical | 过滤在 API 侧完成, 不做拉全量后本地筛 | 大仓分页开销 |
| technical | 缺省路径 (不传参) 的输出必须与改动前逐字一致 | 向后兼容 |
| process | Skill 指令面变更, 发版前过 Rule #6 benchmark | CLAUDE.md 不可协商规则 #6 |
| process | 无 framework 项目语境, A.1.1 的 Framework Constraints 段跳过 | Aria #95 |

## Tasks

- [ ] 定义 `issue_label` 参数契约 (名称 / 取值形态 / 多 label 分隔符 / 大小写与空白处理 / 未知 label 行为)
- [ ] 对真实仓库实证 Forgejo issue API 的 `labels=` 多值语义 (AND vs OR), 结果写回 SKILL.md
- [ ] 收集层: issue 查询透传 label 过滤, 覆盖分页路径
- [ ] 渲染层: 区块标题回显过滤器 + 空结果文案分支
- [ ] 回归: 不传参输出与基线逐字比对
- [ ] 文档同步: SKILL.md 参数表 + 过滤态 / 空结果两个输出示例
- [ ] Rule #6: 跑 `/skill-creator` AB benchmark 并归档结果

## Success Criteria

- [ ] **缺省不变**: 同一仓库同一时刻, 不传 `issue_label` 时 🎫 区块输出与改动前 diff 为空 (逐字比对, 非人眼「看起来一样」)
- [ ] **过滤正确且不漏**: 传 `issue_label=bug` 时, 区块内条目集合与直接查询 `labels=bug` 的结果集合**相等** (既不含多余项, 也不缺项)
- [ ] **空结果可分辨**: 传一个仓库中不存在的 label 时, 区块显示明确的 0 条文案; 既不报错中断整个扫描, 也不回退成全量
- [ ] **多 label 语义成文且可证伪**: SKILL.md 明确写出多 label 是 AND 还是 OR, 并有一条对应的验证记录 (真实仓库实测输出), 而非只写一句断言
- [ ] **标题回显**: 过滤生效时区块标题含当前 label, 使「过滤后子集」不可能被读成全量
- [ ] **正交性**: state-scanner 其它区块 (分支 / Spec / handoff / 版本面) 在传参与不传参两种情况下输出均无差异
- [ ] **Rule #6**: AB benchmark 已跑并归档, 分数不低于基线

---

> 建议后续: 运行 `openspec validate state-scanner-issue-label-filter --strict` 验证格式, 然后进入 A.2 任务规划。本 Spec 为 Level 2, 不生成 `tasks.md` (上面的 Tasks 清单即粗粒度分解, 细化交由 A.2 的 `detailed-tasks.yaml`)。
