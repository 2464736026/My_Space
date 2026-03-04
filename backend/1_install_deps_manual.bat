@echo off
chcp 65001 >nul
echo ========================================
echo   步骤1：安装依赖（手动指定路径）
echo ========================================
echo.

cd /d "%~dp0"

echo 请输入 Python 3.10 的完整路径
echo 例如：C:\Python310\python.exe
echo 或者：C:\Users\你的用户名\AppData\Local\Programs\Python\Python310\python.exe
echo.
set /p PYTHON_PATH="Python 3.10 路径: "

echo.
echo 验证 Python 版本...
"%PYTHON_PATH%" --version

if errorlevel 1 (
    echo ✗ 无法运行 Python
    echo 请检查路径是否正确
    pause
    exit /b 1
)

echo.
echo 清理旧的依赖目录...
if exist python rmdir /s /q python 2>nul
echo.

echo 开始安装依赖...
echo 这可能需要 5-10 分钟，请耐心等待...
echo.

"%PYTHON_PATH%" -m pip install -r requirements.txt -t python --no-cache-dir

if errorlevel 1 (
    echo.
    echo ✗ 依赖安装失败
    echo.
    echo 尝试使用国内镜像重新安装...
    "%PYTHON_PATH%" -m pip install -r requirements.txt -t python --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple
    
    if errorlevel 1 (
        echo.
        echo ✗ 依赖安装失败
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
