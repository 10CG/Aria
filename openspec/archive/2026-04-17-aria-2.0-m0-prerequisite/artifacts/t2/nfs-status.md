# T2.1 — Aether 持久化存储现状调查

> **任务**: [aria-2.0-m0-prerequisite/tasks.md](../../tasks.md) T2.1
> **执行日期**: 2026-04-15
> **调查者**: Claude (Opus 4.6) + human operator
> **状态**: ✅ 事实收集完成, ⚠️ **Spec 假设需修正** (见 §结论)

---

## TL;DR

1. **Aether 集群没有 NFS**。heavy-1/2/3 三个节点都没有任何 `nfs` 挂载, 没有 `nfs-fastpool-aether` 这个卷名。
2. **实际架构是 virtiofs**。所有 heavy 节点共享同一个 **`aether-share` virtiofs** 挂载在 `/opt/aether-volumes`, 由 Proxmox 宿主透传到 KVM guest。
3. **跨节点共享已经自然成立**。virtiofs 的 source 是 Proxmox 宿主的单一目录, 三个节点看到的 `/opt/aether-volumes/` 就是同一份数据。
4. **节点命名偏差**: Spec 中写的 "heavy-80/81/82" 对应实际 Nomad 节点 `heavy-1`(192.168.69.80) / `heavy-2`(192.168.69.81) / `heavy-3`(192.168.69.82)。节点名 ≠ IP 后缀。
5. **T2 后续任务的 Spec 假设全部需要修正** — 不需要 NFS 配置, 不需要 `nfs-fastpool-aether` host_volume, 只需要为 `aria-runner` 在 `/opt/aether-volumes/` 下新增一个子目录并注册成 Nomad host_volume。

---

## 集群拓扑 (Nomad API 事实)

来自 `GET http://192.168.69.70:4646/v1/nodes` (2026-04-15):

| Nomad 节点名 | IP            | Class          | Status | Drain |
|-------------|---------------|----------------|--------|-------|
| heavy-1     | 192.168.69.80 | heavy_workload | ready  | false |
| heavy-2     | 192.168.69.81 | heavy_workload | ready  | false |
| heavy-3     | 192.168.69.82 | heavy_workload | ready  | false |
| light-1..5  | 192.168.69.90-94 | light_exec  | ready  | false |

**命名映射 (⚠️ 容易混淆)**:
- `heavy-1` = IP 尾 `.80` ← Spec 写作 "heavy-80"
- `heavy-2` = IP 尾 `.81` ← Spec 写作 "heavy-81"
- `heavy-3` = IP 尾 `.82` ← Spec 写作 "heavy-82"

**建议**: 后续 Nomad job `constraint` 务必用节点名 `heavy-1` 而非 `heavy-80`:
```hcl
constraint {
  attribute = "${node.unique.name}"
  value     = "heavy-1"
}
```

---

## 节点 × 挂载点矩阵

来自 SSH 远端 `mount | grep aether-volumes` + `findmnt /opt/aether-volumes` (原始输出见 `raw/heavy-{80,81,82}-probe.txt`)。

| 节点 | 挂载点 | 文件系统 | Source | Options | Size (df) | Used | Owner | Mode |
|------|--------|----------|--------|---------|-----------|------|-------|------|
| heavy-1 (.80) | `/opt/aether-volumes` | virtiofs | `aether-share` | rw,relatime | 2.0 TiB | 141 GiB (7%) | root:root | 0777 |
| heavy-2 (.81) | `/opt/aether-volumes` | virtiofs | `aether-share` | rw,relatime | 2.0 TiB | 141 GiB (7%) | root:root | 0777 |
| heavy-3 (.82) | `/opt/aether-volumes` | virtiofs | `aether-share` | rw,relatime | 2.0 TiB | 141 GiB (7%) | root:root | 0777 |

**一致性证据** (virtiofs 单宿主透传的侧面证明):
- 三个节点 `df` 输出的 `Size/Used/Avail` 完全一致 (2.0T / 141G / 1.9T)
- 三个节点 `ls /opt/aether-volumes/` 返回相同的 13 个子目录 + 相同 mtime (如 `test-volume-cli Mar 6 16:53`)
- `stat /opt/aether-volumes` inode 519 (heavy-2) — virtiofs 透传保留 host inode

**查 nfs/fastpool 的反向证据**:
- `mount | grep -iE 'nfs|fastpool'` → 无输出
- `findmnt -t nfs,nfs4` → 无输出
- `/proc/mounts` 中没有任何 `nfs*` 类型

---

## Nomad HostVolumes 现状

来自 `GET /v1/node/{id}` 的 `HostVolumes` 字段 (2026-04-15):

**heavy-1 已注册 (9 个)**: `my-api-{uploads,logs,data}`, `kairos-data`, `dev-db-{data,redis-data}`, `myapp-{data,logs}`, `kairos-prod-data`
**heavy-2 已注册 (10 个)**: `todo-{data,logs,backups,data-dev,logs-dev,backups-dev}`, `kairos-{data,prod-data}`, `nexus-{db-dev,redis-dev}`
**heavy-3 已注册 (8 个)**: `todo-{data,logs,backups,data-dev,logs-dev,backups-dev}`, `kairos-{data,prod-data}`

**共性**: 所有已注册 host_volume 的 `Path` 都是 `/opt/aether-volumes/<project>/<name>` 形式, 即指向 virtiofs 共享池的一个子路径。

**`nfs-fastpool-aether` 查询结果**: **无任何节点注册此名称的 host_volume**。Spec 里这个名字是虚构的 (或已过时)。

---

## Nomad Agent User

| 项目 | 值 |
|------|-----|
| systemd `User=` 字段 | 未设置 (默认 root) |
| 实际 `ps -o user,comm` | `root  nomad` |
| `id nomad` (系统用户) | `no such user` |

**结论**: Nomad agent 以 **root** 身份运行。写入 `/opt/aether-volumes/` 任何位置都不会有权限问题(宿主侧目录模式 0777 + Nomad 为 root)。**T2.3 的 UID 推断步骤可简化为 "root, UID=0"**。

> **Note for T2.3**: 即使 Nomad 是 root, 容器内进程 UID 可能不是 0 (取决于镜像的 `USER` 指令)。bind mount 把宿主 `/opt/aether-volumes/...` 透传到容器后, 容器内写入的文件在宿主侧归属取决于容器内的 effective UID。T2.3 的 md5 双向校验重点变成 "容器 UID → 宿主文件 owner" 的映射验证, 而非 "Nomad agent 是否有权限"。

---

## Spec 假设 vs 现实 — 影响矩阵

| Spec 任务 | Spec 原假设 | 现实 | 需修正? |
|----------|------------|------|---------|
| **T2.1** 现状调查 | "查证 heavy-80/81/82 是否挂载 `nfs-fastpool-aether`" | 无 NFS, 有 virtiofs `aether-share` | ✅ 本文档即修正 |
| **T2.2** parameterized dispatch | 用 `host_volume "nfs-fastpool-aether"` stanza | 需改为注册新 host_volume (如 `aria-runner-outputs` 指向 `/opt/aether-volumes/aria-runner/outputs`) | ⚠️ 改 Spec |
| **T2.3** 宿主 md5 校验 | Nomad agent UID 推断 | root (UID 0); 实际校验点是容器内 UID → 宿主文件 owner | ⚠️ 改 Spec |
| **T2.4** Nomad meta 64KB | 独立于存储, 不受影响 | 不变 | ❌ 保持 |
| **T3.3** read-only rootfs + bind mount | 依赖 "NFS 路径" | 改为依赖 `/opt/aether-volumes/aria-runner/` 路径 | ⚠️ 改 Spec |

**R7 / fallback 影响**:
- 原 Spec 的 fallback "单节点 `constraint` pin heavy-80" 不再必要 — virtiofs 已经自然做到三节点一致, 不存在 NFS 跨节点同步延迟问题
- 反而要注意的新风险: virtiofs 的 **Proxmox 宿主单点** (如果承载 `aether-share` 的 Proxmox 宿主挂了, 三个 heavy 节点的 `/opt/aether-volumes/` 全部不可用)。这个风险**本来就存在**于 todo-web / kairos / my-api 等所有现有服务, 不是 aria-runner 引入的新风险, 但需要在 M0 Report 里显式承认。

---

## 推荐方案 (给 T2.2 的输入)

**不要**: 配置 NFS、申请 `nfs-fastpool-aether` 卷名、修改 Nomad client.hcl 添加 NFS 挂载。

**改为**:
1. 在 Proxmox 宿主(承载 `aether-share` 的那台)为 aria-runner 创建目录:
   ```bash
   # 在 Proxmox 宿主执行 (不是 heavy-1 容器内)
   mkdir -p /path/to/aether-share/aria-runner/outputs
   chmod 0777 /path/to/aether-share/aria-runner/outputs
   ```
   → 因为是 virtiofs 透传, 此目录会自动在三个 heavy 节点的 `/opt/aether-volumes/aria-runner/outputs` 可见。

2. 用 `/aether:aether-volume create` 或直接修改 Nomad `client.hcl`, 在 **三个 heavy 节点** 分别注册:
   ```hcl
   client {
     host_volume "aria-runner-outputs" {
       path      = "/opt/aether-volumes/aria-runner/outputs"
       read_only = false
     }
   }
   ```

3. T2.2 的测试 job (`aria-nfs-smoke.hcl` → 建议改名 `aria-storage-smoke.hcl`) 的 `volumes` stanza:
   ```hcl
   group "smoke" {
     volume "outputs" {
       type      = "host"
       source    = "aria-runner-outputs"
       read_only = false
     }
     task "smoke" {
       volume_mount {
         volume      = "outputs"
         destination = "/opt/aria-outputs"
       }
     }
   }
   ```

---

## 未回答的问题 (交接给 T2.2/T2.3 或人工决策)

1. **Proxmox 宿主访问权限**: 谁有权限在 Proxmox 宿主的 `aether-share` 源目录下创建 `aria-runner/` 子目录? 这是 T2.2 的前置阻塞点 (如果没有 Proxmox 宿主访问权, 需要申请或找 Aether 运维代操作)。
2. **virtiofs 并发写一致性**: 三个 heavy 节点同时写入 `/opt/aether-volumes/aria-runner/outputs/same-file.txt` 时, virtiofs 的 locking 行为是什么? (T2.3 应测)
3. **虚拟化层故障域**: `aether-share` 背后的 Proxmox 宿主是否有备份/快照策略? 是否属于 aria-runner 的 MTTR 风险? (留到 M0 Report 的"风险与假设"章节)
4. **quota / 配额**: 2.0 TiB 总容量被所有服务共享, aria-runner 预计产出规模是多少? 是否需要 quota 限制防止挤压 todo-web / kairos 的数据? (R7 的新形态)

---

## 原始证据

| 文件 | 内容 |
|------|------|
| [`raw/heavy-80-probe.txt`](raw/heavy-80-probe.txt) | heavy-1 (.80) 的 mount + findmnt + stat + df + ls |
| [`raw/heavy-81-probe.txt`](raw/heavy-81-probe.txt) | heavy-2 (.81) 的同上 |
| [`raw/heavy-82-probe.txt`](raw/heavy-82-probe.txt) | heavy-3 (.82) 的同上 |

**调查命令链 (可复现)**:
```bash
# 1. Nomad 节点拓扑
curl -s http://192.168.69.70:4646/v1/nodes | jq '.[] | {Name, Address, NodeClass, Status}'

# 2. 每节点 HostVolumes
for id in $(curl -s http://192.168.69.70:4646/v1/nodes | jq -r '.[] | select(.NodeClass=="heavy_workload") | .ID'); do
  curl -s "http://192.168.69.70:4646/v1/node/$id" | jq '{Name, HostVolumes}'
done

# 3. 每节点宿主 mount (需 SSH)
for ip in 192.168.69.80 192.168.69.81 192.168.69.82; do
  ssh root@$ip 'hostname; mount | grep aether-volumes; findmnt /opt/aether-volumes; df -hT /opt/aether-volumes'
done
```

---

## 签字 & 下一步

- [x] T2.1 事实基线确立
- [ ] 将本文件的"Spec 假设 vs 现实"章节反映到 `proposal.md` 的 T2 章节 (T2.2/T2.3 重写, 或开一个 R8 修正决策记录)
- [ ] 与 Aether 运维确认 Proxmox 宿主的 `aether-share` 源目录路径和写权限 → 开通 T2.2 前置
- [ ] T2.2 执行时产出 `aria-storage-smoke.hcl` 和 dispatch 验证报告

**本文件类型**: 事实基线 (frozen, 不可追溯修改; 如需修正, 新建 `nfs-status-v2.md` + changelog)
