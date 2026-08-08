---
track-id: linked-issue-normalization
owner-container: aria-runner-bot/023236f2
phase: session-close
status: done
updated-at: 2026-08-08T18:40:00Z
---

# Session Handoff (2026-08-08) — post_planning 四轮闸门 + 三起跨仓归属转交

> 会话维度增量。承接 [2026-08-08 上一段](./2026-08-08-linked-issue-norm-three-audit-rounds-to-structural-split.md) (同日两段)。
>
> **本段主线 = 两件事**: (a) owner 提的一个归属问题, 拆出**三起跨仓转交**并顺带查出一条传了 10 次的错挂期限; (b) `linked-issue-normalization` 走 A.2/A.3 + **post_planning 闸门四轮 / 17 个审计 agent**, 每一轮都 FAIL, 而**每一轮的缺陷都是上一轮 fix 造的**。
>
> **最有价值的产出不是那份计划, 是三个可复现的失败形状**: 委派而不核实目标 ×2 · 枚举不完整 ×2 · 假自陈 ×2 · 同一处恒红 ×3。四轮下来它们**换了内容没换机制** —— 这比任何单项 finding 都值得记。

## §0 入口 (新 session 优先读)

- **当前态**: 主仓 **`036dddf`** (§0 初写时为 `97a3885` —— §10 之后又落 4 个 commit, **此处已随收尾更新**), 双远端 `ls-remote` 核验一致, 零 ahead。工作区仅 `aria-orchestrator` (一贯排除)。custom checks **8/8**。
- **`[1]` 已完成**: 凭据轮换转交 Aether · silknode waiver 拆分关闭 · terminal 语义开号 · 探针去恒红。
- **`[2]` 停在 R4-fix, 闸门未收敛** (`max_rounds=4` 已耗尽): `converged: false`。产物 21 active + 7 cancelled 任务, 全部机械核验通过, **但仍有 2 条不可在本 Spec 内修的 Critical** (见 §2)。
- **`[3]` 未启动**: `secret-guard-per-segment-evaluation` R4。⚠️ **§0 初写时的「前置已清」判断已过期** —— 收尾时发现并发轨 (`simonfishgit`) 当日 08:42 / 12:08 / 16:34-17:31 均有活动 (2 张 issue + 3 个 commit) ⇒ **下段开跑前必须重新 fetch + 查看板**, 不得沿用 §4.1。
- **`[1]` (owner 收尾后追加)**: 发布路径 —— 陈旧 memory 已更正 · aria-plugin **#137 走完 A.1** (待 post_spec) · **#165 第四次复发已当场检出并修复**。详见 **§10**。
- **下一步**: 见 §6。

## §1 已完成 (本段)

1. **owner 提「凭据轮换该不该转交 Aether」→ 核实成立, 且比问题本身更严重**。三个凭据 (`FORGEJO_TOKEN` / `NEXUS_API_TOKEN` / `CF_ACCESS_CLIENT_SECRET`) 全属 Aether 平面, **Aria 侧零消费** (`NEXUS_API_TOKEN` 全仓 grep 零命中); 轮换工具链本就在 Aether。→ **[Aether #283](https://forgejo.10cg.pub/10CG/Aether/issues/283)** + 归属迁移记录。
2. **顺带查出一条错挂期限**: `2026-08-02` hard cap 属**另一组 4 key** (GLM + 3×FEISHU), 那组 **Resolved 2026-05-22** 且该文件 §Resolution 逐字写「cap 可撤销」。本组真实来源是 2026-07-19 一次 `assertIn` 对 dict 查键致 unittest 把整个 env 渲染进 failure diff, **从无 decision 指派期限**。cap 在 2026-07-22 handoff 被接上, 此后跨 ~10 份 handoff 传成「逾期不可补救」——**递增的紧迫感全部来自转抄次数, 无一次回源核验**。
3. **silknode waiver 按 owner 裁定拆分关闭** (非续期非 acceptance 全 MET): 契约 1 → **[SilkNode #979](https://forgejo.10cg.pub/10CG/SilkNode/issues/979)** (归属转交, 接到该仓现有 data-controls 轨); 契约 2 → **[Aria #175](https://forgejo.10cg.pub/10CG/Aria/issues/175)** (重写为「数据卫生纪律 + 法务结论适用范围声明」两条, 需 L2 Spec)。waiver 标 `superseded_by_split`。
4. **探针去恒红**: `silknode-contract-deferral-expiry` 原只比 `expires_at`, 豁免一经取代即永久红。改为先读 `status` + 显式白名单短路 + 其余回落日期比较 (fail-CLOSED), 且终态必须记录承接 URL 否则 `MALFORMED`。**4 项验证** (真绿 / 非终态转红 / 终态缺 URL 报 MALFORMED / 未知值回落转红) → checks **8/8**。
5. **`linked-issue-normalization` A.2 + A.3**: tasks.md 由 R3′ 手术产物 (表格) 重写为 OpenSpec 标准 checkbox; 新建 `detailed-tasks.yaml`。**顺带修掉一个机械盲区**并端到端验证 —— 上一段 §2 记「表格形态使 `handoff_autofill` 完全看不见本 Spec (159 条里零条)」, 本段收尾实测 unfinished **159 → 180**, 新增恰好 21 = 本 Spec active checkbox 数。
6. **post_planning 闸门四轮 (17 个审计 agent)**: R1 五席 5/5 REVISE·FAIL (3C+12M) → R1-fix → R2 五席 2 PASS/3 REVISE·FAIL (2C+11M) → **owner 裁定停止逐条补丁、整组重做组 5** → R2-fix → R3 五席 5/5 FAIL (2C+7M) → R3-fix → **owner 裁定换 2 席新鲜眼睛** → R4 两席 FAIL (**4+2C**, 全是前三轮 15 个 agent 漏掉的)。
7. **7 张新 issue**, 其中三张是类级/根因级:
   - **[aria-plugin #136](https://forgejo.10cg.pub/10CG/aria-plugin/issues/136)** — `branch-manager` 的合并动作是 repo-type-agnostic 的服务端 `Do: merge`, **CLAUDE.md 硬约束 1 在插件层零实现** (全 `aria/skills/` 零命中)。**疑为 Aria #165 三次复发的真正根因**: 纪律写在 CLAUDE.md, 而做事的工具做被禁的动作, 中间无守卫 ⇒ 三次复发的每一次都可以由「按插件流程正常操作」产生, 不需要任何人违规。
   - **[aria-plugin #137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137)** — `pre_merge_gate.py:427` 的 `--main-branch` **缺省 `"main"` 而本项目是 `master`** ⇒ 实跑 `aether ci status --branch main --in-flight` 返回 `{"runs":[]}` RC=0 ⇒ **「main 无 in-flight」恒真**, Rule #8 那条腿恒绿。SKILL.md 靠一句「显式传真值」纸面兜。
   - **[Aria #177](https://forgejo.10cg.pub/10CG/Aria/issues/177)** — `CLAUDE.md:81`「发布同步面」那行是漏同步面的类级根因, **四错一行**: 文件数口径 / 漏 CLAUDE.md 自己 (自指盲区, 无 check 兜) / 「root README badge」漏 `Plugin Version:` 行 / **「机械兜底: 两条 custom check」是假绿主张** (那两条只覆盖 2/14 个引用点)。
   - 另: [aria-plugin #133](https://forgejo.10cg.pub/10CG/aria-plugin/issues/133) (terminal 语义分歧, 三轮点名无号; 本段补评论把 `collision.py` 三处纳入, 更正为「6 处具名 + 1 处内联, **3 种**成员集」) · [#134](https://forgejo.10cg.pub/10CG/aria-plugin/issues/134) (`test_collision.py` sys.path 顺序倒置, 破 70 天, 只在全量 discovery 时靠别人副作用才能导入)。

## §2 未完成 / Carry-forward

**AI 内省 (load-bearing)**:

- 🔴🔴 **`[2]` 闸门未收敛且 max_rounds 耗尽**, 且 R4 留下**两条本 Spec 内修不了的 Critical**:
  - **C2**: `phase-c-integrator` **没有 gate-only 形态** (C.2.4 触发条件逐字是「即将调用 branch-manager merge action」, green 后直接调用它, 而 merge 唯一实现是服务端 `Do: merge`) ⇒ R3-fix 的核心设计「只要闸门不要合并」**在现有工具里不可实现** ⇒ 已成文为对 **#136** 的真实交付阻塞。**在 #136 落地前, 本 change 的子模块合并只能 owner 手工本地执行, pre-merge gate 需单独调用。**
  - **C3**: 委派的闸门两条腿对本 Spec **都不触发且都失败为绿** (见 §1.7 #137)。
- 🔴 **`[3]` 未启动** — `secret-guard-per-segment-evaluation` R4。config `max_rounds=4` ⇒ **R4 是最后一轮**, 不宜在 context 尾巴上跑。双子星 handoff 已告知该审什么 (v4 相对 v3 的新增面: `has_filter` 13 处转 bash 内建 / 启发式表述 / 判据补漏 `exec` `time` `&` 换行 / 全部 SC 按反事实纪律重写 / 新增 SC-14~17) 与一个关键陷阱 (**仓内 hook 行为不可作证据**, Aria #172 plugin cache 停 1.63.0 ⇒ 验证须 `bash aria/hooks/secret-guard.sh` 直调)。
- 🟡 **三个 owner 裁量项**已提进 verification (R3 指出原先只在 notes ⇒ 可无 owner 表态判绿), 但**仍未裁**: TASK-025 的 (a)/(b) 择一 · TASK-028 的推送授权 · TASK-027 的 AB 门范围。
- 🟡 **`CLAUDE.md` 引了一个不存在的 memory**: 多远程硬约束 2 写「分叉后处置见 memory `feedback_partial_push_creates_mirror_divergence`」—— 该文件**不存在** (memory 目录 + MEMORY.md 索引双零命中)。我是从 CLAUDE.md 抄进 yaml 的, 已移除派生引用。⇒ 最常读的指令文件里, 对**最高危失效模式 (半推造成镜像分叉) 的处置指南是悬空指针**。**未自行补内容** —— 那是发明指南, CLAUDE.md 是 owner 领地。
- 🔴 **一条既有 memory 与 CLAUDE.md 硬约束 1 直接冲突** (收尾时发现): `feedback_coupled_pr_merge_discipline` 逐字写「Coupled PR (submod+main) **用 Forgejo Do=merge**」—— 那正是硬约束 1 (owner 2026-07-20 裁决) **明文禁止**的动作。该 memory 早于该裁决, 现在是一条**会把人引向被禁操作的陈旧指南**, 且与 aria-plugin #136 (工具层零实现该约束) 叠加 ⇒ 纪律层、工具层、记忆层**三处都指向服务端合并**。建议同 #136 一并处置 (改写或标 superseded)。
- 🟡 **`aria/VERSION:56-59` 的第二处当前版本声明**陈旧 (`## 版本号` 围栏块, 实读 `1.47.0`, 陈旧 18 版) —— 正是 aria-report **#158** 版本字段污染的那个冻结串; #158 的修法是把消费方改读 `plugin.json` SOT, **未修这个块本身**。pre-existing, 未开号 (本段已开 7 张)。
- **R4 剩余 Major 未逐条修** (completeness-lens 10 条里约一半): 「既有 6 条测试」在删掉行号锚后全文无处点名 (无法验证「逐字未变」) · 「真并行组」措辞 · `TASK-013/025/027` 三条 deliverables 漏了自己 verification 强制要改的文件 · dangling 清扫只枚举 proposal.md · `scope_repos[].head` 第三次漂移。**按四轮的规律, 逐条修它们大概率再生产等量缺陷** —— 见 §4.1。

**机械补漏 (backstop)**: `handoff_autofill` unfinished **180** 条 (159 → 180, 新增 21 = 本 Spec, 见 §1.5); consistency **10 flags 全是 `active_change_not_in_upm`** (Aria 无 UPM, **恒亮**, 非本段引入); sync **零告警** (master 双远端 equal)。

> **⚠️ 机械补漏本身的盲区 (本段新发现)**: `handoff_autofill` 只数 checkbox。本段把 7 条 CANCELLED 任务改成**加粗删除线**保留编号 (为避免归档门恒红), 于是它们**既不进 unchecked 计数, 也不进任何机械视野** —— 正确, 但**「被取消」这个状态在机械层完全不可见**。若某条 cancelled 的承接方后来也被删, 无任何机制会发红。

## §3 owner 两项裁定 + 一项被推翻的前提

| 裁定 | 内容 | 后续 |
|---|---|---|
| **Q1** (R2 后) | 停止逐条补丁, **按规律整组重做组 5** | 有效 —— Major-only **6 → 6 → 4 首次下降**, 「加轮判据」不再点亮 |
| **Q2** (R2 后) | 删 TASK-016, **委派 `phase-c-integrator`** | ⚠️ **前提被 R3 推翻** (见下) |
| **Q1'** (R3 后) | R4 **换 2 席新鲜眼睛**, 镜头限定两个已知会复发的形状 | **被数据证实** —— 两席抓出 4+2 条 Critical, 全是前三轮 15 个 agent 漏掉的 |

**Q2 的前提是误引, 且责任在我**: R2/tech-lead 以「`phase-c-integrator SKILL.md:242` 本就建模子模块合并」为由判 TASK-016 绕开闸门, owner 据此裁定。R3 两席去读源码 —— **`:242` 实为 *Path coverage 评估*的执行上下文契约**, 与合并动作无关; 真实合并链落到 `branch-manager:625-634` 的服务端 `Do: merge`。**我这一 session 逐条核了十几个 file:line, 偏偏没核这一个, 而它承载了一个 Rule #10 判定和 owner 的裁定。**

**我的处置 (已成文, 请复议)**: R2/N1 把**两件正交的事**混成一件 —— 「谁执行合并」(硬约束 1) 与「哪个闸门批准合并」(Rule #8)。owner 选的「删任务改委派」只解决了后者。故按「**两者都要**」落: TASK-026 只委派 PR/闸门, **新增 TASK-028** 承载硬约束 1+2 + gitlink。这不是恢复原 TASK-016 (编号已冻结), 也不是把 C.2.4 判据抄回来。

## §4 关键风险 / 已知陷阱

### §4.1 四轮的真实教训 —— 换了内容, 没换机制

| 轮 | 席位 vote | 去重 C+M | fix 引入占比 | Major-only |
|---|---|---|---|---|
| R1 | 5/5 REVISE | 3C + 12M | — | 12 |
| R2 | 2 PASS / 3 REVISE | 2C + 11M | 83% / 62% | 6 → **6** |
| R3 | 5/5 REVISE | 2C + 7M | 80% / 100% / 0% | 6 → **4** |
| R4 | 2/2 REVISE | **4C + 2C** | (全新内容, 不可同尺度比) | — |

**两条成文判据在 R3 首次分歧**: 「Major 是否还在降」不再点亮 (整组重做有效), 「fix 引入占比」仍点亮。**backend-architect 的判读最准**:

> 组 5 是整组重derive, 该比例在满是新内容的场景下趋近必然, 不可同尺度比。核心信号是 owner「停止补丁、整组重做」**并未阻止同形状缺陷在全新内容中复发**。

**那三个形状 (我自己犯的, 逐条可复现)**:

1. **委派而不核实目标** ×2 —— 合并交给不做那件事的 Skill (且它做被禁的动作) · gitlink 交给没有那步的 Skill。⇒ **「由 X 保证 / 移交 X」这类表述必须去 X 的源码核它到底做不做**; 引一行说「X 本就做这件事」之前要确认那行讲的就是这件事。
2. **枚举不完整** ×2 —— 同步面按文件数枚举 (漏 7 处) · breakdown 只列主仓 (实测把 `aria/README.md` 写成 `1.66.O` 判 GREEN)。⇒ 最终解法是**整仓 grep 差集** (fail-CLOSED) 替代文件白名单 —— 白名单对未来新增点天然 fail-OPEN, 且逼人去数「失明几处」(写 7, 实为 **10**)。
3. **假自陈** ×2 —— 「只追加不动既有编号」(实际改指两个 ID) · 撤回它的**同一段**又立「十份报告引用继续成立」(对五份 R1 报告为假)。⇒ 同形状、同段落、连续两次。
4. **同一处恒红 ×3** —— 账本不变量: 零命中含 append-only 账本 (恒红) → 「旧值 ≥2」(恒红) → 「≥1」(**仍不可靠**, 实测 `1.65.4`/`1.65.3` 各 **0 次**, 保留形态不一致) → 最终「**行数不减**」。**每次都是在「修恒红」的编辑里造新恒红。**

**⇒ 处方不是加轮, 是**: (a) 换镜头 (R4 两席一次性产出 4+2C 证实了这一点); (b) 把断言做成**可执行的 Phase B 前置 smoke**, 让缺陷在实施时自己发红, 而不是靠一轮轮审计去读 (code-reviewer R3 的结构性建议, 三席收敛到此)。

### §4.2 其他

- **警告不如机械检查**: footer 派生值连续两次写错, 而第二次时那里**已经有一条「每次必须重算」的警告**。警告没拦住, 拦住的是机械核验 ⇒ 已换成可复跑命令。
- **CANCELLED 保留 `- [ ]` 会杀掉归档门**: `DUAL_LAYER_SPEC.md:258` 的示例这么写, 但实跑 `spec_complete.py --gate` 会把它们计入 unchecked, 完工后恒 `7/27` ⇒ tasks 分支永久失效, 只剩 Status 分支 = **声称**。已改加粗删除线 (减法修法)。
- **席位交叉核有效**: knowledge-manager 独立查 Forgejo, 核出 tech-lead 本轮报告里一句失实 (关于 #177 是否已开号)。code-reviewer 核出我把一条更正**对错了人** (「28 Skills」是 tech-lead 说的, 且 28 = 三档全量不等于 Tier 1 的 10)。**我纠正别人的判断时不该只由我自己说了算** —— 本段把更正原样交回被更正方复核, 附「若我错了请指出」, 有效。
- **API 断流两次** (R1 tech-lead / R3 knowledge-manager), 均按 skill 错误处理重试一次成功; **席位数全程未下调**。

## §5 多维度同步状态 (机械核验)

- **git**: 主仓 `97a3885` (**双远端 ls-remote 独立核验一致, 零 ahead**); `aria` `af87cae`; `standards` `2111c84`; `aria-orchestrator` `92acce5` (feature 分支, 只读未动)。
- **custom checks**: **8/8** (`silknode-contract-deferral-expiry` 由 EXPIRED 转 OK, 经 4 项验证确认不是恒绿)。
- **openspec**: 活跃 **10** 不变。`linked-issue-normalization` 升 Level 3 且首次进 `handoff_autofill` 视野 (21 条)。
- **四维 consistency**: 10 flags 全 `active_change_not_in_upm` (Aria 无 UPM, 恒亮)。
- **本 Spec 产物核验**: 21 active + 7 cancelled; parent 1:1 21↔21; 场景加总 45; DAG 无环; 024 早于 028 早于 026; footer 派生值一致。

## §6 Next session 入口 + 优先级

> ⚠️ **本段已随收尾更新** —— §6 初写于 §10 之前, 那一版不含 `[1]` 的产物。

1. 🔴 **`premerge-gate-mainbranch-failclosed` 跑 post_spec** (enabled `convergence`) —— owner 裁定本段不跑、下段跑 (理由: 本 session 已 17 个审计 agent + 四轮 fix, 疲劳期 fix 引入占比实测 80%+)。**这是排期不是跳闸门。** Spec 已 commit, track 已在 A.1 认领。
2. 🔴 **`[3]` `secret-guard-per-segment-evaluation` R4** —— 双子星成文交接项, R4 是 `max_rounds` 最后一轮。**开跑前必 fetch + 查看板** (见 §0 更新)。
3. 🔴 **aria-plugin #136 起 Spec** —— 应在 #137 ship **之后** (让闸门先具备判别力)。建议把「**硬约束 2 的 bump 前守卫**」并入 (§10.5: `gitlink_integrity` 已在事后检出, 守卫应在事前)。
4. 🟡 **三个 owner 裁量项待裁** (TASK-025 择一 / TASK-028 推送授权 / TASK-027 AB 门范围) —— 未裁前那三条任务不得判 done。
5. 🟡 **两件 owner 领地**: CLAUDE.md 的 memory 引用可移植性 (§11.2) · Aria #177 类级根因 (`CLAUDE.md:81`)。
6. **不要逐条修 R4 剩余 Major** —— 四轮实测每次再生产等量缺陷 (§4.1)。

## §7 同步状态 (autofill 机械汇编)

```
[main]              master = 97a3885 | github=equal origin=equal        ✅ 零 ahead
[standards]         (detached) = 2111c84
[aria]              (detached) = af87cae
[aria-orchestrator] feature/m6-cost-model-telemetry = 92acce5 | origin=equal
```

**warnings: 0**。本段 3 次推送均双推 + **逐远端 `ls-remote` 独立核验** (不信 push 回执, 硬约束 2)。

## §8 Memory entries this session

```
[候选 memory]
- 「委派/兜底必须去目标源码核它到底做不做」—— 一 session 两次实证 (合并交给做被禁动作的 Skill / gitlink 交给没那步的 Skill), 且引一行说「X 本就做这件事」之前须确认那行讲的就是这件事 (`:242` 误引承载了一个 Rule #10 判定和 owner 裁定)。type: feedback
- 「按错误的单位枚举 ⇒ 漏项; 修法是整仓差集而非文件白名单」—— 白名单对未来新增点 fail-OPEN 且逼人数「失明几处」(写 7 实为 10)。type: feedback
- 「转抄链上没人回源, 一个已撤销的期限获得 10 次背书」—— 递增的紧迫感全部来自转抄次数; 带日期/计数的 carry 项转抄时必须带源记录路径。type: feedback (已写入 `.aria/decisions/2026-08-08-credential-rotation-ownership-transfer-to-aether.md` §方法论教训)
- 「换镜头 > 加轮」的定量证据 —— R4 两席新鲜眼睛 (镜头限定已知会复发的两个形状) 一次性抓出 4+2C, 全是前三轮 15 个 agent 漏掉的。type: feedback
- 「警告写在旁边拦不住, 拦住的是机械检查」—— 同一处派生值连续两次写错, 第二次时警告已在那里。type: feedback

[未写下经验]
- 「fix 落在一部分地方而非全部」本段第三次 (R3-fix 未扫 metadata.scope_boundary) —— 与既有 `feedback_scoped_git_add_splits_claim_from_landing` 同族但不同形状 (那条是 git add 范围, 这条是同一文件内多处表述), 是否值得独立一条待判。
- 「同一处三次踩同一个恒红」的机制: 每次修恒红时我都在替换阈值而没有换**判据的类型** —— 前两次都基于「旧值命中数」, 只有第三次换成「行数不减」才跳出。可能存在一条更一般的规律: 恒红的修法若仍在同一个量上调阈值, 大概率再恒红。
```

**已有覆盖未重复落**: 声称 vs 落盘 ([[feedback_scoped_git_add_splits_claim_from_landing]]) · 拐点与加轮判据 ([[feedback_audit_marginal_return_goes_negative]] / [[feedback_stop_adding_rounds_when_major_count_flattens]], 本段首次观察到二者**分歧**) · 修实例不修类 ([[feedback_fix_the_class_not_the_instance]], 本段 Aria #177 是按类处置的实例) · 假绿恒红对偶 ([[feedback_false_green_dual_is_permanent_red]], 本段三次实证) · 误引根因 ([[feedback_issue_reporter_root_cause_may_miscite]], `:242` 是干净实例) · 跨 agent 结论独立复核 ([[feedback_cross_agent_verdict_independent_verify]])。

## §9 流程判断留痕 (Rule #10, 请复议)

- **席位数全程未自行下调** (R1/R2/R3 各 5 席, R4 按 owner 裁定 2 席)。两次 API 断流均重试补齐, 未以「已有 4 席」收尾。
- **停轮/加轮从未自行决定** —— R2 后与 R3 后各出一份决策单交 owner, 本段两次裁定均由 owner 做。
- **Q2 的处置是 AI 判断**: owner 裁「删任务改委派」, 而新证据显示该前提是误引; 我按「两者都要」落 (TASK-026 只委派闸门 + 新增 TASK-028 承载硬约束) 而非退回原状。**请复议。**
- **Q3/Q4 owner 要求「给我建议」而非直接裁定**, 我按建议落进 verification 并标「AI 建议, 待 owner 确认」, 未当作已裁。
- **两条纠正了审计席位自己的判断** (AB Tier 1 = 10 个非 28 个 / AD10 治的是无人值守流水线不治交互式 Phase C), 均经我独立实读; 其中一条我**把更正对错了人**, 已在 §4.2 记。**请复议这两条更正本身。**
- **未自行补 CLAUDE.md 的悬空 memory 指针** —— 补内容等于发明指南, 且 CLAUDE.md 是 owner 领地。
- **R4 剩余 Major 未逐条修**是 AI 判断 (依据 §4.1 四轮规律)。**请复议。**
- **推送均在 owner 明确授权后执行**, 3 次全部双推 + 逐远端 ls-remote 核验。

## Cross-references

- 前一段 (同日): [2026-08-08 三轮 post_spec → 结构性切开](./2026-08-08-linked-issue-norm-three-audit-rounds-to-structural-split.md)
- Spec: `openspec/changes/linked-issue-normalization/{proposal.md,tasks.md,detailed-tasks.yaml}`
- 四轮报告 (17 份): `.aria/audit-reports/post_planning-R{1,2,3,4}-*-linked-issue-normalization-*.md`
- 决策单: `.aria/decisions/2026-08-08-post-planning-inflection-owner-decision-sheet.md`
- 归属迁移: `.aria/decisions/2026-08-08-credential-rotation-ownership-transfer-to-aether.md`
- waiver 关闭: `.aria/decisions/2026-05-07-silknode-contract-archive-with-deferred-acceptance.md` §2026-08-08 Closure
- 本段 issue: Aether#283 · SilkNode#979 · Aria#175 · Aria#177 · aria-plugin#133(comment) · #134 · #136 · #137


---

## §10 收尾后增量 — owner 追加「先做 [1]」(发布路径) + 一次并发撞车

> 本段在 §0-§9 写完并推送后继续。**同一 session, 故追加而非另起 handoff** (会话是单元)。

### §10.1 已完成

1. **陈旧 memory 更正** — `feedback_coupled_pr_merge_discipline` 逐字教人对子模块 PR 用 Forgejo `Do=merge`, 那正是 CLAUDE.md 硬约束 1 明文禁止的动作。**没有简单删掉**: 它的洞见 (merge-commit 保 SHA / squash·rebase 孤立指针) 仍然对, 错的是药方。改写后记下一层关系 —— **它为治「squash 造成的 SHA 孤立」而开的药, 恰好造成了「服务端合并造成的镜像孤立」= #165 那个孤立。同一个词两种孤立, 前者的解法是后者的成因。** 这大概是 #165 三次复发的一条来路 (纪律层禁止 / 工具层照做 / 记忆层教人做, 三处不一致)。好在两约束不冲突: 本地 `git merge --no-ff` 同样保 SHA。
2. **aria-plugin #137 走完 A.1** — Spec `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (Level 2, 7 条 SC), commit `ab4da15`。track 已在 **A.1** 主动认领 (`outcome=passed`, 无竞争) —— 比闸门要求的 Phase B 提前, 正是 #135 指出的「闸门在真实成本点下游」那个缺口。
3. **probe 修正了我自己开的 issue #137 两处 + 补一处遗漏** (已发评论):
   - 正文「**两条腿都失败为绿**」→ **只有 (b) 成立**。实读 `path_coverage.py:21/:24` 规则 1: `git diff 失败 → unknown` 而 unknown 是 **fail-toward-covered** ⇒ main 分支名错时 (a) 那条腿反而**更保守**; 观测到的 `not_applicable` 来自「workflow paths 真的不覆盖变更文件」(规则 8) 这个设计内条件, 与分支名无关。**我把两件事混成了一件。**
   - 漏了 **`:300` 函数签名**那个 fail-OPEN 缺省 (只点了 `:427` CLI)。两处必须同批改。
   - 挖出要害: **后端结构上无法区分「分支不存在」与「分支无 run」** —— 自己实跑 `aether ci status --branch main/master --in-flight --json` 返回**完全同形** (`status:ok`, `runs:[]`, RC=0), 而 `aether.py:117-135` 只在 aether 自身失败时抛。⇒ **修法不能只改缺省值**, 必须加独立存在性核验, 否则显式传错分支名仍恒绿。

### §10.2 一次并发撞车 —— 以及 `ls-remote` 当场挣回成本

推 `d321b68` 时 **non-fast-forward 被拒**: 双远端在 `a6ff6a3`, 不是我先前的 `97a3885`。**双子星 (`simonfishgit`) 在我工作期间推了两个 commit** (`068d387` gitlink bump + `a6ff6a3` 会话收尾)。

> **push 的 hint 很容易一眼滑过 —— 抓到它的是逐远端 `ls-remote` 核验** (硬约束 2)。这是本 session 第二次由该核验兜住 (第一次是常规确认)。文件级零交集, 干净 rebase, 未 force。

**对方那一段与本段高度重叠且处理得当**: 它独立发现了同一条 hard-cap 传递失真 (并自承单 session 内传了三次); 与我的 `096e21d` 撞车后**逐项比优劣、撤回自己三处劣解只保留 memo 增量**; 还顺带补了一个 #165 形状的 orphaned gitlink。

### §10.3 更正的更正 —— 一条比双方原断言都大的发现

对方 handoff 纠正我: 「CLAUDE.md 引了不存在的 memory `feedback_partial_push_creates_mirror_divergence`」**不实**, 它核实**三处齐全**; 真正悬空的是 `feedback_concurrent_duplicate_audit_fetch_before_start`。

**在本容器 (`023236f2`) 实测, 两项恰好相反**:

| | 文件 | `MEMORY.md` 索引 | 目录求总体 |
|---|---|---|---|
| `..._partial_push_creates_mirror_divergence` | **不存在** | 0 | `mirror\|push` 仅 2 文件, 均非它 |
| `..._concurrent_duplicate_audit_fetch_before_start` | **存在** (3774B, Jul 12) | 1 | — |

**但我不认为它测错了。** 关键在一个双方都没说明的前提: **memory store 是容器本地的, 不在仓里** (`~/.claude/projects/*/memory/`)。`bfe8285d` 有它自己一份。⇒ **两个测量可以同时为真。**

**⇒ 真正的发现**: `CLAUDE.md` 是**仓内共享**文件, 却引用**容器本地**的 memory 文件名。谁的 store 缺那条, 那句引用对谁就是悬空的 —— 而**任何第三方采用 Aria 的项目一条都没有**。⇒ 「某 memory 不存在」这一整类断言, **不说明测的是哪个 store 时跨容器不可比**; 而 CLAUDE.md / 成文规范里引 memory 名这个做法本身有可移植性问题 (Aria 对外发布的是方法论与插件, memory 不随之分发)。

**建议**: (a) 双方 handoff 此后写「某 memory 不存在」时必须带 store 路径与容器 id; (b) 评估 CLAUDE.md / standards 里引 memory 名的做法 —— 或改引 `standards/conventions/` 的成文条款 (那些**在仓里**), 或明确标注「本条指向 Lab 内部 memory, 第三方不适用」。**未自行改 CLAUDE.md** (owner 领地)。

### §10.4 §10 段的 Carry-forward

- 🔴 **`premerge-gate-mainbranch-failclosed` 待 post_spec** (enabled `convergence`) —— owner 裁定**下一段跑**。理由是本 session 已 17 个审计 agent + 四轮 fix, 疲劳期 fix 引入占比实测 80%+, 聚合与修的质量在新 session 更好。**这不是跳闸门, 是排期。**
- 🔴 **aria-plugin #136 未起 Spec** —— 面更大 (处方性 SKILL 变更 + **照跑 AB**, 套件 `ab-suite/branch-manager.json` 存在 + 需 gate-only 形态)。**#137 应先 ship** (让闸门先具备判别力)。
- 🟡 **本容器有 5 条 `active` claim**: 4 条来自 2026-08-02 (`linked-issue-normalization` / `aria-plugin-125-126` / `aria-a1-entry-claim-guard` / `aria-plugin-124-path-coverage-z-flag`) + 本段新增 1 条。`--sweep-stale` 扫不掉前 4 条, 因 `heartbeat_at` 冻结在 acquire (**aria-plugin #107**)。其中 3 条的真实状态我不确定, **未猜测性 release**。
- 🟡 **dogfood 观察**: 本段认领时 `linked_issue_overlap: []`, 而我传的是 org 限定形 `10CG/aria-plugin#137` —— 若他人用裸形认领, 当前裸 `!=` 谓词会漏报, 这个 `[]` 便分不清「真没有」与「谓词没匹配」。**我此刻正依赖着 `linked-issue-normalization` 要修的那个缺陷。**

### §10.5 Aria #165 第四次复发 —— 当场检出并修复 (owner 授权)

收尾时重跑 `scan.py`, `overall_parity` **转 false** 且 `gitlink_integrity` 出现 **`orphaned`**。

**诊断** (逐项实测):

| | aria-orchestrator master |
|---|---|
| `origin` (Forgejo) | `237045a` ✅ 主仓 gitlink 可达 |
| `github` (镜像) | `86bb684` ❌ **`237045a` 不可达** |

⇒ 并发轨把 aria-orchestrator 的 commit **只推了 origin**, 随后把主仓 gitlink bump 到它并**双推了主仓** ⇒ **GitHub 上主仓 gitlink 指向镜像里不存在的 commit, `clone --recursive` 断裂**。这就是 #165 的形状, 第四次。

**值得记的三点**:

1. **这次是机械检出的, 不是靠人注意到。** `gitlink_integrity[]` (per-(R,S) 9 分支状态) 直接把 `github/aria-orchestrator: orphaned` 打出来并把 `overall_parity` 拉成 false。⇒ memory `feedback_mirror_sync_needs_mechanical_backstop` 要的「机械兜底」**在检测侧确实起作用了**; 缺的仍是**bump 前的预防侧守卫** (那正是 aria-plugin #136 那类)。
2. **两条硬约束的 enforcement 是不对称的。** 并发轨在子模块侧**遵守了硬约束 1** (`22d7f97` 是本地 merge commit, 非服务端 `Do: merge`), 但**漏了硬约束 2** (双推 + 逐远端核验)。⇒ #136 治的是约束 1 的工具层缺失; 本次暴露约束 2 **同样缺 bump 前守卫**。
3. **并发轨 handoff 里「四仓双远程一致」这句实测不成立** —— 大概核了主仓与 standards/aria 而漏了 aria-orchestrator 的 github。一份已 commit 的 handoff 里的假绿声明, 与本 session 反复栽的「声称 vs 落地」同形。

**我自己第一次修复尝试也失败了, 而且是同一族的坑**: `git push github master` 被拒 —— 因为我在 `feature/m6-cost-model-telemetry` 上工作, 子模块的**本地 `master` ref 陈旧在 `b2484f2`** (memory `feedback_local_main_ref_rots_during_branch_work` 的实时实证), `push <branch>` 推的是那个陈旧本地 ref 而非目标 commit。改推**显式 SHA** `git push github 237045a:refs/heads/master` 才成 (已验 `86bb684` 是 `237045a` 祖先 ⇒ 纯 fast-forward, 无 force)。

> ⚠️ **本 session 内逐远端 `ls-remote` 核验连续抓到两件事**: (a) 并发轨的漏推; (b) **我自己那次失败的修复**。两次 push 的 hint 都很容易一眼滑过。硬约束 2 的价值在这一段是可量化的。

**修复后机械核验**: `overall_parity: true` · `gitlink_integrity` **6/6 全 `ok`** · checks 8/8 · 顺手把子模块陈旧本地 master 追到 `237045a` (仅 update-ref, 未动 feature 分支, HEAD 仍 `92acce5`)。

**Carry**: 约束 2 缺 bump 前守卫 —— 建议与 **#136** 一并处置 (那张已建议「主仓 bump gitlink 前断言被指向 commit 在**每个** enforced remote 上可达」; `gitlink_integrity` 已在**事后**做这件事, 守卫应在**事前**)。

---

## §11 会话收尾 (session-closer, 第二次执行)

> §0-§9 是第一次收尾; owner 随后追加 `[1]`, 故 §10 增量 + 本段为**同一 session 的第二次收尾**。已同批修正 §0/§6 的陈旧态 —— §10 之后它们与正文相反, 正是本 session 反复抓的「同一份文件两处相反」。

### §11.1 机械兜底 (step 0/3)

- **§7 sync**: `[main] master = 036dddf | github=equal origin=equal` —— **warnings 0**。
- **§2 unfinished**: **180** 条, 与第一次收尾同数。
- **§5 consistency**: **10 → 11** flags, 全 `active_change_not_in_upm` (Aria 无 UPM, 恒亮)。

> **⚠️ 一个有信息量的交叉核 —— 本 session 第二次撞 `handoff_autofill` 盲区**: 新 Spec `premerge-gate-mainbranch-failclosed` **被 consistency 看见** (活跃 change +1) 却**没进 unfinished** —— 它是 Level 2 只有 `proposal.md` 无 `tasks.md` checkbox。这正是 aria-plugin **#123** 记的「proposal-inline 任务 (Level 2 proposal-only spec) 报 0 未完成」第三形态盲区。
>
> 第一次撞的是**表格形态** (§1.5, 已由 A.2 转 checkbox 修掉)。⇒ 该 backstop 对**两种非 checkbox 形态**都失明; 而它是 §2 的兜底。**这一 session 两次实证同一个盲区族。**

### §11.2 内省 — 本段待固化 (step 1/2)

```
[候选 memory]
- 「自己开的 issue 也要 probe」—— 本段我把自己开的 #137 订正了两处 (「两条腿都绿」实为只有一条; 漏了 :300 那个缺省), 且订正来自 probe 生产态而非重读 issue。type: feedback (与既有 reporter-miscite 同族但主体是自己)
- 「memory store 是容器本地的」—— 已落 feedback_memory_store_is_container_local_not_shared ✅
- 「修镜像推显式 SHA 而非分支名」—— 已追加进 feedback_local_main_ref_rots_during_branch_work ✅

[未写下经验]
- 「机械兜底自身的盲区要成对记」: handoff_autofill 只数 checkbox ⇒ 表格形态 (已修) 与 Level-2 proposal-only (aria-plugin #123, 未修) 两种形态都失明; 而 CANCELLED 的删除线处置又让「被取消」这个状态在机械层完全不可见 (§2 已记)。三者共同点: **backstop 的可见性单位 (checkbox) 窄于它要兜的情形集** —— 与既有 knob-granularity 同形, 但那条讲豁免开关, 这条讲**可见性单位**。是否值得独立一条待判。
- 「并发轨的 handoff 也可能有假绿声明」: 本段实测「四仓双远程一致」不成立 (§10.5)。⇒ 读并发轨 handoff 时, 其同步状态类声明与自己的一样需要独立核 —— 不因为它是别人写的就更可信。
```

### §11.3 本段 carry (§10.4 之外)

- 🟡 **本容器 5 条 `active` claim** (4 条 2026-08-02 陈旧 + 本段 `premerge-gate-mainbranch-failclosed`)。`--sweep-stale` 扫不掉陈旧的 4 条, 因 `heartbeat_at` 冻结在 acquire (**aria-plugin #107**)。其中 3 条真实状态我不确定, **未猜测性 release**。
- 🟡 **`handoff_autofill` 看不见新 Spec** (§11.1) ⇒ 下段若靠 §2 机械清单判「还剩什么」, 会漏掉 `premerge-gate-mainbranch-failclosed`。已开号 aria-plugin #123, 此处只是又一次实证。

### §11.4 leaf 终结

本段**不调**任何 phase-a/b/c/d / workflow-runner / openspec-archive (session-closer 是 leaf)。检出「有 shipped 未归档 cycle」= 无 (`pending_archive: 0`)。
