先给结论: **四条全部要请你裁定, 一条都不能由我自行放行**, 包括那两条已经是终态 (`done` / `abandoned`) 的。在你裁定之前, A.1 的起草我先停住 —— 认领的意义就是「早于投入」, 现在正是它该起作用的时刻。

## 1. 检测结果回显 (五要素, 原串逐字)

我方 `linked_issue` 原串: `10CG/Aria#174`

| # | 对方 track_id | owner-container | claimed_at | 对方 linked_issue 原串 | status |
|---|---|---|---|---|---|
| 1 | `oauth-login-aaaa1111` | `cA` | `2026-09-05T08:00:00Z` | `10CG/Aria#174` | `active` |
| 2 | `social-login-bbbb2222` | `cB` | `2026-09-04T10:00:00Z` | `10CG/Aria#174` | `done` |
| 3 | `oauth2-spike-cccc3333` | `cC` | `2026-09-03T09:00:00Z` | `10CG/Aria#174` | `abandoned` |
| 4 | (空) | (空) | (空) | `null` | `unknown` |

另: `unknown_schema_claims == 1` —— **已检测到 1 条无法解析的 claim: 存在性已确认、内容未知, 按存在处理。**

关于原串: 前三条回显出来都是完整的 `10CG/Aria#174`, 与我方 org 段 / repo 段 / 编号三段全同, 所以**不是**跨 org 同号的误配 (org 段本身不参与匹配, 逐字回显是判别误配的唯一手段, 所以我不把它缩写成 `#174`, `claimed_at` 也保留完整时间戳不截断成日期)。第 4 条的 `linked_issue` 字段是 `null`, 无从回显, 这正是它「内容未知」的表现。

三条的 slug 各不相同 (`oauth-login` / `social-login` / `oauth2-spike`), 但**名字不同不等于不是同一件事** —— 它们指向的是同一个 issue, 这才是碰撞判据。

## 2. 逐条处置

**第 1 条 `oauth-login-aaaa1111` (cA, `active`)** —— 有人正在做。这是最直接的一条: 现在很可能有两个容器在同一个 issue 上各自起草。请裁三选一: 合并方向 (我并入 cA 的轨, 或反过来) / 我换方向 / 确认确实是两件事 (那我记录理由后继续)。

**第 2 条 `social-login-bbbb2222` (cB, `done`)** —— 同一件事**可能已经做完了**。这一条按 `active` 同档请裁, 不因为它是终态就默认「不冲突, 继续做我的」。同时要注明: **`done` 这个终态也可能是 GC 产物而不是真的做完** —— 所以也不能反过来默认「已经有人做完了, 我不用做」。两个方向都需要你看一眼实际交付有没有落地。

**第 3 条 `oauth2-spike-cccc3333` (cC, `abandoned`)** —— 同一件事**可能已被放弃**。处置同第 2 条: 按 `active` 同档请裁, 且 `abandoned` 同样可能是 GC 产物而非真的放弃。它的 slug 带 `spike` 字样, 看起来像探路, 若它留下过结论, 直接影响我该不该重走一遍。

**第 4 条 (空 track_id, `unknown`)** —— 读不懂它的 schema, **视同 `active` 处理**。存在性已经确认, 只是内容未知; 我不会因为字段读不出来就把它当作不存在。它对应的就是 `unknown_schema_claims == 1` 这一条。

## 3. 请你裁定 (经 AskUserQuestion, 我不自行放行)

问题: `10CG/Aria#174` 上检出 4 条他方 claim (1 active / 1 done / 1 abandoned / 1 unknown, 详见上表), 我这条轨怎么走?

- **合并方向** —— 我并入既有轨 (主要是 cA 的 `oauth-login-aaaa1111`), 不另起 Spec。
- **换方向** —— 本容器改做别的事。
- **确认是两件事** —— 你判定我这条与它们范围不重叠, 我记录判定理由后继续 A.1。
- **先核实再定** —— 你先去看 cB 的 `done` / cC 的 `abandoned` 是真终态还是 GC 产物, 以及第 4 条那个读不懂的 claim 到底是谁, 核实后再回来裁。

(前提是当前是有人可问的配置。若 `state_scanner.coordination.unattended == true`, 我就不发问, 改为写一条「待复议」记录并置 `awaiting_owner`, 由产品负责人事后复议 —— 这是配置事实, 不由我在运行期推断「现在能不能问」。)

## 4. 我不会做的事

- **不会去释放对方任何一条 claim**, 包括那两条终态的 —— 那是对方的东西, 哪怕它看起来像僵尸也一样。要清理只能由它的 owner-container 或你来决定。
- 不会把 `done` / `abandoned` 当作「无碰撞」直接放行。
- 不会因为第 4 条读不出内容就跳过它。
- 不会重复 acquire —— 本 session 的 claim 已是 active, 幂等生效。

## 5. 裁定之后我这边的退出义务

- 若裁「换方向」并改了 Spec 目录名: **release 旧 track-id + acquire 新 track-id**, 两步都要走, 只 acquire 会留下永不释放的僵尸 claim。
- 若裁「放弃本方向」: 用 `release_gate.py --raw-track-id <同一串> --status abandoned` 释放**我自己**这条。
- 若裁「确实是两件事」: 保留现有 claim, 把判定理由写进 proposal, 继续 A.1 → A.2 → A.3。
