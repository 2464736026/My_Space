@echo off
chcp 65001 >nul
echo ========================================
echo   阿里云函数计算打包工具（含依赖）
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] 清理旧文件...
if exist resume-analyzer.zip del resume-analyzer.zip
if exist python rmdir /s /q python 2>nul
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
if exist app\__pycache__ rmdir /s /q app\__pycache__ 2>nul
if exist app\services\__pycache__ rmdir /s /q app\services\__pycache__ 2>nul
if exist app\utils\__pycache__ rmdir /s /q app\utils\__pycache__ 2>nul
echo ✓ 清理完成
echo.

echo [2/5] 安装依赖到本地...
echo 这可能需要几分钟，请耐心等待...
pip install -r requirements.txt -t python --no-cache-dir
if errorlevel 1 (
    echo ✗ 依赖安装失败
    echo.
    echo 请确保已安装 Python 和 pip
    pause
    exit /b 1
)
echo ✓ 依赖安装完成
echo.

echo [3/5] 验证必要文件...
if not exist "app\main.py" (
    echo ✗ 缺少文件：app\main.py
    pause
    exit /b 1
)
if not exist "index.py" (
    echo ✗ 缺少文件：index.py
    pause
    exit /b 1
)
echo ✓ 文件验证通过
echo.

echo [4/5] 打包代码和依赖...
powershell -Command "Compress-Archive -Path app,index.py,config.py,requirements.txt,python -DestinationPath resume-analyzer.zip -Force"

if not exist resume-analyzer.zip (
    echo ✗ 打包失败
    pause
    exit /b 1
)
echo ✓ 打包成功
echo.

echo [5/5] 压缩包信息：
powershell -Command "Get-Item resume-analyzer.zip | Select-Object Name, @{Name='大小(MB)';Expression={[math]::Round($_.Length/1MB,2)}}"
echo.

echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 📦 文件：%cd%\resume-analyzer.zip
echo.
echo 📝 下一步：
echo    1. 访问阿里云控制台
echo    2. 上传 resume-analyzer.zip
echo    3. 点击"部署"
echo.
echo ⚠️  注意：压缩包包含依赖，可能较大（50-100MB）
echo.

pause
