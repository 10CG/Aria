# TASK-004 第一段报告 (10CG/aria-plugin#217, secret-guard W10 尺寸误拦收窄)

执行席: TASK-004 第一段 (新实例)。本文所有贴出的输出都由 `r217impl/t004a/mkreport.sh` 重新生成, 不是手抄。真实流量的命令文本只在 scratchpad 的 `traffic-fresh/` 与 `traffic-frozen/`, 本报告与 `t004a/` 只有计数、编号与 sha256。

## 0. 结论一览

1. 语料还原: 清单 2412 条全部找到且 sha256 与字节数一致; W1 的 138、ident-300 的 300、w1-sample40 的 40 条全部找到, 缺失 0、哈希不符 0。
2. run-evidence.sh: 按 design 2、6 改完 (diff 见第 2 节); 三项检查都符合预期。design 6 的检查句有两种读法, 未自行选择, 见第 6 节第 2 条。
3. 在实现上跑 W8 W11 W9: 退出 0, 三份输出写进 `v31/impl/`, 首行页眉含两个 hook 与三个用例脚本的 sha256 前缀。
4. 验收 1 (W8): 符合。diff 原型 实现 共 6 个 hunk, 逐行都落在 INV-1 的三类里, 无其他差; 五段字面在实现里逐字出现。
5. 验收 4 (W11): 符合。18 个 (分节, 形状) 的 rc 与文案种类全部与 95cf1de7 相同。
6. 验收 3 (W9): **不一致, 已停下**。六组变化 (21ab 21ac 21ag 21aj 21al 21ao) 与 SC-13 都对上, 但 6 条变化断言里只有 5 条与 95cf1de7 逐条相同: SC-21ab 在实现上多出 3 条红 (子用例 `f=x; echo $f yyy…`: 退出码 want 2 got 0)。没有改 hook、套件或期望值。详见第 5 节与第 6 节第 1 条。

## 1. 语料还原 (design 1)

- 抽取 (`extract.py`, TRAFFIC_DIR=traffic-fresh) 与 refreeze 的原始打印 (会话内读数, 未落文件): `unique commands over 4096 bytes: 2584`; `frozen=2412 found=2412 missing=0`。
- 独立复核 (`t004a/corpus_check.py`, 按 W0 清单逐条核字节数与 sha256; 本次重跑):
```
traffic-fresh/cmds 文件数: 2584; traffic-frozen/cmds 文件数: 2412
manifest: entries 2412 found+hash-ok 2412 missing 0 hash-mismatch 0 files-in-frozen 2412
W1-138: listed 138 unique 138 found+hash-ok 138 missing 0 ids=[] hash-mismatch 0 ids=[]
ident-300: listed 300 unique 300 found+hash-ok 300 missing 0 ids=[] hash-mismatch 0 ids=[]
w1-sample40: listed 40 unique 40 found+hash-ok 40 missing 0 ids=[] hash-mismatch 0 ids=[]
```

## 2. run-evidence.sh 的改动 (design 2、6)

改动只在主仓 `v31/run-evidence.sh` (71 行 -> 81 行; 任务书写的 55 行与实际不符, HEAD 版本即 95cf1de7 版本, 之后无改动)。要点:
- `OUT` (环境变量): 默认 `$HERE` (脚本所在目录); 五处原来 `cp ... "$HERE/"` 全部改为 `"$OUT/"`; 开跑前要求 OUT 是可写目录, 否则退出 3 (不自动创建, 防止拼错路径时到处建目录)。
- 被测 bash: 按所选阶段汇总 (W13: 四个固定 bash + BASH32; W12: BASH32 + PATH 上的 bash; W11、W9: PATH 上的 bash), 任一为空、不存在或不可执行即退出 3; 检查在建工作目录之前, 所以不写任何文件。W13 的循环改用同一数组, `${BASH32:-}` 的静默跳过随之去掉。
- `hdr` 另记 `sc-cases.sh`、`sc-direct.sh`、`mutants.py` 的 sha256 前缀 (INV-8), 字段插在 `hook sha256` 之后、`load` 之前, 原有字段与顺序不变; 三个文件缺一即退出 3。
- W8: `W8-v31.diff` 第一行是页眉 (`#` 开头), diff 正文不变。
- 第 8 行 `readlink -f` -> `readlink -m`; `mkdir -p "$W"` 失败 (或 W 为空) 即退出 3。
- 预期在改动之前写在 `t004a/predictions.md`。

```diff
diff --git a/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-evidence.sh b/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-evidence.sh
index 9a5df2da..ed5bab87 100755
--- a/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-evidence.sh
+++ b/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-evidence.sh
@@ -1,24 +1,34 @@
 #!/usr/bin/env bash
 # run-evidence.sh <work dir> [W8 W13 W11 W12 W9] : regenerates the v3.1 evidence. The baseline always comes from aria 59e333c (sha256 prefix e83c5e30f2cc,
 # asserted); the hook under test is the prototype built by mkv31.py, or IMPL=<hook> (TASK-004: the real implementation; its sha256 must differ from the
-# baseline's). Every output is written into the work dir first and copied next to this script only when its stage has finished, so a failed or partial run
-# never overwrites committed evidence. Every output's first line records the date, the platform, both sha256 prefixes and the load.
-# Needs: Linux, bash 5 on PATH, jq, python3, taskset, nice; W12 also TRAFFIC_DIR (the frozen corpus, outside the repo) and BASH32 (a bash 3.2 binary).
+# baseline's). Every output is written into the work dir first and copied to OUT only when its stage has finished, so a failed or partial run never
+# overwrites committed evidence; OUT=<an existing directory> (TASK-004: v31/impl), default this script's directory, which reproduces the evidence of 95cf1de7.
+# Every output's first line records the date, the platform, the sha256 prefixes of both hooks and of sc-cases.sh, sc-direct.sh and mutants.py (INV-8) and
+# the load; the W8 diff starts with that line too (patch and git apply skip the text before a diff).
+# Needs: Linux, bash 5 on PATH, jq, python3, taskset, nice; W13 and W12 also BASH32 (a bash 3.2 binary), W12 also TRAFFIC_DIR (the frozen corpus, outside the
+# repo). A bash under test that is missing or not executable, an OUT that is not a writable directory, or a work dir that cannot be created exits 3 before
+# any file is written.
 set -u
-HERE="$(cd "$(dirname "$0")" && pwd)"; W=$(readlink -f "$1"); shift; STAGES=${*:-W8 W13 W11 W12 W9}
-ROOT=$(git -C "$HERE" rev-parse --show-toplevel); mkdir -p "$W"
+HERE="$(cd "$(dirname "$0")" && pwd)"; W=$(readlink -m "$1"); shift; STAGES=${*:-W8 W13 W11 W12 W9}; OUT=${OUT:-$HERE}
+B13=(/home/dev/.aria/tools/bash-5.0.18/bash /home/dev/.aria/tools/bash-5.1.16/bash /usr/bin/bash /home/dev/.aria/tools/bash-5.3.20/bash)   # W13: one run each, then BASH32
+NB=(); for st in $STAGES; do case $st in W13) NB+=("${B13[@]}" "${BASH32:-}");; W12) NB+=("${BASH32:-}" "$(command -v bash)");; W11|W9) NB+=("$(command -v bash)");; esac; done
+for b in "${NB[@]}"; do [[ -n "$b" && -f "$b" && -x "$b" ]] || { echo "a bash under test is missing or not executable: '$b' (W13 and W12 need BASH32)"; exit 3; }; done
+for f in sc-cases.sh sc-direct.sh mutants.py; do [[ -f "$HERE/$f" ]] || { echo "missing $HERE/$f (its sha256 goes into every header, INV-8)"; exit 3; }; done
+[[ -d "$OUT" && -w "$OUT" ]] || { echo "OUT is not a writable directory: $OUT"; exit 3; }
+ROOT=$(git -C "$HERE" rev-parse --show-toplevel); [[ -n "$W" ]] && mkdir -p "$W" || { echo "cannot create the work dir: ${W:-<empty>}"; exit 3; }
 git -C "$ROOT/aria" show 59e333c:hooks/secret-guard.sh > "$W/base.sh" && [[ "$(sha256sum < "$W/base.sh" | cut -c1-12)" == e83c5e30f2cc ]] || { echo "baseline: not e83c5e30f2cc"; exit 3; }
 if [[ -n "${IMPL:-}" ]]; then cp "$IMPL" "$W/impl.sh"; else python3 "$HERE/mkv31.py" "$W/base.sh" "$W/impl.sh" >/dev/null || exit 3; fi
 [[ "$(sha256sum < "$W/impl.sh")" != "$(sha256sum < "$W/base.sh")" ]] || { echo "the hook under test is the baseline itself"; exit 3; }
 BS=$(sha256sum < "$W/base.sh" | cut -c1-12); IS=$(sha256sum < "$W/impl.sh" | cut -c1-12)
-hdr() { printf '# %s | %s | bash %s | base sha256 %s | hook sha256 %s | load %s\n' "$(date -u +%FT%TZ)" "$(uname -sr)" "$BASH_VERSION" "$BS" "$IS" "$(cut -d' ' -f1-3 /proc/loadavg)"; }
+hdr() { printf '# %s | %s | bash %s | base sha256 %s | hook sha256 %s' "$(date -u +%FT%TZ)" "$(uname -sr)" "$BASH_VERSION" "$BS" "$IS"
+  for f in sc-cases.sh sc-direct.sh mutants.py; do printf ' | %s sha256 %s' "$f" "$(sha256sum < "$HERE/$f" | cut -c1-12)"; done; printf ' | load %s\n' "$(cut -d' ' -f1-3 /proc/loadavg)"; }
 N=(taskset -c 0,1 nice -n 19)
 for st in $STAGES; do case $st in
-W8) diff -u "$W/base.sh" "$W/impl.sh" | sed '1,2s/\t.*//' > "$W/W8-v31.diff"
+W8) { hdr; diff -u "$W/base.sh" "$W/impl.sh" | sed '1,2s/\t.*//'; } > "$W/W8-v31.diff"
     printf 'added %s (blank %s) removed %s\n' "$(grep -c '^+[^+]' "$W/W8-v31.diff")" "$(grep -c '^+$' "$W/W8-v31.diff")" "$(grep -c '^-[^-]' "$W/W8-v31.diff")" > "$W/W8-count.txt"
-    cp "$W/W8-v31.diff" "$HERE/"; echo "W8 done: $(cat "$W/W8-count.txt")" ;;
+    cp "$W/W8-v31.diff" "$OUT/"; echo "W8 done: $(cat "$W/W8-count.txt")" ;;
 W13) { hdr; echo "## 1. the hook under test, one run per bash (SC_BASH); relaxation expected on GNU/Linux bash 5.0-5.3 only"
-      for b in /home/dev/.aria/tools/bash-5.0.18/bash /home/dev/.aria/tools/bash-5.1.16/bash /usr/bin/bash /home/dev/.aria/tools/bash-5.3.20/bash ${BASH32:-}; do
+      for b in "${B13[@]}" "$BASH32"; do
         SC_BASH=$b bash "$HERE/sc-cases.sh" "$W/impl.sh" "$W/base.sh" > "$W/sc-$(basename "$(dirname "$b")").txt" 2>&1
         printf '%-28s %s | %s\n' "$("$b" -c 'echo bash $BASH_VERSION')" "$(tail -1 "$W/sc-$(basename "$(dirname "$b")").txt")" "$(head -1 "$W/sc-$(basename "$(dirname "$b")").txt" | grep -o 'relaxation expected: [a-z]*')"
         grep '^FAIL' "$W/sc-$(basename "$(dirname "$b")").txt"; done
@@ -28,7 +38,7 @@ W13) { hdr; echo "## 1. the hook under test, one run per bash (SC_BASH); relaxat
       echo "  green: $(awk '$1=="PASS"{print $2}' "$W/sc-base.txt" | tr '\n' ' ')"
       echo "## 3. the bad implementations of mutants.py (author-built: a self-check of the cases, not TASK-003), bash 5.2"
       SC_BASH=/usr/bin/bash bash "$HERE/run-mutants.sh" "$W/impl.sh" "$W/mut"; hdr; } > "$W/W13-sc-cases.txt" 2>&1
-    cp "$W/W13-sc-cases.txt" "$HERE/"; echo "W13 done" ;;
+    cp "$W/W13-sc-cases.txt" "$OUT/"; echo "W13 done" ;;
 W11) mkdir -p "$W/adv" "$W/ext/proj/.aria"; printf '%s\n' "billing/conf/prod.toml" > "$W/ext/proj/.aria/secret-guard.paths"
     for s in apply-heavy apply-heavy-seg apply-heavy-cjk shrink segfinding f5like km-ext km-ext-small; do python3 "$HERE/../v3/gen-v3.py" $s "$W/adv/$s.txt" >/dev/null; done
     L="apply-heavy apply-heavy-seg apply-heavy-cjk shrink segfinding f5like km-ext"
@@ -36,7 +46,7 @@ W11) mkdir -p "$W/adv" "$W/ext/proj/.aria"; printf '%s\n' "billing/conf/prod.tom
       for h in base impl; do echo "## $h"; ( cd "$W/adv" && LC_ALL=C.UTF-8 "${N[@]}" bash "$HERE/../v3/matrix.sh" "$W/$h.sh" $(for s in $L; do echo $s.txt; done) 2>&1 | grep -v setlocale ); done
       echo "# extension project (CLAUDE_PROJECT_DIR=<dir with .aria/secret-guard.paths listing the read path>)"
       for h in base impl; do echo "## $h"; ( cd "$W/adv" && EXTDIR="$W/ext/proj" LC_ALL=C.UTF-8 "${N[@]}" bash "$HERE/../v3/matrix.sh" "$W/$h.sh" km-ext.txt km-ext-small.txt 2>&1 | grep -v setlocale ); done
-      hdr; } > "$W/W11-adversarial.txt"; cp "$W/W11-adversarial.txt" "$HERE/"; echo "W11 done" ;;
+      hdr; } > "$W/W11-adversarial.txt"; cp "$W/W11-adversarial.txt" "$OUT/"; echo "W11 done" ;;
 W12) : "${TRAFFIC_DIR:?W12 needs TRAFFIC_DIR}" "${BASH32:?W12 needs BASH32}"; W1="$HERE/../evidence/W1-classification.tsv"
     python3 "$HERE/mkdbg31.py" "$W/impl.sh" "$W/impl-dbg.sh" >/dev/null || exit 3
     { hdr; echo "## 1. the W10 size-blocked class (W1: 138 commands; the baseline blocks all of them for size), the hook under test (instrumented copy), bash 5.2"
@@ -49,7 +59,7 @@ W12) : "${TRAFFIC_DIR:?W12 needs TRAFFIC_DIR}" "${BASH32:?W12 needs BASH32}"; W1
       "${N[@]}" bash "$HERE/ident.sh" "$W/base.sh" "$W/impl.sh" "$HERE/ident-300.lst" 2>&1 | grep -v setlocale | tail -3
       echo "## 3. bash 3.2 (no relaxation): base vs the hook under test on 40 sampled W1 commands (w1-sample40.lst)"
       "${N[@]}" bash "$HERE/ident32.sh" "$BASH32" "$W/base.sh" "$W/impl.sh" "$HERE/w1-sample40.lst" 2>&1 | grep -v setlocale | tail -3
-      hdr; } > "$W/W12-real-traffic.txt"; cp "$W/W12-real-traffic.txt" "$W/W12-replay-138.tsv" "$HERE/"; echo "W12 done" ;;
+      hdr; } > "$W/W12-real-traffic.txt"; cp "$W/W12-real-traffic.txt" "$W/W12-replay-138.tsv" "$OUT/"; echo "W12 done" ;;
 W9) HK="$W/hooks-base"; rm -rf "$HK"; git -C "$ROOT/aria" archive 59e333c hooks | tar -x -C "$W" --transform 's,^hooks,hooks-base,'
     [[ "$(sha256sum < "$HK/secret-guard.sh" | cut -c1-12)" == e83c5e30f2cc ]] || { echo "W9: archived hook is not the baseline"; exit 3; }
     for t in base impl; do rm -rf "$W/tree-$t"; mkdir -p "$W/tree-$t"; cp -r "$HK" "$W/tree-$t/hooks"; done; cp "$W/impl.sh" "$W/tree-impl/hooks/secret-guard.sh"
@@ -66,6 +76,6 @@ for ln in sys.stdin:
         chk = re.sub(r"\[[^\]]*\]", "[...]", chk, count=1)
         print("     ", chk[:220])
     if not body.startswith(tuple("0123456789")): print("     ", re.sub(r"\[[^\]]*\]", "[...]", body)[:220])
-'; done; hdr; } > "$W/W9-suite.txt"; cp "$W/W9-suite.txt" "$HERE/"; echo "W9 done" ;;
+'; done; hdr; } > "$W/W9-suite.txt"; cp "$W/W9-suite.txt" "$OUT/"; echo "W9 done" ;;
 *) echo "unknown stage $st"; exit 2 ;;
 esac; done
```

### 三项检查 (本次重跑; 预期见 predictions.md P1-P3)

- check1: rc=3 | 末行: cannot create the work dir: /r217-t004a-noparent/sub/work
  - 该路径事后存在吗: 不存在 (uid 1000, / 可写: 否)
- check1b: rc=2 | 末行: unknown stage NONE
  - 两种读法探针: 父目录不存在但建得出的路径被 mkdir -p 建出, 其中文件: base.sh impl.sh 
- check2: rc=3 | 末行: a bash under test is missing or not executable: '/nonexistent/bash32' (W13 and W12 need BASH32)
- check3: rc=3 | 末行: a bash under test is missing or not executable: '' (W13 and W12 need BASH32)
- check4: rc=3 | 末行: a bash under test is missing or not executable: '/etc/hostname' (W13 and W12 need BASH32)
- check5: rc=3 | 末行: OUT is not a writable directory: /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t004a/no-such-out
- check2-5 的工作目录事后不存在的个数: 4 / 4
- 检查期间新写的文件 (主仓证据目录与 t004a, 不计检查日志与 check1b 的探针目录): 0
- OUT 不设 (读代码): `OUT=${OUT:-$HERE}`; `"$OUT/"` 出现 5 处, 即原来的五处 `"$HERE/"`; 脚本里已无 `"$HERE/"` 目的地: 0 处

check1 (父目录不存在且建不出) 退出 3、没有写出任何文件; check2 (BASH32 指向不存在的路径跑 W12) 退出 3; OUT 不设时目的地与原来相同。check3-5 是附加的 (BASH32 不设跑 W13、BASH32 指向非可执行文件、OUT 不存在), 都退出 3。check1b 不是任务书的检查, 是为第 6 节第 2 条留的事实。

## 3. 在实现上跑 W8 W11 W9

命令: `IMPL=t004a/impl-hook.sh OUT=<主仓>/.../v31/impl taskset -c 0,1 nice -n 19 bash v31/run-evidence.sh t004a/wd-run W8 W11 W9` (impl-hook.sh 是 worktree `hooks/secret-guard.sh` 的拷贝; worktree HEAD 2893bcc、干净)。run.log:
```
load ok 0.41 after 0s (0.41 0.85 0.98)
start 21:50:10 load 0.41 0.85 0.98
W8 done: added 199 (blank 4) removed 56
W11 done
W9 done
rc=0
end 21:57:43 load 2.79 2.20 1.58
impl-hook.sh sha256 af4658b6f935; worktree hook sha256 af4658b6f935
W8-v31.diff 首行: # 2026-10-24T21:50:10Z | Linux 6.17.9-1-pve | bash 5.2.15(1)-release | base sha256 e83c5e30f2cc | hook sha256 af4658b6f935 | sc-cases.sh sha256 7d29c3cd0f5b | sc-direct.sh sha256 fb3418921bca | mutants.py sha256 2060d2e0c17f | load 0.41 0.85 0.98
W11-adversarial.txt 首行: # 2026-10-24T21:50:10Z | Linux 6.17.9-1-pve | bash 5.2.15(1)-release | base sha256 e83c5e30f2cc | hook sha256 af4658b6f935 | sc-cases.sh sha256 7d29c3cd0f5b | sc-direct.sh sha256 fb3418921bca | mutants.py sha256 2060d2e0c17f | load 0.41 0.85 0.98
W9-suite.txt 首行: # 2026-10-24T21:57:43Z | Linux 6.17.9-1-pve | bash 5.2.15(1)-release | base sha256 e83c5e30f2cc | hook sha256 af4658b6f935 | sc-cases.sh sha256 7d29c3cd0f5b | sc-direct.sh sha256 fb3418921bca | mutants.py sha256 2060d2e0c17f | load 2.79 2.20 1.58
W11 末行: # 2026-10-24T21:50:30Z | Linux 6.17.9-1-pve | bash 5.2.15(1)-release | base sha256 e83c5e30f2cc | hook sha256 af4658b6f935 | sc-cases.sh sha256 7d29c3cd0f5b | sc-direct.sh sha256 fb3418921bca | mutants.py sha256 2060d2e0c17f | load 1.05 0.97 1.01
W9 末行: # 2026-10-24T21:57:43Z | Linux 6.17.9-1-pve | bash 5.2.15(1)-release | base sha256 e83c5e30f2cc | hook sha256 af4658b6f935 | sc-cases.sh sha256 7d29c3cd0f5b | sc-direct.sh sha256 fb3418921bca | mutants.py sha256 2060d2e0c17f | load 2.79 2.20 1.58
```

### 各轮首尾负载 (1/5/15 分钟)

- 语料抽取 + refreeze: 开始 0.68 0.75 0.95, 结束 2.04 1.15 1.07 (会话内读数)。
- W8 W11 W9: 开始 0.41 0.85 0.98 (waitload 门 < 1.2 通过); W11 结束 1.05 0.97 1.01 (即 W9 开始前); W9 与整轮结束 2.79 2.20 1.58。W9 的页眉与页脚都在两遍套件跑完之后才写, 所以 W9 文件自己只记了结束读数 (原有设计, 见第 6 节第 5 条)。
- 对照: 95cf1de7 原型那一轮 W11 为 2.46 2.21 1.94 / 2.18 2.16 1.93, W9 为 3.59 3.94 3.27。

## 4. 验收 1 (W8): diff 原型 实现

原型由 `v31/mkv31.py` 从 `git show 59e333c:hooks/secret-guard.sh` 生成。先核原型: 与 95cf1de7 的 `W8-v31.diff` 去掉前两行 (路径) 后的正文逐字节相同。再逐 hunk 归类 (`t004a/classify_w8.py`: 删除行按原型行号落进 proposal 写明的原型行段或两段函数定义, 新增行按实现行号落进 proposal 字面块在实现里的位置; 两头都落不进的记 OTHER)。
```
base sha256 e83c5e30f2cc; proto (mkv31.py) sha256 9f61db0e7b8b
diff -u base proto 正文 sha256 f43bc3ee749b; 95cf1de7 W8-v31.diff 正文 sha256 f43bc3ee749b
block W1S: 12 lines, verbatim in impl at [819] (in proto: [])
block W7S-1: 2 lines, verbatim in impl at [584] (in proto: [])
block W7S-2: 2 lines, verbatim in impl at [633] (in proto: [])
block W7S-3: 19 lines, verbatim in impl at [87] (in proto: [])
block W7S-4: 2 lines, verbatim in impl at [798] (in proto: [])
What 6 line: proto 1 impl 0; _sg_relax_ok defs impl 1, _sg_relax_platform defs impl 1
H1: proto 88-99 (-12) impl 88-105 (+18) classes ['+W7S-3', '-W7S-3']
H2: proto 578-578 (-1) impl 584-585 (+2) classes ['+W7S-1', '-W7S-1']
H3: proto 626-627 (-2) impl 633-634 (+2) classes ['+W7S-2', '-W7S-2']
H4: proto 675-675 (-1) impl - (+0) classes ['-W6']
H5: proto 792-793 (-2) impl 798-799 (+2) classes ['+W7S-4', '-W7S-4']
H6: proto 815-820 (-3) impl 821-829 (+6) classes ['+W1S', '-W1S']
W7S-1: proposal quotes 1 old line(s); equal to the removed lines: True
W7S-4: proposal quotes 2 old line(s); equal to the removed lines: True
OTHER lines: 0; hunks 6; removed 21 added 30
```

逐 hunk 归类:
- H1 (原型 88-99 -> 实现 88-105): What 7 补充第 3 处, hook 头注释「Shell variable indirection」整条 (proposal 写原型 `:87-99`; 第 87 行未变, 作上下文)。
- H2 (原型 578 -> 实现 584-585): What 7 补充第 1 处, W10 块头第 3 行换成两行; 删除行与 proposal 引的旧字面逐字相同。
- H3 (原型 626-627 -> 实现 633-634): What 7 补充第 2 处, `_sg_vx_replace` 的说明。
- H4 (原型 675, 只删): What 6, 删 `[[ -z "${_SGV_V[j]}" ]] && continue` (基线 `:666` 即此行; 原型 1 处、实现 0 处)。
- H5 (原型 792-793 -> 实现 798-799): What 7 补充第 4 处, 重跑块头两行; 删除行与 proposal 引的两行旧字面逐字相同。
- H6 (原型 815-820 -> 实现 821-829): What 1 补充, `_sg_relax_ok` 与 `_sg_relax_platform` 两段 (实现里这两个函数各只定义一次, 整段与 proposal 的 bash 块逐字相同)。
- OTHER 0 行: 别无他差。另: `patch -o` 把实现的 `v31/impl/W8-v31.diff` 打到基线上, 结果与实现逐字节相同 (页眉行被跳过)。

## 5. 验收 3 (W9) 与验收 4 (W11)

```
W9 sections new ['base', 'impl'] old ['base', 'impl']
W9 base: new == old (prototype round): counts True entries True | new PASS: 813 / 814 / FAIL: 1 / 814
W9 impl: new == old (prototype round): counts True entries False | new PASS: 807 / 814 / FAIL: 7 / 814
W9 new: impl vs base changed groups ['21ab', '21ac', '21ag', '21aj', '21al', '21ao']; entries only in impl 6, only in base 0
W9 old: impl vs base changed groups ['21ab', '21ac', '21ag', '21aj', '21al', '21ao']; entries only in impl 6, only in base 0
W9 every changed entry (name + checks) equal to the prototype round: 5/6
W9 SC-13 entries: {'new-base': 1, 'new-impl': 1, 'old-base': 1, 'old-impl': 1} | all four identical: True
W11 shapes: old 18 new 18; rc+kind differ: 0
--- W9 实现节与 95cf1de7 原型节不同的条目 (逐条):
impl entry names identical and in the same order: True
ENTRY: W10 SC-21ab bf: copy limit exceeded is refused — 8193 characters: the copy is not judged, the command is block | checks old 3 new 6
   @@ -3,0 +4,3 @@
   +refused [...]: exit code: want '2', got '0'
   +refused [...]: names the limit that was hit: want 'a command segment is longer than 8192 characters after variable expansion', got ''
   +refused [...]: says to split: want 'yes', got 'no'
--- 原始输出 (wd-run/suite-impl.out) 里 SC-21ab 的子用例与红的条数:
      3   子用例前缀 f=/etc/forgejo…
      3   子用例前缀 f=x; echo $f y…
```

W9 逐条对照:
- 基线节: 新一轮与 95cf1de7 完全相同 (813/814, 唯一红为 SC-13)。
- 实现节相对基线节的变化: 恰为 21ab、21ac、21ag、21aj、21al、21ao 六组 (6 条只在实现节出现, 0 条只在基线节出现); 原型那一轮同样是这六组。
- SC-13: 新旧两轮的基线节与实现节都是同一条红 (内容逐字相同), 不算变化。
- 变化断言与原型那一轮逐条相同: 21ac、21ag、21aj、21al、21ao 五条相同; **21ab 不同**: 原型那一轮 3 条红 (子用例 1, 读配置文件那条: 放宽后整份判出 finding 文案而不是尺寸文案), 实现这一轮 6 条红, 多出的 3 条来自子用例 2 `f=x; echo $f yyy…`: 退出码 want '2' got '0'、尺寸文案 got ''、分段提示 got 'no' —— 即实现放行了这条 8193 字符的无害副本, 原型那一轮它按基线拦下。计数行相同 (807/814) 是因为两轮都是这一组整组红。

W11 逐形状 (分节 / 形状 / 原型那一轮 / 这一轮; 墙钟只列不比):
```
main	base	apply-heavy	old rc=2 oversize(the command is longer than ) wall=0.36	new rc=2 oversize(the command is longer than ) wall=0.38	same
main	base	apply-heavy-cjk	old rc=2 oversize(the command is longer than ) wall=1.97	new rc=2 oversize(the command is longer than ) wall=2.00	same
main	base	apply-heavy-seg	old rc=2 oversize(the command is longer than ) wall=0.41	new rc=2 oversize(the command is longer than ) wall=0.43	same
main	base	f5like	old rc=2 oversize(a command segment is longer t) wall=0.74	new rc=2 oversize(a command segment is longer t) wall=0.75	same
main	base	km-ext	old rc=2 oversize(the command is longer than ) wall=0.14	new rc=2 oversize(the command is longer than ) wall=0.15	same
main	base	segfinding	old rc=2 oversize(a command segment is longer t) wall=0.69	new rc=2 oversize(a command segment is longer t) wall=0.68	same
main	base	shrink	old rc=2 oversize(the command is longer than ) wall=0.11	new rc=2 oversize(the command is longer than ) wall=0.09	same
main	impl	apply-heavy	old rc=2 oversize(the command is longer than ) wall=3.02	new rc=2 oversize(the command is longer than ) wall=3.02	same
main	impl	apply-heavy-cjk	old rc=2 oversize(the command is longer than ) wall=3.04	new rc=2 oversize(the command is longer than ) wall=3.04	same
main	impl	apply-heavy-seg	old rc=2 oversize(the command is longer than ) wall=3.02	new rc=2 oversize(the command is longer than ) wall=3.02	same
main	impl	f5like	old rc=2 oversize(a command segment is longer t) wall=3.02	new rc=2 oversize(a command segment is longer t) wall=3.01	same
main	impl	km-ext	old rc=0 - wall=0.32	new rc=0 - wall=0.24	same
main	impl	segfinding	old rc=2 finding wall=1.18	new rc=2 finding wall=1.11	same
main	impl	shrink	old rc=0 - wall=0.17	new rc=0 - wall=0.15	same
ext	base	km-ext	old rc=2 oversize(the command is longer than ) wall=0.22	new rc=2 oversize(the command is longer than ) wall=0.15	same
ext	base	km-ext-small	old rc=2 ext-finding wall=0.16	new rc=2 ext-finding wall=0.09	same
ext	impl	km-ext	old rc=2 oversize(the command is longer than ) wall=0.26	new rc=2 oversize(the command is longer than ) wall=0.15	same
ext	impl	km-ext-small	old rc=2 ext-finding wall=0.27	new rc=2 ext-finding wall=0.10	same
```

## 6. 未完成、不一致与拿不准的项

1. **W9 (验收 3) 不一致, 已按任务书停下**: SC-21ab 子用例 2 在实现上放行 (rc 0), 在 95cf1de7 原型那一轮被拦 (rc 2)。没有改 hook、套件或期望值, 也没有补跑实验。推测 (未验证): 放宽重跑受时间预算与硬截止约束, 原型那一轮 W9 在负载 3.59 3.94 3.27 下跑 (高于 INV-7 的 2), 这条子用例可能因时间不足回落到基线而被拦; 这一轮 W9 开始时约 1.05, 放宽生效后放行 (这正是放宽要放行的形状)。反方向的可能 (实现与原型在这条路径上行为不同, 违反 INV-1/INV-3) 未排除。建议主控在低负载下用 OUT 指向 scratchpad 各跑一次原型 (不设 IMPL) 与实现的 W9 (或只跑 SC-21ab), 看子用例 2 是否随负载翻转; 是否按 INV-7 把 W9 当计时类重判, 由主控定。
2. **design 6 的检查句有两种读法, 未选择**: design 6 写「改 readlink -m, 并核 mkdir -p 成功, 否则退出 3; 用父目录不存在的工作目录跑一次, 须在写任何文件前退出 3」。照字面实现 (mkdir -p) 后, 父目录不存在但建得出的路径会被建出并继续跑 (check1b: 建出目录、写出 base.sh 与 impl.sh、因未知阶段退出 2), 只有建不出的路径 (check1, / 下, uid 1000) 才在写任何文件前退出 3。读法 A: 检查指建不出的路径, 现实现满足; 读法 B: 父目录不存在就该拒绝, 则要改掉 mkdir -p (例如先核父目录存在), 与 design 6 的字面冲突。按读法 A 交付, 请主控裁定。
3. **W8 页眉与「默认 OUT 复现 95cf1de7 证据」之间的张力**: W8 加页眉后, 不设 OUT 重跑会把带页眉 (含日期与负载) 的 `W8-v31.diff` 写回 `v31/`, 与 95cf1de7 的那份 (sha256 9fc20fdbb419) 不再逐字节相同, 正文 (第 2 行起) 仍相同。本段只用 OUT=v31/impl, 未触动 v31/ 下的原型证据。
4. proposal 头部写「原型 (`v31/W8-v31.diff`, sha256 前缀 `9f61db0e7b8b`)」: 9f61db0e7b8b 是 mkv31.py 生成的原型 hook 本身的 sha256; `W8-v31.diff` 文件的 sha256 是 9fc20fdbb419。只是措辞, 不影响对照。
5. W9 阶段的两次 `hdr` 都在两遍套件跑完之后, 文件里没有开始负载 (INV-7 要求开始与结束各记一次); 这一轮靠 W11 页脚补开始读数。W9 的结束读数 2.79 >= 2。另外 W12 的 `W12-replay-138.tsv` 没有页眉行 (INV-8 说每份输出首行记哈希), W12 阶段的 TRAFFIC_DIR 缺失仍是 `:?` (退出 1, 且在前面阶段跑完之后才报)。这三处都是原有设计、属第二段或主控判断, 本段未改。
6. `git apply` 直接吃 `W8-v31.diff` 需要路径选项: diff 头里是工作目录的绝对路径 (原有, 95cf1de7 相同), 与页眉无关; 页眉被跳过已用 `patch -o` 验证。
7. 真实流量的 `traffic-fresh/` 与 `traffic-frozen/` 留在 scratchpad 没删: 第二段的 W12 要用 (TRAFFIC_DIR=traffic-frozen); 按计划会话结束时删除。
8. 未 commit (任务书要求)。主仓 git status: run-evidence.sh 已改, `v31/impl/` 新增 W8-v31.diff、W11-adversarial.txt、W9-suite.txt; `v31/impl/` 原有的 W14 文件未动。

## 7. 过程材料 (`r217impl/t004a/`, 不含任何命令文本)

predictions.md (预期, 先写), corpus_check.py, classify_w8.py, compare.py, w9diff.py, waitload.sh, waitdone.sh, mkreport.sh, run.log, check*.log, base.sh / proto.sh / impl-hook.sh, proto-impl.diff, w11-table.tsv, old-W9.txt / old-W11.txt / old-suite.sh (取自 git), wd-run/ (本轮工作目录), patchcheck/, probe-noparent/, outprobe/。

git status (主仓, 生成本报告时):
```
 M .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-evidence.sh
?? .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/W11-adversarial.txt
?? .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/W8-v31.diff
?? .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/W9-suite.txt
```

## 8. 预期 (predictions.md, 先写) 与实际

- P0 (改动面、语法): 符合。
- P1 (父目录不存在且建不出 -> 退出 3、无文件): 符合 (check1)。
- P1b (两种读法探针, 建得出的路径被建出、退出 2): 符合 (check1b), 事实留给第 6 节第 2 条裁定。
- P2 / P2b (BASH32 缺失或不可执行 -> 退出 3, 不起重实验): 符合 (check2-4)。
- P3 (OUT 不设时目的地同原来): 符合 (读代码 + 计数)。
- P4 (三阶段 done、退出 0、页眉含五个前缀): 符合。
- P5 (验收 1): 符合; 原型重现 95cf1de7 的 W8 正文, 6 个 hunk 全归三类, OTHER 0。
- P6 (验收 3): **不符合一项**: 六组变化、SC-13、基线节都对上; 变化断言 5/6 与原型那一轮相同, SC-21ab 多 3 条红 (第 5、6 节)。
- P7 (验收 4): 符合, 18/18。

本段工具调用: 共 19 次 (上限 50)。
