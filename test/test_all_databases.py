#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全数据库测试脚本
测试Flask和FastAPI生成器对MySQL、PostgreSQL、SQLite的支持
"""

import os
import sys
import shutil
import subprocess
from generators.flask_generator import FlaskGenerator
from generators.fastapi_generator import FastAPIGenerator

def test_database_config(framework, database, redis=False):
    """
    测试特定框架和数据库配置
    
    Args:
        framework: 'flask' 或 'fastapi'
        database: 'mysql', 'postgresql', 或 'sqlite'
        redis: 是否启用Redis
    """
    project_name = f"{framework}_{database}_test"
    project_path = f"./test_projects/{project_name}"
    
    print(f"\n{'='*60}")
    print(f"测试配置: {framework.upper()} + {database.upper()} + Redis({redis})")
    print(f"{'='*60}")
    
    # 删除已存在的项目目录
    if os.path.exists(project_path):
        print(f"删除已存在的项目目录: {project_path}")
        shutil.rmtree(project_path)
    
    # 项目配置
    project_config = {
        'project_name': project_name,
        'project_path': './test_projects',
        'framework': framework,
        'database': database,
        'redis': redis,
        'docker': True,
        'tests': True,
        'api_docs': True,
        'auth': False
    }
    
    try:
        # 选择生成器
        if framework == 'flask':
            generator = FlaskGenerator(project_config)
        else:
            generator = FastAPIGenerator(project_config)
        
        # 生成项目
        print(f"正在生成 {framework.upper()} 项目...")
        generator.generate()
        print(f"✅ {framework.upper()} 项目生成成功")
        
        # 验证关键文件
        key_files = [
            f"{project_path}/.env",
            f"{project_path}/requirements.txt",
            f"{project_path}/run.py",
            f"{project_path}/config/settings.py"
        ]
        
        missing_files = []
        for file_path in key_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ 缺失关键文件: {missing_files}")
            return False
        
        # 检查.env文件中的数据库配置
        with open(f"{project_path}/.env", 'r', encoding='utf-8') as f:
            env_content = f.read()
        
        print(f"检查 .env 文件中的数据库配置...")
        if database == 'sqlite':
            if framework == 'fastapi':
                expected_url = "sqlite+aiosqlite://"
            else:
                expected_url = "sqlite://"
        elif database == 'mysql':
            if framework == 'fastapi':
                expected_url = "mysql+aiomysql://"
            else:
                expected_url = "mysql+pymysql://"
        else:  # postgresql
            if framework == 'fastapi':
                expected_url = "postgresql+asyncpg://"
            else:
                expected_url = "postgresql://"
        
        if expected_url in env_content:
            print(f"✅ 数据库URL格式正确: {expected_url}")
        else:
            print(f"❌ 数据库URL格式错误，期望包含: {expected_url}")
            print(f"实际内容:\n{env_content}")
            return False
        
        # 检查requirements.txt中的依赖
        with open(f"{project_path}/requirements.txt", 'r', encoding='utf-8') as f:
            requirements_content = f.read()
        
        print(f"检查 requirements.txt 中的数据库驱动...")
        if database == 'sqlite':
            if framework == 'fastapi' and 'aiosqlite' not in requirements_content:
                print(f"❌ FastAPI SQLite项目缺少aiosqlite依赖")
                return False
            elif framework == 'fastapi':
                print(f"✅ FastAPI SQLite项目包含aiosqlite依赖")
        elif database == 'mysql':
            if framework == 'fastapi' and 'aiomysql' not in requirements_content:
                print(f"❌ FastAPI MySQL项目缺少aiomysql依赖")
                return False
            elif framework == 'flask' and 'pymysql' not in requirements_content:
                print(f"❌ Flask MySQL项目缺少pymysql依赖")
                return False
            else:
                print(f"✅ MySQL项目包含正确的数据库驱动")
        else:  # postgresql
            if framework == 'fastapi' and 'asyncpg' not in requirements_content:
                print(f"❌ FastAPI PostgreSQL项目缺少asyncpg依赖")
                return False
            elif framework == 'flask' and 'psycopg2-binary' not in requirements_content:
                print(f"❌ Flask PostgreSQL项目缺少psycopg2-binary依赖")
                return False
            else:
                print(f"✅ PostgreSQL项目包含正确的数据库驱动")
        
        print(f"✅ {framework.upper()} + {database.upper()} 配置测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """
    主测试函数
    """
    print("开始全数据库配置测试...")
    
    # 测试配置列表
    test_configs = [
        # Flask测试
        ('flask', 'mysql', False),
        ('flask', 'postgresql', False),
        ('flask', 'sqlite', False),
        ('flask', 'sqlite', True),  # 带Redis的SQLite测试
        
        # FastAPI测试
        ('fastapi', 'mysql', False),
        ('fastapi', 'postgresql', False),
        ('fastapi', 'sqlite', False),
        ('fastapi', 'sqlite', True),  # 带Redis的SQLite测试
    ]
    
    results = []
    
    for framework, database, redis in test_configs:
        success = test_database_config(framework, database, redis)
        results.append((framework, database, redis, success))
    
    # 输出测试结果摘要
    print(f"\n{'='*80}")
    print("测试结果摘要")
    print(f"{'='*80}")
    
    passed = 0
    failed = 0
    
    for framework, database, redis, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        redis_str = "+Redis" if redis else ""
        print(f"{framework.upper():8} + {database.upper():10} {redis_str:6} : {status}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n总计: {passed + failed} 个测试")
    print(f"通过: {passed} 个")
    print(f"失败: {failed} 个")
    
    if failed == 0:
        print("\n🎉 所有测试都通过了！")
        return True
    else:
        print(f"\n⚠️  有 {failed} 个测试失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)