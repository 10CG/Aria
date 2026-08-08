---
track-id: linked-issue-normalization
owner-container: aria-runner-bot/023236f2
phase: session-close
status: done
updated-at: 2026-08-08T00:00:00Z
---

# Session Handoff (2026-08-08) — `linked-issue-normalization`: R1-fix 从未落地 → 三轮 post_spec → Q7 假说证伪 → 结构性切开

> 会话维度增量。承接 [2026-08-04 双 Spec R1-fix handoff](./2026-08-04-issue122-collision-to-dual-spec-r1fix.md)。
>
> **本段主线 = 一条「审计越用力, 缺陷越多 → 发现病根不在质量而在结构 → 切开」的完整链。** 最有价值的产出不是那份 Spec, 是**拐点的量化证据**: 三轮 major `~14 → ~11 → 26`, 其中「由本轮 fix 引入」占比 `— → 10/11 → 22/26`, 而第三轮恰恰是唯一用上了 owner 缩范围裁定 + 三件专门造的工具的一轮。

## §0 入口 (新 session 优先读)

- **当前态**: 主仓 `2e3d4dc`, **ahead 1 未推** (见 §7)。工作区仅 `aria-orchestrator` (一贯排除)。
- **`linked-issue-normalization` 已切开**: `proposal.md` **473 → 275 行** (纯交付面) + 新建 [审计轨](../../.aria/audit-reports/linked-issue-normalization-audit-trail.md) 274 行 (append-only, 显式不同步) + 新建 `tasks.md` (升 Level 3)。
- **post_spec 三轮均 5/5 REVISE**, 但**算法本体三轮 × 五席逐条实测零偏差** —— 缺陷全在证据层与一致性层。
- **与母 Spec 无未决协调项** (最后一条 `include_terminal` 归属 owner 2026-08-08 已裁并落)。
- **下一步**: 见 §6。

## §1 已完成 (本段)

1. **发现 R1-fix 对 `linked-issue-normalization` 从未落地** —— 编辑清单 17 条 FIX, `ca4db78` 实际只落 **1 条** (`+8/−1`, 单 hunk)。对照组: 同 commit 给 `a1-entry-claim` 落了 `+68/−6`。**是 handoff 的「均已 R1-fix」把「产出编辑清单」当成了「fix 已落」。**
2. **补落 16 条** + owner 裁 **U-1…U-6** 六项 (U-2 rule6_note 方案 A / U-3 fixture 口径走 JSON Lines / U-5 分族第三条路 / U-6 行值分离)。
3. **SC baseline 实跑留证闭环** (`.aria/repro/sc-baseline-*.py`) —— owner `db2e983` 要求的「substitute 须实证而非声称」在 A.1 阶段即满足。
4. **post_spec 三轮 × 5 席全额**: R1′ (新基线, 5C/~14M) → R2′ (1C/~11M) → R3′ (2C/26M)。三份聚合报告落 `.aria/audit-reports/post_spec-R{1,2,3}prime-*`。
5. **owner 七项决策单** (`.aria/decisions/2026-08-06-*-owner-decision-sheet.md`) —— Q1 D2 半幅成文已知限 / Q2 导出归一 / Q4 两层解主辅定位 / Q5 `SKILL.md:176` 照跑 AB / Q6 缩范围 / Q7 三件工具全做。
6. **三件工具落盘**: `spec-consistency-check.py` (8 项 fail-closed) · `mutation-sweep-*.py` (11 维度) · `sc-baseline-*.py` (三重 fail-closed)。
7. **结构性切开** (owner 2026-08-07 采纳) —— 见 §3。
8. **关闭与母 Spec 的最后一条协调项** (owner 2026-08-08)。

## §2 未完成 / Carry-forward

**AI 内省 (load-bearing)**:

- 🔴🔴 **凭据轮换 —— hard cap `2026-08-02` 已逾期 6 天**。`FORGEJO_TOKEN` / `NEXUS_API_TOKEN` / `CF_ACCESS_CLIENT_SECRET`。**本 session 每次汇报都 surface, owner 始终未动。唯一过期不可补救且 AI 完全无法代劳的项。**
- 🔴 **`2e3d4dc` 未推** (ahead 1 vs 双远端)。本 session 前几次推送均经 owner 显式授权, 这一次收尾时未再问。
- 🟡 **silknode waiver 已过期** (`expires_at 2026-08-05`), custom checks **8/8 → 7/8**。并发轨已开了一份决策输入文档 (`0a837ad`) 但**未做决定**。
- 🟡 **terminal 语义分歧仍无 issue 号** —— `reconcile.py:57-58` 的 `"yielded" is NOT terminal` 与 `claim_lifecycle.py:317` 正面冲突, 3 个取值散在 9 个站点。**R1′/R2′/R3′ 三轮各点名一次, 至今无号。**
- **R3′ 的 2C/26M/27m 按约定不逐条修** —— 两条 critical 已在切分时修掉; 其余作为已知限留在审计轨。**继续修就是重演拐点后的循环** (见 §4)。
- **A.2 未跑**: `tasks.md` 是 R3′ 的 C1 手术产物 (给 Q5 的 AB 任务一个家), **不是 A.2 的产出**。是否跑 `post_planning` 闸门待定。
- **母 Spec `a1-entry-claim-duplicate-work-guard` 仍停在 Draft v2**, 两个阻塞项 (C1 `allowed-tools` / C2 heartbeat 触发点) 未裁。

**机械补漏 (backstop)**: `handoff_autofill` 的 unfinished **159 条全部来自 M6/M7 六个 spec 的 tasks.md, 本段零碰**。consistency 10 flags 全是 `active_change_not_in_upm` —— Aria 无 UPM, **恒亮**, 非本段引入 (活跃 change 9 → 10, 新增的是并发轨的 `secret-guard-per-segment-evaluation`)。

> **⚠️ 机械补漏本身的一个盲区 (本段新发现)**: 我新建的 `tasks.md` 用**表格**而非 `- [ ]` checkbox ⇒ **`handoff_autofill` 完全看不见它**, 159 条里一条都没有本 Spec 的。⇒ 该 backstop 对非 checkbox 形态的 tasks 是失明的。**下一个用表格写 tasks.md 的人会得到一个静默的空 unfinished。**

## §3 结构性切开 (本段最重的产出)

**诊断**: 该文档在同时服务两个**不相容**的目的 —— (a) 规定要建什么 (应稳定收敛); (b) 记录规定怎么来的 (天然 **append-only 且自指**)。**是 (b) 的 append-only 性质在制造耦合**: 每次编辑要同步十几处计数与交叉引用, 而它们指向的是「上一轮说了什么」——一个只会变长的东西。

**关键判据 —— 不是「太大所以重写」**: 要重写的那部分 (交付面) 恰恰是**唯一被三轮验证过是对的**那部分。**大和坏不在同一个地方。**

| | 切分前 | 切分后 |
|---|---|---|
| `proposal.md` | 473 行 (交付面 53% / 审计装置 46%) | **275 行**, 纯交付面 |
| 审计轨 | — | **274 行**, append-only |
| `tasks.md` | 不存在 (Level 2) | **新建** (升 Level 3) |

**切法**: **机械搬运不重写** (手打就是重写) + 逐行覆盖核验零静默丢失 + 三件工具对结果实跑。审计轨顶部写死四条: append-only · 不维护与 Spec 一致性 · 不一致以 Spec 为准 · 不受一致性检查器约束。**切完不再逐条修饰** (已知残留一处: 检查器 C8 输出重复一行, 成文不修)。

**切分时修掉的两条 critical**:
- **rule6_note 同一小节两个相反结论, 先读到的是错的那个** (主段落 substitute vs Q5 框照跑 AB) —— 我只给 `<details>` 加了删除线, 没动主段落的结论句。⇒ 主段落换成**按 hunk 两路表**; **并升 Level 3 建 tasks.md** (Q5 亲裁要求「进 tasks.md」而当时无该产物 —— owner 裁定的唯一落地载体不存在)。
- **SC-9 恢复** —— Q1 拿掉「自己那一侧」后, 「回显对方原串」从两个缓解之一升为**唯一缓解**, 而我同批把 SC-9 移出、理由写「配对对象消失」。**因果反了。**

## §4 关键风险 / 已知陷阱

1. **加轮的边际产出会转负, 且手段越强越快到拐点。** 三轮 major `~14 → ~11 → 26`, fix 引入占比 `— → 10/11 → 22/26`。R3′ 是唯一用上 owner 缩范围 + 三件工具的一轮。**每一件新手段都是新表面, 新表面的缺陷密度与老表面一样。**
2. **三件工具每件都复刻了它要治的病**: 检查器 C1/C3/C4 有与 C8 相同的空真洞 (表格格式一漂即输出「✅ SC 表 0 条」) · 变异 sweep 的「11 个维度」只枚举了 `normalize()` **函数内部**旗标 (函数外的回落分支零覆盖, 3 个变异体全存活) · 全称句 sweep **在同一次编辑里新造了一个全称句**。⇒ 三件工具的定位已降为**「便宜的辅助」不是「机械闸门」**, 已知洞成文写进 `tasks.md` 的「Phase B 开工前必读」而**不修**。
3. **承重实证必须与结论同源落盘**: 「47,211 候选串零差异」在仓里只是一行注释 —— 而它是两条条款**永久不写 SC** 的唯一依据, 且写在批评「声称已跑而不可复核」的段落下方几十行。**结论本身对** (两席各自用 100,633 / 44,069+273,430 对独立复现), 错的是留证方式。
4. **给 owner 的成本估算必须实测校准**: Q6 我报「466 → ~250 行 / 未审表面 16 → ~8 项」, 实得 **472 行 / 14 项** —— 两个指标都差约 2 倍, 且当时 Spec 里没有一处记录这个落差。**owner 裁 Q6 的唯一理由就是缩小审计面。** (真正的缩减由 2026-08-07 的切分实现。)
5. **并发轨两次撞车**, 均文件级零重叠, rebase 通过。**且 rebase 后必须重跑工件** (不能只信 rebase 的 exit code) —— 本段两次都重跑了。
6. **CF 隧道断了一整段**: `ssh-forgejo.10cg.pub` 的 `websocket: bad handshake` + HTTPS `530`。判据是 `forgejo GET /version` 走内网仍通 ⇒ **不是凭据问题, 是隧道到源站断**。走内网 `192.168.69.200:3000` 补推 (wrapper 自己的 fallback 路径, **无 TLS 降级**)。曾一度打 80 端口被重定向到 HTTPS 报证书错 —— 是端口错不是新问题。

## §5 多维度同步状态 (机械核验)

- **git**: 主仓 `2e3d4dc` (**ahead 1, 未推**); `aria` `af87cae`; `standards` `2111c84`; `aria-orchestrator` `92acce5` (feature 分支, 只读未动)。
- **custom checks**: **7/8** —— `silknode-contract-deferral-expiry` 已 EXPIRED (`0d over`), 非本段引入。
- **openspec**: 活跃 **10** (本段 `linked-issue-normalization` 切开并升 Level 3; 并发轨新增 `secret-guard-per-segment-evaluation`)。
- **四维 consistency**: 10 flags 全 `active_change_not_in_upm` (Aria 无 UPM, 恒亮)。
- **本 Spec 的验证面**: 一致性检查器 8/8 · 穷举变异 11/11 维度 · baseline 16/16 · pytest `6 passed`。

## §6 Next session 入口 + 优先级

1. 🔴🔴 **凭据轮换 —— 逾期 6 天**。owner 亲自操作, AI 无法代劳。
2. 🔴 **推 `2e3d4dc`** (ahead 1 双远端)。
3. 🟡 **silknode waiver 决定** —— 并发轨已备好决策输入 (`0a837ad`), 三条路: 关闭豁免 / 续期 / 升级为 `standards/governance/`。
4. 🟡 **terminal 语义分歧开 issue** —— 三轮点名至今无号。
5. **`linked-issue-normalization` 可进 A.2** —— 三轮买来的确定性完整保留在 275 行里。是否跑 post_planning 闸门待定; 若跑, **建议先读 §4.1 再决定值不值**。
6. **不要再对该 Spec 逐条修 R3′ 的 24 条残留** —— 那是拐点后的循环 (见 §4.1 与 memory)。

## §7 同步状态 (autofill 机械汇编)

```
[main]              master = 2e3d4dc | github=ahead(1) origin=ahead(1)   ⚠️ 需 push
[standards]         (detached) = 2111c84
[aria]              (detached) = af87cae
[aria-orchestrator] feature/m6-cost-model-telemetry = 92acce5 | origin=equal
```

**warnings: 1** —— `[main] ahead 1 vs 双远端`。**本段所有已推 commit 均双推 + `ls-remote` 独立核验** (CF 隧道断期间走内网路径, 逐个核验 SHA)。

## §8 Memory entries this session

**新增 3 条** (均经查重, 与既有 memory 形状不同):

- `feedback_audit_marginal_return_goes_negative` — 多轮审计边际产出**转负**且手段越强越快到拐点; 判据不是 major 是否降而是「**本轮 fix 引入的 major 占比**」>1/2。扩展 [[feedback_stop_adding_rounds_when_major_count_flattens]] (那条讲「持平=不收敛」, 本条讲「**缓降也可能已过拐点**, 成分才是信号」)。
- `feedback_fix_the_class_not_the_instance` — 修实例必问「这形状还有几个兄弟位置」; 一 session 四次实证。与 [[feedback_fix_recurs_in_its_own_fallback_path]] 不同形状 (那条讲「在自己新写的兜底路径重犯」, 本条讲「**兄弟位置未扫**」)。
- `feedback_audit_trail_must_not_live_in_spec` — append-only 审计叙事与收敛型交付面**不能同居一文**; 处方是**切开不重写** + 顶部四条不同步声明 + 切完不再修饰。

**已有覆盖未重复落**: 声称 vs 落盘 ([[feedback_scoped_git_add_splits_claim_from_landing]], 本段第四次实证 —— R1-fix 从未落地) · 并发撞车 ([[feedback_concurrent_duplicate_audit_fetch_before_start]], 本段两次) · 多簇 fix 互相拆台 ([[feedback_fixes_contradict_each_other_across_clusters]], Q1×Q6 的 SC-9 因果倒置是新实例)。

## §9 流程判断留痕 (Rule #10, 请复议)

- **闸门全程未自行豁免**。post_spec 三轮各 5 席全额, **席位数从未自行下调**; R2′/R3′ 均与上轮同席位同镜头以保证口径可比 (换席位=换口径, 这条是我拒绝把 R1′ 叫 R2 的同一理由)。
- **R1′ 标为「新基线」而非 R2 是 AI 判断** —— 依据是 R1 审的 166 行与本轮 ~370 行口径不可比。请复议。
- **C3 (U-5 分族规则) 的修法三选一由我选** (撤回机械化 + 承重解耦), 已在 commit 说明理由。**但 R3′ 指出: 我撤回的是 owner 裁定 U-5 的一部分, 只写在 commit message 里, Spec 的复议入口没有这条 —— 且本段专门开了 7 条决策单却无一条是它。这是一次干净的送达机会而没送。请复议。**
- **Q5 的落法我改了一步**: owner 裁「照跑 AB」而 AB 当时跑不了 (hunk 是 Phase B 交付物) ⇒ 我改成「Phase B 照跑 + 升 Level 3 建 tasks.md 承载」。请复议。
- **三件工具的已知洞「成文不修」是 AI 判断** (依据是本段观测到的拐点规律)。请复议。
- **R3′ 的 24 条残留不逐条修**是 AI 判断, 同上。
- **推送均在 owner 明确授权后执行**; `2e3d4dc` 未推正是因为收尾时未再问。

## Cross-references

- 前一段: [2026-08-04 双 Spec R1-fix](./2026-08-04-issue122-collision-to-dual-spec-r1fix.md)
- Spec: `openspec/changes/linked-issue-normalization/{proposal.md,tasks.md}`
- **审计轨** (本段新建): `.aria/audit-reports/linked-issue-normalization-audit-trail.md`
- 三轮聚合报告: `.aria/audit-reports/post_spec-R{1,2,3}prime-*-aggregated.md`
- owner 决策单: `.aria/decisions/2026-08-06-linked-issue-normalization-owner-decision-sheet.md`
- 三件工具: `.aria/repro/{spec-consistency-check,mutation-sweep-linked-issue-normalization,sc-baseline-linked-issue-normalization}.py`
