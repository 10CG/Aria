---
checkpoint: post_spec
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T11:22:42.518Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [code-reviewer]
---

# post_spec R6 — code-reviewer 席 (Phase 1 规范合规 + Phase 2 质量)

被审对象: proposal v7 @ 主仓 `c3a5903`; RESULT.md v6 与基线目录原始产物; 背景为 R5 聚合报告末尾「降级策略裁定 (owner 2026-09-15)」与本席 R5 报告。只审不改: 唯一写入是本报告; 反事实与假 `claude` 实跑的脚本和产物都在 session scratchpad (`scratchpad/r6/`), 仓库文件未动。独立性: 同目录已有一份别席 R6 报告落盘, 未打开。

代码核对面: aria-orchestrator `237045a` (= 主仓 gitlink); skill-creator 插件缓存 `bb335391eb83` 的 `scripts/run_eval.py`。下文数字都来自实跑, 命令与输出见「实跑记录」。

## R5 对账

范围: 本席 R5 报告 Findings 的 3 条。

| 序号 | R5 条目 | v7 落点 | 状态 | 核对依据 |
|---|---|---|---|---|
| 1 | [major] testing/proposal.md §D2: 作废第二情形「缺 query 条目、runs 少于 3」对 `run_eval.py` 不可达, 环境失败落成 fail, 执行者去改一份正确的 description | §D2「同批参照臂」(L51) + 作废改为三情形 (L56) + fail 只在参照臂过门时判 (L57) | partially | 三个作废条件都可达、都可观测 (下表); 但本条的伤害路径仍在: API 报错 / 非零退出 / 超时都静默记成未触发, 参照臂只接得住同时落在它自己 should-trigger 段的故障 (假 `claude` 实跑 S1 / S2 / S3 与 v2 回放)。转 Findings 第 1 条 |
| 2 | [minor] testing/proposal.md §Success Criteria: v5 自主条款、CLAUDE.md 指向句、D6「GLM 未验证」无 SC | SC-12 (L153) | closed | 反事实 (内存中替换): 删 SOT 新句的自主条款 → 红; 「放弃整个任务、不提交任何改动」改为「跳过这一部分」→ 红; 删 CLAUDE.md 指向句 → 红; 删「写明是哪个 skill、为什么要改」→ 红; 原样 → 绿 |
| 3 | [minor] documentation/proposal.md §D1+§D6: SOT 新句带「依 OQ-7 / OQ-9 裁定」草稿括注; D6 引 RESULT v4 | SOT 新句 (L41) 已无内部编号; D6 (L110) 改引 v6; 新增 SC-11 机械兜底 | closed | SC-11 五个正则对全部待转录文本 (CLAUDE.md / SOT §2 新句、§3 边界注、§4.1、§6 第三条、D2 与 D3 正文) 均 0 命中; proposal 里 RESULT 版本引用 8 处 (L9 / L16 / L50 / L53 / L70 / L110 / L125 / L139) 全为 v6。我 R5 修法里「头部重核清单加 §D6」未采纳, 放观察第 10 条 |

合计: closed 2 / partially 1 / open 0。

**作废三情形逐条 (任务第 1 项)**

| 作废情形 | 可达? | 可观测? | 证据 |
|---|---|---|---|
| 同批参照臂过不了门 | 可达 | 参照臂 json 的 `pass` | 基线 v1 (共用根 + 4 worker): 改动前的 old 臂门 FAIL (should 1/10) → 按 v7 判作废, 判对了 |
| 门通过而负控 ≥ 6/10 | 可达 | 负控 json | 基线 v2 (名字泄漏): 负控 should 命中 9/10; 被评为 old 或 poscontrol (门 PASS) 时 → 作废 |
| stderr 出现 `Warning: query failed` | 可达, 但只在 worker 抛异常时 | 执行者自己截了 stderr 才看得到; D3 第 6 行产物形状不含 stderr, 基线目录 `.err` 0 个 | 假 `claude` 实跑 E4 (PATH 里没有 claude → `FileNotFoundError`): 6 行 Warning; E1–E3 (API 报错结果帧 / 非零退出 / 超时): Warning 0, json 与真没触发同形 |

「环境故障只能靠参照臂识别」(RESULT v6 头部原话; proposal L51 写成「必须有它, 因为 … 无法区分」) 只对一部分故障成立:

- 套件前 10 条 should-trigger、后 10 条 should-not; `--num-workers 1` 下按套件顺序执行, 同一 query 的 3 次 run 连着跑 ⇒ 每臂后半程只跑 should-not。should-not 上的故障记成「未触发」= 判 pass, 参照臂在结构上看不见。
- 参照臂与被评臂各用独立项目根、独立进程: 一臂故障、另一臂正常时, 参照臂照常过门, 被评臂按 fail 处置。串行跑 (Impact 明列「串行约 32–59 分钟」) 时参照臂对被评臂时段内的故障零保护; 并行时各臂进度也会拉开 (v5 同时起跑, 结束时间相差 4 分 23 秒)。
- 假 `claude` 实跑 (真实 20 条套件、3 runs、单 worker、每臂独立根; 实跑记录第 7 条):
  - S3: 只有被评臂在第 6–8 次调用 (第 3 条 should-trigger 的三次 run) 报错, 被评 description 本身正确 → 被评 9/10 门 FAIL、参照过门、负控 0/10、无 Warning ⇒ v7 判 **fail**, 处置只剩「改 description / 改套件 / 升级 owner」。
  - S1: 被评是过宽 description (每条都触发), 只有被评臂从第 30 次调用起报错 → 被评门 PASS ⇒ v7 判 **pass**。同一被评臂无故障的对照 S0 判 fail。
  - S2: 同 S1, 但三臂同时从第 30 次调用起报错 ⇒ 仍判 **pass**: 同时发生的故障只要落在后半程, 三个作废条件都不响。
  - S4: 三臂同时在第 12–20 次调用报错 (前半程) → 参照臂 FAIL ⇒ 作废。v7 的设计接得住的是这一类。
- 真实数据回放 (按 v7 规则判基线各轮; v1.71.1 → v1.73.0 这次改动的参照臂 = old): v1 → 作废 (对); v3 → pass (对); v5 → pass (对); **v2 → fail**: old 过门, new 在「phase d.2 该做的事 …」这条 0/3 门 FAIL, 负控 9/10。负控已经给出「这轮测不准」的信号, 但门没过, 负控作废不适用, 于是判 fail。v2 违反前置第 2 条 (合成名未中性化), 合规运行不会再有名字泄漏; 这里说明的是判定逻辑本身: 作废条件本来就是为「前置没排除掉的未知失效」设的, 负控这个现成的无效信号在 fail 分支被丢掉了。

## Findings

- [major] testing/proposal.md §D2 (issue): 作废三情形可达, 但参照臂只接得住同时落在其 should-trigger 段的故障: API 报错与超时静默记未触发 (实跑), 只落被评臂则正确 description 判 fail, 落 should-not 半程则过宽判 pass; 负控 ≥ 6/10 仅门通过时作废 (v2 回放判 fail)。
- [major] documentation/proposal.md §Impact+§D5.6 (issue): 「放弃后记为 container_crash 且默认自动重试、反复告警」与代码不符: 扫描按 attempt=1 行去重不重派, reconciler 只重试卡住的 S5_AWAIT, failure_analysis 默认关闭且不重试 container_crash; D5.6 会把错前提写进跟进 issue。
- [minor] documentation/proposal.md §D5 (issue): D5 第 7 项「编排器不消费 runner 结果枚举」漏删; 头部 / T6 / SC-6 / 交付物均为三张, 提交说明称已并入 D5.6, 与 owner「唯一跟进 issue」裁定相悖; Phase B 照 D5 会多开一张且无 SC。

计数: critical 0 / major 2 / minor 1。minor 列入 Findings 的理由: 它让 D5 正文与 T6 / SC-6 / owner 裁定互相矛盾, Phase B 执行者照哪边做都有一边不满足; 修法是删一行, 不需要为它另开审计轮。

## Findings 证据与修法

1. **§D2: 参照臂接不住的两类环境故障 (major; R5 第 1 条 partially)**
   - 证据见「R5 对账」表后的逐条与实跑记录第 6–8 条。机制: `run_eval.py` 第 88 行 `claude -p` 的 stderr 接 DEVNULL; 第 101 行超时退出循环后第 178 行返回 `triggered` (此时恒为 False); 第 170–171 行遇 `result` 帧直接返回 `triggered`; 只有第 223–225 行的异常分支打 Warning。所以 API 报错、限流、鉴权失败、超时都不打 Warning。
   - 影响: (a) 只落在被评臂的故障 → fail → 处置 (1) 让执行者去改一份正确的 description, 改完重跑通过就带着「4b pass」ship —— 就是 R5 这条的原始伤害, 触发面变窄了但仍可达; (b) 落在 should-not 半程的故障 → 过宽改动判 pass —— D2 承诺的两类破坏之一在故障时静默失守, 这是引入参照臂后新暴露的一面。
   - 修法 (只改文字, 不需要新的实跑): (1) 「负控 ≥ 6/10 ⇒ 作废」去掉「门通过而」这个前提 (作废与 fail 都不得 ship, 安全方向不变), 同步改 L55「不会落到作废」; (2) fail 时先把被评与参照两臂原样同批重跑一次, 仍是「参照过门、被评 fail」才进处置 (1)(2), 否则作废 (成本只在 fail 时发生, 约 10 美元); (3) 按调用识别故障: 前置第 3 条本来就要用 `claude` 垫片, 让垫片把每次调用的最终 `result` 帧 (至少 `is_error`) 追加到日志, 任一 `is_error: true` ⇒ 作废 —— 这一条同时覆盖 should-not 半程与单臂故障 (帧形状须在写手册前实测一次); (4) D3 第 6 行产物形状补「各臂 stderr 与垫片日志」, 否则第三作废条件事后无法审计。做了 (3), (2) 可以省。

2. **§Impact + §D5.6: 「默认自动重试」不成立 (major; v7 新增的事实断言)**
   - 原文: Impact (L126)「代价: runner 开跑后碰到这类任务, 会被打进 S_FAIL (失败类型记为 `container_crash`) 并默认自动重试、反复告警, 直到 owner 手动阻止该 issue 自动派发」; D5.6 (L105)「放弃后的失败类型记为 `container_crash` 且默认自动重试」。
   - 代码 (aria-orchestrator `237045a`, `hermes-extensions/aria-layer1/aria_layer1/`):
     - 「记为 container_crash」成立: `extension.py` `_handle_s5_await` 对 terminated 且 exit_code 非 0 一律返回 `S_FAIL` + `FailReason.CONTAINER_CRASH`。
     - 扫描不重派: `extension.py` `_phase1_scan_and_seed` 对已有 attempt=1 行的 issue (任何状态, 含 S_FAIL) 直接跳过; 注释说明 schema 还带 `UNIQUE (issue_id)`。
     - reconciler 的 RETRY 只针对卡住的 S5_AWAIT 行 (`reconciler.py` Decision.RETRY「row stays in S5_AWAIT」), 不碰 S_FAIL 行。
     - 唯一能对 S_FAIL 行重派的是 failure_analysis 的 `create_rework_dispatch(mode='retry')`: 默认关闭 (`reconcile_runner.py` 未设 `ARIA_FAILURE_ANALYSIS_ENABLED` 即返回 None, reconciler 注释「skipped entirely when failure_analysis_llm DI is None (default)」; `deploy/aria-layer1-reconcile.nomad.hcl` 的 env 块与 template 段都不设这个开关); 即使打开, `_RETRYABLE_FAIL_REASONS` 只有 `infrastructure` 与 `timeout`, 不含 `container_crash`, 且每个 dispatch 最多系统重试 1 次。
     - ⇒ 现行代码下, runner 放弃 → 一次 S_FAIL(container_crash), 不重派, 也就谈不上「反复」; 要让它重跑反而须 owner 手动介入。告警: `extension.py` / `transitions.py` 里 S_FAIL 转移没有通用的飞书告警钩子 (只有 S7 human_reject 一处, 另有 reconciler 对卡死行的 ops 告警), 其他模块本席未穷举。
   - 来源: 这句沿用了 `layer-boundary-contract.md` §S_FAIL handling 的「Acknowledge and let Layer 1 auto-retry (default)」—— 契约文档与代码不一致。本席 R5 观察第 1 条也把这句当成事实转述, 没有核代码, 在此更正。
   - 为什么是 major: 属门槛里的「事实不成立」; 它是写给 owner 的代价, 也是 T6 要写进跟进 issue 的「已知缺口」; owner 2026-09-15 给出的目标设计 (新失败类型「不自动重试」) 也建立在这个前提上。
   - 修法: Impact 与 D5.6 改为「按现行代码, 放弃后进 S_FAIL(container_crash), 不会自动重派 (扫描按 attempt=1 去重; failure_analysis 默认关闭, 且不重试 container_crash); 要重跑须 owner 手动介入」; 删「反复告警, 直到 owner 手动阻止该 issue 自动派发」; D5.6 已知缺口加一条「layer-boundary-contract §S_FAIL handling 写的默认自动重试与代码不一致」。硬前提本身不受影响, 理由换成「放弃即 S_FAIL, 须 owner 逐单处理」即可。

3. **§D5: 第 7 项漏删 (minor)**
   - v6 → v7 的 diff 里, 头部「四张」改「三张」, T6、SC-6、交付物、Impact 都去掉了 D5.7, 提交说明也写「OQ-9 与 D5.7 并入 D5.6」; 但 D5 列表第 7 项 (L106「开 `10CG/Aria` issue「编排器不消费 runner 结果枚举: 部分跳过的改动会按 SUCCESS 推进」」) 在 diff 里是上下文行, 原样保留。它的内容已写进 D5.6 的已知缺口 (「编排器目前不读 runner 的结果枚举 (`CLAUDE_NO_OP` 等)」)。
   - 后果: D5 正文要求开四张 issue, T6 / SC-6 / 交付物 / 头部都是三张; 照 D5 做就违背 R5 聚合里 owner 确认的「并入唯一一张跟进 issue」, 照 T6 做则 D5 有一项没有落点。字面「D5.7」「OQ-9」全文 0 处, 孤儿只剩这一行。
   - 修法: 删 L106。

## 观察 (不进收敛比较键, 不影响 vote)

1. **禁令「不提交任何改动」与 runner 代提交**: 三种模式都由脚本代 Claude 提交 —— `initial.sh` 第 10 步工作区不干净就 `git add -A` 后 commit, `changes.sh` / `redo.sh` 也是 `git add -A` 后提交。所以 L30「整单不提交必进 S_FAIL」只在工作区干净时成立 (三种模式都核了: initial `CLAUDE_NO_OP` → exit 1; changes / redo `no_changes` → exit 1; `_handle_s5_await` 非零 → S_FAIL)。Claude 做了一半才发现要改 description 时, 已做的改动会被脚本提交; initial 模式下 issue YAML 断言命中即 SUCCESS, 正是 D1 想避开的「部分跳过按 SUCCESS 推进」。建议 SOT 句写成「放弃整个任务: 还原已做的改动、不提交任何改动」, 或至少把这一点列进 D5.6 的已知缺口。当前无害, 见下一条。
2. **Impact「跟进 spec (D5.6) 落地之前, 自主 runner 不改任何 skill 的 description, 需要时整单放弃」在 `10CG/Aria#196` 修好前不成立**: aria-orchestrator 代码与 job 定义里 `unattended` 0 处; Aria `.aria/config.json` 的 `state_scanner.coordination` 只有 `enabled` 与 `mode` ⇒ Layer 2 读到 false, 禁令不触发。D1 已写明这个缺口, 实际起保护作用的是「硬前提」这条流程约束加 S7 签字; Impact 这句建议改成条件式。
3. **成本口径**: 三臂的约 15 美元与「并行约 11–20 分钟」在 Impact / OQ-3 / OQ-7 (B) 一致, 数字复算成立 (13 臂 run.log: fable 10m39s–17m39s, opus 15m18s–19m41s; 3 × 10m39s 约 32 分钟, 3 × 19m41s 约 59 分钟; 180 × 0.08 = 14.4 美元)。不一致的: OQ-5「约 15 美元与半小时」与并行 11–20、串行 32–59 都对不上; OQ-2 代价「两臂并行需两个临时根」与 OQ-8 备选代价「一次两臂重跑」仍按两臂写 (现为三臂、三个根、约 15 美元); Impact 标「来源 RESULT.md v6 §时长与成本」, 但该节只有两臂数字 (120 次 / 10 美元), 三臂数字是推导出来的。
4. **「577 次提交 / 6 次」**: 577 是 `git rev-list --count --all` (master 568, 其中合并 112)。复算 origin/master 的非合并提交, 改了已有 skill frontmatter description 的 7 次; 去掉 `ee35928b` (brainstorm 首次加 frontmatter, 改前没有 description) 为 6 次, 与文中一致, 约 1% 成立。建议注明分子分母的口径。
5. **RESULT v6 头部「环境故障只能靠参照臂识别」**: 与 v7 自己的第三作废条件 (stderr Warning, 实跑 E4 可达) 矛盾; 垫片按调用记录 `result` 帧是更直接的识别手段 (Findings 第 1 条修法 3)。
6. **L55「被评 description 退化 ⇒ 门先判 fail, 不会落到作废」** 单独读像「fail 优先于一切作废」; 与 L56 参照臂作废同时成立时, 要靠 L57「同批参照臂过门、而 …」才推得出作废优先。若采纳 Findings 第 1 条修法 1, 这句一并改。
7. **作废清单删掉了 v5 唯一可达的「run_eval 报错退出」**: 主进程崩溃、没有 json 时, 结果既不是 pass / fail, 也不在作废清单里。执行者不会把没输出当 fail, 风险低。
8. **D3 第 5 行机读实证 `v3-isolated-root-1worker-neutral-name/new.json`**: 对 v1.71.1 → v1.73.0 这次改动, 改动前的参照是 v3 的 `old.json`; v3 那轮还没有「参照臂」, 真正按参照臂跑的只有 v5 的 `new.json`。只影响证据标注, SC-2 只查存在性。
9. **SC-11 边角**: Python `re` 把汉字算作 `\w`, `\bD\d` / `\bT\d\b` / `\bSC-\d` 对紧贴汉字的编号不命中 (`re.findall(r'\bD\d', '见D2')` 为空, 带空格才命中); `OQ-\d` 不带 `\b`, 不受影响。当前待转录文本 0 命中。
10. **头部重核清单**「RESULT 再修订须同步重核本文 §Why 与 §D2 §D3」仍未含 §D6 / §Impact / T8 (三处都引 RESULT v6)。
11. **SC-1 / SC-12「含核心句的那一行」**: T2 若在 §场景 4b 开头复述核心句, SC-1 会因那一行缺「照跑场景 1」误红 (本席 R5 观察第 5 条 b 仍在)。

## 优点

- 三个作废条件都换成了可达信号; 参照臂对「环境从头就坏」这一大类有效 (v1 回放判对)。负控门槛的 Fisher 数字复算无误 (10 对 5 单侧 0.016, 10 对 6 为 0.043)。
- 收窄后自主模式只剩一句禁令; D1 旁注对 runner 退出码与 `_handle_s5_await` 的描述逐条对得上代码。
- SC-12 与改版 SC-9 都有真实区分力 (反事实实跑); SC-9 改按条款标题词定位的理由实测成立: 按单独的「fail」数, 同时含「不得 ship」的行是 2 行 (作废条款含 `Warning: query failed`)。
- 转录纪律 SC-11 与 T0 对齐, 全部待转录文本 0 命中; RESULT 引用全部同步到 v6。

## Verdict

**PASS_WITH_WARNINGS** —— critical 0 / major 2 / minor 1 (Findings); 观察 11 条不计入。

- **Phase 1 (规范合规): PASS**
  - `check_bare_issue_refs.py` 对 proposal 与 RESULT 各跑一次: 「裸 issue 引用: 0」, rc 0 / rc 0。
  - 禁用字形 (U+2460–24FF / U+2776–2793 / U+3251–325F / U+32B1–32BF / 希腊与科普特 U+0370–03FF / 希腊扩展 U+1F00–1FFF): proposal 0、RESULT 0; NUL 0 / 0。
  - 本 Spec 的 rule6_note: `n/a` / `no` / `n/a` / `n/a` / `n/a`, 都在 §D4 值域内; `description_changed: no`, 不触发合规条款; aria gitlink 未动 (`1cb3872`), 「本 Spec 自身不触发 Rule #6」成立。
  - D1 三条旧句: CLAUDE.md / SOT / 手册 (去外层反引号) 各恰 1 次 (python 计数与 `/usr/bin/grep -cF` 一致)。核心句在三条新句里各 1 次、逐字相同, 三个现状文件里各 0; 三条新句都含「照跑场景 1」与「另须跑场景 4b」; SC-5 正则 0。
  - 范围: `3b2215e..c3a5903` 只动 proposal 与 R5 聚合报告; CLAUDE.md、SOT、手册、套件都未动; 无范围外变更。头部 Status 与 R5 聚合末尾的裁定一致。
- **Phase 2 (质量)**: 2 条 major (D2 判定逻辑; Impact / D5.6 事实断言), 1 条 minor (D5 第 7 项漏删)。

## Vote

**REVISE** —— major 没有清零。三处都只改文字、不需要新的实跑: D2 负控作废去掉「门通过」前提, 并补按调用识别故障 (或 fail 时原样重跑一次) 与 stderr 入产物; Impact 与 D5.6 按代码改写重试行为; 删 D5 第 7 项。

## 映射表

### D → T → SC (v7)

| D (子项) | T | SC | 备注 |
|---|---|---|---|
| D1 三处新句 (核心句 + 照跑场景 1 + 另须跑场景 4b) | T1 | SC-1, SC-5 | 核心句三处逐字一致 |
| D1 SOT §2 自主禁令 + CLAUDE.md 指向句 | T1 | SC-12 | 反事实 4 种全红 |
| D1 手册 三条 → 四条 | T1 | SC-7 | |
| D1 SOT §3 边界注 | T1 | SC-10 后半 | |
| D1 旧句删除 (CLAUDE.md / SOT) | T1 | 无 | 手册一处由 SC-7「边界三条」= 0 兜住 (沿用 R5) |
| D2 参数 / 20 条 | T2 | SC-10 前半 | 按行判 |
| D2 负控门槛 / 连续 2 轮 / 两条后果 / 参照臂 | T2 | SC-9 | 删任一后果行即红 (实跑) |
| D2 作废三情形的判定逻辑 | T2 | 无 | Findings 第 1 条 |
| D2 不设比较判据 | T2 | SC-5 | |
| D2 套件文件 + version.yaml | T4 | SC-4 | OQ-3 未裁分支一致 |
| D2 手册固定测试集表加 trigger 行 | T2 | 无 | 沿用 R5 |
| D3 六行前置表 | T2 | SC-2 | 机读实证路径全部存在, 第 4 行为唯一 [配置推导] 行 |
| D4 §4.1 五字段 / 值域 / 两套编号 | T3 | SC-3 | |
| D4 合规条款 | T3 | 无 | 沿用 R5 观察 |
| D5.1 拆 4a / 4b | T2 | SC-8 | |
| D5.2 / D5.3 / D5.6 三张 issue | T6 | SC-6 | |
| **D5 第 7 项** | 无 | 无 | **孤儿**, Findings 第 3 条 |
| D5.4 上游反馈 | T6 | SC-6 | |
| D5.5 分工留言 | T7 | SC-6 | |
| D6 §6 第三条 + 计数语 | T5 | SC-7 前半, SC-12 第三项 | 「只在 Claude 模型上实测过」= 1 |
| SOT 文件头 Version | T5 | SC-7 中段 | |
| 转录纪律 | T0 | SC-11 | |
| 合并 / 双推 / 逐 remote `ls-remote` | T7 | 无 | 流程任务, 与 CLAUDE.md 多远程两条约束一致 |
| `10CG/Aria#211` 回帖 | T8 | 无 | 流程任务 |

孤儿检查: SC-1 到 SC-12 都挂得到 D; T0–T8 都挂得到 D 或流程; D 侧孤儿只有 D5 第 7 项。被删的 OQ-9: proposal 与 RESULT 中字面 0 处; 字面「D5.7」0 处。

### 三臂成本在各处的写法

| 位置 | 调用次数 | 时长 | 金额 | 结论 |
|---|---|---|---|---|
| Impact (L125) | 约 180 次 | 并行约 11–20 / 串行约 32–59 分钟 | 约 15 美元 | 复算成立; 标注的来源节只有两臂数字 |
| OQ-3 (L160) | 未写 | 并行约 11–20 分钟 | 约 15 美元 | 一致 |
| OQ-5 (L162) | 未写 | 「半小时」 | 约 15 美元 | 时长与 Impact 对不上 |
| OQ-7 (B) (L164) | 未写 | 并行约 11–20 分钟 | 约 15 美元 | 一致 |
| OQ-8 备选 (L165) | 「一次两臂重跑」 | 未写 | 未写 | 仍按两臂 |
| OQ-2 代价 (L159) | 「两臂并行需两个临时根」 | 不适用 | 不适用 | 仍按两臂 |

### OQ 推荐项与自身代价

| OQ | 推荐 | 推荐项自身的代价 | 结论 |
|---|---|---|---|
| OQ-1 | 0.5 | 放过「2/3 才触发」的 description | 有 |
| OQ-2 | 单 worker + 独立根 | 临时根与手册步骤 | 有 (「两臂 / 两个根」过时, 观察第 3 条) |
| OQ-3 | 先审 | 改 query 须重跑三臂, 并行约 11–20 分钟 / 约 15 美元 | 有; 另写了未裁时的默认 |
| OQ-4 | 无推荐, 两选项各写代价 | 不适用 | 原文无推荐, 未自造默认 |
| OQ-5 | 地板守卫 | 多一条义务, 只挡两类破坏 | 有, 备选代价也写了 |
| OQ-6 | 暂不放宽 | 每次 description 改动多跑一次场景 1 | 有 |
| OQ-7 | (A) | 每个 skill 首次改 description 须等 owner 审约 15 分钟, 不在线即阻塞 | 有 |
| OQ-8 | 判据不改 | 套件没覆盖到的扩张判不出 | 有; 备选代价「两臂」过时 |

### v6 / v7 新增的全称句与事实断言

| 句子 (位置) | 依据 | 结论 |
|---|---|---|
| 「只有结果为 SUCCESS 时以 0 退出」(L30) | `initial.sh` 第 591–595 行 | 成立 |
| 「`_handle_s5_await` 只看退出码、非零即进 S_FAIL」(L30) | `_handle_s5_await` terminated 分支 | 成立 (另有心跳超时进 S_FAIL(timeout)、lost 进 S_FAIL(dispatch_lost), 同为 S_FAIL) |
| 「整单不提交必进 S_FAIL」(L30) | 三种模式的无改动出口都以 1 退出 | 工作区干净时成立; runner 会代提交遗留改动 (观察第 1 条) |
| 「`runs` 恒为 3」(L51) | 每个 future 恰 append 一次; 套件 20 条无重复 | 成立 (E1–E4 runs 全为 3) |
| 「环境故障在输出 json 里与「真没触发」无法区分」(L51) | json 只有 `trigger_rate` / `triggers` / `runs` / `pass` | 成立 (E1–E3 与真没触发同形) |
| 「必须有它 (参照臂)」(L51) | 同上 | 「需要额外信号」成立; 参照臂只覆盖一部分故障 (Findings 第 1 条) |
| 「门通过时被评 description 必为 10/10」(L54) | 门的定义 | 成立 |
| 「编排器目前不读 runner 的结果枚举」(L105) | layer1 非测试代码 `CLAUDE_NO_OP` 0 处 | 成立 |
| 「放弃后 … 默认自动重试」(L105) / 「默认自动重试、反复告警, 直到 owner 手动阻止」(L126) | 契约文档 | **不成立** (Findings 第 2 条) |
| 「runner 镜像没有场景 4b 依赖的 skill-creator」(L105) | runner 镜像目录 / nomad / deploy 中 0 处 | 成立 |
| 「577 次提交里 6 次, 约 1%」(L126) | 复算 | 口径可复现 (观察第 4 条) |
| 「跟进 spec 落地之前, 自主 runner 不改任何 skill 的 description」(L126) | 以禁令生效为前提 | `10CG/Aria#196` 修好前禁令不触发 (观察第 2 条) |

## 实跑记录

1. `python3 aria/skills/state-scanner/scripts/check_bare_issue_refs.py <proposal>` → 「裸 issue 引用: 0」, rc 0; 对 RESULT.md → 同样, rc 0。
2. 禁用字形 + NUL (python 逐字符扫, 区间见 Verdict): proposal 0 / 0, RESULT 0 / 0。
3. D1 表 (python 从 proposal 取三行三列): 旧句在 CLAUDE.md / SOT / 手册的 python 计数 1 / 1 / 1, `/usr/bin/grep -cF` 1 / 1 / 1; 新句核心句各 1, 现状文件核心句各 0; 三条新句都含「照跑场景 1」「另须跑场景 4b」; SC-5 正则 0 / 0 / 0。
4. SC-11 (五个正则) 对 CLAUDE.md 新句、SOT 新句、手册新句、§3 边界注、§4.1 转录段、§6 第三条、D2 正文、D3 正文: 全部 0。CJK 边界探针: `re.findall(r'\bD\d', '见D2')` = `[]`, 对 `'见 D2'` = `['D2']`。
5. SC-9 (取 D2 正文当手册 §场景 4b): 原样 (「fail 的后果」+「不得 ship」行数, 「作废」+「不得 ship」行数) = (1, 1); 删后果行 (0, 1); 删作废行 (1, 0); 单独「fail」+「不得 ship」= 2 行。「≤ 5/10」1、「连续 2 轮」1、「参照臂」4。SC-10: 含「参数钉死」的行 1 行, 四参数与「20 条」齐。SC-12 反事实: 原样绿; 删自主条款 / 改「跳过这一部分」/ 删 CLAUDE.md 指向句 / 删「写明 …」四种全红。SC-2: 前置表 1–6 行机读实证路径全部存在, 第 4 行为唯一 [配置推导] 行。
6. 基线各臂 (python 读 json): v1 四臂门全 FAIL; v2 old / poscontrol 门 PASS, new 门 FAIL (「phase d.2 该做的事 …」0/3), negctrl should 命中 9/10; v3 new / old / poscontrol PASS, negctrl 3/10; v4 overbroad FAIL (should-not 7/10), realroot PASS; v5 new / mildcreep PASS, negctrl 0/10; 全部 runs = 3。按 v7 规则回放 (参照 = 改动前): v1 作废、v2 fail、v3 pass、v5 pass。run.log 单臂时长: v2 11m26s–17m39s, v3 10m39s–12m03s, v4 13m38s–13m54s, v5 15m18s–19m41s。
7. 假 `claude` 实跑 (scratchpad `r6/fakeexp/`: 一个 python 写的假 `claude` 按环境变量决定触发 / 不触发 / 按调用序号报错, 放在 PATH 最前; 用插件缓存里原样的 `run_eval.py`, 设 `PYTHONDONTWRITEBYTECODE=1`; 不调用任何 API):
   - 单元 (2 条 query, 3 runs): E0 正控 → should 3/3、should-not 0/3, Warning 0 (假 claude 能被判触发, 装置可用); E1 API 报错结果帧 → should 0/3 判 fail、should-not 0/3 判 pass, rc 0, Warning 0; E2 非零退出 → 同 E1, Warning 0; E3 超时 (假 claude 睡 4 秒、`--timeout 2`) → 同 E1, Warning 0; E4 PATH 里没有 claude → 同 E1, Warning 6 行。
   - 场景 (真实 20 条套件, 前 10 条 should-trigger, 3 runs, 单 worker, 每臂独立根): S0 过宽被评无故障 → 参照 PASS / 被评 FAIL (should-not 10/10) / 负控 0 → fail; S1 只有被评臂从第 30 次调用起报错 → 被评 PASS → pass; S2 三臂同时从第 30 次起报错 → pass; S3 只有被评臂第 6–8 次调用报错 (被评 description 正确) → 被评 9/10 FAIL、参照 PASS → fail; S4 三臂同时第 12–20 次报错 → 参照 7/10 FAIL → 作废。所有臂 rc 0, 除 E4 外 Warning 0。
8. `run_eval.py` (缓存 `bb335391eb83`): 第 88 行 `stderr=subprocess.DEVNULL`; 第 101 行超时循环; 第 170–171 行遇 `result` 帧返回 `triggered`; 第 178 行 `return triggered`; 第 222–225 行异常 → Warning + `append(False)`; 第 240 行 `"runs": len(triggers)`。
9. aria-orchestrator `237045a` (= 主仓 gitlink): `docker/aria-runner/modes/initial.sh` 第 362–376 行 NO_OP 判定 (工作区干净且无新提交), 第 416–418 行工作区不干净即 `git add -A` 后 commit, 第 524–534 行 SUCCESS 五条件, 第 591–595 行 SUCCESS → 0、其他 → 1; `changes.sh` / `redo.sh` 在 `git add -A` 后无 diff 即 `fail_with no_changes` (exit 1); `extension.py` `_handle_s5_await` (第 2467 行起) terminated 且 exit_code 非 0 → `S_FAIL` + `CONTAINER_CRASH`; `_phase1_scan_and_seed` 对已有 attempt=1 行的 issue 跳过; `reconciler.py` Decision.RETRY 只针对卡住的 S5_AWAIT 行, failure_analysis 扫描在 DI 为 None (默认) 时整段跳过, `_RETRYABLE_FAIL_REASONS` = {infrastructure, timeout}, `_RETRY_COUNT_MAX` = 1; `reconcile_runner.py` 未设 `ARIA_FAILURE_ANALYSIS_ENABLED` 即返回 None; `deploy/aria-layer1-reconcile.nomad.hcl` 的 env 块与 template 段都不设该开关 (template 只注入凭据类键); 部署手册 (`docs/handoff/2026-05-15-m5-deploy-playbook.md` 等) 的 job env 写 `"0"`, 标注 owner 选择。layer1 非测试代码里 `CLAUDE_NO_OP` 0 处; `extension.py` / `transitions.py` 里 S_FAIL 转移没有通用飞书告警钩子 (只有 S7 human_reject 一处)。
10. `unattended`: aria-orchestrator 代码与 job 定义 0 处 (只有一份法律备忘文档出现该词); Aria `.aria/config.json` 的 `state_scanner.coordination` 只有 `enabled` / `mode` (另有 `_comment`), 无 `unattended`; `10CG/Aria#196` open, 标题与 D1 描述一致。skill-creator 在 runner 镜像目录 / nomad / deploy 中 0 处。
11. aria 子模块 (`1cb3872`) 提交计数: `rev-list --count --all` 577, `HEAD` / `master` / `origin/master` 568 (非合并 456)。origin/master 非合并提交中改了已有 `skills/*/SKILL.md` frontmatter description 的 7 次: `2b67ac64` (openspec-archive, 即 v1.73.0 那次)、`557b9535` (24 个 skill)、`55d2e84a`、`641e1649`、`7801bd42`、`ee35928b` (brainstorm 改前无 frontmatter)、`f8713f14`; 另有 2 次合并提交 (对第一父) 同样命中。
12. `git diff 3b2215e..c3a5903 -- proposal.md`: D5 第 7 项是上下文行 (未删); 头部、T6、SC-6、交付物、Impact 中的「D5.7」均已删; 「OQ-9」整段删除。v7 提交说明: 「OQ-9 与 D5.7 并入 D5.6」。
13. 环境: 主机 dev-claude2, git 身份 simonfishgit; 工作区除原有两个 triage 文件与一份别席 R6 报告 (未打开) 外无变动。
