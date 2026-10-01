#!/usr/bin/env python3
"""compose deliver/baseline-evidence.md from the final run outputs (E1a = the pasted stdout; E1b / E2 only feed the prose numbers).
usage: python3 mk_evidence.py"""
import difflib
import hashlib
import re

D = "/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v2/final/"


def rd(p):
    return open(D + p, "rb").read()


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16]


e1a, e1b, e2 = rd("E1a.out"), rd("E1b.out"), rd("E2.out")
assert e1a == e1b, "E1a and E1b differ"
for n in ("E1a", "E1b", "E2"):
    assert rd(n + ".err") == b"", n + ".err not empty"
    assert rd(n + ".rc").strip() == b"rc=0", n
txt = e1a.decode("utf-8")
assert "```" not in txt
assert "baseline shape (baseline-failing + doc-sync all 'no', every other category all 'yes'): holds" in txt
t2 = e2.decode("utf-8")
assert "baseline shape (baseline-failing + doc-sync all 'no', every other category all 'yes'): holds" in t2

# E1 vs E2: which lines differ
a, b = txt.split("\n"), t2.split("\n")
diff = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
row_changes = sorted({re.match(r"^[-+](SC-\d+ │ \w+)", l).group(1) for l in diff if re.match(r"^[-+]SC-\d+ │ ", l)})
print("E1 vs E2 changed rows:", row_changes)
print("E1 vs E2 changed non-row lines:", [l for l in diff if not re.match(r"^[-+]SC-\d+ │ ", l)])

rows = len(re.findall(r"(?m)^SC-\d+ │ ", txt))
n32c = re.search(r"identical over (\d+) hook-direct rows", txt).group(1)

sha_e1, by_e1, sha_e2, by_e2 = sha(e1a), len(e1a), sha(e2), len(e2)

md = f"""# baseline-evidence: secret-net-l3-and-bypass-paths

> 本文件 = 同目录 `baseline_probe.py` 在冻结基线上的实跑 stdout (原样粘贴, 未改一个字符) + 复现说明。`proposal.md` 里 SC 的「基线」值都取自下方输出 (SC-30 除外, 它不由本探针执行)。

## 基线与环境

- 基线: aria `268da8f39d8bc33967e7cdaa5681e3a221fb9e4b` (= v1.74.1); standards `2bc1c4c619c5125a1bb2963864c1683fd9a87739`; 主仓 `0748dbc` (起草时)。
- 被测文件指纹见输出第 2–6 行 (sha256 前 16 位): `hooks/secret-guard.sh` `448b1f71a2af06d7`、`hooks/secret-scan.sh` `c5f53f7a164fa72e`、`hooks/tests/secret-guard.test.sh` `72f8e7d5d58a4b80`、`hooks/tests/secret-scan.test.sh` `78e0e4ca15078177`、`standards/conventions/secret-hygiene.md` `dcf203f1f25ef0c0`。
- 环境: Linux 6.17.9-1-pve, Python 3.11.2, GNU bash 5.2.15 (默认 bash), jq 1.6, GNU grep 3.8, GNU sed 4.9, perl 5.36.0; 本机无 zsh; `C.UTF-8` locale 可用; 真 GNU bash 3.2.57(2) 见下节。实跑日期 2026-10-01。

## 取得真 bash 3.2 (`WPA_BASH32`)

SC-29 29h / 29i 与 SC-32 32c 需要一个真 bash 3.2 (Debian / Ubuntu 的 `bash` 包是 5.x, macOS 自带的 3.2.57 不可在 Linux 容器里取得)。无 root、可联网时从源码构建, 约 4 分钟:

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

1. 布局: 探针按 `<aria>/../standards` 找 standards, 按自身所在目录找 `proposal.md`。本次把 `/home/dev/Aria/aria` 与 `/home/dev/Aria/standards` 用 `cp -a` 复制到实验目录 `<X>/base/` 下, 探针与 `proposal.md` 放在同一目录 (即落盘后的 `openspec/changes/secret-net-l3-and-bypass-paths/`)。
2. 命令 (本输出): `WPA_BASH32=<bash 3.2 路径> TMPDIR=<X>/tmp python3 baseline_probe.py <X>/base/aria`。`TMPDIR` 只决定探针私有临时目录的位置 (结束时删除), 不进输出。不带 `WPA_BASH32` 时 29h / 29i / 32c 三行打印 `not-run` (match 为 `n/a`), 除这三行与末尾的计数行外, 输出与本输出逐字节相同。
3. 带 `WPA_BASH32` 连跑两次, stdout 逐字节相同 (sha256 前 16 位 `{sha_e1}`, {by_e1} 字节), stderr 为空; 不带 `WPA_BASH32` 跑一次: sha256 前 16 位 `{sha_e2}`, {by_e2} 字节, stderr 为空, 基线形态同样 `holds`。单次约 7–10 分钟 (两个测试套件各在默认 bash 与 3.2 下跑一遍, 占大头; 两个探针运行并发时约 9 分钟)。
4. 比对注意: 若 standards 不在 `<aria>/../standards`, SC-26 / SC-27 / SC-28 中读 standards 的行会打印 `standards-absent`; 若探针旁没有 `proposal.md`, SC-15 15e 打印 `proposal.md-absent`。本输出只在复制出的副本上实测过; 对真 checkout 的 `aria/` 跑时, 套件同样在去掉 `.git` 的私有副本里执行。SC-20 20g (不可读文件) 在 root 下不可构造, 本输出由非 root 用户产生。

## 读法

- 列: SC │ 用例 │ 类别 │ 输入形态 (占位描述) │ 期望 (目标态) │ 实得 │ 符合 (`yes` / `no`; `n/a` = 本探针不执行或在本环境不可构造)。共 {rows} 行。
- **基线形态**: `baseline-failing` 与 `doc-sync` 行应全部 `no`, 其余类别 (`reverse-guard` / `allow-guard` / `known-limit` / `zero-regression`) 应全部 `yes`; 输出末尾两行由探针机算该不变量 —— 本次 `holds`。实现完成后同一探针应输出「target shape … holds」。
- SC-30 一行不执行 (`n/a`), 理由见 `proposal.md` SC-30。SC-32 32c 一行在基线上比对 {n32c} 个 hook-direct 行。
- **多用例行** (`l3m` / `l1m` 一类) 是同一类别下若干独立 hook 运行的 AND, `actual` 列逐个列出, 红了仍能指出是哪一个。
- 确定性措施: 像凭据的值在进程内由 `secrets` 生成, 生成时保证字符类与首字符 / 前缀性质 (判定不随随机值变化); hook 的环境变量从零构造 (不继承调用方的 `CLAUDE_PROJECT_DIR` 等); 测试套件在去掉 `.git` 的私有副本里跑、设 `GIT_CEILING_DIRECTORIES`、PATH 中隐去 zsh, 因此 `secret-guard.test.sh` 里依赖 git 历史的测试内 SC-9a / SC-8 与 zsh 用例被跳过 (实得里的 `581/582` 与唯一 FAIL 即此伪影, 见 `proposal.md` SC-29)。
- Rule #7: 输出只有退出码、是否告警、tag 名与计数, 没有任何值; 输入形态一律用占位描述。

## 实跑 stdout (原样)

```text
{txt.rstrip(chr(10))}
```
"""
open(D + "deliver/baseline-evidence.md", "w", encoding="utf-8", newline="").write(md)
print("written", len(md.encode()), "bytes; stdout block", by_e1, "bytes sha", sha_e1, "| E2", by_e2, sha_e2, "| rows", rows, "| 32c rows", n32c)
