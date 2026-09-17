---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T23:29:54.303Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R4 — tech-lead 席 (流程与跨任务结构)

对象: 主仓 master `edd256d` (本地未推送) 上的 `tasks.md` / `detailed-tasks.yaml` / `sc11-predicate-validation.py` v4。
本席 R1–R3 未参与, 无既往立场。

## 审计结论

### 实读范围

- 全文读: `openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md` (167 行) · `.../detailed-tasks.yaml` (896 行, 分四段读完) · `.aria/audit-reports/post_planning-R3-2026-09-15T212707-499Z-...-aggregated.md` (254 行)。
- `sc11-predicate-validation.py`: 读头部 docstring 与 `rep()` / 锚点机制 (:1-60, :69-79, :95, :244); 完整矩阵以实跑核验, 未逐行读 355 行主体 (谓词鉴别力是 code-reviewer 席的镜头)。
- v4 改动面: `git diff 2b9cb3e edd256d` 全文 (yaml 86+/58-, py 79+/14-, tasks.md 21+/13-)。
- 上游依据按要求只读不审: proposal v7 未通读 (只按 tasks.md「读前必看」表交叉定位), 决策单未通读。
- 佐证源码 (只读): `aria/skills/state-scanner/scripts/lib/spec_complete.py` (:300-370 / :1129-1202 / :1565-1660) · `aria/skills/state-scanner/scripts/lib/carry_forward.py` · `aria/skills/state-scanner/scripts/collectors/multi_remote.py` (grep) · `standards/conventions/session-handoff.md` (:95-99 / :169-182)。

### 实跑命令与关键输出

全部临时件落 `/tmp/claude-1000/.../scratchpad/r4-tech-lead/`, 已删除; `python3 -B`, `TMPDIR` 指向该目录。审计前后主仓 / aria / standards 的 HEAD 均未变 (`edd256d` / `1cb3872` / `8b49562`), 主仓 `git status --porcelain` 除本报告外无新增。

1. 结构计数:

```
$ grep -c '^- \[' tasks.md            -> 27      (未勾 26 / 已勾 1)
$ grep -c '^    parent:' yaml         -> 35
$ grep -c '^  - id: TASK-' yaml       -> 35
owner_gates 条目                       -> 15
AI 流程判断清单 1..26 连续             -> True
依赖图: 35 节点 / 缺失引用 0 / 环 0 / 唯一终点 TASK-032 / est_hours 合计 105.0 / agents 15·10·10
```

2. SC-11 验证脚本 (共识项, 本席独立复现):

```
$ python3 -B openspec/changes/.../sc11-predicate-validation.py
rc=0 ; stderr: verdict: OK (mismatch cells 0, stderr notes 0; 18 states x 19 predicates)
stdout 矩阵与 yaml metadata.sc11_predicate_validation.measured_..._v4 逐行一致
```

3. **归档门实测 (支撑「27 行全勾预演」的预期)** — 直接 import `spec_complete.py`, 对 v4 的 27 行逐行跑:

```
classify_artifact_claim (27 行):
  4.3 行 -> artifact_claim / verified=False / "dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在"
  5.5 行 -> artifact_claim / verified=True  / "linked artifact exists: aria-plugin-benchmarks/ab-results/"
_line_has_integration_keyword 命中行: v4 = [2.2, 4.4] ; v3.1 (2b9cb3e 同一判定) = [2.2, 4.4]  (无变化)
tasks.md 内方括号 token 全集: [ ] / [1.70.0\] / [proposal.md] / [`verification-ledger.md`] / [x]  (无 carry-forward / defer 形态)
```

结论: v4 改的 4 条 checkbox 行 (5.2 / 5.4 / 5.5 / 5.6) 未改变 integration-claim 行集, 3 条 unverified_claims 的预期在 v4 文本上仍结构成立; `_ARTIFACT_PATH_TOKEN_RE = [\w./\-]*(?:ab-results|ab-suite)[\w./\-]*` 与 TASK-032 的「不出现其它含 ab-results 或 ab-suite 的已存在路径」恰好同域 (`aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 不匹配该正则, 不会顶替), 且实测未替换时 `verified=True, reason` 里带的就是父目录 token —— 替换规则有效且必要。

4. **git 语义三处实跑** (支撑 M2):

```
(a) 本地 master 领先 origin/master 时:  git merge --ff-only origin/master -> "Already up to date." exit=0
    且 master 与 origin/master 仍不等 (c9c0d3c vs b01a94c)
(b) 已合并过的分支再 merge:            git merge --no-ff feat -> "Already up to date." exit=0, 不产生新合并提交
(c) 首次 --no-ff 合并产生的 HEAD^1/HEAD^2 与回退条前置一致 (对照组, 正常)
```

5. **验证脚本在「已落实现」的树上的行为 (支撑 M3)** — 把 6 个源文件复制到临时目录, 只施加 target 态的**一处**真实编辑 (`Returns only the basename ...` -> `Returns each file's path relative to ...`, 即 (c1) 要求删掉的那句), 再以该目录为源跑脚本:

```
$ python3 -B .../sc11-predicate-validation.py <postimpl 目录> --emit-json
rc=3 ; stdout 空
stderr: anchor drift: scripts/collectors/handoff_multibranch.py: 锚点应恰出现 1 次, 实际 0 次: 'Returns only the basename (not the full path) for each file '
```

6. 佐证:

```
$ grep -c '#<' standards/conventions/session-handoff.md   -> 0   (TASK-025 回填后的 grep 不恒红, 计划的声称属实)
$ git remote -v (三仓)  -> 每仓均有 origin (Forgejo) 与 github 两个真实远端, 无镜像替代
```

### R3 处置落地核验 (本席侧重相关)

| R3 项 | 处置要求 | 落地 | 证据 |
|---|---|---|---|
| PP3-M1 | 27 行勾选合并到 TASK-032 归档预演之前; TASK-026 删「勾选时…」; TASK-028 改措辞; 清单第 15 条同步 | **已落地** | yaml:886 (勾选条, 含 5.5 token 替换) · yaml:772 (TASK-028 改「勾选动作在 TASK-032」) · yaml diff 删去原 TASK-026 的勾选条 (diff:274) · tasks.md:53 清单第 15 条重写 |
| PP3-M2 | 干净断言前移到 checkout 之前; 占位检查改查提交内容; 删旧的工作树 grep | **已落地** | yaml:791 (第 2 步, `git -C standards show <feature>:...` + 自然负控) · yaml:792 (第 3 步才 checkout) · 旧第 4 步工作树 grep 已删 |
| PP3-M3 | 第 4 步停下 + ec72175 指针; 第 5 步冲突 `merge --abort` + 断言 + 停下; 第 6 步加 CHANGELOG 计数断言 | **已落地但引入新缺陷** | yaml:793 / :794 / :795 三条均在位; 缺陷见 M1 / M2 |
| PP3-M4 | `push --atomic` 写死、先 origin 后 github、禁 `--follow-tags`; 被拒 / 半推停下上报; 推后 ls-remote | **部分落地** | yaml:816 / :818 / :819 在位; 但半推之后无下游阻断, 见 M5 |
| PP3-M5 | delta 取法写死 mean(with)−mean(old); 删 WITHOUT_BETTER | **已落地** | yaml:717 (含 `new_skill`/`old_skill` 排序与 `run_summary` 断言) · yaml:716 (WITHOUT_BETTER 删除并注明) · rule6_note 同步 (yaml:152) · tasks.md:136 · 清单第 23 条 |
| PP3-M6 | 清单补 4 项旧判断 + 6 项 R4 新判断 | **已落地** | tasks.md:57-64 = 第 19–26 条, 逐条对上 R3 列的十项; 唯一未列者见 M1 末段 |
| PP3-M7 | (j1)(j3)(j2) 换 CR 的钉元组写法 + 两个新态 + authoring_rules | **已落地** | yaml:90-92 三条谓词 + `bad_tuples_stale_para` / `bad_j2_tuple_stale_para` 两态; 实跑 rc=0, 两态各仅目标谓词 FAIL |
| PP3-M8 | 补丁 1 不改 + 写明 TASK-011 之后的现表现形态 + 清单第 18 条同步 | **已落地** | yaml:532 / :533 两条 · tasks.md:56 清单第 18 条「v4 补」 |
| PP3-M9 | 四任务补台账 deliverable + 程序化核对 | **已落地** | 程序核对: 35 个 TASK 中「verification 提台账 ⇒ deliverables 含 ledger」零反例 (含 TASK-016/017 的 `# §GREEN 与反事实`, TASK-032 按归档后路径) |
| m1 | 8 项补未获授权处置; B.0 与 release_gate 两类协调 ref 口径统一; TASK-031 补「合并」 | **部分落地** | yaml:137-151 中 13/15 项带处置; TASK-034 两条 (:145/:146) 无「不进下游任务」(见 M5); TASK-001 verification 无 B.0 对应条目 (见 m2) |
| m2 | 扩面即拆 TASK | 已落地 | yaml:725 |
| m3 | 补丁 3 不复用副本; TASK-033 与读前必看第 11 条枚举补 3.5 | 已落地 | yaml:535 · yaml:447 · tasks.md:28 |
| m4 | TASK-032 开头补 ff-only 对齐 | 已落地 | yaml:885 |
| m5 | TASK-031 写死 merge 不 rebase / merge commit 不 squash / 祖先核验 | **已落地但与 M4 冲突** | yaml:866; 冲突见 M4 |
| m6 | TASK-027 提交点同式 | 已落地 | yaml:751 |
| m10 / m11 / m14 | 退出码 2/5 分离; `--emit-json` 加 `predicates`; unittest 命令补 cwd; `--repo-root` | 已落地 | yaml:183 / :100 / :301 / :357 / :768; 但 m11 在 TASK-029 的落点不可执行 (见 M3) |
| m12 / m13 / m15 / m16 / m17 | SC-8 取行方式 / TASK-001 检出断言 / 删 `:644` 调用 / writer 两处同改 / (h) 归属 | 已落地 | yaml:223 · yaml:181 · yaml:375 · yaml:410 · tasks.md:31 与 SC 映射表 :155 |

### 实施者试派生 (只看该任务与其引用文件)

**TASK-029 (5.2 子模块合并)** — 卡点 3 处。第 4 / 6 步的比较基准指向 TASK-027 的记录值, 而唯一的恢复动作会改变这两个值, 重走必然再撞 (M1); 第 5 步只写了单仓的冲突分支, 两仓混合结局无处置, 而第 3 步对「本地 master 领先」实测会静默放行 (M2); 第 7 步的 `--emit-json predicates` 在合并树上必然 rc=3 (M3)。其余步序自洽: 第 2 步的前置在第 1 步后成立, 第 3 步记的 SHA 与 CHANGELOG 计数确实只被第 6 步与 TASK-034 消费, 回退条的 `HEAD^1`/`HEAD^2` 前置在其唯一调用位置 (第 6 步、TASK-034 同名 tag 支) 都成立。

**TASK-034 (5.2 推送)** — 可无歧义执行到「被拒 / 半推 ⇒ 停下上报」为止; 卡点在停下之后: 半推态没有写「不进 TASK-030」, 而 TASK-030 只说「取 TASK-034 推送核验后的 master SHA」(M5)。`push --atomic <remote> master refs/tags/v<vNEXT>` 本身字面可执行。

**TASK-031 (5.2 主仓 PR)** — 前三条核验 (有范围提交面 / 已跟踪 / 写法自检) 可执行; 最后一条「合并后主仓 master 在 origin 与 github 的 ls-remote SHA 一致」在本计划的动作集下不可满足 (M4)。另: 有范围核验的路径清单靠手工枚举, 已漏 TASK-001 的 `touchpoints-aria.txt` (m4)。

**TASK-032 (5.4 Phase D)** — 可无歧义执行。勾选 -> 预演 -> Step 7 授权 -> 归档 -> 三子步骤 -> 双推的时点链完整, 与 TASK-031 的有范围核验不再互相拆台 (PP3-M1 已闭)。唯一未定义分支: Phase D 双推被拒 / 半推 (并入 M5)。

**TASK-026 (5.5 AB)** — 可执行。三步协调 ref 安全 + 子进程实测变量 + 两臂绝对路径核验 + 逐 eval 回归判据 + delta 符号 + SOT 登记 + owner 裁决点, 每条都能判真假。`new_skill`/`old_skill` 的 `sorted()` 顺序 (n < o) 与 R3 实跑的 `old_skill` 先于 `with_skill` (o < w) 一致, 写法成立。

### Findings

---

**M1** `[Major] type=issue · category=implementation · scope=detailed-tasks.yaml TASK-029 (:789 / :793 / :795) · v4 引入: 是`

**恢复路径死锁**: 第 4 步与第 6 步的比较基准被写死为「TASK-027 记录的取号时 SHA」与「TASK-027 的取号值」, 而第 4 步给出的唯一恢复动作恰好改变这两者, 且不含「重新记录取号时 SHA」这一步 —— 重走必然在同一处再次停下。

证据 (原文):

- yaml:793 第 4 步: `aria origin/master 相对 TASK-027 记录的取号时 SHA 已前进 ⇒ 停下上报, 不自行改号重走` … 恢复动作 = `在 feature 分支 git merge origin/master, 版本 5 文件取重算号, CHANGELOG 保留对方小节并把本方小节置顶, 重跑 TASK-021 两腿回归与 SC-11 谓词, 补跑 TASK-028 写法自检` (未含 TASK-027 的取号记录)。
- yaml:745 TASK-027: `取号时记录 aria origin/master 的 SHA … TASK-029 据此判断取号之后远端是否前进` —— 该记录只在 TASK-027 产生。
- yaml:789: `经 owner 确认的恢复动作执行完毕后, 三支一律从第 1 步重走本任务`。
- yaml:795 第 6 步: `合并后逐处核版本 5 文件取值 == TASK-027 的取号值` —— 恢复动作写的是「取重算号」, 必然不等。

照计划执行会出的错: 取号被占 -> 停下 -> owner 确认 -> 执行恢复 -> 从第 1 步重走 -> 第 4 步再次判「已前进」-> 再停下。死循环, 或执行者临场决定「把 TASK-027 的记录改掉」(无书面规则, 属 Rule #10 §5 要披露的新判断)。即使跳过第 4 步, 第 6 步也会因「取重算号 != TASK-027 取号值」判不符并触发回退。

根因是 v3.1 -> v4 的组合缺陷: v3.1 的第 3 步写的是「回 TASK-027 重跑取号计算」(基准会被刷新), R3 PP3-M3 要求删掉这条路由, v4 删了路由却把比较基准硬化成 TASK-027 的冻结值 (memory `fixes-contradict` 同形)。

建议改法 (不新增分支): 第 4 步与第 6 步的基准改为「台账中**最近一次**记录的取号时 SHA / 取号值」, 并在第 4 步的恢复指针末尾加一句「重算号后按 TASK-027 的记录格式在台账追加新的取号时 SHA 与取号值, 重走时以该新记录为准」。同时把「三支一律从第 1 步重走」这条 v4 新增的流程规则补进 AI 流程判断清单 (第 22 条只写了「停在本步、记台账、上报」, 未写重走)。

---

**M2** `[Major] type=issue · category=implementation · scope=detailed-tasks.yaml TASK-029 第 3 / 5 步 (:792 / :794) + :789 · v4 引入: 是`

**两个子模块合并结局不一致时无处置, 且重走安全性论证不成立**: 第 5 步「aria 与 standards 各自」合并, 冲突分支只写了单仓的 `merge --abort`; aria 合成功而 standards 冲突时, aria 的本地合并提交留在 master 上无人处理。第 1 条 bullet 用来论证重走安全的前提 (`第 5 / 6 步已把本地 master 复位`) 在这一支不成立, 而第 3 步对「本地 master 领先 origin/master」实测会静默放行。

证据 (三段实跑, 临时仓):

```
(a) 本地 master 领先时: git merge --ff-only origin/master -> "Already up to date." exit=0
    master=c9c0d3c, origin/master=b01a94c  (仍不等; 第 3 步在 ff-only 之后没有再断言一次)
(b) 已合并过的分支再合: git merge --no-ff feat -> "Already up to date." exit=0, 无新合并提交
```

原文: yaml:792 `不相等时先 git -C aria merge --ff-only origin/master, 不能快进则停下上报` (未写 ff-only 之后复核相等); yaml:794 `退出码非 0 (冲突) ⇒ git -C aria merge --abort, 断言 HEAD 等于第 3 步记下的 SHA …; 不在 master 上解冲突`; yaml:796 回退条的括注 `前置不成立 (例如第 5 步冲突中止, 此时根本没有合并提交)` —— 这句把第 5 步当成两仓原子的, 与「各自」矛盾。

这一支不是假想: TASK-023 自己写着 `另有 10CG/aria-standards#20 在跟踪该文件的版本头` (yaml:646), 即 standards 的同一文件上有并发轨, 冲突落在 standards 而 aria 干净是最可能的形态。

照计划执行会出的错: 停下 -> owner 处置 -> 从第 1 步重走 -> 第 3 步 ff-only 返回 0 (静默通过) -> 第 5 步 `--no-ff` 报 Already up to date 不产生合并提交 -> 第 6 步的「合并后」、第 7 步的「HEAD 等于合并 SHA」、第 8 步的 tag 全部落在一个没有本轮合并提交的树上; 台账里会记下一个上一轮遗留的 SHA 当作本轮合并 SHA。

建议改法 (删分支而非加分支): 第 5 步改成「两个子模块的合并视为一个整体: 任一仓退出码非 0 ⇒ 对**两个仓**都执行第 6 步的回退条 (前置成立的执行回退, 不成立的执行 `merge --abort`), 使两仓 HEAD 都回到第 3 步记下的 SHA, 再停下上报」; 第 3 步在 `merge --ff-only` 之后补一句「再次断言 `rev-parse master` 等于 `rev-parse origin/master`, 不等即停下上报 (本地 master 领先说明有未推送的遗留合并)」。第 1 条 bullet 的论证句同步改写。

---

**M3** `[Major] type=issue · category=testing · scope=detailed-tasks.yaml TASK-029 第 7 步 (:797) · v4 引入: 是`

**新加的机械核验在它的执行时点必然红且拿不到输出**: 第 7 步要求「另核 `sc11-predicate-validation.py --emit-json` 的 predicates 与 yaml 谓词块中 `(label)` 开头的行逐字节一致 (口径同 TASK-001)」。该脚本的全部模拟改动锚定 1cb3872 原文, `rep()` 要求 count=1 的锚点恰出现一次, 否则抛 `AnchorDrift` 并以 rc=3 结束、不打印任何 JSON。第 7 步跑在**已落实现的合并树**上, 锚点必然已被实现改掉。

证据 (实跑, 只施加一处真实的 target 编辑即触发):

```
$ python3 -B .../sc11-predicate-validation.py <只改了 (c1) 那一句的副本> --emit-json
rc=3
stdout: (空)
stderr: anchor drift: scripts/collectors/handoff_multibranch.py: 锚点应恰出现 1 次, 实际 0 次:
        'Returns only the basename (not the full path) for each file '
```

脚本原文: `sc11-predicate-validation.py:28-29` 「模拟改动按原文逐字替换: count=1 的锚点必须恰出现一次, 否则 rep() 抛出 AnchorDrift, 脚本以退出码 3 结束」; `:69-79` `rep()`; `:95` 该锚点就是 (c1) 要求删掉的句子。

照计划执行会出的错: 第 7 步拿到 rc=3, 而 TASK-001 对 rc=3 的口径是「先重写模拟改动再判谓词」(yaml:183) —— 在这个时点意味着把 18 个状态的模拟改动整体重写到实现后的基线上, 一项计划外的大工作; 或执行者临场判「这条跳过」, 而第 8 步写着「回归不通过 ⇒ 不打 tag」, 是否算不通过没有定义。两种都是临场裁决。

另一半问题: 即使可执行, 这条在此处也是零信息 —— 脚本与 yaml 同在主仓 change 目录, 自 TASK-001 起未改动 (TASK-029 之前没有任何任务把它们列进 deliverables), 所以比对结果在健康常态下恒等于 TASK-001 的结果 (memory `false_green_dual_is_permanent_red` 的判据「该信号在健康常态下应是什么值」: 恒 PASS)。

建议改法: **删掉第 7 步这一句**, 两份谓词原文的一致性由 TASK-001 一次性核验即可 (R3 m11 要求「TASK-001 与 TASK-029 第 7 步各加」, 是 R3 未核验执行时点的处方; 本席按 R4 处置原则 3「新机械检查须写得出自然红态」判其无自然红态可言)。若仍要留一道 tripwire, 换量: 在第 7 步改为「`git diff <TASK-001 起点 SHA> -- openspec/changes/<本 Spec>/{detailed-tasks.yaml,sc11-predicate-validation.py}` 只含本 cycle 已记录的提交」, 这条在实现落地后仍可跑且有真实红态。

---

**M4** `[Major] type=issue · category=implementation · scope=detailed-tasks.yaml TASK-031 (:866 / :868) 与 TASK-032 (:885) · v4 引入: 部分 (断言沿自 v1; v4 的 m5 / m4 处置把它钉成了确定矛盾)`

**验收判据恒假**: TASK-031 最后一条断言「合并后主仓 master 在 origin 与 github 的 ls-remote SHA 一致」, 但计划里没有任何一步把主仓 master 推到 github —— v4 新写的 yaml:866 把合并方式钉成「PR 以 merge commit 合并」(Forgejo 服务端), yaml:885 又明写「TASK-031 走 Forgejo 服务端合并, 本地 master 此时落后」。服务端合并只发生在 origin, 主仓 master 到 github 的唯一通道是本地推送, 而本计划里主仓的第一次 github 推送要到 TASK-032 的 Phase D 双推。

证据:

```
$ git remote -v            # 主仓
github  git@github.com:10CG/Aria.git (push)
origin  ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git (push)
$ grep -n github detailed-tasks.yaml   # 主仓侧的 github 推送只出现在 TASK-001 (规划提交) 与 TASK-032 (Phase D)
```

CLAUDE.md「多远程推送」: 「多远程一致靠**本地双推** (`git push origin && git push github`) 保证」; memory `mirror_sync_needs_mechanical_backstop`: 服务端无 push mirror 兜底。

照计划执行会出的错: 执行者要么如实记 FAIL 然后停在 TASK-031 (整条发布线被一条写错的断言挡住), 要么临场补一个 owner_gates 里没有的外向推送 `git push github master` (违反 hard_constraints 的「全部外向动作逐项列于 metadata.owner_gates」), 要么不实测直接写「一致」(假绿)。

建议改法 (加一句, 同时修 owner_gates): TASK-031 在 PR 合并之后、断言之前补一步「`git fetch origin` -> `git checkout master` -> `git merge --ff-only origin/master` -> `git push github master` (外向, 与 PR 合并同批授权)」, 并在 owner_gates 第 11 项的性质里补「含合并后把主仓 master 推 github」。TASK-032 的首条 ff-only 对齐随之变成幂等 (保留即可)。

---

**M5** `[Major] type=risk · category=architecture · scope=owner_gates :145/:146 + TASK-030 (:844) + TASK-031 (:865) + TASK-032 (:894) · v4 引入: 部分 (v4 新写了半推分支, 但只写到「记台账上报」为止; 主仓两处推送完全没有失败分支)`

**外向推送的失败分支只覆盖了子模块侧的一半**, 三处缺口同形 (memory `fix-the-class`):

1. **TASK-034 半推之后没有下游阻断**。owner_gates 里其余 5 条外向条目都带「不进下游任务 / 不进 TASK-0xx」(yaml:140 / :141 / :144 / :147 / :150), 唯独 TASK-034 的两条 (yaml:145 / :146) 没有。而 TASK-030 (yaml:844) 只写「gitlink 取 TASK-034 **推送核验后的** master SHA, 从动手当时实测值前进, 不回退」—— 「origin 成功、github 被拒」时这句照样可执行 (取 origin 的 SHA 且确实是前进)。后果正是 CLAUDE.md 硬约束 1 与 memory `mirror_sync_needs_mechanical_backstop` 要防的孤立 gitlink: 主仓 gitlink 指向一个 github 上不存在的子模块 SHA, GitHub 侧 `clone --recursive` 断裂。`multi_remote.gitlink_integrity` 是 per-(remote, submodule) 的检测器, 但计划里它唯一的落点是 TASK-031 合并**之后** (yaml:868), 属事后发现而非事前阻断。
2. **TASK-031 的主仓 feature 分支推送与 PR 合并没有被拒分支** (yaml:865 只写授权记台账)。
3. **TASK-032 的 Phase D 双推没有被拒 / 半推分支** (yaml:894 只写「双推, 逐 remote ls-remote 核验」)。主仓 master 是本仓并发度最高的共享 ref (CLAUDE.md 记录了并发容器常态), 这里被拒的概率高于 TASK-034。

照计划执行会出的错: 半推后继续 bump gitlink (1); 或推送被拒后执行者自行判断是重试、force 还是先 fetch 再合 (2)(3) —— memory `partial-push` 与 `fetch-then-write` 都指向这里最容易出不可逆错。

建议改法 (三处各一句, 不新增流程层): owner_gates 的两条 TASK-034 条目各补「不进 TASK-030」; TASK-030 的第一条核验补前置「前置 = TASK-034 的逐 remote ls-remote 对 **origin 与 github 双方**均已核验一致; 任一方未一致不得 bump gitlink」; TASK-031 与 TASK-032 的推送条各补一句「被拒或只推成一个远端 ⇒ 不 force、不改写历史, 原样记台账并停下上报 (同 TASK-034)」, 并在 owner_gates 第 11 / 15 项里带上这句。

---

**m1** `[Minor] type=issue · category=documentation · scope=owner_gates :144 与 TASK-029 :789 · v4 引入: 是`

owner_gates 第 8 项与 TASK-029 第 1 条 bullet 都只枚举「第 4 / 5 / 6 步」为 fail-closed 上报点, 但第 2 步 (`不成立 ⇒ 停下…或上报`)、第 3 步 (`不能快进则停下上报`)、第 7/8 步 (`前提不成立不得跑` / `回归不通过 ⇒ 不打 tag、不进 TASK-034`) 同样会停在本步等 owner。这三处既不在 owner_gates 里, 也没有重走规则 (「三支一律从第 1 步重走」按字面只管 4/5/6)。建议: 把枚举改为「任一步停下均属 owner 等待点」, 重走规则改为「任何一次停下经 owner 处置后一律从第 1 步重走」。

**m2** `[Minor] type=issue · category=documentation · scope=TASK-001 :176-184 与 owner_gates :137 · v4 引入: 是`

owner_gates 第 1 项 v4 新增了「B.0 phase1_gate 认领推协调 ref … 与本项同批请授权」, 但 TASK-001 的 verification 里没有对应条目, 与 hard_constraints 的「各任务里的对应条目与之一致」(yaml:127) 相违。另: owner 不授权时没有抑制该推送的机制 —— TASK-026 用 `ARIA_COORDINATION_NO_PUSH=1` 显式关掉, B.0 这一处没有对应手段 (memory `ab-harness-real-repo` 记有 `--no-push` 可用)。建议 TASK-001 补一条 verification, 写明未获授权时以 `ARIA_COORDINATION_NO_PUSH=1` 或 `--no-push` 跑 B.0。

**m3** `[Minor] type=issue · category=documentation · scope=tasks.md :70 · v4 引入: 是`

「其中三处须特别留意」仍是 v3 的三处 (1.3 推送 / 5.5 裁决点 / 5.4 Step 7), 未纳入 v4 新增的两处 fail-closed 停下上报点 (TASK-029 / TASK-034)。这两处的后果 (孤儿 tag / 镜像分叉) 比原三处更重。建议改为「四处」或「五处」并点名。

**m4** `[Minor] type=issue · category=implementation · scope=TASK-001 :179 与 TASK-031 :862 · v4 引入: 否`

TASK-001 产出 `touchpoints-aria.txt` (41 行) 但未定其落盘位置。若落在仓内, TASK-031 的有范围核验要求「其余每一行逐条写明归属并**判定与本 cycle 无关**」—— 一个本 cycle 产生却不在交付物清单上的未跟踪文件无法满足该判定。建议 TASK-001 明写落 scratchpad (与 TASK-018 / TASK-022 的副本同处), 或把它加进 TASK-031 的交付物路径清单。同类风险: TASK-026 两臂的一次性 worktree 位置也未写 scratchpad。

**m5** `[Minor] type=decision · category=architecture · scope=TASK-026 :725 · v4 引入: 是`

「扩面即拆任务 (新编号自 TASK-036 起, 工时另估, 依赖与本任务相同)」未说明新任务的 `parent` 归哪一行 checkbox, 也未说明 `metadata.total_tasks: 35` / `est_hours_total: 105` 怎么更新 —— 而 R3 五席共识里「27 个 parent 对 27 个 checkbox」是被核验过的结构不变量。更根本的是: 在 Phase B 执行期新增 TASK 等于 post_planning 之后改 A.3, 计划没说要不要记进 AI 流程判断清单。建议补一句「新任务 parent 沿用 5.5, 不新增 checkbox; total_tasks / est_hours_total 同批更新; 该拆分记入 AI 流程判断清单」。

**m6** `[Minor] type=issue · category=documentation · scope=metadata.verification_ledger.skeleton :27 · v4 引入: 是`

台账骨架 11 个二级标题固定且「后续只在对应标题下追加, **不改标题**」, 但 v4 新增的三类 fail-closed 停下记录 (取号被占 / 合并冲突 / 取号终核不符) 没有对应标题: 「外向动作与授权」不贴切 (这三支都还没推), 「回归」只覆盖第 7 步。建议在骨架里加一个「停下与上报」标题, 或明写这三类记入「外向动作与授权」。

**m7** `[Minor] type=issue · category=documentation · scope=TASK-029 第 2 步 :791 · v4 引入: 是`

同一条里既要求 `grep -c '#<' 为 0`, 又要求「同一输出正向含第三态从句与 `10CG/aria-plugin#<n>`」。`<n>` 在本文件里是元记号 (hard_constraints:134 同写法), 但逐字读会自相矛盾 (含 `#<` 即 grep 非 0)。建议写成「含 `10CG/aria-plugin#` 加数字」。

**m8** `[Minor] type=risk · category=implementation · scope=TASK-029 est_hours :780 · v4 引入: 否`

TASK-029 估 2h, 内含第 7 步的全量回归 (`run_tests.py` 1605 用例 + 两条 pytest 腿 + 19 条谓词), 与 TASK-021 同一工作量却估 3.5h。v4 又给它加了 8 步的逐步记账与三支停下分支。工时与内容不相称, 建议提到 3-4h。

### 核对无误的部分 (不计 finding)

1. 结构不变量: 27 checkbox 对 27 parent、35 TASK、依赖无环无悬空、唯一终点 TASK-032、est_hours 合计 105.0 与 `est_hours_total` 一致、agent 分布 15/10/10 与 `metadata.agents` 一致。
2. owner_gates 恰 15 条, 按执行序排列且与依赖图的一个合法线性化一致; 13/15 条带未获授权处置 (缺的两条见 M5)。
3. AI 流程判断清单 1..26 编号连续无跳号; R3 PP3-M6 点名的十项判断逐条落地 (第 19–26 条), 含两处 conflicted 裁决与「覆盖两个 Skill 默认合并策略」这项自觉披露。
4. 归档门三条 unverified_claims 的预期在 v4 文本上仍结构成立: v4 改的 4 条 checkbox 行未改变 integration-claim 行集 (实测 v3.1 与 v4 同为 2.2 / 4.4), 4.3 的 artifact_claim 仍 `verified=False`, tasks.md 无 carry-forward / defer 形态方括号。
5. TASK-032 的 5.5 父目录 token 替换规则与 `_ARTIFACT_PATH_TOKEN_RE` 恰好同域: `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 不匹配该正则, 不会顶替成第一个存在路径; 实测未替换时 `reason` 正是 `linked artifact exists: aria-plugin-benchmarks/ab-results/` (恒过), 替换规则有效且必要。
6. PP3-M1 已真正闭合: 27 行勾选与 Phase D 提交同点, TASK-031 的有范围核验在好态下不再恒假, TASK-028 / TASK-026 / 清单第 15 条三处措辞一致。
7. PP3-M9 的类级修复到位: 程序化核对 35 个 TASK, 「verification 提台账 ⇒ deliverables 含台账且带标题注释」零反例。
8. SC-11 验证脚本 rc=0, 18 态 x 19 谓词与 yaml 实测块逐行一致; PP3-M7 / m7 / m9 新增的 4 个坏态各仅目标谓词 FAIL, 两个 alt 态全 PASS。
9. AB 段: `new_skill`/`old_skill` 的 `sorted()` 顺序 (n < o) 确实让 with 臂排前, 与 R3 实跑的 `old_skill` < `with_skill` (o < w) 互为验证; delta 取法、逐 eval 回归判据 (三样本 >=2)、SOT 验收登记、owner 裁决点四项都可判定; Rule #6 的时点正确 (5.5 在 5.1 之前)。
10. 组 3 / 组 4 并发的文件域划分成立: TASK-019 (schema) / TASK-020 (collector + phase-1-collectors + dedupe 测试) / TASK-023 (standards + layer-l) / TASK-024 (三份候选) 文件集两两不交, 组 3 的反事实一律在 scratchpad 的一次性 worktree 上做 (memory `workflow-file-domain`)。
11. TASK-025 的 `grep -n '#<' conventions/session-handoff.md 零命中` 不恒红: 实测当前 standards `8b49562` 上该命令输出 0。
12. TASK-029 回退条的 `HEAD^1` / `HEAD^2` 前置在其两个调用位置 (第 6 步、TASK-034 同名 tag 支) 均成立 (实跑对照组确认 `--no-ff` 首次合并的父提交形态)。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 5 Major / 8 Minor)

无 Critical: 五个 Major 都落在 Phase C 发布段的少见分支或单条断言上, 不构成「照计划执行必然造成不可逆损害」; M5 最接近 (半推后 bump gitlink 是不可逆的镜像损坏), 但计划的 fail-closed 基调与 TASK-034 末条「与本地一致才算完成」会让守纪律的执行者停下, 故按 Major 计。

## Vote

**REVISE** (有 Major)

## 边际判断

**结论: 这份计划在「能不能执行」上已经越过拐点 —— 缺的不是机制, 是删减。**

依据:

1. **本轮 5 个 Major 全部落在同一片 200 行文本里 (TASK-029/030/031/034 的发布段), 而且 4 个是最近两轮新加的流程自己长出来的**: M1 是 v4 删了路由却保留冻结基准 (R3 处方的副作用), M2 是 v4 新写的冲突分支只写了单仓, M3 是 R3 m11 的新检查在它的执行时点必然 rc=3, M4 是 v4 把合并方式钉死之后与一条老断言撞车。组 1–4 (24 个 TASK, 约 70 小时, 真正的工程量) 本轮我一条都没挑出来 —— 试派生 TASK-026 / TASK-032 都能无歧义执行。这就是 memory `marginal-return-negative` 说的「本轮 fix 引入的 major 占比 > 1/2」: 5 个里 4 个是新表面上的。
2. **本轮新增的机制里, 有三条在真实执行中几乎肯定用不上或用不了**:
   - 第 4 步的 `ec72175` 重算号恢复指针: 触发条件是 TASK-027 取号到 TASK-029 合并之间 aria `origin/master` 前进 —— 在单人 Lab 加一条并发轨、窗口只有几小时的前提下, 概率很低; 而它一旦触发, 按现文本是死锁 (M1)。
   - 第 6 步的 CHANGELOG 小节计数断言: 它防的是「解冲突时丢掉对方小节」, 但第 5 步已经写死「不在 master 上解冲突, 冲突即 abort」—— 主线上这条断言恒满足 (合并后必然 +1), 只有走完上面那条低概率恢复路径才可能红。
   - 第 7 步的 `--emit-json predicates` 比对: 实测在执行时点 rc=3, 拿不到输出; 即使能跑, 比对的两个文件从 TASK-001 起就没有任何任务会改动, 结果恒等于 TASK-001 的结果。
   与之相对, **同一批新增里确实有便宜又有真红态的**: 第 2 步改查提交内容 (自然负控 = 回填前输出 1)、`push --atomic`、TASK-032 的 ff-only 对齐、验证脚本的 4 个新坏态 —— 这些应当保留。
3. **维护成本与产出不相称的一处**: TASK-031 的有范围核验把 15 个交付物路径逐条内联枚举 (yaml:862), 每加一个产物就要手工同步; 它已经漏掉了 TASK-001 的 `touchpoints-aria.txt` (m4)。这类手工清单在执行期一定会漂, 且漂了没人发现 —— 建议改成「本 Spec 目录 + TASK-030 的 deliverables + 本次 ab-results 目录」三类, 其余行只记归属、不再断言「与本 cycle 无关」。

**给 owner 的三选一建议 (不是我的裁决, 是把选项集摆全)**:

- **A (推荐)**: 不再加轮。本轮 5 个 Major 的修法合计约 6 句话 (M1 改基准来源并补一句重走规则 / M2 把两仓合并当整体回退并在 ff-only 后补一次断言 / M3 直接删那句 / M4 补一步 `git push github master` 并进 owner_gates / M5 三处各补一句停下与一条前置), 全部是「删或改一句」, 不新增流程层。改完由主控做一次只看这 6 处的定点核验后进 Phase B, 不再派五席。
- **B**: 按配置跑满 R5。但要预期 R5 的 Major 仍然会长在 R4 新改的这 6 处上 —— 前三轮 13 -> 9 -> 9 -> 5 的下降主要来自组 1–4 收敛, 发布段的 Major 数没有下降过 (R3 有 M2/M3/M4 三条在这里, R4 有五条)。
- **C (值得认真考虑)**: 把发布段的流程文本**整段降级**。TASK-029/030/031/034 现在用 4 个 TASK、约 40 行 verification 在重新规定 `phase-c-integrator` 与 CLAUDE.md 两条硬约束本来就规定的事; 每一轮审计都在这段文本上找到新缺陷, 而这些缺陷全都是「规格自己写出来的分支之间对不上」, 不是方法论缺口。改成「按 `phase-c-integrator` C.2 执行, 另守三条本 Spec 特有的约束 (取号复核 / `push --atomic` / 两远端核验后才 bump gitlink)」, 新增表面立刻降一个量级, 代价是失去逐步台账的颗粒度。这条选项前三轮没有被摆到 owner 面前过 (memory `narrow-owner-options`)。

顺带一条给 R5 或主控的提醒: 本轮我用到的三段 git 语义实跑 (ff-only 对领先 master 返回 0 / 重复 `--no-ff` 不产生提交 / 验证脚本在实现后的树上 rc=3) 都只要一分钟, 但三条都推翻了纯阅读得到的结论。发布段剩下的任何改动, 建议同样先在临时仓跑一遍状态模拟再落笔 (R3 主控自查里已经写了这条要求, 本轮 M1/M2/M3 说明它没有覆盖到新写的那几支)。

## 轮次记录

- R1 (0C/13M) -> v2 -> R2 (0C/9M, 7 条由 v2 引入, 换执笔人) -> v3 -> 主控核验返修 -> v3.1 -> R3 (0C/9M, 5 条由 v3 引入) -> v4 -> **R4 (本席 0C/5M/8m)**。
- Major 趋势: 13 -> 9 -> 9 -> 5 (本席单席口径, 非聚合)。**首次下降**, 但下降全部来自组 1–4; 发布段 (组 5 的 5.2 / 5.1) 的 Major 数为 R3 的 3 条 -> R4 的 5 条, 未降。
- 本轮 Major 中「由 v4 引入」: M1 是 / M2 是 / M3 是 / M4 部分 / M5 部分 = 3 完全 + 2 部分, 占 5 分之 3 (计入部分为 5 分之 5)。memory `marginal-return-negative` 的拐点判据 (本轮 fix 引入的 major 占比 > 1/2) 仍然亮着。
- 本席为新派席位, 与 R1–R3 无共同上下文; 按 memory `stop-adding-rounds` 的「换新鲜眼睛 > 加轮」, 本轮的信息量主要来自镜头更换而非轮次增加, 这一点已反映在 `## 边际判断` 的选项 A。
