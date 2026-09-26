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
2. **`hard_constraints` 第 10 条违规 11 处, 已修**: 本 cycle 新写的源码注释里 issue 引用写成了 `Aria #195` (带空格) 而非 `<org>/<repo>#<n>`。四个源码文件共 11 处全部改为 `10CG/Aria#195`, 改后复扫新增行裸引用 **0**。
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
- **Version 头保持 1.3.0 未 bump (判断与理由)**: 该文件的版本头已由 `10CG/aria-standards#20` 专门跟踪 (它指出前两次实质增量未 bump、建议 1.4.0)。本次是第三次 additive 增量; 在此自行 bump 会把三次合并进一个号、掩盖 `#20` 记录的事实, 且 standards 版本治理不在本 spec 范围。**请 owner 复议**。
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
