# Tasks: 版本信息规范化

> **Change**: [2026-02-06-version-standardization](./proposal.md)
> **Total Tasks**: 7
> **Estimated**: 2-4h

---

## Phase 1: 修正当前版本

- [ ] **1.1** 更新 `marketplace.json` 版本到 1.3.0
  - 更新 `version` 字段
  - 更新 `plugins[0].version` 字段
  - 更新 `description` 中的 Skills 数量 (24 → 25)

- [ ] **1.2** 更新 `hooks.json` 版本到 1.3.0
  - 更新 `version` 字段
  - 确认描述准确

- [ ] **1.3** 创建 `aria/VERSION` 文件
  - 采用标准格式
  - 包含版本号、发布日期、说明

## Phase 2: 更新文档

- [ ] **2.4** 更新 `aria/README.md` 确保版本一致
  - 验证标题版本号
  - 验证 Skills 数量 (25)

- [ ] **2.5** 在 `CLAUDE.md` 中添加版本更新规范
  - 定义版本号语义约定
  - 提供版本发布检查清单
  - 说明各文件的同步关系

## Phase 3: 归档

- [ ] **3.6** 更新 `aria/CHANGELOG.md` 记录本次规范化
  - 添加 v1.3.0 条目 (如果还没有)
  - 记录版本规范化的变更

- [ ] **3.7** 提交并打标签
  - 提交子模块变更
  - 更新主仓库子模块指针
  - 创建 git tag v1.3.0
