"""
LLM client wrapper - 使用 requests 直接调用
"""
import json
import os
import time
from typing import Dict, Any, Optional
import requests
from .config import Config
from .utils.logger import log


class LLMClient:
    """LLM API 调用"""
    
    def __init__(self):
        self.api_key = Config.LLM_API_KEY
        self.base_url = Config.LLM_BASE_URL
        self.model = Config.LLM_MODEL
        self.temperature = Config.LLM_TEMPERATURE
        self.max_tokens = Config.LLM_MAX_TOKENS
    
    def call(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """调用 LLM API"""
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens
        }
        
        # 重试3次
        for attempt in range(3):
            try:
                log.info(f"Calling LLM API: model={self.model}, attempt {attempt+1}")
                r = requests.post(url, headers=headers, json=data, timeout=60)
                r.raise_for_status()
                result = r.json()
                content = result["choices"][0]["message"]["content"]
                log.info(f"LLM API call successful, response length: {len(content)}")
                return content
            except Exception as e:
                log.warning(f"LLM API call failed: {e}, attempt {attempt+1}/3")
                if attempt < 2:
                    time.sleep(2)
                else:
                    raise
    
    def call_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """调用 LLM API 并解析 JSON"""
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or self.temperature,
            "max_tokens": self.max_tokens,
            "response_format": {"type": "json_object"}
        }
        
        try:
            r = requests.post(url, headers=headers, json=data, timeout=60)
            r.raise_for_status()
            result = r.json()
            return json.loads(result["choices"][0]["message"]["content"])
        except Exception as e:
            log.error(f"LLM JSON call failed: {e}")
            raise


# 全局实例
llm_client = LLMClient()