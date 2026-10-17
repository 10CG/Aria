---
type: owner_decision_sheet
subject: 2026-09-30 紧急 issue 梳理与处理计划的 owner 裁定 (P0 清单 / 凭据轮换延后 / WP-A~C 的 Level / 一次性授权四类 / 双子星分工)
spec_ids: []
status: decided
decided_by: owner
decided_at: 2026-09-30
created: 2026-09-30
container: simonfish/023236f2
---

# 决策单 — 2026-09-30: 紧急 issue 梳理与处理计划

> **来由**: 本会话 (023236f2) 先同步远程 (主仓 fast-forward 101 个提交, aria-plugin v1.73.3 → v1.74.0, 四仓 origin / github 两端 `ls-remote` 一致), 再梳理 `10CG/Aria` 46 + `10CG/aria-plugin` 76 共 122 个 open issue (分类由脚本校验, 每条恰好归一类, 无重复无遗漏), 提出 8 条紧急项加 `10CG/Aria#199` 跟踪, owner 对五个问题逐条答复。
> **授权范围**: 第 4 项 —— 仅四类外发动作; 合并 / 推送 master / tag / 发版不在其内。

---

## 1. 紧急清单 —— 采纳

- **裁定**: 「清单可以」。8 条紧急项加 `10CG/Aria#199` 跟踪按提出的样子采纳; `10CG/Aria#196` 维持 P1 (未被驳回)。
- **紧急判据** (满足任一, 且经核验仍存在): 已发生的泄露而轮换未闭环 / 不可协商规则的闸门有已复现的误放行且已有采用方撞上 / 入口报告失真或静默丢数据且修复很小 / 有明确到期时间。
- **清单归属**:
  - A 类 (泄露轮换悬空, 4 项: `10CG/aria-plugin#203` / `10CG/Aria#221` / `10CG/Aria#170` / `10CG/Aria#136`) —— 按第 2 项延后。
  - B 类 (兜底网与闸门有洞, 3 项) —— 第 5 项 secret 网补洞 (`10CG/aria-plugin#154` + `10CG/aria-plugin#203` + `10CG/Aria#221`) 归 WP-A; 第 6 项 `10CG/Aria#223` 与第 7 项 `10CG/aria-plugin#207` 归 WP-B。
  - C 类 (入口报告失真) —— `10CG/aria-plugin#182` 归 WP-C。
  - D 类 (已在做, 只跟踪) —— `10CG/Aria#199` / `10CG/aria-plugin#161` 归 bfe8285d。
- **依据 (本会话实测, 非转述)**: state-scanner 自己的 `issue_status.open_count` = 48, 同一时刻 API 分页全量 = 130 (aria-plugin 20 / 76, Aria 20 / 46; 被丢的是编号最小的老单, 含 `10CG/Aria#136`); `hooks/secret-scan.sh` 对 09-26 事故形态 `JWT_SECRET = <b64>` (等号两侧带空格) 与 08-20 事故形态 `{"token":"…"}` 均零输出, 同一测试台上阳性对照 (`client_secret` JSON 键 / `JWT_SECRET=` 无空格) 均被检出。

## 2. 凭据轮换 —— 全部延后, 先头脑风暴再统一处理

- **裁定**: 轮换类一概本次不做, 后续统一处理; 且在处理前先做一次针对性的头脑风暴 (`aria:brainstorm`), 设计更有效的应对方案。
- **范围**: `10CG/aria-plugin#203` (Forgejo `JWT_SECRET`, 2026-09-26) / `10CG/Aria#221` (三枚凭据, 2026-09-24) / `10CG/Aria#170` (T4 PAT, 2026-07-22) / `10CG/Aria#136` (Feishu webhook, 2026-05-31); `10CG/Aria#151` 的 Aether 侧吊销同属等待项。
- **执行注**: 不产出轮换清单, 不逐条提示轮换; 相关 issue 保持 open、本项之下不评论。WP-A (代码侧兜底网补洞) 不受影响, 照常推进。
- **代价**: 上述泄露的凭据在统一处理之前继续有效; 已挂最久的 `10CG/Aria#136` 自 2026-05-31 起。

## 3. Level 与 Rule #6 —— 采纳 AI 建议

- **裁定**: 「同意你的方案」。WP-C (`10CG/aria-plugin#182`) = Level 1; WP-A (secret 网补洞) 与 WP-B (`10CG/Aria#223` + `10CG/aria-plugin#207`) = Level 2。
- **依据**: `standards/openspec/project.md` Level 表 (1 = Simple fixes / 2 = Medium features, 1-3 days)。WP-C 是单个 collector 的有界缺陷修复加追加字段; WP-A / WP-B 含新入口与设计取舍。
- **Rule #10 备注**: Level 1 无 Spec ⇒ 无 `post_spec` 检查点 (白名单第四类「结构性前提不成立」), 该分级是 AI 的建议、owner 于本日采纳, 不是 AI 自行降级。config 里 enabled 的 `post_spec` / `post_planning` 对 WP-A / WP-B 照常适用, 不豁免。
- **Rule #6**: WP-C 在 ship 前按 `skill-benchmark-exemption.md` §2 逐 hunk 判定; 预判为决策表第 1 行 (描述性 + 纯 collector 代码, 先例: `state-scanner-stale-refs-false-parity` v1.60.0) ⇒ substitute (baseline-failing 结构化测试); 任一 hunk 触及 SKILL.md 指令面或 `description` 则改照跑 AB。留痕: Level 1 无 spec / tasks, `rule6_note` 落在 PR 描述与 handoff。WP-A 沿用 owner 2026-08-02 对 hook 的 substitute 框定 (提示文案的 hunk 单独判)。

## 4. 外发动作 —— 一次性授权 (按类)

- **裁定**: 「一次性授权」, 覆盖本计划 WP-A / WP-B / WP-C 及其后续, 共四类:
  1. feature 分支推送 (两个 remote, 推后逐个 `ls-remote` 核验);
  2. 开 PR;
  3. issue 评论;
  4. issue 关闭。
- **边界 (不在授权内, 到时逐次请示)**: 合并到任一 master (含子模块本地 merge 后的推送) / 推 master / 打 tag 与发版 / 主仓 PR 的合并 / 删除远端分支。Layer L 协调 ref 的 claim 与心跳沿用 2026-09-17 的例行维护授权。
- **依据**: 提问原文为「feature 分支推送、开 PR、issue 评论和关闭, 逐次授权还是按类一次性授权」, owner 答「一次性授权」; 此处按提问所列的四类落字, 不外推。

## 5. 双子星分工与顺序

- **裁定**: 「双子星分工可以」。023236f2 (本容器) 按 WP-C → WP-A → WP-B 单执行席串行推进; bfe8285d 继续 `10CG/Aria#199` (B.1 起)。
- **文件域**: WP-A (hooks) 与 WP-C (`collectors/issue_scan.py`) 同 `10CG/Aria#199` 的文件集不相交; WP-B 同属 phase-c-integrator, 而 `10CG/Aria#199` 会改其 `SKILL.md`, 起 WP-B 前先核对 `10CG/Aria#199` 进度; `10CG/Aria#173` (`spec_complete.py`) 与 `10CG/aria-plugin#199` (`check_bare_issue_refs.py`) 同 `10CG/Aria#199` 改同一批文件, 排在 `10CG/Aria#199` ship 之后。
- **待 bfe8285d 处理 (AI 提醒)**: `10CG/Aria#199` 的 claim 心跳最后为 2026-09-30T06:57:09Z, `SWEEP_TTL` = 24h ⇒ 2026-10-01T06:57Z 之后可被扫为 `abandoned`。心跳须由 bfe8285d 刷新; 023236f2 不写他人 claim (`10CG/aria-plugin#166` 的 D6 权限面)。
- **ship 顺序 (AI 建议, owner 未单独裁)**: 沿用串行 (aria-plugin 版本源唯一, 版本号在 ship 时刻取、合并前重新核 `plugin.json`)。`2026-09-12` 的 Q3 裁定原文只针对 `10CG/Aria#195` / `10CG/Aria#199` 两份 Spec 的执行顺序, 不是通用规则; 本条按默认沿用, 待复议。

## 6. 记入待办

- 凭据轮换的头脑风暴 (第 2 项) —— 时间由 owner 定。
- issue 卫生清扫: 疑似已修未关或重复的 `10CG/Aria#174` / `10CG/aria-plugin#135` / `10CG/aria-plugin#194` / `10CG/aria-plugin#110`, 以及 `10CG/Aria#180` 与 `10CG/aria-plugin#107` 重复 —— 先 triage 核验, 再评论 / 关闭 (属第 4 项授权范围)。
- P1 批: `10CG/Aria#220` / `10CG/Aria#182` / `10CG/Aria#218`, `10CG/aria-plugin#107` + `10CG/aria-plugin#169`, `10CG/aria-plugin#136`, AB 套件 `10CG/aria-plugin#172` / `10CG/aria-plugin#173` / `10CG/aria-plugin#174`。
