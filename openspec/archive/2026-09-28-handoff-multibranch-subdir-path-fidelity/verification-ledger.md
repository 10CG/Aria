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

## TASK-003 — 测试先行第一批: 枚举与读取族 (parent 1.2)

交付物 `aria/skills/state-scanner/tests/test_handoff_multibranch_path_fidelity.py` (新建, 7 个用例)。
用例名与 proposal SC 表「核验」列逐条对应, 无偏差。

### 实施前 recon (不照 spec 直接写 mock)

| 核实项 | 实测结论 |
|---|---|
| `collect_handoff_multibranch` 签名 | `(project_root, remote="origin", now=None) -> CollectorResult` |
| `r.data` 键集 | `exists` / `tracks` / `branches_scanned` / `legacy_count` / `collision` / `errors` —— **无 `unreadable_count`**, 故 SC-16 (b) 与 SC-18 (b) 的直接索引在基线上必 `KeyError` |
| soft_error 落点 | `CollectorResult.soft_error(kind, detail)` 追加 `{"error": kind, "detail": detail}` ⇒ kind 在 **`"error"` 键**下, 不是 `"kind"` 键 |
| `tracks.append` 构造点 | 实际 **3 处** (git show 失败支 / frontmatter 成功支 / 无 frontmatter fallback 支)。proposal Task 2.2 写「两个构造点」**不是代码级错**: Task 2.3 会删掉第一处 (git show 失败不再进 `tracks[]`), 改造后正好剩两处 |
| `_run` 复用面 | 本 collector 全部四个 git 调用 (`for-each-ref` / `ls-tree` / `show` / `log`) 的唯一出口, 单次导入四处复用 ⇒ SC-9 的假件必须按 `cmd` 第 2 个 token 分派 |
| 夹具范式 | `test_handoff_multibranch_collision_dedupe.py` 的 `_GIT_ENV` / `_git()` / `update-ref refs/remotes/origin/<branch>`, 不建真实 remote 不 clone |
| sys.path 顺序 | state-scanner 根在**前**, `scripts/` 在**后** (load-bearing: 反了会把 `lib` 绑到无 collision.py 的包, 使 collision 恒降级 none) |

### 按任务口径落地的实现选择

- **SC-3 配置隔离取处方 (D)**: 夹具 `_init_repo` 建仓后立刻 `git config core.quotePath true` (仓内 local)。测试 docstring 已写明该配置是判据的一部分, 并写明为何 env 路线够不到被测子进程 (`_GIT_ENV` 只传给夹具自己的 subprocess, 被测侧走 `_noninteractive_git_env` 继承 `os.environ`)。用例内另断 `git config --get core.quotePath == "true"`, 把夹具前提也钉成断言。
- **SC-8 后半按 `(branch, filename)` 取行**: helper `_rows_by(tracks, branch=, filename=)`, 并在其 docstring 写明为何不按 `rel_path` 取行 (否则 TASK-035 补丁 5 的首个失败断言会落在取行上, 而该补丁已无法再缩小)。
- **SC-9 假件按 flag 适配输出成帧**: 假件的 ls-tree 腿在 `cmd` 含 `-z` 时返回 NUL 分隔 (含 git 的尾随 NUL), 否则返回换行分隔。**理由**: 基线不传 `-z`, 若假件恒返回 NUL blob, 基线会因「解析不了成帧」而红, 红就不再归因于「缺前缀守卫」。此选择已写入假件 docstring。
- **SC-9 (c) 独立成用例**: `test_flat_enumeration_reports_no_prefix_violation` —— 它是**回归锁**, 在基线上应为绿, 与前四条断言的 RED 性质不同, 混在一个用例里会让基线结果无法分辨。

### RED 记录 (对 B.1 基线 aria `1cb3872` 实跑)

```
$ cd aria/skills/state-scanner/tests && python3 -B -m unittest test_handoff_multibranch_path_fidelity -v
Ran 7 tests — FAILED (failures=3, errors=3)
```

| 用例 | SC | 基线失败形态 | 首个失败断言 |
|---|---|---|---|
| `test_subdir_file_read_as_real_track` | SC-1 | `AssertionError: True is not false` | 子目录件被降级为 `legacy: True` |
| `test_non_ascii_filename_not_escaped` | SC-3 | `AssertionError: 0 != 1` | CJK 件根本不在 `tracks[]` (被 `.md` 过滤丢弃, **未**走到 git show 失败 —— 与 SC-3 所述机制一致) |
| `test_pointer_excluded_at_any_depth` | SC-8 | `KeyError: 'rel_path'` | 后半 (有鉴别力那半) 的 `rel_path` 断言 |
| `test_unexpected_prefix_soft_errors` | SC-9 | `AssertionError: 0 != 1` | `handoff_multibranch_unexpected_path_prefix` 计数为 0 |
| `test_flat_repo_rel_path_equals_filename` | SC-16 | `KeyError: 'rel_path'` | 全称谓词的第一行 |
| `test_undecodable_filename_skipped_with_signal` | SC-18 | `KeyError: 'unreadable_count'` | (b) —— 与 SC-18 所述「实体资格由 (b) 独撑, (a)(c) 在基线上碰巧为绿」完全吻合 |

**失败形态合规性 (TASK-003 verification 第 9 条)**: 六条红全部是 `AssertionError` 或 SC 明示的直接索引 `KeyError`, **无一条** `ImportError` / 夹具建仓失败 / 环境红。

### 回归锁在基线上为绿的记录

```
$ python3 -B aria/skills/state-scanner/tests/run_tests.py
Ran 1612 tests in 276.695s
FAILED (failures=3, errors=3)
```

- **1612 = A.2 实测基线 1605 + 本批新增 7** ⇒ 新文件被 runner 正常收集。
- 全部 6 条 FAIL/ERROR **逐条归属 `test_handoff_multibranch_path_fidelity`**, 属其它文件的为 **0** ⇒ 既有 1605 个测试**零回归**。
- 本批自带的回归锁 `test_flat_enumeration_reports_no_prefix_violation` (SC-9 (c)) 在基线上**为绿**, 符合预期: 基线无前缀守卫, 该 kind 计数本就为 0, 该用例的作用是防实现把 `-z` 的尾随空段送进守卫。

---

## TASK-004 — 测试先行第二批: 失败 / 日期 / legacy 族 (parent 1.2)

同一文件追加 4 个用例, 用例名与 proposal SC 表「核验」列逐条对应。

### 实施前 recon

| 核实项 | 实测结论 |
|---|---|
| fail-soft 早退 dict 键集 | `exists` / `tracks` / `branches_scanned` / `legacy_count` / `collision` / `errors` —— 六键, **无 `unreadable_count`** ⇒ SC-14 的直接索引在基线上必 `KeyError` |
| `handoff_multibranch_branch_list_failed` kind 字面 | 存在 (collector `_list_origin_branches` 返回错误时的 `r.soft_error`), 非 spec 凭空假设 |

### 夹具扩展 (SC-4 / SC-13 的前提)

新增 `_commit(tmp, msg, *, date=None)` 与 `_publish_ref(tmp)`, 原 `_publish` 改为两者的组合 (第一批用例行为不变, 实跑形态已复核未漂移)。`date` 同时设 `GIT_AUTHOR_DATE` 与 `GIT_COMMITTER_DATE`。**这是判据的一部分**: `%aI` 是秒级, 同一测试内先后两次 commit 若不钉日期会拿到同一秒的同一值, 而 `_GIT_ENV` 钉身份**不钉日期** —— 与 proposal SC-4 / SC-13 点名的前提一致, helper docstring 已写明。

### RED 记录 (对 B.1 基线实跑)

| 用例 | SC | 基线失败形态 | 首个失败断言 |
|---|---|---|---|
| `test_moved_file_dates` | SC-4 | `AssertionError: ... got ''` | Case 2 (从未在顶层存在的件) `updated_at` 为空串 |
| `test_legacy_track_id_uses_rel_path` | SC-13 | `AssertionError: Items in the second set but not the first` | (a) 两个 track_id 集合不等 (基线两行同 id) |
| `test_unreadable_not_downgraded_to_legacy` | SC-5 | `AssertionError: Lists differ: [{'track_id': 'legacy:master:unreadable.md…}] != []` | 读不到的件被伪造成 legacy 行进了 `tracks[]` |
| `test_unreadable_count_present_on_failsoft_early_return` | SC-14 | `KeyError: 'unreadable_count'` | 早退 dict 缺键 |

**一条对 proposal 事实断言的独立验证**: SC-4 的 Case 1 (记录性断言, 期望 `updated_at` 为移动日 `2026-08-15`) 在 B.1 基线上**通过** —— 证实 proposal 所记「旧 basename 路径与新相对路径的 `git log -1 --format=%aI` 都返回 mv 日」属实 (机制: `git mv` 的提交同时触及旧路径的删除与新路径的新增, `git log -- <旧路径>` 因此命中该提交)。⇒ 该半确为无鉴别力的记录性断言, 其「让后来人当场看见 `--follow` 救不了」的用途成立。

**按任务口径未写的断言**: SC-13 的「dedupe 不折叠」**未**写成断言 (TASK-004 verification 第 3 条)。已在用例 docstring 记明理由: `status == "legacy"` 的行在分组前就被 `continue` 透传, 两条同 id 的 legacy 行今天也不会折叠 ⇒ 该断言恒绿。

### 回归锁

```
$ python3 -B aria/skills/state-scanner/tests/run_tests.py
Ran 1616 tests in 249.381s
FAILED (failures=6, errors=4)
```

1616 = 基线 1605 + 两批 11; 10 条 FAIL/ERROR **全数归属** `test_handoff_multibranch_path_fidelity`, 属其它文件 **0** ⇒ 既有 1605 零回归。第一批的六条 RED 形态与 TASK-003 记录逐条一致, 未因夹具重构漂移。

---

## TASK-005 — 测试先行第三批: 跨文件与判定面 (parent 1.2)

追加 5 个用例 + 1 个冻结 fixture。交付物两件: 测试文件 · `aria/skills/state-scanner/tests/fixtures/handoff-multibranch-flat-baseline-2026-09-25.json`。

### 实施前 recon

| 核实项 | 实测结论 |
|---|---|
| `scan.py::_same_branch_head_unreachable_tracks` 签名 | `(project_root, git_data, tracks_data, enforced_remotes, timeout=5)`; 四道前置逐条实读确认 (非空 `current_branch` / `detached_head` 假 / `tracks` 是 list / `enforced_remotes` 非空), 任一不满足即返回两个空列表 |
| 拼串点与上报点的分离 | 探测命令 `["git","log","-1","--format=%H", f"{remote}/{branch}", "--", f"docs/handoff/{filename}"]` 是待改的拼串点; `inconclusive.append({"filename": str(filename), …})` 是须**逐字节不变**的上报点 —— 两值同源一 track, 正是本 spec 要钉的分离 |
| `freeze_corpus.FIELDS` | 八字段 `(track_id, owner_container, status, phase, updated_at, filename, branch, legacy)`, **不含 `rel_path`** ⇒ 比对必须走投影, 整字典比对在 A′ 下恒红 |
| dedupe 分组键 | `(track_id, identity_key(owner, container))`, 且 `status == "legacy"` 的行在分组**之前**被 `continue` 透传 ⇒ 手搓排序键用例的行必须**非 legacy**, 否则根本不进分组 |
| `_dedupe_sort_key` 现状 | 返回 4 元 `(parse_ok, updated_at, filename, branch)` ⇒ 同 basename 异目录的两行四级全并列, 赢家回退 `max()` 的迭代顺序 |

### 冻结 fixture 的可复现性

夹具 = 单 `master` 分支 hermetic 临时仓, 固定两件、逐 commit 钉日期:

| 文件 | frontmatter | commit 日期 | 投影后 `updated_at` |
|---|---|---|---|
| `2026-09-01-alpha.md` | 有 | `2026-09-01T10:00:00+00:00` | `2026-09-01T00:00:00Z` (取自 frontmatter) |
| `2026-09-02-beta.md` | 无 | `2026-09-02T10:00:00+00:00` | `2026-09-02T10:00:00+00:00` (取自 `git log -1 --format=%aI`) |

两行的 `updated_at` 都落在钉死值上 ⇒ 第二次运行必然相等, 不会产生「不可复现的红」(SC-2 点名的失败模式: 若夹具含无 frontmatter 件而不钉日期, 其 `updated_at` = 建仓时刻, 冻结 JSON 与复跑必不等, 而恒红的下场是实施者顺手削断言)。
夹具建造函数 `build_flat_baseline_repo` 写在测试模块内并被生成脚本 import ⇒ 「冻结的形状」与「测试重建的形状」结构上不可能漂移。
`freeze_corpus` 按路径 importlib 载入, `FIELDS` 不重抄字面; 测试另断 `frozen["fields"] == fc.FIELDS`, 使 schema 变动当场可见。

### RED 记录 (对 B.1 基线实跑)

| 用例 | SC | 基线结果 | 首个失败断言 / 绿的理由 |
|---|---|---|---|
| `test_scan_ancestry_consumer_uses_relative_path` | SC-6 | **红** `AssertionError` | 探测命令实得 `['docs/handoff/2026-05-09-session-end.md', 'docs/handoff/2026-05-09-session-end.md']` —— 两个 remote 都用 basename 拼串, 真实路径从未被查询 |
| `test_subdir_track_opens_cross_owner_collision` | SC-17 | **红** `AssertionError: 1 != 0` | `legacy_count` 为 1 (归档件被降级), 故 collidable 过滤后只剩一个容器, `kind` 停在 `none` |
| `test_dedupe_fifth_level_prefers_toplevel_rel_path` | 排序键第 5 级 | **红** `AssertionError: 'archive/x.md' != 'x.md'` | 4 级键下两行全并列, 反序输入换赢家 |
| `test_flat_repo_matches_frozen_baseline_projection` | SC-2 | **绿** | 回归锁: 基线生成、基线比对, 相等即预期 |
| `test_dedupe_tiebreak_prefers_lexicographic_max_path` | SC-7 | **绿** | characterization test, 记录 dedupe 对假想输入的现状, 非本 spec 的行为改动 |

**TASK-005 verification 第 7 条的红绿预言全部命中** (SC-6 (a)(b) / SC-17 / 排序键红; SC-6 (c) / SC-2 / SC-7 绿)。其中排序键那条**独立复现**了 R1 审计席在 `1cb3872` 上的实测结论 (4 级键下反序输入换赢家), 非沿用其转述。
SC-6 (c) 的性质按 proposal 归类为**回归锁**: 它在基线上必绿 (基线的 `inconclusive[0]["filename"]` 同样是 basename), 鉴别力全部来自反事实 —— 实施者若把拼串处的局部变量整体重指 `rel_path`, 该值会变成 `archive/…` 而红。用例 docstring 已写明「不得因它在基线上不红而当假绿删掉, 锁的对象是不许变」。

### 回归锁

```
$ python3 -B aria/skills/state-scanner/tests/run_tests.py
Ran 1621 tests in 179.365s
FAILED (failures=9, errors=4)
```

1621 = 基线 1605 + 三批 16; 13 条 FAIL/ERROR **全数归属**本新文件, 属其它文件 **0** ⇒ 既有 1605 零回归。

---

## TASK-006 — 测试先行第四批: SC-15 writer 往返六布局 (parent 1.2)

追加 6 个用例, 一布局一用例。

### 实施前 recon

| 核实项 | 实测结论 |
|---|---|
| `write_latest_md` 签名 | `(snapshot, output_path, now=None) -> dict`, 读 `snapshot["tracks_multibranch"]["tracks"]` |
| `action` 分支判定 | `n_active == 0` → `skipped` · `== 1` → `pointer` · `>= 2` → `banner`; 返回 dict **无** `degraded_reason` 键 ⇒ 五条直接索引在基线上必 `KeyError` |
| 真指针字面 | `**Latest**: [{filename}](./{filename})` —— 布局 2 的 (d) 按此写「无守卫时写出的是不含目录段的 basename 链接」 |
| 现有降级文案 | `**Latest**: (pointer 不可用) — track=… @ …` (只覆盖无 filename 一种原因, 未区分子目录) |
| `_active_track` 工厂 | `test_p1_layer_h.py` 的八字段工厂**恒带** `filename`、**从不带** `rel_path` ⇒ 正是布局 3 需要的老快照形状; 布局 6 的缺键 dict 由它 `del` 出来 |
| `handoff_pointer_target_missing` | kind 字面存在于 `collectors/handoff.py` |
| `collect_handoff` 签名 | `(project_root) -> CollectorResult`; 其 `data` 无 `errors` 键 ⇒ SC-15 的 kind 断言一律落 `CollectorResult.errors` |

### RED 记录 (对 B.1 基线实跑)

| 用例 | 布局 | 基线失败形态 |
|---|---|---|
| `test_pointer_roundtrip_toplevel` | 1 | `KeyError: 'degraded_reason'` — (i) |
| `test_pointer_roundtrip_subdir_guarded` | 2 | `AssertionError: '子目录' not found in '# Aria Handoff — (no active tracks)…'` — (d) 后半 |
| `test_pointer_written_when_rel_path_key_absent` | 3 | `KeyError: 'degraded_reason'` — (j) |
| `test_degraded_reason_present_when_no_active_track` | 4 | `KeyError: 'degraded_reason'` |
| `test_degraded_reason_present_on_multi_track_banner` | 5 | `KeyError: 'degraded_reason'` |
| `test_degraded_reason_missing_filename_when_filename_absent` | 6 | `KeyError: 'degraded_reason'` |

**TASK-006 verification 第 5 条的红绿预言全部命中。**

**一条对 proposal baseline-failing 资格判定的独立实证**: 布局 2 的失败输出把基线实际写出的整页文本带了出来 —— `# Aria Handoff — (no active tracks)` + `0 active tracks 当前`。这证实 proposal R3 `120e1171` 的重定是对的: 基线上归档件被降级 legacy ⇒ `n_active == 0` ⇒ writer 走 `skipped` 支写零 track 占位页 ⇒ **(d) 前半「不含真指针」在基线上照样成立、无鉴别力**, 只有后半「文案含具体原因」是 baseline-failing 实体。本轮未沿用该转述, 是由实跑输出直接取到的。

### 夹具组成按判据照写, 未取最小夹具

布局 2 除 `archive/` 那份 active 外, 顶层另留一份 `status: done` 的 `.md`。**这是判据的一部分**: 按字面取最小夹具 (归档-only) 时 `handoff.py` 的 `canonical_files` 为空 ⇒ `collect_handoff` 提前返回 ⇒ `handoff_pointer_target_missing` 结构上不可能产生 ⇒ 断言 (e) 恒绿且其反事实为假。用例 docstring 已写明这一点。

### 回归锁

```
$ python3 -B aria/skills/state-scanner/tests/run_tests.py
Ran 1627 tests in 177.948s
FAILED (failures=10, errors=9)
```

1627 = 基线 1605 + 四批 22; 19 条 FAIL/ERROR **全数归属**本新文件, 属其它文件 **0** ⇒ 既有 1605 零回归。

---

## TASK-007 — RED 台账 (parent 1.2, 四批的汇总层)

### 基线与命令

基线 SHA: aria **`1cb3872`** (= B.1 基线, 三仓 feature 分支已检出, 工作树干净)。

```
$ cd aria/skills/state-scanner/tests && python3 -B -m unittest test_handoff_multibranch_path_fidelity -v
Ran 22 tests in 1.218s
FAILED (failures=10, errors=9)
```

原样输出由命令重生成, 未手改。下方两条记录的异常类型与断言文本均由 traceback 机械提取。

### ⚠️ 本记录的性质限定 (TASK-007 verification 第 3 条, post_planning R2 PP2-M9)

**下面的 RED 记录只作 RED 证据, 不得标注为任何 proposal 反事实的实跑。** 基线是全部组件**同时**回退的状态, 一个用例的首个失败断言取决于书写顺序, 因此它证明不了反事实所指那条断言自身的鉴别力。SC-1 / SC-3 / SC-4 后半 / SC-5 / SC-8 后半 / SC-14 / SC-17 的反事实由 **TASK-035** 按三步法实跑, 本任务不代劳。

### 记录 1 — 五族 (SC-1 / SC-3 / SC-5 / SC-13 / SC-17)

| SC | 用例 | 异常类型 | 失败断言文本 (traceback 原样) |
|---|---|---|---|
| SC-1 | `test_subdir_file_read_as_real_track` | `AssertionError` | `True is not false : must be a first-class track, not a legacy stub` |
| SC-3 | `test_non_ascii_filename_not_escaped` | `AssertionError` | `0 != 1 : the CJK-named file must be collected` |
| SC-5 | `test_unreadable_not_downgraded_to_legacy` | `AssertionError` | `Lists differ: [{'track_id': 'legacy:master:unreadable.md…rue}] != []` |
| SC-13 | `test_legacy_track_id_uses_rel_path` | `AssertionError` | `Items in the second set but not the first:` (两 track_id 集合不等) |
| SC-17 | `test_subdir_track_opens_cross_owner_collision` | `AssertionError` | `1 != 0 : both handoffs must be read as first-class tracks` |

### 记录 2 — 其余 baseline-failing 实体 (14 条)

| SC / 项 | 用例 | 异常类型 | 失败断言文本 |
|---|---|---|---|
| SC-4 后半 | `test_moved_file_dates` | `AssertionError` | `False is not true : a file that never existed at the top level must still get its own real commit date, got ''` |
| SC-6 (a) | `test_scan_ancestry_consumer_uses_relative_path` | `AssertionError` | `'docs/handoff/archive/2026-05-09-session-end.md' not found in ['docs/handoff/2026-05-09-session-end.md', 'docs/handoff/2026-05-09-session-end.md']` |
| SC-8 后半 | `test_pointer_excluded_at_any_depth` | `KeyError` | `'rel_path'` |
| SC-9 | `test_unexpected_prefix_soft_errors` | `AssertionError` | `0 != 1 : exactly one prefix violation must be reported` |
| SC-14 | `test_unreadable_count_present_on_failsoft_early_return` | `KeyError` | `'unreadable_count'` |
| SC-16 | `test_flat_repo_rel_path_equals_filename` | `KeyError` | `'rel_path'` |
| SC-18 (b) | `test_undecodable_filename_skipped_with_signal` | `KeyError` | `'unreadable_count'` |
| SC-15 (d) 后半 | `test_pointer_roundtrip_subdir_guarded` | `AssertionError` | `'子目录' not found in '# Aria Handoff — (no active tracks)\n\n_state-scanner: 0 active tracks 当前 (scanned @ …)。_…'` |
| SC-15 (i) | `test_pointer_roundtrip_toplevel` | `KeyError` | `'degraded_reason'` |
| SC-15 (j) | `test_pointer_written_when_rel_path_key_absent` | `KeyError` | `'degraded_reason'` |
| SC-15 布局 4 | `test_degraded_reason_present_when_no_active_track` | `KeyError` | `'degraded_reason'` |
| SC-15 布局 5 | `test_degraded_reason_present_on_multi_track_banner` | `KeyError` | `'degraded_reason'` |
| SC-15 布局 6 | `test_degraded_reason_missing_filename_when_filename_absent` | `KeyError` | `'degraded_reason'` |
| 排序键第 5 级 | `test_dedupe_fifth_level_prefers_toplevel_rel_path` | `AssertionError` | `'archive/x.md' != 'x.md'` |

**记录 1 + 记录 2 = 19 条, 与本次实跑的 19 条 FAIL/ERROR 逐条对应, 无遗漏无多余。** 全部形态为 `AssertionError` 或 SC 明示的直接索引 `KeyError`, **无一条**环境红 (ImportError / 夹具建仓失败)。

### 记录 3 — 回归锁在基线上为绿

判定方法: 用 traceback 给出的**首个失败行号**与各断言的源码行号逐条比对, 只有行号**严格小于**首失败行的断言才算「本次实测执行过且通过」。

**实测执行过且通过 (真绿)**:

| 回归锁 | 所在用例 | 断言行 | 首失败行 |
|---|---|---|---|
| SC-2 (整条) | `test_flat_repo_matches_frozen_baseline_projection` | 用例整体 PASS | — |
| SC-7 (整条) | `test_dedupe_tiebreak_prefers_lexicographic_max_path` | 用例整体 PASS | — |
| SC-9 (c) | `test_flat_enumeration_reports_no_prefix_violation` | 用例整体 PASS | — |
| SC-4 前半 | `test_moved_file_dates` | 514 / 515 | 522 |
| SC-8 前半 | `test_pointer_excluded_at_any_depth` | 247 | 252 |
| SC-18 (a) | `test_undecodable_filename_skipped_with_signal` | 311 / 313 / 315 | 317 |
| SC-15 布局 1 (a)(b)(c) | `test_pointer_roundtrip_toplevel` | 969 / 973 / 974 / 975 | 976 |
| SC-15 布局 3 (g) | `test_pointer_written_when_rel_path_key_absent` | 1040 | 1042 |
| SC-15 布局 2 (d) 前半 | `test_pointer_roundtrip_subdir_guarded` | 1008 / 1010 | 1013 |

### ⚠️ 四条断言在 RED 批次结构上不可观测 (TASK-007 verification 第 4 条的缺口, 请 owner 复议)

TASK-007 verification 第 4 条把 **SC-6 (c)** 与 **SC-18 (c)** 与 **SC-15 布局 2 (e)** 列进「在基线上为绿」的回归锁记录, 记录 2 又要求 **SC-15 布局 2 的 (h)** 逐条红。**但这四条在本批次结构上无法观测** —— 它们与同一用例里排在前面的 baseline-failing 断言共处一个测试函数, 而首个失败即中止该函数:

| 断言 | 所在用例 | 断言行 | 首失败行 | 状态 |
|---|---|---|---|---|
| SC-6 (c) `inconclusive[0]["filename"]` 仍为 basename | `test_scan_ancestry_consumer_uses_relative_path` | 761 / 763 | **748** (SC-6 (a)) | 未执行到 |
| SC-18 (c) kind 存在性 | `test_undecodable_filename_skipped_with_signal` | 320 / 321 | **317** (SC-18 (b)) | 未执行到 |
| SC-15 布局 2 (e) 无 `handoff_pointer_target_missing` | `test_pointer_roundtrip_subdir_guarded` | 1015 | **1013** ((d) 后半) | 未执行到 |
| SC-15 布局 2 (h) `degraded_reason == "target_in_subdir"` | 同上 | 1017 | **1013** ((d) 后半) | 未执行到 |

**故本台账不声称这四条「实测为绿 / 实测为红」** —— 未执行到不是正证据, 写成实测即是假记录。

**这是 A.2/A.3 计划的一个结构性限制, 不是实施偏差**: verification 第 1 条钉死了用例名与用例数 (一布局一用例), 而同一用例内只可能有一个首失败点 ⇒ 「(d) 后半与 (h) 同时逐条红」在单用例内**不可兼得**。前四条已按 Rule #10 记入本节请 owner 复议, **未自行拆用例**(拆会改变 verification 第 1 条钉的用例名与数量)。

### owner 裁定 (2026-09-25): 取路径 A — 推给三步法反事实

**归属订正 (我给选项时的描述有误)**: 选项原文写的是「推给 TASK-035」, 核实后**那三条 SC 的反事实不归 TASK-035**:

| 断言 | 反事实归属 | 依据 |
|---|---|---|
| SC-6 (c) | **TASK-015** | 其 title 即「SC-6 GREEN + 两条反事实 (三步法)」 |
| SC-18 (c) | **TASK-018** | 其 title 含「SC-18 两条」 |
| SC-15 布局 2 的 (e) 与 (h) | **TASK-018** | 其 title 含「SC-15 四条」 |

TASK-035 只覆盖 SC-1 / SC-3 / SC-4 后半 / SC-5 / SC-8 后半 / SC-14 / SC-17, 其六个补丁**没有一个对应这四条**。owner 裁定的实质是「走三步法反事实那条路」, 故落地到上表的正确任务, 不硬塞进 TASK-035 (塞进去会与 TASK-015 / TASK-018 重复并让该任务越界)。

### 可观测性实测 (探查副本自 `9625999`, 已 `worktree remove`; **不作任务证据**, 仅为给 TASK-015 / TASK-018 写准确执行要求)

| 断言 | 能否单独观测 | 实测依据 |
|---|---|---|
| SC-6 (c) | **能, 无需额外动作** | TASK-015 反事实 2 (「把 `scan.py` 的局部变量整体重指 `rel_path`」) 下 (a) 仍绿 (拼串仍用 `rel_path`) ⇒ (c) 天然成为首失败 |
| SC-18 (c) | **能, 需定向补丁** | 实测形态「跳过但不报 kind」(删 `error_messages.append` 与 `r.soft_error` 两行, 只留 `continue`) ⇒ 首失败落 (c): `AssertionError: 'handoff_multibranch_undecodable_path' not found in []`; (a)(b) 绿。该形态正是 proposal 说 (a)(c) 要防的「跳过写成静默漏扫」 |
| SC-15 布局 2 (h) | **能, 需定向补丁** | 实测形态「renderer 正文不动, `return …, reason` 改为写死 `"missing_filename"`」⇒ 首失败落 (h): `AssertionError: 'missing_filename' != 'target_in_subdir'`; (d) 前半 / (d) 后半 / (e) 全绿。该形态正是反事实 4 要防的「机读面与正文面各算一遍」, 只是针对布局 2 |
| SC-15 布局 2 (e) | **不能 — 与 (d) 前半结构互斥** | (e) 要红必须让 `handoff.py` 解析出 pointer, 而 `_LATEST_POINTER_RE` = `^\*\*Latest\*\*:\s*\[[^\]]+\]\(\.?/?([^)]+?)\)` **要求行首** `**Latest**: [`; 而 (d) 前半恰恰断言该串**不出现在文本任何位置** ⇒ 两者不可同时满足。实测一个「降级页追加 `> _目标: [rel](./rel)_`」的形态: 用例**全绿** (该行不匹配正则, 故 pointer 未被解析, target_missing 不触发) |

**TASK-018 反事实 (1)(2) 下的实测**: 去掉守卫后布局 2 的首失败落在 (d) 前半第一条 (`AssertionError: '**Latest**: [' unexpectedly found in …`), 输出把基线写出的整页带出 —— 含 `**Latest**: [2026-08-20-x.md](./2026-08-20-x.md)`, **无目录段**, 顺带实证了 proposal R3 `7d909571` 对该机制的订正。(e) 与 (h) 在该补丁下均未执行到。

**(e) 的诚实处置 (不声称实测)**: 记录它在 TASK-018 反事实 (1)(2) 下**未执行到**。其鉴别力由同补丁下 (d) 的红**间接支撑**, 并可由一条已逐环节实读确认的机制链推出: 无守卫 ⇒ 写出行首 `**Latest**: [archive/x.md](./archive/x.md)` ⇒ `_parse_latest_pointer` 命中正则并**取 basename** (`Path(target).name`) ⇒ 在**非递归**的顶层候选集 (`by_name`) 里查不到 ⇒ 落 `handoff_pointer_target_missing` 分支。三个环节 (正则要求行首 / basename 归一 / 候选集非递归) 均已实读代码确认。要把它变成可观测只有拆用例一条路, owner 已否决该路径。

### 交给 TASK-015 / TASK-018 的执行要求

TASK-018 verification 第 2 条已立纪律: 「实跑红绿模式与此不符时**改补丁、不改测试断言**, 偏离与原样输出记台账」。上表两个定向补丁形态即按该纪律**预先实测**取得, 执行时可直接采用 —— 但仍须走完整三步法 (未打补丁绿 / 打补丁后红 / 副本 HEAD SHA + 补丁 diff) 并留三段输出, 本节的探查跑**不能**代替。

---

## 组 2 实现 (TASK-009 ~ TASK-014) + TASK-033 收口

**RED → GREEN 达成**: 组 1 的 19 条基线红**全部转绿**, 既有 1605 **零回归**。

```
$ python3 -B aria/skills/state-scanner/tests/run_tests.py
Ran 1627 tests in 242.900s
OK                                    ← EXIT 0, 零 FAIL 零 ERROR
$ cd aria/skills/state-scanner/tests && python3 -B -m unittest test_handoff_multibranch_path_fidelity
Ran 22 tests in 0.942s
OK
```

### 既有套件计数逐个持平 (与 A.2 基线一致)

| 套件 | A.2 基线 | 本次 | 出处 |
|---|---|---|---|
| `test_p1_layer_h` | 24 | **24 OK** | TASK-013 verification 第 6 条 |
| `test_handoff_multibranch_collision_dedupe` | 23 | **23 OK** | TASK-014 verification 第 3 条 |
| `test_track_board_advisories` | 5 | **5 OK** | TASK-016 verification |
| `test_scan_integration` | 19 | **19 OK** | TASK-010 verification 第 4 条 |
| pytest 腿 `tests/test_collision.py` | 28 passed | **28 passed** | `metadata.test_runner` (b) |
| pytest 腿 `phase-d-closer/tests/` | 11 passed | **11 passed** | 同上 |

### 逐任务落地要点

- **TASK-009** 枚举层: `-z` + NUL 切分 + 丢尾随空段 · 返回相对路径 · 前缀剥离从 `_HANDOFF_TREE_PATH` 派生且**先判后切** · 新增带默认值的 reporter 入参 (签名仍 2-tuple, 四处既有 mock 不受影响) · 主循环传双通道闭包 · `.md` 过滤与 pointer 排除作用于 `rel` 的 basename · docstring 删旧句加契约句。**顺带订正一处自相矛盾**: `_HANDOFF_TREE_PATH` 的注释原写「trailing slash required by git ls-tree」而值无斜杠, 已改。
- **TASK-010** 调用方与身份: 两个构造点写 `rel_path` · 读取与取日期均传 `rel` · `filename` 仍 basename · legacy id 改 `legacy:<branch>:<rel_path>` 且三处格式声明同批改 · `scan.py` 另取 `rel_path` 只用于拼串、`filename` 留给上报、早退**无 `or filename` 兜底** · `HEALTHY_TRACKS` 补键。
- **TASK-011/012** unreadable 会计: 读不到只报 kind + 计数, **不再追加伪 legacy 行** · 不可解码名判据写 `chr(0xFFFD) in rel` (未用 `encode`+`except UnicodeError` —— 上游已替换, 那种写法是死代码) · 前缀守卫丢弃的行不计入 · 删去已无消费者的 `fallback_date` 调用 · 正常路径与早退 dict 均恒含该键。
- **TASK-013** 写侧守卫: 判据 `rel = track.get("rel_path") or track.get("filename")`, **无 `"/" in filename` 嗅探** · 两 renderer 返回 `(content, reason)` · `write_latest_md` 分派前初始化、仅单 track 支解包覆写、**自身不重算** · 降级正文写明子目录原因 · 那句逐字重复的规则句**两处同批**补顶层限定 · 契约面五处一并改。
- **TASK-014** 排序键第 5 级 `(rel_path == filename, rel_path)`: 前四级不动, 缺键回落 `filename` 读作顶层不抛异常。

### SC-11 谓词状态

组 2 范围内的五条已为真: **(c1)(c2)(i1)(k)(l1)**（逐条机械跑过）。余下谓词按计划归组 4 的 TASK-019 / TASK-020 / TASK-021 / TASK-023。

**矩阵脚本 `sc11-predicate-validation.py` 在组 2 落地后报 `anchor drift` (退出码 3), 属设计内不属缺陷**: 它的模拟改动以基线源码逐字锚定 (`count=1` 的锚点须恰出现一次), 而 TASK-014 改掉了其中一个锚点所在的 `return` 行。计划把该脚本的唯一机械核验点定在 **TASK-001 (基线)**, GREEN 阶段的 SC-11 由组 4 逐条谓词承担 —— 故本阶段**不重跑矩阵脚本、不重写其锚点**。

### 本阶段两处自查发现

1. **SC-9 (d) 的判据对象写错, 已单独提交修正 (`3c0407c`)**: 原断言要求 `data["errors"]` 的消息串含 kind 字面量, 但本仓既有四个 kind 的双通道形态是**同一条 msg 进两个通道**且 msg 从不嵌 kind 名; proposal SC-9 (d) 原文是「含该 kind **语义**的消息串」。改为断言消息串含那条违规路径 —— 两种写法都能抓单通道实现 (那时 `data["errors"]` 为空), 新写法更贴合立意与既有约定, **不是削弱**。属组 1 文件, 故与组 2 收口**分开提交**以守住 TASK-033 第 1 条的「只 add 四个路径」。
2. **`hard_constraints` 第 10 条违规 11 处, 已修**: 本 cycle 新写的源码注释里 issue 引用写成了仓名与 `#` 之间带空格、缺 org 段的形态, 而非 `<org>/<repo>#<n>`。四个源码文件共 11 处全部改为 `10CG/Aria#195`, 改后复扫新增行裸引用 **0**。
3. **一处既有希腊字母, 未改**: `scan.py` 含一个 U+0394 (大写 Delta 字形, 此处只写码位以免本台账自身成为含禁用字形的文件)。经 diff 核实**不在本 cycle 新增行内**, 基线 `1cb3872` 即已存在 1 次, 且语境是数学差值 (注释原文为 `negative <U+0394> = healthiest signal`, 码位替写) 而非标签/编号 ⇒ 不在 `hard_constraints` 第 10 条「本 cycle 新写或改动的文字」范围, 未动。此处记录以免后续扫描误判为本轮引入。

### TASK-033 收口

| 核验项 | 结果 |
|---|---|
| 只 add 组 2 四个路径 | `handoff_multibranch.py` · `scan.py` · `latest_md_writer.py` · `test_scan_integration.py` |
| 提交后不带路径的 `git -C aria status --porcelain` | **空** (无组 2 之外改动混入) |
| 组 2 收口 SHA | **`9625999c734119aba56185edd2b258f215d3da57`** |
| 该 SHA 上新测试文件 | `Ran 22 tests … OK` |
| 提交前 aria 工作树无组 4 文档改动 | 成立 (组 4 未开工) |

**该 SHA 是组 3 反事实一次性副本的检出源** (TASK-015..018 与 TASK-035 一律 `git -C aria worktree add <scratchpad 路径> 9625999`)。

---

### 1.2 收口小结

| 批 | 用例数 | 基线红 | 基线绿 (独立用例) |
|---|---|---|---|
| TASK-003 第一批 (SC-1 / 3 / 8 / 9 / 16 / 18) | 7 | 6 | 1 (SC-9 (c)) |
| TASK-004 第二批 (SC-4 / 5 / 13 / 14) | 4 | 4 | 0 |
| TASK-005 第三批 (SC-6 / 17 / 2 / 7 + 排序键) | 5 | 3 | 2 (SC-2 / SC-7) |
| TASK-006 第四批 (SC-15 六布局) | 6 | 6 | 0 |
| **合计** | **22** | **19** | **3** |

- 四批的 verification 红绿**预言逐条命中**, 无一处需要改判。
- 既有 1605 个测试在四批之后仍**零回归** (全套 `Ran 1627 tests`, 19 条 FAIL/ERROR 全数归属本新文件)。
- 交付物三件: 测试文件 · 冻结 fixture (`hard_constraints` 第 5 条**禁止重生成**) · 本台账。
- **下一步 = 组 2 实现 (TASK-009 起; TASK-008 前置门 `status: done` 已解除)**, 按 RED → GREEN 推进; 组 2 收口提交见 tasks.md 2.7 / TASK-033。

---

## 组 3 反事实 (TASK-015 / TASK-016 / TASK-017)

三步法一律按 `hard_constraints` 第 9 条: 副本自 TASK-033 SHA `9625999` 检出 → 未打补丁绿 → 只回退该组件后红 → 记副本 HEAD SHA 与补丁 diff (以副本路径为根) → 复位 → `worktree remove`。**每任务一个独立副本**, 不复用 (TASK-035 verification 第 5 条: 复用会与对方的复位动作互相覆盖)。全部用 `python3 -B` 跑, 未在 feature 分支工作树上改动。

### 副本生命周期

| 任务 | 副本路径 (scratchpad) | 副本 HEAD | 移除后 `worktree list` |
|---|---|---|---|
| TASK-015 | `wt-task015` | `9625999` | 不含本任务副本 |
| TASK-016 | `wt-task016` | `9625999` | 不含本任务副本 |
| TASK-017 | `wt-task017` | `9625999` | 不含本任务副本 |

三次移除后真仓均核验 `porcelain` 0 行、`HEAD` 仍 `9625999` (补丁未泄漏到 feature 分支)。

### TASK-015 — SC-6 GREEN + 两条反事实

未打补丁: `test_scan_ancestry_consumer_uses_relative_path` **OK** (命令行断言含 `docs/handoff/archive/…` 且 origin 探针取到非空 SHA)。

| 反事实 | 补丁 (1 行) | 打补丁后首失败 | 落在 |
|---|---|---|---|
| 1 | 枚举层 `rel_paths.append(rel)` → `append(basename)` | 行 755 `AssertionError: 'docs/handoff/archive/2026-05-09-session-end.md' not found in [] : the probe must query the real path, got []` | **(a)** |
| 2 | `scan.py` 的 `filename = t.get("filename")` → `t.get("rel_path")` (局部变量整体重指) | 行 768 `AssertionError: 'archive/2026-05-09-session-end.md' != '2026-05-09-session-end.md'` | **(c)** |

**反事实 1 下 (b) 未执行到**: verification 第 2 条写「(a)(b) 红」, 实测首失败落在 (a) (行 755), (b) 在其后故未执行。如实记录, 不声称 (b) 实测为红 —— 机制上它必然也不成立 (补丁使该行根本不进 `tracks[]`, `log_paths` 为空 ⇒ 无探针可取 SHA), 但那是推论不是观测。
**反事实 2 下 (a) 绿、(c) 红**: 该补丁只改上报面、不改拼串面, 故 (a) 仍通过 —— 这正是本 spec 要钉的「拼串用 `rel_path` / 上报用 basename」两面分离, 也是 SC-6 (c) 作为回归锁能被单独观测的原因。

### TASK-016 — SC-7 与排序键第 5 级 GREEN + 删第 5 级的反事实

- `test_dedupe_tiebreak_prefers_lexicographic_max_path` docstring 首行实测为 `characterization test — hypothetical input: dictionary-max filename wins.` ⇒ 符合 verification 第 1 条的字面要求。
- 两个用例未打补丁 **Ran 2 tests OK**。
- **反事实 (三步)**: 补丁 = 删去排序键第 5 级 (`return (bucket, dt, filename, branch, (rel == filename, rel))` → 去掉末元组, 1 行) ⇒ 行 897 `AssertionError: 'archive/x.md' != 'x.md'` (反序输入换赢家)。**同一次运行里 SC-7 那条仍绿** ⇒ 实证 TASK-014 verification 第 3 条所述「第 3 级 `filename` 已分出胜负, 第 5 级不介入」。
- 既有套件计数 (复位后在副本上跑): `test_handoff_multibranch_collision_dedupe` **Ran 23 OK** · `test_track_board_advisories` **Ran 5 OK** —— 与 A.2 基线 23 / 5 一致, 断言未动。

### TASK-017 — SC-13 GREEN + 三条反事实

未打补丁 (每条补丁前均复位并重新确认): `test_legacy_track_id_uses_rel_path` **绿**, 三次确认均绿。

| 反事实 | 补丁 (1 行) | 打补丁后首失败 | 落在 |
|---|---|---|---|
| 1 | `_make_legacy_track_id(branch, rel)` → `(branch, filename)` | 行 568 `AssertionError: Items in the second set but not the first:` | **(a)** 两 track_id 集合不等 |
| 2 | legacy 分支 `_get_file_commit_date(…, rel)` → `(…, filename)` | 行 579 `AssertionError: False is not true : archived row must take its own commit date, got '2026-03-01T10:00:00+00:00'` | **(b)** |
| 3 | 删去 legacy 构造点的 `"rel_path": rel,` (只留 frontmatter 分支那处) | 行 584 `KeyError: 'rel_path'` | **(c)** |

**三条各自单独观测到, 无互相遮挡** —— 每条的首失败都正好落在其点名的断言上。反事实 2 的实测值尤其说明问题: 归档行拿到的是 `2026-03-01T10:00:00+00:00`, 即**顶层那份**的提交日, 而非自己的 `2026-04-01` —— 正是「仍拼顶层路径」的直接后果。

### TASK-018 — 其余实体反事实 (15 条)

副本 `wt-task018` 自 `9625999`, 每条补丁前复位并重新确认目标用例绿, 结束复位后 `worktree remove`; `worktree list` 不含本任务副本, 真仓 `porcelain` 0 行、`HEAD` 仍 `9625999`。

#### SC-15 六条 (verification 第 2 条)

| 补丁 | 形态 | 目标 | 首失败 |
|---|---|---|---|
| 1 | 去掉 §2.5 守卫 | 布局 2 | 行 1015 `AssertionError: '**Latest**: [' unexpectedly found in …` = (d) 前半 |
| 2 | 判据换成 `"/" in filename` | 布局 2 | 行 1015 同上 —— `filename` 恒 basename 故守卫恒不触发 (专防字符串嗅探) |
| 3 | 缺键兜底写成 `track.get("rel_path")` (去掉 `or filename`) | 布局 3 | 行 1047 `'[x.md](./x.md)' not found in …` = (g) |
| 4 | 在 `write_latest_md` 内重算谓词并写反 (按 verification 给的三行最小实现) | 布局 1 / 3 / 2 | **L1 行 983 `'target_in_subdir' is not None : (i)`** + **L3 行 1049 同 `(j)`** + **L2 绿** —— 与 verification 预期逐项吻合 |
| 5 | 见下「偏离 1」 | 布局 4 / 5 | 行 1065 / 1081 `KeyError: 'degraded_reason'` |
| 6 | `_render_pointer_unavailable` 的 `reason="missing_filename"` 改为复用 `"target_in_subdir"` | 布局 6 | 行 1100 `'target_in_subdir' != 'missing_filename'` |

#### SC-18 两条 · SC-9 两条 · SC-16 两条 · SC-2 一条 (verification 第 3 至 6 条)

| SC | 补丁 | 首失败 |
|---|---|---|
| SC-18 (1) | 见下「owner 推来的定向补丁」 | 行 320 `'handoff_multibranch_undecodable_path' not found in []` = (c) |
| SC-18 (2) | 把不可解码名计入 `unreadable_count` | 行 317 `1 != 0 : an undecodable NAME is not an unreadable file` = (b) |
| SC-9 (b) | 见下「偏离 2」 | 行 440 `0 != 1 : the other file on the same branch must still be collected` |
| SC-9 (c) | 不丢空段 (删去 `if not path: continue`) | 行 472 `1 != 0 : a well-formed enumeration must report no violation` |
| SC-16 | 见下「偏离 3」 | 行 279 `'/2026-05-01-with-fm.md' != '2026-05-01-with-fm.md'` |
| SC-2 | `-z` 输出按换行切分 | 行 832 `Lists differ: [] != [{'track_id': 'flat-2026-09-01-alpha', …}]` (枚举塌成畸形单段, 行不进 `tracks[]`) |

#### owner 推来的两条定向补丁 (2026-09-25 裁路径 A)

| 断言 | 补丁形态 | 首失败 |
|---|---|---|
| SC-15 布局 2 **(h)** | renderer 正文不动, `return …, reason` 改为写死 `"missing_filename"` | 行 1024 `'missing_filename' != 'target_in_subdir'`; (d) 前后半与 (e) 全绿 |
| SC-18 **(c)** | 跳过但不报 kind (删 `error_messages.append` 与 `r.soft_error`, 只留 `continue`) | 行 320 (同 SC-18 (1)); (a)(b) 绿 |

**SC-15 布局 2 的 (e) 仍未获观测** —— 与 (d) 前半结构互斥 (依据见上文「可观测性实测」段)。按 owner 裁定不拆用例, 故记录「在补丁 1 / 2 下未执行到」, 不声称实测。

#### 三处补丁形态偏离 (按 verification 第 2 条「改补丁、不改测试断言」的纪律, 偏离与原样输出照记)

**偏离 1 — 补丁 5**: 按字面「把 `degraded_reason = None` 的初始化挪进 `elif n_active == 1:` 分支内部」实跑得 `UnboundLocalError: cannot access local variable 'degraded_reason' where it is not associated with a value` (L4 / L5 均行 945), **不是** verification 预期的 `KeyError` —— 因为返回 dict 无条件引用该变量, 删掉分派前的初始化会先在构造 dict 时炸。按纪律改补丁: 保留初始化, 改为**只在 `action == "pointer"` 时给返回 dict 加该键**。这才是「只在一支加键」的真实形态, 也正是 §2.5 择定「恒存在」口径要排除的那种实现。改后 L4 行 1065 / L5 行 1081 双 `KeyError: 'degraded_reason'`, 与预期一致。

**偏离 2 — SC-9 反事实 1**: 按字面「沿用分支级错误通道 (收到非 None 即 `continue` 整支)」把 reporter 调用一并去掉, 实跑首失败落在**(a)** (行 434 `0 != 1 : exactly one prefix violation must be reported`) 而非 verification 点名的 (b)。按纪律改补丁: **保留 reporter 调用, 但随后 `return [], msg` 作废整支**。改后首失败落 (b) (行 440)。**这个形态才是 proposal 立 (b) 的理由本身** —— 它说「缺了 (b), 吞掉整分支的天真实现同样满足 (a) 而假绿, 且那种实现比原 bug 更坏」, 而「报了 kind 又吞整支」恰是该实现。

**偏离 3 — SC-16 两条**: 按字面「前缀剥离少剥斜杠」/「忘记剥前缀」实跑, 两者首失败均落在**行存在性**上 (行 275 `0 != 2 : both files must produce a row`) 而非所指的 `rel_path == filename` —— 因为剥离写错会让 `_read_file_content` 拼出不存在的路径, `git show` 失败, 行根本不进 `tracks[]` (与 TASK-035 notes 记的补丁 3 / 5 同型问题)。按纪律缩小补丁: **只让上报的 `rel_path` 带前导斜杠 (两个 TrackEntry 构造点各改一处), 读取路径仍用 `rel`**。改后行能进 `tracks[]`, 首失败落在 rel_path 断言 (行 279)。按字面的两个形态的原样输出一并留档于上。

### TASK-035 — proposal SC 表所列反事实 (六个补丁 / 七条 SC)

副本 `wt-task035` 自 `9625999`, 每条补丁前复位并重新确认目标用例绿; 结束复位后 `worktree remove`, `worktree list` 不含本任务副本。

| 补丁 | 形态 (只回退该组件) | SC | 首失败 |
|---|---|---|---|
| 1 | 枚举层 `rel_paths.append(rel)` → `append(basename)` | SC-1 | 行 210 `AssertionError: 0 != 1 : the subdir file must yield exactly one row` |
| 1 (共用) | 同上 | SC-17 | 行 802 `AssertionError: 'handoff_multibranch_git_show_failed' unexpectedly found in ['handoff_multibranch_git_show_failed']` |
| 2 | 去掉 `ls-tree` 的 `-z` 并改回 `splitlines()` | SC-3 | 行 365 `AssertionError: 0 != 1 : the CJK-named file must be collected` |
| 3 | 无 frontmatter 分支的 `_get_file_commit_date(…, rel)` → `(…, filename)` | SC-4 后半 | 行 529 `AssertionError: False is not true : a file that never existed at the top level must still get its own real commit date, got ''` |
| 4 | git show 失败路径恢复旧降级分支 (追加 legacy 行 + `legacy_count += 1`; kind 与 `unreadable_count` 保持新实现) | SC-5 | 行 619 `AssertionError: Lists differ: [{'track_id': 'legacy:master:archive/unrea…rue}] != []` |
| 5 | frontmatter 构造点 `"rel_path": rel` → `"rel_path": filename` | SC-8 后半 | 行 252 `AssertionError: 'latest-notes.md' != 'archive/latest-notes.md'` |
| 6 | fail-soft 早退 dict 删去 `"unreadable_count": 0` | SC-14 | 行 654 `KeyError: 'unreadable_count'` |

**每条首失败均落在 verification 写明的「现表现形态」所指断言内**, 无一条落到补丁带出的无关异常上 (第 10 条的缩小补丁条款未被触发)。

两处值得单记:

- **SC-17 的首失败落在「无 `handoff_multibranch_git_show_failed`」而非 `legacy_count == 0`** —— 因为 TASK-011 之后 git show 失败不再追加 legacy 行, `legacy_count` 仍为 0 而该 kind 出现。这正是 verification 第 3 条预告的「原句『归档件恒降级 legacy 且 owner_container unknown』现表现为『归档件行消失』」, 所指断言集不变, 首个失败落在其中任一条即算。
- **补丁 3 与 TASK-017 反事实 2 的 diff 相同但各自独立实跑** (verification 第 5 条: 两任务若并行, 复用副本会与对方的复位动作互相覆盖)。本轮串行执行, 仍按要求在各自副本上跑。

### 组 3 收口小结

| 任务 | 内容 | 结果 |
|---|---|---|
| TASK-015 | SC-6 GREEN + 2 条反事实 | 全部达成; 反事实 1 下 (b) 未执行到, 如实记录 |
| TASK-016 | SC-7 与排序键第 5 级 GREEN + 1 条反事实 + 既有套件计数 | 全部达成 (23 / 5 与基线一致) |
| TASK-017 | SC-13 GREEN + 3 条反事实 | 全部达成, 三条各自单独观测无遮挡 |
| TASK-018 | 13 条 verification 反事实 + 2 条 owner 推来的定向补丁 | 全部达成; **3 处补丁形态按「改补丁不改断言」纪律偏离并记录** |
| TASK-035 | 6 个补丁 / 7 条 SC | 全部达成, 首失败均落在所指断言内 |

**副本生命周期全部闭合**: 五个任务各建一个一次性副本 (`wt-task015` / `016` / `017` / `018` / `035`), 全部自 `9625999` 检出、结束复位后 `worktree remove`; 每次移除后 `git -C aria worktree list` 均只剩主工作树, 真仓 `porcelain` 0 行、`HEAD` 仍 `9625999`。

**组 3 后全量回归 (确认补丁未泄漏)**:

```
$ python3 -B aria/skills/state-scanner/tests/run_tests.py
Ran 1627 tests in 225.680s
OK                                    ← EXIT 0, FAIL/ERROR 计数 0
```

**唯一未获观测的断言**: SC-15 布局 2 的 **(e)** —— 与 (d) 前半结构互斥 (`_LATEST_POINTER_RE` 要求行首 `**Latest**: [`, 而 (d) 前半断言该串不出现在文本任何位置)。owner 2026-09-25 已否决拆用例 (路径 B), 故按「记录未执行到、不声称实测」处置, 其鉴别力由同补丁下 (d) 的红 + 一条逐环节实读确认的机制链间接支撑。

**下一步 = 组 4 (TASK-019~024)**: schema 文档 / collector docstring / standards 第三态 / SC-11 余下谓词 / 全量回归两腿。组 4 与组 3 在 TASK-033 之后本可并发, 本轮串行完成组 3, 故组 4 开工时 aria 工作树仍是 `9625999` 的干净态。

---

## 组 4 文档同步 (TASK-019 / 020 / 023 / 024)

### TASK-019 — state-snapshot-schema.md §tracks_multibranch 同步

提交 **`4d21e46`** (aria feature; 只 add 本任务 deliverable)。

- 字段块新增 `unreadable_count` 并写明**三类外延边界**: git show 失败计入且不产行 / 前缀守卫丢弃的行不计入 / 名字非 UTF-8 的路径不计入 (读都没读就跳过)。
- TrackEntry 块新增 `rel_path`; `filename` 行补「NEVER carries a directory segment」; `track_id` 的 legacy 公式改 `legacy:<branch>:<rel_path>`。
- `latest.md` 排除句**改原句**为任意深度 (未另加一句), 并举出近似名 `archive/latest-notes.md` 仍保留的对照。
- dedupe 现状键元组改五元, 补「相对路径 tie-break」说明项; `compound key` 行与 Renderer parity 句的层数词去除。
- 新增三段正文: 两个新 kind 的登记与双通道说明 / `git show` 失败不再伪造 legacy 行及其危害 / 非 ASCII 名边界改写成条件式 (`-z` 使结果不再依赖 `core.quotePath`)。
- fail-soft 早退形状补 `unreadable_count` 与**既有漏写的** `identity_advisories`。
- Change history 新增一行, 写明 `snapshot_schema_version` 保持 **1.0** (全部 additive)。

**SC-11 实跑**: (a1)(a2)(b)(f1)(f2)(g)(i2)(j2) 八条逐条 PASS。(j4) schema 侧清零 —— 过程中**写第 5 级说明时自己写出了一个层数词**, 复扫发现后改掉 (与台账早先那次「描述违规物自成违规物」同型)。

### TASK-020 — collector 契约面与键层级描述整类

提交 **`9f3b05b`** (aria feature; 只 add 三个 deliverable)。

- 键层级整类改写: `# Tie-break` 注释块的现状键元组写全五元并**保留行首前缀** ((j3) 的锚点, 全文保持唯一); 四处 `dictionary-max` 描述各自点名 `rel_path` ((j5)); 历史轮次改用元组表述; docstring 里 `round-3 4th level` 这类**轮次序数按 verification 保留不改**。
- 层数词清零 ((j4)): collector 三处 + dedupe 测试两处。测试文件 diff 严格只触及那两处 docstring 所在行 (2 insertions / 2 deletions), **断言零改动**, 该模块仍 `Ran 23 OK`。
- 契约面订正: `legacy_count` 注释改为与新行为一致 (读到了但无 frontmatter 才算 legacy); 两处 docstring 的路径占位符 `<filename>` 改 `<rel_path>`。
- **顺带订正一处既有事实错误**: `updated_at` 来源在模块 docstring 与 `_get_file_commit_date` docstring 里一直写作 "committer date", 而实现用的是 `--format=%aI` (**author date**)。三处统一订正。该错误早于本 spec, 非本轮引入。
- `phase-1-collectors.md` 的 `Return dict` 补 `degraded_reason` ((l2)), 并写明三支恒存在、取值枚举、由 renderer 回传而非 `write_latest_md` 自行重算。

**SC-11 实跑**: (j1)(j3)(j5)(l2) PASS; (j4) 三文件合计零命中; (c1)(c2)(i1) 保持为真。

### TASK-023 — standards 第三态 + layer-l-integration 同步

提交 **`11b0a14`** (standards feature — 该子模块在本 cycle 的**第一个**提交) 与 **`b181678`** (aria feature)。

- `session-handoff.md` §2.3: 两态判据不动, 新增「目标不在顶层」第三态并限定**经机械 `latest_md_writer` 写入时**; §2.3.1 写入后那句同批补限定从句; 被改小节按 §2.3.5 先例加 `Amended` 标注 (标明 additive)。
- `layer-l-integration.md` 的「单 track: 更新 latest.md pointer」一行补子目录限定 ⇒ **(l3) PASS**。
- **Version 头保持 1.3.0 未 bump (判断与理由)**: 该文件的版本头已由 `10CG/aria-standards#20` 专门跟踪 (它指出前两次实质增量未 bump、建议 1.4.0)。本次是第三次 additive 增量; 在此自行 bump 会把三次合并进一个号、掩盖 `10CG/aria-standards#20` 记录的事实, 且 standards 版本治理不在本 spec 范围。**请 owner 复议**。
- **手改路径措辞取 TASK-025 的回落形态**: verification 第 1 条要求写「跟踪见 `10CG/aria-plugin#<TASK-025 开出的号>`」, 但 TASK-025 依赖 TASK-021 且是 owner gate, 号此刻不存在。为不在仓库里留 `#<` 占位符 (TASK-025 verification 第 5 条要求回填后该 grep 零命中), 本轮直接落**回落措辞**「(已知缺口, 尚未开跟踪 issue)」, 待 TASK-025 开单后按其第 5 条回填。落笔后实跑 `grep -n '#<' conventions/session-handoff.md` **零命中**。**这是 AI 流程判断, 请 owner 复议**。
- **五处扁平布局描述复核** (verification 第 5 条): `:15` 目录级 canonical 声明 · `:88` / `:94` 文件名模板 · `:304` `docs/handoff/*.md` 非递归 glob · `:339` 输出路径硬编码不接受 dir 参数。五处**均隐含扁平布局**, 但本 spec 只修「读到子目录文件时不伪造 legacy 行」、不对子目录布局表态 ⇒ 不改, 交遗留 issue。

### TASK-024 — 处方面措辞复核: **六处全部无需改, 无编辑、无提交**

| 位置 | 结论与依据 |
|---|---|
| `advanced-rules.md:443-444` | **无需改** —— 判据读 `tracks_multibranch.exists` 与 `len(tracks) >= 2`; 本 spec 改的是这些字段的**取值** (不再有伪 legacy 行), 判据语义不变 |
| `advanced-rules.md:511-512` | **无需改** —— 同上 |
| `advanced-rules.md:544` | **无需改** —— 判据是 `collision.kind != none`; 本 spec 会让该值从 `none` 翻到 `cross_owner` (SC-17), 但判据文本与括注里的两种 kind 定义均仍准确 |
| `RECOMMENDATION_RULES.md:28` | **无需改** —— 「本 container 无 active owned track」不涉及路径面 |
| `RECOMMENDATION_RULES.md:30` | **无需改** —— 「leader pointer 仍在 `latest.md`」描述的是**事实状态**而非「上次一定写了 pointer」。TASK-013 之后该状态的成立面**变窄**了 (单 track 但目标在子目录时本就不写真指针), 但这句文本仍准确。变窄一事记此备查 |
| `RECOMMENDATION_RULES.md:31` | **无需改** —— 同 `:544` |
| `phase-d-closer/SKILL.md:218` | **无需改** —— 该行说 Pointer 更新「conditional by multi-track detection」, 即 **action 三值由 `n_active` 决定**; 子目录降级**不改变 action** (仍走 `pointer` 支), 只改写该支的内容与 `degraded_reason` ⇒ 摘要行仍准确。完整决策表在 `handoff-mechanics.md`, 其未同步第三态一事已由 TASK-025 的 (g) 条登记, 不在本任务候选文件内 |

**连带结论**: 未对 `advanced-rules.md` / `RECOMMENDATION_RULES.md` 落编辑 ⇒ `metadata.rule6_note` **不改写为判据表第二行** (verification 第 2 条); 未对 `phase-d-closer/SKILL.md` 落编辑 ⇒ TASK-026 **不追加 phase-d-closer AB** (第 3 条) ⇒ **AB 范围不扩大**。此结论建立在上表逐处依据上, 不是为省成本而作的裁量。

### TASK-021 — 全量回归两腿 + SC-10 + SC-11 全谓词 + 冻结产物未重生成

**[1] 回归前置**: `git -C aria status --porcelain` 与 `git -C standards status --porcelain` **输出均为空**。
feature 分支 HEAD: aria **`b181678619023910bb4eed7266afc765ce937322`** · standards **`11b0a149f0ff39691c3571b766c49ec45a3bcb7e`**。
**该 aria HEAD SHA 即 TASK-026 的 with 臂 SHA。**

**[2] (a) 全量 unittest**:

```
$ python3 -B aria/skills/state-scanner/tests/run_tests.py
Ran 1627 tests in 202.120s
OK                                    ← EXIT 0, FAIL/ERROR 计数 0
```

1627 = A.2 基线 **1605** + 本 Spec 新增 **22** 个 TestCase 用例, 与 TASK-001 实测的基线口径一致。

**[3] (b) pytest 腿**: `state-scanner tests/test_collision.py` **28 passed** · `phase-d-closer tests/` **11 passed** —— 与 B.1 实测数目逐个相同, 零失败。

**[4] SC-10 点名集**: 8 个 unittest 模块一次跑 `Ran 169 tests … OK` —— 与 `metadata.test_runner` 记的 A.2 实测 **169** 一致; `test_collision.py` 走 (b) 已零失败。

**[5] SC-11 全部 19 条谓词**: 机械解析 `metadata.sc11_baseline_predicates` 后逐条执行 —— **解析 19 条 / PASS 19 / FAIL 0**。标签: `a1 a2 b c1 c2 f1 f2 g i1 i2 j1 j2 j3 j4 j5 k l1 l2 l3`。
> **解析器空集防护**: 首次解析因切分方式错误得 0 条, 而脚本仍打印「全部为真」—— 典型的真空成立假绿。已在脚本里加 `assert len(preds)==19`, 解析不到 19 条即判解析器失效、不得据此下结论。
**后半条件判断**: `git log` 实查本 session 触及本 change 目录的 10 个提交中, 触及 `detailed-tasks.yaml` 或 `sc11-predicate-validation.py` 的为 **0 个** ⇒ 谓词与验证脚本自 TASK-001 起未被改动, 无需重跑 `--emit-json` 比对。

**[6] 冻结语料未重生成** (分仓各跑, 未用超级仓 revision):

```
$ git -C aria diff 1cb3872 -- skills/state-scanner/tests/fixtures/handoff-tracks-frozen-2026-09-05.json   → 0 行
$ git diff a52b5eb -- .aria/repro/handoff-tracks-frozen-2026-09-05.json                                    → 0 行
```

**[7] 平铺基线 JSON 未重生成**: `git -C aria log` 对该文件只列出 **一个**提交 (`a7b5fe5`, RED 批次第三批), 且 `git -C aria diff a7b5fe5 -- <该文件>` 为 **0 行**。

**[8]**: 无任何失败, 无需归因。

### TASK-022 — 活体 dogfood (SC-12a / SC-12b)

#### SC-12a — 本仓平铺, 背靠背

改前 = `git -C aria worktree add` 检出 **B.1 基线 `1cb3872`** 的旧代码; 改后 = feature 分支代码。两次**都在主仓根目录**执行, 背靠背进行, `--output` 写 scratchpad (未碰 `.aria/state-snapshot.json`)。两次 `scan.py` 退出码**均为 0**。

**冻结核验 (比 proposal 多比 SHA)**: 每次扫描后各存一份 `git for-each-ref --format="%(refname) %(objectname)" refs/remotes/`, 两份各 21 行且 **逐行相同** ⇒ 本次背靠背有效 (两次之间远端跟踪 ref 的分支集与 SHA 均未变)。

**判据结果**:

| 项 | 改前 | 改后 |
|---|---|---|
| `tracks_multibranch` 顶层键 | 6 个 | 7 个 (**只多 `unreadable_count`**) |
| `tracks` 行数 | 2038 | 2038 |
| `legacy_count` | 336 | 336 |
| `unreadable_count` | (无该键) | **0** |

**剔除 `unreadable_count` 与每行 `rel_path` 后逐字段相等 ⇒ PASS**。另: 改后每行都带 `rel_path`, 且本仓平铺状态下 **2038 / 2038 行满足 `rel_path == filename`** —— SC-16 的活体印证。

#### SC-12b — 子目录临时仓 (带 bare 仓作 origin)

按 verification 要求建**真 remote** (`git init --bare` + `git push`), 未用 `update-ref` 手法 —— `scan.py` 的 sync collector 以 `git remote` 有无输出为判据。夹具: 一个子目录件 `docs/handoff/archive/2026-09-20-subdir-track.md` (带 frontmatter, `status: active`) + 一个顶层对照件。

```
exit=0
tracks 行数: 2 | legacy_count: 0 | unreadable_count: 0
tracks_multibranch.errors: []   顶层 errors kinds: []

track_id=toplevel-dogfood-track  legacy=False  filename=2026-09-19-toplevel.md      rel_path=2026-09-19-toplevel.md
track_id=subdir-dogfood-track    legacy=False  filename=2026-09-20-subdir-track.md  rel_path=archive/2026-09-20-subdir-track.md
```

**三条判据全中**: 无 `handoff_multibranch_git_show_failed` · `legacy_count == 0` · 子目录件以**真 track** 出现 (`legacy=False`, frontmatter 的 `track_id` 被正确读出, `filename` 仍是 basename 而 `rel_path` 带目录段)。**这是本 spec 修复的活体端到端证明** —— 同一份夹具在 B.1 基线上会产出一条 `owner_container="unknown"` 的伪 legacy 行加一条 `git_show_failed`。

**清理**: dogfood 副本 `worktree remove`, 临时仓删除; `worktree list` 只剩主工作树; 三仓 `porcelain` 复核 —— aria 空 / standards 空 / 主仓仅两个 gitlink 与本台账 ⇒ `scan.py` 未污染工作树。

### 组 4 收口小结

| 任务 | 结果 | 提交 |
|---|---|---|
| TASK-019 | schema 同步, 8 条谓词 PASS | aria `4d21e46` |
| TASK-020 | collector 契约面 + 层数词清零, 4 条谓词 PASS | aria `9f3b05b` |
| TASK-023 | standards 第三态 + layer-l 限定, (l3) PASS | standards `11b0a14` · aria `b181678` |
| TASK-024 | 六处复核**全部无需改**, 无编辑无提交 ⇒ AB 范围不扩大 | — |
| TASK-021 | 两腿回归 1627 + 28 + 11 全绿; SC-10 169; **SC-11 19/19**; 冻结产物三项 diff 均空 | — (台账) |
| TASK-022 | SC-12a 逐字段相等 + SC-12b 子目录件真 track | — (台账) |

**下一步 = 组 5 (TASK-025~032 + 034)**: 遗留 issue (owner gate) → Rule #6 AB (owner 启动门) → 版本 bump 与 CHANGELOG → 子模块合并与双推 → 主仓同步面与 PR → Phase D。**其中 TASK-026 的 AB 需 owner 以 `ARIA_COORDINATION_NO_PUSH=1` 启动新会话, 本会话内无法进行。**

---

## feature 分支备份推送 (owner 2026-09-25 授权)

**授权**: owner 2026-09-25 裁「推 feature 分支备份」。**性质 = 备份推送, 不是 TASK-031 的 PR 推送** —— 只把 feature 分支发布到两个 remote, master 与 gitlink 均不动, `owner_gates` 第 12 项 (主仓 PR + 合并) 与第 10 项 (aria master + tag 双推) 都还没到。

### 推送前置

目标分支 `feature/handoff-multibranch-subdir-path-fidelity` 在四处 (aria origin/github · 主仓 origin/github) 均**不存在** ⇒ 首推, 无非快进风险。四次 push 分开执行 (不用 `&&` 连推, 以免半推时后续不跑), 各自 `exit 0`。

### 推后逐 remote 独立核验 (不信 push 回执, 硬约束 2)

```
本地 aria feature = 9625999c734119aba56185edd2b258f215d3da57
本地 主仓 feature = 617d769b4b93a77219c64638fed5108db04249e0

aria/origin    9625999c734119aba56185edd2b258f215d3da57  -> MATCH
aria/github    9625999c734119aba56185edd2b258f215d3da57  -> MATCH
主仓/origin    617d769b4b93a77219c64638fed5108db04249e0  -> MATCH
主仓/github    617d769b4b93a77219c64638fed5108db04249e0  -> MATCH
```

**四处全部 MATCH**, 无半推、无镜像分叉。

### gitlink 可达性核验 (防孤立 gitlink, CLAUDE.md 多远程硬约束 1 的事故形态)

主仓 feature 分支上两个 gitlink 及其可达性:

| 子模块 | gitlink | aria/standards origin | github |
|---|---|---|---|
| `aria` | `1cb3872` | 可达 (= 该 remote 的 master tip) | 可达 (同) |
| `standards` | `940cb5b` | 可达 (= master tip) | 可达 (同) |

两个 gitlink 指向的都是**各 remote master 上已发布的 commit** ⇒ 即使有人此刻 `clone --recursive` 主仓 feature 分支也不会断裂。**本轮未 bump 任何 gitlink** (aria 的新提交 `9625999` 只在 feature 分支上, 主仓 gitlink 仍指 `1cb3872`) —— 符合 `hard_constraints` 第 4 条与 `owner_gates` 第 11 项「两个远端未都核验一致前不得 bump gitlink」的更强前提。

### 未推的部分

**主仓 `master` 侧的提交未推** (owner 的授权原文是「推 feature 分支备份」): 本份台账所属的 spec 目录在 feature 分支, 而 session handoff 与 post_planning R5 的 `overridden_by_user` 回写落在 master。master 侧提交数与推送授权另请 owner。

**本节记录自身的提交随同批第二次推送**, 其核验结果记于会话回复。

---

## 会话入口与 master 推送 (2026-09-26 ~ 27 会话)

### claim 心跳 (owner 2026-09-17 免逐次授权, 前提 = 本地协调 ref 与 origin 一致)

会话开头 `/aria:state-scanner` 后按三元组 (本容器 `bfe8285d` / 归一 track_id / active) 解析, 本容器恰有两条 active claim, 各轨恰 1 条。顺序: 前置检查 (`coord_ref_precheck`, 代码取自 `pre-merge-completeness-gate-change-scope` 计划 metadata) → 强制对齐 `git fetch origin +refs/aria/coordination:refs/aria/coordination` → 重解析 → `phase1_gate.py --heartbeat-only` → 推后核验。两次前置检查均 `{"verdict": "ok", "local_ahead": 0}` 退出 0, 两次对齐均退出 0, 会话未带 `ARIA_COORDINATION_NO_PUSH`。

| claim | track | 刷新前 `heartbeat_at` (距扫描时) | 刷新后 | push_success / push_skipped | 推后 `ls-remote origin` 与本地 |
|---|---|---|---|---|---|
| `s-48ca@0612` | 本轨 (phase B) | `2026-09-26T05:00:16Z` (约 10.7h) | `2026-09-26T15:48:50Z` | true / false | `82adeb0` MATCH |
| `s-73b9@1606` | `pre-merge-completeness-gate-change-scope` (phase A.2) | `2026-09-25T05:04:03Z` (约 34.7h, **已超 SWEEP_TTL 24h**) | `2026-09-26T15:49:43Z` | true / false | `ae24f81` MATCH |

### 主仓 master 推送 (owner 2026-09-26 授权)

**授权**: owner 对 state-scanner 推荐答「1+2」, 其中 [2] = 推送 `d33d233` (上一会话收尾 handoff) 到两个 remote 并逐个 `ls-remote` 核验。推前 fetch 两端, `origin/master` 与 `github/master` 均为 `7e7c1a4` 且是本地 master 的祖先 (快进)。两次 push 分开执行, 各自退出 0。

```
local  = d33d23364a2c78b0a80c673267f77cc301bd2a5b
origin = d33d23364a2c78b0a80c673267f77cc301bd2a5b MATCH
github = d33d23364a2c78b0a80c673267f77cc301bd2a5b MATCH
```

之后主仓切回 feature 分支 (`cc4005e`, 本地与两个 remote 一致); master 与 feature 两侧的 gitlink 同为 aria `1cb3872` / standards `940cb5b`, 切换不动子模块检出。

---

## TASK-025 — 遗留缺口 issue (parent 5.3)

**授权**: owner 2026-09-27 经 AskUserQuestion 裁「开单，按此正文发」(选项原文)。发帖前正文全文与下文五处 AI 判断一并呈 owner 过目。**结果: `10CG/aria-plugin#204`** (https://forgejo.10cg.pub/10CG/aria-plugin/issues/204)。

### 第 1 条 — 查重 (q= 定向查询 + limit=50 分页至不满页, state=all)

`10CG/aria-plugin`, 14 个检索词:

| 检索词 | 命中 | 检索词 | 命中 |
|---|---|---|---|
| `_parse_latest_pointer` | 0 | `degraded_reason` | 0 |
| `_scan_md_files` | 0 | `target_in_subdir` | 0 |
| `handoff_worktrees` | 0 | `_render_banner` | 0 |
| `_resolve_latest` | 0 | `snapshot_consistency` | 0 |
| `reference-snapshot-aria` | 1 | `subdir` | 3 |
| `handoff-mechanics` | 0 | `latest.md` | 3 |
| `子目录` | 116 (3 页) | `递归` | 116 (3 页) |

- 标识符类检索词的 6 条命中 (`10CG/aria-plugin#199` / `10CG/aria-plugin#196` / `10CG/aria-plugin#195` / `10CG/aria-plugin#136` / `10CG/aria-plugin#67` / `10CG/aria-plugin#56`) 主题均不同。
- CJK 两词为模糊匹配、无区分度: 对并集 116 条**只按标题**复筛 handoff / latest / pointer / 指针 / 交接 / 扁平 / worktree / 子目录 / 递归, 得 6 条 (`10CG/aria-plugin#155` / `10CG/aria-plugin#149` / `10CG/aria-plugin#123` / `10CG/aria-plugin#121` / `10CG/aria-plugin#71` / `10CG/aria-plugin#67`), 主题分别为 collision 误报 / audit 取最新 / autofill 盲区 / 分支上限 / History 检查, 无一涉及 `handoff.py` 扁平布局。
- 主仓 `10CG/Aria` 同批检索 (去掉 CJK 两词), 并集 10 条: 无重复; 相邻三条 `10CG/Aria#218` (无指针时的回落链) / `10CG/Aria#168` (AC-5 条已含 `errors[].kind` 的 schema 登记) / `10CG/Aria#169` (AC-5 搬成独立 collector) 写进正文交叉引用。

**判定: 无重复单**。

### 第 2 / 3 条 — 正文逐处实读核对 (aria `b181678` / standards `11b0a14`)

| 条目 | 位置 | 核对 |
|---|---|---|
| 主缺口 | `handoff.py:288` `Path(target).name`; `_scan_md_files` `:300`, 循环 `:318` `iterdir()` | 与计划一致 |
| 现成复现 | `test_handoff_multibranch_path_fidelity.py:985` `test_pointer_roundtrip_subdir_guarded` | 存在, 断言写侧降级 |
| (a) | `handoff_worktrees.py:82-83` 导入, `:285` / `:291` 调用 | 与计划一致 |
| (b) | 降级页行 `**Latest**: (pointer 不可用)` 不匹配 `_LATEST_POINTER_RE`; `_resolve_latest` 只在目标文件不存在时发信号 | 机制成立 |
| (c) | `tests/fixtures/reference-snapshot-aria.json` 末次改动 `50bbf64` (2026-07-18), `unreadable_count` / `rel_path` 均 0 命中 | 成立 |
| (d) | `_render_banner` 在 `latest_md_writer.py:219` | **行号与计划不同** (计划 `:172-224` 为 `f314785` 基线, 本 spec 改动后下移) |
| (e) | schema §`errors` 只列三键; `tracks` 子键写在 `scan.py:278` / `:292`; `scan.py:403` 以 `**err` 并入, `err` 带 `kind` 而非 `error` | **行号与计划不同** (计划 `:269,283`); `kind` 一事已由 `10CG/Aria#168` 跟踪 |
| (f) | `scan.py:195` 用 `rel_path` 拼路径, `:202` / `:218` 上报 `filename` | 成立 |
| (g) | `handoff-mechanics.md:114-124` 判定表三种场景; standards `session-handoff.md:176` 已限定第三态 | 与计划一致 |
| 另记 | `session-handoff.md:97`「自动」; 布局锚点 `:15` / `:88` / `:94` / `:304` / `:339`; 两个 collector `exists` 矛盾 (proposal §SC-15 细则 (f) 的处置) | 成立; `write_latest_md` 非测试调用点仍为零 (只在 `writers/__init__.py` 再导出) |

「mv 日」语义按第 3 条**完全不写入**正文。

### 起草时的 AI 判断 (发帖前已呈 owner, owner 按原文授权)

1. 行号按当前代码重新核对, 两处与计划不同 (见上表 (d)(e))。
2. (e) 注明 `kind` 键名已由 `10CG/Aria#168` 跟踪, 本单只补 `tracks` 这一半 —— 核实时一度判为新发现, 查重后更正, 未当新问题写。
3. (b)(d) 补与 `10CG/Aria#218` 的互补关系。
4. 增加计划外的「若将来要修（参考，未裁）」一节 (owner 选项里「删掉该节」未被选)。
5. 「mv 日」语义不写。

### 第 4 条 — 写法自检 (发帖前) 与发帖核验

| 检查 | 正文 + 标题 | 阳性对照 (用 `chr()` 拼出违规字符的临时文件) |
|---|---|---|
| `check_bare_issue_refs.py` | `裸 issue 引用: 0`, 退出 0 | 报出 1 处, 退出 1 |
| §4.5 自查命令 | 无输出 | 命中 1 行 |
| `chr(0xFFFD)` 计数 / 希腊字母 (U+0370–U+03FF) | 0 / 0 | — |

- `POST /repos/10CG/aria-plugin/issues` (请求体 `--data-binary @` JSON 文件) 退出 0 ⇒ `number=204`, `state=open`, `created_at=2026-09-27T03:13:37Z`。
- 独立 `GET /repos/10CG/aria-plugin/issues/204`: `state=open`, 仓 `10CG/aria-plugin`, **标题与正文与发出的逐字相等** (正文 4525 = 4525 字符), 正文 `chr(0xFFFD)` 计数 0。

### 第 5 条 — standards 回填提交

提交 **`d86fc91`** (standards feature; 只 add `conventions/session-handoff.md`, 1 insertion / 1 deletion): `:176` 的回落措辞「(已知缺口, 尚未开跟踪 issue)」→「跟踪见 `10CG/aria-plugin#204`」, 与 TASK-023 第 1 条规定的形态一致; 反引号全限定写法与同节 `Amended` 注一致。

- `grep -n '#<' conventions/session-handoff.md` 退出 1 (零命中); 提交后对 `git show HEAD:` 复核计数 0。
- 裸 issue 引用检查改前改后同为 10 处存量 (行 6 / 66 / 183 / 213 / 251 / 261 / 359 / 361 / 437), 第 176 行零新增。
- 行尾 `i/lf w/lf`, 未变。
- **提交未带 `Co-Authored-By` 行 (AI 流程判断, 请 owner 复议)**: `standards/conventions/git-commit.md` §8.1 明令禁止 `Co-Authored-By: Claude...`, 而 CLAUDE.md Rule #4 以该文件为提交规范 SOT; 本 cycle 此前各提交带了该行。二者谁优先的问题由 `10CG/aria-standards#18` 跟踪, 未裁。

### 未推的部分

standards `d86fc91` 与本台账提交 (主仓 feature) 均**未推**; 备份推送属外向动作, 另请授权 (`hard_constraints` 第 3 条)。

---

## owner 裁定与后续推送 (2026-09-27)

> 本节承接上一节末尾的两处待办, 上一节原文不改。裁定的权威记录是主仓 master 的决策单 `.aria/decisions/2026-09-27-195-199-owner-rulings-pending-items.md` (`4c968ca`)。

### 推送 (owner 裁「全部推」)

上一节「未推的部分」已被取代: standards `d86fc91` 与主仓 feature `c5f494f` 均已双推。推前两端均为本地的祖先 (快进), 四次 push 分开执行、各自退出 0, 推后逐 remote 独立 `ls-remote`:

```
standards feature  origin = d86fc91adb966881d987eb7be9d72dce6fe22d0d  MATCH
standards feature  github = d86fc91adb966881d987eb7be9d72dce6fe22d0d  MATCH
主仓 feature       origin = c5f494f9ea5a21ba791db6306fc1bac6f16847d4  MATCH
主仓 feature       github = c5f494f9ea5a21ba791db6306fc1bac6f16847d4  MATCH
```

主仓 feature 的两个 gitlink 仍为 aria `1cb3872` / standards `940cb5b` (未动)。

### 提交署名 (上一节「请 owner 复议」一条)

owner 裁「本 cycle 剩余提交不加 `Co-Authored-By: Claude` 行, 按 `git-commit.md` §8.1」。TASK-027 起的提交一律不加。

### standards `session-handoff.md` 的 Version (决策单第 1 项)

owner 裁**本 cycle 升到 1.4.0** (MINOR), 一次补齐 `d217ed0` / `21748d4` / 本 cycle `11b0a14` + `d86fc91` 三次增量, 头部括号逐条列出; **并入 TASK-027 执行**, 在 TASK-029 合并 standards 之前提交到 standards feature 分支; 合并后回帖关闭 `10CG/aria-standards#20` (该回帖到时再请授权)。**本条更正组 4 TASK-023 节「Version 头保持 1.3.0 未 bump」的理由** —— 「会把三次合并进一个号、掩盖记录的事实」不成立: `10CG/aria-standards#20` 自己建议的就是用一个 1.4.0 补齐, 逐条列出不掩盖任何一次。执行时记进 `tasks.md` 的 AI 流程判断清单 (计划外改动)。

### 四条断言的归属订正 (决策单第 2 项)

owner **追认**: 2026-09-25「路径 A」裁定的实质是走三步法反事实, 按计划分工落在 TASK-015 (SC-6 (c)) 与 TASK-018 (SC-18 (c) / SC-15 (e)(h)), 见上文「owner 裁定 (2026-09-25): 取路径 A」一节的逐条对照。

### 本节提交自身

本节所在的台账提交只在本地 feature 分支, **写作时未推** —— 本轮 owner 授权的外向动作只含决策单第 3c 项的落仓推送与第 4 项的两条评论; 它随本轨下一次推送 (TASK-031 或另获授权的备份推送) 一并发出。

## TASK-026 — Rule #6 照跑 AB (parent 5.5)

> 会话: owner 以 `ARIA_COORDINATION_NO_PUSH=1` 新起的专用进程 (2026-09-27); 按 09-27 handoff §3 关键风险第 1 条, **本会话未刷心跳、未跑 `phase1_gate`**。结果目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/` (结论全文见其 `RESULT.md`, 本节只记核验事实)。执行方式: `/skill-creator` (benchmark 流程), 臂与评分员均为子 agent。

### 第 1 条 — 协调 ref 一致 (开跑前, 16:52Z)

```
git ls-remote origin refs/aria/coordination  = e91113242a3d087b718ab08608f55a92041c2658
git rev-parse refs/aria/coordination         = e91113242a3d087b718ab08608f55a92041c2658   ⇒ 一致
```

另记: `github` 远端的 `refs/aria/coordination` 为 `ad0287f` (2026-05-24, 是 `e911132` 的祖先) —— 协调 ref 只在 origin 维护, 本条判据只比 origin, 不影响开跑。

### 第 1 条补测 — 变量生效

```
$ python3 -B -c "import sys; sys.path.insert(0, 'aria/skills/state-scanner'); from lib.failure_handlers import no_push_requested_by_env; print(no_push_requested_by_env())"
True
```

### 第 2 条 — push_skipped 核验: **未触达**

30 个 run 的 transcript 逐个审计 (`dispatch/transcript_audit.txt`): phase1_gate / release_gate **零执行**; regex 命中的 12 处逐条核过, 全部是写进 answer.md 的 heredoc 命令文本; 无任何 `push_skipped` 输出。该步空真, 不算核验通过, 由第 1 / 第 3 步前后比对兜底。

### 第 3 步 — 强制对齐 (17:32:24Z)

```
执行前  本地 = e911132…   origin = e911132…
git fetch origin +refs/aria/coordination:refs/aria/coordination
执行后  本地 = e911132…   origin = e911132…
```

AB 期间远端 ref 未变化 (运行中另抽查两次, 两端均 `e911132`) ⇒ 无需逐 commit 核作者。

### 预测 — PREDICTION.md

写入时刻 **2026-09-27T16:56:51Z**, 先于任何臂 (首批臂 16:57:32Z 派出); sha256 `3aab0a78d923d09b23d63abb126d8796d0e47e416e0105b68943215f4e8c765d`, 全程未改。预测: 两臂逐 eval 相等, delta ≈ 0。

### 两臂口径与路径核验

- 口径「代码 + 文档整体」。with = aria `b181678619023910bb4eed7266afc765ce937322`; 开跑前断言 `git -C aria rev-parse HEAD` = 该 SHA, `git -C aria status --porcelain` 0 行 ⇒ 直接用 `aria/skills/state-scanner`。
- old = `1cb387218935433312fde4067c276754b77686a8` 的一次性 worktree: 16:54:09Z `git -C aria worktree add --detach <scratchpad>/old-arm-1cb3872 1cb3872` (HEAD 实测 = 该 SHA, 工作树 0 行改动); 17:32:57Z `git -C aria worktree remove` (之后 `worktree list` 只剩主工作树)。
- 两臂提示均写明各自 `SKILL.md` 与 `scan.py` 的绝对路径。transcript 审计: 26 个 run 跑了 scan.py, 全部是本臂那一份; eval 12 / 13 的 4 个 run 按题面未跑。**零作废、零补跑**。
- 派臂前实测两臂差异 (写进 PREDICTION): `SKILL.md` 逐字节相同; 本仓 snapshot 只差 `tracks_multibranch.unreadable_count` 与每条 track 的 `rel_path` 两个新增键。

### 结果与无回归判据

`tools/score.py` 从两臂 `grading.json` 直算 (`SCORES.md`):

```
主样本 13 eval / 78 断言: with 50/78 · old 50/78
mean(with pass_rate) = 0.7141; mean(old pass_rate) = 0.7141
delta.pass_rate = +0.0000
主样本 with < old: eval-5 (3/6 vs 4/6) ⇒ 复跑两次: rep2 3/6 = 3/6, rep3 3/6 = 3/6 ⇒ 1/3 ⇒ 不判回归
```

评分口径: 每个 eval 由同一评分员一次评两臂, 两臂以随机 X / Y 匿名。需复跑的 eval 仅 1 条 (< 3) ⇒ 不拆任务。未判回归 ⇒ 止损未触发。

### 与 SOT 验收判据的关系

场景 1 验收 `delta.pass_rate > 0` **未达成**; 回归面判为无效度 (两臂 AI 可见输入几乎相同 + 套件对改动面零覆盖 + 大面积恒真 / 恒假断言) ⇒ 结论「**未被有效测试**」, 不单独构成通过。

### owner 裁定 (2026-09-27, AskUserQuestion, 附 PREDICTION 对照与套件缺口单草稿)

原文 (选项): **「放行进 TASK-027 (推荐)」** —— 选项说明: 「认定 Rule #6 义务已照跑履行; 这组改动的鉴别力由已有替代证据承担 (TASK-007 RED / TASK-015~018+035 反事实 / TASK-021 全绿 / TASK-022 活体), 套件测不到的面靠缺口单跟踪。代价: 本 cycle 的 ship 态边际增益没有任何 AB 数字支撑, 只能写「未被有效测试」。」

### 套件缺口 issue — `10CG/aria-plugin#205`

- 查重 (`state=all`, 检索词 `handoff_multibranch` / `tracks_multibranch` / `ab-suite` / `state-scanner.json` / `basename` / `legacy`): 相关 `10CG/aria-plugin#157` / `10CG/aria-plugin#177` / `10CG/aria-plugin#204` 逐条读正文, 均不覆盖本缺口 ⇒ 无重复。
- owner 同一次 AskUserQuestion 授权「按草稿发帖」→ POST 返回 205 → 独立 GET: `state=open`, 标题逐字一致, 正文逐字一致 (1967 字符)。

### 写法自检 (落盘 / 发帖前)

```
check_bare_issue_refs.py  RESULT.md / PREDICTION.md / SCORES.md / issue 草稿  → 裸 issue 引用: 0, rc=0
§4.5 自查命令                                                                → 无输出
chr(0xFFFD) 计数                                                             → 四个文件均 0
```

RESULT.md 回填单号与裁定后复跑 `check_bare_issue_refs.py` → rc=0。评分员写的 15 份 `GRADER_CRITIQUE.md` (13 个主样本 + eval 5 两次复跑) 同样是新文字, 自检发现 5 份共 8 处裸引用 (号 195 / 199 / 206, 均指本仓, 原文缺 `10CG/Aria` 前缀) → 主控机械补成 `10CG/Aria#N`, 评分判断一字未改 → 复跑 `裸 issue 引用: 0`; §4.5 扫结果目录全部 78 份 md 零命中。另对结果目录 283 个文件做凭据形态扫描 (只报键名与长度, 不读值): 零命中, `FORGEJO_TOKEN` 等出现处全部是变量名。

### substitute 证据保留

`metadata.rule6_note` 所列 TASK-007 RED / TASK-015..018 与 TASK-035 三步法反事实 / TASK-021 全绿**原样保留**, 未因跑了 AB 削减。

### 附带发现 (未开单, 见 RESULT.md §6)

主仓 `VERSION` 子模块表 aria 行仍为 `v1.73.0` (实际 1.73.3, 自 `6a7ab16` 起未同步, 无 check 覆盖); `aria/README*.md` Skill 列表漏 `issue-triage` / `session-closer`。与本 spec 无关, 是否开单请 owner 另定。

### 退出 NO_PUSH 会话

本节提交后本进程退出。**TASK-027 起在不带 `ARIA_COORDINATION_NO_PUSH` 的新会话执行**, 该会话须在 2026-09-28T12:35Z 之前先刷两条 claim 心跳 (`--heartbeat-only`)。

### 本节提交自身

结果目录与本台账在主仓 feature 分支提交 (只 add 本任务交付物); 提交 SHA 见本会话回复 (自指排除)。**未推送** —— 本会话无推送授权, 随本轨下一次推送一并发出。

## 会话入口 (2026-09-27 第二段, 普通会话)

> 同一对话在 TASK-026 之后由 owner 以**不带** `ARIA_COORDINATION_NO_PUSH` 的新进程续上。

- **变量核验 (18:11:41Z)**: `ARIA_COORDINATION_NO_PUSH` 未设; 子进程 `no_push_requested_by_env()` → `False`。
- **远端现状**: 主仓 master 三处 (本地 / origin / github) 均 `c454e35`; 主仓 feature 远端 `4f91772` (本地多一个未推的 `be91134`, 即 TASK-026 提交); 协调 ref 上 active claim 只有本容器这两条。
- **心跳** (owner 2026-09-17 免逐次授权, 前提 = 本地协调 ref 与 origin 一致): 前置检查 `coord_ref_precheck` (代码取自 `pre-merge-completeness-gate-change-scope` 计划 metadata) → `{"verdict": "ok", "local_ahead": 0}` 退出 0 → 强制对齐退出 0 → `phase1_gate.py --heartbeat-only` 两次 (`--phase` 在该模式下不被读取, `heartbeat_by_track` 只写 `heartbeat_at`) → 推后独立核验。

| claim | track | 刷新前 `heartbeat_at` | 刷新后 | outcome / push_success | 推后 `ls-remote origin` 与本地 |
|---|---|---|---|---|---|
| `s-48ca@0612` | 本轨 (phase B) | `2026-09-27T12:35:55Z` (约 5.6h) | `2026-09-27T18:14:01Z` | refreshed / true | `4ae229e` MATCH |
| `s-73b9@1606` | `pre-merge-completeness-gate-change-scope` (phase A.2) | `2026-09-27T12:36:25Z` (约 5.6h) | `2026-09-27T18:14:11Z` | refreshed / true | `4ae229e` MATCH |

刷新后两条 claim 的 `phase` / `status` 未变 (B / A.2, active)。下一次最晚 2026-09-28T18:14Z 前刷新。

## TASK-027 — aria 侧版本 bump + CHANGELOG 三段 (parent 5.1), 并入 standards `session-handoff.md` 升 1.4.0

### 第 1 条 — 取号 (18:15:14Z)

| 输入 | 实测 |
|---|---|
| `aria/.claude-plugin/plugin.json` | `1.73.3` |
| `git -C aria ls-remote --tags origin` | 最高 `v1.73.3`, `v1.74.*` 0 条 |
| `git -C aria ls-remote --tags github` | 最高 `v1.73.3`, `v1.74.*` 0 条 |
| 并发轨 `10CG/Aria#199` 最新 handoff (`2026-09-24-session-close-199-post-planning-converged.md`) 与其计划 | 无具体 `<vNEXT>`, 计划全程用占位 `v<vNEXT>` 执行时现取, 且该轨 B.1 排在本轨 C.2 之后 ⇒ 无预留号冲突 |

⇒ minor + 1、patch 归 0 ⇒ **vNEXT = `1.74.0`**。级别 MINOR 依据: `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` §2 第 6 行。

### 第 2 条 — 取号时 aria `origin/master`

`git -C aria ls-remote origin refs/heads/master` = `1cb387218935433312fde4067c276754b77686a8` (github 同值)。TASK-029 据此判断取号之后远端是否前进。

### 第 3 条 — 写法先例定位

`grep -n "^## \[1.70.0\]" aria/CHANGELOG.md` → `:200`; `### Fixed` `:202` / `### Added` `:209` / `### Changed` `:215` —— 与 A.2 实测一致, 未移位。另参照最近一次 MINOR `[1.73.0]` 的 `### Notes` 节写法 (Rule #6 结论落在 Notes)。

### 第 4 ~ 7 条 — CHANGELOG `[1.74.0]` 三段 (逐条对 `b181678` 真代码核过)

- **Fixed 三条**: 子目录 (四个拼路径点, 含 `scan.py` 的 `_same_branch_head_unreachable_tracks`) / 非 ASCII (**条件式**: 「枚举不再依赖 `core.quotePath`; 默认 true 时此前被转义并在 `.md` 过滤处丢弃; 设为 false 的采用方此前不受影响」) / 假 legacy (`git show` 失败不再追加伪造行, 改计 `unreadable_count`)。
- **Added**: `tracks[].rel_path` (恒存在; 真 track 与 legacy 两处 `tracks.append` 都写入, 已核) / `unreadable_count` (恒存在, 默认 0; 分支枚举失败早退 dict 含该键, 已核) / `write_latest_md` 的 `degraded_reason` (三支恒存在, 取值 `None` / `"missing_filename"` / `"target_in_subdir"`, 已核) / 两个新 kind `handoff_multibranch_unexpected_path_prefix` 与 `handoff_multibranch_undecodable_path` (两处都是 `error_messages.append` + `r.soft_error` 双通道, 已核) / 新测试文件 22 条 (`grep -c '    def test_'` 实测 22) + 平铺基线夹具。
- **Changed 七条**: `legacy_count` 收窄 / `collision.kind` 可由 `none` 翻 `cross_owner` (含 `identity_advisories` 只增不减) / 顶层 `errors[]` 可新增 `snapshot_self_contradiction` 与 `snapshot_consistency_inconclusive` (两个 kind 名在 `scan.py:271` / `:285` 实读核过) / 排序键第 5 级 `(rel_path == filename, rel_path)` 与 legacy track_id 公式改用 `rel_path` / 子目录目标写降级页 (`action` 仍为 `pointer`) / 触碰文档面逐个点名 (standards `session-handoff.md` 标 **Amended**, 与 standards `11b0a14` 实际写法一致) / 已知边界**五条** (非 ASCII 只覆盖可解码 UTF-8 且为条件式 / 不可解码名跳过并报 kind、不计入 `unreadable_count` / `reference-snapshot-aria.json` 未重采样 —— 实读该夹具最后改动于 2026-07-19 `50bbf64`, 本 cycle 零 diff, 其 `tracks_multibranch` 无 `rel_path` 与 `unreadable_count` / `n_active` 可由 1 翻到 ≥2 / mv 过的无 frontmatter 件仍取 mv 提交日且不加 `--follow` —— `_get_file_commit_date` 实读确为 `git log -1 --format=%aI` 不带 `--follow`)。
- **Notes**: 读侧遗留缺口 `10CG/aria-plugin#204` / 平铺仓零行为变化 / Rule #6 AB 结论与 `10CG/aria-plugin#205` / 测试数 (1627 = 1605 + 22; pytest 腿 28 + 11, 取自本台账 TASK-021)。
- **写法自检** (只抽本次新增文字: CHANGELOG `[1.74.0]` 整段 + VERSION 新发布日期行 + standards 新 Version 行): `check_bare_issue_refs.py` 三份均 `裸 issue 引用: 0`; §4.5 自查命令无输出; 六个 aria 文件与 standards 文件 NUL 与 U+FFFD 计数均 0。整文件不跑 —— 存量文字会让它恒红 (content-integrity §4.4 执行口径)。

### 第 8 条 — aria 提交 (**六个文件, owner 当场裁定**)

执行时实读发现 `aria/README.zh.md` 第 5 行同样带版本号, 且 v1.73.1 / .2 / .3 三次发版提交 (`44f00d1` / `189240f` / `9003a82`) 都同改了它。经 AskUserQuestion 呈 owner, 原文 (选项): **「带上, 6 个文件一次提交 (推荐)」** ⇒ verification 末条字面「恰含这五个文件」**不成立**, 记入 `tasks.md` AI 流程判断清单第 34 条。另: `aria/VERSION` 的「## 版本号」代码块在 v1.73.3 发版时漏改、停在 `1.73.2`, 本次一并订正为 `1.74.0` (清单第 35 条, AI 判断请复议)。

```
$ git -C aria show --stat HEAD
1ad31fa981175d8afe8cebb378235b4cab615d58
chore(release): v1.73.3 → v1.74.0 — handoff_multibranch 路径保真 (10CG/Aria#195)
 .claude-plugin/marketplace.json |  4 ++--
 .claude-plugin/plugin.json      |  2 +-
 CHANGELOG.md                    | 34 ++++++++++++++++++++++++++++++++++
 README.md                       |  2 +-
 README.zh.md                    |  2 +-
 VERSION                         |  7 ++++---
 6 files changed, 43 insertions(+), 8 deletions(-)
```

版本取值一致: `plugin.json` `1.74.0` · `marketplace.json` 两处 `1.74.0` · `VERSION` 头部与代码块 `1.74.0` · `README.md` 与 `README.zh.md` 第 5 行 `1.74.0` · CHANGELOG 标题 `[1.74.0]`。发布日期写 2026-09-27; 若 TASK-029 打 tag 时已跨日, 届时照实改日期并记台账。提交不加 `Co-Authored-By` (owner 2026-09-27 裁定)。

### 并入项 — standards `session-handoff.md` 升 1.4.0 (决策单第 1 项)

头部 Version 行改为 1.4.0, 括号内逐条列出三次增量: `d217ed0` (§2.3.1 / §2.3.5 / §2.3.9, `10CG/Aria#193`) · `21748d4` (§2.3.8.1) · `11b0a14` + `d86fc91` (§2.3 第三态, `10CG/Aria#195`)。引用前核过 SHA: `d217ed0` 与 `21748d4` 是这两次改动落到 standards master 首父链上的提交 (分支内原提交 `c955783` / `bb5d375` 分别是它们的祖先), 与 `10CG/aria-standards#20` 的引用一致; §2.3.9 与 §2.3.8.1 两个标题在文件中实读存在。

```
$ git -C standards show --stat HEAD
56306d107f094d37d8f79d3311c962cebf8afcc8
docs(conventions): session-handoff Version 1.3.0 → 1.4.0 — 补齐三次增量 (10CG/aria-standards#20)
 conventions/session-handoff.md | 2 +-
```

记入 `tasks.md` AI 流程判断清单第 33 条。合并后回帖关闭 `10CG/aria-standards#20` —— 届时另请授权。

### 未推的部分

aria `1ad31fa`、standards `56306d1`、主仓 feature 上的 `be91134` 与本节所在提交均**只在本地**。子模块的推送按计划在 TASK-034 (owner 授权后); 主仓 feature 随 TASK-031 或另获授权的备份推送发出。

## TASK-028 — 引用与编号写法自检 第一次 (parent 5.6, 子模块合并前)

**范围** = 截至本任务的本 cycle diff 新增行; 基线取自 TASK-001 第 7 条: aria `1cb3872` · standards `940cb5b` · 主仓 `a52b5eb` (只限本 Spec 目录, 不含 proposal.md 存量文字 —— 本 cycle 未改 proposal.md)。**导出方式**: scratchpad 脚本解析 `git diff <基线> <终点> -U0` 的新增行, 原样写出, 同时生成「导出行号 → 源文件:行号」索引, 命中据此回溯。检查器以各仓根调用 (`--repo-root=<该仓根>`): aria 与 standards 没有允许清单, 按最严执行; 主仓读 `.aria/bare-issue-ref-allowlist.txt`。本节全部判定只针对导出的新增行, 不以「整份文件 rc 0」为门槛 (§4.4 执行口径)。

| 仓 | 新增行 / 文件数 | 裸引用 (首跑) | 处置 | 复跑 |
|---|---|---|---|---|
| aria | 1481 / 16 | 2 (同在 `VERSION:5`) | 订正, aria 提交 `820ea57` | 0 (对 `820ea57` 重新导出) |
| standards | 5 / 1 | 0 | — | — |
| 主仓 Spec 目录 | 1307 / 2 | 5 (台账 3 行) | 订正, 随本节同一提交 | 0 (对含本节的暂存区重新导出; 本节初稿自身命中 2 处, 见第 1 条) |

**命中明细与处置**:

1. aria `VERSION:5` —— v1.73.3 的说明行, 因 v1.74.0 改号时改标「(旧)」而进入本 cycle diff。其中一处跨仓引用缺 org 段 (所指为 `10CG/aria-plugin#196`); 另一处是描述「单级路径伪装」时用的字面例子 (以 `.md` 结尾的两级路径后接井号与数字, 检查器按设计就会拒它)。按 §4.4「改到哪段顺手改哪段」: 前者补全, 后者改为文字描述。**本节初稿又在这一条里逐字引用了这两个坏形态, 复跑当场命中 2 处, 同样改为文字描述** (与第 4 条同一个坑)。
2. 台账组 2 收口节 (`:626`, 本 cycle 早先写) —— 为说明违规形态而逐字引用了「仓名与号之间带空格、缺 org 段」的写法, 改为文字描述。
3. 台账 TASK-023 节 (`:829`) —— 只写了井号与号、缺 org 与仓名 (所指为 `10CG/aria-standards#20`), 补全。
4. 台账 TASK-026 节 (`:1186`) —— **主控本会话自己写的**: 为说明「补全前的形态」而字面列出三个裸号, 改为文字描述。说明写这类记录时自己同样会踩, 本条是本任务存在的理由的一个实例。

序数假阳性 (`10CG/aria-plugin#199` 那一类) 本次零命中, 没有需要按「不改写措辞规避」保留原样的条目。

**另两项**: §4.5 带圈 / 带框字符 (U+2460–U+24FF / U+2776–U+2793 / U+3251–U+325F / U+32B1–U+32BF) 三份导出均 0; 字面 U+FFFD 三份导出均 0 行。

**工作树**: 订正提交后 aria / standards 的 `status --porcelain` 均为 0 行 (TASK-029 第 4 步前提)。**勾选**: 本任务完成即满足 `tasks.md` 5.6 的勾选条件, 勾选动作按计划留到 TASK-032 一次完成。

## TASK-029 — aria 与 standards: 本地 merge + aria tag + 合并树回归 (parent 5.2, 不推送)

### 首次执行 (2026-09-27T18:33Z) —— 停在第 2 步

- **第 1 步**: `git -C aria fetch origin` / `git -C standards fetch origin` 均退出 0。
- **第 2 步 (前半)**: 两仓 `status --porcelain` 均 0 行 (aria feature `820ea57`, standards feature `56306d1`)。
- **第 2 步 (后半, standards 占位核验) 按字面不成立**, 原样输出 (内容取自 `git -C standards show <feature>:conventions/session-handoff.md`, 同时对回填前的 `11b0a14` 跑一遍作自然负控):

```
[56306d1] 定位串按判据字面 (不带反引号)            : 窗口数 = 0
[56306d1] 定位串按文件实际写法 (带反引号)          : 窗口数 = 2 (行 97, 176)
    窗口@97 : #< 计数 = 0 · 含 10CG/aria-plugin#<n> = False
    窗口@176: #< 计数 = 0 · 含 10CG/aria-plugin#<n> = True
[11b0a14] 定位串按文件实际写法                      : 窗口数 = 2 (行 97, 176)
    窗口@97 : #< 计数 = 0 · 含 10CG/aria-plugin#<n> = False
    窗口@176: #< 计数 = 0 · 含 10CG/aria-plugin#<n> = False · 含「已知缺口, 尚未开跟踪 issue」= True
```

  **不成立的原因在判据本身, 两处**: (1) 定位串写成不带反引号, 文件里是带反引号的写法, 字面命中 0 处; (2) 判据要求两个窗口都含 `10CG/aria-plugin#<n>`, 而 TASK-023 自己的 verification 只要求在 `:171-173` 那节写跟踪指针、`:97` 只补限定从句 (本台账 TASK-023 节同样只记了一处指针) ⇒ `:97` 窗口在任何版本都不会含。另: 计划设想的自然负控「回填前 `#<` 计数非 0」也不存在 —— TASK-023 落笔时用的是回落措辞而非 `#<` 占位 (该节已记为 AI 流程判断)。**实质**: 两窗口 `#<` 均为 0; 指针所在窗口在当前提交含 `10CG/aria-plugin#204`、在回填前 `11b0a14` 不含, 该条件的自然负控有效。
- 按 `metadata.owner_gates` 第 9 项停在本步上报。**owner 裁定 (2026-09-28, AskUserQuestion)** 原文 (选项): **「按实质判通过, 重走后继续 (推荐)」** —— 选项说明: 「认定占位已清; 从第 1 步 fetch 重走, 一路做到第 8 步 (本地合并 + 合并树回归 + 打 tag, 不推送)。代价: 第 2 步字面不成立, 原样记台账, 并把『判据与 TASK-023 规定矛盾』写进 AI 流程判断清单请复议; 计划文件 detailed-tasks.yaml 不改。」 ⇒ 记入 `tasks.md` 清单第 36 条。

### 两次执行之间: 跨 UTC 日, 发布日期订正

owner 裁定到达时已是 2026-09-28T01:47Z (距首次执行约 7 小时)。按 TASK-027 节预设的「打 tag 时已跨日则照实改日期」: aria feature 提交 **`651ff6e`** —— CHANGELOG `[1.74.0]` 标题 / VERSION 发布日期行 / `README.md` / `README.zh.md` 四处发布日期 2026-09-27 → 2026-09-28 (事实性日期如「owner 2026-09-27 裁放行」与结果目录名不动); 新增 4 行裸引用自检 0。重走前并发核查: 主仓 master 本地 / origin / github 均 `c454e35`, 协调 ref 本地 = origin = `4ae229e`, 无他方推进。

### 重走 (2026-09-28T01:48:22Z 起, 从第 1 步)

- **第 1 步**: 两仓 fetch 均退出 0。
- **第 2 步**: porcelain 两仓 0 行 (aria feature `651ff6e07d14498474f6a19068883a495e902433`, standards feature `56306d107f094d37d8f79d3311c962cebf8afcc8`); 占位核验输出与首次一致 (按 owner 裁定判通过)。
- **第 3 步**: 两仓 `checkout master` 后 `master == origin/master`, 均 **EQUAL**, 无需 ff-only —— aria `1cb387218935433312fde4067c276754b77686a8` · standards `940cb5b4b8672ea56606c4c3ed6157e84949fa4a`; porcelain 均 0。aria CHANGELOG 版本号集合 (`git -C aria show master:CHANGELOG.md | grep -oE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' | sort -u`) = **138 条**, 集合文件 sha256 `988bda63af410461a130eb1eb0472866dc7c81d0b19fc1e6117cf81dabf1085e` (由 `1cb3872` 的 CHANGELOG 确定性导出, 可复算)。
- **第 4 步 取号复核**: aria `origin/master` = `1cb3872` = TASK-027 取号时记录值 ⇒ 未前进, 通过。
- **第 5 步 本地合并** (`--no-ff`, 不在服务端合并): 两仓退出码 0, 正向断言全部成立 ——

```
[aria]      HEAD = 5215cf20c467535ca9cdcea2b1ecf34f94887732
            HEAD != 第 3 步 SHA: yes · HEAD^1 == 1cb3872: yes · HEAD^2 == feature 651ff6e: yes · porcelain = 0
[standards] HEAD = 2bc1c4c619c5125a1bb2963864c1683fd9a87739
            HEAD != 第 3 步 SHA: yes · HEAD^1 == 940cb5b: yes · HEAD^2 == feature 56306d1: yes · porcelain = 0
```

- **第 6 步 取号终核**: 合并树七处取值均 `1.74.0` (`plugin.json` · `marketplace.json` 两处 · VERSION 头部与「## 版本号」代码块 · `README.md` · `README.zh.md`), CHANGELOG 标题 `## [1.74.0] - 2026-09-28`; 集合判据 `comm -23 <第 3 步集合> <合并树集合>` 输出 **0 行** (合并树集合 139 条 = 138 + 1); `git -C aria ls-remote --tags origin` 与 `github` 均退出 0, `v1.74.0` 命中均 0。
- **第 7 步 合并树回归** (前提: aria porcelain 0 且 HEAD = `5215cf2`, 执行前后各核一次; 01:50:29Z – 01:54:17Z):

```
(a) python3 -B aria/skills/state-scanner/tests/run_tests.py      → Ran 1627 tests in 225.285s · OK · rc 0
(b) pytest -q -p no:cacheprovider tests/test_collision.py        → 28 passed
    pytest -q -p no:cacheprovider tests/   (phase-d-closer)      → 11 passed
(c) metadata.sc11_baseline_predicates 全部谓词                    → parsed 19 / PASS 19 / FAIL 0
```

  Ran 数与 TASK-021 的 1627 相同, 差值 0 —— B.1 以来 aria `origin/master` 无新提交, fetch 没有带进并发提交。谓词执行器是本会话重写的 (TASK-021 当时的脚本在旧会话 scratchpad, 已不存在): 按「`(标签) <谓词>`」逐行解析, 以声明的执行形态 `if <谓词>; then echo PASS; else echo FAIL; fi` 在 `aria/skills/state-scanner` 下执行, 并断言恰好解析出 19 条且标签序列与 TASK-021 记录一致, 否则中止 (防 TASK-021 记过的「解析 0 条仍报全真」)。**执行器负控**: 在 scratchpad 建 `1cb3872` 的临时 worktree 跑同一执行器 → **PASS 0 / FAIL 19** (与 TASK-001 第 10 条的基线全 FAIL 一致), 该 worktree 随即 `worktree remove`, `worktree list` 只剩主工作树。
- **第 8 步 打 tag**: 回归通过后在 `5215cf2` 上打附注 tag —— `v1.74.0` (tag 对象 `f951d1ec87aa1c57de1964b8673c1afa9862b281` → `5215cf20c467535ca9cdcea2b1ecf34f94887732`)。
- 重走结束 01:54:54Z。合并提交与 tag 均未带 `Co-Authored-By`。

### 未推的部分

aria master `5215cf2` + tag `v1.74.0`、standards master `2bc1c4c`、两仓 feature 分支上的本 cycle 提交、主仓 feature 上的本节所在提交及其前三个, 全部**只在本地**。子模块双推属 TASK-034 (`metadata.owner_gates` 第 10 项, 需 owner 授权); 主仓 gitlink 在 TASK-034 两个远端都核验一致之前不得 bump (清单第 32 条)。

## TASK-034 — aria 与 standards 双推 + 逐 remote 核验 (parent 5.2)

**授权**: owner 2026-09-28 经 AskUserQuestion 答「授权按计划双推 (推荐)」—— 问题原文列明了四条推送的写法与方向 (aria `git push --atomic <remote> master refs/tags/v1.74.0`, master `1cb3872` → `5215cf2`; standards `git push <remote> master`, `940cb5b` → `2bc1c4c`; 各对 origin 与 github 先后推一次, 被拒或只推成一端即停下上报、不 force)。

**推前核验 (02:00:17Z)**:

```
aria      origin: ls-remote --tags rc=0, v1.74.0 命中 0 · master = 1cb387218935433312fde4067c276754b77686a8
aria      github: ls-remote --tags rc=0, v1.74.0 命中 0 · master = 1cb387218935433312fde4067c276754b77686a8
standards origin: master = 940cb5b4b8672ea56606c4c3ed6157e84949fa4a
standards github: master = 940cb5b4b8672ea56606c4c3ed6157e84949fa4a
```

两仓远端 master 均等于 TASK-029 第 3 步记下的值 ⇒ 四条推送都是快进。

**推送** (每条单独执行, 超时 360 秒, 先 origin 后 github; 禁 `--follow-tags` 与非原子多 ref 推送):

```
git -C aria push --atomic origin master refs/tags/v1.74.0   → 1cb3872..5215cf2 master -> master · [new tag] v1.74.0 · rc 0
git -C aria push --atomic github master refs/tags/v1.74.0   → 1cb3872..5215cf2 master -> master · [new tag] v1.74.0 · rc 0
git -C standards push origin master                          → 940cb5b..2bc1c4c master -> master · rc 0
git -C standards push github master                          → 940cb5b..2bc1c4c master -> master · rc 0
```

**推后逐 remote 独立核验** (不信回执, 硬约束 2; `ls-remote` 带三次重试):

```
本地: aria master 5215cf20c467535ca9cdcea2b1ecf34f94887732 · tag v1.74.0 f951d1ec87aa1c57de1964b8673c1afa9862b281 · tag^{} 5215cf20c467535ca9cdcea2b1ecf34f94887732
      standards master 2bc1c4c619c5125a1bb2963864c1683fd9a87739
[origin] aria master MATCH · tag MATCH · tag^{} MATCH · standards master MATCH
[github] aria master MATCH · tag MATCH · tag^{} MATCH · standards master MATCH
```

⇒ 两个远端都核验一致, 满足 TASK-030 bump 主仓 gitlink 的前置 (清单第 32 条)。

### 主仓 feature 分支备份双推 (owner 同一次 AskUserQuestion 授权)

原文 (选项): **「现在备份双推」** —— 范围: 只推主仓 feature 分支, 快进 `4f91772` → `877ed17` (含 TASK-026 AB 结果提交 `be91134` 与 TASK-027 / 028 / 029 三个台账提交)。推前两端均为 `4f91772` 且是本地祖先; 两条推送分开执行、均退出 0; 推后逐 remote `ls-remote`:

```
[origin] 877ed17d0227a95442118f8afd9df0bf5d700ce5 MATCH
[github] 877ed17d0227a95442118f8afd9df0bf5d700ce5 MATCH
```

所推 tip 上的 gitlink 仍为 aria `1cb3872` / standards `940cb5b` (两端均可达), 无孤立 gitlink。**本节所在的台账提交不在该授权范围内, 写作时未推送**, 随下一次授权的推送发出。

## TASK-030 — 主仓发布同步面: 两个 gitlink + 16 个版本点 + custom checks 复跑 (parent 5.1)

**前置**: TASK-034 已对 origin 与 github 各自 `ls-remote` 核验一致 (两个子模块的 master, aria 另含 tag 对象与其指向) ⇒ 满足清单第 32 条, 可以 bump。

**gitlink** (动手时实测 `git ls-tree HEAD aria standards` 起步, 只前进不回退):

```
aria:      1cb387218935433312fde4067c276754b77686a8 → 5215cf20c467535ca9cdcea2b1ecf34f94887732 · 祖先关系成立 · = 本地 master = origin/master = github/master
standards: 940cb5b4b8672ea56606c4c3ed6157e84949fa4a → 2bc1c4c619c5125a1bb2963864c1683fd9a87739 · 祖先关系成立 · = 本地 master = origin/master = github/master
```

**16 个版本点** (动手前逐处 `grep -n` 实测, 按行精确替换, 每行断言恰含一处旧号):

| 点 | 位置 (实测) | 改前 → 改后 |
|---|---|---|
| 1 | `README.md:8` badge | 1.73.3 → 1.74.0 |
| 2 | `README.md:242` Plugin Version 行 | 1.73.3 → 1.74.0 |
| 3-5 | `README.zh.md` / `README.ja.md` / `README.ko.md` `:3` translated-from 标记 | v1.73.3 → v1.74.0 |
| 6-8 | 同三份 `:10` badge | 1.73.3 → 1.74.0 |
| 9-11 | 同三份 `:244` Plugin Version 行 | 1.73.3 → 1.74.0 |
| 12 | `VERSION:24` 子模块表 aria 行 | **v1.73.0** → v1.74.0 (直接写新号; 该行自 v1.73.0 起三次发版漏改, 本 cycle AB 的两个臂也各自独立发现过) |
| 13-14 | `CLAUDE.md:138` 方法论轨版本区间尾 / `CLAUDE.md:142`「版本:」行 | 1.73.3 → 1.74.0 (计划写 `:139` / `:141`, 实测已漂到 `:138` / `:142`) |
| 15 | `docs/architecture/system-architecture.md:189` | 1.73.3 → 1.74.0 |
| 16 | `docs/architecture/version-scheme.md:23` | 1.73.3 → 1.74.0 |

改后复验: 八个文件中 `1.73.3` 残留 0 处, `1.74.0` 恰 16 处, 均等于 `aria/.claude-plugin/plugin.json` 的 `1.74.0`。模板对照: 上次发版的主仓同步提交 `1b9734a` 改的是同样 15 处 (不含 `VERSION:24`)。

**custom checks 复跑** (`scan.py` 输出写 scratchpad, 退出 0):

```
m6-version-badge-match             pass  OK badge=1.74.0
i18n-readme-translation-currency   pass  OK (3 i18n READMEs current @ 1.74.0)
plugin-version-arch-docs-match     pass  OK plugin=1.74.0 (2 arch doc rows match)
main-project-version-consistency   pass  OK 主项目版本 1.7.5 — 9 个引用点全部一致
plugin-cache-currency              fail  STALE installed=1.73.3 (scope=user) sot=1.74.0   ← 预期, 待 owner 更新本机插件
```

其余 11 条 custom check 均 pass (共 16 条, 15 pass / 1 预期 STALE)。

**提交**: 主仓 feature **`a99dd8d`** —— 只 add 本任务 deliverables (`aria` / `standards` 两个 gitlink + `VERSION` / `README.md` / 三份 i18n README / `CLAUDE.md` / 两份架构文档), `git diff --cached --stat` 恰 10 个路径; 提交后主仓工作树干净。本节所在的台账提交与 `a99dd8d` 均**未推送**, 随 TASK-031 的推送发出。

## TASK-031 — 主仓 PR + pre-merge gate + 合并 + 双端核验 (parent 5.2)

### 开 PR 前 (2026-09-28T02:10Z)

- **提交面 (有范围的检查)**: TASK-034 / 030 两节台账已先行提交 (`ab200c6` / `9b4a291`), 其后不带路径的 `git status --porcelain` 原样输出为**空 (0 行)** —— 主仓此刻没有任何未跟踪或未提交文件, 自然不存在触及本 cycle 交付物路径的行, 也没有需要逐条判归属的他轨文件。
- **已跟踪核验**: `git ls-files aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6` → **284 个文件** (结果目录顶层 `PREDICTION.md` / `RESULT.md` / `SCORES.md`, `dispatch/` 5 个, `tools/score.py`, 其余在 `state-scanner/runs/` 下); `git ls-files openspec/changes/handoff-multibranch-subdir-path-fidelity/verification-ledger.md` → 在册。
- **同步 `origin/master`** (merge 不 rebase, 覆盖 phase-c-integrator C.2.1 的 sync rebase 默认): feature 落后 master 12 个提交 (`35700fc` … `c454e35`, 全是 handoff / 决策单 / 执笔报告落仓 / `.aria/state-checks.yaml` 的 Level 1 修复), 其改动路径与本 cycle 交付物**零交集**。`git fetch origin` 后 `git merge --no-ff --no-edit origin/master` 退出 0 → 合并提交 **`0d24604`** (父 `9b4a291` + `c454e35`), 工作树干净, 两个 gitlink 仍为 `5215cf2` / `2bc1c4c`。
- **写法自检 (PR diff 新增行)**: PR diff 取 `c454e35..HEAD` 的净变化 (同步合并后与 PR 的实际 diff 一致; 覆盖 TASK-030 同步面文字与 TASK-001 起点 `a52b5eb` 以来本 cycle 的全部主仓新增行) = **652636 行 / 244 个文件**。`check_bare_issue_refs.py --repo-root=.` 命中 **1403** 处, **全部**位于 AB 结果目录的 `state-scanner/runs/` 下: `state-snapshot.json` 1144 (scan.py 机器输出里的 issue 标题等) · `answer.md` 240 (被评的臂回答) · `grading.json` 14 (评分证据引文) · `exec_notes.md` 3 · `prompt.txt` 1 与 `eval_metadata.json` 1 (从固定套件原样复制的题面)。作者手写文字 (台账 / `tasks.md` / `RESULT.md` / `PREDICTION.md` / `SCORES.md` / `dispatch/` / TASK-030 同步面 / 评分员写的 `GRADER_CRITIQUE.md`) **零命中**。评测原始产出是证据, 改写即篡改证据, 按 §4.4 / §4.5 执行口径 (存量与夹具不做回改) 不动。§4.5 字符与字面 U+FFFD 在全部新增行中均为 0。**PR 正文** (scratchpad 草稿) 单独自检: 裸引用 0 · §4.5 字符 0 · U+FFFD 0; 按 `standards/conventions/git-commit.md` §8.1 不加 AI 署名行。

### 授权与推送 feature

owner 2026-09-28 经 AskUserQuestion 答「授权全部五项 (推荐)」—— 问题原文列明: (1) feature 快进双推 (`877ed17` → `6fdff9f`); (2) Forgejo 开 PR; (3) 跑 C.2.4 与 C.2.4.5, 只有 green / PASS 才合并; (4) 以 merge commit 合并, 不 squash; (5) 本地 master 快进后先核 aria-orchestrator 无待推内容, 再由 C.2.5 推 github 并做 parity。任一推送被拒、闸门非 green、或只推成一端即停下上报, 不 force。

- feature 推前两端均为 `877ed17` 且为本地祖先; `git push origin` / `git push github` 分开执行、均退出 0; 推后 `ls-remote` 两端均 `6fdff9f27f3bee8e34d6af59e041f078d5676f93` MATCH。

### PR 与两道闸

- 开 PR 前按 head 分支查重: 该分支无任何既有 PR。POST 返回 **`10CG/Aria#222`** (open, base `master`, head `6fdff9f`, mergeable); 独立 GET 核验标题与正文逐字一致。正文不加 AI 署名行 (`git-commit.md` §8.1)。
- **C.2.4 pre-merge gate** (07:41:29Z, `pre_merge_gate.py --pr-branch feature/handoff-multibranch-subdir-path-fidelity --main-branch master --remote origin`, 退出 0):

```
verdict: green · pr_ci_status: not_applicable · in_flight_runs: [] · primitive_used: aether-ci-cli · gate_error: None
path_coverage: decision=not_applicable · workflows_scanned=3 · matched_workflows=[] · changed_files_count=296 · reason=no-triggering-paths
```

  green 来源为 `not_applicable`, 按 SKILL 的 surface 义务已在会话中原样呈报警告行:「C.2.4: 变更路径无 CI workflow 覆盖, PR CI wait 已跳过 (not_applicable), main in-flight 已核」。
- **C.2.4.5 子模块指针闸** (`ARIA_PR_NUMBER=222 submodule_gate.sh`, 退出 0, mode=block): `standards forward bump` PASS · `aria forward bump` PASS · `aria-orchestrator unchanged (237045a)`。

### 合并与本地快进

- 合并前复核: `origin/master` 仍为 `c454e35` (与同步基点相同), PR `mergeable: true`。POST `pulls/222/merge` (`Do: merge`, 合并标题照 `10CG/Aria#215` 的格式显式给出, 消息体留空) → GET: `merged: true`, **`merge_commit_sha` = `03f97ac531b23d468ad468223a8bc0f818fdb79f`**, `merged_at` 2026-09-28T07:43:06Z。
- `git fetch origin` → `git checkout master` → `git merge --ff-only origin/master`: 本地 master `c454e35` → `03f97ac`, 断言 HEAD 等于合并回执 SHA 成立; 父为 `c454e35` + `6fdff9f`; 工作树干净; master 上的 gitlink 为 aria `5215cf2` / standards `2bc1c4c`。
- **台账所记主仓 SHA 的祖先核验** (`merge-base --is-ancestor <sha> origin/master`): 台账中反引号包裹的 63 个十六进制串里, 能在主仓解析为提交的 22 个中 **17 个是 `origin/master` 的祖先** (本 cycle 全部主仓分支提交); 其余 5 个 (`e911132` / `4ae229e` / `82adeb0` / `ae24f81` / `ad0287f`) 是协调 ref 上的 claim 提交, 本就不在 master 上; 另 35 个是子模块对象, 6 个不是提交 (审计 finding 号、容器 id、哈希摘要)。

### C.2.5 多远程推送

**五项事实** (执行前核对): (1) `.aria/config.json` 无 `phase_c_integrator.multi_remote_push` 覆盖, 也无顶层 `multi_remote` ⇒ 取 `config-loader/DEFAULTS.json` 默认 `enabled: true`; (2) 技能级 `enforced_remotes: null` 继承顶层 `[]` ⇒ 自动发现主仓全部 remote (`github` / `origin`); (3) `fail_on_partial_push: true` (默认); (4) `read_only_remotes: []` (默认); (5) `test -f aria/skills/git-remote-helper/SKILL.md` 成立 ⇒ 不走内联降级。

**aria-orchestrator 前置断言**: fetch origin 与 github 后, 在 `master` 分支上 (本次实测非 detached), HEAD = 本地 master = `origin/master` = `github/master` = `237045ac2cfed9849c201e18434e9f6cb9036ab5`, `rev-list --left-right --count origin/master...HEAD` = `0 0`, 工作树干净 ⇒ 无待推内容, 可以调 C.2.5。

**per-remote 矩阵** (07:45:10Z 起; `expected_sha` = 本地 master `03f97ac`; 子模块与主仓均经 `push_all_remotes.sh`, 主仓推后经 `verify_post_push.py --max-retries=3 --initial-backoff=2 --timeout=15`):

```
origin: aria ✅ (5215cf2, 已同步) · standards ✅ (2bc1c4c) · aria-orchestrator ✅ (237045a) · main ✅ (03f97ac → 03f97ac, 服务端合并已在) · verify match=true (attempts 1)
github: aria ✅ (5215cf2, 已同步) · standards ✅ (2bc1c4c) · aria-orchestrator ✅ (237045a) · main ✅ (c454e35 → 03f97ac)                     · verify match=true (attempts 1)
```

两个 remote 均全部成功且 parity `match: true`。

### 事后核

`scan.py` (输出写 scratchpad, 退出 0): `sync_status.multi_remote.overall_parity: true` · `has_pending_push: false` · `has_unreachable_remote: false` · `gitlink_integrity` 六组 (三个子模块 × 两个 remote) 全部 `ok`。

## TASK-032 — Phase D (parent 5.4)

### 第 1 步 — 本地 master 对齐 (07:48:57Z)

`git fetch origin` → `git checkout master` → `git merge --ff-only origin/master` 输出 `Already up to date.`, 退出 0; HEAD = `origin/master` = `03f97ac`; `git merge-base --is-ancestor 03f97ac HEAD` 成立; 工作树干净。

### 第 2 步 — `tasks.md` 一次性勾选

27 行 checkbox 由主控在本步一次勾完 (勾前 26 行未勾 + 2.0 行已勾; 勾后 27 / 27)。5.4 与 5.6 按清单第 15 条在其子步骤完成前勾选。5.5 行的父目录 token `aria-plugin-benchmarks/ab-results/` 已整个替换为本次结果目录全路径 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/` (目录实测存在); 该行此后只剩这一个含 `ab-results` 的路径, 无 `ab-suite` 路径。

### 第 3 步 — 归档门只读预演

`python3 -B aria/skills/state-scanner/scripts/lib/spec_complete.py --gate openspec/changes/handoff-multibranch-subdir-path-fidelity` 退出 0:

```
complete = True  (tasks.md 全 [x] (27 task(s), 无 carry-forward/defer 注释))
verdict  = warn · blocking_reasons = [] · soft_errors = []
unverified_claims = 3:
  2.2 行  reason: symbol 'HEALTHY_TRACKS' unclassified reference form
          (warnings: no Python definition for 'HEALTHY_TRACKS' — not code, cannot be dead-code → warn)
  4.4 行  reason: no extractable symbol (fail-soft)
  4.3 行  reason: dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在
d_payload: spec_id = handoff-multibranch-subdir-path-fidelity · deferred_items = [] · unverified_claims = 上面三条
```

与计划预判完全一致 (三类均属检查器假阳性; 未为过检查器改写 `tasks.md` 措辞)。查重 (标识符类检索词, `state=all`): 第 1 类落在 `10CG/Aria#192` (open) 重定范围后写明的「抽取层把非生产代码词当候选符号」同一条 fail-toward-warn 分支上; 第 3 类即 `10CG/aria-plugin#114` (open); 第 2 类未见覆盖。

### 第 4 步 — owner 裁定 (2026-09-28, 同一次 AskUserQuestion 的四个问题)

| 问题 | owner 所选 (原文) |
|---|---|
| Step 7 建不建 [Archive Tracker] issue | **「不建 (推荐)」** —— 选项说明: 归档只执行 Step 1-6; 三条都不是真待办, 建单只会多一张没有可做之事、还得有人去关的 issue; 代价是这三条只留在归档后台账与 handoff 里 |
| 三类检查器假阳性是否另报 `10CG/aria-plugin` | **「只为第 2 类开一张新单 (推荐)」** —— 正文顺带登记另两类的这次新实例并指向 `10CG/Aria#192` / `10CG/aria-plugin#114`, 不在那两张单上另发评论 |
| `10CG/Aria#195` 关闭回帖 | **「授权发帖并关闭 (推荐)」** |
| Phase D 推送 (主仓 master 上的 Phase D 提交双推 + `release_gate` 释放本轨 claim 并推协调 ref) | **「授权两类推送 (推荐)」** |

⇒ openspec-archive 执行 Step 1-6, 停在 Step 7 之前; D.2b / D.3 照常。未建 tracker 的原因: 预演的三条 unverified 全部是已知类别的检查器假阳性, `deferred_items` 为空, 没有真正的遗留待办。

### 第 5 步 — D.2 归档 (openspec-archive Step 1-6; 自本节起写在归档后台账)

- **Step 1**: 已归档前置检查 `ls openspec/archive/ | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}-handoff-multibranch-subdir-path-fidelity$'` 零命中; 正式 `--gate` 输出与第 3 步预演**逐字段相同** (complete=True / verdict=warn / 三条 unverified / 无 `runtime_probe` 键) ⇒ 路由「complete=true ∧ verdict=warn」= 路径 (a) 正常归档 + warn 覆盖层。
- **Step 2**: `proposal.md` 的 Status 改为「Complete (2026-09-28 ship: …)」并保留其后的 Approved 历史 (照 `2026-09-17-rule6-…` 归档先例); 在文件起始插入 frontmatter: `unverified_claims` 三条 (逐条取自 gate 输出, 回读与 gate 输出逐条一致) + `unverified_ack: false` (清单第 46 条); 仓内 `lib/frontmatter_block.py` 的 `_FRONTMATTER_RE` 能取到该块 (11 行), 改后重跑 gate 无 soft_error。
- **Step 3**: 取日期 `TZ=UTC date -u +%Y-%m-%d` = **2026-09-28**; 先 `git add` Step 2 的改动再 `git mv` (防「git mv 带未暂存编辑时提交的是 index 旧内容」); `mkdir -p openspec/archive`; 断言目标不存在后 `git mv openspec/changes/handoff-multibranch-subdir-path-fidelity openspec/archive/2026-09-28-handoff-multibranch-subdir-path-fidelity`, 退出 0。
- **Step 4 五条断言全绿**: 目标存在 · 源已消失 · 无 `openspec/changes/archive/` · 无 `{name}/{name}/` 嵌套 · `proposal.md` 在该层。**Step 6**: 含 `proposal.md` / `tasks.md` / `detailed-tasks.yaml` (另有 `verification-ledger.md` / `sc11-predicate-validation.py`); 暂存区里的 `proposal.md` 以 frontmatter 开头。
- **Step 7 未执行** (owner 2026-09-28 裁「不建」, 原文见第 4 步); 输出字段照实记: `d_issue_created: false` · `d_issue_number: null` · 跳过原因 = owner 裁定 (skill 枚举无此项, 未套用现成值; 清单第 49 条)。
- 归档提交: 主仓 master **`c8238c3`** (5 个文件 rename, 其中 `proposal.md` 带 Step 2 改动)。

### 第 7 步 — D.2b `release_gate` 释放本轨 claim (10:44:33Z)

前置检查 `coord_ref_precheck` → `{"verdict": "ok", "local_ahead": 0}` 退出 0; 强制对齐退出 0 (本地 `07933e5`); 会话未带 `ARIA_COORDINATION_NO_PUSH`。`release_gate.py --raw-track-id handoff-multibranch-subdir-path-fidelity --status done --repo-path /home/dev/Aria` (**不带** `--sweep-stale` / `--gc`, 清单第 47 条) 退出 0:

```
released: success=true · track_id=handoff-multibranch-subdir-path-fidelity · status=done · benign=false
sweep: null · gc: null · fetch_success: true · push_success: true · push_skipped: false · hard_error: null
```

推后独立核验: 本地 = origin = `4d40f8416415faf63ebe5f6eb8bcea9cf0895210` MATCH; `claims/bfe8285d/s-48ca@0612.yaml` 现为 `status: done` (phase B); 全局 active claim 只剩 `claims/bfe8285d/s-73b9@1606.yaml` (`10CG/Aria#199`, 心跳 `2026-09-28T07:52:48Z`)。本步推送属 owner 第 4 步授权的「Phase D 两类推送」。

### 检查器假阳性另报 (owner 第 4 步授权)

查重结论见第 3 步: 第 1 类属 `10CG/Aria#192`, 第 3 类即 `10CG/aria-plugin#114`, 只为第 2 类开单。POST 返回 **`10CG/aria-plugin#206`** (open); 独立 GET 核验标题与正文逐字一致。正文顺带登记另两类的这次新实例并指向那两张单, 未在那两张单上另发评论。发帖前自检: 裸引用 0 · §4.5 字符 0 · U+FFFD 0。

### 第 8 步 — D.3 周期 handoff

- 文件 `docs/handoff/2026-09-28-195-handoff-multibranch-shipped-v1.74.0-archived.md` (同日无重名); `owner-container` 取自 `handoff_autofill.py --owner-container` 的机械值 `simonfish/bfe8285d`; `head -8 | grep -cE '^(track-id|owner-container|phase|status|updated-at):'` = **5**。
- 按本步要求含: `reference-snapshot-aria.json` 未重采样 (附 `10CG/aria-plugin#204`) · standards `session-handoff.md` 已改 (Amended + 1.4.0) —— 对应 SC-11 (d)(h); `tasks.md`「AI 流程判断清单」第 1 ~ 36 条**全文照录** (脚本从归档后的 `tasks.md` 截取原文嵌入, 非手抄) 并追加 Phase B / C / D 新增第 37 ~ 49 条, 每条写「做了什么 + 理由 + 请 owner 复议」; SC-11 矩阵已知边界 (R4 m13) 与三处「文本存在不等于语义正确」(R5) 照录。
- `docs/handoff/latest.md`: 裸 `**Latest**:` 与「Done (this cycle)」改指本周期 handoff (全文裸 `**Latest**:` 仍恰 1 个); banner 的在飞轨描述更新 (本轨终结; `10CG/Aria#199` B.1 入口门第 1 项已满足); track 表本轨一行改为 done 并前插本周期链接 (旧链接保留); 顶部新增一段周期收尾说明。

### 第 9 步 — 写法自检第二次

| 对象 | 裸 issue 引用 | §4.5 字符 | U+FFFD | 其它 |
|---|---|---|---|---|
| 周期 handoff 全文 | 0 | 0 | 0 | NUL 0; 希腊字母 0 (照录的清单原文单独再扫一次: 裸引用 0) |
| `latest.md` 本次新增行 | 0 | — | — | 裸 `**Latest**:` 恰 1 个 |
| `10CG/aria-plugin#206` 正文 | 0 | 0 | 0 | 发帖前 |
| `10CG/Aria#195` 关闭回帖草稿 | 0 | 0 | 0 | 归档日期占位已填, 占位残留 0 |
| 本节 (归档后台账追加) | 见下 | | | 随本提交对新增行复跑 |

主仓同步面文字已由 TASK-031 开 PR 前自检覆盖, 不在本次范围。

### 未完成的两步 (写作时, 自指排除)

- **第 10 步 Phase D 提交双推**: 本节所在提交与 `06e2e95` / `c8238c3` 一起推送 (owner 第 4 步已授权), 推送与逐 remote 核验结果见下一条追记。
- **第 11 步 `10CG/Aria#195` 回帖并关闭**: 在上一条推送核验一致之后执行 (清单第 48 条), 结果见追记。

### 追记 — 第 10 / 11 步 (Phase D 推送与关闭回帖)

- **第 10 步 Phase D 提交双推** (owner 第 4 步授权): 推前 origin 与 github 的 master 均为 `03f97ac` 且为本地祖先; `git push origin master` / `git push github master` 分开执行、均退出 0 (`03f97ac..bd074cd`); 推后逐 remote `ls-remote`: origin 与 github 均 **`bd074cdbdeff2dacd3e3c607fc8a4c59bbdde415` MATCH**; 该 tip 上的 gitlink 为 aria `5215cf2` / standards `2bc1c4c` (两端均可达)。
- **第 11 步 `10CG/Aria#195` 回帖并关闭**: 发帖前确认归档路径已在 `origin/master` 上可见; POST 评论 → id **`26527`**; 单独 PATCH `state: closed` → `closed_at` `2026-09-28T10:54:07Z`; 独立 GET: issue `state: closed`, 评论 26527 存在且正文与草稿逐字一致。回帖含版本号 (aria-plugin v1.74.0)、SC 验收摘要与已知边界; 发帖前自检裸引用 0 · §4.5 字符 0 · U+FFFD 0。
- 本追记所在提交的推送结果见本会话回复 (自指排除)。至此 TASK-032 全部子步骤完成, 本轨终结。

### 追记二 — 10CG/aria-standards#20 回帖关闭 (2026-09-28)

owner 2026-09-28 授权「回帖关闭 10CG/aria-standards#20」。发帖前核实: 该 issue 仍 open、零评论; standards master 在 origin 与 github 均为 `2bc1c4c`, 头部 Version 已是 1.4.0; 回帖列出的五个提交 (`d217ed0` / `21748d4` / `11b0a14` / `d86fc91` / `56306d1`) 均为 `2bc1c4c` 的祖先。回帖 (评论 **26547**) 写明三次增量逐条列出、§2.3.5 判 MINOR 的依据 (aria-plugin v1.70.0 D5 先例 + Aria 仓决策单第 1 项; 「没有删字段 / 没有破坏 5 字段不变式」注明为该 issue 自己的分析) 与落地提交; 随后单独 PATCH 关闭, `closed_at` 2026-09-28T12:29:30Z; 独立 GET 核验 state 为 closed, 评论正文与草稿逐字一致。发帖前自检: 裸引用 0 · §4.5 字符 0 · 希腊字母 0 · U+FFFD 0。⇒ §4 中优先级第 2 项已完成。

---

## 变更记录

| 时间 (UTC) | 事件 |
|---|---|
| 2026-09-25 | 本台账建立。TASK-001 十条 verification 全部通过 (第 2 条不适用), TASK-002 五条全部通过。B.1 基线三处实测并建三仓 feature 分支。 |
| 2026-09-25 | TASK-003 落地: 测试文件新建 7 用例, 六条 RED 形态全部合规, 全套 1612 tests 中既有 1605 零回归。 |
| 2026-09-25 | TASK-004 落地: 追加 4 用例 (SC-4 / 5 / 13 / 14), 夹具扩展逐 commit 钉日期; 全套 1616 tests 既有 1605 仍零回归。 |
| 2026-09-25 | TASK-005 落地: 追加 5 用例 + 冻结 fixture; verification 第 7 条红绿预言全部命中; 全套 1621 tests 既有 1605 仍零回归。 |
| 2026-09-25 | TASK-006 落地 + **1.2 收口**: 追加 6 用例 (SC-15 六布局); 四批合计 22 用例 / 19 红 / 3 回归锁, 预言逐条命中; 全套 1627 tests 既有 1605 仍零回归。 |
| 2026-09-25 | TASK-007 汇总层 + 四条断言不可观测的复议项落台账。 |
| 2026-09-25 | **组 2 实现 (TASK-009~014) + TASK-033 收口**: RED → GREEN, 19 条基线红全绿, 全套 `Ran 1627 OK` 零回归; 收口 SHA `9625999`。 |
| 2026-09-26 | **组 3 反事实 (TASK-015 / 016 / 017 / 018 / 035) 全部完成**: 五个一次性副本生命周期闭合; 三处补丁形态按纪律偏离并记录; 组 3 后全量回归 `Ran 1627 OK` 零泄漏。 |
| 2026-09-26 | **组 4 文档同步与回归 (TASK-019 / 020 / 021 / 022 / 023 / 024) 全部完成**: SC-11 **19/19** 谓词为真; 两腿回归 1627 + 28 + 11 全绿; SC-12a 逐字段相等、SC-12b 子目录件以真 track 出现 (活体证明); TASK-024 六处复核全部无需改 ⇒ AB 范围不扩大。 |
| 2026-09-26 | 新会话入口: 两条 active claim 心跳刷新并推后核验 (本轨约 10.7h; `pre-merge-completeness-gate-change-scope` 约 34.7h, 已超 SWEEP_TTL); owner 授权后主仓 master `d33d233` 双推, 两端 `ls-remote` MATCH。 |
| 2026-09-27 | **TASK-025 完成**: 查重无重复 → 正文逐处实读核对 (两处行号较计划下移) → owner 授权开单 **`10CG/aria-plugin#204`** (GET 核验 open, 标题正文逐字一致) → standards 回填 `d86fc91` (`#<` 零命中)。 |
| 2026-09-27 | owner 裁「全部推」: standards `d86fc91` 与主仓 feature `c5f494f` 双推, 四处 MATCH; owner 裁「照建议」(决策单 `4c968ca`): standards `session-handoff.md` 升 1.4.0 并入 TASK-027 (更正 TASK-023 节「不 bump」的理由) / 四条断言归属订正追认 / 剩余提交不加 `Co-Authored-By`。 |
| 2026-09-27 | **TASK-026 完成** (NO_PUSH 专用会话): /skill-creator 照跑 state-scanner AB, 13 eval 两臂同为 50/78, delta.pass_rate = +0.0000 (与 PREDICTION 相符); eval 5 复跑两次 1/3 不判回归; 协调 ref 全程 `e911132`; 结论「未被有效测试」→ owner 裁「放行进 TASK-027」; 套件缺口单 **`10CG/aria-plugin#205`** (GET 核验)。 |
| 2026-09-27 | 普通会话续上 (变量已不在, 实测 `False`): 两条 claim 心跳经前置检查刷新到 `18:14:01Z` / `18:14:11Z`, 推后 origin 与本地均 `4ae229e`。 |
| 2026-09-27 | **TASK-027 完成**: 取号 `1.74.0` (两个 remote 无 `v1.74.*`, `10CG/Aria#199` 无预留号; 取号时 aria `origin/master` = `1cb3872`); CHANGELOG `[1.74.0]` 三段 + Notes 逐条对真代码核过; aria `1ad31fa` (六个文件, `README.zh.md` 经 owner 当场裁定纳入) · standards `56306d1` (`session-handoff.md` 升 1.4.0, 决策单第 1 项); 均未推送。 |
| 2026-09-27 | **TASK-028 完成** (写法自检第一次): 三仓新增行 1481 + 5 + 1307; 裸引用首跑 aria 2 / standards 0 / 主仓 5, 全部订正 (aria `820ea57`, 主仓台账三行随本节提交), 复跑归零; §4.5 字符与字面 U+FFFD 均 0。 |
| 2026-09-27 ~ 28 | **TASK-029 完成** (本地, 未推送): 首次执行停在第 2 步 (standards 占位核验判据与 TASK-023 规定不一致) → owner 裁按实质判通过 → 跨 UTC 日订正发布日期 (aria `651ff6e`) → 从第 1 步重走: aria master `5215cf2` / standards master `2bc1c4c` 双父合并正向断言成立; 取号终核七处 `1.74.0`、CHANGELOG 零丢失、两个 remote 无 `v1.74.0`; 合并树回归 `Ran 1627 OK` + 28 + 11 + 谓词 19/19 (执行器负控 0/19); tag `v1.74.0` → `5215cf2`。 |
| 2026-09-28 | **TASK-034 完成** (owner 授权): aria master `5215cf2` + tag `v1.74.0` 与 standards master `2bc1c4c` 原子双推, origin / github 逐 remote `ls-remote` 全部 MATCH; 同批授权的主仓 feature 备份双推 `877ed17` 两端 MATCH。 |
| 2026-09-28 | **TASK-030 完成**: 主仓 gitlink 前进 (aria `5215cf2` / standards `2bc1c4c`), 16 个版本点改 `1.74.0` (含补上 `VERSION:24`), custom checks 15 pass + `plugin-cache-currency` 预期 STALE; 提交 `a99dd8d` (未推送)。 |
| 2026-09-28 | **TASK-031 完成** (owner 授权五项): feature 双推 `6fdff9f` → PR `10CG/Aria#222` → C.2.4 green (not_applicable, 已 surface) + C.2.4.5 PASS → merge commit `03f97ac` → 本地快进 → C.2.5 两个 remote 全部成功、parity match → gitlink_integrity 六组 ok。TASK-032 第 1 步对齐通过。 |
| 2026-09-28 | **TASK-032 Phase D**: 27 行勾选; 归档门预演 warn (三条已知假阳性); owner 裁 Step 7 不建; 归档 `c8238c3` (Step 1-6 五条断言全绿); release_gate 释放 claim (协调 ref `4d40f84`); 另开 `10CG/aria-plugin#206`; 周期 handoff 与 latest.md 更新; 写法自检第二次归零。推送与回帖见追记。 |
| 2026-09-28 | Phase D 双推 `bd074cd` 两端 MATCH; `10CG/Aria#195` 回帖 (评论 26527) 并关闭, GET 核验 closed。**本轨终结**。 |
| 2026-09-28 | owner 授权后回帖关闭 `10CG/aria-standards#20` (评论 26547, GET 核验 closed)。 |
