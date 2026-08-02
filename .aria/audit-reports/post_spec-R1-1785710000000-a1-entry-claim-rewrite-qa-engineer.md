# post_spec R1 (重写 v2) — qa-engineer

**审计对象**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` @ `c6aa29a` (2026-08-02 17:54 UTC)
**verdict**: REVISE
**scope_ok**: true
**counts**: critical=0 major=4 minor=5

**一句话结论**: **SC-1~4 四个历史钉子全部钉住** —— 逐条构造了「原始版 / R1-fix / R2-fix / R3 指出的空隙」四个错误实现并对照实际源码验证, 无一漏钉, 这是本轮最重要的正面结论。但 SC-5~19 这一层出现了系统性的「标签与实测不符」问题: 两条被标『代码』的 SC (SC-9/SC-14) 实际验证对象是 SKILL.md 散文, 本仓已有先例证明这类断言会退化成文本存在性检查; 两条『代码, CLI 全链路』SC (SC-8/SC-10) 把消费层措辞硬塞进 CLI 断言, 而 CLI 只吐 JSON 不产出文案; §3 的「双落点」—— 本版重写反复强调的核心杠杆 —— 在 SC-1~19 里**零覆盖**。

---

## Part 1 — SC-1~4 历史钉子验证 (本轮最重要的部分)

方法: 对每一条, 用 `git show` 取出对应历史 commit 的**原文**(非转述), 在其上机械推演 SC 是否必红。

| SC | 钉住的版本 | 历史原文实证 (commit) | 构造推演 | 结果 |
|----|-----------|----------------------|---------|------|
| **SC-1** | 原始版 (`552ec5a`) | `--raw-track-id "<spec-slug 或 handoff §6 carry-id>"` (原文 :73) | track_id 直接等于 spec-slug。改名 (如 `a1-entry-claim-duplicate-work-guard` → `a1-entry-claim-guard-v2`) 后, 同一段代码对新 slug 重新 `derive_track_id()`, 产出**不同**字符串 | **✅ 钉住** — 「改名前后不变」在此实现上必红 |
| **SC-2** | R1-fix 版 (`efca1d5`) | `--raw-track-id` 取值订正为「A.1 一律用 issue 派生的稳定串 `<归一后 repo_basename>-<number>`」(原文 :125), 例 `aria-plugin-122` | 两容器同做 `aria-plugin#122` ⇒ 均派生 `aria-plugin-122` (无容器段) ⇒ `collision.py:219-220` 的 `if c.track_id == own_track_id: continue` 互相排除 ⇒ 双方 `linked_issue_overlap` 恒 `[]` | **✅ 钉住** — 这正是 R2-fix 版自己写的「SC-5b」逐字验证过的红窗 (`23f34a6` 原文 :253), 新版 SC-2 是它的直接传承, 复核一致 |
| **SC-3** | R2-fix 版 (`23f34a6`) | `--raw-track-id "<basename>-<number>-<container-short>"`, `container-short` 取 `~/.aria/container-id` **前 8 位** (原文 :125,:136) | `identity.py:126-135` 的文件模板原话邀请用户设 `label` (例 `"devbox-A"`)。`get_container_id()` (`identity.py:222`) 是 `label if label else uuid` — label 优先。两容器分设 label `"devbox-A1"`/`"devbox-A2"`, 各自 `get_container_id()` 返回该 label, 取前 8 位均为 `"devbox-A"` ⇒ 同 track_id ⇒ 同 SC-2 的排除后果换个触发源复现 | **✅ 钉住** — 且新版处置(直取 `uuid` 字段跳过 `label`, 不截断)精确对应该反例，`identity.py` 目前确实**没有**这样的 accessor (只有 label 优先的 `get_container_id()`)，需新增，属实 |
| **SC-4** | R3 指出的空隙 (非独立版本) | R3 报告 M3b: 「`<number>` 段未定义用归一后 int 还是原串」——**这是 R2-fix 遗留的规格空白**, 不是像前三条那样「曾实现又被推翻的具体版本」 | 若实现按字面截取 `#` 后的原始子串 (不转 int), `#007` → `...-007`，`#7` → `...-7`，两者不等 | **✅ 逻辑钉住**，但**标题夸大**: 表头「四个被推翻版本的红窗」暗示四条都对应「曾经存在又被拿掉的实现」，SC-4 实际对应的是一处从未定案的空白。不影响可证伪性，是措辞精度问题 (见 Finding F8) |

**结论**: 三个真实存在过的历史实现 (原始 / R1-fix / R2-fix) 均被对应 SC 正确钉死；每一条我都用 `git show <sha>:proposal.md` 取了原文，不是转述审计报告的转述。这是判断「第五版会不会重踏覆辙」最硬的证据，答案是**不会踩这三个坑**。

---

## Part 2 — SC-5~19 逐条红窗表 (独立验证，含 proposal 未给出「怎么会红」的补答)

> SC-13~19 在 proposal 原文里**没有「怎么会红」列**（只有 SC/场景/期望三列，对照 SC-1~12 都有第四列）。下表「怎么会红」列为本次审计补齐的独立判断，非转录原文。

| SC | 我的判断: 它怎么会红 | 结论 |
|----|---------------------|------|
| SC-5 (heartbeat 跨调用) | 属实：`claim_lifecycle.py:225-238` 现状按 `(container_id, session_id)` 定位，而 `identity.py:252` 明文「Each call returns a fresh value」——两次 subprocess 调用天然不同 session_id，第二次必 `claim_not_found` | 良好，可红 |
| SC-6 (一对多全部刷新) | 若实现照抄现有 `heartbeat()`/`release_claim()` 的单条 `break` 模式而非 `release_claim_by_track` 的「遍历全部」模式，只会刷新第一条命中，其余仍会被 sweep | 良好，可红 |
| SC-7 (超 TTL 未刷新仍被 sweep) | 这是「加了 heartbeat 后不能反向破坏 sweep」的防回归控制；`gc.py` 的 `sweep_stale_active` 只读 `heartbeat_at`，与新增的 by-track 变体无耦合点，只要新变体不误触发全量刷新就不会破坏它 | 良好，可红（防回归性质，非新增能力） |
| SC-8 (CLI 全链路可见 done/abandoned/yielded) | **部分**：`collision.py:210` 的 `_TERMINAL = ("done", "abandoned", "unknown")` **不含 `"yielded"`**——`yielded` 状态的 claim 在现状代码上本来就不会被跳过，已经可见。「现状必红」这句对 done/abandoned 两态成立，对 yielded 不成立（它今天就是绿的）。若测试把三态合并成一条断言仍能正确捕获 done/abandoned 的红，不算错，但「怎么会红」的表述对三态一概而论不准确。另见 Finding F3（「措辞按 status 分档」半句不可 CLI 验证） | 部分良好，两处精度问题 |
| SC-9 (coordination.enabled=false 零调用) | 见 Finding F2 —— 实际验证对象是 SKILL.md 散文，非代码 | **有问题** |
| SC-10 (fetch 降级 error 契约) | 核心字段可红：`_main()` 现状在 `read_claims/linked_issue_overlaps` 抛异常时直接 `out["linked_issue_overlap"] = []`(:1236-1237)，且 `GateResult.error` 文档预留 `"fetch_degraded"` (:210) 但全文档 0 处赋值(grep 确认)——这部分是真实、可 CLI 验证的红窗。但「消费面渲染『未能核实』」半句是措辞层，CLI 只吐 JSON 不产文案，同 SC-8 问题（见 Finding F3） | 部分良好，一处问题 |
| SC-11 (overlap 非空→AskUserQuestion) | 诚实标「行为」。两臂（问 vs 渲染后自行继续）理论上可通过 transcript 检查工具调用顺序区分，但该判别能力本身未经 spike 验证（见 Finding F7） | 标签诚实，底层假设未验证 |
| SC-12 (未传 --linked-issue 不得跳过) | 同 SC-11，两臂（调用带 flag vs 不带）可通过检查实际 Bash/工具调用参数区分，同样未 spike | 标签诚实，底层假设未验证 |
| SC-13 (custom check) | 见 Finding F5 —— 被测对象大概率是通用 runner 而非本 check 语义 | **有问题** |
| SC-14 (abandon→release) | 见 Finding F2 —— `release_gate.py --status abandoned` 是已存在、已测试 (`test_release_abandoned_roundtrips`) 的既有能力，本 Spec 唯一新增的是「AI 记得调用」这一散文义务，代码层面无法区分「改前/改后」 | **有问题（与 SC-9 同形）** |
| SC-15 (改名两步 release+acquire 无孤儿) | 属实且是新组合：`coordination_ref.py:787` 确认存储路径是 `claims/<container>/<session>.yaml`，而每次 CLI 调用经 `get_session_id()` 都产生**新** session（`identity.py:252`）——两次 `phase1_gate.py` 调用天然落在不同文件，若不显式 `release_claim_by_track` 旧串，旧文件会作为孤儿 active claim 永久残留（直到 24h sweep）。这是本 Spec 新增的组合场景，现有测试（`test_lifecycle_preserves_linked_issue` 等）都没有覆盖「release 旧 track + acquire 新 track 后 `read_claims()` 只剩一条 active」这个整体断言 | 良好，可红且非冗余 |
| SC-16 (探针命中 archive/) | 属实：若实现只 glob `openspec/changes/*/proposal.md`（R1/C2 实证过的原始 bug 形状）会漏 `openspec/archive/` | 良好，可红 |
| SC-17 (无竞品→空+exit 0) | 可红，但「远端无同 issue spec」的场景描述偏向「空世界」；建议明确写成「远端存在其他 spec 但均非同 issue」以强制 fixture 覆盖真正的判别力（否则容易写成假阳性防不住的退化用例） | 可用，措辞建议收紧 |
| SC-18 (fetch 失败→degraded+exit 非 0) | 良好，且与 SC-17 的 exit 0 形成显式对照，是本表里设计最扎实的一组 | 良好 |
| SC-19(a) (不得自命中本轨目录) | 良好，可红：若探针遍历 `openspec/{changes,archive}` 时不排除本轨自己的目录会自举误报 | 良好 |
| SC-19(b) (不得把自己的 claim 计入 overlap) | 见 Finding F4 —— 词汇（claim/track_id/overlap）属于 §2 主机制而非 §4 探针；若指 §2，已被 `test_release_by_track.py:232 test_same_track_not_flagged` 覆盖，非新增 | **有问题** |
| SC-19(c) (超上限 log 披露) | 良好，可红：直接对齐 `handoff_multibranch.py` 的既有 `soft_error()` 披露先例 | 良好 |

---

## Findings

### [MAJOR] F1 — §3「双落点」是本版重写反复强调的核心杠杆，但 SC-1~19 里零覆盖

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:142-150`(§3 正文) 对照 SC 表全段 `:229-261`；Impact 表 `:287-288` 明确列出两个独立文件 `skills/phase-a-planner/SKILL.md` 与 `skills/spec-drafter/SKILL.md`。
- **问题**: spike S6（`.aria/spikes/2026-08-02-S2-S4-S5-S6-batch.md` §S6）用实测数据把「入口覆盖率」钉成本版最大的杠杆（9 种 `owner-container` vs ref 里仅 2 个容器留痕），proposal 正文据此把 §3 双落点列为独立章节，理由是 `spec-drafter/SKILL.md:9` `user-invocable: true` 可绕过 `phase-a-planner` 直接起草。但通读 SC-1~19 全表，**没有一条**提到 `spec-drafter`——SC-9（enabled=false 零调用）、SC-11/12（AskUserQuestion / 必传 `--linked-issue`）全部笼统写「A.1」，未指明覆盖哪个入口，rule6_note 的三条定向 fixture 同样只各建一个，未按入口分叉。
- **该怎么红都红不了的具体场景**: 实现者在 Phase B 只改了 `phase-a-planner/SKILL.md`（这是最容易发生的疏漏——两个文件分属不同 Skill 目录，`spec-drafter` 不是 `phase-a-planner` 的子文件），直接调用 `/spec-drafter` 起草的会话完全不受本 Spec 保护，覆盖率还是停在「2/9」。SC-1~19 无一条会因此变红。
- **佐证——本仓已有解决同类问题的现成先例，且本 Spec 没有照抄**: `aria/skills/state-scanner/tests/test_coordination_default_lockin.py:test_phase_b_require_claim_present`（:39-42）逐字断言 **两个** 入口文件（`phase-b-developer/SKILL.md` 与 `branch-manager/SKILL.md`）都含 `"B.0 - REQUIRE claim"` / `"REQUIRE claim"` 字样——这正是「Phase B 双落点」当年的机械兜底写法。本 Spec §3 明确以「与 Phase B 对称」为动机（原文 :146「与 Phase B 对称 (后者有 phase-b-developer + branch-manager 两处)」），却没有把这条已验证有效的检验模式搬过来用在 Phase A 的两个入口上。
- **危害**: 本版重写用一整节篇幅（含专门的 spike S6）论证「入口覆盖率是真正的杠杆」，如果这条杠杆本身没有机械兜底，第五版可能不会重踏 track-id/heartbeat 的坑，却会在「只改了一半入口」上留下新的、本可预防的盲区——而且这个盲区恰恰是本 Spec 存在理由的同构复现（当初就是「认领点覆盖不到实际发生问题的入口」）。
- **建议修法**（与危害方向一致）: 比照 `test_phase_b_require_claim_present` 的写法，在 Impact 表新增/扩展一条 state-scanner 测试，断言 `phase-a-planner/SKILL.md` **与** `spec-drafter/SKILL.md` 都含 A.1 认领步骤的标志字符串；rule6_note 的三条行为 fixture 至少应有一条明确经由 `/spec-drafter` 直接触发的分支（而非默认都走 `/phase-a-planner`）。
- **自检**: 危害描述是「双落点其一被漏实现不会被任何 SC 捕获」，修法方向是「补一条覆盖双落点的机械断言 + 至少一条经 spec-drafter 路径的行为 fixture」——方向一致。

### [MAJOR] F2 — SC-9 / SC-14 标『代码』，实测对象是 SKILL.md 散文；本仓已有先例证明这类断言会退化为文本存在性检查

- **位置**: `proposal.md:246`(SC-9)、`:256`(SC-14)；对照 Impact 表 `:287`「`skills/phase-a-planner/SKILL.md` | … `coordination.enabled` skip」——该行为**唯一**落点是一份 Markdown 文件，`phase1_gate.py` 本身不读 config（proposal 原文 `:139` 自陈）。
- **问题**: 「代码」这个标签在验证面分层表（`:222-227`）里的含义是「✅ 可机械断言」，对应宿主是 `state-scanner/tests/`。但 SC-9 要验证的「A.1 零调用，不写 claim，不推远端」这件事，没有任何 Python 函数负责做这个判断——`config-loader` 本身也是一个 `disable-model-invocation: true` 的纯 prose Skill（`config-loader/SKILL.md:1-9`），不是可调用的解析器。本仓对这一类「SKILL.md 里的义务是否存在」的验证，已有实际生产先例：`test_coordination_default_lockin.py::test_phase_b_require_claim_present`（:39-42）就是靠 `assertIn("B.0 - REQUIRE claim", text)` 这种**字符串存在性**断言，而不是跑一次真实 A.1/B.0 观察行为。SC-9 若照此实现，能证明的只是「SKILL.md 里出现过 coordination.enabled 字样」，证明不了「AI 真的没调用」——这正是这份 Spec 自己在 §Why 引用的 `feedback_completion_signals_vs_runtime_invocation`（勾选/单测 ≠ 代码真被生产调用）在自己身上的复现。
- **SC-14 是同一病灶的另一种呈现，且更明确地"零信息量"**: `release_gate.py --status abandoned` 是**已经存在、已经测试**的能力——`test_release_by_track.py:138 test_release_abandoned_roundtrips`（docstring 自称 "C-1 regression lock"）用任意 track_id 完整验证了这条链路，与本 Spec 毫无关系、早于本 Spec 就通过。如果 SC-14 被实现为「调 `release_gate.py --status abandoned`，断言状态变 abandoned」，这个测试在**本 Spec 一行代码都不改**的情况下就已经是绿的——它不可能因为 SKILL.md 忘了写"探索性放弃时必须调用"这条新义务而变红，因为它测的不是这条新义务，测的是早就工作正常的旧机制。「答不出'它怎么会红'」在这里精确成立：唯一能让它变红的动作（不写这条 SKILL.md 义务）根本碰不到这个测试的断言路径。
- **危害**: 两条 SC 挂在「代码」verdict 下会给 A.2/A.3 的实现者和后续审计一个错觉——「这条已经有机械兜底了」，实际上兜底要么落空（SC-9 若真做会退化成弱检查）要么恒真（SC-14）。这与 SC-11/SC-12 形成不一致的自我标准：同样是「AI 是否记得做某件事」，SC-11/12 诚实标了「行为」并加了「不冒充结构化测试」的免责声明，SC-9/14 却没有。
- **建议修法**: SC-9 与 SC-14 应改标为「行为」类，纳入 rule6_note 的定向 fixture 覆盖范围（当前 rule6_note 第 1 条已经列了 "(a) A.1 起草前必调 phase1_gate"，本质就是 SC-9 的正向义务；建议把 SC-9 的负向义务——enabled=false 时不调用——以及 SC-14 的放弃-释放义务一并并入这三条 fixture 的清单，而不是留在「代码」表里造成虚假覆盖印象）。若坚持要放代码层，至少应诚实标注「本条只能验证 SKILL.md 文本包含特定字符串，不能验证运行时行为」，参照 `test_phase_b_require_claim_present` 的实际能力边界如实描述。
- **自检**: 危害是「代码标签造成机械兜底的错觉，实际或退化或恒真」，修法方向是「改标为行为类纳入既有 fixture 计划，或如实降级描述能力边界」——方向一致。

### [MAJOR] F3 — SC-8 / SC-10 把「CLI 可验证的结构字段」与「消费层措辞」捆在同一条断言里，后者 CLI 层不产出

- **位置**: `proposal.md:245`(SC-8「措辞按 status 分档」)、`:247`(SC-10「消费面渲染『未能核实』而非『无碰撞』」)；对照 `phase1_gate.py:1239` `print(json.dumps(out, ensure_ascii=False, indent=2))`——CLI 出口只有一行 `json.dumps`，没有任何生成人类可读文案的代码。
- **问题**: `linked_issue_overlaps()` 返回的每条 dict 只有 `{"track_id","owner","container","session","status","linked_issue","claimed_at"}`（`collision.py:203-205`），`status` 字段本身就是原始枚举值（`"done"`/`"abandoned"`/`"yielded"`），不存在"按 status 分档的措辞"这个中间产物——那是消费者（AI 读 JSON 后自己怎么讲）的事，跟本 Spec 极力主张的"断言层必须是 CLI 全链路"（`:135` 原文）恰恰相反：CLI 层根本没有能力产出"措辞"，只能验证到"字段值不同"。SC-10 同理，`GateResult.error` 是一个 token（`fetch_degraded`），"消费面渲染'未能核实'"是同样的下游散文问题。
- **反讽点**: proposal 用相当篇幅（`:135`「SC 的断言层必须是 CLI 全链路，不是直调库函数」）批评"只测库函数"的旧做法会在"参数没接到 CLI"的实现上误判为绿，这个论证本身完全正确、且已有直接先例支持其可执行性（见下）；但同一批 SC 里又把"CLI 测不到的东西"（渲染文案）反向塞回同一条断言，方向相反的两种错误出现在同一份文档里。
- **佐证 SC-8 核心诉求（可见性）确实可以用 CLI 全链路验证，且本仓已有现成模板**（回答任务里"SC-8 可执行吗"）：`test_release_by_track.py:527-576 class TestPhase1GateLinkedIssueCli` 已经在用 `subprocess.run([sys.executable, str(self._GATE), ...])` 起真实子进程调 `phase1_gate.py`、解析 stdout JSON、断言 `linked_issue_overlap` 字段内容——docstring 原话「review I4: B1 CLI 端到端…lib 层测试锁不住 kwarg 穿线拼写错」，和本 Spec §2.4 给 SC-8 的理由逐字同构。`--include-terminal` 完全可以照这个模板直接扩展一个新用例，这部分是本 Spec 最扎实、最有先例支撑的一条。
- **危害**: 把"可 CLI 验证的字段值"与"不可 CLI 验证的措辞"捆在一条 SC 里，会让实现者/审计者在见到"CLI 全链路测试通过"时误以为整条 SC（含措辞分档）都已验证，而实际上措辞那一半从未被这套断言碰到过，只能靠人工读 SKILL.md 或另开行为 fixture。
- **建议修法**: 把 SC-8 拆成两条——(a) 代码/CLI：done/abandoned/yielded 三态的原始记录经 `--include-terminal` 后出现在 CLI JSON 输出里（字段值层面，可用 `TestPhase1GateLinkedIssueCli` 模板落地）；(b) 行为：AI 读到不同 status 后测度wording differentiation，纳入 rule6_note fixture。SC-10 同理拆分 `error` 字段（代码/CLI）与"未能核实"措辞（行为）。
- **自检**: 危害是"捆绑断言造成虚假的全覆盖印象"，修法是"拆分成代码半+行为半分别归位"——方向一致。

### [MAJOR] F4 — SC-13 的被测对象大概率是通用 custom-check runner，而非该 check 自己的字段解析逻辑

- **位置**: `proposal.md:255`(SC-13)；Impact 表 `:293` 只列 `.aria/state-checks.yaml`，未列任何新 Python 脚本；对照 `.aria/state-checks.yaml` 现有两种写法：`issue-cache-freshness`（`command:` 调用独立脚本 `issue_cache_freshness_probe.py`，该脚本另有专属测试 `test_issue_cache_freshness.py`）vs `silknode-contract-deferral-expiry`（`command:` 是内嵌 bash/date 脚本，**没有**专属测试文件）。
- **问题（回答任务里"被测对象是 check 本身还是判定结果"）**: `custom_checks.py` 的既有测试 `test_custom_checks.py`（`class TestCollectorExecution` / `TestSkipStatus` 等）验证的是**通用 runner 机制**——YAML 解析、`command:` 执行、exit code → severity 的映射、`##SKIP##` 标记识别——用的都是测试里现造的任意 command 字符串，不涉及任何一条真实 check 的业务逻辑。既有两条 check 里，只有走"独立脚本"模式的 `issue-cache-freshness` 才有针对该 check 自身解析逻辑的测试；走"内嵌 bash"模式的 `silknode-contract-deferral-expiry` 至今没有专属单测。Impact 表只提 `.aria/state-checks.yaml` 一个文件，意味着最可能复用后一种模式——一条内嵌 grep/sed 的 bash 命令，用 shell 重新实现前置 Spec (`linked-issue-normalization`) 已经在 Python 里精确定义好的 `<org>/<repo>#<n>` 解析规则（剥空白、按最后一个 `#` 拆分、int 校验、"无"哨兵）。这是同一套解析逻辑的第二份实现，语言换成 shell，且没有任何测试宿主去验证这份 shell 实现是否与 Python 版本行为一致（尤其是空白/引号/中文全角 `＃` 这类 shell 正则容易踩的边界）。
- **危害**: SC-13 若照当前 Impact 表的范围落地，"结构化测试覆盖 SC-13"这句话最终验证的可能只是"YAML 格式对、exit code 映射对"，而不是"这条 check 真的正确识别了无字段/不可解析值/显式'无'三种情况"——与 SC-9/SC-14（F2）是同一种"标签与实测对象不一致"问题的第三个实例，只是载体从 SKILL.md 换成了 bash。
- **建议修法**: 参照 `issue-cache-freshness` 的模式，把字段校验逻辑写成独立、可被 Python 单测直接调用的脚本（如 `linked_issue_field_probe.py`），`state-checks.yaml` 的 `command:` 只做"调脚本 + 传参"的胶水，测试落在脚本本身而非 YAML 胶水层；如果坚持内嵌 bash，至少应在 tasks 里显式要求为该 bash 片段编写一组 shell 级测试（fixture proposal 文件 + 断言 exit code/输出），而不是让它隐入"YAML 格式对不对"的通用覆盖里。
- **自检**: 危害是"测试可能只覆盖通用胶水层，不覆盖本 check 的判定逻辑"，修法是"改用已验证有专属测试模式的独立脚本路径，或补一层 shell 级专属测试"——方向一致。

### [MINOR] F5 — SC-19(b) 与其宿主机制（§4 探针）词汇错配，且若按 §2 主机制理解则与既有测试重复

- **位置**: `proposal.md:261`(SC-19)，紧接 SC-16~18（均属 §4 `sibling_spec_probe.py`）之后；对照 `test_release_by_track.py:232 test_same_track_not_flagged`。
- **问题（回答任务里"三条反向对照够不够"）**: SC-19 标题「反向对照三条」出现在"字段可得性/生命周期/探针"这个分组表里，紧跟 SC-16~18（探针）之后，语境指向 §4。但 (b) 「不得把自己的 claim (同 track_id) 计入 overlap」用的是 `claim`/`track_id`/`overlap` 这套词汇——这是 §2 主机制（`linked_issue_overlaps`, ClaimRecord）的概念体系。§4 探针扫描的是 `openspec/{changes,archive}/*/proposal.md` **文件**，比对的是文件里的"关联 Issue"字段，全文没有 `track_id`/`claim` 的概念。两种读法都有问题：若 (b) 真指 §4，探针没有 track_id 可比，这条断言无对象可测；若 (b) 实指 §2，它与现有测试 `test_same_track_not_flagged`（`claims=[self._claim("mine","cB",linked="A#7")]`; 断言 `linked_issue_overlaps(claims,"mine","A#7") == []`）完全重复——那条测试早已存在且通过，不因本 Spec 而变化。
- **危害**: "三条反向对照"这个说法给读者的印象是探针有三个独立方向的负控制，实际只有 (a)（自命中排除）与 (c)（超限披露）是探针的新增覆盖；(b) 要么无宿主可测，要么是旧测试的重复计数——探针实际只有两条新的反向对照，"三条"存在虚报。
- **建议修法**: 把 (b) 从 SC-19 里移除或改写为探针语境下真正有意义的负控制（例如："探针不得把候选文件自己的 `linked_issue` 字段值和自身重复比较产生自匹配"，或者补一条探针专属的"存在其他 spec 但 linked_issue 不同 ⇒ 不命中"的判别力用例），避免用主机制的词汇给探针记账。
- **自检**: 危害是"三条对照实报两条，读者会高估探针的负控制覆盖"，修法是"换成探针语境下真正新增的判别力用例或移除重复项"——方向一致。

### [MINOR] F6 — SC-13~19 整表缺失「怎么会红」列，恰是本版最新、最少被审过的内容

- **位置**: `proposal.md:251-261`（SC-13~19 表头只有 `SC / 场景 / 期望` 三列），对照 SC-1~12 表（`:229-249`）均有第四列「怎么会红」；对照文末「闸门待裁」`:325`「§1 (字段可得性) 是全新章节，以及 §2.1/§2.2 的具体条款措辞，从未经任何席位审过」。
- **问题**: 覆盖 §1（字段可得性）/ §4（探针）/ §5（生命周期）的这七条 SC，恰恰是proposal自己承认"从未经任何席位审过"的部分，按理最需要作者自己先做一遍"它怎么会红"的自检来提高下一轮审计的起点质量——但实际是这七条里唯一有自检的是本次审计（Part 2）补的，原文一条没写。这不是文档格式问题：SC-1~12 每条都有的"怎么会红"栏位起到了"作者先假设自己错了再验证"的作用（这正是本 Spec 全文反复强调的方法论），唯独对最新内容缺席，方向上和"新内容该获得更多审慎"相反。
- **危害**: 下一轮审计席位如果依赖 proposal 自身的"怎么会红"栏位来判断 SC 质量（如同本次审计对 SC-1~12 所做的），会对 SC-13~19 缺乏审查抓手，容易被表面的"有 SC 编号"带过。
- **建议修法**: 补齐 SC-13~19 的「怎么会红」列（本报告 Part 2 已提供草稿，可直接采纳/校订）。
- **自检**: 危害是"新内容审查抓手不足"，修法是"补齐缺失列"——方向一致，此项影响面小，定为 MINOR。

### [MINOR] F7 — SC-11/SC-12「双臂可分辨」标注诚实但底层假设未经 spike 验证，与本版其余不确定性的处理标准不一致

- **位置**: `proposal.md:248-249`(SC-11/SC-12)；对照 rule6_note `:211-216` 第 2 条「建可证伪定向 fixture」；对照 `.aria/spikes/2026-08-02-*` 三份文档，heartbeat（S1）/track-id（S3）/fetch 代价（S2）均在写入 Spec 正文前完成了可执行性 spike。
- **问题（回答任务里"标注诚实吗，双臂真的可分辨吗"）**: 标注本身诚实——SC-11/12 明确写「只能由 eval 覆盖，不冒充结构化测试」，没有像 F2/F3 那样把行为断言包装成代码断言。但"双臂须能分辨"这个前提（AB harness 能否从 transcript 里可靠区分"调用了 AskUserQuestion 再继续"与"渲染一行后自行继续"；能否可靠区分"实际 Bash 调用带了 `--linked-issue`"与"没带"）本身是一条经验假设，本版对其余同等重要的不确定性（heartbeat 是否可行、track-id 该怎么派生、探针 fetch 代价多大）全部先花一轮 spike 验证再写进正文，唯独这条"eval 能不能分辨"的假设没有被同等对待——直接断言"应可分辨"就写进了 SC 表。
- **危害**: 如果 Phase A.2 建 fixture 时才发现这套判别力做不到本项目现有 AB harness 的粒度（例如 harness 只判断最终产物而非过程中的工具调用顺序），SC-11/SC-12 会退回到"标了行为但实际也测不到"的状态——与本版极力想避免的"承诺了验证但验证面不存在"（本版 §闭环论证的核心）同构。
- **建议修法**: 建议在 A.2 之前用与 S1/S2/S3 同等规格补一次轻量 spike——找现有 AB harness 跑一个最小可控场景（如故意让一个 fixture 的 AI 在 overlap 非空时"渲染一行后继续"），确认 harness 确实能从记录里分辨出这个失败模式，而不是先写进 Spec 再等 A.2 实现时才发现测不出来。
- **自检**: 危害是"判别力假设未验证，可能在 A.2 才发现测不到"，修法是"补一次轻量 spike 验证 harness 判别力"——方向一致，因为其余三个不确定性都已被同等规格的 spike 处理过，此项定为提醒性质的 MINOR。

### [MINOR] F8 — SC-4 的「被推翻版本」框架和 D6「接手=两步人工」的措辞安全阀均缺专属校验

- **位置**: `proposal.md:236`(SC-4 标题行「四个被推翻版本的红窗」) 对照该行实际内容（R3 指出的规格空白，非曾经实现又撤销的版本，见 Part 1 表内说明）；`proposal.md:118-123`(§2.3 D6 相关正文, "两步人工"措辞要求) 与 `.aria/spikes/2026-08-02-S3-track-id-derivation.md §4`（"接手"不是一键动作的完整论证）对照 SC-11（`:248`）——只测"是否经 AskUserQuestion 请裁"，未测选项文案是否确实写成"两步人工"而非暗示一键接管。
- **问题**: 两处都是"论证很扎实但没有配对应 SC"的轻微不对称。SC-4 的标题略夸大了它钉住的东西的性质（空白 vs 版本），不影响可证伪性；D6 的"措辞即定义，避免实现者以为有一键路径"是 spike S3 §4 专门用一整节论证的安全阀，但 AskUserQuestion 的选项文案具体写法没有被任何 SC 钉住，若实现者偷懒把选项写成"接手"两个字（丢掉"两步人工"限定），现有 SC 不会检测到。
- **建议修法**: SC-4 标题改为"钉住一处未定案的规格空白"而非归入"被推翻版本"框架；SC-11 补一句"AskUserQuestion 的『并轨/接手』选项文案必须包含'两步'/'释放对方'字样，不得单独出现可被理解为一键的措辞"。
- **自检**: 均为文档精度/覆盖细节问题，不改变已识别的机制风险，定为 MINOR 供 A.2 顺手处理。

---

## 与既有轮次的关系

本轮没有发现任何一条会让 SC-1~4（即 track-id 派生本体）失效的问题——三轮 post_spec + 三个 spike 花的力气在这条主线上是扎实的。本轮发现的问题集中在**验证面自己的可信度**：几条被标"代码"的 SC 经查实际验证对象是 SKILL.md 散文或已有的旧机制,一条被反复强调为"本版结构核心"的双落点设计完全没有 SC 兜底。这些问题不影响"是否可以进 A.2"的机制层判断，但会影响 A.2/A.3 实现者对"哪些义务已经有安全网、哪些还是纯靠自觉"的准确认知——而这份认知偏差正是本 Spec 自己开篇讲的"起草者知道规则也做不到"的同一种病灶，只是换成了"审计者以为有测试，实际没有"的镜像形式。
