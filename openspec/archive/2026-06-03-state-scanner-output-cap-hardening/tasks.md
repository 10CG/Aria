# Tasks — state-scanner-output-cap-hardening

> Level 2 | Target: aria-plugin v1.38.0 + 主仓 gitlink bump
> Phase A 起草 2026-06-01; Rev1 post_spec R1 修正。
> Phase B+ 在 aria submodule 分支 `feature/state-scanner-output-cap-hardening` 实施。

## TG-A (#72) — 补每区块字段骨架 + 防再漂移

- [ ] TG-A.0 (R1 C2) reconcile canonical 区块集: 对齐 `output-formats.md` 标准场景 (用 📝README同步 + 🔗Forgejo配置) 与 `SKILL.md:146` (用 🔄同步状态), 锁定**确切区块数与名** (10 或 collapse 后更少)。这是 TG-A.1 的前置。
- [ ] TG-A.1 把 `SKILL.md:146` 区块**名清单**扩成**带每区块关键字段示例的精简骨架** (~20-30 行)。降级原则已在 L146, 保留。不恢复全部 90 行。
- [ ] TG-A.2 保留指向 `references/output-formats.md` 链接。
- [ ] TG-A.3 (R1 I-1 / Finding 1) **自动 sync-check 测试** (非仅 dogfood): 解析 `SKILL.md` 骨架 + `output-formats.md`, 断言 canonical 区块 header 两边一致出现 → 防 progressive-disclosure 再次漂移 (根因复发防护)。
- [ ] TG-A.4 dogfood: 跑 `/state-scanner` 人工核 canonical 区块齐全 (确切数, 非"9")、顺序对、空状态降级生效。

## TG-B (#71) — MAX_BRANCHES_SCANNED 三层可配置

- [ ] TG-B.1 `_common.py` 加 `resolve_max_branches_scanned(project_root) -> int` (R1 M-4 定址), 结构镜像 `resolve_forgejo_hosts` 但显式处理 int 域 (R1 I-1/I-2):
  - env `ARIA_HANDOFF_MAX_BRANCHES`: `int(raw.strip())` 包 `except (ValueError, TypeError)` → None 回退。
  - config `state_scanner.handoff_multibranch.max_branches`: `isinstance(v,int) and not isinstance(v,bool)` (拒 bool); 复用 `(OSError, JSONDecodeError)` 守卫。
  - 每层独立 `≤0 → None 回退`; default 20。
  - 上界 (如 500): 超界 `log.warning` (clamp vs warn-only 见 OQ3)。
- [ ] TG-B.2 `handoff_multibranch.py` 改读 resolver: 替换 L302/305/306/311 消费点; cap 文案动态用 resolved 值; 更新 docstring L51 + 注释 L127/L159 (Rule #3)。
- [ ] TG-B.3 `.aria/config.template.json` 文档化 `state_scanner.handoff_multibranch.max_branches`。
- [ ] TG-B.4 (R1 Finding 2) resolver 单测, 镜像 forgejo-hosts **30** 测 (proposal 初稿误作 27), 必含: env 覆盖 / config 覆盖 / default 回退 / env="0" / env 负数 / env 非数字 / env 空串 / env 前后空白 / env-beats-config E2E / 整个 config 文件 malformed JSON / config 非整数值 / config float 值 / config bool 值 (拒) / 边界 (=cap / >cap) / 上界超限。
- [ ] TG-B.5 (R1 M-3) cap-application 路径测试: `monkeypatch` `_list_origin_branches` (或 `_run`) 返回合成 21 元素 list, 断言 (a) `soft_error("handoff_multibranch_branch_cap")` 触发 (b) `branches_scanned` 反映 resolved cap (c) env/config 覆盖时用 override 值非硬编码 20。
- [ ] TG-B.6 回归: `scan.py` 全量 collector 测试 0 regression (本仓 origin 3 分支 → 不触发 cap)。

## Phase C/D (ship — owner-gated, 本 session 不做)

- [ ] C.1 5+1 SOT bump v1.37.0 → v1.38.0
- [ ] C.2 aria-plugin PR + pre-merge gate + merge + 双远程 push
- [ ] C.3 主仓 gitlink bump + CLAUDE.md 项目状态同步
- [ ] D.1 关 #71 + #72 (POST comment + PATCH state, 不改 body per [[feedback_issue_close_comment_not_body_patch]])
- [ ] D.2 归档本 Spec

## Rule #6 benchmark substitute (deterministic/structural skill)

- TG-B: resolver 单测 (env/config/default/int 域 fail-soft/边界/上界) + cap-application monkeypatch 测 = structural substitute
- TG-A: **自动 sync-check 测试** (SKILL.md ↔ output-formats.md 区块一致) + dogfood = structural substitute
- 关键: sync-check 把"格式完整性"变成确定性断言, 补上 v1.32.0 AB 漏测的维度根因
