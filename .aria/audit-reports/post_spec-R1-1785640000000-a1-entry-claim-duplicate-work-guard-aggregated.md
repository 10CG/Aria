---
checkpoint: post_spec
round: 1
converged: false
overridden_by_user: false
incomplete: false
---

# post_spec R1 — a1-entry-claim-duplicate-work-guard

> **席位**: 5/5 (config `teams.post_spec` 全员) · **verdict 分布: 5/5 REVISE** · `scope_ok` 5/5 true
> **counts (各席)**: TL 2C/6M/3m · BA 2C/3M/1m · QA 4C/3M/2m · CR 3C/7M/3m · KM 0C/2M/2m
> **timestamp**: 1785640000000 · 审计对象: 主仓 `09c8e56` + 未提交的 08-02 §Why 增补

## 判定

**REVISE, 未收敛。** 去重后 **4 个 critical 簇**, 其中**两条足以让整个方案静默失效** —— 且两条都由 ≥2 席独立命中并经主控实跑复验。

**最刺眼的事实**: 本 Spec 要防「机制存在但没接对地方」, 而它自己提议的主机制**在生产数据上当场就是失效的**。

---

## Critical 簇 (去重后 4 条)

### C1 — `linked_issue` 无归一, 生产数据两种格式并存 ⇒ 主机制静默失效
**4 席独立命中** (TL / BA / QA / CR) + **主控实跑复验**

- **位置**: proposal §1 (模板用 `<repo>#<n>`) vs `aria/skills/state-scanner/lib/collision.py:217`
- **问题**: `linked_issue_overlaps` 的匹配是**裸字符串 `!=`**(`:217` `if c.linked_issue != own_linked_issue: continue`), 无任何归一。而生产 ref `refs/aria/coordination` 里**两种格式并存**:

  | 格式 | 条数 | 实例 |
  |---|---|---|
  | org 限定 | **9** | `10CG/aria-plugin#110` `10CG/aria-plugin#113` `10CG/Aria#165` `10CG/Aria#147` |
  | 裸形 | **4** | `aria-plugin#124` `aria-plugin#122` `aria-plugin#118` |

- **后果**: 轨 A 认领 `10CG/aria-plugin#122`、轨 B 认领 `aria-plugin#122` ⇒ **`linked_issue_overlap` 恒 `[]`** ⇒ 与「真没人在做」**不可区分**。这正是本 Spec 要根治的漏报, 原样复现在它自己的机制里。
- **加重情节 (主控自认)**: 本 Spec §Why 引以为据的 08-02 dogfood 用的是**裸形** `aria-plugin#124`, 而历史记录多为 org 限定形 —— **起草者本人在给格式分裂添砖**, 且 §Why 把返回的 `linked_issue_overlap=[]` 当成佐证 (CR/m3: 空集在无竞品时**恒空**, 与格式失配的返回值不可区分, 该佐证零信息)。
- **CLI help 自相矛盾** (TL): `phase1_gate` 的 help 示例用 `10CG/Aria#160`, 而 Spec §1 模板用 `<repo>#<n>` —— 两处**直接互斥**。
- **修法方向** (与危害「格式失配致漏报」一致): 在 `linked_issue_overlaps` 入口做归一 (统一补全 org 前缀或统一剥离), 并**同时归一存量 ref 数据**; Spec §1 模板与 CLI help 二者对齐到同一形态; 加 SC: 两种格式的 claim 必须互相看见。

### C2 — 两机制对「竞品已完工并归档」结构性失明 —— 即第 5 次事故的真实形态
**2 席独立命中** (TL / BA) + **主控实跑复验**

- **位置**: proposal §2 (glob `openspec/changes/*/proposal.md`) + §1 (主机制) vs `collision.py:210,213`
- **问题**: 两条腿同时够不到已归档的竞品:
  - **副机制**: glob 写死 `openspec/changes/*/`, 而 `openspec/archive/` 与之**同级**。实跑: 该 glob 对 path-coverage 只命中 `openspec/changes/phase-c-integrator-ci-path-coverage/`(**作者自己那份**), 真竞品 `openspec/archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/` **零命中**;
  - **主机制**: `_TERMINAL = ("done", "abandoned", "unknown")` 在 `:213` 被**直接 skip** ⇒ 对方 ship 完把 claim 置 done 后, overlap 恒空。
- **后果**: **第 5 次事故(即催生本 Spec 的那一次)的最终形态 —— 「对方已 ship 并归档」—— 两条腿都看不见。** 机制对自己的 motivating case 失明。
- **修法方向**: 副机制 glob 扩到 `openspec/{changes,archive}/*/proposal.md`; 主机制对 `done` 状态的同 issue claim **不 skip 而是降级为「已完成」提示**(与 active 竞品区分措辞, 但必须可见)。

### C3 — A.1 claim 的保护窗 (24h) 短于它要防的事故窗 (48-72h)
**TL** (含生产实例) + BA (孤儿 claim 变体)

- **问题**: A.1 claim 无 heartbeat 回路, `SWEEP_TTL=24h` 后被跨容器 sweep 成 `abandoned` ⇒ 再被 `_TERMINAL` skip。而本 Spec 自述的事故窗是 **07-25 起草 → 07-27 发现 (48h+)**、第 5 次是 **07-30 → 08-02 (72h)**。⇒ **保护窗比事故窗短**, 机制在最需要它的时刻已经过期。TL 报告本仓 ref 里已有一条 `phase: A.1` 被 sweep 的生产实例。
- **与 §3 的矛盾**: §3 把残余缺口写成「秒级」, 而真实缺口是 **24h 之后全裸**。
- **修法方向**: A.1 claim 需 heartbeat 或延长 TTL 至覆盖典型 Phase A 时长; §3 的残余缺口措辞按实际重写(CR/M6 另指出「秒级」还低估了跳 A.1 / 直调 spec-drafter / opt-out / legacy 轨四条路径)。

### C4 — 主机制的义务无可执行验证面, 且 Rule #6 分类误判
**QA 4C 中的 3 条 + TL/M5 + CR/M5**

- (a) **`phase-a-planner` 目录只有 SKILL.md, 零 `scripts/` 零 `tests/`** —— 而 Impact 表声称「`skills/phase-a-planner/` 既有测试扩展 (SC-1~3)」, **该测试宿主不存在**;
- (b) **SC-3「A.1 流程断言 `--linked-issue` 在场」无拥有者** —— 无脚本 / 无 hook / 无 checker; 且 `phase1_gate` 的 `--linked-issue` 本身非 required, 而 §非目标又禁止改它 ⇒ D2「条件必需」**无机械落实物**;
- (c) **Rule #6 误判** (QA 双套件实测): Spec 写「照跑 AB, 零裁量」, 但 phase-a-planner (5 eval) 与 audit-engine (2 eval) 的现有 AB 套件**结构性覆盖不到**新增行为 ⇒ 「照跑 AB」是空头支票。按 Rule #6 判据表, 这属**第三行「处方性·套件覆盖外」**, 处置应是「点名行为 + 建可证伪定向 fixture + 套件缺口开 issue」, 而非第二行。
- **这是本 Spec 最反讽的一处**: 它引用 memory `feedback_verify_predicate_inputs_exist` 论证原建议无效, 而它自己的 SC-3 犯了同一个病 —— **判定机制要判的输入(A.1 的可执行表示)不存在**。

---

## Major 簇 (去重后 8 条)

| # | 簇 | 席位 | 要点 |
|---|---|------|------|
| M1 | 「关联 Issue」不是模板字段, 谓词输入不会被生成 | TL / CR / QA | standards 与 spec-drafter 模板**零定义**, 全语料 14/139 (10%) 有该字段, **本 Spec 自己头部就没有** ⇒ 省字段即免义务且不可观测, D2 复制了它要修的「可选=空转」 |
| M2 | claim 生命周期对偶未覆盖 A.1 新增退出路径 | TL / BA | 探索性放弃 / slug 改名致 `release_claim_by_track` 静默 `claim_not_found` ⇒ 孤儿 active claim; 全文零处提 release/sweep/D.2b |
| M3 | 与 `coordination.enabled/mode` 关系未写 | TL / KM | 两种读法各自都坏(恒红 vs 绕过 B.0 保护); `phase1_gate` 本身不读 config, skip 判断全在调用方 SKILL.md 层 ⇒ opt-out 项目在 A.1 仍被强制写 claim+push |
| M4 | 副机制只定义「检测」半, 未定义「消费」半 | QA / CR | audit-engine 命中 sibling 后做什么、是否阻断、exit code —— 全文未写 |
| M5 | 「Step 0.5」与 D3「每轮跑」互斥 | TL / CR | `audit-engine/SKILL.md:85` 明写 Step 0 是「Round 1 启动前**一次性**」; per-round 循环在 `execution-modes.md`, **不在 Impact 表**; 且 audit-engine 现无任何 fetch 能力 |
| M6 | 副机制的规模/代价未定义 | BA / CR | 「grep 全部远端 ref」的 remote 集 × ref 集范围未定; 同代码库 `handoff_multibranch.py` 已因「440 条远端分支」踩坑并做了 scan cap, Spec 未引用 |
| M7 | `fetch` 降级不进 JSON `error` 契约 | BA | 实跑复现: 首次真实调用即触发 fetch 失败而 `error: null` ⇒ SC-1/SC-2 赖以成立的「新鲜度」前提不成立 |
| M8 | `layer-l-integration.md` 同步缺口 + `--repo-path` 未钉 | KM / TL | 该活文档明确断言「闸门仅在 Phase B 触发」, 本 Spec 实施后即过时, 未入 Impact 表; `--repo-path` 未钉致两容器各按所在仓传参 ⇒ 分裂成两条 ref (auto_bootstrap 静默建 ref) |

## Minor (7 条, 详见各席报告)

§Why:74「谁都没认领过」与 ref 事实相反 —— **R 于 07-27T11:53:12Z 认领过, 且在 4 轮 post_spec 之后**(TL: 这是比原文更强的论据) · §自指注记停在 07-30 且用的正是被本 Spec 证伪的那一招, 作者 08-02 为 #124 认领却**未为本轨认领**(ref 实测零命中) · rule6_note 与 Impact 表对 `test_sibling_spec_probe.py` 覆盖范围自相矛盾 (SC-4~6 vs SC-4~7) · SC-6 缺 exit code 与阻断性契约 (SC-5 有, 形成误导性对照) · SC-6 fetch 失败构造有仓内现成先例 (`test_remote_refresh.py`) 未引用 · SC-7 缺「已归档同 issue 不应算命中」控制组 · 历史实证计数口径与 memory 原文对不齐 · **coordination ref 在 origin/github 已分叉**(github 停滞两月+, 非本 Spec 引入, 供 owner 参考)

---

## 经核实**正确**的部分 (下轮免重复)

- **D6/D7 dogfood 属实且比原文更强** (KM: claim yaml 直接给出 `phase: A.1` 字段, 坐实前提; telemetry + claim 双证)
- `--phase` 无 `choices` 约束属实 (与 `--mode` 有 choices 形成对照)
- `phase-a-planner` 零调用 phase1_gate 属实 (grep 确认)
- `phase-b-developer:88-93` 与 `branch-manager:149` **行号与内容精确匹配**
- `--linked-issue` CLI help 逐字核对通过
- 两条援引的 memory 均存在且语义匹配
- `audit-engine` 零 `scripts/` 目录属实; 新建对 `run_all_tests.sh` / 打包**无影响** (BA 已排查)
- §闸门待裁 的 Rule #10 四类白名单论证**成文正确, 无自我豁免**
- §Why 对原建议 (grep 远端 spec) 的证伪方法论正确 —— 只是没回头量自己
- D4 (盲区上正文) 的立场对

---

## 收敛提示 (供 R1-fix)

三席给出同向的结构性建议:

1. **C1 是上游** —— 格式归一不解决, C2 修了也白修 (两条腿都靠 `linked_issue` 匹配)。**R1-fix 从 C1 起手**。
2. **M1 (谓词未定义) 是 C4 与另外三条 M 的共同上游** (TL) —— 「关联 Issue」不进模板, SC-3 就永远没有输入。
3. **C3 与 M2 是同一把 24h 旋钮的相反需求** (TL), 必须一起改。
4. **两条 critical 同源** (TL): D7 只实测了「写得进推得出」, **没测「配得上活得久」**。

**AI 不预判下一轮裁决。**
