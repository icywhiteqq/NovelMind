"""
Configuration for NovelMind
"""
import os


class Config:
    """LLM 配置 - 在这里修改你的API Key"""
    
    # ===== 在这里填入你的 API Key =====
    LLM_API_KEY = "sk-YOUR-KEY-HERE"  # 替换成你的key
    LLM_BASE_URL = os.environ.get("LLM_BASE_URL", os.environ.get("OPENAI_API_BASE", "https://yunai.chat/v1"))
    LLM_MODEL = "gpt-4o-mini"  # 可用: gpt-4o, gpt-4o-mini, claude-3.5-sonnet 等
    LLM_TEMPERATURE = 0.8
    LLM_MAX_TOKENS = 4000
    
    # 可用模型列表
    AVAILABLE_MODELS = {
        "qwen3vl": "qwen3vl",
        "deepseek-r1": "deepseek-r1",
        "deepseek-v3": "deepseek-v3",
        "qwen3coder": "qwen3coder",
    }