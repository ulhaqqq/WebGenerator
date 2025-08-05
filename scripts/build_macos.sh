#!/bin/bash
# macOS 打包脚本
# 用于在 macOS 系统上构建 Web Generator DMG 安装包
# 支持 Intel 和 Apple Silicon 芯片

set -e  # 遇到错误立即退出

echo "================================================"
echo "Python Web框架生成器 - macOS 打包脚本"
echo "================================================"
echo

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印彩色消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否在 macOS 上运行
if [[ "$(uname)" != "Darwin" ]]; then
    print_error "此脚本只能在 macOS 系统上运行"
    exit 1
fi

# 显示系统信息
print_info "系统信息:"
echo "  操作系统: $(uname -s)"
echo "  架构: $(uname -m)"
echo "  macOS 版本: $(sw_vers -productVersion)"
echo

# 检查 Python
if ! command -v python3 &> /dev/null; then
    print_error "未找到 Python 3，请先安装 Python 3.7 或更高版本"
    exit 1
fi

print_info "当前 Python 版本: $(python3 --version)"
echo

# 检查当前目录
if [[ ! -f "main.py" ]]; then
    print_error "请在项目根目录运行此脚本"
    exit 1
fi

# 检查 Homebrew（可选）
if command -v brew &> /dev/null; then
    print_info "检测到 Homebrew: $(brew --version | head -n1)"
else
    print_warning "未检测到 Homebrew，某些功能可能不可用"
fi
echo

# 创建构建虚拟环境
BUILD_VENV="venv_build"
if [[ ! -d "$BUILD_VENV" ]]; then
    print_info "创建构建虚拟环境..."
    python3 -m venv "$BUILD_VENV"
fi

# 激活虚拟环境
print_info "激活虚拟环境..."
source "$BUILD_VENV/bin/activate"

# 升级 pip
print_info "升级 pip..."
pip install --upgrade pip

# 安装项目依赖
print_info "安装项目依赖..."
pip install -r requirements.txt

# 安装打包依赖
print_info "安装打包依赖..."
pip install cx_Freeze

# 安装 dmgbuild
print_info "安装 dmgbuild..."
pip install dmgbuild

# 尝试安装 create-dmg（可选）
if command -v brew &> /dev/null; then
    print_info "尝试安装 create-dmg..."
    brew install create-dmg 2>/dev/null || print_warning "create-dmg 安装失败，将使用 dmgbuild"
fi

# 清理之前的构建
print_info "清理之前的构建文件..."
rm -rf build/ dist/ *.egg-info/
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# 检测当前架构
ARCH=$(uname -m)
print_info "当前架构: $ARCH"

# 构建通用二进制文件
print_info "构建通用二进制文件（Intel + Apple Silicon）..."
export ARCHFLAGS="-arch x86_64 -arch arm64"

# 尝试通用构建
if python setup.py build; then
    print_success "通用构建成功"
else
    print_warning "通用构建失败，尝试当前架构构建..."
    unset ARCHFLAGS
    if python setup.py build; then
        print_success "当前架构构建成功"
    else
        print_error "构建失败"
        exit 1
    fi
fi

# 查找构建目录
BUILD_DIR=$(find build -name "exe.*" -type d | head -n1)
if [[ -z "$BUILD_DIR" ]]; then
    print_error "未找到构建目录"
    exit 1
fi

print_info "构建目录: $BUILD_DIR"

# 创建 dist 目录
mkdir -p dist

# 创建 DMG
print_info "创建 DMG 安装包..."

# 创建临时 DMG 配置
DMG_CONFIG="dmg_settings.py"
cat > "$DMG_CONFIG" << EOF
# -*- coding: utf-8 -*-
# DMG 配置文件

import os

# 应用程序信息
application = os.path.join('$BUILD_DIR', 'WebGenerator')

# DMG 设置
format = 'UDBZ'  # 压缩格式
size = None      # 自动计算大小

# 文件和符号链接
files = [ application ]
symlinks = { 'Applications': '/Applications' }

# 图标位置
icon_locations = {
    'WebGenerator': (140, 120),
    'Applications': (500, 120)
}

# 窗口设置
window_rect = ((100, 100), (640, 280))
icon_size = 128
text_size = 16

# 背景
background = None  # 可以设置背景图片

# 其他设置
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
hide_extension = False
EOF

# 生成 DMG 文件名
DMG_NAME="WebGenerator-macOS-$(uname -m).dmg"
DMG_PATH="dist/$DMG_NAME"

# 创建 DMG
if dmgbuild -s "$DMG_CONFIG" "Web Generator" "$DMG_PATH"; then
    print_success "DMG 创建成功: $DMG_PATH"
else
    print_error "DMG 创建失败"
    
    # 尝试使用 create-dmg 作为备选
    if command -v create-dmg &> /dev/null; then
        print_info "尝试使用 create-dmg..."
        
        # 创建临时目录
        TEMP_DIR="temp_dmg"
        mkdir -p "$TEMP_DIR"
        
        # 复制应用程序
        cp -R "$BUILD_DIR" "$TEMP_DIR/WebGenerator"
        
        # 创建 Applications 链接
        ln -s /Applications "$TEMP_DIR/Applications"
        
        # 使用 create-dmg
        if create-dmg \
            --volname "Web Generator" \
            --window-pos 200 120 \
            --window-size 640 280 \
            --icon-size 128 \
            --icon "WebGenerator" 140 120 \
            --icon "Applications" 500 120 \
            --hide-extension "WebGenerator" \
            "$DMG_PATH" \
            "$TEMP_DIR"; then
            print_success "create-dmg 创建成功: $DMG_PATH"
        else
            print_error "create-dmg 也失败了"
        fi
        
        # 清理临时目录
        rm -rf "$TEMP_DIR"
    fi
fi

# 清理临时文件
rm -f "$DMG_CONFIG"

# 显示结果
echo
print_success "构建完成！"
echo "================================================"
echo

if [[ -d "dist" ]]; then
    print_info "输出文件:"
    ls -la dist/
    echo
    print_info "文件位置: $(pwd)/dist/"
fi

if [[ -d "$BUILD_DIR" ]]; then
    echo
    print_info "可执行文件位置: $(pwd)/$BUILD_DIR/WebGenerator"
fi

# 验证 DMG
if [[ -f "$DMG_PATH" ]]; then
    echo
    print_info "DMG 文件信息:"
    ls -lh "$DMG_PATH"
    
    # 验证 DMG 完整性
    if hdiutil verify "$DMG_PATH" &> /dev/null; then
        print_success "DMG 文件验证通过"
    else
        print_warning "DMG 文件验证失败"
    fi
fi

# 询问是否测试应用
echo
read -p "是否测试构建的应用程序？ (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "启动应用程序测试..."
    if [[ -f "$BUILD_DIR/WebGenerator" ]]; then
        open "$BUILD_DIR/WebGenerator" || "$BUILD_DIR/WebGenerator" &
    else
        print_error "未找到可执行文件"
    fi
fi

# 询问是否打开输出目录
echo
read -p "是否打开输出目录？ (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open dist/
fi

# 询问是否清理构建环境
echo
read -p "是否删除构建虚拟环境？ (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    deactivate 2>/dev/null || true
    rm -rf "$BUILD_VENV"
    print_success "构建虚拟环境已删除"
fi

echo
print_success "打包完成！"