---
checkpoint: post_spec
round: R1-R2
review_target: proposal.md draft v1 (secret-guard-manifest-precision, Aria#179)
spec: secret-guard-manifest-precision
timestamp: 1787375602111
date: 2026-08-22
seat: A2-qa-engineer
seat_id: A2
lens: SC 可证伪性 / 测试策略
verdict: APPROVE
r1_verdict: REVISE
r1_critical_count: 1
r1_major_count: 2
r1_minor_count: 2
r2_review_target: proposal.md draft v2 (post_spec R1 三席 findings 修订)
r2_verdict: APPROVE
r2_critical_count: 0
r2_major_count: 0
r2_minor_count: 1
r2_note: A2-C1/M1/M2/m1/m2 五条全部在 v2 忠实落地且经实测验证; 唯一残留是 m1(carry) — 「适用面点名含 .env 面」停在文字层, 未被任何 SC 锁定, 不阻断
---

# R1 · A2-qa-engineer

## 实测基线 (只读探针, 命令文本不执行, 对 400f0bc 树)

| SC | 探针 | spec 声称基线 | 实测结果 | 判定 |
|---|---|---|---|---|
| SC-1 | `jq -c '{model, env: (.env // {})}' ~/.claude/settings.json` (Bash 面) | exit 0 (漏报) | **exit 0** | 一致, 真红 |
| SC-2 | `Read {file_path: "~/.claude/settings.json"}` (正确嵌套 tool_input 形状) | exit 0 (漏报) | **exit 0** | 一致, 真红 |
| SC-4 | `grep -oE '(\.bashrc|[^)]*)' aria/hooks/secret-guard.sh` | exit 2 (误报) | **exit 2** | 一致, 真红 (且探针本身把我自己的 Bash 调用也现场误拦了一次, 活体三次复现) |
| SC-5 | `cat ~/.bashrc` | exit 2 (既有拦截) | **exit 2** | 一致, 真绿基线 |

四条基线断言全部经实测验证, 非空谈; SC-1/SC-2/SC-4 是真正的 baseline-failing 红态 (不是恒绿断言)。SC-3/SC-6/SC-7 因目标 pattern 未实现, 无法对当前树实测, 改用静态对照 `_sg_compute_credit` (:306-395) 与 `_sg_judge_one` (:926-973) 逻辑推演, 见下方 findings。

## [A2-C1] (Critical) 前置字符类的落点与 risky_patterns 实际消费路径不匹配 —「行首」成员在多行命令下大概率不生效

spec §What.3 写「仅当敏感名前一字符 ∈ {行首, 空白, `"`, `'`, `=`, `/`, `~`} 时视为路径位置」, 并提醒「⚠️ bash ERE 实现须避 `[[ =~ ]]` 已知坑 (`^` 不锚每行), 沿用 `_sg_line_match` 既有基建」。

但实际的拦截判定路径 `_sg_judge_one()` (:926) 对 `risky_patterns` 数组是直接 `[[ "$seg" =~ $pat ]]`, **不经过 `_sg_line_match`**。`_sg_line_match` 只在 `_sg_compute_credit` 内部被使用。而 shell-rc pattern (:709) 和即将新增的 claude-config pattern, 按 spec 描述都是 `risky_patterns` 数组里的字符串常量, 走的正是前者路径。

实测确认 bash 语义:
```
s=$(printf "foo\nbar"); pat="^bar"
[[ "$s" =~ $pat ]]   # NOT MATCHED — ^ 只锚整个字符串开头, 不锚每行
```
对于多行/heredoc 命令 (`_sg_safe_to_split` 遇到 `<<` 会判定不安全分段, 整条多行命令原样进 `_sg_judge_one ... whole` 模式), 前置字符类里的「行首」分支如果按字面实现为 `^(...)`, 只在敏感名出现在整条命令的第一行开头时生效; 出现在物理第 2/3 行行首的敏感名不会被这个分支识别为「路径位置」——除非实现者改用 `[[:space:]]`(而非字面空格)覆盖 `\n`, 但 spec 没有言明这个选择, 反而明确指向「沿用 `_sg_line_match`」这条实际上根本没接到 `risky_patterns` 判定路径上的基建。

后果: Task 1.3 的落点在「(a) 把前置字符类拼进 risky_patterns 字符串常量, 靠 `[[:space:]]` 隐式兜底行首」还是「(b) 新起一条经 `_sg_line_match` 消费的独立判定通路, 与现有 risky_patterns 主循环脱钩」这两个架构选择间悬而未决。SC-4/SC-5 给出的全部是单行命令 fixture, 测不出这个分歧 — 无论实现者选 (a) 还是选一个「行首」根本没生效的错误实现, 单行 fixture 一样全绿。

**建议**: Task 1.3 明确指定架构落点 (a) 或 (b) 二选一; 若选 (a), SC-4/SC-5 必须补至少一条多行/heredoc 形态的 fixture (敏感名出现在物理第 2 行行首) 来锁定「行首」分支真的生效, 而不是靠空白类恰好兜底。

## [A2-M1] (Major) 前置字符类的作用范围 (哪些 risky_patterns 行) 未点名, SC-6 回归套件测不出越界

Why 段的误报证据只指向 :709 shell-rc 一行; SC-4/SC-5 fixture 也只覆盖这一行 (加新增 claude-config 行)。但 `risky_patterns` 里至少还有以下同构「reader + 敏感名字面量 alternation」形态, 会在 grep/awk 审计 hook 自身规则时产生完全等价的误报, 却完全没被 spec 提及处置方向:

- `:685-687` `.env` / `.envrc` 系列 (`cat[[:space:]]+[^|]*\.env...`)
- `:700` id_rsa / .pem / .key / .p12 / kubeconfig 系列
- `:709-710` shell-rc (本 spec 内, 已覆盖)
- `:741` SSH 远程读取系列

spec 既没说「这 15+ 条 sibling 一并治」也没说「明确排除, 维持现状」。这个边界模糊有两个后果都测不出:
1. 若实现者只焊死在 :709 + 新增 claude-config 两行, 其余同构误报依旧存在但从未被记为已知限 (文档不同步, SC-7 也管不到, 因为 SC-7 只回填 secret-hygiene.md 的计数, 不要求逐条列出未治条目)。
2. 若实现者图省事把前置字符类抽成公共 helper 广泛套用到全部 risky_patterns, 造成大范围行为收窄 (defang) — SC-6「全量既有测试绿」测不出来, 因为回归套件里从未有过针对 `.env`/`id_rsa` 等 sibling 行的「正则字面量位置」误报 fixture (历史上没人复现过, 自然没人写), 没有基线可比对退化。

**建议**: What.3 明确写死「本次改动仅触达 :709 shell-rc 行 + 新增 claude-config 行, 其余同构 alternation 维持现状, 记入已知限」(或反过来明确宽治), 并补一条 SC 断言 sibling 行为在改动前后完全一致 (取一条 `.env` 的字面量位置误报做前后对拍, 而不是假设 SC-6 现成套件能兜底)。

## [A2-M2] (Major) SC-2 探针 JSON 形状与 hook 真实输入契约不一致

spec 原文: 「`{tool_name:"Read", file_path:"~/.claude/settings.json"}` 探针 → exit 2」。这是扁平结构, 但 hook 的字段提取 (:466-487) 走 `.tool_input.file_path`, 必须嵌套在 `tool_input` 键下 (对照既有 `read_case` helper :44-49: `{tool_name: $tool_name, tool_input: {file_path: $f}}`)。

若实现者/测试执笔人按 spec 字面构造探针 (未意识到要套 `tool_input`), `.tool_input.file_path` 提取为空串, 命中 `[[ -z "$file_path" ]] && exit 0` 短路 (:540) —— **无论 pattern 加没加, 探针永远 exit 0**。这会制造一个「假红→假绿」的 baseline-failing 窗口: 红态不是因为真漏报, 是探针打不中 hook 的判断路径; 改完 pattern 后依然 exit 0 (同一条短路), 看起来像是「修复生效」, 实际 pattern 从未被真正触发过一次。

已用正确嵌套形状实测确认: 当前基线确实 exit 0 (真漏报, 见上表)。风险在于两种「exit 0」外部完全无法区分, 除非明确读代码或对照 helper。

**建议**: SC-2 直接写「复用既有 `read_case` helper 构造探针」而非给出容易被误读的扁平 JSON 示例; 或在 spec 里把嵌套形状写全。

## [A2-m1] (Minor) 前置字符类允许成员 `~` 在当前所有敏感名组下结构性不可达

前置字符类允许集包含 `~`, 但所有敏感名组成员 (既有 shell-rc 7 条 dot-prefixed `\.bashrc` 等, 以及本 spec 新增的 3 条 claude-config `\.claude/settings\.json` 等) 都以 `.` 开头。真实 shell tilde 展开语法要求 `~` 后必须紧跟 `/` 才生效, 所以任何真实命令形态里, 敏感名前一个字符实际上总是 `/`(来自 `~/`), 从不是 `~` 本身 — `~` 这个允许分支在当前语料下不可达。

SC-3/SC-4/SC-5 列出的示例 (`cat ~/.bashrc` 等) 都无法覆盖这个分支; 若实现把 `~` 写错方向 (比如误写进排除集), 没有任何 fixture 会变红。

**建议**: 补一条人工构造的 fixture 直接让 `~` 贴着敏感名 (哪怕不是常见写法, 只为分支覆盖), 或在 spec 里注明保留 `~` 是为将来「敏感名组新增不带前导 `.`/`/` 的成员」预留, 当前不可达属已知情况。

## [A2-m2] (Minor) 新增 `python3?` reader 无 FP 反事实 SC

Task 1.1 把 `python3?` 加进新 claude-config pattern 的 reader 组, 且不要求 `-c` 限定 (不同于既有 :785 专用 python3 pattern)。这意味着任何 `python3 <script.py> ... <claude 配置路径作为参数>` 都会触发, 包括脚本只是做存在性检查/lint 之类无害操作的场景。spec 未给出对应 SC 或 Out-of-scope 声明, 也没有反事实说明这个新增误杀面是否可接受。

**建议**: 补一句 Out-of-scope 声明 (「python3 读 claude 配置一律拦, 不区分脚本意图, 与 credit 系统既有粒度一致」) 或加一条 SC-3 变体验证一个合理的 python3 no-op 用例是否也需要 `>/dev/null`/字段白名单才能放行(与 jq 同等对待)。

## 正向确认 (未发现问题的部分)

- **SC-3 三条期望内部一致, 未发现写反**: 逐条对照 `_sg_compute_credit` 推演 — (a) 直读 `jq 'keys' ~/.claude/settings.json` 无管道, jq 安全谓词要求 `\|` 前缀 (:332/:337), 不满足 ⇒ credit=0 ⇒ 拦, 与「应拦」一致; (b) `cat ... | jq 'keys'` 管道形态命中 `\|[[:space:]]*jq...keys` ⇒ credit=1 ⇒ 放, 与「exit 0」一致; (c) `jq '{model}' ... >/dev/null` 命中 `>[[:space:]]*/dev/null` 独立于 jq 判据的 credit 分支 (:373) ⇒ credit=1 ⇒ 放, 一致。三条期望与实现语义方向全部对齐, 未见写反。
- **SC-5 的反事实有效性已验证**: 若前置字符类方向写反 (只在 `(`/`|`/`\` 触发, 而非在其余成员触发), `cat ~/.bashrc` 中 `.bashrc` 前一字符是 `/`(允许集成员) ⇒ 方向反转后不再触发 ⇒ 变 exit 0 ⇒ SC-5 三条 fixture 全部会红。SC-5 不是恒绿断言, 是真正锁方向的反事实闸。
- **SC-4 的字面量位置判定与真实字符对得上**: `grep -oE '(\.bashrc|[^)]*)' ...` 中 `.bashrc` 前一字符实际是 `\`(转义反斜杠, 来自 `\.bashrc`), 属排除集, 而非 spec 行文里以为的 `(`; 两者都在排除集里所以结论不受影响, 但精确指出实际触发字符是 `\` 供 Phase B 实现时对照。

## 结论 (R1)

verdict = REVISE。核心卡点是 A2-C1 (前置字符类的实际生效路径与 spec 引用的 `_sg_line_match` 基建脱节, 单行 fixture 掩盖了这个分歧) 和 A2-M1 (作用范围未点名, sibling 误报行为 SC-6 测不出越界)。这两条不解决, Phase B 实现出来的红绿窗口有相当概率是「测过了但没测到点上」的假绿。M2/m1/m2 建议在 Phase B 任务展开时一并吸收, 不构成阻断。

---

## R2 (v2) 复核

聚合处置表: `.aria/audit-reports/post_spec-R1-1787375602111-secret-guard-manifest-precision-aggregated.md`。逐条核对 v2 `proposal.md` 对 A2-C1/M1/M2/m1/m2 的落地, Q1 = 忠实? Q2 = 我 R1 原处方对吗?

### [A2-C1] → v2 What.3「实现路径语义」段 + SC-4/SC-5 多行 fixture

**Q1 忠实。** v2 没有回避分歧, 直接选定架构分支: 「拦截路径对 risky_patterns 用裸 `[[ =~ ]]` **整串匹配** (非 `_sg_line_match` 逐行) — `^` 只锚**整串首**; 多行命令中段行首不享受「串首」成员」, 并要求 SC-4/SC-5 各补多行 fixture。这正是我 R1 列出的两个架构选项 (a)/(b) 里的 (a), 而且明确点破「串首」member 在多行场景下的真实覆盖边界 (不装傻说「反正沿用 `_sg_line_match`」)。

**Q2 我原处方基本对, 但补一层实测验证收窄了残余风险。** 我 R1 只走到「分歧未锁定, 需要选边」, 没有验证选边 (a) 是否真的可行 (即「空白」member 能否在没有逐行拆分的情况下正确捕获 heredoc 中段行首)。R2 补测:

```bash
pat="([[:space:]]|^)\.bashrc" ; s=$(printf "line1\n.bashrc")
[[ "$s" =~ $pat ]]   # → MATCHED
```

确认 bash ERE 的 `[[:space:]]` POSIX class 在整串匹配下**确实吃得到内嵌的 `\n`**, 不需要逐行拆分或 `_sg_line_match` 也能让「空白」member 兜住物理换行。再对现网 (前置字符类尚未实现的) `:709` shell-rc pattern 实测多行命令 `echo hi\ncat ~/.bashrc`, 结果 `exit=2`(见下表) —— 证明「整串匹配 + `[[:space:]]` 兜底换行」这条路径在**既有 pattern** 上已经天然成立, 前置字符类叠加上去 (只要用 `[[:space:]]` 而非字面空格) 不会破坏这个既有行为。残余风险收窄到「实现者是否遵循 `[[:space:]]` 这个仓内既有惯例」而非「架构选型本身是否可行」—— SC-5 新增的多行 fixture 恰好是锁住这个残余风险的正确闸门。**结论: 分歧已解, 且验证了解法本身站得住, 无需再拦。**

### [A2-M1] → v2 What.3「适用面点名」段

**Q1 基本忠实, 有一处停留在文字层未落 SC。** v2 明确点名「全部路径清单型 pattern 行 — `:709` shell-rc 行、claude-config 行、以及 `.env`/`id_rsa` 等同构 sibling 行」, 且指出「活体误拦命中的正是 .env 面, 只改 shell-rc 行治不到」—— 范围边界不再模糊, 直接命中我 R1 的核心诉求(哪些行、含不含 .env)。但落地机制是「B.1 入场时对 pattern 数组逐行枚举, detailed-tasks 列清单」, 即**推迟到 Phase B 任务清单, 而非在 SC-4/SC-5 里直接钉一条 .env 面的具体 fixture**。翻查 v2 SC-4 (`grep -oE` 变体 + 多行) 和 SC-5 (`~/.bashrc`/`~/.zshrc`/`/etc/profile`/`.bashrc` 裸文件名/`"$HOME/.bashrc"`/多行) 的完整清单, **没有一条是 `.env` 面的**, 而 Why 段两次点名的「活体误拦」原始复现 (触发本 spec 立项的那次) 指向的正是 `.env` 面, 不是 `.bashrc` 面。

**Q2 我原处方 (「补一条 SC 断言 sibling 行为在改动前后完全一致」) 方向对, v2 只吸收了一半** —— 吸收了「点名范围」, 没吸收「补 SC 锁定」。这不是回退 (原来是「范围都没点名」, 现在是「范围点名了但没有对应 SC 直接测」), 严重度也从 Major 降到 Minor: 有 B.1 「逐行枚举入 detailed-tasks」的程序性保障兜底, 不会像 v1 那样完全没人管; 但没有 SC 直接锁, 意味着如果 B.1 执行时漏了 .env 这一行 (人工枚举总有疏漏概率), SC-6「全量回归绿」本身也测不出来 (回归套件里从没有过 .env 面的字面量位置误报 fixture, 无基线可比对)。

**残留 (m1-carry, 非阻断)**: 建议 Phase B 在 SC-4 或 SC-5 里显式补一条 `.env` 面的字面量位置误报 fixture (例如 `grep -oE '(\.env|[^)]*)' aria/hooks/secret-guard.sh` 型), 把「活体误拦命中的正是 .env 面」这句 Why 段原话真正锁进红绿窗口, 而不是只停留在任务清单的人工核对。

### [A2-M2] → v2 SC-2「探针嵌套结构写死」

**Q1 忠实。** v2 直接把探针写成可执行的完整命令: `jq -n '{tool_name:"Read", tool_input:{file_path:"'$HOME'/.claude/settings.json"}}' | secret-guard.sh`, 不再是容易被误读的扁平示意 JSON。

**Q2 我原处方对, 且已完整闭环。** 逐字实测 v2 给出的这行命令 (未改一字, 只是本地执行), 结果 `exit=0`(见下表), 与 v2 声称的「基线 0」一致, 且证明这个探针**形状本身可执行、可复现**——不再有「假红假绿」的结构性风险。此条完全解决, 无残留。

### [A2-m1] → v2「白名单删 `~`」

**Q1 忠实, 且是最干脆的一种落地方式。** v2 没有勉强保留 `~` 再补 fixture, 而是直接从白名单删除, 并写清理由 (「真实 tilde 语法后必跟 `/`, 由 `/` 成员覆盖, `~` 成员结构性不可达」)。

**Q2 比我原处方更优。** 我 R1 给的是两个选项 (「补 fixture」或「删除并注明」), v2 选了更干净的后者——删掉一个永远测不到的分支, 比留着它再造一条只为覆盖率而存在的人工 fixture更符合「测试要测真实语义」的原则。无残留。

### [A2-m2] → v2 What.1「python3/node 改走 :785/:786 窄先例」

**Q1 忠实, 且处理力度超出我原建议。** 我 R1 只要求「补 FP 反事实 SC 或 Out-of-scope 声明」, v2 直接**结构性移除**了问题根源——不把 `python3?`/`node` 并入新 claude-config pattern 的通用 reader 组, 而是复用仓内已有的窄先例 `:785`(`python3?[[:space:]]+-c[...]`)/`:786`(`node[[:space:]]+-e[...]`), 只追加 claude-config 关键词, `-c`/`-e` 限定原样保留。这从源头消灭了「无 `-c` 限定的裸 python3 reader」这个新增误杀面, 比打补丁式的 FP SC 更彻底。

**Q2 v2 的方案优于我的原处方。** 我建议的是「事后补测」, v2 是「结构上不引入」——不引入就不需要测, 直接把攻击面归零。无残留。

## R2 实测表增量 (对 v2 proposal 的具体断言/探针, 只读, 命令文本不执行)

| 项目 | 探针 (原样摘自 v2 或按 v2 语义构造) | v2 声称 | 实测 | 判定 |
|---|---|---|---|---|
| SC-2 (v2 逐字) | `jq -n '{tool_name:"Read", tool_input:{file_path:"$HOME/.claude/settings.json"}}' \| secret-guard.sh` | 基线 exit 0 | **exit 0** | 一致, 探针形状可执行, M2 闭环 |
| SC-5 多行守卫 (代理测, 现网 :709 pattern, 前置字符类未实现) | `Bash{command: "echo hi\ncat ~/.bashrc"}` (真实嵌入 `\n`, 单一 segment 整串匹配) | 「仍 2」 (前置类叠加后应保持) | **exit 2** | 现网基线已 2; 隔离验证 `[[:space:]]` 吃得到 `\n`, 前置类叠加后按 [[:space:]] 惯例实现应保持 2, C1 残留风险收窄为「实现是否遵循仓内 `[[:space:]]` 惯例」, 已被 SC-5 新增 fixture 锁住 |
| SC-3 核心断言 (claude-config, jq `{` 形状) | `Bash{command: "cat ~/.claude/settings.json \| jq '{env: .env}'"}` | 基线 0 (待实现后应变 2) | **exit 0** | 一致, 真红 (当前无 claude-config pattern, 未命中 risky_patterns, 非因 credit 豁免) |
| SC-3 对照组 (.env, 通用面不动) | `Bash{command: "cat .env \| jq '{env: .env}'"}` | 隐含「不变」= 现状 0, 且改动后仍应 0 | **exit 0** | 一致, 是有效的非退化守卫 (若实现把 claude-config 专属的 credit 收紧误写成全局生效, 这条会翻红) |
| 隔离正则验证 (支撑 C1/SC-5 判断, 非 hook 端到端) | `[[:space:]]` class vs 嵌入 `\n`, `[[ str =~ '([[:space:]]\|^)\.bashrc' ]]` | — | **MATCHED** | 确认整串匹配下「空白」member 天然覆盖物理换行, 不依赖逐行拆分 |

## 结论 (R2)

verdict = **APPROVE**。A2-C1/M2/m1/m2 四条在 v2 里忠实落地且经本轮实测/隔离验证站得住; A2-M1 吸收了一半 (范围点名到位, 但缺一条直接锁定 `.env` 面的 SC, 降级为 Minor carry-forward, 不阻断)。R1 时「测过了但没测到点上」的假绿风险 (尤其 C1 那条架构分歧) 在 v2 已经被显式选边 + 实测验证收窄到可接受范围。
