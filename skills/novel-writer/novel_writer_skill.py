#!/usr/bin/env python3
"""
小说写作 Skill
用于 OpenClaw 自动化调用 AI 生成小说内容
"""
import sys
import argparse
from pathlib import Path
import json

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.novel_generator import NovelGenerator


def search_topics(keywords: list = None) -> list:
    """搜索选题"""
    gen = NovelGenerator()
    topics = gen.search_topics(keywords)
    return topics


def generate_outline(meta: dict) -> str:
    """生成大纲"""
    gen = NovelGenerator()
    outline = gen.generate_outline(meta)
    return outline


def write_episode(meta: dict, chapter: int, episode: int, context: str = "") -> dict:
    """写作单话"""
    gen = NovelGenerator()
    result = gen.write_episode(meta, chapter, episode, context)
    return result


def save_meta(novel_name: str, meta: dict) -> Path:
    """保存小说设定"""
    from scripts.novel_generator import NovelGenerator
    gen = NovelGenerator()
    novel_dir = Path(__file__).parent.parent.parent / "novels" / novel_name
    path = gen.save_meta(novel_dir, meta)
    return path


def load_meta(meta_path: Path) -> dict:
    """加载小说设定"""
    from scripts.novel_generator import NovelGenerator
    gen = NovelGenerator()
    meta = gen.load_meta(meta_path)
    return meta


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='小说写作 Skill')
    parser.add_argument('action', choices=['topics', 'outline', 'write', 'save-meta'],
                        help='操作类型')
    parser.add_argument('--keywords', '-k', nargs='+', help='搜索关键词')
    parser.add_argument('--title', '-t', help='小说标题')
    parser.add_argument('--chapter', '-c', type=int, help='章节号')
    parser.add_argument('--episode', '-e', type=int, help='话数')
    parser.add_argument('--context', help='上下文（上一话内容）')
    parser.add_argument('--meta', '-m', help='meta.json 路径')
    
    args = parser.parse_args()
    
    if args.action == 'topics':
        keywords = args.keywords or ["人工智能", "量子计算", "赛博朋克"]
        topics = search_topics(keywords)
        print(f"找到 {len(topics)} 个选题:")
        for i, t in enumerate(topics, 1):
            print(f"{i}. {t.get('title', 'N/A')}")
        return 0
    
    elif args.action == 'outline':
        if not args.meta:
            print("错误: 需要指定 --meta 参数")
            return 1
        meta = load_meta(Path(args.meta))
        outline = generate_outline(meta)
        print("生成的大纲:")
        print(outline)
        return 0
    
    elif args.action == 'write':
        if not args.meta or not args.chapter or not args.episode:
            print("错误: 需要指定 --meta, --chapter, --episode 参数")
            return 1
        meta = load_meta(Path(args.meta))
        result = write_episode(meta, args.chapter, args.episode, args.context or "")
        print(f"第{result['chapter']}章第{result['episode']}话:")
        print(f"字数: {result['word_count']}")
        print("---")
        print(result['content'][:500] + "...")
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
