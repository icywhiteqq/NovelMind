"""
Configuration for NovelForge
"""


class Config:
    """LLM 配置 - 在这里修改你的API Key"""
    
    # ===== 在这里填入你的 API Key =====
    LLM_API_KEY = "sk-YOUR-KEY-HERE"  # 替换成你的key
    LLM_BASE_URL = "https://models.sjtu.edu.cn/api/v1"  # API地址
    LLM_MODEL = "minimax-m2.5"
    LLM_TEMPERATURE = 0.8
    LLM_MAX_TOKENS = 4000
    
    # 可用模型列表
    AVAILABLE_MODELS = {
        "minimax-m2.5": "minimax-m2.5",
        "gpt-4o": "gpt-4o",
        "gpt-4": "gpt-4",
        "gpt-3.5-turbo": "gpt-3.5-turbo",
    }