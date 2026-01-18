# Changelog

All notable changes to the `branch-manager` skill will be documented in this file.

## [1.0.0] - 2025-12-16

### Added

- Initial release of branch-manager skill
- B.1: Branch creation functionality
  - Support for main repository branches
  - Support for submodule branches
  - Multiple branch types (feature, bugfix, hotfix, release, experiment)
  - Module identifiers (backend, mobile, shared, cross, docs, standards)
- C.2: PR creation functionality
  - Integration with Forgejo API
  - PR template with Summary, Changes, Test Plan sections
  - Support for squash, merge, and rebase strategies
  - Branch cleanup after merge
- Submodule workflow documentation
- Error handling and recovery procedures

### Related Documents

- Ten-Step Cycle: Phase B (B.1-B.3), Phase C (C.1-C.2)
- Branch Management Guide
- Forgejo API Guide
