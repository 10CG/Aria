      awk -F'\t' '
        function srt(a, n,   i, j, x) { for (i = 2; i <= n; i++) { x = a[i]; for (j = i - 1; j > 0 && a[j] > x; j--) a[j + 1] = a[j]; a[j + 1] = x } }
        function q(a, n, pc,   i) { i = int(pc * n); if (i < pc * n) i++; if (i < 1) i = 1; return a[i] }
        function dist(a, n) { if (n == 0) return "n=0"; srt(a, n); return sprintf("n=%d p50=%.3f p90=%.3f max=%.3f", n, q(a, n, .5), q(a, n, .9), a[n]) }
        FNR == 1 { f++ }
        /^#/ { next }
        f == 1 { o[++m] = $1; rc[$1] = $2 + 0; k[$1] = $3; w[$1] = $4; rs[$1] = $6; next }
        f == 2 { bk[$1] = $3; bw[$1] = $4; bc[$3]++; next }
        f == 3 && /^DIFF n=/ { split($0, dv, /[ =]/); d[dv[3]] = 1; next }
        f == 3 && /^identical=/ { idl = $0; next }
        END {
          for (x in bc) bl = bl sprintf(" %s %d", x, bc[x]); printf "  baseline replay outcomes:%s\n", bl
          for (i = 1; i <= m; i++) { x = o[i]
            if (!(x in bw)) { nb = nb " " x; continue }
            e = w[x] - bw[x]
            if (rs[x] == "-") { nr++; if (x in d) nd = nd " " x; else ni++; continue }
            if (rc[x] == 0) { ea[++na] = e; continue }
            if (rc[x] == 2 && k[x] == bk[x] && k[x] ~ /^(oversize|longline|growth|tmax)$/) { ef[++nf] = e
              fl[nf] = sprintf("    n=%-6s W %.3f  base W %.3f  extra %.3f  (%s; ident pass: %s)", x, w[x], bw[x], e, k[x], ((x in d) ? "differs" : "identical")); continue }
            no++; ol = ol sprintf("\n    n=%-6s rc %d %s (baseline %s)  W %.3f  base W %.3f", x, rc[x], k[x], bk[x], w[x], bw[x])
          }
          printf "  entered the rerun, fell back to the size text of the baseline (relax-start, rc 2, the kind of the baseline): %d\n", nf
          for (i = 1; i <= nf; i++) print fl[i]
          printf "    extra (s): %s\n", dist(ef, nf)
          printf "  entered the rerun and allowed: extra (s): %s\n", dist(ea, na)
          printf "  entered the rerun, any other outcome: %d%s\n", no, ol
          printf "  did not enter the rerun: %d; rc + sha256(stderr) identical to the baseline (ident pass): %d of %d%s\n", nr, ni, nr, (nd == "" ? "" : "; differ:" nd)
          printf "  ident pass over the 138: %s%s\n", idl, (nb == "" ? "" : "; not in the baseline replay:" nb)
        }' "$C/95.tsv" "$C/fakebase.tsv" "$C/fakeident.txt"
