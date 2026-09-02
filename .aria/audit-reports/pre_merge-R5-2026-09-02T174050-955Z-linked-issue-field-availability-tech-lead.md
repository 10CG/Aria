---
checkpoint: pre_merge
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS
timestamp: 2026-09-02T18:04:21.565Z
context: PR #190 linked-issue-field-availability (main 0db60cc / aria d1caa66 / standards ffed204)
agents: [tech-lead]
---

# Pre-merge 收敛审计 R5 — tech-lead 席 (多仓集成 / 发版面 / 流程合规 / 合并安全)

镜头内的**实物面 (gitlink / 远端 / tag / 版本面 / 合并安全 / 两道 gate / 三仓一致性 / Rule #5·#6·#8·#9·#10)
零 finding**。下列 4 条 minor 全部落在**审计自身的记录与验证器**上, 无一落在被交付物上。

## 审计结论

- [minor] testing/`aria/skills/state-scanner/tests/test_normalize_snapshot.py`: `TestStabilityIntegration.test_two_consecutive_runs_diff_zero` 拿**活仓**当扫描目标 (`:272` `project_root = …parent×5`), 而 `collectors/audit.py:234` 读 `.aria/audit-reports/` — 并行席位在两次 scan 之间落报告即致 diff≠0。我实跑 `bash aria/skills/run_all_tests.sh` = **1894 累计 / state-scanner FAIL (failures=1)**, 单独重跑同一 test **OK**。⇒ tasks.md `:5.1`「`run_all_tests.sh` 0 FAIL」与 PR body「1462 全绿 / 1894」只在**静仓**成立。该 test 非本 PR 触碰 (`git -C aria diff --name-only d69091d d1caa66` = 9 文件, 无扫描管线) — 证据: 见「核验记录」§6 (type=risk) — finding_id `303c51a8`
- [minor] implementation/`.aria/repro/handoff-current-state-scan.py`: R4 类级修法的**验证器本身不 fail-CLOSED**, 与其 docstring 自述矛盾。(i) PR body 维度 fail-OPEN: `forgejo GET` 返非 JSON (本仓已成文的复发态 — PAT stale 401, memory `forgejo-agit-pr`) 时 `:49` 只往 **stderr** 打一行然后继续, stdout 照出 `residual = 0` + exit 0 —— 「扫过且干净」与「根本没扫」在出口逐字节同形 (实跑 `--pr 999999` 复现)。(ii) `HIST_OK` 按**整行**豁免且含无锚点通用词 (`已完成` / `已推` / `历史` / `aggregated` / `占位`), 任一出现即整行免检; `STALE` 的轮次类只枚举了具体措辞, 换句话即逃逸 (两条注入实测 residual=0)。**未构成掩盖**: 我逐条人工复核了当前 38 条被豁免行, 全部为真历史/正确陈述 — 证据: 见「核验记录」§7 (type=risk) — finding_id `d61b5fc9`
- [minor] documentation/`docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md`: `:145` 以当前态写「C.2.4 green [not_applicable: **70** 变更文件无 workflow 覆盖]」; 我重跑 gate 得 `changed_files_count: **93**` (审计轮次自身加了 41 文件)。属 `a3bfd693` 同一类 (派生文档复述当前态数字), 而 R4 扫描器的 `STALE` 三类 token **不含文件计数**, 类级修法够不到 — 证据: 见「核验记录」§3 / §8 (type=issue) — finding_id `82513c94`
- [minor] architecture/`PR#190/body`: 合并后主仓 master 的 **github 镜像推送在服务端合并路径上无机械兜底**。实测 `forgejo GET /repos/10CG/Aria/push_mirrors` = `[]`; C.2.5 触发条件是「合并成功 (**本地** master 已 fast-forward)」+ `expected_sha = git rev-parse HEAD` (`phase-c-integrator/SKILL.md:603/612`), Forgejo UI 合并永不推进本地 master ⇒ C.2.5 结构上不触发 (memory `mirror_sync_needs_mechanical_backstop` 点名的正是这条路径, Aria #165)。义务**已成文**于 handoff `:127`「→ ls-remote 两端一致 + github 镜像 master 推」(我去目标文件核过), 但 PR body §注意 与 tasks.md `:5.6` — 合并操作者当场会读的两个面 — 都没有 — 证据: 见「核验记录」§9 (type=risk) — finding_id `55847e9b`

## Verdict

**PASS** — Critical **0** / Major **0** / Minor **4**。

镜头内逐项复核结论 (全部我自己实跑):

| 面 | 结果 |
|---|---|
| gitlink ×3 (HEAD 树) | aria `d1caa66` / standards `ffed204` / aria-orchestrator `237045ac` (与 base 同, 本 PR 未动) |
| ls-remote 四条 | aria origin=github=`d1caa66` ✅ · standards origin=github=`ffed204` ✅ |
| tag peel 两端 | `v1.68.0^{}`=`fe32441` · `v1.68.1^{}`=`d1caa66`, origin/github 逐字一致 |
| R4 后子模块推送 | 零 (两子模块工作树 clean, HEAD == gitlink == 两端 master) |
| 合并安全 | `merge-tree --write-tree` exit 0、输出树 `f5c165e` **== HEAD^{tree}** (FF, 零冲突消息); `git log origin/master ^HEAD` 空; 本地 master == origin/master == github/master == `c423281` (memory `stale-local-main` 满足) |
| post-merge 树三 gitlink | 三个 SHA 在 origin 与 github **都是 master 尖端** ⇒ 无 orphaned gitlink 风险 |
| 版本面 | 主仓 **16** 点 + aria **5** 文件全 `1.68.1`; `1.68.0` 残留 = 0 (剩余命中全为 CHANGELOG/历史叙述) |
| 新 check 三态+ | 5 态实测: 基线 OK(0) / 单点漂 DRIFT(1) / 缺行 MISSING(1, fail-closed) / SOT 不可读 SKIP(0) / SOT bump 而文档未跟 DRIFT×2(1) |
| C.2.4 (Rule #8) | `verdict=green`, backend `aether-ci-cli@f29abee` (真 backend, 非 stub/降级), main in-flight 清 |
| C.2.4.5 | PASS: standards forward bump / aria forward bump / aria-orchestrator unchanged |
| token 活性 | OK, 2 枚应用级 token http=200 且指纹与台账一致 |
| 交付物拒绝能力 | 探针 4 态: 忠实副本 OK / 合规件删字段 FAIL(NO_FIELD) / 在册件变合规 FAIL(陈旧 c) / 在册件指向不存在 slug FAIL(陈旧 a) — 非橡皮图章 |
| 白名单口径 | 9 份在范围, 恰 6 份缺字段, 恰这 6 条在册; 3 份合规件**不在册** ⇒ 零过度豁免 |
| Rule #5 / #6 / #8 / #9 / #10 | 全部通过 (逐条见「核验记录」§10) |

## 投票

**PASS** — 我对**合并本身没有保留意见 (不阻塞)**。

逐条阻塞判定:

| finding_id | 阻塞合并? | 理由 |
|---|---|---|
| `303c51a8` | **否** | test 为本 PR 之前既存 (aria 侧 9 个改动文件无一在扫描管线内), 静仓下单跑与全量都绿; 触发条件 (并行席位写 `.aria/audit-reports/`) 合并后即消失 |
| `d61b5fc9` | **否** | 验证器当前**没有**返假绿 (我的运行里 PR body 确实被读到, 无 stderr 行), 且 38 条豁免逐条人工核为真历史; 缺陷是未来鲁棒性, 不改变今天的事实判定 |
| `82513c94` | **否** | 一个陈旧计数, 不影响任何合并不变量; 与 M1/B3「下次触碰同批改」同性质 |
| `55847e9b` | **否** | 是**合并后**动作而非合并前缺陷, 且义务已成文于 handoff `:127`; 建议合并时把那一行同时贴进 PR body/tasks.md 5.6, 但不构成阻塞 |

**给 owner 的补充事实 (不是我自造的第四个选项, 是 SOT 里已有、但决定 [1]/[2]/[3] 时用得上的一条)**:
`audit-engine/references/report-format.md:93-101` 的「阻塞行为」表对 `pre_merge` 是
`PASS → 继续 / PASS_WITH_WARNINGS → 继续 (附警告) / FAIL → 阻塞`。R1–R4 皆 0 Critical (PASS_WITH_WARNINGS),
R5 本席 0C/0M。也就是说**审计 verdict 这一路从未阻塞过合并**; `converged` 标志与「能不能合」在 SOT 里是两件事,
[1]/[2]/[3] 选的是**收敛记录怎么落**, 不是合并许可本身。H1b 的三档与
`audit-engine/SKILL.md:265-288` 逐字一致 (含 `overridden_by_user: true` / `max_rounds += 2` / `degraded: true`
三个语义), 我核对后**没有发现被收窄的档** —— 我另核了振荡出口是否被漏掉: keys(R4) ≠ keys(R2) (差 7 个四元组),
SOT 的 `oscillation` 条件不成立, 所以那不是一个被漏报的第四条路。

## R4 处置核验 (一句话表)

| R4 处置项 | 我的独立核验 | 结论 |
|---|---|---|
| `3b277328` 收敛口径撤回 | 决策单 `:122` (R3 原行) 原样保留、`:131` 另起「撤回」行 (append-only 未改写); 其三条证据我逐条复跑: `grep -rn 'C∪M\|可执行结论集' aria/skills/audit-engine standards/` = **0 命中**、`SKILL.md:220-223` 确含 severity 的四元组、`convergence-algorithm.md` 边界表确有「Round 1 = ∅ 不视为收敛」 | **诚实, 引用准确** |
| H1b 上呈措辞 | handoff `:57` 逐字给出 [1] override / [2] 加轮 / [3] 降级单轮, 与 `audit-engine/SKILL.md:265-288` 三档语义一一对应; 振荡出口经实算排除 (keys R4 ≠ R2) | **选项集完整, 未收窄** |
| `a3bfd693` 类级修法 (指针口径) | 派生文档已改指针; 我按 R4 逐字命令重跑扫描器 → `residual = 0`, exit 0 (复现) | **成立** |
| `a3bfd693` 类级修法 (扫描器) | 自己跑了三态: 注入真陈旧 → residual=1/exit 1 (有拒绝能力, 非恒绿); 但 PR-body 维度 fail-OPEN + 整行式通用白名单词 (finding `d61b5fc9`) | **成立但不 fail-closed** |
| 白名单是否被放宽以掩盖真残余 | 枚举当前全部 **38** 条 `STALE ∧ HIST_OK` 豁免行逐条人工判读 | **没有掩盖**: 38/38 均为真历史或正确当前陈述 |
| 跨文档一致性 (PR body / handoff / latest.md / 决策单) | 版本口径、gitlink、tag、双推核验、C.2.4 `not_applicable` 留痕 (SKILL.md:265 的 surface 义务, 落在 handoff `:145` + tasks `:83`) 全部对得上 | **一致**, 唯 `:145` 文件计数 70→93 陈旧 (finding `82513c94`) |

---

## 核验记录 (逐字)

### §1 gitlink / 远端 / tag

```
$ git rev-parse HEAD
0db60ccfc21c84835e6a84ae2d6b9afe6e9db045
$ git ls-tree HEAD | grep commit
160000 commit d1caa66cb375c2799f55def453ca232c66a18c22	aria
160000 commit 237045ac2cfed9849c201e18434e9f6cb9036ab5	aria-orchestrator
160000 commit ffed2040dff7964cf9d137e85e174173d2c685b9	standards
$ git ls-tree origin/master | grep commit          # base: aria d69091d / orch 237045ac / standards 334c609
$ git diff origin/master HEAD -- aria-orchestrator # 空 ⇒ 本 PR 未动 orchestrator gitlink

$ git -C aria ls-remote origin refs/heads/master  → d1caa66…
$ git -C aria ls-remote github refs/heads/master  → d1caa66…
$ git -C standards ls-remote origin refs/heads/master → ffed204…
$ git -C standards ls-remote github refs/heads/master → ffed204…

$ git -C aria ls-remote --tags {origin,github} | grep v1.68.
c6aad0d… refs/tags/v1.68.0        fe32441… refs/tags/v1.68.0^{}
5b9de8e… refs/tags/v1.68.1        d1caa66… refs/tags/v1.68.1^{}      # 两端逐字相同

$ git -C aria-orchestrator ls-remote {origin,github} | grep 237045ac
237045ac…	HEAD / refs/heads/master   (两端均为 master 尖端)
```

子模块工作树 `git -C {aria,standards} status --short` 均为空; HEAD 恰为 gitlink ⇒ **R4 后零推送**。

### §2 合并安全

```
$ git merge-tree --write-tree --messages origin/master HEAD
f5c165e75f9a5e9d4f8368672972c763f23346bf        # exit 0, 无 conflict 消息 (输出仅 2 行)
$ git rev-parse HEAD^{tree}
f5c165e75f9a5e9d4f8368672972c763f23346bf        # 完全相同 ⇒ 干净 fast-forward
$ git log --oneline origin/master ^HEAD          # 空
$ git rev-parse master origin/master github/master
c423281a9b1e5d04ebf62bd3132cc63eecd366f1  (三者相同)
$ git ls-tree f5c165e | grep commit               # 三 gitlink 同 §1, 两端均可解析
```

Forgejo 侧: `state=open, draft=False, mergeable=True, base=master c423281, head=0db60cc`。

PR body「零文件重叠」复核: `git diff --name-only e1deaf1 origin/master` = 6 文件,
与 `git diff --name-only e1deaf1 0e9619c` (70 文件) 的 `comm -12` = **空**。
其中 `docs/architecture/system-architecture.md` 在 merge (29c1e4f) **之后**才被分支的 R1/R2 清账触碰,
且 master 侧 2.0.1 内容仍在 (`:968` 2.0.1 行 + `:967` 2.0.2 行, 头部 Version 2.0.2) ⇒ 无静默回归。

### §3 C.2.4 / C.2.4.5 / token

```
$ python3 aria/skills/phase-c-integrator/scripts/pre_merge_gate.py \
    --pr-branch feature/linked-issue-field-availability --main-branch master --remote origin
{"verdict": "green", "pr_ci_status": "not_applicable", "in_flight_runs": [],
 "primitive_used": "aether-ci-cli", "primitive_version_sha": "f29abee",
 "raw_message": "path_coverage: no workflow covers changed files (reason=no-triggering-paths);
                 PR CI wait skipped (not_applicable); main in-flight clear",
 "path_coverage": {"decision": "not_applicable", "workflows_scanned": 3, "matched_workflows": [],
                   "changed_files_count": 93, "reason": "no-triggering-paths", "dispatchable_workflows": []}}
EXIT=0

$ ARIA_SUBMODULE_GATE_MODE=block bash aria/skills/phase-c-integrator/scripts/submodule_gate.sh
GATE: submodule=standards master=334c609… feature=ffed204…   PASS: standards forward bump
GATE: submodule=aria     master=d69091d… feature=d1caa66…    PASS: aria forward bump
OK: aria-orchestrator unchanged (237045ac…)
✓ submodule_gate: all submodules unchanged/forward/first-time (mode=block)
EXIT=0

$ (state-check forgejo-app-token-liveness)  rc=0
OK (2 枚应用级 token 活性正常, 指纹与台账一致)
  aria-layer1-forgejo: OK http=200 fp=c957308a
  aria-layer2-git:     OK http=200 fp=3105220d
```

`changed_files_count = 93` ↔ handoff `:145` 写的 70 ⇒ finding `82513c94`。
Rule #8 三条判据: (a) 本 PR CI = `not_applicable` (零 workflow 覆盖, 非静默降级);
(b) main in-flight = `[]`; (c) 经 CI backend 抽象层 (`aether-ci-cli`), **非** stub, 未走 `no_ci_fallback`。
SKILL.md:265 的 `not_applicable` surface 义务已落 handoff `:145` + tasks.md `:83` (措辞含「无 workflow 覆盖 + main in-flight 已核」)。

### §4 版本面 (16 + 5, 旧值零残留)

主仓 16 点 (逐点实读): `CLAUDE.md:139/:141` · `README.md:8/:242` · `README.zh.md:3/:10/:244` ·
`README.ja.md:3/:10/:244` · `README.ko.md:3/:10/:244` · `VERSION:24` ·
`docs/architecture/version-scheme.md:23` · `docs/architecture/system-architecture.md:189` = **16**, 全 `1.68.1`。
aria 5 文件: `plugin.json:4` · `marketplace.json:3/:16` · `README.md:5` · `VERSION:3` · `CHANGELOG.md:13` = 全 `1.68.1`。

`grep -rn '1\.68\.0'` 主仓 (排除子模块/.git/ab-results/audit-reports) 的全部命中都是 CHANGELOG 条目 /
handoff 时间线 / 决策单历史 / `<vNEXT>` 说明 —— **无一处把 1.68.0 断言为当前版本**。

四条版本类 state-check 实跑: `m6-version-badge-match` rc=0 `OK badge=1.68.1` ·
`main-project-version-consistency` rc=0 `OK 主项目版本 1.7.5 — 9 个引用点全部一致` ·
`i18n-readme-translation-currency` rc=0 `OK (3 i18n READMEs current @ 1.68.1)` ·
`linked-issue-field-availability` rc=0 `OK (9 份在范围内, 6 条在册)`。

### §5 新 check `plugin-version-arch-docs-match` — 5 态对抗实测

在 scratch 副本 (`/tmp/.../tl5/`, 未动仓内文件) 跑同一段 command:

| 状态 | 输出 | rc |
|---|---|---|
| 基线 (忠实副本) | `OK plugin=1.68.1 (2 arch doc rows match)` | 0 |
| system-architecture 行改 1.67.2 | `DRIFT plugin=1.68.1 vs system-architecture.md=1.67.2` | 1 |
| version-scheme 行删除 | `MISSING version-scheme.md aria-plugin 行` (fail-closed) | 1 |
| plugin.json 删除 (SOT 不可读) | `##SKIP## aria/.claude-plugin/plugin.json 不可读` | 0 |
| **真实场景**: plugin.json bump 1.69.0 而两文档未跟 | `DRIFT plugin=1.69.0 vs system-architecture.md=1.68.1 version-scheme.md=1.68.1` | 1 |

非恒绿、非恒红, 且在它被写来防的那个场景 (发版忘了改架构文档) 上会红。
severity=`warning` 与其余 13 条 check 一致 (14/14 全 warning), 无口径不一致。

### §6 finding `303c51a8` 的取证

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
Ran 53 tests in 4.536s   OK
$ cd aria/skills/state-scanner/tests && python3 run_tests.py
Ran 1462 tests in 101.126s   OK                       # 与 PR body 的 1462 逐字一致

$ cd aria/skills && bash run_all_tests.sh ; echo EXIT=$?
state-scanner                                  FAIL (1462 tests) — 见下方详情
    FAIL: test_two_consecutive_runs_diff_zero (test_normalize_snapshot.TestStabilityIntegration.…)
    FAILED (failures=1)
skill 套件: 8 OK / 1 FAIL / 0 SKIP   (累计 1894 个测试)
EXIT=1

$ cd aria/skills/state-scanner/tests && python3 -m unittest \
    test_normalize_snapshot.TestStabilityIntegration.test_two_consecutive_runs_diff_zero -v
Ran 1 test in 23.650s   OK                            # 单独重跑绿
```

因果 (不是猜): `test_normalize_snapshot.py:272` 用**活仓**做扫描目标, 而
`skills/state-scanner/scripts/collectors/audit.py:234` 读 `.aria/audit-reports/` 目录并产出
`candidates_scanned` / 最新 aggregated 指针 —— R5 期间其它席位往该目录落报告 (我跑完后
`git status` 里新出现 `pre_merge-R5-…-code-reviewer.md` / `-qa-engineer.md`), 落在两次 scan 之间即致 diff≠0。
该 test 的 offline freeze 只冻住了网络与时钟, **没有冻住活仓文件系统**。
不属本 PR: `git -C aria diff --name-only d69091d d1caa66` = 9 文件
(2 个 `.claude-plugin` + CHANGELOG/README/VERSION + `spec-drafter/SKILL.md` + `lib/linked_issue_field.py`
+ `scripts/linked_issue_field_probe.py` + `tests/test_linked_issue_field.py`), 无一在扫描管线内。
测试跑完仓内无残留改动 (`git status --short` 只有 ` M aria-orchestrator` 与其它席位的报告文件)。

### §7 finding `d61b5fc9` 的取证 (R4 扫描器)

```
# (a) 按 R4 逐字命令复现
$ python3 .aria/repro/handoff-current-state-scan.py \
    docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md --pr 190 \
    --extra docs/handoff/latest.md openspec/changes/linked-issue-field-availability/{tasks.md,detailed-tasks.yaml,proposal.md}
residual = 0
EXIT=0                                    # 复现成立

# (b) fail-OPEN: PR body 取不到时仍报绿
$ python3 .aria/repro/handoff-current-state-scan.py <handoff> --pr 999999
PR#999999 body 不可读: Expecting value: line 1 column 1 (char 0)     ← stderr
residual = 0
EXIT=0                                    # 「扫过且干净」与「没扫」出口同形

# (b2) 另一条失败分支反而是裸 traceback (try 只包了 json 解析, 没包 subprocess.run)
$ PATH=/usr/bin:/bin python3 .aria/repro/handoff-current-state-scan.py <handoff> --pr 190
FileNotFoundError: [Errno 2] No such file or directory: 'forgejo'   EXIT=1

# (c) 拒绝能力在 (非恒绿)
$ (handoff 副本尾部注入) 「本 Spec 目前仍待 owner 推送授权, aria 侧 4 处未推。」
h1.md:182: …   residual = 1   EXIT=1

# (d) 整行式白名单致逃逸
$ 注入「本 Spec 目前仍待 owner 推送授权 (B.2 已完成)。」   → residual = 0  EXIT=0
$ 注入「当前 pre_merge 审计已跑到第 3 轮, 还剩 2 轮。」     → residual = 0  EXIT=0
```

**是否被用来掩盖真残余 — 没有**: 我把当前 6 个被扫面里所有 `STALE ∧ HIST_OK` 的行全部枚举出来
(共 **38** 行, 每行连同命中的 STALE token 与 HIST_OK token 一起打印) 并逐条判读:
handoff `:38/:40/:41/:42/:43/:44` 为 §1 时间线历史行, `:56` 为标了 ✅ 的原文保留行,
`:83/:111/:112/:116/:128/:148/:149/:153/:170` 为版本谱系 / CHANGELOG 条目 / 双推已完成的正确陈述,
latest.md `:25/:27/:33/:38` 为带日期头的历史更新段, tasks.md `:7/:179/:180` 为 `<vNEXT>` 占位约定,
PR body `:7/:10/:15/:40/:41` 为「前一 SHA」「ab-results 目录名」等。**38/38 豁免正当, 零掩盖。**

### §8 跨文档一致性

- PR body ↔ 实测: `d1caa66` / `ffed204` / 两 tag / `mergeable` / 16 点 / 53 测试 / 1462 —— 全部对上。
- PR body「`ab-suite/version.yaml` 1.2.0 程序化重算」我独立重算: `ls ab-suite/*.json | wc -l` = **31**
  (= `skills_covered`), `sum(len(evals))` = **74** (= `total_eval_cases`); `spec-drafter.json` 三个 eval
  (id 1 / 2 / 3), id 2 有 **5** 条 expectations (= 3+2), id 3 = `linked-issue-field-authoring-TARGETED`。**逐字吻合**。
- SUBSTITUTE.md 贴的两条探针输出我逐字节复跑: `OK (9 份在范围内, 6 条在册)` / `od -c` = `10CG/Aria#174` (13 字节, 无尾换行) —— **一致**。
- handoff frontmatter 5 字段齐 (`track-id` / `owner-container` / `phase` / `status` / `updated-at`), `.aria/handoff/` 不存在。
- 唯一出入: handoff `:145` 的「70 变更文件」(finding `82513c94`)。

### §9 finding `55847e9b` 的取证

```
$ forgejo GET /repos/10CG/Aria/push_mirrors
[]
$ forgejo GET /repos/10CG/Aria   → mirror=False, allow_merge_commits=True, default_branch=master
$ sed -n '600,614p' aria/skills/phase-c-integrator/SKILL.md
### C.2.5 Multi-Remote Push Enforcement (v1.15.0+)
**触发条件**: - Phase C.2 合并成功 (master 已 fast-forward) …
**执行流程**: 1. 快照 `expected_sha = git rev-parse HEAD` (合并后本地 master HEAD)
```

CLAUDE.md 硬约束 1 允许主仓走 Forgejo 服务端合并 (它没有下游 gitlink), 但那条路径下
本地 master 不前进 ⇒ C.2.5 的触发条件与 `expected_sha` 都落空, 而 `push_mirrors=[]` 意味着服务端也不补。
义务在 handoff `:127` 有 (「收敛后合并 (Forgejo merge, 主仓例外) → `ls-remote` 两端一致 + github 镜像 master 推」),
但 PR body §注意 三条 (`/plugin update` / sibling-spec-probe B.1 / phase-d-closer) 与 tasks.md `:5.6` 都没写。
建议 (非阻塞): 合并前把这一行补进 PR body, 合并后逐 remote `ls-remote` 核验 (硬约束 2)。

### §10 Rule 合规逐条

- **#5**: 本项目变更在 `openspec/changes/linked-issue-field-availability/`; `standards/` 侧 diff 仅
  `openspec/templates/proposal-minimal.md` (SOT 模板本体, 非 change) ⇒ 合规。
- **#6**: `git -C aria diff --name-only fe32441 d1caa66` = 7 文件, **`grep -c SKILL.md` = 0** ⇒
  v1.68.1 PATCH 零指令面改动, substitute 车道成立 (`rule6_note` 已留); 且该区间 `plugin.json` /
  `marketplace.json` 的 diff **只有版本串**, `description` 三处逐字未变 ⇒ 不触发「description 变动一律照跑」。
  v1.68.0 区间 (`d69091d..fe32441`) 唯一 SKILL.md 改动 = `spec-drafter/SKILL.md` +19 行 (处方性) ⇒ 已照跑 AB
  (`ab-results/2026-09-02-v1.68.0-linked-issue-field-rule6/`, 3 eval 两臂), 未申请豁免。`state-scanner/SKILL.md` 零改动 (核实)。
- **#8**: 见 §3 —— gate 走真 backend、verdict green、两条腿都有实值, 无静默降级、无 stub NIE。
- **#9**: handoff 在 `docs/handoff/`, 5 字段 frontmatter 齐, `.aria/handoff/` 不存在。
- **#10**: `.aria/config.json` `checkpoints.pre_merge = "off"` (实读) ⇒ 本次审计是 owner 显式调用而非
  被跳过的 enabled 闸门, 无自我豁免; `max_rounds = 5` 与本轮 R5 一致。SOT 基线席位
  (`agent-team-audit/references/audit-points.md` pre_merge = Tech Lead / Code Reviewer / Knowledge Manager)
  实际用了 4 席 (**超集**, 非收窄)。H1b 三档与 SOT 逐字对应, 振荡出口经实算排除 (keys R4 ≠ keys R2, 差 7 个四元组)。

### §11 交付物拒绝能力 (对抗性)

在 scratch 副本上跑 shipped 探针 (`aria/skills/state-scanner/scripts/linked_issue_field_probe.py`):

| 构造 | 输出 | rc |
|---|---|---|
| 忠实副本 | `OK (9 份在范围内, 6 条在册)` | 0 |
| 删掉 `sibling-spec-probe` 的字段行 (合规件, 不在册) | `FAIL 1 项` / `…NO_FIELD 缺字段行 (E0 三谓词无命中)` | 1 |
| 给在册件 `aria-2.0-m6-e2e-resilience` 补上字段 | `FAIL allowlist 陈旧: …-e2e-resilience (c)` | 1 |
| 白名单加一条不存在的 slug | `FAIL allowlist 陈旧: openspec/changes/does-not-exist (a)` | 1 |

白名单口径核实: 9 份在范围内, 逐份实读头部 —— 恰 6 份无字段 (M6/M7 六份), 恰这 6 条在册;
`a1-entry-claim-duplicate-work-guard` / `linked-issue-field-availability` / `sibling-spec-probe`
三份合规且**不在册** (受检)。零过度豁免。
