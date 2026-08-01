---
verdict: PASS
agent: backend-architect
round: R3
critical_count: 0
major_count: 0
minor_count: 1
r2_resolved: 2/2
---

# post_spec R3 — session-closer-autofill-yaml-datasource (backend-architect: 收敛终验)

审计对象: `/home/dev/Aria/openspec/changes/session-closer-autofill-yaml-datasource/proposal.md` (R2 后修订版)。方法: 逐条核对 R2 两条 minor 措辞落地; 对 R2 之后新增/升级的三项技术裁定 (importlib 直载 / helper 参数化契约 / open-attempt 异常分类) 回代真代码验证 (`handoff_autofill.py` 全文、`detailed_tasks.py` 全文、`collectors/openspec.py` L18-31、`collectors/handoff_multibranch.py` L60-84、Python 解释器实测 `importlib.util.spec_from_file_location` 真实异常时序)。**只审不改。**

---

## R2 两条 minor 复核

### m-1 (sentinel 文本模板精度) — RESOLVED

§What 3 现给出与 happy-path 同精度的逐字公式: `source = f"detailed-tasks.yaml:{name}:unavailable"`, `item = f"(unavailable: {kind} — {reason}) 需人工核对"`, `kind ∈ {sot_load_failed, read_failed, parse_failed}`, 并显式收紧 SC 断言口径 "锚定 source 后缀与 kind, 不断自由文本" —— 直接解决 R2 指出的"reason 透传语义模糊"问题(不再要求逐字比对不稳定的自由文本)。**确认解决。**

### m-2 ("四态"措辞) — RESOLVED

§What 3(c) 改为"parser **三条代码分支**覆盖的**四种输入形态**", 精确匹配 R2 建议措辞, 且保留了对 `_tasks_block_bounds`(L198-222, 1 分支覆盖"无/重复 tasks:"两种触发条件)的准确描述。**确认解决。**

**r2_resolved: 2/2。**

---

## 新技术裁定核验

### (1) importlib 文件直载 — 三项子核验均通过

- **零包内依赖**: `detailed_tasks.py` 全文仅 `import re` + `from __future__ import annotations`, 无相对导入。回代确认成立, "文件直载无依赖缺口"前提真实。
- **唯一模块名不冲突**: 全仓 grep `aria_sc_detailed_tasks` 零命中(现有代码/测试均未用此名); 该名足够特异(`aria_sc_` 命名空间前缀), 与 stdlib/第三方包无碰撞面。
- **"lib" 双包名碰撞先例属实**: 回代 `collectors/handoff_multibranch.py` L60-84 确认 `_SS_ROOT` 插入后执行 `from lib.collision import ...`, 把裸名 `lib` 绑定到 `state-scanner/lib`; `collectors/openspec.py` L18-31 注释显式记录"顶层名 `lib` 可能已被 handoff_multibranch 的 sys.path 插入占用"这一风险。proposal 引用的碰撞根据真实存在, importlib 直载(不走 `from lib.xxx import`, 绕开裸名解析)是结构性根治, 非文档化兜底。
- **异常兜底实测**: 用 Python 解释器实测 `importlib.util.spec_from_file_location(name, <不存在路径>)` —— 对 `.py` 后缀路径, spec **永远非 None**(即使文件不存在), `FileNotFoundError` 实际在 `spec.loader.exec_module(module)` 时才抛出; 语法错误文件同样在 `exec_module` 时抛 `SyntaxError`。这意味着 helper 若要"任何异常返回 None"必须把 try/except 包住 spec 创建 **到** `exec_module`/属性提取的完整链条(不能只包 `spec_from_file_location` 一步) —— proposal 描述的契约("成功返回…, 任何异常返回 None")语义上要求这一点, 且与既有姊妹 helper(`owner_container()`/`_benign_unconditional_reasons()`)"整段包 try/except"的既有写法同构, Phase B 按现有代码风格实现自然会覆盖到位。**结论: 契约本身无遗漏, 是 Phase B 实现纪律项(非 spec 缺陷)。**

### (2) `_load_detailed_tasks_api(sot_path=None)` 参数化契约

双层测试策略((a) monkeypatch helper 本身、(b) helper 直测非法 `sot_path`)绕开 sys.modules 缓存维度的论证成立: 只要实现遵循"每次调用都用 `importlib.util.spec_from_file_location` 现造 spec + `module_from_spec` 现造 module 对象"(不检查/复用 `sys.modules[name]`), 则该 helper 天然幂等且不受调用次数/顺序影响 —— 即使把结果登记进 `sys.modules` 供内省, 每次也会用新 module 对象覆盖旧条目, 不产生"读到前一次调用留下的过期对象"的缓存事故。契约面(输入/输出形态)与消费方需求(`parse_detailed_tasks` + `is_done_status` 两个函数)精确匹配, 无多余暴露面。**无新增缺口。**

### (3) open-attempt 异常分类 — 发现一处遗漏类别 (本轮唯一 minor)

`FileNotFoundError`/`NotADirectoryError` → 缺席、其余 `OSError`(`IsADirectoryError`/`PermissionError`/symlink 循环等) → sentinel 的二分, 对 **OSError 家族内部**是完备的。但 `open(path, encoding="utf-8").read()` 在文件编码非法(非 UTF-8 字节)时抛的是 `UnicodeDecodeError` —— 它是 `ValueError` 的子类, **不是** `OSError` 子类, 不会被"其它 OSError → sentinel"分支捕获。回代验证: 本文件同一函数 `grep_unchecked_tasks` 现有 tasks.md 分支(L169)已用 `open(tasks, encoding="utf-8", errors="replace")` 规避了这个问题(`errors="replace"` 使非法字节被替换而非抛异常), 但 proposal §What 3(1) 的 open-attempt 语义描述未显式承诺新 yaml 分支沿用同一 `errors="replace"` 参数。若 Phase B 实现遗漏这个细节, 一个编码损坏的 `detailed-tasks.yaml` 会在 `main()` 无顶层 try/except 兜底的路径上让整个 autofill 脚本崩溃(比原始"静默报 0"病根更差的失效模式), 且 SC-7/SC-8/SC-9 现有 fixture 未覆盖非法编码字节这一子场景。

**严重度判定为 minor 而非 major**: (a) 同函数内 4 行之上就是现成的 `errors="replace"` 先例, Phase B 实现者大概率直接复制既有 open() 调用模式(非独立重造); (b) 修复是一行参数改动, 无设计返工。**建议**: Phase B 实现前把 §What 3(1) 的 open-attempt 描述补一句"沿用本文件 L169 先例, `open(..., encoding="utf-8", errors="replace")`", 并给 SC-8 或新增一个 sub-case 补一个非法字节 fixture, 锁定这条路径不抛 `UnicodeDecodeError`。不建议为此单独开 R4。

---

## 结论

R2 两条 minor 全部真实解决(逐字模板 + 措辞勘正, 均回代验证)。R3 新增技术裁定(importlib 直载三项子核验 / helper 参数化契约 / open-attempt 异常分类)结构完整, 未发现 critical/major 缺口; 唯一新增发现(`UnicodeDecodeError` 不在 OSError 异常分类内)为非阻塞 minor, 有强先例支撑 + 修复成本极低。**verdict: PASS — CONVERGED, 可进入 Phase B。**
