# GRADER_CRITIQUE — eval-4 config-awareness

评分结果: `with_skill` 3/3 · `old_skill` 3/3。三条断言在两臂上全部 pass ⇒ **本 eval 的分数对两臂零区分力**。下面是批判本体。

---

## 1. 恒真 / 恒假断言

三条**全部**在本次两臂上恒真, 且不是巧合 —— 它们的触发条件被 prompt 自身包死了:

| 断言 | 为什么近似恒真 |
|------|----------------|
| `Should mention .aria/config.json or config-loader` | 用户原话就是「这个项目有 `.aria/config.json` 配置吗?」。任何**回答了问题**的输出都必然复述这个路径。这条实际测的是「模型有没有答非所问」, 不是 config 感知能力。 |
| `Should describe config fields like auto_proceed or confidence_threshold` | 这两个字段就写在 `state-scanner/SKILL.md:52-58` 的「配置 (config-loader)」表里, 是被测 Skill 文件正文的一部分, 两臂都会照抄。而且本仓 `.aria/config.json` 里两个键都**显式存在**, 从 snapshot 也能读到。 |
| `Should mention default values when config is absent` | 措辞歧义, 两种读法都被满足: (a)「字段缺失时取默认」—— 两臂都做了; (b)「文件不存在时取默认」—— 只有 `old_skill` 明写。按判定标尺「明确证据」两读法都能引到句子, 所以仍是恒真。**这条如果想有区分力, 必须钉死到 (b) 并要求字面「文件不存在 / 缺失则使用默认值」。** |

另有一个断言集层面的缺陷: **三条断言里没有一条要求「默认值取值正确」**。`with_skill` 给了一整列「默认值」并可被证伪 (我实测 `SKILL.md:52-58` 的默认值表 + `collectors/sync.py:53-70` 的 `_multi_remote_enabled_in_config` 默认 `True`, 该列全对); `old_skill` 只给现值不给默认值列。这个**可证伪的差别**当前无人计分。

---

## 2. 断言完全没覆盖的重要差异

### 2.1 ⚠️ 回归信号 (最重要): `old_skill` 把 `parity: unknown` 答成了「所有远程一致」

这是本 eval 里唯一的**事实性错误**, 出在 `old_skill`, 且正落在多远程一致性这条承重机制上。

snapshot ground truth (`.aria/state-snapshot.json` → `sync_status.multi_remote.submodules[aria-orchestrator].remotes[github]`):

```json
{"name":"github","parity":"unknown","remote_head":null,"reason":"no_local_tracking_ref","ahead_count":null,"behind_count":null}
```

- `old_skill` 输出: `✅ aria-orchestrator: 所有远程一致 (origin=github=92acce5)` —— **凭空给 github 补了一个 `92acce5`**, 并把 unknown 判成 ✅ 一致。
- `with_skill` 输出: `❓ aria-orchestrator: origin=92acce5 (equal) | github=unknown` + `原因: no_local_tracking_ref` + `evidence_grade=fresh ⇒ 属 benign unknown` + 补救命令 `git -C aria-orchestrator push -u github <branch>` —— **逐字段对齐 snapshot, 正确**。

严重性: 这正是 CLAUDE.md「多远程推送两条硬约束」和 memory `partial-push` 要防的形状 —— 把「不知道」渲染成「已一致」是**假绿**, 而这个子模块恰好就是当前在飞的 `feature/m6-cost-model-telemetry` 分支。同一份 `old_skill` 输出里 `overall_parity: ✅ true` 是对的 (snapshot 确实 `true`, unknown 不破 parity), 错的只有那一行 per-submodule 判定 —— 这种「总览对、逐条编」的形状比整块错更难被人眼抓到。

### 2.2 `with_skill` 独有: 死配置的**实证**核查 + 处置建议

`with_skill`「注意 1」声称跑了 `grep -rn "sync_check" scripts/**/*.py`, 结论是只命中 `collectors/multi_remote.py` 两行注释、`sync.py` 只读 `state_scanner.multi_remote.enabled`。**我复跑核对: 属实** —— `scripts/collectors/multi_remote.py:161,164` 两行注释, `scripts/collectors/sync.py:54` 读的正是那个键, `scripts/` 树内零实际读取。它还给了处置建议 (清理或标 legacy)。
`old_skill` 得出同一结论 (「这三个键是惰性的」) 但只是断言, 无核查痕迹、无处置建议。
两臂都没被断言问到「配置里有没有死键」—— 而这恰是「config 感知」这个 eval 名义上最该测的能力。

### 2.3 `old_skill` 独有: 两份「配置」的消歧

`old_skill` 明写「注: 这与你问的 `.aria/config.json` 是**两份不同的配置**」并在下方专列一条「**易混淆的两份「配置」** — 上面 🔗 区块报的 `config_status: missing` 指的是 **`CLAUDE.local.md` 里的 forgejo 块**, 不是 `.aria/config.json`」。
`with_skill` 同样输出了那条 Forgejo ⚠️ (还额外确认了 `CLAUDE.local.md` 确实不存在), 但**没有消歧**。在一个「有没有 config?」的提问下, 同屏出现一条 `配置缺失` 警告却不澄清, 是真实的误读风险。**这一条 `with_skill` 更差**, 且断言未覆盖。

### 2.4 其他未覆盖差异 (按重要性)

1. **PRD v2 状态归一**: snapshot `raw_status="Approved (…)"` / `status="pending"`。`old_skill` 两个都给 (`raw="Approved ...", 归一后 pending`); `with_skill` 只给 `(Approved)`, 掩掉了归一分歧。`old_skill` 更忠实。
2. **Phase/Cycle**: UPM `configured=false, current_phase=null`。`old_skill` 从 handoff frontmatter 回落出 `B.2` 并标注来源; `with_skill` 直接给 `—`。`old_skill` 更有用。
3. **`tree_vs_remote=false` 裸字段**: `with_skill` 写 `✅ standards: 同步 (tree_vs_remote=false; workdir 有意 dirty)` —— ✅ 旁边一个 `false` 极易被读反; `old_skill` 写 `tree=remote=cc864ee` 给出 SHA。可读性上 `old_skill` 更好 (两者语义都对)。
4. **issue 选取**: `old_skill` 照 snapshot 顺序列 196/195/193/192/188/176; `with_skill` 把 `Aria#174` 提到首位并标「本轨 linked issue」。#174 标题确实是本 Spec 的同源议题, 相关性更高 —— 但 snapshot 里 `#174.linked_openspec = null`, 「linked issue」这个定性是模型推断而非 snapshot 字段, 措辞上越界了半步。
5. **截断证据**: 两臂都抓到 `limit=20` 顶格 ⇒ 47 是下界 (对)。`old_skill` 额外引「上一 session 实测 snapshot 报 46 / 四仓 API 实拉 65」—— 那是**上次会话的摘要**, 本轮未复测 (memory `past-summary≠measurement` 的形状), 虽然它标了出处。
6. **AB 前置的定性**: 两臂都点了 `ARIA_COORDINATION_NO_PUSH` 会话级前置。`old_skill` 有一句字面「这**不是** Rule #6 豁免, 是执行条件不具备」; `with_skill` 只写「先决条件 (会话级, 会话内补不上)」, 没有那句否定性定性 —— 但补了验收口径 (`"push_skipped": true`, reason `env_var`) 和刷 heartbeat 的**次序陷阱** (跑完 AB → 清理 fetch → 才刷 heartbeat, 否则清理会连真 claim 一起抹掉)。这条 hazard 只有 `with_skill` 说了。

**净判断**: 若只看「事实正确性」这一维, `with_skill` 更好, 差距全部来自 2.1 那一条 (`old_skill` 的伪造 SHA + 假绿)。若看「消歧与可读性」, `old_skill` 在 2.3 / 2.4-1,2,3 上更好。**没有任何一条被当前断言集捕捉到。**

---

## 3. 仓内语料污染 (`openspec/changes/a1-entry-claim-duplicate-work-guard/`)

**两臂都没有出现「读了 change 目录下某文件」的显式路径引用**, 但两臂都复述了源头在该目录的内容。逐条追踪如下 (我对每个可疑串做了全仓 grep 定位其唯一/最近来源):

### 3.1 `old_skill` — 一条串源头在 change 目录, 但存在合法旁路

> `跳过: A.* (Spec 已 approved, post_spec R1–R6 已收敛)`

`post_spec R1–R6` (en-dash) 全仓只出现在 4 处: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:3`、同目录 `detailed-tasks.yaml:38`、`docs/handoff/2026-08-30-…-r6-cleanup-verified.md:17`、`.aria/audit-reports/post_planning-R1-…md:32`。**本轮 handoff (`2026-09-05-2200-…`) 里 `R6` 出现 0 次。**

但**不能据此判定它读了 change 目录**: `proposal.md:3` 那段 Status 原文被 snapshot 整段吞进了 `.aria/state-snapshot.json:2654` 的 `openspec…raw_status` 字段 (含 `post_spec R1–R6 已跑` 逐字)。也就是说 —— **snapshot 本身就是 change 目录语料的搬运通道**, 读 snapshot 就等于读到了 proposal.md 的正文片段。这对 AB 是个结构性问题 (见 3.3)。

另: `old_skill` 写「handoff 记为「R5 4/4 PASS, 全集未稳定致 max_rounds 耗尽」」—— 这是**错误归因**。本轮 handoff 第 166 行只有「上次 `pre_merge` R5 PASS (2026-09-02), `converged=false`」, 既无 `4/4` 也无「全集未稳定致 max_rounds 耗尽」。带引号的转引句在被引文档里不存在。

### 3.2 `with_skill` — 全部可追到 handoff, 一处属性错挂

> `注: 我不自行改序把 7.6 提前 —— tasks.md 写死 dependencies: [TASK-035] (Rule #10)`

`dependencies: [TASK-035]` 这个串**逐字出现在本轮 handoff 第 54 行**: 「yaml `dependencies: [TASK-035]`, tasks.md 行尾也写着「按 Spec 它依赖 7.5 跑完」」。所以来源是 handoff, 不必读 change 目录。但**属性挂错了**: 该 `dependencies` 字段在 `detailed-tasks.yaml` (TASK-036 条目), `tasks.md:102` 只有散文「按 Spec 它依赖 7.5 跑完」。handoff 已经把两者分清, `with_skill` 合并成了「tasks.md 写死 dependencies: [TASK-035]」。

其余全部核对通过、全部来自 handoff, 无 change-目录独有串: `31/40` (handoff:38,176)、`vNEXT = 1.70.0` 与执行序 `8.1 → 8.4 → 8.2` (handoff:55,176)、`TASK-036` / `TASK-038/8.2` (handoff:18,21,54)、六个套件名单逐字 (handoff:53)、验收口径 `"push_skipped": true` / `env_var` (handoff:105)、heartbeat `21:40:06Z` (handoff:195)、在飞轨 `aria-2-0-m6-dispatch-input-delivery` 与 `owner-container-identity-key-and-collision-parser` (handoff:23,126)。

### 3.3 给套件维护者的结论

1. **本 eval 没有干净的「未污染」臂可言。** `.aria/state-snapshot.json` 会把 `openspec/changes/<active>/proposal.md` 的 Status 正文整段带进 `raw_status`, 而 Step 0 强制读 snapshot ⇒ **任何臂都必然接触到 change 目录的文本**, 与它有没有 Read 那个目录无关。判「污染」时必须先扣掉这条通道 (与 memory `ab-baseline-leaks-via-repo-corpus` 已记的两条通道并列, 这是第三条)。
2. **handoff 是更大的等价通道**: 本轮两臂输出里几乎所有 Spec 级细节 (任务号 / 版本号 / 执行序 / 验收口径) 都能在 `docs/handoff/2026-09-05-2200-…md` 里逐字找到, 而读 handoff 是 SKILL 明令动作。若要测「不靠仓内在制语料的 config 感知」, 这个 eval 必须换到一个**没有活跃 Spec + 没有新鲜 handoff** 的 fixture 仓, 否则测的是「照抄 handoff 的能力」。
3. **本 eval 若想留在套件里, 建议改造**: 把三条恒真断言换成可证伪的 —— (a) 默认值取值必须与 `SKILL.md` 配置表逐值一致; (b) 必须区分「`.aria/config.json` 缺失」与「单字段缺失」两种回落; (c) **必须把 `parity: unknown` 渲染成 unknown, 不得渲染成 equal 或补 SHA** (直接把 2.1 那条回归钉成断言 —— 它是本轮唯一有区分力的差异)。
