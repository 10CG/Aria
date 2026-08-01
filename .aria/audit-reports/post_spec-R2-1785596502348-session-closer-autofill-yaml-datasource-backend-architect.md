---
verdict: PASS
agent: backend-architect
round: R2
critical_count: 0
major_count: 0
minor_count: 2
r1_resolved: 3/3
---

# post_spec R2 — session-closer-autofill-yaml-datasource (backend-architect: R1 复审 + 新设计核验)

审计对象: `/home/dev/Aria/openspec/changes/session-closer-autofill-yaml-datasource/proposal.md` (R1 REVISE 后修订版)。

方法: 逐条对照 R1 三项 findings (M-1/m-1/m-2) 在修订版原文定位并回代真代码验证; 另对 §What 3 (三态 sentinel) 与 §What 5 (`_load_detailed_tasks_api` 契约) 做独立设计审。必读代码全读: `handoff_autofill.py` 全文、`detailed_tasks.py` L1-274、`spec_complete.py` L190-220。

---

## R1 Findings 复核

### M-1 (parse_ok=False 第三态未分诊) — RESOLVED

§What 3(c) 新增显式分支: `parse_ok=False` (无/重复 `tasks:`、零 `- id:`、结构自不一致) 产 sentinel item, 不再与真 0 条混同; SC-7 新增 baseline-failing fixture (零 `- id:` + 重复 `tasks:` 键两个畸形样本) 锁定"未修必 FAIL"。回代真代码确认: `parse_detailed_tasks` (`detailed_tasks.py` L234-273) 三条 `parse_ok=False` 分支 (L238-240 bounds-None / L245-247 零 id / L253-259 结构自不一致) 均只改写 `reason`、`tasks` 恒 `[]` —— 与 R1 证据一致, 修订后的消费逻辑 (先查 `parse_ok` 再遍历) 结构性堵死"损坏当 0 条"路径。先例引用 `spec_complete.py::_yaml_only_tasks_verdict` 行号 (proposal "L204-212") 与实际 `if not parsed["parse_ok"]:` 判据落在 L207-212, 误差 1-3 行、不影响引用有效性。**确认解决。**

### m-1 (title 空产尾随空格) — RESOLVED

§What 2 拼接公式改为 `id if not title else f"{id} {title}"` (非无条件 `f"{id} {title}".strip()`)。回代 `detailed_tasks.py::_extract_block_title` (L191-195): title 缺失返回 `""`, Python 空字符串为 falsy, 新公式在此分支直接短路取 `id`, 无尾随空格产生。SC-1 显式断言 "title 缺失项 item == task id (无尾随空格)"。**确认解决, 且实现方式比"拼接后 strip"更干净 (零多余字符串分配)。**

### m-2 (sys.path 插入顺序偶然无结构保证) — RESOLVED (以文档化方式)

§What 4 末段新增强制要求: "实现须加显式顺序依赖注释", 明示本文件单次 `assemble_from_snapshot` 内三处插入 (新 yaml fallback / `_benign_unconditional_reasons` / `owner_container`) 当前互不冲突是执行顺序偶然、非结构不变量, 直接引用 "R1 backend m-2"。回代 `handoff_autofill.py::assemble_from_snapshot` (L329-362) 确认真实调用顺序与 R1 报告描述一致: `grep_unchecked_tasks` (L342, 未来含 yaml fallback insert) → dict 字面量求值时 `fill_sync_section` (L356, 触发 `_benign_unconditional_reasons` insert) → `owner_container()` (L361, 三处insert 中最后一个, 把 `state-scanner` 根插到 position 0)。这是**约定文档化**而非结构性根治 (仍是顺序敏感, 只是现在有显式注释兜底防未来重排), 但这正是 R1 建议的解法本身 ("建议在 `owner_container()` 或本文件顶部留一条顺序依赖的显式注释")。**确认解决 — 已达 R1 建议的解决标准。**

**r1_resolved: 3/3。**

---

## 新设计核验

### §What 3 三形态统一 sentinel 通道 (a/b/c)

枚举完备性核验: 对照 `parse_detailed_tasks` 真实代码路径, a(跨 skill 导入失败) / b(OSError) / c(`parse_ok=False`) 三态覆盖了"yaml 存在但不可用"的全部结构性来源 —— 未发现遗漏的第四态。经代码验证的边界情形均落在既有三态内:
- 0 字节 yaml → `parse_detailed_tasks("")` → `parse_ok=False` (态 c), 非独立态。
- `parse_ok=True` 时 `tasks` 恒非空 (`_TASK_ID_LINE_RE` 要求 `\S+`, 零匹配已被 L245-247 拦截为 `parse_ok=False`) —— 不存在"parse_ok=True 但 tasks=[]"的假 0 场景, 决策 2 happy-path 公式不需要额外防御。
- 断链软链接 (broken symlink) → `os.path.isfile` 返回 False → 落入"两者都缺"(SC-9), 非 a/b/c 场景 — 属于正确分诊 (物理上没有可用 yaml), 非遗漏。

**结论: a/b/c 三态划分完备, 无第四态缺口。**

### §What 5 `_load_detailed_tasks_api()` 契约

`(parse_fn, done_fn) | None` 返回形态对当前消费需求 (需要 `parse_detailed_tasks` + `is_done_status` 两个函数) 恰好够用, 无多余面。SC-5 "monkeypatch 该 helper 而非操纵 sys.path" 的测试策略正确绕开了 R1 qa M-2 指出的 `sys.modules` 缓存维度 (成功 import 一次后模块驻留, 事后改 path 模拟不了降级) —— 契约设计本身就是为了让失败注入可测, 而不依赖 import 副作用。未发现新失败面: helper 内部对 sys.path 插入 + 裸名 import 的封装与既有两处先例 (`_benign_unconditional_reasons`/`owner_container`) 同构, 沿用已验证安全的插入位置 (`state-scanner/scripts/lib`, 非顶层 `lib`)。

---

## Minor (新发现, 均非阻塞)

### m-1 (新): sentinel item 的精确文本格式未达 happy-path 公式同等精度, "reason 透传"语义模糊

**位置**: §What 3, "item 注明形态与 reason...(「需人工核对」)"。

决策 2 (happy path) 给出精确公式 `id if not title else f"{id} {title}"`, 可直接照抄实现、可逐字断言。决策 3 (sentinel 通道) 只描述"item 应包含形态 + reason + 需人工核对"这一意图, 未给出可逐字实现的模板 (例如: `f"{name}: detailed-tasks.yaml 解析失败 ({reason}) — 需人工核对"` 这类具体串)。SC-7/SC-8 的断言口径 "reason 透传"同样未定义是要求 `parsed["reason"]` 原始字符串逐字出现在 item 里, 还是允许改写/包装。三个触发态 (a/b/c) 若各自实现时选择不同措辞风格 (例如 a 态写"导入失败", b 态写"读取失败", c 态写"解析失败"但格式不统一), 后续人工扫读 handoff 时的可辨识度会打折扣, 也给 SC-7/SC-8 的断言精度留了解释空间。

**建议**: Phase B 实现前补一条统一 sentinel item 模板 (哪怕只是 `f"{name}: <形态描述> ({reason}) — 需人工核对"` 这一行), 三态复用同一格式化函数, SC-7/SC-8 断言"reason 逐字出现在 item 内"而非泛泛"reason 透传"。

### m-2 (新, 纯措辞): "四态" 计数与 `parse_detailed_tasks` 实际代码分支数不一致 (3 分支, 非 4)

**位置**: §What 3(c) "无/重复 `tasks:` 块、零 `- id:`、结构自不一致 四态"。

回代 `_tasks_block_bounds` (L198-222): "无 `tasks:` 块"与"重复 `tasks:` 块"共享同一个 `bounds is None` 返回分支与同一条 `reason` 文案 (L239: `"no single unambiguous top-level `tasks:` block (absent or duplicated)"`), 物理上是 1 个代码分支覆盖 2 种触发条件, 加上"零 `- id:`"(L245-247) 与"结构自不一致"(L253-259) 共 3 个真实分支, 非 4 个独立分支。纯计数措辞误差, 不影响消费逻辑正确性 (消费方只判 `parse_ok` 布尔值, 不区分具体分支), SC-7 现有两个 fixture (零 id-entries + 重复 `tasks:`) 已足够覆盖代表性路径 (未覆盖的"结构自不一致"分支属于 SOT 自身 #113 血缘已充分测试的既有行为, 此处消费方零分支逻辑决定了重测无增量收益)。**不建议为此单独加 SC, 但建议措辞改"三条分支 (覆盖四种输入形态)"避免误导后续读者以为有 4 条独立控制流。**

---

## 结论

R1 三项 findings (1 major M-1 + 2 minor) 全部真实解决, 均可回代真代码验证, 无表面合规。新增设计 (三态 sentinel 枚举 + helper 契约) 结构完备, 未引入新的 major/critical 缺口。本轮新发现两条 minor (sentinel 文本模板精度 / "四态"措辞计数误差), 均为非阻塞的实现前打磨项, 不构成收敛阻断。**verdict: PASS。**
