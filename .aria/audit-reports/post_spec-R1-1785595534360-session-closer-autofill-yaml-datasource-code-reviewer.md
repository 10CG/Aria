---
verdict: REVISE
agent: code-reviewer
round: R1
critical_count: 0
major_count: 1
minor_count: 1
---

# post_spec R1 — session-closer-autofill-yaml-datasource (code-reviewer 视角)

审计对象: `openspec/changes/session-closer-autofill-yaml-datasource/proposal.md` (spec 本身, 无实现代码)。
方法: proposal 中每处代码引用逐行对照真代码核实 (handoff_autofill.py 全文 / detailed_tasks.py 全文 / spec_complete.py 相关段 / collectors/openspec.py L260-300 / plugin.json)。

## Findings

### Major M-1 — `parse_detailed_tasks` 返回形态引用不完整, 且 file-level 解析失败路径 (`parse_ok=False`) 无任何处置分支

- 位置: proposal §What 第 2 条 (L19) + 降级设计第 4 条 (L23) + SC-1~SC-5 (L55-59)
- 主张核实:
  - proposal 写 "`parse_detailed_tasks(text)` 逐 task 取 `{id, raw_status, title}`"。真实签名返回的是**包装 dict** `{"parse_ok": bool, "tasks": [...], "reason": str}` (`detailed_tasks.py` L225-234, L270-273); `{id, raw_status, title}` 只是 `result["tasks"]` 内的元素形态。
  - `parse_ok=False` 有四种真实触发态 (docstring L229-232 + 实现 L237-259): 无顶层 `tasks:` / 顶层 `tasks:` 重复 / 零 `- id:` 条目 / 结构自不一致 (hidden entry)。此时 `tasks=[]`。
- 为什么重要: proposal 的降级设计**只**覆盖「跨 skill 导入失败 → sentinel item」(第 4 条), 对 `parse_ok=False` (以及 yaml 文件 OSError 读失败) 零字未提。照 spec 字面实现 (逐 task 迭代) 会在 yaml 存在但不可解析时对该 spec 报 **0 条** — 静默假绿, 正是本 issue 的病根类, 直接违背 proposal 自己的「宁噪音勿假绿」决策与 fail-CLOSED 哲学。对照: gate 侧同一消费点 `_yaml_only_tasks_verdict` (`spec_complete.py` L207-212) 对 `parse_ok=False` 有显式分支 (`detailed-tasks.yaml unparseable (...)` fall-through); openspec.py 侧对读失败有 `soft_error` (L282-284)。session-closer 是唯一没写这条路的消费方。SC-1~SC-5 也测不到此态 (无 unparseable-yaml fixture SC)。
- 如何修复: §What 第 2 条改写返回形态为 `{parse_ok, tasks, reason}`; 第 4 条降级扩展为「导入失败 **或** `parse_ok=False` **或** yaml 读失败」统一产 sentinel item (可携带 `reason`); 增补一条 SC (unparseable yaml → sentinel 非 0)。

### Minor m-1 — `spec_complete.py L342-356` 行号引用偏移, 且该处导入的符号与 proposal 点名的函数不符

- 位置: proposal §What 第 3 条 (L22) + 关键决策表 "spec_complete L342 同款先例" (L37)
- 真代码证据: L342-346 是无关正则 (`_CODE_EXT_RE` / `_BACKTICK_IDENTIFIER_RE`); dual-context import 块实际在 **L347-356**, 且只导入 `_TASK_ID_LINE_RE`。proposal 点名的 `from detailed_tasks import parse_detailed_tasks, is_done_status` 对应的先例块在 **L441-451** (`from detailed_tasks import _split_task_blocks, is_done_status, parse_detailed_tasks`)。
- 影响: 模式主张本身成立 (两块都是「插 lib 目录进 sys.path + 裸模块名」同款), 但引用坐标会把实现者/后续审计导到导入不同符号的块。建议改引 L441-451 (或双引)。

## 已核实无误项 (逐条)

1. **L160-175 `grep_unchecked_tasks`**: 行号精确 (def L160, return L175); 确实只拼 `tasks.md` 路径 (L166), yaml-only spec 结构性得 0 — Why 段病根描述属实。
2. **L317-321 `owner_container` 的 `lib` 名毒化**: L318 `_ss_root = parents[2] / "state-scanner"`, L319-320 sys.path insert, L321 `from lib.identity import get_identity` — 顶层名 `lib` 确被绑到 state-scanner 根下的 Layer L 包 (与 scripts/lib 是两个不同 lib 包, memory `state_scanner_dual_lib_package_shadow` 印证), 「禁用 `from lib.detailed_tasks import`」的理由实锤。决策表 "L319-321" 亦准。
3. **L46-50 `_benign_unconditional_reasons` 路径解析**: L48 `Path(__file__).resolve().parents[2]` 确在引用范围内。层级数学核实: `__file__` = `aria/skills/session-closer/scripts/handoff_autofill.py` → parents[0]=scripts, parents[1]=session-closer, **parents[2]=skills** → `skills/state-scanner/scripts[/lib]` 定位正确, 层级数无误。
4. **`is_done_status` 白名单**: `_DONE_FAMILY = frozenset({"done", "completed"})` (detailed_tasks.py L83), `.lower()` 后精确匹配, None→False (L104-111) — proposal「done-family 仅 {done, completed}; ... unknown/None 全算未完成」逐字准确。
5. **`detailed_tasks.py` 零回边**: 仅 `import re` (+ `__future__`), 无任何 collectors/lib 导入 — 循环导入论证成立。
6. **openspec.py 决策 6 引用**: L265-277 注释与实现 ("Precedence mirrors the gate (决策 6): tasks.md present ⇒ yaml NOT consulted") 与 proposal 第 1 条取数语义逐字一致。
7. **`assemble_unfinished` 零改动兼容**: unchecked_tasks 经 `out.extend(unchecked_tasks or [])` (L235) 原样透传, `source` 字段完全不被检视; `cross_check_unfilled` 只读 `item` (L257)。session-closer 其余脚本与 SKILL.md 均无对该 `source` 值的前缀匹配消费。新前缀零改动兼容主张成立 (实际比「当自由显示串」更强 — 根本不读)。
8. **版本声明**: plugin.json `"version": "1.65.0"` → PATCH v1.65.1 递增正确。
9. **「两处既有跨 skill import」**: 确为两处且均 lazy (函数体内): `_benign_unconditional_reasons` (collectors.multi_remote) + `owner_container` (lib.identity) — lazy import 一致性主张成立。
10. **`_BENIGN_IMPORT_FAILED` 哲学镜像**: L54-67 哨兵降级可见性设计与 proposal 第 4 条描述一致; "post_planning R2 M-2 隔离路径实测" 引自 L57-58 注释, 属实。
11. **裸名 `detailed_tasks` 无碰撞**: 全 aria 插件树仅一个 `detailed_tasks.py` (state-scanner/scripts/lib), sys.path 插入后裸模块导入无 shadow 风险。
