#!/usr/bin/env python3
"""
配置加载模块
"""
import os
import yaml
from pathlib import Path

class Config:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
    
    @property
    def minimax(self):
        return self._config.get('minimax', {})
    
    @property
    def qwen(self):
        return self._config.get('qwen', {})
    
    @property
    def tavily(self):
        return self._config.get('tavily', {})
    
    @property
    def writing(self):
        return self._config.get('writing', {})
    
    @property
    def publish(self):
        return self._config.get('publish', {})
    
    def get(self, key, default=None):
        return self._config.get(key, default)


def get_config():
    """获取配置单例"""
    return Config()
