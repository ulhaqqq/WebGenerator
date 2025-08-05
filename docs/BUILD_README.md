# Web Generator 打包说明

本文档说明如何将 Python Web框架生成器打包成可执行文件和安装包。

## 快速开始

### macOS 用户

```bash
# 方法1: 使用自动化脚本（推荐）
./scripts/build_macos.sh

# 方法2: 使用 Makefile
cd scripts && make package-macos

# 方法3: 使用 Python 脚本
python scripts/build_package.py
```

### Windows 用户

```cmd
REM 方法1: 使用批处理脚本（推荐）
scripts\build_windows.bat

REM 方法2: 使用 Python 脚本
python scripts/build_package.py
```

### Linux 用户

```bash
# 使用 Makefile
make build

# 或使用 Python 脚本
python scripts/build_package.py
```

## 输出文件

### macOS
- **DMG 文件**: `dist/WebGenerator-macOS-{架构}.dmg`
- **可执行文件**: `build/exe.*/WebGenerator`
- **支持架构**: Intel (x86_64) 和 Apple Silicon (arm64)

### Windows
- **MSI 安装包**: `dist/WebGenerator-{版本}-win-amd64.msi`
- **可执行文件**: `build/exe.*/WebGenerator.exe`

### Linux
- **可执行文件**: `build/exe.*/WebGenerator`
- **压缩包**: 可手动创建 tar.gz

## 系统要求

### 开发环境
- Python 3.7 或更高版本
- pip 包管理器
- 足够的磁盘空间（至少 1GB）

### macOS 特定
- macOS 10.14 (Mojave) 或更高版本
- Xcode Command Line Tools
- Homebrew（推荐，用于安装 create-dmg）

### Windows 特定
- Windows 10 或更高版本
- Microsoft Visual C++ 14.0 或更高版本

## 详细步骤

### 1. 准备环境

```bash
# 克隆或下载项目
git clone <repository-url>
cd web-generator

# 安装项目依赖
pip install -r requirements.txt

# 安装打包依赖
pip install -r requirements-build.txt
```

### 2. 选择打包方法

#### 自动化脚本（推荐）

**macOS:**
```bash
./scripts/build_macos.sh
```

**Windows:**
```cmd
scripts\build_windows.bat
```

#### 手动打包

```bash
# 清理之前的构建
make clean

# 构建可执行文件
python scripts/setup.py build

# 创建安装包
# macOS
make package-macos

# Windows
python setup.py bdist_msi
```

### 3. 验证构建

```bash
# 检查输出文件
ls -la dist/
ls -la build/

# 测试可执行文件
# macOS/Linux
./build/exe.*/WebGenerator

# Windows
.\build\exe.*\WebGenerator.exe
```

## 故障排除

### 常见问题

#### 1. cx_Freeze 安装失败

```bash
# 升级 pip
pip install --upgrade pip setuptools

# 重新安装
pip install cx_Freeze
```

#### 2. macOS 权限问题

```bash
# 给脚本添加执行权限
chmod +x build_macos.sh

# 如果遇到安全限制
sudo spctl --master-disable  # 临时禁用 Gatekeeper
```

#### 3. Windows 编译错误

- 安装 Microsoft Visual C++ Build Tools
- 或安装 Visual Studio Community

#### 4. 依赖缺失

```bash
# 检查依赖
pip list | grep -E "cx_Freeze|dmgbuild|pyinstaller"

# 重新安装所有依赖
pip install -r requirements.txt -r requirements-build.txt
```

#### 5. 内存不足

- 关闭其他应用程序
- 增加虚拟内存
- 使用 `--optimize 1` 而不是 `--optimize 2`

### 调试技巧

#### 启用详细输出

```bash
# cx_Freeze 详细模式
python scripts/setup.py build --verbose

# PyInstaller 详细模式
pyinstaller --log-level DEBUG main.py
```

#### 检查依赖

```bash
# macOS
otool -L build/exe.*/WebGenerator

# Linux
ldd build/exe.*/WebGenerator

# Windows
dumpbin /dependents build\exe.*\WebGenerator.exe
```

## 高级配置

### 自定义图标

1. 准备图标文件：
   - macOS: `icon.icns` (512x512)
   - Windows: `icon.ico` (256x256)
   - Linux: `icon.png` (512x512)

2. 更新 `scripts/setup.py` 中的图标路径

### 代码签名

#### macOS

```bash
# 签名应用
codesign --sign "Developer ID Application: Your Name" build/exe.*/WebGenerator

# 验证签名
codesign --verify --verbose build/exe.*/WebGenerator

# 公证（需要 Apple Developer 账户）
xcrun notarytool submit dist/WebGenerator.dmg --keychain-profile "notarytool-profile"
```

#### Windows

```cmd
REM 使用 signtool 签名
signtool sign /f certificate.p12 /p password dist\WebGenerator.msi

REM 验证签名
signtool verify /pa dist\WebGenerator.msi
```

### 优化构建大小

1. 在 `scripts/setup.py` 中排除不需要的模块
2. 使用 `--optimize 2` 进行字节码优化
3. 压缩资源文件
4. 移除调试信息

### 多架构构建

#### macOS 通用二进制

```bash
# 设置架构标志
export ARCHFLAGS="-arch x86_64 -arch arm64"

# 构建通用版本
python scripts/setup.py build

# 验证架构
lipo -info build/exe.*/WebGenerator
```

## 自动化 CI/CD

### GitHub Actions

创建 `.github/workflows/build.yml`：

```yaml
name: Build Packages

on:
  push:
    tags:
      - 'v*'

jobs:
  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-build.txt
      - name: Build macOS package
        run: ./scripts/build_macos.sh
      - name: Upload DMG
        uses: actions/upload-artifact@v3
        with:
          name: macos-dmg
          path: dist/*.dmg

  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-build.txt
      - name: Build Windows package
        run: scripts\build_windows.bat
      - name: Upload MSI
        uses: actions/upload-artifact@v3
        with:
          name: windows-msi
          path: dist/*.msi
```

## 发布检查清单

- [ ] 在目标平台测试安装
- [ ] 验证所有功能正常工作
- [ ] 检查文件大小合理
- [ ] 确认依赖完整
- [ ] 测试卸载过程
- [ ] 验证数字签名（如适用）
- [ ] 更新版本号
- [ ] 创建发布说明

## 支持

如果遇到问题：

1. 查看本文档的故障排除部分
2. 检查 [PACKAGING.md](PACKAGING.md) 获取更详细信息
3. 提交 Issue 到项目仓库
4. 查看项目的 Wiki 页面

## 更新日志

- v1.0.0: 初始版本，支持 macOS 和 Windows 打包
- 计划: 添加 Linux AppImage 支持
- 计划: 添加自动更新功能