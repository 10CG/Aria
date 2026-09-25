# Verification Ledger — `handoff-multibranch-subdir-path-fidelity`

> **Spec**: [proposal.md](./proposal.md) (v7) · [tasks.md](./tasks.md) (A.2 v6) · [detailed-tasks.yaml](./detailed-tasks.yaml) (A.3 v6)
> **Issue**: `10CG/Aria#195` (open, label `bug`)
> **本文件性质**: Phase B/C/D 全程的实测台账。每条记录 = 命令 + 原样输出 + 判定, 由命令重生成, 不手抄。
> **落点约定**: 本台账落仓内 (交付物)。`touchpoints-aria.txt` 与组 3 / TASK-026 的一次性副本落 scratchpad, **不落仓内** (TASK-001 verification 第 5 条: 落仓内会成为 TASK-031 有范围核验里一个本 cycle 产生却不在交付物清单上的未跟踪文件)。

---

## B.1 执行身份与授权

| 项 | 值 |
|---|---|
| 执行容器 | `simonfish/bfe8285d` (A.2 执笔为 `simonfish/023236f2`, 已 `yielded`; 本容器 2026-09-25 接手) |
| claim | `claims/bfe8285d/s-48ca@0612.yaml` — `track_id: handoff-multibranch-subdir-path-fidelity`, `phase: B`, `status: active`, `claimed_at: 2026-09-25T06:12:29Z`, `linked_issue: 10CG/Aria#195` |
| owner 授权 | 2026-09-25 owner 经 AskUserQuestion 裁「本容器接手, 走 B.1 → C.2」⇒ 构成 `metadata.owner_gates` 第 1 项同批授权 (规划提交推送 + B.0 `phase1_gate` 认领推协调 ref) |
| B.1 基线 | aria `1cb3872` · standards `940cb5b` · 主仓 `a52b5eb` (三处均 `ls-remote` 实测, 非跟踪 ref) |
| feature 分支 | 三仓同名 `feature/handoff-multibranch-subdir-path-fidelity` |

---

## TASK-001 — B.1 基线复核 (parent 1.3)

### 第 1 条 — 规划提交推送前置 (`owner_gates` 第 1 项)

规划提交本体 = 本地 master 上触及本 change 目录或本 Spec post_planning 报告的最新提交:

```
$ git log -1 --format='%H' -- openspec/changes/handoff-multibranch-subdir-path-fidelity/ '.aria/audit-reports/*handoff-multibranch*'
c839fc67146de81b1dd6469d1bbd14fa8229ae3a
# c839fc6 2026-09-16 13:26:22 +0000 docs(openspec): 10CG/Aria#195 A.2/A.3 v6 — post_planning 收口定点修 (owner 裁定接受当前结论)
```

逐 remote `ls-remote` + `merge-base --is-ancestor` 判定 (两 remote 均先 `git fetch`):

```
origin  master = a52b5eb7f26baaacafa7b7f0f04c5e958f798871   -> 规划提交 IS ancestor (已推送)
github  master = a52b5eb7f26baaacafa7b7f0f04c5e958f798871   -> 规划提交 IS ancestor (已推送)
```

**判定: 通过。** 规划提交已双推, 两端 master 同为 `a52b5eb`。

### 第 2 条 — 回落支

**不适用。** 第 1 条两端均判 ancestor ⇒ 主仓 feature 分支正常从 `origin/master` 起, 不走「从包含规划提交的本地 master 起」的回落支, 无需追加进 tasks.md AI 流程判断清单第 13 条的回落支。

### 第 3 条 — 三处 `origin/master` 实测

取值前对三仓各跑 `git fetch`, 再用 `ls-remote` 取值 (不读陈旧的远端跟踪 ref):

```
aria/origin/master       1cb387218935433312fde4067c276754b77686a8
standards/origin/master  940cb5b4b8672ea56606c4c3ed6157e84949fa4a
Aria/origin/master       a52b5eb7f26baaacafa7b7f0f04c5e958f798871

$ git ls-tree HEAD aria standards
160000 commit 1cb387218935433312fde4067c276754b77686a8	aria
160000 commit 940cb5b4b8672ea56606c4c3ed6157e84949fa4a	standards
```

**判定: 通过。** 两个 gitlink 与各自子模块的 `origin/master` 实测值相等 ⇒ 主仓已发布指针无孤儿风险。
**与 A.2 的差异**: aria `1cb3872` 与 `metadata.scope_repos` 记的 `head_at_a2` **相同**; standards 从 A.2 的 `8b49562` 前进到 `940cb5b` (他轨推进, 本 spec 的 standards 触点面见第 6 条附注)。

### 第 4 条 — B.0 `phase1_gate` 认领

获授权 (见上「B.1 执行身份与授权」), 照常跑, 未用 `--no-push` / `ARIA_COORDINATION_NO_PUSH=1`:

```
$ python3 <plugin>/skills/state-scanner/scripts/phase1_gate.py \
    --raw-track-id "handoff-multibranch-subdir-path-fidelity" --phase B --mode advisory \
    --repo-path /home/dev/Aria --linked-issue "10CG/Aria#195" --include-terminal
{
  "outcome": "passed",
  "proceed": true,
  "track_id": "handoff-multibranch-subdir-path-fidelity",
  "raw_input_id": "handoff-multibranch-subdir-path-fidelity",
  "error": null,
  "own_claim": {
    "track_id": "handoff-multibranch-subdir-path-fidelity",
    "owner": "simonfish", "container": "bfe8285d", "session": "s-48ca@0612",
    "phase": "B", "status": "active", "claimed_at": "2026-09-25T06:12:29Z"
  },
  "competing_winner": null,
  "surface": null,
  "push_success": true,
  "push_skipped": false,
  "push_skipped_reason": null,
  "linked_issue_overlap": [
    {
      "track_id": "handoff-multibranch-subdir-path-fidelity-bfe8285d",
      "owner": "aria-runner-bot", "container": "bfe8285d", "session": "s-e4b1@1447",
      "status": "abandoned", "linked_issue": "10CG/Aria#195",
      "claimed_at": "2026-09-06T14:47:15Z"
    }
  ],
  "unknown_schema_claims": 0,
  "label_migration": null
}
```

推后核验 (不信 push 回执, 逐 remote 独立取值):

```
local  refs/aria/coordination = 07c8091b8a723932f75bcccd451c4a2d6a38e67f
origin refs/aria/coordination = 07c8091b8a723932f75bcccd451c4a2d6a38e67f   -> MATCH
```

**判定: 通过。** `outcome=passed` / `proceed=true` / `push_success=true` / `surface=null` / `competing_winner=null`。
`linked_issue_overlap` 唯一命中项是本容器前任 claim (`…-bfe8285d`, `status=abandoned`, 2026-09-06 认领后于 09-09 被 TTL sweep), **不是竞争者** —— 与 tasks.md §范围边界所记的已知缺口形态一致 (CLI 每次调用新生成 session id, 走不到 self-resume), 但本次因前任已 `abandoned` 且 A.2 执笔容器的 claim 已 `yielded`, **未触发 `occupied` surface**。

### 第 5 条 — `touchpoints-aria.txt` 机械导出

导出脚本 `scratchpad/export_touchpoints.py` (SOT = proposal §触点文件清单 aria 表; 脚本内置四道核验: 行数 41 / 序号连续 1..41 / 类别计数 / 路径唯一):

```
$ python3 -B scratchpad/export_touchpoints.py scratchpad/touchpoints-aria.txt
OK 导出 41 行 → scratchpad/touchpoints-aria.txt
类别计数: 改写 12 / 改写待定 2 / 新增 1 / 引用 26
$ wc -l < scratchpad/touchpoints-aria.txt
41
```

**判定: 通过。** 41 行, 类别计数与 proposal §触点文件清单的机械计数 (改写 12 / 改写待定 2 / 新增 1 / 引用 26, 合计 41) 逐项相符。输出落 scratchpad, 未落仓内。

### 第 6 条 — 两份触点 diff

```
$ git -C aria diff --stat f314785 1cb3872 -- $(tr '\n' ' ' < scratchpad/touchpoints-aria.txt)
 .claude-plugin/marketplace.json                    |  4 +-
 .claude-plugin/plugin.json                         |  2 +-
 CHANGELOG.md                                       | 91 ++++++++++++++++++++++
 README.md                                          |  2 +-
 VERSION                                            |  9 ++-
 .../references/layer-l-integration.md              |  2 +
 .../state-scanner/references/phase-1-collectors.md |  2 +-
 .../references/state-snapshot-schema.md            |  7 +-
 8 files changed, 109 insertions(+), 10 deletions(-)

$ git -C aria diff --stat 1cb3872 1cb3872 -- $(tr '\n' ' ' < scratchpad/touchpoints-aria.txt)
(空)
```

**判定: 通过, 且偏移表无需更新。**

- 第二份为空, 因为 **B.1 基线 `1cb3872` 与 A.2 基线 `head_at_a2` 是同一个 SHA** ⇒ `metadata.baseline_rebase.shifts` 的四组偏移记录 (`state_snapshot_schema_md` / `layer_l_integration_md` / `phase_1_collectors_md` / `changelog_md`) 在 B.1 时点**完整继承**, 不需重测行号。
- 第一份与 `metadata.baseline_rebase.result` 记的「8 文件 / 109 增 / 10 删」**逐字吻合**, 文件清单亦逐项相同。
- **代码落点零 diff** (`handoff_multibranch.py` / `scan.py` / `latest_md_writer.py` / `handoff.py` / `_common.py` / 全部 tests 均未出现在 diff 里) ⇒ proposal 对实现面的全部 `文件:行号` 引用在 B.1 基线上有效。
- 出现 diff 的 8 个文件里, 5 个是版本派生面 (`marketplace.json` / `plugin.json` / `VERSION` / `README.md` / `CHANGELOG.md`, v1.73.0 → v1.73.3), 3 个是本 spec 的 references 改写面 —— 这 3 个的行号漂移已由 A.2 `shifts` 覆盖并逐处实读核验过。
- **standards 侧附注**: A.2 `head_at_a2` = `8b49562`, B.1 实测 `940cb5b`。本 spec 在 standards 的触点面仅 `conventions/session-handoff.md`, 其行号有效性在 Task 4.3 开工前复核 (本条不代劳, 避免把未实测的断言写进台账)。

### 第 7 条 — feature 分支建立与工作树断言

```
aria:       branch=feature/handoff-multibranch-subdir-path-fidelity  HEAD=1cb387218935433312fde4067c276754b77686a8  porcelain=0 行
standards:  branch=feature/handoff-multibranch-subdir-path-fidelity  HEAD=940cb5b4b8672ea56606c4c3ed6157e84949fa4a  porcelain=0 行
Aria (主仓): branch=feature/handoff-multibranch-subdir-path-fidelity  HEAD=a52b5eb7f26baaacafa7b7f0f04c5e958f798871  porcelain=0 行
```

**判定: 通过。** 三仓 HEAD 均等于各自 B.1 基线, 工作树全部干净。aria 已真实检出到基线 (不是只移动了远端跟踪 ref), 故第 8 / 第 10 条跑的是这份工作树。

### 第 8 条 — SC-11 验证脚本复跑

```
$ python3 -B openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py
(stdout: 27 行矩阵, 表头 + 26 个 state 行)
(stderr: verdict: OK (mismatch cells 0, stderr notes 0; 26 states x 19 predicates))
退出码 0
```

逐字节比对 (用 python 按行严格比 + SHA256, 未用 shell grep —— 本环境 shell 的 `grep` 是 ugrep 函数包装):

| 比对项 | yaml 侧字段 | 结果 |
|---|---|---|
| stdout 矩阵 | `sc11_predicate_validation.measured_2026_09_16_at_1cb3872_v6` | 27 行逐行逐字节 IDENTICAL, SHA256 均 `dc48ae0c7de198f8` |
| `--emit-json` `states` | `sc11_predicate_validation.states` | IDENTICAL, SHA256 `64136b0815c0d020` |
| `--emit-json` `expected` | `sc11_predicate_validation.expected` | IDENTICAL, SHA256 `3a7c0f55cf9ec2a0` |
| `--emit-json` `matrix` | 同上矩阵字段 | IDENTICAL, SHA256 `dc48ae0c7de198f8` |
| `--emit-json` `predicates` 的 `(label)` 开头行 | `sc11_baseline_predicates` 的同形行 | 19 条逐字节 IDENTICAL |

**判定: 通过。** 两份谓词原文 (yaml `sc11_baseline_predicates` 与脚本内嵌) 的唯一机械核验点闭合。

### 第 9 条 — 退出码口径

退出码 **0** ⇒ 逐格一致且无谓词写 stderr。口径表里 1 / 2 / 3 / 4 / 5 五个分支**均未触发**, 故无「重写模拟改动」「修脚本」「修调用」「查异常」「判差异格来源」任何后续处置, 亦无因放宽谓词而需附三态实跑的情形。

### 第 10 条 — 19 条谓词在 B.1 基线上全 FAIL

矩阵 `base` 行 (base = 原样不改, 即 B.1 基线的 `aria/skills/state-scanner` 工作树):

```
base                      FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL
```

**判定: 通过。** 19 条谓词 (a1 a2 b c1 c2 f1 f2 g i1 i2 j1 j2 j3 j4 j5 k l1 l2 l3) 在 B.1 基线上逐条 FAIL, 无一条输出 PASS ⇒ 判据全部保有鉴别力, 可进 TASK-003。

---

## TASK-002 — 前置核验 (parent 1.1)

### 命令 1 — `docs/handoff` 无子目录

```
$ find docs/handoff -mindepth 1 -type d
(无输出, 0 行)
```

python 独立核验: `os.listdir('docs/handoff')` 共 **209** 条目, 其中 `os.path.isdir` 为真的 **0** 个。
**判定: 通过** (A.2 实测亦为无输出; 条目数从 A.2 的 201 增至 209 系此后新增 handoff)。

### 命令 2 — 无非 ASCII 文件名

```
$ ls docs/handoff | LC_ALL=C grep -c -P "[^\x00-\x7F]"
0
(grep 退出码 1 = grep -c 计数为 0 时的正常退出码, 非命令失败)
```

**反事实 (证判据有鉴别力, 不是真空成立)**:

```
$ printf '<含非 ASCII 的文件名>.md\nascii-only.md\n' | LC_ALL=C grep -c -P "[^\x00-\x7F]"
1
```

python 独立核验: 209 个文件名中含码位 > 127 字符的 **0** 个。
**判定: 通过。** 三路一致 (照字面命令 0 / 反事实 1 / python 0)。
**附注**: 本环境 shell 的 `grep` 是 ugrep 函数包装, 已知会拒某些多字节与 `{m,n}` 形态; 本条的 `-P "[^\x00-\x7F]"` 经反事实实测**可用且有鉴别力**, 故照字面执行成立, 无需改写规范命令。

### 命令 3 — 全部 `origin` ref 的 handoff 树

```
$ git for-each-ref --format="%(refname)" refs/remotes/origin/
(14 个 ref: HEAD · aria/DEMO-001 · aria/DEMO-002 · chore/submodule-bump-234-auth-reversal ·
 feature/152-no-run-for-branch · feature/a1-entry-claim-duplicate-work-guard ·
 feature/agent-router-auto-project-agent-injection · feature/archive-gate-registration-class-and-skill-drift ·
 feature/linked-issue-field-availability · feature/linked-issue-normalization ·
 feature/owner-container-identity-key-and-collision-parser · feature/rule6-description-change-trigger-eval-lane ·
 fix/dec-20260712-002-file-and-renumber · master)

$ for r in $REFS; do git ls-tree -r --name-only "$r" -- docs/handoff; done | wc -l
2049          # 去重后 209
```

判定用 python (严格前缀剥离, 不用 shell 正则):

| 形态 | 判据 | 命中 |
|---|---|---|
| A 子目录 | 以 `docs/handoff/` 开头且剥前缀后仍含 `/` | **0** |
| B 转义路径 | 以双引号开头 (git 对特殊字符路径的转义形态) | **0** |
| 意外形态 | 既不以 `docs/handoff/` 开头也不以双引号开头 | **0** |

**反事实**: 构造 3 串 (`docs/handoff/archive/x.md` / 双引号包裹的转义名 / `docs/handoff/plain.md`) 喂同一判据 ⇒ 形态 A 命中 1、形态 B 命中 1 (各期望 1) ⇒ 两个判据均有鉴别力。

**判定: 通过。** A.2 由 R1 审计席实测 13 个 ref (子目录 0 / 带引号 0), 本次 14 个 ref (多一个此后新建的分支) 结论相同。
**附注**: 去重后 209 与命令 1 的当前工作树条目数相同 ⇒ 14 个 ref 的 handoff 树文件名集合与当前 master 一致, 无分支私有的 handoff 文件。

### 命令 4 — 两份冻结语料无子目录路径

```
aria/skills/state-scanner/tests/fixtures/handoff-tracks-frozen-2026-09-05.json
  文件行数 9976 · filename 字段 996 个 · 含 / 的 0 个 · raw 里 "rel_path" 出现 0 次
.aria/repro/handoff-tracks-frozen-2026-09-05.json
  文件行数 9968 · filename 字段 996 个 · 含 / 的 0 个 · raw 里 "rel_path" 出现 0 次
```

**反事实**: 构造 2 值 (`a/b.md` / `plain.md`) 喂同一判据 ⇒ 命中 1 (期望 1)。

**判定: 通过。** 两份语料各 996 个 `filename` 字段, 含 `/` 的 0 个 —— 与 A.2 实测 (各 996, 0 行) 相符。
`rel_path` 在两份语料里出现 0 次, 与「旧 collector 取 basename, 结构上不可能含 `/`」一致 ⇒ 本条**结构性成立**, 按 proposal Task 1.1 要求照记, 不当作行为性证据。

### 命令 5 — 台账写入

本节四条命令与原样输出均由命令重生成后写入, 未手抄。

---

## 变更记录

| 时间 (UTC) | 事件 |
|---|---|
| 2026-09-25 | 本台账建立。TASK-001 十条 verification 全部通过 (第 2 条不适用), TASK-002 五条全部通过。B.1 基线三处实测并建三仓 feature 分支。 |
