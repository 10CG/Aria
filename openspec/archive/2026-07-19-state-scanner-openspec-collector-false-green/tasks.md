# Tasks: state-scanner-openspec-collector-false-green (#166)

> Level 2 — 任务 1:1 派生自已 audited 的 11 条 SC。TDD: 每缺陷先 RED (baseline-failing) → GREEN → doc-sync。

## 缺陷 1 — collectors/openspec.py (layout_drift + 正交扫 archive)
- [x] T1.1 RED: `test_openspec_layout_drift.py` — SC-1 / SC-2 冷启动负控 / SC-3 两形状 / SC-4 configured=False (RED 实证: 3 失败 + 负控绿)
- [x] T1.2 GREEN: 移 early-return; changes-loop 改 `for d in ... if changes_dir.is_dir() else []` (防 FileNotFoundError, 零 re-indent); drift 裁决移到 archive 扫描后复用 `archive_items` (消除重复探测); 高置信 layout_drift; configured → `changes_dir.is_dir()`
- [x] T1.3 doc: state-snapshot-schema.md 加 layout_drift kind + configured=False∧archive>0 组合语义 + openspec_scan_failed

## 缺陷 2 — lib/spec_complete.py (gate_result yaml-only 可见)
- [x] T2.1 RED: `test_gate_yaml_only_source.py` — SC-5 (RED: verdict pass≠warn) / SC-6 双源负控
- [x] T2.2 GREEN: `gate_result:1298` yaml-only 分支追 unverified_claims (含 symbols:[]) + verdict=warn + `_build_d_payload` 非 None
- [x] T2.3 verify: openspec-archive Step7 D-tracker (`d_payload!=null`) + Step2 warn_overlay (`verdict==warn`) 经既有路径点亮, 零改 openspec-archive (code-reviewer 消费侧核实)

## 缺陷 3 — collectors/_status.py (completed token)
- [x] T3.1 RED: `test_status_completed_token.py` — SC-7 (RED: unknown≠done) / SC-8 #101 护栏 / SC-9 design_deferred→pending_archive 迁移
- [x] T3.2 GREEN: `_status.py` done 家族加 `completed`
- [x] T3.3 doc: status-field-guide.md done token 表 + #166 note

## 收尾
- [x] T4.1 SC-10/SC-11: 全量 **1232 tests 绿** (rebase 到主 spec Phase 1-3 基线 `e162f7b` 后; rebase 前 1072, 当时唯一 failure = 既有 time-bucket flaky `remote_refs_age` 属 sync collector 与本 diff 零交集, 已被对方 `3ceb177` 根治) + dogfood 合成 fixture → scan.py **exit=10** / configured=False / archive.total=1 / layout_drift detail 点名 stray。**产物**: `openspec/changes/state-scanner-openspec-collector-false-green/dogfood-evidence.md` (真实执行记录落盘)
- [x] T4.2 output-formats.md 补 layout_drift worked-example (区别于「未配置」模板)
- [x] T4.3 code-review **PASS** (0 Critical/0 Important, 4 Minor) + silent-failure-hunter 抓 **1 MEDIUM fix-introduced regression** (`except OSError: pass` 静默吞咽 = 本 change 立意要杀的同款反模式) → 已修: helper 收 `r` 参数发 `openspec_scan_failed` + archive iterdir 对称 fail-soft + 补 2 个 OSError 测试
