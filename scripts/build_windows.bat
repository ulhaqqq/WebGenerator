@echo off
REM Windows 打包脚本
REM 用于在 Windows 系统上构建 Web Generator 安装包

setlocal enabledelayedexpansion

echo ================================================
echo Python Web框架生成器 - Windows 打包脚本
echo ================================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.7 或更高版本
    pause
    exit /b 1
)

echo 当前 Python 版本:
python --version
echo.

REM 检查当前目录是否正确
if not exist "main.py" (
    echo 错误: 请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 创建虚拟环境（如果不存在）
if not exist "venv_build" (
    echo 创建构建虚拟环境...
    python -m venv venv_build
    if errorlevel 1 (
        echo 错误: 虚拟环境创建失败
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv_build\Scripts\activate.bat
if errorlevel 1 (
    echo 错误: 虚拟环境激活失败
    pause
    exit /b 1
)

REM 升级 pip
echo 升级 pip...
python -m pip install --upgrade pip

REM 安装项目依赖
echo 安装项目依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 项目依赖安装失败
    pause
    exit /b 1
)

REM 安装打包依赖
echo 安装打包依赖...
pip install cx_Freeze pyinstaller
if errorlevel 1 (
    echo 错误: 打包依赖安装失败
    pause
    exit /b 1
)

REM 清理之前的构建
echo 清理之前的构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.egg-info" rmdir /s /q "*.egg-info"

REM 构建可执行文件
echo 构建可执行文件...
python setup.py build
if errorlevel 1 (
    echo cx_Freeze 构建失败，尝试使用 PyInstaller...
    
    REM 使用 PyInstaller 作为备选
    pyinstaller --onedir --windowed ^|
        --add-data "generators;generators" ^
        --add-data "templates;templates" ^
        --add-data "utils;utils" ^
        --add-data "screenshots;screenshots" ^
        --name "WebGenerator" ^
        main.py
    
    if errorlevel 1 (
        echo 错误: PyInstaller 构建也失败了
        pause
        exit /b 1
    )
    
    echo PyInstaller 构建成功
) else (
    echo cx_Freeze 构建成功
)

REM 创建 MSI 安装包
echo 创建 MSI 安装包...
python setup.py bdist_msi
if errorlevel 1 (
    echo 警告: MSI 创建失败，但可执行文件已生成
) else (
    echo MSI 安装包创建成功
)

REM 显示结果
echo.
echo ================================================
echo 构建完成！
echo ================================================
echo.

if exist "dist" (
    echo 输出文件:
    dir /b "dist"
    echo.
    echo 文件位置: %cd%\dist\
) else (
    echo 警告: dist 目录不存在
)

if exist "build" (
    echo.
    echo 可执行文件位置:
    for /d %%i in (build\exe.*) do (
        echo   %%i\WebGenerator.exe
    )
else (
    echo 警告: build 目录不存在
)

REM 询问是否测试应用
echo.
set /p test_app="是否测试构建的应用程序？ (y/n): "
if /i "!test_app!"=="y" (
    echo 启动应用程序测试...
    for /d %%i in (build\exe.*) do (
        if exist "%%i\WebGenerator.exe" (
            start "" "%%i\WebGenerator.exe"
            goto :test_done
        )
    )
    echo 未找到可执行文件
    :test_done
)

REM 询问是否打开输出目录
echo.
set /p open_dist="是否打开输出目录？ (y/n): "
if /i "!open_dist!"=="y" (
    if exist "dist" (
        explorer "dist"
    ) else (
        explorer "build"
    )
)

REM 清理虚拟环境询问
echo.
set /p cleanup="是否删除构建虚拟环境？ (y/n): "
if /i "!cleanup!"=="y" (
    deactivate
    rmdir /s /q "venv_build"
    echo 构建虚拟环境已删除
)

echo.
echo 打包完成！按任意键退出...
pause >nul