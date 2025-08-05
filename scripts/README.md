# 构建脚本目录

本目录包含了Web Generator项目的所有构建和打包脚本。

## 📁 脚本说明

### 🚀 快速构建脚本

| 脚本名称 | 平台 | 描述 | 使用方法 |
|---------|------|------|----------|
| `build_macos.sh` | macOS/Linux | macOS自动化构建脚本 | `./build_macos.sh` |
| `build_windows.bat` | Windows | Windows批处理构建脚本 | `build_windows.bat` |
| `build_windows_simple.py` | Windows | Windows Python构建脚本 | `python build_windows_simple.py` |

### 🔧 高级构建工具

| 脚本名称 | 描述 | 使用方法 |
|---------|------|----------|
| `build_package.py` | 跨平台自动化构建脚本 | `python build_package.py` |
| `setup.py` | cx_Freeze配置文件 | `python setup.py build` |
| `Makefile` | Make构建配置 | `make help` |

## 🚀 快速开始

### macOS用户
```bash
# 方法1: 使用shell脚本（推荐）
chmod +x build_macos.sh
./build_macos.sh

# 方法2: 使用Makefile
make package-macos

# 方法3: 使用Python脚本
python build_package.py --platform macos
```

### Windows用户
```cmd
REM 方法1: 使用批处理脚本（推荐）
build_windows.bat

REM 方法2: 使用Python脚本
python build_windows_simple.py

REM 方法3: 使用高级脚本
python build_package.py --platform windows
```

### Linux用户
```bash
# 使用macOS脚本（兼容Linux）
./build_macos.sh

# 或使用Python脚本
python build_package.py --platform linux
```

## 📋 脚本详细说明

### build_macos.sh
- **功能**: 自动化macOS应用程序构建和DMG创建
- **输出**: `.app`文件和`.dmg`安装包
- **特性**: 支持Intel和Apple Silicon通用构建
- **依赖**: PyInstaller, dmgbuild

### build_windows.bat
- **功能**: Windows批处理自动化构建
- **输出**: `.exe`文件和可选的MSI安装包
- **特性**: 完整的环境检查和错误处理
- **依赖**: Python, PyInstaller

### build_windows_simple.py
- **功能**: 简化的Windows构建脚本
- **输出**: `.exe`文件
- **特性**: 纯Python实现，跨平台兼容
- **依赖**: PyInstaller

### build_package.py
- **功能**: 高级跨平台构建脚本
- **输出**: 根据平台生成相应的安装包
- **特性**: 支持多种构建工具，自动依赖管理
- **依赖**: cx_Freeze, PyInstaller, dmgbuild

### setup.py
- **功能**: cx_Freeze配置文件
- **输出**: 可执行文件和安装包
- **特性**: 详细的打包配置，支持多平台
- **依赖**: cx_Freeze

### Makefile
- **功能**: Make构建系统配置
- **输出**: 根据目标生成相应文件
- **特性**: 统一的构建接口，支持多种操作
- **依赖**: make, Python构建工具

## 🛠️ 环境要求

### 通用要求
- Python 3.8+
- 项目依赖已安装 (`pip install -r requirements.txt`)

### macOS特定
- Xcode Command Line Tools
- dmgbuild (`pip install dmgbuild`)

### Windows特定
- Visual Studio Build Tools (可选)
- NSIS (创建安装程序时需要)

## 📦 输出文件

构建完成后，所有输出文件将位于项目根目录的`dist/`文件夹中：

```
dist/
├── Web Generator.app/          # macOS应用程序包
├── Web Generator.dmg           # macOS DMG安装包
├── Web Generator.exe           # Windows可执行文件
└── Web Generator Setup.msi     # Windows MSI安装包（可选）
```

## 🐛 故障排除

### 常见问题

1. **权限错误 (macOS/Linux)**
   ```bash
   chmod +x build_macos.sh
   ```

2. **Python模块未找到**
   ```bash
   pip install -r ../requirements-build.txt
   ```

3. **构建失败**
   - 检查Python版本 (`python --version`)
   - 确认所有依赖已安装
   - 查看详细错误信息

4. **DMG创建失败 (macOS)**
   ```bash
   pip install dmgbuild
   # 或使用系统工具
   hdiutil create -volname "Web Generator" -srcfolder "dist/Web Generator.app" "dist/Web Generator.dmg"
   ```

### 调试模式

大多数脚本支持详细输出模式：

```bash
# 启用详细模式
export VERBOSE=1
./build_macos.sh

# 或直接使用PyInstaller
pyinstaller --debug=all main.py
```

## 📝 自定义配置

### 修改应用程序信息
编辑相应的脚本文件，修改以下变量：
- 应用程序名称
- 版本号
- 图标路径
- 输出目录

### 添加新的构建目标
1. 复制现有脚本
2. 修改平台特定的配置
3. 更新Makefile（如需要）

## 🔗 相关文档

- [DISTRIBUTION_GUIDE.md](../docs/DISTRIBUTION_GUIDE.md) - 分发指南
- [BUILD_README.md](../docs/BUILD_README.md) - 详细构建说明
- [PACKAGING.md](../docs/PACKAGING.md) - 打包技术文档

---

**注意**: 在使用这些脚本之前，请确保已阅读相关文档并满足环境要求。