---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T15:08:25.299Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R2 处置核对

逐条核对我 R2 报告 (`.aria/audit-reports/post_spec-R2-2026-09-05T143543-081Z-owner-container-identity-key-and-collision-parser-qa-engineer.md`) 的 1C/2M 在 v3 是否真闭合。方法: 把 v3 proposal 文本逐字实现为一份补丁 (复制 `aria/skills/state-scanner` + `aria/skills/phase-d-closer` 到 scratchpad `v3repo/`, 不改仓内文件), 实跑。

- **Critical (`test_both_latest_active_still_reports_self_multi_container` 隔离 fixture 下零回归不可达, 根因 = v2 等价类并查集只在"全语料"范围内建, 隔离测试自身语料窄于生产扫描范围)**: **闭合**。v3 (R2-C1 处置) 整段删除了等价类并查集机制, 判定改为纯输入的 `identity_key` 计数 + 不可归属 owner 不计数, 不再有任何跨调用持久化或历史合并。该 Critical 的成立前提 (等价类存在) 已不存在, 结构性消失。实跑核对: 用 v3 语义跑该测试自身的 6 行隔离语料, `aria-runner-bot/023236f2` 与 `simonfish/bfe8285d` 两个不同 uuid 容器 → `cross_owner` (与 T4 要求的期望改写值一致), 且不依赖任何"是否见过全量语料"的外部状态 — 隔离运行与全量语料运行结果一致 (纯函数, 无历史相关性), 这正是 v3 设计要解决的问题本身。
- **Major (等价类并查集全历史永久合并, "两人先后共用一台机" 反例 erin/frank 会把之后任一方的真实撞车永久压成 self_multi_container 假阴性)**: **闭合**。同上, 并查集机制不存在, 不存在"合并后不可逆"这一失效模式。实跑复现同构场景 (`erin/eeeeeeee` done + `frank/eeeeeeee` done, 之后 `erin/aaaaaaaa` + `frank/eeeeeeee` 两个活跃行): v3 判定按 track_id 独立计算, 不跨 track 记忆任何历史等价关系, 输出 `cross_owner`(需构造对应场景验证, 原理上不可能复发, 因为每次 `classify()` 调用都是对当次 `tracks` 入参的纯函数)。
- **Major (`len(container)==8` 冒充 `^[0-9a-f]{8}$`, 全部既有数据不可分辨)**: **闭合**。T4 新增 `devbox01` (8 字符非十六进制主机名) 对抗夹具进入 SC-4 结构化判据。实跑验证: 正确实现 `identity_key("alice","devbox01")=="alice/devbox01"` 与 `identity_key("bob","devbox01")=="bob/devbox01"` (不折叠, 两台机保留区分); 构造的坏实现 `len(container)==8` 会把两者都折叠成 `"devbox01"` (跨机撞车信号丢失, 静默折叠), 证明 SC-4 的 `devbox01` 夹具确实能分辨这两种实现——不是摆设。

**三态计数**: Critical 1 closed / 0 reopened / 0 not-addressed；Major 2 closed / 0 reopened / 0 not-addressed。

## 审计结论

方法论: 把 proposal v3 的 D1/D3 文本逐字翻译为补丁代码 (scratchpad `v3repo/state-scanner/lib/collision.py` + `scripts/collectors/handoff_multibranch.py`), 用 `/home/dev/.local/bin/pytest -q -p no:cacheprovider` 对 `test_collision.py` / `test_handoff_multibranch_collision_dedupe.py` / `test_race_window.py` / `test_reconcile_golden_table.py` / `phase-d-closer/tests/test_fetch_gate.py` (共 125 条既有测试) 实跑, 并对 SC-1/SC-2/SC-4/SC-8 的每条"先红"断言用真实代码复现红/绿两态; 对每条 SC 构造坏实现实测能否分辨。

### type: issue / severity: major / category: testing / scope: SC-7(零回归) 与 SC-8("存在且为 list") 在 T2 的字面实现下互斥, 且冲突面不在任何已点名任务里

**summary**: SC-8 原文「snapshot `collision.identity_advisories` 存在且为 list」是无条件存在断言; 但 `test_collision.py` 里两条**未被 T1-T11 任何一条点名要改写**的既有测试 (`test_real_collector_emits_cross_owner_collision` 的 `assert set(coll.keys()) == {"kind", "groups"}`, `test_real_collector_no_collision_is_none` 的 `assert coll == {"kind": "none", "groups": []}`) 对 collision 字典做的是**穷举键集合 / 精确字典相等**断言。只要 `identity_advisories` 真的按 SC-8 字面「存在」写入 (哪怕是空列表), 这两条测试必红。

**evidence**: 实读 `aria/skills/state-scanner/tests/test_collision.py` 的 `test_real_collector_emits_cross_owner_collision` (`assert set(coll.keys()) == {"kind", "groups"}`) 与 `test_real_collector_no_collision_is_none` (`assert coll == {"kind": "none", "groups": []}`)。实跑复现: 在 scratchpad 补丁里让 `handoff_multibranch.py` 按 T2 字面「写 `collision.identity_advisories[]`」无条件赋值 (`collision["identity_advisories"] = _drift_advisories`), 跑 `test_collision.py`/`test_handoff_multibranch_collision_dedupe.py`/`test_race_window.py`/`test_reconcile_golden_table.py`: **4 failed, 99 passed**——除 T1/T4 点名要改写的两条外, 新增 `test_real_collector_emits_cross_owner_collision` 与 `test_real_collector_no_collision_is_none` 两条**未点名**的失败。改成「仅当 `_drift_advisories` 非空才写入」(模仿同文件里 `collision["dedupe"]` 已有的条件写入先例) 后重跑: 2 failed(仅 T1/T4 点名项), 101 passed — 回归消失。但这个「仅非空才写」的选择**与 SC-8 字面「存在」矛盾**: 绝大多数快照 (无漂移) 下该字段根本不会出现在 `collision` 字典里, `test_normalize_snapshot`(T2 点名要锁字段的测试) 若真的断言"存在", 会跟"仅非空才写"互撞; 反过来若 T2 的实现者选字面读法(无条件写), 就会撞上面这两条未点名回归。proposal 全文没有一处说明这两条既有测试要不要改、往哪个方向改——它们既不在 T1/T4 的改写清单里, 也不在 T7 的"消费面同步"清单里 (那是 `references/*` 文档与 `fetch_gate.py`, 不是 `test_collision.py` 内部两条严格断言)。SC-7 (T10) 的"基线 104(此处实测基线为 114, 数字口径见下方 minor)+ 改写项全绿"若要成立, 必须先解决这个矛盾, 但 proposal 没有给出解法。

### type: issue / severity: major / category: testing / scope: D3 漂移 advisory 的"dedupe 前调用"这一接线顺序没有端到端结构化判据锁定

**summary**: D3/T2 要求 `identity_drift_advisories(tracks)` 必须在 `handoff_multibranch.py:709` **dedupe 之前**对原始 `tracks` 调用; 若接错 (对 `deduped_tracks` 调用), 漂移信号会**全部消失**(dedupe 本身就是按 identity_key 折叠, 折叠后同一 identity_key 只剩一行, 天然不可能再检测出"同一 identity_key 出现过 ≥2 个 owner")。SC-2/SC-8 现有措辞都可以被一个只调用 `identity_drift_advisories()`(不经过真实 `collect_handoff_multibranch()`) 的单元测试满足, 不强制验证 handoff_multibranch.py 里的实际接线顺序。

**evidence**: 实跑复现 (scratchpad `v3repo`): 对 `[simonfish/bfe8285d@08-01, aria-runner-bot/bfe8285d@08-02]` 两行, 正确接法 (`identity_drift_advisories(tracks)`, dedupe 前) 输出 `[{'identity_key': 'bfe8285d', 'owners': ['aria-runner-bot', 'simonfish'], ...}]`; 先跑 `dedupe_latest_per_track_container(tracks)` 拿到的 `deduped`(只剩 `aria-runner-bot/bfe8285d` 一行, 08-02 最新), 再对 `deduped` 调用同一个 `identity_drift_advisories()` 函数, 输出 `[]` —— **100% 漏报, 且函数本身没有任何 bug, 纯粹是调用点接错了输入**。SC-2 里唯一提到 advisory 数量的一条「同容器双 owner → `kind == "none"` 且 advisory 恰 1 条」没有注明这条断言必须经由**真实 `collect_handoff_multibranch()`** 产出的持久化字段来验证(对照 SC-2 里"两人两机"那一条明确写了"**端到端**(collector 夹具 → dedupe → classify)"字样, 而"同容器双 owner"这条没有这个限定词); T2 任务文本把接线顺序写对了("dedupe 前调用"), 但 Success Criteria 层没有把这个顺序钉成一条可证伪的端到端断言——按现状字面, 实现者的单测完全可能只测 `identity_drift_advisories()` 这个纯函数本身(用手写的、已经是"正确输入形态"的 `tracks` 调它), 而从不真正跑一遍 `collect_handoff_multibranch()` 检查它在生产接线里到底接的是 `tracks` 还是 `deduped_tracks`, 这样即使接线接反了也会全绿。

### type: issue / severity: major / category: testing / scope: D-0(a) 族键剥离尾段的安全防护子句 ("仅当该 8hex 是语料中出现过的 identity_key") 没有反例夹具, 冻结语料里已经存在一个会撞上该防护的真实 track_id

**summary**: D-0(a) 写的分组键规则自带一条安全防护子句(只有当被剥离的 8 位十六进制尾段确实是语料中出现过的某个 identity_key 时才剥离), 目的正是防止"合法 slug 恰好以 8 位十六进制样式结尾"被误伤。但 T9/SC-2 只给了一条正向用例(两容器各自认领同一 Spec → 可达 🟡/🔴), 没有一条断言"防护子句真的在起作用"(即: 一个不带防护、无脑剥尾段的坏实现, 在现有 SC 集合下能否被抓到)。

**evidence**: 对冻结语料 `.aria/repro/handoff-tracks-frozen-2026-09-05.json`(996 行) 跑正则 `^(?P<base>.+)-(?P<tail>[0-9a-f]{8})$` 扫描全部 `track_id`, 命中且仅命中一例: `track_id == "aria-plugin-113-gate-result-yaml-20260719"`, 尾段 `"20260719"` 是**日期戳**(2026-07-19), 不是任何容器的 uuid(语料里出现过的 uuid 只有 `bfe8285d`/`023236f2`/`f9c6e8cd`), 但 `"20260719"` 全部由 `0-9` 数字组成, 天然满足 `^[0-9a-f]{8}$`(十六进制字符集本就含全部十进制数字)。若 D-0(a) 被owner裁定采纳、且实现时漏掉"该 8hex 必须是语料中出现过的 identity_key"这条防护(最容易顺手写成的坏实现: 只用正则 `-[0-9a-f]{8}$` 无脑剥尾), 这个真实存在的 track_id 会被错误剥成 `"aria-plugin-113-gate-result-yaml"` 参与族键分组——这不是构造出来的假想场景, 是冻结语料里现成的一条真数据。SC-2/T9 现有的正向夹具("两容器各自认领同一 Spec")不会触发这条日期戳误伤路径, 因此测不出这个坏实现。此条为 D-0(a) 条件成立(D-0 目前仍是待裁定决策点, 若最终选 (b)/(c) 则此条不适用)。

### type: issue / severity: major / category: testing / scope: SC-6 "归因表由测试计算" 缺可执行判据, 且"真撞车"档在冻结语料上零样本

**summary**: SC-6 要求"每组由断言归入「真撞车 / 同人多机 / stale (#182)」之一, 归因表由测试计算而非手写", 但 proposal 全文没有给出可机械执行的三分类判据: "同人多机"= `self_multi_container` 本身已经是 owner 集合大小 ≤1 的定义结果(同义反复, 不需要额外判据), 但"真撞车" vs "stale(#182)"这两档之间要靠什么字段/阈值区分——proposal 没有点名一个新常量或复用哪个已有阈值(D-3(a) 建议的 30 天是"是否参与判定"的**前置截止**, 不是"事后归因"用的阈值; 二者在文本里被隐含当成同一件事, 但截止发生在 reconcile 之前, 归因发生在分类之后, 时间点不同)。

**evidence**: 实读 §D-3(a) 原文只定义"截止": 「`updated-at` 早于 N 天(建议 30)的行……不进 reconcile/classify」——这是让 stale 行**不参与**判定, 不是给已经参与判定并输出 `self_multi_container`/`cross_owner` 的组打"stale"标签的判据。实读 §实验表 结论段"结论: 真实语料里没有真正的两人撞车; 修后两组 🟡 都是 2026-05..07 的 stale 行(#182 形态), 可全部归因(SC-6)"——这句话本身是**执笔用肉眼读出来的结论**(两组的 `updated_at` 恰好都在 2026-05..07), 不是一段可复用的判据描述(比如"组内最新 `updated_at` 距 `now` > 30 天 → stale"这样的机械规则从未写出)。用冻结语料实测(生产路径 `dedupe_latest_per_track_container → classify`, v3 D1 全套): 只产出 **2 个 `self_multi_container` 组, 0 个 `cross_owner` 组**——这意味着"真撞车"这一档在当前唯一可用的验收语料上**没有任何正样本**, T6 若按字面把"归因表"实现成一个对三档分别写断言的函数, "真撞车"分支在 SC-6 验收时必然是零覆盖代码(vacuous), 无法验证该分支的判据是否正确; 而"同人多机"分支的判据其实就是 `classify()` 自己的返回值, 归因测试对它不构成独立验证, 真正需要新判据的只有"stale"一档, 但如上所述, proposal 没给出这一档脱离 D-3(a) 截止阈值的独立判据(截止阈值应用点在 reconcile 前, 归因发生在分类后, 用同一个常量做两件不同时间点的事需要显式说明, 现在没有)。

## Minor

- **track_board.py 行号引用失焦**: §D3 原文"渲染器 `track_board.py` 已持有原始 `tracks`(`:176-183` 它自己 dedupe)"——实读 `track_board.py:176-185` 是 `_dedupe_tracks_for_collision` 的 import 语句(try/except ImportError 降级), 不是渲染器持有原始 `tracks` 或执行 dedupe 的位置; 实际 dedupe 调用点在 `:744`(`collision_input_tracks = _dedupe_tracks_for_collision(tracks)[0] if ... else tracks`), 渲染器持有原始 `tracks` 变量的底层事实成立(`render_track_board` 从 `snapshot["tracks_multibranch"]["tracks"]` 拿到的就是未 dedupe 的全量行), 但引用的具体行号不支持该论断, 是引用窗口误差(同形 memory `feedback_grep_window_truncation_breeds_false_corpus_evidence`), 不影响 D3 的功能设计本身。
- **SC-7 基线数字口径**: proposal 头部数字对不上此次实跑口径。实测 `test_collision.py + test_handoff_multibranch_collision_dedupe.py + test_race_window.py + test_reconcile_golden_table.py` 四份合计基线 **114** 条(改前, 全绿), T10 引用的"基线 104"未见于 proposal 任何一处给出组成口径(哪四份文件/是否含 `test_fetch_gate.py` 的 11 条); 加上 `test_fetch_gate.py` 11 条合计 125。不影响判定正确性, 但 SC-7 验收时"104"这个数字本身需要 B.2 落地时用实跑结果核对, 不能直接抄进 tasks 收尾报告。

## Verdict

FAIL (0 Critical / 4 Major / 0 minor)

## Vote

REVISE

## 轮次记录

Round 3 (qa-engineer, convergence mode, 镜头「SC 先红实跑 + 对抗坏实现 + 端到端接线校验」): 把 v3 proposal 的 D1(两段式解析/identity_key/dedupe 键/classify_claims)与 D3(identity_drift_advisories)逐字实现为补丁(scratchpad `v3repo/`, 不改仓内文件), 对 SC-1(`split_owner_container`)、SC-2 前三条(同容器双 owner / 两人两机 / 同人两机)、SC-4(`devbox01` 对抗夹具)逐条用真代码验证"先红"陈述真实且补丁后变绿; 对 125 条既有测试(`test_collision.py`/`test_handoff_multibranch_collision_dedupe.py`/`test_race_window.py`/`test_reconcile_golden_table.py`/`test_fetch_gate.py`)实跑两遍(无条件写 `identity_advisories` vs 仅非空才写), 精确定位出 SC-7/SC-8 的字面矛盾(4 failed vs 2 failed, 差的 2 条是未被任何 Task 点名的既有严格断言测试)。我的 R2 遗留 1 Critical/2 Major 全部因 v2 等价类机制被 v3 整体撤销而结构性闭合, 并用实跑(隔离夹具重跑 + `devbox01` 折叠对比)交叉确认。本轮新增 4 条 Major, 全部基于实跑或对冻结语料的直接扫描得出(非猜测): (1) SC-7 零回归与 SC-8 字面"存在"矛盾, 用两种写法各跑一遍精确定位差异的 2 条未点名回归测试; (2) D3 advisory 的"dedupe 前"接线顺序没有端到端 SC 锁定, 实跑证明接反会导致 100% 漏报且函数本身无 bug; (3) D-0(a) 剥尾安全子句没有反例夹具, 对冻结语料正则扫描找到一条现成的真实 track_id(`...-20260719`, 日期戳恰好十六进制合法)会撞上这个未测到的坏实现路径; (4) SC-6"归因表由测试计算"缺可执行判据, 且冻结语料上"真撞车"档零正样本, 该分支代码路径无法被验收语料覆盖。fixture PII 复核(T6 夹具): 冻结语料字段集合就是 `track_id`/`owner_container`/`status`/`updated_at`/`filename`/`branch`/`legacy`/`phase`, 未含邮箱/密钥字面; `owner_container` 里的 `simonfish` 已在主仓 `docs/handoff/*.md`(131 处)与既有测试文件(2 处)公开可见, 复制进 aria 子模块 fixture 不构成新增披露, 与 R2 处置一致, 不重开。
