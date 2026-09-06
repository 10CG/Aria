已跑完 Step 0 机械扫描 (`scan.py`, **exit 0**, `errors[]` 为空, snapshot schema 1.0), 下面是全量状态 + 你点名的三项专项核查。

**先说最重要的一件事**: 你的前提与仓库实测不符 —— **当前 aria-plugin 不是 v1.14.0, 是 v1.69.1**。所以「badge 还停在旧版本」这个怀疑**不成立**; 但你担心的「Skill 列表没跟上」**确实存在**, 只是漏的是 2 个、而且漏了很久了。详见下方专项核查。

---

## 📍 当前状态

| 项 | 值 |
|----|----|
| 分支 | `feature/a1-entry-claim-duplicate-work-guard` (upstream 已配, ahead 0 / behind 0) |
| 模块 | Aria meta-repo (子模块 `aria` / `standards` / `aria-orchestrator`) |
| Phase / Cycle | UPM 未配置 (`upm.configured=false`) → 以 handoff 为准: **Phase B.2**, track `a1-entry-claim-duplicate-work-guard` |
| 变更文件数 | 4 (3 个 dirty 子模块指针 + 1 个未跟踪目录) |
| 关联 OpenSpec | `a1-entry-claim-duplicate-work-guard` (approved) |
| git 中间态 | 无 (`operation=none`, 无冲突) |
| 中断状态 | `.aria/workflow-state.json` 存在但为 **已完成态** (D.1–D.4 全部收尾, `completed_at=2026-09-02T23:26Z`), 且 `branch_anchor_match=false` (锚定 `master`, 当前在 feature 分支) → **不是活跃中断**, 无需 Resume/Abandon 决策 |

## 📊 变更分析

- 变更类型: 全部落在 `other` (4/4) —— 3 个子模块 gitlink dirty + `aria-plugin-benchmarks/ab-results/2026-09-05-.../` 未跟踪
- 复杂度: **Level 2**
- 架构影响: 无 (`architecture_impact=false`)
- 测试覆盖: 本次变更不含测试文件
- Skill 变更: **未检出** (`skill_changes.detected=false`) → 本轮不触发 Rule #6 AB 门

> 提示: 最新 handoff §0 明确写了这 3 个 dirty 子模块**是有意的**, gitlink bump 归 TASK-038/8.2、要等各自合 master 之后, **不要 `git add`**。

## 📄 需求状态

- 配置: 已启用 (`requirements.configured=true`)
- PRD: 2 份 (`prd-aria-v1.md` / `prd-aria-v2.md`)
- User Stories: **21 份** — done 17 / in_progress 2 / approved 1 / pending 1
- OpenSpec 覆盖: 7 个活跃变更全部 approved

## 🏗️ 架构状态

- `docs/architecture/system-architecture.md` 存在, status = **Active**, 最后更新 **2026-09-02** (3 天前)
- 需求链路完整 (`chain_valid=true`), 双父 PRD (v1 + v2) 均可解析

## 📋 OpenSpec 状态

- 活跃变更: **7 个, 全部 approved** (`a1-entry-claim-duplicate-work-guard` / m6-dispatch-input-delivery / m6-cost-model-telemetry / m6-e2e-resilience / m6-release-closeout / m7-agent-lifecycle / m7-fleet-aggregation)
- 已归档: **142** | 待归档: **0**
- ⚠️ 设计未实施 (`design_deferred`) **5 个**:

| id | status | 未勾任务 | staleness |
|----|--------|---------|-----------|
| aria-2.0-m6-release-closeout | approved | 41/41 | **103d** |
| aria-2.0-m7-agent-lifecycle | approved | 18/18 | 65d |
| aria-2.0-m6-cost-model-telemetry | approved | 25/38 | 58d |
| aria-2.0-m6-e2e-resilience | approved | 25/40 | 55d |
| aria-2.0-m7-fleet-aggregation | approved | 20/20 | 48d |

## 🛡️ 审计状态

- 审计系统: **enabled**
- 上次审计: `pre_merge` **R5**, verdict **PASS**, 2026-09-02T18:10Z (spec: linked-issue-field-availability)
- `converged=false` —— R5 判 PASS 但未标记收敛, 该 spec 已于 09-02 归档, 属历史记录
- 选取来源: 694 个候选 / 88 个 aggregated, 按 filename-timestamp 排序

## 🔧 自定义检查

**14/14 全部 ✅ PASS** (0 FAIL / 0 SKIP)。与本次提问直接相关的四条:

| check | 结果 |
|-------|------|
| `m6-version-badge-match` | ✅ **OK badge=1.69.1** — 主项目 README badge 与 plugin.json 一致 |
| `plugin-version-arch-docs-match` | ✅ OK plugin=1.69.1 (2 处架构文档版本行匹配) |
| `i18n-readme-translation-currency` | ✅ OK (3 份 i18n README 均已同步到 1.69.1) |
| `main-project-version-consistency` | ✅ OK 主项目版本 1.7.5 — 9 个引用点全部一致 |

其余 10 条 (issue 缓存新鲜度 / claude-md 卫生 / config 模板键 / plugin 缓存 / Forgejo token 活性 / linked-issue 字段 / 架构文档陈旧度 等) 亦全绿。

## 🔄 同步状态

- 当前分支: ahead 0 / behind 0 vs `origin/feature/a1-entry-claim-duplicate-work-guard`
- 多远程 parity: **`overall_parity=true`**; 主仓 `5d9b568` 在 `origin` 与 `github` 两端一致, evidence_grade = **fresh** (remote refs 1 分钟前刷新)
- gitlink 完整性: **6/6 `ok`** (3 子模块 × 2 remote), 无 orphaned
- 子模块分支 head: `standards` `bb5d375` (两端 MATCH) / `aria` `ab3dbd0` (两端 MATCH) / `aria-orchestrator` `92acce5` 在 `feature/m6-cost-model-telemetry`
- ⚠️ 一处需知悉: `aria-orchestrator` 的 **github leg parity = `unknown`** (`reason=no_local_tracking_ref`) —— 该分支在 github 侧没有本地 tracking ref, 属「未测到」而非「已同步」。`overall_parity` 仍为 true, 但这一条不构成正证据

**📝 README 版本一致性** (Phase 1.8 `readme` collector):

| 面 | 值 | 判定 |
|----|----|----|
| `aria/README.md` 版本头 | 1.69.1 | ✅ 与 plugin.json **match** |
| `aria/.claude-plugin/plugin.json` | 1.69.1 | — |
| 根 `README.md` 版本头 | `null` | 不适用 (根 README 无 `**版本**:` 行, 该 collector 只认这个模式, 不认 badge) |

**📦 插件依赖**: `standards` 子模块已 initialized + registered。
**🔗 Forgejo 配置**: 检出 Forgejo remote (`forgejo.10cg.pub`), 但 `config_status=missing` —— 可跑 `/forgejo-sync` 引导创建 (非阻塞)。

## 🎫 Open Issues

**47 条 open** (2026-09-05T23:19Z 抓取, 来自缓存, 无 fetch 错误):

| repo | open |
|------|------|
| 10CG/Aria | 20 |
| 10CG/aria-plugin | 20 |
| 10CG/aria-standards | 5 |
| 10CG/aria-orchestrator | 2 |

与本次提问同域的一条: **aria-plugin #150** —「Rule #6 判据表第三行的兜底『缺一照跑』对 14/43 个 skill 结构上不可执行 —— 它们根本没有 AB 套件」。它和下面要说的 README 漏列问题指向同一件事: **skill 清册面缺机械核对**。

## 🌐 交接与多 track 感知

- 最新 handoff: `docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md` (**0.75h 前**, frontmatter 完整; track `a1-entry-claim-duplicate-work-guard`, phase **B.2**, status **active**)
- 无错放文件 (`misplaced_files=[]`), 跨 worktree 无其他交接 (worktree_count=1)
- ⚠️ **collision.kind = `self_multi_container`** —— 检出同一 owner 的两个容器串 (`dev-claude` / `simonfishgit/dev-claude`) 落在同一组。`coordination.enabled=true, mode=advisory`, 但按契约闸门只在**用户确认进入 Phase B 时**由编排层调用 `phase1_gate`, 本轮为只读扫描, **未调用** (也未写/推任何 claim)

---

## 🔬 专项核查 — 你点名的三个问题

### 问题 0 (前提勘正): 版本根本不是 v1.14.0

| 面 | 实测值 | 位置 |
|----|--------|------|
| plugin.json (**版本 SOT**) | **1.69.1** | `aria/.claude-plugin/plugin.json` |
| aria/README.md 版本头 | **1.69.1** (Released 2026-09-04) | `aria/README.md:5` |
| 主项目 README badge | **v1.69.1** | `README.md:8` |
| 主项目 README 版本区 | 1.69.1 (aria-plugin, 42 Skills + 11 Agents) | `README.md:242` |

**v1.14.0 与当前 SOT 相差 55 个 minor**。请先确认你说的是不是另一个环境或另一份 checkout —— 如果你本地装的插件副本停在旧版, 那是 `plugin-cache-currency` 的范畴, 而该 check 本轮报 **OK installed=1.69.1 (scope=user) sot=1.69.1**, 即本机安装副本也已是 1.69.1。

### 问题 1: README 的 Skill 数量与实际目录一致吗 → ✅ **一致**

| 口径 | 声称 | 实测 | 判定 |
|------|------|------|------|
| 总数 | 42 (`aria/README.md:44` 标题 "Skills (35 user-facing + 7 internal = 42 total)") | **42** 个含 `SKILL.md` 的目录 | ✅ |
| user-facing | 35 (`README.md:7` + `:44`) | **35** (42 减去 7 个 `user-invocable: false`) | ✅ |
| internal | 7 (`README.md:46` 具名列出 7 个) | **7**: agent-router / agent-team-audit / arch-common / aria-token-telemetry / audit-engine / config-loader / git-remote-helper | ✅ 名单逐个对上 |
| plugin.json description | "42个 Skills (35 user-facing + 7 internal) + 11个 Agents" | 同上 | ✅ |
| Agents | 11 (`README.md:115` "Agents (11)") | 11 条 bullet | ✅ |

> 附注: `aria/skills/` 下有 **43** 个目录, 但其中 `session-closeout/` 只有一个空的 `scripts/` 子目录、**没有 SKILL.md 且未被 git 跟踪** —— 是本地残留物, 不是 skill, 不计入 42。它与真实存在的 `session-closer` 名字相近, 容易在人工清点时把数字数错, 建议直接删掉本地这个空目录。

### 问题 2: Skill 列表完整吗 → ❌ **不完整, 漏 2 个 (这是本次唯一的真问题)**

`aria/README.md` 的 Skills 小节 (`:44`–`:114`) 共 **40 条 bullet** = 33 个 user-facing + 7 个 internal。而实际 user-facing 是 **35** 个, 漏掉:

| 漏列 skill | 加入时间 | 漏了多久 | 该放进哪个分类 |
|-----------|---------|---------|--------------|
| **`issue-triage`** | 2026-05-13 (`d2d7cb6`) | **约 3.7 个月** | `**Feedback & Reporting**` (紧挨 `aria-report`, 二者同域) |
| **`session-closer`** | 2026-06-25 (`7801bd4`) | **约 2.4 个月** | `**Ten-Step Cycle Core**` (与 `phase-d-closer` 相邻, 且需一句消歧: session 维度 vs cycle 维度) |

建议补的两行 (与现有条目同体例):

```markdown
**Ten-Step Cycle Core**
...
- session-closer — Session-level closeout (leaf): synthesize unhandoffed work into docs/handoff/ (orthogonal to phase-d-closer's cycle closeout)

**Feedback & Reporting**
- aria-report — Report bugs, feature requests, or questions to the Aria team
- issue-triage — Systematically verify an incoming issue (version / code path / in-flight branch / reproduction) before recommending a fix
```

**这个缺陷的形状值得单独点出**: 标题里的**总数 42 是对的**, 分项 35/7 也是对的, 但**正文只列了 40 条**。也就是说计数行是手写的、与 bullet 数**不自洽** —— 数量核对**恰恰通不过**这个漏洞, 只有逐条比对目录才抓得到。你原本担心的是「数量没更新」, 真实情况反过来: **数量对、列表少**。

### 问题 3: plugin badge 版本与 plugin.json 一致吗 → ✅ **一致**

- 机械检查 `m6-version-badge-match` 本轮 **OK badge=1.69.1**, 它的判据就是 `grep` 出 `README.md` 的 badge 版本与 `plugin.json` 的 `version` 逐字符比对, 不一致即 exit 1
- 交叉核对: `README.md:8` = `Plugin-v1.69.1-blue`, `plugin.json.version` = `1.69.1` ✅
- 派生面也全绿: 架构文档 2 处版本行 ✅ / 3 份 i18n README ✅ / 主项目版本 9 个引用点 ✅

---

## ⚠️ 顺带发现的机械覆盖缺口 (建议开单)

**没有任何检查在核对「README 的 Skill 清册 vs `aria/skills/` 实际目录」。** 证据:

- `readme` collector (`scripts/collectors/readme.py`) 只做一件事: 用 `^(?:#{1,6}\s+)?\s*>?\s*(?:\*\*)?(?:版本|Version)(?:\*\*)?[:：]\s*v?([\d.]+)` 抓版本号做比对, **完全不看 skill 数量和列表**
- `.aria/state-checks.yaml` 14 条 check 里, `m6-version-badge-match` 只比 badge 数字, 其余无一涉及 skill 清册
- 结果就是这两个漏列**平安存活了 2.4 到 3.7 个月, 期间跑过无数次全绿扫描**

这正好是 `main-project-version-consistency` 那条 check 的设计注释里写的同一类问题 ——「没有同步面清单 ⇒ 漂移在机械层完全不可见」。建议照它的形态加一条 repo-local check, 判据可写成 (fail-closed):

```
实际 = ls aria/skills/*/SKILL.md 的目录名集合
声称 = aria/README.md Skills 小节的 bullet 名 ∪ :46 internal 具名清单
实际 ⊄ 声称  → FAIL 并列出漏列项
声称 ⊄ 实际  → FAIL 并列出幽灵条目
标题里的 total / user-facing / internal 三个数 ≠ 实测三数 → FAIL
```

三个判据缺一不可: 只比总数会被本次这种「总数对、列表少」骗过去; 只比列表会漏掉标题数字漂移。

---

## 🎯 推荐工作流

修 README 漏列属文档同步 (Rule #3), 不是需求变更 → OpenSpec **Level 1 (Skip)** 即可; 本轮 `skill_changes.detected=false`, **不触发 Rule #6 AB**。

**【1】(推荐) 只修 README 漏列 — Level 1 doc-only**
- 在 `aria/README.md` 补 `issue-triage` + `session-closer` 两行 (位置与文案见上)
- 数字**不用改** (42 / 35 / 7 本来就对), 版本**不用 bump** (这是补当年漏同步的账, 不是新增能力)
- 步骤: B.2 编辑 → C.1 提交 (`docs(readme): 补列 issue-triage / session-closer 两个 user-facing skill`)
- ⚠️ **落点在 `aria` 子模块**, 按 CLAUDE.md 硬约束: 子模块合并**一律本地 `git merge` + 双推**, 禁用 Forgejo 服务端 merge; 推后对 `origin` 和 `github` **各自 `git ls-remote` 取 SHA 比对**, 全部一致才算成功

**【2】修 README + 同时加机械检查 (根治, 推荐搭配 1 一起做)**
- 【1】的全部 + 在 `.aria/state-checks.yaml` 加 `readme-skill-roster-match` (三判据见上)
- 新检查**必须先在当前基线亲跑三态**: 打补丁前应 **FAIL** 并点名那 2 个漏列 (证明它抓得到)、补完 README 后应 **PASS**、人为删一行 bullet 应重新 **FAIL** —— 否则就是写了一条恒绿的假绿检查
- 这条落在**主仓** (`.aria/` 是仓本地数据, 不在 plugin 分发件里), 与【1】的 `aria` 子模块是两个提交面
- 复杂度 Level 2, 建议配 `openspec/changes/` 下一份 proposal

**【3】只报告不动手** — 你已拿到全部结论, 我不改任何文件

**【4】自定义** — 例如先只删本地残留的空目录 `aria/skills/session-closeout/`, 或先开 issue 记账、改动排到下个 cycle

**我的建议是【2】**: 单修 README 是修实例, 三个月内它已经因为「新增 skill 时漏改 README」复发两次, 而漏改之所以能活下来完全是因为没有任何机械信号 —— 补上检查才是修这一类。

---

### 两点需要你先拍板

**1. 版本前提**: 你说的 v1.14.0 与仓库实测的 1.69.1 差 55 个 minor, 且「新增 3 个 Skill」与实测「漏列 2 个 (分别在 5 月和 6 月加入)」也对不上。请确认你指的是不是这个 checkout —— 如果是, 那么真正要修的是上面那 2 个漏列, 与任何近期发布无关。

**2. 当前 track 冲突**: 本仓正处在 `a1-entry-claim-duplicate-work-guard` 的 **Phase B.2** (31/40, 0.75h 前刚收尾一次会话), 且检出 `self_multi_container` collision。README 修复是个 disjoint 的小文件域, 但**要不要现在插队**归你定; 若要开做, 进 Phase B 前我会按契约先跑一次 `phase1_gate` advisory 认领。另外最新 handoff §0 第 3 条记着 **Rule #6 AB 仍未跑且不属豁免** (`ARIA_COORDINATION_NO_PUSH` 未设, 会话内补不上) —— 这条与本次 README 改动无关 (无 skill 逻辑变更), 但仍挂在母 Spec 上, 我没有自行豁免它。
