---
track-id: session-close-20260812-issue128-phaseb-batches
owner-container: simonfish/bfe8285d
phase: session-close
status: done
updated-at: 2026-08-12T19:49:16Z
---

# Session Handoff — aria-plugin #128 Phase B 批1+批2 (逐段判定落地) + census 逼出 4 个 spec 复议项

> **一句话**: 接上一份 handoff 的 §6-1「续 #128 进 Phase B」, 把 #128 从 Phase A 闭环推进到
> **Phase B 实现+测试主体完成** (29 task 里 **19 done**, 全经主 loop 独立核验)。**最重的产出不是
> 代码, 是 census/测试落地反复逼出的 4 个上游 spec 精度缺陷** —— 两个计数争议 (family 55→实跑57 /
> newline_affected.strict 11→实跑13) + 两个反事实表描述误差 (SC-6 恒split 15→16 / SC-1 粘性 1vs3
> 变体)。四者同族 (与 F-1 一样, 都是「把设计逐条落成可执行产物」时暴露的、六轮 post_spec + 机械闸
> 都没走到的精度面), 按 SC-18 明文**未凑数**, 全部挂 owner 复议。**代码本身零争议**: 批1+批2 回归
> 474/474 全绿, 反事实鉴别力主 loop 全部独立实证。

## §0 入口 (新 session 优先读)

- **#128 (`secret-guard-per-segment-evaluation`) Phase B 主体已落地, 未完**: 29 task 里 **19 done**
  (TASK-001..015 / 017 / 018 / 019), **10 挂起**。挂起分两类:
  - **卡 owner 复议 (4 项, 见 §2)**: TASK-016 (SC-19, 依赖 `family_count` 55 vs 57 裁决) + TASK-020
    (SC-13, 依赖全部测试写完的实跑总数)。SC-18 在裁定前无法变绿 (enabled SC, Rule #10 不自行豁免)。
  - **纯顺序未起 (不卡 owner)**: TASK-021/022 (B-验证: canonical 全量回归 + 五档性能) / TASK-023..028
    (ship 前/时/后: 版本 bump + 14 点核对 + 9 转出 issue + SC-9b)。
- **代码在 aria 子模块 feature 分支** `feature/secret-guard-per-segment-evaluation` (本地 HEAD `152cac8`,
  **未 push**)。主仓 gitlink 仍指 `af87cae` (feature 未合并, Phase B 期间**不 bump gitlink**, 正确 —
  C.2 合并 aria feature→master 后才 bump, 见 CLAUDE.md 硬约束 1)。
- **4 个 owner 复议项全文** (含主 loop 独立核验结论): `.aria/notes/2026-08-12-secret-guard-128-phaseb-batch1-count-disputes.md`。

## §1 已完成 (按时间顺序)

1. **B-entry advisory 认领** (`phase1_gate.py --mode advisory`): claim 写推 `simonfish/bfe8285d`,
   `outcome=passed`, 无竞争、无 linked-issue 重叠。coordination-gate-invocation 探针从此又一次真调。
2. **B.1** (aria 子模块建 `feature/secret-guard-per-segment-evaluation`, 基点 `af87cae`)。
3. **批 1 = TASK-001..010** (两 agent 并行: backend-architect hook + qa-engineer census):
   - `hooks/secret-guard.sh` 逐段判定: `_sg_safe_to_split` 四判据 (块字符引号感知字符扫描 / BLOCK_KW_RE /
     SCOPE_KW_RE exec·time 同精度 / 裸 & 独立字符扫描 TASK-029) + `_sg_split_top` (与块字符判据**同一
     引号状态机**) + `_sg_line_match` 逐行 helper (13 处 credit 判据零 fork) + 判定循环先 pattern 后
     credit + credit 段内缓存 (`_sg_judge_one` local, 每段重置, 根治 Aria#170 段间残留) + **子 shell
     隔离 fail-closed** (`( _sg_per_segment_eval )` — set -u unbound 唯一可捕获边界) + BLOCKED 补
     `Triggering segment:` 行 (SC-21) + sourcing gate (供单元测试 source)。
   - `hooks/tests/corpus_census.py` 权威计数器 (stdlib-only, subprocess grep -E 不模拟 ERE)。
   - **主 loop 6 项独立核验全绿**: 13 处 credit 正则逐字节一致 (verify_regex_bytes.py) / risky_patterns
     块逐字节一致 / SC-1·6·9a·14·20·21 探针 47/47 / **全语料 305 对拍唯一分歧=KNOWN-LIMIT** / 回归
     365/366 / SC-20 子 shell fail-closed 注错验证。commit `454d29f`。
4. **批 2 = TASK-011..019 (除 016)** (qa-engineer, 主 loop brief 明确 016/020 挂 owner):
   - 测试族: SC-5 分段器单元 / SC-6 降级族 18 项 (直断言 `_sg_safe_to_split`) / SC-14 A5+B2 两组公式 /
     SC-15 credit 双向 + **14 零覆盖分支逐条取 census `branch_table`** / SC-1 五条 (#2/#3/#5 credit-then-risk
     粘性锁) / SC-4 quote-aware / SC-20 python marker-assert 注入 / SC-21 字节相等 / SC-9a 6 条 canonical /
     SC-17 去重 + 无重复用例名自检 + 新 helper `sts_case`/`split_case`/`sc9a_case`。
   - **KNOWN-LIMIT 翻新**: `secret-guard.test.sh:829` (原 :770) `put:...compound credit leak` want 0→2
     (改后逐段化拦得住; 测试作者原就埋了「到时转红强制翻新」的注释)。
   - **主 loop 独立核验**: 回归 **474/474** (亲跑, 不信 agent) / fixture 全段抽查 (形态正确, 去重虚惊
     澄清 — grep -c=2 的第 2 处是注释里的字面名) / **反事实鉴别力独立实证** (counterfactual.sh 拷 test+
     坏hook 到临时目录相对路径跑): 恒fallback→SC-6 2/18 + SC-1 **5/5** (baseline-failing 成立) + SC-14 9 /
     恒split→SC-6 16/18 / 最小粘性→SC-1 #3 (Aria#170 本体被抓)。commit `152cac8`。

## §2 未完成 / Carry-forward 清单

**本 session 新增 (#128 特定)**:

- 🔴 **owner 复议 4 项 (卡 SC-18 + proposal 修订; 全文见 `.aria/notes/2026-08-12-*-count-disputes.md`)**:
  1. `family_count`: proposal 正文 55, census 实跑 **57**。主 loop 独立重写归键器也得 57 (三种合理约定
     得 57/57/56, 无一得 55)。建议采 57 + 写死「`\b` 视作停止字面 token 串」约定。
  2. `newline_affected.strict`: proposal 正文 11, census 实跑 **13**。数学可证 13 (每处判据含 `[[:space:]]`,
     POSIX 含换行 → 必分歧)。11 无可复现口径。建议采 13。
  3. SC-6 反事实表「恒 split」行: proposal 写 15/18, 实测 **16/18** (case 隔离断言在完整 stub 下也红)。
  4. SC-1 反事实「粘性实现」描述: proposal 的「3/5」对应**急切版**粘性; 另有**最小版**只红 #3。不影响
     fixture 正确性 (5 条对两版合起来有完整鉴别力), 但 proposal 宜注明变体以免复核者对不上。
  → 1/2 是 SC-18 机械比对项 (**enabled SC, 裁前不能变绿, Rule #10 不自行豁免**); 3/4 是 proposal 下版
     修订项 (不阻塞)。**四者均非 census/hook bug** (代码回归 474/474 全绿)。
- 🔴 **TASK-016** (SC-19 跨段 fail-open 测量 + SC-7): 依赖 family 裁决定探针集规模 (12 族已覆盖, 余 43 或
  45 族待补)。**owner 裁 55 vs 57 前不宜施工** (返工)。
- 🔴 **TASK-020** (SC-13 三点回填): 依赖全部测试写完的实跑总数 (现 474, 但 016 会再加) + 依赖 016。
- 🔴 **TASK-021/022** (B-验证, **不卡 owner**): 021 全量回归 canonical 直调 + SC-16 可移植性实跑; 022
  五档性能 (改前基线**须经 `git show af87cae:hooks/secret-guard.sh` 提取到独立临时文件**, ⛔ 禁
  stash/checkout 切换工作树, 见 TASK-022 verification + memory `feedback_git_stash_pop_race_recovery_hazard`)。
- 🔴 **TASK-023..028** (ship 前/时/后, **不卡 owner**): 版本 bump (SOT re-check, 现 1.65.5, 并发轨可能推进
  须顺延重算) + aria 5 SOT 文件 + 主仓 gitlink + 14 点核对 + CHANGELOG 两类 + secret-hygiene 回填 + 9 转出
  issue + close #128 + SC-9b harness 链复验。
- 🟡 **census 10 个 pyright lint** (未使用变量, 批 1 `corpus_census.py`): 非功能问题 (21/23 数字实跑正确),
  归 Phase C code review 清理。
- 🟡 **未 push**: aria feature 2 commit (`454d29f`/`152cac8`) + 主仓 master 3 commit (`e18a4c4`/`f97db52`/
  本 handoff)。本 session 收尾双推主仓 master + push aria feature 备份 (见 §7)。

**承前 (来自上一份 handoff, 本 session 未动)**:

- 🟡 **并发轨** (`aria-runner-bot/023236f2`) `premerge-gate-mainbranch-failclosed` post_planning R3 FAIL —
  与本 track「机械闸能否替代规划轮收敛」同题, owner 让先只跑本 track, 未合看。
- 🟡 **Aria #178** 落点判断 (hook 专属还是所有 plugin 分发型产物通病) — 挂 6+ 轮, 判完大概率 Level 2 Spec。
- 🟡 清理 **7 份** handoff 的悬空 memory 引用 `feedback_concurrent_duplicate_audit_fetch_before_start`。
- 承前未动: SilkNode #979 · Aria #175 / #177 · aria-plugin #136 / #137 · #120 / #117 / #123 · 三个 owner 裁量项。

## §3 关键风险 / 已知陷阱

- **四个 spec 复议项都不是代码 bug** — 主 loop 已独立重算/数学论证证成 census 与 hook 正确, 争议在 proposal
  正文的**人工数/描述**。⛔ **下个 session 别为了让 SC-18 变绿去调 census 凑 55/11, 也别改 proposal 迁就
  57/13** (两者 SC-18/TASK-010 明禁) — 唯一合法动作是 owner 裁定后按裁定改**一处** (采 57 则改 proposal;
  坚持 55 则 owner 须给出能复现 55 的归键约定)。
- **census/测试落地反复逼出上游 spec 精度缺陷** (family/newline/SC-6恒split/SC-1粘性 一 session 撞 4 个) —
  这是 A.2/Phase B「把设计逐条落成可执行产物」的固有产出, 与 F-1 (A.2 逼出 SC→Task 表不自洽) 同族。**说明
  六轮 post_spec + 五轴机械闸仍收不了「设计落成可执行物」这一层的精度**, 印证机械闸判据集缺维的一贯诊断
  (memory `feedback_mechanical_gate_axis_set_provably_incomplete`)。
- **agent 自写测试须主 loop 真数据核验** — 批 2 qa-engineer 报告 474/474 + 反事实, 主 loop **亲跑回归 +
  独立注入坏实现复现反事实** (counterfactual.sh), 不仅确认了 agent 的数, 还比 agent 报告更全面 (发现恒
  fallback 同时打红 SC-1 5/5)。这是 memory `feedback_agent_authored_tests_encode_own_bug_false_green` 的
  又一次兑现。
- **gitlink 未 bump 是正确态, 不是遗漏** — feature 未合并, 主仓 gitlink 保持 `af87cae`; 若此时 bump 会指向
  未合并 commit 制造 orphaned gitlink (CLAUDE.md 硬约束 1 / Aria #165 根因)。C.2 合并后才 bump。

## §4 实战教训 (memory 沉淀来源)

```
[候选 memory]
- (无新增) 本 session 的教训全部被现有 memory 覆盖:
  · census/机械计数器落地逼出 spec 人工数错 → [[feedback_spec_inherits_upstream_dec_errors]] +
    [[feedback_meta_dogfood_solution_validates_self_mid_ship]] + [[feedback_never_write_unverified_impossibility_claims]]
  · agent 自写测试须主 loop 真数据核验 → [[feedback_agent_authored_tests_encode_own_bug_false_green]]
  · 反事实必须能证伪 + 坏实现有多变体 → [[feedback_counterfactual_test_for_every_new_sc]]
  · 机械闸/六轮审计收不了「设计落成可执行物」的精度面 → [[feedback_mechanical_gate_axis_set_provably_incomplete]]

[未写下经验]
- 反事实「坏实现」常有多个都合理的变体 (最小粘性 vs 急切粘性), proposal 只写一个红条数会让复核者拿
  另一变体对不上而误判 fixture 有问题 —— 是 counterfactual_test_for_every_new_sc 的补充面 (反事实表须
  注明「该数对应哪种坏实现变体」), 但暂未单列, 因本 session 只 1 例, 观察是否复发再决定沉淀。
```

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| OpenSpec | #128 活跃, proposal v10 + detailed-tasks.yaml (29 task, **19 done / 10 pending**); 收敛态仍 `converged: false` (Phase A override 进的) |
| User Story | 本 session 未动 (US-025 与 #128 无直接关联) |
| PRD | 未动 |
| UPM | Aria 不用 UPM (`upm.configured=false`) |

**consistency flag (advisory)**: 多条 `active_change_not_in_upm` — Aria 不配 UPM, 结构性 noise 非真不一致 (同历次)。
**已做但未在四维反映**: 无。本 session 改动全部落在 aria 子模块 feature 分支 (`hooks/secret-guard.sh` +
`hooks/tests/{secret-guard.test.sh,corpus_census.py}`) + 主仓 `openspec/changes/.../detailed-tasks.yaml` +
`.aria/notes/`。

## §6 Next session 入口 + 优先级建议

入口: `/aria:state-scanner` (会读到本 handoff, phase 应显示 Phase B in-progress)。

1. **先解 4 个 owner 复议项** (轻决策, 但卡 SC-18/016/020) — owner 逐条裁: family 55/57 · newline 11/13 ·
   SC-6 恒split 15/16 · SC-1 粘性变体注记。裁完按裁定改 proposal 正文**一处** (采 census 值则同步 SC-18 断言)。
2. **裁完 family 后做 TASK-016** (SC-19 探针补齐到裁定的家族数, 55 或 57) **+ TASK-020** (SC-13 三点回填,
   secret-hygiene.md 三处 + test 头注释 + SC-11 正文, 权威值=实跑 `PASS: N/N`)。
3. **TASK-021/022 B-验证** (不卡 owner, 可与 1 并行): 021 canonical 全量回归 + SC-16 可移植性; 022 五档性能
   (改前基线经 `git show af87cae:` 提取独立文件, 禁 stash/checkout)。
4. **TASK-023..028 ship** → **Phase C** (aria feature→master 本地 merge + 双推 + gitlink bump + census lint
   清理; 版本 bump 前 re-check SOT, 并发轨可能已推进须顺延重算)。
5. (可选, 承前) 合看并发轨 premerge-gate 的 post_planning 结论 — 与本 track「机械闸能否替代规划轮收敛」同题。

## §7 提交清单 (commit hash + multi-remote parity)

```
aria 子模块 (feature/secret-guard-per-segment-evaluation, 基点 af87cae):
  454d29f  批1  hook 逐段判定 + corpus_census (TASK-001..010)
  152cac8  批2  测试族 (TASK-011..019 除016)
主仓 (master):
  e18a4c4  批1 spec 状态 + owner 复议 note
  f97db52  批2 spec 状态 + note 追加 (2 反事实表误差)
  <本 handoff commit>
```

**push 状态 (收尾时处理)**: aria feature 2 commit **未 push** — 本 session 收尾 push 到 origin+github 做
备份 (feature 分支, 不 bump gitlink, 安全)。主仓 master ahead 2+handoff **未 push** — 双推 origin+github,
逐个 `git ls-remote` 核验 SHA (不信 push 回执, CLAUDE.md 硬约束 2)。**主仓 gitlink 保持 af87cae 不动**
(feature 未合并)。

## §8 Memory entries this session

**无新增**。本 session 的教训全部被现有 memory 覆盖 (§4 已列链接)。唯一未沉淀的观察 (反事实坏实现多变体)
只 1 例, 待复发再决定 — 符合「不保存 repo 已记录的 / 只对本对话重要的」原则。

## Cross-references

- 前序 (同 track, 本容器): [2026-08-12 — #128 A.2/A.3 postplanning + 机械闸第 5 轴](./2026-08-12-issue128-a2-a3-postplanning-and-the-fifth-judge-axis.md) (Phase A 闭环)
- 并发轨 (`aria-runner-bot/023236f2`): [2026-08-11 — premerge-gate 换人执笔 + 机械交叉检查](./2026-08-11-adjudication-authoring-swap-and-the-mechanical-crosscheck.md)
- owner 复议项全文: `.aria/notes/2026-08-12-secret-guard-128-phaseb-batch1-count-disputes.md`
- spec: `openspec/changes/secret-guard-per-segment-evaluation/{proposal.md (v10), detailed-tasks.yaml (19/29 done)}`
