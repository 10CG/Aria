---
verdict: PASS
agent: qa-engineer
round: R3
critical_count: 0
major_count: 0
minor_count: 1
r2_resolved: 2/2
---

# post_spec R3 审计 — session-closer-autofill-yaml-datasource (qa-engineer 视角, convergence mode 收敛终验)

审计对象: `/home/dev/Aria/openspec/changes/session-closer-autofill-yaml-datasource/proposal.md`(R2 修订版)
对照: R2 报告 `post_spec-R2-1785596502348-...qa-engineer.md`; 逐行核对 `handoff_autofill.py`(现行未改动, Tasks 1.1 仍未勾, 与 proposal 状态一致)、`detailed_tasks.py` L184-273(`parse_detailed_tasks` 四态)。**实测**(非猜测)本机 Python 对 5 种路径形态的 `open()` 真实异常类型, 并实测 `importlib.util.spec_from_file_location` 对不存在路径的真实失败行为。

---

## R2 两条 finding 逐条核对(全部 RESOLVED)

### M-3(SC-8 isfile 闸门致 fixture 不触发 OSError) → RESOLVED

proposal §What 第 1 点现已显式裁定: yaml 侧「存在性判断」**不设 `isfile()` 前置闸门**, 直接 `open()`; `FileNotFoundError`/`NotADirectoryError` ⇒ 缺席(0 条无 sentinel); 其它 `OSError`(`IsADirectoryError`/`PermissionError`/symlink 循环等) ⇒ sentinel。这消除了 R2 指出的「实现照抄 `tasks.md` 的 `isfile()` 惯例」歧义 —— 判据本身已钉死在 spec 文本里, 不再靠实现者临场判断。

**实测核验**(本机, 非 root, 5 种路径形态):
```
目录            → IsADirectoryError   (OSError 子类)  → 落「其它 OSError」桶 → sentinel  ✓ 与 SC-8 预期一致
断链 symlink    → FileNotFoundError                    → 落「缺席」桶 → 0/无 sentinel   ✓ 与 SC-9 新增子 case 预期一致
symlink 循环    → OSError(ELOOP, 非细分子类)            → 落「其它 OSError」桶 → sentinel  ✓ 与 §What「symlink 循环等」表述一致
不存在文件      → FileNotFoundError                    → 落「缺席」桶                     ✓ 覆盖「真双缺席」
父路径分量是文件 → NotADirectoryError                   → 落「缺席」桶(spec 显式两类之一)
```
五种形态的真实异常类型与 spec 文本逐条对应, 无一处文本与运行时语义不符。SC-8(目录 fixture)在新语义下**结构上必然**触达 `open()` 并产出 `IsADirectoryError`, fixture 与断言自洽 —— M-3 指出的「fixture 不触发 OSError」风险已随判据钉死而结构性消失。SC-9 新增断链 symlink 子 case 同样经实测验证落入正确桶, 边界锁定有效。

### m-4(SC-5 验证强度) → RESOLVED

proposal §What 第 5 点新增 SC-5(b): 传入不存在的 `sot_path` 直测 helper 本身返回 `None`。**实测核验**: 用与 `importlib.util.spec_from_file_location` + `exec_module` 相同结构的最小复现脚本, 对不存在路径调用, 确认 `exec_module` 阶段抛出真实 `FileNotFoundError`, 被 helper 自身 `except Exception` 捕获并转换为 `None`(非模拟, 真实异常路径)。这不同于 M-2 修复的「跨 skill sys.path/裸模块名碰撞」维度, 但确实是 helper **自身** try/except 骨架在一次真实(非 monkeypatch)失败下的端到端验证 —— 达到与姊妹 helper `_benign_unconditional_reasons()` 同等的「真实触发」验证强度, R2 提出的加固建议已被采纳。

2/2 全部真实解决, 均可对照运行时实测结果验证, 非表面遣词。

---

## 终验: SC-1~SC-9 状态空间覆盖(在 M-3/m-4 均解决后重新核对)

以「`tasks.md` 存在性 × yaml 存在性/可读性/`parse_ok`」为轴, 划分:

- tasks.md 在场 ⇒ yaml 不看(SC-2, 并存优先级) — 与 yaml 分支正交, 独立不受影响
- tasks.md 缺席, yaml 正常解析(`parse_ok=True`): done-family 净空(SC-3)/ 混合态逐项判(SC-4)/ 含 title 缺失项的 happy path(SC-1, baseline-failing)
- tasks.md 缺席, yaml `parse_ok=False`: 四态代码分支中的「零 `- id:`」与「重复 `tasks:` 键」两 fixture(SC-7, baseline-failing) — 逐行核对 `detailed_tasks.py` L209-215(bounds=None)、L238-240(`parse_ok=False`)、L245-247(`reason="zero ... entries"`)均真实触发
- tasks.md 缺席, yaml 存在但 `open()` 失败于「其它 OSError」桶: 目录(SC-8, 经实测确认触发 `IsADirectoryError`)
- tasks.md 缺席, yaml 与 tasks.md 双缺席(真双缺席, SC-9): `FileNotFoundError` 桶, 追加断链 symlink 子 case(经实测确认)
- SOT 加载失败(独立轴, 可与任意 yaml 态叠加, 但单独测试): monkeypatch 消费方(SC-5a)+ helper 自身真实失败路径(SC-5b, 经实测确认)
- SC-6: 回归 + lib 迁移红灯(经 SC-1 默认路径实算 SOT 达成, 与 R2 tech-lead m-3 勘正一致)

该划分互斥且穷尽(M-3 解决后, 判据本身不再有歧义, 划分才真正落地; R2 时的「划分逻辑自洽但判据未定案」前置歧义已消除)。baseline-failing 纪律(SC-1/SC-7 在未修代码上必须先 FAIL): 已对照现行 `handoff_autofill.py`(仍是 R1 前原始版本, 无 yaml 分支)核实 — 该版本对 yaml-only fixture 与畸形 yaml fixture 均返回 0 条(无 yaml 处理逻辑), 两条 SC 在此基线上确实先 FAIL, 修后转 PASS 的红绿闭环成立。

---

## Minor(新发现, 非阻塞)

### m-5(新) — `NotADirectoryError` 桶(「缺席」二元组的第二成员)无专属 SC 覆盖, 但风险已被架构性下调为噪音而非危险

**位置**: proposal §What 第 1 点「`FileNotFoundError`/`NotADirectoryError` ⇒ 视为 yaml 缺席」; SC-9 仅追加 `FileNotFoundError`(断链 symlink)子 case, 未追加 `NotADirectoryError` 代表性 fixture(构造方式: `changes_dir` 内放一个**非目录**条目, 如误落地的 `README.md`, 使 `os.path.join(changes_dir, name, "detailed-tasks.yaml")` 中 `name` 分量本身是文件)。

**主张**: 若实现的 `except` 元组遗漏 `NotADirectoryError`(只写 `except FileNotFoundError:`), 该分支不会走「缺席」路径, 而是被更外层的「其它 `OSError` ⇒ sentinel」兜底捕获(spec 架构本身是「特定异常元组在前、宽 `OSError` 兜底在后」, 非纯字面量枚举)——**结果是对一个非法/非 spec 的目录条目多报一条 sentinel 噪音**, 而非崩溃、也非静默假绿。这与本 spec 反复强调的哲学「宁噪音勿假绿」(§What 第 3 点、`_BENIGN_IMPORT_FAILED` 同源注释)方向一致, 并非违反。故本条**不影响 CONVERGED 判定**, 纯记录性观察。

**建议**(可选, 非本轮必须项): 若追求 spec 文本与测试断言的字面一致, 可选择性给 SC-9 补一个 `NotADirectoryError` 代表性 fixture(如上); 不加也不构成缺陷, 可留给实现阶段视 Rule #6 substitute 覆盖率自行取舍。

---

## Verdict 依据

R2 两条 finding(1 Major M-3 + 1 Minor m-4)经本轮修订版逐条**实测核验**(非仅读 prose, 而是用最小复现脚本对 5 种路径形态 + helper 失败路径做了真实 Python 运行时验证), 确认真实解决: M-3 的判据歧义已在 spec 文本层面钉死, SC-8/SC-9 与运行时语义完全自洽; m-4 的 helper 自身失败路径现有真实(非 monkeypatch)端到端验证。终验对 SC-1~SC-9 状态空间做完整穷尽性复核, 划分互斥无重叠, baseline-failing 纪律(SC-1/SC-7)对照现行未改代码确认成立。新发现 1 条 Minor(m-5, `NotADirectoryError` 未测但风险已被架构性下调为噪音, 非阻塞)。无 Critical、无 Major。判定 **PASS(CONVERGED)**。
