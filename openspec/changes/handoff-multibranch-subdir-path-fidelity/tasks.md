# Tasks — `handoff-multibranch-subdir-path-fidelity`

> **Spec**: [proposal.md](./proposal.md) (v7, Approved 2026-09-12) | **决策单**: [`2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md`](../../../.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md) (§2 的 10CG/Aria#195 表 8 行 + §5 复核, 21 条即最终口径) · [`2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md`](../../../.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md) (A′ + 写侧守卫, 09-12 追认) | **审计**: post_spec R1–R5 (R5 `overridden_by_user: true`) → post_planning (本文件)
> **Level**: 3 (决策单 §2 第 7 行, 不拆) — 本文件 (A.2) + `detailed-tasks.yaml` (A.3, 单一 SOT: verification / 依赖 / 工时 / rule6_note / A.2 基线复核记录)
> **Status**: A.2/A.3 v1 (2026-09-15, simonfish/023236f2) — 待 post_planning
> **Scope**: 三个仓 — aria 子模块 (A.2 实测 `1cb3872` = v1.73.3; proposal 行号冻结于 `f314785`) · standards 子模块 (`8b49562`) · 主仓 (`36ea288`)
> **ship target**: aria-plugin `<vNEXT>`, 档位 **MINOR** (决策单 §2 第 6 行)。本文件不写字面版本号, 号在 5.1 执行时按 `plugin.json` + 远端 tag + 并发轨取号计
> **执行记录**: B 期新建 [`verification-ledger.md`](./verification-ledger.md) (基线 / RED / GREEN / 反事实 / 复核结论), 下文「记入台账」均指该文件

---

## 读前必看 — proposal 正文与执行口径的差异 (proposal 不改, 以本节为准)

proposal 是 09-10 冻结、09-12 裁定前写成的; 下列各项在正文里写的是另一支或已过期的事实。实施者照正文字面执行会做错, 故逐条列出。

| 编号 | 事项 | proposal 正文 | 执行口径 | 依据 |
|---|---|---|---|---|
| 1 | dedupe 排序键 | 推荐默认「不改排序键」; Task 4.1 / 4.2 / SC-11(j) 三处写「仅默认支下」把 build-order 不变量条件化为「同 `rel_path` 前提下」 | **改键支**: 新增 2.6 加第 5 级键; 三处文档改写为五级键序说明, 不变量句保持无条件; SC-11(j) 取「键序说明含 `rel_path`」 | 决策单 §2 第 4 行附问 + §5 终裁 |
| 2 | CHANGELOG 已知边界 | §6.5 与 SC-11(e) 写「四条」 | **五条**: 追加「mv 过的无 frontmatter 件, `updated_at` 仍取 mv 提交日; 不加 `--follow`」; `### Changed` 另追加 dedupe 第 5 级键一条 ⇒ 至少六条 | 决策单 §2 第 5 行、第 4 行 |
| 3 | standards 第三态措辞 | Task 4.4 限定从句「AI 手改路径是否同步该态待 owner 裁」 | 改为「本 cycle 不同步 (owner 2026-09-12 裁定), 缺口并入 5.3 issue」 | 决策单 §2 第 2 行第 (4) 问 |
| 4 | 遗留缺口 issue 所在仓 | Task 5.3 未定 | `10CG/aria-plugin` | 决策单 §2 第 2 行第 (2) 问 |
| 5 | 前置门 Task 2.0a / 2.0b | 未解除, 阻断 B.1 | 已随 09-12 裁定解除 (Level 3 / MINOR), 并入 2.0 | 决策单 §2 第 6、7 行 |
| 6 | SC-10 可执行命令 | 9 模块一条 `python3 -m unittest …`, 「Ran 169」 | A.2 实跑: 该命令对 `test_collision` **收集 0 条** (28 个 pytest 风格裸函数), 169 = 其余 8 模块之和 ⇒ **追加 pytest 腿** (只增不改); 同型的 phase-d-closer `test_fetch_gate.py` (11 条, 消费 `collision.kind`) 一并进 4.3 回归 | `detailed-tasks.yaml` `metadata.test_runner` |
| 7 | SC-12a 改前 / 改后快照 | 两次扫描间比对分支集; 改前在 B.1 时跑 | **追加** ref→SHA 映射比对 (同分支上的新提交同样改变 collector 输入, 只比分支名会误判); 改前扫描改用基线 SHA 的一次性 worktree 旧代码, 与改后**背靠背**跑 (只增不改; 消除「改前与改后之间整个 Phase B 不许推送」的长窗口) | memory `partial-freeze` 同型 |
| 8 | 基线行号 | 冻结 `f314785` | A.2 复核 `f314785..1cb3872` (41 触点): **代码落点零 diff, 行号全部有效**; `state-snapshot-schema.md` `:1062` 后插 2 行 ⇒ 正文引用的 `:1074` 起全部 +2 (例 `:1104`→`:1106` / `:1114`→`:1116` / `:1126`→`:1128` / `:1136`→`:1138`); `layer-l-integration.md` `:84` 后插 2 行 (`:103`→`:105`); `phase-1-collectors.md` 原位改 1 行, 不移位; schema `## Change history` 表末已有 2026-09-13 新行 (正文「表末行仍是 2026-07-19」过期)。1.3 在 B.1 时对当时 HEAD 重跑 | `detailed-tasks.yaml` `metadata.baseline_rebase` |
| 9 | 主仓 16 个版本点 | 写作时取值 v1.73.0 | A.2 实测: 15 点 = 1.73.3, **`VERSION:24` 仍为 v1.73.0** (v1.73.1 / v1.73.2 / v1.73.3 三次发版漏改; 该点无机械兜底) ⇒ 5.1 直接写新号, 不按「上一版 +1」核对 | 同上 |
| 10 | 编号 | 含 2.0a / 2.0b / 5.4a | 2.0a / 2.0b 并入 2.0; 5.4a → **5.6** (内容按 standards `content-integrity.md` §4.4 / §4.5 更新); 新增 **1.3 / 2.6 / 3.4**。字母后缀不被归档门的 checkbox 正则识别为 parent, 故不沿用 | 归档门 `spec_complete.py` `_CHECKBOX_ANY_RE` |
| 11 | 测试编写时点 | 3.1–3.3 列在实现之后 | 用例本体全部在组 1 写好并取 RED (Task 1.2 的例外清单已把 SC-6(c) / SC-7 列为同文件用例, 第二条记录含 SC-6(a)(b)); 3.1–3.3 承接实现后的 GREEN 与反事实。2.5 依赖 2.1 / 2.2 产出 `rel_path` 的数据序不变 | proposal Task 1.2 |

---

## 范围边界 — 本文件到哪里为止

| 阶段 | 归属 | 说明 |
|------|------|------|
| 组 1–5: 基线复核 / 测试先行 / 实现 / 实现后钉测 / 文档与回归 / AB / 发布同步 / 收尾 | **本文件** | change 自身交付物 |
| Phase B 入口 `phase1_gate` (advisory) | `phase-b-developer` | 若 B.0 调用: 用同一串 raw track-id `handoff-multibranch-subdir-path-fidelity` (不带容器后缀)。预期: CLI 每次调用都新生成 session id, 对本容器 09-12 的 claim 走不到 self-resume ⇒ 另写一条 claim (该 claim 心跳新鲜时还会报 `occupied`, 对象是本容器自己)。属已知缺口, 不是竞争者, 记入台账 |
| Phase C: 主仓 PR / pre-merge gate (Rule #8) / merge | `phase-c-integrator` | 由 5.2 交付 |
| Phase D: 归档 / claim 释放 / 周期 handoff (Rule #9) / owner 插件更新 | `phase-d-closer` + owner | 归档门消费本文件全部 checkbox; `plugin-cache-currency` 在 owner 更新插件前预期 STALE |
| `handoff.py` 子目录支持 (原选项 (ii)) / `handoff-mechanics.md:114-124` 处方表 / mv 日语义 / `reference-snapshot-aria.json` 重采样 / schema `errors[].tracks[]` 形状 | **不在本文件** | 决策单 §2 第 2、5 行; 统一登记进 5.3 的 issue |

---

## Task Group Overview

| 组 | 主题 | 依据 |
|----|------|------|
| **1** | B.1 基线复核 + 前置核验 + 测试先行 (RED 台账) | proposal Task 1.1 / 1.2, §触点文件清单 |
| **2** | 实现: 枚举层 / 调用方与 legacy id / 读不到不伪造 / fail-soft 键 / 写侧守卫 / 排序键第 5 级 | proposal §What 1–4、§2.5; 决策单 §2 第 4 行 |
| **3** | 实现后钉测: F1 消费方 / tie-break / legacy id 的 GREEN 与反事实; 其余实体的反事实实跑 | proposal Task 3.1–3.3, SC 表「反事实」列 |
| **4** | 文档同步 (schema / docstring / standards / references) + 全量回归 + 活体 dogfood + 处方面措辞复核 | proposal §6, Task 4.1–4.5, SC-10 / 11 / 12 |
| **5** | 遗留 issue → Rule #6 AB → 版本与 CHANGELOG → 引用写法自检 → 子模块合并双推 → 主仓同步面与 PR → 收尾 | proposal Task 5.1–5.5; 执行序以 yaml 依赖为准 |

## 1. B.1 基线复核与测试先行 (RED — 对 B.1 基线实跑红, 组 2 落地后转绿)

- [ ] 1.1 前置核验: 本仓 `docs/handoff/` 无子目录、无非 ASCII 文件名; 两份冻结语料 (`aria/skills/state-scanner/tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 与 `.aria/repro/handoff-tracks-frozen-2026-09-05.json`) 内无子目录路径 — 命令与输出记入台账
- [ ] 1.2 新建 `tests/test_handoff_multibranch_path_fidelity.py` (`unittest.TestCase` 风格), 按 SC 分四批写完全部用例 (含 SC-6 / SC-7 / SC-13 与 2.6 的排序键用例); 对 B.1 基线逐条实跑, 记两条 RED 记录 (五族 SC-1 / 3 / 5 / 13 / 17 + 其余 baseline-failing 实体) 与回归锁在基线上为绿的记录 — 台账
- [ ] 1.3 B.1 基线复核: 实测 aria `origin/master` 与主仓 gitlink; 照 proposal §触点文件清单 41 条对 `f314785` 与 `1cb3872` 两个点各跑 `git diff --stat`, 更新行号偏移表; yaml TASK-001 列出的 SC-11 grep 判据在基线上全红 — 台账

## 2. 实现 (aria `state-scanner`)

- [x] 2.0 前置门全部解除: A′ + 写侧守卫 (决策单 2026-09-07, 09-12 追认) · Level 3 不拆 (原 2.0a) · MINOR (原 2.0b) — 决策单 §2 第 2、6、7 行
- [ ] 2.1 枚举层 `_list_handoff_files`: `-z` 按 NUL 切分并丢空段 · 相对路径的前缀剥离从 `_HANDOFF_TREE_PATH` 派生 · 前缀守卫逐项上报 (保持 2-tuple 签名 + 注入 reporter, 双通道) · `.md` 过滤作用于 `rel` 的 basename · docstring 契约句与 `:177` 常量注释 — SC-3 / 9 转绿, SC-2 保持绿
- [ ] 2.2 三个仓内调用方与 legacy track_id 改用 `rel_path`; 两个 TrackEntry 构造点都写 `rel_path`; `scan.py:186` 只拼串改读 `rel_path` (无兜底, 同形早退), `:193` / `:209` 上报的 `filename` 不变; 同批给 `test_scan_integration.py` 的 `HEALTHY_TRACKS` 补键; `:36` / `:332` / `:494` 格式声明同改 — SC-1 / 4 / 6 / 8 / 13 / 17 转绿
- [ ] 2.3 git show 失败只报 soft_error, 不进 `tracks[]`; 新增 `unreadable_count` 按三类外延实现; 不可解码名 (`"�" in rel`) 显式跳过并报 `handoff_multibranch_undecodable_path` — SC-5 / 16 / 18 转绿
- [ ] 2.4 fail-soft 早退 dict 补 `unreadable_count: 0` — SC-14 转绿
- [ ] 2.5 pointer 写侧守卫 (`writers/latest_md_writer.py`): 判据 `rel = track.get("rel_path") or track.get("filename")` 再比 `rel == filename`; `_render_pointer` / `_render_pointer_unavailable` 返回 `(content, reason)`; `write_latest_md` 三支恒带 `degraded_reason`; 降级文案写明子目录原因; 两处被改函数 docstring 与 `:159` 口径句同改 — SC-15 转绿, SC-11(k)
- [ ] 2.6 dedupe 排序键加第 5 级 `rel_path` (决策单 §2 第 4 行附问): 顶层行 (`rel_path == filename`) 优先, 其余按 `rel_path` 字典序取大; 缺 `rel_path` 键按 `filename` 处理; 算法字面见 yaml TASK-014 — 排序键用例转绿

## 3. 实现后钉测 (GREEN + 反事实)

- [ ] 3.1 SC-6 (F1 跨文件消费方): 端到端产出 tracks_data、四道前置齐备下 GREEN; 反事实: 枚举退回 basename ⇒ (a)(b) 红, `:180` 局部变量整体重指 `rel_path` ⇒ (c) 红 — 台账
- [ ] 3.2 SC-7 特性化测试 (docstring 首行标注 hypothetical input) 与 2.6 排序键用例 GREEN; 既有 dedupe 用例 (含 `TestDedupeTiebreakByBranchWhenUpdatedAtAndFilenameTie`) 不变 — 台账
- [ ] 3.3 SC-13 GREEN; 三条反事实 (id 沿用 basename / 日期仍拼顶层路径 / 只给 frontmatter 分支加 `rel_path`) 各自转红; 不写「不折叠」断言 — 台账
- [ ] 3.4 其余实体的反事实实跑 (SC-15 四条 / SC-18 两条 / SC-9 (b)(c) / SC-16 两条 / SC-2 解析写错): 在一次性 worktree 副本上打补丁、`python3 -B` 跑, 不在 feature 分支工作树上改 — 台账

## 4. 文档同步与回归

- [ ] 4.1 `references/state-snapshot-schema.md` §`tracks_multibranch` 同步 (行号按 A.2 偏移表): `rel_path` 行 / `unreadable_count` 与三类外延 / legacy 公式 / pointer 排除句勘正为任意深度 / 四级改五级键序说明 (改键支) / fail-soft 形状补 `unreadable_count` 与 `identity_advisories` / 两个新 kind 登记 / git show 失败不再产生 legacy 行 / F2 条件式边界 / committer 改 author date / `## Change history` 新增一行 — SC-11 (a)(b)(f)(g)(i)(j)
- [ ] 4.2 collector 与 writer 的 docstring / 注释 (proposal Task 4.2 清单; 其中 `:396` 模块注释与 `_dedupe_sort_key` docstring 取改键支; `:36` / `:332` / `:494` 已由 2.2 落, 本项只核); `references/phase-1-collectors.md:102` 返回契约补 `degraded_reason` — SC-11 (c)(j)(l)
- [ ] 4.3 回归: `run_tests.py` 全量 + pytest 腿 (`test_collision.py` / phase-d-closer `test_fetch_gate.py`) 零失败; SC-10 点名集按两腿执行; 两份冻结语料未重生成; SC-12a (本仓平铺, 背靠背 + ref→SHA 映射比对) 与 SC-12b (子目录临时仓) 活体 dogfood — 台账
- [ ] 4.4 `standards/conventions/session-handoff.md:97` 与 `:171-173` 补第三态 (限定机械 writer 路径, 措辞按「读前必看」第 3 条); `references/layer-l-integration.md:105` 同步; 记一行「已复核, 本 spec 不对子目录布局表态」 — SC-11 (h)(l)
- [ ] 4.5 处方面措辞复核: `references/rules/advanced-rules.md:443-444,511-512,544` · `RECOMMENDATION_RULES.md:28,30,31` · `phase-d-closer/SKILL.md:218` 逐处读并记结论; 若落编辑, rule6_note 落行升判据表第二行 — 台账

## 5. Rule #6 AB / 发布 / 收尾 (执行序: 5.3 → 5.5 → 5.1 (aria 侧) → 5.6 → 5.2 (子模块) → 5.1 (主仓同步面) → 5.2 (主仓 PR) → 5.4)

- [ ] 5.1 版本与发布同步面 (MINOR, 号执行时计): aria 版本 SOT 5 文件 + `CHANGELOG.md` (`### Fixed` 三条 / `### Added` 三个字段与两个新 kind / `### Changed` 至少六条含五条已知边界); 子模块推送核验之后, 主仓两个 gitlink + 16 个版本点 (含 `VERSION:24`) + custom checks 复跑 — SC-11(e)
- [ ] 5.2 Phase C: aria 与 standards 各自本地 `git merge` + aria tag + owner 授权后双推 + 逐 remote `ls-remote` 核验 master 与 tag; 主仓 gitlink 从实测值前进、不得回退; 主仓经 `phase-c-integrator` 开 PR 过 pre-merge gate 后合并
- [ ] 5.3 遗留缺口 issue 开在 `10CG/aria-plugin` (外向, owner 授权后发): `handoff.py` 子目录支持 + SC-15 布局 2 复现 + proposal Task 5.3 的 (a)–(f) 分条 + `session-handoff.md:97`「自动」一词 + 子目录布局不表态的锚点
- [ ] 5.4 Phase D: 归档 + `release_gate` 释放 claim + 10CG/Aria#195 回帖关闭 + 周期 handoff 内两处记录 (`reference-snapshot-aria.json` 未重采样; standards 已改) — SC-11(d)(h)
- [ ] 5.5 Rule #6 照跑 AB: 前置 = owner 以 `ARIA_COORDINATION_NO_PUSH=1` 重启会话; 用 `/skill-creator` 跑 state-scanner, 结果落 `aria-plugin-benchmarks/ab-results/`; 开 AB 套件缺口 issue (外向); substitute 实体台账全部保留 — rule6_note
- [ ] 5.6 引用与编号写法自检 (原 proposal Task 5.4a, 按 standards `content-integrity.md` §4.4 / §4.5 更新): 本 cycle 新写或改动的文字 issue 引用全限定、文内编号不用 `#` 与带圈字符; `check_bare_issue_refs.py` 作手动自检, 不把整份文件 rc 0 当验收门槛 — 台账

---

## Success Criteria ↔ 任务映射

| SC | 编写 (RED) | 转绿 | 钉测 / 反事实 |
|----|------|------|------|
| SC-1 | 1.2 | 2.2 | 4.3 |
| SC-2 | 1.2 (基线 JSON 在实现前生成) | (回归锁) | 3.4 |
| SC-3 | 1.2 (仓内 `core.quotePath true`) | 2.1 | 4.3 |
| SC-4 | 1.2 | 2.2 (后半) | 4.3 |
| SC-5 | 1.2 | 2.3 | 4.3 |
| SC-6 | 1.2 | 2.2 | 3.1 |
| SC-7 | 1.2 | (回归锁) | 3.2 |
| SC-8 | 1.2 | 2.2 (后半) | 4.3 |
| SC-9 | 1.2 | 2.1 | 3.4 |
| SC-10 | — | — | 4.3 (两腿) |
| SC-11 | 1.3 (基线全红) | 2.2 (i) / 2.5 (k) / 4.1 / 4.2 / 4.4 / 5.1 (e) | 5.6 |
| SC-12a / SC-12b | — | — | 4.3 |
| SC-13 | 1.2 | 2.2 | 3.3 |
| SC-14 | 1.2 | 2.4 | 4.3 |
| SC-15 (六个布局) | 1.2 | 2.5 | 3.4 |
| SC-16 | 1.2 | 2.3 (`rel_path` 由 2.2, `unreadable_count` 由 2.3) | 3.4 |
| SC-17 | 1.2 | 2.2 | 4.3 |
| SC-18 | 1.2 | 2.3 | 3.4 |
| 决策单 §2 第 4 行 (排序键第 5 级) | 1.2 | 2.6 | 3.2 |

## rule6_note

单一来源 = `detailed-tasks.yaml` `metadata.rule6_note` (本节不复述, 防两份不同文)。
