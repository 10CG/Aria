---
checkpoint: pre_merge
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-02T17:33:15.838Z
context: PR #190 linked-issue-field-availability (main 265a5f9 / aria d1caa66 / standards ffed204)
agents: [tech-lead]
---

# Pre-merge R4 (稳定性确认轮) — tech-lead 席

> 镜头: 多仓集成 / 发版面 / 流程合规 / 合并安全。fresh 席位, 先读 R1/R2/R3 三份聚合, 再在 265a5f9 / d1caa66 / ffed204 上独立重审。
> **实物面 (gitlink / 双远端 / tag peel / 16 点版本面 / merge 安全 / C.2.4 / C.2.4.5 / 探针 / 53+1462 测试 / 新 check 四态 / token 活性): 零 finding, 连续第三轮。**
> 本轮全部 finding 落在**记录面与流程口径**: 三轮清账自身留下的当前态残余 + 收敛判据的成文依据。

## 审计结论

- [major] documentation/`docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md`: R3「机械扫描残余 = 0」被证伪 —— 同一文件内 `:11` `:14` `:126` 仍写「R1/R2 已清账, R3/R4 稳定性确认」, 与 R3 自己改过的 `:4` `:152` `:179`「R1–R3 已清账」直接矛盾; 扫描器与其输出均不在仓内, 该证据不可复核 — 证据: `sed -n '14p'` = `> **Status**: Active — H1 四处推送完成; PR #190 pre_merge 收敛审计 R1/R2 已清账, R3/R4 稳定性确认后按 owner 指令合并 → D 归档` vs `sed -n '179p'` = `**Status**: Active — … R1–R3 已清账, R4 稳定性确认后…`; `git show 265a5f9` 的 handoff hunk 只动 frontmatter/§5/§6/§7, `:11`/`:14`/`:126` 一字未改; `git ls-files | grep -i stale` 无扫描器 (type=issue) — finding_id `a3bfd693`
- [major] architecture/`.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md`: 「收敛口径」行把稳定性比较集从成文的**全结论集**改成自创的「可执行结论集 (C∪M)」, 且理据自相矛盾 —— 用全集非空来否掉 0-finding 守卫, 同时用 C∪M 空来宣布收敛; 二者不能并存 — 证据: SOT `aria/skills/audit-engine/SKILL.md:220-223` `current_keys = {(r.type, r.severity, r.category, r.scope) for r in round_N}` (severity 是键的分量 ⇒ minor 在集内) + `references/convergence-algorithm.md:60`「Round 1 = ∅ … 不视为收敛, 必须进入 Round 2」; `grep -rn '可执行结论集'` 全仓仅命中本决策单 `:122` 与本轮审计报告自身, `grep -rn 'C∪M' aria/skills/audit-engine/ standards/` 零命中 (type=decision) — finding_id `3b277328`
- [minor] documentation/`docs/handoff/latest.md`: R3 清账**完全未触碰**本文件, `:4` `:13` `:23` 三处仍是 R2 时点陈述「R1·R2 已清账 → R3/R4 稳定性确认」, 与 handoff frontmatter `:4`「R3 0C/1M 已清账」跨文档矛盾 — 证据: `git show --name-only --format='' 265a5f9 | grep handoff` 只列 `2026-09-02-linked-issue-field-b2-…md` (latest.md 不在其中); `git show --name-only --format='' fdfb183 | grep handoff` 两文件都在 (type=issue) — finding_id `1d2fe175`
- [minor] documentation/`PR#190/body`: L32 整条已被实测推翻 (「master 已前进到 `882707f`」实为 `c423281`; 「`forgejo-app-token-liveness` 在本分支报指纹漂移」实跑为 OK); L41 记 R3 为「0C / 1M / 5m」而 R3 聚合是 1 Major / 4 Minor (同款错在决策单 `:114` 也有一份) — 证据: 实跑 `python3 .aria/probes/forgejo-app-token-liveness.py` → `OK (2 枚应用级 token 活性正常, 指纹与台账一致)` exit 0; `git ls-remote origin master` = `c423281a9b1e…`; R3 聚合 `:36`「0 Critical / 1 Major / 4 Minor」 (type=issue) — finding_id `b66c5239`
- [minor] documentation/`openspec/changes/linked-issue-field-availability/detailed-tasks.yaml`: `:66` `metadata.status` 仍写「TASK-025 in_progress (主仓 PR #190, pre_merge 收敛审计 R1/R2 已清账)」, 归档门消费的三份文件里只有这份没跟上 R3 (tasks.md `:5` 与 proposal Status 行均已是轮次无关表述) — 证据: `sed -n '66p' openspec/changes/linked-issue-field-availability/detailed-tasks.yaml` 逐字含「pre_merge 收敛审计 R1/R2 已清账」 (type=issue) — finding_id `95f02272`

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **2** / Minor **3**。

交付物本体 (代码 / 测试 / 版本面 / gitlink / 合并安全 / Rule #6·#8·#10) 我这轮零异议; 两条 Major 一条是三轮清账自身的残余 (第四轮同形), 一条是决定「何时停止审计」的判据缺成文依据。

**C ∪ M = 2 ≠ ∅** ⇒ 按本轮任一口径 (成文全集比较 / 决策单 C∪M 口径) 都**不能声称 CONVERGED**。

## 投票

**REVISE**

理由 (只列我认为必须在合并前处置的):

1. `3b277328` —— 合并这个动作的授权链条是「CONVERGED ⇒ 合并」。判据本身没有成文依据、且理据自相矛盾时, 先把判据摆正再执行合并, 否则合并是建立在一个 AI 自造的口径上 (Rule #10 末句: AI 自作主张的流程判断必须写进 handoff 请复议)。**可在本循环内完成的最小处置**: 决策单「收敛口径」行改写为「这是对 `convergence-algorithm.md` 的偏离, 不是它的一种读法」+ handoff §2 加一条 owner 复议项。把口径写进 SOT 是另一交付面 (`references/` 属处方性指令面, 须过 Rule #6), 不必在本循环做。
2. `a3bfd693` —— 这份 handoff 是 Rule #9 canonical, 且自称「Next session 入口: 优先读本 doc」。合并后它就是 master 上的永久记录, 而它的 §Status 与自己的 footer 互相矛盾。三处 prose 编辑, 成本极低。

对 `1d2fe175` / `b66c5239` / `95f02272` 我不坚持合并前修, 但它们与 `a3bfd693` 是同一次编辑该覆盖的范围 (memory `fix-the-class-not-the-instance`), 建议同批。

**若这两条处置完毕, 我对合并本身无保留意见** —— 实物面我这轮做了 11 项独立复核, 全部成立。

## 核验记录

### 1. gitlink × 双远端 × tag peel (实物面)

```
$ git ls-tree origin/feature/linked-issue-field-availability aria standards aria-orchestrator
160000 commit d1caa66cb375c2799f55def453ca232c66a18c22	aria
160000 commit 237045ac2cfed9849c201e18434e9f6cb9036ab5	aria-orchestrator
160000 commit ffed2040dff7964cf9d137e85e174173d2c685b9	standards
$ git ls-tree origin/master aria standards aria-orchestrator
160000 commit d69091dfdeb0c6cd83b03da2492812d33cec3712	aria
160000 commit 237045ac2cfed9849c201e18434e9f6cb9036ab5	aria-orchestrator
160000 commit 334c609ef55d4c5970ea1ea7e91d64193478e726	standards
```
⇒ 本 PR 只 bump aria / standards, **aria-orchestrator gitlink 未动** (base == head == 237045a)。

```
$ git -C aria ls-remote origin master   → d1caa66cb375c2799f55def453ca232c66a18c22	refs/heads/master
$ git -C aria ls-remote github master   → d1caa66cb375c2799f55def453ca232c66a18c22	refs/heads/master
$ git -C standards ls-remote origin master → ffed2040dff7964cf9d137e85e174173d2c685b9	refs/heads/master
$ git -C standards ls-remote github master → ffed2040dff7964cf9d137e85e174173d2c685b9	refs/heads/master
```
四条独立 `ls-remote` 与两个 gitlink 逐字一致 (CLAUDE.md 硬约束 2: 不信 push 回执)。

两 tag 双端 peel:
```
$ git -C aria ls-remote origin 'refs/tags/v1.68.1*'
5b9de8e041311b7bc84f8275c20df74fd273ef93	refs/tags/v1.68.1
d1caa66cb375c2799f55def453ca232c66a18c22	refs/tags/v1.68.1^{}
$ git -C aria ls-remote github 'refs/tags/v1.68.1*'   → 同上两行逐字相同
$ git -C aria ls-remote origin 'refs/tags/v1.68.0*'
c6aad0dc1dd53a519ea4edb4da9656312e2846c0	refs/tags/v1.68.0
fe324414f3d8e0ad5284afa82e0154f18ea049d6	refs/tags/v1.68.0^{}
$ git -C aria ls-remote github 'refs/tags/v1.68.0*'   → 同上两行逐字相同
```
两个 annotated tag 的 peel 目标各自等于 v1.68.1 = gitlink / v1.68.0 = 前一 commit; `merge-base --is-ancestor fe32441 d1caa66` → YES (handoff `:127`「d1caa66 ⊇ fe32441」成立)。

**R3 后子模块零推送 (自查)**: 上面 aria origin master 仍 `d1caa66`、standards origin master 仍 `ffed204`, 与 R3 简报所记同值 ⇒ 决策单 B9-补「本循环内不再推任何子模块 commit」在 R3→R4 之间**被遵守**。两子模块工作树 `git status --short` 均为空, `git submodule status` 只有 aria-orchestrator 带 `+` (92acce5 有意停泊, handoff `:22`/`:133` 两处成文, 且 anchor 列为 out_of_scope)。

### 2. 版本面 16 点 (aria 5 文件 + 主仓 16 引用点, 旧值零残留)

aria 侧 5 文件 (SOT = `plugin.json`):
```
aria/.claude-plugin/plugin.json:4     1.68.1   ← SOT
aria/.claude-plugin/marketplace.json:3,16  1.68.1 ×2
aria/VERSION:3                       1.68.1   (:4-:5 的 1.68.0 是「发布日期(旧)」账本行)
aria/CHANGELOG.md:13                 ## [1.68.1]  (:17 起为 1.68.0 历史条目)
aria/README.md:5                     1.68.1
```
主仓 16 点 (= TASK-024 的 14 点 + R1 新纳入同步面的 2 行), 逐点实读:
```
CLAUDE.md:139 / :141                          v1.68.1  (2)
VERSION:24  | aria (插件) | v1.68.1 |          (1)
README.md:8 badge / :242 Plugin Version       1.68.1   (2)
README.zh.md:3/:10/:244                       1.68.1   (3)
README.ja.md:3/:10/:244                       1.68.1   (3)
README.ko.md:3/:10/:244                       1.68.1   (3)
docs/architecture/system-architecture.md:189  v1.68.1  (1)
docs/architecture/version-scheme.md:23        v1.68.1  (1)
                                              ── 合计 16
```
旧值残留扫描: `grep -rn '1\.67\.2' . --exclude-dir={.git,aria,standards,aria-orchestrator,ab-results,audit-reports}` 命中 18 处, **逐条判为历史锚点**, 无一是当前值断言 —— 全部是 (a) 各 Spec 的 `scope_repo_head` / 基线 SHA 标注 (`d69091d (v1.67.2)`), (b) 决策单 H1a/H1b 的先例论证, (c) `.aria/state-checks.yaml:377-378` 新 check 的「来源」说明 (记的正是 1.67.2→1.68.0 那次漂移)。

### 3. 新 check `plugin-version-arch-docs-match` — 副本上实跑四态

在 `/tmp/.../scratchpad/r4check/` 的独立副本上逐字执行 `.aria/state-checks.yaml` 里的 command (仓内文件零改动):
```
STATE 1 baseline         → OK plugin=1.68.1 (2 arch doc rows match)                    rc=0
STATE 2 system-arch 漂移  → DRIFT plugin=1.68.1 vs system-architecture.md=1.60.0        rc=1
STATE 2b version-scheme 漂移 → DRIFT plugin=1.68.1 vs version-scheme.md=1.61.0          rc=1
STATE 3 删掉 arch 行       → MISSING system-architecture.md §2.8 aria-plugin 行          rc=1
STATE 4 plugin.json 不可读 → ##SKIP## aria/.claude-plugin/plugin.json 不可读             rc=0
```
两条腿**各自独立**能翻红 (不是只有一条承重); 缺行走 fail-CLOSED 而非静默 OK; 零证据走 SKIP 而非假绿。健康常态下取值 = OK ⇒ 不是恒红。R2 minor `d91f074e` (无专属回归测试) 的 carry (C6) 我核为成立且合理。

### 4. 合并安全

```
$ git rev-parse origin/master                 → c423281a9b1e5d04ebf62bd3132cc63eecd366f1
$ git rev-parse master                        → c423281a9b1e5d04ebf62bd3132cc63eecd366f1   (本地 master 未陈旧, memory stale-local-main)
$ git ls-remote origin master / github master → 两条均 c423281a9b1e…                      (主仓两端已一致)
$ git log --oneline origin/master ^HEAD       → (空)
$ git merge-base --is-ancestor origin/master HEAD → YES (fast-forwardable)
$ git merge-tree --write-tree origin/master HEAD  → 8519c9e439e548cbb77330bf1f84fcf797188373 (exit 0, 输出 0 行 conflict)
$ git ls-tree 8519c9e aria standards aria-orchestrator
  d1caa66… aria / 237045a… aria-orchestrator / ffed204… standards
```
**post-merge 树的三个 gitlink 在各自双远端可解析**: aria d1caa66 与 standards ffed204 已由 §1 的四条 `ls-remote` 直接坐实; aria-orchestrator 237045a `branch -r --contains` → `github/master` + `origin/master` 双端命中 ⇒ 合并后 `clone --recursive` 不会断 (无 orphaned gitlink)。

**C.2.4 (Rule #8) 对当前 head 重跑**:
```
$ python3 aria/skills/phase-c-integrator/scripts/pre_merge_gate.py \
    --pr-branch feature/linked-issue-field-availability --main-branch master --remote origin
{"verdict": "green", "pr_ci_status": "not_applicable", "in_flight_runs": [],
 "primitive_used": "aether-ci-cli", "primitive_version_sha": "f29abee",
 "raw_message": "path_coverage: no workflow covers changed files (reason=no-triggering-paths); PR CI wait skipped (not_applicable); main in-flight clear",
 "path_coverage": {"decision": "not_applicable", "workflows_scanned": 3, "matched_workflows": [],
                   "changed_files_count": 87, "reason": "no-triggering-paths", "dispatchable_workflows": []}}
exit 0
```
`primitive_used = aether-ci-cli` (真 backend, 非 stub, 未走 `no_ci_fallback` 静默降级) ⇒ Rule #8 满足。`not_applicable` 我复核了三个 workflow 的触发面: `issue-triage-tests.yml` paths = `aria/skills/issue-triage/**` (对裸 `aria` gitlink 结构上不命中, = R1 carry C1); `submodule-gate-tripwire.yml` 头部 `⚠️ DEPRECATED for execution` 且只有 `workflow_dispatch` (审计已迁 host cron); `build-aria-runner.yaml` 与本 PR 改动面无交集 ⇒ 判定属实, 不是漏配。

**C.2.4.5 对当前 head 重跑**:
```
$ ARIA_SUBMODULE_GATE_MODE=block bash aria/skills/phase-c-integrator/scripts/submodule_gate.sh
GATE: submodule=standards master=334c609… feature=ffed204…
PASS: standards forward bump
GATE: submodule=aria master=d69091d… feature=d1caa66…
PASS: aria forward bump
OK: aria-orchestrator unchanged (237045a…)
✓ submodule_gate: all submodules unchanged/forward/first-time (mode=block)
exit 0
```
**非空真核验 (对抗)**: 两个被 bump 的子模块都打印了 `GATE:` 行, 说明走的是祖先比较分支而非 `unchanged` 捷径; 反向对照 `git -C aria merge-base --is-ancestor d1caa66 d69091d` → **rc=1**, 即 backward bump 不会落进 `:266` 的 forward 分支, 会掉到 `:273` 的 BLOCK 路径。⇒ 这个 PASS 有判别力。

`.aria/probes/forgejo-app-token-liveness.py` 实跑:
```
OK (2 枚应用级 token 活性正常, 指纹与台账一致)
  aria-layer1-forgejo: OK http=200 fp=c957308a
  aria-layer2-git:     OK http=200 fp=3105220d
exit 0
```
(此即 finding `b66c5239` 中 PR body L32 被推翻的那条。)

### 5. 交付面功能复核 (简报强制项 + 对抗)

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
Ran 53 tests in 3.053s / OK
$ python3 run_tests.py            (全量)
Ran 1462 tests in 68.180s / OK    exit 0
```
⇒ PR body L15 与 tasks.md `:5` 的「53 / 1462」两个数**我自己跑出来一致**。

```
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . \
    --grandfathered .aria/linked-issue-field-grandfathered.txt
OK (9 份在范围内, 6 条在册)                       exit 0
$ … --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
10CG/Aria#174                                     exit 0   (无换行, 逐字节)
$ … --emit-arg openspec/changes/linked-issue-field-availability/proposal.md
(空)                                              exit 0   (本 Spec 自身写 `none` 哨兵 ⇒ E6 不产生实参, dogfood 成立)
$ … . --emit-arg <path>       (互斥)
error: --emit-arg 与位置参数 root 互斥 (root 仅 check 模式)   exit 2
```
9 份在范围 = `openspec/changes/*/proposal.md` 实际 9 个; 6 条在册 = 白名单 6 行 ⇒ 3 份合规, 与白名单头注「回填一份删一条」自洽。

**对抗核验 (C9 carry 是否属实)** — 在 scratchpad 造合成仓, 一 good 一 bad:
```
A 两目录可读, bad 不在册        → FAIL 1 项 / bad-spec/proposal.md:- NO_FIELD …   rc=1
B bad-spec 目录 chmod 000       → OK (1 份在范围内, 0 条在册)                      rc=0   ← fail-open by omission
C bad-spec/proposal.md chmod 000 → FAIL 1 项 / :- UNREADABLE PermissionError       rc=1   ← fail-closed 正确
```
⇒ 决策单 C9 对缺陷形状的描述**逐字属实**且边界划得准 (文件不可读已 fail-CLOSED, 只有目录不可读会漏), 前置需手工 chmod (git 不存目录权限) ⇒ 维持 minor + carry v1.68.2, 我不重报。同理 R2/R3 明确 carry 的 `ae4f1c9f` / `2ed89c8a` / `a2a4165f` 我复核 carry 裁定成立, 不重报。

### 6. Rule #6 / #8 / #10 合规再核

- **Rule #6**: v1.68.0 动了 `skills/spec-drafter/SKILL.md` 两 hunk = 处方性·运行时指令面 ⇒ 照跑, 结果在 `ab-results/2026-09-02-v1.68.0-linked-issue-field-rule6/`, CHANGELOG 明写「不申请豁免」。v1.68.1 的 `rule6_note: substitute` 我做了机械核对: `git -C aria diff --name-only fe32441 d1caa66` = 7 文件 (版本 5 文件 + 探针 + 测试), `| grep -c 'SKILL.md'` = **0** ⇒「零 SKILL.md 指令面变更」属实, substitute (5 条对 v1.68.0 探针 baseline-failing 的结构化测试) 合判据表第 1 行。
- **Rule #8**: `.aria/config.json` `phase_c_integrator.pre_merge_gate.enabled = true`, gate 实跑 green 且用真 backend (见 §4)。
- **Rule #10**: `.aria/config.json` `audit.checkpoints.pre_merge = "off"` ⇒ 本次 pre_merge 审计是 owner 显式调用而非 AI 跳过 enabled 闸门, **不构成自我豁免**; 反过来 enabled 的 C.2.4 / C.2.4.5 两个闸门本轮都真跑了。⚠️ Rule #10 的**末句**(自作主张的流程判断须写进 handoff 请复议) 未被满足 —— 见 finding `3b277328`: 收敛口径的偏离只写在决策单与 PR body, handoff §2「高优先级 (owner 动作门)」里没有对应的复议项。
- Rule #4 (Conventional Commits): `origin/master..HEAD` 12 个 commit 全部合规 (`docs(pr190)` / `fix(pr190)` / `feat(state-checks)` / `chore(release)` / `test(benchmarks)` …)。Rule #5 (Spec 落本项目 `openspec/changes/`) / Rule #9 (handoff 落 `docs/handoff/`) 均成立。

### 7. 跨文档一致性扫描 (三轮清账是否引入新矛盾)

自写扫描, 对 7 份被改文档跑 4 条「R3 仍待办」形态正则:
```
docs/handoff/2026-09-02-…-push-auth.md:11   [R3R4-pending]      → R3/R4 稳定性确认后合并
docs/handoff/2026-09-02-…-push-auth.md:14   [only-R1R2-cleared] → R1/R2 已清账, R3/R4 稳定性确认后…
docs/handoff/2026-09-02-…-push-auth.md:126  [only-R1R2-cleared] → R1/R2 已清账, **R3 (+R4 稳定性确认) → 合并**
docs/handoff/latest.md:4                    [R3R4-pending]      → … → R3/R4 稳定性确认后合并 → D 归档
docs/handoff/latest.md:13                   [only-R1R2-cleared] → 收敛审计 R1·R2 已清账, R3/R4 后合并
docs/handoff/latest.md:23                   [R3R4-pending]      → … → R3/R4 稳定性确认 → 合并。
openspec/…/detailed-tasks.yaml:66           [only-R1R2-cleared] → TASK-025 in_progress (…R1/R2 已清账)
```
`proposal.md` / `tasks.md` / `CLAUDE.md` / 决策单 零命中 (前两者用的是轮次无关表述, 正确)。

已核**成立**、不重报的三轮处置:
| 轮 | id | 处置 | 我的独立复核 |
|---|---|---|---|
| R1 | `ac44ace3` | arch 两行 + 新 check | 成立 — 两行皆 1.68.1, check 四态实跑有判别力 (§3) |
| R1 | `e4cde200` / `ae4f1c9f` / `2ed89c8a` / `a0ff4897` / `4605dc4d` | aria/standards 侧 | 成立 — 53 测试全绿, 探针五项加固行为实测符合 CHANGELOG 描述 |
| R2 | `ee23ca88` | Spec 三文件口径 | **部分成立** — proposal / tasks.md 成立 (tasks.md `:5` = 53 / 1462 / **1894** 与实跑一致), yaml `:66` 未跟 R3 ⇒ 新报 `95f02272` |
| R2 | `a04601ce` / `c2e60555` | arch 2.0.2 行 / 推送授权面自纠 | 成立 — `system-architecture.md:967` 有 2.0.2 行; B9-补的「不再推子模块」在 R3→R4 间被遵守 (§1) |
| R3 | `62285020` | tasks.md 1889 → 1894 | 成立 |
| R3 | `b66c5239` (TASK-014 留记) | PR body L22 + handoff `:136` | 成立 — 且判据 `git -C aria branch -a \| grep a1-entry` 实跑为空, 母 Spec 分支确实不存在 |
| R3 | `a3bfd693` (类级清账) | 机械扫描零残余 | **不成立** ⇒ 重报 (见 finding) |
| R3 | C8 / C9 | 决策单落行 | 两条判据都可证伪, 且 C9 我实测复现 (§5) |

### 8. 本轮未做 / 已知边界

- 未跑 `/state-scanner`、未跑 `phase1_gate` / `release_gate` (简报禁令); 未做任何仓内写操作 —— 我的唯一写入是本报告, 三态测试与对抗夹具全部在 scratchpad 副本上。
- `refs/aria/coordination` 上 a1-entry 轨 3 条 active claim (R1 carry `6ab01600` / 决策单 C2) 我只读确认仍是 D.2b 的事, 不重报。
- 母 Spec / 探针 Spec 内容、M6-M7 六份 proposal 回填、proposal 正文理据勘正 (B3)、AB iteration-2 —— 按 anchor 属 out_of_scope, 未审。
