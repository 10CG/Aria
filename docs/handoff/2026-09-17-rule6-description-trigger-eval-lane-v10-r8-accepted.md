---
track-id: rule6-description-change-trigger-eval-lane
owner-container: simonfish/bfe8285d
phase: A.1
status: active
updated-at: 2026-09-17T10:45:43Z
---

# Aria — Session Handoff (2026-09-17) — `10CG/Aria#211` Rule #6 description 维度: post_spec R7 + R8 跑完, owner 裁定接受当前结论 (v10) + 九条待裁项同日裁完 (v11)

> **一句话**: 接上一份 handoff (v8 待跑 R7) —— 周用量窗口重置后跑完 R7 (0C / 3M / 1m, 2 REVISE / 3 PASS) → owner 2026-09-17 裁定「增加轮次 (7 → 8) + 四条现在就改」→ v9 (`a563192`) → R8 (0C / 3M / 0m, 4 REVISE / 1 PASS) → owner 2026-09-17 裁定「接受当前结论, 改完收工」(audit-engine 降级策略第 1 条, `overridden_by_user: true`) → **v10 (`9de3074`) 与 RESULT v9 已双推, 两端 `ls-remote` 核验一致**。post_spec 到此结束。同日 owner 裁完九条待裁项 → **v11 (`a7e852e`)**, 与双子星四个提交合并后为 `85d680b`, 两端核验一致。九条里只有 OQ-1 带实质改动 (0.5 门加一道调用级地板 28/30), 余八条取推荐或现稿。下一步是 Phase B。
>
> **本段最该记住的**: (1) **加固动作自身会带出同类缺口** —— R8 三条 major 里有两条是 v9 的修复动作造成的: SC-9 的存在性断言被我换成定指写法 (「含 `classify_calls.py` 的那一行同时含…」), 定义 bullet 漏转录时该子句在空集上真空成立, SC-9 反而全绿; RESULT 的加固记录溯源过头。改 SC 文字时「存在性 + 实质口径」两半必须同时断言。(2) **同一条文本上两席给出相反结论可以都不错**: qa 席按带存在性断言的**实现**测三类反事实, 全红, 判 closed; code-reviewer 与 tech-lead 按**文字**字面读, 判 major。差别在读法, 修法是让文字与实现对齐。
>
> **Next session 入口**: 读本 doc §0 → `/aria:state-scanner` → §6。

---

## §0 入口 (新 session 优先读)

1. 本轨 claim `rule6-description-change-trigger-eval-lane-bfe8285d` (`claims/bfe8285d/s-b741@1657.yaml`, status=active, 本容器)。**心跳停在 2026-09-13T16:57:29Z**, 已远超 sweep 阈值; 未刷新 —— 刷新要写共享协调 ref, 按 09-16 双子星那次的先例须 owner 授权 (见 §2 第 4 条)。
2. spec v10 @ `9de3074`: `openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md`。基线与实验: `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/` (RESULT.md **v9**; `v6-per-call-health-opus5/` 根下是 v6b 的工具与结果, `v6a/` 是原预登记那一批)。
3. 审计报告: R1–R8 各五席 + 每轮聚合在 `.aria/audit-reports/`。R7 聚合与 R8 聚合末尾各记着对应的 owner 裁定。
4. 主仓 master 本地与两端一致 (`9de3074`), 无未推送提交、工作区干净。
5. 双子星 `simonfish/023236f2` 手上的 `10CG/Aria#195` / `10CG/Aria#199` 本容器不碰。

---

## §1 本次会话已完成 (UTC)

| 时间 | 事件 | 证据 |
|---|---|---|
| 09-16 23:53Z | R7 五席跑完 (首次派发三席撞周限额 429、无报告无改动, 重置后按同一批提示词重跑): 0C / 3M / 1m, R6 对账 closed 10 | `post_spec-R7-2026-09-16T235317-000Z-*-aggregated.md` |
| 09-17 | owner 裁定「增加轮次 7 → 8」+「四条现在就改」→ v9 (SC-9 两个实质锚点 / SC-12 加「含新增 skill」/ T2b 与 T4 的「搬」改「复制」/ `fault_matrix.py` 非空输出目录改报错退出) + RESULT v8 | `a563192` |
| 09-17 09:27Z | R8 五席跑完: 0C / 3M / 0m, 4 REVISE / 1 PASS, R7 对账 closed 3 / partially 1 / open 0, 观察 33 条 | `1728cbb` |
| 09-17 | R7 / R8 两轮共三处席位报告的引用写法机械订正 (只改写法, 不动结论) | `ccfcb41` / `8a9fe35` |
| 09-17 | owner 裁定「接受当前结论, 改完收工」→ v10 修 R8 三条 major + RESULT 升 v9 + 聚合追记裁定 | `9de3074` (双推 MATCH) |
| 09-17 10:45Z | 本轨 handoff + `latest.md` 指针与表行 | `e4874d4` (双推 MATCH) |
| 09-17 | 本轨 claim 心跳按 owner 裁定刷新 (`heartbeat-only`, `outcome: refreshed`, `push_success: true`) | 协调 ref `9e668fb` (只推 origin) |
| 09-17 | owner 裁完九条待裁项 → v11: D2 加调用级地板 + 依据条, 新增 SC-14, 九条裁定逐条追记 | `a7e852e`; 与双子星合并后 `85d680b` (双推 MATCH) |

---

## §2 AI 流程判断 (Rule #10, 请 owner 复议)

1. **R8 入口漏跑竞品 spec 探针**: audit-engine 要求每轮入口跑一次, 我这轮忘了, 聚合时补跑, 结论 `no_sibling_found`, 已如实写进 R8 聚合的抬头。这是疏漏不是豁免。
2. **席位报告的引用写法由我代改**: R7 / R8 两轮共三处 (文内以井号加数字做的条目编号, 以及一处没带仓名的 issue 引用) 不合 standards content-integrity §4.4, 我机械订正并在提交信息里写明「只改写法, 不动结论」。
3. **v10 的三处改动没有再经席位复核** —— 这是 owner 选「接受当前结论」的已知代价。我对每条都做了反事实自检 (10 条可模拟 SC 全绿 / 18 条扰动全部转红), 但自检是我自己写的实现, 不等于独立复核。
4. **claim 心跳**: 曾落后四天未刷新 (status 仍 active)。已如实报 owner, owner 2026-09-17 裁定刷新并保持占用 —— 已执行 (`phase1_gate.py --heartbeat-only`, 协调 ref `9e668fb`, 只推 origin)。**首次调用踩了一个坑**: `--raw-track-id` 传不带容器后缀的 `rule6-description-change-trigger-eval-lane` 会报 `claim_not_found`, 要传 claim 里存的那个带后缀的 id。
5. **沿用未决**: 20 条 query 未经 owner 审阅 (OQ-3); Level 2 与 LEVEL_GUIDE 跨模块规则的关系 (OQ-4)。

---

## §3 关键事实 (均经核实)

- **R8 三条 major 与修法** (三条都由我独立复现过, 修法都过了反事实):
  1. SC-9 丢了存在性断言 ⇒ 整条逐调用健康检查定义 bullet 漏转录时真空成立。修法: 写回「含 `classify_calls.py` 的行 ≥ 1、其中至少一行同时含「两种可能」」。
  2. R7 那条 SC-12 只闭了 SOT 半边, 手册侧「新增 skill 的首个 description 同样要过本场景, 其首个套件随之建立」无 SC 覆盖 ⇒ 删掉它 10 条 SC 全绿。修法: SC-12 加锚该句 (须同时含「同样要过」与「首个套件」)。
  3. RESULT v8 那句「归档的就是加固后重跑的产物」溯源过头。事实: 两份 `matrix-summary.json` 的重跑输出与归档副本逐字节相同 (`cmp` 无差异), 所以它们在加固那次提交里没有变化, 内容最后一次改动仍是 `76959c8`; 同目录 23 份逐用例报告有变化, 差异只在日志文件名与耗时, 判定字段零差异。修法: 照这个说法重写。
- **收敛的形式判据**: R8 的比较键集合与 R7 不相等 (R7 三键 = SC-9 锚点 / T2b 与 T4 措辞 / SC-12; R8 三键 = SC-9 存在性 / D2 套件侧 SC-12 / RESULT 溯源措辞), 且仍有 major ⇒ 结构上不可能判「收敛」。收敛只可能出现在「干净轮 + 下一轮零 rework」。
- **趋势**: R6 6 个 major → R7 3 → R8 3。R7 与 R8 的 major 全是一句话级的文字锚点问题, 无一指向判据本身、运行时描述或实验结论; 三席各自重跑实验, 数值全部复现。
- **v11 的两件事**: (1) OQ-1 的依据是实测分组 —— 基线目录里跑满 20 条 query 的臂共 21 个 (另有 4 次单 query 探针), 真 description 臂 14 个, 健康配置 (独立根 + 单 worker) 的 11 个里 10 个是调用级 30/30, 唯一的 27/30 有一条 query 三次全没触发、按 query 门本来就是 fail; 0.5 与 0.8 在这些臂上从未改变过任何一臂的门判定, 所以单挑阈值定不出优劣, 补地板才有增量。(2) SC-14 第一版锚太松 —— 只要小节里出现过「28/30」就算过, 而「阈值与地板的依据」那一条里也有这个数字, 把门判据里的地板整句删掉 SC-14 仍全绿; 自检的反事实当场抓到, 改成锚在通过判据那一行的三段实质串后三条反事实全红。**这是 R8 那类缺陷的第三次出现, 教训固定为: 新 SC 落地后必须跑反事实, 不跑就是没验。**
- **自检口径 (scratchpad 脚本会话结束即不可用, 重建要点)**: 按 D1 的三行替换重建 `CLAUDE.md` / SOT / 手册的模拟落地, 把 D2 与 D3 正文转录进手册 §场景 4b, 然后逐条判 10 条可模拟 SC, 再跑 18 条扰动 (每条扰动须先断言「确实改动了文本」, 否则算锚点失效)。

---

## §4 待办

- ~~九条待裁项~~ **已于 2026-09-17 全部裁定**, 裁定逐条记在 proposal 的 Open Questions 各项末尾。对 Phase B 有约束的两条: T4 要等 owner 审过那 20 条 query 才执行 (OQ-3); 每个 skill 的新套件都须 owner 审过才能作门, 不设过渡 lane (OQ-7)。
- **Phase B: T0–T8** —— 含 T2b 把 `v6-per-call-health-opus5/` 下四个工具**复制** (基线原件保留) 到 `aria-plugin-benchmarks/tools/trigger-eval/` 并在新位置重跑故障矩阵 (SC-13); T7 走 standards 子模块本地 merge + 双推 + 逐 remote `ls-remote` 核验 + 主仓 gitlink。
- **T6**: 开三张 issue (D5.2 / D5.3 / D5.6) + 给上游 skill-creator 的反馈 (渠道待 owner 定, 修复方向取 iii)。
- **T8**: `10CG/Aria#211` 回帖 (基线结论 RESULT.md v9 + 落地位置), 关单归 owner。

---

## §6 Next

1. Phase B: B.1 起分支 (本轨尚未起分支) → T0–T8。
2. 进 T4 之前先把那 20 条 query 交 owner 审 (OQ-3 裁定); 新套件同样是审过才作门 (OQ-7 裁定)。
3. T6 开三张 issue + 上游反馈; T8 回帖 `10CG/Aria#211`。
