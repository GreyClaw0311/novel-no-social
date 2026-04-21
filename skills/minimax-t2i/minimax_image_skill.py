#!/usr/bin/env python3
"""
MiniMax 文生图 Skill
用于 OpenClaw 自动化调用 MiniMax image-01 模型生成小说配图
"""
import sys
import argparse
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.minimax_image import MiniMaxImageGenerator


def generate_cover(scene_desc: str, output_path: str = None) -> dict:
    """生成封面图"""
    gen = MiniMaxImageGenerator()
    
    if output_path is None:
        output_path = f"./generated_cover_{Path(scene_desc[:20]).stem}.png"
    
    result = gen.generate_cover(scene_desc, output_path)
    return result


def generate_scene(scene_desc: str, output_path: str = None, ref_image_path: str = None) -> dict:
    """生成场景插图"""
    gen = MiniMaxImageGenerator()
    
    if output_path is None:
        output_path = f"./generated_scene_{Path(scene_desc[:20]).stem}.png"
    
    result = gen.generate_scene(scene_desc, output_path, ref_image_path)
    return result


def generate_character(character_desc: str, output_path: str = None) -> dict:
    """生成角色形象图"""
    gen = MiniMaxImageGenerator()
    
    if output_path is None:
        output_path = f"./generated_character_{Path(character_desc[:20]).stem}.png"
    
    result = gen.generate_character(character_desc, output_path)
    return result


def generate_image(prompt: str, output_path: str = None) -> dict:
    """通用图片生成"""
    gen = MiniMaxImageGenerator()
    
    if output_path is None:
        output_path = f"./generated_{Path(prompt[:20]).stem}.png"
    
    result = gen.generate_image(prompt, output_path)
    return result


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='MiniMax 文生图 Skill')
    parser.add_argument('type', choices=['cover', 'scene', 'character', 'image'], 
                        help='图片类型')
    parser.add_argument('prompt', help='图片描述 prompt')
    parser.add_argument('--output', '-o', help='输出路径')
    parser.add_argument('--ref', '-r', help='参考图片路径（图生图时使用）')
    
    args = parser.parse_args()
    
    if args.type == 'cover':
        result = generate_cover(args.prompt, args.output)
    elif args.type == 'scene':
        result = generate_scene(args.prompt, args.output, args.ref)
    elif args.type == 'character':
        result = generate_character(args.prompt, args.output)
    else:
        result = generate_image(args.prompt, args.output)
    
    if result.get('success'):
        print(f"✅ 图片生成成功: {result.get('path')}")
        if result.get('url'):
            print(f"📎 URL: {result.get('url')}")
        return 0
    else:
        print(f"❌ 图片生成失败: {result.get('error')}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
