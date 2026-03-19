"""
Plot Manager - 伏笔管理与情节线索跟踪

解决"埋了伏笔后面忘记回收"的问题
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json
import uuid


class PlotType(Enum):
    """伏笔/情节类型"""
    FORESHADOW = "foreshadow"      # 伏笔
    CHARACTER_ARC = "character_arc"  # 角色成长线
    MYSTERY = "mystery"            # 悬念
    SUBPLOT = "subplot"            # 支线情节
    REVEAL = "reveal"              # 揭露/回收


class PlotStatus(Enum):
    """伏笔状态"""
    ACTIVE = "active"              # 活跃/已埋下
    DEVELOPING = "developing"      # 发展中
    READY_TO_REVEAL = "ready"      # 准备回收
    REVEALED = "revealed"          # 已回收
    ABANDONED = "abandoned"        # 已放弃/遗忘


@dataclass
class PlotThread:
    """
    情节线索/伏笔
    
    每个伏笔都是一个完整的生命周期：
    埋下 → 酝酿 → 回收
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""                    # 伏笔标题
    content: str = ""                  # 具体内容
    plot_type: PlotType = PlotType.FORESHADOW
    status: PlotStatus = PlotStatus.ACTIVE
    
    # 生命周期管理
    created_chapter: int = 0           # 埋下的章节
    target_reveal_chapter: Optional[int] = None  # 计划回收章节
    revealed_chapter: Optional[int] = None       # 实际回收章节
    
    # 关联
    related_characters: List[str] = field(default_factory=list)  # 相关角色
    related_locations: List[str] = field(default_factory=list)   # 相关地点
    
    # 线索片段（随着章节推进自动收集）
    clues: List[str] = field(default_factory=list)
    
    # 元数据
    created_at: datetime = field(default_factory=datetime.utcnow)
    importance: float = 7.0           # 1-10 重要程度
    
    def add_clue(self, clue: str, chapter: int):
        """添加关于这个伏笔的新线索"""
        self.clues.append(f"[第{chapter}章] {clue}")
    
    def reveal(self, reveal_content: str, chapter: int):
        """回收伏笔"""
        self.status = PlotStatus.REVEALED
        self.revealed_chapter = chapter
    
    def should_reveal(self, current_chapter: int) -> bool:
        """判断是否应该回收"""
        if self.status != PlotStatus.ACTIVE:
            return False
        
        if self.target_reveal_chapter:
            return current_chapter >= self.target_reveal_chapter
        
        # 默认：超过5章就该回收了
        return current_chapter - self.created_chapter >= 5
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "plot_type": self.plot_type.value,
            "status": self.status.value,
            "created_chapter": self.created_chapter,
            "target_reveal_chapter": self.target_reveal_chapter,
            "revealed_chapter": self.revealed_chapter,
            "related_characters": self.related_characters,
            "related_locations": self.related_locations,
            "clues": self.clues,
            "importance": self.importance
        }


class PlotManager:
    """
    情节管理器 - 全局管理所有伏笔和线索
    
    核心功能：
    1. 自动追踪所有伏笔
    2. 适时提醒回收
    3. 生成回收建议
    """
    
    def __init__(self):
        self.threads: Dict[str, PlotThread] = {}
        self.plot_outline: List[Dict[str, Any]] = []  # 大纲
    
    def create_foreshadow(
        self,
        title: str,
        content: str,
        chapter: int,
        related_characters: List[str] = None,
        target_reveal: int = None,
        importance: float = 7.0
    ) -> PlotThread:
        """创建一个新伏笔"""
        thread = PlotThread(
            title=title,
            content=content,
            plot_type=PlotType.FORESHADOW,
            created_chapter=chapter,
            target_reveal_chapter=target_reveal,
            related_characters=related_characters or [],
            importance=importance
        )
        self.threads[thread.id] = thread
        return thread
    
    def add_character_arc(
        self,
        character_name: str,
        arc_description: str,
        chapter: int
    ) -> PlotThread:
        """创建角色成长线"""
        thread = PlotThread(
            title=f"{character_name}的成长",
            content=arc_description,
            plot_type=PlotType.CHARACTER_ARC,
            created_chapter=chapter,
            related_characters=[character_name]
        )
        self.threads[thread.id] = thread
        return thread
    
    def add_subplot(
        self,
        title: str,
        content: str,
        chapter: int,
        related_characters: List[str] = None
    ) -> PlotThread:
        """创建支线情节"""
        thread = PlotThread(
            title=title,
            content=content,
            plot_type=PlotType.SUBPLOT,
            created_chapter=chapter,
            related_characters=related_characters or []
        )
        self.threads[thread.id] = thread
        return thread
    
    def get_active_plots(self) -> List[PlotThread]:
        """获取所有活跃的伏笔"""
        return [t for t in self.threads.values() if t.status == PlotStatus.ACTIVE]
    
    def get_plots_needing_attention(self, current_chapter: int) -> List[PlotThread]:
        """
        获取需要关注的伏笔（该回收了）
        
        触发条件：
        1. 已到计划回收章节
        2. 酝酿时间过长（超过5章）
        3. 重要性很高但迟迟未回收
        """
        attention_needed = []
        
        for thread in self.get_active_plots():
            if thread.should_reveal(current_chapter):
                thread.status = PlotStatus.READY_TO_REVEAL
                attention_needed.append(thread)
            elif current_chapter - thread.created_chapter >= 8 and thread.importance >= 8:
                # 重要伏笔拖太久
                attention_needed.append(thread)
        
        return attention_needed
    
    def generate_reveal_suggestions(self, current_chapter: int) -> List[Dict[str, Any]]:
        """
        生成伏笔回收建议
        
        为每个该回收的伏笔生成具体的回收方案
        """
        suggestions = []
        
        for thread in self.get_plots_needing_attention(current_chapter):
            suggestion = {
                "plot_id": thread.id,
                "title": thread.title,
                "original_content": thread.content,
                "clues_collected": thread.clues,
                "suggested_reveal": self._generate_reveal_way(thread),
                "chapter": current_chapter,
                "related_characters": thread.related_characters
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_reveal_way(self, thread: PlotThread) -> str:
        """生成回收方式建议"""
        if thread.plot_type == PlotType.FORESHADOW:
            return f"通过{thread.related_characters[0] if thread.related_characters else '某个关键事件'}揭露"
        elif thread.plot_type == PlotType.CHARACTER_ARC:
            return f"让{thread.related_characters[0]}经历关键转折点"
        else:
            return "在情节高潮处自然揭露"
    
    def reveal_plot(self, plot_id: str, chapter: int):
        """标记伏笔已回收"""
        if plot_id in self.threads:
            self.threads[plot_id].status = PlotStatus.REVEALED
            self.threads[plot_id].revealed_chapter = chapter
    
    def get_character_plots(self, character_name: str) -> List[PlotThread]:
        """获取与某个角色相关的所有伏笔"""
        return [
            t for t in self.threads.values()
            if character_name in t.related_characters and t.status != PlotStatus.REVEALED
        ]
    
    def check_plot_consistency(self, current_chapter: int, characters: List[str]) -> List[str]:
        """
        检查情节一致性
        
        返回潜在的问题列表
        """
        issues = []
        
        for thread in self.get_active_plots():
            # 检查相关角色是否在最近章节出现
            if thread.related_characters:
                # 如果伏笔超过3章没动静，可能需要关注
                if current_chapter - thread.created_chapter >= 3:
                    # 检查是否有线索
                    if len(thread.clues) == 0:
                        issues.append(
                            f"⚠️ 伏笔 '{thread.title}' 已{current_chapter - thread.created_chapter}章无进展"
                        )
        
        return issues
    
    def save_to_file(self, filepath: str):
        """保存到文件"""
        data = {
            "threads": [t.to_dict() for t in self.threads.values()],
            "plot_outline": self.plot_outline
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filepath: str):
        """从文件加载"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.threads = {}
        for thread_data in data.get("threads", []):
            thread = PlotThread(
                id=thread_data["id"],
                title=thread_data["title"],
                content=thread_data["content"],
                plot_type=PlotType(thread_data["plot_type"]),
                status=PlotStatus(thread_data["status"]),
                created_chapter=thread_data["created_chapter"],
                target_reveal_chapter=thread_data.get("target_reveal_chapter"),
                revealed_chapter=thread_data.get("revealed_chapter"),
                related_characters=thread_data.get("related_characters", []),
                importance=thread_data.get("importance", 7.0)
            )
            self.threads[thread.id] = thread
        
        self.plot_outline = data.get("plot_outline", [])
    
    def __len__(self):
        return len(self.threads)


# 便捷函数
def create_plot_tracker() -> PlotManager:
    """创建情节追踪器"""
    return PlotManager()