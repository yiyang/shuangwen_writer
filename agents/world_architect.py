#!/usr/bin/env python3
"""
世界观架构师 Agent - 负责构建爽文世界观
"""

import json
import random
from typing import Dict, Any
from .base_agent import BaseAgent


class WorldArchitectAgent(BaseAgent):
    """世界观架构师 - 构建完整的爽文世界观体系"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.genre_templates = self._load_genre_templates()
    
    def _load_genre_templates(self) -> Dict[str, Any]:
        """加载世界观模板"""
        return {
            "玄幻": {
                "level_system": ["凡人", "练气", "筑基", "金丹", "元婴", "化神", "炼虚", "合体", "大乘", "渡劫", "真仙", "仙王", "仙帝"],
                "golden_fingers": ["万界签到系统", "老爷爷残魂", "重生记忆", "神器认主", "特殊血脉"],
                "core_conflicts": ["家族被灭", "宗门被毁", "女友背叛", "身世之谜", "夺舍危机"],
                "key_scenes": ["退婚现场", "拍卖会", "宗门大比", "秘境探险", "丹道大会"]
            },
            "都市": {
                "level_system": ["明劲", "暗劲", "化劲", "宗师", "大宗师", "先天", "筑基", "金丹"],
                "golden_fingers": ["神级选择系统", "医术传承", "透视眼", "未来记忆", "超能力觉醒"],
                "core_conflicts": ["家族弃子", "女友被抢", "商业打压", "身份暴露", "强敌追杀"],
                "key_scenes": ["同学聚会", "商业谈判", "地下拳场", "医院救人", "拍卖会"]
            },
            "游戏": {
                "level_system": ["黑铁", "青铜", "白银", "黄金", "铂金", "钻石", "大师", "宗师", "王者"],
                "golden_fingers": ["全知全能系统", "隐藏职业", "神级天赋", "未来攻略", "BUG利用"],
                "core_conflicts": ["账号被删", "队友背叛", "公会打压", "现实威胁", "游戏入侵"],
                "key_scenes": ["新手村", "副本开荒", "竞技场", "世界BOSS", "公会战"]
            }
        }
    
    def design_world(self, genre: str = "玄幻") -> Dict[str, Any]:
        """设计爽文世界观"""
        self.log(f"开始设计{genre}世界观...")
        
        if genre not in self.genre_templates:
            genre = "玄幻"  # 默认使用玄幻
        
        template = self.genre_templates[genre]
        
        prompt = f"""你是一位顶级的网络爽文世界观架构师，请为{genre}小说设计完整的世界观：

【核心要求】
1. 必须有明确的等级体系（至少9个大境界，体现力量差距）
2. 必须有独特的"金手指"设定（系统、传承、重生等）
3. 必须有能激起读者愤怒的核心矛盾
4. 必须设计至少3个经典的装逼打脸场景

【{genre}特色元素】
- 等级压制：高境界对低境界的绝对优势
- 扮猪吃虎：主角隐藏实力的经典套路  
- 奇遇不断：秘境、传承、拍卖会等机遇
- 势力斗争：宗门、家族、国家间的博弈

【输出格式】
必须严格返回JSON格式：
{{
    "title": "小说标题（必须包含'帝'、'神'、'尊'、'圣'等霸气字眼）",
    "genre": "{genre}",
    "world_view": "世界观描述（200字内，要吸引人）",
    "level_system": {json.dumps(template["level_system"][:10], ensure_ascii=False)},
    "golden_finger": "金手指设定（要新颖有趣）",
    "core_conflict": "核心矛盾（要让读者愤怒）",
    "key_scenes": ["场景1", "场景2", "场景3"],
    "special_rules": ["世界特殊规则1", "特殊规则2"]
}}

示例标题：'万古仙帝'、'神级选择系统'、'我真是大魔王'"""

        payload = {
            "model": self.volc_config.get("model", "deepseek-v3-2-251201"),
            "messages": [
                {"role": "system", "content": "你是专业的网络爽文世界观架构师，严格只输出JSON格式"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8
        }
        
        response = self.call_volc_api(payload)
        
        if not self.validate_response(response, ["choices"]):
            return self._create_fallback_world(genre)
        
        try:
            content = response["choices"][0]["message"]["content"].strip()
            world_data = self.extract_json_from_response(content)
            
            if world_data and all(key in world_data for key in ["title", "world_view", "level_system"]):
                self.log(f"✅ 世界观设计完成: {world_data['title']}")
                return world_data
            else:
                self.log("❌ 世界观数据不完整，使用备用方案")
                return self._create_fallback_world(genre)
                
        except Exception as e:
            self.log(f"世界观解析错误: {str(e)}")
            return self._create_fallback_world(genre)
    
    def _create_fallback_world(self, genre: str) -> Dict[str, Any]:
        """创建备用世界观"""
        self.log("使用备用世界观方案")
        
        templates = {
            "玄幻": {
                "title": "万古仙帝",
                "genre": "玄幻",
                "world_view": "这是一个以武为尊的世界，强者可翻江倒海，弱者如蝼蚁。主角叶凡本是天骄，却因一场阴谋沦为废人，获得神秘系统后开始逆袭之路。",
                "level_system": ["凡人", "练气", "筑基", "金丹", "元婴", "化神", "炼虚", "合体", "大乘", "渡劫", "真仙", "仙王", "仙帝"],
                "golden_finger": "神级选择系统：每次面临选择都能获得逆天奖励",
                "core_conflict": "被青梅竹马背叛，家族被灭，丹田被废，沦为废人",
                "key_scenes": ["退婚现场打脸", "宗门大比一鸣惊人", "秘境获得上古传承"],
                "special_rules": ["境界压制绝对", "杀人夺宝常见", "强者为尊"]
            },
            "都市": {
                "title": "神级透视眼",
                "genre": "都市",
                "world_view": "现代都市中隐藏着古武世家和异能者，主角林凡意外获得透视异能，从此开启逆袭人生。",
                "level_system": ["明劲", "暗劲", "化劲", "宗师", "大宗师", "先天", "筑基", "金丹"],
                "golden_finger": "黄金透视眼：可看透万物本质，赌石鉴宝无往不利",
                "core_conflict": "被富二代陷害，女友被抢，家破人亡",
                "key_scenes": ["赌石大会捡漏", "医院救活绝症患者", "地下拳场一战成名"],
                "special_rules": ["金钱至上", "隐藏世家", "异能觉醒"]
            },
            "游戏": {
                "title": "全职大神",
                "genre": "游戏",
                "world_view": "全球首款虚拟现实游戏《神域》上线，主角林风带着前世记忆重生，誓要登顶巅峰。",
                "level_system": ["黑铁", "青铜", "白银", "黄金", "铂金", "钻石", "大师", "宗师", "王者"],
                "golden_finger": "重生记忆：知晓所有隐藏任务和BUG",
                "core_conflict": "被队友背叛，账号被删，从零开始",
                "key_scenes": ["新手村隐藏任务", "首杀世界BOSS", "竞技场一挑五"],
                "special_rules": ["游戏影响现实", "隐藏职业", "特殊天赋"]
            }
        }
        
        return templates.get(genre, templates["玄幻"])