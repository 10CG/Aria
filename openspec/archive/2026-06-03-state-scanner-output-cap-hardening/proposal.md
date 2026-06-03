# state-scanner-output-cap-hardening

> **Status**: ✅ **SHIPPED 2026-06-03** (aria-plugin v1.38.0, PR #73 merge `c7ec539` 双远程 parity; 主仓 gitlink → `c7ec539`)。Phase A.2 CONVERGED 2026-06-01 (R1 NEEDS_FIX/PWW/PWW → Rev1 → R2 PWW/PASS/PASS unanimous; 2 Critical CLOSED)。Phase B full cycle: TG-A (10 区块字段骨架 + sync-check) + TG-B (3 层 resolver + 30 测; OQ3=warn-only / OQ4=10 核心块不 collapse); 45 新测 676 全绿零回归。Closes #71 + #72。
> **Phase A.2 carry (Phase B 启动前须办)**: OQ3 (上界 clamp vs warn-only) owner 定 → TG-B.4「上界超限」测试据此断言; OQ4 (canonical 区块数 10 vs collapse) 在 TG-A.0 reconcile 锁定 (TG-A.3 sync-check 依赖其输出)。
> **Rev1** 2026-06-01 post_spec R1 修正
> **Level**: 2 (Minimal — proposal + tasks)
> **Target skill**: `aria/skills/state-scanner` (aria-plugin)
> **Target version**: v1.38.0 (aria-plugin) / 主仓 gitlink bump
> **Forgejo issues**: [#72](https://forgejo.10cg.pub/10CG/aria-plugin/issues/72) (输出格式) + [#71](https://forgejo.10cg.pub/10CG/aria-plugin/issues/71) (branch cap 硬编码)

## Why

`/state-scanner` 是十步循环的统一入口、最高频工具。两个独立 dogfood 暴露了它在「输出」与「扩展性」两个维度的劣化。

### Problem 1 (#72) — 输出区块缺**每区块字段示例**, AI 凭记忆补字段 → 字段层漂移

> **Rev1 更正 (R1 C1/C2/M1/M2)**: R1 audit 核实了真实代码, 推翻了本节初稿的两处失实, 现据实重写。

**实际现状** (`SKILL.md:146`, 5 行 section): **已内联**有序 10 区块清单 (📍当前状态 / 📊变更分析 / 📄需求状态 / 🏗️架构状态 / 📋OpenSpec状态 / 🛡️审计状态 / 🔧自定义检查 / 🔄同步状态 / 🎫Open Issues / 🎯推荐工作流) + 「每区块只在数据可用时显示, 空状态优雅降级」原则 + 指向 `references/output-formats.md` 的链接。

所以**初稿"砍到 8 行罗列、骨架缺失、漏区块"的说法夸大且部分失实**:区块清单与降级原则**未丢**(它们在 L146)。真实 gap 是更细的一层:

- L146 只列区块**名**, **没有每区块的关键字段示例** (字段示例只在 `output-formats.md` L7-118 标准场景才有, 如 📍下的 分支/模块/Phase-Cycle/变更/OpenSpec)。
- v1.32.0 progressive-disclosure 重构 (SKILL.md 669→317 行) 把这些**字段级骨架**移到引用文件。AI 不读 reference 就只能凭记忆补字段 → **字段层漂移** (区块在、但每区块内容/字段每次不同, 偶有区块因无字段提示被一笔带过)。
- `references/output-formats.md` 本身**未被削弱** (全程 685 行, 完好)。这是 progressive-disclosure 的**字段级触达 gap**, 非区块清单缺失。

**附带发现 (R1 C2)**: `output-formats.md` 标准场景 (L7-118) 用 `📝 README 同步状态` + `🔗 Forgejo 配置检查`, 而 `SKILL.md:146` 用 `🔄 同步状态`。存在区块命名分裂, TG-A 须先 reconcile 出**单一 canonical 区块集**再补字段。

### Problem 2 (#71) — `MAX_BRANCHES_SCANNED` 硬编码 20, 大仓恒触发软错误

`handoff_multibranch.py:97` 硬编码 `MAX_BRANCHES_SCANNED: int = 20`。仓库 `refs/remotes/origin/` 分支数 > 20 时:

- `scan.py` 恒发 `handoff_multibranch_branch_cap` soft_error → **退出码 10** (非 0)。
- 多终端看板 (`tracks_multibranch`) 只扫最近 20 个分支 (committerdate desc), 漏更旧分支的 handoff track。

**外部大仓实证**: 一个第三方项目 dogfood 报告 **远程分支 440 个** 超上限 20。删已合并分支的临时消音方案在此**数学上不可行** (活跃 feature 分支也远超 20), `multi-terminal` 核心能力在目标规模下**静默失效** (覆盖 20/440 < 5%)。

## What Changes

单一 Level 2 Spec, 两 task group (同属 state-scanner skill, 均 <5 task、同文件面、无交叉依赖 → 合并降低 ship overhead)。

### TG-A (#72) — 补每区块字段骨架进 SKILL.md, 并防再漂移

- 先 reconcile canonical 区块集 (R1 C2: `🔄 同步状态` ↔ `📝 README 同步` ↔ `🔗 Forgejo 配置检查` 三者对齐 `output-formats.md`), 锁定**确切区块数与名**。
- 把 `SKILL.md:146` 的区块**名清单**扩成**带每区块关键字段示例的精简骨架** (~20-30 行), 使「不读 reference 也能正确排版到字段层」成立。降级原则已在 L146, 保留。
- **自动化 sync-check** (R1 I-1 / Finding 1): 加测试断言 canonical 区块 header 在 `SKILL.md` 骨架 与 `output-formats.md` **同时出现且一致**, 防止二者再次漂移 (根因复发防护)。
- `references/output-formats.md` 保留为详细变体来源, 不动。不恢复全部 90 行——只补字段骨架 + sync guard。

### TG-B (#71) — `MAX_BRANCHES_SCANNED` 三层可配置

- 在 `_common.py` (R1 M-4: 与 `resolve_forgejo_hosts` 同文件是 import graph 唯一一致选择) 加 `resolve_max_branches_scanned(project_root) -> int`, **结构**镜像 `resolve_forgejo_hosts` 的 env > config > default, 但**显式处理 int 域差异** (R1 I-1/I-2):
  1. env `ARIA_HANDOFF_MAX_BRANCHES`: `int(raw.strip())` 包 `try/except (ValueError, TypeError)` → 失败回退下一层。
  2. config `state_scanner.handoff_multibranch.max_branches`: 接受 int, **显式拒 bool** (`isinstance(v,int) and not isinstance(v,bool)` — bool 是 int 子类 footgun), 复用同 `(OSError, JSONDecodeError)` 守卫。
  3. default `20` (向后兼容, 不变)。
  - 每层独立判 `≤0 → 回退下一层` (env="0" 落到 config, 非直接 default)。
  - **上界安全** (R1 I4/Finding 4): 设推荐上界 (如 500); 超上界 `log.warning` 提示但仍尊重 (或 clamp — Phase A.2/owner 定)。
- `handoff_multibranch.py` 改读 resolver: 替换 L97 常量的运行时消费点 (L302/305/306/311), cap 文案动态用 resolved 值; 同步更新 docstring L51 + 注释 L127/L159 (Rule #3 docs-in-sync)。
- `.aria/config.template.json` 文档化新 key。

## Impact

- **Affected**: `SKILL.md` (TG-A) + `references/output-formats.md` 仅作 sync-check 只读源 + `handoff_multibranch.py` (TG-B) + `_common.py` (TG-B resolver) + `.aria/config.template.json` (TG-B) + tests。
- **向后兼容**: ✅ TG-B default=20 不变; TG-A 纯文档增量。
- **Downstream 安全** (R1 I3 / qa 显式核): cap 可配置对 `lib/collision.classify` + `phase1_gate` + rule 1.54 `concurrent_churn_detected` 是 **additive-only** (扫更多分支 → 看到更多 track/collision = 目标行为, 无 false-negative)。新增风险仅 **性能**: 440 分支 × 每分支最多 3 git subprocess (5s timeout) → 须由上界 + 文档管控。
- **Rule #6** (deterministic/structural skill substitute = structural fixture + unit tests + dogfood, per [[feedback_deterministic_structural_skill_rule6_substitute]]): TG-B = resolver 单测 (镜像 forgejo-hosts **30** 测, 含 int 域用例); TG-A = **自动 sync-check 测试** (非仅 manual dogfood) + dogfood 人工核区块完整。
- **Versioning**: v1.37.0 → **v1.38.0** (MINOR); 主仓 gitlink bump。

## Out of scope

- 第三方报告的 `git fetch 失败` 软错误 (独立 remote/凭据/网络问题, 与本 Spec 无关)。
- output-formats.md 内容重写 (它没坏)。
- 给 AB benchmark 真正新增「格式完整性」维度的实现 (本 Spec 用 sync-check 测试覆盖根因; AB 维度可 defer)。

## Open questions (Phase A.2 audit / owner 确认)

1. ~~resolver 放哪~~ → **已定** (`_common.py`, R1 M-4)。
2. default 是否从 20 提高? → 倾向保持 20 向后兼容, 大仓用 config/env 覆盖。
3. cap 上界超限时 **clamp 还是 warn-only**? → **已定 (owner 2026-06-03): warn-only + 尊重用户值** (log.warning 提示但仍用用户设的值, 不静默改意图)。TG-B.1 据此实现, TG-B.4「上界超限」测试断言 = 超限返回原值 + 发 warning。
4. canonical 区块集最终是 10 还是 collapse README/Forgejo? (R1 C2 — Phase B 实施前 reconcile 锁定)。
