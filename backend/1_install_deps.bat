@echo off
chcp 65001 >nul
echo ========================================
echo   步骤1：安装依赖（使用 Python 3.10）
echo ========================================
echo.

cd /d "%~dp0"

echo 检测 Python 版本...
echo.

REM 尝试使用 py launcher 指定 Python 3.10
py -3.10 --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✓ 找到 Python 3.10
    set PYTHON_CMD=py -3.10
    goto :install
)

REM 尝试直接使用 python3.10
python3.10 --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✓ 找到 Python 3.10
    set PYTHON_CMD=python3.10
    goto :install
)

REM 检查默认 python 版本
python --version 2>&1 | findstr "3.10" >nul
if %errorlevel% == 0 (
    echo ✓ 默认 Python 是 3.10
    set PYTHON_CMD=python
    goto :install
)

REM 检查 Python 3.9
py -3.9 --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✓ 找到 Python 3.9（也可以使用）
    set PYTHON_CMD=py -3.9
    goto :install
)

echo ✗ 未找到 Python 3.10 或 3.9
echo.
echo 请安装 Python 3.10：
echo https://www.python.org/downloads/release/python-31011/
echo.
echo 安装后重新运行此脚本
pause
exit /b 1

:install
echo 使用命令：%PYTHON_CMD%
%PYTHON_CMD% --version
echo.

echo 清理旧的依赖目录...
if exist python rmdir /s /q python 2>nul
echo.

echo 开始安装依赖...
echo 这可能需要 5-10 分钟，请耐心等待...
echo.

%PYTHON_CMD% -m pip install -r requirements.txt -t python --no-cache-dir

if errorlevel 1 (
    echo.
    echo ✗ 依赖安装失败
    echo.
    echo 尝试使用国内镜像重新安装...
    %PYTHON_CMD% -m pip install -r requirements.txt -t python --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple
    
    if errorlevel 1 (
        echo.
        echo ✗ 依赖安装失败
        echo.
        echo 请检查：
        echo   1. Python 版本：%PYTHON_CMD% --version
        echo   2. pip 版本：%PYTHON_CMD% -m pip --version
        echo   3. 网络连接是否正常
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
echo 📦 依赖已安装到：%cd%\python
echo.
echo 下一步：运行 2_package.bat 进行打包
echo.

pause
