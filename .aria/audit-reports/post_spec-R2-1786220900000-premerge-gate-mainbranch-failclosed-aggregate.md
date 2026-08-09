---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T19:48:20.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_spec R2 汇总 — premerge-gate-mainbranch-failclosed

> 编排层汇总。五份席位报告见 `post_spec-R2-*-{role}.md`。R1 汇总见 `post_spec-R1-1786216818583-*-aggregate.md`。

## 投票

| 席位 | VOTE | VERDICT | 原始 C+M+m | fix 引入比 |
|---|---|---|---|---|
| tech-lead | REVISE | FAIL | 1+10+4 = 15 | 14/15 (93%) |
| code-reviewer | REVISE | FAIL | 1+8+4 = 13 | 12/13 (92%) |
| backend-architect | REVISE | FAIL | 1+4+2 = 7 | 6/7 (86%) |
| qa-engineer | REVISE | PASS_WITH_WARNINGS | 0+4+1 = 5 | 5/5 (100%) |
| knowledge-manager | REVISE | FAIL | 1+1+1 = 3 | 2/3 (67%) |

5/5 REVISE · 聚合 verdict **FAIL** · 零 spawn 失败/超时 ⇒ `incomplete: false`。

## 收敛判定 (机械)

```
comparison_key = (type, severity, category, scope)
R1 去重 21 条 -> keys 21 个
R2 去重 26 条 -> keys 26 个
两轮共有 key: 0
conclusions_stable: False      unanimous_pass: False      => converged: False
```

> 共有 key = 0 的原因: Spec 四节被整体重写, 绝大多数 scope 字符串本身变了。**这意味着四元组比较在「结构性重写」后不具可比性** —— 它测的是「同一批结论是否稳定」, 而重写换掉了结论的载体。本轮真正的收敛信号来自下节。

## 边际产出拐点 (本轮的关键数据)

| 指标 | R1 | R2 | 判据 |
|---|---|---|---|
| Critical | 5 | **3** | 降 |
| **Major** | 10 | **15** | **升** — `stop-adding-rounds` 判据「major 是否还在降」**不点亮** |
| Minor | 6 | 8 | 升 |
| **Major 中由 R1-fix 引入** | — | **15/15 = 100%** | `marginal-return-negative` 判据「>1/2 即转负」**决定性点亮** |
| 全部 finding 中由 R1-fix 引入 | — | 23/26 = 88% | 同上 |

**⇒ 本轮 fix 消灭 21 条、生产 23 条, 其中 Major 净增 5 条且 100% 是新造的。这个循环当前是负产出。**

**R1 真正漏掉的只有 1 条 Critical** (RC1) —— 即 R1 的审计质量不是问题, 问题在 fix 环节。

## R2 去重结论集

### Critical (3)

| ID | key | cat | scope | 席 | fix引入 | 编排层复现 | summary |
|---|---|---|---|---|---|---|---|
| `db7a5f6b` | RC1 | implementation | proposal.md §5 存在性核验命令 | 3 | 否 | ✅ | ls-remote pattern 是 ref 尾段 glob: 远端只有 refs/heads/wip/master 时 `--heads <r> master` RC=0 判「存在」⇒ 承重核验在其要治的病同一形状上 fail-OPEN。锚定 refs/heads/<name> 实测 RC=2 |
| `2306b232` | RC2 | architecture | proposal.md §3 权威解析路径 | 1 | **是** | ✅ | ls-remote --symref 存在 RC=0 但无 ref: 行的两种实测边界 (unborn remote → 空输出; detached 远端 HEAD → '<sha>\tHEAD')。§3 二元判定不覆盖, 字面实现取不到 name |
| `3b8072d3` | RC3 | documentation | proposal.md §Rule #6 处置 | 2 | **是** | ✅ | 「存在专属 AB 套件」论据证伪: 该套件 0 prompt/0 双臂, 其历史运行记录自证 type=structural_verification 且明文『AB measurement ... not feasible in mock, deferred to dogfood』; phase-c-integrator.json 3 eval 覆盖 C.1/C.2/C.2.5 零触 C.2.4 ⇒ 应落判据表第三行非第二行 |

### Major (15)

| ID | key | cat | scope | 席 | fix引入 | 编排层复现 | summary |
|---|---|---|---|---|---|---|---|
| `2ea6b166` | RM1 | documentation | SC 编号命名空间 | 3 | **是** | ✅ | 新 SC-9/10/11/12 与既有 test_sc9/10/11/12 (#122, 语义完全不同) 重名; 生产注释 pre_merge_gate.py:379 亦引 SC-9/10。同名方法静默覆盖 |
| `bea904a5` | RM2 | testing | SC-10 红窗 | 2 | **是** | — | 打桩写则等于既有 test_sc10 (今天就绿); 不打桩需真 git fixture, 与 §Impact 自己要加强的 test_sc22 卫生守卫冲突。两条路都不成立 |
| `e9f73cdf` | RM3 | testing | SC-11 可观测面 | 3 | **是** | — | 断言的是 SKILL.md:253 给编排 AI 的散文义务, 无代码产出该警告行; Spec 自陈 AB 套件也覆盖不到该 surface ⇒ 双通道无观测面, 恒绿 |
| `4d964f4c` | RM4 | testing | SC-9 红窗 | 1 | **是** | — | 所比较的「in-flight 查询用的 remote」在代码里不存在 (query_branch_in_flight(branch) 不接受 remote, aether 按 cwd 解析), SC-9 恒绿 |
| `1f80903d` | RM5 | testing | SC-8 可实现性 | 2 | **是** | ✅ | 要求测 workflow-runner 的 write_gate_state, 但该模块不在测试 sys.path 上 (实测 ImportError); 且 gate verdict 词表{green,wait,fail} 与 gate_state status 词表{waiting,green,fail} 本就不同; 又与『不改 workflow-runner』非目标矛盾 |
| `e7902032` | RM6 | architecture | proposal.md §8 在场范围表 | 2 | **是** | — | §8 逐字引 SKILL.md:279 的四分支六键契约, 表里只列三条, 漏 backend query 失败分支 (:369-376/:392-399) — 该分支在解析点之后, 按 D-I 会被加键 ⇒ 违反自己引的契约 |
| `586c1e4b` | RM7 | architecture | proposal.md §6 / D-G 重试规范适用面 | 3 | **是** | — | 所引 SKILL.md:259 的确切触发与终止条件都是 timeout, :260 对 exit 1-126 明文『→ fail』不重试; §5/SC-6 却要求确定性非零也重试 3 次 ⇒ 超出规范适用面, 且每次白等 65s 得同一结论 |
| `2721a555` | RM8 | architecture | proposal.md §3 解析顺序 | 1 | **是** | — | 权威路径只在快路径『失败』时触发, 未覆盖『成功但陈旧』(上游默认分支改名 ⇒ 本地 ref 返旧名 ⇒ §5 判 not-found ⇒ 健康仓恒红且 kind 指错方向) |
| `59877fb3` | RM9 | testing | 六键契约的机械守护 | 1 | **是** | — | §8 称『有 _OLD_KEYS 守护测试』『全分支在场则必红』; 实读 _OLD_KEYS 只做逐键值相等与 assertIn 存在性, 无 exhaustive key-set 断言 ⇒ 加新键照绿, 该契约今天零守护 |
| `65b31459` | RM10 | implementation | proposal.md §7 gate_error schema | 1 | **是** | — | §7 钉死 kind/remote/attempted 三键无 message, 而 §5 与承重断言 SC-4 都要求『message 须点明…』; message 未绑定到 raw_message 或 gate_error.message ⇒ 两实现者分叉 |
| `15607a60` | RM11 | architecture | D-B vs D-C 判据对称性 | 1 | **是** | — | D-C 用『健康常态恒红=零信息』否决只用本地 ref; D-B 却给 remote 字面缺省 origin, 在 remote 非 origin 的仓上确定性失败 = 同一个恒红, 且 remote 无任何解析尝试。判据未对称适用 |
| `6915b2ab` | RM12 | documentation | proposal.md §同形状兄弟位置 | 1 | **是** | — | 一错一漏: sync.py 无该形状 (其 _ORIGIN_HEAD_REFS 是子模块 SHA 回落链), 失实说法逐字继承自 fetch_gate.py 注释未去 target 核验; 漏真同形第三处 audit-engine/SKILL.md:389-390 |
| `dec20fbe` | RM13 | documentation | proposal.md §引用卫生 | 1 | **是** | ✅ | 修 M7 的动作自身引入两处悬空引用: 『§3 的零证据不得当正证据』全文仅出现在该句自己里 (§3 无此原句); 『standards/conventions/ 的 fail-CLOSED 原则』该目录 grep 零文件命中。把真实但容器本地的引用换成了哪里都不存在的引用 |
| `aca30b31` | RM14 | implementation | proposal.md §4 _resolve_main_branch 失败信令 | 1 | **是** | — | 『抛/返回 error 输出』未择一, 与 tuple-unpack 赋值语法及相邻 _verify_branch_exists 隐含的仅 raise 约定不一致 |
| `e3ce9ed1` | RM15 | testing | SC 打桩策略一致性 | 1 | **是** | — | SC-3/6/7 明文要求打桩, SC-1/SC-10 未提; SC-1 若走真实 git 依赖 ambient origin/HEAD, 而 aria 仓唯一 CI workflow 用 fetch-depth:1 浅克隆 — 该配置下 origin/HEAD 通常非 symbolic ref, 与 Spec 自己 m6 段点名的风险同形 |

### Minor (8)

| ID | key | cat | scope | 席 | fix引入 | 编排层复现 | summary |
|---|---|---|---|---|---|---|---|
| `88018c7c` | Rm1 | architecture | §7 消费点表完整性 | 1 | **是** | — | 『五个消费点』漏 workflow-runner/SKILL.md:332-336 Exit conditions (fail/green 封闭二分支无 catch-all) 与 :313/:324 wait 触发。结论不变但本节立论方式就是穷举 |
| `1f67e7d0` | Rm2 | architecture | §8 / follow-up (b) 保护面 | 1 | **是** | — | 只保护 main_branch_resolved, 漏同批新增的 gate_error — write_gate_state 与 workflow-state-schema 同样无其位置, fail 时三个 kind 从 audit trail 全丢 |
| `00ce9e01` | Rm3 | testing | §Impact 既有测试小节算术 | 1 | **是** | — | 『其余 23 处会真起子进程』与 §4『解析点在三个早退之后』矛盾 — 三处早退前返回, 上限 21 处 |
| `97d6aa5a` | Rm4 | documentation | 行号/自陈漂移 4 处 | 2 | **是** | ✅ | _ProbeCacheResetMixin 实为 :59-80 (我改成 :59-88 是把对的改错); SC-11 引 SKILL.md:252 应为 :253; §Impact 漏 SKILL.md:270 的 "branch":"main"; R1 吸收记录 C2 行写『§Impact + SC』但无任何 SC 覆盖 |
| `b94a64b2` | Rm5 | documentation | §4 伪代码保真度 | 2 | **是** | — | 实际是 :356 pc=None → :357 条件 → :358 调用, Spec 画成无条件且两处标 :356; path_coverage_enabled=false 时 §4 第二条理由不成立, 未讨论该分支; :344 锚点应为 :345/346 |
| `9e6907af` | Rm6 | documentation | gate verdict 词表 vs gate_state status 词表 | 1 | 否 | ✅ | {green,wait,fail} 与 {waiting,green,fail} 不同一 (wait≠waiting), 说明 workflow-runner 侧本有翻译层; 不破坏 SC-8 但读者易误以为已被本 Spec 钉死 |
| `afcbf970` | Rm7 | testing | SC 负控标注 | 1 | **是** | — | SC-5/5b/6/9/12 实质是负控 (今日代码上即绿, 只有错误实现才转红) 但未像 SC-3/SC-7 那样标注, 易致 Phase B 误判 TDD 红灯预期 |
| `f8731fc1` | Rm8 | documentation | proposal.md:5 Level 判定佐证 | 1 | 否 | — | Level 2 数字核对无误, 但佐证文字『单文件+其测试』在 R1 重写后过时 — 实际 4 文件 + 外部 issue 编辑 + 2 follow-up issue |

## 编排层独立复现 (8 条)

| finding | 复现方法 | 结果 |
|---|---|---|
| RC1 | 受控裸仓: 只推 `refs/heads/wip/master` | `--heads <r> master` **RC=0** 匹配到 `wip/master`; `refs/heads/master` **RC=2** ✅ |
| RC2 | 受控裸仓 ×2 | unborn → RC=0 空输出; detached 远端 HEAD → RC=0 `"<sha>\tHEAD"`, **均无 `ref:` 行** ✅ |
| RC3 | 读套件 JSON + 其历史 ab-results | 0 prompt / 0 双臂; `benchmark.json type=structural_verification`; `benchmark.md:173` 明文 "not feasible in mock, deferred to dogfood" ✅ |
| RM1 | grep 测试方法名 | 既有 `test_sc9/10/11/12/13/15/21/22` ✅ |
| RM5 | 实跑 import | `ImportError: No module named 'gate_state_helper'` ✅; 且 `wait` ≠ `waiting` ✅ |
| RM13 | grep 本文件 + standards/ | 「零证据不得当正证据」全文仅 1 次(在该句自己里); `standards/conventions/` grep `fail-CLOSED` 零文件 ✅ |
| Rm4 | 精确算 class 边界 | mixin 实为 `:59-80`; **编排层此前把对的改成错的** ✅ |
| Rm6 | 读两处常量 | `{green,wait,fail}` vs `{waiting,green,fail}` ✅ |

## 三次同形状复发 (`fix-recurs-in-fallback`)

本 Spec 的主张是「修一个 fail-OPEN」, 而 R1-fix 在三处把同一形状造了回来:

1. **C1 的解法** — 新增 `verdict="error"` 使 fail-OPEN 从消费侧复发 (R1 已抓); 我改用 `gate_error` 后, §7 的立论表又把 `wait`/`waiting` 两个不同词表当成直通链 (R2 抓);
2. **§5 存在性核验** — 裸分支名 pattern 是尾段 glob ⇒ **承重条款自己 fail-OPEN** (R2 RC1);
3. **§3 权威解析路径** — 为治 m6 恒红而新写, 结果引入「RC=0 + 无载荷」不可区分态 —— **正是 §Why 控诉 aether 的那条罪名** (R2 RC2)。

## 编排层自身的错误 (留痕)

1. **Rule #6 建议基于浅核验** — 只核了「套件文件存在 + 7 fixtures」, 未核「它能否测量该行为」; 证据 (`benchmark.md:173`) 就在同目录。owner 据此裁定「照跑 AB」, **该裁定的前提已不成立, 须重裁**。
2. **把对的行号改成错的** — `_ProbeCacheResetMixin` 实为 `:59-80`, 我用「下一个 class 行号」启发式改成 `:59-88`, 而该启发式把中间注释块算了进去。两轮席位都报的是对的。
3. **`cut -c1-150` 截断致误判 `SKILL.md:242`** (已在 R1 前自我推翻, 未流入 Spec)。
4. **一次受控实验脚本写坏** (漏 `git init --bare`) 差点把脚本错误当证据, 已重跑更正。

## 轮次记录

| 轮 | 席位 | vote | 去重 C+M+m | Major 走势 | fix 引入(Major) | converged |
|---|---|---|---|---|---|---|
| R1 | 5 | 5/5 REVISE | 5+10+6 = 21 | — | — | false |
| R2 | 5 | 5/5 REVISE | 3+15+8 = 26 | 10 → **15 ↑** | **100%** | false |

**下一步不是 R3。** 两条成文判据 (major 是否还在降 / fix 引入占比是否过半) **同时点亮**, 且方向一致。处置须由 owner 裁定, 决策单随附。
