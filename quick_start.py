#!/usr/bin/env python3
"""
快速启动脚本
"""

import sys
import os
from typing import Dict, Any, List, Optional  # 添加类型注解

# 从配置文件导入配置
from config import VOLC_CONFIG, SYSTEM_CONFIG

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def quick_test():
    """快速测试"""
    config = {
        "volc_config": VOLC_CONFIG,  # 从配置文件导入API配置
        "generation_config": {
            "default_genre": SYSTEM_CONFIG["default_genre"],
            "default_chapters": 3,  # 只测试3章
            "output_dir": "./test_outputs"
        }
    }
    
    print("🚀 快速测试 - 生成3章玄幻爽文")
    print("="*50)
    
    try:
        from main import ShuangNovelGenerator
        generator = ShuangNovelGenerator(config)
        result = generator.generate_novel(genre="玄幻", target_chapters=3)
        
        if result["success"]:
            print(f"\n✅ 测试成功！")
            print(f"📖 书名: {result['novel_info']['title']}")
            print(f"📊 章节: {result['novel_info']['total_chapters']}章")
            print(f"📝 字数: {result['novel_info']['total_words']:,}字")
            print(f"📁 路径: {result['novel_info']['output_path']}")
        else:
            print(f"❌ 测试失败: {result.get('error', '未知错误')}")
            
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请检查agents目录是否存在")
    except Exception as e:
        print(f"❌ 运行错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_test()