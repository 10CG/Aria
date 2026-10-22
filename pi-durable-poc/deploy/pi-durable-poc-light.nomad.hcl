# pi-durable PoC-L — 轻节点可行性 (exec driver, 零 Docker)。
#
# 与 heavy 版 (pi-durable-poc.nomad.hcl) 的差异:
#   - driver = "exec" (chroot + cgroup, 无容器层) — 回应「docker 太重」的原始担忧
#   - 运行时: 官方 Node 22.23.3 linux-x64 tarball 经 artifact 解到 alloc (自包含,
#     依赖宿主 glibc; 无 Python vendor 式版本断裂面)
#   - 依赖: npm ci (91 包, 无 photon) 打的 bundle, 同走 artifact
#   - 存储: NOMAD_ALLOC_DIR/data, 同 heavy 版 (锐边 6 教训)
#
# PoC 边界 (诚实): artifact 走本机 aether-dist http.server (light-4 永久 systemd
# unit /etc/systemd/system/aether-dist.service, enabled — 2026-10-22 收编, 重启存活;
# 内容仍手工 scp staging; 这版 Nomad getter 不支持 file://) —
# 生产化候选是 Forgejo generic packages + artifact header 带 package-read token,
# 见 README「PoC-L 局限」。
#
# Deploy: nomad job run pi-durable-poc/deploy/pi-durable-poc-light.nomad.hcl
# Stop:   nomad job stop -purge pi-durable-poc-light

job "pi-durable-poc-light" {
  type        = "service"
  datacenters = ["dc1"]

  # 单 owner storage 模型同 heavy 版: pin 单节点 (light-4 为当前最空: 935MB 可用, 零 alloc)
  constraint {
    attribute = "${node.unique.name}"
    value     = "light-4"
  }

  group "poc" {
    count = 1

    restart {
      attempts = 4
      interval = "10m"
      delay    = "5s"
      mode     = "delay"
    }

    task "sentinel" {
      driver = "exec"

      artifact {
        source      = "http://127.0.0.1:8000/node-22.23.3.tar.xz"
        destination = "local/node"
      }

      artifact {
        source      = "http://127.0.0.1:8000/pi-durable-bundle.tgz"
        destination = "local/app"
      }

      config {
        command = "local/node/node-v22.23.3-linux-x64/bin/node"
        args    = ["local/app/src/sentinel.mjs"]
      }

      env {
        POC_INTERVAL_MS = "45000"
        CHUNK_MS        = "3000"
        POC_CHUNKS      = "3"
        DATA_DIR        = "${NOMAD_ALLOC_DIR}/data"
        TZ              = "UTC"
      }

      resources {
        cpu    = 100
        memory = 150
      }
    }
  }
}
