# subprocess 解码加固: 结构性消除 text=True 解码异常 (aria-plugin #147)

> **Level**: Minimal (Level 2 Spec)
> **Status**: ⚠️ **SUPERSEDED-BY-SHIP (待 owner 处置)** — post_spec CONVERGED (R1→R2, 2 轮) 后、owner 批准前, 发现并发轨 (simonfish/023236f2) 已于 2026-08-19 直接修复并 ship **aria-plugin v1.66.2** (aria `de1eba5`: 11 调用点 `errors="replace"` + repo-wide AST 守卫测试 RED→GREEN + 假阳性勘正, Closes #147)。对方产物已实读比对: 覆盖本 spec 核心价值 (结构性消除 + 机械防再长 + coordination_ref 假阳性), 残值仅剩 traps.md #5 措辞勘正等零星项 (见下)。
>
> ```yaml
> converged: true          # R1 3×REVISE (9 实质点) → v2 → R2 0 Critical → v3/v3.1 → 确认轮 3/3 PASS
> rounds: 2
> superseded_by: aria-plugin v1.66.2 (aria de1eba5, 2026-08-19)
> residual_delta:          # 实读 de1eba5 + guard 测试 + traps.md 后核实
>   - "traps.md #5 措辞仍不精确 (「下游 json.dumps 时炸」— 实测 dumps 默认路径不炸, 炸在 utf-8 encode sink) — Level 1 文档勘正即可"
>   - "guard 谓词只扫 skills/** (排除 examples), hooks/ 生产 python 不在面内 — 当前零命中, 潜在缺口备忘"
>   - "L4 层 4 点未统一迁移 — guard 析取谓词 (errors= 或 ValueError 族 except) 下合规, 价值低"
> pending_owner: [spec 处置 — 归档 design-only (先例: premerge-gate 2838 行) 或删除; 残值项是否单独走 Level 1]
> ```
> **Issue**: [aria-plugin#147](https://forgejo.10cg.pub/10CG/aria-plugin/issues/147) (triage: confirmed / major / next-cycle, 复现 4/4, `.aria/triage-report-147.json`)
> **Owner 裁定 (2026-08-20)**: 走 **B 方案** (不逐处补 except, 统一从结构上消除解码异常)
> **审计轨迹**: post_spec R1 三席 (backend-architect / qa-engineer / code-reviewer) 一致 REVISE, 合计 1C+8M+7m 去重 9 实质点, 全部落本版; 方案本体三席均未动摇, A3 席独立重写普查脚本复现全部机械数字。报告: `.aria/audit-reports/post_spec-R1-1787225614997-subprocess-decode-hardening-*`
> **基线冻结**: aria submodule @ `3b97c35` (v1.66.1) — 全部语料数字对此 SHA 得出, 复核须对同 SHA 跑 (非活文件)

---

## Why

`issubclass(UnicodeDecodeError, OSError)` = False (它属 ValueError 族)。仓内 subprocess 调用点普遍传 `text=True` 让 subprocess 自己解码, 而 `except` 元组写的是 OSError 族 —— 远端返回非 UTF-8 字节时解码异常从元组底下穿过。

这是**类级缺陷**且带放大器: `pre_merge_gate.py:310` 明文把 `(TimeoutExpired, FileNotFoundError, OSError)` 元组立为「异常轴先例」(出处 `path_coverage.py`), 照先例抄元组 + 用 `text=True` 的新调用点会稳定复制缺口。`references/pre-merge-gate-empirical-traps.md` #4/#5 已把坑记录在案, 但**只有文档, 没有清理存量, 也没有机械防再长**。

**AST 普查 (对冻结 SHA; 方法: ast.walk 找 `text=True`/`universal_newlines=True` 实参 + 逐层枚举 enclosing except + [R1 补] `errors=`/`encoding=` kwarg 轴 + 调用链顶层捕获人工补查)**:

| 面 | 数字 |
|---|---|
| 含命中的文件 | 25 (issue 初筛 26/27 为 grep 文件级粗筛, 本表为 AST 精筛) |
| 全部调用点 | 46 |
| **生产调用点 (迁移目标)** | **16** |
| 测试调用点 | 30 (范围外; 30/30 已逐点核验仅吃本地 fixture — R1 A2 席 7 文件 + 主 loop 补验 5 文件) |

**生产 16 处按真实失效行为分四层 (R1 A3/A1/A2 席核验后的口径, 取代 v1 的「12 接不住」二分)**:

| 层 | 数量 | 点位 | 真实行为 (非 UTF-8 输入时) |
|---|---|---|---|
| L1 真穿透 | **7** | verify_post_push.py:65/:89 · aether.py:150/:173 · worktree_manager.py:117¹ · phase1_gate.py:240 · validate_schema_doc.py:130² | 未捕获崩溃 (脚本级) |
| L2 顶层兜住但整流程报废 | **4** | custom_checks.py:342 · spec_complete.py:863/:874 (以上三处均经 scan.py:476-480 顶层 `except Exception` → :480 EXIT_INTERNAL_BUG) · issue-triage `_common.py:39` (经 triage.py:315-323 → EXIT_HARD_FAIL) | 降级为整次运行内部错误 — 单点坏字节报废全 snapshot/report |
| L3 errors= 结构安全 | **1** | coordination_ref.py:255 (`errors="replace"`) | 不可抛 (真防线是 kwarg, 非 except) |
| L4 except 接得住 | **4** | fetch_gate.py:68 (ValueError 在元组) · closeout_trigger.py:90 / identity.py:173 (except Exception) · ss `_common.py:406` (元组含 UnicodeDecodeError; 真防线同为 `errors="replace"`) | 已捕获降级 |

> ¹ worktree_manager.py:117 现无生产调用方 (仅 lib 导出 + tests), 词法成立生产不可达 — 仍迁移 (统一模式)。
> ² validate_schema_doc.py:130 词法上无任何 enclosing try (调用者 main 的 try 仅 `except RuntimeError` :167/:173, 不接解码异常; 口径按 R2 A3 席两次勘正)。
>
> **全部 16 处都是迁移目标** —— B 方案的目标是统一模式使缺口不可能再长出, L2 的「兜住」也是把可局部降级的故障放大成全流程报废, L3/L4 是模式不统一的先例源。逐点清单 + except 元组见 `.aria/notes/2026-08-20-census-147.md` (census 脚本随本 spec 入库, SC-9)。

## What Changes (B 方案, 含一处实现精化 B′ — ⚠️ 待 owner 确认)

**1. 迁移全部 16 处生产调用点**: 去掉 `text=True` / `universal_newlines=True` / 逐点既有 `errors=` kwarg, 改 bytes 捕获 + 统一安全解码。

**2. 解码用单步 `decode("utf-8", errors="backslashreplace")` (B′ 精化)**。owner 裁定原文是「surrogateescape + 出口净化」; 实测 (三 sink 逐一验证, R1 两席独立复现) 表明:

- surrogateescape 残留的孤立代理码位, **崩溃点不在 `json.dumps` 默认路径** (ensure_ascii=True 能过), 而在两类 utf-8 encode sink: `dumps(ensure_ascii=False)` 后 encode / 直接文件写入 —— traps.md #5 措辞不精确 (任务 5 勘正);
- `backslashreplace` 在**解码这一步**就把坏字节转成字面 `\xff` 转义, 全程不产生代理码位 ⇒ sink 天然安全, 无需独立「出口净化」环节, 也消掉 decode 到 scrub 之间的裸奔窗口;
- 语义代价与「surrogateescape + 出口 scrub」相同 (均不可逆); 16 处消费者均为展示/解析文本, JSON 解析点上合法 JSON 必为 UTF-8 可解码, 坏字节 mangled 后走既有 JSONDecodeError 路径。L3 点 (errors="replace") 迁移后行为差异仅为坏字节的呈现形态 (`�` → `\xff` 字面), 信息量增加。

**若 owner 倾向严格按裁定原文执行, 本条降级为实现细节回退, 不影响其余条目。**

**3. canonical helper 按文件级去重内联** (标准形态 ~6 行: `subprocess.run(..., capture_output=True)` + stdout/stderr 各 `decode("utf-8", "backslashreplace")`)。同文件多调用点 (如 aether.py :150/:173) 共用一个文件内 helper def, 不逐调用点物理复制; 不建跨 skill 共享模块 (plugin 分发约束下脚本自包含是仓内既有纪律)。形态一致性由第 4 条结构检查保证, 不靠 import。

**4. 机械防再长 (修类不修实例的核心)**: 普查脚本落地为结构化测试, 断言 `text=True`/`universal_newlines=True` AST 命中数 = **0**。**扫描谓词为默认全含**: `aria/**/*.py` 全量, 显式排除仅 `**/tests/**` 与 `test_*.py`/`conftest.py` —— 排除式谓词使新目录/新 skill 结构上不可能静默逃逸 (R1 A1-M2: 允许清单会漏未来非常规目录)。`examples/`/`templates/` 等文档性目录**有意不排除** (R2 A1-R2-m1): 示例代码同样是被复制的先例面, 命中即红是期望行为 (当前基线零命中, 实测核对)。**baseline-failing**: 对冻结基线跑必红, 迁移完必绿。先例: #181 `config-template-key-currency`。

**5. 文档勘正 (换非作者执笔复核)**: (a) traps.md #5 「下游 json.dumps 时炸」→ 精确为「utf-8 encode sink (dumps ensure_ascii=False 后 encode / 文件写入) 时炸; dumps 默认路径不炸」+ 补 backslashreplace 单步替代注记; (b) `pre_merge_gate.py:310` docstring: **保留**其对自身实现 (surrogateescape + `_sanitize_for_json`, 结构安全, 不在迁移范围) 的局部描述, **追加**指向本 spec 全局约定的 cross-ref, 并声明全局约定适用于新增/迁移调用点、不要求重写既有结构安全实现 (R1 A1-M1: 防 docstring 与紧邻代码矛盾重演先例误导)。

**6. 回归面**: 全仓 test suite (非仅被改 skill 的 tests/ — 跨 skill 消费方风险) + 关键脚本 smoke (aether.py gate 路径 / verify_post_push / scan.py 全量)。

## Out of scope

- **30 处测试调用点**: 30/30 已逐点核验仅吃本地 fixture (git-in-tmpdir / sys.executable 自调 / bash 本地脚本), 解码崩溃即测试失败自暴露; 结构检查因此排除 tests。未来测试需喂非 UTF-8 fixture 时按本 spec 模式迁移。
- **其他仓库同类缺陷** (Aether 等): ship 时逐仓开转出 issue。
- **pre_merge_gate.py 自身实现**: 已是结构安全 (surrogateescape + 出口净化), 不重写 (见条目 5b)。
- **except 元组本身不缩窄** (SC-6): OSError 族捕获仍守护 spawn 失败, 迁移不得顺手删。

## Success Criteria

> 每条 SC 过反事实检验 (「机制没实现这条会红吗」); 复核轮请重跑该检验。

- **SC-1 (helper 行为)**: fixture 喂 `b"\xff\xfe"` 经标准形态解码 → 不抛、得确定性转义字面 `\xff\xfe`; 对照组: L1 层任一真穿透点的改前形态 (`text=True` + OSError 族元组) 同输入必抛 UnicodeDecodeError (锁「改前红」— 对照仅取 L1 层, L2-L4 改前不以裸抛形式失效)。
- **SC-2 (迁移完备, 机械)**: AST 普查对迁移后树 → 生产 `text=True`/`universal_newlines=True` 命中 = 0 (基线 16)。普查脚本与 SC-3 测试同源。(v2 曾附「裸 errors= 混用」判据, R2 A2 席指出无定义, 已删 — `errors=` 轴的角色是 SC-9 的 census 报告维度, 不是本条的红绿判据。)
- **SC-3 (防再长, 三态实测)**: 执行口径写死 —— 基线树 = `git -C aria archive 3b97c35 | tar -x -C <隔离 tmpdir>` (不用 repo.parent, 不污染工作树); (a) 对基线树跑 = 红 (16 命中); (b) 对迁移树跑 = 绿; (c) 向迁移树副本任一生产脚本注入一处 `text=True` → 必红。三态留痕。
- **SC-4 (sink 链端到端)**: 对**静态追验过的唯一真实链** (符号锚定, 防迁移后行号漂移): aether.py `_run_with_retry` 的 subprocess 输出 → pre_merge_gate.py `gate_check` 的 raw_message → `json.dumps(ensure_ascii=False)` 出口。fixture: mock CLI 须先让 capability check (`_verify_in_flight_flag`) 通过、再在查询段吐 `b"\xff"` (R2 A3 席实证: capability check 段短路会使查询段不执行)。喂非 UTF-8 → 无异常走完, JSON 出口含转义字面。**fixture 构造前置**: 任何 sink fixture 必须先在 spec/tasks 引用静态调用链 (符号逐跳), 禁止按想象造链 (R1 A2-C1: v1 的第二条链无可达路径; R2 A2/A3 双席独立发现 v2 并列的 `_verify_in_flight_flag` leg 的解码内容只进布尔判定、不流向 sink, 均已删)。
- **SC-5 (零回归)**: 全仓 test suite 绿; 基线计数在 B.1 入场时对冻结快照 `3b97c35` 的树实测记录 (非活分支), 迁移后不低于该数。
- **SC-6 (except 面不变, 机械)**: 迁移前后比较 except 元组成员集合的 **multiset**, 匹配键 = **(文件路径, enclosing 函数名, 函数内站点序号)** — 行号漂移免疫且站点级可辨 (R2 A2 席反例: 文件级 multiset 对「同文件两站点元组互换」不可见, aether.py `_verify_in_flight_flag` 三元组 vs `_run_with_retry` 单元组即真实语料); **13 个目标文件 / 16 个站点**逐站点相等。
- **SC-7 (文档勘正落地)**: traps.md #5 新措辞含「dumps 默认路径不炸」与 encode sink 点名; pre_merge_gate docstring 追加而非改写局部描述; 勘正执笔人 ≠ 实现执笔人。
- **SC-8 (无 try 点处置)**: validate_schema_doc.py:130 迁移后解码结构性不可抛。spawn 类异常 (FileNotFoundError 等) **spec 层默认 = 保持裸抛 + 行注声明** (dev-time 校验脚本, loud failure 可接受); A.2 若推翻此默认须在 tasks 记理由。
- **SC-9 (census 入库 + kwarg 轴, R1 新增)**: 普查脚本作为 spec 交付物入库 (tests/ 或 scripts/), 且检测轴含 `errors=`/`encoding=` kwarg (缺此轴正是 v1 把 coordination_ref.py:255 误判「接不住」的根因); 对冻结基线跑复现四层计数 7/4/1/4。**机制边界声明 (R2 A1/A3 席)**: L3/L4 与词法 except 轴由脚本机械推导; **L1/L2 的区分 (调用链顶层捕获) 不做通用调用图分析** — 以 §Why 四层表为人工标注输入, 脚本结构性回验标注点位存在且词法特征相符, 标注表变更须人工重核。

## rule6_note (Rule #6 豁免判据申报)

本 spec 全部变更为 **Python 脚本代码面 + reference 文档勘正**, 不触碰任何 SKILL.md description / 运行时指令流程:

| 变更内容 | 性质 | 处置 |
|---|---|---|
| 16 处调用点迁移 + helper + 结构化测试 + census 入库 | deterministic 代码 | substitute: SC-1..SC-6/SC-9 baseline-failing 结构化测试 (AB 套件测不到 Python 脚本内部行为) |
| traps.md #5 / pre_merge_gate docstring 勘正 | 描述性勘误 | substitute: SC-7 结构化断言 |

无 `description` / 指令流程变动 ⇒ 无需照跑 AB。SOT: `standards/conventions/skill-benchmark-exemption.md`。

## Impact

- **版本**: aria-plugin PATCH (bug 修复)。目标版本**不写死** —— bump 前 re-check SOT 并顺延重算 (#128 版本撞车教训)。
- **行为变更申报 (三类)**: (1) L1 层: 未捕获崩溃 → 转义字面继续执行 (fail-safe 方向); (2) L2 层: 整流程报废 → 单点降级继续 (可用性提升); (3) L3 层: `�` 替换字符 → `\xff` 转义字面 (呈现形态变化, 信息量增)。无「由拦变放」类风险面。
- **同步面**: aria 子模块 (代码 + 测试) + 主仓 gitlink; standards 无涉; CHANGELOG 两类。

## Tasks (A.2 细化为 detailed-tasks.yaml; 此处为骨架)

- [ ] 1.1 helper 标准形态定稿 + SC-1 fixture (L1 对照红)
- [ ] 1.2 census 脚本入库 + kwarg 轴 + 四层计数复现 (SC-9)
- [ ] 1.3 迁移 L1 层 7 处 (逐处保留既有 except 元组)
- [ ] 1.4 迁移 L2 层 4 处 + L3/L4 层 5 处 (统一模式)
- [ ] 1.5 SC-8: validate_schema_doc.py 处置 (默认裸抛+注释)
- [ ] 1.6 结构化测试落地 (SC-2/SC-3 三态, 排除式谓词)
- [ ] 1.7 SC-4 sink 链 fixture (静态链引用前置)
- [ ] 1.8 文档勘正 (SC-7, 换人执笔)
- [ ] 1.9 全仓回归 + 关键脚本 smoke (SC-5, 冻结快照基线计数)
- [ ] 1.10 ship: 版本 re-check + 顺延 bump + 多远程双推 + ls-remote 核验
- [ ] 1.11 转出: 其他仓库同类缺陷逐仓开 issue

---

**起草**: 2026-08-20 v1 (主 loop); v2 = post_spec R1 三席 findings 修订 (主 loop 执笔, R1 报告为修订依据)
