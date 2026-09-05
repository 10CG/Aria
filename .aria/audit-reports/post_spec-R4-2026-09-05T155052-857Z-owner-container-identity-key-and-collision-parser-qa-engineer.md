---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T15:50:52.857Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R3 处置核对

方法: 对我 R3 报告 (`.aria/audit-reports/post_spec-R3-2026-09-05T150825-299Z-owner-container-identity-key-and-collision-parser-qa-engineer.md`) 的 4 条 Major 逐条核对 v4 文本, 并对其中可机械验证的部分实跑复现 (真实源码 `aria/skills/state-scanner/lib/collision.py` / `scripts/collectors/handoff_multibranch.py` / `scripts/renderers/track_board.py` — 均未改动, 只读; 补丁落 scratchpad `v3repo/` 不改仓内文件; 冻结语料 `.aria/repro/handoff-tracks-frozen-2026-09-05.json`)。

- **R3-Major-1 (SC-7/SC-8 恒存在与两条既有严格断言测试冲突, 且未点名)**: **闭合**。v4 T2 明文点名 `改写 test_real_collector_emits_cross_owner_collision / test_real_collector_no_collision_is_none 的 keys == {kind, groups} 断言`。实读这两条测试 (`test_collision.py:261-290`) 确认它们正是我 R3 指出的两条穷举键测试。实跑复现: 把 collector 补丁改为 v4 字面「`collision["identity_advisories"] = _drift_advisories` 恒执行 (不判空)」, 对真实 `aria/skills/state-scanner/tests` 全量 1492 个 test 跑一遍 (方法见下「审计结论」T10 一节), 新增失败集合精确等于 `{test_split_owner_container_variants, test_real_collector_emits_cross_owner_collision, test_real_collector_no_collision_is_none, test_both_latest_active_still_reports_self_multi_container}` 四项——与 T1/T2/T4 点名清单逐一对应, 零遗漏未点名项 (4 项均可在任务文本中找到对应点名)。按 T2 文本把这两条测试的 `keys` 断言改为 `{"kind","groups","identity_advisories"}` / 字典整体改为含 `identity_advisories: []` 后重跑, 两条转绿, 且未产生新的次生失败。
- **R3-Major-2 (D3 漂移 advisory「dedupe 前调用」这一接线顺序无端到端结构化判据锁定)**: **部分处置, 窄化重开** (详见下「审计结论」新增 finding 一, 与 R3-Major-2 同根同源, 未视为独立新问题)。v4 在 SC-2 文本本身新增了函数级反事实 (「同 uuid 容器两串跨两份 handoff, dedupe 折叠后 advisory 仍恰 1 (反事实: 对 deduped 调用 → 0)」), 这是真实进展, 直接堵死了 R3 复现的「先跑 dedupe 再传给 `identity_drift_advisories()`」这类函数级坏实现。但该反事实句在 SC-2 原文里没有携带判定臂那句「端到端(collector 夹具 → dedupe → classify)」限定词, 而 SC-8 的恒存在断言与 T2 点名改写的两条「真实 collector」测试都用非 uuid 容器 (`box-A`/`box-B`) 夹具, 天生不会触发漂移信号。三者叠加的结果是: 按 SC-2/SC-8/T2 字面要求写的测试集, 完全可以从不曾用 uuid 容器夹具跑一次真实 `collect_handoff_multibranch()` 来检验 `:709` 处到底传的是 `tracks` 还是 `deduped_tracks`——即生产接线本身仍未被锁定, 只是「函数本身对不对」被锁定了。R3 指出的核心风险 (接反了会被全绿放过) 因而只是从「函数级」收窄到了「仅剩生产接线一处未锁」, 没有完全闭合。
- **R3-Major-3 (D-0(a) 剥尾安全防护子句缺反例夹具, 冻结语料现成的 `-20260719` 日期戳会撞上未测到的坏实现)**: **闭合**。v4 T9 与 SC-2 都明文要求新增 `x-20260719 剥后与语料零碰撞` 与 `slug-abcdefg 不剥` 两条夹具, 与我 R3 指出的确切场景 (`aria-plugin-113-gate-result-yaml-20260719`) 完全对应。此条为 D-0(a) 条件成立 (D-0 仍待 owner 裁定), 但只要选 (a), 该反例已被点名钉入 SC 文本。
- **R3-Major-4 (SC-6「归因表由测试计算」缺可执行判据, 且冻结语料上「真撞车」档零正样本)**: **闭合**。v4 SC-6 新增明确机械规则: 「组内全部行 `updated_at` 早于 `LAYER_H_ACTIVE_WINDOW_DAYS` (缺省 30) → `stale(#182)`; 否则按 `kind` 归 真撞车/同人多机」, 并要求「注入的合成真撞车组必须归入真撞车」正面堵死「把所有组都标 stale」的坏实现 (若坏实现无视日期一律判 stale, 新注入的、经过特意构造为「近期」的真撞车组会被该断言直接抓到)。实跑核对冻结语料上现有的 2 个 `self_multi_container` 组 (`aria-2-0-m5-replay-reconciler-drift-review-loop-audit` 的两行 `updated_at` = 2026-05-20/05-23; `aria-submodule-gate-block-flip` 的两行 = 2026-05-25/05-28), 均早于 2026-09-05 三十天以上, 与 proposal「结论: 两组 🟡 都是 2026-05..07 的 stale 行」逐字符合——不是执笔口算, 是可复算的真数据。

**三态计数**: Critical 0 closed / 0 reopened / 0 not-addressed；Major 3 closed / 1 reopened(窄化) / 0 not-addressed。

## 审计结论

方法论: (1) 对 v4 新增/改写 SC 逐条构造坏实现做反事实测试; (2) 对「先红」逐条用未改动的真实源码复现; (3) 对 T6 字段裁剪逐一比对 `track_to_claim_record` / `dedupe_latest_per_track_container` 的 `track.get(...)` 调用点; (4) 用 scratchpad `v3repo/`(state-scanner 完整目录, 含 `tests/`, 源码补丁到 v4 语义) 对**真实全部 1492 个 test** 跑三次 (未改测试基线 / 源码补丁+未改测试 / 源码补丁+四项点名测试改写), 与**真实仓库未改动版**的同法基线做差集比对, 隔离出真正由本 Spec 引入的回归。

### type: issue / severity: major / category: testing / scope: SC-2 advisory 臂的「dedupe 前调用」生产接线 (`handoff_multibranch.py:709`) 仍无端到端判据锁定, 与 SC-10 对渲染器同类接线的锁定方式不对称

**summary**: SC-10 (T8) 明确写了反事实「渲染器改为对 dedupe 后行算 → 0 行 (红)」且上下文限定为「board 对 fixture 渲染」——这天然要求测试跑真实渲染函数, 从而锁定 `track_board.py` 里 `identity_drift_advisories` 的调用顺序。SC-2 (T2) 的 advisory 臂反事实「对 deduped 调用 → 0」没有这个限定, 且旁边仅有的两处会真正驱动 `collect_handoff_multibranch()` 的测试 (T2 点名改写的 `test_real_collector_emits_cross_owner_collision` / `test_real_collector_no_collision_is_none`) 用的都是非 uuid 容器 (`box-A`/`box-B`) 夹具, 天生不产生 drift advisory。三者叠加, collector 侧 `:709` 的调用顺序 (传 `tracks` 还是 `deduped_tracks`) 在 SC 文本字面要求下**没有任何一条断言必须经由真实 collector 输出来验证**。

**evidence**: 实读 `handoff_multibranch.py:707-722`(现状, 我方案已做等价 v4 语义补丁于 scratchpad, 未改仓内文件) 确认 `:709` 是 `deduped_tracks, dedupe_stats = dedupe_latest_per_track_container(tracks)` 的位置, 正确接法必须在此行之前用原始 `tracks` 调用 `identity_drift_advisories`。构造判定实验: 在 scratchpad 补丁里把调用点故意接反 (`_identity_drift_advisories(deduped_tracks)` 而非 `_identity_drift_advisories(tracks)`), 只用 SC-2/SC-8/T2 字面要求的测试集合(即: (a) 手写 `tracks` vs `deduped_tracks` 两个列表直接调用纯函数验证反事实; (b) `test_real_collector_emits_cross_owner_collision`/`test_real_collector_no_collision_is_none` 两条真实 collector 测试, 用 `box-A`/`box-B` 非 uuid 夹具; (c) `test_normalize_snapshot` 字段存在性锁) 全部跑一遍: **全部通过**, 接反的 bug 未被任何一条抓到——因为 (a) 是纯函数级, 不经过 `:709`; (b)/(c) 的夹具容器不是 uuid, `identity_drift_advisories` 内部按 `_UUID_RE.match(container)` 提前跳过, 无论传 `tracks` 还是 `deduped_tracks` 结果都是 `[]`, vacuous pass。真正会被该 bug 影响的场景 (SC-2 里「同容器双 owner」那条: 同一 track_id、同一 uuid 容器、两个 owner 串) 若要暴露必须用 uuid 容器夹具跑一次真实 collector, 但 SC 文本没有点名要求这一条。
**建议修法** (窄, 可在 B.1 补一句到 SC-2, 不涉及方案重新设计): 仿照 SC-10 的写法, 给 SC-2 advisory 臂的反事实句加一个前置限定, 例如「端到端 (真实 `collect_handoff_multibranch()`, uuid 容器夹具, 同 track_id 双 owner): dedupe 前 advisory 恰 1 条; 若接反 (对 deduped 调用) → 0 条」, 并要求 T2 点名改写的两条「真实 collector」测试之一(或新增一条)改用 uuid 容器夹具而非 `box-A`/`box-B`。

### type: issue / severity: minor / category: testing / scope: SC-11「谓词只有一个实现 (grep 断言无第二份)」按名字 grep 可被同义改名绕过

**summary**: T13/SC-11 要求「collector 与 renderer 调同一谓词」且验收判据写成「grep 断言无第二份」。若该 grep 具体实现为搜索固定函数名字符串 (如 `grep -c "def layer_h_is_fresh"`), 一个把 renderer 侧逻辑复制一份但改名 (如 `_layer_h_fresh_check`) 的实现, grep 计数仍是 1, 会被误判「只有一个实现」, 但实际存在两份可独立漂移的逻辑拷贝——这正是「共享谓词」条款想防止的维护性风险本身。**该维护性风险不影响即时正确性**: SC-11 另一条「collector 与 renderer 对同一 fixture 得同一 `kind`/`groups`」已经独立锁定了当下的行为一致性, 命名绕过只会在未来两份拷贝各自被修改时才实际分叉, 属于防御性判据的表述精度问题, 不是正确性缺口, 定为 minor。
**evidence**: 阅读 SC-11 原文「谓词只有一个实现 (grep 断言无第二份)」未指定 grep 的目标模式 (函数名字符串 / import 关系 / 常量引用点), 三种目标模式里只有「两处调用点是否 import 同一个可调用对象」能真正防绕过, 而「grep 函数名」防不住改名。此为 D-3(a) 条件项 (T13), D-3 仍待 owner 裁定。

### type: note / severity: minor / category: fixture-completeness / scope: T6 七字段清单未列出 `phase`, 但 `track_to_claim_record` 确实读取该字段(不影响 `kind`/`groups` 输出)

**summary**: T6 明文「只保留 `track_id / owner_container / status / updated_at / filename / branch / legacy` 七字段」。实读 `lib/collision.py::track_to_claim_record` (`phase = track.get("phase") or ""`) 确认它确实读取第八个字段 `phase` 并写入 `ClaimRecord.phase`。但实读 `lib/reconcile.py` 全文 grep `phase` 零命中——`reconcile_all`/`classify_claims` 都不使用 `phase` 参与判定, 缺省空串不会影响 `kind`/`groups` 输出, 也不会抛异常。另一方面, `legacy` (布尔字段, 区别于 `status=="legacy"` 字符串) 被 T6 列入七字段但实际在 `dedupe_latest_per_track_container`/`track_to_claim_record`/`classify` 全链路里从未被读取 (只有 `test_p1_layer_h.py` 一处无关测试用到)。两处加起来看, T6 的字段清单是「实际功能所需」与「历史字段列表」的不完全对齐, 但**功能性结论不受影响**: 用只含 T6 七字段(不含 `phase`)的 fixture 跑生产路径, `kind`/`groups`/新增的 `identity_advisories` 均与含 `phase` 字段的原始语料跑出的结果逐字一致(已用 `r3_v3impl.py` 对冻结语料实跑验证, 见「R3 处置核对」)。归为文档口径 minor, 不影响 SC-6 验收。

## Minor（补充，非独立扣分项）

- 全套 pytest 在这个沙箱环境下用最朴素的 `pytest tests`/`pytest .` 调用会因 `_helpers.py`/`lib` 两个非包顶层辅助模块在 `tests/__init__.py` 存在时的 sys.path 语义问题直接在collection阶段炸 12 个文件 (`ModuleNotFoundError: No module named '_helpers'` 等)，且**这在完全未改动的真实仓库上同样复现**——与本 Spec 无关，是环境/调用方式问题，非 Spec 引入。用 `PYTHONPATH=".:..:../scripts" python -m pytest tests/`（cwd=`state-scanner/`的父级不行，须显式把 `tests/`、`state-scanner/`、`scripts/` 都塞进 `PYTHONPATH` 并用 `python -m pytest`，纯 `pytest` CLI 不行）可让全部 1492 个 test 正常 collect。T10/SC-7 落地时 B.2 报告应记录可复现的调用方式，否则「全套跑没跑起来」会被误判成回归。

## Verdict

PASS_WITH_WARNINGS (0 Critical / 1 Major / 2 minor)

## Vote

REVISE

**理由**: 剩余 1 条 Major (SC-2 advisory 臂生产接线未端到端锁定) 的修法本身很窄——只需在 SC-2 文本里补一句仿照 SC-10 的端到端限定 + 把点名改写的两条「真实 collector」测试之一换成 uuid 容器夹具——但它是**验收标准文本**层面的缺口, 不是留给 B.2 实现者自由裁量就能补齐的执行细节: 按当前 SC-2/SC-8/T2 字面, 一个完全合规的实现仍可能把 `:709` 接反而不被任何点名测试发现, 这正是 R3 Major-2 想堵住但 v4 只堵了一半的同一个风险敞口。鉴于该风险敞口的性质与 R3 判定为 Major 一致 (都是「生产接线顺序可被绕过」), 且本 Spec 三层处置里 D3 是专门为解决"漂移信号可用性"新增的机制, 其唯一验收依据之一 (advisory) 存在这个漏点应在下一版 SC 文本里补齐, 故投 REVISE, 而非把它下放成 B 期顺手项。若 owner/tech-lead 认为该缺口足够窄、可以直接在 B.1 任务分解阶段补一句而不需要重新走 post_spec 收敛, 我不反对以聚合结论覆盖此票。

## 轮次记录

Round 4 (qa-engineer, convergence mode, 镜头「SC 稳定性: v4 的 SC-1..SC-11 是否全部可证伪、先红声明是否属实、是否只剩 B 期顺手项」): 对 R3 遗留 4 条 Major 逐条核对, 3 条闭合 (SC-7/SC-8 两条既有测试冲突被 T2 明文点名; D-0(a) 日期戳反例被 T9/SC-2 明文钉入; SC-6 归因判据从「无判据」变为「LAYER_H_ACTIVE_WINDOW_DAYS 阈值 + 强制注入真撞车样本」且冻结语料上的机械归因结果经实跑核实与 proposal 声称的「两组 2026-05..07 stale」逐字符合), 1 条窄化重开 (D3 advisory 的生产接线顺序在 SC 文本字面上仍可被绕过, 但风险面从「函数级」收窄到「仅剩 collector `:709` 一处调用点」)。新增 1 条 minor (SC-11 grep 判据可被改名绕过, 但不影响当前正确性)。方法论上做了三件实证工作: (1) 用 scratchpad `v3repo/`(state-scanner 完整目录含全部 tests/) 把 v4 的源码语义 (两段式解析 / `identity_key` / 不可归属 owner 排除 / dedupe 键改用 `identity_key` / `identity_drift_advisories` 恒写入且置于 dedupe 之前) 打成补丁, 对**真实全部 1492 个 test** 分三阶段跑 (未改动真实仓库基线 46 failed / 源码补丁+未改点名测试 56 failed / 源码补丁+四项点名测试改写后 50 failed), 用集合差运算精确定位出 v4 引入的新失败集合**恰好等于**四项点名测试 (`test_split_owner_container_variants`、`test_real_collector_emits_cross_owner_collision`、`test_real_collector_no_collision_is_none`、`test_both_latest_active_still_reports_self_multi_container`), 且额外出现的 4 项差异经逐一排查全部是 scratchpad 部分拷贝(缺 `phase-b-developer/SKILL.md`、`config-loader/SKILL.md`、`hooks/` 目录、非 git 仓库)导致的环境假阳性, 补齐后即消失, 与 SC-7/T10「点名改写后零回归」的声称严丝合缝; (2) 把点名的 4 条测试按 v4 语义实际改写并重跑, 确认全绿且未产生次生回归; (3) 对 T6 字段裁剪逐一比对 `track_to_claim_record`/`dedupe_latest_per_track_container` 的字段读取点, 发现 `phase` 被读取但未列入 T6 七字段清单 (功能上无影响, 因 `reconcile.py` 全链路不消费 `phase`)、`legacy` 布尔字段被列入但实际全链路未读 (同样无功能影响), 定性为文档口径 minor 而非功能缺口。附带发现: 该沙箱环境下 `pytest tests/`(简单调用) 会在完全未改动的真实仓库上同样炸 12 个文件的 collection (`_helpers` sys.path 问题, 与本 Spec 无关), 需要 `PYTHONPATH` 显式包含三层目录 + `python -m pytest` 才能让全部 1492 个 test 正确 collect——记入报告供 B.2 落地引用可复现命令。
