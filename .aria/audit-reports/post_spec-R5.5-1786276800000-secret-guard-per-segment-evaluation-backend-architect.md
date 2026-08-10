---
checkpoint: post_spec
round: R5.5
round_kind: findings_review
review_target: v7 (commit e946955)
spec: secret-guard-per-segment-evaluation
timestamp: 1786276800000
date: 2026-08-09
seat: backend-architect
seat_id: BA
lens: bash / 正则实现层机械验证
verdict: REVISE
critical_count: 0
major_count: 0
minor_count: 2
mechanically_verified: 17
authored_versions: none
---

# R5.5 · backend-architect — v7 实现层复核

> **落盘补记 (R6 code-reviewer M-2)**: 本报告原为临时 agent 派发, 未按约定落盘,
> 而 v8 的全部改动挂在其编号 (W-1..W-8) 上, 且 proposal 正文引用了「W-1」。
> 本次按 owner 2026-08-10 裁定补档。编号统一为 **`BA-*`** (席位前缀), 原 `W-*`
> 为主 loop 下发的工单号, 二者对应关系见文末。

## 三项强制核验 (Q1 忠实度 / Q2 正确性)

| 项 | Q1 | Q2 |
|---|---|---|
| `BLOCK_KW_RE` 删 `in` / 加 `!` / 保 `&` | PASS | PASS |
| 「保留 `&`」驳回 | PASS | PASS, 且「第三条路」经压力测试更差 |
| B-4 计数 141/81/79/7/5/1 | PASS | PASS, 自写扫描器精确复算 |

**删 `in` 无覆盖回归**: `in` 在 bash 文法里只出现于 `for`/`select`/`case`, 其后永远是词表或
模式。唯一构造出的 OLD=1/NEW=0 对比串 `echo a; value in for b; do echo x; done` 经
`bash -n` 核实是**非法语法**, 不构成真实攻击面。

**「第三条路」严格更差** (把 `\|&` 显式编码进位置清单、删裸 `&`):

```
cat x |& for f in a; do :; done     保&=1   第三条路=1
cat x  & for f in a; do :; done     保&=1   第三条路=0   ← 漏检 (合法语句)
cat x &> f; for i in a; do :; done  保&=1   第三条路=1
```
裸 `&` 天然同时覆盖「裸后台」与「`|&` 尾部」两种情形, `\|&` 只覆盖后者。

## BA-1 (Minor, Q2) — `!` 松散边界未被完整刻画

`!` 作为顶层 alternation 分支左侧无边界要求 (不像 `;`/`&&`/`||`/`&` 是 shell 元字符):

```
echo myapp!for-config                OLD=0 NEW=1   (bash -n 合法)
git log --grep=!for                  OLD=0 NEW=1
echo '!if x'                         OLD=0 NEW=1
```

**非新增风险类别** —— 同类问题 v6 即存在:
```
echo redo for-real                   OLD=1   ("do" 是 "redo" 子串)
echo strengthen for a moment         OLD=1   ("then" 是 "strengthen" 子串)
```
方向 fail-safe (只多降级不漏拦)。owner 裁 A-2 时只测了 `!=` / `[[ ! -f ]]` /
`awk '!/if/'` 三种, 未覆盖「子串邻接」这一角度 —— 属分析覆盖面不完整, 非结论错误。

**已验证的候选修法** (owner 2026-08-09 裁定不采, 归转出 11):
```bash
FIX='(^|'"$nl"'|;|&&|\|\||\||&)[[:space:]]*!?[[:space:]]*(for|while|until|if|case|select)\b'
```
真阳性 3 条全保留 / 假阳性 3 条全消除。**不解决 `do`/`then` 同类问题。**

> R6 code-reviewer m-1 补充: 该候选**同时删除了 `do|then|else|elif` 四个位置分支**,
> 本报告正文未提, 代价面未评估。

## BA-2 (Minor, Q2) — 转出 10 行号引用错误

`secret-guard.sh:695` 实为 **`:691`** (`grep -n 'Command was'`)。实体结论 (泄漏路径
可达) 经假值实跑复现成立; `:416` 的 `nomad var put` pattern 行号核实准确。

## 工单号对应

| 主 loop 工单 | 本报告编号 | 内容 |
|---|---|---|
| W-1 | (源自 R5.5 tech-lead TL-1) | SC-6/SC-14 补鉴别 fixture |
| W-5 | BA-1 | `!` 边界 → 转出 11 |
| W-3 | BA-2 | `:695`→`:691` |

**仓库文件一字未改。**
