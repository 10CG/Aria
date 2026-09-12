---
type: owner_decision
subject: aria-plugin-version-number-v1.73.1-allocation
status: decided
decided_by: owner (uni.concept.wzfq@gmail.com)
decided_at: 2026-09-12
---

# Owner Decision — `v1.73.1` 号归 `aria-plugin#194`, 两条 L2 Spec 顺延

> **Date**: 2026-09-12 · **Decider**: solo-lab owner · **Type**: 版本号分配 (跨轨仲裁)
> **Trigger**: 2026-09-11 合表时发现撞号 —— 并发轨 `pre-merge-completeness-gate-change-scope` 的 proposal `:366`/`:450` 已把目标号写成 `v1.73.1`, 而 `aria-plugin#194` 的修复已在 aria master `f314785` 未发版。

## 裁定

**`v1.73.1` 归 `aria-plugin#194`** (collision_dedupe 测试时钟修复)。**两条 L2 Spec 顺延。**

## 背景 (为什么会撞)

`#194` 的修复 2026-09-09 已合入 aria master `f314785` 但**未发版** (当时 owner 裁定「先不发, 只进 master」)。于是:

- 它不占号 ⇒ 并发轨读 `git tag --list` 看到最高仍是 `v1.73.0`, 合理地把下一个 PATCH 号算成 `v1.73.1`;
- 但它在 master 上 ⇒ **任何后续从 master 切的发布都会自动带上它**。

⇒ 「未发版的已合并修复」既不占号、又必然搭车, 是撞号的结构成因。两条轨各自的算号都没错。

## 操作含义

1. **`#194` 取 `v1.73.1`, 级别 PATCH** —— 纯测试文件改动, 零运行时行为变更, 对齐 `CLAUDE.md`「bug 修复 = PATCH」。
2. **两条 L2 Spec 顺延** —— 号在**各自 ship 时**按当时的 `aria/.claude-plugin/plugin.json` 重算 (本仓成文规则「落地时按 plugin.json 计算」/ TASK-023 re-check 机制), **不在此预分配**。
   - ⚠️ 两条 Spec 的**级别** (PATCH vs MINOR) 仍是**未裁事项**, 本裁定不触及 —— 见各自 proposal 的「待 owner 复议」条目。级别裁定后才谈得上具体号。
3. 两条 proposal 中把 `v1.73.1` 写成目标号的位置需勘正为「ship 时重算」。⚠️ 那是**并发容器 `aria-runner-bot/bfe8285d` 在制的 artifact**, 本容器只在其中留裁定指针, 不改写其正文结论。

## 后果 (对 `#194` 的 carry-forward)

本裁定使 `#194` 的「修复未发版, 已发布 v1.73.0 与采用方副本仍红」这条 carry-forward **可闭合** —— 发 `v1.73.1` 即修到采用方。

## 已知阻塞 (2026-09-12 发版当日)

**github 不可达**: `ls-remote github` 三次重试均 rc=128, 代理 `192.168.69.212:7890` 报 "No route to host"。按 `CLAUDE.md` 多远程约束 2 (双推 + 逐端 `ls-remote` 核验), **本轮不做任何 push** —— 只推 origin 会造镜像分叉; 若同时 bump 主仓 gitlink 到 github 上不存在的 aria SHA, 就是 `Aria#165` 记录的 orphaned gitlink 事故的确切形状。本地 bump + tag 完成后**等 github 恢复再双推**。

## 跨引用

- `10CG/aria-plugin#194` — 被授号的修复
- `10CG/Aria#195` / `10CG/Aria#199` — 顺延的两条轨
- `10CG/Aria#177` — 发布同步面无枚举式机械覆盖 (本次发版即用其 comment 23105 实测出的 POINTS 清单当检查表)
- `10CG/Aria#165` — GitHub 镜像漏推类级根因 (本轮 github 不可达时不推的依据)
