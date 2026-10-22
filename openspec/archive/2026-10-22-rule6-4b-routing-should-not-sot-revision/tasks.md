# Tasks — rule6-4b SOT 修订方向 B 落地

> **依据**: `proposal.md` (方向 C 已裁: B 立即 + A P2) + Forgejo `10CG/Aria#243` owner comment (2026-10-22T10:19Z)。
> **裁定项 2/3 执行口径** (proposal §Owner 裁定项明示建议): 项 2 = 套件内标注 + 报告呈现, `rule6_note` 五字段不动; 项 3 = 既有套件不回溯 (本次触碰的 trigger 套件随触碰标注, 其余套件下次触碰时标)。

## 任务

- [x] T1 spec 骨架: proposal.md Status 按裁定链升级 + 本 tasks.md
- [x] T2 standards SOT: `standards/conventions/skill-benchmark-exemption.md` §6 边界注增 **should-not 二分** (capability 门 / routing 观察) + 末尾双句号勘正
- [x] T3 AB 手册: `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` — :88 目录表注 type + :282 门判据改写 (只计 capability 类) + :293 should-not 二分表 + 套件规约 (type 标注 + 新套件含首次加标须经 owner 审阅)
- [x] T4 套件标注: `ab-suite/trigger/issue-groomer.json` 10 条 should-not 标 `type` (4 routing / 6 capability, 两可从严) + `ab-suite/version.yaml` → 1.8.0
- [x] T5 重判 dogfood: 见 `rejudge-demo.md` (三臂 fail 集 3→2 / 9→5 / 9→5 分流; 门布尔值均维持 FAIL — capability 残留误触如实报告)
- [x] T6 A 跟进轨: Forgejo **#253** (P2): `run_eval.py --sibling-placeholders` runner 增强; ship 后 routing 类恢复设门
- [x] T7 集成: standards `81300e0` → 本地 merge `79ecd75` → 双推 (origin+github ls-remote 核验一致); 主仓 `3222480` + `cf84934` → PR **#255** → Forgejo merge `52ff227` → 双推核验一致 (Rule #8: 触面零 CI 触发, `no_ci_fallback` 显式降级; master 无 in-flight run 双核验过)
- [x] T8 验证: 对抗 review (非作者席 aria:code-reviewer) **PASS** — 0 Critical / 1 Important (已修: 未标注 `type` 硬规则 fail-CLOSED, 防整面空转) / 4 Minor (3 已修: :285 限 capability / rejudge.py 入库+idx 对齐 / proposal 裁定记录注; 1 预存不阻塞: issue-groomer SKILL.md description 重复段落, 下次触碰时清+照跑 4b)。独立重分类 10/10 一致; 重算数字逐格吻合。SC-1/2/3 全绿 (修复后复验)。

## 结构化校验 (SC, deterministic substitute)

| SC | 判据 | 证伪路径 | 实测 |
|----|------|---------|------|
| SC-1 套件标注合规 | trigger/issue-groomer.json 每条 should-not 条目含合法 `type` ∈ {capability, routing}; 20 条总数不变, query/should_trigger 零漂移 (git diff 恰 10 行) | 删任一 `type` 或标非法值 → 校验转红 | ✅ T4 内联断言 + diff 10/10 行 |
| SC-2 重判可证伪 | ≥1 臂新旧门 fail 集合不同 (分类分流真实发生); 门布尔值翻转**不作**修订有效的必要条件 (如报告: 布尔翻转与否取决于 capability 残留误触, 如实呈现) | 若所有臂 fail 集合不变 ⇒ 分类对门判据零效果, 修订无门效果 | ✅ 三臂集合均缩小 (GREEN) |
| SC-3 SOT 交叉一致 | standards 边界注与 AB 手册 §4b 的分类术语/token 一致 (capability/routing/观察面), 互指路径可达 | 任一侧术语漂移 → 交叉 grep 转红 | 见 T8 |

## rule6_note

```yaml
rule6_note:
  decision_table_row: n/a   # 本轨零 SKILL.md 变更; 触面 = methodology SOT + AB 手册 + 套件 schema (描述性/规范面)
  description_changed: no
  scenario1: not_required
  scenario4b: not_required   # 4b 门判据本身是本轨修订对象; substitute = SC-1/SC-2/SC-3 (套件标注合规 + 历史三轮重判可证伪 + SOT 交叉一致)
  negctrl: n/a
```
