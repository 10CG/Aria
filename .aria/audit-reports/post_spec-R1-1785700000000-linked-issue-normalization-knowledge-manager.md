# post_spec R1 — knowledge-manager (linked-issue-normalization)
**verdict**: REVISE
**scope_ok**: true
**counts**: critical=0 major=2 minor=2

> **方法**: 全部 9 项指定核实点逐条去目标处实测 (`refs/aria/coordination` 临时 fetch + `git grep` / Forgejo API / 三份 aggregated 审计报告原文比对 / CHANGELOG 原文 / commit 原文 / 对当前 `collision.py` 直接跑 SC 场景脚本)。临时 ref `refs/aria/tmp-km-audit` 已用 `git update-ref -d` 删除。零文件改动, 零 commit。

## 指针核实表

| # | 声称 | 位置 | 实测命令 | 结果 | 判定 |
|---|------|------|---------|------|------|
| 1a | A 族 (裸形) ref 中 4 条 | proposal.md:31 | `git fetch origin '+refs/aria/coordination:refs/aria/tmp-km-audit'` → `git grep -h "linked_issue" refs/aria/tmp-km-audit \| sed ...` | 实测 **4** 条 (`aria-plugin#116/#118/#122/#124`) | ✅ 精确匹配 |
| 1b | B 族 (org 限定) ref 中 9 条 | proposal.md:32 | 同上, 按 `10CG/xxx#n` 无空格分类计数 | 实测 **11** 条 (2 条 `claimed_at` 为今日 14:04/16:22, 晚于 R1 审计取样时刻; 13→16 总量增量与「13 条已有记录」历史值吻合) | ⚠️ 数字漂移, 见 Finding m-1 |
| 1c | C 族 (org+空格) ref 中 0 | proposal.md:33 | 同上, 检查是否存在 `#` 前含空格的值 | 实测 **0** 条, 16 条值中无一含空格 | ✅ 精确匹配 |
| 2 | `collision.py:217` 是裸字符串 `!=` | proposal.md:20-24 | `Read aria/skills/state-scanner/lib/collision.py:190-230` | 逐字确认: `if c.linked_issue != own_linked_issue:` | ✅ 精确匹配 |
| 3 | 「已在生产中被调用」— `phase1_gate.py:1232` + `phase-b-developer/SKILL.md:88-93` 构成一条今天在跑的路径 | proposal.md:39 | `Read phase1_gate.py:1200-1247` + `Read phase-b-developer/SKILL.md:75-104` | `:1211-1213` 注释自证「ONE production call site」; `:1232` 确为 `linked_issue_overlaps(...)` 调用; SKILL.md `:88-93` 的 B.0 MUST 步骤给出同一 CLI 命令含 `--linked-issue` | ✅ 两处互证成立 |
| 4a | `10CG/10cg.local` 是真实仓 | proposal.md:60 | `forgejo GET /repos/10CG/10cg.local` | `"full_name":"10CG/10cg.local"`, private=true, 非 fork/mirror | ✅ 属实 |
| 4b | 11 个 open issue | proposal.md:60 | 同上 | `"open_issues_count":11` | ✅ 精确匹配 |
| 4c | handoff 引用过 `10cg.local #20` | proposal.md:60 | `grep -rn "10cg.local" docs/handoff/` | `docs/handoff/2026-07-22-...md` 5 处 + `latest.md` 1 处 + `2026-08-01-...md` 2 处引用 `10cg.local #20` | ✅ 属实 (且引用次数比声称更多) |
| 5 | R1「4 席独立命中」 | proposal.md:145 | `Read post_spec-R1-...-aggregated.md` | C1 簇原文: 「**4 席独立命中** (TL / BA / QA / CR) + 主控实跑复验」 | ✅ 精确匹配 |
| 6 | R2「18 元语料穷举零违例 / 撤销传递性担忧 / org-basename 极性 / SC-3」 | proposal.md:146 | `Read post_spec-R2-...-aggregated.md` + individual 报告 | 四点均逐字可对应 R2 原文 (聚合报告「经 R2 核实设计对了的部分」1-3 条 + M1/M2) | ✅ 四点均属实, 但见 Finding M-1 (选择性引用) |
| 7 | R3「唯一无缺口的核心项」 | proposal.md:147 | `Read post_spec-R3-...-aggregated.md` | 原文无逐字「评估表」措辞, 但「R3 确认够实现的部分」6 条中仅 §0 归一算法获得**无保留**的「可直接照写, 不需要实现者猜」评价, 其余 5 条均是外围确认/文本更新或带显式例外 (`release-by-track` 虽同样无保留但服务的是另一机制 `M2` 已判仍有缺口) | ✅ 合理复述, 非逐字引用但实质成立 |
| 8a | v1.65.2 `#124` 纯脚本修复走同一判据路径 | proposal.md:94 | `Read aria/CHANGELOG.md:89-109` | 原文: 「**Rule #6**: 零 SKILL.md / 零 description 变更, 内容属判据表第一行「命令」勘正 ⇒ substitute SC 级 baseline-failing 结构化测试」 | ✅ 精确匹配 |
| 8b | owner 裁定 `db2e983` + 先例 `2026-06-19-secret-guard-exfil-coverage-iteration/` | proposal.md:96 | `git show db2e98341aa127e7162669881273a47b5d5b9dd2` + `ls` 该 archive 目录 | commit 存在, 内容属实, 但改的是**另一个 Spec** (`2026-08-02-secret-guard-nomad-var-put-echo/proposal.md`, hook 场景); 先例目录存在且内容 (`Rule #6: deterministic detector skill → ... 不走 AB`) 与 commit message 引用一致 | ✅ 两指针均存在且内容对得上, 但引用的是**程序性原则**(substitute vs「不适用」二选一)而非同一实体场景, 见下方说明 |
| 9 | 文档同步面完整性 | proposal.md:129-135 | `grep -rln linked_issue` 全仓 + 逐文件核查 `layer-l-integration.md` / config-loader / `state-scanner/SKILL.md:176` / 函数 docstring | `layer-l-integration.md` 零命中 (无需同步); config-loader 零命中 (无需同步); `SKILL.md:176` 与 docstring 均描述笼统, 不算「错」但 Impact 表未列 | ⚠️ 部分缺口, 见 Finding m-2 |

**附带核实 (超出 9 项清单, 因排查 rule6_note 时发现有必要验证)**: `rule6_note` 声称「SC-1~6 均在现状代码上可红」。用一次性只读脚本 (未改任何仓库文件) 直接对当前 `collision.py` 跑 6 个 SC 的场景, 见下方 Finding M-2。

---

## Findings

### [MAJOR] M-1 — 「审计资产继承」表选择性引用 R2, 略去了 R2 自己标记为 MAJOR 的「取样口径」发现, 三族格式表因此漏掉 prose 语料最高频的一族

- **位置**: `proposal.md:29-34`(三族格式表) + `proposal.md:146`(审计资产继承表 R2 行) vs `.aria/audit-reports/post_spec-R2-1785660000000-a1-entry-claim-duplicate-work-guard-type-design-analyzer.md:154-177`(M2) 与 `:281-287`(m4)
- **问题**: R2 个人报告的 M2 (MAJOR) 明确指出:「§0 的三族表取自 `refs/aria/coordination`(13 条), 而实际输入语料是 proposal 头部 prose(139 篇)—— 两者不是同一个总体」, 并在 m4(MINOR) 给出具体数据: prose 语料里**最高频**的写法是「裸仓名 + 空格 + `#`」——`Aria #124`(78×)/`aria-plugin #113`(17×)/`aria-plugin #122`(16×), 建议族表补一行「族 D」并标注两个取样面的口径。本 daughter Spec 的「审计资产继承」表只列了 R2 四项贡献 (等价关系验证 / 传递性担忧撤销 / org-basename 极性 / SC-3 区分度), 对这条 MAJOR+MINOR 组合发现**只字未提**——`git grep -n "139\|prose\|取样\|空格\|族D\|D族" proposal.md` 零命中。三族格式表在 daughter Spec 里被原样继承 (仍是「ref 中 N 条」口径), R2 指出的问题原样保留, 却因为「继承表」暗示「R2 已被吸收」而不会被当作待办。
  - **诚实的一面**: R2 自己也说「四步规则本身能正确处理它 (`Aria #124` 经 `left.rstrip()` 与 `Aria#124` 归一到同一 basename), 这不是缺陷」——我用 daughter Spec 的算法描述逐步推演确认这一点属实, 即**不是功能性 bug**。
  - **但仍是缺口**: (a) 没有任何 SC 用具名方式钉住这个「现实中最常见」的形态 (SC-1 的第三项是「org+空格」即 C 族, 不是「裸名+空格」即缺失的 D 族), 与本 Spec 自己在 SC-5/SC-5b 处坚持的「两者的处置不同, SC 须分开钉」原则不一致; (b) daughter Spec 结尾明确写道 post_spec 应检查「**SC 遗漏** / 与母 Spec 的边界是否干净」——这正是一个被自己点名的风险类别命中的实例; (c) 若未来有人「优化」`left.rstrip()`(例如误认为只需处理 C 族的 org 场景, 把 rstrip 移到 org 分支内), 没有任何测试会因此变红, 因为没人把 D 族的正确性钉在测试里。
- **建议修法**: (1) 三族表加一行「D: `aria-plugin #122` (裸仓名+空格) · 来源 proposal prose · R2 实测 139 篇语料中最高频 (78+17+16=111/139)」, 并在表头/脚注注明两个取样面 (ref 13~16 条 vs prose 139 篇) 各自的条数口径, 避免读者误以为输入总体只有 ref 那十几条; (2) 新增一条具名 SC (如 SC-9) 显式钉住「`Aria #124` ≡ `Aria#124`」(裸名+空格 vs 裸名无空格), 使其获得与其它族同等的回归保护; (3)「审计资产继承」表的 R2 行补一句, 明确 M2/m4 的「取样口径」发现**未被吸收**, 是有意搁置 (若判断确实可搁置) 还是遗漏, 别让「已被三轮确认」的措辞暗示不存在的完整性。

### [MAJOR] M-2 — rule6_note 声称「SC-1~6 均在现状代码上可红」不成立: 6 个 SC 里只有 3 个真正在现状代码上失败, 3 个负控/健全性用例本就在现状代码上通过

- **位置**: `proposal.md:94`「与 v1.65.2 (#124 纯脚本修复) 同一判据路径」句后括注「SC-1~6 均在现状代码上可红」 vs 当前 `aria/skills/state-scanner/lib/collision.py`(未改动版本)
- **问题**: 用一次性只读脚本 (仅 `import`, 未写任何仓库文件) 直接调用当前 `linked_issue_overlaps`, 对 SC-1 到 SC-6 的六个场景逐一实测「现状代码是否如预期」:

  | SC | 现状代码结果 | 与期望值比较 | 是否「baseline-red」 |
  |----|------|------|------|
  | SC-1 (三族两两) | 现状不命中 (期望命中) | 不符 | **是** |
  | SC-2 (同 org 同号不同仓, 负控) | 现状不命中 (期望不命中) | 符合 | 否 — 现状已绿 |
  | SC-3 (org 不同, 期望命中) | 现状不命中 (期望命中) | 不符 | **是** |
  | SC-4 (`#007` vs `#7`) | 现状不命中 (期望命中) | 不符 | **是** |
  | SC-5 (截断别名, 负控/已知限) | 现状不命中 (期望不命中) | 符合 | 否 — 现状已绿 |
  | SC-6 (不可解析值, 同串/异串两个子用例) | 同串命中、异串不命中 (期望同) | 符合 | 否 — 现状已绿 |

  即: SC-2 / SC-5 / SC-6 是负控或健全性检查, 现状裸 `!=` 从不误报 (只会漏报) 且从不抛异常, 所以它们在**修复前就已经通过**, 并非「baseline-failing」。只有 SC-1 / SC-3 / SC-4 三条是真正暴露该 bug 的正控。
- **为什么这不是吹毛求疵**: rule6_note 引用的 owner 裁定 `db2e983` 明确要求「substitute 须实证而非声称」, 且 daughter Spec 自己写明「SC-1~6 的 baseline-failing 状态在 Phase B 须实跑留证」——即这条断言目前是**待验证的承诺**, 不是既成事实。我在 post_spec 阶段提前做了这个验证, 发现按字面「SC-1~6 均可红」不成立。如果 Phase B 实现者照抄这句话去「留证」, 要么被迫编造 SC-2/5/6 的「红」证据 (与其负控本质矛盾), 要么发现矛盾后困惑该怎么处理这条已经写死的断言。
- **证据 (可复跑)**: 脚本 `sys.path.insert(0, ".../state-scanner"); from lib.collision import linked_issue_overlaps` 后对 6 组 `(own, other, expect_hit)` 直接调用, 完整输出已在上方核实表与本节表格给出; 未修改任何文件。
- **建议修法**: 把 rule6_note 的措辞改为精确版本, 例如「SC-1/SC-3/SC-4 (含 SC-5b) 在现状代码上可红, 是暴露该 bug 的正控; SC-2/SC-5/SC-6 是负控与健全性检查, 现状已通过, 用于防止过度修复引入新的误报/异常」——这样 Phase B 的「实跑留证」任务有明确、可达成的验收目标, 不会卡在一句无法被诚实满足的断言上。

### [MINOR] m-1 — 三族表「B 族 ref 中 9 条」在审计时点已漂移为 11 条 (ref 为活数据, 引用快照数字未锚定时点)

- **位置**: `proposal.md:32`
- **问题**: 本轮实测时 (`refs/aria/coordination` HEAD = `022619a`, 2026-08-02T16:55:30Z) B 族 (`10CG/xxx#n` 无空格) 共 **11** 条, 而非声称的 9 条。逐条核对 `claimed_at` 字段, 发现其中两条 (`10CG/aria-plugin#125` 于 14:04 / `10CG/Aria#170` 于 16:22) 均创建于**今天**, 时间晚于「存量数据不迁移」一节所引「13 条已有记录」这个历史基线 (4+9=13, 与 R1/R2 审计时的取样口径一致)。即 4+11=15、加 1 条 sentinel(见下)=16, 与「13 条」的差额可由这两条新增记录完全解释——**不是** proposal 编造或算错, 而是 `refs/aria/coordination` 作为活协调数据, 在 Spec 写作与本轮审计之间的几个小时内自然增长。
  - 额外发现: ref 中还有 1 条 `linked_issue: AUDIT-TEST-DO-NOT-USE#0`(track_id 含「delete-me」字样, status=abandoned), 明显是此前某轮审计的自证遗留测试数据, 状态 terminal 不参与匹配, 不影响三族分类, 仅记录在案。
- **建议修法**: 三族表这类引用活 ref 的精确计数, 建议标注取样时的 commit SHA / 时间戳(如「ref @ `<sha>` 实测」), 而非裸写一个会随时间漂移的数字; 或改用「个位数」/「两位数」这类对小幅漂移不敏感的表述,若精确数字本身不是论证的承重点。

### [MINOR] m-2 — Impact 表未列 `linked_issue_overlaps` docstring 与 `state-scanner/SKILL.md:176` 的同步项, 是 D4(b)「不暗示已穷尽核实」的一个可补漏点

- **位置**: `proposal.md:129-135`(Impact 表) vs `aria/skills/state-scanner/lib/collision.py:182-206`(函数 docstring) + `aria/skills/state-scanner/SKILL.md:176`
- **问题**: 全仓 `grep -rl linked_issue` 命中 9 个文件; 逐一核查后, `layer-l-integration.md` 与 config-loader 相关文件**零命中**(确认不需要同步, 排除了任务提示里的两个假线索)。但 `collision.py:182-206` 的 docstring 目前完全不描述比较语义 (只说 "sharing our linked_issue", 未提归一规则、未提 basename 轴的已知限), `state-scanner/SKILL.md:176` 对 `linked_issue_overlap` 的说明也停留在「同 issue 不同 track-id」的字面, 两处都不算错 (归一后「同 issue」这个词仍然成立), 但都是**本次改动直接影响其准确性期望**的「surface 文案」, 而 D4(b) 明确要求「在 surface 文案中不暗示已穷尽核实」。目前 Impact 表只列 `collision.py` 谓词本体 + 测试 + 发版文件, 未把 docstring/SKILL.md 的说明更新纳入变更面。
- **建议修法**: Impact 表加一行, 建议 `linked_issue_overlaps` 的 docstring 补充: 归一规则概述 + 明确写出 basename 轴的已知限 (不做别名归一, 依赖精确 basename 匹配); `SKILL.md:176` 视篇幅可选择性追加半句「(basename 精确匹配, 不做别名归一)」, 使实现细节与用户可见文案对齐, 履行 D4(b) 的承诺而不仅仅停留在 SC-5 的测试断言里。
