# Web Generator 分发指南

## 📦 构建结果

### macOS 版本 ✅ 已完成
- **应用程序**: `dist/Web Generator.app` (26.8 MB)
- **DMG安装包**: `dist/Web Generator.dmg` (27.1 MB)
- **支持架构**: Apple Silicon (M1/M2) 和 Intel 芯片

### Windows 版本 📋 待构建
- **构建脚本**: `scripts/build_windows_simple.py`
- **需要环境**: Windows 系统
- **输出文件**: `Web Generator.exe`

## 🚀 快速开始

### macOS 用户
1. 下载 `Web Generator.dmg`
2. 双击打开 DMG 文件
3. 将 `Web Generator.app` 拖拽到 Applications 文件夹
4. 在 Applications 中找到并运行 Web Generator

### Windows 用户
1. 在 Windows 系统中运行:
   ```bash
   python scripts/build_windows_simple.py
   ```
2. 构建完成后运行 `dist/Web Generator.exe`

## 🛠️ 构建详情

### macOS 构建过程
```bash
# 1. 安装依赖
pip install pyinstaller

# 2. 构建应用程序
pyinstaller --onefile --windowed --name="Web Generator" main.py

# 3. 创建 DMG 安装包
hdiutil create -volname "Web Generator" -srcfolder "dist/Web Generator.app" -ov -format UDZO "dist/Web Generator.dmg"
```

### Windows 构建过程
```bash
# 在 Windows 系统中运行
python scripts/build_windows_simple.py
```

## 📋 系统要求

### macOS
- macOS 10.13 或更高版本
- 支持 Intel 和 Apple Silicon 芯片
- 约 30 MB 磁盘空间

### Windows
- Windows 10 或更高版本
- Python 3.8+ (仅构建时需要)
- 约 30 MB 磁盘空间

## 🔧 高级配置

### 自定义图标
如需添加自定义图标，请:
1. 准备 `.icns` 文件 (macOS) 或 `.ico` 文件 (Windows)
2. 在构建命令中添加 `--icon=your_icon.icns`

### 代码签名 (macOS)
```bash
# 签名应用程序
codesign --force --deep --sign "Developer ID Application: Your Name" "dist/Web Generator.app"

# 公证应用程序 (可选)
xcrun notarytool submit "dist/Web Generator.dmg" --keychain-profile "notarytool-profile" --wait
```

### 创建 Windows 安装程序
使用 NSIS 或 Inno Setup 创建专业的 Windows 安装程序:

```nsis
; NSIS 脚本示例
Name "Web Generator"
OutFile "Web Generator Setup.exe"
InstallDir "$PROGRAMFILES\Web Generator"

Section
    SetOutPath $INSTDIR
    File "dist\Web Generator.exe"
    CreateShortcut "$DESKTOP\Web Generator.lnk" "$INSTDIR\Web Generator.exe"
SectionEnd
```

## 📁 文件结构

```
web-generator/
├── dist/                          # 构建输出目录
│   ├── Web Generator.app/         # macOS 应用程序包
│   ├── Web Generator.dmg          # macOS DMG 安装包
│   └── Web Generator              # macOS 可执行文件
├── scripts/                       # 构建脚本目录
│   ├── build_windows_simple.py    # Windows 构建脚本
│   ├── setup.py                   # cx_Freeze 配置 (备用)
│   ├── build_package.py           # 自动化构建脚本
│   ├── build_macos.sh             # macOS 构建脚本
│   ├── build_windows.bat          # Windows 批处理脚本
│   └── Makefile                   # 跨平台构建配置
└── requirements-build.txt          # 构建依赖
```

## 🐛 故障排除

### 常见问题

1. **macOS: "无法打开应用程序"**
   - 在系统偏好设置 > 安全性与隐私中允许运行
   - 或右键点击应用程序，选择"打开"

2. **Windows: "缺少 DLL 文件"**
   - 安装 Visual C++ Redistributable
   - 使用 `--hidden-import` 添加缺失的模块

3. **应用程序启动缓慢**
   - 这是正常现象，PyInstaller 打包的应用程序首次启动较慢
   - 后续启动会更快

4. **文件大小过大**
   - 使用 `--exclude-module` 排除不需要的模块
   - 考虑使用 UPX 压缩可执行文件

### 调试模式
```bash
# macOS 调试
./"dist/Web Generator.app/Contents/MacOS/Web Generator"

# Windows 调试
# 移除 --windowed 参数以显示控制台输出
pyinstaller --onefile --name="Web Generator" main.py
```

## 📊 性能优化

### 减小文件大小
```bash
# 排除不需要的模块
pyinstaller --onefile --windowed \
    --exclude-module tkinter \
    --exclude-module matplotlib \
    --name="Web Generator" main.py

# 使用 UPX 压缩 (可选)
upx --best "dist/Web Generator.exe"
```

### 提升启动速度
- 使用 `--onedir` 模式而非 `--onefile`
- 减少导入的模块数量
- 使用延迟导入

## 📝 发布检查清单

- [ ] 应用程序正常启动
- [ ] 所有功能正常工作
- [ ] 图标显示正确
- [ ] 文件关联正确 (如适用)
- [ ] 在目标系统上测试
- [ ] 准备发布说明
- [ ] 更新版本号
- [ ] 创建发布标签

## 🔗 相关资源

- [PyInstaller 官方文档](https://pyinstaller.readthedocs.io/)
- [macOS 应用程序分发指南](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases)
- [Windows 应用程序打包](https://docs.microsoft.com/en-us/windows/msix/)
- [代码签名最佳实践](https://developer.apple.com/documentation/xcode/notarizing-macos-software-before-distribution)

---

**注意**: 本指南基于当前的构建配置。根据项目需求，可能需要调整构建参数和配置。