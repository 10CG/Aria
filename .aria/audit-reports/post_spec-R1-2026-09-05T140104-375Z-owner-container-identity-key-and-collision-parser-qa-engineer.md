---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T14:12:45.019Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

### type: issue / severity: critical / category: testing / scope: SC-7 zero-regression 承诺 vs Task 范围

**summary**: 既有测试 `test_both_latest_active_still_reports_self_multi_container` 锁死的 owner-container 对, 在实跑目标语义下必然翻转为 `cross_owner`; Tasks 未列名此测试, SC-7「零回归」在当前 Task 范围内不可达成。

**evidence**: 实读 `aria/skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py:305-341`, 该测试用真实两段式串 `aria-runner-bot/023236f2` (3 条 active) 与 `simonfish/bfe8285d` (3 条 active) 断言 `coll["kind"] == "self_multi_container"`。用当前代码实跑验证: `split_owner_container("aria-runner-bot/023236f2")` (当前) 返回 `('', 'aria-runner-bot', '023236f2')`, `split_owner_container("simonfish/bfe8285d")` 返回 `('', 'simonfish', 'bfe8285d')` → 两条记录 owner 都被吞成 `''`/`unknown`, container 分别是 `aria-runner-bot`/`simonfish` → 现判 `self_multi_container`, 与测试断言一致 (故今天绿)。按 proposal D1 目标语义 (两段式正确解析 + container 主键判定): owner 变为 `aria-runner-bot` vs `simonfish` (两个不同), container 变为 `023236f2` vs `bfe8285d` (两个不同) → 按「≥2 distinct container 再看 owner, owner 不同 → cross_owner」规则, 该对必然判成 `cross_owner`。这与 proposal 自己 §What 实验表变体 C 的原文完全吻合: 「`[aria-runner-bot/023236f2, simonfish/bfe8285d]` (🔴 — 实为同一 owner 两机, 由 D-1/D-2 裁定后消解)」——proposal 作者自己已经预判了这对字符串在修复后变红, 但没有把它对应到这条具体的既有测试断言上。`grep` 确认该字符串对在同一测试文件里被至少 7 处 fixture 复用 (`grep -n "aria-runner-bot/023236f2\|simonfish/bfe8285d"`), 其中仅 line 305-341 这一处直接断言 `kind` 为 `self_multi_container` 且两条记录都是唯一/最新 active (其余复用处因 dedupe 后只剩 1 条 active, 结果为 `none`, 不受影响)。T1 只点名重写 `test_split_owner_container_variants` (`test_collision.py`), T4 只泛称「`handoff_multibranch.py` dedupe 行为随 split 变化的锁定测试」, 均未点名 `test_handoff_multibranch_collision_dedupe.py:305` 这条; SC-7 却承诺「state-scanner 测试...零回归」。这是 Spec 内部自相矛盾 (§What 实验表已预见, Tasks 未落地), 不是不可预见的实现期意外。

---

### type: issue / severity: major / category: documentation / scope: D2/T5 §2.3.7 编号冲突

**summary**: proposal 计划「新增 §2.3.7「AI runner 提交身份」」, 但 `session-handoff.md` 已有 §2.3.7 (Frontmatter content enforcement, #137); SC-5「§2.3.7 存在」在改动前即可平凡为真, 判据不具区分力。

**evidence**: 实读 `standards/conventions/session-handoff.md` 章节列表 (`grep -n "^### 2.3"`): 已存在 2.3.1 Schema 字段 / 2.3.2 YAML 示例 / 2.3.3 与 prose 共存 / 2.3.4 向后兼容 / 2.3.5 collision 类型 / 2.3.6 Layer L 区别 / **2.3.7 Frontmatter content enforcement (#137, aria-plugin v1.43.0+)** / 2.3.8 结构化 Carry-id schema。proposal `## Key Deliverables D2` 第三条写「新增 §2.3.7「AI runner 提交身份」」, 但该编号已被占用; 下一个空闲编号应是 §2.3.9。SC-5 原文「`session-handoff.md` §2.3.5 表三行 + §2.3.7 存在且与 D-1/D-2 裁定文本一致」——若字面执行, 实现者要么覆盖既有 #137 enforcement 章节内容 (破坏性、未在 Tasks/非目标声明), 要么被迫临场重新编号 (未成文的机制判断, 触及 Rule #10 边界)。且 proposal `## References` 只列 `§2.3.1 / §2.3.5 / §2.3.6`, 未提及 §2.3.7, 与 `## What D2` 正文本身不一致, 佐证这是笔误而非刻意复用编号。

---

### type: issue / severity: major / category: testing / scope: SC-6 冻结快照不可机械执行

**summary**: SC-6 依赖的「冻结快照」`.aria/state-snapshot.json` 实测被 `.gitignore` 排除、未纳入版本控制, 且每次 state-scanner 运行即被覆写, 与 memory 已记录的「基线须对 git 冻结快照跑」判据直接冲突。

**evidence**: `git check-ignore -v .aria/state-snapshot.json` → `.gitignore:18:.aria/state-snapshot.json .aria/state-snapshot.json`, 确认未受版本控制。实读该文件当前内容: `generated_at: "2026-09-05T13:11:31Z"`, 而本轮审计发起时刻 (`r1_ts`) 已是 `2026-09-05T14:01:04Z`——同一 cycle 内文件已滚动过至少一次, 说明它是随每次 scan 变化的活文件, 不是「起草日」意义上的静态快照。proposal T6/SC-6 全文都只说「对冻结快照 (本 Spec 起草日 `.aria/state-snapshot.json` 的 tracks[])」, 没有一步「把该文件复制到 git 版本控制路径」的动作; B.2 期间任何一次 state-scanner 调用 (含本容器自己或并发容器) 都会覆盖它, 届时「起草日基线」将不可复现。这正是 memory `feedback_baseline_corpus_stat_must_run_against_frozen_snapshot` 记录的同类错误: 对会随本 cycle 增长/变化的活文件做基线统计。

---

### type: issue / severity: major / category: testing / scope: cross_owner 正控测试族对真实两段式数据的覆盖缺口

**summary**: 现有全部 4 个「cross_owner 正控」测试都只用虚构三段式 `owner/container/session` 串验证, 0/154 份真实 frontmatter 是三段式; SC-2 只在 `classify()` 层补了真实两段式的 case-3, T4/SC-4 未要求端到端 (collector→dedupe→classify) 场景下用真实两段式数据验证 cross_owner 可达, 半闭合了「测试用假契约掩盖真 bug」的病根。

**evidence**: 实读并确认 `test_classify_cross_owner` / `test_classify_multiple_groups_escalates_to_cross_owner` (`test_collision.py`) / `test_real_collector_emits_cross_owner_collision` (`test_race_window.py`) / `test_both_latest_active_different_owners_still_reports_cross_owner` (`test_handoff_multibranch_collision_dedupe.py:353-382`) 全部使用 `alice/box-A/s1` / `bob/box-B/s2` 形态的三段式字符串。实测真实语料: `grep -h "^owner-container:" docs/handoff/*.md | awk -F'/' '{print NF}' | sort | uniq -c` → `12 个一段 / 142 个两段 / 0 个三段`, 与 proposal §Why 引用的 154 份统计完全一致。也就是说, 迄今唯一能触发 `cross_owner` 的既有测试路径从未对应过任何一份真实数据的形状——这正是本 Spec triage 揭出的「病根」本身 (三段式契约与真实两段式契约错位)。proposal SC-2 已在 `classify()` 直调层面补上真实两段式 cross_owner case (triage case-3), 但 T4「dedupe 行为随 split 变化的锁定测试」/SC-4 只锁 dedupe 折叠计数与 advisory 产出, 未要求一条「用真实两段式串走完整 `collect_handoff_multibranch` → dedupe → classify` 管道得到 `cross_owner`」的端到端断言。修复落地后, 如果只满足现有 Task 字面要求, 端到端路径的 cross_owner 可达性仍只由虚构数据形态的旧测试担保。

---

### type: risk / severity: minor / category: testing / scope: SC-2 同容器多 owner 场景只覆盖 2 变体, 真实数据有 3 变体

**summary**: 真实数据里同一 container 对应 3 个不同 owner 段的情形已存在 (`dev-claude: ['', simonfish, simonfishgit]`), SC-2 只用 triage case-2 (2 owner) 验证 `identity_advisories`, 未覆盖 ≥3 owner 变体下的 advisory 形状。

**evidence**: proposal §What 实验表下方明文列出 `dev-claude: ['', simonfish, simonfishgit]` / `dev-claude2: ['', simonfish]` / `023236f2: [aria-runner-bot, simonfish]` / `bfe8285d: [aria-runner-bot, simonfish]` 四组, 其中两组是 3-owner。SC-2 三条断言 (triage case-2/3/4) 全部只涉及 2 个 owner 值的组合, 没有一条对 3-owner-1-container 的 `identity_advisories[].owners[]` 内容做断言。

---

### type: risk / severity: minor / category: testing / scope: legacy 行不参与 advisory 缺专属断言

**summary**: D3 文字承诺「无 frontmatter (legacy) 行不参与」identity_advisories, 但 SC 列表没有一条把这句话变成可证伪断言; 该行为目前只是由 `classify()` 顶部既有的 `owner_container == "unknown"` 过滤间接继承 (已实读代码确认该过滤先于分组发生), 修改 D1/D2 时若过滤顺序被无意调整, 没有专属测试会捕获。

**evidence**: 实读 `aria/skills/state-scanner/lib/collision.py` `classify()` 开头: `collidable = [t for t in (tracks or []) if (t.get("owner_container") or "unknown") != "unknown"]` — legacy 行 (`owner_container` 恒为 `"unknown"`, 见 proposal 与 `handoff_multibranch.py:636/678` 的 `"owner_container": "unknown"` 写入点) 在此步即被剔除, 不会进入 T2 新增的分组/advisory 逻辑。但 SC-1..SC-7 中没有一条专门对「输入含 legacy 行时 identity_advisories 不含该行」做断言。

---

### type: risk / severity: minor / category: testing / scope: T1 既有测试重写范围表述不完整

**summary**: T1 只点名「2-part 断言按新契约改写」, 但同一函数 `test_split_owner_container_variants` 里的 1-part (`"solo"`) 断言在 SC-1 目标语义下同样需要改写 (`("","","solo")` → `("","solo","")`), Task 措辞未提及, 有被字面理解为「只改 2-part 那一行」而遗漏的风险 (风险较低, 因同函数内改动通常会被一并注意到)。

**evidence**: 实读 `aria/skills/state-scanner/tests/test_collision.py:158-164`: `assert collision.split_owner_container("solo") == ("", "", "solo")`。proposal SC-1 目标语义「零段 -> (owner='', container=<串>, session='')」应用到 `"solo"` 上得到 `("", "solo", "")`, 与既有断言矛盾, 必须一并改写, 但 T1 文本只提「2-part 断言」。

---

### type: decision / severity: minor / category: architecture / scope: Rule #6 豁免判据自评估

**summary**: proposal 将本次改动 (无 SKILL.md 指令面变动) 归入 `skill-benchmark-exemption.md` 第一行「描述性/机械」档, 走 substitute; 对照该规范 §5 已裁定样例 (`F1′-F10″ collector 代码层 → substitute`) 与本次 `lib/` + collector/renderer 纯代码改动性质一致, 判据引用成立, 未见明显误判。

**evidence**: 实读 `standards/conventions/skill-benchmark-exemption.md` §5 样例表: `state-scanner-stale-refs-false-parity` 的 collector 代码层改动 (纯代码, 无 dispatch/判定规则变化) 被裁定为 substitute。本 Spec T1-T4 全部落在 `lib/collision.py` / `lib/identity.py` / collector / renderer 的纯代码逻辑与展示字段, 不触及「在什么状态下给什么建议」的 dispatch 表 (对照同规范 v1.62.0 Phase 4 `basic-rules.md` 案例, 那才是「照跑 AB」档), 分类基本站得住; 但注意 `rule6_note` 按 Tasks 计划推迟到 B.2 才写入 (proposal 本身未在 Spec 阶段落笔), 需在 B.2 落地时确保确实引用本规范并逐 hunk 复核 (尤其 track_board.py 渲染改动)。

## Verdict

FAIL (1 Critical / 3 Major / 3 minor)

## Vote

REVISE

## 轮次记录

Round 1 (qa-engineer, convergence mode): 对 SC-1/SC-2/SC-3/SC-4 的「对当前代码先红」断言逐条实跑验证 (`split_owner_container` / `classify()` 五个 triage case / `get_container_id` label 陷阱复现 / `dedupe_latest_per_track_container` 同容器异 owner 折叠) —— 全部属实, 无恒绿断言。真实语料复核 (154 份 frontmatter 分段统计) 与 proposal 数字一致。核心发现是 Critical 1 条: proposal 自己的实验表已预判某具体 owner-container 对修复后翻转为 cross_owner, 但该预判未落到 Tasks 里对应到具体会破的既有测试断言上, 使 SC-7 的「零回归」承诺在当前 Task 范围内不成立。另有 §2.3.7 编号冲突与 SC-6 冻结快照未版本控制两条 Major, 均为可在 Spec 文本层面直接修正的缺陷, 未触及架构性返工。
