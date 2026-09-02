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
verdict: PASS
timestamp: 2026-09-02T13:31:14.891Z
context: PR #190 linked-issue-field-availability (main 0e9619c / aria fe32441 / standards fad8b4b)
agents: [code-reviewer]
---

# PR #190 pre_merge R1 — code-reviewer (两阶段: 规范合规 + 代码质量)

被审对象逐字读: BRIEF.md / proposal.md §2 :154-158, §3 :160-325, §4 :326-455, SC 表 :516-550 / detailed-tasks.yaml TASK-007/008/009/011/013/014/015 (+005/020/021/024/025) / CONTRACT §1-§3 / aria.diff 9 文件 / standards.diff / main-core.diff (.aria 两文件 + CLAUDE.md hunk) / 工作树 `aria/skills/state-scanner/lib/linked_issue_field.py` (158 行) / `scripts/linked_issue_field_probe.py` (196 行) / `tests/test_linked_issue_field.py` (1103 行)。

## 审计结论

- [minor] implementation/aria/skills/state-scanner/scripts/linked_issue_field_probe.py: 白名单条目归一不一致 — 陈旧守卫 `:118` 做 `rstrip("/")`, 但违规判定 `:98` 用原始条目做 `in entries`, 尾斜杠条目 `openspec/changes/foo/` 不豁免而被报 NO_FIELD (fail-closed 但误导); 重复条目使 `m 条在册` 双计且陈旧行重复打印; `:122` archive glob 未 escape slug 元字符 (`foo[X]` 命中 `…-fooX` 判 (b) 应为 (a)); `root` 位置参数与 `--emit-arg` 同给时静默忽略 root — 证据: 实跑 A/C/R/K (见核验记录), `FAIL 1 项 / openspec/changes/foo/proposal.md:- NO_FIELD` 于条目 `openspec/changes/foo/` 在册时; `OK (1 份在范围内, 2 条在册)` 于同条目写两遍 (type=issue) finding_id=ae4f1c9f
- [minor] implementation/aria/skills/state-scanner/scripts/linked_issue_field_probe.py: check 模式 `:84` `wl_path.read_text` 与 `:92` `p.read_text` 无异常守卫 (与 `--emit-arg` 模式 `:155-159` 的 OSError 守卫不对称); 作用域内某 proposal.md 或白名单不可读 ⇒ traceback, stdout 空, rc=1 ⇒ custom_checks 记 status=fail / output=`rc=1`, 首行不再满足 SC-8(c) 的 {OK, FAIL, ##SKIP##} 形状 — 证据: 实跑 M/N `PermissionError: [Errno 13] Permission denied: …/proposal.md` exit=1; `collectors/custom_checks.py:372-379` rc≠0 且 first_line 空 ⇒ `"output": f"rc={rc}"` (type=risk) finding_id=4a675f17
- [minor] architecture/aria/skills/state-scanner/scripts/linked_issue_field_probe.py: check 模式 stdout 含 CJK (`份在范围内` / `条在册` / `项` / `陈旧` / 细节文案, 由 proposal §4 :429 与 TASK-008 :270 钉死, 实现合规), 在 stdout 编码非 UTF-8 的宿主 (Windows 原生 Python 管道 cp125x 无 PYTHONUTF8 / 显式 legacy locale) 抛 UnicodeEncodeError ⇒ traceback, stdout 空; 这是本目录**首个**输出面含 CJK 的 plugin 分发探针 (同目录 `coordination_probe.py:8/:15` 的 CJK 只在 docstring); 一行 `sys.stdout.reconfigure(encoding="utf-8")` 或 `errors="replace"` 可在不改任何输出字面的前提下消除 — 证据: `PYTHONIOENCODING=latin-1 python3 … probe.py <root>` ⇒ `UnicodeEncodeError: 'latin-1' codec can't encode characters in position 6-10` exit=1; 同编码下 `--emit-arg` 输出 `10CG/a#1` exit=0 (纯 ASCII 面不受影响) (type=risk) finding_id=2ed89c8a
- [minor] testing/aria/skills/state-scanner/tests/test_linked_issue_field.py: check 模式 CLI 的 BAD_TOKEN / NO_TOKEN 细节行 (probe `:100-109`: `不可解析元素: <bad_elements> (无关联请写 \`none\`)` / `首个非空白不是反引号 (E2)`) 无任何 subprocess 级测试; TASK-008 verification :270 钉了这两段文案, proposal E5 :199 要求「在输出里点名那个元素」, 现有 SC-5 夹具只覆盖 NO_FIELD 违规 + 陈旧行; 库级 `bad_elements` 已测 (`:549-554`), 但 CLI 拼接面 (`", ".join(fv.bad_elements)`) 是零覆盖 — 证据: `grep -n '不可解析元素\|首个非空白不是反引号\|缺字段行' tests/test_linked_issue_field.py` 零命中; 手工实跑 V 确认输出正确 (`openspec/changes/bad/proposal.md:2 BAD_TOKEN 不可解析元素: [b](url) (无关联请写 \`none\`)`), 故为测试缺口非缺陷 (type=issue) finding_id=26934d03
- [minor] documentation/aria/skills/state-scanner/scripts/linked_issue_field_probe.py: (a) `:45` 注释与测试 `:76` 引 `CONTRACT-linked-issue-field.md §2 / :60` — 该文件只存在于本 session scratchpad, 三仓 `find -name 'CONTRACT-linked-issue-field*'` 零命中, 随 plugin 分发的代码把读者指向不可达文档; 应改引 proposal §4 :431-455 + detailed-tasks TASK-008; (b) `:173` `# noqa: F401 -- re-exported import surface, contract-pinned` 不真实: 该 import 位于 `main()` 函数体内 (`:170-175`), 不构成任何 re-export; 其真实作用是「旧版 lib 缺 `is_sentinel` 时 ImportError ⇒ ##SKIP##」的版本探针, 注释应如实写 — 证据: `grep -rn CONTRACT-linked-issue-field aria/ standards/ openspec/ docs/ .aria/` 仅命中上述两处引用行, 无定义文件 (type=issue) finding_id=a0ff4897
- [minor] documentation/standards/openspec/templates/proposal-minimal.md: TASK-013 verification :377 逐字「**不写**中文 alias (`关联 Issue` / `无`)」, 但模板 `:58` 含两个 alias 字面 (读取侧说明); `:57` 在英文句中嵌 `(不留空、不删行: …)`, 形状是为满足测试 `:903-904` `assertIn("不留空")/("不删行")` 而写 (该字面要求源于 TASK-005 :194 的 A.2 派生, proposal SC-6 :544 只要求「无关联时逐字写 \`none\`」); 跨项目英文 SOT 因此在 2 行带 CJK — 正是 D9 :498 点名的「本仓中文语料的结论写进全英文跨项目模板」形状 (温和形态: 语义仍只教 `none` + "always write the English canonical form", 故 minor) — 证据: `grep -n '[一-龥]' standards/openspec/templates/proposal-minimal.md` ⇒ `:57` / `:58` 两行 (type=issue) finding_id=4605dc4d

### Phase 1 规范合规 — 判定 PASS (逐条对照, 无阻塞)

| 检查点 | SOT | 实现锚点 | 结果 |
|---|---|---|---|
| E0 谓词 1 正则字面 + flags | TASK-007 :238 | `lib/linked_issue_field.py:62-64` `r"^> \*\*(?:Linked Issue\|关联 Issue)\*\*:"`, `re.IGNORECASE \| re.ASCII` | 逐字一致 |
| E0 谓词 2 围栏正则 | proposal :167 / TASK-007 :239 | `:69` `r"^[ ]{0,3}(?:> ?)?(?:```\|~~~)"`; `:121-123` 翻转且 `continue` (围栏行不参与谓词 1) | 一致 |
| E0 谓词 3 首条 + 1-based | proposal :169 | `:126-129` break; `hit_line_no = i + 1` | 一致 |
| E1 不 strip | proposal :178 | `:136` `rest = hit_line[m.end():]` | 一致 (`:120` 先 `rstrip("\r")`, CONTRACT §1.1 钉死 CRLF 容忍; 对 token 无影响, 实跑 O 验证) |
| E2 首个非空白 = 反引号 | proposal :180 | `:138-140` `lstrip(" \t")` 后 `rest2[0] != "\`"` ⇒ NO_TOKEN | 一致 |
| E3 未闭合 ⇒ NO_TOKEN; 原始串 | proposal :195 | `:142-145` `find("\`", 1) == -1` ⇒ NO_TOKEN; `rest2[1:end]` | 一致 |
| E4 split + strip | proposal :197 | `:147` | 一致 |
| E5 判 E3 原始串 | proposal :199 | `:149` `is_sentinel(token_str)` 在 E4 之后但吃 `token_str` 非元素 | 一致 (SC-4(f) 实测 BAD_TOKEN) |
| E6 四格 | proposal :211-220 | `:103-105` 仅 `OK and not is_sentinel` 返回 `token_elements[0]` | 一致 |
| is_sentinel 判据 | TASK-007 :249 建议式 | `:89-91` `== "无" or (isascii() and lower() == "none")` | 逐字一致 |
| 六臂 exit / 首行前缀 | proposal :420-429 | 作用域缺失 `:69-71` SKIP/0; import 失败 `:183-186` SKIP/0 (emit-arg 分支 `:177-182` stderr/2); FAIL `:139-142`/1; 陈旧 `:141`; 白名单缺失 `:147-148` 末行注; OK `:144-145`/0 | 六臂全到位, 首行前缀 ∈ {OK, FAIL, ##SKIP##} |
| 白名单缺省语义 | proposal :428 / SC-5 (e1)(e2) | `:75-82` 缺省或非文件 ⇒ 空集 + `missing_note`; 相对路径以 root 解析 `:79-80` | 一致 (裁量 8) |
| 陈旧守卫 a/b/c | TASK-008 :269 / CONTRACT §2 | `:114-131` 不以前缀起首 ⇒ b; 不存在 → archive `*-<slug>` ⇒ b 否则 a; OK ⇒ c | 一致 |
| 输出排序 | TASK-008 :270 | `:133-141` 违规按 rel 字典序在前, 陈旧按 e 字典序在后, 首行 `FAIL <k> 项` | 一致 |
| `--emit-arg` 无换行 / exit 2 / 互斥 | TASK-009 :292-294 | `:161` `sys.stdout.write`; `:155-159` OSError ⇒ stderr + 2; `:59-61` mutually_exclusive_group | 一致 (od -c 实跑无 `\n`) |
| 除 stdlib 外只一处 import; 不 import scripts/lib | TASK-008 :266 | `:40-42` argparse/sys/pathlib; `:171-175` 唯一非 stdlib import; 无 `scripts/lib` 引用 | 一致 |
| `<vNEXT>` 回填 | TASK-008 :266 | `:179` / `:184` `版本 < 1.68.0` | 一致 (plugin.json 1.68.0) |
| audit-engine 无 lib/ collectors/ | proposal :278 / TASK-008 :272 | `ls aria/skills/audit-engine/` ⇒ `references SKILL.md` | 一致 |
| collision.py / state-scanner SKILL.md / lib/__init__.py 零改动 | TASK-007 :244 | `git -C aria diff d69091d fe32441 --stat -- …` 空 | 一致 |
| TASK-013 模板 | :375-377 | standards.diff `:6` `> **Linked Issue**: \`{<org>/<repo>#<n>}\`` canonical; Usage Note `:55-58` | 一致 (alias 字面见 finding 4605dc4d) |
| TASK-014 hunk A | :400-402 | SKILL.md `:339-352` 独立小节, 落 `## tasks.md 格式要求` 之前; A.1.4 指针 `:113`; 不在旧 :127-162 | 一致 |
| TASK-015 hunk B | :420-422 | SKILL.md `:142-143` Created + Linked Issue placeholder, 顺序 Level→Status→Created→Linked Issue; Level 3 预览 `:169-182` 为框图无头部行, 无需对齐 | 一致 |
| TASK-011 注册 7 键 / 13 条 | :332-335 | main-core.diff state-checks.yaml +25 行, 键 = name/description/command/severity/fix/timeout_seconds/enabled; `grep -c '^  - name:'` = 13 | 一致 |
| 版本面 | TASK-021/024 | plugin.json / marketplace ×2 / VERSION / README / CHANGELOG 全 1.68.0; `grep -rn '1\.67\.2'` 于 14 点文件零命中; CLAUDE.md hunk 只改两处版本号 | 一致 |
| 范围控制 | in_scope | aria.diff 9 文件 / standards.diff 1 文件 / main-core.diff 与 TASK-025 :644 清单一一对应 | 无 scope creep |

一处**非阻塞偏差**记录: proposal §4 :433-443 的 import 骨架把 import 放模块顶层且只 import `normalize_linked_issue`; 实现在 `main()` 内 argparse 之后 import `lib.linked_issue_field` 三符号 — 这是 CONTRACT §2 :29-41 与 TASK-008 notes :275-276 明写的取代 (纯函数落版后探针不再直接 import 归一), 且 SKIP 文案仍点名归一 SOT。以 detailed-tasks 为准, 不算偏离。

### Phase 2 优点

1. E0–E6 字符级落地, 每条规则在源码有一行对应 (`:120-157`), 可与 proposal §3 逐行对读; E5 哨兵判定吃 E3 原始串 (`:149`) 而非 E4 元素, R6/QA M2 亲踩的坑被正确避开。
2. 探针 fail-CLOSED 是真的: `:98` 只放行字面 `"OK"`, `:104` else 分支注释点明是封闭枚举的最后一员; 六臂全部实跑可辨 (核验记录 §2)。
3. 跨 skill import 走 skill root 非 `lib/` (`:49-51`), 与 `coordination_probe.py` 的反向选择互不打架 — 全量 1457 测试同进程全绿 (核验记录 §1) 实证两个同名 `lib` 绑定不冲突。
4. 坏实现矩阵 `_ref_extract` (`tests:238-313`) 与被测模块零共享代码, 13 个 flaw 各钉一参数, 且 `_MATRIX_EXEMPT` 显式列出无区分力的 3 个正例夹具而非静默漏判。
5. SC-5(d) 降级夹具 (`tests:712-741`) 是真降级: 复制探针 + lib 到临时目录**不含** `collision.py` 实跑, 不是 mock。
6. 主仓侧: 白名单头注把格式 / 三子情形 / 「回填一份删一条」/ 「不改 aria/ 探针」写全; state-checks 条目零新键。

## Verdict

**PASS** — Critical 0 / Major 0 / Minor 6。

Phase 1 全部关键检查点通过 (上表 25 项); Phase 2 六条 minor 全部为 fail-closed 侧的健壮性 / 注释真实性 / 测试缺口 / 跨项目 SOT 语言卫生, 无一改变判定结果或产生假绿。

## 投票

**PASS**。无任何 finding 属「必须在合并前修」: 六条 minor 的最坏后果都是「探针在极端输入下崩成 rc=1 + 空 stdout」(仍是红, 非假绿) 或「注释 / 模板文案不够准」。建议 PR 合并后以 Level 1 (或并入 sibling-spec-probe 触碰同文件时) 一并处理: 白名单条目读入时统一 `rstrip("/")` + 去重; check 模式两处 `read_text` 加 OSError 守卫并输出 `FAIL <path> 不可读`; `sys.stdout.reconfigure(errors="replace")`; 补两条 CLI 细节行测试; 改写 `:45` / `:173` 注释; 模板去 CJK 并让测试断言英文短语。

## 核验记录

### 1. 测试 (BRIEF 必跑)

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
Ran 48 tests in 1.469s
OK

$ cd aria/skills/state-scanner/tests && python3 run_tests.py     # 全量, 同进程
Ran 1457 tests in 82.959s
OK

$ grep -rh '^\s*def test_' aria/skills/state-scanner/tests/*.py | wc -l      → 1473
$ grep -c '^\s*def test_' aria/skills/state-scanner/tests/test_linked_issue_field.py → 48
  (1473 - 48 = 1425 = CHANGELOG 声称基线; Ran 1457 = CHANGELOG 声称; 两数均复核相符)
```

### 2. 探针两条命令 (BRIEF 必跑) + 零改动断言

```
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt
OK (9 份在范围内, 6 条在册)
exit=0

$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | od -c
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4
0000015                                                   ← 13 字节, 无换行
exit=0

$ python3 … --emit-arg openspec/changes/linked-issue-field-availability/proposal.md | od -c
0000000                                                   ← 空 (哨兵 none)
exit=0

$ git -C aria diff d69091d fe32441 --stat -- skills/state-scanner/lib/collision.py skills/state-scanner/SKILL.md skills/state-scanner/lib/__init__.py
(空)
$ ls -d aria/skills/audit-engine/lib aria/skills/audit-engine/collectors
ls: cannot access 'aria/skills/audit-engine/lib': No such file or directory
ls: cannot access 'aria/skills/audit-engine/collectors': No such file or directory
$ grep -c '^  - name:' .aria/state-checks.yaml   → 13
$ python3 -c "import json;print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"  → 1.68.0
$ grep -n '"version"' aria/.claude-plugin/marketplace.json  → :3 1.68.0 / :16 1.68.0
$ grep -rn '1\.67\.2' VERSION README.md README.zh.md README.ja.md README.ko.md CLAUDE.md aria/.claude-plugin aria/README.md  → 零命中 (exit=1)
```

### 3. 对抗性坏输入 (全部在 scratchpad `cr-adv/` 临时目录, 仓内零写入)

```
A. 白名单尾斜杠 `openspec/changes/foo/` + foo 缺字段
   FAIL 1 项
   openspec/changes/foo/proposal.md:- NO_FIELD 缺字段行 (E0 三谓词无命中)          exit=1   ← 在册却被报 (finding ae4f1c9f)
B. 白名单 `./openspec/changes/foo`
   FAIL 2 项 / …NO_FIELD… / FAIL allowlist 陈旧: ./openspec/changes/foo (b)      exit=1   ← 按 TASK-008 :269 (b) 合规
C. 白名单同条目两遍 (foo 在册)          OK (1 份在范围内, 2 条在册)                 exit=0   ← 双计
   白名单 `gone` 两遍                    FAIL 3 项 / … / 陈旧: …gone (a) ×2         exit=1   ← 重复打印
D. --grandfathered 指向目录             OK (1 份在范围内, 0 条在册) / (白名单文件缺失, 视为空集)  exit=0  ← 优雅降级
E. root 与 slug 含空格                  OK (1 份在范围内, 0 条在册)                  exit=0
F. 空 proposal.md                        FAIL 1 项 / …:- NO_FIELD …                   exit=1
G. 仅未闭合围栏 + 字段行                 FAIL 1 项 / …:- NO_FIELD …                   exit=1   ← 围栏未闭合 ⇒ 后续全跳, 合规
H. 2MB 单行 + 字段行                     OK …   real 0m0.098s                          exit=0
I. token 内 \xff 字节 (errors=replace)   OK …; --emit-arg 输出 `10CG/a\xef\xbf\xbd#1`  exit=0   ← 按 TASK-009 errors=replace 钉死
J. 深层 openspec/changes/grp/foo + 同路径在册   OK (1 份在范围内, 1 条在册)          exit=0
K. `/nonexistent-root --emit-arg p.md`  stdout `10CG/a#1`                            exit=0   ← root 静默忽略 (finding ae4f1c9f)
L. --emit-arg 指向目录                   stderr `--emit-arg 读取失败: … Is a directory`  exit=2  ← 合规
M. proposal.md chmod 000                 PermissionError traceback, stdout 空          exit=1   ← finding 4a675f17
N. 白名单 chmod 000                      PermissionError traceback, stdout 空          exit=1   ← finding 4a675f17
O. CRLF 文件                             OK …; --emit-arg `10CG/a#1` 无 \r            exit=0
P. 白名单行内注释 `…foo  # why`          FAIL 2 项 (violation + 陈旧 (a))              exit=1   ← 格式只认行首 #, 已成文
Q. openspec/changes/proposal.md 直挂     FAIL 1 项 / openspec/changes/proposal.md:- NO_FIELD  exit=1
R. 白名单 slug `foo[X]`, archive 有 `…-fooX`   FAIL allowlist 陈旧: openspec/changes/foo[X] (b)  exit=1  ← 应为 (a) (finding ae4f1c9f)
S. root 是文件                           ##SKIP## openspec/changes/ 不存在或 0 份 proposal.md (作用域缺失)  exit=0
T. PYTHONIOENCODING=latin-1 check 模式   UnicodeEncodeError: 'latin-1' codec can't encode characters in position 6-10  exit=1  ← finding 2ed89c8a
U. PYTHONIOENCODING=latin-1 --emit-arg   `10CG/a#1`                                    exit=0
V. check 模式 BAD_TOKEN / NO_TOKEN 细节行 (手工, 测试零覆盖)
   openspec/changes/bad/proposal.md:2 BAD_TOKEN 不可解析元素: [b](url) (无关联请写 `none`)
   openspec/changes/notok/proposal.md:2 NO_TOKEN 首个非空白不是反引号 (E2)          exit=1   ← 文案与 TASK-008 :270 一致 (finding 26934d03 为测试缺口)
```

### 4. 真实语料围栏奇偶扫描 (E0 谓词 2 稳健性)

```
$ for f in openspec/changes/*/proposal.md; do python3 - "$f" <<'PY' … 计数 ^[ ]{0,3}(?:> ?)?(?:```|~~~) 命中, 奇数则打印 PY; done
(零输出 — 作用域内 9 份围栏计数全为偶数, 无未闭合围栏把真字段吞掉的情形)
```

### 5. 引用 / 文案真实性

```
$ grep -rn "CONTRACT-linked-issue-field" aria/ standards/ openspec/ docs/ .aria/
aria/skills/state-scanner/scripts/linked_issue_field_probe.py:45
aria/skills/state-scanner/tests/test_linked_issue_field.py:76
$ find /home/dev/Aria -name 'CONTRACT-linked-issue-field*'      → 零命中 (仅 scratchpad 有)
$ grep -n '[一-龥]' standards/openspec/templates/proposal-minimal.md  → :57 / :58
$ grep -n '[一-龥]' aria/skills/state-scanner/scripts/coordination_probe.py → :8 / :15 (均 docstring)
$ grep -n 'proposal-minimal' aria/skills/spec-drafter/SKILL.md → :341 / :448 均 ../../../standards/openspec/templates/proposal-minimal.md (test iv 解析通过)
$ awk '/### Level 3 预览/…' aria/skills/spec-drafter/SKILL.md → :169-182 框图预览, 无 `> **Level**` 等头部行
```

### 6. finding_id 计算

```
$ python3 -c 'import hashlib; …sha256("<category>:<scope>:<severity>:<type>")[:8]'
ae4f1c9f implementation:aria/skills/state-scanner/scripts/linked_issue_field_probe.py:minor:issue
4a675f17 implementation:aria/skills/state-scanner/scripts/linked_issue_field_probe.py:minor:risk
2ed89c8a architecture:aria/skills/state-scanner/scripts/linked_issue_field_probe.py:minor:risk
26934d03 testing:aria/skills/state-scanner/tests/test_linked_issue_field.py:minor:issue
a0ff4897 documentation:aria/skills/state-scanner/scripts/linked_issue_field_probe.py:minor:issue
4605dc4d documentation:standards/openspec/templates/proposal-minimal.md:minor:issue
```
