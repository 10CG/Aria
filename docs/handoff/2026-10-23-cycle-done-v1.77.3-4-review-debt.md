---
track-id: 257-v1.77.3-review-debt
owner-container: simonfish/bfe8285d
phase: D.3
status: done
updated-at: 2026-10-23T16:20:31Z
---

# Aria — 周期收尾 (2026-10-23) — #257 review 债务清偿双 PATCH (v1.77.3 一轮 3I/6M + v1.77.4 二轮收口; PR #259/#260)

> **性质**: 周期收尾 (D.3)。用户选 [1] #257; 双轮发版 + 两轮 post-merge 对抗 review。

## §0 入口

`/state-scanner` 全绿复扫 → 推荐 [1] #257 → B-entry claim (track=257-v1.77.3-review-debt)。

## §1 已完成 (时间线)

1. **v1.77.3 一轮清偿** (`0648622`): I-1 SKILL §C.2.4.5 摘录同步 (6 处 + 定向 fixture 4 SC, Rule #6 第三行 — 套件缺口 **#258** 已开) / I-2 枚举面 7 处 / M-4 BASE_REF_OK fetch 后重算 (scenario 14 **逼出附带真 bug**: `git rev-parse <ref>` 失败回显 + FIRST_RUN 拼接 → 首次 fetch 误判 rewrite exit 3, 既存潜伏, 修 `-q --verify`) / M-5 warn verdict=ALLOWED / M-8 / M-10
2. **行尾事故与钉正**: SKILL.md 原生 CRLF 被 python 写回变 LF (全文件漂移 1124 行) → `a5ee63b` 钉正 (内容 23+/8-), **tag v1.77.3 移至钉正 commit** (自推数分钟内, 自我钉正范围)
3. **一轮 review PASS** (0C/3I/4M) 抓三点: I-1′ 摘录 exit 码残点 (fetch/rewrite 仍 exit 1) / **I-2′ M-6 无处置却宣称 6M 清偿 = 决策记录失真** / I-3′ SC-2 精确串枚举可被 v1.77.2 原文形态逃逸 (reviewer 实测全绿, #179 C-1 同型)
4. **v1.77.4 二轮收口** (`8614066`): **M-6 实修** (exit 严重度: REGRESSION(1) 不被环境类(4) 降格, 4 处守卫 + scenario 15 改前 exit 4 修后 1, 全量反事实红) / I-1′ exit 2/3 + enum error + 消息 $BASE_REF 化 (**CRLF 保持** — newline="" 读写) / I-3′ SC 行族收口 (v1.77.2 形态回退转红, 反事实复验) + exit 码分类 SC / Minor×3 (gate 头注/docstring 残句/schema history 补 #218 行)
5. **#257 关单** (评论: 全明细表 + v1.77.3 宣称失真正式修正; M-9 仍缓期捎带, M-7 记录不修)
6. 发版双推: v1.77.3 `a5ee63b` + v1.77.4 `8614066` (master+tag ×2 remote); 主仓 PR #259/#260 → `c6b93b7` 双端; §6.4 三步 dogfood 双轮全过 (回评两 PR)

## §2 关键数字 / 产物

| 面 | 产物 |
|----|------|
| aria | v1.77.3 `a5ee63b` + v1.77.4 `8614066` (双端; 15 scenario/20 断言 + 5 SC 全绿) |
| 主仓 | PR #259 + #260 → `c6b93b7` (双端; 同步面 8 文件 ×2 轮) |
| issue | #257 closed (全清偿明细); **#258 open** (套件缺口待裁); #246 三步 dogfood ×2 |
| review | 两轮 post-merge PASS (0 Critical); 二轮 3I/4M 全清于 v1.77.4 |

## §3 关键风险 / 已知陷阱 (本 session 新增)

- **「宣称清偿 vs 无处置」失真**: v1.77.3 标题/CHANGELOG 宣称 3I/6M 而 M-6 未修未记 — review I-2′ 裁「不能再无声」。教训: 记录不修也必须写进 issue/CHANGELOG, 宣称口径与处置清单逐项对账
- **CRLF 双连击**: v1.77.3 全文件漂移 → v1.77.4 用 `newline=""` 读写零漂移; 该仓确有 CRLF 原生文件 (SKILL.md), python 机械写必须保行尾 (`jq-CRLF` memory 教训二次复发+正解)
- **SC 形态族**: 精确串枚举的守卫可被「部分回退/换形」逃逸 (reviewer 实测); 行族收口 (正则匹配判定行族) 才是形态族穷举的正解
- **流程偏差 (如实记录)**: PR #260 merge 前未做 in-flight 显式核验 (merge 直接执行) — 客观风险为零 (双方触面均零 CI 触发), 但顺序违反 Rule #8 惯例, 本条即为呈报

## §4 待固化经验

```
[候选 memory]
- python 机械写 CRLF 原生文件必须 newline="" (v1.77.3 全文件漂移 + v1.77.4 零漂移正解; jq-CRLF 族二次复发)
- 「清偿宣称」必须与处置清单逐项对账, 记录不修也是处置 (M-6 失真教训)
```

## §5 四维一致性

CLAUDE.md 版本块 v1.77.4 已覆写; sync 面三仓双 remote 一致 (16:20 快照); i18n ×4 / arch ×2 / VERSION 全绿。

## §6 Next session 入口

- **plugin cache 刷新至 v1.77.4** (owner 手动三步 + 三面复验; 前两版同样积压 — 1.77.1 缓存上跑到现在)
- **#258 套件缺口** 待 owner 裁 (补 eval vs 常驻 substitute)
- #229/#241 secret-guard 族仍勿接 (双子星 #217 状态未复核)
- M-9 (§6.4 措辞) 捎带; M6-M7 记录不修
- 本 session 已 3 个完整 cycle (rule6-4b / v1.77.2 / v1.77.3+4), 建议会话收尾

## §7 提交清单 (按仓)

| 仓 | 提交 |
|----|------|
| aria | `908f0b5`+`53ba42d`+`60a6bfe` → `0648622` + 钉正 `a5ee63b` (v1.77.3); 二轮 → `8614066` (v1.77.4) |
| 主仓 | PR #259 (`8a0687b`) + PR #260 (`c6b93b7` 前序) → `c6b93b7` |
| 外向 | issue #257 closed / #258 opened; PR #259/#260 + dogfood 回评 |

## §8 rule6_note

SKILL.md §C.2.4.5 = 第三行 substitute (5 SC 行族收口 + 反事实 ×2 实证; 套件缺口 #258); gate 脚本 = 15 scenario replay 红→绿 (新 13/14/15); references = 描述性 + 行为已锁; 无 description 变动。详 CHANGELOG v1.77.3/1.77.4 节。
