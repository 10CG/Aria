---
checkpoint: post_spec
round: 4
role: code-architect
verdict: REVISE
scope_ok: true
counts: 2C/5M/1m
---

# post_spec R4 — a1-entry 三份 Spec 联审 — code-architect 席 (实现蓝图可行性)

> **⚠️ 落盘说明**: 本席工具集仅 `Read/Glob/Grep/WebFetch/WebSearch`, **无法自行写盘**;
> 回执以正文返回, 由**主控代为落盘**并逐条复核。主控对两条 Critical 都做了独立实读, 结论见各条下方。
> 基线: 主仓 `322f280`; aria `d50f9c3` (本席经 GitHub 镜像核实 `58a49e7`→`d50f9c3` 的 2 commit 不触及任何被引文件, 故以工作树核验等价)。

## C-1 (Critical, 母 Spec) — SC-2 引用了本 Spec 自己声明「不存在」的函数

§2.1a `:164` 逐字:「**本 Spec 不新增拼接函数** —— 新增代码落点只有 `lib/identity.py` 的直取 `uuid` accessor」。
而 SC-2 的夹具硬约束逐字要求「两条 track-id **必须由 §2.1a 的 compose 函数派生**(不得手写字面串)」。
全文 grep `compose` **仅命中 SC-2 自身** ⇒ 实现者写夹具时字面上找不到可 import 的对象。
**这正是本项目三次最重 critical 共同的形状 (要求改/调一个不存在的函数)。**

**主控复核**: **成立, 且是主控 R3 清账轮 (M16 反恒绿) 引入的。** 已订正 —— SC-2 改为「按 §2.1 规则**手写拼接**」
并显式标注「拼接无代码宿主是 §2.1a 成文交付的一半」, 归一仍走 `lib/track_id.py::derive_track_id`;
负控臂 (容器段置空) 保留, 它才是 SC-2 的牙齿。

## C-2 (Major, 母 Spec) — 两处新库函数只有落点文件, 没有函数签名

`heartbeat` by-track 并存变体 与 `identity.py` 直取 uuid 的 accessor, 全文 (§2.2 / D16 / Impact) 均无函数名与签名,
对照 `release_claim_by_track(raw_track_id, status, identity, repo_path, *, now)` 的精确度明显不足 ⇒
A.2 两个实现者可能各起其名, 与 SC-3 / SC-5~7 对不上 (memory `spec-underdetermination`)。

**主控复核**: 成立。已补 —— `def heartbeat_by_track(raw_track_id, identity=None, repo_path=None, *, spec_slug=None, now=None) -> AcquireResult`
与 `def get_container_uuid(home_dir: Optional[Path] = None) -> str`, 分别镜像 `release_claim_by_track` / `get_container_id`。

## S-1 (本席判 Critical → **主控实读后降为 Major**) — 跨 skill import 未证可行

本席依据: 本仓唯一相关先例是**反例** —— `fetch_gate.py:111-112` 逐字「replicated to keep phase-d-closer
self-contained — **no cross-skill runtime import**」; 且 `audit-engine/` 无 `scripts/`、无 `__init__.py`;
`sys.path` 技巧只解决「同 skill 内 scripts/ import lib/」。

**主控复核 —— 前提部分不成立, 故降级**:
- 反例为真, 但那是**该处的取舍**(为 self-contained 而复制), **不是仓级禁令**;
- **先例确实存在**: `skills/session-closer/scripts/handoff_autofill.py:403-407` 逐字
  「# state-scanner/lib 是兄弟 skill 的包; 加其 skill root 使 `from lib.identity` 解析。」
  + `_ss_root = ...parents[2]/"state-scanner"` + `sys.path.insert` + `from lib.identity import get_identity`;
  同文件 `:48-51` 另有一处 (`.../state-scanner/scripts` + `from collectors.multi_remote import ...`)。
  ⇒ **「插入兄弟 skill 的 root 再 import 其 lib」在本仓是已在生产运行的模式。**
- ⇒ 真实缺陷是「**没给 import 代码**」而非「不可行」。两份子 Spec 已各补一段逐字 import 骨架 +
  「`audit-engine` 内不得新建 `lib/`/`collectors/` 顶层目录」的 A.2 约束 (同名包冲突, `coordination_probe.py:80-83` 点名过)。

## S-2 (Major, 探针 Spec) — Rule #6 处置未承诺使用 `/skill-creator`

CLAUDE.md 不可协商规则 #6 逐字「**Skill 基准测试必须用 `/skill-creator`**(自研 runner 已废弃)」;
探针 Spec 的 rule6_note 计划「格式照既有套件…流程照 `AB_TEST_OPERATIONS.md` §场景 2」, **全篇无 `/skill-creator`**,
且其「新表面」#4 自陈「未审: 建套件本身是否需要单独走 `/skill-creator`」。
⇒ 手工仿写 JSON **不等于**跑 `/skill-creator`, 这不是「未审」而是与规则 #6 字面直接冲突的**未闭合项**。

**主控复核**: 成立。已在 rule6_note 落「**必须经 `/skill-creator` 产出**, 手工仿写不满足规则 #6」。

## S-3 (minor, 探针 Spec) — 同文档 `ab-suite/*.json` 计数自相矛盾 (30 vs 31)

rule6_note 表写「目录 30 个 `.json`」, 「新表面」#4 写「从实测的 31 增到 32」。实测 **31**。
**主控复核**: 成立, 已订正为 31 并加注。

## F-1 (Major, 字段 Spec) — 同 S-1 的消费方视角

字段 Spec 承诺导出纯函数**明确目的是让另一个 skill import**, 却未给跨 skill 消费方的 import 方式;
与探针 Spec 各自默认「对方已解决」。**主控复核**: 成立, 已在字段 Spec 同批补同一段 import 骨架 (消费方视角)。

## 必答 5 题 (摘要)

1. **落点完整性**: 绝大多数精确到文件+行号+参数名; 两处缺签名 (C-2, 已补); `--heartbeat-only` 落点刻意留活口给 A.2 (非缺陷)。
2. **是否要求改不存在的东西**: 除 C-1 外**本轮无第二处**; `release_claim_by_track`/`heartbeat`/`_main`/`_gated`/`run_gate`/`_run_gate_impl`/`coordination_probe.py` 逐条实读均存在且行号精确匹配。
3. **跨 Spec 依赖闭合**: 签名/返回契约一致; 探针取 `text` 的代码路径**两份 Spec 都没明写** (`git show <ref>:<path>` / `git cat-file`); 跨 skill import 见 S-1。
4. **可行 ship 顺序**: field-availability → sibling-spec-probe → 母 (或母与 field 并行, probe 殿后)。两处摩擦: ① 母与 field **都改 `spec-drafter/SKILL.md` 的不同 hunk** 且各自 rule6_note 都要求照跑 `ab-suite/spec-drafter.json` —— 不同批合并时后者的 AB 基线已被前者改过, 两份文档都未言明; ② probe 若先 ship, 其「姊妹未 ship 时退化」**没有给出 import 失败的兜底代码** (对照字段 Spec 有明确的 `try/except ImportError: print("##SKIP##")`)。
5. **Rule #6 论证**: **结构成立** (判据表第三行三件套逐条落实 + Phase B.1 前置断言未自判豁免, 符合 Rule #10), **但落地手段有缺口** (S-2)。

## 抽样核验 (约 35 处 `文件:行号`, **全部命中, 无一处漂移**)

`collision.py:178/230-234/268/278-279` · `claim_lifecycle.py:228/274/377/425/427/430` ·
`phase1_gate.py:335/989/1032/1173/1191/1230/1233-1235/1236-1238` · `identity.py:191/222/242/244` ·
`track_id.py:61`(确认 `derive_track_id` **不含**拼接) · `constants.py:36/40-44/50/51` ·
`claim_schema.py:130` · `coordination_ref.py:119/596` · `gc.py:338` · `release_gate.py:225/236-237` ·
`phase-a-planner:9` / `spec-drafter:9-10` · `phase-b-developer:86-93`(YAML 键非标题) · `branch-manager:146` ·
`phase-d-closer:42/50-56`(`:56` 确实误写 STALE_TTL) · `session-handoff.md:217/238` ·
`DEFAULTS.json` **无** `coordination` 键 · `multi_remote.py:255-286` · `state-scanner/SKILL.md:149/176` ·
`execution-modes.md:84/89/113/118` · `report-format.md:50-67` · `run_all_tests.sh:48/50/71` ·
`coordination_probe.py:80-90` · `fetch_gate.py:111-112` · ab-suite eval 计数 (phase-a-planner=2/spec-drafter=2/state-scanner=12) ·
`audit-engine/` 确认仅 8 文件**无 scripts/tests** · `ab-suite/audit-engine.json` **确认不存在**
