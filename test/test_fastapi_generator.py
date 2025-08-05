#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FastAPI模板测试脚本

用于测试FastAPI生成器的功能
"""

import os
import sys
import shutil
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generators.fastapi_generator import FastAPIGenerator

def test_fastapi_generator():
    """测试FastAPI生成器"""
    print("开始测试FastAPI生成器...")
    
    # 测试项目配置
    project_config = {
        'project_name': 'fastapi_test_project',
        'project_path': './test_projects',
        'framework': 'fastapi',
        'database': 'sqlite',
        'redis': False,
        'docker': True,
        'tests': True,
        'api_docs': True,
        'auth': False,  # 已移除认证功能
        'description': 'FastAPI测试项目'
    }
    
    # 输出目录
    output_dir = Path('./test_projects')
    project_path = output_dir / project_config['project_name']
    
    # 如果项目目录已存在，先删除
    if project_path.exists():
        print(f"删除已存在的项目目录: {project_path}")
        shutil.rmtree(project_path)
    
    # 创建输出目录
    output_dir.mkdir(exist_ok=True)
    
    try:
        # 创建生成器实例
        generator = FastAPIGenerator(project_config)
        
        # 生成项目
        print(f"正在生成FastAPI项目: {project_config['project_name']}")
        generator.generate()
        
        print(f"FastAPI项目生成成功: {project_path}")
        
        # 验证生成的文件
        if verify_generated_files(project_path):
            return True
        else:
            return False
            
    except Exception as e:
        print(f"生成FastAPI项目时出错: {e}")
        return False

def verify_generated_files(project_path):
    """验证生成的文件结构"""
    print("\n验证生成的文件结构...")
    
    # 期望的文件列表
    expected_files = [
        'app/__init__.py',
        'app/main.py',
        'app/api/__init__.py',
        'app/api/v1/__init__.py',
        'app/api/v1/api.py',
        'app/api/deps.py',
        'app/api/endpoints.py',
        'app/models/__init__.py',
        'app/models/base.py',
        'app/schemas/__init__.py',
        'app/schemas/base.py',
        'app/crud/__init__.py',
        'app/crud/base.py',
        'app/db/__init__.py',
        'app/db/session.py',
        'config/__init__.py',
        'config/settings.py',
        'tests/__init__.py',
        'tests/conftest.py',
        'tests/test_api.py',
        'requirements.txt',
        'run.py',
        '.env',
        '.gitignore',
        'README.md',
        'Dockerfile',
        'docker-compose.yml'
    ]
    
    # 不应该存在的认证相关文件
    auth_files = [
        'app/auth/',
        'app/api/endpoints/auth.py',
        'app/models/user.py',
        'app/schemas/user.py',
        'app/crud/user.py'
    ]
    
    existing_files = 0
    missing_files = 0
    auth_files_found = 0
    
    # 检查期望的文件
    for file_path in expected_files:
        full_path = project_path / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
            existing_files += 1
        else:
            print(f"✗ {file_path} (缺失)")
            missing_files += 1
    
    # 检查不应该存在的认证文件
    for auth_file in auth_files:
        full_path = project_path / auth_file
        if full_path.exists():
            print(f"✗ {auth_file} (不应该存在的认证文件)")
            auth_files_found += 1
    
    print(f"\n文件验证结果:")
    print(f"- 存在的文件: {existing_files}/{len(expected_files)}")
    print(f"- 缺失的文件: {missing_files}")
    print(f"- 意外的认证文件: {auth_files_found}")
    
    return missing_files == 0 and auth_files_found == 0

if __name__ == '__main__':
    success = test_fastapi_generator()
    if success:
        print("\n✓ FastAPI生成器测试通过")
        sys.exit(0)
    else:
        print("\n✗ FastAPI生成器测试失败")
        sys.exit(1)