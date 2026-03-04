@echo off
chcp 65001 >nul
echo ========================================
echo   步骤1：安装依赖
echo ========================================
echo.

cd /d "%~dp0"

echo 清理旧的依赖目录...
if exist python rmdir /s /q python 2>nul
echo.

echo 开始安装依赖...
echo 这可能需要 5-10 分钟，请耐心等待...
echo.

pip install -r requirements.txt -t python --no-cache-dir

if errorlevel 1 (
    echo.
    echo ✗ 依赖安装失败
    echo.
    echo 请检查：
    echo   1. Python 版本：python --version
    echo   2. pip 版本：pip --version
    echo   3. 网络连接是否正常
    echo.
    pause
    exit /b 1
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
