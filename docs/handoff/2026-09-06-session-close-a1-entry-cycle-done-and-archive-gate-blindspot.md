---
track-id: a1-entry-claim-duplicate-work-guard
owner-container: simonfish/023236f2
phase: D
status: done
updated-at: 2026-09-06T14:42:10Z
---

# Aria — Session Handoff (2026-09-06, session-closer 会话收尾) — 一个 cycle 从 36/40 走完并归档, 路上被三个闸门各拦一次

> **一句话**: 本对话把母 Spec `a1-entry-claim-duplicate-work-guard` 从 **36/40 推到 40/40 并归档**, 期间连发 **aria-plugin v1.71.0 → v1.71.1** 两版, 三仓全部合到 master 并逐 remote 核验。**三个不同的闸门/断言各抓到一次真问题**, 没有一次是事后发现的。
> **本 session 最该记住的一件事**: 我提出的方案两次被 owner 问回来后变得更好 —— 「先修还是先绕」那次, 我列了三个选项并倾向强推归档, owner 一句「遇到问题不应该先修吗」把它扳到正确路径; 事后影响面证明修复只动 19 个 Spec 里的 1 个, 成本远低于我当时的估计。**我倾向低估「修根因」的性价比。**

---

## §0 入口 (新 session 优先读)

1. **cycle 已闭环**: Spec 归档在 `openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/`, claim 已 release (远端实读 `status: done`), 本容器无 active claim。
2. ⚠️ **唯一硬待办: 主仓 `feature/a1-entry-claim-duplicate-work-guard` 未合入 master** —— 本 session 全部产出 (含两次发版) 都在该分支, 已双推核验但未合并。走 C.2 + Rule #8 pre-merge gate。
3. **两个 issue 是本 session 的对外产出**: [aria-plugin#171](https://forgejo.10cg.pub/10CG/aria-plugin/issues/171) (7.6 套件缺口) · [Aria#201](https://forgejo.10cg.pub/10CG/Aria/issues/201) (Archive Tracker, 14 条 unverified claims)。
4. **本 session 承诺过但没做的一件事**: 我说「无论选哪个我都会把闸门缺口开成 issue」—— 结果选了「先修」, 修完就**没开那个 issue**。缺口本身已消, 但「同类注册面还有没有别的漏网」这个问题没人跟踪。见 §2 H2。
5. 周期维度的收尾另有一份: [2026-09-06-a1-entry-shipped-v1.71.0-and-gate-fix-v1.71.1-archived.md](./2026-09-06-a1-entry-shipped-v1.71.0-and-gate-fix-v1.71.1-archived.md) (phase-d-closer D.3 产出)。本份是**会话维度**, 覆盖面更广 (含 heartbeat 恢复、env 溯源、方法论层教训)。
6. 硬约束不变: 禁带圈数字 (memory `no-tiny-glyphs`)。

---

## §1 已完成 (本对话, UTC)

| 时段 | 事项 |
|---|---|
| 05:5x–07:4x | `/state-scanner` 两次; 查明 heartbeat 刷不了是 `ARIA_COORDINATION_NO_PUSH=1` 会话级前置; **进程树溯源**确认它只来自命令行前缀 (profile / settings.json 均无) ⇒ 建议 `claude --resume` 不带前缀重启, 兼得上下文与干净 env |
| 07:4x | 重启后 env 三级全清; fetch (纯 FF 已验) → **heartbeat 刷新** `push_skipped:false`, 远端实读核验; 本地 master FF 20 commit |
| 08:2x | **8.1** aria CHANGELOG + 版本 SOT 5 文件 (当时定 1.70.0) |
| 08:3x | **8.4 条款 1 拦下撞车** —— 同伴轨 08:27:19Z 抢先合并并 tag v1.70.0; 按 Spec「落地时按 plugin.json 计算」重算 **1.71.0** |
| 09:xx | 合 aria master 进 feature: 5 处冲突 (三处代码冲突全是「双方各加一个新函数位置相撞」⇒ 两存) + **四处无冲突标记的静默错误合并** |
| 10:xx | **8.4** 本地 merge → aria master `985e629` + tag `v1.71.0` + 双推 + 四项 × 两 remote 核验 |
| 11:xx | **8.2** 主仓 16 处版本点 (14 + Spec 清单漏列的 2 处架构文档) + gitlink |
| 11:4x | **standards 收口** (合 master → 本地 merge → `21748d4` → 双推核验) + 主仓 gitlink bump |
| 12:0x | **7.6 开单** aria-plugin#171 (查重发现 Spec 未记的同族 #157) ⇒ **40/40** |
| 12:1x | Phase D: D.1 skip / D.post skip / **D.2 BLOCK** |
| 13:xx | 闸门盲点定位 → owner 裁「先修」→ 影响面基线 19 Spec → 改前必红测试 → 修复 → 只动 1 条 → **v1.71.1** ship |
| 14:xx | D.2 重跑放行 → 归档 + 14 条 unverified_claims 入 frontmatter → D.2b release → Aria#201 → D.4 estimator (618 turns / 4.51M / 8.5h) |
| 14:3x | 会话收尾: 内省 + 机械兜底交叉核验 + memory ×2 + 本 doc |

---

## §2 未完成 / Carry-forward

### 高优先级

| # | 项目 | 状态 |
|---|---|---|
| **H1** | **主仓 feature 分支合入 master** —— 本 session 全部产出所在 | 待做, 走 C.2 + Rule #8 |
| **H2** | **闸门注册面缺口的类级排查** —— 我承诺开 issue 未开。`_is_hooks_or_config_path` 只认 `hooks.json`/`.aria/config.json`, 新加了 `.aria/state-checks.yaml`; **还有没有别的「声明式注册 + 运行时真执行」的面没被认?** 这是 memory `fix-the-class` 的形状 | **未做 (承诺过)** |
| **H3** | **24 条 AB 缺陷开单** (`DEFECTS.md`), A 节四条「断言奖励错误行为」优先 | 本 session 提了 4 次都被挤掉 |

### 中优先级

| # | 项目 |
|---|---|
| M1 | `issue_scan.open_count` 静默截断 (每仓截在 `limit`=20; 实测 47 报 vs 74 真) —— 两次扫描都报了, 仍未开单 |
| M2 | **openspec-archive SKILL.md 两处漂移**: (a) Step 3 写调 `openspec` CLI, 但该 CLI **未安装**且本仓 143 次归档实际全走 `git mv`; (b) SHA 占位行文案 SKILL.md 写 `Step2` 而实际 `d_payload` 是 `Step 7`, **逐字匹配静默落空** (本次实撞) |
| M3 | `aria/README.md` skill 名册漏 `issue-triage` / `session-closer`, 无机械检查覆盖名册 |
| M4 | root `VERSION` standards v2.2.3 vs `standards/openspec/project.md` 2.2.2 |
| M5 | `.aria/config.json` 的 `coordination` 是 `state_scanner` 下嵌套键, 顶层读得 `None` |
| M6 | 上轮原样: Aria#192 真修 / Aria#182 类级修 / `.aria/repro/` 测试不在 gate 路径 / aria-plugin#169 (`resilient_push`) 未修 |
| M7 | `aria-orchestrator` 指针全程 dirty (他轨 `feature/m6-cost-model-telemetry`) —— 本 session 从未处置, 也**未向 owner 确认归属**, 只是每次都当「范围外」带过 |

### 机械补漏 (autofill backstop)

- **backstop 对本轨零发现** —— `unfinished` 132 条全部来自他轨 M6/M7 spec, a1-entry 零条 (已归档)。
- `sync` **零告警**, 三仓两端全 equal (`aria-orchestrator` 的 `github=unknown` 是该分支 github 上不存在, 非分叉)。
- `consistency_check` 6 条 `active_change_not_in_upm` 是 UPM 未配置的恒亮 advisory (Aria#188), 从 7 降到 6 = 本轨归档了。
- **补漏方向是反的**: 我内省出的 7 条线程机械侧**一条都看不见** (全是对话层)。这次 backstop 没兜到东西, 但它证实了「我没漏 repo 层的」。

---

## §3 关键风险 / 已知陷阱

1. **⚠️ 归档闸门的修复是自证循环形状** —— 改的是 D.2 闸门自己, 改完拿它归档触发它的那个 cycle。缓解两项独立证据: (a) **先写改前必红的测试再改代码** (基线三态 2 红 2 绿 → 4 绿); (b) **19 个 Spec 改前/改后对跑, 只动 1 条**。两项都不是「闸门说绿了」。
2. **合并版本文件时最危险的是没有冲突标记的那几个。** 双方都把 `1.69.1` 改成**同一个字符串** `1.70.0` ⇒ git 判零冲突静默采纳。CHANGELOG/VERSION 因文案不同正常报冲突, 而四个纯版本串文件一声不吭。已落 memory `same-value-merge-silent`。
3. **断言必须钉「本次」而非「存在」。** `git merge -F -` (stdin) 不被支持 ⇒ exit 129 ⇒ 合并根本没发生; 而当时打印的双父是**上游那个既有 merge commit 的**。Spec 里「断言本次新 merge commit 而非既有双父」那句救的。已落 memory `assert-this-action`。
4. **核验脚本自己会是 bug。** `ls-remote --tags <remote> <pattern>` 带 pattern **不返回 `^{}` 解引用行** ⇒ 核验腿恒空报 ❌。**拿已存在的 v1.70.0 做对照**证伪 (它在同形式下也取空) 才判定是检查坏了不是推送坏了。
5. **测试夹具不忠实 = 零复现力。** 闸门测试首版红在 `ambiguous` 而非 `dead` (stub 不含符号名, 走不到「有 Python 定义」支)。**两天前 json-branch 测试 docstring 里记的同款坑, 那条注释救了这次。**
6. **查重要拉全量。** `issue_scan` 每仓截在 20; 开单前拉全 42 条逐条看才发现 Spec 裁量里没有的同族 `#157`。
7. **`--heartbeat-only` 只存在于当时的在制代码** —— 已安装插件与 aria master 都没有。修复前若照 SKILL.md 直接调会失败; 我是先 grep 三处版本确认才跑的。这类「文档写的能力尚未 ship」在自举项目里会反复出现。

---

## §4 实战教训 (memory 沉淀来源)

```
[已写入 memory, 本 session 新增 2 条]
- same-value-merge-silent — 并发两侧改成同一个串 ⇒ git 零冲突零标记静默采纳;
  版本号/常量类合并后不问「有没有冲突」而问「这值现在该是什么」
- assert-this-action — 验「动作发生了」须钉本次新产生的对象而非「该状态存在」;
  上游遗留同形状物会让根本没执行的动作假绿

[候选 memory, 未写]
- 新写的核验脚本先在「已知为真」的对象上跑对照组。ls-remote --tags 带 pattern 不返回 ^{}
  行, 差点被读成推送失败; 拿已存在的 tag 做对照才分辨出是检查坏了。
  建议 type: feedback (check-runs-at-baseline-first 的「对照组」具体形态)
- 遇到闸门 block, 判据不是「绕过成本低不低」而是「闸门判错了什么」——
  按自己规则判对了但规则漏了一个面 ⇒ 修规则; 判对了而人类另有决定 ⇒ 逃生舱。
  建议 type: feedback

[未写下经验]
- **我倾向低估「修根因」的性价比。** 提三个选项时我把「先修」标成「要走 Spec 走审计, 是独立
  cycle 的量」, owner 一句「遇到问题不应该先修吗」问回来后, 我才去核先例 —— 发现两天前同一
  文件同一函数刚以 Level 1 出过货 (v1.69.1 c98646e)。**先例是我自己能查的, 但我先给了估计
  再去查证。** 正确顺序是先查执行史再估成本 (memory spec-precedent-verify-execution-history
  讲的是引先例要核验, 这里是更前一步: 估成本前就该去查)。
- 承诺的跟踪动作要当场落地。「无论选哪个都会开 issue」说完就被后续步骤冲掉了 (§2 H2)。
```

---

## §5 多维度同步状态

| 维度 | 涉及 | 状态 |
|---|---|---|
| UPM | no | 未配置 ⇒ 6 条 `active_change_not_in_upm` 恒亮 advisory (Aria#188) |
| User Stories | no | 21 条无变更 (done 17 / in_progress 2 / approved 1 / pending 1) |
| OpenSpec | **yes** | 活跃 7 → **6** (本轨归档); pending_archive 0 |
| PRD | no | 无变更 |
| Standards | **yes** | `session-handoff.md` §2.3.8.1 已 ship, master `21748d4` |
| Skill docs | **yes** | `phase-a-planner` / `spec-drafter` A.1 认领段 + `state-scanner` heartbeat 段, 随 v1.71.0 ship |
| Auto-memory | **yes** | **+2** (索引 24510 字节, 腾位移 2 条窄指针入 archive) |
| Decision memos | no | owner 裁定走对话, 未单独立决策单 |
| Audit reports | no | D.post config 显式 off |
| CHANGELOG | **yes** | v1.71.0 + v1.71.1 两条 |

---

## §6 Next session 入口 + 优先级建议

```bash
/aria:state-scanner
```

1. **`{id: carry-a1-entry-branch-merge, desc: 主仓 feature 分支合入 master, 走 C.2 + Rule #8 pre-merge gate}`** —— 本 session 全部产出所在, 已双推未合并。**类型: 集成 · 估时 1-2h**
2. **`{id: carry-gate-registration-surface-class-sweep, desc: 闸门注册面缺口的类级排查 + 开 issue}`** —— §2 H2, 我承诺了没做。判据「还有没有别的『声明式注册 + 运行时真执行』的面没被 `_is_hooks_or_config_path` 认」。**类型: 类级修复 · 估时 1-2h**
3. **`{id: carry-ab-suite-defects-24, desc: DEFECTS.md 24 条开单, A 节四条优先}`** —— 连续三个 session 被挤掉。**类型: 质量债 · 估时 2-3h**
4. **`{id: carry-archive-skill-drift, desc: openspec-archive SKILL.md 两处与实现漂移}`** —— §2 M2。**类型: 文档/代码同步 · 估时 1h**

---

## §7 提交清单 (multi-remote parity)

| 仓 | ref | SHA | origin | github |
|---|---|---|---|---|
| Aria (主) | `feature/a1-entry-claim-duplicate-work-guard` | 见本 doc 收尾 commit | 待推 | 待推 |
| aria-plugin | **master** + tag `v1.71.0` | `985e629` | ✅ MATCH | ✅ MATCH |
| aria-plugin | **master** + tag `v1.71.1` | `301641b` | ✅ MATCH | ✅ MATCH |
| aria-standards | **master** | `21748d4` | ✅ MATCH | ✅ MATCH |

本 session 所有 push 均逐 remote `ls-remote` 独立取 SHA 核验 (master / tag 对象 / tag 解引用 / feature 四项), **未信 push 回执** (硬约束 2); 子模块合并一律**本地** `git merge`, 未用 Forgejo 服务端合并 (硬约束 1)。autofill `sync` 段零告警。

---

## §8 Memory entries this session (2 new)

- `feedback_same_value_concurrent_edit_merges_silently.md` (type: feedback) — 索引别名 `same-value-merge-silent`
- `feedback_assertion_must_pin_this_action_not_state.md` (type: feedback) — 索引别名 `assert-this-action`

索引腾位: `feedback_cross_agent_verdict_independent_verify` 与 `feedback_owner_invoked_convergence_loop` 两条窄指针移入 `MEMORY-archive.md` (**fact 文件仍在 memory/ 目录, 移出索引 ≠ 删除**)。索引 24324 → 24510 字节 (上限 24576)。

§4 另有 2 条候选 + 2 条未写下经验待固化。

---

## Cross-references

- 周期维度收尾 (同日, phase-d-closer D.3): [2026-09-06-a1-entry-shipped-v1.71.0-and-gate-fix-v1.71.1-archived.md](./2026-09-06-a1-entry-shipped-v1.71.0-and-gate-fix-v1.71.1-archived.md)
- 前一份会话收尾: [2026-09-06-0015-rule6-ab-shipped-36of40-and-24-suite-defects.md](./2026-09-06-0015-rule6-ab-shipped-36of40-and-24-suite-defects.md)
- 归档产物: `openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/`
- 本 session 开的 issue: [aria-plugin#171](https://forgejo.10cg.pub/10CG/aria-plugin/issues/171) · [Aria#201](https://forgejo.10cg.pub/10CG/Aria/issues/201)
- 版本史 SOT: `aria/CHANGELOG.md` (v1.71.0 / v1.71.1)
