#!/usr/bin/env python3
"""
Windows跨平台构建脚本 - 在macOS上构建Windows可执行文件
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

def clean_build_dirs():
    """清理构建目录"""
    print("清理构建目录...")
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除 {dir_name}")
    
    # 删除spec文件
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"已删除 {spec_file}")

def create_pyinstaller_spec():
    """创建PyInstaller spec文件用于Windows构建"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('generators', 'generators'),
        ('assets', 'assets'),
        ('utils', 'utils'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WebGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
'''
    
    with open('WebGenerator-Windows.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("已创建 WebGenerator-Windows.spec")

def build_windows_executable():
    """使用PyInstaller构建Windows可执行文件"""
    print("\n开始构建Windows可执行文件...")
    
    # 创建spec文件
    create_pyinstaller_spec()
    
    # 使用PyInstaller构建
    cmd = "pyinstaller --clean --noconfirm WebGenerator-Windows.spec"
    if not run_command(cmd):
        print("PyInstaller构建失败")
        return False
    
    print("Windows可执行文件构建成功")
    return True

def create_windows_zip():
    """创建Windows发布包的ZIP文件"""
    print("\n创建Windows发布包...")
    
    # 检查可执行文件（在macOS上构建时不会有.exe扩展名）
    exe_path = 'dist/WebGenerator.exe' if os.path.exists('dist/WebGenerator.exe') else 'dist/WebGenerator'
    if not os.path.exists(exe_path):
        print("错误: 找不到构建的可执行文件")
        return False
    
    # 创建发布目录
    release_dir = 'dist/WebGenerator-Windows'
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # 复制可执行文件并重命名为.exe
    target_exe = os.path.join(release_dir, 'WebGenerator.exe')
    shutil.copy2(exe_path, target_exe)
    print(f"已复制可执行文件: {exe_path} -> {target_exe}")
    
    # 复制必要文件
    files_to_copy = ['README.md', 'LICENSE']
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, release_dir)
    
    # 创建ZIP文件
    import zipfile
    zip_path = 'dist/WebGenerator-Windows.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'dist')
                zipf.write(file_path, arcname)
    
    print(f"Windows发布包已创建: {zip_path}")
    return True

def main():
    """主构建函数"""
    print("=" * 50)
    print("WebGenerator - Windows跨平台构建")
    print(f"当前平台: {sys.platform}")
    print("=" * 50)
    
    # 检查是否在项目根目录
    if not os.path.exists('main.py'):
        print("错误: 请在项目根目录运行此脚本")
        return False
    
    # 1. 清理构建目录
    clean_build_dirs()
    
    # 2. 构建Windows可执行文件
    if not build_windows_executable():
        print("Windows可执行文件构建失败")
        return False
    
    # 3. 创建发布包
    if not create_windows_zip():
        print("Windows发布包创建失败")
        return False
    
    print("\n=" * 50)
    print("🎉 Windows构建完成!")
    print("输出文件:")
    print("  - dist/WebGenerator.exe (可执行文件)")
    print("  - dist/WebGenerator-Windows.zip (发布包)")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💥 构建失败")
        sys.exit(1)