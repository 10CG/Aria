---
track-id: aria-plugin-196-issue-ref-and-numbering-conventions
owner-container: simonfish/bfe8285d
phase: D
status: done
updated-at: 2026-09-13T11:20:00Z
---

# Aria — Session Handoff (2026-09-13, 会话收尾第二次) — 插件缓存核验、aria-plugin#196 裁定写入规范、「文内编号用普通数字」规则 + 代码注释清理

> **一句话**: 接在 aria-plugin#197 发版之后 (本对话后半段): 核验 owner 刷新后的插件缓存 (1.73.2, 与 tag 逐文件一致); owner 裁定 aria-plugin#196 选修法 B、暂不注册闸门 → 写入 `standards/conventions/content-integrity.md` §4.4; owner 追加「编号不用带圈数字和希腊字母」→ 同文件 §4.5, 并清掉 aria 代码注释里全部 7 行带圈编号 (分两批)。三仓两端逐一核验一致, 零行为变更, 不发版。
>
> **本段最该记住的两件事**: 我曾告诉 owner「aria 代码注释里只剩 2 处带圈数字」, 全仓普查实为 aria 69 行 + 主仓 743 行, 只好当场更正; 我还两次在执行的命令里写出了带圈字形, 第二次被原样写进了规范, 靠「用规范自己的自查命令扫规范自身」才抓到。两条都已写成 memory。

> **Next session 入口**: 优先读本 doc → `/aria:state-scanner` → §6

---

## §0 入口 (新 session 优先读)

1. 运行 `/aria:state-scanner`。主仓 `c9fe08f` (+ 本 handoff 提交); aria `fcbc8ac` (v1.73.2 之后又合入 2 批纯注释改动, 未发版); standards `8b49562`; aria-orchestrator `237045a`; 四仓 origin / github 两端一致。
2. **下一个发插件版的人请注意** (很可能是双子星的 Aria#195 MINOR): aria master 在 tag `v1.73.2` 之后有 2 个未发版的合并 —— `308ccce` 与 `fcbc8ac`, 均为 state-scanner 代码注释改动 (编号改用普通数字, 无行为变化)。CHANGELOG 里要带一句。另外 aria-plugin#196 还剩「检查器报错文案指向规范 §4.4」一件, 可顺带做完后关单。
3. **git 身份在会话中途变了**: 本机 git 配置在 2026-09-13 04:28Z 到 07:44Z 之间由 `aria-runner-bot` 变为 `simonfishgit` (本会话没有执行过 `git config`, 原因未查)。容器 uuid `bfe8285d` 不变, 按 `session-handoff.md` §2.3.5 仍是同一身份; 本 handoff 的 owner-container 按机械输出填写。
4. Aria#195 / #199 两条 L2 轨仍在 `simonfish/023236f2` 手上 (claim A.2, 心跳停在 09-12 18:3x, 之后该容器无推送)。本容器不碰。

---

## §1 已完成 (2026-09-13, 按顺序)

| 时间 (UTC) | 事件 | 证据 |
|---|---|---|
| ~08:4x 后 | owner 刷新插件并重启 → 核验: `installed_plugins.json` 记 1.73.2, marketplace 本地副本在 `5a973e7`, 缓存目录与 `git archive v1.73.2` 逐文件一致 (只多一个 `.in_use` 标记), `plugin-cache-currency` OK。另发现该文件的 `gitCommitSha` 仍记 `36428b9` (4 月 v1.15.2 的提交), 不影响加载 | — |
| — | 给 owner 大白话汇报 aria-plugin#196 → owner 选修法 B (写法约定) + 暂不注册闸门 | — |
| 10:1x | standards `content-integrity.md` §4.4「Issue / PR 引用写法」(v2.1.0): 分支提交 `0c24409` → 本地 merge `f4e61b1`; 主仓 `a510bf4`; aria-plugin#196 回帖 comment 23668 (保持 open) | `f4e61b1` / `a510bf4` |
| — | 回答 owner: 该检查与带圈数字禁令不是一回事 (前者防同号异仓、后者防终端里看不清), 只是方向一致 | — |
| 10:3x | standards §4.5「文内编号用普通数字」(v2.2.0): `a174d0f` → merge `8b49562`; aria 注释清理第 1 批 4 行 (`runtime_probe.py` / `multi_remote.py`): `c3ae817` → merge `308ccce`; 主仓 `eddc3b5` | `8b49562` / `308ccce` / `eddc3b5` |
| 11:0x | aria 注释清理第 2 批 3 行 (`phase1_gate.py` / `spec_complete.py`): `f1c75d6` → merge `fcbc8ac`; 主仓 `c9fe08f` | `fcbc8ac` / `c9fe08f` |

每一步都: C.2.4 pre-merge gate green (`not_applicable`: aria 唯一 workflow 不覆盖改动文件, standards 无 workflow; main 无 in-flight) · 主仓 C.2.4.5 submodule gate forward bump PASS · 各仓 origin / github 逐一 `ls-remote` MATCH。测试: 第 1 批相关 4 组 128 条全绿, 第 2 批相关 19 组全绿; 均确认无测试依赖被改的注释原文。

**Cycles shipped this session**: 0 (规范 + 纯注释改动, 未发版)

---

## §2 未完成 / Carry-forward 清单

### 高优先级 (需要 owner)

| # | 项 | 说明 | 来源 |
|---|---|---|---|
| H1 | ~~定 github SSH 根治方式~~ ✅ 已转交 10cg.local (2026-09-13): `10CG/10cg.local#40` —— owner 定 VIP 永久为 `.199`, 统一 10cg.local 与 Aether 文档, 并建议删掉冗余 ProxyCommand | 写死代理地址 vs 删掉改走 `ssh.github.com:443` | 承前 |
| H2 | 复议两处 AI 流程判断 (Rule #10) | (a) aria-plugin#197 按 Level 1 处理 + 选修法 A (见 #197 handoff §2); (b) 本次两处 standards 规范改动没有起 OpenSpec, 按「owner 直接指示的文档规则 = Level 1」处理 | 本会话 |

### 中优先级

- **下次插件发版**: CHANGELOG 带上 `308ccce` / `fcbc8ac` 两批注释改动; 顺带做 aria-plugin#196 剩余的「检查器报错文案指向 §4.4」, 然后关 #196。
- **`check_bare_issue_refs.py` 另一类误报** (2026-09-13 发 10cg.local#40 时撞到): 仓名带 `.` 的全限定引用 (如 `10CG/10cg.local` 加 `#40`) 不被认作全限定 —— 其正则要求 repo 段不含 `.` (本意排除文件路径伪装)。并入 aria-plugin#196 的剩余工作, 下次插件发版一起修。
- **其余带圈字形** (按 §4.5 口径不批量回改, 改到哪段顺手改哪段): aria 测试 5 个文件、参考文档 4 份、session-closer `SKILL.md` (运行时指令面, 改前先按 Rule #6 判断是否要跑 AB)、CHANGELOG / VERSION 历史条目、测试夹具 `issue-201.md` (照抄的 issue 原文, 不应改); 主仓 743 行大多在历史审计报告、归档 spec、handoff 里。
- aria-plugin#198 待定方案; aria-plugin#182 截断证据未回帖 —— 均承前。

### 低优先级 / cleanup

- 本会话 5 个已合并的本地分支已删除 (aria 3 个、standards 2 个)。

### 机械补漏 (autofill backstop)

- `unfinished` 132 条全部来自 M6/M7 六份 spec 的 `tasks.md`, 属各自轨, 与前几份 handoff 分布相同。
- consistency: 8 条 `active_change_not_in_upm` advisory (本仓无运行时 UPM, 已知恒出; 两份 L2 Spec 转 Approved 后由 6 条变 8 条)。
- sync: 零告警。

---

## §3 关键风险 / 已知陷阱

| 风险 | 触发条件 | 缓解 |
|---|---|---|
| 未发版的已合并改动在下次发版时被漏写 | 下次发版者没读到本 handoff | latest.md 更新段已点名; §0 第 2 点 |
| 在命令或文件里表达带圈字符时, 手敲的转义被写成字形本身 | 写正则、自查命令、替换脚本 | 用 `chr()` 拼, 落盘后用独立扫描器核零命中 (memory `feedback_forbidden_glyphs_build_escapes_with_chr`) |
| 局部 grep 得出的「只剩 N 处」是假数字 | 向 owner 报数量 | 全仓 × 完整字符区间普查后再报 (memory `feedback_grep_window_truncation_breeds_false_corpus_evidence` 追记) |

---

## §4 实战教训 (memory 沉淀来源)

- **报数前全仓普查**: 我按几个目录、两个字形的 grep 报了「2 处」, 实际 812 行。→ 追记 memory `feedback_grep_window_truncation_breeds_false_corpus_evidence`。
- **禁用字形不能手敲转义**: 两次写出带圈字形, 第二次进了规范。改用 `chr(92) + "u2460"` 拼转义串、`chr(0x2460)` 拼正则后解决; 规范里的自查命令用来扫规范自身, 抓到了第二次失误。→ 新 memory `feedback_forbidden_glyphs_build_escapes_with_chr`。
- **`installed_plugins.json` 的 `gitCommitSha` 不随更新**: 核验缓存要看 `version`, 再与 tag 逐文件 diff。→ 追记 memory `feedback_plugin_cache_stale_via_stale_marketplace_clone`。

[候选 memory]
- 报数前全仓全区间普查 — type: feedback ✅ 已追记
- 禁用字形用 chr 拼转义 + 独立扫描核零命中 — type: feedback ✅ 已写
- installed_plugins.json 的 gitCommitSha 不可信 — type: feedback ✅ 已追记

[未写下经验]
- git 身份在会话中途由 aria-runner-bot 变为 simonfishgit, 原因未查; 只有一次, 暂不立规。

---

## §5 多维度同步状态

| 维度 | 本段涉及? | 状态 | 备注 |
|---|---|---|---|
| UPM | no | — | 本仓无运行时 UPM |
| User Stories | no | — | — |
| OpenSpec | no | — | 规范改动未起 spec (见 §2 H2) |
| Standards / conventions | yes | `content-integrity.md` 2.0.0 → 2.2.0 (§4.4 + §4.5 + §10.1 工具表) | `8b49562` |
| Skill docs | no | — | 只改了 state-scanner 脚本里的注释 |
| CHANGELOG | no | 未发版 | 下次发版补 (§2 中优先级) |
| Issues | yes | aria-plugin#196 comment 23668 (open) | 回读核验 |
| Auto-memory | yes | 1 新 + 2 追记 | 见 §8 |

---

## §6 Next session 入口 + 优先级建议

```
/aria:state-scanner
```

1. ~~**`{id: carry-github-ssh-proxy-root-fix}`** owner 定 github SSH 根治方式 (承前)。~~ → ✅ 已转 `10CG/10cg.local#40`
2. **`{id: carry-next-plugin-release-notes}`** 下次插件发版时 CHANGELOG 带上 `308ccce` / `fcbc8ac`, 并做完 aria-plugin#196 的报错文案后关单。
3. **`{id: carry-aria-plugin-198-status-paren}`** 等方案定了再修 aria-plugin#198 (承前)。
4. **`{id: carry-owner-review-level1-judgments}`** owner 复议 §2 H2 的两处 AI 流程判断。

**不应该做的**:
- 不碰 Aria#195 / #199 (claim 在 `simonfish/023236f2`)。
- 不批量回改存量带圈字形; 不改测试夹具 `issue-201.md`。

---

## §7 提交清单 (commit hash + multi-remote parity)

```
[main]              a510bf4 → eddc3b5 → c9fe08f (+ 本 handoff 提交) | origin = github ✅
[aria]              308ccce, fcbc8ac (纯注释, 未发版)              | origin = github ✅
[standards]         f4e61b1 (§4.4) → 8b49562 (§4.5)                 | origin = github ✅
[aria-orchestrator] 237045a (未动)                                   | origin = github ✅
```

**Tags published**: 无
**Issues**: aria-plugin#196 comment 23668 (保持 open)

---

## §8 Memory entries this session (本段 1 新 + 2 追记)

| File | Type | Theme |
|---|---|---|
| `feedback_forbidden_glyphs_build_escapes_with_chr.md` | feedback | 禁用字形用 chr 拼转义, 独立扫描核零命中 |
| `feedback_grep_window_truncation_breeds_false_corpus_evidence.md` (追记) | feedback | 给 owner 报数量前全仓全区间普查 |
| `feedback_plugin_cache_stale_via_stale_marketplace_clone.md` (追记) | feedback | installed_plugins.json 的 gitCommitSha 不随更新 |

加上同日上午会话收尾的 2 新 + 2 追记, 当日共 3 新 + 4 追记; MEMORY.md 索引零新增行 (148 行, 22.6KB)。

---

## Cross-references

- 规范: `standards/conventions/content-integrity.md` §4.4 / §4.5
- issue: [aria-plugin#196](https://forgejo.10cg.pub/10CG/aria-plugin/issues/196)
- 前序 handoff: [2026-09-13 aria-plugin#197 发版](./2026-09-13-aria-plugin-197-coordination-fetch-shipped-v1.73.2.md) · [2026-09-13 会话收尾 (上午)](./2026-09-13-session-close-l2-rulings-reconciled-tracks-handed-over.md)

---

**Created**: 2026-09-13
**Status**: Done — 本段工作全部落地; 剩余为 owner 项与下次发版事项
