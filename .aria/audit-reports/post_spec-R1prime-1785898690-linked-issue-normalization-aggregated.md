# post_spec R1′ — `linked-issue-normalization` 聚合报告

> **轮次**: R1′ (**新基线轮, 非 R2**) | **日期**: 2026-08-05 | **被审 SHA**: `4ea1a32`
> **checkpoint**: `post_spec` (`.aria/config.json` = `convergence`, enabled, max_rounds 4)
> **席位**: 5 席全额 (`audit.teams.post_spec` 配置值, 未缩编)
> **裁决**: ⛔ **REVISE (5/5 席一致)**

---

## 为什么是「新基线轮」而不是 R2

此前 post_spec R1 (5 席) 审的是 **166 行**的旧文本并判 5/5 REVISE。此后:

- R1-fix 编辑清单 **17 条全部落地** (`ca4db78` 只落了 1 条, 2026-08-05 补落 16 条 — 见 `d7c00fd` / `5bfaa91`);
- owner 裁定 **U-1…U-6** 全部六项;
- 新增 baseline 留证 artifact (`6b3437a`) 与 §SC-7 fixture 口径整节 (`4ea1a32`)。

被审文本已扩到 **~370 行**。**R1 与本轮不可比** —— 收敛判据是「同口径 major 数是否还在降」, 而两轮的口径与总体都不同。做 R1→R2 的收敛比较即是 memory `feedback_critique_repeats_the_error_it_names` 点名的跨总体比较。**故本轮记为新基线 R1′**, 下一轮 (R2′) 方可与之比较。

---

## 席位裁决

| 席位 | 裁决 | Critical | Major | Minor | 镜头 |
|---|---|---|---|---|---|
| `aria:tech-lead` | REVISE | 3 | 5 | 5 | 范围边界 / 交付顺序 / **母 Spec 接缝** |
| `aria:backend-architect` | REVISE | 1 | 0 | 2 | 归一算法欠定性 / 实现可照写性 |
| `aria:qa-engineer` | REVISE | 1 | 5 | 6 | SC 可测性与判别力 / 变异测试 |
| `aria:code-reviewer` | REVISE | 0 | 4 | 2 | 事实断言逐条实读 |
| `aria:knowledge-manager` | REVISE | 0 | 4 | 3 | 条款间交叉一致性 / 方法论合规 |
| **原始合计** | | **5** | **18** | **18** | |
| **去重后** | | **5** | **~14** | **~13** | |

---

## 多席独立命中 (信号最强, 优先处置)

| 议题 | 命中席位 | 说明 |
|---|---|---|
| baseline 表「取证方式」与 artifact 相反 | **3 席** (code-reviewer M2 / qa M5 / tech-lead M3) | 表写 SC-7「结构推理, **未跑**」· SC-8b「**未调用本函数**」, 而 `.aria/repro/sc-baseline-…py` 两处都实调了生产函数 |
| ⭐分族规则不判定六族表 | **2 席** (tech-lead **C1** / code-reviewer M3) | tech-lead 升级为 Critical 并给出重算数 |
| D2 半幅缺口两边无 owner | **2 席** (tech-lead **C2** / km M2) | 两席各自去母 Spec 实读, 结论一致 |
| `≥35` 应为 `≥36` | **2 席** (qa m1 / km m1) | 算术错误 |
| `aria-orch` 计数在 HEAD 漂移 | **2 席** (code-reviewer m1 / km m2) | 自指语料 |
| terminal 分歧「建议单开 issue」无追踪号 | **2 席** (tech-lead m4 / km m3) | 无落点 |

---

## Critical (5 条, 去重)

### [C1] 归一规则漏第三次 strip 的实现, 通过全部 30 个 SC 子用例 — `qa-engineer`

规则 1 要求 `left`/`number_str`/`org`/`repo_basename` **每段各自 strip** (三个切分点), 但 SC 表 14 条**无一条**的空白贴在 `/` 上。变异体「`#`-split 后 strip 了, `/`-split 后忘了」对 30 个子用例零发红, 却把 Spec 步骤 1 自己举的例子 `10CG / aria-plugin#1 ≡ 10CG/aria-plugin#1` 判错。

**并已证明放进 fixture 也救不了**: SC-7 只验「实现自洽」不验「分组正确」—— 纯函数的相等判定恒自洽, 无论算得对不对。⇒ **行为断言必须直接覆盖该空白位置, 语料覆盖不能替代。**

### [C2] 规则 1 无自守卫 → 异常吞掉整批, 波及面比原缺陷更宽 — `backend-architect`

规则 3 自守卫 (「**若** `left` 含 `/`…」), 规则 1 不是 ——「无 `#`」只在规则 4 出现, 与拆分动作文本脱钩。直译 `s.rsplit('#',1)` 解包抛 `ValueError`, 下标写法抛 `IndexError`; 规则 2 的 `try/except` 只包 `int()`。异常逃到 `phase1_gate.py:1235` 的 `except Exception` ⇒ **该次调用的全部** `linked_issue_overlap` (含已正确算出的其他命中) 一并退化为 `[]`。

`--linked-issue` 是零校验自由文本 CLI 参数, `claim_schema.py:288-295` 只做 `isinstance(str)`。⇒ **任意一条畸形历史 claim 使全体 session 的重叠检测集体失明**。原缺陷影响限于同一 issue 双方; 此缺陷影响全体。**且是本 Spec 亲手引入的新击发点。**

### [C3] ⭐分族规则用了它自己明令禁止的语义知识, 两种机械读法都复现不出六族表 — `tech-lead`

规则逐字写「**不引入「这个 token 是不是真仓名」的语义知识**」, 但 **A=1** 只有把 `Forgejo [aria-plugin#17]` 的 `Forgejo` 当平台名剔除才成立, 而同批 `Forgejo [#134]/[#137]/[#139]` **保留**了它才落进 F。同一 token 一张表两种待遇。**D=1** 亦只有取**第一个**引用才成立, 而规则写「最后一个 `#`」。

实测 (同总体 / 同范围 / 同计数法, 三项与 Spec 逐字相同):

```
先 strip 判空格:  {A:4, B:4, C:1, F:2}   (n=11)
不 strip 判空格:  {C:5, F:6}             (n=11)
Spec 表声称:      {A:1, B:0, C:4, D:1, F:5}
```

U-5 裁定的成文目的逐字是「防下一轮读者重算出不同的数」—— 下一轮读者重算得到不同的数。**且「11 值」仍是行计数**: 那 11 行共含 **16** 条 `#N` 引用 (第 7 行 5 条 / 第 5 行 2 条), U-6 的「行/值分开」未真正产生值级总体。

> **结论方向不受影响** (不 strip 读法 F=6>5, SC-1 第四元论据更强)。倒下的是**可复现性**与「纯结构判定」这一措辞。

### [C4] D2 的半幅缺口指派给母 Spec, 而母 Spec 两边都没有 owner — `tech-lead` + `knowledge-manager`

本 Spec 写「母 Spec §2.3 逐字要求双方原始串、其 Impact 表已列 `phase1_gate.py`, 该半缺口由母 Spec 闭合」。两席各自去母 Spec 实读:

- 母 Impact 表 `:347` 的 `phase1_gate.py` 行只列三项 (`--include-terminal` flag / `_main():1232` 关键字参数 / `error` 带 `fetch_degraded`), **无**「把 `linked_issue` 加进 JSON 投影」;
- 母 SC-1~19 **无任何一条**断言输出 JSON 含自己那侧的 `linked_issue`;
- 母 `:154` 的要求由行为类 SC-11 承接, 而母 Spec `:289` 自己声明行为类 SC「只能由 eval 覆盖, **不冒充结构化测试**」。

⇒ 「A 说归 B 管、B 的清单里没有」的完整形态, 且母 Spec 现停在 Draft v2 + 两个 owner 阻塞项, **关闭时点无界**。

### [C5] 母 Spec 要 import 调用本 Spec 的归一, 而 SC-8a 把扩展口冻死 — `tech-lead`

母 Spec §2.1 track-id 派生表 (`:117`) 逐字规定 `basename`「经前置 Spec 归一 (含 S5 的 `./_ → -`)」⇒ 要求一个**可被 import 的归一单元**。本 Spec 通篇写「内部比较谓词」, Impact 只有一行且不承诺导出; 新增的 **SC-8a 把签名冻成 committed 测试**。

母 Spec §2.4 自己写着「**⇒ `lib/collision.py` 必须进 Impact 表** (原表零覆盖)」—— 而它**没进**母 Spec 的 Impact 表。⇒ 母 Spec 落地只剩两条路: 重实现一遍字符级算法 (而钉到字符级的全部理由正是防这个), 或回头重构。

---

## Major (~14 条, 去重后按主题)

**证据面与自指**
- baseline 表「取证方式」与 artifact 相反 (**3 席**) — SC-7 实跑了 400 次谓词调用; SC-8b 必须调用才能取 key-set; 只有 SC-8a 的「未调用」描述准确。`:203` 的「结构上不可能」全称句被自己的 artifact 反证。**且 SC-7 用的是 8 条内联串, 不是它规定的 `linked_issue_corpus.jsonl`, 未披露该替换。**
- baseline artifact **自己没有漂移守卫** (tech-lead m3→升) — 它把 proposal 的 baseline 表手抄成 `SPEC_TABLE`/`EVIDENCE_FACE` 常量, proposal 改了它不会红。**而本 Spec 对 SC-7 fixture 强制要求了漂移守卫。**

**SC 表覆盖缺口**
- 「取**最后一个** `#`」方向零覆盖 (qa M1) — 全部 SC 与 G1–G5 无一要求含 2 个以上 `#` 的值 ⇒ `split` 写成 `rsplit` 零发红
- SC-8c「6 条中 5 条驱动谓词」不成立 (qa M2) — `test_none_own_issue_short_circuits` 命中函数顶端 `if not own_linked_issue: return []`, 循环体不执行。实为 **3 条完整 + 1 条部分 + 2 条锁守卫**
- 「near-miss **负控**」命名与自己给的失败模式矛盾 (qa M3) — 「CLI 未接线 ⇒ 跨格式应命中却没命中」需要**正例**; 且被模仿的 `test_linked_issue_written_and_overlap_surfaced` 本身是正例
- G2 漏收 SC-2/SC-3 字面值 (qa M4) — **SC-3 是全 Spec 唯一能区分两种 org 实现的用例**

**文档面与合规**
- `claim_schema.py:107-114` 是第三处描述该谓词的文档面 (code-reviewer M1) — 用承重措辞 (`SAME linked_issue` / `Two **active** claims`), 不在 Impact 表 ⇒ ship 后成唯一仍描述旧语义的面, 违 Rule #3; 且**本 Spec 让这处错更承重** (yielded 变可达)
- terminal 站点枚举漏 4 处 (code-reviewer M4) — 值确为 3 个 distinct, 但站点 ≥7 处, 含 **`collision.py:155`(就在本 Spec 唯一要改的文件里)** / `reconcile.py:62` / `worktree_manager.py:615` / `gc.py:213`; 另 `reconcile.py:55-60` 注释逐字写 `"yielded" is NOT terminal`, 与 `claim_lifecycle.py` **正面冲突**
- rule6_note 未逐条对照 standards §2 的 **SKILL.md 专属附加约束** (km M1) — 只引 CLAUDE.md 摘要表; 而该 convention 的 `Source incidents` 记录的两起误判之一就发生在**同一个 state-scanner skill 家族**内
- Impact 发版行漏 3 处同步面 (tech-lead M5) — 主仓 `VERSION` / root README badge / i18n README, **后两处由 enabled custom check 守着** (`m6-version-badge-match` / `i18n-readme-translation-currency`)

**术语与决策记录**
- 「**真实输入总体**」是未纳入唯一定义处的第四种说法 (km M4) — 与「未来输入总体」共享后缀且都提 `--linked-issue`, 但后者定义为「今天尚不存在」却给出「=0 实例」实测
- 「未来输入总体」与母 §1.3 实测直接矛盾 (tech-lead M1) — 母 §1.3 实跑「直接拿字段值喂归一 **OK=0 / 不可解析=13**」; 且两份 Spec 是**同一问题的两层解**, 没写谁是主防线
- D 表缺两条承重判据 (tech-lead M4) — 规则 3 的封闭授权清单 (自陈「**最可能被下一版引用来放宽别的东西**」) 与规则 2 的可解析谓词, 都只在正文引用块里, D 表零记录
- SC-8a/8b 冻结**机械阻断**母 Spec 的 `include_terminal` 形参 (tech-lead M2) — 母 Spec 逐字写「该协调项须 owner 确认」, 而本 Spec §闸门待裁 无此项, §落地状态 反写「U-1…U-6 **全部裁定完毕**」
- §审计资产继承 R3 行「**唯一**无缺口的核心项」与 R3 原报告矛盾 (km M3) — R3 原文列**六条**并列确认项, 其中 `release-by-track` 同样无 caveat。**R1-fix 编辑清单 FIX-15 已发现该事实, 却只用它删了「可实现性评估表」措辞, 没修「唯一」这个定语**

---

## Minor (~13 条, 摘要)

`≥35`→`≥36` 算术 (2 席) · `aria-orch` 自指语料在 HEAD 漂移 738/18 (2 席) · terminal issue 无追踪号 (2 席) · G3「传递性唯一可能破在交界」被证伪 (传递性在任何位置都不会破) · `sys.get_int_max_str_digits()` 返回 `0` 是「无限制」哨兵 ⇒ 公式退化为 `len>0` **方向反转** · `normalize` 三操作顺序未在一处钉死 (已证顺序无关但 Spec 未声明) · JSON Lines 未强制 UTF-8 而内容强制含 `１２３`/`²` · 分桶退化路径未说明如何侦测违例 · 漂移守卫只能对齐硬编码清单不能对齐 SC 表 · D4 的「0 实例⇒已知限」形状可被逐字引用否定本 Spec 自身 · 三处已知限全押在双阻塞的母 Spec 上无回退 · SC-6/SC-7 故意双重覆盖需标注防误删 · `:554-557` 还断言了 `container` · Level 2 定级站得住但 G1/G3/G4/G5 无完成证据面 · S4 spike 报告的作废措辞至今未订正

---

## 被实证**站得住**的承重项 (下轮免重复)

- **D3 论域划分 / 传递性**: `backend-architect` 建完整 5 步参照实现, 对 400+ 串 + 45 元子语料的 **91,125 个三元组** fuzz 自反/对称/传递 — **0 违例**, 构造不出反例
- **`normalize` 顺序无关**: 扫全部 **1,114,112 个 Unicode 码点**确认 `casefold()` 不产生/吞噬 `#`/`/`/`.`/`_`/`-`/空白 — 0 命中; 对 3019 个 basename 跑 `{strip,译码,casefold}` 全 6 种排列 — **0 处不一致**
- **规则 2 的 CPython 断言**: 双向分叉 / `int('²')` ValueError / 4300 位边界 — 逐值复现无误
- **零 delta**: 2 席各自独立实现归一后对 ref 全 16 条回放双跑 — **TOTAL DELTA ROWS = 0**
- **substitute 证据面 `{SC-1,SC-3,SC-4,SC-5b}`**: 3 席实跑 artifact, exit 0 / 13 格 OK / SC-8c `6 passed` — **证据面结论本身正确** (被证伪的只是「取证方式」列的描述)
- **代码面全部 `file:line`**: 2 席逐条实读 — **零偏差** (含函数体真实起止行)
- **数据面**: ref 16 值 / A=4·B=11 / 号集交集空 / 3 条 yielded 时间戳 / `10CG/10cg.local` 恰 11 个 open issue 含 #20 / 1322 tests OK — 全部复现
- **blast radius**: 全仓非测试代码里 `linked_issue_overlaps` 生产调用点**只有** `phase1_gate.py:1232` 一处 ⇒ Level 2 定级成立
- **`aria-orch` 九个计数在 pinned SHA `65f17de` 上 9/9 精确复现** (km 用 `git archive` 重建历史语料树验证)

---

## 处置分类 (供 owner 裁)

| 类 | 条目 | 能否由 AI 单独处置 |
|---|---|---|
| **A. 本 Spec 内, 可直接修** | C1 · C2 · 多数 major/minor | ✅ 可 |
| **B. 我本轮工作被推翻, 需重做** | C3 (U-5 分族规则) · G2 缺口 · G3 理由 · `≥36` · artifact 与表矛盾 · artifact 缺漂移守卫 | ✅ 可 (但 C3 有三条修法, 建议 owner 选) |
| **C. 跨 Spec 边界, 须 owner 协调** | **C4** (D2 半幅归属) · **C5** (导出归一 + Impact 归属) · tech-lead M1 (两层解主辅定位) · tech-lead M2 (`include_terminal` 形参归属) | ❌ 不可 — 改的是两份 Spec 的边界 |

> **C 类的存在本身是本轮最重要的产出**: 它印证 memory `feedback_combined_mode_sister_spec_audit_value` —— 只审单 Spec 对 X-Critical 的漏率是 100%。本轮把母 Spec 交给 `tech-lead` 与 `knowledge-manager` 对读, 4 条跨 Spec 缺陷才浮出。

---

## 下一轮

R1′-fix 落地后跑 **R2′**, 与本轮同口径比较 major 数。按 memory `feedback_stop_adding_rounds_when_major_count_flattens`: **加轮判据是 major 数是否还在降**, 持平即不收敛, 届时换新鲜眼睛而非加轮。`max_rounds = 4`。
