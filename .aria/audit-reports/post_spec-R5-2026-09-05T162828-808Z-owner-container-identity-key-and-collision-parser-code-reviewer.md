---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-05T16:28:28.808Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 (max_rounds, 最后一轮) — code-reviewer 席 (v5 定点编辑稳定性 + 规格合规终检)

审计对象: `openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md` **v5** @ `681e872` (151 行)。只审不改, 未修改任何仓内文件。本轮实读: `git diff addc8a1..HEAD -- proposal.md` 全部 17 个 hunk、proposal v5 全文、本席 R4 报告与 R4 聚合; 代码锚点: `track_board.py` :738-760 / :778-797 (`tracks_by_tid` 建于 :789-793, `_render_collision_lines(verdicts, tracks_by_tid)` :796)、`handoff_multibranch.py` :516-524 (dedupe 键) / :546 (`def collect_handoff_multibranch`) / :705-716 (`deduped_tracks` :709, classify :714)、`collision.py:127` (`phase = track.get("phase")`)、`identity.py:220-224` (`return label if label else uuid` :222)、`phase1_gate.py` :18/:352/:465 (`raw_track_id`)、`RECOMMENDATION_RULES.md:31`、`test_handoff_multibranch_collision_dedupe.py` :208 (`def _build_repo`) / :360-361 / :1030-1031 (`box-A` 夹具)、`aria/templates/session-handoff.md:43` (「设 label 使更可读」)、a1-entry proposal :104 / :183-195 (§2.1b carry-id 契约 + `--raw-track-id`)、七处消费文档三 token 逐文件 `grep -c`。

## R4 处置核对

| R4 编号 | 三态 | 依据 (v5 实读) |
|---|---|---|
| R4-m1 头部计数 / `constants.py` 口径 / 行号 | **partial** | :103 改「14 个 checkbox 含 T3b」(`grep -c '^- \[ \] T'` = 14 ✓), 头部加「`lib/constants.py` (条件 T13)」✓, :148 改「:374-379 注释 / :379-383 代码」✓; **未动**: :8 代码落点仍把 `lib/constants.py` 列为无条件项 (见 R5-m3) |
| R4-m2 SC-5 反向 token 加三 | **closed** | :126 反向名单增 `Kairos` `DEC-2026` `10cglocal` ✓; 同时加 `仅用于` / `§2.3.8.2` 正向 token, 与 D2 :41 新增限定句逐字对应 ✓ |
| R4-m3 SC-3 S1 臂 lock-in 断言 | **closed** | :124 新增「**仅 S1**: lock-in 断言 `get_container_id()` 在 label 非空时仍返回 label」; 与 `identity.py:222` 现值一致; 与 Impact :100「S1 不 flip」/ Rule #6 :101「flip 臂仅 S2」口径一致 ✓ |
| R4-m4 SC-9 量词歧义 / `RECOMMENDATION_RULES.md:31` | **partial** | :130 改为「交集不为空」+ 显式说明 `RECOMMENDATION_RULES.md:31` 今日无取值字面、加 `identity_advisories` 一句后满足 ✓ (量词歧义消除); 但量词作用域从 v4 点名的五文件扩成「七处文档 … 每个文件 F」, 把 `aria/templates/session-handoff.md` 也纳入, 该文件三 token 全零且 D4 对它的改动 (示例 uuid 形 + 删鼓励句) 不会引入任何一个 token ⇒ 断言对第七处恒不成立 (见 R5-m1) |

计数: **closed 2 / partial 2 / open 0**。两条 partial 都是文字作用域 / 一处条件标注, 不动设计。

## 本轮镜头逐 hunk

1. **Status 行** (:4): 「R4 三席 PASS / qa 与 km 各 1-2 条 Major」与 R4 聚合 (QA 0C/1M, KM 0C/2M) 一致 ✓; 「R1..R4 聚合见 §References」—— References :146 仍写 `R{1,2,3}`, 未随本 hunk 更新 (R5-m2)。
2. **D1 族键段** (:35): 新增作用域句「只改 Layer H `ClaimRecord.track_id` 用于 §2.3.5 分组; 不改 frontmatter 原串 / 不影响 §2.3.8.2 / 不触及 Layer L」+ 「`tracks_by_tid` 须用同一剥离后键 (T8)」。代码核对: `track_board.py:789-793` 用原始 `t.get("track_id")` 建索引, `verdicts` 键来自 `claim_records` 的 `track_id` (:783 经 `_track_to_claim_record`), D-0(a) 剥离后两键域确实分叉 ⇒ 该句为真、T8 :113 与 Risk (7) :98 三处一致 ✓。
3. **D2 §2.3.1 句** (:41): 显式限定文本与 SC-5 :126 新增 token `仅用于` `§2.3.8.2` 对得上 ✓; 与 D-0(a) :71「不改 a1-entry 契约」一致 ✓。
4. **D4 模板条** (:51): 「删除示例旁鼓励句」—— `aria/templates/session-handoff.md:43` 实存 `(label 空 → uuid; 设 label 使更可读)` ✓ 落点真实。
5. **D5** (:54): 改「版本档位」+ 引 CLAUDE.md 原句 + 「判据上 PATCH; owner 可升 MINOR (二选一记入 CHANGELOG)」。T12 :117 仍写死「aria-plugin PATCH bump」, 与 D5 的二选一口径不同步 (R5-m3)。
6. **D-0(b) 后果** (:72): 新增「§2.3.8.2 同串 ⇒ carry-id 也须去容器段, 与 a1-entry 用 carry-id 喂 `phase1_gate --raw-track-id` 相冲, 对方要连带改 §2.1b」。a1-entry proposal :104 (`--raw-track-id "<spec-slug>-<container_uuid>"`) 与 :183-195 (§2.1b「A.1 原串即 carry-id」, D.2b `release_gate.py --raw-track-id <A.1 原串>`) 实读成立 ✓; 四选项后果对称性未被破坏 ✓。
7. **Risk (7)** (:98): 加 `tracks_by_tid` 退化 + 「T8 锁」, 与 hunk 2 / T8 同源 ✓。
8. **Tasks 头** (:103): 「6 个 .py + `lib/constants.py` (条件 T13)」—— 6 = collision / identity / handoff_multibranch / track_board / phase1_gate / release_gate ✓; 「14 个 checkbox 含 T3b, T9 / T13 条件」✓ 实数 14; SC checkbox 11 与 SC-1..SC-11 ✓。
9. **T6** (:111): 加 `phase` 为第八字段, 理由「被 `track_to_claim_record` 读取」—— `collision.py:127` 确实读 `track.get("phase")` ✓ (v4 七字段 fixture 会让 ClaimRecord.phase 恒空, 本 hunk 修的是真缺口)。
10. **T8** (:113): 「D-0(a) 时 `tracks_by_tid` 改用剥离后键 (与 `verdicts` 键域一致)」与 hunk 2 ✓。
11. **SC-2 advisory 臂** (:123): 区分「函数级反事实」与「生产接线端到端」; 夹具点名 `_build_repo` 风格 + uuid 形容器 `aaaa1111` 而非 `box-A` (`test_handoff_multibranch_collision_dedupe.py:208` 存在 `_build_repo`, :360-361 / :1030-1031 现用 `box-A` 是主机名形 ⇒ identity_key 含 owner 段 ⇒ advisory 恒空, QA R4-M1 的诊断成立) ✓; 接线反事实「`:709` 传 `deduped_tracks` → 0」—— `:709` 即 `deduped_tracks, dedupe_stats = dedupe_latest_per_track_container(tracks)` ✓ 行号与变量名逐字命中。**精度缺口**: dedupe 键 (`:518-522`) 是 `(track_id, owner, container)` 改后 `(track_id, identity_key)`, 只在**同 track** 内折叠; 该端到端夹具的「两份 handoff 两串」若落在不同 `track_id`, 反事实分支 advisory 仍为 1, 断言「→ 0, 红」不成立。SC-2 未写「同 track_id」(R5-m4)。
12. **SC-3** (:124): 三臂 (共同 / 仅 S1 / 仅 S2) 与 D1 :37-38、T3 :107、T3b :108、Impact :100、Rule #6 :101 六处口径一致 ✓; Rule #6 点名「SC-3 (S1 臂; flip 臂仅 S2)」与 SC-3 拆分一致 ✓。
13. **SC-5** (:126): 见 R4-m2 ✓。
14. **SC-6** (:127): 「D-3(a) 读常量 / D-3(b) 常量不存在, 测试自带 30 天字面, 改后组数 2 而非 0」与 D-3 :89-90 两选项后果一致 ✓, 与「改后 = 2 组 (D-3(a) 时 0 组)」自洽 ✓。
15. **SC-9** (:130): 见 R4-m4 partial / R5-m1。
16. **SC-11** (:132): grep 断言具体化为「`updated_at` 与天数比较的表达式在 collector / renderer 各零处, 只在 lib 一处; 同义改名绕过属 B 期 review 责任」✓ 可机械执行。
17. **References 代码行** (:148): 「:374-379 注释 / :379-383 代码」✓ (R4 实读)。

**规格合规终检**: Linked Issue :6 单 code span、`, ` 分隔、行首无空白 ✓; 带圈数字 / 希腊字母 `grep -P` 全文零命中 (exit 1) ✓ (🔴🟡⚪ 为 collision 等级约定符, 不在禁用集); Level 段 :3 「判据上 Level 3」与「owner 维持 Level 2 = 显式 override (Rule #10)」并列、未替 owner 裁 ✓; Rule #6 :101 点名集 SC-1 / SC-2 / SC-3 (S1 臂) / SC-4 / SC-8, 其中 SC-3 S1 臂现在含 lock-in 断言 (S1 下先红: `get_container_label` 不存在 + 两 gate 无告警; lock-in 本身基线绿但作为守卫臂随 S1 臂一起落) ✓; R4 聚合 12 条 minor 逐条在 v5 找到落点 (checkbox 14 / constants 条件 (Tasks 头) / 行号 / SC-5 三 token / SC-3 S1 lock-in / SC-9 量词 / `tracks_by_tid` (D1+T8+Risk) / SC-3 S2 宿主「发布脚本/清单断言」/ SC-6 常量作用域 / D5 引原句 / D-0(b) §2.3.8.2 / T6 `phase` / SC-11 改名成文) ✓。

## 审计结论

### Critical

无。

### Major

无。

### Minor

**[R5-m1] SC-9 量词作用域扩到第七处 `aria/templates/session-handoff.md`, 该文件三 token 恒零, 断言对它不可满足** (R4-m4 修法引入)
- type: issue / severity: minor / category: testing / scope: proposal:130 vs :51 / `aria/templates/session-handoff.md` 全文
- evidence: v4 SC-9 点名五文件; v5 改为「七处文档 … 每个文件 F 与 token 集 {`cross_owner`, `self_multi_container`, `identity_advisories`} 的交集不为空」。`grep -c` 实测: 模板三 token 均 0; SKILL.md `self_multi_container`=1 (交集非空, 可过); `RECOMMENDATION_RULES.md` 三 token 均 0 (proposal 已成文「加一句后满足」)。D4 :51 对模板的改动只是示例 uuid 形 + 删鼓励句, 不会也不该引入任何 kind token ⇒ 机械断言对模板恒红, 或迫使 B 期往模板塞无关 token。
- 修法: 量词范围写成「除 `aria/templates/session-handoff.md` 外的六处」, 或恢复 v4 的显式文件名单 (五处 + SKILL.md)。一句话, B 期顺手。

**[R5-m2] References 审计行未随 Status 行更新**
- type: issue / severity: minor / category: documentation / scope: proposal:4 vs :146
- evidence: :4 「R1..R4 聚合见 §References」; :146 仍是 `post_spec-R{1,2,3}-…-aggregated.md`; R4 聚合文件实存 (`post_spec-R4-2026-09-05T155052-857Z-…-aggregated.md`)。
- 修法: :146 改 `R{1,2,3,4}` (R5 落地后再加 5)。B 期顺手 (或 owner 批准时一并回填)。

**[R5-m3] 两处口径未随 v5 同步: :8 `lib/constants.py` 无条件 (R4-m1 残留); T12 写死 PATCH 而 D5 改为二选一**
- type: issue / severity: minor / category: documentation / scope: proposal:8, :117 vs :54, :103
- evidence: :103 已写「`lib/constants.py` (条件 T13)」, :8 代码落点仍把它与六个无条件 .py 并列; D5 :54 改为「判据上 PATCH; owner 可据此升 MINOR (二选一记入 CHANGELOG)」, T12 :117 仍是「aria-plugin PATCH bump」—— 若 owner 裁 MINOR, T12 字面与 D5 冲突。
- 修法: :8 `lib/constants.py` 后加「(D-3(a) 时)」; T12 改「按 D5 裁定档位 bump」。B 期顺手。

**[R5-m4] SC-2 生产接线端到端夹具缺「同 `track_id`」限定, 接线反事实的「→ 0, 红」只在同 track 成立**
- type: issue / severity: minor / category: testing / scope: proposal:123 (advisory 臂「生产接线端到端」句) vs `handoff_multibranch.py:518-522`
- evidence: dedupe 键改后为 `(track_id, identity_key)`, 只折叠同 track 的同身份行。「两份 handoff 两串 (`alice/aaaa1111` / `bob/aaaa1111`)」若写成两个 track, `deduped_tracks` 仍含两行, 反事实分支 advisory 仍恰 1, 「接线反事实 → 0」不红, 该端到端锁退化为只锁字段存在。函数级反事实那句 (「同 uuid 容器两串跨两份 handoff, dedupe 折叠后仍恰 1」) 隐含同 track, 但端到端句未继承这个前提。
- 修法: 句中加「同 `track_id`」四字。B 期写夹具时必然会撞到 (反事实不红即发现), 故为 minor。

### 核验通过、不构成 finding

- 17 个 hunk 逐一与全文对照: 除上列四条文字口径外, 无新矛盾; 判定模型 (D1 三条确定性规则 + 实验表) 自 v3 逐字未变。
- `tracks_by_tid` 分叉 (D1 / T8 / Risk (7)) 经 `track_board.py:783` vs `:789-793` 实读成立; T6 `phase` 字段经 `collision.py:127` 实读成立; D-0(b) 新后果经 a1-entry :104 / :183-195 实读成立; SC-2 端到端夹具点名的 `_build_repo` / `box-A` / `collect_handoff_multibranch` / `:709 deduped_tracks` 四个锚点逐字命中。
- 计数: T checkbox 14 / SC 11 / 6 个 .py / 七处文档 / 1 处代码消费方 全部与正文一致 (:8 条件标注除外, 已入 m-3)。
- Linked Issue 格式 / 带圈数字与希腊字母零命中 / Level 段 Rule #10 姿态 / Rule #6 点名集与 SC-3 三臂一致 / R4 聚合 12 条 minor 全部有落点。

## Verdict

**PASS** — 0 Critical / 0 Major / 4 Minor。

R4 本席 4 条: closed 2 / partial 2 / open 0; 两条 partial 残留 (:8 条件标注、SC-9 作用域) 已并入本轮 m-3 / m-1。v5 的 17 个定点 hunk 没有引入任何影响判定模型、决策点集合、Rule #6 substitute 集或 S1/S2 口径的矛盾; 四条 minor 全是一处文件名单 / 一个引用范围 / 两处口径同步 / 四个字的前提限定。

## Vote

**PASS**。理由: 无 Critical / Major; 四条 minor 都不影响 owner 对 D-0 ~ D-3 的裁定基础, 也不影响 B.1 入口; 其中 m-1 / m-4 会在 B.2 写 SC-9 / SC-2 测试时被机械暴露 (断言恒红 / 反事实不红), 不存在静默假绿风险。**B 期顺手项清单**: (1) m-1 SC-9 量词范围排除模板 (或恢复显式名单); (2) m-2 References :146 加 R4 (与 R5); (3) m-3 :8 `lib/constants.py` 加条件 + T12 改「按 D5 裁定档位」; (4) m-4 SC-2 端到端句加「同 `track_id`」。

## 轮次记录

- R1 (code-reviewer): 0C/4M/5m, PASS_WITH_WARNINGS / REVISE。
- R2 (code-reviewer): 0C/2M/4m, PASS_WITH_WARNINGS / REVISE —— 等价类无数据通路 + 零 baseline-failing SC。
- R3 (code-reviewer): 0C/3M/7m, PASS_WITH_WARNINGS / REVISE —— D-0(a) 语料子句 / S1 缓解声称 / D-3(a) 零落点。
- R4 (code-reviewer): 0C/0M/4m, PASS / PASS —— 规格合规终检 + v4 内部一致性。
- R5 (本轮, max_rounds; 镜头: v5 定点编辑稳定性 + 规格合规终检): 实读 `addc8a1..681e872` 全部 17 个 hunk + proposal 151 行 + R4 本席与聚合 + 上列 12 处代码/测试/文档锚点; 逐 hunk 对照 Tasks / SC / Impact / 决策点; 计数 14/11/6/7/1 核对; Linked Issue / 符号 / Level / Rule #6 点名集终检。R4 处置 closed 2 / partial 2 / open 0; 新 0C/0M/4m; **PASS / PASS**。比较键与 R4 不重叠 (R4 四 minor 承载体均已改写, 本轮 m-1 / m-3 是其修法的残留而非复发), 非振荡; 连续两轮 0C/0M, 收窄至文字口径级。
