# 📖 NovelMind

用 AI 写长篇小说，让每个角色都是有灵魂的 Agent。

解决 AI 写长篇时的"失忆"、人设崩塌、伏笔丢失等核心痛点。

## ⭐ 特性

- 🧠 **长期记忆** - 角色记得之前所有章节的事，不会"失忆"
- 🎭 **角色灵魂** - 每个角色有独立性格、目标、秘密
- 🎯 **伏笔管理** - 自动追踪埋下的伏笔，适时回收
- 🌍 **世界统一** - 统一管理世界观，拒绝前后矛盾
- 🌐 **Web 界面** - 点点鼠标就能写小说

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/icywhiteqq/NovelMind.git
cd NovelMind
```

### 2. 配置 API Key

编辑 `novelforge/config.py`，填入你的 API Key：

```python
LLM_API_KEY = "sk-你的KEY"  # 换成你的key
LLM_BASE_URL = "https://api.openai.com/v1"  # 或其他兼容API
```

### 3. 启动 Web 界面

```bash
pip install streamlit openai
streamlit run app.py
```

然后打开浏览器 http://localhost:8501

### 4. 命令行运行

```bash
PYTHONPATH=. python examples/scifi_novel.py
```

## 📦 依赖

```
streamlit
openai
requests
```

## 🤝 欢迎 Star！

MIT License