# Web Generator 打包 Makefile
# 支持macOS和Windows平台的自动化打包

.PHONY: help install clean build build-macos build-windows package-macos package-windows all

# 默认目标
help:
	@echo "Web Generator 打包工具"
	@echo "可用命令:"
	@echo "  install        - 安装打包依赖"
	@echo "  clean          - 清理构建文件"
	@echo "  build          - 构建可执行文件"
	@echo "  build-macos    - 构建macOS通用版本（Intel + Apple芯片）"
	@echo "  build-windows  - 构建Windows版本"
	@echo "  package-macos  - 创建macOS DMG安装包"
	@echo "  package-windows- 创建Windows MSI安装包"
	@echo "  all            - 完整打包流程"
	@echo "  test-app       - 测试应用程序"

# 安装依赖
install:
	@echo "安装打包依赖..."
	pip install cx_Freeze
	@if [ "$$(uname)" = "Darwin" ]; then \
		echo "安装macOS特定依赖..."; \
		pip install dmgbuild; \
		if command -v brew >/dev/null 2>&1; then \
			brew install create-dmg || echo "create-dmg安装失败，将使用dmgbuild"; \
		fi; \
	fi
	@if [ "$$(uname)" = "MINGW"* ] || [ "$$(uname)" = "CYGWIN"* ]; then \
		echo "安装Windows特定依赖..."; \
		pip install pyinstaller; \
	fi

# 清理构建文件
clean:
	@echo "清理构建文件..."
	rm -rf build/ dist/ *.egg-info/ __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# 构建可执行文件
build: clean
	@echo "构建可执行文件..."
	python setup.py build

# 构建macOS通用版本
build-macos: clean
	@echo "构建macOS通用版本（Intel + Apple芯片）..."
	@if [ "$$(uname)" = "Darwin" ]; then \
		ARCHFLAGS="-arch x86_64 -arch arm64" python setup.py build; \
	else \
		echo "错误: 只能在macOS系统上构建macOS版本"; \
		exit 1; \
	fi

# 构建Windows版本
build-windows: clean
	@echo "构建Windows版本..."
	python setup.py build

# 创建macOS DMG
package-macos: build-macos
	@echo "创建macOS DMG安装包..."
	@if [ "$$(uname)" = "Darwin" ]; then \
		mkdir -p dist; \
		python -c "import dmgbuild; print('dmgbuild可用')" 2>/dev/null && \
			python build_package.py || \
			echo "DMG创建失败，请检查dmgbuild安装"; \
	else \
		echo "错误: 只能在macOS系统上创建DMG文件"; \
		exit 1; \
	fi

# 创建Windows MSI
package-windows: build-windows
	@echo "创建Windows MSI安装包..."
	python setup.py bdist_msi

# 完整打包流程
all:
	@echo "开始完整打包流程..."
	python build_package.py

# 测试应用程序
test-app:
	@echo "测试应用程序..."
	python main.py

# 显示构建信息
info:
	@echo "系统信息:"
	@echo "  操作系统: $$(uname -s)"
	@echo "  架构: $$(uname -m)"
	@echo "  Python版本: $$(python --version)"
	@echo "  当前目录: $$(pwd)"
	@echo "构建目录状态:"
	@ls -la build/ 2>/dev/null || echo "  build/ 目录不存在"
	@ls -la dist/ 2>/dev/null || echo "  dist/ 目录不存在"

# 快速打包（根据当前系统）
quick:
	@echo "快速打包当前平台..."
	@if [ "$$(uname)" = "Darwin" ]; then \
		make package-macos; \
	elif [ "$$(uname)" = "Linux" ]; then \
		make build; \
	else \
		make package-windows; \
	fi