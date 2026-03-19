# 🖊️ NovelForge

AI-Powered Long-Form Novel Writing with Autonomous Characters

NovelForge is an innovative framework for writing long novels with AI agents. Each character is an autonomous agent with their own soul, memory, and goals. The system solves the core problems of AI novel writing:

- 🔮 **Long-term Memory** — Characters remember everything, even chapters later
- 🎯 **Foreshadowing & Payoff** — Built-in plot threading for callbacks
- 🎭 **Autonomous Characters** — Each character is an agent with distinct personality
- 📖 **Consistent World** — World state management across chapters

## ✨ Features

- **Character Agents** — Each character is an autonomous AI agent with their own SOUL (Personality, Goals, Memories)
- **Memory System** — Powered by AgentScope, with vector storage for semantic search
- **Plot Threading** — Track foreshadowing and ensure callbacks
- **World State** — Consistent world-building across the entire novel
- **Chapter Planning** — AI-assisted plot outline generation
- **Multi-Agent Collaboration** — Characters interact and influence each other

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      NovelForge                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │  World Manager  │  │  Plot Manager   │                  │
│  │  (世界设定)      │  │  (情节规划+伏笔)  │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Memory System (AgentScope)             │   │
│  │  - Character Memories    - Plot Threads             │   │
│  │  - World State           - Chapter History          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Character│ │ Character│ │ Character│ │ Character│      │
│  │  Agent   │ │  Agent   │ │  Agent   │ │  Agent   │      │
│  │ (主角A)  │ │ (主角B)  │ │ (反派)   │ │ (配角)   │      │
│  │  SOUL    │ │  SOUL    │ │  SOUL    │ │  SOUL    │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│                         ↓                                   │
│              ┌──────────────────┐                          │
│              │  Narrative Agent │                          │
│              │   (叙事润色)       │                          │
│              └──────────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

```python
from novelforge import Novel, Character

# Create a novel
novel = Novel(
    title="我的小说",
    genre="奇幻",
    world_settings={"魔法体系": "五行元素", "世界观": "仙侠世界"}
)

# Create characters with SOUL
protagonist = Character(
    name="李云",
    role="主角",
    soul={
        "personality": "沉稳内敛，但关键时刻果断",
        "goals": "拯救宗门，找出灭门真相",
        "secrets": "体内藏有上古血脉"
    }
)
novel.add_character(protagonist)

# Generate a chapter
chapter = novel.write_chapter(
    title="第一章：下山",
    plot_points=["李云初次下山", "遭遇神秘少女", "发现仇家线索"]
)
print(chapter)
```

## 📖 Documentation

Full documentation coming soon. For now, check the examples in `examples/`.

## 🤝 Contributing

Contributions welcome! Please read our Contributing Guide.

## 📝 License

MIT License.

---

<p align="center">
  Made with ❤️ by NovelForge Team
</p>