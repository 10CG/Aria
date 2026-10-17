# 派单: WP-A 实现执笔 — TASK-002 (测试先行, 关键子集)

你是 Spec `secret-net-l3-and-bypass-paths` (Level 2, WP-A) 的**实现执笔实例**。按 owner 2026-10-07 的「实现优先」裁定, TASK-002 到 TASK-009 都由你这同一个实例完成, 主控会逐条派任务 (每条一次消息)。**本次只做 TASK-002**; 做完就报告并停下, 等主控派下一条。

## 背景 (主控已完成 TASK-001, 实测)

- 分支: aria 子模块 `/home/dev/Aria/aria` 已在 `feature/secret-net-l3-and-bypass-paths` (= `268da8f`, 基线); standards 子模块同名分支 (= `2bc1c4c`)。你直接在这个真 checkout 里改文件。
- 基线: `secret-guard.test.sh` 在真 checkout 上 `PASS: 593 / 593` (zsh 未装; 头注释 `Coverage: 599 cases (593 without zsh)`); `secret-scan.test.sh` 49 条。被测文件指纹与 `baseline-evidence.md` 一致, Spec 里的行号全部有效。
- 探针 `baseline_probe.py` 在基线上带 bash 3.2 复跑, 与 `baseline-evidence.md` 逐字节一致。
- 真 bash 3.2: `WPA_BASH32=/home/dev/.aria/tools/bash-3.2.57/bash`; 第二 locale `en_US.UTF-8` 已装; 你是非 root (uid 1000)。

## 必读 (按顺序; proposal 很大, 分段读)

1. `/home/dev/Aria/.aria/decisions/2026-10-07-wpa-implementation-first-owner-rulings.md` (owner 裁定, 3 KB)。
2. `/home/dev/Aria/openspec/changes/secret-net-l3-and-bypass-paths/detailed-tasks.yaml`: `invariants` (INV-1 – INV-7) 与 TASK-002。
3. `/home/dev/Aria/openspec/changes/secret-net-l3-and-bypass-paths/proposal.md`: `## What Changes` (W1 – W14, 约第 48–249 行)、`## Success Criteria` (约第 260–313 行, 每个 SC 的行与类别)、`## Tasks` 的 1.2 (约第 377 行)。
4. 同目录 `baseline_probe.py` (每一行用例的输入构造、期望与判据, 是把用例移植进套件最直接的来源) 与 `baseline-evidence.md` (每行在基线上的实得)。
5. 原型 (INV-1: 实现以它为起点, 行为以 Spec 为准, 冲突时以 Spec 为准并上报): `/home/dev/Aria/.aria/notes/2026-09-30-wpa-phase-a/writer-v6-proto/README.md` 先读; 测试侧原型是 `patch_tests.py`。本任务只动测试, hook 侧原型 (`patch_l3.py` / `patch_l1.py` / `patch_hooks_json.py`) 留到后续任务。

## 本次任务 (TASK-002 / Spec Tasks 1.2)

把回归关键子集移植进两个套件 (owner 裁定: 探针是验收工具, 套件只承载关键子集):

1. **每个 W (W1 – W14) 至少一组新用例**, 优先取 `baseline-failing` 行; L3 (W1 – W7) 进 `aria/hooks/tests/secret-scan.test.sh`, L1 (W8 – W12) 进 `aria/hooks/tests/secret-guard.test.sh`。W13 (拒绝文案零改动) 与 W14 (元耦合) 由你判断落在哪个套件、用哪类断言 (例如 W13 用 `reverse-guard` 钉住拒绝文案关键行不变), 并在报告里说明理由。
2. **夹具一律运行时拼装**, 源码里不出现凭据形状的字面量 (W6 / W7; GitHub 镜像的 push protection 只放行这两个测试文件)。像凭据的值在运行时生成 (参照套件现有写法或探针的生成器), 不打印。
3. 每组新用例旁边注释它对应的 SC 行号与类别, 如 `# SC-5 5a (baseline-failing)`; 用例名不得与现有用例重复 (测试内 SC-17)。
4. **头注释计数**: `secret-guard.test.sh` 顶部 `Coverage: N cases (M without zsh)` 改成加用例后的实跑总数, 让测试内 SC-13 保持绿 (W14 第 1 条; 权威值 = 真 checkout 实跑)。`standards/conventions/secret-hygiene.md` 里的三处计数**本次不改** (留给 TASK-008 / TASK-009), 在报告里写明新数字。`secret-scan.test.sh` 的头注释计数与自检断言属于 W14 的改动本身, 可以作为 W14 的那组新用例 (在基线上应是红的), 由你决定并说明。
5. **不改 hook**: `aria/hooks/secret-scan.sh`、`aria/hooks/secret-guard.sh`、`aria/hooks/hooks.json` 本次一行不动。
6. **在基线 hook 上跑两个套件**, 验收 (TASK-002 的 verification):
   - 新增的 `baseline-failing` 用例全部红, 新增的 `reverse-guard` / `allow-guard` 用例全部绿;
   - 既有用例结果不变 (secret-guard 既有 593 条仍全绿, secret-scan 既有 49 条仍全绿)。
   - 跑套件时 **HOME 必须指向你实验目录下的私有目录** (W6 的隔离要到 TASK-003 才做; 现在不设就会往真实 `~/.claude/logs/` 追加夹具事件)。命令形如 `HOME=<实验目录>/home bash /home/dev/Aria/aria/hooks/tests/secret-guard.test.sh`。

## 资源纪律 (owner 2026-10-07 要求降低宿主机负载)

你的命令已在主控设定的 nice 19、只用 0–1 号核的环境下运行 (自动继承), 不要改回。另外:

1. 同一时刻只跑一个重负载实验 (探针全量、套件全量、大输入用例都算); 不并行。
2. 本任务不需要探针全量; 要对照某几行的构造与判据时, 用 `WPA_ONLY=<SC 列表>` 或 `WPA_ROWS=<行列表>` 只跑子集。
3. 套件全量 (secret-guard 约 2.5 分钟) 跑到够判定即可, 不要反复全量重跑; 调试单条用例用小脚本。
4. 时档类测量本任务不做。

## 硬性纪律

- 只改这两个文件: `aria/hooks/tests/secret-scan.test.sh`、`aria/hooks/tests/secret-guard.test.sh`。实验用的副本、脚本、输出只放在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/impl/` 下。
- 真仓内**不做任何 git 写操作** (commit / push / fetch / pull / checkout / switch / stash / reset / tag / update-ref 一律禁止), 提交由主控统一做。不开 issue、不发评论。
- **禁止派子代理** (不得使用 Agent 工具)。
- **Rule #7**:
  - 不读取、不打印任何真实凭据;
  - 需要「像凭据的值」时在进程内运行时生成, 经 stdin 喂给 hook, 绝不打印;
  - 报告只写退出码、是否告警、tag 名与计数等元数据。
- 现行 hook 的两个已知副作用:
  - 现行 L1 会拦 heredoc / `python3 -c` 命令行里仅为文字提及的敏感读取形状 (如含 `.env` 的文字)。写这类文本一律用 Write / Edit 工具落文件, 再执行文件。
  - 用 Bash 输出 `secret-scan.test.sh` 的文本 (cat / grep / sed) 会被现行 L3 当作泄露告警 (W7 的现状, 基线命中 33 处)。看这个文件用 Read 工具 (基线 L3 不扫 Read 结果)。
- Spec 有歧义、做不到, 或与原型 / 源码事实冲突时: 不要自行发明, 写进报告「请裁 / 冲突」节并说明你的临时处理。

## 报告格式 (最后一条消息就是报告; 中文叙述, 代码 / 路径 / SC 编号保留原文)

1. **概览**: 两个套件新增多少条用例, 改了哪些头注释计数。
2. **按 W 的用例表**: W 编号 │ 套件 │ 新用例名 │ 对应 SC 行 │ 类别 │ 基线实得 (红 / 绿)。
3. **基线实跑**: 每个套件的命令原文、`PASS / FAIL` 行原文; 失败用例清单, 并核对它恰好等于新增的 `baseline-failing` 集合 (多一个或少一个都要点名)。
4. **计数**: 新的实跑总数 (secret-guard 含 / 不含 zsh 两个数; secret-scan), 以及 `secret-hygiene.md` 里待 TASK-008 / 009 同步的三处位置。
5. **请裁 / 冲突 / 偏离**: 没有就写「无」。
6. **用量**: 墙钟, 跑了几次套件全量, 有没有跑探针 (子集名)。
