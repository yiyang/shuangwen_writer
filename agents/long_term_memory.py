#!/usr/bin/env python3
"""
长期记忆 Agent - 维护故事连续性
"""

import json
import re
from typing import Dict, Any, List
from .base_agent import BaseAgent


class LongTermMemoryAgent(BaseAgent):
    """长期记忆 - 维护人物状态、情节连续性、伏笔回收"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.memory = self._initialize_memory()
    
    def _initialize_memory(self) -> Dict[str, Any]:
        """初始化记忆系统"""
        return {
            "current_state": {
                "main_character": {
                    "name": "",
                    "level": "",
                    "cultivation": "",
                    "golden_finger_unlocked": [],
                    "relationships": {},
                    "enemies_defeated": [],
                    "treasures_obtained": [],
                    "current_location": "",
                    "reputation": 0
                },
                "world_status": {
                    "time_passed": 0,
                    "major_events": [],
                    "foreshadowing": [],  # 埋下的伏笔
                    "callback_opportunities": []  # 可回收的伏笔
                }
            },
            "character_status": {},  # 所有角色状态
            "plot_threads": [],  # 未解决的剧情线
            "callback_reminders": []  # 需要回收的伏笔提醒
        }
    
    def initialize_story(self, world_info: Dict[str, Any], character_info: Dict[str, Any]):
        """初始化故事记忆"""
        self.log("初始化故事记忆...")
        
        self.memory["current_state"]["main_character"] = {
            "name": character_info.get("name", "叶凡"),
            "level": "凡人",  # 初始境界
            "cultivation": 0,
            "golden_finger_unlocked": [character_info.get("hidden_identity", "")],
            "relationships": {},
            "enemies_defeated": [],
            "treasures_obtained": [],
            "current_location": "起始地点",
            "reputation": 0
        }
        
        # 初始化角色关系
        for love_interest in character_info.get("love_interests", []):
            self.memory["character_status"][love_interest["name"]] = {
                "relationship": "acquaintance",
                "affection": 30,
                "last_interaction": 0,
                "status": "alive"
            }
        
        for enemy in character_info.get("enemies", []):
            self.memory["character_status"][enemy["name"]] = {
                "relationship": "enemy",
                "hatred": 80,
                "last_interaction": 0,
                "status": "alive"
            }
        
        self.log(f"✅ 记忆初始化完成: {character_info.get('name')}的故事开始")
    
    def update_after_chapter(self, chapter_content: str, chapter_number: int, 
                           chapter_plan: Dict[str, Any]) -> Dict[str, Any]:
        """分析章节内容，更新记忆"""
        self.log(f"更新第{chapter_number}章记忆...")
        
        # 提取关键信息
        level_up = self._extract_level_up(chapter_content)
        new_enemies = self._extract_new_enemies(chapter_content)
        new_treasures = self._extract_new_treasures(chapter_content)
        new_foreshadowing = self._extract_foreshadowing(chapter_content)
        location_change = self._extract_location_change(chapter_content)
        relationship_changes = self._extract_relationship_changes(chapter_content)
        
        # 更新主角状态
        if level_up:
            self.memory["current_state"]["main_character"]["level"] = level_up
            self.memory["current_state"]["main_character"]["cultivation"] += 1
        
        if new_enemies:
            self.memory["current_state"]["main_character"]["enemies_defeated"].extend(new_enemies)
        
        if new_treasures:
            self.memory["current_state"]["main_character"]["treasures_obtained"].extend(new_treasures)
        
        if location_change:
            self.memory["current_state"]["main_character"]["current_location"] = location_change
        
        # 更新世界状态
        self.memory["current_state"]["world_status"]["time_passed"] += 1
        self.memory["current_state"]["world_status"]["major_events"].append({
            "chapter": chapter_number,
            "event": chapter_plan.get("main_shuang", ""),
            "impact": "medium"
        })
        
        # 更新伏笔系统
        if new_foreshadowing:
            self.memory["current_state"]["world_status"]["foreshadowing"].extend(new_foreshadowing)
        
        # 检查伏笔回收机会
        self._check_callback_opportunities(chapter_number)
        
        # 更新角色关系
        self._update_relationships(relationship_changes, chapter_number)
        
        self.log(f"✅ 第{chapter_number}章记忆更新完成")
        return self.memory["current_state"]
    
    def _extract_level_up(self, content: str) -> str:
        """提取境界提升信息"""
        level_patterns = [
            r'突破.*?(境界|层级)',
            r'晋升.*?期',
            r'达到.*?境界',
            r'进阶.*?层'
        ]
        
        for pattern in level_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return matches[0]
        
        return ""
    
    def _extract_new_enemies(self, content: str) -> List[str]:
        """提取新击败的敌人"""
        enemy_patterns = [
            r'击败.*?[，。]',
            r'战胜.*?[，。]', 
            r'打脸.*?[，。]',
            r'碾压.*?[，。]'
        ]
        
        enemies = []
        for pattern in enemy_patterns:
            matches = re.findall(pattern, content)
            enemies.extend(matches)
        
        return enemies[:3]  # 最多记录3个
    
    def _extract_new_treasures(self, content: str) -> List[str]:
        """提取新获得的宝物"""
        treasure_patterns = [
            r'获得.*?[，。]',
            r'得到.*?[，。]',
            r'收获.*?[，。]',
            r'捡到.*?[，。]'
        ]
        
        treasures = []
        for pattern in treasure_patterns:
            matches = re.findall(pattern, content)
            treasures.extend(matches)
        
        return treasures[:5]  # 最多记录5个
    
    def _extract_foreshadowing(self, content: str) -> List[Dict[str, Any]]:
        """提取新埋下的伏笔"""
        foreshadowing_keywords = ['秘密', '真相', '谜团', '奇怪', '异常', '神秘', '隐藏', '背后']
        foreshadowing = []
        
        sentences = re.split(r'[。！？!?]', content)
        for sentence in sentences:
            if any(keyword in sentence for keyword in foreshadowing_keywords):
                foreshadowing.append({
                    "content": sentence.strip(),
                    "type": "mystery",
                    "severity": "medium",
                    "chapter_introduced": self.memory["current_state"]["world_status"]["time_passed"] + 1
                })
        
        return foreshadowing[:3]  # 最多记录3个
    
    def _extract_location_change(self, content: str) -> str:
        """提取地点变化"""
        location_patterns = [
            r'来到.*?[，。]',
            r'进入.*?[，。]',
            r'到达.*?[，。]',
            r'前往.*?[，。]'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return matches[0].replace('，', '').replace('。', '')
        
        return ""
    
    def _extract_relationship_changes(self, content: str) -> List[Dict[str, Any]]:
        """提取关系变化"""
        relationship_patterns = {
            "improve": [r'结交.*?[，。]', r'结识.*?[，。]', r'收服.*?[，。]'],
            "worsen": [r'得罪.*?[，。]', r'结仇.*?[，。]', r'激怒.*?[，。]']
        }
        
        changes = []
        for change_type, patterns in relationship_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    changes.append({
                        "type": change_type,
                        "description": match,
                        "target": self._extract_character_name(match)
                    })
        
        return changes
    
    def _extract_character_name(self, text: str) -> str:
        """从文本中提取角色名"""
        # 简单的角色名提取逻辑
        name_pattern = r'[叶林苏陈王李张赵刘周杨吴][\u4e00-\u9fa5]{1,2}'
        matches = re.findall(name_pattern, text)
        return matches[0] if matches else "未知角色"
    
    def _check_callback_opportunities(self, current_chapter: int):
        """检查伏笔回收机会"""
        foreshadowing = self.memory["current_state"]["world_status"]["foreshadowing"]
        callback_opportunities = []
        
        for i, f in enumerate(foreshadowing):
            chapters_passed = current_chapter - f["chapter_introduced"]
            
            # 如果伏笔埋下超过5章，建议回收
            if chapters_passed >= 5:
                callback_opportunities.append({
                    "foreshadowing": f,
                    "chapters_passed": chapters_passed,
                    "suggested_chapter": current_chapter + 1
                })
        
        self.memory["current_state"]["world_status"]["callback_opportunities"] = callback_opportunities
    
    def _update_relationships(self, changes: List[Dict[str, Any]], chapter_number: int):
        """更新角色关系"""
        for change in changes:
            char_name = change["target"]
            if char_name not in self.memory["character_status"]:
                self.memory["character_status"][char_name] = {
                    "relationship": "neutral",
                    "affection": 50,
                    "last_interaction": chapter_number,
                    "status": "alive"
                }
            
            if change["type"] == "improve":
                self.memory["character_status"][char_name]["affection"] += 20
            else:  # worsen
                self.memory["character_status"][char_name]["affection"] -= 20
            
            self.memory["character_status"][char_name]["last_interaction"] = chapter_number
    
    def get_current_context(self) -> Dict[str, Any]:
        """获取当前记忆上下文"""
        return {
            "current_state": self.memory["current_state"],
            "callback_opportunities": self.memory["current_state"]["world_status"]["callback_opportunities"],
            "active_plot_threads": self._get_active_plot_threads(),
            "character_status": self.memory["character_status"]
        }
    
    def _get_active_plot_threads(self) -> List[Dict[str, Any]]:
        """获取活跃的剧情线"""
        active_threads = []
        
        # 未击败的敌人
        enemies = [char for char, status in self.memory["character_status"].items() 
                  if status.get("relationship") == "enemy" and status.get("status") == "alive"]
        if enemies:
            active_threads.append({
                "type": "revenge",
                "targets": enemies,
                "priority": "high"
            })
        
        # 未回收的伏笔
        if self.memory["current_state"]["world_status"]["foreshadowing"]:
            active_threads.append({
                "type": "mystery",
                "count": len(self.memory["current_state"]["world_status"]["foreshadowing"]),
                "priority": "medium"
            })
        
        return active_threads
    
    def suggest_next_chapter_focus(self, chapter_number: int) -> Dict[str, Any]:
        """建议下一章的重点"""
        context = self.get_current_context()
        suggestions = {
            "priority": "medium",
            "focus": "continue_main_plot",
            "suggested_elements": [],
            "callback_opportunities": []
        }
        
        # 检查是否有需要回收的伏笔
        if context["callback_opportunities"]:
            suggestions["focus"] = "callback_resolution"
            suggestions["callback_opportunities"] = context["callback_opportunities"][:2]  # 最多2个
            suggestions["priority"] = "high"
        
        # 每10章建议一个大高潮
        if chapter_number % 10 == 0:
            suggestions["focus"] = "major_climax"
            suggestions["priority"] = "high"
            suggestions["suggested_elements"].append("大型战斗/重大发现")
        
        # 每3章建议一个关系发展
        elif chapter_number % 3 == 0:
            suggestions["focus"] = "relationship_development"
            suggestions["suggested_elements"].append("收服新角色/发展感情线")
        
        return suggestions