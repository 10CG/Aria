# README 国际化与内容升级

## Level: 2 (Minimal)

## 概述

Aria 主项目已在 GitHub 公开，需要将 README 国际化并修复内容准确性问题，使国际用户能正确理解和安装 Aria。

## 动机

- README 全文中文，GitHub 国际用户无法理解
- Skills 数量、安装命令等多处不准确
- 缺少 LICENSE 文件（死链）
- 缺少 Prerequisites 说明

## 变更内容

### 1. 国际化结构
- 英文 `README.md` 作为默认（重写，非翻译）
- 中文迁移至 `README.zh.md`
- 日文 `README.ja.md` 和韩文 `README.ko.md` 占位
- 所有文件顶部添加语言切换栏

### 2. 内容修复
- 创建 MIT LICENSE 文件
- 安装命令大小写修正（`10CG-aria-plugin`）
- Skills 表格补全（workflow-runner、agent-team-audit）
- 添加 Prerequisites 章节
- 十步循环 ASCII art → Mermaid 图
- 章节顺序优化（Quick Start 提前）
- `.aria/` 配置体系体现

### 3. 不变更
- 不创建 CONTRIBUTING.md（后续迭代）
- 不添加截图/GIF（后续迭代）
- 日文/韩文不翻译（占位等待社区贡献）

## 影响范围

| 文件 | 操作 |
|------|------|
| `README.md` | 重写为英文版 |
| `README.zh.md` | 新建，迁移中文内容 |
| `README.ja.md` | 新建，占位 |
| `README.ko.md` | 新建，占位 |
| `LICENSE` | 新建 |
| `VERSION` | 更新 Skills 数量 |

## 验收标准

- [ ] 英文 README.md 包含完整且准确的项目信息
- [ ] 中文 README.zh.md 内容与英文版结构对齐
- [ ] 所有语言文件顶部有切换栏
- [ ] LICENSE 文件存在且链接有效
- [ ] 安装命令准确可用
- [ ] Skills/Agents 数量与实际一致
