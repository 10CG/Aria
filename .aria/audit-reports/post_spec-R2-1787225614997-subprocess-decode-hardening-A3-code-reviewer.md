---
seat: A3-code-reviewer
round: R2
checkpoint: post_spec
spec: subprocess-decode-hardening
verdict: APPROVE
v3_confirmation: APPROVE
v3_confirmation_timestamp: 2026-08-20T00:00:00Z
critical_count: 0
major_count: 1
minor_count: 4
timestamp: 2026-08-20T00:00:00Z
---

# post_spec R2 — A3 code-reviewer (spec v2 与真代码一致性收敛核验)

审计对象: `openspec/changes/subprocess-decode-hardening/proposal.md` (v2)
基线核验环境: aria submodule HEAD = `3b97c35` (与 spec 冻结 SHA 一致), 工作树干净 → 对工作树核验即对冻结快照核验。
方法: 四层表 16 点位逐一打开文件核对 file:line + 层归属; SC-4 链逐跳数据流追验; 脚注/Out-of-scope 主张逐条对真代码复核; R1 五项 finding 落地忠实度 + 原判定二次自验。

## 结论

**verdict: APPROVE** (0 Critical / 1 Major / 4 Minor; 判据同 R1: ≥2 Major → REVISE)

方案本体与语料口径已收敛。唯一 Major 是**编辑级勘正** (SC-4 链的 :150 leg 不达 sink, 删一个 token + 加一句 fixture 注记即闭合), 不动摇 SC-4 本身与其余任何条目; 建议主 loop 落 v2.1 后由聚合轮复读该行确认, 无需再开整轮。

## Q1/Q2 (R1 finding 落地忠实度 + 原判定自验)

**Q1: 忠实, 5/5。** A3-M1 (coordination_ref:255 errors="replace") → v2 L3 层 + SC-9 kwarg 轴 + census R1 勘正附录 ✓; A3-M2 (scan.py:476-479 顶层兜住) / A3-M3 (triage.py:315-323) → v2 L2 层, 行号与降级出口 (EXIT_INTERNAL_BUG / EXIT_HARD_FAIL) 引用准确 ✓; A3-m1 (worktree_manager 生产不可达) → 脚注 ¹, 措辞「仅 lib 导出 + tests, 仍迁移」与我的原结论一致 ✓; A3-m2 (ss `_common.py:406` 真防线是 errors=) → L4 行内注记原样落地 ✓。v2 还采纳了我 R1 建议 1 的「更准确卖点」改写 (L2 = 单点坏字节报废全 snapshot/report)。

**Q2: 原判定全部成立, 今日对冻结树逐点重验无一翻案。** 关键复核: coordination_ref.py:260-261 确为 `encoding="utf-8", errors="replace"`; scan.py:476-480 / triage.py:315-323 顶层 `except Exception` 原样在; handoff_worktrees.py:132 确用自有 `_list_worktrees` 实现 (非 lib 导入), worktree_manager `_run` 生产不可达成立; ss `_common.py:412` errors="replace" + :436 元组含 UnicodeDecodeError 成立。

## Findings

### Major

**[A3-R2-M1] SC-4 链的 aether.py:150 leg 静态不成立 — 该点 subprocess 输出不流向 JSON sink**
SC-4 写「静态追验过的唯一真实链 aether.py:150/:173 → pre_merge_gate.py:495/:518 → :568」。逐跳实核: **:173 leg 完整成立** (`_run_with_retry` :164-179 返回 stdout/stderr → `_query` :199-208 → err 并入 `AetherQueryError` 消息 aether.py:105/:123 → pre_merge_gate.py:489/:512 捕获 → :495/:518 `raw_message=str(exc)` → :568 `json.dumps(ensure_ascii=False)` ✓)。但 **:150 leg 不成立**: `_verify_in_flight_flag` (aether.py:139-162) 的 subprocess 输出只进 `last_haystack` 做 `"in-flight" in ...` 布尔判定, 探测失败时上抛的是**静态 f-string** (aether.py:88-92, 不含子进程字节), 该点字节结构上到不了 raw_message / dumps。
为什么重要: (a) SC-4 自己的规则就是「禁止按想象造链, file:line 逐跳」— R1 A2-C1 (Critical) 删掉的正是同类虚链, v2 的替换链又混入半条; (b) 实操陷阱: 按 SC-4 字面造「mock CLI 吐 `b"\xff"`」的 fixture, `--help` 探测 (:150) 的 haystack 将不含 "in-flight" → capability check 失败短路, **:173 的查询可能根本不执行**, 「JSON 出口含转义字面」断言假红, 实现者会白白调试。
如何修复 (编辑级): SC-4 链改为仅 `aether.py:173 → ...` (:150 的覆盖由 SC-1/SC-2/SC-3 承担); fixture 注记补一句「mock 的 `ci status --help` 输出须含 `in-flight` (可含坏字节但不短路 capability check), 坏字节喂给 query 命令输出」。

### Minor

**[A3-R2-m1] SC-6 「16 目标文件逐一相等」— 实为 13 文件 / 16 调用点**
verify_post_push / aether / spec_complete 各含 2 点, 去重后目标文件 = 13。SC-6 是机械判据, 按「16 文件」枚举永远对不上数。修复: 改「13 个目标文件 (16 调用点) 逐一相等」。

**[A3-R2-m2] 脚注 ² 「validate_schema_doc.py:130 无任何 enclosing try」— 词法为真, 运行链上有 try 但不接**
census 口径 `<none>` 是同函数词法域; 运行时调用者 main 有 try (:167) / `except RuntimeError` (:173), 只是接不住解码异常 (L1 归层不变)。建议限定措辞:「无词法 enclosing try; 调用者仅 except RuntimeError, 解码异常穿透」— 防止复核者 grep 到 :167 的 try 误判脚注为假。

**[A3-R2-m3] SC-9 「脚本对冻结基线跑复现四层计数 7/4/1/4」缺 L1/L2 划分的机械口径**
L3 (errors= kwarg) 与 L4 (except 元组含 Exception/ValueError/UnicodeDecodeError) 可从 AST 机械判出; 但 L1 vs L2 (7/4) 的划分依据是**跨文件调用链顶层捕获** (scan.py:476 / triage.py:315), §Why 自己声明这是「人工补查」, 单文件 AST 推不出来。实现者要么做跨程序分析 (超出 spec 声明的方法), 要么把 L2 成员表硬编码为标注数据。修复: SC-9 明示「L1/L2 划分以标注表 (含顶层捕获点 file:line) 作为脚本输入数据, 非 AST 推导」, 防止假机械声称或无法满足。

**[A3-R2-m4] 四层表 L2 行括注绑定歧义 — scan.py 链同样适用于 custom_checks.py:342**
「custom_checks.py:342 · spec_complete.py:863/:874 (经 scan.py:476-479 ...)」的括注按分隔符只绑 spec_complete, 使 custom_checks:342 无明示链。实际三点同经 build_snapshot → scan.py:476-479 (R1 A3-M2 已验)。移括注至三点共同尾部即可。另注: 「scan.py:476-479」的 `return EXIT_INTERNAL_BUG` 实在 :480, 引用范围差一行 (trivial, 源自我 R1 原文, 一并修)。

## 核验表

| # | 核验项 | 结果 |
|---|--------|------|
| 1 | 冻结 SHA `3b97c35` = submodule HEAD, 工作树干净 | PASS |
| 2 | L1 7 点位 file:line 处确为 subprocess.run + text=True (verify_post_push:65/:89 · aether:150/:173 · worktree_manager:117 · phase1_gate:240 · validate_schema_doc:130) | PASS 7/7 |
| 3 | L1 穿透性 (verify_post_push main 无顶层兜底; aether→gate_check 仅接 NIE/AetherQueryError; phase1_gate `_main`→`_gated`→impl 无 except Exception 包裹, :459 try 仅罩 get_identity; validate_schema_doc 调用者仅 except RuntimeError) | PASS 7/7 |
| 4 | L2 4 点位 + 链行号 (custom_checks:342 · spec_complete:863/:874 · scan.py:476-479 except Exception→EXIT_INTERNAL_BUG(:480) · it `_common.py:39` · triage.py:315-323→EXIT_HARD_FAIL) | PASS (差一行注记见 m4) |
| 5 | L3 coordination_ref:255 (`encoding="utf-8"` :260 / `errors="replace"` :261) | PASS |
| 6 | L4 4 点位 except 元组 (fetch_gate:68→:78 含 ValueError; closeout_trigger:90→:95 Exception; identity:173→:186 Exception; ss `_common:406`→:436 含 UnicodeDecodeError, :412 errors="replace") | PASS 4/4 |
| 7 | 7+4+1+4=16 与 census 16 目标一致; 无点分错层 | PASS |
| 8 | SC-4 链逐跳 (:173→aether:105/:123→pmg:489/:512→:495/:518→:568 dumps(ensure_ascii=False)) | :173 leg PASS; **:150 leg FAIL** (M1) |
| 9 | 脚注 ¹ worktree_manager 生产不可达 (handoff_worktrees.py:132 自有实现; lib 导出仅 tests 消费) | PASS |
| 10 | 脚注 ² 无 enclosing try | PASS (词法; 措辞注记 m2) |
| 11 | Out-of-scope: pre_merge_gate 自身结构安全 (surrogateescape :339/:344 + `_sanitize_for_json` :292/:464; 全文件无 text=True 调用点, 不在 census 16 内) | PASS |
| 12 | pre_merge_gate.py:310 先例 docstring (310-317, 含「⛔ 不传 text=True」) | PASS |
| 13 | traps.md #4/#5 原文与 spec 引用/勘正对象一致 | PASS |
| 14 | R1 聚合 9 实质点 → v2 落地逐条映射 (含「1C+8M+7m 去重 9」计数与 aggregated frontmatter 一致) | PASS 9/9 |
| 15 | A3 R1 五项落地忠实 + 原判定今日重验 | PASS 5/5 |

**通过率: 14/15** (唯一 FAIL = SC-4 的 :150 leg, 见 M1)。

## 收敛意见

实质面 (四层语料 / 16 迁移目标 / B′ 论据 / SC 可操作性主修复) 已收敛; M1 + 4m 均为编辑级, 修法唯一且可一句话验证。建议: 主 loop 落 v2.1 勘正 (M1 必修, m1-m4 建议同批), 聚合轮复读 SC-4 一行即可闭合, 不必开 R3。

---

## v3 收敛确认 (2026-08-20, 应主 loop 收敛确认轮)

对 v3 (`proposal.md` Status 行标 "v3 = R2 findings 编辑勘正") 逐条核验 R2 的 1M+4m 闭合; 引用行号为 v3 文本行号, 符号存在性对冻结树 `3b97c35` grep 实核。

| R2 finding | v3 落点 | 判定 |
|---|---|---|
| [A3-R2-M1] SC-4 链 :150 leg | SC-4 (L75): :150 leg 已删, 删除理由如实记档 ("R2 A2/A3 双席独立发现 ... 只进布尔判定、不流向 sink"); fixture 注记「mock CLI 须先让 capability check 通过、再在查询段吐 b"\xff"」= 我 M1 指出的短路陷阱, 准确落地 | **closed** (原诉求); 但符号锚定引入新缺陷, 见 [A3-R2-CC1] |
| [A3-R2-m1] SC-6 「16 文件」 | SC-6 (L77): 「13 个目标文件 / 16 个站点」✓; 匹配键还升级为 (文件路径, enclosing 函数名, 站点序号) (A2 席站点级反例驱动, 机制更强) | **closed**; 例证符号名沾染 CC1 |
| [A3-R2-m2] 脚注 ² 词法限定 | 脚注 ² (L37): 「词法上无任何 enclosing try」✓ 限定词落地 | **closed** (主限定); 括注措辞残余见 [A3-R2-CC2] |
| [A3-R2-m3] SC-9 机制边界 | SC-9 (L80): 「L1/L2 的区分不做通用调用图分析 — 以 §Why 四层表为人工标注输入, 脚本结构性回验 ... 标注表变更须人工重核」— 与我建议逐点对应 | **closed** |
| [A3-R2-m4] L2 括注绑定 + :480 | 四层表 L2 行 (L32): 「(以上三处均经 scan.py:476-480 顶层 except Exception → :480 EXIT_INTERNAL_BUG)」— 绑定消歧 ✓, 范围含 :480 ✓ | **closed** |

### v3 新文本缺陷 (收敛确认轮发现, 均编辑级 / 非阻塞)

**[A3-R2-CC1] (minor) SC-4/SC-6 符号锚定引用不存在的函数名** — SC-4 (L75) 写 "aether.py `_query_run` 的 subprocess 输出", SC-6 (L77) 写 "`_probe_capability` 三元组 vs `_query_run` 单元组"。对冻结树 grep: 两符号在 phase-c-integrator 下**零命中**; 真名为 `_run_with_retry` (aether.py:164, :173 站点的 enclosing 函数, except 元组 = (TimeoutExpired) 单元组 ✓) 与 `_verify_in_flight_flag` (aether.py:139, :150 站点, 三元组 (TimeoutExpired, FileNotFoundError, OSError) ✓)。元组语义描述与真代码逐一吻合 — 是**改名笔误而非链错**, 数据流锚定 (raw_message → dumps(ensure_ascii=False)) 本身经我 R2 逐跳验证成立。但符号锚定的全部价值就在 grep 可达, 引用不存在的符号会让实现者 grep 落空。修法 (token 级): `_query_run` → `_run_with_retry` (两处), `_probe_capability` → `_verify_in_flight_flag` (一处)。闭合验证口径: 对 proposal.md `grep -c "_query_run\|_probe_capability"` = 0 且 `grep -c "_run_with_retry\|_verify_in_flight_flag"` ≥ 3。

**[A3-R2-CC2] (trivial) 脚注 ² 括注「同文件调用链亦无捕获」字面不真** — 调用者 main 有 try (:167) / `except RuntimeError` (:173), 「亦无捕获」按字面为假 (有捕获, 只是接不住解码异常) — 这正是 m2 想防的「复核者 grep 到 try 误判脚注为假」的复发形态。建议改「调用者 main 的 try 仅 except RuntimeError, 不接解码异常」。非阻塞。

### 最终判定

**verdict: APPROVE** — R2 全部 5 项 finding 原诉求 closed (5/5); v3 新增 1 minor (CC1 符号名笔误) + 1 trivial (CC2 括注措辞), 均 token 级、修法唯一、grep 可验, 不构成重开审计轮的理由。建议主 loop 按 CC1 给出的闭合口径落 v3.1 后即可提请 owner 批准, 无需再确认轮 (grep 两条命令即自验)。

**timestamp**: 2026-08-20 (收敛确认轮; 基线核验环境同 R2: aria @ `3b97c35`, 工作树干净)
