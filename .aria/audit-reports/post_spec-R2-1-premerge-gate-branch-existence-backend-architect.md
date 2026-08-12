---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T15:26:51.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — Spec A `premerge-gate-branch-existence` — backend-architect

seat: backend-architect · vote: PASS (with warnings) · 0 Critical + 2 Major

## 0. 结论先行

R1 的两条 Critical **真闭合**(不是 paper-fix)。R1-fix 声称的「三处纠正」(SOT 行号 / 归属 / 去重)**逐条实测成立**。
但 R1-fix 自己在**异常/解码轴**新引入(或更准确地说: 在这个轴上把承诺抬高到超过它实际兑现的程度)了
**2 条新 Major**, 都在我的席位职责内(插入点/退出码分区/异常·重试·解码三轴/additive 代码级复核)。

## 1. R1 两条 Critical 的闭合复核

### C-1 划界承重句 —— 真闭合

**判据**: 这是 Level 2/proposal-only 阶段, 被审对象是「声称的范围与其自我诚实度」, 不是代码行为。
在这个语境下, doc 修正**就是**恰当的修复介质(不落入 `feedback_paper_fix_antipattern` —— 那条 memory 讲的是
「代码 bug 被 doc-only advisory 掩盖」, 这里是「Spec 自己的范围声称」, 主体不同)。

逐字核对新增内容:
- 实读 `SKILL.md:238-262` (`aria/skills/phase-c-integrator/SKILL.md`) 确认: §C.2.4 执行流程步骤 3/4
  逐字给出**可直接照抄的裸命令** (`aether ci status --branch main --in-flight --json`), 「Helper 实现」
  只在 `:262` 作为一行脚注出现, **不是**一条「请调用 helper」的指令。这坐实了 §根因引用的
  「AI 走散文那份」不是臆测,是这份文档当前确实这样组织。
- 本仓 `git ls-remote --heads origin main` 实测 = 零行 + RC=0 (复跑确认, 与 R1 一致)。
- B 侧抬头 (`premerge-gate-mainbranch-failclosed/proposal.md:14-19`) 与 DEC §3
  (`docs/decisions/DEC-20260812-001-...md:80-105`) **都**已同步更正 —— 「A 承接关掉恒绿腿所需的**全部**
  内容」这句已作废, 两处逐字加了限定块。这是关键: 若只改了 A 自己而 DEC/B 仍在传播旧的过度声称,
  才是真正的 paper-fix (改了被审对象、没改上游会继续复读错误结论的地方)。**两处都改了, 视为真闭合**。

### C-2 Rule #6 定档 —— 真闭合, 且改判理由本身经得起复核

逐字核对 SOT `standards/conventions/skill-benchmark-exemption.md`:
- `:28` = `**deterministic substitute**: 以结构化测试...` (substitute 定义) ✅ 与 proposal 引用一致
- `:31` = `拿不准算不算处方性... | — | **照跑**(宁跑勿豁)` ✅
- `:33` = `**SKILL.md 有变动时的附加约束**...\`description\` 或指令流程变动 ⇒ 一律第二行。` ✅

三行引用**逐字命中**, R1 aggregate 原引用(`:26`/`:33`「第四行」)确实错位 —— 这条「R1 aggregate 引错」
的自陈**属实**(见下 §3)。改判本身的三条论证 (a)(b)(c)(d) 独立复核也站得住: SC-A6/A13/A-zero 三条断言
全部只读 `gate_check()` 返回 dict (`verdict`/`gate_error.kind`/`raw_message`), 单独回退 `SKILL.md` 侧 hunk
它们确实仍全绿 —— 我用同样的方法核对了这三条 SC 的断言描述(SC 表 `:297-299` 行), 无一处提到读取
`SKILL.md` 字节, 结论一致。**该改判成立。**

## 2. R1-fix「三处纠正」逐条验真

1. **SOT 行号错位** —— 见上 §1, 实测确认 R1 aggregate `:76` 写「SOT `:33` 第四行逐字『拿不准⇒照跑』」,
   而该句实际在 `:31`; `:33` 是 SKILL.md 附加约束段。**属实。**
2. **归属错误** —— journal 原始记录 (`.../wf_d165b8cd-ed6/journal.jsonl` record 4) 中 tech-lead 的
   `additive_claim` 字段逐字包含「(a) 行为兼容面未评估...(b) `:6` 逐字『无跨仓同步面』被 `:229`...自我推翻」,
   与 R1 aggregate `## 两条 A 声称里没想到的破坏面 (backend-architect)` 一节内容**逐句对应**,
   但署名是 `backend-architect`。**属实, 确系误署。**
3. **未去重** —— 我对 journal 五席原始 findings 逐条按 severity 分类统计: **6 Critical** 精确对应
   两个不同论点各 3 份重复 (boundary-claim 论点: backend-architect/qa-engineer-F1/knowledge-manager-F2;
   Rule#6-substitute-恒绿 论点: tech-lead/qa-engineer-F2/knowledge-manager-F1), 去重后确为 **2 条独立
   Critical**; 14 Major 中至少 2 对逐句重复 (「--remote CLI 零覆盖 + 24 vs 25」见于 tech-lead 与
   code-reviewer 两份; 「无跨仓同步面自相矛盾」见于 tech-lead 与 knowledge-manager 两份)。
   **「6C 里 4 条指向同一件事」与「14M 含至少两处同形重复」两条描述与我的独立统计一致, 属实。**

⇒ 这三条纠正**不是自我表扬的空话**, 是可独立复核的事实, 且我的复核路径(读 journal 原始记录,
不依赖 aggregate 转述)与它给出的结论一致。

## 3. 新发现 —— 2 条 Major (均由 R1-fix 新引入, `introduced_by_r1fix: true`)

### Major-1: §5 新钉的 `bytes + surrogateescape` 解码策略解决了 UnicodeDecodeError, 但在 `main()` 的 JSON 输出边界新开了一个未被任何 SC 覆盖的 UnicodeEncodeError 缺口

**背景**: R1-fix 新增的 §5「🔒 钉死」段(本次 diff 新增, 原版没有)明确要求私有 runner 复制
`path_coverage.py:78-102` 的形状: **bytes 读回 + `.decode("utf-8", errors="surrogateescape")`**,
理由是「那两件是配套的 —— 只抄 except 元组而用 `text=True` 就会撞上...UnicodeDecodeError」。
这条修法对**解码步骤**本身是对的、也是我复核过的既有先例 (`path_coverage.py:81-84` 注释逐字确认同一动机)。

**但**: `surrogateescape` 对无法解码的字节不抛异常, 而是把每个坏字节编码成一个**孤立代理码位**
(lone surrogate, U+DC80–U+DCFF)写进 Python `str`。这个 `str` 后续会被塞进 `raw_message` /
`gate_error.message`(§4 逐字要求两者「含分支名与 remote 名」, 而 remote 名/分支名可以逐字包含刚才
解码出的、含孤立代理码位的原始诊断文本),最终经 `main():438`
`sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")` 写出。

`json.dumps(..., ensure_ascii=False)` 对孤立代理码位**不报错**(只是原样嵌入结果字符串), 但
`sys.stdout` 默认以 `errors="strict"` 的 UTF-8 编码器写出 —— 孤立代理码位**不是合法的 Unicode 标量值**,
UTF-8 编码器会拒绝它。**我已实测复现**(与本仓 Python/环境一致, `sys.stdout.errors` 实测确为 `strict`):

```
$ python3 -c "
import json, sys
raw = b\"fatal: couldn't find remote ref \xff\xfeweird-branch\"
s = raw.decode('utf-8', errors='surrogateescape')
out = {'raw_message': s, 'verdict': 'fail'}
dumped = json.dumps(out, ensure_ascii=False)
sys.stdout.write(dumped + '\n')
"
UnicodeEncodeError: 'utf-8' codec can't encode characters in position 49-50: surrogates not allowed
```

`json.dumps(..., ensure_ascii=True)` 可以规避(转成 `\udcff` 字面转义序列,纯 ASCII, 编码不会失败 ——
我也实测确认), 但当前 `main():438` 用的正是 `ensure_ascii=False`。

**怎么会红**: 传一个包含非法 UTF-8 字节的 `--main-branch`(或目标远端在 stderr 里回显了这样的分支名 ——
git 从不校验 ref 名是不是合法 UTF-8, 这正是 §5 本段自己援引的前提), 私有 runner 正确地
`surrogateescape` 解码、正确地把诊断塞进 `raw_message`、`gate_check()` 正确返回 `verdict=fail` 的干净
dict —— 到这里为止, §5 声称要防的 `UnicodeDecodeError` 确实被防住了。但 `main()` 在把这个**完全合规**
的返回值序列化成 JSON 并写到 stdout 时, 会以 `UnicodeEncodeError` 崩溃退出(非 0 exit code, 且不打印
任何 verdict), 直接违反模块自己 docstring 里的契约 (`Exit code: 0 = success (any verdict)`)。这与
Spec 花大篇幅要避免的模式(把一个真实结果误判成基础设施失败)是**同一形状的错误**, 只是从「gate_check
内部裸抛」搬到了「main() 收尾时裸抛」。

**是否是全新缺陷类**: 不是。同一形状的暴露点(`surrogateescape` 解码结果经 `path_coverage.py` 的
`reason=f"git-diff-failed: {err}"` 一路传导进同一个 `main()` 的 `json.dumps(ensure_ascii=False)` +
`sys.stdout.write`)在 `path_coverage.py` 里**今天就已经存在**(我读了 `path_coverage.py:430-432` 的
`_result("unknown", f"git-diff-failed: {err}")` 路径确认), 早于 A/B 拆分。但 R1-fix 是**明确把这个模式
当作范式钉死、并第一次为「解码轴」写下穷尽性声明**(`⛔ 任何情形都不得当成存在放行` / 「本表以其余一切
收口」)的版本, 而它的穷尽性声明**没有覆盖到编码这一侧**; 且新代码 `_verify_branch_exists()` 的**存在
理由本身就是诊断"分支名有问题"**, 恰是最容易撞上非法字节分支名的入口。`SC-A14` 的描述(「逐个喂...
异常类」, 打桩边界表标「必须 mock」)是在**注入到 subprocess 调用**这一层测试, 不会走到 `main()` 的
`json.dumps`+`stdout.write` 这一步 —— SC 表 16 条里没有一条覆盖这条路径。

**建议**(供 Phase B 参考, 不代替 owner 裁量): 要么 `main()` 侧对写出做 `ensure_ascii=True`
或对 `raw_message`/`gate_error.message` 做一次 `.encode("utf-8","replace").decode("utf-8")` 净化,
要么给 `sys.stdout.write` 包一层 try/except 兜底为 `verify-failed`。**本 Spec 未处理, 建议 A.2
或 Phase B spike 补一条 SC。**

### Major-2: 新增的 `SC-A-doc` 要求「从 SKILL.md 的 json 块实际解析出键名集合」, 但那个块不是合法 JSON, 也没有说明如何避免把嵌套键当成顶层键

`SC-A-doc` 是 R1-fix 本轮全新增加的 SC(§SC 表 R1 新增 4 条之一)。断言原文: 「从 `SKILL.md` §C.2.4
Output schema json 块**实际解析**出的键名集合(⛔ 不得硬编码 doc 侧)== `_build_output` 的实产键全集」。

**实测**: `SKILL.md:265-277` 的 ```json 块**不是合法 JSON** —— `"verdict"` 与 `"pr_ci_status"` 两行用了
`"green" | "wait" | "fail"` 这种 pipe-联合伪类型语法(给人读的文档惯例, 不是 JSON 值)。我直接把这段
原文喂给 `json.loads()`:

```
$ python3 -c "
import json
json.loads(open('skill_block.json').read())
"
json.JSONDecodeError: Expecting ',' delimiter: line 2 column 22 (char 23)
```

(用的正是 `SKILL.md:266-276` 的逐字内容, 含 `"verdict": "green" | "wait" | "fail",` 那一行)。

⇒ 「实际解析」如果理解为 `json.loads()`,**今天就解析不过去**, 这不是 Phase B 才会踩的坑,
是这条 SC 描述本身现在就不成立(与它声称的现状「今日 doc 侧 7 键 / code 侧 7 键」矛盾 ——
那个「7」是人工数出来的,不是任何程序解析出来的)。

若改用容错手段(例如按缩进层级用正则抓 `^\s{2}"(\w+)":` 只取顶层), 又要面对第二个问题:
`in_flight_runs` 数组元素里的 `run_id`/`branch`/`started_at`/`elapsed_seconds`,
以及 `path_coverage` 对象里的 `decision`/`workflows_scanned`/`matched_workflows`/`changed_files_count`/
`reason`,都是**嵌套键**, 一个不区分嵌套层级的抓取会把它们也算进「doc 侧键集」, 使比对**结构性对不上**
`_build_output` 的顶层键集合(六固定键 ∪ `path_coverage` ∪ `gate_error`)。Spec 没有说明用什么手段
既避开「json 块不是合法 JSON」又只取顶层键 —— 这两件事都需要专门写解析逻辑, 但 Spec 把它当作
「纯文件读取, 不涉 subprocess」的低复杂度档位(打桩边界表)对待。

**怎么会红/怎么会假绿**: (a) 若实现者直接 `json.loads()` 会在 Phase B 当场炸掉, 逼着改用某种
容错解析——这条本身不是缺陷, 但说明「今天就能" 实际解析"」的现状描述不准确; (b) 更值得关注的是
如果实现者写的正则抓取过宽(把嵌套键混进去), `SC-A-doc` 判「不相等」时的失败信息会指向一堆不相关的
嵌套字段, 或者(更糟)如果两侧都恰好因为同一种嵌套污染方式凑巧「集合仍然相等」, 这条 SC 就会退化成
一个**看似机械、实则容易被实现细节意外做对或做错、而不是被它自称要防的"doc/code 键漂移"本身左右**的
弱信号 —— 与本轮 R1-fix 自己刚刚修好的 SC-A11 空真问题是同一类风险(打桩/解析边界没钉死,
断言的"看起来在测 X"和"实际测的是 X"出现分叉), 只是这次出现在一条新增 SC 自己身上。

**建议**: SC-A-doc 的实现说明应显式指定键抓取算法(例如「只取 `re.match(r'^  "(\w+)":', line)`
命中的顶层缩进行,书面钉死缩进层级假设」), 并把「SKILL.md 该 json 块不是合法 JSON」这一事实
写进 Spec 的已知限制里,而不是留给 Phase B 自己撞见。

## 4. 未发现问题的方向(供交叉核对参考)

- 插入点穷尽性(§3): `SC-A-order` 对「早于三早退」与「晚于 `evaluate_path_coverage` 调用」两个方向
  都有效钉住(反向反推验证:若核验插在 `:345` 之前, 会先违反 SC-A10/10b/10c 的「未被调用」断言;
  若插在 `:358` 之后, 违反 SC-A-order 本身)——没有找到第三个能同时绕开这两组断言的插入位置。
- 退出码分区: 用 catch-all(非零退出码全部收口)而非正向枚举,对我能想到的 git 失败模式
  (128/坏 remote、权限错误、DNS 失败)都不构成分类空洞,设计原则本身合理。
- additive 代码级复核: 25 个真实调用点(24 测试 + `main():435`)逐一核对为关键字调用风格,
  加带默认值参数确实零破坏; `_ProbeCacheResetMixin` 覆盖的 12 个测试类**逐一核对**均确实覆盖
  全部 24 处 `gate_check(` 调用(无遗漏类), 支撑「不逐条改 24 个调用点」的可行性声称。
- 重试/异常轴的常量复用先例(`pre_merge_gate.py:251` 的 `from ci_backends.aether import
  AETHER_CLI_MIN_SHA`)逐字核对存在,支撑「已有先例」的类比成立。

## 5. 严重度与投票

0 Critical + 2 Major + 0 minor ⇒ **PASS_WITH_WARNINGS**。两条 Major 均为 Phase B 可修的实现级缺口
(不动摇本 Spec 的划界/范围诚实度这一核心), 不构成 `blocks_phase_b` 级别的重开。
