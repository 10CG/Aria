# 10CG/Aria#199 A.2/A.3 工具 — 跨容器接手用

> **为什么在仓里**: 这些文件原本只在容器 `simonfish/023236f2` 的会话 scratch (`/tmp/...`) 里, 双子星 (`bfe8285d`) 看不到。计划的 yaml 约定「只经生成器产出、不手改」, post_planning 各轮的席位提示词也要跨轮保持一致, 所以随 2026-09-17 会话收尾一并入仓。
> **对应**: `openspec/changes/pre-merge-completeness-gate-change-scope/{tasks.md,detailed-tasks.yaml}` v2 (主仓 `caa40c8` 起) · 交接 `docs/handoff/2026-09-17-199-a2-a3-v2-r1-paused-handover-to-twin.md`

## 文件

| 文件 | 用途 |
|---|---|
| `gen_yaml.py` | `detailed-tasks.yaml` 的生成器 (v2)。**改 yaml 一律改这个脚本再重新生成**, 不手改产物 |
| `audit-seat-prompt-template.md` | post_planning 席位提示词的公共模板 (占位符 `{ROUND}` `{ROLE}` `{VERSION}` `{SHA}` `{FOCUS}` `{ROUND_CONTEXT}` `{REPORT_PATH}`) |
| `r1-seat-prompts/*.md` | R1 实际下发的五份完整提示词; 各席的「你的视角」段 (`{FOCUS}`) 从这里取 |

三态实跑脚本 **不在本目录**: 它们的全文已嵌在 yaml 的 `metadata.a2_state_runs.script` 与 `metadata.v2_state_runs.script`, 输出在同节 `output`。

## 重新生成 yaml (须逐字节一致才算工具可用)

在主仓根执行 (生成器从 cwd 读 `openspec/changes/<id>/tasks.md`):

```bash
W=<你的 scratch 目录>; mkdir -p "$W"
python3 - "$W" <<'EOF'
import sys, yaml
w = sys.argv[1]
m = yaml.safe_load(open('openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml'))['metadata']
for k, n in [('a2_state_runs', 'a2'), ('v2_state_runs', 'v2')]:
    open(f'{w}/{n}_script.py', 'w', encoding='utf-8').write(m[k]['script'])
    open(f'{w}/{n}_output.txt', 'w', encoding='utf-8').write(m[k]['output'])
EOF
python3 .aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py "$W/out.yaml" \
  "$W/a2_script.py" "$W/a2_output.txt" "$W/v2_script.py" "$W/v2_output.txt"
cmp "$W/out.yaml" openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml && echo REGEN_IDENTICAL
```

2026-09-17 在 `023236f2` 上实跑: `REGEN_IDENTICAL`。

## 重跑三态证据

两份脚本都要一个**一次性**主仓副本 (改完会自行复原, 但不要拿真仓跑):

- 副本 = 主仓 `a563192` 的 checkout + aria `1cb3872` 以嵌套 clone 放在 `aria/` 并 `git submodule init aria` (使 `git grep --recurse-submodules` 看得见), 工作树干净。
- 命令见 yaml 各自的 `command` 字段; 输出须与 `output` 字段逐字节一致, 不一致就是证据坏了, 先查再改计划。
- tasks.md 改动后必须重跑 (两份脚本都以 tasks.md 为输入), 再用生成器重新生成 yaml。

## 用模板下发下一轮席位

- 占位符逐个替换; `{ROUND_CONTEXT}` 写上一轮聚合报告路径与本轮入口竞品探针结论。
- 模板里有两类**容器相关**内容要按接手方改: scratch 路径 (`/tmp/claude-1000/...`) 与「可 `cp -a` 执笔人副本」那句 (副本需按上节重建); 「背景事实」段的主仓 SHA、版本号、执笔人自报薄弱点也要换成当轮值。
- 严重度口径、证据要求、硬性纪律 (只写自己的报告 / 不做 git 写操作 / 禁止派子代理)、报告 frontmatter 模板保持不变, 保证跨轮可比。
- 并发: 默认 2 席滑动窗口; 每席完成后跑不带路径的 `git status --porcelain`, 确认只多了它自己的报告。
