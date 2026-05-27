---
audit_id: post_spec-R1-tl-2026-05-27-aria-forgejo-hosts-parameterization
checkpoint: post_spec
round: R1
agent: tech-lead
spec_id: aria-forgejo-hosts-parameterization
spec_level: L2
verdict: REVISE
verdict_reason: "C1 假设的 config-loader skill API 不存在(documentation-only skill),§A helper 设计需要落地到具体 module;C2 三处共享 helper 物理位置/import 路径未定义,跨 file dedup 机制悬空"
issues:
  critical: 2
  major: 3
  minor: 4
timestamp: 2026-05-27T15:30:00Z
---

# tech-lead R1 audit — aria-forgejo-hosts-parameterization

## Critical findings (blocks Approved)

### C1. `_config_loader_forgejo_hosts()` helper 的物理位置和实现路径未定义,假设的"config-loader skill API"不存在

**位置**: proposal.md §A (L75-84) 第二段注

**问题**:
- proposal §A 写道:"`_config_loader_forgejo_hosts()` 是新 helper, 内部读 `.aria/config.json` **通过 config-loader skill API**(避免重复实现 JSON load)"
- 实测 `aria/skills/config-loader/` 目录只有 `SKILL.md` / `DEFAULTS.json` / `config-example.md` 三个文件 — **没有任何 Python 文件,无 callable API surface**。config-loader 是 documentation-only / convention skill,所有 collector (`multi_remote.py` / `issue_scan.py` / `requirements.py`) 都各自实现私有 `_load_config(project_root)` 函数读 `.aria/config.json`
- 这意味着 §A 描述的"helper 复用"在 Phase B 实施时会发现 API 不存在 → 要么 (a) Phase B 临时复制 `issue_scan.py::_load_config()` pattern 到 `forgejo_config.py`(违背 §A "避免重复"宣称),要么 (b) Phase B 临时新建 `config-loader/loader.py` Python module(scope creep — 一个新的可 import module 引入跨 skill 依赖,需独立 design)

**建议修复**:
- 必须在 §A 明确选定其一: **方案 A1** 在 `forgejo_config.py` 自有 `_load_config()`(模仿 `issue_scan.py::_load_config` L90+ pattern),完全本地化,**不依赖** config-loader 提供 API; **方案 A2** Spec scope 扩展到"新建 `aria/skills/config-loader/loader.py` 提供 `load_state_scanner_config(project_root, section_path) -> dict | None`"作为共享 module — 这变成有意义的基础设施投入但增加 ~1h
- 推荐 **方案 A1**(本地 `_load_config`),与 §B `issue_scan.py` 已有 `_load_config()` 对称,scope 不扩大,符合 L2 Minimal 定位
- §A code listing 必须 import line + 完整函数 stub(给 Phase B 起手不留歧义)

### C2. 跨文件"共享 helper"机制不可达 → R1 mitigation"抽取共享 helper"是 paper-promise

**位置**: proposal.md §Risks R1 (L232) + §A (L75-84) + §B (L93-98)

**问题**:
- R1 mitigation 写:"抽取共享 helper `_load_known_forgejo_hosts()` → 三处复用"
- 但 §A 实现在 `forgejo_config.py`,§B 实现在 `issue_scan.py`,§C 是 JSON 文件 — **三个文件分布在 2 个目录**(`collectors/` 和 `config-loader/`),collector 之间互相 import 私有 helper 违背模块边界(collector 应彼此独立 — multi_remote/issue_scan/requirements/forgejo_config 现状无 cross-import)
- 实际能"共享"的只有:`DEFAULTS.json` 作 single-source 值 + `ARIA_FORGEJO_HOSTS` 作 env single-source — 但 **precedence chain 的执行逻辑(env→config→default)在两个 collector 各自跑一遍**,无真正共享代码
- 这是 R1 风险的根因,但 mitigation 只是"声明"共享,无具体落地 → R1 实际无 mitigation

**建议修复**:
- 选项一(推荐):承认"逻辑共享不可行,值共享可行" — 显式声明 `forgejo_config.py` 和 `issue_scan.py` 各自实现 precedence chain(代码 duplication ~15 行 × 2),但**通过 unit test 强制等价**:`tests/test_forgejo_hosts_precedence_parity.py` 给两个 collector 喂同样的 env/config/default 三组 fixture,断言输出 host list 相等。Parity test 作为"三处一致"的执行性保障,替代不可行的代码共享
- 选项二:在 §A 改 §A 的 helper 移到 `aria/skills/state-scanner/scripts/collectors/_common.py`(已存在 module,`forgejo_config.py` L1 已 import)— 这是唯一在 collectors/ 边界内 legit 的共享位置。两个 collector 都 import `_common._load_forgejo_hosts_precedence_chain(project_root)`
- §Risks R1 必须重写 mitigation 列具体执行机制(parity test 或 _common 共享),不能停留在"抽取共享 helper"宣称层面

---

## Major findings (should-fix, warrants Rev1)

### M1. 跳号 v1.28 → v1.30 在 SemVer 上合法,但 CHANGELOG 编辑顺序的并发风险未充分设计

**位置**: proposal.md §Rollout Plan L213-224 + Cross-coordination 注 L224

**问题**:
- 本 Spec ship v1.30.0(2026-06-06 deadline),v1.29.0 ship 2026-06-07(block-flip)— **CHANGELOG 物理文件**会在 2026-06-06 先写入 `## [1.30.0]` 条目,然后 2026-06-07 block-flip ship 时再插入 `## [1.29.0]` 条目到 v1.30.0 之上
- 这要求 block-flip ship 时手动编辑 CHANGELOG.md **顶端 - 第二段位置**插入,容易出错(手动 sed/insert 高错率)
- 提案 L222 注"等 block-flip ship 时再补 v1.29.0 entry 后顺序仍为 1.28 → 1.29 → 1.30" — 但**没明确谁负责**(本 Spec 还是 block-flip Spec)
- 更严重:若本 Spec 因任何原因 D+13 delay 到 v1.30.x patch(per L224 mitigation),CHANGELOG 已有 v1.30.0 entry → 必须先 revert 删掉,scope creep

**建议修复**:
- 显式约定:**本 Spec ship 时 CHANGELOG 顶端先放占位 `## [1.29.0] - 2026-06-07 (reserved for block-flip)` 单行注释 + 然后 `## [1.30.0] - 2026-MM-DD` 真实条目**。block-flip Spec ship 时只需替换该单行 placeholder 为真实 entry,**不需手动定位插入点**
- 或:**反过来 sequencing** — 先 ship block-flip v1.29.0(2026-06-07),再 ship 本 Spec 为 v1.30.0(2026-06-09 之后)。代价是本 Spec slip 一周,但消除 CHANGELOG 编辑歧义。提案 §Risks R4 应加这个 sequencing 选项作为 alternative mitigation
- §Rollout Plan §5+1 SOT bump 清单中 CHANGELOG 行加注"插入位置:文件最顶部(`## [1.28.0]` 上方,留 placeholder for v1.29.0)"

### M2. §C "`forgejo: ['forgejo.10cg.pub']` 仍是 fallback 不删" 与 aria-fleet DEC D2 "通用层禁止新增 10CG-specific hardcode" 张力

**位置**: proposal.md §C L108-115 + §Cross-references aria-fleet DEC D2

**问题**:
- §C 保留 `DEFAULTS.json` 中 `"forgejo": ["forgejo.10cg.pub"]` 作 fallback,理由是 backward compat
- 但 aria-fleet DEC D2(`feedback_three_layer_universal_workspace_instance`)明确"通用层禁止新增 10CG-specific hardcode" — `forgejo.10cg.pub` 在 `DEFAULTS.json` 是**已存在**的 hardcode,**本 Spec 是参数化 audit 的窗口期**,保留还是清除值得明确论证
- 提案 §Backward compatibility guarantee L147 写"任何 Aria 项目无显式配置 → 行为不变(仍只识别 `forgejo.10cg.pub`)" — 这是 backward compat 的真实业务诉求,但**与 D2 硬约束的边界在哪里?** DEC D2 是否允许"legacy hardcode 保留但加 deprecated marker"?
- 当前提案对 D2 的 compliance argument 不充分(只在 §Cross-references 列了 memory pointer)

**建议修复**:
- §C 加显式 compliance discussion 段:引用 DEC D2 原文 + 说明本 Spec 的解读:"D2 禁止**新增** hardcode,但允许在参数化 wrapper 下保留**legacy fallback**(以 deprecation roadmap 形式)"
- 在 `DEFAULTS.json` 注释中加 `// DEPRECATED in M7+: 移除 forgejo.10cg.pub fallback, 改为 [] (require explicit config). Tracked: <future Spec ID>` 显式标注 fallback 的 deprecation 路径
- 或:直接在本 Spec 引入 `ARIA_FORGEJO_FALLBACK_DEFAULT` env(默认 true)— 当 false 时禁用 hardcode fallback → 用户可主动 opt out,为 M7+ deprecation 铺路。这是更彻底但 scope 扩大的选项

### M3. Phase B subagent 分配 / Agent 路由未在 Rollout Plan 体现 → 违 Phase A.3 baseline

**位置**: proposal.md §Rollout Plan §Phase B L194-197

**问题**:
- Phase B 子任务列出 3 个 sub-step(B.1/B.2/B.3),无 Agent 分配
- Phase A 标准要求 A.3 = Agent 分配(Aria 十步循环 Phase A.3,见 CLAUDE.md "A.3 Agent 分配 → 谁去执行")
- 本 Spec 属 Level 2 Minimal,虽 task.md 不强制,但 Rollout Plan §Phase B 至少应**简注** subagent-driver 是否会被使用、若用则用哪个 Agent(backend-architect for collector impl + qa-engineer for unit test?)
- 这与 `feedback_release_phase_d_5_files_synchronization`(Phase D atomicity)同档级的 baseline 缺失

**建议修复**:
- §Phase B 加一行:"B.0 Agent 分配 — 主 implementer: backend-architect(`forgejo_config.py` / `issue_scan.py` 修改); 测试: qa-engineer(parity test + unit tests); reviewer: code-reviewer(Phase B.3 之前)"
- 或显式声明"single-owner session 不 dispatch subagent"(符合 §Drafted L270 "single owner simonfishgit session")— 但需 explicit 写出,而非沉默省略

---

## Minor findings (carry-forward to Phase B 即可)

### N1. C2 行号 L71 与实测 DEFAULT_CONFIG 起始位置不完全对齐

**位置**: proposal.md L33 hardcode 表 "C2 ... L71"

**问题**:实测 `issue_scan.py` 中 `DEFAULT_CONFIG` 起始位置(`"enabled": False`)在 L66 附近,`platform_hostnames.forgejo` 在 L71-72。提案行号准确但表 §A/§B 引用的"L66-78"略宽于精确范围。Minor,不影响理解。

**建议**:Phase B 实施时校准 — 这是 Phase B 自检即可。

### N2. §Acceptance Criteria 缺"env override 大小写敏感性"边界

**位置**: §Acceptance Criteria L155

**问题**:`ARIA_FORGEJO_HOSTS="Forge.Example.COM"` 与 collector 的 `host in remote_url` 子串匹配是大小写敏感的(`_detect_forgejo_host` 见 forgejo_config.py L24-34 实测)。若用户 env 给 mixed-case host 而 remote URL 是 lowercase,会 silent miss。

**建议**:Acceptance §7 加"env hosts 与 remote_url 大小写匹配语义文档化 — 推荐 lowercase or 显式 case-fold in helper"。

### N3. §Testing Strategy `test_env_beats_config` 但缺 `test_config_beats_default`

**位置**: §Testing Strategy L173

**问题**:4 个 test 列出 env / config / default / env-vs-config,但 config-vs-default 的边界未独立测试(config 提供 hosts 时 DEFAULTS 必须被覆盖,但 config 为空 list `[]` 时是 falsy → 走 default 吗?还是当作 explicit-empty 不走 default?)— precedence 的语义对"显式空"未定义。

**建议**:Phase B unit test 增 `test_config_empty_list_behavior`(决策:explicit `[]` 视作"用户明确不要任何 host" 或 fallback to default,任择一并文档化)。

### N4. §Out of Scope 列表 与 boundary audit memo 是否完整对应未交叉验证

**位置**: §Out of Scope L240-249 vs `.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md`(未读)

**问题**:boundary audit 列出 P0=C1+C2+C3,P1+ 包括 C4? C5/C6/C7/C8 显式 defer。但 audit memo 是否还有 C4 / C9+ 项,本 Spec defer list 是否漏列?提案 §Out of Scope 应交叉验证 audit memo 完整 hardcode list,确保 P0+P1 都有 disposition(本 Spec 内、defer Sprint 2、defer M7+、不处理 三选一)。

**建议**:Rev1 时 cat boundary audit memo 完整 hardcode list 交叉对比,N4 状态从 "uncovered audit gap" → "verified complete"。

---

## Verdict summary

**Verdict**: REVISE → Rev1 后期望 PASS_WITH_WARNINGS

**关键判断**:
1. **C1+C2 是真实 architectural gap**(不是 nitpick):Spec 描述的"config-loader skill API"和"跨 file 共享 helper"在当前 codebase 实际不可行。Phase B 起手 0.5h 内会撞这个墙,导致 implementation drift from spec → spec 失去 source-of-truth 价值。必须在 R1→Rev1 修正
2. **M1-M3 是 baseline 不足**(可补救):CHANGELOG sequencing 风险 / DEC D2 compliance argument / Phase A.3 Agent 分配 baseline — 这些不阻塞实施但破坏方法论 hygiene。Rev1 补充 ~30 min 即可
3. **Risk 表完整性总评**:R1-R5 覆盖了主要风险面,**但 R1 mitigation 是 paper-promise**(见 C2),R4 mitigation 是 hard cap 而非真正 sequencing(见 M1)。Rev1 后这两项 risk mitigation 应有可执行 fallback
4. **Cross-Spec coordination**(与 v1.29.0 block-flip):**已被 §Cross-coordination 注 L224 + R4 充分识别**,只缺 M1 的 CHANGELOG 编辑顺序细化。Sequencing 总体合理
5. **Ship target staleness**(per `feedback_dec_ship_target_staleness_verify`):**已验证** — 当前 aria/VERSION = 1.28.0,plugin.json = "1.28.0",CHANGELOG 最新 `## [1.28.0] - 2026-05-24`,v1.29.0 在 CHANGELOG L31-32 明确 reserved 给 block-flip。**v1.30.0 slot 真空**,跳号 SemVer 合法 ✓
6. **Methodology compliance**:Rule #1 OpenSpec ✓ / Rule #4 conventional commits 未提及但 implicit ✓ / Rule #5 位置正确 ✓ / Rule #6 substitute pattern 已选择 deterministic structural(符合 collector 性质,引用 `feedback_deterministic_structural_skill_rule6_substitute` ✓)/ Rule #7 secret hygiene 不适用 / Rule #8 pre_merge_gate 显式列在 §C.2.4 ✓ / Rule #9 handoff 触发条件已识别("cycle 跨 4 phases" L209)✓。**唯一 baseline 缺失:Phase A.3 Agent 分配(M3)**

**推荐 Phase A.2 next action**:**REVISE → Rev1**。Rev1 工作量预估:
- C1 修复:§A code listing 改"in `forgejo_config.py` 自含 `_load_config()` 复刻 issue_scan pattern"(~10 min)
- C2 修复:§Risks R1 加 parity test mitigation + §A/§B 显式声明 "code 不共享,值通过 env+DEFAULTS 共享,测试通过 parity fixture 保障"(~15 min)
- M1-M3 修复:CHANGELOG placeholder 约定 + DEC D2 compliance 段 + Phase B.0 Agent 分配一行(~15 min)
- N1-N4:carry-forward to Phase B,Rev1 不强制

**总 Rev1 预估 ~40 min**,然后 R2 expectation = unanimous PASS_WITH_WARNINGS(per `feedback_post_spec_audit_two_round_pragmatic_for_l2`,L2 baseline 2-round)。

---

**Audit completed**: 2026-05-27T15:30:00Z
**Agent**: tech-lead
**Convergence track**: R1 → Rev1 → R2 (Level 2 baseline)
