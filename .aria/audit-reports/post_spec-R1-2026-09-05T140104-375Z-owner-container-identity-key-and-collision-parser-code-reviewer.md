---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T14:26:19.625Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — code-reviewer 席 (规格合规 + 内部一致性)

审计对象: `openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md` @ 144d79e (110 行)。只审不改。

## Phase 1: 规格合规 — PASS

逐项实读结果:

- 头部字段: Level / Status / Created / Linked Issue 四行齐, 顺序与 `standards/openspec/templates/proposal-minimal.md:3-6` 一致。Linked Issue 值为单个 code span `10CG/Aria#193, 10CG/aria-plugin#135`, 用 `, ` 分隔, 行首无空白, ASCII 冒号, 非链接形 —— 满足 `aria/skills/spec-drafter/SKILL.md:349-351` 写法三条。
- Rule #5: Spec 落主仓 `openspec/changes/`, 代码落 aria / standards 子模块 (proposal:8), 正确。
- Rule #6: 陈述落「描述性 / 纯代码 -> substitute」档 (proposal:74), 与 `skill-benchmark-exemption.md:28` 第一行及 :63-64 先例 (v1.59.0/v1.60.0 collector 纯代码) 一致; 无 SKILL.md / description / rules dispatch 变更面; `rule6_note` 承诺 B.2 写入 (proposal:74)。判档成立, 但 baseline-failing 集合的点名有误 (见 minor-4)。
- Rule #10: 未见自行豁免任何 enabled 闸; SC-5 明写复用 phase-d D.2 gate。
- 禁用符号: `grep -P` 带圈数字 / 希腊字母区段 exit=1, 零命中。
- 引用行号逐字核对 (proposal:108): `split_owner_container` :63 / `track_to_claim_record` :86 / `classify_claims` :143 / `classify` :300 / `get_container_id` :191 / `handoff_multibranch.py:518` / `track_board.py:412` 全部命中。
- triage 数字 (proposal:16-17 vs `.aria/triage-report.json` case-1..5): 142/12/0 分布、34+2 / 23+17 份数、日期区间、case-2..5 的 🟡/🟡/none/🔴 全一致; #193 comment 21431 实取 (2026-09-05T13:42:49Z, partial-repro/major/next-cycle) 一致。
- 频次复核: `grep -h '^owner-container:' docs/handoff/*.md | awk -F'/' '{print NF-1}' | sort | uniq -c` 得 `12 0 / 142 1`, 与 proposal:16 一致。
- a1-entry 引用: 「新增直取 uuid accessor」= a1-entry proposal.md:144 逐字; `include_terminal` 形参 = :356; 「口径待定 … 不在本 Spec 统一二者」= :416, 所属节为 `### §3 入口覆盖 (S6)` (:374), proposal:10 的「§3」引用准确。
- 非目标 (proposal:100) 与 D3 (proposal:42) 关于 #182 的表述一致 (都是「只抄送, 不处理」), 无矛盾。
- Tasks 与 SC 映射: T1..T6 各有 SC-1..SC-6 一一覆盖; T7 (回帖/关票) 无 SC, SC-7 (零回归) 无 T —— 见 minor-5。
- D-1/D-2 回填落点: T5 / SC-5 明写「按裁定回填」, 落点清楚; SC-5 在裁定前不可验, SC-1..SC-4 与裁定无关可先行。

## 审计结论

### Major

**[M-1] 实验表 A/B/C 与 §Why 第 4 段的数据不是生产路径产出 (绕过了 dedupe)**
- type: issue / severity: major / category: testing / scope: proposal:20, :44-52, :57, SC-6
- summary: 表 A/B/C 是把 154 行原始 frontmatter 直接喂 `classify()` 得到的; 生产 collector 先 `dedupe_latest_per_track_container` 再 `classify` (handoff_multibranch.py:709-714)。按生产路径复跑: A = 1 组 (与 live snapshot 一致), B = 2 组, C 中不存在那组 🔴。「修 parser 立刻暴露 🔴 / 三层必须一起处置」的叙事失据。
- evidence: 我在 154 份工作树 frontmatter 上用真函数复跑 (脚本 `scratchpad/exp.py`): 经 dedupe 后 `A: kind=self_multi_container groups=[['dev-claude','simonfishgit/dev-claude']]`; `B: groups=[['simonfish/dev-claude','simonfish/dev-claude2'],['dev-claude','simonfishgit/dev-claude']]`; 不经 dedupe 的 raw 调用才得到 proposal 表 A 的两组和表 B 的三组 (含 `['aria-runner-bot/023236f2','simonfish/bfe8285d']`)。`.aria/state-snapshot.json` (2026-09-05T13:11:31Z) 的 `tracks_multibranch.collision.groups` 亦只有 `[['dev-claude','simonfishgit/dev-claude']]`; triage-report case-2 notes 已写明这一点, proposal 未采纳。那组 🔴 的来源 track `state-scanner-stale-refs-false-parity` 两个 container 的最新行都是 `done` (07-17 / 07-19), dedupe 后不再是 active 对。
- 修法: 表 A/B/C 与 SC-6 的冻结基线改用生产路径 (`dedupe` -> `classify`) 重算; §Why 第 4 段「响亮误报」改为按真实结果陈述 (目前生产路径下修 parser 后没有 cross_owner 误报, 只有 `dev-claude` 组因零段/两段混判会变 🔴)。

**[M-2] D1「dedupe 不改逻辑」与 SC-4「同容器不同 owner 两行折叠为 1 且产出 advisory」互斥, 且与 D3 数据流冲突**
- type: issue / severity: major / category: architecture / scope: proposal:31, :41, SC-4 (:91)
- summary: dedupe 分组键是 `(track_id, owner, container)`; 新 split 下同容器不同 owner 得两把不同键, 结构上不会折叠。要折叠只能把键改成 `(track_id, container)`, 这就是改逻辑。dedupe 本身也没有 advisory 输出。再者 collector 先 dedupe 再 classify: 若在 dedupe 层就把双 owner 折成一行, classify 看不到第二个 owner, D3「identity_advisories 由 D1 的分组副产物产出」在生产路径上拿不到同 track 的证据。
- evidence: handoff_multibranch.py:518-523 `key = (t.get("track_id"), owner, container)`; :709 `deduped_tracks, dedupe_stats = dedupe_latest_per_track_container(tracks)` -> :714 `collision = _classify_collision_summary(deduped_tracks)`; classify() 只接收 deduped 列表 (collision.py:300 起)。
- 修法: 二选一并写明: (a) dedupe 键改 `(track_id, container)` (承认改逻辑, 加 SC 锁), identity_advisories 改由 dedupe 前的全量 tracks 扫描产出 (需要给 classify 加入口或在 collector 单独算); (b) dedupe 键不改, SC-4 删掉「同容器不同 owner 折叠为 1」这半句, 由 classify 的 container 主键分组吸收双 owner 行。

**[M-3] D1 判定键谓词在「单 container 自身多 owner」形态下未定义**
- type: issue / severity: major / category: architecture / scope: proposal:30, :36, :52
- summary: 规则写「≥2 个 distinct container 时再看 owner: owner 全同 -> self_multi, owner 不同 -> cross_owner」。当某 container 自身出现两个 owner 段 (proposal:52 列出的 4 个 container 全是这种形态) 时, 「owner 全同」取并集还是取每容器一个代表, 结果相反 (并集必 ≥2 -> 一律 🔴; 取代表则取哪个未定)。该谓词要写进 §2.3.5 规范表, 不能留给实现顺序裁决。
- evidence: proposal:30 原文; proposal:52 `023236f2: [aria-runner-bot, simonfish] · bfe8285d: [aria-runner-bot, simonfish]`; 我复跑 C 近似 (取并集) 时 `aria-submodule-gate-block-flip` 的 `dev-claude` 容器同时携带 `''` 与 `simonfishgit` 两个 owner, 恰是需要裁决的格。
- 修法: 在 D1 写死全分割规则 (例: 先按 container 归并并产 advisory, 再以「每 container 最新 active 行的 owner」参加 owner 比较; 或按并集并接受 🔴 偏保守), 并把选定规则连同反例写进 SC-2。

**[M-4] 「表 C 那组 🔴 由 D-1/D-2 裁定后消解」在推荐选项 (a)+(a) 下不成立**
- type: risk / severity: major / category: documentation / scope: proposal:50, :57, :62
- summary: D-2(a) 只改未来 commit 署名; 历史 handoff 明写不 rewrite (proposal:38, :102); D-1(a) 定义 owner = 提交身份。三者叠加, 历史双 owner 行原样保留, 任何含 `simonfish/<uuid>` 与 `aria-runner-bot/<uuid>` 两 active 行的 track 在 container 主键规则下仍是 cross_owner。能消解的只有 D-1(b) 映射、#182 状态收口, 或 M-2 里的 (track_id, container) 覆盖式 dedupe —— 后两者 proposal 都没把它们和这句因果连起来。给 owner 的决策后果描述因此失真。
- evidence: proposal:57 「必须靠 D-2 把 AI runner 的身份收敛到一个值, 否则 cross_owner 会误报 (实验表 C 那组 🔴)」与 :38 / :102 不 rewrite 并读。
- 修法: 改写 D-1/D-2 的「后果」句: 明确 (a)+(a) 消解的是「未来新增的漂移」, 存量并存期由 D3 advisory + #182 处理; 若期望存量也消解, 须在 D1 写出覆盖式 dedupe 并加 SC。

### Minor

**[m-1] 「9 种 owner-container 串对应 2 台机器」计数错, 且漏一个 container 标识**
- type: issue / severity: minor / category: documentation / scope: proposal:18
- evidence: `grep -h '^owner-container:' docs/handoff/*.md | sort | uniq -c` 得 10 种 distinct 串, 第 10 种 `simonfish/f9c6e8cd` (1 份, `docs/handoff/2026-07-04-m6-blocker3-b2-impl-postplanning-rollout.md`) 是第 5 个 container 标识; 「2 台机器」未给 hostname <-> uuid 对应证据。
- 修法: 改为「10 种串 / 5 个 container 标识 (含 hostname 时代 2 个)」, 或给出机器映射依据。

**[m-2] 「自 2026-05-30 (aria 83a1a45) 引入」归因过晚, 继承自 triage**
- type: issue / severity: minor / category: documentation / scope: proposal:16
- evidence: `git -C aria log -S'Two-part: treat as container/session'` 得 f9306a0 (2026-05-20, TASK-016/017 在 track_board.py 首次引入) -> 83a1a45 (05-30 搬入 lib, docstring 自述 `relocated verbatim from track_board.py`) -> c6988b4。三段式契约始于 05-20 的 renderer。
- 修法: 改「引入于 f9306a0 (2026-05-20, track_board.py), 83a1a45 搬迁至 lib 未改语义」。

**[m-3] 引用 §2.3.3 的「写入频度 = 会话结束一次」落错节**
- type: issue / severity: minor / category: documentation / scope: proposal:29
- evidence: `session-handoff.md:198` 「写入频度 | session 结束时一次 (D.3) | …」位于 `### 2.3.6 与 Layer L claim schema 的区别` (:189); `### 2.3.3` (:143) 是「与 prose 段共存规则」。
- 修法: 改引 §2.3.6。

**[m-4] Rule #6 substitute 点名的 baseline-failing 集合含两条不是测试的 SC; 一处过时注释未列入同步面**
- type: issue / severity: minor / category: testing / scope: proposal:74, :92-93
- evidence: proposal:74 「见 SC-1..SC-6, 每条对当前代码必须先红」, 但 SC-5 的判据是既有 14 check 全绿 (`.aria/state-checks.yaml` 实数 14, 名字 `linked-issue-field-availability` :346 / `claude-md-changelog-free` :190 均在), SC-6 是 handoff 内的对照表 —— 二者结构上不能「先红」; `skill-benchmark-exemption.md:28` 要求的是 SC 级 baseline-failing 结构化测试。另 `aria/skills/state-scanner/references/rules/advanced-rules.md:578` 「collision helper 已按 owner+container 归类」在 D1 后过时 (Rule #3 同步面), 属溯源注释档, 不改判档。
- 修法: substitute 集合改点名 SC-1..SC-4 (+ SC-2 的 identity_advisories 断言); 把 advanced-rules.md:578 注释与 :544 的 kind 枚举注释列入 D3 同步面。

**[m-5] Tasks 与 SC 有孤儿, schema bump 无锁**
- type: issue / severity: minor / category: documentation / scope: proposal:79, :84, :94
- evidence: T7 (回帖 / 关票) 无对应 SC; SC-7 (零回归) 无对应 T; T2 的「snapshot schema additive bump 记录到 `state-snapshot-schema.md`」(文件实存 `aria/skills/state-scanner/references/state-snapshot-schema.md`) 无 SC 检查其落地。
- 修法: 给 T7 加一条 SC (两票均有回帖链接, #193 closed); SC-7 归到 T1..T4 的联合验收; T2 的 schema 文档 bump 并入 SC-2。

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical / 4 Major / 5 Minor。

Phase 1 规格合规通过; Phase 2 的四条 Major 集中在一件事: proposal 的核心实证 (实验表 + 「三层必须一起修」+ D-1/D-2 后果描述) 建立在绕过生产 dedupe 的调用路径上, 而 D1/SC-4/D3 之间的数据流又没有对齐。第 1 层 parser 缺陷本身 (triage case-2..5) 经真函数直调核实成立, 第 2/3 层漂移事实也成立, 因此 Spec 方向不需要推翻, 但 What 段的判定键规则、SC-4/SC-6 与实验表须按生产路径重写后再进 A.2。

## Vote

**REVISE**

## 轮次记录

- R1 (2026-09-05, code-reviewer 席, convergence): 实读 proposal 110 行、模板、spec-drafter :342-360、skill-benchmark-exemption 判据表与 §3、CLAUDE.md Rule #5/#6/#10、collision.py (:55-215, :295-403)、identity.py (:191-244)、handoff_multibranch.py (:495-540, :709-714)、track_board.py (:400-425)、triage-report.json 全文、a1-entry proposal.md (:3-6, :142-144, :356, :374, :416)、session-handoff.md §2.3 各节、.aria/state-checks.yaml (14 项)、live snapshot collision; 在 154 份工作树 frontmatter 上用真函数复跑实验表 (dedupe 路径与 raw 路径各一次)。结论 0C/4M/5m, 投 REVISE。
