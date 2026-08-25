---
checkpoint: post_spec
round: 3
role: backend-architect
verdict: PASS_WITH_WARNINGS
scope_ok: true
counts: 0C/3M/4m
---

# post_spec R3 — a1-entry rework v3 combined — backend-architect

**联审对象**: 母 Spec `a1-entry-claim-duplicate-work-guard/proposal.md` (第 **R3** 轮) + 子 Spec `linked-issue-field-availability/proposal.md` (第 **R1** 轮) + 子 Spec `sibling-spec-probe/proposal.md` (第 **R1** 轮)。三份**独立 verdict**, 见下; 镜头 = 实现可行性 (照 Spec 写代码第一处卡在哪)。

## 审计对象与实读环境

主仓 HEAD `027a50f` (工作树干净) = 上一 commit `cc1bdef` (母 Spec 自述基线) + 本轮三份 proposal.md 落盘。aria 子模块本地检出 `58a49e7`, 引用基线 `d50f9c3` 经 `git -C aria show d50f9c3:<path> | sed -n` 实读 (commit 对象本地可达, 已验)。全篇实读约 40+ 条 `文件:行号` 断言, **全部逐字核实通过** (含 `phase1_gate.py` 全部行号 / `collision.py` 全部行号 / `claim_lifecycle.py` / `identity.py` / `track_id.py` / `claim_schema.py` / `coordination_ref.py` / `constants.py` / `gc.py` / `release_gate.py` / `fetch_gate.py` / `run_all_tests.sh` / `remote_refresh.py` / `scan.py` / `execution-modes.md` / `report-format.md` / `DEFAULTS.json` / `layer-l-integration.md` / `state-scanner/SKILL.md` / `custom_checks.py` / `.aria/state-checks.yaml` / spec-drafter & phase-a-planner frontmatter)。两处**实跑复现**: (1) `linked_issue_field_probe.py` 的两种 import 写法, 结果与 Spec 逐字一致 (`('aria-plugin', 122)` / `ImportError: attempted relative import`); (2) `git ls-remote --symref {origin,github} HEAD` 在主仓与 aria 子模块四组合上全部实跑, 结果与 Spec 逐字一致 (`ref: refs/heads/master`)。未发现任何一处「引用不存在的函数/行」。

## R2 遗留 (3C/17M) — 本镜头相关部分, closed/still-open

C-A→已迁field-availability**已收(E0-E6钉字符级, CLOSED)**; C-B→§5.1/§5.2**已解(CLOSED, 见新M-3的边界说明)**; C-C→§2.1b**已解(CLOSED, 三处carry-id统一实读确认)**; M-1/M-5→已迁sibling-probe**已收(CLOSED, 层0-3谓词+ls-remote方案均实跑验证)**; M-6→**已收(audit-engine rule6_note点名α/β, CLOSED)**; M-9→**已收(SC-8场景列已删yielded, CLOSED)**; M-10→已迁field-availability**已收(D3新script+import机制已验, CLOSED)**; M-12→**部分收 — 3级回落已定义, 但新引入CLI冲突见M-1下方**; M-17第1/3/4/5项→**已收**; M-17第2项(改键vs增并存)→**未完全收, 见M-2**。

## 本轮新 findings

| id | severity | category | 定位 | 标题 | 证据 | 处方 |
|---|---|---|---|---|---|---|
| BA-M1 | **Major** | 实现可行性/母Spec | `phase1_gate.py:1185-1198`(现状) vs 母Spec `:215`/`:557`(×2)/`:605` | `--heartbeat-only` 字面调用形态与既有 `--phase required=True` 冲突, 第一次实跑即 argparse 拒绝 | 实读 `_main()` argparse: `--raw-track-id required=True`(`:1186-1189`), `--phase required=True`(`:1191`)。母Spec **全部 4 处**给出的 CLI 形态 `phase1_gate.py --heartbeat-only --raw-track-id "<carry-id>" --repo-path <root>` **均不含 `--phase`**。若 `--heartbeat-only` 按 Spec 唯一给出的读法(「同一 CLI 文件下的两个独立模式」)加到同一 parser, 该命令会在参数解析阶段即被拒绝(`the following arguments are required: --phase`), 根本到不了 `--heartbeat-only` 分支逻辑。全文搜索 `required`/`store_true` 零处提及此冲突 | Impact 表 `phase1_gate.py` 第二行补一句: `--phase` 改 `required=False` + `_main()` 内加条件校验 `if not args.heartbeat_only and not args.phase: parser.error(...)`; 或显式声明 `--heartbeat-only` 与 `--phase` 互斥组 (`add_mutually_exclusive_group` 不适用于此处需求, 需手写校验) |
| BA-M2 | **Major** | 自洽性/母Spec | `:454`(D4) vs `:188`(口径统一声明) | 决策记录 D4 仍用「匹配键**改**」措辞, 与「全文自此只用『增并存变体』」的自我约束矛盾 | `git diff` 内 grep 确认: `:188` 逐字「**全文自此只用「增并存变体」这一种措辞**」, 但 `:454` D4 行原样保留「heartbeat **匹配键改** `(container, track_id)`, 刷新全部匹配」——「改」与「增并存」是两种不同实现(改现有键会打破 Phase B 既有认领路径, 撞 §非目标)。这正是我任务brief点名要验的「两读是否已统一」, **答案: 未完全统一**, D16 是修正版但 D4 未同步删除/改写, 是 R2/M-17 fix 遗留的同形残留(memory `fix-the-class`) | 把 `:454` D4 一行内容改为「⛔ 已被 D16 取代, 见 D16」, 不删行不改编号(决策记录无 SC 式编号纪律但同理保留可追溯) |
| BA-M3 | **Major** | 契约完整性/母Spec | 母Spec自陈"新表面#6"/"未做#5" vs `state-scanner/SKILL.md:176`(现状) | `linked_issue_overlap` 返回型从恒`list`放宽为`list\|null`, 但已存在的 Phase B 消费文档未同步, 且 Phase B **确实会** 传 `--linked-issue` | 实读 `phase-b-developer/SKILL.md:93`: `[--linked-issue "<repo>#<n>"]` 是**可选但存在**的实参位, 非母Spec自述"Phase B 两个入口都不带"(那句指的是 `--include-terminal`, 不是 `--linked-issue`, 两者混淆); 而 `state-scanner/SKILL.md:176` 现描述 `linked_issue_overlap[]`(暗示恒列表)但**该行不在母Spec Impact表覆盖范围**(Impact表`state-scanner/SKILL.md`行只提"Layer L A.1 heartbeat集成"新增小节, 未提`:176`现有段落的同步)。若 Phase B 消费方沿用旧文档做真值判断(非空即告警), `null` 会被当 falsy 静默吞成"无碰撞"——正是本Spec要根治的「零证据当正证据」, 换了条未审的路径复现 | Impact 表 `state-scanner/SKILL.md` 行追加: 同步 `:176` 措辞為四态感知, 或至少显式声明"Phase B 侧本轮不处理, 残余风险成文"(仿§6缺口表体例), 而非仅留在"新表面"自陈段 |
| BA-m1 | minor | 完整性/母Spec | Impact表`identity.py`行 | 新 uuid accessor 无函数名/签名 | 全文搜索, 该函数仅以"新增直取 uuid 字段的 accessor"描述, 无具体 def 签名(对比`--heartbeat-only`/`unknown_schema_claims`等其他新增项均给字面量) | 补一行如 `def get_container_uuid(home_dir=None) -> str` |
| BA-m2 | minor | 完整性/sibling-spec-probe | `sibling_spec_probe.py` 全文 | 新脚本无 CLI 调用签名 | 对比姊妹 Spec field-availability §4 对 `linked_issue_field_probe.py` 给了精确 argv 约定(`argv[0]`=repo root, 照抄两个既有探针), 本 Spec 全文未给 `sibling_spec_probe.py` 的 `main(argv)` 签名或调用命令行, §8 两处插入串也只是`每轮入口: 竞品 spec 探针`纯文本 | 补 `def main(argv: list[str] \| None=None)->int` 签名 + 一行调用命令, 照抄已验证的 `argv[0]` 惯例 |
| BA-m3 | minor | 数字新鲜度/field-availability | §4 "共10条check" | `.aria/state-checks.yaml` 当前(HEAD `027a50f`)实测 **11** 条, 非10 | `grep -c '^  - name:'` = 11; 新增 `main-project-version-consistency`(:289, 由中间commit `2ae012f` 引入, 晚于Spec基线`cc1bdef`)。**不影响设计结论**(新check同为(iii)类`.aria/probes/`, 反而加强"并存"论据) | 一行订正"10→11", 按Spec自身"口径vs观测值"惯例处理即可, 非阻塞 |
| BA-m4 | minor | 论证严谨性/sibling-spec-probe | §5(d) P1"必然超时"论证 | 自引数字实际上不支持"必然超时" | (a)13.8s+(b)10.5s=24.3s均值, 即便取(a)最差样本15.9s+(b)10.5s=26.4s, 均 **< 30s** ⇒ "若当整轮预算, 本仓单轮就会必然超时"与自身数据不符。**但结论(每子进程独立30s优于整轮共享30s)本身是合理工程判断**, 不受此影响 | 措辞改"逼近预算上限、且第三方仓语料更大时会超"或直接删"必然"二字 |

## 经本轮实读确认成立的部分 (下轮免重复)

母Spec全部F-1~F-42实测事实(逐条已核实, 含"三读同源验证"链条: `collision.py`/`claim_schema.py`/`claim_lifecycle.py`/`identity.py`/`track_id.py`/`constants.py`/`gc.py`/`phase1_gate.py`门控与异常路径/`layer-l-integration.md:45`悬空函数名`update_heartbeat()`确认不存在); field-availability §4的两种import写法**已实跑复现一致**; sibling-spec-probe §4的`ls-remote --symref`四组合**已实跑复现一致**, `git symbolic-ref`失败/`refs/remotes/probe`陈旧/`refs/aria/*`三条既有ref/`remote_refresh.py`唯一生产调用点`scan.py:312`/`run_all_tests.sh`自动发现机制, 均逐字确认。C-B(§5.1形态判据由AI在派生时的session-local知识决定, 非需要CLI字符串反解析, 可行)、C-C(carry-id三处统一, 可行)均判定可实现。三份子Spec对R2迁出项(C-A/M-1/M-2/M-5/M-6/M-10/M-17各子项/FIX-06/07/08/10)**逐一核对, 确认均被接住**, 无"迁出即丢弃"情形(回应母Spec"未做#6"的自陈缺口)。

## scope_ok

**true** (三份)。变更面均未溢出各自 §依赖方向/非目标声明。

## 三份 verdict

- **母 Spec (R3)**: **PASS_WITH_WARNINGS** — 0C/2M(BA-M1/BA-M2)/1m(BA-m1)+BA-M3跨文件
- **linked-issue-field-availability (R1)**: **PASS_WITH_WARNINGS** — 0C/0M/2m(BA-m3 + 分摊BA-M3消费面缺口的另一半)
- **sibling-spec-probe (R1)**: **PASS_WITH_WARNINGS** — 0C/0M/2m(BA-m2/BA-m4)

## Combined verdict: PASS_WITH_WARNINGS (0C/3M/4m)

无 Critical、无"改不存在函数"类硬伤; 3 条 Major 均为**浅层可机械修复**(补一个校验/改一行措辞/补一行 Impact), 非架构级返工。
