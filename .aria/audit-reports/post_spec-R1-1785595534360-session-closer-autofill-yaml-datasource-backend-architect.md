---
verdict: REVISE
agent: backend-architect
round: R1
critical_count: 0
major_count: 1
minor_count: 2
---

# post_spec R1 — session-closer-autofill-yaml-datasource (backend-architect: import 机制与模块设计)

审计对象: `/home/dev/Aria/openspec/changes/session-closer-autofill-yaml-datasource/proposal.md`

审计视角: sys.path 插入的污染面与顺序问题 / `lib` 顶层名毒化坑的解法是否真成立 (决策 3) / lazy import 时机 / 降级 sentinel 设计 (决策 4) 的失败模式 / `detailed_tasks.py` 公开 API 是否够用 / 循环导入论证是否属实。

方法: 逐行核对 proposal.md 引用行号against `handoff_autofill.py` 全文、`detailed_tasks.py` 全文、`spec_complete.py` L128-190+L340-360、`collectors/openspec.py` L20-60、`frontmatter_block.py` 全文, 并追溯到 #113 archived proposal 的「决策」记录核实血缘引用是否真实存在。

---

## Major

### M-1: `parse_detailed_tasks` 返回 `parse_ok=False` (yaml 存在但不可解析) 时的行为未在决策 2/4 中定义, 且 SC-1~SC-6 无一覆盖 — 有重新制造「静默 0」同类假绿的具体路径

**位置**: proposal.md 决策 2 ("yaml 分支" 段) + 决策 4 ("降级方向") + Success Criteria SC-1~SC-6。

**主张**: `detailed_tasks.py::parse_detailed_tasks` 在四种文件级失败态 (无 `tasks:` 块 / 重复 `tasks:` 块 / 零 `- id:` 条目 / indent-anchored 结构自不一致) 下均返回 `{"parse_ok": False, "tasks": [], "reason": "..."}` — `tasks` 恒为空列表, 与「yaml 全部任务真的是 0 条」在返回形态上**完全不可区分** (真代码证据, `detailed_tasks.py` L234: `result: dict = {"parse_ok": False, "tasks": [], "reason": ""}`, 后续 3 个 early-return 分支 [L239, L246, L259] 均不改写 `tasks`)。

proposal 决策 2 只描述了 `parse_ok=True` 的 happy path ("`parse_detailed_tasks(text)` 逐 task 取 `{id, raw_status, title}`"), 决策 4 的 fail-closed sentinel 设计**只覆盖「跨 skill 导入失败」一种降级路径**, 未提及「导入成功但解析失败」这个独立失败态。若实现时朴素地写 `for t in parse_detailed_tasks(text)["tasks"]: ...` 而不先检查 `parse_ok`, 一份**存在但损坏**的 `detailed-tasks.yaml` (如误产生重复 `tasks:` 顶层键, 或 `- id:` 行被折行拆开触发 indent-anchored 自不一致守卫) 会被静默报 0 条残留 —— 这正是本 issue (#121) 与其上游 #113 存在的理由: 「yaml-only spec 静默假绿 0」。此路径没有被 SC-1~SC-6 中任何一条钉住 (SC-1 测的是干净 yaml / SC-3 测 done-family / SC-4 测 status 白名单 fail-CLOSED, 三者前提都是 `parse_ok=True`)。

**真代码证据 — 同血缘的 #113 已建立且证明必要的先例**: 本 proposal 自称是 #113 "同根因谱系第四处消费方", 且明示 "复用 #113 parser SOT, 不第二次实现 yaml 解析"。但 #113 archived proposal (`/home/dev/Aria/openspec/archive/2026-07-22-state-scanner-gate-yaml-datasource/proposal.md` L57) 对**同一个** `parse_ok=False` 场景有明文独立分支:

> `parse 失败`: 退回 v1.61.0 行为 — `{"claim": "archive-safety-net-source-unparseable", "reason": "detailed-tasks.yaml 存在但解析失败 (<reason>) — 完成声称无法核验; 需人工复核", "symbols": []}` + `verdict=warn` + 非 None d_payload + soft_error。

即 #113 的姊妹消费方 (`spec_complete.py::_yaml_only_tasks_verdict`, L207-212 亦印证: `if not parsed["parse_ok"]: return (False, f"...unparseable ({parsed['reason']})")`) **显式**把 `parse_ok=False` 当成第三态处理, 不与「0 条残留」混同。本 proposal 没有把这条已验证必要的先例带过来, 是本次 fallback 分支设计相对于其声称复用的 SOT 血缘的一个真实缺口, 而非臆测边角情形 —— parser 自身的三个 fail-closed 结构性守卫 (重复 `tasks:` / 零条目 / indent 自不一致) 正是为「宁可拒绝解析也不要吐出错误数据」而设计的, 消费方若不检查 `parse_ok` 就等于让这些守卫的存在毫无意义。

**建议**: 决策 2/4 显式加一条 — `parse_ok=False` 时对该 yaml-only spec 产 sentinel item (与决策 4 现有「跨 skill 导入失败」sentinel 同构, 消息文案区分为「detailed-tasks.yaml 存在但解析失败 (<reason>) — 需人工核对」), 并补 SC-7 (fixture: 重复 `tasks:` 顶层键或零 `- id:` 条目的畸形 yaml → 报 sentinel 而非 0 条)。

---

## Minor

### m-1: `item` 字段格式 `"<id> <title>"` 在 `title` 为空字符串时产生尾随空格

**位置**: 决策 2 "输出 `{"source": ..., "item": "<id> <title>"}`"。

`detailed_tasks.py::_extract_block_title` 在无 `title:` 字段时返回 `""` (非 `None`, L191-195: `if raw is None: return ""`)。若某 task 条目无 `title` 字段, 拼接结果会是 `"TASK-003 "` (尾随空格) 而非干净的 `"TASK-003"`。纯展示层瑕疵, 不影响 `_item_key` 归一化比对 (该函数会 `.strip()`), 建议实现时对拼接结果做一次 `.strip()`。

### m-2: 新增 sys.path 插入点在单次 `assemble_from_snapshot` 调用中与既有两处叠加, 累积三个 state-scanner 相关目录

**位置**: `handoff_autofill.py::assemble_from_snapshot` (L329-362) 现有执行顺序。

`assemble_from_snapshot` 在一次调用内, 按代码顺序会依次触发: `grep_unchecked_tasks` (L342, 若命中 yaml-only spec, 新增插入 `state-scanner/scripts/lib`) → `fill_sync_section` (返回字典 "sync" 键求值时, 触发 `_benign_unconditional_reasons` 插入 `state-scanner/scripts`) → `owner_container()` (返回字典 "frontmatter" 键求值时, 插入 `state-scanner` skill root)。三次 `sys.path.insert(0, ...)` 全部落在同一进程且从不回滚 (Python sys.path mutation 无自然过期机制), 使该进程后续任何代码的裸模块名解析都要考虑这三层目录。

**验证结论 (非阻塞)**: 已逐一验证这三次插入在当前实现下彼此不冲突 —— `grep_unchecked_tasks` 分支用裸名 `detailed_tasks` (非 `lib.` 限定), 且发生在另外两次插入**之前**, 结果被 `sys.modules` 缓存, 不受后续插入影响; `owner_container()` 是三者中最后执行且始终把 `state-scanner` 插到 position 0, 使 `from lib.identity import ...` 稳定解析到 `state-scanner/lib` (Layer L) 而不会被更早插入的 `state-scanner/scripts` 抢先 (`scripts/` 下也有一个同名 `lib/` 子目录, 顺序颠倒会解析错)。当前顺序安全, 但这是**执行顺序偶然保证**而非结构性不变量 —— 若未来任何一次插入顺序被重排 (例如把 `owner_container()` 调用移到 `grep_unchecked_tasks` 之前), `from lib.identity import get_identity` 有被 `state-scanner/scripts/lib` (而非 `state-scanner/lib`) 抢先绑定的风险。建议在 `owner_container()` 或本文件顶部留一条顺序依赖的显式注释, 防止未来重排引入静默错误。

---

## 已核实、无发现的主张 (含验证证据摘要)

- **决策 3 `lib` 顶层名毒化坑真实存在, 且是结构性问题, 非仅执行顺序偶然**: 确认 `state-scanner/` 下同时存在两个物理上不同的 `lib/` 包 —— `state-scanner/lib/` (含 `identity.py`/`collision.py` 等, Layer L) 与 `state-scanner/scripts/lib/` (含 `detailed_tasks.py`/`spec_complete.py` 等), 两者都有 `__init__.py`。任何 `from lib.detailed_tasks import ...` 写法都**结构性不可行**: 要让 `lib` 解析出 `detailed_tasks` 子模块, 必须把 `state-scanner/scripts/lib` 的**父目录** (`state-scanner/scripts`) 插入 sys.path 并写 `from lib.detailed_tasks import ...` —— 但 `state-scanner/scripts` 目录本身不含 `lib/` 子目录 (`detailed_tasks.py` 直接就在 `scripts/lib/` 里, 不是 `scripts/lib/lib/`); 唯一能让 `lib.X` 语法解析到 `state-scanner/scripts/lib` 内容的方式是把 `scripts/lib` 本身当 `lib` 包根插入 sys.path —— 而这要求把 `scripts/lib` 的父目录 (`scripts`) 插入并 import `lib.detailed_tasks`, 此时 `lib` 会指向 `scripts/lib` 没错, 但 `owner_container()` 若同进程后跑, 需要的是 `lib.identity` (在 `state-scanner/lib`, 不在 `scripts/lib`) —— 两个消费者对 `lib` 的期望物理目标**互斥**, 无法用单一 `lib.` 限定名同时满足。proposal 选择的「插具体 `scripts/lib` 目录 + 裸模块名 `detailed_tasks`」路线是唯一避开该冲突的方式, 结论成立。
- **circular import 论证**: `detailed_tasks.py` 逐行核对确认仅 `import re` (+ `from __future__ import annotations`), 零 `lib.*`/`collectors.*` 依赖 (L33-35)。全仓 `find` 确认此文件是唯一的 `detailed_tasks.py` (无重名碰撞候选)。且新导入路径用**裸模块名插入 `scripts/lib` 目录本身**, 不经过任何 `__init__.py` 执行 (`state-scanner/scripts/lib/__init__.py` 确认为 0 字节空文件) —— 结构性避开了 #113 实施期证伪过的「包 `__init__` 才是环的载体」陷阱 (`collectors/__init__.py` 会级联 import 到 `collectors.openspec → lib.spec_complete`, 但本次改动完全不触碰 `collectors` 包)。比 #113 最初 (被证伪的) 论证更稳固, 因为它连「哪个包的 `__init__` 会被执行」这个问题都不存在。
- **`frontmatter_block.py` acyclic-graph 论证方式引用属实**: 该文件 docstring (L1-25) 确有完全相同风格的 leaf-module + 依赖图 ASCII 论证 (`collectors.openspec -> lib.frontmatter_block -> (nothing)`), 引用真实存在, 非杜撰。
- **`owner_container()` L317-321 / `_benign_unconditional_reasons` L46-50 行号引用准确**: 逐行比对, 两处引用的代码内容 (sys.path 插入 + import 语句) 与 proposal 描述一致, 行号误差在 ±1 行内 (含注释行计入方式差异), 不构成误导性引用。
- **`spec_complete.py` L128-190 (dual-context 先例) / detailed_tasks 二次 re-import 块 (proposal 称 L340-360, 实际落在 L350-356 附近)**: 内容属实 —— `try: from .carry_forward import ... / except ImportError: sys.path.insert(0, lib_dir); from carry_forward import ...` 模式确认存在且被复用 3 次 (carry_forward / frontmatter_block+runtime_probe / detailed_tasks 两处), "lib 顶层名故意避免" 注释 (L138-140) 原文属实。行号区间稍宽松但落点在标注范围内, 不算引用错误。
- **`detailed_tasks.py` 公开 API 签名/返回形态对 proposal 用法够用**: `parse_detailed_tasks(text) -> {"parse_ok": bool, "tasks": [{"id","raw_status","title"}], "reason": str}`、`is_done_status(raw_status: str|None) -> bool` (白名单 `{"done","completed"}`, L104-111) 与决策 2/5 描述的取数字段、fail-CLOSED 判据完全匹配, 无缺失字段、无签名不符 (M-1 是"消费方未用满 API 的第三返回态", 不是 API 本身不够用)。
- **降级 sentinel 设计的核心哲学 (决策 4) 与 `_BENIGN_IMPORT_FAILED` 类比恰当**: `_BENIGN_IMPORT_FAILED` 是类型级哨兵 (frozenset 子类, 供 `isinstance` 判别), 而决策 4 是数据级哨兵 (直接产一条 `{source, item}` sentinel item); 两者机制不同但 proposal 措辞是"镜像哲学"而非"复用同一实现", 表述准确, 不构成误导。`assemble_unfinished` (`handoff_autofill.py` L235: `out.extend(unchecked_tasks or [])`) 确认对 `source` 字段零校验、纯直通, 新前缀兼容性声明属实。
- **lazy import 时机**: 两处既有先例 (`_benign_unconditional_reasons` L42-44、`owner_container` L313-315) 均为函数体内 `import sys` / `from pathlib import Path`, 确认是函数级 lazy import 而非模块顶层, 与决策 5 的"仅 yaml-only spec 命中时触发"一致。
