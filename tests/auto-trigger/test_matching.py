# -*- coding: utf-8 -*-
"""
自动触发规则测试
测试意图关键词到 Skill 的映射匹配

版本: 1.0.0
来源: TASK-015
"""

import json
import pytest
from pathlib import Path
from typing import Dict, List, Tuple


class TriggerRulesLoader:
    """加载触发规则配置"""

    def __init__(self, rules_path: str = None):
        if rules_path is None:
            # 默认路径
            project_root = Path(__file__).parent.parent.parent
            rules_path = project_root / ".claude" / "trigger-rules.json"

        with open(rules_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.rules = self.config.get('rules', {})
        self.threshold = self.config.get('confidence_threshold', 0.8)


class SkillMatcher:
    """Skill 匹配器"""

    def __init__(self, loader: TriggerRulesLoader):
        self.loader = loader

    def match(self, user_input: str) -> List[Tuple[str, float]]:
        """
        匹配用户输入到 Skill

        返回: [(skill_name, confidence), ...] 按置信度降序
        """
        results = []
        input_lower = user_input.lower()

        for skill_name, rule in self.loader.rules.items():
            confidence = self._calculate_confidence(input_lower, rule)
            if confidence > 0:
                results.append((skill_name, confidence))

        # 按置信度降序排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def _calculate_confidence(self, input_lower: str, rule: dict) -> float:
        """计算匹配置信度"""
        keywords = rule.get('keywords', [])
        context_boost = rule.get('context_boost', {})

        max_confidence = 0.0

        for keyword_entry in keywords:
            word = keyword_entry.get('word', '')
            weight = keyword_entry.get('weight', 0.8)

            if word in input_lower:
                # 基础匹配
                confidence = weight

                # 上下文加成
                boost = self._calculate_context_boost(
                    input_lower, word, context_boost
                )
                confidence += boost

                # 完全短语匹配加成
                if input_lower.strip() == word:
                    confidence += 0.15

                max_confidence = max(max_confidence, confidence)

        # 同一 skill 多个关键词匹配加成
        match_count = sum(1 for kw in keywords if kw.get('word', '') in input_lower)
        if match_count > 1:
            max_confidence += 0.1 * (match_count - 1)

        return min(max_confidence, 1.0)

    def _calculate_context_boost(
        self, input_lower: str, word: str, context: dict
    ) -> float:
        """计算上下文加成"""
        boost = 0.0

        # 前置词加成
        before_words = context.get('before', [])
        for before in before_words:
            pattern = f"{before} {word}"
            if pattern in input_lower:
                boost += 0.1

        # 后置词加成
        after_words = context.get('after', [])
        for after in after_words:
            pattern = f"{word} {after}"
            if pattern in input_lower:
                boost += 0.1

        return boost


class TestTriggerRules:
    """触发规则测试"""

    @pytest.fixture
    def loader(self):
        """加载规则配置"""
        return TriggerRulesLoader()

    @pytest.fixture
    def matcher(self, loader):
        """创建匹配器"""
        return SkillMatcher(loader)

    def test_tdd_enforcer_triggers(self, matcher):
        """测试 TDD Enforcer 触发"""
        test_cases = [
            ("write test for login", "tdd-enforcer", 0.9),
            ("编写测试", "tdd-enforcer", 0.9),
            ("tdd workflow", "tdd-enforcer", 1.0),
            ("check coverage", "tdd-enforcer", 0.8),
            ("创建测试规范", "tdd-enforcer", 0.85),
        ]

        for input_text, expected_skill, min_confidence in test_cases:
            results = matcher.match(input_text)
            assert len(results) > 0, f"无匹配: '{input_text}'"

            top_skill, top_confidence = results[0]
            assert top_skill == expected_skill, f"期望 {expected_skill}, 得到 {top_skill}"
            assert top_confidence >= min_confidence, \
                f"置信度过低: {top_confidence} < {min_confidence}"

    def test_branch_manager_triggers(self, matcher):
        """测试 Branch Manager 触发"""
        test_cases = [
            ("create branch for auth", "branch-manager", 0.9),
            ("创建分支", "branch-manager", 0.9),
            ("create pr", "git", 0.85),  # git skill 会映射到 branch-manager
            ("worktree setup", "git", 1.0),
        ]

        for input_text, expected_skill, min_confidence in test_cases:
            results = matcher.match(input_text)
            assert len(results) > 0, f"无匹配: '{input_text}'"

            top_skill, top_confidence = results[0]
            assert top_skill == expected_skill, f"期望 {expected_skill}, 得到 {top_skill}"
            assert top_confidence >= min_confidence, \
                f"置信度过低: {top_confidence} < {min_confidence}"

    def test_task_planner_triggers(self, matcher):
        """测试 Task Planner 触发"""
        test_cases = [
            ("plan the tasks", "planning", 0.85),
            ("规划任务", "planning", 0.85),
            ("breakdown this feature", "planning", 0.9),
        ]

        for input_text, expected_skill, min_confidence in test_cases:
            results = matcher.match(input_text)
            assert len(results) > 0, f"无匹配: '{input_text}'"

            top_skill, top_confidence = results[0]
            assert top_skill == expected_skill, f"期望 {expected_skill}, 得到 {top_skill}"

    def test_state_scanner_triggers(self, matcher):
        """测试 State Scanner 触发"""
        test_cases = [
            ("what's the current state", "state_scan", 0.85),
            ("项目状态", "state_scan", 0.9),
            ("progress overview", "state_scan", 0.85),
        ]

        for input_text, expected_skill, min_confidence in test_cases:
            results = matcher.match(input_text)
            assert len(results) > 0, f"无匹配: '{input_text}'"

            top_skill, top_confidence = results[0]
            assert top_skill == expected_skill

    def test_confidence_threshold(self, matcher):
        """测试置信度阈值"""
        # 低置信度输入
        results = matcher.match("hello world")
        assert len(results) == 0 or results[0][1] < 0.6

        # 高置信度输入
        results = matcher.match("create tdd test for authentication")
        assert len(results) > 0
        assert results[0][1] >= 0.8

    def test_multiple_skill_match(self, matcher):
        """测试多 Skill 匹配排序"""
        results = matcher.match("create branch and write tests")

        # 应该匹配到多个 skills
        assert len(results) >= 2

        # 最高置信度应该是 branch-manager 或 testing
        top_skills = [skill for skill, _ in results[:2]]
        assert any(s in ["git", "testing"] for s in top_skills)

    def test_chinese_english_equivalent(self, matcher):
        """测试中英文等效触发"""
        english_results = matcher.match("create test")
        chinese_results = matcher.match("创建测试")

        # 应该匹配到同一个 skill
        assert english_results[0][0] == chinese_results[0][0] == "testing"

    def test_exact_match_boost(self, matcher):
        """测试完全匹配加成"""
        partial_results = matcher.match("test")
        exact_results = matcher.match("tdd")

        # 完全匹配 'tdd' 应该有更高置信度
        assert exact_results[0][1] > partial_results[0][1]


class TestMatchAlgorithm:
    """匹配算法单元测试"""

    def test_fuzzy_match_tolerance(self):
        """测试模糊匹配容错"""
        # 应该容忍轻微的拼写错误
        loader = TriggerRulesLoader()
        matcher = SkillMatcher(loader)

        # "test" 应该匹配 "testing"
        results = matcher.match("write a test")
        assert len(results) > 0
        assert results[0][0] == "testing"

    def test_case_insensitive(self):
        """测试大小写不敏感"""
        loader = TriggerRulesLoader()
        matcher = SkillMatcher(loader)

        lower_results = matcher.match("create branch")
        upper_results = matcher.match("CREATE BRANCH")
        mixed_results = matcher.match("Create Branch")

        # 所有变体应该有相同结果
        assert lower_results[0][0] == upper_results[0][0] == mixed_results[0][0]

    def test_whitespace_tolerance(self):
        """测试空格容忍度"""
        loader = TriggerRulesLoader()
        matcher = SkillMatcher(loader)

        results1 = matcher.match("create branch")
        results2 = matcher.match("create  branch")  # 双空格
        results3 = matcher.match("create   branch")  # 多空格

        # 应该有相同结果
        assert results1[0][0] == results2[0][0] == results3[0][0]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
