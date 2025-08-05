#!/usr/bin/env python3
"""
Windows构建脚本 - 在Windows环境中运行
使用PyInstaller构建Windows可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"运行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"错误: {result.stderr}")
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False

def main():
    """主构建函数"""
    print("开始构建Windows可执行文件...")
    
    # 检查是否在Windows环境
    if sys.platform != "win32":
        print("警告: 此脚本应在Windows环境中运行以构建Windows可执行文件")
        print("当前平台:", sys.platform)
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 安装依赖
    print("\n1. 安装构建依赖...")
    if not run_command("pip install pyinstaller"):
        print("安装PyInstaller失败")
        return False
    
    # 清理旧的构建文件
    print("\n2. 清理旧的构建文件...")
    for path in ["build", "dist", "*.spec"]:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
                print(f"删除目录: {path}")
            else:
                os.remove(path)
                print(f"删除文件: {path}")
    
    # 构建可执行文件
    print("\n3. 构建可执行文件...")
    build_cmd = (
        "pyinstaller "
        "--onefile "
        "--windowed "
        "--name=\"Web Generator\" "
        "--distpath=dist "
        "--workpath=build "
        "main.py"
    )
    
    if not run_command(build_cmd):
        print("构建失败")
        return False
    
    # 检查构建结果
    exe_path = project_root / "dist" / "Web Generator.exe"
    if exe_path.exists():
        print(f"\n✅ 构建成功!")
        print(f"可执行文件位置: {exe_path}")
        print(f"文件大小: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        # 创建安装包目录
        installer_dir = project_root / "installer"
        installer_dir.mkdir(exist_ok=True)
        
        # 复制可执行文件到安装包目录
        shutil.copy2(exe_path, installer_dir / "Web Generator.exe")
        
        print(f"\n📦 安装包准备完成:")
        print(f"安装包目录: {installer_dir}")
        print(f"\n使用说明:")
        print(f"1. 可以直接运行 'Web Generator.exe'")
        print(f"2. 或者使用NSIS等工具创建安装程序")
        
        return True
    else:
        print("\n❌ 构建失败: 找不到可执行文件")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Windows构建完成!")
    else:
        print("\n💥 构建失败")
        sys.exit(1)