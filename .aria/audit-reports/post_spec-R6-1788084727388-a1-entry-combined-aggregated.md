---
checkpoint: post_spec
round: 6
mode: convergence
verdict: REVISE
converged: false
scope_ok: true
counts: 9C/28M/25m (五席原始合计, 去重前)
clusters: 7C
teams: [aria:tech-lead, aria:backend-architect, aria:qa-engineer, aria:code-reviewer, aria:knowledge-manager]
---

# post_spec R6 (combined) — a1-entry 三份 Spec · **owner 显式加的一轮** (决策单第 3 项, `max_rounds=5` 用尽后)

> **对象**: rework v4 (2026-08-30, owner 六项裁定落版后) 的三份 Spec: 母 `a1-entry-claim-duplicate-work-guard` / 字段 `linked-issue-field-availability` / 探针 `sibling-spec-probe` + 决策单 `.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md`。
> **席位**: config `teams.post_spec` 五个 agent, 但每席给全新镜头 (R3 用过同 team 的正确性镜头; R4/R5 用别的 agent): tech-lead = 实现者试派生 (A.2 dry-run) · backend-architect = 代码宿主与「怎么会红」实证 · qa-engineer = 对抗夹具三态 (真写坏实现去打断言) · code-reviewer = 跨 Spec 接缝 + 三张表回灌 + 条款交叉一致性 · knowledge-manager = 断言**内容**事实核 (非行号存在性)。
> **R6 之前执笔侧已做**: 三条机械不变量 (每个 `SC-NN` 在 SC 表内 / 每个 `--flag` 在 Impact 内 / 枚举拼写唯一) + 行号存在性, 在改前备份上确认能红、改后三份全绿 —— 五席均复跑确认。

## 判定

| 席 | verdict | counts | 一句话 |
|---|---|---|---|
| code-reviewer | REVISE | 3C/11M/13m | R5 点名的九条回灌干净; 但三席约一半 Major 未进清账清单; 三 Critical 全在接缝与「批注 vs 表」 |
| backend-architect | REVISE | 0C/2M/1m | ~60 条 `file:line` 引用逐字实读全部一致; 两条 Major 都是 08-30 新文 (SC-32 撞 argparse `required` / import 顺序敏感, /tmp 实跑复现) |
| tech-lead | REVISE | 6C/9M/7m | 只看三张表试派生 tasks.md ⇒ 6 条 Critical, 4 条同形 (新条款与它旁边那句互斥); **86% finding 落在 08-30 新文**; 「R5 那版收敛为真, 今天这版为假」 |
| qa-engineer | REVISE | 0C/3M/2m | 真写 10+ 坏实现打 SC-22 / SC-1 / SC-4 / SC-18 / SC-19, 全部能分辨; 3 Major = §Why 数字失效 / SC-4(f) 数据流陷阱 (亲踩) / 大小写折叠意见 (供 owner) |
| knowledge-manager | **PASS** | 0C/3M/2m | ~65 条新写断言回源核验, 命中率 ~91%, 承重引用无偏差; 3 Major = 决策单两处数字 + `:235` 出处 (R5 自证但漏清) |

**合并判定: REVISE, 未收敛。** 但走势与 R4/R5 性质不同 —— 见「收敛判断」。

## Critical 簇 (五席去重后 7 个) 与处置

| # | 簇 | 席位 | 处置 (rework v4.1, 2026-08-30 同日) |
|---|---|---|---|
| **R6-C1** | **`--linked-issue` 省略门只豁免哨兵**: 字段 E6 四态表规定 `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` 一律省略, 母 Spec 四处只写「哨兵时省略」且 SC-12 反向写「不得跳过」—— 对存量 14/14 markdown 链接形 (`NO_TOKEN`) 给出相反验收; 且字段 Spec 声称母 §2 已有「从 `--emit-arg` stdout 取实参」一句而母 Spec 零命中, 切换编辑无归属 | CR 接缝 C1 · TL C4 + C5 | **已落**: 母 §2 NEW-01 门改为「不产生合法 canonical 值时 (哨兵/BAD/NO_TOKEN/NO_FIELD) 整参省略」; 新增「两阶段取值」段 (脚本存在 ⇒ `--emit-arg` stdout; 否则按 E6 手工判; **模板行归母 Impact, 一次写死不需二次编辑**); SC-12 场景改为「判 `OK` 且非哨兵但未传」+ 第二臂 (照传整串 ⇒ 复现 K8 ⇒ 红); §6 首行 / rule6 (a) / Impact 同步; 字段 Impact 探针行 + 新表面 #8 + §非目标改为「只负责模式存在, 不编辑母 hunk」; SC-22 ② 加字面 `--emit-arg` |
| **R6-C2** | **探针 Spec「可先于姊妹 ship 全走层 2」与「E0–E6 一条不复制」+「钉死 import `lib.linked_issue_field`」三者不可同时成立**: 姊妹未 ship 时层 0 定位与整套 SC 测试无宿主 | CR 接缝 C2 | **属 owner 权限 (改变 08-23「均非阻塞前置」成文前提)**: 两案上呈 —— (i) 字段纯函数是探针硬前置; (ii) 保留可先 ship, 模块缺席时 `not_established` + `reason="extractor_unavailable"`。已写进探针闸门状态 #3(b) / 字段 O-4 / 决策单 R6-1; 执笔倾向 (i) |
| **R6-C3** | **Level 1 路径「前置 claim 零调用」只在 Impact 括注里**, SC-9 / §2.5 / rule6 (a) 未动, 与 rule6 (a)「必调」互为相反规定 —— 正是 R5 判「不可进 A.2」的形状 (对表的声称, 表没动) | CR 母 C1 | **已落**: §2.5 新增 Level 1 例外 bullet (`phase-a-planner/SKILL.md:67`); SC-9 改两臂 (A) enabled=false / (B) Level 1; rule6 (a) 加「Level 1 与 enabled=false 时零调用」 |
| **R6-C4** | **SC-22 ⑤ 与「②–⑥ 只在切片内求值」互斥**; 唯一自洽落法 (标题插在 `### 步骤执行` 与 yaml 之间) 违反 §2「不塞进 YAML 列表」; 两个实现者得相反结果 | TL C1 · CR M3 · QA m1 | **已落**: 块边界规则改为「②③④⑥⑦ 切片内; ⑤ 切片外独立断言, 对象 = 含 `A.1 - Spec 管理:` 的那个 yaml 围栏 (文件内 7 处, 不可抓第一个)」; 新标题落点钉死「放在 `### 步骤执行` (`:60`) 之前」; Impact `phase-a-planner` 行同步 |
| **R6-C5** | **SC-22 ② 没落 D17 第 2 要件**: 六个独立子串, 一段散文即全绿 (TL 给出三分钟反例); 与 R5 判 Critical 的探针 C1 同形, D17 在发源地没落点 (memory `cite≠apply`) | TL C2 · CR M2 | **已落**: SC-22 ⑦「含一条以 `python3` 起首、含 `phase1_gate.py` 与 `--phase A.1` 的完整命令行, **先做反斜杠续行折叠再判**」; SC-22 头部注明落 D17 ①②③ |
| **R6-C6** | **SC-32 要求 `--heartbeat-only` 可省 `--raw-track-id`, 但 `phase1_gate.py:1187` 是 `required=True`** 且 Impact 逐字写「零改动」; 与 `--phase` 的处置不对称无解释; 触 §非目标; 三种落法欠定 | BA M1 · TL C3 | **已落**: Impact 第二处变更 ⑦ (`required=False` + `_main()` 模式校验; acquire 模式缺参仍 `parser.error` 负控; 与 `--phase` 不对称的理由 = heartbeat 模式下 `--raw-track-id` 没有值可传, 空串会被归一成 sha256 哈希); 第一处变更行「零改动」改为「除 ⑦ 外零改动, 本行改六处」; §非目标加第二处限定; SC-32 补坏实现 1 (argparse 层拒绝) |
| **R6-C7** | **字段 hunk B 让预览骨架默认写哨兵 `none`** = 把「已核实无关联」这条正证据做成写入侧默认值 ⇒ check 恒绿、母 Spec 主机制对每份新 Spec 恒零输入; SC-7 / SC-7a 都测不到 | TL C6 | **已落**: hunk B 改为 SOT 同串 placeholder `` `{<org>/<repo>#<n>}` ``; SC-7a 加负控 (ii)「值不得是哨兵集合成员」; Impact / §1 落版段同步 |

## Major (去重后 20 条) 与处置

| # | 簇 | 席位 | 处置 |
|---|---|---|---|
| M1 | `branch-manager:146` 的 `Part A1` 是已 ship Spec `coordination-claim-lifecycle-and-overlap` 的**部件名**, 非 Phase A.1; R5/M2 误读, rework v4 落成错误改名 | CR M1 | **已撤回** (§2 触发时机 / rule6 #8 / Impact `branch-manager` 三处, 附部件名释义; SC-22 ① 带点 `A.1` + ④ 禁 `--phase B` 足以区分) |
| M2 | SC-23 / SC-14(a) 标「现状必红」为假 —— 代码夹具同一串 X 先 acquire 后 release 今天就绿; 文本层无 SC | CR M4 | **已落**: 两条改为 baseline 即绿的回归守卫 (坏实现 = `derive_track_id` 去容器段 / 匹配键改坏); **新增 SC-34** (文本层: 三处 SKILL.md 各含字面 `A.1 认领时派生的那一串`, baseline 必红) |
| M3 | 母 §Why `:78/:83`「可当场复核」段复核即错 (`:13` 非 `:12`; changes/ 命中 3 非 1; 6i 后中文谓词已不命中本文件 ⇒「真阳」反了) | CR M5 · TL M6 · QA M1 | **已落**: `:78` 改两拼写命令 + 口径注; `:83` 重写; 字段 §Why 加两拼写注 + `:88`→`cc1bdef:75`、`:65/:86`→`:95/:116` |
| M4 | `:235` 引文「逐字」出处仍标 `coordination_probe.py:4-25` (真身 `phase1_gate.py:1047-1049`) —— R5 自证 #1 点名, rework v4 漏清 | CR M6 · KM 母 M1 | **已落** (出处改 `phase1_gate.py:1047-1049`, 探针侧改引 `coordination_probe.py:18-21`) |
| M5 | K6「加 swept 标记」follow-up 无行 | CR M7 | **已落** (follow-up 表第 7 行) |
| M6 | `unattended` 取值路径「容器镜像 / Nomad env」二选一混写, env 三腿又明写不在本 Spec ⇒ 生产进入条件未定义 (R5/code-simplifier M4 未处置) | CR M8 | **已落**: 钉死为 aria-runner 镜像内 `.aria/config.json` 的 `unattended: true`, env 三腿仍 follow-up (决策单台账同记) |
| M7 | 探针 §3 两处仍只写 `无` (`:116` 写死判据 / `:186` 对 E6 的失实引述) | CR 探针 M1 | **已落** (两处改哨兵集合 / E6 四态表引述) |
| M8 | 字段头部「代码落点」缺 `lib/linked_issue_field.py` 与 `.aria/linked-issue-field-grandfathered.txt` | CR 字段 M1 | **已落** |
| M9 | 字段 SC-5 臂数三个值 (五/五/四+e1e2), §4 判据表无「白名单文件缺失」行 | CR 字段 M2 | **已落** (统一六臂; 判据表补第 6 行; 宿主表同步) |
| M10 | §2.1 把 `derive_track_id` 的「超长」写成截断, 实读是整串 sha256 回落 (`sha256-<16 hex>`, 不含 slug/容器段可读形); slug > 55 字符即触发, `archive/` 历史最长 53 | TL M1 | **已落**: §2.1 依据格逐字复述回落条件; §6 加「slug 过长 ⇒ 不可读哈希」已知限行 |
| M11 | §2.4b 四态表第 1 行「键缺席 = 既未传 A 也未传 B」在门控放宽后为假, 且恰是哨兵轨常态 | TL M2 | **已落** (改为单条件「未传 `--linked-issue`」, `--include-terminal` 正交) |
| M12 | §5.2 不穷尽 §2.3 选项集: 「并轨」与「done 档复用对方产出」无 release 行; `active` 档「我去释放对方的 claim」无可执行动作 | TL M3 | **已落** (§5.2 补两行; §2.3 `active` 档措辞改为人工协作动作 + 无命令声明) |
| M13 | 「放弃整个 issue = 逐方向 release」没给枚举方向的机制, 而机制存在 (overlap 不按 container 过滤) | TL M4 | **已落** (§5.2 第 2 行补枚举机制, 引 `collision.py:271-279`) |
| M14 | `--no-push` 修复是 ship 硬前置, 却不在「前置依赖」也不在闸门; 该分支未推、非 `origin/master` 祖先 | TL M5 | **已落** (头部前置依赖新增行 + 闸门状态表 #7 + 未做 #6 升格) |
| M15 | 探针 SC-17「全文恰 2 次」与同文件新增契约节相冲 | TL M7 · CR 探针 m2 | **已落** (分块计数 + 负控「其余 0 次」; Impact 契约节禁前缀字面) |
| M16 | 无 SC 钉 `execution-modes.md` 新契约节存在, SKILL.md 指针可悬空; 母 rule6 #10 同形 | TL M8 | **已落** (探针 SC-20 加 (ii) 臂; 母 rule6 #10 substitute 加存在断言) |
| M17 | D17 三要件无适用范围, ②③ 对骨架块不适用; ① 的围栏边界规则缺 | TL 字段 M9 · CR m1 | **已落** (D17 重写: 范围 + 围栏规则 + 「引用本条的 SC 须写明落了哪几件」; SC-7a 注明只落 ①) |
| M18 | 探针双 `sys.path` 插入顺序敏感 —— `state-scanner/scripts/lib/` 今天就存在, 反序 ⇒ `ModuleNotFoundError` (BA 在 /tmp 实跑复现) | BA 探针 M1 | **已落**: §3 唯一代码块 (顺序钉死) + 已知限重写 + **新增 SC-21** (import 顺序断言); Impact 段不再复述 |
| M19 | 字段 SC-4(f): E5 哨兵判定若复用 E4 已 strip 的元素, `none ` 恒判合法 (QA 按文实现亲踩) | QA M2 | **已落** (E5 明写「判定对象 = E3 原始 token 串」; SC-4(f) 补该坏实现) |
| M20 | 决策单两处数字: 反驳 1 的 grep 计数 (今天 17 非 15) / 修复段测试计数 (静态 1409→1425, 非 1393→1409) | KM 决策单 M1/M2 | **已落** (反驳 1 改为「14 份 archive 稳定子集」口径 + 当日观测说明; 测试计数改两口径并注明来源) |

**未采纳 / 待裁 (Major 级)**: QA M3 (字段名 E0 大小写折叠, GitHub 原生术语 `Linked issues` 假阴性) → **字段 O-5 / 决策单 R6-2, 待 owner**; TL 收敛判断建议「换执笔席清账」→ **未采 (主控一次落版)**, 母闸门状态表 #8 留痕请复议, 决策单 R6-3。

**minor (25 条)**: 行号勘正批 (`:66`→`:67` ×3 / `:260`→`:259` / `_run_gate_impl` 区间 / `:133-140` / `:237` / D4 `:188` / FIX-04 自指 / `basicConfig` 范围 / 第 12 行→13 行 ×3) 全部已落; SC-11「四档选项集不同」→「渲染不同, abandoned 与 active 共用选项集」已落; SC-15 负控夹具前缀约束 (QA m2) 已落; SC-22 ⑤ yaml 围栏定位提示 (QA m1) 已落; 探针「请 R4 优先审」残留 / 段尾句 / 「旧 SC-NN」说明 / `read_only` 来源 / SC-20 锚定起首 (m7) 已落; 字段「请 R4 优先审」×2 / 10 条 check 注 / `:469` 失效引文已落; **未动**: 字段 `custom_checks.py:122-123`→`:123-124` (锚点未命中, 留待定向复核) / `GRANDFATHERED` 作机制名的用法 (篇幅项) / CR 流程 m1 → 决策单已补 R5 code-simplifier 13 项台账。

## 席位分歧 (主控独立裁决)

- **「设计侧是否已收敛」**: QA / BA / KM 同意 (「新文本第一次被对抗夹具照面时的正常边界问题」); CR「不同意但距离很近」; TL 不同意 (86% 自伤率)。**主控判**: 两边说的是两个版本 —— R5 五席审的是 v3+清账那版, TL 说得对: **1A 是结构重写、D17 是当天新立当天三处引用**, rework v4 不是「机械清账」。v4 新写文本的缺陷占比 (CR 39% / TL 86% / QA 全部相关) 明确越过 memory `marginal-return-negative` 的 1/2 拐点; **但七簇全是文本层动作** (五席给的处方都到字面级), 不是设计返工。⇒ 本轮按处方一次清账 (v4.1), 之后**不加 R7**, 只做一次定向复核 (新席位, 只核七簇是否真落 + 清账是否引入新矛盾)。
- **TL 建议换执笔席落 6C/9M**: 未采 (主控一次落版), 理由 = 七簇里六簇有字面级处方, 换席交接成本高于收益。**与 owner 既往「换人执笔」处方相左, 已在母闸门状态表 #8 留痕请复议。**
- **KM verdict PASS vs 其余 REVISE**: 事实核镜头下承重引用无偏差, 与其他镜头的结论不冲突 (它们抓的是条款互斥与接缝, 不是引用不实)。R5 factcheck 席 22 条不实 → 本轮 KM 65 条里 ~6 条不实, **引用面明显收敛**。

## 收敛判断

- **不是 R7 的理由 (五席一致)**: 每席都给了可机械复核的处方; 三条 grep 不变量已绿; 再跑通用轮只会在新清账文本上产出下一批同形缺陷。
- **本轮 fix 引入的缺陷占比** (memory `marginal-return-negative` 的判据): TL 口径 86% / CR 口径 39%; 主控取 TL 口径为准 (它的镜头 —— 试派生 —— 正是能看到「新条款与旁边那句互斥」的那一个)。**这意味着 v4 落版方式 (结构重写 + 新立类级规则 + 三份同批改接缝, 同一执笔) 本身在制造缺陷**, 不是审计席不够。
- **v4.1 清账之后的状态**: 三条不变量 PASS (母 34 SC / 探针 21 / 字段 9 全部有表行; 行号引用 80 + 26 + 23 条全部存在); 残留 grep 干净 (`派生形`/`回落形`/`track_form`/`spec_slug` 只在撤销说明; `Part B1` 只在部件名释义; `请 R4` 0)。**定向复核席 (`…-cleanup-verification.md`) 的结论决定能否交 owner 批准进 A.2。**

## 下一步 (非裁定 — Rule #10, AI 不自行选)

| # | 待 owner | 选项 |
|---|---|---|
| 1 | **R6-1 探针依赖方向** (接缝 C2) | (i) 字段纯函数 = 探针硬前置 [执笔倾向] / (ii) 探针可先 ship 但模块缺席时恒 `not_established` |
| 2 | **R6-2 字段名大小写折叠** (QA M3) | (i) 折叠 (不放宽单复数) [QA 倾向] / (ii) 维持不折叠 |
| 3 | **R6-3 清账执笔** | (i) 接受主控 v4.1 一次落版 + 定向复核 [已按此做] / (ii) 换执笔席重做 |
| 4 | **R5 code-simplifier 台账里的 4 项范围决定** (决策单): 删 `--heartbeat-only` 改入口重跑 acquire / `unknown_schema_claims` 整条转 follow-up / 白名单改注册行参数 / editlist 对账表迁回 SOT 状态列 | 各自采纳或拒绝 |
| 5 | **`--no-push` 修复的 ship** (aria 分支 `fix/phase1-gate-no-push` @ 007d355, 未推): 它是母 Spec 的硬前置 | 授权推送 + PATCH 发版 / 先不推 |
| 6 | 定向复核 PASS 后: 批准三份 Spec 进 A.2, 或指定再改 | — |

## 报告索引

五席: `post_spec-R6-1788084727388-a1-entry-combined-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md` · 定向复核: `…-cleanup-verification.md` · 决策单: `.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md` · R5 聚合: `post_spec-R5-1787840920000-a1-entry-combined-aggregated.md` · 三份审计轨 (append-only): `a1-entry-claim-audit-trail.md` §6–§7 / `linked-issue-field-availability-audit-trail.md` §2–§3 / `sibling-spec-probe-audit-trail.md` §2–§3。

## 定向复核结论 (追记, 2026-08-30 同日)

`.aria/audit-reports/post_spec-R6-1788084727388-a1-entry-combined-cleanup-verification.md`: **PASS** · `2 未落 / 1 部分落 / 1 新矛盾`。8 簇里 6 簇实文落地 (逐条给当前行号 + 逐字), 2 簇 (探针依赖方向 / 字段名大小写折叠) 按 Rule #10 正确上呈; 28 条 Major 逐簇有实文落点, **无一条停在「Impact 括注声称 SC 已改而 SC 没动」的 R5 形状**; 九对交叉一致性八对自洽。**唯一新矛盾 N-1** (决策单台账写「`unattended` 取值路径已钉死为 `.aria/config.json`」而母 §2.3 仍写「容器镜像 / Nomad task env」—— 清账当轮新写的跨文档声称在目标处不成立, memory `cross_doc_claim_verify_at_target`) 与两条 minor (探针 `:236-237` 锚点 / 字段 `FIX-07` 承接锚点) **已于同日闭合**, 三条不变量复跑 PASS。QA m2 / BA m1 两条 minor 复核席断线前未核, 主控已按处方落 (SC-15 负控夹具前缀 / helper 抽取建议未采)。

**主控结论**: 三份 Spec 可交 owner 批准进 A.2, 前提 = owner 裁 R6-1 (探针依赖方向) 与 R6-2 (字段名大小写折叠); 不再加通用审计轮。
