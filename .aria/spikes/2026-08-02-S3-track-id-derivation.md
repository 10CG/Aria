# Spike S3 — track-id 该怎么派生? (三版三个答案, 每版都被推翻)

> **母 Spec**: `openspec/changes/a1-entry-claim-duplicate-work-guard/` (spike-first 挂起)
> **触发**: 该项三版三个答案且**每版都被下一轮审计推翻** —— 原始 (spec-slug) → R1-fix (issue 派生) → R2-fix (加容器段)。
> **执行**: 2026-08-02, 主控直接实读代码 + 生产 ref 取证
> **附带任务**: 回答 R3/M2 —— 「接手」在含容器段后的可操作定义

---

## 结论 (先给答案)

**派生规则: `<归一后 basename>-<number>-<container_uuid>`, 其中 `container_uuid` 取 container-id 文件的 `uuid` 字段本身 (8 位十六进制), 不截断、不用 `label`。**

碰撞域**已知且小**: 8 位 hex = 16⁸ ≈ 4.3×10⁹, 生日碰撞需 ~65k 个容器; 本 Lab 实测 **2 个**。

**「接手」的可操作定义: 不存在一键接手 —— 现有代码结构上不支持跨容器 release。** 见 §4。

---

## §1 三版被推翻的轨迹 (为什么必须 spike)

| 版本 | 派生规则 | 被谁推翻 | 根因 |
|---|---|---|---|
| 原始 | `spec-slug` | R1/M2 | A.1 期间改名极常见 ⇒ `release_claim_by_track` 按新 slug 定位 ⇒ 静默 `claim_not_found` ⇒ 孤儿 claim |
| R1-fix | `<basename>-<number>` (纯 issue 派生) | **R2/C1** | 两轨做同一 issue ⇒ **同 track_id** ⇒ 被 `collision.py:219-220` 互相排除 ⇒ **overlap 恒空, 主机制死** |
| R2-fix | `<basename>-<number>-<container-short>` (**前 8 位**) | **R3/M1** | `get_container_id()` **label 优先**, 而文件模板**明确邀请**用户设 human-readable label ⇒ `devbox-A1`/`devbox-A2` 截断后同为 `devbox-A` ⇒ 同 track_id ⇒ **R2/C1 的后果换个触发对象复现** |

**三次都是同一形状**: 派生规则的**碰撞域没被穷举**, 每次都是下一轮审计构造出反例才发现。⇒ 这正是必须 spike 而非继续写 Spec 的理由。

---

## §2 `container_id` 的真实取值空间 (实测)

**`get_container_id()` 逻辑** (`lib/identity.py:191-244`), docstring 逐字:

> Returns `label` field if non-empty, **otherwise `uuid` field value**. Falls back to hostname when the file cannot be read *and* cannot be created.

⇒ **三种可能取值**: (1) 用户设的 `label` (**任意字符串**); (2) 自动生成的 8 位 hex `uuid`; (3) **hostname** (只读文件系统兜底)。

**文件模板** (`identity.py:126-140`) 逐字:

```
# Edit the `label` line to add a human-readable tag (e.g. "devbox-A" / "laptop")
uuid: 023236f2
label:
created_at: ...
```

⇒ **模板主动邀请用户设 label** ⇒ R3/M1 的担忧**不是理论风险, 是被文档鼓励的用法**。

**生产实测**:

| 容器 | `uuid` | `label` | `get_container_id()` 返回 |
|---|---|---|---|
| 本容器 | `023236f2` | **空** | `023236f2` |
| 并发轨 | `bfe8285d` | (推定空) | `bfe8285d` |

⇒ **今天两个容器都走 uuid 分支, label 全空** —— R3/M1 属**结构性 dormant 风险**, 不是活跃 bug。但只要有人照模板建议设了 label, 它立即变活跃。

---

## §3 派生规则定案与碰撞域

**规则**: `<归一后 basename>-<number>-<container_uuid>`

| 段 | 取值 | 碰撞域 |
|---|---|---|
| `basename` | §0 归一后的 repo basename | 见下方「已知限」 |
| `number` | **`str(int(number))`** —— 与 §0 的 int 解析对齐 (R3/M3b: 否则 `#007` 与 `#7` 派生出两个 track_id ⇒ 自排除失效 ⇒ 自己较早的 claim 被误判为他人碰撞) | 无 |
| `container_uuid` | **container-id 文件的 `uuid` 字段本身**, 不截断、**跳过 label** | 16⁸ ≈ 4.3e9; 生日碰撞 ~65k 容器; 实测 2 个 |

**为什么跳过 label**: label 是**用户可任意命名**的字符串, 碰撞域不可控且被模板鼓励使用。uuid 是机器生成的定长 hex, 碰撞域可算。⇒ **需要新增一个直取 `uuid` 字段的 accessor** —— 现有 `get_container_id()` 是 label 优先, 不能直接用。(实测 `identity.py:222` 是 `return label if label else uuid`, `:244` 是 hostname 兜底。)

**为什么不截断**: 8 位已是 uuid 全长 (`_generate_uuid()` 产 8 char hex), 截断是 no-op 于 uuid 分支、却是碰撞源于 label 分支。**不截断 = 一条规则同时对两个分支安全**。

**hostname 兜底分支**: 只读文件系统时 `get_container_id()` 返回 hostname。新 accessor 须定义该分支行为 —— 建议**同样返回 hostname**并接受其碰撞域 (同名主机罕见, 且该分支本身已是降级路径)。

**已知限 (承 R3/M3a)**: `derive_track_id` 会把 `/`、`.`、`_` 全部译成 `-` (`track_id.py:71`)。⇒ 仓名 `aria.orch` / `aria_orch` / `aria-orch` 三者**在 §0 判不同** (§0 只做 casefold) 但**归一后塌成同一 track_id**。**本组织当前无含 `.`/`_` 的仓名** (实测: `Aria` / `aria-plugin` / `aria-orchestrator` / `aria-standards`) ⇒ **dormant, 非活跃**。处置: 记为已知限并加一条断言型 SC 钉死当前行为 (仿 `linked-issue-normalization` 的 SC-5 处理别名的方式)。

---

## §4 「接手」的可操作定义 (R3/M2)

**现状实测**:

- `release_claim_by_track` (`claim_lifecycle.py:377+`) 只匹配**调用者自己的** container (`rec.container == resolved.container_id`);
- grep 复核: **无任何函数支持释放别的容器的 claim**;
- 既有 takeover 路径 `_takeover_eligible` (`phase1_gate.py:282-293`) 的条件是 `stale_takeover_eligible` / `no_active_candidates` / `empty_claims` —— 它处理的是**同 track_id 的陈旧 claim**, 而含容器段后**两轨必然不同 track_id** (这正是 R2/C1 修复要的效果) ⇒ **既有 takeover 路径对本场景不可达**。

⇒ **「接手」不能是一键动作。** 三个可选定义:

| 定义 | 可行性 | 代价 |
|---|---|---|
| **(i) 两步人工** — owner 去对方容器执行 release, 再由本容器 acquire | ✅ 现有代码即可 | AskUserQuestion 的选项文案**必须说清这是两步人工**, 不是一键 |
| (ii) 新增跨容器 release | ⚠️ 需新函数 + 授权检查 (写别人的 claim 是权限面) | 新表面; 与 advisory-over-hardlock 立场需对齐 |
| **(iii) 不接手 —— 直接并行, 让 reconcile 仲裁** | ✅ 零代码 | 与 advisory 语义最一致; 但两轨真的会重复劳动 |

**建议 (i)**, 并把选项文案从「接手」改为**「我去释放对方的 claim 后再开始 (两步)」** —— 措辞即定义, 避免实现者以为有一键路径。**(ii) 不建议在本 Spec 引入** (权限面变更应独立评估)。

---

## §5 给母 Spec 重写时的可执行结论

1. **派生规则**: `<归一后 basename>-<str(int(number))>-<container_uuid>`; 无关联 issue 时回落 `<spec-slug>-<container_uuid>`;
2. **新增 accessor** 直取 `uuid` 字段 (跳过 label), hostname 兜底分支行为须成文 —— **Impact 表须补 `lib/identity.py`**;
3. **`number` 段用 int 归一后的字符串**, 与 §0 对齐;
4. **basename 分隔符碰撞记为已知限** + 断言型 SC;
5. **「接手」定义为两步人工**, AskUserQuestion 文案随之改写;
6. **SC 须覆盖**: (i) 两不同容器同 issue → track_id 不同 → overlap 互见 (R2/C1 红窗); (ii) 同容器 label 设为长字符串时 track_id 仍用 uuid (R3/M1 红窗); (iii) `#007` 与 `#7` 派生同一 track_id (R3/M3b 红窗); (iv) 改名前后 track_id 不变 (原始版的红窗)。

**注意**: 上述 6 条中的 (i)(ii)(iii)(iv) 四个红窗**分别对应四个被推翻的版本** —— 每个版本的失败模式都要有一条 SC 钉住, 否则第五版会再踩其中之一。

## §6 本 spike 未回答的

- basename 别名 (`aria-orch` vs `aria-orchestrator`) —— 属 **S4**, 需按 prose 语料统计;
- 归一 × `derive_track_id` 的**完整**碰撞穷举 —— 属 **S5** (本 spike 只覆盖了 container 段与 number 段, basename 段留给 S5)。
