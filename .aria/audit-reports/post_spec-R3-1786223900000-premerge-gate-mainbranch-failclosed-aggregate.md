---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T20:38:20.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_spec R3 汇总 — premerge-gate-mainbranch-failclosed

## 投票

| 席位 | VOTE | VERDICT | 原始 C+M+m | 减法引入 | 砍过头 |
|---|---|---|---|---|---|
| tech-lead | REVISE | FAIL | 2+6+5 = 13 | 11/13 | 3 |
| code-reviewer | REVISE | FAIL | 1+7+6 = 14 | 14/14 | 5 |
| knowledge-manager | REVISE | FAIL | 1+3+1 = 5 | 5/5 | 1 |
| qa-engineer | REVISE | FAIL | 1+1+2 = 4 | 4/4 | 1 |
| **backend-architect** | **PASS** | PASS_WITH_WARNINGS | 0+3+2 = 5 | 2/5 | 0 |

**4 REVISE / 1 PASS** · 聚合 verdict **FAIL** · `converged: false` · 零 spawn 失败 ⇒ `incomplete: false`。

## 三轮走势

| 轮 | Critical | Major | Minor | 合计 | 投票 |
|---|---|---|---|---|---|
| R1 | 5 | 10 | 6 | 21 | 5/5 REVISE |
| R2 | 3 | **15 ↑** | 8 | 26 | 5/5 REVISE |
| R3 | 3 | **10 ↓** | 9 | 22 | **4 REVISE / 1 PASS** |

- **Major 由升转降** (15 → 10), `stop-adding-rounds` 判据本轮**不点亮**;
- **首张 PASS 票**出现;
- 但 **`cut_too_much` = 9/22 (41%), 3 条 Critical 里 2 条属之** —— 这是本轮专设字段, 它给出了本轮真正的答案。

## 本轮结论: 减法砍掉了承重件, 且三个版本都打错了层

**TC1 (2 席 + 编排层实跑复现) 是本次审计最重要的产出**:

```
SKILL.md 提到 pre_merge_gate.py 只有 :262 一处 —— 「Helper 实现: ...」, 从无带参调用示范。
而 C.2.4 步骤 1-5 是逐条裸命令, 步骤 3 逐字:
    aether ci status --branch main --in-flight --json
编排层实跑占位符版本:
    $ aether ci status --branch '<main-branch>' --in-flight --json
    {"status":"ok",...,"runs":[]}   RC=0        <- 同一个假绿
```

⇒ `required=True` 守的是一条 **AI 从不被指示去走的路**; 把 `:243` 的 `main` 换成占位符也只是换一个不存在的分支名。

| 症状 | Rule #8 那条腿恒绿 |
|---|---|
| 病因 (a) | helper 缺省 `main` — **#137 报的是它, 三个版本全都只治它** |
| 病因 (b) | `SKILL.md:243` 裸命令字面量 — AI 照抄时 **helper 根本不参与** |

治 (a) 不关闭 (b)。而 R2-fix 砍掉的**存在性核验**恰是唯一对两条路径都有效的拦截物 —— 它作用在「实际被查询的分支名」上, 与该名字如何得来无关。

## Rule #6: 定档已无争议 — **第二行「照跑 AB, 零裁量」**

三席独立命中, 编排层逐字复核 SOT:

- `standards/conventions/skill-benchmark-exemption.md` 附加约束段: **「`description` 或指令流程变动 ⇒ 一律第二行」** —— **直接管辖条款**, 前两版都绕开它去做实证;
- 同文件 §3 界定第三行专指「**给 spec 作者读的**处方」(authoring), 非运行时指令;
- 「C.2.4 零命中」被 `ab-results/2026-07-31-v1.65.0-122-rule6/eval-2/with_skill/answer.md` 推翻 (答卷逐条执行 C.2.4 含查 main in-flight); 此前 grep 只扫 prompt 未扫答卷;
- 援引 `benchmark.md:173` 属 mis-citation: 其确切条件是 **multi-PR concurrent CI 在 mock 不可测**, 与「命令写哪个分支名」无关;
- SOT:55 强制的 `rule6_note`, 本 change 目录 grep **零命中**。

## R3 去重结论集

### Critical (3)

| ID | key | cat | scope | 席 | 减法引入 | 砍过头 | 复现 | summary |
|---|---|---|---|---|---|---|---|---|
| `2f276d13` | TC1 | architecture | §What Changes 的守护对象 vs SKILL.md C.2.4 实际执行路径 | 2 | 是 | **是** | ✅ | required=True 守的是 SKILL.md 从不指示 AI 走的路: 全文仅 :262 把 helper 当「实现指引」提及, 从无带参调用示范; C.2.4 步骤 1-5 是裸命令, 步骤 3 逐字 `aether ci status --branch main`。占位符逐字执行实测仍 RC=0 runs:[] ⇒ 同一假绿。被砍的存在性核验是唯一对两条路径都有效的拦截物 |
| `5705bfe7` | TC2 | documentation | §Rule #6 处置 | 3 | 是 | **是** | ✅ | 归第三行的三条依据全错: SOT 有直接管辖条款『指令流程变动一律第二行』被遗漏; 『C.2.4 零命中』被 ab-results eval-2 答卷推翻 (答卷逐条执行 C.2.4 含查 main in-flight); 援引 benchmark.md:173 是 mis-citation (它讲 multi-PR concurrent CI 模拟不可行, 非讲命令里写哪个分支名)。另 SOT:55 强制的 rule6_note 缺失 |
| `ecc73641` | TC3 | testing | SC-M4 grep 断言 | 4 | 是 | 否 | ✅ | 两种自然实现都失效: 窄模式 `"main"` 漏 :21 (无引号 docstring) ⇒ 改后 :21 不改照绿=假绿; 宽模式裸词命中 def main()/sys.exit(main()) ⇒ 永不收敛。『机械 grep, 零裁量』不成立; 且 §待R3 里『实测 3/3』用的是未写进 SC 的复合模式 |

### Major (10)

| ID | key | cat | scope | 席 | 减法引入 | 砍过头 | 复现 | summary |
|---|---|---|---|---|---|---|---|---|
| `3c5b12e3` | TM1 | architecture | §非目标 末条「结构上不受影响」 | 3 | 是 | 否 | — | 必填在**调用绑定期**失败, 早于 gate_check 内全部三个早退 (:328 enabled=false / :338 no-backend / :344 precheck); 4 个现绿测试证实早退分支可达性实际改变, 并破坏 SKILL.md:284/:294 的 v1.2.0 兼容承诺 |
| `040b2d7e` | TM2 | architecture | §ship target PATCH | 3 | 是 | 否 | — | CLI 参数由可选改必填 + 函数签名去缺省 = 教科书式破坏性变更 (既有 24 处调用将 TypeError), 与 CLAUDE.md『破坏性变更须 MAJOR』未和解; 减法删掉了旧版 PATCH 的论证却保留结论, 且破坏面反而变大 |
| `2e7e1b33` | TM3 | architecture | §Why 判据 vs D2 vs D4 交叉一致性 | 1 | 是 | **是** | — | 判据中途被换: §Why:31 是『猜错会不会被发现』, §What:51 变成『不会猜错』。D2 把 100% 调用方转成「显式传值」类, 而 D4 恰把守这一类的存在性核验移出 ⇒ 唯一剩下的失效模式无人看守 |
| `ea6a47ee` | TM4 | testing | SC-M1/SC-M3 与 §SC 前言矛盾 | 2 | 是 | 否 | — | 前言称『无 subprocess、无网络、无打桩分歧』, 但走 main(argv) 会经 _load_config_from_file + resolve_ci_backend + precheck 起真子进程; 本机 aether 在 PATH 时 SC-M3 打真网络, 违测试文件 docstring:10『no real aether/gh calls』; 该文件零 CLI 级测试先例 |
| `84ed3e84` | TM5 | testing | §Rule #6 ② 定向 fixture 断言方向 | 1 | 是 | **是** | — | 只断言『产出命令不含字面 main』= fail-OPEN: 实测 `--branch trunk` / `--branch <main-branch>` 均不含 main 却同样返 runs:[] RC=0 判绿。且未要求保留 :242 的『本项目 master』取值来源, 该 fixture 可能设计上不可满足 |
| `7b4eab93` | TM6 | testing | §Rule #6 ② fixture 落点与 schema | 2 | 是 | 否 | — | `ab-suite/fixtures/` 目录不存在 (既有布局是 `ab-suite/<skill>-fixtures/`); 且 ab-suite eval schema 只有 {id,name,prompt} 无断言位 ⇒ ② 按字面不可执行。双臂快照对照本身可行 (2026-07-31 有先例), 卡点在路径与 schema |
| `a6b47b05` | TM7 | documentation | 审计叙事寄生交付面文档 | 2 | 是 | 否 | — | §审计轨迹 / §待R3重点审 是 append-only 叙事, 与 2026-08-07 owner 对姊妹 Spec 的裁定『审计轨与交付面切开』相反且未说明豁免; 且已自相矛盾 —— :5 称『下一道不是第三个读文档的 agent』而 R3 正在跑 |
| `796dd377` | TM8 | documentation | §风险 blast-radius grep 口径 | 2 | 否 | 否 | — | 限 `aria/` 且限 py/md, 排除 aria-orchestrator 与 sh/json/yaml, 对外部采用方 (Kairos 等) 天然不可见。两席各自跑了更宽版本, 实测当下均零命中故结论对, 但作为 breaking change 的核查处方口径不足; §Impact 无下游协调行 |
| `1fc8f593` | TM9 | documentation | §对 issue #137 原文的订正 | 1 | 是 | **是** | — | 打稻草人: #137 的 (a) 讲的是 not_applicable 设计跳过 PR CI wait (gate_check:378-386 确证成立), Spec 用『分支名错时 (a) 更保守』去否定它, 而 :76 又承认该通路存在。据此在 issue body 打删除线会划掉一条成立的陈述 |
| `7c25c9c9` | TM10 | testing | 存在性核验移出后的覆盖空洞 | 1 | 是 | **是** | — | 『显式传了错误分支名』这条路径移出后全仓零测试覆盖 (grep 核实), 与本 Spec 治的缺陷同构仅触发条件不同; Spec 已诚实披露但 follow-up issue 未承诺带上『零覆盖』这一事实 |

### Minor (9)

| ID | key | cat | scope | 席 | 减法引入 | 砍过头 | 复现 | summary |
|---|---|---|---|---|---|---|---|---|
| `dcad96fc` | Tm1 | documentation | pre_merge_gate.py:427 help 文案 | 2 | 是 | 否 | — | help 里 `(default: main)` 未被 §What Changes 钉住; 只删 default 不改文案则 --help 继续显示与必填矛盾的字样, 且该裸词不被 SC-M4 窄模式捕获 |
| `9b17e0cd` | Tm2 | testing | SC-M3 负控检验力 | 2 | 是 | 否 | — | 现有 mock 化测试下接近重言式 (main_branch 只是透传给 mock); 且『行为与现状逐字一致』改后单跑内无 golden 可比, 不可执行, 实际只能退化成正向期望值断言 |
| `cc060584` | Tm3 | documentation | 审计证据链的 artifact 版本 | 1 | 是 | 否 | — | 『387 行砍到 186 行』不可核 — git HEAD 版是 179 行, 本次净 +7; 387 行版从未提交, R1/R2 十份报告全 untracked ⇒ 审计证据链指向 git 里不存在的 artifact 版本 |
| `5f75c0f4` | Tm4 | testing | SC-M5 覆盖面 | 1 | 是 | **是** | — | 只覆盖 4 行同步面中的 3 行 — :242 散文改动无断言腿 (而 §Why 称它是唯一现有约束); 且 :167 行尾『(查 main 是否有 in-flight)』括注两个模式都扫不到 |
| `c88c5219` | Tm5 | documentation | 占位符拼写一致性 | 1 | 是 | **是** | — | 三套拼写并存 (`<name>` / `<main-branch>` / 既有 `<PR_BRANCH>`), 削弱『这是要替换的』可辨识度, 抬高照抄概率 —— 与 TC1 实测后果直接相关 |
| `681249c1` | Tm6 | documentation | §移出面『见下方风险』悬空 | 2 | 是 | **是** | — | (a) 腿 not_applicable 通路那行指向 §风险, 而 §风险通篇未提该通路, 移出理由没有落点 |
| `e12b20f0` | Tm7 | documentation | §非目标 措辞 | 1 | 是 | 否 | — | 『main_branch 仍由调用方显式传入 (与现状同)』的『仍』与现状不符 — 今日 24/24 调用点都不传靠缺省, 那正是要治的病; 把『改后应然』写成了『现状既然』 |
| `21580d37` | Tm8 | documentation | 外溢陈旧面 | 2 | 否 | 否 | — | 缺省移除后 path_coverage.py:19 括注与姊妹 Spec linked-issue-normalization 的 workaround 理由变陈旧, §Impact 未列 (规则 #3); 另 SKILL.md:765 `skip_if in [develop, main]` 是同形硬编码兄弟实例 (机制不同、失败方向相反, 记 follow-up) |
| `72f40ec0` | Tm9 | documentation | §Rule #6 对 :167 的处理 | 1 | 是 | 否 | — | :167 被称与 :243『同性质』但未被 ①②③ 三项义务逐条点名, 是否共用同一 fixture 不明确 |

## 编排层三轮累计自身错误 (留痕)

| # | 错误 | 性质 |
|---|---|---|
| 1 | Rule #6 定档**两次都错且方向相反** | 有 dispositive 成文规则时绕开规则去做实证 |
| 2 | 把席位报对的行号「修正」成错的 (`:59-80` → `:59-88`) | 用了比对方更差的启发式 |
| 3 | `cut -c1-150` 截断致误判 `SKILL.md:242` | 已在流入 Spec 前自我推翻 |
| 4 | 受控实验漏 `git init --bare`, 差点把脚本错误当证据 | 已重跑更正 |
| 5 | SC-M4 声称「实测 3/3」用的是**未写进 SC 的复合 grep 模式** | 自陈与交付物不符 (TC3) |
| 6 | 本报告首次写盘因 cwd 被受控实验带跑而失败, 靠同命令内 `ls` 计数才发现 | 回执不等于落盘 |
| 7 | R1-fix 引入 23 条新缺陷 (Major 100% 新造); R2-fix 砍掉承重件 | 见 R2/R3 汇总 |

## 轮次记录

| 轮 | 席位 | vote | 去重 | Major | 本轮 fix 引入(Major) | cut_too_much | converged |
|---|---|---|---|---|---|---|---|
| R1 | 5 | 5/5 REVISE | 21 | 10 | — | — | false |
| R2 | 5 | 5/5 REVISE | 26 | 15 ↑ | 100% | — | false |
| R3 | 5 | 4 REVISE / 1 PASS | 22 | 10 ↓ | 9/10 | **41%** | false |

**R3 的结论不是「再修一轮」** —— 是本 Spec 三个版本共同的**范围前提**被推翻 (TC1)。处置须 owner 裁定。
