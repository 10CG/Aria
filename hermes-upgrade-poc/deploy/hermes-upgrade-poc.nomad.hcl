# hermes-upgrade-poc — Aria #262 升级评估 PoC cell (P2a/P3/P4/P5)
#
# P5 独立性: 独立 job 名 + 容器内 /root/.hermes (不挂 aria-layer1 卷, 不触
# 现役 0.7 的 hermes-home/state); 凭据只读复用 nomad/jobs/aria-orchestrator var
# 的 LUXENO_API_KEY (model 调用) 与 docker_auth (拉镜像)。
#
# Deploy: nomad job run (digest 钉版后)
# Stop:   nomad job stop -purge hermes-upgrade-poc

job "hermes-upgrade-poc" {
  type        = "service"
  datacenters = ["dc1"]

  constraint {
    attribute = "${node.class}"
    value     = "heavy_workload"
  }

  group "poc" {
    count = 1

    restart {
      attempts = 2
      interval = "10m"
      delay    = "10s"
      mode     = "delay"
    }

    task "poc" {
      driver = "docker"

      config {
        image = "forgejo.10cg.pub/10cg/hermes-upgrade-poc@sha256:8abc82eafeb7fd4476d277cafda4e774a7ac2a252316d5fedc0293daaaf2d8d3"
        auth {
          username = "${docker_auth_user}"
          password = "${docker_auth_password}"
        }
      }

      env {
        # P4: claude -p 走 luxeno 路由 (与现役 orchestrator 同款接线)
        ANTHROPIC_BASE_URL = "https://api.luxeno.ai"
        ANTHROPIC_MODEL    = "glm-4.5-air"
        # P2b v2 差分修正: 镜像生产工作选择器 (v1 缺 allow-all → pairing fail-close 沉默)
        GATEWAY_ALLOW_ALL_USERS = "true"
        FEISHU_DOMAIN           = "feishu"
        TZ                      = "UTC"
      }

      template {
        destination = "secrets/poc.env"
        perms       = "0600"
        env         = true
        change_mode = "noop"
        data        = <<EOH
{{- with nomadVar "nomad/jobs/aria-orchestrator" }}
LUXENO_API_KEY={{ .LUXENO_API_KEY }}
ANTHROPIC_API_KEY={{ .LUXENO_API_KEY }}
docker_auth_user={{ .docker_auth_user }}
docker_auth_password={{ .docker_auth_password }}
{{- end }}
{{- with nomadVar "nomad/jobs/hermes-upgrade-poc" }}
FEISHU_APP_ID={{ .FEISHU_APP_ID }}
FEISHU_APP_SECRET={{ .FEISHU_APP_SECRET }}
{{- end }}
EOH
      }

      resources {
        cpu    = 300
        memory = 512
      }
    }
  }
}
