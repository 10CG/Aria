---
verdict: REVISE
agent: qa-engineer
round: R2
critical_count: 0
major_count: 1
minor_count: 1
r1_resolved: 6/6
---

# post_spec R2 审计 — session-closer-autofill-yaml-datasource (qa-engineer 视角, convergence mode)

审计对象: `/home/dev/Aria/openspec/changes/session-closer-autofill-yaml-datasource/proposal.md`(R1 修订版)
对照: R1 报告 `post_spec-R1-1785595534360-...qa-engineer.md`; 逐行核对 `handoff_autofill.py`(现行, 未改动 — Tasks 1.1 仍未勾)、`state-scanner/scripts/lib/detailed_tasks.py` L184-273(`parse_detailed_tasks` 四态)、`spec_complete.py` L200-217(OSError/parse_ok=False 分诊先例)、`test_handoff_autofill.py`(现行结构)。实测 Python `os.path.isfile()`/`open()` 对目录路径的真实行为(本机 Linux, 非 root)。

---

## R1 六条 finding 逐条核对(全部 RESOLVED)

- **C-1(parse_ok=False 无 SC 覆盖)** → RESOLVED。§What 第 2/3(c) 点显式要求先查 `parse_ok`, 仅 `True` 时遍历 `tasks`; SC-7 构造「零 `- id:` 条目」「重复 `tasks:` 键」两 fixture。逐行核对 `detailed_tasks.py`: 零 `- id:` → L245-247 `reason="zero \`- id:\` entries..."`, `parse_ok=False`; 重复顶层 `tasks:` → L209-215 `tasks_indices>1` → `bounds=None` → L238-240 `parse_ok=False`。两 fixture 均真实触发, 非空判定。
- **M-1(yaml OSError 降级方向未定义)** → RESOLVED。§What 3(b) 明文禁止照抄 `tasks.md` 分支静默 `continue`, 要求 sentinel; SC-8 补测试。方向裁决与姊妹消费方 `spec_complete.py` L200-206(OSError 独立态, 返回帯 reason 的 `(False, ...)`)先例一致, 逐行核对属实。
- **M-2(SC-5 sys.modules 缓存假绿)** → RESOLVED, 且是架构级修复而非测试手法修补。§What 第 5 点新增 `_load_detailed_tasks_api()` seam helper, SC-5 明文「不得依赖 sys.path 操纵 — import 缓存维度」, 改为 monkeypatch helper 本身。这在函数调用边界拦截, 与内部 `sys.modules` 缓存状态无关, 对测试执行顺序不敏感 —— 真正绕开 R1 指出的缓存维度, 非表面遣词。
- **m-1(双缺席未覆盖)** → RESOLVED, SC-9 显式补「0 条且无 sentinel」。
- **m-2(title 空串尾空格)** → RESOLVED, §What 第 2 点显式契约「title 空时不产尾随空格」+ SC-1 显式断言「title 缺失项 item == task id(无尾随空格)」。
- **m-3(done/pending 混合态未覆盖)** → RESOLVED, SC-4 新增混合态逐态断言。

6/6 全部真实解决, 非表面遣词 —— 均可在代码/测试设计层面对照验证。

---

## Major(新发现, R1 未覆盖)

### M-3(新) — SC-8「yaml 为目录」fixture 依赖「存在性判定用 `os.path.exists` 而非 `os.path.isfile`」这一未言明的实现细节; 若实现照抄相邻 `tasks.md` 分支的 `isfile()` 惯例, 该 fixture 根本不会触达 `open()`, 更不会产生 OSError

**位置**: proposal §What 第 1 点(「`detailed-tasks.yaml` 存在 ⇒ 走 yaml 分支」未定义「存在」判据)+ Success Criteria SC-8; 对照 `handoff_autofill.py` 现行 L167 `if os.path.isfile(tasks):`(yaml 分支大概率原地复制的惯例)。

**实测**(本机核实, 非猜测):
```
os.mkdir(<dir>/detailed-tasks.yaml)   # SC-8 拟用的「yaml 为目录」fixture
os.path.isfile(<dir>/detailed-tasks.yaml)  → False   # 而非 True
os.path.exists(<dir>/detailed-tasks.yaml)  → True
open(<dir>/detailed-tasks.yaml)            → IsADirectoryError(OSError 子类)  # 仅当真的走到 open()
```

**主张**: `grep_unchecked_tasks` 现行对 `tasks.md` 用 `os.path.isfile(tasks)` 作存在性闸门(先判后开)。proposal §What 第 1 点只说「yaml 存在 ⇒ 走 yaml 分支」, 未指明这个「存在」判据的具体谓词。若实现者按原地惯例对 yaml 也写 `if os.path.isfile(yaml_path): ... open(yaml_path) ...`(三处 sys.path 插入之外, 这是本函数目前唯一的「判存在」范式, 复制概率高), 则 SC-8 的「detailed-tasks.yaml 是一个目录」这一 fixture 在 `os.path.isfile()` 闸门处就返回 `False` —— 代码**根本不会进入 yaml 分支**, 直接落到 decision 1 的「两者都缺」隐式路径, 产出 0 条、无 sentinel。这与 SC-8 预期的「sentinel item, 非静默 continue」完全相反, 而且是以一种**新的机制**(存在性判据类型不匹配, 而非 M-1 原指的『读取失败后静默 continue』)复刻同一「静默回 0」病根 —— 与 C-1 精神同源, 只是命中点从「解析后处置」前移到了「存在性闸门」。

进一步: 这不只是「SC-8 会失败」这么简单。若实现者用 `isfile()` 版本跑测试、看到 SC-8 红, 排查后可能有两种收敛路径: (a) 正确识别根因, 把闸门换成 `os.path.exists()`(或干脆去掉预判闸门、直接 `try: open() except OSError`)——这是期望路径; (b) 图省事把 SC-8 fixture 从「目录」换成别的(如 `os.chmod(0o000)` 权限拒绝, 本机非 root 环境下确实可行), **绕过而非解决**闸门谓词歧义, 让「目录」这一形态本身重新失去测试覆盖。proposal 当前文本对两条路径没有裁决依据, 纯靠实现者临场判断。

**建议**: proposal §What 第 1 点(或第 3(b) 点)显式裁定 yaml 分支的存在性判据必须是 `os.path.exists()`(与「不看类型, 只要占了这个路径就必须给出确定性结果 —— 存在但不可读 ⇒ sentinel, 不存在 ⇒ 0」的哲学一致), 不得沿用 `tasks.md` 分支的 `isfile()` 闸门原样复制; 或等价地要求 yaml 分支不设预判闸门, 直接 `try/except OSError` 包裹 `open()`, 用异常本身(含 `FileNotFoundError`/`IsADirectoryError`/`PermissionError`)分诊「不存在」vs「存在但不可读」。二选一均可, 但必须在 spec 里钉死, 否则 SC-8 作为 baseline-failing 测试的「baseline」本身就不确定该长什么样, 实现窗口期会产生歧义返工。

---

## Minor(新发现)

### m-4(新) — SC-5 的 monkeypatch 只测「`_load_detailed_tasks_api()` 返回 None 后消费方如何降级」, 未端到端覆盖「helper 自身在真实跨 skill import 失败时确实返回 None」这一层

**位置**: proposal §What 第 5 点; Success Criteria SC-5; 对照本文件姊妹 helper `_benign_unconditional_reasons()` L54-59 的既有先例注释「R2 实测: 把 skill 目录复制到隔离路径时该 fallback 真的静默触发过」。

**主张**: `_benign_unconditional_reasons()` 这个同文件、同类型(跨 skill sys.path + 裸模块名导入, best-effort try/except)的既有 helper, 其「导入失败」分支历史上是靠**真实隔离路径 fixture**(复制 skill 目录到隔离位置、破坏 sys.path 解析)实测触发过的, 留痕在注释里。`_load_detailed_tasks_api()` 是同一模式的新 helper, 但 SC-5 只用 monkeypatch 直接令其返回 `None`, 测的是**下游消费逻辑**(拿到 `None` 后是否正确产 sentinel), 并不覆盖 helper **内部** try/except 是否真的能把一次genuine `ImportError`/`ModuleNotFoundError` 转换成 `None`(而非泄漏异常到调用方, 或吞掉了不该吞的异常类型)。风险很低(helper 大概率是薄包装, 复制 `_benign_unconditional_reasons` 已验证过的 try/except 骨架), 故只标 Minor, 但与本文件自身刚建立的更高验证先例(隔离路径实测)相比, SC-5 的验证强度是降级的。

**建议**: 可接受现状(monkeypatch 已解决 M-2 的核心风险), 但若追求与姊妹 helper 同等验证强度, 可选择性补一条隔离路径集成 fixture(非阻塞项, 可作为 SC-5 的可选加固, 不建议作为本轮 REVISE 的必须项)。

---

## 已核对、未发现新问题的部分

- SC-1~SC-9 对 `{tasks.md 存在性} × {yaml 存在性/可读性/parse_ok}` 状态空间的划分: 剔除 M-3(新)指出的「存在性谓词未定案」这一前置歧义后, 划分本身(SC-9 双缺席 / SC-2 并存优先级 / SC-1+SC-3+SC-4 yaml-ok 的 pending/done/混合三态 / SC-7 parse_ok=False / SC-8 OSError / SC-5 import 失败)在逻辑上互斥且穷尽, 无重叠格、无遗漏格。
- SC-7 双 fixture 对照 `detailed_tasks.py` L198-222(`_tasks_block_bounds`)与 L244-247 逐行核对, 确认「零 `- id:` 条目」与「重复 `tasks:` 键」都是真实的、独立的 `parse_ok=False` 触发路径(非同一条件的两种措辞), 断言可证伪。
- `_load_detailed_tasks_api` seam 设计本身(点 5)与 M-2 修复方案一致, monkeypatch 在函数调用边界拦截, 对 unittest 方法执行顺序(字母序, 同进程)不敏感, 真解决 R1 指出的缓存维度问题。
- 循环导入 / `lib` 顶层名双包绑定(§What 第 4 点)论证与既有代码(`detailed_tasks.py` 头部注释、`owner_container()` L305-326、`_benign_unconditional_reasons()` L42-53)逐行核对一致, 无新问题(非本轮 qa 视角重点, 但顺带核实无矛盾)。
- rule6_note substitute 判据维持 R1 结论(纯 deterministic 脚本, SKILL.md 零变动), 无异议。

---

## Verdict 依据

R1 全部 6 条 finding(1 Critical + 2 Major + 3 Minor)经修订版逐条核对**真实解决**, 非表面遣词 —— 若审计仅限于「R1 收敛」范围, 本应可判 PASS。但复审中发现 1 条新 Major(M-3: SC-8「yaml 为目录」fixture 的可证伪性依赖一个 proposal 未言明的存在性判据选择, 若实现照抄相邻 `isfile()` 惯例则该 fixture 结构上无法触达其声称测试的 OSError 路径, 且以新机制复刻本 issue 要根治的「静默回 0」病根 —— 与本轮审计任务特别点名要核实的「SC-8 是否真必产 OSError」直接对应, 证实为真实风险非跨平台层面而是同平台闸门谓词层面)+ 1 条新 Minor(m-4: SC-5 验证强度低于同文件姊妹 helper 已建立的先例)。存在未收敛 Major, 判定 **REVISE**。
