---
verdict: REVISE
agent: knowledge-manager
round: R2
critical_count: 0
major_count: 2
minor_count: 1
r1_resolved: 2/3
---

# post_spec R2 — knowledge-manager 视角审计 (convergence)

对象: `openspec/changes/secret-guard-per-segment-evaluation/proposal.md`

## R1 核销结果 (2M+1m)

- **M-1 (CHANGELOG 迁移指引) → RESOLVED**: Task 1.5「CHANGELOG 行为变更显著标注 + 迁移写法」+ SC-10「CHANGELOG 含行为变更段 + 至少 2 条迁移写法示例 (机械 grep 断言)」— Task 与 SC 均已落地, 与 Impact §「行为变更」段 (L119) 呼应一致。
- **m-1 (归档不回写依据) → RESOLVED**: Impact 新增专段「归档 spec 不回写」(L125), 明示 `openspec/archive/2026-08-02-.../` 的 `KNOWN-LIMIT` 表述届时失效但按先例不回写, 依据说明完整。
- **M-2 (`secret-hygiene.md` 366 计数会再陈旧) → 部分核销**: Task 1.6「`secret-hygiene.md` 自测计数回填 (366 → 新值)」已加, 且 Impact「文档回填」段 (L124) 点名三处引用同根因。**但我在 R1 的建议动作原文是「补一条覆盖 secret-hygiene.md 三处计数同步…挂对应 SC 断言」—— SC 断言这一半未落地**。逐条核对 SC-1~SC-11, 无一条对 `secret-hygiene.md` 的 L23/L286/L318 (三处均已实读核实存在) 做机械校验; 对比同一 Impact 段落里 CHANGELOG 要求的 Task+SC 齐全 (1.5+SC-10), 计数同步现呈现新的不对称 (只有 Task, 无 SC)。2026-08-02 先例对同类 SOT 订正专设 SC-7 (正向+负向双断言) 珠玉在前, 本 spec 未比照。**降级但仍判 Major**, 见下 Major-1。

## 新发现

- **Major-1 (延续, 降级)**: 同上, `secret-hygiene.md` 计数同步仅 Task 级、无 SC 级机械校验。Rule #3 (文档与代码必须同步更新) 是不可协商规则, 且这正是 v1.1.1→v1.1.2 已经复发过一次的漂移类别 (同文件同根因)。建议: 补一条 SC (可比照 SC-11 「总数须注明 zsh 在场与否」的模式), 断言 `secret-hygiene.md` 三处活体计数与 SC-11 的最终总数一致、且残留 "366" 字面值仅允许出现在版本历史表 (L401 类) 的既往记录行内。

- **Major-2 (新)**: 转出项 2 (组/循环/条件整体重定向 5/5 误伤) 与转出项 3 (ssh/`sh -c` 外壳逃逸 5/5) 均只给出**泛化模板** (`{ …; …; } >/dev/null`、`ssh host '…'`) 与审计方代号引用 (tech-lead M-2/M-3), **未内联具体可执行的失败命令**。核实 `.aria/audit-reports/post_spec-R1-*` 系列文件目前是**未提交的 git 工作区文件** (`git status --short` 显示 `??`, 非 gitignore 排除 —— 可被 `git add` 但当前未入库), 且核对 2026-08-02 先例的归档目录 `openspec/archive/2026-08-02-secret-guard-nomad-var-put-echo/` 只含 `proposal.md`, 审计报告并未随归档保存。即: 这两项转出的完整复现证据**只存在于本 cycle 结束后大概率被清理/不随归档留存的临时文件里**, 一旦审计报告丢失, 未来开 issue 者拿不到实证的 5 条具体命令, 只能凭泛化模板重新摸索。对照本 spec 自身其余 5 项转出 (1/4/5/6/7) 与 2026-08-02 先例的转出项 (逐条内联完整命令, 如 `curl -v -X PUT … >/dev/null`), 这是本 spec 内部标准不一致, 也是相对先例的质量回退。建议: 转出项 2/3 各补 1-2 条内联的具体失败命令 (从 R1 tech-lead M-2/M-3 摘录), 使其自包含。

## 复核通过项

- **模板符合度**: PASS。章节顺序 Why→What→关键决策→Impact→转出→rule6_note→Tasks→Success Criteria, 与 `standards/openspec/templates/proposal-minimal.md` 及 2026-08-02 先例 (同款「转出」章节插在 Impact 与 rule6_note 之间) 结构一致; `Level`/`Status`/`Created`/`Issue` 字段齐全。
- **Rule #5**: PASS。落点 `openspec/changes/secret-guard-per-segment-evaluation/` (本项目自身目录), 非 `standards/openspec/changes/`。
- **rule6_note 框定**: PASS。substitute 框定 (structural fixture + unit-test corpus + dogfood) 与同一 hook 先例 (`2026-08-02-secret-guard-nomad-var-put-echo` + `2026-06-19-secret-guard-exfil-coverage-iteration`) 引用一致, 未越界套用 skill AB。
- **「dogfood 面限制」诚实声明核实**: PASS, 非变相豁免。实测核验: 本机 `~/.claude/plugins/cache/10CG-aria-plugin/aria/` 下现存最高版本目录确为 `1.63.0` (另有 1.55.0/1.59.1, 无 1.64.x/1.65.x), 与声明中「plugin cache 停在 1.63.0」逐字吻合; Aria#172 (`forgejo GET /repos/10CG/Aria/issues/172` 实查) 标题「plugin cache 停在 1.63.0 — v1.64/v1.65 全部 hook 修复在 Aria 自身运行时未生效」与本 spec 引用一致。该声明**未减损验收强度**——它把 dogfood 证据来源从「仓内 harness 触发」平移到「canonical 直调端到端脚本 (SC-9), 覆盖本 session 实际用过的 5 类命令形态」, 证据量与可证伪性不降, 只是换了可靠的采集点, 符合 substitute 精神而非规避。
- **验收环境声明的规范意义**: 判定为**本 cycle 说明, 暂不需要同步进 `standards/conventions/`**。理由: 该声明的触发条件 (canonical 与仓内 cache 版本不一致) 是 Aria#172 这一具体缺陷的症状, 而非稳定的架构事实; #172 一旦收口 (cache 与 canonical 重新同步), 声明本身即失效, 不具备「每 session 都该知道」的稳定性 (对齐 `claude-md-hygiene.md` 的稳定性判据, 虽然目标文件不同但判据可类比)。且 2026-08-02 先例对类似「值得独立成条」的通用发现 (转出 6: CLI 工具 TTY 相关默认输出行为) 采用的处置正是「点名 + 转出」而非当场写入 standards/conventions/ ——本 spec 遵循同一处置模式一致。**Minor-1 建议**: 在 Aria#172 的 issue 描述或跟进 comment 里补一句「验收基准点选择」的通用提醒 (canonical 优先于可能陈旧的本地/仓内运行时), 供 #172 关闭前其余 hook 类 spec 参考, 但不构成本 spec 的阻塞项。

## 结论

CONVERGED 判定: **否**。r1_resolved 2/3 (M-1、m-1 已核销; M-2 仅 Task 级核销, SC 级未落地, 降级保留为 Major-1), 另新增 Major-2 (转出 2/3 复现证据依赖非持久化审计报告, 自包含性不足)。两项均为**文本补丁级**修订 (各增补 1 条 SC + 2 处转出项内联命令), 不触及架构/范围, 预期 R3 可收敛。
