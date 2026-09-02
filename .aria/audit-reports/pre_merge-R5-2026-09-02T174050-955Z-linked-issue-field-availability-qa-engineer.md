---
checkpoint: pre_merge
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS
timestamp: 2026-09-02T17:55:39.000Z
context: PR #190 linked-issue-field-availability (main 0db60cc / aria d1caa66 / standards ffed204)
agents: [qa-engineer]
---

# Pre-merge 收敛审计 — PR #190 `linked-issue-field-availability` — Round 5 — qa-engineer

> 镜头: 测试与证据真实性 (对抗性验红 / 逐 SC-5(d) 隔离性复现 / 数字口径互证 / 新 check 三态 / R4 处置核验)。fresh 席位, 独立复核, 不采信 R1-R4 报告的自述数字, 全部自己实跑。

## 核验记录 (逐字命令与输出)

**1. 工作树状态确认 (无仓内写入)**
```
$ git log --oneline -1
0db60cc docs(pr190): pre_merge 收敛审计 R4 清账 — ...
$ git status --short
 M aria-orchestrator   # 与本 PR 无关, anchor 明确 out_of_scope
$ git submodule status
 d1caa66cb375c2799f55def453ca232c66a18c22 aria (v1.68.1)
+92acce5cef03eb5cde2f2bb73974f800473d52a9 aria-orchestrator (heads/feature/m6-cost-model-telemetry)
 ffed2040dff7964cf9d137e85e174173d2c685b9 standards (heads/master)
```

**2. 目标测试文件**
```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
Ran 53 tests in 3.366s
OK
```
匹配 CHANGELOG 1.68.1 / tasks.md:5 / PR body「48 → 53 条」。

**3. 全量 state-scanner 套件**
```
$ python3 run_tests.py
Ran 1462 tests in 102.474s
OK
```
匹配 CHANGELOG「Ran 1462」/ tasks.md「state-scanner 1462」。

**4. 静态 `def test_` 计数 (state-scanner/tests 全目录)**
```
$ grep -rE "^\s*def test_" aria/skills/state-scanner/tests/*.py | wc -l
1478
```
匹配 CHANGELOG「静态 def test_ 1473 → 1478」。

**5. 插件全量套件**
```
$ bash aria/skills/run_all_tests.sh
... state-scanner  OK (1462 tests)
skill 套件: 9 OK / 0 FAIL / 0 SKIP   (累计 1894 个测试)
[exited with code 0]
```
匹配 tasks.md:5「run_all_tests 1894」/ PR body「run_all_tests 9 套件 1894」。

**6. 1462 vs 1478 差 16 的口径核验 (CHANGELOG/决策单 C3 声称)**
```
$ grep -n "^def test_" aria/skills/state-scanner/tests/test_collision.py | wc -l
16
$ python3 -c "
import unittest
loader = unittest.TestLoader()
suite = loader.discover('.', pattern='test_collision.py')
print(suite.countTestCases())"
0
```
`test_collision.py` 恰 16 个模块级裸函数, `unittest.TestLoader.discover` 收集数=0 —— 证实「差 16 = test_collision.py 不被 unittest discover」的口径注为真, 非编造。

**7. 探针两条主命令 (与简报逐字比对)**
```
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt
OK (9 份在范围内, 6 条在册)
$ echo $?
0
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | od -c | head -2
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4
```
逐字匹配简报声称。独立核验作用域基数: `find openspec/changes -maxdepth 2 -name proposal.md | wc -l` = **9**; `.aria/linked-issue-field-grandfathered.txt` 非注释非空行数 = **6**。数字非巧合。

**8. 对抗性核验 — a1-entry-claim-duplicate-work-guard/proposal.md 假阳性陷阱**
该文件正文早段有一处**非字段行**提及「关联 Issue」(裁定 2 说明段, 非 `> **Linked Issue**:` 形), `grep -m1` 会误中；手工核验真实字段行位于 `:13`:
```
> **Linked Issue**: `10CG/Aria#174` — 本 Spec 的立项 issue...
```
与 `--emit-arg` 实测输出 `10CG/Aria#174` 完全一致 —— 证明探针 E0 定位逻辑在本仓真实语料 (proposal 正文引述字段名但非字段本身) 下未被假阳性欺骗, 是本 Spec 文档自陈的「本仓 Spec 文档正是假阳性陷阱」这句话的一次成功真实检验, 非仅测试套件里的合成 fixture。

**9. `plugin-version-arch-docs-match` 三态实测**
```
# OK 态 (真实仓)
PLUGIN=1.68.1 A=1.68.1 B=1.68.1 → OK plugin=1.68.1 (2 arch doc rows match)
# DRIFT 态 (scratch 副本注入旧版本号)
sed 's/aria-plugin | v1.68.1/aria-plugin | v1.67.2/' system-architecture.md(副本)
→ DRIFT plugin=1.68.1 vs system-architecture.md=1.67.2   # would exit 1
# MISSING 态 (空输入模拟正则不命中)
→ MISSING system-architecture.md §2.8 aria-plugin 行 (exit 1)
```
三态与 check 定义 (`.aria/state-checks.yaml:372-399`) 逻辑一致, 均在 scratch 副本上操作, 未改仓内文件。

**10. R4 扫描器 `.aria/repro/handoff-current-state-scan.py` 复跑 + 对抗性注入**
```
$ python3 .aria/repro/handoff-current-state-scan.py docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md --pr 190 --extra docs/handoff/latest.md openspec/changes/linked-issue-field-availability/tasks.md openspec/changes/linked-issue-field-availability/detailed-tasks.yaml openspec/changes/linked-issue-field-availability/proposal.md
residual = 0
$ echo $?
0
```
逐字匹配 R4 聚合报告声称。对抗性注入 (scratch 临时文件, 含「测试全绿 1889 条, 待推送授权中」):
```
.../fake-stale.md:5: 测试全绿 1889 条, 待推送授权中。
residual = 1
$ echo $? → 1
```
扫描器对真实注入的陈旧 token 正确 fail-CLOSED (非恒绿/恒真)。

**11. 指针口径落实面 grep (5 处派生文档)** — 手工逐份核验, 均已改为「轮次与结果以 `.aria/audit-reports/pre_merge-R*-…-aggregated.md` 最新一份为准」指针句, 不写当前轮次数字断言 (历史轮次的**既成事实**引用如「R1 12 条 / R2 11 条」允许保留, 属白名单 HIST_OK 覆盖范畴, 非陈旧声明):
- `docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md` frontmatter `phase:` 行、正文「一句话」段 — 指针句确认
- `docs/handoff/latest.md` §4 行 / track 表行 / 「2026-09-02 更新 #2」段 — 指针句确认
- `openspec/changes/linked-issue-field-availability/proposal.md` Status 行 — 指针句确认
- `openspec/changes/linked-issue-field-availability/detailed-tasks.yaml:66` metadata.status — 指针句确认
- PR #190 body (`forgejo GET /repos/10CG/Aria/pulls/190`) —「后续轮次: 轮次与结果以…最新一份为准」段确认; R1-R3 段落保留历史数字 (12/11/5 条, 四票 PASS 等), 均为已完成轮次的既成记录, 非当前态声明

**12. SC-5(d) 隔离性复现 (独立于测试套件, scratch 手工重建)**
按 R1 修复后的夹具逻辑手工重建:
```
$ cp -r aria/skills/state-scanner/lib <scratch>/copy/lib; rm <scratch>/copy/lib/collision.py
$ python3 -c "import sys; sys.path.insert(0,'<scratch>/copy'); import lib.linked_issue_field"
ModuleNotFoundError: No module named 'lib.collision'   # rc=1, 点名 lib.collision ✓
$ python3 <scratch>/copy/scripts/linked_issue_field_probe.py <scratch>/root --grandfathered <scratch>/root/does-not-exist.txt
##SKIP## 归一 SOT 不可导入 (aria 侧 lib/collision.py 或 lib/linked_issue_field.py 缺失 / 版本 < 1.68.0)
$ echo $? → 0
```
对抗性反证 (刻意重建 R1 修复**前**的旧夹具形态 —— 只复制 `__init__.py` + `linked_issue_field.py`, 不含完整 `lib/`):
```
$ python3 -c "...; import lib.linked_issue_field"
ModuleNotFoundError: No module named 'lib.claim_lifecycle'   # 不是 lib.collision!
```
证实 R1 finding `e4cde200` (旧夹具真正先炸的是 `claim_lifecycle`, 与 collision 无关) 属实; 新夹具的第一条断言 (`assertIn("lib.collision", imp.stderr)`) 在旧夹具形态下会**真的失败** —— 具备判别力, 非纸面修复。

**13. ≥5 条测试对抗验红 (临时 monkeypatch, 进程内, 未改任何仓内文件)**
选取跨 SC-1/SC-3/SC-4 的 5 条: `test_sc1e_canonical_spelling_ok` / `test_sc1f_plural_spelling_rejected` / `test_sc4e_na_is_bad_token` / `test_sc3a_two_valid_elements_ok_emits_first` / `test_e3_empty_code_span_is_bad_token`。
```
BASELINE (真实实现): ran=5 failures=0 errors=0   # 绿
BROKEN (monkeypatch extract_linked_issue_field → 恒返回 NO_TOKEN/空 elements):
  ran=5 failures=0 errors=5  # 全部转红 (AttributeError/断言失败)
RESTORED (卸载 monkeypatch 后重跑): ran=5 failures=0 errors=0  # 绿, 无残留副作用
```
`git status --short` 复核: 除 anchor 明确 out_of_scope 的 `aria-orchestrator` 外无任何改动 —— monkeypatch 全程进程内, 未落盘。

**14. AB 产物一致性抽查**
- `_BAD_EXTRACTORS` 坏实现矩阵: `grep -c "^def _bad_" test_linked_issue_field.py` = 13, 与 `test_at_least_twelve_bad_extractors_defined` 断言 `len(_BAD_EXTRACTORS)+1 == 13` 一致。
- `benchmark.json` `run_summary.old_skill.pass_rate.mean` = 1.0 / `with_skill.pass_rate.mean` = 1.0, 与 RESULT.md §1 iteration-1「12/12 vs 12/12」一致 (该 benchmark.json 只覆盖 iteration-1, RESULT.md 已注明 tokens 字段为 grader 代理值, 非隐藏矛盾)。
- PREDICTION.md「可证伪点」第 3 条逐字预告「若基线也写出合规行…Rule #6『有区分力』结论要降级为『本轮未证』」, 与 RESULT.md §2.2 实际结论「区分力: 落地前世界已证, skill 边际未证」逐字吻合 —— 非事后编造的预测。
- `git log` 显示 PREDICTION.md 与 RESULT.md 同一 commit (`989d14c`) 引入, 无法从 git 历史证明「先写预测后跑测」的时序 (与 R1 `46b1df1a` 已裁定一致: 接受为方法论留痕, 不重报为新 finding)。

**15. 双远端 SHA 核验 (无镜像分叉)**
```
aria:      origin/master = d1caa66... | github/master = d1caa66...   (一致)
standards: origin/master = ffed204... | github/master = ffed204...   (一致)
```

## 审计结论

无新增 finding。逐条复核 R4 遗留的 9 条 (2 major + 7 minor) 在 0db60cc 均已实质处置且经我独立复测确认 (§核验记录 10/11); C6/C7/C9/C9-补 (aria 侧探针代码 minor: archive 不可读守卫 / `stdout.reconfigure` 作用域 / rglob fail-open / symlink+BOM) 按简报明示口径 carry, 未发现 carry 裁定本身有误或应升级为 major, 不重报。

## Verdict

**PASS** — 0 Critical / 0 Major / 0 Minor (qa-engineer 独立复核, 无新发现)。

## 投票

**PASS** — 无「必须在合并前修」的 finding (本席本轮 0 条 finding，无条目需要判断阻塞性)。补充说明: R4 遗留的 9 条均已由 0db60cc 处置且我逐条复测确认成立，无一条需要在合并前追加修复；C6/C7/C9/C9-补 carry 项按简报明示口径继续 carry（非阻塞，v1.68.2 候选，需 owner 后续授权推送）。

## 附注 (非 finding, 供主控收敛判定参考)

- 本轮 (R5) 是「测试与证据真实性」维度连续第 4 轮零残留 (R2 起「实物面」零 finding 已由前序聚合报告记录；本轮独立复测同样零残留，含对抗性验红/三态测试/isolation 重建/双远端核验)。
- 收敛判据本身 (四元组全集 R5==R4 且四票 PASS) 是流程/架构层问题，不在本席 qa 镜头范围内裁定；上述 15 项证据均支持"本 PR 的测试与证据面"已稳定，具体收敛与否请汇总时按 SOT 字面结合其余三席结果判定。
