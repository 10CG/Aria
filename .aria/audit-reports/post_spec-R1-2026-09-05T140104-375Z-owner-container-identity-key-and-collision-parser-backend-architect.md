---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T14:05:00.000Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

### Finding 1 (critical / issue / testing)
- **scope**: proposal.md D1 (line 31) + SC-4 (line 91); `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py:511-521`; `aria/skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py:958-971`
- **summary**: SC-4 要求「同容器不同 owner 两行折叠为 1」, 但 D1 明确对 `handoff_multibranch.py:518` 的 dedupe key「不改逻辑」; 该 key 字面含 owner (`(track_id, owner, container)`), 结构上不可能把「同 container 不同 owner」两行合并——且与既有锁定测试的设计不变式直接冲突, 无调和方案。
- **evidence**: 实读 `handoff_multibranch.py:511-521`:
  ```
  key = (t.get("track_id"), owner, container)
  ...
  groups.setdefault(key, []).append(t)
  ```
  用 proposal 自己描述的 NEW split (owner=first-seg, container=second-seg) монkey-patch 后实跑 `dedupe_latest_per_track_container`, 输入 `aria-runner-bot/bfe8285d` 与 `simonfish/bfe8285d` (同容器 `bfe8285d`, owner 漂移):
  ```
  NEW split dedupe: len(deduped)= 2 stats= {'input_tracks': 2, 'after_dedupe': 2, 'legacy_passthrough': 0}
     aria-runner-bot/bfe8285d 2026-08-27T00:00:00Z
     simonfish/bfe8285d 2026-09-03T00:00:00Z
  ```
  两行未折叠 (len=2), 与 SC-4「折叠为 1」矛盾。此外, 现存测试 `test_owner_segment_participates_in_grouping_key` (`test_handoff_multibranch_collision_dedupe.py:958-971`) 明文断言「Same container NAME under two different owners ... must stay two rows」且理由是「a key of (track_id, container) that drops the owner folds them into one and erases a cross_owner collision」——这是一条刻意锁住的设计不变式 (owner 必须参与 key), 与 SC-4 对 2 段式身份漂移场景要求的相反行为 (owner 不同仍应折叠) 结构性互斥。proposal 未讨论如何在同一个 dedupe key 公式下同时满足两者 (例如按段数分支处理), T4 任务描述也只字未提修改 key 公式。SC-4 按 T4「不改逻辑」的现有设计路径不可实现。

### Finding 2 (major / risk / testing)
- **scope**: proposal.md T6 / SC-6 (line 83, 93); `.aria/state-snapshot.json`; `.gitignore:18`
- **summary**: SC-6 依赖「冻结」的 `.aria/state-snapshot.json`, 但该文件被 `.gitignore` 忽略且随每次扫描变化, Tasks 里无任何机制把它真正冻结成一份 fixture; 实测当前活文件已与 proposal 自己的实验表 A 行数据不一致。
- **evidence**: `git check-ignore -v .aria/state-snapshot.json` → 命中 `.gitignore:18`; `git log --oneline -1 -- .aria/state-snapshot.json` 空输出 (从未被 git 追踪)。实读当前活文件:
  ```
  collision: {"kind": "self_multi_container", "groups": [["dev-claude", "simonfishgit/dev-claude"]], "dedupe": {...}}
  ```
  只有 1 个 group, 而 proposal 实验表变体 A (line 48) 声称有 2 个 group (`[dev-claude, simonfishgit/dev-claude]` 与 `[aria-runner-bot/023236f2, simonfish/bfe8285d]`)。当前活文件已经缺失第二组——证明「本 Spec 起草日 snapshot」这句话所指的具体数据在 B.2 执行时大概率已经漂移, 而 T6 未规划把当日快照另存为仓内 fixture (如 `openspec/changes/.../fixtures/`), SC-6 的「前后对照」在实现时会失去可复现的输入基准。

### Finding 3 (major / risk / architecture)
- **scope**: proposal.md D1 (`get_container_id()`, line 32) + Impact 表; `aria/skills/state-scanner/lib/claim_lifecycle.py:39,88`; `scripts/phase1_gate.py:294,486`; `lib/concurrent_tracks.py:25,133`
- **summary**: T3 把 `get_container_id()` 语义从「label 优先」改为「恒 uuid」, 但除 proposal 点名的 identity.py 自身外, `claim_lifecycle.py`(写 claim) / `phase1_gate.py:294`(裁决 winner 归属) / `concurrent_tracks.py`(计数 active claim) 都经由 `get_identity()` 间接消费同一函数; proposal 未评估「修复前已写入 `refs/aria/coordination` 的历史 claim 若 `container` 字段是旧 label 值」在修复后与新 uuid 比较会不会重演 #135 式误判。
- **evidence**: `grep -rln "get_identity\|from .identity import" aria/` 命中 `lib/claim_lifecycle.py:39` (`from .identity import Identity, get_identity`)、`scripts/phase1_gate.py:294` (`verdict.winner.container == identity.container_id`)、`lib/concurrent_tracks.py:25,133` (`from .identity import get_container_id` / `container_id = get_container_id()`)。这 3 个文件均不在 proposal §Impact / Tasks 的落点清单里 (清单只提 identity.py 自身 + collision.py 两消费方)。实测复现「先 acquire (uuid) 再打 label」序列下, `get_container_id()` 的返回值从 `c9e19e10` 变为 `dev-claude2` (脚本 `/tmp/claude-1000/-home-dev-Aria/660cdd00-d2ad-4227-a5bb-5312810322f1/scratchpad` 内实跑), 证实修复前 claim 写入时可能已固化 label 值; 修复后 `phase1_gate.py:294` 用新 uuid 比较陈旧 claim 的 label 值会不匹配, 复现 #135 的另一变体, 但 proposal 未提及迁移期风险或补偿措施。

### Finding 4 (minor / issue / documentation)
- **scope**: proposal.md D2 (line 37); `standards/conventions/session-handoff.md §2.3.7 / §2.3.8`
- **summary**: D2 计划「新增 §2.3.7「AI runner 提交身份」」, 但 §2.3.7 已被 `Frontmatter content enforcement (#137, aria-plugin v1.43.0+)` 占用, §2.3.8 也已被「结构化 Carry-id schema」占用; 新章节实际应编号 §2.3.9。
- **evidence**: 实读 `standards/conventions/session-handoff.md` TOC — `### 2.3.7 Frontmatter content enforcement (#137, aria-plugin v1.43.0+)` (行 204 附近) 与 `### 2.3.8 结构化 Carry-id schema (§6 prose 层, ...)` (行 217 附近) 均已存在且非空。

### Finding 5 (minor / risk / implementation)
- **scope**: `aria/skills/state-scanner/lib/collision.py:346-356, 390-398` (`oc_by_tid_key` / `members` 计算)
- **summary**: NEW split 下, 所有 2 段式 handoff 记录的 `session` 字段恒为 `""` → `track_to_claim_record` 内 fallback 成 `"unknown"`; `classify()` 用 `(owner, container, session)` 三元组做标签去重 key 与 members 的 set 去重 key, 当上游未先做 `dedupe_latest_per_track_container` (例如直接调用 `classify()`, 或 dedupe fail-soft 降级) 时, 同 owner+container 的两条真实活跃行会在 `groups[]` 显示层被静默合并成 1 条, 丢失行数信息 (不影响 `kind` 判定本身)。
- **evidence**: 实读 `collision.py:353` `key = (rec.owner, rec.container, rec.session)`、`:393-397` `members = sorted({label_map.get((c.owner, c.container, c.session)) ... for c in active_claims})`; 结合已验证的「2 段串 session 恒 unknown」事实 (Finding 1 的 monkeypatch 实验), 推导得出。proposal 未在 SC 中覆盖此路径 (SC-2/SC-4 均通过预 dedupe 或单容器输入验证, 未测「未 dedupe 的同 owner+container 双活跃行」)。

## Verdict

FAIL — 1 Critical (SC-4 结构性不可实现) + 2 Major + 2 Minor (1C/2M/2m)。

## Vote

REVISE

## 轮次记录

**读了什么**: `proposal.md` 全文 (逐行核对 file:line 引用); `lib/collision.py` 全文 (split_owner_container/track_to_claim_record/classify_claims/classify/linked_issue_overlaps); `lib/identity.py` 全文; `lib/reconcile.py` 全文 (_tiebreak_key/reconcile 主流程); `lib/claim_schema.py` 全文 (_validate_superseded_from); `scripts/collectors/handoff_multibranch.py` 的 dedupe_latest_per_track_container 全函数 (含 docstring); `scripts/renderers/track_board.py` 的 import 块与 :380-440 渲染段; `tests/test_collision.py` 的 split/classify_claims 测试; `tests/test_handoff_multibranch_collision_dedupe.py` 的 owner-segment / session-fold / branch-tiebreak 测试段; `.aria/triage-report.json` 全文 (5 case); `.aria/state-snapshot.json` 的 tracks_multibranch 摘要; `standards/conventions/session-handoff.md` §2.3.1/§2.3.5/§2.3.6/§2.3.7/§2.3.8 TOC 与正文。

**跑了什么** (均在 `/tmp/claude-1000/-home-dev-Aria/660cdd00-d2ad-4227-a5bb-5312810322f1/scratchpad/` 内脚本, 未改仓内文件):
1. `split_owner_container` 对 2/3/1/0 段输入的当前行为直跑, 核对 proposal Why 段与 SC-1 的「先红」断言 — 一致 (`("", "simonfish", "bfe8285d")`)。
2. 用真实 triage case-2/3/4/5 输入直调 `lib.collision.classify()`, 核对 proposal/triage-report.json 声称的当前值 — 全部一致 (self_multi_container / self_multi_container / none / cross_owner)。
3. monkeypatch `split_owner_container` 为 proposal NEW 语义 (需注意 `scripts/lib/` 与 `lib/` 的双包遮蔽陷阱, 已用正确 sys.path 顺序规避), 直跑 `dedupe_latest_per_track_container` 验证 SC-4「同容器不同 owner 折叠为 1」——**不成立**, 见 Finding 1。
4. `get_container_id()` 复现 #135 08-13 时间线 (先 acquire 后加 label) — 确认现状「先红」且看到修复后仍可能对旧 claim 数据产生新的不匹配 (Finding 3)。
5. `git check-ignore` / `git log` 核实 `.aria/state-snapshot.json` 未纳入版本控制、当前活文件与实验表 A 行不一致 (Finding 2)。
6. `pytest -q` 跑 `test_collision.py` + `test_handoff_multibranch_collision_dedupe.py` + `test_reconcile_golden_table.py` — 91 passed (基线, 供 SC-7 回归对照)。
7. 全仓 grep `split_owner_container` / `get_container_id` / `get_identity` 消费方, 核对 proposal 落点清单完整性 — 发现 3 个未列消费方 (Finding 3)。

**未发现问题的项**: SC-1/SC-2/SC-3 对当前代码「先红」的断言均实测为真; D1 关于三段式 `superseded_from` 与 split_owner_container 互不干扰的判断成立; classify_claims 分类逻辑本身 (非输入契约) 无缺陷, 与 triage-report.json 结论一致。
