"""
NovelForge Demo - 完整章节生成流程演示
"""

from novelforge import (
    Novel, Character, 
    StyleProfile, PresetStyles, StyleAnalyzer
)


def demo_full_workflow():
    """演示完整的写小说流程"""
    
    print("=" * 70)
    print("🖊️ NovelForge 完整流程演示")
    print("=" * 70)
    
    # ===== 1. 创建小说 =====
    print("\n📖 1. 创建小说项目")
    print("-" * 40)
    
    novel = Novel(
        title="仙云纪",
        genre="仙侠",
        world_settings={
            "灵气体系": "五行灵气",
            "境界划分": "炼气→筑基→金丹→元婴→化神",
            "世界观": "修仙世界，门派林立"
        }
    )
    print(f"   创建成功: {novel}")
    
    # ===== 2. 设置文风 =====
    print("\n🎨 2. 设置文风（可选预设或自定义）")
    print("-" * 40)
    
    # 方式A: 使用预设
    style = PresetStyles.get_网文风格()
    novel.style = style
    print(f"   使用预设: {style.name}")
    print(f"   词汇等级: {style.vocabulary_level}/10")
    print(f"   情感强度: {style.emotional_tone}/10")
    print(f"   节奏: {'快' if style.pacing > 6 else '中等'}")
    
    # 方式B: 从示例学习（可选）
    # examples = ["你的文风示例文本..."]
    # style = StyleAnalyzer().analyze(examples)
    
    # ===== 3. 创建角色 =====
    print("\n👥 3. 创建角色（每个角色都有 SOUL）")
    print("-" * 40)
    
    # 主角
    protagonist = Character(
        name="林风",
        role="主角",
        soul={
            "background": "青云宗外门弟子，父母双亡",
            "origin": "偏远山村",
            "current_situation": "刚踏入修仙之路",
            "goals": ["找到灵根觉醒的方法", "进入内门"],
            "long_term_goals": ["成仙", "揭开灭门真相"],
            "fears": ["永远无法觉醒灵根", "失去师父"],
            "personality": "沉稳内敛，但关键时刻果断",
            "strengths": ["剑道天赋", "意志坚定"],
            "weaknesses": ["感情用事", "不善于表达"],
            "speech_style": "简洁有力，不多说废话",
            "habits": ["思考时抚摸剑柄", "喜欢独处"],
            "secrets": ["体内有上古血脉封印"],
            "hidden_past": "十年前的灭门惨案幸存者"
        }
    )
    novel.add_character(protagonist)
    print(f"   添加主角: {protagonist.name}")
    
    # 女主角
    heroine = Character(
        name="苏晴",
        role="女主角",
        soul={
            "background": "苏家千金，天之骄女",
            "origin": "修仙世家",
            "current_situation": "奉家族之命下山历练",
            "goals": ["找到合适的道侣", "振兴家族"],
            "personality": "活泼开朗，但有城府",
            "strengths": ["冰系天灵根", "家传功法"],
            "speech_style": "俏皮灵动",
            "secrets": ["体内有寒毒，每月发作"]
        }
    )
    novel.add_character(heroine)
    print(f"   添加女主: {heroine.name}")
    
    # 反派
    villain = Character(
        name="黑曜",
        role="反派",
        soul={
            "background": "堕入魔道的青云宗弃徒",
            "goals": ["报复青云宗", "夺取掌门之位"],
            "personality": "阴险狡诈，、城府极深",
            "secrets": ["暗中修炼禁术"]
        }
    )
    novel.add_character(villain)
    print(f"   添加反派: {villain.name}")
    
    # ===== 4. 规划章节大纲 =====
    print("\n📋 4. 规划章节大纲")
    print("-" * 40)
    
    # 批量规划
    novel.plan_outline({
        1: {
            "title": "第一章：下山",
            "plot_points": ["林风奉命下山", "偶遇苏晴", "发现敌踪"],
            "purpose": "开场",
            "foreshadowing": ["林风的血脉封印"]
        },
        2: {
            "title": "第二章：激战",
            "plot_points": ["遭遇黑曜", "危机关头血脉觉醒", "击退敌人"],
            "purpose": "展示主角能力",
            "foreshadowing": ["黑曜的阴谋"]
        },
        3: {
            "title": "第三章：结缘",
            "plot_points": ["与苏晴结伴而行", "苏晴的寒毒发作", "林风出手相救"],
            "purpose": "感情线",
            "foreshadowing": ["苏晴的秘密"]
        },
        10: {
            "title": "第十章：真相",
            "plot_points": ["揭露十年前灭门真相", "黑曜的真面目"],
            "purpose": "回收伏笔"
        }
    })
    print("   已规划 4 章大纲")
    
    # ===== 5. 生成章节 =====
    print("\n✍️ 5. 开始写章节")
    print("-" * 40)
    
    # 写第1章
    print("\n--- 正在写第1章 ---")
    chapter1 = novel.write_chapter()
    print(f"   章节: {chapter1.title}")
    print(f"   字数: {chapter1.word_count}")
    print(f"   文风得分: {chapter1.style_score}/100")
    
    # 写第2章
    print("\n--- 正在写第2章 ---")
    chapter2 = novel.write_chapter()
    print(f"   章节: {chapter2.title}")
    print(f"   字数: {chapter2.word_count}")
    print(f"   文风得分: {chapter2.style_score}/100")
    
    # 写第3章
    print("\n--- 正在写第3章 ---")
    chapter3 = novel.write_chapter()
    print(f"   章节: {chapter3.title}")
    print(f"   字数: {chapter3.word_count}")
    print(f"   文风得分: {chapter3.style_score}/100")
    
    # ===== 6. 检查伏笔 =====
    print("\n🔮 6. 伏笔状态检查")
    print("-" * 40)
    
    active = novel.plot_manager.get_active_plots()
    print(f"   活跃伏笔数: {len(active)}")
    for plot in active[:3]:
        print(f"   • {plot.title} (第{plot.created_chapter}章)")
    
    # 伏笔回收建议（第5章时）
    print("\n   第5章伏笔回收建议:")
    suggestions = novel.plot_manager.generate_reveal_suggestions(5)
    if suggestions:
        for s in suggestions:
            print(f"   • {s['title']}: {s['suggested_reveal']}")
    else:
        print("   暂无需要回收的伏笔")
    
    # ===== 7. 记忆系统 =====
    print("\n🧠 7. 记忆系统")
    print("-" * 40)
    
    print(f"   总记忆条数: {len(novel.memory)}")
    
    # 搜索相关记忆
    results = novel.memory.search("林风", limit=3)
    print(f"   搜索'林风'相关: {len(results)}条")
    
    # ===== 8. 保存进度 =====
    print("\n💾 8. 保存进度")
    print("-" * 40)
    
    novel.save()
    
    print("\n" + "=" * 70)
    print("✅ 完整流程演示结束!")
    print("=" * 70)
    print("""
这个 Demo 展示了 NovelForge 的核心能力：

📖 小说管理
   - 世界观设定、境界划分、势力设定
   - 章节规划、进度追踪

👥 角色系统
   - 每个角色有独立的 SOUL（背景、目标、性格、秘密）
   - 角色间关系追踪

🧠 记忆系统
   - 长期记忆，不会越写越乱
   - 向量级检索相关记忆

🎯 伏笔管理
   - 自动追踪所有伏笔
   - 适时提醒回收

🎨 文风控制
   - 预设文风（网文/传统/悬疑）
   - 自定义文风参数
   - 写完自动检查一致性

下一章想做什么？
1. 完善 LLM 对接（接入 GPT 生成真正内容）
2. 推送到 GitHub
3. 其他功能
""")


if __name__ == "__main__":
    demo_full_workflow()