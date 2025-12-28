"""
网络爽文生成Agent系统
"""

from .base_agent import BaseAgent
from .world_architect import WorldArchitectAgent
from .character_designer import CharacterDesignerAgent
from .shuang_planner import ShuangPlannerAgent
from .chapter_writer import ChapterWriterAgent
from .quality_checker import QualityCheckerAgent
from .long_term_memory import LongTermMemoryAgent

__all__ = [
    'BaseAgent',
    'WorldArchitectAgent', 
    'CharacterDesignerAgent',
    'ShuangPlannerAgent',
    'ChapterWriterAgent',
    'QualityCheckerAgent',
    'LongTermMemoryAgent'
]

__version__ = "1.0.0"
__author__ = "杨一"