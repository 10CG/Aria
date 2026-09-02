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
verdict: PASS
timestamp: 2026-09-02T17:29:12.097Z
context: PR #190 linked-issue-field-availability (main 265a5f9 / aria d1caa66 / standards ffed204)
agents: [code-reviewer]
---

# PR #190 pre_merge 收敛审计 — Round 4 (稳定性确认轮) — code-reviewer (fresh 席)

> 镜头: Phase 1 规范合规 (proposal §2/§3/§4/SC 表 + CONTRACT ↔ `lib/linked_issue_field.py` / `scripts/linked_issue_field_probe.py` / spec-drafter SKILL.md hunk A/B / SOT 模板 / `.aria/state-checks.yaml` / 白名单; 子模块自 R1 起零改动, 本席在 d1caa66 / ffed204 上逐字重核) → Phase 2 代码质量 (对抗实跑 30 例 CLI + 9 例纯函数 + 2 例 C7 复现, 全部在 scratchpad 临时目录; 真实语料只读)。
> 结论口径: R3 处置 (a3bfd693 类级清账 / C8 TASK-014 留记 / tasks.md 1894) 逐条核验写进 §核验记录; R2/R3 carry (决策单 C6/C7/C9) 逐条确认确属 minor, 不重报; 下列 3 条 minor 中 2 条与既有 quad 同 id (新增形态, 行内标明), 1 条为决策单 scope 新 quad。**无一须在合并前修。**

## Phase 1 规范合规 — PASS

- 三仓交付面与 Spec Impact / yaml deliverables 一致: `git -C aria diff --stat d69091d d1caa66` = 9 文件 (版本 5 + SKILL.md +19 + lib 新建 157 + probe 新建 238 + tests 新建 1172); 零改动断言 (`lib/collision.py` / `lib/__init__.py` / `state-scanner/SKILL.md` / 两既有探针) diff 为空; `aria/skills/audit-engine/` 仅 `references` + `SKILL.md` (无 `lib/` `collectors/`, proposal :278)。主仓 gitlink `git ls-tree 265a5f9 aria standards` = d1caa66 / ffed204; tag `v1.68.1` → d1caa66, `v1.68.0` → fe32441。
- E0–E6 ↔ `lib/linked_issue_field.py` 逐字: `_FIELD_RE` `^> \*\*(?:Linked Issue|关联 Issue)\*\*:` + `IGNORECASE|ASCII` (:62-64) / `_FENCE_RE` `^[ ]{0,3}(?:> ?)?(?:```|~~~)` (:69) 翻转且本行 `continue` (:121-125) / 首条 `break` (:126-129) / E1 不 strip (:136) / E2 `lstrip(" \t")` 首字符 U+0060 (:138-140) / E3 `find("`", 1)` 未闭合 NO_TOKEN (:142-145) / E4 `split(",")`+`strip()` (:147) / E5 先 `is_sentinel(token_str)` 吃 E3 原串 (:149) 再逐元素 `normalize_linked_issue` (:152) / E6 `emit_arg` 仅 OK 且非哨兵 (:103-105); `VERDICTS` 四态封闭 (:58)。纯函数直调 P1–P9 (§核验记录) 全部与 §2/§3 字面一致 (`无` OK emit 空 / `無` BAD_TOKEN / `NoNe` OK / `关联 ISSUE` 折叠命中 / `无 ` BAD_TOKEN / 未闭合围栏后字段 NO_FIELD)。
- §4 六臂 ↔ 探针: 臂 1 `##SKIP##` (:86-88, K8/K9 实跑) / 臂 2 import 失败 `##SKIP##` 文案含 `1.68.0` (:226-229, K21/K22 实跑) / 臂 3 `fv.verdict != "OK"` 封闭枚举 (:129) / 臂 4 (a)(b)(c) (:145-166, K11–K14/K19 实跑) / 臂 5 末行 `(白名单文件缺失, 视为空集)` (:92-99, K10 实跑) / 臂 6 `OK (n 份在范围内, m 条在册)` (:179)。`--emit-arg`: 母 Spec ⇒ 13 字节 `10CG/Aria#174` 无尾换行; 本 Spec / 探针 Spec ⇒ 空; BAD_TOKEN 混合 `10CG/a#1, TBD` ⇒ 空 (K18, E6 四格「只有 OK 且非哨兵产生实参」)。
- TASK-010/011: 白名单 6 条逐字 = §5 表 6 份 NO_FIELD; `_parse_state_checks_yaml` 解析 14 条, 本条第 13 (7 键 `command/description/enabled/fix/name/severity/timeout_seconds`, enabled=True timeout=10 severity=warning), 新 check 第 14; 注册 command 逐字经 `sh -c` 实跑 `OK (9 份在范围内, 6 条在册)` rc=0 wall 0.11s。
- TASK-013 模板 (ffed204): `:6` `> **Linked Issue**: `{<org>/<repo>#<n>}`` 与 SKILL.md hunk B `:143` 同串; Usage Notes `:55-58` 英文 (`none` / do not leave empty / do not delete / `, ` / 引 Spec §3); 全文 `alias|关联|无` 0 命中; CRLF 63/63 保持。
- TASK-014/015 hunk A (`:339-352`, 围栏外, 不在 :127-162, 不碰 :10; 相对链接 `:341` `:448` 解析到存在文件) / hunk B (Level 2 预览围栏 `:140-143` 四行 `Level → Status → Created → Linked Issue`, placeholder 非哨兵); SKILL.md CRLF 457/457 保持。TASK-014 verification 第二分支 (`git -C aria branch -a | grep -ci a1-entry` = 0 ⇒ 记「未核验」): PR body + handoff `:136` + 决策单 C8 三处已记。
- Rule #6 / B9: `git -C aria diff --stat fe32441 d1caa66 -- skills/spec-drafter/SKILL.md skills/state-scanner/lib/ skills/state-scanner/SKILL.md` 为空 ⇒ PATCH 零指令面, substitute 车道成立; CHANGELOG 1.68.1 `rule6_note: substitute` 与之一致。

## 审计结论

- [minor] documentation/docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md: R3 类级清账 (决策单「a3bfd693 ×3」行) 对**推送授权类** token 残余为零 (本席复扫成立), 但同一「当前态陈述」类里**轮次进度**这一子类未纳入 STALE 正则 ⇒ 同文件仍矛盾: `:4` frontmatter「R3 0C/1M 已清账, R4 稳定性确认」/ `:179` footer「R1–R3 已清账, R4 稳定性确认后」 vs `:14` Status「R1/R2 已清账, R3/R4 稳定性确认后」/ `:126` §6 第 1 条「R1/R2 已清账, R3 (+R4 稳定性确认) → 合并」; `:46`「Cycles shipped this session: 0 (C.2 推送 + PR + D **待授权后走**)」括注仍是推送前理由 (R3 cr `82513c94` 已逐字点名 `:46`, R3 清账未收)。判 minor 而非重报 major: 读者动作在所有取值下相同 (等稳定性确认 → 合并), §0 `:23` 入口与 footer 正确, 无 owner 动作门取值错误 —— 与 R3 三席定 major 的依据 (同字段相反取值 + 「推送授权」门错) 不同形 — 证据: `sed -n '4p;14p;46p;126p;179p'` 逐字; `git diff fdfb183 265a5f9 -- docs/handoff/…` hunk 仅触及 :4/:6/:12/:108/:113/:116/:136-137/:152/:179; R3 扫描器 `scratchpad/pr190/apply_r3_fixes_main.py:29` STALE 正则逐字 `未推|推送授权|待 owner merge|待 owner 一句|22/25|48/48|\b1457\b|\b1889\b|48 条 RED|1\.68\.0|fe32441|fad8b4b` (不含「待授权」「R1/R2」「R3/R4」) (type=issue) finding_id=82513c94
- [minor] implementation/aria/skills/state-scanner/scripts/linked_issue_field_probe.py: **同 quad 为 R3 carry `4a675f17` (决策单 C9), 本条为新增形态**: 作用域枚举 `changes.rglob("proposal.md")` (:85) 在 Python 3.11 下**跳过 dangling symlink** `openspec/changes/<slug>/proposal.md` 与 **symlink 指向的 slug 目录** ⇒ 该 slug 从作用域消失, 探针 `OK` —— 与 C9 (不可读目录) 同为 fail-open by omission, 但**前置条件可入 git** (symlink 是版本化对象, chmod 不是), 故比 C9 的「须手工 chmod」略强; 现实语料零实例、须刻意构造, 仍 minor; 修法与 C9 同一处 (`os.walk` / `scandir`+`lstat` 显式枚举, 不可读/悬空/symlink 目录记 UNREADABLE 违规), 建议 v1.68.2 候选一并改 — 证据: 核验记录 K15 `rc=0 'OK (1 份在范围内, 0 条在册)'` (z/proposal.md 为悬空 symlink, `os.walk` 可见而 `rglob` 不可见, 直调对比见记录); K15b symlink 目录 `zlink/` 含 NO_FIELD proposal 未列出 (`FAIL 1 项` 仅 y) (type=risk) finding_id=4a675f17
- [minor] documentation/.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md: R3 清账追记段三处记录失准: (i) C9 行只收 R3 cr `4a675f17`-(i) (rglob 吞 PermissionError), **漏 (ii)** 白名单 UTF-8 BOM 首条目不归一 (修 = `encoding="utf-8-sig"`, fail-closed 但输出含不可见字符), handoff `:137` carry 清单同漏 ⇒ v1.68.2 候选清单不完整; (ii) 「a3bfd693 ×3」行声称「扫描结果贴进 R3 聚合报告」「以后 handoff 二次编辑一律先跑**同一扫描**」, 但 R3 聚合报告 `:21`/`:28` 只有一句摘要 (无正则、无逐行输出), 扫描器只存在于 session scratchpad (`apply_r3_fixes_main.py:29-30`), 仓内无宿主 ⇒ 「同一扫描」不可复跑 (memory `no-code-host-no-assertion` / `pasted-evidence-is-derived`), 其正则覆盖不足即 finding 1 的直接成因; (iii) R3 聚合表 `:29` 把 C9 内容挂在 id `ae4f1c9f` 行而 `4a675f17` 整行缺席 (R3 cr 原报两条不同 quad), 与决策单 C9 引用 `4a675f17` 不一致 (R2 km `5da757d0` 点名过的同 scope 去重吞条缺陷再现)。三处均为记录精度, 不改任何机制/合并安全 — 证据: 决策单 `:118` `:120` 逐字; R3 cr `:39` (ii) BOM 原文; R3 聚合 `:21` `:28` `:29` 逐字; `grep -c utf-8-sig` 决策单/handoff = 0/0 (type=issue) finding_id=ebab7adc

## Verdict

**PASS** — Critical 0 / Major 0 / Minor 3 (quad 去重后 3; 其中 2 条与既有 quad 同 id 为新增形态, 1 条新 quad)。

理由: 三仓交付面在 265a5f9 / d1caa66 / ffed204 上逐字合规 (Phase 1 全项通过); 强制项 53 / 1462 / 1894 全绿; 41 例对抗实跑中六臂首行 / exit code 契约在全部非极端输入上保持, 真实语料 changes 9 = 3 OK + 6 NO_FIELD 且 6 份恰为在册; R3 处置三项 (a3bfd693 推送授权类 / C8 留记 / tasks.md 1894) 核验成立; 本轮新发现全部落在「记录精度」与「symlink 极端前置」, 无假绿于现实语料、无数据风险、无跨文档事实矛盾 (版本 16 点 / 测试计数 / gitlink / tag / 检查条数 在 PR body / handoff / tasks.md / proposal / CHANGELOG 间逐数一致)。

## 投票

**PASS** — 无「必须在合并前修」的 finding。建议 (不阻塞): 若主控在合并前再动一次主仓文档面, 顺手收 finding 1 的三行 (`:14` `:46` `:126`) 并把 STALE 正则补「待授权|R1/R2|R3/R4」; finding 2 与 (ii) BOM 并入决策单 C9 候选清单 (一句话); 不推子模块 (B9-补)。

## 核验记录

### 强制项 (BRIEF §纪律), 逐字

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
Ran 53 tests in 2.852s
OK                                                                  rc=0
$ cd aria/skills/state-scanner/tests && python3 run_tests.py | grep -E "^Ran |^OK|^FAILED"
Ran 1462 tests in 79.153s
OK
$ cd aria && bash skills/run_all_tests.sh | tail -3
skill 套件: 9 OK / 0 FAIL / 0 SKIP   (累计 1894 个测试)             exit=0
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt
OK (9 份在范围内, 6 条在册)                                          rc=0
$ sh -c '<state-checks.yaml 第 13 条 command 逐字: python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . \ --grandfathered .aria/linked-issue-field-grandfathered.txt>'
OK (9 份在范围内, 6 条在册)                                          rc=0  wall=0.11s (timeout 10s)
$ python3 …/linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | od -c
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4           rc=0 (13 字节, 无尾换行)
$ python3 …/linked_issue_field_probe.py --emit-arg openspec/changes/linked-issue-field-availability/proposal.md | od -c
0000000                                                               rc=0 (空; 哨兵 none)
$ python3 …/linked_issue_field_probe.py --emit-arg openspec/changes/sibling-spec-probe/proposal.md | od -c
0000000                                                               rc=0 (空; 哨兵 none)
$ find openspec/changes -name proposal.md | wc -l → 9 ; find openspec/archive -name proposal.md | wc -l → 140
```

环境: Python 3.11.2, uid 1000, HEAD 265a5f9; `git submodule status` aria d1caa66 (v1.68.1) / standards ffed204。收尾 `git status --short` 主仓仅 ` M aria-orchestrator` (会话起点即有), `git -C aria status --short` / `git -C standards status --short` 均空 ⇒ 三仓零写入; 全部夹具在 `scratchpad/pr190/r4cr/work/` (脚本 `scratchpad/pr190/r4cr/adv.py`)。

### R3 处置核验 (BRIEF 特别请核)

| R3 id | 声称 | 本席核验 | 判定 |
|---|---|---|---|
| `a3bfd693` (handoff 类级清账, 推送授权类) | footer `:178`→`:179` / §5 三行 / `:152` PR 行 / `:12` 全部对正; 机械扫描残余 0 | `git diff fdfb183 265a5f9` 逐 hunk: `:4` phase 加 R3 / `:12`「只剩推送授权」→「推送授权已于同日给出并执行」/ `:108` 24/25 + yaml 24/1 / `:113` Decision memos 加 R1–R3 / `:116` 架构文档 2.0.2 / `:136-137` C8 留记 + C9 / `:152` R1–R3 / `:179` footer 对正。本席自扫 (正则 `未推|待授权|待 owner 授权|推送授权|四处未推|ahead|1\.68\.0|fe32441|fad8b4b|22/25|22 done|1889|1457|R1/R2|R3/R4|只剩|待 PR|本地合并态|C\.2 推送`) 命中 22 行, 逐行判: `:9` `:11` 叙事箭头 (历史) / `:40-44` §1 时戳时间线 (历史) / `:56` H1 行标 ✅ 已完成「原文保留」(历史) / `:64` M2「待授权」指 #116 评论 (仍成立) / `:82` `:110` `:111` `:115` `:127` `:147` `:148` `:152` `:169` 当前态正确; **未对正**: `:14` `:126` (轮次落后一轮) / `:46` (括注「待授权后走」) — 见 finding 82513c94 | **推送授权类: 成立 (零残余)**; 轮次进度类: 残 3 行, 降 minor 重报 |
| C8 (`b66c5239` TASK-014 留记) | PR body + handoff 补记 | PR #190 body (GET 回读, head=265a5f9, mergeable=True) 含「**TASK-014 verification 留记**: … `git merge-tree` 复核 (决策单 C8)」; handoff `:136` 同文; 决策单 `:119` C8 行; 判据 `git -C aria branch -a \| grep -ci a1-entry` = 0 (90 个分支, 无 a1-entry) | **成立** |
| `62285020` (tasks.md 1894) | tasks.md `:5` 1889 → 1894 | tasks.md `:5` 逐字「run_all_tests **1894** (v1.68.1 后重跑)」; 本席独立重跑 `run_all_tests.sh` = 1894 (第三次独立复现); PR body「run_all_tests 9 套件 **1894**」一致 | **成立** |
| C9 (决策单新行) | `4a675f17`-(i) carry 入 v1.68.2 候选 | 决策单 `:120` 存在; handoff `:137` 首项同记; 但只收 (i), 漏 (ii) BOM — 见 finding ebab7adc | 成立, 记录不全 (minor) |

### carry (决策单 C6 / C7 / C9) 逐条确认「确属 minor、不影响合并」

| id | carry 描述 | 本席实跑 | 判定 |
|---|---|---|---|
| `d91f074e` (C6) | 新 check `plugin-version-arch-docs-match` 无专属测试 | `_parse_state_checks_yaml` 解析该条 7 键 enabled=True timeout=5 severity=warning (第 14 条); 三态已由 R1/R2 实测, 本席镜头外未重跑 | carry 不反证; minor |
| `ae4f1c9f` (C7) | archive 目录不可读 + 陈旧候选 ⇒ traceback | C7-a: archive chmod 000 + 在册 `gone` ⇒ `rc=1 stdout='' stderr 末行 PermissionError` (违反 SC-8(c) 首行前缀) | minor 成立 (前置 = chmod 000, git 不存目录权限) |
| `2ed89c8a` (C7, 候选最高优先) | `stdout.reconfigure` 覆盖 `--emit-arg`, 非 ASCII 实参被改写 | C7-b: `PYTHONIOENCODING=ascii` + `10CG/仓库#1` ⇒ stdout `b'10CG/??#1'` rc=0 (对照 utf-8 ⇒ `b'10CG/\xe4\xbb\x93\xe5\xba\x93#1'`) | minor 成立 (前置 = 非 ASCII repo slug × 非 UTF-8 stdout; CC Bash 为 UTF-8); 同意最高优先 (E6「探针自身失败 ⇒ 非 0」语义回退) |
| `4a675f17` (C9) | rglob 吞不可读 slug 目录 ⇒ fail-open by omission | K15 / K15b: symlink 两形态同类 (finding 2, 新形态); A-BOM 未重跑 (R3 已实证 fail-closed) | minor 成立; 新增形态同 quad |
| `a2a4165f` (C7) | UNREADABLE / 不可读 note / root+emit-arg 互斥 / `~~~`↔``` 围栏种类 未回写 proposal | proposal §4 六臂表 `:420-429` 仍只列四态; 「新表面」#3 `:600` 仍三条已知限 | minor 成立; carry (随 B3) |
| `9ac5533a` (B8) | hunk A 顺序条款措辞软化延后 | SKILL.md `:341` 仍「必须 … 逐行对齐」; 白名单头注 + state-checks fix 已含「位置不限」; 测试 `test_long_header_field_on_line_61_still_found` 钉位置无关 | 裁定站得住 (处方性改动须 Rule #6, 不在本循环) |

### 对抗性实跑 (CLI 30 例 K1–K30 + 纯函数 9 例 P1–P9 + C7 复现 2 例; 全部临时目录)

| 例 | 输入 | rc | stdout 首行 / 要点 | 判定 |
|---|---|---|---|---|
| K1 | `>\t**Linked Issue**:` (tab) | 1 | `FAIL 1 项` NO_FIELD | E0 谓词 1「恰一个 U+0020」成立 |
| K2 | 首条 markdown 链接形, 第二条 code span | 1 | `…:2 NO_TOKEN` | E0 谓词 3 首条胜 (不跳到第二条) |
| K3 | `  > ~~~` 引用内围栏 (2 空格) 含字段 | 1 | NO_FIELD | 谓词 2 `[ ]{0,3}(?:> ?)?` 成立 |
| K4 | 4 空格缩进字段行 | 1 | NO_FIELD | 行首锚定成立 |
| K5 | `10CG/a#1,,10CG/b#2` | 1 | `BAD_TOKEN 不可解析元素:  (无关联请写 \`none\`)` | E4 空元素 ⇒ E5 点名 `""` |
| K6 / K7 | `--emit-arg` 目录 / 不存在 | 2 / 2 | stdout 空, stderr 一行 | 契约 §2 emit-arg 失败分支 |
| K8 / K9 | root 是文件 / root 不存在 | 0 / 0 | `##SKIP## openspec/changes/ 不存在或 0 份 …` | 臂 1 |
| K10 | `--grandfathered` 指向目录 | 0 | `OK (1 份在范围内, 0 条在册)` + 末行 `(白名单文件缺失, 视为空集)` | 臂 5 (`is_file()` 判) |
| K11 / K12 / K13 | 条目反斜杠 / 绝对路径 / 裸 `openspec/changes/` | 1 / 1 / 1 | 陈旧 (b) / `FAIL 2 项` NO_FIELD + (b) / (b) | fail-closed |
| K14 | slug `a[x]` 已归档 `2026-01-01-a[x]/` | 1 | 陈旧 (b) | 精确后缀无 glob (R1 修复保持) |
| **K15** | `z/proposal.md` 为**悬空 symlink** (另有合规 y) | **0** | `OK (1 份在范围内, 0 条在册)` | **z 从作用域消失** (finding 4a675f17 新形态); 直调: `rglob`/`glob("**")` 均不含 z, `os.walk` 含 |
| **K15b** | `y/proposal.md` 为有效 symlink (指向无字段文件) + `zlink/` 为 symlink 目录 (含无字段 proposal) | 1 | `FAIL 1 项` 仅 y NO_FIELD | 文件 symlink 正常读 (fail-closed); **symlink 目录不递归 ⇒ 缺席** (同 finding) |
| K16 / K17 | 冒号后空 / 字段名尾空格 `Linked Issue **:` | 1 / 1 | NO_TOKEN / NO_FIELD | E2 / E0 字符级 |
| **K18** | `--emit-arg` `10CG/a#1, TBD` | 0 | stdout `b''` | E6 BAD_TOKEN 格整参省略 (有效首元素**不**泄出) |
| K19 | OK proposal 却在册 | 1 | 陈旧 (c) | 臂 4(c) |
| K20 | 同一 slug 三种写法 `x/` `./x` `  x  ` | 0 | `OK (1 份在范围内, 1 条在册)` | 归一 + 去重 (R1 修复保持) |
| K21 / K21b | 复制 scripts+lib 只删 `collision.py`, check / emit | 0 / 2 | `##SKIP## 归一 SOT 不可导入 (… 版本 < 1.68.0)` / stdout 空 stderr 一行 | 臂 2 / SC-5(d) 真实降级 |
| K22 / K22b | lib 缺 `is_sentinel` (模拟 < 1.68.0), check / emit | 0 / 2 | 同上 | 版本探针 (import 整体失败) 成立 |
| K23 | 字段在第 5000 行 | 0 | OK | 位置无关 (D2) |
| K24 | 全角反引号 `｀…｀` | 1 | NO_TOKEN | E2 U+0060 逐字节 |
| K25 | 2000 份 proposal | 0 | `OK (2000 份在范围内, 0 条在册)` wall 0.28s | timeout 10s 余量 35× |
| K26 | 相对 root `./k19/` (cwd = 临时目录) | 1 | 陈旧 (c) | 相对 root 以 cwd 解析后 resolve, 白名单以 root 解析 |
| K27 | `--emit-arg` chmod 000 文件 | 2 | stdout 空, stderr 一行 | 失败分支 |
| K28 | `none, 10CG/a#1` | 1 | `BAD_TOKEN 不可解析元素: none` | E5 哨兵判整串非元素 (哨兵不可与 token 混写) |
| K29 | ``` 开、`> ``` ` 闭 | 0 | OK | 状态机按任意匹配行翻转 (proposal 字面, 已知限族) |
| K30 | check 模式 `PYTHONIOENCODING=ascii` + 违规 | 1 | `FAIL 1 ?` / 细节 `????` | 首行前缀 `FAIL` 保持, 不崩 (R1 2ed89c8a 修复面) |

纯函数 P1–P9: `无` ⇒ OK emit 空 / `無` ⇒ BAD_TOKEN / `NoNe` ⇒ OK emit 空 / 冒号后无空格 ⇒ OK `x#1` / `关联 ISSUE` ⇒ OK (ASCII 折叠只作用 `Issue`) / `` ` `10CG/a#1` `` ⇒ token `" "` BAD_TOKEN `("",)` / CRLF + 尾注 ⇒ OK `10CG/a#1` / EOF 前未闭合 ``` 后字段 ⇒ NO_FIELD / `无 ` ⇒ BAD_TOKEN。`is_sentinel`: none/NONE/无 True; 無/`none `/N/A/空 False。全部与 §2 / E0–E6 字面一致。

### 真实语料 (只读) 与跨文档一致性

- changes 9 = 3 OK (a1-entry `10CG/Aria#174` / 本 Spec `none` / sibling-spec-probe `none`) + 6 NO_FIELD (= 白名单 6 条逐一); archive 140 (与 proposal §Why 观测表同数; 本席未重跑 archive 四态分布, R3 已实测 126/14/0)。
- 版本面: `plugin.json` / `marketplace.json` ×2 / aria README / aria VERSION = 1.68.1; 主仓 CLAUDE.md :139/:141 / VERSION:24 / README.md :8/:242 / i18n ×3 各 :3/:10/:244 / system-architecture.md :189 / version-scheme.md :23 = 1.68.1 (16 点); `1.67.2` 残留仅 system-architecture.md `:968` Version History 2.0.1 行 (历史记述, 正确)。
- 计数一致性: 新测试 53 (实跑) = tasks.md :5 = PR body = proposal Status; state-scanner 1462 (实跑) = 四处; run_all_tests 1894 (实跑) = tasks.md :5 = PR body; tasks.md `- [x]` 24 / `- [ ]` 1 (5.6) = yaml `status: done` 24 / `in_progress` 1 (`:635` TASK-025) = handoff :108 = PR body「24/25 done; 5.6 = 本 PR」; state-checks 14 条, 本条第 13 = PR body「第 13 条」。
- PR #190: head 265a5f9 = 被审 head, base master, open, mergeable=True, merged=False; body 含 v1.68.1 / d1caa66 / ffed204 / TASK-014 留记 / R1–R3 段 / R4 占位。
- **观察 (不计 finding)**: latest.md `:4` 指针 / `:13` track 行 / `:23` 更新 #2 均为 R2 时点口径 (「R1·R2 已清账, R3/R4 后合并」), R3 未触碰; 各段带日期属 dated 记述, 且字面仍真 (R1/R2 确已清账), 故不另立; latest.md `:9`「08-29 post_spec R5 … 6 项待 owner 裁定」段为本 PR 之前既有 (`git diff c423281 265a5f9` 未触及), 镜头外。
