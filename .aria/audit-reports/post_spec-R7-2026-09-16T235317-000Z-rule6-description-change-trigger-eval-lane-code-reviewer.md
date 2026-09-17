---
checkpoint: post_spec
mode: convergence
rounds: 7
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS
timestamp: 2026-09-17T00:13:09.418Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [code-reviewer]
---

# post_spec R7 — code-reviewer 席 (Phase 1 规范合规 + Phase 2 质量)

被审对象: proposal v8 @ 主仓 `15ab323`; 新证据 = 基线目录 RESULT.md v7 的「v6: 逐调用健康检查」一节与 `v6-per-call-health-opus5/` (v6a / v6b 两批)。只审不改: 唯一写入是本报告; 自己重跑的故障矩阵、反事实、边界探针都在 session scratchpad (`r7-code-reviewer/`), 仓库文件未动 (`git status --porcelain` 空)。独立性: 同目录未见本 spec 的别席 R7 报告; 列出的 R7 文件属其他 spec, 未打开。

代码核对面: skill-creator 插件缓存 `bb335391eb83` 的 `scripts/run_eval.py`; aria-orchestrator `237045a` (= 主仓 gitlink); aria 子模块 `1cb3872`。下文数字都来自实跑, 命令与输出见「实跑记录」。

## R6 对账

范围: 本席 R6 报告 Findings 的 3 条 (major 2 / minor 1)。

| 序号 | R6 条目 | v8 落点 | 状态 | 核对依据 |
|---|---|---|---|---|
| 1 | [major] testing §D2: 作废三情形可达, 但参照臂只接得住同时落在其 should-trigger 段的故障 | 参照臂整条删除 (全文「参照臂」0 处), 换成「逐调用健康检查」(L51) + 作废三情形改写 (L55) + fail 判据改写 (L56) | **closed** | 自己重跑故障矩阵 24 用例全符合、rc 0; 自己做反事实 (删报错结果帧判定) 得 5 例不符、rc 1, 与 SC-13 写的 5 个用例名逐一相同; R6 四个假 claude 场景在 v8 下全部翻成作废 (下表); 逐行对 `run_eval.py` 核判定事件集与触发次数区间, 完备且偏保守 (下文) |
| 2 | [major] documentation §Impact+§D5.6: 「默认自动重试、反复告警」与代码不符 | Impact (L125) 改「进 S_FAIL, 失败类型 `container_crash`, 这是终态 —— 不自动重试, 默认也不告警 … 停在那里无人察觉」; D5.6 已知缺口 (1) 同向改写, 另加缺口 (8) 指出契约文档与代码不一致 | **closed** | 新增的三个子断言逐条核代码全部成立: `fail_detail` 实串 = `S5_AWAIT: alloc terminated with exit_code=… alloc_id=… (container_crash)` (确只有退出码与 alloc id); 失败分析的 `NOT EXISTS` 反连接注释原文「zero re-fires after the first analysis lands」⇒「至多一张通知卡」成立; `_RETRYABLE_FAIL_REASONS` 仍为 {infrastructure, timeout}、`_RETRY_COUNT_MAX` = 1 |
| 3 | [minor] documentation §D5: 第 7 项漏删 | D5 现恰 6 条 | **closed** | 正则数 D5 顶层条目 = 6; 「参照臂」「D5.7」「OQ-9」(作为被删项) 的残留均已清零; T6 / SC-6 / 交付物 / 头部的「三张」与 D5 一致 |

合计: closed 3 / partially 0 / open 0。

### major 1 的独立复核 (任务第 1 项)

**自己重跑故障矩阵** (`python3 fault_matrix.py --out <scratchpad>/fm`, 不调用 API): 24 用例、与预期不符 0、退出码 0, 逐行结论与归档的 `fault-matrix/matrix-summary.json` 完全一致。**自己做 SC-13 的反事实** (临时副本里删掉 `classify_calls.py` 的 `if errored: reasons.append("result 帧报错")` 两行) → 与预期不符 5、退出码 1, 不符的正是 `F1_result_error` / `S1_overbroad_fault_in_shouldnot_half` / `S2_correct_fault_on_one_should_query` / `S8_two_run_fault_should` / `S10_negctrl_two_run_fault_x6` —— SC-13 写的反事实属实。

**判定事件的定义对 `run_eval.py` 的提前返回点**: `run_single_query` 的返回点共 6 处, 逐个对上 `classify_calls.py` 的 `decisive` 集合 (tool_use 开始 / `message_stop` / 含 tool_use 的 assistant 消息 / 结果帧):

| `run_eval.py` 返回点 | 触发的事件 | classify 记为 | 结论 |
|---|---|---|---|
| 第 141 行 (tool_use 名不是 Skill/Read → False) | `content_block_start` + tool_use | `tool_use_start` | 覆盖 |
| 第 148 / 152 行 (input_json 命中 / `content_block_stop`、`message_stop` 且 pending) | 必先有 tool_use 的 `content_block_start` | `tool_use_start` | 覆盖 (`content_block_stop` 未单列, 但它只在 pending 时返回, 而 pending 只能由 tool_use 开始置位 ⇒ 不漏) |
| 第 154 行 (`message_stop` 无 pending → False) | `message_stop` | `message_stop` | 覆盖 |
| 第 168 行 (assistant 消息里第一个 tool_use) | assistant | `assistant_tool_use` | 覆盖 |
| 第 171 行 (结果帧) | result | `result` | 覆盖 |
| 第 178 行 (while 超时退出) | 无 | 无判定事件 / 耗时达阈值 | 由「耗时 ≥ 超时阈值 - 1 秒」与「无判定事件」接住 (F5 / F6 实测) |

**「输出流里出现过 tool_use 才可能被记成触发」**: 成立, 且是严格必要条件。`triggered` 只在第 165 / 167 行赋 True, 两处都紧跟同一 for 迭代内的第 168 行 `return triggered` ⇒ 第 171 行与第 178 行的 `return triggered` 恒为 False; 其余两处返回 True 都要求 `accumulated_json` 命中, 而 `accumulated_json` 只在 pending_tool_name 置位后累积。所以没出现过 tool_use 的调用, run_eval 只可能记成未触发。

**触发次数区间 `[triggers - 可能被记成触发的不健康数, triggers + 不健康数]`**: 与 run_eval 的记录方式一致。`lo = trig - u_maybe` 对应「本来记成触发、真实是没触发」; `hi = trig + u_false + u_maybe` 对应「本来记成未触发、真实是触发」, 上下界都按 `[0, runs]` 截断。一处**偏保守**: 名字不在 (Skill, Read) 的 tool_use, run_eval 必记 False, 而 classify 仍把它算进 `u_maybe` ⇒ 区间偏宽 ⇒ 结论更容易落到 void。void 与 fail 同为「不得 ship」, 方向安全。另可证 `lo ≤ trig ≤ hi` ⇒ `pass ⇒ 门通过`、`fail ⇒ 门判 fail`, 与 D2 正文「门判 fail, 且不健康的调用改变不了这一点」逐字相符。

**R6 的 S1 / S2 / S3 / S4 与 v2 回放在 v8 规则下的判定**:

| R6 场景 | v7 判定 | v8 判定 | 依据 |
|---|---|---|---|
| S1 过宽被评臂只在后半程 (should-not) 故障 | **pass (假绿)** | **作废** | 矩阵 `S1_overbroad_fault_in_shouldnot_half`: 门 True、Warning 0、检查 void (30 次报错结果帧) |
| S2 三臂同时从后半程故障 | **pass (假绿)** | **作废** | 每臂各自判, 被评臂形态同 S1 ⇒ void; 负控臂另由 `--role negctrl` 的命中上界判 |
| S3 正确 description, 只有被评臂在一条 should-trigger 的三次 run 故障 | **fail (假红)** | **作废** | 矩阵 `S2_correct_fault_on_one_should_query`: 门 False、检查 void |
| S4 三臂同时在前半程故障 | 作废 (参照臂 FAIL) | **作废** | 被评臂形态同上 ⇒ void; 不再依赖参照臂 |
| 基线 v2 回放 (负控 9/10, 被评门 FAIL) | **fail** | **作废** | v8 作废条件写「负控 ≥ 6/10, **不论被评 description 过没过门**」; 另 `--role negctrl` 在命中上界 > 5 时直接 void |

⇒ R6 这条 major 指出的两条伤害路径 (只落一臂 ⇒ 正确 description 判 fail; 落 should-not 半程 ⇒ 过宽改动判 pass) 与「负控信号在 fail 分支被丢掉」都已关闭, 且不是靠收窄文字, 是靠一个可重跑、有反事实的机制。

## Findings

- [minor] implementation/proposal.md §Key Deliverables (tools/trigger-eval 四文件) (risk): `fault_matrix.py` 第 110–111 行对 `--out` 指向的已有目录无条件 `shutil.rmtree`, 无确认、无空目录检查; `--out .` 会删空当前目录。SC-13 把四文件冻成逐字节相同, 进 Phase B 后再改要动已锁定的实验产物或改 SC-13。

计数: critical 0 / major 0 / minor 1。这条列进 Findings 而不是观察的理由只有一个: 它是**单向门**。T2b 一旦把四个文件原样搬进 `aria-plugin-benchmarks/tools/trigger-eval/`, SC-13 的 `cmp` 就把它们钉死在基线目录那份上, 而基线目录那份是 prereg 锁定的实验产物, 事后改它会破坏溯源。所以要么现在改 (同步改基线副本并在 RESULT 记一笔), 要么现在就在手册 §场景 4b 的用法行里写明「`--out` 会先删除该目录, 只传新路径」。两条路都是一行的事, 不需要重跑任何实验。

## 观察 (不进收敛比较键, 不影响 vote)

1. **`classify_calls.py` 在空结果集上真空成立**: 对 `{"results": []}` + 空日志目录, `all([])` 为真 ⇒ 结论 `pass`、退出码 0 (已实跑)。按 D2 的参数钉死 (套件 20 条) 与 run_eval 的行为 (每条 query 必产一行结果, 崩溃则没有 json ⇒ 检查脚本返回 2), 这条路在规定流程里够不着; 但作为要 ship 的工具, 加一句「results 为空 ⇒ 无法判定」更稳。
2. **垫片的可执行位不在 SC-13 的判据里**: `cmp` 只比字节不比 mode。`fake-claude` 掉了 +x 会让矩阵大面积不符 (SC-13 转红, 接得住); `claude-shim.sh` 掉了 +x 矩阵却发现不了 (`fault_matrix.py` 自己 `chmod 755` 了副本), 只在真实跑臂时表现为整轮 void。T2b 用 `cp -p` 或在 SC-13 加一句 mode 断言即可。
3. **垫片里的真 claude 默认路径写死为 `/home/dev/.local/bin/claude`**: 换机器就得设 `TRIGGER_EVAL_REAL_CLAUDE`, 否则 `exec` 失败 ⇒ 每次调用都不健康 ⇒ 整轮作废 (F7 已覆盖这一形态, 方向安全, 但报错信息只落在 `.err` 里)。垫片本身不能从 PATH 找 `claude` (它自己就是 PATH 上的 `claude`), 所以写死是有理由的; 建议手册的前置里点名这个环境变量。
4. **日志目录的环境变量名没进规范文字**: D2 / D3 只说「每臂一个新建的空日志目录」, 没写 `TRIGGER_EVAL_CALL_LOG_DIR`。不设它垫片直接报错退出 ⇒ 检查脚本读不到目录 ⇒ 返回 2 ⇒ 作废 (fail-closed), 但执行者得去读脚本才知道要设什么。
5. **Claude Code 版本已经漂了**: RESULT 记的是 2.1.269, 本机现在是 2.1.273。RESULT 的已知局限已写明「升级后先重跑 `fault_matrix.py`, 再实跑一臂确认零误报」—— 注意我这次重跑矩阵用的是假 claude, **不验证真实帧名**, 所以「先重跑矩阵」只覆盖逻辑不覆盖帧名, 那句局限里的第二半 (实跑一臂) 才是帧名的证据面。
6. **`may_be_recorded_true` 对非 Skill/Read 工具偏保守** (见上文 major 1 复核): 不是缺陷, 方向安全; 若将来想收紧误报, 可按工具名区分。
7. **D5.6 缺口 (3) 里的「不要带着半成品提交」是意译**: runner 提示词 (`docker/aria-runner/prompts/issue-dispatch.md` 第 29 行) 的原文是 `do NOT make a commit with partial work`。含义一致, 但用引号括起来容易被读成逐字引用。
8. **SC-9 依赖 `**作废**` 的粗体字面**: 断言的是「含『**作废**在以下任一情形发生』的那一行」, 转录时若丢了粗体星号会误红 (fail-closed, 方向安全, 但会浪费一次返工)。同类问题在 SC-1「含核心句的那一行」上仍在 (本席 R5 观察第 5 条)。
9. **「15 个提交新增 skill (不含首版)」口径可复现**: `origin/master` 456 个非合并提交里, 新增过 `skills/*/SKILL.md` 的提交 16 个; 最早一笔 `6862a2a8` (2026-01-23 initial release) 一次加 24 份 = 首版, 去掉后恰 15。建议在文中补一句分母口径, 与「7 个」那句同处理。
10. **D4 的合规条款仍无 SC**: SC-3 只查五个字段名、值域含 `void` / `n/a` 与「两套编号」一句; 「套件未经审阅 ⇒ 不合规」「`description_changed: yes` 而 scenario 为空 ⇒ 不合规」两条转录后没有机械断言 (沿用 R5 / R6 观察)。
11. **头部重核清单已修好**: 改成「以 `grep -n RESULT` 逐处列出, 不只看某几节」; 实测 proposal 里 12 处 RESULT 引用全部为 v7, 「RESULT.md v6 / RESULT v6」0 处。D6 里那句给执行者的指令 (写入时附版本号与 SHA) 已从待转录文本移进 T5, R6 聚合第 6 条的两半都闭合。
12. **成本口径已统一**: 「约 120 次 / 约 10 美元 / 并行约 11–23 分钟 / 串行约 21–46 分钟」在 Impact / OQ-3 / OQ-5 / OQ-7(B) 四处一致 (R6 本席观察第 3 条的三处不一致全部消失); 复算成立: 17 臂 run.log 的单臂区间 10m39s–23m05s, 两臂串行 21–46、并行取上沿 23。OQ-2「两臂并行需两个临时根」与 OQ-8「一次两臂重跑」现在也对得上臂数。

## 优点

- **实验设计本身是这轮最大的增量**: 预登记先锁 (`prereg.lock` sha1 + 时间戳, 声明「任何实验运行之前」), 真实数据打脸后不是偷偷改判据, 而是另写修订预登记、再锁一次、把 A / B / C 三组**全部重跑**, 并在 proposal 的 rule6_note 段把「看到数据之后修订规则」当作待 owner 复议的流程判断写出来。这是本仓少见的、对「事后改判据」这一类假绿的正面处理。
- 故障矩阵有真实区分力: 我删掉一个判定条件就有 5 个用例转红, 不是恒绿套件; 24 个用例覆盖了正常四类、故障七类、垫片缺位、超时余量边缘、单 run / 双 run 故障、负控角色与 query 对不上六种形态。
- 新机制把 R6 的 major 从「文字收窄」升级成「可证伪的机制」: 参照臂那三种正当情形下的必然作废 (tech-lead 席 R6 第 2 条 (2)) 也随参照臂一起消失, 一个改动同时关掉两条。
- 真实两臂 120 次调用零不健康、零 Warning, 且 v6a 里那 2 次不健康经逐条核对是真故障 (rate_limit_event + 5 次 api_retry + 耗满 120 秒), 不是误报 —— 误报率这一面有实测支撑。

## Verdict

**PASS** —— critical 0 / major 0 / minor 1 (Findings); 观察 12 条不计入。

- **Phase 1 (规范合规): PASS**
  - `check_bare_issue_refs.py` 对 proposal / RESULT.md / 两份预登记各跑一次: 均「裸 issue 引用: 0」, rc 0 / 0 / 0 / 0。
  - 禁用字形 (U+2460–24FF / U+2776–2793 / U+3251–325F / U+32B1–32BF / 希腊与科普特 U+0370–03FF / 希腊扩展 U+1F00–1FFF) 与 NUL: proposal、RESULT、两份预登记、四个工具文件共 8 个文件全部 0 / 0。
  - 本 Spec 自己的 rule6_note: `n/a` / `no` / `n/a` / `n/a` / `n/a`, 逐项在 §D4 值域内; `description_changed: no` 不触发合规条款; aria 子模块 gitlink 未动 (`1cb3872`) ⇒ 「aria-plugin 零改动, 本 Spec 自身不触发 Rule #6」成立 (新增的四个工具文件落在主仓 `aria-plugin-benchmarks/`, 不是 SKILL.md)。
  - D1 三条旧句: CLAUDE.md / SOT / 手册 (去外层反引号) 各恰 1 次; 核心句在三条新句里各 1 次且逐字相同, 在三个现状文件里各 0 次; 三条新句都含「照跑场景 1」与「另须跑场景 4b」; SC-5 正则在三条新句与 D2 正文 (去掉「不设比较判据」行) 上均为 0。
  - 转录纪律 (SC-11) 对**真正待转录**的六块文字 (CLAUDE 新句 / SOT 新句 / 手册新句 / §3 边界注引号内 / §4.1 的 YAML 与三条转录条款 / §6 第三条引号内) 全部 0 命中。
  - 范围: `c3a5903..15ab323` 只动 proposal、RESULT.md、v6 实验产物、R6 审计报告与 triage 文件; CLAUDE.md / SOT / 手册 / `ab-suite/` 都未动; 子模块 gitlink 未动; 无范围外变更。
- **Phase 2 (质量): PASS** —— 四个工具文件的缺陷只剩一条 minor (见 Findings), 其余为观察级。

## Vote

**PASS** —— critical 与 major 均为 0。唯一的 minor 是一行代码或一行手册文字的事, 不需要新的实跑, 也不构成进 Phase B 的阻塞; 但因为 SC-13 会把这四个文件冻成字节级不可改, 建议在 T2b 落地之前一并处理。

## 映射表

### D → T → SC (v8)

| D (子项) | T | SC | 备注 |
|---|---|---|---|
| D1 三处新句 (核心句 + 照跑场景 1 + 另须跑场景 4b) | T1 | SC-1, SC-5 | 三处核心句逐字一致 (实测) |
| D1 SOT §2 自主禁令 (含「撤销本任务已做的全部改动」) + CLAUDE.md 指向句 | T1 | SC-12 | v8 新加的撤销子句已进 SC-12 |
| D1 手册 三条 → 四条 | T1 | SC-7 | 手册现状「边界三条」1、「边界四条」0 |
| D1 SOT §3 边界注 | T1 | SC-10 后半 | |
| D1 旧句删除 | T1 | 无 | 手册一处由 SC-7「边界三条」= 0 兜住 (沿用 R5) |
| D2 参数 / 20 条 | T2 | SC-10 前半 | 按行判 |
| D2 负控门槛 / 连续 2 轮 / 两条后果 / 逐调用健康检查 | T2 | SC-9 | v8 新增两项断言 (`classify_calls.py` 行、作废行三串), 实测都能命中且可证伪 |
| D2 逐调用健康检查的工具与故障矩阵 | **T2b** | **SC-13** | v8 新增; 本席独立重跑与反事实都复现 |
| D2 不设比较判据 | T2 | SC-5 | |
| D2 套件文件 + version.yaml | T4 | SC-4 | OQ-3 未裁时 T4 deferred, SC-4 有改判分支; `ab-suite/trigger/` 现不存在, version 1.5.0 |
| D2 手册固定测试集表加 trigger 行 | T2 | 无 | 沿用 R5 |
| D3 六行前置表 | T2 | SC-2 | 14 条机读实证路径全部 `test -e` 为真 (含 v8 新加的 4 条) |
| D4 §4.1 五字段 / 值域 / 两套编号 | T3 | SC-3 | 现行 SOT 五字段全 0, 反事实成立 |
| D4 合规条款 | T3 | 无 | 观察第 10 条 |
| D5.1 拆 4a / 4b | T2 | SC-8 | 手册现只有 1 个 `### 场景 4` 标题 |
| D5.2 / D5.3 / D5.6 三张 issue | T6 | SC-6 | D5 现恰 6 条, 无孤儿 |
| D5.4 上游反馈 (三条修复方向) | T6 | SC-6 | 第 (iii) 条的证据指向 `fault-matrix/matrix-summary.json`, 存在 |
| D5.5 分工留言 | T7 | SC-6 | |
| D6 §6 第三条 + 计数语 | T5 | SC-7 前半, SC-12 第三项 | 「只在 Claude 模型上实测过」= 1 |
| SOT 文件头 Version | T5 | SC-7 中段 | |
| 转录纪律 | T0 | SC-11 | |
| 合并 / 双推 / 逐 remote `ls-remote` | T7 | 无 | 流程任务 |
| `10CG/Aria#211` 回帖 | T8 | 无 | 流程任务; `10CG/Aria#211` open, `10CG/Aria#196` open (实查) |

孤儿检查: SC-1 到 SC-13 (文件里顺序为 1–9、11、12、10、13) 各挂得到 D; T0–T8 (含 T2b) 各挂得到 D 或流程; **D 侧无孤儿** (R6 的 D5 第 7 项已删)。

### 两臂成本在各处的写法

| 位置 | 调用次数 | 时长 | 金额 | 结论 |
|---|---|---|---|---|
| Impact (L124) | 约 120 次 | 并行约 11–23 / 串行约 21–46 分钟 | 约 10 美元 | 复算成立 (17 臂 run.log 单臂 10m39s–23m05s) |
| OQ-3 (L161) | 未写 | 并行约 11–23 分钟 | 约 10 美元 | 一致 |
| OQ-5 (L163) | 未写 | 并行约 11–23 分钟 | 约 10 美元 | 一致 (R6 的「半小时」已改掉) |
| OQ-7(B) (L165) | 未写 | 并行约 11–23 分钟 | 约 10 美元 | 一致 |
| OQ-2 代价 | 「两臂并行需两个临时根」 | — | — | 与两臂口径一致 |
| OQ-8 备选代价 | 「一次两臂重跑」 | — | — | 与两臂口径一致 |

### OQ 推荐项与自身代价

| OQ | 推荐 | 推荐项自身的代价 | 结论 |
|---|---|---|---|
| OQ-1 | 0.5 | 放过「2/3 才触发」的 description | 有 |
| OQ-2 | 单 worker + 独立根 | 两个临时根, 手册步骤多两行 | 有 |
| OQ-3 | 先审 | 改 query 须重跑两臂, 并行约 11–23 分钟 / 约 10 美元 | 有; 另写了未裁时的默认 |
| OQ-4 | 无推荐, 两选项各写代价 | — | 原文无推荐, 未自造默认 |
| OQ-5 | 地板守卫 | 多一条义务 (两臂约 10 美元 / 并行 11–23 分钟, 首次还要建套件), 只挡两类破坏 | 有, 备选代价也写了 |
| OQ-6 | 暂不放宽 | 每次 description 改动多跑一次场景 1 | 有 |
| OQ-7 | (A) | 每个 skill 首次改 description 等 owner 审约 15 分钟, 不在线即阻塞 | 有 |
| OQ-8 | 判据不改 | 套件没覆盖到的扩张判不出 | 有 |
| OQ-9 | 「算」 | 每个新 skill 多建一份 20 条套件并等 owner 审阅 (约 1 小时 + owner 时间) | 有, 备选代价也写了 |

### v8 新增的全称句与事实断言

| 句子 (位置) | 依据 | 结论 |
|---|---|---|
| 「`run_eval.py` 把报错、超时、非零退出都记成一次『未触发』」「`runs` 恒为 3」「只有工作进程抛异常才打印 Warning」(L51) | 本席重跑矩阵: F1–F7 七类故障全部门判未触发且 Warning 0; 唯一有 Warning 的是 F8 (垫片不在 PATH) | 成立 |
| 「单次调用须走到 run_eval 据以判定的事件 (四者之一)」(L51) | 逐行对 6 个返回点 (上表) | 成立, 且 `content_block_stop` 被 tool_use 开始蕴含, 不漏 |
| 「不健康的调用按两种可能都算 … 判定不变才 pass / fail / valid」(L51) | `lo ≤ trig ≤ hi` 可证 ⇒ pass ⇔ 门通过、fail ⇒ 门 fail | 成立 |
| 「逐调用健康检查不调用 API, 每臂几秒」(L124) | 60 次调用日志实测 0.069 秒 | 成立 (实际远快于「几秒」) |
| 「负控 ≥ 6/10, 不论被评 description 过没过门」(L55) | 矩阵 S10 (负控角色, 命中上界超限) → void | 成立 |
| 「放弃后进 S_FAIL(`container_crash`), 终态, 不重试, 默认不告警」(L125 / D5.6) | `_handle_s5_await` 非零退出分支; `_RETRYABLE_FAIL_REASONS`; 失败分析 DI 默认 None | 成立 (R6 已核 + 本轮补核 fail_detail 与反连接) |
| 「打开后同一派发至多一张通知卡, 原因由模型据 `fail_detail` 生成, 而 `fail_detail` 只有退出码与 alloc id」(D5.6) | `NOT EXISTS` 反连接注释「zero re-fires after the first analysis lands」; fail_detail 实串 | 成立 |
| 「runner 会把工作区里未提交的改动一并提交并开 PR」(D1 / D5.6) | `initial.sh` Step 10 `git add -A` + commit (R6 已核) | 成立 |
| 「runner 提示词要求『不要带着半成品提交』」(D5.6) | `prompts/issue-dispatch.md` 第 29 行 `do NOT make a commit with partial work` | 成立 (意译, 观察第 7 条) |
| 「456 个非合并提交里改了已有 description 的 7 个, 约 1.5%; 另有 15 个提交新增 skill (不含首版)」(Impact) | 16 个新增 SKILL.md 的提交 - 首版 1 个 = 15 | 口径可复现 (观察第 9 条) |
| 「`unattended` 键传递未定义, 修好之前禁令在 runner 里不会触发」(D1 / Impact) | `.aria/config.json` 的 `state_scanner.coordination` 只有 `_comment` / `enabled` / `mode`; `10CG/Aria#196` open | 成立 |
| 「场景 4b 只在 Claude 模型上实测过」(D6) | v1–v4 fable, v5 / v6 opus | 成立 |

## 实跑记录

1. `check_bare_issue_refs.py` 对 proposal / RESULT.md / `PREREGISTRATION.md` / `PREREGISTRATION-AMENDMENT.md` 各一次: 「裸 issue 引用: 0」, rc 0 / 0 / 0 / 0。
2. 禁用字形 + NUL (python 逐字符扫, 区间见 Verdict): 上述 4 个文档 + 4 个工具文件, 全部 0 / 0。
3. D1 表 (python 从 proposal 取三行三列): 旧句在 CLAUDE.md / SOT / 手册各 1; 三条新句核心句各 1、逐字相同; 三个现状文件核心句各 0; 三条新句都含「照跑场景 1」「另须跑场景 4b」; SC-5 正则 0 / 0 / 0, D2 正文 (去「不设比较判据」行) 0, D2 含「不设比较判据」1。
4. SC-11 (五个正则) 对真正待转录的六块: CLAUDE 新句 / SOT 新句 / 手册新句 / §3 边界注引号内 / §4.1 的 YAML 与三条转录条款 / §6 第三条引号内, 全部 0。(注: 按整节扫 D4 / D6 会命中非转录的说明文字, 不是转录纪律的判据面。)
5. SC-9 / SC-10 / SC-12 代理 (取 D2 正文当手册 §场景 4b): 「fail 的后果」+「不得 ship」行 1; 「作废」+「不得 ship」行 2; 含 `classify_calls.py` 行 1; 「**作废**在以下任一情形发生」的那一行同时含「逐调用健康检查不通过」「≥ 6/10」「不得 ship」= 1; 「≤ 5/10」2、「连续 2 轮」1; 「参数钉死」行同时含四个参数与「20 条」= 1。SC-12: SOT 新句五串各 1, CLAUDE 指向句 1, D6「只在 Claude 模型上实测过」1。
6. **自己重跑故障矩阵**: `python3 fault_matrix.py --out <scratchpad>/fm` → 24 用例、与预期不符 0、RC 0; 逐行结论与归档一致 (F1 6 次「result 帧报错」、F2–F4 6 次「无判定事件」、F5 / F6 6 次「耗时达到超时阈值」+「无判定事件」、F8 Warning 6 行且日志 0、F9 6 次耗时超限、S1 30 次、S2 3 次、S6 / S7 各 1 次仍 pass、S8 2 次转 void、S9 6 次仍 valid、S10 12 次转 void、M1 对不上 query 转 void)。
7. **自己做 SC-13 的反事实**: 临时副本删掉 `classify_calls.py` 的报错结果帧判定 → 24 用例、与预期不符 5、RC 1, 不符的 5 个用例名与 SC-13 所写完全一致。
8. **边界探针**: `{"results": []}` + 空日志目录 → 结论 pass、rc 0 (观察第 1 条)。
9. **可搬运性探针**: 把四个文件复制到 `<scratchpad>/mimic/aria-plugin-benchmarks/tools/trigger-eval/`, `find_suite()` 正确定位到 `ab-results/2026-09-13-…/trigger-eval-openspec-archive.json` ⇒ T2b 搬家后 SC-13 的「在新位置跑」可执行。
10. **检查脚本耗时**: 对 60 次调用的日志目录跑一次 `classify_calls.py` = 0.069 秒 (real)。
11. 归档产物核对: `fault-matrix/matrix-summary.json` 24 用例不符 0; `fault-matrix-counterfactual/matrix-summary.json` 不符 5; `real/` 四组 summary —— B1 (不存在的模型名) 2 次「result 帧报错」→ void、B2 (`--timeout 3`) 2 次「耗时达到超时阈值」+「无判定事件」→ void、C1 60/60 健康 → pass 且 `gate_recorded` true、C2 60/60 健康 → valid 且命中区间 0–0; `real/run.log` 时间戳与 RESULT 写的 C1 11m33s / C2 12m13s 吻合。两份锁定记录带 sha1 与时间戳, 分别声明「任何实验运行之前」与「v6b 任何重跑之前」。
12. SC-2 机读实证: D3 六行第三列共 14 条路径 (含 v8 新加的 `v5-mildcreep-opus5/negctrl.json`、`v6-per-call-health-opus5/claude-shim.sh`、`fault-matrix/matrix-summary.json`、`real/C1_new.classify.json`、`real/C2_negctrl.classify.json`) 全部存在; 第 4 行为唯一 `[配置推导]` 行。
13. aria-orchestrator `237045a`: `_handle_s5_await` 非零退出分支 `fail_detail = "S5_AWAIT: alloc terminated with exit_code=… alloc_id=… (container_crash)"`; `reconciler.py` 第 1153–1180 行失败分析 `NOT EXISTS` 反连接 (注释「zero re-fires after the first analysis lands」), `_RETRYABLE_FAIL_REASONS` = {infrastructure, timeout}, `_RETRY_COUNT_MAX` = 1; `prompts/issue-dispatch.md` 第 29 行 `do NOT make a commit with partial work`。
14. aria 子模块 `1cb3872`: `origin/master` 456 个非合并提交, 新增 `skills/*/SKILL.md` 的 16 个, 最早一笔 `6862a2a8` 一次加 24 份 (首版) ⇒ 「不含首版 15 个」成立。
15. 现状面: 手册「边界三条」1 / 「边界四条」0 / `^### 场景 4` 1 个; SOT「两个已知缺陷」1 / 「三个已知缺陷」0 / 五个字段名全 0; `ab-suite/version.yaml` = 1.5.0, `ab-suite/trigger/` 不存在; `.aria/config.json` 的 `state_scanner.coordination` = `_comment` / `enabled` / `mode`; `10CG/Aria#196` open, `10CG/Aria#211` open。
16. 范围: `git diff --stat c3a5903..15ab323` 只含 proposal、RESULT.md、v6 实验产物、R6 五席 + 聚合报告、triage 两文件、两个 run_arms 脚本; 无子模块 gitlink 变动。套件 20 条 query 去重后仍 20 条 (10 / 10), 不存在会让 run_eval 合并结果行的重复 query。
17. 环境: 主机 dev-claude2, git 身份 simonfishgit, 工作区干净; 本机 `claude` = 2.1.273 (RESULT 记的实验版本为 2.1.269)。
