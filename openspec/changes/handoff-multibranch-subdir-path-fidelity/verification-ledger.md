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

## 1.2 收口小结 (TASK-003 ~ TASK-006 四批)

| 批 | 用例数 | 基线红 | 基线绿 (回归锁) |
|---|---|---|---|
| TASK-003 第一批 (SC-1 / 3 / 8 / 9 / 16 / 18) | 7 | 6 | 1 (SC-9 (c)) |
| TASK-004 第二批 (SC-4 / 5 / 13 / 14) | 4 | 4 | 0 |
| TASK-005 第三批 (SC-6 / 17 / 2 / 7 + 排序键) | 5 | 3 | 2 (SC-2 / SC-7) |
| TASK-006 第四批 (SC-15 六布局) | 6 | 6 | 0 |
| **合计** | **22** | **19** | **3** |

- 全部 19 条红的形态均为 `AssertionError` 或 SC 明示的直接索引 `KeyError`, **无一条**环境红 (ImportError / 夹具建仓失败)。
- 四批的 verification 红绿预言**逐条命中**, 无一处需要改判。
- 既有 1605 个测试在四批之后仍**零回归**。
- 交付物两件: `aria/skills/state-scanner/tests/test_handoff_multibranch_path_fidelity.py` · `aria/skills/state-scanner/tests/fixtures/handoff-multibranch-flat-baseline-2026-09-25.json` (后者按 `hard_constraints` 第 5 条**禁止重生成**)。
- **下一步 = 组 2 实现 (TASK-007 起)**, 按 RED → GREEN 推进; 组 2 收口提交见 tasks.md 2.7。

---

## 变更记录

| 时间 (UTC) | 事件 |
|---|---|
| 2026-09-25 | 本台账建立。TASK-001 十条 verification 全部通过 (第 2 条不适用), TASK-002 五条全部通过。B.1 基线三处实测并建三仓 feature 分支。 |
| 2026-09-25 | TASK-003 落地: 测试文件新建 7 用例, 六条 RED 形态全部合规, 全套 1612 tests 中既有 1605 零回归。 |
| 2026-09-25 | TASK-004 落地: 追加 4 用例 (SC-4 / 5 / 13 / 14), 夹具扩展逐 commit 钉日期; 全套 1616 tests 既有 1605 仍零回归。 |
| 2026-09-25 | TASK-005 落地: 追加 5 用例 + 冻结 fixture; verification 第 7 条红绿预言全部命中; 全套 1621 tests 既有 1605 仍零回归。 |
| 2026-09-25 | TASK-006 落地 + **1.2 收口**: 追加 6 用例 (SC-15 六布局); 四批合计 22 用例 / 19 红 / 3 回归锁, 预言逐条命中; 全套 1627 tests 既有 1605 仍零回归。 |
