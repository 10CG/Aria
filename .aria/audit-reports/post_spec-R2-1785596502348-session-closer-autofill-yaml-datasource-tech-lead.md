---
verdict: PASS
agent: tech-lead
round: R2
critical_count: 0
major_count: 0
minor_count: 4
r1_resolved: 7/8
---

# post_spec R2 · tech-lead 复审 (convergence mode)

审计对象: `openspec/changes/session-closer-autofill-yaml-datasource/proposal.md` (aria-plugin #121, Level 2)
基线: 本人 R1 报告 `post_spec-R1-1785595534360-...-tech-lead.md` (M-1 / M-2 / m-1~m-5 + 1 条建议)

本轮实读代码 (非依赖 R1 记忆, 逐条重验):
`handoff_autofill.py` 全文 392 行 / `lib/detailed_tasks.py` 全文 274 行 / `lib/spec_complete.py` L140-185, L189-232, L340-362, L438-452 / `collectors/openspec.py` L1-45 / `collectors/__init__.py` / `collectors/handoff_multibranch.py` L80-100 / `scripts/lib/` 目录清单 + `__init__.py` 字节数 / `session-closer/tests/test_handoff_autofill.py` L220-255。

结论: **R1 两条 Major 均实质解决, 无一条以措辞掩盖**; 5 条 minor 中 4 条解决、1 条 (m-4) 只解决了一半 (方向勘正对了, 替换上去的新依据不成立)。修订未重开 R1 findings 的同类 bug。新增 4 条 minor, 均不阻断 Approved, 但 m-2 需在 Phase B 落地前裁决一次 (否则 SC-8 必红)。

---

## 一、R1 findings 逐条核对 (对照真代码, 不看措辞看判据)

### M-1 `parse_ok=False` 未处理 — 已解决 ✅

- §What 2 现明写返回值是**包装 dict** `{parse_ok, tasks, reason}`, 且「仅当 `parse_ok=True` 时遍历 `tasks`」。与 `detailed_tasks.py` L225-273 的真实签名逐字一致 (L234 `result = {"parse_ok": False, "tasks": [], "reason": ""}`)。
- §What 3 把 sentinel 从「只覆盖导入失败」泛化成三形态闭包, (c) 明确列了 `parse_ok=False` 的四态, 并点出**关键判据**「`tasks` 恒 `[]`, 与真 0 条返回形态不可分」——这正是 M-1 的病理本体, 不是复述症状。
- 对照真代码四条 file-level 失败路径: L237-240 (无/重复 `tasks:`, `_tasks_block_bounds` L209-215 的 duplicate 短路)、L246-247 (零 `- id:`)、L254-259 (结构自不一致)。SC-7 的两个 fixture (零 `- id:` / 重复 `tasks:` 键) 分别命中前两条, 且要求 reason 透传 + baseline FAIL。第三条 (structural self-inconsistency, 现实最易撞的隐藏条目类) **没有专属 fixture** — 但它与前两条共用同一 `parse_ok=False` 分支与同一 sentinel 出口, 属同一等价类, 不再重开 (记录于此, 供后续轮次不必再提)。
- 先例引用 `spec_complete.py::_yaml_only_tasks_verdict L204-212` 核实无误: 函数 def 在 L189, L204-205 OSError → 显式 reason, L208-212 `parse_ok=False` → 显式 reason。

### M-2「第四处 = 收口」封闭性不成立 — 已解决 ✅

- §Why 新增「范围界定」段, 显式命名第三形态 (proposal-inline), 承认本 spec 自身即实例, 并给出**真实理由**而非托词: proposal 内 `- [ ]` 混含 Success Criteria 复选框, 无差别扫会把验收标准灌进 carry-forward。这正是 R1 要求的两条之一, 且理由与我 R1 给的一致 (不是抄措辞 — 它进一步点明「需独立语义设计」)。
- Tasks 1.4 + §Impact 收尾项双处挂住 follow-up issue, 满足 R1「否则第五处会以同样方式重开」的要求。
- 关键决策表新增「范围」行, 使 scope 决策进入可追溯面。
- 遗留 (不构成 finding): R1 顺带建议的「SC-2 在本仓真实目录 `aria-2.0-m6-dispatch-input-delivery` 上跑一次」未采纳, 改为全 tempdir。此处**我撤回该建议** —— 与 memory `feedback_test_worktree_fixture_isolated_tmpdir` 冲突, 且 SC-2 的断言不依赖真实语料形态。修订选择更优。

### m-1 行号漂移 — 已解决 ✅

逐条复核修订后的引用:

| 引用 | 真代码 | 判定 |
|------|--------|------|
| `spec_complete.py` L350-356 | L350-356 = `_TASK_ID_LINE_RE` 的 try/except dual-context import | 准确 |
| `spec_complete.py` L441-451 | L441-451 = `_split_task_blocks, is_done_status, parse_detailed_tasks` 的 try/except | 准确 |
| `collectors/openspec.py:18-31` | L18-37 header note, 「Deliberately NOT `from lib.carry_forward`」在 L27-30 | 准确 (含尾行) |
| `handoff_autofill.py` L46-50 (`_benign_unconditional_reasons`) | L48 路径计算 / L49-50 插入 | 准确 |
| `handoff_autofill.py` L317-321 (`owner_container`) | def L305, L317 注释, L318 `_ss_root`, L319-320 插入, L321 `from lib.identity` | 准确 |

R1 指出的「表格 L342 指到 `_CODE_EXT_RE`」与「正文/表格自相矛盾的 L319-321」两处均已消除, 表格与正文现在同源。

### m-2 `lib` 毒化论证选错证据 — 已解决 ✅

修订把理由改写成「`lib` 顶层名绑到哪个是 **sys.path 插入顺序敏感的不确定行为**」, 并引 `collectors/openspec.py:18-31` 作权威论证。这与真代码完全吻合 (`state-scanner/lib/` 有 `identity.py` 无 `detailed_tasks.py`; `scripts/lib/` 反之), 且不再依赖 R1 已证伪的「必然 ImportError」说法 —— 实施者按图索骥不会把理由证伪。结论 (禁用 `from lib.detailed_tasks`) 保留, 论证换成站得住的那条。

新增的两条支撑也核实通过: `scripts/lib/__init__.py` 实测 **0 字节** ✓; `detailed_tasks.py` L33-35 只有 `from __future__` + `import re`, 零回边 ✓; 裸模块名导入不执行目录的 `__init__.py` ✓。

### m-3 OSError 处置未规定 — 已解决 ✅ (一处建议未采纳, 见 nits)

§What 3 (b) 明确禁止照抄 tasks.md 分支的静默 `continue` (L171-172), 并归入统一 sentinel 通道; SC-8 配了独立断言。核心诉求达成。

### m-4 SC-6 memory 方向反了 — **部分解决** ⚠️

- 方向勘正**做对了**: SC-6 现明写「该 memory 说的是改 SOT 方须扫消费方 — 方向相反」, 依据不再挂错。这是 R1 的主诉求。
- 但**替换上去的新依据不成立**, 详见下方 m-3 (new)。

### R1 建议 (记录被否决的 snapshot-加字段路线) — 已采纳 ✅

关键决策表新增「否决: snapshot 加字段路线」行, 且理由写到了实处 (schema additive bump + 两 skill 发版耦合 + AD-2 backstop 定位), 不是一句「更复杂」。后续 review 重开该讨论的成本已被封住。

---

## 二、修订本身引入的新问题 (4 Minor, 均不阻断)

### m-1 (new) `sys.path.insert(0, scripts/lib)` 的顺序风险, 用「加注释」兜不住 — 存在结构性更优解

位置: §What 4 第 2/3 条 + 关键决策表「import 路径」行

修订自己承认了关键事实:「当前互不冲突是**执行顺序偶然而非结构不变量**」, 然后开出的处方是「加显式顺序依赖注释」。注释不改变不变量的有无 —— 而本 spec 的整个论点恰恰是「不许依赖偶然、失败必须显性」, 这里对自己放宽了一档。

真代码把风险坐实 (R1 我漏了这一层, 是复核 §What 4 第 3 条时才挖到):

- `collectors/__init__.py` 无条件 `from .handoff_multibranch import collect_handoff_multibranch` ⇒ `from collectors.multi_remote import ...` 会**连带执行** `handoff_multibranch.py`;
- `handoff_multibranch.py` L92-100 是**带守卫的**插入: `if _SS_ROOT not in _sys.path: insert(0, _SS_ROOT)`, 随后 `from lib.collision import classify`。守卫意味着: 只要 state-scanner root 已在 sys.path 但排在 `scripts/lib` **之后**, 它就不会重新前置 ⇒ 顶层 `lib` 绑到 `scripts/lib` (那是个合法包, `__init__.py` 存在) ⇒ `lib.collision` ImportError, 且**失败的子模块导入仍会把 `lib` 留在 `sys.modules`** ⇒ 之后 `owner_container()` 的 `from lib.identity` 一并失效, 静默返回 None。
- 真实执行顺序: `grep_unchecked_tasks` 在 L342 被调用, **早于** L356 的 `fill_sync_section` 和 L361 的 `owner_container` —— 即新插入是三者中的**第一个**。默认单次 CLI 路径仍安全 (handoff_multibranch 首次插入 root 时 root 尚不在 path), 所以这不是 Major; 但一旦有外部 sys.path 布置方 (test 的 conftest / phase-d-closer 包装进程 / 未来第三处消费方) 先把 state-scanner root 放进去, 上述降级即触发。
- 另: proposal 说「本文件单次 `assemble_from_snapshot` 内将存在三处 sys.path 插入」。限定在「本文件」是准的, 但**决定绑定结果的是传递触发的那些**: `handoff_multibranch.py:97`、`spec_complete.py:147/157/171/180`、`custom_checks.py:112`。注释若只列本文件三处, 读者仍看不见真正的顺序面。

建议 (任选, 都是几行, 不扩 scope):
1. **首选**: 完全不碰 sys.path —— `importlib.util.spec_from_file_location("detailed_tasks", <abs path>)` 按绝对路径加载。既消除顺序敏感, 也不把 `spec_complete` / `carry_forward` / `runtime_probe` 等通用名注入顶层命名空间; 顺带让 §What 4 第 3 条的「注释」需求归零。
2. 退一步: 用 `sys.path.append` 而非 `insert(0)` (本仓无第二个 `detailed_tasks` 顶层模块, 追加即可解析, 却不可能遮蔽任何已有条目)。
3. 若坚持 `insert(0)`, 则注释须点名上面那批**传递插入方**, 而非只列本文件三处。

### m-2 (new) SC-8 的「目录」fixture 与 §What 1 的分支进入条件互相矛盾 — 且真实 OSError 前置仍留静默 0

位置: §What 1 (「`detailed-tasks.yaml` 存在 ⇒ 走 yaml 分支」) vs SC-8 (「`detailed-tasks.yaml` 为目录 → sentinel」)

「存在」未定义成 `exists` 还是 `isfile`。本函数既有惯例 (L166-167 `os.path.isfile(tasks)`) 与姊妹消费方 (`spec_complete.py` L200 `yaml_path.is_file()`) **都是 isfile**。实施者照惯例写 `isfile` ⇒ 目录不是 file ⇒ 落入「两者都缺 ⇒ 零条目」⇒ SC-8 必红且**无法靠实现修好**, 只能改判据。这正是「baseline 也过就删断言」磨钝测试集的入口 (memory `feedback_ab_baseline_contaminated_...` 同型风险)。

更实质的一面: 真正现实可达的 OSError 前置是**权限拒绝 / 断链 symlink / I/O 错误**, 其中断链 symlink 在 `isfile` 下同样返回 False ⇒ yaml 名义在场却静默报 0, **本 spec 要杀的病根残留一条**。

建议: §What 1 显式写死分支进入条件 (推荐 `os.path.lexists`/`exists`, 与 §What 3「yaml 在场 ⇒ 要么真实条目要么 sentinel」自洽), 或把 SC-8 fixture 换成 chmod 000 / 断链 symlink 并同步条件。二选一即可, 但必须在 Phase B 落地前裁决, 不要留给实现临场决定。

### m-3 (new, 承接 m-4 未尽部分) SC-6 的新依据不成立 — 真正的红灯是 SC-1, 不是 state-scanner 回归

位置: SC-6 方向说明

现文: 跑 state-scanner 侧「是防其 lib 未来迁移时本侧只静默降级无红灯的基线留存」。这条推不通: `lib/detailed_tasks.py` 若迁移/改名, state-scanner 自己的测试会随迁移一并更新并保持绿 —— 它对 session-closer 的降级**零信号**。

真正让路径断裂即红的是 **SC-1 本身**: 它在真实 skill 布局下跑 (fixture 只隔离 `changes_dir`, 导入路径仍由 `Path(__file__).resolve().parents[2]` 实算), 路径一断 ⇒ 走 sentinel ⇒ SC-1 断言的「2 条 + source=`detailed-tasks.yaml:{name}`」立刻失败。这是结构性成立的, 只是没被写出来。

建议: SC-6 依据改写成「保险成本近零的邻接回归」即可 (诚实且够用), 同时把「路径断裂由 SC-1 兜红 (fixture 不 mock 跨 skill import)」补进 SC-1 一句话。可选加固 (R1 原建议仍有效, 成本一行): 在 `lib/detailed_tasks.py` docstring 加 external-consumer 契约注记 —— 该文件 L2-32 已有大量此类注记惯例, 融入无违和。

### m-4 (new) sentinel item 缺可判别标记 — 测试与下游只能靠自由文本认它

位置: §What 3 + SC-5 / SC-7 / SC-8

三条 SC 都断言「产 sentinel item」, 但 spec 只规定了 item 是人话 (「注明形态与 reason / 需人工核对」), 未规定 `source` 取什么值, 也未给稳定判别位。后果: 测试只能断子串, 措辞一改就假绿或误红; §2 渲染时 sentinel 与真实残留项混在同一 `source` 名下, 人类读 handoff 分不清「有 3 条待办」和「有 1 条读不出来」。

建议 (零成本): 在 §What 3 定死 `source`, 例如 `detailed-tasks.yaml:{name}:unavailable`, 并让三条 SC 断言该 source 前缀而非 item 措辞。schema 仍是 `{source, item}`, 兼容性结论不变。

---

## 三、Nits (不计入 minor_count, 供顺手改)

1. §What 2 引「`assemble_unfinished` (L224-240)」— 真区间 def L223 / 体 L225-238, 松散超集, 不影响判断。
2. §What 4「L441-451 (同三符号)」措辞可歧义 (该块导入的是 `_split_task_blocks` / `is_done_status` / `parse_detailed_tasks` 三个, 与本 spec 要用的两个不同名)。改成「同款 dual-context 写法」更准。
3. R1 m-3 建议的「tasks.md 分支既有静默 `continue` 属存量问题, §Impact 记一笔」未采纳。§What 3(b) 实际已把它判成「第三条假绿路径」却不修 —— 同一函数内两套 OSError 政策, 建议 §Impact 一行说明 scope-out 理由, 免得下个 reviewer 当新发现重开。

---

## 四、本轮复核通过、明确不再重开的部分

1. **M-1 修订未重开同类 bug**: 三形态闭包是「yaml 在场 ⇒ 无返回空的路径」的全称约束, 而非再枚举几种已知失败模式 —— 抗未来新增失败模式。
2. **§What 5 的 helper 缝论证正确**: 「成功导入过一次后模块驻留 `sys.modules`, 改 path 模拟不了后续失败」属实, monkeypatch `_load_detailed_tasks_api` 是唯一能可证伪测到降级的缝。SC-5 相应改写, 未留「改 sys.path 测降级」的假绿。
3. **顶层命名空间碰撞实测为空**: `scripts/lib/` 内模块名 (`carry_forward` / `detailed_tasks` / `frontmatter_block` / `runtime_probe` / `spec_complete`) 与 `session-closer/scripts/` 内 (`closeout_trigger` / `consistency_check` / `handoff_autofill`) 无交集, 故 m-1 的风险仅限 `lib` 包绑定一路, 不含模块遮蔽。
4. **重复模块实例无害**: 顶层 `detailed_tasks` 与 `lib.detailed_tasks` 可能并存为两个模块对象, 但本 spec 只用纯函数 + 白名单常量, 无 identity 断言消费方 (`spec_complete` 的 SC-9 边界一致性测试在 state-scanner 自己的进程内)。
5. **R1 已核对通过的 6 项 (耦合方向 / 不双写 parser / 决策 2 与 #113 决策 6 同型 / 输出 schema 兼容 / 决策 5 fail-CLOSED / Rule #6 substitute + PATCH 定级) 本轮抽验未变**, 修订未触碰这些面。
6. **SC-1 fixture 设计与 parser 真实行为自洽**: title 缺失 → `_extract_block_title` L191-195 返回 `""` (非 None) → item 只出 id, 与 §What 2 的 `id if not title else f"{id} {title}"` 一致; 两 task 且 `id` 为首字段 ⇒ 结构自洽性计数通过, 不会误落 `parse_ok=False`。
