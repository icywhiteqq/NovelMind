"""
Memory System - 长期记忆与向量检索

对接 AgentScope，提供语义级别的记忆检索
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json
import os
from pathlib import Path


class MemoryType(Enum):
    """记忆类型"""
    CHARACTER = "character"      # 角色记忆
    PLOT = "plot"                # 情节记忆
    WORLD = "world"              # 世界设定
    DIALOGUE = "dialogue"        # 对话记忆
    EMOTION = "emotion"          # 情感记忆
    Foreshadowing = "foreshadowing"  # 伏笔


@dataclass
class Memory:
    """记忆单元"""
    id: str
    type: MemoryType
    content: str
    chapter: int
    embedding: Optional[List[float]] = None  # 向量（预留）
    importance: float = 5.0  # 1-10
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "content": self.content,
            "chapter": self.chapter,
            "importance": self.importance,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
            "metadata": self.metadata
        }


class MemoryStore:
    """
    记忆存储 - 支持向量检索和关键词搜索
    
    支持两种模式：
    1. 本地文件存储（开发用）
    2. 对接 AgentScope（生产用）
    """
    
    def __init__(self, project_name: str, storage_path: str = "./novel_memory"):
        self.project_name = project_name
        self.storage_path = Path(storage_path) / project_name
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.memories: Dict[str, Memory] = {}
        self._load_from_disk()
    
    def _load_from_disk(self):
        """从磁盘加载记忆"""
        index_file = self.storage_path / "index.json"
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for mem_data in data.get("memories", []):
                    mem = Memory(
                        id=mem_data["id"],
                        type=MemoryType(mem_data["type"]),
                        content=mem_data["content"],
                        chapter=mem_data["chapter"],
                        importance=mem_data.get("importance", 5.0),
                        tags=mem_data.get("tags", []),
                        metadata=mem_data.get("metadata", {})
                    )
                    self.memories[mem.id] = mem
    
    def _save_to_disk(self):
        """保存记忆到磁盘"""
        index_file = self.storage_path / "index.json"
        data = {
            "project": self.project_name,
            "updated_at": datetime.utcnow().isoformat(),
            "memories": [m.to_dict() for m in self.memories.values()]
        }
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add(self, memory: Memory):
        """添加记忆"""
        self.memories[memory.id] = memory
        self._save_to_disk()
    
    def add_memory(
        self,
        content: str,
        memory_type: MemoryType,
        chapter: int,
        importance: float = 5.0,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> Memory:
        """便捷添加记忆方法"""
        import uuid
        memory = Memory(
            id=str(uuid.uuid4()),
            type=memory_type,
            content=content,
            chapter=chapter,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {}
        )
        self.add(memory)
        return memory
    
    def search(
        self,
        query: str,
        memory_type: Optional[MemoryType] = None,
        chapter_range: Optional[tuple] = None,
        limit: int = 10
    ) -> List[Memory]:
        """
        搜索记忆
        
        简单实现：关键词匹配 + 重要性排序
        进阶：使用向量相似度
        """
        results = []
        query_words = query.lower().split()
        
        for mem in self.memories.values():
            # 按类型过滤
            if memory_type and mem.type != memory_type:
                continue
            
            # 按章节范围过滤
            if chapter_range:
                if not (chapter_range[0] <= mem.chapter <= chapter_range[1]):
                    continue
            
            # 计算相关性分数
            score = 0
            content_lower = mem.content.lower()
            
            # 关键词匹配
            for word in query_words:
                if word in content_lower:
                    score += 2
            
            # 重要性加权
            score += mem.importance * 0.5
            
            # 最近章节加权
            score += max(0, 10 - mem.chapter) * 0.2
            
            if score > 0:
                results.append((score, mem))
        
        # 排序并返回
        results.sort(key=lambda x: x[0], reverse=True)
        return [mem for _, mem in results[:limit]]
    
    def get_by_chapter(self, chapter: int, memory_type: Optional[MemoryType] = None) -> List[Memory]:
        """获取指定章节的记忆"""
        results = []
        for mem in self.memories.values():
            if mem.chapter == chapter:
                if memory_type is None or mem.type == memory_type:
                    results.append(mem)
        return results
    
    def get_all_by_type(self, memory_type: MemoryType) -> List[Memory]:
        """获取指定类型的所有记忆"""
        return [m for m in self.memories.values() if m.type == memory_type]
    
    def __len__(self):
        return len(self.memories)


class CharacterMemoryPool:
    """
    角色记忆池 - 管理每个角色的个人记忆
    
    解决"越写越乱"的核心组件
    """
    
    def __init__(self, character_name: str, store: MemoryStore):
        self.character_name = character_name
        self.store = store
    
    def store_interaction(
        self,
        other_character: str,
        content: str,
        chapter: int,
        emotional_impact: float = 0.0
    ):
        """记录角色互动"""
        self.store.add_memory(
            content=f"[与{other_character}] {content}",
            memory_type=MemoryType.CHARACTER,
            chapter=chapter,
            importance=5.0 + abs(emotional_impact),
            tags=[other_character, "互动"],
            metadata={
                "character": self.character_name,
                "other": other_character,
                "emotional_impact": emotional_impact
            }
        )
    
    def store_secret_event(
        self,
        content: str,
        chapter: int,
        will_reveal_chapter: Optional[int] = None
    ):
        """记录秘密事件（伏笔）"""
        self.store.add_memory(
            content=content,
            memory_type=MemoryType.Foreshadowing,
            chapter=chapter,
            importance=8.0,  # 秘密通常重要
            tags=["伏笔", "秘密"],
            metadata={
                "will_reveal": will_reveal_chapter,
                "revealed": False
            }
        )
    
    def get_relationship_status(self, other_character: str) -> str:
        """获取与其他角色的关系状态"""
        memories = self.store.search(
            query=other_character,
            memory_type=MemoryType.CHARACTER,
            limit=5
        )
        
        if not memories:
            return "陌生"
        
        # 简单分析情感倾向
        total_impact = 0
        for mem in memories:
            meta = mem.metadata
            if meta.get("other") == other_character:
                total_impact += meta.get("emotional_impact", 0)
        
        if total_impact > 3:
            return "友好"
        elif total_impact < -3:
            return "敌对"
        else:
            return "一般"
    
    def recall_important_events(self, chapter: int, how_many_back: int = 3) -> List[Memory]:
        """让角色回忆过去的重要事件"""
        target_chapters = range(max(1, chapter - how_many_back), chapter + 1)
        all_memories = []
        
        for ch in target_chapters:
            ch_memories = self.store.get_by_chapter(ch, MemoryType.CHARACTER)
            for mem in ch_memories:
                if mem.metadata.get("character") == self.character_name:
                    if mem.importance >= 7.0:  # 只回忆重要的
                        all_memories.append(mem)
        
        return all_memories


# 便捷函数：创建带有 AgentScope 集成的记忆系统
def create_memory_system(novel_name: str, use_agentscope: bool = False) -> MemoryStore:
    """
    创建小说记忆系统
    
    Args:
        novel_name: 小说名称
        use_agentscope: 是否使用 AgentScope（需要额外配置）
    
    Returns:
        MemoryStore 实例
    """
    store = MemoryStore(novel_name)
    
    if use_agentscope:
        # TODO: 对接 AgentScope
        # 可以在这里集成 AgentScope 的向量搜索
        pass
    
    return store