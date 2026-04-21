#!/usr/bin/env python3
"""
测试脚本 - 验证各个模块功能
"""
import sys
import json
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.config_loader import get_config
from scripts.novel_generator import NovelGenerator, search_topics
from scripts.minimax_image import MiniMaxImageGenerator

def test_config():
    """测试配置加载"""
    print("=== 测试配置加载 ===")
    config = get_config()
    print(f"MiniMax Token: {config.minimax.get('token', '')[:20]}...")
    print(f"Qwen Token: {config.qwen.get('token', '')[:20]}...")
    print(f"写作字数/话: {config.writing.get('words_per_episode')}")
    print("✅ 配置加载正常\n")

def test_topic_search():
    """测试选题搜索"""
    print("=== 测试选题搜索 ===")
    generator = NovelGenerator()
    topics = generator.search_topics()
    print(f"找到 {len(topics)} 个选题")
    for i, t in enumerate(topics[:3]):
        print(f"{i+1}. {t.get('title', 'N/A')}")
    print("✅ 选题搜索正常\n")

def test_outline_generation():
    """测试大纲生成"""
    print("=== 测试大纲生成 ===")
    generator = NovelGenerator()
    test_meta = {
        "title": "最后的备份",
        "genre": "科幻",
        "theme": "意识上传与身份认同",
        "characters": """主角-林远：40岁，神经科学家，在一次实验中意识被困在量子服务器中
配角-小雨：林远的AI助手，逐渐觉醒自我意识""",
        "setting": "2089年，人类已经实现意识数字化，城市中充斥着各种AI实体",
        "style": "简洁悬疑，充满哲学思考",
        "plot_direction": "林远的意识备份开始质疑：我还是原来的我吗？"
    }
    print("生成大纲中...")
    outline = generator.generate_outline(test_meta)
    print(f"大纲长度: {len(outline)} 字符")
    print(f"前500字:\n{outline[:500]}")
    print("✅ 大纲生成正常\n")

def test_image_generation():
    """测试图片生成"""
    print("=== 测试 MiniMax 文生图 ===")
    generator = MiniMaxImageGenerator()
    print("测试生成一张简单的科幻图片...")
    
    result = generator.generate_image(
        "一个未来城市的夜景，霓虹灯光，高耸入云的建筑，赛博朋克风格",
        "./test_cover.png"
    )
    
    if result.get('success'):
        print(f"✅ 图片生成成功: {result.get('path')}")
    else:
        print(f"❌ 图片生成失败: {result.get('error')}")
    print()

def main():
    """主测试流程"""
    print("=" * 50)
    print("novel-no-social 模块测试")
    print("=" * 50)
    print()
    
    # 依次测试
    test_config()
    test_topic_search()
    test_outline_generation()
    # test_image_generation()  # 取消注释以测试实际生成
    
    print("=" * 50)
    print("所有测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
