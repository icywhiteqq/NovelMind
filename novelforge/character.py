"""
Character Module - 每个角色都是有灵魂的 AI Agent

SOUL 系统：
- S: Situation (处境/背景)
- O: Objectives (目标/追求)  
- U: Uniqueness (独特性/性格)
- L: Legacy (秘密/伏笔)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid


@dataclass
class Soul:
    """
    角色的灵魂 - 定义角色的核心特征
    
    每个角色不只是一个名字，而是有血有肉的人。
    """
    # Situation - 背景处境
    background: str = ""           # 角色背景故事
    origin: str = ""               # 出身
    current_situation: str = ""    # 当前处境
    
    # Objectives - 目标追求
    goals: List[str] = field(default_factory=list)      # 短期目标
    long_term_goals: List[str] = field(default_factory=list)  # 长期目标
    fears: List[str] = field(default_factory=list)      # 恐惧/害怕失去的
    
    # Uniqueness - 独特性
    personality: str = ""          # 性格描述
    strengths: List[str] = field(default_factory=list)  # 长处
    weaknesses: List[str] = field(default_factory=list) # 弱点
    speech_style: str = ""         # 说话风格
    habits: List[str] = field(default_factory=list)     # 习惯/小动作
    
    # Legacy - 秘密/伏笔
    secrets: List[str] = field(default_factory=list)    # 隐藏的秘密
    hidden_past: str = ""          # 不为人知的过去
    connections: Dict[str, str] = field(default_factory=dict)  # 与其他角色的隐藏关联
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "background": self.background,
            "origin": self.origin,
            "current_situation": self.current_situation,
            "goals": self.goals,
            "long_term_goals": self.long_term_goals,
            "fears": self.fears,
            "personality": self.personality,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "speech_style": self.speech_style,
            "habits": self.habits,
            "secrets": self.secrets,
            "hidden_past": self.hidden_past,
            "connections": self.connections
        }
    
    def __str__(self) -> str:
        return f"""
=== {self.background[:50]}... ===
目标: {', '.join(self.goals[:2])}
性格: {self.personality[:50]}...
秘密: {', '.join(self.secrets[:2])}
"""


@dataclass
class CharacterMemory:
    """角色记忆片段"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    chapter: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    importance: float = 1.0  # 1-10 重要程度
    tags: List[str] = field(default_factory=list)
    emotional_impact: float = 0.0  # 情感冲击 -5 到 +5
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "chapter": self.chapter,
            "timestamp": self.timestamp.isoformat(),
            "importance": self.importance,
            "tags": self.tags,
            "emotional_impact": self.emotional_impact
        }


class Character:
    """
    角色类 - 包含角色的灵魂和记忆
    """
    
    def __init__(
        self,
        name: str,
        role: str = "配角",  # 主角/配角/反派/龙套
        soul: Optional[Dict[str, Any]] = None,
        description: str = ""
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.description = description
        self.created_at = datetime.utcnow()
        
        # Initialize SOUL
        if soul:
            self.soul = Soul(
                background=soul.get("background", ""),
                origin=soul.get("origin", ""),
                current_situation=soul.get("current_situation", ""),
                goals=soul.get("goals", []),
                long_term_goals=soul.get("long_term_goals", []),
                fears=soul.get("fears", []),
                personality=soul.get("personality", ""),
                strengths=soul.get("strengths", []),
                weaknesses=soul.get("weaknesses", []),
                speech_style=soul.get("speech_style", ""),
                habits=soul.get("habits", []),
                secrets=soul.get("secrets", []),
                hidden_past=soul.get("hidden_past", ""),
                connections=soul.get("connections", {})
            )
        else:
            self.soul = Soul()
        
        # Character's personal memories
        self.memories: List[CharacterMemory] = []
        
        # Current emotional state
        self.emotional_state: float = 0.0  # -5 到 +5
    
    def add_memory(
        self,
        content: str,
        chapter: int,
        importance: float = 5.0,
        tags: List[str] = None,
        emotional_impact: float = 0.0
    ):
        """为角色添加一段记忆"""
        memory = CharacterMemory(
            content=content,
            chapter=chapter,
            importance=importance,
            tags=tags or [],
            emotional_impact=emotional_impact
        )
        self.memories.append(memory)
        
        # Update emotional state
        self.emotional_state += emotional_impact * 0.1
        self.emotional_state = max(-5.0, min(5.0, self.emotional_state))
        
        return memory
    
    def get_relevant_memories(self, query: str, limit: int = 5) -> List[CharacterMemory]:
        """
        获取与当前情境相关的记忆
        
        简单实现：基于关键词匹配
        进阶：使用向量相似度搜索（对接 AgentScope）
        """
        # 简单实现：按重要性排序 + 关键词匹配
        scored = []
        query_lower = query.lower()
        
        for mem in self.memories:
            score = mem.importance
            # 关键词匹配加分
            if any(word in mem.content.lower() for word in query_lower.split()):
                score += 3
            # 最近章节加分
            if mem.chapter >= max(1, len(self.memories) - 3):
                score += 1
            scored.append((score, mem))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [mem for _, mem in scored[:limit]]
    
    def react_to_event(self, event: str, chapter: int) -> str:
        """
        角色对事件的反应
        
        根据角色的 SOUL 生成符合人设的反应
        """
        relevant = self.get_relevant_memories(event)
        
        reaction = f"{self.name}"
        
        # 基于性格和情绪状态生成反应
        if self.emotional_state > 2:
            reaction += "表现得兴奋"
        elif self.emotional_state < -2:
            reaction += "沉默不语"
        else:
            reaction += "若有所思"
        
        # 加入相关记忆的影响
        if relevant:
            reaction += f"，脑海中浮现起过去的{relevant[0].content[:20]}..."
        
        return reaction
    
    def __str__(self) -> str:
        return f"Character({self.name}, {self.role})"


class CharacterAgent:
    """
    角色 Agent - 可以进行自主决策的角色
    
    这个类代表一个可以"思考"和"行动"的 AI 角色
    """
    
    def __init__(self, character: Character, llm_client=None):
        self.character = character
        self.llm_client = llm_client  # LLM 客户端（可选）
    
    def think(self, context: str) -> str:
        """
        角色思考 - 根据当前情境和记忆生成想法
        """
        relevant_memories = self.character.get_relevant_memories(context)
        
        prompt = f"""
你正在扮演角色：{self.character.name}
角色设定：{self.character.soul.personality}
当前处境：{self.character.soul.current_situation}
目标：{', '.join(self.character.soul.goals[:2])}

相关记忆：
{chr(10).join([m.content for m in relevant_memories[:3]])}

当前情境：{context}

请以这个角色的第一人称视角思考：你会怎么做？怎么想？
"""
        # 如果有 LLM，就调用
        if self.llm_client:
            return self.llm_client.chat(prompt)
        else:
            # 模拟思考
            return f"{self.character.name} 陷入了沉思..."
    
    def generate_dialogue(self, context: str, other_characters: List[Character] = None) -> str:
        """
        生成角色对话
        """
        prompt = f"""
角色：{self.character.name}
性格：{self.character.soul.personality}
说话风格：{self.character.soul.speech_style}

当前情境：{context}

请生成符合角色设定的对话。
"""
        if self.llm_client:
            return self.llm_client.chat(prompt)
        else:
            return f"{self.character.name} 说道：..."
    
    def __str__(self) -> str:
        return f"CharacterAgent({self.character.name})"