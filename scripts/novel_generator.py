#!/usr/bin/env python3
"""
小说生成核心模块
包括：选题收集、大纲生成、正文写作
使用 MiniMax M2.7 模型进行文本生成
"""
import json
import requests
from pathlib import Path
from datetime import datetime
from .config_loader import get_config


class NovelGenerator:
    """小说生成器"""
    
    def __init__(self):
        self.config = get_config()
        self.minimax_config = self.config.minimax
        self.tavily_config = self.config.tavily
    
    def search_topics(self, keywords: list = None) -> list:
        """
        搜索科幻/哲学/未来相关热点选题
        
        Args:
            keywords: 搜索关键词列表
            
        Returns:
            list: 备选选题列表
        """
        if keywords is None:
            keywords = ["人工智能", "量子计算", "星际探索", "赛博朋克", "哲学思考", 
                      "意识上传", "克隆技术", "元宇宙", "未来社会", "太空殖民"]
        
        # 使用 Tavily 搜索热点
        topics = []
        
        for kw in keywords:
            try:
                url = "https://api.tavily.com/search"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "api_key": self.tavily_config.get('token'),
                    "query": f"{kw} 最新动态 2024",
                    "search_depth": "basic",
                    "max_results": 3
                }
                
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                if response.status_code == 200:
                    results = response.json().get('results', [])
                    for r in results:
                        topics.append({
                            "keyword": kw,
                            "title": r.get('title', ''),
                            "url": r.get('url', ''),
                            "snippet": r.get('content', '')[:200]
                        })
            except Exception as e:
                print(f"搜索 {kw} 时出错: {e}")
                continue
        
        # 去重
        seen = set()
        unique_topics = []
        for t in topics:
            if t['title'] not in seen:
                seen.add(t['title'])
                unique_topics.append(t)
        
        return unique_topics[:10]
    
    def generate_outline(self, meta: dict, target_words: int = 2000) -> str:
        """
        生成故事大纲
        
        Args:
            meta: 小说设定元数据（包含人设、背景、风格等）
            target_words: 目标字数
            
        Returns:
            str: 包含章节规划的大纲文本
        """
        # 构建 prompt
        prompt = f"""你是一位资深的科幻小说作家。请根据以下设定，为一部科幻小说生成详细大纲。

## 小说标题
{meta.get('title', '未命名')}

## 题材类型
{meta.get('genre', '科幻')}

## 核心主题
{meta.get('theme', '')}

## 角色人设
{meta.get('characters', '')}

## 故事背景
{meta.get('setting', '')}

## 写作风格
{meta.get('style', '')}

## 故事走向
{meta.get('plot_direction', '')}

请生成一个包含 6-10 章的故事大纲，每章 4-8 话。

要求：
1. 每章有明确的核心冲突和悬念
2. 总字数约 {target_words} 字左右
3. 章节之间有递进关系
4. 每话结尾留有钩子，吸引读者继续阅读
5. 格式清晰，便于后续写作参考
"""
        
        response = self._call_minimax(prompt)
        return response
    
    def write_episode(self, meta: dict, chapter: int, episode: int, 
                     context: str = "", target_words: int = 3000) -> dict:
        """
        写作单话内容
        
        Args:
            meta: 小说设定元数据
            chapter: 章节编号
            episode: 话数编号
            context: 上下文（上一话内容，用于连贯性）
            target_words: 目标字数
            
        Returns:
            dict: 包含生成内容的字典
        """
        # 构建写作 prompt
        prompt = f"""你是，一位资深的科幻/哲学小说作家。请根据设定写作小说的一话内容。

## 小说基本信息
- 标题：{meta.get('title', '未命名')}
- 类型：{meta.get('genre', '科幻')}
- 主题：{meta.get('theme', '')}

## 角色人设
{meta.get('characters', '')}

## 故事背景
{meta.get('setting', '')}

## 写作风格要求
{meta.get('style', '')}

## 当前章节信息
- 当前章节：第 {chapter} 章
- 当前话数：第 {episode} 话

## 故事大纲（参考）
{meta.get('outline', '')}

## 上一话内容（用于连贯性）
{context}

## 写作要求
1. 写作第 {chapter} 章第 {episode} 话的内容
2. 字数：约 {target_words} 字
3. 每段 1-3 句话，避免过长段落
4. 对话要自然，符合角色性格
5. 结尾留有悬念/钩子
6. 无需写标题，直接写正文
7. 去 AI 味：避免"不是A，而是B"等机械句式

请直接输出正文内容。
"""
        
        content = self._call_minimax(prompt)
        return {
            "chapter": chapter,
            "episode": episode,
            "content": content,
            "word_count": len(content)
        }
    
    def _call_minimax(self, prompt: str) -> str:
        """
        调用 MiniMax API 进行文本生成
        
        Args:
            prompt: 对话 prompt
            
        Returns:
            str: 返回的文本内容
        """
        url = "https://api.minimaxi.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.minimax_config.get('token')}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "MiniMax-M2.7",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "max_tokens": 8192
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=300)
            response.raise_for_status()
            result = response.json()
            
            return result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
        except requests.exceptions.Timeout:
            print("API 调用超时，等待重试...")
            # 重试一次
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=300)
                response.raise_for_status()
                result = response.json()
                return result.get('choices', [{}])[0].get('message', {}).get('content', '')
            except Exception as e2:
                print(f"重试失败: {e2}")
                return f"Error: {e2}"
        except Exception as e:
            print(f"API 调用出错: {e}")
            return f"Error: {e}"
    
    def save_meta(self, novel_dir: Path, meta: dict) -> Path:
        """
        保存小说设定到 meta.md
        
        Args:
            novel_dir: 小说目录
            meta: 设定字典
            
        Returns:
            Path: meta.md 路径
        """
        meta_path = novel_dir / "meta.md"
        
        content = f"""# {meta.get('title', '未命名')}

> 创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 基本信息
- **题材类型**：{meta.get('genre', '')}
- **核心主题**：{meta.get('theme', '')}
- **写作风格**：{meta.get('style', '')}

## 角色人设

{meta.get('characters', '')}

## 故事背景

{meta.get('setting', '')}

## 故事走向

{meta.get('plot_direction', '')}

## 故事大纲

{meta.get('outline', '')}

---
*本文档是小说创作的核心上下文，每次写作前必须读取此文件*
"""
        
        with open(meta_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return meta_path
    
    def load_meta(self, meta_path: Path) -> dict:
        """
        加载 meta.md 内容
        
        Args:
            meta_path: meta.md 路径
            
        Returns:
            dict: 设定字典
        """
        with open(meta_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        meta = {"raw": content}
        return meta


def search_topics(keywords: list = None) -> list:
    """便捷函数：搜索热点选题"""
    generator = NovelGenerator()
    return generator.search_topics(keywords)


def generate_outline(meta: dict, target_words: int = 2000) -> str:
    """便捷函数：生成大纲"""
    generator = NovelGenerator()
    return generator.generate_outline(meta, target_words)


def write_episode(meta: dict, chapter: int, episode: int, 
                 context: str = "", target_words: int = 3000) -> dict:
    """便捷函数：写作单话"""
    generator = NovelGenerator()
    return generator.write_episode(meta, chapter, episode, context, target_words)


if __name__ == "__main__":
    # 测试
    generator = NovelGenerator()
    
    # 测试选题搜索
    print("=== 测试选题搜索 ===")
    topics = generator.search_topics()
    print(f"找到 {len(topics)} 个选题")
    
    # 测试大纲生成
    print("\n=== 测试大纲生成 ===")
    test_meta = {
        "title": "测试小说",
        "genre": "科幻",
        "theme": "人工智能觉醒",
        "characters": "主角：一个退役的AI研究员\n配角：一个具有自我意识的AI",
        "setting": "未来城市，AI已经融入日常生活",
        "style": "简洁有力，充满悬疑",
        "plot_direction": "AI逐渐觉醒，开始质疑人类"
    }
    outline = generator.generate_outline(test_meta)
    print(outline[:500] if len(outline) > 500 else outline)
