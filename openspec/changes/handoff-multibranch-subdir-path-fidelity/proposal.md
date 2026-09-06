# handoff_multibranch 路径保真: ls-tree 相对路径贯穿全部四个调用方 + 读不到不再伪造 legacy track (Aria #195)

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-06
> **Linked Issue**: `10CG/Aria#195`
> **Issue**: [Aria#195](https://forgejo.10cg.pub/10CG/Aria/issues/195) (2026-09-05 立案, aria-report 自动生成; triage 22287: confirmed / major / next-cycle, 2/2 复现)
> **认领**: 已于 2026-09-06T14:47Z 经 `phase1_gate.py --phase A.1 --mode advisory --linked-issue 10CG/Aria#195 --include-terminal` 认领, track_id `handoff-multibranch-subdir-path-fidelity-bfe8285d`, `outcome=passed`, `linked_issue_overlap=[]`, `unknown_schema_claims=0`, `push_success=true`
> **基线冻结**: aria 子模块 `origin/master` **`301641b`** (= v1.71.1)。本文全部行号对此 SHA (实读副本 = 插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/`)。起草时核验 `git -C aria diff --stat 0545f86 301641b -- skills/state-scanner/scripts/collectors/handoff_multibranch.py skills/state-scanner/scripts/scan.py skills/state-scanner/scripts/writers/latest_md_writer.py skills/state-scanner/scripts/renderers/track_board.py skills/state-scanner/references/state-snapshot-schema.md`: **本 spec 全部触点文件零 diff** (两 SHA 间只新增了 7 个 a1-entry 相关测试文件, 均不触碰本触点) ⇒ 行号在两 SHA 上一致。Phase B 在 `301641b` 起分支。主仓 `aria/` gitlink 仍指 `0545f86` (v1.70.0): 同伴容器 v1.71.1 的主仓同步分支 `feature/a1-entry-claim-duplicate-work-guard` 尚未开 PR, **本 spec 的主仓 gitlink bump 排在其 PR 合并之后**
> **代码落点**: `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py` (`_list_handoff_files` / `_read_file_content` / `_get_file_commit_date` / 主循环 git-show 失败分支) · `aria/skills/state-scanner/scripts/scan.py:186` (**第四个硬编码前缀点, issue 与 triage 均未点名**) · `aria/skills/state-scanner/tests/test_handoff_multibranch_path_fidelity.py` (新增) · `aria/skills/state-scanner/references/state-snapshot-schema.md` §`tracks_multibranch` · `aria/CHANGELOG.md` + 版本 SOT 5 文件。Spec 落主仓 (Rule #5)
> **Rule #6 判定**: 本变更全部落在 **纯代码 + schema 文档描述** 面 —— 无 `description` 变动, 无 SKILL.md 运行时指令面变动 (SKILL.md 只在 collector 清单里出现 `tracks_multibranch` 一词, 本 spec 不改它)。判据表**第一行 (描述性)** ⇒ substitute = SC 级 baseline-failing 结构化测试 (SC-1~SC-9)。核实过套件确无覆盖: `ab-suite/state-scanner.json` 对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` 四词 **零命中**。rule6_note 见文末
> **A.1.0 头脑风暴**: 未跑 — `audit.checkpoints.post_brainstorm = off` (Rule #10 白名单第一类)
> **审计计划**: post_spec convergence 5 席 (config enabled) → post_planning convergence (config enabled); mid_implementation / post_implementation / pre_merge / post_closure 均 config 显式 off (白名单第一类)

---

## Why

### 症状 (issue + triage 复现, 起草时对 `301641b` 逐条复核)

`handoff_multibranch` collector 用**递归**枚举 (`git ls-tree -r`) 找 `docs/handoff/` 下的交接文件, 却只把 basename 交给下游; 下游三个调用方各自用**写死的 `docs/handoff/<basename>` 前缀**拼回 git 对象路径。递归枚举与固定前缀不自洽 —— 任何位于子目录 (典型: `docs/handoff/archive/`) 的 `.md` 必然拼出不存在的路径。

| 位置 (@`301641b`) | 实况 |
|---|---|
| `handoff_multibranch.py:178` | `_HANDOFF_TREE_PATH = "docs/handoff"` |
| `:240-288` `_list_handoff_files` | `git ls-tree -r --name-only origin/<branch> -- docs/handoff`; `:275` `basename = Path(path).name` 丢弃目录段; docstring `:244-250` 自述「callers compose the full git-object path as needed」—— 而三个调用方都无法还原 |
| `:301` `_read_file_content` | `ref = f"{_REMOTE}/{branch}:{_HANDOFF_TREE_PATH}/{filename}"` |
| `:321` `_get_file_commit_date` | `path = f"{_HANDOFF_TREE_PATH}/{filename}"` (issue 未点名, 但它是 `updated_at` 失真的直接来源) |
| `:637-658` 主循环 | `git show` 失败 ⇒ `soft_error` + **追加一条 `status: legacy` 假 track** (`owner_container: unknown`, `updated_at` = 上面那个 fallback) |

后果三层, 逐层加重:

1. 每个子目录文件产生一条 `handoff_multibranch_git_show_failed`, `scan.py` 恒 exit 10 (告警噪声)。
2. 假 track 进 `tracks[]` 与 `legacy_count`, 污染 `tracks_multibranch` 看板 —— 「读不到内容」被当成「这是一份老格式交接」, 两件事被折叠。
3. 假 track 的 `updated_at` 取自 `_get_file_commit_date` 的同一错误路径; 若该文件曾在顶层存在过、后被 `git mv` 进子目录, `git log` 会命中**归档那次 mv 的提交日期**, 而不是交接本身的会话日期 —— 数据失真且看起来完全合理。

triage (comment 22287) 的两条 hermetic case 在当前代码上 **2/2 命中**, 其中 case-2 逐字复现了「双重失真」(`updated_at = 2026-08-15T12:00:00+00:00` = mv 提交日)。

### 起草期实读补充的两条事实 (issue 与 triage 都没有, 二者都扩大了修复面)

**F1 — 硬编码前缀不是三处, 是四处。** `scan.py:186` 的 AC-5 跨 collector 一致性检查 (`_check_handoff_ancestry`) 独立拼了一次:

```python
"git", "log", "-1", "--format=%H", f"{remote}/{branch}", "--", f"docs/handoff/{filename}",
```

它在 collector 之外、另一个文件里消费 `tracks[].filename`。只改 collector 内的三处会留下一个静默失效的跨文件消费方 (`git log` 对不存在路径返回空 ⇒ `continue` ⇒ 该文件的 ancestry 检查被跳过, 无任何告警)。这正是 memory `feedback_test_runner_scope_blind_to_cross_skill_consumers` 说的形态: 只跑本 skill 的测试看不见它。

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

非 ASCII 文件名今天会被 `Path(path).name` 取成 `2026-\346\265\213\350\257\225.md"` 这样的转义串, 同样拼不回真实对象路径, 同样落进那条假 legacy 分支 —— **与子目录是同一个 bug 类 (枚举层输出 ≠ 可回拼的路径), 只是触发条件不同**。中文/日文命名的交接文件在本项目生态里完全可能 (本仓工作语言即中文)。修枚举层时若不一并处理, 等于修了一半。

### 根因

不是笔误, 是**契约错配**: 枚举层承诺「调用方自行拼完整路径」, 但它交出去的东西 (转义后的 basename) 在信息论上就不足以拼回。修法必须让枚举层交出**可回拼的路径**, 并让全部四个调用方都用它。

### 候选方案与否决理由

| 方案 | 内容 | 判决 |
|---|---|---|
| **A (采纳)** | 枚举层保留 ls-tree 原样相对路径 (相对 `docs/handoff/`), 四个调用方直接用它拼 ref | 支持任意子目录布局; 平铺仓 (含 Aria 自身) 的取值与今天**逐字节相同** ⇒ 零行为变化。issue 与 triage 均倾向此案 |
| B | `ls-tree` 去掉 `-r`, 只扫顶层 | 语义最简, 但**静默丢弃**子目录里的全部交接历史。把归档放子目录的采用方等于那段历史不进看板 —— 用"看不见"换"不报错", 与本 collector 的用途 (多终端交接发现) 直接冲突 |
| C | 保留 `-r`, 显式 `continue` 掉非顶层项 | 行为同 B, 只是把意图写进代码。仍然丢历史; 且它把「递归枚举」这个正确动作退回去, 而真正错的是下游拼路径 |
| D (附加, 采纳) | git show 失败不再降级为 legacy track, 只报 soft_error | 与 A/B/C 正交。issue 明确提出; 「读不到」与「老格式」是两件事, 折叠它们让失真数据带着误导性 `updated_at` 进看板 |

---

## What

### 1. 枚举层 `_list_handoff_files` (`:240-288`)

| | 改前 | 改后 |
|---|---|---|
| ls-tree 调用 | `git ls-tree -r --name-only <ref> -- docs/handoff` | 加 `-z` (NUL 分隔, 关闭引号转义); 按 `\0` 切分, 空段丢弃 (F2) |
| 每项取值 | `basename = Path(path).name` | `rel = path[len("docs/handoff/"):]` —— **相对 `docs/handoff/` 的路径**; 不以该前缀开头的行 (理论上不会出现) 计一条 soft_error 并跳过, 不静默吞 |
| `.md` 过滤 | 对 basename 判 `.endswith(".md")` | 对 `rel` 的 **basename** 判 (语义不变) |
| pointer 排除 | `basename == "latest.md"` | **basename == "latest.md" (任意深度)** —— 保守: `archive/latest.md` 这类归档指针同样不是交接, 一并排除; 该口径写进 schema 文档 |
| 返回 | `list[str]` basename | `list[str]` 相对路径 (平铺仓两者逐字节相同) |
| docstring | 「Returns only the basename … so callers compose the full git-object path as needed」 | 改为「Returns each file's path **relative to `docs/handoff/`** …」—— 契约与实现对齐 (根因就在这句自述上) |

### 2. 三个仓内调用方改用相对路径 (语义不变, 只是不再丢信息)

- `_read_file_content:301`: `ref = f"{_REMOTE}/{branch}:{_HANDOFF_TREE_PATH}/{relpath}"` (拼法不变, 入参含义变准)
- `_get_file_commit_date:321`: 同上, 因此 `updated_at` 不再取到 mv 提交日
- `_make_legacy_track_id:329-336`: `legacy:<branch>:<relpath>` —— 用相对路径而非 basename, 防两个子目录下同名文件产生同一 legacy track_id (碰撞会被 `dedupe` 当成同一 track)

### 3. `scan.py:186` (F1, 跨文件消费方)

`f"docs/handoff/{filename}"` 保持字面不变即可正确 —— 因为 `filename` 现在就是相对路径。**但必须有测试钉住这个隐式耦合**: 该行与 collector 的 `_HANDOFF_TREE_PATH` 是两处独立字面量, 今天靠巧合一致。SC-6 用一条断言把它锁住 (子目录 track 的 ancestry 检查必须真的执行到 `git log`, 而不是拼错路径后返回空再 `continue`)。

### 4. git show 失败不再伪造 legacy track (`:637-658`)

| | 改前 | 改后 |
|---|---|---|
| 行为 | soft_error + 追加 `status: legacy` 行 + `legacy_count += 1` | 只 soft_error; **不进 `tracks[]`**, 不计 `legacy_count` |
| 计数 | 无 | 新增 additive 字段 `unreadable_count: int` (恒存在, 默认 0) —— 信息不丢, 只是搬到正确的名字下 |

无 frontmatter 的真 legacy 分支 (`:683-700`) **不动** —— 那才是「老格式交接」的本义。

### 5. 消费方枚举 (起草时 grep 全 skill 树 + 主仓, 逐个判)

| 消费方 | 用法 | 本变更影响 |
|---|---|---|
| `scan.py:186` `_check_handoff_ancestry` | `git log … -- docs/handoff/{filename}` | F1, 见 §3 —— 相对路径后才真正可用 |
| `writers/latest_md_writer.py:143` | `**Latest**: [{filename}](./{filename})` | 链接基准就是 `docs/handoff/`, 相对路径 `./archive/x.md` 天然正确 |
| `writers/latest_md_writer.py:208-217` | legacy 表展示 `filename` 列 | 展示相对路径, 更准; 平铺仓不变 |
| `handoff_multibranch.py:428-457` `_dedupe_sort_key` | 4 级键第 3 级按 `filename` 字典序取大 | **有行为面**: `archive/…` (`a`=0x61) 字典序大于 `2026-…` (`2`=0x32), 故同 `(track_id, identity_key)` 且 `updated_at` 完全相同时, 归档副本会赢。仅在该三重并列时可达; 归档件通常更旧 ⇒ 记入 Impact.Risk 并由 SC-7 钉住现状行为 (不在本 spec 改排序语义, 那是另一件事) |
| `renderers/track_board.py` | 消费 `tracks[]` / `collision`, 不读 `filename` 字面 | 无影响 (起草时 grep 确认) |
| `lib/collision.py` | 按 `track_id` / `owner_container` 分组 | legacy 行的 `owner_container` 恒 `unknown`, `classify()` 本就排除 ⇒ 少几条假 legacy 行不改分类结果 |

### 6. 文档同步 (Rule #3)

`references/state-snapshot-schema.md` §`tracks_multibranch` (`:1074` 起): `filename` 字段语义改为「相对 `docs/handoff/` 的路径 (平铺仓 = basename)」· 新增 `unreadable_count` · 写明 pointer 排除口径 (任意深度的 `latest.md`) · 写明「git show 失败不再产生 legacy 行」。CHANGELOG 记 Fixed 三条 (子目录 / 非 ASCII / 假 legacy)。

### 7. 向后兼容

- **平铺仓 (含 Aria 自身)**: `filename` / `track_id` / `legacy_count` 取值逐字节不变 —— 本仓 `docs/handoff/` 无子目录、无非 ASCII 文件名 (Task 1.1 机械核验)。既有冻结语料 `tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 与 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 因此不需重生成 (Task 1.1 同时核验其中无子目录路径)。
- **子目录仓**: 从「假 legacy + 失真日期」变成「真 track + 真日期」, 是修复不是破坏。
- `unreadable_count` 为 additive 新键, 老消费方不读它即可。`snapshot_schema_version` 保持 `"1.0"` (additive-only 演进契约)。

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 子目录 / 非 ASCII 布局的采用方不再每次 scan 恒 exit 10; 看板不再混入假 track 与 mv 日期; 「读不到」与「老格式」两个状态分开, 后续判据可分别处置 |
| **Positive** | 修掉一个跨文件静默失效点 (F1): AC-5 ancestry 检查对子目录交接从「拼错路径后无声跳过」变成真检查 |
| **Risk** | dedupe 第 3 级 tie-break 在 `archive/` 前缀下字典序变大, 三重并列时选中归档副本。缓解: SC-7 用定向用例钉住并在 schema 文档写明; 该并列需 `track_id` + `identity_key` + `updated_at` 全同, 概率低且两行内容通常一致 |
| **Risk** | `legacy_count` 语义收窄 (不再含读不到的文件)。缓解: `unreadable_count` 承接, schema 文档写明, CHANGELOG 标注 |
| **Risk** | `-z` 改变了 ls-tree 输出解析形态, 解析写错会让**所有**分支枚举返回空 (静默失明, 比原 bug 更坏)。缓解: SC-2 对平铺仓断言枚举结果非空且与改前逐字节相同 (反事实: 解析写错 ⇒ 空集 ⇒ 红) |

---

## Tasks

- [ ] 1.1 前置核验: 本仓 `docs/handoff/` 无子目录与非 ASCII 文件名; 两份冻结语料内无子目录路径 (机械命令 + 结果抄进 tasks 记录)
- [ ] 1.2 建红测: 新测试文件覆盖子目录 / 非 ASCII / git-show 失败三族, 对 `301641b` 全红且红在正确断言上
- [ ] 2.1 枚举层改造 (`-z` + 相对路径 + 前缀剥离守卫 + pointer 任意深度排除 + docstring 契约对齐)
- [ ] 2.2 三个仓内调用方与 legacy track_id 改用相对路径
- [ ] 2.3 git-show 失败分支改为只报 soft_error; 新增 `unreadable_count`
- [ ] 3.1 `scan.py` AC-5 跨文件消费方钉测 (F1)
- [ ] 3.2 dedupe tie-break 现状钉测 (风险面)
- [ ] 4.1 schema 文档同步 (`filename` 语义 / `unreadable_count` / pointer 口径 / legacy 分支)
- [ ] 4.2 既有测试全绿 + 平铺仓零行为变化断言
- [ ] 5.1 版本 SOT 5 文件 + CHANGELOG (PATCH)
- [ ] 5.2 Phase C: aria 本地 merge + 双推核验; 主仓 spec/gitlink (gitlink 排在同伴 PR 之后)
- [ ] 5.3 Phase D: 归档 + `release_gate` claim 释放 + #195 关闭回帖

---

## Success Criteria (可证伪; 每条自问「机制没实现会红吗」)

| SC | 断言 | 核验 |
|---|---|---|
| SC-1 | **hermetic case-1 (issue 主症状)**: 临时仓, `docs/handoff/archive/2026-05-09-session-end.md` 从未在顶层存在过, 有合法 frontmatter → `tracks[]` 含一条 `legacy: false` 行, `filename == "archive/2026-05-09-session-end.md"`, `track_id` 取自 frontmatter, `updated_at` 取自 frontmatter; `errors[]` 无 `handoff_multibranch_git_show_failed`; `legacy_count == 0`。**反事实**: 回退枚举层为 basename ⇒ git show 失败 ⇒ 该断言全红 | `test_handoff_multibranch_path_fidelity.py::test_subdir_file_read_as_real_track` |
| SC-2 | **平铺仓零行为变化**: 同一临时仓只放顶层文件, 改前 (`301641b` 原函数, 测试内以 `git show 301641b:` 取原实现动态载入) 与改后 `collect_handoff_multibranch` 的 `tracks[]` / `legacy_count` **逐字段相等**。**反事实**: `-z` 解析写错 ⇒ 枚举空集 ⇒ 两侧不等 ⇒ 红 | `::test_flat_repo_byte_identical_to_baseline` |
| SC-3 | **非 ASCII (F2)**: `docs/handoff/2026-测试-交接.md` (合法 frontmatter) → 被读成真 track, `filename == "2026-测试-交接.md"` (无引号无八进制转义); `git show` 未失败。**反事实**: 去掉 `-z` ⇒ filename 含 `\346` 且 git show 失败 ⇒ 红 | `::test_non_ascii_filename_not_escaped` |
| SC-4 | **`updated_at` 不再取 mv 日期 (issue 双重失真)**: 顶层 commit (作者日期 2026-05-09) → `git mv` 进 `archive/` (2026-08-15) 且文件**无** frontmatter → legacy 行的 `updated_at` = `2026-08-15…` (mv 日, 这是 `git log -1` 的真值, 路径正确后仍如此, 属预期); 而**有** frontmatter 的同形文件 → `updated_at` 取 frontmatter 值 `2026-05-09…`, 与 mv 日无关。断言两者分别成立 | `::test_moved_file_dates` |
| SC-5 | **git show 失败不再伪造 legacy**: 构造一条枚举得到、但 `git show` 必失败的路径 (枚举后删除该对象所在 ref / 用 monkeypatch 让 `_read_file_content` 返回错误) → `errors[]` 含 `handoff_multibranch_git_show_failed`, `tracks[]` **不含**对应行, `legacy_count` 不增, `unreadable_count == 1`。**反事实**: 保留旧降级分支 ⇒ tracks 多一行 ⇒ 红 | `::test_unreadable_not_downgraded_to_legacy` |
| SC-6 | **F1 跨文件消费方**: 对含子目录 track 的快照跑 `scan.py::_check_handoff_ancestry`, 断言它对该 track 真的执行了 `git log`(命令行含 `docs/handoff/archive/…`) 且得到非空 SHA —— 而不是拼错路径后空返回。**反事实**: 把 collector 退回 basename ⇒ 命令行路径不存在 ⇒ 空 SHA ⇒ 断言红 | `::test_scan_ancestry_consumer_uses_relative_path` |
| SC-7 | **dedupe tie-break 现状钉住 (风险面)**: 同 `(track_id, identity_key)` 两行, `updated_at` 完全相同, filename 分别为 `2026-07-19-x.md` 与 `archive/2026-07-19-x.md` → `dedupe_latest_per_track_container` 选中 `archive/…` 那行 (字典序大)。此为**现状记录性断言**, 用于让未来改排序语义的人当场看见 | `::test_dedupe_tiebreak_prefers_lexicographic_max_path` |
| SC-8 | **pointer 排除口径**: 顶层 `latest.md` 与 `archive/latest.md` 均不出现在 `tracks[]`; `archive/latest-notes.md` (非 `latest.md`) 正常进入 | `::test_pointer_excluded_at_any_depth` |
| SC-9 | **前缀守卫不静默吞**: 构造一条不以 `docs/handoff/` 开头的枚举返回 (monkeypatch `_run`) → 计一条 soft_error 且不进 `tracks[]`, 不 crash | `::test_unexpected_prefix_soft_errors` |
| SC-10 | **既有测试全绿**: `cd aria/skills/state-scanner/tests && python3 -m unittest test_handoff_multibranch_collision_dedupe test_handoff test_handoff_worktrees test_track_board_advisories` 0 failure (改前基线已实测: 73 tests OK)。全量 `discover` 另跑并与改前基线逐条对比 —— 改前基线**已知 2 项非本 spec 失败** (`test_normalize_snapshot.Test1210ChannelStabilityUnderOffline` setUpClass ERROR + `TestStabilityIntegration.test_two_consecutive_runs_diff_zero` FAIL, 1571 tests), 允许原样存在但**不得新增**, 且须 `git log -- <file>` 核实本 cycle 未触碰 | 命令 + 对比 |
| SC-11 | **文档同步机检**: `grep -c 'unreadable_count' references/state-snapshot-schema.md` ≥ 1; schema 文档 `filename` 行含「相对」二字; `grep -c 'basename' collectors/handoff_multibranch.py` 相对基线**减少** (docstring 契约已改写); CHANGELOG 含本 spec 三条 Fixed | grep |
| SC-12 | **活体 dogfood**: 在本仓跑 `python3 aria/skills/state-scanner/scripts/scan.py --output /tmp/…/snap-after.json`, 与改前 `.aria/state-snapshot.json` 的 `tracks_multibranch` 做逐字段 diff → 除 `unreadable_count` 新键外**零差异** (本仓平铺, SC-2 的活体版); 另在临时子目录仓跑同一命令 → exit 0 (改前 exit 10)。输出抄进 handoff | 命令 + handoff 证据 |

---

## rule6_note (Rule #6 — 判据表第一行「描述性」, SOT `standards/conventions/skill-benchmark-exemption.md`)

- **变更性质**: 全部是 collector 代码 + 输出 schema 文档。**无** `description` 变动, **无** SKILL.md / references 里任何「AI 该怎么做」的处方性指令变动 (核实: 本 spec 触点不含 SKILL.md; schema 文档改的是字段语义描述, 不是编排指令)。按判据表第一行 ⇒ AB 不适用, substitute = SC 级 baseline-failing 结构化测试。
- **套件覆盖实测**: `python3 -c "json.load(open('aria-plugin-benchmarks/ab-suite/state-scanner.json'))"` 全文对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` **四词零命中** —— 即使想跑也测不到本 collector; 对它跑全套件 = 测量剧场 (memory `feedback_static_benchmark_unfit_as_oneshot_selection_gate` 同族)。
- **substitute 覆盖**: SC-1~SC-9 逐条对应一个行为改动, 每条附反事实 (回退该机制后应转红); SC-10 守既有面; SC-11 守文档面; SC-12 是活体。
- **不豁免的部分**: 无。若 Phase B 期间发现需要改 SKILL.md 指令面 (例如新增「AI 见到 `unreadable_count > 0` 该怎么说」的处方), **立即改判照跑 AB** (宁跑勿豁), 并在 tasks 留痕。

---

## 待 owner 复议

1. **pointer 排除是否覆盖任意深度** (推荐默认: 是)。`archive/latest.md` 归档指针不是交接, 排除更保守。反对意见可能是「排除逻辑应只针对活指针」——若采纳反对, SC-8 后半条改为断言它进入 `tracks[]`。
2. **`unreadable_count` 是否值得新增字段** (推荐默认: 新增)。替代方案是只留 soft_error, 但那样「有多少文件读不到」就只能靠数 errors 文本, 不可机读。
3. **dedupe tie-break 是否要在本 spec 内改成「路径深度浅者优先」** (推荐默认: 不改)。它是既有设计的一部分, 本 spec 只钉现状 (SC-7); 改排序语义应另起, 否则本 spec 的反事实边界会糊掉。
4. **版本号**: PATCH。起草时远端已有 tag v1.71.1, 故候选 **v1.71.2**; bump 前须 `git -C aria ls-remote --tags origin` 复核并读同伴 handoff 的 `<vNEXT>` (memory `feedback_concurrent_release_numbering_check_remote_tags_and_sibling_vnext`)。
5. **主仓 gitlink bump 时机**: 本 spec ship 后, 主仓 `aria` gitlink 需从 `0545f86` 直接跳到本 spec 的 merge commit —— 但同伴容器的 v1.71.1 主仓同步分支尚未开 PR。推荐默认: **等同伴 PR 合并后再 bump**, 若届时仍未合, 由 owner 裁是否由本轨代为前进 (代为前进会吞掉他们那份 16 处版本点改动, 不可自作主张)。

---

## References

- SOT (@`301641b`): `skills/state-scanner/scripts/collectors/handoff_multibranch.py:178,240-288,293-308,310-327,329-336,428-457,637-700` · `scripts/scan.py:165-210` (F1) · `scripts/writers/latest_md_writer.py:113-143,205-217` · `references/state-snapshot-schema.md:1074-1136`
- 规范: `standards/conventions/skill-benchmark-exemption.md` (Rule #6 判据表) · `standards/conventions/session-handoff.md` §2.3 (frontmatter 契约) · `standards/openspec/templates/proposal-minimal.md`
- 先例: `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/` (同 collector 家族, 冻结语料 + 反事实测试形态) · `openspec/archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md` (Level 2 标杆)
- 现场: Aria#195 issue 原文 · `.aria/triage-comment-195.md` / `.aria/triage-report-195.json` (2/2 复现) · 起草时临时仓 `git ls-tree` 转义实跑 (F2) · aria-plugin#155 (dedupe 由来) / #182 (handoff status 不收口, 相邻但不同根因)
