---
track-id: secret-guard-manifest-precision
owner-container: simonfish/bfe8285d
phase: D
status: done
updated-at: 2026-08-22T15:50:48Z
---

# Aria — Session Handoff (2026-08-22) — Aria#179 secret-guard 漏报+误报双修 **ship v1.66.4 + Phase D 归档**

> **一句话**: 一个 session 把 #179 从 triage 走完十步循环: A.1 spec (post_spec 2 轮收敛) → A.2/A.3 (post_planning 1 轮+确认) → B (TDD 红绿链 14 commit, 对抗 review 抓出自洽假绿 1 处回归) → C (gate green, **aria-plugin v1.66.4** 三仓双推) → D (归档 + tracker #187)。同 session 顺手: 归档两个 superseded/僵尸 spec (#147 轨、ci-path-coverage)、裁 a1-entry C1/C2、核实 NEXUS token 08-09 已轮换。**track 终结。**

## §0 入口 (新 session 优先读)

- **#179 全闭环**: aria `9e6a17c` (v1.66.4) / standards `334c609` / 主仓 `c469eea`+后续; #179 closed; claim released; spec 归档 `openspec/archive/2026-08-22-secret-guard-manifest-precision/`; tracker #187 (零残留, 已关)。
- **plugin cache 本机已是 1.66.4**, 活体 harness 已验证新行为 (TASK-015 PASS)。
- carry-forward 见 §2 —— 全是 **owner 复议/知悉项**, 无未完成机械步骤。

## §1 已完成 (按顺序)

1. **卫生**: #185 收尾关闭; 僵尸 spec `phase-c-integrator-ci-path-coverage` 归档 design-only (tracker #186 建即关); R2 聚合报告补机读 `verdict`。
2. **a1-entry-claim C1/C2 裁定回填** (C1=(a) 扩 allowed-tools / C2=(ii)+(iii) heartbeat 挂扫描入口 + TTL 24h 量级); spec 转待 rework 进 A.2; 关联 #180。
3. **#179 triage** (confirmed/major, 4/4 @1.66.3, 活体二次复现误报) + phase1_gate 认领 (无重叠)。
4. **A.1 spec v1→v3.1**: 双平面缺口 (Bash :709 无 jq / Read :546 无 claude 条目) + What.1b credit 收紧 + What.3 前置白名单; post_spec R1 3×REVISE (3C: credit 逃逸 / bash ERE 整串匹配 / 轮换引证张冠李戴) → R2 → 3/3 PASS。
5. **A.2/A.3**: detailed-tasks.yaml 17 任务/44h (TDD 配对, TASK-000 owner 门); post_planning P1 PASS / P2 3M / P3 1M → v2 → 3/3 PASS。
6. **Phase B** (aria `feature/secret-guard-manifest-precision`):
   - TASK-001/005 RED 8/9 → TASK-002 (claude-config 行 + jq + :785/786 源组, `$_SG_CLAUDE_CFG` 单一定义) / TASK-006 (:546) → GREEN
   - TASK-007 枚举 → **Amendment-1**: 白名单按全名型/后缀型两族 (字面套后缀型会放走 `prod.env`), 适用集收窄为 14 行
   - TASK-008 守卫 8 GREEN / TASK-009 SC-4 6 RED (两条反事实失败的恒绿形态当场替换) → TASK-003 SC-3 4 RED → TASK-004 (tight 模式, 7 条 credit 分支 gated) / TASK-010 (14 行改写, `([^|]*PP)?` 可选组解单空格争用) → 子集 32/32
   - TASK-011 全量: 首跑 588/590 (SC-19 family 60→61 合法 + SC-8 tier e +58% 负载噪声) → 修 → 599/599
   - TASK-012 文档 (knowledge-manager 换人执笔): hook 头注释 History + 已知限三类; secret-hygiene.md 计数 558→599
   - **对抗 code review**: 首审 REVISE 1C/3I/4m — **C-1 真回归**: `/`-根名 (`/.aws/credentials` 等) 套白名单后 `cat ${HOME}/.aws/credentials` 从拦变放, 591 全绿是假绿 (守卫全是 basename 形态) → **Amendment-2** (拆 `/`-根名分支 / 删 `~` / 名组容忍 `./` `//`) + 7 条守卫先 RED 后 GREEN → 复核 PASS_WITH_WARNINGS
7. **Phase C**: C.2.4 gate green (path coverage not_applicable — hooks/ 无 CI workflow; main in-flight 清; 本地 aria master 陈旧曾误判 covered, 对齐 origin 后正确); bump 1.66.4 (5 SOT + CHANGELOG); ff 合并 + 三仓双推 ls-remote MATCH; 主仓 14 点同步 0 残留; gitlink 6/6 ok。
8. **TASK-0 (泄露凭据) 核实**: 泄露键 = `NEXUS_API_TOKEN` (Nexusm 记忆服务, 非 #283 所称 devpi 镜像); 租户 API key 清单仅存 `10cg-prod-dogfood-r20260809` (08-09 16:25 创建) ⇒ **当日已轮换**, 缺的只是记录。#179/#283 已评论。
9. **Phase D**: 归档 (verdict=warn, ack 人工核验) + tracker #187 + D.2b + 本 handoff + D.4。

## §2 Carry-forward (全部 owner 复议/知悉, 无机械待办)

- 🟡 **SC-8 性能档数据请复议**: tier (e) min 增幅五次 = +58% (load≈12) / +6.8% / +83% (reviewer 复审, load 15-22) / +0.8% / +9.2%; a-d 档全部 -47%..-83%。两次超标均在 load ≥15 时段; 进程级三点复测 +4%。按 Rule #10 不自判噪声, 最近三跑全过 (gate 绿), 数据原样呈报。
- 🟡 **Amendment-1/2 范围修正请复议** (spec 文末): 白名单两族 + 适用集从「全部路径清单型」收窄为枚举 14 行; `/`-根名不套白名单。未动的行 (find/xargs 组合、重定向、ssh/kubectl 远程、token 起始行) 若要覆盖需逐行评估合法前缀词汇。
- 🟡 **行为变化知悉**: 全名型前为词字符的形态 (`cat x.profile`) 从拦变放 — Amendment-1 设计本意 (`x.bashrc` 不是该文件)。
- 🟡 **review 建议立案 (挂 #138)**: 两条预先存在的 credit 位置无关弱点 (`| tee /dev/stderr | jq keys`、jq 错误信息回显输入值); `node -p` 未覆盖 (同构既有限)。未立案, owner 定。
- 🟡 **a1-entry-claim** 待 rework 落版 (C1/C2 已裁); 前置 `linked-issue-normalization` 三轮未收敛待 owner 方向裁定 (补证据层 R4′ 还是 override)。
- 🟡 Aether#283: NEXUS 项可结 (已评论); FORGEJO_TOKEN / CF_ACCESS_CLIENT_SECRET 两项状态未核。

## §3 关键决策 / 教训 (memory 候选)

- **自写 fixture + 自写实现 = 自洽假绿** (本 cycle 实证): 守卫集只含"看起来像真路径"的 basename 样本, 漏掉 `/`-根名族 → 591 全绿下藏真回归。**守卫集必须按敏感名形态族穷举** (basename 型 / `/`-根型 / 后缀型), 对抗 review 自造探针是唯一抓手。
- **spec 层白名单对后缀型名的盲点只在实现期可见** (Amendment-1): 设计阶段两轮审计 (6 席) 都没抓到 `prod.env` 会被放走 — 审计看的是 FP 方向, 没人反向问"合法前缀词汇是什么"。
- **secret-guard ack 规则**: reason 首 token 须 ≥8 非空白字符 (`reading` 7 字符恒失效, 用 `inspecting`)。
- **bash ERE 可选组技巧**: `READER[[:space:]]+([^|]*PP)?(NAMES)` 让单空格裸名靠必选空白匹配、其余前缀受白名单约束 — 解 `[[:space:]]+` 与前置类争用。
- **共享机性能判据**: min-based 在 load ≥15 时仍会超标 (两次 +58/+83%), 不只是 median 问题; 单跑 + 记录 load 是底线。
- **index.lock 间歇** (harness 后台 `git status --porcelain`): 本 session 主仓/子模块各撞一次, 清锁重试即可。
- **子模块 detached HEAD 推送**: `push origin master` 推的是陈旧本地分支 → 用 `HEAD:master` 或先 `branch -f master origin/master` (C.2.4 gate 也因本地 master 陈旧误判 covered)。

## §6 Next session 入口

`/aria:state-scanner`。本轨终结, 无本轨后续。候选: a1-entry rework (需先裁 linked-issue-normalization 方向) / #182 handoff status 收口 / #184 / 并发轨 #152 (post_spec R7 已批进 A.2, 另一容器在跑)。

## §7 提交清单

```
aria    master 9e6a17c (v1.66.4): feature 13 commit ff + bump; 双远程 MATCH
standards master 334c609: 计数 599 + Claude 配置行; 双远程 MATCH
主仓    c469eea ship + 3ea44dc 17/17 + 本 handoff commit; 双远程 MATCH; gitlink 6/6 ok
Forgejo: #179 closed · #185 closed · #186/#187 tracker 建即关 · #283 评论 · a1-entry 裁定回填
coordination ref: claim secret-guard-manifest-precision released (done)
```

## §8 Memory entries (本 session 新增候选)

- `feedback_guard_fixture_set_must_enumerate_name_shape_families` — 守卫 fixture 按敏感名形态族穷举, 否则自写测试+实现假绿 (本 cycle C-1)。
- `feedback_secret_guard_ack_reason_first_token_8_chars` — ack 首 token ≥8 非空白字符。

## Cross-references

- spec 归档: `openspec/archive/2026-08-22-secret-guard-manifest-precision/` (proposal v3.1 + Amendment-1/2, detailed-tasks v2 17/17)
- 审计: `.aria/audit-reports/post_spec-R{1,2}-1787375602111-*` / `post_planning-R1-1787379624181-*` / `phase-b-review-179-*`
- 语料: `.aria/notes/secret-guard-179-pattern-rows.md`
- 前序: [2026-08-18 #128 Phase D](./2026-08-18-issue128-phase-d-archive-and-sc9b-close.md) · 并发轨 [2026-08-22 会话收尾 (023236f2)](./2026-08-22-session-close-credential-defense-and-mirror-collisions.md)
