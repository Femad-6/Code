"""
日志工具模块
提供统一的日志记录功能
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class Logger:
    """日志记录器单例类"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._configure()
        return cls._instance
    
    @staticmethod
    def _configure():
        """配置日志记录器"""
        cls = Logger
        
        # 创建日志目录
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 配置根日志记录器
        cls.logger = logging.getLogger('VehicleDroneDelivery')
        cls.logger.setLevel(logging.DEBUG)
        
        # 清除现有处理器
        cls.logger.handlers.clear()
        
        # 文件处理器
        log_file = os.path.join(log_dir, 'vehicle_drone_delivery.log')
        cls.file_handler = RotatingFileHandler(
            log_file, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8'
        )
        cls.file_handler.setLevel(logging.DEBUG)
        
        # 控制台处理器
        cls.stream_handler = logging.StreamHandler()
        cls.stream_handler.setLevel(logging.INFO)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        cls.file_handler.setFormatter(formatter)
        cls.stream_handler.setFormatter(formatter)
        
        # 添加处理器
        cls.logger.addHandler(cls.file_handler)
        cls.logger.addHandler(cls.stream_handler)
    
    @staticmethod
    def debug(message: str):
        """记录调试信息"""
        Logger.logger.debug(message)
    
    @staticmethod
    def info(message: str):
        """记录信息"""
        Logger.logger.info(message)
    
    @staticmethod
    def warning(message: str):
        """记录警告"""
        Logger.logger.warning(message)
    
    @staticmethod
    def error(message: str):
        """记录错误"""
        Logger.logger.error(message)
    
    @staticmethod
    def critical(message: str):
        """记录严重错误"""
        Logger.logger.critical(message)
    
    @staticmethod
    def get_logger():
        """获取日志记录器实例"""
        return Logger.logger

def get_logger(name: str = 'VehicleDroneDelivery') -> logging.Logger:
    """
    获取指定名称的日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        日志记录器实例
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # 如果该名称的日志记录器没有处理器，使用默认配置
        logger.setLevel(logging.DEBUG)
        
        # 创建日志目录
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 文件处理器
        log_file = os.path.join(log_dir, f'{name.lower()}.log')
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 控制台处理器
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        
        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    
    return logger

# 创建默认日志记录器实例
default_logger = Logger()



