# Web Generator 打包指南

本文档详细说明如何将 Python Web框架生成器打包成不同平台的可执行文件和安装包。

## 支持的平台

- **macOS**: 支持 Intel (x86_64) 和 Apple Silicon (arm64) 芯片
- **Windows**: 支持 x64 架构
- **Linux**: 支持 x64 架构（可执行文件）

## 快速开始

### 自动化打包（推荐）

```bash
# 完整自动化打包流程
python scripts/build_package.py

# 或使用 Makefile
cd scripts && make all
```

### 手动打包步骤

#### 1. 安装依赖

```bash
# 安装打包工具
pip install cx_Freeze

# macOS 额外依赖
pip install dmgbuild
brew install create-dmg  # 可选，用于更好的 DMG 创建

# Windows 额外依赖
pip install pyinstaller  # 备选打包工具
```

#### 2. 清理环境

```bash
# 清理之前的构建文件
make clean
# 或手动删除
rm -rf build/ dist/ *.egg-info/
```

#### 3. 构建可执行文件

```bash
# 通用构建
python scripts/setup.py build

# macOS 通用构建（支持 Intel + Apple 芯片）
ARCHFLAGS="-arch x86_64 -arch arm64" python scripts/setup.py build
```

#### 4. 创建安装包

**macOS DMG:**
```bash
make package-macos
```

**Windows MSI:**
```bash
python scripts/setup.py bdist_msi
```

## 详细说明

### macOS 打包

#### 通用二进制文件

为了支持 Intel 和 Apple Silicon 芯片，我们使用通用二进制文件：

```bash
# 设置架构标志
export ARCHFLAGS="-arch x86_64 -arch arm64"

# 构建通用版本
python scripts/setup.py build
```

#### DMG 创建

DMG 文件包含以下特性：
- 拖拽安装界面
- 应用程序快捷方式
- 自定义背景和图标
- 自动挂载和弹出

#### 系统要求
- macOS 10.14 (Mojave) 或更高版本
- 支持 Retina 显示屏
- 支持深色模式

### Windows 打包

#### MSI 安装程序

MSI 安装程序包含：
- 标准 Windows 安装向导
- 程序文件夹创建
- 开始菜单快捷方式
- 卸载程序
- 注册表项管理

#### 系统要求
- Windows 10 或更高版本
- .NET Framework 4.7.2 或更高版本

### 构建选项说明

#### scripts/setup.py 配置

```python
# 包含的文件
include_files = [
    ("generators/", "generators/"),    # 代码生成器
    ("templates/", "templates/"),      # 项目模板
    ("utils/", "utils/"),              # 工具函数
    ("screenshots/", "screenshots/"),  # 截图文件
]

# 优化选项
build_exe_options = {
    "optimize": 2,                     # 字节码优化
    "include_msvcrt": True,            # Windows 运行时
}
```

#### 文件大小优化

- 排除不必要的模块
- 字节码优化
- 资源文件压缩
- 依赖项精简

## 使用 Makefile

### 可用命令

```bash
make help           # 显示帮助信息
make install        # 安装打包依赖
make clean          # 清理构建文件
make build          # 构建可执行文件
make build-macos    # 构建 macOS 通用版本
```

## 故障排除

### 常见问题及解决方案

#### 1. cx_Freeze 找不到文件错误

**问题**: `error: cannot find file/directory named ../generators`

**原因**: setup.py 文件在 scripts 目录中，相对路径配置不正确

**解决方案**: 
- 确保 setup.py 中的文件路径使用正确的相对路径
- 从项目根目录执行 `python scripts/setup.py build`

#### 2. DMG 创建失败

**问题**: `ImportError: cannot import name 'defines' from 'dmgbuild'`

**原因**: dmgbuild 配置文件格式不正确

**解决方案**: 
- 使用正确的 dmgbuild 配置格式（不使用 defines 对象）
- 确保配置文件中的变量名正确

#### 3. 图标文件缺失

**问题**: 打包时找不到 .ico 或 .icns 格式的图标

**解决方案**: 
```bash
# 从 PNG 创建所需格式的图标
cp assets/icon.png assets/icon.ico    # Windows
cp assets/icon.png assets/icon.icns   # macOS
```

#### 4. PyInstaller 作为备选方案

当 cx_Freeze 失败时，自动化脚本会使用 PyInstaller：

```bash
pyinstaller --onedir --windowed \
  --add-data 'generators:generators' \
  --add-data 'templates:templates' \
  --add-data 'utils:utils' \
  --add-data 'screenshots:screenshots' \
  --name 'WebGenerator' main.py
```

### 验证打包结果

#### macOS
```bash
# 检查生成的文件
ls -la dist/
# WebGenerator-macOS.dmg    # DMG 安装包
# WebGenerator.app/         # 应用程序包
# WebGenerator/             # 可执行文件目录

# 测试 DMG 文件
open dist/WebGenerator-macOS.dmg
```

#### Windows
```bash
# 检查生成的文件
dir dist\
# WebGenerator.msi          # MSI 安装包
# WebGenerator.exe          # 可执行文件
```

### 其他 Makefile 命令

```bash
make build-windows  # 构建 Windows 版本
make package-macos  # 创建 macOS DMG
make package-windows# 创建 Windows MSI
make all            # 完整打包流程
make quick          # 快速打包当前平台
make test-app       # 测试应用程序
make info           # 显示构建信息
```

### 平台检测

Makefile 会自动检测当前平台并执行相应的打包流程：

```bash
# 自动选择平台
make quick
```

#### 2. macOS 通用构建失败

**原因**: 某些依赖不支持通用二进制

**解决方案**: 分别构建 Intel 和 ARM 版本

```bash
# Intel 版本
arch -x86_64 python scripts/setup.py build

# ARM 版本
arch -arm64 python scripts/setup.py build
```

#### 3. Windows 权限问题

**解决方案**: 以管理员身份运行命令提示符

#### 4. 依赖缺失

**检查方法**:
```bash
# 检查依赖
pip list | grep -E "cx_Freeze|dmgbuild|pyinstaller"

# 重新安装
pip install --upgrade cx_Freeze dmgbuild
```

### 调试技巧

#### 1. 详细输出

```bash
# 启用详细模式
python scripts/setup.py build --verbose
```

#### 2. 测试构建

```bash
# 测试可执行文件
./build/exe.*/WebGenerator
```

#### 3. 检查依赖

```bash
# macOS
otool -L build/exe.*/WebGenerator

# Linux
ldd build/exe.*/WebGenerator
```

## 分发说明

### 文件命名规范

- macOS: `WebGenerator-v1.0.0-macOS-universal.dmg`
- Windows: `WebGenerator-v1.0.0-Windows-x64.msi`
- Linux: `WebGenerator-v1.0.0-Linux-x64.tar.gz`

### 发布检查清单

- [ ] 在目标平台测试安装
- [ ] 验证所有功能正常
- [ ] 检查文件大小合理
- [ ] 确认依赖完整
- [ ] 测试卸载过程
- [ ] 验证数字签名（如适用）

### 数字签名（可选）

#### macOS
```bash
# 代码签名
codesign --sign "Developer ID Application: Your Name" WebGenerator.app

# 公证
xcrun notarytool submit WebGenerator.dmg --keychain-profile "notarytool-profile"
```

#### Windows
```bash
# 使用 signtool
signtool sign /f certificate.p12 /p password WebGenerator.msi
```

## 性能优化

### 启动时间优化

1. 延迟导入非关键模块
2. 预编译 Python 字节码
3. 优化资源加载

### 文件大小优化

1. 排除测试文件
2. 压缩资源文件
3. 移除调试信息

## 自动化 CI/CD

### GitHub Actions 示例

```yaml
name: Build and Package

on: [push, pull_request]

jobs:
  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: make install
      - name: Build macOS package
        run: make package-macos
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: macos-dmg
          path: dist/*.dmg

  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install cx_Freeze
      - name: Build Windows package
        run: python scripts/setup.py bdist_msi
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: windows-msi
          path: dist/*.msi
```

## 总结

通过本指南，您可以：

1. 快速打包应用程序
2. 创建专业的安装包
3. 支持多平台分发
4. 解决常见打包问题
5. 优化应用程序性能

如有问题，请参考故障排除部分或提交 Issue。