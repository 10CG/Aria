---
track-id: a1-entry-claim-duplicate-work-guard
owner-container: simonfish/023236f2
phase: A.1-post-spec-R3-awaiting-owner-direction
status: active
updated-at: 2026-08-25T03:10:00Z
---

# Session Handoff (2026-08-25) — a1-entry rework v3 落版 (方向 b) + post_spec R3 五席联审 REVISE

> **一句话**: owner 2026-08-23 两条裁定全部落版 (换人执笔三席 + 主控逐条核验), 拆出两份 Level 2 子 Spec, 跑完 post_spec **R3 (母) / R1 (两子) 五席联审** —— **REVISE, 3 critical + 19 major, 未收敛**; 12 项机械订正已落, **3 条 critical + ~7 条设计类 major 待 owner 裁方向** (Rule #10: AI 不自行选)。
>
> ⭐ **这段会话最该留下的一件事**: **过半新缺陷是本轮修复动作自身引入的** —— 2/3 的 critical 可直接追溯到「拆 Spec」这个动作与「主控 round-2 的两条指令」。memory `no-ruling-shortens` 说的「拆 Spec 降复杂度是净负」在本轮拿到了第二次实证; `stop-adding-rounds` (major 17→19 不降) 与 `marginal-return-negative` (fix 引入占比接近 1/2) 两条判据同时逼近。

## §0 入口 (新 session 优先读)

- **决策包在这里**: `.aria/audit-reports/post_spec-R3-1787652625000-a1-entry-rework-v3-combined-aggregated.md` §主控处置建议 —— 四个选项 (a) 换新席跑 R4 / (b) 收缩交付面部分回撤方向 b / (c) 直接进 A.2 把 3 critical 转承重任务 / (d) 另裁。**AI 不预选。**
- **claim**: `a1-entry-claim-duplicate-work-guard` (phase A) 本 session 刷新为 `s-6389@0120`, **保持 active**; 对方容器 (`bfe8285d`) 在本 track 上无重叠认领。
- **本地领先 origin 2 commit, 未推** (`027a50f` rework v3 / `13dd8fe` R3 审计+机械订正) —— **推共享 master 须 owner 显式授权** (memory `sync≠push-auth`)。
- **另请 owner 复议两项主控自主流程判断** (Rule #10 留痕): ① 三份 Spec 的「实读清单」切出审计轨; ② 字段 spec 的 `GRANDFATHERED` allowlist 机制。CR 席对二者的判定分别是「**方向对, 执行有缺陷**」与「**机制可接受, 当前落法不可接受**」。

## §1 已完成

1. **并发安全**: 起点 fetch 发现本地落后 3 commit (对方容器) → 核零交集后 ff; R3 前再 fetch 又发现 1 commit → rebase。全程 3 次 fetch, 每次实质动作前一次。
2. **基线换代**: aria `origin/master` 已到 `d50f9c3` (v1.67.1+2), Spec 里的 `cb6bd5d`/`ca52d1c` 全部过期 ⇒ 主控在 `d50f9c3` 上**重跑 42 条事实断言**落成执笔说明书。
3. **一个更简备选被实测证伪并留证**: 「去掉 track-id 的 container 段, 靠 reconcile 同名碰撞 (7c occupied surface) 报警」不成立 —— 7c 受 `_takeover_eligible` 门控, 竞品 claim 超 `STALE_TTL`(30min) 走 7d **零 surface** (= Aria #180); 而 `linked_issue_overlaps` 全函数**不做新鲜度过滤**。⇒ 容器段是把检测从**新鲜度脆弱通道**挪到**新鲜度免疫通道**的承重设计, 已写进 D3 补注。
4. **换人执笔三席并行** (文件域互不相交) + 主控字符级说明书 (42 条实测事实 F-1…F-42 + 裁定 D-A…D-J + SC 编号表 + 8 条硬约束)。三席在第二轮中途撞周限中断, 主控测量磁盘后接手完成剩余机械收尾。
5. **主控跨 Spec 抓到三条接缝** (单席结构性看不见):
   - **SEAM-1**: 母 SC-19 称「(b) 由 SC-2 反向臂承担」**不实** (SC-2 只断言「各含对方」, 无反向臂) → 新起 SC-29, 明标 baseline 即绿的回归守卫;
   - **SEAM-2**: 字段 spec 产 **4** 态 / 探针消费 **3** 态, `BAD_TOKEN` 无归宿 → 探针补逐格映射, 且用反例 (`` `#122, TBD` `` 只走 URL 回落会丢失有效 `#122`) **反驳了主控与字段席共同的建议**, 改取层1∪层2 并集;
   - **SEAM-3**: 探针 §3 层 0 自定义定位规则 = 姊妹 E0 **减去围栏排除**, 与其自称「不得内含第二份抽取实现」矛盾 → 改为逐字采纳姊妹 E0 三谓词。
6. **post_spec R3 五席联审** (combined mode, 一次同时承担母 R3 + 两子 R1)。聚合 `converged: false` / `verdict: REVISE`。
7. **12 项机械订正**已落并复验 (详见 `13dd8fe` commit message)。
8. **两个机械核验器**建成并**先在基线亲跑三态**: `verify_line_refs.py` (逐条实读所有 `文件:行号`) / `verify_structure.py` (23 条硬约束)。终态: 结构 23/23 PASS · 行号 82/82 可实读 · 同一检查器在基线 FAIL 16。

## §2 未完成 / Carry-forward (load-bearing)

- 🔴 **3 条 critical 未修, 待 owner 裁方向**:
  - **C1** C-B 只闭一半 —— `release_claim_by_track` 释放 **ALL matching** ⇒ 方向1收尾**连坐**同 issue 其他在制方向; SC-27 仅两臂抓不到。主控处方 (未落): D.2b 对 **issue 派生形**不得无条件 release, 仅当本容器同 issue 无其他在制 Spec 时才 release; 回落形维持无条件; SC-27 补第三臂。
  - **C2** `GRANDFATHERED` 6 条 Aria 本仓硬编码路径 × **随 plugin 分发**的脚本 ⇒ 采用方注册后陈旧守卫全命中 **exit 1 恒红**。根因 = 主控 round-2 的宿主改判与 allowlist 仓本地性冲突。主控处方 (未落): allowlist 移出脚本 → 仓本地数据, 分发件里零 Aria 路径。
  - **C3** E0–E6 抽取规则**实现无归属** (三约束不可同时满足)。主控处方 (未落): 姊妹把 E0–E6 交付为**可 import 的纯函数** (输入 = 文本 blob 非路径), 探针 import 之 —— 先例是姊妹 Spec `linked-issue-normalization` D9 为同样理由导出 `normalize_linked_issue`。
- 🟠 **约 7 条设计类 major 未修**: M1 (`--heartbeat-only` 已补 `--phase`, 但「放开参数 vs 补文档」的取舍请复议) / M3 (`linked_issue_overlap` null 形态 × Phase B 消费面) / M8 (heartbeat 挂载点在审计轮结构性缺席) / M9 (`--heartbeat-only` 走 `_gated` 会把 `coordination-gate-invocation` 变**恒绿**) / M10 (「形态是否含 slug」无判定式 + 反例 `fix-issue-149-<uuid>`) / M16+M17 (**SC-2 与 SC-7 恒绿** —— 既有测试已绿, 测不出新机制) / M18 (SC-29 fixture 未命中真正新开风险面) / M19 (字段 spec 的「代码」类 SC 无测试宿主 —— **复发它自己要治的 C-A 病根**)。
- 🟡 **两子 Spec 状态**: 仍 `Draft — 待 post_spec R1`; 本轮联审已是其 R1 且判 REVISE ⇒ Status 行需随 owner 裁定一并更新 (未改, 因裁定会改变措辞)。
- 🟡 `aria-orchestrator` gitlink 停泊 (承前, 有意排除)。
- ⏸️ 承前: M6/M7 六 spec 门在 owner/基建; backlog #138/#180/#182/#184。

## §3 关键风险 / 已知陷阱

- **机械核验只证明「该行存在」, 不证明「断言内容属实」** —— CR 席原话「机械核验全过, 内容全错」。本轮 `母 Spec :88` 在任何已提交 SHA 上都不是那行, 而我的核验器全绿。**两层必须都做。**
- **迁出会删掉别人的证据**: 母 Spec 的 §1 迁出使字段 spec 引用的「母 `:88` depth-2 真实实例」悬空。**跨文档引用必须钉到不会被本批次改动的锚点。**
- **「按字节搬」这句话很容易变成不实断言**: 若同一轮里先重生成再搬, 它就只对没重生成的那部分成立。且**未提交过的内容搬迁后结构性不可独立复核**。
- **A.0 是已占用的标签**: `spec-drafter/SKILL.md` 里 `A.0` = state-scanner。新锚点须换 (建议照 `branch-manager/SKILL.md:146` 的 `### 前置: REQUIRE claim` 体例)。
- 对方容器活跃: 本 session 内 master 前进 2 次 (`cc1bdef` → `2ae012f`), 且其 `2ae012f` 给 `.aria/state-checks.yaml` 加了第 11 条 check, 当场使字段 spec 的「10 条」断言过期 —— **语料/配置是自修改的, 数字只能当日期观测**。

## §4 实战教训 (memory 沉淀来源)

```
[候选 memory]
- (新) 「拆 Spec 会制造新的接缝型缺陷」: 本轮 3 个 critical 里 2 个由拆分动作与协调指令引入;
  拆分后跨文件引用会因另一侧的迁出而悬空。与 no-ruling-shortens 同族, 但补的是「拆的代价具体长什么样」
- (追记 feedback_completion_signals_vs_runtime_invocation): 「文档里写了一条 CLI 形态」≠「那条命令能跑」
  —— --heartbeat-only 三处形态全缺 required 的 --phase, 三轮审计+两轮核验都没人真跑一遍
- (追记 feedback_own_past_summary_is_not_a_measurement): 主控 round-2 引 phase-b-developer:88 作先例,
  实读是布尔谓词不携带 track_id ——「我读过那行」与「那行讲的是这件事」是两回事
[未写下]
- combined-mode 联审在本轮的实证: 3 critical 里 2 个跨 Spec, 单 Spec 审必漏 (已有 memory, 本轮第 2 次实证, 不新写)
```

## §5 多维度同步状态

| 维 | 状态 |
|---|---|
| OpenSpec | 活跃 **9** (本轮 +2 子 Spec); a1-entry 待 owner 裁; pending_archive 0 |
| 审计 | post_spec R3 combined **REVISE 3C/19M**, `converged: false`; max_rounds=5 ⇒ 字面还剩 R4/R5 |
| 版本 | 无变动 (纯 Spec 轮) — 插件 v1.67.1 / 主项目 v1.7.5 (对方本 session 修正) |
| custom checks | 11 条 (对方 `2ae012f` 新增第 11) |
| git | 本地 `13dd8fe` 领先 origin/github **2 commit**, **未推** (待 owner 授权) |

## §6 Next session 入口 + 优先级建议

入口: `/aria:state-scanner`。**第一件事 = 读聚合报告的「主控处置建议」并请 owner 裁 (a)/(b)/(c)/(d)**。
裁定后: (a) → 主控先清 12 项机械项余项再换新席 R4; (b) → 收缩交付面, 两子 Spec 转 issue; (c) → A.2 任务拆解, 3 条 critical 转承重任务。
顺带: owner 授权后推 2 commit; 两子 Spec 的 Status 行随裁定更新。

**结构化 carry-id (§2.3.8 schema)**:
- `{id: a1-entry-claim-duplicate-work-guard, desc: "post_spec R3 REVISE 3C/19M, 待 owner 裁方向 (a)/(b)/(c)/(d)"}`

## §7 提交清单

```
[main master] 2ae012f (对方, 版本 SOT) → 027a50f (rework v3: 母改 + 两子新建 + 3 审计轨)
              → 13dd8fe (R3 五席报告 + 聚合 + 12 项机械订正)
              ⚠️ 两条均**未推** — 待 owner 授权 (memory sync≠push-auth)
[coord ref]   claims/023236f2/s-6389@0120 (a1-entry, phase A) → active 保持
[aria 子模块] 未改; 工作树 58a49e7 (= gitlink), 实读基线用 d50f9c3 对象
[aria-orchestrator] 停泊 (承前, 有意排除)
```

## Cross-references

- 聚合: `.aria/audit-reports/post_spec-R3-1787652625000-a1-entry-rework-v3-combined-aggregated.md`
- 五席: 同前缀 `-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md`
- 三份 Spec: `openspec/changes/{a1-entry-claim-duplicate-work-guard,linked-issue-field-availability,sibling-spec-probe}/proposal.md`
- 三份审计轨: `.aria/audit-reports/{a1-entry-claim,linked-issue-field-availability,sibling-spec-probe}-audit-trail.md`
- 上一 session: [2026-08-23-session-close-v1.67.1-batch-and-a1-entry-r2-direction-b.md](./2026-08-23-session-close-v1.67.1-batch-and-a1-entry-r2-direction-b.md)
