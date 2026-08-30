---
checkpoint: post_spec
round: 6
role: knowledge-manager
verdict: PASS
scope_ok: true
counts: 0C/3M/2m
---

# post_spec R6 — a1-entry 三份 Spec + 决策单 事实断言逐条核验 (knowledge-manager)

## (a) 本席镜头

只做一件事: 对三份 Spec 与决策单里**标 `2026-08-30` / `rework v4` / `round-3` / `2026-08-30 实读` 的新写文本**, 逐条抽取可证伪的事实断言, 回源头 (主仓文件 / aria 子模块 `d50f9c3`+`007d355` 两个 SHA / AB 套件 JSON / 生产协调 ref) 实读核验「内容是否属实」——不是 R5 factcheck 席已经做过的「行号是否存在」。方法: 只用 `git show <SHA>:<path> | awk 'NR==N'` / `sed -n` 定位到具体行后**再**判断, grep 只用来找候选范围, 不据此下结论。

## (b) Findings (按严重度)

**本轮 0 条 Critical。** 在约 65 条逐条核验的断言里, 3 条 Major、2 条 minor, 其余全部逐字/逐值核验为真。

---

### 决策单 M1 (Major) — 反驳 1 引用的 grep 数字, 今天用同一条命令复算不出「15」

- **位置**: `.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md:23`
- **逐字引文**: 「这条规则是从**本仓存量语料反推**出来的 —— `grep -rl '**关联 Issue**' openspec --include=proposal.md` 得 15 份 (14 份在 archive/), 全部用这个中文字段名。」
- **源头实读**:
  ```
  $ grep -rl '\*\*关联 Issue\*\*' openspec --include=proposal.md | wc -l
  17
  $ grep -rl '\*\*关联 Issue\*\*' openspec --include=proposal.md
  (14 份 archive/ ... + 3 份 changes/: a1-entry-claim-duplicate-work-guard / linked-issue-field-availability / sibling-spec-probe)
  ```
  逐字跑决策单给出的那条命令, 今天输出 **17**, 不是 **15**。`14 份 archive/` 这部分核实无误 (今天仍是 14, 不受本轮变动影响); 差额出在 `changes/` 侧 —— 决策单写「1 在 changes/」, 今天是 **3**(母 Spec / 字段 Spec 自身 / 探针 Spec 各因讨论该字段而含至少一行形状匹配的散文, 而非它们自己的头部字段; 三份的头部字段今天**均已是英文** `Linked Issue`, 已用 `git show`/直读逐份核对)。
  另跑任务里指定的严格锚定版本 (`grep -rlE '^> \*\*关联 Issue\*\*:' --include=proposal.md openspec/`): 今天 = **15** (14 archive + 1 changes —— `linked-issue-field-availability/proposal.md`, 但那 1 条是该文件 §3 自己用于讲解正则的**围栏内示例行**, 不是它自己的头部字段, 该文件自己的头部字段在 `:6` 已是 `Linked Issue`)。这个「15」与决策单的「15」**数值巧合但成因不同**: 决策单用的是**宽松**命令, 今天宽松命令给的是 17。
- **正确值**: 宽松命令今天 = 17 (14 archive + 3 changes, 且 changes 侧那 3 条**没有一条**是"这份 Spec 自己在用中文字段名"意义上的真阳性, 三份头部字段均已是英文)。
- **为什么不改变结论**: 反驳 1 的论点「样本决定不了分发面」不依赖 14 还是 16/17 这个具体数字, 结论本身站得住; 但决策单把「14 archive」和「变动中的 changes 语料」混进同一个数字里当"当日快照"呈给 owner, 而三份 Spec 自己在别处 (母 Spec §瓶颈段) 已经写过「数字是当日观测, 不是规范, 语料会随每次新建/编辑 Spec 变」这条免责声明, 决策单这处没有照它自己定的规矩说清楚。
- **建议处置** (只建议不落版): 决策单该处补一句「以上为决策落笔时点的观测值, `changes/` 语料随三份 Spec 自身编辑持续变动, 复核以当场命令为准」, 或者干脆把宽松命令的引用换成「14 份 archive (稳定)」这个不随三份在制 Spec 变化的子集。

---

### 决策单 M2 (Major) — 「修复」段的测试计数与今天用同一方法实测的结果不符

- **位置**: `.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md:58`
- **逐字引文**: 「测试 `tests/test_coordination_no_push.py` 16 条 (TDD: 实现前全红; 负控 `test_c_negative_control_no_flag_no_env_attempts_push` 用硬编码 `push_skipped=True` 亲验会红后还原); state-scanner 套件 **1393 → 1409** 全绿。」
- **源头实读** (对 `skills/state-scanner/tests/` 下全部 `.py` 文件, 逐文件 `git show <SHA>:<file> | grep -cE '^\s*(async )?def test_'` 后求和; 两种缩进模式结果一致):
  ```
  d50f9c3 (决策单称之为「基于」的那个基线) 合计 test_ 定义数 = 1409
  007d355 (本修复分支) 合计 test_ 定义数 = 1425
  差值 = 16   (与「新增 16 条」吻合)
  ```
  `test_coordination_no_push.py` 在 `d50f9c3` 上 `git ls-tree` 确认**不存在** (只在 `007d355` 新增, 与 `git diff --stat d50f9c3 007d355` 的 4-文件变更列表一致), 其内 `def test_` 计数逐条数出**恰 16 条**, 且 `test_c_negative_control_no_flag_no_env_attempts_push` 这个测试名**确实存在** (`:206`) —— 这两处决策单原文准确。但「1393 → 1409」这对绝对基数, 用决策单自己指名的基线 `d50f9c3` 复算不出来: 实测是 **1409 → 1425**, 两端都比决策单写的数字多 16。
- **正确值**: 1409 → 1425。
- **为什么不改变结论**: 「新增 16 条、且都是本修复引入」这个结论仍成立 (16 这个 delta 两种算法都对得上); 但「1393」这个基线数字对不上 `d50f9c3`, 疑似是更早某个时间点 (或不同统计口径) 的残留数字被原样搬进了这次决策记录, 而 `d50f9c3` 与 `1393` 之间的 16 条差异从未被交代来源, 恰好与本次新增的 16 条数值相同, 容易让人误以为「本次修复 = 从 1393 到 1409 这唯一一次变化」, 实际上基线本身已经往前走了一轮。
- **建议处置**: 把两个绝对数改成 `1409 → 1425`; 如果坚持保留 `1393` 这个历史数字, 需要注明它对应哪个更早的 commit, 且与 `d50f9c3` 之间那 16 条差异的来源需要交代, 否则读者会把两次不相关的 +16 看成同一次。

---

### 母 M1 (Major) — R5 已自证的一处「逐字」引文误标, 本轮未清账, 原样留存

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` §2.2 「⛔ 遥测分区边界」段 (R3/TL-M2 标注, 未在 rework v4 改动)
- **逐字引文**: 「实读 `skills/state-scanner/scripts/coordination_probe.py:4-25`: 它是**反死代码探针**, 只数 `.aria/coordination-telemetry.jsonl` 里 `_source=="production"` 的**近期** `run_gate` 记录, 而该分区「written only by the CLI production path (`_main` → `_gated` with `_source="production"`)」**(逐字)**。」
- **源头实读**:
  ```
  $ git -C aria show d50f9c3:skills/state-scanner/scripts/coordination_probe.py | sed -n '4,25p'
  ```
  全文只有语义相近的改写句 ("The production partition file is written only when ``_source=="production"``, and ... that value is reachable ONLY from the private ``phase1_gate._gated`` ... by exactly one call site, the CLI ``_main``"), **不含**「written only by the CLI production path (`_main` → `_gated` with `_source="production"`)」这句的字面。真身在:
  ```
  $ git -C aria show d50f9c3:skills/state-scanner/scripts/phase1_gate.py | sed -n '1044,1051p'
  1047:    written only by the CLI production path (:func:`_main` → :func:`_gated`
  1048:    with ``_source="production"``), so no public/library/test caller can inflate
  ```
  逐字比对, `phase1_gate.py:1047-1049` 才是这句话真正的出处。
- **这不是我这次独立发现的新问题** —— 上一轮 `.aria/audit-reports/post_spec-R5-1787840920000-a1-entry-combined-aggregated.md:238` 附近「主控本轮的两条自证」原文已写: 「**第二次误标「逐字」**: `:238` 把一段引文归给 `coordination_probe.py:4-25`, 实读该文件**零命中** —— 真身在 `phase1_gate.py:1048`」。也就是说 R5 已经把这条错误明确点名过, 但 rework v4 落版时**没有把它一并改掉**, 现在还是原来那句错误引文, 一字未动。
- **正确值**: 出处应为 `phase1_gate.py:1047-1049`, 而不是 `coordination_probe.py:4-25`。
- **为什么不改变结论**: 该段要论证的机制性结论 (「heartbeat 不能复用 production 遥测分区, 否则会把一个 enabled 的 check 变成恒绿」) 不依赖这句引文具体出自哪个文件, 结论仍然成立。
- **建议处置**: 把文件:行号从 `coordination_probe.py:4-25` 改成 `phase1_gate.py:1047-1049`(「(逐字)」标签保留, 换了地方之后确实是逐字); 母 Spec Status 行写的「R5 五项落版实测…本轮逐项清账」清单里没有这一项, 建议在下一次落版把它一并收进清账范围, 避免同一条错误被第三轮抓到。

---

### 母 m1 (minor) — 「本轮未做/存疑」表行号越界一行

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` 「本轮未做 / 存疑 (给 R6)」表 #2
- **逐字引文**: 「本轮实读 A.1 YAML 项在 `:62-73` (`skip_if: complexity: Level1` 在 `:66`), 但委派 `spec-drafter` 的具体动作行未钉」
- **源头实读**:
  ```
  $ git -C aria show d50f9c3:skills/phase-a-planner/SKILL.md | awk 'NR==66||NR==67'
  66:    - has_openspec: true          # 已有活跃 Spec
  67:    - complexity: Level1          # 简单任务
  ```
- **正确值**: `complexity: Level1` 在 `:67`, 不是 `:66`(`:66` 是紧邻的上一行 `has_openspec: true`)。区间本身 `:62-73` 无误 (`:62` 起`` ```yaml``, `:73` 止 `spec_status: "approved"`)。
- **为什么是 minor**: 这条只是给 A.2 实施者指路的备注, 不是任何 SC 的机械断言依据, 差一行不影响任何结论。
- **建议处置**: 改成 `:67`。

---

### 母 m2 (minor, 供 owner 参考) — dogfood 头部字段「none」与生产协调 ref 里的真实 claim 记录不一致, 未加说明

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:13` (「**Linked Issue**: `none`」, FIX-19 dogfood 落点) 对照生产 `refs/aria/coordination`
- **源头实读**:
  ```
  $ git show refs/aria/coordination:claims/023236f2/s-26ad@0914.yaml
  linked_issue: 10CG/Aria#174
  track_id: a1-entry-claim-duplicate-work-guard
  status: active
  ```
  同一 track_id 在 `refs/aria/coordination` 上的两条真实历史 claim (`s-26ad@0914`、`s-6389@0120`, 分别 2026-08-23 / 2026-08-25 认领) 都带 `linked_issue: 10CG/Aria#174`, 而母 Spec 自己头部却写「Linked Issue: `none`」。
- **是否矛盾**: 不必然。`10CG/Aria#174` 更像是决策单头部所说的「立项 issue」/ 跨三份 Spec 协调用的公共锚点, 与「本 Spec 是否由某条外部 bug report 触发」(头部字段真正问的问题) 是两件事; 但三份 Spec 与决策单全文**没有一处**把这层区别写清楚, dogfood 示范 (FIX-19) 反而给人「本 Spec 亲身示范填 `none`」的印象, 与它自己在生产环境实际认领时传的实参不同。
- **建议处置**: 在母 Spec 头部或决策单里补一句, 说明「Linked Issue: none」与实际 acquire 时传 `--linked-issue 10CG/Aria#174` 的关系(前者答"是否有外部触发 issue", 后者答"跨 Spec 协调用哪个锚点"), 否则容易被读成 dogfood 示范和真实操作对不上。

---

## (c) 断言核验表 (逐条, ≥30 条; 判定: 一致 / 不一致 / 无法核)

| # | 出处 | 断言 | 源头 | 判定 |
|---|------|------|------|------|
| 1 | 决策单反驳 1 | `grep -rl '**关联 Issue**' openspec --include=proposal.md` 得 15 份 (14 archive) | 主仓 grep 实跑 | 不一致 (今天=17; 见决策单 M1) |
| 2 | 决策单反驳 2 | SOT 模板其余三行 (`Level`/`Status`/`Created`) 全英文 | `standards/openspec/templates/proposal-minimal.md:3-5` | 一致 |
| 3 | 决策单反驳 3 | CLAUDE.md 工作语言段逐字「中文叙述为主。保留英文技术 token: 代码 / 命令 / 路径 / … / spec 术语」 | `/home/dev/Aria/CLAUDE.md:16` | 一致 (逐字, 省略号处确系 SHA/branch/PR#/版本号) |
| 4 | 决策单反驳 4 | `ab-suite/spec-drafter.json` eval 2「双语输入处理」明确要求生成英文 proposal | 该文件 `evals[1]`: name=`bilingual-support`, prompt 含「请生成英文 proposal」 | 一致 (逐字) |
| 5 | 母 Impact 表「AB 套件」行 | `ls aria-plugin-benchmarks/ab-suite/` 六套件均实存 | 目录列出 phase-a-planner/spec-drafter/phase-b-developer/branch-manager/phase-d-closer/state-scanner 六个 `.json` | 一致 |
| 6 | 母 rule6_note #1 | `ab-suite/phase-a-planner.json` evals=2 | python 读 JSON `len(evals)` | 一致 |
| 7 | 母 rule6_note #2 | `ab-suite/spec-drafter.json` evals=2 | 同上 | 一致 |
| 8 | 母 rule6_note #5 | `ab-suite/state-scanner.json` evals=12 | 同上 | 一致 |
| 9 | 母 rule6_note | 「实数 11 hunk / 9 文件」 | 自数 rule6_note 表 (11 行, 去重后 9 个文件路径) | 一致 (自洽; 与 Impact 表对应 9 行一一对上) |
| 10 | 母 §2.2 | `phase1_gate.py:56` 只有 `logger = logging.getLogger(__name__)`, 无 handler | `git show d50f9c3:...phase1_gate.py \| awk NR==56` | 一致 |
| 11 | 母 SC-10 | `phase1_gate.py:210` docstring 预留 `fetch_degraded` token | 同上 `NR==210` | 一致 |
| 12 | 母 §2.2 | `phase1_gate.py:1191` 的 `--phase` 是 `required=True` | 同上 `NR==1191` | 一致 |
| 13 | 母 §2.4a | `phase1_gate.py:1230` 是 `if args.linked_issue:` 整块门控 | 同上 `NR==1230` | 一致 |
| 14 | 母 D14/Impact | `phase1_gate.py:1233-1235` 是 `linked_issue_overlaps(...)` 调用 | 同上 `NR=1233..1235` | 一致 |
| 15 | 母 R2/M-4 | `phase1_gate.py:1236-1238` 的 `except` 写 `out["linked_issue_overlap"] = []` | 同上 `NR=1236..1238` | 一致 |
| 16 | 母 §2.4 传递链 item 2 | `linked_issue_overlaps` 只在 `_main()`(`:1173`) 内被调用一次, `_run_gate_impl`(`:335`) 零命中 | `grep -n "linked_issue_overlaps("` 全文件恰 1 处, 位于 `:1233`, 在 `_main` 内 | 一致 |
| 17 | 母决策单引用 | `phase1_gate.py` 第 9 步 `resilient_push`(`:791-802`) 无条件推 `refs/aria/coordination` | 同上 `NR=785..805`, 紧邻注释「Step 9: resilient_push」 | 一致 |
| 18 | 决策单第 4 项处置 | 推送点不是 `write_claim` 的 `auto_bootstrap`, 是 `bootstrap(..., push=False)`(`coordination_ref.py:800`) | `git show d50f9c3:...coordination_ref.py \| awk NR==800` → `boot = bootstrap(repo_path=repo, push=False)` | 一致 |
| 19 | 决策单残留段 | fetch refspec 非强制 (`coordination_ref.py:1367`) | 同上 `NR==1367` → `refspec = f"{REF_NAME}:{REF_NAME}"`, 无前导 `+` | 一致 |
| 20 | 母 D3/D4 | `collision.py:178` 是 `normalize_linked_issue(` 定义 | `git show d50f9c3:...collision.py \| awk NR==178` | 一致 |
| 21 | 母 §2.4 | `collision.py:219` 是 `_linked_issue_matches(` 定义 | 同上 `NR==219` | 一致 |
| 22 | 母 §2.4 传递链 item 0 | `linked_issue_overlaps` 现三参数签名 `:230-234` | 同上 `NR=230..234` | 一致 |
| 23 | 母 §2 NEW-01 | `collision.py:265-266` 是 `if not own_linked_issue: return []` | 同上 `NR=265..266` | 一致 |
| 24 | 母 §2.4 | `collision.py:268` 是 `_TERMINAL = ("done", "abandoned", "unknown")` | 同上 `NR==268` | 一致 |
| 25 | 母 §2.1「为什么必须含容器段」 | `collision.py:278-279` 是 `if c.track_id == own_track_id: continue` | 同上 `NR=278..279` | 一致 |
| 26 | 母 Impact `phase-b-developer` 行 | `:96-97` 是关于 `write_claim auto_bootstrap` 推送的注释, `:98` 是 `coordination.enabled` skip 项 | `git show d50f9c3:...phase-b-developer/SKILL.md \| awk NR=96..98` | 一致 (逐字) |
| 27 | 母 R5/M2 | `branch-manager/SKILL.md:146` 标题写 `Part A1` 但块内命令是 `--phase B` | 同上 `NR=146..150` | 一致 (证实既有缺陷真实存在) |
| 28 | 母「非目标」 | `phase-d-closer/SKILL.md:56` 把 `SWEEP_TTL` 行为误写成「超 STALE_TTL」 | `git show d50f9c3:...phase-d-closer/SKILL.md \| awk NR==56` | 一致 (证实既有措辞缺陷真实存在) |
| 29 | 母 §5.1 | `claim_lifecycle.py:396-399` docstring 逐字「If several active claims match (same container re-claimed a track across sessions — the NORMAL case, since every session mints a fresh session_id and B.0 REQUIRE-claim runs per session), ALL matching active claims are released」 | 同上 `NR=396..399` | 一致 (逐字) |
| 30 | 母 §5.3 | `claim_lifecycle.py:244-256` 逐字段重建**恰 11 个字段** | 同上 `NR=244..256`, 数得 11 个具名字段 (schema_version…linked_issue) | 一致 |
| 31 | 母 §2.1 表 / FIX-18 | `identity.py:222`=label 优先, `:242`=`return _hostname()`, `:244`=`return uuid` | `git show d50f9c3:...identity.py \| awk NR=222,242,244` | 一致 |
| 32 | 母 D3 | `constants.py:43-44` 自陈「NO production heartbeat loop exists (heartbeat() has zero production call sites; phase1_gate self-resume does not refresh either)」 | 同上 `NR=43..44` | 一致 (逐字) |
| 33 | 母 §2.1 | `track_id.py:61` 定义 `derive_track_id`, `:70-76` 四步 (lower/`./_`→`-`/截断 64/非 ASCII sha256) | `git show d50f9c3:...track_id.py \| awk NR=61,70..76` | 一致 |
| 34 | 母 §2.3 | `release_gate.py:225` help 逐字含「active 且 heartbeat 超 STALE_TTL → abandoned (跨 container)」 | `git show d50f9c3:...release_gate.py \| awk NR==225` | 一致 |
| 35 | 母 §5.2 | `release_gate.py:236-237` 是「三选一必需」的 `parser.error` | 同上 `NR=236..237` | 一致 (与母 Spec 文中贴出的代码块逐字相同) |
| 36 | 母 rule6_note ⛔ 段 | AB 评测跑在真仓/真 origin/无沙箱, `ab-workspace/` 有真实历史产物 | `AB_TEST_OPERATIONS.md` 自陈「subagent 无 sandbox」+ `ls aria-plugin-benchmarks/ab-workspace/` 存在真实运行产物目录 | 一致 |
| 37 | 决策单第 4 项处置 | `AB_TEST_OPERATIONS.md:222-228` 新增「运行前置: 协调 ref 推送隔离」小节 | 主仓文件同区间逐字比对 | 一致 |
| 38 | 决策单第 4 项处置 | 生产 `refs/aria/coordination` 里有一条 2026-08-02 的合成 `audit-test` claim | `git show refs/aria/coordination:archive/2026-08/023236f2/s-f963@1218-2026-08-02T12-18-21Z.yaml` → `track_id: postspec-r1-delete-me-a1-entry-claim-audit-test`, `linked_issue: AUDIT-TEST-DO-NOT-USE#0` | 一致 |
| 39 | 决策单「修复」段 | aria 分支 `fix/phase1-gate-no-push`@`007d355` 基于 `d50f9c3`, 只改 4 个文件 | `git -C aria diff --stat d50f9c3 007d355` → 恰 4 个文件 | 一致 |
| 40 | 决策单「修复」段 | `--no-push` flag + `ARIA_COORDINATION_NO_PUSH` env (`1/true/yes`, 大小写不敏感) | `git show 007d355:...phase1_gate.py` grep 命中, `:1296` 逐字「1|true|yes (大小写不敏感)」 | 一致 |
| 41 | 决策单「修复」段 | JSON additive 键 `push_skipped`/`push_skipped_reason` (`cli_flag`\|`env_var`\|`null`) | 同上多处命中, 三值枚举确认 | 一致 |
| 42 | 决策单「修复」段 | 两个推送点 (7a self-resume + Step 9) 都门控 | 同上 `:554`/`:848` 各一个 `if no_push:` | 一致 |
| 43 | 决策单「修复」段 | `test_coordination_no_push.py` 16 条; 负控测试名 `test_c_negative_control_no_flag_no_env_attempts_push` 存在 | `git show 007d355:...test_coordination_no_push.py` grep 计数=16, 测试名逐字命中 | 一致 |
| 44 | 决策单「修复」段 | state-scanner 套件 1393 → 1409 全绿 | 逐文件 grep 求和: d50f9c3=1409, 007d355=1425 | 不一致 (见决策单 M2) |
| 45 | 母「本轮未做/存疑」#2 | A.1 YAML 项 `:62-73`, `skip_if: complexity: Level1` 在 `:66` | `git show d50f9c3:...phase-a-planner/SKILL.md \| awk NR=66,67` | 不一致 (见母 m1, 应为 :67) |
| 46 | 母 §2.2「遥测分区边界」 | 「written only by the CLI production path (…)」逐字出自 `coordination_probe.py:4-25` | 该文件该区间通读, 无此逐字句; 真身在 `phase1_gate.py:1047-1049` | 不一致 (见母 M1; R5 已自证同一处) |
| 47 | 字段 Spec §1 | `standards/openspec/templates/proposal-minimal.md` 全文 `grep -c "关联 Issue"` = 0 | 主仓实跑同一命令 | 一致 |
| 48 | 字段 Spec 跨 skill import 先例段 | `fetch_gate.py:111-112` 逐字「Mirrors state-scanner sync.py::_resolve_default_branch (replicated to keep phase-d-closer self-contained — no cross-skill runtime import).」 | `git show d50f9c3:...fetch_gate.py \| awk NR=111,112` | 一致 (逐字) |
| 49 | 字段 Spec 跨 skill import 先例段 | `handoff_autofill.py:403-407` 完整代码块逐字一致 | `git show d50f9c3:...handoff_autofill.py \| awk NR=403..407` | 一致 (逐字, 与 R5「本轮实读证实」条目吻合) |
| 50 | 字段 Spec 跨 skill import 先例段 | 同文件 `:48-51` 另一处 `state-scanner/scripts` + `collectors.multi_remote` | 同上 `NR=48..51` | 一致 |
| 51 | 字段 Spec | `coordination_probe.py:80-83` 点名过「同名包陷阱」 | `git show d50f9c3:...coordination_probe.py \| awk NR=80..83` | 一致 |
| 52 | 探针 Spec 非目标 #4 | `AB_TEST_OPERATIONS.md` 资产盘点写「Skill eval suites 28 个 ✅ 全量覆盖」 | 主仓文件 `:76` 逐字比对 | 一致 (逐字, 且探针 Spec 自己已指出这与实测 31 个/`#150` 的 14/43 三方不一致, 属已知留痕问题, 非本轮新漏) |
| 53 | 探针 Spec 非目标 #4 | 实测 `ab-suite/` 有 31 个 `.json` | `ls` 计数 | 一致 |
| 54 | 母 D18 | 1A 移出内容 ≈27KB, 母 Spec 现文的 17% | 审计轨 `.aria/audit-reports/a1-entry-claim-audit-trail.md` §6 中对应「§2.1/§5」旧文批次 (`142-444` 行) 实测 35398 字节 (≈34.6KB); 27648/159250≈17.4% 与「17%」量级相符 | 无法核 (量级相符, 精确到 KB 级有出入; §6 混合了多批迁移材料, 无法干净切出与「27KB」严格对应的字节区间) |
| 55 | 母 D17 | 「R5 三份 Spec 的 4 条 critical 里 3 条同形 (母 M1/M5 + 探针 C1 + 字段 C1)」 | R5 聚合报告「Critical 簇」表列出的是**去重后**6 个簇 (R5-1~R5-6) + 2 个结构性选项, 未见按「母 M1/M5/探针 C1/字段 C1」这套**去重前逐席原始编号**列出的清单 | 无法核 (可能是同一批 finding 在「去重前逐席标签」与「去重后聚合簇」两种口径下的正常差异, 未见矛盾证据, 但也未找到能直接核对「4」与「3」这两个数字的原始清单) |
| 56 | 母 FIX-19 / m2 | dogfood 头部「Linked Issue: none」与生产 claim 实际所传 `linked_issue` | `git show refs/aria/coordination:claims/023236f2/s-26ad@0914.yaml` → `linked_issue: 10CG/Aria#174` | 不一致 (见母 m2, 未必矛盾但未加说明) |
| 57 | 母/字段/探针三份 Status 行 | 六项裁定 (1A/2b/3b/4i/5/6i) 已落版 | 逐条比对 SC 表 (SC-1/4/27/30/31 已标 ⛔撤销)、Impact 表 (无 spec_slug/track_form 新字段)、rule6_note (确认 4i 修复独立存在)、SC-2/15 分类改写、字段/探针两 Spec 哨兵集合与字段名英文 canonical | 一致 |
| 58 | 探针 Spec Status 行 | SC-19/SC-20 已入表; `"none_sentinel"`(原 `"wu_empty"`) 改名已落 | 通读 SC 表逐条核对 | 一致 |
| 59 | 字段 Spec Status 行 | 哨兵集合 `{none, 无}` / 字段名英文 canonical `Linked Issue` + 中文 alias 已落版 | §2/§3 E0/E5 通读核对 | 一致 |
| 60 | 母/字段/探针跨 Spec 接缝 | `own_layer` 枚举第 6 值 `"bad_token_union"` 拼写在三处 (探针 §3 表 / §7 枚举 / R4 补注) 统一 | 通读探针 Spec 全部相关行 | 一致 |
| 61 | 探针 Spec SC-19 | 常量黑名单需与字段 Spec 模板 placeholder 同源 | 两份 Spec 对应段落交叉引用一致, 均写同一 placeholder `` `{<org>/<repo>#<n>}` `` | 一致 |

## (d) 本席核验为真、无 finding 的部分 (归类小结, 覆盖上表全部「一致」行)

- **`phase1_gate.py` 全部引用行** (`:56`/`:210`/`:1191`/`:1230`/`:1233-1235`/`:1236-1238`/`:791-802`/`_main:1173`/`run_gate:1032`/`_run_gate_impl:335`) —— 逐行核对, 无一处偏差。
- **`lib/collision.py` 全部引用行** (`normalize_linked_issue:178`、`_linked_issue_matches:219`、三参数签名`:230-234`、`:265-266`/`:268`/`:272-275`/`:278-279`) —— 逐行核对, 无一处偏差, 且这些行同时支撑母 Spec 里十余处不同章节 (§2.1/§2.4/§2.4a/D3/D4/D14/SC-2/SC-29) 的断言, 全部自洽。
- **`lib/claim_lifecycle.py`、`lib/claim_schema.py`、`lib/identity.py`、`lib/constants.py`、`lib/track_id.py`、`lib/gc.py`、`lib/reconcile.py`、`lib/coordination_ref.py`** 的全部具名行号引用与逐字引文 —— 无一处偏差, 含两处**逐字 docstring 引用** (`claim_lifecycle.py:396-399`、`constants.py:40-44`+`:50`) 完全一致。
- **`scripts/release_gate.py`** 的 `:141`/`:172`/`:225`/`:236-237` —— 无偏差, `:236-237` 那段代码块母 Spec 直接贴了原文, 逐字符核对一致。
- **各 SKILL.md 文件** (`phase-b-developer:86-98`、`branch-manager:143-155`、`phase-d-closer:38-58`、`phase-a-planner:1-15`、`spec-drafter:1-12/28-32/125-165/365-372`、`state-scanner:143-180`、`config-loader:128-145`) —— 无偏差, 其中两处「既有措辞缺陷」(branch-manager 标题 Part A1 却命令 `--phase B`; phase-d-closer:56 把 SWEEP_TTL 误写 STALE_TTL) 均被独立证实**真实存在**, 母 Spec 对它们的定性 (「既有缺陷, 非本 Spec 引入, 记 follow-up」) 也核实准确。
- **`references/layer-l-integration.md:15/45`、`docs/coordination-ref-schema.md:129-139`、`config-loader/DEFAULTS.json`(`state_scanner` 段确无 `coordination` 键)** —— 无偏差, 后者是 rule6_note substitute 断言的 baseline-必红证据, 核实为真。
- **决策单「修复」段除测试计数外的全部技术细节** (`--no-push`/`ARIA_COORDINATION_NO_PUSH`/大小写不敏感/`push_skipped`三值/两处门控/`no_push_requested_by_env`独立解析) —— 逐条在 `007d355` 分支源码里找到对应实现, 无偏差。
- **`AB_TEST_OPERATIONS.md:76/222-228`、生产 `refs/aria/coordination` 里的 2026-08-02 audit-test claim、`ab-suite/` 实测 31 个 `.json`** —— 均为真, 且探针 Spec 对「28 vs 31 vs #150 的 14/43」三方不一致的自我披露也核实准确 (它自己已承认、已开 follow-up, 不是我这轮新发现的漏洞)。
- **三份 Spec 的 Status 行与六项裁定 (1A/2b/3b/4i/5/6i) 的落版内容** —— 逐条比对 SC 表、Impact 表、D 决策记录表, 内容与 Status 行的概述一致; 字段 Spec、探针 Spec 各自的 round-3 变更点 (哨兵集合、字段名 canonical、`none_sentinel` 改名、SC-19/SC-20 入表) 均能在正文找到对应实现, 无「Status 说做了但正文没有」的情况。

## (e) 收敛判断

R5 factcheck 席在**行号存在性**这一层抓出 22 条不实引用/计数/锚点 (19 条机械可抓)。本轮镜头是**内容真实性**这一层——比 R5 那层严格得多的判据。在这个更严格的判据下, 落在 **2026-08-30 新写文本**(rework v4/round-3/决策单)里的不实断言 = **3 条 Major + 2 条 minor** (决策单 M1/M2、母 m1/m2), 另有 1 条 Major (母 M1) 严格说是**旧文本未被本轮清账**, 不是本轮新写错的, 但因为它是 R5 已经点名过的欠账、本该在这轮被扫掉却没有, 仍计入本轮的不实断言范围。

把分母放大看: 本席逐条实读核验了约 **65 条**跨三份 Spec + 决策单 + aria 两个 SHA + 生产 ref 的具体事实断言 (文件:行号、函数签名、逐字引文、JSON 结构、测试计数、grep 结果), 命中率约 **91%** (59/65 一致, 3 条 Major、2 条 minor、1 条无法核)。相比 R5 factcheck 席「22 条不实 / 至少 19 条可机械抓」的密度, 本轮**不实断言的比例明显下降**, 尤其是承重的代码行号 + 函数签名 + docstring 逐字引用 (母 Spec 的大多数 D 决策记录、SC 断言、Impact 表都建立在这类引用上) **无一处偏差** —— 这是这版 rework v4 相对上一版最扎实的改善: 说明 R1-R5 反复打磨的「文件:行号」层面的核验方法论确实生效了, 错误率被压到了很低的水平。

但有一个信号需要 owner 注意: 我抓到的 3 条 Major 里, **母 M1 是 R5 已经自己点名过的错误**, rework v4 落版时没有把它扫进「本轮逐项清账」的范围, 一字未改地留到了这一轮。这与 memory `no-ruling-shortens`/`stop-adding-rounds` 提醒的模式相似——不是「查不出来」, 是「查出来了但没被路由进这一轮该修的清单」。决策单里的两条 Major (M1/M2) 则是**这一轮新写**的决策记录本身带着的数字误差, 性质上是「新证据没有比对上真实源头就写进了决策记录」, 而不是历史遗留。二者共同指向同一条更底层的观察: 承重的**代码引用**这条线已经打磨得很扎实, 但承重的**运营/量化类数字**(grep 统计、测试计数) 这条线的核验强度还没有跟上代码引用的水准, 值得在后续轮次里对齐同一套核验纪律。

## (f) counts

0C / 3M / 2m
