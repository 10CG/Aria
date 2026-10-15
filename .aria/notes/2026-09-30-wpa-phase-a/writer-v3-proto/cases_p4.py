B = "Bash"
CASES = [(B, "cat <<'EOF'\nps aux\nEOF", 2), (B, "sudo -u svc ls", 0), (B, "timeout 5 ls", 0), (B, "ps aux", 2)]
