"""
Style Manager - 文风一致性系统

解决"文笔风格不一致"的问题
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json


class ToneStyle(Enum):
    """基调风格"""
    STERN = "严肃"           # 严谨、正式
    HUMOR = "幽默"           # 轻松、诙谐
    ROMANTIC = "浪漫"        # 抒情、感性
    REALISTIC = "写实"       # 平实、接地气
    EPIC = "史诗"            # 宏大、壮阔
    MYSTERIOUS = "神秘"      # 悬疑、奇幻


class NarrativeStyle(Enum):
    """叙事风格"""
    FIRST_PERSON = "第一人称"
    THIRD_PERSON = "第三人称"
    OMNISCIENT = "全知视角"


@dataclass
class StyleProfile:
    """
    文风档案 - 定义写作的各种风格参数
    
    使用方法：
    1. 手动定义（用这个类）
    2. 从参考文本学习（自动提取）
    """
    # 基础信息
    name: str = "默认文风"
    description: str = ""
    
    # 句式特征
    sentence_length_avg: float = 20.0      # 平均句长（词数）
    sentence_length_variance: float = 5.0  # 句长变化幅度
    short_sentence_ratio: float = 0.3      # 短句比例
    long_sentence_ratio: float = 0.2       # 长句比例
    
    # 修辞偏好
    use_metaphor: bool = True               # 使用比喻
    use_simile: bool = True                 # 使用拟人
    use_hyperbole: bool = False             # 使用夸张
    use_allusion: bool = True               # 用典
    
    # 用词特征
    vocabulary_level: float = 7.0           # 1-10 词汇等级（接地气到典雅）
    use_classical: bool = False             # 是否用文言
    use_technical: bool = False             # 是否用专业术语
    
    # 情感倾向
    emotional_tone: float = 5.0             # 1-10 情感强度（平淡到强烈）
    sentiment: float = 5.0                  # 1-10 情感倾向（悲观到乐观）
    
    # 对话风格
    dialogue_to_narration_ratio: float = 0.3  # 对话占比
    dialogue_style: str = "自然流畅"          # 对话风格描述
    
    # 节奏控制
    pacing: float = 5.0                     # 1-10 节奏快慢
    tension_buildup: float = 7.0            # 1-10 紧张感营造
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "sentence_length_avg": self.sentence_length_avg,
            "sentence_length_variance": self.sentence_length_variance,
            "short_sentence_ratio": self.short_sentence_ratio,
            "long_sentence_ratio": self.long_sentence_ratio,
            "use_metaphor": self.use_metaphor,
            "use_simile": self.use_simile,
            "use_hyperbole": self.use_hyperbole,
            "use_allusion": self.use_allusion,
            "vocabulary_level": self.vocabulary_level,
            "use_classical": self.use_classical,
            "use_technical": self.use_technical,
            "emotional_tone": self.emotional_tone,
            "sentiment": self.sentiment,
            "dialogue_to_narration_ratio": self.dialogue_to_narration_ratio,
            "dialogue_style": self.dialogue_style,
            "pacing": self.pacing,
            "tension_buildup": self.tension_buildup
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StyleProfile':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    def generate_prompt(self) -> str:
        """生成风格提示词（用于 LLM）"""
        prompt = f"""
风格要求：
- 平均句长：{self.sentence_length_avg}词
- 短句比例：{int(self.short_sentence_ratio*100)}%
- 词汇等级：{int(self.vocabulary_level)}/10
- 情感强度：{int(self.emotional_tone)}/10
- 节奏：{'快' if self.pacing > 6 else '慢' if self.pacing < 4 else '中等'}
"""
        
        if self.use_metaphor:
            prompt += "- 适当使用比喻\n"
        if self.use_allusion:
            prompt += "- 可以用典\n"
        if self.sentiment > 6:
            prompt += "- 保持积极乐观的基调\n"
        elif self.sentiment < 4:
            prompt += "- 可以有阴郁沉重的氛围\n"
        
        return prompt
    
    def __str__(self) -> str:
        return f"StyleProfile({self.name}, 词汇等级:{self.vocabulary_level}, 情感强度:{self.emotional_tone})"


# 预设文风
class PresetStyles:
    """预设文风模板"""
    
    @staticmethod
    def get_网文风格() -> StyleProfile:
        return StyleProfile(
            name="网文风格",
            description="适合网络小说的快节奏风格",
            sentence_length_avg=15.0,
            sentence_length_variance=8.0,
            short_sentence_ratio=0.4,
            long_sentence_ratio=0.1,
            use_metaphor=True,
            use_simile=True,
            use_hyperbole=True,
            use_allusion=False,
            vocabulary_level=5.0,
            use_classical=False,
            use_technical=False,
            emotional_tone=7.0,
            sentiment=6.0,
            dialogue_to_narration_ratio=0.4,
            dialogue_style="直白有趣",
            pacing=8.0,
            tension_buildup=8.0
        )
    
    @staticmethod
    def get_传统文学() -> StyleProfile:
        return StyleProfile(
            name="传统文学",
            description="经典文学作品的庄重风格",
            sentence_length_avg=25.0,
            sentence_length_variance=10.0,
            short_sentence_ratio=0.2,
            long_sentence_ratio=0.3,
            use_metaphor=True,
            use_simile=True,
            use_hyperbole=False,
            use_allusion=True,
            vocabulary_level=8.0,
            use_classical=True,
            use_technical=False,
            emotional_tone=5.0,
            sentiment=5.0,
            dialogue_to_narration_ratio=0.25,
            dialogue_style="含蓄典雅",
            pacing=5.0,
            tension_buildup=6.0
        )
    
    @staticmethod
    def get_悬疑紧张() -> StyleProfile:
        return StyleProfile(
            name="悬疑紧张",
            description="悬疑小说的紧凑风格",
            sentence_length_avg=18.0,
            sentence_length_variance=12.0,
            short_sentence_ratio=0.35,
            long_sentence_ratio=0.15,
            use_metaphor=True,
            use_simile=False,
            use_hyperbole=False,
            use_allusion=False,
            vocabulary_level=6.0,
            use_classical=False,
            use_technical=True,
            emotional_tone=8.0,
            sentiment=3.0,
            dialogue_to_narration_ratio=0.3,
            dialogue_style="简洁紧张",
            pacing=9.0,
            tension_buildup=10.0
        )


class StyleAnalyzer:
    """
    文风分析器 - 从参考文本学习风格
    
    给几段你喜欢的文字，自动提取风格参数
    """
    
    def __init__(self):
        pass
    
    def analyze(self, reference_texts: List[str]) -> StyleProfile:
        """
        分析参考文本，提取风格特征
        
        简化实现：基于规则的特征提取
        生产环境可以用 NLP 模型
        """
        import re
        
        all_text = " ".join(reference_texts)
        sentences = re.split(r'[。！？\n]', all_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return StyleProfile()
        
        # 1. 计算平均句长
        word_counts = [len(self._split_words(s)) for s in sentences]
        avg_length = sum(word_counts) / len(word_counts)
        
        # 2. 句长分布
        short = sum(1 for c in word_counts if c < 15)
        long = sum(1 for c in word_counts if c > 30)
        short_ratio = short / len(sentences)
        long_ratio = long / len(sentences)
        
        # 3. 词汇等级（简化：检测文言词/生僻字）
        classical_count = sum(1 for s in sentences if any(w in s for w in ["之", "乎", "者也", "乃", "遂"]))
        classical_ratio = classical_count / len(sentences)
        
        # 4. 修辞检测（简化）
        has_metaphor = "如" in all_text or "像" in all_text or "似" in all_text
        has_simile = "仿佛" in all_text or "似乎" in all_text
        
        # 5. 情感倾向（简化：检测情感词）
        positive_words = ["爱", "希望", "幸福", "美好", "温暖", "快乐"]
        negative_words = ["死", "亡", "痛", "悲", "伤", "绝望", "恐惧"]
        pos_count = sum(1 for w in positive_words if w in all_text)
        neg_count = sum(1 for w in negative_words if w in all_text)
        
        sentiment = 5.0 + (pos_count - neg_count) * 0.5
        sentiment = max(1.0, min(10.0, sentiment))
        
        # 构建风格档案
        return StyleProfile(
            name="自定义风格",
            description="从参考文本学习",
            sentence_length_avg=avg_length,
            sentence_length_variance=10.0,
            short_sentence_ratio=short_ratio,
            long_sentence_ratio=long_ratio,
            use_metaphor=has_metaphor,
            use_simile=has_simile,
            use_hyperbole=False,
            use_allusion=classical_ratio > 0.1,
            vocabulary_level=7.0 if classical_ratio > 0.1 else 5.0,
            use_classical=classical_ratio > 0.2,
            use_technical=False,
            emotional_tone=6.0 if pos_count + neg_count > 5 else 4.0,
            sentiment=sentiment,
            dialogue_to_narration_ratio=0.3,
            dialogue_style="自然流畅",
            pacing=6.0,
            tension_buildup=5.0
        )
    
    def _split_words(self, text: str) -> List[str]:
        """简单分词（按字符）"""
        # 实际应该用 jieba 等分词库
        return list(text)


class StyleConsistencyChecker:
    """
    文风一致性检查器
    
    写完一章后，检查是否符合既定风格
    """
    
    def __init__(self, profile: StyleProfile):
        self.profile = profile
    
    def check(self, text: str) -> Dict[str, Any]:
        """
        检查文风一致性
        
        返回检查结果和改进建议
        """
        import re
        
        sentences = re.split(r'[。！？\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {"score": 100, "issues": []}
        
        issues = []
        
        # 1. 句长检查
        word_counts = [len(self._split_words(s)) for s in sentences]
        avg = sum(word_counts) / len(word_counts)
        if abs(avg - self.profile.sentence_length_avg) > 10:
            issues.append(f"平均句长 {avg:.1f} 与风格要求 {self.profile.sentence_length_avg} 偏差较大")
        
        # 2. 对话比例检查
        dialogue_count = text.count('"') // 2 + text.count('"') // 2
        if dialogue_count > 0:
            ratio = dialogue_count / len(sentences)
            if abs(ratio - self.profile.dialogue_to_narration_ratio) > 0.2:
                issues.append(f"对话比例 {ratio:.0%} 与风格要求 {self.profile.dialogue_to_narration_ratio:.0%} 不符")
        
        # 3. 词汇等级检查
        if self.profile.use_classical:
            if not any(w in text for w in ["之", "乎", "者也", "乃", "遂"]):
                issues.append("风格要求使用文言，但文本中未体现")
        
        # 4. 节奏检查（简化：短句比例）
        short_ratio = sum(1 for c in word_counts if c < 15) / len(sentences)
        if self.profile.pacing > 7 and short_ratio < 0.2:
            issues.append("快节奏风格但短句不足，节奏偏慢")
        
        # 计算一致性得分
        base_score = 100
        for issue in issues:
            base_score -= 10
        
        return {
            "score": max(0, base_score),
            "issues": issues,
            "suggestions": self._generate_suggestions(issues)
        }
    
    def _split_words(self, text: str) -> List[str]:
        return list(text)
    
    def _generate_suggestions(self, issues: List[str]) -> List[str]:
        if not issues:
            return ["文风一致，很好！"]
        
        suggestions = []
        for issue in issues:
            if "句长" in issue:
                suggestions.append("尝试调整句子长度，长短交错")
            if "对话" in issue:
                suggestions.append("增加或减少对话，改变叙事节奏")
            if "文言" in issue:
                suggestions.append("可以适当加入文言词汇")
            if "节奏" in issue:
                suggestions.append("增加短句使用，提升节奏感")
        
        return suggestions


def create_style_from_examples(examples: List[str]) -> StyleProfile:
    """便捷函数：从示例文本创建风格"""
    analyzer = StyleAnalyzer()
    return analyzer.analyze(examples)


def get_preset(style_name: str) -> StyleProfile:
    """便捷函数：获取预设风格"""
    presets = {
        "网文": PresetStyles.get_网文风格(),
        "传统文学": PresetStyles.get_传统文学(),
        "悬疑": PresetStyles.get_悬疑紧张(),
    }
    return presets.get(style_name, StyleProfile())