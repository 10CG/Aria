---
checkpoint: post_spec
round: R6
review_target: v8 (commit 4923380)
spec: secret-guard-per-segment-evaluation
timestamp: 1786404620467
date: 2026-08-10
seat: silent-failure-hunter
seat_id: SFH
lens: 静默失败 / fail-open vs fail-close 方向
verdict: REVISE
critical_count: 3
major_count: 2
minor_count: 3
fail_open_paths: 4
ready_for_a2: no
note: 本席视角前五轮从未应用过; 三条 Critical 全在既往未审的 2→0 方向
---

# R6 · silent-failure-hunter

**先说结论: 逐行 helper 本身经得起打。** 13 条真判据 × 22 条自造对抗串 (含空串 /
裸换行 / 首尾换行 / 反斜杠续行 / `echo` 选项前缀 `-n` `-e` `-E` `-ne`) = 286 组对拍,
**helper 与 grep 0 分歧**, 独立复现 spec 的 0/143 且对抗集更宽。候选 A 无 finding。
问题全部集中在**另一个方向**: 逐段化引入的 2→0。

## SFH-C1 (Critical, fail-open) — §Impact「行为变更 (穷尽声明)」是假的, 漏掉的正好是唯一的 fail-open 类

`:322` 写「**只有一类** —— 可安全分段的 `a; b` / `a && b` / `a || b` 将开始被拦」,
而 `:228` 自己写着「跨段 pattern fail-open … 实证 `set -o posix; set | grep foo` **2→0**」。

实测 (canonical 直调): 两条形态**今天都是 exit=2**, 改后按 spec 均为 0。

**Phase B 正常路径必撞**: §Impact 行为变更段是 Task 1.6 + SC-10 (CHANGELOG) 的**唯一
输入**; SC-10 只要求「行为变更段 + ≥2 条迁移写法示例」, 而迁移写法只对 0→2 类有意义。
⇒ 发布说明告诉用户「变严了, 请这样改写」, 对「以前被拦、现在放行了」只字不提。

次生后果: 「穷尽声明」立在那里, Phase B/C 观察到任何 2→0 都有现成解释框架
(「设计内的预期翻转」)。spec 为 credit 面写了「观察到**任何**差异就是实现 bug」——
**pattern 面缺的正是这句的对偶**。

## SFH-C2 (Critical, fail-open) — SC-7 把一个 fail-open 写成「锁现状」, 且是「转红=好事」型闸门却无处置表

两处硬错:
1. **事实错误**: `:228` 写「本版不兜底, SC-7 **锁现状**」; SC-7 本体要求「两形态**改后均
   exit=0**」。而现状是 **exit=2**。**SC-7 锁的是一个回归, 不是现状。**
2. **Rule #10 死结**: SC-7 是带勾选框的 enabled SC。若某实现碰巧仍拦住 (例如保留一遍
   整命令 pattern 扫描), SC-7 **转红**。注解「转红 = 已收口」是非正式提示,
   **不属于 Rule #10 四类封闭豁免的任何一类** ⇒ Phase B 只剩「卡死」或「自行裁定
   这条不算数」。**与 SC-9b 被修的缺陷完全同型, SC-9b 拿到了三分表, SC-7 没有 ——
   上一轮的修复没做同类扫描。**

## SFH-C3 (Critical, fail-open 闸门失明) — SC-3 对 fail-open 方向结构上零鉴别力

SC-3 是全 spec 唯一名义上守「任一转 0 = 安全回归」的闸。本席按 spec §What.1/§2/§3 写
参考实现 (机械抽取真 141 pattern + 真 13 判据), 扫全 305 条语料:

```
2 -> 0 (FAIL-OPEN regressions): 0
0 -> 2 (intended fix):          1   (KNOWN-LIMIT compound credit leak)
```

**全绿, 但这不是因为面小, 是因为语料里根本没有跨段形态**:
`grep -n 'posix' secret-guard.test.sh` → 无输出。spec 点名的唯一已知实例不在语料里。

跨段可达面不小 —— 机械复算: 能跨顶层 `;`/`&&` 的 pattern (含 `[^|]` 或 `.*`) = **82**,
与转出 1 的「1 条 `.*` + 81 条含 `[^|]`」逐数吻合。但这 82 条的**可达性从未被测量**。

手工构造几分钟即出 (TODAY = canonical, AFTER = 参考实现):
```
2  0   set -o posix; set | grep foo
2  0   set -o posix && set | grep buildid
2  0   kubectl exec mypod --namespace prod; sh -c env
2  0   tar czf x /home/user/.ssh; cat out | ssh remote
2  0   psql -c "select 1"; echo password from users
2  2   dd bs=4k; if=/home/user/.ssh/id_rsa            ← 段2被别的 pattern 独立接住
2  2   curl -s https://example.invalid; echo /v1/var/  ← 同上
```
**5 个不同 pattern 家族**, 而 spec 通篇只列 1 条。后两条证明必须实测不能推理。

⇒ spec 反复引用的「0/305 分歧」对 credit 面成立 (本席复现了), 对 **pattern 面的
fail-open 方向不具证明力** —— 语料在那个方向上是空集。

## SFH-M1 (Major, fail-open) — 新机制任何运行时错误 ⇒ exit 1 ⇒ 不拦 = 完全绕过

`secret-guard.sh:78` = `set -uo pipefail   # NOT -e`。PreToolUse **只有 exit 2 拦截**。
hook 同构脚本实测:
```
A. helper 少传第 2 参数 → $2: unbound variable → exit 1  (不拦)
B. safe_to_split 引用别处 local 的 $nl → nl: unbound → exit 1  (不拦)
```
B 正是 §What.1 规范写法的天然实现陷阱 (`nl=$'\n'` 与 `BLOCK_KW_RE` 分处两个作用域)。

**与本文件自己的纪律直接冲突**: `secret-guard.sh` 有 10 处 `fail-closed` 注释 ——
jq 没装 / JSON 格式错 / 字段数≠4 全部 exit 2。**唯独本 spec 新加的这一大块逻辑挂了却
fail-open**, spec 通篇零字提及内部错误退出码。

## SFH-M2 (Major, fail-open) — `has_filter` 是粘性全局, spec 无「每段重置」规范句

canonical 结构: `has_filter=0` 一次 (`:323`), 随后 13 处 `has_filter=1`。伪代码写
`compute_credit(seg)` 像函数, 但**规范性 Task 文本从未要求做成函数或重置** ——
Task 1.3b 反而写「13 处正则文本一个字节不动」。

照字面最省事的实现 (原地把 `"$command"` 换成 `"$seg"`, 循环外仍只初始化一次)
⇒ 段 1 的 credit 漏给段 2..N ⇒ **`nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2`
即 Aria#170 泄漏形态原封不动**。

关联: SC-1 的「5 条泄漏形态」全 spec **从未枚举**, Phase B 自挑 5 条时完全可能挑成
3 条「风险段在前」的形态, 那样粘性 credit 就漏检。

## SFH-m1/m2/m3 (Minor)

- **m1**: `:49`「不可安全分段的判据 (**引号外**命中任一即降级)」统摄四行, 但只有块字符
  行是引号感知的; `BLOCK_KW_RE` 是普通正则不解析引号 (转出 11 自己承认 `echo '!if x'`
  命中)。方向安全, 但一句涵盖四行的限定词在只对一行成立时就是下一个「两种读法」的种子。
- **m2**: `:499`「helper 无 fork 无 I/O (**bash 5.1+** here-string 走管道)」vs hook 自称
  「bash 3.2+ guaranteed」。低版本 `<<<` 走临时文件 ⇒ −94.8% 与 SC-8 的 ≤50% 闸失去支撑。
  与转出 9 (macOS 自带 bash 3.2) 指向同一批环境, 但转出 9 只立案了正则可移植性。
  **本条未在 bash 3.2 实测, 按推理登记。**
- **m3**: SC-16 反事实只算了转红条数, 未记**故障方向** —— 关键字正则恒假 ⇒
  `safe_to_split` 恒真 ⇒ 一切都切 (回到 v2); 而同一 `[[ =~ ]]` 静默恒假发生在 13 处
  credit 判据上时方向**相反** (helper 返回 1 = 不给 credit = 多拦)。同一故障在两个
  消费点方向相反, 值得写进 spec 一句, 否则 Phase B 排查时第一反应会被误导。

## 我核过、没有问题的项 (显式记录, 免下轮重开)

1. `_sg_line_match` 记录语义: 286 组 **0 分歧**, 对抗集含空串/裸换行/首尾换行/反斜杠续行/纯空白/tab 起首
2. `echo` 选项前缀分歧点**不可达** (只有整条命令恰等于 `-n`/`-e`/`-E`/`-ne` 才触发, 而该 2 字符串不命中任何 pattern 或判据)
3. `# guard:ack` 逐段化后**无新绕过路径** (两处检测在 `:302`/`:311`, 不在 342–397 抽取区间内, 且位于 filter detection 之前)。唯一值得记: 本 spec 关掉「整命令 redirect 毯子」后, ack 成为**唯一剩下的命令级毯子**, 存量弱点相对权重上升
4. 转出 1 的 82 条工作面数字正确 (`[^|]` ∪ `.*` = 82 = 1 + 81)
5. fail-safe 降级路径本身不失效 (credit 换 helper 后在整命令上与 canonical 0 分歧)

## owner 定案异议

无。三条 Critical 全在「不得重开」清单之外 —— 跨段 fail-open 的**存在**是 owner 已知
并接受的 (归转出 1), 本席针对的是它的**声明方式**、**闸门设计**与**测量覆盖**。
