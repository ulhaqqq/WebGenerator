#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flask模板测试脚本

用于测试Flask生成器的功能
"""

import os
import sys
import shutil
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generators.flask_generator import FlaskGenerator

def test_flask_generator():
    """测试Flask生成器"""
    print("开始测试Flask生成器...")
    
    # 测试项目配置
    project_config = {
        'project_name': 'flask_test_project',
        'project_path': './test_projects',
        'framework': 'flask',
        'database': 'sqlite',
        'redis': False,
        'docker': True,
        'tests': True,
        'api_docs': True,
        'auth': False,  # 已移除认证功能
        'description': 'Flask测试项目'
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
        generator = FlaskGenerator(project_config)
        
        # 生成项目
        print(f"正在生成Flask项目: {project_config['project_name']}")
        generator.generate()
        
        print(f"Flask项目生成成功: {project_path}")
        
        # 验证生成的文件
        verify_generated_files(project_path)
        
        return True
        
    except Exception as e:
        print(f"生成Flask项目时出错: {e}")
        return False

def verify_generated_files(project_path):
    """验证生成的文件"""
    print("\n验证生成的文件结构...")
    
    # 必须存在的文件和目录
    required_items = [
        'app/__init__.py',
        'app/api/__init__.py',
        'app/api/routes.py',
        'app/models/__init__.py',
        'app/models/base.py',
        'app/models/database.py',
        'app/utils/__init__.py',
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
    
    missing_files = []
    existing_files = []
    
    for item in required_items:
        file_path = project_path / item
        if file_path.exists():
            existing_files.append(item)
            print(f"✓ {item}")
        else:
            missing_files.append(item)
            print(f"✗ {item} (缺失)")
    
    # 检查不应该存在的认证相关文件
    auth_files = [
        'app/auth',
        'app/models/user.py',
        'app/utils/auth.py'
    ]
    
    auth_files_found = []
    for item in auth_files:
        file_path = project_path / item
        if file_path.exists():
            auth_files_found.append(item)
            print(f"⚠ {item} (不应该存在的认证文件)")
    
    print(f"\n文件验证结果:")
    print(f"- 存在的文件: {len(existing_files)}/{len(required_items)}")
    print(f"- 缺失的文件: {len(missing_files)}")
    print(f"- 意外的认证文件: {len(auth_files_found)}")
    
    if missing_files:
        print(f"\n缺失的文件: {missing_files}")
    
    if auth_files_found:
        print(f"\n意外发现的认证文件: {auth_files_found}")
    
    return len(missing_files) == 0 and len(auth_files_found) == 0

if __name__ == '__main__':
    success = test_flask_generator()
    if success:
        print("\n✓ Flask生成器测试通过")
        sys.exit(0)
    else:
        print("\n✗ Flask生成器测试失败")
        sys.exit(1)