---
track-id: secret-guard-multiline-and-anchor-fix
owner-container: simonfish/bfe8285d
phase: D
status: done
updated-at: 2026-07-11
---

# Session Handoff — secret-guard 四票并案 triage + 修复全周期 ship (v1.55.2)

## §0 入口 (新 session 优先读)

- **本 session 干了什么**: owner 要求同步三仓 + 状态扫描 → 选「secret-guard 四票并案」→ **triage** (`/issue-triage` 核对 #154/#156/#157/#152, POST verdict, #156 关为 dup) → **Level 2 修复 cycle** 全周期 (A.1 proposal → B 双缺陷实施 → B.2 RED-first 测试 + code-review → C PR#103 合并 → D 归档 + 关三活票)。**aria-plugin v1.55.2 SHIPPED**。
- **当前态**: 全闭环, 本 track 无阻塞 carry-forward。aria master `023351b` (origin=github ✓)。四票 (#154/#156/#157/#152) 全 closed。
- **下一步优先级**: 见 §6。

## §1 已完成

### Triage (十步循环前置)
1. 四票逐一跑 `triage.py` (Step 0 机械采集, exit 0/10); 读全文 + 核实真代码。
2. **两个独立缺陷定性**: 缺陷 A (`hooks/secret-guard.sh:118` readarray 逐行读) 一行两症状 = macOS bash3.2/zsh 无 readarray 崩溃 (#154/#156) + 多行 command 截断仅首行进正则 (#157); 缺陷 B (7 处 `^` 锚定正则) = 中段 env 逃逸 (#152)。本机实测复现 #152/#157 (exit 0 放行), #154/#156 根因代码级确认 (无 macOS/zsh 本机)。
3. **核实 #157 dual-install 论断属实**: 主仓 settings.json 挂 `.claude/scripts/secret-guard.sh` (旧副本, 逐字段 jq 完整捕获多行) 掩盖了分发版 `hooks/` 的回归。
4. verdict: #154/#157 confirmed critical, #152 confirmed major, #156 dup-of-#154; POST 4 comment (#157 完整锚点 + 3 精简), #156 关闭。

### 修复 (Level 2, owner 定方案: NUL 分隔 + Level 2)
5. **缺陷 A**: `:118` readarray → `jq -j` NUL 分隔 + `while IFS= read -r -d ''` (newline-safe + bash3.2 兼容, 无 readarray/mapfile)。源码用可见 `\u0000` escape (非真 NUL 字节)。
6. **re-exec-to-bash guard (zsh 端到端实测揭示的 #154 更深根因)**: 只做 NUL 修复后 zsh 直接执行**仍全 fail-closed** (合法 ls 也 exit2) —— hook runner 用 `$SHELL`=zsh 忽略 shebang, 整 bash-specific 脚本体 (`read -d ''`/`[[ =~ ]]`/数组/进程替换) 在 zsh 崩。顶部加 POSIX-sh `[ -z "$BASH_VERSION" ] && exec bash "$0" "$@"`。
7. **缺陷 B**: 7 处 `^[[:space:]]*` → `(^|[;&|]|[[:space:]])[[:space:]]*` 前缀 (**含换行** —— 缺陷 A 修好后多行第 2 行 env 前是 `\n`, issue 建议前缀漏换行仍逃逸, 实测验证); 4 处 bare dump 后缀重构 `([[:blank:]]*($|[;&|]|[[:cntrl:]]))` (含 code-review Important#1: 后缀侧 `;`/`&`/无空格`|` 逃逸)。
8. **B.2**: 测试 260→292 (16 缺陷 case + 6 review#1 逃逸 + 4 静态断言 + 6 zsh 端到端); RED-first 证明 (revert 后缀 fix 后逃逸 case exit0); code-review (aria:code-reviewer, 3 critical 隔离实测正确, Important#1 修 + 补测, Minor tab over-block 保留 fail-safe)。副本字节同步。
9. **C/D**: PR#103 合并 `023351b` (C.2.4 零 CI run → Rule #8 exception 留痕); github parity 3/3; 归档 `openspec/archive/2026-07-11-secret-guard-multiline-and-anchor-fix`; 关 #154/#157/#152; 主仓 VERSION/badge/CLAUDE.md v1.55.2。

## §2 未完成 / Carry-forward 清单

- {id: carry-secretguard-subshell-152, desc: code-review Minor#3 — 子壳 env 逃逸 `$(env)`/`` `env` ``/`(env)` 仍放行 (pre-existing, threat-model 已声明 adversarial shell quoting out of scope); 非阻塞已知 gap, 若要收需专门 cycle}
- {id: carry-secretguard-tab-overblock, desc: `printenv\tPATH` (tab 分隔参数) 被保守 over-block (fail-safe, 极罕见); 若要精确区分需 pattern 嵌真换行, 低优}
- (承前, 非本 cycle) M6 owner 4 门 (input-delivery build/deploy/egress/E2E ← Blocker 4 Luxeno) → 遥测 Track-1 合并; M7 D3 门; aria-plugin#101 (TT 摘要表漂移); i18n README @1.51.0; 主仓 /VERSION 内部陈旧。

## §3 关键风险 / 已知陷阱

- **harness 把源码里 backtick/引号间的空格转成真 NUL 字节**: 本 session 反复中招 (secret-guard.sh jq 程序 / CHANGELOG / proposal 三处)。`grep -P '\x00'` **不可靠** (遇 NUL 视 binary 返空), 必须用 **python `b'\x00' in open(f,'rb').read()`** 核验。git `Bin X -> Y bytes` 是真 NUL 信号。修法: python latin-1 byte-replace `` `\x00` `` → 可见 escape。
- **sed 全局替换灾难**: `sed -i "${LINE}s/..."` 中 `$LINE` 为空 → 退化全文件替换 (误改 line 85 printf 分隔符)。改用 python 按行 index 或唯一 marker 定位 + 断言替换数。
- **secret-guard 修复生效即拦自己**: review-fix commit message 含字面 `env|grep`/`env;` 触发刚修好的 hook (dogfood 极致验证)。commit/comment 用文件传 (`-F`/`-d @file`), hook 只看 command 不看文件内容。
- **zsh 兼容不能只靠断言**: 只改字段提取 (readarray→NUL) 后必须**真在 zsh 下 end-to-end 跑** —— 实测才发现整脚本 fail-closed, 单点修复不够 (feedback_dryrun_peels_blocker_chain 体现)。装 zsh (`apt-get install zsh`) 实测。
- **forgejo 长 body POST 500**: PR#103 首次全量 body 触发 500 (同 #157 comment); 用精简 body / 去 markdown 表格 pipe 转义。

## §4 实战教训 (memory 沉淀候选)

1. **[候选 memory] 防御修复必须在真实执行环境 end-to-end 验证, 不能只单元测试**: readarray→NUL 修复后 bash 测试 286 全绿, 但 zsh 实测暴露整脚本 fail-closed (hook runner 用 zsh)。若不测 zsh 会 ship 一个"看似修好但 macOS 上仍全崩"的补丁。补 re-exec guard 才根治。→ 强化既有 `feedback_dryrun_peels_blocker_chain` / `feedback_noop_in_test_env_hardening_needs_mechanism_assertion`。
2. **[候选 memory] harness 会把编辑内容里 backtick/引号包裹的空格转成真 NUL 字节**: 本 session 三处中招。检测必用 python 二进制读 (grep -P 遇 NUL 骗人)。→ 可能值得记 (工具环境陷阱)。
3. **修 pattern 补明必带正反例实测**: 缺陷 B 前缀设计中 issue 建议的 `(^|[;&|]|&&|\|\|)` 漏换行, 实测才发现 (缺陷 A 修后多行第2行 env 前是 `\n`); review 又发现后缀侧漏 `;`/无空格`|`。安全正则改动每一版都要跑正反例矩阵。

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| aria-plugin | **v1.55.2** @ `023351b` (origin=github ✓); PR#103 merged |
| 主仓 | 本 cycle 收尾 commit (归档 + 副本同步 + gitlink + VERSION/badge/CLAUDE.md); 推后核 parity |
| standards / aria-orchestrator | 未变更 (9df1722 / daf7c79) |
| Forgejo | Aria #154/#156/#157/#152 全 closed |

## §6 Next session 入口 + 优先级建议

1. (承前) **M6 owner 4 门** (尤 Blocker 4 Luxeno) → 遥测 Track-1 合并 + Track-2/3。
2. secret-guard 子壳逃逸 (carry-subshell-152) —— 若 owner 认为 threat-model 该扩到子壳, 专门 cycle。
3. aria-plugin#101 摘要表漂移 (Level 2 独立)。
4. 惯例: 大活前 fetch 三仓 + 双子星 claim。

## §7 提交清单 (multi-remote parity)

- aria-plugin: `217ef4e` (缺陷A/B/re-exec) + `625c0cc` (review#1 后缀) → merge `023351b` (PR#103); origin=github ✓
- 主仓: 本 handoff 随收尾 commit (归档 + 副本 `.claude/scripts/secret-guard.sh` 同步 + gitlink 8fea71d→023351b + VERSION/badge/CLAUDE.md v1.55.2)
- Triage 产物: `.aria/triage-report-{154,156,157,152}.json`

## §8 Memory entries this session

- 候选见 §4 (2-3 条); 本 handoff 写完后评估是否落盘 (dryrun-end2end 强化 + harness-NUL 陷阱 + 安全正则正反例)。

## Cross-references

- Spec: `openspec/archive/2026-07-11-secret-guard-multiline-and-anchor-fix/`
- Issues: Aria #154/#156/#157/#152 (全 closed)
- 上一 handoff: [2026-07-09-agent-router-baseline-semantics-shipped-v1.55.1.md](./2026-07-09-agent-router-baseline-semantics-shipped-v1.55.1.md)
