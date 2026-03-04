@echo off
chcp 65001 >nul
echo ========================================
echo   查找已安装的 Python 版本
echo ========================================
echo.

echo 方法1：使用 py launcher
echo.
py -0
echo.

echo ========================================
echo.
echo 方法2：检查常见安装位置
echo.

set FOUND=0

if exist "C:\Python310\python.exe" (
    echo ✓ 找到：C:\Python310\python.exe
    C:\Python310\python.exe --version
    set FOUND=1
    echo.
)

if exist "C:\Python39\python.exe" (
    echo ✓ 找到：C:\Python39\python.exe
    C:\Python39\python.exe --version
    set FOUND=1
    echo.
)

if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    echo ✓ 找到：%LOCALAPPDATA%\Programs\Python\Python310\python.exe
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" --version
    set FOUND=1
    echo.
)

if exist "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" (
    echo ✓ 找到：%LOCALAPPDATA%\Programs\Python\Python39\python.exe
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" --version
    set FOUND=1
    echo.
)

if %FOUND%==0 (
    echo ✗ 未在常见位置找到 Python 3.10 或 3.9
    echo.
    echo 请手动查找 Python 安装目录
)

echo ========================================
echo.
echo 使用说明：
echo 1. 如果找到了 Python 3.10 或 3.9，复制其完整路径
echo 2. 运行 1_install_deps_manual.bat
echo 3. 粘贴路径并按回车
echo.

pause
