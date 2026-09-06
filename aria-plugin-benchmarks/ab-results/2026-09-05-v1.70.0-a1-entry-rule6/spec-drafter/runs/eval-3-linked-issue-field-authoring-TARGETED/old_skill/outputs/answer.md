按 spec-drafter (A.1) 走了一遍。先给判断过程, 再给 proposal.md 全文 —— **只输出, 不写入仓库**。

---

## A.1.0 头脑风暴检查

扫了 `docs/decisions/`, 没有与「Open Issues 区块过滤」相关的 technical decision-log。这个需求边界清晰 (单 skill、单区块、可选参数)、无方案分歧, 判定**不必先跑 brainstorm.technical**; 若你希望先讨论「过滤发生在抓取期还是渲染期」这一点, 可以回退到 `brainstorm.technical` 再回来预填充。

## A.1.2 Level 判断 → **Level 2 (Minimal)**

| 因素 | 观察 | 倾向 |
|------|------|------|
| 关键词 | 「加一个可选参数」= add / 扩展, 无 refactor / breaking / 跨模块 | Level 2 |
| 影响范围 | 单模块: `aria/skills/state-scanner/` (scan 入口 + issue_scan collector + references + tests) | Level 2 |
| 变更类型 | 纯增量, 参数可选、缺省行为不变, 非 breaking | Level 2 |
| 冲突处理 | 「小功能」暗示 Level 1, 但涉及行为逻辑 + 测试 + 文档三面, 按「冲突取高」规则取 Level 2 | Level 2 |

⇒ 产出物: `proposal.md`, 不生成 `tasks.md`。

## A.1.3 模块检测 → `standards` 系 (aria-plugin skill 层)

落点: `openspec/changes/state-scanner-issue-label-runtime-filter/proposal.md` —— **本项目仓内**, 不放 `standards/openspec/changes/` (不可协商规则 #5)。

## A.1.1 补充说明

- **Framework Constraints**: 本变更是 Python 脚本 + Markdown 文档, 非 Next.js / Astro 等 framework 项目, 该段跳过。
- **一处现状勘正 (影响 What 的写法)**: `state_scanner.issue_scan.label_filter` **已经存在** (array, 默认 `[]`), 但它是**配置级 + 抓取期**过滤 (`issue_scan.py:_fetch_repo` 在 normalize 之后、写缓存之前过滤)。所以本 Spec 要做的不是「从零加过滤」, 而是加一个**单次调用生效、不改配置、不污染缓存**的运行时参数。这条区分直接决定了实现落点, 已写进 proposal 的 Why/What。
- **Linked Issue**: 你已核实该功能没有对应的 issue ⇒ 按头部字段要求逐字写 `` `none` `` (哨兵, 不留空、不删行; `N/A` / `TBD` / `-` 都会被机械 check 判不合规)。

---

```
╔══════════════════════════════════════════════════════════╗
║           SPEC DRAFT PREVIEW (Level 2)                   ║
╚══════════════════════════════════════════════════════════╝

Feature: state-scanner-issue-label-runtime-filter
Module: standards (aria-plugin / state-scanner skill)
Location: openspec/changes/state-scanner-issue-label-runtime-filter/proposal.md
```

## proposal.md 全文

````markdown
# state-scanner Open Issues 运行时 label 过滤参数

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-05
> **Linked Issue**: `none`

## Why

state-scanner 阶段 1.13 的 🎫 Open Issues 区块目前只能整块呈现。既有的 `state_scanner.issue_scan.label_filter` 只解决了「长期固定口味」这一半:

1. 它是**配置级**的 —— 换一次过滤条件要编辑 `.aria/config.json`, 用完还得改回去;
2. 它是**抓取期**生效的 —— 过滤后的结果直接落进 `.aria/cache/issues.json`, 换条件后在 `cache_ttl_seconds` (默认 900s) 内会读到按旧条件裁剪过的缓存, 表现为「改了配置却没变化」;
3. 因此日常那类**一次性**诉求 ("这次只想看 `blocker`") 没有承载面。

缺的是一个「本次调用生效、不改配置、不污染缓存」的可选参数。

## What

给 state-scanner 增加一个**可选的、单次调用生效**的 label 过滤参数, 只影响 🎫 Open Issues 区块的呈现, 不改变抓取与缓存语义。

- **参数**: `--issue-label <label>`, 可重复传 (`--issue-label bug --issue-label blocker`), 亦接受逗号分隔 (`--issue-label bug,blocker`)。
- **匹配语义**: 命中任一 label 即保留 (OR / any-match), 与既有 `label_filter` 的 `set.intersection` 语义一致; label 比较大小写敏感, 与平台返回值逐字比对。
- **作用位置 (承重决策)**: 过滤发生在**渲染侧** —— 读缓存 / 抓取完成之后, 组装 `issue_status` 展示视图之前。**不**进入 `_fetch_repo`, **不**参与 cache key, **不**写回缓存。理由: 抓取期过滤会把裁剪后的子集当成全量存进缓存, 使下一次不带参数的扫描读到残缺数据。
- **与配置级 `label_filter` 的叠加**: 配置级先在抓取期生效, 运行时参数在其结果上再过滤 (AND 关系, 即两者都要满足); 两者同时非空时在区块头一行显式标注生效来源, 避免用户把「配置已滤掉」误读成「参数没生效」。
- **缺省行为**: 不传该参数时, 输出与当前版本**字节级一致** (向后兼容硬要求)。
- **opt-in 边界**: `issue_scan.enabled=false` 时传该参数 → 不报错、不改退出码, 区块照旧完全省略, 仅在诊断行提示「参数已忽略 (issue_scan 未启用)」。fail-soft 契约不变。
- **空结果呈现**: 过滤后为 0 条时区块**仍然显示**, 计数写成 `0 / N (label: bug)`, 与「本来就没有 open issue」区分开。
- **非目标**: 不改 `label_summary` 的聚合口径 (仍按全量统计), 不加 label 的排除语法 (`!bug`), 不扫 PR, 不做写操作。

### Key Deliverables

- `aria/skills/state-scanner/scripts/scan.py` — argparse 新增 `--issue-label` (action append + 逗号拆分归一), 透传至阶段 1.13
- `aria/skills/state-scanner/scripts/collectors/issue_scan.py` — 新增渲染侧过滤函数 + 生效来源标注; `_fetch_repo` / 缓存读写路径**不改**
- `aria/skills/state-scanner/references/issue-scanning.md` — 配置项表后新增「运行时参数」小节, 写清与 `label_filter` 的叠加关系与缓存不变式
- `aria/skills/state-scanner/references/output-formats.md` — 🎫 Open Issues 区块补过滤态 / 过滤后为空两个样例
- `aria/skills/state-scanner/SKILL.md` — 参数清单与阶段 1.13 描述同步
- `aria/skills/state-scanner/tests/test_issue_scan_mocked.py` — 新增用例 (见 Success Criteria)

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 一次性 label 过滤不再需要改配置 + 等 TTL; 「改了配置没变化」这个缓存陷阱不会被新参数复制一遍 |
| **Risk** | 若实现落到抓取期, 会把过滤后的子集写进缓存并污染后续不带参数的扫描 —— 这是本变更**最容易犯**的错, 需由测试钉住 (见 SC-4) |
| **Risk** | 配置级与运行时两层过滤叠加时语义易被误读 (AND 而非覆盖), 需靠输出侧显式标注消解 |
| **Scope** | 单模块 (aria-plugin / state-scanner), 无跨模块契约变更, `issue_status` schema 不升版 |
| **Backward Compatibility** | 参数可选; 不传参数时输出与当前版本一致, 无 MAJOR/MINOR 破坏性 |
| **流程约束** | 本变更改动 skill 运行时行为 ⇒ 发版前须按不可协商规则 #6 用 `/skill-creator` 跑 AB benchmark, 不适用豁免 |

## Tasks

- [ ] 在 `scan.py` 加 `--issue-label` 参数并归一化 (重复传 + 逗号分隔 → 去重列表)
- [ ] 在 `issue_scan.py` 渲染侧实现过滤, 并断言不触及 `_fetch_repo` 与缓存写入路径
- [ ] 实现配置级 / 运行时两层过滤的叠加与来源标注
- [ ] 处理 `enabled=false` + 过滤后为空 两个边界分支
- [ ] 补测试 (含缓存不变式与缺省行为回归)
- [ ] 同步 SKILL.md / issue-scanning.md / output-formats.md
- [ ] 跑 Rule #6 AB benchmark

## Success Criteria

- [ ] **SC-1 缺省不变**: 不传 `--issue-label` 时, 同一 mock 输入下的 🎫 Open Issues 区块输出与变更前**逐字节相同** (diff 为空)
- [ ] **SC-2 过滤正确**: mock 5 条 issue (labels 分别为 `bug` / `enhancement` / `bug,blocker` / 无 label / `blocker`), `--issue-label bug` 得 2 条, `--issue-label bug,blocker` 得 3 条 (OR 语义)
- [ ] **SC-3 空结果不塌陷**: `--issue-label nonexistent-label` 时区块仍出现, 计数逐字含 `0 / 5`, 且退出码为 0
- [ ] **SC-4 缓存不被污染 (负控)**: 带 `--issue-label bug` 跑一次后, `.aria/cache/issues.json` 的 `items` 长度仍为 5; 该断言在「把过滤误放进 `_fetch_repo`」的坏实现下必须转红 —— 实施时先构造该坏实现跑一次确认它会红, 再删掉
- [ ] **SC-5 叠加语义**: 配置 `label_filter=["bug","enhancement"]` + 参数 `--issue-label bug` 时结果为两者交集 (2 条), 且输出含两层来源标注
- [ ] **SC-6 opt-in 不破**: `issue_scan.enabled=false` + 传参 → 无 traceback、无非零退出码、区块不出现, 提示行存在
- [ ] **SC-7 文档同步**: `issue-scanning.md` 与 `output-formats.md` 均含该参数与缓存不变式描述 (不可协商规则 #3)
````

---

## A.1.6 验证提示与下一步

1. 上面**只是预览**, 按你的要求没有写入 `openspec/changes/`, 也没有跑 git 或任何脚本。
2. 落盘后建议跑 `openspec validate state-scanner-issue-label-runtime-filter --strict` 验证格式。
3. Level 2 不生成 `tasks.md`; 下一步进 A.2, 用 `/task-planner` 把上面 7 条 Tasks 展成 `detailed-tasks.yaml` (含文件路径与估算), 再进 B.1 建分支。

要我把这份 proposal 写进仓库、或者调整 feature 目录名 (当前用的是 `state-scanner-issue-label-runtime-filter`) 的话, 说一声。
