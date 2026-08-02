# post_spec R1 — qa-engineer
**verdict**: REVISE
**scope_ok**: true
**counts**: critical=4 major=3 minor=2

## SC 逐条红窗分析

| SC | 被测对象 | 怎么会红 | 判定 |
|----|---------|---------|------|
| SC-1 | 混合: `phase1_gate` 返回值(代码, 已 ship 继承逻辑) + 「AI 在起草前渲染 🔴 告警」(执行期行为, 本 Spec 新增) | 代码半: 两轨用不同格式写同一 issue (`aria-plugin#124` vs `10CG/aria-plugin#124`) → `linked_issue_overlaps` 精确字符串比较判不相等 → 告警不触发 (假阴性, 见 CRITICAL-4)。执行期半: AI 干脆不在 A.1 调用 `phase1_gate` 直接开写 → 无任何 committed 测试能捕获, 只能靠人工事后翻 transcript | **不完整可红** — 代码半有格式盲区; 执行期半结构性不可测且无对应测试 |
| SC-2 | 同上镜像场景 + 「claim 已写且已推 (`push_success` 真)」 | `phase1_gate.py:1229-1237` 的 `try/except` 对 `linked_issue_overlaps` 任何异常一律 fail-soft 成 `[]`("overlap advisory must not break the gate") ⇒ 真实重叠因异常被吞时, SC-1 的「应告警」与 SC-2 的「正常起草」在输出上不可区分。`push_success` 本身可机械验 (继承 phase1_gate 既有行为), 但「AI 在起草前调用」这一半仍是执行期行为 | **部分可红**(仅覆盖 push_success 字段的代码半) |
| SC-3 | 声称「A.1 流程断言该参数在场」, 实为纯 AI judgment | 见下方 CRITICAL-2 —— 答不出「谁执行、何时执行」。当前设计里没有任何脚本/hook/checker 拥有这条断言, `phase1_gate.py` 的 `--linked-issue` 本身非 `required` (:1198-1200), D6/非目标又明确排除改 phase1_gate 代码。**没有一条实现路径能让这条 SC 变红** | **恒真 / 不可执行** |
| SC-4 | `sibling_spec_probe.py` (待建代码) | 若实现照抄 `collision.py:217` 的精确字符串匹配 (无归一化) 会漏检格式不同的同 issue sibling; 若只 fetch `origin` 不 fetch `github` (本仓当前就存在双远程分叉现状, 见 MAJOR-3) 也会漏检落在另一远程的 sibling | 可红, 但红窗有两个未被规范约束的已知盲区 |
| SC-5 | `sibling_spec_probe.py` | 反例: 实现遍历 ref 不全 (如只查 `refs/heads/*` 漏掉其他命名空间) 对真实存在的 sibling 误报「空」→ 该 SC 会检测到并变红 | 可红 |
| SC-6 | `sibling_spec_probe.py` 的 fetch 失败路径 | 反例: 实现在 fetch 抛异常时静默吞掉返回「看似正常的空结果」而非标注 `degraded` → 可用仓内既有先例 `mock.patch.object(module, "_run", side_effect=...)` (`test_remote_refresh.py` 的 `test_failed_fetch_*` 系列) 可靠、非 flaky 地构造 | 可红, 且构造手法仓内有现成先例 (proposal 未引用) |
| SC-7 | `sibling_spec_probe.py` 自排除逻辑 | 反例: 实现忘记排除自身 track-id/spec 目录 → 探针命中自己 → 逻辑上可红。但见 MAJOR-2: rule6_note 与 Impact 表对这条 SC 是否真被新结构化测试覆盖**自相矛盾**, 落地时可能两头都不测 | 逻辑可红, 但文档对「是否会被测」自相矛盾 |

## Findings

### [CRITICAL] SC-1/SC-2 主机制「AI 记得在 A.1 调用+消费告警」无可执行验证面, Impact 表所称「既有测试」不存在
- **位置**: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:97, :137-138, :164 (对照 aria/skills/phase-a-planner/ 全目录)
- **问题**: proposal Impact 表写「`skills/phase-a-planner/` 既有测试 | 扩展 (SC-1~3)」(:164), 暗示存在可扩展的既有测试套件。实测 `aria/skills/phase-a-planner/` 目录只有一个 `SKILL.md` (318 行纯 prose), 零 `scripts/`、零 `tests/`；repo 全局 grep 「phase-a-planner」的测试文件只命中一个不相关的 benchmark fixture (`aria-plugin-benchmarks/emergency-hotfix-audit-file-scope/test_doc_existence.py`)。SC-1/SC-2 里「AI 在起草前渲染 🔴 告警」「AI 在起草前调用 phase1_gate」这两条断言, 是纯粹的 AI 执行期 judgment (读 SKILL.md 后决定是否照做), 没有任何编排层代码把这一步接住 —— 与本项目刚发生过的同形先例完全一致 (`aria/skills/state-scanner/tests/test_runtime_probe_authoring_guide_contract.py` docstring: 「向导承诺 ↔ 运行时现实一致性」这类行为「状态-scanner 固定 AB 测试集结构上测不到」)。
- **证据**:
  ```
  $ find aria/skills/phase-a-planner -iname "*test*"
  (无输出)
  $ grep -rln "phase-a-planner" --include="test_*.py" --include="*.sh" .
  aria-plugin-benchmarks/emergency-hotfix-audit-file-scope/test_doc_existence.py   # 与本 SC 无关
  ```
- **建议修法**: 要么 (a) 在 Impact 表如实标注「phase-a-planner 无既有测试, 本 change 需**新建**测试基础设施」并具体设计一个可执行的检查载体 (例如仿照 `coordination_probe.py` 的 telemetry-探针模式, 见 CRITICAL-2 的建议), 要么 (b) 按 Rule #6 判据表第三行诚实降级: 承认「AI 是否在 A.1 调用/渲染告警」这一半结构上不可自动化验证, 点名该行为 + 建可证伪定向 fixture (如: 录制一段真实 A.1 transcript, 人工/LLM-judge 复核是否出现调用与告警) + 开 issue 记录该缺口, 而不是让 Impact 表的失实陈述掩盖「无测试」的事实。

### [CRITICAL] SC-3「A.1 流程断言该参数在场」没有任何拥有者 —— 无脚本/无hook/无checker, 且当前架构下无法长出一个
- **位置**: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:139 (SC-3), 对照 :151 (非目标「不改 phase1_gate 自身代码」) 与 aria/skills/state-scanner/scripts/phase1_gate.py:1198-1200
- **问题**: 任务原文明确问「谁执行这个断言? 什么时候执行? 它需要一个『A.1 流程』的可执行表示, 那个东西存在吗?」—— 答案是不存在。三个可能的执行位置全部被排除或缺失: ① `phase1_gate.py` 本身 —— `--linked-issue` 定义为 `default=None` 而非 `required=True` (:1198-1200), 且本提案「非目标」条款明确「不改 phase1_gate 自身代码」(:151); ② `phase-a-planner` —— 纯 SKILL.md prose, 无代码, 见上一条; ③ 任何新增文件 —— Impact 表 (:160-165) 列出的新文件只有 `sibling_spec_probe.py` 及其测试 (服务于 §2), 没有任何一个新文件的职责是「校验某次 A.1 调用在 spec 有关联 Issue 时确实带了 `--linked-issue`」。值得注意的是, 仓内**已有**可复用先例: `aria/skills/state-scanner/tests/test_phase1_gate_telemetry.py` (TASK-011/012) 描述的「production 分区 telemetry + `coordination_probe` 反欺骗探针」机制, 本质上就是「校验某次调用真的发生了」的基础设施, 但本提案既未引用也未纳入范围去扩展它以覆盖「调用时参数是否合规」。
- **证据**:
  ```
  $ grep -n "required=True" aria/skills/state-scanner/scripts/phase1_gate.py | grep -i linked
  (无输出 — --linked-issue 不是 required)
  $ grep -rn "phase1_gate\|linked-issue" aria/skills/phase-a-planner/
  (无输出 — phase-a-planner 目前零调用, 这正是本 Spec 要修的缺口, 但修完后仍是 prose)
  ```
- **建议修法**: 要么设计一个真实的执行体 (例如: 扩展 `coordination_probe.py`, 在 A.1 结束后读取本 session 的 production telemetry 记录, 比对本次生成的 proposal.md 是否含「关联 Issue」字段, 二者不一致时输出可被 post_spec 审计消费的 finding), 并把它加进 Impact 表; 要么把 SC-3 降级措辞为「AI 应做到 X, 但目前仅靠 SKILL.md 指令约束, 无机械兜底」, 不要用「可红」这种暗示结构化可证伪性的用词。

### [CRITICAL] Rule #6 分类误判 — 两个 SKILL.md 改动的 AB 套件结构性覆盖不到新行为, 「照跑 AB 零裁量」是空头支票
- **位置**: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:129 (rule6_note)
- **问题**: rule6_note 断言 `phase-a-planner/SKILL.md` 与 `audit-engine/SKILL.md` 的改动落在 CLAUDE.md Rule #6 判据表第二行「处方性 · 运行时指令面 → [AB] 能测得到 → 照跑 AB, 零裁量」。实测两个 Skill 现有的固定 AB eval 套件:
  - `phase-a-planner`: 5 个 eval (`full-cycle-execution` / `skip-condition-detection` / `existing-spec-detection` / `yaml-output-format` / `error-recovery`), 全部围绕单轨场景, 零个涉及并发 track / linked-issue / phase1_gate。
  - `audit-engine`: 2 个 eval (`convergence-spec-review` / `challenge-architecture-decision`), 全部是单份 proposal 内容审查, 零个涉及 sibling-spec 扫描 / fetch 远端 / Step 0.5。
  这与本仓 `aria/skills/state-scanner/tests/test_runtime_probe_authoring_guide_contract.py` docstring 记载的同形先例完全吻合 (「对一个套件结构上测不到的行为跑 AB 是测量剧场」)。按 CLAUDE.md Rule #6 判据表, 这应落**第三行**「处方性 · 套件覆盖外 → 点名行为 + 建可证伪定向 fixture + 套件缺口开 issue」, 而不是第二行。这不是文字游戏: 它意味着「照跑 AB, 零裁量」这句话给读者的印象 (有一个安全网会验证新指令确实起作用) 是假的, 且直接影响上面两条 CRITICAL —— 如果指望 AB 兜底 SC-1/2/3, 而 AB 结构上碰不到, 那 SC-1/2/3 就真的没有任何自动化验证面了。
- **证据**:
  ```
  $ cat aria-plugin-benchmarks/phase-a-planner/iteration-1/eval-*/eval_metadata.json | grep eval_name
  "eval_name": "full-cycle-execution"
  "eval_name": "skip-condition-detection"
  "eval_name": "existing-spec-detection"
  "eval_name": "yaml-output-format"
  "eval_name": "error-recovery"
  $ cat aria-plugin-benchmarks/audit-engine/evals/evals.json | grep eval_name
  "eval_name": "convergence-spec-review"
  "eval_name": "challenge-architecture-decision"
  ```
- **建议修法**: 把 rule6_note 改判到第三行: 点名「A.1 认领调用 + 告警渲染」「Step 0.5 竞品扫描的消费」两个行为为 AB 套件覆盖外, 补一条定向 fixture (例如上面 CRITICAL-1 建议的 transcript 复核法), 并对两个 benchmark 套件各开一个「补 concurrent-track eval」的缺口 issue。**不要**在套件结构性测不到的前提下继续宣称「零裁量照跑」。

### [CRITICAL] `linked_issue` 精确字符串匹配 + 仓内生产数据已现两种格式共存 ⇒ SC-1 可被格式不一致静默绕过
- **位置**: aria/skills/state-scanner/lib/collision.py:217 (`if c.linked_issue != own_linked_issue: continue`); openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:91 (`--linked-issue "<repo>#<n>"` 示例), 全文未提归一化规则
- **问题**: `linked_issue_overlaps()` 对 `linked_issue` 字段做**精确字符串相等**判断, 无任何大小写/前缀归一化。我在本仓当前的 `refs/aria/coordination` (主仓 coordination ref, 与 origin 一致, SHA `474cb12...`) 里直接找到**同一容器 (023236f2) 在不同 claim 里写的两种格式并存**:
  - `claims/023236f2/s-b291@1154.yaml` → `linked_issue: aria-plugin#124`
  - `claims/023236f2/s-9c6f@0316.yaml` / `s-bd4b@1845.yaml` → `linked_issue: 10CG/aria-plugin#113`
  以及 `bfe8285d` 容器同样存在裸 `aria-plugin#118/#122/#116` 与带前缀 `10CG/aria-plugin#110/#121` 混用。这不是假设的边界情形, 是**当前生产数据里已经并存的事实**。若 track L 用 `10CG/aria-plugin#124` 起草认领, track R 稍后用 `aria-plugin#124` (或反之) 起草同一 issue, `linked_issue_overlaps` 判定两者不相等 ⇒ SC-1 期望的「🔴 告警」**不会触发**——原样复现本 Spec 存在的理由 (「防两个 AI 容器对同一 issue 重复起草」)。proposal 的 §1/§2/非目标/D1-D7 均未提及格式归一化, SC 表也没有对应的「格式不同但语义相同」反例测试。
- **建议修法**: 在 A.1 认领的 `--linked-issue` 前加一步归一化 (如统一剥离 `owner/` 前缀, 只保留 `repo#n`), 并在 SC-1 或新增 SC 里显式加一条「格式不同但指向同一 issue 仍应告警」的用例; 若认为归一化超出本 Spec 范围 (D1 明确「不新造检查」), 至少应像 §3 处理「残余缺口」一样, 在正文里诚实记录这条格式盲区, 而不是完全不提。

### [MAJOR] §2 只定义「检测」半, 未定义「消费」半 —— audit-engine 命中后做什么, 全文未写
- **位置**: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:99-105 (§2 全段), 对照 :97 (§1 明确写了「AI 先向用户报告再决定是否继续起草」的消费义务)
- **问题**: §1 对「命中之后怎么办」写得很具体 (渲染 🔴 告警 + 要求 AI 先报告再决定)。§2 只写了 Step 0.5「grep 全部远端 ref … 报告命中」, 完全没写 audit-engine 拿到命中结果后做什么: 是写进报告哪个章节 (Step 0 的 anchor 有明确去向「报告 body 的 drift_metrics 章节」, 见 `aria/skills/audit-engine/SKILL.md:99`)? 是否影响收敛判定? 只是打印在 stdout 没人看? SC-4「`sibling_spec_probe.py` 报告命中」只验证脚本自身输出正确, 不验证这个输出是否/如何被人类可见地消费。如果消费环节被漏掉或被 AI 静默略过, 探测再准也不会产生本 Spec 想要的效果——这是同一份提案在 §1 上很谨慎、在 §2 上却留了空档。
- **证据**: proposal.md :99-105 通篇没有出现「报告」「渲染」「章节」「消费」等指向人类可见输出的词, 对比 :97 「并**要求 AI 先向用户报告再决定是否继续起草**」的明确措辞。
- **建议修法**: 比照 Step 0 的写法, 明确 Step 0.5 命中后写入报告的哪个章节/字段, 以及 audit-engine 编排层看到该字段后的强制动作 (至少是「渲染给用户」这一步), 并补一条 SC 验证这条消费路径。

### [MAJOR] rule6_note (SC-4~6) 与 Impact 表 (SC-4~7) 对 `test_sibling_spec_probe.py` 覆盖范围自相矛盾
- **位置**: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:129 vs :163
- **问题**: 第129行写「新增 `sibling_spec_probe.py` 为确定性代码 → 结构化测试覆盖 (**SC-4~6**)」, 第163行 Impact 表写「`skills/audit-engine/tests/test_sibling_spec_probe.py` | 新增 (**SC-4~7**)」。两处对同一个新测试文件覆盖几条 SC 给出不同答案, 差的正好是 **SC-7**——全套件里最安全攸关的反向对照 (自命中排除)。这不是抄写笔误级别的小事: 若开发者按 rule6_note 执行 (只覆盖 SC-4~6), SC-7 会在「已声明有测试」的错觉下实际零测试落地; 若按 Impact 表执行则没问题, 但两处矛盾意味着**读者/实现者无法确定该信哪个**。
- **证据**: 原文逐字引用如上, 行号见「位置」。
- **建议修法**: 统一两处为 SC-4~7 (既然 D4「副机制的盲区写进 Spec 正文, 不藏进脚注」的精神也要求反向对照不能是可选项), 并在 tasks 拆分阶段把 SC-7 的测试用例明确列出, 避免开发时选择性遗漏。

### [MAJOR] Dogfood 可信度: 文档不自证, 独立取证部分吻合但覆盖面比措辞窄, 且双远程未同步
- **位置**: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:15-28 (dogfood 叙述), :126-127 (D6/D7 「已实测坐实, 非推断」)
- **问题**: proposal 正文引用了一次 2026-08-02 的实跑, 但**没有引用任何仓内可核验的指针**(commit SHA / ref 名 / claim 文件路径) —— 单看文档本身, 这条声称无法被验证, 是任务提示里点名的「不可验证的自述」形状。我做了独立取证, 结果是**部分吻合, 但比文档措辞暗示的窄**:
  1. **吻合部分**: 主仓 `refs/aria/coordination` (本地与 `origin` 一致, SHA `474cb123879c1189394b124b1dc5f75eca1ffae2`) 下确有 blob `claims/023236f2/s-b291@1154.yaml`, 内容为 `track_id: aria-plugin-124-path-coverage-z-flag` / `linked_issue: aria-plugin#124` / `phase: A.1` / `claimed_at: '2026-08-02T11:54:59Z'` / `owner: aria-runner-bot`, 与叙述的 track-id、linked-issue、phase、`push_success=true` (确实已推 origin) 一致。**D6 的「`--phase` 无 choices 约束」这条纯技术性核实是真的** (`phase1_gate.py:1189-1191` 确认无 `choices=`)。
  2. **未同步**: 同一个 ref 在 `github` 远端的 SHA 是 `ad0287f759c23f9ee85d02fe0b47842eb5f71103`, 与 origin/本地的 `474cb12...` **不一致**——即这条「已推远端」的证据本身就是本仓 CLAUDE.md 明文的「多远程推送两条硬约束」正在被违反的活样本 (coordination ref 只推了 Forgejo 没推 GitHub)。
  3. **覆盖面比措辞窄**: 所选场景 aria-plugin#124, 从 `aria/` 子模块提交历史看只有 `fix(phase-c): ... (#124)` / `Merge fix/124-...` / `chore(release): ...` 系列提交, 没有对应的 `docs(spec)` proposal —— 也就是说 #124 是走 Level-1「简单修复」路径, 真实场景下 `phase-a-planner/SKILL.md:65-67` 的 `skip_if: complexity: Level1` 会让 A.1 (从而本 Spec 新增的认领调用) **整体跳过**。这次 dogfood 是手工模拟 CLI 调用形态, 验证的只是「`phase1_gate` 接受 `--phase A.1` 这个自由字符串」, 不是「A.1 在真实自然触发路径上会调用它」。D6/D7 用「已实测坐实」「非推断」这类强措辞, 但没有验证到「自然触发路径」这一层, 也没有验证到「AI 看到 `linked_issue_overlap` 非空后真的渲染了告警」这一层 (本次是空 `[]`, SC-2 分支, 没有练到 SC-1 分支)。
- **证据**: 见上文逐条; `git ls-remote origin refs/aria/coordination` = `474cb12...`, `git ls-remote github refs/aria/coordination` = `ad0287f...` (2026-08-02 现场取证)。
- **建议修法**: 在 proposal 正文里补一句可核验指针 (哪怕只是 "见 refs/aria/coordination commit 474cb12"), 让声称可以脱离我的独立取证被别人复核; 措辞上把 D6/D7 的验证范围收窄为「验证了 CLI 参数形态, 未验证 A.1 自然触发路径与 SC-1 告警渲染分支」; 另外双远程分叉是本仓已知的高优先级纪律项, 建议顺手 `git push github refs/aria/coordination` 补齐 (不属于本 Spec 范围, 但既然审计发现了不应放着不提)。

### [MINOR] SC-6 的 fetch-失败构造法在仓内有现成可靠先例, 但 proposal 未引用
- **位置**: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:142 (SC-6); 对照 aria/skills/state-scanner/tests/test_remote_refresh.py (`test_failed_fetch_keeps_stale_fetched_at_honest` / `test_failed_fetch_increments` 等, 用 `mock.patch.object(remote_refresh, "_run", side_effect=...)` 确定性模拟 fetch 失败)
- **问题**: 任务提示专门问「怎么构造 fetch 失败? fixture 能可靠制造这个条件吗?」——答案是可以, 且本仓已有现成、非 flaky 的先例模式 (mock 内部 `_run` 而非依赖真实网络断连)。但 proposal 全文没提这个可复用手法, `sibling_spec_probe.py` 目前连文件都不存在, 无法保证实现时会预留一个可注入失败的 `_run`-类似接缝; 如果实现者直接写死 `subprocess.run(...)` 而不留 seam, SC-6 的测试就只能退化成依赖真实网络条件的脆弱测试。
- **证据**: `grep -n "mock.patch.object" aria/skills/state-scanner/tests/test_remote_refresh.py` 命中 10+ 处, 均为 mock 内部 `_run`/`fetch_budget_override` 等函数, 非真实网络调用。
- **建议修法**: 在 tasks 拆分阶段明确要求 `sibling_spec_probe.py` 把 git 调用封装成可 mock 的内部函数 (仿 `remote_refresh._run` 模式), 并直接引用 `test_remote_refresh.py` 的对应测试作为实现范本。

### [MINOR] SC-7 反向对照不足一项 + §2 同样存在未声明的格式归一化盲区
- **位置**: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:143 (SC-7), :99-105 (§2 全段)
- **问题**: 两点缺口: (1) SC-7 只排除「自身 track-id / 自身目录」, 未覆盖「远端存在的是已归档/已废弃的同 issue 目录」(例如已合并进 `openspec/changes/archive/` 或在其他分支被标记 Superseded 的旧草稿) —— 探针若对所有历史 ref 不加区分地 grep, 可能对早已解决的旧草稿重复告警, 制造噪音, 长期侵蚀 advisory 机制的可信度 (「狼来了」效应, 人类学会忽略); (2) §2 的「关联 Issue」比对同样没有说明是否归一化格式, 与 CRITICAL-4 是同一病灶的姊妹缺口, 但 SC-4~7 没有一条测试覆盖它。
- **证据**: proposal.md :99-113 通篇没有出现「归档」「废弃」「Superseded」或格式归一化相关字样。
- **建议修法**: 给 SC-4 或新增 SC 补一条「远端存在的 sibling 目录已被归档/标记废弃 ⇒ 不应算命中(或至少降级展示)」的反向对照; 格式归一化建议 §1/§2 共用同一份归一化规则 (一次实现, 两处调用), 避免出现两套不一致的匹配语义。
