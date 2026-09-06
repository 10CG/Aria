# handoff_multibranch 路径保真: ls-tree 相对路径贯穿全部四个调用方 + 读不到不再伪造 legacy track (Aria #195)

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-06
> **Linked Issue**: `10CG/Aria#195`
> **Issue**: [Aria#195](https://forgejo.10cg.pub/10CG/Aria/issues/195) (2026-09-05 立案, aria-report 自动生成; triage 22287: confirmed / major / next-cycle, 2/2 复现)
> **认领**: 已于 2026-09-06T14:47Z 经 `phase1_gate.py --phase A.1 --mode advisory --linked-issue 10CG/Aria#195 --include-terminal` 认领, track_id `handoff-multibranch-subdir-path-fidelity-bfe8285d`, `outcome=passed`, `linked_issue_overlap=[]`, `unknown_schema_claims=0`, `push_success=true`
> **基线冻结**: aria 子模块 `origin/master` **`301641b`** (= v1.71.1)。本文全部行号对此 SHA (实读副本 = 插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/`)。**两 SHA 增量实况 (R1 rework 订正)**: `git -C aria diff --name-status 0545f86 301641b` = **29 文件变更 (5 added + 24 modified)**, modified 含 `lib/collision.py` / `lib/identity.py` / `lib/claim_lifecycle.py` / `lib/constants.py` / `scripts/phase1_gate.py` / `scripts/lib/spec_complete.py` / `scripts/coordination_probe.py` 等生产文件 —— 其中 `lib/collision.py` 正是 SC-7 所测 dedupe 分组键 (`identity_key` / `split_owner_container`) 的实现所在, **复审者不得据「只新增测试文件」跳过对它的复核**。载重结论仍成立: `git -C aria diff --stat 0545f86 301641b -- <本 spec 5 个触点文件>` **输出为空** ⇒ 本 spec 全部触点零 diff, 行号在两 SHA 上一致。Phase B 在 `301641b` 起分支
> **主仓实况 (R1 rework 实测, 2026-09-06)**: `git -C /home/dev/Aria rev-parse HEAD origin/master` 均 = `ecb6296`; `git ls-tree origin/master aria` = **`301641b`** —— 同伴容器的 v1.71.1 主仓同步 PR (#202, merge `9f25a66`) **已合并**, 主仓 gitlink 已从 `0545f86` 前进到 `301641b`。头部原写「gitlink 仍指 0545f86 / 同伴 PR 尚未开 / 本 spec gitlink bump 排在其后」系起草时的陈旧 origin 视图, 已作废。**Phase C 硬约束**: 本 spec 的 gitlink bump 起点是 `301641b`, 任何情况下不得把主仓 gitlink 回退到 `0545f86`
> **代码落点**: `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py` (`_list_handoff_files` / `_read_file_content` / `_get_file_commit_date` / `_make_legacy_track_id` / 分支枚举 fail-soft 早退 / 主循环 git-show 失败分支) · `aria/skills/state-scanner/scripts/scan.py:186` (**第四个硬编码前缀点, issue 与 triage 均未点名**) · `aria/skills/state-scanner/tests/test_handoff_multibranch_path_fidelity.py` (新增) · `aria/skills/state-scanner/references/state-snapshot-schema.md` §`tracks_multibranch` · `aria/skills/state-scanner/references/json-diff-normalizer.md` · `aria/CHANGELOG.md` + 版本 SOT 5 文件 + 主仓版本引用面 (见 Task 5.1)。Spec 落主仓 (Rule #5)
> **Rule #6 判定**: 本变更全部落在 **纯代码 + schema 文档描述** 面 —— 无 `description` 变动, 无 SKILL.md 运行时指令面变动 (SKILL.md 出现 `tracks_multibranch` 共 **3 处**: `:117` collector 清单、`:149` 与 `:153` coordination 闸门接线; 本 spec 三处均不改)。判据表**第一行 (描述性)** ⇒ substitute = SC 级 baseline-failing 结构化测试。核实过套件确无覆盖: `ab-suite/state-scanner.json` 对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` 四词 **零命中**。rule6_note 见文末
> **A.1.0 头脑风暴**: 未跑 — `audit.checkpoints.post_brainstorm = off` (Rule #10 白名单第一类)
> **审计计划**: post_spec convergence 5 席 (config enabled) → post_planning convergence (config enabled); mid_implementation / post_implementation / pre_merge / post_closure 均 config 显式 off (白名单第一类)
> **审计轨迹**: post_spec R1 (2026-09-06) 票型 **REVISE 5 / PASS 0** (单席 verdict: FAIL 3 + PASS_WITH_WARNINGS 2), verdict **FAIL** —— Critical 2 / Major 15 / Minor 10 (+ 6 decisions, 其中 1 条 major); 聚合报告 `.aria/audit-reports/post_spec-R1-2026-09-06T154800-000Z-R1-handoff-multibranch-subdir-path-fidelity-aggregated.md`。**本文件为 v2 (R1 rework 后)**: 全部 critical / major 已逐条处置, 处置记录见 rework 表 (scratchpad `handoff-multibranch-subdir-path-fidelity-rework-R1.md`); 两条 conflicted 已用机械证据闭合 (见头部主仓实况行与 SC-10)

---

## Why

### 症状 (issue + triage 复现, 起草时对 `301641b` 逐条复核)

`handoff_multibranch` collector 用**递归**枚举 (`git ls-tree -r`) 找 `docs/handoff/` 下的交接文件, 却只把 basename 交给下游; 下游三个调用方各自用**写死的 `docs/handoff/<basename>` 前缀**拼回 git 对象路径。递归枚举与固定前缀不自洽 —— 任何位于子目录 (典型: `docs/handoff/archive/`) 的 `.md` 必然拼出不存在的路径。

| 位置 (@`301641b`) | 实况 |
|---|---|
| `handoff_multibranch.py:178` | `_HANDOFF_TREE_PATH = "docs/handoff"` (注意 `:177` 注释写「trailing slash required by git ls-tree --name-only」, 而 `:178` 的值并无斜杠 —— 既有注释错误, 顺带勘正) |
| `:240-288` `_list_handoff_files` | `git ls-tree -r --name-only origin/<branch> -- docs/handoff`; **`:277`** `basename = Path(path).name` 丢弃目录段; docstring **`:246-247`** 自述「callers compose the full git-object path as needed」—— 而三个调用方都无法还原 |
| `:301` `_read_file_content` | `ref = f"{_REMOTE}/{branch}:{_HANDOFF_TREE_PATH}/{filename}"` |
| `:321` `_get_file_commit_date` | `path = f"{_HANDOFF_TREE_PATH}/{filename}"` (**issue 正文第 21 行已点名此函数**; triage comment `:25` 写的「issue 未点名」有误, 本文起草时承袭了该转述偏差, R1 rework 订正) |
| `:637-658` 主循环 | `git show` 失败 ⇒ `soft_error` + **追加一条 `status: legacy` 假 track** (`owner_container: unknown`, `updated_at` = 上面那个 fallback) |

后果三层:

1. 每个子目录文件产生一条 `handoff_multibranch_git_show_failed`, `scan.py` 恒 exit 10 (`EXIT_SCAN_PARTIAL`, `scan.py:119`) —— 告警噪声。
2. 假 track 进 `tracks[]` 与 `legacy_count`, 污染 `tracks_multibranch` 看板 —— 「读不到内容」被当成「这是一份老格式交接」, 两件事被折叠。
3. **同名不同目录的静默串读** (R1 rework 补, hermetic 实测): 当 `docs/handoff/x.md` 与 `docs/handoff/archive/x.md` 同时存在时, 枚举层交出两条**一模一样**的 `"x.md"`, 于是 `_read_file_content` 对归档副本读到的是**顶层文件的内容** —— 连 `git show` 失败都不会发生, 两行 track 在 `tracks[]` 里逐字段相同。这条比 1/2 更隐蔽: 它不报错, 只是把归档件伪装成顶层件的副本。

`updated_at` 的失真需要分成两半看 (R1 rework 订正归因, 见下方 §What.2 与 SC-4):

- **路径造成的那一半**: 文件「从未在顶层存在过」时, `git log -1 -- docs/handoff/<basename>` 命中不到任何提交 ⇒ `_get_file_commit_date` 返回**空串**, `updated_at` 为空。hermetic 实测: 错误路径 `-> ''`, 正确路径 `-> '2026-06-01T09:00:00+00:00'`。
- **路径修不掉的那一半**: 文件曾在顶层存在、后被 `git mv` 进子目录时, `git log -1 --format=%aI` 对**旧 basename 路径**与**新相对路径**都返回 **mv 那次提交的日期** (hermetic 实测两者均 `2026-08-15T12:00:00+00:00`, 加 `--follow` 亦同 —— 因为 mv 提交同时触碰了两条路径, 而 `-1` 取的就是「最近一次触碰」)。**这不是路径 bug 的产物**, 路径修正后依然如此; 它是「无 frontmatter 时只能拿 git 提交日当会话日」这一 fallback 设计的固有语义, 属另一件事 (见 §待 owner 复议 3)。

triage (comment 22287) 的两条 hermetic case 在当前代码上 **2/2 命中**; 其中 case-2 的 `updated_at = 2026-08-15T12:00:00+00:00` (mv 提交日) 属上面第二半 —— 现象为真, 但**不在本 spec 的修复承诺内**。

### 起草期实读补充的两条事实 (issue 与 triage 都没有, 二者都扩大了修复面)

**F1 — 硬编码前缀不是三处, 是四处。** `scan.py:186` 的 AC-5 跨 collector 一致性检查独立拼了一次。真实符号是 **`_same_branch_head_unreachable_tracks`** (`scan.py:126` 定义, `:186` 拼串, 由 `_check_snapshot_self_consistency` 在 `:255` 调用) —— 本文 v1 三处写作 `_check_handoff_ancestry`, 该符号在 `301641b` 的 `scripts/` 与 `tests/` 全树零命中, R1 rework 已全文更正:

```python
"git", "log", "-1", "--format=%H", f"{remote}/{branch}", "--", f"docs/handoff/{filename}",
```

它在 collector 之外、另一个文件里消费 `tracks[].filename`。只改 collector 内的三处会留下一个静默失效的跨文件消费方 (`git log` 对不存在路径返回空 SHA ⇒ `scan.py:199-200` `continue`, 且该行注释明写把空输出判定为「a real answer」⇒ 该文件的 ancestry 检查被无声跳过, 无任何告警)。这正是 memory `feedback_test_runner_scope_blind_to_cross_skill_consumers` 说的形态: 只跑本 skill 的测试看不见它。

**F2 — 同一函数还有第二条同族路径失真: `git ls-tree` 默认转义并加引号。** 起草时在临时仓实跑 (`docs/handoff/2026-测试.md` + `docs/handoff/archive/b.md` + `docs/handoff/a.md`):

```
$ git ls-tree -r --name-only HEAD -- docs/handoff
"docs/handoff/2026-\346\265\213\350\257\225.md"      ← 引号 + 八进制转义
docs/handoff/a.md
docs/handoff/archive/b.md
$ git ls-tree -r --name-only -z HEAD -- docs/handoff   # NUL 分隔, 原样路径
docs/handoff/2026-测试.md
docs/handoff/a.md
docs/handoff/archive/b.md
```

**今天的失效形态 (R1 rework 订正)**: 转义后 `Path(path).name` 得到的是 `2026-\346\265\213\350\257\225.md"` —— **带一个尾引号**, 因此在 `handoff_multibranch.py:278` 的 `.endswith(".md")` 处就被 `continue` 丢弃。逐行模拟基线循环的实测输出: `DROPPED(.md filter): '2026-\\346\\265\\213\\350\\257\\225.md"'`。非 ASCII 落在**目录段**时同理 (basename 得 `b.md"` 之类)。

所以 F2 今天的形态是**静默漏扫**: 不产生 `git show` 失败、不进假 legacy 行、不推高 exit 10, 该文件在看板上**根本不存在**。它与子目录 bug 同属「枚举层输出 ≠ 可回拼的路径」这一契约错配根因, 但**失效表现不同**, 本文 v1 写的「同样落进那条假 legacy 分支」不成立。中文/日文命名的交接文件在本项目生态里完全可能 (本仓工作语言即中文)。修枚举层时若不一并处理, 等于修了一半 —— 而且是**更难被发现**的那一半 (漏扫无任何信号)。

### 根因

不是笔误, 是**契约错配**: 枚举层承诺「调用方自行拼完整路径」, 但它交出去的东西 (转义后的 basename) 在信息论上就不足以拼回。修法必须让枚举层交出**可回拼的路径**, 并让全部四个调用方都用它。

### 候选方案与否决理由

| 方案 | 内容 | 判决 |
|---|---|---|
| **A (v1 采纳, R1 后转 待 owner 复议 2)** | 枚举层保留 ls-tree 原样相对路径; 四个调用方直接用它拼 ref; **`tracks[].filename` 的取值语义随之从 basename 变为相对路径** | 支持任意子目录布局; 平铺仓 (含 Aria 自身) 的取值与今天**逐字节相同** ⇒ 零行为变化。**但**: 它改的是既有输出字段的语义, 下游 `latest_md_writer` → `handoff.py` pointer 往返会断 (见 §5 与待复议 2), 且与 issue / triage 原案的关键分句相反 |
| **A′ (R1 新增候选, = issue / triage 原案)** | 枚举层同样交出相对路径, 但**`filename` 字段仍派生 basename**, 另加 additive 字段 (`relpath`) 承载相对路径, 供 `_read_file_content` / `_get_file_commit_date` / `_make_legacy_track_id` / `scan.py:186` 消费 | issue-195 正文第 41 行 A 案原文:「`filename` / `track_id` 等需要 basename 的字段**另行派生**」; triage comment `:53`:「`filename` 字段另派生 basename」。兼容面最干净 (既有消费方语义不变, `snapshot_schema_version` 的 additive-only 声明也才成立)。**代价**: `scan.py:186` 与 `latest_md_writer` 需显式改用新字段; 子目录 pointer 往返的既有缺口 (见待复议 2) 不会因此修好, 只是不新增 |
| B | `ls-tree` 去掉 `-r`, 只扫顶层 | 语义最简, 但**静默丢弃**子目录里的全部交接历史。把归档放子目录的采用方等于那段历史不进看板 —— 用"看不见"换"不报错", 与本 collector 的用途 (多终端交接发现) 直接冲突 |
| C | 保留 `-r`, 显式 `continue` 掉非顶层项 | 行为同 B, 只是把意图写进代码。仍然丢历史; 且它把「递归枚举」这个正确动作退回去, 而真正错的是下游拼路径 |
| D (附加, 采纳) | git show 失败不再降级为 legacy track, 只报 soft_error | 与 A/A′/B/C 正交。issue 明确提出; 「读不到」与「老格式」是两件事, 折叠它们让失真数据带着误导性 `updated_at` 进看板 |

> **A vs A′ 未决** (R1 critical `63d1ce08` + decision `109b412c`): 本文 v1 直接采纳 A 且称「issue 与 triage 均倾向此案」——**该转述失实**, 两个来源的关键分句都是「`filename` 另行派生 basename」。取舍已升级为 §待 owner 复议 2, **Phase B 不得在裁决前动枚举层输出字段的语义**。下文 §What / §5 / §7 / SC 凡涉及 `filename` 取值语义处, 均已标注 A / A′ 两分支的差异。

---

## What

### 1. 枚举层 `_list_handoff_files` (`:240-288`)

| | 改前 | 改后 |
|---|---|---|
| ls-tree 调用 | `git ls-tree -r --name-only <ref> -- docs/handoff` | 加 `-z` (NUL 分隔, 关闭引号转义); 按 `\0` 切分, 空段丢弃 (F2) |
| 每项取值 | `basename = Path(path).name` (`:277`) | `rel` = 相对 `docs/handoff/` 的路径。**前缀剥离必须从常量派生**, 不得新写字面量 (`rel = path[len(_HANDOFF_TREE_PATH) + 1:]` 或 `PurePosixPath(path).relative_to(_HANDOFF_TREE_PATH)`) —— 写死 `path[len("docs/handoff/"):]` 等于新造**第五处硬编码前缀**, 正是本 spec 认定的根因族 |
| 前缀守卫 | 无 | 不以 `docs/handoff/` 开头的行 (理论上不会出现) 计一条 soft_error 并**只跳过该行**。**契约变更 (R1 rework 补)**: 现签名 `tuple[list[str], str \| None]` 只有**分支级**错误通道 —— 主循环 `:619-626` 收到非 None 即 `soft_error("handoff_multibranch_ls_tree_failed")` 后 `continue`, **整支分支的已枚举文件全部丢弃**。要表达「跳过该行、其余照常」必须改签名 (例: 第三个返回位携带 per-item 错误列表) 或向函数注入 reporter。此契约变更由 Task 2.1 承接, 由 SC-9 的第二条断言钉住 |
| `.md` 过滤 | 对 basename 判 `.endswith(".md")` (`:278`) | 对 `rel` 的 **basename** 判 (语义不变; `-z` 之后不再有尾引号, F2 的漏扫随之消失) |
| pointer 排除 | `basename == "latest.md"` (`:280`) | **不变 —— 现状即任意深度** (R1 rework 订正)。`:277` 先取 basename、`:280` 再比常量, 所以 `archive/latest.md` 今天**就已经**被排除。hermetic 实测: 含 `docs/handoff/latest.md` + `docs/handoff/archive/latest.md` 的临时仓上跑基线循环, 两者均 `DROPPED(pointer)`。本行不是行为变更, 只需把该口径**补写进 schema 文档** (今天未成文) |
| 返回 | `list[str]` basename | **A 案**: `list[str]` 相对路径 (平铺仓两者逐字节相同) / **A′ 案**: 相对路径供内部拼 ref, `tracks[].filename` 另派生 basename |
| docstring (`:246-247`) | 「Returns only the basename … so callers compose the full git-object path as needed」 | 改为「Returns each file's path **relative to `docs/handoff/`** …」—— 契约与实现对齐 (根因就在这句自述上) |

### 2. 三个仓内调用方改用相对路径 (语义不变, 只是不再丢信息)

- `_read_file_content:301`: `ref = f"{_REMOTE}/{branch}:{_HANDOFF_TREE_PATH}/{relpath}"` (拼法不变, 入参含义变准)。**这一处才是同名串读 (§Why 后果 3) 的修复点**
- `_get_file_commit_date:321`: 同上。**真实收益 (R1 rework 订正)** = (a) 「从未在顶层存在过」的子目录文件, `updated_at` 从**空串**变成真日期 (hermetic 实测); (b) `git show` 成功后走 frontmatter 分支, 根本不再落到这个 fallback。**mv 过的无 frontmatter 文件仍取 mv 提交日** —— 路径正确后依然如此, 与 SC-4 一致, 不是本 spec 的修复承诺 (v1 此处写「不再取到 mv 提交日」系误断, 已实跑证伪)
- `_make_legacy_track_id:329-336`: `legacy:<branch>:<relpath>` —— 用相对路径而非 basename。今天 `docs/handoff/x.md` 与 `docs/handoff/archive/x.md` 会产生**同一个** `legacy:<branch>:x.md`, 被 `dedupe_latest_per_track_container` 当成同一 track 折叠 (且如 §Why 后果 3, 两行内容还完全相同)。由 SC-13 覆盖

> A′ 案下本节三个函数的入参改名为 `relpath` 不变, 变的只是 `tracks[]` 里回填哪个值。

### 3. `scan.py:186` (F1, 跨文件消费方)

**A 案**: `f"docs/handoff/{filename}"` 保持字面不变即可正确 —— 因为 `filename` 现在就是相对路径。**A′ 案**: 该行必须显式改读新的 `relpath` 字段, 否则 F1 仍然静默失效。

无论哪案, **必须有测试钉住这个隐式耦合**: 该行与 collector 的 `_HANDOFF_TREE_PATH` 是两处独立字面量, 今天靠巧合一致。SC-6 用一条断言把它锁住 (子目录 track 的 ancestry 检查必须真的执行到 `git log` 并拿到非空 SHA, 而不是拼错路径后返回空再 `continue`)。

### 4. git show 失败不再伪造 legacy track (`:637-658`)

| | 改前 | 改后 |
|---|---|---|
| 行为 | soft_error + 追加 `status: legacy` 行 + `legacy_count += 1` | 只 soft_error; **不进 `tracks[]`**, 不计 `legacy_count` |
| 计数 | 无 | 新增 additive 字段 `unreadable_count: int` (**恒存在, 默认 0**) —— 信息不丢, 只是搬到正确的名字下 |

**「恒存在」必须把错误路径一起改 (R1 rework 补)**: 分支枚举失败的 fail-soft 早退 dict (`handoff_multibranch.py:586-596`) 逐字列出 `{exists, tracks, branches_scanned, legacy_count, collision, errors}`, 没有 `unreadable_count`; `references/state-snapshot-schema.md:1136` 的 fail-soft 形状说明同样逐字列了这六个键。两处不同改, 「恒存在」这个不变量在错误路径上就是假的。由 Task 2.4 + SC-14 承接。

无 frontmatter 的真 legacy 分支 (`:683-700`) **不动** —— 那才是「老格式交接」的本义。

### 5. 消费方枚举 (起草时 grep 全 skill 树 + 主仓; R1 rework 逐行复核并订正两行)

| 消费方 | 用法 | 本变更影响 |
|---|---|---|
| `scan.py:186` `_same_branch_head_unreachable_tracks` | `git log … -- docs/handoff/{filename}` | F1, 见 §3 —— A 案下字面不变即可用, A′ 案下必须改读 `relpath` |
| `writers/latest_md_writer.py:143` (`_render_pointer`, 由 `write_latest_md:259` 调用) | `**Latest**: [{filename}](./{filename})` | ⚠️ **A 案下这是本 spec 引入的新失败面** (R1 critical, 4 席一致; v1 此行原写「相对路径天然正确 / 无影响」——只对**人类点击的 markdown 链接**成立, **机器读回链没追**)。姊妹 collector `handoff.py` 仍是扁平世界: `_parse_latest_pointer` 在 `:288` 用 `Path(target).name` 剥掉目录段, 候选集 `_scan_md_files` (`:300`) 用 `iterdir()` **非递归**扫描 (`:318`), 匹配又按 `p.name` 建索引 (`:389`)。于是 D.3 写出 `[archive/x.md](./archive/x.md)` 后: (a) 顶层还有旧交接时 ⇒ `handoff_pointer_target_missing` soft_error (`:399`) + `latest_source` 由 pointer 退回 mtime ⇒ `scan.py` 继续 exit 10, 且重开了 H5「pointer 是语义权威」那条既有修复; (b) 全部交接都在子目录时 ⇒ `canonical_files` 为空 ⇒ `handoff.py:438-440` 直接 `exists: False` 且**零 soft_error**, 两个 collector 在同一快照里互相矛盾而无任何信号。**注意 A′ 案不会新增这条失败面, 但也修不好它** —— pointer 写 basename、候选集非递归, 子目录目标一样找不回。处置见 §待 owner 复议 2 + SC-15 |
| `writers/latest_md_writer.py:208-217` | legacy 表展示 `filename` 列 | A 案: 展示相对路径, 更准; 平铺仓不变。A′ 案: 不变 |
| `handoff_multibranch.py:428-457` `_dedupe_sort_key` | 4 级键第 3 级按 `filename` 字典序取大 (`:455`) | **A 案有行为面**: `archive/…` (`a`=0x61) 字典序大于 `2026-…` (`2`=0x32), 故同 `(track_id, identity_key)` 且 `updated_at` 完全相同时, 归档副本会赢。仅在该三重并列时可达; 归档件通常更旧 ⇒ 记入 Impact.Risk, 由 SC-7 钉住现状行为, 并由 Task 4.1 订正 schema `:1125` 那条已变假的论据。A′ 案下无此面 |
| `renderers/track_board.py` | 不读 `filename` **字面** (`:254,559` 的 HANDOFF 列只吃 `updated_at`), 但 `:183,188` 直接 import 并应用 collector 的 `dedupe_latest_per_track_container` | **不是「无影响」(R1 rework 订正)**: 经共享 dedupe 的四级排序键第 3 级 (`filename`) **间接消费** ⇒ 上一行的 tie-break 风险同样落到看板 collision 输入的代表行选择上, 而同组两行的 `status` / `phase` 可以不同 ⇒ 渲染随之改变。实际差异在三重并列下近乎为零, 语义由 SC-7 一并覆盖, 本 spec 不另加断言 |
| `lib/collision.py` | 按 `track_id` / `owner_container` 分组 | legacy 行的 `owner_container` 恒 `unknown`, `classify()` (`:480-486` 的 `collidable` 过滤) 本就排除 ⇒ 少几条假 legacy 行不改分类结果 |

### 6. 文档同步 (Rule #3)

1. `references/state-snapshot-schema.md` §`tracks_multibranch` (`:1074` 起):
   - `:1110` `filename` 字段语义 (A 案改为「相对 `docs/handoff/` 的路径 (平铺仓 = basename)」; A′ 案保持 basename 并新增 `relpath` 行)
   - 新增 `unreadable_count`
   - **`:1136` fail-soft 形状**补 `unreadable_count` (见 §4)
   - 写明 pointer 排除口径 = 任意深度的 `latest.md` (今天未成文, 且是现状而非新行为)
   - 写明「git show 失败不再产生 legacy 行」
   - **`:1125` tie-break 论据订正**: 现文「Handoff filenames are `YYYY-MM-DD-...`-prefixed, so the lexicographically greater name is also the later-authored one among same-day files」在 A 案的相对路径下**直接变假** (`archive/` 的 `a` = 0x61 > 数字), 不改就是把一条错误不变量留给下一个动排序的人 (Impact.Risk 第 1 条承诺的「在 schema 文档写明」落点即此)
2. **collector 自身的机读契约 docstring** (`handoff_multibranch.py`, R1 rework 补): `:14-31` 的 top-level 键表缺 `unreadable_count`; `:42` 逐字写 `"filename": str,  # basename of the handoff file` (A 案直接推翻它); `:20` 的 `legacy_count` 注释「tracks that fell back to legacy (no frontmatter)」是 code/doc 早已不一致的那半 (代码在 git-show 失败分支同样 `legacy_count += 1`), 本 spec 改完该分支后正好使注释成真, 一并勘正
3. `references/json-diff-normalizer.md:241` 显式枚举了 `branches_scanned / legacy_count / collision / errors / exists` 键集 —— 补 `unreadable_count`
4. `:177` 的常量注释勘正 (「trailing slash required」与 `:178` 无斜杠的值不符)
5. CHANGELOG 记 Fixed 三条 (子目录 / 非 ASCII / 假 legacy)

### 7. 向后兼容

- **平铺仓 (含 Aria 自身)**: `filename` / `track_id` / `legacy_count` 取值逐字节不变 —— 本仓 `docs/handoff/` 无子目录、无非 ASCII 文件名 (Task 1.1 机械核验)。既有冻结语料 `tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 与 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 因此不需重生成 (Task 1.1 同时核验其中无子目录路径)。
- **子目录仓**: 从「假 legacy / 静默漏扫 / 空 `updated_at`」变成「真 track + 真日期」, 是修复不是破坏。
- `unreadable_count` 为 additive 新键, 老消费方不读它即可。
- ⚠️ **`snapshot_schema_version` 的处置随 A / A′ 裁决而定 (R1 rework)**: A′ 案是纯 additive, 保持 `"1.0"` 名副其实; **A 案改的是既有字段 `filename` 的取值语义, 不属 additive** —— 若采纳 A, 必须由 owner 明确「取值语义变更是否触发 schema_version bump」, 不能一边改语义一边声称「additive-only 演进契约」。见 §待 owner 复议 2。
- ⚠️ **F2 的覆盖边界 (R1 rework 补)**: `_common.py::_run` 用 `encoding="utf-8", errors="replace"` (`:411-412`) ⇒ `-z` 方案对**可解码 UTF-8** 的路径成立; 真正非 UTF-8 字节的文件名解码即失真、拼不回 git 对象, 修后它从「静默漏扫」变成「新增一条 unreadable + 继续 exit 10」, 并非修好。姊妹 collector `handoff.py:318-322` 对同类文件名是**显式跳过**的既有先例。schema 与 CHANGELOG 须写明 F2 只覆盖「可解码 UTF-8 的非 ASCII 名」, 以免后续被当成回归。

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 子目录 / 非 ASCII 布局的采用方: `tracks_multibranch` 侧不再产生 `handoff_multibranch_git_show_failed` 与假 legacy 行, 子目录交接从「漏扫 / 假 track」变成真 track。**措辞收窄 (R1 rework)**: 不能承诺「不再恒 exit 10」—— 姊妹 collector `handoff.py` 的 pointer 往返缺口 (§5) 未在本 spec 内闭合前, 子目录仓的 `handoff_pointer_target_missing` 仍会把 scan 拉到 exit 10。该承诺的最终范围由待复议 2 的裁决决定 |
| **Positive** | 看板不再混入内容串读的重复行与空/失真 `updated_at`; 「读不到」与「老格式」两个状态分开, 后续判据可分别处置 |
| **Positive** | 修掉一个跨文件静默失效点 (F1): AC-5 ancestry 检查对子目录交接从「拼错路径后无声跳过」变成真检查 |
| **Risk** | (仅 A 案) dedupe 第 3 级 tie-break 在 `archive/` 前缀下字典序变大, 三重并列时选中归档副本, 并经共享 dedupe 传导到 track_board 的 collision 输入。缓解: SC-7 用定向用例钉住现状, Task 4.1 订正 schema `:1125` 那条已变假的论据; 该并列需 `track_id` + `identity_key` + `updated_at` 全同, 概率低且两行内容通常一致 |
| **Risk** | (仅 A 案) `latest_md_writer` → `handoff.py` pointer 往返断裂 (§5 详述, R1 critical)。缓解: 待复议 2 裁决 + SC-15 往返断言; 裁决前 Phase B 不得动 `filename` 语义 |
| **Risk** | `legacy_count` 语义收窄 (不再含读不到的文件)。缓解: `unreadable_count` 承接, schema 文档 (含 `:1136` fail-soft 形状) 写明, CHANGELOG 标注 |
| **Risk** | `-z` 改变了 ls-tree 输出解析形态, 解析写错会让**所有**分支枚举返回空 (静默失明, 比原 bug 更坏)。缓解: SC-2 用冻结语料/同工作区双跑比对断言平铺仓枚举结果非空且与改前逐字节相同 (反事实: 解析写错 ⇒ 空集 ⇒ 红) |
| **Risk** | F2 只覆盖可解码 UTF-8 名; 真正非 UTF-8 字节的文件名修后仍不可读 (§7 末条)。缓解: schema + CHANGELOG 写明边界, 并考虑对不可解码名显式跳过 (对齐 `handoff.py:318-322` 先例) 而非计入 `unreadable_count` |

---

## Tasks

- [ ] 1.1 前置核验: 本仓 `docs/handoff/` 无子目录与非 ASCII 文件名; 两份冻结语料内无子目录路径 (机械命令 + 结果抄进 tasks 记录)
- [ ] 1.2 建红测: 新测试文件覆盖子目录 / 非 ASCII / git-show 失败 / 同名串读 四族, 对 `301641b` 全红且红在正确断言上 (逐条记录红的断言文本, 防「红在环境上」)
- [ ] 2.0 **前置门**: 待复议 2 (A vs A′) 与待复议 1/3 由 owner 裁决落地后, 才动枚举层输出字段语义
- [ ] 2.1 枚举层改造 (`-z` + 相对路径 + **从 `_HANDOFF_TREE_PATH` 派生**的前缀剥离守卫 + 返回契约改为可携带 per-item 错误 + docstring 契约对齐); pointer 排除**不改代码**, 只补文档口径
- [ ] 2.2 三个仓内调用方与 legacy track_id 改用相对路径 (A′ 案下另加 `relpath` 字段并改 `scan.py:186`)
- [ ] 2.3 git-show 失败分支改为只报 soft_error; 新增 `unreadable_count`
- [ ] 2.4 fail-soft 早退路径 (`:586-596`) 补 `unreadable_count`, 使「恒存在」不变量在错误路径上成立
- [ ] 3.1 `scan.py` AC-5 跨文件消费方钉测 (F1) —— 端到端产出 tracks_data, 四道前置显式配齐 (见 SC-6)
- [ ] 3.2 dedupe tie-break 现状钉测 (风险面)
- [ ] 3.3 legacy track_id 相对路径化钉测 (同名不同目录不折叠, SC-13)
- [ ] 4.1 schema 文档同步 (`filename` 语义 / `relpath` (A′) / `unreadable_count` / `:1136` fail-soft 形状 / pointer 口径 / legacy 分支 / **`:1125` tie-break 论据订正** / F2 覆盖边界)
- [ ] 4.2 collector 模块 docstring (`:14-31` 键表 / `:42` filename 契约 / `:20` legacy_count 注释) + `references/json-diff-normalizer.md:241` 键集 + `:177` 常量注释勘正
- [ ] 4.3 既有测试全绿 + 平铺仓零行为变化断言
- [ ] 5.1 版本 SOT 5 文件 + `aria/CHANGELOG.md` (PATCH) + **主仓版本引用面** (R1 rework 补, 三条 enabled custom check 兜底): `README.md:8` badge 与 `:242` 正文版本行 (`.aria/state-checks.yaml:88 m6-version-badge-match`) · `README.zh.md` / `README.ja.md` / `README.ko.md` 顶部 `<!-- translated-from: vX.Y.Z -->` marker (`:141 i18n-readme-translation-currency`; 仅正文实质变更才重译, #140 B 档) · `docs/architecture/system-architecture.md:189` 与 `docs/architecture/version-scheme.md:23` 的 aria-plugin 版本行 (`:372 plugin-version-arch-docs-match`)。三条 check 判据均为「与 `aria/.claude-plugin/plugin.json` 比对」⇒ 漏改必在归档闸转红
- [ ] 5.2 Phase C: aria 本地 merge + 双推核验 (Rule: 子模块禁服务端合并 + 逐个 `ls-remote` 核验); 主仓 spec + gitlink bump **从 `301641b` 前进** (实测起点, 见头部主仓实况行; 严禁回退到 `0545f86`)
- [ ] 5.3 Phase D: 归档 + `release_gate` claim 释放 + #195 关闭回帖

---

## Success Criteria (可证伪; 每条自问「机制没实现会红吗」)

| SC | 断言 | 核验 |
|---|---|---|
| SC-1 | **hermetic case-1 (issue 主症状)**: 临时仓, `docs/handoff/archive/2026-05-09-session-end.md` 从未在顶层存在过, 有合法 frontmatter → `tracks[]` 含一条 `legacy: false` 行, `track_id` / `updated_at` 取自 frontmatter; `errors[]` 无 `handoff_multibranch_git_show_failed`; `legacy_count == 0`。`filename` 断言随裁决取值 (A: `"archive/2026-05-09-session-end.md"` / A′: `filename == "2026-05-09-session-end.md"` 且 `relpath == "archive/2026-05-09-session-end.md"`)。**反事实**: 回退枚举层为 basename ⇒ git show 失败 ⇒ 该断言全红 | `test_handoff_multibranch_path_fidelity.py::test_subdir_file_read_as_real_track` |
| SC-2 | **平铺仓零行为变化**: 同一临时仓只放顶层文件, 改前与改后 `collect_handoff_multibranch` 的 `tracks[]` / `legacy_count` **逐字段相等**。**载入方式 (R1 rework 改)**: 禁用「测试内 `git show 301641b:` 动态载入原实现」—— 实跑确认三层障碍: 朴素 `exec` 直接 `ImportError: attempted relative import with no known parent package` (collector `:120` `from ._common import` / `:127` `from .handoff import`); 必须建 `collectors.<name>` 包上下文并手动设 `__file__`, 否则 `:141` 的 `_Path(__file__)` 抛 NameError 而 `:152` 只 `except ImportError` 接不住; 且插件把 `tests/` 分发到**无 `.git`** 的 cache 目录、组织 CI checkout 为 `fetch-depth: 1` ⇒ 异地必 error。改用**冻结语料比对** (仓内已有 `tests/fixtures/freeze_corpus.py` + `handoff-tracks-frozen-*.json` 形态): 改前在同一工作区跑一次生成 baseline JSON 落 `tests/fixtures/`, 改后比对。**反事实**: `-z` 解析写错 ⇒ 枚举空集 ⇒ 两侧不等 ⇒ 红 | `::test_flat_repo_byte_identical_to_frozen_baseline` |
| SC-3 | **非 ASCII (F2)**: `docs/handoff/2026-测试-交接.md` (合法 frontmatter) → 被读成真 track, `filename` 无引号无八进制转义。**反事实 (R1 rework 订正机制)**: 去掉 `-z` ⇒ `Path(path).name` 得到带尾引号的 `2026-\346\265\213\350\257\225.md"` ⇒ 在 `.endswith(".md")` 处被 `continue` **静默丢弃** ⇒ 该 track 根本不在 `tracks[]` 里 ⇒ 红。(**不是**「git show 失败」—— 今天该路径连 git show 都到不了, 见 §Why F2 实测) | `::test_non_ascii_filename_not_escaped` |
| SC-4 | **`updated_at` 语义分割 (现状记录性 + 修复性各一半)**: 顶层 commit (作者日期 2026-05-09) → `git mv` 进 `archive/` (2026-08-15) 且文件**无** frontmatter → legacy 行的 `updated_at` = `2026-08-15…`。**这一半是现状记录性断言, 改前改后同值** (hermetic 实测: 旧 basename 路径与新相对路径的 `git log -1 --format=%aI` 都返回 mv 日, `--follow` 亦同), 用于让未来给 `_get_file_commit_date` 加 `--follow` 的人当场看见「那救不了」。**有鉴别力的另一半 (修复性)**: 从未在顶层存在过、无 frontmatter 的 `archive/2026-06-01-x.md` → `updated_at` 为**非空真日期**; **反事实**: 回退为 basename ⇒ `git log` 命中不到 ⇒ 空串 ⇒ 红。第三条: **有** frontmatter 的同形文件 → `updated_at` 取 frontmatter 值, 与 mv 日无关 | `::test_moved_file_dates` |
| SC-5 | **git show 失败不再伪造 legacy**: 构造一条枚举得到、但 `git show` 必失败的路径 (枚举后删除该对象所在 ref / 用 monkeypatch 让 `_read_file_content` 返回错误) → `errors[]` 含 `handoff_multibranch_git_show_failed`, `tracks[]` **不含**对应行, `legacy_count` 不增, `unreadable_count == 1`。**反事实**: 保留旧降级分支 ⇒ tracks 多一行 ⇒ 红 | `::test_unreadable_not_downgraded_to_legacy` |
| SC-6 | **F1 跨文件消费方**: 对含子目录 track 的快照跑 `scan.py::_same_branch_head_unreachable_tracks` (真实符号, 非 `_check_handoff_ancestry`), 断言它对该 track 真的执行了 `git log` (命令行含 `docs/handoff/archive/…`) 且得到非空 SHA。**tracks_data 必须由同一临时仓上的 `collect_handoff_multibranch` 端到端产出, 禁止手搓 dict** (R1 rework: 函数签名只吃 dict, 手搓会让 collector 根本没被调用, 反事实变假 ⇒ SC 恒绿)。**四道前置必须在夹具里显式配齐** (`scan.py:166-183`, 任一不满足即在早返回 `[]` 上假绿): `git_data["current_branch"]` 非空 · `detached_head` 为假 · `enforced_remotes` 非空 · track 的 `branch` 等于 `current_branch`。**反事实**: 把 collector 退回 basename ⇒ 命令行路径不存在 ⇒ 空 SHA ⇒ 断言红 | `::test_scan_ancestry_consumer_uses_relative_path` |
| SC-7 | **dedupe tie-break 现状钉住 (风险面, 现状记录性断言)**: 同 `(track_id, identity_key)` 两行, `updated_at` 完全相同, filename 分别为 `2026-07-19-x.md` 与 `archive/2026-07-19-x.md` → `dedupe_latest_per_track_container` 选中 `archive/…` 那行 (字典序大)。用于让未来改排序语义的人当场看见; 与 Task 4.1 对 schema `:1125` 论据的订正配套 | `::test_dedupe_tiebreak_prefers_lexicographic_max_path` |
| SC-8 | **pointer 排除口径 (前半现状记录性, 后半有鉴别力)**: 顶层 `latest.md` 与 `archive/latest.md` 均不出现在 `tracks[]` —— **这在 `301641b` 上已经为真** (`:277` 先取 basename 再于 `:280` 比常量, 本来就是任意深度; hermetic 实测两者均被排除), 故前半是记录性断言, 无鉴别力, 仅防未来收窄时无声回归。**有鉴别力的后半**: `archive/latest-notes.md` (非 `latest.md`) 进入 `tracks[]`, 且其 `filename`/`relpath` 保留 `archive/` 目录段 (A 案) 或 `relpath` 保留而 `filename` 为 basename (A′ 案); **反事实**: 回退为 basename ⇒ 目录段丢失 ⇒ 红 | `::test_pointer_excluded_at_any_depth` |
| SC-9 | **前缀守卫不静默吞 (两条断言, 缺一即假绿)**: 构造一批枚举返回, 其中一条不以 `docs/handoff/` 开头 (monkeypatch `_run`) → (a) 计一条 soft_error 且该项不进 `tracks[]`, 不 crash; (b) **同分支的其它文件仍照常进 `tracks[]`**。**反事实**: 沿用现签名的分支级错误通道 (`:619-626` 收到非 None 即 `continue` 整支分支) ⇒ (b) 红。缺了 (b), 「吞掉整分支」的天真实现同样满足 (a) 而假绿, 且那种实现比原 bug 更坏 | `::test_unexpected_prefix_soft_errors` |
| SC-10 | **既有测试全绿**: `cd aria/skills/state-scanner/tests && python3 -m unittest test_handoff_multibranch_collision_dedupe test_handoff test_handoff_worktrees test_track_board_advisories` → **`Ran 78 tests … OK`** (R1 rework 订正: v1 记 73 系漏计 `test_track_board_advisories` 的 5 条; 五席各自实跑 + 本次 rework 在**仓内工作树** `/home/dev/Aria/aria/...` 与**插件缓存副本**两处复跑, 均 78, 分模块 21+27+25+5)。全量 `discover` 另跑并与改前基线逐条对比。**已删除 v1 对两条「已知失败」的豁免** (R1 critical `24165c1c`): 那两条 (`test_normalize_snapshot.TestStabilityIntegration.test_two_consecutive_runs_diff_zero` + `Test1210ChannelStabilityUnderOffline`) 是**测量环境伪失败**, 不是被审对象属性 —— 根因是 `tests/test_normalize_snapshot.py:272` / `:344` 的 `Path(__file__).resolve().parent×5`, 在插件缓存里解析到 `~/.claude/plugins/cache/10CG-aria-plugin/aria` (**非 git 仓**, 实测 `.git` 不存在) ⇒ `scan.py` 返回 20 (`EXIT_HARD_PRECONDITION`, `scan.py:120`) ⇒ 两条 assert 挂; 本次 rework 在**真 git checkout** (`/home/dev/Aria/aria`, HEAD = `301641b`) 上跑同一文件得 **`Ran 32 tests … OK`**。故基线口径 = **真仓 checkout 零失败**, 出现任何失败都要逐条 `git log -- <file>` 归因, 不得预先豁免 | 命令 + 对比 (基线须在真 git checkout 上测) |
| SC-11 | **文档同步机检 (R1 rework: 换掉不定位的代理判据)**: (a) `grep -c 'unreadable_count' references/state-snapshot-schema.md` ≥ 2 (字段表 + `:1136` fail-soft 形状各一); (b) schema 文档 `filename` 行含「相对」二字 (A 案) 或含 `relpath` 行 (A′ 案); (c) **`grep -q 'callers compose the full git-object path' collectors/handoff_multibranch.py` 无命中** (旧契约句消失) **且** 模块 docstring `:42` 的 `filename` 行不再是 `# basename of the handoff file` (A 案) / 已新增 `relpath` 行 (A′ 案) —— 取代 v1 的 `grep -c 'basename' … 相对基线减少`, 该代理判据不定位 (基线 7 处: `:42,246,277,278,280,284,288`, 新实现仍需 basename 做 `.md` 过滤与 pointer 排除, 只改 `:246` 一句即可让计数下降, 结构上钉不住 `:42` 的漏改); (d) `grep -q 'unreadable_count' references/json-diff-normalizer.md`; (e) CHANGELOG 含本 spec 三条 Fixed | grep |
| SC-12 | **活体 dogfood (R1 rework: 基线改同工作区双跑)**: 在本仓同一工作区先跑**改前** `scan.py --output …/snap-before.json`, 再跑改后 `…/snap-after.json`, 对 `tracks_multibranch` 做逐字段 diff → 除 `unreadable_count` 新键外**零差异** (本仓平铺, SC-2 的活体版)。**不得拿活文件 `.aria/state-snapshot.json` 当基线** —— 它随 origin 上任何一份新交接而变, Phase B 期间必假红 (memory `feedback_baseline_corpus_stat_must_run_against_frozen_snapshot` 同型)。另在临时子目录仓跑同一命令并抄下退出码与全部 soft_error kind (**不预先断言 exit 0**: 是否达成取决于待复议 2 的裁决, 见 SC-15) | 命令 + handoff 证据 |
| SC-13 | **legacy track_id 相对路径化 (R1 rework 新增, 覆盖 §2 第三条)**: 临时仓放两份**均无 frontmatter** 的 `docs/handoff/x.md` 与 `docs/handoff/archive/x.md` → `tracks[]` 产生**两条不同 `track_id`** (`legacy:<branch>:x.md` 与 `legacy:<branch>:archive/x.md`), `dedupe_latest_per_track_container` **不折叠**。**反事实**: legacy track_id 沿用 basename ⇒ 两行同 id ⇒ 折叠成一条 ⇒ 红。(改前该场景还叠加 §Why 后果 3 的内容串读, 两行连 `updated_at` 都相同) | `::test_legacy_track_id_uses_relpath` |
| SC-14 | **`unreadable_count` 恒存在覆盖错误路径 (R1 rework 新增, 覆盖 §4)**: monkeypatch 让 `_list_origin_branches` 返回错误 → 走 `:586-596` fail-soft 早退 → 返回 dict **含** `unreadable_count == 0` 键, 且 `errors[]` 非空。**反事实**: 只改正常路径 ⇒ 早退 dict 缺键 ⇒ `KeyError` / 断言红 | `::test_unreadable_count_present_on_failsoft_early_return` |
| SC-15 | **writer → collector pointer 往返 (R1 rework 新增, 覆盖 critical `63d1ce08`)**: 子目录布局临时仓上依次跑 `collect_handoff_multibranch` → `write_latest_md` → `collect_handoff`, 断言 (a) `handoff.exists` 与 `tracks_multibranch.exists` 不互相矛盾; (b) `errors[]` 不含 `handoff_pointer_target_missing`; (c) `latest_source == "pointer"`。**本 SC 的成立与否直接取决于待复议 2 的裁决**: 采纳 A 且不同时修 `handoff.py` 的扁平假设 ⇒ (b)(c) 必红 (机制见 §5); 采纳 A′ ⇒ 不新增失败面但既有缺口仍在, (b)(c) 同样红。因此本 SC 有两种合法落地: (i) 裁决含「同 cycle 修 `handoff.py::_parse_latest_pointer` + `_scan_md_files` 的扁平假设」⇒ 三条全绿断言; (ii) 裁决为「本 spec 不碰该缺口」⇒ 本 SC 降为**现状记录性断言** (抄下实际 soft_error 与 `latest_source`), 同时 Impact 首行的「不再恒 exit 10」承诺必须相应收窄, 并另开 issue 追该缺口。**无论哪种, 都不得让 spec 一边留着该缺口一边宣称子目录采用方 exit 0** | `::test_pointer_roundtrip_subdir_layout` |

---

## rule6_note (Rule #6 — 判据表第一行「描述性」, SOT `standards/conventions/skill-benchmark-exemption.md`)

- **变更性质**: 全部是 collector / scan 代码 + 输出 schema 文档。**无** `description` 变动, **无** SKILL.md / references 里任何「AI 该怎么做」的处方性指令变动。核实 (R1 rework 勘正): SKILL.md 出现 `tracks_multibranch` 共 **3 处** —— `:117` collector 清单 (描述性) 与 `:149` / `:153` coordination 闸门接线 (运行时指令面), 本 spec **三处均不改**; 且假 legacy 行的 `owner_container` 恒 `unknown`, `lib/collision.py:480-486` 的 `classify()` 本就排除它们 (`collidable` 过滤 `owner_container != "unknown"`) ⇒ 少几条假 legacy 行不动 `collision.kind` ⇒ 闸门面 (`:149`/`:153` 的触发条件) 不受影响。按判据表第一行 ⇒ AB 不适用, substitute = SC 级 baseline-failing 结构化测试。
- **套件覆盖实测**: `aria-plugin-benchmarks/ab-suite/state-scanner.json` 全文对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` **四词零命中** (连 `handoff` 一词也是 0) —— 即使想跑也测不到本 collector; 对它跑全套件 = 测量剧场 (memory `feedback_static_benchmark_unfit_as_oneshot_selection_gate` 同族)。
- **substitute 覆盖 (R1 rework 收紧措辞)**: **baseline-failing 实体** = SC-1 / SC-3 / SC-4 (后半) / SC-5 / SC-6 / SC-8 (后半) / SC-9 / SC-13 / SC-14 九条, 每条附反事实。**回归锁 (baseline 上本就为绿, 非 baseline-failing)** = SC-2 (零行为变化)、SC-7 (现状记录性)、SC-4 前半、SC-8 前半; v1 称「SC-1~SC-9 逐条对应一个行为改动, 每条附反事实」失准, 但结论不倒 —— substitute 实体由上述九条撑住。SC-15 的性质随待复议 2 裁决而定。SC-10 守既有面; SC-11 守文档面; SC-12 是活体。
- **不豁免的部分**: 无。若 Phase B 期间发现需要改 SKILL.md 指令面 (例如新增「AI 见到 `unreadable_count > 0` 该怎么说」的处方), **立即改判照跑 AB** (宁跑勿豁), 并在 tasks 留痕。

---

## 待 owner 复议

> R1 rework 说明: 条目 1 已按实测重写 (原写法把现状包装成待定默认), 条目 2 为 R1 critical 新增且是 Phase B 的前置门, 原条目 5 (gitlink 时机) 因实况变化**已作废删除**。

1. **pointer 排除口径要不要从「任意深度」收窄到「只排顶层」** (推荐默认: **不收窄, 保持现状**)。实测确认: `301641b` 上 `archive/latest.md` **已经**被排除 (`:277` 取 basename → `:280` 比常量), 所以「任意深度」不是本 spec 引入的新行为, 而是**未成文的现状**; 本 spec 只把它写进 schema 文档。反对意见可能是「排除逻辑应只针对活指针, 归档目录下的 `latest.md` 是历史文件、应当进 tracks」——若采纳反对, 那是一次**行为变更**(需改代码 + 改 SC-8 前半为断言其进入 `tracks[]`), 不是保持现状。
2. **⚠️ `filename` 语义取舍: A 案 (改既有字段语义) vs A′ 案 (保持 basename + 另加 `relpath`)** —— R1 critical `63d1ce08` + decision `109b412c`, **Phase B 前置门**。事实面: (a) issue-195 正文第 41 行与 triage comment `:53` 两个来源的原文都是「`filename` 字段另派生 basename」, 本文 v1 称「issue 与 triage 均倾向此案 (A)」失实, 已订正; (b) A 案会让 D.3 写出的 pointer 被姊妹 collector `handoff.py` 读不回 (§5 详述, 机制已实读逐行确认), 影响正好落在本 spec 声称要服务的子目录采用方身上; (c) A 案改既有字段取值语义, 与 §7「additive-only / `snapshot_schema_version` 保持 1.0」的声明不相容。三条可选路径 (可组合): **(i) 采纳 A′** —— 兼容面最干净, 不新增失败面, 但子目录 pointer 往返的**既有**缺口不修; **(ii) 采纳 A 并同 cycle 一并修 `handoff.py::_parse_latest_pointer` (`:288` 剥目录段) 与 `_scan_md_files` (`:300,318` 非递归) 的扁平假设** —— 修复最彻底, 但本 spec 的触点面与测试面扩大到姊妹 collector; **(iii) 采纳 A 但限定 `latest_md_writer` 只在顶层 track 时写真指针** —— 折中, 子目录采用方拿不到 pointer 语义权威。**无论选哪条, 都必须补 SC-15 的往返断言, 并按结果订正 §5 该行与 Impact 首行的「不再恒 exit 10」措辞**; 若选 (i) 或 (iii), 还须为遗留缺口另开 issue。另请一并裁定: 若最终选 A, `snapshot_schema_version` 是否 bump。
3. **`unreadable_count` 是否值得新增字段** (推荐默认: 新增)。替代方案是只留 soft_error, 但那样「有多少文件读不到」就只能靠数 errors 文本, 不可机读。
4. **dedupe tie-break 是否要在本 spec 内改成「路径深度浅者优先」** (推荐默认: 不改)。它是既有设计的一部分, 本 spec 只钉现状 (SC-7) 并订正 schema `:1125` 那条在相对路径下已变假的论据; 改排序语义应另起, 否则本 spec 的反事实边界会糊掉。
5. **`_get_file_commit_date` 的 mv 日残余是否本 spec 处理** (推荐默认: 不处理, 但要写进 CHANGELOG 的已知边界)。#195 报告方归档进 `archive/` 的正是老格式 (无 frontmatter) 交接, 他们抱怨的「日期是归档日不是会话日」那一半**路径修好后依然存在** (§Why 与 SC-4 已实跑证明, `--follow` 也救不了「最近一次触碰该路径」的语义)。真要修只能换语义 (例: 取该路径的**最早**提交日, 或引入 `--diff-filter=A`), 属另一件事。裁决前 Phase B **不得**给该函数加 `--follow` (那既不解决问题又改了语义)。
6. **版本号**: PATCH。起草时远端已有 tag v1.71.1, 故候选 **v1.71.2**; bump 前须 `git -C aria ls-remote --tags origin` 复核并读同伴 handoff 的 `<vNEXT>` (memory `feedback_concurrent_release_numbering_check_remote_tags_and_sibling_vnext`)。

---

## References

- SOT (@`301641b`): `skills/state-scanner/scripts/collectors/handoff_multibranch.py:14-31,42,177-178,240-288,293-308,310-327,329-336,428-457,586-596,619-626,637-700` · `scripts/scan.py:119-120,126-210,255` (F1) · `scripts/collectors/handoff.py:269-330,380-410,438-440` (pointer 往返, R1 critical) · `scripts/collectors/_common.py:411-412` (`_run` 编码) · `scripts/writers/latest_md_writer.py:110-143,205-217,259` · `scripts/renderers/track_board.py:183,188,254,559` · `references/state-snapshot-schema.md:1074-1136` · `references/json-diff-normalizer.md:241` · `SKILL.md:117,149,153`
- 规范: `standards/conventions/skill-benchmark-exemption.md` (Rule #6 判据表) · `standards/conventions/session-handoff.md` §2.3 (frontmatter 契约) · `standards/conventions/version-management.md` §4.3 + 主仓 CLAUDE.md「发布同步面」(Task 5.1) · `standards/openspec/templates/proposal-minimal.md`
- 闸门: `.aria/state-checks.yaml:88` `m6-version-badge-match` · `:141` `i18n-readme-translation-currency` · `:372` `plugin-version-arch-docs-match` (三条均 `enabled: true`, 兜底 Task 5.1)
- 先例: `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/` (同 collector 家族, 冻结语料 + 反事实测试形态) · `openspec/archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md` (Level 2 标杆)
- 现场: Aria#195 issue 原文 (第 21 行点名 `_get_file_commit_date`, 第 41 行 A 案原文) · `.aria/triage-comment-195.md` (`:53` 修法倾向) / `.aria/triage-report-195.json` (2/2 复现) · 起草时临时仓 `git ls-tree` 转义实跑 (F2) · R1 rework 期 hermetic 复跑 (F2 静默漏扫 / pointer 任意深度 / mv 日期三处) · aria-plugin#155 (dedupe 由来, closed)
- R1 审计: `.aria/audit-reports/post_spec-R1-2026-09-06T154800-000Z-R1-handoff-multibranch-subdir-path-fidelity-aggregated.md` + 同前缀 5 份单席报告
</content>
