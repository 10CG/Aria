# part 3: W14, Success Criteria, SC rows.   `E(old, new)` = replace one exact substring; `L(prefix, new)` = replace the whole (single) line that starts with `prefix`.
EDITS = []


def E(old, new, count=1):
    EDITS.append(("sub", old, new, count))


def L(prefix, new):
    EDITS.append(("line", prefix, new, 1))


# ---------------------------------------------------------------- W14
E("度量脚本的参考实现随变异汇总归档 (`writer-v4-proto/timing.py`: 档位 `f` `f0` `g` (= g-a) `gmax` (= g-b) `h` `i` `w1`; 它只打印比值与活性, 判据由上面的上界给出)。",
  "度量脚本的参考实现随变异汇总归档 (`writer-v5-proto/timing.py`: 档位 `f` `f0` `fhit` (= f-hit) `g` (= g-a) `gmax` (= g-b) `h` `i` `i3` `w1`; 默认只打印比值与活性; 加 `--judge` 时按下面第 2 项的上界逐档给出 PASS / FAIL 并以退出码表示)。")
E("(i): ≤ 2.0 (新增 6 个 tag = 6 趟额外的 `grep -oE`, 固有开销 20–30%, 上界只为抓「逐 span 无上界迭代」); (g): ≤ 2.5 (W10 第二遍对含引用的段重判一遍, 设计上近乎翻倍)。",
  "(i): ≤ 2.0 (新增 6 个 tag = 6 趟额外的 `grep -oE`, 固有开销 20–30%, 上界只为抓「逐 span 无上界迭代」); (i3): ≤ 2.5 (长单行的匹配与取值是线性的: 固有开销与坏实现的实测倍数见第 5 项); (g): ≤ 2.5 (W10 第二遍对含引用的段重判一遍, 设计上近乎翻倍); **(f-hit): ≤ 3.0** (命令里出现列入的路径时扩展多付一遍内建判定, 设计上约 2 倍)。")
E("(i) 仍告警且各 tag 计数与基线的相等。",
  "(i) 仍告警且各 tag 计数与基线的相等; (i3) 新 tag 仍被计数 (基线档位上的既有 tag 与基线的相等); (f-hit) 内建判定函数 `_sg_core_eval` 在命中档被调用两次 (命令与它的替换副本)、在无命中的对照档一次 (SC-20 20m 的标记法)。")
E("(i) L3 稠密输入: 约 900 KB、每行一个 `Authorization: Bearer <32>` 的输入 (既有 `bearer-token`, 约 1.6 万命中) 与约 600 KB 的 JSON 口令行 (既有 `json-secret-field`, 约 2 万命中)。",
  "(i) L3 稠密输入: 约 900 KB、每行一个 `Authorization: Bearer <32>` 的输入 (既有 `bearer-token`, 约 1.6 万命中) 与约 600 KB 的 JSON 口令行 (既有 `json-secret-field`, 约 2 万命中); **(i3)** L3 长单行: 8 KB 的头值、60 KB 的 `-` 串后接旗标、100 KB 的大写连续段后接键 (基线自己对这类输入也是超线性的: 300 KB 时基线单独就要约 5 s CPU, 所以时档取 100 KB; 探针 SC-34 34b 取 300 KB 但只按每进程 CPU 上限判)、8 KB 的空白串 (export 形)、8 KB 的 bearer 头值 (既有 tag); **(f-hit)** 200 条扩展条目 × 4 KB 单行 Bash 命令: (a) 列入的路径在末尾出现一次, (b) 在填充之后出现 64 次, 另有无出现的对照档。探针内同类退化的功能版本是 SC-34 (CPU 上限下的行, 不依赖比值)。")
E("- **原位改写通则**: 被**原位改写** (而非新增) 的既有规则行与条件 —— `/proc` 两行 (W11)、`python3 -c` / `node -e` 两行 (W8 / W11 追加名字)、`_sg_compute_credit` 的 tight 判定 (W8 / W11 并入名字组) —— 其基线拦截集必须在 SC 里**逐条重放** (SC-22 22bc / 22aj、SC-16 16o / 16p):",
  "- **原位改写通则**: 被**原位改写** (而非新增) 的既有规则行与条件 —— `/proc` 两行 (W11)、`python3 -c` / `node -e` 两行 (W8 / W11 追加名字)、`_sg_compute_credit` 的 tight 判定 (W8 / W11 并入名字组)、**Read/Edit 面路径正则 `:641` (W8 追加名字组, 32 个基线备选)** —— 其基线拦截集必须在 SC 里**逐条重放** (SC-22 22bc / 22aj、SC-16 16o / 16p、SC-18 18j / 18k):")
E("`secret-guard.sh:21-23`「Phase 2 would add PostToolUse hook … style env lines + redacts —」(三行整句:",
  "`secret-guard.sh:8` 的「It covers the ~100 most common patterns」(基线 145 行规则、目标 149 行: 数字删去且**不得**换成新的数量字面; 句子跨两行注释, 判据先把注释行拼成一句再查: 28o); `secret-guard.sh:21-23`「Phase 2 would add PostToolUse hook … style env lines + redacts —」(三行整句:")
E("28l 含 `updatedToolOutput`, 且 `exposes no field to` 与 `version-dependent behaviour` 都不在文件里。",
  "28l 含 `updatedToolOutput`, 且 `exposes no field to` 与 `version-dependent behaviour` 都不在文件里; 28o 头注释前 25 行里 `~100` 不在文件里、`most common patterns` 在场且拼合后的句子不含数量字面。")

# ---------------------------------------------------------------- Success Criteria preface
E("(共 411 行, 其中 SC-30 一行不执行)。", "(共 @ROWS@ 行, 其中 SC-30 一行不执行)。")
E("(汇总见 `writer-v4-proto/` 与 `writer-v3-proto/` 的 mut_summary 文件; v4 另把 W9 的条目格式规则 (剥空白、字节长度)、W4 的 16 字符门槛与两个哈希工具回退腿、既有 `json-secret-field` 的键表与既有提取链的各分支、tight 判定的每个成员各自补了成员行)。",
  "(汇总见 `writer-v5-proto/` 的 mut_summary 文件; W9 的条目格式规则 (剥空白、BOM、字节长度)、W4 的 16 字符门槛与两个哈希工具回退腿、既有 `json-secret-field` 的键表与既有提取链的各分支、tight 判定的每个成员、Read/Edit 面路径正则的 32 个基线备选各有成员行)。")
E("每个 (既有 tag, 分类器步骤) 对 (7l / 7m)、阶段切分不识别引号 / 全不切 (19z / 19aa)、执行了命令文本或条目的 eval 式实现 (19ab / 21z / 23i)、字符类与 locale 相关 (32d)、tight 拷贝与规则行漂移 (22bm) 各有对应的坏实现并证明转红。",
  "每个 (既有 tag, 分类器步骤) 对 (7l / 7m)、扩展另写阶段切分而不复用内建判定 (19af)、偏移与切片单位不一致 (19ag)、字节语义依赖调用方导出 `LC_ALL` (19ah / 19am)、执行了命令文本或条目的 eval 式实现 (19ab / 21z / 23i)、字符类与 locale 相关 (32d / 32e)、tight 拷贝与规则行漂移 (22bm)、包裹下的转储并入 tight (22br)、NUL 视图替换基线视图 (1e / 1f)、无界前缀与平方级取值 (34a / 34b / 34c) 各有对应的坏实现并证明转红。")

# ---------------------------------------------------------------- SC-1
L("- **SC-1** (`baseline-failing` ×4, W1):",
  "- **SC-1** (`baseline-failing` ×5 + `reverse-guard` ×2, W1): Read 真实信封, 内容为 `AWS_ACCESS_KEY_ID=<AKIA+16>` / json:client_secret=<32 alnum> → 期望 `aws-access-key-id=1` / `json-secret-field=1`; **1c / 1d**: NUL 分隔的进程环境 (`HOME` / `PATH` / `DB_PASSWORD` / `LANG` / `JWT_SECRET` / `API_TOKEN` 六条记录, 每条以 NUL 结尾; 1c 经 Read 真实信封、1d 经 Bash 信封 —— `/proc/<pid>/environ` 与 `env -0` 的形态) → 期望 `env-line-secret-keyword=3`, 另允许至多一个 `kv-secret-assign` (粘连的基线视图 D 可能为最后一条记录多计一次: 同一凭据被两个视图各看一次; 计数只多不少, 3 个 env 行命中不可少); **1e / 1f**: UTF-16LE 形态的文本 (每个 ASCII 字符后夹一个 NUL: AWS 密钥行 / env 行 / `token <PAT>` 行 / JSON client_secret 四形) 经 Bash (1e, `reverse-guard`) 与 Read (1f) 信封 → 与对应 ASCII 文本相同的检出 (`aws-access-key-id=1` / `env-line-secret-keyword=1` / `github-pat=1` / `json-secret-field=1`); **1g** (`reverse-guard`): 内容只是字面写了 `\\u0000` 这六个字符 (没有 NUL 字节) 并带一个 AWS 密钥 → 仍是 `aws-access-key-id=1` (不翻倍)。**基线: 1a–1d、1f 静默 (Read 不扫), 1e / 1g 相符**。怎么会红: 提取链没加 `file.content` 或加错层级; **没有第二个 NUL 视图** (1c / 1d; `nul_off` 转红); **NUL 视图替换了基线视图** (1e / 1f: UTF-16 形态被拆成每字符一行而静默 —— 对输入的任何变换都必须是既有检出的超集); 把 NUL 换成空格 (1c / 1d 的 tag 变成 `kv-secret-assign`); 第二个视图只凭预检就追加而不与第一个比较、或对每个输入都追加 (1g 与 SC-2 的计数翻倍转红)。")

# ---------------------------------------------------------------- SC-9 / SC-10
E("(`allow-guard` ×25, W2)", "(`allow-guard` ×26, W2)")
E("**9y** 路径形起头标记的 4 个成员 (`/` `~/` `./` `../`, 值含三类字符, 所以只有路径规则能让它们静默)。**基线 25/25**。",
  "**9y** 路径形起头标记的 4 个成员 (`/` `~/` `./` `../`, 值含三类字符, 所以只有路径规则能让它们静默); **9z** kv-secret-assign 的左边界: 紧贴在小写字母之后的大写键、紧贴在小写前缀与下划线之后的键都不是键起点 (`xJWT_…=<值>`、`abc_API_…=<值>`)。**基线 26/26**。")
E("或路径形缺任一起头标记 (9y)。", "或路径形缺任一起头标记 (9y)、kv 没有左边界 (9z: 从词中间读出键)。")
E("(`known-limit` ×11 + `baseline-failing` ×1, W2)", "(`known-limit` ×14 + `baseline-failing` ×1, W2)")
E("**10k** 单字符类的第三种 (40 个大写字母; 10a 小写、10b 数字) → 静默。**基线 11/11**。",
  "**10k** 单字符类的第三种 (40 个大写字母; 10a 小写、10b 数字) → 静默; **10m** Forgejo / Gitea 容器环境变量覆写 `FORGEJO__<section>__<KEY>` / `GITEA__<section>__<KEY>` (section 小写; compose 环境列表、compose 环境映射、docker inspect 的 Env 数组三形, 各经 Bash 与 Read 两种信封: 6 个独立运行) → 静默; **10n** 关键字前有 70 个大写字符的键 (超过 64 的上界) → 静默; **10o** 紧贴字母的旗标 (`abc--token=<值>`) 与参数名有 45 个字符的旗标 (超过 40 的上界) → 静默。**基线 14/14**。")
E("怎么会红: 有人覆盖了该类 (须同步更新已知限制; 变异实测: kv 键接受小写 → 10d、10j 红);",
  "怎么会红: 有人覆盖了该类 (须同步更新已知限制; 变异实测: kv 键接受小写 → 10d、10j、10m 红; 键 / 旗标名的上界或左边界被去掉 → 10n / 10o 红, 同时 34b 红);")

# ---------------------------------------------------------------- SC-18
E("怎么会红: `:641` 只改了 Bash 面, 名字组两面漂移",
  "**18j / 18k** (`reverse-guard`): 被原位改写的 `:641` 路径正则保留基线的 32 个备选 —— 每个备选一条只命中它的路径 (`.env`、`.envrc`、`secrets/` `credentials/` 目录、`id_rsa` / `id_ed25519` / `id_ecdsa` / `.ssh/id_*`、`.pem` `.key` `.gpg` `.age` `.p12` `.pfx` `.jks`、`.tfstate` 及其 `.backup`、`.aws` 的 credentials / config、`.kube/config`、`kubeconfig`、`.docker/config.json`、`service-account` / `gcp-key` / `firebase` 的 json、`known_hosts`、`secret-token` / `master-key` / `encryption-key`、三个 claude-config 名), Read (18j) 与 Edit (18k) 各 32 个独立运行 → exit 2, **基线 32/32**。怎么会红: `:641` 只改了 Bash 面, 名字组两面漂移")
E("或新拦截绕开了 nonce 逃生口。", "或新拦截绕开了 nonce 逃生口; 为并入名字组而重写那条正则时丢了基线的任一备选 (18j / 18k 逐成员转红: 丢 16 个备选的实现转红 16 个成员, 丢单个备选转红对应成员)。")
