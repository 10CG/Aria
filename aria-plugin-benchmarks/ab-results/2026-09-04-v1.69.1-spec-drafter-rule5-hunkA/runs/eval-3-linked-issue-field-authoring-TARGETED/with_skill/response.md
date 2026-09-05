按 spec-drafter A.1 流程推演 (描述性, 未落盘):

- **A.1.0 头脑风暴检查**: 需求边界清晰 (单个可选参数, 默认行为不变), 无需 `brainstorm.technical`; 无决策记录可引用, 故 proposal 不含「决策来源」行。
- **A.1.2 Level 判断**: 关键词「加 / 可选参数 / 过滤」命中 Level 2 增强改进词; 单模块 (state-scanner 自身 SKILL.md + 其取数脚本); 可选参数 ⇒ 非 breaking; 影响文件 2-5 ⇒ **Level 2 (Minimal)**, 只出 `proposal.md`, 不出 `tasks.md`。
- **A.1.3 模块检测**: `standards` 类 (Skill / OpenSpec 关键词)。
- **A.1.4 落点**: `openspec/changes/state-scanner-issue-label-filter/proposal.md` —— **本项目仓内**, 不是 `standards/openspec/changes/` (不可协商规则 #5)。
- **头部字段**: 已核实无关联 issue ⇒ `Linked Issue` 值逐字写 `` `none` ``, 不留空、不删行 (`N/A` / `TBD` / `-` 不是哨兵)。
- **Framework Constraints**: 本变更不涉及 Next.js / Astro 等 framework 项目, 按 A.1.1 跳过该段。

---

```markdown
# state-scanner Open Issues Label Filter

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-04
> **Linked Issue**: `none`

## Why

state-scanner 的 🎫 Open Issues 区块当前无条件列出全部 open issue。issue 数量增长后, 单个周期真正相关的往往只是其中一类 (如 `bug` / `rule6` / `v2.0`), 其余条目稀释了 A.0 状态扫描的信噪比, 也稀释了它作为工作流推荐输入的判断力。需要一个**可选**的 label 过滤参数, 让扫描按需收窄, 而不传参时行为与今天完全一致。

## What

给 state-scanner 增加一个可选输入参数 (拟名 `issue_label`), 仅作用于 🎫 Open Issues 区块的取数与渲染: 优先以 Forgejo API 的 `labels=` 查询参数在服务端过滤, 服务端不可用时退回读取侧过滤。区块 header 回显当前生效的 filter, 使「过滤后为空」与「本来就没有 open issue」在输出上可区分。

### Key Deliverables
- `aria/skills/state-scanner/SKILL.md`: 输入参数表新增 `issue_label` 行 + Open Issues 区块说明 + 用法示例
- state-scanner issue 取数实现: 参数透传到 Forgejo API `labels=`, 含读取侧过滤兜底
- 渲染层: 有 filter 时区块 header 显示生效值; 0 命中时输出显式的 `0 matched (label=<x>)` 措辞
- 测试与 fixture: 默认无参 golden 一致性 / 单 label / 多 label / 0 命中 / 不存在的 label 五类

## Impact

| Type | Description |
|------|-------------|
| **Positive** | A.0 扫描输出可按关注面收窄, 提升 Open Issues 区块信噪比; 默认路径零改变, 现有调用方无需迁移 |
| **Risk** | **假绿**: 0 命中若静默退回全量或渲染成「无 open issue」, 会被误读为「问题都清了」→ 强制 filter 回显 + 独立的 0-match 措辞, 并用负控 fixture 验证该措辞在坏实现下会红 |
| **Risk** | **默认行为回归**: 参数注入点在共享取数路径上, 可能污染无参调用 → 以旧版输出为基线做 golden 逐字节比对 |
| **Risk** | **Rule #6**: 本变更改动 state-scanner 的运行时指令面 (SKILL.md 参数语义), 属处方性内容, 按判据**照跑 AB**; 若最终落地仅剩描述性 hunk (参数表字段罗列), 按逐 hunk 判并在本文件补 `rule6_note` 说明豁免类别 —— 拿不准一律照跑 |

## Tasks

- [ ] 定位 Open Issues 区块现有取数与渲染路径, 记录参数注入点及其共享范围
- [ ] 定义参数契约: 参数名 / 多 label 语义 (AND 还是 OR, 二选一钉死) / 大小写敏感性 / 缺省值 / 0 命中语义
- [ ] 实现服务端 `labels=` 过滤 + 读取侧兜底 + 区块 header 的 filter 回显
- [ ] 补测试: 无参 golden 一致 / 单 label / 多 label 语义 / 0 命中措辞 / 不存在的 label 不报错
- [ ] 更新 `aria/skills/state-scanner/SKILL.md` 参数表与示例
- [ ] Rule #6: 用 `/skill-creator` 跑 AB, 结果归档 `aria-plugin-benchmarks/ab-results/`
- [ ] 版本面: aria-plugin 版本 bump (SOT = `aria/.claude-plugin/plugin.json`) 及派生文件同步

## Success Criteria

- [ ] 不传 `issue_label` 时, state-scanner 输出与变更前逐字节一致 (golden diff 为空)
- [ ] 传 `issue_label=bug` 时, 区块内 issue id 集合 == API `labels=bug` 返回的 id 集合 (逐 id 比对, 非计数比对)
- [ ] 多 label 语义有一条测试按名字钉死所选语义 (AND 或 OR), 且对相反语义的实现会红
- [ ] 0 命中时输出同时含 filter 回显与 `0 matched` 措辞, 且不含任何未命中 issue; 静默退回全量的坏实现会红
- [ ] 不存在的 label 走 0 命中路径, 不抛异常、不中断整体扫描
- [ ] Rule #6 AB 已跑并归档 (若判豁免, 本文件含 `rule6_note` 及所属豁免类别)
```

---

**A.1.6 验证提示**: 落盘后建议运行 `openspec validate state-scanner-issue-label-filter --strict` 验证格式, 随后进入 A.2 (task-planner)。
