---
round: R1
checkpoint: post_spec
spec: secret-guard-manifest-precision
seats: [A1-backend-architect, A2-qa-engineer, A3-code-reviewer]
verdicts: {A1: REVISE, A2: REVISE, A3: REVISE}
converged: false
totals: {critical: 3, major: 6, minor: 6}
timestamp: 2026-08-22T07:55:00Z
---

# post_spec R1 聚合 — secret-guard-manifest-precision (Aria#179)

三席一致 REVISE。方案骨架 (双平面清单 + 误报收敛方向) 三席均认可; 三条 Critical 各自独立且都实质。

## 去重后处置表 (→ v2)

| # | 来源 | 内容 | v2 处置 |
|---|------|------|---------|
| 1 | A1-C1 | **credit 逃逸**: `cat settings.json \| jq '{env: .env}'` 因形状 credit (:335-339) exit 0, 恰好泄走要保护的 env 节点; 「与 .env 同类已知面」类比不成立 (.env 非 JSON, 该逃逸在彼处实际死路; settings.json 是真 JSON 真 env 键, 直接可利用, A1 席 .bashrc 代理实测 exit 0) | Out-of-scope 撤销该条; What.1 增 claude-config 作用域的 credit 收紧: 字段白名单形状 (`jq '{`) credit **不适用**于 claude-config 源, 仅名字面/计数/哈希/丢弃类 credit 有效 |
| 2 | A2-C1 | **架构分歧**: 拦截路径对 risky_patterns 用裸 `[[ =~ ]]` 非 `_sg_line_match`; `^` 只锚整串 ⇒ 前置类「行首」成员在多行/heredoc 下不生效; SC-4/5 全单行 fixture 测不出 | What.3 写死实现路径语义 (整串匹配, `^` = 串首); SC-4/SC-5 各增多行 (heredoc) fixture |
| 3 | A3-C1 | **轮换引证张冠李戴**: 08-20 handoff 闭环的是 registration-token; #179 的 2026-08-09 `*_API_TOKEN` 无轮换记录, 可能是活凭据 | Impact 该句撤销; 新增 **TASK-0 (owner 门): 泄露凭据轮换核实**, ship 前置; 已 surface owner |
| 4 | A3-M1+A3-M2+A2-M1 | 前置字符类: 三重口径问题 — 适用 pattern 行未点名 (活体误拦命中 .env 面) / 「正则字面量位置」标签宽于机制 (引号定界裸名仍拦但按标签应治) / 白名单+排除集双集并存语义歧义 | What.3 重写: **单一白名单语义** (仅前一字符 ∈ {串首, 空白, ", ', =, /} 触发, 其余一律不触发); 适用面 = 全部路径清单型 pattern 行 (点名枚举, 含 .env 面); 分类标签改「非路径前缀位置」; 引号定界裸名归已知限 |
| 5 | A1-M1+A2-m2 | python3 并入通用 reader 会重开 prose 误报 (仓内 :785 已有 `-c` 限定的窄先例) | What.1 改: 新 pattern reader = 既有 12 + jq; python3/node 由扩展 :785/:786 源组承载 (加 claude-config 条目) |
| 6 | A1-M2 | 前置类与 `[[:space:]]+` 争用同一空白字符, `cat .bashrc` 单空格形态可能结构性失配 | What.3 补 ERE 陷阱点名; SC-5 显式含裸文件名单空格形态 |
| 7 | A2-M2 | SC-2 探针 JSON 须嵌套 `tool_input.file_path`, 扁平结构恒 exit 0 假窗口 | SC-2 探针写死嵌套结构 |
| 8 | A2-m1 | 前置类成员 `~` 结构性不可达 (真实 tilde 后必跟 `/`) | 从白名单删 `~` |
| 9 | A1-m1+A3-m1 | 计数错: :709 reader = 12 非 11; :546 = 29 分支非 17 类 | 数字勘正 |
| 10 | A3-m2 / A1-m2 | bare-filename/glob 变体已知限入 hook 头注释; secret-scan.sh 非第二清单面 (informational) | What.5 补注 / 不动作 |

## 席位实测亮点

- A2: SC-1/2/4/5 四条基线探针逐条实测与 spec 声称一致 (真红真绿); SC-3 与 credit 语义逐条核对无写反。
- A1: credit 逃逸用 .bashrc 代理实测而非纯读码。
- A3: 核验表 11/13; :709 无 jq / :546 无 claude 条目 / 误报形态逐字符一致等关键主张全部成立。

## 收敛判定

R1 REVISE → v2 落上表 → R2。
