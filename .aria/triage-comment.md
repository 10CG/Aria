## Triage 更正 — 我上一条 (issuecomment-17187) 的 case-3 判定是错的

上一条把「无 redirect 的写向 `curl -X PUT /v1/var/` 被拦」判为**过度拦截**, 依据是 issue 原文的前提「PUT 上传, response 丢弃, 不回显 secret」。**我没有核实这个前提, 它是错的。**

### 事实

HashiCorp Nomad Variables API 官方文档 (Create/Update Variable, `PUT /v1/var/:var_path`) 的成功响应示例:

```json
{
  "Namespace": "prod",
  "Path": "example/first",
  "CreateIndex": 1457,
  "ModifyIndex": 1457,
  "CreateTime": 1662061225600373000,
  "ModifyTime": 1662061225600373000,
  "Items": {
    "user": "<值>",
    "password": "<值>"
  }
}
```

(官方示例的 `Items` 里是**明文键值对**; 此处按 secret 卫生把示例值替换为占位符 — 原文档给的是可读的明文口令字面量, 这正是要点所在。)

原文: 「The response body returns the created or updated variable along with metadata created by the server」—— **response body 含解密后的 `Items` 值**。

### 因此

无 redirect 的写向 PUT **确实会把 secret 打进 tool output**。secret-guard 拦它是**正确行为, 不是 bug**。而 issue 原文那句「response 丢弃」指的正是 `>/dev/null` —— 而带 `>/dev/null` 的形态本来就被放行 (上一条 case-1/2 已实测)。

**结论: issue 要求 2 (`/v1/var/` 读写分离) 的前提整个不成立, 该项无需修改。** 现行 hook 在这个面上的判据是准的:

| 写向形态 | 是否回显 secret | 现行 hook | 判定 |
|----------|----------------|-----------|------|
| `curl -X PUT ... --data-binary @file >/dev/null` | 否 | exit=0 放行 | ✅ 正确 |
| `curl -X PUT ... --data-binary @file -o /dev/null` | 否 | exit=0 放行 | ✅ 正确 |
| `curl -X PUT ... --data-binary @file` (无 redirect) | **是** (response 含 Items) | exit=2 拦 | ✅ 正确 |
| `curl -v -X PUT ...` | **是** (verbose 回显请求体) | exit=2 拦 | ✅ 正确 |
| `curl --trace-ascii - -X PUT ...` | **是** | exit=2 拦 | ✅ 正确 |
| `curl -X PUT ... -d '{"Items":{...}}'` | **是** (值上 argv) | exit=2 拦 | ✅ 正确 |

六种形态逐条实测, 安全的放行、危险的拦住, 无假阴也无假阳。

---

## 但实测暴露了一个**真** gap (本次修复的新目标)

`nomad var put` **完全不在 risky_patterns 内** (pattern 只列了 `nomad var (get|list)`), 而它有个反直觉的默认行为 —— 本机 nomad v1.11.2 `nomad var put --help` 原文:

```
-out (go-template | hcl | json | none | table)
   Format to render created or updated variable. Defaults to "none" when
   stdout is a terminal and "json" when the output is redirected.
```

**在 Claude Code 的 Bash 工具里 stdout 是 pipe 而非 terminal**, 于是 nomad 判定为「输出被重定向」→ 默认渲染完整变量 JSON (含 `Items` 值) → **直接进 AI 上下文**。而 hook 对它零拦截:

| 形态 | 是否回显 | 现行 hook | 判定 |
|------|---------|-----------|------|
| `nomad var put -in=json <path> @file` (非 TTY) | **是** (-out 默认切 json) | exit=0 放行 | ❌ **gap** |
| `nomad var put <path> PAT=<value>` | **是** (值上 argv + 渲染) | exit=0 放行 | ❌ **gap** |
| `nomad var put -out=none ...` | 否 | exit=0 放行 | ✅ 正确 |
| `nomad var put ... >/dev/null` | 否 (渲染被吞) | exit=0 放行 | ✅ 正确 |

这才是本次事故第 3 环的真实机制 —— 也解释了为什么绕道 `nomad var put` 会泄漏, 但机制不是 issue 说的「回显走 stderr」(stderr 是 `-verbose` 档), 而是**非 TTY 下 stdout 渲染**。

### 附带发现: 测试面结构性盲区

`hooks/tests/secret-guard.test.sh:56-59` 的 `/v1/var/` 用例**全为读向** (GET / wget)。上面那张「六种写向形态」表里的正确行为**一条都没有测试锁定** —— 将来任何人调整 has_filter 逻辑都可能无声破坏它, 而且没有红灯。

## 修复范围 (owner 已定案)

1. **拦 `nomad var put` 的不安全形态** (无 `-out=none` 且无 stdout redirect), 安全形态继续放行;
2. **补写向测试用例族** — 把上面两张表的 10 条行为全部锁定 (含现已正确的 6 条, 防回归);
3. 要求 2 (读写分离) **关闭, 无需修改** —— 前提经官方文档证伪。

Level 2 spec 起草中, 走完整 post_spec 审计。要求 1 (轮换 T4 + revoke `446b79`) 仍是 owner/infra 项, 不在本 cycle。要求 3 已转交 aether ([aether-plugin#11](https://forgejo.10cg.pub/10CG/aether-plugin/issues/11), 前提同样做了修正 —— 现行 skill 用的是 curl PUT 而非 `nomad var put`, 原建议不适用)。

---

*更正由 `/issue-triage` 复核产生 — 教训: 「X 坏了」类 issue 在动手前必须独立核实 X 真的坏了, 上一条我拿 issue 的前提当事实用了。*
