---
track-id: session-close-20260802-121-ship-170-secret-guard
owner-container: simonfish/bfe8285d
phase: session-close
status: done
updated-at: 2026-08-02T16:30:00Z
---

# Aria — Session Handoff (2026-08-02) — #121 完整 ship + #170 secret-guard 四轮审计 cycle

## §0 入口 (新 session 优先读)

- **当前态**: 主仓 `db2e983` / aria `af87cae` (**v1.65.5**) / standards `2111c84` (**secret-hygiene v1.1.2**) — 三仓双远程 ls-remote 核验一致。custom checks **8/8**。active spec 9 / pending_archive 0。工作区 clean。
- **本段两条主线**: (1) aria-plugin **#121** 从 triage 走完整十步循环 ship **v1.65.1**; (2) Aria **#170** (T4 凭据泄漏) triage → 目标重定向 → post_spec **R1→R4** → ship **v1.65.4/v1.65.5 + standards v1.1.1/v1.1.2**, 并转出 6 项 issue。
- **本段最值得读的一段**: §4 实战教训第 1 条 —— 一个 cycle 内**三次「未实测即断言」全部由审计方推翻, 无一自查发现**。
- 🔴 **凭据轮换 hard cap = 今天 (2026-08-02) 已到期**, 第十次 surface, 仍未做。且 #170 要求 1 (轮换 T4 + revoke `446b79`) **仍阻塞 cesura 第 2 段部署**。两者都是 owner 亲自操作项。
- **同日并列轨**: 本文件是 2026-08-02 第二份 handoff。并发轨 (`phase-c-integrator-ci-path-coverage`) 的 [双 Spec 碰撞事后勘误](./2026-08-02-dual-spec-collision-postmortem-and-shipped-defects.md) 同日先写。**两轨零冲突** (本轨改 hooks + standards, 对方改 phase-c-integrator + spike), 但**版本号撞过车**, 见 §3。

## §1 已完成 (按时间顺序)

1. **`/state-scanner` 开局** — 工作区 clean, parity 全绿, 8/8 checks; 按前序 handoff §6 优先级选定 #121。
2. **aria-plugin #121 完整 cycle → v1.65.1** (`52d6f22`):
   - triage **confirmed** (repro 2/2, severity major, [comment 17136](https://forgejo.10cg.pub/10CG/aria-plugin/issues/121#issuecomment-17136)) — `handoff_autofill.py::grep_unchecked_tasks` 只扫 `tasks.md`, yaml-only spec 报 0 未完成 (#113 同根因**跨 skill 第四处**消费方)。
   - owner 判级 Level 2 → spec `session-closer-autofill-yaml-datasource` → post_spec **R1→R3 CONVERGED** (R1 4/5 独立命中同一洞: `parse_ok=False` 静默 0) → owner 签字。
   - 实施: 复用 #113 parser SOT, **importlib 文件直载**替代 sys.path (R2 证 sys.path 方案有残余顺序风险) + 三形态 sentinel + open-attempt 存在性语义。SC-1~SC-9 (baseline-failing 已验), session-closer 50 + state-scanner 1322 全绿。
   - ship + 归档 + claim 释放 + #121 closed + follow-up [aria-plugin#123](https://forgejo.10cg.pub/10CG/aria-plugin/issues/123) (proposal-inline 第三形态)。
3. **Aria #170 triage → 两次自我更正**:
   - 首轮 verdict `partial-repro` ([17187](https://forgejo.10cg.pub/10CG/Aria/issues/170#issuecomment-17187))。
   - **更正 1** ([17269](https://forgejo.10cg.pub/10CG/Aria/issues/170#issuecomment-17269)): 核 Nomad 官方 API 文档后确认 `PUT /v1/var/` response body **含解密 `Items`** ⇒ 无 redirect 的写向 PUT 确实回显, **拦它是正确的** ⇒ issue 要求 2 (读写分离) 前提**整个证伪**, 零代码改动。我此前把 issue 的前提当事实用了。
   - 真 gap 另在: `nomad var put` **零 pattern 覆盖**, 而它在 stdout 非 TTY 时 (Bash 工具恒真) `-out` 默认切 `json`, 渲染含解密 `Items` 的完整变量到 **stdout** (issue 原文归因 stderr, 不符 — stderr 是 `-verbose` 档)。
4. **转交 aether** ([aether-plugin#11](https://forgejo.10cg.pub/10CG/aether-plugin/issues/11)) — **没照抄要求 3**: 核实现行 skill (`SKILL.md:216`) 用的是 `curl PUT` 而非 `nomad var put`, 且该形态实测不被 secret-guard 拦 ⇒ 原建议前提不成立。转过去的是修正后的知识 (`-out` 非 TTY 切 json 的坑 + `-out=none` 正解)。
5. **#170 spec `secret-guard-nomad-var-put-echo` → post_spec R1→R4** (20 份报告):
   - R1 `1C+13M+21m` → 大改 → R2 `4C+13M+24m` (严重度**未降**) → **owner 裁定缩到最小范围** → R3 `3C+15M+15m` → R4 `0C+8M+18m` (2 PASS + 3 REVISE) → 收尾编辑 → ship。
   - R1/R2 我各提一版豁免设计 (全局 credit → pattern 作用域), **两版都被实测推翻**, 且 347 条全量回归对两次退化**都全绿**。
6. **ship v1.65.4** (`183836b`) + **standards v1.1.1** (`7e2b48c`) co-land: 一条 pattern (带尾边界) + 零新增豁免 + 测试 347→366 (7 条 baseline-failing); SOT 4 个推荐位订正 + 两段警示。
7. **收尾补丁 v1.65.5** (`af87cae`) + **standards v1.1.2** (`2111c84`): 陈旧计数同步 (`~50 cases` → 366; SOT 208/251 → 366)。
8. **6 项转出立案** + **#170 进展 comment** ([17404](https://forgejo.10cg.pub/10CG/Aria/issues/170#issuecomment-17404), **不关闭**) + rule6_note 按 owner 裁定统一为 substitute 框定 (`db2e983`)。

## §2 未完成 / Carry-forward 清单

**AI 内省 (load-bearing)**:

- 🔴🔴 **凭据轮换 — hard cap 今天已过期, 第十次 surface**: `FORGEJO_TOKEN` / `NEXUS_API_TOKEN` / `CF_ACCESS_CLIENT_SECRET`。owner 亲自操作项, 本段 owner 全程选了其他工作。**逾期后果仍未成文**。
- 🔴 **#170 要求 1 未做**: 轮换 T4 (`aria-build-bot-2026-Q3`) + revoke 已泄漏 PAT `446b79`。**仍阻塞 cesura 第 2 段部署** —— retention GC 代码已 ship 未部署, job/cache 表 + host-vol spilled 文件持续增长。**#170 因此保持 open**, 是否拆独立 issue 跟踪由 owner 定。
- **6 项新转出全部未排期**: [aria-plugin#128](https://forgejo.10cg.pub/10CG/aria-plugin/issues/128) (架构: 整命令扫描致复合命令 credit 泄漏, **本 spec 唯一交付物在最常见的批量写形态下等于没加**) / [#129](https://forgejo.10cg.pub/10CG/aria-plugin/issues/129) (stderr 假阴家族 + `2>&1` 顺序陷阱) / [#130](https://forgejo.10cg.pub/10CG/aria-plugin/issues/130) (`guard:ack` 文案实现不符) / [#131](https://forgejo.10cg.pub/10CG/aria-plugin/issues/131) (尾边界 + FP 面, severity 已升中) / [#132](https://forgejo.10cg.pub/10CG/aria-plugin/issues/132) (per-pattern 提示) / [Aria#171](https://forgejo.10cg.pub/10CG/Aria/issues/171) (CLI 输出随 TTY 变化的通用 convention)。
- **前序 handoff §6 的第 2/3 项仍未动**: **#120** (yaml-only C-gate liveness parity, Level 2 倾向) / **#117** (AB 套件缺 authoring 维度 — 上上个 session 说要「带上 AB 新佐证回帖」, **跨两个 session 仍未做**)。
- **[aria-plugin#123](https://forgejo.10cg.pub/10CG/aria-plugin/issues/123)** (#121 让渡的 proposal-inline 第三形态) 未排期。
- **aether-plugin#11** 转交后无跟进 (等 aether 侧响应)。
- **rule6_note 框定裁决已落但未回填其他 spec**: owner 定的 substitute 框定只改了本 spec, 若其他 hook 类 spec 有同类混用未清查。

**机械补漏 (snapshot 有但 AI 内省未提)**:

- **§2 机械汇编 186 条未完成任务**, 其中 **27 条来自 `detailed-tasks.yaml`** —— ⚖️ **这正是本段修的 #121 在本次收尾里兑现**: 修之前这 27 条结构上不可见 (报 0)。meta-dogfood 当场生效。
- consistency_check **9 条 advisory** (`active_change_not_in_upm`): 9 个 active spec 全部未列入 UPM in-progress。属常态 flag (UPM 未配 cycle), 非本段引入。
- `aria-orchestrator` 子模块 detached (`86bb684`), origin parity `unknown` — 长期状态, 本段未触碰。

## §3 关键风险 / 已知陷阱

- ⚠️ **本 spec 是部分覆盖, 不要表述为「`put` 已受保护」**: secret-guard 全部判定都是整命令字符串扫描, 复合命令中任一段携带 redirect 即全段放行。`nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2` 的第二段零保护 —— 而那正是 #170 的泄漏形态。已用 `KNOWN-LIMIT` 用例锁定现状 (转红 = #128 已收口)。
- ⚠️ **本 spec 主推的安全出路 `>/dev/null` 自身有洞**: `nomad var put -verbose … >/dev/null` 实测放行, 但 `-verbose` 按 nomad 设计走 stderr。SOT 已补警示 (须 `>/dev/null 2>&1`, **且顺序敏感** —— `2>&1 >/dev/null` 无效且 hook 放行), hook 侧未收口 (#129)。
- ⚠️ **并发版本号撞车**: 推送时发现并发轨已 ship v1.65.2 + v1.65.3 (#124/#125/#126), 我的 1.65.2 顺延至 **1.65.4**。两轨改动面零重叠, rebase 后双方测试均绿 (366/366 + 40/40)。**下次 bump 前先 fetch**。
- ⚠️ **SSH 瞬断两次** (10cg.local #20 同族): standards push github 撞 `kex_exchange_identification`; 主仓 ls-remote 返回空。**两次都靠重试确认不是分叉** —— 单次 ls-remote 失败不可当分叉证据 (CLAUDE.md 多远程约束 2 已成文, 本段第二次实战兑现)。
- ⚠️ **secret-guard FP 面在本段命中 5 次**: 读 `--help` ×2 / 审计 agent 测试命令 / 写文档时 heredoc 内引用命令文本 / grep 搜索词含该串。**讨论这个 hook 本身就会被这个 hook 拦** —— 下个 session 若要动 #129/#131, 预期会反复撞到; 逃生门 `# guard:ack:` 的**理由首词须 ≥8 连续非空白字符** (否则静默失效, 见 #130)。

## §4 实战教训 (memory 沉淀来源)

1. 🔑 **一个 cycle 内三次「未实测即断言」, 全部由审计方实跑推翻, 无一自查发现** —— (a)「六形态无假阴无假阳」→ `curl -v … >/dev/null` 就是假阴; (b) 采信 `-out=keys` 为合法安全写法 (继承自 issue + 审计方 finding) → 实机核验该 flag 值**不存在**; (c)「SC-3/SC-4 不可兼得」→ 实测放宽字符类即可兼得。第 (c) 条最贵: 它写在**专门用来修正前一次事实错误的段落里**, 且是 spec 归档后关于「为什么边界只能这样」的唯一记载。→ memory `feedback_never_write_unverified_impossibility_claims`。
2. 🔑 **Rule #7 SOT 自身教了一条跑不通的命令, 且是双重错误** —— 4 个推荐位教 `nomad var get -out=keys`, 而 (a) 该 flag 值在 nomad 三个子命令上都不存在; (b) 即便合法, 原写法的 `2>/dev/null` 也会被同一套规范配的 hook 拦掉。后果与该规范要防的事故**同构**: 照做连撞两次失败 → 转向不安全替代 (正是 #170 第 2→3 环)。→ memory `feedback_sot_example_commands_are_never_executed`。
3. 🔑 **我在 R3 审计进行中改了审计对象**, 导致五个并行 agent 读到不同版本: 一位据旧版报了假 finding (R4 自行撤回), 另一位察觉 mtime 变化后按新版复核才没出错。「审计只审不改」有个对偶面 —— **主 loop 也不得在轮次进行中改**。→ 更新 memory `feedback_audit_workflow_land_edits_between_rounds` (加第 4 条)。
4. **严重度不降 = 该换方向而不是加轮**: R1→R2 严重度未降 (1C→2C 去重后), 说明我在同一个结构性假设上反复栽 —— owner 裁定缩范围后, R3/R4 的问题性质才从「设计缺陷」降到「逐字文本」。**两版豁免设计被推翻时 347 条回归都全绿**, 说明测试集对该维度结构上无鉴别力, 这本身是继续加轮无用的信号。
5. **审计方的 finding 也需自验**: R1 tech-lead 的 M-1 (`get -out=keys` 被拦 = 事故成因同构) 是错的 —— 它只测了 hook 没核 CLI, 而我**忠实继承**了这个错误写进 spec, 直到 R2 才被同一个 agent 自己纠正并认领。
6. **陈旧计数会跨文档传染**: `secret-guard.test.sh` 头注释 `~50 cases` 让本 spec R1 把基线记成 ~50 (实为 347); SOT 里 208/251 同样陈旧。已全部同步为 366 并加「保持同步」提醒。
7. **meta-dogfood 当场兑现**: 本段修的 #121 (yaml-only carry-forward) 在**本次收尾的 §2 机械汇编里**直接生效 —— 27 条 yaml 来源任务从不可见变为可见。

## §5 多维度同步状态

| 维度 | 状态 | 备注 |
|------|------|------|
| **UPM** | present, cycle 未配 | 9 个 active change 均未列入 UPM in-progress (9 条 advisory flag, 常态) |
| **OpenSpec** | active 9 / pending_archive **0** | 本段归档 2 个 (`2026-08-01-session-closer-autofill-yaml-datasource` + `2026-08-02-secret-guard-nomad-var-put-echo`) |
| **User Story** | 21 (done 17 / in_progress 2 / approved 1 / pending 1) | 本段未触碰 |
| **PRD** | present | 本段未触碰 |

一致性 flag: 9 条 `active_change_not_in_upm` (advisory, 非本段引入)。

## §6 Next session 入口 + 优先级

1. 🔴🔴 **凭据轮换 — hard cap 已过期 (2026-08-02 = 今天)**, 第十次 surface。owner 亲自操作。
2. 🔴 **#170 要求 1** — 轮换 T4 + revoke `446b79`, **cesura 解阻塞的唯一前提**。可与第 1 项同批处理。
3. **新转出六项**里优先级最高的是 [#128](https://forgejo.10cg.pub/10CG/aria-plugin/issues/128) (架构面) —— 它决定 #170 的修复是否真正有效 (当前批量写形态零保护)。#129 (stderr 假阴) 次之, 因为它使本 spec 主推的出路有洞。
4. **承前未动**: #120 (Level 2 倾向) → #117 (**跨两 session 未回帖**, 带 AB 新佐证) → #123。
5. 被动等待: aether-plugin#11 / #165 收窗 (orchestrator 合并) / `_open_question_no_ci_fallback` (owner)。
6. 承前 owner 门: #168 / #169 / M6 四门 + 168h / M7 fleet。

## §7 提交清单 (commit hash + multi-remote parity)

| 仓 | HEAD | origin | github |
|----|------|--------|--------|
| 主仓 Aria | `db2e983` | equal | equal |
| aria (v1.65.5) | `af87cae` | equal | equal |
| standards (secret-hygiene v1.1.2) | `2111c84` | equal | equal |
| aria-orchestrator | `86bb684` (detached) | unknown | — (本段未触碰) |

本段 ship: aria-plugin **v1.65.1** (`52d6f22`) → **v1.65.4** (`183836b`) → **v1.65.5** (`af87cae`); standards **v1.1.1** → **v1.1.2** (`2111c84`)。claim: 2 acquire / 2 release, 零残留。

## §8 Memory entries this session (2 new + 1 updated)

**已落**:
- `feedback_never_write_unverified_impossibility_claims` (新) — 事实断言尤其「不可能/不可兼得」写进 spec 前必实跑; 继承自上游与审计方的断言同样要自验。
- `feedback_sot_example_commands_are_never_executed` (新) — conventions/SOT 的示例命令大概率从未实跑; 规范判据对 ≠ 示例可执行, 安全类尤其致命。
- `feedback_audit_workflow_land_edits_between_rounds` (更新, 加第 4 条) — 「审计只审不改」的对偶: 主 loop 也不得在轮次进行中改审计对象。

**本段未落 (已有覆盖并实景应用)**: 并发版本撞车 rebase (`feedback_concurrent_sot_conflict_mechanical_resolve`) / ls-remote 重试纪律 (CLAUDE.md 多远程约束 2 已成文, 本段第二次兑现) / meta-dogfood (`feedback_meta_dogfood_solution_validates_self_mid_ship`) / 修复自身重开同类缺陷 (`feedback_multiround_audit_catches_fix_introduced_regression`, 本段第 (c) 条断言即是)。

## Cross-references

- 上一份 session-close: [2026-08-01 triage-修复列车 + #122 not_applicable](./2026-08-01-triage-fix-train-and-122-not-applicable-ship.md)
- 同日并发轨 (先写): [2026-08-02 双 Spec 碰撞事后勘误](./2026-08-02-dual-spec-collision-postmortem-and-shipped-defects.md)
- 本段归档 spec: `openspec/archive/2026-08-01-session-closer-autofill-yaml-datasource/` + `openspec/archive/2026-08-02-secret-guard-nomad-var-put-echo/`
- 审计报告: `.aria/audit-reports/post_spec-R{1,2,3}-*-session-closer-autofill-yaml-datasource-*.md` (15 份) + `post_spec-R{1,2,3,4}-*-secret-guard-nomad-var-put-echo-*.md` (20 份)
