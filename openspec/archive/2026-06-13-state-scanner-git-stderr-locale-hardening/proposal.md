# state-scanner-git-stderr-locale-hardening

> **Status**: ✅ **SHIPPED 2026-06-13** (aria-plugin **v1.46.1**, PR [#83](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/83) merge `2976dc3` + release `528d4af` 双远程 parity; 主仓 gitlink → `528d4af`)。post_spec R1 REVISE (2/4, 3 major) → Rev1 → **R2 PASS 4/4 unanimous**。Phase B: TG-A/B/C + env-断言测试 + CJK 真测 (805 全绿, 138 git-collector 测试 under LC_ALL=C 零回归) + code-review PASS (M-1 加固)。#143 fixed; #142 wont-fix 收口。
> **Level**: 2 (Minimal — proposal + tasks)
> **Target skill**: `aria/skills/state-scanner` (aria-plugin)
> **Target version**: v1.46.0 → **v1.46.1** (PATCH — locale-robustness 硬化; 见 §Impact)
> **Forgejo issues**: [Aria #143](https://forgejo.10cg.pub/10CG/Aria/issues/143) (F4 — **本 Spec 修复**) + [Aria #142](https://forgejo.10cg.pub/10CG/Aria/issues/142) (F3 — **wont-fix 收口**, 非本 Spec 修复, 见 §#142 收口); 均源自 #141 code-review silent-failure-hunter。
> **Rev1 (post_spec R1)**: 修 #142 收口语义 (LC_ALL=C 不解决 #142 auth-masked 隐患, git 不可解 → wont-fix 非 fixed; tech-lead-major); TG-B 加 env-断言测试 (C-locale CI 下 "803 绿" 对注入有效性循环论证, qa-major); 修 CJK 实测命令 `--format=%s`→`--oneline` (实际 git.py:181 路径, qa-major); OQ2 定 **drop LANG=C** (LC_ALL=C 已折叠所有 LC_*, backend-arch); 补 tasks.md; 路径补 `scripts/` 前缀; custom_checks 独立 subprocess + ls-tree 注记。

## Why

state-scanner 多个 collector 通过**匹配 git/网络 stderr 的英文文本**分类错误:
- `scripts/collectors/coordination_fetch.py`: benign 闸 (`"couldn't find remote ref"`, v1.46.0 #141) + `_classify_error` (`"could not resolve"` / `"connection refused"` / `"authentication failed"` / `"non-fast-forward"` / `"rejected"`)
- `scripts/collectors/multi_remote.py:259-261`: `"could not resolve host"` / `"timed out"` / `"authentication failed"` / `"permission denied"`
- `scripts/collectors/issue_scan.py:296-300`: `"could not resolve host"` / `"connection refused"`

`scripts/collectors/_common.py::_run` (L314-358) 用 `subprocess.run(... text=True, encoding="utf-8")` 但**不设 `env=`** → 继承进程 locale。

### Problem (#143/F4) — 非英文 git locale 致 stderr 文本匹配失灵

git 诊断消息 (stderr) 随 `LC_MESSAGES`/`LANG` 本地化。非英文 locale 下:
- coordination_fetch benign 闸 `"couldn't find remote ref"` 匹配失败 → 良性"协调 ref 未发布"误报为 Fetch2 故障 (false-negative, spurious soft_error, 回退 #141 想消灭的噪音)。
- `_classify_error` / multi_remote / issue_scan 网络·auth 分类退化为 fallback (误分类)。

**当前运行时已 C locale** (实测 `setlocale: LC_ALL: cannot change locale (en_US.UTF-8)` → fallback C → 英文输出), in-deployment 暂不触发 → 属**防御性硬化** + 消除一类 latent 脆弱性。silent-failure-hunter (#141 review #2) 明确建议 `LC_ALL=C` 为"性价比最高、加固整个文件所有 stderr 匹配"的单点修复。

### #142 (F3) 收口 — git 协议不可解, wont-fix (本 Spec **不**修复)

> **Rev1 关键澄清** (tech-lead-major): #142 与 #143 **病灶不同**, 不能混为一谈。

#142 的原始关切 (silent-failure-hunter #1) = **auth-masked ref 被吞成 benign** (token 失效 / ACL / `uploadpack.hideRefs` 隐藏 ref 时, git 报 `rc=128 + "couldn't find remote ref"`, 与"ref 真不存在"**完全相同** → 误判 benign, success=True, silent)。

- **`LC_ALL=C` 不解决此隐患**: 它只统一 locale (修 #143); auth-masked 场景仍是 rc=128 + 英文 "couldn't find" → 仍判 benign。两者正交。
- **ls-remote 也不解决** (实测验证 2026-06-13): `git ls-remote --exit-code <remote> <ref>` → rc=0 (advertised) / **rc=2 (未 advertise — absent 与 hidden 同 rc=2)** / rc-other (transport)。git 协议层**根本无法区分 absent vs hidden** (#142 标题的目标不可达)。ls-remote 唯一真实价值 = locale-independent benign 信号, 但 LC_ALL=C 落地后该价值归零, 仅剩"抓极罕见 race"边际收益, 不值 +1 网络往返 (非协调项目热路径)。
- **结论**: #142 的 auth-masked silent 隐患 = **git 协议不可解**, 保持 **documented-limitation** (#141 已落地缓解: benign 命中 log.info 可追踪 + docstring/schema 显式记限制)。ls-remote **decline** (不解决问题 + 成本)。→ #142 **wont-fix 收口** (诚实留 comment, 不 imply 被修复)。

## What Changes

单一 Level 2 Spec, 三 task group (链式 TG-A→TG-B→TG-C)。**仅修复 #143**; #142 是 wont-fix 收口 (无代码)。

### TG-A — `_run` 注入 `LC_ALL=C` (locale 根治, 全 git-stderr 匹配点受益)

- `scripts/collectors/_common.py::_run` 的 `subprocess.run(...)` 加 `env={**os.environ, "LC_ALL": "C"}` (os 已 import L17), 强制 git 诊断输出英文/C-locale。
- **OQ2 定: 只设 `LC_ALL=C`, drop `LANG=C`** (backend-arch 实测: `LC_ALL=C` 折叠所有 `LC_*` 含 `LC_MESSAGES` 无视 `LANG` → `LANG=C` 冗余; `LC_ALL=C` 是 git-scripting 标准惯例)。
- **与 #61 UTF-8 fix 兼容** (实测): `LC_ALL=C` 影响 git **自身生成的诊断文本** (英文化), **不影响 commit 消息/ref/路径字节直通** —— 用**实际 git.py:181 路径** `git log --oneline --no-decorate -N` 实测: `LC_ALL=C` 输出与默认 locale **字节完全相同** (md5 一致, 含 CJK + em-dash 双语 commit; backend-arch 独立复核 `for-each-ref` / `worktree list --porcelain` 同字节直通)。`encoding="utf-8"` + `errors="replace"` 解码不变。
- **不改任何 collector 匹配逻辑** —— 它们本就假设英文, 本 Spec 只让该假设在任意 host locale 成立。
- **不覆盖 `custom_checks.py:320`** (code-reviewer-m1): 该处独立 `subprocess.run(shell=True)` 跑**用户任意 shell 命令** (rc-based, 不做 git stderr 英文分类) → 非本 Spec 病灶; 其 locale 由用户命令自负。`handoff_multibranch.py` ls-tree `"not a tree object"` 等是 git 内部常量 token (非 i18n catalogue) locale-stable, 已审视确认安全。

### TG-B — 测试 (env 断言 + CJK 直通 + 全套件回归)

> qa-major: C-locale CI 下 `LC_ALL=C` 是 no-op, "803 绿"只证"英文环境无破坏"**不证注入有效**。必须有显式 env 断言。

- **env 注入断言** (核心可证伪): `unittest.mock.patch("collectors._common.subprocess.run")` 捕获 `call_args.kwargs["env"]`, 断言 `env["LC_ALL"]=="C"` 且保留 `os.environ` 其余键 (superset `>=` 比较, 非整 dict 硬断言, 防脆弱); 保留 6 个既有 kwarg (capture_output/text/encoding/errors/timeout/check)。
- **(可选) 非英文 locale 集成测试**: `zh_CN.utf8` 本 CI 已装 (`locale -a` 确认) → parent 设 `LANG=zh_CN.UTF-8` 真跑一条出英文 stderr 的 git 命令经 `_run`, 断言 stderr 英文。可行则加, 固化"真起效"。
- **CJK 直通回归**: 基于**实际 `--oneline` 路径** (非 `--format=%s`) 真跑 fixture repo (含 CJK commit), 断言 LC_ALL=C 下 subject 不 mangle (隔离 tmpdir fixture per [[feedback_test_worktree_fixture_isolated_tmpdir]])。
- **全套件零回归**: `python3 tests/run_tests.py` (**canonical runner**, 设 sys.path → 803 全绿; 本环境无 pytest; **不用** `unittest discover` — 它缺 sys.path 致 `lib.claim_schema` import-err 得 717+4err 假基线, R2 code-reviewer/qa 实证)。绿 gate = "既有通过项不回归"。
- Rule #6 = unit (env 断言) + 全套件 + CJK 固化, 无 capability AB ([[feedback_deterministic_structural_skill_rule6_substitute]])。

### TG-C — 文档同步 (Rule #3)

- `_common.py::_run` docstring: 加 `LC_ALL=C` locale-forcing 说明 (为何 + 与 #61: locale 管诊断文本, encoding 管字节解码, 正交; LANG 冗余故未设)。
- `coordination_fetch.py::_is_benign_coordination_absent` docstring: 现有"英文 locale 假设"已知限制注记 → 更新为"已由 `_run LC_ALL=C` 强制保证"(#143 闭环); **absent-vs-hidden 限制保留** (git 不可解, #142 wont-fix)。
- `references/state-snapshot-schema.md` coordination_fetch section: 同步 benign 闸 locale 注记。
- 无 schema 字段变更 → `snapshot_schema_version` 保持 `1.0`。

## Impact

- **Affected**: `scripts/collectors/_common.py::_run` (TG-A 单点) + `tests/test_common.py` (env 断言) + `tests/test_git.py` 或新 fixture (CJK 直通) (TG-B) + `_common.py`/`coordination_fetch.py` docstring + `references/state-snapshot-schema.md` (TG-C)。
- **向后兼容**: ✅ 纯 additive env 注入; 已英文/C-locale 环境 (含当前运行时 + CI) **无可观测变化** (LC_ALL=C no-op); **非英文 locale 用户**会观察到 false-negative 噪音消失 (observable bug-fix, 仍 PATCH 轴; tech-lead-minor: 非"完全不变"措辞精修)。CJK 字节直通实测零影响。
- **Cross-cutting 安全**: `_run` 全 git-collector 共用 → TG-B 全套件回归是硬闸。已审视全部 git-stderr 匹配点 (coordination_fetch/_classify_error/multi_remote/issue_scan/handoff_multibranch ls-tree) 均英文-假设或 locale-stable token; `custom_checks` 用户命令独立 subprocess 不在范围。
- **Rule #6**: deterministic infra → env 断言 unit + 全套件回归 + CJK 固化, 无 AB。
- **Versioning**: v1.46.0 → **v1.46.1** (PATCH)。锁定既有英文假设, 无新字段/能力/API/exit-code 变化 (对比 #141 加 `coordination_ref_present` field + observable exit 10→0 = MINOR; 本 Spec 仅强制隐含假设, 非英文 locale 的噪音消失属 bug-fix 轴)。**post_spec 可挑战** PATCH vs MINOR。

## Out of scope

- **#142 ls-remote / auth-masked silent** (wont-fix, 见 §#142 收口): git 协议不可解 (absent-vs-hidden 同 rc=2); ls-remote 不解决问题 + 成本; 已 documented-limitation + log.info 缓解。**本 Spec 不碰**。
- **absent-vs-hidden ref 区分** (git 协议不可解)。
- F1 (lib::fetch_coordination_ref) / F2 (耦合解耦) / F5 (track_board 黄条) — 独立 follow-up。

## #142 收口 (Rev1, 非本 Spec 修复)

#142 → **wont-fix close**, comment 诚实说明: (1) 标题"区分 absent vs hidden" git 协议不可解 (实测 ls-remote rc=2 覆盖两者); (2) ls-remote decline (不解决 + 成本); (3) auth-masked silent 隐患保持 documented-limitation (#141 log.info + docstring/schema 已缓解, in-deployment 不可达因 Aria repo 级 ACL); (4) 相关 locale 脆弱性由 #143 (本 Spec) 解决。POST comment + 单独 PATCH state (per [[feedback_issue_close_comment_not_body_patch]])。

## Open questions (待 post_spec R2)

1. **版本 PATCH vs MINOR**: 拟 PATCH (锁定既有假设)。
2. ~~LANG=C 是否必要~~ → **Rev1 定: drop, 只 LC_ALL=C** (折叠所有 LC_*, LANG 冗余)。
3. ~~ls-remote 彻底 decline~~ → **Rev1 定: decline + #142 wont-fix** (不解决其隐患 + 成本)。
