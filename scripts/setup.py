#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Web框架生成器打包配置
支持生成macOS dmg和Windows exe文件
"""

import sys
from cx_Freeze import setup, Executable
import os

# 应用信息
APP_NAME = "Web Generator"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Python Web框架生成器 - 快速生成Flask和FastAPI项目"
APP_AUTHOR = "Web Generator Team"

# 包含的文件和目录
include_files = [
    ("../generators/", "generators/"),
    ("../templates/", "templates/"),
    ("../utils/", "utils/"),
    ("../screenshots/", "screenshots/"),
    ("../README.md", "README.md"),
    ("../requirements.txt", "requirements.txt")
]

# 需要包含的包
packages = [
    "PyQt5",
    "jinja2",
    "os",
    "sys",
    "json",
    "shutil",
    "logging",
    "datetime",
    "pathlib"
]

# 排除的模块
excludes = [
    "tkinter",
    "unittest",
    "email",
    "http",
    "urllib",
    "xml",
    "pydoc",
    "doctest",
    "argparse"
]

# 构建选项
build_exe_options = {
    "packages": packages,
    "excludes": excludes,
    "include_files": include_files,
    "optimize": 2
}

# Windows特定选项
if sys.platform == "win32":
    build_exe_options["include_msvcrt"] = True

# macOS特定选项
bdist_mac_options = {
    "bundle_name": APP_NAME,
    "iconfile": "../assets/icon.icns" if os.path.exists("../assets/icon.icns") else None,
    "custom_info_plist": {
        "CFBundleIdentifier": "com.webgenerator.app",
        "CFBundleShortVersionString": APP_VERSION,
        "CFBundleVersion": APP_VERSION,
        "LSMinimumSystemVersion": "10.14",
        "NSHighResolutionCapable": True,
        "LSArchitecturePriority": ["arm64", "x86_64"]
    }
}

# Windows特定选项
bdist_msi_options = {
    "upgrade_code": "{12345678-1234-1234-1234-123456789012}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\Web Generator"
}

# 可执行文件配置
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Windows GUI应用

executables = [
    Executable(
        "../main.py",
        base=base,
        target_name="WebGenerator" + (".exe" if sys.platform == "win32" else ""),
        icon="../assets/icon.ico" if os.path.exists("../assets/icon.ico") and sys.platform == "win32" else None,
        shortcut_name=APP_NAME,
        shortcut_dir="DesktopFolder"
    )
]

setup(
    name=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    author=APP_AUTHOR,
    options={
        "build_exe": build_exe_options,
        "bdist_mac": bdist_mac_options,
        "bdist_msi": bdist_msi_options
    },
    executables=executables
)