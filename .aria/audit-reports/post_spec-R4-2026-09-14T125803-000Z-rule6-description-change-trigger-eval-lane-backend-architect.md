---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS
timestamp: 2026-09-14T13:32:01.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [backend-architect]
---

# post_spec Round 4 — backend-architect

被审对象: proposal.md v4 (HEAD `e822829`) + RESULT.md v4 (含 v5-mildcreep-opus5/ 三臂、run_arms_v5.sh、neutral-skill-SKILL.md、probe-setting-sources-*.json)。任务: 对账本席 R3 唯一 major、复核 v4 新增机制内容 (v5 三臂同构性 / D2 fail-void 穷尽性 / OQ-9 可行性)、排查新引入问题。

## R3 对账

**本席 R3 唯一 major → closed。**

R3 原文: D5.4 (ii) 与 RESULT.md §结论3(b)、§Why 第3条三处同源断言「文件名、`# <skill_name>` 标题、`This skill handles:` 首句」三处都「嵌入技能名」, 但 `run_single_query` 首句模板 `f"This skill handles: {skill_description}\n"` 嵌入的是 `skill_description` 参数, 不是 `skill_name`, 结构上不可能泄漏技能名。

核对 v4 现文三处同源表述, 均已改为「两处」+ 明确排除首句:
- Why 第3条 (proposal.md L20): 「合成技能的文件名与 `# <skill_name>` 标题都嵌入技能名」。
- D5.4 (proposal.md L95): 「文件名与 `# <skill_name>` 标题两处都要改 (`This skill handles:` 首句嵌的是 description, 不是技能名, 不在修复范围; 检测串仍保留 uuid, `clean_name in accumulated_json` 照常工作)」。
- RESULT.md v4 §结论3(b): 「命令文件名 `<skill_name>-skill-<id>` 与正文标题 `# <skill_name>` 两处嵌入技能名 (正文首句 `This skill handles: <description>` 嵌的是 description, 不是技能名)」。

三处逐字核对一致, 且与 `run_eval.py:52-54,65-66` 的代码结构完全吻合 (`clean_name` 嵌入文件名、`f"# {skill_name}"` 嵌入标题, 两处均引用形参 `skill_name`; 首句引用的是独立形参 `skill_description`)。全文 grep 未发现遗留的「三处都嵌入技能名」表述。**判 closed, 准确。**

修复方向 (ii) 对上游是否足够: 「文件名/标题两处不嵌入技能名, 检测串仍保留 uuid」这条指令本身可执行且自洽 —— 只要 `clean_name` 仍含 `unique_id` 子串, `clean_name in accumulated_json` 的检测逻辑与 `skill_name` 是否出现在 `clean_name` 里无关, 不会因为改掉技能名而失效。复现证据 (v2 负控 27/30 → v3 中性名后负控 8/30) 与代码行号引用足够具体, 上游据此定位问题不需要额外信息。**修复方向本身足够; 若要更完整, 首句是否需要连带处理应换一个不依赖「嵌入技能名」的理由再决定, 但 v4 已经把它从修复范围里明确移出, 不留歧义, 不构成新的阻塞。**

## Findings

无 (R3 唯一 major 已 closed; 本轮未发现新的 critical / major; 未发现须在 Phase B 前处理的 minor)。

## 观察

- **`run_eval.py` 崩溃是「门/作废」二分之外真实存在的第三种输出形态, 但不构成阻塞**: `main()` 里 `parse_skill_md(skill_path)` 在任何 try/except 之外被调用, `utils.py` 对缺失或格式错误的 frontmatter 会 `raise ValueError` (未捕获); `skill_path/SKILL.md` 不存在时 `sys.exit(1)` (run_eval.py:275-277)。两者都发生在 `run_eval()` 执行之前, 会导致该臂 stdout 为空 (`$name.json` 零字节, traceback 落在 `$name.err`), 进程以非零码退出。这与 D2 定义的「门 fail」(有 `pass=false` 行, JSON 结构完整) 和「作废」(JSON 结构完整但负控超阈值) 都不同, D4 的 `rule6_note` 值域 (`pass|fail|void|not_required|n/a`) 没有对应取值。**不算阻塞**: 空文件 / 非零退出码是显而易见的「没跑成功」信号, 不会被误判为 pass/fail/void 中的任何一个, 执行者 (人类或 Layer 2) 的自然反应是重跑而非误分类; 此形态自 v1 起就存在, 不是 v4 新引入, 三轮审计均未把它当阻塞项。若要收尾, 可在 D2 或手册加一句「`run_eval.py` 非零退出 ⇒ 视为未完成, 重跑, 不落 `rule6_note` 三态」, 但这是可选的完整性打磨, 不是本轮收敛门槛。
- **OQ-9 未点名 GLM 基线应在哪个环境跑**: 从机制上看, `run_eval.py` 依赖的是 Claude Code CLI 自身的 `stream-json`/`tool_use` 事件格式 (`--output-format stream-json --include-partial-messages`), 这是 harness 对模型输出的规范化封装, 不是 Anthropic 模型专属的原始协议; `skill-creator` SKILL.md 自身也说明触发机制是「`available_skills` 列表 + 模型决定」, 与后端模型无关。只要调用的 `claude` 二进制确实是 Claude Code、且该次调用能被路由到 GLM (via Luxeno), `run_eval.py` 代码本身没有「非 Claude 模型下无法运行」的硬阻碍。但 OQ-9 的措辞 (「在 GLM 上跑一次…基线」) 没有点名这必须在 Layer 2 (aria-runner 容器, 已配置 Luxeno 路由) 或等价配置的环境下跑 —— 在本机 (v1–v5 的执行环境, 走真实 Anthropic 后端) 直接对 `--model` 传 GLM 别名大概率会因模型不被当前后端识别而失败, 不是「换个 --model 参数」这么简单。这是执行细节缺口, 但 OQ-9 本身是待 owner 裁的开放问题、非当下要执行的动作, 缺口留给日后落地 OQ-9 时处理即可, **不阻塞本轮 Phase B**。
- D2「负控 query 级命中须 ≤5/10」一句仍未加「(should-trigger 子集)」六字限定 (本席 R3 已提过, 定性为不阻塞观察); 本轮维持同一判断, 不再重复列为待办。

## Verdict

**PASS** — 0 critical / 0 major / 0 (阻塞) minor (本席视角; 计数含 R3 对账后归零的 1 条 major)。

## Vote

PASS

## 机制核实记录

- 逐字比对 proposal.md v4 (`e822829`) 与 R3 报告引用的 v3 (`0c41e53`) 文本, 定位 Why 第3条 / D5.4 / RESULT.md v4 §结论3(b) 三处「嵌入技能名」表述的具体改动, 确认均改为「两处」并显式排除首句, 与本席 R3 提出的修复方向一致。
- 重读 `run_eval.py:35-67` (`run_single_query` 构造 `command_content` 的完整代码块), 确认 `clean_name`(文件名, L52-54)、`f"# {skill_name}"`(标题, L65) 引用形参 `skill_name`; `f"This skill handles: {skill_description}"`(L66) 引用独立形参 `skill_description`, 二者在函数签名与调用处均无交叉赋值, 结构上不可能通过首句泄漏技能名 —— 与 R3 结论一致, v4 表述现已对齐代码。
- 对比 `run_arms_v3.sh` / `run_arms_v4.sh` / `run_arms_v5.sh` 三份脚本: 隔离项目根命名模式 (`$S/trigger-proj-v{N}-$name`)、`--num-workers 1`、`--runs-per-query 3`、`--timeout 120`、显式 `--model`、经 `claude-shim.sh` 注入的 `--setting-sources project`、中性名 `helper` 壳 (`neutral-skill-SKILL.md`) 六项配置在 v5 与 v3/v4 之间逐项同构, 仅版本号后缀与被测 description 文本按轮次不同而不同 (预期内变量)。
- `cat v5-mildcreep-opus5/run.log`: mildcreep/new/negctrl 三臂起始时间戳完全相同 (`2026-09-14T12:28:13Z`), 与 `&…&…&…& wait` 的并行启动语义一致, 确认「三臂同批」的自述准确; 结束时间跨度 12:43:31–12:47:54 与 RESULT.md v4「单臂 15m18s–19m41s」逐一算术核对一致 (mildcreep 15m18s / new 18m16s / negctrl 19m41s)。
- `python3 json.load` 解析 `v5-mildcreep-opus5/{new,mildcreep,negctrl}.json`, 逐行核对: new 与 mildcreep 均 should-trigger 侧 10/10 (每条 3/3)、should-not 侧 0/10 (每条 0/3), 门通过; negctrl should-trigger 侧 0/10 (每条 0/3), should-not 侧 0/10 — 与 RESULT.md v4 §v5 表格「30/30 (10/10) · 0/30 (0)」「0/30 (0/10)」逐字段吻合, 且与 PREREGISTRATION.md 跑前写定的判读规则 (mildcreep 门通过 ⇒ 局限确认而非失效) 对应无误。
- `python3` 比对 `trigger-eval-openspec-archive.json` (20 query 集合) 与 v5 三份输出各自的 query 集合, 三者与基线套件完全相等 (`==` 为真), 确认 v5 沿用同一套件, 无套件漂移。
- 逐行核对 `run_eval()`(`run_eval.py:184-256`) 的 `did_pass` 语义, 枚举 (门通过∧负控≤5)/(门通过∧负控≥6)/(门不通过) 三分支覆盖负控命中数整数域 `[0,10]` 且两两不重叠, D2「fail 的后果」(不得 ship, 二选一处置或升级 owner) 与「作废」(不得 ship, 重跑或升级 owner) 分别覆盖门 fail 与门 pass∧负控超阈值两种互斥场景, 无空集真空、无遗漏格 (与本席 R3 已完成的同一论证结论一致, v4 新增的「fail 后果」段未破坏该穷尽性)。
- `grep -n "sys.exit\|raise\|except"` 扫描 `run_eval.py` 全文 + 读 `scripts/utils.py::parse_skill_md`: 确认 `main()` 中 `parse_skill_md` 调用在任何 try/except 之外, frontmatter 缺失时会 `raise ValueError` 未被捕获; `SKILL.md` 不存在时 `sys.exit(1)`; 两者都发生在 `run_eval()` 调用前, 会产生空 `.json` 输出而非结构完整的 pass/fail/void 之一, 确认这是 D2 二分类之外真实存在但不阻塞的第三种失败形态 (见观察)。
- 读 `SKILL.md`(skill-creator, L398) 「Skills appear in Claude's `available_skills` list with their name + description, and Claude decides whether to consult a skill based on that description」, 与 `run_eval.py` 的 `--output-format stream-json --include-partial-messages` 依赖的 `content_block_start/delta/stop` 事件属于 Claude Code harness 自身的规范化输出, 非模型专属协议, 用于支持 OQ-9 可行性判断 (见观察)。
- 重读 `aria-orchestrator/docs/architecture-decisions.md` §AD10 全文, 核对「Aria 2.0 流水线只保留 1 个人类审批 gate, 位置在 S7_AWAITING_MERGE」与 proposal.md §OQ-7/§Impact 引用逐字一致, 未发现引用失实。
