---
verdict: REVISE
agent: knowledge-manager
round: R4
critical_count: 1
major_count: 1
minor_count: 1
r3_resolved: 1/2
---

# post_spec R4 — knowledge-manager 视角审计 (max_rounds=4, 最后一轮)

对象: `openspec/changes/secret-guard-per-segment-evaluation/proposal.md` (v4 + 2026-08-08 前提刷新, 工作区未提交改动, 对比基线 `a89d999`)

## 0. 结论先行

**REVISE**。前提刷新本身（验收环境重写 / 转出 7 撤销 / rule6_note dogfood 段）**逐句核实准确，无新增不实声称**——这点是本轮最重要的正面结论。但审计要求重点核的「转出清单 1-8 逐条核 + 编号空洞处置」发现一条**真实存在的自相矛盾**：Task 1.9 与今日刷新后的转出清单状态不一致（Critical-1）。另发现 §Impact 的 ship 同步面清单本身重蹈 Aria#177 诊断的同类缺口（Major-1）。两条均为文本层修法，不涉及分段算法本身，**不需要再开一轮**——建议 owner 直接采纳文中给出的一行改法后 ship，无需 R5。

## 1. 转出清单 1-8 逐条核（本轮重点）

| 项 | 当前状态 | 内联复现命令 | Task 1.9「开转出 1-6」覆盖? |
|---|---|---|---|
| 1 跨段 pattern fail-open | 存活 | `set -o posix; set \| grep foo` 等 | 覆盖 |
| 2 块结构内泄漏 | 存活 | `{ }` / `for…done` / `( )` 三例 | 覆盖 |
| 3 ssh/sh -c 外壳逃逸 | 存活 | `ssh h '...'` | 覆盖 |
| 4 `&`/换行切分记号 | 存活 | `&>` 冲突例 + heredoc 例 | 覆盖 |
| 5 `$()`/反引号/heredoc 欠拦 | 存活 | 反引号例 | 覆盖 |
| 6 `has_filter` 转内建 | **2026-08-04 已撤销**（拉回本 spec 范围, 见 §What.4） | 不需要（本 spec 自己实现） | **仍被「1-6」误含** |
| 7 Aria#172 dogfood 失真 | **2026-08-08 已撤销**（已关闭, 衍生 #178 已开） | 不需要（已有 #172 历史 + #178 衍生票） | 未被「1-6」覆盖（v4 起就是这样, 属巧合正确） |
| 8 fail-safe 判据不封闭残余误报 | 存活（R3-C-2 新增） | `exec >/dev/null; nomad var get x` | **未被「1-6」覆盖** |

**Critical-1**: `openspec/changes/secret-guard-per-segment-evaluation/proposal.md:176` — Task 1.9「开转出 1-6 issue」与转出清单当前状态矛盾。

- **问题**: 若按字面执行 Task 1.9，会为**已撤销**的转出 6（`has_filter` 已拉回本 spec 内实现，Task 1.3b 就是它）开一张多余/自相矛盾的 issue（标题若照抄该行的删除线文本会直接把「~~已拉回~~」这类 markdown 语法带进 issue title，可读性也有问题）；同时会**漏开**转出 8（fail-safe 判据不封闭的残余误报面，R3-C-2 实测出的新已知限制），导致这条本该被追踪的已知缺口无票可查——这正是本 spec 自己在 §转出 标题上标注要杜绝的「R2 knowledge M-2: 不得只引用未提交的审计报告」同类问题的镜像形态（有清单条目、无对应可执行动作）。
- **核实**: `git diff` 显示今日刷新触碰了 Status 行 / §Impact 验收环境段 / 转出 7 / rule6_note dogfood 段 / SC 表头，**唯独没有碰 Task 1.9**（见下方 diff 片段）；而转出 6 的删除线早在 `a89d999`（2026-08-05 提交, `git log --oneline` 仅此一条记录）就已经存在，说明这不是今日刷新引入的新问题，而是 v4 起就存在、三轮 R3 报告均未点名、直到本轮任务简报明确要求「逐条核」才浮出的**存量缺陷**：
  ```
  $ git diff openspec/changes/secret-guard-per-segment-evaluation/proposal.md
  ... (无 Task 1.9 相关 hunk)
  ```
  ```
  $ grep -n "1.9\|开转出" proposal.md
  176:- [ ] 1.9 开转出 1-6 issue; 回填 #170 覆盖率声明; close #128
  ```
- **建议改法**（一行文本改动，无需重新设计）:
  ```
  - [ ] 1.9 开转出 1、2、3、4、5、8 issue（6 已拉回本 spec 范围不开；7 已关闭, 衍生转出见 #178）; 回填 #170 覆盖率声明; close #128
  ```
- 定级 Critical 的理由：这是**同一份文档内部的自相矛盾**（§转出 章节明写 6/7 已撤销的理由，§Tasks 却仍要求为 6 开票、漏 8），按 knowledge-manager 镜头衡量，文档内部一致性的失守是最高优先级问题类别；且若不修就 ship，Phase D.2「开转出 issue」会被机械执行出错误结果，不是纸面瑕疵。

## 2. SOT 回填面 / ship 同步面（对照 Aria#177，不照抄 CLAUDE.md:81）

**Major-1**: `proposal.md:140`「ship 同步面: aria 子模块 3 交付文件 + 5 版本文件 + 主仓 gitlink + VERSION + README badge (i18n B 档)」**遗漏两类版本引用点**，与 Aria#177 诊断的系统性根因**同构复发**（不是抄错 CLAUDE.md:81，是自己新写的清单独立踩进同一个坑）：

- **实测**: `CLAUDE.md:141` 自身含版本行 `版本: 插件 aria-plugin v1.65.5 | 主项目 v1.7.3 | ...`——proposal 的同步面清单完全没提 CLAUDE.md，若 v1.65.6 ship 后不改这一行，CLAUDE.md 会立刻过期，且 #177 已指出现有 custom checks 对此**结构性失明**（不是"暂时没查"，是查不到）。
- **实测**: `README.md:8`（badge）与 `README.md:242`（独立一行 `Plugin Version:   1.65.5 (aria-plugin, 42 Skills + 11 Agents)`）是**两处不同字符串**；三个 i18n README (`README.zh.md` / `README.ja.md` / `README.ko.md`) 各自在 `:10` 与 `:244` 重复此结构。proposal 清单只写「README badge」，未提独立的 `Plugin Version:` 行——四个文件 × 各 1 处 = 4 个引用点游离于清单外。
- 与 CLAUDE.md:141 的 2 处合计，proposal 当前清单遗漏至少 6 个版本引用点（对照 Aria#177 统计的全量 14 点，proposal 只覆盖了约 8 点：aria 子模块 5 文件 + 主仓 gitlink + VERSION + README badge×1，i18n 正文按 B 档口径不算独立引用点）。
- **建议改法**: 在 ship 同步面清单后补一句：「另需同步 `CLAUDE.md:141` 版本行 + `README.md`/i18n README 各自独立的 `Plugin Version:` 行（与 badge 非同一字符串，Aria#177 已诊断此类遗漏为系统性根因，本 spec 不豁免）」。此为 Major 而非 Critical：不影响 hook 本身正确性，是纯粹的发版收尾遗漏，且有 Aria#177 兜底追踪（虽然 #177 指出兜底本身有缺口，但至少留了痕迹）。

## 3. 交叉引用真实性核查表

| 引用 | 存在? | 内容相符? | 核实命令 |
|---|---|---|---|
| `71bdd60` | 是 | 是——`feat(state-checks): plugin-cache-currency 探针 — 检出 Aria #172 两层滞后`, 与 proposal 引用的「机械兜底」描述一致 | `git show 71bdd60 --stat` |
| `Aria#172` | 是, **closed** (2026-08-08T19:02:53Z) | 是——标题「plugin cache 停在 1.63.0」与 proposal「已修复并关闭」一致 | `forgejo GET /repos/10CG/Aria/issues/172` |
| `Aria#178` | 是, open | 是——body 明确是「hook 类 Spec 的 SC 须显式声明测哪份副本」, 引用 #172 建议 3, 与 proposal「衍生转出」描述完全一致 | `forgejo GET /repos/10CG/Aria/issues/178` |
| `aria-plugin#128` | 是, open | 是——标题「secret-guard 判定是整命令字符串扫描」匹配; comment 17512（triage confirmed/critical）与 17545（分隔符更正）均存在 | `forgejo GET /repos/10CG/aria-plugin/issues/128` + `/comments` |
| `aria-plugin#170` | **否**（404） | — | `forgejo GET /repos/10CG/aria-plugin/issues/170` → 404 |
| （实际应为）`Aria#170` | 是, open | 是——标题「aether-build-container T4 push 凭据经 nomad var put 回显泄漏」与 CHANGELOG「Aria #170 第 3 环」/proposal「#170 泄漏形态本身」语义一致 | `forgejo GET /repos/10CG/Aria/issues/170` |
| `5fab5b8` | 是 | 是——`chore(hooks): 移除 .claude/scripts 本地 hook 副本`, 含 `secret-guard.sh 688 行删除`, 与 proposal「不含 .claude/scripts/」一致 | `git show 5fab5b8 --stat` |
| memory `feedback_deterministic_structural_skill_rule6_substitute` | 是 | 是——内容即「deterministic Skill 改动 = structural fixture + unit tests + dogfood, 不跑 /skill-creator AB」, 与 rule6_note 引用一致（memory 本体讨论的是「Skill」非「hook」, 但 substitute 方法论一致, 且有 2026-08-02 姊妹 spec 的 owner 裁定先例佐证该框定扩展到 hook 合理） | `Read` 该 memory 文件 |

**结论**: 6 个「存在」的引用全部内容相符，**无悬空引用**。唯一问题是 **`#170` 全文 4 处（:25 / :138 / :150 / :176）均未标注仓库前缀**——proposal 主题 issue 是 `aria-plugin #128`，读者/AI 若按「未注明视为同仓」的默认习惯解读，会被误导向一个不存在的 `aria-plugin#170`（本轮我自己也先按此假设查了一次并撞见 404，靠 CHANGELOG.md 交叉核实才定位到正确的 `Aria#170`）。这正是系统提示里点名的「跨文档引用一个从未存在的对象」失效模式的**轻量变体**——不是引用不存在的对象，而是引用**可被误判到**不存在对象的裸编号。

**Minor-1**: 建议把 proposal.md 中 4 处裸 `#170` 全部改写为 `Aria#170`（对照 CHANGELOG.md:18/24 已经是这么写的, proposal 自己反而不一致）。非阻塞，纯降低未来误读概率。

## 4. rule6_note 框定核验

判据「hook 非 capability skill」与 CLAUDE.md 不可协商规则 6 的字面范围**一致**：规则 6 标题即「Skill 基准测试必须用 `/skill-creator`」，触发条件全部是 Skill 语言（新增 Skill / 改逻辑 / 改 description / 发版审计），`secret-guard.sh` 无 `SKILL.md`、不参与 `/aria:` 触发，结构上不在规则 6 的适用对象集合内，不是「拿不准」也不是「豁免」，是**从未落入该规则的射程**。

- 与 2026-08-02 归档 spec `secret-guard-nomad-var-put-echo/proposal.md:130` 的 rule6_note 逐句对比：措辞高度一致（"hook 非 capability skill, 无 SKILL.md / 无 description / 不参与 skill 触发, AB 套件的被测对象...与之无交集"），且该归档 spec 明确记录了 owner 2026-08-02 的裁决过程（前一版曾误写成"Rule #6 不适用"被 R4 code-reviewer 纠正为"substitute 框定"）。本 spec 的 rule6_note 正确复用了这个已裁决的框定，未重犯"不适用 vs substitute 二选一"的错误表述。**PASS**。
- substitute 列出的 SC-1/SC-5/SC-6/SC-2/SC-3：核对 §Success Criteria 正文，五条描述与 rule6_note 摘要一致（SC-1 五形态 baseline-failing / SC-5 分段器单元测试数组基数断言 / SC-6 fail-safe 降级族 12 条分支断言 / SC-2 SC-3 迁移回归锁），**真实覆盖**判定机制的核心分支，非空转列举。**PASS**。

## 5. SOT 计数（SC-13 / Tasks 1.7）现值核实

- `standards/conventions/secret-hygiene.md` 现存 3 处 `366`（L23 Path↔Layer 表 / L286 §5.1 测试清单 / L318 §5.4 实证边界段），与 R2/R3 已确认的「三处」一致。
- **实跑** `aria/hooks/tests/secret-guard.test.sh`：`PASS: 366 / 366`，与文档现值**完全一致**，SC-13 断言的前提当前成立、无既存漂移（这与本 spec 反复强调「数字口径需固化」的问题类别不同——那是未来漂移风险，不是当下已漂移）。
- 顺带验证 SC-17 引用的重复用例：`grep -n "FP-fix timeout run-env"` 命中 `:641` 与 `:673` 两处字节级相同，SC-17 的问题描述真实存在（非虚构立靶）。

## 6. 前提刷新段落自身准确性（逐句核）

对 `git diff` 命中的每一处改动逐句核实：

- 「Aria#172 已修复并关闭 (2026-08-08)」→ 核实 closed_at = `2026-08-08T19:02:53Z`，**准确**。
- 「本仓 plugin cache 现为 1.65.5」→ 核实 `/home/dev/.claude/plugins/installed_plugins.json` 中 `aria@10CG-aria-plugin` 的 `installPath` 含 `.../aria/1.65.5`，**准确**。
- 「`cmp` 判定与 canonical 字节相同」→ 实跑 `cmp aria/hooks/secret-guard.sh <cache 同路径>`，exit=0（无差异），**准确**。
- 「机械兜底 = 主仓 `71bdd60` 的 `plugin-cache-currency` state-check」→ 核实该 commit 确实新增该探针且内容与「两层滞后」描述吻合，**准确**。
- 「衍生转出 Aria#178」→ 已在 §3 表格核实内容相符。
- rule6_note dogfood 段「仓内 harness 现跑 1.65.5（与 canonical 字节相同）」→ 与上面 `cmp` 结果一致，**准确**。

**未发现新增不实声称**。这是本轮最值得记一笔的正面结果——一次涉及 6 处文本改动、引用 3 个外部对象（issue/commit）的"前提刷新"，逐句核验零失实，说明作者这次没有重犯本 cycle 前几轮「断言未实测」的模式（参见 proposal 自己 §Why 上方列的 7 条被推翻断言）。

## 7. 留给 R4 的 SC-9 设计问题——本轮裁定

**问题**: SC-9（dogfood）当前仍写「canonical 直调端到端脚本」；#172 解除后，harness hook 链已可信，是否应该把 SC-9 改为经 harness 链验证？

**裁定：SC-9 应新增一条 harness hook 链的验证腿，与 canonical 直调并存（不是替换）。**

理由：

1. **dogfood 存在的意义与其余 SC 不同**。SC-1/SC-2/SC-3/SC-5/SC-6/SC-7 全部测的是 `secret-guard.sh` 这份源码本身的判定逻辑正确性——canonical 直调对它们是唯一正确的验收方式，因为这些 SC 关心的是"代码写对了没有"，与部署形态无关，harness 链反而引入了不必要的环境依赖（plugin 安装态、`CLAUDE_PLUGIN_ROOT` 解析等），会降低可复现性且不提供额外信号。
2. **SC-9 关心的是另一件事：「用户真的会被拦住」**。如果 SC-9 也只做 canonical 直调，它相对 SC-1/SC-3 不提供任何增量证据——两者测的是同一件事（源码判定），SC-9 就沦为 SC-1 的重复劳动。dogfood 这个词本身的方法论含义就是"吃自己的狗粮"，即验证**实际部署路径**，而 #172 事故恰恰证明了"canonical 一直是对的，用户加载的却是错的"这种分裂完全可能发生且发生过 168 小时以上未被察觉。若 SC-9 仍只测 canonical，本 spec 对"用户是否真的被保护"这件事**没有任何一条 SC 提供证据**——这是一个真实的验收空洞，不是理论洁癖。
3. **不构成对"其余 SC 保持 canonical 以求可复现"这一立场的推翻**。SC-9 通常是一次性的人工/半自动验证步骤（不是每次 CI 都要跑的高频回归），可复现性的边际价值在这里远低于 SC-1/SC-2/SC-3 那种高频机械回归场景，因此为 SC-9 单独承担 harness 链的环境依赖是合理的取舍，不需要为了"整体一致"而牺牲它本该验证的对象。

**建议 SC-9 改法**：
```
SC-9 (dogfood): (a) canonical 直调端到端脚本, 覆盖 5 类实际使用形态 [沿用]；
                (b) 新增至少 1 类形态经 harness hook 链实测 (即真实触发 Claude Code
                    PreToolUse, 而非直接调用脚本), 验证"用户在本仓 Bash 工具下确实被拦/放行"，
                    覆盖旗舰泄漏形态 (nomad var put echo, 对应 #170)。
```

**与 Aria#178 的边界**：#178 是**规范层**的通用问题——"所有 hook 类 Spec 今后都应显式声明 SC 测的是哪份副本"，它的解决产物应该是一条 convention 文档或 state-check（长期、跨 spec 适用）。本裁定是**本 spec 单点**的应用——只回答"这一条 SC-9 现在该怎么写"，不替 #178 做出通用规范决定，也不应等 #178 结项才能 ship 本 spec（#178 是慢变量的方法论建设，本 spec 是快变量的具体交付，两者不应互相阻塞）。若 #178 后续订出通用格式（例如要求所有 dogfood 类 SC 统一用某种双腿模板），届时可回头把 SC-9 的措辞对齐，不影响本次 ship。

## 8. R3 遗留 Minor 核销状态

- **R3 Minor-2**（carry-forward 原 R2 m-1）：Aria#172 issue 补「验收基准点选择」跟进 comment——**因 #172 已于今日关闭而 moot**：目标对象已不存在（issue 已结项），且其实质关切（canonical vs harness 该用哪个做基准）已经被更完整地转化为 Aria#178 追踪，视为**已通过等价路径解决**，计入已核销。
- **R3 Minor-1**：`corpus_census.py` 未接入 `state-checks.yaml` 持续复核机制——**仍未解决**，proposal 的 Task 1.1-1.9 依然没有对应项，維持原判：不阻塞，建议 ship 时在 CHANGELOG 或转出里补一句显式标注为有意的范围外决定。

`r3_resolved: 1/2`。

## 9. 复核通过项（未变动部分）

- 模板符合度、Rule #5 落点、§6 数字口径自洽性（65/49/16/15/1 加总）：R3 已核实且今日未改动相关文本，维持 PASS，未重新逐位复算。
- 转出清单 1-5 与 8 的内联复现命令：全部具体可执行，符合 R2 M-2 要求（详见 §1 表格）。

## 结论

CONVERGED 判定：**否，但收尾成本极低**。本轮发现 1 Critical（Task 1.9 与转出清单矛盾，一行文本改法）+ 1 Major（ship 同步面清单遗漏 CLAUDE.md/Plugin Version 行两类引用点，一句文本补充）+ 1 Minor（`#170` 裸编号建议标前缀）。前提刷新本身零失实、交叉引用零悬空、rule6_note 框定成立、SOT 计数当前无漂移——这些是本轮的主要复核对象，全部通过。鉴于 `max_rounds=4` 已是最后一轮且两条阻塞项均为文本层一行/一句改法、不涉及分段算法设计本身，建议 owner 直接采纳本报告 §1/§2 给出的具体改法后收敛 ship，无需再开 R5。
