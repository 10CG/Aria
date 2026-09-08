---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-07T01:16:38.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [qa-engineer]
---

# post_spec R2 单席报告 — qa-engineer (handoff-multibranch-subdir-path-fidelity)

席位透镜: 可证伪性 (每条 SC 过反事实) · hermetic case 可构造性 · 既有测试与冻结语料受影响面 · 负向测试缺口 · 已知失败项处置。本席为新席位, 不继承 R1 结论; 全部结论对 `301641b` 副本实读 + 临时仓实跑复核。本轮**只审不改**, 工作区零改动 (`git status --short` 空)。

## 审计结论

### Decisions

- [minor] testing/R1 critical·major 落地复核: R1 的 2 critical + 15 major 逐条复核, **均落进正文而非批注**。抽验: SC-10 基线数已改 78 且写明真仓 checkout 口径 (本席在插件缓存 `tests/` 复跑同一条命令得 `Ran 78 tests … OK`); `_check_handoff_ancestry` 三处已改 `_same_branch_head_unreachable_tracks` (证据: scan.py:126 定义 / :186 拼串); §What.2 的 mv 归因已重写为「空串→真日期 + frontmatter 分支」; SC-8 拆前后半; SC-9 补 (b); 新增 SC-13/14/15; Task 5.1 展开主仓版本引用面; 头部「主仓实况」行作废旧 gitlink 表述。(证据: proposal.md:9-15,224-237 · scan.py:126,186)
- [minor] architecture/事实底座 hermetic 复验: 五项独立实测与 §Why / SC-4 陈述一致 —— (1) 子目录件今天产 `handoff_multibranch_git_show_failed` + 假 legacy 行且 `updated_at` 为空; (2) 非 ASCII 名被 `git ls-tree` 整条加引号, `Path(path).name` 带尾引号, 在 `.endswith(".md")` 处静默丢弃, 不进 tracks 也不报错; (3) 顶层与 `archive/` 两个 `latest.md` 今天都已被排除; (4) 同名不同目录两行逐字段相同 (归档副本读到顶层内容); (5) mv 过的无 frontmatter 文件在旧 basename 路径 / 新相对路径 / `--follow` 三种写法下都返回 mv 提交日 `2026-08-15T12:00:00+00:00`。(证据: handoff_multibranch.py:277-288,301,321,637-658)

### Issues

- [critical] testing/SC-15 子目录布局 fixture 组成: SC-15 是 A′ 裁定 (v3 增量) 唯一的端到端验收, 但它没钉死子目录 fixture 的组成。照字面「**唯一 active track 的文件在 `archive/`**」只放子目录件时, `collect_handoff` 的 `canonical_files` 为空 ⇒ 在 `handoff.py:438-451` 提前返回, **根本不解析 pointer**。后果两条: (a) 断言 (e)「`errors[]` 不含 `handoff_pointer_target_missing`」在**有守卫与无守卫下都绿**, 其反事实「去掉守卫 ⇒ (e) 因该 soft_error 出现而红」被证伪; (b) 断言 (f)「`handoff.exists` 与 `tracks_multibranch.exists` 不互相矛盾」在修好路径后**恒红** —— 子目录件变成真 track 使 `tracks_multibranch.exists=True`, 而 `_scan_md_files` 非递归使 `handoff.exists=False`, 守卫对此无能为力 (它只管 latest.md 写什么)。hermetic 实测 (subdir-only + 指向 `archive/x.md` 的 latest.md): `handoff.exists=False`, `latest_source=None`, **soft errors=[]**。必须把 fixture 明确成 §5 的 sub-case (a)「子目录 active + 顶层另有非 active .md」, 否则该 SC 同时携带一条恒绿断言与一条不可满足断言, 而 (f) 恒红正是「改断言就范」的诱因。(证据: proposal.md:237 · handoff.py:300,318,438-451)
- [major] testing/SC-13 legacy dedupe 反事实: SC-13 的「`dedupe_latest_per_track_container` **不折叠**」断言与其反事实「沿用 basename ⇒ 两行同 id ⇒ 折叠成一条 ⇒ 红」被代码直接证伪。`status == "legacy"` 的行在 `handoff_multibranch.py:521-524` 被 `continue` 掉、**从不进入分组**, 所以两条 id 完全相同的 legacy 行今天也不会折叠 (实测: 2 行进 → 2 行出, `legacy_passthrough=2`)。该行为在 docstring `:493-499` 与 `state-snapshot-schema.md:1128` 都是明文契约。连带 §What.2 第三条 (proposal.md:113)「今天会产生同一个 `legacy:<branch>:x.md`, **被 `dedupe_latest_per_track_container` 当成同一 track 折叠**」是事实错误 —— 前半对, 后半不成立。SC-13 尚靠「两条不同 `track_id`」那半保住 baseline-failing 资格, 但 rule6_note 把它列进 substitute 实体时依据的是被证伪的那半。(证据: proposal.md:113,235 · handoff_multibranch.py:521-524,493-499 · state-snapshot-schema.md:1128)
- [major] architecture/§5 消费方枚举与闸门面结论: §5 与 rule6_note 的「闸门面 (`SKILL.md:149`/`:153`) 不受影响」只算了**删掉的假 legacy 行** (owner_container 恒 unknown, 被 `lib/collision.py:483-486` 的 collidable 过滤排除), 没算**新增的真 track** —— 路径修好后子目录里带合法 frontmatter 的交接会带着真 owner_container 进入 collidable。hermetic 实测: 同一 track_id 下「顶层 simonfish/… active + `archive/` aria-runner-bot/… active」在今天是 `collision.kind = none`, 修好后是 `cross_owner` (groups 两个成员)。`collision.kind` 非空正是闸门触发条件本身。同时 §5 的枚举表漏了三类消费方: `phase-d-closer/references/handoff-mechanics.md:116-121` 的 D.3 pointer 决策表 (读 `exists` / `len(tracks)` / 「其他 container 有 status==active」, 三个量本 spec 全动)、`references/rules/advanced-rules.md:443-444,511-512,544` 与 `RECOMMENDATION_RULES.md:28,31` 的推荐规则 1.51/1.54 触发条件、`phase-d-closer/scripts/fetch_gate.py:175-188` (吃 `collision_kind` 出 verdict)。(证据: proposal.md:146-155,243 · lib/collision.py:480-486 · handoff-mechanics.md:116-121 · advanced-rules.md:443,511,544)
- [major] documentation/rule6_note 套件覆盖实测证据: 头部 Rule #6 判定行与 rule6_note 都写「`ab-suite/state-scanner.json` 对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` 四词**零命中**」。现测 `tracks_multibranch` **命中 1 处** (`aria-plugin-benchmarks/ab-suite/state-scanner.json:214`, case `id=13` `a1-heartbeat-on-entry-TARGETED`), 由 commit `5697477` (2026-09-05 14:12 UTC, HEAD 的祖先) 加入; 文件在该 commit 前后为 15518 B → 17551 B, 而 R1 决策条目记的正是 **15518 B** ⇒ R1 四席与本 spec 都是对**改前副本**测的。结论 (substitute) 本席复核后仍可成立 —— 该 case 的承重期望 (C) 逐字写「触发条件**不依赖** collision.kind」, 测不到本 collector 的行为面; 但证据必须重测重写, 且须与上一条 (collision.kind 会翻转) 一并重做「照跑 vs 豁免」的判定 (CLAUDE.md Rule #6「拿不准 → 照跑」/ Rule #10 不得以价值评估自行豁免)。(证据: proposal.md:12,244 · ab-suite/state-scanner.json:214 · commit 5697477)
- [major] testing/SC-1·SC-5·SC-14·SC-15 的 `errors[]` 指代: 本 collector 有两个同名 error 面, 而 SC 表全部裸写 `errors[]`。`tracks_multibranch.errors[]` (= `r.data["errors"]`, `handoff_multibranch.py:753`) 只装**消息串**, soft_error 的 kind 只进 `CollectorResult.errors` (`_common.py:312-313` 的 `{"error": kind, "detail": …}`), 最后由 `scan.py:382-383` 汇进顶层 `errors[]`。实测 `data["errors"][0]` = `"[master/…] git show failed: git show failed for origin/master:docs/handoff/… (other, rc=128)"` —— **不含** `handoff_multibranch_git_show_failed` 字面。按 §Why/§4 的上下文, 实施者最可能把 `errors[]` 读成前者, 于是 SC-5 的「`errors[]` **含** `handoff_multibranch_git_show_failed`」不可满足 (恒红), SC-1 的「**无**」在 `301641b` 上即为真 (恒绿, 违反 Task 1.2「对 301641b 全红」)。SC-15 (c)(e) 又指的是 `collect_handoff` 的 `CollectorResult.errors` (其 `data` 根本没有 errors 键), 同一张表里两种含义。(证据: proposal.md:223,227,236,237 · handoff_multibranch.py:753 · _common.py:312-313 · scan.py:382-383)
- [major] testing/SC-12 子目录仓半条: 两处失效。(1) 断言「soft_error 里…也无 `handoff_pointer_target_missing`」在全子目录布局下**结构上不可能产生** (同 critical 条: `handoff.py:438-451` 提前返回), 属恒绿断言; 若改成有顶层旧件的布局才有鉴别力, 但 SC 未写。(2) 「**断言 exit 0**; 若实跑非 0, 逐条抄下 kind 并在 handoff 说明 (不得改断言就范)」—— 失败模式是「记录」不是「转红」, 该半条因此不是验收判据。建议改为: 顶层布局断言 exit 0, 子目录布局只断言「不出现 `handoff_multibranch_git_show_failed`」并把 pointer 相关断言全部让给 SC-15。(证据: proposal.md:234 · handoff.py:438-451 · scan.py:431)
- [minor] documentation/A→A′ 切换后的下游漂移: Impact.Risk 第 1 条与 §5 dedupe 行都已标「(仅 A 案)」/「A′ 案下无此面」, 但 Task 3.2 (dedupe tie-break 现状钉测) 与 Task 4.1 里的 `schema:1125` 论据订正仍是无条件必做项, 而其唯一理由「相对路径下 `archive/` 的 `a`=0x61 字典序大于数字」在 A′ 下不成立 —— A′ 的 `filename` 恒为 basename, `:1125` 那句 (「`YYYY-MM-DD-` 前缀 ⇒ 字典序大者即更晚」) 依然为真。同时 SC-7 要求的两行 (`2026-07-19-x.md` vs `archive/2026-07-19-x.md`) 在 A′ 下 collector 永远造不出来, 只能手搓 dict。留着不算有害 (dedupe 键与 track_board 共享), 但理由需改写, 否则 Phase B 会照一个已失效的前提改 schema。(证据: proposal.md:153,188,207,209,229 · state-snapshot-schema.md:1125)
- [minor] documentation/schema :1136 fail-soft 形状既存 drift: Task 4.1 要把 `unreadable_count` 补进 `state-snapshot-schema.md:1136`, 而同一句里 `collision` 写作 `{"kind": "none", "groups": []}`, 与代码 `handoff_multibranch.py:593` 早退实际返回的 `{"kind","groups","identity_advisories"}` 已不一致 (identity_advisories 在 CHANGELOG 里标「恒存在」)。本 spec 正是为「恒存在不变量在错误路径上要成立」才动这一行, 只补一半会留下另一个错误形状。(证据: proposal.md:142,209 · state-snapshot-schema.md:1136 · handoff_multibranch.py:593)

### Risks

- [minor] architecture/latest_md_writer 生产调用面: §5 / §2.5 / Impact.Risk 用「D.3 写出 `[archive/x.md](./archive/x.md)` 后…」的既成时态描述失败面, 但 `write_latest_md` 在全插件树**只有测试调用方** (`tests/test_p1_layer_h.py`), 且 `references/phase-1-collectors.md:95-99` 逐字记录了「deliberately D.3-scoped — 不在 scan.py 内自动触发, **不在 P1 内引入 production call-site**; D.3 集成由 TASK-029 或独立 follow-up 承担」; phase-d-closer 今天的 latest.md 维护走的是 `handoff-mechanics.md:102-131` 的人工两子步骤。⇒ 这条「新失败面」的部署可达性远低于文中口径, SC-15 的「端到端」实为测试内三步管道。这不推翻加守卫的决定 (writer 一旦接线即命中), 但**直接影响待复议 2 请 owner 追认的代价陈述** ——「子目录采用方本轮只拿降级 pointer」这个代价目前无人在付。建议在待复议 2 与 §2.5 各加一句可达性说明。(证据: proposal.md:131,151,189 · phase-1-collectors.md:95-99 · handoff-mechanics.md:102-131)

## Verdict

**FAIL** — Critical 1 / Major 5 / Minor 3 (另 2 条 decision 不计入缺陷计数)。

rationale: 唯一一条 Critical 落在 **v3 增量自己的验收判据**上 —— SC-15 是 A′ + 写侧守卫这次 AI 裁定的唯一端到端验收, 而它的子目录布局按字面构造时, 一条断言 (e) 恒绿 (其反事实被 `handoff.py:438-451` 的提前返回证伪), 另一条断言 (f) 恒红 (守卫管不到两个 collector 的 `exists` 自相矛盾, 该缺口已被本文自己推给 Task 5.3 的另开 issue)。也就是说: **本轮新增的机制, 其验收既抓不住机制缺失, 又要求实现做到方案明说不做的事**。两者都是 hermetic 实跑判定, 不是推理。

5 条 Major 分三类, 都可在 Phase A 内改 spec 消解, 不动方案骨架:

1. **判据可证伪性** (3 条): SC-13 的反事实被 dedupe 的 legacy 透传契约证伪; SC-1/5/14/15 的裸 `errors[]` 在两个同名面之间摇摆, 一边恒绿一边不可满足; SC-12 子目录半条既含恒绿断言又含「失败就记录」的非判据式失败模式。
2. **影响面事实错误** (1 条): §5 与 rule6_note 判「闸门面不受影响」只算了删掉的行、没算新增的真 track; 实测 `collision.kind` 在子目录仓从 `none` 翻到 `cross_owner`, 而这正是闸门触发条件本身, 另有三类消费方 (D.3 pointer 决策表 / 推荐规则 1.51·1.54 / fetch_gate) 未入枚举表。
3. **Rule #6 证据链** (1 条): 「四词零命中」取自 2026-09-05 之前的套件副本 (15518 B vs 今 17551 B), 现测 `tracks_multibranch` 命中 1 处。结论仍可成立, 但按 Rule #10 该判定不能建立在已知为假的证据上, 须重测重写并与第 2 类一并复判「照跑 vs 豁免」。

正面记录 (不因 FAIL 抹掉): R1 的 2 critical + 15 major 本席逐条复核**全部落进正文而非批注**, 且未发现「改一处引入另一处矛盾」的回填错误; 事实底座五项 hermetic 复验全部成立 (假 legacy / 静默漏扫 / pointer 任意深度 / 同名串读 / mv 日 `--follow` 不救); SC-10 的 78 与「真仓 checkout 零失败」口径本席复跑确认, R1 那条 conflicted 的已知失败豁免已被正确删除; 冻结语料 `tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 与 `.aria/repro/` 两份实测存在, §7「不需重生成」的前提成立。本轮缺陷集中在**新增机制的验收强度**与**影响面枚举的完备性**, 不在调研质量。

计算依据:
- Critical: 1 (1 issue + 0 risk)
- Major: 5 (5 issue + 0 risk)
- Minor: 3 (2 issue + 1 risk)
- Decisions (不计入): 2

## 轮次记录

### Round 2

- Agents: qa-engineer (本报告为五席之一的单席产出)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 9 findings (1 critical / 5 major / 3 minor) + 2 decisions
- Vote: **REVISE**
