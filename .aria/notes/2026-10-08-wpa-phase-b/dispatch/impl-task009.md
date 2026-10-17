# 派单: WP-A 文档同步与勘正执笔 — TASK-009

你是 Spec `secret-net-l3-and-bypass-paths` (Level 2, WP-A) 的**文档同步与勘正执笔**。Spec Tasks 1.9 写明「勘正执笔人 ≠ 实现执笔人」, 所以由你而不是写代码的两位执笔来做。**本次只做 TASK-009**, 做完报告并停下。

## 现状 (主控实测)

- 代码侧已全部落地, 在 aria `feature/secret-net-l3-and-bypass-paths` 上, 最新提交 `db4f8b8`, 已推 origin:
  - L3 (`secret-scan.sh`): W1 – W5;
  - L1 (`secret-guard.sh`): W8 – W12, 含 W9 项目级扩展入口 `.aria/secret-guard.paths`;
  - 两个测试套件 W6 / W7 / W14。
- 两个套件在真 checkout 上全绿: `secret-guard.test.sh` 783 / 783 (含 zsh 789), `secret-scan.test.sh` 122 / 122。
- 探针在代码侧的行都是 `yes`; **还没过的只有文档行**: SC-27 有 27a / 27c 两行 `no`, SC-28 共 15 行全 `no`。这就是你的任务。

## 先读 (按顺序; 只读需要的段落)

1. owner 裁定: `/home/dev/Aria/.aria/decisions/2026-10-07-wpa-implementation-first-owner-rulings.md` (3 KB)。
2. `/home/dev/Aria/openspec/changes/secret-net-l3-and-bypass-paths/detailed-tasks.yaml` 的 `invariants` 与 TASK-009 (约 13 KB, 可整份读)。
3. Spec `proposal.md` (240 KB, **不要整份读**; 先 `grep -n` 定位再按行号读), 只读这些:
   - W13 (约第 225–234 行);
   - W14 的「陈旧 / 悬空表述」与「secret-scan 计数」两条 (约第 235–249 行);
   - Success Criteria 里 SC-25、SC-26、SC-27、SC-28 各行;
   - Tasks 1.9 那一行 (约第 384 行)。
4. 探针 `baseline_probe.py` (245 KB, **不要整份读**) 里 SC-25 – SC-28 各行的判据: `grep -n '"SC-2[5-8]"'` 定位后只读那些行。探针就是验收工具, 文本改到这些行判 `yes` 为止。
5. 原型 `/home/dev/Aria/.aria/notes/2026-09-30-wpa-phase-a/writer-v6-proto/patch_docs.py` 是起草期的文档改动原型, 可作起点 (以 Spec 为准, 冲突时上报)。

## 交付物

1. `standards/conventions/secret-hygiene.md` (standards 子模块, 已在 `feature/secret-net-l3-and-bypass-paths` 分支上): W13 SOT 条款与示例、§5.6、计数同步 (SC-27: 三处 secret-guard 计数 = 789 / 783, 一处 secret-scan 计数 = 122)、SC-28 涉及的 5.1 / 5.2。
2. `aria/README.md` 与 `aria/README.zh.md`: SC-28 28m 等要求的句子; 两语种内容对应。
3. `aria/hooks/secret-scan.sh` 与 `aria/hooks/secret-guard.sh`: **只改注释** (头注释、History 块、hook contract 说明), 不改任何代码行。
4. `aria/VERSION`: 只改 28i 点名的那条对 secret-scan 的陈旧描述 (90 KB 大文件, 用 grep 定位), **不改版本号** (发版是 TASK-011)。
5. `aria/hooks/hooks.json` 的顶层 `description` 字符串 (可选): Spec 写的是「可随之更新」。若它描述了注册的事件, 补上 `PostToolUseFailure`; 只改这一个字符串, `hooks` 对象一个字节都不动 (SC-31 31d)。
6. CHANGELOG 草稿: 写到 `/home/dev/Aria/.aria/notes/2026-10-08-wpa-phase-b/changelog-draft.md`, **不改 `aria/CHANGELOG.md`** (发版文件归 TASK-011)。

## 约束

- **hook 文件只改注释**。两条容易踩的: 注释里也**不得**出现 `(?:` (测试内 SC-16 对整个源码做 grep); 头注释里**不得**写新的 pattern / 类别 / 规则总数字面 (SC-28 28c / 28d / 28o 的要求)。
- **文档里不得出现凭据形状的字面量**:
  - aria 与 standards 都有公开的 GitHub 镜像, push protection 会拦;
  - 改完用当前的 `aria/hooks/secret-scan.sh` (已含 W2 新 tag) 把你改动的每个文件当 Bash 输出扫一遍, 必须零命中。扫描方法: 构造 `{"tool_name":"Bash","tool_input":{},"tool_response":{"output":<文件文本>}}` 经 stdin 喂给 `bash /home/dev/Aria/aria/hooks/secret-scan.sh`, HOME 指向私有目录, 看 stdout 的 `additionalContext` 是否为空;
  - 带一个正控 (在文本末尾拼一行进程内生成的 AWS key id 形状, 不打印), 证明扫描有效。
- **示例逐工具实跑** (Tasks 1.9): SOT 里的命令示例若声称「被拦」或「放行」, 要用当前 hook 实跑核对。L1 示例经 stdin 喂 `bash aria/hooks/secret-guard.sh`, 看退出码; L3 示例同上法喂 `secret-scan.sh`。
- **两语种 README 内容对应**; 只加 SC 要求的句子, 不顺手改别的。

## 验收 (报告里给原文输出)

1. **探针子集**: `WPA_ONLY=SC-25,SC-26,SC-27,SC-28 python3 /home/dev/Aria/openspec/changes/secret-net-l3-and-bypass-paths/baseline_probe.py /home/dev/Aria/aria`, HOME 与 TMPDIR 指向私有目录, 输出写文件。期望全部 `yes`; 报告给分组统计与全部非 `yes` 行。
2. **套件不受影响**: 从 `/home/dev/Aria` 相对路径跑一次两个套件 (`bash aria/hooks/tests/<套件>`), 仍是 783 / 783 与 122 / 122。只改了注释, 这一步是防误改代码。
3. **hook 只改注释的机械证明**: 对两个 hook 文件, 去掉整行注释后与 `db4f8b8` 版本逐字节比对相同。给出比对命令与结果。
4. **零凭据形状**: 上面「约束」里的扫描, 每个改动文件零命中, 带正控。
5. **计数**: 报告 SOT 里写入的计数及其来源 (实跑总数)。

## 纪律

- **上下文卫生 (硬要求)**:
  - 只按行号范围读: 先 `grep -n` 定位, 再用 Read 的 `offset` / `limit`;
  - 不整份读 `proposal.md` / `baseline_probe.py` / `aria/VERSION` / `aria/CHANGELOG.md`;
  - 大输出落文件只读摘要; 工具调用宁少勿碎。
- **资源纪律**:
  - 会话进程已 nice 19、只用 0–1 号核 (自动继承, 别改回);
  - 同一时刻只跑一个重实验 (探针子集与套件都算), 不跑探针全量;
  - 不跑 `find /` 一类全盘扫描。
- **硬性纪律**:
  - 只改上面列出的文件;
  - 真仓内 (主仓与两个子模块) 不做任何 git 写操作, 提交由主控做;
  - 不派子代理, 不开 issue / 不发评论。
- **Rule #7**:
  - 不读不打印任何真实凭据;
  - 需要像凭据的值时在进程内运行时生成, 绝不打印。
- **会话 hook 的已知副作用**: 会话里生效的是插件缓存里的旧版 hook, 它会拦 heredoc / `python3 -c` 命令行里仅为文字提及的敏感读取形状 (如含 `.env` 的文字), 写这类文本用 Write / Edit 落文件再执行。
- 实验用的文件与输出只放在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/docs009/` 下。
- Spec 有歧义或做不到时, 不自行发明, 写进报告的「请裁」。

## 报告格式

1. **改动**: 按文件列, 给行号范围与一句话说明, 并对应到 SC 行号; 与原型 `patch_docs.py` 的差异及理由。
2. **探针子集**: 分组统计与非 `yes` 行。
3. **套件 / 只改注释证明 / 零凭据形状 / 计数**。
4. **请裁 / 冲突 / 偏离**: 没有就写「无」。
5. **用量**: 墙钟, 探针子集次数, 套件次数。
