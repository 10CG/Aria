---
track-id: rule6-4b-routing-should-not-sot-revision
owner-container: simonfish/bfe8285d
phase: D.3
status: done
updated-at: 2026-10-22T17:18:27Z
---

# Aria — 周期收尾 (2026-10-22) — rule6-4b SOT 修订方向 B 落地 (#243 方向 C · B 立即) + i18n 三语种版本面同步 1.77.1

> **性质**: 周期收尾 (D.3)。goal 直驱 session (`/goal` = 遵循 aria 规范 / agent team 动态工作流 / 执行推荐 [1]+[2] / 确认双子星无冲突); B-entry 已补 claim (phase1_gate advisory passed, track=rule6-4b-routing-should-not-sot-revision)。

## §0 入口

`/state-scanner` (exit 10, 2 软错误均 advisory) → 推荐 [1] rule6-4b 实施 + [2] i18n 判定 → `/goal` 确认双执行 + agent team → 对抗 review → ship → 归档 → 本收尾。

## §1 已完成 (时间线)

1. **双子星冲突核验 (开工前 + 收工实证双确认)**: claim board 全扫 (collision.kind=none; 其 track `substrate-eval-poc-phase1` 已 done 释放) + 其终局 handoff §6 后续选项全落 PoC/orchestrator 面; 收工时 master 并发新提交 (`95cf1de`/`cddb246` = secret-guard #217 spec + pi-durable PoC) 与本轨零交集, PR #255 干净 merge。**#217 全程未触碰 (勿接纪律遵守)**
2. **[1] 轨 C 全周期**: spec 升级 (Status 按裁定链: issue #243 owner comment 2026-10-22T10:19Z 方向 C + 周期 handoff §6; 项 2/3 按 proposal 明示建议执行, 兜底闸=owner 审阅) → T2 standards 边界注 (should-not 二分) → T3 AB 手册 §4b (判据改写 + 二分表 + 观察面) → T4 套件 type 标注 (4 routing/6 capability, 两可从严) + ab-suite 1.8.0 → T5 重判 dogfood → T6 issue #253 (P2) → T8 对抗 review → T7 ship
3. **对抗 review (非作者席 aria:code-reviewer) PASS**: 0 Critical / 1 Important / 4 Minor。**Important-1 已修**: 门判据对「未标注 type 的套件」字面空转 (假绿族) → 加 fail-CLOSED 硬规则; Minor 3 修 (:285 限定 capability / rejudge.py 入库+idx 对齐 / proposal 裁定记录注); Minor-4 预存不阻塞 (issue-groomer SKILL.md description 重复段落, 下次触碰清理+照跑 4b)。独立重分类 10/10 与作者一致; 重算数字逐格吻合
4. **[2] i18n 判定+执行**: v1.77.0→v1.77.1 正文 diff 仅版本行 ⇒ #140 B 档无需重译; 三译文各 3 处机械同步 (translated-from + badge + 版本表行) → `i18n-readme-translation-currency` 转绿。reviewer 认定 = 补 `0bd647a` 发版提交漏掉的同步面 (与 memory `version-checks-blind-to-i18n-readme-body` 吻合)
5. **ship**: standards `81300e0` → 本地 merge `79ecd75` → 双推 (双 remote ls-remote 核验一致); 主仓 PR **#255** (`3222480`+`cf84934`) → Forgejo merge `52ff227` → 双推核验一致; 归档 `46d1fe0` 双端。#243 评论+关单 (B 落地, A 转 #253)

## §2 关键数字 / 产物

| 面 | 产物 |
|----|------|
| standards | `79ecd75` (双端): skill-benchmark-exemption §6 二分边界注 |
| 主仓 | PR #255 merge `52ff227` + 归档 `46d1fe0` (双端): AB 手册 §4b + 套件 1.8.0 + spec 归档件 (含 rejudge.py) + i18n ×3 |
| issue | #253 新立 (P2 `--sibling-placeholders`) / #243 关单 / #255 PR |
| 重判 | 三轮 4b 历史: fail 集 3→2 / 9→5 / 9→5; 门布尔值均维持 FAIL (如实) |

## §3 关键风险 / 已知陷阱 (本 session 新增)

- **门布尔值不翻转为如实结论**: 保守分类下三臂新门仍 FAIL (capability 残留 5 条误触 = description 能力边界弱或模型接活倾向, 修订结构性论证只覆盖 routing 类)。修订未为 issue-groomer 开后门 — 分类裁量与受益方同体的防放水原则 (两可从严) 是防线
- **SC-3 实证证伪路径**: 首跑 RED 抓到 standards 中文术语 vs 手册英文 token (`capability`/`routing`) 漂移 — SC 不是摆设
- **reviewer 抓的 Important-1 与 memory `universal-predicate-vacuous-truth-on-empty-set` 同族**: 「每条 capability 类 should-not < 0.5」在零 capability 集上真空成立 → 整面空转。fail-CLOSED 硬规则堵住

## §4 待固化经验

```
[候选 memory]
- 「防放水防线」: 判据修订的作者与误触受益方同体时, 两可分类一律从严计门 + owner 审阅闸 + 独立重分类 (对抗 review 先自判后比对) 三层防线
- (SC 价值类已有 memory 覆盖, 不重复)
```

## §5 四维一致性

active_change_not_in_upm advisory 族减一 (rule6-4b 归档); CLAUDE.md 项目状态已覆写; sync 面双远程三仓核验一致 (17:18 快照)。

## §6 Next session 入口

- **套件 type 标注 owner 审阅** (遗留义务): `trigger/issue-groomer.json` 的 4 routing/6 capability 待 owner 审阅后才能作门 (裁量记录: archive/2026-10-22-rule6-4b-*/rejudge-demo.md)
- rule6-4b 后续无本轨动作; A 跟进 = #253 (P2, 未排期)
- i18n check 已绿; 下次发版机械跟进 (v1.78.0+ 若正文实质变更才重译)
- 双子星 #217 仍在飞 (spec v3.1 修订中) — 勿接纪律不变

## §7 提交清单 (本 session, 按仓)

| 仓 | 提交 |
|----|------|
| standards | `81300e0` → merge `79ecd75` (双端) |
| 主仓 | `3222480` + `cf84934` → PR #255 → merge `52ff227`; 归档 `46d1fe0` (双端) |
| 外向 | issue #253 新立 / #243 评论+关单; PR #255 |

## §8 rule6_note

零 SKILL.md 变更 (`decision_table_row: n/a`); substitute = SC-1/2/3 全绿 + 对抗 review PASS。全文见 archive/2026-10-22-rule6-4b-routing-should-not-sot-revision/tasks.md。
