# PoC soak 复查提醒 — 一次性 (2026-10-29 10:00 北京 = 02:00 UTC 触发)
#
# Owner 指令 (2026-10-22): "7 天后复查 PoC soak, 到时候提醒我"。
# 会话内 cron 活不过 7 天 → 用 Nomad periodic 一次性触发 + 飞书 webhook 主动提醒;
# 被动层 (memory + handoff §0-2 基线) 已另记。
#
# 镜像复用 CI 产物 aria-layer1 (c3290150, python stdlib — 零新构建);
# webhook 从 nomad/jobs/aria-orchestrator var 注入 (与 cost-sentinel 同源, 不落明文)。
# 触发后 parent job 变 dead 留档; 复查完成时 nomad job stop -purge 清掉。
#
# Deploy: nomad job run pi-durable-poc/deploy/poc-soak-review-reminder.nomad.hcl

job "poc-soak-review-reminder" {
  type        = "batch"
  datacenters = ["dc1"]

  constraint {
    attribute = "${node.class}"
    value     = "heavy_workload"
  }

  periodic {
    crons            = ["0 2 29 10 *"] # 2026-10-29 02:00 UTC = 10:00 北京
    time_zone        = "UTC"
    prohibit_overlap = true
  }

  group "remind" {
    task "notify" {
      driver = "docker"

      config {
        image   = "forgejo.10cg.pub/10cg/aria-layer1@sha256:c3290150e3ef035801e5ee7ff52ca7c33606c047fdcd8fd7a3499c59952dc874"
        command = "python"
        # 签名必带 (bot 开了校验; 首版无 sign → HTTP 200 + body code 19021 静默拒收)。
        # 复用 aria_layer1.feishu_webhook 的已验证签名函数 (05-09 修过 key/msg 装反),
        # 并断言 body code==0 — client.send 只回 HTTP 码不查 body, 不能裸用。
        args    = ["-c", "import os,json,time,urllib.request;from aria_layer1.feishu_webhook import _compute_feishu_signature as sig;ts=str(int(time.time()));t='PoC soak 复查到期 (基线 2026-10-22T16:52Z)\\nPoC-H heavy-2: cycle 1562 / RSS 55.6MiB (+40% 漂移, 主观察项)\\nPoC-L light-4: cycle 1031 / cgroup 61.8MB\\n复查: logs 对照 cycle/漂移 → 决定去留; 详见 handoff 10-22 §0-2';b={'timestamp':ts,'sign':sig(ts,os.environ['ARIA_FEISHU_SIGNING_SECRET']),'msg_type':'text','content':{'text':t}};r=json.loads(urllib.request.urlopen(urllib.request.Request(os.environ['ARIA_FEISHU_WEBHOOK_URL'],data=json.dumps(b).encode(),headers={'Content-Type':'application/json'}),timeout=30).read());assert r.get('code')==0,f'FEISHU-REJECT {r}';print('FEISHU-OK',r.get('msg'))"]

        auth {
          username = "${docker_auth_user}"
          password = "${docker_auth_password}"
        }
      }

      template {
        destination = "secrets/feishu.env"
        perms       = "0600"
        env         = true
        change_mode = "noop"
        data        = <<EOH
{{- with nomadVar "nomad/jobs/aria-orchestrator" }}
ARIA_FEISHU_WEBHOOK_URL={{ .ARIA_FEISHU_WEBHOOK_URL }}
ARIA_FEISHU_SIGNING_SECRET={{ .ARIA_FEISHU_SIGNING_SECRET }}
docker_auth_user={{ .docker_auth_user }}
docker_auth_password={{ .docker_auth_password }}
{{- end }}
EOH
      }

      resources {
        cpu    = 50
        memory = 64
      }
    }
  }
}
