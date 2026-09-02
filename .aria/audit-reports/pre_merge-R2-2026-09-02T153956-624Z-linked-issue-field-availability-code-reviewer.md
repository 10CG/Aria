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
verdict: PASS
timestamp: 2026-09-02T15:53:58.828Z
context: PR #190 linked-issue-field-availability (main 17ae85e / aria d1caa66 / standards ffed204)
agents: [code-reviewer]
---

# PR #190 pre_merge 收敛审计 — Round 2 — code-reviewer (fresh 席)

> 镜头: Phase 1 规范合规 (proposal §2/§3/§4/SC 表 + TASK-008/009/013/014/015 ↔ `lib/linked_issue_field.py` / `scripts/linked_issue_field_probe.py` / SKILL.md hunk A/B / 模板, 重点 R1 清账 PATCH 增量 `aria-patch-only.diff`) → Phase 2 代码质量 (27 例对抗性夹具实跑 + 新 state-check 四态实跑)。
> 结论口径: R1 已处置且核验成立的条目不列 finding (见 §核验记录); 下列 4 条 minor 中 3 条落在 R1 清账 PATCH **自己新写的路径**上 (memory `fix-recurs-in-fallback` 形状), 全部 fail-CLOSED 方向或极端边界, 无一须在合并前修。

## Phase 1 规范合规 — PASS

- 文件路径: 与 Spec Impact / yaml deliverables 一致 (lib 新建 / scripts 新建 / tests 新建 / spec-drafter SKILL.md 两 hunk / standards 模板 / `.aria/state-checks.yaml` 注册 / `.aria/linked-issue-field-grandfathered.txt`); PATCH 增量只触 probe + tests + 5 版本面文件, `git -C aria diff fe32441 d1caa66 --stat -- skills/spec-drafter/SKILL.md` 空 ⇒ B9「零 SKILL.md 指令面变更」成立。
- E0–E6: `lib/linked_issue_field.py` 未被 PATCH 触碰; `VERDICTS` 四态不变 (:58); E5 哨兵判定吃 E3 原串 (:149); E6 只在 OK 且非哨兵产值 (:103-105)。
- §4 六臂 ↔ 探针: 臂 1 (:85-88) / 臂 2 (:213-229, SKIP 文案含 `1.68.0`) / 臂 3 (:129-141, `fv.verdict != "OK"` 封闭枚举) / 臂 4 (:143-166, (a)(b)(c) 文案 `FAIL allowlist 陈旧: <path> (x)`) / 臂 5 (:92-99, 末行 note) / 臂 6 (:179)。TASK-008 输出格式 (:270) 首行 / 违规行 `<path>:<line|-> <VERDICT> <细节>` / 路径字典序 / 陈旧行在后 — 实跑一致 (核验记录 c2/c3/c10)。
- TASK-009: `--emit-arg` 读单文件 → `sys.stdout.write(emit_arg(fv))` (:189-197); 读失败 exit 2 (c13); 母 Spec 接缝 `--emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` ⇒ `10CG/Aria#174` 逐字节, 本 Spec ⇒ 空 (核验记录)。
- 新违规形态 `UNREADABLE` (:120-125) 与「verdict 封闭枚举」**不冲突**: 纯函数 `VERDICTS` 不变, 探针判定 `fv.verdict != "OK"` 仍是封闭枚举; `UNREADABLE` 是 CLI 层在读文件失败时写进 `<VERDICT>` 槽的第五个 token, 方向 fail-CLOSED (计入 `FAIL k 项`, exit 1), 不改既有六臂任何首行/exit code。**属 CLI 输出契约外扩而非设计冲突**, 但 SOT (proposal §4 六臂表 / TASK-008 verification :270) 未记 ⇒ finding `a2a4165f` (documentation minor)。全 `aria/skills` 下只有 lib + probe 自身提及 `NO_FIELD|BAD_TOKEN|UNREADABLE`, 无机器消费方解析该槽 (grep 实跑)。
- SKILL.md hunk A ↔ TASK-014: 新小节 `## proposal.md 头部字段要求` 落在 `## tasks.md 格式要求` 之前 (aria-R2.diff :131-147) ✓; A.1.4 一行指针 (:114) ✓; 写法三条 (code span / `, ` / `none` 不留空不删行, N/A TBD 非哨兵) ✓; 指向模板相对路径 + Spec §3 ✓; 不重复 Why/What/Tasks ✓。:351「读取侧另认中文 alias」与 proposal §4 fix 骨架 (:409-410) 同口径, 非 finding。
- SKILL.md hunk B ↔ TASK-015: Level 2 预览围栏 :140-143 四行顺序 Level → Status → Created → Linked Issue ✓, placeholder `{<org>/<repo>#<n>}` 非哨兵 ✓; Level 3 预览 (:167) 无头部 blockquote 行 ⇒ 条件分支不触发 ✓。
- 模板 (standards ffed204) ↔ TASK-013: `:6` canonical 行 ✓; Usage Notes 英文: `none` / do not leave empty / do not delete the line / `, ` / 引 Spec §3 ✓; `grep -n "alias\|关联\|无\b"` 零命中 ✓ (「不写中文 alias」字面对齐)。
- 范围: PATCH 新增 `UNREADABLE` 臂 (fail-CLOSED 外扩, 见上) + 主仓新 check `plugin-version-arch-docs-match` (R1 `ac44ace3` 类级兜底, anchor in_scope 含 check 注册) — 均有 R1 处置记录, 非无主 scope creep。

## 审计结论

- [minor] implementation/aria/skills/state-scanner/scripts/linked_issue_field_probe.py: PATCH 把 archive 陈旧判定从 `glob` 换成 `iterdir()` 后, archive 目录不可读时 `PermissionError` 未捕获 ⇒ traceback、stdout 空、exit 1 (违反 SC-8(c) 首行前缀契约); v1.68.0 的 pathlib glob 静默吞该异常判 (a)。R1 `ae4f1c9f` 修复自己的新路径重犯读错误未 fail-closed。修: `:154-156` 包 `try/except OSError` ⇒ 视为未归档 (a) 或输出 UNREADABLE 陈旧行 — 证据: `:154-156`; c17 实跑 `stdout='' rc=1 stderr 末行 PermissionError: [Errno 13] Permission denied: '.../openspec/archive'` (type=issue) finding_id=ae4f1c9f
- [minor] implementation/aria/skills/state-scanner/scripts/linked_issue_field_probe.py: `_normalize_entry` 只归一 `./` 前缀 + 尾 `/`, 残余形态 `openspec/changes/./a` `openspec/changes/b/.` 计入「m 条在册」且陈旧守卫经 `is_file()` 按 OS 路径语义放行, 但违规判定按字符串比较不豁免 ⇒ 该条目静默无效; `openspec//changes/c` (b) / `zz/../d` (a) 则被守卫抓到。全部 fail-CLOSED 且点名 proposal, 无假绿; 同 R1 类 (fix-the-class), 修: `posixpath.normpath` 一次收干净 — 证据: `:68-79`; c10 实跑 `FAIL 6 项` 四份 NO_FIELD + 陈旧 2 条 (`./a` `b/.` 无陈旧行) (type=risk) finding_id=4a675f17
- [minor] architecture/aria/skills/state-scanner/scripts/linked_issue_field_probe.py: `sys.stdout.reconfigure(errors="replace")` (:208-211) 对 `--emit-arg` 模式同样生效, 而该模式 stdout 是机器消费的 `--linked-issue` 实参: 非 ASCII token (`10CG/仓库#1`, E5 接受, `normalize_linked_issue` → `('仓库', 1)`) 在 `PYTHONIOENCODING=ascii` 下输出 `10CG/??#1` exit 0 — v1.68.0 同输入 `UnicodeEncodeError` exit 1 (= §3 E6「探针自身失败 ⇒ 非 0」)。R1 `2ed89c8a` 修复过度覆盖到机读面: 静默改写实参而非报错。修: 仅 check 模式 reconfigure, 或 emit 模式 `sys.stdout.buffer.write(v.encode("utf-8"))` — 证据: 核验记录「emit-arg ascii」od 输出 `1 0 C G / ? ? # 1` rc=0 vs fe32441 探针 rc=1 (type=risk) finding_id=2ed89c8a
- [minor] documentation/openspec/changes/linked-issue-field-availability/proposal.md: PATCH 三处 CLI 契约外扩未回写 SOT: (i) 违规行 `<VERDICT>` 槽新 token `UNREADABLE` (§4 六臂表 :420-429 / TASK-008 :270 只列四态); (ii) 末行 note 新变体 `(白名单文件不可读, 视为空集: <Exc>)` vs 钉死的 `(白名单文件缺失, 视为空集)` (:428 / TASK-008 :268); (iii) `root` 与 `--emit-arg` 互斥 exit 2 (TASK-009 :294 只写与 `--grandfathered` 互斥; probe docstring :30-31 同)。probe docstring :16-20 亦未提 UNREADABLE 臂。随 B3「下次触碰 proposal」同批 + docstring 两处同步 — 证据: `aria-patch-only.diff` :184-189/:162-166/:236-237; c5/c12/c8 实跑 (type=issue) finding_id=a2a4165f

## Verdict

**PASS** — Critical 0 / Major 0 / Minor 4。

理由: 四条全部 fail-CLOSED 方向或双重极端前置 (archive 目录无读权限 + 陈旧候选; 非 ASCII repo slug + ASCII stdout; 白名单写 `/./`), 无假绿、无数据风险、既有六臂首行/exit code 契约在全部 27 例对抗夹具上保持。清账 PATCH 对 R1 点名形态的修复全部成立 (见核验记录), 残余是同类未推广 + 修复过度覆盖, 属 carry 级。

## 投票

**PASS** — 无「必须在合并前修」的 finding。建议合并后以一个 aria PATCH 一并收 `ae4f1c9f` / `4a675f17` / `2ed89c8a` 三处 (各 1-3 行), SOT 回写随 B3 下次触碰 proposal 时同批。

## 核验记录

### 强制项 (BRIEF §纪律)

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
Ran 53 tests in 2.787s
OK
$ python3 run_tests.py | grep -E "^Ran |^OK|^FAILED"
Ran 1462 tests in 67.471s
OK
$ grep -c "^\s*def test_" *.py | awk -F: '{s+=$2} END {print s}'   → 1478
$ grep -c "^def test_" test_collision.py                            → 16     (1478 − 1462 = 16, R1 6cdc6077 口径注成立)
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt
OK (9 份在范围内, 6 条在册)      rc=0     (find openspec/changes -name proposal.md → 9 份, 白名单 6 条)
$ python3 .../linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | od -c
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4      rc=0   (无尾换行, 13 字节)
$ python3 .../linked_issue_field_probe.py --emit-arg openspec/changes/linked-issue-field-availability/proposal.md | od -c
0000000                                                           rc=0   (空; 哨兵 none)
```

环境: Python 3.11.2, uid 1000 (非 root, chmod 000 夹具有效), `/bin/sh -> dash`, HEAD 17ae85e; `git submodule status` aria d1caa66 (v1.68.1) / standards ffed204。

### R1 各条处置核验 (本席镜头内逐条; 镜头外三条只读记录)

| R1 id | 处置声称 | 本席核验 | 判定 |
|---|---|---|---|
| `e4cde200` (qa, SC-5(d) 夹具) | 复制完整 lib/ 只删 collision.py + 断言 ImportError 点名 lib.collision | diff :299-317 逐字读; `test_sc5_d_degraded_missing_collision_module_is_skip` 在 53 条中通过 | 已修 |
| `a3bfd693` (handoff frontmatter) | phase / updated-at 刷新; 已 merge origin/master | 文件 :4 phase 含「R1 0C/4M 已清账, R2 待」, :6 `updated-at: 2026-09-02T14:27:14Z`; `git log` 见 29c1e4f Merge origin/master | 已修 |
| `9ac5533a` (B8 裁定) | 位置无关是设计; 白名单头注 + fix 文案补位置说明; SKILL.md 软化 carry | 头注 :836-837 / state-checks fix :880-881 有「位置不限 … 建议紧随 Created」; proposal E0 三谓词 (:164-169) 确无行号约束, :176 明写否决「只扫前 N 行」; 可证伪证据 `tests/…:506 test_long_header_field_on_line_61_still_found` 实存; SKILL.md 自 fe32441 零改动 (carry 成立, 处方性改动须 Rule #6) | 裁定站得住 |
| `ac44ace3` (arch 两行 + 新 check) | 两行 → 1.68.1; CLAUDE.md 同步面; 新 check 三态 | `system-architecture.md:189` / `version-scheme.md:23` 均 v1.68.1; CLAUDE.md :81 列入两行 + check 名; 新 check 经 `_parse_state_checks_yaml` 解析 (14 条, keys 7 个与既有同形, enabled True, timeout 5) 并以 `/bin/sh -c` (custom_checks.py:345 `shell=True`) 实跑四态: 仓内 `OK plugin=1.68.1 (2 arch doc rows match)` rc=0; scratchpad 副本改一行 → `DRIFT plugin=1.68.1 vs system-architecture.md=1.67.2` rc=1; 删 version-scheme 行 → `MISSING version-scheme.md aria-plugin 行` rc=1; 删 plugin.json → `##SKIP## …不可读` rc=0。`-m1` 在两文档各只有一行候选 (grep -n 各 1 命中) | 已修 + 兜底成立 |
| `ae4f1c9f` (白名单归一 / archive 不 glob / root 互斥) | 三形态归一; 精确后缀; exit 2 | c1 `./openspec/changes/x/` → `OK (1 份在范围内, 1 条在册)`; c18 CRLF + 尾空白 → 同; c4 slug `x[1]` + archive `-x[1]` → (b), c4b archive `-x1` → (a) (glob 会误判 (b)); c8 root + `--emit-arg` → rc=2 stdout 空 | 点名形态已修; 残余见 finding ae4f1c9f (新路径回归) / 4a675f17 (同类未推广) |
| `2ed89c8a` (stdout 非 UTF-8) | reconfigure errors=replace | c7 ascii + FAIL → rc=1 首行 `FAIL 1 ?` (前缀保真); c7c ascii + SKIP → `##SKIP##` 前缀保真; c7b ascii + parser.error → rc=2 stderr backslashreplace 不崩 | check 模式已修; 对 `--emit-arg` 过度覆盖见 finding 2ed89c8a |
| `a0ff4897` (注释) | 去 CONTRACT 引用; is_sentinel 注释改真实用途 | `grep -n CONTRACT` probe / test / lib 零命中; :216 注释改为「版本探针」。注: 该理由是空真 (模块本身 1.68.0 新建, 缺符号的 lib 必缺整个模块, `extract_linked_issue_field` 那一项已足以让 import 失败), 但 TASK-008 :266 逐字 mandate 该 import, 无害, 不计 finding | 已修 |
| `4605dc4d` (模板英文化) | Usage Note 英文 + 删 alias | standards-R2.diff :17-20 逐字读; alias / 关联 / 无 零命中; SC-6 (iii) 测试接受 EN (diff :392-394) | 已修 |
| `6cdc6077` (Ran vs 静态) | 记入口径注 | 1462 vs 1478 差 16 = test_collision 裸函数 16 (上方计数) | 口径成立 |
| `46b1df1a` / `5333fe78` / `6ab01600` | 方法论留痕 / carry C1 / carry C2 | 镜头外 (AB 时序 / CI paths / coordination refs), 未独立核验, 按聚合报告记录 | 未核验 (非本席镜头) |
| B9 (PATCH 车道) | 零 SKILL.md 变更; 5 新测试对 v1.68.0 探针 4 红 1 绿 | SKILL.md diff 空 (上); 在 scratchpad 复制整个 state-scanner 并换回 `git show fe32441:…probe.py` 后跑同测试模块: `FAILED (failures=4, errors=1, skipped=2)` — 4 FAIL 全在 `TestSC5ProbeHardening` (normalization / ascii_stdout / root_emit_arg_exit2 / unreadable_proposal), `test_detail_lines_bad_token_and_no_token` 绿; 1 ERROR 是副本位置使 SC-7a 找不到 spec-drafter SKILL.md (副本伪影, 非声称范围); 2 skip = SC-6/SC-8 跨仓 | 声称成立 |

### 对抗性夹具 (27 例, 全部在 scratchpad 临时目录; 脚本 `scratchpad/pr190/r2cr/adv.py`)

| 例 | 输入 | rc | stdout 首行 / 要点 | 判定 |
|---|---|---|---|---|
| c1 | 白名单 `./openspec/changes/x/` | 0 | `OK (1 份在范围内, 1 条在册)` | 归一成立 |
| c2 | 白名单只有 `#` 与空行 | 1 | `FAIL 1 项` + NO_FIELD | fail-closed, m=0 |
| c3 | 条目指向 `…/x/proposal.md` (文件) | 1 | `FAIL 2 项`: x NO_FIELD + `陈旧: …/x/proposal.md (a)` | fail-closed, 坏条目被点名 |
| c4 / c4b | slug `x[1]`, archive `-x[1]` / `-x1` | 1 / 1 | `(b)` / `(a)` | 精确后缀, 元字符不改语义 |
| c5 | `proposal.md` 为目录 | 1 | `…/weird/proposal.md:- UNREADABLE IsADirectoryError (无法读取, 按违规计)`; stderr 无 Traceback | fail-closed |
| c5b | 同上且在册 | 1 | UNREADABLE + `陈旧: …/weird (a)` | fail-closed; 注: (a) 文案「不存在」对「存在但是目录」不准, 极端边界, 不计 |
| c6 | `--grandfathered` 指向目录 | 0 | `OK (1 份在范围内, 0 条在册)` + `(白名单文件缺失, 视为空集)` | 空集正确; 文案「缺失」对「是目录」略失准, 不计 |
| c7 / c7b / c7c | `PYTHONIOENCODING=ascii` × FAIL / root+emit-arg / SKIP | 1 / 2 / 0 | `FAIL 1 ?` / stderr `与…` / `##SKIP## …` | 前缀保真, 不崩 |
| c8 | root + `--emit-arg` | 2 | stdout 空; stderr `--emit-arg 与位置参数 root 互斥` | 成立 |
| c9 / c9b | 正文 latin-1 字节 / token 内 `\xff` | 0 / 0 | OK / OK (token `10CG/a�#1` 经 normalize → `('a�', 1)`) | errors=replace 为 TASK-009 逐字要求; 归一接受任意非空 basename 是 v1.67.0 既有语义, 非本 PR, 不计 |
| c9c | 白名单内 `\xff` | 1 | `陈旧: openspec/changes/x� (a)`; 第二条 `x` 正常豁免 | fail-closed |
| c10 | `./a` `b/.` `//c` `zz/../d` | 1 | `FAIL 6 项`: 四份 NO_FIELD + 陈旧 `openspec//changes/c (b)` + `zz/../d (a)`; `./a` `b/.` 无陈旧行 | finding 4a675f17 |
| c11 / c12 | proposal chmod 000 / 白名单 chmod 000 | 1 / 0 | `UNREADABLE PermissionError` / `(白名单文件不可读, 视为空集: PermissionError)` | fail-closed / 空集 |
| c13 | `--emit-arg` 指向目录 | 2 | stdout 空; stderr `[Errno 21] Is a directory` | 成立 |
| c14 | `proposal.md` 为断链 symlink | 0 | `##SKIP## …0 份` | pathlib rglob 对断链 `exists()` 假 ⇒ 不进作用域; v1.68.0 同; 极端边界, 不计 |
| c15 | `weird/proposal.md/proposal.md` | 1 | 目录 UNREADABLE; 内层文件 OK 不列 | 一致 |
| c16 | root 路径打错 | 0 | `##SKIP## openspec/changes/ 不存在…` | §4 臂 1 字面; v1.68.0 同 |
| c17 | archive 目录 chmod 000 + 陈旧候选 | 1 | **stdout 空**, stderr `PermissionError … openspec/archive` traceback | finding ae4f1c9f (PATCH 回归) |
| c18 | `openspec/changes/x  \r\n` | 0 | `OK (1 份在范围内, 1 条在册)` | 归一成立 |
| c19 | 绝对路径 / 反斜杠条目 | 1 | 两条 `(b)` | TASK-008 :269 字面 |
| c20 | `--grandfathered .aria/wl.txt` 相对 root | 0 | OK 1 在册 | 裁量 8 成立 |
| c21 | 同 slug 既在 changes/ 又在 archive/ | 0 | OK 1 在册 | 在册优先, 正确 |

`--emit-arg` × ascii stdout × 非 ASCII token (finding 2ed89c8a):

```
$ printf '> **Linked Issue**: `10CG/仓库#1`\n' > $S/na.md
$ PYTHONIOENCODING=ascii python3 scripts/linked_issue_field_probe.py --emit-arg $S/na.md | od -c
0000000   1   0   C   G   /   ?   ?   #   1        rc=0        (v1.68.1)
$ python3 scripts/linked_issue_field_probe.py --emit-arg $S/na.md | od -c
0000000   1   0   C   G   / 344 273 223 345 272 223   #   1    rc=0   (UTF-8 宿主, 正确)
$ PYTHONIOENCODING=ascii python3 <fe32441 探针副本> --emit-arg $S/na.md
rc=1  stdout 空  stderr 末行: UnicodeEncodeError: 'ascii' codec can't encode characters in position 5-6
$ python3 -c "normalize_linked_issue('10CG/仓库#1')"  → ('仓库', 1)   (E5 接受, verdict OK, emit_arg 非空)
```

披露: 为跑 fe32441 探针 (它以 `__file__` 定位 skill root), 本席曾把副本临时放到 `aria/skills/state-scanner/scripts/_r2cr_tmp_probe.py` 跑一次后立即删除; 之后改为整目录复制到 scratchpad 复跑 B9 声称。收尾 `git status --short` 主仓仅既有 ` M aria-orchestrator` (会话起点即有), `git -C aria status --short` / `git -C standards status --short` 均空 ⇒ 三仓零残余写入。

### 版本面 (PATCH 增量)

`aria-patch-only.diff`: plugin.json / marketplace.json ×2 / README / VERSION / CHANGELOG 均 1.68.1 (5 文件); 主仓 `grep -n "1\.68\.0" VERSION README*.md CLAUDE.md docs/architecture/{system-architecture,version-scheme}.md` 零命中, `1.68.1` 各文件 1–3 命中 (14 点)。
