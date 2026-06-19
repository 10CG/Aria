# tdd-enforcer-security-commit-separation

> **Status**: ✅ **SHIPPED 2026-06-19** (aria-plugin v1.47.0, PR #88 merge `281388d` 双远程 parity)。代码侧完成 + reviewed (Cycle D of v1.47.0 issue-sweep release train)。实现 → **agent-team 2-lens review** (code-reviewer + tech-lead) → 全部 2 Critical + 3 Important + Minor 处置。
> **Review 处置**: Crit-1 (code-reviewer) 参考 hook 用 `git log -1` 读错 commit (pre-commit 时机读到上一条, bypass 失效) → 改 **commit-msg hook** ($1=消息文件); Crit-2 test 分类漏 `test_*.py` 前缀 → 补正则; Imp-3 安全 grep 无词边界 `authority/healthcheck/oauth` 误命中 (memory `feedback_word_boundary_root_causes_substring_shadows`) → 锚定完整前导段 `(^|/)(kw)([_.-]…)?\.ext$`; Imp-4 strict.json 缺 ts 三项 → 对齐 schema; I-1 (tech-lead) advisory 行 self-negating (特性仅 strict+ 激活) → 删 advisory 行改 2 行表; Minor: #32 第4触发省略说明 + hook=strict 档示意注 + workflow 摩擦提示。
> **Level**: 2 (Minimal — proposal + tasks)
> **Target skill**: `aria/skills/tdd-enforcer`
> **Target version**: → **v1.47.0** (MINOR — 新增可选检测特性; release-train 同批)
> **Forgejo issue**: [Aria #32](https://forgejo.10cg.pub/10CG/Aria/issues/32) — tdd-enforcer Level 3 security 特性 RED/GREEN commit 强制分离
> **Rule #6**: capability skill 子特性 (prompt-guidance + deterministic 检测规则 + config) → structural (schema 有效 + 检测 pattern 良构) + dogfood-by-construction (回放 Aether #42 bundled RED+GREEN commit)。

## Why

Aether #42 (fix-hardcoded-docker-auth) post_implementation audit Round 1, aria:code-reviewer 发现:

> TDD discipline is nominal, not enforceably followed. The only way to prove RED-first would be a commit where tests fail; no such commit exists.

两个关键 commit (`f105646` / `e2ceeb0`) 把 **RED test + GREEN impl 打包在单 commit** (+349 test + +108 impl 同 commit)。测试质量本身好 (95% 覆盖), 但**审计员无法从 git history 验证 test-first**。对 **安全敏感特性** (credential / auth / acl / secret handling) 这是明显的 discipline gap —— 这正是最需要可证 test-first 的代码类别。

当前 tdd-enforcer 的 strict/superpowers 模式检查"测试存在 + RED 状态", 但**不强制 commit 粒度的 RED/GREEN 分离**, 故 bundled commit 通过。

## What Changes

tdd-enforcer 在 `strict` / `superpowers` strictness 下新增 **安全代码 commit 分离** 检测 (可选, 默认关)。

> **命名决策 (自我判断优化)**: #32 原提 config key `level_3_strict` / `level_3_patterns`, 但 "Level 3" 与 tdd-enforcer 既有 strictness 第三档 **"Level 3: Superpowers"** 命名**严重冲突** (读者无法区分"Level 3 安全特性"与"Level 3 严格度")。本 Spec 改用语义清晰的 `security_commit_separation`, 并在文档注明此即 #32 的 `level_3_strict`。

- **TG-A (schema)** — `tdd-config-schema.json` 加 `security_commit_separation` object: `enabled` (默认 false) + `path_patterns` (默认 `check*/auth*/acl*/secret*/credential*` × go/py/ts) + `commit_msg_keywords` (`security/auth/credential/secret/token`) + `trigger_on_spec_level_3` (默认 true) + `bypass_token` (默认 `[skip-tdd]`)。
- **TG-B (SKILL.md)** — 加 **安全代码 RED/GREEN commit 分离** 节: 检测触发 (路径 OR commit-msg OR spec level:3 OR 安全相关 skill) → 要求 RED commit (`test(<scope>): [RED]`, 仅 test/fixtures) 与 GREEN commit (`feat(<scope>): [GREEN]`, prod code + 通过测试) 分离; REFACTOR commit 可选。明确与 strictness 的交互 (见升级路径)。
- **TG-C (升级路径 + bypass)** — 本特性仅 `enabled=true` 且 strict/superpowers 激活 (故**无 advisory 行**, 避免 self-negating 矛盾): strict: 阻断, `[skip-tdd]` 显式绕过 (需 PR description justification); superpowers: 不可绕过 (`[skip-tdd]` 失效)。
- **TG-D (reference hook + example)** — `examples/config-examples/` 加 security 示例配置; SKILL 内附**可选** PreCommit hook 参考实现 (项目侧 opt-in 部署, **不**接入 Aria 自身 hooks.json — Aria 非安全代码项目)。

## Impact

- **版本**: v1.47.0 (release-train MINOR)。
- **向后兼容**: ✅ `security_commit_separation.enabled` 默认 false → 现有 tdd-enforcer 行为零变化; 仅显式开启 + strict/superpowers 才激活。
- **受影响文件**: `tdd-config-schema.json` (schema) + `SKILL.md` (检测节 + 升级路径 + hook 参考) + `examples/config-examples/` (security 示例) + `CHANGELOG.md`。
- **Rule #6**: structural (schema 有效 JSON + 检测 pattern 良构 + 与 strictness 矩阵一致) + dogfood-by-construction (Aether #42 `f105646` bundled commit → 检测会要求拆 RED/GREEN)。

## Out of Scope

- 把 PreCommit hook 接入 Aria 自身 `hooks.json`: Aria 是方法论项目无安全代码, hook 是**项目侧 opt-in** 参考实现; 不在 Aria 运行时强制。
- 自动拆分已 bundled 的 commit: 仅**检测 + 要求人/AI 重新分离**, 不自动 rewrite history。
- 跨所有语言的完整安全路径 pattern 库: 给代表性默认 (go/py/ts 常见安全文件名) + 可 config 扩展。
- 强制改名既有 strictness "Level 3: Superpowers": 不动 strictness 命名; 仅新特性用 `security_commit_separation` 避免歧义。
