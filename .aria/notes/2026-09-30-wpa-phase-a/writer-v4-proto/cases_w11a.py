B = "Bash"
BLOCK = [
    "ps aux", "ps -ef", "ps auxww", "ps -eo pid,args", "ps e", "ps -aux", "ps -ax", "ps -x", "ps -ux", "ps -au", "ps -axu", "ps -auxww",
    "ps -w -x", "ps -eO rss", "ps -O rss", "ps -eu", "ps -u", "ps 123", "ps -ex", "ps -xw",
    "pgrep -af curl", "pgrep --list-full curl", "pstree -ap", "top -b -n1 -c",
    "/bin/ps aux", "/usr/bin/ps -ef", "/usr/bin/pgrep -af curl", "/usr/bin/pstree -ap", "/usr/bin/top -b -n1 -c",
    "sudo ps aux", "doas ps aux", "nice ps aux", "timeout 5 ps aux", "timeout 5s ps aux", "nohup ps aux", "stdbuf -oL ps aux", "env ps aux",
    "time ps aux", "setsid ps aux", "ionice ps aux", "watch ps aux", "command ps aux", "exec ps aux", "xargs ps -fp", "eval ps aux", "unbuffer ps aux",
    "sudo -u forgejo ps -ef", "sudo -u svc -g grp ps aux", "doas -u root ps aux", "timeout -s KILL 5 ps aux", "nice -n 5 ps aux",
    "ionice -c 2 -n 7 ps aux", "env -i LANG=C ps aux", "env LANG=C ps aux", "xargs -r ps -o pid,args -p", "pgrep -f curl | xargs ps -fp",
    "pgrep -f curl | xargs -r ps -o pid,args -p", "pgrep -f x | xargs -I{} ps -fp {}", "/usr/bin/sudo ps aux", "sudo /bin/ps aux",
    "if true; then ps aux; fi", "for i in 1 2; do ps aux; done", "while true; do ps aux; sleep 5; done", "if false; then true; else ps aux; fi",
    "if false; then true; elif true; then ps aux; fi", "for i in 1 2; do pgrep -af x; done",
    "ssh host 'ps aux'", "ssh host ps aux", "ssh host /bin/ps aux", "docker exec c ps aux", "docker compose exec web ps aux", "podman exec c ps -ef",
    "kubectl exec pod -- ps aux", "lxc exec c -- ps aux", "nomad alloc exec abc ps aux", "pct exec 101 -- ps aux", "sh -c 'ps aux'", "bash -c \"ps -ef\"", "watch 'ps aux'",
    "docker top abc", "docker ps --no-trunc", "podman top abc", "podman ps --no-trunc",
    "ps aux | grep curl", "ps -aux | grep curl",
    "cat /proc/123/environ", "cat /proc/self/cmdline", "head -c 400 /proc/123/environ", "xargs -0 -a /proc/123/environ echo", "cat /proc/*/cmdline",
    "cat /proc/$pid/cmdline", "cat /proc/${pid}/cmdline", "cat /proc/$(pgrep x)/cmdline", "cat /proc/1/task/1/environ",
    "python3 -c \"print(open('/proc/1/environ').read())\"", "node -e \"console.log(require('fs').readFileSync('/proc/1/environ','utf8'))\"",
    "python3 -c \"print(open('/proc/self/cmdline').read())\"",
]
ALLOW = [
    "ps -e", "ps -eo pid,comm", "ps -p 123", "ps -o pid,stat,comm -p 123", "ps -u dev -o pid,comm", "ps -U dev", "ps -A", "ps -C curl", "ps -t pts/0",
    "ps -ejH", "ps -ely", "ps -aux | wc -l", "for i in 1; do ps -eo pid,comm; done", "pgrep -f curl | xargs ps -o pid,comm -p",
    "pgrep curl", "pgrep -f curl", "pgrep -l curl", "pstree -p", "top -b -n1", "docker ps", "docker ps -a", "ps --forest -eo pid,comm",
    "cat /proc/N/cmdline", "cat /proc/<pid>/cmdline", "grep -a x /proc/<pid>/environ", "cat /proc/123/comm", "cat /proc/cpuinfo",
    "grep VmRSS /proc/123/status", "echo 'use ps aux to list'", "grep -rn 'ps aux' docs/", "man ps",
    "sudo -u svc ls", "timeout 5 ls", "docker exec c ps", "kubectl exec pod -- ps", "sudo nice ps aux", "pgrep -fl curl",
    "ps -U dev -u dev u", "ps -e o pid,args", "find /proc -maxdepth 2 -name environ -exec cat {} +",
]
CASES = [(B, c, 2) for c in BLOCK] + [(B, c, 0) for c in ALLOW]
