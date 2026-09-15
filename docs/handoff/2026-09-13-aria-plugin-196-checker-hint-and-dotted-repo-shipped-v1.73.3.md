---
track-id: aria-plugin-196-bare-issue-refs-msg-and-dotted-repo
owner-container: simonfish/bfe8285d
phase: D
status: done
updated-at: 2026-09-13T15:20:00Z
---

# Aria — Cycle Handoff (2026-09-13) — 10CG/aria-plugin#196 插件侧收口: 检查器报错指向 §4.4 + 放行带 `.` 的仓名, 发 v1.73.3 (Level 1, track 终结)

> **一句话**: `/aria:state-scanner` 推荐项 1 (唯一不依赖 owner、不撞双子星的 carry 项) → `check_bare_issue_refs.py` 两件: (1) 有违规时打印规范指引, 指到 `standards/conventions/content-integrity.md` §4.4; (2) 全限定引用的仓名允许带 `.` (`10CG/10cg.local#40` 不再误报), 单级路径伪装靠封闭扩展名集仍拒 → 发 **aria-plugin v1.73.3** (顺带收入 `308ccce` / `fcbc8ac` 两个未发版纯注释合并) → `10CG/aria-plugin#196` 关单, claim 释放。
>
> **本段最该记住的**: 这个 cycle 没有新教训, 只是把上一份 handoff 的 carry 项照单做完。三处 AI 流程判断 (Level 1 / Rule #6 substitute / 扩展名封闭集) 列在 §2 H1 请 owner 复议。

> **Next session 入口**: 优先读本 doc → `/aria:state-scanner` → §6

---

## §0 入口 (新 session 优先读)

1. 运行 `/aria:state-scanner`。主仓 `1b9734a`; aria `1cb3872` (tag `v1.73.3`); standards `8b49562`; aria-orchestrator `237045a`; 四仓 origin / github 两端 `ls-remote` 一致。custom checks 15/16 pass, 唯一 FAIL = `plugin-cache-currency` STALE (本机装的插件 1.73.2 < SOT 1.73.3, 第 1 层 marketplace clone 滞后) —— 装机侧动作, 见 §2 H2。
2. 10CG/aria-plugin#196 已关。`check_bare_issue_refs.py` 仍是**手动自检工具, 不是闸门** (owner 09-13 裁定); Spec 不得把「整份文件 rc 0」写成验收门槛。
3. 10CG/Aria#195 / 10CG/Aria#199 两条 L2 轨在 `simonfish/023236f2` 手上 (A.2 active), 本容器不碰。双子星发版时按 `plugin.json` 当前 1.73.3 取下一个 MINOR, 即 **v1.74.0**。

---

## §1 已完成 (2026-09-13, 按顺序, UTC)

| 时间 | 事件 | 证据 |
|---|---|---|
| 14:15 | `/aria:state-scanner` scan.py exit 0; 工作树干净, collision kind=none, 本容器无 active claim (心跳不触发); 推荐 3 项, owner 选 1 | `.aria/state-snapshot.json` |
| 14:49 | A.1 入口认领 `phase1_gate --phase A.1 --linked-issue 10CG/aria-plugin#196`, `outcome=passed`, `linked_issue_overlap=[]`, push ok | 协调 ref |
| — | recon: 读 10CG/aria-plugin#196 原文 + owner 09-13 裁定评论 (修法 B, 暂不注册闸门, 只剩报错文案一件) + 上一份 handoff 追加的第二件 (带 `.` 仓名误报); 实跑复现: `10CG/10cg.local#40` 被判裸引用 rc=1 | scratchpad |
| — | 基线: state-scanner 1599 全绿。写 6 条测试, 旧代码 **3 红** (带 `.` 仓名放行 / 放行区间只覆盖自己 / 违规输出含规范指引) **+ 3 护栏绿** (含 `10cg.local.md` 变体的单级路径伪装仍拒 / 两级路径仍拒 / 零违规无指引) | `tests/test_check_bare_issue_refs.py` |
| — | 修脚本: `QUALIFIED` repo 段允许 `.` + 命名捕获; `FILE_EXTENSIONS` 封闭集 + `_is_path_disguise`; `CONVENTION_HINT` 只在 total>0 时打印。22/22 绿; `content-integrity.md` 自扫仍 rc 0; 最新 handoff 实扫 33 → 19 (少掉的 14 条全是 `10cg.local` 引用) | aria `94b2a44` |
| — | 全量 harness `skills/run_all_tests.sh`: 7 OK / 0 FAIL / 4 SKIP (未装 pytest), 2003 → 2009; state-scanner 1599 → 1605 | — |
| — | 版本 bump 5 文件 + CHANGELOG [1.73.3] `9003a82` → 分支推 origin → C.2.4 gate **green** (`not_applicable`: 改动文件无 CI workflow 覆盖, PR CI wait 跳过; main 无 in-flight) → 本地 `--no-ff` merge `1cb3872` + annotated tag `v1.73.3` → aria 双推, master 与 tag 两端 MATCH `1cb3872` | aria `1cb3872` |
| — | 主仓 gitlink `fcbc8ac→1cb3872` + 15 个版本点 (CLAUDE.md ×2 / 四语种 README badge+版本行 / 三份 i18n `translated-from` 标记 / 两份架构文档) `1b9734a` → C.2.4.5 submodule gate PASS (aria forward bump, mode=block) → 双推两端 MATCH `1b9734a`; 重扫 custom checks 版本类全 OK | 主仓 `1b9734a` |
| — | 10CG/aria-plugin#196 回帖 (comment 23857) + 关闭; claim 释放 `done` (push ok) | Forgejo |

外向动作 (回帖 + 关单) 是 owner 选项 1 里明示的「做完关单」, 也是 owner 09-13 裁定评论的原话。所有 push 均对 origin / github 逐一 `ls-remote` 比对。

**Cycles shipped this session**: 1 (aria-plugin v1.73.3)

---

## §2 未完成 / Carry-forward 清单

### 高优先级 (需要 owner)

| # | 项 | 说明 | 来源 |
|---|---|---|---|
| H1 | **复议本 cycle 三处 AI 流程判断 (Rule #10)** | (a) 按 **Level 1** (无 OpenSpec) 处理: 理由是两件都是 owner 已裁定修法下的实现收口, 无需求变更; (b) **Rule #6 走 substitute** 而非 AB: 脚本是 deterministic 手动自检工具, 不在任何 SKILL.md 指令面, description 未动; (c) 放行带 `.` 仓名的实现选择 = **封闭扩展名集** `FILE_EXTENSIONS` (md/py/yaml/json/sh 等 30 个) —— 未列的扩展名会被当仓名放行, 这是 fail-CLOSED 面上唯一的让步; 备选是只放白名单仓名 (更严, 但采用方每个带 `.` 的仓都要登记)。三处任一改判, 本容器按裁定回改 | 本 cycle |
| H2 | 装机侧刷新插件缓存 | `/plugin marketplace update 10CG-aria-plugin` → `/plugin update aria@10CG-aria-plugin` → **重启 session**; 之后 `plugin-cache-currency` 应 OK。这是 slash 命令, AI 在 session 内做不了 | custom check |
| H3 | 承前: 复议上一批两处 AI 流程判断 | 10CG/aria-plugin#197 按 Level 1 + 修法 A; 两处 standards 改动未起 OpenSpec (上上份 handoff §2 H3) | 承前 |

### 中优先级

- 10CG/aria-plugin#198 (Status 括号内旧状态参与归类) 待方案; 10CG/aria-plugin#182 截断证据未回帖 —— 均承前。
- `10CG/10cg.local#40` / `10CG/Aether#404` 结论出来后, 本机按结论改 `~/.ssh/config` 并清 `known_hosts` 里的 `.212` —— 承前。
- 新到两条 Aria issue 无人认领: `10CG/Aria#212` (openspec CLI 口径) / `10CG/Aria#211` (AB 臂直接喂 SKILL.md, description 变动的 AB 触发面被绕过)。10CG/Aria#211 直接质疑 Rule #6 AB 的有效性, 建议先 triage。

### 低优先级 / cleanup

- 存量文档里剩下的裸 `#n` 文内编号按 §4.4 执行口径「改到哪段顺手改哪段」, 不批量回改。

### 机械补漏 (autofill backstop)

- `unfinished` 全部来自 M6/M7 六份 spec 的 `tasks.md`, 属各自轨 (门在 owner / 基建), 分布与前几份 handoff 相同。
- consistency: 8 条 `active_change_not_in_upm` advisory (本仓无运行时 UPM, 已知恒出)。
- sync: 零告警; `overall_parity=true`。

---

## §3 关键风险 / 已知陷阱

| 风险 | 触发条件 | 缓解 |
|---|---|---|
| 带 `.` 的单级路径伪装用了 `FILE_EXTENSIONS` 之外的扩展名 (如 `a/b.tsx#3`) 会被当仓名放行 | 文档里出现这种写法 | 撞到就把扩展名加进封闭集 (脚本注释已写明这是唯一扩展点); H1(c) 若改判白名单仓名则此风险消失 |
| 双子星发版取号 | 它走到 Phase C | 按 `plugin.json` 当前 1.73.3 算下一个 MINOR = v1.74.0; bump 前 `ls-remote --tags` 两端 |
| 本机插件缓存落后 SOT, 新报错文案 / 带 `.` 仓名放行在本机仍是旧行为 | 直到 H2 做完 | 用 `python3 aria/skills/state-scanner/scripts/check_bare_issue_refs.py` (子模块路径) 自检即为新版 |

---

## §4 实战教训 (memory 沉淀来源)

- 无新教训。本 cycle 全程照既有 memory 走: 先 fetch + 读并发轨 handoff 再起活; 红测试先于修复 (反事实 3 红 3 绿); 每次 push 后逐 remote `ls-remote`; 写「已完成」前实跑 (自扫 33→19、harness 2009)。

[候选 memory]
- 无。

[未写下经验]
- 无。

---

## §5 多维度同步状态

| 维度 | 本段涉及? | 状态 | 备注 |
|---|---|---|---|
| UPM | no | — | 本仓无运行时 UPM |
| User Stories | no | — | — |
| OpenSpec | no | — | Level 1, 无 spec |
| Standards / conventions | no | — | §4.4 上一 session 已落, 本 cycle 只消费 |
| Skill docs | yes | ✅ | 脚本 docstring 同步 (豁免 (a) 的判据措辞); 无 SKILL.md 变动 |
| CHANGELOG | yes | ✅ | aria `CHANGELOG.md` [1.73.3] (含收入 `308ccce` / `fcbc8ac`) |
| Issues | yes | ✅ | `10CG/aria-plugin#196` closed (comment 23857) |
| Auto-memory | no | — | 无新条目 |

---

## §6 Next session 入口 + 优先级建议

```
/aria:state-scanner
```

1. **`{id: carry-owner-review-cycle-judgments-196}`** owner 复议 §2 H1 三处判断; 任一改判本容器回改。
2. **`{id: carry-plugin-cache-refresh-1733}`** 装机侧 `/plugin marketplace update` + `/plugin update` + 重启 (§2 H2)。
3. **`{id: carry-triage-aria-211-212}`** triage `10CG/Aria#211` (优先, 关乎 Rule #6 AB 有效性) 与 `10CG/Aria#212`。
4. **`{id: carry-aria-plugin-198-status-paren}`** 等方案定了再修 10CG/aria-plugin#198 (承前)。
5. **`{id: carry-vip-199-followup}`** `10CG/10cg.local#40` / `10CG/Aether#404` 结论后改本机 ssh 配置 (承前)。

**不应该做的**:
- 不碰 10CG/Aria#195 / 10CG/Aria#199 (claim 在 `simonfish/023236f2`)。
- 不动 5 个 design_deferred 的 M6/M7 spec (门在 owner / 基建)。

---

## §7 提交清单 (commit hash + multi-remote parity)

```
[aria]              fcbc8ac → 94b2a44 (fix) → 9003a82 (bump) → 1cb3872 (merge, tag v1.73.3) | origin = github ✅
[main]              94293de → 1b9734a (gitlink + 15 版本点) (+ 本 handoff 提交)                | origin = github ✅
[standards]         8b49562 (未动)                                                              | origin = github ✅
[aria-orchestrator] 237045a (未动)                                                              | origin = github ✅
```

**Tags published**: aria-plugin `v1.73.3` (annotated, 两端一致)
**Issues**: `10CG/aria-plugin#196` closed (comment 23857)
**Gates**: C.2.4 green (`not_applicable`, main in-flight clear) · C.2.4.5 PASS (aria forward bump, mode=block) · claim acquire/release 均 push ok

---

## §8 Memory entries this session

无新增 / 无追记。

---

## Cross-references

- issue: [10CG/aria-plugin#196](https://forgejo.10cg.pub/10CG/aria-plugin/issues/196)
- 规范: `standards/conventions/content-integrity.md` §4.4「Issue / PR 引用写法」
- 前序 handoff: [2026-09-13 会话收尾第三次](./2026-09-13-session-close-vip-199-routed-to-10cglocal-and-aether.md) · [2026-09-13 会话收尾第二次 (10CG/aria-plugin#196 规范落地)](./2026-09-13-session-close-issue-ref-and-plain-numbering-conventions.md) · [2026-09-13 v1.73.2 发版](./2026-09-13-aria-plugin-197-coordination-fetch-shipped-v1.73.2.md)

---

**Created**: 2026-09-13
**Status**: Done — track 终结; 后续只剩 owner 复议 (§2 H1) 与装机侧刷新 (§2 H2)
