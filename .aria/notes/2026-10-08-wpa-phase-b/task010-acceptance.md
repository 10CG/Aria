# WP-A TASK-010 验收记录 (发版前)

> 主控独立复跑 (不信执笔回执)。2026-10-15。基线 aria `268da8f` (= v1.74.1); 目标 aria `bae5c10` (hook 码 = 83d8f30 冻结态) / standards `191560e` / 主仓 `06c08db`。
> 环境: 非 root `dev` (uid 1000; SC-20 20g 可构造) · `WPA_BASH32=/home/dev/.aria/tools/bash-3.2.57/bash` (3.2.57) · `sha256sum`+`shasum` 双哈希 (12o) · `en_US.utf8` (32d) · 共享主机 4 核, 负载波动 1.3–12。

## 1. 验收探针 `baseline_probe.py` (WPA_BASH32 + WPA_REQUIRE_ALL=1)

- 命令: `WPA_BASH32=<bash3.2> HOME=<priv> TMPDIR=<priv> python3 openspec/changes/secret-net-l3-and-bypass-paths/baseline_probe.py <主仓>/aria`
- **PROBE_EXIT=0**; `target shape ... : holds`。
- 分类计数全绿: baseline-failing 226/226 · doc-sync 26/26 · reverse-guard 82/82 · allow-guard 70/70 (含 SC-33 归因清单复核) · known-limit 40/40 · zero-regression 9/9。
- `rows not run (n/a): by design 1 (30a)` (git-history 腿, 另跑见 §2); `leg missing or not constructible 0`。
- 验收点名的 n/a 禁区全部 `yes` (ran): 32c / 32d / 32e / 29h / 29i / 12o / 20g。
- 过程: 首轮 (doc-sync 前) PROBE_EXIT=4, 唯三红行 = SC-26 26g + SC-27 27a/27c (doc-sync), 功能/bash3.2/归因行全绿 ⇒ 无功能回归; doc-sync 后复跑 = 上述全绿。

## 2. SC-30 (真 git checkout, 测试内 SC-9a + SC-8 五档延迟闸)

- `bash aria/hooks/tests/secret-guard.test.sh` 于真 checkout (带 .git), **load@start=1.37 (<2, 空闲窗口)**: **PASS 816 / 816, FAIL 0** (zsh 缺席 ⇒ 6 条 zsh 用例跳过, 816 = 无 zsh 全量)。SC-9a 与 SC-8 五档含在内, 零失败。
- `bash aria/hooks/tests/secret-scan.test.sh`: **PASS 129 / 129, FAIL 0**。

## 3. W14 时档 `timing.py --judge` (基线 268da8f vs 目标; 交错 A/B, 每侧 min/5, 判 CPU 比值)

- 命令: `python3 writer-v6-proto/timing.py <268da8f hooks> aria/hooks f,f0,fhit,g,gmax,gc,h,i,i3 --judge`
- **TIMING_RC=0 — judge: 20 bounded tiers, 0 failed** (全部有界档 PASS)。
- 关键档 (比值 = 目标/基线, W14 上界):
  - f 1.72 / 1.55 (≤3.0) · f0 1.19 / 1.12 (≤1.5×max(base,100ms)) · fh-a/b 1.99 / 1.99 (≤3.0, 活性 `_sg_core_eval`×2)
  - g-a 1.07 · g-b 1.13 · **g-c 1.04** (≤2.5; M6-rework 验证: 无长度预算的实现在此稠密档 3.7–5.0 FAIL, 1.04 = 预算拒绝超限副本, fail-closed 正确) · h2 1.23 (≤1.5)
  - i1 1.23 · i2 1.15 (≤2.0) · i3-a..e 1.14–1.74 (≤2.5) · i3-f/g/h 3.23 / 3.04 / 3.41 (≤5.0, 300KB 不带引号 kv)
  - 实测比值与 proposal §W14 原型量级吻合 (f 原型 1.60/1.55; i3-f 原型 3.21; 等)。
- **负载透明 (Rule #10, 不充数)**: timing `load@start=3.39` (非字面 <2); 结果仍有效 —— W14 §241 明文判据为**负载稳健的 CPU 比值 min-over-N** (墙钟与 loadavg 只记录不判), 过载兜底 (基线 CPU ≥5s) **未触发** (最大基线 CPU 1.79s), 且比值与原型吻合。真正负载敏感的腿 (SC-8 五档, §2) 已在 load 1.37 (<2) 跑过。如需严格 <2 复跑 timing, 另开窗口即可, 不改判。

## 4. 结论

TASK-010 全部验收腿 PASS: 探针 exit 0/holds · SC-30 816/816 + scan 129/129 · W14 时档 20/20 有界档 · SC-33 归因 (探针内) · doc-sync 已落地 SYNCED。5 条 review minor 仍延后。下一步 TASK-011 发版 (取号 + 同步面) **需 owner 授权**。
