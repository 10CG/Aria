B = "Bash"
CASES = [
    (B, "python3 -c \"print(open('/v1/var/nomad/jobs/x').read())\""),
    (B, "node -e \"console.log(require('fs').readFileSync('/v1/var/nomad/jobs/x','utf8'))\""),
    (B, "cat /v1/var/nomad/jobs/x"),
    (B, "python3 -c \"print(open('/secretsmanager/x').read())\""),
]
