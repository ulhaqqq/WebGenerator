#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flask项目生成器

这个模块提供了Flask项目的生成器类。
"""

import os
from generators.base_generator import BaseGenerator
from utils.logger import get_logger

logger = get_logger(__name__)


class FlaskGenerator(BaseGenerator):
    """Flask项目生成器类"""
    
    def _uses_templates(self):
        """Flask使用模板"""
        return True
    
    def _generate_framework_files(self, report_progress=None):
        """生成Flask框架特定文件"""
        logger.info("生成Flask框架文件")
        
        # 定义总共需要生成的文件数量
        total_files = 12  # 根据实际生成的文件数量调整
        current_file = 0
        
        # 使用传入的report_progress函数或默认使用self.progress_callback
        if report_progress is None:
            report_progress = lambda message, sub_step=None, total_sub_steps=None: \
                self.progress_callback(message, sub_step=sub_step, total_sub_steps=total_sub_steps)
        
        # 报告进度 - 开始生成Flask框架文件
        report_progress("开始生成Flask框架文件...", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/__init__.py
        self._render_template(
            "flask/app_init.py.j2",
            os.path.join(self.full_path, "app", "__init__.py"),
            project_name=self.project_name,
            use_redis=self.use_redis,
            include_auth=False
        )
        
        # 报告进度 - app/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/api/__init__.py
        self._render_template(
            "flask/api_init.py.j2",
            os.path.join(self.full_path, "app", "api", "__init__.py")
        )
        
        # 报告进度 - app/api/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/api/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/api/routes.py
        self._render_template(
            "flask/api_routes.py.j2",
            os.path.join(self.full_path, "app", "api", "routes.py"),
            include_auth=False
        )
        
        # 报告进度 - app/api/routes.py 生成完成
        current_file += 1
        report_progress("生成 app/api/routes.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/models/__init__.py
        self._render_template(
            "flask/models_init.py.j2",
            os.path.join(self.full_path, "app", "models", "__init__.py")
        )
        
        # 报告进度 - app/models/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/models/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/models/base.py
        self._render_template(
            "flask/models_base.py.j2",
            os.path.join(self.full_path, "app", "models", "base.py"),
            database=self.database
        )
        
        # 报告进度 - app/models/base.py 生成完成
        current_file += 1
        report_progress("生成 app/models/base.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/schemas/__init__.py
        self._render_template(
            "flask/schemas_init.py.j2",
            os.path.join(self.full_path, "app", "schemas", "__init__.py")
        )
        
        # 报告进度 - app/schemas/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/schemas/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/services/__init__.py
        self._render_template(
            "flask/services_init.py.j2",
            os.path.join(self.full_path, "app", "services", "__init__.py")
        )
        
        # 报告进度 - app/services/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/services/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/utils/__init__.py
        self._render_template(
            "flask/utils_init.py.j2",
            os.path.join(self.full_path, "app", "utils", "__init__.py")
        )
        
        # 报告进度 - app/utils/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/utils/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/utils/helpers.py
        self._render_template(
            "flask/utils_helpers.py.j2",
            os.path.join(self.full_path, "app", "utils", "helpers.py")
        )
        
        # 报告进度 - app/utils/helpers.py 生成完成
        current_file += 1
        report_progress("生成 app/utils/helpers.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/templates/index.html
        self._render_template(
            "flask/templates_index.html.j2",
            os.path.join(self.full_path, "app", "templates", "index.html"),
            project_name=self.project_name
        )
        
        # 报告进度 - app/templates/index.html 生成完成
        current_file += 1
        report_progress("生成 app/templates/index.html 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/templates/base.html
        from datetime import datetime
        self._render_template(
            "flask/templates_base.html.j2",
            os.path.join(self.full_path, "app", "templates", "base.html"),
            project_name=self.project_name,
            now=datetime.now()
        )
        
        # 报告进度 - app/templates/base.html 生成完成
        current_file += 1
        report_progress("生成 app/templates/base.html 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/static/css/style.css
        self._render_template(
            "flask/static_css_style.css.j2",
            os.path.join(self.full_path, "app", "static", "css", "style.css")
        )
        
        # 报告进度 - app/static/css/style.css 生成完成
        current_file += 1
        report_progress("生成 app/static/css/style.css 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/static/js/main.js
        self._render_template(
            "flask/static_js_main.js.j2",
            os.path.join(self.full_path, "app", "static", "js", "main.js")
        )
        
        # 报告进度 - app/static/js/main.js 生成完成
        current_file += 1
        report_progress("生成 app/static/js/main.js 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成config/__init__.py
        self._render_template(
            "flask/config_init.py.j2",
            os.path.join(self.full_path, "config", "__init__.py")
        )
        
        # 报告进度 - config/__init__.py 生成完成
        current_file += 1
        report_progress("生成 config/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成config/settings.py
        self._render_template(
            "flask/config_settings.py.j2",
            os.path.join(self.full_path, "config", "settings.py"),
            project_name=self.project_name,
            database=self.database,
            use_redis=self.use_redis
        )
        
        # 报告进度 - config/settings.py 生成完成
        current_file += 1
        report_progress("生成 config/settings.py 完成", sub_step=current_file, total_sub_steps=total_files)
    
    def _generate_database_config(self, report_progress=None):
        """生成数据库配置"""
        logger.info(f"生成{self._get_database_name()}数据库配置")
        
        # 如果没有提供report_progress函数，使用默认的progress_callback
        if report_progress is None:
            # 创建一个不使用关键字参数的lambda函数
            report_progress = lambda msg, sub_step=None, total_sub_steps=None: self.progress_callback(
                msg, sub_step=sub_step, total_sub_steps=total_sub_steps
            )
        
        # 初始化子步骤进度计数
        total_files = 3  # 根据实际生成的文件数量调整
        current_file = 0
        
        # 报告进度 - 开始生成数据库配置
        report_progress(f"开始生成{self._get_database_name()}数据库配置...", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/models/database.py
        self._render_template(
            f"flask/models_database_{self.database}.py.j2",
            os.path.join(self.full_path, "app", "models", "database.py"),
            project_name=self.project_name
        )
        
        # 报告进度 - app/models/database.py 生成完成
        current_file += 1
        report_progress("生成 app/models/database.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成migrations/README.md
        self._render_template(
            "flask/migrations_readme.md.j2",
            os.path.join(self.full_path, "migrations", "README.md")
        )
        
        # 报告进度 - migrations/README.md 生成完成
        current_file += 1
        report_progress("生成 migrations/README.md 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成scripts/db_init.py
        self._render_template(
            f"flask/scripts_db_init_{self.database}.py.j2",
            os.path.join(self.full_path, "scripts", "db_init.py"),
            project_name=self.project_name
        )
        
        # 报告进度 - 数据库配置生成完成
        current_file += 1
        report_progress(f"{self._get_database_name()}数据库配置生成完成", sub_step=current_file, total_sub_steps=total_files)
    
    def _generate_redis_config(self, report_progress=None):
        """生成Redis配置"""
        # 如果没有提供report_progress函数，使用默认的progress_callback
        if report_progress is None:
            # 创建一个不使用关键字参数的lambda函数
            report_progress = lambda msg, sub_step=None, total_sub_steps=None: self.progress_callback(
                msg, sub_step=sub_step, total_sub_steps=total_sub_steps
            )
        logger.info("生成Redis缓存配置")
        
        # 初始化子步骤进度计数
        total_files = 1  # 根据实际生成的文件数量调整
        current_file = 0
        
        # 报告进度 - 开始生成Redis配置
        report_progress("开始生成Redis缓存配置...", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/utils/redis_client.py
        self._render_template(
            "flask/utils_redis_client.py.j2",
            os.path.join(self.full_path, "app", "utils", "redis_client.py")
        )
        
        # 报告进度 - Redis配置生成完成
        current_file += 1
        report_progress("Redis缓存配置生成完成", sub_step=current_file, total_sub_steps=total_files)
    
    def _generate_docker_config(self, report_progress=None):
        """生成Docker配置"""
        logger.info("生成Docker配置")
        
        # 如果没有提供report_progress函数，使用默认的progress_callback
        if report_progress is None:
            report_progress = lambda msg, sub_step=None, total_sub_steps=None: self.progress_callback(
                msg, sub_step=sub_step, total_sub_steps=total_sub_steps
            )
        
        # 初始化子步骤进度计数
        total_files = 3  # 根据实际生成的文件数量调整
        current_file = 0
        
        # 报告进度 - 开始生成Docker配置
        report_progress("开始生成Docker配置...", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成Dockerfile
        self._render_template(
            "flask/dockerfile.j2",
            os.path.join(self.full_path, "Dockerfile"),
            project_name=self.project_name
        )
        
        # 报告进度 - Dockerfile 生成完成
        current_file += 1
        report_progress("生成 Dockerfile 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成docker-compose.yml
        self._render_template(
            "flask/docker-compose.yml.j2",
            os.path.join(self.full_path, "docker-compose.yml"),
            project_name=self.project_name,
            database=self.database,
            use_redis=self.use_redis
        )
        
        # 报告进度 - docker-compose.yml 生成完成
        current_file += 1
        report_progress("生成 docker-compose.yml 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成.dockerignore
        self._render_template(
            "flask/dockerignore.j2",
            os.path.join(self.full_path, ".dockerignore")
        )
        
        # 报告进度 - Docker配置生成完成
        current_file += 1
        report_progress("Docker配置生成完成", sub_step=current_file, total_sub_steps=total_files)
    
    def _generate_tests(self, report_progress=None):
        """生成测试框架"""
        logger.info("生成测试框架")
        
        # 如果没有提供report_progress函数，使用默认的progress_callback
        if report_progress is None:
            report_progress = lambda msg, sub_step=None, total_sub_steps=None: self.progress_callback(
                msg, sub_step=sub_step, total_sub_steps=total_sub_steps
            )
        
        # 初始化子步骤进度计数
        total_files = 4  # 根据实际生成的文件数量调整
        current_file = 0
        
        # 报告进度 - 开始生成测试框架
        report_progress("开始生成测试框架...", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成tests/__init__.py
        self._render_template(
            "flask/tests_init.py.j2",
            os.path.join(self.full_path, "tests", "__init__.py")
        )
        
        # 报告进度 - tests/__init__.py 生成完成
        current_file += 1
        report_progress("生成 tests/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成tests/conftest.py
        self._render_template(
            "flask/tests_conftest.py.j2",
            os.path.join(self.full_path, "tests", "conftest.py"),
            project_name=self.project_name
        )
        
        # 报告进度 - tests/conftest.py 生成完成
        current_file += 1
        report_progress("生成 tests/conftest.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成tests/test_api.py
        self._render_template(
            "flask/tests_test_api.py.j2",
            os.path.join(self.full_path, "tests", "test_api.py")
        )
        
        # 报告进度 - tests/test_api.py 生成完成
        current_file += 1
        report_progress("生成 tests/test_api.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成pytest.ini
        self._render_template(
            "flask/pytest.ini.j2",
            os.path.join(self.full_path, "pytest.ini"),
            project_name=self.project_name
        )
        
        # 报告进度 - 测试框架生成完成
        current_file += 1
        report_progress("测试框架生成完成", sub_step=current_file, total_sub_steps=total_files)
    
    def _generate_api_docs(self, report_progress=None):
        """生成API文档"""
        logger.info("生成API文档")
        
        # 如果没有提供report_progress函数，使用默认的progress_callback
        if report_progress is None:
            report_progress = lambda msg, sub_step=None, total_sub_steps=None: self.progress_callback(
                msg, sub_step=sub_step, total_sub_steps=total_sub_steps
            )
        
        # 初始化子步骤进度计数
        total_files = 3  # 根据实际生成的文件数量调整
        current_file = 0
        
        # 报告进度 - 开始生成API文档
        report_progress("开始生成API文档...", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成docs/api.md
        self._render_template(
            "flask/docs_api.md.j2",
            os.path.join(self.full_path, "docs", "api.md"),
            project_name=self.project_name
        )
        
        # 报告进度 - docs/api.md 生成完成
        current_file += 1
        report_progress("生成 docs/api.md 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成docs/index.md
        self._render_template(
            "flask/docs_index.md.j2",
            os.path.join(self.full_path, "docs", "index.md"),
            project_name=self.project_name,
            framework=self._get_framework_name(),
            database=self._get_database_name()
        )
        
        # 报告进度 - docs/index.md 生成完成
        current_file += 1
        report_progress("生成 docs/index.md 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成mkdocs.yml
        self._render_template(
            "flask/mkdocs.yml.j2",
            os.path.join(self.full_path, "mkdocs.yml"),
            project_name=self.project_name
        )
        
        # 报告进度 - API文档生成完成
        current_file += 1
        report_progress("API文档生成完成", sub_step=current_file, total_sub_steps=total_files)
    
    # 认证系统已移除
    # def _generate_auth_system(self, report_progress=None):
    #     pass
        
        #     pass
        
        # 最终进度报告
        if report_progress == self.progress_callback:
            self.progress_callback(9, "项目生成完毕！")
        else:
            report_progress("项目生成完毕！")