# post_spec R8 聚合报告 — state-scanner-stale-refs-false-parity (v8 @ fe9003d)

> **Verdict: FAIL 3/3** (D15′对抗 3C/4M/5m + RC核验 1C/5M/7m + qa-fixture 1C/9M/9m; 去重后 ~4C/~14M/~15m)
> 2026-07-14 | 三方 code-grounded + 真 git 实验 | **收敛信号**: R7 的 20 条 finding 15 条被独立确认落地扎实; 全部 git 语义类修复实验复核零翻车; 三方一致「D15′ 轴是对的, 不需要换轴」— 剩余为窄缺口

## 一句话

D15′ 双角色拆分正确切断了 R7 三 Critical 的共同根 (创始事故形态在 ∃ 侧被结构性杀死), 但**三档处置自己留了一个守卫不相交格** (E∧¬X, 两 agent 独立命中 = 第 11 次复发候选位不幸兑现), 加上载体/分母 scope/引用换血三类窄残留。

## 去重后 Critical (4)

| # | 内容 | v9 修法 | 备注 |
|---|------|---------|------|
| 🔴 **8C-1** (agent1 C-1 + agent3 C-1 独立命中) | **equal 三档守卫不相交**: `证据资格 ∧ ¬豁免资格` 格同时命中第一档 (作证) 与第三档 (blocking), 可达路径 = 负代龄钳位 / D18 恢复 scan 清零先序未定 / 退避腿快节奏 scan (56min≤1h 但 gen=8>k_eff); AC-15(a)/(b) 从两侧钳住该格互相矛盾 | ⚠️ **两 agent 修法方向相反, v9 裁决点**: agent1 建议 ¬X 优先 (E∧¬X ⇒ blocking, 偏红, 与钳位「不可信」语义一致 — 钳位场景下 fetched_at 本身可能同被污染); agent3 建议 E 优先 (第三档改 `¬豁免∧¬证据资格`, 偏绿, 与「作证要世界时间新鲜」立意一致)。**附带无论选哪边都要做**: D18 清零先序写死 (清零在豁免判定前) + AC-15(a)/(b) 措辞随裁决同步 + 5.1d 闸加「守卫互斥性」维度 | 真设计裁决, 建议 owner 过目或下 session 冷静推演 |
| **8C-2** (agent1 C-2 + agent2 M-4 同发现) | `stale_unverified` snapshot **载体未定义** — 若实现进 parity.reason ⇒ blocking_unknown 补集自动阻断 ⇒ 三档塌两档 (spec 自己在 gitlink 层 13.4 解过的同一陷阱, parity 层漏掉) | 载体钉死: parity 保持 `equal` + per-remote 独立可见字段 `evidence_grade ∈ {fresh, stale_unverified}` (与 gitlink_integrity 不进 reason 同构); F4′/横扫表/10.1 schema 同步 | 修法无争议 |
| **8C-3** (agent1 C-3 + agent3 m-2 同 species) | k_eff 收敛不等式**分母 host-scope 未定义** — 全局读法下异速双 host (本仓真实拓扑 7s vs 3.5s) forgejo 腿恒滚动红, 「不恒红由构造保证」被否证 | 分母写死 = per-host 覆盖数 (逐 host 记录, rotation 取最慢 host); m-1 冷启动 rotation 记录缺失 ⇒ 视同 K_CAP? 不 — fail 方向裁定 (缺失 ⇒ k_eff=k_min 偏红) 一并写死 | 修法无争议 |
| **8C-4** (agent2 C-1) | **lag-1 使上一份 snapshot 成为 Phase 1.11 的环境输入**, 9.7 冻结面 (三面) 没接住 ⇒ Spec C AC-4 双跑结构性打不平 (run1 SKIP/FAIL vs run2 PASS) | 9.7 缓存态面加第四项冻结输入 (预置上一份 snapshot); Spec C AC-4 fixture 加「预置健康上一份」前置 | 修法无争议 |

## 去重后 Major (14, 修法全部明确)

- **8M-1** 退役谓词 `可信` live 引用残留 ≥6 处 (agent1 M-2 + agent2 M-1 清单合并: tasks 2.6/2.8/5.2b/3.5 引导句/13.5 [还引已废 D15] + proposal AC-8 L687/AC-15(b)注 L715/L427/L331) — 且 5.1d 闸只查定义不查引用 ⇒ 闸加「退役谓词零 live 引用」断言 (机制化封口)
- **8M-2** DEC D15′ 与 proposal/tasks 豁免资格 3 vs 4 conjunct 漂移 (agent1 M-1) — DEC 公式改指针引用 F4′ SOT; 5.1d 语料扩到 DEC
- **8M-3** 13.1 `¬reachable` 过宽 (agent2 M-2): rc=128 会被判 orphaned 与分支 7 矛盾; S 无 R 未前置滤与分支 8 矛盾 — 收窄为 `(rc==0 ∧ out空) ∨ no_object` + leg 枚举预滤写进 13.1
- **8M-4** F4′ 公式块缺 gitlink 项 (agent2 M-3): 补 `∧ (∀ R: ¬gitlink_blocking(R))` 引 13.4
- **8M-5** consecutive_unverified 是第 7 漂移通道候选 + offline 行为未定义 (agent1 M-3 + agent3 M-9 扩展: v8 全部新键 [fetch_ok/skipped_remotes/generation*/gitlink_integrity.status] 无 normalize 登记任务; 9.7 与新键落地无顺序依赖声明) — 12.10 清单补第 7 条 + 9.7 定义 offline 下计数器冻结 + 13.8 golden 新字段期望说明
- **8M-6** gitlink pair 清零条件类型不匹配 (agent1 M-4): orphan_unverified 是 (R,S) 键, 清零绑「status 判出 ok/orphaned」非证据资格; m-5 双分区歧义一并写死 (per-leg 与 per-(R,S) 两份计数器, 各自键空间)
- **8M-7** Spec C §2 首句「本次 snapshot 内」与 D19 lag-1 互斥残留 (agent2 M-5) + AC-3/3b 叙事「本次」框架残留 (agent3 m-8)
- **8M-8** Spec C 迁移态未定义 (agent3 M-8): 上一份存在但缺 generated_at ⇒ 视同首跑 SKIP 可见 (否则升级窗自造红)
- **8M-9** Spec C AC-4 落地链断 (agent3 M-6): 3.1 悬空引用 (零字提 output 确定性) + AC-4 零实现任务 — 补 3.1 确定性子任务 (output 不嵌 Δ/时刻) + AC-4 双跑 diff 测试任务
- **8M-10** AC-15(a) 稳态 fixture 使 k_eff 惰性 (agent3 M-1a): 补「稀疏节律多轮跑」fixture (scan 间隔>1h, 走 stale_unverified 档, 真执行豁免/k_eff 代码路径)
- **8M-11** 收敛条件缺墙钟项 (agent3 M-1b): 真条件 = `rotation ≤ k_eff ∧ rotation × scan间隔 ≤ hard_cap`; fixture 钉 scan 间隔 (防反推病换参数复活)
- **8M-12** rotation>k_eff 边界 fixture 参数不可构造 (agent3 M-2): 写死批准参数 (72 腿单 host 变体)
- **8M-13** budget seam 零任务 (agent3 M-3): 每 scan 覆盖 N 腿的确定性注入点任务化; ARIA_SCAN_NOW 对非 offline fixture 可用性声明
- **8M-14** ¬豁免三分支无单变量 fixture (agent3 M-4) + AC-17(e) tag-only fixture 须本地造 tag 才锁得住 (agent3 M-5) + (f) 代差 fixture 构造路径与防饥饿矛盾需指引 (agent3 m-6)

## Minor (~15, 原文见三方报告)

agent1 m-1..5 (冷启动 k_eff/零边距瞬红/in-flight 杀放行/D18 k_eff 动态解锁/渲染落点 10.4) + agent2 m-1..7 (3.15 断言对象改 coordination_ref_present [Fetch 2 是 src-only 不产本地 ref, 实读确认]/served_stale_cache 未定义/2.19 枚举补 3 支/Spec B 4→6 条陈旧数字/AC-2 主句限定/scan.py 写盘非原子→坏 JSON 并 SKIP/零边距) + agent3 m-1..9 (含 m-7 dogfood fixture 环境依赖拆分/m-9 b′ 三断言配对)。

## 收敛评估

- **已固化的可信面** (三方交叉): F10″ 原语 + 八分支定义域 + prune 前提 (实验: refspec 限定 prune 不伤 coordination ref, 且比声称更强) + rc 语义全套 + cache 键 + generation 写入侧三条 + shim 9 格 + 退避 carve-out + lag-1 可行性前提 (scan.py 实读) + AC-16/17 大部分 fixture 可构造性。
- **剩余工作特征**: 无换轴级问题; 8C-1 是唯一真裁决点 (两 agent 方向相反); 其余全部是「写死一句/补一个任务/换一个词」级。
- **R9 建议范围**: 8C-1 裁决 + 4C 修复文本 + 8M-1 引用清扫核验 + Spec C v5 (M-7/8/9)。

## 教训 (第 11/12 次复发形态定型)

- **第 11 (兑现)**: 新谓词组的**守卫互斥性** — 拆一个谓词成 N 档时, 档间守卫必须构成全分割 (∀格恰一档), 5.1d 类机械闸应加「守卫两两互斥 + 并集全覆盖」断言维度。
- **第 12 (候选)**: **修复自己引入的新环境输入** — lag-1 把上一份 snapshot 变成了新的 run-to-run 耦合, 而冻结面清单是修复前定义的。每引入一个「读持久态」的机制, 必须回头把该持久态登记进所有「环境冻结面/漂移通道」清单。
