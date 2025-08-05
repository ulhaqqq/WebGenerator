#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理模块

这个模块提供了配置管理功能，用于保存和加载用户配置。
"""

import os
import json
from utils.logger import get_logger

# 设置日志
logger = get_logger('config_manager')

# 默认配置文件路径
DEFAULT_CONFIG_PATH = os.path.expanduser('~/.web_generator_config.json')


class ConfigManager:
    """配置管理类"""
    
    def __init__(self, config_path=None):
        """初始化配置管理器
        
        Args:
            config_path (str, optional): 配置文件路径
        """
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置
        
        Returns:
            dict: 配置字典
        """
        if not os.path.exists(self.config_path):
            logger.info(f"配置文件 {self.config_path} 不存在，将使用默认配置")
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 确保配置包含所有必要的键
            default_config = self._get_default_config()
            for key in default_config:
                if key not in config:
                    config[key] = default_config[key]
                    logger.warning(f"配置中缺少 {key} 键，使用默认值: {default_config[key]}")
            
            logger.info(f"已从 {self.config_path} 加载配置")
            return config
        except Exception as e:
            logger.error(f"加载配置失败: {e}")
            return self._get_default_config()
    
    def _get_default_config(self):
        """获取默认配置
        
        Returns:
            dict: 默认配置字典
        """
        return {
            "framework": "flask",
            "database": "mysql",
            "redis": False,
            "docker": False,
            "testing": False,
            "api_docs": False,
            "auth": False,
            "project_name": "",
            "project_path": os.path.expanduser('~')
        }
    
    def save_config(self, config):
        """保存配置
        
        Args:
            config (dict): 配置字典
        
        Returns:
            bool: 是否保存成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            logger.info(f"配置已保存到 {self.config_path}")
            self.config = config
            return True
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            return False
    
    def get_config(self):
        """获取当前配置
        
        Returns:
            dict: 配置字典
        """
        return self.config
    
    def update_config(self, new_config):
        """更新配置
        
        Args:
            new_config (dict): 新配置字典
        
        Returns:
            bool: 是否更新成功
        """
        self.config.update(new_config)
        return self.save_config(self.config)