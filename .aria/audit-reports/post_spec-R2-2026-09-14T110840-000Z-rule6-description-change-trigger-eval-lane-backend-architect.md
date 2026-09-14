---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-14T11:08:40.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [backend-architect]
---

## R1 对账

被审对象: proposal.md v2 (HEAD 55bc9f3) + RESULT.md v2 (含 v4-counterfactuals)。逐条核对 R1 中 found_by 含 backend-architect 的 5 条 (major-12 / major-5 / minor-17 / minor-22 / minor-23)。

1. **major-12「真实项目根未验证」→ partially closed**。`run_arms_v4.sh` 的 `realroot` 臂造了 11 组 `openspec/changes/<c>/{proposal.md,tasks.md}` + 1 个 `openspec/archive/2026-08-01-example-change/proposal.md` + `docs/handoff/2026-09-01-example.md` + 空 `.aria/audit-reports/` + `README.md`, 约 25 个文件, 跑出 `realroot.json` 20/20 全 pass (should-not 10 条全 0/3 触发, 与空根 v3 一致)。这证实「第一个 tool_use」判据在这一档「有少量可探索文件」的根下没有被破坏。但这不是「真实项目根」本身 (无 `CLAUDE.md`、无竟品 skill、无深层嵌套、文件量比 aria-plugin/Aria 主仓小一到两个量级) —— RESULT.md §已知局限第 4 条如实写明「更大的真实仓 (如 Aria 主仓, 有 CLAUDE.md 与数百文件) 未验证」, 限定动作到位, 但 R1 原诉求的前半 (在真正的大型真实仓里验证) 仍未做, 只做了后半 (钉限适用范围)。判 partially closed。
2. **major-5「rule6_note 模板宿主 (D4)」→ closed**。D4 改口为「本 Spec 新建最小结构化模板 (五字段, 宿主 = SOT §4)」, 不再说「加两栏」; 与 SOT `skill-benchmark-exemption.md:47-56` 现状 (只一句散文) 不冲突, 因为这是新建而非编辑既有结构。SC-3 的反事实 (现行 SOT 五个字段名 grep 为 0) 与「新建」动作一致, 不再存在「模板不存在却要加栏」的悬空引用。closed。
3. **minor-17「97→13 无机读产物 + model 半条不同类」→ closed**。`probe-setting-sources-default.json` / `-project.json` 现已存在, `result` 字段分别为 `"97,yes"` / `"12,no"` (机读, 已用 `test -e` 与内容核对), RESULT.md v2 引用的数字 (97/12) 与探针一致。D3 第 4 行「显式 --model」明确标注「配置推导, 无对照实测」, 把「这条本来就不是同类实证」的疑虑从隐含变成显式声明, 满足 SC-2 对该行的例外许可。closed (残留一处数字漂移单独记入 Findings, 不影响本条闭合判断)。
4. **minor-22「v1→v2 双变量 (结论 3a)」→ closed**。RESULT.md §结论 3(a) 现文: 「注意 v1→v2 同批改了两个变量, 记分表本身分不开; 机制证据是 `diag02-sibling-command-collision.jsonl`…弥补了这层不精确」——把 R1 要求「点破论证结构」的动作原样做了, 且未新增反例。closed。
5. **minor-23「上游反馈内容要求 (D5.4)」→ partially closed**。D5.4 现要求反馈含「复现步骤、diag02 jsonl、v1/v2/v3 记分表、两条修复方向」, 解决了 R1「只要求发出证据、不要求含材料」的结构性缺口。但深挖两条修复方向的第二条「命令文件名不嵌技能名」逐字只对应 `run_eval.py:52,54` (`clean_name` / 文件名), 未覆盖 `:65-66` 的正文头「# {skill_name}」与「This skill handles: {skill_description}」——而 RESULT.md 自己 §结论 3(b) 的诊断原文是「命令文件名**与正文** = `<skill_name>-skill-<id>` / `# <skill_name>`」, 两处都点名了。修复方向的表述比诊断窄, 若上游按字面只改文件名, 正文头仍会原样泄漏技能名, 复现 bug (b)。判 partially closed, 详见 Findings F2。

汇总: closed 3 / partially 2 / open 0。

## Findings

- [minor] testing/RESULT.md §已知局限·D3 第1条 (issue): v4 realroot 用约 25 个合成文件近似「真实项目根」, 未含 CLAUDE.md/竟品 skill/深层嵌套, 与「aria-plugin/Aria 主仓」量级仍有一到两个量级差距; RESULT.md 已如实限定适用范围, 但 R1 原诉求「真实仓验证」本身仍未完成。
- [minor] architecture/proposal.md §D5.4 (issue): 上游反馈第二条修复方向「命令文件名不嵌技能名」逐字只指向 run_eval.py 的 clean_name/文件名 (行52/54), 未覆盖同样泄漏技能名的正文头「# {skill_name}」与「This skill handles: {desc}」(行65-66); RESULT.md 自己的 (b) 诊断点名「文件名与正文」两处, 修复方向表述比诊断窄, 按字面修可能只改文件名而正文头仍原样复现泄漏。建议措辞扩为「clean_name (文件名+检测串) 与正文头/内容均不嵌真实技能名」。
- [minor] testing/manifest.json vs RESULT.md v2 §隔离 (risk): manifest.json 仍写「技能数 97→13」, RESULT.md v2 与新探针给出「97→12」; RESULT.md「原始产物」段已声明 manifest.json 保留原样作历史、请看本文表格 (免责已到位), 但 13→12 这个具体变化本身 (四舍五入 / 不同探针口径 / 单次抽样误差) 未被解释, 留一处未消歧的数字漂移, 细心读者会疑惑两次探测是否可比。
- [minor] testing/v4-counterfactuals/overbroad.json §机制解读 (issue): overbroad description 原文含显式强制指令「只要用户提到…中任意一个词, 都必须先使用本技能」, 是「关键词撞库 + 强制指令」触发, 不是纯语义泛化; 22/30 (7/10) 的 FAIL 分布与该关键词表高度相关但非严格线性 (如「分支+归档」双关键词命中的 query 反而 0/3 未触发, 单一「handoff」关键词命中的 query 却 3/3 触发)。这足以证明 D2「should-not < 0.5」半边门在存在性意义上可达 (backend 本轮任务2的核心问题有答案: 是, 门可达), 但只证明了「显式强制指令式过宽」这一种失效模式会触发它, 未证明「不带强制词、只是范围写宽的自然过宽 description」同样能可靠触发同一半边门; proposal/RESULT 均未加此层限定, 读者可能把「门可达」泛化为「对任何过宽描述都可达」。

## Verdict

PASS_WITH_WARNINGS — critical: 0, major: 0, minor: 4 (本席视角)。R1 中由 backend-architect 提出的 5 条 (1 major + 3 minor + 1 major-adjacent 的 D4 项) 经核实: 3 条 closed, 2 条 partially closed (均为「诉求主体已回应, 但深挖后发现表述/范围比证据窄一档」的精度缺口, 非推翻式缺陷); 新增 1 条机制层面观察 (overbroad 触发机制是关键词撞库而非语义泛化)。四条新 finding 均为 minor, 不构成对 D1-D6/OQ 结构或 RESULT.md v2 三条核心结论 (饱和退化 / 地板守卫两侧有FAIL样本 / 三处缺陷) 的推翻理由, Phase B 落地前可随手补一句限定即可, 不阻塞收敛。

## Vote

PASS

## 机制核实记录

- 读 `proposal.md` v2 全文 (D1-D6, Tasks, SC-1~8, OQ-1~7, rule6_note), 核对 D4/D5.4/D3 逐字与 R1 对账用词。
- 读 `RESULT.md` v2 全文 (§记分/§统计/§结论/§已知局限/§原始产物), 核对结论3(a)(b)/负控分布/97-12数字/已知局限第4条。
- `cat run_arms_v4.sh`: 核对 realroot 臂构造的文件集合 (11×proposal+tasks / 1×archive例 / 1×handoff / 空 audit-reports / README), 判定"多真实"。
- `python3` 解析 `v4-counterfactuals/{overbroad,realroot}.json`: 逐条打印 `should_trigger/triggers/runs/pass/query`, 核对 summary (13/20, 20/20) 与 RESULT.md 记分表 (30 should / 22 should-not; realroot 30/0) 一致; 核对 overbroad 的 FAIL 分布与 description 关键词表的对应关系 (非严格线性, 见 Findings)。
- `python3` 解析 `probe-setting-sources-{default,project}.json` 的 `result` 字段: 分别为 `"97,yes"` / `"12,no"`, 与 RESULT.md v2 引用数字一致; 与 `manifest.json` 里旧数字 "97→13" 比对, 确认漂移未获解释 (但 RESULT.md 已对 manifest.json 整体做免责声明)。
- 读 `run_eval.py` 全文 (`find_project_root` :22-32, `run_single_query` :35-181 含 `clean_name` 构造 :52 / 命令文件内容 :60-68 含正文头 :65-66 / 触发检测 :128-171, `run_eval` :184-256 含 `did_pass` 语义 :227-242, `main`/argparse :259-296): 核对 D2「参数钉死」与 D3 覆盖的完整 argparse 参数面 (`--eval-set`/`--skill-path`/`--description` 为数据面非语义面; `--num-workers`→D3#1, `--model`→D3#4, `--runs-per-query`/`--trigger-threshold`/`--timeout`→D2 三项, `--verbose` 不影响判据), 未发现遗漏参数; 核对「clean_name in accumulated_json」检测机制不依赖 skill_name 是否出现在 clean_name 里, 只依赖 uuid 唯一性 + 文件名/检测串一致, 故 D5.4 修复方向 2 若只改文件名 (clean_name 组装去掉 skill_name), 检测机制仍成立 —— 但正文头 (:65-66) 是另一条独立泄漏面, 修复方向文字未覆盖。
- 读 `utils.py::parse_skill_md` (:7-47): 确认 `name`/`description` 抽取逻辑与 `neutral-skill-SKILL.md` (`name: helper`) 配合 `run_arms_v3.sh --description` override 的机制成立, 与 R1 已核实结论一致, 本轮未发现新问题。
- `find`/`test -e` 核对 D3 六行前置表的机读实证路径 (`v1-shared-root-4workers/*`, `v2-isolated-root-1worker/*`, `v3-isolated-root-1worker-neutral-name/*`, `diag02-sibling-command-collision.jsonl`, `neutral-skill-SKILL.md`, `probe-setting-sources-{default,project}.json`, `v3.../negctrl.json`) 全部存在, SC-2 机读证据面成立; 第 4 行「配置推导, 无对照实测」按 proposal 措辞如实, 不违反 SC-2 例外条款。
- 核对 D3 第 1 条「单 worker 消除同根内兄弟命令文件; 独立根允许多臂并行」两句是否正交: 从 `run_single_query` 的 `command_file` 生命周期 (创建于函数入口, `finally` 块 `unlink`) 与 `run_eval` 的 `ProcessPoolExecutor(max_workers=num_workers)` 提交逻辑 (同一 `project_root` 值对该次 `run_eval()` 调用内所有 future 共享, :198-211) 推导: num_workers=1 保证同一 `run_eval.py` 进程内任意时刻最多一个命令文件存在 (消除同根内兄弟); 独立根解决的是"多个不同 `run_eval.py` 进程 (对应不同臂) 并行跑" 时彼此不共享同一 `.claude/commands/` 目录的问题, 即使各自 num_workers=1, 若共享根仍会在并行窗口内互相看到对方的命令文件。两者作用面不同、缺一不可, 且经 `diag02-sibling-command-collision.jsonl` (v1: 共享根+4 worker) 独立证实机制层面的跨 worker 泄漏, 确认 D3 第 1 条拆分正确。
