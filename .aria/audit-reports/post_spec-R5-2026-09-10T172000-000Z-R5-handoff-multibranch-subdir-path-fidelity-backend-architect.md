---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T17:25:56.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [backend-architect]
---

# post_spec 单席审计报告 — backend-architect (Round 5)

席位透镜: 数据契约与实现可行性 —— 字段语义变更的向后兼容与消费方枚举完整性 (自行 grep 核实, 不采信 proposal 的表) / 错误路径是否穷举 / 伪代码与真代码结构是否对得上。

被审对象: `openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` (408 行 / 191908 B, v6 = R4 rework 后)。全部行号以插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= aria `301641b` / v1.71.1) 为准, 逐处实读。

---

## 审计结论

### Decisions

- [minor] architecture/消费方枚举完整性: 独立全树 grep 复核 —— `tracks[].filename` 的全部非测试消费点恰为 4 处: `handoff_multibranch.py:455` (dedupe 第 3 级键) · `scan.py:180` (喂 `:186` 拼串 + `:193`/`:209` 上报) · `latest_md_writer.py:116` (`_render_pointer`) · `:213` (banner legacy 表), §5 逐条在册, **无遗漏** (证据: `grep -rn '\["filename"\]\|\.get("filename")' skills/ --include=*.py | grep -v /tests/`)。
- [minor] architecture/硬编码前缀点数复核: 非测试面 `docs/handoff/` 字面拼串恰 4 处 = collector 内 3 处经 `_HANDOFF_TREE_PATH` 派生 (`:257` ls-tree pathspec / `:301` git show / `:321` git log) + `scan.py:186` 独立字面量, 与 §Why F1 一致; `handoff.py`/`handoff_worktrees.py` 走本地 FS 的 `CANONICAL_DIR` (`handoff.py:254`), 不是同一失效族。
- [minor] testing/additive 声明对现有测试面成立: 全树无任何测试断言 track dict 或 `handoff_multibranch` 的 `r.data` 精确键集 (`.keys()` 断言仅 `test_collision.py:131,277,445` · `test_handoff.py:141` · `test_handoff_worktrees.py:446,451` · `test_p1_layer_h.py:734`, 均不覆盖 `tracks_multibranch` 行) ⇒ 新增 `rel_path` / `unreadable_count` 不打红既有键集断言; `test_collision.py:445` 钉的是 `collision` 三键, 顶层新增字段结构上触不到它。
- [minor] architecture/「恒存在」不变量覆盖完全: `collect_handoff_multibranch` (`:556-755`) 恰两个 `return r` —— `:596` fail-soft 早退与 `:755` 正常返回, 无第三条路径 ⇒ Task 2.3 + Task 2.4 两处即穷尽, §4 的「恒存在」在错误路径上可满足。
- [minor] implementation/返回形状变更零外部影响属实: `writers/__init__.py:12,14` 只再导出 `write_latest_md`; 全树唯一 import 是 `test_p1_layer_h.py:51`, **无任何测试直调** `_render_pointer` / `_render_pointer_unavailable` (`grep -rn '_render_pointer' skills/ --include=*.py`) ⇒ §2.5 / Task 2.5(e2) 的 `tuple[str, str | None]` 改法可行。
- [minor] implementation/前缀守卫确为「理论上不会出现」+ `-z` 尾随空段属实 (本席 hermetic 实跑): 在含 `docs/handoff/a.md` / `docs/handoff/archive/b.md` / `docs/handoff-archive/c.md` / `docs/handoff.md` 的临时仓上, `git ls-tree -r --name-only HEAD -- docs/handoff` **只**输出前两条 (pathspec 在目录边界匹配, 不会误吞 `docs/handoff-archive/`); `-z` 输出经 `od -c` 确认为 NUL **结尾** ⇒ `split("\0")` 必产生尾随空段, SC-9(c) 的要求成立且必要。
- [minor] documentation/R4 处置逐条落在正文而非批注 (11 条缺陷类全查): `5c28d58f`→§3+Task 2.2(c)+Task 4.3+SC-10 · `5513534d`→§3+§5 表 · `ead9ac24`→§2.5 表行+Task 2.5(e2)+SC-15 (i)(j)+第 4 条反事实 · `5105b00e`→§2.5 裁定依据重写 · `7ae33f13`→SC-13(c)+SC-16 夹具组成 · `177d72e6`→§Why F2 条件式+SC-3 配置隔离 · `31bc3c6a`→§7+Task 4.3 · `b3e5ea8d`→Task 2.0a · `ab615189`→头部 Rule #6 行+rule6_note 首条 · `5b252465`→§6.2+Task 2.5(g)+SC-11(k) · `23b414c9`→§5 新行+Impact.Risk+Task 5.3(d)。minor `0328fdb3` 亦以 SC-11(l) 落地。
- [minor] testing/SC-11(l) 三条新 grep 均 baseline-failing (本席实测): `degraded_reason` 在 `writers/latest_md_writer.py` 与 `references/phase-1-collectors.md` 上基线 `grep -c` 均为 **0**; `子目录\|subdir` 在 `references/layer-l-integration.md` 上基线 `grep -c` = **0** ⇒ 三条都有鉴别力, 不是恒绿代理判据。
- [minor] architecture/R4 两条载重更正复核为真: (a) 排除 `tests/` 后全树 `["action"]` / `.get("action")` **零命中**, 与「`write_latest_md` 零生产调用点」互证 (`writers/__init__.py` + `test_p1_layer_h.py` 之外无引用); (b) `tests/fixtures/freeze_corpus.py:29,32-37,48-53` 确实把每行投影成恰好八个 FIELDS 并回写 `"fields"` ⇒ 重生成会红的是 `test_collision_frozen_corpus.py:111` 的 `assertEqual(len(self.rows), 996)` 而非 `:51`/`:112`, §7 / Task 4.3 的更正正确。
- [minor] architecture/待复议 7 的第二条判据核实成立: `spec-drafter/LEVEL_GUIDE.md:156-162`「跨模块条件 (满足任一)」四条实读为「涉及 2 个及以上模块 / 修改 shared/ 目录 / **需要 API 契约变更** / 影响多个子模块」⇒ 即便 Task 4.4 判 deferred, 第三条仍独立命中 (本 spec 新增三个机读契约字段 + 改两个私有函数返回形状 + 改 `_render_pointer_unavailable` 签名)。**本席不代裁 Level, 交 owner (Rule #10)**。
- [minor] documentation/Rule #6 反证 1 复核成立 (本席实测): `aria-plugin-benchmarks/ab-suite/state-scanner.json` 现为 **17551 B**, `tracks_multibranch` 命中 **1** (`:214`), `handoff_multibranch` / `legacy` / `basename` 三词均 **0** —— 与 rule6_note 逐字一致。
- [minor] architecture/`legacy:<branch>:<rel_path>` 引入 `/` 无下游破坏: 全树 `legacy:` 字面只在 `handoff_multibranch.py:36`/`:332`/`:494` 三处 docstring 与 `:336` 构造点出现, **无任何反解析方**; `phase1_gate` 的 claim track_id 走 `lib/track_id.derive_track_id` 独立派生并按字符串相等过滤, 不参与 ref/路径构造; 姊妹 `handoff_worktrees.py:230` 的 legacy id 是裸 `latest.name`, 本就不用该公式 ⇒ 无跨 collector 格式耦合。

### Issues

- [major] architecture/§4 `unreadable_count` 三类外延定义第 3 类 / §7 末条 / Impact.Risk 末条 / Task 2.3: 「不可解码 UTF-8 名 ⇒ 显式跳过, 不计入 `unreadable_count`」这一 R4 `dd55dac3` 刚收敛的择一**在本 collector 上不可实现, 且实际结果与之相反**。所援引的先例 `handoff.py:317-322` (`try: entry.name.encode("utf-8") / except UnicodeError: continue`) 之所以有效, 是因为那里的名来自 `os.scandir` 的 **surrogateescape** 字符串; 而本 collector 的名来自 `_run`, 其解码是 `encoding="utf-8", errors="replace"` (`scripts/collectors/_common.py:411-412`) ⇒ 坏字节变 **U+FFFD**, 而 `"�".encode("utf-8")` **不抛**, 守卫恒不触发。本席 hermetic 实跑 (临时仓内建名含 0xff 的 `docs/handoff/2026-\xff-bad.md`): `git ls-tree -r --name-only -z` 经同款解码得 `'docs/handoff/2026-�-bad.md'` → `.encode("utf-8")` **OK** (跳过不发生) → 过 `.endswith(".md")` → `git show HEAD:<该路径>` **rc=128** `fatal: path ... does not exist` ⇒ 落进 §4 第 1 类 ⇒ **被计入 `unreadable_count`**。同一脚本内 `os.scandir` 对同一文件得 `'2026-\udcff-bad.md'` 并抛 `UnicodeEncodeError` (先例在 `handoff.py` 侧确实有效) —— 两条数据通路的字符串生成机制不同, 先例不可移植。后果正是 §4 自己警示要避免的那条:「计进 `unreadable_count` 会让一个恒不可修复的量永久非零」。且 SC 集**无一条覆盖第 3 类** (SC-5 只造 git show 失败, SC-3 只造可解码中文名), 故该错误不会被任何验收判据抓到。⇒ 修法二选一, 须在正文择定: (i) 改判据为「`rel` 含 U+FFFD (或 `rel.encode("utf-8", "surrogateescape")` 回写后与 tree 原字节不等) 即跳过」并补一条 SC; (ii) 承认本 collector 结构上分辨不出, 把第 3 类改写为「不可解码名与 git show 失败合流、计入 `unreadable_count`」并同步 §7 / Impact.Risk / CHANGELOG 的边界措辞。**不得**保留现文 —— 它对一个新机读契约字段的外延给了一条实现不出来的规定 (证据: `_common.py:411-412`; proposal.md §4「⚠️ `unreadable_count` 的外延必须就地定义」第 3 条; §7 末条; Impact.Risk 末条)。
- [minor] architecture/§What.1 前缀守卫行 / Task 2.1 推荐实现路径 (i) / SC-9: 新 kind `handoff_multibranch_unexpected_path_prefix` 按处方「主循环传 `r.soft_error`」注入后, 只会进 `CollectorResult.errors`, **不进** `data["errors"]` (= 快照 `tracks_multibranch.errors[]`, schema `references/state-snapshot-schema.md:1101` 逐字「accumulated non-fatal error messages」)。而本 collector 现有四个 kind **全部**双通道成对: `:587` + 早退 dict `:594` · `:607`+`:608` · `:622`+`:623` · `:641`+`:642`+`:643`。SC-9 只断 soft_error 通道, 而 SC-14 对 `handoff_multibranch_branch_list_failed` 恰好**两个通道各断一次** —— 同一份 SC 集对新旧 kind 用了不同强度的判据。⇒ Task 2.1 明写 reporter 是否同时回填 `error_messages` (推荐: 传一个同时写两处的闭包), SC-9 补一条 `data["errors"]` 断言; 或显式写明「本 kind 有意只进 soft_error 通道」并在 schema 登记该例外。
- [minor] documentation/§2.5 `degraded_reason` 传播路径块 / Task 2.5(e2): 「`_render_pointer` …… 其**唯一**调用点是 `:302`」为 off-by-one —— `scripts/writers/latest_md_writer.py:302` 是 `elif n_active == 1:`, 真实调用在 `:303` (`content = _render_pointer(active_tracks[0], now)`)。与 R4 五席全席命中的 `7b7aed03` (dedupe 论据句 `:495-496` 实为 `:494`) 同型: SC 走 grep 不致假绿, 但 Task 2.5(e2) 会把实施者指到错行。
- [minor] documentation/Task 4.4 (standards 同步清单) / §5 消费方枚举: 本 spec 使 `docs/handoff/**` 成为 multibranch collector 的一等输入域 (方案 B/C 被显式否决), 但共享子模块 SOT `standards/conventions/session-handoff.md` 自始至终**只描述扁平布局** —— `:15`「Session handoff documents MUST be written to `docs/handoff/` (canonical)」· `:88`/`:94` 路径模板 `docs/handoff/{YYYY-MM-DD}-…` · `:336`「输出路径硬编码 …… **不接受 dir 参数**」· `:301`「`exists: bool # docs/handoff/*.md has files?`」(单星 glob)。Task 4.4 在同一文件内只改 `:97` 与 `:171-173` 两处 latest.md 派生行为, 未就子目录布局的规范地位表态。后果: Task 5.3 的遗留 issue (姊妹 collector `handoff.py` 是否也该递归) 缺规范锚点 —— 到底该让 `handoff.py` 变递归, 还是该判定子目录不受约定支持, 是同一份 SOT 该回答而现在没答的问题。这些句子今天**未被证伪** (归档件仍在 `docs/handoff/` 之下), 故列为 risk 而非事实错误; 但既然本 cycle 已为 Task 4.4 付出 standards 子模块链路成本, 顺带在同节加一句子目录布局的规范表态 (或明写「本 spec 不表态, 交 Task 5.3 的 issue」) 的边际成本接近零。

### Risks

- (无独立于上述条目之外的新增风险条目; §5 / Impact.Risk 现有七条风险经本席逐条对真代码复核, 机制陈述与行号均成立 —— 含 `n_active` 三分派 `latest_md_writer.py:298-310`、`_render_banner` `:172-224` 不含 `**Latest**: [` 行、`handoff.py:263-266` `_LATEST_POINTER_RE` 要求 `^\*\*Latest\*\*:\s*\[`、`handoff.py:288` `Path(target).name`、`:300/:318` 非递归 `iterdir()`、`:389` 按 `p.name` 建索引、`:397-404` 与 `:438-451` 早返回。)

---

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **1** / Minor **3** (decisions 11 条不计入)。

rationale: 本轮未发现方案性错误、未发现会破坏既有消费方的字段变更、未发现恒绿导致假绿的 SC。R4 的 1 critical + 10 major 经逐条对正文核验**全部落在正文而非批注**, 且新引入的论证 (freeze_corpus 八字段投影 / `action` 零消费方 / `core.quotePath` 条件式 / SC-11(l) 三条 grep) 本席独立实跑复核**均成立**。唯一 major 是本轮新面: §4 刚收敛的「不可解码 UTF-8 名显式跳过」这一新机读契约外延, 其所依赖的机制在本 collector 的数据通路上恒不触发, 实际行为与规定相反, 且无 SC 覆盖 —— 属「设计缺口 + 事实错误」, 按定级表落 major, 不达 critical (影响面窄、不破坏现有消费方、不制造既有 SC 的假绿)。三条 minor 均为定点修文, 零风险。

按投票规则 (critical + major 均为 0 才 PASS): 本席 **vote = REVISE**。

---

## 轮次记录

### Round 5: Agents

- 本席: backend-architect (五席之一, 新席位, 不继承上轮结论)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- 审计对象冻结: 本轮**只审不改**, 未编辑 proposal 或任何仓库文件; 全部核验产物落 scratchpad 临时仓 (`/tmp/claude-1000/-home-dev-Aria/…/scratchpad/ba5-*`, `ba5b-*`), 未触碰 `/home/dev/Aria` 工作区
- Conclusions 数: 15 (Decisions 11 / Issues 4 / Risks 0)
- Vote: **REVISE** (Critical 0 / Major 1 / Minor 3)

### 本轮机械核验清单 (逐条实读 / 实跑, 供 R5 汇总席复算)

1. 行号基线: `handoff_multibranch.py` 755 行 · `handoff.py` 511 · `latest_md_writer.py` 320 · `scan.py` 492 · `track_board.py` 842 · `state-snapshot-schema.md` 1168 · `test_handoff_multibranch_collision_dedupe.py` 1177。
2. collector docstring 两块归位属实: 顶层返回键表 `:16-31` (含 `:20` legacy_count 注释) / TrackEntry 块 `:35-44` (`:36` legacy 公式 · `:40` committer-date 误述 · `:42` basename 注释)。
3. `_list_handoff_files` `:240` / docstring `:243`,`:246-247` / `:257` pathspec / `:275-276` 空行早退 / `:277` basename / `:278` `.md` 过滤 / `:280` pointer 排除 —— 逐行确认。
4. `_read_file_content` `:293`/`:301` · `_get_file_commit_date` `:310`/`:313` docstring 写 committer 而 `:316`/`:322` 实为 `%aI` author date · `_make_legacy_track_id` `:329`/`:332`/`:336`。
5. 主循环三个 TrackEntry 构造点: git-show 失败 `:646-656` (§4 删除) / frontmatter `:665-676` / 无 frontmatter legacy `:687-698` —— §4 后剩两处, 与 SC-13(c)/SC-16 的夹具要求一致。
6. `legacy:<branch>:<filename>` 字面在 collector 内**恰 3 次** = `:36` / `:332` / `:494` (+ `schema:1104`) ⇒ R4 minor `7b7aed03` 的勘正正确。
7. `scan.py` AC-5: `:126` 定义 / `:166-173` 四道前置 / `:180-182` filename 早退 / `:186` 拼串 / `:193`,`:209` 上报 / `:269`,`:283` 进 `errors[].tracks` / `:255` 调用 / `:388` 传 `phase1_17_handoff_mb.data` (⇒ §3 的「缺 `rel_path` 生产不可达」成立)。
8. `HEALTHY_TRACKS` (`test_scan_integration.py:164-166`) 确为三键无 `rel_path`; `_mock_run` (`:172-176`) 对路径无鉴别力; `:270`/`:272`/`:317` 三条断言存在 ⇒ R4 critical `5c28d58f` 与其修法 (补 `"rel_path": "2026-07-19-x.md"`) 成立。
9. `_active_track` (`test_p1_layer_h.py:230-240`) 确为八字段无 `rel_path`。
10. writer: `_get_active_tracks` `:72` (active 过滤 `:89-95`, docstring `:78-81`) · `_render_pointer` `:110` (docstring `:111-114` / `:113` 单行锚 / `:124` 内部降级调用 / `:143` 真指针行) · `_render_pointer_unavailable` `:151` (`:152` docstring / `:159` v1.22.x 句 / `:162` 降级行 / `:164` 硬编码原因) · `_render_banner` `:172` · `write_latest_md` `:259` (`:279` 返回键 / `:287-290` Scenarios / `:296` n_active / `:298`,`:302`,`:306` 三分派 / **`:303` 才是 `_render_pointer` 调用点**) · 模块 docstring `:32` action 枚举。
11. `_render_banner` 全函数复读: 输出**不含** `**Latest**: [` 行 ⇒ R4 `23b414c9` 的静默 mtime 退回链成立。
12. `handoff.py`: `_LATEST_POINTER_RE` `:263-266` · `_parse_latest_pointer` `:269`/`:288` · `_scan_md_files` `:300`/`:318`/`:319-322` UnicodeError 跳过 · `:389` by_name · `:399` kind · `:438-451` 早返回 · `:455` `_resolve_latest`。
13. `_common.py`: `soft_error` `:312-313` 产 `{"error": kind, "detail": …}` · `_noninteractive_git_env` `:317-346` 只注 `LC_ALL`/`GIT_TERMINAL_PROMPT`/`GIT_SSH_COMMAND` (继承宿主 git 配置, F2 条件式成立) · `_run` `:411-412` `encoding="utf-8", errors="replace"`。
14. hermetic 实跑 A (pathspec 边界 + `-z` 形态): 见 Decisions 第 6 条。
15. hermetic 实跑 B (不可解码名全链): `ls-tree -z` → 解码 `'docs/handoff/2026-�-bad.md'` → `.encode("utf-8")` OK → `git show` rc=128 → 会计入 `unreadable_count`; 对照 `os.scandir` 得 `'2026-\udcff-bad.md'` 抛 `UnicodeEncodeError` ⇒ major 条目的证据链。
16. `standards/` 侧: `git rev-parse HEAD` = `origin/master` = **`21748d4`** (与 proposal 头部写死起点一致); `session-handoff.md:15`/`:88`/`:94`/`:97`/`:171-173`/`:301`/`:336` 逐行实读。
17. `validate_schema_doc.py` 经实读为 **TOP-LEVEL KEY GRANULARITY only** (模块 docstring 明写「nested field completeness is NOT checked」) ⇒ 新增嵌套字段不触发该机械闸, 本 spec 无须登记它 —— 记录在此以免 R5 其他席位重开。
