#!/usr/bin/env python3
"""
人设构建师 Agent - 设计爽文人物角色
"""

import json
import random
from typing import Dict, Any, List
from .base_agent import BaseAgent


class CharacterDesignerAgent(BaseAgent):
    """人设构建师 - 设计主角、配角、反派等角色"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name_library = self._load_name_library()
    
    def _load_name_library(self) -> Dict[str, List[str]]:
        """加载姓名库"""
        return {
            "male_names": ["叶凡", "林逸", "苏尘", "陈凡", "王浩", "李强", "张伟", "赵峰", "刘明", "周宇"],
            "female_names": ["林婉儿", "苏小小", "赵灵儿", "王雪", "李梦", "张雨", "陈静", "周婷", "刘菲", "杨雪"],
            "surnames": ["叶", "林", "苏", "陈", "王", "李", "张", "赵", "刘", "周", "杨", "吴"]
        }
    
    def design_main_character(self, world_info: Dict[str, Any]) -> Dict[str, Any]:
        """设计主角人设"""
        self.log("开始设计主角人设...")
        
        prompt = f"""你是一位顶级的爽文人设设计师，请为以下{world_info['genre']}小说设计主角：

小说标题：{world_info['title']}
世界观：{world_info['world_view']}
金手指：{world_info['golden_finger']}
核心矛盾：{world_info['core_conflict']}

【主角设计核心要求】
1. 初始状态：必须是废柴/被背叛/被陷害的悲惨处境
2. 性格特点：杀伐果断、有恩必报、有仇必报、不圣母
3. 外貌：英俊但低调，关键时刻能惊艳全场
4. 口头禅/习惯动作：如"就这？"、"你也配？"、摇头叹息
5. 隐藏身份：必须是某大能转世/神子/帝子
6. 成长轨迹：废柴→获得金手指→逆袭→打脸→登顶

【配角设置要求】
- 红颜1：高冷圣女/公主，被主角英雄救美
- 红颜2：温柔师妹/邻家女孩，默默支持主角
- 反派1：嚣张跋扈的富二代/宗门天骄
- 反派2：嫉妒主角的同门师兄
- 老爷爷：神秘强者残魂（可选）
- 小弟：被主角救下的天才/妖兽

【输出格式】
严格返回JSON格式：
{{
    "name": "主角名字（2-3字，要霸气）",
    "nickname": "外号（如：叶帝、林尊）",
    "age": 年龄（16-25岁）,
    "initial_state": "初始废柴状态描述",
    "personality": "性格特点（杀伐果断等）",
    "appearance": "外貌描述（要低调但帅气）",
    "hidden_identity": "隐藏身份（必须很牛逼）",
    "catchphrase": "口头禅（装逼用）",
    "love_interests": [
        {{"name": "姓名", "identity": "圣女/公主", "relationship": "英雄救美/青梅竹马"}},
        {{"name": "姓名", "identity": "师妹/邻家女", "relationship": "默默支持/倒追"}}
    ],
    "enemies": [
        {{"name": "反派名字", "identity": "富二代/天骄", "hatred_reason": "嫉妒/抢女友", "defeat_method": "如何被打脸"}},
        {{"name": "反派名字", "identity": "长老/前辈", "hatred_reason": "打压天才", "defeat_method": "如何被打脸"}}
    ],
    "special_abilities": ["特殊能力1", "特殊能力2"]
}}"""

        payload = {
            "model": self.volc_config.get("model", "deepseek-v3-2-251201"),
            "messages": [
                {"role": "system", "content": "你是专业的爽文人设设计师，严格只输出JSON格式"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        response = self.call_volc_api(payload)
        
        if not self.validate_response(response, ["choices"]):
            return self._create_fallback_character(world_info)
        
        try:
            content = response["choices"][0]["message"]["content"].strip()
            character_data = self.extract_json_from_response(content)
            
            if character_data and all(key in character_data for key in ["name", "personality", "love_interests"]):
                self.log(f"✅ 主角设计完成: {character_data['name']}")
                return character_data
            else:
                self.log("❌ 角色数据不完整，使用备用方案")
                return self._create_fallback_character(world_info)
                
        except Exception as e:
            self.log(f"角色解析错误: {str(e)}")
            return self._create_fallback_character(world_info)
    
    def _create_fallback_character(self, world_info: Dict[str, Any]) -> Dict[str, Any]:
        """创建备用角色"""
        genre = world_info.get("genre", "玄幻")
        name = random.choice(self.name_library["male_names"])
        
        if genre == "玄幻":
            return {
                "name": name,
                "nickname": f"{name[0]}帝",
                "age": 18,
                "initial_state": f"{name}本是天才，却被青梅竹马背叛，丹田被废，沦为废人",
                "personality": "杀伐果断，有仇必报，有恩必报",
                "appearance": "剑眉星目，气质不凡，但平时低调内敛",
                "hidden_identity": "上古仙帝转世",
                "catchphrase": "就这？也配与我为敌？",
                "love_interests": [
                    {"name": "林婉儿", "identity": "宗门圣女", "relationship": "英雄救美"},
                    {"name": "苏小小", "identity": "小师妹", "relationship": "青梅竹马"}
                ],
                "enemies": [
                    {"name": "王浩", "identity": "宗门天骄", "hatred_reason": "嫉妒天赋，抢走女友", "defeat_method": "宗门大比上当众打脸"},
                    {"name": "李长老", "identity": "宗门长老", "hatred_reason": "打压天才，偏袒亲传", "defeat_method": "展露真实实力后跪地求饶"}
                ],
                "special_abilities": ["越级战斗", "炼丹天才", "剑道通神"]
            }
        else:  # 都市
            return {
                "name": name,
                "nickname": f"{name[0]}少",
                "age": 22,
                "initial_state": f"{name}被富二代陷害，家破人亡，流落街头",
                "personality": "杀伐果断，商业奇才，重情重义",
                "appearance": "相貌普通但眼神锐利，气质独特",
                "hidden_identity": "隐世家族继承人",
                "catchphrase": "我无敌，你随意",
                "love_interests": [
                    {"name": "赵灵儿", "identity": "豪门千金", "relationship": "意外邂逅"},
                    {"name": "王雪", "identity": "医院护士", "relationship": "治病救人相识"}
                ],
                "enemies": [
                    {"name": "张狂", "identity": "富二代", "hatred_reason": "抢走女友，陷害主角", "defeat_method": "商业上彻底击垮"},
                    {"name": "李老板", "identity": "商业对手", "hatred_reason": "打压主角公司", "defeat_method": "用技术优势碾压"}
                ],
                "special_abilities": ["商业洞察", "武术高手", "医术通神"]
            }
    
    def design_supporting_characters(self, main_character: Dict[str, Any]) -> Dict[str, Any]:
        """设计配角网络"""
        self.log("设计配角网络...")
        
        # 基于主角设计配角关系网
        supporting_chars = {
            "mentors": [],
            "allies": [],
            "rivals": [],
            "neutral": []
        }
        
        # 添加师傅/老爷爷
        if random.random() > 0.3:  # 70%概率有老爷爷
            supporting_chars["mentors"].append({
                "name": "药老" if main_character.get("name", "") == "叶凡" else "玄老",
                "identity": "上古强者残魂",
                "relationship": "师徒",
                "ability": "炼丹/炼器大师",
                "role": "传授功法，关键时刻救场"
            })
        
        # 添加小弟
        supporting_chars["allies"].extend([
            {
                "name": "王虎",
                "identity": "忠厚小弟",
                "relationship": "生死兄弟",
                "loyalty": "绝对忠诚",
                "role": "帮主角处理杂事，收集情报"
            },
            {
                "name": "小狐狸",
                "identity": "化形妖兽",
                "relationship": "主仆",
                "loyalty": "誓死追随", 
                "role": "战斗伙伴，卖萌担当"
            }
        ])
        
        return supporting_chars