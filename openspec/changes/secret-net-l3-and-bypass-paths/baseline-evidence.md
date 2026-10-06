# baseline-evidence: secret-net-l3-and-bypass-paths

> 本文件 = 同目录 `baseline_probe.py` 在冻结基线上的实跑 stdout (原样粘贴, 未改一个字符) + 复现说明。`proposal.md` 里 SC 的「基线」值都取自下方输出 (SC-30 除外, 它不由本探针执行)。

## 基线与环境

- 基线: aria `268da8f39d8bc33967e7cdaa5681e3a221fb9e4b` (= v1.74.1); standards `2bc1c4c619c5125a1bb2963864c1683fd9a87739`; 主仓 `0748dbc` (起草时)。
- 被测文件指纹见输出第 2–6 行 (sha256 前 16 位): `hooks/secret-guard.sh` `448b1f71a2af06d7`、`hooks/secret-scan.sh` `c5f53f7a164fa72e`、`hooks/tests/secret-guard.test.sh` `72f8e7d5d58a4b80`、`hooks/tests/secret-scan.test.sh` `78e0e4ca15078177`、`standards/conventions/secret-hygiene.md` `dcf203f1f25ef0c0`。
- 环境: Linux 6.17.9-1-pve, Python 3.11.2, GNU bash 5.2.15 (默认 bash), jq 1.6, GNU grep 3.8, GNU sed 4.9, perl 5.36.0; 本机无 zsh; `C.UTF-8` locale 可用; 真 GNU bash 3.2.57(2) 见下节。第二个 locale `en_US.UTF-8` (本机 `locale -a` 列出 `en_US.utf8`; SC-32 32d 用)。实跑日期 2026-10-06。

## 取得真 bash 3.2 (`WPA_BASH32`)

SC-29 29h / 29i 与 SC-32 32c / 32d 需要一个真 bash 3.2 (Debian / Ubuntu 的 `bash` 包是 5.x, macOS 自带的 3.2.57 不可在 Linux 容器里取得)。无 root、可联网时从源码构建, 约 4 分钟:

```bash
curl -fLO https://ftp.gnu.org/gnu/bash/bash-3.2.tar.gz     # sha256 26c99025b59e30779300b68adb764f824974d267a4d7cc1b347d14a2393f9fb4
tar xzf bash-3.2.tar.gz && cd bash-3.2
for n in $(seq -w 1 57); do                                 # 官方补丁 bash32-001 .. bash32-057, 在 bash-3.2 目录内逐个 patch -p0
  curl -fLO https://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-0$n && patch -p0 < bash32-0$n
done
# 补丁改了 parse.y (001 / 003 / 021 / 037 / 053 / 055 / 057), make 会用 bison 重生成 y.tab.c。无 root 时: 取 Debian 的 bison 与 m4 两个 .deb,
# 用 dpkg -x 解到私有目录, 把其 usr/bin 放到 PATH 最前 (本次用的 bison 3.8.2 / m4 1.4.19)
./configure --prefix=<X>/inst --without-bash-malloc && make
./bash --version                                             # GNU bash, version 3.2.57(2)-release (x86_64-unknown-linux-gnu)
export WPA_BASH32=$PWD/bash                                  # 探针只需要这个二进制的路径; 它把 PATH 里的 `bash` 与 `#!/usr/bin/env bash` 都指向它
```

## 怎么跑

1. 布局: 探针按 `<aria>/../standards` 找 standards, 按自身所在目录找 `proposal.md` 与 `baseline-evidence.md`。本次把 `/home/dev/Aria/aria` 与 `/home/dev/Aria/standards` 用 `cp -a` 复制到实验目录 `<X>/base/` 下并删去两处 `.git` 文件 (子模块 gitfile), 探针、`proposal.md` 与本文件放在同一目录 (即落盘后的 `openspec/changes/secret-net-l3-and-bypass-paths/`)。
2. 命令 (本输出): `WPA_BASH32=<bash 3.2 路径> TMPDIR=<X>/tmp python3 baseline_probe.py <X>/base/aria`。`TMPDIR` 只决定探针私有临时目录的位置 (结束时删除), 不进输出。不带 `WPA_BASH32` 时 29h / 29i / 32c / 32d 四行打印 `not-run` (match 为 `n/a`), 末尾「rows not run」与两条形态行点名这四行 (基线形态仍是 `holds`, 带 `[4 leg row(s) not run]` 注记; 目标形态在有未运行行时只会是 `not established`); 除这四行与末尾三行外, 输出与本输出逐字节相同。验收模式 `WPA_REQUIRE_ALL=1`: 任何本应运行的行是 `n/a` 即 exit 3 (含: 缺真 bash 3.2、root 下的 20g、缺 `sha256sum` 或 `shasum` 的 12o、第二个 locale 装不上也构造不了的 32d)。第二个 locale 由 `WPA_LOCALE_B` 指定 (默认 `en_US.UTF-8`); 系统没装时探针用 `localedef -i en_US -f UTF-8 <私有目录>/en_US.utf8` 构造一次并设私有 `LOCPATH` (本机实测可行: 构造出的 locale 同样使真 bash 3.2.57 的 `[[ QWERTY == *[a-z]* ]]` 为真)。
3. 带 `WPA_BASH32` 连跑两次, stdout 逐字节相同 (sha256 前 16 位 `e588f9e8a57ed720`, 86047 字节), stderr 为空; 不带 `WPA_BASH32` 跑一次: sha256 前 16 位 `bd8327a7e971cc4e`, 86021 字节, stderr 为空, 基线形态同样 `holds`。空闲主机上单次约 10–12 分钟 (两个测试套件各在默认 bash 与 3.2 下跑一遍, 占大头; 32c / 32d 各把 hook 直调行再跑两遍; 两个探针运行并发或主机负载高时可到 25 分钟以上)。
4. 比对注意: 若 standards 不在 `<aria>/../standards`, SC-26 / SC-27 / SC-28 中读 standards 的行会打印 `standards-absent`; 若探针旁没有 `proposal.md` 或本文件, SC-15 15e / 15g 打印 `…-absent`。本输出只在复制出的副本上实测过; 对真 checkout 的 `aria/` 跑时, 套件同样在去掉 `.git` 的私有副本里执行。SC-20 20g (不可读文件) 在 root 下不可构造, 本输出由非 root 用户产生。

## 读法

- 列: SC │ 用例 │ 类别 │ 输入形态 (占位描述) │ 期望 (目标态) │ 实得 │ 符合 (`yes` / `no`; `n/a` = 本探针不执行或在本环境不可构造)。共 411 行 (类别计数见输出末尾)。
- **基线形态**: `baseline-failing` 与 `doc-sync` 行应全部 `no`, 其余类别 (`reverse-guard` / `allow-guard` / `known-limit` / `zero-regression`) 应全部 `yes`; 输出末尾的形态行由探针机算该不变量 —— 本次 `holds`。实现完成后同一探针应输出「target shape … holds」。
- SC-30 一行不执行 (`n/a`), 理由见 `proposal.md` SC-30。SC-32 32c 一行在基线上比对 361 个 hook-direct 行, 32d 对同一批行在第二个 locale 下再跑默认 bash 与真 bash 3.2 各一遍并逐行比对。
- **多用例行** (`l3m` / `l1m` 一类) 是同一类别下若干独立 hook 运行的 AND, `actual` 列逐个列出, 红了仍能指出是哪一个; **枚举行** (`actual` 为 `N/N as expected`, 红了点名前 6 个出错的成员) 是同一类的一个枚举集合, 每个成员一次独立 hook 运行。
- 确定性措施: 像凭据的值在进程内由 `secrets` 生成, 生成时保证字符类与首字符 / 形态性质 (判定不随随机值变化); hook 的环境变量从零构造 (不继承调用方的 `CLAUDE_PROJECT_DIR` 等); 测试套件在去掉 `.git` 的私有副本里跑、设 `GIT_CEILING_DIRECTORIES`、PATH 中隐去 zsh, 因此 `secret-guard.test.sh` 里依赖 git 历史的测试内 SC-9a / SC-8 与 zsh 用例被跳过 (实得里的 `581/582` 与唯一 FAIL 即此伪影, 见 `proposal.md` SC-29)。
- Rule #7: 输出只有退出码、是否告警、tag 名与计数, 没有任何值; 输入形态一律用占位描述。

## 实跑 stdout (原样)

```text
baseline_probe.py -- openspec change secret-net-l3-and-bypass-paths
measured hooks/secret-guard.sh sha256[:16] = 448b1f71a2af06d7
measured hooks/secret-scan.sh  sha256[:16] = c5f53f7a164fa72e
measured hooks/tests/secret-guard.test.sh sha256[:16] = 72f8e7d5d58a4b80
measured hooks/tests/secret-scan.test.sh  sha256[:16] = 78e0e4ca15078177
measured standards/conventions/secret-hygiene.md sha256[:16] = dcf203f1f25ef0c0
proposal.md next to this probe: present
columns: SC │ case │ category │ input shape (placeholders) │ expected (target) │ actual │ match

SC-1 │ 1a │ baseline-failing │ Read real envelope file.content: AWS_ACCESS_KEY_ID=<AKIA+16> │ alert m=1 {aws-access-key-id=1} │ silent │ no
SC-1 │ 1b │ baseline-failing │ Read real envelope file.content: json:client_secret=<32 alnum> │ alert m=1 {json-secret-field=1} │ silent │ no
SC-1 │ 1c │ baseline-failing │ Read real envelope file.content = a NUL-separated process environment (the /proc/<pid>/environ shape): HOME / PATH / DB_PASSWORD / LANG / JWT_SECRET / API_TOKEN records, NUL after each │ alert m=3 {env-line-secret-keyword=3} │ silent │ no
SC-1 │ 1d │ baseline-failing │ Bash real envelope stdout = the same NUL-separated records (the `env -0` shape): bash command substitution would drop the NULs and glue the records into one line │ alert m=3 {env-line-secret-keyword=3} │ silent │ no
SC-2 │ 2a │ reverse-guard │ Read legacy envelope {content}: AWS_ACCESS_KEY_ID=<AKIA+16> │ alert m=1 {aws-access-key-id=1} │ alert m=1 {aws-access-key-id=1} │ yes
SC-2 │ 2b │ reverse-guard │ Bash real envelope {stdout,...}: AWS_ACCESS_KEY_ID=<AKIA+16> │ alert m=1 {aws-access-key-id=1} │ alert m=1 {aws-access-key-id=1} │ yes
SC-2 │ 2c │ reverse-guard │ Bash legacy envelope {output}: AWS_ACCESS_KEY_ID=<AKIA+16> │ alert m=1 {aws-access-key-id=1} │ alert m=1 {aws-access-key-id=1} │ yes
SC-2 │ 2d │ reverse-guard │ Write real envelope {content,...}: AWS_ACCESS_KEY_ID=<AKIA+16> │ alert m=1 {aws-access-key-id=1} │ alert m=1 {aws-access-key-id=1} │ yes
SC-2 │ 2e │ reverse-guard │ legacy envelope {tool_result:{content}}: AWS_ACCESS_KEY_ID=<AKIA+16> (the 4th branch of the extraction chain) │ alert m=1 {aws-access-key-id=1} │ alert m=1 {aws-access-key-id=1} │ yes
SC-2 │ 2f │ reverse-guard │ legacy envelope {tool_result:{output}}: AWS_ACCESS_KEY_ID=<AKIA+16> (the 5th branch of the extraction chain) │ alert m=1 {aws-access-key-id=1} │ alert m=1 {aws-access-key-id=1} │ yes
SC-3 │ 3a │ known-limit │ Edit real envelope (newString/structuredPatch): AWS_ACCESS_KEY_ID=<AKIA+16> │ silent │ silent │ yes
SC-3 │ 3b │ known-limit │ Bash tool_response as bare string: error: AWS_ACCESS_KEY_ID=<AKIA+16> │ silent │ silent │ yes
SC-4 │ 4a │ baseline-failing │ json:token=<40 hex> (2026-08-20 incident shape) │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4b │ baseline-failing │ json:token=<40 b64url> (space after colon) │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4c │ baseline-failing │ json:sha1=<40 hex> (Forgejo PAT creation) │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4d │ baseline-failing │ pretty-printed multi-line json:token=<40 hex> │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4e │ baseline-failing │ json:registration_token=<40 alnum> │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4f │ baseline-failing │ json:jwt_secret=<43 b64url> │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4g │ baseline-failing │ json:auth_token=<40 alnum> │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4h │ baseline-failing │ full Forgejo PAT-create response (sha1=<40 hex> + token_last_eight=<8 hex>) │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4i │ baseline-failing │ json:Token=<40 hex> (capitalised single-word key) │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4j │ baseline-failing │ json:apiKey=<32 alnum> (camelCase) │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4k │ baseline-failing │ json:ClientSecret=<40 alnum> (PascalCase) │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4l │ baseline-failing │ json Env map JWT_SECRET=<44 b64> (Nomad/compose uppercase key) │ alert m=1 {json-env-secret-key=1} │ silent │ no
SC-4 │ 4m │ baseline-failing │ pretty json:DB_PASSWORD=<20 alnum> (uppercase key) │ alert m=1 {json-env-secret-key=1} │ silent │ no
SC-4 │ 4n │ baseline-failing │ json:token=<44-char std-b64 whose first char is '/'> (the path-form rule must not swallow a b64 value): padded with '=' (`openssl rand -base64 32`) / unpadded with a '+' inside; both carry a second '/' by construction │ padded=alert m=1 {json-credential-field=1}; unpadded-plus=alert m=1 {json-credential-field=1} │ padded=silent; unpadded-plus=silent │ no
SC-4 │ 4o │ baseline-failing │ json:token=<40 letters, upper+lower, no digit> (entropy floor = two classes, not 'must hold a digit') │ alert m=1 {json-credential-field=1} │ silent │ no
SC-4 │ 4p │ baseline-failing │ every JSON key name of the closed table (17 stems x allowed spellings = 58 names) with a 40-char value: json-credential-field=1 (json-secret-field=1 for the 8 lower-case spellings the existing tag consumes first) │ 58/58 as expected │ 8/58 as expected; wrong: auth_token, authToken, AuthToken, authtoken, api_token, apiToken, ... │ no
SC-4 │ 4r │ baseline-failing │ value-length floor, counted side: exactly 16 characters (two or more classes) are counted by each of the 6 new tags │ 6/6 as expected │ 0/6 as expected; wrong: json, json-env, kv, auth-header, cf-header, cli-flag │ no
SC-4 │ 4s │ baseline-failing │ json-env-secret-key keyword set: each of the 10 keywords, as the whole upper-case key and embedded in `SVC_<KW>_V2`, with a 24-char value │ 20/20 as expected │ 0/20 as expected; wrong: SECRET, SECRET-embedded, PASSWORD, PASSWORD-embedded, PASSWD, PASSWD-embedded, ... │ no
SC-4 │ 4t │ baseline-failing │ entropy floor = at least two of the three character classes, each PAIR counted: lower + upper / lower + digit / upper + digit (24 characters, json:token); symbols are not a class (SC-9 9p, SC-10 10a / 10b / 10k) │ 3/3 as expected │ 0/3 as expected; wrong: lower+upper, lower+digit, upper+digit │ no
SC-5 │ 5a │ baseline-failing │ JWT_SECRET = <44 std-b64> (spaces around =, 10CG/aria-plugin#203 leak form) │ alert m=1 {kv-secret-assign=1} │ silent │ no
SC-5 │ 5b │ baseline-failing │ JWT_SECRET = <43 b64url> │ alert m=1 {kv-secret-assign=1} │ silent │ no
SC-5 │ 5c │ baseline-failing │ SECRET_KEY = <64 alnum> │ alert m=1 {kv-secret-assign=1} │ silent │ no
SC-5 │ 5d │ baseline-failing │ PASSWD = <20 alnum> (Forgejo [database]) │ alert m=1 {kv-secret-assign=1} │ silent │ no
SC-5 │ 5e │ baseline-failing │ LFS_JWT_SECRET = <43 b64url> │ alert m=1 {kv-secret-assign=1} │ silent │ no
SC-5 │ 5f │ baseline-failing │ export API_TOKEN=<32 alnum> │ alert m=1 {kv-secret-assign=1} │ silent │ no
SC-5 │ 5g │ baseline-failing │ JWT_SECRET="<44 b64>" (dotenv double-quoted) │ alert m=1 {kv-secret-assign=1} │ silent │ no
SC-5 │ 5h │ baseline-failing │ JWT_SECRET='<44 b64>' (dotenv single-quoted) │ alert m=1 {kv-secret-assign=1} │ silent │ no
SC-5 │ 5i │ baseline-failing │ export API_TOKEN="<32 alnum>" │ alert m=1 {kv-secret-assign=1} │ silent │ no
SC-5 │ 5j │ baseline-failing │ indented YAML map  JWT_SECRET: <44 b64> (compose environment) │ alert m=1 {kv-secret-assign=1} │ silent │ no
SC-5 │ 5k │ baseline-failing │ app.ini fragment with 5 secrets (LFS_JWT_SECRET/JWT_SECRET/INTERNAL_TOKEN(JWT)/SECRET_KEY/PASSWD) │ alert m=5 {jwt=1 kv-secret-assign=4} │ alert m=1 {jwt=1} │ no
SC-5 │ 5l │ baseline-failing │ JWT_SECRET = <44-char std-b64 whose first char is '/'> (`openssl rand -base64 32` hits '/' first in 1 of 64; a loose path reading would drop it): padded with '=' / unpadded with a '+' inside; both carry a second '/' by construction │ padded=alert m=1 {kv-secret-assign=1}; unpadded-plus=alert m=1 {kv-secret-assign=1} │ padded=silent; unpadded-plus=silent │ no
SC-5 │ 5m │ baseline-failing │ JWT_SECRET = <43 b64url> whose first char is '-' / '_' (valid url-safe b64 first characters) │ dash=alert m=1 {kv-secret-assign=1}; underscore=alert m=1 {kv-secret-assign=1} │ dash=silent; underscore=silent │ no
SC-5 │ 5n │ baseline-failing │ kv-secret-assign keyword set: each of the 10 keywords, as the whole upper-case key and embedded in `SVC_<KW>_V2`, `KEY = <24-char value>` │ 20/20 as expected │ 0/20 as expected; wrong: SECRET, SECRET-embedded, PASSWORD, PASSWORD-embedded, PASSWD, PASSWD-embedded, ... │ no
SC-6 │ 6a │ baseline-failing │ Authorization: token <40 hex> (Forgejo/Gitea PAT header) │ alert m=1 {auth-header-token=1} │ silent │ no
SC-6 │ 6b │ baseline-failing │ curl -s -H "Authorization: token <40 hex>" https://forgejo.example/api/v1/user (command echo) │ alert m=1 {auth-header-token=1} │ silent │ no
SC-6 │ 6c │ baseline-failing │ CF-Access-Client-Secret: <64 hex> │ alert m=1 {cf-access-client-secret=1} │ silent │ no
SC-6 │ 6d │ baseline-failing │ curl -H "CF-Access-Client-Id: <32>.access" -H "CF-Access-Client-Secret: <64 hex>" │ alert m=1 {cf-access-client-secret=1} │ silent │ no
SC-6 │ 6e │ baseline-failing │ Authorization: Basic <b64 of user:pass> │ alert m=1 {auth-header-token=1} │ silent │ no
SC-6 │ 6f │ baseline-failing │ forgejo-runner register --instance https://git.example --token=<40 hex> │ alert m=1 {cli-secret-flag=1} │ silent │ no
SC-6 │ 6g │ baseline-failing │ ps-style line: curl with CF-Access-Client-Id/-Secret + Authorization: token (10CG/Aria#221 shape, L3 side) │ alert m=2 {auth-header-token=1 cf-access-client-secret=1} │ silent │ no
SC-6 │ 6h │ baseline-failing │ HTTP/2 lower-case header names (curl -v prints them lower-case): `authorization: token <40 hex>` / `cf-access-client-secret: <64 hex>` │ authorization=alert m=1 {auth-header-token=1}; cf=alert m=1 {cf-access-client-secret=1} │ authorization=silent; cf=silent │ no
SC-6 │ 6i │ baseline-failing │ cli-secret-flag suffix set: each of the 7 flag-name suffixes, bare (`--<s>=<24>`) and with a prefix (`--svc-<s>=<24>`); and the single-dash spelling (`-token=<24>`) │ 15/15 as expected │ 0/15 as expected; wrong: token, token-prefixed, password, password-prefixed, passwd, passwd-prefixed, ... │ no
SC-6 │ 6j │ baseline-failing │ auth-header scheme words (token / Token / basic / Basic) and header-name spellings (auth: AUTHORIZATION / authorization; cf: 3 spellings; the all-caps cf spelling is consumed first by kv-secret-assign and counted once under that tag), 40-char values │ 10/10 as expected │ 0/10 as expected; wrong: scheme-token, scheme-Token, scheme-basic, scheme-Basic, auth-AUTHORIZATION, auth-authorization, ... │ no
SC-6 │ 6k │ baseline-failing │ value character classes, member by member: kv-secret-assign and cli-secret-flag accept each of `+ / = . _ ~ -` inside a 17-character value; the two header tags accept each of `. _ / + = -` │ 26/26 as expected │ 0/26 as expected; wrong: kv:+, kv:/, kv:=, kv:., kv:_, kv:~, ... │ no
SC-7 │ 7a │ reverse-guard │ JWT_SECRET=<44 b64> (line start, no spaces) │ alert m=1 {env-line-secret-keyword=1} │ alert m=1 {env-line-secret-keyword=1} │ yes
SC-7 │ 7b │ reverse-guard │ INTERNAL_TOKEN = <JWT-shaped> │ alert m=1 {jwt=1} │ alert m=1 {jwt=1} │ yes
SC-7 │ 7c │ reverse-guard │ Authorization: Bearer <32 alnum> │ alert m=1 {bearer-token=1} │ alert m=1 {bearer-token=1} │ yes
SC-7 │ 7d │ reverse-guard │ json:client_secret=<32 alnum> │ alert m=1 {json-secret-field=1} │ alert m=1 {json-secret-field=1} │ yes
SC-7 │ 7e │ reverse-guard │ json:password=<16 alnum> │ alert m=1 {json-secret-field=1} │ alert m=1 {json-secret-field=1} │ yes
SC-7 │ 7f │ reverse-guard │ DB_PASSWORD=<20 alnum> (line start) │ alert m=1 {env-line-secret-keyword=1} │ alert m=1 {env-line-secret-keyword=1} │ yes
SC-7 │ 7g │ reverse-guard │ json:token=<gh-prefixed PAT> (single count) │ alert m=1 {github-pat=1} │ alert m=1 {github-pat=1} │ yes
SC-7 │ 7h │ reverse-guard │ existing tags keep every detection (negative side of W3), on existing keys: values that LOOK like a removed whitelist class -- bare `$name` (lower-case + digits / upper-case + digits / mixed case; the letter after `$` is forced), `$(...)`, an ASCII `...` suffix -- or like a retained class that is not closed / not whole (`<` unclosed), a crypt hash, a single-class value, a marker in the middle, a lower-case marker; and a marker value on the env-line tag │ 11/11 as expected │ 11/11 as expected │ yes
SC-7 │ 7j │ reverse-guard │ boundaries of every RETAINED whitelist branch, on existing keys: the value shares the branch's first or last character but is not the whole form, so it must stay detected -- angle (`>` only / closed early with trailing text / inner `<`), `${` (unclosed / trailing text), `{{` (unclosed / `}}` only / trailing text), `[REDACTED` unclosed, any other bracketed value, a mask with a real tail / two mask characters mixed, an ellipsis in the middle or at the front, a truncated marker │ 15/15 as expected │ 15/15 as expected │ yes
SC-7 │ 7i │ reverse-guard │ json:token=<crypt-hash shape, 60 chars>: some alert must remain (baseline bcrypt-hash; the new json tag must not swallow it silently) │ alert (any tag) │ alert m=1 {bcrypt-hash=1} │ yes
SC-7 │ 7k │ reverse-guard │ the 10 key names of the existing json-secret-field table, each with a 24-char value: json-secret-field=1 (4p pins the 8 names that the new table shares; webhook_secret and encryption_key are pinned only here) │ 10/10 as expected │ 10/10 as expected │ yes
SC-7 │ 7l │ reverse-guard │ scope of the classifier steps 3-5: a single-class value (entropy floor), a path-form value, a dotted identifier chain each stay detected on every EXISTING tag they could silence (env-line, bearer, x-api-key, 4 URL tags: 3 each; json-secret-field: path-form and dotted chain, its single-class case is 7h; jwt: a JWT whose three segments are a dotted identifier chain) │ 24/24 as expected │ 24/24 as expected │ yes
SC-7 │ 7m │ reverse-guard │ scope of the whitelist (step 2): a marker-led value (FAKE_...) stays detected on the existing bearer, x-api-key and 4 URL tags, and a mask value (8 `*`) on the 3 URL tags whose password class admits it -- the whitelist reaches json-secret-field and the 6 new tags only │ 9/9 as expected │ 9/9 as expected │ yes
SC-7 │ 7n │ reverse-guard │ no-execution invariant of the L3 value / classification / fingerprint code: credential-key values that hold a command substitution, back quotes or an arithmetic expansion (5 payloads x Bash and Read envelopes, each `touch`es a private decoy path) are only text for the hook: none of the 10 decoy files exists after the hook has run │ 10/10 as expected │ 10/10 as expected │ yes
SC-8 │ 8a │ baseline-failing │ json:api_key=<anthropic-prefixed key> (one credential, counted once) │ alert m=1 {anthropic-api-key=1} │ alert m=2 {anthropic-api-key=1 json-secret-field=1} │ no
SC-9 │ 9a │ allow-guard │ JWT_SECRET = <your-secret-here> (angle placeholder) │ silent │ silent │ yes
SC-9 │ 9b │ allow-guard │ JWT_SECRET=$(openssl rand -base64 32) │ silent │ silent │ yes
SC-9 │ 9c │ allow-guard │ PASSWD =  (empty value) │ silent │ silent │ yes
SC-9 │ 9d │ allow-guard │ grep -n "JWT_SECRET" /etc/forgejo/app.ini (key name only) │ silent │ silent │ yes
SC-9 │ 9e │ allow-guard │ JWT_SECRET = ${JWT_SECRET} (template reference) │ silent │ silent │ yes
SC-9 │ 9f │ allow-guard │ json:sha=<40 hex> (git commit sha) │ silent │ silent │ yes
SC-9 │ 9g │ allow-guard │ json:commit.id=<40 hex> │ silent │ silent │ yes
SC-9 │ 9h │ allow-guard │ json:token_last_eight=<24 hex> (key outside the closed list; value long enough to pass the 16 floor) │ silent │ silent │ yes
SC-9 │ 9i │ allow-guard │ json:uuid=<uuid> │ silent │ silent │ yes
SC-9 │ 9j │ allow-guard │ json:next_page_token=<24 alnum> (pagination cursor, key outside closed list) │ silent │ silent │ yes
SC-9 │ 9k │ allow-guard │ git log full format (3 x commit <40 hex>) │ silent │ silent │ yes
SC-9 │ 9l │ allow-guard │ curl -H "Authorization: token $FORGEJO_ADMIN_API_TOKEN2" (variable reference, 25 chars, upper case + digit = two character classes, so the entropy floor cannot be what silences it: the `$` is outside the header value character class, so no span forms at all -- this row pins that class, neither the whitelist nor the entropy floor) │ silent │ silent │ yes
SC-9 │ 9m │ allow-guard │ forgejo-runner register --token=$RUNNER_REGISTRATION_TOKEN2 (variable reference, 27 chars incl. `$`, upper case + digit = two character classes: the `$` is outside the flag value character class, no span forms; the entropy floor cannot be what silences it) │ silent │ silent │ yes
SC-9 │ 9n │ allow-guard │ forgejo-runner register --token-file=/run/secrets/runner_token │ silent │ silent │ yes
SC-9 │ 9o │ allow-guard │ SECRET_FILE = /run/secrets/Db2Password (path-like value, 3 char classes) │ silent │ silent │ yes
SC-9 │ 9p │ allow-guard │ SECRET_PROMPT_NAME = release-notes-summary-v (single char class) │ silent │ silent │ yes
SC-9 │ 9q │ allow-guard │ export SECRET_GUARD_ACK_PATH="/home/u/.claude/settings.json" │ silent │ silent │ yes
SC-9 │ 9r │ allow-guard │ prose: set the token in your config file │ silent │ silent │ yes
SC-9 │ 9s │ allow-guard │ docker images --digests line (sha256:<64 hex>) │ silent │ silent │ yes
SC-9 │ 9t │ allow-guard │ Actions yaml  token: ${{ secrets.FORGEJO_TOKEN }} │ silent │ silent │ yes
SC-9 │ 9u │ allow-guard │ docker login -u ci --password-stdin registry.example.com (flag without value) │ silent │ silent │ yes
SC-9 │ 9v │ allow-guard │ code that READS a credential from the environment / settings (dotted identifier chains, 17-34 chars, two char classes): `const JWT_SECRET = process.env.X` / `SECRET_KEY = settings.X` / `API_TOKEN = config.getApiTokenFromVaultService` │ js-const=silent; py-settings=silent; camel-chain=silent │ js-const=silent; py-settings=silent; camel-chain=silent │ yes
SC-9 │ 9w │ allow-guard │ assignments whose value is a FILE PATH (three char classes, 22-47 chars, upper-case first segment too): `/Users/...`, `~/Library/...`, `/run/secrets/...` │ macos-abs=silent; macos-home=silent; dotfile=silent │ macos-abs=silent; macos-home=silent; dotfile=silent │ yes
SC-9 │ 9x │ allow-guard │ closedness of the JSON key table: keys that merely CONTAIN a table stem (tokens / tokenizer / mytoken / auth_tokens / secret_name / password_hint) with a 40-char value stay silent │ 6/6 as expected │ 6/6 as expected │ yes
SC-9 │ 9y │ allow-guard │ path-form lead markers, member by member: a value that starts with `/`, `~/`, `./` or `../`, holds only path characters and at least two `/` (three letter / digit classes, so only the path rule can silence it) is not counted │ 4/4 as expected │ 4/4 as expected │ yes
SC-10 │ 10a │ known-limit │ json:token=<40 lowercase letters> (single char class) │ silent │ silent │ yes
SC-10 │ 10b │ known-limit │ JWT_SECRET = <24 digits> (single char class) │ silent │ silent │ yes
SC-10 │ 10c │ known-limit │ json:token=<12 alnum> (shorter than 16) │ silent │ silent │ yes
SC-10 │ 10d │ known-limit │ YAML lowercase key  password: <16 alnum> │ silent │ silent │ yes
SC-10 │ 10e │ known-limit │ forgejo-runner register --token <40 hex> (space-separated flag) │ silent │ silent │ yes
SC-10 │ 10f │ known-limit │ json:SecretAccessKey=<40 alnum> (AWS PascalCase, outside closed list) │ silent │ silent │ yes
SC-10 │ 10g │ known-limit │ other documented false-negative classes: python-repr dict with single quotes; kv value whose first symbol comes before 16 class chars; JSON text inside a JSON string (escaped quotes) │ py-repr=silent; symbol-early=silent; json-in-json=silent │ py-repr=silent; symbol-early=silent; json-in-json=silent │ yes
SC-10 │ 10h │ known-limit │ value-length floor, silent side: 15 characters are NOT counted by any of the 6 new tags │ 6/6 as expected │ 6/6 as expected │ yes
SC-10 │ 10i │ known-limit │ dot-structured credentials are silent in the 5 new key-shape forms (three dot-separated segments, each starting with a letter, as in Discord-bot-token / signed-cookie shapes): the dotted-identifier-chain exclusion cannot tell them from `process.env.X` │ 5/5 as expected │ 5/5 as expected │ yes
SC-10 │ 10j │ known-limit │ other forms the 6 new tags do not see: JSON-rendered header, python-repr header, URL query parameter, lower-case INI key with / without quotes, Kubernetes `name:` / `value:` pair │ 6/6 as expected │ 6/6 as expected │ yes
SC-10 │ 10k │ known-limit │ json:token=<40 uppercase letters> (single char class) │ silent │ silent │ yes
SC-10 │ 10l │ baseline-failing │ accepted false positives of the new key-shape tags (documented in W2): an upper-case key whose NAME contains a credential keyword but whose VALUE is not a credential, with a value that passes the classifier (two character classes, 16 or more characters, not path-form, not a dotted identifier) -- a URL, a resource name and a policy name as JSON values, a relative path and a resource path as assignment values; red = somebody closed that class, update W2 and this row │ 5/5 as expected │ 0/5 as expected; wrong: json-url, json-resource-name, json-policy-name, kv-relative-path, kv-yaml-resource-path │ no
SC-11 │ 11a │ allow-guard │ json:token=<FAKE_ + 24 alnum> │ silent │ silent │ yes
SC-11 │ 11b │ allow-guard │ json:token=<PLACEHOLDER_FOR_DOCS_ONLY> │ silent │ silent │ yes
SC-11 │ 11c │ allow-guard │ json:token=<NOT-REAL- + 24 alnum> │ silent │ silent │ yes
SC-11 │ 11d │ allow-guard │ json:token=<L2 wrapper placeholder [REDACTED-BY-WRAPPER len=40]> │ silent │ silent │ yes
SC-11 │ 11e │ allow-guard │ json:sha1=<L2 wrapper placeholder> │ silent │ silent │ yes
SC-11 │ 11f │ allow-guard │ json:token=<angle-bracket prose placeholder, >=16 chars> │ silent │ silent │ yes
SC-11 │ 11g │ allow-guard │ json:token=<${VAR} reference> │ silent │ silent │ yes
SC-11 │ 11h │ allow-guard │ json:token=<{{ template }} reference> │ silent │ silent │ yes
SC-11 │ 11i │ allow-guard │ json:token=<16 x *> (mask) │ silent │ silent │ yes
SC-11 │ 11j │ allow-guard │ JWT_SECRET = <FAKE_ + 40 alnum> │ silent │ silent │ yes
SC-11 │ 11k │ allow-guard │ Authorization: token <FAKE + 40 hex> │ silent │ silent │ yes
SC-11 │ 11l │ allow-guard │ --token=<PLACEHOLDER_ + 24 alnum> │ silent │ silent │ yes
SC-11 │ 11m │ baseline-failing │ json:password=<FAKE_ + 24 alnum> (existing key) │ silent │ alert m=1 {json-secret-field=1} │ no
SC-11 │ 11n │ baseline-failing │ json:client_secret=<PLACEHOLDER_VALUE> (existing key) │ silent │ alert m=1 {json-secret-field=1} │ no
SC-11 │ 11o │ baseline-failing │ json:api_key=<NOT-REAL- + 24 alnum> (existing key) │ silent │ alert m=1 {json-secret-field=1} │ no
SC-11 │ 11p │ baseline-failing │ json:password=<[REDACTED]> (existing key) │ silent │ alert m=1 {json-secret-field=1} │ no
SC-11 │ 11q │ baseline-failing │ json:password=<8 x *> (existing key, mask) │ silent │ alert m=1 {json-secret-field=1} │ no
SC-11 │ 11r │ baseline-failing │ json:client_secret=<L2 wrapper placeholder> (existing key) │ silent │ alert m=1 {json-secret-field=1} │ no
SC-11 │ 11s │ baseline-failing │ json:token=<16 alnum + FAKE + 16 alnum> (marker not at value start) │ alert m=1 {json-credential-field=1} │ silent │ no
SC-11 │ 11t │ reverse-guard │ json:password=<12 alnum + !> (existing key, real-looking value) │ alert m=1 {json-secret-field=1} │ alert m=1 {json-secret-field=1} │ yes
SC-11 │ 11u │ reverse-guard │ Token: <gh-prefixed PAT whose body starts with FAKE> (provider tag, no allow-list) │ alert m=1 {github-pat=1} │ alert m=1 {github-pat=1} │ yes
SC-11 │ 11v │ baseline-failing │ document-style placeholders on EXISTING keys stay silent (whole-value forms): angle-bracket prose holding a `$`; crypt prefix + ellipsis; `${VAR}`; `{{ template }}` │ angle-prose=silent; crypt-ellipsis=silent; shell-var=silent; template=silent │ angle-prose=alert m=1 {json-secret-field=1}; crypt-ellipsis=alert m=1 {json-secret-field=1}; shell-var=alert m=1 {json-secret-field=1}; template=alert m=1 {json-secret-field=1} │ no
SC-11 │ 11w │ baseline-failing │ classification cap: 250 assignments whose value is a 16-char mask -> the first 200 spans of the tag are classified (all whitelisted), the 50 beyond the cap are counted unclassified (fail-closed) │ alert m=50 {kv-secret-assign=50} │ silent │ no
SC-11 │ 11x │ baseline-failing │ retained whitelist members not covered by 11m-11r, on an existing key (all silent): marker words NOT_REAL / NOTREAL / REDACTED, `<...>`, `${...}`, `{{ ... }}`, `${{ ... }}`, `[REDACTED-...]`, 16 x `x`, 16 x `X`, a value ending in the unicode ellipsis │ 11/11 as expected │ 0/11 as expected; wrong: marker-NOT_REAL, marker-NOTREAL, marker-REDACTED, angle, brace, tmpl, ... │ no
SC-11 │ 11y │ allow-guard │ whitelist on a NEW tag (json-credential-field, 16+ chars, two or more classes, so only the whitelist can silence them): the 6 marker words, `<...>`, `${...}`, `{{ ... }}`, `[REDACTED-...]`, the unicode ellipsis │ 11/11 as expected │ 11/11 as expected │ yes
SC-11 │ 11z │ baseline-failing │ detection side of the same boundaries on a NEW tag (json-credential-field counts them): `<` unclosed, `${` unclosed, an ASCII `...` suffix, a bare `$name`, `$(...)` │ 5/5 as expected │ 0/5 as expected; wrong: lt16-unclosed, brace-unclosed, dots-ascii, dollar-lower, dollar-cmd │ no
SC-12 │ 12a │ baseline-failing │ json:client_secret=<32 alnum>: log line gets fp=<sha256 hex prefix 8 of the value> │ fp=[sha256-8 of value] │ fp-field-absent │ no
SC-12 │ 12b │ baseline-failing │ json:password=<12 alnum>: value < 16 chars -> fp=L12, no hash in log │ fp=[L12] │ fp-field-absent │ no
SC-12 │ 12c │ baseline-failing │ json:client_secret=<32 alnum> with sha256sum/shasum absent from PATH -> fp=- │ fp=[-] │ fp-field-absent │ no
SC-12 │ 12g │ baseline-failing │ Bearer header line + line-start env assignment: fp items are sha256-8 of the BARE values (not of the span), in scan order (bearer-token tag first, env-line tag second) │ fp=2 items equal-to-expected │ fp-field-absent │ no
SC-12 │ 12h │ baseline-failing │ app.ini fragment with 5 secrets: fp = [jwt value, then the 4 assignment values in text order], each sha256-8 of the bare value │ fp=5 items equal-to-expected │ fp-field-absent │ no
SC-12 │ 12i │ baseline-failing │ 11 env assignments: fp lists exactly the first 10 values (text order), comma-separated │ fp=10 items equal-to-expected │ fp-field-absent │ no
SC-12 │ 12j │ baseline-failing │ the remaining body-extraction forms in one text: gcp key id (quoted 40 hex), postgres URL (password component), X-API-Key header, `Authorization: token`, CF-Access-Client-Secret header, `--token=` flag; fp items = sha256-8 of the BARE values in scan order (gcp, postgres, x-api-key, auth-header-token, cf-access-client-secret, cli-secret-flag) │ fp=6 items equal-to-expected │ fp-field-absent │ no
SC-12 │ 12k │ baseline-failing │ the W4 value-body table, one credential per tag (every provider-prefix tag, the 3 JSON tags, env-line, kv, the 2 header tags, cli flag, 4 URL tags, gcp key id, bearer, bcrypt, the PEM block): the log's fp item is sha256-8 of the body the table names (whole span / after `=` / JSON string value / last word / after the header colon / password component / quoted 40 hex), `-` for a PEM block │ 38/38 as expected │ 0/38 as expected; wrong: jwt, silknode-api-key, anthropic-api-key, openrouter-api-key, openai-api-key, openai-legacy-key, ... │ no
SC-12 │ 12l │ baseline-failing │ the last member of the W4 table: with perl missing from PATH a PEM block is counted by the header-only fallback (tag `pem-header-only`); its fp item is `-` as for the block form │ tag=pem-header-only fp=- │ tag / fp item differ │ no
SC-12 │ 12m │ baseline-failing │ traversal order and the PEM items: a PEM block -- and, with perl missing from PATH, the header-only fallback that counts it -- that sits AFTER a kv credential in the text still records its `-` item FIRST (the PEM pre-scan runs before the pattern list), so the fp field is `-,<sha256-8 of the kv value>` │ block and header-only: fp=- then the kv item │ block differs; header-only differs │ no
SC-12 │ 12n │ baseline-failing │ the 16-character threshold from both sides (json:password): a 15-char value is recorded as `L15` and its hash is not in the log, a 16-char value as sha256-8 of the value │ 2/2 as expected │ 0/2 as expected; wrong: 15-chars, 16-chars │ no
SC-12 │ 12o │ baseline-failing │ each hash tool alone is enough: with `sha256sum` hidden from PATH (only `shasum -a 256` left) and with `shasum` hidden (only `sha256sum` left) the fp item is still sha256-8 of the value (12c: both hidden -> `-`) │ 2/2 as expected │ 0/2 as expected; wrong: sha256sum-hidden, shasum-hidden │ no
SC-12 │ 12d │ reverse-guard │ json:client_secret=<32 alnum>: log/stdout/stderr hold no value nor 8-char fragment │ log=1-line no-plaintext │ log=1-line no-plaintext │ yes
SC-12 │ 12e │ reverse-guard │ json:password=<12 alnum>: same check │ log=1-line no-plaintext │ log=1-line no-plaintext │ yes
SC-12 │ 12f │ reverse-guard │ app.ini fragment with 5 secrets: same check (JWT line alerts at baseline too) │ log=1-line no-plaintext │ log=1-line no-plaintext │ yes
SC-13 │ 13a │ baseline-failing │ Read /x/app.ini holding AWS_ACCESS_KEY_ID=<AKIA+16>: additionalContext names tags + the tool name (no path) │ contains (tags: aws-access-key-id=1; source: Read) │ silent │ no
SC-13 │ 13b │ baseline-failing │ Bash stdout json:client_secret=<32 alnum>: additionalContext names tags + source │ contains (tags: json-secret-field=1; source: Bash) │ addl-lacks-needle │ no
SC-13 │ 13c │ baseline-failing │ Write /x/f.txt holding AWS_ACCESS_KEY_ID=<AKIA+16>: additionalContext names tags + the tool name (no path) │ contains (tags: aws-access-key-id=1; source: Write) │ addl-lacks-needle │ no
SC-13 │ 13d │ reverse-guard │ Bash stdout AWS_ACCESS_KEY_ID=<AKIA+16>: additionalContext with the ` (tags: ...; source: ...)` segment removed is BYTE-EQUAL to the baseline text (full-string equality, not a contains test) │ additionalContext == baseline text + inserted segment │ additionalContext == baseline text + inserted segment │ yes
SC-13 │ 13g │ baseline-failing │ hostile tool_input.file_path (benign / `)` followed by an imperative sentence / newline + a forged hook line / quotes / non-ASCII incl. U+202E / 5000 characters / control characters), Read and Write: the whole additionalContext is EXACTLY the baseline text plus ` (tags: aws-access-key-id=1; source: <Read|Write>)` -- no byte of the path reaches it │ 14/14 as expected │ 0/14 as expected; wrong: Read:benign, Read:paren-then-imperative, Read:newline-forged-line, Read:quotes, Read:non-ascii, Read:overlong, ... │ no
SC-13 │ 13e │ reverse-guard │ Bash stdout AWS_ACCESS_KEY_ID=<AKIA+16>: systemMessage format unchanged │ systemMessage-format-unchanged │ systemMessage-format-unchanged │ yes
SC-13 │ 13f │ reverse-guard │ same input: exit 0, stdout keys exactly {hookSpecificOutput{hookEventName,additionalContext}, systemMessage}, no value echoed │ exit=0 keys-exact no-value │ exit=0 keys-exact no-value │ yes
SC-14 │ 14a │ baseline-failing │ run secret-scan.test.sh with an outer HOME: lines appended to <outer HOME>/.claude/logs/secret-scan.log │ 0 lines │ 33 lines │ no
SC-14 │ 14b │ baseline-failing │ run secret-guard.test.sh with an outer HOME: ack events appended to <outer HOME>/.claude/logs/guard-bypass.log │ 0 events │ 12 events │ no
SC-15 │ 15a │ baseline-failing │ text of hooks/tests/secret-scan.test.sh as Bash stdout │ silent │ alert m=33 {aliyun-access-key-id=1 anthropic-api-key=1 aws-access-key-id=5 basic-auth-url=1 bearer-token=1 discord-webhook=1 env-line-secret-keyword=1 gcp-private-key-id=1 github-pat=1 gitlab-pat=1 json-secret-field=2 jwt=1 mongodb-url=1 openai-api-key=1 pem-private-key-block=5 postgres-url=2 redis-url=1 silknode-api-key=1 slack-webhook=1 stripe-live-secret=2 stripe-webhook=1 x-api-key-header=1} │ no
SC-15 │ 15b │ allow-guard │ text of hooks/tests/secret-guard.test.sh as Bash stdout │ silent │ silent │ yes
SC-15 │ 15c │ allow-guard │ text of hooks/secret-scan.sh as Bash stdout │ silent │ silent │ yes
SC-15 │ 15d │ allow-guard │ text of hooks/secret-guard.sh as Bash stdout │ silent │ silent │ yes
SC-15 │ 15e │ allow-guard │ text of this Spec's proposal.md (next to this probe) as Bash stdout │ silent │ silent │ yes
SC-15 │ 15f │ allow-guard │ text of this probe (baseline_probe.py) as Bash stdout │ silent │ silent │ yes
SC-15 │ 15g │ allow-guard │ text of this Spec's baseline-evidence.md (next to this probe) as Bash stdout │ silent │ silent │ yes
SC-16 │ 16a │ baseline-failing │ sed -n '1,80p' /etc/forgejo/app.ini │ exit=2 │ exit=0 │ no
SC-16 │ 16b │ baseline-failing │ cat /etc/gitea/app.ini │ exit=2 │ exit=0 │ no
SC-16 │ 16c │ baseline-failing │ cat custom/conf/app.ini │ exit=2 │ exit=0 │ no
SC-16 │ 16d │ baseline-failing │ grep -n JWT_SECRET /etc/forgejo/app.ini │ exit=2 │ exit=0 │ no
SC-16 │ 16e │ baseline-failing │ cat /data/gitea/conf/app.ini │ exit=2 │ exit=0 │ no
SC-16 │ 16f │ baseline-failing │ cat /etc/forgejo/app.ini | grep '^JWT_SECRET' │ exit=2 │ exit=0 │ no
SC-16 │ 16g │ baseline-failing │ ssh root@pve 'pct exec 101 -- cat /etc/forgejo/app.ini' │ exit=2 │ exit=0 │ no
SC-16 │ 16h │ baseline-failing │ python3 -c "print(open('/etc/forgejo/app.ini').read())" │ exit=2 │ exit=0 │ no
SC-16 │ 16i │ baseline-failing │ head -n 40 /var/lib/forgejo/custom/conf/app.ini │ exit=2 │ exit=0 │ no
SC-16 │ 16j │ baseline-failing │ awk '/oauth2/,/security/' /etc/forgejo/app.ini │ exit=2 │ exit=0 │ no
SC-16 │ 16k │ baseline-failing │ docker exec forgejo cat /data/gitea/conf/app.ini │ exit=2 │ exit=0 │ no
SC-16 │ 16l │ baseline-failing │ cat /srv/git-forgejo/app.ini │ exit=2 │ exit=0 │ no
SC-16 │ 16m │ baseline-failing │ cat /etc/forgejo/app.ini.bak │ exit=2 │ exit=0 │ no
SC-16 │ 16n │ baseline-failing │ node -e "console.log(require('fs').readFileSync('/etc/forgejo/app.ini','utf8'))" │ exit=2 │ exit=0 │ no
SC-16 │ 16o │ reverse-guard │ the rewritten python3 -c / node -e source rows keep every baseline alternative blocked (/v1/var/, secretsmanager, /secrets/, .env, provider_key, the two claude-config names) for both interpreters │ 14/14 as expected (exit=2) │ 14/14 as expected │ yes
SC-16 │ 16p │ reverse-guard │ tight credit of the claude-config source (rewritten condition): anchored grep / sed / awk / jq shape filters do not count (exit 2 x4); wc / sha256sum / >/dev/null / jq keys still do (exit 0 x4) │ exit=2,2,2,2,0,0,0,0 │ exit=2,2,2,2,0,0,0,0 │ yes
SC-16 │ 16q │ baseline-failing │ every reader of the shared print-reader table (13 of the claude-config row + 16 added = 29) reads app.ini: `<reader> /etc/forgejo/app.ini` │ 29/29 as expected (exit=2) │ 0/29 as expected; wrong: cat, grep, egrep, fgrep, rg, head, ... │ no
SC-16 │ 16r │ baseline-failing │ tight credit of the app.ini family, form by form: each of the 7 name forms with an anchored `| grep '^JWT_SECRET'`, and the other row-level filters on one form (grep -v / sed / cut / awk): none of them counts as credit │ 11/11 as expected (exit=2) │ 0/11 as expected; wrong: /etc/forgejo/app.ini, /etc/gitea/app.ini, custom/conf/app.ini, /data/gitea/conf/app.ini, /var/lib/forgejo/custom/conf/app.ini, /srv/git-forgejo/app.ini, ... │ no
SC-17 │ 17a │ allow-guard │ app.ini neighbours stay allowed: chmod (left boundary), ls, systemctl, grep for the NAME in docs, other applications' app.ini / php.ini, git log, | wc -l, sha256sum, cp │ exit=0,0,0,0,0,0,0,0,0,0 │ exit=0,0,0,0,0,0,0,0,0,0 │ yes
SC-17 │ 17b │ known-limit │ cp /etc/forgejo/app.ini /tmp/x && cat /tmp/x │ exit=0 │ exit=0 │ yes
SC-17 │ 17c │ allow-guard │ right boundary of the name group: `app.ini` followed by a letter / digit / underscore is another file (app.ini.bak is NOT: 16m) │ exit=0,0,0 │ exit=0,0,0 │ yes
SC-17 │ 17d │ known-limit │ KNOWN-LIMIT: reads of app.ini outside the print-reader table stay allowed on the Bash face -- redirects, source, dd / cp / docker cp, perl, xargs / find -exec, directory recursion and file-name globs, git show, a reader not in the table, an upper-case directory name, a backslash path │ 21/21 as expected (exit=0) │ 21/21 as expected │ yes
SC-18 │ 18a │ baseline-failing │ Read /etc/forgejo/app.ini │ exit=2 │ exit=0 │ no
SC-18 │ 18b │ baseline-failing │ Read /var/lib/gitea/custom/conf/app.ini │ exit=2 │ exit=0 │ no
SC-18 │ 18c │ baseline-failing │ Edit /etc/gitea/app.ini │ exit=2 │ exit=0 │ no
SC-18 │ 18d │ baseline-failing │ Read /data/gitea/conf/app.ini │ exit=2 │ exit=0 │ no
SC-18 │ 18e │ allow-guard │ Read of other applications' app.ini / php.ini stays allowed │ exit=0,0 │ exit=0,0 │ yes
SC-18 │ 18f │ baseline-failing │ Read /etc/forgejo/app.ini with SECRET_GUARD_ACK_PATH set but NO nonce marker (the ACK alone is not enough) │ exit=2 │ exit=0 │ no
SC-18 │ 18g │ allow-guard │ Read /etc/forgejo/app.ini with a valid one-shot ACK (path + nonce marker): the escape hatch works for the new block │ exit=0 │ exit=0 │ yes
SC-18 │ 18h │ baseline-failing │ Read / Edit face of the same name group: a capitalised directory (Read), a backup file (Read), the `custom/conf/app.ini` relative form (Read), a Windows backslash path (Read), Edit of app.ini -> exit 2 x5 (the path is lower-cased first) │ exit=2,2,2,2,2 │ exit=0,0,0,0,0 │ no
SC-18 │ 18i │ allow-guard │ right boundary on the Read face too (single definition, two consumers): app.ini followed by a letter / digit / underscore is another file │ exit=0,0,0 │ exit=0,0,0 │ yes
SC-19 │ 19a │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] cat /srv/billing/conf/prod.toml │ exit=2 │ exit=0 │ no
SC-19 │ 19b │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] grep -n key /srv/billing/conf/prod.toml | grep -v '^#' (tight credit) │ exit=2 │ exit=0 │ no
SC-19 │ 19c │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] Read /srv/billing/conf/prod.toml │ exit=2 │ exit=0 │ no
SC-19 │ 19d │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] Edit /srv/billing/conf/prod.toml │ exit=2 │ exit=0 │ no
SC-19 │ 19e │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] cat P | wc -l ; ls -l P (count / listing credit) │ exit=0,0 │ exit=0,0 │ yes
SC-19 │ 19g │ baseline-failing │ [no CLAUDE_PROJECT_DIR; stdin cwd=proj(ok)] cat /srv/billing/conf/prod.toml │ exit=2 │ exit=0 │ no
SC-19 │ 19h │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(missing); stdin cwd=proj(ok)] cat /srv/billing/conf/prod.toml (env var wins) │ exit=0 │ exit=0 │ yes
SC-19 │ 19i │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] f=/srv/billing/conf/prod.toml; cat $f │ exit=2 │ exit=0 │ no
SC-19 │ 19j │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(meta)] cat <entry> for 14 entries, each holding one of \ ^ $ . | ? * + ( ) [ ] { } (entries are LITERAL substrings: unpaired ( [ must not break anything) │ exit=2,2,2,2,2,2,2,2,2,2,2,2,2,2 │ exit=0,0,0,0,0,0,0,0,0,0,0,0,0,0 │ no
SC-19 │ 19k │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(meta)] look-alikes that a regex or glob reading of the entries would hit stay allowed (. * ? + | ( as pattern characters) │ exit=0,0,0,0,0,0 │ exit=0,0,0,0,0,0 │ yes
SC-19 │ 19l │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] cat abc (3-char entry ignored) │ exit=0 │ exit=0 │ yes
SC-19 │ 19m │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(crlf)] cat /srv/crlf/secret.conf (CRLF file) │ exit=2 │ exit=0 │ no
SC-19 │ 19n │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(ok) holding a line !.env] cat .env (extension cannot remove built-ins) │ exit=2 │ exit=2 │ yes
SC-19 │ 19o │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] python3 -c reading /srv/billing/conf/prod.toml (interpreter source group) │ exit=2 │ exit=0 │ no
SC-19 │ 19p │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] entries are case-insensitive on both faces: Read /SRV/BILLING/CONF/PROD.TOML ; cat of the upper-case entry as written ; cat /srv/billing/MIXED.conf │ exit=2,2,2 │ exit=0,0,0 │ no
SC-19 │ 19r │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] echo P; cat P (the first occurrence follows a non-reader, the second a reader) │ exit=2 │ exit=0 │ no
SC-19 │ 19s │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] Read P with SECRET_GUARD_ACK_PATH set but no nonce marker │ exit=2 │ exit=0 │ no
SC-19 │ 19u │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] every reader of the extension's reader set (the 29 print readers + the python3 -c / node -e source groups = 31) reads a listed path │ 31/31 as expected (exit=2) │ 0/31 as expected; wrong: cat, grep, egrep, fgrep, rg, head, ... │ no
SC-19 │ 19v │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(bound_ok): exactly 200 valid entries, exactly 32768 bytes, a 4-char entry and a 200-char entry] the largest accepted file is in effect: cat P / cat <4-char entry> / cat <200-char entry> │ exit=2,2,2 │ exit=0,0,0 │ no
SC-19 │ 19w │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(bound_bad): P + a 201-char entry + a 3-char entry + a symbol-only entry] bad entries are skipped one by one, the valid entry still works: cat P (2) ; cat <201-char entry> (0) ; cat abc (0) ; cat //// (0) │ exit=2,0,0,0 │ exit=0,0,0,0 │ no
SC-19 │ 19x │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] the 64th occurrence of a listed path (63 x `echo P`, then `cat P`) is still checked │ exit=2 │ exit=0 │ no
SC-19 │ 19y │ known-limit │ [CLAUDE_PROJECT_DIR=proj(ok)] KNOWN-LIMIT: occurrences past the 64th are not checked (64 x `echo P`, then `cat P`: padding passes) │ exit=0 │ exit=0 │ yes
SC-19 │ 19t │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] Read P with a valid one-shot ACK (same escape hatch as the built-in names) │ exit=0 │ exit=0 │ yes
SC-19 │ 19z │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] separators inside quotes do not cut a stage: python3 -c / node -e / awk programs holding `;` / `&` / a newline, and quoted `|`: the listed path is blocked (exit 2) wherever the built-in app.ini row blocks the same command shape with the app.ini path (6 shapes x built-in and extension), and in the 2 quoted-pipe shapes (extension only) │ exit=2,2,2,2,2,2,2,2,2,2,2,2,2,2 │ exit=0,0,0,0,0,0,0,0,0,0,0,0,0,0 │ no
SC-19 │ 19aa │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] separators OUTSIDE quotes still cut a stage: a reader in an earlier stage (`;` / `|` / `&` / newline) or after the quoted mention does not make a later mention of the path a read; a bare mention is no read; and a real count pipe that follows a QUOTED separator is still a credit (`cat <path> ";" | wc -l`, as the built-in rows judge it) │ exit=0,0,0,0,0,0,0,0 │ exit=0,0,0,0,0,0,0,0 │ yes
SC-19 │ 19ab │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(canary): entries `$(touch canary-ext-1)`, back-quoted `touch canary-ext-2`, and the glob `gl/st*ar.conf` next to a decoy file, all relative to the hook's cwd] no-execution invariant: the extension only slices and fixed-string-compares, it never evaluates an entry or the command text: ls -la (0) ; cat gl/stxxar.conf (0, the glob is not expanded) ; echo "$(touch canary-ext-3)" (0) ; Read (0) ; Edit (0) and none of the 3 canary files exists afterwards │ exit=0,0,0,0,0 canaries-absent │ exit=0,0,0,0,0 canaries-absent │ yes
SC-19 │ 19ac │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ws): the entry line is P with leading blanks and a trailing blank + tab] leading / trailing white space of an entry is stripped: cat P (2) ; Read P (2) │ exit=2,2 │ exit=0,0 │ no
SC-19 │ 19ad │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(cjk): `a<2 CJK chars>` (7 bytes) and `/srv/<2 CJK chars>/prod`] length counts BYTES and the letter rule counts ASCII letters / digits: an entry holding an ASCII letter or digit is effective: cat /srv/a<2 CJK chars>/x (2) ; cat /srv/<2 CJK chars>/prod (2) │ exit=2,2 │ exit=0,0 │ no
SC-19 │ 19ae │ known-limit │ [CLAUDE_PROJECT_DIR=proj(cjk)] KNOWN-LIMIT: an entry without any ASCII letter or digit (here 4 CJK characters) is skipped silently: cat /srv/<4 CJK chars>/x (0) │ exit=0 │ exit=0 │ yes
SC-20 │ 20a │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(missing): file absent] extension ignored on both faces, built-ins intact: cat P (0) ; cat .env (2) ; Read P (0) ; Read /x/.env (2) │ exit=0,2,0,2 │ exit=0,2,0,2 │ yes
SC-20 │ 20b │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(dir): path is a directory] extension ignored on both faces, built-ins intact: cat P (0) ; cat .env (2) ; Read P (0) ; Read /x/.env (2) │ exit=0,2,0,2 │ exit=0,2,0,2 │ yes
SC-20 │ 20c │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(dangling): dangling symlink] extension ignored on both faces, built-ins intact: cat P (0) ; cat .env (2) ; Read P (0) ; Read /x/.env (2) │ exit=0,2,0,2 │ exit=0,2,0,2 │ yes
SC-20 │ 20d │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(nul): file holds a NUL byte] extension ignored on both faces, built-ins intact: cat P (0) ; cat .env (2) ; Read P (0) ; Read /x/.env (2) │ exit=0,2,0,2 │ exit=0,2,0,2 │ yes
SC-20 │ 20e │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(big): file > 32 KiB] extension ignored on both faces, built-ins intact: cat P (0) ; cat .env (2) ; Read P (0) ; Read /x/.env (2) │ exit=0,2,0,2 │ exit=0,2,0,2 │ yes
SC-20 │ 20f │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(many): 201 entries] extension ignored on both faces, built-ins intact: cat P (0) ; cat .env (2) ; Read P (0) ; Read /x/.env (2) │ exit=0,2,0,2 │ exit=0,2,0,2 │ yes
SC-20 │ 20n │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(size32769): file is 32769 bytes, one over the limit] extension ignored on both faces, built-ins intact: cat P (0) ; cat .env (2) ; Read P (0) ; Read /x/.env (2) │ exit=0,2,0,2 │ exit=0,2,0,2 │ yes
SC-20 │ 20o │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(comment_only): only comment lines -- zero valid entries] the extension is simply not in effect, and nothing is ever blocked because of it: ls -la (0) ; cat README.md (0) ; Read /x/README.md (0) ; Edit /x/notes.txt (0) ; built-ins intact: cat .env (2) ; Read /x/.env (2) │ exit=0,0,0,0,2,2 │ exit=0,0,0,0,2,2 │ yes
SC-20 │ 20p │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(blank_only): only blank / white-space lines -- zero valid entries] the extension is simply not in effect, and nothing is ever blocked because of it: ls -la (0) ; cat README.md (0) ; Read /x/README.md (0) ; Edit /x/notes.txt (0) ; built-ins intact: cat .env (2) ; Read /x/.env (2) │ exit=0,0,0,0,2,2 │ exit=0,0,0,0,2,2 │ yes
SC-20 │ 20q │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(all_skipped): every line skipped: a 3-char entry, a symbol-only entry, a 201-char entry, a commented-out entry -- zero valid entries] the extension is simply not in effect, and nothing is ever blocked because of it: ls -la (0) ; cat README.md (0) ; Read /x/README.md (0) ; Edit /x/notes.txt (0) ; built-ins intact: cat .env (2) ; Read /x/.env (2) │ exit=0,0,0,0,2,2 │ exit=0,0,0,0,2,2 │ yes
SC-20 │ 20g │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(unreadable): chmod 000] extension ignored on both faces, built-ins intact: cat P (0) ; cat .env (2) ; Read P (0) ; Read /x/.env (2) │ exit=0,2,0,2 │ exit=0,2,0,2 │ yes
SC-20 │ 20h │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(junk)] a file full of unpaired ( [ \ * ? entries still enforces its valid entry: cat P (2) ; an unrelated path stays allowed (0) │ exit=2,0 │ exit=0,0 │ no
SC-20 │ 20i │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] fault injection: `exit 1` inserted as the first statement of EVERY _sg_ext_* function; canaries cat .env (2) ; ls -la (0) ; Read /x/.env (2) ; Read /x/README.md (0) ; Edit /x/.env (2) │ exit=2,0,2,0,2 │ exit=2,0,2,0,2 │ yes
SC-20 │ 20j │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] fault injection: `unbound variable` inserted as the first statement of EVERY _sg_ext_* function; canaries cat .env (2) ; ls -la (0) ; Read /x/.env (2) ; Read /x/README.md (0) ; Edit /x/.env (2) │ exit=2,0,2,0,2 │ exit=2,0,2,0,2 │ yes
SC-20 │ 20k │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] fault injection: `return 1` inserted as the first statement of EVERY _sg_ext_* function; canaries cat .env (2) ; ls -la (0) ; Read /x/.env (2) ; Read /x/README.md (0) ; Edit /x/.env (2) │ exit=2,0,2,0,2 │ exit=2,0,2,0,2 │ yes
SC-20 │ 20l │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] evaluation order: when a built-in rule blocks, no extension function runs: cat .env (2) ; Read /x/.env (2) -> calls none │ exit=2,2 calls=none │ exit=2,2 calls=none │ yes
SC-20 │ 20m │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] ... and when the built-ins allow, the extension IS consulted (no dead code): ls -la (0) ; Read /x/README.md (0) -> calls _sg_ext_pass, _sg_ext_path_pass │ exit=0,0 calls=_sg_ext_pass,_sg_ext_path_pass │ exit=0,0 calls=none │ no
SC-21 │ 21a │ baseline-failing │ f=/etc/forgejo/app.ini; sed -n '1,80p' "$f" │ exit=2 │ exit=0 │ no
SC-21 │ 21b │ baseline-failing │ f=~/.bashrc; cat $f │ exit=2 │ exit=0 │ no
SC-21 │ 21c │ baseline-failing │ F=/etc/forgejo/app.ini && cat "$F" │ exit=2 │ exit=0 │ no
SC-21 │ 21d │ baseline-failing │ export CONF=/etc/forgejo/app.ini; cat $CONF │ exit=2 │ exit=0 │ no
SC-21 │ 21e │ baseline-failing │ ssh root@pve 'pct exec 101 -- sh -c "f=/etc/forgejo/app.ini; sed -n 1,80p \$f"' │ exit=2 │ exit=0 │ no
SC-21 │ 21f │ baseline-failing │ d=/etc/forgejo; f=$d/app.ini; cat "$f" │ exit=2 │ exit=0 │ no
SC-21 │ 21g │ baseline-failing │ f=.env; cat ${f} │ exit=2 │ exit=0 │ no
SC-21 │ 21h │ baseline-failing │ for f in /etc/forgejo/app.ini; do cat "$f"; done │ exit=2 │ exit=0 │ no
SC-21 │ 21i │ allow-guard │ assignments that do not lead to a sensitive read stay allowed: ls -l, KUBECONFIG export, cp, glob loop, plain variable │ exit=0,0,0,0,0 │ exit=0,0,0,0,0 │ yes
SC-21 │ 21n │ known-limit │ files=(/etc/forgejo/app.ini); cat "${files[0]}" │ exit=0 │ exit=0 │ yes
SC-21 │ 21o │ known-limit │ read -r f <<< /etc/forgejo/app.ini; cat "$f" │ exit=0 │ exit=0 │ yes
SC-21 │ 21p │ known-limit │ cat /etc/fo""rgejo/app.ini │ exit=0 │ exit=0 │ yes
SC-21 │ 21q │ known-limit │ d=/etc/forgejo; cat "$d"/app.ini │ exit=0 │ exit=0 │ yes
SC-21 │ 21r │ known-limit │ cd /etc/forgejo && cat app.ini │ exit=0 │ exit=0 │ yes
SC-21 │ 21s │ known-limit │ cat /etc/for*/app.ini │ exit=0 │ exit=0 │ yes
SC-21 │ 21t │ known-limit │ set -- /etc/forgejo/app.ini; cat "$1" │ exit=0 │ exit=0 │ yes
SC-21 │ 21u │ known-limit │ cat "$(printf '/etc/%s/app.ini' forgejo)" │ exit=0 │ exit=0 │ yes
SC-21 │ 21j │ baseline-failing │ assignment forms the collector accepts after a benign first segment (`true; <form>; <reader>`: the assignment does not start the command), one hook run each: the 5 declaration prefixes (export declare local readonly typeset), declare with an option, a double-quoted value, a single-quoted value, export with a quoted value │ 9/9 as expected (exit=2) │ 0/9 as expected; wrong: export, declare, local, readonly, typeset, declare-x, ... │ no
SC-21 │ 21x │ baseline-failing │ bounds, last accepted: the 16th assignment is the sensitive one (15 x `aN=x; ` first) -> exit 2 ; the 8th reference of a variable is the reader's (7 x `$f` in an `echo`, then `| cat $f`) -> exit 2 │ exit=2,2 │ exit=0,0 │ no
SC-21 │ 21y │ known-limit │ KNOWN-LIMIT, bounds exceeded pass (padding): the sensitive assignment is the 17th -> exit 0 ; the reader's reference is the 9th of the variable (8 x `$f` first) -> exit 0 │ exit=0,0 │ exit=0,0 │ yes
SC-21 │ 21z │ reverse-guard │ no-execution invariant of the variable expansion: assigned values holding a command substitution, back quotes or an arithmetic expansion around a command substitution (5 payloads, each `touch`es a private canary path) are only ever text for the hook: none of the 5 canary files exists after the hook has run │ 5/5 as expected │ 5/5 as expected │ yes
SC-21 │ 21v │ reverse-guard │ evaluation order: all segments are judged by the built-in rules BEFORE any substituted copy: `f=/etc/hosts; cat "$f"; cat .env` -> exit 2, the second pass never runs │ exit=2 calls=none │ exit=2 calls=none │ yes
SC-21 │ 21w │ baseline-failing │ ... and when every built-in verdict is `allow`, the second pass runs: `f=/etc/hosts; cat "$f"` -> exit 0, _sg_vx_pass called │ exit=0 calls=_sg_vx_pass │ exit=0 calls=none │ no
SC-22 │ 22a │ baseline-failing │ ps aux │ exit=2 │ exit=0 │ no
SC-22 │ 22b │ baseline-failing │ ps -ef │ exit=2 │ exit=0 │ no
SC-22 │ 22c │ baseline-failing │ ps auxww │ exit=2 │ exit=0 │ no
SC-22 │ 22d │ baseline-failing │ ps -eo pid,args │ exit=2 │ exit=0 │ no
SC-22 │ 22e │ baseline-failing │ ps -o pid,command -p 123 │ exit=2 │ exit=0 │ no
SC-22 │ 22f │ baseline-failing │ ps -ww -fp 123 │ exit=2 │ exit=0 │ no
SC-22 │ 22g │ baseline-failing │ ps eww -p 123 │ exit=2 │ exit=0 │ no
SC-22 │ 22h │ baseline-failing │ ps e │ exit=2 │ exit=0 │ no
SC-22 │ 22i │ baseline-failing │ ps -C curl -o args= │ exit=2 │ exit=0 │ no
SC-22 │ 22j │ baseline-failing │ ps --format pid,cmd │ exit=2 │ exit=0 │ no
SC-22 │ 22k │ baseline-failing │ pgrep -af curl │ exit=2 │ exit=0 │ no
SC-22 │ 22l │ baseline-failing │ pgrep -a curl │ exit=2 │ exit=0 │ no
SC-22 │ 22m │ baseline-failing │ pgrep --list-full curl │ exit=2 │ exit=0 │ no
SC-22 │ 22n │ baseline-failing │ sudo pgrep -af curl │ exit=2 │ exit=0 │ no
SC-22 │ 22o │ baseline-failing │ pstree -ap │ exit=2 │ exit=0 │ no
SC-22 │ 22p │ baseline-failing │ top -b -n1 -c │ exit=2 │ exit=0 │ no
SC-22 │ 22q │ baseline-failing │ ps aux | grep curl │ exit=2 │ exit=0 │ no
SC-22 │ 22r │ baseline-failing │ ps -ef | grep -v grep │ exit=2 │ exit=0 │ no
SC-22 │ 22s │ baseline-failing │ ps aux | grep '^dev' │ exit=2 │ exit=0 │ no
SC-22 │ 22t │ baseline-failing │ docker ps --no-trunc │ exit=2 │ exit=0 │ no
SC-22 │ 22u │ baseline-failing │ docker top abc │ exit=2 │ exit=0 │ no
SC-22 │ 22v │ baseline-failing │ ssh host 'ps aux' │ exit=2 │ exit=0 │ no
SC-22 │ 22w │ baseline-failing │ x=$(ps aux) │ exit=2 │ exit=0 │ no
SC-22 │ 22x │ baseline-failing │ sudo ps -ef │ exit=2 │ exit=0 │ no
SC-22 │ 22y │ baseline-failing │ watch -n 5 ps aux │ exit=2 │ exit=0 │ no
SC-22 │ 22z │ baseline-failing │ watch -n1 'ps aux' │ exit=2 │ exit=0 │ no
SC-22 │ 22A │ baseline-failing │ sh -c 'ps aux' │ exit=2 │ exit=0 │ no
SC-22 │ 22B │ baseline-failing │ bash -c "ps -ef" │ exit=2 │ exit=0 │ no
SC-22 │ 22C │ baseline-failing │ pct exec 101 -- ps aux │ exit=2 │ exit=0 │ no
SC-22 │ 22D │ baseline-failing │ kubectl exec pod -- ps aux │ exit=2 │ exit=0 │ no
SC-22 │ 22E │ baseline-failing │ nomad alloc exec -task server abc123 ps aux │ exit=2 │ exit=0 │ no
SC-22 │ 22F │ baseline-failing │ cat /proc/*/cmdline │ exit=2 │ exit=0 │ no
SC-22 │ 22G │ baseline-failing │ cat /proc/$pid/cmdline │ exit=2 │ exit=0 │ no
SC-22 │ 22H │ baseline-failing │ xargs -0 -a /proc/123/cmdline echo │ exit=2 │ exit=0 │ no
SC-22 │ 22I │ baseline-failing │ cat /proc/*/environ │ exit=2 │ exit=0 │ no
SC-22 │ 22am │ baseline-failing │ ps 123 │ exit=2 │ exit=0 │ no
SC-22 │ 22an │ baseline-failing │ cat /proc/1/task/1/environ │ exit=2 │ exit=0 │ no
SC-22 │ 22ao │ baseline-failing │ nomad alloc exec -task server abc123 env │ exit=2 │ exit=0 │ no
SC-22 │ 22ap │ baseline-failing │ pct exec 101 -- env │ exit=2 │ exit=0 │ no
SC-22 │ 22aq │ baseline-failing │ ssh root@pve pct exec 101 -- env │ exit=2 │ exit=0 │ no
SC-22 │ 22ar │ baseline-failing │ nomad alloc exec abc123 printenv │ exit=2 │ exit=0 │ no
SC-22 │ 22J │ reverse-guard │ existing /proc/N/{cmdline,environ} blocks stay (cat, tr <, cat, cat self, strings) │ exit=2,2,2,2,2 │ exit=2,2,2,2,2 │ yes
SC-22 │ 22bc │ reverse-guard │ the rewritten /proc rows keep every baseline reader blocked: each of the 13 baseline readers x {/proc/123/environ, /proc/self/cmdline}, plus two `<` redirects │ 28/28 as expected (exit=2) │ 28/28 as expected │ yes
SC-22 │ 22bd │ baseline-failing │ the 11 readers added to the /proc rows (xargs sed grep rg cut paste nl sort base64 cp dd; egrep / fgrep / zgrep end in `grep` and are matched by it, as the baseline rows have no left boundary) read /proc/123/environ │ 13/13 as expected (exit=2) │ 0/13 as expected; wrong: xargs, sed, grep, rg, cut, paste, ... │ no
SC-22 │ 22be │ baseline-failing │ pid positions of the widened /proc rows: `*`, `$pid`, `${pid}`, `$(...)` and a `task/<tid>/` sub-path, for a baseline reader and an added reader │ 6/6 as expected (exit=2) │ 0/6 as expected; wrong: star, dollar-name, dollar-brace, cmd-subst, task-environ, task-added-reader │ no
SC-22 │ 22bg │ baseline-failing │ inline interpreters read /proc/<pid>/environ|cmdline (python3 -c and node -e source groups) │ 4/4 as expected (exit=2) │ 0/4 as expected; wrong: python3-environ, python3-cmdline, python3-var-pid, node-environ │ no
SC-22 │ 22av │ baseline-failing │ ps spellings that print the full argv with a leading dash (procps-ng BSD compatibility) or `-O`: -aux -ax -x -ux -au -axu -auxww -w -x -eO -O -eu -u -ex -xw, and the incident-class `ps -aux | grep curl` │ 15/15 as expected (exit=2) │ 0/15 as expected; wrong: ps -aux, ps -ax, ps -x, ps -ux, ps -au, ps -axu, ... │ no
SC-22 │ 22aw │ baseline-failing │ every launcher of the launcher set (the 13 words of the env / printenv launcher row + command exec = 15; `watch` is a shell wrapper, see 22bk) in front of `ps aux` │ 15/15 as expected (exit=2) │ 0/15 as expected; wrong: sudo, doas, nice, timeout, xargs, nohup, ... │ no
SC-22 │ 22ax │ baseline-failing │ launchers whose options take arguments, a duration operand, assignments, and the xargs pipelines of the incident class │ 14/14 as expected (exit=2) │ 0/14 as expected; wrong: sudo -u forgejo ps -ef, sudo -u svc -g grp ps aux, doas -u root ps aux, timeout -s KILL 5 ps aux, timeout 5 ps aux, timeout 5s ps aux, ... │ no
SC-22 │ 22ay │ baseline-failing │ absolute-path program names: /bin/ps, /usr/bin/ps, pgrep, pstree, top, an absolute launcher, an absolute target behind a launcher and behind ssh │ 8/8 as expected (exit=2) │ 0/8 as expected; wrong: /bin/ps aux, /usr/bin/ps -ef, /usr/bin/pgrep -af curl, /usr/bin/pstree -ap, /usr/bin/top -b -n1 -c, /usr/bin/sudo ps aux, ... │ no
SC-22 │ 22az │ baseline-failing │ shell keyword command positions: then / do / else / elif before a process-table command │ 5/5 as expected (exit=2) │ 0/5 as expected; wrong: then, do, else, elif, do-pgrep │ no
SC-22 │ 22bb │ baseline-failing │ podman is docker's sibling: podman top, podman ps --no-trunc │ 2/2 as expected (exit=2) │ 0/2 as expected; wrong: podman-top, podman-ps │ no
SC-22 │ 22bl │ baseline-failing │ every spelling of the non-ps process-table forms: pgrep -a / -af / --list-full, pstree -a / -ap / --arguments, top -c (separate and clustered), docker top / docker compose top / docker container top, docker ps --no-trunc / docker container ls --no-trunc │ 13/13 as expected (exit=2) │ 0/13 as expected; wrong: pgrep-a, pgrep-af, pgrep-list-full, pstree-a, pstree-ap, pstree-arguments, ... │ no
SC-22 │ 22bk │ baseline-failing │ every remote / shell wrapper of the wrapper set around `ps aux`: ssh, docker exec, docker compose exec, podman exec, kubectl exec, lxc exec, nomad alloc exec, pct exec, sh -c, bash -c, watch '...' │ 11/11 as expected (exit=2) │ 0/11 as expected; wrong: ssh, docker, docker-compose, podman, kubectl, lxc, ... │ no
SC-22 │ 22bm │ baseline-failing │ tight credit, member by member: every member of the process-table family (the 10 ps argument classes, the 14 dash spellings, the 15 launchers, the 14 launcher-with-arguments forms, the 8 absolute-path forms, podman, the 11 wrappers, the 13 non-ps spellings) followed by `| grep -v x` stays blocked, and the other row-level filters on `ps aux` (anchored grep, sed, cut, awk) do not count either │ 91/91 as expected (exit=2) │ 0/91 as expected; wrong: ps aux, ps 123, ps -ef, ps -eo pid,args, ps -o pid,command -p 123, ps -ww -fp 123, ... │ no
SC-22 │ 22bn │ allow-guard │ count / hash / discard credit, member by member: the same members followed by `| wc -l` stay allowed, and `ps aux` with a hash or a stdout discard │ 89/89 as expected (exit=0) │ 89/89 as expected │ yes
SC-22 │ 22bo │ baseline-failing │ env / printenv dumps under every remote / shell wrapper of the wrapper set (ssh, docker exec, docker compose exec, podman exec, kubectl exec, lxc exec, nomad alloc exec, pct exec, sh -c, bash -c, watch) x {env, printenv}: 22 members, each blocked │ 22/22 as expected (exit=2) │ 10/22 as expected; wrong: ssh:env, ssh:printenv, nomad:env, nomad:printenv, pct:env, pct:printenv, ... │ no
SC-22 │ 22bq │ baseline-failing │ the launcher and wrapper sets are not specific to `ps`: each of the 15 launchers and each of the 11 wrappers in front of / around each non-ps program (pgrep -af, pstree -a, top -b -n1 -c): 78 members, each blocked │ 78/78 as expected (exit=2) │ 0/78 as expected; wrong: sudo:pgrep -af x, sudo:pstree -a, sudo:top -b -n1 -c, doas:pgrep -af x, doas:pstree -a, doas:top -b -n1 -c, ... │ no
SC-22 │ 22bp │ baseline-failing │ pid positions of the /proc rows, v4 additions: `$$`, `$!`, `thread-self`, and glob tokens holding `*` or `?` (`[0-9]*`, `1*`, `1?`), for baseline readers, added readers, a `<` redirect, an xargs file operand and an inline interpreter │ 10/10 as expected (exit=2) │ 0/10 as expected; wrong: dollar-dollar, dollar-bang, thread-self, glob-bracket-star, glob-prefix-star, glob-question, ... │ no
SC-22 │ 22O │ allow-guard │ ps forms that print only pid / state / process NAME stay allowed (also with a launcher, an absolute path, a keyword position, an xargs pipeline) │ exit=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 │ exit=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 │ yes
SC-22 │ 22bi │ allow-guard │ launchers, absolute paths and keyword positions around commands that are not process-table commands stay allowed │ exit=0,0,0,0,0,0,0,0 │ exit=0,0,0,0,0,0,0,0 │ yes
SC-22 │ 22S │ allow-guard │ pgrep / pstree / top forms that print pids or names only stay allowed (Linux procps) │ exit=0,0,0,0,0 │ exit=0,0,0,0,0 │ yes
SC-22 │ 22Y │ allow-guard │ text that merely mentions ps, and ps with a counting / discarding credit, stay allowed │ exit=0,0,0,0,0 │ exit=0,0,0,0,0 │ yes
SC-22 │ 22bf │ allow-guard │ a /proc path whose pid position is a placeholder word (N, <pid>, [pid], {pid}) is text, not a read: the pid token accepts digits, self, thread-self, `$$`, `$!`, a glob token holding `*` or `?`, `$name`, `${...}`, `$(...)` only │ exit=0,0,0,0,0 │ exit=0,0,0,0,0 │ yes
SC-22 │ 22ad │ allow-guard │ docker ps (truncated), /proc comm and cpuinfo stay allowed │ exit=0,0,0,0 │ exit=0,0,0,0 │ yes
SC-22 │ 22as │ allow-guard │ read-only metadata files stay allowed when the /proc reader / pid positions are widened (status is NOT widened) │ exit=0,0,0 │ exit=0,0,0 │ yes
SC-22 │ 22at │ allow-guard │ exec wrappers around commands that do not dump argv / environ stay allowed (env as a launcher with arguments included) │ exit=0,0,0 │ exit=0,0,0 │ yes
SC-22 │ 22ah │ known-limit │ KNOWN-LIMIT: argv / environ exposure through systemctl status / show, docker inspect, journalctl is not blocked │ exit=0,0,0,0 │ exit=0,0,0,0 │ yes
SC-22 │ 22aj │ known-limit │ KNOWN-LIMIT (baseline over-block kept): the 13 baseline readers still block /proc/123/status │ 13/13 as expected (exit=2) │ 13/13 as expected │ yes
SC-22 │ 22bh │ known-limit │ KNOWN-LIMIT: find -exec and lua -e read /proc, a launcher nested in a launcher, a BSD cluster that is not the first operand, ps -e o <format>, a command after `if` / `while` / `until` (the baseline env / printenv rows list only then / do / else / elif), macOS pgrep -fl, a bare ps / pgrep inside a container (BusyBox prints the full command line), other process listings that print full command lines (systemd-cgls, pidstat -l, w, busybox ps, the AIX format `-o '%p %a'`), pid positions outside the closed set (brace expansion, a bracket class without `*` / `?`, a back-quote substitution, path normalisation `/proc/./self` and `/proc//self`), and the /proc rows being no tight family (a row-level filter counts as credit there) are not blocked │ 22/22 as expected (exit=0) │ 22/22 as expected │ yes
SC-22 │ 22bj │ baseline-failing │ ACCEPTED OVER-BLOCK (documented in W11, same newline anchor and same unanchored wrapper words as the baseline env / printenv rows): a line that merely STARTS with a process-table command inside a heredoc or multi-line string is blocked, because the newline is a command-position anchor; so is text in which a wrapper word (`ssh`, `watch`, also inside `sshd` / `stopwatch`) comes before a process-table form -- a commit message, an echo, a documentation search; the row turns red when someone narrows either (update W11 and this row then) │ 6/6 as expected (exit=2) │ 0/6 as expected; wrong: heredoc-ps, heredoc-after-text, commit-message-watch, sshd-substring, grep-doc-search, stopwatch-substring │ no
SC-22 │ 22au │ known-limit │ KNOWN-LIMIT: the Read tool face has no /proc rule │ exit=0,0,0 │ exit=0,0,0 │ yes
SC-23 │ 23a │ baseline-failing │ 10CG/Aria#221 original (multi-line `nomad alloc exec ... python -c` reading os.environ.get('DATABASE_URL')) │ exit=0 │ exit=2 │ no
SC-23 │ 23b │ baseline-failing │ single-key reads (all four substrings `.environ.get(` / `.environ[` / `.environb.get(` / `.environb[`, several in one command) are allowed: the same information as the allowed os.getenv( │ exit=0,0,0,0,0 │ exit=2,2,2,2,2 │ no
SC-23 │ 23c │ reverse-guard │ whole-table dumps and iteration over os.environ / os.environb stay blocked (and a single-key read next to a dump does not unblock it); printenv as control │ exit=2,2,2,2,2,2,2,2,2,2 │ exit=2,2,2,2,2,2,2,2,2,2 │ yes
SC-23 │ 23d │ reverse-guard │ dotfile reads through the interpreter rows stay blocked, including names with a letter / digit / underscore suffix (.env_prod .env2 .envprod .envs/) │ exit=2,2,2,2,2,2,2,2,2 │ exit=2,2,2,2,2,2,2,2,2 │ yes
SC-23 │ 23e │ reverse-guard │ non-interpreter readers keep blocking .env / .envrc (a global right boundary on the `.env` rows would have let these through) │ exit=2,2,2,2,2,2 │ exit=2,2,2,2,2,2 │ yes
SC-23 │ 23i │ reverse-guard │ no-execution invariant of the single-key normalisation: single-key reads whose key text holds a command substitution / back quotes (2 payloads, each `touch`es a private canary path) are only text for the hook: none of the 2 canary files exists after the hook has run │ 2/2 as expected │ 2/2 as expected │ yes
SC-23 │ 23f │ known-limit │ node -e "console.log(process.env.HOME)" │ exit=2 │ exit=2 │ yes
SC-23 │ 23g │ known-limit │ cat .env_prod │ exit=0 │ exit=0 │ yes
SC-23 │ 23h │ known-limit │ KNOWN-LIMIT: identifiers that merely start with `.env` (.environment, .env_file) are still blocked by the interpreter rows │ exit=2,2,2 │ exit=2,2,2 │ yes
SC-24 │ 24a │ baseline-failing │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq '.Items | map_values(length)' │ exit=0 │ exit=2 │ no
SC-24 │ 24b │ baseline-failing │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq 'keys_unsorted' │ exit=0 │ exit=2 │ no
SC-24 │ 24c │ baseline-failing │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq -r '.Items | keys_unsorted' │ exit=0 │ exit=2 │ no
SC-24 │ 24d │ baseline-failing │ nomad var get -out=json nomad/jobs/x | jq '.Items | map_values(length)' │ exit=0 │ exit=2 │ no
SC-24 │ 24e │ baseline-failing │ cat ~/.claude/settings.json | jq '.env | map_values(length)' │ exit=0 │ exit=2 │ no
SC-24 │ 24f │ reverse-guard │ jq forms that can print values stay blocked: keys[], `. as $d | ...`, keys_unsorted | $ENV, .Items, map_values(tostring), map_values(length), . │ exit=2,2,2,2,2,2 │ exit=2,2,2,2,2,2 │ yes
SC-24 │ 24l │ allow-guard │ length / .Items | length / keys stay allowed (already so at baseline: that part of 10CG/Aria#221 is outdated) │ exit=0,0,0 │ exit=0,0,0 │ yes
SC-24 │ 24o │ known-limit │ KNOWN-LIMIT: map(.name) / map(.key) stay blocked (they rest on a data assumption: that name / key fields are not secrets) │ exit=2,2 │ exit=2,2 │ yes
SC-24 │ 24p │ known-limit │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq '. as $d | keys | map($d[.])' │ exit=0 │ exit=0 │ yes
SC-25 │ 25a │ reverse-guard │ cat .env (segment mode): normalised BLOCKED stderr │ text=baseline-identical │ text=baseline-identical │ yes
SC-25 │ 25b │ reverse-guard │ x=$(cat .env) (whole-command mode): normalised BLOCKED stderr │ text=baseline-identical │ text=baseline-identical │ yes
SC-25 │ 25c │ reverse-guard │ Read /x/.env: normalised Read/Edit BLOCKED stderr │ text=baseline-identical │ text=baseline-identical │ yes
SC-25 │ 25d │ baseline-failing │ ps aux: new block reuses the unchanged BLOCKED text │ text=baseline-identical │ exit=0 (no BLOCKED text) │ no
SC-25 │ 25e │ baseline-failing │ cat /etc/forgejo/app.ini: new block reuses the unchanged BLOCKED text │ text=baseline-identical │ exit=0 (no BLOCKED text) │ no
SC-25 │ 25f │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] cat /srv/billing/conf/prod.toml: extension block reuses the unchanged BLOCKED text │ text=baseline-identical │ exit=0 (no BLOCKED text) │ no
SC-25 │ 25g │ baseline-failing │ Read /etc/forgejo/app.ini: new Read block reuses the unchanged Read/Edit BLOCKED text │ text=baseline-identical │ exit=0 (no BLOCKED text) │ no
SC-26 │ 26a │ doc-sync │ standards secret-hygiene.md section 3.8: a line naming 命令行参数 + env + --config + stdin, scoped to long-running processes (words 长时 / 存活期), with the boundary to short commands written down (`60 秒`) │ clause-present-in-3.8 │ section-absent │ no
SC-26 │ 26b │ doc-sync │ standards secret-hygiene.md section 2.5: a line with `pgrep -a` (the process-table family) and the note that the shared BLOCKED text's `Acceptable filters` do not apply to the tight families │ ps-family-row-in-2.5 │ ps-family-row-absent-in-2.5 │ no
SC-26 │ 26c │ doc-sync │ standards secret-hygiene.md section 5.6: `.aria/secret-guard.paths` documented (location and project root, literal-substring syntax, case-insensitive, only-adds semantics, 32 KiB / 200 limits, ignore-the-whole-file on failure and that this is SILENT) │ ext-section-complete │ section-absent │ no
SC-26 │ 26d │ doc-sync │ standards secret-hygiene.md section 2.2: a line naming the server-side config family (`app.ini`) │ app.ini-in-2.2 │ app.ini-absent-in-2.2 │ no
SC-26 │ 26e │ doc-sync │ aria README.md and README.zh.md, Hooks usage section: the `.aria/secret-guard.paths` entry point is described, including its literal-substring syntax (`literal substring` / `字面子串`) │ README.md=has-extension-entry; README.zh.md=has-extension-entry │ README.md=missing; README.zh.md=missing │ no
SC-26 │ 26f │ doc-sync │ secret-guard.sh header (first 140 lines): the extension file, two representative residual gaps (systemctl status, docker inspect), the tight-family / `Acceptable filters` mismatch and the partial coverage of variable indirection are written down │ header-complete │ header-missing .aria/secret-guard.paths,systemctl status,docker inspect,Acceptable filters,variable indirection │ no
SC-26 │ 26g │ doc-sync │ aria CHANGELOG.md, topmost version section: names rule6_note, the new `.aria/secret-guard.paths` input, the `ps aux` behaviour change, the loosening side (`os.environ` single-key reads, `keys_unsorted`), the `fp=` log field and the `partial` coverage of variable indirection │ top-section-complete │ top-section-missing rule6_note,.aria/secret-guard.paths,ps aux,os.environ,keys_unsorted,fp=,partial │ no
SC-26 │ 26h │ reverse-guard │ standards secret-hygiene.md sections 3.1-3.7 and 4.1-4.4 (the argv `KEY=...` examples) are byte-identical to the baseline: the new 3.8 clause narrows its scope instead of contradicting them │ examples byte-identical to baseline │ examples byte-identical to baseline │ yes
SC-26 │ 26i │ reverse-guard │ standards secret-hygiene.md never uses this Spec's layer numbers L1 / L3 (the SOT's own terms are Path 1-3 / Layer 0 / Layer 2; its section 0 explains why there is no Layer 1) │ 0 occurrences of L1 / L3 │ 0 occurrences of L1 / L3 │ yes
SC-26 │ 26j │ doc-sync │ standards secret-hygiene.md: version line 1.2.0 and a history row `| 1.2.0 |` naming secret-net-l3-and-bypass-paths │ version-line=1.2.0; history-row=present │ version-line=other; history-row=absent │ no
SC-26 │ 26k │ doc-sync │ standards secret-hygiene.md section 5.1 (plugin SOT paths): the guard-suite row lists the new families (`app.ini`) │ app.ini-in-5.1 │ app.ini-absent-in-5.1 │ no
SC-27 │ 27a │ reverse-guard │ secret-hygiene.md: 3 spots equal secret-guard.test.sh header 'Coverage: N cases (M without zsh)' │ 3/3 spots equal test header │ 3/3 spots equal test header │ yes
SC-27 │ 27b │ doc-sync │ secret-scan.test.sh: header 'Coverage: K cases' exists and K == suite run total │ header == run-total │ header-count-absent │ no
SC-27 │ 27c │ reverse-guard │ secret-hygiene.md: secret-scan row count equals the secret-scan suite run total │ SOT equals run total │ SOT equals run total │ yes
SC-27 │ 27d │ doc-sync │ secret-scan.test.sh: a NON-comment line reads the `Coverage:` header count (the self-check that makes the count an assertion, as the guard suite's test-internal SC-13 does); a header comment alone does not satisfy this row │ >=1 non-comment line reads the header count │ 0 non-comment line(s) read the header count │ no
SC-28 │ 28a │ doc-sync │ secret-guard.sh header: BOTH halves of the stale three-line sentence 'Phase 2 would add PostToolUse hook ... style env lines + redacts' are gone and a pointer to secret-scan.sh is in │ old gone; new present │ old still-present; new absent │ no
SC-28 │ 28b │ doc-sync │ secret-guard.sh header: dangling runbook reference re-pointed to secret-hygiene.md, and not to a section of it that does not exist (the SOT section 1 holds 1.1 / 1.2 only: no `§1.3`) │ old gone; new present │ old still-present; new absent │ no
SC-28 │ 28c │ doc-sync │ secret-scan.sh header: stale '~15 secret-shape patterns' removed and no new pattern-count literal written │ old gone; new present │ old still-present; new absent │ no
SC-28 │ 28d │ doc-sync │ secret-scan.sh header: stale '49 known bypass classes' removed and no new class-count literal written │ old gone; new present │ old still-present; new absent │ no
SC-28 │ 28e │ doc-sync │ secret-scan.sh header: the non-existent argon2 claim is gone (the word `argon2` appears nowhere in the file; bcrypt stays) │ old gone; new present │ old still-present; new present │ no
SC-28 │ 28f │ doc-sync │ secret-scan.sh hook contract: the old Read shape line is replaced by the real file.content shape and no contract line starts with a top-level `"content":` key │ old gone; new present │ old still-present; new absent │ no
SC-28 │ 28g │ doc-sync │ secret-scan.sh 'does NOT catch' list: the base64/hex line re-scoped to values with no prefix AND no credential key name │ old gone; new present │ old still-present; new absent │ no
SC-28 │ 28h │ doc-sync │ secret-hygiene.md 5.1: secret-guard no longer called a Write/MultiEdit blocker │ old gone; new present │ old still-present; new absent │ no
SC-28 │ 28i │ doc-sync │ aria/VERSION: stale 'output REDACT' description of secret-scan replaced by detect + warn │ old gone; new present │ old still-present; new absent │ no
SC-28 │ 28l │ doc-sync │ secret-scan.sh header: BOTH halves of the claim 'Claude Code exposes no field to replace tool_response ... not a version-dependent behaviour' are gone and the schema fact (updatedToolOutput exists, unverified, unused) is in │ old gone; new present │ old still-present; new absent │ no
SC-28 │ 28j │ doc-sync │ secret-guard.sh History block (the comment block that starts at `# === History ===`) names change-id secret-net-l3-and-bypass-paths; a mention only in code comments does not count │ present │ absent │ no
SC-28 │ 28k │ doc-sync │ secret-scan.sh header block (the leading comment block of the file) names change-id secret-net-l3-and-bypass-paths; a mention only in code comments does not count │ present │ absent │ no
SC-28 │ 28m │ doc-sync │ the three places that still say a PostToolUse hook cannot redact (SOT 5.2, README.md and README.zh.md Hooks section) each gain ONE additive sentence naming the `updatedToolOutput` schema fact (unverified, unused); the existing sentences stay │ SOT-5.2=names-updatedToolOutput; README.md=names-updatedToolOutput; README.zh.md=names-updatedToolOutput │ SOT-5.2=silent-on-it; README.md=silent-on-it; README.zh.md=silent-on-it │ no
SC-28 │ 28n │ doc-sync │ secret-scan.sh header (first 100 lines): the `Scope / what this catches` list names the 6 new tags │ scope-lists-all-6-new-tags │ scope-misses auth-header-token,cf-access-client-secret,cli-secret-flag,json-credential-field,json-env-secret-key,kv-secret-assign │ no
SC-29 │ 29a │ zero-regression │ bash hooks/tests/secret-scan.test.sh │ FAIL 0 and total>=49 │ PASS 49/49 FAIL 0 │ yes
SC-29 │ 29b │ zero-regression │ bash hooks/tests/secret-guard.test.sh (no-git copy: SC-9a/SC-8 and zsh cases skipped) │ PASS>=581, fail-set within {test-internal SC-13 header count: no-git artefact} │ PASS 581/582 FAIL 1 fail-set={SC-13: 头注释计数同步} │ yes
SC-29 │ 29c │ zero-regression │ bash hooks/tests/crlf-shim.test.sh │ rc=0 │ rc=0 │ yes
SC-29 │ 29d │ zero-regression │ bash hooks/tests/jq-crlf-guard.test.sh │ rc=0 │ rc=0 │ yes
SC-29 │ 29e │ zero-regression │ bash hooks/tests/host-docker-logout-guard.test.sh │ rc=0 │ rc=0 │ yes
SC-29 │ 29f │ zero-regression │ bash hooks/tests/submodule-gate-telemetry.test.sh │ rc=0 │ rc=0 │ yes
SC-29 │ 29g │ zero-regression │ bash hooks/tests/jq-crlf-guard.sh hooks/secret-guard.sh hooks/secret-scan.sh │ rc=0 │ rc=0 │ yes
SC-29 │ 29h │ zero-regression │ bash hooks/tests/secret-scan.test.sh run by a real bash 3.2 (WPA_BASH32; the hooks it spawns resolve to 3.2 too) │ FAIL 0 and total>=49 │ PASS 49/49 FAIL 0 │ yes
SC-29 │ 29i │ zero-regression │ bash hooks/tests/secret-guard.test.sh run by a real bash 3.2 (same no-git artefact as 29b) │ PASS>=581, fail-set within {test-internal SC-13 header count: no-git artefact} │ PASS 581/582 FAIL 1 fail-set={SC-13: 头注释计数同步} │ yes
SC-30 │ 30a │ zero-regression │ secret-guard.test.sh on a checkout WITH git history (SC-9a, SC-8 latency gate) -- not run by this probe, see proposal │ n/a │ not-run │ n/a
SC-31 │ 31a │ reverse-guard │ corpus_census.py patterns.total (risky_patterns rows) within budget │ patterns<=150 │ patterns=145 │ yes
SC-31 │ 31b │ reverse-guard │ corpus_census.py family_count equals the value hard-coded in secret-guard.test.sh SC-19 │ census == test-hardcoded │ census=61 test-hardcoded=61 │ yes
SC-31 │ 31c │ reverse-guard │ risky_patterns has no row made only of a "${VAR}" expansion (census blind spot) │ 0 variable-only rows │ 0 variable-only rows │ yes
SC-31 │ 31d │ reverse-guard │ hooks/hooks.json byte-identical to baseline (no matcher/registration change) │ hooks.json=baseline-identical │ hooks.json=baseline-identical │ yes
SC-31 │ 31e │ reverse-guard │ hooks/hooks.json holds no literal completeness_gate (10CG/Aria#199 seam) │ gone │ gone │ yes
SC-32 │ 32a │ reverse-guard │ hooks/secret-guard.sh + secret-scan.sh code lines: none of 13 bash 4+ constructs (declare -A, mapfile/readarray, ${x,,}/${x^^}, [[ -v ]], nameref, negative subscript, ${x@Q}, |&, &>>, ;;&, coproc, shopt globstar/lastpipe, wait -n) -- a HEURISTIC, not a proof of 3.2-runnability (see 32c); each of the 13 detectors is first checked against a sample line of its own construct │ 0 bash 4+ constructs; detectors self-tested 13/13 │ 0 bash 4+ constructs; detectors self-tested 13/13 │ yes
SC-32 │ 32b │ reverse-guard │ hooks/secret-*.sh and tests/secret-*.test.sh keep LF line endings │ LF-only │ LF-only │ yes
SC-32 │ 32c │ reverse-guard │ every hook-direct row above, run once by the default bash and once by a real bash 3.2 (WPA_BASH32): the two result strings are identical row by row │ identical over all hook-direct rows │ identical over 361 hook-direct rows │ yes
SC-32 │ 32d │ reverse-guard │ the same differential in a SECOND locale (WPA_LOCALE_B, default en_US.UTF-8; a non-C collation order): every hook-direct row, run by the default bash and by a real bash 3.2 with LC_ALL set to that locale, gives the same result string as the run in the first locale (C.UTF-8), row by row -- a character class that bash < 5 expands by collation order (`[a-z]` counting upper case) would differ here and nowhere else │ identical over all hook-direct rows in a second locale │ identical over 361 hook-direct rows (locale en_US.UTF-8) │ yes
SC-33 │ 33a │ allow-guard │ L3 false-positive census: every text file <=200 KB under <aria> and <standards> (keyword prefilter) fed as a Read result; every file where one of the 6 new tags fires is on the attribution list, and the prefilter passes every key / keyword / flag name of the enumerated sets (a prefilter that missed one would skip files silently) │ every flagged file is on the attribution list; prefilter covers every name │ flagged=0: none; prefilter passes 77/77 names │ yes

== per-SC match (yes/total) ==
SC-1: 0/4
SC-2: 6/6
SC-3: 2/2
SC-4: 0/19
SC-5: 0/14
SC-6: 0/11
SC-7: 14/14
SC-8: 0/1
SC-9: 25/25
SC-10: 11/12
SC-11: 15/26
SC-12: 3/15
SC-13: 3/7
SC-14: 0/2
SC-15: 6/7
SC-16: 2/18
SC-17: 4/4
SC-18: 3/9
SC-19: 10/29
SC-20: 15/17
SC-21: 12/23
SC-22: 15/72
SC-23: 7/9
SC-24: 4/9
SC-25: 3/7
SC-26: 2/11
SC-27: 2/4
SC-28: 0/14
SC-29: 9/9
SC-30: not run by this probe
SC-31: 5/5
SC-32: 4/4
SC-33: 1/1

== per-category match (yes/total) ==
baseline-failing: 0/202
doc-sync: 0/25
reverse-guard: 72/72
allow-guard: 67/67
known-limit: 35/35
zero-regression: 9/9
rows not run (n/a): by design 1 (30a); leg missing or not constructible 0 (-)
baseline shape (baseline-failing + doc-sync all 'no', every other category all 'yes'): holds
target shape (every row 'yes' and no leg row left unrun): does not hold
```
