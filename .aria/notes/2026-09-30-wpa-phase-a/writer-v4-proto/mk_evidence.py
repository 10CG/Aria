#!/usr/bin/env python3
"""mk_evidence.py -- compose deliver/baseline-evidence.md from the final baseline probe stdout files.

usage: python3 mk_evidence.py <stdout WITH WPA_BASH32 (pasted)> <stdout WITHOUT WPA_BASH32> <out evidence.md> [<2nd stdout WITH WPA_BASH32>]

The pasted block is the first file byte for byte; the second and third files only feed the prose numbers (sha256 prefix, size, differing lines).
If a 2nd WITH-run is given it must be byte-equal to the first (reproducibility); the prose then says the stdout is byte-equal over two runs."""
import difflib
import hashlib
import re
import sys

a_path, n_path, out_path = sys.argv[1:4]
b_path = sys.argv[4] if len(sys.argv) > 4 else None


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16]


A, N = open(a_path, "rb").read(), open(n_path, "rb").read()
if b_path:
    B = open(b_path, "rb").read()
    assert A == B, "the two WITH-runs differ"
txt, tn = A.decode("utf-8"), N.decode("utf-8")
assert "```" not in txt
SHAPE = "baseline shape (baseline-failing + doc-sync all 'no', every other category all 'yes'): holds"
assert SHAPE in txt, "baseline shape does not hold (WITH run)"
assert SHAPE in tn or "baseline shape (baseline-failing + doc-sync all 'no', every other category all 'yes'): holds [" in tn, "baseline shape does not hold (WITHOUT run)"

diff = [l for l in difflib.unified_diff(txt.split("\n"), tn.split("\n"), lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
row_changes = sorted({re.match(r"^[-+](SC-\d+ │ \w+)", l).group(1) for l in diff if re.match(r"^[-+]SC-\d+ │ ", l)})
other = [l for l in diff if not re.match(r"^[-+]SC-\d+ │ ", l)]
print("WITH vs WITHOUT changed rows:", row_changes)
print("WITH vs WITHOUT changed non-row lines:", len(other))

rows = len(re.findall(r"(?m)^SC-\d+ │ ", txt))
n32c = re.search(r"identical over (\d+) hook-direct rows", txt).group(1)
heads = {m.group(1): m.group(2) for m in re.finditer(r"(?m)^measured (\S+)\s+sha256\[:16\] = ([0-9a-f]{16}|absent)$", txt)}
cats = dict(re.findall(r"(?m)^(baseline-failing|doc-sync|reverse-guard|allow-guard|known-limit|zero-regression): (\d+/\d+)$", txt))
sha_a, by_a, sha_n, by_n = sha(A), len(A), sha(N), len(N)
runs = "连跑两次, stdout 逐字节相同" if b_path else "跑了一次"
rows_changed = " / ".join(r.replace(" │ ", " ") for r in row_changes)

md = f"""# baseline-evidence: secret-net-l3-and-bypass-paths

> 本文件 = 同目录 `baseline_probe.py` 在冻结基线上的实跑 stdout (原样粘贴, 未改一个字符) + 复现说明。`proposal.md` 里 SC 的「基线」值都取自下方输出 (SC-30 除外, 它不由本探针执行)。

## 基线与环境

- 基线: aria `268da8f39d8bc33967e7cdaa5681e3a221fb9e4b` (= v1.74.1); standards `2bc1c4c619c5125a1bb2963864c1683fd9a87739`; 主仓 `0748dbc` (起草时)。
- 被测文件指纹见输出第 2–6 行 (sha256 前 16 位): `hooks/secret-guard.sh` `{heads.get('hooks/secret-guard.sh')}`、`hooks/secret-scan.sh` `{heads.get('hooks/secret-scan.sh')}`、`hooks/tests/secret-guard.test.sh` `{heads.get('hooks/tests/secret-guard.test.sh')}`、`hooks/tests/secret-scan.test.sh` `{heads.get('hooks/tests/secret-scan.test.sh')}`、`standards/conventions/secret-hygiene.md` `{heads.get('standards/conventions/secret-hygiene.md')}`。
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
3. 带 `WPA_BASH32` {runs} (sha256 前 16 位 `{sha_a}`, {by_a} 字节), stderr 为空; 不带 `WPA_BASH32` 跑一次: sha256 前 16 位 `{sha_n}`, {by_n} 字节, stderr 为空, 基线形态同样 `holds`。空闲主机上单次约 10–12 分钟 (两个测试套件各在默认 bash 与 3.2 下跑一遍, 占大头; 32c / 32d 各把 hook 直调行再跑两遍; 两个探针运行并发或主机负载高时可到 25 分钟以上)。
4. 比对注意: 若 standards 不在 `<aria>/../standards`, SC-26 / SC-27 / SC-28 中读 standards 的行会打印 `standards-absent`; 若探针旁没有 `proposal.md` 或本文件, SC-15 15e / 15g 打印 `…-absent`。本输出只在复制出的副本上实测过; 对真 checkout 的 `aria/` 跑时, 套件同样在去掉 `.git` 的私有副本里执行。SC-20 20g (不可读文件) 在 root 下不可构造, 本输出由非 root 用户产生。

## 读法

- 列: SC │ 用例 │ 类别 │ 输入形态 (占位描述) │ 期望 (目标态) │ 实得 │ 符合 (`yes` / `no`; `n/a` = 本探针不执行或在本环境不可构造)。共 {rows} 行 (类别计数见输出末尾)。
- **基线形态**: `baseline-failing` 与 `doc-sync` 行应全部 `no`, 其余类别 (`reverse-guard` / `allow-guard` / `known-limit` / `zero-regression`) 应全部 `yes`; 输出末尾的形态行由探针机算该不变量 —— 本次 `holds`。实现完成后同一探针应输出「target shape … holds」。
- SC-30 一行不执行 (`n/a`), 理由见 `proposal.md` SC-30。SC-32 32c 一行在基线上比对 {n32c} 个 hook-direct 行, 32d 对同一批行在第二个 locale 下再跑默认 bash 与真 bash 3.2 各一遍并逐行比对。
- **多用例行** (`l3m` / `l1m` 一类) 是同一类别下若干独立 hook 运行的 AND, `actual` 列逐个列出, 红了仍能指出是哪一个; **枚举行** (`actual` 为 `N/N as expected`, 红了点名前 6 个出错的成员) 是同一类的一个枚举集合, 每个成员一次独立 hook 运行。
- 确定性措施: 像凭据的值在进程内由 `secrets` 生成, 生成时保证字符类与首字符 / 形态性质 (判定不随随机值变化); hook 的环境变量从零构造 (不继承调用方的 `CLAUDE_PROJECT_DIR` 等); 测试套件在去掉 `.git` 的私有副本里跑、设 `GIT_CEILING_DIRECTORIES`、PATH 中隐去 zsh, 因此 `secret-guard.test.sh` 里依赖 git 历史的测试内 SC-9a / SC-8 与 zsh 用例被跳过 (实得里的 `581/582` 与唯一 FAIL 即此伪影, 见 `proposal.md` SC-29)。
- Rule #7: 输出只有退出码、是否告警、tag 名与计数, 没有任何值; 输入形态一律用占位描述。

## 实跑 stdout (原样)

```text
{txt.rstrip(chr(10))}
```
"""
open(out_path, "w", encoding="utf-8", newline="").write(md)
print("written", out_path, len(md.encode()), "bytes; stdout block", by_a, "bytes sha", sha_a, "| without b32", by_n, sha_n, "| rows", rows, "| 32c rows", n32c)
print("category tallies:", cats)
