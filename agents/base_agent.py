#!/usr/bin/env python3
"""
Agent基类 - 提供通用的API调用和工具方法
"""

import json
import urllib.request
import time
from typing import Dict, Any, Optional
import re

# 从配置文件导入配置
from config import VOLC_CONFIG


class BaseAgent:
    """所有Agent的基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.volc_config = config.get("volc_config", {})
        
    def log(self, message: str):
        """统一的日志输出"""
        agent_name = self.__class__.__name__
        print(f"  🤖 {agent_name}: {message}")
    
    def call_volc_api(self, payload: Dict[str, Any], max_retries: int = 3) -> Dict[str, Any]:
        """调用火山引擎API（带重试机制）"""
        # 优先使用实例配置，否则使用全局配置
        api_url = self.volc_config.get("api_base", VOLC_CONFIG["api_base"])
        api_key = self.volc_config.get("api_key", VOLC_CONFIG["api_key"])
        model = self.volc_config.get("model", VOLC_CONFIG["model"])
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": api_key
        }
        
        # 确保payload中有模型信息
        if "model" not in payload:
            payload["model"] = model
        
        for attempt in range(max_retries):
            try:
                data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
                req = urllib.request.Request(
                    url=api_url,
                    data=data,
                    headers=headers,
                    method='POST'
                )
                
                with urllib.request.urlopen(req, timeout=300) as response:
                    response_data = response.read().decode('utf-8')
                    result = json.loads(response_data)
                    
                    if "choices" in result and len(result["choices"]) > 0:
                        return result
                    else:
                        self.log(f"API响应格式异常 (尝试 {attempt+1}/{max_retries})")
                        if attempt < max_retries - 1:
                            time.sleep(2 ** attempt)  # 指数退避
                            continue
                        else:
                            return {"error": "无效的API响应格式"}
                            
            except urllib.error.HTTPError as e:
                error_msg = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
                self.log(f"HTTP错误 {e.code} (尝试 {attempt+1}/{max_retries}): {error_msg[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(3 ** attempt)
                    continue
                else:
                    return {"error": f"HTTP {e.code}: {error_msg[:200]}"}
                    
            except Exception as e:
                self.log(f"网络错误 (尝试 {attempt+1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    return {"error": f"网络错误: {str(e)}"}
        
        return {"error": "超过最大重试次数"}
    
    def extract_json_from_response(self, content: str) -> Optional[Dict[str, Any]]:
        """从响应内容中提取JSON"""
        try:
            # 尝试直接解析
            return json.loads(content)
        except json.JSONDecodeError:
            # 尝试提取JSON部分
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
            
            # 尝试修复常见的JSON问题
            content = re.sub(r'^```json\n?', '', content)
            content = re.sub(r'\n?```$', '', content)
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            
            try:
                return json.loads(content)
            except:
                self.log("JSON解析失败")
                return None
    
    def validate_response(self, response: Dict[str, Any], required_fields: list) -> bool:
        """验证API响应是否包含必要字段"""
        if "error" in response:
            self.log(f"API错误: {response['error']}")
            return False
        
        if "choices" not in response or len(response["choices"]) == 0:
            self.log("API响应中没有choices字段")
            return False
        
        return True