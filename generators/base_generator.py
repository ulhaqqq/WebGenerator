#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基础项目生成器

这个模块提供了一个基础生成器类，所有特定框架的生成器都继承自这个类。
"""

import os
import shutil
import json
import time
import subprocess
from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader
import jinja2.exceptions

from utils.logger import get_logger

logger = get_logger(__name__)


class BaseGenerator(ABC):
    """基础项目生成器类"""
    
    def __init__(self, config, progress_callback=None):
        """初始化生成器
        
        Args:
            config (dict): 项目配置
            progress_callback (callable, optional): 进度回调函数，用于报告生成进度
        """
        self.config = config
        self.project_name = config["project_name"]
        self.project_path = config["project_path"]
        self.full_path = os.path.join(self.project_path, self.project_name)
        self.database = config["database"]
        self.use_redis = config["redis"]
        self.use_docker = config["docker"]
        self.include_tests = config["tests"]
        self.include_api_docs = config["api_docs"]
        self.include_auth = config["auth"]
        
        # 进度回调函数
        self.progress_callback = progress_callback
        
        # 设置模板环境
        self.templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        
        # 初始化进度追踪
        self._last_progress = 0
    
    def generate(self):
        """生成项目"""
        logger.info(f"开始生成项目: {self.project_name}")
        
        # 定义总步骤数 - 增加更多的子步骤以使进度条更平滑
        total_steps = 10  # 基础步骤：创建目录(1)、生成结构(1)、基础文件(2)、框架文件(2)、数据库配置(1)、其他配置(3)
        
        current_step = 0
        
        # 报告进度函数 - 自动计算step_increment
        def report_progress(message, sub_step=None, total_sub_steps=None):
            nonlocal current_step
            
            # 如果是子步骤进度报告
            if sub_step is not None and total_sub_steps is not None:
                # 计算当前主步骤的进度百分比
                step_percentage = (current_step / total_steps) * 100
                # 计算下一个主步骤的进度百分比 - 假设每个主步骤增量为1
                next_step_percentage = ((current_step + 1) / total_steps) * 100
                # 计算当前子步骤的进度百分比
                sub_percentage = (sub_step / total_sub_steps) * (next_step_percentage - step_percentage)
                # 最终百分比 = 当前主步骤百分比 + 子步骤贡献的百分比
                progress = int(step_percentage + sub_percentage)
                # 确保进度值在0-100之间
                progress = max(0, min(100, progress))
                logger.debug(f"子步骤进度计算: 当前步骤百分比={step_percentage}, 下一步骤百分比={next_step_percentage}, 子步骤进度={sub_percentage}, 最终进度={progress}")
                # 确保进度值是递增的
                if hasattr(self, '_last_progress') and progress < self._last_progress:
                    progress = self._last_progress
                self._last_progress = progress
            else:
                # 如果是主步骤完成的进度报告
                current_step += 1  # 自动增加一个步骤
                progress = int((current_step / total_steps) * 100)
                # 确保进度值在0-100之间
                progress = max(0, min(100, progress))
                logger.debug(f"主步骤进度计算: 当前步骤={current_step}, 总步骤={total_steps}, 进度={progress}%")
                # 确保进度值是递增的
                if hasattr(self, '_last_progress') and progress < self._last_progress:
                    progress = self._last_progress
                self._last_progress = progress
            
            logger.info(f"[{progress}%] {message}")
            if self.progress_callback:
                # 传递参数给progress_callback，不使用关键字参数
                self.progress_callback(progress, message, sub_step, total_sub_steps)
                # 添加停顿，使进度更新更平滑
                import time
                time.sleep(0.3)  # 停顿0.3秒
        
        # 创建项目目录
        self._create_project_directory(report_progress)
        report_progress("创建项目目录完成")
        
        # 生成项目结构
        self._generate_project_structure(report_progress)
        current_step += 1
        report_progress("生成项目结构完成")
        
        # 生成基础文件
        self._generate_base_files(report_progress)
        current_step += 2
        report_progress("生成基础文件完成")
        
        # 生成框架特定文件
        self._generate_framework_files(report_progress)
        current_step += 2
        report_progress("生成框架特定文件完成")
        
        # 生成数据库配置
        self._generate_database_config(report_progress)
        current_step += 1
        report_progress("生成数据库配置完成")
        
        # 如果需要，生成Redis配置
        if self.use_redis:
            self._generate_redis_config(report_progress)
            current_step += 1
            report_progress("生成Redis配置完成")
        
        # 如果需要，生成Docker配置
        if self.use_docker:
            self._generate_docker_config(report_progress)
            current_step += 1
            report_progress("生成Docker配置完成")
        
        # 如果需要，生成测试框架
        if self.include_tests:
            self._generate_tests(report_progress)
            current_step += 1
            report_progress("生成测试框架完成")
        
        # 如果需要，生成API文档
        if self.include_api_docs:
            self._generate_api_docs(report_progress)
            current_step += 1
            report_progress("生成API文档完成")
        
        # 认证系统已禁用
        # if self.include_auth:
        #     self._generate_auth_system(report_progress)
        #     current_step += 1
        #     # 此时进度应该接近100%，但不是100%
        #     report_progress("生成用户认证系统完成")
        
        # 执行最终操作，确保所有文件都已写入
        time.sleep(0.5)  # 给文件系统一些时间完成所有写入操作
        
        # 最后一步，确保进度为100%
        logger.info(f"项目生成完成: {self.full_path}")
        # 强制设置进度为100%
        if self.progress_callback:
            self.progress_callback(100, "项目生成完毕！", 1, 1)
    
    def _create_project_directory(self, report_progress=None):
        """创建项目目录
        
        Args:
            report_progress: 报告进度的函数
        """
        os.makedirs(self.full_path, exist_ok=True)
        logger.debug(f"创建项目目录: {self.full_path}")
        
        # 如果没有提供report_progress函数，则使用self.progress_callback
        if report_progress is None:
            report_progress = self.progress_callback
        
        # 报告进度 - 创建项目根目录
        if report_progress:
            report_progress(f"创建项目根目录: {self.project_name}")
    
    def _generate_project_structure(self, report_progress):
        """生成项目结构
        
        Args:
            report_progress: 报告进度的函数
        """
        # 创建基本目录结构
        directories = [
            "app",
            "app/api",
            "app/models",
            "app/schemas",
            "app/services",
            "app/utils",
            "app/static",
            "app/static/css",
            "app/static/js",
            "app/static/img",
            "app/templates" if self._uses_templates() else None,
            "config",
            "docs",
            "migrations",
            "scripts",
            "tests" if self.include_tests else None,
        ]
        
        # 过滤掉None值
        directories = [d for d in directories if d is not None]
        
        # 报告进度 - 开始创建项目目录结构
        report_progress("准备创建项目目录结构...")
        
        # 创建目录
        for i, directory in enumerate(directories):
            os.makedirs(os.path.join(self.full_path, directory), exist_ok=True)
            logger.debug(f"创建目录: {directory}")
            
            # 每创建一个目录更新一次进度
            # 使用report_progress函数而不是直接调用self.progress_callback
            # 这样可以确保进度计算的一致性
            report_progress(f"创建目录: {directory}", sub_step=i+1, total_sub_steps=len(directories))
    
    def _generate_base_files(self, report_progress):
        """生成基础文件
        
        Args:
            report_progress: 报告进度的函数
        """
        # 获取框架名称（小写）
        framework_dir = "flask" if self.config["framework"] == "flask" else "fastapi"
        
        # 初始化子步骤进度计数
        total_files = 4  # 根据实际生成的文件数量调整
        current_file = 0
        
        # 报告进度 - 开始生成基础文件
        report_progress("开始生成基础文件...")
        
        # 生成README.md
        self._render_template(
            f"{framework_dir}/README.md.j2",
            os.path.join(self.full_path, "README.md"),
            project_name=self.project_name,
            framework=self._get_framework_name(),
            database=self._get_database_name(),
            use_redis=self.use_redis,
            use_docker=self.use_docker,
            include_tests=self.include_tests,
            include_api_docs=self.include_api_docs,
            include_auth=self.include_auth
        )
        
        # 报告进度 - README.md 生成完成
        current_file += 1
        report_progress("生成 README.md 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成.gitignore
        self._render_template(
            f"{framework_dir}/gitignore.j2",
            os.path.join(self.full_path, ".gitignore")
        )
        
        # 报告进度 - .gitignore 生成完成
        current_file += 1
        report_progress("生成 .gitignore 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成requirements.txt
        template_params = {
            "framework": self.config["framework"],
            "database": self.database,
            "use_redis": self.use_redis,
            "include_tests": self.include_tests,
            "include_api_docs": self.include_api_docs
        }
        
        # 设置db_type参数，用于模板中的数据库驱动选择
        template_params["db_type"] = self._get_db_type()
        
        self._render_template(
            f"{framework_dir}/requirements.txt.j2",
            os.path.join(self.full_path, "requirements.txt"),
            **template_params
        )
        
        # 报告进度 - requirements.txt 生成完成
        current_file += 1
        report_progress("生成 requirements.txt 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成.env文件
        self._render_template(
            f"{framework_dir}/env.j2",
            os.path.join(self.full_path, ".env"),
            project_name=self.project_name,
            database=self.database,
            use_redis=self.use_redis,
            db_type=self._get_db_type()
        )
        
        # 报告进度 - .env 文件生成完成
        current_file += 1
        report_progress("生成 .env 文件完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 更新总文件数量
        total_files = 5  # 只包含 run.py
        
        # 生成run.py
        self._render_template(
            f"{framework_dir}/run.py.j2",
            os.path.join(self.full_path, "run.py"),
            project_name=self.project_name
        )
        
        # 报告进度 - run.py 文件生成完成
        current_file += 1
        report_progress("生成 run.py 文件完成", sub_step=current_file, total_sub_steps=total_files)
    
    def _render_template(self, template_path, output_path, **kwargs):
        """渲染模板并写入文件
        
        Args:
            template_path (str): 模板路径
            output_path (str): 输出文件路径
            **kwargs: 传递给模板的变量
        """
        try:
            template = self.env.get_template(template_path)
            content = template.render(**kwargs)
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 写入文件
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            logger.debug(f"生成文件: {os.path.relpath(output_path, self.full_path)}")
        except Exception as e:
            logger.error(f"渲染模板 {template_path} 失败: {str(e)}")
            raise
    
    def _get_framework_name(self):
        """获取框架名称"""
        framework_names = {
            "flask": "Flask",
            "fastapi": "FastAPI"
        }
        return framework_names.get(self.config["framework"], self.config["framework"])
    
    def _get_database_name(self):
        """获取数据库名称"""
        database_names = {
            "mysql": "MySQL",
            "postgres": "PostgreSQL"
        }
        return database_names.get(self.database, self.database)
    
    def _get_db_type(self):
        """获取数据库类型，用于模板渲染"""
        if "db_type" in self.config:
            return self.config["db_type"]
        else:
            # 根据database配置自动设置db_type
            db_type_mapping = {
                "mysql": "mysql",
                "postgresql": "postgresql",
                "postgres": "postgresql",
                "sqlalchemy": "sqlite"  # 默认SQLite
            }
            return db_type_mapping.get(self.database, "sqlite")
    
    @abstractmethod
    def _uses_templates(self):
        """框架是否使用模板"""
        pass
    
    @abstractmethod
    def _generate_framework_files(self, report_progress=None):
        """生成框架特定文件
        
        Args:
            report_progress: 报告进度的函数
        """
        pass
    
    @abstractmethod
    def _generate_database_config(self, report_progress=None):
        """生成数据库配置
        
        Args:
            report_progress: 报告进度的函数
        """
        pass
    
    @abstractmethod
    def _generate_redis_config(self, report_progress=None):
        """生成Redis配置
        
        Args:
            report_progress: 报告进度的函数
        """
        pass
    
    @abstractmethod
    def _generate_docker_config(self, report_progress=None):
        """生成Docker配置
        
        Args:
            report_progress: 报告进度的函数
        """
        pass
    
    @abstractmethod
    def _generate_tests(self, report_progress=None):
        """生成测试框架
        
        Args:
            report_progress: 报告进度的函数
        """
        pass
    
    @abstractmethod
    def _generate_api_docs(self, report_progress=None):
        """生成API文档
        
        Args:
            report_progress: 报告进度的函数
        """
        pass
    
    # 认证系统已被完全移除
    # def _generate_auth_system(self, report_progress=None):
    #     """生成用户认证系统
    #     
    #     Args:
    #         report_progress: 报告进度的函数
    #     """
    #     pass