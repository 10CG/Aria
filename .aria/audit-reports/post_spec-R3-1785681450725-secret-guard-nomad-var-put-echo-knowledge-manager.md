---
verdict: REVISE
agent: knowledge-manager
round: R3
critical_count: 0
major_count: 4
minor_count: 1
r2_resolved: 0/1
---

# post_spec R3 审计报告 — secret-guard-nomad-var-put-echo (knowledge-manager 视角, convergence 终验)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md`（owner 裁定缩到最小范围后的版本；审计过程中该文件被再次实时编辑，本报告以最终读取到的版本为准，对应当前 §Why/§What/§Impact/§Tasks 全文）。

**方法**: 全文重读 + 逐条对照 `/home/dev/Aria/CLAUDE.md`（版本管理/多远程推送两条硬约束）+ `standards/conventions/{secret-hygiene.md,version-management.md,changelog-format.md}` + `aria/hooks/secret-guard.sh` 真实源码；对 secret-hygiene.md 提及的新旧 jq 写法用真实 `secret-guard.sh`（通过 stdin JSON payload 直调，避开本会话自身 Bash 工具的 PreToolUse 拦截）实测 exit code；`git status`/`git diff`/`git blame`/`git log` 核对 standards 与 aria 两个子模块工作树真实状态；`git show HEAD:...` 取订正前基线做计数比对。

## 一、缩范围后的模板/一致性终检

- Level/Status/Created/Issue/审计轨迹 五个头部字段齐全，`Created: 2026-08-02` 格式合规，章节顺序（Why → What → 关键决策 → Impact → 转出 → rule6_note → Tasks → Success Criteria）与 R2 已核对的项目既有惯例一致，未见结构性偏离。Rule #5（spec 位置）满足：proposal 位于 `openspec/changes/secret-guard-nomad-var-put-echo/`，未误放 `standards/openspec/changes/`。
- **rule6_note 论证**: 缩范围后「提示文案不改」使得 rule6_note 唯一灰区（hook 文案是否算 AI 指令面）确实不复存在，论证比 R2 版本更干净；「跨仓核实: 本 cycle 零 SKILL.md 改动」这句话覆盖面足够宽，能同时兜住 aria(hook) 与 standards(SOT 文档) 两个子模块的改动对象，逻辑仍然严密，未发现新缺口。

## 二、Major 发现（4 条，均可复现验证，构成本轮 REVISE 依据）

### Major-1 — Task 1.3 / Impact 未跟上 Why/Key Deliverables 刚完成的"3→4 处"订正，spec 内部自相矛盾

`§Why › 附带修复`（L65）与 `§What › Key Deliverables`（L61）已订正为准确的「**4 个推荐位**」（§1 Verification 定义行 / §3.3 python / §3.4 bash / 附录「正确替代」句），但：
- **Tasks 1.3**（L120）仍写「`secret-hygiene.md` §3.3/§3.4 **三处** `-out=keys` 订正」——只点了 2 个位置，遗漏 §1 与附录句；
- **Impact**（L93）仍写「`secret-hygiene.md` **3 处**示例」——同一处滞后的第二证据。

这不是风格问题：Tasks 是执行清单，Impact 是发布记录，两者若与 Why 的事实认定不一致，未来按 Tasks 字面执行或按 Impact 复核发布范围的人会依据错误数字工作。经我用 `git diff -- conventions/secret-hygiene.md` 核对 standards 子模块工作树，**实际编辑已正确覆盖 4/4 处**（§1 L39 / §3.3 / §3.4 / 附录句均已改），说明"4 处"是事实层面正确的数字——问题纯粹是 proposal 文本内部未同步，Tasks/Impact 两处仍停留在旧的"3 处"表述。

### Major-2 — "§4.3" 引用编号错误，应为 §4.4

`§Why › 附带修复`（L65）与 `§What › Key Deliverables`（L61）两处都把"正确替代"句所在小节称为 **§4.3**。经对 `standards/conventions/secret-hygiene.md` 实际标题编号核对（`grep -n "^### "` 结果）：

```
### 4.3 Bash — 默认 stdio        ← 与 -out=keys 无关的另一条反例
### 4.4 Round-trip 验证          ← "正确替代: 用 `nomad var get -out=keys` 检查 key 存在..." 一句实际所在
```

`§4.3` 是完全不同的一段内容（不含 `-out=keys`），proposal 引用编号有误，会误导执行者/复核者去错的小节核对。

### Major-3 — secret-hygiene.md 自身 `Version` header / §10 版本历史表未纳入本次订正范围（R2 已提，现证据升级为 Major）

R2 knowledge-manager 曾以 Minor 提出该文件自身 `Version: 1.1.0` header + §10 版本历史表的既定记录习惯未被 Task 1.3 覆盖，判定"非阻断"。本轮补充核实项目**实际惯例**：`git log -p -- conventions/secret-hygiene.md` 显示最近一次相关提交（`0c6e6c2`）里，secret-hygiene.md 只是被**捎带加了一条交叉引用**（非本次改动的主要对象），其自身 `Version` header 确实**未**跟着 bump（仍 1.1.0）；而当次改动的**主要对象**文件 `nomad-docker-registry-auth.md` 则同步做了 `v2.0.0 → v2.1.0`。

本次订正中，secret-hygiene.md **正是主要对象**（不是捎带旁引用）——Task 1.3 的全部工作量都发生在这个文件内。按项目自己刚示范过的惯例（主要对象 bump，旁引用不 bump），本次理应把 `Version: 1.1.0 → 1.1.1`（纯 Patch：`version-management.md` §2.3「文档错误修正」）并在 §10 版本历史表补一行，但当前 Task 1.3 未提及。鉴于这是不可协商 Rule #7 的 SOT 文档、且证据已从"仅次于既定习惯"升级为"有本仓库最近一次同类操作的直接反例先例"，本轮判定升级为 Major（仍非阻断发布，但应在合入前补齐，否则该文档自身的版本审计线索出现空洞）。

### Major-4 — SC-6 测的字符串与 SOT 实际新推荐的字符串不一致，验收标准未覆盖真实交付物

SC-6（L131）写「`nomad var get -out=json <p> | jq 'keys'` 仍 exit=0（既有 jq credit, **亦即 SOT 订正后推荐写法的可行性验证**）」。但 standards 子模块工作树里 secret-hygiene.md 实际订正后的推荐写法是 **`jq '.Items | keys'`**（带 `.Items` 前缀），不是裸 `jq 'keys'`——两者是不同的 jq 表达式字符串。SC-6 的字面表述把"验证了 `jq 'keys'`"直接等同于"验证了 SOT 的新写法"，这个等价并不成立，是验收标准与真实交付物脱节。

我用真实 `secret-guard.sh`（`CLAUDE_PLUGIN_ROOT=/home/dev/Aria/aria`，JSON payload 直调，规避本会话自身 Bash 工具被同一 hook 拦截）逐条实测：

```
exit=0  nomad var get -out=json nomad/jobs/myapp | jq '.Items | keys'
exit=0  nomad var get -out=json nomad/jobs/myapp | jq 'keys'
exit=2  nomad var get -out=json nomad/jobs/myapp | jq '.Items'
exit=2  nomad var get -out=json nomad/jobs/myapp | jq '.Items | keys[]'   # 方括号确会破坏识别，与 proposal L77 断言一致
```

结论层面 `.Items | keys` 确实被放行，proposal L77 的断言是**对**的；但这个"对"是我额外实测出来的，SC 清单本身没有一条显式锁定这个确切字符串——SC-6 应改为直接测 `jq '.Items | keys'`（可保留 `jq 'keys'` 作对照，但不能用后者代替前者作为"SOT 推荐写法的可行性验证"）。否则将来 secret-guard.sh 的 jq 白名单正则被改动时，回归套件测的是 SC-6 写的旧字符串，测不出 SOT 文档里真正在用的那个字符串失效。

## 三、跨仓变更面（对照 CLAUDE.md 版本管理 + 多远程推送两条硬约束）

- Impact「ship 同步面: aria 子模块 5 文件 + standards 子模块 1 文件 + 主仓双 gitlink + VERSION + README badge (i18n B 档)」与 CLAUDE.md 版本管理段逐项对得上，"双 gitlink"是对基线描述的合理扩展（aria + standards 各一次 gitlink bump），非冲突，R2 已核，本轮复核仍成立。
- standards 子模块本身**没有仓级 VERSION/CHANGELOG**（`find . -iname "CHANGELOG*" -o -iname "VERSION*"` 只命中 `conventions/version-management.md` 与 `conventions/changelog-format.md` 两篇规范文档本身，无仓根 VERSION 文件）；standards 的版本颗粒度是**逐文档 `Version:` header + 文档内 §版本历史表**，不是仓级发布版本。因此"standards 子模块是否需要独立版本/CHANGELOG 处理"这一问题的答案是：**不需要仓级机制，但需要文档级机制**——即 Major-3 指出的 secret-hygiene.md 自身 header/历史表，这是 standards 唯一适用的版本颗粒度，目前未被覆盖。
- 多远程推送两条硬约束（子模块合并本地做 + 推后逐个 `ls-remote` 核验）属于 phase-c-integrator 执行层规程，Level 2 Minimal proposal 不需要在文档里复述，Task 1.5/1.4 未提及不算缺陷。

## 四、SOT 订正的规范面

- 本次订正内容是纯事实性勘误（CLI flag 取值域），未触及 Rule #7 核心条款本体（"不读 secret value 字面, 用 metadata 验证"不变，只是把不可执行的示例换成可执行的），不需要在 Level 2 之上叠加额外流程；proposal 已用「owner 裁定本 session 修」显式记录了裁定人与裁定时点，满足 Rule #10 意义上的可追溯性（这是 owner 决策，非 AI 自行豁免）。
- **订正后 §3.3/§3.4/附录 与 hook 的 Acceptable filters 清单是否会保持一致**: 功能上一致（已实测 `.Items | keys` 被放行），但 `aria/hooks/secret-guard.sh:662-664` 的 BLOCKED 提示文本自身只展示 `jq 'keys'` 一例，不含 `.Items | keys`；`§What` 已经过论证明确决定"提示文案不改"（避免全局 heredoc 被 nomad 专属内容污染），这是一个**已充分披露、有权衡依据的既定决策**，不构成本轮新增缺陷——但也是「以后可能再次分裂」的真实风险点，proposal 自己也没有回避这点（转出项 5 与"提示文案不改"决策行都间接承认了这个权衡）。此处判定：不新增 finding，维持已有决策记录。

## 五、owner 裁定留痕质量

两处 owner 裁定（"缩范围" L27 标题内联 + L36-38 论证段；"顺带修 SOT" L63 标题内联 + 关键决策表一行）都清楚标注了**谁**（owner）、**何时**（2026-08-02）、**为什么**（R1/R2 两版豁免设计均被实测推翻 + 结构性前提超出 Level 2 / SOT 教了跑不通的命令、与 #170 事故链同构）、**转出了什么**（§转出 五项，逐项有 tag+severity+repro）。这个记录密度足以支撑未来复议——**唯一需要留意的留痕缺口**见下方 Minor-1（工作树已有未提交实现，但 spec 状态仍写"待 R3"）。

## 六、Minor 发现

### Minor-1 — standards 子模块工作树已有对生产文件的未提交编辑，早于 spec 状态标注的"待 R3"节点

`git -C standards status --short` 显示 `M conventions/secret-hygiene.md`（未 commit、未 push）。经 diff 核对，这份未提交编辑内容与 Task 1.3 的目标高度吻合，且经我实测其中的 jq 新写法确实被 secret-guard.sh 放行（见 Major-4 的实测数据）——**内容本身是对的**。但 proposal 头部仍写 `Status: Draft (post_spec R1+R2 后 owner 裁定缩范围, 待 R3)`，按十步循环 Phase A 尚未收尾（R3 是本轮才做）。这大概率是起草者在撰写"附带修复"段落时的验证性草稿（未落盘提交），而非误跳 Phase 顺序，但建议在本轮结论或后续 handoff 里显式确认这一点，避免"Draft 阶段生产文件已被动过"这一事实缺乏留痕、日后复议时说不清是谁在什么阶段做的。**非阻断**，建议 Phase B 正式开始时把这份工作树编辑当作起点核对后再提交，而不是重新写一遍。

## 结论

0 Critical；4 Major（均为可核实、可复现的文档内部一致性/引用/验收覆盖缺口，集中在"缩范围+追加 SOT 订正"这次编辑动作本身留下的尾巴，不是架构级问题）；1 Minor（工作树留痕建议）。R2 遗留的 1 条 minor（secret-hygiene.md 自身版本号）本轮**未解决**，且经新证据（项目自身先例 `0c6e6c2`）升级为 Major-3。

**verdict: REVISE** — 建议收敛动作：(1) Tasks 1.3 / Impact 的"三处"→"4 处"同步；(2) "§4.3"→"§4.4"引用订正；(3) Task 1.3 显式加入 secret-hygiene.md 自身 `Version` header (1.1.0→1.1.1) + §10 历史表一行；(4) SC-6 改为直接锁定 `jq '.Items | keys'` 字符串（可保留 `jq 'keys'` 做对照，不作等价替代）。四项均为局部文本级修订，不涉及范围/架构再讨论，预期一轮即可收敛。
