#!/usr/bin/env python3
"""
爽点策划师 Agent - 编排爽点节奏和情节
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class ShuangPlannerAgent(BaseAgent):
    """爽点策划师 - 编排密集的爽点节奏"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.shuang_patterns = self._load_shuang_patterns()
    
    def _load_shuang_patterns(self) -> Dict[str, Any]:
        """加载爽点模式库"""
        return {
            "face_slapping": [
                "退婚打脸：前未婚妻后悔莫及",
                "拍卖会打脸：用最低价拍得至宝",
                "宗门大比打脸：越级挑战成功",
                "医术打脸：治好名医都治不好的病",
                "鉴宝打脸：捡漏绝世宝物"
            ],
            "upgrade": [
                "突破境界：引来天地异象",
                "学会神功：瞬间战力飙升", 
                "获得神器：威力惊天动地",
                "收服神兽：获得强大助力",
                "炼丹成功：炼制出极品丹药"
            ],
            "relationship": [
                "英雄救美：获得美女芳心",
                "收服小弟：获得忠诚追随者",
                "结交强者：扩展人脉网络",
                "打脸情敌：让情敌无地自容",
                "家族认可：让曾经看不起的人刮目相看"
            ],
            "discovery": [
                "发现秘境：获得上古传承",
                "破解谜题：获得隐藏奖励",
                "意外捡漏：用低价买到至宝",
                "血脉觉醒：获得特殊能力",
                "系统奖励：完成隐藏任务"
            ]
        }
    
    def plan_shuang_points(self, world_info: Dict[str, Any], 
                          character_info: Dict[str, Any], 
                          chapter_count: int = 50) -> List[Dict[str, Any]]:
        """编排爽点节奏表"""
        self.log(f"开始编排{chapter_count}章爽点节奏...")
        
        prompt = f"""你是一位顶级的爽文节奏策划师，请为以下小说编排前{chapter_count}章的爽点节奏：

小说标题：{world_info['title']}
世界观：{world_info['world_view']}
主角：{character_info['name']}（{character_info['initial_state']}）
金手指：{character_info.get('hidden_identity', '')} + {world_info['golden_finger']}

【黄金三章要求（必须严格执行）】
第1章：必须出现第一个高潮（退婚/背叛现场打脸）
第2章：必须获得金手指/开始逆袭
第3章：必须完成第一次越级挑战/打脸

【爽点编排原则】
1. 每章必须至少有3个爽点（打脸、升级、收获交替进行）
2. 每3章必须有一个中型高潮（收服重要角色/获得重大突破）
3. 每10章必须有一个大型高潮（宗门大比/拍卖会/秘境探险）
4. 章末必须有悬念钩子（新敌人出现/新危机降临）
5. 情绪曲线：压抑→爆发→爽快→新目标

【爽点类型库】
打脸类：{', '.join(self.shuang_patterns['face_slapping'][:3])}
升级类：{', '.join(self.shuang_patterns['upgrade'][:3])}
关系类：{', '.join(self.shuang_patterns['relationship'][:3])}
奇遇类：{', '.join(self.shuang_patterns['discovery'][:3])}

【输出格式】
严格返回JSON数组，每个元素对应一章：
[
    {{
        "chapter_number": 1,
        "title": "章节标题（要吸引人）",
        "main_shuang": "主要爽点描述",
        "secondary_shuangs": ["次要爽点1", "次要爽点2"],
        "emotional_arc": "情绪曲线（压抑→爆发→爽）",
        "ending_hook": "章末悬念钩子",
        "word_count_target": 3000,
        "key_scenes": ["关键场景1", "关键场景2"]
    }},
    ...
]"""

        payload = {
            "model": self.volc_config.get("model", "deepseek-v3-2-251201"),
            "messages": [
                {"role": "system", "content": "你是专业的爽文节奏策划师，严格只输出JSON数组格式"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 4000
        }
        
        response = self.call_volc_api(payload)
        
        if not self.validate_response(response, ["choices"]):
            return self._create_fallback_plan(chapter_count, world_info, character_info)
        
        try:
            content = response["choices"][0]["message"]["content"].strip()
            shuang_plan = self.extract_json_from_response(content)
            
            if isinstance(shuang_plan, list) and len(shuang_plan) >= chapter_count:
                self.log(f"✅ 爽点策划完成: {len(shuang_plan)}章")
                return shuang_plan[:chapter_count]  # 只取需要的章节数
            else:
                self.log("❌ 爽点计划不完整，使用备用方案")
                return self._create_fallback_plan(chapter_count, world_info, character_info)
                
        except Exception as e:
            self.log(f"爽点计划解析错误: {str(e)}")
            return self._create_fallback_plan(chapter_count, world_info, character_info)
    
    def _create_fallback_plan(self, chapter_count: int, 
                           world_info: Dict[str, Any], 
                           character_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """创建备用爽点计划"""
        self.log("使用备用爽点计划")
        
        plan = []
        genre = world_info.get("genre", "玄幻")
        main_char = character_info.get("name", "叶凡")
        
        # 黄金三章
        plan.extend([
            {
                "chapter_number": 1,
                "title": "退婚之辱",
                "main_shuang": f"{main_char}被当众退婚，觉醒金手指",
                "secondary_shuangs": ["获得系统奖励", "发现隐藏天赋"],
                "emotional_arc": "屈辱→愤怒→觉醒",
                "ending_hook": "系统发布第一个任务",
                "word_count_target": 3200,
                "key_scenes": ["退婚现场", "金手指觉醒"]
            },
            {
                "chapter_number": 2,
                "title": "初露锋芒", 
                "main_shuang": f"{main_char}第一次展现实力，打脸小反派",
                "secondary_shuangs": ["修为突破", "获得第一桶金"],
                "emotional_arc": "隐忍→爆发→爽快",
                "ending_hook": "引起更大反派的注意",
                "word_count_target": 3000,
                "key_scenes": ["坊市冲突", "越级战斗"]
            },
            {
                "chapter_number": 3,
                "title": "宗门考核",
                "main_shuang": f"{main_char}在考核中一鸣惊人",
                "secondary_shuangs": ["被长老看中", "收获迷弟迷妹"],
                "emotional_arc": "紧张→惊艳→自豪", 
                "ending_hook": "神秘强者发出邀请",
                "word_count_target": 3100,
                "key_scenes": ["天赋测试", "实战考核"]
            }
        ])
        
        # 后续章节
        for i in range(4, chapter_count + 1):
            if i % 10 == 0:  # 每10章大高潮
                plan.append(self._create_major_cliffhanger(i, main_char, genre))
            elif i % 3 == 0:  # 每3章中高潮
                plan.append(self._create_medium_cliffhanger(i, main_char, genre))
            else:  # 普通章节
                plan.append(self._create_normal_chapter(i, main_char, genre))
        
        return plan
    
    def _create_major_cliffhanger(self, chapter_num: int, main_char: str, genre: str) -> Dict[str, Any]:
        """创建大高潮章节"""
        events = {
            "玄幻": ["宗门大比", "秘境探险", "拍卖盛会", "丹道大会"],
            "都市": ["商业大战", "武林大会", "鉴宝大会", "医院危机"],
            "游戏": ["世界BOSS", "公会大战", "竞技场决赛", "隐藏副本"]
        }
        
        event = events.get(genre, events["玄幻"])[chapter_num % 4]
        
        return {
            "chapter_number": chapter_num,
            "title": f"{event}（上）",
            "main_shuang": f"{main_char}在{event}中惊艳全场",
            "secondary_shuangs": ["收获至宝", "实力大涨", "名声大噪"],
            "emotional_arc": "期待→激烈→巅峰",
            "ending_hook": "出现更强大的对手",
            "word_count_target": 3500,
            "key_scenes": [f"{event}现场", "巅峰对决"]
        }
    
    def _create_medium_cliffhanger(self, chapter_num: int, main_char: str, genre: str) -> Dict[str, Any]:
        """创建中高潮章节"""
        return {
            "chapter_number": chapter_num,
            "title": f"突破！{main_char}的成长",
            "main_shuang": f"{main_char}突破新境界",
            "secondary_shuangs": ["获得新技能", "收服新小弟", "打脸小反派"],
            "emotional_arc": "修炼→突破→爽快",
            "ending_hook": "新危机出现",
            "word_count_target": 3200,
            "key_scenes": ["修炼突破", "实力验证"]
        }
    
    def _create_normal_chapter(self, chapter_num: int, main_char: str, genre: str) -> Dict[str, Any]:
        """创建普通章节"""
        return {
            "chapter_number": chapter_num,
            "title": f"{main_char}的日常",
            "main_shuang": f"{main_char}解决一个小麻烦",
            "secondary_shuangs": ["日常修炼", "人际互动", "小奇遇"],
            "emotional_arc": "平静→小高潮→满足",
            "ending_hook": "铺垫下一个事件",
            "word_count_target": 3000,
            "key_scenes": ["日常修炼", "小冲突解决"]
        }