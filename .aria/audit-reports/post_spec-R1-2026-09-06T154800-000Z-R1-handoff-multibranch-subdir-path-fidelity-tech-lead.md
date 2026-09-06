---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-06T16:25:59.698Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [tech-lead]
---

# post_spec 审计报告 — handoff-multibranch-subdir-path-fidelity (Round 1, tech-lead 席)

审计对象: `/home/dev/Aria/openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md`
事实基准: aria 子模块 `origin/master` = `301641b` (= v1.71.1), 行号以插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` 为准。proposal 的自述一律不采信, 逐条对真文件与真运行核。

## 审计结论

### Decisions

- [major] architecture/方案 A 的两种形态取舍与 schema 契约声明: triage 明确建议「`filename` 字段另派生 basename」(即相对路径只进 git 操作面), proposal 直接改既有 schema 字段语义, 候选方案表未列这一变体供 owner 对比; 同时仍声明「additive-only 演进契约、`snapshot_schema_version` 保持 1.0」——改既有字段取值语义不是 additive。下面的 critical 项正是这一取舍的直接产物。(证据: `.aria/triage-comment-195.md:53` · `references/state-snapshot-schema.md:1110` 「basename of the handoff file」 · proposal.md:70-75, 89, 124, 130)

**核验通过、不计 finding 的判断** (记录以便下轮不重复审):

1. A 优于 B/C 成立。实跑确认 git pathspec `docs/handoff` 只匹配 `docs/handoff/**`, 不匹配 `docs/handoff-old/c.md` 或 `docs/handoff.md`, 故 B/C 确实只能靠丢历史换不报错, 而 A 在平铺仓零行为变化。本仓 `docs/handoff/` 185 文件、零子目录、零非 ASCII; 两份冻结语料各 996 行、`filename` 零 `/` 零非 ASCII ⇒ §7「冻结语料不需重生成」成立。
2. F1 是真的。全 `.py` 树对 `docs/handoff` 硬编码前缀只有四处 (`handoff_multibranch.py:257,301,321` + `scan.py:186`), 无第五处; issue 与 triage 都未点名 `scan.py`。
3. `-z` 方案可行。`_common.py:355-360` 的 `_run` 用 `encoding=utf-8, errors=replace`, 实跑 `git ls-tree -r --name-only -z` 输出为 NUL 结尾记录 (末尾带一个空段, 与「空段丢弃」一致)。
4. §5 对 `lib/collision.py` 与 `renderers/track_board.py` 的判断成立: `lib/collision.py:480-485` 显式排除 `owner_container == "unknown"`, 少几条假 legacy 不改分类; track_board 实际不读 `filename` 字面 (只有 `track_board.py:19` 的陈旧 docstring 那样写, `_handoff_date` 只吃 `updated_at`)。
5. Rule #6 判定成立。`aria-plugin-benchmarks/ab-suite/state-scanner.json` 对四词零命中, 连 `handoff` 一词都零命中; 本 spec 触点不含 SKILL.md/`description` ⇒ 判据表第一行 substitute 正确。
6. 基线冻结的**结论**成立: 五个触点文件在 `0545f86..301641b` 间 `diff --stat` 为空 (旁证描述有误, 见 Issues)。
7. 越界检查通过: 本 spec 触点与同伴容器 v1.71.1 在飞面 (`phase1_gate.py` / `lib/claim_lifecycle.py` / `lib/identity.py` / `spec-drafter`·`phase-a-planner` SKILL.md / AB 套件) 文件级零重叠。

### Issues

- [critical] architecture/latest_md_writer 到 handoff collector 的 pointer 往返: §5 断言 `latest_md_writer.py:143` 的相对路径「天然正确、无影响」, 实跑推翻。链路是 `write_latest_md` 把 `tracks[].filename` 原样写进 `**Latest**: [x](./x)`, 而 `handoff.py:288` 用 `Path(target).name` 剥掉目录段、`handoff.py:300-301` 的 `_scan_md_files` 非递归, 于是子目录里的 active track 写出去的 pointer 再也读不回来。(证据: proposal.md:116 · `writers/latest_md_writer.py:143,295-304` · `collectors/handoff.py:263-288,300-327,383-404` · 我在 scratchpad 对 `301641b` 副本打上 proposal 的枚举层改法后实跑两例: 变体 A「仓内交接全在子目录」→ 收集器给出 `filename="sub/2026-09-06-subdir-track.md"` 且 legacy_count=0 (修本身有效), 但 `collect_handoff` 返回 `exists=False`、`latest_source=None`、**零 soft_error** ——两个 collector 在同一快照里互相矛盾且无任何信号; 变体 B「顶层有旧件 + 子目录 active」→ `handoff_pointer_target_missing`, `latest_source=mtime`, latest 落到更旧的 done 文档, scan 依旧 exit 10)
  - 影响正好落在本 spec 服务的人群 (采用子目录布局的仓), 且与 SC-12「子目录仓 exit 0」的承诺在 D.3 写完 latest.md 后即失效; 也重开了 H5 「pointer 是语义权威、mtime 只是兜底」那条既有修复。
  - 处置建议 (任一): 保持 `TrackEntry.filename` 为 basename、另加 `relpath` 字段供 git 操作与 `scan.py:186` 消费 (= triage 原建议); 或在本 cycle 同时修 `handoff.py::_parse_latest_pointer` 与 `_scan_md_files` 的扁平假设, 并补一条「writer 写出 → collector 读回」的往返 SC。
- [major] architecture/ship 顺序与主仓 gitlink 归属: proposal 的 ship 计划建立在陈旧的 origin 视图上。实况: `origin/master` = `9f25a66`「Merge pull request #202 … from feature/a1-entry-claim-duplicate-work-guard」, 提交时间 2026-09-06T15:27:16Z; `git ls-tree origin/master aria` 已是 `301641b`, 其中 `4c3c826` 就是「主仓同步 aria-plugin v1.71.1 — gitlink 301641b + 16 处版本点」。而 proposal 于 15:46:20Z 提交 (本地 `.git/refs/remotes/origin/master` 早在 15:31:43 就已更新到 9f25a66) 仍写「尚未开 PR / gitlink 仍指 0545f86 / 本 spec gitlink bump 排在其 PR 之后」, 并把一个已不存在的选择升级给 owner。本地 master 与 origin 已分叉 (本地 HEAD 非 origin/master 祖先)。若 Phase C 照字面在陈旧 master 上把 gitlink 从 `0545f86` 前进, 会把主仓 gitlink 从 `301641b` 回退。(证据: proposal.md:9,158,197 · `git log -1 --format=%ad origin/master` · `git ls-tree origin/master aria` · `git rev-list --left-right --count origin/master...origin/feature/a1-entry-claim-duplicate-work-guard` = `1 0`)
- [major] implementation/F1 与 SC-6 引用的函数符号: proposal 三处称跨文件消费方为 `_check_handoff_ancestry`, 该符号在 `301641b` 的 `scripts/` 与 `tests/` 全树零命中。真实符号是 `scan.py:126 _same_branch_head_unreachable_tracks` (由 `scan.py:216 _check_snapshot_self_consistency` 调用, 且带 `claims_health` 与「track.branch == 当前分支」两道前置)。SC-6 按字面写不出测试, 且实施者需要知道那两道前置才能构造用例。(证据: proposal.md:41,115,172 · `scripts/scan.py:126,216,250-257,177-186`)
- [major] testing/SC-10 基线数字与基线冻结旁证: 两处起草期机械核验的数字与实测不符。其一, SC-10 的「改前基线已实测: 73 tests OK」——同一条命令在三处实测均为 **78** (`301641b` 抽取副本逐模块 21+27+25+5; 1.71.1 插件缓存 78 OK; 仓内 aria 工作树 78 OK)。其二, frontmatter 称两 SHA 间「只新增了 7 个 a1-entry 相关测试文件」——实为 **29 文件变更、2462 行新增**, 其中新增测试文件 5 个, 另有 `lib/collision.py` / `lib/identity.py` / `lib/claim_lifecycle.py` / `phase1_gate.py` / `scripts/lib/spec_complete.py` 等生产文件与 6 个 SKILL.md; §5 对 collision 的影响判断恰恰依赖这个文件 (我已按 `301641b` 版本复核, 结论仍成立, 但旁证描述会误导下一位 reviewer 跳过复核)。SC-10 的另两项 (`1571 tests` 与两项已知失败) 我在 `301641b` 抽取副本上复现属实, 不属错误。(证据: proposal.md:9,176 · `git diff --name-status 0545f86 301641b` · `python3 -m unittest` 三处实跑 · 抽取副本 discover 输出 `Ran 1571 tests`, 含 `Test1210ChannelStabilityUnderOffline` setUpClass ERROR 与 `TestStabilityIntegration.test_two_consecutive_runs_diff_zero` FAIL)

### Risks

- [minor] testing/SC-2 的改前基线动态载入机制: 「测试内以 `git show 301641b:` 取原实现动态载入」在本套件无先例 (`tests/` 全树零 `importlib` / `exec`), 且 collector 用相对 import (`from ._common import` / `from .handoff import`), 载入需自建包上下文; 更实际的是插件把 `tests/` 一并分发到无 `.git` 的 cache 目录 (我就在那里跑过全套), 而组织的 CI checkout 约定是 `fetch-depth: 1` ——三者都会让这条守 top-risk 的测试在异地 error。它失败得响亮 (不会假绿), 但建议改用已存在的冻结语料或 vendored baseline。(证据: proposal.md:168 · `collectors/handoff_multibranch.py:120,127` · `.forgejo/workflows/issue-triage-tests.yml:33-35` · `grep -rn "importlib.util\|exec_module" tests/*.py` 零命中)
- [minor] documentation/SC-4 与 Why 第三层后果的表述张力: Why 把「mv 提交日期污染 updated_at」列为要修的第三层后果, SC-4 又把无 frontmatter 文件取到 mv 日定为预期真值。两者都对 (路径修正后, 有 frontmatter 的走 frontmatter 日期; 无 frontmatter 的只能靠 `git log -1`, 且 `--follow` 也救不了「最近一次触碰该路径」的语义), 但报告方归档进 `archive/` 的正是老格式交接——他们抱怨的那一半可能仍在。建议把这条残余写进 Impact.Risk 或待 owner 复议, 别只藏在 SC-4 的括号里。(证据: proposal.md:35,170 · `collectors/handoff_multibranch.py:310-326,682-705`)
- [minor] implementation/F2 非 ASCII 修复的覆盖边界: `_run` 用 `errors="replace"` 解码, 真正非 UTF-8 字节的文件名解码即失真, `-z` 也拼不回对象——修后它从「假 legacy 行」变成「新的 unreadable 分支 + 继续 exit 10」, 并非修好; 同类文件名在 `handoff.py:318-322` 是显式跳过。建议 schema 与 CHANGELOG 把 F2 的覆盖面写成「可解码 UTF-8 的非 ASCII 名」, 并考虑对不可解码名显式跳过而非计入 `unreadable_count`。(证据: proposal.md:49-62,169 · `collectors/_common.py:355-360` · `collectors/handoff.py:308-322`)

## Verdict

**FAIL** — Critical 1 / Major 4 / Minor 3。

理由: 唯一的 critical 不是推理, 是实跑结论——按 proposal 写法改完枚举层后, 用真生产代码跑完「collector 出 filename → writer 写 latest.md → handoff collector 读回」这条链, 在子目录仓上要么静默自相矛盾 (`handoff.exists=False` 且零告警), 要么报 `handoff_pointer_target_missing` 并把 latest 指到更旧的文档、scan 继续 exit 10。这落在本 spec 声称要服务的那类仓上, 而 §5 对该消费方的结论恰好写成「无影响」, 实施者不会去碰它。四条 major 中, ship 顺序那条会直接把主仓 gitlink 从 `301641b` 推回去; 函数名与基线数字两条使 SC-6/SC-10 不能按字面执行。post_spec 为 `blocking: false`, 本 verdict 只作记录, 但按横切「数据可用性」原则, 基线规模不符必须载重到 verdict, 故 vote = REVISE。

修订后重审建议聚焦三点: (1) `filename` 语义取舍重做一次并给出往返 SC; (2) 依 `origin/master` 9f25a66 重写 ship 顺序段与待复议 5; (3) 订正符号名与两处基线数字。

## 轮次记录

### Round 1

- Agents: tech-lead (五席之一, 本报告仅本席结论)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 8 (Decisions 1 / Issues 4 / Risks 3)
- Vote: REVISE

核验手段留痕 (全部只读, 未改仓库任何文件; 临时副本与探针脚本均落 scratchpad):

1. 实读 SOT: `handoff_multibranch.py` / `scan.py` / `latest_md_writer.py` / `track_board.py` / `handoff.py` / `_common.py` / `lib/collision.py` / `state-snapshot-schema.md` / `validate_schema_doc.py`。
2. 实跑测试: 四模块命令在三处 (1.71.1 cache / 仓内工作树 / `301641b` 抽取副本) 均 78; 全量 discover 在仓内工作树 1505 OK, 在 `301641b` 抽取副本 1571 (含 proposal 点名的两项失败)。
3. 实跑 git 语义: pathspec 边界与 `ls-tree -z` NUL 形态。
4. 实跑端到端探针: 对 `301641b` 抽取副本打上 proposal 的枚举层改法, 跑 `collect_handoff_multibranch` → `write_latest_md` → `collect_handoff` 两个变体。
5. 数据可用性核: 两份冻结语料存在且各 996 行零子目录零非 ASCII; 本仓 `docs/handoff/` 185 文件零子目录零非 ASCII; AB 套件四词零命中; 主仓 open PR 列表为空、`origin/master` 与 gitlink 实况如上。
