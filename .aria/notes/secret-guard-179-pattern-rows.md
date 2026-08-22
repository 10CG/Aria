# #179 TASK-007 — risky_patterns 路径清单型行枚举 (aria @ 400f0bc, hooks/secret-guard.sh :639-800)

> 前置白名单 (What.3) 适用面的机械枚举。判据: 敏感名 token 紧跟在 `[^|]*` (任意位置匹配) 之后, 处于 reader 参数位置 —— 这正是 issue 复现与两次活体误拦 (`(\.bashrc|` / `(\.env|` 正则字面量位置) 的 FP 形状。

## 实现期发现 (→ proposal 附录 Amendment-1)

spec What.3 的单一白名单 {串首, 空白, `"`, `'`, `=`, `/`} 按字面套到**后缀型**敏感名 (`\.env` `\.envrc` `\.pem` `\.key` …) 会放走合法前缀: `cat prod.env` (前缀 `d`) / `cat app.env.production` / `find -name '*.env'` (前缀 `*`) —— 这些是真实 env 文件, 今天被拦, 套字面白名单后**漏报回归**; SC-5 守卫只覆盖 shell-rc 全名形态, 抓不到。⇒ 白名单按两族定义, 各自仍是单一白名单 (无排除集):

| 族 | 敏感名形态 | 前置白名单 | 理由 |
|---|---|---|---|
| **全名型** | `.bashrc` `.zshrc` … / `.claude/settings.json` … (完整 basename) | `(^\|[[:space:]"'=/])` | 合法读取时 basename 前只能是路径分隔/空白/引号/`=`; `x.bashrc` 不是该文件 |
| **后缀型** | `.env` `.envrc` `.pem` `.key` `.p12` `id_rsa` … (可作 basename 尾段) | `(^\|[[:space:]"'=/*A-Za-z0-9_.-])` | `prod.env` / `*.env` / `a.b.env` 合法; 仍排除 `(` `\|` `\` `[` `{` 等正则/alternation 上下文字符 |

两族对 issue 复现的 FP 前缀 (`(`, `|`, `\`) 都不触发 ⇒ SC-4 全部形态在两族下均放行; 差异只在后缀族额外允许词字符与 `*`。

## 适用行 (本 spec 改动面, 13 行 + 新增 1 行)

| 行 | 族 | 敏感名组 (截) | 备注 |
|---|---|---|---|
| :685 | 后缀 | `\.env(\b\|/\|$\|[[:space:]])` | cat |
| :686 | 后缀 | `\.envrc` | cat |
| :687 | 后缀 | `\.env` | head/tail/less/more — **活体误拦命中行** |
| :700 | 后缀 | `id_rsa\|…\|\.pem\|\.key\|…` | 多 reader; `id_rsa` 亦可为后缀 (`my_id_rsa`) 归后缀族 |
| :709 | 全名 | `\.bashrc\|…\|/etc/profile` | shell-rc, issue 复现行 |
| :710 | 全名 | 同上 (ssh 包装) | |
| :724 | 后缀 | `\.env` | strings |
| :725 | 后缀 | `\.env` | hexdump |
| :726 | 后缀 | `\.env` | od |
| :727 | 后缀 | `\.env` | awk |
| :728 | 后缀 | `\.env` | perl |
| :785 | 后缀 | `(…\|\.env\|…)` + 本 spec 扩 claude-config | python3 -c (源组混合, claude 条目为全名但同组, 取后缀族宽集不损安全: 全名前出现词字符本就不匹配真路径) |
| :786 | 后缀 | 同上 | node -e |
| **新增** | 全名 | `\.claude/settings\.json\|\.claude/settings\.local\.json\|\.claude\.json` | TASK-002 |

## 明确不适用 (FP 形状不同或已自锚, 本 spec 不动)

- `/`-根路径行 :714 :715 (`/(var/)?run/secrets/`): token 以 `/` 起头, 自锚, 正则字面量里写 `(/run/secrets` 极罕见。
- token 在 pattern **起始**的行 :721 :722 :735 :737 :738: FP 形状是「`.env` 出现在管道/重定向前的任意位置」, 非 reader 参数位置, 属另一类 (若治需独立评估)。
- find/xargs 组合行 :718 :719 :720 :723: 多 token 已互相约束 (`find … -name … -exec cat`), 正则字面量同时含这些 token 的概率可忽略; 且 `-name '*.env'` 的 `*` 前缀本就是该行主形态。
- 重定向读取行 :731-:734: `<` 语境自锚。
- ssh/kubectl 远程行 :741 :742 :759: 远程命令串语境, 暂不动 (保守)。
- 命令注入型 (base64/sops/age/gpg/openssl/jq 链/云 CLI): 无路径 token, 不适用。

## 核验

- 本枚举由 TASK-010 实现时逐行应用; SC-4 的 `.env` 面 fixture 打 :687 行; SC-5 新增守卫 `cat prod.env` / `find . -name '*.env' -exec cat {} \;` (后缀族合法前缀不得放走) — 见 proposal Amendment-1 与 TASK-008 扩充。
