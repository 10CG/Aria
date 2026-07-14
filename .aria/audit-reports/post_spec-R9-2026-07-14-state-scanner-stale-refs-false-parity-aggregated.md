# post_spec R9 聚合报告 — state-scanner-stale-refs-false-parity (v9 @ 13bebb5)

> **Verdict: PASS-with-fixes 2/2** (D20 对抗 0C/6M/4m + 修复核验/引用复扫 0C/6M/9m)
> 2026-07-14 | **本轨 R1-R8 八轮全 FAIL 后首个非 FAIL verdict** | 两方一致: fixes 全部文本级、目标态由 D20 唯一确定、**修后无需整轮 R10** — 按报告清单 grep 复核即可

## 一句话

**D20 (三档全分割, E 优先) 本体经受住全部证伪**: 全分割数学成立、SOT 七处互相一致、裁决基石 (E 不可被 artifact 伪造) 在 whole-file cache 模型下论证严密 (lost-update 只能把 fetched_at 覆盖成旧值 → 方向安全)、evidence_grade 载体与 9.7 五面冻结闭环。唯一实质设计补丁 = **负墙钟龄钳位** (时钟回拨可伪造 E — 一行, 与负代龄钳位同构)。其余 findings 全部是「SOT 已对、镜像/残留未跟」。

## v10 已折入 (本 commit, 全部 R9 findings)

| R9 # | 内容 | 落点 |
|---|---|---|
| M-1 (两方同发现) | 6 处 v8 形态守卫 (`¬豁免 ⇒ blocking`, E∧¬X 格与 D20 矛盾) | 横扫表 deadline 行 / F3′ 块+注 / F1′ 行 / 降级表读法 / AC-11b 注 — 全部改三档全分割或指针 F4′ |
| M-2 (两方同发现) | `可信` live 残留 7+5 处 (两轮清扫均不彻底 — 「正向枚举漏格」病在清扫动作自身上重演) | tasks 3.5 引导 (backtick 变体)/3.5d/5.1 注/5.2 标题/L89 + proposal L332/L335/裁决表 + AC-1/AC-7 白话 (m-7) — 全清 |
| agent1-M3 | **负墙钟龄可伪造 E** (时钟回拨; 唯一实质设计补丁) | F4′ E 定义 `0 ≤ (now−fetched_at)` + 负值⇒视同 null 钳位 (tasks 4.2/3.16 镜像) |
| agent1-M4 | D20 核心格 E∧¬X 零 fixture | AC-15(a⁗) + 2.18(a⁗): E∧¬X 腿 ⇒ fresh ∧ 作证 (v8 式实现必 RED) |
| M-5/m-2 | AC-15 子项标号漂移 (b′ vs a′) | 统一 (a′) |
| agent1-M6 | D18 冻结 vs 清零先序 | 3.16: fetch 成功 > 冻结 > 递增 先序链明写 |
| agent2-M3 | DEC D15′ 公式漂移 (3 conjunct/全局分母/被推翻的声明) | D15′ 指针化 (SOT=F4′, 不复制) + D11 读法注 (m-9) |
| agent2-M4 | evidence_grade 缺 schema 链 | tasks 3.6 + 10.1 补字段 |
| agent2-M5 | Spec C §2 首句未修 (**v5 status 虚报** — R9 用 git diff 抓出) | Spec C v6: 首句/§Why/「本次」框架真修 + status 教训注 |
| agent2-M6 | tasks 5.2 缺 gitlink 子句 | 补第 4 子句 (镜像 F4′) |
| minors | max(1,·) 同步 / AC-17(a) 合成 fixture 归属 / k_eff 全局取舍声明 / 瞬红可接受 / Spec B 簿记 / Spec C AC-5b SKIP 三态锚 / 8 腿/host/scan 单位 | 各落点 |

## 修后机械复核 (代 R10, 两方建议)

- `¬豁免 ⇒` 单守卫: 仅剩 gitlink 层 13.5 (语义正确 — ¬豁免 ⇒ 不判, 非 blocking) + 溯源区 ✓
- `可信` live: 补清 5 处漏网 (backtick 变体/白话) 后, 仅剩 rationale/溯源区 ✓
- `freshness_window`/`300s`: 零 live 残留 (R9 复扫确认) ✓
- Spec C「本次」框架: 仅剩 L47 代码事实句 (关于 scan.py 的真陈述, 非断言语义) ✓
- NUL: 干净 ✓

## 状态迁移

**R9 = 本轨收敛点**: 9 轮审计 (R1-R9), 11 次复发形态全部捕获并机制化 (5.1d 闸六维度: 集合成员/单一定义/守卫全分割/退役零引用/语料含 DEC/reason 落桶)。三 spec (主 v10 / B v2+簿记 / C v6) 文档自洽。**下一步 = owner sign-off → A.2/A.3** (落地顺序 Spec C → Spec B → 主 Spec 不变)。
