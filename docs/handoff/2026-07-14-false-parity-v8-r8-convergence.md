---
track-id: state-scanner-stale-refs-false-parity
linked-issue: 10CG/aria-plugin#110
owner-container: simonfish/bfe8285d
phase: A.1-postspec-R8
status: active
updated-at: 2026-07-14
---

# Session Handoff — v8 (R7 全折 + D15′/D18/D19 代裁) → R8 FAIL 3/3 (显著收敛)

> owner /goal「按你的建议裁决并完成 v8→R8」。完成: 3 裁决落 DEC v9 (§3d) + v8 全折 (`fe9003d`) + split-brain 横扫修补 15 残留 + R8 三视角审计 + 聚合落盘。

## §0 入口 (新 session 优先读)

- **下一步 = v9**: 修法全部在 [R8 聚合报告](../../.aria/audit-reports/post_spec-R8-2026-07-14-state-scanner-stale-refs-false-parity-aggregated.md) (4C/14M/15m 逐条带锚)。
- 🔴 **唯一真裁决点 8C-1 (建议 owner 裁)**: equal 三档在 `证据资格∧¬豁免资格` 格守卫重叠 (两 agent 独立命中), 修法方向相反 — **¬X 优先** (E∧¬X ⇒ blocking, 偏红; 理由: 该格可达路径全是钳位/计数器 artifacts, 彼时 fetched_at 本身可能同被污染) vs **E 优先** (第三档改 ¬豁免∧¬证据资格, 偏绿; 理由: fetch 真成功 <1h = 世界时间新鲜, 与 D15′ 立意一致)。附带无论选哪边: D18 清零先序写死 (清零在豁免判定前) + AC-15(a)/(b) 同步 + 5.1d 闸加守卫互斥维度。
- 其余 3C (载体/分母 scope/lag-1 冻结面) + 14M **修法无争议, 纯机械**。
- **收敛信号强**: R7 20 条中 15 条三方确认扎实; 三方一致「D15′ 轴对, 不换轴」; git 语义类修复实验复核零翻车。轨从「换轴期」进入「收口期」。

## §1 已完成

1. **DEC v9 §3d 代裁**: D15′ (双角色谓词: 证据资格 1h / 豁免资格 k_eff+7d; k_eff 收敛耦合) + D18 (unverified ≥k_eff 代升级 blocking + 必渲染) + D19 (Spec C lag-1 两跑断言)。
2. **v8 (`fe9003d`)**: R7 8C/12M/10m 全折 — prune / D15′ 全落位 / §13 八分支 / gitlink_integrity 独立结构 / generation 写入侧三 fail-CLOSED / shim 9 格 / offline 三面 / AC-16·17 fixture 群; Spec C v4 (lag-1 + AC-2 两跑 + AC-4 收窄)。
3. **split-brain 横扫 agent** 抓 15 处传播残留 (改主位点漏镜像位点 — RC-2 预言的错误类在我自己身上兑现), 全部修补。
4. **R8 三视角** (D15′对抗 / RC核验 / qa-fixture, 全 code-grounded + 真 git 实验): FAIL 3/3 但高收敛; R8 聚合落盘; proposal Status 收敛。
5. R8 期间实验固化的可信面: prune refspec 限定不伤 coordination ref (比声称更强) / rc 语义全套 / lag-1 可行性 (scan.py L239 实读) / AC fixture 可构造性大部。

## §2 未完成 / Carry-forward

- **carry-v9**: 8C-1 裁决 (owner) → 4C+14M 折入 → R9 窄范围 (8C-1 裁决文本 + 引用清扫核验 + Spec C v5)。
- **carry-spec-c-v5**: 迁移态 (缺 generated_at ⇒ SKIP) + AC-4 任务链 (3.1 确定性子任务 + 双跑 diff 测试任务) + §2 首句 lag-1 残留。
- (承前) 落地顺序 Spec C → Spec B → 主 Spec; Spec B 有一处 4→6 条陈旧数字待顺手改 (agent2 m-4)。
- (承前) M6 owner 4 门 / carry-136-rotation / plugin#107/#109 / orchestrator#31。

## §3 关键风险 / 已知陷阱 (增量)

- **复发形态 11 号定型**: 拆谓词成 N 档时, 档间守卫必须构成**全分割** (两两互斥 + 并集全覆盖) — 我写三档时第二档带了 ∧¬证据资格 而第三档没带对称项, 守卫重叠格由两个独立审计命中。机械闸应加守卫互斥维度。
- **复发形态 12 号候选**: 修复引入的新持久态读取 (lag-1 读上一份 snapshot) 必须回头登记进所有「环境冻结面/漂移通道」清单 — 冻结面是修复前定义的, 不会自动覆盖修复自己造的新输入。
- **传播修补要横扫不要点修** (亲历): v8 我改了 F4′ 公式块+横扫表+DEC 三处「主位点」, 漏了 15 处镜像位点 — 与 R7 抓 bot 的 split-brain 完全同形。改核心符号后必须 grep 全符号出现面逐处判 [已改/溯源区/残留], 交给机械 agent 做比自己记忆可靠。

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| 主仓 | `fe9003d` (v8) + 本 commit (R8 聚合 + Status + handoff); 推 origin+github |
| 三 spec | 主 Draft v8 (R8 FAIL 收敛) / Spec B v2 (未动, 1 处陈旧数字待顺手) / Spec C v4 (待 v5) |
| DEC | v9 (D15′/D18/D19; 8C-1 裁决后 D15′ 需补先序条款) |
| aria-plugin 等 | 未变更 |
| 协调 ref | 本 cycle claim 以 yielded 释放 (轨 active) |

## §6 Next session 入口 + 优先级

1. ⭐ **8C-1 裁决** (owner 一句话: ¬X 优先偏红 / E 优先偏绿) → **v9 折入** (全机械) → **R9 窄范围**。
2. (承前) M6 owner 4 门 / carry-136-rotation。

## §8 Memory entries this session

- 已落: feedback_windowed_predicate_needs_convergence_inequality (上一轮)。
- 本轮候选: 「拆谓词 N 档须证守卫全分割」+「新持久态读取须登记冻结面」— 均已写进 R8 聚合报告教训段, 待轨收口时评估是否单独成条 (避免密集同主题 memory)。

## Cross-references

- R8 聚合: `.aria/audit-reports/post_spec-R8-2026-07-14-state-scanner-stale-refs-false-parity-aggregated.md`
- v8: `fe9003d`; R7 聚合: 同目录 R7 文件; 前序 handoff: 2026-07-14-false-parity-v7-r7-fail-d15-triple-hit
