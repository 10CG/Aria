---
checkpoint: pre_merge
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-02T13:32:08.906Z
context: PR #190 linked-issue-field-availability (main 0e9619c / aria fe32441 / standards fad8b4b)
agents: [tech-lead]
---

## 审计结论

- [major] documentation/docs/architecture/system-architecture.md: 合并即产生**新的**版本面漂移 — 并发 master commit `c423281` (今天, "2.0.1 复审校准 … §2.8 版本表") 把 `:189` 校准到 `v1.67.2` (当时正确, master gitlink = aria d69091d = 1.67.2); 本 PR 把 gitlink 推到 fe32441 = plugin.json **1.68.0**, 合并后该行即为假。同类第二处 `docs/architecture/version-scheme.md:23` = `v1.67.1` (已落后两版, 且 c423281 没顺手改)。这两处是**全部**落在 CLAUDE.md 声明的「14 点发布同步面」之外的当前值断言点, 且 13 条 state-check 里无一覆盖 (`m6-version-badge-match` 只比 README badge, `i18n-readme-translation-currency` 只比 3 份 i18n, `main-project-version-consistency` 只比主项目 1.7.5)。— 证据: 总体 = `git ls-files | grep -v '^aria/\|^standards/\|^aria-orchestrator/\|^docs/handoff/\|ab-results/\|^\.aria/audit-reports/\|^\.aria/decisions/\|^openspec/'` = **1427** 个 tracked 文件, 对其 `grep -Hn 'v\?1\.6[0-9]\.[0-9]'` 后剔除历史记述 (triage-report / DEC 存档 / AB fixture / CHANGELOG), 剩当前值断言点 16 个: 14 个在同步面内**全部 = 1.68.0** (README.md :8/:242 · README.zh/ja/ko .md 各 :3/:10/:244 · CLAUDE.md :141 · VERSION:24, 逐点实读), 2 个在面外且**都陈旧**; `git cat-file -p 2004478…:docs/architecture/system-architecture.md | sed -n '189p'` (2004478 = `git merge-tree --write-tree origin/master origin/feature/…` 产出的合并树) ⇒ `| aria-plugin | v1.67.2 | \`aria/.claude-plugin/plugin.json\` |`; `sed -n '23p' docs/architecture/version-scheme.md` ⇒ `v1.67.1`。(type=risk) finding_id = `ac44ace3`
- [major] documentation/aria/skills/spec-drafter/SKILL.md: hunk A 的**顺序条款**「与 SOT 模板头部逐行对齐 (`Level` → `Status` → `Created` → `Linked Issue`)」在**产出物**一侧零机械宿主 —— SC-7a 只在 `### Level 2 预览` 围栏 (模板文本) 内求值 (proposal.md:546 逐字「块边界 = 该围栏; 断言只在围栏内求值」), 纯函数与探针**完全位置无关** (`grep -n 'order\|position\|顺序' lib/linked_issue_field.py scripts/linked_issue_field_probe.py` ⇒ 仅一条无关注释 `:19`; 实跑 `extract_linked_issue_field("…> **Status**…> **Created**…> **Spec Level**…> **Linked Issue**: \`10CG/Aria#1\`")` ⇒ `verdict='OK'`)。实测作用域 9 份 proposal **0/9** 符合该顺序 (三份 a1-entry 族均为 `Status→Created→Spec Level→Linked Issue`, 六份 M6/M7 为 `Level→Status→Change ID→…`), 而 AB 的 A4 断言**正是**把这一偏离判 FAIL (RESULT.md §1 control eval-3「A4 四行顺序 FAIL: 无 `> **Level**` 行, 改名 `> **Spec Level**: 2` 且挪到第三位」)。更硬的一面是前向的: O-1 回填指令的两个宿主 —— `.aria/linked-issue-field-grandfathered.txt` 头注 (「回填一份删一条」) 与 `.aria/state-checks.yaml` 第 13 条 `fix:` (「在被点名的 proposal.md 头部 blockquote 补一行」) —— **都不提位置**, 6 份在册的 M6/M7 回填将各自再造一处偏离, 且没有任何东西会发红。— 证据: 上述实跑 + `grep -c '位置\|顺序\|Level.*Status.*Created' .aria/state-checks.yaml` 在第 13 条 fix 段 = 0; 9/9 顺序普查脚本输出见 §核验记录 (5)。(type=risk) finding_id = `9ac5533a`
- [minor] documentation/docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md: 并发基线**少算一个 commit** — handoff `:144` 与 PR body「注意」段均写「master 已前进到 `882707f`」「feature 分支基 e1deaf1 **落后 1**」, 实际 `origin/master` = `c423281`, `git log --oneline origin/master ^HEAD` 返回 **2** 条 (c423281 + 882707f)。「与本轨零文件重叠」这一结论的**总体只算了 882707f**。我按真实基线独立复算后结论仍成立 (见核验记录 3), 但被漏算的 `c423281` 恰好是唯一动 `docs/architecture/system-architecture.md` 的 commit —— 即 finding `ac44ace3` 逃逸的近因就是这次总体不完整 (memory `critique-repeats-error`: 报数字必须并列总体/范围/计数法)。— 证据: `git log --oneline origin/master ^HEAD` ⇒ 2 行; handoff `:143` 自身写的 `master = c423281` 与 `:144` 的 `882707f` 在同一段互相矛盾。(type=issue) finding_id = `82513c94`
- [minor] architecture/.forgejo/workflows/issue-triage-tests.yml: 主仓唯一为守 aria 子模块而设的 workflow (文件头逐字「Runs pytest for `aria/skills/issue-triage/tests/` from the main repo context」) 的 `paths: ['aria/skills/issue-triage/**']` 对 **gitlink bump 结构上不可能命中** —— 子模块指针变更在 changed-files 里是裸路径 `aria` (`git diff --name-only origin/master...HEAD` 第 11 行逐字 `aria`), 不是 `aria/skills/…`。经验证据: 全仓 CI 历史 `forgejo GET /repos/10CG/Aria/actions/tasks?limit=20` ⇒ `total_count: 11`, 11 条全是 `tripwire` (5) + `Build & Push aria-runner` (6), **`issue-triage tests` 零次运行**, 而期间 aria 的 issue-triage 已多次 ship (aria/VERSION:6 记 v1.67.1 含 issue-triage collector 四缺陷批)。本 PR 的 C.2.4 `not_applicable` 判定本身**正确**且已按 SKILL 义务 surface (handoff `:142` + PR body 逐字「C.2.4 green [not_applicable: 70 变更文件无 workflow 覆盖, main in-flight 已核]」), 但「无覆盖」的一半是这条恒不触发的 workflow 造成的 (memory `false_green_dual_is_permanent_red` / `completion_signals_vs_runtime_invocation`)。**非本 PR 引入, 不在 diff 内**, 不阻塞合并。— 证据: 上述两条实跑。(type=risk) finding_id = `5333fe78`
- [minor] architecture/refs/aria/coordination:claims/023236f2/: Layer L 陈旧 active claim — `git ls-tree -r refs/aria/coordination` 下 `claims/` 有 **3 条** a1-entry 轨 claim 同时 `status: active`: `s-26ad@0914.yaml` (claimed 2026-08-23T09:14:48Z, track_id `a1-entry-claim-duplicate-work-guard`, phase A) / `s-6389@0120.yaml` (2026-08-25T01:20:15Z, 同 track_id, phase A) / `s-0873@0641.yaml` (2026-09-02T06:41:44Z, track_id `a1-entry-claim-duplicate-work-guard-023236f2`, phase B, 本轨)。前两条 10/8 天未 reconcile 到 `done`, 且与本轨 track_id 只差容器后缀 —— 下一件事正是同族 `sibling-spec-probe` 与母 Spec 进 B.1, 认领时可能撞上自己的历史 claim (memory `concurrent_feature_collision_claim_before_build` 的反向形态)。本轨 claim `heartbeat_at` 停在 06:41:44Z, 距审计起点 13:17Z ≈ 6.6h。**非本 PR 引入**; 按简报纪律未跑任何闸门脚本, 只读 ref 树。— 证据: 上述 `git ls-tree` + 逐 blob `git show refs/aria/coordination:claims/…`。(type=risk) finding_id = `9a856513`

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **2** / Minor **3**。

两条 Major 都**不阻塞合并**: `ac44ace3` 是 2 行文档改动, 落在合并后的 `phase-d-closer` commit 里成本更低 (改本分支会破坏审计 anchor 的 source_sha); `9ac5533a` 是前向设计缺口 (6 份待回填才会兑现), 修法是往 `state-checks.yaml` 第 13 条 `fix:` 与白名单头注各加一句位置说明, 或显式把顺序条款的适用面写成「仅新建时」。三条 Minor 里两条明确标注**非本 PR 引入**。

本 PR 在我这四个镜头 (多仓集成 / 发版面 / 流程合规 / 合并安全) 上的核心项**全部干净**: gitlink 双远端四点一致 + tag 指向正确、发版同步面 14 点零残留、check 注册只用既有 7 键且解析不抛、merge-tree 无冲突且与两条并发 commit 文件集不交、Rule #6 逐 hunk 五格证据齐备且降级措辞诚实、无任何 enabled 闸门被自行豁免、接缝占位串三宿主逐字节同一。

## 投票

**PASS**

不存在必须在合并前修的 finding。建议 owner 合并, 并把 `ac44ace3` 的两行改动并入合并后的第一个 commit (`phase-d-closer` 归档 commit 是天然落点), `9ac5533a` 与 `5333fe78` 各开一条 issue。

## 核验记录

### 1. gitlink 完整性 (硬约束 1/2, Aria #165 形状) — 全部 PASS

```
$ git ls-tree origin/feature/linked-issue-field-availability aria standards
160000 commit fe324414f3d8e0ad5284afa82e0154f18ea049d6	aria
160000 commit fad8b4b6487f0362e6f947f0bc0651d5e94c5732	standards
$ git -C aria ls-remote origin master   ⇒ fe324414f3d8e0ad5284afa82e0154f18ea049d6	refs/heads/master
$ git -C aria ls-remote github master   ⇒ fe324414f3d8e0ad5284afa82e0154f18ea049d6	refs/heads/master
$ git -C standards ls-remote origin master ⇒ fad8b4b6487f0362e6f947f0bc0651d5e94c5732	refs/heads/master
$ git -C standards ls-remote github master ⇒ fad8b4b6487f0362e6f947f0bc0651d5e94c5732	refs/heads/master
$ git -C aria ls-remote --tags origin v1.68.0 ⇒ c6aad0dc1dd53a519ea4edb4da9656312e2846c0	refs/tags/v1.68.0
$ git -C aria ls-remote --tags github v1.68.0 ⇒ c6aad0dc1dd53a519ea4edb4da9656312e2846c0	refs/tags/v1.68.0
$ git -C aria rev-parse v1.68.0^{commit}      ⇒ fe324414f3d8e0ad5284afa82e0154f18ea049d6   # == gitlink
```

四条 `ls-remote` 各自独立取值 (不信 push 回执, memory `partial-push`), 两子模块两 remote **四点全一致**, tag 在两端是同一个 annotated tag 对象 `c6aad0d` 且 peel 到 gitlink SHA。⇒ 合并后 GitHub `clone --recursive` 不会断。

主仓自身镜像亦无先存分叉: `git ls-remote origin master` = `git ls-remote github master` = `c423281` (与本地 `origin/master` 一致)。主仓走 Forgejo merge 是硬约束 1 明写的例外 (主仓无「被 bump gitlink」的下游), 但合并后主仓 master 仍须双推 —— handoff `:126` 只写「merge 后 `ls-remote` 两端一致」而未逐字写「推 github」, 不另开 finding (核验动作在, 且 §7 已列两端 parity 惯例)。

### 2. 版本面 — 全部 PASS

aria 5 文件: `plugin.json:4` = `1.68.0` (SOT) / `marketplace.json` **两点** `:3` `:16` = 1.68.0 / `README.md:5` = `> **Version**: 1.68.0 | **Released**: 2026-09-02` / `VERSION:3` = 1.68.0 且账本**只增不改** (`git -C aria show d69091d:VERSION | wc -l` = 176 → `wc -l < aria/VERSION` = 177) / `CHANGELOG.md:13` = `## [1.68.0] - 2026-09-02`。

主仓 14 点逐点实读 (自己 grep, 非引 PR body): 见 finding `ac44ace3` 证据段, 全部 1.68.0; 旧值 `1.67.*` 在同步面内**零残留** (`grep -n '1\.67' aria/.claude-plugin/plugin.json aria/.claude-plugin/marketplace.json aria/README.md` 无输出; VERSION/CHANGELOG 是 append 账本, 1.67 条目为预期)。

计数一致性: `plugin.json` description 声称「42个 Skills (35 user-facing + 7 internal) + 11个 Agents」—— 实测 `find aria/skills -maxdepth 2 -name SKILL.md | wc -l` = **42** ✅ (`ls -d aria/skills/*/ | wc -l` = 43, 多出的 `aria/skills/session-closeout/` 无 SKILL.md, 不计); `ls aria/agents/*.md | wc -l` = **11** ✅。description 字符串本身在 `git -C aria diff d69091d fe32441 -- .claude-plugin/` 中**未改动** (只改 version 行), 故不触发 Rule #6 的 description 分支。

MINOR 判据 (决策单 §H1a 可证伪条款逐字: 「发版时 `aria/CHANGELOG.md` 新条目首节为 `### Added` 且 plugin.json 次版本号 +1、修订号归 0」): `sed -n '13,15p' aria/CHANGELOG.md` ⇒ `## [1.68.0] - 2026-09-02` 后紧跟 `### Added — state-scanner / spec-drafter: …` ✅; 1.67.2 → 1.68.0 (minor +1, patch → 0) ✅。**两项均满足。**

派生检查实跑 (合并后取值等价, 因 master 的两个 commit 不动版本文件):
```
m6-version-badge-match            ⇒ OK badge=1.68.0
i18n-readme-translation-currency  ⇒ missing [] stale [] ok ['README.zh.md','README.ja.md','README.ko.md'] plugin 1.68.0
main-project-version-consistency  ⇒ OK 主项目版本 1.7.5 — 9 个引用点全部一致 (exit=0)
m6-claude-md-version              ⇒ 2.0.0
claude-md-changelog-free          ⇒ lines=151 bytes=13139 (预算 200 / 24000)
```
(`m6-arch-doc-stale` 在**本分支**工作树上会红 —— `Last Updated: 2026-05-27`, 98d; 合并后取 `c423281` 的 `2026-09-02` 即转绿。不计为 finding。)

### 3. 合并安全 — PASS

```
$ git rev-parse origin/master  ⇒ c423281a9b1e5d04ebf62bd3132cc63eecd366f1
$ git merge-base origin/master HEAD ⇒ e1deaf1f85408126d5c78b35c9c751b504756747
$ git log --oneline origin/master ^HEAD
c423281 docs(architecture): system-architecture.md 2.0.1 复审校准 …
882707f docs(m6): aria-layer2-git-2026-Q3 签发闭环 — TASK-028 done …          # ← 落后 2, 非 1 (finding 82513c94)
$ git merge-tree --write-tree --name-only origin/master origin/feature/linked-issue-field-availability
2004478cbc660ab8f954d28fb8f199fa3cdea205        # exit=0, 输出无 CONFLICT 行
```

文件集求交 (自己算, 不引 PR body):
- `882707f` 5 文件 (`.aria/decisions/2026-08-30-forgejo-token-ownership-three-layers.md` / `.aria/notes/2026-08-29-…` / `.aria/pat-inventory.yaml` / `openspec/changes/aria-2.0-m6-dispatch-input-delivery/{detailed-tasks.yaml,tasks.md}`) vs PR 70 文件 ⇒ `comm -12` **空集**。
- `c423281` 1 文件 (`docs/architecture/system-architecture.md`) vs PR 70 文件 ⇒ **不交** (PR `git diff --stat origin/master...HEAD -- docs/architecture/` 为空)。

`.aria/pat-inventory.yaml` 陈旧自消, **实测非推论**: 合并树里该文件 md5 = `006688f98c67f565702bd73e17c8c016` = `git show origin/master:.aria/pat-inventory.yaml` 的 md5; 本分支版本 md5 = `5e123f777d867f57e82910f0dc9e5868` ≠。⇒ 本分支未改它, 合并后**以 master 版为准**, PR body 「`forgejo-app-token-liveness` 指纹漂移合并后自消」成立。

### 4. check 注册 — PASS

用生产解析器实跑 (先 `cd aria/skills/state-scanner/scripts` 使 `from collectors import custom_checks` 成包内导入):
```
n_checks: 13                                     # 无异常抛出
union keys ALL: ['command','description','enabled','fix','name','severity','timeout_seconds']
LAST name: linked-issue-field-availability
NEW-ONLY keys in 13th: []                        # 相对前 12 条**零新键**
LAST enabled: True | severity: 'warning' | timeout_seconds: 10 <class 'int'>
```
command 路径存在且以 `aria/skills/` 起首 (`ls -l aria/skills/state-scanner/scripts/linked_issue_field_probe.py` ⇒ 7765 B); `custom_checks.py:342-344` 以 `cwd=str(project_root)` 执行 ⇒ 注册行里的相对路径 (`aria/skills/…` + `.aria/…`) 语义正确。

timeout 10s 的余量, 三次实测:
```
run1 exit=0 elapsed=0.162s / run2 exit=0 elapsed=0.150s / run3 exit=0 elapsed=0.197s
stdout: OK (9 份在范围内, 6 条在册)
```
作用域 9 份 proposal ⇒ **~60× 余量**; 即使作用域涨到 archive 的 140 份量级 (探针明写不扫 archive) 仍在 ~2.5s。**10s 足够。**

### 5. 对抗性核验 (拒绝能力, 非当前取值 — memory `adversarial-fixture`)

探针三臂全部**能红**, 逐字输出:
```
$ …probe.py . --grandfathered <空白名单>
FAIL 6 项 / 6 行 `…/proposal.md:- NO_FIELD 缺字段行 (E0 三谓词无命中)` / exit=1
$ …probe.py . --grandfathered <白名单+不存在路径>
FAIL 1 项 / FAIL allowlist 陈旧: openspec/changes/does-not-exist-xyz (a) / exit=1
$ …probe.py . --grandfathered <白名单+已合规条目>
FAIL 1 项 / FAIL allowlist 陈旧: openspec/changes/linked-issue-field-availability (c) / exit=1
```
`--emit-arg` 四态复跑 (SUBSTITUTE.md §2 贴文是派生物, 我重跑而非引用 — memory `pasted-evidence-is-derived`):
```
$ …--emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | od -c
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4      # 逐字节吻合贴文, 无换行, exit=0
$ …--emit-arg openspec/changes/linked-issue-field-availability/proposal.md | od -c
0000000                                                          # 哨兵 none ⇒ 空, exit=0
$ …--emit-arg /nonexistent/proposal.md
--emit-arg 读取失败: … [Errno 2] …    exit=2                       # stdout 空 + stderr + exit 2
```
测试套件 (简报强制项): `cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field` ⇒ `Ran 48 tests in 1.824s / OK`。

9 份 proposal 头部字段顺序普查 (finding `9ac5533a` 的数据; 计数法 = 取每份前 20 行里所有 `^> \*\*(.+?)\*\*:` 捕获组, 与 SOT 前 4 个比):
```
SOT      : ['Level','Status','Created','Linked Issue']
spec-drafter 预览围栏 : ['Level','Status','Created','Linked Issue']     # SC-7a 钉住的那份, 合规
a1-entry-claim-duplicate-work-guard : ['Status','Created','Spec Level','Linked Issue','代码落点']   DEV
linked-issue-field-availability     : ['Status','Created','Spec Level','Linked Issue','母 Spec']    DEV
sibling-spec-probe                  : ['Status','Created','Spec Level','Linked Issue','代码落点']   DEV
aria-2.0-m6-cost-model-telemetry / -dispatch-input-delivery / -e2e-resilience / -release-closeout
aria-2.0-m7-agent-lifecycle / -fleet-aggregation : ['Level','Status','Change ID','Parent US',…]     DEV ×6
⇒ 0/9 符合
```

### 6. 流程合规 (Rule #6 / #8 / #10) — PASS

**Rule #6**: `git -C aria diff --name-only d69091d fe32441` 共 9 文件, 其中**唯一**的 SKILL.md 是 `skills/spec-drafter/SKILL.md`; `state-scanner/SKILL.md` 零改动 (SUBSTITUTE.md §3 该行的声称经 diff 核实为真); frontmatter `description` / `allowed-tools` 未动 (hunk 起于 `@@ -110`, 无 frontmatter hunk)。逐 hunk 五格处置表 (SUBSTITUTE.md §3) 六行**每行都有指向证据**:

| hunk | 落格 | 处置 | 我核到的证据 |
|---|---|---|---|
| spec-drafter hunk A+B | 处方性·运行时指令面 | 照跑 AB | RESULT.md §1 三表 + 逐 run `grading.json`/`timing.json` 在库 |
| 新增 authoring 行为 | 处方性·套件覆盖外 | 三件套齐 | SC-7 点名 ✓ / eval id 3 fixture ✓ / #117 comment 20573 ✓ |
| standards 模板 | 描述性 | substitute SC-6 | §1 红 (ModuleNotFoundError) → §2 绿 |
| 探针脚本 | 确定性 Python | substitute SC-4/5/9 | 同上 + 我上面三臂对抗跑 |
| state-checks 注册 | 机械读取数据 | substitute SC-8 | 同上 + 我的解析器实跑 |
| lib 纯函数 | 确定性 Python | substitute SC-1~4/9 + 13 坏实现矩阵 | 48 tests OK |

**AB 输入同一性 (delegate-verify)**: RESULT.md 称被测新版是 aria `b47fe11`, 而 ship 的是 `fe32441` —— 实测 `git -C aria rev-parse b47fe11:skills/spec-drafter/SKILL.md` = `git -C aria rev-parse fe32441:skills/spec-drafter/SKILL.md` = `58637d7e…` (同一 blob), `git -C aria diff --stat b47fe11 fe32441 -- skills/spec-drafter/` 为空, 且 `merge-base --is-ancestor` = YES。⇒ **AB 测的就是 ship 的那份文本。**

**AB 结论措辞诚实性**: RESULT.md §2-2 逐字「Rule #6 结论按 memory `ab-input-baseline` 降级为『区分力: 落地前世界已证, **skill 边际未证**』」; §2-3 主动记录 hunk B 的必要性主张被 3 个基线 run 反证; §4 主动记录两条基线泄漏通道、评测 run 的约束违反、以及 grader 贴文证据失真。**未见任何「skill 边际已证」的越界声称**, PR body「Rule #6 结论」段同样保留了「ship 态 skill 边际未证」。`ab-suite/version.yaml` 的 `skills_covered: 31 / total_eval_cases: 74` 我程序化重算 (31 个 `ab-suite/*.json`, `sum(len(j['evals']))` = 74) —— **逐位吻合**, 非引用。

**Rule #8 / C.2.4**: `.aria/config.json` `phase_c_integrator.pre_merge_gate.enabled = true`, `ci_backends = null` (auto-detect), `no_ci_fallback = "skip_with_warning"`。not_applicable 放行的 SKILL 义务 (surface 警告行) **已履行** —— handoff `:142` 与 PR body 都逐字带出 `[not_applicable: 70 变更文件无 workflow 覆盖, main in-flight 已核]`。判定本身经我独立核实为真: 仓内仅 3 个 workflow, 唯一带 `pull_request` 触发的是 `issue-triage-tests.yml`, 其 `paths` = `aria/skills/issue-triage/**`, 而 PR 的 70 个变更路径里子模块是裸 `aria` / `standards` ⇒ 零命中。(该路径过滤的结构性问题另计为 finding `5333fe78`。)

**Rule #10 (无自行豁免)**: `.aria/config.json` `audit.checkpoints` = `{post_brainstorm: off, post_spec: convergence, post_planning: convergence, mid_implementation: off, post_implementation: off, pre_merge: off, post_closure: off}`。两个 **enabled** 的闸门都已执行且有产物: post_spec R1–R6 (聚合件 `.aria/audit-reports/post_spec-R6-1788084727388-a1-entry-combined-aggregated.md` 实存, 18093 B) / post_planning R1→R4 CONVERGED (proposal `:3` 记载)。`pre_merge` 在 config 里是 **off** ⇒ phase-c-integrator 未跑它**不构成**自行豁免 (四类白名单第一类: config 显式 off); 本轮 pre_merge 是 owner 显式调用, 属加严非放松。**未发现任何 enabled 闸门被以「变更小 / 性价比 / 1:1 派生」等理由跳过、降级或改序。**

### 7. 接缝 (探针 Spec ↔ 本 Spec 导出面) — PASS

`grep -n 'linked_issue_field\|is_sentinel\|extract_linked_issue_field\|FieldVerdict' openspec/changes/sibling-spec-probe/proposal.md` 命中 `:70` `:137` `:138` `:167` `:544` + `tasks.md:52`, 逐条与实际导出比对:

| 探针 Spec 处的引用 | 实际 (`aria/skills/state-scanner/lib/linked_issue_field.py`) | 判定 |
|---|---|---|
| `lib/linked_issue_field.py::extract_linked_issue_field(text: str) -> FieldVerdict` (`:137`) | `:108 def extract_linked_issue_field(text: str) -> FieldVerdict` | ✅ 签名逐字一致, 且**输入是文本 blob 非路径** (docstring 明写为非文件系统调用方保留) |
| `from lib.linked_issue_field import extract_linked_issue_field` (`:167`) | 模块实位 `state-scanner/lib/`, 48 条测试经同一 import 全绿 | ✅ |
| `FieldVerdict.line_no` (`tasks.md:52` 层 2 定位用) | `:73-79` dataclass 字段 = `verdict / token_str / token_elements / line_no / bad_elements` (4 + 1 默认) | ✅ 字段名与数量吻合 |
| 哨兵集合 `{none (ASCII 折叠), 无 (逐字节)}` 定义在姊妹 §2 (`:112`/`detailed-tasks.yaml:62`) | `:57 SENTINELS = ("none", "无")` + `:81 is_sentinel()` 逐字实现「`== "无"` 或 `isascii() and lower()=="none"`」 | ✅ |
| 常量名 `_RAW_KEY_BLACKLIST` (`detailed-tasks.yaml:390`) | 探针侧尚未实现 (sibling-spec-probe 未进 B), 本 Spec 侧无对应常量 —— 契约是文本级同步义务, 已双向成文 | ✅ 无冲突 |
| **占位串** `{<org>/<repo>#<n>}` (SC-19 黑名单字面, `proposal.md:508`) | 三宿主 **逐字节同一** | ✅ |

占位串逐字节核验 (Python `re.findall(r'\{<org>/<repo>#<n>\}')` + `.encode('utf-8')` 打印, 并同时扫近似变体 `\{[^\n\`]{0,25}org[^\n\`]{0,25}\}` 排查同形异串):
```
standards/openspec/templates/proposal-minimal.md : exact [b'{<org>/<repo>#<n>}'] / near-variants 同一条
aria/skills/spec-drafter/SKILL.md:143            : exact [b'{<org>/<repo>#<n>}'] / near-variants 同一条
openspec/changes/sibling-spec-probe/proposal.md  : exact [b'{<org>/<repo>#<n>}'] / near-variants 同一条
```
**三处零变体、零近似异串。**

跨 skill import 的顺序承重问题 (memory `ss-two-lib-pkgs`) 亦复核: `aria/skills/state-scanner/lib/` (含 `collision.py` / `linked_issue_field.py`) 与 `aria/skills/state-scanner/scripts/lib/` (含 `runtime_probe.py` 等) **今天就同名并存**, 探针 Spec `:170` 的代码块已把 `_SS_ROOT` 排在 `_SS_SCRIPTS` 之后插入 (即 sys.path 最前) 并写明「顺序承重」+ 4 条实现约束 + SC-21 钉住。⇒ 接缝无悬空。

**Level 3 模板缺口排查 (无 finding)**: hunk A 写「Level 2 / Level 3 的 proposal.md 头部**必须**含该字段」, 我核 `standards/openspec/templates/README.md` 模板表逐字「`proposal-minimal.md` … 适用级别 **Level 2, 3**」—— Level 3 复用同一份 proposal 模板, 该模板已带字段行, 无第二份需同批改的 proposal 模板 (`tasks.md` / `design.md` 模板头部不是 proposal, 探针只扫 `proposal.md`)。⇒ **不存在 Level 3 侧缺口。**

**已知且不另报的两项**: (a) `spec-drafter/SKILL.md:110-112` 的 A.1.4 路径块写 `standards/openspec/changes/{feature}/proposal.md`, 与 CLAUDE.md 规则 #5 相反, 本 PR 的新增行紧贴其下未顺手修 —— 已由 handoff §6 第 4 条 `carry-spec-drafter-path-rule5-drift` 显式挂起, 并给出了不合并处理的理由 (路径 hunk 需独立 Rule #6 重判), 属成文延期非漏项。(b) hunk A 里 `[proposal-minimal 模板](../../../standards/openspec/templates/proposal-minimal.md)` 对未 vendor standards 的第三方悬空 —— 但仓内已有 **16 个文件**用同一相对路径形态 (含 `spec-drafter/LEVEL_GUIDE.md:350` 指向**同一目标文件**), 且 hunk A 正文三条写法规则**自包含**, 链接仅为补充, 属既有类级形态而非本 PR 新造。
