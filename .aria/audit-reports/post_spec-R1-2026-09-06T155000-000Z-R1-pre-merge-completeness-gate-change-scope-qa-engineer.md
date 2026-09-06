---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-06T16:24:57.269Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [qa-engineer]
---

# post_spec 审计报告 — pre-merge-completeness-gate-change-scope (Round 1, qa-engineer)

审计透镜: 可证伪性 (每条 SC 反事实) / hermetic case 可构造性 / 既有测试与冻结语料 / 缺失负向测试 / 既有失败项处置。

方法: proposal 自述一律不采信。所有 SOT 行号对 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= aria `301641b`) 实读; 语料事实用 python 对 `/home/dev/Aria/.aria/audit-reports/` 与 `openspec/{changes,archive}/` 实跑枚举; SC-12 三条测试腿实跑。

---

## 审计结论

### Decisions

- [minor] testing/proposal.md SC-12 (:196) 基线: 三条既有测试腿实跑基线全绿 (@ aria 0545f86): audit-engine 104 tests OK / phase-c-integrator 148 OK / state-scanner 1505 OK, 均 exit 0。无既有失败项需 carve-out, SC-12「三者 0 failure」起点成立 (证据: 实跑 `python3 -m unittest discover` 于 `/home/dev/Aria/aria/skills/{audit-engine,phase-c-integrator,state-scanner}/tests`)
- [minor] documentation/proposal.md F1/F2/F3 (:46-48): 语料事实实测复核通过 — `.aria/audit-reports/` 780 条目 (778 `.md` + 2 目录 `pr19-submodule-scan`/`wf-r1fix`), post_spec 499 / post_planning 209 / post_implementation 3 (归属 `state-scanner-mechanical-t3` / `aria-secret-guard-plugin-default-orchestrator` / `audit-drift-guard` 逐字一致), 非 `-R\d+-` 计数 24/2/1/1 全中; 152 个 change_id 中前缀碰撞唯一 (`aria-orchestrator` → `aria-orchestrator-divestiture`); `.aria/config.json` `pre_merge=off` 且 `post_planning=convergence` ⇒ 本 spec 对 triage 注记的勘正 (`.aria/triage-comment-199.md` 「只会把 post_spec 纳入校验」) 正确 (证据: `.aria/config.json` audit 块 + python 枚举)
- [minor] documentation/Rule #6 判据: 第三行 (处方性·套件覆盖外) 判定成立 — `aria-plugin-benchmarks/ab-suite/audit-engine.json` 实测 2 evals (id 1 sibling_found 渲染 / id 2 not_established 措辞), `grep -ic 'completeness\|missing_checkpoint\|allow_incomplete'` = 0 命中 (证据: 该文件实读)

### Issues

- [critical] implementation/proposal.md §1.2 规则 2 (:98): 双侧连字符规则漏掉终端段形态 —— 本仓 63 份真报告以 `-{change_id}.md` 结尾 (无 agent_role 段), 25 个 (checkpoint, change_id) 对实有报告却匹配 0 份 → 判 `missing` → `verdict=fail` 假红阻断合并。最重的两例各 9 份 (`post_spec@aria-2.0-m6-cost-acceptance` / `post_spec@aria-2.0-m6-release-closeout`)。该形态不是历史遗留: 最新一例 `post_spec-R2-2026-06-25-session-closer-synthesis.md`。F2 (:47) 声称「匹配必须是连字符界定的子串 `-{change_id}-`, 不依赖前后段形态」—— 恰恰相反, 它**依赖尾部还有一段**。反证: 其援引的先例 `state-scanner/scripts/collectors/audit.py:107` `_ISO_DATE_TOKEN = r"-(\d{4})-(\d{2})-(\d{2})"` 只做**左侧**连字符界定, 正是为了不假设尾段存在 (证据: python 枚举 `.aria/audit-reports/` + `collectors/audit.py:100-114`)
- [critical] testing/proposal.md SC-2 (:186): SC-2 选的 fixture id `pre-merge-gate-no-run-for-branch` 全部 42 份 post_spec 报告都带 `-A{n}-{role}` / `-aggregated` 尾段, 终端段形态 0 份 ⇒ 号称覆盖「本仓文件名形态」的那条 SC, 对唯一会红的形态族结构性失明, 对上一条缺陷恒绿。其反事实只覆盖「位置解析」这一种错法, 不覆盖「尾段缺失」。守卫 fixture 须按名形态族穷举 (证据: python 列举该 id 全部 72 份报告文件名)
- [critical] implementation/proposal.md §1.2 excluded_legacy_count (:101): 计数定义「以 `{checkpoint}-` 开头但不含任何 `-{c}-`」把上述 63 份**真报告**归入 legacy。于是 R-a (:163) 依赖的「`excluded_legacy_count` 显影」不但不显影, 反而把归属 bug 伪装成「旧 schema」, 编排者读到 `legacy 不计入: N` 会得出错误结论。F4 (:49)「收窄后结构上不可能属于任何 change」只对 `{checkpoint}-{timestamp}.md` (report-storage.md:37) 成立, 不能外推到这 63 份 (证据: 同上 python 枚举 + report-storage.md:34-39)
- [major] architecture/proposal.md §1.3(b) (:110) + R-c (:165): `mid_implementation` 是阈值条件触发 (`config-loader/DEFAULTS.json` `audit.mid_implementation = {trigger: task_progress, threshold: 50}`; `audit-engine/SKILL.md:63` 标「条件触发」), 与 Step 3 已排除的 `mid_post_spec` 同因 (`execution-modes.md:51-52`「启用但无漂移时合法不产出 → 否则启用即会误阻」)。R-c 给的缓解「mid_implementation 走 1.3(b)」只在 **diff 全部 ⊆ scope_skip_paths** 时生效; 最常见的场景是 code diff + 任务进度未过 50% 阈值, 此时仍判 `missing` 假红。全表零 SC 覆盖此路径 (证据: DEFAULTS.json + SKILL.md:63 + execution-modes.md:51-52)
- [major] testing/proposal.md §1 (:76) + SC-5 (:189): 脚本 `scope_skip_paths` 缺省值「与 DEFAULTS.json / SKILL.md 文档一致」= 造出第二份副本, 但没有任何 SC 断言二者相等。该副本一旦漂移, 直接改变 `not_applicable(b)` 的**放行**面 (DEFAULTS 实为 `deploy/` `docs/` `.forgejo/workflows/` `.github/workflows/` `*.md`): 变宽 = 更多假绿, 变窄 = 更多假红。跨 skill 读 SOT 的机制 (importlib 文件直载 vs 内联复制) 也未成文 (证据: `config-loader/DEFAULTS.json` audit.scope_skip_paths 实读)
- [major] testing/proposal.md SC-2 冻结清单 (:186): 「起草时冻结的 40 个真实文件名形态」没有产物 —— `openspec/changes/pre-merge-completeness-gate-change-scope/` 实测只有 `proposal.md` 一个文件, 仓内也没有该清单; 而活体语料正被本轮 post_spec 审计写入而变动。Phase B 无法复原「起草时冻结」, 只能重新取样, 追溯性丢失。同时期望值定义为「冻结清单中含 `-{id}-` 的份数」未说明 provenance: 若测试用与实现同一谓词现算, 该断言退化为重言 (证据: `ls -la` 该 spec 目录)
- [minor] documentation/proposal.md 基线冻结 (:9): 「`git diff --stat 0545f86 301641b` 对本 spec **全部触点文件**为空 ⇒ 两 SHA 上行号一致」是过强的全称断言。F7 (:52) 与 References (:215) 引用的 `state-scanner/scripts/lib/spec_complete.py` 在两 SHA 间**有改动** (25 行): `if name == "SKILL.md":` 在 301641b 是 `:924` (F7 引用正确), 在主仓当前 gitlink 0545f86 是 `:903` —— 按当前 gitlink 追这条引用会读到 `.yaml`/`.json` 分支 (证据: `git -C aria diff --stat 0545f86 301641b -- skills/state-scanner` + 两 SHA `git show | grep -n`)
- [minor] documentation/proposal.md SC-13 (:197): 断言「三份文件的调用串逐字相同」, 但 §1 (:68) 只规定 SKILL.md 与 execution-modes.md **两处**同字面, §3 (:135-136) 给 phase-c-integrator 加的是 `change_id` 参数与 4.5 处置, 没有调用串 —— 第三个 diff 对象不存在, 该断言不可执行
- [minor] documentation/proposal.md rule6_note (:11,:93) + §4 (:148): 「固定套件 `ab-suite/audit-engine.json` **v1.3.0**」有误 —— 该文件内 `version` 实测为 `1.0.0`; `1.3.0` 是 `ab-suite/version.yaml` 的套件版本 (现为 `1.4.0`, 其 changelog 1.3.0 条即「audit-engine.json 新建」)。§4 只写 version.yaml 1.4.0→1.5.0, 未提文件内 `version` 字段该不该动 (证据: 两文件实读)
- [minor] testing/proposal.md SC-8 (:192) + 待复议 #1 (:208): SC-8 的 config fixture 里根本没有 `post_brainstorm` 键, 所以复议 #1 说的「不采纳则 SC-8 的排除集少一项」不成立; 复议 #1 的两个分支 (追加排除 / 不追加) 都没有 SC 覆盖, owner 裁决后无法被测试证伪
- [minor] testing/proposal.md SC-1 (:185): fixture 只声明 feature 分支改 `openspec/changes/x/tasks.md` + `src/a.py`, 未声明锚点 `openspec/changes/x/proposal.md` 存在。按 S1 (:84), `--change-id x` 无锚即 `error_kind=change_id_unanchored` / exit 2, 与 SC-1 期望的 exit 1 + `missing` 直接冲突。另 `git init` 建 `master` 需显式 `-b master` (现代 git `init.defaultBranch` 可能为 `main`), 否则 `--base master` 的 merge-base 解析失败落 `git_failed`
- [minor] documentation/proposal.md §5 行为变化面 (:156): §1.1 (:89) 把 `allow_incomplete_checkpoints` 从 `execution-modes.md:41-44` 的「跳过校验, 继续执行」收窄成「仍评估三态; S1/S3 的 error 不被豁免」。这对已开该旗标的采用方是第二条行为变更, §5 只列了「曾经的假绿会变成 missing」, CHANGELOG 迁移文案也未覆盖它

### Risks

- [minor] implementation/proposal.md §1.2 规则 3 (:99): 最长匹配只覆盖 `c'.startswith(change_id + "-")` 的**前缀扩展**。若某 id 是另一 id 的连字符界定**后缀或中缀** (如 `bar` 与 `foo-bar`), 归属会双计 → 假绿方向。实测当前 152 个 id 中后缀对 0 / 中缀对 0 (前缀对 1), 所以是潜伏风险而非现症, 但既无守卫也无 SC 锁定该不变量 (证据: python 三类碰撞枚举)

---

## Verdict

**FAIL** — Critical 3 / Major 3 / Minor 8 (含 2 条 decision + 1 条 risk)。

rationale: 三条 Critical 咬在同一处根: §1.2 的归属谓词要求 change_id **两侧**都有连字符, 而本仓 63 份真实报告的 change_id 就在文件名末尾。后果是这个 spec 把它要修的「假绿」换成了同等规模的「假红」—— 25 个 (checkpoint, change_id) 对明明跑过审计却被判 `missing` 并阻断合并; 而唯一号称用真实语料形态验证该谓词的 SC-2, 选了一个 100% 不含该形态的 id, 对这条缺陷结构上恒绿; 再加上 `excluded_legacy_count` 把这 63 份算作 legacy, R-a 的「显影」缓解反过来掩盖了 bug。三者叠起来构成「假绿测试掩护假红实现」的闭环, 不是措辞问题。

修法方向 (供 Round 2 参考, 不代替 owner 裁决): 归属谓词改成**左侧连字符界定 + 右侧为 `-` 或 `.md`** 二选一 (即 `-{id}-` 或以 `-{id}.md` 结尾), 与 `collectors/audit.py` 的单侧界定先例对齐; `excluded_legacy_count` 只统计**不含任何已知 id** 且形如 `{checkpoint}-{timestamp}.md` 的文件, 另设一个计数或直接报错通道给「含 id 但形态异常」的文件; SC-2 的冻结清单必须按名形态族穷举 (至少含终端段族 + role 后缀族 + `aggregated` 族 + 无 `-R\d+-` 族), 且期望值固化为字面数字并把清单落成 spec 目录内的产物。

Major 三条各自独立可修: `mid_implementation` 需要一个与 `mid_post_spec` 同构的排除条款或阈值感知的 not_applicable 通道 (并配 SC); `scope_skip_paths` 缺省副本需要一条断言「脚本缺省 == DEFAULTS.json」的 SC; SC-2 冻结清单需要落盘。

正面记录: SC-12 的三条既有测试腿实跑全绿 (104 / 148 / 1505, 均 exit 0), 无既有失败项需要处置; F1/F2/F3 的语料统计逐条实测复核无误; Rule #6 第三行判定 (套件 2 evals + completeness 关键词零命中) 成立; 对 triage 「只会把 post_spec 纳入校验」的勘正也是对的 —— 这几处的事实纪律明显高于基线, 问题集中在谓词设计与其测试覆盖。

---

## 轮次记录

### Round 1

- Agents: qa-engineer (五席之一, 本报告仅本席)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 14 (Decision 3 / Issue 10 / Risk 1) —— Critical 3, Major 3, Minor 8
- Vote: REVISE
