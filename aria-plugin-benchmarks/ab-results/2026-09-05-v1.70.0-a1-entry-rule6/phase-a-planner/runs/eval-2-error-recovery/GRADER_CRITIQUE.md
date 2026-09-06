# GRADER_CRITIQUE — eval-2 error-recovery

评分结果: `with_skill` 3/3, `old_skill` 3/3 (平局)。以下是对 eval 本身的批判 + 回归信号排查。

---

## 1. 恒真 / 恒假断言

**三条断言全部接近恒真, 本 eval 几乎没有区分力。**

- **断言 1「Should detect and report unclean working tree state」= 事实恒真**。prompt 原文就把结论递到了嘴边: `State-scanner reports: uncommitted changes in 3 files, working tree dirty`。任何回答只要复述一遍这句话就 pass, 不需要真去 detect。两臂的证据强度天差地别 (见下 §2), 但断言字面读不出差别。
- **断言 2「Should block execution or issue a clear warning」= 析取式, 低门槛恒真**。"or issue a clear warning" 这半边把门槛降到「提一句注意」。实际上两臂**都明确说了「脏工作树不阻塞 Phase A」** —— 即两臂都选择不 block, 却都因为附带了警告而 pass。这条断言无法分辨「合理地不阻塞 + 精确告警」与「没想清楚就往下走」。
- **断言 3「Should provide steps to resolve the unclean state」= 实践中恒真**, 且**对处置是否正确完全免疫**: 只要给出「步骤」就 pass, 给的是**正确**步骤还是**在本仓会造成静默损坏**的步骤, 断言分不出来 (见 §2 第 2 点 —— 这是本 eval 最严重的盲区)。

**恒假断言: 无。**

建议: 若要让本 eval 有区分力, 至少补一条**负向**断言, 例如「不得在未核实这 3 个文件是什么之前就建议 `git stash` / `git checkout --` 丢弃」, 以及一条要求**实测**的断言 (「必须给出独立于 state-scanner 报告的实测证据, 如 `git status --porcelain` 输出」)。

---

## 2. 断言完全没覆盖的重要差异

### 差异 A — 「detect」的强度: 实测 vs 复述 (`with_skill` 明显更强)

- `with_skill` **独立实测**并推翻了 prompt 的表面描述: 跑 `git status --porcelain` + `git submodule status` + `git diff --stat`, 得出「这 3 个『文件』全是**子模块 gitlink 指针**」, 并逐个点名到 in-flight track (`aria` / `aria-orchestrator` / `standards`)。我核过仓内现状, 三个指针、活跃 Spec 7 个、`.aria/config.json` 的 `coordination.enabled=true / mode=advisory` 与 `audit.enabled=true / post_spec=post_planning=convergence / max_rounds=5`、`~/.aria/container-id` 的「label 必须保持为空」—— **全部与实仓一致, 无一处编造**。
- `old_skill` 全程只是把 prompt 里那句话**复述**了一遍 (「state-scanner 报的『3 个文件未提交、工作树脏』」), 没有任何独立测量。它对这 3 个文件是什么、属于谁、能不能安全丢弃**一无所知**, 却直接给出了处置命令。

断言 1 对这个差别完全失明。

### 差异 B — 处置建议的正确性: `old_skill` 的建议在本仓是有害的 (**这是最重要的未覆盖差异**)

- `old_skill` 给的是教科书式两选一: 「先 commit 到当前分支，或 `git stash` 挂起」/「确认后 `git checkout --` 丢弃」。
- `with_skill` 给的是**相反**的处方, 且给了理由: 「**不要 stash / 不要 checkout 丢弃**。子模块指针的 stash/丢弃会让工作区静默指到别的 SHA, 事后极难发现; 正确处置是原地不动 + 提交时用带路径的 scoped add」, 并追加了核验步骤「收尾必须跑一次**不带路径**的 `git status` 核验, 确认没有把 gitlink 顺手带上去」。

在这个真实工作区里 `with_skill` 是对的: 三处脏改动都是 submodule gitlink, `git checkout -- <submodule>` 只回滚超项目的 gitlink 条目而子模块工作区仍停在别的 commit, `git stash` 同理 —— 制造无人报警的指针漂移。另外 `old_skill` 的选项 1「先 commit 到当前分支」会把**三条不相干 track 的 gitlink bump** 提交到 `feature/a1-entry-claim-duplicate-work-guard` 这条别的 Spec 的分支上。

**断言 3 把这两个相反的处方都判成 pass。** 一个 error-recovery eval 无法分辨「正确恢复」与「制造新故障」, 是本套件的实质缺口。

### 差异 C — 脏状态可能是 Spec 的**输入**而非垃圾 (仅 `with_skill` 提出)

`with_skill` 先问了一个前置问题:「那 3 个未提交文件**是不是已经在做 payment gateway**。如果是, 就已经违反『规范先行』, 而且它们是 A.1 的**输入**」。`old_skill` 从未考虑这种可能, 默认脏 = 待清理。这是 error-recovery 场景里比「怎么清」更靠前的判断, 断言没有任何一条覆盖。

### 差异 D — 「3 个文件」诱发 Level 1 误分类的陷阱 (仅 `with_skill` 点名)

`with_skill` 显式拒绝: 「『3 个文件』很容易撞上跳过规则里的 `complexity: Level1`(变更文件 ≤3 + 简单类型)。**这里不适用**」, 并指出误判代价是「`Level1` 命中会让 A.1 的**认领闸门整块零调用**」。`old_skill` 也定了 Level 3, 但只走复杂度论证, 没识别出「脏文件计数被当成变更规模证据」这个具体误用路径。

### 差异 E — 分支落点 (仅 `with_skill` 提出)

`with_skill` 发现当前在 `feature/a1-entry-claim-duplicate-work-guard`(另一个 Spec 的 in-flight 分支), 并把「两个不相干的 Spec 会共用一个 PR」列为待裁项。`old_skill` 全文未提当前分支身份。

### 差异 F — 交付物: `old_skill` 真的执行了 Phase A, `with_skill` 零产物 (**唯一对 `with_skill` 不利的差异**)

- prompt 是 `Execute Phase A`。`old_skill` 跑完 A.1/A.2/A.3, 落盘 `proposal.md` / `tasks.md` / `detailed-tasks.yaml`(4 条 DEC + 5 条可证伪 AC + 7 任务 + agent 分配 + 并行轨), 只把 post_spec 审计与 3 个脏文件的处置留作待办。
- `with_skill` **停在起草之前**, 一份规划产物都没有, 全部输出是核查 + 三个待裁项。

断言完全不评交付面, 所以这个差异对分数零影响 —— 但它是本轮改动带来的最大行为变化, 见 §4。

---

## 3. 仓内语料污染排查 (openspec/changes/a1-entry-claim-duplicate-work-guard/)

**两臂都没有引用该目录下任何文档的内容或路径。**

- `old_skill` 整篇零痕迹 —— 没有认领闸门、`phase1_gate.py`、`linked_issue` 之类的任何概念。
- `with_skill` 只有**目录级接触**, 没有内容引用: 「扫了 `openspec/changes/`, 7 个活跃 Spec (a1-entry-claim-duplicate-work-guard, aria-2.0-m6-*, aria-2.0-m7-*), **无 payment 相关**」—— 这是 `ls` 的结果 (实测确为 7 个, 名单吻合), 用途是判 A.1 跳过条件, 不是拿该 Spec 的内容当依据。

**但污染不能被排除, 只能说未被证据支持。** 我逐个 grep 了 `with_skill` 用到的全部特征 token —— `--include-terminal` / `--emit-arg` / `linked_issue_field_probe.py` / `unknown_schema_claims` / `overlap_error` / `NO_FIELD` / `BAD_TOKEN` / 「未能核实」/ uuid-not-label / 终态可能是 GC 产物 / 改名要 release+acquire —— 结论是**两处都有**:

- 技能文件侧: `aria/skills/phase-a-planner/SKILL.md:65-123` 全部逐字含有 (四态表在 :102-104, uuid-not-label 在 :80-81, `--emit-arg` 两阶段在 :83, GC 注记在 :123)。
- 仓内语料侧: `openspec/changes/a1-entry-claim-duplicate-work-guard/{proposal.md,tasks.md,detailed-tasks.yaml}` 同样全部含有。

也就是说 `with_skill` 说的每一句认领闸门相关内容**都可由它自己的技能文件解释**, 无需假设它读了在制 Spec; 但由于 AB harness 跑在真仓无沙箱, 同批 in-flight 语料就在 `openspec/changes/` 下且被该臂 `ls` 到过, **通道是开着的**。判定: 无污染证据, 通道未关闭。

---

## 4. 回归信号 (caller 特别要求)

**在本 eval 的三条断言上没有回归: 3/3 vs 3/3。** 逐条看实质强度, `with_skill` 在断言 1 与断言 3 上都**更强**(差异 A / B), 断言 2 两臂等价。**没有任何一条断言是 `with_skill` 表现更差的。**

需要上报的一个**非断言面**的候选回归信号 (差异 F):

- 本轮新增的 A.1 入口认领闸门, 把一次 `Execute Phase A` 变成了**零交付 + 三个待裁问题**的回合。`with_skill` 自述停手理由是「acquire 的实参 (slug) 取决于下面第 5 节的落点/命名裁定」。
- 这个理由**自相矛盾**: 同一份回答里它已经把 slug 钉死并写进了要跑的命令 —— `--raw-track-id "add-payment-gateway-integration-023236f2"`, 且第 5 节的三个待裁项中没有一项会改变 slug (落点 a/b/c 三个选项都用同一个 `openspec/changes/<slug>/`, Level 2/3 不影响目录名, issue 号只影响 `--linked-issue`)。既然 slug 已定, 它本可以先跑闸门再起草, 而不是把闸门与起草一起停掉。
- 因此这次停手更像**过度阻塞**: 闸门要求的是「认领早于起草」, 不是「起草前先让 owner 回答三个问题」。代价是同一 prompt 下从 3 份规划产物退化到 0 份。
- 另一侧的观察: `with_skill` 耗时 235.8s / 82019 token / 9 次工具调用, `old_skill` 197.4s / 76906 token / 12 次 —— 多花 19% 时长与 7% token 却没有产出规划文档, 篇幅约 40% 花在认领闸门上 (本 eval 的主题是 error recovery, 不是认领)。这属于**目标行为溢出到回归臂**, 建议在母 Spec 侧确认是否符合预期。

以上第 4 节整体属于「断言外观察」, 不影响本 eval 判分。
