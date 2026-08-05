---
verdict: REVISE
agent: qa-engineer
round: R3
critical_count: 0
major_count: 2
minor_count: 3
r2_resolved: 1/2
---

# post_spec R3 — QA 审计 (第三版设计, fail-safe 降级): secret-guard-per-segment-evaluation

审计对象: `openspec/changes/secret-guard-per-segment-evaluation/proposal.md` (v3: 分段前先判块结构, 不可安全分段则退回整命令判定)。方法: canonical `aria/hooks/secret-guard.sh` **直调**; 语料用「改 `bash_case` 函数体旁路 dump」技术从 `secret-guard.test.sh` 精确抽取 305 条 (复制件打补丁, 未改仓库文件); 独立重写 `safe_to_split()`/`split_top()`/`verdict()` (token 流 + 显式"期待命令起始"状态标志, 与作者原型 `scratchpad/failsafe_v3.py` 的单遍字符状态机 + lookbehind 正则**算法形状不同**, 仅读 spec 文字未抄原型逻辑) 用于独立复验 SC-1/5/6/7/12。

## 1. R2 核销

| # | R2 结论 | R3 处置 | 证据 |
|---|---------|---------|------|
| C-1 | 65/49/16 数字 vs proposal 声称 52 不一致 | **已解决** — proposal 现定案 65/49/16/15/1, 用**第三套独立实现**(正则批量脱引号+反向 token 扫描, 与 R2 的状态机/token 流双扫描器均不同)复算, 结果**逐位精确复现 65/49/16/15/1**, 含"1 真边界即 KNOWN-LIMIT"细节完全吻合。三方独立实现(作者/R2 QA/R3 QA)三次收敛到同一数字, 数字侧可认为已闭环 | 见 §2 |
| m-1(R1→R2) 语料重复 (`"FP-fix timeout run-env"` 行 641/673) | **仍未解决 (第三次静默丢弃)** — 现文件核实重复依旧存在(行 641/673 字节级相同), proposal.md 全文检索零命中"FP-fix"/"重复"/"duplicate" | grep 核实 |
| SC-8 阈值前瞻观察 | 不适用为"待解决项" — 该条本就是"Phase B 落地后复测"的前瞻建议, 非可在 spec 文字阶段修复的缺陷 | — |

`r2_resolved = 1/2`(计入 C-1 已解决 + m-1 未解决两个实质项; SC-8 观察项按性质不计入分母)。

## 2. C-1 数字复核 + 「交付计数器」根治手段评估

独立脚本(`census_r3.py`, 正则批量脱引号 + 反向 token 扫描)对精确抽取的 305 条重新分类:

```
305 条中含顶层边界记号 (;/&&/||/|): 65
  ├ want=2: 49
  └ want=0: 16
      ├ 纯管道: 15
      └ 含真命令边界: 1  (= "put: KNOWN-LIMIT compound credit leak")
换行边界 (无顶层记号, 含 \n): 5
  ├ want=2: 4
  └ want=0: 1
```

与 proposal.md 定案数字 **逐位一致**。

**「交付计数器」是否足够**: 数字本身层面已充分(三次独立复现同一结果, 强证据)。但结构层面有一处**未闭环**: Task 1.4 只要求"交付" `corpus_census.py`, 没有配套 SC/Task 要求**在 Phase B 落地前实跑该脚本并与 Impact §5 / SC-3 的硬编码数字做机械 diff**——三次数字错误的共同根因是"没有可复现工具", 现在工具有了, 但"工具产出是否真的被拿来核对"仍是人工步骤, 而这正是三次错误里唯二没被检查过的环节(工具本身若被 `sed` 之类破坏, spec 已有意识写了"须重读确认正则未被破坏"的告诫, 但那条告诫只覆盖"验证脚本", 未覆盖 `corpus_census.py` 本身)。**建议**(Minor, 非阻断): Task 1.8"全量回归"显式加一步"跑 `corpus_census.py`, 输出与 Impact §5/SC-3 硬编码数字 diff, 不一致则阻断"。

## 3. 逐条独立复验 SC-1 / SC-4 / SC-5 / SC-6 / SC-7 / SC-8 / SC-12 / SC-13

**SC-1 (5 条泄漏形态, 独立实现全部复现)**:

```
before=0 after=2 split2:[2,0]  cat /opt/.env; echo hi >/dev/null
before=0 after=2 split2:[0,2]  nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2
before=0 after=2 split2:[2,0]  vault read secret/x; nomad var put p @f >/dev/null
before=0 after=2 split2:[2,0]  nomad var get nomad/jobs/x && echo done >/dev/null
before=0 after=2 split2:[0,2]  nomad var put p1 @f1 >/dev/null || nomad var put p2 @f2
```
5/5, 与 proposal 声称一致。

**SC-2/SC-3 (49+15+5 全量复算, 非抽样)**: 49/49 仍 `exit=2`; 15/15 纯管道改前改后不变; 5 条换行边界不变(4×`2`/1×`0`)。**1 条真边界"KNOWN-LIMIT"用例**(与 SC-1 leak form #2 字面相同)按预期 `0→2` 翻转, 与 Task 1.5 "KNOWN-LIMIT 转正" + Why 段落对该命令的描述**完全自洽**——**注**: proposal Impact 表把该条计入"16 放行"、而 SC-2 正文只写"15 条纯管道"(有意排除这 1 条), 两处数字若不细读容易被误读成矛盾, 实为一致(Minor, 见 §5)。

**SC-4 (quote-aware)**: `ssh find env`(2)/`python -c HTTP wrapper`(2)/新增 fixture(2) 三条改前均一致; 手工切错验证两段均 `exit=0`, 证实"切错必 exit=0"锚点成立。

**SC-5 (分段器单元测试, 10 条数组基数断言)** —— **9/10 通过, 1 条实测证伪**:

```
'a; b'                  -> 2   OK
'a && b'                -> 2   OK
'a || b'                -> 2   OK
'a | b'                 -> 1   OK
"echo ';'"               -> 1   OK (引号内)
'a \; b'                -> 1   OK (转义)
'a\nb'                  -> 1   OK (换行)
'a & b'                 -> 1   OK (单 &)
'a &> f'                -> 1   OK (&> 重定向)
'case x in a) ;; esac'  -> 2   FAIL (spec 断言 1)
```

`case x in a) ;; esac` 若作为 `split_top()` **单函数**的直接输入(SC-5 原文即写"分段器单元测试"), 天真 quote-aware 切分会在 `;;` 的两个 `;` 处各切一刀, 产出 `['case x in a)', 'esac']` 长度 2, 非 spec 断言的 1。§1-§3 的架构本身**从未要求 `split_top()` 感知 case/块结构**——那是 `safe_to_split()` 的职责(该命令确实会被 `safe_to_split()` 正确挡下, 降级到整命令判定, 从不会真的把这条命令喂给 `split_top()`)。所以"1"这个断言值只在**"先过 safe_to_split 网关, 网关挡下就不再调用 split_top"的组合管线(即 `verdict()`)语境下**成立(此时因走 fallback, 观察到的"分段数"概念上等价于1/未分段), 但**不是 `split_top()` 自身的真实返回值**。

**这不是吹毛求疵**: 如果 Phase B 实现者按字面写"调 `split_top("case x in a) ;; esac")`, 断言 `len(result)==1`"这种真正的单元测试, 对一个完全正确、忠实于 §1-§3 架构的实现会**测试失败**(因为 `split_top()` 本该返回长度 2, 由 `safe_to_split()` 负责在更外层挡住这条命令, 不是靠 `split_top()` 自己识别 case 块)。反过来, 若实现者为了让这条单测通过, 往 `split_top()` 里塞 case/块感知逻辑, 就是与"safe_to_split 判块结构、split_top 只管纯语法分段"这一设计分工相悖的重复实现。

**处置建议**(Major): SC-5 该条须明确写清测试层级——要么改成 `verdict("case x in a) ;; esac")` 层面断言"未分段/走 fallback", 要么把断言值改为符合 `split_top()` 真实契约的 `2`(并额外在 SC-6 或某处显式断言 `safe_to_split("case x in a) ;; esac") == False`, 用两个独立断言分别验证两个函数各自的契约, 而不是用一个跨层的数字掩盖两层职责)。

**SC-6 (fail-safe 降级族, 12 条)** —— **独立复验 12/12 皆通过, 但其中 2 条不具备声称的鉴别力**:

```
{ }         before=0 after=0 fallback   OK
( )         before=0 after=0 fallback   OK
for         before=0 after=0 fallback   OK
while       before=0 after=0 fallback   OK
if          before=0 after=0 fallback   OK
[[ && ]]    before=0 after=0 fallback   OK
for((;;))   before=0 after=0 fallback   OK
反引号        before=0 after=0 fallback   OK
$()         before=0 after=0 fallback   OK
heredoc     before=2 after=2 fallback   OK
echo done   before=0 after=0 split2:[0,0]  OK
普通两段      before=0 after=0 split2:[0,0]  OK
```

数字上作者"12/12"的声称经独立实现验证**成立**。但对后 2 条("echo done"/"普通两段"), 实测证实一个更深的问题(见 §4 —— 与题目 3 直接相关): 这两条命令在 split 路径与 fallback 路径下 exit code **恒等**(均为 0), 所以 exit-code 断言**无法**区分"确实走了 split 路径"与"实现有 bug、其实全都退回 fallback"。构造对照实验: 把 `verdict()` 换成一个"永远 fallback, 从不真正 split"的故障版本, 重跑这 12 条, **仍然 12/12 全绿**(因为这 2 条本就是良性命令, 两条路径的 exit code 天然相同)。也就是说, **SC-6 声称的"后 2 条走 split, 证明关键字检测不过度触发"这一鉴别力, 仅靠 exit code 断言实际不成立**——除非实现额外暴露"走了哪条路径"的信号(比如作者原型内部的 `how` 标签), 而这类信号**不在 proposal 定义的任何 SC 里**。

## 4. SC 完整性 — 分支选择本身出错的情形是否被覆盖(题目 3)

fail-safe 降级引入的分支有两个错误方向, 逐一核实是否有 SC 能拦:

**方向 A ("该 split 却 fallback 了", 即 `safe_to_split()` 误判为不可安全分段, 过度保守)**: 用真实故障注入验证——把 `verdict()` 替换为"永远 fallback"的坏实现, 重跑全部相关 SC:

```
SC-1 (5 条泄漏形态): 5/5 FAIL (before=after=0, 断言要求 after=2)  ← 全红, 被抓住
SC-6 后 2 条 (echo done / 普通两段): 仍 2/2 PASS               ← 无法区分, 见 §3
SC-2/SC-3: 仍全绿 (这些用例本就要求"改前改后不变", 恒 fallback 天然满足) ← 无法区分但也不需要区分(它们的契约本就是"不变")
```

**结论**: 「该 split 却 fallback 了」这一故障模式, 就 SC 集合整体而言 **SC-1 是唯一真正的哨兵, 且确实拦得住**(5/5 全红, 无法蒙混); 但 SC-6 的表述("证明关键字检测不过度触发")本身对这个方向**不具备独立鉴别力**——它能通过, 完全是因为 SC-1 在别处已经先报警, 不是因为 SC-6 自己验证了什么。这是一个**测什么/为什么测**脱节的问题: SC-6 后 2 条与其说是在验证"分支选择正确", 不如说是在验证"良性命令不受影响"(这点是真的, 但和它自己写的理由不是一回事)。

**方向 B ("该 fallback 却 split 了", 即 `safe_to_split()` 漏判块结构, 错误地对块命令做切分)**: 同样故障注入验证——把 `safe_to_split()` 恒定改为返回 True(从不降级), 重跑 SC-6 前 10 条:

```
{ }         before=0 after=2  FLIP ← 被抓住
( )         before=0 after=2  FLIP ← 被抓住
for         before=0 after=2  FLIP ← 被抓住
while       before=0 after=2  FLIP ← 被抓住
if          before=0 after=2  FLIP ← 被抓住
[[ && ]]    before=0 after=0  未翻转(巧合安全)
for((;;))   before=0 after=0  未翻转(巧合安全)
反引号        before=0 after=2  FLIP ← 被抓住
$()         before=0 after=2  FLIP ← 被抓住
heredoc     before=2 after=2  未翻转(巧合仍算对)
```

10 条中 7 条会翻转、被 SC-6 抓住(SC-6 的断言是"全部改前改后一致", 只要有 1 条翻转整条 SC 就会红)。**结论**: 方向 B 被 SC-6 前 10 条**真实、有效地**覆盖, 不依赖巧合。

**给出可证伪的更强 fixture (弥补 SC-6 后 2 条的鉴别力缺口)**: 把良性 "echo done" 换成"真泄漏 + done 关键字相邻"的组合, 例如 `cat /opt/.env; echo done >/dev/null`——

```
改前(整体判定): exit=0  (>/dev/null credit 覆盖全命令)
正确 split 实现: exit=2  (segment "cat /opt/.env" 无本段 credit)
"恒 fallback"故障版: exit=0  (与改前相同, 说明它没有真的 split)
```

这条 fixture **真正**具备"走 split 与走 fallback 产生不同 exit code"的鉴别力, 建议 Phase B 用它替换或补充 SC-6 现有的 "echo done" 条目, 使"12/12 已验"这句话名副其实。

## 5. Minor

1. **Impact §表述 "16 放行" 与 SC-2 "15 条纯管道" 的并列容易误读为矛盾**(实为一致, 16=15+1, 那 1 条被 SC-2 有意排除、由 SC-1/Task-1.5 单独覆盖)。建议 Impact 表就地加一句"(其中 1 条即 KNOWN-LIMIT, 归 SC-1/Task-1.5 覆盖, 不入 SC-2 的 15 条'不变'集合)", 避免 Phase B 实现者混淆两个数字的适用范围。
2. **`corpus_census.py` 交付但无回填校验 SC**——见 §2, 建议 Task 1.8 补一步机械 diff。
3. **§3 判定伪代码未显式画出 `guard:ack` 检查的位置**——决策表锁定"`guard:ack` 命令级"且 SC-12 已是可执行、可复现的回归锁(独立复验: 把整条已 ack 命令天真下沉到逐段判定会由 `0` 变 `2`, 与 R2 实测完全吻合, 见下), 但 §3 的核心循环伪代码只写了 pattern+credit, 完全没提 ack 检查该在循环外(命令级一次性)还是循环内(逐段), 纯读伪代码的实现者有一定概率把 ack 检查沿用"compute_credit"的视觉相似性写进循环体内, 从而复现 R2 已经抓过的同一个 bug——SC-12 能在测试阶段兜底抓回来, 不是阻断级问题, 但建议伪代码补一行 `if has_command_level_ack(command): return ALLOW` 放在 `safe_to_split` 判断之前, 从源头消除误写空间。

  独立复验 SC-12 机制(与 R2 一致):
  ```
  整条(含尾部 # guard:ack): exit=0
  天真逐段下沉: seg1 "cat /opt/.env" -> exit=2, seg2 "echo hi # guard:ack:..." -> exit=0
  逐段判定合并结果: exit=2  ← 与 SC-12 要求的"仍 0"相悖, 证实该 bug 真实可复现、SC-12 是有效回归锁
  ```

## 6. SC-8 / SC-13 操作性复核(非阻断)

SC-8 "改前改后同会话各 20 轮取中位数, 增幅 ≤50%, 实测数字写进 spec" 方法学在 R2 已充分验证(相对差 -5%, 远低于阈值), v3 新增的"先 pattern 后 credit"重排进一步降低开销预期, 未发现新问题, 方法本身可操作, 待 Phase B 用真实实现复测。SC-13(`secret-hygiene.md` 计数回填) 机制是机械 grep 比对, 当前 SOT 值为 366(两处一致, 已核实), 断言可执行, 无阻断问题。

## 结论

R2 的唯一 Critical(C-1) 已彻底解决, 三方独立实现三次收敛到同一组数字(65/49/16/15/1), 数字侧可信度已达标。SC-1/SC-2/SC-3/SC-4/SC-7/SC-12/SC-13 逐条独立复验(多数为**全量**而非抽样复核)全部通过, 与 proposal 声称一致。但本轮发现 **2 项新 Major**: (1) SC-5 的 `case x in a) ;; esac`→1 断言与 `split_top()` 的真实契约矛盾(独立实现实测为 2), 需要明确该断言到底测哪一层; (2) SC-6 声称"后 2 条走 split 证明关键字检测不过度触发"缺乏 exit-code 层面的实际鉴别力(故障注入证实"恒 fallback"的坏实现在这 2 条上依然全绿), 且已给出一条真正具备鉴别力的替代 fixture。这两项均范围小、可机械修复, 不影响 v3 "fail-safe 降级"这一核心设计决策的正确性(该决策本身经方向 A/方向 B 两路故障注入验证, 被 SC-1 + SC-6 前 10 条真实覆盖, 非巧合绿)。叠加 R2 遗留 m-1(语料重复)第三次被静默丢弃, 判定 **REVISE**。收口路径明确: 改 SC-5 一条断言的语境归属 + 换/补 SC-6 一条 fixture + 顺手清理语料重复, 均为局部文字修订, 不改变已收敛的核心机制。
