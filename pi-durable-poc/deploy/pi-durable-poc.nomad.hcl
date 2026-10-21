# pi-durable PoC — cost-sentinel 用 Pi Durable 重写的耐久执行试点 (Aria #232 follow-up)。
#
# 设计要点 (评估结论见 pi-durable-poc/README.md):
#   - 单 task 单 owner: pi-durable "One process owns a storage at a time; there is
#     no cross-process locking" → pin 到单节点, count=1。storage 落容器本地盘
#     (= heavy 节点本地 SSD; docker data-root 不在 NFS 上, Aether #67)。
#   - restart mode=delay: 默认 mode=fail 在宿主重启后永久停摆 (Aether 已知陷阱)。
#   - 镜像 digest 钉死 (immutable); LATEST-BUILD-SHA 是占位, build 后替换。
#   - registry pull 走 nomadVar (48/48 job-level auth 模式), 读 aria-orchestrator
#     的 registry-scope token — 与 aria-layer1-* 相同来源, 不新造凭据。
#
# Deploy: nomad job run pi-durable-poc/deploy/pi-durable-poc.nomad.hcl
# Stop:   nomad job stop -purge pi-durable-poc

job "pi-durable-poc" {
  type        = "service"
  datacenters = ["dc1"]

  # 单 owner storage 模型: pin 死单节点 (reschedule = 状态丢失, PoC 接受此边界)
  constraint {
    attribute = "${node.unique.name}"
    value     = "heavy-2"
  }

  group "poc" {
    count = 1

    restart {
      attempts = 4
      interval = "10m"
      delay    = "5s"
      mode     = "delay" # NOT fail — fail 在节点重启后永久停摆
    }

    task "sentinel" {
      driver = "docker"

      config {
        image = "forgejo.10cg.pub/10cg/pi-durable-poc@sha256:LATEST-BUILD-SHA"
        auth {
          username = "${docker_auth_user}"
          password = "${docker_auth_password}"
        }
      }

      env {
        POC_INTERVAL_MS = "45000"
        CHUNK_MS        = "3000"
        POC_CHUNKS      = "3"
        DATA_DIR        = "/data"
        TZ              = "UTC"
      }

      # Registry pull credentials — 与 aria-layer1-* 同源 (nomad/jobs/aria-orchestrator
      # 的 registry-scope token; do NOT use FORGEJO_BOT_PAT)。
      template {
        destination = "secrets/registry-auth.env"
        perms       = "0600"
        env         = true
        change_mode = "noop"
        data        = <<EOH
{{- with nomadVar "nomad/jobs/aria-orchestrator" }}
docker_auth_user={{ .docker_auth_user }}
docker_auth_password={{ .docker_auth_password }}
{{- end }}
EOH
      }

      resources {
        cpu    = 200
        memory = 256
      }
    }
  }
}
