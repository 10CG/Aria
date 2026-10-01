---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-01T00:15:08.818Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 backend-architect 报告 — secret-net-l3-and-bypass-paths (proposal v1 @ 47aa15f)

## 已实读文件

- 被审: `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 全文 (1-366); `baseline-evidence.md` 全文; `baseline_probe.py` 全文。
- 必读材料: 三个 issue 正文与评论 (aria-plugin-154 / aria-plugin-203 / Aria-221); 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; CLAUDE.md 规则 #6 / #7 / #10 与多远程两条硬约束。
- 源码 (aria @ 268da8f): `hooks/secret-scan.sh` 全文 (1-377); `hooks/secret-guard.sh` 全文 (1-1120); `hooks/hooks.json` 全文; `hooks/tests/secret-scan.test.sh` 全文; `hooks/tests/secret-guard.test.sh` 1-40 / 819 / 1600-1640 / 1660-1880 (SC-8 延迟闸) / 2000-2050; `.github/secret_scanning.yml`。
- 规范: `standards/conventions/secret-hygiene.md` 全文; `skill-benchmark-exemption.md` 全文; `.aria/pat-inventory.yaml` 1-60; `aria/skills/spec-drafter/LEVEL_GUIDE.md:160-162`。
- 研究笔记 (背景, 与源码冲突以源码为准): `cc-hooks.md` 全文、`secret-scan.md` 1-260、`secret-guard.md` 1-120。
- Claude Code 2.1.285 二进制 `strings` 抽查: `updatedToolOutput` schema 与 `CLAUDE_PROJECT_DIR` 相关文本。

### 实跑验证 (全部在副本 `.../audit/post_spec-R1-backend-architect/` 内; 值运行时生成, 只看退出码 / 是否告警 / tag)

- **V1 基线可复现 (Spec 头部声明)**: `cp -a` 复制 aria / standards / spec 后 `TMPDIR=$PWD/tmp HOME=$PWD/home python3 spec/baseline_probe.py $PWD/aria > probe_run1.out` → rc=0, 41873 字节, `sha256sum | cut -c1-16` = `1ab63a323da13f45`, stdout 与 `baseline-evidence.md` 内嵌块逐字相同, 末两行 `baseline shape ... holds` / `target shape ... does not hold`。成立。
- **V2 W1-W3 可表达 (SC-4..SC-11 可满足)**: 按 W1/W2/W3 字面写出原型 (`make_proto.py` → `proto/secret-scan.strict-spec.sh`: 6 个新 tag 为线性 ERE + `grep -oE`/`sed -E` 计数框架内的 bash 3.2 风格分类器) 并放进探针: SC-1..SC-11 与 SC-15 共 101 行, 仅 15a 仍红 (`alert m=34`, 需 W7 夹具拼装; 基线 33, 新 tag 在该文件多命中 1 处)。15b-15f (含 proposal.md 与探针自身) 静默。
- **V3 W8/W11/W12 可表达**: `make_guard_proto.py` 加 5 条 `risky_patterns` 行 + 名字组变量 + tight 并入 + jq 锚定 credit + 三行 `\.env(rc)?([^A-Za-z0-9_]|$)`: SC-16/17/22/23/24 共 120 条命令行全部等于目标期望, SC-18 4/4, SC-25 d/e/g 文案哈希相同。首版 5 条外壳形态 (`ssh host 'ps aux'`、`x=$(ps aux)`、`watch -n1 'ps aux'`、`sh -c 'ps aux'`、`bash -c "ps -ef"`) 失败, 原因是 BSD 选项簇后只认空白作终止符; 把终止符类放宽到 `[;&|)}<>'"`]` 即全绿 (自报薄弱点 4 因此有实证)。副作用与 W14 描述一致: 套件 PASS 580/582, 红的是测试内 SC-13 头注释 (无 git 副本假红) 与 SC-19 census (`family_count` 65 ≠ 61, `risky_patterns` 145 → 150)。
- **V4 C1 证据**: `python3 exp1b_w3_on_proto.py` (基线 / W3 字面原型 / W3 收窄原型三列)。
- **V5 C2 证据**: `python3 exp6_envdump.py` (基线 / W12 原型两列)。
- **V6 M1 证据**: `python3 exp2_fpfn.py` + 把 loose 路径读法与收窄白名单两个原型各放进探针 (`probe_loose-spec.out`、`probe_strict-narrow.out`)。
- **V7 延迟**: `exp4_timing_l1.py` / `exp4b_glob_prefilter.py` / `exp5_timing_l3.py` (wall-clock, 取 min, 机器 load 2-9)。
- **V8 本仓语料普查 (自报薄弱点 3)**: `exp7_census.py` 用 W1-W3 字面原型扫 `git ls-files` 取得的 3963 个 ≤200KB 文本文件 (主仓 + 三个子模块, 排除 ab-results): 原型告警 13 个文件; 含新 tag 告警 7 个, 其中 3 个基线已告警; 仅新增 4 个 (`aria-orchestrator/docs/t2-2-job-register-dispatch-evidence.md`、`.../tests/test_feishu_redact.py`、一份 benchmark `result.txt`、`aria/skills/requesting-code-review/examples/no-plan-fallback.md`), 新 tag 分布 `kv-secret-assign` 6 文件 / `json-credential-field` 1 文件; 全是示例或夹具。
- **V9 其它**: `echo '{"pin":483920}' | jq -c 'map_values(length)'` → `{"pin":483920}` (jq 1.6); 二进制含 `updatedToolOutput: "Replaces the tool output before it is sent to the model"`; bash 正则微测 (见 M4); W8 边界微测 (见 m5)。

## Findings

### C1 — id `14b7e703` / critical / issue / architecture / scope `proposal.md What.W3`
**summary**: W3 把 `<`、`$`、`{{` 前缀白名单延伸到既有 `json-secret-field`, 使基线已检出的真实形态变静默 (含 JSON 里的 bcrypt 哈希), 且验收看不见。

**证据**:
- Spec W3: 「作用范围 = 6 个新 tag + 既有 `json-secret-field`」, 值以 `<` / `$` / `{{` 开头即不计数; 「被放行的 span 仍被计数哨兵替换, 后序 tag 看不到它」; 已知限制写「以白名单词开头的真凭据会被放过 (须人为构造)」。
- 基线 (268da8f) 实跑: `{"password":"<16 位混合值, 首字符 $>"}`、首字符 `<`、`{"client_secret":"<...>"}`、`{"password":"$2b$12$<53>"}`、`{"passwd":"$2b$12$<53>"}` 全部 `alert m=1 {json-secret-field=1}`。
- W3 字面原型 (`proto/secret-scan.strict-spec.sh`) 同 5 个输入全部 `silent`; 对照输入 (首字符 `{` 与 `A`) 仍告警。因 span 被哨兵吞掉, 后序 `bcrypt-hash` 也不会再见到该哈希。
- 收窄原型 (`strict-narrow`: 仅 `FAKE`/`PLACEHOLDER`/`NOT-REAL`/`REDACTED`/`[REDACTED`、掩码、精确哨兵前缀 `<secret-scan-counted:`、整值闭合形 `<...>`、`${...}`、`$(...)`、`{{...}}`) 放进同一探针: 与字面原型逐行相同 (SC-1..11 共 101 行除 15a 外全 yes), 且上述 5 个基线检出输入全部保持告警。即没有任何 SC 需要裸 `<` / `$` 前缀规则。
- 验收盲区: `baseline_probe.py:98` `BAD_FIRST = set("/.~<$*{[\"'+=-_")` 与 `:104` `_ok()` 使所有生成值都不以这些字符开头; SC-11 11t 的正例是 `<12 alnum>!`。

**失败场景**: 实现者照 W3 写 → API/日志里 `{"username":"x","password":"$2b$12$..."}` 或口令管理器生成的 `$...` / `<...` 开头口令, 基线 `json-secret-field=1`, 目标态静默; 全部 326 行探针仍绿。属「现有检出变成放行」。

**建议修法**: 既有 `json-secret-field` 只加 issue #154 评论 19339 点名的四个标记与掩码 / wrapper 占位 / 精确哨兵前缀; `<`、`$`、`{{` 仅作用于 6 个新 tag 且要求整值闭合形; SC-11 增 reverse-guard: `$` 开头与 `<` 开头的真实形态值 (既有键与新键各一)、JSON 里的 bcrypt 哈希仍检出。

### C2 — id `179045cd` / critical / issue / architecture / scope `proposal.md What.W12`
**summary**: W12 的 `\.env` 右边界改动把 Python `os.environ` 整表导出 (等价 `printenv`) 从拦截变放行, Impact 与 SC-23 都未识别该语义。

**证据**:
- 基线 (副本实跑, exit 码): `python3 -c "import os; print(os.environ)"`、`print(dict(os.environ))`、`json.dumps(dict(os.environ))`、`os.environ.items()` 循环、`os.environ.copy()`、`os.environb` 全部 exit=2 (被 `\.env` 命中 `os.environ` 的子串, 属偶然); 裸 `printenv` / `env` exit=2 (有意: `secret-guard.sh:866-868` 「Bare printenv / bare env (no args = dump everything)」)。
- W12 原型 (三行 `\.env(rc)?([^A-Za-z0-9_]|$)`) 下上述 Python 形态全部 exit=0; `node -e "console.log(process.env)"` 仍 exit=2 (KNOWN-LIMIT 23r); 裸 `printenv` / `env` 仍 exit=2。
- SC-23 只有 `.env` 文件读取的 reverse-guard (23g-23q), 没有环境整表导出的 reverse-guard; 23b 还钉住 `sorted(os.environ)` 放行。Impact 「新放行」只写 `os.environ` / `os.environb` / `*.environment`, 未提整表导出。

**失败场景**: 会话环境导出了 token (本仓有 2026-07-01 `~/.bashrc` 里 `FORGEJO_TOKEN` 先例) → AI 跑 `python3 -c "import os; print(dict(os.environ))"` 直接执行, 值进上下文; L3 看到的是单引号 dict repr, 只有 provider 前缀类能命中 (见 m1)。属「现有拦截变成放行」且泄密不可撤销。

**建议修法**: 边界改动保留, 但加 fail-closed 收口: 只放行单键访问 (`os.environ.get(` / `os.environ[` / `os.getenv(`) 与键名 / 长度形 (`sorted(` / `len(` / `.keys(` 包裹), 整表用法 (`print(os.environ)`、`dict(`、`.items(`、`.values(`、`.copy(`、`json.dumps(`、`**os.environ`) 继续拦; 或另设 python/node/lua 环境导出专行。SC-23 增整表导出 reverse-guard 并在 Impact 明写。

### M1 — id `a3054a20` / major / issue / testing / scope `baseline_probe.py value generators; proposal.md SC-5 SC-9 SC-11`
**summary**: 探针值生成器排除一切 `/ + - _ $ <` 开头的值, 且 W2 对「路径形」只用散文定义, 两种合理实现读法 (严格 / 宽松) 同样通过全部 326 行。

**证据**: `baseline_probe.py:98` `BAD_FIRST`; W2 原文「不是『以 `/`、`~/`、`./`、`../` 开头、首段为小写目录名』的路径形」, 「小写目录名」无字符类定义。我做两个字面原型 (严格: 首段 `[a-z0-9._-]+`; 宽松: 任何 `/` 开头即路径形) 各过一遍探针, SC-1..11、15 的行结果逐行相同; 但 `JWT_SECRET = <44 位 std-b64, 首字符 '/'>` 与 `{"token":"<44 位 b64, 首字符 '/'>"}` 严格版 `alert m=1`, 宽松版 `silent`。首字符 `+` `-` `_` 两版均告警 (但探针从不构造)。

**失败场景**: 实现者取更省事的宽松读法 → 全绿; `openssl rand -base64 32` (即 10CG/aria-plugin#203 事故形态) 有 1/64 (约 1.6%) 以 `/` 开头, 这部分泄露静默。

**建议修法**: W2 用正则写死路径形判据 (含首段字符类); 生成器增「强制首字符」模式, SC-4 / SC-5 各加 `/` `+` `-` `_` 开头的正例, BAD_FIRST 只留给 allow-guard 行; C1 的 `$` / `<` 反向守卫同走该模式。

### M2 — id `d4bcaf7c` / major / issue / architecture / scope `proposal.md What.W9 What.W10 Impact.性能预算`
**summary**: W9 扩展条目与 W10 变量展开的延迟无上界、无 SC; 5 秒超时即放行, 功能自身会把「超时放行」悬崖左移。

**证据**:
- `hooks.json` 中 secret-guard 的 `timeout` 为 5; 超时即放行是 Spec 自己 7.1 的建议开单项 (研究笔记有活体证据)。
- 实测 (min, ms; 单次调用含 bash+jq 启动): 基线 1 段 49 / 40 段 250 / 100 段 752 / 200 段 1703; W8/W11/W12 的 5 行原型 1 段 50 / 100 段 947 / 200 段 1993 (在 1.5 倍内); 基线 + 200 条扩展行 (每条一次正则, 模拟 W9 上限) 1 段 87 / 40 段 1578 / 100 段 3871 / 200 段 11041, 约 130 段起越过 5 秒; 同样 200 条字面条目改用 glob 预筛 (`[[ $seg == *"$lit"* ]]`, 命中才跑读取器正则) 为 51 / 279 / 1370。W10 下界 (`$` 段多判一次): 「8 赋值 + 40 引用」317 → 496 ms; 研究笔记另测含真实替换的 1.7 → 3.9 s (负载下)。
- 现有闸门覆盖不到: `secret-guard.test.sh:1861-1873` 五档负载 (a)-(e) 只有 echo 与命中末位 pattern 的串, 无变量、无扩展; SC-31 31a 只计静态行 145 → 150; W14 「变量展开只在段含 `$` 且收集到赋值时触发」是触发条件而非上界。

**失败场景**: 采用方放满 200 行扩展 (Spec 允许) 并跑 130+ 段的链式脚本 → hook 超时 → 整条命令 (含内建规则) 被放行; 同样的扩展让每次 Bash 调用多 40-300 ms, 若按 SC-8 口径测会超过 100 ms 天花板, 但无人测。

**建议修法**: W9 规定字面预筛实现 (或建一次组合正则), 加 SC-8 风格档 (f) 「200 条扩展 × 4 段」与 (g) 「8 赋值 + 40 引用」, 沿用 `max(100ms, 改前 × 1.5)` 天花板; W10 对赋值值先做一次合成判定, 无命中则跳过展开。

### M3 — id `7deac83f` / major / decision / architecture / scope `proposal.md Impact.issue 收尾口径 待 owner 复议.3`
**summary**: 待复议 3 的默认值 (理解 A: 在 10CG/aria-plugin#203 与 10CG/Aria#221 上评论代码侧进展) 对含糊的 owner 原话选了「动手」, 且是外向动作。

**证据**: 决策单第 1 项把 #203 / #221 归 A 类, 第 2 项执行注「相关 issue 保持 open、本项之下不评论」; Spec Impact 「issue 收尾口径」写「保持 open, 只评论代码侧进展」, 待复议 3 默认理解 A; 决策单第 4 项授权的是评论这一类动作, 与第 2 项的字面冲突由 Spec 自行裁成「只对轮换话题不评论」。

**失败场景**: 发版时执行席按默认在 #203 / #221 发评论, owner 实际取字面理解 → 已发出的通知与评论无法收回, 且违背「含糊授权不等于授权」的既有教训。另: Spec 允许 ship 后即关闭 #154, 但 post-ship 腿 (harness hook 链复验) 需 owner 更新插件缓存并重启, 关闭可能早于端到端验证。

**建议修法**: 默认改为理解 B (#203 / #221 不评论, 待 owner 复议后再发); 关闭 #154 的前置写明「post-ship 复验完成, 或评论里明示复验待办」。

### M4 — id `719ae05c` / major / issue / testing / scope `proposal.md SC-19 SC-20`
**summary**: SC-19 / SC-20 只用 `.` 与 `+` 两种元字符验证「字面子串」, 实现者只转义这两个也全绿; 含其它元字符的条目会静默失效, 组合正则下一条坏条目会让全部扩展静默失效。

**证据** (bash 5.2 实测): 条目 `/srv/app(prod)/secret.conf` 仅转义 `.` `+` 后 `[[ "cat /srv/app(prod)/secret.conf" =~ $re ]]` rc=1 (不匹配); 条目 `/srv/app[prod]/secret.conf` rc=1; 把一条未配对 `(` 的条目放进组合交替正则, 合法条目路径也得 rc=2 (正则非法, `if` 当假, 全部条目失效)。探针扩展内容 (`baseline_probe.py` `EXT_OK`) 只有 `/srv/billing/conf/prod.toml`、`/srv/a.b/c+d/key.conf`、`abc`、`!.env`; SC-20 的坏文件种类不含「坏条目」。

**失败场景**: 实现者按组合正则 + 转义 `. +` 实现 → SC-19 / SC-20 全绿; 采用方写 `[prod]` 或 `(` 的路径条目 → 条目或整个扩展静默不生效, 项目误以为受保护 (W9 自认「失效是静默的」)。

**建议修法**: W9 规定用 glob / `case` 做字面匹配 (不拼正则); SC-19 加逐元字符条目 (`\ ^ $ . | ? * + ( ) [ ] { }`), SC-20 加「一条坏条目不得使其它条目失效」行。

### m1 — id `1b61303c` / minor / issue / implementation / scope `proposal.md What.W2 已知限制 SC-9 SC-10`
**summary**: W2 的漏报 / 误报类清单不全, 若干类未成文也未钉住。

**证据** (原型实跑): 漏报 — Python dict repr `{'token': '<40 hex>'}` 静默; `DB_PASSWORD="<20 位含符号>"` 与 `PASSWD = <20 位含符号>` 静默 (值字符类不含符号); JSON 套 JSON 的转义引号静默; `cf-access-client-secret` 的大小写未规定 (curl -v 经 HTTP/2 回显为小写头名, SC-6 只测首字母大写)。误报 — `{"files":[{"sha1":"<40 hex>",...}]}` 校验和 JSON → `json-credential-field=1`; `Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=` 文档示例 → `auth-header-token=1`; `TOKEN_ID: <uuid>` → `kv-secret-assign=1`。原样静默 (符合 SC-9): git sha / sha256sum / UUID / npm integrity / digest。

**失败场景**: 实现按 Spec 字面做, 行为与上面一致, 但使用者与审计者不知这些边界。

**建议修法**: 并入已知限制并以 known-limit / known-FP 行钉住; 单引号变体成本低, 可直接纳入 `json-credential-field`; 明确头名大小写。

### m2 — id `369a8b32` / minor / issue / implementation / scope `proposal.md What.W4 SC-12`
**summary**: W4 的指纹取值对象在头部 / 参数 / URL / PEM 类 tag 上未定, SC-12 只覆盖 `json-secret-field`。

**证据**: 「键形 tag 取分隔符之后的值, 其余 tag 取整个 span」未说 `auth-header-token` / `cf-access-client-secret` / `cli-secret-flag` / 既有 `bearer-token` 归哪类; `.aria/pat-inventory.yaml` 指纹是「sha256(token 原文, 无换行)」, 对 `Authorization: token <v>` 整 span 取哈希则与台账不可比 (正是 10CG/Aria#221 的形态); PEM 走 perl 预扫, 取块方式未写; 「按出现序」是 tag 序还是文本序未写。

**失败场景**: 两种实现得到不同指纹, 全部 SC-12 仍绿; 指纹对头部类泄露失去对账价值。

**建议修法**: 逐 tag 写明取值对象 (头部取末词、参数取 `=` 后、PEM 取整块), 排序规则写明, SC-12 各族补一例。

### m3 — id `b9d73d73` / minor / issue / documentation / scope `proposal.md What.W12 jq`
**summary**: 「`map_values(length)` 只出元数据」对数值型字段不成立。

**证据**: jq 1.6 实测 `{"pin":483920,"neg":-7}` → `map_values(length)` 输出 `{"pin":483920,"neg":7}` (数字的 `length` 是绝对值); 既有 `length` credit 同类, 非新增类。

**失败场景**: 数值型秘密 (PIN 等) 经被 credit 的 `map_values(length)` 原样输出。

**建议修法**: W12 与 SC-24 增一条 KNOWN-LIMIT (数值字段会被回显), 不改 Nomad Variable 的现有结论 (其值恒为字符串)。

### m4 — id `60eea71e` / minor / issue / testing / scope `proposal.md SC-26`
**summary**: SC-26 的判定命令与其文字范围不符, 且是短语匹配。

**证据**: Spec 写「§2.5 有一行含 `pgrep -a`」, `baseline_probe.py` `_sot_ps_row` 对整份 `secret-hygiene.md` 任一行含 `pgrep -a` 即过; `_sot_clause` 任一行同时含四个词即过。

**失败场景**: 在 §9 之类位置写一句即可全绿 (为通过检查器而写的内容)。

**建议修法**: 把 §2.5 切成区段再判, 或同时断言所在小节标题。

### m5 — id `c941e4e1` / minor / issue / implementation / scope `proposal.md What.W8`
**summary**: W8 名字组的右边界与左前缀未定, 模板 / 示例被拦、连字符目录漏拦。

**证据** (`proto/secret-guard.proto2.sh` 实跑): `cat jobs/forgejo/app.ini.tpl`、`sed -n 1,20p docs/forgejo/app.ini.example`、`grep -rn x /home/dev/forgejo/app.ini.go` 均 exit=2; `cat /srv/git-forgejo/app.ini` exit=0 (被 `_SG_PP_NAME` 前置白名单挡掉); `cat /tmp/app.ini.bak` 放行 (先 `cp` 再读副本, SC-17 17j 刻意放行 `cp`, 该类与基线 `.bashrc` 一致)。

**失败场景**: 基础设施仓里的 Forgejo 配置模板每次编辑都要 ack; 反向是 `git-forgejo` 之类目录漏拦。

**建议修法**: 决定并钉住右边界 (`app\.ini([^[:alnum:]_.-]|$)` 或明确接受 `.bak` / `.tpl`) 与 `-` / `_` 前缀的处理; 在 W8 已知限制里写明 `cp` 后读副本。

## 对执笔人自报薄弱点与请裁项的表态

自报薄弱点:

1. SC-30 无探针基线: **可接受** — 测试内 SC-8 为计时闸且需 `af87cae` 历史, 放 B.1 实测并记 handoff 的做法成立。
2. 目标态文本自扫描只能 B.2 验: **可接受, 且已部分验证** — W1-W3 字面原型下 15b-15f 静默, 15a 需 W7 (新 tag 在该文件多命中 1 处, W7 须一并拆掉)。
3. W2 终版未普查: **可接受, 已在本仓复跑** — 见 V8, 3963 文件仅新增 4 个告警, 均为示例 / 夹具。
4. W11 外壳形态无原型: **可接受, 已有实证** — V3 全绿; 实现坑 = 选项簇后的终止符类要含 `)`、引号、`;`。
5. W9 项目根语义: **可接受** — 二进制含「a guard that inspects the project must use $CLAUDE_PROJECT_DIR or the cwd field on stdin」, 与 W9 两级来源一致; 超限整体忽略的成本问题见 M2。
6. SC 钉得很紧: **部分不成立** — tag 与计数钉死, 但值边缘 (路径形、首字符) 自由度很大, 见 M1。
7. 用例规模 326 行: **可接受**。
8. rule6_note 块 B 归类: **可接受** — 插入文本是事实陈述, 符合 SOT §2 第 1 行与逐 hunk 判定; Rule #10 的复议已列。
9. Level: **可接受** — 维持 owner 已裁的 Level 2; 规模接近 Level 3 的事实 Spec 已自陈。
10. `linked_issue_overlap == []` 未见 gate 原文: **可接受** — 头部已声明取证来源。

待 owner 复议 (产品级): 1 默认 A **可接受** (二进制确认 `updatedToolOutput` 存在, Spec 的平台陈述正确; 研究笔记 `cc-hooks.md` §1 与二进制不符); 2 默认 A **可接受**; 3 默认 A **不可接受** (见 M3); 4 **可接受**; 5 **可接受** (`ps aux | grep -c X` 一类习惯会被拦, 已申报); 6 MINOR **可接受**; 7 清单 **可接受** (7.1 超时放行应提高优先级, 见 M2)。

技术级: 8 **可接受**; 9 **部分不可接受** (路径形未定义, 见 M1 / m1); 10 **不可接受** (C1); 11 **可接受** (补 m2); 12 **可接受**; 13 **可接受** (补 m5); 14 **可接受** (须先解 M2 / M4); 15 **可接受**; 16 **不可接受** (`.env` 边界的整表导出副作用, 见 C2); 17 **可接受**。

## 风险 / 疑问

- Windows Git-Bash: L3 对 6 字节干净输入基线已需约 254 ms (约 100 次进程派生), 6 个新 tag 约再加 24 次; 10CG/aria-plugin#203 报告者在 MINGW64, Spec 的 2.5 s 预算只在 Linux 实测。
- `node -e "...process.env..."` 仍被拦 (KNOWN-LIMIT 23r), 对 TS/Node 采用方 (Kairos) 的误拦继续存在。
- SC-31 31a 的 150 行上限被我的 5 行原型恰好用满; 实现者若把 W11 拆成更多行会越线, 建议写明「合并行」或放宽到 155。
- 活体观察: 本会话已装的 v1.74.1 guard 拦了我含 `/run/secrets/` 字样的 heredoc (既有 prose 误拦); B.2 期间 AI 自己的命令也会撞新规则, 建议 handoff 记「改测试文件用 Write 工具」。
- W10 我没有原型, 只有下界测量与研究笔记数字; bash 3.2 (macOS) 在本机不可测。
- 研究笔记 `cc-hooks.md` §1「不存在 `updatedToolOutput`」与 2.1.285 二进制 schema 不符, 不是 Spec 缺陷, 但落盘材料应订正以免后续误引。
- 超时放行本身的可观测性: 超时无任何告警, 建议 W9 / W10 落地后在日志里记延迟。

## Verdict

- verdict: **FAIL**
- counts: **2C/4M/5m**
- **Vote: REVISE**

## 是否足以进入 A.2

不足以 — C1 (W3 白名单延伸造成既有检出变静默) 与 C2 (W12 放行 Python 环境整表导出) 照 v1 实现会是安全回退且验收看不见, 须出 v2 收窄这两处并补 reverse-guard SC, 同时补 M1-M4 的 SC 与延迟预算后再进入 A.2。
