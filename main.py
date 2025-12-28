#!/usr/bin/env python3
"""
网络爽文生成系统 - 主程序
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union  # 添加类型注解导入

# 从配置文件导入配置
from config import VOLC_CONFIG, SYSTEM_CONFIG

# 导入所有Agent
try:
    from agents import (
        WorldArchitectAgent,
        CharacterDesignerAgent, 
        ShuangPlannerAgent,
        ChapterWriterAgent,
        QualityCheckerAgent,
        LongTermMemoryAgent
    )
except ImportError as e:
    print(f"❌ 导入Agent失败: {e}")
    print("请确保agents目录存在且包含所有Agent文件")
    # 创建空的Agent类作为备用
    class BaseAgent:
        def __init__(self, config):
            self.config = config
    
    class WorldArchitectAgent(BaseAgent): pass
    class CharacterDesignerAgent(BaseAgent): pass
    class ShuangPlannerAgent(BaseAgent): pass
    class ChapterWriterAgent(BaseAgent): pass
    class QualityCheckerAgent(BaseAgent): pass
    class LongTermMemoryAgent(BaseAgent): pass


class ShuangNovelGenerator:
    """网络爽文生成系统主控制器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        # 如果没有提供配置，使用默认配置
        if config is None:
            config = {
                "volc_config": VOLC_CONFIG,
                "system_config": SYSTEM_CONFIG
            }
        self.config = config
        self.initialize_agents()
        
    def initialize_agents(self):
        """初始化所有Agent"""
        print("🤖 初始化智能体系统...")
        
        try:
            self.world_architect = WorldArchitectAgent(self.config)
            self.character_designer = CharacterDesignerAgent(self.config)
            self.shuang_planner = ShuangPlannerAgent(self.config)
            self.chapter_writer = ChapterWriterAgent(self.config)
            self.quality_checker = QualityCheckerAgent(self.config)
            self.memory = LongTermMemoryAgent(self.config)
            print("✅ 智能体系统初始化完成")
        except Exception as e:
            print(f"❌ 智能体初始化失败: {e}")
            print("⚠️  Agent功能可能受限")
    
    def generate_novel(self, genre: str = "玄幻", target_chapters: int = 50, 
                     output_dir: str = "./outputs") -> Dict[str, Any]:
        """生成完整爽文"""
        print(f"\n🎬 开始生成{genre}爽文，目标{target_chapters}章")
        print("="*60)
        
        start_time = time.time()
        
        try:
            # 1. 构建世界观
            print("\n🌍 步骤1: 构建世界观...")
            world_info = self.world_architect.design_world(genre)
            print(f"   ✅ 世界观: {world_info['title']}")
            
            # 2. 设计人设
            print("\n👤 步骤2: 设计人设...")
            character_info = self.character_designer.design_main_character(world_info)
            print(f"   ✅ 主角: {character_info['name']}")
            
            # 3. 初始化记忆系统
            print("\n💾 步骤3: 初始化记忆...")
            self.memory.initialize_story(world_info, character_info)
            
            # 4. 策划爽点节奏
            print(f"\n📈 步骤4: 策划{target_chapters}章爽点节奏...")
            shuang_plan = self.shuang_planner.plan_shuang_points(
                world_info, character_info, target_chapters
            )
            print(f"   ✅ 爽点策划完成: {len(shuang_plan)}章")
            
            # 5. 逐章生成
            print(f"\n✍️ 步骤5: 生成章节内容...")
            novel_chapters = self._generate_chapters(
                shuang_plan, world_info, character_info, target_chapters
            )
            
            # 6. 生成总结报告
            print(f"\n📊 步骤6: 生成总结报告...")
            summary = self._generate_summary(novel_chapters, world_info, character_info)
            
            # 7. 保存结果
            print(f"\n💾 步骤7: 保存结果...")
            output_path = self._save_results(novel_chapters, summary, world_info, output_dir)
            
            # 计算统计信息
            total_time = time.time() - start_time
            total_words = sum(len(chap["content"]) for chap in novel_chapters)
            
            print(f"\n🎉 生成完成！")
            print(f"⏱️ 总耗时: {total_time/60:.1f}分钟")
            print(f"📖 总字数: {total_words:,}字")
            print(f"📁 保存路径: {output_path}")
            
            return {
                "success": True,
                "novel_info": {
                    "title": world_info["title"],
                    "genre": genre,
                    "total_chapters": len(novel_chapters),
                    "total_words": total_words,
                    "output_path": output_path
                },
                "summary": summary,
                "chapters": novel_chapters
            }
            
        except Exception as e:
            print(f"\n❌ 生成失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_chapters(self, shuang_plan, world_info, character_info, target_chapters):
        """逐章生成内容 - 无fallback版本"""
        novel_chapters = []
        
        for chapter_num in range(1, target_chapters + 1):
            try:
                print(f"  📝 生成第{chapter_num}/{target_chapters}章...")
                
                chapter_plan = shuang_plan[chapter_num - 1]
                
                memory_context = self.memory.get_current_context()
                memory_context.update({
                    "world_info": world_info,
                    "character_info": character_info
                })
                
                # 强制生成章节，不接收fallback
                chapter_content = self.chapter_writer.write_chapter(
                    chapter_plan, memory_context, chapter_num
                )
                
                if not chapter_content or len(chapter_content) < 1000:
                    print(f"❌ 第{chapter_num}章生成失败：内容过短或无内容")
                    raise Exception("内容生成失败")
                
                # 质量检查
                quality_report = self.quality_checker.check_chapter(chapter_content, chapter_plan)
                
                if not quality_report["pass"]:
                    print(f"❌ 第{chapter_num}章质量检查失败：{quality_report['fail_reasons']}")
                    # 不通过就继续，但记录问题
                    print("⚠️  质量不达标，但继续生成")
                
                # 更新记忆
                self.memory.update_after_chapter(chapter_content, chapter_num, chapter_plan)
                
                # 保存章节
                chapter_data = {
                    "chapter_number": chapter_num,
                    "title": chapter_plan["title"],
                    "content": chapter_content,
                    "quality_score": quality_report.get("quality_score", 0),
                    "word_count": len(chapter_content),
                    "quality_metrics": quality_report.get("metrics", {})
                }
                novel_chapters.append(chapter_data)
                
                print(f"✅ 第{chapter_num}章生成完成")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ 第{chapter_num}章生成失败：{str(e)}")
                # 可以选择继续或停止
                continue
        
        return novel_chapters
    
    def _generate_summary(self, chapters: List[Dict[str, Any]], 
                         world_info: Dict[str, Any], 
                         character_info: Dict[str, Any]) -> Dict[str, Any]:
        """生成总结报告"""
        if not chapters:
            return {"error": "没有生成章节"}
        
        total_words = sum(chap["word_count"] for chap in chapters)
        avg_quality = sum(chap["quality_score"] for chap in chapters) / len(chapters)
        
        return {
            "title": world_info["title"],
            "main_character": character_info["name"],
            "total_chapters": len(chapters),
            "total_words": total_words,
            "average_quality": round(avg_quality, 1),
            "average_words_per_chapter": total_words // len(chapters),
            "completion_rate": f"{len(chapters)}/{len(chapters)}章",
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _save_results(self, chapters: List[Dict[str, Any]], 
                     summary: Dict[str, Any],
                     world_info: Dict[str, Any],
                     output_dir: str) -> str:
        """保存生成结果"""
        # 创建输出目录
        safe_title = "".join(c for c in world_info["title"] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        novel_dir = os.path.join(output_dir, f"{safe_title}_{timestamp}")
        os.makedirs(novel_dir, exist_ok=True)
        
        # 保存元信息
        with open(os.path.join(novel_dir, "novel_info.json"), 'w', encoding='utf-8') as f:
            json.dump({
                "title": world_info["title"],
                "summary": summary,
                "world_info": world_info,
                "generation_config": self.config
            }, f, ensure_ascii=False, indent=2)
        
        # 保存各章节
        for chapter in chapters:
            filename = f"chapter_{chapter['chapter_number']:03d}.txt"
            filepath = os.path.join(novel_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"第{chapter['chapter_number']}章：{chapter['title']}\n")
                f.write("="*50 + "\n\n")
                f.write(chapter['content'])
                f.write(f"\n\n【本章统计】\n")
                f.write(f"字数：{chapter['word_count']}字\n")
                f.write(f"质量评分：{chapter['quality_score']}/10\n")
        
        # 保存总结报告
        with open(os.path.join(novel_dir, "summary.md"), 'w', encoding='utf-8') as f:
            f.write(f"# {world_info['title']} - 生成报告\n\n")
            f.write(f"**生成时间**：{summary['generation_date']}\n\n")
            f.write(f"**主角**：{summary['main_character']}\n\n")
            f.write(f"**总章节**：{summary['total_chapters']}章\n\n")
            f.write(f"**总字数**：{summary['total_words']:,}字\n\n")
            f.write(f"**平均质量**：{summary['average_quality']}/10\n\n")
            f.write(f"**平均每章字数**：{summary['average_words_per_chapter']}字\n\n")
        
        return novel_dir


def main():
    """主函数"""
    print("🎬 网络爽文生成系统 v1.0")
    print("="*50)
    
    # 创建生成器
    generator = ShuangNovelGenerator()
    
    # 用户选择
    print("\n请选择生成模式:")
    print("1. 快速测试 (10章玄幻)")
    print("2. 完整生成 (50章玄幻)") 
    print("3. 自定义生成")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        # 快速测试
        result = generator.generate_novel(genre="玄幻", target_chapters=10)
    elif choice == "2":
        # 完整生成
        result = generator.generate_novel(genre="玄幻", target_chapters=50)
    elif choice == "3":
        # 自定义生成
        genre = input("请输入类型 (玄幻/都市/游戏): ").strip() or "玄幻"
        chapters = input("请输入章节数 (默认10): ").strip()
        target_chapters = int(chapters) if chapters.isdigit() else 10
        result = generator.generate_novel(genre=genre, target_chapters=target_chapters)
    else:
        print("❌ 无效选择")
        return
    
    # 显示结果
    if result["success"]:
        print(f"\n🎉 生成成功！")
        print(f"📖 书名: {result['novel_info']['title']}")
        print(f"📊 章节: {result['novel_info']['total_chapters']}章")
        print(f"📝 字数: {result['novel_info']['total_words']:,}字")
        print(f"📁 路径: {result['novel_info']['output_path']}")
    else:
        print(f"❌ 生成失败: {result['error']}")


if __name__ == "__main__":
    main()