---
checkpoint: post_spec
round: 3
converged: false
overridden_by_user: false
incomplete: false
verdict: REVISE
---

# post_spec R3 (combined) — a1-entry rework v3 + 两份新拆子 Spec

> **模式**: convergence · **席位**: 5/5 (配置 roster, 零裁量) · **scope_ok 5/5 true**
> **联审 (combined mode)**: 母 Spec 第 **R3** 轮 + `linked-issue-field-availability` / `sibling-spec-probe` 各自第 **R1** 轮
> —— 依据 memory `feedback_combined_mode_sister_spec_audit_value`「≥2 sister-Spec 联审抓 X-Critical, single-Spec 漏率 100%」。本轮结果**验证了该判断**: 3 个 critical 里 **2 个是跨 Spec 的**, 分开审必漏。
> **审计对象**: 主仓 commit `027a50f` (工作树干净) · aria 子模块基线 `origin/master` = `d50f9c3`
> **各席 verdict**: TL REVISE 3C/10M/4m · CR REVISE 1C/4M/10m · QA REVISE 0C/5M/5m · KM REVISE 0C/2M/1m · BA **PASS_WITH_WARNINGS** 0C/3M/4m
> **报告**: `post_spec-R3-1787652625000-a1-entry-rework-v3-combined-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md`

## 判定

**REVISE, 未收敛。** 去重后 **3 个 critical 簇 + 19 个 major 簇**。

**R2 的三条 critical 处置**: C-A 随 §1 迁出并在子 Spec 解 (**closed**, CR/KM/BA 三席独立确认迁出零丢弃) · C-C carry-id 断链 (**closed**, 由其发现者 KM 席复核) · C-B 连坐 release (**只闭一半 ⇒ 见 C1**)。

### 🔑 本轮的形状: **过半新缺陷由本轮的修复动作自身引入**

| R3 critical/major 簇 | 来源 |
|---|---|
| C2 allowlist × 分发面 | **主控 round-2 宿主改判**引入 |
| C3 E0–E6 实现无归属 | **拆 Spec 这个动作本身**引入 |
| M4 审计轨「按字节搬」不实 | **本轮搬迁动作**引入 |
| M5 `母 Spec :88` 悬空 | **母 Spec 的迁出删掉了姊妹的证据** |
| M7 SEAM-2/3 两侧自述未回灌 | **本轮接缝修复**只修单侧 |
| M13 `phase-b-developer:88` 先例误引 | **主控 round-2 指令**误读 |
| M17 `A.0` 锚点命名冲突 | **本轮 FIX-13 落地**引入 |
| C1 / M1 / M2 / M18 / M19 | R1/R2 遗留, 本轮未闭或首次被发现 |

⇒ 粗算 **≥8/22 簇是本轮 fix 的副产品**, 且 **3 个 critical 里 2 个是**。memory `feedback_audit_marginal_return_goes_negative` 的判据 (「本轮 fix 引入的 major 占比 > 1/2 即到拐点」) **已接近命中**; memory `feedback_stop_adding_rounds_when_major_count_flattens` 的判据 (major 不降) **命中**: R2 17 → R3 19。

**⚠️ 口径诚实声明**: R2 审的是**一份** 71KB 的 Spec; R3 审的是**三份** 共 256KB (含审计轨)。表面积扩大 ⇒ finding 数上升有一部分是口径变化, **不能直接判「更差」**。但 (a) critical 仍为 3 且**换了一批**, (b) 过半新簇可追溯到本轮动作, 这两点与总体大小无关。

## Critical 簇 (3)

| # | 簇 | 席位 | 要点与实读证据 |
|---|---|---|---|
| **C1** | **C-B 只闭一半** — 母 §5.2「走完循环 ⇒ D.2b release」经 `release_claim_by_track` 释放 **ALL matching** ⇒ 方向 1 收尾**连坐**掉同 issue 下仍在制的方向 2/3; SC-27 仅两臂, 结构性抓不到 | TL-C1 | `claim_lifecycle.py` docstring 逐字「**ALL matching active claims are released**」(主控复核实读)。R2/C-B 的另一半 (探索性放弃) 已闭 |
| **C2** ⭐ | **`GRANDFATHERED` 6 条 Aria 本仓硬编码路径 × 随 plugin 分发的脚本** ⇒ 每个采用方注册后陈旧守卫 (a)「路径不存在」全命中 ⇒ **exit 1 恒红**; 且 fix 文案让采用方去改 plugin 分发件; SC-5(c) 恰把该失败模式断言成期望行为 | TL-F1 · CR/LIFA-C1 (**两席独立同判**) | 根因 = 主控 round-2 把探针宿主改判到分发面, 与 allowlist 的**仓本地性**冲突 —— 改对了一半造出另一半 |
| **C3** | **E0–E6 抽取规则实现无归属** — 三条约束不可同时满足: (逐字采纳姊妹 E0) ∧ (不得内含第二份实现) ∧ (不改 state-scanner)。姊妹唯一宿主是**项目根扫描的 CLI check** (作用域仅 `changes/`, 无导出 API); 探针要的是**远端 ref 上任意 blob 含 `archive/`** 求四态 ⇒ 探针「姊妹非阻塞」**在实现层为假** | TL-P1/F2 | 这是主控点名要 TL 找的「第四条接缝」。**拆 Spec 动作本身**制造的 |

## Major 簇 (19; ⭐ = 多席独立同判)

| # | 簇 | 席位 |
|---|---|---|
| M1 | `--heartbeat-only` 三处调用形态全缺 `--phase`, 而 `phase1_gate.py:1191` 是 `required=True` ⇒ 照字面实现**第一次实跑被 argparse 拒**, 到不了 heartbeat 逻辑 (主控实跑复现) | BA-M1 |
| M2 | D4 (`:454`) 仍写「匹配键**改**」, 与 `:188`「以增并存变体为准」+ D16 矛盾 (三处只统一了两处) | BA-M2 |
| M3 | `linked_issue_overlap` 由恒 `[]` 放宽为 `list\|null` 影响 **Phase B 消费面**; 母 Spec 自述「Phase B 两入口都不带」指的是 `--include-terminal`, 与 `--linked-issue` 混淆 —— 实读 `phase-b-developer/SKILL.md:93` = `[--linked-issue "<repo>#<n>"]` **可选传** | BA-M3 · TL-M3 |
| M4 | 母审计轨「按字节搬运, 未重写任何一句」对 §5 **为假**: 与已提交前身比 22/29 行找不到 (该表本轮先按 `d50f9c3` 重测重生成再搬)。两子 Spec 的搬运**无已提交前身可 diff ⇒ 结构性不可独立证伪** | CR/M-M1 |
| M5 ⭐ | 「母 Spec `:88`」在**任何已提交 SHA 上都不是那行** (真身 `cc1bdef:75`); 字段 spec 自引 `:65`/`:86` 实为 `:95`/`:116`。**母 Spec 的迁出亲手删掉了姊妹 Spec 引用的证据** | CR/LIFA-M1 · TL-F3 |
| M6 ⭐ | `.aria/state-checks.yaml` 实测 **11** 条非 Spec 称的 10 条 (第 11 条由**对方容器**同 session 的 `2ae012f` 引入); 形态 (iii) 实为 3 条,「最近两条新增」为假 | CR · KM-3 · BA-m3 · QA-F8 (**四席**) |
| M7 ⭐ | SEAM-2/3 只修在探针 §3, **两侧自述未回灌** ⇒ 同一 commit 内三处互相矛盾 (字段 spec 仍断言探针「无围栏谓词 / 三态无 `BAD_TOKEN` 格」; 探针「新表面」仍自陈「单方面三态 / 未交叉核对」) | CR/LIFA-M3 · CR/SSP-M1 · KM-2 |
| M8 | heartbeat 的唯一挂载点 (`/state-scanner` 入口) 在**审计轮内结构性缺席** (实读 `execution-modes.md` 两模式块轮内均无 `/state-scanner`); §2.3 把常态写成「漏跑一次」 | TL-M1 |
| M9 | `--heartbeat-only` 若走 `_gated(_source=production)`, 会把 enabled 的 `coordination-gate-invocation` check 变**恒绿** (假绿) | TL-M2 |
| M10 | §5.1「形态是否含 slug」自称可机械判定但**无判定式**且有反例 (`fix-issue-149-<uuid>`); 三条 SC 的夹具预标形态, 对此免疫 | TL-M4 |
| M11 | §6 缺口表迁出时丢掉「**部分**」限定词 (探针自测覆盖率 90.5%, 非全覆盖) | TL-M5 |
| M12 | 母 `:212` 引 `phase-b-developer:88` 作 telemetry 先例**不成立** —— 实读该行是**布尔谓词**「本 session 是否已跑 phase1_gate」, **不携带 track_id**; track_id 在 `:92` 另取自 carry-id ⇒ 对 R2-CR-M1「回到依赖 AI 记性」的反驳前提不成立 | TL-M6 (**主控 round-2 指令误引, 主控担责**) |
| M13 | 探针 `"bad_token"` 泄漏出 §7 的 5 值枚举 (SEAM-2 修法未传导到 §7) | TL-P2 |
| M14 | 探针 SC-18 三臂**无一验 E0 谓词 2 (围栏排除)**, 且姊妹实测真实语料差异 = 0 ⇒ 漏实现围栏的实现也全绿 | TL-P3 |
| M15 | 母 §2 + SC-22 的新锚点 `A.0 - REQUIRE claim` 与 `spec-drafter/SKILL.md` 既有 `A.0` = **state-scanner** 步骤标签命名冲突 (`:30`/`:369` 等) | QA-F1 |
| M16 ⭐ | **SC-2 恒绿** — 既有 `test_release_by_track.py:533` 传两个**不含容器段**的手写串**今天就绿** ⇒ SC-2 钉不住它声称钉的 R1-fix 回归 (容器段被丢弃) | QA-F2 (主控实读复核) |
| M17 | **SC-7 恒绿** — 既有 `test_sweep_stale_cross_container_fresh_untouched` (`:380`) 已覆盖同场景且**全程不调用新 heartbeat 机制** ⇒ SC-7 零新代码路径覆盖 | QA-F3 |
| M18 | SC-29 非纯装饰但 fixture (own claim = active) **未命中本 Spec 真正新开的风险面** (own claim = terminal + `--include-terminal`) | QA-F4 |
| M19 ⭐ | 字段 spec 的 SC-1~6 / SC-8 全部标「代码」类却**无声明测试宿主** ⇒ **直接复发该 Spec 自己要治的 C-A 病根**「无实现宿主」 | QA-F6 · KM-1 (母 `session-handoff.md` §2.3 应为 **§2.3.8** 归入本簇的同形: 引错受影响 SOT 章节) |

## 本轮实读**证实**的部分 (下轮免重复)

- **两段 owner 裁定 blockquote `diff` 逐字节零差异** (CR 席独立跑 diff)
- **(iii) 撤销的四落点全撤、零残余** (CR)
- **约 60 处 aria `文件:行号` 逐行 `cat -v` 全中** (CR); BA 另有 40+ 条逐字核实全成立
- **迁出零丢弃** —— R2 迁往两子 Spec 的 11 项逐项落地核过 (CR) · BA 与 KM 独立同判 (**三席一致**)
- **探针 SC-18 三臂九个数字**由 CR 独立全量重算**一个不差**; 字段 spec 的 **E0–E6 规则原型 149 篇重跑**与其 §Why/§5 逐格一致
- **SC-29 修得对** (TL: 负控可构造, 两侧无孤儿) —— 即 SEAM-1 的修复成立
- BA/CR 两席各自**亲自实跑复现**了 Spec 自称的实测 (字段 spec 两种 import 写法 / 探针 `ls-remote --symref` 四组合), 输出与 Spec 逐字一致

## 收敛判定 (convergence, `max_rounds=5`)

- R2 → R3: critical **3 → 3** (全换: 旧 3 条 2 闭 1 半闭, 新 3 条其中 2 条本轮引入); major **17 → 19**。
- **major 不降 ⇒ memory `stop-adding-rounds` 判据命中**; **过半新簇是本轮 fix 副产品 ⇒ memory `marginal-return-negative` 判据接近命中**。
- 按字面 `max_rounds=5` 还剩 R4/R5。**但主控不建议直接加轮** —— 三轮 rework + 一轮拆分后, 每轮修复引入的同形缺陷占比未下降, 且本轮两条 critical 直接源于「拆 Spec」与「主控 round-2 指令」这两个**本轮新增的动作**。

## 主控处置建议 (非裁定, Rule #10 留痕 — **AI 不自行选**)

**已知的可分离性**: 19 个 major 里约 12 条是**机械事实订正** (行号 / 计数 / 措辞 / 枚举同步 / 自述回灌), 修它们不引入设计裁量; 剩下 3 critical + ~7 major 是**设计问题**, 需要方向裁定。

呈请 owner 在以下之间裁 (**AI 不预选**):

1. **(a) 继续 R4** —— 先由主控清完 12 条机械项, 再换新席跑 R4。风险: 前三轮实证「每轮 fix 引入约等量同形缺陷」, 本轮该比例仍 >1/2。
2. **(b) 收缩交付面** —— 三份 Spec 里**只保留母体的 A.1 认领 + track-id 契约**进 A.2/A.3, 两个子 Spec 降级为 backlog issue (它们各自的 C2/C3 都源自「拆」这个动作)。这等于**部分回撤方向 b**, 须 owner 明示。
3. **(c) 直接进 A.2 并把 3 条 critical 转为 A.2 的承重任务** —— 理由: C1/C2/C3 都是**实现层归属问题** (谁 release / allowlist 放哪 / E0–E6 谁导出), 在 A.2 任务拆解时天然成形, 继续在 Spec 文档层打磨可能就是 memory `no-ruling-shortens` 说的「净负」。
4. **(d) owner 另裁**。

**另请 owner 复议两项主控自主流程判断** (Rule #10 要求留痕):
- ① 三份 Spec 的「实读清单」切出审计轨 (仿姊妹 Spec 2026-08-07 owner 裁定先例) —— CR 席判「**方向对, 执行有缺陷**」(见 M4), 措辞须订正;
- ② 字段 spec 的 `GRANDFATHERED` allowlist 机制 —— CR 席判「**机制可接受, 当前落法不可接受**」(见 C2)。
