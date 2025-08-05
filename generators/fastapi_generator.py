#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FastAPI项目生成器

这个模块提供了FastAPI项目的生成器类。
"""

import os
from generators.base_generator import BaseGenerator
from utils.logger import get_logger

logger = get_logger(__name__)


class FastAPIGenerator(BaseGenerator):
    """FastAPI项目生成器类"""
    
    def _uses_templates(self):
        """FastAPI不使用模板"""
        return False
    
    def _generate_framework_files(self, report_progress=None):
        """生成FastAPI框架特定文件
        
        Args:
            report_progress: 报告进度的函数
        """
        logger.info("生成FastAPI框架文件")
        
        # 如果没有提供report_progress函数，则使用self.progress_callback
        if report_progress is None:
            # 创建一个不使用关键字参数的lambda函数
            report_progress = lambda msg, sub_step=None, total_sub_steps=None: self.progress_callback(
                msg, sub_step=sub_step, total_sub_steps=total_sub_steps
            )
        
        # 定义总共需要生成的文件数量
        # 基础文件 + api_v1 结构文件 (包括 __init__.py, api.py, endpoints/__init__.py, health.py, items.py)
        total_files = 14
        current_file = 0
        
        # 报告进度 - 开始生成FastAPI框架文件
        report_progress("开始生成FastAPI框架文件...", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/__init__.py
        self._render_template(
            "fastapi/app_init.py.j2",
            os.path.join(self.full_path, "app", "__init__.py")
        )
        
        # 报告进度 - app/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/main.py
        self._render_template(
            "fastapi/app_main.py.j2",
            os.path.join(self.full_path, "app", "main.py"),
            project_name=self.project_name,
            use_redis=self.use_redis,
            include_auth=False,
            include_api_docs=self.include_api_docs
        )
        
        # 报告进度 - app/main.py 生成完成
        current_file += 1
        report_progress("生成 app/main.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/api/__init__.py
        self._render_template(
            "fastapi/api_init.py.j2",
            os.path.join(self.full_path, "app", "api", "__init__.py")
        )
        
        # 报告进度 - app/api/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/api/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/api/endpoints.py
        self._render_template(
            "fastapi/api_endpoints.py.j2",
            os.path.join(self.full_path, "app", "api", "endpoints.py"),
            include_auth=False
        )
        
        # 报告进度 - app/api/endpoints.py 生成完成
        current_file += 1
        report_progress("生成 app/api/endpoints.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/api/deps.py
        self._render_template(
            "fastapi/api_deps.py.j2",
            os.path.join(self.full_path, "app", "api", "deps.py"),
            include_auth=False
        )
        
        # 报告进度 - app/api/deps.py 生成完成
        current_file += 1
        report_progress("生成 app/api/deps.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/api/v1/__init__.py
        self._render_template(
            "fastapi/api_init.py.j2",
            os.path.join(self.full_path, "app", "api", "v1", "__init__.py")
        )
        
        # 报告进度 - app/api/v1/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/api/v1/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/api/v1/api.py
        self._render_template(
            "fastapi/api_v1_api.py.j2",
            os.path.join(self.full_path, "app", "api", "v1", "api.py"),
            use_auth=False
        )
        
        # 报告进度 - app/api/v1/api.py 生成完成
        current_file += 1
        report_progress("生成 app/api/v1/api.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/api/v1/endpoints/__init__.py
        self._render_template(
            "fastapi/api_init.py.j2",
            os.path.join(self.full_path, "app", "api", "v1", "endpoints", "__init__.py")
        )
        
        # 报告进度 - app/api/v1/endpoints/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/api/v1/endpoints/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/api/v1/endpoints/health.py
        self._render_template(
            "fastapi/endpoints_health.py.j2",
            os.path.join(self.full_path, "app", "api", "v1", "endpoints", "health.py")
        )
        
        # 报告进度 - app/api/v1/endpoints/health.py 生成完成
        current_file += 1
        report_progress("生成 app/api/v1/endpoints/health.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/api/v1/endpoints/items.py
        self._render_template(
            "fastapi/endpoints_items.py.j2",
            os.path.join(self.full_path, "app", "api", "v1", "endpoints", "items.py"),
            use_auth=False
        )
        
        # 报告进度 - app/api/v1/endpoints/items.py 生成完成
        current_file += 1
        report_progress("生成 app/api/v1/endpoints/items.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 认证功能已移除
        
        # 生成app/models/__init__.py
        self._render_template(
            "fastapi/models_init.py.j2",
            os.path.join(self.full_path, "app", "models", "__init__.py")
        )
        
        # 报告进度 - app/models/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/models/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/models/base.py
        self._render_template(
            "fastapi/models_base.py.j2",
            os.path.join(self.full_path, "app", "models", "base.py")
        )
        
        # 报告进度 - app/models/base.py 生成完成
        current_file += 1
        report_progress("生成 app/models/base.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/models/item.py
        self._render_template(
            "fastapi/models_item.py.j2",
            os.path.join(self.full_path, "app", "models", "item.py"),
            use_auth=False
        )
        
        # 报告进度 - app/models/item.py 生成完成
        current_file += 1
        report_progress("生成 app/models/item.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/schemas/__init__.py
        self._render_template(
            "fastapi/schemas_init.py.j2",
            os.path.join(self.full_path, "app", "schemas", "__init__.py")
        )
        
        # 报告进度 - app/schemas/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/schemas/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/schemas/base.py
        self._render_template(
            "fastapi/schemas_base.py.j2",
            os.path.join(self.full_path, "app", "schemas", "base.py")
        )
        
        # 报告进度 - app/schemas/base.py 生成完成
        current_file += 1
        report_progress("生成 app/schemas/base.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/schemas/item.py
        self._render_template(
            "fastapi/schemas_item.py.j2",
            os.path.join(self.full_path, "app", "schemas", "item.py"),
            use_auth=False
        )
        
        # 报告进度 - app/schemas/item.py 生成完成
        current_file += 1
        report_progress("生成 app/schemas/item.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/crud/__init__.py
        self._render_template(
            "fastapi/crud_init.py.j2",
            os.path.join(self.full_path, "app", "crud", "__init__.py")
        )
        
        # 报告进度 - app/crud/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/crud/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/crud/base.py
        self._render_template(
            "fastapi/crud_base.py.j2",
            os.path.join(self.full_path, "app", "crud", "base.py")
        )
        
        # 报告进度 - app/crud/base.py 生成完成
        current_file += 1
        report_progress("生成 app/crud/base.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/crud/item.py
        self._render_template(
            "fastapi/crud_item.py.j2",
            os.path.join(self.full_path, "app", "crud", "item.py"),
            use_auth=False
        )
        
        # 报告进度 - app/crud/item.py 生成完成
        current_file += 1
        report_progress("生成 app/crud/item.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/services/__init__.py
        self._render_template(
            "fastapi/services_init.py.j2",
            os.path.join(self.full_path, "app", "services", "__init__.py")
        )
        
        # 报告进度 - app/services/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/services/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/utils/__init__.py
        self._render_template(
            "fastapi/utils_init.py.j2",
            os.path.join(self.full_path, "app", "utils", "__init__.py")
        )
        
        # 报告进度 - app/utils/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/utils/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/utils/helpers.py
        self._render_template(
            "fastapi/utils_helpers.py.j2",
            os.path.join(self.full_path, "app", "utils", "helpers.py")
        )
        
        # 报告进度 - app/utils/helpers.py 生成完成
        current_file += 1
        report_progress("生成 app/utils/helpers.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成config/__init__.py
        self._render_template(
            "fastapi/config_init.py.j2",
            os.path.join(self.full_path, "config", "__init__.py")
        )
        
        # 报告进度 - config/__init__.py 生成完成
        current_file += 1
        report_progress("生成 config/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成config/settings.py
        self._render_template(
            "fastapi/config_settings.py.j2",
            os.path.join(self.full_path, "config", "settings.py"),
            project_name=self.project_name,
            database=self.database,
            use_redis=self.use_redis
        )
        
        # 报告进度 - config/settings.py 生成完成
        current_file += 1
        report_progress("生成 config/settings.py 完成", sub_step=current_file, total_sub_steps=total_files)
            
        # 报告进度 - 所有框架文件生成完成
        report_progress("所有框架文件生成完成", sub_step=total_files, total_sub_steps=total_files)
    
    def _generate_database_config(self, report_progress=None):
        """生成数据库配置
        
        Args:
            report_progress: 报告进度的函数
        """
        logger.info(f"生成{self._get_database_name()}数据库配置")
        
        # 如果没有提供report_progress函数，则使用self.progress_callback
        if report_progress is None:
            # 创建一个不使用关键字参数的lambda函数
            report_progress = lambda msg, sub_step=None, total_sub_steps=None: self.progress_callback(
                msg, sub_step=sub_step, total_sub_steps=total_sub_steps
            )
        
        # 定义总共需要生成的文件数量
        total_files = 7
        current_file = 0
        
        # 报告进度 - 开始生成数据库配置
        report_progress(f"开始生成{self._get_database_name()}数据库配置...", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/db/__init__.py
        self._render_template(
            "fastapi/db_init.py.j2",
            os.path.join(self.full_path, "app", "db", "__init__.py")
        )
        
        # 报告进度 - app/db/__init__.py 生成完成
        current_file += 1
        report_progress("生成 app/db/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 创建db目录
        os.makedirs(os.path.join(self.full_path, "app", "db"), exist_ok=True)
        
        # 生成app/db/session.py
        # 映射数据库类型到正确的模板文件名
        db_template_map = {
            'sqlite': 'sqlalchemy',
            'mysql': 'mysql',
            'postgresql': 'sqlalchemy',
            'mongodb': 'mongodb'
        }
        db_template = db_template_map.get(self.database, 'sqlalchemy')
        self._render_template(
            f"fastapi/db_session_{db_template}.py.j2",
            os.path.join(self.full_path, "app", "db", "session.py"),
            project_name=self.project_name
        )
        
        # 报告进度 - app/db/session.py 生成完成
        current_file += 1
        report_progress("生成 app/db/session.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/db/base.py
        self._render_template(
            "fastapi/db_base.py.j2",
            os.path.join(self.full_path, "app", "db", "base.py")
        )
        
        # 报告进度 - app/db/base.py 生成完成
        current_file += 1
        report_progress("生成 app/db/base.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成migrations/README.md
        self._render_template(
            "fastapi/migrations_readme.md.j2",
            os.path.join(self.full_path, "migrations", "README.md")
        )
        
        # 创建alembic/versions目录
        os.makedirs(os.path.join(self.full_path, "alembic", "versions"), exist_ok=True)
        
        # 生成alembic/env.py
        self._render_template(
            "fastapi/alembic_env.py.j2",
            os.path.join(self.full_path, "alembic", "env.py"),
            use_auth=False
        )
        
        # 生成alembic/script.py.mako
        self._render_template(
            "fastapi/alembic_script.py.mako.j2",
            os.path.join(self.full_path, "alembic", "script.py.mako")
        )
        
        # 报告进度 - alembic/script.py.mako 生成完成
        current_file += 1
        report_progress("生成 alembic/script.py.mako 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 报告进度 - alembic/env.py 生成完成
        current_file += 1
        report_progress("生成 alembic/env.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 报告进度 - migrations/README.md 生成完成
        current_file += 1
        report_progress("生成 migrations/README.md 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成alembic.ini
        self._render_template(
            "fastapi/alembic.ini.j2",
            os.path.join(self.full_path, "alembic.ini"),
            project_name=self.project_name,
            db_type=self._get_db_type()
        )
        
        # 报告进度 - alembic.ini 生成完成
        current_file += 1
        report_progress("生成 alembic.ini 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成migrations/env.py
        self._render_template(
            "fastapi/migrations_env.py.j2",
            os.path.join(self.full_path, "migrations", "env.py"),
            project_name=self.project_name
        )
        
        # 报告进度 - migrations/env.py 生成完成
        current_file += 1
        report_progress("生成 migrations/env.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成scripts/db_init.py
        # 映射数据库类型到正确的模板文件名
        script_template_map = {
            'sqlite': 'sqlalchemy',
            'mysql': 'mysql',
            'postgresql': 'sqlalchemy',
            'mongodb': 'mongodb'
        }
        script_template = script_template_map.get(self.database, 'sqlalchemy')
        self._render_template(
            f"fastapi/scripts_db_init_{script_template}.py.j2",
            os.path.join(self.full_path, "scripts", "db_init.py"),
            project_name=self.project_name
        )
        
        # 报告进度 - scripts/db_init.py 生成完成
        current_file += 1
        report_progress("生成 scripts/db_init.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成scripts/reset_db.py
        self._render_template(
            "fastapi/scripts_reset_db.py.j2",
            os.path.join(self.full_path, "scripts", "reset_db.py"),
            project_name=self.project_name,
            db_type=self.database,
            include_auth=False
        )
        
        # 报告进度 - scripts/reset_db.py 生成完成
        current_file += 1
        report_progress("生成 scripts/reset_db.py 完成", sub_step=current_file, total_sub_steps=total_files)
            
        # 报告进度 - 所有数据库配置生成完成
        report_progress(f"{self._get_database_name()}数据库配置生成完成", sub_step=total_files, total_sub_steps=total_files)
    
    def _generate_redis_config(self, report_progress=None):
        """生成Redis配置
        
        Args:
            report_progress: 报告进度的函数
        """
        
        # 如果没有提供report_progress函数，则使用self.progress_callback
        if report_progress is None:
            # 创建一个不使用关键字参数的lambda函数
            report_progress = lambda msg, sub_step=None, total_sub_steps=None: self.progress_callback(
                msg, sub_step=sub_step, total_sub_steps=total_sub_steps
            )
        
        # 定义总共需要生成的文件数量
        total_files = 1
        current_file = 0
        
        # 报告进度 - 开始生成Redis配置
        report_progress("开始生成Redis缓存配置...", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成app/utils/redis.py
        self._render_template(
            "fastapi/utils_redis.py.j2",
            os.path.join(self.full_path, "app", "utils", "redis.py")
        )
        
        # 报告进度 - Redis配置生成完成
        current_file += 1
        report_progress("Redis缓存配置生成完成", sub_step=current_file, total_sub_steps=total_files)
    
    def _generate_docker_config(self, report_progress=None):
        """生成Docker配置
        
        Args:
            report_progress: 报告进度的函数
        """
        logger.info("生成Docker配置")
        
        # 如果没有提供report_progress函数，则使用self.progress_callback
        if report_progress is None:
            # 创建一个不使用关键字参数的lambda函数
            report_progress = lambda msg, sub_step=None, total_sub_steps=None: self.progress_callback(
                msg, sub_step=sub_step, total_sub_steps=total_sub_steps
            )
        
        # 定义总共需要生成的文件数量
        total_files = 3
        current_file = 0
        
        # 报告进度 - 开始生成Docker配置
        report_progress("开始生成Docker配置...", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成Dockerfile
        self._render_template(
            "fastapi/dockerfile.j2",
            os.path.join(self.full_path, "Dockerfile"),
            project_name=self.project_name,
            db_type=self._get_db_type()
        )
        
        # 报告进度 - Dockerfile 生成完成
        current_file += 1
        report_progress("生成 Dockerfile 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成docker-compose.yml
        self._render_template(
            "fastapi/docker-compose.yml.j2",
            os.path.join(self.full_path, "docker-compose.yml"),
            project_name=self.project_name,
            database=self.database,
            use_redis=self.use_redis,
            db_type=self._get_db_type()
        )
        
        # 报告进度 - docker-compose.yml 生成完成
        current_file += 1
        report_progress("生成 docker-compose.yml 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成.dockerignore
        self._render_template(
            "fastapi/dockerignore.j2",
            os.path.join(self.full_path, ".dockerignore")
        )
        
        # 报告进度 - .dockerignore 生成完成
        current_file += 1
        report_progress("生成 .dockerignore 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 报告进度 - Docker配置生成完成
        report_progress("Docker配置生成完成", sub_step=total_files, total_sub_steps=total_files)
    
    def _generate_tests(self, report_progress=None):
        """生成测试框架
        
        Args:
            report_progress: 报告进度的函数
        """
        logger.info("生成测试框架")
        
        # 如果没有提供report_progress函数，则使用self.progress_callback
        if report_progress is None:
            # 创建一个不使用关键字参数的lambda函数
            report_progress = lambda msg, sub_step=None, total_sub_steps=None: self.progress_callback(
                msg, sub_step=sub_step, total_sub_steps=total_sub_steps
            )
        
        # 定义总共需要生成的文件数量
        total_files = 9  # 包括app/db/__init__.py, app/db/session.py, app/db/base.py, alembic/env.py, alembic/script.py.mako, migrations/README.md, alembic.ini, migrations/env.py, scripts/db_init.py, scripts/reset_db.py
        current_file = 0
        
        # 报告进度 - 开始生成测试框架
        report_progress("开始生成测试框架...", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成tests/__init__.py
        self._render_template(
            "fastapi/tests_init.py.j2",
            os.path.join(self.full_path, "tests", "__init__.py")
        )
        
        # 报告进度 - tests/__init__.py 生成完成
        current_file += 1
        report_progress("生成 tests/__init__.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成tests/conftest.py
        self._render_template(
            "fastapi/tests_conftest.py.j2",
            os.path.join(self.full_path, "tests", "conftest.py"),
            project_name=self.project_name
        )
        
        # 报告进度 - tests/conftest.py 生成完成
        current_file += 1
        report_progress("生成 tests/conftest.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成tests/test_api.py
        self._render_template(
            "fastapi/tests_test_api.py.j2",
            os.path.join(self.full_path, "tests", "test_api.py"),
            project_name=self.project_name
        )
        
        # 报告进度 - tests/test_api.py 生成完成
        current_file += 1
        report_progress("生成 tests/test_api.py 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成pytest.ini
        self._render_template(
            "fastapi/pytest.ini.j2",
            os.path.join(self.full_path, "pytest.ini"),
            project_name=self.project_name
        )
        
        # 报告进度 - pytest.ini 生成完成
        current_file += 1
        report_progress("生成 pytest.ini 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 报告进度 - 测试框架生成完成
        report_progress("测试框架生成完成", sub_step=total_files, total_sub_steps=total_files)
    
    def _generate_api_docs(self, report_progress=None):
        """生成API文档
        
        Args:
            report_progress: 报告进度的函数
        """
        logger.info("生成API文档")
        
        # 如果没有提供report_progress函数，则使用self.progress_callback
        if report_progress is None:
            # 创建一个不使用关键字参数的lambda函数
            report_progress = lambda msg, sub_step=None, total_sub_steps=None: self.progress_callback(
                msg, sub_step=sub_step, total_sub_steps=total_sub_steps
            )
        
        # 定义总共需要生成的文件数量
        total_files = 3
        current_file = 0
        
        # 报告进度 - 开始生成API文档
        report_progress("开始生成API文档...", sub_step=current_file, total_sub_steps=total_files)
        
        # FastAPI自带Swagger和ReDoc，只需生成额外的文档
        
        # 生成docs/api.md
        self._render_template(
            "fastapi/docs_api.md.j2",
            os.path.join(self.full_path, "docs", "api.md"),
            project_name=self.project_name
        )
        
        # 报告进度 - docs/api.md 生成完成
        current_file += 1
        report_progress("生成 docs/api.md 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 生成docs/index.md
        self._render_template(
            "fastapi/docs_index.md.j2",
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
            "fastapi/mkdocs.yml.j2",
            os.path.join(self.full_path, "mkdocs.yml"),
            project_name=self.project_name
        )
        
        # 报告进度 - mkdocs.yml 生成完成
        current_file += 1
        report_progress("生成 mkdocs.yml 完成", sub_step=current_file, total_sub_steps=total_files)
        
        # 报告进度 - API文档生成完成
        report_progress("API文档生成完成", sub_step=total_files, total_sub_steps=total_files)
    
    # 认证系统已移除
    # def _generate_auth_system(self, report_progress=None):
    #     pass