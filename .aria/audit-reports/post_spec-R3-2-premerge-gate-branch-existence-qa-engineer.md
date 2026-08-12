---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T17:20:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 — Spec A `premerge-gate-branch-existence` — qa-engineer

角度: SC 可证伪性 — 18 条 (非任务书写的"12 条", 已核实计数法, 见下) 红窗是否真实存在 / 有无恒红恒绿空真 /
打桩边界自洽 / 三条负控早退是否真能拒绝坏实现。方法: 对 R2-fix (`017eb54`) 的每条自称**本轮独立复跑**
(不引用 R1/R2 或 commit message 的转述), 对新增两条 SC 与"兄弟位置清点表"做对抗性复核。

## 0. 计数法更正

任务书写"12 条", 但当前 proposal.md SC 表实际 **18 条** (R1 12→16, R2 16→18)。已实读确认。
下文按 18 条的现状复核。

## 1. R2 的 13M 是否真闭合 — 逐条回源复核 (本轮独立重跑, 非转述)

aggregate 列出的 5 类 Major (代表 13 条择要), 本轮**独立重新推导**其闭合证据, 结论: **全部真闭合**。

| R2 Major | 声称的修法 | 本轮独立验证 |
|---|---|---|
| hunk①③零机械锚 (`SC-A-doc`只管hunk②) | 新增 `SC-A-step`/`SC-A-note` | ✅ 独立跑 Python 正则: `执行流程`/`Subprocess调用规范`间提取步骤号序列 = `[1, 2, 2.5, 3, 4, 5, 6]` (与声称完全一致, 区间 (2,2.5) 内确实零编号 ⇒ 今日必红); `:279` 段独立核对 (a)4项无`main-branch` ✅ (b)`gate_error`零命中 ✅ (c)`无 path_coverage`零命中 ✅ — 三腿今日状态与声称逐字一致 |
| `SC-A-cli`/`SC-A-cwd` 对 backend ambient 零安排 | 新增"可达前提"块, 定义适用集10/例外集3/不适用3 | ✅ 独立核对: 10+3+3+2(元断言) = 18, 与 SC 表行数吻合, 无遗漏无重复; `SC-A10`/`A10b`/`A10c` 正确落入例外集(它们本就要打两道早退), `SC-A-cli`/`A-cwd` 正确落入适用集且打桩边界表已同步标注"backend 必须打桩" |
| `SC-A-doc` 代码侧操作数未定义 | 钉死 `gate_error` 必经 `_build_output()` 产出 | ✅ 独立读 `pre_merge_gate.py:232-263`: `_build_output` 六固定键 + 条件 `path_coverage` 键, 结构支持同款追加 `gate_error`; "实产键全集"现有唯一良定义操作数 |
| 与 B 侧 `SC-M3a` 对撞 | 明文禁 `--main-branch` 字面量, 取(i)不取(ii) | ✅ (i)/(ii)论证独立复核站得住(见§4); ⚠️ 但**兄弟位置清点表本身的穷尽性有缺口**, 见 §3 新发现 |
| Level2三项义务零承载 | 上提 BLOCKER 块 | ✅ 独立读文首 `:29-49`, O-1/O-2/O-3 三项均有"今日的唯一载体"与"漏做时会红吗"两栏, 两条出路交给 owner, 符合规则#10 |

**Unicode 出口净化 (§5 R2 追加)** — 本轮独立复现整条因果链 (未引用 R1/R2 输出):

```
$ python3 -c "import sys; print(sys.stdout.errors)"   → strict   (本机独立复跑)
$ 构造 b'...\xff\xfe...'.decode('utf-8','surrogateescape') 后 json.dumps(ensure_ascii=False) → 成功
$ sys.stdout.write(该 json 串) → UnicodeEncodeError: 'utf-8' codec can't encode ... surrogates not allowed
$ 用声称的净化 s.encode('utf-8','replace').decode('utf-8') 后再 write → 成功
```

三步独立复现, 与 R2 声称完全一致 —— **真闭合, 非 paper-fix**。

**结论**: R2 的 13M(含 2 条我本人 R2 报的: `SC-A-order` 条件轴缺失 / 已在本版闭合)**逐条真闭合**,
无一条只是"写下来"。

## 2. R1-fix 引入率能否压到 50% 以下

本席**独立发现 1 条 Major + 1 条 Minor**, 均判定 `introduced_by_r2fix=true`(细节见 §3)。
仅从本席角度看: 若五席去重后的 R2-fix 新引入总量与本轮 aggregate 一起核算, 需其余四席交叉印证方能定总比率
(单席无权判定整体收敛率), 但本席至少确认**并非零引入** —— "兄弟位置清点"这个新方法本身**没有做到自己声称的
"穷举"**, 这是新方法自身的一个洞, 而不是外部强加的新要求。

## 3. 对抗"兄弟位置清点"表 (本轮任务书点名的核心面) —— 发现真实缺口

### Finding QA-3-1 (Major): 清点表自称"穷举"但遗漏了 7 条同名 B 侧 SC, 它们目标文件正是 A 也改的文件

清点表原文 (`:143-145`): 「本轮**穷举** B 侧全部断言到『A 会碰的文件』的 SC (实跑 `grep -n 'SC-M' B/proposal.md`),
逐条判 A 是否落在其拒绝域内」。

**本轮独立复跑同一条 grep**:

```
$ grep -n 'SC-M[0-9A-Za-z]*' openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md \
  | grep -oE 'SC-M[0-9]+[a-z]?' | sort -u
SC-M1 SC-M10 SC-M11 SC-M12 SC-M13 SC-M14 SC-M15 SC-M16 SC-M17 SC-M18 SC-M2 SC-M3
SC-M3a SC-M3b SC-M3c SC-M4 SC-M5 SC-M6 SC-M7 SC-M8 SC-M9
```

清点表最终只覆盖 10 条 (M1/M2/M3a/M3b/M3c/M4/M5/M15/M16/M18) —— **全部是"grep 计数型"静态断言**。
它**完全遗漏** SC-M6/M7/M8/M10/M11/M13/M14 共 **7 条**。这 7 条不是随便挑的 7 条 ——
它们**恰是 DEC-20260812-001 §2 逐字点名要"过户"给 A 的号段**(「SC: SC-M6·M7·M8·M10·M11·M13·M14」,
后来落地时才改名 `SC-A*`)。本轮独立核对: 这 7 条**今天仍以原文一字不改**地留在 B 的 `proposal.md` 里
——例如 B `:352` 的 `SC-M6` 与 A `:437` 的 `SC-A6` 的"断言"/"期望"两列**逐字相同**
(「受控裸仓: 远端只有 `refs/heads/wip/master`, 传 `--main-branch master`」→「`verdict=fail` + `kind=="main-branch-not-found"` + `raw_message` 含分支名与 remote 名」)。

**这不是无害的文字重复**: B 侧头部虽已声明"下方正文…尚未按 A/B 划界重写"是"Phase A.1 的待办"
(`DEC §5` 第 3 项: "B 的 `detailed-tasks.yaml` 删去迁往 A 的任务时须留 cancelled 痕迹"), 但**本轮独立核对该项今天并未执行**:

```
$ grep -n "^- id: TASK-00[3-9]" -A4 openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml \
  | grep "status:"
   status: pending   (TASK-003, TASK-004, TASK-005, TASK-006, TASK-007, TASK-008, TASK-009 — 全部 pending, 无一 cancelled)
```

B 头部点名"迁往 A 的条款"正是 TASK-003/004/005/007/008/009(6 条), 它们的**目标文件**正是
`tests/test_pre_merge_gate.py` / `pre_merge_gate.py` —— **与 A 的 §Impact 第 1/2 行完全相同的文件**。
清点表的方法论 (`实跑 grep -n 'SC-M'`)已经把这 7 条 grep 出来了, 却在写"10 条"时把它们筛掉,
且**表内、表外都没有一句话解释为什么排除它们、或它们不构成风险**。

**怎么会红 (可证伪的判据)**: 若 B 侧的 `TASK-003`(在 `status: pending` 状态下, 理论上可被任何未读到
DEC 头部警告的执行者拿去跑)与 A 各自独立落地, 且 A 先 ship: B 侧 `TASK-003` 试图往
`tests/test_pre_merge_gate.py` / `pre_merge_gate.py` 里补的正是 A 已经补过的"分支存在性核验"实现与测试
—— 这在合并时会产生真实冲突(重复函数定义 / import 冲突 / git merge conflict), 是一个**清点表自称覆盖、
实际没覆盖**的碰撞类别, 与清点表已处理的 `SC-M3a` 属**同一个"这形状还有几个兄弟位置"问题**,
只是维度不同(静态字面量计数 vs. 整条行为规格与任务重复)。

**为什么不算 Critical**: (a) B 头部已声明"本侧当前不具备进 Phase B 的条件"(阻塞门尚在), 实际执行窗口不开放;
(b) 若真的发生, 大概率是响亮失败(合并冲突/重复定义), 不是 SC-M3a 那种"完全合规实现下静默转红"的隐蔽形态;
(c) DEC §5 第 3 项本就把"清理 B 的 task 列表"列为独立于 A/B 各自 post_spec 的待办项。
但它确实是**本轮任务书明确点名要对抗的那张表**的一个真实、可证伪的遗漏, 判 **Major**。

`introduced_by_r2fix`: **true** —— 遗漏本身是"兄弟位置清点表"这个 R2 新方法/新产物自己的缺口
(R1 版本没有这张表, 也就没有"穷举"这个可被证伪的承诺; 承诺是 R2-fix 新许下的)。

### Finding QA-3-2 (Minor): `SC-A-step` 的 (c) 三禁一含没有定义"该步骤正文"的抽取边界

`SC-A-step` 对 (a)(b) 两腿都本轮独立复跑验真(见 §1), 但 (c) 腿("该步骤正文 ⛔ 不含 …")
**没有像 `SC-A-doc` 那样写死抽取规则** —— `SC-A-doc` 在同一版里因为"实际解析"四个字被判欠定
(R2 已补两条解析规则, `:456-467`), 但 `SC-A-step` 的"该步骤正文"边界同样欠定:
今天文档里每个编号步骤恰好是单行(`:240-252` 逐行验证), 但 SC 判据本身**没有一句话规定**
"正文"是"匹配步骤号那一行"还是"直到下一个匹配步骤号之前的整个区块(含续行/缩进子项)"。

**怎么会红/绿(可证伪)**: 若一个不合规实现把新步骤写成两行 ——
第一行只含步骤号与占位描述(过 (a)(b) 与朴素的"该行不含禁用串"检查), 第二行(缩进续行)才写
`aether ci status --branch master --in-flight --json`(实际违反约束 2) —— 在"仅取匹配步骤号那一行"的
抽取实现下, (c) 会对着**违反约束的实现**判 GREEN(误判合规), 而在"取到下一步骤号之前的整个区块"的
抽取实现下才会正确判 RED。两种"合理"实现方式会对**同一份坏实现**给出相反判决 —— 这正是
`memory spec-underdetermination` 的形状, 且 §Rule#6 (c) 段落已明确认识到"不写死解析规则,
『实际解析』这四个字就是欠定"这条原则, 却只把它用在 `SC-A-doc` 上, 没有推广到同批新增的 `SC-A-step`。

**为什么是 Minor 非 Major**: 今日 doc 的所有步骤都是单行惯例, 且执笔方的"1 好 + 5 坏"对抗测试
(commit message 逐条列出)覆盖了值/位置/三类字面量/缺失标注五种坏实现, **但未包含"跨行拆分逃逸"这一种**
—— 是对抗测试集本身遗漏的一个真实但边缘的向量, 不影响已验证的 5 个坏实现结论。

`introduced_by_r2fix`: **true** —— `SC-A-step` 是 R2-fix 新增的 SC, 该欠定是随它一起引入的。

## 4. 复核执笔方的四条"不同意" —— 本轮独立核实结论: 均站得住

1. **SC-M3a 二选一, 取(i)不取(ii)**: 独立推演 —— 若取(ii)(把 B 的 `SC-M3a` 期望值从 2 改为 3),
   则 B 在 A ship **之前**独立跑该 SC 时字面量计数仍是 2(A 尚未落地), 断言"==3"会**先于 A 落地就失败**,
   使该值的"对不对"取决于 A/B 谁先 ship —— 这是一个随时序漂移的验收目标, 结构上比"新步骤永不写该字面量"
   (取(i))更差。论证成立。
2. **CLI 示范非新步骤自然形态**: 独立读 `SKILL.md:241-242` 确认步骤 2/2.5 确实都是函数调用形态
   (`resolve_ci_backend(cfg)` / `evaluate_path_coverage(main_branch, pr_branch)`), 与执笔方引用一致。
3. **doc 侧 7 键"本来就对", 欠定的是解析规则**: 本轮独立跑两条正则(见 §1 附带验证), 规则1(顶层键正则)
   得 7 键、朴素正则得 16 键 —— 与声称完全一致, 数字本身没错, 错的是上一版没写清规则。
4. **#137 耐久性缺陷成立但 A 内不可修, 路由进 BLOCKER**: 独立复核 `§残余暴露` 与 O-3 —— 这不是回避,
   是把一件仓外动作(在 #137 上留痕)正确地路由给了 owner 而非静默声称"已解决"。判断合理。

四条均站得住, 未发现"该修而推给 owner"的误分类。

## 5. 常规 SC 落地复核 (对 R1/R2 已验部分, 本轮抽样重跑而非照抄)

抽样重跑(非引用既有结果, 全部本轮独立执行):

- 受控裸仓仅 `refs/heads/wip/master`: 查 `master`(裸)→ 命中, `rc=0`(SC-A6 场景验真);
  查 `refs/heads/master`(锚定前缀但无 glob)→ **零命中**, `rc=0`(证明"纯锚定、且查询串本身不含 glob 字符"时锚定确实有效——这与 SC-A13 场景[查询串本身含 glob 字符]不矛盾, 两者测的是不同前提, 现文没有混淆两者);
- 受控裸仓仅 `master`: `mast*` / `m[a]ster` / `maste?`(均加 `refs/heads/` 锚定前缀)**三者全部命中**, `rc=0`
  (SC-A13 "锚定关不掉 glob" 声称验真);
- `develop`(零命中): 裸查询 `rc=0` 零行输出; `--exit-code` 查询 `rc=2`(SC-A-zero 声称验真);
- 指向不存在路径的 remote: `rc=128`, 确定性可复现, 非仅 mock 场景(SC-A7 声称验真)。

三条负控早退(`SC-A10`/`A10b`/`A10c`)本轮未发现内容变化(R2-fix 未触碰), 沿用 R2 已做的位置 mutant 结论
(核验错放在任一早退之前时, 对应负控的因果断言 `assert ls-remote 未被调用` 会转红) —— 仍然成立, 三条各自
钉住自己前面那道早退, 组合可拒绝"核验插在任一早退之前"的全部错误位置。

打桩边界表(10+3+3+2 分类)与"可达前提"块交叉核对, 无矛盾无遗漏(见 §1)。

未发现新的恒红 / 恒绿 / 空真 SC。

## 6. 结论与投票

- R2 的 13M: **全部真闭合**, 本轮五类代表性 Major 逐条独立重新推导证据, 无一处只是"写下来"(§1);
- 引入率: 本席独立发现 1M+1m, 均判定 `introduced_by_r2fix=true`(§3);
- 兄弟位置清点表: **不是真穷举** —— 遗漏 7 条与 A 目标文件相同的 B 侧行为型 SC(即 DEC 原本点名过户给 A 的
  `SC-M6/7/8/10/11/13/14`), 对应 B 侧 6 个任务仍 `status: pending` 未 cancelled(§3, Major);
- `SC-A-step` 的 (c) 腿"正文"边界欠定, 与 `SC-A-doc` 已认识到但未推广的同一类问题(§3, Minor);
- 四条"不同意"与 #137 路由决定: 均核实站得住, 无误分类(§4);
- 其余 SC 红窗真实存在, 打桩边界自洽, 三条负控早退具备真实拒绝能力(§5)。

`0 Critical + 1 Major + 1 Minor` ⇒ **verdict = PASS_WITH_WARNINGS**。

`vote = REVISE`(相对上一轮): 虽然 R2 的 13M 真闭合、Critical 保持归零, 但本轮点名要对抗的"兄弟位置清点表"
本身被发现**没有兑现"穷举"的自我声称**, 且遗漏的正是与 DEC 原始过户清单直接对应、可验证、非空的一类——
这类"新方法自己的完备性声称经不起对抗"的发现, 按本 session 的既有纪律(方法论修复须验证其"拒绝能力"而非
当前取值)应记为需要再处理一轮, 而非可以直接 PASS 带过。
