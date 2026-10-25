# 5f3 复核：预期（实测之前写下）

## 一、坏实现在函数层（主控 12 种情形探针 cases3.sh / run3.sh，uid 1000，PATH bash 5.2.15）的预期

基准（expected-v34 的函数）：host 0, autofs+WSLInterop 0, binfmt+late 1, binfmt+none 0, autofs-on-top 0, empty 1, unreadable 1, dir-as-table 1, noglob+late 1, failglob+none 0, nosearch 1, listless+late 1。

- MW-while-read：12 种全与基准相同（只坏在开销，函数层看不出）。
- MG-glob：noglob+late 0（不符）；failglob+none 报错中止（其后两条跑不到）；其余同基准。
- MF-first-line：autofs-on-top 1（不符）；其余同基准。
- MX-no-search-check：nosearch 0（不符）；其余同基准。
- MO / MS / MI：只动准入门，函数层 12 种全同基准。
- ME-empty-as-none：empty 0、dir-as-table 0（不符）；unreadable 仍 1（awk 失败走 `|| return 1`）；其余同基准。
- MN-one-name：binfmt+late 0、noglob+late 0、listless+late 0（不符）；其余同基准。

## 二、坏实现在套件 V15 用例上（run-suite.sh，SG_W10_ONLY 取 V15，PATH bash）的预期 —— 用例编号待 5f3 报告到后按语义对上，再实跑

- MW：只有开销用例红（叠 1000 tmpfs，0.5 s 界）；没有 unshare -rm 时 SKIP，那就记为「本机抓不住」。
- MG：noglob、failglob（报错或 stderr 非空）、可查不可列三条红。
- MF：叠 autofs 那条红。
- MX：目录不可查那条红。
- MO：顺序那条红（平台失败 / 没有时间时被调用了）；W1e 两面仍绿。
- ME：空表、目录当表两条红。
- MS：W1e「桩返回 1 时准入门须为 1」那一面红；其余绿。
- MI：W1e 两面都红；另外端到端里依赖放宽开门的用例大面积红（本机 nowslfs 返回 0，取反后门恒关）。
- MN：binfmt+late、noglob+late、可查不可列+late 三条红。
- 负控：5f3 的 hook 本身，V15 全绿。

## 三、静态

- `git diff 710a36d <5f3> -- hooks/secret-guard.sh` 与 `diff expected-v34.sh <5f3 hook>`：后者只差 hook 头注释里补 D-3 例外的那一处（纯注释）；前者 = 准入门删一行加一行、函数整段替换、头注释一处。
- 新函数在 source 闸门之上；hook 别处一字不动。

## 二补：按 5f3 的编号写定（5f3 报告到后、套件实跑之前写下）

编号：W1a autofs 不看项 0、W1b binfmt+late 1、W1c binfmt 无项 0、W1d 读不出 1、W1e 两面（[open] = 桩 0 时门没开；[closed] = 桩 1 时门没关）、W1f 空表 1、W1g 叠 autofs 0、W1h 目录当表 1、W1i noglob+late 1、W1j failglob 无项 0、W1k 不可查 1、W1l 可查不可列+late 1、W1m 顺序（[platform] [time] [control]）、W1n 开销（MODE relax）。跑法：run-suite.sh，SG_W10_ONLY='^V15-'，PATH bash 5.2.15，uid 1000。

- 负控（5f3 的 hook）：V15 全 PASS。
- MW：只有 W1n 红（墙钟超 0.5 s；首尾负载 < 2 时记 FAIL，否则可能 SKIP [load]——那就低负载重跑）。
- MG：W1i、W1j、W1l 红；其余绿。
- MF：只有 W1g 红。
- MX：只有 W1k 红。
- MO：只有 W1m 红（[platform] [time]）。
- ME：只有 W1f 红；W1h 仍绿（本机 mawk 读目录自己报错退出，走 `|| return 1`）。
- MS：只有 W1e 红（[closed]）。
- MI：W1e 红（[open] [closed] 两面）；T1-T3 是否受影响不作预测。
- MN：W1b、W1i、W1l 红；其余绿。
