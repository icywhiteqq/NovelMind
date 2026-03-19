"""
NovelForge - AI-Powered Long-Form Novel Writing with Autonomous Characters

每个角色都是有灵魂的 AI Agent。
"""

__version__ = "0.1.0"

from .novel import Novel, Chapter, ChapterPlan, WorldState
from .character import Character, CharacterAgent, Soul
from .memory import Memory, MemoryType, MemoryStore, CharacterMemoryPool
from .plot import PlotThread, PlotManager, PlotType, PlotStatus
from .style import StyleProfile, StyleAnalyzer, StyleConsistencyChecker, PresetStyles

__all__ = [
    # Novel
    "Novel",
    "Chapter",
    "ChapterPlan",
    "WorldState",
    # Character
    "Character", 
    "CharacterAgent",
    "Soul",
    # Memory
    "Memory",
    "MemoryType",
    "MemoryStore",
    "CharacterMemoryPool",
    # Plot
    "PlotThread",
    "PlotManager",
    "PlotType",
    "PlotStatus",
    # Style
    "StyleProfile",
    "StyleAnalyzer",
    "StyleConsistencyChecker",
    "PresetStyles",
]