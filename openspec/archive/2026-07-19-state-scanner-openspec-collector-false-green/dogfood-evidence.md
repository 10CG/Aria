# Dogfood evidence (SC-11) — state-scanner-openspec-collector-false-green (#166)

真实执行记录, ship 时一次性观测。归档后作为 T4.1 声称的可链接产物 (#95 C-gate:
dogfood 声称须有产物, 否则 fail-toward-warn)。

## 缺陷 1 — layout drift 端到端 (scan.py exit=10 + 正交扫 archive)

构造:

```bash
rm -rf /tmp/dogfood166 && mkdir -p /tmp/dogfood166/openspec/archive/2026-01-01-foo
cd /tmp/dogfood166 && git init -q
printf -- '---\nstatus: Complete\n---\n# foo\n' > openspec/archive/2026-01-01-foo/proposal.md
printf -- '> **Status**: Draft\n' > openspec/my-change-proposal.md   # 裸 proposal, changes/ 不存在
python3 <aria>/skills/state-scanner/scripts/scan.py --output snap.json
```

实测输出:

```
scan.py exit code: 10          # 期望 10 (软错误, snapshot 仍可用)
configured:   False            # 保 `changes/ exists` 语义 (SC-4)
archive.total: 1               # 正交扫描生效 — 修复前恒为 0 (SC-1)
errors kinds: ['git_log_failed', 'layout_drift', 'coordination_fetch_failed']
layout_drift detail: openspec/ exists but openspec/changes/ is missing
                     (misplaced: my-change-proposal.md) — active changes ...
```

(`git_log_failed` / `coordination_fetch_failed` 系空 git repo 无提交无远程的预期噪声,
与本 change 无关。)

**判定**: SC-1 / SC-3 / SC-4 / SC-11 端到端成立 — 修复前该场景 `errors=[]` +
`archive.total=0` + exit 0, 与「没用 OpenSpec」输出完全等价。

## 缺陷 2 — gate_result yaml-only baseline 反转

`test_gate_yaml_only_source.py` 的 baseline 由 code-reviewer 独立 stash 源码复核:
修复前 yaml-only spec 得 `{'complete': True, 'verdict': 'pass', 'warnings': [],
'd_payload': None}` (静默放行), 修复后 `verdict=warn` + 1 条
`archive-safety-net-source-unsupported` unverified_claim + 非 None d_payload。

## 缺陷 3 — _has_token 词边界实测

```
_has_token('completed',  'completed') = True
_has_token('uncompleted','completed') = False    # 不重开 #101
_has_token('incomplete', 'completed') = False
_normalize_status: Completed / COMPLETED / 'Status: Completed' → done (修复前 unknown)
```

## 测试总量

rebase 到主 spec Phase 1-3 基线 (`e162f7b`, v1.60.0) 后, 全量套件 **1232 tests 绿**
(本 change 新增 13; 基线自身 1219)。rebase 前为 1072。
