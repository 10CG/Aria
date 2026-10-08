你是 Aria 仓 (`/home/dev/Aria`) WP-A Spec `secret-net-l3-and-bypass-paths` 的 **post_spec 定点修补核验席** (qa-engineer, 新派实例, 与执笔不是同一个, 也没参与前五轮)。

背景: post_spec 收敛审计跑满 `max_rounds` 5 轮未收敛。owner 2026-10-07 裁定「接受当前结论 + 定点修补」: 新执笔实例把 proposal v5 修补为 v6, 再由**你一个席**只核修补处及其与未改文字的接缝。这**不是第 6 轮全审**, 你的结论决定能否进入 A.2。

被审提交 `{V6_SHA}`, 在主仓分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 上。全程中文叙述, 代码 / 命令 / 路径 / SHA 保留英文。

## 你要核的 (范围严格限定)

1. **改动面**: `git diff 785209f {V6_SHA} -- openspec/changes/secret-net-l3-and-bypass-paths/`, 即 v5 → v6 的全部改动 (proposal.md / baseline_probe.py / baseline-evidence.md)。
2. **接缝**: 改动与未改文字之间的一致性。
   - 新改条款之间, 以及新改条款与未改条款之间, 有没有互相违反隐含前提;
   - 改动里引用的行号、SC 编号、7.x 编号、待复议编号是否落地。
3. **对账清单**: 以 R5 聚合报告 `.aria/audit-reports/post_spec-R5-2026-10-07T080138-000Z-secret-net-l3-and-bypass-paths-aggregated.md` 为准, 逐项写 closed / not closed / partially closed:
   - 「全部 finding」表的 21 个席位条目;
   - 「主控记录」节的 owner 裁定 2 条与主控裁定 1–8。

不在范围内: 未改动段落本身的问题。确实看到的, 写进「风险 / 疑问」, 不计入 finding。不要重做全量语料普查。

## 背景事实 (主控实测)

{CONTROLLER_FACTS}

## 必读

1. v5 → v6 的 diff 与 v6 三份文件 (按需读改动附近的上下文)。
2. R5 聚合报告全文, 尤其「主控记录」节的 owner 裁定与主控裁定 1–8; 以及五席报告里与各条 finding 对应的段落。
3. 执笔的修补报告 `.aria/notes/2026-09-30-wpa-phase-a/writer-reports/v6-writer-report.md` 与处置 `v6-dispositions.json`。
4. 你的视角需要的源码与规范, 实读并以 `file:line` 为准:
   - `aria/hooks/secret-guard.sh`、`aria/hooks/secret-scan.sh`、`aria/hooks/hooks.json`、`aria/hooks/tests/`;
   - `standards/conventions/secret-hygiene.md`。
5. 平台二进制 `/home/dev/.local/share/claude/versions/2.1.285` (簇 X 相关): 只读, 用 `LC_ALL=C /usr/bin/grep -a -o '<片段>.\{0,N\}'` 取片段, 不要整文件读。

## 你的视角: 修补是否真的关上了, 而且没有开新口子

1. **每个修补点三态**: 逐项回答基线 / 目标 / 坏实现三态下各是什么值, 并亲自跑判定命令。
2. **坏实现由你独立构造**: 对每个 major 的修补点, 你自己在原型副本上构造至少一个「像真实错误」的坏实现, 不能只复跑执笔的; 确认它让对应行转红。本仓教训: 执笔自带的夹具会和执笔同源盲区。
   - 簇 AA: 用第 5 轮 qa 席列出的六类自然窄化;
   - 簇 Z: 用 `remote_env_split` 与 `printenv NAME` 两个方向;
   - 簇 Y: 把 `_sg_core_eval` 放回闸门之下;
   - 簇 X: 两个方向都要有, 即「只提取 `error` 不注册」与「只注册不提取」。
3. **簇 X 专项**:
   - `hooks.json` 只多一条注册, 全文不含 `completeness_gate` 字面;
   - 失败事件的输出字段 (`hookSpecificOutput` 等) 与二进制 schema 对得上;
   - 成功路径对既有检出是超集: 拿既有 L3 测试语料与 R5 各席用过的形态, 对比 v5 原型与 v6 原型的成功信封检出, 0 回退;
   - 失败信封的检出与同内容的成功信封一致。
4. **证据复跑**: 在新副本 (aria `268da8f` + standards `2bc1c4c`) 上:
   - 带 `WPA_BASH32` 复跑探针, stdout 必须与 `baseline-evidence.md` 内嵌输出逐字节相同, 基线形态 holds;
   - 用执笔的构建脚本重建 v6 原型, 带 `WPA_REQUIRE_ALL=1` 全量跑一次, 目标形态 holds, 且新的退出码约定按 Spec 生效;
   - 簇 Y 的 git 腿: 在带 `af87cae` 历史的本地 clone 上跑一次既有套件的 SC-8 块, 确认原型下五档是真测 (不是 127 返回)。
5. **净增长与范围**: 改动是否超出 owner 与主控裁定点名的范围 (新机制、未点名段落的重写)。超出的部分按其影响定级。

## 资源纪律 (owner 2026-10-07 要求降低宿主机负载)

宿主机是共享的, 前几轮实验把它的 CPU 打满过。你的命令已在主控进程设定的 nice 19、只用 0–1 号核的环境下运行 (自动继承), 不要尝试改回。另外:

1. **同一时刻只跑一个重负载实验**: 探针全量、坏实现批量、时档测量、大输入性能用例都算重负载。不要并行起多个探针或批量任务。
2. **探针全量最多跑两次**: 带 `WPA_BASH32` 的基线一次, 目标原型带 `WPA_REQUIRE_ALL=1` 一次。其余一律用 `WPA_ONLY=<SC 列表>` 只跑相关子集。
3. **坏实现只跑与修补点相关的**: 每个修补点 1–2 个, 由你独立构造。不重跑执笔归档的整套坏实现。
4. **模糊 / 差分用例每类不超过 30 个**。不做几百次级别的普查。
5. **时档测量** (W14 `timing.py`、既有套件 SC-8、SC-34):
   - 跑前看 `/proc/loadavg` 的一分钟值, 低于 2 才跑; 高于就等一会儿, 或只报比值;
   - 结论只依据比值与活性断言, 不以绝对毫秒下结论;
   - 与其它实验串行。

## 严重度口径 (与前五轮一致)

- **critical**: 照 Spec 实现会造成安全回退 (现有的拦截或检出变成放行), 或造成难以撤销的外向后果, 或 Spec 自身的验收会放过一个错误实现。
- **major**: 符合以下任一:
  - 照 Spec 字面实现会卡死;
  - 得出不可证伪 / 恒绿 / 恒红的验收结论;
  - 漏掉某个必做项;
  - 与 SOT (issue 诉求、决策单、owner 裁定、CLAUDE.md、源码事实、平台事实) 矛盾;
  - 修补没有关上它要关的 finding。
- **minor**: 措辞、引用精度、可读性, 不改变实现者会做什么。
- 一条 finding 若不影响「实现者会不会做错 / 做漏 / 卡住」, 也不影响安全效果, 最高只能是 minor。

## 证据要求

- 每条 finding 附你亲自核验的证据: `file:line` 原文片段, 或实跑命令与输出 (可截断, 不得改写)。无证据的推测写进「风险 / 疑问」。
- 每条 finding 写清失败场景, 并回答「它怎么会红」(三态)。
- finding 的 `id` 计算方式: `sha256(f"{category}:{scope}:{severity}:{type}")[:8]`, scope 只写一个节锚, 规则同前五轮:
  - scope 取值只能是 `proposal.md What.W<n>`、`proposal.md SC-<n>`、`proposal.md <节名>`、`baseline_probe.py`、`baseline-evidence.md` 之一;
  - 「修补未关上」的 finding 沿用 R5 那条的四元组。

## 硬性纪律

- **不写任何仓内文件**。报告放进结构化输出的 `report_markdown`, 由主控原样落盘。
- 实跑只在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/audit/post_spec-R5-fixcheck-qa-engineer/` 下进行: `cp -a` 到那里再跑, 运行 hook 时 HOME 指向该目录下的 `home/`。本地 `git clone` (源为本机仓, 只读) 可用。
- 真仓内**不做任何 git 写操作** (commit / push / fetch / pull / checkout / switch / stash / reset / tag / update-ref 一律禁止)。需要远端事实用 `git ls-remote`。不开 issue、不发评论。
- **禁止派子代理** (不得使用 Agent 工具)。
- **Rule #7**:
  - 不读取、不打印任何真实凭据;
  - 需要「像凭据的值」时在 Python 进程内用 `secrets` 运行时生成, 经 stdin 喂给 hook (`capture_output=True`), 绝不打印;
  - 报告只写退出码 / 是否告警 / 命中规则等元数据。
- 含敏感形状讨论的文字用 Write 工具落文件, 不放进 heredoc / `python3 -c` 命令行 (现行 L1 会拦)。

## 报告格式

报告以下列 YAML frontmatter 开头:

```
---
checkpoint: post_spec
mode: fix_verification
rounds: 5
converged: false
oscillation: false
overridden_by_user: true
degraded: false
verdict: PASS | PASS_WITH_WARNINGS | FAIL
timestamp: <你写完报告时的 UTC ISO 8601 毫秒>
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---
```

verdict 规则: 有 critical ⇒ FAIL; 无 critical 有 major ⇒ PASS_WITH_WARNINGS; 否则 PASS。

正文依次为:

1. `## 已实读文件`
2. `## 对账` —— 一张表, 逐项写出:
   - R5 的 21 个席位条目;
   - owner 裁定 2 条;
   - 主控裁定 1–8 (含第 7 条列出的各个定点勘误)。

   每项写 closed / not closed / partially closed, 以及你亲自核验的证据 (含你独立构造的坏实现及其结果)。
3. `## Findings` —— 本次核验发现的问题, 按 critical → major → minor 排序编号 (C1 / M1 / m1 …)。每条包含: `id` / severity / type / category / scope / summary / 证据 / 失败场景 / 建议修法。
4. `## 证据复跑记录` —— 命令、sha256 前 16 位、字节数、形态结论。
5. `## 风险 / 疑问` (不计入 finding)。
6. `## Verdict` —— verdict + counts + **Vote: PASS 或 REVISE**。
7. `## 是否足以进入 A.2` —— 一句话结论加理由。

结构化输出的 verdict / counts / vote / findings 必须与正文一致。
