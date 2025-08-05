#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化打包脚本
支持构建macOS dmg和Windows exe文件
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def run_command(cmd, cwd=None):
    """执行命令并返回结果"""
    print(f"执行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"命令执行失败: {result.stderr}")
            return False
        print(f"命令执行成功: {result.stdout}")
        return True
    except Exception as e:
        print(f"命令执行异常: {e}")
        return False

def install_dependencies():
    """安装打包依赖"""
    print("正在安装打包依赖...")
    
    # 安装cx_Freeze
    if not run_command("pip install cx_Freeze"):
        return False
    
    # macOS特定依赖
    if platform.system() == "Darwin":
        # 安装dmgbuild用于创建dmg文件
        if not run_command("pip install dmgbuild"):
            return False
        # 安装create-dmg（可选，用于更好的dmg创建）
        run_command("brew install create-dmg")
    
    # Windows特定依赖
    elif platform.system() == "Windows":
        # 安装pyinstaller作为备选方案
        run_command("pip install pyinstaller")
    
    return True

def clean_build_dirs():
    """清理构建目录"""
    print("清理构建目录...")
    dirs_to_clean = ["build", "dist", "__pycache__"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除目录: {dir_name}")

def build_executable():
    """构建可执行文件"""
    print("正在构建可执行文件...")
    
    # 使用cx_Freeze构建
    if not run_command("python scripts/setup.py build"):
        print("cx_Freeze构建失败，尝试使用PyInstaller...")
        
        # 备选方案：使用PyInstaller
        pyinstaller_cmd = (
            "pyinstaller --onedir --windowed "
            "--add-data 'generators:generators' "
            "--add-data 'templates:templates' "
            "--add-data 'utils:utils' "
            "--add-data 'screenshots:screenshots' "
            "--name 'WebGenerator' "
            "main.py"
        )
        
        if not run_command(pyinstaller_cmd):
            return False
    
    return True

def create_macos_dmg():
    """创建macOS DMG文件"""
    if platform.system() != "Darwin":
        print("跳过DMG创建（非macOS系统）")
        return True
    
    print("正在创建macOS DMG文件...")
    
    # 检查构建目录
    build_dir = None
    
    # 首先检查PyInstaller生成的目录
    if os.path.exists("dist/WebGenerator.app"):
        build_dir = "dist/WebGenerator.app"
    elif os.path.exists("dist/WebGenerator"):
        build_dir = "dist/WebGenerator"
    # 然后检查cx_Freeze生成的目录
    elif os.path.exists("build"):
        for item in os.listdir("build"):
            if item.startswith("exe."):
                build_dir = os.path.join("build", item)
                break
    
    if not build_dir or not os.path.exists(build_dir):
        print("未找到构建目录")
        return False
    
    # 创建DMG配置文件
    dmg_config = '''
# DMG配置文件
files = [ '{build_dir}' ]
symlinks = {{ 'Applications': '/Applications' }}
badge_icon = None
icon_locations = {{
    'WebGenerator.app': (140, 120),
    'Applications': (500, 120)
}}
window_rect = ((100, 100), (640, 280))
icon_size = 128
text_size = 16
'''.format(build_dir=build_dir)
    
    with open('dmg_settings.py', 'w') as f:
        f.write(dmg_config)
    
    # 创建DMG
    dmg_cmd = f"dmgbuild -s dmg_settings.py 'Web Generator' dist/WebGenerator-macOS.dmg"
    
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    success = run_command(dmg_cmd)
    
    # 清理临时文件
    if os.path.exists('dmg_settings.py'):
        os.remove('dmg_settings.py')
    
    return success

def create_windows_installer():
    """创建Windows安装程序"""
    if platform.system() != "Windows":
        print("跳过Windows安装程序创建（非Windows系统）")
        return True
    
    print("正在创建Windows安装程序...")
    
    # 使用cx_Freeze的bdist_msi
    return run_command("python scripts/setup.py bdist_msi")

def create_universal_macos_build():
    """创建支持Intel和Apple芯片的通用macOS构建"""
    if platform.system() != "Darwin":
        return True
    
    print("正在创建通用macOS构建...")
    
    # 设置环境变量以支持通用构建
    env = os.environ.copy()
    env['ARCHFLAGS'] = '-arch x86_64 -arch arm64'
    
    # 重新构建
    cmd = "python scripts/setup.py build"
    try:
        result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
        if result.returncode == 0:
            print("通用构建成功")
            return True
        else:
            print(f"通用构建失败，使用标准构建: {result.stderr}")
            return build_executable()
    except Exception as e:
        print(f"通用构建异常，使用标准构建: {e}")
        return build_executable()

def main():
    """主函数"""
    print("=" * 50)
    print("Python Web框架生成器 - 自动化打包脚本")
    print(f"当前平台: {platform.system()} {platform.machine()}")
    print("=" * 50)
    
    # 1. 安装依赖
    if not install_dependencies():
        print("依赖安装失败")
        return False
    
    # 2. 清理构建目录
    clean_build_dirs()
    
    # 3. 构建可执行文件
    if platform.system() == "Darwin":
        success = create_universal_macos_build()
    else:
        success = build_executable()
    
    if not success:
        print("可执行文件构建失败")
        return False
    
    # 4. 创建平台特定的安装包
    if platform.system() == "Darwin":
        if not create_macos_dmg():
            print("DMG创建失败")
            return False
        print("✅ macOS DMG文件创建成功")
    
    elif platform.system() == "Windows":
        if not create_windows_installer():
            print("Windows安装程序创建失败")
            return False
        print("✅ Windows安装程序创建成功")
    
    print("\n=" * 50)
    print("打包完成！")
    print("输出文件位置: ./dist/")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)