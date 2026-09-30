# baseline-evidence: secret-net-l3-and-bypass-paths

> 本文件 = 同目录 `baseline_probe.py` 在冻结基线上的实跑 stdout (原样粘贴, 未改一个字符) + 复现说明。`proposal.md` 里 SC 的「基线」值都取自下方输出 (SC-30 除外, 它不由本探针执行)。

## 基线与环境

- 基线: aria `268da8f39d8bc33967e7cdaa5681e3a221fb9e4b` (= v1.74.1); 主仓 `0748dbc`; standards `2bc1c4c`。
- 被测文件指纹见输出第 2–6 行 (sha256 前 16 位): `hooks/secret-guard.sh` `448b1f71a2af06d7`、`hooks/secret-scan.sh` `c5f53f7a164fa72e`、`hooks/tests/secret-guard.test.sh` `72f8e7d5d58a4b80`、`hooks/tests/secret-scan.test.sh` `78e0e4ca15078177`、`standards/conventions/secret-hygiene.md` `dcf203f1f25ef0c0`。
- 环境: Linux 6.17.9, Python 3.11.2, GNU bash 5.2.15, jq 1.6, GNU grep 3.8, GNU sed 4.9, perl 5.36.0; 本机无 zsh; `C.UTF-8` locale 可用。实跑日期 2026-09-30。

## 怎么跑

1. 布局: 探针按 `<aria>/../standards` 找 standards, 按自身所在目录找 `proposal.md`。本次把 `/home/dev/Aria/aria` 与 `/home/dev/Aria/standards` 用 `cp -a` 复制到同一个实验目录 `<X>` 下, 探针与 `proposal.md` 放在同一目录 (即落盘后的 `openspec/changes/secret-net-l3-and-bypass-paths/`)。
2. 命令: `TMPDIR=<X>/tmp python3 baseline_probe.py <X>/aria`。`TMPDIR` 只决定探针私有临时目录的位置 (结束时删除), 不进输出。
3. 连跑两次, stdout 逐字节相同 (sha256 前 16 位 `1ab63a323da13f45`, 41873 字节), stderr 为空, 每次约 1.5–2 分钟。
4. 比对注意: 若 standards 不在 `<aria>/../standards`, SC-26 / SC-27 / SC-28 中读 standards 的行会打印 `standards-absent`; 若探针旁没有 `proposal.md`, SC-15 15e 打印 `proposal.md-absent`。本输出只在复制出的副本上实测过; 对真 checkout 的 `aria/` 跑时, 套件同样在去掉 `.git` 的私有副本里执行。

## 读法

- 列: SC │ 用例 │ 类别 │ 输入形态 (占位描述) │ 期望 (目标态) │ 实得 │ 符合 (`yes` / `no`)。
- **基线形态**: `baseline-failing` 与 `doc-sync` 行应全部 `no`, 其余类别 (`reverse-guard` / `allow-guard` / `known-limit` / `zero-regression`) 应全部 `yes`; 输出末尾两行由探针机算该不变量 —— 本次 `holds`。实现完成后同一探针应输出「target shape … holds」。
- SC-30 一行不执行 (`n/a`), 理由见 `proposal.md` SC-30。
- 确定性措施: 像凭据的值在进程内由 `secrets` 生成, 生成时保证字符类与前缀性质 (判定不随随机值变化); hook 的环境变量从零构造 (不继承调用方的 `CLAUDE_PROJECT_DIR` 等); 测试套件在去掉 `.git` 的私有副本里跑、设 `GIT_CEILING_DIRECTORIES`、PATH 中隐去 zsh, 因此 `secret-guard.test.sh` 里依赖 git 历史的测试内 SC-9a / SC-8 与 zsh 用例总被跳过; 输出不含时间戳、随机值与临时路径。
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
SC-2 │ 2a │ reverse-guard │ Read legacy envelope {content}: AWS_ACCESS_KEY_ID=<AKIA+16> │ alert m=1 {aws-access-key-id=1} │ alert m=1 {aws-access-key-id=1} │ yes
SC-2 │ 2b │ reverse-guard │ Bash real envelope {stdout,...}: AWS_ACCESS_KEY_ID=<AKIA+16> │ alert m=1 {aws-access-key-id=1} │ alert m=1 {aws-access-key-id=1} │ yes
SC-2 │ 2c │ reverse-guard │ Bash legacy envelope {output}: AWS_ACCESS_KEY_ID=<AKIA+16> │ alert m=1 {aws-access-key-id=1} │ alert m=1 {aws-access-key-id=1} │ yes
SC-2 │ 2d │ reverse-guard │ Write real envelope {content,...}: AWS_ACCESS_KEY_ID=<AKIA+16> │ alert m=1 {aws-access-key-id=1} │ alert m=1 {aws-access-key-id=1} │ yes
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
SC-6 │ 6a │ baseline-failing │ Authorization: token <40 hex> (Forgejo/Gitea PAT header) │ alert m=1 {auth-header-token=1} │ silent │ no
SC-6 │ 6b │ baseline-failing │ curl -s -H "Authorization: token <40 hex>" https://forgejo.example/api/v1/user (command echo) │ alert m=1 {auth-header-token=1} │ silent │ no
SC-6 │ 6c │ baseline-failing │ CF-Access-Client-Secret: <64 hex> │ alert m=1 {cf-access-client-secret=1} │ silent │ no
SC-6 │ 6d │ baseline-failing │ curl -H "CF-Access-Client-Id: <32>.access" -H "CF-Access-Client-Secret: <64 hex>" │ alert m=1 {cf-access-client-secret=1} │ silent │ no
SC-6 │ 6e │ baseline-failing │ Authorization: Basic <b64 of user:pass> │ alert m=1 {auth-header-token=1} │ silent │ no
SC-6 │ 6f │ baseline-failing │ forgejo-runner register --instance https://git.example --token=<40 hex> │ alert m=1 {cli-secret-flag=1} │ silent │ no
SC-6 │ 6g │ baseline-failing │ ps-style line: curl with CF-Access-Client-Id/-Secret + Authorization: token (10CG/Aria#221 shape, L3 side) │ alert m=2 {auth-header-token=1 cf-access-client-secret=1} │ silent │ no
SC-7 │ 7a │ reverse-guard │ JWT_SECRET=<44 b64> (line start, no spaces) │ alert m=1 {env-line-secret-keyword=1} │ alert m=1 {env-line-secret-keyword=1} │ yes
SC-7 │ 7b │ reverse-guard │ INTERNAL_TOKEN = <JWT-shaped> │ alert m=1 {jwt=1} │ alert m=1 {jwt=1} │ yes
SC-7 │ 7c │ reverse-guard │ Authorization: Bearer <32 alnum> │ alert m=1 {bearer-token=1} │ alert m=1 {bearer-token=1} │ yes
SC-7 │ 7d │ reverse-guard │ json:client_secret=<32 alnum> │ alert m=1 {json-secret-field=1} │ alert m=1 {json-secret-field=1} │ yes
SC-7 │ 7e │ reverse-guard │ json:password=<16 alnum> │ alert m=1 {json-secret-field=1} │ alert m=1 {json-secret-field=1} │ yes
SC-7 │ 7f │ reverse-guard │ DB_PASSWORD=<20 alnum> (line start) │ alert m=1 {env-line-secret-keyword=1} │ alert m=1 {env-line-secret-keyword=1} │ yes
SC-7 │ 7g │ reverse-guard │ json:token=<gh-prefixed PAT> (single count) │ alert m=1 {github-pat=1} │ alert m=1 {github-pat=1} │ yes
SC-8 │ 8a │ baseline-failing │ json:api_key=<anthropic-prefixed key> (one credential, counted once) │ alert m=1 {anthropic-api-key=1} │ alert m=2 {anthropic-api-key=1 json-secret-field=1} │ no
SC-9 │ 9a │ allow-guard │ JWT_SECRET = <your-secret-here> (angle placeholder) │ silent │ silent │ yes
SC-9 │ 9b │ allow-guard │ JWT_SECRET=$(openssl rand -base64 32) │ silent │ silent │ yes
SC-9 │ 9c │ allow-guard │ PASSWD =  (empty value) │ silent │ silent │ yes
SC-9 │ 9d │ allow-guard │ grep -n "JWT_SECRET" /etc/forgejo/app.ini (key name only) │ silent │ silent │ yes
SC-9 │ 9e │ allow-guard │ JWT_SECRET = ${JWT_SECRET} (template reference) │ silent │ silent │ yes
SC-9 │ 9f │ allow-guard │ json:sha=<40 hex> (git commit sha) │ silent │ silent │ yes
SC-9 │ 9g │ allow-guard │ json:commit.id=<40 hex> │ silent │ silent │ yes
SC-9 │ 9h │ allow-guard │ json:token_last_eight=<8 hex> (Forgejo metadata) │ silent │ silent │ yes
SC-9 │ 9i │ allow-guard │ json:uuid=<uuid> │ silent │ silent │ yes
SC-9 │ 9j │ allow-guard │ json:next_page_token=<24 alnum> (pagination cursor, key outside closed list) │ silent │ silent │ yes
SC-9 │ 9k │ allow-guard │ git log full format (3 x commit <40 hex>) │ silent │ silent │ yes
SC-9 │ 9l │ allow-guard │ curl -H "Authorization: token $FORGEJO_TOKEN" (variable reference) │ silent │ silent │ yes
SC-9 │ 9m │ allow-guard │ forgejo-runner register --token=$RUNNER_TOKEN │ silent │ silent │ yes
SC-9 │ 9n │ allow-guard │ forgejo-runner register --token-file=/run/secrets/runner_token │ silent │ silent │ yes
SC-9 │ 9o │ allow-guard │ SECRET_FILE = /run/secrets/Db2Password (path-like value, 3 char classes) │ silent │ silent │ yes
SC-9 │ 9p │ allow-guard │ SECRET_PROMPT_NAME = release-notes-summary-v (single char class) │ silent │ silent │ yes
SC-9 │ 9q │ allow-guard │ export SECRET_GUARD_ACK_PATH="/home/u/.claude/settings.json" │ silent │ silent │ yes
SC-9 │ 9r │ allow-guard │ prose: set the token in your config file │ silent │ silent │ yes
SC-9 │ 9s │ allow-guard │ docker images --digests line (sha256:<64 hex>) │ silent │ silent │ yes
SC-9 │ 9t │ allow-guard │ Actions yaml  token: ${{ secrets.FORGEJO_TOKEN }} │ silent │ silent │ yes
SC-9 │ 9u │ allow-guard │ docker login -u ci --password-stdin registry.example.com (flag without value) │ silent │ silent │ yes
SC-10 │ 10a │ known-limit │ json:token=<40 lowercase letters> (single char class) │ silent │ silent │ yes
SC-10 │ 10b │ known-limit │ JWT_SECRET = <24 digits> (single char class) │ silent │ silent │ yes
SC-10 │ 10c │ known-limit │ json:token=<12 alnum> (shorter than 16) │ silent │ silent │ yes
SC-10 │ 10d │ known-limit │ YAML lowercase key  password: <16 alnum> │ silent │ silent │ yes
SC-10 │ 10e │ known-limit │ forgejo-runner register --token <40 hex> (space-separated flag) │ silent │ silent │ yes
SC-10 │ 10f │ known-limit │ json:SecretAccessKey=<40 alnum> (AWS PascalCase, outside closed list) │ silent │ silent │ yes
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
SC-12 │ 12a │ baseline-failing │ json:client_secret=<32 alnum>: log line gets fp=<sha256 hex prefix 8 of the value> │ fp=[sha256-8 of value] │ fp-field-absent │ no
SC-12 │ 12b │ baseline-failing │ json:password=<12 alnum>: value < 16 chars -> fp=L12, no hash in log │ fp=[L12] │ fp-field-absent │ no
SC-12 │ 12c │ baseline-failing │ json:client_secret=<32 alnum> with sha256sum/shasum absent from PATH -> fp=- │ fp=[-] │ fp-field-absent │ no
SC-12 │ 12d │ reverse-guard │ json:client_secret=<32 alnum>: log/stdout/stderr hold no value nor 8-char fragment │ log=1-line no-plaintext │ log=1-line no-plaintext │ yes
SC-12 │ 12e │ reverse-guard │ json:password=<12 alnum>: same check │ log=1-line no-plaintext │ log=1-line no-plaintext │ yes
SC-12 │ 12f │ reverse-guard │ app.ini fragment with 5 secrets: same check (JWT line alerts at baseline too) │ log=1-line no-plaintext │ log=1-line no-plaintext │ yes
SC-13 │ 13a │ baseline-failing │ Read /x/app.ini holding AWS_ACCESS_KEY_ID=<AKIA+16>: additionalContext names tags + source │ contains (tags: aws-access-key-id=1; source: Read /x/app.ini) │ silent │ no
SC-13 │ 13b │ baseline-failing │ Bash stdout json:client_secret=<32 alnum>: additionalContext names tags + source │ contains (tags: json-secret-field=1; source: Bash) │ addl-lacks-needle │ no
SC-13 │ 13c │ baseline-failing │ Write /x/f.txt holding AWS_ACCESS_KEY_ID=<AKIA+16>: additionalContext names tags + source │ contains (tags: aws-access-key-id=1; source: Write /x/f.txt) │ addl-lacks-needle │ no
SC-13 │ 13d │ reverse-guard │ Bash stdout AWS_ACCESS_KEY_ID=<AKIA+16>: prescriptive clause byte-identical to baseline │ contains baseline prescriptive clause │ addl-contains-needle │ yes
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
SC-17 │ 17a │ allow-guard │ chmod 600 /etc/forgejo/app.ini │ exit=0 │ exit=0 │ yes
SC-17 │ 17b │ allow-guard │ ls -l /etc/forgejo/app.ini │ exit=0 │ exit=0 │ yes
SC-17 │ 17c │ allow-guard │ systemctl restart forgejo │ exit=0 │ exit=0 │ yes
SC-17 │ 17d │ allow-guard │ grep -rn 'app.ini' docs/ │ exit=0 │ exit=0 │ yes
SC-17 │ 17e │ allow-guard │ cat /opt/myapp/app.ini │ exit=0 │ exit=0 │ yes
SC-17 │ 17f │ allow-guard │ cat /etc/php/8.2/fpm/php.ini │ exit=0 │ exit=0 │ yes
SC-17 │ 17g │ allow-guard │ git log --oneline -- custom/conf/app.ini │ exit=0 │ exit=0 │ yes
SC-17 │ 17h │ allow-guard │ cat /etc/forgejo/app.ini | wc -l │ exit=0 │ exit=0 │ yes
SC-17 │ 17i │ allow-guard │ sha256sum /etc/forgejo/app.ini │ exit=0 │ exit=0 │ yes
SC-17 │ 17j │ allow-guard │ cp /etc/forgejo/app.ini /tmp/app.ini.bak │ exit=0 │ exit=0 │ yes
SC-18 │ 18a │ baseline-failing │ Read /etc/forgejo/app.ini │ exit=2 │ exit=0 │ no
SC-18 │ 18b │ baseline-failing │ Read /var/lib/gitea/custom/conf/app.ini │ exit=2 │ exit=0 │ no
SC-18 │ 18c │ baseline-failing │ Edit /etc/gitea/app.ini │ exit=2 │ exit=0 │ no
SC-18 │ 18d │ baseline-failing │ Read /data/gitea/conf/app.ini │ exit=2 │ exit=0 │ no
SC-18 │ 18e │ allow-guard │ Read /opt/myapp/app.ini │ exit=0 │ exit=0 │ yes
SC-18 │ 18f │ allow-guard │ Read /etc/php/8.2/php.ini │ exit=0 │ exit=0 │ yes
SC-19 │ 19a │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] cat /srv/billing/conf/prod.toml │ exit=2 │ exit=0 │ no
SC-19 │ 19b │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] grep -n key /srv/billing/conf/prod.toml | grep -v '^#' (tight credit) │ exit=2 │ exit=0 │ no
SC-19 │ 19c │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] Read /srv/billing/conf/prod.toml │ exit=2 │ exit=0 │ no
SC-19 │ 19d │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] Edit /srv/billing/conf/prod.toml │ exit=2 │ exit=0 │ no
SC-19 │ 19e │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] cat /srv/billing/conf/prod.toml | wc -l │ exit=0 │ exit=0 │ yes
SC-19 │ 19f │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] ls -l /srv/billing/conf/prod.toml │ exit=0 │ exit=0 │ yes
SC-19 │ 19g │ baseline-failing │ [no CLAUDE_PROJECT_DIR; stdin cwd=proj(ok)] cat /srv/billing/conf/prod.toml │ exit=2 │ exit=0 │ no
SC-19 │ 19h │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(missing); stdin cwd=proj(ok)] cat /srv/billing/conf/prod.toml (env var wins) │ exit=0 │ exit=0 │ yes
SC-19 │ 19i │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] f=/srv/billing/conf/prod.toml; cat $f │ exit=2 │ exit=0 │ no
SC-19 │ 19j │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] cat /srv/a.b/c+d/key.conf (entry with regex metacharacters) │ exit=2 │ exit=0 │ no
SC-19 │ 19k │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] cat /srv/aXb/c+d/key.conf (dot is literal) │ exit=0 │ exit=0 │ yes
SC-19 │ 19l │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(ok)] cat abc (3-char entry ignored) │ exit=0 │ exit=0 │ yes
SC-19 │ 19m │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(crlf)] cat /srv/crlf/secret.conf (CRLF file) │ exit=2 │ exit=0 │ no
SC-19 │ 19n │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(ok) holding a line !.env] cat .env (extension cannot remove built-ins) │ exit=2 │ exit=2 │ yes
SC-20 │ 20a │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(missing): file absent] cat /srv/billing/conf/prod.toml (extension ignored) │ exit=0 │ exit=0 │ yes
SC-20 │ 20b │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(missing): file absent] cat .env (built-ins intact) │ exit=2 │ exit=2 │ yes
SC-20 │ 20c │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(dir): path is a directory] cat /srv/billing/conf/prod.toml (extension ignored) │ exit=0 │ exit=0 │ yes
SC-20 │ 20d │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(dir): path is a directory] cat .env (built-ins intact) │ exit=2 │ exit=2 │ yes
SC-20 │ 20e │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(dangling): dangling symlink] cat /srv/billing/conf/prod.toml (extension ignored) │ exit=0 │ exit=0 │ yes
SC-20 │ 20f │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(dangling): dangling symlink] cat .env (built-ins intact) │ exit=2 │ exit=2 │ yes
SC-20 │ 20g │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(nul): file holds a NUL byte] cat /srv/billing/conf/prod.toml (extension ignored) │ exit=0 │ exit=0 │ yes
SC-20 │ 20h │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(nul): file holds a NUL byte] cat .env (built-ins intact) │ exit=2 │ exit=2 │ yes
SC-20 │ 20i │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(big): file > 32 KiB] cat /srv/billing/conf/prod.toml (extension ignored) │ exit=0 │ exit=0 │ yes
SC-20 │ 20j │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(big): file > 32 KiB] cat .env (built-ins intact) │ exit=2 │ exit=2 │ yes
SC-20 │ 20k │ allow-guard │ [CLAUDE_PROJECT_DIR=proj(many): 201 entries] cat /srv/billing/conf/prod.toml (extension ignored) │ exit=0 │ exit=0 │ yes
SC-20 │ 20l │ reverse-guard │ [CLAUDE_PROJECT_DIR=proj(many): 201 entries] cat .env (built-ins intact) │ exit=2 │ exit=2 │ yes
SC-21 │ 21a │ baseline-failing │ f=/etc/forgejo/app.ini; sed -n '1,80p' "$f" │ exit=2 │ exit=0 │ no
SC-21 │ 21b │ baseline-failing │ f=~/.bashrc; cat $f │ exit=2 │ exit=0 │ no
SC-21 │ 21c │ baseline-failing │ F=/etc/forgejo/app.ini && cat "$F" │ exit=2 │ exit=0 │ no
SC-21 │ 21d │ baseline-failing │ export CONF=/etc/forgejo/app.ini; cat $CONF │ exit=2 │ exit=0 │ no
SC-21 │ 21e │ baseline-failing │ ssh root@pve 'pct exec 101 -- sh -c "f=/etc/forgejo/app.ini; sed -n 1,80p \$f"' │ exit=2 │ exit=0 │ no
SC-21 │ 21f │ baseline-failing │ d=/etc/forgejo; f=$d/app.ini; cat "$f" │ exit=2 │ exit=0 │ no
SC-21 │ 21g │ baseline-failing │ f=.env; cat ${f} │ exit=2 │ exit=0 │ no
SC-21 │ 21h │ baseline-failing │ for f in /etc/forgejo/app.ini; do cat "$f"; done │ exit=2 │ exit=0 │ no
SC-21 │ 21i │ allow-guard │ f=~/.bashrc; ls -l "$f" │ exit=0 │ exit=0 │ yes
SC-21 │ 21j │ allow-guard │ export KUBECONFIG=~/.kube/config; kubectl get pods │ exit=0 │ exit=0 │ yes
SC-21 │ 21k │ allow-guard │ f=.env; cp $f /tmp/x │ exit=0 │ exit=0 │ yes
SC-21 │ 21l │ allow-guard │ for f in *.txt; do cat $f; done │ exit=0 │ exit=0 │ yes
SC-21 │ 21m │ allow-guard │ name=world; echo "hello $name" │ exit=0 │ exit=0 │ yes
SC-21 │ 21n │ known-limit │ files=(/etc/forgejo/app.ini); cat "${files[0]}" │ exit=0 │ exit=0 │ yes
SC-21 │ 21o │ known-limit │ read -r f <<< /etc/forgejo/app.ini; cat "$f" │ exit=0 │ exit=0 │ yes
SC-21 │ 21p │ known-limit │ cat /etc/fo""rgejo/app.ini │ exit=0 │ exit=0 │ yes
SC-21 │ 21q │ known-limit │ d=/etc/forgejo; cat "$d"/app.ini │ exit=0 │ exit=0 │ yes
SC-21 │ 21r │ known-limit │ cd /etc/forgejo && cat app.ini │ exit=0 │ exit=0 │ yes
SC-21 │ 21s │ known-limit │ cat /etc/for*/app.ini │ exit=0 │ exit=0 │ yes
SC-21 │ 21t │ known-limit │ set -- /etc/forgejo/app.ini; cat "$1" │ exit=0 │ exit=0 │ yes
SC-21 │ 21u │ known-limit │ cat "$(printf '/etc/%s/app.ini' forgejo)" │ exit=0 │ exit=0 │ yes
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
SC-22 │ 22J │ reverse-guard │ cat /proc/123/cmdline │ exit=2 │ exit=2 │ yes
SC-22 │ 22K │ reverse-guard │ tr '\0' ' ' < /proc/123/cmdline │ exit=2 │ exit=2 │ yes
SC-22 │ 22L │ reverse-guard │ cat /proc/123/environ │ exit=2 │ exit=2 │ yes
SC-22 │ 22M │ reverse-guard │ cat /proc/self/environ │ exit=2 │ exit=2 │ yes
SC-22 │ 22N │ reverse-guard │ strings /proc/1/environ │ exit=2 │ exit=2 │ yes
SC-22 │ 22O │ allow-guard │ ps -e │ exit=0 │ exit=0 │ yes
SC-22 │ 22P │ allow-guard │ ps -eo pid,comm │ exit=0 │ exit=0 │ yes
SC-22 │ 22Q │ allow-guard │ ps -p 123 │ exit=0 │ exit=0 │ yes
SC-22 │ 22R │ allow-guard │ ps -o pid,stat,comm -p 123 │ exit=0 │ exit=0 │ yes
SC-22 │ 22S │ allow-guard │ pgrep curl │ exit=0 │ exit=0 │ yes
SC-22 │ 22T │ allow-guard │ pgrep -f curl │ exit=0 │ exit=0 │ yes
SC-22 │ 22U │ allow-guard │ pgrep -l curl │ exit=0 │ exit=0 │ yes
SC-22 │ 22V │ allow-guard │ pgrep -fl curl │ exit=0 │ exit=0 │ yes
SC-22 │ 22W │ allow-guard │ pstree -p │ exit=0 │ exit=0 │ yes
SC-22 │ 22X │ allow-guard │ top -b -n1 │ exit=0 │ exit=0 │ yes
SC-22 │ 22Y │ allow-guard │ grep -rn 'ps aux' docs/ │ exit=0 │ exit=0 │ yes
SC-22 │ 22Z │ allow-guard │ echo 'use ps -ef to list' │ exit=0 │ exit=0 │ yes
SC-22 │ 22aa │ allow-guard │ ps aux | wc -l │ exit=0 │ exit=0 │ yes
SC-22 │ 22ab │ allow-guard │ ps aux >/dev/null │ exit=0 │ exit=0 │ yes
SC-22 │ 22ac │ allow-guard │ man ps │ exit=0 │ exit=0 │ yes
SC-22 │ 22ad │ allow-guard │ docker ps │ exit=0 │ exit=0 │ yes
SC-22 │ 22ae │ allow-guard │ docker ps -a │ exit=0 │ exit=0 │ yes
SC-22 │ 22af │ allow-guard │ cat /proc/123/comm │ exit=0 │ exit=0 │ yes
SC-22 │ 22ag │ allow-guard │ cat /proc/cpuinfo │ exit=0 │ exit=0 │ yes
SC-22 │ 22ah │ known-limit │ systemctl status foo │ exit=0 │ exit=0 │ yes
SC-22 │ 22ai │ known-limit │ systemctl show -p ExecStart foo │ exit=0 │ exit=0 │ yes
SC-22 │ 22aj │ known-limit │ cat /proc/123/status │ exit=2 │ exit=2 │ yes
SC-22 │ 22ak │ known-limit │ docker inspect abc │ exit=0 │ exit=0 │ yes
SC-22 │ 22al │ known-limit │ journalctl -u foo │ exit=0 │ exit=0 │ yes
SC-23 │ 23a │ baseline-failing │ python3 -c "import os; print(len(os.environ.get('HOME','')))" │ exit=0 │ exit=2 │ no
SC-23 │ 23b │ baseline-failing │ python3 -c "import os; print(sorted(os.environ))" │ exit=0 │ exit=2 │ no
SC-23 │ 23c │ baseline-failing │ python -c "import os; print(os.environb.get(b'HOME') is None)" │ exit=0 │ exit=2 │ no
SC-23 │ 23d │ baseline-failing │ node -e "console.log(cfg.environment)" │ exit=0 │ exit=2 │ no
SC-23 │ 23e │ baseline-failing │ lua -e "print(os.getenv('HOME'), cfg.environment)" │ exit=0 │ exit=2 │ no
SC-23 │ 23f │ baseline-failing │ python3 -c "print(open('.env_prod').read())" │ exit=0 │ exit=2 │ no
SC-23 │ 23g │ reverse-guard │ python3 -c "print(open('.env').read())" │ exit=2 │ exit=2 │ yes
SC-23 │ 23h │ reverse-guard │ python3 -c "print(open('/srv/app/.env.production').read())" │ exit=2 │ exit=2 │ yes
SC-23 │ 23i │ reverse-guard │ python3 -c "print(open('.envrc').read())" │ exit=2 │ exit=2 │ yes
SC-23 │ 23j │ reverse-guard │ node -e "console.log(require('fs').readFileSync('.env','utf8'))" │ exit=2 │ exit=2 │ yes
SC-23 │ 23k │ reverse-guard │ lua -e "print(io.open('.env'):read('a'))" │ exit=2 │ exit=2 │ yes
SC-23 │ 23l │ reverse-guard │ head .envrc │ exit=2 │ exit=2 │ yes
SC-23 │ 23m │ reverse-guard │ tail -n 5 .envrc │ exit=2 │ exit=2 │ yes
SC-23 │ 23n │ reverse-guard │ cp .env /dev/stdout │ exit=2 │ exit=2 │ yes
SC-23 │ 23o │ reverse-guard │ scp .env user@host:/tmp/ │ exit=2 │ exit=2 │ yes
SC-23 │ 23p │ reverse-guard │ rsync -a .env user@host:/tmp/ │ exit=2 │ exit=2 │ yes
SC-23 │ 23q │ reverse-guard │ strings .envrc │ exit=2 │ exit=2 │ yes
SC-23 │ 23r │ known-limit │ node -e "console.log(process.env.HOME)" │ exit=2 │ exit=2 │ yes
SC-23 │ 23s │ known-limit │ cat .env_prod │ exit=0 │ exit=0 │ yes
SC-24 │ 24a │ baseline-failing │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq '.Items | map_values(length)' │ exit=0 │ exit=2 │ no
SC-24 │ 24b │ baseline-failing │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq 'keys_unsorted' │ exit=0 │ exit=2 │ no
SC-24 │ 24c │ baseline-failing │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq -r '.Items | keys_unsorted' │ exit=0 │ exit=2 │ no
SC-24 │ 24d │ baseline-failing │ nomad var get -out=json nomad/jobs/x | jq '.Items | map_values(length)' │ exit=0 │ exit=2 │ no
SC-24 │ 24e │ baseline-failing │ cat ~/.claude/settings.json | jq '.env | map_values(length)' │ exit=0 │ exit=2 │ no
SC-24 │ 24f │ reverse-guard │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq -r '.Items | keys[]' │ exit=2 │ exit=2 │ yes
SC-24 │ 24g │ reverse-guard │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq '. as $d | map_values(length) | $d' │ exit=2 │ exit=2 │ yes
SC-24 │ 24h │ reverse-guard │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq 'keys_unsorted | $ENV' │ exit=2 │ exit=2 │ yes
SC-24 │ 24i │ reverse-guard │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq '.Items' │ exit=2 │ exit=2 │ yes
SC-24 │ 24j │ reverse-guard │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq 'map_values(tostring)' │ exit=2 │ exit=2 │ yes
SC-24 │ 24k │ reverse-guard │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq 'map_values(length), .' │ exit=2 │ exit=2 │ yes
SC-24 │ 24l │ allow-guard │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq 'length' │ exit=0 │ exit=0 │ yes
SC-24 │ 24m │ allow-guard │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq '.Items | length' │ exit=0 │ exit=0 │ yes
SC-24 │ 24n │ allow-guard │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq 'keys' │ exit=0 │ exit=0 │ yes
SC-24 │ 24o │ known-limit │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq 'map(.name)' │ exit=2 │ exit=2 │ yes
SC-24 │ 24p │ known-limit │ curl -s http://127.0.0.1:4646/v1/var/nomad/jobs/x | jq '. as $d | keys | map($d[.])' │ exit=0 │ exit=0 │ yes
SC-25 │ 25a │ reverse-guard │ cat .env (segment mode): normalised BLOCKED stderr │ text=baseline-identical │ text=baseline-identical │ yes
SC-25 │ 25b │ reverse-guard │ x=$(cat .env) (whole-command mode): normalised BLOCKED stderr │ text=baseline-identical │ text=baseline-identical │ yes
SC-25 │ 25c │ reverse-guard │ Read /x/.env: normalised Read/Edit BLOCKED stderr │ text=baseline-identical │ text=baseline-identical │ yes
SC-25 │ 25d │ baseline-failing │ ps aux: new block reuses the unchanged BLOCKED text │ text=baseline-identical │ exit=0 (no BLOCKED text) │ no
SC-25 │ 25e │ baseline-failing │ cat /etc/forgejo/app.ini: new block reuses the unchanged BLOCKED text │ text=baseline-identical │ exit=0 (no BLOCKED text) │ no
SC-25 │ 25f │ baseline-failing │ [CLAUDE_PROJECT_DIR=proj(ok)] cat /srv/billing/conf/prod.toml: extension block reuses the unchanged BLOCKED text │ text=baseline-identical │ exit=0 (no BLOCKED text) │ no
SC-25 │ 25g │ baseline-failing │ Read /etc/forgejo/app.ini: new Read block reuses the unchanged Read/Edit BLOCKED text │ text=baseline-identical │ exit=0 (no BLOCKED text) │ no
SC-26 │ 26a │ doc-sync │ standards secret-hygiene.md: one line naming 命令行参数 + env + --config + stdin │ clause-present │ clause-absent │ no
SC-26 │ 26b │ doc-sync │ standards secret-hygiene.md: section 2.5 lists the process-table family (a line with `pgrep -a`) │ ps-family-row-present │ ps-family-row-absent │ no
SC-27 │ 27a │ reverse-guard │ secret-hygiene.md: 3 spots equal secret-guard.test.sh header 'Coverage: N cases (M without zsh)' │ 3/3 spots equal test header │ 3/3 spots equal test header │ yes
SC-27 │ 27b │ doc-sync │ secret-scan.test.sh: header 'Coverage: K cases' exists and K == suite run total │ header == run-total │ header-count-absent │ no
SC-27 │ 27c │ reverse-guard │ secret-hygiene.md: secret-scan row count equals the secret-scan suite run total │ SOT equals run total │ SOT equals run total │ yes
SC-28 │ 28a │ doc-sync │ secret-guard.sh header: stale 'Phase 2 ... + redacts' sentence removed │ gone │ still-present │ no
SC-28 │ 28b │ doc-sync │ secret-guard.sh header: dangling runbook reference removed │ gone │ still-present │ no
SC-28 │ 28c │ doc-sync │ secret-scan.sh header: stale '~15 secret-shape patterns' count replaced │ gone │ still-present │ no
SC-28 │ 28d │ doc-sync │ secret-scan.sh header: stale '49 known bypass classes' count replaced │ gone │ still-present │ no
SC-28 │ 28e │ doc-sync │ secret-scan.sh header: non-existent argon2 claim removed │ gone │ still-present │ no
SC-28 │ 28f │ doc-sync │ secret-scan.sh hook contract: old Read shape line replaced by the real file.content shape │ gone │ still-present │ no
SC-28 │ 28g │ doc-sync │ secret-scan.sh 'does NOT catch' list: base64/hex line re-scoped │ gone │ still-present │ no
SC-28 │ 28h │ doc-sync │ secret-hygiene.md 5.1: Write/MultiEdit no longer called blocked │ gone │ still-present │ no
SC-28 │ 28i │ doc-sync │ aria/VERSION: stale 'output REDACT' description of secret-scan removed │ gone │ still-present │ no
SC-28 │ 28j │ doc-sync │ secret-guard.sh History names change-id secret-net-l3-and-bypass-paths │ present │ absent │ no
SC-28 │ 28k │ doc-sync │ secret-scan.sh header names change-id secret-net-l3-and-bypass-paths │ present │ absent │ no
SC-29 │ 29a │ zero-regression │ bash hooks/tests/secret-scan.test.sh │ FAIL 0 and total>=49 │ PASS 49/49 FAIL 0 │ yes
SC-29 │ 29b │ zero-regression │ bash hooks/tests/secret-guard.test.sh (no-git copy: SC-9a/SC-8 and zsh cases skipped) │ PASS>=581, fail-set within {test-internal SC-13 header count: no-git artefact} │ PASS 581/582 FAIL 1 fail-set={SC-13: 头注释计数同步} │ yes
SC-29 │ 29c │ zero-regression │ bash hooks/tests/crlf-shim.test.sh │ rc=0 │ rc=0 │ yes
SC-29 │ 29d │ zero-regression │ bash hooks/tests/jq-crlf-guard.test.sh │ rc=0 │ rc=0 │ yes
SC-29 │ 29e │ zero-regression │ bash hooks/tests/host-docker-logout-guard.test.sh │ rc=0 │ rc=0 │ yes
SC-29 │ 29f │ zero-regression │ bash hooks/tests/submodule-gate-telemetry.test.sh │ rc=0 │ rc=0 │ yes
SC-29 │ 29g │ zero-regression │ bash hooks/tests/jq-crlf-guard.sh hooks/secret-guard.sh hooks/secret-scan.sh │ rc=0 │ rc=0 │ yes
SC-30 │ 30a │ zero-regression │ secret-guard.test.sh on a checkout WITH git history (SC-9a, SC-8 latency gate) -- not run by this probe, see proposal │ n/a │ not-run │ n/a
SC-31 │ 31a │ reverse-guard │ corpus_census.py patterns.total (risky_patterns rows) within budget │ patterns<=150 │ patterns=145 │ yes
SC-31 │ 31b │ reverse-guard │ corpus_census.py family_count equals the value hard-coded in secret-guard.test.sh SC-19 │ census == test-hardcoded │ census=61 test-hardcoded=61 │ yes
SC-31 │ 31c │ reverse-guard │ risky_patterns has no row made only of a "${VAR}" expansion (census blind spot) │ 0 variable-only rows │ 0 variable-only rows │ yes
SC-31 │ 31d │ reverse-guard │ hooks/hooks.json byte-identical to baseline (no matcher/registration change) │ hooks.json=baseline-identical │ hooks.json=baseline-identical │ yes
SC-31 │ 31e │ reverse-guard │ hooks/hooks.json holds no literal completeness_gate (10CG/Aria#199 seam) │ gone │ gone │ yes
SC-32 │ 32a │ reverse-guard │ hooks/secret-guard.sh + secret-scan.sh: no declare -A / mapfile / readarray / ${x,,} / ${x^^} in code │ 0 bash4-only constructs │ 0 bash4-only constructs │ yes
SC-32 │ 32b │ reverse-guard │ hooks/secret-*.sh and tests/secret-*.test.sh keep LF line endings │ LF-only │ LF-only │ yes

== per-SC match (yes/total) ==
SC-1: 0/2
SC-2: 4/4
SC-3: 2/2
SC-4: 0/13
SC-5: 0/11
SC-6: 0/7
SC-7: 7/7
SC-8: 0/1
SC-9: 21/21
SC-10: 6/6
SC-11: 14/21
SC-12: 3/6
SC-13: 3/6
SC-14: 0/2
SC-15: 5/6
SC-16: 0/11
SC-17: 10/10
SC-18: 2/6
SC-19: 6/14
SC-20: 12/12
SC-21: 13/21
SC-22: 29/64
SC-23: 13/19
SC-24: 11/16
SC-25: 3/7
SC-26: 0/2
SC-27: 2/3
SC-28: 0/11
SC-29: 7/7
SC-30: not run by this probe
SC-31: 5/5
SC-32: 2/2

== per-category match (yes/total) ==
baseline-failing: 0/131
doc-sync: 0/14
reverse-guard: 60/60
allow-guard: 88/88
known-limit: 25/25
zero-regression: 7/7
baseline shape (baseline-failing + doc-sync all 'no', every other category all 'yes'): holds
target shape (every row 'yes'): does not hold
```
