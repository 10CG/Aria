---
verdict: REVISE
agent: tech-lead
round: R2
critical_count: 2
major_count: 5
minor_count: 5
r1_resolved: 7/10
---

# post_spec R2 — secret-guard-nomad-var-put-echo (tech-lead 视角, 复审)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md` (R1 后大改版)
R1 报告: `.aria/audit-reports/post_spec-R1-1785678596308-secret-guard-nomad-var-put-echo-tech-lead.md`

## 核对方法 (全部实跑, 不只读)

1. **实装新设计并对比**: 按 §What 1 的伪代码把 `_pat_scoped_safe` + 新 pattern + 循环内 `continue` 真实打进 `secret-guard.sh` 副本 (scratchpad `variant-r2.sh`), 对 baseline 与变体逐条跑同一命令集 (30+ 形态)。
2. **对 nomad CLI v1.11.2 实机核验 flag 取值域** (`var get/put/list --help`)。
3. 跑全量回归套件: baseline 347/347; 变体 346/347 (唯一 FAIL 是我把 `HOOK=` 指到 scratchpad 导致的 `plugin-root: hooks.json` 结构检查, 行为用例 **347/347 全绿**)。
4. 跨仓 grep 核对 `-out=keys` / ack 文案 / skill 耦合面。

---

## R1 逐条核销 (7/10)

| R1 | 处置 | 核销结论 |
|----|------|---------|
| **C-1** 全局 credit 致 block→allow | §What 1 改 pattern 作用域 `continue` | **已解决** — 实测 R1 列的四条 block→allow 全部消失 (`cat /opt/.env; nomad var put -out=none p @f` = 2, `vault read secret/x -out=none` = 2, SC-9/SC-10 全部符合)。§What 2 也按 R1 要求写成**独立 pattern 条目 + 尾边界** (实测 `nomad var putty p` 不误配)。**但作用域收窄不彻底 → 见 R2-C-2** |
| **M-1** `-out=keys` 对称性 | 纳入本 spec | **文本上已回应, 但采纳了一个不存在的 flag 取值 → 见 R2-C-1** |
| **M-2** 漏 `secret-hygiene.md` | Impact + Tasks 1.5 补上 | **已解决** (Key Deliverables 未同步列出, 见 r2-m-5) |
| **M-3** 六形态假阴 | §Why 表加 2 行 + 显式勘正 + 纳入修复 | **已解决**, 且处置比 R1 建议更进一步 (从"记录残余"升级为"修") |
| **M-4** 备选零记录 | 决策表加 2 行备选 | **部分** — (a) TTY 统一规则 / (c) PostToolUse 已入表; **(b) 知识层 convention 条目未采纳 → 见 R2-M-5** |
| m-1 SC-8 基线 347 | SC-13 已改 347 | 已解决 |
| m-2 doc-mention FP | §What 4 + SC-11 | 已解决 |
| m-3 rule6_note 论证 | 重写为"对象是 hook 非 Skill" | 已解决 (裁定站得住, 见文末) |
| m-4 flag 覆盖残余 | — | **未核销** → r2-m-1 |
| m-5 事故链第 2 环未确认 | — | **未核销且反向加码** → r2-m-2 |

---

## Critical

### R2-C-1 `-out=keys` 不是 nomad 的有效取值 — 豁免表第 2 行 / SC-4 / SC-7 hint / 决策表依据 全部建立在一条会报错的命令上; 本仓 2026-05-20 已记录过这个事实

**位置**: §What 1 豁免表第 2 行 / §Why L44 / 关键决策「`get -out=keys` 对称豁免」/ SC-4 / SC-7 / Impact 文档同步

**真机核验** (nomad v1.11.2, 本机 `/home/dev/.local/bin/nomad`):

```
var get:  -out ( go-template | hcl | json | none | table )
var put:  -out ( go-template | hcl | json | none | table )
var list: -out ( go-template | json | table | terse )
```

**`keys` 不在 get 的取值域里, 也不在 list 的取值域里。** `nomad var get -out=keys <path>` 会被 CLI 拒绝。

更要紧的是: **这个事实本仓早就记录过**, spec 与我的 R1 都没查:

- `docs/handoff/2026-05-20-m5-phase-b-shipped.md:156` — 「`feedback_nomad_var_get_out_keys_flag`: `-out=keys` flag 在 nomad var get 中**不存在**(valid: go-template, hcl, json, none, table); playbook 文字 stale。Rule #7 hygiene 替代方式 = `nomad var get -out=go-template -template='{{range $k,$v := .Items}}{{$k}}{{"\n"}}{{end}}'`。Owner 决定。」
- `aria-orchestrator/docs/glm-5.2-cutover-runbook.md:34` — 「(注: 此 nomad 1.11.2 **不支持 `-out=keys`**, key 名从 python 解析后打印。)」

**先认我 R1 的错**: R1 M-1 直接引 `secret-hygiene.md` §3.3/§3.4 的 `-out=keys` 当"SOT 明文推荐的安全读法", 只实测了 hook 拦不拦, **没对 CLI 核实该命令是否存在**。spec 忠实采纳了这条错误上游 (memory `feedback_spec_inherits_upstream_dec_errors` / `feedback_calibrate_source_of_truth_before_translating` 的原型复现)。R2 纠正: SOT 那三处 (`secret-hygiene.md` L39 / L161-163 / L175) **本身是错的**, 不是"对的规范被 hook 拦了"。

**四处派生后果**:

1. **hint 文案会主动教一条报错命令 (最严重)**。SC-7 要求 get 拦截时 stderr 打印 `-out=keys`。被拦者照抄 → nomad 报 usage error → 再退回不安全写法。**这正是 spec 自己指认的事故第 3 环机制**, spec 用它论证要给正解, 然后在 get 侧给了一个假正解。
2. **§Why L44 的因果断言不成立**。「SOT §3.3/§3.4 两处推荐的正解今天被拦, 这正是事故链第 2→3 环成因」—— 那条命令根本跑不通, 它不可能是操作者的 fallback 起点。
3. **文档同步的 scope 判错**。Impact 说 SOT 只需「补一行说明 `-out=none` 与 redirect 的关系」; 实际必须**订正三处错误示例**, 且订正内容要给出真正可用的替代 (`-out=go-template -template=...` 或 `-out=none` + exit code)。这是 Rule #3 的实质修复, 不是补一行。
4. **get/list 被合并成一条豁免规则, 但两者取值域和泄漏面都不同**。list 的 `-out` 没有 `none`; 且 Nomad list API 返回的是 VariableMetadata (**不含 Items**), 即 `nomad var list` 结构上不回显 value —— SC-5 把它永久锁在 `exit=2`, 锁的是一条纯 FP。一条规则同时管两个命令, 封闭集必然不封闭。

**建议**: get 侧的安全形态改为**实机验证过的**取值 —— 最小可行是 `-out=none` (get 有效, 无输出, 只验存在性); 若要保留"列 key 名"能力, 走 `-out=go-template` + 特定 template 形状 (注意 `-out=go-template` 本身不可整体豁免, 模板能打 `{{$v}}` 即 value)。list 单独裁定 (候选 `-out=terse`, 或把 list 从 pattern 里拆出去)。同步订正 `secret-hygiene.md` 三处 + 检查 `docs/handoff/2026-05-09` / `2026-05-22` 两份 playbook 里的同款过期写法。**任何取值进 spec 前跑一次 `nomad var <sub> --help` 核对。**

---

### R2-C-2 「pattern 作用域」仍是**命令级**判定 — 同一 pattern 在一条命令里出现两次时, 一次安全形态豁免整条; 实测重开 block→allow, 且 SC-9/SC-10/SC-13 三层再次全盲

**位置**: §What 1 / 关键决策「豁免机制」栏「作用域豁免零副作用」/ SC-9 / SC-10 / SC-13

**主张**: `continue` 把 credit 从「全部 pattern」收窄到「本条 pattern」, 这一步是对的 (R1 C-1 已解决)。但 `_pat_scoped_safe "$pat" "$command"` 的第二个入参是**整条命令**, 谓词是"命令里任意位置存在安全 token"。于是收窄只到 pattern 粒度, **没到命令片段粒度** —— 同一条 pattern 在一条复合命令里出现两次时, 第一次带安全 flag 就把第二次一起豁免了。

**实测 (baseline vs 实装变体)**:

| 命令 | baseline | 新设计变体 |
|------|----------|-----------|
| `nomad var get -out=keys p1; nomad var get p2` | **exit=2** | **exit=0** ← block→allow 回归 |
| `nomad var get -out=none p1; nomad var get p2` (C-1 修正后取值, 同样成立) | **exit=2** | **exit=0** |
| `nomad var put -out=none p1 @f1; nomad var put p2 @f2` | exit=0 | exit=0 ← 第二条 put 完全无保护 |
| `nomad var put p1 @f1 && nomad var put -out=none p2 @f2` | exit=0 | exit=0 |

get 那两行是**真回归**(今天拦, ship 后放行); put 那两行是**新增覆盖面被自己的豁免掏空**(spec 的 §What 2 主交付物在这个形态下等于没加)。

**这是 R1 C-1 的同类问题降一级重演, 且防护结构失效方式一模一样**:
- SC-9 测的是**别的 pattern** 不外溢 → 结构上探不到同 pattern 内的外溢;
- SC-10 测的是**跨类复合** (`cat .env; put -out=none` / `get; put -out=none`) → 两个片段属不同 pattern, 同样探不到;
- SC-13 全量回归: 变体行为用例 **347/347 全绿**, 与 baseline 零差异 → 再一次没有鉴别力 (R1 m-1 对旧方案的批评原样适用于新方案)。

**可达性不是理论的**: §What 5 的 hint 会主动教 AI 写 `-out=none`; 一次写多个 var (`nomad var put -out=none a @f1; nomad var put b @f2`) 是极常见形态, 只要 AI 在第二条上漏掉 flag, hook 静默放行, 而 `-out` 在非 TTY 下默认 `json` ⇒ 完整 Items 进上下文 = **本 spec 要防的那次泄漏原样再来一次**。

**建议 (三选一, 按成本递增)**:
1. 谓词从「命令含安全 token」改为「**该 pattern 的每一次出现都带安全 token**」—— bash 可用 `${command//…}` 计数或按 `;`/`&&`/`|` 切片后逐段判 (切片不需完美 shell 解析, 只需保证漏判方向是**拦**);
2. 保守回退: 只在命令里该 pattern **恰好出现一次**时才允许豁免, 出现多次一律拦 (fail-closed, 实现 3 行);
3. 至少把它写进 §遗留 + 加 `KNOWN-LIMIT` 用例 —— 但 get 侧是**已 ship 行为的放宽**, 我不认为可以只记录不处理。
无论选哪条, **SC 必须新增同 pattern 二次出现的反回归断言** (至少 get / put 各一条), 否则第三层防护又是空的。

---

## Major

### R2-M-1 §What 3 的撤销规则是**命令级全局** `has_filter=0`, 与 Impact「三者均为 pattern 作用域」直接矛盾; 它是 C-1 的镜像 (方向安全但同一架构病)

**位置**: §What 3 vs Impact「兼容」栏

- §What 3: 「实现为 has_filter 计算末尾的一条**撤销**规则 (`has_filter=0` 覆写), 作用域限定在含这些 flag 的命令」
- Impact: 「两条豁免与 stderr 撤销规则**均为 pattern 作用域**, 既有放行/拦截行为由 SC-11 全量回归锁保证」

「限定在含这些 flag 的**命令**」= 命令级, 不是 pattern 级。`has_filter` 这一个变量对全部 ~140 条 pattern 一视同仁 —— 这正是 R1 C-1 认定的架构病, 只是这次写的是 0 不是 1。后果举例: `nomad var get p | jq 'keys'; curl -v http://example.com >/dev/null` 会因为末尾那个无关的 `curl -v` 把前半段的 jq keys credit 一并撤销 → 拦。方向是 fail-safe (过拦), 所以不是 Critical, 但:

(a) Impact 那句是**事实错误**, 会让 owner 以为三处改动同构;
(b) SC 集合没有任何一条覆盖"撤销规则跨 pattern 撤销无关 credit"的 FP 面;
(c) `-v` 这个 token 与既有 `grep -v` credit 规则 (`secret-guard.sh:361`) 抢同一个字符串 —— 若谓词不锚定到 curl/wget 语境, 既有用例 `curl http://nomad/v1/var/x | grep -v secret` (测试 L273, expected 0) 会转红。这条**已有测试是锁**, 属地雷不是漏洞, 但 §What 3 的实现约束里必须写死"锚定 curl 语境", 别留给实施者临场判断。

**建议**: Impact 那句改为「两条豁免是 pattern 作用域; stderr 撤销规则是**命令级** has_filter 覆写 (过拦方向), 已知会跨 pattern 撤销无关 credit, 作为已知代价接受」; §What 3 补实现约束「`-v` 须锚定 curl/wget 命令语境」+ 加一条 SC 锁 `| grep -v` credit 不受影响。

### R2-M-2 stderr 假阴家族只修了 2 个成员, 其余实测同样假阴; 且「须有 `2>&1`」这个判据本身会被 `2>&1 >/dev/null` 的顺序陷阱骗过

**位置**: §What 3 / SC-6

live hook 实测 (全部 **exit=0 放行**, 全部与 SC-6 修的两条同源):

| 命令 | baseline | SC-6 覆盖? |
|------|----------|-----------|
| `curl -v … --data-binary @f >/dev/null` | 0 | ✅ 已列 |
| `curl --trace-ascii - … >/dev/null` | 0 | ✅ 已列 |
| `curl **--verbose** … >/dev/null` | 0 | ❌ (`-v` 的长形式, 一个 token 之差) |
| `curl **-vv** … >/dev/null` | 0 | ❌ |
| `curl **--trace** - … >/dev/null` | 0 | ❌ (§What 3 正文提了 `--trace`, SC 没测) |
| `curl -v … **-o /dev/null**` | 0 | ❌ (另一条 stdout-only credit 路径, `secret-guard.sh:390`) |
| `curl -v … **2>&1 >/dev/null**` | 0 | ❌ **且判据会给错误 credit** |

最后一行是硬伤: shell 里 `2>&1 >/dev/null` 的语义是「stderr 复制到**当时的** stdout (= 流向 Claude 的管道), 然后才把 stdout 挪去 /dev/null」—— **stderr 根本没被挡住**。而 §What 3 的判据写的是「须 `2>&1` 到 /dev/null 或 `&>/dev/null` 才算」, 一个朴素的"命令含 `2>&1`"检查在这条命令上会判定"已挡住" → 保留 credit → 假阴原样保留。一个专治 redirect 误解的 spec, 判据里再踩一次 redirect 顺序, 值得当场写死。

**建议**: §What 3 的 flag 集合枚举全变体 (`-v` / `-vv…` / `--verbose` / `--trace` / `--trace-ascii` / `--trace-time`, 并说明 `-o /dev/null` 与 `>/dev/null` 同属 stdout-only); 判据显式写「`2>&1` 必须出现在 stdout 重定向**之后**才算挡住 stderr」, SC-6 把上表 5 个未覆盖行全部补进去 (含一条 `2>&1 >/dev/null` 应 exit=2 的反向断言)。

### R2-M-3 `-out=none` 豁免对 `-verbose` 无判别 — nomad 官方 help 明写它把信息送 stderr, 即 spec 一边修 curl 的 stderr 假阴, 一边在自己新开的豁免口上留同类未验证面

**位置**: §What 1 豁免表第 1 行 / §Why「走 stderr 的是 `-verbose` 档」

`nomad var put --help` 原文:

```
-verbose
   Provides additional information via standard error to preserve standard
   output (stdout) for redirected output.
```

spec 自己在 §Why 里点名「走 stderr 的是 `-verbose` 档」, 又在 §What 3 花一整节修「stderr 通道 + stdout-only redirect = 假阴」, 却让 `-out=none` 的豁免**无条件成立**: 实测变体 `nomad var put -out=none -verbose p @f` → **exit=0**。`-out=none` 与 `-verbose` 同时给出时 nomad 到底往 stderr 写什么 (仅状态行? 还是变量内容?) —— proposal 没查, 我在无 server 环境下也无法定论。**未定论就不能给无条件豁免**, 这与 §What 3 的立场自相矛盾。

**建议**: (a) 实机验证 `nomad var put -out=none -verbose` 的 stderr 内容 (对一个丢弃用 var 跑一次, 输出按 Rule #7 redirect, 只看有无 Items 字样); (b) 在验证前, 豁免谓词按 fail-closed 加合取项 —— 命令含 `-verbose` 时**不给**豁免; (c) SC 加一条锁定。

### R2-M-4 §What 4 FP 守卫的范围理由被 §What 1 自身证伪; 且守卫谓词按现描述会造出一条"文本工具起始 = 可执行绕过"的新口子

**位置**: §What 4「范围限定」/ 关键决策「FP 守卫范围」栏

**(a) 理由自相矛盾**。排除既有条的理由写的是「修既有 `(get|list)` 条会改变已 ship 行为 (可能有人依赖现拦截), 属独立裁量」。但 **§What 1 已经在改同一条既有 pattern 的已 ship 行为了** —— 给 `(get|list)` 加 `-out=keys` 豁免, 实测 base=2 → variant=0。同一条 pattern, 放宽 A 说"有 SOT 依据所以做", 放宽 B 说"会改已 ship 行为所以不做", 而 A 的 SOT 依据经 R2-C-1 已证伪。裁定结论我不反对 (缩小 diff 面是合理的), 但**理由必须换一个站得住的**, 否则这个先例会被后续 cycle 引用成"想做就说有依据, 不想做就说改了已 ship 行为"。

顺带: §Why 的 dogfood 实证 1 和 3 全是 **get 侧** FP (`nomad var get --help` 被拦、审计测试命令被拦), 即 spec 亲历的 FP 痛点全在被排除的那一侧, 而修的是没人抱怨过的 put 侧。这一点应在 §遗留写明白, 别让读者以为 dogfood 痛点已解决。

**(b) 守卫谓词本身有洞**。现描述 = 「命令以 `grep`/`rg`/`echo`/`git commit -m`/`cat <<` 起始且该串出现在**引号内**时不拦」。`echo "$(nomad var put p @f)"` 完全满足这个描述 —— 以 echo 起始、串在引号内 —— 但它**真的执行**那条 put, 且 `$(...)` 会把渲染出的 JSON 直接 echo 出来。同类: `` echo `nomad var get p` ``、`git commit -m "$(nomad var get p)"`。守卫必须显式排除引号内含命令替换 (`$(` / 反引号) 的情形。

**现成先例可抄**: 同 plugin 的 `aria/hooks/host-docker-logout-guard.sh` 已有成熟的"提及 vs 执行"处理 (BLOCKED 文案 L159-161: 「writing prose that merely mentions these words is not blocked; only an ssh/scp command aimed at a heavy host is」), §What 4 应引用它并对齐实现手法, 而不是只引 `#69`。

### R2-M-5 R1 M-4(b) 的知识层 convention 条目被静默丢弃; 而 C-1 又证明 SOT 侧真正需要的是**订正**不是"补一行"

**位置**: 关键决策「备选」两行 / Impact 文档同步 / Tasks 1.5

R1 M-4 给了三条, spec 采纳了 (a) TTY 统一规则否决 和 (c) PostToolUse 否决 —— 这两条**论证都成立**, 我复核认可 (见文末)。但 (b)「可统一的是知识层, 不是规则层」被 R1 明确标为**采纳**, 却在新 proposal 里没有任何落点: Tasks 1.5 只写「§3.4 补 `-out=none` 关系说明」, 是纯 nomad 专用的一句。

结果是本 spec 的全部交付仍然是 nomad 专用正则, ship 完「Claude Code 的 Bash 下 stdout 恒为 pipe ⇒ 凡默认输出档随 isatty 变化的 CLI 在此环境下可能输出**更多**」这条唯一可复用的知识仍然只沉在一条 regex 里。而 R2-C-1 又表明 SOT 侧的工作量本来就比 spec 估的大 (三处错误示例要订正), 顺手把这条通用条目写进同一次 SOT 编辑, 边际成本接近零。

**建议**: Tasks 1.5 改为「`secret-hygiene.md` 订正 `-out=keys` 三处 (L39 / §3.3 / §3.4) + 新增一条通用条目 (isatty 默认档) + 补 `-out=none` 与 redirect 的关系」, Impact 的跨仓同步面同步更新。

---

## Minor

### r2-m-1 R1 m-4 未核销: `-out=none -out=json` 实测仍放行, 决策表残余清单仍只列"注释伪造"
Go flag 后者胜出, 实测新设计变体 `nomad var put -out=none -out=json p @f` → **exit=0** (渲染完整 JSON)。R1 已点名要求写进决策表的残余清单, 新版仍无一字。危害等级不高 (需主动构造), 但现在 `-out=none` 是 spec **主推**的 credit 路径, 它的唯一逃逸面不记录, 未来读者会以为该 credit 无残余。

### r2-m-2 R1 m-5 未核销, 且反向加码 — 事故第 2 环仍未确认, 新版却给出了一个更强的未验证因果断言
triage `deviation_note` 已认定 issue 叙述的第 2 环 (带 `>/dev/null` 的 curl PUT 被拦) 在 v1.56.1 / v1.65.1 都不成立。新版 §Why L44 不但没标记开放项, 反而写下「SOT §3.3/§3.4 两处推荐 `nomad var get -out=keys` … **这正是 #170 事故链第 2→3 环的成因**」—— 而 R2-C-1 已证该命令跑不通, 它不可能是事故里的实际触发形态。考虑到 ship 后要给 #170 发 close comment, 这句会被引用出去。建议改为可核验的表述: 第 2 环真实触发形态**推定**为无 redirect 的写向 PUT (§Why 表第 3 行), 该拦截经核实正确; issue 原文引用的带 redirect 版本从未被拦, 属复述失真; 若无法确认, 显式标 OPEN。

### r2-m-3 ack 文案勘正只覆盖 secret-guard.sh, 同 plugin 的姊妹 hook 与 README 携带同一句错文案
`# guard:ack: <reason ≥ 8 non-whitespace chars>` 这句(与实现「首 token ≥8 连续非空白」不符)在非测试文件里共 6 处 3 文件:
`aria/hooks/secret-guard.sh` L61 / L314 / L679 (§What 6 覆盖), 以及 **`aria/hooks/host-docker-logout-guard.sh` L63 (注释) + L157 (运行时 BLOCKED 文案)** —— 该 hook L127 用的是**逐字相同的正则**, 即同一个"逃生门在合法理由下失效"的坑; 另有 **`aria/README.md:147`** (发布 5 文件同步面之一, i18n `README.zh.md` 同理)。纯文本修正零行为风险, 同 cycle 一起改的成本约 4 行。实测复核: `# guard:ack: reading CLI help text only, no secret access` → exit=2; 把首词换成 `inspecting` → exit=0。

### r2-m-4 SC-12 后半不可证伪, 缺负向锚点
「文案 grep 断言其描述与实现一致」—— grep 只能断言文本写了什么, 无法断言它与实现一致 (两边都可能错)。可证伪的写法是加一条**负向**用例: 首 token 7 字符但总长 ≥8 的 ack (如上条实测的 `reading …`) 对 put 拦截**仍 exit=2** —— 这才把"文案现在描述的语义"锁死在实现上。

### r2-m-5 Key Deliverables 与 Impact/Tasks 不一致; SC-5 把一条纯 FP 永久锁死
(a) Key Deliverables 只列 2 个文件 (`secret-guard.sh` + 其测试), 而 Impact 与 Tasks 1.5 都含 `standards/conventions/secret-hygiene.md` (跨仓 co-land) —— R1 M-2 要求的正是"Key Deliverables 增列", 请补齐, 否则实施者按 Key Deliverables 干活会漏掉跨仓项。
(b) SC-5 把 `nomad var list` 锁在「恒 exit=2 (改前改后一致)」。Nomad list API 返回 VariableMetadata (**不含 Items**), 即 list 结构上不回显 value —— 这条断言把一个纯 FP 固化进回归套件。与 R2-C-1 第 4 点合并处理 (get / list 分开裁定)。

---

## 我复核后认可成立的部分 (不构成 finding)

- **pattern 作用域 `continue` 的主设计正确**, 且实装后 R1 C-1 列的四条 block→allow 全部消失、SC-9/SC-10 实测通过、尾边界实测有效 (`nomad var putty` 不误配)。R2-C-2 是这个方向的**收窄不彻底**, 不是方向错误 —— 不要因为 C-2 回退到全局 credit。
- **备选「TTY 类统一规则」否决成立**: 每个 CLI 的 flag 名/默认值/取值域各异 (本 R2 亲测: 同一个 nomad 的 get / put / list 三个子命令 `-out` 取值域就三样), 统一判别式只能退化成一张 CLI 表。
- **备选「PostToolUse 替代」否决成立**: PostToolUse 在工具执行之后运行, 值已进 transcript, 只能告警不能阻断; 保留为纵深的措辞恰当。建议补一句依据来源 (Claude Code hook 契约中 PostToolUse 无 output 改写字段), 让下一个 cycle 不必重新论证。
- **rule6_note 选定「Rule #10 白名单第四类」站得住**。核实: `skill-benchmark-exemption.md` 全文四分表逐行主语都是 Skill 内容 (SKILL.md / `references/*` / description); 本 cycle 交付面 = `hooks/*.sh` + `hooks/tests/*` + `standards/*.md`, 跨仓 grep 确认**零 SKILL.md 改动**, 与 secret-guard 有耦合的 `aria-doctor` / `state-scanner` 只消费"hook 装没装"的安装态, 不消费其 pattern 语义。「审的对象整个未产生」成立。一条限定建议: rule6_note 已写「若未来变更触及任何 SKILL.md 须重新判定」, 再补一句「本 cycle 的 `aria/README.md` 改动 (若采纳 r2-m-3) 属发布同步面文档, 不改变本判定」, 把边界钉死。
- **§What 5 条件 hint (`$pattern_hint`) 的设计正确且可实现** —— 匹配循环内 `$pat` 在 heredoc 作用域可见 (`secret-guard.sh:648-682`), SC-8 的负向断言是合格锚点。**但 hint 的内容依赖 R2-C-1 先修正**, 否则锁死的是一句错建议。
- **SC-3 的 `2>/dev/null` 仍 exit=2 判定与 R2-C-10 语义一致**, 实测成立。
- **SC-14 用 KNOWN-LIMIT 命名锁定既有架构限制**是好做法, 建议 R2-C-2 若走"只记录"路线也用同一手法 (但 get 侧是放宽已 ship 行为, 我不建议只记录)。
