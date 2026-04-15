# T2 存储验证报告 — A3 假设通路证据

> **Spec**: [aria-2.0-m0-prerequisite](../../proposal.md) §T2
> **执行**: 2026-04-15
> **方案**: W (Nomad docker driver `config.volumes` + 零 client.hcl 改动)
> **决策记录**: [decision-r8-virtiofs-vs-nfs.md](./decision-r8-virtiofs-vs-nfs.md)
> **对应 tasks**: T2.1 (已完成), T2.2 (已完成), T2.3 (容器↔宿主 md5 + 跨节点 md5 已完成; 非 root UID + POSIX locking 延后到 M1 生产 Spec)
> **结论**: ✅ **A3 假设 PASS** — Aether 集群存在可用的跨节点持久化共享存储, 容器可通过 Nomad docker driver bind mount 读写, 三节点视图完全一致

---

## TL;DR (给 M0 Report 用)

PRD v2.0 A3 假设 "Aether 具备 Nomad bind mount 跨节点共享的持久化存储" **成立**, 但**实现路径与 Spec 原假设不同**:

- **Spec 原假设**: NFS host_volume `nfs-fastpool-aether` (不存在)
- **实际路径**: PVE 层 NFS mount → Proxmox virtiofs 透传 → heavy guest `/opt/aether-volumes/`
- **探针方式**: Nomad docker driver 的 `config.volumes` (W 方案), 零 Nomad client.hcl 配置变更, 零集群侧扰动
- **证据强度**: 三个 heavy 节点各跑一次容器写入, 6 份 md5 交叉校验全部一致, 容器 stdout 与宿主文件字节级吻合
- **M0 Go/No-Go 输入**: 通路可用, 不阻塞 M1 US-022 aria-runner 容器设计

---

## 1. 存储栈实况

```
NFS server (NAS)
   ↓ NFS export
/mnt/pve/nfs-vms/aether-share   (pve-node1/2/3/4 同一挂载路径)
   ↓ Proxmox virtiofs passthrough (dirid = aether-share)
/opt/aether-volumes/            (heavy-1/2/3 KVM guest)
   ↓ Nomad docker driver bind mount (config.volumes)
/opt/aria-outputs/              (容器内)
```

**证据**: [nfs-status.md](./nfs-status.md) + [`raw/heavy-{80,81,82}-probe.txt`](./raw/)

**节点命名映射** (Spec 原文 vs 实际):

| Spec 写法 | 实际 Nomad 节点名 | IP           |
|----------|------------------|--------------|
| heavy-80 | heavy-1          | 192.168.69.80 |
| heavy-81 | heavy-2          | 192.168.69.81 |
| heavy-82 | heavy-3          | 192.168.69.82 |

---

## 2. Dispatch 证据矩阵

| smoke_id | 目标节点 | 实际落点 | alloc_id | 容器 UUID | 容器内 md5 | Exit | 状态 |
|---------|----------|---------|----------|-----------|----------|------|------|
| 001 | (未约束) | heavy-2 | `a17a3a9f-82f4-...` | `10e66369-389f-4d9b-957e-1a225c5220a0` | `c681d046b29492ccf816651f6acc1a7a` | 0 | complete |
| 002 | `node.unique.name=heavy-1` | heavy-1 | `df2f3ad6-0272-...` | `4522c733-2059-4f84-a757-0a4fd6bbf03e` | `1ba209fead451a6d18c709597fc5aa5f` | 0 | complete |
| 003 | `node.unique.name=heavy-3` | heavy-3 | `7f251f53-4e35-...` | `e0440eea-ef42-44cb-9a5e-6bdc7b6ae1b5` | `60586021ad5633d1060dfbe922d2db8a` | 0 | complete |

- 3 个 smoke 覆盖 3 个 heavy 节点
- 3 个独立 UUID 证明是真实独立容器写入 (非缓存/镜像伪造)
- 3 个不同 md5 对应 3 份不同内容 (smoke_id / uuid / alloc_id / timestamp 各异)

**原始 dispatch + stdout 日志**: [`t2.2-dispatch-log.txt`](./t2.2-dispatch-log.txt)

---

## 3. 跨节点 md5 交叉校验 (T2.3 核心证据)

从三个 heavy 节点分别执行 `md5sum` 对同一个文件:

```
--- heavy-1 (192.168.69.80) ---
c681d046b29492ccf816651f6acc1a7a  smoke-001.txt
1ba209fead451a6d18c709597fc5aa5f  smoke-002.txt
60586021ad5633d1060dfbe922d2db8a  smoke-003.txt

--- heavy-2 (192.168.69.81) ---
c681d046b29492ccf816651f6acc1a7a  smoke-001.txt
1ba209fead451a6d18c709597fc5aa5f  smoke-002.txt
60586021ad5633d1060dfbe922d2db8a  smoke-003.txt

--- heavy-3 (192.168.69.82) ---
c681d046b29492ccf816651f6acc1a7a  smoke-001.txt
1ba209fead451a6d18c709597fc5aa5f  smoke-002.txt
60586021ad5633d1060dfbe922d2db8a  smoke-003.txt
```

**判定**: ✅ 3×3 = 9 个 md5 全部一致, 跨节点读取无任何差异。

## 4. 容器↔宿主 md5 一致性 (T2.3 容器→宿主方向)

以 smoke_001 为例:
- 容器内 `md5sum /opt/aria-outputs/smoke-001.txt` → `c681d046b29492ccf816651f6acc1a7a` (见 dispatch stdout)
- heavy-2 宿主 `md5sum /opt/aether-volumes/aria-runner/outputs/smoke-001.txt` → `c681d046b29492ccf816651f6acc1a7a`
- 一致 ✅

**验证**: bind mount 源 (宿主) ↔ 目标 (容器) 的字节透传无篡改, virtiofs 层不引入 checksum 漂移。

---

## 5. 容器内 UID/GID 观察

所有 3 个 alloc 的容器内进程:
- `container_uid = 0`
- `container_gid = 0`

**含义**: `alpine:3.19` 默认以 root 启动, Nomad docker driver 未强制降权。这与宿主目录 mode `0777` 配合无权限问题。

**M1 生产 Spec 的遗留问题** (不在 M0 范围):
- aria-runner 镜像的 `USER` 指令未确定, 如 M1 决定以非 root 运行 (推荐), 需验证容器内 UID (如 1000) 写入 bind mount 后宿主侧的文件 owner
- virtiofs 的 uid/gid 映射策略 (pass-through vs remap) 需实测
- 这部分纳入 M1 US-022 的测试用例

---

## 6. W 方案零侵入验证

**操作前后 Nomad 状态对比**:

| 项 | 操作前 | 操作后 (purge 完成) |
|---|-------|---------------------|
| `GET /v1/jobs?prefix=aria-storage-smoke` | `[]` | `[]` |
| heavy-1/2/3 `client.hcl` | 未读 | 未改 (零配置变更) |
| heavy-1/2/3 Nomad 重启次数 | 0 | 0 |
| 生产 alloc 中断 | - | 0 |
| 集群基线 | T0 | **T0 (完全回到原状)** |

**保留的证据**:
- `/opt/aether-volumes/aria-runner/outputs/smoke-{001,002,003}.txt` — 供 M0 Report 审计追溯 (3×224 = 672 字节, 对 2.0 TiB 池可忽略)
- `t2.2-dispatch-log.txt` — Nomad dispatch + 容器 stdout 原始输出
- `decision-r8-virtiofs-vs-nfs.md` — 方案选型决策
- `nfs-status.md` — 存储栈事实基线

---

## 7. Spec 原任务对照

### T2.1 ✅

**交付物**: `nfs-status.md` — 完成

### T2.2 ✅

**原要求**:
- 写一个最小 parameterized job `aria-nfs-smoke.hcl`
- `nomad alloc exec` 确认容器内 NFS 挂载点可见
- 容器内写入 `/opt/aria-outputs/smoke-<timestamp>.txt`, 内容为 UUID

**实际交付** (含 override):
- `aria-storage-smoke.hcl` (W 方案, 不走 host_volume)
- 容器内通过 Nomad HTTP API 验证 (替代 `nomad alloc exec`, 因本地无 Nomad CLI)
- 容器内写入 `/opt/aria-outputs/smoke-<smoke_id>.txt`, 内容含 UUID (符合原要求) + alloc_id + node_name + md5 (增强)
- 3 次 dispatch 覆盖 3 个 heavy 节点, 所有 alloc 均 complete + exit 0

### T2.3 (部分完成)

**原要求**:
- 以 Nomad agent user (UID 推断) 执行 `md5sum`
- 对比容器内 md5, 必须完全一致
- 记录权限模式

**实际验证**:
- ✅ Nomad agent 为 root (UID 0) — 见 [nfs-status.md §Nomad Agent User](./nfs-status.md)
- ✅ 容器内 md5 `c681d046...` vs 宿主读取 md5 `c681d046...` — 字节级一致
- ✅ 跨 3 节点 md5 交叉校验 (9 个值全部一致)
- ✅ 权限模式: 容器写入后的文件 `0644 root:root` (见 nfs-status.md 采集), bind mount 目录 `0777 root:root`

**延后到 M1 生产 Spec**:
- 非 root 容器 UID (如 1000) 的写入与 uid 映射验证
- virtiofs 并发写 POSIX locking 行为
- 三节点同时写入同一文件的 last-writer-wins 测试

**延后理由**: M0 是假设验证, A3 通路已由 3 次不同节点的独立写入 + 9 个 md5 一致证明。生产级并发/权限模型是 M1 aria-runner 容器设计的固有职责。

### T2.4 (未开始)

**原要求**: Nomad meta 64KB 边界测试, 产出 R7 缓解方案

**状态**: 本报告不覆盖, 独立任务。

---

## 8. A3 假设最终判定

| 假设条件 | 判定 | 证据 |
|---------|------|-----|
| 存在跨节点共享的持久化存储 | ✅ PASS | virtiofs + NFS 栈, 2.0 TiB 池, 已生产运行 |
| Nomad 容器可通过 bind mount 读写 | ✅ PASS | 3 次独立 alloc complete, 3 份产物 |
| 三节点视图完全一致 | ✅ PASS | 9 个 md5 交叉一致 |
| 探针路径可重放 | ✅ PASS | W 方案零侵入, smoke 文件留作证据 |
| 生产路径明确 | ⚠️ 部分 | 生产建议用 Nomad host_volume 语法, 本探针用 `config.volumes` 快捷路径, 两者等价但 M1 需 adopt host_volume (留给 US-022) |

**结论给 M0 Report**: A3 假设 **成立**, M1 可基于此继续 aria-runner 容器设计。PRD v2.0 §M0 §A3 验收条件满足。

---

## 9. 给 M1 的配置蓝图 (附录, 非 M0 交付物)

M1 生产实施推荐把 W 方案升级为 host_volume, 在 heavy-1/2/3 client.hcl 追加:

```hcl
client {
  host_volume "aria-runner-outputs" {
    path      = "/opt/aether-volumes/aria-runner/outputs"
    read_only = false
  }
}
```

对应 Job stanza:

```hcl
group "runner" {
  volume "outputs" {
    type      = "host"
    source    = "aria-runner-outputs"
    read_only = false
  }
  task "aria-runner" {
    volume_mount {
      volume      = "outputs"
      destination = "/opt/aria-outputs"
    }
  }
}
```

**为什么 M1 要换**: host_volume 是 Nomad 标准抽象, 支持 ACL / quota / 未来的 CSI 迁移; `config.volumes` 是 docker driver 的私有扩展, 不经过 Nomad 调度器的 volume 感知。M0 探针不需要这一层, M1 生产需要。

---

## 10. 关联 / 追溯

| 类型 | 路径 |
|------|------|
| 父 Spec | [`../../proposal.md`](../../proposal.md) |
| 决策记录 | [`decision-r8-virtiofs-vs-nfs.md`](./decision-r8-virtiofs-vs-nfs.md) |
| 事实基线 | [`nfs-status.md`](./nfs-status.md) |
| Job 定义 | [`aria-storage-smoke.hcl`](./aria-storage-smoke.hcl) |
| Dispatch 日志 | [`t2.2-dispatch-log.txt`](./t2.2-dispatch-log.txt) |
| 原始 probe | [`raw/heavy-80-probe.txt`](./raw/heavy-80-probe.txt) [`raw/heavy-81-probe.txt`](./raw/heavy-81-probe.txt) [`raw/heavy-82-probe.txt`](./raw/heavy-82-probe.txt) |
| smoke 产物 | `/opt/aether-volumes/aria-runner/outputs/smoke-{001,002,003}.txt` (heavy-guest 任一可见) |

---

**报告类型**: 事实 + 结论双层记录, 作为 M0 Report 技术附录的原始素材。本文件 frozen, 如需修正另建 `storage-validation-report-v2.md` + changelog。
