---
type: owner_decision_sheet
subject: 10CG/Aria#195 与 10CG/Aria#199 的四项待裁 (版本号 / 断言归属 / 10CG/Aria#199 的 minor 时点、21 条执笔请裁与报告落仓 / 心跳 issue 候选) — owner 裁「照建议」
spec_ids: [handoff-multibranch-subdir-path-fidelity, pre-merge-completeness-gate-change-scope]
status: decided
decided_by: owner
decided_at: 2026-09-27
created: 2026-09-27
container: simonfish/bfe8285d
---

# 决策单 — 2026-09-27 四项待裁: owner 裁「照建议」

> **来由**: 2026-09-26 ~ 27 会话收尾时列出四项待 owner 裁定 (`docs/handoff/2026-09-27-session-close-195-task025-legacy-issue-204.md` §3)。owner 要求 AI 给建议; AI 逐项核实事实后给出建议与代价, owner 答「照建议」。本单记录每项的裁定、依据、代价与落地位置, 是这些裁定的权威记录。
> **授权范围**: 「照建议」同时授权本会话内的两类外向动作 —— 第 3c 项落仓的提交与推送、第 4 项的两条评论。其余外向动作 (如第 1 项合并后关闭 `10CG/aria-standards#20` 的回帖) 到执行时按各自计划再请授权。

---

## 1. standards `conventions/session-handoff.md` 的 Version

- **裁定**: 本 cycle 升到 **1.4.0** (MINOR), 一次补齐三次增量 —— `d217ed0` (§2.3.1 / §2.3.5 / §2.3.9) · `21748d4` (§2.3.8.1) · 本 cycle 的 `11b0a14` + `d86fc91` (§2.3「目标不在顶层」第三态)。头部括号按 `10CG/aria-standards#20` 建议的格式逐条列出。并入 `10CG/Aria#195` 的 TASK-027 (版本号任务) 执行, 在 TASK-029 合并 standards 之前提交到 standards feature 分支; 合并后回帖关闭 `10CG/aria-standards#20`。
- **依据**: `10CG/aria-standards#20` 自己建议用一个 1.4.0 补齐前两次; 第三次列进同一个括号, 每次一条, 不掩盖任何一次。本 cycle 的 standards 本就要走「本地合并 + 双推 + 主仓 gitlink 升级」, 单独为 `10CG/aria-standards#20` 再走一遍成本更高。§2.3.5 那次是否算破坏性 (`10CG/aria-standards#20` 留给维护方的 2.0.0 问题): 同一改动在插件侧已按「对采用方是行为变更 ⇒ MINOR」发为 aria v1.70.0 (2026-09-12 决策单 §2 的 `10CG/Aria#195` 表第 6 行引述的 D5 先例), 同判 MINOR。
- **更正**: `10CG/Aria#195` 台账 TASK-023 节「Version 头保持 1.3.0 未 bump」的理由 (「会把三次合并进一个号、掩盖记录的事实」) 不成立, 以本条为准。
- **代价**: `10CG/Aria#195` 多一处计划外改动 (头部一行), 执行时记进 `tasks.md` 的 AI 流程判断清单与台账。

## 2. 四条断言的归属订正 (`10CG/Aria#195`)

- **裁定**: 追认。owner 2026-09-25 裁「路径 A」的实质是走三步法反事实; 四条断言 (SC-6 (c) / SC-18 (c) / SC-15 (e)(h)) 按计划分工归 TASK-015 与 TASK-018, TASK-035 的六个补丁无一对应 (台账「owner 裁定 (2026-09-25): 取路径 A」一节有逐条对照)。
- **代价**: 无。

## 3. `10CG/Aria#199` 的三项

### 3a. R7 六条 minor 与各轮未处置 minor 的处置时点

- **裁定**: **进 Phase B 之前一并处置**, 与 `10CG/Aria#195` 合并后的基线平移合成一次返修 (v2.7)。
- **依据**:
  1. 本轨 B.1 本就要等 `10CG/Aria#195` 完成 C.2; 本轨文件集含 standards `session-handoff.md` (v2.4 补入), `10CG/Aria#195` 已改该文件, aria 也将发新版 ⇒ 基线必然平移, 现在改 minor 会做两遍。
  2. 六条虽为措辞 / 口径级, 其中两条执行时会绊人: TASK-029「前四条首行须为 OK」按字面是全等比较, 而这四个检查通过时首行都带后缀 (R7 `6be9db6a` 的 cr 一半); yaml `owner_gates` 第 14 项少写「强制对齐」(R7 `ce6f31fc`) ⇒ 必须在执行到对应任务之前改掉, 「随 Phase B 首个返修」可能来得太晚。
  3. 只含 minor 的返修不破坏已收敛的结论 (本仓 2026-09-24 修正后的收敛判据), 不重开 post_planning; 若基线平移带出实质改动, 按审计规则走。
- **执行注**: 各轮「未处置」minor 的清单须在返修前按 R2 ~ R7 聚合报告重新对账, 不凭记忆。
- **代价**: 已知 minor 在计划里多挂一段时间 (本轨 B.1 本就被入口门挡住)。

### 3b. 三批执笔请裁 (v2.4 九条 / v2.5 十条 / v2.6 两条, 共 21 条)

原文见 `.aria/notes/2026-09-17-199-a2-a3-tooling/writer-reports/` 各版执笔报告的「请裁项」一节。

| 分类 | 条目 | 处置 |
|---|---|---|
| 已失效, 无需再裁 (5 条) | v2.4 第 2 条 (被 v2.5 的 13a / 13b 拆分取代) · v2.4 第 7 条 (track-id 停点, v2.6 `354faf33` 已闭合) · v2.4 第 9 条 (owner 2026-09-22 已裁) · v2.5 第 9 条 (v2.6 `6ad0a84b` 已改) · v2.6 第 2 条 (状态说明) | 记录即可 |
| 追认 (12 条) | v2.4 第 1、3、4、6、8 条; v2.5 第 1 ~ 6、8 条 | 追认。这些做法经 R5 / R6 / R7 三轮五席审计, 有的被补强过 (如强制对齐在 v2.6 推广到 release), 无一被判方向错。v2.4 第 8 条 (R4-M1 前提的勘正) 在 v2.7 的 `revision_log` 记一行 |
| owner 决定 (3 个, 覆盖 4 条) | 见下 | — |

1. **C.2.4.5 的 override 走哪一路 (v2.6 第 1 条)**: 定 **PR 标签为默认路径**。trailer 路要改写并强推已推送分支, 与 `owner_gates` 第 8 项冲突, 且 C.2.4、本闸与提交范围核验都要重做; 标签路不动提交, API 失败按无标签处理 (挡住, 方向安全)。v2.7 须补写 R7 `3de4b245` 指出的代价 —— 标签不分子模块, 一经打上即对本 PR 所有受影响子模块生效 —— 并要求 owner 授权打标签时逐个子模块点名、记台账。
2. **latest.md 的 History 节是否恢复 (v2.5 第 7 条, 含 v2.4 第 5 条)**: **不在本轨内裁, 交 `10CG/Aria#220`** (该单登记的正是 History 节被整文件重写删掉 88 条、且「不可跳过」无机械核验)。`10CG/Aria#220` 定案前, 本轨 Phase D 沿用现行版式 (track 表本轨行 + 收尾注)。
3. **`no-unresolved-version-placeholder` 检查的漏洞 (v2.5 第 10 条)**: 属实 (2026-09-27 复核: command 为 `! grep … 2>/dev/null`, grep 出错 [如 `aria/` 未检出] 时出错码被 `!` 反转为 0 ⇒ 假绿)。**修, 但不放进本轨** (不在其可写集): 另开 Level 1 小修, 只改主仓 `.aria/state-checks.yaml` 该条 command。**未排期**, 任一会话可做。

### 3c. 执笔报告与三份机器清单落仓

- **裁定**: 立即落仓 —— 三版派单与执笔报告共 6 个文件逐字节原样落到 `.aria/notes/2026-09-17-199-a2-a3-tooling/writer-reports/` 并附来源说明; 各版 `writer-work/` 与 `repo/` 副本 (约 790MB) 不落仓。
- **依据**: 唯一副本在 2026-09-24 会话的 `/tmp` scratch, 该目录树已达 11G, 随时可能被清理; 清掉后 `revision_log` 与轨级 handoff 里的「160 个候选改 46 条」「9 张交互表」「序号引用 342 行」等说法无法复核 (R6 聚合流程记录第 5 条的可审计性缺口)。
- **代价**: 仓内多约 280KB 历史产物, 原样保存, 其中写法按存量对待不回改。

## 4. 心跳的两条插件侧 issue 候选 (2026-09-24 提出)

- **裁定**: 不开新单, 在已有单上补评论。
  - 候选一「入口心跳只认本会话持有的 claim, 新会话不刷继承的 claim」→ 评论 `10CG/aria-plugin#107`。该单写于心跳尚无生产调用路径时; 现已接上 `--heartbeat-only`, 残余缺口是 SKILL.md 的触发条件按会话写。附四次实测与最小修法 (触发条件改为「本容器持有」; `heartbeat_by_track` 本就按容器、归一 track_id、active 三者匹配, 与会话无关)。
  - 候选二「落后的本地协调 ref 上心跳静默失败」→ 即 `10CG/aria-plugin#169` 的机制; 评论补调用方一侧的规避做法 (写前强制对齐 + 推后 `ls-remote` 核验) 作修法方向佐证。
- **代价**: 两条对外评论; `10CG/aria-plugin#107` 的修复仍需排期 (改 SKILL.md 属处方性运行时指令改动, Rule #6 照跑 AB)。

---

## 落地记录 (2026-09-27)

| 项 | 落地 | 核验 |
|---|---|---|
| 3c | 主仓 master `5f48b08` (6 个文件 + 两处 README) | 6 个文件 sha256 与源文件逐一一致; 落仓前凭据形态扫描零命中 |
| 4 | `10CG/aria-plugin#107` 评论 id 26263 · `10CG/aria-plugin#169` 评论 id 26265 (均 2026-09-27T12:33:03Z) | 独立 GET 两条均在且正文与发出的逐字相等; 评论数 0 → 1 / 2 → 3 |
| 1 / 2 | 记入 `10CG/Aria#195` 台账 `4f91772` (feature 分支; owner 同日追加授权后双推, 两端 MATCH); 第 1 项的升版随 TASK-027 执行 | — |
| 3a / 3b | 作为 v2.7 返修的输入 (本轨 B.1 之前) | — |
| 3b 第 3 个决定 | owner 同日追加「Level 1 也顺手做掉」→ 主仓 master `0ed4a31`: 占位符检查按 grep 退出码三分并先断言 `aria/skills` 存在; 同族扫描 16 条 check 另发现 `claude-md-changelog-free` 同类假绿 (CLAUDE.md 不可读仍打印 OK 并退出 0), 一并补可读断言 | 按运行器同一方式在夹具上实测 7 个情形: 三处假绿改前均 pass、改后均 fail, 其余四个情形判定不变; 真仓 custom checks 16/16 pass |

**v2.7 返修须一并处理的新输入 (由上一行引起)**: 本轨计划对 `no-unresolved-version-placeholder` 的描述 (`tasks.md` 3 处 / `detailed-tasks.yaml` 7 处) 按旧行为写成 —— 「以 `!` 反转 grep 退出码并丢弃 stderr」「通过时无输出」「换到别的目录起跑仍无输出且退出 0」, 以及据此加的 `test -d aria/skills` 前置。`0ed4a31` 之后: 通过时首行为 `OK (…)`; `aria/skills` 不存在或 grep 出错一律退出 1 且首行 `UNVERIFIED — …`。TASK-029 custom checks 条的期望首行须改 (该检查从「无输出」变为以 `OK` 开头, 与 R7 `6be9db6a`「首行须为 OK 按字面全等」那条 minor 同批按「以 OK 开头」处理); `test -d` 前置变为冗余但无害, 去留由 v2.7 定。
