# Cross-Project Benchmark Results

This directory stores benchmark results from projects outside of Aria.

## Structure

```
external/
└── <project-name>/
    ├── evals/evals.json      # Project-specific eval cases
    ├── context.md             # Project description (optional)
    └── iteration-N/
        └── benchmark.json     # AB test results
```

## How to Add Your Project

See [CROSS_PROJECT_BENCHMARKING.md](../CROSS_PROJECT_BENCHMARKING.md) for the full guide.

Quick version:
1. Create `external/<your-project>/evals/evals.json`
2. Run `/skill-creator benchmark <skill-name>`
3. Share results via [Adoption Report](https://github.com/10CG/aria-plugin/issues/new?template=adoption-report.yml)
