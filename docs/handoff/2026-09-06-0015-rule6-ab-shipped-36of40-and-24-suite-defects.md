---
track-id: a1-entry-claim-duplicate-work-guard
owner-container: simonfish/023236f2
phase: B.2
status: active
updated-at: 2026-09-06T06:43:46Z
---

# Aria — Session Handoff (2026-09-06, 会话收尾) — Rule #6 AB 跑完 36/40, 并挖出 24 条套件/评测台缺陷

> **一句话**: owner 以 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启 → 前置三项实测通过 → **6 套件 / 31 eval / 66 臂 / 67 份评分**全跑完 → **定向 fixture with 45/45 vs old 16/45 (delta +0.644)** → 中途按预注册规则补了一次指令面缺陷 (纯增 +16/−0, 不改断言) → 7.1–7.5 回写 **31/40 → 36/40**。
> **本 session 最该记住的一件事**: 跑分只有**定向 fixture 那 45 条**有效度。110 条回归断言里大面积恒真, 且**四处方向性错误** —— 其中两处把 Aria 自己推崇的行为判成失败 (**拒绝虚构进度记录得 0/3, 编造记录得 3/3**; **拒绝拿别的套件顶替验证得低分**)。**照这个分数优化会把技能改坏。**

---

## §0 入口 (新 session 优先读)

1. **AB 已完成, 不必重跑。** 全部产物在 `aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/` —— 先读 `RESULT.md` (137 行总账), 再按需看 `SCORES.md` (脚本汇总) / `DEFECTS.md` (24 条)。
2. **母 Spec 36/40**, 只剩 **7.6 开单** + **8.1/8.2/8.4 发版** (`<vNEXT>` = **1.70.0**, 执行序 8.1 → 8.4 → 8.2)。
3. **7.6 的依赖已解除** (7.5 跑完了), 且本次攒了 24 条素材 —— 但开单是**外向动作待授权**。
4. ⚠️ **heartbeat 待刷**: 上次刷是 `2026-09-05T21:40:06Z`, **sweep 死线 2026-09-06T21:40Z**。上一会话带 `NO_PUSH=1` 故意没刷 (刷了只写本地, 下次 fetch 会冲掉)。**下一个不带该 env 的会话第一件事就刷它。**
5. 三仓 feature 分支**都已推且两端 MATCH** (主仓 `5d9b568` / aria `ab3dbd0` / standards `bb5d375`); 三个子模块指针仍**有意** dirty (gitlink bump 归 8.2)。
6. 硬约束不变: 禁带圈数字 (memory `no-tiny-glyphs`)。

---

## §1 已完成 (本对话, UTC)

| 时间 | 事项 |
|---|---|
| 22:37 | 会话以 `NO_PUSH=1` resume。前置三项实测: env SET 且值 truthy · 子进程 `no_push_requested_by_env()==True` · 协调 ref 基线 `539d231` local==remote |
| 22:4x | old 臂快照 (aria master `7dd0135`) 建立并逐文件核验 `==old ∧ !=with`; 六份 `PREDICTION.md` 派臂前写死 |
| 23:0x–00:0x | 66 臂 + 67 份评分跑完 (含 eval 3 三轮复跑 6 臂) |
| 23:2x | **发现指令面缺陷并补丁**: `proposal.md:277` 成文要求两个 SKILL.md 都漏抄; `spec-drafter` 整段 overlap 分档缺失 (`:668`)。纯增 +4/+12, CRLF 保持, **断言未动**。因果证据 `10CG/Aria#174` 出现 0→6, eval 4 5/6→6/6 |
| 23:3x | 两次「疑似回归」用多样本排除 (见 §3) |
| 00:0x | 手册三条隔离验收全过; 强制清理 `+` fetch 执行 |
| 00:1x | `RESULT.md` / `SCORES.md` / `DEFECTS.md` 落盘; 7.1–7.5 回写 **36/40**; 本 doc |

---

## §2 未完成 / Carry-forward

### 高优先级 — 本 cycle 剩 4 条

| # | 项目 | 状态 |
|---|---|---|
| **H1** | **7.6 套件缺口 issue** (aria-plugin) —— 依赖已解除, 素材充足 (24 条) | **外向待授权** |
| **H2** | **8.1** CHANGELOG + 版本 SOT 5 文件 (`<vNEXT>` = 1.70.0, MINOR) | 待做 |
| **H3** | **8.4** aria 本地 merge → master + 双推 + 逐 remote `ls-remote` 核验 + tag (CLAUDE.md 硬约束 1/2 宿主) | 待做, **在 8.2 之前** |
| **H4** | **8.2** 主仓 16 版本点 + gitlink bump | 待做 |

### 中优先级

| # | 项目 |
|---|---|
| M1 | **开 24 条缺陷 issue** (`DEFECTS.md`) —— A 节四条「奖励错误行为」最高优先级, **会持续污染后续所有 AB** |
| M2 | `issue_scan.open_count` 静默截断 —— 本次实测 **47 报 vs 74 真** (吞 36%), 被丢的恰含 `aria-plugin#110/#135/#107/#109`、`Aria#136`(secret 泄漏)。仍未开单 |
| M3 | `aria/README.md` skill 名册漏 `issue-triage` / `session-closer` (数量对 42, 列表只有 40), **无机械检查覆盖名册**, 漂移活过三个月 |
| M4 | root `VERSION:25` standards **v2.2.3** vs `standards/openspec/project.md:3` **2.2.2** —— `version-management.md §5.1` 记了待裁但无机械检查 |
| M5 | `.aria/config.json` 的 `coordination` 是 `state_scanner` 下**嵌套键**, 顶层读得 `None` ⇒ 静默误判「闸门未启用」 |
| M6 | 上轮原样: Aria#192 真修 / Aria#182 类级修 / `.aria/repro/` 测试不在 gate 路径 / aria-plugin#169 (resilient_push) 未修 |
| M7 | `constants.py:44-52` 用现在时引用**尚未 ship** 的 A.1 heartbeat 集成 (aria `master` / plugin 1.69.1 均无该段) —— 8.1 落版时裁「改条件式 vs ship 后即真」。详见 §3 第 8 条 |
| M8 | 清 `aria/aria-plugin-benchmarks/ab-workspace/…` **6.4MB / 424 文件**未跟踪残留 (写错 cwd, 未被 gitignore 覆盖)。详见 §3 第 9 条 |

### 机械补漏 (autofill backstop)

- **backstop 抓到一条真缺口**: 7.1–7.5 跑完但未回写 tasks.md —— 已在本 session 末补 (31/40 → **36/40**)。这正是 backstop 的价值所在。
- `sync` **零告警**, 三仓两端全 equal。`consistency_check` 7 条 `active_change_not_in_upm` 是 UPM 未配置的恒亮 advisory (Aria#188)。

---

## §3 关键风险 / 已知陷阱

1. **⛔ 只有定向 fixture 的 45 条有效度。** 回归臂 85/110 vs 82/110 (+0.027) **不可**读作「新版略好」, 也不可读作「已验证无回归」。四处方向性错误见 `DEFECTS.md` A 节 —— 尤其 `phase-d-closer` eval 1 **给虚构打满分**、`phase-b-developer` eval 2 **罚拒绝假绿**。
2. **「无回归」的证据来源是手工比对, 不是断言。** 五 eval 输出特征横向对照 + eval 3 七样本 (目标区块 with 0/4 · old 1/4)。**「没检出」≠「已验证」**, 这句写死在 `SCORES.md`。
3. **我在同一天两次拿 n=1 报「回归」**, 第二次是在已写下「单次不足以定性」之后。真正救回来的是我**重复派发的意外**制造了第二样本。判据已硬化: **任何跨臂差异, n≥3 之前一律标「未定」, 不进结论段、不报 owner**。
4. **一处单侧承重污染**: `phase-b-developer` eval 2 的 with 臂 3:1 建立在读仓内 Spec 挑替身任务上 ⇒ 该分差不得计为区分力。其余为对称的 handoff/快照通道泄漏。
5. **语料泄漏第三通道**: `.aria/state-snapshot.json` 的 `openspec.raw_status` **内嵌 proposal 的 Status 行**, 而读快照是 Step 0 硬性要求 ⇒ **躲不开**。
6. **评测台并发写竞争**: `scan.py` 用 `Path.write_text` 非原子写 630KB 到固定路径, 20+ 并发臂互相截断。本次中途加隔离条款 (改写各臂 `outputs/`), 零损害 —— **下次跑之前先确认该条款在 ARM 指令里**。
7. **单个臂能吃光全局 subagent 配额**: `phase-a-planner` eval 1 的 with 臂真跑了 post_spec 3 轮 × 5 席, **自己撞 20 上限**; old 臂 65 分钟 / 40.6 万 token。跑这条时不要并发别的。
8. **`SWEEP_TTL` 的 24h 理据引用了尚未 ship 的机制, 而 30min 那条阈值本 doc 从没写过。** 两个阈值语义不同 (`aria/skills/state-scanner/lib/constants.py:28-58` + `lib/gc.py:341/355` 实测): `STALE_TTL` = 1800s (30min) 只标「可接管」, advisory 且下次读即可逆; `SWEEP_TTL` = 86400s (24h) 才是 `sweep_stale_active` **持久改写** `status=abandoned` 的那条, 注释明写「受害方无恢复路径」。§0 第 4 条与 §6 第 1 条都只记了 24h ⇒ **抢占风险的实际起点比死线早 23.5 小时**: 本轨 heartbeat 停在 `2026-09-05T21:40:06Z`, 自 **22:10Z** 起在别的 session 的 track board 上就已渲染 🔴「abandoned? 可接管」。
   更麻烦的是 `constants.py:44-52` 用**现在时**为 24h 辩护 ——「the AI orchestration layer **now** refreshes on every `/state-scanner` entry via `phase1_gate.py --heartbeat-only` (see `state-scanner/SKILL.md`「Layer L A.1 heartbeat 集成」)」, 并据此宣称「frozen heartbeat」前提已消解。**三处实测**: 该 SKILL.md 段只存在于 feature 分支 `ab3dbd0`, **aria `master` 0 命中, 已安装 plugin cache 1.69.1 也没有** (全文仅 2 处 heartbeat, 均非 A.1 入口)。⇒ 对每个跑**已发布**插件的会话 —— 含 2026-09-06 06:0x 这次 `/state-scanner` —— 那前提**依然成立**, 扫描入口不会自动刷心跳。随 v1.70.0 ship 即自动变真; **8.1 落版时需 owner 裁一句: 改成条件式措辞, 还是判「ship 后即真, 不改」**。形状同 memory `delegate-verify` (注释按未来时态写成了现在时)。
9. **AB 臂按错 cwd 把 6.4MB 工作区产物写进了 `aria` 子模块。** `aria/aria-plugin-benchmarks/ab-workspace/2026-09-05-a1-entry-rule6/skill-snapshot/`, **424 个文件**, `git status` 里是 `??` 且**未被 `.gitignore` 覆盖** —— 正确位置是仓根的 `aria-plugin-benchmarks/`。下次在 `aria` 里 `git add -A` 会把它误提交进插件仓。清理前已核: `ab-results/` 里该留的产物确实已落在主仓 `7542485`, 删这个残留不丢东西。

---

## §4 实战教训 (memory 沉淀来源)

```
[候选 memory]
- 跨臂/跨样本差异在 n≥3 之前一律标「未定」, 不进结论段、不报 owner。同一天两次拿 n=1 报「回归」,
  第二次还是在写下「单次不足以定性」之后 —— 不是没有规则, 是规则没被挂到手上这件事上。
  建议 type: feedback (与 cite≠apply 同族, 但给出可执行阈值)
- **断言可以奖励错误行为**, 这比恒真更危险。四个实例: 拒绝虚构得 0/编造得满分 · 拒绝假绿被罚 ·
  按现行设计做对了扣分 · 闯闸照跑仍满分。判据: 写断言时问「一个按我们方法论做对的臂, 会不会因此扣分?」
  建议 type: feedback (与 false-green-dual-is-permanent-red 同族的第三种形态: 反向激励)
- 「跑分」与「有效度」必须分开呈现。本次若只报合计 +0.206, 会把无效度的 110 条混进结论。
  正确做法是分组报 + 逐组标效度。建议 type: feedback
- 并发多臂跑同一技能时, 技能若写仓内固定路径产物 (非原子写), 臂之间会互相截断。
  评测台须在指令层强制「产物落各臂自己的 outputs/」。建议 type: reference (AB 运维)

[未写下经验]
- 重复派发是本 session 数据完整性的唯一威胁源 (4 个臂被重派, 2 份 grading 评了已被覆盖的答卷)。
  防线应是派发前查 DONE_ARMS 清单, 但我是事后才建的。下次跑多臂 AB 前先建清单。
- 「grader 提的疑虑要不要采信」这次有两个反例: 一个 grader 说 old 快照含目标行为 ⇒ 对照失效 (核实是它误判,
  那节来自更早的 Spec); 另一个 grader 主动说自己的判定是边界判定、换标尺结论会翻。
  ⇒ 判据不是「grader 说的对不对」, 是「它给没给可核验的依据」。值得单独成条但本次没写。
```

---

## §5 多维度同步状态

| 维度 | 状态 |
|---|---|
| OpenSpec | `a1-entry-claim-duplicate-work-guard` **36/40** (7.1–7.5 本 session 回写), 仍 active |
| UPM | 未配置 ⇒ 7 条 `active_change_not_in_upm` 恒亮 advisory (Aria#188) |
| User Story / PRD / 架构 | 本 cycle 无变更 (发版时 8.2 会动 16 版本点) |
| 同步 | 三仓 feature 分支两端全 **equal**, 零告警 |
| 协调 ref | `539d231` **全程纹丝未动**; 66 臂无一调 `phase1_gate` |

---

## §6 Next session 入口 + 优先级建议

```bash
/aria:state-scanner
```

1. ⭐ **先刷 heartbeat** (若本会话不带 `NO_PUSH`): `git fetch origin '+refs/aria/coordination:refs/aria/coordination'` 然后 `phase1_gate.py --raw-track-id "a1-entry-claim-duplicate-work-guard" --phase B --heartbeat-only`。死线 **2026-09-06T21:40Z**。
2. **`{id: a1-entry-claim-duplicate-work-guard}`** —— 36/40。先 7.6 开单 (依赖已解除), 再 Group 8 发版 (8.1 → 8.4 → 8.2, `<vNEXT>` = **1.70.0**)。
3. **`{id: carry-ab-suite-defects-24}`** —— `DEFECTS.md` 24 条开单, A 节四条优先。

---

## §7 提交清单

| 仓 | 分支 | SHA | origin | github |
|---|---|---|---|---|
| Aria | `feature/a1-entry-claim-duplicate-work-guard` | `5d9b568` + 本 session 新提交 | 待推 | 待推 |
| aria-plugin | 同名 | `ab3dbd0` + 补丁 (+16/−0) | 待推 | 待推 |
| aria-standards | 同名 | `bb5d375` | ✅ MATCH | ✅ MATCH |

⚠️ **本 session 的改动尚未提交**: aria 的 SKILL.md 补丁 (+16/−0) · 主仓的 tasks.md/yaml 回写 · 整个 `ab-results/2026-09-05-v1.70.0-a1-entry-rule6/` 目录。**推送是外向动作, 待 owner 授权。**

---

## §8 Memory entries this session

本 session **未写新 memory** (context 预算优先给了结果落盘)。§4 的 4 条候选 + 2 条未写下经验**待下次固化** —— 其中「断言可以奖励错误行为」与「n≥3 才下结论」两条最值得写。

---

## Cross-references

- 前一份 handoff: [2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md](./2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md)
- **AB 总账**: `aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/RESULT.md`
- 分数 (脚本汇总): 同目录 `SCORES.md` | 缺陷 24 条: 同目录 `DEFECTS.md`
- 手册: `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 1
