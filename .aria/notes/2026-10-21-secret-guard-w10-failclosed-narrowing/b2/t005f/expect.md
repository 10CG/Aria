# t005f 各轮预期（开跑前写，2026-10-25；判据与理由）
1. 移植用例 SG_W10_ONLY=.，5 个 bash：5.0.18 / 5.1.16 / 5.2.15 / 5.3.20 放宽平台，FAIL 0、SKIP 0（非 root，V5-S10 照跑），新增 8 个编号全 PASS；3.2.57 FAIL 0，SKIP 只有 [platform]（含 V15-T1/T2/T3/W1e），V15-W1a-d PASS（纯 bash 函数，3.2 可跑）。每轮计时批 judged（首尾一分钟负载 < 2，否则低负载重跑一次）。
2. 整轮 PATH bash：FAIL 0，总数 974（本机无 zsh；改前 966 + 8），SC-13 PASS，计时批 judged。
3. 整轮 WSL_DISTRO_NAME=Ubuntu：FAIL 0；helper 走 norelax，放宽类直调用例（含 4 个新 relax 编号）SKIP [platform]，V15-W1a-d PASS；6 组的分支说明行为 baseline branch。
4. sc-cases.sh（BASE = 59e333c 的 hook）：FAIL / MISSING / SETUP 0，V0-H2 PASS（新 8 个编号各报一次）。
5. run-mutants v31 模式：57 个 BI 全 CAUGHT，6 个扰动 CAUGHT，P-0 GREEN（负载致 NOT-JUDGED 时低负载重跑）。理由：mutants.py 在新 hook 上生成的 64 个文件与在 2893bcc 上生成的改动行逐个相同，锚点无一变化。
6. 套件模式 MUT_SUITE：同 5；BI-8 的原因为 [reference]（同 3d 记录）。
7. w14.sh：31 个全抓住（as predicted 26 + by the added case 5，同 W14 原记录），not judged 0。理由同 5（w14-mutants.py 只改了 IMPL_SHA12，31 个坏实现改动行逐个相同）。
