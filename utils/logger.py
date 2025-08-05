#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日志工具模块

这个模块提供了日志记录功能。
"""

import os
import logging
from logging.handlers import RotatingFileHandler

# 日志级别映射
LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

# 默认日志格式
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 默认日志级别
DEFAULT_LOG_LEVEL = 'info'

# 默认日志目录
DEFAULT_LOG_DIR = 'logs'

# 应用日志名称
APP_LOGGER_NAME = 'web_generator'


def get_logger(name=None, level=None, log_format=None, log_dir=None):
    """
    获取日志记录器
    
    Args:
        name (str, optional): 日志记录器名称，默认为APP_LOGGER_NAME
        level (str, optional): 日志级别，可选值：debug, info, warning, error, critical
        log_format (str, optional): 日志格式
        log_dir (str, optional): 日志目录
        
    Returns:
        logging.Logger: 日志记录器
    """
    # 设置默认值
    name = name or APP_LOGGER_NAME
    level = level or DEFAULT_LOG_LEVEL
    log_format = log_format or DEFAULT_LOG_FORMAT
    log_dir = log_dir or DEFAULT_LOG_DIR
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    
    # 设置日志级别
    logger.setLevel(LOG_LEVELS.get(level.lower(), logging.INFO))
    
    # 如果已经有处理器，直接返回
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(log_format)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 创建文件处理器
    try:
        # 确保日志目录存在
        os.makedirs(log_dir, exist_ok=True)
        
        # 创建文件处理器
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, f'{name}.log'),
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"无法创建日志文件处理器: {e}")
    
    return logger


def setup_logger(name=None, level=None, log_format=None, log_dir=None):
    """
    设置并获取应用日志记录器
    
    这是一个便捷函数，用于设置和获取应用的主日志记录器。
    
    Args:
        name (str, optional): 日志记录器名称，默认为APP_LOGGER_NAME
        level (str, optional): 日志级别，可选值：debug, info, warning, error, critical
        log_format (str, optional): 日志格式
        log_dir (str, optional): 日志目录
        
    Returns:
        logging.Logger: 日志记录器
    """
    return get_logger(name, level, log_format, log_dir)