---
track-id: aria-2-0-m5-replay-reconciler-drift-review-loop-audit
owner-container: simonfish/dev-claude
phase: C
status: active
updated-at: 2026-05-22T13:25:00Z
---

# Aria — Session Handoff (2026-05-22 ~13:25 UTC) — M5 Phase C: O1 ✅ + O2 ✅

> **Status**: M5 Phase C 推进 —— O1 (Feishu secret 轮换) + O2 (Layer 2 aria-runner 镜像 build + 注册) 完成。**O3 (Tier-1 live LLM real smoke) + Phase D.2 close 待续** (owner 选 O3 单独 session)。
> **Predecessor (same track)**: [`2026-05-21-m5-phase-b-stabilization-hermes-luxeno.md`](2026-05-21-m5-phase-b-stabilization-hermes-luxeno.md)
> **本 session 性质**: 用户驱动 one-by-one 推进 M5 Phase C O1+O2 (本 session 前半段另完成独立 track aria-plugin #50,见 §0)

---

## §0 入口 (新 session 优先读)

读取顺序:
1. **本 doc** — M5 Phase C O1+O2 done
2. **`2026-05-22-m5-phase-c-playbook.md`** — Phase C 完整 step-by-step (§执行记录 含 O1/O2 成果 + O3 grounding 契约)
3. Predecessor: `2026-05-21-m5-phase-b-stabilization-hermes-luxeno.md`

→ **next**: O3 单独 session (见 §6) | Phase D.2 在 O3 后

> ⚠️ **另一独立 track 已 DONE**: 本 session 前半段完成 aria-plugin #50 full A→D cycle (state-scanner `_status` 提取范围修复, v1.23.1),见 [`2026-05-22-aria-plugin-50-status-extraction-range-shipped.md`](2026-05-22-aria-plugin-50-status-extraction-range-shipped.md)。与 M5 正交,已闭环。

---

## §1 已完成 (本 session M5 部分, 2026-05-22)

### O1 — FEISHU secret 轮换 ✅

- 飞书后台**保留 app** (`cli_a95f50f09f7adcb5`) 仅重置 3 key (App Secret + Verification Token + Encrypt Key) —— 偏离 decision §2.5 原文"删 app 重建" (APP_ID 不变免重配 callback,安全目标等效)
- `/root/.hermes/.env` 3 key 更新 (getpass 静默) → `nomad job restart aria-orchestrator` → 验证 Hermes `✓ feishu connected` (WS 干净重连,新 App Secret 有效)
- decision `2026-05-02-secret-rotation-deferred.md` → **Resolved 2026-05-22**;原 4-key deferral set 整体 CLOSED (3 FEISHU 轮换 + GLM_API_KEY 经 Luxeno 重定向架构性退役);2026-08-02 hard cap reminder 可撤销

### O2 — Layer 2 aria-runner 镜像 ✅ (6 步)

- bot PAT 加 `read:repository` scope → aria-build 容器 clone 打通
- 镜像 `forgejo.10cg.pub/10cg/aria-runner:claude-m5-91b8975-v11` (+`claude-latest`) 构建+推送
  - **digest `sha256:5b80ca6cd04ab31b3d8165eb82f4ac9edd824b45e8181adf9325e80cf35148f5`**
  - 烤入 aria-plugin v1.23.1 (8253b6e) + Layer 2 changes/redo (Spec X+Y)
- `m1-handoff.yaml` image_refs 更新到新镜像
- `nomad/jobs/aria-layer2-runner` var 填全 8 key (5 配置 + 3 密钥;`ANTHROPIC_BASE_URL=https://api.luxeno.ai` 实测核实)
- `aria-layer2-runner.hcl` image ref `10CG`→`10cg` 修正 → `nomad job run` **注册成功** (parameterized batch job, running)

### O3 — grounding ✅ (未执行)

读 entrypoint.sh + modes/initial.sh,dispatch 契约写进 playbook §O3。**未执行** —— 见 §2。

---

## §2 未完成 / Carry-forward

### O3 — Tier-1 live LLM real smoke (单独 session)

会真实花钱 (~¥0.10) + 创建真实 PR 的 live autonomous dispatch。4 个前置 (详见 `2026-05-22-m5-phase-c-playbook.md` §O3):

| # | 前置 | 状态 |
|---|------|------|
| O3-a | `aria-runner-inputs`/`-outputs` host volume 在 heavy 节点配置 | ⏳ 未核实 — `nomad volume status -type host` 未见,需重新确认/配置 |
| O3-b | `issue.yaml` 起草 + 放 inputs 卷 | AI 可做 (schema 见 modes/initial.sh Step 2) |
| O3-c | test repo + trivial throwaway issue | **owner 决策** — runner 会真建分支/开 PR,需 sandbox |
| O3-d | 接受成本 + 真实 PR artifact | owner 确认 |

### Phase D.2 — close (O3 后)

勾 M5 Spec tasks.md 6.21.1/6.27-6.30 + `m5-handoff.yaml` go_decision final Go + 归档 M5 proposal + US-025 → done。

### S6 hygiene (时间敏感)

- `/root/.hermes/.env.bak-feishu-rotate-*` (O1 留的) — O1 稳定 ≥24h 后 (~2026-05-23) shred
- 旧 3 个 `.env.bak-*` (Hermes→Luxeno 那次) — 24h 窗口已过,**现可 shred** (`ls /root/.hermes/.env.bak-*` 看清日期勿误删 O1 那个)

---

## §3 关键风险 / 已知陷阱 (本 session M5 部分新增)

- **R1 — `git config insteadOf` 多值需 `--add`**: 同一 url base 设 2 个 insteadOf,第 2 个 `git config`(无 `--add`)覆盖第 1 个。改用 `git -c "url.X.insteadOf=Y"` 单命令传 (会传播到 `--recurse-submodules` 子模块 clone),不写 gitconfig 更干净。
- **R2 — docker 镜像路径必须小写**: `forgejo.10cg.pub/10CG/aria-runner` 的 `10CG` 大写 → docker build/pull 报 "repository name must be lowercase"。全链路用 `10cg`。`aria-layer2-runner.hcl` image ref 已同步修正。
- **R3 — `.gitmodules` ssh URL + 无 SSH key 容器**: aria-build 容器无 SSH key,`.gitmodules` 用 `ssh://` → `--recurse-submodules` "Host key verification failed"。`-c url.insteadOf` 把 ssh 重写为 https-带-PAT 解决。
- **R4 — forgejo.10cg.pub 集群内自签证书**: 容器内 git 需 `-c http.sslVerify=false`。
- **R5 — mawk 不支持 `{n}` 区间量词**: light-1 的 awk 是 mawk,`/^[0-9a-f]{8}/` 静默不匹配 → 变量空。用 grep ERE 或硬编码。

---

## §4 实战教训

本 session M5 教训固化于 §3 (R1-R5) + playbook §执行记录"踩坑记录"。**未新增 memory 文件** —— MEMORY.md 已超 size limit (41.4KB/24.4KB);建议未来 session 先瘦身再补。

---

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| **UPM** | N/A — Aria 主仓不使用 UPM |
| **User Story** | US-025 `in_progress` — 正确 (Phase C O3 + D.2 未完) |
| **OpenSpec** | M5 Spec `approved` 不变 (Phase C/D 未完不归档);closeout Q3 audit 把 tasks.md `6.21.1` 标 `[~]` partial + O2 Layer 2 image 成果注记 (commit `6cf98b4`),消除轻微 spec↔reality drift。其余 `[ ]`/`[~]` (6.19/6.26/6.27-6.30) 留 Phase D.2 sweep |
| **PRD / Architecture** | 不变 |
| **Auto-memory** | 未新增 (MEMORY.md 超限) |
| **Decision memos** | `2026-05-02-secret-rotation-deferred.md` → Resolved;`2026-05-20-secret-rotation-during-m5-deploy.md` §3.3 → ✅ 注记 |
| **Production** | aria-orchestrator alloc d43c2a7e healthy (Hermes Restarts 6, Feishu 新 key);`aria-layer2-runner` 注册 (parameterized, 待 dispatch);新镜像在 registry |
| **Multi-remote parity** | 主仓 `bfd01f6` + aria-orchestrator `ebd5bdd`:origin == github 全程 verified |

---

## §6 Next session 入口 + 优先级

```bash
/aria:state-scanner   # 多 track 看板 surface 本 handoff
```

**优先级 ⭐ O3 (单独 session)** —— 起点:
1. O3-a:`nomad volume status -type host` 核实 `aria-runner-inputs`/`-outputs`;缺则配 (heavy 节点 client config host volume)
2. O3-c:owner 定 test repo + trivial issue
3. O3-b:author `issue.yaml` → 放 `/opt/aria-inputs/${ISSUE_ID}/issue.yaml`
4. dispatch (契约见 playbook §O3) → 观测 → 验证 issue→PR 闭环
5. O3 通过 → Phase D.2 close US-025

**不应该做的**:
- ❌ 不要在没有 test 目标 + host volume 未核实的情况下 dispatch
- ❌ 不要 shred O1 的 `.env.bak-feishu-rotate-*` 直到 O1 稳定 ≥24h

---

## §7 提交清单

**本 session M5 commits** (主仓 origin+github 双推,全程 parity verified):
- `558b5f8` docs(decision): O1 FEISHU secret 轮换完成 + M5 Phase C playbook
- `2296675` docs(handoff): playbook §4 #2/#3/#4 SSH-verified
- `9b38a95` chore(submodule): bump aria-orchestrator → 9cfbce8 (O2 image refs)
- `8668cac` chore(submodule): bump aria-orchestrator → ebd5bdd (HCL lowercase)
- `3ea20f7` docs(handoff): playbook O1+O2 执行记录
- `bfd01f6` docs(handoff): playbook O3 grounding
- (本 commit) docs(closeout): M5 Phase C O1+O2 handoff

**aria-orchestrator commits**: `9cfbce8` (m1-handoff image_refs) + `ebd5bdd` (aria-layer2-runner.hcl lowercase)。

**无 regression**: 0 prod 破坏;Hermes + Layer 1 健康;`aria-layer2-runner` 注册就绪。

---

## §8 Memory entries this session

无新增 memory 文件 (MEMORY.md 超 size limit)。M5 教训见 §3 + playbook。

**Q-audit (收尾)**:
- Q1 未完成 task? O3 + Phase D.2 全 documented (§2) + gated;O3 4 前置明列。无遗漏。
- Q2 未固化经验? §3 R1-R5 已记;MEMORY.md 超限故未开新文件。
- Q3 UPM/US/Spec/PRD? 见 §5 — US-025 正确不变,Spec 不归档 (Phase C/D 未完)。
- Q4 收尾交接? 本 doc + latest.md 更新。

---

## Cross-references

- **Phase C playbook (执行细节)**: [`2026-05-22-m5-phase-c-playbook.md`](2026-05-22-m5-phase-c-playbook.md)
- **Predecessor (same track)**: [`2026-05-21-m5-phase-b-stabilization-hermes-luxeno.md`](2026-05-21-m5-phase-b-stabilization-hermes-luxeno.md)
- **独立 track (本 session 另完成)**: [`2026-05-22-aria-plugin-50-status-extraction-range-shipped.md`](2026-05-22-aria-plugin-50-status-extraction-range-shipped.md)
- **Decision**: `.aria/decisions/2026-05-02-secret-rotation-deferred.md` (Resolved) + `2026-05-20-secret-rotation-during-m5-deploy.md`

---

**Created**: 2026-05-22 ~13:25 UTC
**Author**: solo-lab (uni.concept.wzfq@gmail.com), drafted by Claude Opus 4.7 (1M context)
**Status**: M5 Phase C O1+O2 done;O3 (live LLM smoke) + Phase D.2 待单独 session。
**Next entry**: O3 — 起点 O3-a host volume 核实 + O3-c owner 定 test 目标。
