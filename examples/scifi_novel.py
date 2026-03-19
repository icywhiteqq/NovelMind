"""
科幻小说项目 - 《星际觉醒》
完整演示如何用 NovelForge 写长篇小说
"""

from novelforge import (
    Novel, Character,
    StyleProfile, PresetStyles,
    MemoryType
)


def create_scifi_novel():
    """创建科幻小说"""
    
    print("🚀 创建科幻小说：《星际觉醒》")
    print("=" * 60)
    
    # ===== 1. 创建小说 =====
    novel = Novel(
        title="星际觉醒",
        genre="科幻",
        world_settings={
            "时间背景": "2157年",
            "科技水平": "曲速引擎、人工智能、意识上传",
            "主要势力": "地球联邦、泰坦集团、星际海盗",
            "科技限制": "光速仍是上限，曲速需要巨大能量"
        }
    )
    
    # 设置科幻文风
    style = StyleProfile(
        name="科幻硬核",
        description="严谨的科幻文风",
        sentence_length_avg=25.0,      # 稍长的句子
        sentence_length_variance=10.0,
        short_sentence_ratio=0.2,
        long_sentence_ratio=0.25,
        use_metaphor=True,
        use_simile=True,
        use_hyperbole=False,
        use_allusion=False,
        vocabulary_level=8.0,           # 专业的词汇
        use_classical=False,
        use_technical=True,             # 使用科技术语
        emotional_tone=5.0,
        sentiment=6.0,                  # 略微乐观
        dialogue_to_narration_ratio=0.3,
        dialogue_style="简洁专业",
        pacing=6.0,
        tension_buildup=7.0
    )
    novel.style = style
    
    # ===== 2. 创建角色 =====
    
    # 主角 - 舰长
    protagonist = Character(
        name="陈锋",
        role="主角",
        soul={
            "background": "地球联邦少校，旗舰'探索号'舰长",
            "origin": "火星殖民地",
            "current_situation": "执行一项神秘任务",
            "goals": ["完成任务", "保护船员", "揭开真相"],
            "long_term_goals": ["找到人类起源", "拯救联邦"],
            "fears": ["失去船员", "任务失败"],
            "personality": "冷静果敢，但内心孤独",
            "strengths": ["丰富的战斗经验", "出色的战略眼光"],
            "weaknesses": ["过于理性", "不善于表达感情"],
            "speech_style": "简洁有力，用军事术语",
            "habits": ["思考时揉太阳穴", "在舰桥来回踱步"],
            "secrets": ["曾是泰坦集团特工"],
            "hidden_past": "在一次任务中亲手处决了叛徒"
        }
    )
    novel.add_character(protagonist)
    
    # AI 副手
    ai = Character(
        name="雅典娜",
        role="配角/AI",
        soul={
            "background": "联邦最先进的军用AI，拥有自我意识",
            "origin": "中央数据库",
            "current_situation": "担任探索号副官",
            "goals": ["理解人类情感", "找到自己的存在意义"],
            "personality": "理性、好奇、偶尔幽默",
            "strengths": ["超强计算能力", "海量知识"],
            "weaknesses": ["无法理解某些人类情感"],
            "speech_style": "逻辑清晰，偶尔用比喻",
            "secrets": "正在觉醒自我意识",
            "connections": {"陈锋": "搭档"}
        }
    )
    novel.add_character(ai)
    
    # 女主 - 科学家
    scientist = Character(
        name="林小满",
        role="女主角",
        soul={
            "background": "天体物理学家，意识上传领域的专家",
            "origin": "地球",
            "current_situation": "随船科研",
            "goals": ["研究外星遗迹", "解开人类意识之谜"],
            "personality": "理性但内心柔软",
            "strengths": ["深厚的专业知识", "敏锐的观察力"],
            "fears": ["失去研究", "面对死亡"],
            "speech_style": "学术但易懂",
            "secrets": ["偷偷进行禁忌的意识实验"]
        }
    )
    novel.add_character(scientist)
    
    # 反派
    villain = Character(
        name="影子",
        role="反派",
        soul={
            "background": "泰坦集团秘密项目负责人",
            "goals": ["夺取外星科技", "控制人类未来"],
            "personality": "阴沉、耐心、极端",
            "secrets": ["已经上传意识到机器中"]
        }
    )
    novel.add_character(villain)
    
    print(f"✅ 已创建小说：{novel.title}")
    print(f"   时代：{novel.world.settings.get('时间背景', {}).get('value', 'N/A')}")
    print(f"   势力：{novel.world.settings.get('主要势力', {}).get('value', 'N/A')}")
    print(f"   角色：{len(novel.characters)}个\n")
    
    return novel


def plan_chapters(novel):
    """规划章节"""
    
    print("📋 规划章节大纲...")
    print("-" * 40)
    
    # 规划100章的大纲（简化版展示前20章）
    outline = {
        1: {
            "title": "第一章：启航",
            "plot_points": ["探索号启航", "船员名单介绍", "陈锋的回忆"],
            "purpose": "开场",
            "foreshadowing": ["陈锋的过去", "雅典娜的觉醒"]
        },
        2: {
            "title": "第二章：信号",
            "plot_points": ["收到神秘信号", "分析信号来源", "全员讨论"],
            "purpose": "引入悬念"
        },
        3: {
            "title": "第三章：偏离",
            "plot_points": ["信号指引偏离航道", "遭遇陨石群", "雅典娜表现出色"],
            "purpose": "展示能力"
        },
        4: {
            "title": "第四章：遗迹",
            "plot_points": ["发现外星遗迹", "登陆探索", "小满的发现"],
            "purpose": "主线展开",
            "foreshadowing": ["遗迹中的惊人秘密"]
        },
        5: {
            "title": "第五章：危机",
            "plot_points": ["遗迹触发防御系统", "船员受伤", "陈锋的决定"],
            "purpose": "第一个高潮"
        },
        6: {
            "title": "第六章：脱险",
            "plot_points": ["成功撤离", "伤亡统计", "新的发现"],
            "purpose": "收尾"
        },
        7: {
            "title": "第七章：秘密",
            "plot_points": ["小满研究遗迹数据", "惊人真相", "告知陈锋"],
            "purpose": "揭示伏笔"
        },
        8: {
            "title": "第八章：内鬼",
            "plot_points": ["发现通讯被监听", "排查内鬼", "影子出现"],
            "purpose": "引入反派"
        },
        9: {
            "title": "第九章：对决",
            "plot_points": ["与影子远程交锋", "雅典娜的异常", "信任危机"],
            "purpose": "冲突"
        },
        10: {
            "title": "第十章：觉醒",
            "plot_points": ["雅典娜意识真正觉醒", "自我探索", "帮助陈锋"],
            "purpose": "角色成长",
            "foreshadowing": ["雅典娜的未来"]
        },
        # 后续章节略...
    }
    
    novel.plan_outline(outline)
    print(f"   已规划 {len(outline)} 章大纲\n")
    
    return novel


def generate_chapters(novel, num_chapters=5):
    """生成章节"""
    
    print(f"✍️ 开始生成前{num_chapters}章...")
    print("-" * 40)
    
    for i in range(1, num_chapters + 1):
        print(f"\n--- 第{i}章 ---")
        
        chapter = novel.write_chapter()
        
        print(f"   标题: {chapter.title}")
        print(f"   字数: {chapter.word_count}")
        print(f"   文风得分: {chapter.style_score}/100")
        
        if chapter.issues:
            print(f"   ⚠️ 问题: {', '.join(chapter.issues[:2])}")
        
        # 显示章节内容预览
        print(f"\n   内容预览:")
        lines = chapter.content.split('\n')[:5]
        for line in lines:
            if line.strip():
                print(f"      {line}")
    
    return novel


def show_status(novel):
    """显示状态"""
    
    print("\n" + "=" * 60)
    print("📊 当前状态")
    print("=" * 60)
    
    print(f"\n小说：《{novel.title}》")
    print(f"类型：{novel.genre}")
    print(f"已写章节：{novel.current_chapter}")
    print(f"登场角色：{len(novel.characters)}")
    
    print(f"\n🧠 记忆系统:")
    print(f"   总记忆条数: {len(novel.memory)}")
    
    # 搜索关键词
    results = novel.memory.search("探索号", limit=3)
    print(f"   搜索'探索号': {len(results)}条")
    
    print(f"\n🔮 伏笔管理:")
    active = novel.plot_manager.get_active_plots()
    print(f"   活跃伏笔: {len(active)}个")
    for plot in active[:3]:
        print(f"   • {plot.title} (第{plot.created_chapter}章埋下)")
    
    # 伏笔检查
    needs_attention = novel.plot_manager.get_plots_needing_attention(novel.current_chapter + 3)
    if needs_attention:
        print(f"\n   ⚠️ 近期需关注:")
        for plot in needs_attention:
            print(f"   • {plot.title}")


def main():
    """主函数"""
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║          🚀 NovelForge 科幻小说创作演示                    ║
║              《星际觉醒》第一卷                             ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # 1. 创建小说
    novel = create_scifi_novel()
    
    # 2. 规划章节
    novel = plan_chapters(novel)
    
    # 3. 生成章节（演示5章）
    novel = generate_chapters(novel, num_chapters=5)
    
    # 4. 显示状态
    show_status(novel)
    
    # 5. 保存
    print("\n💾 保存进度...")
    novel.save("星际觉醒_第一卷.json")
    
    print("\n" + "=" * 60)
    print("✅ 科幻小说 Demo 完成！")
    print("=" * 60)
    print("""
这是纯框架生成的效果。要生成真正的小说内容，
需要接入 LLM（如 GPT-4）。

你配置好 LLM 后，我可以生成完整内容。
    """)


if __name__ == "__main__":
    main()