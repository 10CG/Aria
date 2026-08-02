---
verdict: REVISE
agent: tech-lead
round: R1
critical_count: 1
major_count: 4
minor_count: 5
---

# post_spec R1 — secret-guard-nomad-var-put-echo (tech-lead 视角)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md`
视角: 架构/决策合理性 · scope 裁定 · 更根本方案 · credit 作用域取舍

## 核对方法 (不只读, 全部实跑)

1. 逐行读 `aria/hooks/secret-guard.sh` (688 行全文) + `aria/hooks/tests/secret-guard.test.sh` (737 行) + `.aria/triage-report.json`。
2. 对 live hook 跑 baseline 行为探针 (30+ 条命令形态)。
3. **构造两个实现变体并实测**, 存放于 scratchpad:
   - `变体 A` = proposal §What.1+2 字面实现 (新 pattern + `-out=none` 语境守卫写进全局 `has_filter`)
   - `变体 B` = 备选实现 (新 pattern + **pattern 作用域豁免**, 不碰全局 `has_filter`)
   两者各跑全部 SC 对应命令 + 既有全量回归套件。
4. 核对 proposal 引用的行号与 `standards/conventions/secret-hygiene.md` (Rule #7 SOT)。

**行号引用核对结果 — 全部正确**: `nomad var (get|list)` 确在 `secret-guard.sh:406`; threat model 在 L4-44 (proposal 说 L14-24 指的是「What this hook is NOT」段, 精确为 L14-25, 可接受); has_filter 段 L318-399; risky_patterns 起 L402; 匹配循环 + BLOCKED heredoc L648-688。测试文件 `L56-59` 的 4 条 `/v1/var/` 用例确实全是读向 (`curl` GET ×3 + `wget -O-`), proposal 该主张成立。
**6 形态表核对 — 实测与 proposal 完全一致** (3 放行 / 3 拦, 加 `-d` argv 形态拦)。
**版本核对**: `aria/.claude-plugin/plugin.json` = `1.65.1` ⇒ PATCH 到 `1.65.2` 正确 (CLAUDE.md「项目状态」段写 v1.65.0 是该段自身过期, 与本 spec 无关)。

---

## Critical

### C-1 `-out=none` 写进全局 `has_filter` 会把 4 类既有 BLOCK 变成 ALLOW; 语境守卫没有实现它声称的性质; SC-9/SC-1/SC-8 全部测不到

**位置**: proposal §What.2 / 关键决策「`-out=none` credit 作用域」/ SC-9 / SC-10 / Impact「只放宽不收紧 ⇒ 既有放行行为不变」

**主张**: 决策把取舍轴设成「全局 credit vs nomad-put 语境守卫」, 但这是**错的轴**。真正的轴是「污染全局 `has_filter` vs 只豁免被命中的那条 pattern」。语境守卫仍然落在 `has_filter=1` 上, 而 `has_filter` 在匹配循环 (`secret-guard.sh:653`) 里对**全部 ~100 条 pattern 一视同仁**。结果是: 命令串里只要出现 `nomad var put` + `-out=none` 两个**字面子串**, 同一条命令里任何其他 secret 读取全部解除拦截。

**真代码证据 (变体 A 实测 vs baseline)** — 四条 block→allow 回归:

| 命令 | baseline | 变体 A |
|------|----------|--------|
| `nomad var get nomad/jobs/a && nomad var put -out=none nomad/jobs/b @f` | **exit=2** | exit=0 |
| `cat /opt/.env && nomad var put -out=none x @f` | **exit=2** | exit=0 |
| `curl http://nomad/v1/var/x ; nomad var put -out=none y @f` | **exit=2** | exit=0 |
| `echo "use nomad var put -out=none" ; cat /opt/.env` | **exit=2** | exit=0 |

第 3 行是 hook 的旗舰规则 (2026-05-16 事故原型 `/v1/var/` 读) 被解除; 第 4 行的 `nomad var put -out=none` **整串在 echo 的字符串里**, 根本没有 nomad 调用 —— 这直接证伪决策栏的核心论证「**必须加语境守卫**: 无守卫的全局 credit 会让 `-out=none` 变成通用绕过词」。加了守卫它**依然是**通用绕过词, 只是把入场券从「打 `-out=none`」抬到「打 `nomad var put ... -out=none`」, 而这串正是 hint 文案 (§What.4) 主动教给 AI 的。

**三处派生问题**:

1. **SC-10 把新回归当既有限制锁死**。proposal 说复合命令获 credit 是「既有 has_filter 架构对复合命令的通病 (所有 credit 皆然), 不在本 spec 收口」。前半句结构上成立 (baseline 实测 `cat /opt/.env && ls >/dev/null` 确已 exit=0), **但 SC-10 那条具体命令今天是 exit=2**, 本 spec 之后才变 exit=0。它不是「记录既有限制」, 是**新开的洞**, 而 SC-10 用 `expected=0` 把它写进回归套件永久固化。
2. **Impact 表述失真**。「`-out=none` credit 只放宽不收紧 ⇒ 既有放行行为不变」—— 既有**放行**行为确实不变, 但既有**拦截**行为被放宽了, 而这正是安全 hook 唯一要守的方向。Impact 段没有一个字提到 block→allow 的存在。
3. **SC 集合对该回归零覆盖**。SC-9 三条探针全都不含 `nomad var put` 子串, 结构上探不到守卫失效; SC-1 六条 curl 形态与 `-out=none` 无交集 (实测两变体行为一致); **SC-8「全量回归全绿」也没有鉴别力 —— 变体 A 与变体 B 都是 347/347 PASS**。所以本 spec 的三层回归保护对它自己引入的最大风险全盲。

**存在更简且严格更优的实现 (已实测)**。`secret-guard.sh:648-686` 的循环里 `$pat` 是可见的, 做 pattern 作用域豁免只需在 `if [[ $has_filter -eq 0 ]]` 之前加两行:

```bash
if [[ "$pat" == 'nomad[[:space:]]+var[[:space:]]+put' && $nomad_put_out_none -eq 1 ]]; then
  continue
fi
```

变体 B 实测结果: SC-2/3/4/5/6/9 全部符合 spec 预期, **上表四条 block→allow 全部消失** (仍 exit=2), 既有套件 347/347 绿, 且连 `-out=none` 的 `nomad var put` 合取条件都不再需要 (作用域本身就把 credit 关死在那条 pattern 上, SC-9 变成结构保证而非字符串巧合)。代价比 spec 现方案更低 —— 不必写合取判断。

**建议**: 改 §What.2 为 pattern 作用域豁免; 删除或反转 SC-10 (改为 `expected=2` 并新增三条 block→allow 反回归断言); Impact 增加「本变更是否放宽任何既有拦截」的显式结论。**另外 §What.1 必须明确要求把 `nomad var put` 写成独立 pattern 条目而不是并进 `(get|list)` 的 alternation** —— 一旦并成 `(get|list|put)`, pattern 作用域豁免就会连带豁免 get/list, 这个修法结构上不可用。

---

## Major

### M-1 「安全写法不该被拦」的理由没有对称适用到 `nomad var get -out=keys`, 而那条命令是 Rule #7 SOT 自己的 ✅ 推荐写法, 今天正被 hook 拦

**位置**: proposal §What.2 理由 / SC-6 /「本 spec 不做要求 2」的 scope 边界

**主张**: §What.2 的论证是「`-out=none` 是语义上比 redirect 更强的安全写法, 若不给 credit, 会把最正确的写法也拦掉 —— 那正是 #170 事故链『安全工具把人推向不安全替代』的重演」。这个论证**完全同样地适用于读侧的 `-out=keys`**, 而 spec 不但没做, SC-6 还把「`nomad var get` 仍 exit=2」当作不回归目标固化。

**真代码证据**: `standards/conventions/secret-hygiene.md` §3.4 (L175-177) 把这条写成 ✅ 推荐的验证命令:

```bash
# ✅ 验证 (取 key 名仅): -out=keys 不输出 value
keys=$(nomad var get -out=keys nomad/jobs/myapp 2>/dev/null)
```

实测 live hook: `nomad var get -out=keys nomad/jobs/myapp 2>/dev/null` → **exit=2**; 带 `keys=$(...)` 赋值形态同样 **exit=2**。§3.3 的 Python 等价写法 (L161-167) 也用 `-out=keys` 作为「只读 key 名不读 value」的标准手法。

也就是说: 本项目 Rule #7 的规范 SOT 明文推荐的安全读法, 被本 hook 拦掉, 操作者只能靠 `# guard:ack:` 逃生 —— 这与 spec 指认为事故第 3 环成因的机制**是同一个**, 只是发生在 get 侧。spec 用这个机制论证 put 侧必须给 credit, 却把 get 侧的同款问题留在原地, 属于同一决策理由的非对称适用。

**建议**: 要么把 `-out=keys` (以及 `-out=table` 之外的非渲染值档) 一并纳入 pattern 作用域豁免并加 SC; 要么在 proposal 显式记录「get 侧同类问题已知, 本 spec 不做, 理由 = X, 挂 issue Y」。当前 proposal 对此零字。

### M-2 影响面漏掉 `standards/conventions/secret-hygiene.md` (Rule #7 SOT), 造成 hint 文案与规范 SOT 分叉 (Rule #3)

**位置**: proposal §Key Deliverables / §Impact「影响面: `secret-guard.sh` 单文件 3 处 + 其测试; 零 skill / 零 schema 改动」

**主张**: §What.4 要把 `-out=none  # nomad var put: 不渲染 (优于 redirect)` 写进 BLOCKED 文案, 并称这是「本 spec 的事故预防核心」。但同一件事的规范 SOT 是 `secret-hygiene.md` §3.4, 它现在教的是另一句话:

```bash
# ✅ secret 写入: 全 redirect
nomad var put -force nomad/jobs/myapp KEY="$VAL" >/dev/null 2>&1
```

(实测该命令 baseline 与两变体均 exit=0, 行为无冲突 — 冲突在**教什么**上。) ship 之后, hook 说「`-out=none` 优于 redirect」, 规范 SOT 说「用 `>/dev/null 2>&1`」, 两处对同一操作给不同的首选答案, 且 SOT 里没有 `-out=none` 这个词。这违反不可协商规则 #3 (文档与代码必须同步更新), 也让 §What.4 声称的「被拦者第一时间看到正解」在**读规范的人**那一侧失效。

**建议**: Key Deliverables 增列 `standards/conventions/secret-hygiene.md` §3.4/§3.5 同步 (标注是 standards 子模块变更, 影响 ship 同步面); Impact「零 skill / 零 schema」改为「零 skill, 含 1 处 standards 规范同步」。

### M-3 「不做要求 2」的依据是 6 形态「无假阴无假阳」, 但 `curl -v` + redirect 是实测存在的假阴, 且假阴通道恰是事故本身踩的那条

**位置**: proposal §Why「本 spec 不做 issue 的要求 2」6 形态表 / 关键决策「要求 2 不做」

**主张**: 表里 6 条都是**无 redirect** 或**只测 redirect 的安全形态**, 没有测「危险 flag + redirect」的组合。实测:

- `curl -v -X PUT http://n:4646/v1/var/x --data-binary @f >/dev/null` → **exit=0 (放行)**
- `curl --trace-ascii - -X PUT ... --data-binary @f >/dev/null` → **exit=0 (放行)**

`--trace-ascii -` 的目标是 stdout, 被 `/dev/null` 吞, 放行无害。但 **`curl -v` 的 verbose 输出走 stderr**, `>/dev/null` 只挡 stdout —— 它会把请求/响应 header (含 `X-Nomad-Token:` 一类认证 header) 送进 tool output。这就是 #170 事故本体的同一结构 (「`>/dev/null` 只挡 stdout」), 只是主语从 `nomad var put` 换成 `curl -v`。

这不必然要求本 spec 去修 (可以显式列为已知残余), **但它推翻了「要求 2 关闭」所依赖的『6 形态实测无假阴无假阳』这句结论**。结论应改为「6 形态在测到的范围内无假阴假阳; 危险 flag 与 redirect 组合的形态存在残余假阴 (已枚举: `curl -v` + stdout-only redirect), 该残余属 R2-C-10 stdout-only credit 的既有边界, 不在本 spec 收口」。

**建议**: 修正 §Why 该句措辞 + 表格加一行「危险 flag + redirect」; 关闭要求 2 的裁定本身可保留 (PUT response 含解密 Items 已由官方文档确认, 拦无 redirect 的写向 PUT 正确, 这一点我认同且实测支持)。

### M-4 更根本的方案未评估: PostToolUse `secret-scan.sh` 已实证检出本次泄漏; 「CLI 默认输出档受 isatty 影响」这一类知识没有落到任何 SOT

**位置**: proposal 全文 (无「备选方案」段)

**主张 (直接回应 owner 提的两个问题)**:

**(a) 「hook 层面统一处理 TTY 类问题」不可行, 但结论要写清楚**。`-out` 默认值随 isatty 变化是**每个 CLI 各自的产品决策**, PreToolUse hook 只有命令字符串, 要「统一处理」必须先知道哪些 CLI 有这个行为 —— 那就退化成一张 CLI 表, 与逐命令打补丁同构, 只是换了个容器。所以 spec 选逐命令补丁**没有选错**。但 spec 从未把这个论证写下来, 以致读者 (和下一个撞到同类问题的 cycle) 无从判断这是深思后的取舍还是没想到。

**(b) 真正可统一的是知识层, 不是规则层, 而这一层 spec 空着**。可统一的产物是一条 convention 条目: 「Claude Code 的 Bash 工具下 stdout 恒为 pipe 而非 terminal; 凡默认输出档受 isatty 影响的 CLI, 在非交互档可能输出**更多**内容 (nomad `var put -out` 是已知实例); 写/读 secret 前必须显式指定静默档, 不能依赖『交互下默认不打印』的经验」。放进 `secret-hygiene.md` 的成本是几行, 收益是下一个同类 CLI (不是 nomad 的那个) 在**被写进代码前**就被拦住 —— 这才是本 spec 唯一可复用的资产。当前 §What 的 4 项交付全是 nomad 专用, ship 完知识就沉在一条 regex 里。

**(c) 另一条更根本路径也未评估**: issue 原文写着「PostToolUse secret-scan 检测 2 个 secret-shape, 恰对应 per-run var 的 2 个 Items」—— 即 `aria/hooks/secret-scan.sh` **实际检出了本次泄漏**。而 `secret-guard.sh` 文件头 L20-23 自述「Not a content scanner ... Phase 2 would add PostToolUse hook that regex-scans output ... out of scope」。现实是 Phase 2 已经存在且在这次事故里命中。那么架构问题就变成: 继续无限扩黑名单 (已 ~100 条, 本次 +1), 还是把投资转向已被证明能覆盖未知命令的检测层 (评估其能否 redact 而非仅告警)? 我**不主张**本 spec 改道 —— 一条 pattern 的边际成本远低于改造 scanner, 而且检测层是否真能在值进 context 前拦下需要先核实 Claude Code PostToolUse 的能力边界 (不可凭假设下结论)。但 proposal 连提都没提, 这在一个「安全 hook 覆盖面」类 spec 里是决策记录的缺口。

**建议**: 加一段「备选方案与不选的理由」, 三条各两行 (TTY 统一规则 = 退化成 CLI 表; scanner 转向 = 成本与能力待核实, 另开 issue; 知识层条目 = **采纳**, 并入 M-2 的 secret-hygiene.md 同步)。

---

## Minor

### m-1 SC-8 的基线数字错 7 倍, 且 SC-8 对本 spec 的主要风险无鉴别力
SC-8 写「既有 ~50 用例 + 新增 10」。实测 `bash aria/hooks/tests/secret-guard.test.sh` = **PASS: 347 / 347**。「~50」抄自测试文件 L8 的过期头注释, 不是实测。更要紧的是 (见 C-1): 变体 A 与变体 B **都是 347/347 绿**, 所以 SC-8 无法把「引入 block→allow 回归的实现」与「没引入的实现」区分开, 不能当回归锁使用。建议改 SC-8 为「347 + 新增 N 全绿」并明说它只是不劣化基线, 真正的作用域回归锁由新增的反回归断言承担。

### m-2 新 pattern 会拦文档提及形态, Impact 风险段只提了运维脚本 FP
实测: `grep -rn "nomad var put" docs/` 在变体 A/B 下均 → exit=2。本仓自身已有 10+ 个文件含该串 (含本 spec 的 proposal.md 与将写的测试文件), 实施期间对自己仓库 grep 会被拦。注: `nomad var get` 今天已是同样行为 (`grep -rn "nomad var get" docs/` baseline 即 exit=2), 所以这是**对称扩张而非新类**, 不构成阻断; 但 #69 已有先例把 doc-mention FP 当正式问题处理并加了 ALLOW 守卫用例 (测试 L575-576 `grep -r "X-Vault-Token: " docs/` 必须放行), 项目对该类的立场目前不一致。建议 Impact 风险段补一句 + 加一条记录现状的测试用例。

### m-3 rule6_note 的理由不准确 (结论对, 论证错)
写的是「处方性但作用于 harness 执行层而非 **AI 指令面**」。§What.4 的 hint 文案恰恰**就是** AI 指令面 —— 它的整个存在意义 (proposal 自己写: 「使被拦者第一时间看到正解」) 就是在运行时向 AI 下处方。按 Rule #6「同文件两性质并存时逐 hunk 判」, 这个 hunk 的正确归类是「处方性 · 套件覆盖外」。结论 (不跑 AB) 仍然正确, 但正确理由应是「变更对象是 hook 不是 Skill, Rule #6 的触发条件 (新增 Skill / 改逻辑 / 改 description) 结构上不成立」, 而不是「非 AI 指令面」。后者若被后续 cycle 引用会成为坏先例 (任何 hook 里的 AI 可读文案都能借此免检)。SC-7 的 grep 断言已经是合格的可证伪 fixture, 保留。

### m-4 `-out=none -out=json` 仍获 credit (flag 覆盖残余), 决策表未列
Go flag 后者胜出 ⇒ `nomad var put -out=none -out=json x @f` 实际渲染完整 JSON。实测变体 A → **exit=0**。决策表「credit 串伪造」栏只列了「写在注释里即可伪造」这一种残余, 未列 flag 覆盖。危害等级与注释伪造同级 (都需要主动构造), 但应写进决策表的残余清单, 否则未来读者会以为 credit 只有注释一个逃逸面。

### m-5 事故链第 2 环的真实触发命令仍未确认, proposal 未标记为开放项
triage `deviation_note` 明确: issue 叙述的「带 `>/dev/null` 的 curl PUT 被拦促使改用 nomad var put」在 v1.56.1 与 v1.65.1 上都不成立 (case-1/case-2 均 exit=0), 「真实被拦的应是某条无 redirect 变体」。proposal §Why 重建了第 3 环的机制 (做得很好, 且与 CLI 文档一致), 但对第 2 环只在 6 形态表里隐含给出答案 (第 3 行「无 redirect → 拦 ✅」), 正文没有一句把它说破。考虑到 Impact 段计划 ship 后给 #170 发 close comment, 建议在 §Why 显式写一句「第 2 环的实际触发形态推定为无 redirect 的 PUT (表第 3 行), 该拦截经核实为正确行为; issue 原文引用的带 redirect 版本从未被拦, 属复述失真」, 让 close comment 有据可引。

---

## 我认同并已核实成立的部分 (不构成 finding, 记录以免下一轮重复质疑)

- **要求 2「读写分离」关闭的裁定站得住**。Nomad PUT response 含解密 Items 是官方行为, 拦无 redirect 的写向 PUT 是正确的; 实测 3 条安全形态放行 + 3 条危险形态拦截, 判据在被测范围内正确。唯一需修的是「无假阴」这句结论的范围 (见 M-3), 裁定本身不必推翻。
- **不写负向 pattern 的决策正确**。bash `[[ =~ ]]` 是 POSIX ERE, 无负向先行断言, 这是硬约束不是偏好; 复用 has_filter 闸门在架构上与既有 ~100 条 pattern 一致。(但见 C-1: 复用「闸门」不等于必须复用「全局标志」。)
- **`KEY=<value>` argv 形态仍要拦的决策正确**。值确已在命令串里拦不回来, 但阻断执行 + 给正解仍有价值, 与既有 `curl -d` 被拦同理。
- **hint 文案必须同步增补的决策正确, 且是本 spec 里最有价值的一项**。事故第 3 环的直接成因是被拦后无正解可循; SC-7 用机械 grep 锁文案是恰当的防漏改手段。
- **PATCH → v1.65.2 的版本判断正确** (plugin.json 实为 1.65.1)。虽然本变更同时新增拦截面与新增 credit token, 按 Aria 约定「bug 修复 = PATCH」且非新增 Skill, PATCH 成立。
- **proposal 引用的所有行号与测试用例区间经逐条核对无误** (详见上文「核对方法」)。
