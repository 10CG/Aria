# aria-storage-smoke — T2.2 parameterized dispatch smoke test
#
# 目的: 验证 A3 假设 — Aether heavy 节点容器可通过 bind mount 写入 virtiofs+NFS
#       共享存储, 产物跨容器生命周期持久, 且在宿主侧可读。
#
# 方案: W (探针零侵入) — 用 Nomad docker driver 的 config.volumes 而非
#       host_volume, 完全不修改 Nomad client.hcl, 探针结束集群 100% 回基线。
#
# 决策记录: ../decision-r8-virtiofs-vs-nfs.md
# 前置条件:
#   - /opt/aether-volumes/aria-runner/outputs/ 存在于三个 heavy 节点 (虚拟文件系统层)
#   - driver.docker.volumes.enabled = true (已验证)
#
# 预期产出: /opt/aether-volumes/aria-runner/outputs/smoke-<smoke_id>.txt
#           内容含 UUID + container hostname + 宿主节点名 + timestamp

job "aria-storage-smoke" {
  type        = "batch"
  datacenters = ["dc1"]

  parameterized {
    payload       = "forbidden"
    meta_required = ["smoke_id"]
    meta_optional = ["target_node"]
  }

  # 只允许派发到 heavy 节点 (light 节点无 docker driver)
  constraint {
    attribute = "${node.class}"
    value     = "heavy_workload"
  }

  group "smoke" {
    count = 1

    restart {
      attempts = 0
      mode     = "fail"
    }

    reschedule {
      attempts = 0
      unlimited = false
    }

    task "write-uuid" {
      driver = "docker"

      config {
        image   = "alpine:3.19"
        command = "sh"
        args = [
          "-c",
          <<-EOT
            set -eu
            # 容器内的 UUID 写入点 (通过 bind mount 落到宿主 virtiofs)
            OUT="/opt/aria-outputs/smoke-${NOMAD_META_smoke_id}.txt"

            # 生成证据
            UUID="$(cat /proc/sys/kernel/random/uuid)"
            TS="$(date -Iseconds)"
            CHOSTNAME="$(hostname)"
            CUID="$(id -u)"
            CGID="$(id -g)"

            echo "smoke_id=${NOMAD_META_smoke_id}"           >  "$OUT"
            echo "uuid=$UUID"                                 >> "$OUT"
            echo "container_hostname=$CHOSTNAME"              >> "$OUT"
            echo "container_uid=$CUID"                        >> "$OUT"
            echo "container_gid=$CGID"                        >> "$OUT"
            # target_node meta 仅作为 dispatch 标签, 不写入产物 (避免 Nomad 二阶段插值卡壳)
            echo "ts=$TS"                                     >> "$OUT"
            echo "nomad_alloc_id=${NOMAD_ALLOC_ID}"            >> "$OUT"
            echo "nomad_node_name=${node.unique.name}"        >> "$OUT"

            # 回显给 stdout (Nomad logs 可见)
            echo "--- wrote $OUT ---"
            cat "$OUT"

            # md5 自验 — 为 T2.3 做铺垫
            MD5="$(md5sum "$OUT" | awk '{print $1}')"
            echo "md5_in_container=$MD5"
          EOT
        ]

        # W 方案核心: 宿主路径 bind mount, 不走 Nomad host_volume
        volumes = [
          "/opt/aether-volumes/aria-runner/outputs:/opt/aria-outputs"
        ]

        # 安全约束 (对齐 T3.3 要求)
        readonly_rootfs = false  # T2.2 不测 read-only, T3.3 才测
        network_mode    = "none" # 无需网络, 纯本地 I/O
      }

      resources {
        cpu    = 100  # MHz
        memory = 64   # MB
      }

      logs {
        max_files     = 2
        max_file_size = 1
      }
    }
  }

  meta {
    owner         = "aria-m0-prerequisite"
    purpose       = "A3-assumption-smoke"
    ephemeral     = "true"
    stop_after    = "T2.2-validation"
    decision_ref  = "openspec/changes/aria-2.0-m0-prerequisite/artifacts/t2/decision-r8-virtiofs-vs-nfs.md"
  }
}
