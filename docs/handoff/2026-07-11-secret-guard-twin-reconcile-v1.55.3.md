---
track-id: secret-guard-bash3-multiline-hardening
owner-container: simonfish/bfe8285d
phase: reconcile
status: done
updated-at: 2026-07-11
---

# Session Handoff — secret-guard 双子星撞车和解 + v1.55.3 安全加固

> 承接同日 [2026-07-11-secret-guard-four-issue-fix-v1.55.2.md](./2026-07-11-secret-guard-four-issue-fix-v1.55.2.md)。本篇是那次 ship 之后 owner 提出的质量质疑 → 双子星撞车定性 → 和解。

## §0 入口 (新 session 优先读)

- **本 session 干了什么**: v1.55.2 ship 后 owner 问「确定我们质量更高吗」→ 实读双子星 L3 spec + 实测 → **发现双子星质量更高**, 且我 ship 的 v1.55.2 有它抓到的**真安全洞 (NUL-in-field 绕过)** → owner 决策 **B (和解, 非回退)** → v1.55.3 补 NUL 守卫 + log_ack + 归因订正, 双子星 spec 转权威设计。
- **当前态**: aria-plugin **v1.55.3** @ `c209c5b` 三方 parity。NUL 洞已堵。双子星 spec adopted-as-authoritative (部件 A+守卫已 ship, 部件 B 待实现)。
- **下一步优先级**: 见 §6。

## §1 双子星撞车定性 (owner 最初的问题)

- **谁**: git author 铁证 —— 双子星 secret-guard 那批 commit (759b980/5fe9562) 全是 **`aria-runner-bot`** (Aria 2.0 Layer 2 自主运行时容器 023236f2), **不是 dev-claude2**。owner 心智模型 (只用 dev-claude, dev-claude2 仅并行时开) 不含这个: 无人值守 bot 在同 repo 自主接方法论轨的活 (M6 遥测 / runtime-probe / 本 secret-guard spec 都是它)。
- **为什么 claim 没拦**: 两层洞。(1) **主因: bot 干活前根本没 claim** —— 协调 ref 里它唯一活跃 claim 是 `carry-runtime-probe-phase-b` (7-07, 早 ship 未释放), secret-guard 零 claim。协调系统无物可检测 (goal 直驱绕 claim gate 模式)。(2) 次因: 就算都 claim, track-id 字符串不同 (`secret-guard-bash3-multiline-hardening` vs `carry-secretguard-fieldparse-anchor`) 也判不出撞车 —— 系统是**字符串匹配, 非语义重叠检测**。
- **附带发现**: 协调 ref 一堆 stale active claim 从不释放 (bot runtime-probe / 我 dec002 / followup-99 都 ship 了还挂 active)。advisory 协调在泄漏。

## §2 质量重评 (owner 质疑触发, 实读 + 实测)

**双子星 spec 更强 (我漏的)**:
1. **NUL-in-field 绕过 (Critical)**: 我 v1.55.2 注释断言「JSON 值不能含 NUL」—— 只对字面 NUL 成立, JSON `\u0000` 转义 jq 会解码成真 NUL 与分隔符同形。**实测我 ship 的 v1.55.2 可绕过**: `ls\u0000printenv` / `echo hi\u0000env|grep TOKEN` → exit 0 放行 (dumper 溢出到 Bash 分支从不查的 file_path)。
2. **#152 归因**: 双子星 git 史核实 = `e8e847c` (SilkNode cherry-pick, 先于 v1.26.0); 我 changelog 写 `e9dc0f7` 错。本 session `git log -S` 复核确认双子星对。
3. 覆盖面 (命令替换/组合/包装器, owner 全覆盖决策)、log_ack 多行、bash3.2 BASH_ENV 夹具、two-state 可证伪测试 —— 均比我周全。

**我唯一更强**: zsh re-exec guard —— 双子星 spec 完全没提, 而 hook runner 用 $SHELL=zsh 忽略 shebang, 整脚本在 zsh 下 fail-closed 才是 #154 在 macOS 的真实执行路径 (它 SC-1 只测 bash 3.2)。已补进双子星 spec。

**结论**: 双子星 L3 更周全; 我抢先 ship 反把带 NUL 洞的版本推上 master + 分发下游。

## §3 owner 决策 B (和解) + 执行

不回退 v1.55.2 (macOS 用户已脱困, 下游不撤), 而是:
- **v1.55.3 ship** (本 session): NUL-in-field 守卫 (字段数恒 4 否则 fail-closed) + log_ack CR/LF/TAB 净化 + #152 归因订正。测试 292→297 (+5 NUL 绕过锁测, 修复前 exit0→后 exit2)。
- **双子星 spec 转权威设计** (`openspec/changes/secret-guard-bash3-multiline-hardening/` 加 ADOPTION NOTE): 标注 v1.55.2/v1.55.3 已实现部件 A+re-exec+NUL 守卫+log_ack; **补入我的 zsh re-exec 发现** (它漏的); 部件 B (命令替换/包装器全覆盖) 待实现。

## §4 未完成 / Carry-forward

- {id: carry-secretguard-partB, desc: 双子星 spec 部件 B (命令替换 $(env)/反引号 + 组合 {env;} + 单层包装器 sudo/nice/timeout env 的命令位全覆盖) 待实现 — 权威设计已在 spec + spike 36/37 + 误报矩阵; 走 post_spec R2→批准→实现 (aria-runner-bot 续 或 simonfish 接), 复用 v1.55.x 测试框架}
- {id: carry-coordination-stale-claims, desc: 协调 ref 多个 stale active claim 从不释放 (bot runtime-probe / dec002 / followup-99) + track-id 字符串匹配防不了语义重叠 + 自主 bot 干活不 claim — 方法论层协调机制 3 个缺陷, 值得专门 cycle 修 (DEC-002 advisory 协调的实战暴露)}
- (承前) M6 owner 4 门 / M7 D3 门 / aria-plugin#101 / i18n README

## §5 多维度同步

| 维度 | 状态 |
|------|------|
| aria-plugin | **v1.55.3** @ `c209c5b` (origin=github ✓); PR#104 merged |
| 主仓 | 本 handoff 随收尾 commit (副本同步 + gitlink + 版本 + spec adoption note) |
| Forgejo | #154/#156/#157/#152 保持 closed (v1.55.2 关, v1.55.3 是加固不重开) |
| 双子星 (aria-runner-bot) | 空闲 ~2h+ (最后活动 13:59 UTC), 无 secret-guard claim; spec 待其续或本侧接 |

## §6 Next session 入口 + 优先级建议

1. **协调机制 3 缺陷** (carry-coordination-stale-claims) —— 本次撞车的根因, 不修会再撞。DEC-002 advisory 协调实战暴露: 自主 bot 不 claim + 字符串匹配 + claim 不释放。值得专门 cycle。
2. 双子星 spec 部件 B (carry-secretguard-partB) —— 若要 secret-guard 命令替换全覆盖, 按其 L3 设计实现。
3. (承前) M6 owner 4 门。

## §7 提交清单

- aria-plugin: `60b99fe` → merge `c209c5b` (PR#104); origin=github ✓
- 主仓: 本 handoff 随收尾 commit (副本 + gitlink 023351b→c209c5b + 版本 + spec adoption)

## §8 Memory entries this session

- 已落盘 2 (上一 handoff): `feedback_defensive_fix_end2end_in_real_exec_env` + `feedback_harness_nul_in_backtick_edits_verify_with_python`
- **候选新增**: 「抢先 ship ≠ 质量更高: 并发轨质量对比要实读对方产物 + 实测自己产物, 不能凭'我 ship 了'下 superseded」(本 session 核心教训); 「自主 bot (aria-runner-bot) 会在同 repo 独立接活, 撞车不限于 dev-claude2」

## Cross-references

- 双子星 spec (权威): `openspec/changes/secret-guard-bash3-multiline-hardening/proposal.md` (含 ADOPTION NOTE)
- v1.55.2 handoff: `2026-07-11-secret-guard-four-issue-fix-v1.55.2.md`
- Issues: #154/#156/#157/#152 (closed)
