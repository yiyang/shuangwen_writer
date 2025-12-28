📖 网络爽文生成Agent系统

基于大语言模型的智能网络爽文生成平台 日更万字

 商业级质量

✨ 核心特性

🤖 专业Agent分工

• 🌍 世界观架构师 - 构建完整的修仙/都市/游戏世界观体系

• 👤 人设构建师 - 设计杀伐果断的主角+丰富配角网络

• 📈 爽点策划师 - 密集爽点排布，每章至少3个爽点

• ✍️ 章节生成师 - 专业爽文写作，符合网文阅读习惯

• 🔍 爽文质检员 - 质量监控，确保商业价值

• 💾 长期记忆Agent - 维护情节连续性，伏笔回收

🎯 爽文专业优化

• 黄金三章 - 开篇即高潮，快速抓住读者

• 打脸套路 - 退婚、拍卖会、宗门大比等经典场景

• 等级体系 - 完整的9境81阶修炼体系

• 金手指 - 系统、老爷爷、重生等经典设定

• 悬念钩子 - 章末断章，引导追读

📊 质量控制

• 爽点密度 ≥ 3个/章

• 打脸场景 ≥ 1个/章

• 对话比例 30%-60%

• 段落长度 ≤ 5行/段

• 悬念强度 ≥ 7/10分

🚀 快速开始

环境要求

• Python 3.8+

• 火山引擎API密钥（或其他大模型API）

• 内存：8GB+

• 磁盘空间：1GB+

安装步骤

1. 克隆项目
git clone https://github.com/yiyang/shuangwen_writer.git
cd shuangwen_writer


2. 安装依赖
pip install -r requirements.txt


3. 配置API密钥
# 在 config.py 中配置
VOLC_CONFIG = {
    "api_key": "your-api-key-here",
    "api_base": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "model": "deepseek-v3-2-251201"
}


4. 运行示例
# 生成50章玄幻爽文
python quick_start.py

# 或使用交互模式
python main.py


📁 项目结构


shuangwen_agent/
├── agents/                 # 智能体模块
│   ├── world_architect.py     # 世界观架构师
│   ├── character_designer.py  # 人设构建师
│   ├── shuang_planner.py      # 爽点策划师
│   ├── chapter_writer.py      # 章节生成师
│   ├── quality_checker.py     # 爽文质检员
│   └── long_term_memory.py    # 长期记忆
├── outputs/                # 生成输出
├── config.py               # 配置文件
├── main.py                 # 主程序
├── quick_start.py          # 快速启动
└── requirements.txt        # 依赖列表


🎮 使用方法

基本使用

from main import ShuangNovelGenerator

# 初始化生成器
generator = ShuangNovelGenerator()

# 生成50章玄幻爽文
novel = generator.generate_novel(
    genre="玄幻",
    target_chapters=50,
    output_dir="./outputs"
)

print(f"📖 书名: {novel['title']}")
print(f"📈 总字数: {novel['total_words']}")
print(f"🎯 平均爽点密度: {novel['avg_shuang_density']}个/章")


高级定制

# 自定义世界观
custom_world = {
    "genre": "都市",
    "level_system": ["明劲", "暗劲", "化劲", "宗师", "大宗师"],
    "special_rules": ["灵气复苏", "国术崛起"]
}

# 自定义人物设定
custom_character = {
    "name": "林凡",
    "personality": "杀伐果断",
    "golden_finger": "神级选择系统",
    "initial_state": "被家族抛弃的废柴"
}

# 生成定制爽文
novel = generator.generate_custom_novel(
    world_settings=custom_world,
    character_settings=custom_character,
    target_chapters=100
)


批量生成

# 批量生成多部小说
genres = ["玄幻", "都市", "游戏"]
for genre in genres:
    novel = generator.generate_novel(
        genre=genre,
        target_chapters=30
    )
    print(f"✅ 已完成: {novel['title']}")


⚙️ 配置说明

API配置 (config.py)

# 大模型配置
VOLC_CONFIG = {
    "api_key": "your-api-key",
    "api_base": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "model": "deepseek-v3-2-251201"
}

支持的世界观类型

类型 等级体系 特色玩法 代表作品

玄幻 练气→渡劫→仙帝 宗门、秘境、炼丹 《凡人修仙传》

都市 明劲→化劲→先天 商业、校园、异能 《校花的贴身高手》

游戏 黑铁→钻石→王者 副本、竞技、公会 《全职高手》

科幻 基因锁→行星级→宇宙级 星际、机甲、进化 《吞噬星空》

📊 输出格式

章节文件结构


outputs/novels/玄幻_我真是大魔王_20241201/
├── novel_info.json          # 小说元信息
├── chapter_001.txt          # 第1章
├── chapter_002.txt          # 第2章
├── ...
├── chapter_050.txt          # 第50章
└── summary.md               # 全书摘要


元信息示例

{
  "title": "我真是大魔王",
  "genre": "玄幻",
  "author": "AI作家",
  "total_chapters": 50,
  "total_words": 152000,
  "created_date": "2024-12-01",
  "main_character": {
    "name": "叶凡",
    "level": "金丹期",
    "golden_finger": "万界签到系统"
  },
  "quality_metrics": {
    "avg_shuang_density": 3.8,
    "avg_face_slapping": 1.2,
    "reader_engagement": 8.5
  }
}


🎯 爽文特色功能

1. 经典打脸场景库

# 内置经典打脸套路
FACE_SLAPPING_SCENES = [
    "退婚流：三年之期已到，恭迎龙王归来",
    "拍卖会：用最低价拍得神器，打脸富二代",
    "宗门大比：隐藏实力，越级挑战成功",
    "医术打脸：治好绝症，打脸名医",
    "鉴宝流：捡漏至宝，打脸专家"
]


2. 金手指系统

# 支持的金手指类型
GOLDEN_FINGERS = [
    "系统流：神级选择系统、签到系统",
    "老爷爷流：戒指里的上古大能",
    "重生流：带着记忆重生",
    "穿越流：现代知识碾压古代",
    "血脉流：觉醒上古血脉"
]


3. 智能伏笔管理

# 自动伏笔回收
foreshadowing_manager = {
    "active_foreshadowing": [
        "神秘的黑衣人身份",
        "主角的身世之谜", 
        "上古秘境的钥匙"
    ],
    "callback_reminders": [
        "第10章：需要回收黑衣人伏笔",
        "第25章：揭示主角身世"
    ]
}

🤝 贡献指南

我们欢迎贡献！请阅读：

1. 开发流程
# 1. Fork 项目
# 2. 创建特性分支
git checkout -b feature/awesome-feature

# 3. 提交更改
git commit -m "Add awesome feature"

# 4. 推送到分支
git push origin feature/awesome-feature

# 5. 创建Pull Request


2. 代码规范
• 使用 Black 格式化代码

• 添加类型注解

• 编写单元测试

• 更新文档

3. 测试要求
# 运行测试
pytest tests/

# 检查代码覆盖率
pytest --cov=shuangwen_agent tests/


📄 许可证

本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情。

🙏 致谢

• https://www.volcengine.com/ - 提供强大的大语言模型API

• 网络文学平台 - 提供爽文创作灵感

• 开源社区 - 各种工具和库的支持

📞 技术支持

• 📧 邮箱：contactyang@163.com

• 💬 讨论区：https://github.com/yiyang/shuangwen-agent/discussions

• 🐛 问题反馈：https://github.com/yiyang/shuangwen-agent/issues

如果这个项目对你有帮助，请给个 ⭐️ 支持一下！

让AI帮你写出下一个爆款爽文！