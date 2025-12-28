#!/usr/bin/env python3
"""
爽文质检员 Agent - 检查章节质量
"""

import re
import jieba
from typing import Dict, Any, Tuple
from .base_agent import BaseAgent


class QualityCheckerAgent(BaseAgent):
    """爽文质检员 - 检查爽点密度和质量"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.shuang_keywords = self._load_shuang_keywords()
    
    def _load_shuang_keywords(self) -> Dict[str, list]:
        """加载爽点关键词库"""
        return {
            "face_slapping": ["打脸", "碾压", "秒杀", "完爆", "完胜", "吊打", "虐菜", "碾压", "完虐"],
            "upgrade": ["突破", "升级", "进阶", "晋升", "暴涨", "飙升", "大涨", "提升"],
            "reward": ["获得", "得到", "收获", "奖励", "宝物", "神器", "功法", "丹药"],
            "discovery": ["发现", "找到", "获得", "奇遇", "机缘", "传承", "秘境"],
            "relationship": ["收服", "结交", "结识", "红颜", "小弟", "追随", "投靠"],
            "system": ["叮！", "系统", "提示", "奖励", "任务", "完成", "发布"]
        }
    
    def check_chapter(self, chapter_content: str, chapter_plan: Dict[str, Any]) -> Dict[str, Any]:
        """检查章节质量"""
        self.log("开始质量检查...")
        
        metrics = self._calculate_metrics(chapter_content, chapter_plan)
        
        # 爽文合格标准
        pass_criteria = {
            "shuang_density": metrics["shuang_density"] >= 3,  # 每章至少3个爽点
            "face_slapping_count": metrics["face_slapping_count"] >= 1,
            "dialogue_ratio": 0.2 <= metrics["dialogue_ratio"] <= 0.6,
            "paragraph_length": metrics["avg_paragraph_lines"] <= 5,
            "hook_strength": metrics["hook_strength"] >= 7,
            "word_count": 2500 <= metrics["word_count"] <= 4000,
            "readability": metrics["readability_score"] >= 6
        }
        
        quality_score = self._calculate_quality_score(metrics, pass_criteria)
        
        result = {
            "pass": all(pass_criteria.values()),
            "quality_score": quality_score,
            "metrics": metrics,
            "pass_criteria": pass_criteria,
            "fail_reasons": [k for k, v in pass_criteria.items() if not v],
            "suggestions": self._generate_suggestions(metrics, pass_criteria)
        }
        
        self.log(f"质量检查完成: 得分{quality_score}/10, {'通过' if result['pass'] else '不通过'}")
        return result
    
    def _calculate_metrics(self, content: str, chapter_plan: Dict[str, Any]) -> Dict[str, Any]:
        """计算各项质量指标"""
        # 基础统计
        word_count = len(content)
        char_count = len(content.replace(' ', '').replace('\n', ''))
        
        # 爽点密度
        shuang_density = self._count_shuang_points(content)
        
        # 对话比例
        dialogue_ratio = self._calculate_dialogue_ratio(content)
        
        # 段落长度
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        avg_paragraph_lines = sum(len(p.split('\n')) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        
        # 悬念钩子强度
        hook_strength = self._evaluate_hook_strength(content)
        
        # 可读性评分
        readability_score = self._calculate_readability(content)
        
        return {
            "word_count": word_count,
            "char_count": char_count,
            "shuang_density": shuang_density,
            "face_slapping_count": self._count_face_slapping(content),
            "dialogue_ratio": dialogue_ratio,
            "avg_paragraph_lines": avg_paragraph_lines,
            "hook_strength": hook_strength,
            "readability_score": readability_score,
            "paragraph_count": len(paragraphs),
            "sentence_count": len(re.findall(r'[。！？!?]', content))
        }
    
    def _count_shuang_points(self, content: str) -> int:
        """计算爽点密度"""
        total_shuangs = 0
        
        for category, keywords in self.shuang_keywords.items():
            for keyword in keywords:
                total_shuangs += len(re.findall(keyword, content))
        
        # 系统提示也算爽点
        system_count = len(re.findall(r'【[^】]*?】', content))
        total_shuangs += system_count
        
        return total_shuangs
    
    def _count_face_slapping(self, content: str) -> int:
        """计算打脸次数"""
        face_slapping_patterns = [
            r'打脸', r'碾压', r'秒杀', r'完爆', r'吊打', r'虐菜',
            r'不敢置信', r'目瞪口呆', r'震惊', r'骇然', r'惊恐'
        ]
        
        count = 0
        for pattern in face_slapping_patterns:
            count += len(re.findall(pattern, content))
        
        return count
    
    def _calculate_dialogue_ratio(self, content: str) -> float:
        """计算对话比例 - 修复版"""
        if not content or len(content) < 100:
            return 0.0
        
        # 改进的对话识别
        dialogue_patterns = [
            r'[""]([^""]+)[""]',  # 双引号对话
            r'["]([^"]+)["]',  # 单引号对话
            r'[「]([^」]+)[」]',  # 中文引号
            r'[『]([^』]+)[』]',  # 中文引号2
        ]
        
        dialogue_length = 0
        for pattern in dialogue_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                dialogue_length += len(str(match))
        
        # 也识别"XX说："格式
        said_pattern = r'[\u4e00-\u9fa5]{2,4}(?:道|说|问|答|喊|喝|骂)[:：]\s*([^。？！]+)[。？！]'
        said_matches = re.findall(said_pattern, content)
        for match in said_matches:
            dialogue_length += len(match)
        
        total_length = len(content)
        
        if total_length == 0:
            return 0.0
        
        ratio = dialogue_length / total_length
        return round(ratio, 3)
    
    def _evaluate_hook_strength(self, content: str) -> int:
        """评估悬念钩子强度（1-10分）"""
        # 获取最后一段
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        if not paragraphs:
            return 5
        
        last_paragraph = paragraphs[-1]
        
        # 检查悬念关键词
        hook_keywords = ['突然', '意外', '震惊', '没想到', '竟然', '原来', '秘密', '真相', '危机', '危险']
        hook_score = 0
        
        for keyword in hook_keywords:
            if keyword in last_paragraph:
                hook_score += 1
        
        # 检查问号和省略号
        if '？' in last_paragraph or '...' in last_paragraph or '……' in last_paragraph:
            hook_score += 2
        
        # 检查是否是新事件的开头
        if any(word in last_paragraph for word in ['就在这时', '突然', '意外的是']):
            hook_score += 3
        
        return min(10, hook_score)
    
    def _calculate_readability(self, content: str) -> float:
        """计算可读性评分（1-10分）"""
        score = 6.0  # 基础分
        
        # 段落长度评分
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        if paragraphs:
            avg_para_length = sum(len(p) for p in paragraphs) / len(paragraphs)
            if avg_para_length < 300:
                score += 1
            elif avg_para_length > 600:
                score -= 1
        
        # 句子长度评分
        sentences = re.split(r'[。！？!?]', content)
        sentences = [s for s in sentences if s.strip()]
        if sentences:
            avg_sentence_length = sum(len(s) for s in sentences) / len(sentences)
            if avg_sentence_length < 30:
                score += 1
            elif avg_sentence_length > 60:
                score -= 1
        
        # 对话比例评分
        dialogue_ratio = self._calculate_dialogue_ratio(content)
        if 0.3 <= dialogue_ratio <= 0.5:
            score += 1
        elif dialogue_ratio < 0.2 or dialogue_ratio > 0.6:
            score -= 1
        
        return max(1, min(10, score))
    
    def _calculate_quality_score(self, metrics: Dict[str, Any], pass_criteria: Dict[str, bool]) -> float:
        """计算综合质量评分（1-10分）"""
        score = 6.0  # 基础分
        
        # 爽点密度加分
        if metrics["shuang_density"] >= 5:
            score += 1
        elif metrics["shuang_density"] < 2:
            score -= 1
        
        # 打脸次数加分
        if metrics["face_slapping_count"] >= 2:
            score += 0.5
        
        # 可读性加分
        if metrics["readability_score"] >= 7:
            score += 0.5
        
        # 字数合理性
        if 2800 <= metrics["word_count"] <= 3500:
            score += 0.5
        elif metrics["word_count"] < 2000 or metrics["word_count"] > 5000:
            score -= 1
        
        # 悬念钩子强度
        if metrics["hook_strength"] >= 8:
            score += 0.5
        
        return max(1, min(10, round(score, 1)))
    
    def _generate_suggestions(self, metrics: Dict[str, Any], pass_criteria: Dict[str, bool]) -> list:
        """生成改进建议"""
        suggestions = []
        
        if not pass_criteria.get("shuang_density", True):
            suggestions.append("增加爽点密度，每章至少3个爽点")
        
        if not pass_criteria.get("face_slapping_count", True):
            suggestions.append("增加打脸场景，至少1次打脸")
        
        if not pass_criteria.get("dialogue_ratio", True):
            current_ratio = metrics["dialogue_ratio"]
            if current_ratio < 0.2:
                suggestions.append("增加对话比例，建议20%-60%")
            else:
                suggestions.append("减少对话比例，建议20%-60%")
        
        if not pass_criteria.get("paragraph_length", True):
            suggestions.append("缩短段落长度，每段不超过5行")
        
        if not pass_criteria.get("hook_strength", True):
            suggestions.append("加强章末悬念钩子")
        
        if not pass_criteria.get("word_count", True):
            suggestions.append(f"调整字数，建议3000字左右，当前{metrics['word_count']}字")
        
        return suggestions