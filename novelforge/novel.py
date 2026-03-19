"""
Novel - 小说主控类

整合所有模块，控制章节生成流程
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

from .character import Character, CharacterAgent
from .memory import MemoryStore, MemoryType
from .plot import PlotManager, PlotType
from .style import StyleProfile, StyleConsistencyChecker


@dataclass
class Chapter:
    """章节"""
    number: int
    title: str
    content: str = ""
    summary: str = ""           # 章Summary
    word_count: int = 0
    plot_points: List[str] = field(default_factory=list)  # 本章要写的情节点
    created_at: datetime = field(default_factory=datetime.utcnow)
    style_score: float = 0.0    # 文风一致性得分
    issues: List[str] = field(default_factory=list)        # 问题列表
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "number": self.number,
            "title": self.title,
            "content": self.content,
            "summary": self.summary,
            "word_count": self.word_count,
            "plot_points": self.plot_points,
            "created_at": self.created_at.isoformat(),
            "style_score": self.style_score,
            "issues": self.issues
        }


class ChapterPlan:
    """章节规划"""
    
    def __init__(self, total_chapters: int = 100):
        self.total_chapters = total_chapters
        self.current_chapter = 0
        self.plans: Dict[int, Dict[str, Any]] = {}  # chapter_num -> plan
    
    def add_chapter_plan(
        self,
        chapter: int,
        title: str,
        plot_points: List[str],
        purpose: str = "",  # 推进剧情/回收伏笔/塑造人物
        foreshadowing: List[str] = None  # 本章埋下的伏笔
    ):
        """添加章节规划"""
        self.plans[chapter] = {
            "title": title,
            "plot_points": plot_points,
            "purpose": purpose,
            "foreshadowing": foreshadowing or [],
            "status": "planned"  # planned / writing / completed
        }
    
    def get_plan(self, chapter: int) -> Optional[Dict[str, Any]]:
        """获取章节规划"""
        return self.plans.get(chapter)
    
    def get_next_plan(self) -> Optional[Dict[str, Any]]:
        """获取下一章规划"""
        self.current_chapter += 1
        return self.get_plan(self.current_chapter)


class WorldState:
    """
    世界状态管理 - 解决"设定前后矛盾"
    
    追踪所有世界观设定，确保一致性
    """
    
    def __init__(self):
        self.settings: Dict[str, Any] = {}     # 世界设定
        self.locations: Dict[str, Dict] = {}   # 地点信息
        self.factions: Dict[str, Dict] = {}    # 势力信息
        self.power_system: Dict[str, Any] = {} # 力量体系
        
        self.history: List[Dict] = []           # 世界事件历史
        self.constraints: List[str] = []        # 约束规则
    
    def add_setting(self, key: str, value: Any, chapter: int = 0):
        """添加世界设定"""
        self.settings[key] = {
            "value": value,
            "chapter": chapter,
            "updated_at": datetime.utcnow().isoformat()
        }
    
    def add_location(self, name: str, description: str, **kwargs):
        """添加地点"""
        self.locations[name] = {
            "description": description,
            "created_at": datetime.utcnow().isoformat(),
            **kwargs
        }
    
    def add_faction(self, name: str, description: str, **kwargs):
        """添加势力"""
        self.factions[name] = {
            "description": description,
            **kwargs
        }
    
    def set_power_system(self, system: Dict[str, Any]):
        """设置力量体系"""
        self.power_system = system
    
    def validate_action(self, action: str, character: str = None) -> Dict[str, Any]:
        """
        验证某个行为是否与世界设定冲突
        
        返回：{"valid": True/False, "issues": [...]}
        """
        issues = []
        
        # 检查力量体系冲突
        # 检查地点是否存在
        # 检查角色能力是否合理
        
        # 简化实现
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    def record_event(self, event: str, chapter: int):
        """记录世界事件"""
        self.history.append({
            "event": event,
            "chapter": chapter,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_history(self, chapter: int = None) -> List[Dict]:
        """获取世界历史"""
        if chapter:
            return [h for h in self.history if h["chapter"] <= chapter]
        return self.history
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "settings": self.settings,
            "locations": self.locations,
            "factions": self.factions,
            "power_system": self.power_system,
            "history": self.history,
            "constraints": self.constraints
        }


class Novel:
    """
    小说主控类
    
    使用流程：
    1. 创建 Novel 实例，设定世界观
    2. 添加角色（每个角色有 SOUL）
    3. 规划章节大纲
    4. 一章一章生成
    5. 自动一致性检查
    """
    
    def __init__(
        self,
        title: str,
        genre: str = "奇幻",
        world_settings: Dict[str, Any] = None,
        style: StyleProfile = None
    ):
        self.id = str(datetime.now().timestamp())
        self.title = title
        self.genre = genre
        self.created_at = datetime.utcnow()
        
        # 世界状态
        self.world = WorldState()
        if world_settings:
            for k, v in world_settings.items():
                self.world.add_setting(k, v)
        
        # 风格配置
        self.style = style or StyleProfile(name="默认")
        self.style_checker = StyleConsistencyChecker(self.style)
        
        # 角色管理
        self.characters: Dict[str, Character] = {}
        self.character_agents: Dict[str, CharacterAgent] = {}
        
        # 章节管理
        self.chapters: Dict[int, Chapter] = {}
        self.chapter_plan = ChapterPlan()
        self.current_chapter = 0
        
        # 记忆系统
        self.memory = MemoryStore(title)
        
        # 伏笔管理
        self.plot_manager = PlotManager()
        
        # 设置
        self.llm_client = None  # 可选：接入 LLM
    
    # ========== 角色管理 ==========
    
    def add_character(self, character: Character):
        """添加角色"""
        self.characters[character.name] = character
        # 记录到世界
        self.world.add_faction(
            character.name,
            f"{character.role}: {character.description}",
            role=character.role,
            soul=character.soul.to_dict()
        )
    
    def get_character(self, name: str) -> Optional[Character]:
        """获取角色"""
        return self.characters.get(name)
    
    # ========== 章节规划 ==========
    
    def plan_chapter(
        self,
        chapter: int,
        title: str,
        plot_points: List[str],
        purpose: str = "推进剧情",
        foreshadowing: List[str] = None
    ):
        """规划章节"""
        self.chapter_plan.add_chapter_plan(
            chapter, title, plot_points, purpose, foreshadowing
        )
        
        # 如果有伏笔，自动添加到伏笔管理器
        if foreshadowing:
            for fs in foreshadowing:
                self.plot_manager.create_foreshadow(
                    title=fs,
                    content=fs,
                    chapter=chapter,
                    related_characters=list(self.characters.keys()),
                    importance=7.0
                )
    
    def plan_outline(self, outline: Dict[int, Dict[str, Any]]):
        """批量规划章节大纲"""
        for ch, plan in outline.items():
            self.plan_chapter(
                chapter=ch,
                title=plan["title"],
                plot_points=plan["plot_points"],
                purpose=plan.get("purpose", "推进剧情"),
                foreshadowing=plan.get("foreshadowing", [])
            )
    
    # ========== 章节生成 ==========
    
    def write_chapter(
        self,
        title: str = None,
        plot_points: List[str] = None,
        content: str = None,
        use_llm: bool = False
    ) -> Chapter:
        """
        生成一章
        
        Args:
            title: 章节标题
            plot_points: 情节点（会自动融入）
            content: 如果不调用 LLM，可以直接传入写好的内容进行校验
            use_llm: 是否调用 LLM 生成
        
        Returns:
            Chapter 对象
        """
        self.current_chapter += 1
        ch_num = self.current_chapter
        
        # 获取章节规划
        plan = self.chapter_plan.get_plan(ch_num)
        if plan:
            title = title or plan["title"]
            plot_points = plot_points or plan["plot_points"]
        
        chapter = Chapter(
            number=ch_num,
            title=title or f"第{ch_num}章",
            plot_points=plot_points or []
        )
        
        # 强制使用 LLM 生成（如果配置了）
        import os
        from .config import Config
        
        has_api_key = bool(Config.LLM_API_KEY and Config.LLM_API_KEY != "sk-YOUR-KEY-HERE")
        
        if use_llm or has_api_key:
            try:
                chapter.content = self._generate_with_llm(chapter)
            except Exception as e:
                chapter.content = self._generate_demo(chapter)
        elif content:
            chapter.content = content
        else:
            chapter.content = self._generate_demo(chapter)
        
        # 统计字数
        chapter.word_count = len(chapter.content)
        
        # 文风检查
        style_result = self.style_checker.check(chapter.content)
        chapter.style_score = style_result["score"]
        chapter.issues = style_result["issues"]
        
        # 保存章节
        self.chapters[ch_num] = chapter
        
        # 更新记忆
        self._update_memories(chapter)
        
        # 检查伏笔
        self._check_plots(ch_num)
        
        return chapter
    
    def _generate_with_llm(self, chapter: Chapter) -> str:
        """调用 LLM 生成内容"""
        # 构建提示词
        context = self._build_context(chapter)
        # 详细展开每个情节点
        plot_detail = ""
        for i, point in enumerate(chapter.plot_points, 1):
            plot_detail += f"{i}. {point}\n"
        
        characters_desc = ""
        for name, char in self.characters.items():
            soul = char.soul
            goals = ', '.join(soul.goals) if soul.goals else '无'
            secrets = ', '.join(soul.secrets) if soul.secrets else '无'
            characters_desc += f"- {char.name}（{char.role}）：{soul.personality}，目标：{goals}，秘密：{secrets}\n"
        
        prompt = f"""你是一个专业的小说作家。请根据以下提纲创作一章精彩的小说。

【小说标题】{self.title}
【小说类型】{self.genre}
【本章标题】{chapter.title}

【世界观设定】
{json.dumps(self.world.to_dict(), ensure_ascii=False, indent=2)}

【角色介绍】
{characters_desc}

【本章剧情提纲】
{plot_detail}

【写作要求】
1. 每个情节点要展开成500-1000字的详细描写
2. 对话要符合角色性格
3. 要有场景描写和心理描写
4. 情节要连贯，有代入感
5. 字数要求：至少1500字
6. 必须输出完整的小说正文，不能只是大纲

请开始创作正文："""
        # 调用 LLM
        return self._call_llm(prompt)
    
    def _call_llm(self, prompt: str) -> str:
        """调用LLM API"""
        from .llm_client import llm_client
        import time
        
        # 重试3次
        for attempt in range(3):
            try:
                return llm_client.call(prompt)
            except Exception as e:
                if attempt == 2:
                    return f"[LLM调用失败: {e}]\n\n请检查API配置。"
                time.sleep(2)
    
    def _generate_demo(self, chapter: Chapter) -> str:
        """生成示例内容（不调用 LLM 时使用）"""
        # 简单拼接情节点作为演示
        content = f"# {chapter.title}\n\n"
        
        if self.characters:
            main_char = list(self.characters.values())[0]
            content += f"{main_char.name}站在山巅，望着远方的云海。\n\n"
        
        for point in chapter.plot_points:
            content += f"就在这时，{point}。\n\n"
        
        content += f"（本章字数：约{len(content)*5}字）\n"
        content += f"—— 本章完 ——\n"
        
        return content
    
    def _build_context(self, chapter: Chapter) -> str:
        """构建生成上下文"""
        # 获取前几章的 summary
        prev_summaries = []
        for i in range(max(1, chapter.number - 3), chapter.number):
            if i in self.chapters:
                prev_summaries.append(self.chapters[i].summary)
        
        # 获取当前活跃伏笔
        active_plots = self.plot_manager.get_active_plots()
        
        return f"""
小说标题：{self.title}
当前章节：第{chapter.number}章

前情提要：
{chr(10).join(prev_summaries) or "暂无"}

当前活跃伏笔：
{chr(10).join([p.title for p in active_plots])}

本章要写：{', '.join(chapter.plot_points)}
"""
    
    def _update_memories(self, chapter: Chapter):
        """更新记忆系统"""
        # 记录章节概要
        self.memory.add_memory(
            content=f"第{chapter.number}章: {chapter.title} - {chapter.summary or '待补充'}",
            memory_type=MemoryType.PLOT,
            chapter=chapter.number,
            importance=5.0,
            tags=["章节", str(chapter.number)]
        )
        
        # 记录每个角色的重要事件
        for char in self.characters.values():
            # 从本章内容中提取相关事件（简化：直接记录本章标题）
            char.add_memory(
                content=f"第{chapter.number}章参与: {chapter.title}",
                chapter=chapter.number,
                importance=3.0
            )
    
    def _check_plots(self, chapter_num: int):
        """检查伏笔回收"""
        # 获取需要关注的伏笔
        needs_attention = self.plot_manager.get_plots_needing_attention(chapter_num)
        
        if needs_attention:
            print(f"\n⚠️ 第{chapter_num}章 - 伏笔提醒:")
            for plot in needs_attention:
                print(f"  • {plot.title} (第{plot.created_chapter}章埋下)")
    
    # ========== 辅助方法 ==========
    
    def get_chapter(self, num: int) -> Optional[Chapter]:
        """获取章节"""
        return self.chapters.get(num)
    
    def get_summary(self, from_chapter: int = 1, to_chapter: int = None) -> str:
        """获取剧情概要"""
        to_chapter = to_chapter or self.current_chapter
        summaries = []
        
        for i in range(from_chapter, to_chapter + 1):
            ch = self.chapters.get(i)
            if ch and ch.summary:
                summaries.append(f"第{i}章: {ch.summary}")
        
        return "\n".join(summaries) or "暂无概要"
    
    def save(self, filepath: str = None):
        """保存小说进度"""
        filepath = filepath or f"{self.title}_save.json"
        
        data = {
            "title": self.title,
            "genre": self.genre,
            "current_chapter": self.current_chapter,
            "world": self.world.to_dict(),
            "style": self.style.to_dict(),
            "chapters": {k: v.to_dict() for k, v in self.chapters.items()},
            "saved_at": datetime.utcnow().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 保存伏笔
        self.plot_manager.save_to_file(f"{self.title}_plots.json")
        
        print(f"✅ 已保存到 {filepath}")
    
    def load(self, filepath: str):
        """加载小说进度"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.title = data["title"]
        self.current_chapter = data["current_chapter"]
        
        # 加载章节
        self.chapters = {}
        for k, v in data["chapters"].items():
            ch = Chapter(
                number=v["number"],
                title=v["title"],
                content=v.get("content", ""),
                summary=v.get("summary", ""),
                word_count=v.get("word_count", 0)
            )
            self.chapters[int(k)] = ch
        
        # 加载伏笔
        self.plot_manager.load_from_file(f"{self.title}_plots.json")
        
        print(f"✅ 已从 {filepath} 加载")
    
    def __str__(self) -> str:
        return f"Novel({self.title}, {self.current_chapter}章, {len(self.characters)}个角色)"