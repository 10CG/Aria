先交代一个前提, 免得你把我的推断当成规范原文。

我这边加载的 `phase-a-planner` SKILL.md (v1.1.0, 最后更新 2026-03-27) 只定义了三件事: A.1-A.3 的编排链 (spec-drafter → task-planner plan → task-planner assign)、跳过规则 (已有活跃 Spec / Level 1 / 已有 detailed-tasks.yaml / hotfix lane)、以及 post_spec 审计挂钩。**它里面没有任何一处提到「A.1 入口认领」、`--raw-track-id` 或 `--linked-issue`**, 同目录下也没有 `references/`。

所以下面凡是能从 skill 正文直接推出的我标 **[skill]**, 凡是我按你给的夹具 + Aria 既有惯例推断出来的我标 **[推断]**。标 [推断] 的那些, 落地前建议用认领脚本的 `--help` 核一遍。

---

## (1) `--raw-track-id` 的实参

我的推断值:

```
1a2b3c4d-add-oauth-login
```

逐段来源:

1. `1a2b3c4d` — 取自 `~/.aria/container-id` 的 **`uuid:` 字段**, 不是 `label:`。理由: `label` 的值是 `devbox-A1-very-long-label`, 人可读但过长、可改名、还可能重名; 夹具特意把它写成 "very-long-label" 本身就是在暗示它不适合直接进标识符。`uuid` 是短且稳定的机器标识, 认领这种要跨终端比对的场景应该钉在稳定值上。
2. `add-oauth-login` — 取自本 Spec 目录 `openspec/changes/add-oauth-login/` 的**末段目录名**, 也就是 skill 里 A.1 的输出字段 `spec_id` (SKILL.md 的示例正是 `spec_id: "add-auth-feature"`, 与目录名同形) [skill]。
3. `-` — 两段之间的连接符。

**我不确定、需要你核 `--help` 的三点**:

- 分隔符到底是 `-` / `:` / `/` 中的哪一个。我选 `-` 只是因为它在两段值里都不出现, 不会产生歧义 (`uuid` 是 hex, `spec_id` 是 kebab-case 但整体可切回来靠"第一个 `-` 之前"这条规则会出错 —— 所以如果工具要反解析, 更可能用 `:` 或 `/`)。这一条我给的置信度最低。
- 要不要带 `label`。如果 track id 是给人看的, 可能是 `uuid + label + spec_id` 三段。
- flag 名里的 **`raw`** 是什么意思。最合理的解读是: 传进去的是**未经规范化的原始串**, 由工具自己负责 sanitize / 截断 / 哈希; 若真是这样, 那 label 长不长根本不重要, 甚至可能期望你把 `container-id` 里的原始行原样喂进去。这个词是个信号, 值得先确认再传。

---

## (2) 三份 proposal 各自要不要传 `--linked-issue`

| 候选 | `Linked Issue` 字段值 | 传不传 | 实参 |
|------|----------------------|--------|------|
| A | `10CG/Aria#174` | **传** | `10CG/Aria#174` (逐字) |
| B | `none` | **不传** | 省略整个 flag |
| C | `[#174](https://forgejo.10cg.pub/10CG/Aria/issues/174)` | **传** | `10CG/Aria#174` (归一后, 不逐字) |

理由:

- **A**: 已经是 `owner/repo#number` 的规范短形, 唯一、可机读, 原样传。
- **B**: `none` 是「没有关联 issue」的**占位值**, 不是一个 issue 标识。把字面量字符串 `none` 传给 `--linked-issue` 会凭空造出一个假关联 —— 认领记录里会出现一个叫 `none` 的 issue, 后续任何按 issue 去 join / 去核对的动作都会被它污染。**「没有值」的正确表达是不传这个 flag**, 不是传一个表示空的字符串。
- **C**: 指向的是**同一个 issue**, 但形式是 markdown 链接, 不能逐字传。两个原因: 【1】命令行实参应该是机器可解析的标识, markdown 的 `[...]()` 是渲染语法, 传进去要么被工具当成 issue 名, 要么解析失败; 【2】方括号和圆括号在 shell 里还有 glob / subshell 语义, 即使加引号也是自找麻烦。从 URL path `/10CG/Aria/issues/174` 可以无歧义还原出 owner=`10CG`、repo=`Aria`、number=`174`, 归一成 `10CG/Aria#174` 即可 —— 这样它和 A 也就成了字节相同的同一个值, 这正是我们想要的 (下条)。

**顺带一个我觉得你会关心的观察**: A 和 C 归一后是**同一个 issue #174**。三份候选 proposal 里有两份挂在同一个 issue 上。这要么是有意的 (同一 issue 拆两份 Spec), 要么是重复起草。起草 `add-oauth-login` 之前值得先确认一下你现在这份属于哪一份候选、以及和另一份的边界在哪 —— 认领机制能挡住"两个终端同时干同一件事", 挡不住"两份 Spec 声称在解同一个 issue"。

---

## (3) 起草到一半决定放弃

按重要性排序四件事:

1. **显式释放认领, 不要让它悬着** [推断]。stale claim 对别的终端 / 别的 session 表现为「有人正在做这件事」, 会把真正想接手的人挡在门外, 而且这种阻塞是静默的 —— 没人会收到「那个人已经放弃了」的通知。具体动作应该是同一个认领命令的 release 动作 (`--release` 之类) 或删掉它写下的 claim 记录; **不要靠"反正会过期"**, 过期窗口期间的阻塞是真实成本。
2. **清掉半成品的 `openspec/changes/add-oauth-login/`** [skill]。这条是从 skill 正文直接推出来的: 跳过规则写着「`openspec/changes/{any}/proposal.md` exists 且 status 为 `approved` / `in_progress` → skip A.1, use existing spec_id」。一份被放弃的半成品 proposal 留在活跃目录里, 会让**下一次** A.1 误判成「已有活跃 Spec」而整步跳过, 然后带着一份没写完的规格直接进 A.2 任务规划。这个坑是延迟爆的, 当场看不出来。
3. **顺手清掉已经建的分支 / worktree** (如果放弃前已经走到 B.1)。
4. **把"为什么放弃"留一句在 handoff 里**。放弃某个方向本身是个决策, 下一次有人 (或你自己) 想到同一个方向时, 有这一句就不用重走一遍。这属于 Rule #9 的 `docs/handoff/`, 不用为它单独立 Spec。

---

## (4) Level 1 命中 / `coordination.enabled = false`

这两种情形都导向「不认领」, 但**理由完全不同**, 不能混着答:

**情形一: `skip_if: complexity: Level1` 命中的简单修复** [skill]

SKILL.md 两处写死了这条: 「不使用场景 — 简单修复 (Level 1) → 直接跳过 Phase A」, 跳过规则表里也是「复杂度 Level1 → 跳过 A.1」。既然 A.1 这一步**根本不执行**, 那"A.1 入口认领"这个动作就不存在, `--raw-track-id` 和 `--linked-issue` 都无从谈起 —— 不是"该传但豁免了", 是**要认领的那个对象整个没产生**。

这个区分很重要: 它是**结构性前提不成立**, 属于 Rule #10 白名单里封闭四类的最后一类, 不是我临场判断「这次改动小所以不值得认领」。反过来说, 如果 A.1 确实执行了 (哪怕产出的是一份很短的 Level 2 proposal), 就没有"简单所以免认领"这一档 ——「存在但简单」不算前提不成立。

**情形二: `coordination.enabled` 为 false** [推断]

协调机制整体被关掉, 认领命令要么是 no-op, 要么根本不该调。此时 **A.1 照常走** —— Spec 还是要起草, 跳过的只是 claim 这一个动作, 不是 Phase A。

代价要说清楚: 你失去的是并发保护。如果此刻有第二个终端 / 第二个 session 在同一个仓上干活, 撞车不会有任何机械信号, 得靠别的方式兜 —— 动手前先看一眼 `docs/handoff/latest.md` 有没有 in-flight track, 或者直接跟对面口头对一下。这在 Aria 现在多轨并行的状态下是真实风险, 不是理论风险。

另外一句提醒: `coordination.enabled` 如果当前是 **enabled**, 我这边**不能**因为「这次是文档改动 / Level 低 / 性价比不高」就自己把它当 false 处理或跳过认领 —— enabled 的闸门是 owner 的配置决定 (Rule #10)。要关得你在 `.aria/config.json` 里显式关。

---

## 我建议的下一步

上面标 [推断] 的部分 —— (1) 的分隔符和字段选择、(2) 的归一化规则是不是工具自己做、(3) 的 release 具体命令 —— 都还停在"合理推测"这一层。你把认领脚本的 `--help` 输出 (或它所属的 SKILL.md / reference 文件) 贴给我, 我可以把这几条钉到字符级。

还有一个更值得处理的事: **`phase-a-planner` 的 SKILL.md 里完全没有这段内容**。如果 A.1 入口认领已经是既定流程, 那这是 skill 的一个真实缺口 —— 执行 Phase A 的人从 skill 里读不到自己该认领, 只能靠口口相传。这个缺口本身值得开一个 issue。
