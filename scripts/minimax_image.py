#!/usr/bin/env python3
"""
MiniMax 文生图模块
基于 image-01 模型
API文档: https://platform.minimaxi.com/docs/api-reference/image-generation-t2i
"""
import requests
import json
import uuid
import base64
from pathlib import Path
from .config_loader import get_config


class MiniMaxImageGenerator:
    """MiniMax image-01 文生图生成器"""
    
    def __init__(self):
        self.config = get_config().minimax
        self.token = self.config.get('token')
        self.base_url = self.config.get('base_url', 'https://api.minimaxi.com')
        self.model = self.config.get('image_model', 'image-01')
        
    def generate_image(self, prompt: str, output_path: str = None) -> dict:
        """
        生成图片
        
        Args:
            prompt: 图片描述 prompt
            output_path: 输出路径，不指定则保存到当前目录
            
        Returns:
            dict: 包含 image_url 或 base64 数据
        """
        url = f"{self.base_url}/image_generation"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "image_size": "1:1",  # 1:1 方图适合小红书封面
            "prompt_extension": True  # 启用 prompt 优化
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            
            # 提取图片数据（支持 base64 或 URL）
            image_data = result.get('data', {})
            image_url = None
            
            # 优先使用 base64
            if image_data.get('image_base64'):
                image_bytes = base64.b64decode(image_data['image_base64'])
            # 其次使用 URL
            elif image_data.get('image_urls') and len(image_data['image_urls']) > 0:
                image_url = image_data['image_urls'][0]
                image_response = requests.get(image_url, timeout=120)
                image_response.raise_for_status()
                image_bytes = image_response.content
            else:
                return {
                    "success": False,
                    "error": "No image data in response",
                    "raw": result
                }
            
            # 保存到文件
            if output_path is None:
                output_path = f"./generated_{uuid.uuid4().hex[:8]}.png"
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(image_bytes)
            
            return {
                "success": True,
                "path": output_path,
                "url": image_url,
                "prompt": prompt
            }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_character(self, character_desc: str, output_path: str) -> dict:
        """
        生成角色形象图
        
        Args:
            character_desc: 角色描述（来自meta.md中的角色人设）
            output_path: 输出路径
            
        Returns:
            dict: 生成结果
        """
        # 构建角色形象的 prompt
        prompt = f"""
科幻小说角色形象，{character_desc}
风格：数字绘画，精细细节，电影感光照，高质量
正面视角，全身或半身都可以
"""
        return self.generate_image(prompt.strip(), output_path)
    
    def generate_cover(self, scene_desc: str, output_path: str) -> dict:
        """
        生成小说封面图
        
        Args:
            scene_desc: 场景描述（根据小说内容）
            output_path: 输出路径
            
        Returns:
            dict: 生成结果
        """
        prompt = f"""
科幻小说封面，{scene_desc}
风格：电影感构图，氛围感灯光，科幻未来风格，高质量插画
适合作为小说章节封面图
"""
        return self.generate_image(prompt.strip(), output_path)
    
    def generate_scene(self, scene_desc: str, output_path: str, ref_image_path: str = None) -> dict:
        """
        生成场景插图（支持图生图）
        
        Args:
            scene_desc: 场景描述
            output_path: 输出路径
            ref_image_path: 参考图片路径（用于保持风格一致）
            
        Returns:
            dict: 生成结果
        """
        if ref_image_path:
            return self.generate_with_reference(scene_desc, ref_image_path, output_path)
        else:
            return self.generate_cover(scene_desc, output_path)
    
    def generate_with_reference(self, prompt: str, ref_image_path: str, output_path: str) -> dict:
        """
        图生图 - 基于参考图生成新图
        
        Args:
            prompt: 图片描述
            ref_image_path: 参考图片路径
            output_path: 输出路径
            
        Returns:
            dict: 生成结果
        """
        url = f"{self.base_url}/image_to_image"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # 读取参考图片并转为 base64
        with open(ref_image_path, 'rb') as f:
            ref_image_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "input_image_base64": ref_image_base64,
            "image_size": "1:1",
            "prompt_extension": True
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            
            if result.get('data', {}).get('image_base64'):
                image_data = result['data']['image_base64']
                
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(base64.b64decode(image_data))
                
                return {
                    "success": True,
                    "path": output_path,
                    "prompt": prompt,
                    "reference": ref_image_path
                }
            else:
                return {
                    "success": False,
                    "error": "No image data in response",
                    "raw": result
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


def generate_image(prompt: str, output_path: str = None) -> dict:
    """便捷函数：生成单张图片"""
    generator = MiniMaxImageGenerator()
    return generator.generate_image(prompt, output_path)


def generate_character(character_desc: str, output_path: str) -> dict:
    """便捷函数：生成角色形象"""
    generator = MiniMaxImageGenerator()
    return generator.generate_character(character_desc, output_path)


def generate_cover(scene_desc: str, output_path: str) -> dict:
    """便捷函数：生成封面"""
    generator = MiniMaxImageGenerator()
    return generator.generate_cover(scene_desc, output_path)


def generate_scene(scene_desc: str, output_path: str, ref_image_path: str = None) -> dict:
    """便捷函数：生成场景图"""
    generator = MiniMaxImageGenerator()
    return generator.generate_scene(scene_desc, output_path, ref_image_path)


if __name__ == "__main__":
    # 测试
    import sys
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else "./test_output.png"
        result = generate_image(prompt, output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Usage: python minimax_image.py <prompt> [output_path]")
