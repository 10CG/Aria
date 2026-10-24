#!/usr/bin/env bash
# mkreport.sh: writes T004a-report.md; every pasted output below is regenerated here, not hand-copied
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; T=$S/r217impl/t004a; RPT=$S/r217impl/T004a-report.md
E=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing; R=$E/v31/run-evidence.sh; P=/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
N=(taskset -c 0,1 nice -n 19)
chk() { local name=$1; shift; "$@" > "$T/$name.log" 2>&1; local rc=$?; echo "- $name: rc=$rc | 末行: $(tail -1 "$T/$name.log" | cut -c1-150)"; }
{
cat <<'TXT'
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
TXT
echo '```'; echo "traffic-fresh/cmds 文件数: $(ls "$S/traffic-fresh/cmds" | wc -l); traffic-frozen/cmds 文件数: $(ls "$S/traffic-frozen/cmds" | wc -l)"
(cd "$E" && python3 -I "$T/corpus_check.py" evidence/W0-corpus-manifest.tsv "$S/traffic-frozen" W1-138,evidence/W1-classification.tsv,0 ident-300,v31/ident-300.lst,0 w1-sample40,v31/w1-sample40.lst,0); echo '```'
cat <<'TXT'

## 2. run-evidence.sh 的改动 (design 2、6)

改动只在主仓 `v31/run-evidence.sh` (71 行 -> 81 行; 任务书写的 55 行与实际不符, HEAD 版本即 95cf1de7 版本, 之后无改动)。要点:
- `OUT` (环境变量): 默认 `$HERE` (脚本所在目录); 五处原来 `cp ... "$HERE/"` 全部改为 `"$OUT/"`; 开跑前要求 OUT 是可写目录, 否则退出 3 (不自动创建, 防止拼错路径时到处建目录)。
- 被测 bash: 按所选阶段汇总 (W13: 四个固定 bash + BASH32; W12: BASH32 + PATH 上的 bash; W11、W9: PATH 上的 bash), 任一为空、不存在或不可执行即退出 3; 检查在建工作目录之前, 所以不写任何文件。W13 的循环改用同一数组, `${BASH32:-}` 的静默跳过随之去掉。
- `hdr` 另记 `sc-cases.sh`、`sc-direct.sh`、`mutants.py` 的 sha256 前缀 (INV-8), 字段插在 `hook sha256` 之后、`load` 之前, 原有字段与顺序不变; 三个文件缺一即退出 3。
- W8: `W8-v31.diff` 第一行是页眉 (`#` 开头), diff 正文不变。
- 第 8 行 `readlink -f` -> `readlink -m`; `mkdir -p "$W"` 失败 (或 W 为空) 即退出 3。
- 预期在改动之前写在 `t004a/predictions.md`。

```diff
TXT
git -C /home/dev/Aria diff -- "$R"; echo '```'
cat <<'TXT'

### 三项检查 (本次重跑; 预期见 predictions.md P1-P3)

TXT
touch "$T/mark2"; rm -rf "$T/probe-noparent"
chk check1 env IMPL="$T/impl-hook.sh" OUT="$T/outprobe" timeout 60 "${N[@]}" bash "$R" /r217-t004a-noparent/sub/work W8
echo "  - 该路径事后存在吗: $([ -e /r217-t004a-noparent ] && echo 存在 || echo 不存在) (uid $(id -u), / 可写: $([ -w / ] && echo 是 || echo 否))"
chk check1b env IMPL="$T/impl-hook.sh" OUT="$T/outprobe" timeout 60 "${N[@]}" bash "$R" "$T/probe-noparent/sub/work" NONE
echo "  - 两种读法探针: 父目录不存在但建得出的路径被 mkdir -p 建出, 其中文件: $(ls "$T/probe-noparent/sub/work" | tr '\n' ' ')"
chk check2 env BASH32=/nonexistent/bash32 TRAFFIC_DIR="$S/traffic-frozen" IMPL="$T/impl-hook.sh" OUT="$T/outprobe" timeout 60 "${N[@]}" bash "$R" "$T/wd-check2" W12
chk check3 env -u BASH32 IMPL="$T/impl-hook.sh" OUT="$T/outprobe" timeout 60 "${N[@]}" bash "$R" "$T/wd-check3" W13
chk check4 env BASH32=/etc/hostname IMPL="$T/impl-hook.sh" OUT="$T/outprobe" timeout 60 "${N[@]}" bash "$R" "$T/wd-check4" W13
chk check5 env IMPL="$T/impl-hook.sh" OUT="$T/no-such-out" timeout 60 "${N[@]}" bash "$R" "$T/wd-check5" W8
echo "- check2-5 的工作目录事后不存在的个数: $(for d in 2 3 4 5; do [ -e "$T/wd-check$d" ] || echo x; done | wc -l) / 4"
echo "- 检查期间新写的文件 (主仓证据目录与 t004a, 不计检查日志与 check1b 的探针目录): $(find "$E" "$T" -newer "$T/mark2" -type f ! -path "$T/probe-noparent/*" ! -name 'check*.log' | wc -l)"
echo "- OUT 不设 (读代码): \`$(grep -o 'OUT=${OUT:-$HERE}' "$R")\`; \`\"\$OUT/\"\` 出现 $(grep -c -F '"$OUT/"' "$R") 处, 即原来的五处 \`\"\$HERE/\"\`; 脚本里已无 \`\"\$HERE/\"\` 目的地: $(grep -c -F '"$HERE/"' "$R") 处"
cat <<'TXT'

check1 (父目录不存在且建不出) 退出 3、没有写出任何文件; check2 (BASH32 指向不存在的路径跑 W12) 退出 3; OUT 不设时目的地与原来相同。check3-5 是附加的 (BASH32 不设跑 W13、BASH32 指向非可执行文件、OUT 不存在), 都退出 3。check1b 不是任务书的检查, 是为第 6 节第 2 条留的事实。

## 3. 在实现上跑 W8 W11 W9

命令: `IMPL=t004a/impl-hook.sh OUT=<主仓>/.../v31/impl taskset -c 0,1 nice -n 19 bash v31/run-evidence.sh t004a/wd-run W8 W11 W9` (impl-hook.sh 是 worktree `hooks/secret-guard.sh` 的拷贝; worktree HEAD 2893bcc、干净)。run.log:
```
TXT
cut -c1-160 "$T/run.log" | grep -v '^\[1\]'
echo "impl-hook.sh sha256 $(sha256sum < "$T/impl-hook.sh" | cut -c1-12); worktree hook sha256 $(sha256sum < "$S/wt217/aria/hooks/secret-guard.sh" | cut -c1-12)"
for f in W8-v31.diff W11-adversarial.txt W9-suite.txt; do echo "$f 首行: $(head -1 "$E/v31/impl/$f" | cut -c1-260)"; done
echo "W11 末行: $(tail -1 "$E/v31/impl/W11-adversarial.txt" | cut -c1-260)"; echo "W9 末行: $(tail -1 "$E/v31/impl/W9-suite.txt" | cut -c1-260)"; echo '```'
cat <<'TXT'

### 各轮首尾负载 (1/5/15 分钟)

- 语料抽取 + refreeze: 开始 0.68 0.75 0.95, 结束 2.04 1.15 1.07 (会话内读数)。
- W8 W11 W9: 开始 0.41 0.85 0.98 (waitload 门 < 1.2 通过); W11 结束 1.05 0.97 1.01 (即 W9 开始前); W9 与整轮结束 2.79 2.20 1.58。W9 的页眉与页脚都在两遍套件跑完之后才写, 所以 W9 文件自己只记了结束读数 (原有设计, 见第 6 节第 5 条)。
- 对照: 95cf1de7 原型那一轮 W11 为 2.46 2.21 1.94 / 2.18 2.16 1.93, W9 为 3.59 3.94 3.27。

## 4. 验收 1 (W8): diff 原型 实现

原型由 `v31/mkv31.py` 从 `git show 59e333c:hooks/secret-guard.sh` 生成。先核原型: 与 95cf1de7 的 `W8-v31.diff` 去掉前两行 (路径) 后的正文逐字节相同。再逐 hunk 归类 (`t004a/classify_w8.py`: 删除行按原型行号落进 proposal 写明的原型行段或两段函数定义, 新增行按实现行号落进 proposal 字面块在实现里的位置; 两头都落不进的记 OTHER)。
```
TXT
echo "base sha256 $(sha256sum < "$T/base.sh" | cut -c1-12); proto (mkv31.py) sha256 $(sha256sum < "$T/proto.sh" | cut -c1-12)"
echo "diff -u base proto 正文 sha256 $(diff -u "$T/base.sh" "$T/proto.sh" | sed '1,2s/\t.*//' | tail -n +3 | sha256sum | cut -c1-12); 95cf1de7 W8-v31.diff 正文 sha256 $(git -C /home/dev/Aria show 95cf1de7:.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/W8-v31.diff | tail -n +3 | sha256sum | cut -c1-12)"
diff -u "$T/proto.sh" "$T/impl-hook.sh" > "$T/proto-impl.diff"; python3 -I "$T/classify_w8.py" "$T/proto.sh" "$T/impl-hook.sh" "$T/proto-impl.diff" "$P"; echo '```'
cat <<'TXT'

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
TXT
python3 -I "$T/compare.py" "$E/v31/impl/W9-suite.txt" "$T/old-W9.txt" "$E/v31/impl/W11-adversarial.txt" "$T/old-W11.txt" "$T/w11-table.tsv"
echo "--- W9 实现节与 95cf1de7 原型节不同的条目 (逐条):"; python3 -I "$T/w9diff.py" "$E/v31/impl/W9-suite.txt" "$T/old-W9.txt"
echo "--- 原始输出 (wd-run/suite-impl.out) 里 SC-21ab 的子用例与红的条数:"; grep 'FAIL \[W10 SC-21ab' "$T/wd-run/suite-impl.out" | grep -o '{refused \[[^]]*\]' | sed 's/^{refused \[\(.\{0,14\}\).*/  子用例前缀 \1…/' | sort | uniq -c
echo '```'
cat <<'TXT'

W9 逐条对照:
- 基线节: 新一轮与 95cf1de7 完全相同 (813/814, 唯一红为 SC-13)。
- 实现节相对基线节的变化: 恰为 21ab、21ac、21ag、21aj、21al、21ao 六组 (6 条只在实现节出现, 0 条只在基线节出现); 原型那一轮同样是这六组。
- SC-13: 新旧两轮的基线节与实现节都是同一条红 (内容逐字相同), 不算变化。
- 变化断言与原型那一轮逐条相同: 21ac、21ag、21aj、21al、21ao 五条相同; **21ab 不同**: 原型那一轮 3 条红 (子用例 1, 读配置文件那条: 放宽后整份判出 finding 文案而不是尺寸文案), 实现这一轮 6 条红, 多出的 3 条来自子用例 2 `f=x; echo $f yyy…`: 退出码 want '2' got '0'、尺寸文案 got ''、分段提示 got 'no' —— 即实现放行了这条 8193 字符的无害副本, 原型那一轮它按基线拦下。计数行相同 (807/814) 是因为两轮都是这一组整组红。

W11 逐形状 (分节 / 形状 / 原型那一轮 / 这一轮; 墙钟只列不比):
```
TXT
cat "$T/w11-table.tsv"; echo '```'
cat <<'TXT'

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
TXT
echo; echo "git status (主仓, 生成本报告时):"; echo '```'; git -C /home/dev/Aria status --short; echo '```'
} > "$RPT"
