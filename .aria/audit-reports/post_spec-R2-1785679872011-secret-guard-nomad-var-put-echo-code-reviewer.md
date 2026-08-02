---
verdict: REVISE
agent: code-reviewer
round: R2
critical_count: 1
major_count: 5
minor_count: 11
r1_resolved: 11/13
---

# post_spec R2 — secret-guard-nomad-var-put-echo (code-reviewer, convergence 复审)

**审计对象**: `/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md` (R1 后大改版)
**核实手段**: 全量实跑 — 对 47 条命令形态实跑现行 `aria/hooks/secret-guard.sh` 取真实 exit code; 全量跑 `secret-guard.test.sh`; 精确重数 pattern 数组与 `/v1/var/` 用例; 实跑 `nomad var put/get/list --help` 并实测 `-out=keys` 合法性; 实拉 HashiCorp 官方文档 (HTTP 200) 核 PUT response; 经 Forgejo API 核 #170 / aether-plugin#11 / 两条 issuecomment ID; 读 archive 先例 proposal。

---

## Phase 1 — 规范合规性

**判定**: PASS (结构完整; R1 五方 findings 大部分已实质落地; 无阻塞性缺失章节)

---

## Phase 2 — 引用终检 (全部实测)

### 核实为**正确**的新增引用与数字 (记录以免后轮重开)

| 断言 | 核实 | 结果 |
|------|------|------|
| `secret-guard.sh:406` = `nomad[[:space:]]+var[[:space:]]+(get\|list)` | 读第 406 行 | ✅ 逐字一致 |
| `:653` = `if [[ $has_filter -eq 0 ]]` | 读第 653 行 | ✅ 精确 |
| `:654` = BLOCKED heredoc 起始 (`cat >&2 <<EOF`) | 读 654-682 | ✅ 精确, 且确为全局共享 (循环内唯一出口) |
| 「140 条 pattern」 | `risky_patterns` 数组 402-646, bash `${#arr[@]}` = **140** | ✅ (R1 m-2 已闭) |
| 「347 条用例」 | 实跑 → `PASS: 347 / 347` | ✅ (R1 m-1 已闭) |
| 「L56-L418 共 37 处 `/v1/var/`」 | `grep -c` = **37**; 首 = L56, 末 = L418 | ✅ 三个数字全精确 (R1 m-4 已闭) |
| plugin.json SOT = 1.65.1 → v1.65.2 (PATCH) | 读 `.claude-plugin/plugin.json:4` + CHANGELOG `[1.65.1] - 2026-08-01` | ✅ |
| `secret-hygiene.md` §3.3/§3.4 **两处**推荐 `-out=keys` | :163 (§3.3) + :176 (§3.4) | ✅ (另 :39 / :248 也提及, 「两处」偏保守但不错) |
| §3.4 现推荐 `nomad var put … >/dev/null 2>&1` | :173 | ✅ 逐字一致 |
| Nomad 官方文档 URL + 「PUT 响应含解密 Items」 | 实拉 HTTP 200, 原文 "The response body returns the created or updated variable…" + Sample Response 内含明文 `Items` | ✅ 前提证伪成立, 要求 2 关闭正确 |
| `nomad var put -out` help 原文 (v1.11.2) | 实跑 | ✅ 逐字一致 |
| `#69` FP 守卫先例 | `test.sh:568-579` 实存 (`#69 FP: grep X-Vault-Token in docs` 等) | ✅ 先例引用真实 |
| `R2-C-10` 引用 (SC-3) | `secret-guard.sh:322` 注释逐字 | ✅ |
| #170 / aether-plugin#11 / issuecomment-17187 / -17269 | Forgejo API 逐个取回, 两条 comment 均属 issue 170 | ✅ |
| §Why 假阴表 8 行「现行 hook」列 | 逐条实跑 → `0,0,2,2,2,2,0,0` | ✅ **8 行逐条一致**, 末两行假阴属实 |
| SC-1 五形态「改前 exit=0」 | 实跑 → 全 0 | ✅ |
| SC-4「get/list `-out=keys` 改前 exit=2」 | 实跑 → 2,2 | ✅ (hook 行为断言真; 但见 M-1) |
| SC-5 五形态「恒 exit=2」 | 实跑 → 全 2 | ✅ |
| SC-9 三条 / SC-10 两条「exit=2」 | 实跑 → 全 2 | ✅ 反-C-1 锚点成立 |
| SC-14 `cat /opt/.env; echo hi >/dev/null` → 0 | 实跑 | ✅ |
| SC 编号 1-14 | 逐条 | ✅ 连续, 无缺号/无重号 |

### R1 findings 核销 (11/13)

| R1 项 | 状态 | 依据 |
|-------|------|------|
| M-1 SC-1 算术 6 vs 7 | ✅ 已闭 | SC-1 重写为 5 条 nomad put 形态, 无算术分解 |
| M-2 计数「10 条」矛盾 | ❌ **未闭** | 10 → 24, 但 SC 实需 ≈40 (见 M-5) |
| M-3 SC-4 假绿 + `-out` 三档无 SC | ✅ 已闭 | 新 SC-1 含 `-out=json/table/hcl` 必拦 (实测 baseline 0→ 目标 2), 构成机制断言 |
| M-4 FP 面无覆盖 | ✅ 已闭 | 新增 §What 4 + SC-11, 并显式援引 #69 先例 (已核实真实) |
| M-5 SC-10 太弱 | ✅ 已闭 | SC-10 已含跨类 `cat /opt/.env; nomad var put -out=none …` |
| m-1 ~50→347 | ✅ | m-2 ~100→140 | ✅ | m-3 L14-24 | ✅ (整段已删) |
| m-4 `:56-59` 偏窄 | ✅ | m-5 SC-5 真空措辞 | ✅ (SC-3 已明写 baseline-failing) | m-6 list 回归锁 | ✅ |
| m-7 rule6_note 措辞 | ❌ 未闭 (反向加强, 见 m-8) | m-8 issue 收尾张力 | ✅ (已改条件式) |

---

## Critical (必须修复 — 1)

### C-1. `_pat_scoped_safe` 与 FP 守卫都是**命令级**判定, 不是**出现处级** → 同 pattern 复合绕过 (新引入, 无任何 SC)

- 位置: `proposal.md:69-79` (伪码 `_pat_scoped_safe "$pat" "$command"`) / `:98` (§What 4 「命令以 grep/rg/echo/git commit -m/cat << 等文本工具**起始**…时不拦」) / 决策表 `:117` 「作用域豁免**零副作用**」
- 问题: 伪码把**整条 `$command`** 传给 `_pat_scoped_safe`。于是「命令里任意位置出现 `-out=none`」就豁免该 pattern 的**全部**出现处。R1 C-1 (tech-lead) 打掉的是「跨 pattern 泄漏」, 本版把它压缩到了**单 pattern 内**, 但没有消除 —— 同一 pattern 的复合命令仍整体解锁。
- **实测证据** (现行 baseline + 改后语义推演, 三条形态):

| 形态 | baseline 实测 | 本 spec 改后 | 应然 |
|------|--------------|-------------|------|
| `nomad var put -out=none a K=v; nomad var put -out=json b K=v` | 0 | **0** (put 条被豁免 → 第二子句渲染含 Items 的 JSON) | 2 |
| `echo "use -out=none"; nomad var put b K=v` | 0 | **0** (§What 4 守卫: 命令以 echo 起始 ⇒ 直接不拦) | 2 |
| `nomad var get -out=keys a; nomad var get b` | **2** | **0** (get 条被豁免 → 第二子句明文回显) | 2 |

  第三行尤其严重: 它是**从 BLOCK 退化为 ALLOW 的真回归**, 与 R1 C-1 的伤害形态完全同类, 只是触发面从「任意 pattern」缩到「同一 pattern」。
  第二行是 §What 4 的 FP 守卫**自己**造的洞 —— 「以文本工具起始」是命令级前缀判断, 一条 `echo "…"; <真执行>` 即整体放行。
- 为何 Critical: 这是**安全控制**的绕过, 由本 spec 的核心机制新引入; 且 spec 明文断言「零副作用」/「SC-9/SC-10 可证伪」—— 而 SC-9 测的是**别的 pattern**, SC-10 测的是**跨类**复合, 没有一条测**同 pattern 内**复合。整个 SC 集合对这个洞是盲的 (对齐 memory `feedback_multiround_audit_catches_fix_introduced_regression`: 加固防-false-pass 闸时加固本身重开同类 bug)。
- 修法 (任一, 但必须配 SC):
  (a) `_pat_scoped_safe` 改按**出现处**判定 —— 先按 `;` / `&&` / `||` / `|` / 换行切子句, 只有**含该 pattern 匹配的那个子句**自身带安全形态才 `continue`; 同理 FP 守卫按子句判「该子句是否文本工具调用」而非「整条命令是否以文本工具起始」。
  (b) 若判定 (a) 成本过高, 则在决策表**删掉「零副作用」断言**, 改为显式接受, 并按 SC-14 的写法加 `KNOWN-LIMIT` 用例锁住上表三行现状 + §遗留 加一条。
  无论选哪条, 都须新增 SC: 「同 pattern 复合: `put -out=none a; put -out=json b` / `echo "…-out=none"; put b K=v` / `get -out=keys a; get b`」并写明期望值。

---

## Major (应修复 — 5)

### M-1. `-out=keys` **不是合法的 nomad flag 值** —— get 豁免整条分支的前提被证伪

- 位置: `:44` (§Why 「安全形态被拦」) / `:86` (`_pat_scoped_safe` 规则 2) / `:119` (决策表「`get -out=keys` 对称豁免」) / `:166` (SC-4) / `:169` (SC-7 「触发 get 拦截时含 `-out=keys`」) / `:102` (§What 5 `$pattern_hint`)
- **实测** (本机 Nomad v1.11.2, 与 spec 自己引用的版本同一个二进制):

```
$ nomad var get -out=keys <path>
Invalid value for "-out"; valid values are [go-template, hcl, json, none, table]   (exit=1)
$ nomad var list --help  →  -out (go-template | json | table | terse )
```

  即 `get` 的合法值里**没有 `keys`**, `list` 的合法值里**既没有 `keys` 也没有 `none`**。对照组: `-out=none` 通过 flag 校验后才报 `connection refused` (证明报错确实来自 flag 校验而非网络)。
- 连锁后果 (四处):
  1. §Why「SOT 明文推荐的安全写法今天被拦 = 事故成因同构」—— 前提不成立。它不是「安全写法被拦」, 而是 **SOT 自己推荐了一条根本跑不通的命令** (`secret-hygiene.md:39` / `:163` / `:176` / `:248` 四处均需更正)。事故成因同构的论证需要重写或撤回。
  2. `_pat_scoped_safe` 封闭集的第 2 条规则会为一个**永远执行失败的命令形态**开豁免 = 纯死代码。
  3. SC-7 强制 BLOCKED 提示对 get 拦截打印 `-out=keys` ⇒ **hook 会主动教 AI/操作者跑一条非法命令**。这是 AI 指令面缺陷: 提示给了错解, 操作者失败后极可能改用 `-out=json` 或 `2>/dev/null` 等真会泄漏的写法 —— 恰是 §Why 描述的事故链本身。
  4. Task 1.5 「§3.4 补 `-out=none` 关系说明」范围不足: SOT 需要的是**更正 `-out=keys`**, 不是补充说明; 且改动点是 4 处而非 1 处。
- 已实测的**真·可用**替代 (供重写参考, 均现行即 exit=0): `nomad var get -out=json <path> | jq 'keys'` (`:342` jq-keys credit) / `nomad var get <path> | jq keys`。对 `list` 则 `-out=terse`。请对候选逐个跑 `--help` + 实跑校验后再写进 spec (memory `feedback_fix_target_verify_data_vs_code` / `feedback_spec_inherits_upstream_dec_errors`: 据上游文档起草会继承上游的代码级错误)。
- 注: SC-4 的**hook 行为**断言 (改前 exit=2) 实测为真 —— 错的是「该形态值得豁免」这个语义前提, 不是行号/exit code。

### M-2. §Why 假阴表 rows 1-6 **无任何 SC** —— spec 自陈的盲区只闭了一半 (R1 改写引入)

- 位置: `:29-38` (8 行表) vs `:54` (「上表 **8 条**写向行为**零测试锁定** —— 任何人调整 has_filter 都可能无声破坏且无红灯") vs SC 集合
- 逐条核对: SC-6 只覆盖 rows **7-8** (`curl -v … >/dev/null` / `curl --trace-ascii … >/dev/null`)。rows **1-6** (`curl -X PUT … >/dev/null` → 0 / `-o /dev/null` → 0 / 无 redirect → 2 / `-v` 无 redirect → 2 / `--trace-ascii` 无 redirect → 2 / `-d '{"Items":…}'` → 2, **均已实跑确认**) 在 SC-1…SC-14 中**一条都没有**。
- 为何重要: 这是 R1 改写造成的**回退** —— R1 版 SC-1 本来覆盖这 6 条 curl 形态 (我 R1 的 M-1 只是要求改正它的算术), 本版把 SC-1 整条重定向到 nomad put 后, 6 条 curl 形态失去了归属。spec 自己在 §Why 把「零测试锁定」列为立项理由之一, 却在验收面把其中 6/8 留空。而 §What 3 正要动 `has_filter` (M-3), 这 6 条恰恰是它的回归风险面。
- 修法: 补一条 SC (「curl 写向 6 形态回归锁: 2 放行 + 4 拦, 全部改前改后一致」), 期望值直接用上面实测的 `0,0,2,2,2,2`。

### M-3. §What 3 的 stderr 撤销规则**退回命令级全局 `has_filter`** —— 与本 spec 自己的核心设计决策冲突, 且撤销方向零 SC

- 位置: `:94` (「实现为 has_filter 计算末尾的一条**撤销**规则 (`has_filter=0` 覆写), 作用域限定在含这些 flag 的命令」) vs `:58-79` + 决策表 `:117` (「不碰 `has_filter`」「全局 credit 会让任意命令片段关掉全部拦截」)
- 问题: 「作用域限定在含这些 flag 的**命令**」= 命令级 = 就是 §What 1 判定为病根的那个粒度, 只是方向从「授信」翻成「撤信」。撤信方向不造成泄漏 (fail-closed), 但会**跨 pattern 过拦**, 而 SC 集合只有授信方向的锚点 (SC-9/SC-10), 撤销方向一条没有。
- **实测的新 FP 面** (现行 baseline 全 = 0, 按 §What 3 字面实现后会变 2, 且无红灯):
  - `curl -v http://api/health; nomad var get x >/dev/null` — 一条无关的 `curl -v` 健康检查, 撤掉了另一子句的合法 stdout 丢弃
  - `cp -v a b; nomad var get x >/dev/null` — 若规则把裸 `-v` 当匹配 token (spec 只写「`-v` / `--trace*` 类 curl flag」, 未要求 curl 语境), FP 面覆盖 `cp -v`/`rm -v`/`mkdir -v`/`git commit -v` 等极常见形态
  - 唯一被现有套件兜住的是 `| grep -v …` (test `:273` `R4-C-2: grep -v secret invert ALLOW` 期望 0) —— SC-13 会红。其余两类**无兜底**。
- 修法: (a) spec 明写撤销规则的**语境限定** (必须同时命中 curl/wget 调用, 且 `-v`/`--trace*` 属于该调用的 argv, 不接受裸 token 匹配); (b) 补 FP-SC: 上述两条 + `| grep -v` 三条 exit=0; (c) 若无法做到子句级, 至少在决策表登记它与 §What 1 立场的张力, 别让读者以为本 spec 全面消灭了命令级判定。

### M-4. §What 2 的**尾边界**要求 (`nomad var putty`) 没有 SC

- 位置: `:90` (「**须带尾边界** … 无边界会误配 `nomad var putty`」) vs SC 集合
- 实测: `nomad var putty something` 现行 exit=**0**。若实施者把 pattern 写成无尾边界的 `nomad[[:space:]]+var[[:space:]]+put`, 它会变 2 —— 而 SC-1…SC-14 无一条能亮红 (SC-2 的 `-out=nonelegit`/`-out=none-such` 测的是 **`-out` 取值**的尾边界, 不是 **pattern token** 的尾边界, 两者是不同代码位置)。
- 为何重要: 「§What 明写的实现约束 → 无验收锚点」正是 R1 M-3 那类假绿的同构; 这条约束是 R1 backend m-2 专门提出的, 落进 §What 却没落进 SC。
- 修法: SC-2 追加或新开一条 —— `nomad var putty x` / `nomad var putx` **exit=0**。

### M-5. 交付物计数「约 24 条」仍与 SC 集合实需矛盾 (R1 M-2 未闭)

- 位置: `:111` (Key Deliverables「下表逐条, 约 24 条」) / `:155` (Task 1.4「下方 SC 逐条, 约 24 条」)
- 按 SC 文本**自己写死的条数**逐条加总: SC-1(5) + SC-2(2+2) + SC-3(2) + SC-4(2+1) + SC-5(5) + SC-6(2+2) + SC-7(2) + SC-8(3) + SC-9(3) + SC-10(2) + SC-11(3+1) + SC-12(1+1) + SC-14(1) = **约 40**。再加 M-2/M-4 要求补的 (+6 / +2) 会到 ~48。「约 24」低估 40% 以上。
- 相比 R1 (10 → 与 ≈18 矛盾) 已改善, 且新增了「以 SC 逐条为准」的权威锚点 (这一半 R1 修法已采纳), 但数字本身仍错。实施者若按 24 收工, 最可能被砍掉的正是 SC-8/SC-9/SC-10/SC-12 这批唯一的可证伪安全锚点。
- 附带: Key Deliverables 写「**下表**逐条」, 但其下方是 SC 复选框列表, 不存在表格 —— 指代落空。
- 修法: 直接写实数或删掉数字只留「以 SC-1…SC-14 逐条为准」。

---

## Minor (建议修复 — 11)

**m-1. Key Deliverables 漏了 `standards/conventions/secret-hygiene.md`** (`:110-111`)。Tasks 1.5 与 §Impact「ship 同步面: … standards 子模块 1 文件」都有它, 唯独 Key Deliverables 只列 2 个 aria 文件。Rule #3 的文档同步物不应从交付物清单里掉出去。

**m-2. Task 1.5 (跨仓文档同步) 无对应 SC**。SC-1…SC-14 全部指向 hook 行为, 没有一条锚定 `secret-hygiene.md` 的更正落地。配合 M-1 (SOT 4 处需更正), 建议补一条机械 SC (grep SOT 中不再出现 `-out=keys` 推荐 / 出现 `-out=none` 说明)。

**m-3. SC-11 末句「而真执行形态 `nomad var put <path> @f` **仍** exit=2」措辞错** (`:173`)。实测 baseline = **0**, 「仍」不成立 —— 它是 baseline-failing 项, 且与 SC-1a 重复。建议改「改前 exit=0 (FAIL), 改后 exit=2」或直接引用 SC-1。

**m-4. SC-6 整条标 `baseline-failing` 不准** (`:168`)。前两条 (`>/dev/null`) 实测 baseline=0 → 目标 2, 确为 baseline-failing; 后两条 (`>/dev/null 2>&1` / `&>/dev/null`) 实测 baseline **已是 0** 且目标也是 0 = **不回归控制项**。建议分标, 否则 baseline 记录表会出现「期望 FAIL 却 PASS」的噪音。

**m-5. SC-2 未标 baseline-failing 但其后半是** (`:164`)。`-out=nonelegit` / `-out=none-such` 实测 baseline=0 → 目标 2, 属新增 block, 应与 SC-1 同类计入 baseline-failing 集 (rule6_note 的 substitute 证据面也应含它)。

**m-6. SC-13 脚本计数重复** (`:175`)。`hooks/tests/` 下共 6 个 `.test.sh` (crlf-shim / host-docker-logout-guard / jq-crlf-guard / secret-guard / secret-scan / submodule-gate-telemetry)。除 `secret-guard.test.sh` 外「其余 5 个」**已包含** `secret-scan.test.sh`, 所以「`secret-scan.sh` 及其余 5 个」是 6 项里数了 7 次。建议写「`hooks/tests/` 其余 5 个 `.test.sh` 全绿」。

**m-7. §遗留 1「其余 ~140 条 pattern」应为 ~139** (`:138`)。140 是**全量**(已实测), 「其余」需减掉 `(get|list)` 那条。

**m-8. rule6_note 与同文件 archive 先例框定不一致 (R1 m-7 未闭, 且反向加强)** (`:144-148`)。`openspec/archive/2026-06-19-secret-guard-exfil-coverage-iteration/proposal.md:9` 对**同一个 hook** 写的是「deterministic detector skill → structural fixture + unit test corpus + dogfood (per memory `feedback_deterministic_structural_skill_rule6_substitute`); **不**走 /skill-creator AB (hook 非 capability skill)」= substitute 框定; 本 spec 改成「Rule #6 **不适用** — 走 Rule #10 豁免白名单第四类」并据此**免除**「开套件缺口 issue」义务。我理解 R1 有三方 (knowledge/qa/tech-lead) 要求二选一挑明, 本版照办了, 论证也自洽; 但结论与同文件已 ship 先例相反, 且方向是**收缩义务**。按 Rule #10 (「AI 任何自作主张的流程判断必须写进 handoff 请复议」), 建议二者取一: 回到先例的 substitute 措辞, 或保留现措辞但在 handoff 显式挂 owner 复议。实质证据面 (SC-1/2/3/6/11 一批 baseline-failing) 两种框定下都成立, 不影响 Phase B 启动。

**m-9. §Impact issue 收尾仍有轻微张力** (`:134`)。「ship 后 #170 发 close comment」与「关 issue 前须与 owner 确认是否拆独立 issue」并列 —— 「close comment」这个词本身预设了要关。改成「发进展 comment; 是否 close 取决于 owner 对要求 1 的分拆裁定」即可完全消歧。

**m-10. `secret-guard.test.sh:8` 陈旧注释 `Coverage: ~50 cases` 未纳入勘正范围**。SC-13 已用实测 347, 但注释仍是 R1 m-1 的污染源 (它已误导过本 spec 一次)。本 cycle 顺手改一行, 可避免下个 spec 再继承。

**m-11. §Why dogfood 实证可补第 4 例 (本轮 R2 自身)**。本次审计执行 `nomad --version …; nomad var get --help …` 的复合审计命令被真实 hook 拦截 (实测 exit=2, 匹配 `(get|list)` 条) —— 与实证 1 同形态, 且发生在 **R1 之后**, 是 §遗留 1 (既有 get/list 条 FP 面) 的又一次独立复现。加进 §Why 可加强 §遗留 1 单独开 issue 的论据。

---

## 建议 (Recommendations)

1. **先解 M-1 再动 SC 集合** —— `-out=keys` 一旦被替换成真正可执行的 metadata 形态 (实测 `… -out=json <path> \| jq 'keys'` 现行即 exit=0), `_pat_scoped_safe` 的 get 分支可能**整条不需要存在** (既有 jq-keys credit 已覆盖), 从而 §What 1 的封闭集缩到 1 条、SC-4/SC-7 一半、Task 1.5 全部随之简化。这会显著缩小 C-1 的暴露面 (只剩 put 一条 pattern)。建议在 R3 前先做这个前置裁决。
2. **给 `_pat_scoped_safe` 加「子句切分」的显式实现约束** —— 现有的实现约束段 (`:161`, R1 backend M-1 的合取要求) 只管住了「授信不得写成析取」, 管不住「授信作用于整条命令」。补一句「豁免判定的输入必须是**匹配所在子句**而非整条 `$command`」即可同时关掉 C-1 与 §What 4 的 FP-守卫洞。
3. **SC 增设一张覆盖矩阵** (§What 六点 × SC 编号)。本轮逐条对照发现 §What 2 (尾边界) 与 Task 1.5 (SOT 同步) 两处无锚点, 而 §Why 表 6/8 行无锚点 —— 一张矩阵能机械挡住这类遗漏, 成本一行。
4. **SC-3 与 §What 3 的交互需要点名**: `nomad var put … 2>/dev/null` 要求改后 exit=2, 而 §What 3 的撤销规则也在动 stderr 语义。两者是不同代码位置 (前者靠 `:378-388` 既有 R2-C-10 语义 + 新 put pattern, 后者是新增撤销), spec 应说明二者不互相覆盖, 免得实施者合并成一条规则。

---

## 评估

**是否可以继续?**: **REVISE** —— 需修复 C-1 + M-1/M-2 后再进 Phase B (M-3/M-4/M-5 可与 Phase B 首个 commit 同批落, 但须在动代码前定稿)。

**理由**: 这一版的**事实底座质量很高** —— 本轮把新增的每一处行号 (`:406`/`:653`/`:654`)、每一个数字 (140/347/37/L56-L418/v1.65.1)、每一条外部引用 (Nomad 官方文档、两条 issuecomment、#69 先例、`secret-hygiene.md` §3.3/§3.4)、以及 §Why 假阴表 8 行的 exit code 全部实跑/实拉核实, **无一处失真**, R1 的 9 条 minor 闭了 7 条、5 条 Major 闭了 4 条。阻碍集中在两个仍在的语义面: 其一, 新设计的 `_pat_scoped_safe` 与 FP 守卫都在**命令级**而非出现处级判定, 把 R1 C-1 从「跨 pattern」压成「同 pattern」但没消灭它, 且 SC-9/SC-10 结构上测不到 (C-1); 其二, 整条 get 豁免分支建立在 `-out=keys` 是合法安全写法这个**未经实跑的上游假设**上, 而本机同一 Nomad 二进制直接判它 `Invalid value` —— 连带会让 hook 的 BLOCKED 提示教出一条跑不通的命令 (M-1)。加上 §Why 自陈盲区 8 行里 6 行无 SC (M-2), 当前 SC 集合若照原样进 Phase B, 会生成一个**看起来全绿、但对本 spec 两个最大风险面完全无感**的测试集。
