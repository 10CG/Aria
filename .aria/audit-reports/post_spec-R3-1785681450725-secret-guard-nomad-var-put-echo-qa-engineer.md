---
verdict: REVISE
agent: qa-engineer
round: R3
critical_count: 0
major_count: 1
minor_count: 2
r2_resolved: 5/6
---

# post_spec R3 审计（收敛终验）— secret-guard-nomad-var-put-echo (qa-engineer 视角)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md`
(owner 裁定「缩到最小, 零豁免」后的版本)。只审不改；未修改仓库任何文件。

方法论: 未复用任何"忠实实现"臆造代码 —— 本轮直接对**真实**
`aria/hooks/secret-guard.sh`（改前, HEAD 未打补丁）与一份**逐字**按 proposal §What
唯一改动（新增 1 条 pattern，插入既有 `(get|list)` 同组，零新增逻辑分支）构建的
补丁副本（`/tmp/.../scratchpad/sg-patched.sh`, 未落回仓库）做双侧 exit code 对照。
SC-1~SC-4/SC-6 全部逐条实跑；SC-7 用本机 `nomad v1.11.2` CLI（`NOMAD_ADDR` 指向不可达
地址）验证"flag 解析层先于网络层报错"的方法论是否成立；SC-5 全量回归（347 条）实跑确认
改前基线绿。凡本会话内需要真执行含 `nomad var get/put` 字面文本的探测命令，均按任务指示
用 `# guard:ack: <理由>` 逃生门放行（探针本身不触真实集群/真实密钥）。

## 结论总览

R2 六条中五条已实质核销（含 R2 唯一 Critical `C-1(R2)`）——**已用真实补丁副本实测复现验证**
其对应机制（`_pat_scoped_safe`）在当前零豁免设计里根本不存在，不是仅凭读文档推定。
但发现 1 条新 Major：proposal 自己给出的 SC-4 三条 FP 探针中，有 **2 条**（不是 R2
m-1(R2) 指出的 1 条）在按 proposal 唯一改动字面实现后，实测并不会翻红——与 SC-4 正文
明确写的"改后 exit=2"矛盾。判 REVISE，但修复面窄（仅需替换 SC-4 两条探针命令字面量），
非架构级问题。

## Major

### M-1(R3) — SC-4 三条 FP 探针中有 2 条（grep / echo）未真正触发新 pattern，与 proposal 自己写的"改后 exit=2"矛盾

proposal 原文 §Success Criteria SC-4：

> `grep -rn 'nomad var put' aria/` / `echo "改用 nomad var put"` /
> `git commit -m "fix: nomad var put 回显"` **改后 exit=2**

实测（对`sg-patched.sh`，唯一改动 = 插入
`'nomad[[:space:]]+var[[:space:]]+put([[:space:]]|$)'`，与 proposal §What 逐字一致）：

```
grep -rn 'nomad var put' aria/                 before=0 after=0   ← 与 spec 断言矛盾
echo "改用 nomad var put"                       before=0 after=0   ← 与 spec 断言矛盾
git commit -m "fix: nomad var put 回显"          before=0 after=2   ← 与 spec 断言一致
```

独立用 Python `re.search` 复核（排除 hook 脚本本身逻辑干扰的可能性）同一结论：

```
"grep -rn 'nomad var put' aria/"   -> False (无匹配)
'echo "改用 nomad var put"'         -> False (无匹配)
'git commit -m "fix: nomad var put 回显"' -> True, matched "nomad var put"
```

根因: 新 pattern 尾边界 `put([[:space:]]|$)` 要求 "put" 后紧跟空白或行尾。两条不触发
的探针里，"put" 后紧跟的都是**引号字符**（grep 探针是 `'`，echo 探针是 `"`，均因
"put" 恰好是被引字符串的最后一个词），既非空白也非字符串结尾（命令整体仍在继续），
边界判定不通过。只有 git commit 探针里 "put" 后跟的是空格（"…回显" 前有空格）才命中。

**这不是我新造的问题，是 R2 m-1(R2) 已经点过的同一缺陷类别未被彻底收口、且范围从
1/3 扩大到 2/3**：R2 m-1(R2) 当时只发现 `grep -rn 'nomad var put' aria/`（探针 a）
因引号边界不触发，并给出具体修复建议（换成 `grep -rn "nomad var put -out=none" aria/`
这类 "put" 后跟空格的形态）；R2 判定探针 b（echo）/c（git commit）在其反例实现上
"确实会翻红"。但当前最终版 proposal 的 echo 探针文案（`echo "改用 nomad var put"`）
与 R2 审查时的版本不同 —— "put" 现在正好落在引号收尾前，重新踩中同一颗雷，R2 的
"b 探针没问题"结论对现在这句已经不成立。

**影响**: 若 B.2 把 SC-4 三条断言逐字编码进 `secret-guard.test.sh`（如 SC-1~SC-3/SC-6
那样），针对 grep/echo 两条的 `want=2` 断言会实测得到 `exit=0`，测试立即失败。后果
两种都不理想：(a) 实现者当场发现矛盾、临时改测试期望或改探针文案，产生一次未经审计
记录的 spec 偏移；(b) 更危险的路径——为了让这两条"真的"翻红而放宽尾边界正则（比如
去掉 `([[:space:]]|$)` 要求），会重新打开 R1 backend m-2 已经用真实调用点名过的
`nomad var putty` 误配 FP（SC-3 专门锁定的回归）。两条路径都不该在 B.2 现场臆断，
应在 spec 文本层面先钉死。

**建议**（沿用 R2 已给出且仍适用的修复方向，扩展到第二条探针）：
- 探针 1 改为 `grep -rn "nomad var put -out=none" aria/`（"put" 后有空格，真触发）
- 探针 2 改为在 "put" 后补一个词，如 `echo "改用 nomad var put 命令"` 或
  `echo "nomad var put deprecated, use xxx"`（同样让 "put" 后紧跟空白）
- 或者：明确承认"引号收尾在词法上豁免于尾边界"是**本 spec 尾边界设计的已知子集**，
  把 SC-4 三条里不触发的两条重新标注为"KNOWN-LIMIT: 未触发（预期内, 边界正则收紧的
  副作用）"而不是断言 exit=2 —— 但这样等于承认 FP 覆盖面比正文其余部分描述的更窄，
  需要相应调整 Impact 段"该 FP 已被 SC-4 显式记录现状"这句的准确性。
- 两种修法二选一，但不能保持现状（断言与实现结果矛盾）。

## Minor

### m-1(R3) — Key Deliverables「SC-1~SC-5, 共 14 条断言」区间标注比实际来源多算了 SC-5

逐条相加 SC-1(5) + SC-2(4) + SC-3(1) + SC-4(4，含本轮确认已补的阳性对照) = **14**，
与正文数字精确吻合（相比 R2 时期 "≈24" vs 实需 ~40 的严重错位，本轮**数字本身已收敛
准确** —— m-4(R2) 实质核销）。但区间标注写的是 "SC-1~SC-5"，而 SC-5 本身是「跑现有
347+新增 全量回归」的聚合校验步骤，不贡献独立断言（贡献者精确是 SC-1~SC-4）。建议把
Key Deliverables 该行的区间改成 "SC-1~SC-4"，避免与 SC-5 的性质（回归运行 vs 新断言）
混淆——纯文字精度问题，不影响实现正确性。

### m-2(R3) — §转出 1「影响 140 pattern」的计数在本 spec ship 后即刻过期

已实测确认当前（改前）`risky_patterns` 数组恰好 **140** 条（`bash -c 'source <(...); echo
${#risky_patterns[@]}'` 实测 =140，非估算）。本 spec 唯一改动是再插入 1 条，ship 后
变为 **141** 条。转出 1 描述的"整命令扫描" has_filter 架构缺陷是**通用于列表内任意
pattern**的（不区分具体是哪条），本轮已实测确认新 put pattern 确实落入该既有缺陷面
（两个新复现，均属既有面而非新增暴露类别，见下）：

```
nomad var put p1_secret @f; echo hi >/dev/null        → exit=0（put 侧新实例，架构缺陷既有面）
cat /opt/.env; nomad var put x @f >/dev/null           → exit=0（cat/.env 侧既有实例，put 只是同行）
```

两者都与既有基线复现（`cat /opt/.env; echo hi >/dev/null` → exit=0，改前改后一致；
`vault read x && echo bogus >/dev/null` → exit=0，R1 M2 已记录）同构——**不是新增的
暴露面类别**，只是新 pattern 加入后，架构缺陷覆盖的具体 pattern 数从 140 变 141。
转出 1 的文字本身未随 ship 动态更新这个数字（也不需要精确到每次 pattern 新增都改字），
但建议把 "影响 140 pattern" 改写为 "影响全部 risky_patterns（ship 后 141 条, 含本次
新增）"，避免未来读者误以为新 put pattern 独立于该已知限制之外。

## R2 特别核验：C-1(R2) 与 M-1(R2) 是否真的不再适用（非纸面判断，已实测复现验证）

### C-1(R2)（Critical，`_pat_scoped_safe` 位置盲区）—— 已核销，机制本身已不存在

R2 的 Critical 建立在 proposal 当时给出的 `_pat_scoped_safe "$pat" "$command"` 伪代码
（对每个匹配 pattern 单独判定"命令里有没有该 pattern 家族的安全 token"，逐 pattern
scoped-credit）。当前最终版 proposal **完全删除了这个设计** —— "What" 只剩 1 条
pattern 插入，"命中后走**既有** `has_filter` 闸门，零新增豁免逻辑"。已实测确认
`has_filter` 现有实现里根本没有针对 `-out=none` / `-out=keys` 的任何 credit 分支
（唯一的 credit 来源是 `>/dev/null` / `&>/dev/null` / `-o /dev/null` / jq keys·length·
`{...}` / grep 锚定或 `-v` / sed s·d / cut -d·-f / awk `$N`·`/regex/` / wc -c·l·w /
sha·md5sum，逐条读码确认，无一处提及 `-out=`）。用 C-1(R2) 原始复现命令直接打在
`sg-patched.sh` 上：

```
nomad var put p1_secret @f; nomad var put p2_decoy @f -out=none extra   → before=0 after=2（拦截，非泄漏）
```

不再泄漏——`-out=none extra` 根本不触发任何 has_filter 分支，两个子句都没有真 credit，
两个 `nomad var put` 都因 `has_filter=0` 被拦（含 p2_decoy 自身的 `-out=none` 也一并
被拦，这是 SC-1 第 5 条本来就承诺的"零豁免故 -out=none 单独出现也拦"的预期行为，不是
新问题）。C-1(R2) 的攻击面随着 `_pat_scoped_safe` 设计被完全放弃而一并消失，"转出 1"
对它的处置（划归既有架构面, 本 spec 不新增）成立，本轮用真实补丁副本实测验证，非仅读
文档推定。

### M-1(R2)（Major，stderr 撤销规则与 `grep -v` credit 冲突）—— 已核销，对应设计已整体转出

当前 proposal "What" 完全没有 stderr 撤销规则相关的任何文字（对照§转出 2 "stderr 假阴
家族...转出"）。M-1(R2) 批评的是一个不存在于当前 spec 范围内的设计，随该设计整体转出
而同步核销，无需单独验证 `grep -v` 交互（该交互面在当前 spec 里压根没有被触碰，
`grep -v` credit 逻辑 (`:361`) 未受本 spec 任何改动影响 —— 已用 SC-6/SC-2 系列探针
间接确认 has_filter 各既有分支行为不变）。

## R2 六条核销状态

| 编号 | R2 结论 | R3 核验 | 状态 |
|------|---------|---------|------|
| C-1(R2) | `_pat_scoped_safe` 位置盲区导致同族多次出现绕过 | 机制随设计转向零豁免被完全移除；用 C-1(R2) 原复现命令实测确认不再泄漏（改为正确拦截） | 已核销 |
| M-1(R2) | stderr 撤销规则与 `grep -v` credit 相撞 | 对应设计整体转出（§转出 2），当前 spec 未触碰该交互面 | 已核销 |
| m-1(R2) | SC-11 三条 FP 探针第一条未测到真实 FP 守卫，需阳性对照 | 阳性对照已补（SC-4 新增 `nomad var put <path> @f` 亦 exit=2）；但**原探针本身仍未替换**，且新版本里连第二条（echo）也踩中同一颗雷 → 本轮升级为独立 Major M-1(R3) | 部分核销（并入新 Major，未完全解决） |
| m-2(R2) | SC-2 两条尾边界探针（`-out=nonelegit`/`-out=none-such`）未标注 baseline-failing | 当前 SC-2 已不含这两条探针（缩范围时被移除，非标注修正） | 已核销（items 移除） |
| m-3(R2) | R1 m2（`-out= none` 畸形分隔符过度慷慨）未被新测试收口 | 当前设计零新增 `-out=` 相关 credit 正则，R1 m2 前提本身不再存在 | 已核销（moot） |
| m-4(R2) | "约 24 条" 与逐 SC 加总 ~40 条不匹配 | 当前 "14 条" 与 SC-1~SC-4 精确加总（5+4+1+4=14）吻合，数字已收敛准确（区间标注另有 m-1(R3) 小瑕疵） | 已核销 |

`r2_resolved: 5/6`（m-1(R2) 因阳性对照已补计为"部分"，但根因未清零，不计入完全核销；
其後果并入本轮 M-1(R3)，不重复计数为独立未核销项）。

## SC 完整性核对（任务 3）

零豁免设计下状态空间基本闭合：SC-1(5 baseline-failing) / SC-2(4 既有 credit 不变) /
SC-3(1 尾边界不误配) / SC-4(3 FP 现状 + 1 阳性对照) / SC-5(全量回归) / SC-6(3 读向
不回归) / SC-7(SOT 订正)。"14 条断言" 数字本身准确（见 m-1(R3)），唯一实质缺口是
M-1(R3) 指出的 SC-4 探针文本与实测结果不符，其余 SC 逐条实测（本报告全部命令附实测
输出）与 proposal 标注**完全一致**，包括此前 R1/R2 反复往返的 SC-3 方向、SC-6 读向、
SC-2 credit 语义。

## SC-7 可执行性核验（任务 4，本机 `nomad v1.11.2`, `NOMAD_ADDR` 指向不可达地址）

实测确认 "只验 flag 解析层" 方法论成立、可执行、非空谈：

```
nomad var get -out=json ...   → "dial tcp ...: connect: connection refused"   (flag 通过, 网络层失败)
nomad var get -out=keys ...   → "Invalid value for \"-out\"; valid values are [...]"（flag 层直接拒绝，不发起网络请求）
nomad var put -out=json ...   → "dial tcp ...: connect: connection refused"   (flag 通过, 网络层失败)
nomad var put -force ...      → "dial tcp ...: connect: connection refused"   (flag 通过, 网络层失败)
```

`-out=keys`（订正前的错误写法）与 `-out=json`（订正后写法）在完全相同的不可达
`NOMAD_ADDR` 下产生**不同类别**的错误（flag 校验 vs 网络拨号失败）——证明 nomad CLI
在发起网络请求前先做本地 flag 校验，"不验端到端写入、只验 flag 解析层"是可行且可
判别的验证手段，SC-7 可执行。附带发现：`standards/conventions/secret-hygiene.md`
当前工作区**已有未提交的本地修改**，内容与 proposal §What"附带修复"描述的订正
（`-out=keys` → `-out=json ... | jq '.Items | keys'`）逐字吻合，且该未提交内容本身
经本轮验证 flag 层可解析通过——但 Tasks 1.3 仍显示未勾选、proposal Status 仍是
"Draft"。这是环境/流程层面的观察（work-in-progress 提前落地但未随 spec 状态同步），
不构成本报告的 finding（未被要求审计实现进度），仅供 owner/下一 session 知悉，避免
误判"改动尚未开始"。

## 结论

0 Critical，1 Major（SC-4 三条 FP 探针里有 2 条与实测 exit code 矛盾，且是 R2
m-1(R2) 同类问题范围扩大后的复发，非全新问题类别，修复面窄——只需替换 2 条探针
命令文字或改写为 KNOWN-LIMIT 标注），2 Minor（Key Deliverables 区间标注偏差 /
转出 1 计数随 ship 过期）。R2 六条中五条已用真实补丁副本实测核销（含唯一 Critical，
非纸面推定）。判 REVISE；建议范围限定为 SC-4 两条探针文字修正，不需要重新展开
架构层讨论，B.2 前可快速收敛。
