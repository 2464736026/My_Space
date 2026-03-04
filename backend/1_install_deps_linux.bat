@echo off
chcp 65001 >nul
echo ========================================
echo   安装 Linux 版本的依赖（用于阿里云）
echo ========================================
echo.

cd /d "%~dp0"

echo 清理旧的依赖目录...
if exist python rmdir /s /q python 2>nul
echo.

echo 开始下载 Linux 版本的依赖...
echo 这可能需要 10-15 分钟，请耐心等待...
echo.

REM 尝试使用 py launcher 指定 Python 3.10
py -3.10 --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=py -3.10
    goto :install
)

REM 使用默认 python
set PYTHON_CMD=python

:install
echo 使用命令：%PYTHON_CMD%
%PYTHON_CMD% --version
echo.

echo 下载 Linux x86_64 版本的依赖包...
%PYTHON_CMD% -m pip install -r requirements.txt -t python --platform manylinux2014_x86_64 --only-binary=:all: --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

if errorlevel 1 (
    echo.
    echo ✗ 依赖安装失败
    echo.
    echo 尝试使用官方源重新安装...
    %PYTHON_CMD% -m pip install -r requirements.txt -t python --platform manylinux2014_x86_64 --only-binary=:all: --no-cache-dir
    
    if errorlevel 1 (
        echo.
        echo ✗ 依赖安装失败
        echo.
        echo 可能的原因：
        echo   1. pip 版本太旧（需要 pip 20.3+）
        echo   2. 网络连接问题
        echo.
        echo 请尝试升级 pip：
        echo   %PYTHON_CMD% -m pip install --upgrade pip
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo   依赖安装完成！
echo ========================================
echo.
echo 📦 已安装 Linux 版本的依赖到：%cd%\python
echo.
echo ⚠️  注意：这些依赖只能在 Linux 环境（阿里云 FC）运行
echo    不能在 Windows 本地测试
echo.
echo 下一步：运行 2_package.bat 进行打包
echo.

pause
