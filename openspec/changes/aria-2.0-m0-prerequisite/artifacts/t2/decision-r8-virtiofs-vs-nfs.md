# R8 决策记录 — virtiofs 取代 NFS 作为 aria-runner 持久化存储

> **Spec 变更**: [aria-2.0-m0-prerequisite](../../proposal.md) §T2 / §T3.3
> **记录日期**: 2026-04-15
> **决策人**: @simonfishgit + Claude (Opus 4.6)
> **证据基础**: [nfs-status.md](./nfs-status.md) + `raw/heavy-{80,81,82}-probe.txt`
> **状态**: ✅ Accepted (proposal.md 原文保持不变, 本记录作为 binding 修正)

---

## 背景

`aria-2.0-m0-prerequisite` Spec 的 T2 章节假设 Aether 集群存在名为 `nfs-fastpool-aether` 的 NFS 共享卷, 并把 "Nomad parameterized dispatch + NFS host_volume + 跨节点 md5 双向校验" 作为 aria-runner 持久化存储方案的核心验证路径。

T2.1 实测调查 (2026-04-15) 推翻了此假设: **集群没有任何 NFS 挂载**, 实际的跨节点共享存储通过 Proxmox 宿主 virtiofs 透传实现。

## 决策

**采用 virtiofs 方案**, 不引入 NFS。

具体: 为 aria-runner 在现有 virtiofs 共享池 (`aether-share` → 宿主 `/opt/aether-volumes/`) 下新建专属子路径 `aria-runner/outputs`, 并注册为 Nomad host_volume `aria-runner-outputs`, 供 T2.2 及后续 T3 bind mount 使用。

## 为什么 (Rationale)

| 维度 | NFS (原 Spec) | virtiofs (新方案) |
|------|--------------|------------------|
| **生产已验证** | ❌ 不存在 | ✅ 已承载 todo-web / kairos / my-api / nexus 等多个生产服务 |
| **跨节点一致性** | 需 NFS 协议 + 缓存策略 | 单宿主单目录, 自然一致 |
| **新增组件** | 需 NFS server/client 配置 | 0 新组件 |
| **新增 Nomad 配置** | host_volume + NFS 前置挂载 | 仅 host_volume (各节点已有 virtiofs 挂载) |
| **新增故障点** | NFS server + 网络 + 缓存一致性 | 复用现有 virtiofs 故障点 (无净新增) |
| **T2 工时** | 原估 4.5h (含 NFS 配置) | 预计 2.5h (跳过 NFS 部分) |
| **与现有模式一致性** | ❌ 与 todo-web 等不同 | ✅ 与所有现有 host_volume 一致 |

**关键洞察**: Spec 原假设试图解决一个集群里已经被解决的问题 (跨节点持久化共享)。todo-web / kairos / nexus 早已通过 virtiofs+host_volume 跑了几个月, aria-runner 没有理由另起炉灶引入 NFS 栈。

## 不选 NFS 的代价

如果真要上 NFS 栈:
- 需 Aether 运维配合在集群新增 NFS server (或对接外部 NAS)
- 需在三个 heavy KVM guest 安装 `nfs-common`, 配置 autofs / fstab
- 需修改 Nomad `client.hcl` 增加 NFS 挂载前置依赖
- 需解决 NFS 的 uid/gid 映射问题 (virtiofs 默认透传 host UID, NFS 需显式配)
- 预计工时 > 4.5h, 且引入的每一层都是**对 aria-runner 而言**的新故障域

ROI 为负。

## 实际存储栈 (2026-04-15 补充调查)

初版决策文档写的是 "Proxmox 宿主 virtiofs 透传", 忽略了 PVE 层的 NFS。实测 `pvesh get /cluster/mapping/dir/aether-share` 显示:

```
map = [
  "node=pve-node1,path=/mnt/pve/nfs-vms/aether-share",
  "node=pve-node2,path=/mnt/pve/nfs-vms/aether-share",
  "node=pve-node3,path=/mnt/pve/nfs-vms/aether-share"
]
```

**真实栈**:

```
NFS server (NAS) 
   ↓ NFS mount (PVE 层, 三个 PVE 节点都挂)
pve-node1/2/3 : /mnt/pve/nfs-vms/aether-share
   ↓ virtiofs passthrough (dirid=aether-share)
heavy-1/2/3   : /opt/aether-volumes/   (KVM guest)
```

**含义**:
- `aether-share` 是 Proxmox cluster-level dir mapping, 所有 PVE 节点映射到相同 NFS 挂载点
- 三个 heavy guest 无论 migrate 到哪个 PVE 节点, 看到的 `/opt/aether-volumes/` 都是同一份 NFS 数据
- 只需在**任一** PVE 节点创建子目录, NFS 语义保证其它节点立即可见

**Spec 原假设的 "NFS" 并非完全错误** — NFS 确实存在于栈里, 只是位于 PVE 宿主层而非 KVM guest 层。Spec 的错误是把 "NFS client 在 guest 里 + host_volume NFS 挂载" 当成实现路径, 而实际上 PVE 已经帮我们做了这一层, guest 看到的是 virtiofs。

## 不确定性与风险

1. **NFS server 单点故障** (取代原 "Proxmox 宿主单点" 描述): 承载 `/mnt/pve/nfs-vms/` 的 NFS server (NAS) 挂了, 三个 PVE 节点同时断开 NFS, 随之三个 heavy guest 的 `/opt/aether-volumes/` 不可用 → aria-runner 产出不可达。
   - **现状**: 这个风险**本来就存在**于 todo-web / kairos 等所有 PVE 托管服务, aria-runner 不新增风险。
   - **PVE 节点故障容忍度**: ✅ 良好 — 单个 PVE 节点挂了, 其它两个节点仍能承载 heavy guest migrate 并读取同一份 NFS 数据。这比初版分析里的 "Proxmox 宿主单点" 更 HA。
   - **处置**: M0 Report 的 "风险与假设" 章节记录 "存储层依赖 NAS 的 NFS 服务健康", 将 NFS HA (如 NFS server HA pair / Ceph 替代) 作为 M1+ 的独立工作项。

2. **并发写一致性**: 三个 heavy 节点的 Nomad alloc 同时写入同一个 virtiofs 路径, locking 语义需要实测 (T2.3 的新职责)。
   - **现状**: virtiofs 底层是宿主文件系统 (ext4 / xfs), POSIX locking 应当成立, 但 virtiofsd 的 daemon 实现有 `writeback` 缓存可能导致 fsync 延迟。
   - **处置**: T2.3 md5 双向校验测试需在三个节点并发写入同名文件验证 last-writer-wins 行为, 并记录结论。

3. **quota 缺失**: 当前 2.0 TiB 共享池无 quota 限制, aria-runner 若产出失控会挤占 todo-web 的数据空间。
   - **处置**: T2.2 smoke 测试完成后, 在 Spec §T6 M0 Report 的 "运维建议" 章节列为 "M1 前必须解决" 的运维事项。优先级不阻塞 M0 交付。

## 对 Spec 任务的具体修正 (Override proposal.md)

下列 **override** 优先于 proposal.md 原文; proposal.md 保持不动作为历史。

### T2.1 — NFS 挂载现状调查 (4.5h → 已完成)

- ✅ **交付物**: [`nfs-status.md`](./nfs-status.md) (文件名保留 "nfs" 作为可搜索的 Spec 关联标记, 内容为 virtiofs 实况)
- ✅ **结论**: 无 NFS, 有 virtiofs, 跨节点一致性自然成立

### T2.2 — Nomad parameterized dispatch 实测 (2h)

**原 Spec**: "写一个最小 parameterized job `aria-nfs-smoke.hcl`"

**Override**:
- **文件名**: `aria-storage-smoke.hcl` (去掉 nfs 字样)
- **前置**: Proxmox 宿主创建 `aether-share/aria-runner/outputs/` 子目录 (手工步骤, 见 §执行指令)
- **前置**: 三个 heavy 节点的 Nomad `client.hcl` 注册 host_volume `aria-runner-outputs`, 路径 `/opt/aether-volumes/aria-runner/outputs`
- **Job 内容**: parameterized dispatch, 容器内写入 `/opt/aria-outputs/smoke-${timestamp}.txt` (UUID 内容), 通过 `volume_mount` 映射到 host_volume
- **交付物**: `aria-storage-smoke.hcl` + `t2.2-dispatch-log.txt` (dispatch 输出 + alloc exec 验证)

### T2.3 — 宿主侧 md5 双向校验 (1h)

**原 Spec**: "以 Nomad agent user (UID 推断自 nomad node status) 执行 md5sum..."

**Override**:
- Nomad agent 为 **root (UID 0)**, UID 推断步骤取消
- **新增**: 容器内 effective UID → 宿主文件 owner 映射验证 (因为容器镜像可能 USER 非 root)
- **新增**: 三节点并发写入同名文件测试 virtiofs POSIX locking (see §不确定性 #2)
- **交付物保持**: `nfs-validation-report.md` → 建议改名 `storage-validation-report.md`

### T2.4 — Nomad meta 64KB 边界测试 (0.5h)

**Override**: 无修改, 与存储方案无关。

### T2 交付物清单 (替代 proposal.md 原清单)

- ✅ `nfs-status.md` (T2.1)
- [ ] `aria-storage-smoke.hcl` (T2.2)
- [ ] `t2.2-dispatch-log.txt` (T2.2)
- [ ] `storage-validation-report.md` (T2.3)
- [ ] `t2.4-meta-boundary.md` (T2.4)
- [x] 本决策记录

### T3.3 — Read-only rootfs + bind mount 共存验证

**原 Spec**: "`docker run --read-only --tmpfs /tmp -v $(pwd)/aria-outputs:/opt/aria-outputs ...`"

**Override**: bind mount 源路径从 `$(pwd)/aria-outputs` 改为 `/opt/aether-volumes/aria-runner/outputs`, 其它验证逻辑不变。

### 不变项

- **T1** Legal 闸门: 不受影响
- **T2.4** meta 边界测试: 不受影响
- **T3.1/T3.2/T3.4/T3.5/T3.6/T3.7**: 不受影响 (除 T3.3 路径修正)
- **T4** Hermes Spike: 已完成, 不受影响
- **T5** AD 收敛: AD3/AD5/AD8 如涉及存储假设需同步 override (见下)

## 对 ADR 的影响 (T5 收敛范围内)

需要在 AD 最终版中同步修正的段落 (由 knowledge-manager 在 T5 收敛时处理):

- **AD3** (Hermes Layer): 如提到 "NFS 作为 runner 产出落地" → 改为 "virtiofs host_volume"
- **AD5** (Nomad Job 架构, 假设存在): 如提到 `nfs-fastpool-aether` → 改为 `aria-runner-outputs`
- **AD8** (运维与观测, 假设存在): 如提到 NFS server 监控 → 改为 Proxmox virtiofs daemon 监控

T5.2 (已完成) 的 AD 撰写草案需要 grep 一遍 "nfs|NFS|fastpool" 做批量替换, 列入 T5.5 "AD 最终评审" (若尚未存在则新增) 的 checklist。

## 工时影响

| 任务 | proposal.md 原估 | override 预估 | 差 |
|------|-----------------|--------------|-----|
| T2.1 | 1h | 1h (已花) | 0 |
| T2.2 | 2h | 1.5h (NFS 配置跳过) | -0.5h |
| T2.3 | 1h | 1h (改变 focus 不改变总时长) | 0 |
| T2.4 | 0.5h | 0.5h | 0 |
| **T2 小计** | **4.5h** | **4h** | **-0.5h** |
| T3.3 | 1.5h | 1.5h (路径改一字, 验证逻辑不变) | 0 |

净收益: -0.5h, 落入 T2 原本的缓冲内, 无需调整 M0 整体工时。

## 执行指令 — 给人类操作者 (@simonfishgit)

### 步骤 1: 在 Proxmox 宿主创建 aria-runner 子目录

先定位 `aether-share` 的源路径。登录承载三个 heavy KVM guest 的 Proxmox 宿主 (很可能是单台, 根据 `df -hT /opt/aether-volumes` 显示的 2.0 TiB 容量可大致锁定), 然后:

```bash
# 1. 找到 aether-share 的 source 路径 (Proxmox VM 配置)
#    在 Proxmox 宿主上检查任一 heavy guest 的配置文件:
cat /etc/pve/qemu-server/<VMID>.conf | grep -i virtiofs
# 或
cat /etc/pve/qemu-server/<VMID>.conf | grep -iE 'virtfs|virtio-fs|fs0'
# 预期输出形如: virtiofs0: aether-share,mount_tag=aether-share,directory=/path/to/aether-share

# 2. 进入源路径
cd /path/to/aether-share   # 用上一步找到的实际路径替换

# 3. 创建子目录树
mkdir -p aria-runner/outputs
mkdir -p aria-runner/failed-samples   # T3.4 GLM smoke 归档需要
mkdir -p aria-runner/m0-handoff       # T3.6 image_sha256 归档需要

# 4. 设置权限 (0777 以匹配 /opt/aether-volumes/ 根目录现状)
chmod 0777 aria-runner aria-runner/outputs aria-runner/failed-samples aria-runner/m0-handoff

# 5. 写一个 marker 文件, 便于下一步跨节点验证
echo "created=$(date -Iseconds) by=simonfishgit for=aria-runner-m0" > aria-runner/README
```

### 步骤 2: 验证三个 heavy guest 可见 (在 dev 机器上执行, 无需 Proxmox 宿主权限)

```bash
for ip in 192.168.69.80 192.168.69.81 192.168.69.82; do
  echo "=== $ip ==="
  ssh root@$ip 'ls -la /opt/aether-volumes/aria-runner/ && cat /opt/aether-volumes/aria-runner/README'
done
```

**预期**: 三个节点都能看到 `aria-runner/` 目录, 内容相同 (mtime + README 内容相同)。

**失败分诊**:
- 只有部分节点可见 → virtiofs 挂载不一致, 可能需要重启对应 guest 的 virtiofs daemon (Proxmox 侧)
- 全部不可见 → Proxmox 宿主上的 source 路径找错了, 回到步骤 1 重新定位

### 步骤 3: 通知我继续 T2.2

只需告诉我: "done" 或贴一下验证输出。后续的 Nomad host_volume 注册和 smoke job 我来写, 需要你点一下 aether-volume create 的 confirm 即可。

---

## 审计 / 追溯

- **原 Spec 作者假设来源**: 未知 (Spec 在 2026-04-11 agent-project-adapter 的后续 brainstorm 中引入, 可能继承自 Aether PRD 中的 "计划中的 NFS fastpool"、但该计划已被 virtiofs 方案取代)。
- **发现时间**: 2026-04-15 state-scanner → T2.1 执行中
- **人类决策**: A 路径 (最小侵入 override, 不改 proposal.md)
- **不触发 post_spec 审计**: 修正方向单一、边界清晰、现有生产方案已验证, 无需多轮收敛

## Related

- Parent Spec: [`proposal.md`](../../proposal.md) §T2 §T3.3
- Evidence: [`nfs-status.md`](./nfs-status.md)
- Raw probes: [`raw/heavy-80-probe.txt`](./raw/heavy-80-probe.txt), [`raw/heavy-81-probe.txt`](./raw/heavy-81-probe.txt), [`raw/heavy-82-probe.txt`](./raw/heavy-82-probe.txt)
- Future work: M1+ "Proxmox 宿主 HA + virtiofs quota" (尚未立 Spec, 列入 M0 Report 的运维建议)
