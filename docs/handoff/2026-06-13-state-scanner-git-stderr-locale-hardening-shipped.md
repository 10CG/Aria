---
track-id: state-scanner-git-stderr-locale-hardening
owner-container: simonfishgit/dev-claude
phase: D-closed
status: done
updated-at: 2026-06-13T08:00:00Z
---

# Aria — Session Handoff (2026-06-13) — state-scanner-git-stderr-locale-hardening (#143 + #142) ship v1.46.1

> **Status**: ✅ **DONE**。Forgejo Aria #143 (F4) 完整十步循环 + #142 (F3) wont-fix 收口: state-scanner → owner 选"修 #142" → 验证 ls-remote 不可解 → owner 选 ③ 合并 #142+#143 → Level 2 Spec (post_spec R1 2/4 REVISE → R2 4/4 PASS) → 实施 → code-review PASS → **v1.46.1** (aria PR [#83](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/83) merge `2976dc3` + release `528d4af`; 主仓 gitlink 本 commit)。Spec 归档; #143 closed (fixed) + #142 closed (wont-fix)。
> **本 session 另含** (插件 reload 前): 前序 v1.46.0 (#141 cross-fetch) 已 ship + handoff `2026-06-12-...`; root README badge 根治 (`13bf409`, 加入发版清单)。
> **Rule #9 trigger**: ship v1.46.1 全 cycle + 跨 A/B/C/D + session 长。

---

## §0 入口 (新 session 优先读)

1. **本 doc** + 同周前序 (`2026-06-12-state-scanner-coordination-fetch-resilience-shipped.md` v1.46.0)。
2. ✅ **#143 fix**: `collectors/_common.py::_run` 注入 `env={**os.environ, "LC_ALL": "C"}` 强制 git 英文诊断 → 全 git-collector (coordination_fetch benign 闸 + `_classify_error` / multi_remote / issue_scan) 英文 stderr 文本匹配在任意 host locale 可靠。与 #61 `encoding="utf-8"` **正交** (LC_ALL 管诊断文本, encoding 管字节解码; commit/ref/path 字节直通 md5 一致实测)。`LANG=C` 冗余省。
3. ✅ **#142 wont-fix**: ls-remote `--exit-code` 实测 absent 与 hidden 同 rc=2 → git 协议**无法区分** (标题目标不可达)。ls-remote decline; auth-masked silent 保持 documented-limitation (#141 已缓解, Aria repo 级 ACL 不可达)。
4. **plugin cache 已刷新到 1.46.x** (本 session `/plugin` + reload; scan.py 现 15 collector 含 handoff_worktrees + coordination_fetch 双 fetch)。
5. **owner-gated 残留** (不变): block-flip / M6 Spec #2 168h / #136 Feishu / i18n #140。**AI follow-up 剩**: F1 (lib::fetch_coordination_ref benign) / F2 (耦合解耦) / F5 ([#144](https://forgejo.10cg.pub/10CG/Aria/issues/144) track_board 黄条)。**F3/F4 本 cycle 已收口** (#142/#143 closed)。

→ **next session 入口**: `/aria:state-scanner`。

---

## §1 已完成 (本 session, v1.46.0 之后)

| # | 项 | 产物 |
|---|----|------|
| 0 | root README badge 根治 | badge 1.45→1.46 + **CLAUDE.md 发版清单加 root README badge 同步项** (根因: badge 非 aria/ 子模块 SOT, 连续两 ship 滞后一版); `13bf409` |
| 1 | 3 follow-up 开 issue | F3→#142 / F4→#143 / F5→#144 (10CG/Aria, cross-ref #141) |
| 2 | #142 诊断验证 | ls-remote 实测 absent=hidden=rc=2 → 标题"区分 absent vs hidden" git 不可解 → owner 大白话理解后选 ③ 合并 #142+#143 |
| 3 | Spec + post_spec | Level 2 `state-scanner-git-stderr-locale-hardening`; R1 2/4 REVISE 3 major [#142 收口 conflate / "803 绿"循环论证 / CJK 命令错] → Rev1 → **R2 4/4 PASS** |
| 4 | 实施 | TG-A `_run` LC_ALL=C (主 loop 亲自) + TG-B env 断言 + CJK 真测 + TG-C 文档 |
| 5 | code-review | aria:code-reviewer **PASS** (M-1 CJK 全 subject 断言加固) |
| 6 | ship | aria PR #83 merge `2976dc3` + release `528d4af` 双远程; 5 SOT v1.46.1; 主仓 gitlink 528d4af; #143 closed (fixed) + #142 closed (wont-fix) |

## §2 未完成 / Carry-forward

owner 四项不变 (§0.5)。**AI follow-up**: F1 / F2 / **F5 ([#144](https://forgejo.10cg.pub/10CG/Aria/issues/144))** track_board 黄条 (coordination_ref_present=None + coordination_ref_fetch_failed 时看板提示; render-side, soft_error 已进 errors[]/exit 10 仅 render 缺感知)。**F3/F4 已收口** (#142 wont-fix / #143 fixed)。

## §3 关键陷阱 (本 cycle 实证)

1. **验证 issue 标题目标是否可达再决定怎么修** (§4 memory 复用): #142 标题"区分 absent vs hidden" 实测 ls-remote rc=2 覆盖两者 → git 协议不可解 → 不是实现问题, 是死规矩 → wont-fix 而非硬做。起 cycle 前验诊断 (per [[feedback_rebenchmark_test_diagnosis_not_metric]])。
2. **no-op-in-test-env 硬化的循环论证** (新 memory): LC_ALL=C 在已 C-locale CI 是 no-op → "805 绿"不证注入起效。须 mock dispatch 边界断言 env 已传 (host-locale-agnostic), 非断言结果。post_spec qa-major 抓出。
3. **adversarial Critical 按部署可达性裁断** (复用上 cycle memory): silent-failure-hunter #142 auth-masked Critical → LC_ALL=C 不解决 (正交), git 不可解, Aria 部署不可达 → documented-limitation, 不盲做。区分 #142(wont-fix)/#143(fixed) 两病灶 (post_spec tech-lead-major)。
4. **git add 路径前缀** (实证): aria submodule 内 `git add` 用 submodule-根相对路径 `skills/state-scanner/...`, 非 `scripts/collectors/...` (后者匹配失败致 commit 空跑, HEAD 未动)。

## §4-§5 memory / 同步状态

**新建 1 memory**: [[feedback_noop_in_test_env_hardening_needs_mechanism_assertion]] — 防御性 fix 在测试环境 no-op 时全套件绿循环论证, 须 mock 边界断言机制本身。**复用**: [[feedback_adversarial_finding_severity_by_deployment_reachability]] (#142 wont-fix 裁断) + [[feedback_rebenchmark_test_diagnosis_not_metric]] (验诊断)。Spec 归档 `2026-06-13-state-scanner-git-stderr-locale-hardening`; #143/#142 非 US 关联; CLAUDE.md/主仓 VERSION 本 commit 同步 v1.46.1。

## §6 Next session 入口

`/aria:state-scanner`。优先级: owner 四项 > AI 可做 (F5 #144 / F1 / F2)。

## §7 提交清单

| 仓 | HEAD | parity |
|----|------|--------|
| aria-plugin | `528d4af` (PR #83 merge `2976dc3` + release; feature 分支已删) | ✓ origin+github |
| standards | (本 cycle 未改) | ✓ |
| 主仓 | 本 commit (gitlink 528d4af + 归档 + handoff + CLAUDE.md/VERSION) | push 后 ✓ |

> C.2.4 gate: aria-plugin 无 CI → skip_with_warning (Rule #8)。

## Cross-references
- 归档 Spec: `openspec/archive/2026-06-13-state-scanner-git-stderr-locale-hardening/`
- 审计报告: `.aria/audit-reports/post_spec-R2-2026-06-13-state-scanner-git-stderr-locale-hardening.md`
- Forgejo: Aria [#143](https://forgejo.10cg.pub/10CG/Aria/issues/143) (closed/fixed) + [#142](https://forgejo.10cg.pub/10CG/Aria/issues/142) (closed/wont-fix) + aria-plugin [PR #83](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/83)
