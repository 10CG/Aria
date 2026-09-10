---
track-id: archive-gate-registration-class-and-skill-drift
owner-container: simonfish/023236f2
phase: D
status: done
updated-at: 2026-09-08T15:56:29Z
---

# Aria — Session Handoff (2026-09-08) — v1.73.0 已发布; 一个 cycle 被三轮 agent team 复审拦下 6 个 Critical

> **一句话**: `archive-gate-registration-class-and-skill-drift` 从 post_planning R4 走完 **68/69** 并归档, aria-plugin **v1.73.0 已双推到两个公共 remote**, PR `10CG/Aria#209` 已合并。剩余 1 项 (`E-0`) 是等你裁的規范问题, **不阻塞已发布的东西**。
> **本 session 最该记住的一件事**: **我在同一个地方错了两次, 两次都是「维度不匹配」。** 复审席说「`git mv` 静默嵌套」, 我加了个**存在性**检查 (「`proposal.md` 在该层」); 发布前验证席实测证明它**在唯一存在理由的场景里是绿的** —— dst 已存在的现实成因只有「该 spec 已归档过一次」⇒ dst 里必然已有上次留下的 `proposal.md`。**我造的夹具是个不含 proposal.md 的空目录, 那不是现实中会发生的坏情形。** 判据换成钉嵌套确切形状的「`{name}/{name}/` 不存在」后三方向实测通过。

---

## §0 入口 (新 session 优先读)

1. **已发布**: `aria-plugin v1.73.0` (tag `fde38d0`, master `6726df1`), 主仓 master `e99f10d` —— **两端 `ls-remote` 独立核验一致, 三个 gitlink orphan-free**
2. 归档在 `openspec/archive/2026-09-08-archive-gate-registration-class-and-skill-drift/` (含 `evidence/phase-b-probe-runs.md`)
3. Tracker `10CG/Aria#210` —— 残留待办
4. 本文 §2 是唯一需要你动作的地方

---

## §1 已完成

**TG-B (18 hunk) / TG-C (3 探针 + 单测 + 夹具) / TG-D (6 单) / TG-E (发版)** 全部落地。

**三轮 agent team 复审, 共 58 条 finding 全部处置**:

| 轮 | 席位 | 结果 |
|---|---|---|
| 落地复审 | 6 席 + 反驳席 (58 agent) | 5 席 FAIL, 28 条存活 |
| 完备性批评 | `context-manager` | `safe_to_ship: false`, 10 条 (含 1C) |
| **发布前验证** | 3 席 (只审未被审计看过的 delta) | **3 席全 FAIL, 全判 `safe_to_publish: false`, 20 条 (6C/10M/4m)** |

发布前那一轮拦下的 6 个 Critical, 每一条都会真的发出去:
1. **断言 4 恒绿** (见上方「最该记住的一件事」) —— 且 **AB 的 v_new 臂逐字复述了那个假陈述**, 证明采用方的 AI 读了确实会得出错误结论
2. **`<vNEXT>` 占位符残留在要发布的 SKILL.md 里** —— E-5 的判据是「grep 旧号残留」, 对「占位符从未解析」**天然 fail-OPEN**。已新注册机械 check `no-unresolved-version-placeholder` 封死该类
3. `aria/README.md` 版本跳到 1.73.0 但发布日期还是上一版的
4. `check_bare_issue_refs.py` 非 UTF-8 清单裸崩, rc=1 与自己的 rc 契约冲突 —— **`fix-the-class` 又一次**: 上轮同款 Major 标为 fixed, 但两次改写都只加在 `scan()` 没扩散到 `load_allowlist`

**顺带挖出两个从未进过同步面的版本点**: `aria/README.zh.md` 停在 **1.41.0** (落后 26 版)、`aria/VERSION` 的裸 semver 停在 **1.47.0** —— 因为 E-5 grep 的是旧值 `1.71.1` 而它们**根本不含**那个值。同一个 fail-OPEN 形状的第二个实例。

**dogfood**: D.2 归档走的正是本 Spec 自己刚定义的流程 —— 五条断言全绿; Step 7 建的 tracker `10CG/Aria#210` 通过**本 Spec 新增的回链校验** (rc 0), 而当初立案的两个坏形态 (`10CG/Aria#185` 无 SHA / `10CG/Aria#186` 无回链行) **仍被正确拒绝**。

---

## §2 未完成 / 需要你

### 唯一未勾项 — `E-0`: `SC-11 owner 裁定`

**这不阻塞已发布的东西。** SC-11 原本混着两件事, 其中的阻塞那一半已由测量闭合:

**(1) Rule #6 完备性** ✅ **已闭合** —— 按 SOT §2 决策表第四行「拿不准 ⇒ 照跑」**无条件执行了分支 (b)**:

| 套件 | v_old SKILL.md sha256 | v_new | `--numstat` | 处置 |
|---|---|---|---|---|
| `openspec-archive` | `5593508c…` | `edba8c5e…` | 63+/34− | ✅ 已跑 |
| `phase-d-closer` | `550f33b7…` | `4b432573…` | 2+/2− | ✅ 已跑 |
| `state-scanner` | `cf5257599672ee04…` | `cf5257599672ee04…` | **0+/0−** | ⛔ 两臂**逐字节相同** ⇒ 结构上零信息 |

**(2) 規范空白** ⏳ **待裁**: SOT §1「整个变更」在跨多 Skill 时的作用域无明文 (全文 76 行实读确认: §1 那句的语境通篇是文件内部, §5 五个样例全单 Skill, §6「已知局限」讲的是别的事)。**值得写进 SOT §5, 但无论怎么裁 AB 该做的都已做完。**

### 待复议三项 (均不阻塞已发布的东西)

1. **`keep_changes_copy 声明接口移除`** —— 零代码宿主 (全仓仅 SKILL.md 出现 2 次, 零消费方/零测试/零 eval); 若行使会使同一 spec 同时存在于 `changes/` 与 `archive/` 被计成幽灵活跃变更。你若裁定保留, **一个 patch 撤回, 版本级别不变**。
2. **`plugin-cache-currency`** —— 版本 bump 后期望 **STALE 而非绿** (实测 `STALE installed=1.71.1 sot=1.73.0` rc=1)。它比的是**运行时**插件缓存与 SOT, 转绿要你在终端跑 `/plugin marketplace update` + `/plugin update` + 重启 session。**已如实登记, 未算进「全绿」。**
3. **`post_spec converged=false`** 与 post_planning `converged=false` —— 两个检查点各用满 `max_rounds=5` 仍未全票 PASS, post_planning R5 verdict = **FAIL**。按 Rule #10 我既不自行宣告收敛也不自行加开 R6。

### `D-6 定时风险`

`10CG/Aria#208` 已开并**订正过根因** (起草时的判断被实跑推翻)。⏰ 定时性在于 `aria-2.0-m6-e2e-resilience` 归档时会撞上「C 分级死码检查对带连字符的文件名符号失明」。

### `<vNEXT>`

本轮实取 **`v1.73.0`** (三腿实跑避开并发轨 `10CG/Aria#195` / `10CG/Aria#199` 正在争的 `v1.71.2` / `v1.72.0`)。**下一轮取号仍须重跑三腿** —— 那两条轨还在飞。

---

## §3 关键风险 / 已知陷阱

1. **`10CG/Aria#165` 形状本轮实测复现**: 主仓走 Forgejo 服务端合并后, GitHub 镜像**落后 29 个 commit**。已本地 FF + 补推。**这条每次都要做。**
2. **主仓本地 master 曾落后 origin/master 9 个 commit** —— E-7a 的断言当场不成立, 已按 `stale-local-main` 先 FF 再合。
3. **一次不可复现的 `FAIL: state-scanner`**: bump 后首跑 harness 报过一次, 两次独立复跑均全绿。**诊断明细被我自己 `| tail -5` 截掉了** —— harness 本会打印失败详情。跑闸门必须全量捕获输出。
4. **`aria-orchestrator` 指针全程 dirty** (他轨 `feature/m6-cost-model-telemetry`) —— 全程未卷入, 每次提交前都核过。

---

## §4 实战教训

1. **同一个地方错两次, 两次都是维度不匹配。** 别人说「多了一层」, 我查「有没有」。判据的**维度**必须匹配错误的维度 —— 而验证它的唯一办法是造一个**像真实坏情形**的夹具, 不是造一个能让断言变红的夹具。
2. **「grep 旧值」这个同步方法对「从未被解析的占位符」与「早就停在别的版本的点」双双 fail-OPEN。** 两个实例同一轮出现。已用 `no-unresolved-version-placeholder` 封死前者。
3. **我自己造过一道 SOT 不要求的闸门并据此自我阻塞了 8 小时。** R5 的 tech-lead 席指出「eval 2 无 `project_root`」——**事实是对的**, 但它推出的结论 (要 `ARIA_COORDINATION_NO_PUSH`) 不成立, 而我采纳时没验证推理链。`exact-exception-condition` 是**双向**的。
4. **每一批没被第二双眼睛看过的产物, 复审都能挖出真缺陷** —— 三轮, 58 条, 无一轮空手。而每轮的修复又会引入下一轮约 40% 的 finding。
5. **AB 跑了不等于验了**: 两个套件、四次 AB, **区分力全为零**。formal 满足 Rule #6, 实质什么也没测到。缺口见 `10CG/aria-plugin#190`。

---

## §5 提交清单

| 仓 | 最终 SHA | 推送状态 |
|---|---|---|
| `10CG/Aria` | `e99f10d` (PR `10CG/Aria#209` merged) + 归档提交 | origin ✅ / github ✅ (逐个 `ls-remote` 核验) |
| `10CG/aria-plugin` | `6726df1` + tag `v1.73.0` (`fde38d0`) | origin ✅ / github ✅ |
| `10CG/aria-standards` | 未改 | — |

---

## §6 Next session 入口

1. ⭐ **`{id: archive-gate-registration-class-and-skill-drift, desc: 已归档, 只剩 E-0 等 owner 裁 SC-11 的規范空白}`** —— 不阻塞任何东西, 裁完把结论写进 SOT §5 即可
2. 并发轨 `10CG/Aria#195` / `10CG/Aria#199` 仍在 post_spec 轮次, **与本轨共享发版面** —— 它们下次取号时 `v1.73.0` 已被占, 须重算
3. 本轮开的 8 张单: `10CG/aria-plugin#190` `10CG/aria-plugin#191` `10CG/aria-plugin#192` `10CG/aria-plugin#193` · `10CG/aria-standards#21` · `10CG/Aria#208` `10CG/Aria#210`; 另给 `10CG/aria-plugin#172` 补了一份干净的新实证
