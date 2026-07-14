# post_spec R7 聚合报告 — state-scanner-stale-refs-false-parity (v7 @ ed21aba)

> **Verdict: FAIL 3/3** (backend 4C/8M/4m + qa 2C/6M/3m + 复发狩猎 2C/6M/3m; 窄范围: F10″ §13/AC + D15-D17 + R6 Majors 折入核验)
> 2026-07-14 | 审计 agent 全部 code-grounded (multi_remote.py/coordination_fetch.py/track_board.py/scan.py 实读 + 真仓 git 实验) | 只审不改, 本报告 = 三方原文的去重聚合

## 一句话

v7 的 parity 轴 fail-CLOSED 工事扎实 (三方一致确认无新正向枚举口子), 但 **D15 代裁在三个方向被击穿** (🔍 预警成立) 且 **F10″ 的定义域完整性声明被真 git 实验证伪** — 第十次复发的宿主按谱系规律又换了位置: **新原语的喂数视图** (no-prune fetch) 与**新窗口的参数耦合** (k/rotation 脱钩)。

## 去重后 Critical (8)

| # | 来源 | 内容 | v8 修法锚 |
|---|------|------|----------|
| RC-1 | 狩猎 C-1 | **Fetch 1 无 `--prune` ⇒ ref 删除类漂移结构性不可见** — force-push/删支后本地化石 ref 仍 contains G ⇒ orphan 假绿, 全部 v7 护栏绿灯通过。第十次复发最强候选 (陈旧证据, 宿主=fetch refspec/prune 语义) | F3′ Fetch 1 加 `--prune` + 横扫表前提列 + AC-16 加删支 fixture; 论证 prune 对 #141 无害并写死 |
| RC-2 | backend C-1 | **D15 只落 2 位点, `可信(r)` split-brain** — F1′/F4′ 公式块/tasks 3.5/4.2/AC-15/OQ-D 共 ≥7 处仍是 wall-clock 300s 定义 (「定义两次且互斥」= 第九次复发同形) | D15 全量落位; 配置键命名 (`freshness_generations`/`freshness_hard_cap_days`); `freshness_window` 退役路径; 5.1d 闸加「同一谓词单一定义」断言 |
| RC-3 | backend C-2 + 狩猎 C-2 (独立同算) | **k=3 与 rotation 脱钩** — 用 spec 自己实测数字: 60 腿 2 host ⇒ 8 腿/scan ⇒ rotation=4 > k=3 零边距, 抖动即滚动恒红; 3.16 的 AC-15 fixture 预算参数是反推值 (mock 出真实拓扑不存在的预算 = fixture-shape-drift 假绿) | 写死耦合 `k ≥ rotation−1` (自适应推导, 固定 3 仅下限); fixture 预算取 §承重实测数字; 补 rotation>k 边界 fixture |
| RC-4 | backend C-3 | **hard_cap 7d 把有界陈旧容忍放宽 2000×** — 创始事故 (14h 陈旧 equal 供 ∃ 证据) 在窗内复活; OQ-D 「≤5min」承诺字面已假 | **双角色窗拆分** (三 C 合并解): ∃ 正证据资格 = 短墙钟窗 (≤max(scan 起点,1h)); ¬blocking 豁免 = 代际窗 (D15 原案)。与 AC-15(b)「origin 不能替 github 作证」同构 |
| RC-5 | backend C-4 + qa M-1 (同一格两向) | **contains rc=129 分支缺失** — G 不在 S odb (更严重的破损: gitlink 无处存在) 落 fail-soft ⇒ soft-error 放行, 严重度倒挂; 且 rev-parse 对普通目录 rc=0 返 tree sha, 「G 解析失败」分支按 rc 探不到 | 13.2 增第 6 分支 (可信 ∧ rc=129 no-such-commit ⇒ orphaned 候选); G 取得改 `ls-tree` 断言 mode=160000 (或 cat-file -t 前置); AC-16 加对应 fixture |
| RC-6 | qa C-2 | **13.2 五分支零测试落点** — 尤其 ¬可信→unverified 假阳守卫不可证伪: 忽略 可信(S,R) 的实现能过全部现列红测试 (「只测一半定义域」在测试集设计层预埋) | 13.2 各分支配红测试成对 (至少 unverified 守卫 + shallow 不阻断), 纳入 2.13 全-RED 闸 |
| RC-7 | qa C-1 | **Spec C 重定义 check 的求值基底未裁** — Phase 1.11 时本次 issue_status 不存在: 读上一份 snapshot ⇒ lag-1, AC-2 单跑不可证伪 (修后转不绿, 撞 2.14 设计闸); 读本次 ⇒ 「不挪位置」承诺破产 | Spec C v4 裁 (a)/(b); (a) 则 AC-2 改两跑断言 + lag-1 公示 |
| RC-8 | 狩猎 M-1 (升格候审) | **¬可信子模块腿双通道全静默** — 子模块 parity 恒 detached_head (benign), gitlink 是唯一 blocking 通道, ¬可信弃判 ⇒ deploy key 吊销/退避腿的真 orphan 永不阻断; 与第八次复发 (没去问⇒放行) 结构同构, advisory 可见通道有被吞史 | orphan_unverified 持续 ≥k 代升级 blocking (「过期即诚实」同构); 或显式声明有意接受 + 输出必渲染进 AC |

## 去重后 Major (12)

- **RM-1** (backend M-2 + 狩猎 M-2a): orphan 谓词缺 `可信(主仓 R leg)` — C 陈旧 ⇒ 新 orphan 假绿; 修: 谓词加合取, ¬可信 ⇒ orphan_unverified
- **RM-2** (狩猎 M-2b): 跨腿代差假红 — C 新 S 旧(窗内可信) ⇒ 健康 ship 报 orphaned; 修: 前置 `gen(S,R) ≥ gen(主仓,R)`, 不满足 ⇒ unverified + AC-17 fixture
- **RM-3** (backend M-3 + qa M-2): remote 名配对假设未声明 + `S 无 R remote` 分支缺失 (与真 orphan 原语层同像, 实测 exp5) + .gitmodules 绝对 URL 下断裂叙事字面不成立; 修: 第 7 分支 no_matching_remote + 叙事修正 + F5′ 显式配置与 per-repo remote 集合的交集语义
- **RM-4** (backend M-4): 3.14 shim 没对准真消费字段 — track_board 红条读 `degraded` 非 `success`; degraded/cached 派生规则未定义; 修: 映射表扩 3×{success,degraded,cached} + 行为变更公示或保留派生 `degraded := fetch_ok==false ∧ served_stale_cache`
- **RM-5** (backend M-5): `scan_generation` 递增语义未定义 — TTL 命中若 +1, 快速连跑 k+1 次恒红; 修: 仅 TTL-miss 真跑 fetch 轮次时 +1, 配 lock 测试
- **RM-6** (backend M-6): 并发 scan cache lost-update ⇒ 计数器回退 ⇒ 负代龄恒 ≤k (fail-OPEN 微缝); 修: 钳位 `gen_fetched > scan_gen ⇒ 视同 null` + 计数器单调不回退 + 3.13 降级声明扩 cache 层
- **RM-7** (backend M-7): AC-15(c) 全称量词与 3.5d 退避 (最长 2^8 scan 不刷) 字面互斥; 修: carve-out 非退避腿
- **RM-8** (backend M-8): 可信/generation cache 键形状未写死 — 按 remote 名单键 ⇒ 主仓/子模块同名腿碰撞 (形态 #3 经 cache 键复活); 修: 写死键=(repo 相对路径, remote 名) + AC-6 碰撞 fixture
- **RM-9** (狩猎 M-3): `generation_fetched` 缺「只在 Fetch 1 真成功时推进」镜像约束 (3.7 只约束 fetched_at) — 写入侧污染架空代际窗; 修: 逐字镜像 3.7 + lock 测试
- **RM-10** (狩猎 M-4): 13.4 五个新 reason 未在 F4′ 裁决表落格 — 按补集规则全 blocking, 与 13.2 「不判」字面矛盾; 修: 独立 `gitlink_integrity` 结构 (不进 parity.reason, 与 AC-16 一致) + F4′ 补 gitlink 层裁决节逐格填
- **RM-11** (狩猎 M-5): 「可达」= branch-可达 only (`--no-tags` + `R/*`) — tag-only pin 恒红假警报, AC-17(d) fixture 测不出; 修: 显式声明收窄 + 后果 + 逃生口 + tag-only fixture 钉死行为
- **RM-12** (狩猎 M-6 + qa M-4/M-5): 12.10 offline 主手段的覆盖损失未声明 + 9.7 一行定义不足承重 (mtime/时钟通道 offline 冻结不了) + 通道 #5 是被静音的真产品缺陷 + Spec C AC-4 新验收面被通道 #6 打破 (需收窄到单 check 或补 output 确定性任务); 修: 9.7 扩成完整段 (offline 冻结面枚举: 网络+缓存态+时钟源) + 覆盖损失声明 + 通道 #5 真序修复或显式接受 + Spec C AC-4 收窄

## Minor (10, 原文见三方报告)

backend m-1..4 (3.2 清单补 2 命中 / 3.15 限定主仓 origin / 主仓 detached HEAD 分支 / feature 分支盲窗公示) + 狩猎 m-1..3 (锚定集扩 {current_branch}∪默认分支 / F1′ ahead 理据改写 / shallow 定性改「代价裁量」) + qa m-1..3 (2.15 双断言措辞 / AC-17(c) 拆两 checkbox / Spec C 3.3 跑次标注)。

## 无发现清单 (三方交叉确认的可信面)

AC-16 主 fixture 可构造可 RED/GREEN (qa 给出零网络搭建步骤) / AC-16 与 AC-8 字面互斥已解除 (狩猎构造反例失败) / contains 正常路径零分支名假设成立 / cache 删除后冷启动 fail-CLOSED / 退避腿 generation 语义自洽 / 12.10 与 Spec C v3 tasks 侧一致 / 谓词横扫表登记完备 (成员层)。

## 本轮已顺手落地 (同 commit)

- proposal Verification 段 stale v6 文本 (qa M-3, 本 v7 commit 自引入的矛盾) → 已同步 CE 结案版
- proposal Status 行 → R7 FAIL + v8 待办核心清单

## R8 建议范围

v8 按上表折入后, R8 窄范围: RC-1..8 的修复文本 + RM-1..12 抽查 + D15′ (双角色窗) 作为新核心谓词重点对抗 (它是第 11 次复发候选位)。
