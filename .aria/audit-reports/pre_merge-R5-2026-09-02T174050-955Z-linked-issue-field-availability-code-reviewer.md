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
timestamp: 2026-09-02T17:56:55.994Z
context: PR #190 linked-issue-field-availability (main 0db60cc / aria d1caa66 / standards ffed204)
agents: [code-reviewer]
---

# PR #190 pre_merge 收敛审计 — Round 5 (max_rounds 最后一轮) — code-reviewer (fresh 席)

> 镜头: Phase 1 规范合规 (proposal §2/§3/§4/SC 表 + CONTRACT ↔ `lib/linked_issue_field.py` / `scripts/linked_issue_field_probe.py` / spec-drafter SKILL.md hunk A/B / SOT 模板 / `.aria/state-checks.yaml` 第 13·14 条 / 白名单; 子模块自 R1 起零改动, 本席在 d1caa66 / ffed204 上逐字重核) → Phase 2 代码质量 (对抗实跑: 探针 CLI 16 例 + 纯函数 4 例 + 扫描器 8 条 mutant + 2 例降级路径, 全部在 scratchpad 临时目录; 真实语料只读)。
> 结论口径: R4 处置 (a3bfd693 指针口径 + 扫描器入库 / 3b277328 撤回 / 1d2fe175 / c0b02c06 / 95f02272 / b66c5239 / 20f4845f / ebab7adc / 4a675f17→C9-补) 逐条核验写进 §核验记录; carry (决策单 C6/C7/C9) 逐条确认确属 minor, 不重报。下列 4 条 minor 中 3 条与既有 quad 同 id (新增形态, 行内标明), 1 条为新 quad (扫描器, R4 才入库的新代码宿主)。**无一须在合并前修。**

## Phase 1 规范合规 — PASS

- 三仓交付面与 Spec Impact / yaml deliverables 一致 (本席实跑): `git -C aria diff --stat d69091d d1caa66` = 9 文件 (版本 5 + SKILL.md +19 + lib 新建 157 + probe 新建 238 + tests 新建 1172, 1625+/6−); 零改动断言 (`lib/collision.py` / `lib/__init__.py` / `state-scanner/SKILL.md` / 两既有探针) diff 为空; PATCH 增量 `fe32441..d1caa66` 对 `spec-drafter/SKILL.md` / `state-scanner/lib/` / `state-scanner/SKILL.md` diff 为空 ⇒ v1.68.1 零指令面, substitute 车道成立 (CHANGELOG `:13-21` 与之一致); `aria/skills/audit-engine/` 仅 `references` + `SKILL.md` (proposal :278 约束)。主仓 `git ls-tree 0db60cc aria standards` = d1caa66 / ffed204; tag `v1.68.0` → fe32441, `v1.68.1` → d1caa66; `ls-remote` origin/github 对 aria / standards master 均 = d1caa66 / ffed204 (只读核验, 推送本身 out_of_scope)。PR #190 head = 0db60cc = 工作树 HEAD = `origin/feature/linked-issue-field-availability`, base master, mergeable=True, merged=False; merge-base = origin/master c423281。
- 主仓 R4→R5 增量 (`git diff --stat 265a5f9 0db60cc`): 11 文件, 全部为 R4 四席报告 + 聚合 (5) / 决策单 +9 行 / 扫描器新建 57 行 / handoff 19± / latest.md 6± / yaml 2± / proposal 2± —— 无代码交付面改动, 与简报「仅主仓文档面 + 扫描器」一致。扫描器 `.aria/repro/handoff-current-state-scan.py` 不在 Spec Impact 表, 但落在既有 `.aria/repro/` 惯例目录 (同目录已有 4 个 repro 脚本), 属审计清账产物 (与 R1 新 check 同性质), 判在 anchor in_scope「决策单追记 / handoff」之内, 非 scope creep; 其质量见 Phase 2 finding 1。
- E0–E6 ↔ `lib/linked_issue_field.py` 逐字 (与 R4 同结论, 本席重核): `_FIELD_RE` `^> \*\*(?:Linked Issue|关联 Issue)\*\*:` + `IGNORECASE|ASCII` (:62-64) / `_FENCE_RE` `^[ ]{0,3}(?:> ?)?(?:\`\`\`|~~~)` (:69) 翻转且本行 `continue` (:121-125) / 首条 `break` (:126-129) / E1 不 strip (:136) / E2 `lstrip(" \t")` 首字符 U+0060 (:138-140) / E3 `find("\`", 1)` 未闭合 NO_TOKEN (:142-145) / E4 `split(",")`+`strip()` (:147) / E5 先 `is_sentinel(token_str)` 吃 E3 原串 (:149) 再逐元素 `normalize_linked_issue` (:152) / E6 `emit_arg` 仅 OK 且非哨兵 (:103-105); `VERDICTS` 四态封闭 (:58)。纯函数直调 A17–A20 (§核验记录) 与 §2/§3 字面一致。
- §4 六臂 ↔ 探针: 臂 1 `##SKIP##` (:86-88; A12 `openspec/changes` 为文件 ⇒ SKIP) / 臂 2 import 失败 `##SKIP##` 文案含 `1.68.0` (:226-229; 由 `test_sc5_d` 真实降级夹具钉住, 本席复核该测试先证 `lib.collision` 是唯一失效点再断言 SKIP, 与 R1 清账描述一致) / 臂 3 `fv.verdict != "OK"` 封闭枚举 (:129) / 臂 4 (a)(b)(c) (:145-166; A1/A3/A15 实跑) / 臂 5 末行 `(白名单文件缺失, 视为空集)` (:92-99) / 臂 6 `OK (n 份在范围内, m 条在册)` (:179)。`--emit-arg`: 母 Spec ⇒ 13 字节 `10CG/Aria#174` 无尾换行 (od 逐字节); 本 Spec / 探针 Spec ⇒ 空 (哨兵 `none`); A10 CRLF 文件 ⇒ `10CG/a#1` (无 `\r`); A11 `\` 10CG/a#1 ,10CG/b#2\`` ⇒ `10CG/a#1` (E4 strip 后首元素)。
- TASK-010/011: 白名单 6 条逐字 = §5 表 6 份 NO_FIELD (注释头 17 行含位置说明 + 「不要改 aria/ 探针」); `.aria/state-checks.yaml:346-369` 本条 7 键 (enabled true / timeout 10 / severity warning), `:372-399` 新 check `plugin-version-arch-docs-match` 7 键; 两条 command 逐字经 `sh -c` 实跑: `OK (9 份在范围内, 6 条在册)` rc=0 wall 0.18s / `OK plugin=1.68.1 (2 arch doc rows match)` rc=0。
- TASK-013 模板 (ffed204): `:6` `> **Linked Issue**: \`{<org>/<repo>#<n>}\`` 与 SKILL.md hunk B `:143` 同串; Usage Notes `:55-58` 英文 (`none` / do not leave empty / do not delete / `, ` / 引 Spec §3); CRLF 63/63 保持。TASK-014/015 hunk A (`:339-352`, 围栏外) / hunk B (`:142-143` 两行插在 `Status` 后, placeholder 非哨兵); SKILL.md CRLF 457/457 保持; 三 hunk 合计 +19 行 (1+2+16) = handoff `:112` 所记。
- 版本 16 点 (本席 grep): plugin.json / marketplace.json ×2 / aria README / aria VERSION / 主仓 CLAUDE.md :141 / VERSION:24 / README.md :8/:242 / system-architecture.md :189 / version-scheme.md :23 = 1.68.1; `1.67.2` 仅存于 system-architecture.md :968 (2.0.1 历史行) 与 aria/VERSION :6 (旧发布日期账本), 皆历史记述; master 侧 VERSION:24 仍 1.67.2 (handoff §3 首行陈述成立)。
- 计数一致性: 新测试 53 (实跑) = tasks.md :5 = PR body; state-scanner 1462 (本席实跑 161s OK) = 四处; tasks.md `- [x]` 24 / `- [ ]` 1 (5.6, :83) = yaml `status: done` 24 / `in_progress` 1 (:635) = handoff :109 = PR body「24/25」。

## 审计结论

- [minor] implementation/.aria/repro/handoff-current-state-scan.py: R4 入库的「当前态陈旧扫描器」不是 fail-CLOSED (docstring `:10` 声称), 三个形态: (i) `HIST_OK` (:20-29) 是**逐行**求值的通用子串白名单 (`aggregated` / `已完成` / `历史` / `前一` / `已推` / `均已双推` / `决策单 [BC][0-9]` …), 同行任何 STALE 命中都被整行豁免 —— 而 R4 写进派生文档的指针短语本身含 `aggregated`, 故 handoff :4/:11/:14/:127/:153/:180、latest.md :4/:13/:23、proposal :3、yaml :66 这批最易陈旧的行**结构上永远不可扫**; 8 条合成 mutant 中 6 条真陈旧句 (如「R3/R4 稳定性确认后合并 (见 aggregated 报告)」「推送授权待 owner; H1 已完成」) 全部 flagged=0; (ii) `STALE` (:15-19) 是正向枚举 blocklist ⇒ 对 R5 期措辞天然 fail-OPEN: handoff `:57`「R5 = max_rounds 最后一轮, 若仍不满足 ⇒ …」在 R5 结束后即陈旧但 STALE 无任何 R5/R6 形态 (mutant「R6 稳定性确认后合并」STALE=0); (iii) `--pr` 分支 (:45-50) PR body 不可读 ⇒ 仅 stderr 一行, 仍打印 `residual = 0` 且 exit 0 (伪造 `forgejo` 回 `{}` 实跑 rc=0) —— 「未扫」被当成「零残余」。今日真实语料 33 行被 HIST_OK 压下, 本席逐行人工判全部为历史/正确陈述 ⇒ 当前无假绿实例, 故 minor; 但决策单 R4 行把「扫描器 exit 0 且 residual = 0」写成 a3bfd693 的判据, 该判据的信息量目前主要来自人工而非机械 (memory `false-green-dual-is-permanent-red` / `invariant-needs-failclosed-default`)。修法 (下次触碰, 非合并前): HIST_OK 改为与 STALE 命中**同一 token 邻域**匹配 (或对指针行用独立锚 `^…最新一份为准` 而非通用词), STALE 加 `R[5-9]` 族, `--pr` 不可读 ⇒ exit 2 — 证据: `scratchpad/pr190/r5cr/adv_scan.py` 逐字输出 (suppressed total = 33; mutants 6×`STALE=1 HIST_OK=1 flagged=0` + 2×`STALE=0`; fake forgejo `rc = 0 | stdout: residual = 0 | stderr: PR#190 body 不可读: 'body'`) (type=risk) finding_id=d61b5fc9
- [minor] documentation/.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md: **同 quad 为 R4 `ebab7adc`, 新增形态**: R4 清账追记段标题 `:124`「PR #190 pre_merge 收敛审计 R4 清账 (2026-09-02; **四席投 PASS**; 一席判 major = 同形第四轮)」与事实相反 —— R4 tech-lead 投 **REVISE** (R4 tl 报告 `:40-42` 逐字 `## 投票` / `**REVISE**`; R4 聚合 `:20`「投票 **3 PASS / 1 REVISE**」), 且同段下方 3b277328 行正是接受该席 REVISE 所附两条处置而写。记录精度错误, 落在本轮新写文本 (memory `marginal-return-negative`: 清账文本自身引入), 不改任何机制 — 证据: `grep -n 'R4 清账' 决策单` → `:124` 逐字; `grep -n -A3 '^## 投票' pre_merge-R4-*-tech-lead.md` → `**REVISE**` (type=issue) finding_id=ebab7adc
- [minor] documentation/docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md: **同 quad 为 R4 cr `82513c94` (R4 聚合并入 a3bfd693 ×4), 新增形态**: R4「指针口径」类级清账后同文件仍残两处轮次/当前态复述, 且两处都在扫描器视野外: (i) `:114` §5 Decision memos 行逐字「追记 §B 期 B1–B7 (`989d14c`) + pre_merge R1 B8/B9 + C1–C3 + R2 B9-补 + C4–C7 + R3 C8–C9」—— 同一 commit 已向决策单追加 R4 段 (a3bfd693 ×4 / C9-补 / 记录 / 3b277328, 决策单 `:124-132`), 该行既仍按轮次枚举 (R4 裁定「派生文档不再写轮次数字」) 又漏 R4; STALE 无命中故不被扫; (ii) `:12`「**产品级待 owner: 零** (推送授权已于同日给出并执行; 剩 PR #190 合并按 owner『审计通过后合并』指令)」与同文件 `:57` H1b「(**请 owner 复议**, Rule #10) … 降级策略由 owner 选 [1]/[2]/[3]」同居: H1b 是本轮新增的 owner 动作门, `:12` 的「零」未随之更新; 该行被 HIST_OK `推送授权已于` 整行豁免。判 minor 不重报 major: H1b 行本身正确且位于「高优先级 (owner 动作门)」表首, 读者动作不变; 无 SHA / 版本 / 授权门取值错误 — 证据: `sed -n '12p;57p;114p'` 逐字; `git diff 265a5f9 0db60cc -- .aria/decisions/…` 新增 `:124-132` 段; `adv_scan.py` 输出 `…:12 STALE='推送授权' OK_by='推送授权已于'` (type=issue) finding_id=82513c94
- [minor] documentation/openspec/changes/linked-issue-field-availability/proposal.md: **同 quad 为 carry `a2a4165f` (决策单 C7, 随 B3 下次触碰 proposal 同批回写), 新增一条已知限**: §「本轮引入的新表面」#3 (`:600`) 成文三条 fence 状态机已知限 (i) 缩进代码块 / (ii) 嵌套围栏长度 / (iii) 两层 blockquote, 未列 **HTML 注释**: 多行 `<!-- … -->` 内的 `> **Linked Issue**: \`…\`` 行按 E0 字面命中 ⇒ verdict OK 且 `--emit-arg` 泄出注释掉的 token (A6 实跑 `OK` / emit `'10CG/a#1'`)。实现与 Spec 字面一致 (非实现缺陷); 真实语料 `openspec/changes/*/proposal.md` 含 `<!--` 者 2 份 (M6 release-closeout / e2e-resilience), 注释内无字段行且两份均在册 ⇒ 今日零影响; 与 (i)–(iii) 同族「成文不假装覆盖」缺一条 — 证据: `adv_probe.py` A6 输出; `grep -rln '<!--' openspec/changes/*/proposal.md` = 2; proposal `:600` 逐字三条 (type=issue) finding_id=a2a4165f

## Verdict

**PASS** — Critical 0 / Major 0 / Minor 4 (quad 去重后 4; 其中 3 条与既有 quad 同 id 为新增形态 (ebab7adc / 82513c94 / a2a4165f), 1 条新 quad (d61b5fc9, 宿主为 R4 才入库的扫描器))。

理由: 三仓交付面在 0db60cc / d1caa66 / ffed204 上逐字合规 (Phase 1 全项通过); 强制项 53 / 1462 全绿 (本席实跑), 探针 check 与 `--emit-arg` 三条与注册 command 实跑一致; 20 例对抗实跑中六臂首行 / exit code 契约在全部输入上保持 (A1/A3/A5/A8/A15/A16 fail-CLOSED, A12 SKIP, A6/A7/A9/A17 为 Spec 字面已知限族); R4 九条处置全部核验成立 (表见下); 本轮新发现全部落在「记录精度」(决策单投票记错 / handoff 两行未随类级清账) 与「扫描器自身 fail-open」(今日无假绿实例), 无假绿于真实语料、无数据风险、无跨文档 SHA / 版本 / 计数矛盾 (16 版本点 / 53 / 1462 / 24+1 / 第 13 条 在 PR body / handoff / tasks.md / proposal / yaml / CHANGELOG 间逐数一致)。

## 投票

**PASS** — 无「必须在合并前修」的 finding。逐条:

1. `d61b5fc9` 扫描器 fail-open 三形态 — **不阻塞** (否): 扫描器是 `.aria/repro/` 审计留痕工具, 不在任何 gate / state-check 路径上; 其 residual=0 结论经本席 33 行人工复核为真, 只是机械保证弱于文档声称。建议下次触碰时按 finding 内修法收紧, 并把「机械 + 人工」两句并列写进决策单 R4 行。
2. `ebab7adc` 决策单 `:124`「四席投 PASS」记错 — **不阻塞** (否): 一处记录错误, R4 聚合报告 (append-only SOT) `:20` 正确; 主控若在合并前再动主仓文档面, 顺手改为「3 PASS / 1 REVISE」。
3. `82513c94` handoff `:114` / `:12` 两处残余 — **不阻塞** (否): 无 owner 动作门取值错误 (H1b 行本身正确), 读者动作在所有取值下相同; 与上一条同批顺手收即可。
4. `a2a4165f` proposal 已知限漏 HTML 注释 — **不阻塞** (否): Spec 字面一致、真实语料零影响、carry 已有落点 (B3 下次触碰 proposal)。

不推子模块 (B9-补); 本席未修改任何仓内文件 (收尾 `git status --short` 主仓仅 ` M aria-orchestrator`, aria / standards 均空)。

## 核验记录

### 强制项 (BRIEF §纪律), 逐字

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
Ran 53 tests in 3.921s
OK                                                                  rc=0
$ cd aria/skills/state-scanner/tests && python3 run_tests.py | grep -E "^Ran |^OK|^FAILED"
Ran 1462 tests in 161.464s
OK                                                                  rc=0
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt
OK (9 份在范围内, 6 条在册)                                          rc=0
$ sh -c '<state-checks.yaml :357-358 command 逐字>'
OK (9 份在范围内, 6 条在册)                                          rc=0  real 0m0.184s (timeout 10s)
$ sh -c '<state-checks.yaml :382-392 plugin-version-arch-docs-match command 逐字>'
OK plugin=1.68.1 (2 arch doc rows match)                            rc=0
$ python3 …/linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | od -c
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4  0000015   rc=0 (13 字节, 无尾换行)
$ … --emit-arg openspec/changes/linked-issue-field-availability/proposal.md | od -c → 0000000  rc=0 (空)
$ … --emit-arg openspec/changes/sibling-spec-probe/proposal.md | od -c            → 0000000  rc=0 (空)
$ python3 .aria/repro/handoff-current-state-scan.py docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md --pr 190 --extra docs/handoff/latest.md openspec/changes/linked-issue-field-availability/tasks.md openspec/changes/linked-issue-field-availability/detailed-tasks.yaml openspec/changes/linked-issue-field-availability/proposal.md
residual = 0                                                        rc=0
```

环境: Python 3.11.2, HEAD 0db60cc (= `origin/feature/linked-issue-field-availability` ls-remote), `git submodule status` aria d1caa66 (v1.68.1) / standards ffed204; origin/master = merge-base = c423281。全部夹具在 `scratchpad/pr190/r5cr/` (脚本 `adv_probe.py` / `adv_scan.py`)。

### R4 处置核验 (BRIEF 特别请核)

| R4 id | 声称 | 本席核验 | 判定 |
|---|---|---|---|
| `a3bfd693` ×4 (派生文档指针口径 + 扫描器入库) | handoff 6 处 / latest.md 3 处 / proposal / yaml / PR body 不再写轮次数字; 扫描器 residual = 0 | `git diff 265a5f9 0db60cc` 逐 hunk: handoff :4 / :11 / :14 / :46 / :127 / :153 / :180 → 指针或已完成态; latest.md :4 / :13 / :23 → 指针; proposal :3 / yaml :66 → 指针; PR body「后续轮次」段 = 指针 + 撤回说明 (GET 回读)。扫描器本席实跑 residual = 0 rc=0 成立; **但扫描器本身 fail-open 三形态 (finding d61b5fc9), 且同文件残 :114 / :12 两处 (finding 82513c94, 皆在扫描器视野外)** | 成立 (指针口径); 机械判据弱, 残余降 minor |
| `3b277328` (C∪M 口径撤回) | 决策单 R4 行撤回 + handoff H1b 上呈 owner | 决策单 `:132` 逐字「撤回 R3『收敛口径』行, 认定为对 SOT 的偏离」+ 三选项交 owner; handoff `:57` H1b 同文; PR body「自创的 C∪M 口径已撤回 (3b277328)」; `grep -rn 'C∪M\|可执行结论集' aria/skills/audit-engine standards/` 本席未重跑 (R4 tl 已证 0 命中, 子模块零改动) | 成立 |
| `1d2fe175` (latest.md) | 指针行 / track 行 / 更新 #2 → 指针口径 | latest.md :4 / :13 / :23 三处均含「以 … aggregated.md 最新一份为准」; :25 起各 dated 更新段原文保留 (历史) | 成立 |
| `c0b02c06` (proposal Status + yaml) | → 指针口径 | proposal :3 末段「其后各轮文档口径对正; 轮次与结果以 … 最新一份为准」; yaml :66「轮次与结果以最新 aggregated 报告为准」 | 成立 |
| `95f02272` (yaml :66) | 同上 | 同上 | 成立 |
| `b66c5239` (PR body 三处) | R3 段 5m → 1M+4m; 882707f → c423281; R4 行 → 指针 | PR body 逐字「**R3** … 0C / 1M / 4m (去重 5 条)」/「master 期间前进到 `c423281` (含 aria-runner-bot `882707f` …)」/「**后续轮次**: 轮次与结果以 … 最新一份为准 … 自创的 C∪M 口径已撤回 (3b277328); R5 = max_rounds 最后一轮」 | 成立 |
| `20f4845f` (R3 聚合勘误不改写) | append-only, 决策单勘误 | `git diff --stat 265a5f9 0db60cc -- <R3 aggregated>` 为空 (未改写); 决策单 `:130`「记录」行勘误三项 | 成立 |
| `ebab7adc` (决策单记录精度) | 扫描器入库 / C9-补 / 勘误 | 决策单 `:129` C9-补 (symlink + BOM) / `:130` 记录 / 扫描器实存 57 行; **新形态: `:124` 标题「四席投 PASS」与 R4 tl REVISE 相反** (finding ebab7adc) | 成立, 记录仍不全 (minor) |
| `4a675f17` → C9-补 | symlink 两形态 + BOM 并入 v1.68.2 候选 | 决策单 `:129` + handoff `:138` carry 清单含「不可读或 symlink 的 `<slug>/` 目录 / 白名单 BOM (`utf-8-sig`)」 | 成立 |

### carry (决策单 C6 / C7 / C9) 逐条确认「确属 minor、不影响合并」

| id | carry 描述 | 本席实跑 / 实读 | 判定 |
|---|---|---|---|
| `d91f074e` (C6) | 新 check `plugin-version-arch-docs-match` 无专属测试 | command 逐字 `sh -c` 实跑 `OK plugin=1.68.1 (2 arch doc rows match)` rc=0; 7 键与其余 13 条同形; 三态由 R1/R2 实测 | carry 不反证; minor |
| `ae4f1c9f` / `2ed89c8a` / `_normalize_entry` (C7) | archive 不可读 traceback / `stdout.reconfigure` 覆盖 `--emit-arg` / `./` 中缀 | 前置条件 (chmod 000 / 非 ASCII slug × 非 UTF-8 stdout / 手写异常路径) 在真实语料与 CC Bash (UTF-8) 下均不成立; A1 (`../` 中缀) ⇒ 违规 FAIL = fail-CLOSED 方向 | minor 成立; 同意 `2ed89c8a` 最高优先 |
| `a2a4165f` (C7) | proposal §4 未回写 UNREADABLE / 互斥 / 已知限 | proposal `:420-429` 六臂表仍四态, `:425` 仍写「版本 < v1.67.0」(探针实为 1.68.0); 本席加一条 HTML 注释已知限 (finding a2a4165f) | minor 成立; carry |
| `4a675f17` (C9 + C9-补) | rglob 吞不可读 / symlink; BOM | 本席未重跑 (R3/R4 已实证); A13 嵌套三层 slug 正常入作用域并可在册 | minor 成立 |
| `9ac5533a` (B8) | hunk A 顺序条款措辞软化延后 | SKILL.md `:341` 仍「与 SOT 模板头部逐行对齐」; 白名单头注 `:4-5` + state-checks fix `:361-362` 已含「位置不限」; A17 (第 5000 行等价: 字段在 tab 缩进围栏后仍被找到) 钉位置无关 | 裁定站得住 (处方性改动须 Rule #6, 不在本循环) |

### 对抗性实跑 — 探针 CLI 16 例 (A1–A16) + 纯函数 4 例 (A17–A20), 全部临时目录 (`adv_probe.py` 逐字输出)

| 例 | 输入 | rc | stdout 首行 / 要点 | 判定 |
|---|---|---|---|---|
| A1 | 白名单条目 `openspec/changes/../changes/slug` (路径穿越) | 1 | `FAIL 1 项` + `slug/proposal.md:- NO_FIELD` | 归一不做 normpath ⇒ 条目不匹配 slug_dir ⇒ 违规 (fail-CLOSED 方向; C7 `./` 中缀同族) |
| A2 | CRLF 白名单文件 | 0 | `OK (1 份在范围内, 1 条在册)` | `strip()` 吃 `\r` |
| A3 | 条目尾随 `# M6 track` 行内注释 | 1 | `FAIL 2 项` (NO_FIELD + 陈旧 (a)) | 行内注释不支持 ⇒ 两条 FAIL 而非静默豁免 (fail-CLOSED; 白名单头注只承诺行首 `#`) |
| A4 | `> **Linked Issue**:\t\`10CG/a#1\`` (tab) | 0 | OK | E2 `lstrip(" \t")` 字面 |
| A5 | UTF-8 BOM + 字段在第 1 行 | 1 | NO_FIELD | BOM 首字符使谓词 1 不命中 ⇒ FAIL (fail-CLOSED; 真实 proposal 第 1 行恒为标题, 零影响) |
| **A6** | 多行 `<!-- … -->` 内的字段行 | **0** | **OK**; emit `'10CG/a#1'` | Spec 字面一致; 已知限族未成文 (finding a2a4165f) |
| A7 | `\`\`\`\`` 开 / `\`\`\`` 闭, 围栏内假字段, 围栏后真字段 | 0 | OK; emit `10CG/a#1` | 状态机按前缀翻转 (已知限 ii 反向: 长开短闭仍正确) |
| A8 | `\`10CG/a\`b#1\`` (token 内反引号) | 1 | `BAD_TOKEN 不可解析元素: 10CG/a` | E3 取到下一个反引号 |
| A9 | `> > \`\`\`` 两层引用围栏 + depth-1 字段 | 0 | OK | 已知限 (iii) 字面: 两层围栏不翻转, depth-1 字段仍命中 |
| A10 | `--emit-arg` CRLF 文件 | 0 | stdout `'10CG/a#1'` | `rstrip("\r")` 生效, 实参不带 `\r` |
| A11 | `--emit-arg` `\` 10CG/a#1 ,10CG/b#2\`` | 0 | `'10CG/a#1'` | E4 strip 后首元素 (E6 「第一个 token 元素」) |
| A12 | `openspec/changes` 是文件 | 0 | `##SKIP## … (作用域缺失)` | 臂 1 (`is_dir()` 判) |
| A13 | 三层嵌套 slug `a/b/c/proposal.md` + 在册 `…/a/b/c/` | 0 | `OK (1 份在范围内, 1 条在册)` | rglob 深层 + 尾斜杠归一 |
| A14 | 标题含非法 UTF-8 字节, 字段完好 | 0 | OK | `errors="replace"` 不影响字段行 |
| A15 | 在册 `ok` (哨兵 OK) + 在册 `bad` (NO_FIELD) | 1 | `FAIL 1 项` + `陈旧: …/ok (c)` | (c) 精确; bad 在册不计 |
| A16 | 字段名 `Linked\u00A0Issue` (NBSP) | 1 | NO_FIELD | `re.ASCII` 折叠只作用 ASCII, NBSP 不等于 U+0020 |
| A17 | `\t\`\`\`` tab 缩进围栏 + 字段 | — | OK `10CG/a#1` | `[ ]{0,3}` 字面: tab 缩进不算围栏 (已知限 i 同族) |
| A18 | token `\`,\`` | — | BAD_TOKEN elements `('', '')` bad `('', '')` | E4/E5 点名空元素 |
| A19 | `\`NONE\` — verified` | — | OK, emit `''` | E5 折叠 + E6 哨兵省略 |
| A20 | `\`无\u200b\`` (零宽空格) | — | BAD_TOKEN bad `('无\u200b',)` | 集合封闭, 逐字节 |

### 扫描器对抗 (`adv_scan.py` 逐字输出摘录)

```
suppressed total = 33      # 真实五文件里 STALE 命中但被 HIST_OK 压下的行; 逐行人工判: 全部为 §1 时间线 / 「前一 …」/ dated 更新段 / ab-results 路径 / 指针行 — 无一为真陈旧
  …handoff.md:153 STALE='1.68.0' OK_by='aggregated'      # 指针短语整行豁免 (形态 i)
  latest.md:4  STALE='1.68.0' OK_by='aggregated'
  latest.md:13 STALE='1.68.0' OK_by='aggregated'
  …handoff.md:12 STALE='推送授权' OK_by='推送授权已于'   # 同行「产品级待 owner: 零」不被扫 (finding 82513c94)
mutants:
  STALE=1 HIST_OK=1 flagged=0 :: R3/R4 稳定性确认后合并 (见 aggregated 报告)
  STALE=1 HIST_OK=1 flagged=0 :: 推送授权待 owner; H1 已完成
  STALE=1 HIST_OK=1 flagged=0 :: 四处未推, 待授权 — 历史上也这样
  STALE=1 HIST_OK=1 flagged=0 :: R1/R2 已清账, R3/R4 稳定性确认后合并 → 前一 handoff
  STALE=1 HIST_OK=1 flagged=0 :: aria fe32441 待 owner merge (决策单 B9)
  STALE=1 HIST_OK=1 flagged=0 :: 1.68.0 是当前版本, 均已双推
  STALE=0 HIST_OK=0 flagged=0 :: R5 = max_rounds 最后一轮, 若未收敛 R6 待 owner 加轮   # 形态 ii
  STALE=0 HIST_OK=0 flagged=0 :: R6 稳定性确认后合并
fake forgejo (echo '{}') --pr 190:  rc = 0 | stdout: residual = 0 | stderr: PR#190 body 不可读: 'body'   # 形态 iii
--extra does/not/exist.md:          rc = 1 | FileNotFoundError traceback                                   # 非 0 (可接受, 只是不整洁)
```

### 真实语料 (只读) 与跨文档一致性

- changes 9 = 3 OK (母 Spec `10CG/Aria#174` / 本 Spec `none` / sibling-spec-probe `none`) + 6 NO_FIELD = 白名单 6 条逐一 (探针 `OK (9 份在范围内, 6 条在册)`)。
- PR #190 (GET 回读): head 0db60cc = 被审 head, base master, open, mergeable=True, merged=False; body 含 v1.68.1 / d1caa66 / ffed204 / 第 13 条 / 24/25 / 53 / 1462 / 1894 / TASK-014 留记 / R1–R3 dated 段 / 「后续轮次」指针段 —— 与 handoff / tasks.md / proposal / yaml / CHANGELOG 逐数一致。
- 决策单 R4 段 `:124-132` 与 R4 聚合 `:25-37` 表逐条对应 (a3bfd693 / C9-补 / 记录 / 3b277328), 唯 `:124` 投票记述错 (finding ebab7adc)。
- 手工核对 handoff 全文当前态: `:22` 子模块停本地 master 与 gitlink 一致 (`git submodule status` 无 `+`); `:83` master 侧 VERSION:24 = 1.67.2 (实读); `:88` origin/master = c423281 (fetch 后 rev-parse); `:145` feature 已推 (ls-remote = 0db60cc); `:150` aria-orchestrator gitlink 237045a (`git ls-tree HEAD` 实读); 残余仅 `:12` / `:114` 两处 (finding 82513c94)。
