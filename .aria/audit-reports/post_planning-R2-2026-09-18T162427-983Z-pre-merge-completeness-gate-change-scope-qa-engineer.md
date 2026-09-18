---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-18T17:07:37.659Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md`(全文, 225 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml`(全文, 1613 行, 分段读取)
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md`(节选: `## Tasks` `:407-452`; `## Success Criteria` 全部 SC-1~SC-22 表格行 `:457-478`; `## rule6_note` `:480-487`; `## 待 owner 复议` 全文 `:488-558`)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md`(全文, 116 行)
- `CLAUDE.md`(「多远程推送」段与不可协商规则 #3/#6/#8/#10, 经 system prompt 全文可见)
- `aria/skills/audit-engine/tests/test_sibling_spec_probe.py:295-339`(两条既有守卫 `TestNoPytestImport` / `TestRunAllTestsDiscovery`)
- `aria/skills/run_all_tests.sh`(全文, 108 行, 含 `is_pytest_suite()` `:41-46`)
- `aria/skills/state-scanner/scripts/lib/spec_complete.py:508-575`(`extract_claim_symbols`)、`:725-754`(`_is_hooks_or_config_path` 等路径判据)、`:1033-1082`(`classify_symbol_liveness`)
- `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py:260-270`
- `aria/skills/state-scanner/lib/failure_handlers.py`(grep 确认 `no_push_requested_by_env` 定义于 `:95`)
- `aria-plugin-benchmarks/ab-suite/audit-engine.json`、`aria-plugin-benchmarks/ab-suite/version.yaml`(核对当前基线值)
- 实跑核验(均在自建 scratch 副本 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/audit-R2-qa-engineer/repo` 或真仓内只读命令完成, 无写操作): `git merge-base --is-ancestor` / `git diff --shortstat`(核验行号冻结与零 diff声称)、`git worktree add/remove`(核验 rc=128 声称)、`python3 -c` 一致性脚本(依赖图/工时求和/agent 计数)、`no_push_requested_by_env` 三态探针、`test_pre_merge_gate` 三条 catalog 命令 + 坏 node id

## Findings

| id | severity | type | category | scope | 摘要 |
|---|---|---|---|---|---|
| 7a0fc162 | minor | issue | testing | detailed-tasks.yaml `metadata.sc12_liveness.guard_config_hooks`(消费方 TASK-021/TASK-031) | `guard_config_hooks` 的 shell grep 口径比它要防护的 Python 分类器更窄, 存在未记录的盲区 |
| 1c3a64a2 | minor | issue | documentation | detailed-tasks.yaml TASK-018 | TASK-018 的 title 未列全其 verification 实际核验的 N3/N4/N7/N8/crlf_guard |

### m1 · 7a0fc162 · guard_config_hooks 的口径比它防护的分类器更窄

- **证据**: `spec_complete.py:733-744` `_is_hooks_or_config_path`:
  ```
  def _is_hooks_or_config_path(rel_path: str) -> bool:
      name = Path(rel_path).name
      norm = "/" + rel_path.replace("\\", "/")
      if name == "hooks.json":
          return True
      return name == "config.json" and "/.aria/" in norm
  ```
  只要求 `basename == "config.json"` 且路径中**任意位置**含 `/.aria/` 子串; 而 yaml `sc12_liveness.guard_config_hooks` 给的 shell 判据是
  `git grep --recurse-submodules -l -F completeness_gate | grep -E '(^|/)(hooks\.json|\.aria/config\.json)$'`,
  要求路径**尾部逐字**是 `.aria/config.json`(即 `.aria` 必须是 `config.json` 的直接父目录)。我实测两者对同一样例路径判定不同:
  ```
  $ python3 -c "
  import re
  p = 'foo/.aria/bar/config.json'
  name = p.rsplit('/',1)[-1]
  norm = '/' + p
  print('python 分类器:', name=='config.json' and '/.aria/' in norm)   # True
  print('guard 等价 grep:', bool(re.search(r'(^|/)(hooks\.json|\.aria/config\.json)\$', p)))  # False
  "
  python 分类器: True
  guard 等价 grep: False
  ```
  当前仓内真实存在的 `config.json` 都在 `.aria/config.json` 这一浅层形态 (`find . -name config.json -path '*.aria*'` 只返回 `./.aria/config.json` 与 `./aria-orchestrator/.aria/config.json`), 均落在 guard 的窄口径内, 故今天两侧结论一致, 该差异当前不触发。
- **失败场景**: 若在本 spec 执行期间(或并发轨)新增一个 basename 为 `config.json` 但父目录不是字面 `.aria`(如某处 `.aria/<sub>/config.json`)的文件, 且其中提及字面串 `completeness_gate`(哪怕只是注释或说明文字), TASK-021 / TASK-031 执行者按计划先跑 `guard_config_hooks` 得到「无输出」, 会把这当作「L2 未被配置文件污染」的确认继续往下走; 但若这份新文件真的存在, `classify_symbol_liveness` 仍可能把它归入 `aria_plugin_integration` 类别, 使 L2 被这份未被 guard 捕捉到的文件带绿, 而执行者因为 guard「无输出」不会再复核这一点。`sc12_liveness.blind_spots` 已记录了另外两类盲区(脚本缺失时的 `ambiguous` / `generic_path_call`), 但没有记录这一条。
- **它怎么会红**: 基线(当前仓) = guard 与分类器结论一致, 都不判 aria_plugin_integration; 目标(3.2 行 + 真实脚本 + SKILL.md fenced bash) = 两者一致地判 alive/aria_plugin_integration, 不依赖这条差异; 坏实现(如上例的嵌套 `config.json`) = 分类器判 True(可能虚增 alive_categories), guard 判 False(无输出, 放行), 二者出现分歧, 而计划把 guard「无输出」当作可以信任 L2 的前提, 这条分歧不会被现有任务发现。
- **建议修法**: 把 guard 的 grep 口径改宽到与 `_is_hooks_or_config_path` 一致, 例如 `grep -E '(^|/)hooks\.json$|/\.aria/.*config\.json$'`, 或者干脆用 `python3 -B -c` 直接调用 `_is_hooks_or_config_path` 本身做判定而不是另写一条平行的 shell 正则; 顺手把这条差异补进 `blind_spots`。

### m2 · 1c3a64a2 · TASK-018 title 未列全实际核验范围

- **证据**: TASK-018 `title: 文档机检 (SC-13 + N1 / N2) 与组 3 提交`; 但其 `verification` 第 2 条逐字: 「metadata.new_checks: n1 与 n2 对 execution-modes.md 为真, n3 对 completeness_gate.py 为真, n4(canonical = metadata.canonical_call 按行切分) 与 n8 为真 ...; metadata.crlf_guard 对两个 CRLF 文件为真(暂存前跑); audit-engine / phase-c-integrator / phase-b-developer 三份 SKILL.md 的 frontmatter 与 aria 起点逐字相同」——实际核验的是 N1/N2/N3/N4/N8 + crlf_guard + 三份 frontmatter, 比 title 里的「N1/N2」多了 N3/N4/N8/crlf_guard/frontmatter 五项。
- **失败场景**: 不影响本轨执行者(verification 段落本身完整列出全部核验项, 不会漏做), 但若后续维护者(例如别的轨想复用「哪个任务核验了 N4/N8」这条信息)只扫读 title 就下结论, 会误以为组 3 提交前只核了 SC-13+N1/N2, 从而在别处重复安排 N3/N4/N7/N8 的核验或误判其未被覆盖。
- **建议修法**: title 改为「文档机检 (SC-13 + N1/N2/N3/N4/N8 + CRLF) 与组 3 提交」, 或在原 title 后加「(含 N3/N4/N8/CRLF)」。

## 对执笔人自报薄弱点的表态

- **(a) `stage_cells` 的 39 格「在 P6 之前以终局结束」按求值总序推出、实现前无法实测**: **可接受**。这是「在实现存在之前先验证计划」这件事本身结构性带来的限制, 不是可以绕开的缺陷。我抽查了 SC-15(9) 的格 D/格 C 两格与 SC-9(4) 的 bypassed 格, 其在 §1.0 P0→P6 求值序里的位置与 TASK-008~012 的实现顺序(严格按 P 阶段编号)一致; 更重要的是 `stage_cells.code` 对「未命中该格」「该格失败」「该格被跑两次」「格名对不上」四态都判非 0(我实跑过 `cell_status.py` 的五个状态, 全部符合预期), 一旦 Phase B 实现出的真实控制流与本计划推导的不一致, 会立刻以退出 1 的形式暴露, 不会被放过。
- **(b) `coord_ref_precheck` / `commit_attribution` 偏严, 方向 fail-closed**: **可接受**。CLAUDE.md「多远程推送」两条硬约束与不可协商规则 #10 本身就要求这个方向; 我实测了 `git worktree remove` 在脏工作树下确实 rc=128(与 TASK-019/020 的做法描述一致), 也读了两个脚本的 `cannot_catch` 段, 描述的场景(心跳提交格式变化、同容器同轨多 claim 文件、`docs/handoff/latest.md` 被判 foreign)都只导向「停下请裁」而不是给出错误结论, 偏严不产生假绿, 只产生更多合法的止步点。
- **(c) 三态脚本(`a2_v2_checks.py` 的 `n6_block`)第 99 行仍 `git fetch /home/dev/Aria` 取真仓协调 ref 作 base tree**: **可接受**。我读了 `coord_ref_precheck.code`(生产用的判据本体)与 TASK-001/024/031 的实际调用方式, 均不依赖这个硬编码路径——它只出现在 `v2_state_runs` 这份**取证脚本自身**用来给 fixture 的裸仓播种一段可信历史的一行, 且已如实自报「空 ref 变体同输出」(不影响结论)。这只影响「换一台没有 `/home/dev/Aria` 路径的机器重跑这份取证脚本」这一件事, 不影响 production 的 `coord_ref_precheck` 或本计划任何一个任务的实际执行路径。建议 Phase B 顺手把播种源换成脚本内自建的最小裸仓, 但不构成阻塞开工的理由。
- **(d) `metadata.coord_ref_precheck.own_claim_files` 描述生产用法, 与 fixture 自造 claim 的做法并列时可能被读成矛盾**: **可接受**(且不构成矛盾)。我读了 `n6_block` 的源码与其内嵌注释——「N6 的本轨 claim 由脚本在临时仓自造(raw id 每跑唯一), 不依赖执笔容器是谁, 也不依赖真仓此刻的认领状态」——与 `own_claim_files` 描述的是两件不同的事(前者是取证脚本的隔离设计, 后者是 TASK-001 在真仓里的生产读法), 两处各自内部自洽, 代码层面没有冲突。唯一缺的是一条显式的交叉引用把两者关联起来防止读者一次扫读时的错觉, 这属于可读性问题, 不影响任何执行者的实际动作, 我不为此单独开 finding。

## 风险 / 疑问

- `tasks.md` 判断清单第 31 条与 yaml `new_checks`/`v2_state_runs` 合起来出现的新检查编号是 N1, N2, N3, N4, N7, N8, N10, 中间跳过了 N5、N6(coord_ref_precheck)、N9(commit_attribution)——后两者其实是 yaml 内部脚本分块的命名(`n6_block`/`n9_block`), 不是 proposal 意义上的「文档/代码同步机检」序列, N5 则完全没有出现在任何地方。这只是编号本身有缺口, 没有任何执行者动作挂在「N5」或「补齐 N5/N6/N9 编号」上, 不计入 finding, 仅记录以防日后有人误以为遗漏了一项机检。
- 「重写 b」(`§1.3(c)` 自证段, 关于本仓 154/54/17/37 等 change 目录形态计数的论证)不在我被指派的第 4 条视角范围内(该条明确点名的是重写 a 与重写 c 的区分力), 我没有独立复核这组计数, 留给其他席位; 若他们已核过, 此处不重复。
- guard_config_hooks 的口径问题(finding m1)理论上也可能被其他并发轨的类似「元数据里嵌了符号名」的改动触发, 但我没有查遍全部并发轨(10CG/Aria#211 等)是否恰好新增了这类嵌套 config.json, 只确认了「当前 A.2/v2.1 审计时点」不触发, 这条留作风险记录而非坐实的现状问题。

## Verdict

verdict: **PASS**(0C / 0M / 2m)

**Vote: PASS**

## 是否足以开始 Phase B

从测试设计与可证伪性视角看, **足以**。SC-1~SC-22 与 N1/N2/N3/N4/N7/N8/N10 在 tasks.md 的 SC↔任务映射表与 yaml 各 TASK 的 verification 之间逐条核对一致(未发现遗漏或矛盾); RED 批次(1.4-1.7)的 AssertionError 机制、`unittest`/禁 `pytest`/禁 `conftest.py` 的约束均与 `test_sibling_spec_probe.py` 两条既有守卫和 `run_all_tests.sh:41-46` 的真实分类逻辑相符(已实读源码逐条比对); 反事实设计的「三步法」在真实 git 行为下可执行(worktree remove 的 rc=128 已实测复现); 三处 Level 3 重写中, 重写 a(SC-12 liveness 的 L1/L2/L3)以 A-F 六态提供了充分区分力, 重写 c(SC-6 快照自证移到 4.4 活体)把唯一有区分力的断言放在冻结快照上、诚实标注当前目录已无区分力, 两处设计都经我读代码确认技术上成立; 我找到的两条问题均为 minor, 且都不改变执行者会做什么(guard_config_hooks 的窄口径今天不触发, TASK-018 的 title 只是概括不全, 正文本身完整)。
