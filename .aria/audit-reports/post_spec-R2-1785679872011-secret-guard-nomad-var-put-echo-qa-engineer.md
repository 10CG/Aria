---
verdict: REVISE
agent: qa-engineer
round: R2
critical_count: 1
major_count: 1
minor_count: 4
r1_resolved: 5/6
---

# post_spec R2 审计 — secret-guard-nomad-var-put-echo (qa-engineer 视角, convergence 复审)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md`
(post_spec R1 六方 findings 落修订版)。只审不改；未修改仓库任何文件。

方法论: 对 R1 六条 finding 逐条核销（文本对照 + 实测）；对现行 `secret-guard.sh`
（改前, HEAD 未打补丁）逐条实测 SC-1~SC-14 全部探针的真实 exit code；并按 proposal
「What」章节 §1 给出的 `_pat_scoped_safe "$pat" "$command"` 伪代码，在
`/tmp/.../scratchpad/sg-faithful.sh`（未落回仓库）构建一份**忠实字面实现**（新增
pattern + helper + loop 接线，均照抄 proposal 原文，未额外发挥），对该实现做穷举
+ 新构造探针验证。所有结论均基于实测 exit code，非推演。

## 结论总览

R1 六条 finding 五条已实质核销（M1/M2/m1/m3/m4）。但本轮基于 proposal 自己给出的
`_pat_scoped_safe` 伪代码构建忠实实现后，**实测发现一个 proposal 自身 SC 集合完全未
覆盖的真实密钥泄漏绕过**：同一 pattern 家族（put 或 get 皆然）在同一复合命令中出现
两次、仅其中一次带安全形态时，整条命令被放行——包括那条**没有**安全形态、货真价实
会回显密钥的那次调用。这不是我的反例实现引入的臆造 bug，是 proposal §What 1 伪代码
签名 `_pat_scoped_safe "$pat" "$command"`（只传"整条命令字符串"，不传匹配位置/次序）
的结构性必然结果——任何忠实该签名的实现都会继承此缺陷。判 REVISE。

## Critical

### C-1(R2) — `_pat_scoped_safe` 整命令扫描对「同 pattern 家族命令内出现两次」无鉴别力，构成真实密钥泄漏绕过

**实测（对忠实实现, `sg-faithful.sh`, 双向顺序、put/get 两侧均复现）：**

```
nomad var put p1_secret @f; nomad var put p2_decoy @f -out=none extra   → exit=0 (泄漏)
nomad var put p2_decoy @f -out=none extra; nomad var put p1_secret @f   → exit=0 (泄漏)
nomad var get p1_secret; nomad var get p2_decoy -out=keys extra          → exit=0 (泄漏)
nomad var get p2_decoy -out=keys extra; nomad var get p1_secret          → exit=0 (泄漏)
```

四条命令里真正执行的 `nomad var put p1_secret @f` / `nomad var get p1_secret` 均**无**
任何安全形态（无 `-out=none` / `-out=keys`），本应被拦——但因为同一条复合命令里**另一个
不相关的 `p2_decoy` 调用**带了安全形态字样，`_pat_scoped_safe` 对整个 `$command` 做
无位置感知的字符串扫描，把这个 credit 错误地泛化到了整条命令，`p1_secret` 那次真实的
不安全调用随之被一并放行。

**根因是 proposal 自己的伪代码签名**（§What 1）：

```bash
if _pat_scoped_safe "$pat" "$command"; then continue; fi
```

传入的是**整条** `$command`，不是"当前触发这条 pattern 的具体子串/位置"。给定这个签名，
`_pat_scoped_safe` 能拿到的信息只有"pattern 家族是谁"+"命令全文里有没有出现对应安全
token"——它结构上无法回答"**这次**匹配是否带着安全形态"，因为它压根不知道"这次"指哪
个位置。这不是我实现草率，是任何忠实该签名的实现的共同上限。

**与既有 §遗留 3 的区别**：§遗留 3 锁定的 `cat /opt/.env; echo hi >/dev/null`（SC-14）
是"跨 pattern 家族"通过 `has_filter` 全局布尔借用 credit——proposal 已知悉且明确记录
为既有架构问题、本 spec 不收口。但本条 C-1(R2) 是**同一 pattern 家族**（put 自己，或
get 自己）在**新引入的 `_pat_scoped_safe`** 机制下的多次出现互相借用——这是本 spec
**新增代码**的行为，不是继承的既有缺陷，proposal 未提及、未纳入 §遗留、也没有对应
KNOWN-LIMIT 锁定。

**SC-9/SC-10 为什么没抓到**：两者都只构造了"两个**不同** pattern 各出现一次"的复合
命令（vault+put / cat.env+put / get+put），验证的是"跨 pattern 身份不外溢"这一个维度
（对应 R1-C-1 的合取判断约束）。没有任何 SC 探针使用"**同一** pattern 出现两次、一次
安全一次不安全"的形态——这正是 C-1(R2) 命中的维度，SC-9/SC-10 结构上覆盖不到。

**建议**：`_pat_scoped_safe` 不能只按"pattern 身份 + 命令全文子串匹配"判定，需要
拿到触发匹配的**具体位置/子串**（例如用 `BASH_REMATCH` 或按 `;`/`&&`/`||`/`|` 切分
命令后逐子句独立判定，与既有 §遗留 3 的"has_filter 命令级全局"问题同源同解——建议
一并在本 spec 内解决，或至少把此形态显式记入 §遗留 + 补一条 SC-15 KNOWN-LIMIT 锁定
现状（参照 SC-14 先例），而不是留白不提。「关键决策表」现在写的"SC-9/SC-10 是该约束
的可证伪锚点"这句话需要改写——它们只锚定了合取判断的**跨 pattern** 一半，不是全部。

## Major

### M-1(R2) — stderr 撤销规则 (§What 3) 的匹配范围在 spec 文本里未定死，存在与既有 `grep -v` filter-credit 规则相撞的风险，零 SC 覆盖

§What 3 原文："这些 flag 出现时不接受纯 stdout redirect 作为 filter...作用域限定在
含这些 flag 的命令"——没有写清楚"这些 flag" 的检测正则是否限定在 `curl` 语境内
（如 `curl[^|]*(-v\b|--trace)`）还是对整条命令做无上下文的 `-v` / `--trace` 子串匹配。

现有代码里 `-v` 已经是一个被合法复用的 filter-credit 触发词——`:361`
`grep -qE '\|[[:space:]]*grep[[:space:]]+(-v|--invert-match)\b'`（"grep -v 判定为
过滤, 已实测 `cat /opt/.env | grep -v FOO` 今天 exit=0）。若新撤销规则的实现不像
既有代码那样把检测严格限定在 `curl` 上下文，而是对整条命令做无上下文 `-v` 子串扫描，
会把 `curl -v <不相关的公网地址> >/dev/null; cat /opt/.env | grep -v SECRET` 这类
命令里、本来靠 `grep -v` 合法拿到的 credit 意外撤销，导致一个此前正常工作、与
nomad/vault 毫无关系的过滤命令被误拦——功能回归，且方向上恰是 spec §Why 反复强调的
"安全写法被拦→操作者被迫走不安全捷径"同一事故模式的变体。

无任何 SC 测试这一交互面（SC-6 只测 curl PUT 自身，不测"curl -v 与另一条不相关的
`grep -v` 过滤命令共处一行"）。鉴于既有代码库对同类风险一贯用严格上下文限定的正则
（`\|[[:space:]]*grep...`），一个谨慎实现者大概率会做对，但 spec 文本没有把这一点
钉死为约束，也没有测试兜底——按项目惯例（R1 M1/M2 同类问题的处置方式），应在
"实现约束"或 §What 3 里明确写死"撤销规则的触发检测须限定在 `curl[^|]*` 语境内，不得
对整条命令做无上下文 `-v` 匹配"，并补 1 条 SC 验证该交互不回归。

## Minor

### m-1(R2) — SC-11 三条 FP 探针中第一条并未真正测到 FP 守卫机制

`grep -rn 'nomad var put' aria/`（proposal 原文探针）今天在**完全不装 FP 守卫**的
反例实现上仍是 exit=0——不是 FP 守卫生效，是因为字符串里 "put" 后紧跟单引号
（非空白、非行尾），新增 pattern 自带的尾边界正则 `put([[:space:]]|$)` 本身就不匹配，
与 §What 4 的 FP 守卫无关。已实测验证 b/c 两条（`echo "..."` / `git commit -m "..."`）
在同一份"无 FP 守卫"反例实现上确实会翻红（exit=2），证明它俩真正需要 FP 守卫、有
鉴别力；只有 a 条是巧合通过。建议把 a 条换成 "put" 后紧跟空白的例子，如
`grep -rn "nomad var put -out=none" aria/`——已实测：无 FP 守卫时 exit=2（翻红，
证明有鉴别力），改前基线 exit=0（与其余同类探针一致，非阻塞）。

### m-2(R2) — SC-2 的两条尾边界探针实为未标注的 baseline-failing

`-out=nonelegit` / `-out=none-such` 两条实测**改前**（put 模式尚不存在）即为
exit=0，需求是**改后** exit=2——结构上与 SC-1 的 0→2 转换完全同类，但 SC-2 整条
未像 SC-1/3/4/6 那样标注 "baseline-failing"，也未被本轮任务列入"标注恒定的
(SC-5/9/10/11)"名单。不影响测试正确性，但破坏了 proposal 对"哪些条目改前即 FAIL"
的标注一致性承诺——未来审计者若只读标注不实测，会漏掉这两条的真实底色。

### m-3(R2) — R1 m2（`-out[=[:space:]]+` 混合分隔符过度慷慨）未被新增测试收口，仍是 open item

R1 minor m2 指出 `-out= none`（等号后跟空格再跟独立 token）在原设计下会被过度慷慨
地判定为安全形态；R1 自己已判定"不可利用、不阻塞发版"。本轮 SC-2 新增了尾边界探针
（`-out=nonelegit`/`-out=none-such`）但**没有**补上 m2 点名的这个具体畸形分隔符形态
探针。维持 R1 的"不阻塞"结论，但记录为仍未闭环，§What 1 的分隔符描述（"`=`或空格
分隔"）仍未精确到能排除这个畸形交叉形态。

### m-4(R2) — SC-13 "约 24 条" 与逐 SC 枚举加总仍有数量落差（R1 code-reviewer 已指出的同类问题未完全收敛）

逐条数 SC-1~SC-14（不含 SC-13 自身，它是"跑现有 347 条全量回归"而非新增断言）列出
的独立断言数：5+4+2+3+5+4+2+3+3+2+4+2+1 ≈ 40 条，显著多于 proposal Key Deliverables
段所写"约 24 条"。不影响正确性（无论最终写成几个 test 函数，只要断言内容对即可），
但延续了 R1 code-reviewer 已经点过的"数量估算与实需不匹配"问题，建议实现时如实登记
真实断言数，不要继续沿用一个明显偏低的估算数字。

## R1 六条核销状态

| 编号 | R1 结论 | R2 核验 | 状态 |
|------|---------|---------|------|
| M1 | SC-7 heredoc 全局污染 | §What 5 改为条件插入 `$pattern_hint`（按当前循环迭代的 `$pat` 选择内容，逐位置精确，无位置歧义问题）+ 新增 SC-8 专测作用域（vault/cat.env/aws 拦截时 stderr 不得含 `-out=` 提示）。设计上可行、无 C-1(R2) 那类整命令扫描问题。 | 已核销 |
| M2 | SC-10 例子弱于决策表跨家族例子 | SC-10 第一条改为 `cat /opt/.env; nomad var put -out=none ...`——`cat .env` 与 `nomad var` 是不同 pattern 家族，属真正跨类复合，非原先的"nomad 内部左右手"同类例子。 | 已核销 |
| m1 | SC-1"回归锁"措辞与实际保护面不符 | 现文写法已改为 "SC-1 (baseline-failing, put 无豁免)"，不再使用"回归锁"框架。 | 已核销 |
| m2 | `-out[=[:space:]]+` 畸形分隔符过度慷慨 | 未被新增探针覆盖（见 m-3(R2)）。R1 自身已判定不阻塞，维持该判定，标记为仍 open。 | 未核销 (non-blocking) |
| m3 | rule6_note 借用第三行措辞但未走三件套 | 现文已重排为"优先陈述不是 Skill 制品"这一结构性理由，明确写"不是走四分表第三行"，消除了措辞混用歧义。 | 已核销 |
| m4 | 缺 guard:ack × put 交互用例 | 新增 SC-12 显式覆盖。 | 已核销 |

`r1_resolved: 5/6`（m2 维持 R1 原判"非阻塞"但未真正闭环，不计入已核销）。

## 结论

新发现 1 条 Critical（`_pat_scoped_safe` 对同 pattern 家族多次出现无位置鉴别力，
构成真实密钥泄漏绕过, 用 proposal 自己的伪代码忠实实现验证复现, put/get 两侧、
双向顺序均命中）+ 1 条 Major（stderr 撤销规则的匹配范围未在文本中钉死, 存在与既有
`grep -v` filter-credit 相撞导致功能回归的风险, 零 SC 覆盖）。R1 六条中五条已实质
核销, 但 R2 引入的新问题比已核销的旧问题更严重——C-1(R2) 直接命中本 spec 存在的
核心理由（防止 #170 同构泄漏）, 判 REVISE。建议：`_pat_scoped_safe` 需要位置/子句
级别的判定能力（切分命令按分隔符逐子句判定，或用 `BASH_REMATCH` 定位），并补
SC-15 类探针锁定"同 pattern 家族多次出现"这一维度；M-1(R2) 需在 §What 3 钉死撤销
规则的匹配上下文并补交互测试；m-1(R2)/m-2(R2)/m-3(R2)/m-4(R2) 供 B.2 实现时参考，
不阻塞（若 owner 判定单独处理数量估算/畸形分隔符可留 §遗留, 但 C-1(R2) 必须在
B.2 前收敛设计, 否则测试再多也测不出这个真实绕过）。
