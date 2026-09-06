---
track-id: a1-entry-claim-duplicate-work-guard
owner-container: simonfish/023236f2
phase: D
status: done
updated-at: 2026-09-06T14:28:26Z
---

# Aria — Cycle Handoff (2026-09-06, phase-d-closer 周期收尾) — a1-entry 母 Spec 40/40 ship + 归档; 顺带修掉归档闸门一个误报

> **一句话**: 母 Spec `a1-entry-claim-duplicate-work-guard` 从 36/40 走到 **40/40 并归档** —— 8.1/8.4/8.2 发版三步 + 7.6 开单 (aria-plugin#171); 中途 **v1.70.0 号被同伴轨抢走**, 按 Spec「落地时按 plugin.json 计算」重算为 **v1.71.0**; 收尾时 D.2 闸门 **BLOCK**, 查明是 `.aria/state-checks.yaml` 未被认作运行时调用面的**闸门盲点**, 按 owner 决定「先修再归档」以 **v1.71.1** ship 修复后归档成功。
> **本 cycle 最该记住的一件事**: 三个不同的闸门/断言在这一天各抓到一次真问题 —— **8.4 条款 1** 抓到版本号撞车, **条款 2 的「本次而非既有双父」断言** 抓到一次根本没发生的合并, **D.2 C-gate** 抓到自己的白名单缺口。都不是事后发现的, 是被机制当场拦下的。

---

## §0 入口 (新 session 优先读)

1. **本 cycle 已闭环, 无待办。** Spec 归档在 `openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/`; claim 已 release (远端实读 `status: done`)。
2. **两个 issue 是本 cycle 产出的对外待办**: [aria-plugin#171](https://forgejo.10cg.pub/10CG/aria-plugin/issues/171) (套件缺口, 7.6 交付物) 与 [Aria#201](https://forgejo.10cg.pub/10CG/Aria/issues/201) (Archive Tracker, 14 条 unverified claims 兜底)。
3. **aria-plugin 连发两版**: v1.71.0 (母 Spec) → v1.71.1 (闸门修复)。主仓发布同步面两次都做全 (16 处版本点 + gitlink)。
4. ⚠️ **主仓 `feature/a1-entry-claim-duplicate-work-guard` 分支尚未合入 master** —— 本 cycle 全部工作都在该分支上, 已双推核验。合并归 C.2 (Rule #8 pre-merge gate)。
5. `git status` 只剩 `M aria-orchestrator` (他轨 `feature/m6-cost-model-telemetry`, 非本 Spec)。
6. 硬约束不变: 禁带圈数字 (memory `no-tiny-glyphs`)。

---

## §1 已完成 (按时间顺序, UTC)

| 时间 | 事项 |
|---|---|
| 07:4x | owner 以**不带** `ARIA_COORDINATION_NO_PUSH` 的 `claude --resume` 重启 (env 溯源确认只来自命令行前缀); heartbeat 刷新 `push_skipped:false`, 远端实读核验 |
| 08:0x | 本地 `master` 788fac8 → 8e3d9dc FF; 发现同伴轨 `owner-container-identity-key-and-collision-parser` 活跃 |
| 08:2x | **8.1** aria CHANGELOG + 版本 SOT 5 文件 (当时定 1.70.0) |
| 08:3x | **8.4 条款 1 拦下撞车**: 同伴轨 08:27:19Z 抢先合并并 tag **v1.70.0**; 按 Spec 重算为 **1.71.0** |
| 09:xx | 合 aria master 进 feature (5 处冲突, 三处代码冲突全是「双方各加一新函数位置相撞」⇒ 两存); **另修四处无冲突标记的静默错误合并** |
| 10:xx | **8.4** 本地 merge → aria master `985e629` + tag `v1.71.0` + 双推 + 四项 × 两 remote `ls-remote` 核验 |
| 11:xx | **8.2** 主仓 16 处版本点 + gitlink; **另补 2 处 Spec 清单漏列的架构文档版本行** |
| 11:4x | standards 收口 (合 master → 本地 merge → master `21748d4` → 双推核验) + 主仓 gitlink bump |
| 12:0x | **7.6** 开单 aria-plugin#171 (查重发现 Spec 未记的同族 #157); **40/40** |
| 12:1x | Phase D: D.1 skip (无 UPM) / D.post skip (config off) / **D.2 BLOCK** |
| 13:xx | 闸门盲点定位 → 影响面基线 (19 Spec) → 改前必红测试 → 修复 → **只有 1 条变** → v1.71.1 ship |
| 14:xx | D.2 重跑 `verdict=warn` 放行 → 归档 + frontmatter 14 条 unverified_claims → D.2b claim release → Step 7 tracker Aria#201 → D.4 estimator |

---

## §2 未完成 / Carry-forward 清单

### 本 cycle 无待办

母 Spec 40/40 已归档, claim 已释放。以下是**移交给 issue 的**, 不占 carry-forward:

| 去处 | 内容 |
|---|---|
| [aria-plugin#171](https://forgejo.10cg.pub/10CG/aria-plugin/issues/171) | `phase-a-planner` / `spec-drafter` 套件零覆盖 A.1 入口认领编排行为 (7.6 交付物) |
| [Aria#201](https://forgejo.10cg.pub/10CG/Aria/issues/201) | Archive Tracker — 14 条 unverified claims (静态不可核验, 非未完成任务; `deferred_items=0`) |

### 中优先级 (跨 cycle, 原样承接上一份 handoff)

| # | 项目 |
|---|---|
| M1 | **开 24 条 AB 缺陷 issue** (`ab-results/2026-09-05-.../DEFECTS.md`) —— A 节四条「断言奖励错误行为」会持续污染后续所有 AB |
| M2 | `issue_scan.open_count` 静默截断 (每仓截在 `limit`=20; 实测 47 报 vs 74 真) —— 仍未开单 |
| M3 | `aria/README.md` skill 名册漏 `issue-triage` / `session-closer`, 无机械检查覆盖名册 |
| M4 | root `VERSION` standards v2.2.3 vs `standards/openspec/project.md` 2.2.2 —— 记了待裁但无机械检查 |
| M5 | `.aria/config.json` 的 `coordination` 是 `state_scanner` 下嵌套键, 顶层读得 `None` |
| M6 | 上轮原样: Aria#192 真修 / Aria#182 类级修 / `.aria/repro/` 测试不在 gate 路径 / aria-plugin#169 (`resilient_push`) 未修 |
| **M7** | **新**: `openspec` CLI 未安装 —— 本仓 143 次归档实际全走 `git mv` (同伴今天 `62de051` 亦然)。openspec-archive SKILL.md 的 Step 3 写的是调 CLI, 与实际执行史不符, 值得对齐 |
| **M8** | **新**: openspec-archive SKILL.md 引的 SHA 占位行文案是 `由 openspec-archive Step2 归档提交后填入`, 实际 `d_payload.body` 里是 `Step 7`。逐字匹配会**静默落空** (本次实撞, 已按实际文案填) |

---

## §3 关键风险 / 已知陷阱

1. **⚠️ 归档闸门的修复是「自证循环」形状** —— 改的是 D.2 闸门自己, 改完拿它归档触发它的那个 cycle。缓解已做: **先写改前必红的测试再改代码** (基线三态亲跑 2 红 2 绿 → 4 绿), 使「闸门变绿」有独立证据而非「改到它绿」(memory `author-to-match-checker`)。另做 19 个 Spec 的改前/改后对跑, **只有 1 条 block→warn, 其余 18 条逐字不变** —— 这是「白名单遗漏而非判据变更」的承重证据。
2. **合并版本文件时最危险的是「没有冲突标记」的那几个。** 本次 `plugin.json` / `marketplace.json` ×2 / `VERSION:3` / `README.md:5` 四处, 双方都把 `1.69.1` 改成了**同一个字符串** `1.70.0`, git 判定「两边改成一样」直接采纳、零冲突标记。不专门复核就会把一个**已发布的版本号**带进 tag。CHANGELOG/VERSION 那两处反而因为文案不同而正常报冲突。
3. **闸门断言必须钉「本次」而非「存在」。** 8.4 条款 2 明写「断言的是本次新 merge commit, 而非既有的双父」。本次 `git merge -F -` (stdin) 不被支持、exit 129、合并根本没发生, 而当时打印的双父是**对方那个既有 merge commit** 的 —— 断言若写成「有双父就算过」, 这一步会假绿通过。
4. **检查脚本自己会是 bug。** `ls-remote --tags <remote> <pattern>` **带 pattern 时不返回 `^{}` 解引用行**, 导致 tag 解引用核验腿恒空报 ❌。用**已存在的 v1.70.0 做对照**证伪 (它在同形式下也取空) 才判定是检查坏了而非推送坏了。
5. **测试夹具不忠实 = 零复现力。** 新写的闸门测试首版红在 `ambiguous` 而非 `dead` —— stub 不含符号名, 走不到「有 Python 定义」那支。与两天前 json-branch 测试 docstring 里记的是同一个坑, **那条注释救了这次**。
6. **查重要拉全量, 不能只信 snapshot。** `issue_scan` 每仓截断在 20 条; 7.6 开单前拉全 42 条逐条看, 才发现 Spec 裁量记述里没有的同族 `#157`。

---

## §4 实战教训 (memory 沉淀来源)

```
[候选 memory]
- 「双方改成同一个值」在 git 里是零冲突, 不产生任何标记。版本号/常量类文件在并发 ship 场景下
  必须专门复核, 不能依赖冲突标记来发现问题。本次四处静默合成了一个已发布的版本号。
  建议 type: feedback (与 false-green 同族, 但机制是 git 的合并语义而非检查器)
- 闸门/断言必须钉「本次动作」而非「状态存在」。写成「有双父就算过」的断言, 会被一次
  根本没发生的合并骗过 —— 因为上游那个既有 merge commit 天然就有双父。
  建议 type: feedback (与 completion_signals_vs_runtime_invocation 同族的时序变体)
- 新写的核验脚本要先在「已知为真」的对象上跑一遍。`ls-remote --tags <remote> <pattern>`
  带 pattern 不返回 ^{} 行, 差点被读成推送失败; 拿已存在的 tag 做对照才分辨出是检查坏了。
  建议 type: feedback (check-runs-at-baseline-first 的一个具体形态: 用已知真值做对照组)
- 「先修还是先绕」: 遇到闸门 block 时, 判据不是「绕过成本低不低」, 而是「闸门判错了什么」——
  它按自己的规则判对了但规则漏了一个注册面 ⇒ 修规则; 它判对了而人类另有决定 ⇒ 逃生舱。
  本次是前者, owner 选了先修, 事后影响面证明只动 1/19。
  建议 type: feedback
```

---

## §5 多维度同步状态

| 维度 | 涉及 | 状态 | 备注 |
|---|---|---|---|
| UPM | no | 未配置 | D.1 skip; 恒亮 `active_change_not_in_upm` advisory (Aria#188) |
| User Stories | no | 无变更 | — |
| OpenSpec | **yes** | **已归档** | `openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/`; frontmatter 含 14 条 `unverified_claims` + `unverified_ack: false` |
| PRD | no | 无变更 | — |
| Standards | **yes** | 已 ship | `conventions/session-handoff.md` §2.3.8.1 `id` 行补 A.1 认领口径; master `21748d4` |
| Skill docs | **yes** | 已 ship | `phase-a-planner` / `spec-drafter` 各加「前置: REQUIRE claim (A.1, MUST)」; `state-scanner` 加 A.1 heartbeat 集成段 |
| Auto-memory | no | 0 new | §4 候选 4 条待固化 |
| Decision memos | no | — | 本 cycle 的 owner 裁定走对话, 未单独立决策单 |
| Audit reports | no | — | D.post `post_closure` config 显式 off (豁免白名单第 1 类) |
| CHANGELOG | **yes** | v1.71.0 + v1.71.1 | 两条独立条目 |

---

## §6 Next session 入口 + 优先级建议

```bash
/aria:state-scanner
```

1. **`{id: carry-a1-entry-branch-merge, desc: 把 feature/a1-entry-claim-duplicate-work-guard 合进主仓 master}`** —— 本 cycle 全部产出都在该分支 (已双推核验), 尚未合入。走 C.2 + Rule #8 pre-merge gate。**类型: 集成 · 估时 1-2h**
2. **`{id: carry-ab-suite-defects-24, desc: DEFECTS.md 24 条开单, A 节四条「断言奖励错误行为」优先}`** —— 会持续污染后续所有 AB。**类型: 质量债 · 估时 2-3h**
3. **`{id: carry-archive-skill-drift, desc: openspec-archive SKILL.md 与实现的两处漂移}`** —— §2 的 M7 (Step 3 写调 CLI 但实际全走 git mv) + M8 (SHA 占位行文案 Step2 vs Step 7, 逐字匹配静默落空)。**类型: 文档/代码同步 · 估时 1h**

---

## §7 提交清单 (multi-remote parity)

| 仓 | ref | SHA | origin | github |
|---|---|---|---|---|
| Aria (主) | `feature/a1-entry-claim-duplicate-work-guard` | 见收尾 commit | 待本 handoff 提交后推 | 同 |
| aria-plugin | **master** + tag `v1.71.0` | `985e629` | ✅ MATCH | ✅ MATCH |
| aria-plugin | **master** + tag `v1.71.1` | `301641b` | ✅ MATCH | ✅ MATCH |
| aria-standards | **master** | `21748d4` | ✅ MATCH | ✅ MATCH |

全部 push 后逐 remote `ls-remote` 独立取 SHA 比对 (master / tag 对象 / tag 解引用 / feature 四项), 未信 push 回执 (CLAUDE.md 硬约束 2)。子模块合并一律本地 `git merge`, 未用 Forgejo 服务端合并 (硬约束 1)。

---

## §8 Memory entries this session (0 new)

本 cycle 未写新 memory (预算给了执行与核验)。§4 的 4 条候选待固化 —— 其中「双方改成同值 = 零冲突」与「断言钉本次而非存在」两条最值得写。

---

## Cross-references

- 前一份 handoff: [2026-09-06-0015-rule6-ab-shipped-36of40-and-24-suite-defects.md](./2026-09-06-0015-rule6-ab-shipped-36of40-and-24-suite-defects.md) (AB 会话, 本 cycle 的上半程)
- 归档产物: `openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/`
- Archive Tracker: [Aria#201](https://forgejo.10cg.pub/10CG/Aria/issues/201) | 套件缺口: [aria-plugin#171](https://forgejo.10cg.pub/10CG/aria-plugin/issues/171)
- AB 总账: `aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/RESULT.md`
- 版本史 SOT: `aria/CHANGELOG.md` (v1.71.0 / v1.71.1 两条)
