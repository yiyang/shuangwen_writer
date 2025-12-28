#!/usr/bin/env python3
"""
章节生成师 Agent - 完全重写，确保生成对话
"""

import json
import re
import time
from typing import Dict, Any, List
from .base_agent import BaseAgent


class ChapterWriterAgent(BaseAgent):
    """章节生成师 - 强制要求生成包含对话的章节"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
    
    def write_chapter(self, chapter_plan: Dict[str, Any], 
                     memory_context: Dict[str, Any],
                     chapter_number: int) -> str:
        """生成具体章节内容 - 强制要求对话"""
        self.log(f"生成第{chapter_number}章: {chapter_plan.get('title', '')}")
        
        main_char = memory_context.get("character_info", {}).get("name", "叶凡")
        
        # 构建强制对话的提示词
        prompt = self._build_dialogue_enforced_prompt(chapter_plan, memory_context, chapter_number)
        
        # 尝试生成，必须包含对话
        for attempt in range(5):  # 增加尝试次数
            self.log(f"生成尝试 {attempt+1}/5")
            content = self._generate_with_dialogue(prompt, main_char)
            
            if content and self._has_sufficient_dialogue(content):
                dialogue_count = self._count_dialogue(content)
                self.log(f"✅ 生成成功: {len(content)}字, {dialogue_count}段对话")
                return content
            
            time.sleep(1)  # 等待后重试
        
        # 如果所有尝试都失败，使用强制注入对话的生成
        self.log("⚠️ 所有尝试失败，使用强制对话生成")
        return self._generate_with_forced_dialogue(chapter_plan, memory_context, chapter_number)
    
    def _build_dialogue_enforced_prompt(self, chapter_plan: Dict[str, Any],
                                      memory_context: Dict[str, Any],
                                      chapter_number: int) -> str:
        """构建强制对话的提示词"""
        main_char = memory_context.get("character_info", {}).get("name", "叶凡")
        
        return f"""# 指令：你必须写一段网络爽文的第{chapter_number}章

## 章节信息
标题：{chapter_plan.get('title', '')}
主要爽点：{chapter_plan.get('main_shuang', '')}
次要爽点：{', '.join(chapter_plan.get('secondary_shuangs', []))}
章末钩子：{chapter_plan.get('ending_hook', '')}

## 硬性要求（必须遵守！）
1. **必须有至少3段完整对话**，用双引号""包裹
2. 每段对话必须推动情节发展
3. 开头必须有冲突对话
4. 中间必须有打脸对话
5. 结尾可以有系统提示或悬念对话

## 对话格式示例
反派："你这个废物，也敢上台？"
主角："三招之内，让你跪地求饶。"
系统：【叮！打脸任务完成，奖励发放】

## 情节要求
1. 开头：用对话直接进入冲突
2. 发展：主角展现实力，反派震惊
3. 高潮：主角打脸成功，获得奖励
4. 结尾：留下悬念，为下一章铺垫

## 字数要求
3000字左右，短段落，多对话，少描述

## 立即开始写作，必须包含对话！"""

    def _generate_with_dialogue(self, prompt: str, main_char: str) -> str:
        """生成带对话的内容"""
        payload = {
            "model": self.volc_config.get("model", "deepseek-v3-2-251201"),
            "messages": [
                {"role": "system", "content": "你是一个必须写对话的爽文作家。不写对话就是失败！"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 4000
        }
        
        response = self.call_volc_api(payload)
        
        if not self.validate_response(response, ["choices"]):
            return ""
        
        try:
            content = response["choices"][0]["message"]["content"].strip()
            return self._clean_chapter_content(content)
        except:
            return ""
    
    def _has_sufficient_dialogue(self, content: str) -> bool:
        """检查是否有足够的对话"""
        dialogue_patterns = [
            r'["]([^"]+)["]',  # 英文引号
            r'[""]([^""]+)[""]',  # 双引号
            r'["「]([^"」]+)["」]',  # 中文引号
            r'[\u4e00-\u9fa5]+(?:道|说|问|答|喊|喝|骂)[:：]\s*[^。？！]+[。？！]'  # XX说：对话
        ]
        
        total_dialogue = 0
        for pattern in dialogue_patterns:
            matches = re.findall(pattern, content)
            total_dialogue += len(matches)
        
        return total_dialogue >= 2  # 至少2段对话
    
    def _count_dialogue(self, content: str) -> int:
        """统计对话段数"""
        patterns = [r'["]([^"]+)["]', r'[""]([^""]+)[""]']
        total = 0
        for pattern in patterns:
            total += len(re.findall(pattern, content))
        return total
    
    def _generate_with_forced_dialogue(self, chapter_plan: Dict[str, Any],
                                     memory_context: Dict[str, Any],
                                     chapter_number: int) -> str:
        """强制注入对话生成"""
        main_char = memory_context.get("character_info", {}).get("name", "叶凡")
        
        # 先获取基本内容
        basic_prompt = f"""写第{chapter_number}章：{chapter_plan.get('title', '')}
内容：{chapter_plan.get('main_shuang', '')}
3000字左右"""
        
        payload = {
            "model": self.volc_config.get("model", "deepseek-v3-2-251201"),
            "messages": [
                {"role": "user", "content": basic_prompt}
            ],
            "max_tokens": 3000
        }
        
        response = self.call_volc_api(payload)
        
        if not self.validate_response(response, ["choices"]):
            content = ""
        else:
            content = response["choices"][0]["message"]["content"].strip()
        
        # 如果没有对话，强制添加对话
        if not self._has_sufficient_dialogue(content):
            content = self._inject_dialogue(content, main_char, chapter_plan)
        
        return content
    
    def _inject_dialogue(self, content: str, main_char: str, chapter_plan: Dict[str, Any]) -> str:
        """强制注入对话"""
        dialogue_template = f'''"就凭你们，也配拦我？" {main_char}冷冷地看着面前的几人。

"小子，你很狂啊？"一个满脸横肉的大汉狞笑着走上前。

"狂不狂，试试就知道。" {main_char}微微一笑。

大汉怒吼一声，一拳轰出。拳风呼啸，气势惊人。

但{main_char}只是轻轻一侧身，就躲过了这致命一击。

"什么？"大汉大惊，"这不可能！"

"就这点实力？" {main_char}摇了摇头，"该我了。"

话音未落，{main_char}的身影突然消失。

下一刻，他已经出现在大汉身后。

砰！一声闷响，大汉倒飞出去，重重摔在地上。

【叮！系统提示：恭喜宿主完成{chapter_plan.get('main_shuang', '打脸')}，获得奖励】'''

        # 将对话插入到内容开头
        if content:
            return dialogue_template + "\n\n" + content
        return dialogue_template
    
    def _clean_chapter_content(self, content: str) -> str:
        """清理章节内容"""
        # 移除可能的标题
        content = re.sub(r'^第[一二三四五六七八九十\d]+章\s*[:：]?\s*', '', content)
        content = re.sub(r'^章节\s*[:：]?\s*', '', content)
        content = re.sub(r'^标题\s*[:：]?\s*', '', content)
        return content.strip()