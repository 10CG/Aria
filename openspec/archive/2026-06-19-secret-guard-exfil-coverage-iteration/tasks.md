# Tasks — secret-guard-exfil-coverage-iteration

> ✅ SHIPPED 2026-06-19 (v1.47.0, PR #88 `281388d`)。aria-plugin #69; target v1.47.0。RED-first: 先把 11 探针加进测试 corpus (RED=ALLOW 失败), 再扩 regex 至全 BLOCK + 零回归。

## TG-0 — RED corpus (test-first) ✅
- [x] 0.1. `tests/secret-guard.test.sh` 新增 16 个期望 BLOCK + 4 个 FP-guard ALLOW: FN1-5 + rsync/base64/dd/cp ssh-key + tar|ssh + wget --post-file + kubectl bash-c。
- [x] 0.2. RED 确认: 精确 16 新 BLOCK 用例 FAIL (ALLOW), 225 既有 + 4 FP guard PASS (229/245)。

## TG-A — 密钥/凭据文件覆盖加宽 (FN1, FN2, base64/dd/cp key)
- [x] A1. 397 行 Bash reader regex: 工具集加 `base64`; key 名 `id_rsa|id_ed25519|id_ecdsa` → `id_[A-Za-z0-9_]+`; 目标集加 `\.docker/config\.json`。
- [x] A2. 174 行 Read/Edit `lower_path` regex 同步: 加 `\.ssh/id_[a-z0-9_]+$`(或等效) + `\.docker/config\.json$` (Bash↔Read parity 不变式)。
- [x] A3. `dd if=` (410 行) + 新增 `cp` 目标加 key 文件类 (`id_[A-Za-z0-9_]+|\.pem|\.key|...`)。

## TG-B — Vault HTTP API (FN3)
- [x] B1. risky_patterns 加 `X-Vault-Token:` header 形 + `hvs\.[A-Za-z0-9]{6,}` token 字面。

## TG-C — kubectl 间接 shell 包裹 (FN4)
- [x] C1. 444-446 行同级加 `kubectl exec ... -- ... sh -c .*(env|printenv|cat)` (兼顾 `sh -c`/`bash -c`)。

## TG-D — exfil-to-destination 加宽 (FN5, rsync/cp/tar|ssh/wget)
- [x] D1. 539-540 行 scp/rsync: 目标加 key 文件类 + 覆盖 download 形 (`host:/path/secret .`)。
- [x] D2. 新增 `tar ... ~/.ssh ... | (ssh|nc|curl)` 外传。
- [x] D3. 新增 `wget --post-file=` + 补 `cp` key 文件到本地目录。
- [x] D4. 注释重申 R3-C-8 威胁模型扩展边界 (exfil-to-destination = defense-in-depth)。

## TG-A..D — regex 实现 ✅
- [x] A1/A2. 397 行 reader +base64 +`\.ssh/id_[A-Za-z0-9_]+` +`.docker/config.json`; 174 行 Read/Edit 同步 (Bash↔Read parity)。
- [x] A3. dd if= key 文件 pattern。
- [x] B1. `X-Vault-Token:` + `hvs\.[A-Za-z0-9]{6,}`。
- [x] C1. kubectl `-- (sh|bash) -c .*(env|printenv|cat)`。
- [x] D1-D3. scp/rsync key (download+upload) + `\bcp` key + tar .ssh|ssh + wget --post-file。
- [x] D4. 注释重申 R3-C-8 威胁模型扩展边界。

## TG-E — 验证 (Rule #6 substitute) ✅
- [x] E1. 全 16 RED 用例转 GREEN (BLOCK)。
- [x] E2. 全 corpus 245/245 零回归。
- [x] E3. FP sanity: `cp ./src/a.txt ...` / `scp host:index.html .` / `tar ./dist` / `echo|base64` / `ls` / `git status` 仍 ALLOW。
- [x] E4. 真 hook dogfood: triage driver 重跑 16/16 BLOCK + benign ALLOW。

## Phase B/C/D
- [x] 代码 review (agent team: code-reviewer + silent-failure-hunter — 重点 ReDoS / over-block FP / 跨管道误吞)。
- [x] aria submodule 分支 → PR → merge → 双远程 parity。
- [x] 主仓 gitlink + 5 SOT v1.47.0 + CHANGELOG + i18n badge。
- [x] close #69 (comment + PATCH state) + 归档 Spec。
