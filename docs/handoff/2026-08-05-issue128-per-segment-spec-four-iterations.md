---
track-id: session-close-20260804-0805-issue128-per-segment-spec
owner-container: simonfish/bfe8285d
phase: session-close
status: done
updated-at: 2026-08-05T02:30:00Z
---

# Aria — Session Handoff (2026-08-05) — #128 逐段判定 spec 四版迭代 + 本地 hook 副本清理

## §0 入口 (新 session 优先读)

- **当前态**: 主仓 `a89d999` / aria `af87cae` (v1.65.5) / standards `2111c84` (v1.1.2) — 三仓双远程 ls-remote 核验一致。active spec 10 / pending_archive 0。
- **本段主线**: aria-plugin **#128** (secret-guard 整命令扫描致复合命令 credit 泄漏) 的 triage + **四版设计 + 三轮五席审计**, spec 已落 v4 **待 R4**; 另落 owner 两项裁定 (性能根治方向 / 本地 hook 副本移除)。
- 🔴 **本段未 ship 任何版本** —— #128 spec 停在 Draft 待 R4, **Phase B 未开始**。
- 🔴 **凭据轮换 hard cap (2026-08-02) 已逾期 3 天**, 第十一次 surface。
- 🔴 **#170 要求 1** (轮换 T4 + revoke `446b79`) 仍未做, 仍阻塞 cesura。

## §1 已完成 (按时间顺序)

1. **triage #128** — confirmed / **critical** / 5-5 复现 ([17512](https://forgejo.10cg.pub/10CG/aria-plugin/issues/128#issuecomment-17512))。`;` `&&` `|` 三种分隔符 + 同族/跨族均可绕过; 定 critical 的核心理由是**它使 #170 的修复在「一次写多个 var」下等于没加**。
2. **发 issue 原文更正** ([17545](https://forgejo.10cg.pub/10CG/aria-plugin/issues/128#issuecomment-17545)) — 我在开 issue 时写的分隔符集合含 `|` 是错的: 管道是 filter 语义载体, 按 `|` 切会毁 13~15 条正确用例 (12 条 pattern 把 `|` 编码进正则本身)。该更正把判级从 Level 3 拉回 Level 2。
3. **owner 裁定一: 移除本仓 `.claude/scripts/` 本地 hook 副本** (主仓 `2890b25`)。诊断依据 SOT §6: secret-guard 副本与 plugin cache **SHA 字节相同** (零定制); secret-scan 副本有**实质代差** (SilkNode v1.2 旧版, 声称能 redact 并打印 `REDACTED N matches`, 而 canonical 已认定 PostToolUse 架构上不能脱敏 —— 旧版的错误声称比不提示更危险)。端到端验证防护零中断。
4. **开 [Aria#172](https://forgejo.10cg.pub/10CG/Aria/issues/172)** — 三副本对比发现 **plugin cache 也停在 1.63.0**, 即 v1.64/v1.65 全部 hook 修复在 Aria 自身运行时**从未生效**。这使**仓内所有 hook dogfood 失真**。
5. **#128 spec 四版迭代 + post_spec R1/R2/R3** (15 份报告入库, 主仓 `a89d999`)。
6. **owner 裁定二: 性能拉回根治** — `has_filter` 13 处 subprocess 转 bash 内建纳入本 spec 范围 (原转出 6), 而非靠判定顺序重排绕开。

## §2 未完成 / Carry-forward

**AI 内省 (load-bearing)**:

- 🔴 **#128 spec 待 R4** — v4 已落盘 (17 条 SC / 10 条 Task / 7 项转出), 但**未经审计**。v4 相对 v3 的新增面 (has_filter 13 处转内建 / 启发式表述 / 判据补漏 `exec` `time` `&` 换行 / 全部 SC 按反事实纪律重写 / 新增 SC-14~SC-17) 都是**没有被任何一轮审计看过的**。
- 🔴🔴 **凭据轮换逾期 3 天** (hard cap 2026-08-02), 第十一次 surface。
- 🔴 **#170 要求 1** 未做, cesura 第 2 段部署仍阻塞。
- **Aria#172 未处理** — plugin cache 更新到 ≥1.65.5 需 owner/环境层操作。**在它解决前, 任何仓内 hook 验收都不可信** (#128 spec 已写死「SC 一律以 canonical 直调为准」)。
- **前序 handoff §6 的 #120 / #117 / #123** 三项跨多个 session 未动。
- **6 项 #170 转出** (aria-plugin#128-132 + Aria#171) 中只有 #128 在推进。

- 🔴 **[收尾机械检查新发现] `silknode-contract-deferral-expiry` 今日到期** — custom checks 由 8/8 转为 **7/8**。这是**设计好的时间驱动 WARN**, 非 bug 非本段引入: `.aria/decisions/2026-05-07-silknode-contract-archive-with-deferred-acceptance.md` 的 `expires_at: 2026-08-05T23:59:59Z` 正是今天, `status: deferred`。该 waiver 覆盖的是 **Contract 2 (业务数据分类约束) 在 M2 从未被机械 enforce**。按决策文件 §70 需 owner 三选一: **关闭 waiver** (acceptance 全 MET) / **续期** (新文件 + 新 expires_at) / **upgrade 至 `standards/governance/silknode-no-storage.md`**。在处置前该 check 会持续红。

**机械补漏**: §2 汇编 186 条 (159 tasks.md + **27 detailed-tasks.yaml** —— 后者仍是 #121 修复在起作用); consistency 10 条 advisory (active change 未入 UPM, 常态)。

## §3 关键风险 / 已知陷阱

- ⚠️ **v4 未经审计, 不可直接进 Phase B**。R1→R3 每一轮都推翻了上一版的核心设计, v4 没理由例外。
- ⚠️ **仓内 hook 行为不可作证据** (Aria#172): harness 跑 1.63.0, canonical 是 1.65.5。做 #128 的任何验证都必须 `bash aria/hooks/secret-guard.sh` 直调。
- ⚠️ **Python 原型正则不可搬进 bash**: `(?:…)` / `\b` / `\s` 在 POSIX ERE 全不支持, 逐字搬运会让 `safe_to_split()` 静默失配 → 退回 v2 的 5/5 误报。已写进 spec §6 + SC-16。
- ⚠️ **fail-safe 判据不封闭**: `exec >/dev/null; …` 无块标记却仍需降级。v4 已把承诺从「保证正确」下调为「启发式」, 残余面归转出 8。新形态出现时应扩充判据表, **不算 SC 失败**。

## §4 实战教训 (memory 沉淀来源)

1. 🔑 **本 cycle 我有 8 条断言被审计方实测推翻, 无一自查发现** —— `&` 可作切分记号 / 「保守不切 = 不会少拦」方向反 / 「切错 = 安全回归」/ 「pattern 匹配已全是 bash 内建」/ 「60ms 是 bash 启动」(实为 jq) / 把已核实的 141 改成 139 / 「只切 `;` `&&` = 最小可靠子集」/ 「判定重排已化解性能矛盾」(只在 benign 负载成立)。**第 6 条尤其值得记: 它是在修正前 5 条的那次重写里新引入的**。→ memory `feedback_never_write_unverified_impossibility_claims` (本段第二次实证)。
2. 🔑 **反事实构造纪律** (R3 tech-lead 教的, 本 cycle 最有价值的方法论产出): 每条新增 SC 都问「假设这机制没实现, 这条断言会变红吗?」不会的换 fixture。它单轮抓出 **8 条恒绿断言**, 含我自称的「核心锚点」SC-6 (12 条里 5 条在恒 fallback 的坏实现下同样全绿) 与 SC-4 (引号盲实现 3/3 仍 exit=2 —— 而 rule6_note 正把 SC-4 当 Rule #6 substitute 证据)。→ memory `feedback_counterfactual_test_for_every_new_sc`。
3. 🔑 **「最小」不等于「可靠」** —— v2 缩到只切 `;` `&&` 自以为是最小可靠子集, 实测 5/5 安全写法误报, 因为这两个记号大量嵌在 bash 块结构里。真正的可靠是**只在能证明正确的场景才改变行为** (v3 的 fail-safe), 而即便如此判据仍不封闭 (v3→v4)。
4. **样本设计决定结论有效性**: 我测性能重排时只覆盖 benign 与「一段命中」, 得出「省 80~86%」; backend 测最坏情况 (每段命中) 得 +102~324%, tech-lead 测 spec 自己推荐的迁移写法得 **+583%**。同一实现三个结论, 差别只在负载。→ v4 的 SC-8 已把四档负载写死。
5. **验证脚本经 `sed` 编辑后必须重读** —— v2 原型被 sed 写坏正则 (损坏部分恰被解析成字符类) 仍输出"全绿", 我干净重写才发现。这是本 cycle **唯一一次自查拦截**。
6. **数字要固化数法而非再猜一个** — 同一语料统计出过五个结果 (68/52/16 · 72/53/19 · 53/17/2 · 65/49/16 ×2), 根因是数法未定义。v4 交付 `corpus_census.py` 权威计数器随 spec 归档。
7. **连续三轮静默丢弃**: R1 的 m-1/m-2/m-3 我连续三轮既不解决也不驳回。R3 tech-lead 建议对每条上轮 finding 强制「解决/转出/驳回+理由」三选一 —— 已在 v4 的转出表落实 (含划掉的第 6 项)。

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| UPM | present, cycle 未配 (10 条 advisory, 常态) |
| OpenSpec | active **10** (+1 本段新增) / pending_archive 0 |
| User Story | 21 (done 17 / in_progress 2 / approved 1 / pending 1), 本段未触碰 |
| PRD | present, 本段未触碰 |

## §6 Next session 入口 + 优先级

1. 🔴🔴 **凭据轮换** — 逾期 3 天, 第十一次 surface。owner 亲自操作。
2. 🔴 **#170 要求 1** (轮换 T4 + revoke `446b79`) — cesura 解阻塞唯一前提。可与第 1 项同批。
3. **[Aria#172](https://forgejo.10cg.pub/10CG/Aria/issues/172) plugin cache 更新** — **优先级高于 #128 继续推进**: 在它解决前, #128 的 Phase B 验收只能靠 canonical 直调, dogfood 一项始终缺失。
4. **#128 spec R4** — v4 待审。重点审 v3→v4 的新增面 (13 处转内建 / 判据补漏 / SC-14~17), 那些没被任何一轮看过。R4 若收敛即可进 Phase B。
5. 🔴 **`silknode-contract-deferral-expiry` waiver 今日到期** (custom checks 8/8 → 7/8) — owner 三选一: 关闭 waiver / 续期 / upgrade 至 `standards/governance/silknode-no-storage.md`。决策依据见 `.aria/decisions/2026-05-07-silknode-contract-archive-with-deferred-acceptance.md`。
6. 承前: #120 / #117 / #123 / #170 其余转出 (#129-132, Aria#171)。

## §7 提交清单

| 仓 | HEAD | origin | github |
|----|------|--------|--------|
| 主仓 Aria | `a89d999` | equal | equal |
| aria | `af87cae` (v1.65.5) | equal | equal |
| standards | `2111c84` (v1.1.2) | equal | equal |
| aria-orchestrator | `86bb684` (detached) | — | 本段未触碰 |

本段提交: `2890b25` (本地 hook 副本移除) + `a89d999` (spec v4 + 15 份审计报告 + triage 产物)。**本段零版本发布**。

custom checks: **7/8** —— 唯一红项 `silknode-contract-deferral-expiry` 为今日到期的时间驱动 WARN (见 §2), 非本段引入。

## §8 Memory entries this session (2 new)

- `feedback_counterfactual_test_for_every_new_sc` (新) — 每条新增 SC 过反事实构造「机制没实现这条会变红吗」; 单轮抓出 8 条恒绿断言。
- `feedback_never_write_unverified_impossibility_claims` (本段第二次实证, 未新建) — 8 条断言被推翻, 含「在修正前 5 条的重写里新引入第 6 条」这一形态。

**本段未落但已有覆盖**: 样本设计决定结论 (并入上条的 How to apply) / sed 破坏验证脚本 (已写进 spec §6, 暂不足以单独成条)。

## Cross-references

- 上一份 session-close: [2026-08-02 #121 ship + #170 四轮审计](./2026-08-02-121-ship-and-170-secret-guard-four-round-audit.md)
- 本段 spec: `openspec/changes/secret-guard-per-segment-evaluation/proposal.md` (v4, Draft 待 R4)
- 审计报告: `.aria/audit-reports/post_spec-R{1,2,3}-*-secret-guard-per-segment-evaluation-*.md` (15 份)
- 权威计数器原型: `scratchpad/authoritative_census.py` (v4 要求交付为 `aria/hooks/tests/corpus_census.py`)
