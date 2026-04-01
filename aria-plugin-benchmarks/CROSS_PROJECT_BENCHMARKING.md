# Cross-Project Benchmarking Guide

> **Version**: 1.0.0 | **Status**: Active | **Date**: 2026-04-01

How to evaluate Aria Skills in your own project using the AB benchmark framework.

---

## Overview

The Aria benchmark framework measures whether a Skill improves AI agent quality by comparing `with_skill` vs `without_skill` execution on the same task. This guide extends the framework to non-Aria projects.

**You don't need to modify the benchmark framework itself.** You create project-specific eval cases that run through the same `/skill-creator benchmark` pipeline.

---

## Quick Start (5 minutes)

### 1. Create your eval directory

```
aria-plugin-benchmarks/
└── external/
    └── your-project/
        └── evals/
            └── evals.json
```

### 2. Write eval cases for your project context

```json
{
  "skill_name": "commit-msg-generator",
  "project": "your-project",
  "project_context": {
    "tech_stack": "Python/Django",
    "description": "E-commerce REST API"
  },
  "evals": [
    {
      "id": 1,
      "name": "django-model-migration",
      "prompt": "I added a new Product model to shop/models.py with fields: name, price, category (FK to Category), and created the migration. shop/views.py was updated to add a ProductListView. Generate a commit message for these staged changes.",
      "expectations": [
        "Commit type should be 'feat' for new model addition",
        "Scope should reference 'shop' or 'product' module",
        "Subject should mention the model or its purpose, not just 'changes'"
      ]
    }
  ]
}
```

### 3. Run the benchmark

```
/skill-creator benchmark commit-msg-generator
```

Point it at your eval file when prompted, or copy it into the standard location.

---

## Which Skills to Benchmark First

Not all Skills benefit equally from cross-project testing. Prioritize by portability:

### High Portability (test these first)

| Skill | Why it matters | What to test |
|-------|---------------|-------------|
| `commit-msg-generator` | Every project has commits | Your actual file types and change patterns |
| `state-scanner` | Every project has Git state | Detection accuracy with your project structure |
| `tdd-enforcer` | Any project with tests | Your test framework (pytest, jest, go test, etc.) |
| `brainstorm` | Any feature discussion | Your domain-specific terminology and constraints |
| `spec-drafter` | Any structured planning | Your requirements style and complexity |

### Medium Portability (test after basics)

| Skill | Adaptation needed |
|-------|------------------|
| `arch-search` | Needs architecture docs in your project |
| `arch-update` | Needs your project's doc structure |
| `task-planner` | Works with any OpenSpec, but task patterns vary |

### Low Portability (Aria-specific)

| Skill | Why |
|-------|-----|
| `forgejo-sync` | Aria's Forgejo integration |
| `requirements-sync` | Aria's UPM format |
| `phase-*` | Ten-Step Cycle orchestration |
| `openspec-archive` | Aria's archive structure |

---

## Writing Good Cross-Project Eval Cases

### Principle: Test the Skill's value in YOUR context

The eval case should represent a **real task from your project**, not a generic scenario.

### Template

```json
{
  "skill_name": "<skill-to-test>",
  "project": "<your-project-name>",
  "project_context": {
    "tech_stack": "<language/framework>",
    "description": "<one-line project description>",
    "conventions": "<any project-specific conventions that matter>"
  },
  "evals": [
    {
      "id": 1,
      "name": "<descriptive-kebab-case-name>",
      "prompt": "<50+ chars, real scenario from your project with specific filenames, modules, and context>",
      "expected_output": "<what good output looks like>",
      "expectations": [
        "<assertion that tests Skill's unique value, not generic ability>",
        "<something without_skill would likely get wrong>"
      ]
    }
  ]
}
```

### Good vs Bad Eval Cases

| Good (tests Skill value) | Bad (tests generic ability) |
|--------------------------|---------------------------|
| "Commit type correctly identifies 'fix' for the bug in auth module" | "Output contains text" |
| "Brainstorm asks about Django-specific constraints before proposing solution" | "Output has questions" |
| "State scanner detects pytest test files alongside source changes" | "Scanner runs without error" |

### Expectations that discriminate

The key test: **would vanilla Claude (without the Skill) also pass this expectation?** If yes, it's not testing the Skill's value.

```
Bad:  "Output is formatted as markdown"  (Claude always does this)
Good: "Commit follows <type>(<scope>): <subject> format with imperative mood"

Bad:  "Mentions the changed files"  (Claude can read git diff)
Good: "Groups changes by logical unit, not by file"
```

---

## Running Cross-Project Benchmarks

### Option A: In the Aria repo (recommended for first test)

```bash
# Create your eval file
mkdir -p aria-plugin-benchmarks/external/my-project/evals
# Write evals.json (see template above)

# Run
/skill-creator benchmark <skill-name>
# Point to your eval file when prompted
```

### Option B: In your own project

```bash
# Install aria-plugin
/plugin install aria@10CG-aria-plugin

# Create eval directory in your project
mkdir -p .aria/benchmarks/evals
# Write evals.json

# Run via /skill-creator
/skill-creator benchmark <skill-name>
```

### Interpreting Results

Same verdict standards as Aria internal benchmarks:

| Verdict | Meaning for your project |
|---------|------------------------|
| **WITH_BETTER** (delta > 0, >70% win) | Skill adds value in your context |
| **MIXED** (40-70%) | Skill helps on some tasks but not others |
| **EQUAL** (delta ~0) | Skill doesn't add value for this task type — consider not using it |
| **WITHOUT_BETTER** | Skill hurts quality — check if your context conflicts with Skill assumptions |

---

## Reporting Results

After running benchmarks, share your findings via the [Adoption Report](https://github.com/10CG/aria-plugin/issues/new?template=adoption-report.yml) Issue Template. Include:

- Which Skills you tested
- Your project's tech stack
- Delta scores for each Skill
- Any adaptations you needed to make

This data helps us understand which Skills are truly portable and which need improvement.

---

## Example: Django REST API Project

```json
{
  "skill_name": "commit-msg-generator",
  "project": "shopify-clone",
  "project_context": {
    "tech_stack": "Python 3.12 / Django 5.0 / DRF",
    "description": "E-commerce platform with product catalog, cart, and checkout"
  },
  "evals": [
    {
      "id": 1,
      "name": "django-model-feat",
      "prompt": "Added a new ReviewModel to products/models.py (rating IntegerField, comment TextField, user FK, product FK, created_at). Created migration 0015_review.py. Updated products/serializers.py to add ReviewSerializer. Added ReviewViewSet to products/views.py with list/create actions. Updated products/urls.py with router registration. Generate a commit message.",
      "expectations": [
        "Type must be 'feat' (new feature, not fix/refactor)",
        "Scope should reference 'products' or 'reviews'",
        "Subject should mention review functionality, not list individual files"
      ]
    },
    {
      "id": 2,
      "name": "django-bugfix",
      "prompt": "Fixed a bug in cart/views.py where CartViewSet.update() was not checking if the product was in stock before updating quantity. Added a stock check that returns 400 if requested quantity exceeds available_stock. Also added a test in cart/tests/test_views.py for this edge case. Generate a commit message.",
      "expectations": [
        "Type must be 'fix' (bug fix)",
        "Scope should reference 'cart'",
        "Subject should describe the bug (stock check), not just 'fix bug'"
      ]
    }
  ]
}
```

---

## Directory Convention

```
aria-plugin-benchmarks/
├── external/                        # Cross-project benchmarks
│   ├── README.md                    # This section as quick reference
│   └── <project-name>/
│       ├── evals/
│       │   └── evals.json           # Project-specific eval cases
│       ├── iteration-1/
│       │   └── benchmark.json       # Results
│       └── context.md               # Project description (optional)
├── ab-suite/                        # Aria internal (existing)
└── ab-results/                      # Aria internal (existing)
```

---

**Related**:
- [AB_TEST_OPERATIONS.md](AB_TEST_OPERATIONS.md) — Full benchmark operations manual
- [Adoption Report Template](https://github.com/10CG/aria-plugin/issues/new?template=adoption-report.yml) — Share your results
