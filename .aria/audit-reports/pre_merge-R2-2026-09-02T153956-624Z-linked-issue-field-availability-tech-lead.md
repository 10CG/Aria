---
checkpoint: pre_merge
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-02T16:19:53.189Z
context: PR #190 linked-issue-field-availability (main 17ae85e / aria d1caa66 / standards ffed204)
agents: [tech-lead]
---

# Pre-merge R2 — tech-lead 席 (多仓集成 / 发版面 / 流程合规 / 合并安全)

> 镜头: gitlink 与两远端一致性 · 版本同步面 · 版本档判据 · 合并安全 · B8/B9 裁定可证伪性 · 跨 Spec 接缝 · C.2.4 / C.2.4.5 闸门。
> **实物面 (代码 / gitlink / tag / 版本串 / 闸门) 全部核验通过, 零 finding。全部 6 条 finding 落在同一个类**: R1 清账把交付实物从 v1.68.0/`fe32441`/`fad8b4b` 换成了 v1.68.1/`d1caa66`/`ffed204`, 但**描述这些实物的 5 处记录**没跟着换 —— 修了实例, 没修类 (memory `fix-the-class`)。

## 审计结论

- [major] documentation/`docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md`: R1 `a3bfd693` 的处置**不完整** —— 只刷了 frontmatter 与「落后 1→2」, 正文 6 处仍断言「四处未推、待 owner 授权」, 与本文件自己的 `:14` / §7 状态块 `:143-150` 直接矛盾; 其中 `:23` (§0「第一件事」) 与 `:126` (§6 next session 第 1 条) 正是文档自称要先读的两个入口, 会把下个 session 导向一次已经完成的动作 — 证据: `:11`「**全部未推**: aria master `fe32441` (4 ahead)…待 owner 一句授权」/ `:23`「**第一件事 = 拿 owner 推送授权**」/ `:56` §2「高优先级 (owner 动作门)」H1 行仍列 `fe32441`+`fad8b4b` 为待推 / `:126`「拿 owner 推送授权后按序执行 H1」/ `:135`「三端 master **仍是** d69091d / e1deaf1 / 334c609 直到 H1 完成」/ `:177`「下个 session 第一件事 = owner 推送授权」; 实测 `git ls-remote` 四条: aria origin==github==`d1caa66`, standards origin==github==`ffed204`, 主仓 origin==github==`c423281` (finding_id = `a3bfd693`) (type=issue)
- [major] documentation/`openspec/changes/linked-issue-field-availability/`: Spec SOT **三份文件全部**仍把 ship 记为 v1.68.0 / `fe32441` / `fad8b4b`, 全目录 `1.68.1` / `d1caa66` / `ffed204` **零命中**; `phase-d-closer` D.2 归档消费的正是这三份, 归档即把错误 ship 号冻结 — 证据: `grep -n "1\.68\.1\|d1caa66\|ffed204" openspec/changes/linked-issue-field-availability/{proposal.md,tasks.md,detailed-tasks.yaml}` → 0 命中; `proposal.md:3`「B.2 实施完成 2026-09-02: aria v1.68.0 本地合并 `fe32441` (+tag) / standards `fad8b4b` / 主仓 feature 分支; **待 owner 授权双推 + 主仓 PR**」(推已完成、PR 已开); `tasks.md:5`「aria `fe32441` (v1.68.0, tag 已建) / standards `fad8b4b` … 测试 48/48 + state-scanner 1457」(实测 53 / **1462**, 见核验记录); `tasks.md:80`「origin/github `ls-remote master` = fe32441 … 与本地逐一 MATCH」/ `:81`「= fad8b4b MATCH」均已为假; 宿主 = TASK-025 (in_progress, deliverable 恰为本目录) (finding_id = `ee23ca88`) (type=issue)
- [minor] documentation/`docs/architecture/system-architecture.md`: R1 `ac44ace3` 的 §2.8 行修好了, 但同文件的 Version History **没加新行**, 于是当前那条 `2.0.1` 行自述「§2.8 版本表 (aria-plugin **v1.67.2**…)」与它所描述的 §2.8 现值 (1.68.1) 相矛盾; 新 check 因 `-m1` + 行首锚 `^\| aria-plugin \| v` 结构上扫不到该行 (实测该正则在本文件全库只 1 命中 = `:189`) — 证据: `:189` `| aria-plugin | v1.68.1 |` vs `:967` `| 2.0.1 | 2026-09-02 | 复审校准…§2.8 版本表 (aria-plugin v1.67.2; …)`; 先例 `:969` 的 1.9.0 行「aria-plugin v1.14.0→1.15.0」说明本文件惯例是版本表变动写进 History (finding_id = `a04601ce`) (type=issue)
- [minor] documentation/`docs/handoff/latest.md`: 机读指针行的**人读部分**停在推送前 —— `phase=C.1-field-spec-B-done-awaiting-push-auth` 与它指向的 handoff 自己的 frontmatter `phase: C.2 (PR #190 open …)` 不一致, 且逐字写「**全部未推, 待 owner 一句推送授权**」; 机读路径不受影响 (`collectors/handoff.py:269` `_parse_latest_pointer` 只取文件名, frontmatter 从目标文件读), 故限 minor — 证据: `docs/handoff/latest.md:4` 与 `:13` (track 表同款) vs 目标文件 frontmatter `:5-6` (finding_id = `1d2fe175`) (type=issue)
- [minor] architecture/`.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md`: 决策单 B9 把「发 v1.68.1 PATCH」(技术级, AI 可裁 — 成立) 与「推共享 master + 新 tag 的**授权**」(owner 动作门) 写成同一条裁定, 授权依据是**类推**而非字段级匹配: owner 授权面是 handoff §2 H1 逐条枚举的 (a)`fe32441`+`v1.68.0` / (b)`fad8b4b` / (c) feature / (d)`c423281`, `d1caa66`+`v1.68.1`+`ffed204` 不在其中 (memory `exact-exception-condition` / `sync≠push-auth`); 且 B9 自陈「而非留作 carry」—— 存在**不需要新增外向动作**的备选 (R1 对 `9ac5533a` 就是 carry), 但没有把「现修 (需再推一次) vs carry」上呈 (memory `narrow-owner-options`); handoff §2 两张表 (`:56` 高优先级 owner 门 / `:60-70` 中优先级 AI 可自裁) 均无该条请复议记录 (Rule #10 末句)。**减轻情节 (故为 minor)**: 「合并要求 gitlink 指向已推的子模块 commit」在 CLAUDE.md 硬约束 1 下确实成立, 不推即孤立 gitlink; 且推后逐 remote `ls-remote` 已核验一致。**前瞻风险**: 同一推理会在 R2/R3 清账时再次授权 v1.68.2 — 证据: 决策单 `:99` B9 行「推送依据 = owner 2026-09-02「执行 PR 190 审计, 通过后合并」指令 … 与早间 H1 推送授权同一交付」vs handoff `:56` H1 行的枚举 (finding_id = `c2e60555`) (type=risk)
- [minor] documentation/`PR#190/body`: PR 标题与「## 本 PR 携带 (主仓侧)」段仍是 v1.68.0 口径, 更正只出现在 30 行外的另一段 (L37); 其中 L32 给 owner 的操作指令**未被任何行更正** — 证据 (`forgejo GET /repos/10CG/Aria/pulls/190`): title「…(aria-plugin **v1.68.0** + standards 模板 + check 注册)」/ L7「两 gitlink 同一 commit `e5947fe`: **aria → `fe32441`** / **standards → `fad8b4b`**」/ L9「主仓发版同步面 14 点 → **v1.68.0**」/ L32「合并后 owner 需 `/plugin update` 刷本机缓存到 **1.68.0**」; L37 才写「gitlink → aria d1caa66 / standards ffed204; 14 点 → 1.68.1」。L7 带 commit 限定 (`e5947fe`) 故属可辩护的编年叙述, L32 与 title 不是 (finding_id = `8c067861`) (type=risk)

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **2** / Minor **4**。

实物面零 finding: gitlink==两远端==tag peel 四方一致 · 14 点版本面零残留 · PATCH 档位字面成立 · 合并 fast-forward 无冲突 · C.2.4 green + C.2.4.5 PASS · 跨 Spec 导出面与占位串接缝零漂 · 新 check 五态实跑正确。全部 Major/Minor 均为「记录未跟上实物」。

## 投票

**PASS**

理由: 6 条全部是文档/记录一致性, 无一条影响合并后的运行时行为、合并安全或发布正确性; 两条 Major 的修法都是分钟级文本编辑, 且各有明确宿主 (handoff 本身 / TASK-025 in_progress)。**但不建议本轮直接合并**: `ee23ca88` 若随 merge 进入 `phase-d-closer` 归档会把错误 ship 号永久冻结, 应在 R2 清账内改掉再进 R3 稳定性确认。`c2e60555` 请 owner 在下一轮清账**动手前**给一句话: R2/R3 若再出 aria 侧 finding, 是发 v1.68.2 (需再一次共享 master 推送授权) 还是 carry。

## 核验记录

### 1. gitlink / 两远端 / tag (四条 `ls-remote`, 不信 push 回执)

```
$ git ls-tree origin/feature/linked-issue-field-availability aria standards
160000 commit d1caa66cb375c2799f55def453ca232c66a18c22	aria
160000 commit ffed2040dff7964cf9d137e85e174173d2c685b9	standards
(git ls-tree HEAD 同值; git submodule status: ` d1caa66 aria (v1.68.1)` / ` ffed204 standards` 无 +/- 前缀)

$ git -C aria ls-remote origin refs/heads/master 'refs/tags/v1.68*'
d1caa66cb375c2799f55def453ca232c66a18c22	refs/heads/master
c6aad0dc1dd53a519ea4edb4da9656312e2846c0	refs/tags/v1.68.0
fe324414f3d8e0ad5284afa82e0154f18ea049d6	refs/tags/v1.68.0^{}
5b9de8e041311b7bc84f8275c20df74fd273ef93	refs/tags/v1.68.1
d1caa66cb375c2799f55def453ca232c66a18c22	refs/tags/v1.68.1^{}
$ git -C aria ls-remote github …   # 逐字节相同 (含两个 tag 与两个 ^{} peel)

$ git -C standards ls-remote origin refs/heads/master → ffed2040…
$ git -C standards ls-remote github refs/heads/master → ffed2040…

$ git ls-remote origin refs/heads/master refs/heads/feature/…
17ae85e9…	refs/heads/feature/linked-issue-field-availability
c423281a…	refs/heads/master
$ git ls-remote github refs/heads/master → c423281a…   (feature 分支不镜像 GitHub, 符合预期)
$ git rev-parse master origin/master → c423281 / c423281   (memory stale-local-main: 本地 master 未陈旧)
```

⇒ aria: gitlink == origin == github == `v1.68.1^{}` = `d1caa66`; `v1.68.0^{}` = `fe32441` (未被移动), 两 tag 两端 present。standards: gitlink == origin == github = `ffed204`。**无孤立 gitlink 风险** (CLAUDE.md 硬约束 1/2 满足)。`aria-orchestrator` gitlink 在 HEAD 与 master 同为 `237045a` (本 PR 未动; 工作树 `92acce5` 为有意停泊)。

### 2. 版本同步面 (14 点逐点实读 + 类级兜底三态实跑)

aria 5 文件全 `1.68.1` (`plugin.json:4` / `marketplace.json:3,16` / `VERSION:3` / `CHANGELOG.md:13` / `README.md:5`)。主仓 14 点逐点 `sed -n` 实读全 `1.68.1`:
`CLAUDE.md:139,:141` · `VERSION:24` · `README.md:8,:242` · `README.{zh,ja,ko}.md:3,:10,:244`。
`grep -n "1\.68\.0\|1\.67\.2" CLAUDE.md VERSION README.md README.{zh,ja,ko}.md` → **零命中**。

**R1 `ac44ace3` 类级修法核验** — CLAUDE.md §版本管理 发布同步面已加「+ `docs/architecture/system-architecture.md` §2.8 与 `docs/architecture/version-scheme.md` 的 aria-plugin 版本行 (PR #190 审计补入)」并列入 `plugin-version-arch-docs-match`; 两行实读 `system-architecture.md:189` / `version-scheme.md:23` 均 `v1.68.1`。

新 check **五态实跑** (逐字提取 `.aria/state-checks.yaml` 的 `command` 到副本树, 仓内文件零改动, 跑完 `git status --porcelain` 仅 ` M aria-orchestrator`):

| 态 | 构造 | 输出 | rc |
|---|---|---|---|
| 基线 | 原样 | `OK plugin=1.68.1 (2 arch doc rows match)` | 0 |
| DRIFT-A | `sa.md` 改 v1.67.9 | `DRIFT plugin=1.68.1 vs system-architecture.md=1.67.9` | 1 |
| DRIFT-B | `vs.md` 改 v1.66.0 | `DRIFT plugin=1.68.1 vs version-scheme.md=1.66.0` | 1 |
| MISSING-A | 删 `sa.md` 那行 | `MISSING system-architecture.md §2.8 aria-plugin 行` | 1 |
| MISSING-B | 删 `vs.md` 那行 | `MISSING version-scheme.md aria-plugin 行` | 1 |
| SKIP | 移走 `plugin.json` | `##SKIP## aria/.claude-plugin/plugin.json 不可读` | 0 |
| 双漂 (对抗) | 两侧同时改 | `DRIFT … system-architecture.md=1.0.0 version-scheme.md=2.0.0` (两点都列, 不早退) | 1 |

**运行时真被调用** (memory `completion-signals-vs-runtime-invocation`): 用仓自己的最小 YAML 解析器 `collectors.custom_checks._parse_state_checks_yaml` 解析 → 14 条 check, 新条为第 14 条 `enabled=True`; 按 `collect_custom_checks` 同款循环逐条 `_run_check` 实跑, 新 check `status=pass elapsed=0.03s`。附带发现两点 (均**不构成 finding**): (a) 全部 14 条真实 wall = **0.60s** 而 `TOTAL_BUDGET_SECONDS=60`, 尾部三条 (`forgejo-app-token-liveness` / `linked-issue-field-availability` / 新 check) 的最坏累计超时 95s 只在全部超时时才会触发预算耗尽, 且耗尽路径产出可见的 `status=skipped` + `custom_checks_budget_exhausted` soft error, 非假绿; (b) `plugin-cache-currency` = **fail** (`STALE installed=1.67.2 scope=user sot=1.68.1`) —— 属 owner 交互动作 (`/plugin update` + 重启), 非仓内缺陷, 且本 PR 的 check 走仓内路径 `aria/skills/state-scanner/scripts/…` 而非安装缓存, 证据链不受影响。

**第三处当前值断言点扫描**: 简报给的命令 `… | grep -v CHANGELOG | grep -v handoff | grep -v audit-reports` 把排除项作用在**整行**而非路径上, 实测漏掉 2 行 (`CLAUDE.md:139` 因含 "CHANGELOG"、`system-architecture.md:967` 因含 "docs/handoff")。改成按路径排除后共 15 处: 14 点 + `system-architecture.md:189` + `version-scheme.md:23` (`:967` 为修订史行, 见 finding `a04601ce`)。逐条判定后 **同步面之外无遗漏的当前值断言点**; 14 点中仅 4 点有机械 check 覆盖 (README.md badge / i18n ×3 的 translated-from) —— 该 4/10 账目**是既有已成文事实** (`openspec/archive/2026-08-18-secret-guard-per-segment-evaluation/proposal.md:432`「正确的账是 4 覆盖 / 10 零覆盖」), 非本 PR 引入, 不重报。

### 3. 版本档判据 (PATCH) 与 Rule #6 车道

- `git -C aria diff fe32441 d1caa66 --stat -- 'skills/*/SKILL.md'` → **空**; 全量 7 文件 = 5 版本文件 + 探针 + 测试, `--name-only` 无任何 SKILL.md。
- `standards/conventions/version-management.md §2.3` 触发条件逐字含「Bug 修复」「小改进」⇒ PATCH 字面覆盖 ✅。§4.3 三分判据下 aria-plugin = **按需锚点型** ⇒ 打 tag 作历史锚点、双推并逐 remote 核验 tag 对象 —— 实测两 tag 两端 present ✅。
- `aria/CHANGELOG.md:15` 首节标题为 `### Fixed — …` ✅; 同节末尾带 `rule6_note: 纯代码 + 测试, 零 SKILL.md 指令面变更 → substitute = 上述 baseline-failing 结构化测试 (决策单 §B 期 B9)`。
- **substitute 车道的可证伪证据独立复跑** (memory `past-summary≠measurement` — 不采信 CHANGELOG 自述): 把 skill 树复制到副本、用 `git -C aria show fe32441:skills/state-scanner/scripts/linked_issue_field_probe.py` 换回 v1.68.0 探针 (195 行 vs 新 238 行), 跑新增类:
  ```
  $ python3 -m unittest test_linked_issue_field.TestSC5ProbeHardening -v
  Ran 5 tests   FAILED (failures=4)
  ```
  与 CHANGELOG 声称的「5 条新测试, 4 条对 v1.68.0 探针实测红」**逐字吻合**。红的 4 条含 `test_root_positional_with_emit_arg_is_exit2` (`AssertionError: 0 != 2`)、`test_unreadable_proposal_is_fail_not_crash` (`'' != 'FAIL 1 项'`) 与 stdout 非 UTF-8 崩溃 (`UnicodeEncodeError` in old `_run_check`)。绿的那 1 条被 CHANGELOG 诚实标注为「纯覆盖补充」。
- 注: Rule #6 判据是「内容是否影响 AI 行为 + AB 套件测不测得到」而非文件目录 (CLAUDE.md 明写「不按文件目录判」)。本 PATCH 改的是机械探针的判定逻辑, 属描述性/机械面, spec-drafter AB 套件结构上测不到 ⇒ substitute 成立; 「零 SKILL.md」只是佐证不是判据本身。

### 4. 合并安全

```
$ git log --oneline origin/master ^HEAD          → (空)
$ git merge-base origin/master HEAD              → c423281  (== origin/master ⇒ fast-forward)
$ git merge-tree --write-tree origin/master HEAD → 35f6079…  rc=0, 冲突标记 0
$ ARIA_SUBMODULE_GATE_MODE=block bash aria/skills/phase-c-integrator/scripts/submodule_gate.sh
  PASS: standards forward bump (334c609 → ffed204)
  PASS: aria forward bump (d69091d → d1caa66)
  OK: aria-orchestrator unchanged (237045a)
  ✓ submodule_gate: all submodules unchanged/forward/first-time (mode=block)   rc=0
$ python3 aria/skills/phase-c-integrator/scripts/pre_merge_gate.py \
    --pr-branch feature/linked-issue-field-availability --main-branch master --remote origin
  {"verdict":"green","pr_ci_status":"not_applicable","in_flight_runs":[],
   "primitive_used":"aether-ci-cli","primitive_version_sha":"f29abee",
   "raw_message":"path_coverage: no workflow covers changed files (reason=no-triggering-paths); PR CI wait skipped (not_applicable); main in-flight clear",
   "path_coverage":{"decision":"not_applicable","workflows_scanned":3,"matched_workflows":[],
                    "changed_files_count":77,"reason":"no-triggering-paths","dispatchable_workflows":[]}}   rc=0
```
`not_applicable` 走的是已 ship 的 path-coverage 分支 (`pre-merge-gate-no-run-for-branch` v1.66.5), 非静默降级, 与 R1 carry `5333fe78` 同源, 不重报。
PR 侧: `forgejo GET /repos/10CG/Aria/pulls/190` → `state=open, mergeable=True, merged=False, head=17ae85e, base=c423281`。

**R1-`ae4f1c9f` 复核 — `forgejo-app-token-liveness` 已转绿**: `pass elapsed=0.21s out=OK (2 枚应用级 token 活性正常, 指纹与台账一致)` (R1 时因 `.aria/pat-inventory.yaml` 未含 `882707f` 报指纹漂移, merge origin/master `29c1e4f` 后自消, 与 PR body L31 的预测一致)。

### 5. B8 (顺序条款 = 模板对齐建议, D2 位置无关) 的可证伪性

- Spec 侧: `proposal.md:491` D2 逐字「**定位谓词 = 行首 depth-1 + fence 排除 + 文档序第一条**; 明确否决「只扫头部 N 行」」, 依据写明「两份归档件的真字段在 `:61` / `:45`, 任何 N 都是拍脑袋且造假阴性」。
- 测试侧: `test_linked_issue_field.py:506` `test_long_header_field_on_line_61_still_found` 断言 `fv.verdict=="OK"` 且 `fv.line_no==61`, docstring 带「它怎么会红」⇒ 若将来 check 改为要位置, 该测试必先红。可证伪 ✅。
- **对抗性实跑 (自造字段行在第 40 行的 proposal, 走完整 check 路径而非只调纯函数)**:
  ```
  $ sed -n '40p' <sandbox>/openspec/changes/pos-test/proposal.md
  > **Linked Issue**: `10CG/Aria#190`
  $ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py <sandbox> --grandfathered /dev/null
  OK (1 份在范围内, 0 条在册)      rc=0
  $ python3 …/linked_issue_field_probe.py --emit-arg <…>/proposal.md
  10CG/Aria#190                    rc=0   (无尾换行 = 模块 docstring :23 明写的契约)
  # 边界: 字段行在第 1 行 (标题之前) 同样 OK rc=0
  ```
- 主仓侧文案与探针行为一致 ✅: `.aria/linked-issue-field-grandfathered.txt` 头注「位置: 回填时字段行放在头部 blockquote 内任意位置均可 (探针 E0 取文档序第一条 depth-1 命中, 与行号无关, Spec D2); 建议紧随 `> **Created**:` 行」; `.aria/state-checks.yaml:362` fix 文案同款; `RESULT.md:48` 追注把 A4 定性为 skill 指令跟随断言。⇒ R1 `9ac5533a` 的处置成立, 不重报。

### 6. 跨 Spec 接缝 (导出面 + 占位串)

`sibling-spec-probe/proposal.md:137` 钉的签名 `lib/linked_issue_field.py::extract_linked_issue_field(text: str) -> FieldVerdict` vs v1.68.1 实际 `:108 def extract_linked_issue_field(text: str) -> FieldVerdict` — **逐字相符**; `FieldVerdict` `:73` / `is_sentinel` `:81` / `emit_arg` `:94` / `FIELD_NAMES` `:56` / `SENTINELS` `:57` 均在。PATCH 未动 `lib/` (diff `--name-only` 无 lib 文件), 零漂 ✅。

**占位串字节级接缝** (R1 清账把 standards 模板 Usage Note 英文化, 正是最可能碰坏这条缝的动作 — memory `split-makes-seams`):
```
standards/openspec/templates/proposal-minimal.md:6   b'{<org>/<repo>#<n>}'
aria/skills/spec-drafter/SKILL.md:143                b'{<org>/<repo>#<n>}'
openspec/changes/sibling-spec-probe/proposal.md:508  b'{<org>/<repo>#<n>}'   (SC-19 _RAW_KEY_BLACKLIST 字面)
```
三处 `bytes` 逐字节相同 ✅。`git -C standards diff fad8b4b ffed204` 实读: 只改 Usage Note 两行 (去 `不留空、不删行` 与 `关联 Issue / 无` 两处 CJK), **未触碰 `:6` 的字段行与占位串** ✅。与 memory `machine-tokens-english` 一致 (英文 canonical 写入侧, 读取侧 alias 仍在 `FIELD_NAMES`/`SENTINELS` 内)。

### 7. R1 十二条处置的逐条核验

| R1 id | 处置声称 | 我的核验 | 判定 |
|---|---|---|---|
| `e4cde200` | SC-5(d) 夹具复制完整 lib/ 只删 collision.py + 断言 ImportError 点名 `lib.collision` | 实读 `test_linked_issue_field.py:712-753`: `shutil.copytree(… ignore_patterns("collision.py"))` + `assertTrue((copy_root/"lib"/"claim_lifecycle.py").exists())` + `assertIn("lib.collision", imp.stderr)` 后才断 `##SKIP##`; 53 条全绿 | **成立** |
| `a3bfd693` | handoff frontmatter 刷新 + 「落后 1」→2 | frontmatter/`:14`/§7 已对, **正文 6 处未跟** (`:11/:23/:56/:126/:135/:177`) | **不完整 → 重报** |
| `9ac5533a` | 裁定 B8 + 主仓侧位置说明 + carry SKILL.md 软化 | D2 `:491` / 测试 `:506` / 白名单头注 / `state-checks.yaml:362` / `RESULT.md:48` 逐条实读, 并用第 40 行与第 1 行两个自造 proposal 跑通探针 | **成立** |
| `ac44ace3` | arch 两行 → 1.68.1 + CLAUDE.md 同步面 + 新 check | 两行实读 1.68.1 ✅, CLAUDE.md 同步面已列 ✅, 新 check 五态+对抗态实跑正确且真被 collector 调用 ✅; **副作用**: 同文件修订史未追记 → 新 minor `a04601ce` | **成立 (带新副作用)** |
| `ae4f1c9f` | 白名单归一统一两处 / archive 判定不用 glob / root 与 --emit-arg 互斥 exit 2 | `_normalize_entry` `:66-77` 单一函数供两处; 异地 cwd 实跑 `--grandfathered .aria/…` (相对 root 解析) → `OK (9 份在范围内, 6 条在册)`; 白名单路径写错 → `FAIL 6 项` + `(白名单文件缺失, 视为空集)` rc=1 (**fail-CLOSED, 非 fail-OPEN**); 互斥 exit 2 已由 v1.68.0 对照实跑证红 | **成立** |
| `2ed89c8a` | `sys.stdout.reconfigure(errors="replace")` | `:209` 实读; v1.68.0 对照跑复现 `UnicodeEncodeError` | **成立** |
| `a0ff4897` | 注释去 CONTRACT 引用 / `is_sentinel` 注释改真实用途 | `grep -n "CONTRACT" aria/skills/state-scanner/{scripts/linked_issue_field_probe.py,tests/test_linked_issue_field.py}` → 0 命中 | **成立** |
| `4605dc4d` | standards 模板 Usage Note 英文化 + SC-6(iii) 接受中英任一 | `git -C standards diff fad8b4b ffed204` 只两行且不碰占位串; 53 条测试全绿 (含 SC-6) | **成立** |
| `6cdc6077` | 口径注入 CHANGELOG / SUBSTITUTE / RESULT | `CHANGELOG.md` 1.68.1 节末 `> 口径注 (R1 qa minor)` ✅ / `SUBSTITUTE.md:48` ✅ / `RESULT.md:63` ✅; 本轮实测 `Ran 1462 … OK` 与 CHANGELOG 声称一致 | **成立** |
| `46b1df1a` | PREDICTION 时序接受为方法论留痕 | 无更强证据可造, 认同 | **成立 (接受)** |
| `5333fe78` | carry (C1): issue-triage workflow paths 对 gitlink bump 不触发 | 本轮 gate 实跑 `matched_workflows: []`, `reason=no-triggering-paths`, 与 carry 描述一致 | **成立 (carry)** |
| `6ab01600` | carry (C2): 3 条 active claim, D.2b 归档时 release | 未复跑 (简报禁跑 phase1_gate/release_gate); 按 carry 接受 | **接受 (未独立复跑)** |

### 8. 全量测试 (本轮实跑, 非引用)

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
Ran 53 tests in 2.160s   OK
$ python3 run_tests.py
Ran 1462 tests in 75.321s   OK
```
(Spec `tasks.md:5` 仍写「48/48 + 1457」—— 见 finding `ee23ca88`。)

### 9. 未做 / 边界声明

- 未跑 `phase1_gate` / `release_gate` / `/state-scanner` (简报禁令); `refs/aria/coordination` claim 状态按 R1 carry 接受, 未独立复跑。
- 未改动任何仓内文件: 三态测试与 v1.68.0 对照跑全部在 scratchpad 副本树内完成; 结束时 `git status --porcelain` = ` M aria-orchestrator` (与 session 起点一致)。
- `aria-plugin-benchmarks/ab-results/**` (4812 行) 作为**已冻结的 AB 运行记录**只做交叉引用核验 (RESULT/SUBSTITUTE 的追注), 其中的 `Ran 1457` 是该次运行的真实快照, 不视为漂移。
