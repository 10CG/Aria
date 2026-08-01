---
verdict: PASS
agent: tech-lead
round: R3
critical_count: 0
major_count: 0
minor_count: 2
r2_resolved: 4/4
---

# post_spec R3 · tech-lead 收敛终验 (convergence mode)

审计对象: `openspec/changes/session-closer-autofill-yaml-datasource/proposal.md` (aria-plugin #121, Level 2)
基线: 本人 R2 报告 (m-1 sys.path 顺序 / m-2 SC-8 isfile 矛盾 / m-3 SC-6 依据 / m-4 sentinel 判别位)

本轮方法: 不看措辞看判据 + **实机验证**。对 R2 四条裁定各自的「架构合理性」跑了两组实测 (open() 异常分类 6 例 / importlib 直载 4 例), 不依赖推断。

结论: **R2 四条全部实质解决 (4/4), 且三条裁定经实机验证成立**; 无一条以措辞掩盖, 修订未重开任何前轮 finding 的同类 bug。新增 2 条 minor 均为文本级 (一条行为洞 + 一条论证自相矛盾), 不阻断。**判定 CONVERGED**。

---

## 一、R2 findings 逐条核销 (含裁定本身的架构复核)

### m-1 sys.path 顺序风险 → 已解决 ✅ 且裁定经实测确认无新坑

修订弃 sys.path 方案, 改 `importlib.util.spec_from_file_location("aria_sc_detailed_tasks", <abs path>)` 直载。我实跑了这条路径 (真实 SOT 文件):

| 实测项 | 结果 | 意义 |
|--------|------|------|
| 载入成功 + 两符号可取 | OK (`parse_detailed_tasks` / `is_done_status` 均在) | 可行性成立 |
| `sys.path` 是否被改动 | 否 (无 `state-scanner` 条目新增) | R2 m-1 的顺序不变量问题**结构性消失**, 非靠注释兜 |
| `"lib" in sys.modules` | False | 双 `lib` 包名碰撞面彻底不进场; `owner_container()` 的 `from lib.identity` 不再有被连带废掉的通道 |
| smoke parse | `{'parse_ok': True, tasks: [T-1/pending/'a', T-2/done/'']}` | 顺带二次确认 R2 第 6 项 (title 缺失 → `''` 非 None) |
| `__pycache__` 副作用 | 仍写 `detailed_tasks.cpython-*.pyc` (path-based, 非 module-name-based) | 自定义模块名**不**污染 SOT 侧 pycache, 无新文件 |

可行性前提复核: `detailed_tasks.py` 实测 273 行, `^import|^from` 全量只有 L33 `from __future__` + L35 `import re` — 零包内相对导入, 文件直载无依赖缺口 ✓。proposal 所述属实。

**R2 我提的首选方案被采纳, 且我没预见到的坑经实测为空**。§What 4 对 R1 方案「为何被推翻」保留了完整谱系 (不是静默换方案), 后续 reviewer 不会重开。

### m-2 SC-8 与分支进入条件矛盾 → 已解决 ✅ 分界经实测确认正确

修订改「open-attempt 存在性语义」, 撤掉 `isfile()` 前置闸。我按 spec 的分界逐形态实跑:

| 形态 | 实测异常 | `isinstance(e, OSError)` | spec 归档 | 判定 |
|------|----------|---------------------------|-----------|------|
| yaml 是目录 | `IsADirectoryError` [Errno 21] | True | sentinel (b) | ✅ SC-8 现可达且必然触发, 矛盾消除 |
| symlink 自环 | 裸 `OSError` [Errno 40 ELOOP] | True | sentinel (b) | ✅ 无专属子类, 落 else 分支正确 |
| 父路径是普通文件 | `NotADirectoryError` [Errno 20] | True | 缺席 | ✅ **归缺席是对的** (见下) |
| 断链 symlink | `FileNotFoundError` [Errno 2] | True | 缺席 | ✅ 行为正确, 但论证有矛盾 (m-2 new) |
| 文件不存在 | `FileNotFoundError` | True | 缺席 | ✅ |

`NotADirectoryError` 归缺席的架构正确性 (spec 没写出理由, 我替它验了): 本函数是 `os.listdir(changes_dir)` 无 `isdir` 过滤的裸遍历 (真代码 L164-166), 所以 `changes_dir` 里任何**普通文件** (README.md 之类) 都会走到 `<file>/detailed-tasks.yaml` 并抛 `NotADirectoryError`。这一形态的现实主因就是「这个条目根本不是 spec 目录」= 真缺席, 不是异常。若归 sentinel, 每个杂散文件都产一条噪音 sentinel。**归缺席是唯一正确档**, 且与现行 tasks.md 分支 `isfile()` 的行为逐条 parity。

### m-3 SC-6 新依据不成立 → 已解决 ✅ 替换依据经路径实算确认

SC-6 改写为「lib 迁移红灯不靠此: SC-1 走 helper **默认路径**实算 SOT」, 并在 SC-1 加了「须走默认路径」的硬约束。路径实算复核:

`handoff_autofill.py` 在 `aria/skills/session-closer/scripts/` ⇒ `Path(__file__).resolve().parents[2]` = `aria/skills` ⇒ 兄弟 skill SOT = `aria/skills/state-scanner/scripts/lib/detailed_tasks.py` ✓ 与本文件既有两处先例 (L48 `parents[2]/"state-scanner"/"scripts"`、L318 `parents[2]/"state-scanner"`) 同型, proposal 的先例引用准确。

结论: SOT 挪位 ⇒ 默认路径解析失败 ⇒ helper 返回 None ⇒ 走 `sot_load_failed` sentinel ⇒ SC-1 断言的「2 条 + `source=detailed-tasks.yaml:{name}`」立刻失败。**红灯链结构性成立**, R2 我指出的「state-scanner 侧回归对本侧零信号」已被正确替换, SC-6 降格为诚实的邻接回归纪律。

### m-4 sentinel 缺可判别标记 → 已解决 ✅

§What 3 定死 `source = f"detailed-tasks.yaml:{name}:unavailable"` + `kind ∈ {sot_load_failed, read_failed, parse_failed}`, 并明写「SC 断言锚定 source 后缀与 kind, 不断自由文本」。SC-5/SC-7/SC-8 三条已同步改为按 kind 断言。措辞漂移导致假绿/误红的通道关闭; §2 渲染时人类也能区分「3 条待办」与「1 条读不出来」。输出 schema 仍 `{source, item}`, §Impact 兼容性结论不变 ✓。

---

## 二、本轮新增 (2 Minor, 均文本级, 不阻断 Approved)

### m-1 (new) `UnicodeDecodeError` 落在 OSError 分类之外 — 唯一逃逸出「三形态闭包」的路径

位置: §What 1 (「直接 `open()`」, 未规定 encoding/errors)

spec 把异常面**穷举**成两桶 (`FileNotFoundError`/`NotADirectoryError` ⇒ 缺席; 其余 `OSError` ⇒ sentinel), 并以此支撑 §What 3 的全称约束「yaml 在场 ⇒ 要么真实条目要么 sentinel」。实测反例:

```
badenc.yaml (含 \xff\xfe 字节) -> UnicodeDecodeError (isinstance OSError = False)
```

`UnicodeDecodeError` 是 `ValueError` 子类, **不是 OSError** ⇒ 两桶都接不住 ⇒ 异常穿透 `grep_unchecked_tasks` → `assemble_from_snapshot` → 整个 autofill 崩, handoff 写不出来。

严重度按「是否复刻病根」判: 崩是**响的**, 不是静默 0, 所以不重开 #121 病根 ⇒ minor 而非 major。但它破坏 spec 自称的闭包性, 且修法是一个参数:

- 本仓两处同类先例**都已经解决了这个问题**: 现行 tasks.md 分支 L169 `open(tasks, encoding="utf-8", errors="replace")`; 姊妹消费方 `spec_complete.py` L202 `read_text(encoding="utf-8", errors="replace")`。实测 `errors="replace"` 下同一文件正常返回 `'��\x00bad'`, 交给 parser 后自然落 `parse_ok=False` → `parse_failed` sentinel — **恰好是本 spec 想要的归档**。
- 建议 §What 1 一句话写死 `open(p, encoding="utf-8", errors="replace")` (「沿用 L169 既有惯例」), 并把 `.read()` 明确纳入同一 `try` 块 (open 不解码, 解码发生在 read)。

### m-2 (new) §What 1 的论证把「断链 symlink」列为被治形态, 但 SC-9 把它锁成 0 条无 sentinel — 论证与行为自相矛盾

位置: §What 1 论证句 vs SC-9 子 case

- 论证句: 「`isfile()` 对**目录/断链 symlink** 返回 False, 会把这些异常形态静默送进「双缺席」分支报 0 — 以新机制复刻病根」
- SC-9 子 case: 「yaml 为断链 symlink → `FileNotFoundError` 归入缺席**同样 0 条无 sentinel**」

即: 换成 open-attempt 后, 目录形态确实被救了 (`IsADirectoryError` → sentinel), 但断链 symlink 的结局与 `isfile()` 方案**逐字相同** (0 条无 sentinel)。论证却把它算作 open-attempt 解决掉的病根之一。

**行为本身我不反对**——`FileNotFoundError` 语义准确 (指向的目标确实不存在), 且 SC-9 显式锁定了这条边界 (是有意决策不是遗漏), 现实中没人会 symlink `detailed-tasks.yaml`。这也是我 R2 提出该点后的一个**明确裁定**, 按收敛纪律算已处置。

问题只在论证文本: 未来 reviewer 读 §What 1 会以为断链 symlink 产 sentinel, 与 SC-9 对照即认定实现有 bug, 白重开一轮。建议删掉论证句里的「/断链 symlink」, 或补一句「断链 symlink 语义上判为缺席 (指向目标不存在), 与目录形态不同档 — SC-9 锁定」。

---

## 三、Nits (不计入 minor_count, 顺手改)

1. **importlib 配方三个落地细节值得在 §What 4 或 Tasks 1.1 点名**, 免得实施临场踩:
   (a) 必须 `import importlib.util` — 裸 `import importlib` 不保证绑定 `util` 子模块;
   (b) 必须调 `spec.loader.exec_module(module)` — 实测 `spec_from_file_location` 对**不存在的路径仍返回合法 spec** (loader = SourceFileLoader), 失败点在 exec_module 抛 `FileNotFoundError`。SC-5(b) 因此可达 ✓, 但若实现漏调 exec_module, SC-5(b) 仍会因 `AttributeError` 而「通过」——**该 SC 无法区分「载入正确」与「从未 exec」**, 真正兜底的是 SC-1。不改判据, 记录供实施者知情。
   (c) helper 宜在 spec 目录循环**外**调一次 / 或做模块级 memoize; 否则 N 个 yaml-only spec ⇒ N 次模块执行 + N 个模块对象 (仅浪费, 无正确性问题, 因本 spec 只用纯函数)。
2. SC-1「须走 helper **默认路径** (真实仓布局解析 SOT)」与末条「fixture **全部**用独立 tempdir (不依赖 repo 布局)」措辞相抵。实质不冲突 (tempdir 只隔离 `changes_dir`, SOT 由 `parents[2]` 实算), 建议末条限定为「fixture **数据面** (changes_dir/spec 目录) 全部用独立 tempdir」。
3. R2 nit 3 (tasks.md 分支既有静默 `continue` 属存量、建议 §Impact 记一笔 scope-out 理由) 仍未采纳。同一函数内两套 OSError 政策会被下个 reviewer 当新发现重开, 成本一行。

---

## 四、收敛判定

| 轮次 | Critical | Major | Minor | 新增 finding 性质 |
|------|----------|-------|-------|-------------------|
| R1 (本 agent) | 0 | 2 | 5 (+1 建议) | 结构性 (返回值形态 / scope 封闭性) |
| R2 | 0 | 0 | 4 | 机制级 (sys.path 顺序 / fixture 与语义矛盾 / 依据不成立 / 判别位) |
| R3 | 0 | 0 | 2 | 文本级 (一个参数 / 一句论证) |

判定 **CONVERGED**, 理由三条:

1. **严重度单调下降且已触底**: R1 结构性 → R2 机制级 → R3 文本级。R3 两条都是「一个参数 + 一句话」量级, 且各自有仓内现成先例可抄, 无设计空间待探。
2. **修订未引入回归**: R2 四条裁定我逐条实机验证 (非推断), 三条经实测确认架构正确 (importlib 零 sys.path 触碰 / 异常分类五形态全对 / 默认路径红灯链成立), 一条 (sentinel 判别位) 纯加固无副作用。**没有出现「加固本身重开同类 bug」** (memory `feedback_multiround_audit_catches_fix_introduced_regression` 的典型失败态未发生)。
3. **无未决设计裁量**: R2 我要求「必须在 Phase B 落地前裁决、不留给实现临场决定」的两处 (存在性语义 / sentinel 判别位) 均已在 spec 内写死。R3 两条 minor **不含裁量** — 都是照抄既有惯例, 实施者不会分叉。

建议: 两条 minor 直接落进 proposal 文本 (无需再开审计轮), 随后 Approved 进 Phase B。

## 五、本轮复核通过、明确不再重开

1. R2 已核销的 R1 全部 findings (M-1/M-2/m-1~m-4) 本轮抽验未回退。
2. 关键决策表 7 行与 §What 正文逐条同源, 含「否决 snapshot 加字段路线」与「范围」两行 — 两处历史争议点均已封存。
3. rule6_note (deterministic 脚本 → SC 级 baseline-failing substitute) + PATCH 定级 + §Impact ship 同步面, 与 Rule #6 判据表「描述性/deterministic ⇒ substitute」一致, SKILL.md 零变动确实无照跑面。
4. §What 5 的可测缝论证 (monkeypatch helper 是唯一能可证伪测到降级的缝) 在 importlib 方案下**依然成立且更干净** — 实测直载模块以唯一名注册, 裸名空间零污染, 不存在「改 sys.path 测降级」的假绿替代路径。
