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
> **Rule #6 判定 (R2 rework 改判: 照跑 AB, 不豁免)**: 变更本体仍是 **纯代码 + schema 文档描述** (无 `description` 变动, 无 SKILL.md 文本变动; SKILL.md 出现 `tracks_multibranch` 共 **3 处**: `:117` collector 清单、`:149` 与 `:153` coordination 闸门接线, 本 spec 三处均不改)。**但 v3 的两条免跑支撑证据经 R2 五席实测双双不成立**: (1) 「四词零命中」为假 —— `ab-suite/state-scanner.json:214` 对 `tracks_multibranch` **命中 1 次** (5/5 席各自 grep; 文件今 17551 B, 该用例由 `5697477` 2026-09-05 引入), 另三词确为 0; (2) 「闸门面不受影响」为假 —— 本次 rework hermetic 实跑: 同一 track_id、异 `owner_container` 的「顶层 active + `archive/` active」临时仓, 改前 `collision.kind = none` (子目录件恒 legacy ⇒ `owner_container: unknown` 被 collidable 过滤排除), 路径修好后 = **`cross_owner`** (groups 1) —— 而 `collision.kind != none` 正是 `SKILL.md:149/153` 闸门与 `advanced-rules.md:544` 规则 1.54 的触发条件本体。⇒ 落判据表**第四行「拿不准」⇒ 照跑** (CLAUDE.md Rule #6; Rule #10 禁 AI 以「代码面 / 成本」自行豁免)。**处置 = 照跑 state-scanner AB + 开套件缺口 issue + 保留全部 substitute SC** (三者并做, 不取其一)。rule6_note 见文末
> **A.1.0 头脑风暴**: 未跑 — `audit.checkpoints.post_brainstorm = off` (Rule #10 白名单第一类)
> **审计计划**: post_spec convergence 5 席 (config enabled) → post_planning convergence (config enabled); mid_implementation / post_implementation / pre_merge / post_closure 均 config 显式 off (白名单第一类)
> **审计轨迹**: post_spec R1 (2026-09-06) 票型 **REVISE 5 / PASS 0** (单席 verdict: FAIL 3 + PASS_WITH_WARNINGS 2), verdict **FAIL** —— Critical 2 / Major 15 / Minor 10 (+ 6 decisions, 其中 1 条 major); 聚合报告 `.aria/audit-reports/post_spec-R1-2026-09-06T154800-000Z-R1-handoff-multibranch-subdir-path-fidelity-aggregated.md`。**本文件为 v3 (R1 rework → 2026-09-07 A′ 裁定)**: 全部 critical / major 已逐条处置, 处置记录见 rework 表 (scratchpad `handoff-multibranch-subdir-path-fidelity-rework-R1.md`); 两条 conflicted 已用机械证据闭合 (见头部主仓实况行与 SC-10)。**v3 增量 (2026-09-07)**: 前置门 critical `63d1ce08` 裁定为 **A′ + 写侧守卫** (决策单 `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md`, AI 在 owner 不在场时裁, 待追认); 同时**订正 R1 的一处结论** —— R1 写「A′ 不会新增 pointer 失败面」经实读 `latest_md_writer.py:78-95` 证伪 (legacy 行不入 pointer 候选集, 路径修好后子目录 track 转 active 即入选), 两案都新增, 故守卫是必需项。新增 §2.5 (守卫设计) / Task 2.5 / Task 5.3 (遗留缺口开 issue); SC-15 收敛为顶层与子目录两个布局 + 两条反事实
> **审计轨迹 (R2)**: post_spec R2 (2026-09-07) 票型 **REVISE 5 / PASS 0** (单席 verdict: FAIL 3 + PASS_WITH_WARNINGS 2), verdict **FAIL** —— **Critical 3 / Major 10 / Minor 9** (+ 9 decisions, 全部 minor, 不计入); 去重前 55 / 去重后 31; R1 的 27 条缺陷类**无一被重开** (交集 0), 新缺陷全部落在 v3 增量 (A′ 裁定 + §2.5 守卫 + 新增 SC-13/14/15) 的下游或 R1 未测到的机械事实。聚合报告 `.aria/audit-reports/post_spec-R2-2026-09-07T004500-000Z-R2-handoff-multibranch-subdir-path-fidelity-aggregated.md` + 同前缀 5 份单席报告。**本文件为 v3 → v4 rework (R2, 2026-09-07, 非原作者执笔)**: 3 critical + 10 major 逐条处置于正文 (非批注), 9 minor 全部顺手订正; 处置记录见 scratchpad `handoff-multibranch-subdir-path-fidelity-rework-R2.md`。**R2 唯一 conflicted 项 `cecc06af` (闸门面是否受影响) 已由本次 rework 的 hermetic 实跑机械闭合 —— qa-engineer 一侧成立** (`collision.kind` none → cross_owner), 连带改判 Rule #6 为照跑 (见上行) 并重写 §5 collision 行与 rule6_note。**字段更名 (R2 minor `4835b148`)**: 决策单原名 `relpath` → 本文统一为 **`rel_path`**, 对齐本 schema 多词键的下划线口径 (`legacy_count` / `owner_container` / `identity_advisories` …; 插件 1.71.1 全树 `\brelpath\b` 零命中, 无先例可援)。决策单原文写 `relpath`, 以本文为准, 追认时一并确认。**rework 收口复核 (同一 R2 轨, 换非作者执笔, memory `feedback_author_and_verifier_must_differ_for_corrections`)**: 三项载重实测独立复跑一致 —— (1) SC-10 五模块在真 checkout `301641b` 得 `Ran 102 tests … OK` (四模块 78, 差值 24 = `test_p1_layer_h`); (2) `cecc06af` 的 hermetic 临时仓改前 `collision.kind=none`/`groups 0`/1 条 `git_show_failed`, 改后 `cross_owner`/`groups 1`/零 soft_error (A 与 A′ 两种回填形态各跑一次, 结论同 —— 两行落在不同 `(track_id, owner/container)` 组, `filename` 不参与判定); (3) Task 5.1 的 16 个版本点逐处 `grep -n` 命中、行号全对。**同时修掉 rework 自身引入的一处硬伤**: §2.5 / Task 2.5 / SC-15 的守卫判据代码写作 `track.get("relpath")`, 与本次采纳的字段名 `rel_path` 不符 ⇒ 照写则该键**恒取不到** ⇒ `rel` 恒等于 `filename` ⇒ 守卫恒不触发 (与 `88a49037` 要防的失效同型, 只是方向相反), 已全文更正为 `track.get("rel_path")`

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
| **A′ ✅ 采纳 (+ 写侧守卫)** | 枚举层同样交出相对路径, 但**`filename` 字段仍派生 basename**, 另加 additive 字段 `rel_path` 承载相对路径, 供 `_read_file_content` / `_get_file_commit_date` / `_make_legacy_track_id` / `scan.py:186` 消费; **并给 `latest_md_writer._render_pointer` 加写侧守卫** (见 §2.5) | issue-195 正文第 41 行 A 案原文:「`filename` / `track_id` 等需要 basename 的字段**另行派生**」; triage comment `:53`:「`filename` 字段另派生 basename」。兼容面最干净 (既有消费方语义不变, `snapshot_schema_version` 的 additive-only 声明也才成立), 且不触发 A 案的两处下游副作用 (dedupe tie-break / schema `:1125` 论据变假)。**代价**: `scan.py:186` 与 `latest_md_writer` 需显式改用新字段; 子目录采用方本轮只拿降级 pointer, 遗留缺口另开 issue。裁定见 `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md` |
| B | `ls-tree` 去掉 `-r`, 只扫顶层 | 语义最简, 但**静默丢弃**子目录里的全部交接历史。把归档放子目录的采用方等于那段历史不进看板 —— 用"看不见"换"不报错", 与本 collector 的用途 (多终端交接发现) 直接冲突 |
| C | 保留 `-r`, 显式 `continue` 掉非顶层项 | 行为同 B, 只是把意图写进代码。仍然丢历史; 且它把「递归枚举」这个正确动作退回去, 而真正错的是下游拼路径 |
| D (附加, 采纳) | git show 失败不再降级为 legacy track, 只报 soft_error | 与 A/A′/B/C 正交。issue 明确提出; 「读不到」与「老格式」是两件事, 折叠它们让失真数据带着误导性 `updated_at` 进看板 |

> **A vs A′ 已裁定 (2026-09-07, AI 裁定 + 待 owner 复议)**: 取 **A′ + 写侧守卫**, 决策单 `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md`。本文 v1 直接采纳 A 且称「issue 与 triage 均倾向此案」——**该转述失实**, 两个来源的关键分句都是「`filename` 另行派生 basename」(R1 已订正)。
>
> ⚠️ **裁定同时订正 R1 的一处结论**: R1 rework 在 §5 写「A′ 案不会新增这条 pointer 失败面」——**该断言不成立**。实读 `latest_md_writer.py::_get_active_tracks` (`:89-95`, docstring `:78-81`): 候选集只收 `status == "active"`, legacy 行被有意排除。今天子目录文件恒为 legacy ⇒ 永不被选为 pointer; **A 与 A′ 修好路径后它都会变成 active track 而进入候选集**, 于是 A 写出带目录的路径、A′ 写出顶层不存在的 basename —— 两案都断在 `handoff.py` 的非递归候选集上 (`:300,318` `iterdir()`, `:389` 按 `p.name` 建索引), 只是断点不同。**⇒ 写侧守卫在两案下都是必需项**, 不是「(iii) 折中」的可选装饰。
>
> 下文 §What / §5 / §7 / SC 凡涉及 `filename` 取值语义处, 保留 A / A′ 两分支的对照记述 (供复议时对比), 但**实施以 A′ 为准**。

---

## What

### 1. 枚举层 `_list_handoff_files` (`:240-288`)

| | 改前 | 改后 |
|---|---|---|
| ls-tree 调用 | `git ls-tree -r --name-only <ref> -- docs/handoff` | 加 `-z` (NUL 分隔, 关闭引号转义); 按 `\0` 切分, 空段丢弃 (F2) |
| 每项取值 | `basename = Path(path).name` (`:277`) | `rel` = 相对 `docs/handoff/` 的路径。**前缀剥离必须从常量派生**, 不得新写字面量 (`rel = path[len(_HANDOFF_TREE_PATH) + 1:]` 或 `PurePosixPath(path).relative_to(_HANDOFF_TREE_PATH)`) —— 写死 `path[len("docs/handoff/"):]` 等于新造**第五处硬编码前缀**, 正是本 spec 认定的根因族 |
| 前缀守卫 | 无 | 不以 `docs/handoff/` 开头的行 (理论上不会出现) 计一条 soft_error 并**只跳过该行**。**kind 定名 = `handoff_multibranch_unexpected_path_prefix`** (R2 minor `e9f28dc8`: 本 collector 现有四个 kind 全为 `handoff_multibranch_*` 且是机读契约的一部分, `:587,607,623,643`; 不定名则实现可能复用 `..._ls_tree_failed`, SC-9 仍绿而消费方分不清「整支分支失败」与「单行前缀异常」), 须登记进 schema (§6.1)。**契约变更 (R1 rework 补)**: 现签名 `tuple[list[str], str \| None]` 只有**分支级**错误通道 —— 主循环 `:619-626` 收到非 None 即 `soft_error("handoff_multibranch_ls_tree_failed")` 后 `continue`, **整支分支的已枚举文件全部丢弃**。要表达「跳过该行、其余照常」必须改签名 (例: 第三个返回位携带 per-item 错误列表) 或向函数注入 reporter。此契约变更由 Task 2.1 承接, 由 SC-9 的第二条断言钉住 |
| `.md` 过滤 | 对 basename 判 `.endswith(".md")` (`:278`) | 对 `rel` 的 **basename** 判 (语义不变; `-z` 之后不再有尾引号, F2 的漏扫随之消失) |
| pointer 排除 | `basename == "latest.md"` (`:280`) | **不变 —— 现状即任意深度** (R1 rework 订正)。`:277` 先取 basename、`:280` 再比常量, 所以 `archive/latest.md` 今天**就已经**被排除。hermetic 实测: 含 `docs/handoff/latest.md` + `docs/handoff/archive/latest.md` 的临时仓上跑基线循环, 两者均 `DROPPED(pointer)`。本行不是行为变更, 只需把该口径**补写进 schema 文档** (今天未成文) |
| 返回 | `list[str]` basename | **A 案**: `list[str]` 相对路径 (平铺仓两者逐字节相同) / **A′ 案**: 相对路径供内部拼 ref, `tracks[].filename` 另派生 basename |
| docstring (`:246-247`) | 「Returns only the basename … so callers compose the full git-object path as needed」 | 改为「Returns each file's path **relative to `docs/handoff/`** …」—— 契约与实现对齐 (根因就在这句自述上) |

### 2. 三个仓内调用方改用相对路径 (语义不变, 只是不再丢信息)

- `_read_file_content:301`: `ref = f"{_REMOTE}/{branch}:{_HANDOFF_TREE_PATH}/{rel_path}"` (拼法不变, 入参含义变准)。**这一处才是同名串读 (§Why 后果 3) 的修复点**
- `_get_file_commit_date:321`: 同上。**真实收益 (R1 rework 订正)** = (a) 「从未在顶层存在过」的子目录文件, `updated_at` 从**空串**变成真日期 (hermetic 实测); (b) `git show` 成功后走 frontmatter 分支, 根本不再落到这个 fallback。**mv 过的无 frontmatter 文件仍取 mv 提交日** —— 路径正确后依然如此, 与 SC-4 一致, 不是本 spec 的修复承诺 (v1 此处写「不再取到 mv 提交日」系误断, 已实跑证伪)
- `_make_legacy_track_id:329-336`: `legacy:<branch>:<rel_path>` —— 用相对路径而非 basename。今天 `docs/handoff/x.md` 与 `docs/handoff/archive/x.md` 会产生**同一个** `legacy:<branch>:x.md`, 两行连内容都完全相同 (§Why 后果 3 的串读), 于是 `tracks[]` 里出现一对**机读上不可区分**的行: 同 `track_id`、同 `filename`、同 `updated_at`、同 `branch`, 消费方无法判断这是两份文件还是一份被重复计数。**R2 订正 (`3cb2cf2b`)**: v3 此处原写「被 `dedupe_latest_per_track_container` 当成同一 track 折叠」——**该后半为事实错误**。`status == "legacy"` 的行在 `handoff_multibranch.py:521-524` 被 `continue` 掉、**从不进入分组**, 所以两条 id 完全相同的 legacy 行今天也不会折叠 (实测 2 行进 → 2 行出, `legacy_passthrough=2`); 该透传行为在 docstring `:493-499` 与 `state-snapshot-schema.md:1128` 都是明文契约。真实危害是上句的「不可区分」而非折叠。由 SC-13 覆盖

> A′ 案下本节三个函数的入参改名为 `rel_path` 不变, 变的只是 `tracks[]` 里回填哪个值。

### 3. `scan.py:186` (F1, 跨文件消费方)

**A 案**: `f"docs/handoff/{filename}"` 保持字面不变即可正确 —— 因为 `filename` 现在就是相对路径。**A′ 案**: 该行必须显式改读新的 `rel_path` 字段, 否则 F1 仍然静默失效。

无论哪案, **必须有测试钉住这个隐式耦合**: 该行与 collector 的 `_HANDOFF_TREE_PATH` 是两处独立字面量, 今天靠巧合一致。SC-6 用一条断言把它锁住 (子目录 track 的 ancestry 检查必须真的执行到 `git log` 并拿到非空 SHA, 而不是拼错路径后返回空再 `continue`)。

### 2.5 pointer 写侧守卫 (`writers/latest_md_writer.py::_render_pointer`) — A′ 裁定的必需配套

| | 改前 | 改后 |
|---|---|---|
| 选取 | `_get_active_tracks` (`:89-95`) 只收 `status == "active"`; 子目录文件今天恒为 `legacy` ⇒ **永不入选** | 不变 (本 spec 不动选取逻辑) |
| 写指针 | `_render_pointer` (`:143`) 无条件写 `**Latest**: [{filename}](./{filename})` | **仅当 `rel_of(track) == filename`** (该 track 的文件在 `docs/handoff/` 顶层) 才写真指针; 否则走 `_render_pointer_unavailable` 分支 |
| **`rel_path` 缺失语义 (R2 critical `6f8fa9f7`, 4/5 席)** | 无此字段 | **缺键 ⇒ 按 `rel = filename` 处理 (即视为平铺世界), 照写真指针**。判据必须写成 `rel = track.get("rel_path") or track.get("filename")` 再比 `rel == filename`, **不得**写成 `track.get("rel_path") != filename` |
| 降级文案 | `_render_pointer_unavailable(track_id, now)` (`:151`) 现只有一条硬编码原因「active track 数据缺少 filename 字段」(`:164`) | **签名变更**: 增加一个原因入参 (例 `_render_pointer_unavailable(track_id, now, reason)`) 或新增姊妹函数, 使「目标在子目录」有专属文案 —— 现签名与硬编码文案装不下第二个原因。文案须写明: 目标在子目录 (`rel_path`), 姊妹 collector `handoff.py` 的候选集非递归 (`:300,318` `iterdir()`, `:389` 按 `p.name` 建索引), 写出去也读不回 —— **必须写明原因, 不得静默退化** |

**为什么必需 (不是折中)**: 见 §候选方案表下方的裁定注 —— 路径修好后子目录文件会从 `legacy` 变成 `active` 而进入 pointer 候选集, A 与 A′ 都会写出 `handoff.py` 解析不回的目标。守卫的判据用 **`rel == filename` 这一数据事实**, 不要用 `"/" in filename` 之类的字符串嗅探。

**⚠️ 缺键必须显式兜底 (R2 critical `6f8fa9f7`, backend-architect 执行探针 + 三席同判)**: `_render_pointer` 读的是 track dict (`latest_md_writer.py:143` 起), 若判据写成 `track.get("rel_path") != filename`, 则**任何没有 `rel_path` 键的 track 都恒真** ⇒ 一律走 `_render_pointer_unavailable`, 而该函数只渲染 `track=<track_id>`、**不含文件名** (`:151-169`)。三层后果:

1. **既有夹具立刻翻红**: `tests/test_p1_layer_h.py:230-240` 的 `_active_track()` 是八字段 dict (`track_id` / `owner_container` / `phase` / `status` / `updated_at` / `branch` / `filename` / `legacy`), **无 `rel_path`**; 用它跑打了守卫的 `write_latest_md`, 指针行退化成 `**Latest**: (pointer 不可用) — track=my-spec`, `:270` 的 `assertIn("2026-05-20-my-spec.md", content)` 由绿转红。该模块当前基线为绿 (真仓 checkout `301641b` 实跑 `Ran 24 tests … OK`), 且它是**全插件树唯一 import `write_latest_md` 的测试** ⇒ 已并入 SC-10 点名集 (R2 minor `7cba5aa4` 同处)。
2. **跨版本读盘 (真实生产触发路径)**: `session-closer/SKILL.md:90` 明确允许「跑 `scan.py` 取 snapshot **或读既有 `.aria/state-snapshot.json`**」; 升级前写下的快照每行 track 都没有 `rel_path` ⇒ **平铺仓 (含 Aria 自身) 每条 active track 都会被判「在子目录」**, 真指针被吞、写出一条理由为假的降级横幅, `handoff.py` 随即由 pointer 退回 mtime —— 正好**重开 H5「pointer 是语义权威」那条既有修复** (与 R1 critical `63d1ce08` 同族, 触发条件从「子目录布局」换成「快照跨版本」)。
3. **SC-15 结构上覆盖不到该分支**: 其两个布局都在同一次运行里由新 collector 端到端产出, `rel_path` 恒在。故 SC-15 补第三条断言 (g) 专覆盖缺键。

**⚠️ 生产可达性 —— 守卫落点当前零生产调用点 (R2 critical `d1f01126`, 4/5 席; 待 owner 复议)**: `write_latest_md` 在插件 1.71.1 全树的命中集 = 函数自身 (`latest_md_writer.py:259`) · `writers/__init__.py:9,12,14` 再导出 · `tests/test_p1_layer_h.py` (5 处调用) · 两份 reference 文档 —— **排除 `tests/` 后无任何生产调用方** (本次 rework 实跑 `grep -rn 'write_latest_md'` 复核)。这不是遗漏而是既有设计决定: `references/phase-1-collectors.md:95` 逐字写「`latest_md_writer` 是 **deliberately D.3-scoped** —— 不在 scan.py 内自动触发, **不在 P1 内引入 production call-site**」, `:104` 把 D.3 集成推给「TASK-029 或独立 follow-up」(至今未落地), `references/layer-l-integration.md:101,107` 同。**生产 D.3 的 pointer 写入是 AI 按处方指令手改**: `phase-d-closer/references/handoff-mechanics.md:114-124` 的 3 行决策表 (读 `tracks_multibranch.exists` / `len(tracks)` / 「其他 container 有 `status==active`」), 且该文档 `:4` 声明自己是 phase-d-closer 与 session-closer **共享的 handoff-write 机制 SOT**; 两个 closer 目录对 writer 零引用。本仓 `docs/handoff/latest.md:103-107` 自记「机械 `latest_md_writer` 当前不可用」并声明这是一处对约定的**有意偏离**。

⇒ 三条必须据此重述, 已就地改掉: (a) Impact.Risk 的缓解承诺「使这类指针压根不写出」在**生产路径上今天为假** —— 守卫只覆盖机械 writer 这条路, 属 memory `feedback_completion_signals_vs_runtime_invocation` 形态; (b) §待复议 2 向 owner 要的「子目录采用方只拿降级 pointer」这个代价, **目前无人在付** (没有生产调用点就没有人被降级), owner 应据此重新估价; (c) 若 owner 要求**真修生产面**, 落点是 `handoff-mechanics.md:114-124` 的处方决策表 = **运行时指令面** ⇒ Rule #6 判据表第二行, AB **必须照跑**且范围扩到 phase-d-closer / session-closer。四席**都不主张撤掉守卫** (writer 是已发布的公开 API, 一旦接线即命中; 且守卫是 A′ 裁定的组成部分), 只要求把可达性写明 —— 本行即是。

**遗留缺口**: 让 `handoff.py::_parse_latest_pointer` (`:288` 剥目录段) 与 `_scan_md_files` (`:300,318` 非递归) 支持子目录 = 原选项 (ii), 由 Task 5.3 开 issue 独立立项, 不并入本 Level 2。子目录采用方本轮拿到的是**诚实降级**: 有横幅 + 原因, 而不是一个静默失效的指针。

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
| `scan.py:186` `_same_branch_head_unreachable_tracks` | `git log … -- docs/handoff/{filename}` | F1, 见 §3 —— A 案下字面不变即可用, A′ 案下必须改读 `rel_path` |
| `writers/latest_md_writer.py:143` (`_render_pointer`, 由 `write_latest_md:259` 调用) | `**Latest**: [{filename}](./{filename})` | ⚠️ **A 案下这是本 spec 引入的新失败面** (R1 critical, 4 席一致; v1 此行原写「相对路径天然正确 / 无影响」——只对**人类点击的 markdown 链接**成立, **机器读回链没追**)。姊妹 collector `handoff.py` 仍是扁平世界: `_parse_latest_pointer` 在 `:288` 用 `Path(target).name` 剥掉目录段, 候选集 `_scan_md_files` (`:300`) 用 `iterdir()` **非递归**扫描 (`:318`), 匹配又按 `p.name` 建索引 (`:389`)。于是 D.3 写出 `[archive/x.md](./archive/x.md)` 后: (a) 顶层还有旧交接时 ⇒ `handoff_pointer_target_missing` soft_error (`:399`) + `latest_source` 由 pointer 退回 mtime ⇒ `scan.py` 继续 exit 10, 且重开了 H5「pointer 是语义权威」那条既有修复; (b) 全部交接都在子目录时 ⇒ `canonical_files` 为空 ⇒ `handoff.py:438-440` 直接 `exists: False` 且**零 soft_error**, 两个 collector 在同一快照里互相矛盾而无任何信号。**订正 (2026-09-07 裁定时实读): A′ 案同样会新增这条失败面** —— `_get_active_tracks` (`:89-95`) 只收 `status == "active"`, 今天子目录文件恒为 `legacy` 故永不入选; 路径修好后它变成 active track 而**进入候选集**, A′ 写出的 `./x.md` 在非递归候选集里同样查不到 ⇒ 同一条 `handoff_pointer_target_missing`。断点不同, 后果同型。**⇒ 已采纳 A′ + §2.5 写侧守卫**, 由 SC-15 端到端钉住。⚠️ **可达性限定 (R2 critical `d1f01126`)**: 上述「D.3 写出」为**机械 writer 路径**的推演, 而 `write_latest_md` 今天**零生产调用点** (`phase-1-collectors.md:95` 的既有设计决定); 生产 D.3 的指针由 AI 按 `handoff-mechanics.md:114-124` 手改 ⇒ 这条失败面**目前只在测试与未来接线时可达**, 不是今天正在发生的损坏。详见 §2.5 可达性块 |
| `writers/latest_md_writer.py:208-217` | legacy 表展示 `filename` 列 | A 案: 展示相对路径, 更准; 平铺仓不变。A′ 案: 不变 |
| `handoff_multibranch.py:428-457` `_dedupe_sort_key` | 4 级键第 3 级按 `filename` 字典序取大 (`:455`) | **A 案有行为面**: `archive/…` (`a`=0x61) 字典序大于 `2026-…` (`2`=0x32), 故同 `(track_id, identity_key)` 且 `updated_at` 完全相同时, 归档副本会赢。仅在该三重并列时可达; 归档件通常更旧 ⇒ 记入 Impact.Risk, 由 SC-7 钉住现状行为。**A′ 案下的实况 (R2 minor `16e07a83` 订正, v3 原写「A′ 案下无此面」过强)**: A′ 保留 basename, 故**字典序翻转**风险确实消失 (第 3 级仍吃 basename, 归档副本不会因 `archive/` 前缀而赢); 但它把 **tie 的可观测性打开了** —— 同 `(track_id, identity_key)`、同 `updated_at`、同 `branch`、同 basename 而目录不同的两行, 四级键 `(parse_ok, updated_at, filename, branch)` (`:428-455`) **全部并列**, `max()` 回退到迭代顺序, 与 `_dedupe_sort_key` docstring `:438-452` 与 schema `:1126` 宣称的「a pure function of the row's own fields / invariant to build order」相悖 (那正是 round 3 finding [M1] 建立的不变量)。改前这两行因串读逐字段相同, 选谁都一样; **改后 `rel_path` 不同 ⇒ 两行读到的是不同文件 ⇒ 代表行的 `status` / `phase` 可能不同**, 经共享 dedupe 传导到 collision 与看板。触发窄但不是不可达 (schema `:1125` 自述本仓真出现过同日 date-only 并列)。是否把 `rel_path` 加进排序键 = §待复议 4 附问 |
| `renderers/track_board.py` | 不读 `filename` **字面** (`:254,559` 的 HANDOFF 列只吃 `updated_at`), 但 `:183,188` 直接 import 并应用 collector 的 `dedupe_latest_per_track_container` | **不是「无影响」(R1 rework 订正)**: 经共享 dedupe 的四级排序键第 3 级 (`filename`) **间接消费** ⇒ 上一行的 tie-break 风险同样落到看板 collision 输入的代表行选择上, 而同组两行的 `status` / `phase` 可以不同 ⇒ 渲染随之改变。实际差异在三重并列下近乎为零, 语义由 SC-7 一并覆盖, 本 spec 不另加断言 |
| `skills/state-scanner/lib/collision.py` (Layer L 包, **不是** `scripts/lib/`) | 按 `track_id` / `identity_key` 分组, `classify()` 出 `collision.kind` | ⚠️ **受影响 (R2 conflicted `cecc06af`, 本次 rework hermetic 实跑闭合 —— 只算减法的旧结论被推翻)**。旧结论「不受影响」只量了**减法** (删掉的假 legacy 行 `owner_container` 恒 `unknown`, 被 `:480-486` 的 `collidable` 过滤排除 —— 这半仍然成立), **没量加法**: 路径修好后, 子目录里带合法 frontmatter 的交接会带着**真 `owner_container`** 进入 collidable 集。实测 (临时仓: 顶层 `2026-09-01-x.md` = `simonfish/c1` active + `archive/2026-09-02-y.md` = `aria-runner-bot/c2` active, 同 `track_id`): 改前 `collision.kind = none` / `groups 0` / 1 条 `handoff_multibranch_git_show_failed`; 改后 **`collision.kind = cross_owner` / `groups 1` / 零 soft_error**。⇒ `exists` / `len(tracks)` / `legacy_count` 之外, **`collision.kind` 也是本 spec 会改动的量**, 下面三行的处方性消费方随之全部在射程内 |
| `SKILL.md:149` / `:153` coordination 闸门接线 | 触发条件读 `collision.kind` | ⚠️ **受影响** (上一行实测)。本 spec 不改这两行的**文本**, 但改变它们看到的**值** ⇒ Rule #6 由 substitute 改判**照跑**, 见头部 Rule #6 行与文末 rule6_note |
| `references/rules/advanced-rules.md:443-444` (`multi_terminal_follower_detected`) · `:511-512` (D.3 follower 规则) · `:544` (规则 1.54 `concurrent_churn_detected`) | 前两条读 `tracks_multibranch.exists: true` + `len(tracks_multibranch.tracks) >= 2`; `:544` 读 `collision.kind != none` | ⚠️ **受影响, 且全是处方性 AI 判定面** (R2 major `cecc06af`)。§4 把「读不到」的行移出 `tracks[]` 同时改动 `exists` (= `len(tracks) > 0`, `handoff_multibranch.py:748`) 与 `len(tracks)`: 子目录仓里「一份读不到的假 legacy 行」被删后可能使 `len(tracks)` 由 2 降到 1 ⇒ follower 规则不再触发; 反向地, 子目录件转真 track 又可能使 `collision.kind` 由 `none` 翻到 `cross_owner` ⇒ 规则 1.54 开始触发。两个方向都要在 CHANGELOG 写明 |
| `RECOMMENDATION_RULES.md:28` (规则 1.51) · `:31` (规则 1.54) | 同上两量的规则表登记行 | ⚠️ **受影响**, 与 `advanced-rules.md` 是同一判定的两份登记面, 须一并复核措辞 (本 spec 不改判定逻辑, 只是其输入变了) |
| `phase-d-closer/references/handoff-mechanics.md:116-121` (D.3 pointer 决策表) | 读 `tracks_multibranch.exists` / `len(tracks)` / 「其他 container 有 `status==active`」 | ⚠️ **受影响, 且这是 pointer 写入在生产上的真实落点** (§2.5 可达性块): 机械 writer 零生产调用, D.3 指针由 AI 按这张表手改。三个量本 spec 全动。**本 spec 不改这张表** (改它 = 动运行时指令面 ⇒ Rule #6 范围扩大), 但必须在此登记, 并由 §待复议 2 交 owner 裁是否本 cycle 一并动 |
| `phase-d-closer/scripts/fetch_gate.py:175-188` | `run_fetch_gate(..., collision_kind=...)` 吃 `tracks_multibranch.collision.kind` 出 verdict | ⚠️ **受影响** —— 与上面 `collision.kind` 翻转同源。fail-soft advisory, 不会崩, 但 verdict 会变 |

### 6. 文档同步 (Rule #3)

1. `references/state-snapshot-schema.md` §`tracks_multibranch` (`:1074` 起):
   - `:1110` `filename` 字段语义 (A 案改为「相对 `docs/handoff/` 的路径 (平铺仓 = basename)」; A′ 案保持 basename 并新增 `rel_path` 行)
   - 新增 `unreadable_count`
   - **`:1136` fail-soft 形状**补 `unreadable_count` (见 §4); **同一行顺带勘正既有漂移 (R2 minor `e03d8a32`)**: 该行现把 `collision` 写作 `{"kind": "none", "groups": []}`, 而代码早退 dict 实为三键 `{"kind", "groups", "identity_advisories"}` (`handoff_multibranch.py:593`) —— 本 spec 正是为「恒存在不变量在错误路径上要成立」才动这一行, 只补一半会留下另一个错误形状
   - 写明 pointer 排除口径 = 任意深度的 `latest.md` (今天未成文, 且是现状而非新行为)
   - 写明「git show 失败不再产生 legacy 行」
   - **新增 per-item 前缀守卫的 soft_error kind 登记 (R2 minor `e9f28dc8`)**: 定名 **`handoff_multibranch_unexpected_path_prefix`**, 与本 collector 现有四个 kind 的 `handoff_multibranch_*` 口径一致 (`:587,607,623,643` 的 `branch_list_failed` / `branch_cap` / `ls_tree_failed` / `git_show_failed`)
   - **`## Change history` 加一行 (R2 minor `e03d8a32` 第二半)**: 该表既有口径是每次 schema 变更加一行 (H5 pointer / #134 / #141 / Task 10.1 逐条在列, `:1156-1168`), 本 spec 新增 `unreadable_count` + `rel_path` 两个字段, 必须登记, 并写明 `snapshot_schema_version` 保持 `"1.0"` (纯 additive)
   - ~~**`:1125` tie-break 论据订正**~~ **⇒ R2 删除该必做项 (`e3ca1e1a`)**: 现文「Handoff filenames are `YYYY-MM-DD-...`-prefixed, so the lexicographically greater name is also the later-authored one among same-day files」只在 `filename` 取相对路径 (A 案) 时才变假; **A′ 下 `filename` 恒为日期前缀 basename ⇒ 该句仍然为真** (三席各自实读原文复核)。照 v3 的无条件写法去「订正」= 把一条正确的不变量改成错的, 或往 schema 里写一条错误勘正。**若 owner 复议时改判回 A 案, 本条才恢复为必做项**
2. **collector 自身的机读契约 docstring** (`handoff_multibranch.py`, R1 rework 补): `:14-31` 的 top-level 键表缺 `unreadable_count`; `:42` 逐字写 `"filename": str,  # basename of the handoff file` (A 案直接推翻它); `:20` 的 `legacy_count` 注释「tracks that fell back to legacy (no frontmatter)」是 code/doc 早已不一致的那半 (代码在 git-show 失败分支同样 `legacy_count += 1`), 本 spec 改完该分支后正好使注释成真, 一并勘正
3. `references/json-diff-normalizer.md:241` 显式枚举了 `branches_scanned / legacy_count / collision / errors / exists` 键集 —— 补 `unreadable_count`
4. `:177` 的常量注释勘正 (「trailing slash required」与 `:178` 无斜杠的值不符)
5. CHANGELOG 记 Fixed 三条 (子目录 / 非 ASCII / 假 legacy) + Changed 两条 (`legacy_count` 语义收窄 / 子目录仓的 `collision.kind` 可能由 `none` 翻到 `cross_owner`, 见 §5)
6. **`standards/conventions/session-handoff.md:171-173` (Rule #9 SOT, R2 major `94935605`)** —— §2.5 的写侧守卫给 latest.md 派生行为引入**第三态**, 而该 SOT 现把它写成**穷尽两态**: 「**单 track 场景** (1 active track): `latest.md` 写当前 track 指针」/「**多 track 场景** (≥2 active): 仅 deprecation banner」。落地后「单 active track 但文件在子目录 ⇒ 不写真指针, 走降级并写明原因」使该无条件表述对子目录采用方为假。该文件在共享子模块 `standards/` 内, 影响所有采用方。
   - **本 spec 的处置 = 改, 不 defer**: 由 Task 4.4 承接, 只加第三态的条件从句, 不动前两态判据。
   - **实施面成本 (必须在 Tasks 里可见)**: Rule #5 允许「规范自身的变更落 standards 仓」, 但会带出 standards 子模块的独立 commit + 双推核验 + 主仓 gitlink bump (Task 5.2 已有 aria 子模块的同型动作, standards 是**第二条**同类链路)。
   - 若 Phase B 判定本轮不动 standards, **必须**在本文与 handoff 显式写成 deferred + 理由 + 跟踪 issue, 不得静默不改 (Rule #3 文档与代码同步)。

### 7. 向后兼容

- **平铺仓 (含 Aria 自身)**: `filename` / `track_id` / `legacy_count` 取值逐字节不变 —— 本仓 `docs/handoff/` 无子目录、无非 ASCII 文件名 (Task 1.1 机械核验)。既有冻结语料 `tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 与 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 因此不需重生成 (Task 1.1 同时核验其中无子目录路径)。
- **子目录仓**: 从「假 legacy / 静默漏扫 / 空 `updated_at`」变成「真 track + 真日期」, 是修复不是破坏。
- `unreadable_count` 为 additive 新键, 老消费方不读它即可。
- `rel_path` 同为 additive 新键 (每行 track 多一个键, 老消费方不读它即可)。**平铺仓恒有 `rel_path == filename`** —— 该不变量由 SC-16 钉住 (决策单 §落地约束第 1 条要求)。
- ⚠️ **`snapshot_schema_version` 处置 (A′ 采纳后已收敛): 保持 `"1.0"`, 纯 additive, 不 bump。** **R2 minor `b5d25ad4` 订正**: v3 附带的论据「A 案改既有字段取值语义**不属 additive**, 与保持 1.0 不相容」**与 schema SOT 自身不符** —— `state-snapshot-schema.md:46-48` 的 Additive / Breaking / Forward 三档只列「新增键 / 改名 / 改类型 / 删键 / 可选转必填 / 重构形状」, **取值语义变更不在任一档**; `:1070` 更有既有先例: `coordination_fetch.success` 的语义翻转明记「carried by plugin MINOR, **NOT** a `snapshot_schema_version` bump」。A 案未被采纳故该论据不载重, 但它同时出现在决策单第 2 条与 §待复议 2, **会污染 owner 的复议判断**, 故在此就地更正: 若 owner 改判回 A 案, 「是否 bump」应按上述先例讨论 (倾向不 bump + plugin MINOR 承载), 而不是按一句与 SOT 冲突的断言。
- ⚠️ **F2 的覆盖边界 (R1 rework 补)**: `_common.py::_run` 用 `encoding="utf-8", errors="replace"` (`:411-412`) ⇒ `-z` 方案对**可解码 UTF-8** 的路径成立; 真正非 UTF-8 字节的文件名解码即失真、拼不回 git 对象, 修后它从「静默漏扫」变成「新增一条 unreadable + 继续 exit 10」, 并非修好。姊妹 collector `handoff.py:318-322` 对同类文件名是**显式跳过**的既有先例。schema 与 CHANGELOG 须写明 F2 只覆盖「可解码 UTF-8 的非 ASCII 名」, 以免后续被当成回归。

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 子目录 / 非 ASCII 布局的采用方: `tracks_multibranch` 侧不再产生 `handoff_multibranch_git_show_failed` 与假 legacy 行, 子目录交接从「漏扫 / 假 track」变成真 track。**措辞定稿 (R2 rework 同步待复议 2 的裁定, `90a5604b`)**: 待复议 2 已裁为 **A′ + §2.5 写侧守卫**, 守卫使子目录目标的真指针压根不写出 ⇒ `handoff_pointer_target_missing` 在**机械 writer 路径**上不再产生。**承诺范围收窄到 kind 级 (R2 `112b4299`)**: 本 spec 承诺的是「子目录仓的 `tracks_multibranch` 侧不再产生 `handoff_multibranch_git_show_failed`」(SC-12b), **不承诺 `scan.py` 的具体退出码** —— 退出码是全部 collector soft_error 的聚合结果, 本 spec 只管其中一个 collector; 本仓平铺场景则断言「退出码与改前相同」(SC-12a)。**仍不承诺的部分**: (a) `handoff.py` 非递归候选集的本体缺口未修 (Task 5.3 另开 issue), 全子目录布局下两个 collector 的 `exists` 仍会不一致 —— 该不一致今天**零信号**, 属遗留; (b) 生产 D.3 的指针由 AI 手改而非机械 writer 写出 (§2.5 可达性块), 守卫覆盖不到那条路 |
| **Positive** | 看板不再混入内容串读的重复行与空/失真 `updated_at`; 「读不到」与「老格式」两个状态分开, 后续判据可分别处置 |
| **Positive** | 修掉一个跨文件静默失效点 (F1): AC-5 ancestry 检查对子目录交接从「拼错路径后无声跳过」变成真检查 |
| **Risk** | dedupe tie-break。**(a) 仅 A 案**: 第 3 级在 `archive/` 前缀下字典序变大, 三重并列时选中归档副本 —— A 案未采纳, 不载重。**(b) A′ 案实况 (R2 `16e07a83`)**: 字典序翻转风险消失, 但四级键 `(parse_ok, updated_at, filename, branch)` 在「同 basename 异目录」两行上**全部并列** ⇒ `max()` 回退迭代顺序, 违反 `:438-452` / schema `:1126` 宣称的 build-order 不变性; 改后两行读到不同文件 ⇒ 代表行的 `status` / `phase` 可能不同, 经共享 dedupe 传导到 collision 与 track_board。缓解: SC-7 钉现状 (标注为假想输入的特性化测试), 是否把 `rel_path` 加进排序键交 §待复议 4 |
| **Risk** | ⚠️ **`collision.kind` 可能由 `none` 翻到 `cross_owner` (R2 `cecc06af`, hermetic 实测)** —— 子目录里带真 `owner_container` 的交接转成真 track 后进入 collidable 集。它是 `SKILL.md:149/153` 闸门、`advanced-rules.md:544` 规则 1.54、`fetch_gate.py:175-188` 的触发条件本体 ⇒ 子目录采用方可能**突然开始**看到并发碰撞告警。**这是修复的正确后果 (以前是假阴性), 不是回归**, 但必须在 CHANGELOG 的 Changed 段写明, 否则会被当成本 spec 引入的噪声。缓解: §5 已登记全部处方性消费方; Rule #6 改判照跑 AB |
| **Risk** | `latest_md_writer` → `handoff.py` pointer 往返断裂 (§5 详述, R1 critical) —— **A 与 A′ 都会新增**, 因为路径修好后子目录文件从 legacy 变成 active track 而进入 pointer 候选集。缓解: 已裁定 A′ **并配 §2.5 写侧守卫**, 由 SC-15 两个布局 + 三条断言 + 两条反事实端到端钉住; 遗留的姊妹 collector 子目录支持另开 issue (Task 5.3)。⚠️ **缓解范围限定 (R2 critical `d1f01126`)**: 守卫只作用于机械 `write_latest_md`, 而该函数**今天零生产调用点** ⇒ 「使这类指针压根不写出」这句在**生产路径上为假** (生产 D.3 指针由 AI 按 `handoff-mechanics.md:114-124` 手改)。换言之: 本 spec 消除的是 writer 一旦接线就会命中的失败面, 以及「子目录采用方拿降级 pointer」这个**目前无人在付**的代价 —— owner 请据此重新估价 (§待复议 2) |
| **Risk** | `legacy_count` 语义收窄 (不再含读不到的文件)。缓解: `unreadable_count` 承接, schema 文档 (含 `:1136` fail-soft 形状) 写明, CHANGELOG 标注 |
| **Risk** | `-z` 改变了 ls-tree 输出解析形态, 解析写错会让**所有**分支枚举返回空 (静默失明, 比原 bug 更坏)。缓解: SC-2 在**固定分支集**的 hermetic 临时仓上比对改前 / 改后, 断言平铺仓枚举结果非空且**在 `freeze_corpus.py:29` 的八字段投影下逐字段相等** (反事实: 解析写错 ⇒ 空集 ⇒ 红)。**R2 订正 (`d02ec3f0`)**: v3 此处写「与改前**逐字节相同**」在 A′ 下**恒假** —— A′ 给每一行 track 新增了 `rel_path` 键, 改前基线由无该键的旧代码产出; 「逐字节 / 零差异」必须限定到投影或显式豁免新键, 否则是一条自己写红自己的断言, 而实施者最可能的反应是顺手削掉断言 |
| **Risk** | F2 只覆盖可解码 UTF-8 名; 真正非 UTF-8 字节的文件名修后仍不可读 (§7 末条)。缓解: schema + CHANGELOG 写明边界, 并考虑对不可解码名显式跳过 (对齐 `handoff.py:318-322` 先例) 而非计入 `unreadable_count` |

---

## Tasks

- [ ] 1.1 前置核验: 本仓 `docs/handoff/` 无子目录与非 ASCII 文件名; 两份冻结语料内无子目录路径 (机械命令 + 结果抄进 tasks 记录)
- [ ] 1.2 建红测: 新测试文件覆盖子目录 / 非 ASCII / git-show 失败 / 同名串读 四族, 对 `301641b` 全红且红在正确断言上 (逐条记录红的断言文本, 防「红在环境上」)
- [x] 2.0 **前置门 — 已解除 (2026-09-07)**: 待复议 2 (A vs A′) 已裁定为 **A′ + 写侧守卫**, 决策单 `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md` (AI 在 owner 不在场时裁, 已列入待追认)。待复议 1 / 3 / 4 / 5 / 6 均取各自的「推荐默认」推进, 全部保留在 §待 owner 复议 供复议
- [ ] 2.5 pointer 写侧守卫 (`latest_md_writer._render_pointer`)。四个硬要求缺一不可: (a) 判据是**数据事实**, 写成 `rel = track.get("rel_path") or track.get("filename")` 后比 `rel == filename` 才写真指针, **严禁**字符串嗅探 (`"/" in filename`); (b) **`rel_path` 缺键 ⇒ 按 `rel = filename` 兜底 = 照写真指针** (老快照即平铺世界, R2 critical `6f8fa9f7`; 写成 `track.get("rel_path") != filename` 会让所有无该键的 track 恒走降级, 当场打红 `test_p1_layer_h.py:270` 并在跨版本读盘时重开 H5 修复); (c) **`_render_pointer_unavailable(track_id, now)` 的签名变更** —— 现签名与 `:164` 硬编码文案「缺少 filename 字段」装不下第二个原因, 须加 reason 入参或新增姊妹函数; (d) 降级文案必须写明「目标在子目录」这个具体原因, 不得静默退化
- [ ] 2.1 枚举层改造 (`-z` + 相对路径 + **从 `_HANDOFF_TREE_PATH` 派生**的前缀剥离守卫 + 返回契约改为可携带 per-item 错误 + docstring 契约对齐); pointer 排除**不改代码**, 只补文档口径
- [ ] 2.2 三个仓内调用方与 legacy track_id 改用相对路径 (A′ 案下另加 `rel_path` 字段并改 `scan.py:186`)
- [ ] 2.3 git-show 失败分支改为只报 soft_error; 新增 `unreadable_count`
- [ ] 2.4 fail-soft 早退路径 (`:586-596`) 补 `unreadable_count`, 使「恒存在」不变量在错误路径上成立
- [ ] 3.1 `scan.py` AC-5 跨文件消费方钉测 (F1) —— 端到端产出 tracks_data, 四道前置显式配齐 (见 SC-6)
- [ ] 3.2 dedupe tie-break 现状钉测 (风险面)。**必须在测试 docstring 与 SC-7 里显式标注「假想输入的特性化测试 (characterization)」** (R2 major `e3ca1e1a`): A′ 下 `filename` 恒为 basename, collector **结构上不可能产出** `filename = "archive/2026-07-19-x.md"` 的行, 该用例只能手搓 dict, 它记录的是 `dedupe_latest_per_track_container` 对该假想输入的行为, **不是**本 spec 的行为改动。若 owner 复议改判回 A 案, 该标注去掉、恢复为真实输入用例
- [ ] 3.3 legacy track_id 相对路径化钉测 (同名不同目录产生**两条不同 `track_id`** 且 `updated_at` 各取自己那条路径的提交日, SC-13)。⚠️ **不得写成「不折叠」断言 (R2 major `3cb2cf2b`)**: legacy 行在 `handoff_multibranch.py:521-524` 被 `continue`、从不进入 dedupe 分组, 「不折叠」在改前改后都为真 ⇒ 恒绿
- [ ] 4.1 schema 文档同步 (`filename` 语义保持 basename / 新增 `rel_path` 行 / `unreadable_count` / **`:1136` fail-soft 形状同时补 `unreadable_count` 与既有漏写的 `identity_advisories`** / pointer 排除口径 / legacy 分支 / **新 soft_error kind `handoff_multibranch_unexpected_path_prefix` 登记** / **`## Change history` 加一行** / F2 覆盖边界)。**R2 删除项 (`e3ca1e1a`)**: 不做 `:1125` tie-break 论据订正 —— A′ 下 `filename` 恒为日期前缀 basename, 该句仍为真, 照做即写入一条错误勘正; 仅当 owner 改判回 A 案才恢复
- [ ] 4.2 collector 模块 docstring (`:14-31` 键表补 `unreadable_count` + `rel_path` / `:42` filename 契约 / `:20` legacy_count 注释) + `references/json-diff-normalizer.md:241` 键集 + `:177` 常量注释勘正 + **`_get_file_commit_date` 的 committer/author date 勘正 (R2 minor `bf0d93cb`)**: `:313` docstring 写 "ISO 8601 UTC **committer** date", 而实现用 `%aI` = **author** date (`:316` 自己就写了 author date, `:322` 是命令行), 模块 docstring `:40` 与 `state-snapshot-schema.md:1108` 同错 —— 与 `:20` / `:177` 属同一族「既有 code/doc 不一致, 顺手勘正」, 且 §Why 与 SC-4 的全部日期结论都建立在 author date 语义上
- [ ] 4.3 既有测试全绿 + 平铺仓零行为变化断言 (投影口径见 SC-2 / SC-16)
- [ ] 4.4 **`standards/conventions/session-handoff.md:171-173` 同步 (R2 major `94935605`, Rule #3 + Rule #9 SOT)**: latest.md 派生行为现为穷尽两态 (单 track 写指针 / 多 track 只写 banner), §2.5 守卫引入第三态 (单 active track 但文件在子目录 ⇒ 降级 + 写明原因) ⇒ 补条件从句, 不动前两态判据。**该文件在共享子模块 standards/ 内**: 需独立 commit + 本地 merge + 双推 ls-remote 核验 + 主仓 standards gitlink bump (与 Task 5.2 的 aria 链路同型, 是**第二条**)。若判定本轮不改, 须在本文与 handoff 显式写成 deferred + 理由 + 跟踪 issue
- [ ] 5.1 版本 SOT 5 文件 + `aria/CHANGELOG.md` (PATCH) + **主仓 aria-plugin 版本引用面 —— 共 16 处, 逐处勾** (R2 major `d58dfb65` 补全; 本次 rework 实测枚举, 与上次发版 commit `4c3c826` 自述的「16 处版本点」逐一对上):

  | # | 位置 | 机械兜底 |
  |---|---|---|
  | 1 | `README.md:8` Plugin badge | ✅ `m6-version-badge-match` (`.aria/state-checks.yaml:88`) |
  | 2 | `README.md:242` 正文 `Plugin Version:` 行 | ❌ 无 |
  | 3-5 | `README.zh.md:3` / `README.ja.md:3` / `README.ko.md:3` `<!-- translated-from: vX.Y.Z -->` marker | ✅ `i18n-readme-translation-currency` (`:141`) |
  | 6-8 | `README.zh.md:10` / `README.ja.md:10` / `README.ko.md:10` Plugin badge | ❌ 无 |
  | 9-11 | `README.zh.md:244` / `README.ja.md:244` / `README.ko.md:244` 正文 `Plugin Version:` 行 | ❌ 无 |
  | 12 | `VERSION:24` `\| aria (插件) \| vX.Y.Z \|` (CLAUDE.md §版本管理「发布同步面」逐字列出「主仓 VERSION」) | ❌ 无 |
  | 13-14 | `CLAUDE.md:139` (版本区间尾) / `CLAUDE.md:141` (「版本:」行) | ❌ 无 |
  | 15 | `docs/architecture/system-architecture.md:189` | ✅ `plugin-version-arch-docs-match` (`:372`) |
  | 16 | `docs/architecture/version-scheme.md:23` | ✅ 同上 |

  **⚠️ 删除 v3 的「三条 check 判据均为与 plugin.json 比对 ⇒ 漏改必在归档闸转红」这句 —— 经实读四条 check 判定为假**: `m6-version-badge-match` 的命令是 `grep -m1 … README.md`, **只看首个 badge**; `i18n-readme-translation-currency` 只正则 `translated-from`, **不读 i18n 正文** (memory `feedback_version_checks_blind_to_i18n_readme_body` 同型); `plugin-version-arch-docs-match` 只比两处架构行; 另一条 `main-project-version-consistency` 的 POINTS 清单 (`.aria/probes/main-project-version-consistency.py:39-49`) 全是**主项目 1.7.5** 那条线, 不含任何插件版本行 ⇒ **上表 10 处 (#2 / #6-11 / #12 / #13-14) 零机械兜底**, 只能人工逐处核对。i18n 正文重译仍按 #140 B 档 (仅正文实质变更才重译), 但 badge 与 `Plugin Version:` 行是**版本点不是译文**, 每次发版都要改
- [ ] 5.5 **Rule #6 照跑 AB (R2 改判, `885edf34` + `cecc06af`)**: 按头部 Rule #6 行的改判执行三件事, 缺一不可 —— (a) 用 `/skill-creator` 跑 state-scanner AB (自研 runner 已废弃), 结果落 `aria-plugin-benchmarks/ab-results/`; (b) 开**套件缺口 issue**: `ab-suite/state-scanner.json` 对 `handoff_multibranch` / `legacy` / `basename` 三词零命中, `tracks_multibranch` 仅 `:214` 一处命中且该 prompt **把 `collision.kind` 的值写死在题面里**, 结构上测不到 collector 输出变化 ⇒ 即使照跑也覆盖不到本变更, 缺口须成文; (c) 保留全部 substitute SC (rule6_note 的十条 baseline-failing 实体), 不因跑了 AB 而削减。**禁止**以「代码面 / 成本 / 套件测不到」自行降回豁免 (Rule #10)
- [ ] 5.2 Phase C: aria 本地 merge + 双推核验 (Rule: 子模块禁服务端合并 + 逐个 `ls-remote` 核验); 主仓 spec + gitlink bump **从 `301641b` 前进** (实测起点, 见头部主仓实况行; 严禁回退到 `0545f86`)。**若 Task 4.4 落地, 同一套动作对 `standards/` 再做一遍** (独立 commit + 本地 merge + 双推 ls-remote + 主仓 standards gitlink bump) —— 两条子模块链路各自核验, 不合并成一步
- [ ] 5.3 遗留缺口开 issue: `handoff.py::_parse_latest_pointer` (`:288` 剥目录段) 与 `_scan_md_files` (`:300,318` 非递归) 的扁平假设 = 原选项 (ii); 本 spec 只用守卫使其**诚实降级**, 不修本体。issue 里必须带上本 spec 的 SC-15 子目录布局作为现成复现
- [ ] 5.4 Phase D: 归档 + `release_gate` claim 释放 + #195 关闭回帖

---

## Success Criteria (可证伪; 每条自问「机制没实现会红吗」)

| SC | 断言 | 核验 |
|---|---|---|
| SC-1 | **hermetic case-1 (issue 主症状)**: 临时仓, `docs/handoff/archive/2026-05-09-session-end.md` 从未在顶层存在过, 有合法 frontmatter → `tracks[]` 含一条 `legacy: false` 行, `track_id` / `updated_at` 取自 frontmatter; `legacy_count == 0`; **`filename == "2026-05-09-session-end.md"` 且 `rel_path == "archive/2026-05-09-session-end.md"`** (R2 `28f9d80c`: A′ 已裁定, 此处**单值化**, 不再并列 A 案取值; A 案取值仅在 §候选方案表内留作复议对照)。**错误面断言消歧 (R2 major `fc925710`)**: 本 collector 有两个同名 error 面 —— `tracks_multibranch.errors[]` (= `r.data["errors"]`, `handoff_multibranch.py:753`) 只装**消息串**, soft_error 的 **kind** 只进 `CollectorResult.errors` (`_common.py:312-313` 的 `{"error": kind, "detail": …}`) 再由 `scan.py:382-383` 汇进顶层 `errors[]`。本条断言的是 **`CollectorResult.errors` 里无 kind == `handoff_multibranch_git_show_failed`**, 不是裸 `errors[]` (写成裸 `data["errors"]` 不含该字面量 ⇒ 在 `301641b` 上就恒绿, 违反 Task 1.2「对 `301641b` 全红且红在正确断言上」)。**反事实**: 回退枚举层为 basename ⇒ git show 失败 ⇒ 该行变 legacy + 该 kind 出现 ⇒ 全红 | `test_handoff_multibranch_path_fidelity.py::test_subdir_file_read_as_real_track` |
| SC-2 | **平铺仓零行为变化**: 同一临时仓只放顶层文件, 改前与改后 `collect_handoff_multibranch` 的 `tracks[]` / `legacy_count` **逐字段相等**。**载入方式 (R1 rework 改)**: 禁用「测试内 `git show 301641b:` 动态载入原实现」—— 实跑确认三层障碍: 朴素 `exec` 直接 `ImportError: attempted relative import with no known parent package` (collector `:120` `from ._common import` / `:127` `from .handoff import`); 必须建 `collectors.<name>` 包上下文并手动设 `__file__`, 否则 `:141` 的 `_Path(__file__)` 抛 NameError 而 `:152` 只 `except ImportError` 接不住; 且插件把 `tests/` 分发到**无 `.git`** 的 cache 目录、组织 CI checkout 为 `fetch-depth: 1` ⇒ 异地必 error。改用**冻结语料比对** (仓内已有 `tests/fixtures/freeze_corpus.py` + `handoff-tracks-frozen-*.json` 形态): 改前跑一次生成 baseline JSON 落 `tests/fixtures/`, 改后比对。**R2 两处订正**: (1) **基线必须跑在固定分支集上** (`db0db697`) —— 「同工作区双跑」只换了基线的落盘位置, 没治时变的**根**: collector 枚举全部 `refs/remotes/origin/*` (`handoff_multibranch.py:202-208`, 按 committerdate 排序取 cap), `tracks[]` 从不去重、每 (branch, file) 一行 (模块 docstring `:14,:54`); 主仓 `docs/handoff/` 现有 **190 份**顶层 `.md` (本次 rework 实测, 零子目录) ⇒ **Phase B 自己把 feature 分支推上 origin, 「改后」那次扫描就凭空多约 190 行**, 同伴容器往 master 推交接同样加行, 而 Phase 0.5 `remote_refresh` 的 `fetch --prune` 保证看到最新态 ⇒ 必假红。落地取**hermetic 临时仓 (单 master 分支, 固定文件集)**; 若坚持用本仓, 则只比对 before 分支集内的行并把分支集写死进夹具。(2) **比对口径 = `freeze_corpus.py:29` 的八字段投影** (`d02ec3f0`) —— `FIELDS` 硬编码 `(track_id, owner_container, status, phase, updated_at, filename, branch, legacy)`, **不含 `rel_path`**; A′ 给每行新增该键, 故必须明写「走投影」或「除 `rel_path` / `unreadable_count` 外逐字段相等」, 否则断言在采纳的设计下**恒红**, 而恒红的下场是实施者顺手削断言。**反事实**: `-z` 解析写错 ⇒ 枚举空集 ⇒ 两侧不等 ⇒ 红 | `::test_flat_repo_byte_identical_to_frozen_baseline` |
| SC-3 | **非 ASCII (F2)**: `docs/handoff/2026-测试-交接.md` (合法 frontmatter) → 被读成真 track, `filename` 无引号无八进制转义。**反事实 (R1 rework 订正机制)**: 去掉 `-z` ⇒ `Path(path).name` 得到带尾引号的 `2026-\346\265\213\350\257\225.md"` ⇒ 在 `.endswith(".md")` 处被 `continue` **静默丢弃** ⇒ 该 track 根本不在 `tracks[]` 里 ⇒ 红。(**不是**「git show 失败」—— 今天该路径连 git show 都到不了, 见 §Why F2 实测) | `::test_non_ascii_filename_not_escaped` |
| SC-4 | **`updated_at` 语义分割 (现状记录性 + 修复性各一半)**: 顶层 commit (作者日期 2026-05-09) → `git mv` 进 `archive/` (2026-08-15) 且文件**无** frontmatter → legacy 行的 `updated_at` = `2026-08-15…`。**这一半是现状记录性断言, 改前改后同值** (hermetic 实测: 旧 basename 路径与新相对路径的 `git log -1 --format=%aI` 都返回 mv 日, `--follow` 亦同), 用于让未来给 `_get_file_commit_date` 加 `--follow` 的人当场看见「那救不了」。**有鉴别力的另一半 (修复性)**: 从未在顶层存在过、无 frontmatter 的 `archive/2026-06-01-x.md` → `updated_at` 为**非空真日期**; **反事实**: 回退为 basename ⇒ `git log` 命中不到 ⇒ 空串 ⇒ 红。第三条: **有** frontmatter 的同形文件 → `updated_at` 取 frontmatter 值, 与 mv 日无关 | `::test_moved_file_dates` |
| SC-5 | **git show 失败不再伪造 legacy**: 构造一条枚举得到、但 `git show` 必失败的路径 (枚举后删除该对象所在 ref / 用 monkeypatch 让 `_read_file_content` 返回错误) → **`CollectorResult.errors` 里存在 kind == `handoff_multibranch_git_show_failed`** (R2 `fc925710` 消歧: **不是** `tracks_multibranch.errors[]` —— 后者只装消息串, 实测其 `[0]` = `"[master/…] git show failed: git show failed for origin/master:docs/handoff/… (other, rc=128)"`, **不含该 kind 字面**, 按裸 `errors[]` 写则本条**不可满足 / 恒红**), `tracks[]` **不含**对应行, `legacy_count` 不增, `unreadable_count == 1`。**反事实**: 保留旧降级分支 ⇒ tracks 多一行 ⇒ 红 | `::test_unreadable_not_downgraded_to_legacy` |
| SC-6 | **F1 跨文件消费方**: 对含子目录 track 的快照跑 `scan.py::_same_branch_head_unreachable_tracks` (真实符号, 非 `_check_handoff_ancestry`), 断言它对该 track 真的执行了 `git log` (命令行含 `docs/handoff/archive/…`) 且得到非空 SHA。**tracks_data 必须由同一临时仓上的 `collect_handoff_multibranch` 端到端产出, 禁止手搓 dict** (R1 rework: 函数签名只吃 dict, 手搓会让 collector 根本没被调用, 反事实变假 ⇒ SC 恒绿)。**四道前置必须在夹具里显式配齐** (`scan.py:166-183`, 任一不满足即在早返回 `[]` 上假绿): `git_data["current_branch"]` 非空 · `detached_head` 为假 · `enforced_remotes` 非空 · track 的 `branch` 等于 `current_branch`。**反事实**: 把 collector 退回 basename ⇒ 命令行路径不存在 ⇒ 空 SHA ⇒ 断言红 | `::test_scan_ancestry_consumer_uses_relative_path` |
| SC-7 | **dedupe tie-break 现状钉住 —— 明标「假想输入的特性化测试」(R2 major `e3ca1e1a`)**: 同 `(track_id, identity_key)` 两行, `updated_at` 完全相同, filename 分别为 `2026-07-19-x.md` 与 `archive/2026-07-19-x.md` → `dedupe_latest_per_track_container` 选中 `archive/…` 那行 (字典序大)。⚠️ **A′ 下 collector 结构上不可能产出 `filename = "archive/…"`** (`filename` 恒 basename), 故本条只能手搓 dict, 记录的是 dedupe 函数对**假想输入**的行为, **不是本 spec 的行为改动**, 不计入 rule6_note 的 baseline-failing 实体。价值: 让未来改排序语义 (或改判回 A 案) 的人当场看见。**与之配套的 Task 4.1 `:1125` 论据订正已在 R2 删除** —— A′ 下该句仍为真。A′ 下真正打开的 tie 面 (同 basename 异目录 ⇒ 四级键全并列 ⇒ 回退迭代顺序) 见 §5 dedupe 行与 §待复议 4, 本 spec 不加断言 | `::test_dedupe_tiebreak_prefers_lexicographic_max_path` (docstring 首行须写 "characterization test — hypothetical input") |
| SC-8 | **pointer 排除口径 (前半现状记录性, 后半有鉴别力)**: 顶层 `latest.md` 与 `archive/latest.md` 均不出现在 `tracks[]` —— **这在 `301641b` 上已经为真** (`:277` 先取 basename 再于 `:280` 比常量, 本来就是任意深度; hermetic 实测两者均被排除), 故前半是记录性断言, 无鉴别力, 仅防未来收窄时无声回归。**有鉴别力的后半 (R2 `28f9d80c` 单值化到 A′)**: `archive/latest-notes.md` (非 `latest.md`) 进入 `tracks[]`, 且 **`rel_path == "archive/latest-notes.md"` 保留目录段, `filename == "latest-notes.md"` 为 basename**; **反事实**: 回退为 basename-only 枚举 ⇒ `rel_path` 里目录段丢失 (或该字段不存在) ⇒ 红 | `::test_pointer_excluded_at_any_depth` |
| SC-9 | **前缀守卫不静默吞 (两条断言, 缺一即假绿)**: 构造一批枚举返回, 其中一条不以 `docs/handoff/` 开头 (monkeypatch `_run`) → (a) 计一条 soft_error **且其 kind 字面为 `handoff_multibranch_unexpected_path_prefix`** (R2 minor `e9f28dc8`: 必须断言 kind 字面 —— 现有四个 kind 全是 `handoff_multibranch_*` 机读契约的一部分, 若实现直接复用 `handoff_multibranch_ls_tree_failed`, 只断言「计一条 soft_error」仍绿而消费方无法区分「整支分支 ls-tree 失败」与「单行前缀异常」), 且该项不进 `tracks[]`, 不 crash; (b) **同分支的其它文件仍照常进 `tracks[]`**。**反事实**: 沿用现签名的分支级错误通道 (`:619-626` 收到非 None 即 `continue` 整支分支) ⇒ (b) 红。缺了 (b), 「吞掉整分支」的天真实现同样满足 (a) 而假绿, 且那种实现比原 bug 更坏 | `::test_unexpected_prefix_soft_errors` |
| SC-10 | **既有测试全绿**: `cd aria/skills/state-scanner/tests && python3 -m unittest test_handoff_multibranch_collision_dedupe test_handoff test_handoff_worktrees test_track_board_advisories test_p1_layer_h` → **`Ran 102 tests … OK`**。**R2 补入第 5 个模块 `test_p1_layer_h` (critical `6f8fa9f7` + minor `7cba5aa4`)**: Task 2.5 改的是 `latest_md_writer.py`, 而**全插件树唯一 import `write_latest_md` 的测试就是它** (24 tests), v3 的 4 模块点名集恰好把它漏在外面, 只靠尾句「全量 discover 另跑」兜底 —— 而它正是 `rel_path` 缺键写法会打红的地方 (`:270`)。基线由本次 rework 在**真 git checkout** `/home/dev/Aria/aria` (HEAD 实测 `301641b1c893477f387a1f85d1e90d105ebf0db9`) 上实跑: 4 模块 = `Ran 78 tests … OK` (21+27+25+5), 5 模块 = **`Ran 102 tests … OK`** (78 + 24)。全量 `discover` 另跑并与改前基线逐条对比。**已删除 v1 对两条「已知失败」的豁免** (R1 critical `24165c1c`): 那两条 (`test_normalize_snapshot.TestStabilityIntegration.test_two_consecutive_runs_diff_zero` + `Test1210ChannelStabilityUnderOffline`) 是**测量环境伪失败**, 不是被审对象属性 —— 根因是 `tests/test_normalize_snapshot.py:272` / `:344` 的 `Path(__file__).resolve().parent×5`, 在插件缓存里解析到 `~/.claude/plugins/cache/10CG-aria-plugin/aria` (**非 git 仓**, 实测 `.git` 不存在) ⇒ `scan.py` 返回 20 (`EXIT_HARD_PRECONDITION`, `scan.py:120`) ⇒ 两条 assert 挂; 本次 rework 在**真 git checkout** (`/home/dev/Aria/aria`, HEAD = `301641b`) 上跑同一文件得 **`Ran 32 tests … OK`**。故基线口径 = **真仓 checkout 零失败**, 出现任何失败都要逐条 `git log -- <file>` 归因, 不得预先豁免 | 命令 + 对比 (基线须在真 git checkout 上测) |
| SC-11 | **文档同步机检 (R1 rework: 换掉不定位的代理判据)**: (a) `grep -c 'unreadable_count' references/state-snapshot-schema.md` ≥ 2 (字段表 + `:1136` fail-soft 形状各一); (b) schema 文档新增 `rel_path` 字段行 (A′ 单值化, R2 `28f9d80c`); (c) **`grep -q 'callers compose the full git-object path' collectors/handoff_multibranch.py` 无命中** (旧契约句消失) **且**模块 docstring `:14-31` 键表已新增 `rel_path` 行 (A′ 下 `:42` 的 `# basename of the handoff file` **保持不变即为正确**, 不得当成漏改) —— 取代 v1 的 `grep -c 'basename' … 相对基线减少`, 该代理判据不定位 (基线 7 处: `:42,246,277,278,280,284,288`, 新实现仍需 basename 做 `.md` 过滤与 pointer 排除, 只改 `:246` 一句即可让计数下降, 结构上钉不住 `:14-31` 的漏改); (d) `grep -q 'unreadable_count' references/json-diff-normalizer.md`; (e) CHANGELOG 含本 spec 三条 Fixed 与两条 Changed; (f) `grep -q 'handoff_multibranch_unexpected_path_prefix' references/state-snapshot-schema.md` (新 kind 登记, R2 `e9f28dc8`); (g) schema `## Change history` 表新增一行且含 `rel_path` (R2 `e03d8a32`); (h) **Task 4.4 落地时**: `standards/conventions/session-handoff.md` 的 latest.md 派生行为段出现第三态措辞 (R2 `94935605`); 若判 deferred, 则本文与 handoff 各有一处显式 deferred 记录 | grep |
| SC-12a | **活体 dogfood — 本仓平铺 (R2 major `112b4299` 拆分 + `db0db697` 治时变根 + `d02ec3f0` 豁免新键)**: 在本仓同一工作区先跑**改前** `scan.py --output …/snap-before.json`, 再跑改后 `…/snap-after.json`, 对 `tracks_multibranch` 做逐字段 diff → **除新键 `unreadable_count` 与每行新键 `rel_path` 外零差异** (v3 只豁免了 `unreadable_count`, 在 A′ 下必假红)。**基线时变必须机械封住**: 两次扫描之间**不得向任何 origin 推送分支**, 且各跑一次 `git for-each-ref --format='%(refname:short)' refs/remotes/origin/` 存档并比对 —— 分支集不同即本条作废重跑, 不得据不同分支集的两份快照下结论 (根因: collector 枚举全部 `refs/remotes/origin/*` 且每 (branch, file) 一行, 主仓 `docs/handoff/` 现有 190 份顶层 `.md` ⇒ Phase B 推一条 feature 分支就凭空多约 190 行)。**不得拿活文件 `.aria/state-snapshot.json` 当基线** (memory `feedback_baseline_corpus_stat_must_run_against_frozen_snapshot`)。**断言 exit code 与改前相同** (本仓平铺, 零行为变化 ⇒ 退出码不该动; 不承诺具体数值, 因它受本仓其它 collector 状态影响) | 命令 + 两份 snapshot + 两份分支集存档 |
| SC-12b | **活体 dogfood — 子目录临时仓 (R2 `112b4299` 拆分后只保留有鉴别力的半条)**: 在 hermetic 子目录仓跑同一 `scan.py` → **`tracks_multibranch` 侧不出现 kind `handoff_multibranch_git_show_failed`, 且 `legacy_count == 0`, 子目录件以真 track 出现**。**R2 删除两处**: (1) 原「soft_error 里也无 `handoff_pointer_target_missing`」在**全子目录布局下结构上不可能产生** —— `handoff.py::_scan_md_files` 非递归且过滤 `latest.md` (`:300,318,323`) ⇒ `canonical_files` 为空 ⇒ `collect_handoff` 在 `:438-451` 提前返回, `_resolve_latest` (`:455`) 根本不执行 ⇒ 该 kind (`:397-404`) 无从产生, 与守卫有没有实现无关 ⇒ **恒绿断言**, 已移交 SC-15 (那里的夹具有顶层文件, 候选集非空, 才有鉴别力); (2) 原「**断言 exit 0**; 若实跑非 0, 逐条抄下 kind 并在 handoff 说明」—— 失败模式是「记录」不是「转红」, **不是验收判据**; 且 hermetic 临时仓的退出码还受其它 collector 影响, 不可控 ⇒ 整条删除, 以上面的 kind 级断言取代。**反事实**: 回退枚举层为 basename ⇒ 该 kind 出现 + `legacy_count == 1` ⇒ 红 | 命令 + handoff 证据 |
| SC-13 | **legacy track_id 相对路径化 (R1 rework 新增, 覆盖 §2 第三条)**: 临时仓放两份**均无 frontmatter** 的 `docs/handoff/x.md` 与 `docs/handoff/archive/x.md` (两文件在不同提交里落盘, 提交日期不同) → **两条断言**: (a) `tracks[]` 产生**两条不同 `track_id`** (`legacy:<branch>:x.md` 与 `legacy:<branch>:archive/x.md`); (b) 两行的 `updated_at` **各自等于自己那条路径的提交日**, 互不相同。**反事实**: legacy track_id 沿用 basename ⇒ (a) 两行同 id ⇒ 红; 且 `_get_file_commit_date` 仍拼顶层路径 ⇒ (b) 两行同日 ⇒ 红。**⚠️ R2 major `3cb2cf2b` 删除的那一半**: v3 原断言「`dedupe_latest_per_track_container` **不折叠**」及其反事实「沿用 basename ⇒ 两行同 id ⇒ 折叠成一条 ⇒ 红」**被代码直接证伪** —— `status == "legacy"` 的行在 `handoff_multibranch.py:521-524` 被 `continue`、**从不进入分组**, 所以两条 id 完全相同的 legacy 行**今天也不会折叠** (实测 2 行进 → 2 行出, `legacy_passthrough=2`); 该透传是 docstring `:493-499` 与 `state-snapshot-schema.md:1128` 的明文契约。「不折叠」因此是**恒绿**记述, 已从判据里剔除 (可留作 docstring 注记, 不作断言)。SC-13 的 baseline-failing 资格由上面 (a)(b) 两条撑住 | `::test_legacy_track_id_uses_rel_path` |
| SC-14 | **`unreadable_count` 恒存在覆盖错误路径 (R1 rework 新增, 覆盖 §4)**: monkeypatch 让 `_list_origin_branches` 返回错误 → 走 `:586-596` fail-soft 早退 → 返回 dict **含** `unreadable_count == 0` 键, 且 **`r.data["errors"]` (消息串列表) 非空、`CollectorResult.errors` 里存在 kind == `handoff_multibranch_branch_list_failed`** (R2 `fc925710` 消歧: 两个面各断一次, 不写裸 `errors[]`)。**反事实**: 只改正常路径 ⇒ 早退 dict 缺键 ⇒ `KeyError` / 断言红 | `::test_unreadable_count_present_on_failsoft_early_return` |
| SC-15 | **writer → collector pointer 往返 (R1 critical `63d1ce08`; 2026-09-07 裁定后收敛为单一形态)**: 同一临时仓上依次真跑 `collect_handoff_multibranch` → `write_latest_md` → `collect_handoff` 三步 (禁手搓中间产物), 分**三个**布局各断言一次 (R2 critical `88a49037` 重定夹具 + `6f8fa9f7` 增第三布局) —— **三个布局的夹具组成与全部断言见本表下方 §SC-15 细则; 夹具组成是判据的一部分, 不得按字面取最小夹具**。下文 `errors[]` 一律指 **`collect_handoff` 返回的 `CollectorResult.errors` 里的 kind 集合** (R2 `fc925710` 消歧, 非 `data["errors"]` —— `collect_handoff` 的 `data` 根本没有 errors 键) | `::test_pointer_roundtrip_toplevel` / `::test_pointer_roundtrip_subdir_guarded` / `::test_pointer_written_when_rel_path_key_absent` |
| SC-16 | **平铺仓 `rel_path == filename` 恒成立 (R2 major `d02ec3f0` 补, 承接决策单 §落地约束第 1 条)**: 只放顶层文件的临时仓 → `tracks[]` 每一行都满足 `rel_path == filename` 且两者都不含 `/`。决策单要求「平铺仓 `rel_path == filename` 要有一条 SC 钉住」, v3 的 SC 集**无任何一条承接** ⇒ 本条补上。**反事实**: 前缀剥离写成 `path[len("docs/handoff"):]` (少剥斜杠) ⇒ `rel_path` 带前导 `/` ⇒ 红; 或忘记剥前缀 ⇒ `rel_path == "docs/handoff/x.md"` ⇒ 红。它同时是 §What.1「前缀剥离必须从常量派生」那条要求的验收 | `::test_flat_repo_rel_path_equals_filename` |

#### SC-15 细则 (三个布局 + (f) 的处置 + 三条反事实) — 与上表 SC-15 同为验收判据

**布局 1 — 顶层** (唯一 active track 的文件在 `docs/handoff/` 顶层): (a) `latest.md` 含真指针 `[x.md](./x.md)`; (b) `collect_handoff` 读回 `latest_source == "pointer"` 且 `latest_filename == "x.md"`; (c) kind 集合不含 `handoff_pointer_target_missing`。

**布局 2 — 子目录 + 顶层留一份非-active `.md`** ⚠️ **夹具组成是判据的一部分, 必须照写 (R2 critical `88a49037`)**: 唯一 **active** track 的文件在 `archive/`, **同时**顶层另有一份 `status != active` 的 `.md` (例 `2026-05-01-old.md`) 使 `handoff.py` 的 `canonical_files` **非空**。断言: (d) `latest.md` **不含** `**Latest**: [` 真指针行, 而是走降级分支且文案含「目标在子目录」的具体原因; (e) kind 集合**不含** `handoff_pointer_target_missing`。

**为什么必须留顶层那一份**: v3 按字面取最小夹具 (归档-only) 时 (e) **恒绿且其反事实为假** —— `_scan_md_files` 非递归且过滤 `latest.md` (`handoff.py:300,318,323`) ⇒ `canonical_files` 为空 ⇒ `collect_handoff` 在 `:438-451` 提前返回, `_resolve_latest` (`:455`) 根本不执行 ⇒ `handoff_pointer_target_missing` (`:397-404`) **结构上不可能产生**, 与守卫有没有实现无关 (qa-engineer hermetic 实测: `handoff.exists=False`, `latest_source=None`, **soft errors=[]**)。留下顶层那一份后候选集非空, 去掉守卫时 writer 会写出 `[archive/x.md](./archive/x.md)`, `_parse_latest_pointer` (`:288`) 剥成 `x.md` 在候选集里查不到 ⇒ 该 kind 真的出现 ⇒ (e) 才有鉴别力。

**布局 3 — 老快照缺 `rel_path` 键 (R2 critical `6f8fa9f7` 新增)**: 直接喂一个**没有 `rel_path` 键**的 active track dict (形如 `tests/test_p1_layer_h.py:230-240` 的八字段 `_active_track`) 给 `write_latest_md` → (g) **仍写真指针** `[x.md](./x.md)`, 不走降级。**反事实**: 判据写成 `track.get("rel_path") != filename` ⇒ 缺键取 `None` ⇒ 判据恒真 ⇒ 走降级 ⇒ (g) 红。本布局是**唯一**能覆盖缺键分支的 SC —— 布局 1/2 都由新 collector 端到端产出, `rel_path` 恒在。

**(f) 的处置 (R2 `88a49037` 改写)**: v3 的「`handoff.exists` 与 `tracks_multibranch.exists` **不互相矛盾**」在归档-only 夹具下**恒红且不可满足** (守卫只管 latest.md 写什么, 管不到 `handoff.py` 的非递归扫描 ⇒ 全子目录布局下 `handoff.exists=False` / `tracks_multibranch.exists=True` 的矛盾**必然存在**, 而本文自己已把它推给 Task 5.3 另开 issue), 且「不互相矛盾」未给可执行谓词、由实施者自定 ⇒ 不可证伪。**⇒ 整条从 SC-15 移除**, 改为: 在布局 2 下记一条**记述性**观测 (两者均为 `true`, 无矛盾, 无鉴别力, 不计入 baseline-failing 实体), 并把「全子目录布局下两个 collector 的 `exists` 矛盾且**零信号**」原样写进 Task 5.3 的 issue 正文当现成复现。

**反事实 (三条, 缺一不可)**: (1) 去掉 §2.5 守卫 ⇒ 布局 2 的 (d) 立即红, 且 (e) 因 `handoff_pointer_target_missing` 出现而红; (2) 把守卫判据换成 `"/" in filename` ⇒ A′ 下 `filename` 恒无斜杠 ⇒ 守卫恒不触发 ⇒ (d)(e) 同样红 (专防字符串嗅探); (3) 把缺键兜底写成 `track.get("rel_path") != filename` ⇒ 布局 3 的 (g) 红 (专防缺键恒降级)

---

## rule6_note (Rule #6 — **R2 改判: 判据表第四行「拿不准 ⇒ 照跑」**, SOT `standards/conventions/skill-benchmark-exemption.md`)

> **R2 rework 说明**: v3 落判据表**第一行 (描述性 ⇒ substitute, AB 不适用)**, 其两条支撑证据经 R2 实测**双双不成立**, 故改判照跑。下文逐条给反证。

- **变更性质 (不变的部分)**: 变更本体仍全是 collector / scan 代码 + 输出 schema 文档。**无** `description` 变动, **无** SKILL.md / references 的文本变动; SKILL.md 出现 `tracks_multibranch` 共 **3 处** (`:117` collector 清单 · `:149` / `:153` coordination 闸门接线), 本 spec **三处均不改**。
- **❌ 反证 1 —— 「四词零命中」为假 (R2 major `885edf34`, 本轮唯一 5/5 全席独立命中)**: `aria-plugin-benchmarks/ab-suite/state-scanner.json` 对 `tracks_multibranch` **命中 1 次** (`:214`), `handoff_multibranch` / `legacy` / `basename` 三词确为 0。文件现为 **17551 B**, 命中用例由 commit `5697477` (2026-09-05T14:12Z) 引入 —— 而 R1 decision `0f9dc120` 记的「四席实测全 0 / 文件 15518 B」与现场两项都对不上 ⇒ **R1 的四席交叉核验是对改前副本测的, v3 原样继承** (memory `feedback_spec_inherits_upstream_dec_errors`)。**该分歧已在本次 rework 机械闭合** (聚合报告把它留给 R3, 现无需再算): `git show 5697477^:…/state-scanner.json | wc -c` = **15518**, 同版本 `grep -c tracks_multibranch` = **0**; 而 R1 审计所见树 `813e82c` 上同文件 = **17551 B / 命中 1** —— 即 15518/全 0 是 `5697477^` 的形态, **在 R1 开审前就已被取代**, 两席对「R1 为何测错」的两种解释 (读了改前副本 / 在 R1 树上本就为 1) 因此相容且同时为真。**证据句改写**: 唯一命中落在协调闸门用例的 prompt 上, 问「本次扫描的 `tracks_multibranch.collision.kind` 是空的 —— 这会改变 (A) 的答案吗」, 即 `SKILL.md:149/153` 闸门面。
- **❌ 反证 2 —— 「闸门面不受影响」为假 (R2 conflicted `cecc06af`, 本次 rework hermetic 实跑闭合)**: v3 的论证只量了**减法** —— 假 legacy 行 `owner_container` 恒 `unknown`, `skills/state-scanner/lib/collision.py:483-486` 的 `collidable` 过滤 (Layer L 包; 本 skill 有两个 `lib` 包, 见 memory `feedback_state_scanner_dual_lib_package_shadow`)本就排除它们 ⇒ 删掉这些行不动 `collision.kind`。**该半仍然成立**, 但它**没量加法**: 路径修好后, 子目录里带合法 frontmatter 的交接会带着**真 `owner_container`** 进入 collidable。实测 (顶层 `simonfish/c1` active + `archive/` `aria-runner-bot/c2` active, 同 `track_id`): 改前 `collision.kind = none` / `groups 0`, 改后 **`cross_owner` / `groups 1`**。而 `collision.kind != none` 正是闸门 (`SKILL.md:149/153`)、规则 1.54 (`advanced-rules.md:544`)、`fetch_gate.py:175-188` 的**触发条件本体** ⇒ 本 spec 不改闸门的**文本**, 却改变它看到的**值**。
- **⇒ 改判与处置**: 「变更是纯代码 / 描述性」与「它改变了处方性判定面的输入」两个事实并存 ⇒ 落判据表**第四行「拿不准 ⇒ 照跑 (宁跑勿豁)」**。按 Rule #10, AI **不得**以「代码面 / 成本 / 套件测不到」把它降回豁免。**三件事并做 (Task 5.5)**: (a) 用 `/skill-creator` 跑 state-scanner AB, 结果落 `ab-results/`; (b) **开套件缺口 issue** —— 即使照跑, 唯一那处命中的 prompt 也把 `collision.kind` 的值**写死在题面里**, 结构上测不到 collector 输出变化, 缺口须成文 (memory `feedback_static_benchmark_unfit_as_oneshot_selection_gate` 同族); (c) substitute SC 集**全部保留**, 不因跑了 AB 而削减。
- **substitute 覆盖 (R2 重算)**: **baseline-failing 实体 = 十一条** —— SC-1 / SC-3 / SC-4 (后半) / SC-5 / SC-6 / SC-8 (后半) / SC-9 / SC-13 / SC-14 / SC-15 / **SC-16 (R2 新增)**, 每条附反事实。R2 对其中两条的**依据**做了订正 (实体资格不变): SC-13 的「dedupe 不折叠」那半被证伪 (legacy 行从不进分组, `handoff_multibranch.py:521-524`), 资格改由「两条不同 `track_id`」+「两行 `updated_at` 各取自己路径」撑住; SC-15 的资格改由布局 2 的 (d)(e) + 布局 3 的 (g) 撑住 (原 (f) 因恒红不可满足已移除)。**回归锁 (baseline 上本就为绿, 非实体)** = SC-2 (零行为变化) · **SC-7 (假想输入的特性化测试, R2 明标)** · SC-4 前半 · SC-8 前半。SC-10 守既有面 (R2 补入 `test_p1_layer_h`, 102 tests); SC-11 守文档面; SC-12a / SC-12b 是活体。
- **不豁免的部分**: 无, 且本轮已从「豁免」改成「照跑」。若 Phase B 期间进一步需要改 SKILL.md 或 `handoff-mechanics.md` 的指令面 (例如 §待复议 2 若裁定「真修生产 D.3 pointer 面」, 或新增「AI 见到 `unreadable_count > 0` / `collision.kind` 翻转该怎么说」的处方), **AB 范围随之扩到 phase-d-closer / session-closer**, 并在 tasks 留痕。

---

## 待 owner 复议

> R1 rework 说明: 条目 1 已按实测重写 (原写法把现状包装成待定默认), 条目 2 为 R1 critical 新增且是 Phase B 的前置门, 原条目 5 (gitlink 时机) 因实况变化**已作废删除**。

1. **pointer 排除口径要不要从「任意深度」收窄到「只排顶层」** (推荐默认: **不收窄, 保持现状**)。实测确认: `301641b` 上 `archive/latest.md` **已经**被排除 (`:277` 取 basename → `:280` 比常量), 所以「任意深度」不是本 spec 引入的新行为, 而是**未成文的现状**; 本 spec 只把它写进 schema 文档。反对意见可能是「排除逻辑应只针对活指针, 归档目录下的 `latest.md` 是历史文件、应当进 tracks」——若采纳反对, 那是一次**行为变更**(需改代码 + 改 SC-8 前半为断言其进入 `tracks[]`), 不是保持现状。
2. **✅ 已裁定 (2026-09-07, AI 在 owner 不在场时裁, 请追认) — `filename` 语义取舍**: 取 **A′ + 写侧守卫**。决策单 `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md` 载完整理由、反证据与代价; §2.5 是配套的守卫设计; SC-15 是端到端验收。**⚠️ R2 必读的代价重述 (critical `d1f01126`, 4/5 席)**: 下面第 (1) 点原本请 owner 为「子目录采用方只拿降级 pointer」签字, 但实测表明**这个代价目前无人在付** —— `write_latest_md` 在插件 1.71.1 全树**零生产调用点** (`phase-1-collectors.md:95` 的既有设计决定「deliberately D.3-scoped, 不引入 production call-site」, D.3 集成推给 TASK-029 至今未落地), 生产 D.3 的指针是 AI 按 `handoff-mechanics.md:114-124` 的处方决策表**手改**, 本仓 `docs/handoff/latest.md:103-107` 甚至自记「机械 `latest_md_writer` 当前不可用」。⇒ 守卫消除的是**writer 一旦接线就会命中**的失败面, 不是今天正在发生的损坏; owner 请据此重新估价。**请 owner 复议五点**: (1) 是否接受「子目录采用方(在 writer 接线后)只拿降级 pointer」这个代价, 还是要求本 cycle 内一并做 (ii); (2) 遗留缺口 issue 开在 `10CG/aria-plugin` 还是 `10CG/Aria`; (3) 是否追认本次 AI 裁定 —— 不追认则回退 `rel_path` 字段与守卫, 成本约一个 commit; (4) **是否要求本 cycle 一并修「生产面」** —— 即动 `handoff-mechanics.md:114-124` 的处方决策表让 D.3 手改路径也认子目录; 若是, 该文档是**运行时指令面** ⇒ Rule #6 的 AB 范围扩到 phase-d-closer / session-closer (tech-lead 的推论, 与本文头部已改判的「照跑」是不同层级的两件事); (5) **字段名 `rel_path` 追认** —— R2 minor `4835b148` 把决策单里的 `relpath` 改成下划线口径 `rel_path` (对齐 `legacy_count` / `owner_container` / `identity_advisories`; 插件 1.71.1 全树 `\brelpath\b` 零命中, 无先例), 决策单原文未同步改, 以本文为准。**以下为裁决前的原始三选项记述, 保留供复议对照**:事实面: (a) issue-195 正文第 41 行与 triage comment `:53` 两个来源的原文都是「`filename` 字段另派生 basename」, 本文 v1 称「issue 与 triage 均倾向此案 (A)」失实, 已订正; (b) A 案会让 D.3 写出的 pointer 被姊妹 collector `handoff.py` 读不回 (§5 详述, 机制已实读逐行确认), 影响正好落在本 spec 声称要服务的子目录采用方身上; (c) A 案改既有字段取值语义, 与 §7「additive-only / `snapshot_schema_version` 保持 1.0」的声明不相容。三条可选路径 (可组合): **(i) 采纳 A′** —— 兼容面最干净, 不新增失败面, 但子目录 pointer 往返的**既有**缺口不修; **(ii) 采纳 A 并同 cycle 一并修 `handoff.py::_parse_latest_pointer` (`:288` 剥目录段) 与 `_scan_md_files` (`:300,318` 非递归) 的扁平假设** —— 修复最彻底, 但本 spec 的触点面与测试面扩大到姊妹 collector; **(iii) 采纳 A 但限定 `latest_md_writer` 只在顶层 track 时写真指针** —— 折中, 子目录采用方拿不到 pointer 语义权威。**无论选哪条, 都必须补 SC-15 的往返断言, 并按结果订正 §5 该行与 Impact 首行的「不再恒 exit 10」措辞**; 若选 (i) 或 (iii), 还须为遗留缺口另开 issue。另请一并裁定: 若最终选 A, `snapshot_schema_version` 是否 bump。
3. **`unreadable_count` 是否值得新增字段** (推荐默认: 新增)。替代方案是只留 soft_error, 但那样「有多少文件读不到」就只能靠数 errors 文本, 不可机读。
4. **dedupe tie-break 是否要在本 spec 内动排序键** (推荐默认: 不改)。它是既有设计的一部分, 本 spec 只钉现状 (SC-7, 已明标为假想输入的特性化测试); 改排序语义应另起, 否则本 spec 的反事实边界会糊掉。**R2 两处订正**: (a) 原文附带的「订正 schema `:1125` 那条在相对路径下已变假的论据」**已删除** —— A′ 下 `filename` 恒为日期前缀 basename, 该句仍为真 (`e3ca1e1a`); (b) **新增附问 (`16e07a83`)**: A′ 消除了字典序**翻转**风险, 却把 **tie 的可观测性**打开了 —— 同 `(track_id, identity_key)`、同 `updated_at`、同 `branch`、同 basename 而目录不同的两行, 四级键 `(parse_ok, updated_at, filename, branch)` 全并列 ⇒ `max()` 回退迭代顺序, 违反 `:438-452` / schema `:1126` 宣称的 build-order 不变性; 改前两行串读逐字段相同选谁都一样, **改后两行读到不同文件 ⇒ 代表行的 `status` / `phase` 可能不同**。请 owner 裁: 是否把 `rel_path` 加进排序键作为第 5 级 (成本 = 改 `_dedupe_sort_key` + 同步 schema `:1126` 的不变量表述; 不改则该 tie 的结果依赖迭代顺序, 属已知边界)。
5. **`_get_file_commit_date` 的 mv 日残余是否本 spec 处理** (推荐默认: 不处理, 但要写进 CHANGELOG 的已知边界)。#195 报告方归档进 `archive/` 的正是老格式 (无 frontmatter) 交接, 他们抱怨的「日期是归档日不是会话日」那一半**路径修好后依然存在** (§Why 与 SC-4 已实跑证明, `--follow` 也救不了「最近一次触碰该路径」的语义)。真要修只能换语义 (例: 取该路径的**最早**提交日, 或引入 `--diff-filter=A`), 属另一件事。裁决前 Phase B **不得**给该函数加 `--follow` (那既不解决问题又改了语义)。
6. **版本号**: PATCH。起草时远端已有 tag v1.71.1, 故候选 **v1.71.2**; bump 前须 `git -C aria ls-remote --tags origin` 复核并读同伴 handoff 的 `<vNEXT>` (memory `feedback_concurrent_release_numbering_check_remote_tags_and_sibling_vnext`)。

---

## References

- SOT (@`301641b`): `skills/state-scanner/scripts/collectors/handoff_multibranch.py:14-31,42,177-178,240-288,293-308,310-327,329-336,428-457,586-596,619-626,637-700` · `scripts/scan.py:119-120,126-210,255` (F1) · `scripts/collectors/handoff.py:269-330,380-410,438-440` (pointer 往返, R1 critical) · `scripts/collectors/_common.py:411-412` (`_run` 编码) · `scripts/writers/latest_md_writer.py:110-143,205-217,259` · `scripts/renderers/track_board.py:183,188,254,559` · `references/state-snapshot-schema.md:1074-1136` · `references/json-diff-normalizer.md:241` · `SKILL.md:117,149,153`
- 规范: `standards/conventions/skill-benchmark-exemption.md` (Rule #6 判据表) · `standards/conventions/session-handoff.md` §2.3 (frontmatter 契约) · `standards/conventions/version-management.md` §4.3 + 主仓 CLAUDE.md「发布同步面」(Task 5.1) · `standards/openspec/templates/proposal-minimal.md`
- 闸门: `.aria/state-checks.yaml:88` `m6-version-badge-match` · `:141` `i18n-readme-translation-currency` · `:372` `plugin-version-arch-docs-match` (三条均 `enabled: true`) · `.aria/probes/main-project-version-consistency.py:39-49` (POINTS 清单)。⚠️ **R2 实读订正 (`d58dfb65`)**: 四条合计只覆盖 Task 5.1 表里的 6 处 (#1 / #3-5 / #15-16), **另 10 处零机械兜底**; v3 的「漏改必在归档闸转红」是错误陈述, 已删
- **R2 新增引用** (本次 rework 逐处实读/实跑): `skills/state-scanner/lib/collision.py:480-486` (`collidable` 过滤 —— **Layer L 的 `lib/`, 不是 `scripts/lib/`**; 该 skill 双 `lib` 包同名遮蔽见 memory `feedback_state_scanner_dual_lib_package_shadow`) · `skills/state-scanner/references/phase-1-collectors.md:95,104` + `references/layer-l-integration.md:101,107` (writer 零生产调用点的既有设计决定) · `skills/phase-d-closer/references/handoff-mechanics.md:4,114-124` (生产 D.3 pointer 的处方决策表 + 共享 SOT 声明) · `skills/phase-d-closer/scripts/fetch_gate.py:175-188` · `skills/state-scanner/references/rules/advanced-rules.md:443-444,511-512,544` · `skills/state-scanner/RECOMMENDATION_RULES.md:28,31` · `skills/session-closer/SKILL.md:90` (允许读既有快照 ⇒ 缺 `rel_path` 的跨版本读盘路径) · `skills/state-scanner/tests/test_p1_layer_h.py:230-240,270` (八字段 `_active_track` 夹具 + 会翻红的断言) · `skills/state-scanner/tests/fixtures/freeze_corpus.py:29` (`FIELDS` 八字段投影) · `skills/state-scanner/references/state-snapshot-schema.md:46-48,1070,1125-1128,1156-1168` · `aria-plugin-benchmarks/ab-suite/state-scanner.json:214` (唯一 `tracks_multibranch` 命中; 文件 17551 B, 由 `5697477` 引入) · `standards/conventions/session-handoff.md:171-173` (latest.md 派生行为两态表述) · `docs/handoff/latest.md:103-107` (本仓自记「机械 writer 当前不可用」)
- 先例: `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/` (同 collector 家族, 冻结语料 + 反事实测试形态) · `openspec/archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md` (Level 2 标杆)
- 现场: Aria#195 issue 原文 (第 21 行点名 `_get_file_commit_date`, 第 41 行 A 案原文) · `.aria/triage-comment-195.md` (`:53` 修法倾向) / `.aria/triage-report-195.json` (2/2 复现) · 起草时临时仓 `git ls-tree` 转义实跑 (F2) · R1 rework 期 hermetic 复跑 (F2 静默漏扫 / pointer 任意深度 / mv 日期三处) · aria-plugin#155 (dedupe 由来, closed)
- R1 审计: `.aria/audit-reports/post_spec-R1-2026-09-06T154800-000Z-R1-handoff-multibranch-subdir-path-fidelity-aggregated.md` + 同前缀 5 份单席报告
- R2 审计: `.aria/audit-reports/post_spec-R2-2026-09-07T004500-000Z-R2-handoff-multibranch-subdir-path-fidelity-aggregated.md` + 同前缀 5 份单席报告; rework 处置表 scratchpad `handoff-multibranch-subdir-path-fidelity-rework-R2.md`
</content>
