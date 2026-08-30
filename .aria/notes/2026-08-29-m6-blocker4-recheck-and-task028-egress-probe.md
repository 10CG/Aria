# M6 实测: Blocker 4 复核 + TASK-028 egress/auth 实跑证据 (2026-08-29)

> **执行**: 主 loop 亲验 (无 agent), 容器 `bfe8285d`, claim `aria-2-0-m6-dispatch-input-delivery` (Phase B, advisory, passed)
> **触发**: owner 选 [1]+[2] —— 先复核 Luxeno 延迟, 再并行起 TASK-021 / TASK-028
> **一句话**: 两道门实测都是硬阻断, 且都不在 input-delivery 代码侧:
> (A) Luxeno 上 GLM 生成速率仅 ~20 tok/s ⇒ 生产口径单次调用 54-84s, **越过 `LUXENO_TIMEOUT_SEC=60`**
> (比 2026-07-02 的 44-54s 更差), 另有长请求 TLS EOF 2/5 —— 已反馈 SilkNode #1058;
> (B) Layer 2 容器用的 `FORGEJO_BOT_PAT` 已失效 (401 user does not exist)。

---

## 1. Blocker 4 复核 —— 结论: 延迟依旧, 而且比 2026-07-02 更差

> ⚠️ **本节含一次自我更正**: 首轮 (17:00-17:15) 我测到 `glm-4.5-air` 连续 503、
> 其余 GLM 型号 403, 曾据此判定「Blocker 4 变形为策略层不可用」。**该判定错误** ——
> 那 503 是字面意义的临时故障, 约 17:49 自愈。owner 要求先钉死 key 有效性后复测,
> 才得到下面的真实图景。教训: 单一时间窗的连续失败不足以判「策略层」, 必须先做
> 真/假凭据对照把认证层排除掉。

### 1.1 口径

复用生产同一条 HTTP 路径 (`silknode_client.py` 的 header/payload 形状: `Authorization: Bearer`,
UA `aria-orchestrator/1.0 (+luxeno-client)`, `POST {base}/chat/completions`), key 取自
`nomad/jobs/aria-orchestrator.LUXENO_API_KEY` (Rule #7: `capture_output=True`, 全程不 print)。
低频 (间隔 15-20s) 避免自造限流。

### 1.2 key 有效性判别 (真/假 key 对照)

| 用例 | 结果 |
|---|---|
| 真 key + `glm-4.5-air` | **200** |
| 假 key + `glm-4.5-air` | **401** `authentication_error` / Invalid API key |
| 真 key + `gpt-4o-mini` | 400 not available via the OpenAI Chat Completions API |
| 假 key + `gpt-4o-mini` | 401 Invalid API key |

真假 key 响应判然不同 ⇒ **key 有效, 认证层无问题**。

### 1.3 延迟实测 (生产口径)

| 口径 | 输入 tok | 输出 tok | 耗时 |
|---|---|---|---|
| triage prompt, max_tokens=2000 | 238 | 1126 | **73.4s** |
| 同上 | 238 | 1417 | **84.2s** |
| 同上 | 238 | 1244 | **54.6s** |
| 短 prompt, max_tokens=200 | 10 | 112 | 9.3s |
| 短 prompt | 10 | 73 | 5.3s |
| 短 prompt | 10 | 200 | 9.7s |

**关键分解: 耗时几乎完全由输出 token 数决定, 生成速率恒定 17-21 tokens/s**, 与输入长度、
固定开销无关。这比 2026-07-02 的「44567ms / 53944ms」**更慢**。

另: 同批 5 次长请求里 **2 次在约 5.0s 时 TLS EOF** (`TLS/SSL connection has been closed (EOF)`),
短请求 3/3 无此现象。

### 1.4 附带观察 — 名义模型 ≠ 实际模型

请求 `glm-4.5-air` → 200, 但响应 `model` 字段回的是 **`glm-4.7`** (5/5); 而直接点名
`glm-4.7` / `glm-5.2` / `glm-4.6` / `glm-4.5` 一律 **403** "no provider with a confirmed
no-training policy"。同一承接模型换个名字进得去 —— 若非刻意降级, 则 opt-out 判定可能没覆盖
路由后的实际模型。(opt-out 可用模型清单本身是 SilkNode #1019 已在跟的题, 不重复报。)

### 1.5 判定 + 已反馈

**Blocker 4 依然成立, 且已越过我们自己的止血线**: `LUXENO_TIMEOUT_SEC=60` 当初为扛 44-54s
才从 30s 提上来, 现在 73s / 84s 两次都会直接 timeout → 重试链耗尽 → dispatch 失败。
**168h 跑在此解除前仍不能启动。**

已按 owner 指示第一时间反馈上游: **SilkNode #1058**
(https://forgejo.10cg.pub/10CG/SilkNode/issues/1058) — 含速率表、TLS EOF、名义/实际模型
不一致、503 窗口实例、真假 key 对照。三个待答问题: 20 tok/s 是否正常 / TLS EOF 成因 /
路由替换是否预期。

## 2. TASK-028 —— egress 腿 PASS / auth 腿 FAIL (真实 heavy-node 实跑)

### 2.1 怎么跑的

仓里 `docs/m6-dispatch-input-delivery-task028-egress-probe.md §2.1` 已有现成 HCL, 但它
**从未被执行过**, 实跑当场暴露它三处会直接让 task 起不来/必错的缺陷:

| 缺陷 | 后果 | 修法 |
|---|---|---|
| `curl -w '<百分号>{http_code}'` | Nomad client 会把 task config 再过一遍 consul-template, `%{` 被当模板控制字 → `Failed Validation: Invalid template control keyword: "http_code"`, task 根本不启动 | 改用 `-D <hdrfile>` 存响应头后 `head -1 | cut -d' ' -f2` 解析 |
| 用 `jq` 提 `.number` | `curlimages/curl` 镜像里**没有 jq** | 改 `grep -q '"number"'` (布尔, 不打印正文) |
| 只探外网 `https://forgejo.10cg.pub` | 容器里该域名 TLS 握手直接失败 (`curl (60) self-signed certificate`), 而**生产 fetch 走的是内网 URL** (`initial.sh:46` `ARIA_FORGEJO_INTERNAL_URL` 默认 `http://192.168.69.200:3000`) —— 原设计探的不是生产路径 | 内网为主, 外网留作对照 |

> 这条正是 memory `feedback_sot_example_commands_are_never_executed` 的又一实例:
> 规范/文档里的示例命令大概率从未实跑, 「设计写好了」≠「能跑」。

### 2.2 结果 (heavy 节点容器内, node class = heavy_workload)

**无 auth 腿 (探网络可达性)**:

| 目标 | http | content-type | 判读 |
|---|---|---|---|
| 内网 `/api/v1/version` | 403 | `application/json;charset=utf-8` | **egress 通** —— Forgejo 应用层应答 (403 = 未登录, 预期) |
| 内网 issue 端点 | 403 | `application/json` | 同上 |
| 外网 `forgejo.10cg.pub` | curl(60) TLS 自签证书 | — | 容器出网被 TLS 拦截; 生产不走此路径 |

**带 auth 腿 (PAT 来自 `nomad/jobs/aria-layer2-runner`, 即 Layer 2 容器实际用的那份)**:

```
PROBE name=internal_issue verdict=FAIL http=401 ctype=application/json bytes=96
  error_body: {"message":"user does not exist [uid: 0, name: ]"}
```

### 2.3 四份 PAT 有效性矩阵 (同一 issue 端点, 只输出 http code + sha256 前 8 位指纹)

| Nomad 变量路径 | 指纹 | 长度 | 结果 |
|---|---|---|---|
| `nomad/jobs/aria-layer2-runner` ← **Layer 2 容器实际用的** | `ed07d152` | 40 | **401 user does not exist (失效)** |
| `nomad/jobs/aria-orchestrator` ← Layer 1 用 | `c957308a` | 40 | **200 OK (有效, user = `aria-runner-bot`)** |
| `nomad/jobs/aria-runner-template` | `2c3fdb16` | 40 | 401 失效 |
| `nomad/jobs/aria-build` | `446b7916` | 40 | 403 `token does not have at least one of required scope(s): [read:issue]` (有效但 scope 窄) |

四份是**四个不同的 token**。

### 2.4 判定

- **egress: PASS** (heavy-node 容器 → 内网 Forgejo 可达, 返回合法 JSON, 非 CF-Access 伪成功)
- **auth: FAIL** —— Layer 2 那份 PAT 已失效。后果不止 fetch:
  `initial.sh:602` 的 `REPO_URL` 把同一个 PAT 内嵌进 git clone URL, 所以**容器连 clone 都做不了**。
- 机制侧是「对」的: 401 落 `classify_http_result` 的 `NON_RETRIABLE:http_401` → 不重试 →
  `emit_outcome_marker INPUT_FETCH_FAILED` —— AC-6 的 infra-fail 归类会正确工作。
  但**没有任何一次自主 dispatch 能成功**, 直到 PAT 修好。
- 相关: Aria #151 (确认两个 `10cg-ci-bot` token 归属) — 本次实测给了它一个具体后果。

### 2.5 待 owner 决定 (凭据动作, AI 不自行改)

修法候选 (**2026-08-30 复核后修订, 见 §2.6**): ~~(a) 把 `aria-orchestrator` 那份有效 PAT 同步进
`aria-layer2-runner`~~ —— **复核证伪**: 该 token 只有 `read:repository + write:issue`, `git push --dry-run`
实测 403, 搬过去 clone 能过、push/开 PR 必挂; (b) 给 `10cg-ci-bot` 签一枚 Layer 2 专用 token
(至少 `write:repository` + `write:issue`; 不需要 `write:package`, 镜像拉取已由 `docker_auth_*` 承担),
经 get-json→改单键→`put -check-index` 写入 `nomad/jobs/aria-layer2-runner.FORGEJO_BOT_PAT`;
(c) 若 owner 手里还存着 `aria-runner-bot-prod-20260523-v2-full-scope` (Aether 指纹 `5aaff023`,
10cg-ci-bot 名下, 最后使用 2026-07-03, 四个 Aria 变量里都没有它) 的值, 可直接复用, 但它带
`write:package` 属过宽 (Aria #151 第 4 点已提醒)。

### 2.5b owner 裁定 (2026-08-30): 归属 = Aria, 已落地纸面三件

owner 问「token 归 Aria / Aether / 10cg local 谁管」→ 裁定三层: 实例 = 10cg.local, 账号 + 规则 + 集群级 token = Aether,
应用级 token = Aria (判据沿用 08-08 决策「谁有轮换执行面」)。全文: `.aria/decisions/2026-08-30-forgejo-token-ownership-three-layers.md`。
落地: 台账 `.aria/pat-inventory.yaml` / state-check `forgejo-app-token-liveness` (首跑 Layer 1 OK, Layer 2 FAIL DEAD — 预期) /
Aria #151 归属回复 comment 20214。签 token 那一步归 owner (或走 Aether 原语), 见决策文件「待办」。

### 2.6 复核 (2026-08-30, owner 要求「重新核对」)

**方法 1 — HTTP API (curl, heavy 节点容器内, 与昨天同源变量)**:

| 变量路径 | 指纹 | 形态 | `/user` | `issues/188` | `Bearer` 头 | 判读 |
|---|---|---|---|---|---|---|
| `aria-layer2-runner` | `ed07d152` | hex40 | 401 | 401 | 401 | `user does not exist [uid: 0]` — Forgejo 的 access_token 表里**没有这枚 token** (uid 为 0 = 按 SHA 查不到; 若是「用户被删」uid 会是非零) |
| `aria-orchestrator` | `c957308a` | hex40 | 403 缺 `read:user` | **200** | 403 | 有效, 但 scope 窄 |
| `aria-runner-template` | `2c3fdb16` | hex40 | 401 | 401 | 401 | 同第一行, 死 token |
| `aria-build` | `446b7916` | hex40 | 403 | 403 | 403 | 有效, 仅 `write:package` (= Aether 台账 T4 `sha256=446b79`, 指纹算法对上了) |

形态全部 hex40 ⇒ 排除「模板渲染 / 存储把值弄坏」; `token` 与 `Bearer` 两种头一致 ⇒ 排除 header 形式问题。

**方法 2 — git 本体 (alpine/git, URL 形式逐字对齐生产 `initial.sh:602` `http://aria-runner-bot:<PAT>@…`)**:

| 变量路径 | `git ls-remote` (读) | `git push --dry-run` 到不存在的分支 (写, 只走鉴权不落引用) |
|---|---|---|
| `aria-layer2-runner` | rc=128 `Authentication failed` | `remote: Credentials are incorrect or have expired` |
| `aria-orchestrator` | **rc=0, 8 refs** | **403 Forbidden** ⇒ 无 `write:repository`, **不能给 Layer 2 用** |
| `aria-build` | 403 | 403 |

顺带证实: 账号 2026-07-01 已从 `aria-runner-bot` 改名 `10cg-ci-bot`, 但 URL 里旧用户名 + 有效 token 照样过
(Forgejo basic auth 以 token 定用户, 用户名只影响日志可读) ⇒ **改名不是失效原因**。

**结论**: Layer 2 那份 PAT **确实失效**, 两种方法、两种协议、两种 header 形式一致; 且它是 Forgejo 侧
「不存在」而非「权限不够」。

**它是怎么死的 (尽力追溯, 非定论)**: 变量 `nomad/jobs/aria-layer2-runner` 创建于 2026-05-22 12:37Z
(M5 Phase C 填 8 键), 唯一一次修改是 2026-07-12 21:22Z (Aether 为 DEC-20260712-001 加 `docker_auth_*`
两键, 其工具走 get→改→put -check-index, 不动其他键)。2026-05-23 的 handoff 记录当天**吊销**了
`aria layer2 runner 2026 05 22` 这枚 token (docker-auth 修复时换成 v2-full-scope 放到节点 docker config),
同一 session 还发生过「编辑 l2var.json 时 FORGEJO_BOT_PAT 替换错位, 40 字符长度蒙骗了验证」。
最可能: 变量里留的是 05-22 那枚、05-23 已吊销的 token。Nomad 只记最后修改时间, 无法从变量侧铁证;
Forgejo 侧要 owner 用密码登录列 token 才能对账。`aria-runner-template` 那份 (04-22 起未动) 死因同类。
**系统性原因** = 吊销 token 时没有枚举全部 Nomad 变量 store —— 与 Aether H1 教训同型
(`feedback_revoke_shared_token_enumerate_all_stores`)。

**复现**: scratchpad `m6-pat-recheck.hcl` (curl 矩阵) / `m6-pat-scope-probe.hcl` (git 读写探针);
两个 job 跑完已 purge。

---

## 3. TASK-021 (build) —— 未触发, 待决

- `/aether:aether-build-container` 是 owner-triggered 原语, `detailed-tasks.yaml` TASK-021
  的 notes 也把它建模为 owner action (AI preps, owner triggers)。
- 另有一个真实的顺序疑问: tasks.md 的注记写「对 **post-merge master SHA** 构建」, 但
  TG-1 容器侧代码只在 `feature/m6-dispatch-input-delivery` 上, 而 C.2 合并本身又被这四道门
  挡着 —— 要么先从 feature 分支 build 供 dogfood 用, 合并后再 rebuild; 要么先合再 build。
- **且 memory `feedback_freeze_task_must_coland_with_volatile_state_phase` 提醒**:
  TASK-022 的 IMAGE_SHA freeze 不该在 168h 跑不可能启动的当口做 —— 冻早了就会在真正开跑前
  作废。建议 022 与「跑起来」同批。

---

## 4. 账目影响

| Task | 原 | 现 | 依据 |
|---|---|---|---|
| TASK-028 | pending | **in_progress** (egress PASS / auth FAIL, 被 PAT 阻断) | 本文件 §2 |
| TASK-029 | pending | pending (双重阻断: Blocker 4 + PAT) | §1.5 + §2.4 |
| TASK-021 | in_progress | in_progress (未触发, 待 owner + 顺序裁定) | §3 |

另记一条**账目自身的不一致** (供下次清理): `detailed-tasks.yaml` 里 `TASK-028.dependencies`
写着 `[TASK-021]`, 而 `proposal.md:13` 写的是「互为前置 **021→022, 028→029**」两条独立链。
本次实测证明 028 确实不需要新镜像 (探的是网络/凭据, 与镜像无关), 以 proposal 为准。

## 5. 证据可复现

探针 HCL 与脚本留在本 session scratchpad:
`m6-egress-probe.hcl` / `m6-egress-probe-auth.hcl` / `m6-pat-matrix.hcl` /
`luxeno_latency_probe.py` / `luxeno_probe2.py` / `luxeno_probe4.py`。
三个临时 Nomad job 跑完已 `nomad job stop -purge` 清理, 集群无残留。
