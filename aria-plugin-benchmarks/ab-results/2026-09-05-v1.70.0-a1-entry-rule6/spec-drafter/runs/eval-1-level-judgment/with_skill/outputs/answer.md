判定结果: **Level 1 (Skip) —— 不需要 Spec**。

```
═══════════════════════════════════════════════════════════
  LEVEL 1 DETECTED - SKIP SPEC
═══════════════════════════════════════════════════════════

需求: 修复登录页面一个 typo
类型: 文案/拼写修复 (Typo)
模块: mobile 或 frontend (登录页面 UI; 单模块)
影响: 单文件、单处字符串
风险: 极低 (无逻辑变更、无契约变更、无 breaking)

推荐操作:
   跳过 A.1 (不写 proposal.md)，直接进入 B.1 (分支创建) 开始开发
```

## 为什么是 Level 1

按 `LEVEL_GUIDE.md` 的判断链逐项过一遍:

**1. 决策流程图 Q1 —— 「是否简单修复/配置/文档格式?」= YES**
命中即落 Level 1，不再往下走 Q2 (架构/跨模块/Breaking)。

**2. 关键词匹配**

| 维度 | 命中 | 说明 |
|------|------|------|
| Level 1 触发词 | `typo`、`修复` | `typo` / `fix typo` 属**高置信度**触发词 |
| 上下文限定词 | 「一个」 | 等价于 "just / only / a single"，进一步收窄范围 |
| Level 2 触发词 | 无 | 没有 feature / add / implement / new / 组件 等功能开发词 |
| Level 3 触发词 | 无 | 没有 refactor / 架构 / breaking / migration / 跨模块 |

关键词冲突解决规则 (`Level 3 > Level 2 > Level 1`) **不触发** —— 因为没有更高级别的词与之竞争。对照 `LEVEL_GUIDE.md` 边界情况里那个反例 "Add simple authentication feature"：那里 "simple" 与 "authentication feature" 冲突所以升到 Level 2；本例中 "typo" 是**唯一**的性质词，没有东西把它顶上去。

**3. 文件影响分析**
- 单模块 (登录页面所属的前端/mobile 模块)，不涉及 2 个及以上模块
- 不改 `shared/`，不涉及 API 契约变更
- 因此**跨模块自动提升 Level 3** 的条件不成立

**4. 变更类型识别**
纯文案更正，不改行为、不改数据模型、不改接口签名 ⇒ 非 breaking change。

**5. 综合评分**
关键词 (40%) 落最低档、影响范围 (30%) 单文件、变更类型 (20%) 非破坏性、历史模式 (10%) 与 "Fix typo in README" 同型 ⇒ `score < 3` ⇒ Level 1。

结论与 `LEVEL_GUIDE.md` 示例 3 (`"Fix typo in README" → Level 1 (Skip)`) 完全同型。

## 接下来怎么做

1. 跳过 A.1，不创建 `openspec/changes/<slug>/`；本次不产出 proposal.md，也就没有 `Linked Issue` 字段、`openspec validate` 等后续动作。
2. 直接进入 **B.1 分支创建** (`branch-manager`)，例如 `fix/login-page-typo`。
3. 提交按 Conventional Commits：文案是 UI 可见字符串用 `fix(login): ...`；若只是注释/文档里的拼写则用 `docs: ...`。
4. Level 1 只是「跳过 Spec」，**不跳过十步循环的其余闸门** —— B.2 验证、C 集成 (含 pre-merge gate, 规则 #8)、D 收尾照走。

## 需要你确认的两点

**(1) 这个 "typo" 到底是哪一类？** 判定为 Level 1 的前提是它**纯粹**是拼写。下面任一成立就要**上调到 Level 2**，请先确认:

- 改的是 i18n key / 翻译资源 key 本身 (而非 value) —— 会牵动多语言文件与调用点
- 改的不是展示文案而是**标识符**: 表单 `name`、API 字段名、事件埋点名、CSS class、路由 path —— 这属于契约变更，可能 breaking
- 同一处错字在多处复制存在，需要跨模块 sweep (前端 + 后端错误码文案等) —— 触发跨模块条件，直接 Level 3
- 它其实是个**内容错误**而不是拼写错误 (例如提示语说反了语义)，那是行为修正而非 typo

若属以上任一，请告诉我，我按 Level 2 起草 `proposal.md`。你也可以直接用 `level_override=2` 强制覆盖本次判断。

**(2) A.1 前置认领 (claim)。** 本次是**直接调用** `spec-drafter`，没有经过 `phase-a-planner`，所以 SKILL 里那条「起草之前先认领」的 MUST 落在我这一侧；而且该块**没有 Level 1 例外** (直调路径的设计前提是「进来时还没有 Level 判定」)。判定结果是 Level 1 ⇒ 本次不会起草任何产物、不会有 `openspec/changes/<slug>/`，也就没有可投入的工作面需要防重复。所以我**没有**执行下面这条命令，把它连同判断一并交给你复议，而不是自行认定豁免:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "login-page-typo-<container_uuid>" \
  --phase A.1 --mode advisory \
  --include-terminal \
  --repo-path "<主仓根>"
```

(`<container_uuid>` 取 `~/.aria/container-id` 的 `uuid` 字段，不是 `label`；`--linked-issue` 本次省略 —— 没有 proposal.md 可供 `linked_issue_field_probe.py` 抽取，按规则「输出为空 ⇒ 整个参数省略」，绝不传哨兵。)

如果你希望即使 Level 1 也照认领 (例如已经有对应 issue、想先占坑防止另一个容器重复修同一处)，说一声我就跑；只要跑了，后续放弃方向时我会补 `release_gate.py --raw-track-id <同一串> --status abandoned`，避免留下永不释放的僵尸 claim。
