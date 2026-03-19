"""
NovelForge Demo - 展示核心功能
"""

from novelforge import Character, CharacterAgent
from novelforge.memory import MemoryStore, MemoryType, CharacterMemoryPool
from novelforge.plot import PlotManager, PlotType


def demo_character_soul():
    """演示角色 SOUL 系统"""
    print("=" * 60)
    print("🎭 角色 SOUL 系统演示")
    print("=" * 60)
    
    # 创建一个有灵魂的角色
    character = Character(
        name="李云",
        role="主角",
        soul={
            "background": "青云宗外门弟子，父母双亡",
            "origin": "偏远山村",
            "current_situation": "下山历练，寻找灭门真相",
            "goals": ["找到仇家", "提升实力"],
            "long_term_goals": ["振兴家族", "揭开真相"],
            "fears": ["失去身边重要的人", "实力不足"],
            "personality": "沉稳内敛，但关键时刻果断",
            "strengths": ["剑道天赋", "意志坚定"],
            "weaknesses": ["感情用事", "不善表达"],
            "speech_style": "简洁有力，不多说废话",
            "habits": ["思考时抚摸剑柄", "喜欢独处"],
            "secrets": ["体内藏有上古血脉", "其实是天灵根"],
            "hidden_past": "曾被灭门，但记忆被封印",
            "connections": {"神秘少女": "救命恩人"}
        }
    )
    
    print(f"\n角色: {character.name}")
    print(f"定位: {character.role}")
    print(f"\n{character.soul}")
    
    return character


def demo_memory_system():
    """演示记忆系统"""
    print("\n" + "=" * 60)
    print("🧠 记忆系统演示")
    print("=" * 60)
    
    store = MemoryStore("demo_novel")
    
    # 添加各种记忆
    store.add_memory(
        content="李云在山下遇到神秘少女，少女救了他一命",
        memory_type=MemoryType.CHARACTER,
        chapter=1,
        importance=8.0,
        tags=["李云", "神秘少女", "相遇"]
    )
    
    store.add_memory(
        content="李云发现体内有异样的灵气流动",
        memory_type=MemoryType.Foreshadowing,
        chapter=2,
        importance=9.0,
        tags=["伏笔", "血脉"]
    )
    
    store.add_memory(
        content="五行灵气分为金木水火土五种属性",
        memory_type=MemoryType.WORLD,
        chapter=1,
        importance=6.0,
        tags=["世界观", "灵气"]
    )
    
    # 搜索记忆
    print("\n🔍 搜索 '李云' 相关的记忆:")
    results = store.search("李云", limit=5)
    for i, mem in enumerate(results, 1):
        print(f"  {i}. [第{mem.chapter}章] {mem.content[:40]}...")
    
    # 搜索伏笔
    print("\n🔮 当前所有伏笔:")
    foreshadowings = store.get_all_by_type(MemoryType.Foreshadowing)
    for f in foreshadowings:
        print(f"  • {f.content}")
    
    return store


def demo_plot_manager():
    """演示伏笔管理"""
    print("\n" + "=" * 60)
    print("🎯 伏笔管理系统演示")
    print("=" * 60)
    
    plot_manager = PlotManager()
    
    # 创建伏笔
    plot_manager.create_foreshadow(
        title="神秘血脉",
        content="李云体内藏有上古血脉，觉醒后将拥有强大力量",
        chapter=1,
        related_characters=["李云"],
        target_reveal=10,
        importance=9.0
    )
    
    # 创建支线
    plot_manager.add_subplot(
        title="神秘少女的身份",
        content="神秘少女实际上是仙族后裔，与李云有婚约",
        chapter=2,
        related_characters=["李云", "神秘少女"]
    )
    
    # 模拟情节发展，添加线索
    thread = list(plot_manager.get_active_plots())[0]
    thread.add_clue("李云在战斗中意外激活了血脉", 3)
    thread.add_clue("神秘少女看到李云的血脉后表情大变", 5)
    
    print("\n📋 当前活跃伏笔:")
    for plot in plot_manager.get_active_plots():
        print(f"  • {plot.title} (第{plot.created_chapter}章埋下)")
    
    print("\n💡 第6章的伏笔回收建议:")
    suggestions = plot_manager.generate_reveal_suggestions(6)
    for s in suggestions:
        print(f"  伏笔: {s['title']}")
        print(f"  线索: {s['clues_collected']}")
        print(f"  建议: {s['suggested_reveal']}")
    
    # 情节一致性检查
    print("\n⚠️ 情节一致性检查:")
    issues = plot_manager.check_plot_consistency(6, ["李云", "神秘少女"])
    for issue in issues:
        print(f"  {issue}")
    
    return plot_manager


def demo_character_memory_pool():
    """演示角色记忆池"""
    print("\n" + "=" * 60)
    print("👤 角色记忆池演示")
    print("=" * 60)
    
    store = MemoryStore("demo_novel2")
    pool = CharacterMemoryPool("李云", store)
    
    # 记录互动
    pool.store_interaction(
        other_character="神秘少女",
        content="少女为李云疗伤，两人的距离拉近了",
        chapter=1,
        emotional_impact=2.0
    )
    
    pool.store_interaction(
        other_character="神秘少女",
        content="少女似乎有什么隐瞒，匆匆离去",
        chapter=3,
        emotional_impact=-1.0
    )
    
    # 记录秘密
    pool.store_secret_event(
        content="李云发现自己能吸收五种灵气，这是五行天灵根的标志",
        chapter=2,
        will_reveal_chapter=15
    )
    
    # 查询关系
    print("\n🤝 李云与神秘少女的关系状态:")
    status = pool.get_relationship_status("神秘少女")
    print(f"  {status}")
    
    # 回忆重要事件
    print("\n📖 李云回忆过去的重要事件:")
    events = pool.recall_important_events(4, how_many_back=3)
    for e in events:
        print(f"  • {e.content}")


def main():
    print("\n🖊️ NovelForge Demo")
    print("AI小说写作框架 - 每个角色都是有灵魂的 Agent\n")
    
    # 1. 角色 SOUL 系统
    character = demo_character_soul()
    
    # 2. 记忆系统
    store = demo_memory_system()
    
    # 3. 伏笔管理
    plot_manager = demo_plot_manager()
    
    # 4. 角色记忆池
    demo_character_memory_pool()
    
    print("\n" + "=" * 60)
    print("✅ Demo 完成!")
    print("=" * 60)
    print("""
这个 Demo 展示了 NovelForge 的核心能力：

1. 🎭 角色 SOUL
   - 每个角色有独特的背景、目标、性格、秘密
   - 角色不再是提线木偶，而是有灵魂的个体

2. 🧠 记忆系统  
   - 长期记忆存储，不会越写越乱
   - 向量级检索，相关记忆随时调用

3. 🎯 伏笔管理
   - 自动追踪所有伏笔
   - 适时提醒回收，不再遗忘

4. 👤 角色记忆池
   - 记录角色间的互动
   - 追踪情感变化和关系发展
""")


if __name__ == "__main__":
    main()