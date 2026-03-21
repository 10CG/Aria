[English](README.md) | [中文](README.zh.md) | **日本語** | [한국어](README.ko.md)

# Aria

> AIをソフトウェアプロジェクトの真のコラボレーターに

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Plugin Version](https://img.shields.io/badge/Plugin-v1.7.2-blue)](https://github.com/10CG/aria-plugin)

---

> **翻訳状況**: このドキュメントは準備中です。完全な情報については [English](README.md) 版をご参照ください。
>
> 翻訳への貢献を歓迎します！Pull Request をお送りください。

---

## Aria とは？

Aria は **AI-DDD（AI支援ドメイン駆動設計）方法論**です。Claude Code のような AI アシスタントが、構造化されたワークフローを通じてソフトウェア開発の全工程に深く参加できるようにします。

従来の「AIがコードを書く」ツールとは異なり、Aria は**AIにプロジェクトの意図を理解させ、価値あるコラボレーターにする方法**に焦点を当てています。

## クイックスタート

### 前提条件

- [Claude Code](https://claude.ai/code) がインストール済みで認証完了
- Git 2.x+（standards サブモジュールを使用する場合）

### インストール

```bash
# マーケットプレイスを追加
/plugin marketplace add 10CG/aria-plugin

# インストール（Skills + Agents を含む）
/plugin install aria@10CG-aria-plugin
```

### 使い方

```bash
# プロジェクト状態をスキャン
/aria:state-scanner

# 要件仕様を作成
/aria:spec-drafter

# 構造化ブレインストーミング
/aria:brainstorm

# 専門エージェントを呼び出す
/aria:tech-lead この機能のアーキテクチャを設計してください
```

---

詳細については [English](README.md) 版をご覧ください。

## ライセンス

MIT License — [LICENSE](LICENSE) を参照

## お問い合わせ

- **リポジトリ**: https://github.com/10CG/Aria
- **プラグイン**: https://github.com/10CG/aria-plugin
- **メール**: help@10cg.pub
- **メンテナー**: 10CG Lab
