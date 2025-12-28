#!/usr/bin/env python3
"""
配置文件 - 存储所有敏感信息和系统配置
"""

# 火山引擎API配置
VOLC_CONFIG = {
    "api_base": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "api_key": "Bearer place-your-api-key-here",
    "model": "deepseek-v3-2-251201"
}

# 系统配置
SYSTEM_CONFIG = {
    "default_genre": "玄幻",
    "default_chapters": 50,
    "output_dir": "./outputs",
    "max_retries": 3
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}