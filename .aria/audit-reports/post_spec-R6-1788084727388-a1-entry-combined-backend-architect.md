---
checkpoint: post_spec
round: 6
role: backend-architect
verdict: REVISE
scope_ok: true
counts: 0C/2M/1m
---

# post_spec R6 — a1-entry 三份 Spec · backend-architect 席 (代码宿主与机制实证)

## (a) 本席镜头一句话

对三份 Spec 里每一条「代码」类 SC、每一处 Impact 代码落点、以及 2026-08-30 新写的六处机制点, 逐条到 aria `d50f9c3` 实读代码 + 在 `/tmp` 实跑最小复现, 只问「宿主真在、语义真符、坏实现真会红」三件事, 不评价设计取舍本身。

## (b) Findings

结论先行: 本席核对的约 60 处「文件:行号 + 逐字引文」在 `d50f9c3` 上**全部逐字精确命中, 零一处漂移或篡改**(细节见 (d))。真正的机制缺口只有 2 条, 且都落在 2026-08-30 当轮新写的文本上(SC-32 的 argparse 契约 / 探针的 `sys.path` 双插入)。以下按严重度列出。

### Major

---

**母 M1 — SC-32 要求 `--heartbeat-only` 模式下 argparse 不得强制 `--raw-track-id`, 但现状该参数是无条件 `required=True`, Impact 表未提及需要改这一行**

- **Spec 行号 + 逐字引文**(`openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` SC 表, SC-32 行):
  > 编排层两级来源(§2.2 ①②)都取不到 ⇒ **仍**调用 `phase1_gate.py --heartbeat-only --phase A.1 --repo-path <repo>` 且**不传** `--raw-track-id`(**该模式下 argparse 不得要求它**)

  同一份 Spec §2.2 正文逐字写:
  > **`--heartbeat-only` 刷哪条 track**……**③ 两级都取不到 ⇒ 编排层仍调用且不传该参数**

  Impact 表「第二处变更」行只描述了 `--heartbeat-only` 的应用层回落逻辑(遥测记录 / 不写新 claim), **完全没有提到需要改动 `--raw-track-id` 的 argparse 定义本身**。

- **代码行号 + 逐字引文**(`git -C aria show d50f9c3:skills/state-scanner/scripts/phase1_gate.py | sed -n '1185,1192p'`):
  ```
  1185      parser.add_argument(
  1186          "--raw-track-id",
  1187          required=True,
  1188          help="用户选定的 carry-id 原始串(未归一; run_gate 内部 derive_track_id 归一)",
  1189      )
  1190      parser.add_argument(
  1191          "--phase", required=True, help="当前十步循环 phase(如 B / B.1), 写入 claim"
  1192      )
  ```
  `parser` 是单一 flat `ArgumentParser`(无 subparsers), `--raw-track-id` 在**全部**调用模式下都是 `required=True`。这是 argparse 库自身在 `parser.parse_args()` 阶段做的校验, 发生在**任何应用代码(包括 `_main()` 里将来新增的 `--heartbeat-only` 分支判断)执行之前**。

- **为什么这是缺口, 不是「怎么会红」列已经覆盖的坏实现**: SC-32 的「怎么会红」只点名了一种坏实现——「只 `logger.debug` 不落盘」——这是**应用层**的坏实现, 隐含前提是 CLI 调用本身已经成功进入 `_main()` 内部逻辑。但如果实现者只是照字面加一个 `--heartbeat-only`(store_true)开关而**不动** `:1187` 的 `required=True`, 那么 `python3 phase1_gate.py --heartbeat-only --phase A.1 --repo-path <repo>`(不传 `--raw-track-id`, 这正是 SC-32 要测的场景)会在 argparse 阶段直接被拒:
  ```
  error: the following arguments are required: --raw-track-id
  ```
  程序在进入 `_main()` 函数体之前就已经以非零退出码终止, SC-32 期望的「遥测 JSONL 新增恰一条 `outcome="skipped_no_track"` 记录」根本没有机会发生——这是一种比「怎么会红」列举的坏实现更早、更根本的失败模式, 且未被列出。
- **实测验证**: 本席未新建代码, 仅静态读出 `:1185-1192` 与 `_main()` 全文(`:1173-1241`), 确认没有任何后置的 `args.heartbeat_only` 分支可以在 argparse 报错之后补救——argparse 的 `required=True` 检查无法被应用层代码绕过。
- **建议处置(只建议, 不落版)**: Impact 表「第二处变更」行需补一句, 明确 `:1187` 的 `--raw-track-id` 需要从 `required=True` 改为 `required=False`, 并在 `_main()` 内新增等价的手工校验(例如 `if not args.heartbeat_only and not args.raw_track_id: parser.error(...)`), 以保证「acquire 模式仍然强制要求 `--raw-track-id`, 仅 `--heartbeat-only` 模式豁免」这条既有契约不被放松成全局可选。SC-32 的「怎么会红」列建议补一条「argparse 层面因未松绑 `required=True` 而直接拒绝调用」的反例。

---

**探针 M1 — `sys.path` 双插入(`state-scanner` skill root 供 `lib.*`, `state-scanner/scripts` 供 `collectors.multi_remote`)按 Spec 文字最直接的读法组合会产生顺序敏感的 `ModuleNotFoundError`, 已知限文本把这个「现在就存在」的碰撞对象错误地描述成「将来才可能出现」**

- **Spec 行号 + 逐字引文**(`openspec/changes/sibling-spec-probe/proposal.md` §3「跨 skill import 的可运行模式」段与 Impact 段):
  > ```python
  > _SS_ROOT = str(Path(__file__).resolve().parents[2] / "state-scanner")
  > if _SS_ROOT not in sys.path:
  >     sys.path.insert(0, _SS_ROOT)
  > from lib.collision import normalize_linked_issue
  > from lib.linked_issue_field import extract_linked_issue_field
  > ```
  > **已知限(成文)**: 该写法把 `state-scanner` 的 skill root 放进 `sys.path`, 于是**顶层包名 `lib` 与 `collectors` 被占用**。
  > 若 `audit-engine` 将来自己长出 `lib/` 或 `collectors/`, 会与之**同名冲突**……

  Impact 段另有一句补充: 「**`resolve_enforced_remotes` 亦经同一路径 import**……该 import 须同时插 `state-scanner/scripts` 到 `sys.path`(它与 §3 插的 skill root 是两条不同路径, 都要)」。两段文字**没有给出一份把两次插入与三条 import 语句合并在一起的完整代码块**, 只是分别叙述, 顺序留白。

- **代码行号 + 逐字引文**(冲突的真正来源——`state-scanner/scripts/` 下**已经存在**另一个名为 `lib` 的包, `git -C aria show d50f9c3:skills/state-scanner/scripts/coordination_probe.py | sed -n '80,89p'`):
  ```
  80  # Deliberately NOT ``import lib.runtime_probe``: in some test sys.path layouts
  81  # the top-level name ``lib`` resolves to state-scanner/lib (Layer L — a
  82  # DIFFERENT package, claim_schema.py etc.), not scripts/lib — the exact
  83  # collision documented in collectors/openspec.py:29. Inserting scripts/lib
  84  # itself onto sys.path and importing the bare module name sidesteps the
  85  # collision entirely.
  86  # ---------------------------------------------------------------------------
  87  _LIB_DIR = str(Path(__file__).resolve().parent / "lib")
  ```
  `git ls-tree d50f9c3 skills/state-scanner/scripts/lib` 证实 `state-scanner/scripts/lib/__init__.py` 真实存在(内含 `runtime_probe.py`/`detailed_tasks.py`/`frontmatter_block.py`/`spec_complete.py`/`carry_forward.py`), 是一个**正式的、带 `__init__.py` 的 Python 包**, 与 `state-scanner/lib/__init__.py`(Layer L, 含 `collision.py`)是两个不同目录但**同名**的包。

- **实测复现(在 `/tmp` 内、按 `git archive d50f9c3 skills/state-scanner` 还原的真实目录树上跑, 未改动仓库任何文件)**:
  - **安全顺序**(先插入 `state-scanner` root 并完成全部 `lib.*` import, 再插入 `state-scanner/scripts` 并 import `collectors.multi_remote`, 最后再补一次 `lib.*` import 验证缓存不被破坏)——**全部成功**, `sys.modules['lib'].__file__` 正确指向 `state-scanner/lib/__init__.py`。
  - **危险顺序**(两条 `sys.path.insert(0, …)` 都在任何 `lib.*` import 之前执行完, 且 `state-scanner/scripts` 后插入、因而排在 `sys.path` 更前面)——`from lib.collision import normalize_linked_issue` 直接失败:
    ```
    sys.path[0:2] = ['.../state-scanner/scripts', '.../state-scanner']
    lib.collision FAILED: ModuleNotFoundError No module named 'lib.collision'
    lib.__file__ (whichever got bound): .../state-scanner/scripts/lib/__init__.py
    ```
    即 `lib` 被错误地绑定成了 `state-scanner/scripts/lib`(该目录没有 `collision.py`), 因为 Python 对同名顶层包按 `sys.path` 顺序解析、一旦绑定就写入 `sys.modules` 缓存。
- **为什么已知限文本不够**: 已知限写的是「**若** audit-engine **将来**自己长出 `lib/` 或 `collectors/`, 会与之同名冲突」——这是在提醒一个假设性的、发生在别的 skill(`audit-engine`)身上的未来风险。但本席实测证明, **同名碰撞的另一方今天就存在, 就在同一个 `state-scanner` skill 内部**(`scripts/lib/`), 且被 `coordination_probe.py` 明确记录过、明确避开过。探针脚本要不要踩中这颗雷, 完全取决于两处 `sys.path.insert()` 与三条 `import` 语句在最终文件里的**书写顺序**, 而 Spec 从未给出这份合并后的完整代码, 只给了两段各自独立、读者需要自己拼接的片段——按最直白的「先把两条路径都插好, 再统一写 import」的写法(这也是很自然的编码习惯), 恰好踩中危险顺序。
- **建议处置(只建议, 不落版)**: (1) 已知限一句改为诚实版本——「顶层包名 `lib` 与 `state-scanner/scripts/lib`(既有包, 含 `runtime_probe.py` 等)**现在就**同名, `coordination_probe.py:80-85` 已为同一根因绕开过一次」; (2) §3 与 Impact 段的两处代码片段合并成**一份**唯一的、顺序确定的代码块(`state-scanner` root 插入 + 全部 `lib.*` import 必须先于 `state-scanner/scripts` 插入 + `collectors.multi_remote` import), 消除「两处引用各自独立、由实现者自行拼接」的欠定状态; (3) 建议给 `test_sibling_spec_probe.py` 补一条针对导入顺序的回归测试(例如断言不论 `_SS_SCRIPTS` 是否已经在 `sys.path` 中, `lib.collision` 都能正确解析), 防止未来重构改变插入顺序时静默复发。

### minor

**母 m1 — Impact 表为 `heartbeat_by_track` 与新增的 `get_container_uuid` 各自平行复刻了既有函数(`release_claim_by_track`/`get_container_id`)的整段样板逻辑, 未提示可抽取共享 helper**

- `lib/identity.py:191-244` 的 `get_container_id()` 已经完整实现「读文件 → 解析 uuid/label → 首次生成 → 写文件 → hostname 兜底」的全部分支; Impact 表为 `get_container_uuid()` 写的签名是**独立的新函数**, 按描述("跳过 label")需要重复这一整段 I/O 逻辑, 唯一差异只是最终 `return uuid` 而非 `return label if label else uuid`。这不是宿主不存在或断言会假, 只是一处「本可以让 `get_container_id` 内部调用 `get_container_uuid` 再套 label 优先逻辑, 反过来更省一次重复」的实现质量提示, 不影响任何 SC 的可构造性, 故列为 minor。`heartbeat_by_track` 与 `release_claim_by_track` 之间的关系不受此影响——二者本就是 Spec 明确要求的「照抄并存模式」, 不是同一形状的问题。
- 建议处置: A.2 拆任务时可提示实现者评估是否把 `get_container_id` 重写为 `get_container_uuid()` 的一层薄封装(`return _read_or_generate().label_or_uuid`), 但不阻塞本 Spec 的裁决。

## (c) SC 核验表(代码类为主; 行为类只标注「非本镜头对象」)

| SC | 宿主实存? | 坏实现会红? | baseline 红/绿与 Spec 自述一致? |
|---|---|---|---|
| 母 SC-2(CLI 全链路, overlap 双向) | 是——`linked_issue_overlaps`(`collision.py:230-234`)、`_main()` 调用处(`phase1_gate.py:1233-1235`)均实存 | 是——负控删掉 `:278-279` 自排除两行, 或让 `:1230` 门控丢失 `--linked-issue` 分支, 均会让正/负控翻转 | 一致, baseline 即绿属实(现有三参数签名今天就能跑通正控与负控) |
| 母 SC-3(container-uuid accessor) | 是——`get_container_id`(`identity.py:191`, `:222` label 优先, `:242` hostname 兜底, `:244` 新生成 uuid)全部逐字命中; 新 accessor 待建 | 是——直接调 `get_container_id()` 在设了 label 的夹具上必红, 可辨 | 一致, baseline 必红(新 accessor 不存在) |
| 母 SC-5~7(heartbeat by-track) | 部分——`heartbeat()`(`:178-256`, 逐字段重建 11 字段确认)、`release_claim_by_track` 并存范式(`:377-407`)均实存; `heartbeat_by_track` 待建 | 是——SC-7 第二臂点名的既有测试 `test_sweep_stale_cross_container_fresh_untouched`(`test_release_by_track.py:380`)已核实只覆盖「超时」臂、不覆盖「心跳后免疫」臂, 结论成立 | 一致, baseline 必红 |
| 母 SC-8(终态可见性) | 是——`_TERMINAL = ("done", "abandoned", "unknown")`(`collision.py:268`)逐字确认不含 `yielded` | 是 | 一致 |
| 母 SC-10 / SC-25(`fetch_degraded` / error 双字段) | 是——`GateResult.error` 文档在 `:210` 预留 token, 全文再无第二处赋值(`grep fetch_degraded` 仅命中该行); 除 `:1236-1238` 外无其他 except 写手 | 是 | 一致, baseline 必红属实 |
| 母 SC-14(a)/SC-23(carry-id 闭环) | 是——`release_gate.py:236-237` 的三选一 `parser.error` 逐字确认; `release_claim_by_track` 匹配键(`:422-428`, container+track_id+status=="active")确认第三方不受影响 | 是 | 一致 |
| 母 SC-15(改名两步, baseline 即绿) | 是——`release_claim_by_track:377`、`acquire_claim:99` 均实存且匹配键精确到 `(container, 归一 track_id, status=="active")`, 不含 `linked_issue`/批量维度 | 是——把匹配键改成按 `linked_issue` 或按 container 批量, 第三方 claim 会被误伤, 可辨 | 一致, 本席认为这条「baseline 即绿」诚实且可被打破(非装饰性恒真) |
| 母 SC-22(①-⑥ 文本层) | 是——宿主 `test_coordination_default_lockin.py` 确认存在; `branch-manager/SKILL.md:146` 标题 "Part A1" 与命令 `--phase B` 的错位确认属实 | 是——裸 `assertIn` 对「塞进现有 YAML 列表」免疫, Spec 已自陈并要求块边界断言, 逻辑自洽 | 一致, baseline 必红(两处 SKILL.md 目前均无该步骤块) |
| 母 SC-24 | 是——`ReadClaimsResult`(`coordination_ref.py:119`)、`read_claims`(`:596`)、`parse_claim` unknown sentinel(`claim_schema.py:222-233`, 确认不传 `linked_issue`)均逐字命中 | 是 | 一致 |
| 母 SC-28/SC-29(baseline 即绿, 自我排除) | 是——`:278-279` 自排除逻辑今天就在跑 | 是——删除该两行即可验证负控会红(memory `adversarial-fixture` 要求的验证方式) | 一致, 诚实 |
| 母 SC-32 | 见 Major 母 M1 — 应用层宿主待建, 但 argparse 层存在未声明的结构性冲突 | **否, 不完整**——只覆盖了应用层坏实现, 漏了 argparse 层坏实现 | 见 M1 |
| 母 SC-33 | 是——`:1230` 门控、`:1236-1238` except 分支逐字确认现状只赋 `linked_issue_overlap=[]`; 同时赋 `unknown_schema_claims=None` 与 `linked_issue_overlap_error` 在机制上无冲突(纯字典赋值, 无并发/顺序约束) | 是 | 一致, baseline 必红属实 |
| 字段 SC-1~4(E0-E6) | 部分——`lib/linked_issue_field.py` 待建(确认 `d50f9c3` 上不存在), 但其唯一依赖 `normalize_linked_issue`(`collision.py:178`)签名与语义逐字确认, 且 `collision.py:46` 的 `from .claim_schema import` 相对导入模式证实新模块内部对 `normalize_linked_issue` 走包内相对导入即可, 无跨包障碍 | 未直接实跑坏实现(纯函数尚未落地), 但夹具设计(first-code-span 反例等)有真实语料支撑, 可信 | baseline 必红属实(模块不存在) |
| 字段 SC-6/SC-7a(模板/预览骨架) | 是——SOT `standards/openspec/templates/proposal-minimal.md` 头部三行(`Level`/`Status`/`Created`)确认, `spec-drafter/SKILL.md` 预览围栏 `:127-162`、头部仅两行(`:139-140` 只有 `Level`/`Status`)逐字确认, 与 SOT 漂移(缺 `Created`)属实 | 是 | 一致, baseline 必红属实 |
| 字段 SC-9(`--emit-arg`) | 待建, 无既有反例, 设计自洽(与母 Spec §2 的省略语义对应一致) | 未实跑, 纯函数级设计无阻断性问题 | N/A(新模式) |
| 探针 SC-5~6(层 0 定位/围栏/cap) | 是——`d50f9c3` 上 `audit-engine` 确认无 `scripts/`、无 `tests/`(需新建两个目录), `resolve_enforced_remotes`(`multi_remote.py:255-286`)签名逐字确认 | 未独立复算三臂计数(147 篇语料的统计核验超出本席「代码宿主」镜头, 留给量化类镜头), 定位规则本身(行首+围栏+文档序)在机制上自洽 | N/A(见上) |
| 探针 SC-12~14(默认分支解析) | 是——`fetch_gate.py:108-128`(`_resolve_default_branch`, `_ORIGIN_HEAD_REFS` 全部为 `refs/remotes/origin/*`)、`:55` fallback 名字猜测、`:86-101` `_classify_error` 五分类均逐字确认, 与探针「不复用」的理由完全对应 | 是——照抄 `_DEFAULT_BRANCH_FALLBACKS` 的坏实现在 `github` remote(本仓真实无 symbolic-ref)上会失败, 可辨 | 一致 |
| 探针 SC-17/SC-20(execution-modes.md 双插入) | 是——`## Convergence 模式`(`:84`)+`Round N:`(`:89`)、`## Challenge 模式`(`:113`)+`Round N (一个完整周期):`(`:118`)插入点逐字确认; `Step 0`(`:83`, Round 1 前一次性)与「每轮」语义冲突确认属实 | 是 | 一致 |
| 探针跨 skill import(§3 code block) | 见 Major 探针 M1 | 见 M1 | 见 M1 |

## (d) 本席核验为真、无 finding 的清单

以下均已到 `d50f9c3` 逐字核对, 与 Spec 引文完全一致, 未发现问题:

1. `ClaimRecord` 确为 `@dataclass(frozen=True)`(`claim_schema.py:69`); `heartbeat()` 的逐字段重建恰好 11 个字段(`claim_lifecycle.py:244-256`); `dataclasses.replace(existing, heartbeat_at=…)` 与序列化路径`serialize_claim()`(`claim_schema.py:315-337`)完全兼容——该函数用纯属性访问(`record.schema_version` 等), 不依赖构造方式, 新写的 `heartbeat_by_track` 用 `dataclasses.replace` 不会引入任何序列化不一致。
2. `get_container_id()` 的 `:191`/`:222`(label 优先)/`:242`(hostname 兜底)/`:244`(新生成 uuid)四处引用全部逐字精确, FIX-18 的勘误(`:244` 而非 `:242` 才是 hostname)属实。
3. `lib/collision.py` 的 `normalize_linked_issue`(`:178`)、`linked_issue_overlaps` 三参数签名(`:230-234`)、`_TERMINAL` 定义不含 `yielded`(`:268`)、两道丢弃门(`:272-273`/`:274-275`)、自排除(`:278-279`)、`:46` 的相对导入全部逐字精确。
4. `phase1_gate.py` 的 `--phase required=True`(`:1191`, 无 `choices=`)、`:1230` 门控、`:1233-1235` 唯一调用处(`_run_gate_impl` 内 grep 命中 0 已复核)、`:1236-1238` except 分支现状、`GateResult.error` docstring 预留 `fetch_degraded` 但全文无第二处赋值(`:210`)、`run_gate`(`:1032`)/`_run_gate_impl`(`:335`)/`_main`(`:1173`)行号、Step 9 `resilient_push`(`:791-802`)与 7a self-resume(`:512-533`)两个无条件推送点, 全部逐字精确。
5. `release_gate.py` 的三选一 `parser.error`(`:236-237`)、`:225` help 文案确写 `STALE_TTL`(与既有既有措辞缺陷一致)、`:172` 无条件推送、`:141` `sweep_stale_active` 未传覆盖参数, 全部逐字精确。
6. `lib/constants.py` 全文核对: `STALE_TTL=1800`(`:36`)、`SWEEP_TTL=86400`(`:51`)、`:32` 不变量注释、`:40-44` 三行逐字("Deliberately much longer than STALE_TTL"…)、`:43-44`("NO production heartbeat loop exists"…)、`:50`("Revisit when a heartbeat loop ships")全部逐字精确。
7. `lib/reconcile.py:154-163` 的 `_is_stale()` 与末行 `return age_seconds > STALE_TTL`、`lib/gc.py:324`("rewritten to `status='abandoned'`")、`:338-344`(`sweep_stale_active` 默认 `SWEEP_TTL`)全部逐字精确。
8. `coordination_ref.py:800` 的 `bootstrap(repo_path=repo, push=False)`、`:119`(`ReadClaimsResult`)、`:596`(`read_claims`)全部逐字精确; `write_claim` 序列化经 `serialize_claim(record)` 走纯属性访问, 与母 Spec §5.3 的实现纪律无冲突。
9. `phase-b-developer/SKILL.md:86-99` 的 B.0 块(标题、`:91-93` 调用模板、`:96-97` 「write_claim auto_bootstrap 会自动建 ref 并 push」的原文、`:98` `coordination.enabled` skip 项)全部逐字精确——2026-08-30 的推送点勘正(改指向 `phase1_gate.py` Step 9 与 7a)本身在代码层完全站得住, 且已在 `007d355`(`git diff --stat d50f9c3 007d355` 确认仅改 `phase1_gate.py`/`release_gate.py`/`failure_handlers.py`/新测试文件, 含 `--no-push`/`ARIA_COORDINATION_NO_PUSH`/`push_skipped`/`push_skipped_reason` 等要素)落地为真实修复, 与决策单描述一致。
10. `branch-manager/SKILL.md:146-152`、`phase-d-closer/SKILL.md:38-58`(D.2b 表行 `:42`、调用 `:51-52`、说明句 `:55` 逐字"carry-id = Phase B-entry 时传给 phase1_gate 的同一原始串"、`:56` 既有 STALE_TTL 措辞缺陷)全部逐字精确。
11. `config-loader/DEFAULTS.json` 的 `state_scanner` 段确认**没有** `coordination` 键(rule6_note 的 substitute check 断言基线为真红, 非装饰性恒真); `config-loader/SKILL.md:134`(`enabled`)/`:140`(`mode`)登记确认; `adaptive_rules.level_3="challenge"`(`:124-127`)确认。
12. `.aria/state-checks.yaml` 当前 11 条 check(`main-project-version-consistency` 为第 11 条)、`issue-cache-freshness`(`:12`)、`coordination-gate-invocation`(`:221`)行号全部与字段 Spec 引文精确一致。
13. `session-handoff.md` §2.3(机读 frontmatter schema)与 §2.3.8(`:217`, 结构化 Carry-id, 明确"非 frontmatter")、§2.3.8.3 硬约束段全部与引文一致, R3/KM-1 的行号勘正属实。
14. `phase-a-planner/SKILL.md:9`、`spec-drafter/SKILL.md:9-10` frontmatter(`allowed-tools` 变更前状态、`user-invocable: true`)全部逐字精确; `phase-a-planner/SKILL.md:62-73` 的 A.1 YAML 块(`:66` `skip_if: complexity: Level1`)确认无 `precondition:` 键, baseline 必红属实。
15. `spec-drafter/SKILL.md:125-162`(`### Level 2 预览` 围栏边界)、`:139-140`(头部仅 `Level`/`Status` 两行)与 SOT `proposal-minimal.md` 三行头部(多 `Created`)的漂移, 逐字确认, R5-5/SC-7a 的诊断准确。
16. `state-scanner/SKILL.md:149`(接线点为 AI 编排层)、`:168`(CLI 输出键集不含 `push_skipped`)、`:176`(既有 STALE_TTL 措辞缺陷)全部逐字精确。
17. `audit-engine/SKILL.md:83-85`(Step 0, "Round 1 启动前一次性")、`execution-modes.md:84/89`(Convergence 插入点)、`:113/118`(Challenge 插入点)全部逐字精确; `d50f9c3` 上 `audit-engine/` 确认只有 `SKILL.md` 与 `references/`, 无 `scripts/`、`tests/`。
18. `handoff_autofill.py:403-407`(`from lib.identity import`)与 `:48-51`(`from collectors.multi_remote import`)两处跨 skill import 先例逐字精确; 本席另确认该文件的两处用法各自函数作用域独立、且从未在同一进程内触发 `lib` 与 `scripts/lib` 的同名竞争(它只消费 `lib.identity` 与 `collectors.multi_remote`, 两个互不相干的顶层名), 因此它是「跨 skill import 模式可行」的有效先例, 但**不构成**「双路径同时插入不会互相顶替」的先例(这正是探针 M1 的缺口)。
19. `multi_remote.py:255-286` 的 `resolve_enforced_remotes(configured, actual_remotes, read_only)` 签名与截断逻辑(`configured` 真值判定)逐字精确; 模块 docstring 自陈 stdlib-only, 与探针脚本的 import 不会引入传递性第三方依赖。
20. `run_all_tests.sh:48`(`find … -type d -name tests`)、`:50`(跳过空目录)、`:71`(`unittest discover`)逐字精确; `test_release_by_track.py:380`(既有测试)、`:531`(subprocess 体例先例)逐字精确; `test_coordination_default_lockin.py` 确认存在。

## (e) 收敛判断

本席两条 Major finding **全部**落在 2026-08-30 当轮新写/新入表的文本上(母 SC-32 是 rework v4 当轮才从「K 段诊断」回灌进 SC 表的; 探针的 `sys.path` 双插入组合是 2026-08-30 才新增的「`resolve_enforced_remotes` 亦经同一路径 import」补丁, 其「新表面」清单第 10 条本身就写着「未实跑两条并存时的包名解析……请 R6 / A.2 实测」)——即 2/2 = 100%。

除此之外, 本席对贯穿全文、横跨 R1-R5 历次修订的约 60 处「文件:行号 + 逐字引文」逐条实读, **无一处**发现宿主不存在、语义相反或引文失真——这是本轮审计里少见的高精度水平, 说明前几轮审计对旧文本的事实核验已经相当扎实, 不需要在这些点上再花力气。

**本席同意「设计侧已收敛」这一结论**, 但有一个限定: 收敛的是**架构与既有代码引用**这一层面, 2026-08-30 当轮为了清账新入表/新组合的两处机制细节(SC-32 的 argparse 契约、探针的双 `sys.path` 顺序)还没有被这个精度水平覆盖到, 需要在落地前补一句 Impact 表文字(母 M1)和合并成一份确定顺序的代码块(探针 M1)——两条都是「文字补丁级」的修复, 不需要重新论证任何设计决策, 也不影响 owner 已裁的六项结论。若这两条按建议处置收口, 本席认为三份 Spec 已具备进入 A.2 的代码层前提条件。

## (f) Counts

0 Critical / 2 Major / 1 minor
