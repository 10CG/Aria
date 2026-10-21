# manifest.py -- freeze the real-traffic corpus by hash, no command text: TRAFFIC_DIR/cmds/<n>.txt -> stdout TSV "n<TAB>bytes<TAB>sha256"
# The corpus itself never enters the repo; a later session re-extracts with the extract.py of 2026-10-20-secret-guard-scan-cost-and-firstpass-cap/traffic
# into a fresh TRAFFIC_DIR and runs refreeze.py to map those files back onto these n by hash -- new transcripts shift the numbering of extract.py
import hashlib, os, pathlib, sys
d = pathlib.Path(os.getenv("TRAFFIC_DIR", "/tmp/r1traffic")) / "cmds"
rows = []
for p in d.glob("*.txt"):
    b = p.read_bytes()
    rows.append((int(p.stem), len(b), hashlib.sha256(b).hexdigest()))
for n, ln, h in sorted(rows):
    sys.stdout.write(f"{n}\t{ln}\t{h}\n")
