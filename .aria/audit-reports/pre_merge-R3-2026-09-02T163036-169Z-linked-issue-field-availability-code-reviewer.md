---
checkpoint: pre_merge
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS
timestamp: 2026-09-02T16:55:18.048Z
context: PR #190 linked-issue-field-availability (main fdfb183 / aria d1caa66 / standards ffed204)
agents: [code-reviewer]
---

# PR #190 pre_merge 收敛审计 — Round 3 — code-reviewer (fresh 席)

> 镜头: Phase 1 规范合规 (proposal §2/§3/§4/SC 表 + TASK-007~011 / TASK-013~015 ↔ `lib/linked_issue_field.py` / `scripts/linked_issue_field_probe.py` / spec-drafter SKILL.md hunk A/B / SOT 模板; 子模块自 R2 起零改动, 本席在 d1caa66 / ffed204 上逐字重核) → Phase 2 代码质量 (46 例对抗性实跑: 探针 CLI 31 例 + 纯函数 15 例, 全部在 scratchpad 临时目录; 真实语料 149 份只读扫描)。
> 结论口径: R2 carry (决策单 C6/C7) 与 R2 两条 major 的清账逐条核验后写进 §核验记录, 不重报; 下列 5 条 minor 中 3 条与 R2 carry 同四元组 (同 id) 但是**新增形态**, 已在行内标明; 2 条为新 quad (handoff 残余 / PR body 漏记)。无一须在合并前修。

## Phase 1 规范合规 — PASS

- 文件路径与 Spec Impact / yaml deliverables 一致: `git -C aria diff --stat d69091d d1caa66` = 9 文件 (版本 5 文件 + SKILL.md +19 + lib 新建 157 + probe 新建 238 + tests 新建 1172); 零改动断言 (`lib/__init__.py` / `lib/collision.py` / `state-scanner/SKILL.md` / 两既有探针) diff 为空; `aria/skills/audit-engine/` 下无 `lib/` `collectors/` (:278)。
- E0–E6 ↔ `lib/linked_issue_field.py` 逐字: `_FIELD_RE = ^> \*\*(?:Linked Issue|关联 Issue)\*\*:` + `re.IGNORECASE | re.ASCII` (:62-64, TASK-007 逐字条) / `_FENCE_RE = ^[ ]{0,3}(?:> ?)?(?:```|~~~)` (:69) 翻转且本行 `continue` (:121-125) / 谓词 3 首条 `break` (:126-129) / E1 不 strip (:136) / E2 `lstrip(" \t")` 后首字符 U+0060 (:138-140) / E3 `find("`", 1)` 未闭合 NO_TOKEN (:142-145) / E4 `split(",")` + `strip()` (:147) / E5 先 `is_sentinel(token_str)` 吃 E3 原串 (:149) 再逐元素 `normalize_linked_issue` (:152) / E6 `emit_arg` 仅 OK 且非哨兵 (:103-105)。`VERDICTS` 四态封闭 (:58); `FieldVerdict` = proposal 钉的 4 字段 + additive `bad_elements` (裁量 3)。实测 `关联 issue` 命中 (H4) / KELVIN SIGN 不命中 (53 测试内 SC1h) 与 O-5「折叠只作用于 ASCII 字母」一致。
- §4 六臂 ↔ 探针: 臂 1 `##SKIP##`(:86-88) / 臂 2 import 失败 `##SKIP##` 文案含 `1.68.0` (:226-229, `<vNEXT>` 已回填为该符号首现版本, PATCH 后仍正确) / 臂 3 `fv.verdict != "OK"` 封闭枚举 (:129) / 臂 4 (a)(b)(c) `FAIL allowlist 陈旧: <e> (x)` (:145-166, :176) / 臂 5 末行 `(白名单文件缺失, 视为空集)` (:92-99, :182-183) / 臂 6 `OK (n 份在范围内, m 条在册)` (:179)。TASK-008 输出格式 (首行 `FAIL k 项` / 违规行 `<rel>:<line|-> <VERDICT> <细节>` 路径字典序在前 / 陈旧行在后) 实跑一致 (E1 / F3 / A1)。
- TASK-009: `--emit-arg` 读单文件 → `sys.stdout.write(emit_arg(fv))` 无换行 (:189-197); 读失败 / import 失败 exit 2 且 stdout 空 (D3 / SC-9 测试); 与 `--grandfathered` 互斥 (argparse group :62-64, D1) 与 root 互斥 (:204-205, D2)。母 Spec 接缝: `--emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` ⇒ 13 字节 `10CG/Aria#174` 无尾换行; 本 Spec ⇒ 空 (见核验记录)。
- TASK-010 白名单: 6 条逐字 = §5 表 6 份 NO_FIELD (真实语料扫描 changes 9 = 3 OK + 6 NO_FIELD, 6 份恰为在册); 头注含格式 / 陈旧守卫三子情形 / 「回填一份删一条」/ O-1 指针 / 「不要改 aria/ 探针」。TASK-011: `_parse_state_checks_yaml` 解析 14 条, 本条 7 键 (`command/description/enabled/fix/name/severity/timeout_seconds`) 零新键, `enabled=True timeout=10 severity=warning`; 注册 command 经 `sh -c` 实跑 `OK (9 份在范围内, 6 条在册)` rc=0, wall 0.22s (timeout 10s 余量 45x)。
- TASK-013 模板 (ffed204): `:6` canonical `> **Linked Issue**: `{<org>/<repo>#<n>}`` 与 SKILL.md hunk B `:143` 同串; Usage Notes `:55-58` 英文: `none` / do not leave the value empty / do not delete the line / `, ` / 引 Spec §3; 全文 `alias` / `关联` / `无` 零命中 (写入侧只教 canonical)。CRLF 保持 (63/63 行)。
- TASK-014 hunk A: `## proposal.md 头部字段要求` (:339-352) 落在 `## tasks.md 格式要求` (:356) 之前, 围栏外, 不在 :127-162, 不碰 :10; A.1.4 指针 `:113`; 写法三条 (code span / `, ` / `none` 不留空不删行, N/A TBD - 非哨兵 / 行首形态 + 不写 markdown 链接形) + 模板相对链接 (:341, 解析到存在文件, SC-6(iv)) + Spec §3 引用。**未满足的一条见 finding b66c5239** (母 Spec 分支不存在时应在 PR 说明记「未核验」)。
- TASK-015 hunk B: Level 2 预览围栏 :140-143 四行 `Level → Status → Created → Linked Issue`, placeholder 非哨兵 (SC-7a 测试绿); Level 3 预览围栏 (:166-185) 无任何 `> **` 头部行 ⇒ 条件分支不触发。SKILL.md CRLF 保持 (457/457 行)。
- Rule #6 / B9: `git -C aria diff --stat fe32441 d1caa66 -- skills/spec-drafter/SKILL.md skills/state-scanner/lib/ skills/state-scanner/SKILL.md` 为空 ⇒ PATCH 零指令面改动, substitute 车道成立。

## 审计结论

- [minor] documentation/docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md: R2 对 `a3bfd693` 的类级清账仍漏 3 处**当前态陈述** (非历史记述): `:46`「Cycles shipped this session: 0 (C.2 推送 + PR + D 待授权后走)」/ `:178` footer「Status: Active — 下个 session 第一件事 = owner 推送授权 → C.2 + PR → D」(与 `:23` §0「第一件事 = 看审计是否已收敛并合并」直接矛盾) / `:12`「只剩推送授权这一动作门」(现存动作门 = merge); R2 聚合表声称「footer 全部对正」与 `:178` 实况不符 (第三轮同形残余, memory fix-the-class)。§0 / §6 入口段已正确, 读者按文档自身路由不会落到这三行 ⇒ minor; 修 = 三处各一行文本 (主仓文档, 无推送授权问题) — 证据: `sed -n '12p;46p;178p'` 逐字; `git diff 17ae85e fdfb183 -- docs/handoff/…` 未触及 :46/:178 (type=issue) finding_id=82513c94
- [minor] implementation/aria/skills/state-scanner/scripts/linked_issue_field_probe.py: **同 quad 为 R2 carry ae4f1c9f, 本条为新增同类形态**: 在册条目的 slug **目录**不可读 (chmod 000) ⇒ 陈旧守卫 `cand.is_file()` (:150) 对 EACCES 不吞 (pathlib 只忽略 ENOENT/ENOTDIR/EBADF/ELOOP) ⇒ `PermissionError` traceback, stdout 空, exit 1 (违反 SC-8(c) 首行前缀契约), 与 R2 archive 目录不可读同形; 修法同 C7 候选 (读/stat 目录处包 `try/except OSError` ⇒ 记 UNREADABLE 或 (a)) — 证据: 核验记录 B3 `rc=1 stdout='' stderr 末行 PermissionError … /openspec/changes/secret/proposal.md`; B5 复现 R2 archive 形态 (type=issue) finding_id=ae4f1c9f
- [minor] implementation/aria/skills/state-scanner/scripts/linked_issue_field_probe.py: **同 quad 为 R2 carry 4a675f17, 两条新增形态**: (i) **不在册**的 slug 目录不可读 ⇒ `changes.rglob("proposal.md")` (:85) 内部 `except PermissionError: return` 静默吞掉该目录 ⇒ 该 proposal **从作用域消失**, 探针输出 `OK (1 份在范围内, 0 条在册)` exit 0 —— 方向是 **fail-OPEN by omission** (零证据当正证据), 比文件级 UNREADABLE (fail-closed) 与目录级 traceback 都差; 前置条件极端 (git 不存储目录权限, 须手工 chmod), 故仍 minor, 但建议在 v1.68.2 候选里与 ae4f1c9f 一并改为 `os.walk(onerror=…)` / 逐目录 `scandir` 把不可读目录记为 UNREADABLE 违规; (ii) 白名单文件带 UTF-8 BOM 时首条目 `﻿openspec/changes/x` 不被 `strip()` 归一 ⇒ 不豁免 + 陈旧 (b), fail-closed 但输出行含不可见字符; 修 = `encoding="utf-8-sig"` — 证据: 核验记录 B2 `rc=0 first='OK (1 份在范围内, 0 条在册)'` (secret/ 含 NO_FIELD proposal 却未列出); A2 stdout 逐字 `FAIL allowlist 陈旧: ﻿openspec/changes/x (b)`; A4 复现 R2 `./` 中缀形态 (type=risk) finding_id=4a675f17
- [minor] documentation/openspec/changes/linked-issue-field-availability/proposal.md: **同 quad 为 R2 carry a2a4165f, 新增一条已知限漏记**: 「新表面」#3 三条 fence 已知限未含**围栏标记种类不匹配**子形态 —— `~~~` 开块内出现行首 ``` 时状态机翻转 (E0 谓词 2 字面「凡匹配 … 的行翻转」), CommonMark 则不视为闭合 ⇒ 块内字段行被判真字段 (G3 实跑 `OK`); 实现与 proposal 字符级一致, 属 spec 级已知限须成文 (与 (ii)「嵌套围栏长度差」同族), 随 B3 下次触碰 proposal 同批 — 证据: 核验记录 G3 `~~~ / text / ``` / 字段行 / ~~~` ⇒ `OK (1 份在范围内, 0 条在册)`; proposal `:600` 已知限 (i)(ii)(iii) 逐字无此形态 (type=issue) finding_id=a2a4165f
- [minor] documentation/PR#190/body: TASK-014 verification 逐字「若母 Spec 分支已存在: `git merge-tree` 干跑核验两 hunk 无冲突; 不存在则在 PR 说明记『未核验, 母 Spec 落地时复核』」—— aria 仓无任何 a1-entry / claim 分支 (`git -C aria branch -a` 零命中) ⇒ 应走第二分支, 但 PR #190 body (44 行) / handoff / RESULT.md / 审计轨均无 `merge-tree` / `未核验` / `母 Spec 落地时复核` 字样; tasks.md 3.2 已勾 `[x]`。零合并风险 (今日无对手 hunk), 修 = PR body 加一句 (Forgejo PATCH, R2 已用同法) — 证据: `forgejo GET /repos/10CG/Aria/pulls/190` body 关键词 `merge-tree`=False `未核验`=False `母 Spec`=0 hits; `grep -rn "merge-tree\|母 Spec 落地时复核" ab-results/…/ docs/handoff/2026-09-02-… .aria/audit-reports/…-audit-trail.md` 零命中 (type=issue) finding_id=b66c5239

## Verdict

**PASS** — Critical 0 / Major 0 / Minor 5 (quad 去重后 5; 其中 3 条与 R2 carry 同 quad)。

理由: 三仓交付面在当前 head 上逐字合规 (Phase 1 全项通过); 46 例对抗实跑中六臂首行 / exit code 契约在全部**非极端**输入上保持, 真实语料 149 份判定分布 (changes 3 OK + 6 NO_FIELD; archive 126 NO_FIELD + 14 NO_TOKEN) 与 proposal §Why 观测表逐数相等; 新发现全部落在「目录级权限」「BOM」「围栏标记种类」三类极端前置或文档残余, 无假绿于现实语料、无数据风险。R2 两条 major 的清账: `ee23ca88` 完整 (三文件 SHA/版本齐, checkbox 24 = yaml done 24), `a3bfd693` 主体完整但残 3 行 (本轮降为 minor 重报)。

## 投票

**PASS** — 无「必须在合并前修」的 finding。建议 (不阻塞): R3 清账若动主仓文档面, 顺手收 `82513c94` (3 行) 与 `b66c5239` (PR body 1 句); aria 侧三处新增形态并入决策单 C7 的 v1.68.2 候选清单 (其中 4a675f17-(i) 的 fail-OPEN 方向建议排在 2ed89c8a 之后第二优先), 不在本循环推子模块 (B9-补)。

## 核验记录

### 强制项 (BRIEF §纪律), 逐字

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
Ran 53 tests in 2.126s
OK
$ python3 run_tests.py | grep -E "^Ran |^OK|^FAILED"
Ran 1462 tests in 95.315s
OK
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt
OK (9 份在范围内, 6 条在册)                                    rc=0
$ sh -c '<state-checks.yaml command 逐字>'                       → 同上 rc=0   (wall 0.22s)
$ python3 …/linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | od -c
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4      rc=0  (13 字节, 无尾换行)
$ python3 …/linked_issue_field_probe.py --emit-arg openspec/changes/linked-issue-field-availability/proposal.md | od -c
0000000                                                           rc=0  (空; 哨兵 none)
$ find openspec/changes -name proposal.md | wc -l → 9 ; ls -d openspec/changes/*/ | wc -l → 9
```

环境: Python 3.11.2, uid 1000 (非 root, chmod 000 夹具有效), HEAD fdfb183; `git submodule status` aria d1caa66 (v1.68.1) / standards ffed204。收尾 `git status --short` 主仓仅 ` M aria-orchestrator` (会话起点即有), `git -C aria status --short` / `git -C standards status --short` 均空 ⇒ 三仓零写入; 全部夹具在 `scratchpad/pr190/r3cr/work/` (脚本 `scratchpad/pr190/r3cr/adv.py`)。

### R2 两条 major 的清账完整性 (BRIEF 特别请核)

| R2 id | 声称 | 本席核验 | 判定 |
|---|---|---|---|
| `ee23ca88` (Spec 三文件口径) | proposal Status 行 + tasks.md Status/5.3/5.4 + yaml metadata.status 追加 v1.68.1 / d1caa66 / ffed204 / 53 / 1462 | `grep -c` 逐 token: proposal.md `1.68.1`=1 `d1caa66`=1 `ffed204`=1 `53`=1 `1462`=1; tasks.md `1.68.1`=2 `d1caa66`=2 `ffed204`=2 `53/53`=1 (`:5`) `1462`=1; detailed-tasks.yaml `:66` metadata.status 含 `v1.68.1 d1caa66` + `ffed204` (测试计数不在 yaml 声称集内, R2 tech-lead 原 finding 要求的是三文件 SHA/版本 + tasks.md:5 计数); tasks.md `- [x]` = **24**, `- [ ]` = 1 (5.6); yaml `status: done` = **24**, 唯一非 done = `:635` TASK-025 `in_progress` ⇒ 24 = 24 | **完整** |
| `a3bfd693` (handoff 当前态) | 标题 / 一句话 / §0-2 / §2 H1 / §3 风险行 / §5 三行 / §6 1-2 条 / 不应该做的 / footer 全部对正 | 全文 grep `未推|待 owner 授权|1.68.0|待授权` 逐处判: `:9` `:11` 叙事箭头 (历史) / `:41-43` §1 时间线带时戳 (历史) / `:56` H1 行标 ✅ 已完成「原文保留供追溯」(历史) / `:64` M2「待授权」指 #116 评论 (仍成立) / `:82` `:111` `:115` `:146` `:151` 已对正 / `:168` 为目录名; **未对正的当前态**: `:12` `:46` `:178` (见 finding 82513c94); `git diff 17ae85e fdfb183` 对该文件的 hunk 未触及 :46 / :178 | **主体完整, 残 3 行** ⇒ 降级重报 |

B9-补 (决策单 `:108`) 自纠核验: 明写「按『通过后合并』**类推**自授权, 不是字段级匹配」+「已推内容不撤 (撤 = 再一次外向动作)」+「本循环不再推任何子模块 commit」+「v1.68.2 候选由 owner 决定」; 与 memory `sync≠push-auth` (推共享 master 外向不可撤销须显式确认, 不能自我授权) 与 `exact-exception-condition` (字段级匹配) 同口径; handoff `:23` §0 与 `:135` 「不应该做的」各复述一次该约束。判定: **诚实且一致**。

### R2 carry (决策单 C6 / C7) 逐条确认「确属 minor、不影响合并」

| id | R2 描述 | 本席实跑 | 判定 |
|---|---|---|---|
| `ae4f1c9f` | archive 目录不可读 + 陈旧候选 ⇒ traceback | B5: `rc=1 stdout=''` stderr 末行 `PermissionError … /openspec/archive` | minor 成立 (前置 = chmod 000 on git 目录); **新增同形 B3** (在册 slug 目录不可读) 同 quad |
| `4a675f17` | `_normalize_entry` 残余 `./` 中缀 | A4: `openspec/changes/./x` `openspec/changes/x/.` ⇒ `FAIL 1 项` NO_FIELD (不豁免, 无陈旧行, fail-closed) | minor 成立; **新增 B2 (fail-open by omission) + A2 (BOM)** 同 quad |
| `2ed89c8a` | `stdout.reconfigure` 覆盖 `--emit-arg`, 非 ASCII 实参被改写 | C4: `PYTHONIOENCODING=ascii` + `10CG/仓库#1` ⇒ stdout bytes `b'10CG/??#1'` rc=0 (`normalize_linked_issue('10CG/仓库#1')` = `('仓库', 1)`, E5 接受) | minor 成立 (前置 = 非 ASCII repo slug + 非 UTF-8 stdout; 消费方 CC Bash 为 UTF-8); 同意 C7「候选内最高优先」(E6「探针自身失败 ⇒ 非 0」语义回退) |
| `a2a4165f` | UNREADABLE / 不可读 note / root+emit-arg 互斥 未回写 SOT | proposal §4 六臂表 `:420-429` + TASK-008 `:270` 仍只列四态; TASK-009 `:294` 只写与 `--grandfathered` 互斥 | minor 成立; **新增 G3 已知限漏记** 同 quad |
| `d91f074e` (C6) | 新 check 无专属测试 | `plugin-version-arch-docs-match` 经 `_parse_state_checks_yaml` 解析 7 键 enabled=True timeout=5; 本席未重跑其三态 (R1/R2 已实测), 镜头外 | 按聚合记录, carry 不反证 |

### 对抗性实跑 (46 例; 探针 CLI 31 + 纯函数 15; 全部临时目录)

| 例 | 输入 | rc | stdout 首行 / 要点 | 判定 |
|---|---|---|---|---|
| A1 | 白名单条目带行内注释 `openspec/changes/x  # inline comment` | 1 | `FAIL 2 项` (NO_FIELD + 陈旧 (a)) | fail-closed (不支持行内注释, 与头注「`#` 起首为注释」一致) |
| A2 | 白名单文件 UTF-8 BOM | 1 | `FAIL 2 项`; 陈旧行 `﻿openspec/changes/x (b)` | fail-closed; 输出含不可见字符 (finding 4a675f17-(ii)) |
| A3 | 条目大小写不符 `openspec/changes/X` | 1 | `FAIL 2 项` | fail-closed |
| A4 | R2 4a675f17 `./` 中缀 ×2 | 1 | `FAIL 1 项` (仅 NO_FIELD, 无陈旧行) | carry 复现 |
| B1 | proposal.md chmod 000 | 1 | `FAIL 1 项` `…:- UNREADABLE PermissionError` | fail-closed (R2 c11 复现) |
| **B2** | slug 目录 chmod 000, **不在册** | **0** | `OK (1 份在范围内, 0 条在册)` — secret/ 的 NO_FIELD proposal 未出现 | **fail-OPEN by omission** (finding 4a675f17-(i)) |
| **B3** | slug 目录 chmod 000, **在册** | 1 | stdout 空, `PermissionError` traceback | 违反 SC-8(c) (finding ae4f1c9f 新形态) |
| B4 | `openspec/changes` 自身 chmod 000 | 0 | `##SKIP## openspec/changes/ 不存在或 0 份 proposal.md (作用域缺失)` | 保守结局 (SKIP 非 OK); 文案「0 份」对「不可读」失准, 不计 |
| B5 | archive chmod 000 + 陈旧候选 | 1 | stdout 空, traceback | R2 ae4f1c9f 复现 |
| C1 / C1b | UTF-8 BOM + 字段在第 1 行 / 第 3 行 | 1 / 0 | NO_FIELD / OK | 第 1 行形态在真实 proposal 不存在 (`# 标题` 恒占首行), 不计 |
| C2 | UTF-16 文件 | 1 | `FAIL 1 项` NO_FIELD | fail-closed |
| C3 | token 内 NUL 字节 | 0 | OK (`normalize` 接受 `10CG/a\x00#1`) | v1.67.0 归一既有语义, 非本 PR, 不计 |
| C4 | `--emit-arg` 非 ASCII token × ascii stdout | 0 | `10CG/??#1` | R2 2ed89c8a 复现 |
| C5 | CRLF 文件 check / emit | 0 / 0 | OK / `10CG/a#1` | `rstrip("\r")` 成立 |
| D1–D6 | `--emit-arg`+`--grandfathered` / root+`--emit-arg` / `--emit-arg ""` / 两个 root / `--grandfathered` ×2 / `--emit-arg` ×2 | 2/2/2/2/0/0 | argparse 拒绝 ×4 (stderr 一行, stdout 空); 重复 flag 取最后 | 互斥成立; 重复取后者为 argparse 默认, 不计 |
| E1 / E1b | 嵌套 `a/b/c/proposal.md`, 白名单 `a` / `a/b/c` | 1 / 0 | `FAIL 2 项` (嵌套 NO_FIELD + `a` 陈旧 (c)) / `OK (2 份在范围内, 1 条在册)` | 逐 proposal 独立 slug_dir, 与 `**` 作用域一致 |
| E2 | `openspec/changes/proposal.md` (无 slug) + 白名单 `openspec/changes` | 1 | `FAIL 1 项` 陈旧 (b) | fail-closed |
| E3 / E4 | changes/ 下 symlink 目录环 / proposal.md 为 symlink 指向 archive 文件 | 0 / 0 | OK / OK | rglob 不递归 symlink 目录; 文件 symlink 正常读 |
| E5 | `Proposal.md` / `proposal.MD` | 0 | OK (1 份) | 大小写变体不在作用域 (Linux 大小写敏感), 设计如此 |
| F1 / F2 / F3 / F4 | 空文件 / 仅空白 / 空 code span / 0 字节白名单 | 1/1/1/0 | NO_FIELD / NO_FIELD / `BAD_TOKEN 不可解析元素:  (无关联请写 \`none\`)` / OK 0 在册 | 契约 §1 步 10 逐字 (空 span ⇒ `("",)`) |
| G1 / G2 | 只有围栏含字段 / 未闭合围栏后字段 | 1 / 1 | NO_FIELD / NO_FIELD | E0 谓词 2 成立; 未闭合方向 fail-closed |
| **G3** | `~~~` 开块, 块内行首 ``` , 字段行, `~~~` | 0 | OK | 状态机按任意标记翻转 (proposal 字面) vs CommonMark 不闭合 ⇒ 块内字段被判真 (finding a2a4165f 新形态) |
| G4 / G5 | `> ```` 引用内围栏示例后真字段 / 4 反引号围栏后真字段 | 0 / 0 | emit `10CG/real#2` / `10CG/real#2` | 谓词 2 `(?:> ?)?` 与前缀匹配成立 |

纯函数 15 例 (H1–H15): 冒号后无空格 OK / tab OK / NBSP ⇒ NO_TOKEN / `关联 issue` OK / 双反引号 span ⇒ BAD_TOKEN `("",)` / 尾随空元素 ⇒ BAD_TOKEN `("",)` / `none,` ⇒ BAD_TOKEN `('none','')` / `NONE` OK emit 空 / `无 ` ⇒ BAD_TOKEN / 元素两侧空白 OK emit `10CG/a#1` / 表格行内 ⇒ NO_FIELD / 全角星号 ⇒ NO_FIELD / CR-only 行尾 ⇒ NO_FIELD (整文件单行) / `>>>` ⇒ NO_FIELD / 字段名双空格 ⇒ NO_FIELD。全部与 proposal E0–E6 字面一致, 无一偏离。

`normalize_linked_issue` 直测: `none` / `无` / `N/A` / `` / `#1` / `10CG/a` / `TBD` ⇒ None; `10CG/a#1` ⇒ `('a', 1)`; `10CG/仓库#1` ⇒ `('仓库', 1)`; `a#1` ⇒ `('a', 1)` —— 与 SC-4 (c)(f) 期望所需的 `normalize("none") is None` 成立。

### 真实语料 (只读扫描, `extract_linked_issue_field` 直调)

```
changes  n=9   {'OK': 3, 'NO_FIELD': 6}    OK = a1-entry (10CG/Aria#174, emit 同串) / 本 Spec (none, emit 空) / sibling-spec-probe (none, emit 空); 6 NO_FIELD = 白名单 6 条逐一
archive  n=140 {'NO_FIELD': 126, 'NO_TOKEN': 14}
```
与 proposal §Why「当日观测值」表 (archive 126/14/0; changes 3 OK / 6 NO_FIELD) 逐数相等; 全语料零 BAD_TOKEN。

### 版本面 / 注册面

`grep -n "1\.68\.\|1\.67\.2" CLAUDE.md VERSION README*.md docs/architecture/{system-architecture,version-scheme}.md`: 14 引用点全部 `1.68.1`, `1.67.2` 零命中; `system-architecture.md` 头部 2.0.2 + Version History `:967` 2.0.2 行 (C5 已修)。`aria/.claude-plugin/plugin.json` = 1.68.1。`.aria/state-checks.yaml` 14 条, 本条第 13 (`:346`), 新 check 第 14 (`:372`); `git diff 17ae85e fdfb183` 对该文件只改 fix 文案括注 (C4)。PR #190: head `fdfb183` = 被审 head, base master, open, mergeable=True, 标题/正文含 v1.68.1 / d1caa66 / ffed204。
