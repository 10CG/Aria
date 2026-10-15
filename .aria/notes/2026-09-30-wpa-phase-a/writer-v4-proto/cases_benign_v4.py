B = "Bash"
CASES = [(B, c) for c in [
    "ps -e | grep nginx", "ps -p 1 -o comm=", "ps -o pid,ppid,comm", "ps -eo pid,comm,etime", "pgrep -x nginx", "pgrep nginx | head", "pgrep -u dev -l", "timeout 5 pgrep nginx",
    "ps -ef --no-headers | wc -l", "ps aux | wc -l", "ps -p $$ -o comm=", "ps -o rss= -p 1", "ps -u dev -o pid,comm", "ps -C nginx -o pid=", "pstree -p", "pstree", "top -b -n1 | head -5",
    "top -b -n 1 -o %MEM | head", "uptime", "watch -n 1 uptime", "sh -c 'echo hi'", 'bash -c "ls /tmp"', "docker exec web ls /app", "docker exec -it web sh", "ssh host uptime", "ssh host 'ls -la /tmp'",
    "nomad alloc exec -task web abc ls /", "pct exec 101 -- ls /root", "kubectl exec pod -- ls /", "sudo systemctl restart nginx", "sudo -u svc ls /srv", "timeout 5s sleep 1", "nohup sleep 100 &",
    "env FOO=1 ./run.sh", "env | wc -l", "printenv HOME", "printenv PATH | tr ':' '\\n'", "echo $$", "kill -0 $$", "cat /proc/cpuinfo", "cat /proc/meminfo", "cat /proc/self/comm", "cat /proc/1/comm",
    "grep VmRSS /proc/self/status | head -1", "ls /proc | head", "ls /proc/$$/fd | wc -l", "readlink /proc/self/exe", "cat /proc/loadavg", "xargs -I{} echo {}", "docker ps", "docker ps -a --format '{{.Names}}'",
    "docker top web | wc -l", "docker compose ps", "docker logs web | tail -5", "journalctl -u nginx -n 5 | wc -l", "git log --oneline | head", "grep -rn 'ps aux' docs/ | wc -l", "echo 'run ps to list'",
    "man ps | head", "which ps", "type ps", "command -v pgrep", "ps --help | head", "pgrep --help | head -3", "ssh -V", "watch --version", "sh --version", "bash --version | head -1", "ssh-keygen -l -f x.pub",
    "python3 -c \"import os; print(os.getpid())\"", "python3 -c \"print(open('/proc/self/comm').read())\"", "python3 -c \"import psutil; print(len(psutil.pids()))\"",
    "awk '{print $1}' /proc/loadavg", "cat /proc/net/dev | head -3", "stat /proc/1", "du -sh /proc/1 2>/dev/null",
]]
